"""Track 6: the ten synthetic end-to-end disposition-path models
(integration-surface artifact 6) and presentation-model probes for the
Form 1098-E Student Loan Interest Deduction / AGI milestone.

Closes ``docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md``
Track 0's ``PENDING`` "Integration surface" row: every path here is *run*
through the real coordinator (``live_coordinate_run``, ``packages/derivation/
live.py:105``) against a real, wired production package (``package.core-
calculations`` v33 / ``published-packages`` v28 / release v26 / the
``adopt-core-v33-current`` fixture, built by ``tools/
generate_f1098e_track6_content.py``), matching the ``ssa-no-activity-
applicability`` precedent's own evidentiary bar
(``tests/test_ssa_no_activity_line6b_track1.py``) exactly.

Paths (a)-(i) are the nine disposition paths named in artifact 6's own
"Synthetic end-to-end models required" paragraph. Path (j) is the tenth
case the foreman chartered on review of Track 3: a multi-statement family
whose two statements *disagree* on a per-statement universal eligibility
witness, exercising the known ``packages/derivation/marshal.py`` unkeyed-ref
limitation Track 3 carried forward, live, for the first time.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.findings import FindingModelError
from packages.tax.loader import TAX_CONTENT_DIR
from tests.test_form1099g_box1_schedule1_line7 import _act, _attested, _disposition, _published_numeric
from tests.test_ssa1099_benefits_line6_track2 import _ssa_acts

ROOT = Path(__file__).resolve().parent.parent
CONTENT = TAX_CONTENT_DIR
FIXTURES = ROOT / "packages" / "sample_data" / "f1098e_student_loan_interest_track6"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2025"}
SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}

FAMILY_ID = "tax.us.2025.f1098e.1"
BOX1 = "tax.us.2025.f1098e.box1-student-loan-interest"
BOX2 = "tax.us.2025.f1098e.box2-checked-authority"
CLOSURE_TYPE = "tax.us.2025.f1098e.1.source-closure"
LINE21 = "tax.us.2025.schedule1.line21-sli-deduction"
LINE26 = "tax.us.2025.schedule1.line26-total-adjustments"

UNIVERSAL_WITNESS_TOKENS = (
    "no-related-person-interest",
    "no-qualified-employer-plan-interest",
    "no-non-qualified-loan-component",
    "no-employer-educational-assistance-interest",
    "no-qtp-earnings-used",
)

SLI_SCOPE_UNIVERSAL_TOKENS = (
    "no-form-2555",
    "no-form-4563",
    "no-puerto-rico-or-samoa-income",
)
SLI_SCOPE_LEGAL_ZERO_TOKENS = (
    "not-claimed-as-dependent",
    "legally-obligated-for-interest",
)

SCHED1_LINE_TOKENS = (
    "no-line11-educator", "no-line12-business-expenses", "no-line13-hsa",
    "no-line14-moving", "no-line15-deductible-se", "no-line16-se-retirement",
    "no-line17-se-health", "no-line18-penalty", "no-line19-alimony-paid",
    "no-line20-ira-deduction", "no-line23-archer-msa", "no-line25-other-adjustments",
)

# Sections bound by the form-field-bound symbols the integration surface names.
SECTIONS = ("line-10", "line-11a", "line-11b", "line-sch1-21")


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))


def _surface() -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases",
        CONTENT / "published-packages.v28.json",
        CONTENT,
    )


def _load_fixture_adoption() -> dict[str, object]:
    return cast(
        dict[str, object],
        json.loads((FIXTURES / "adoptions" / "adopt-core-v33-current.json").read_text("utf-8")),
    )


def _member_fact_id(fact_type: str, lender: str, statement: str) -> str:
    return f"{fact_type}|lender={lender},statement={statement},tax-year=2025"


class Statement:
    """One synthetic Form 1098-E statement to admit into the family."""

    def __init__(
        self,
        *,
        lender: str,
        stmt: str,
        box1: float,
        box2: object = False,
        witnesses: dict[str, str] | None = None,
    ) -> None:
        self.lender = lender
        self.stmt = stmt
        self.box1 = box1
        self.box2 = box2
        self.witnesses = dict.fromkeys(UNIVERSAL_WITNESS_TOKENS, "yes")
        if witnesses:
            self.witnesses.update(witnesses)


def _f1098e_acts(
    *,
    statements: list[Statement] | None = None,
    close: bool = True,
    wages: float = 90000,
    filing_status: str = "single",
    sli_scope_overrides: dict[str, str] | None = None,
    sched1_overrides: dict[str, str] | None = None,
    assert_sli_scope: bool = True,
    assert_sched1_scope: bool = True,
    extra: list[dict[str, object]] | None = None,
    horizon_prefix: str = "demo.f1098e.h",
) -> list[dict[str, object]]:
    """Extend the proven SSA-1099/IRA base return with a Form 1098-E
    statement lifecycle, mirroring ``tests/test_f1098_mortgage_interest_
    line12e_track2.py``'s ``_f1098_acts`` shape one family over.

    ``statements=None`` or ``[]`` means a closed-empty family: the source
    family is still closed (when ``close=True``), just with zero current
    members. Every statement gets its own lender/statement entity pair and
    advances the family's own horizon lineage.
    """
    acts = _ssa_acts(benefits=[], close=True, wages=wages, filing_status=filing_status)
    acts.pop()  # drop the SSA-1099 milestone's own trailing adoption

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load("f1098e.bundle.json")})
    add("bundle-adoption", {"bundle": _load("sli-scope.bundle.json")})
    if assert_sched1_scope and not any(
        act.get("kind") == "bundle-adoption"
        and cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("bundle", {})).get("id")
        == "tax.us.2025.schedule1-adjustments-scope.vocabulary"
        for act in acts
    ):
        add("bundle-adoption", {"bundle": _load("schedule1-adjustments-scope.bundle.json")})

    stmts = statements or []
    for s in stmts:
        add(
            "entity-introduced",
            {"entity": {"schema": "entity.v1", "id": s.lender, "kind": "tax.us.student-loan-lender", "label": "Synthetic student loan lender"}},
        )
        add(
            "entity-introduced",
            {"entity": {"schema": "entity.v1", "id": s.stmt, "kind": "tax.us.1098e-statement", "label": "Synthetic Form 1098-E"}},
        )

    add("horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": SCOPE_KEY, "horizon_id": f"{horizon_prefix}0"})
    horizon = f"{horizon_prefix}0"

    for index, s in enumerate(stmts):
        # Companion-presence admission (BOX2, kernel-enforced) requires the
        # companion already current *before* the subordinate (box1) fact
        # touches -- enforcement runs per-act against the fully-updated
        # successor state, so a same-batch-but-later act does not satisfy
        # it. Mirrors tests/test_ssa1099_benefits_line6_track2.py's own
        # "assert companions first" ordering for its box5/box3-6 companion
        # set. Plain "assertion" acts (not "member-transition") keep the
        # family on the genesis horizon; only the late-member path below
        # advances the horizon.
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.f1098e.box2.{index}",
                    _member_fact_id(BOX2, s.lender, s.stmt),
                    s.box2,
                )
            },
        )
        for token, value in s.witnesses.items():
            add(
                "assertion",
                {
                    "finding": _attested(
                        f"demo.f1098e.{token}.{index}",
                        _member_fact_id(f"tax.us.2025.f1098e.{token}", s.lender, s.stmt),
                        value,
                    )
                },
            )
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.f1098e.box1.{index}",
                    _member_fact_id(BOX1, s.lender, s.stmt),
                    s.box1,
                )
            },
        )

    if close:
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.f1098e.closure",
                    f"{CLOSURE_TYPE}|family-horizon={horizon},tax-year=2025",
                    True,
                )
            },
        )

    if assert_sli_scope:
        sli_values = {token: "yes" for token in SLI_SCOPE_UNIVERSAL_TOKENS + SLI_SCOPE_LEGAL_ZERO_TOKENS}
        if sli_scope_overrides:
            sli_values.update(sli_scope_overrides)
        for token, value in sli_values.items():
            add(
                "assertion",
                {
                    "finding": _attested(
                        f"demo.sli-scope.{token}",
                        f"tax.us.2025.sli-scope.{token}|tax-year=2025",
                        value,
                    )
                },
            )

    if assert_sched1_scope:
        sched1_values = {token: "yes" for token in SCHED1_LINE_TOKENS}
        if sched1_overrides:
            sched1_values.update(sched1_overrides)
        for token, value in sched1_values.items():
            add(
                "assertion",
                {
                    "finding": _attested(
                        f"demo.sched1.{token}",
                        f"tax.us.2025.schedule1-adjustments-scope.{token}|tax-year=2025",
                        value,
                    )
                },
            )

    for item in extra or []:
        acts.append(item)

    adoption = _load_fixture_adoption()
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts


def _renumber(acts: list[dict[str, object]]) -> list[dict[str, object]]:
    for index, act in enumerate(acts):
        act["committed_against"] = index
        act["act_id"] = f"demo.f1098e.t6.act.{index:03d}"
    return acts


def execute(
    acts: list[dict[str, object]], run_id: str
) -> tuple[dict[str, Any], dict[str, Any] | None, str | None]:
    acts = _renumber(list(acts))
    with TemporaryDirectory() as tmp:
        result = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope=SCOPE,
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=_surface(),
            output_name="out.json",
        )
        if result.refusal is not None:
            return {}, None, str(result.refusal)
        assert result.output_path is not None and result.presentation_path is not None
        return (
            json.loads(result.output_path.read_text("utf-8")),
            json.loads(result.presentation_path.read_text("utf-8")),
            None,
        )


def _by_artifact(report: dict[str, Any], artifact_id: str) -> list[dict[str, Any]]:
    return [row for row in report.get("dispositions", []) if row.get("artifact_id") == artifact_id]


def _line21_rows(report: dict[str, Any]) -> list[dict[str, Any]]:
    return _by_artifact(report, "tax.us.2025.rule.sli-worksheet")


def _assert_valid_model_and_cardinality(model: dict[str, Any] | None) -> None:
    """Cardinality check: exactly one presentation row per form-field-bound
    symbol, mirroring the SSA no-activity precedent's own obligation 9."""
    assert model is not None
    assert model["schema"] == "presentation-model.v1"
    seen_ids = [section["id"] for section in model.get("sections", [])]
    for section_id in SECTIONS:
        assert seen_ids.count(section_id) == 1, (section_id, seen_ids)


# --- (a) closed-empty family --------------------------------------------


class TestPathAClosedEmpty(unittest.TestCase):
    def test_closed_empty_family_computes_zero_line21_attachment_unaffected(self) -> None:
        acts = _f1098e_acts(statements=[], close=True, wages=90000)
        report, model, refusal = execute(acts, "t6.a.closed-empty")
        self.assertIsNone(refusal)
        _assert_valid_model_and_cardinality(model)
        assert model is not None
        rows = _line21_rows(report)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "published")
        self.assertEqual(_published_numeric(model, "line-sch1-21"), 0)
        self.assertEqual(_disposition(model, "line-sch1-21"), "closure_backed_zero")
        # Line 26/AGI unaffected by this route's presence at $0.
        self.assertEqual(_disposition(model, "line-11a"), "published_value")


# --- (b) single statement, full eligibility, MAGI below phaseout floor --


class TestPathBFullyEligibleBelowFloor(unittest.TestCase):
    def test_single_statement_below_floor_full_capped_deduction_attachment_required(self) -> None:
        # box1 = 3000 (over cap) -> line1 = 2500 capped; wages 50000 total
        # income well under the $85000 single threshold -> ratio 0, full cap.
        statements = [Statement(lender="demo.f1098e.lender.b", stmt="demo.f1098e.stmt.b", box1=3000.0)]
        acts = _f1098e_acts(statements=statements, close=True, wages=50000)
        report, model, refusal = execute(acts, "t6.b.below-floor")
        self.assertIsNone(refusal)
        _assert_valid_model_and_cardinality(model)
        assert model is not None
        self.assertEqual(_published_numeric(model, "line-sch1-21"), 2500)
        self.assertEqual(_disposition(model, "line-sch1-21"), "published_value")
        attachment = next(a for a in model["attachments"] if a["id"] == "tax.us.2025.rule.attachment.schedule-1")
        self.assertEqual(attachment["resolved"]["disposition"], "published")


# --- (c) single statement, MAGI inside the phaseout band ----------------


class TestPathCPhaseoutBand(unittest.TestCase):
    def test_single_statement_in_phaseout_band_reduces_deduction(self) -> None:
        # box1 = 2000 (under cap); wages 90000 single threshold 85000, range
        # 15000 -> ratio 5000/15000 = 0.333 -> line9 = 2000 - 666 = 1334.
        statements = [Statement(lender="demo.f1098e.lender.c", stmt="demo.f1098e.stmt.c", box1=2000.0)]
        acts = _f1098e_acts(statements=statements, close=True, wages=90000)
        report, model, refusal = execute(acts, "t6.c.phaseout-band")
        self.assertIsNone(refusal)
        _assert_valid_model_and_cardinality(model)
        assert model is not None
        self.assertEqual(_published_numeric(model, "line-sch1-21"), 1334)
        self.assertEqual(_disposition(model, "line-sch1-21"), "published_value")


# --- (d) single statement, MAGI at/above ceiling -------------------------


class TestPathDAtOrAboveCeiling(unittest.TestCase):
    def test_magi_at_or_above_ceiling_computes_zero_not_blocked(self) -> None:
        statements = [Statement(lender="demo.f1098e.lender.d", stmt="demo.f1098e.stmt.d", box1=1000.0)]
        acts = _f1098e_acts(statements=statements, close=True, wages=110000)
        report, model, refusal = execute(acts, "t6.d.at-ceiling")
        self.assertIsNone(refusal)
        _assert_valid_model_and_cardinality(model)
        assert model is not None
        rows = _line21_rows(report)
        self.assertEqual(rows[0]["disposition"], "published")
        self.assertEqual(_published_numeric(model, "line-sch1-21"), 0)
        self.assertEqual(_disposition(model, "line-sch1-21"), "computed_zero")


# --- (e) box 2 checked -> hard admission-time block ----------------------


class TestPathEBox2Checked(unittest.TestCase):
    def test_box2_checked_is_rejected_at_kernel_admission(self) -> None:
        """Per rule.sli-worksheet.json's own notes (T0-3, component 8): box 2's
        value_schema admits only null/false and box-1 is registered as its
        companion-presence pair, so a checked box 2 is rejected at kernel
        admission before any box-1 finding bearing it could ever become
        current -- a *harder* block than a runtime ``blocked`` disposition,
        never a silent full-box-1 pass-through. Observed directly, not
        assumed: this raises ``FindingModelError`` inside ``live_coordinate_
        run`` itself. The actual rejection point observed is even earlier
        than the companion-presence check the box-1/box-4 pair exercises
        (``test_form1099g_box1_schedule1_line7.py::test_n2_nonzero_box4_rejected``):
        box 2's own ``value_schema`` (``anyOf`` null/false) rejects the
        finding outright before companion-presence admission is ever
        reached."""
        statements = [Statement(lender="demo.f1098e.lender.e", stmt="demo.f1098e.stmt.e", box1=1000.0, box2=True)]
        acts = _renumber(_f1098e_acts(statements=statements, close=True, wages=50000))
        with self.assertRaises(FindingModelError) as ctx:
            with TemporaryDirectory() as tmp:
                live_coordinate_run(
                    WorkspaceCapability(Path(tmp) / "L"),
                    repo_root=ROOT,
                    authoritative_acts=acts,
                    workspace_revision=len(acts),
                    run_scope=SCOPE,
                    scope_user=USER,
                    request={"schema": "run-request.v1"},
                    run_id="t6.e.box2-checked",
                    governance_pins=[],
                    surface=_surface(),
                    output_name="out.json",
                )
        message = str(ctx.exception)
        # Observed: box 2's own value_schema (anyOf null/false) rejects the
        # assertion before the companion-presence check is ever reached --
        # an even harder, earlier admission-time block than the
        # companion-presence shape f1099g box-1/box-4 exercises.
        self.assertIn("does not conform to", message)
        self.assertIn(BOX2, message)


# --- (f) universal-component violation ------------------------------------


class TestPathFUniversalComponentViolation(unittest.TestCase):
    def test_related_person_interest_present_blocks_whole_route(self) -> None:
        statements = [
            Statement(
                lender="demo.f1098e.lender.f", stmt="demo.f1098e.stmt.f", box1=1000.0,
                witnesses={"no-related-person-interest": "no"},
            )
        ]
        acts = _f1098e_acts(statements=statements, close=True, wages=50000)
        report, model, refusal = execute(acts, "t6.f.universal-violation")
        self.assertIsNone(refusal)
        _assert_valid_model_and_cardinality(model)
        assert model is not None
        rows = _line21_rows(report)
        self.assertEqual(rows[0]["disposition"], "blocked")
        self.assertEqual(rows[0]["code"], "SLI_UNIVERSAL_COMPONENT_VIOLATION")
        self.assertEqual(_disposition(model, "line-sch1-21"), "blocked")


# --- (g) legal-zero component answered against deduction -----------------


class TestPathGLegalZero(unittest.TestCase):
    def test_claimed_as_dependent_computes_zero_not_blocked(self) -> None:
        statements = [Statement(lender="demo.f1098e.lender.g", stmt="demo.f1098e.stmt.g", box1=1000.0)]
        acts = _f1098e_acts(
            statements=statements, close=True, wages=50000,
            sli_scope_overrides={"not-claimed-as-dependent": "no"},
        )
        report, model, refusal = execute(acts, "t6.g.legal-zero")
        self.assertIsNone(refusal)
        _assert_valid_model_and_cardinality(model)
        assert model is not None
        rows = _line21_rows(report)
        self.assertEqual(rows[0]["disposition"], "published")
        self.assertEqual(_published_numeric(model, "line-sch1-21"), 0)
        self.assertEqual(_disposition(model, "line-sch1-21"), "computed_zero")


# --- (h) unclosed family ---------------------------------------------------


class TestPathHUnclosed(unittest.TestCase):
    def test_unclosed_family_blocks_source_set_unclosed(self) -> None:
        statements = [Statement(lender="demo.f1098e.lender.h", stmt="demo.f1098e.stmt.h", box1=1000.0)]
        acts = _f1098e_acts(statements=statements, close=False, wages=50000)
        report, model, refusal = execute(acts, "t6.h.unclosed")
        self.assertIsNone(refusal)
        _assert_valid_model_and_cardinality(model)
        assert model is not None
        rows = _line21_rows(report)
        self.assertEqual(rows[0]["disposition"], "blocked")
        self.assertEqual(rows[0]["code"], "SOURCE_SET_UNCLOSED")
        self.assertEqual(_disposition(model, "line-sch1-21"), "blocked")


# --- (i) late member added after prior close ------------------------------


def _late_member_extension(
    late: Statement, *, predecessor_horizon: str, successor_horizon: str, reclose: bool
) -> list[dict[str, object]]:
    """The acts that admit ``late`` on a successor horizon (member-transition),
    mirroring ``tests/test_ssa_no_activity_line6b_track1.py``'s own
    ``_late_member_acts`` shape: companions asserted first (plain
    ``assertion``, same-batch-before ordering for companion-presence
    admission), then a ``member-transition`` for box1 itself carries the
    horizon succession. ``reclose`` appends a fresh closure attestation
    keyed on the new horizon; when False, the prior closure (keyed on the
    old horizon) is left displaced and un-renewed."""
    ext: list[dict[str, object]] = [
        {"kind": "entity-introduced", "payload": {"entity": {"schema": "entity.v1", "id": late.lender, "kind": "tax.us.student-loan-lender", "label": "Late synthetic lender"}}},
        {"kind": "entity-introduced", "payload": {"entity": {"schema": "entity.v1", "id": late.stmt, "kind": "tax.us.1098e-statement", "label": "Late synthetic Form 1098-E"}}},
        {"kind": "assertion", "payload": {"finding": _attested("demo.f1098e.late.box2", _member_fact_id(BOX2, late.lender, late.stmt), late.box2)}},
    ]
    for token, value in late.witnesses.items():
        ext.append(
            {"kind": "assertion", "payload": {"finding": _attested(f"demo.f1098e.late.{token}", _member_fact_id(f"tax.us.2025.f1098e.{token}", late.lender, late.stmt), value)}}
        )
    ext.append(
        {
            "kind": "member-transition",
            "payload": {
                "family": {"id": FAMILY_ID, "version": "v1"},
                "scope": SCOPE_KEY,
                "member": {
                    "action": "assert",
                    "finding": _attested("demo.f1098e.late.box1", _member_fact_id(BOX1, late.lender, late.stmt), late.box1),
                },
                "successor": {"id": successor_horizon, "predecessor": predecessor_horizon},
            },
        }
    )
    if reclose:
        ext.append(
            {
                "kind": "assertion",
                "payload": {
                    "finding": _attested(
                        "demo.f1098e.closure.late",
                        f"{CLOSURE_TYPE}|family-horizon={successor_horizon},tax-year=2025",
                        True,
                    )
                },
            }
        )
    return [{"schema": "act.v1", "act_id": "", "actor": USER, "at": "2026-08-15T12:00:00Z", "committed_against": 0, **e} for e in ext]


class TestPathILateMember(unittest.TestCase):
    def test_late_member_displaces_closure_and_reclosure_recomputes(self) -> None:
        base_statements = [Statement(lender="demo.f1098e.lender.i0", stmt="demo.f1098e.stmt.i0", box1=1000.0)]
        h0 = "demo.f1098e.hi.0"
        h1 = "demo.f1098e.hi.1"
        acts0 = _f1098e_acts(statements=base_statements, close=True, wages=50000, horizon_prefix="demo.f1098e.hi.")
        report0, model0, refusal0 = execute(acts0, "t6.i.base")
        self.assertIsNone(refusal0)
        assert model0 is not None
        self.assertEqual(_line21_rows(report0)[0]["disposition"], "published")
        self.assertEqual(_published_numeric(model0, "line-sch1-21"), 1000)

        # Add a second, late statement on a successor horizon WITHOUT a fresh
        # closure attestation on that horizon: the prior closure (keyed on
        # h0) is displaced by horizon succession (ADR-0017), reproducing
        # artifact 3's trace live, not merely on paper.
        late = Statement(lender="demo.f1098e.lender.i1", stmt="demo.f1098e.stmt.i1", box1=500.0)
        late_unclosed = _late_member_extension(late, predecessor_horizon=h0, successor_horizon=h1, reclose=False)
        acts1 = _f1098e_acts(statements=base_statements, close=True, wages=50000, horizon_prefix="demo.f1098e.hi.", extra=late_unclosed)
        report1, model1, refusal1 = execute(acts1, "t6.i.late-unclosed")
        self.assertIsNone(refusal1)
        assert model1 is not None
        rows1 = _line21_rows(report1)
        self.assertEqual(rows1[0]["disposition"], "blocked")
        self.assertEqual(rows1[0]["code"], "SOURCE_SET_UNCLOSED")
        self.assertEqual(_disposition(model1, "line-sch1-21"), "blocked")

        # Reclose on the new horizon: recomputes with both members.
        late_reclosed = _late_member_extension(late, predecessor_horizon=h0, successor_horizon=h1, reclose=True)
        acts2 = _f1098e_acts(statements=base_statements, close=True, wages=50000, horizon_prefix="demo.f1098e.hi.", extra=late_reclosed)
        report2, model2, refusal2 = execute(acts2, "t6.i.reclosed")
        self.assertIsNone(refusal2)
        _assert_valid_model_and_cardinality(model2)
        assert model2 is not None
        rows2 = _line21_rows(report2)
        self.assertEqual(rows2[0]["disposition"], "published")
        self.assertEqual(_disposition(model2, "line-sch1-21"), "published_value")
        self.assertEqual(_published_numeric(model2, "line-sch1-21"), 1500)


# --- (j) multi-statement disagreement on a per-statement witness ----------


class TestPathJMultiStatementDisagreement(unittest.TestCase):
    """Foreman-chartered on review of Track 3: two statements, different
    lenders, disagreeing on ``no-related-person-interest`` (one "yes", one
    "no"). Track 3 flagged that ``marshal.py`` bound only one arbitrary
    current finding per unkeyed symbol for these per-statement refs, so
    this case's actual behavior had never been observed running until
    Track 6 first ran it live.

    **Track 6 (2026-08-15): observed, not assumed** (both statement
    orderings run below): the real pre-repair behavior was order-dependent
    -- reordering the same two statements changed the disposition between
    ``blocked`` and a published $1500 that silently included the
    disqualified statement's own interest, contradicting Track 0
    adversarial closure artifact 2 ("never a silent zero and never a
    silent full-box-1 pass-through"). Not repaired in Track 6; reported as
    a finding instead (out of that track's scope per the standing
    authorization's stop condition on touching an already-reviewed rule's
    computed values without reporting first).

    **Track 6b (owner-dispositioned repair): fixed and reproved here.**
    ``tax.us.2025.rule.sli-worksheet.json``'s five per-statement universal
    witnesses now read via the new ``collect_categorical_all_equal``
    evaluator op (``rule-artifact.v6``) over every current finding for the
    witness fact type, marshalled as ``sources`` (never a single unkeyed
    ``ref``) -- a true "no member answers 'no'" universal test, independent
    of assertion order. ``packages/derivation/marshal.py`` was additionally
    hardened (Track 6b guard) so an unkeyed binding matching two or more
    *disagreeing* current findings for a symbol that is not a collect
    source name is left unbound (an ordinary blocked disposition) rather
    than arbitrarily picking one. **Both orderings below now correctly
    block** with ``SLI_UNIVERSAL_COMPONENT_VIOLATION`` -- there is no
    longer an "order" that matters, since the witness is read via a
    universal test over every member, not a single arbitrary one. Kept as
    permanent regression fixtures for both statement orderings."""

    def _run_pair(self, *, violation_first: bool, run_id: str) -> tuple[dict[str, Any], dict[str, Any] | None]:
        clean = Statement(
            lender=f"demo.f1098e.lender.{run_id}.clean", stmt=f"demo.f1098e.stmt.{run_id}.clean", box1=1000.0,
            witnesses={"no-related-person-interest": "yes"},
        )
        violating = Statement(
            lender=f"demo.f1098e.lender.{run_id}.bad", stmt=f"demo.f1098e.stmt.{run_id}.bad", box1=500.0,
            witnesses={"no-related-person-interest": "no"},
        )
        statements = [violating, clean] if violation_first else [clean, violating]
        acts = _f1098e_acts(statements=statements, close=True, wages=50000)
        report, model, refusal = execute(acts, run_id)
        self.assertIsNone(refusal)
        _assert_valid_model_and_cardinality(model)
        return report, model

    def test_violation_asserted_last_correctly_blocks(self) -> None:
        report, model = self._run_pair(violation_first=False, run_id="t6.j.violation-last")
        assert model is not None
        rows = _line21_rows(report)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "blocked")
        self.assertEqual(rows[0]["code"], "SLI_UNIVERSAL_COMPONENT_VIOLATION")
        self.assertEqual(_disposition(model, "line-sch1-21"), "blocked")

    def test_violation_asserted_first_also_correctly_blocks(self) -> None:
        """Track 6b repair, reproved live: the same real-world facts (one
        statement has a related-person-interest violation) as the test
        above, only the assertion order swapped, must produce the *same*
        disposition -- correctly blocked, never a published $1500 that
        silently includes the disqualified statement's own interest. This
        is the order-dependence this repair exists to eliminate: before
        Track 6b, swapping the order alone changed the disposition; after
        it, it does not."""
        report, model = self._run_pair(violation_first=True, run_id="t6.j.violation-first")
        assert model is not None
        rows = _line21_rows(report)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "blocked")
        self.assertEqual(rows[0]["code"], "SLI_UNIVERSAL_COMPONENT_VIOLATION")
        self.assertEqual(_disposition(model, "line-sch1-21"), "blocked")


if __name__ == "__main__":
    unittest.main()
