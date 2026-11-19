"""Full-surface replay: published v97 against the scratch v98 (head of household and qualifying surviving spouse tests).

Run: python3 replay.py <scratch-core.json> --shard I/N --part <part-file-outside-repo>
     python3 replay.py <scratch-core.json> --summarize <part-files...> --out replay-q.json
     python3 replay.py <scratch-core.json> --probe --part <part-file-outside-repo>
     python3 replay.py <scratch-core.json> --paired --out replay-paired.json
     python3 replay.py --census --out census.json

Uses tools/recorded_replay.py (`run_full` with the expectations below): every
saved page field, attachment, explanation-graph node and report row on both
cores, strict, every difference no expectation names failing the list.
``--probe`` replays the probe.py lists instead (each hoh and qss case
unanswered, answered yes and answered no; the other cases once), which reach
the surfaces the recorded lists do not. Its expectations are the same: a
refused or unanswered list is meant to fail with the line 12e chain blocked,
and every other probe list is meant to pass.
``--paired`` compares, for each head of household and qualifying surviving
spouse probe case, the list a v97 filer has (no answer) on v97 against the same
list answered yes on the scratch core, in process: every difference is
counted, and every difference outside the explanation graph, pins, citation
sites and generated finding or act ids is listed (a qualifying filer must see
no other change).
The census reads every recorded act list for its filing status and for any
child, other dependent or relative it records.
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
RULE = P + "rule.dependents-worksheet-line-3"
DEPENDENT_PREFIXES = ("eic.child.", "ctc.child.", "odc.child.", "odc.dependent.", "dtb.child.")


def _design():
    return rr._module("hoh_p0_design", HERE / "design.py")


def expectations() -> list[rr.Expectation]:
    d = _design()
    question = {d.HOH: d.HOH_QUESTION, d.QSS: d.QSS_QUESTION}
    out: list[rr.Expectation] = [
        rr.version_change(RULE, "v1", "v2", "the standard deduction base rule reads the status tests"),
        rr.version_change(P + "package.core-calculations", "v97", "v98"),
    ]
    # Seen only where a head of household or qualifying surviving spouse return leaves the answer
    # unanswered or answers no (the probe lists): the page shows the question.
    for fact, text in question.items():
        out.append(rr.Expectation(("page", "model"), r".*(?:questions|reasons|blocked_reasons).*", "", None, rr.ANY,
                                  text, f"question shown:{fact.removeprefix(P)}"))
    return out


def census() -> dict:
    lists = rr.recorded_lists()
    status: Counter = Counter()
    dependents: Counter = Counter()
    by_source: Counter = Counter()
    for key, acts in lists:
        found = None
        kinds: set[str] = set()
        for act in acts:
            payload = act.get("payload") or {}
            finding = payload.get("finding") or (payload.get("member") or {}).get("finding") or {}
            fid = str(finding.get("fact_id", ""))
            if fid.startswith(P + "filing-status|"):
                found = finding.get("value")
            for prefix in DEPENDENT_PREFIXES:
                if fid.startswith(P + prefix):
                    kinds.add(prefix.rstrip("."))
        status[str(found)] += 1
        dependents[f"{found}: " + (", ".join(sorted(kinds)) or "none")] += 1
        by_source[key.split("/")[0]] += 1
    return {"lists": len(lists), "by_source": dict(sorted(by_source.items())),
            "filing_status": dict(status.most_common()),
            "status_and_recorded_dependents": dict(dependents.most_common())}


def probe_lists(core_content: Path) -> list:
    probe = rr._module("hoh_p0_probe", HERE / "probe.py")
    out = []
    for key in probe.KEYS:
        answers = ("none", "yes", "no") if key.split("/")[0] in probe.QUESTION else ("none",)
        for answer in answers:
            out.append((f"probe/{key}/{answer}", probe.build(key, core_content, answer)))
    return out


IDENTITY_ONLY = re.compile(r"pins|edges|citationSites|pinId|finding~|act~|records\[|\|(?:finding_id|act_id)$")


def paired(core_spec: str) -> dict:
    core = rr.resolve_core(core_spec)
    probe = rr._module("hoh_p0_probe", HERE / "probe.py")
    out: dict = {"format": "hoh-paired.v1", "cores": [rr.core_fingerprint("v97"), rr.core_fingerprint(core)],
                 "compared": "v97 on the list with no answer, against the scratch core on the same list answered yes",
                 "substantive_filter": "differences outside kind graph whose identity and attribute name no pin, edge, "
                                       "citation site, generated finding id or act id (a row's finding_id and act_id are hashes of its pins, so "
                                       "they move on every row downstream of the line that now pins the answer; "
                                       "generated_id_rows counts those rows)",
                 "cases": {}}
    for key in probe.KEYS:
        if key.split("/")[0] not in probe.QUESTION:
            continue
        run_id = "demo.fsr.hoh." + key.replace("/", ".")
        before = rr.snapshot_run("v97", probe.build(key, core.content, "none"), run_id)
        after = rr.snapshot_run(core, probe.build(key, core.content, "yes"), run_id)
        diffs = rr.diff_snapshots(before, after)
        substantive = [d for d in diffs if d["kind"] != "graph"
                       and not IDENTITY_ONLY.search(d["identity"] + "|" + d["attribute"])]
        generated = sorted({d["identity"] for d in diffs if d["kind"] == "row" and d["attribute"] in ("finding_id", "act_id")})
        out["cases"][key] = {
            "generated_id_rows": generated,
            "outcomes": [before["outcome"], after["outcome"]],
            "differences": len(diffs),
            "by_kind_change": dict(sorted(Counter(f"{d['kind']}|{d['change']}" for d in diffs).items())),
            "substantive": len(substantive),
            "substantive_by_attribute": dict(sorted(Counter(f"{d['kind']}|{d['attribute']}" for d in substantive).items())),
            "substantive_rows": sorted({d["identity"] for d in substantive}),
        }
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("core", nargs="?")
    parser.add_argument("--shard", default="0/1")
    parser.add_argument("--part")
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--summarize", nargs="*")
    parser.add_argument("--census", action="store_true")
    parser.add_argument("--keys", default="")
    parser.add_argument("--probe", action="store_true", help="the probe.py lists instead of the recorded lists")
    parser.add_argument("--paired", action="store_true")
    parser.add_argument("--out")
    args = parser.parse_args()
    if args.paired:
        body = paired(args.core)
        text = json.dumps(body, indent=1) + "\n"
        rr._check_no_local_paths(text, "paired")
        Path(args.out).write_text(text, encoding="utf-8")
        print(json.dumps({k: {x: v[x] for x in ("outcomes", "differences", "substantive", "substantive_by_attribute")}
                          for k, v in body["cases"].items()}, indent=1))
        return
    if args.census:
        body = census()
        Path(args.out).write_text(json.dumps(body, indent=1) + "\n", encoding="utf-8")
        print(json.dumps(body, indent=1)[:3000])
        return
    specs = expectations()
    if args.summarize:
        results: dict = {}
        for part in args.summarize:
            results.update(json.loads(Path(part).read_text(encoding="utf-8"))["results"])
        summary = rr.run_full("v97", args.core, specs, lists=[], workers=1)  # fingerprints only
        summary = _summary(results, specs, summary["cores"])
        summary["lists_set"] = "probe" if args.probe else "recorded"
        text = json.dumps(summary, indent=1) + "\n"
        rr._check_no_local_paths(text, "summary")
        Path(args.out).write_text(text, encoding="utf-8")
        print(json.dumps({k: summary[k] for k in ("lists", "classes", "passing", "failing", "unexpected_differences",
                                                   "expectations_declared", "expectations_used", "outcomes")}, indent=1))
        return
    index, total = (int(x) for x in args.shard.split("/"))
    if args.probe:
        lists = probe_lists(rr.resolve_core(args.core).content)  # the scratch content holds the new bundle
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
    summary = rr.run_full("v97", args.core, specs, workers=args.workers, part=args.part, lists=lists)
    print(json.dumps({"shard": args.shard, "wall_time_s": round(time.monotonic() - started, 1),
                      **{k: summary[k] for k in ("lists", "classes", "passing", "failing", "unexpected_differences",
                                                 "expectations_used", "outcomes")},
                      "unexpected": {k: v["lists"] for k, v in summary["unexpected_by_kind_attribute"].items()}}, indent=1))


def _summary(results: dict, specs: list, cores: list) -> dict:
    classes = Counter(row["class"] for row in results.values())
    used = {i for row in results.values() for i in row.get("used", [])}
    used_by: dict = {}
    for key, row in results.items():
        for i in row.get("used", []):
            used_by.setdefault(i, []).append(key)
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
        "expectation_lists": {rr.describe_expectation(s)["note"]: (len(used_by.get(i, [])) if len(used_by.get(i, [])) > 12
                                                                     else sorted(used_by.get(i, [])))
                              for i, s in enumerate(specs)},
        "expected_by_note": dict(sorted(sum((Counter(r["expected_by_note"]) for r in results.values()), Counter()).items())),
        "outcomes": dict(sorted(Counter("/".join(r["outcomes"]) for r in results.values()).items())),
        "list_classes": {k: r["class"] for k, r in sorted(results.items())},
        "failing_lists": {k: r["unexpected_total"] for k, r in sorted(results.items()) if r["class"] == "unexpected"},
    }


if __name__ == "__main__":
    main()
