"""P0 path-dependent scan: declared required inputs that a published finding did not read.

Reads the JSON-lines dumps written by p0_path_probe.py. Each published finding
carries, for every symbol in its rule's declared `requires`, the status the
runner recorded when it published: `pinned` (read on this path, so the pin is
in the finding), or `unpinned` / `no-source` / `collected-unpinned` (declared
but not read, so a correction to it would not displace the finding).

Usage (repository root):
  python3 <this file> <dump-dir> [--json <out.json>]
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([".."] * 5)))
sys.path.insert(0, HERE)
from p0_static_scan import CONTENT, index_content  # noqa: E402

ABSENT = {"unpinned", "no-source", "collected-unpinned"}


def latest_core_members() -> set[str]:
    """Rule id@version members of the highest-numbered core-calculations package."""
    best = None
    for path in glob.glob(os.path.join(CONTENT, "**", "package.core-calculations.v*.json"), recursive=True):
        with open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
        number = int(str(doc["version"]).lstrip("v"))
        if best is None or number > best[0]:
            best = (number, doc)
    members = set()
    for member in best[1].get("members", []):
        if member.get("role") == "computation":
            members.add(f"{member['id']}@{member['version']}")
    return members


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("dump_dir")
    parser.add_argument("--json", dest="json_out")
    args = parser.parse_args()

    index = index_content()
    latest_members = latest_core_members()
    records: dict[tuple[str, str], dict] = {}
    for path in sorted(glob.glob(os.path.join(args.dump_dir, "probe-*.jsonl"))):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                row = json.loads(line)
                records.setdefault((row["test"], row["finding_id"]), row)

    stats = collections.Counter()
    rules: dict[str, dict] = {}
    for (test, _fid), row in sorted(records.items()):
        stats["published findings"] += 1
        if not row["rule_pins"]:
            stats["published without a rule pin (input or default finding)"] += 1
            continue
        if not row["matched"]:
            stats["published with a rule pin but no matching pins_for record"] += 1
            continue
        stats["matched to a rule evaluation"] += 1
        rule_pin = row["rule_pins"][0]
        found = index.get((rule_pin["id"], str(rule_pin["version"])))
        if found is None:
            stats["rule file not found"] += 1
            continue
        rule_path, rule = found
        key = f"{rule['id']}@{rule['version']}"
        entry = rules.setdefault(key, {
            "file": os.path.relpath(rule_path, ROOT), "findings": 0, "tests": set(),
            "absent_count": collections.Counter(), "status": collections.defaultdict(collections.Counter),
            "findings_with_absent": 0, "example": {},
        })
        entry["findings"] += 1
        entry["tests"].add(test)
        absent_here = False
        for sym, state in (row["statuses"] or {}).items():
            entry["status"][sym][state["status"]] += 1
            if state["status"] in ABSENT:
                entry["absent_count"][sym] += 1
                entry["example"].setdefault(sym, test)
                absent_here = True
        if absent_here:
            entry["findings_with_absent"] += 1

    print("PATH-DEPENDENT SCAN: declared required inputs not read on a published finding's path")
    print(f"dump dir: {os.path.basename(os.path.normpath(args.dump_dir))}")
    for name in sorted(stats):
        print(f"{name}: {stats[name]}")
    print()
    print("Rule versions with at least one absent required input. 'never read' = absent on every"
          " published finding of that rule in the run; 'path-dependent' = absent on some findings only.")
    print("rule version | in latest core package | published findings | tests | findings with an absent input | never read (symbol: findings) | path-dependent (symbol: absent/findings)")
    summary = {}
    for key in sorted(rules):
        entry = rules[key]
        if not entry["absent_count"]:
            continue
        never, partial = [], []
        for sym in sorted(entry["absent_count"]):
            absent = entry["absent_count"][sym]
            if absent == entry["findings"]:
                never.append(f"{sym}: {absent}")
            else:
                partial.append(f"{sym}: {absent}/{entry['findings']}")
        print(f"{key} | {'yes' if key in latest_members else 'no'} | {entry['findings']} | {len(entry['tests'])} | {entry['findings_with_absent']} | "
              f"{'; '.join(never) or '-'} | {'; '.join(partial) or '-'}")
        summary[key] = {
            "file": entry["file"], "findings": entry["findings"], "tests": len(entry["tests"]),
            "findings_with_absent": entry["findings_with_absent"],
            "in_latest_core_package": key in latest_members,
            "absent_findings_by_symbol": dict(sorted(entry["absent_count"].items())),
            "status_by_symbol": {s: dict(c) for s, c in sorted(entry["status"].items())},
            "example_test": entry["example"],
        }
    print()
    print(f"rule versions published in the run: {len(rules)}")
    print(f"rule versions with an absent required input on at least one published finding: {len(summary)}")
    never_total = sum(1 for k in summary for s, n in summary[k]["absent_findings_by_symbol"].items()
                      if n == summary[k]["findings"])
    print(f"rule-symbol pairs absent on every published finding of their rule: {never_total}")
    print(f"rule-symbol pairs absent on some but not all published findings: "
          f"{sum(len(summary[k]['absent_findings_by_symbol']) for k in summary) - never_total}")
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump({"stats": dict(stats), "rules": summary}, fh, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
