"""Regenerate the production-shaped presentation golden (Presentation L2
Integration Grounding, Track 1).

Runs one canonical, obviously synthetic authoritative act log through
``live_coordinate_run`` against the real ``tax.us.2025.package.core-calculations``
v6 content (the same package ``tests/test_dsbs_t4_dividend_live_integration.py``
exercises), and copies the coordinator's own confined presentation-model.v1
artifact — never a hand-authored or caller-shaped payload — to the committed
fixture path the ``citation-walk-production-shaped.v1.json`` manifest reads.

Determinism: the run's authoritative acts, run id, and scope are fixed
constants below, so re-running this script reproduces the identical
byte-for-byte golden. It never reads a workspace or any user data; every fact,
entity, and evidence label here is a reserved ``demo.*`` synthetic value.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402
from packages.derivation.production_resolver import PublicationSurface  # noqa: E402

CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
T3 = ROOT / "packages" / "sample_data" / "frrs_t3"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2055"}
RUN_ID = "demo.presentation-l2.production-shaped"
GOLDEN_PATH = (
    ROOT / "tools" / "presentation_harness" / "examples" / "pages"
    / "citation-walk-fixtures" / "production-shaped.v1.json"
)


def _surface() -> PublicationSurface:
    return PublicationSurface(T3 / "publication_surface" / "releases", CONTENT / "published-packages.json", CONTENT)


def _act(name: str) -> dict[str, object]:
    return json.loads((T3 / "adoptions" / name).read_text("utf-8"))


def _live_act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.presentation-l2.act.{index:03d}",
        "kind": kind,
        "actor": USER,
        "at": f"2026-07-26T00:00:{index:02d}Z",
        "committed_against": index,
        "payload": payload,
    }


def _attested_finding(finding_id: str, fact_id: str, value: object) -> dict[str, object]:
    return {"schema": "finding.v1", "id": finding_id, "fact_id": fact_id, "value": value, "basis": "attested", "evidence_ids": []}


def canonical_acts() -> list[dict[str, object]]:
    """One complete, production-shaped synthetic v6 authoritative act log.

    Wages, two 1099-INT box-1 facts, and a 1099-DIV statement (ordinary and
    qualified boxes) over the Schedule B threshold, each backed by its own
    declared evidence label (forwarded verbatim by the projector, never
    invented) — plus every Part III / QDCG declared-absence declaration the
    v6 package's optional-default bindings do not already cover.
    """
    acts: list[dict[str, object]] = []

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_live_act(len(acts), kind, payload))

    for name in (
        "w2.bundle.v3.json",
        "f1099int.bundle.json",
        "interest_composition.bundle.json",
        "core_calculations.bundle.v2.json",
        "f1099div.bundle.json",
        "scheduleb.bundle.json",
        "qdcg.bundle.json",
    ):
        add("bundle-adoption", {"bundle": json.loads((CONTENT / name).read_text())})

    def entity(entity_id: str, kind: str, label: str) -> None:
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": entity_id, "kind": kind, "label": label}})

    entity("demo.presentation-l2.employer", "tax.us.employer", "Synthetic employer")
    entity("demo.presentation-l2.w2", "tax.us.w2-slip", "Synthetic W-2 slip")
    entity("demo.presentation-l2.bank1", "tax.us.interest-payer", "Synthetic First Bank")
    entity("demo.presentation-l2.bank2", "tax.us.interest-payer", "Synthetic Second Credit Union")
    entity("demo.presentation-l2.stmt1", "tax.us.1099int-statement", "Synthetic 1099-INT statement 1")
    entity("demo.presentation-l2.stmt2", "tax.us.1099int-statement", "Synthetic 1099-INT statement 2")
    entity("demo.presentation-l2.payer", "tax.us.dividend-payer", "Synthetic dividend payer")
    entity("demo.presentation-l2.divstmt", "tax.us.1099div-statement", "Synthetic 1099-DIV statement")

    scope = {"tax-year": "2025", "subject": "demo.primary"}
    families = (
        ("tax.us.2025.w2", "v2", "demo.presentation-l2.w2.h0"),
        ("tax.us.2025.f1099int.b1", "v1", "demo.presentation-l2.int-b1.h0"),
        ("tax.us.2025.f1099int.b3", "v1", "demo.presentation-l2.int-b3.h0"),
        ("tax.us.2025.f1099oid.b1", "v1", "demo.presentation-l2.oid-b1.h0"),
        ("tax.us.2025.non-form-interest", "v1", "demo.presentation-l2.nonform.h0"),
        ("tax.us.2025.f1099div.1a", "v1", "demo.presentation-l2.div1a.h0"),
        ("tax.us.2025.f1099div.1b", "v1", "demo.presentation-l2.div1b.h0"),
    )
    for family_id, version, horizon_id in families:
        add("horizon-genesis", {"family": {"id": family_id, "version": version}, "scope": scope, "horizon_id": horizon_id})

    submitted_evidence: set[str] = set()

    def submit_and_assert(
        *, evidence_id: str, evidence_kind: str, evidence_label: str, contribution_id: str,
        family_id: str, family_version: str, predecessor: str, successor: str,
        finding_id: str, fact_id: str, value: object,
    ) -> None:
        if evidence_id not in submitted_evidence:
            add("evidence-submitted", {"evidence": {
                "schema": "evidence.v1", "id": evidence_id, "kind": evidence_kind,
                "label": evidence_label, "content": {"value": value},
            }})
            submitted_evidence.add(evidence_id)
        add("contribution", {"contribution": {
            "schema": "contribution.v1", "id": contribution_id, "evidence_id": evidence_id,
            "content": {"mode": "manual-entry", "synthetic": True},
        }})
        add("member-transition", {
            "family": {"id": family_id, "version": family_version},
            "scope": scope,
            "member": {"action": "assert", "finding": {
                "schema": "finding.v2", "id": finding_id, "fact_id": fact_id,
                "value": value, "basis": "documentary", "evidence_ids": [evidence_id],
                "contribution_id": contribution_id,
            }},
            "successor": {"id": successor, "predecessor": predecessor},
        })

    submit_and_assert(
        evidence_id="demo.presentation-l2.evidence.w2", evidence_kind="demo.statement.w2",
        evidence_label="W-2 — Synthetic employer, box 1", contribution_id="demo.presentation-l2.contribution.w2",
        family_id="tax.us.2025.w2", family_version="v2",
        predecessor="demo.presentation-l2.w2.h0", successor="demo.presentation-l2.w2.h1",
        finding_id="demo.presentation-l2.finding.wages",
        fact_id="tax.us.2025.w2.box1-wages|employer=demo.presentation-l2.employer,w2-slip=demo.presentation-l2.w2,tax-year=2025",
        value=90000,
    )
    submit_and_assert(
        evidence_id="demo.presentation-l2.evidence.int1", evidence_kind="demo.statement.f1099int",
        evidence_label="1099-INT box 1 — Synthetic First Bank", contribution_id="demo.presentation-l2.contribution.int1",
        family_id="tax.us.2025.f1099int.b1", family_version="v1",
        predecessor="demo.presentation-l2.int-b1.h0", successor="demo.presentation-l2.int-b1.h1",
        finding_id="demo.presentation-l2.finding.int1",
        fact_id="tax.us.2025.f1099int.box1-interest|payer=demo.presentation-l2.bank1,statement=demo.presentation-l2.stmt1,tax-year=2025",
        value=1000,
    )
    submit_and_assert(
        evidence_id="demo.presentation-l2.evidence.int2", evidence_kind="demo.statement.f1099int",
        evidence_label="1099-INT box 1 — Synthetic Second Credit Union", contribution_id="demo.presentation-l2.contribution.int2",
        family_id="tax.us.2025.f1099int.b1", family_version="v1",
        predecessor="demo.presentation-l2.int-b1.h1", successor="demo.presentation-l2.int-b1.h2",
        finding_id="demo.presentation-l2.finding.int2",
        fact_id="tax.us.2025.f1099int.box1-interest|payer=demo.presentation-l2.bank2,statement=demo.presentation-l2.stmt2,tax-year=2025",
        value=234,
    )
    submit_and_assert(
        evidence_id="demo.presentation-l2.evidence.div", evidence_kind="demo.statement.f1099div",
        evidence_label="1099-DIV — Synthetic dividend payer", contribution_id="demo.presentation-l2.contribution.div1a",
        family_id="tax.us.2025.f1099div.1a", family_version="v1",
        predecessor="demo.presentation-l2.div1a.h0", successor="demo.presentation-l2.div1a.h1",
        finding_id="demo.presentation-l2.finding.box1a",
        fact_id="tax.us.2025.f1099div.box1a-ordinary|payer=demo.presentation-l2.payer,statement=demo.presentation-l2.divstmt,tax-year=2025",
        value=2000,
    )
    submit_and_assert(
        evidence_id="demo.presentation-l2.evidence.div", evidence_kind="demo.statement.f1099div",
        evidence_label="1099-DIV — Synthetic dividend payer", contribution_id="demo.presentation-l2.contribution.div1b",
        family_id="tax.us.2025.f1099div.1b", family_version="v1",
        predecessor="demo.presentation-l2.div1b.h0", successor="demo.presentation-l2.div1b.h1",
        finding_id="demo.presentation-l2.finding.box1b",
        fact_id="tax.us.2025.f1099div.box1b-qualified|payer=demo.presentation-l2.payer,statement=demo.presentation-l2.divstmt,tax-year=2025",
        value=600,
    )

    add("assertion", {"finding": _attested_finding("demo.presentation-l2.finding.rounding", "rounding.convention|tax-year=2025", "half_up")})
    add("assertion", {"finding": _attested_finding("demo.presentation-l2.finding.status", "tax.us.2025.filing-status|tax-year=2025", "single")})
    add("assertion", {"finding": _attested_finding("demo.presentation-l2.finding.foreign-account", "tax.us.2025.scheduleb.foreign-account|tax-year=2025", "no")})
    add("assertion", {"finding": _attested_finding("demo.presentation-l2.finding.foreign-trust", "tax.us.2025.scheduleb.foreign-trust|tax-year=2025", "no")})
    add("assertion", {"finding": _attested_finding("demo.presentation-l2.finding.cg-dist", "tax.us.2025.capital-gain-distributions|tax-year=2025", "no")})
    add("assertion", {"finding": _attested_finding("demo.presentation-l2.finding.sched-d", "tax.us.2025.schedule-d-required|tax-year=2025", "no")})

    closures = (
        ("demo.presentation-l2.closure.w2", "tax.us.2025.w2.source-closure", "demo.presentation-l2.w2.h1"),
        ("demo.presentation-l2.closure.int-b1", "tax.us.2025.f1099int.b1.source-closure", "demo.presentation-l2.int-b1.h2"),
        ("demo.presentation-l2.closure.int-b3", "tax.us.2025.f1099int.b3.source-closure", "demo.presentation-l2.int-b3.h0"),
        ("demo.presentation-l2.closure.oid-b1", "tax.us.2025.f1099oid.b1.source-closure", "demo.presentation-l2.oid-b1.h0"),
        ("demo.presentation-l2.closure.nonform", "tax.us.2025.non-form-interest.source-closure", "demo.presentation-l2.nonform.h0"),
        ("demo.presentation-l2.closure.div1a", "tax.us.2025.f1099div.1a.source-closure", "demo.presentation-l2.div1a.h1"),
        ("demo.presentation-l2.closure.div1b", "tax.us.2025.f1099div.1b.source-closure", "demo.presentation-l2.div1b.h1"),
    )
    for finding_id, fact_type, horizon_id in closures:
        add("assertion", {"finding": _attested_finding(finding_id, f"{fact_type}|family-horizon={horizon_id},tax-year=2025", True)})

    adoption = _act("adopt-core-v6-current.json")
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts


def regenerate() -> dict[str, Any]:
    acts = canonical_acts()
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        result = live_coordinate_run(
            WorkspaceCapability(root / "L"), repo_root=ROOT, authoritative_acts=acts,
            workspace_revision=len(acts), run_scope=SCOPE, scope_user=USER,
            request={"schema": "run-request.v1"}, run_id=RUN_ID, governance_pins=[],
            surface=_surface(), output_name="production-shaped.json",
        )
        if result.refusal is not None:
            raise SystemExit(f"canonical run refused: {result.refusal}")
        assert result.presentation_path is not None
        model = json.loads(result.presentation_path.read_text("utf-8"))
    return model


def main() -> None:
    model = regenerate()
    body = json.dumps(model, indent=2, sort_keys=True) + "\n"
    GOLDEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    GOLDEN_PATH.write_text(body, encoding="utf-8")
    print(f"wrote {GOLDEN_PATH.relative_to(ROOT)} ({len(body)} bytes)")


if __name__ == "__main__":
    main()
