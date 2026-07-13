"""Shared test fixtures: a demo schema set and act builders.

The demo vocabulary is deliberately synthetic (milestone plan, ratified
decision 3): tests prove the machinery obeys the Constitution without
entangling tax content.
"""

import json
import shutil
from pathlib import Path
from typing import Any

from packages.kernel.schema_registry import (
    KERNEL_SCHEMA_DIR,
    SchemaRegistry,
    write_manifest,
)

DEMO_NOTE_PAYLOAD_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {"text": {"type": "string", "minLength": 1}},
    "required": ["text"],
    "additionalProperties": False,
}


def registry_with_demo_kinds(schema_dir: Path) -> SchemaRegistry:
    """A registry over the published kernel schemas plus a demo act kind.

    Kernel schema files are copied byte-for-byte so tests exercise the
    real published versions; the synthetic ``demo-note`` act kind exists
    only to give envelope-level tests a payload with no kernel meaning.
    """
    for path in sorted(KERNEL_SCHEMA_DIR.glob("*.schema.json")):
        shutil.copy(path, schema_dir / path.name)
    (schema_dir / "act-demo-note.v1.schema.json").write_text(
        json.dumps(DEMO_NOTE_PAYLOAD_SCHEMA, indent=2), "utf-8"
    )
    write_manifest(schema_dir)
    return SchemaRegistry(schema_dir)


def demo_note_act(index: int, text: str | None = None) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": f"demo-act-{index:03d}",
        "kind": "demo-note",
        "actor": "user",
        "at": f"2026-01-01T00:00:{index % 60:02d}Z",
        "committed_against": index,
        "payload": {"text": text if text is not None else f"note {index}"},
    }


def demo_fact_type_payment() -> dict[str, Any]:
    return {
        "schema": "fact-type.v1",
        "id": "demo.counterparty-payment",
        "title": "Payment received from a counterparty",
        "nature": "determinable",
        "identity_keys": [
            {"name": "counterparty", "kind": "entity", "entity_kind": "demo.counterparty"},
            {"name": "period", "kind": "literal", "values": ["2025"]},
        ],
        "value_schema": {"type": "number"},
        "supersession": {"policy": "free"},
    }


def demo_fact_type_rate_choice() -> dict[str, Any]:
    return {
        "schema": "fact-type.v1",
        "id": "demo.rate-choice",
        "title": "Rate treatment for the period",
        "nature": "elective",
        "identity_keys": [
            {"name": "period", "kind": "literal", "values": ["2025"]},
        ],
        "value_schema": {"enum": ["standard", "reduced"]},
        "supersession": {"policy": "free"},
    }


def demo_bundle() -> dict[str, Any]:
    return {
        "schema": "bundle.v1",
        "id": "demo.vocabulary",
        "label": "Demo vocabulary",
        "fact_types": [demo_fact_type_payment(), demo_fact_type_rate_choice()],
    }


def act(index: int, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": f"demo-act-{index:03d}",
        "kind": kind,
        "actor": "user",
        "at": f"2026-01-01T00:{index // 60:02d}:{index % 60:02d}Z",
        "committed_against": index,
        "payload": payload,
    }


def demo_entity(entity_id: str, label: str, kind: str = "demo.counterparty") -> dict[str, Any]:
    return {"schema": "entity.v1", "id": entity_id, "kind": kind, "label": label}


def demo_evidence(
    evidence_id: str = "demo-evidence-001",
    label: str = "Demo statement",
    content: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "schema": "evidence.v1",
        "id": evidence_id,
        "kind": "demo.statement",
        "label": label,
        "content": content if content is not None else {"amount": 1200},
    }


def demo_payment_fact_id(counterparty_id: str = "demo-corp-a") -> str:
    return f"demo.counterparty-payment|counterparty={counterparty_id},period=2025"


def demo_finding(
    finding_id: str = "demo-finding-001",
    fact_id: str | None = None,
    value: Any = 1200,
    evidence_ids: list[str] | None = None,
    basis: str = "documentary",
    captured: bool = False,
) -> dict[str, Any]:
    """A synthetic asserted finding.

    ``captured`` is opt-in: capture preserves a claim that was shown by a
    proposing process, and the demo scenarios model direct manual entry,
    where nothing was presented. Decorative capture would dilute the
    vocabulary (Ontology §3).
    """
    finding: dict[str, Any] = {
        "schema": "finding.v1",
        "id": finding_id,
        "fact_id": fact_id if fact_id is not None else demo_payment_fact_id(),
        "value": value,
        "basis": basis,
        "evidence_ids": evidence_ids if evidence_ids is not None else ["demo-evidence-001"],
    }
    if captured:
        finding["capture"] = {
            "presented": {"value": value, "basis": basis},
            "asserted": {"value": value, "basis": basis},
        }
    return finding


def demo_closure_authority(*, closed: bool = True) -> dict[str, Any]:
    """RunContext kwargs granting closure authority over the demo W-2 family.

    ADR-0014: there is no closed-set input. Tests that want the empty demo
    source set to publish zero must present the full authority chain — an
    adopted declaration and mapping, one current literal-true closure
    finding, and the current horizon — exactly as the persistence boundary
    marshals it from record state.
    """
    from packages.derivation.source_authority import ClosureFindingRecord

    declaration = {
        "schema": "source-family.v1",
        "id": "demo.w2",
        "version": "v1",
        "title": "Demo W-2 box 1 statements",
        "scope": {"tax_year": 2025, "jurisdiction": "us", "family": "tax"},
        "closure_claim": "Every demo W-2 box 1 statement is recorded.",
        "member_predicate": {"fact_type": "demo.w2.box1"},
        "authorizes_subtotal": "demo.form1040.line1a",
    }
    mapping = {
        "schema": "source-closure-mapping.v1",
        "id": "demo.mapping.w2",
        "version": "v1",
        "family": {"id": "demo.w2", "version": "v1"},
        "member_fact_type": "demo.w2.box1",
        "closure_fact_type": "demo.w2.closure",
        "closure_horizon_key": "family-horizon",
        "admits_symbol": "demo.form1040.line1a",
        "admission": {"condition": "current-literal-true"},
    }
    findings = (
        [ClosureFindingRecord("f.closure.demo", "demo.w2.closure", "demo.h0", True)]
        if closed
        else []
    )
    return {
        "family_declarations": [declaration],
        "closure_mappings": [mapping],
        "closure_findings": findings,
        "current_horizons": {"demo.w2": "demo.h0"},
    }
