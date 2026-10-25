"""Required-versus-read check.

A rule's ``requires`` list names the inputs a person is asked for and whose
later correction must displace the rule's result. An input that no part of the
rule reads is a defect of two kinds:

* **Static:** a required symbol that no expression, selection path, or
  dependency set in the rule references at all. Checked here, in CI, through
  ``tests/test_required_versus_read.py``.
* **Path-dependent:** a symbol referenced only on branches that a publishing
  run never takes. Only runs show it, and the path scan is slow because it
  also measures test coverage, so it is an on-demand tool, not a CI gate.

Usage (repository root)::

    python3 tools/required_versus_read.py static
    python3 tools/required_versus_read.py path <test module>...

``static`` exits 1 on any required symbol that is neither read nor listed in
``tools/required_versus_read_allowlist.json``. ``path`` runs the given pytest
modules with ``tools/required_versus_read_probe.py`` and prints, for each
published finding, which of its rule's required inputs its runtime pins lack.
"""

from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTENT = REPO_ROOT / "packages" / "content" / "tax"
ALLOWLIST = REPO_ROOT / "tools" / "required_versus_read_allowlist.json"
ABSENT_STATUSES = {"unpinned", "no-source", "collected-unpinned"}

# Operations whose ``name`` reads a symbol from the environment. Source:
# packages/derivation/evaluator.py, ``_evaluate`` and ``_eval_categorical_operand``.
READ_NAME_OPS = {"ref", "collect", "count", "bound_sources", "collect_categorical_all_equal"}
# Operations that read named keyed sources (``links``, ``reductions``) or a
# fact type. Source: ``_link_coverage``, ``_link_count``, ``_shared_key_count``.
READ_LIST_KEYS = {
    "link_coverage": ("links", "reductions"),
    "link_count": ("links",),
    "shared_key_count": ("fact_type",),
}
# Top-level rule keys that are declarations, not evaluated expressions.
NON_EXPRESSION_KEYS = {
    "requires", "pins", "blocked", "citations", "notes", "publishes", "id",
    "version", "scope", "schema", "role", "subject", "joined", "direction",
    "wording", "title", "composition", "accounts_for", "selection",
    "attachment", "completeness", "requirement", "itemizations", "fields",
}


def walk_reads(node: Any, reads: set[str]) -> None:
    if isinstance(node, dict):
        op = node.get("op")
        if op in READ_NAME_OPS and isinstance(node.get("name"), str):
            reads.add(node["name"])
        if op in READ_LIST_KEYS:
            for key in READ_LIST_KEYS[op]:
                value = node.get(key)
                if isinstance(value, str):
                    reads.add(value)
                elif isinstance(value, list):
                    reads.update(v for v in value if isinstance(v, str))
        for key, value in node.items():
            if key == "reads_subject_results" and isinstance(value, list):
                for item in value:
                    if isinstance(item, dict) and isinstance(item.get("symbol"), str):
                        reads.add(item["symbol"])
                continue
            if key == "member_fact_types" and isinstance(value, list):
                # selection activity: presence of a member fact type in a source
                for item in value:
                    if isinstance(item, dict) and isinstance(item.get("id"), str):
                        reads.add(item["id"])
                continue
            walk_reads(value, reads)
    elif isinstance(node, list):
        for item in node:
            walk_reads(item, reads)


def rule_requires(rule: dict[str, Any]) -> dict[str, str]:
    """Map each required symbol to its origin: top, selection-path:<id>, or selection-default."""
    origin: dict[str, str] = {}
    for sym in rule.get("requires", []) or []:
        origin.setdefault(sym, "top")
    selection = rule.get("selection")
    if isinstance(selection, dict):
        for path in selection.get("paths", []) or []:
            for sym in path.get("requires", []) or []:
                origin.setdefault(sym, "selection-path:" + str(path.get("id")))
        default = selection.get("default")
        if isinstance(default, dict):
            for sym in default.get("requires", []) or []:
                origin.setdefault(sym, "selection-default")
    return origin


def rule_reads(rule: dict[str, Any]) -> set[str]:
    reads: set[str] = set()
    for key, value in rule.items():
        if key in NON_EXPRESSION_KEYS:
            continue
        walk_reads(value, reads)
    selection = rule.get("selection")
    if isinstance(selection, dict):
        walk_reads(selection.get("paths", []), reads)
        walk_reads(selection.get("default", {}), reads)
        walk_reads(selection.get("refusal", {}), reads)
        for path in selection.get("paths", []) or []:
            if isinstance(path, dict):
                for item in path.get("reads_subject_results", []) or []:
                    if isinstance(item, dict) and isinstance(item.get("symbol"), str):
                        reads.add(item["symbol"])
        default = selection.get("default")
        if isinstance(default, dict):
            for item in default.get("reads_subject_results", []) or []:
                if isinstance(item, dict) and isinstance(item.get("symbol"), str):
                    reads.add(item["symbol"])
    return reads


def rule_static_misses(rule: dict[str, Any]) -> list[tuple[str, str]]:
    """(symbol, origin) for each required symbol that no part of the rule reads."""
    origin = rule_requires(rule)
    reads = rule_reads(rule)
    return [(sym, origin[sym]) for sym in sorted(set(origin) - reads)]


def index_content(content: Path = CONTENT) -> dict[tuple[str, str], tuple[str, dict[str, Any]]]:
    index: dict[tuple[str, str], tuple[str, dict[str, Any]]] = {}
    for path in sorted(glob.glob(str(content / "**" / "*.json"), recursive=True)):
        try:
            with open(path, encoding="utf-8") as fh:
                doc = json.load(fh)
        except (OSError, ValueError):
            continue
        if isinstance(doc, dict) and isinstance(doc.get("id"), str) and "version" in doc:
            index.setdefault((doc["id"], str(doc["version"])), (path, doc))
    return index


def latest_core_package(content: Path = CONTENT) -> tuple[str, dict[str, Any]]:
    best: tuple[int, str, dict[str, Any]] | None = None
    for path in glob.glob(str(content / "**" / "package.core-calculations.v*.json"), recursive=True):
        with open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
        number = int(str(doc["version"]).lstrip("v"))
        if best is None or number > best[0]:
            best = (number, path, doc)
    if best is None:
        raise RuntimeError("no core-calculations package found under " + str(content))
    return best[1], best[2]


def package_static_misses(
    package: dict[str, Any], index: dict[tuple[str, str], tuple[str, dict[str, Any]]]
) -> tuple[list[dict[str, Any]], list[str]]:
    """Static misses for every computation member; also the members that did not resolve."""
    misses: list[dict[str, Any]] = []
    unresolved: list[str] = []
    for member in package.get("members", []):
        if member.get("role") != "computation":
            continue
        key = (member["id"], str(member["version"]))
        if key not in index:
            unresolved.append(f"{key[0]}@{key[1]}")
            continue
        rule_path, rule = index[key]
        if "requires" not in rule:
            continue
        for sym, origin in rule_static_misses(rule):
            misses.append({
                "rule_id": rule["id"],
                "rule_version": str(rule["version"]),
                "symbol": sym,
                "origin": origin,
                "rule_file": os.path.relpath(rule_path, REPO_ROOT),
            })
    return misses, unresolved


def load_allowlist(path: Path = ALLOWLIST) -> dict[tuple[str, str, str], str]:
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    allowed: dict[tuple[str, str, str], str] = {}
    for entry in doc.get("entries", []):
        for field in ("rule_id", "version", "symbol", "reason"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                raise ValueError(f"allowlist entry lacks a non-empty {field}: {entry}")
        key = (entry["rule_id"], entry["version"], entry["symbol"])
        if key in allowed:
            raise ValueError(f"duplicate allowlist entry: {key}")
        allowed[key] = entry["reason"]
    return allowed


def static_check(content: Path = CONTENT, allowlist: Path = ALLOWLIST) -> dict[str, Any]:
    package_path, package = latest_core_package(content)
    misses, unresolved = package_static_misses(package, index_content(content))
    allowed = load_allowlist(allowlist)
    missed_keys = {(m["rule_id"], m["rule_version"], m["symbol"]) for m in misses}
    return {
        "package": f"{package['id']}@{package['version']}",
        "package_file": os.path.relpath(package_path, REPO_ROOT),
        "misses": misses,
        "allowlisted": [m for m in misses if (m["rule_id"], m["rule_version"], m["symbol"]) in allowed],
        "unallowed": [m for m in misses if (m["rule_id"], m["rule_version"], m["symbol"]) not in allowed],
        "stale_allowlist": sorted(k for k in allowed if k not in missed_keys),
        "unresolved": unresolved,
    }


def _print_static(result: dict[str, Any]) -> None:
    print(f"STATIC CHECK: {result['package']} ({result['package_file']})")
    print(f"required symbols with no reading part of the rule: {len(result['misses'])}")
    for m in result["misses"]:
        status = "allowlisted" if m in result["allowlisted"] else "UNALLOWED"
        print(f"  {status}: {m['rule_id']}@{m['rule_version']} | requires {m['symbol']} | origin {m['origin']}")
    print(f"unresolved computation members: {len(result['unresolved'])}")
    for line in result["unresolved"]:
        print("  " + line)
    print(f"stale allowlist entries: {len(result['stale_allowlist'])}")
    for key in result["stale_allowlist"]:
        print(f"  {key}")


def run_path_probe(modules: list[str], dump_dir: Path) -> int:
    env = dict(os.environ)
    env["RVR_PROBE_OUT"] = str(dump_dir)
    env["PYTHONPATH"] = os.pathsep.join(filter(None, [str(REPO_ROOT), env.get("PYTHONPATH")]))
    command = [
        sys.executable, "-m", "pytest", "-p", "tools.required_versus_read_probe",
        "-p", "no:cacheprovider", "-q", *modules,
    ]
    completed = subprocess.run(command, cwd=REPO_ROOT, env=env, check=False)
    return completed.returncode


def read_dumps(dump_dir: Path) -> dict[tuple[str, str], dict[str, Any]]:
    records: dict[tuple[str, str], dict[str, Any]] = {}
    for path in sorted(glob.glob(str(dump_dir / "probe-*.jsonl"))):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                row = json.loads(line)
                records.setdefault((row["test"], row["finding_id"]), row)
    return records


def path_summary(
    records: dict[tuple[str, str], dict[str, Any]], index: dict[tuple[str, str], tuple[str, dict[str, Any]]]
) -> tuple[collections.Counter[str], dict[str, dict[str, Any]]]:
    """Classify each published finding; return (stats, every rule version the run published)."""
    stats: collections.Counter[str] = collections.Counter()
    rules: dict[str, dict[str, Any]] = {}
    for (test, _fid), row in sorted(records.items()):
        stats["published findings"] += 1
        if not row["rule_pins"]:
            stats["published without a rule pin (input or default finding)"] += 1
            continue
        if not row["matched"]:
            stats["published with a rule pin but no matching pins_for record (not covered)"] += 1
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
            "file": os.path.relpath(rule_path, REPO_ROOT), "findings": 0, "tests": set(),
            "absent_count": collections.Counter(), "status": collections.defaultdict(collections.Counter),
            "findings_with_absent": 0,
        })
        entry["findings"] += 1
        entry["tests"].add(test)
        absent_here = False
        for sym, state in (row["statuses"] or {}).items():
            entry["status"][sym][state["status"]] += 1
            if state["status"] in ABSENT_STATUSES:
                entry["absent_count"][sym] += 1
                absent_here = True
        if absent_here:
            entry["findings_with_absent"] += 1
    return stats, rules


def path_report(
    stats: collections.Counter[str], rules: dict[str, dict[str, Any]], dump_label: str,
    latest_members: set[str],
) -> None:
    print("PATH-DEPENDENT SCAN: declared required inputs not read on a published finding's path")
    print(f"dump: {dump_label}")
    for name in sorted(stats):
        print(f"{name}: {stats[name]}")
    print()
    print("Rule versions with at least one absent required input. 'never read' = absent on every"
          " published finding of that rule in the run; 'path-dependent' = absent on some findings only.")
    print("rule version | in latest core package | published findings | tests | findings with an absent input"
          " | never read (symbol: findings) | path-dependent (symbol: absent/findings)")
    never_total = 0
    partial_total = 0
    flagged = {k: v for k, v in rules.items() if v["absent_count"]}
    for key in sorted(flagged):
        entry = flagged[key]
        never, partial = [], []
        for sym in sorted(entry["absent_count"]):
            absent = entry["absent_count"][sym]
            if absent == entry["findings"]:
                never.append(f"{sym}: {absent}")
                never_total += 1
            else:
                partial.append(f"{sym}: {absent}/{entry['findings']}")
                partial_total += 1
        print(f"{key} | {'yes' if key in latest_members else 'no'} | {entry['findings']} | "
              f"{len(entry['tests'])} | {entry['findings_with_absent']} | "
              f"{'; '.join(never) or '-'} | {'; '.join(partial) or '-'}")
    print()
    print(f"rule versions published in the run: {len(rules)}")
    print(f"rule versions with an absent required input on at least one published finding: {len(flagged)}")
    print(f"rule-symbol pairs absent on every published finding of their rule: {never_total}")
    print(f"rule-symbol pairs absent on some but not all published findings: {partial_total}")
    print()
    print("NOT COVERED: findings whose pins match no recorded pins_for call are not measured by the probe"
          " (the count above); their rules publish without going through pins_for.")


def path_check(modules: list[str]) -> int:
    dump_dir = Path(tempfile.mkdtemp(prefix="rvr-probe-"))
    try:
        returncode = run_path_probe(modules, dump_dir)
        _package_path, latest = latest_core_package()
        latest_members = {
            f"{m['id']}@{m['version']}" for m in latest.get("members", []) if m.get("role") == "computation"
        }
        stats, rules = path_summary(read_dumps(dump_dir), index_content())
        path_report(stats, rules, "run of " + " ".join(modules), latest_members)
    finally:
        shutil.rmtree(dump_dir, ignore_errors=True)
    if returncode != 0:
        print(f"pytest exited with status {returncode}; the scan above covers the findings published before that.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("static", help="check the latest core package for required symbols nothing reads")
    path = sub.add_parser("path", help="run test modules and report required inputs absent from published pins")
    path.add_argument("modules", nargs="+")
    args = parser.parse_args(argv)
    if args.command == "static":
        result = static_check()
        _print_static(result)
        return 1 if result["unallowed"] or result["unresolved"] else 0
    return path_check(args.modules)


if __name__ == "__main__":
    sys.exit(main())
