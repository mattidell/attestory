"""Track 2 deliverables 3-4 authoritative-surface goldens: lines 3a/3b
publication and line 9 with dividends folded in, entering exclusively
through ``live_coordinate_run`` from an authoritative act log (never a
``RunContext`` shortcut) - the charter's mandatory verification shape,
per the Track 0a review-chain lesson.

The package under test is ``tax.us.2025.package.core-calculations`` v4
(tools/generate_dsbs_t2_content.py), adopted via
``packages/sample_data/frrs_t3/adoptions/adopt-core-v4-current.json`` at
scope year 2053 - a distinct synthetic scope from the v3 goldens in
tests/test_frrs_t4_w2_live_integration.py, so both packages stay
independently exercisable.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.runner import InputFinding, RunContext, SourceFact, run
from packages.derivation.source_authority import ClosureFindingRecord
from packages.derivation.production_resolver import PublicationSurface

REPO = Path(__file__).resolve().parent.parent
CONTENT = REPO / "packages" / "content" / "tax" / "2025"
T3 = REPO / "packages" / "sample_data" / "frrs_t3"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2053"}


def _act(name: str) -> dict[str, object]:
    return cast(dict[str, object], json.loads((T3 / "adoptions" / name).read_text("utf-8")))


def _surface() -> PublicationSurface:
    return PublicationSurface(
        T3 / "publication_surface" / "releases", CONTENT / "published-packages.json", CONTENT
    )


def _live_act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.dsbs.t2.act.{index:03d}",
        "kind": kind,
        "actor": USER,
        "at": f"2026-07-19T00:00:{index:02d}Z",
        "committed_against": index,
        "payload": payload,
    }


def _attested_finding(finding_id: str, fact_id: str, value: object) -> dict[str, object]:
    return {"schema": "finding.v1", "id": finding_id, "fact_id": fact_id, "value": value, "basis": "attested", "evidence_ids": []}


def _dsbs_t2_acts(
    *,
    box1a: float | None = None,
    box1b: float | None = None,
    close_1a: bool = True,
    close_1b: bool = True,
) -> list[dict[str, object]]:
    """A complete synthetic live record for the v4 package.

    ``box1a``/``box1b`` are the single demo statement's box amounts (``None``
    means no member is recorded for that box). ``close_1a``/``close_1b``
    control whether that family's closure finding is asserted at all
    (``False`` leaves the family open/undeclared, blocking its line only -
    the per-box closure independence case).
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
    ):
        add("bundle-adoption", {"bundle": json.loads((CONTENT / name).read_text())})

    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.dsbs.t2.employer", "kind": "tax.us.employer", "label": "Synthetic employer"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.dsbs.t2.w2", "kind": "tax.us.w2-slip", "label": "Synthetic W-2 slip"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.dsbs.t2.payer", "kind": "tax.us.dividend-payer", "label": "Synthetic dividend payer"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.dsbs.t2.stmt", "kind": "tax.us.1099div-statement", "label": "Synthetic 1099-DIV statement"}})

    scope = {"tax-year": "2025", "subject": "demo.primary"}
    families = (
        ("tax.us.2025.w2", "v2", "demo.dsbs.t2.w2.h0"),
        ("tax.us.2025.f1099int.b1", "v1", "demo.dsbs.t2.int-b1.h0"),
        ("tax.us.2025.f1099int.b3", "v1", "demo.dsbs.t2.int-b3.h0"),
        ("tax.us.2025.f1099oid.b1", "v1", "demo.dsbs.t2.oid-b1.h0"),
        ("tax.us.2025.non-form-interest", "v1", "demo.dsbs.t2.nonform.h0"),
        ("tax.us.2025.f1099div.1a", "v1", "demo.dsbs.t2.div1a.h0"),
        ("tax.us.2025.f1099div.1b", "v1", "demo.dsbs.t2.div1b.h0"),
    )
    for family_id, version, horizon_id in families:
        add("horizon-genesis", {"family": {"id": family_id, "version": version}, "scope": scope, "horizon_id": horizon_id})

    def _member(fact_type: str, family_id: str, family_version: str, predecessor: str, successor: str, value: float, finding_id: str) -> None:
        add("member-transition", {
            "family": {"id": family_id, "version": family_version},
            "scope": scope,
            "member": {"action": "assert", "finding": {
                "schema": "finding.v2", "id": finding_id,
                "fact_id": f"{fact_type}|payer=demo.dsbs.t2.payer,statement=demo.dsbs.t2.stmt,tax-year=2025",
                "value": value, "basis": "attested", "evidence_ids": [],
            }},
            "successor": {"id": successor, "predecessor": predecessor},
        })

    div1a_horizon = "demo.dsbs.t2.div1a.h0"
    div1b_horizon = "demo.dsbs.t2.div1b.h0"
    if box1a is not None:
        _member(
            "tax.us.2025.f1099div.box1a-ordinary", "tax.us.2025.f1099div.1a", "v1",
            div1a_horizon, "demo.dsbs.t2.div1a.h1", box1a, "demo.dsbs.t2.finding.box1a",
        )
        div1a_horizon = "demo.dsbs.t2.div1a.h1"
    if box1b is not None:
        _member(
            "tax.us.2025.f1099div.box1b-qualified", "tax.us.2025.f1099div.1b", "v1",
            div1b_horizon, "demo.dsbs.t2.div1b.h1", box1b, "demo.dsbs.t2.finding.box1b",
        )
        div1b_horizon = "demo.dsbs.t2.div1b.h1"

    add("assertion", {"finding": _attested_finding("demo.dsbs.t2.finding.rounding", "rounding.convention|tax-year=2025", "half_up")})
    add("assertion", {"finding": _attested_finding("demo.dsbs.t2.finding.status", "tax.us.2025.filing-status|tax-year=2025", "single")})

    closures = [
        ("demo.dsbs.t2.closure.w2", "tax.us.2025.w2.source-closure", "demo.dsbs.t2.w2.h0"),
        ("demo.dsbs.t2.closure.int-b1", "tax.us.2025.f1099int.b1.source-closure", "demo.dsbs.t2.int-b1.h0"),
        ("demo.dsbs.t2.closure.int-b3", "tax.us.2025.f1099int.b3.source-closure", "demo.dsbs.t2.int-b3.h0"),
        ("demo.dsbs.t2.closure.oid-b1", "tax.us.2025.f1099oid.b1.source-closure", "demo.dsbs.t2.oid-b1.h0"),
        ("demo.dsbs.t2.closure.nonform", "tax.us.2025.non-form-interest.source-closure", "demo.dsbs.t2.nonform.h0"),
    ]
    if close_1a:
        closures.append(("demo.dsbs.t2.closure.div1a", "tax.us.2025.f1099div.1a.source-closure", div1a_horizon))
    if close_1b:
        closures.append(("demo.dsbs.t2.closure.div1b", "tax.us.2025.f1099div.1b.source-closure", div1b_horizon))
    for finding_id, fact_type, horizon_id in closures:
        add("assertion", {"finding": _attested_finding(finding_id, f"{fact_type}|family-horizon={horizon_id},tax-year=2025", True)})

    adoption = _act("adopt-core-v4-current.json")
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts


def _run(acts: list[dict[str, object]], run_id: str) -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        result = live_coordinate_run(
            WorkspaceCapability(root / "L"), repo_root=REPO, authoritative_acts=acts,
            workspace_revision=len(acts), run_scope=SCOPE, scope_user=USER,
            request={"schema": "run-request.v1"}, run_id=run_id, governance_pins=[],
            surface=_surface(), output_name="out.json",
        )
        assert result.refusal is None, result.refusal
        assert result.output_path is not None
        return cast(dict[str, Any], json.loads(result.output_path.read_text()))


def _by_artifact(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Every disposition row, keyed by its producing artifact_id.

    Published and blocked rows both always carry ``artifact_id``; a
    published row additionally carries ``symbol``, a blocked row does not
    (it never published anything to name).
    """
    return {row["artifact_id"]: row for row in report["dispositions"]}


LINE_3B_RULE = "tax.us.2025.rule.form1040-line3b"
LINE_3A_RULE = "tax.us.2025.rule.form1040-line3a"
SUBTOTAL_1A_RULE = "tax.us.2025.rule.f1099div-1a-subtotal"
SUBTOTAL_1B_RULE = "tax.us.2025.rule.f1099div-1b-subtotal"
SUBTOTAL_1B_SYMBOL = "tax.us.2025.dividends.1b-subtotal"
LINE_9_RULE = "tax.us.2025.rule.form1040-line9"


class Lines3a3bPublication(unittest.TestCase):
    """Charter Verification item 1: 3a/3b publication cases.

    The live surface's dispositions carry symbol/disposition/pins/lineage,
    never a raw value (the same shape test_frrs_t4_w2_live_integration.py's
    goldens rely on) - value correctness for the same rule content is
    covered separately by RunContext-level scenario tests below, which are
    supplementary unit coverage, not a substitute for these goldens.
    """

    def test_both_boxes_present_publish_their_own_totals(self) -> None:
        report = _run(_dsbs_t2_acts(box1a=120, box1b=80), "demo.dsbs.t2.both")
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE_3B_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE_3A_RULE]["disposition"], "published")
        # Lineage: each line's publication pins its own box's subtotal
        # finding, never the other box's (per-box closure independence).
        ordinary_pins = {p["id"] for p in rows[LINE_3B_RULE]["pins"]}
        qualified_pins = {p["id"] for p in rows[LINE_3A_RULE]["pins"]}
        self.assertIn(rows[SUBTOTAL_1A_RULE]["finding_id"], ordinary_pins)
        self.assertIn(rows[SUBTOTAL_1B_RULE]["finding_id"], qualified_pins)
        self.assertNotIn(rows[SUBTOTAL_1B_RULE]["finding_id"], ordinary_pins)
        self.assertNotIn(rows[SUBTOTAL_1A_RULE]["finding_id"], qualified_pins)

    def test_qualified_zero_ordinary_present(self) -> None:
        report = _run(_dsbs_t2_acts(box1a=120, box1b=0), "demo.dsbs.t2.qzero")
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE_3B_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE_3A_RULE]["disposition"], "published")

    def test_both_families_closed_empty_publish_honest_zero(self) -> None:
        report = _run(_dsbs_t2_acts(box1a=None, box1b=None), "demo.dsbs.t2.empty")
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE_3B_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE_3A_RULE]["disposition"], "published")
        # A closure-backed zero pins the family closure, never a source finding.
        pinned_ids = {p["id"] for p in rows[SUBTOTAL_1A_RULE]["pins"]}
        self.assertIn("demo.dsbs.t2.closure.div1a", pinned_ids)

    def test_one_family_open_blocks_only_its_own_line(self) -> None:
        # box1a present and closed; box1b's family is left open (no closure
        # asserted) - per-box closure independence: 3a blocks, 3b publishes.
        # The subtotal rule (which evaluates `collect` directly against the
        # source set) reports SOURCE_SET_UNCLOSED; the composing line rule's
        # `requires` gates its own evaluation on the subtotal symbol, so it
        # never reaches its own `require_closed` when and instead reports
        # DEPENDENCY_ABSENT - the same established two-tier pattern already
        # committed for line 2b's interest composition (see
        # packages/sample_data/tax/scenarios/unclosed_interest_composition/
        # expected/report.json: line2b DEPENDENCY_ABSENT, its blocked
        # subtotal rule SOURCE_SET_UNCLOSED).
        report = _run(_dsbs_t2_acts(box1a=120, box1b=None, close_1b=False), "demo.dsbs.t2.open1b")
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE_3B_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE_3A_RULE]["disposition"], "blocked")
        self.assertEqual(rows[LINE_3A_RULE]["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(rows[LINE_3A_RULE]["missing"], [SUBTOTAL_1B_SYMBOL])
        self.assertEqual(rows[SUBTOTAL_1B_RULE]["code"], "SOURCE_SET_UNCLOSED")


class Line9WithDividends(unittest.TestCase):
    """Charter Verification item 2: line 9 with dividends folded in."""

    def test_total_income_publishes_pinning_ordinary_dividends(self) -> None:
        report = _run(_dsbs_t2_acts(box1a=120, box1b=80), "demo.dsbs.t2.line9")
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE_9_RULE]["disposition"], "published")
        pinned_ids = {p["id"] for p in rows[LINE_9_RULE]["pins"]}
        self.assertIn(rows[LINE_3B_RULE]["finding_id"], pinned_ids)

    def test_zero_dividends_still_publishes_total_income(self) -> None:
        report = _run(_dsbs_t2_acts(box1a=None, box1b=None), "demo.dsbs.t2.line9zero")
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE_9_RULE]["disposition"], "published")


class Line3a3bAndLine9Values(unittest.TestCase):
    """Supplementary value-correctness coverage over the same committed rule
    content, at the RunContext/evaluator level (not a substitute for the
    live_coordinate_run goldens above - those are the authoritative surface;
    this class only pins down the arithmetic)."""

    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.canon = load_canon(self.schemas)
        self.family_1a = json.loads((CONTENT / "family.f1099div-1a.json").read_text())
        self.family_1b = json.loads((CONTENT / "family.f1099div-1b.json").read_text())
        self.mapping_1a = json.loads((CONTENT / "closure-mapping.f1099div-1a.json").read_text())
        self.mapping_1b = json.loads((CONTENT / "closure-mapping.f1099div-1b.json").read_text())
        self.subtotal_1a = json.loads((CONTENT / "rule.f1099div-1a-subtotal.json").read_text())
        self.subtotal_1b = json.loads((CONTENT / "rule.f1099div-1b-subtotal.json").read_text())
        self.line3a = json.loads((CONTENT / "rule.form1040-line3a.json").read_text())
        self.line3b = json.loads((CONTENT / "rule.form1040-line3b.json").read_text())
        self.line9 = json.loads((CONTENT / "rule.form1040-line9.v2.json").read_text())

    def _context(self, sources: list[SourceFact]) -> RunContext:
        return RunContext(
            run_id="demo.dsbs.t2.values",
            rules=[self.subtotal_1a, self.subtotal_1b, self.line3a, self.line3b, self.line9],
            parameters={},
            canon=self.canon,
            inputs=[
                InputFinding("rounding.convention", "half_up", "demo.round", "input"),
                InputFinding("tax.us.2025.wages.total-w2-box1", "0", "demo.wages", "input"),
                InputFinding("tax.us.2025.interest.taxable-total", "0", "demo.int", "input"),
            ],
            sources=sources,
            adoption_pin={"role": "adoption", "id": "tax.us.2025.package.core-calculations", "version": "v4"},
            governance_pins=[],
            family_declarations=[self.family_1a, self.family_1b],
            closure_mappings=[self.mapping_1a, self.mapping_1b],
            closure_findings=[
                ClosureFindingRecord("demo.closure.1a", "tax.us.2025.f1099div.1a.source-closure", "demo.h1a", True),
                ClosureFindingRecord("demo.closure.1b", "tax.us.2025.f1099div.1b.source-closure", "demo.h1b", True),
            ],
            current_horizons={self.family_1a["id"]: "demo.h1a", self.family_1b["id"]: "demo.h1b"},
        )

    def test_both_present_line9_sums_ordinary_only(self) -> None:
        ctx = self._context(
            [
                SourceFact("tax.us.2025.f1099div.box1a-ordinary", "120", "demo.f.1a"),
                SourceFact("tax.us.2025.f1099div.box1b-qualified", "80", "demo.f.1b"),
            ],
        )
        result = run(ctx, self.schemas)
        published = {p.finding["symbol"]: p.finding["value"] for p in result.publications}
        self.assertEqual(published["tax.us.2025.dividends.ordinary-total"], "120")
        self.assertEqual(published["tax.us.2025.dividends.qualified-total"], "80")
        self.assertEqual(published["tax.us.2025.income.total-income"], "120")


if __name__ == "__main__":
    unittest.main()
