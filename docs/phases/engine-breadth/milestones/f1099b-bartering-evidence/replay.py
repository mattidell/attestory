"""Full-surface replay of the recorded lists: published v96 against the scratch v97.

Run: python3 replay.py <scratch-core.json> --variant q|qf --shard I/N --part <part-file-outside-repo>
     python3 replay.py <scratch-core.json> --variant q|qf --summarize <part-files...> --out replay-<variant>.json
     python3 replay.py <scratch-core.json> --variant q|qf --probe --part <part-file-outside-repo>
     python3 replay.py --census --out census.json

Uses tools/recorded_replay.py (`run_full` with the expectations below): every
saved page field, attachment, explanation-graph node and report row on both
cores, strict, with every difference no expectation names failing the list.
The census reads every recorded act list for a Form 1099-B box 13 or
bartering fact, and for the answers to the five facts that share the
Schedule 1 lines 2a-6 question.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools import recorded_replay as rr  # noqa: E402

P = "tax.us.2025."
SHARED = tuple(P + "schedule1-part1-scope." + s for s in (
    "no-sch1-line2a-alimony", "no-sch1-line3-business", "no-sch1-line4-other-gains", "no-sch1-line5-rental",
    "no-sch1-line6-farm"))
OTHER = P + "w2g-scope.no-sch1-other-income-except-w2g"


def expectations(variant: str) -> list[rr.Expectation]:
    rows = [r for r in json.loads((HERE / "wording.json").read_text())["replacements"] if variant in r["variants"]]
    build = json.loads((HERE / f"build-{variant}.json").read_text())
    out: list[rr.Expectation] = []
    question = {(r["old"], r["new"]) for r in rows if r["property"] == "question"}
    for old, new in sorted(question):
        out.append(rr.Expectation(("page", "model", "graph", "row", "report", "attachment"), r".*", "", "changed", old, new,
                                  "the Schedule 1 lines 2a-6 question names box 13 bartering"))
    for r in rows:
        if r["property"] != "question":
            out.append(rr.Expectation(("page", "model", "graph", "row", "report", "attachment"), r".*" + re.escape(r["property"].split(".")[-1]),
                                      rr._id_pattern(r["id"]), "changed", r["old"], r["new"],
                                      "the Schedule 1 line 10 guard sentence names its causes"))
    for s in build["successors"]:
        out.append(rr.version_change(s["id"], s["old_version"], s["new_version"]))
    out.append(rr.version_change(P + "package.core-calculations", "v96", "v97"))
    return out


def census() -> dict:
    lists = rr.recorded_lists()
    counts: Counter = Counter()
    box13: list[str] = []
    shared_answers: Counter = Counter()
    other_answers: Counter = Counter()
    for key, acts in lists:
        text = json.dumps(acts).lower()
        if "barter" in text or re.search(r"f1099b[^\"|]*box-?13", text):
            box13.append(key)
        values = {}
        for act in acts:
            finding = (act.get("payload") or {}).get("finding") or {}
            fid = str(finding.get("fact_id", ""))
            for fact in (*SHARED, OTHER):
                if fid.startswith(fact + "|"):
                    values[fact] = finding.get("value")
        shared_answers["/".join(str(values.get(f)) for f in SHARED)] += 1
        other_answers[str(values.get(OTHER))] += 1
        counts[key.split("/")[0]] += 1
    return {"lists": len(lists), "by_source": dict(sorted(counts.items())),
            "lists_with_a_box13_or_bartering_fact": box13,
            "shared_lines_2a_6_answers (alimony/business/other-gains/rental/farm)": dict(shared_answers.most_common()),
            "other_income_except_w2g_answer": dict(other_answers.most_common())}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("core", nargs="?")
    parser.add_argument("--variant", choices=("q", "qf"), default="q")
    parser.add_argument("--shard", default="0/1")
    parser.add_argument("--part")
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--summarize", nargs="*")
    parser.add_argument("--census", action="store_true")
    parser.add_argument("--keys", default="")
    parser.add_argument("--probe", action="store_true", help="the probe.py lists instead of the recorded lists")
    parser.add_argument("--out")
    args = parser.parse_args()
    if args.census:
        body = census()
        Path(args.out).write_text(json.dumps(body, indent=1) + "\n", encoding="utf-8")
        print(json.dumps({k: v for k, v in body.items() if k != "by_source"}, indent=1)[:3000])
        return
    specs = expectations(args.variant)
    if args.summarize:
        results: dict = {}
        for part in args.summarize:
            results.update(json.loads(Path(part).read_text(encoding="utf-8"))["results"])
        summary = rr.run_full("v96", args.core, specs, lists=[], workers=1)  # fingerprints only
        summary = _summary(results, specs, summary["cores"])
        summary["variant"] = args.variant
        text = json.dumps(summary, indent=1) + "\n"
        rr._check_no_local_paths(text, "summary")
        Path(args.out).write_text(text, encoding="utf-8")
        print(json.dumps({k: summary[k] for k in ("lists", "classes", "passing", "failing", "unexpected_differences",
                                                   "expectations_declared", "expectations_used", "outcomes")}, indent=1))
        return
    index, total = (int(x) for x in args.shard.split("/"))
    if args.probe:
        probe = rr._module("bart_p0_probe", HERE / "probe.py")
        lists = [(f"probe/{key}", probe.build(key, rr.CONTENT)) for key in probe.KEYS]
        from tests import evidence_loader  # as rr.recorded_lists does, release the loader before spawning workers

        owner = evidence_loader.current_owner()
        if owner:
            evidence_loader.release(owner)
    else:
        lists = rr.recorded_lists()
    if args.keys:
        wanted = set(args.keys.split(","))
        lists = [item for item in lists if item[0] in wanted]
    lists = lists[index::total]
    started = time.monotonic()
    summary = rr.run_full("v96", args.core, specs, workers=args.workers, part=args.part, lists=lists)
    print(json.dumps({"shard": args.shard, "wall_time_s": round(time.monotonic() - started, 1),
                      **{k: summary[k] for k in ("lists", "classes", "passing", "failing", "unexpected_differences",
                                                 "expectations_used", "outcomes")},
                      "unexpected": {k: v["lists"] for k, v in summary["unexpected_by_kind_attribute"].items()}}, indent=1))


def _summary(results: dict, specs: list, cores: list) -> dict:
    classes = Counter(row["class"] for row in results.values())
    used = {i for row in results.values() for i in row.get("used", [])}
    by_attribute: dict = {}
    for key, row in results.items():
        for item in row["unexpected"]:
            slot = by_attribute.setdefault(f"{item['kind']}|{item['change']}|{re.sub(r'[0-9]+', 'N', item['attribute'])}",
                                           {"lists": set(), "samples": []})
            slot["lists"].add(key)
            if len(slot["samples"]) < 3:
                slot["samples"].append({"list": key, **item})
    return {
        "format": "full-surface-replay.v1", "cores": cores, "lists": len(results),
        "classes": dict(sorted(classes.items())),
        "passing": sum(1 for r in results.values() if r["class"] != "unexpected"),
        "failing": sum(1 for r in results.values() if r["class"] == "unexpected"),
        "unexpected_differences": sum(r["unexpected_total"] for r in results.values()),
        "unexpected_by_kind_attribute": {k: {"lists": len(v["lists"]), "samples": v["samples"]} for k, v in sorted(by_attribute.items())},
        "expectations_declared": len(specs), "expectations_used": len(used),
        "unused_expectations": [rr.describe_expectation(s) for i, s in enumerate(specs) if i not in used],
        "expected_by_note": dict(sorted(sum((Counter(r["expected_by_note"]) for r in results.values()), Counter()).items())),
        "outcomes": dict(sorted(Counter("/".join(r["outcomes"]) for r in results.values()).items())),
        "list_classes": {k: r["class"] for k, r in sorted(results.items())},
        "failing_lists": {k: r["unexpected_total"] for k, r in sorted(results.items()) if r["class"] == "unexpected"},
    }


if __name__ == "__main__":
    main()
