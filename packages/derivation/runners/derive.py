"""Run a synthetic derivation scenario and explain its outputs.

Reads a synthetic scenario from a JSON file, runs the saturation runner over
the published schemas and operation-semantics canon, and prints the derived
findings, the blocked surface, and an explanation tree per output. A scenario
may name a shared content fixture containing declared rule/package paths; this
keeps several lifecycle workspaces on the same versioned content rather than
copying tax meaning into each workspace. Read-only and deterministic: the same
scenario always prints the same report, which is what the goldens pin.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence, cast

from packages.derivation.explanation import explain, index_derived
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.runner import InputFinding, RunContext, SourceFact, run
from packages.derivation.source_authority import ClosureFindingRecord


def _load_json(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text("utf-8")))


def _load_content_fixture(scenario_path: Path, fixture_ref: str) -> dict[str, Any]:
    """Materialize declared content paths for a synthetic scenario.

    The fixture carries only relative paths to committed, versioned citizens.
    It is deliberately a runner-fixture convenience, not a package loader or
    an authority decision: the scenario still supplies the synthetic workspace
    inputs, sources, and closure record state it is exercising.
    """
    fixture_path = (scenario_path.parent / fixture_ref).resolve()
    fixture = _load_json(fixture_path)

    def citizens(key: str) -> list[dict[str, Any]]:
        return [_load_json((fixture_path.parent / ref).resolve()) for ref in fixture[key]]

    package = _load_json((fixture_path.parent / fixture["package"]).resolve())
    fact_types: list[dict[str, Any]] = []
    for bundle in citizens("fact_type_bundles"):
        fact_types.extend(bundle["fact_types"])
    return {
        "rules": citizens("rules"),
        "parameters": citizens("parameters"),
        "family_declarations": citizens("family_declarations"),
        "mappings": citizens("mappings"),
        "fact_types": fact_types,
        "input_bindings": package["input_bindings"],
        "adoption_pin": fixture["adoption_pin"],
        "governance_pins": fixture["governance_pins"],
    }


def load_scenario(path: Path) -> dict[str, Any]:
    """Load one scenario and, if named, its shared declared content fixture."""
    scenario = _load_json(path)
    fixture_ref = scenario.pop("content_fixture", None)
    if fixture_ref is None:
        return scenario
    if not isinstance(fixture_ref, str):
        raise ValueError("content_fixture must be a relative fixture path")
    content = _load_content_fixture(path, fixture_ref)
    overlap = set(scenario).intersection(content)
    if overlap:
        raise ValueError(f"scenario duplicates shared content keys: {sorted(overlap)}")
    return {**content, **scenario}


def _context(scenario: dict[str, Any]) -> RunContext:
    if "closed_sets" in scenario:
        raise ValueError(
            "scenario names caller-supplied closed_sets; that input was "
            "removed by ADR-0014 — closure enters only through the adopted "
            "mapping and record state in the scenario's closure section"
        )
    closure = scenario.get("closure", {})
    return RunContext(
        run_id=scenario["run_id"],
        rules=scenario["rules"],
        parameters={p["id"]: p for p in scenario["parameters"]},
        canon=load_canon(DerivationSchemas()),
        inputs=[InputFinding(**i) for i in scenario["inputs"]],
        sources=[SourceFact(**s) for s in scenario["sources"]],
        adoption_pin=scenario["adoption_pin"],
        governance_pins=scenario["governance_pins"],
        family_declarations=closure.get(
            "family_declarations", scenario.get("family_declarations", [])
        ),
        closure_mappings=closure.get("mappings", scenario.get("mappings", [])),
        closure_findings=[
            ClosureFindingRecord(**record) for record in closure.get("findings", [])
        ],
        current_horizons=closure.get("current_horizons", {}),
        fact_types=scenario.get("fact_types", []),
        input_bindings=scenario.get("input_bindings", []),
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
    # Closure findings are leaf findings a closure-backed zero pins; index
    # them so the explanation walk renders the authority, not a bare id.
    for record in scenario.get("closure", {}).get("findings", []):
        input_index[record["finding_id"]] = {
            "symbol": record["fact_type"], "value": record["value"], "role": "input",
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

    scenario = load_scenario(args.scenario)
    report = build_report(scenario)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(_human(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
