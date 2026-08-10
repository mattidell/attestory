"""Track 2: Form 1098 mortgage interest through Schedule A, line 12e/13a/13b/14,
and taxable income (line 15) - required-evidence integration against the real
v29 package via ``live_coordinate_run``.

Base return corpus: reuse ``_ssa_acts`` (the SSA-1099 milestone's own Track 2
fixture, which itself extends ``_ira_acts``) rather than ``_ira_acts`` alone,
since v29 is built on the v28 base tip that already includes SSA-1099's own
closed families and residual-scope declarations - any rule reachable from
v28 (AGI, line 9, the SS benefits worksheet, line 2a residual scopes, etc.)
needs those closures satisfied even for a return with no SSA-1099 benefits
(``benefits=[]``), or it blocks with ``DEPENDENCY_ABSENT``/``SOURCE_SET_UNCLOSED``
rather than a genuine Form-1098-specific finding. This milestone's own acts
are additive-only on top of that already-proven, fully-closed corpus - then
splice in the Form 1098 statement lifecycle (mirroring
``tests/test_f1098_mortgage_interest_lifecycle.py``'s act shapes, now driven
through the real v29 package rather than a resolver monkeypatch) and swap
the trailing adoption for this milestone's own v29 fixture.

2025 single standard deduction is $15,000
(``parameter.standard-deduction-base.json``), with no age/blindness
additions asserted, so it is exact and stable across every case here.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import load_published_citizen_checksums, validate_package
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.facts import fact_id_for
from packages.tax.loader import TAX_CONTENT_DIR
from tests.test_form1099g_box1_schedule1_line7 import _attested, _corpus, _disposition, _published_numeric
from tests.test_form1099r_ira_line4b_track2 import _ira_acts
from tests.test_ssa1099_benefits_line6_track2 import _report_item, _ssa_acts

ROOT = Path(__file__).resolve().parent.parent
CONTENT = TAX_CONTENT_DIR
FIXTURES = ROOT / "packages" / "sample_data" / "f1098_mortgage_interest_line12e"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2025"}
SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}

FAMILY_ID = "tax.us.2025.f1098"
ITEMIZED_ASSERTION = "tax.us.2025.deductions.itemized"
NO_MORTGAGE_STATEMENT_FLAG = "tax.us.2025.f1098-scope.no-mortgage-statement"
STANDARD_DEDUCTION_SINGLE = 15000.0

AUTHORITY = (
    "liable-and-paid",
    "qualified-main-home",
    "acquisition-debt-use",
    "no-balance-increase",
    "no-refinance",
    "single-mortgage-single-home",
    "not-shared-except-spouse",
    "no-mortgage-interest-credit",
)

# Repair round 3 finding 2: the seven Schedule A boundary categories' own
# mandatory absence-declaration facts (schedule-a-boundary.bundle.json,
# edited in place to add them) and the two QBI/Schedule-1-A absence-
# declaration facts (qbi-schedule1a-scope.bundle.json, new this round).
SCHEDULE_A_BOUNDARY_CATEGORIES = (
    "no-medical",
    "no-salt",
    "no-other-interest",
    "no-investment-interest",
    "no-charitable",
    "no-casualty-theft",
    "no-gambling-other",
)
SCHEDULE_A_BOUNDARY_DECLARED_SYMBOLS = tuple(
    f"tax.us.2025.schedule-a-boundary.{cat}-declared" for cat in SCHEDULE_A_BOUNDARY_CATEGORIES
)
QBI_NO_DEDUCTION_DECLARED = "tax.us.2025.qbi.no-qbi-deduction-declared"
SCHEDULE1A_NO_ADDITIONAL_DEDUCTIONS_DECLARED = "tax.us.2025.schedule1a.no-additional-deductions-declared"


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))


def _member_fact_id(fact_type: str, payer: str, statement: str) -> str:
    return fact_id_for(
        fact_type,
        (
            ("payer", payer),
            ("statement", statement),
            ("tax-year", "2025"),
        ),
    )


def _surface() -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases",
        CONTENT / "published-packages.v24.json",
        CONTENT,
    )


def _load_fixture_adoption() -> dict[str, object]:
    return cast(
        dict[str, object],
        json.loads((FIXTURES / "adoptions" / "adopt-core-v29-current.json").read_text("utf-8")),
    )


def _f1098_acts(
    *,
    interest: float | None,
    box2: float = 200000.0,
    box3: str = "2020-06-01",
    box4: float = 0.0,
    box5: float = 0.0,
    box6: float = 0.0,
    box9: float = 1.0,
    box11: float = 0.0,
    authority_overrides: dict[str, str] | None = None,
    itemized_assertion: float | None = None,
    second_statement_interest: float | None = None,
    wages: float = 90000,
    assert_scope_flag: bool = True,
    scope_flag_value: bool = False,
    boundary_declarations: dict[str, str] | None = None,
    assert_boundary_declarations: bool = True,
    qbi_declaration: str = "yes",
    schedule1a_declaration: str = "yes",
    assert_qbi_schedule1a_declarations: bool = True,
) -> list[dict[str, object]]:
    """Extend the proven SSA-1099/IRA base return with a Form 1098 statement
    lifecycle.

    ``interest is None`` means no Form 1098 statement at all (the family is
    still closed, but closed-empty: count 0, the out-of-milestone/legacy
    path). ``second_statement_interest`` adds a second, distinct statement
    identity to exercise the MULTIPLE_F1098_OUT_OF_SCOPE guard alongside a
    normal single-statement admission. ``wages`` defaults to 90000 (matching
    this suite's original IRA-precedent base) so AGI comfortably exceeds the
    standard deduction and any Form 1098 deduction in this test file's cases
    - a taxable-income recomputation test on a $15,000-wage base would floor
    at 0 well before line 15 exercises anything interesting. ``assert_scope_flag``
    defaults to True (matching every ordinary caller); set False to build the
    foreman's exact silent-bypass repro shape - a fully-authorized, real Form
    1098 statement on record that simply never asserts the now-mandatory
    ``tax.us.2025.f1098-scope.no-mortgage-statement`` pin at all.
    ``scope_flag_value`` controls the value asserted when
    ``assert_scope_flag`` is True (defaults to False, the ordinary/Path-B
    value for a return with a real statement on record); set True together
    with a real ``interest`` to build the repair-round-3 finding-1 repro - a
    self-contradictory declaration (flag says no statement; the family says
    otherwise).
    ``boundary_declarations`` overrides individual Schedule A boundary
    absence-declaration facts (default "yes" for every one of the seven
    categories); ``assert_boundary_declarations=False`` omits all seven
    entirely (repair round 3 finding 2's missing-declaration case).
    ``qbi_declaration``/``schedule1a_declaration`` similarly default "yes";
    ``assert_qbi_schedule1a_declarations=False`` omits both entirely.
    """
    acts = _ssa_acts(benefits=[], close=True, wages=wages)
    acts.pop()  # drop the SSA-1099 milestone's own trailing adoption

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(
            {
                "schema": "act.v1",
                "act_id": f"demo.f1098.t2.act.{len(acts):03d}",
                "kind": kind,
                "actor": USER,
                "at": f"2026-08-09T12:{len(acts) // 60:02d}:{len(acts) % 60:02d}Z",
                "committed_against": len(acts),
                "payload": payload,
            }
        )

    add("bundle-adoption", {"bundle": _load("f1098.bundle.json")})
    add("bundle-adoption", {"bundle": _load("f1098-scope.bundle.json")})
    add("bundle-adoption", {"bundle": _load("schedule-a-boundary.bundle.json")})
    add("bundle-adoption", {"bundle": _load("qbi-schedule1a-scope.bundle.json")})

    statements: list[tuple[str, str, float]] = []
    if interest is not None:
        statements.append(("demo.f1098.lender.a", "demo.f1098.stmt.a", interest))
    if second_statement_interest is not None:
        statements.append(("demo.f1098.lender.b", "demo.f1098.stmt.b", second_statement_interest))

    for payer, stmt, _ in statements:
        add(
            "entity-introduced",
            {"entity": {"schema": "entity.v1", "id": payer, "kind": "tax.us.mortgage-lender", "label": "Synthetic lender"}},
        )
        add(
            "entity-introduced",
            {"entity": {"schema": "entity.v1", "id": stmt, "kind": "tax.us.1098-statement", "label": "Synthetic Form 1098"}},
        )

    add("horizon-genesis", {"family": {"id": FAMILY_ID, "version": "v1"}, "scope": SCOPE_KEY, "horizon_id": "demo.f1098.h0"})
    horizon = "demo.f1098.h0"

    authority_values = {token: "yes" for token in AUTHORITY}
    if authority_overrides:
        authority_values.update(authority_overrides)

    for index, (payer, stmt, box1) in enumerate(statements):
        successor = f"demo.f1098.h{index + 1}"
        add(
            "member-transition",
            {
                "family": {"id": FAMILY_ID, "version": "v1"},
                "scope": SCOPE_KEY,
                "member": {
                    "action": "assert",
                    "finding": _attested(
                        f"demo.f1098.box1.{index}",
                        _member_fact_id("tax.us.2025.f1098.box1-mortgage-interest", payer, stmt),
                        box1,
                    ),
                },
                "successor": {"id": successor, "predecessor": horizon},
            },
        )
        horizon = successor

        companions: list[tuple[str, object]] = [
            ("tax.us.2025.f1098.box2-outstanding-principal", box2),
            ("tax.us.2025.f1098.box3-origination-date", box3),
            ("tax.us.2025.f1098.box4-overpaid-refund", box4),
            ("tax.us.2025.f1098.box5-mortgage-insurance", box5),
            ("tax.us.2025.f1098.box6-points", box6),
            ("tax.us.2025.f1098.box9-number-of-properties", box9),
            ("tax.us.2025.f1098.box11-other", box11),
        ]
        for fact_type, value in companions:
            short = fact_type.rsplit(".", 1)[-1]
            add(
                "assertion",
                {"finding": _attested(f"demo.f1098.{short}.{index}", _member_fact_id(fact_type, payer, stmt), value)},
            )
        for auth, value in authority_values.items():
            add(
                "assertion",
                {
                    "finding": _attested(
                        f"demo.f1098.{auth}.{index}",
                        _member_fact_id(f"tax.us.2025.f1098.{auth}", payer, stmt),
                        value,
                    )
                },
            )

    add(
        "assertion",
        {
            "finding": _attested(
                "demo.f1098.closure",
                f"tax.us.2025.f1098.source-closure|family-horizon={horizon},tax-year=2025",
                True,
            )
        },
    )

    # Track 2 review finding 1 repair round 2: this helper always closes the
    # tax.us.2025.f1098 family (even closed-empty, interest=None), so it must
    # always assert the flag false - rule.form1040-line12e.json's own value
    # branches on it, taking the derived-composition path only when it is
    # false. The flag is now a mandatory pin (no optional_default): a return
    # that never asserts it at all blocks DEPENDENCY_ABSENT rather than
    # silently defaulting to the legacy max(standard, itemized) path.
    if assert_scope_flag:
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.f1098.no-mortgage-statement-flag",
                    f"{NO_MORTGAGE_STATEMENT_FLAG}|tax-year=2025",
                    scope_flag_value,
                )
            },
        )

    if itemized_assertion is not None:
        add(
            "assertion",
            {"finding": _attested("demo.f1098.itemized-assertion", f"{ITEMIZED_ASSERTION}|tax-year=2025", itemized_assertion)},
        )

    # Repair round 3 finding 2: the seven Schedule A boundary categories and
    # the two QBI/Schedule-1-A categories are now mandatory taxpayer
    # declarations (never optional_default) - attachment.schedule-a.json's
    # completeness.required_answers blocks required-and-incomplete unless
    # every one of the seven is genuinely declared "yes", and rule.
    # form1040-line13a/13b.json each block DEPENDENCY_ABSENT unless their own
    # fact is asserted "yes".
    if assert_boundary_declarations:
        declared = dict.fromkeys(SCHEDULE_A_BOUNDARY_DECLARED_SYMBOLS, "yes")
        if boundary_declarations:
            declared.update(boundary_declarations)
        for symbol, value in declared.items():
            short = symbol.rsplit(".", 1)[-1]
            add(
                "assertion",
                {"finding": _attested(f"demo.{short}", f"{symbol}|tax-year=2025", value)},
            )

    if assert_qbi_schedule1a_declarations:
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.qbi-no-deduction-declared",
                    f"{QBI_NO_DEDUCTION_DECLARED}|tax-year=2025",
                    qbi_declaration,
                )
            },
        )
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.schedule1a-no-additional-deductions-declared",
                    f"{SCHEDULE1A_NO_ADDITIONAL_DEDUCTIONS_DECLARED}|tax-year=2025",
                    schedule1a_declaration,
                )
            },
        )

    adoption = _load_fixture_adoption()
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts


def _no_f1098_acts(*, wages: float = 90000) -> list[dict[str, object]]:
    """Track 2 review finding 1 repair round 2: a return that declares
    neither Path A (no-mortgage-statement) nor Path B (a real Form 1098
    statement) - no bundle adoption, no horizon-genesis, no closure
    assertion, no scope-flag assertion at all. Distinct from
    ``_f1098_acts(interest=None, ...)``, which still closes the family
    (closed-empty) and asserts the flag. This is the exact reproduction shape
    the independent review used against v29; under the now-mandatory scope
    pin it correctly blocks DEPENDENCY_ABSENT rather than silently
    defaulting to the legacy path."""
    acts = _ssa_acts(benefits=[], close=True, wages=wages)
    acts.pop()  # drop the SSA-1099 milestone's own trailing adoption
    adoption = _load_fixture_adoption()
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts


def _path_a_acts(*, wages: float = 90000) -> list[dict[str, object]]:
    """A return that explicitly declares Path A - no Form 1098 statement on
    record - by asserting ``tax.us.2025.f1098-scope.no-mortgage-statement =
    true``, without ever touching the tax.us.2025.f1098 bundle, horizon, or
    closure machinery at all. This is this corpus's normal "no-X" scope
    declaration convention (compare ss-benefits-scope, line2a-scope,
    schedule-a-boundary): a plain assertion, not a family-closure check, so
    it correctly avoids the original finding-1 defect (an unconditional
    require_closed on the f1098 family) while also avoiding round 1's
    silent-bypass defect (an optional_default flag whose absence quietly
    unlocked a bypass).

    Repair round 3 finding 1: round 2's "never touch the family at all"
    design is exactly what let a contradictory Path A declaration (flag
    true, real family on record) go unnoticed - the flag was trusted
    without ever consulting the observed world. The repair now checks the
    flag and ``count`` together, which requires the family to actually be
    closed (even closed-empty) to verify Path A is genuine - "no statement
    genuinely on record", not merely undeclared. This helper therefore
    routes through ``_f1098_acts`` with ``interest=None`` (closed-empty
    family) and ``scope_flag_value=True``, unchanged in externally-observed
    behavior (still just a plain flag + a closed-empty family, still never
    reaches ``tax.us.2025.schedule-a.line8a``) but no longer skips family
    closure outright."""
    return _f1098_acts(interest=None, wages=wages, assert_scope_flag=True, scope_flag_value=True)


def _run(acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    for index, act in enumerate(acts):
        act["committed_against"] = index
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
            raise AssertionError(result.refusal)
        assert result.output_path is not None and result.presentation_path is not None
        return (
            json.loads(result.output_path.read_text("utf-8")),
            json.loads(result.presentation_path.read_text("utf-8")),
        )


def _by_artifact(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["artifact_id"]: row for row in report.get("dispositions", [])}


def _attachment_status(model: dict[str, Any], attachment_id: str) -> dict[str, Any]:
    return next(a for a in model["attachments"] if a["id"] == attachment_id)


def _schedule_a_tie_out_value(model: dict[str, Any]) -> float:
    """Read the published Schedule A line-8a value from the attachment's own
    citation-group tie-out text (only present when the attachment publishes,
    i.e. required-and-complete)."""
    group = next(g for g in model["citationGroups"] if g["id"] == "tax.us.2025.rule.attachment.schedule-a")
    part = group["parts"][0]
    match = re.search(r"Reported subtotal: ([0-9.]+)", part["tieOutText"])
    assert match is not None, part["tieOutText"]
    return float(match.group(1))


ATTACHMENT_ID = "tax.us.2025.rule.attachment.schedule-a"
LINE8A_RULE = "tax.us.2025.schedule-a.line8a.rule"


class TestF1098Line12eTrack2(unittest.TestCase):
    def test_package_resolves_v29(self) -> None:
        acts = _f1098_acts(interest=20000.0)
        report, model = _run(acts, "demo.f1098.t2.resolve")
        self.assertEqual(_disposition(model, "line-12e"), "published_value")

    def test_deductible_interest_greater_than_standard_requires_schedule_a(self) -> None:
        acts = _f1098_acts(interest=20000.0)
        report, model = _run(acts, "demo.f1098.t2.greater")
        self.assertEqual(_disposition(model, "line-12e"), "published_value")
        self.assertEqual(_published_numeric(model, "line-12e"), 20000.0)
        status = _attachment_status(model, ATTACHMENT_ID)
        self.assertEqual(status["resolved"]["disposition"], "published")
        self.assertEqual(_schedule_a_tie_out_value(model), 20000.0)
        row = _by_artifact(report)[LINE8A_RULE]
        self.assertEqual(row["disposition"], "published")

    def test_deductible_interest_less_than_standard_no_schedule_a_required(self) -> None:
        acts = _f1098_acts(interest=5000.0)
        report, model = _run(acts, "demo.f1098.t2.less")
        self.assertEqual(_published_numeric(model, "line-12e"), STANDARD_DEDUCTION_SINGLE)
        status = _attachment_status(model, ATTACHMENT_ID)
        self.assertEqual(status["resolved"]["disposition"], "guard_inapplicable")

    def test_deductible_interest_equal_to_standard_ties_to_standard_not_required(self) -> None:
        acts = _f1098_acts(interest=STANDARD_DEDUCTION_SINGLE)
        report, model = _run(acts, "demo.f1098.t2.equal")
        self.assertEqual(_published_numeric(model, "line-12e"), STANDARD_DEDUCTION_SINGLE)
        status = _attachment_status(model, ATTACHMENT_ID)
        self.assertEqual(status["resolved"]["disposition"], "guard_inapplicable")

    def test_zero_interest_publishes_zero_schedule_a_not_required(self) -> None:
        acts = _f1098_acts(interest=0.0)
        report, model = _run(acts, "demo.f1098.t2.zero")
        self.assertEqual(_published_numeric(model, "line-12e"), STANDARD_DEDUCTION_SINGLE)
        status = _attachment_status(model, ATTACHMENT_ID)
        self.assertEqual(status["resolved"]["disposition"], "guard_inapplicable")
        row = _by_artifact(report)[LINE8A_RULE]
        self.assertEqual(row["disposition"], "published")

    def test_no_f1098_statement_uses_legacy_itemized_assertion(self) -> None:
        """count == 0: out of this milestone; the legacy raw-assertion path
        is unaffected and remains usable."""
        acts = _f1098_acts(interest=None, itemized_assertion=20000.0)
        report, model = _run(acts, "demo.f1098.t2.no-statement")
        self.assertEqual(_published_numeric(model, "line-12e"), 20000.0)
        status = _attachment_status(model, ATTACHMENT_ID)
        self.assertEqual(status["resolved"]["disposition"], "guard_inapplicable")

    def test_no_f1098_statement_below_standard_uses_standard(self) -> None:
        acts = _f1098_acts(interest=None, itemized_assertion=1000.0)
        report, model = _run(acts, "demo.f1098.t2.no-statement-below")
        self.assertEqual(_published_numeric(model, "line-12e"), STANDARD_DEDUCTION_SINGLE)

    def test_f1098_present_guards_off_the_generic_itemized_assertion(self) -> None:
        """The bounded guard (Track 0 Sec 6): once a Form 1098 statement is
        admitted, the raw tax.us.2025.deductions.itemized assertion is never
        consulted, even when it is asserted and would otherwise dominate."""
        acts = _f1098_acts(interest=5000.0, itemized_assertion=500000.0)
        report, model = _run(acts, "demo.f1098.t2.guard")
        # If the assertion could bypass the guard, line-12e would be 500000.
        self.assertEqual(_published_numeric(model, "line-12e"), STANDARD_DEDUCTION_SINGLE)

    def test_multiple_statements_block_out_of_scope(self) -> None:
        acts = _f1098_acts(interest=15000.0, second_statement_interest=5000.0)
        report, model = _run(acts, "demo.f1098.t2.multiple")
        row = _by_artifact(report)[LINE8A_RULE]
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "MULTIPLE_F1098_OUT_OF_SCOPE")
        self.assertEqual(_disposition(model, "line-12e"), "blocked")

    def test_line13a_line13b_closed_absent_never_silent_zero(self) -> None:
        acts = _f1098_acts(interest=20000.0)
        report, model = _run(acts, "demo.f1098.t2.line13")
        # computed_zero (not published_value) is the correct disposition for
        # an explicit, always-true, literal-0 closed-absent rule - it is a
        # distinct, walkable disposition in the form-field taxonomy, never
        # silence: the "never silent zero" claim is that a rule/citation
        # trail exists at all, not that the disposition label omits "zero".
        self.assertEqual(_disposition(model, "line-13a"), "computed_zero")
        self.assertEqual(_published_numeric(model, "line-13a"), 0)
        self.assertEqual(_disposition(model, "line-13b"), "computed_zero")
        self.assertEqual(_published_numeric(model, "line-13b"), 0)
        rows = _by_artifact(report)
        self.assertEqual(rows["tax.us.2025.rule.form1040-line13a"]["disposition"], "published")
        self.assertEqual(rows["tax.us.2025.rule.form1040-line13b"]["disposition"], "published")

    def test_line14_equals_line12e_plus_zero_plus_zero(self) -> None:
        acts = _f1098_acts(interest=20000.0)
        report, model = _run(acts, "demo.f1098.t2.line14")
        line12e = _published_numeric(model, "line-12e")
        self.assertEqual(_published_numeric(model, "line-1040-14"), line12e)

    def test_taxable_income_recomputes_exactly_from_line14(self) -> None:
        acts = _f1098_acts(interest=20000.0)
        report, model = _run(acts, "demo.f1098.t2.line15")
        agi = _published_numeric(model, "line-11")
        line14 = _published_numeric(model, "line-1040-14")
        self.assertEqual(_disposition(model, "line-15"), "published_value")
        self.assertEqual(_published_numeric(model, "line-15"), max(0.0, agi - line14))

    def test_downstream_recompute_below_standard(self) -> None:
        acts = _f1098_acts(interest=5000.0)
        report, model = _run(acts, "demo.f1098.t2.line15-below")
        agi = _published_numeric(model, "line-11")
        self.assertEqual(_published_numeric(model, "line-1040-14"), STANDARD_DEDUCTION_SINGLE)
        self.assertEqual(_published_numeric(model, "line-15"), max(0.0, agi - STANDARD_DEDUCTION_SINGLE))

    def test_corrected_statement_still_resolves_through_v29(self) -> None:
        """Same-identity correction collapses to count 1 (real v29 package,
        not the Track 1 resolver-patch fixture)."""
        acts = _f1098_acts(interest=15000.0)
        # Insert a correction assertion for the same statement identity right
        # before the closure/adoption tail.
        adoption = acts.pop()
        fact_id = _member_fact_id(
            "tax.us.2025.f1098.box1-mortgage-interest", "demo.f1098.lender.a", "demo.f1098.stmt.a"
        )
        acts.append(
            {
                "schema": "act.v1",
                "act_id": f"demo.f1098.t2.act.{len(acts):03d}",
                "kind": "assertion",
                "actor": USER,
                "at": "2026-08-09T13:00:00Z",
                "committed_against": len(acts),
                "payload": {
                    "finding": _attested("demo.f1098.box1.correction", fact_id, 18000.0)
                },
            }
        )
        adoption["committed_against"] = len(acts)
        acts.append(adoption)
        report, model = _run(acts, "demo.f1098.t2.correction")
        self.assertEqual(_published_numeric(model, "line-12e"), 18000.0)
        row = _by_artifact(report)[LINE8A_RULE]
        self.assertEqual(row["disposition"], "published")

    def test_line16_recomputes_exactly_from_line15(self) -> None:
        acts = _f1098_acts(interest=20000.0)
        report, model = _run(acts, "demo.f1098.t2.line16")
        self.assertEqual(_disposition(model, "line-16"), "published_value")
        line15 = _published_numeric(model, "line-15")
        self.assertGreater(float(line15), 0.0)
        # line-16 is a monotonic function of taxable income (line-15); this
        # exercises the real downstream tax computation the review's finding
        # 1 repro showed cascading into a hard block, not merely that line-15
        # itself is present.
        self.assertGreaterEqual(float(_published_numeric(model, "line-16")), 0.0)
        self.assertLess(float(_published_numeric(model, "line-16")), float(line15))

    def test_path_a_no_statement_declared_reaches_line15_and_line16(self) -> None:
        """Track 2 review finding 1 repair round 2's evidence case (a),
        updated for repair round 3 finding 1: a return that explicitly
        declares Path A - tax.us.2025.f1098-scope.no-mortgage-statement =
        true - over a genuinely closed-empty tax.us.2025.f1098 family (count
        0), still reaches a correct line-15/line-16, exactly as it did under
        v28 (the historical rule.form1040-line12 path: max(standard
        deduction, itemized) with itemized defaulting to 0 when unasserted).
        Round 2 originally built this case without ever touching the family
        at all; round 3 now requires the family to be closed (even
        closed-empty) so the flag and the observed count are verified
        together rather than the flag being trusted alone - see
        ``_path_a_acts``."""
        acts = _path_a_acts(wages=90000)
        report, model = _run(acts, "demo.f1098.t2.path-a")

        # rule.form1040-line12e is still the sole producer of line-12e; its
        # own value-level branch verified both the mandatory tax.us.2025.
        # f1098-scope.no-mortgage-statement pin and the closed-empty count
        # together, then took the legacy max(standard, itemized) path and
        # published.
        rows = _by_artifact(report)
        self.assertEqual(rows["tax.us.2025.rule.form1040-line12e"]["disposition"], "published")

        self.assertEqual(_disposition(model, "line-12e"), "published_value")
        self.assertEqual(_published_numeric(model, "line-12e"), STANDARD_DEDUCTION_SINGLE)
        self.assertEqual(_published_numeric(model, "line-1040-14"), STANDARD_DEDUCTION_SINGLE)

        agi = _published_numeric(model, "line-11")
        self.assertEqual(_disposition(model, "line-15"), "published_value")
        self.assertEqual(
            _published_numeric(model, "line-15"), max(0.0, float(agi) - STANDARD_DEDUCTION_SINGLE)
        )
        self.assertEqual(_disposition(model, "line-16"), "published_value")
        self.assertGreaterEqual(float(_published_numeric(model, "line-16")), 0.0)

    def test_neither_path_declared_blocks_line12e_and_cascade(self) -> None:
        """Track 2 review finding 1 repair round 2's evidence case (b): a
        return that asserts neither Path A nor Path B at all - no scope-flag
        assertion, no Form 1098 facts - correctly blocks line-12e (and the
        cascade to line-14/15/16) with DEPENDENCY_ABSENT. This is this
        corpus's normal, expected behavior for an unasserted completeness
        declaration (compare ss-benefits-scope, line2a-scope, schedule-a-
        boundary), not a defect to route around."""
        acts = _no_f1098_acts(wages=90000)
        report, model = _run(acts, "demo.f1098.t2.neither-path")

        rows = _by_artifact(report)
        line12e_row = rows["tax.us.2025.rule.form1040-line12e"]
        self.assertEqual(line12e_row["disposition"], "blocked")
        self.assertEqual(line12e_row["code"], "DEPENDENCY_ABSENT")
        self.assertIn(NO_MORTGAGE_STATEMENT_FLAG, line12e_row["missing"])

        self.assertEqual(_disposition(model, "line-12e"), "blocked")
        self.assertEqual(_disposition(model, "line-1040-14"), "blocked")
        self.assertEqual(_disposition(model, "line-15"), "blocked")
        self.assertEqual(_disposition(model, "line-16"), "blocked")

    def test_foreman_repro_real_f1098_without_scope_flag_blocks(self) -> None:
        """Named, permanent regression test for the foreman's exact
        silent-bypass reproduction (2026-08-09): a return with a
        fully-authorized, real Form 1098 statement on record (box 1
        interest $20,000, all seven Track 1 taxpayer-authority facts
        asserted yes, family closure asserted) and a bogus tax.us.2025.
        deductions.itemized assertion of $500,000, but the new mandatory
        tax.us.2025.f1098-scope.no-mortgage-statement pin never asserted at
        all. Round 1's optional_default/default-true design let this return
        silently publish the bogus $500,000 itemized figure, completely
        bypassing the derived Schedule A computation - the exact
        "unexplained contributed conclusion" bypass this milestone exists to
        prevent. Round 2 must block DEPENDENCY_ABSENT instead."""
        acts = _f1098_acts(interest=20000.0, itemized_assertion=500000.0, assert_scope_flag=False)
        report, model = _run(acts, "demo.f1098.t2.foreman-repro")

        rows = _by_artifact(report)
        line12e_row = rows["tax.us.2025.rule.form1040-line12e"]
        self.assertEqual(line12e_row["disposition"], "blocked")
        self.assertEqual(line12e_row["code"], "DEPENDENCY_ABSENT")
        self.assertIn(NO_MORTGAGE_STATEMENT_FLAG, line12e_row["missing"])

        # The bogus $500,000 figure must never surface as the published
        # line-12e value - the whole point of this regression test.
        self.assertEqual(_disposition(model, "line-12e"), "blocked")
        self.assertNotEqual(_published_numeric(model, "line-12e"), 500000.0)

    def test_foreman_repro_contradictory_scope_flag_blocks(self) -> None:
        """Named, permanent regression test for repair round 3 finding 1
        (both independent reviews, 2026-08-09): a return with a
        fully-authorized, real Form 1098 statement on record (box 1
        interest $40,000, all seven Track 1 taxpayer-authority facts
        asserted yes, family closure asserted) that *also* asserts
        ``tax.us.2025.f1098-scope.no-mortgage-statement = true`` - a
        self-contradictory declaration (the flag says no statement is on
        record; the family says otherwise). Before this repair, the outer
        guard on ``rule.form1040-line12e.json`` branched on the flag alone,
        so this published the raw, unverified $500,000 ``tax.us.2025.
        deductions.itemized`` assertion as line-12e while
        ``tax.us.2025.schedule-a.line8a.rule`` independently derived $40,000
        and Schedule A was marked required - internally contradictory, and
        nothing blocked. The repair checks the flag and the observed family
        together: asserting the flag true while the family is non-empty now
        blocks F1098_SCOPE_CONTRADICTION instead."""
        acts = _f1098_acts(
            interest=40000.0,
            itemized_assertion=500000.0,
            assert_scope_flag=True,
            scope_flag_value=True,
        )
        report, model = _run(acts, "demo.f1098.t2.scope-contradiction")

        rows = _by_artifact(report)
        line12e_row = rows["tax.us.2025.rule.form1040-line12e"]
        self.assertEqual(line12e_row["disposition"], "blocked")
        self.assertEqual(line12e_row["code"], "F1098_SCOPE_CONTRADICTION")

        self.assertEqual(_disposition(model, "line-12e"), "blocked")
        self.assertNotEqual(_published_numeric(model, "line-12e"), 500000.0)

        # The independently-derived Schedule A figure is unaffected - it
        # still derives $40,000 and Schedule A is still marked required;
        # the contradiction is caught at line-12e, not by silencing line8a.
        line8a_row = rows[LINE8A_RULE]
        self.assertEqual(line8a_row["disposition"], "published")

    def test_schedule_a_boundary_missing_declaration_blocks_attachment(self) -> None:
        """Repair round 3 finding 2: the seven Schedule A boundary rules
        previously published "absent" unconditionally, consuming no
        taxpayer declaration whatsoever. One category (no-charitable) left
        undeclared here must make the whole Schedule A attachment
        required-and-incomplete - never silently required-and-complete -
        even though the Form 1098 mortgage-interest figure itself is fully
        authorized and exceeds the standard deduction."""
        acts = _f1098_acts(interest=20000.0, boundary_declarations={}, assert_boundary_declarations=False)
        report, model = _run(acts, "demo.f1098.t2.boundary-missing")

        status = _attachment_status(model, ATTACHMENT_ID)
        self.assertEqual(status["resolved"]["disposition"], "blocked")

        rows = _by_artifact(report)
        attachment_row = rows[ATTACHMENT_ID]
        self.assertEqual(attachment_row["disposition"], "blocked")
        self.assertEqual(attachment_row["code"], "DEPENDENCY_ABSENT")
        for symbol in SCHEDULE_A_BOUNDARY_DECLARED_SYMBOLS:
            self.assertIn(symbol, attachment_row["missing"])

        # The individual boundary rule for the undeclared category blocks
        # too, exactly like every other now-mandatory declaration in this
        # corpus - never a silent "true".
        boundary_row = rows["tax.us.2025.rule.schedule-a-boundary-no-charitable"]
        self.assertEqual(boundary_row["disposition"], "blocked")
        self.assertEqual(boundary_row["code"], "DEPENDENCY_ABSENT")

    def test_schedule_a_boundary_declared_present_blocks_attachment(self) -> None:
        """A category declared present (real, unreported medical expenses -
        "no" rather than "yes") must never be silently excluded: the
        attachment's completeness.required_answers value-checks "yes"
        specifically, so a genuine "no" (a real category the milestone does
        not support deriving) also blocks required-and-incomplete, rather
        than passing merely because *something* was asserted."""
        acts = _f1098_acts(interest=20000.0, boundary_declarations={SCHEDULE_A_BOUNDARY_DECLARED_SYMBOLS[0]: "no"})
        report, model = _run(acts, "demo.f1098.t2.boundary-present")

        status = _attachment_status(model, ATTACHMENT_ID)
        self.assertEqual(status["resolved"]["disposition"], "blocked")
        rows = _by_artifact(report)
        attachment_row = rows[ATTACHMENT_ID]
        self.assertEqual(attachment_row["disposition"], "blocked")
        self.assertEqual(attachment_row["code"], "COMPLETENESS_VALUE_VIOLATION")

    def test_schedule_a_boundary_corrected_declaration_lifecycle(self) -> None:
        """A return that first declares a category present ("no") and later
        corrects it to absent ("yes") - a genuine lifecycle correction, not
        a bypass - reaches required-and-complete on the corrected value,
        exactly like this corpus's other free-supersession categorical
        facts (compare the Form 1098 box1 same-identity correction test)."""
        acts = _f1098_acts(interest=20000.0, boundary_declarations={SCHEDULE_A_BOUNDARY_DECLARED_SYMBOLS[0]: "no"})
        adoption = acts.pop()
        acts.append(
            {
                "schema": "act.v1",
                "act_id": f"demo.f1098.t2.act.{len(acts):03d}",
                "kind": "assertion",
                "actor": USER,
                "at": "2026-08-09T13:30:00Z",
                "committed_against": len(acts),
                "payload": {
                    "finding": _attested(
                        "demo.no-medical-declared.correction",
                        f"{SCHEDULE_A_BOUNDARY_DECLARED_SYMBOLS[0]}|tax-year=2025",
                        "yes",
                    )
                },
            }
        )
        adoption["committed_against"] = len(acts)
        acts.append(adoption)
        report, model = _run(acts, "demo.f1098.t2.boundary-corrected")

        status = _attachment_status(model, ATTACHMENT_ID)
        self.assertEqual(status["resolved"]["disposition"], "published")
        rows = _by_artifact(report)
        self.assertEqual(rows[ATTACHMENT_ID]["disposition"], "published")

    def test_qbi_schedule1a_missing_declaration_blocks_line13a_line13b(self) -> None:
        """Repair round 3 finding 2: rule.form1040-line13a/13b.json
        previously gated on mere presence of filing_status (true for every
        return in existence). Omitting the new QBI/Schedule-1-A absence
        declarations must block DEPENDENCY_ABSENT, not silently publish
        zero."""
        acts = _f1098_acts(interest=20000.0, assert_qbi_schedule1a_declarations=False)
        report, model = _run(acts, "demo.f1098.t2.qbi-missing")

        rows = _by_artifact(report)
        line13a_row = rows["tax.us.2025.rule.form1040-line13a"]
        self.assertEqual(line13a_row["disposition"], "blocked")
        self.assertEqual(line13a_row["code"], "DEPENDENCY_ABSENT")
        self.assertIn(QBI_NO_DEDUCTION_DECLARED, line13a_row["missing"])

        line13b_row = rows["tax.us.2025.rule.form1040-line13b"]
        self.assertEqual(line13b_row["disposition"], "blocked")
        self.assertEqual(line13b_row["code"], "DEPENDENCY_ABSENT")
        self.assertIn(SCHEDULE1A_NO_ADDITIONAL_DEDUCTIONS_DECLARED, line13b_row["missing"])

        self.assertEqual(_disposition(model, "line-13a"), "blocked")
        self.assertEqual(_disposition(model, "line-13b"), "blocked")

    def test_citations_explanations_and_presentation(self) -> None:
        """Track 2 review finding 5, following
        ``tests/test_ssa1099_benefits_line6_track2.py``'s
        ``test_citations_explanations_and_presentation`` as the pattern."""
        acts = _f1098_acts(interest=20000.0)
        report, model = _run(acts, "demo.f1098.t2.citations")
        section_ids = {s["id"] for s in model["sections"]}
        for sid in ("line-12e", "line-1040-14", "line-15", "line-16"):
            self.assertIn(sid, section_ids)
        self.assertEqual(_disposition(model, "line-12e"), "published_value")

        # Citation pins on rules.
        for name, cites in (
            ("rule.form1040-line12e.json", ("tax.us.2025.citation.form1040.line-12e",)),
            ("rule.form1040-line14.json", ("tax.us.2025.citation.form1040.line-14",)),
            ("rule.form1040-line15.v2.json", ("tax.us.2025.citation.form1040.line-15",)),
            ("attachment.schedule-a.json", ("tax.us.2025.citation.attachment.schedule-a",)),
        ):
            blob = json.dumps(_load(name))
            for cite in cites:
                self.assertIn(cite, blob)

        # Walkable explanation pins present on the published line-12e
        # disposition.
        line12e_item = _report_item(report, "tax.us.2025.deductions.line-12e")
        self.assertTrue(line12e_item.get("pins") or line12e_item.get("finding_id"))
        self.assertIn("tax.us.2025.rule.form1040-line12e", json.dumps(line12e_item))

        # The Schedule A attachment is present and walkable when required.
        status = _attachment_status(model, ATTACHMENT_ID)
        self.assertEqual(status["resolved"]["disposition"], "published")

    def test_package_and_registry_integrity(self) -> None:
        """Track 2 review finding 5: schema-registry / published-packages
        integrity, not merely loading v24 as a presentation surface."""
        v29 = _load("package.core-calculations.v29.json")
        result = validate_package(
            v29,
            _corpus(),
            DerivationSchemas(),
            load_published_citizen_checksums(CONTENT / "published-packages.v24.json"),
        )
        self.assertTrue(result.ok, result.issues)

        registry = _load("published-packages.v24.json")
        citizens = {(c["id"], c["version"]): c["checksum"] for c in registry["citizens"]}
        for member in v29["members"]:
            self.assertIn((member["id"], member["version"]), citizens)
        packages = {(p["id"], p["version"]) for p in registry["packages"]}
        self.assertIn((v29["id"], v29["version"]), packages)

        # Finding 1 repair round 2's new member (the scope-flag bundle) is
        # present and reachable; tax.us.2025.deductions.line-12e stays
        # single-producer (no conflict_semantics entry). Round 1's
        # optional_default default parameter (tax.us.2025.parameter.
        # default-true) is gone: the scope flag is now a mandatory pin, so
        # it needs no package-level input_bindings entry at all - exactly
        # like this corpus's other "no-X" scope-declaration tokens.
        member_ids = {m["id"] for m in v29["members"]}
        self.assertIn("tax.us.2025.f1098-scope.vocabulary", member_ids)
        self.assertNotIn("tax.us.2025.parameter.default-true", member_ids)
        input_binding_symbols = {b["symbol"] for b in v29.get("input_bindings", [])}
        self.assertNotIn("tax.us.2025.f1098-scope.no-mortgage-statement", input_binding_symbols)
        conflict_symbols = {c["symbol"] for c in v29.get("conflict_semantics", [])}
        self.assertNotIn("tax.us.2025.deductions.line-12e", conflict_symbols)

    def test_v22_exact_entrypoints_hard_refuse_stale_and_dangling_mutations(self) -> None:
        """Repair round 3 finding 3: the exact-entrypoint check
        (ENTRYPOINT_VERSION_MISMATCH/ENTRYPOINT_DANGLING) was gated to
        ``package.get("schema") in {"artifact-package.v20",
        "artifact-package.v21"}`` - artifact-package.v22 (this milestone's
        own additive successor, admitted by package.core-calculations.v29)
        was missing from that set, so a stale or dangling entrypoint in a
        v29-schema package passed validation silently. Mirrors
        ``test_ssa1099_benefits_line6_track2.
        test_v21_exact_entrypoints_hard_refuse_authenticated_mutations``,
        but calls ``validate_package`` directly (no resolver/surface
        plumbing needed) since the defect and its repair are entirely
        inside that one function."""
        v29 = _load("package.core-calculations.v29.json")
        self.assertEqual(v29["schema"], "artifact-package.v22")
        corpus = _corpus()
        schemas = DerivationSchemas()
        checksums = load_published_citizen_checksums(CONTENT / "published-packages.v24.json")

        for mutation in ("stale", "dangling"):
            with self.subTest(mutation=mutation):
                mutated = json.loads(json.dumps(v29))
                if mutation == "stale":
                    for entry in mutated["entrypoints"]:
                        if entry["id"] == "tax.us.2025.rule.form1040-line12e":
                            entry["version"] = "v0"
                            break
                    else:
                        raise AssertionError("line-12e entrypoint not found")
                else:
                    mutated["entrypoints"].append(
                        {"id": "tax.us.2025.rule.nonexistent-entrypoint", "version": "v1"}
                    )
                result = validate_package(mutated, corpus, schemas, checksums)
                self.assertFalse(result.ok, result.issues)
                expected = "ENTRYPOINT_VERSION_MISMATCH" if mutation == "stale" else "ENTRYPOINT_DANGLING"
                self.assertIn(expected, {issue.code for issue in result.issues})


if __name__ == "__main__":
    unittest.main()
