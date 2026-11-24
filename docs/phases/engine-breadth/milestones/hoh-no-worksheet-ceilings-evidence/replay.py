"""Full-surface replay of published v102 against the scratch ceiling successor.

Run: python3 replay.py <scratch-core.json> --shard I/N --part <part-file>
     python3 replay.py <scratch-core.json> --summarize <part-files...> --out replay.json
     python3 replay.py <scratch-core.json> --pilot --out <pilot.json>
     python3 replay.py --census --out census.json

Uses tools/recorded_replay.py. Every saved page field, attachment,
explanation-graph node and report row is compared. A difference no
expectation names fails the list. Expectations name rule and package
versions only. A numeric value that changes does not match them.
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
LINE6 = P + "rule.qdcg-worksheet.line-6"
LINE13 = P + "rule.qdcg-worksheet.line-13"
PACKAGE = P + "package.core-calculations"


def expectations() -> list[rr.Expectation]:
    return [
        rr.version_change(LINE6, "v1", "v2", "worksheet line 6 reads the status-test answer"),
        rr.version_change(LINE13, "v1", "v2", "worksheet line 13 reads the status-test answer"),
        rr.version_change(PACKAGE, "v102", "v103", "scratch package version"),
    ]


def census() -> dict:
    lists = rr.recorded_lists()
    status: Counter = Counter()
    for _key, acts in lists:
        found = None
        for act in acts:
            payload = act.get("payload") or {}
            finding = payload.get("finding") or (payload.get("member") or {}).get("finding") or {}
            if str(finding.get("fact_id", "")).startswith(P + "filing-status|"):
                found = finding.get("value")
        status[str(found)] += 1
    return {"lists": len(lists), "filing_status": dict(status.most_common())}


def _summary(results: dict, specs: list, cores: list) -> dict:
    classes = Counter(row["class"] for row in results.values())
    used = {index for row in results.values() for index in row.get("used", [])}
    number_changes = []
    by_attribute: dict = {}
    for key, row in results.items():
        for item in row.get("unexpected") or []:
            slot = by_attribute.setdefault(
                f"{item['kind']}|{item['change']}|{re.sub(r'[0-9]+', 'N', item['attribute'])}",
                {"lists": set(), "samples": []},
            )
            slot["lists"].add(key)
            if len(slot["samples"]) < 2:
                sample = {"list": key, "identity": str(item.get("identity", ""))[:180],
                          "attribute": item.get("attribute"), "before": item.get("before"), "after": item.get("after")}
                slot["samples"].append(sample)
            before, after = item.get("before"), item.get("after")
            if item.get("attribute") in {"value", "amount"} and before != after and (
                isinstance(before, (int, float)) or isinstance(after, (int, float))
            ):
                number_changes.append(key)
    return {
        "format": "full-surface-replay.v1",
        "cores": cores,
        "lists": len(results),
        "classes": dict(sorted(classes.items())),
        "passing": sum(1 for row in results.values() if row["class"] != "unexpected"),
        "failing": sum(1 for row in results.values() if row["class"] == "unexpected"),
        "unexpected_differences": sum(row.get("unexpected_total", 0) for row in results.values()),
        "number_change_lists": sorted(set(number_changes)),
        "unexpected_by_kind_attribute": {
            key: {"lists": len(value["lists"]), "samples": value["samples"]} for key, value in sorted(by_attribute.items())
        },
        "expectations_declared": len(specs),
        "expectations_used": len(used),
        "unused_expectations": [rr.describe_expectation(spec) for index, spec in enumerate(specs) if index not in used],
        "expected_by_note": dict(sorted(sum((Counter(row.get("expected_by_note") or {}) for row in results.values()), Counter()).items())),
        "outcomes": dict(sorted(Counter("/".join(row.get("outcomes") or []) for row in results.values()).items())),
        "list_classes": {key: row["class"] for key, row in sorted(results.items())},
    }


def _check(text: str, label: str) -> None:
    rr._check_no_local_paths(text, label)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("core", nargs="?")
    parser.add_argument("--shard", default="0/1")
    parser.add_argument("--part")
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--summarize", nargs="*")
    parser.add_argument("--census", action="store_true")
    parser.add_argument("--pilot", action="store_true")
    parser.add_argument("--out")
    args = parser.parse_args()
    if args.census:
        body = census()
        text = json.dumps(body, indent=1) + "\n"
        _check(text, "census")
        Path(args.out).write_text(text, encoding="utf-8")
        print(text)
        return
    specs = expectations()
    cores = [rr.core_fingerprint("v102"), rr.core_fingerprint(args.core)]
    if args.summarize:
        results: dict = {}
        for part in args.summarize:
            results.update(json.loads(Path(part).read_text(encoding="utf-8"))["results"])
        summary = _summary(results, specs, cores)
        text = json.dumps(summary, indent=1) + "\n"
        _check(text, "summary")
        Path(args.out).write_text(text, encoding="utf-8")
        print(json.dumps({key: summary[key] for key in (
            "lists", "classes", "passing", "failing", "unexpected_differences", "number_change_lists",
            "expectations_declared", "expectations_used", "expected_by_note", "outcomes",
        )}, indent=1))
        return
    if args.pilot:
        lists = rr.recorded_lists()
        key, acts = lists[0]
        started = time.monotonic()
        row = rr.FullSurfaceCompare(specs, max_unexpected=30)(key, acts, (rr.resolve_core("v102"), rr.resolve_core(args.core)))
        body = {"list": key, "wall_time_s": round(time.monotonic() - started, 1), **row}
        text = json.dumps(body, indent=1) + "\n"
        _check(text, "pilot")
        Path(args.out).write_text(text, encoding="utf-8")
        print(json.dumps({"list": key, "class": row["class"], "unexpected_total": row["unexpected_total"],
                          "expected_by_note": row["expected_by_note"], "outcomes": row["outcomes"],
                          "sample": row["unexpected"][:8]}, indent=1)[:8000])
        return
    index, total = (int(part) for part in args.shard.split("/"))
    lists = rr.recorded_lists()[index::total]
    started = time.monotonic()
    results = rr.replay(lists, (rr.resolve_core("v102"), rr.resolve_core(args.core)), rr.FullSurfaceCompare(specs),
                        workers=args.workers, part=args.part)
    summary = _summary(results, specs, cores)
    print(json.dumps({"shard": args.shard, "wall_time_s": round(time.monotonic() - started, 1),
                      **{key: summary[key] for key in (
                          "lists", "classes", "passing", "failing", "unexpected_differences", "number_change_lists",
                          "expected_by_note", "outcomes")}}, indent=1))


if __name__ == "__main__":
    main()
