"""P0 static scan: required symbols that no part of a shipped rule reads.

Run from the repository root:  python3 <this file> [--list-all]
Reads package members (not file names) of every package under
packages/content/tax, resolves each member to its rule file by id and version,
and compares the rule's declared `requires` (plus selection path and default
requires) with the symbols its expressions read.
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *([".."] * 5)))
CONTENT = os.path.join(ROOT, "packages", "content", "tax")

# Operations whose `name` (or listed name keys) reads a symbol from the
# environment. Source: packages/derivation/evaluator.py _evaluate.
READ_NAME_OPS = {"ref", "collect", "count", "bound_sources", "collect_categorical_all_equal"}
# Operations that read named keyed sources (links/reductions) or a fact type.
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


def walk_reads(node, reads: set[str]) -> None:
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


def rule_requires(rule: dict) -> tuple[set[str], dict[str, str]]:
    """Return (required symbols, origin of each: top|selection-path|selection-default)."""
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
    return set(origin), origin


def rule_reads(rule: dict) -> set[str]:
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


def index_content() -> dict[tuple[str, str], tuple[str, dict]]:
    index: dict[tuple[str, str], tuple[str, dict]] = {}
    for path in sorted(glob.glob(os.path.join(CONTENT, "**", "*.json"), recursive=True)):
        try:
            with open(path, encoding="utf-8") as fh:
                doc = json.load(fh)
        except (OSError, ValueError):
            continue
        if isinstance(doc, dict) and isinstance(doc.get("id"), str) and "version" in doc:
            index.setdefault((doc["id"], str(doc["version"])), (path, doc))
    return index


def family_of(package_id: str) -> str:
    # tax.us.2025.package.core-calculations -> core-calculations
    return package_id.split(".package.", 1)[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-all", action="store_true",
                        help="also list every hit in every package, not only the latest")
    args = parser.parse_args()

    index = index_content()
    packages = []
    for path in sorted(glob.glob(os.path.join(CONTENT, "**", "package.*.json"), recursive=True)):
        with open(path, encoding="utf-8") as fh:
            packages.append((path, json.load(fh)))

    rel = lambda p: os.path.relpath(p, ROOT)  # noqa: E731
    per_family_packages: collections.Counter = collections.Counter()
    per_family_members: collections.Counter = collections.Counter()
    per_family_hit_pairs: collections.Counter = collections.Counter()
    per_family_hit_rules: dict[str, set[str]] = collections.defaultdict(set)
    per_family_scanned_rules: dict[str, set[str]] = collections.defaultdict(set)
    non_computation: collections.Counter = collections.Counter()
    unresolved: list[str] = []
    rule_hits_all: dict[str, dict] = {}
    latest: dict[str, tuple[int, str]] = {}

    for path, pkg in packages:
        family = family_of(pkg["id"])
        version_number = int(re.sub(r"\D", "", str(pkg["version"])) or 0)
        if family not in latest or version_number > latest[family][0]:
            latest[family] = (version_number, path)
    latest_path = {fam: p for fam, (_n, p) in latest.items()}

    hits_by_package: dict[str, list[dict]] = {}
    for path, pkg in packages:
        family = family_of(pkg["id"])
        per_family_packages[family] += 1
        hits: list[dict] = []
        for member in pkg.get("members", []):
            per_family_members[family] += 1
            if member.get("role") != "computation":
                non_computation[(member.get("role"), member.get("schema"))] += 1
                continue
            key = (member["id"], str(member["version"]))
            if key not in index:
                unresolved.append(f"{rel(path)}: {key}")
                continue
            rule_path, rule = index[key]
            if "requires" not in rule:
                non_computation[("no-requires", rule.get("schema"))] += 1
                continue
            per_family_scanned_rules[family].add(rule["id"] + "@" + rule["version"])
            required, origin = rule_requires(rule)
            reads = rule_reads(rule)
            for sym in sorted(required - reads):
                hit = {
                    "package": pkg["id"] + "@" + str(pkg["version"]),
                    "rule_id": rule["id"],
                    "rule_version": rule["version"],
                    "rule_file": rel(rule_path),
                    "symbol": sym,
                    "origin": origin.get(sym, "top"),
                    "publishes": rule.get("publishes"),
                    "role_of_rule": rule.get("role"),
                }
                hits.append(hit)
                per_family_hit_pairs[family] += 1
                per_family_hit_rules[family].add(rule["id"] + "@" + rule["version"])
                rule_hits_all.setdefault(rule["id"] + "@" + rule["version"], hit)
        hits_by_package[path] = hits

    print("STATIC SCAN: required symbols with no reading part of the rule")
    print("scope: packages/content/tax/**/package.*.json; members with role=computation")
    print("resolved by member id+version; rules without `requires` are counted separately")
    print()
    print("family | package files | member rows | scanned rule versions | rule versions with hits | (package, rule) hit pairs")
    for family in sorted(per_family_packages):
        print(f"{family} | {per_family_packages[family]} | {per_family_members[family]} | "
              f"{len(per_family_scanned_rules[family])} | {len(per_family_hit_rules[family])} | "
              f"{per_family_hit_pairs[family]}")
    print()
    print("non-scanned member rows (role, schema): count")
    for key, count in sorted(non_computation.items(), key=lambda kv: str(kv[0])):
        print(f"  {key}: {count}")
    print(f"unresolved computation members: {len(unresolved)}")
    for line in unresolved:
        print("  " + line)
    print()
    for family in sorted(latest):
        latest_pkg = latest_path[family]
        hits = hits_by_package[latest_pkg]
        with open(latest_pkg, encoding="utf-8") as fh:
            name = json.load(fh)
        print(f"LATEST PACKAGE {name['id']}@{name['version']}: {len(hits)} hits, "
              f"{len({h['rule_id'] for h in hits})} distinct rule ids")
        for hit in hits:
            print(f"  {hit['rule_id']}@{hit['rule_version']} | requires {hit['symbol']} | "
                  f"origin {hit['origin']} | publishes {hit['publishes']} | {hit['rule_file']}")
        print()
    # Distinct (rule version, symbol) hits across every core package member
    # list, with the package versions that carry each one.
    carriers: dict[tuple[str, str, str], list[str]] = collections.defaultdict(list)
    for path, _pkg in packages:
        for hit in hits_by_package[path]:
            key = (hit["rule_id"] + "@" + hit["rule_version"], hit["symbol"], hit["origin"])
            carriers[key].append(hit["package"].split("@")[1])
    print("DISTINCT HITS ACROSS ALL PACKAGE FILES (rule version, required symbol, origin): carried by package versions")
    for (rule_key, symbol, origin), versions in sorted(carriers.items()):
        print(f"  {rule_key} | requires {symbol} | origin {origin} | "
              f"{len(versions)} package rows: {', '.join(sorted(set(versions), key=lambda v: int(v.lstrip('v') or 0)))}")
    print()
    if args.list_all:
        print("ALL PACKAGES: hit count per package file")
        for path, _pkg in packages:
            print(f"  {rel(path)}: {len(hits_by_package[path])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
