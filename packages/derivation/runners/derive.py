"""Run a synthetic derivation scenario and explain its outputs.

Reads a self-contained scenario (rules, parameters, findings, sources, closure
assertions, and run identity) from a JSON file, runs the saturation runner over
the published schemas and operation-semantics canon, and prints the derived
findings, the blocked surface, and an explanation tree per output. Read-only
and deterministic: the same scenario always prints the same report, which is
what the goldens pin.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

from packages.derivation.explanation import explain, index_derived
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.runner import InputFinding, RunContext, SourceFact, run


def _context(scenario: dict[str, Any]) -> RunContext:
    return RunContext(
        run_id=scenario["run_id"],
        rules=scenario["rules"],
        parameters={p["id"]: p for p in scenario["parameters"]},
        canon=load_canon(DerivationSchemas()),
        inputs=[InputFinding(**i) for i in scenario["inputs"]],
        sources=[SourceFact(**s) for s in scenario["sources"]],
        closed_sets=frozenset(scenario.get("closed_sets", [])),
        adoption_pin=scenario["adoption_pin"],
        governance_pins=scenario["governance_pins"],
    )


def build_report(scenario: dict[str, Any]) -> dict[str, Any]:
    schemas = DerivationSchemas()
    ctx = _context(scenario)
    result = run(ctx, schemas)

    derived = index_derived([pub.finding for pub in result.publications])
    input_index: dict[str, Any] = {i["finding_id"]: i for i in scenario["inputs"]}
    # Source facts are leaf findings too; index them so collected inputs render
    # their value and name rather than a bare id.
    for source in scenario["sources"]:
        input_index[source["finding_id"]] = {
            "symbol": source["name"], "value": source["value"], "role": "input",
        }
    published = sorted(
        ({"symbol": pub.finding["symbol"], "value": pub.finding["value"], "finding_id": pub.finding["id"]}
         for pub in result.publications),
        key=lambda entry: entry["symbol"],
    )
    explanations = {
        entry["symbol"]: explain(entry["finding_id"], role="output", derived=derived, inputs=input_index).to_dict()
        for entry in published
    }
    return {
        "run_id": result.run_id,
        "stop_reason": result.stop_reason,
        "published": published,
        "blocked": sorted(result.blocked, key=lambda b: b["artifact_id"]),
        "explanations": explanations,
    }


def _human(report: dict[str, Any]) -> str:
    from packages.derivation.explanation import ExplanationNode, render_text

    lines = [f"Run: {report['run_id']} ({report['stop_reason']})", "Published:"]
    for entry in report["published"]:
        lines.append(f"  - {entry['symbol']} = {entry['value']}  [{entry['finding_id']}]")
    if not report["published"]:
        lines.append("  - none")
    lines.append("Blocked:")
    for entry in report["blocked"]:
        lines.append(f"  - {entry['artifact_id']}: {entry['code']} (missing {', '.join(entry['missing']) or 'none'})")
    if not report["blocked"]:
        lines.append("  - none")
    lines.append("Explanations:")

    def _node(d: dict[str, Any]) -> ExplanationNode:
        return ExplanationNode(
            finding_id=d["finding_id"], role=d["role"], kind=d["kind"], symbol=d["symbol"],
            value=d["value"], version=d["version"], produced_by=d["produced_by"],
            children=tuple(_node(c) for c in d["children"]),
        )

    for symbol in sorted(report["explanations"]):
        lines.append(render_text(_node(report["explanations"][symbol]), indent=1))
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", required=True, type=Path, help="Path to a scenario JSON file")
    parser.add_argument("--json", action="store_true", help="Print the JSON report instead of the human summary")
    args = parser.parse_args(argv)

    scenario = json.loads(args.scenario.read_text("utf-8"))
    report = build_report(scenario)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(_human(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
