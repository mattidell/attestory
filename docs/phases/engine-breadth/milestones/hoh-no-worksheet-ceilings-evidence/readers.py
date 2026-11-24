"""Who reads the status-test answers, and who reads worksheet lines 6 and 13.

Run: python3 readers.py --out readers.json

Scans the published 2025 content directory. Does not run the engine and does
not edit packages/ or tests/.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
CONTENT = REPO / "packages/content/tax/2025"
P = "tax.us.2025."
LINE6 = P + "qdcg-worksheet.line-6"
LINE13 = P + "qdcg-worksheet.line-13"
HOH = P + "hoh.tests-met"
QSS = P + "qss.tests-met"


def _refs(node: Any, found: set[str]) -> None:
    if isinstance(node, dict):
        if node.get("op") == "ref" and isinstance(node.get("name"), str):
            found.add(node["name"])
        for value in node.values():
            _refs(value, found)
    elif isinstance(node, list):
        for value in node:
            _refs(value, found)


def _load(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def scan() -> dict[str, Any]:
    rules: dict[str, dict[str, Any]] = {}
    mentions: dict[str, list[str]] = {HOH: [], QSS: []}
    publishes: dict[str, str] = {}
    zero: list[str] = []
    fifteen: list[str] = []
    for path in sorted(CONTENT.glob("*.json")):
        text = path.read_text(encoding="utf-8")
        body = _load(path)
        for symbol, bucket in mentions.items():
            if symbol in text:
                bucket.append(path.name)
        if not isinstance(body, dict):
            continue
        if "parameter.preferential-zero-ceiling" in text and path.name.startswith("rule."):
            zero.append(path.name)
        if "parameter.preferential-fifteen-ceiling" in text and path.name.startswith("rule."):
            fifteen.append(path.name)
        rule_id = body.get("id")
        if not isinstance(rule_id, str) or not rule_id.startswith(P + "rule."):
            continue
        requires = [item for item in body.get("requires") or [] if isinstance(item, str)]
        refs: set[str] = set()
        _refs(body.get("value"), refs)
        rules[rule_id] = {"file": path.name, "version": body.get("version"), "requires": requires, "refs": refs}
        if isinstance(body.get("publishes"), str) and "qdcg-worksheet" in rule_id:
            publishes[rule_id] = body["publishes"]

    def readers_of(symbol: str) -> list[dict[str, Any]]:
        found = []
        for rule_id, row in sorted(rules.items()):
            how = []
            if symbol in row["requires"]:
                how.append("requires")
            if symbol in row["refs"]:
                how.append("ref")
            if how:
                found.append({"id": rule_id, "version": row["version"], "file": row["file"], "how": how})
        return found

    def downstream(starts: list[str]) -> list[str]:
        seen = set(starts)
        wave = list(starts)
        order: list[str] = []
        while wave:
            symbol = wave.pop(0)
            for rule_id, published in sorted(publishes.items()):
                row = rules[rule_id]
                if symbol in row["requires"] or symbol in row["refs"]:
                    if published not in seen:
                        seen.add(published)
                        wave.append(published)
                        order.append(published)
        return order

    watched = {HOH, QSS, "filing_status", LINE6, LINE13}
    return {
        "tests_met_files": mentions,
        "tests_met_rule_readers": {HOH: readers_of(HOH), QSS: readers_of(QSS)},
        "ceiling_parameter_readers": {
            P + "parameter.preferential-zero-ceiling": zero,
            P + "parameter.preferential-fifteen-ceiling": fifteen,
        },
        "line6_direct": readers_of(LINE6),
        "line13_direct": readers_of(LINE13),
        "line6_downstream_published": downstream([LINE6]),
        "line13_downstream_published": downstream([LINE13]),
        "worksheet_rules": {
            rule_id: {
                "version": rules[rule_id]["version"],
                "file": rules[rule_id]["file"],
                "requires": rules[rule_id]["requires"],
                "refs": sorted(name for name in rules[rule_id]["refs"] if name in watched or "qdcg-worksheet" in name),
            }
            for rule_id in sorted(publishes)
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    body = scan()
    text = json.dumps(body, indent=1) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"readers output contains {needle}")
    args.out.write_text(text, encoding="utf-8")
    print(json.dumps({
        "tests_met_rule_readers": body["tests_met_rule_readers"],
        "tests_met_files": body["tests_met_files"],
        "line6_direct": body["line6_direct"],
        "line13_direct": body["line13_direct"],
        "line6_downstream": body["line6_downstream_published"],
        "line13_downstream": body["line13_downstream_published"],
        "zero_files": body["ceiling_parameter_readers"][P + "parameter.preferential-zero-ceiling"],
        "fifteen_files": body["ceiling_parameter_readers"][P + "parameter.preferential-fifteen-ceiling"],
    }, indent=1))


if __name__ == "__main__":
    main()
