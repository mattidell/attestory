"""Track 4: Schedule 1 line-26 composition and attachment succession.

Exercises ``tax.us.2025.rule.schedule1-line26`` (publishing
``tax.us.2025.schedule1.line26-total-adjustments``) and
``tax.us.2025.rule.attachment.schedule-1`` version ``v2`` (schema
unchanged at ``attachment-rule.v4`` -- Track 0 T0-7's settlement that "the
existing attachment-rule.v4 grammar already expresses everything this
route needs" is confirmed directly against
``packages/schemas/tax/attachment-rule.v4.schema.json``: ``requirement.
subtotals`` and ``itemizations`` are already arrays, so no new schema
shape / no ``attachment-rule.v9`` file is written -- see that rule's own
``title`` field for the reconciliation note), directly through the
saturation runner's own ``RunContext``/``run`` entry point, mirroring
Track 3's lightweight non-kernel harness idiom
(``tests/test_sli_worksheet_line21_track3.py``).

See ``docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md``
T0-6 (line-26 completeness) and T0-7 (attachment disposition) for the
settled design this test proves.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any, cast

from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.runner import InputFinding, RunContext, SourceFact, run
from packages.derivation.source_authority import ClosureFindingRecord

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"

# -- Form 1098-E (SLI) fixtures, mirroring Track 3 exactly --------------
SLI_RULE_FILE = "rule.sli-worksheet.json"
SLI_SUBTOTAL_RULE_FILE = "rule.sli-worksheet-line1-subtotal.json"
F1098E_FAMILY_FILE = "family.f1098e-1.json"
F1098E_FAMILY = "tax.us.2025.f1098e.1"
F1098E_BOX1 = "tax.us.2025.f1098e.box1-student-loan-interest"
F1098E_CLOSURE_TYPE = "tax.us.2025.f1098e.1.source-closure"
LINE21 = "tax.us.2025.schedule1.line21-sli-deduction"
LINE1_SUBTOTAL = "tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal"

UNIVERSAL_FILER = [
    "tax.us.2025.sli-scope.no-form-2555",
    "tax.us.2025.sli-scope.no-form-4563",
    "tax.us.2025.sli-scope.no-puerto-rico-or-samoa-income",
]
UNIVERSAL_STATEMENT = [
    "tax.us.2025.f1098e.no-related-person-interest",
    "tax.us.2025.f1098e.no-qualified-employer-plan-interest",
    "tax.us.2025.f1098e.no-non-qualified-loan-component",
    "tax.us.2025.f1098e.no-employer-educational-assistance-interest",
    "tax.us.2025.f1098e.no-qtp-earnings-used",
]
SCHED1_ABSENCE_TOKENS = [
    "11-educator", "12-business-expenses", "13-hsa", "14-moving",
    "15-deductible-se", "16-se-retirement", "17-se-health", "18-penalty",
    "19-alimony-paid", "20-ira-deduction", "23-archer-msa", "25-other-adjustments",
]
SCHED1_ABSENCES = [
    f"tax.us.2025.schedule1-adjustments-scope.no-line{tok}" for tok in SCHED1_ABSENCE_TOKENS
]
LEGAL_ZERO = [
    "tax.us.2025.sli-scope.not-claimed-as-dependent",
    "tax.us.2025.sli-scope.legally-obligated-for-interest",
]
ALL_CONDITIONAL = UNIVERSAL_FILER + UNIVERSAL_STATEMENT + SCHED1_ABSENCES + LEGAL_ZERO
assert len(ALL_CONDITIONAL) == 22

# -- Form 1099-G (unemployment) fixtures ---------------------------------
UG_SUBTOTAL_RULE_FILE = "rule.f1099g-1-subtotal.json"
F1099G_FAMILY_FILE = "family.f1099g-1.json"
F1099G_FAMILY = "tax.us.2025.f1099g.1"
F1099G_BOX1 = "tax.us.2025.f1099g.box1-unemployment"
F1099G_CLOSURE_TYPE = "tax.us.2025.f1099g.1.source-closure"
UG_SUBTOTAL = "tax.us.2025.unemployment.box1-subtotal"

SCOPE_TOKENS = (
    "no-sch1-line1-taxable-refunds",
    "no-sch1-line2a-alimony",
    "no-sch1-line3-business",
    "no-sch1-line4-other-gains",
    "no-sch1-line5-rental",
    "no-sch1-line6-farm",
    "no-sch1-other-income",
    "no-unemployment-repayment",
    "no-f1099g-box2-state-refund",
    "no-f1099g-other-payment-classes",
)
SCOPE_IDS = [f"tax.us.2025.schedule1-part1-scope.{tok}" for tok in SCOPE_TOKENS]

# -- Line 26 / attachment citizens ---------------------------------------
LINE26_RULE_FILE = "rule.schedule1-line26.json"
LINE26 = "tax.us.2025.schedule1.line26-total-adjustments"
ATTACHMENT_V2_FILE = "rule.attachment.schedule-1.v2.json"
ATTACHMENT_ID = "tax.us.2025.rule.attachment.schedule-1"

ADOPTION_PIN = {"role": "adoption", "id": "demo.package.schedule1-line26.2025", "version": "v1"}
GOV_PINS = [{"role": "governance", "id": "governance.constitution", "version": "v1"}]


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))


def _f1098e_closure(*, closed: bool) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[ClosureFindingRecord], dict[str, str]]:
    family = _load(F1098E_FAMILY_FILE)
    mapping = {
        "schema": "source-closure-mapping.v1",
        "id": "tax.us.2025.mapping.f1098e.1",
        "version": "v1",
        "family": {"id": family["id"], "version": family["version"]},
        "member_fact_type": F1098E_BOX1,
        "closure_fact_type": F1098E_CLOSURE_TYPE,
        "closure_horizon_key": "family-horizon",
        "admits_symbol": family["authorizes_subtotal"],
        "admission": {"condition": "current-literal-true"},
    }
    findings = (
        [ClosureFindingRecord("f.sch1.closure.f1098e", F1098E_CLOSURE_TYPE, "h0", True)] if closed else []
    )
    return [family], [mapping], findings, {F1098E_FAMILY: "h0"}


def _f1099g_closure(*, closed: bool) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[ClosureFindingRecord], dict[str, str]]:
    family = _load(F1099G_FAMILY_FILE)
    mapping = {
        "schema": "source-closure-mapping.v1",
        "id": "tax.us.2025.mapping.f1099g.1",
        "version": "v1",
        "family": {"id": family["id"], "version": family["version"]},
        "member_fact_type": F1099G_BOX1,
        "closure_fact_type": F1099G_CLOSURE_TYPE,
        "closure_horizon_key": "family-horizon",
        "admits_symbol": family["authorizes_subtotal"],
        "admission": {"condition": "current-literal-true"},
    }
    findings = (
        [ClosureFindingRecord("f.sch1.closure.f1099g", F1099G_CLOSURE_TYPE, "g0", True)] if closed else []
    )
    return [family], [mapping], findings, {F1099G_FAMILY: "g0"}


def _merge_closures(*parts: tuple[list[Any], list[Any], list[Any], dict[str, str]]) -> dict[str, Any]:
    families: list[Any] = []
    mappings: list[Any] = []
    findings: list[Any] = []
    horizons: dict[str, str] = {}
    for fam, maps, finds, hz in parts:
        families.extend(fam)
        mappings.extend(maps)
        findings.extend(finds)
        horizons.update(hz)
    return {
        "family_declarations": families,
        "closure_mappings": mappings,
        "closure_findings": findings,
        "current_horizons": horizons,
    }


def _yes_inputs(components: list[str], *, offset: int = 0, answers: dict[str, str] | None = None) -> list[InputFinding]:
    answers = answers or {}
    findings = []
    for i, component in enumerate(components):
        value = answers.get(component, "yes")
        findings.append(InputFinding(component, value, f"f.sch1.component.{offset + i}", "input"))
    return findings


def _split_witness_inputs(inputs: list[InputFinding]) -> tuple[list[InputFinding], list[SourceFact]]:
    """Route the five per-statement universal witnesses to ``sources``.

    Track 6b repair: ``rule.sli-worksheet.json`` now reads these five
    (``UNIVERSAL_STATEMENT``) via the new ``collect_categorical_all_equal``
    op over ``env.sources``, never a single unkeyed ``ref`` over
    ``env.symbols`` (mirrors ``tests/test_sli_worksheet_line21_track3.py``'s
    own helper of the same name -- see that file for the full rationale).
    This harness still builds every test scenario the same way it always
    has, via ``InputFinding`` lists keyed by component id; this helper is
    the one place that translates a witness ``InputFinding`` into the
    ``SourceFact`` the rule now actually reads, so every existing call
    site and test method is unchanged and computed dollar values stay
    byte-identical for every single-statement input.
    """
    kept: list[InputFinding] = []
    witness_sources: list[SourceFact] = []
    for finding in inputs:
        if finding.symbol in UNIVERSAL_STATEMENT:
            fact_id = (
                f"{finding.symbol}|lender=demo.sch1.lender.0,"
                f"statement=demo.sch1.stmt.0,tax-year=2025"
            )
            witness_sources.append(
                SourceFact(
                    name=finding.symbol,
                    value=finding.value,
                    finding_id=finding.finding_id,
                    fact_id=fact_id,
                )
            )
        else:
            kept.append(finding)
    return kept, witness_sources


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.canon = load_canon(self.schemas)
        self.sli_rule = _load(SLI_RULE_FILE)
        self.sli_subtotal_rule = _load(SLI_SUBTOTAL_RULE_FILE)
        self.ug_subtotal_rule = _load(UG_SUBTOTAL_RULE_FILE)
        self.line26_rule = _load(LINE26_RULE_FILE)
        self.attachment_rule = _load(ATTACHMENT_V2_FILE)
        for rule in (
            self.sli_rule,
            self.sli_subtotal_rule,
            self.ug_subtotal_rule,
            self.line26_rule,
        ):
            self.schemas.validate_declared(rule)
        self.parameters = {
            p["id"]: p
            for p in [
                _load("parameter.sli-interest-cap.json"),
                _load("parameter.sli-magi-threshold.json"),
                _load("parameter.sli-magi-phase-range.json"),
                _load("parameter.default-zero.json"),
            ]
        }

    def base_inputs(self, *, filing_status: str = "single", total_income: str = "50000") -> list[InputFinding]:
        return [
            InputFinding("rounding.convention", "half_up", "f.sch1.rounding", "input"),
            InputFinding("filing_status", filing_status, "f.sch1.filing", "choice"),
            InputFinding("tax.us.2025.income.total-income", total_income, "f.sch1.income", "input"),
        ]

    def input_bindings(self) -> list[dict[str, Any]]:
        return [
            {
                "symbol": "filing_status",
                "fact_type": {"id": "tax.us.2025.filing-status", "version": "v1"},
                "mode": "required",
            }
        ]

    def sli_box1_source(self, amount: str, *, index: int = 0) -> SourceFact:
        fact_id = f"{F1098E_BOX1}|lender=demo.sch1.lender.{index},statement=demo.sch1.stmt.{index},tax-year=2025"
        return SourceFact(name=F1098E_BOX1, value=amount, finding_id=f"f.sch1.box1.{index}", fact_id=fact_id)

    def ug_box1_source(self, amount: str, *, index: int = 0) -> SourceFact:
        fact_id = f"{F1099G_BOX1}|payer=demo.sch1.payer.{index},statement=demo.sch1.ug-stmt.{index},tax-year=2025"
        return SourceFact(name=F1099G_BOX1, value=amount, finding_id=f"f.sch1.ug.box1.{index}", fact_id=fact_id)

    def published(self, result: Any, symbol: str) -> str | None:
        for pub in result.publications:
            if pub.finding["symbol"] == symbol:
                return cast(str, pub.finding["value"])
        return None

    def blocked_entry(self, result: Any, artifact_id: str) -> dict[str, Any] | None:
        for entry in result.blocked:
            if entry["artifact_id"] == artifact_id:
                return cast(dict[str, Any], entry)
        return None

    def disposition_entry(self, result: Any, artifact_id: str) -> dict[str, Any] | None:
        for entry in result.dispositions:
            if entry["artifact_id"] == artifact_id:
                return cast(dict[str, Any], entry)
        return None


class Line26CompositionCases(Fixture):
    """(d): line 26 sums correctly; (e): line 26 propagates line 21's block."""

    def _context(self, *, sources: list[SourceFact], inputs: list[InputFinding], closures: dict[str, Any]) -> RunContext:
        kept_inputs, witness_sources = _split_witness_inputs(inputs)
        return RunContext(
            run_id="run.sch1.line26",
            rules=[self.sli_rule, self.sli_subtotal_rule, self.line26_rule],
            parameters=self.parameters,
            canon=self.canon,
            inputs=kept_inputs,
            sources=sources + witness_sources,
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOV_PINS,
            input_bindings=self.input_bindings(),
            **closures,
        )

    def test_line26_sums_to_line21_when_all_twelve_absences_yes(self) -> None:
        # box1 = 1000 (under cap), income 50000 <= 85000 single threshold ->
        # no phaseout -> line21 = 1000. All twelve Schedule-1-native
        # absences "yes" -> line 26 must equal line 21 exactly (T0-6:
        # lines 11-20/23/25 each contribute $0, line 22 is structural $0).
        ctx = self._context(
            sources=[self.sli_box1_source("1000")],
            inputs=self.base_inputs(total_income="50000") + _yes_inputs(ALL_CONDITIONAL),
            closures=_merge_closures(_f1098e_closure(closed=True)),
        )
        result = run(ctx, self.schemas)
        self.assertIsNone(self.blocked_entry(result, self.sli_rule["id"]))
        self.assertEqual(self.published(result, LINE21), "1000")
        self.assertIsNone(self.blocked_entry(result, self.line26_rule["id"]))
        self.assertEqual(self.published(result, LINE26), "1000")

    def test_line26_sums_to_line21_in_phaseout_band(self) -> None:
        # Reuses Track 3's phaseout-band arithmetic (box1=2000, income=90000,
        # single) -> line21 = 1334; line 26 must track it exactly.
        ctx = self._context(
            sources=[self.sli_box1_source("2000")],
            inputs=self.base_inputs(total_income="90000") + _yes_inputs(ALL_CONDITIONAL),
            closures=_merge_closures(_f1098e_closure(closed=True)),
        )
        result = run(ctx, self.schemas)
        self.assertEqual(self.published(result, LINE21), "1334")
        self.assertEqual(self.published(result, LINE26), "1334")

    def test_line26_zero_when_no_f1098e_activity(self) -> None:
        # Closed-empty family: line21 computes 0 without evaluating any of
        # the twelve absences via the SLI worksheet's own count==0
        # shortcut, but line 26 still independently requires and checks
        # them (T0-6: line-26 completeness is not optional).
        ctx = self._context(
            sources=[],
            inputs=self.base_inputs(total_income="50000") + _yes_inputs(SCHED1_ABSENCES),
            closures=_merge_closures(_f1098e_closure(closed=True)),
        )
        result = run(ctx, self.schemas)
        self.assertEqual(self.published(result, LINE21), "0")
        self.assertEqual(self.published(result, LINE26), "0")

    def test_line26_blocks_when_line21_blocks_mfs(self) -> None:
        ctx = self._context(
            sources=[self.sli_box1_source("1000")],
            inputs=self.base_inputs(filing_status="married_filing_separately", total_income="50000")
            + _yes_inputs(ALL_CONDITIONAL),
            closures=_merge_closures(_f1098e_closure(closed=True)),
        )
        result = run(ctx, self.schemas)
        blocked21 = self.blocked_entry(result, self.sli_rule["id"])
        self.assertIsNotNone(blocked21)
        assert blocked21 is not None
        self.assertEqual(blocked21["code"], "SLI_MFS_INELIGIBLE")
        self.assertIsNone(self.published(result, LINE21))
        # Line 26's own ref to line 21 raises DEPENDENCY_ABSENT the moment
        # it is evaluated -- no special-casing needed for propagation.
        blocked26 = self.blocked_entry(result, self.line26_rule["id"])
        self.assertIsNotNone(blocked26)
        assert blocked26 is not None
        self.assertEqual(blocked26["code"], "DEPENDENCY_ABSENT")
        self.assertIn(LINE21, blocked26["missing"])
        self.assertIsNone(self.published(result, LINE26))

    def test_line26_blocks_when_line21_blocks_universal_component(self) -> None:
        answers = {"tax.us.2025.f1098e.no-related-person-interest": "no"}
        ctx = self._context(
            sources=[self.sli_box1_source("1000")],
            inputs=self.base_inputs(total_income="50000") + _yes_inputs(ALL_CONDITIONAL, answers=answers),
            closures=_merge_closures(_f1098e_closure(closed=True)),
        )
        result = run(ctx, self.schemas)
        blocked21 = self.blocked_entry(result, self.sli_rule["id"])
        assert blocked21 is not None
        self.assertEqual(blocked21["code"], "SLI_UNIVERSAL_COMPONENT_VIOLATION")
        blocked26 = self.blocked_entry(result, self.line26_rule["id"])
        self.assertIsNotNone(blocked26)
        assert blocked26 is not None
        self.assertEqual(blocked26["code"], "DEPENDENCY_ABSENT")
        self.assertIsNone(self.published(result, LINE26))

    def test_line26_inapplicable_when_a_schedule1_absence_is_no(self) -> None:
        # A "no" on one of the twelve Part II absences means this return has
        # an adjustment line 26 cannot honestly compute -- guard_inapplicable
        # (all-conjunction when clause), not a silent zero.
        answers = {"tax.us.2025.schedule1-adjustments-scope.no-line13-hsa": "no"}
        ctx = self._context(
            sources=[],
            inputs=self.base_inputs(total_income="50000") + _yes_inputs(SCHED1_ABSENCES, answers=answers),
            closures=_merge_closures(_f1098e_closure(closed=True)),
        )
        result = run(ctx, self.schemas)
        self.assertEqual(self.published(result, LINE21), "0")
        self.assertIsNone(self.published(result, LINE26))
        self.assertIsNone(self.blocked_entry(result, self.line26_rule["id"]))
        disp = self.disposition_entry(result, self.line26_rule["id"])
        self.assertIsNotNone(disp)
        assert disp is not None
        self.assertEqual(disp.get("guard_result"), False)


class AttachmentTriggerCases(Fixture):
    """(a) Part I only regression, (b) Part II only newly triggers, (c) neither."""

    def _context(
        self,
        *,
        sli_sources: list[SourceFact],
        ug_sources: list[SourceFact],
        sli_answers: list[InputFinding],
        scope_answers: list[InputFinding],
        total_income: str,
        f1098e_closed: bool,
        f1099g_closed: bool,
    ) -> RunContext:
        closures = _merge_closures(
            _f1098e_closure(closed=f1098e_closed),
            _f1099g_closure(closed=f1099g_closed),
        )
        kept_inputs, witness_sources = _split_witness_inputs(
            self.base_inputs(total_income=total_income) + sli_answers + scope_answers
        )
        return RunContext(
            run_id="run.sch1.attachment",
            rules=[
                self.sli_rule,
                self.sli_subtotal_rule,
                self.ug_subtotal_rule,
                self.attachment_rule,
            ],
            parameters=self.parameters,
            canon=self.canon,
            inputs=kept_inputs,
            sources=sli_sources + ug_sources + witness_sources,
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOV_PINS,
            input_bindings=self.input_bindings(),
            **closures,
        )

    def test_a_part1_unemployment_only_still_triggers(self) -> None:
        ctx = self._context(
            sli_sources=[],
            ug_sources=[self.ug_box1_source("500")],
            sli_answers=[],
            scope_answers=_yes_inputs(SCOPE_IDS),
            total_income="50000",
            f1098e_closed=True,
            f1099g_closed=True,
        )
        result = run(ctx, self.schemas)
        self.assertEqual(self.published(result, UG_SUBTOTAL), "500")
        self.assertEqual(self.published(result, LINE21), "0")
        disp = self.disposition_entry(result, ATTACHMENT_ID)
        self.assertIsNotNone(disp)
        assert disp is not None
        self.assertEqual(disp["disposition"], "published")

    def test_b_part2_sli_only_now_triggers(self) -> None:
        # Under the $2,500 cap so the itemization row-level tie-out holds
        # (documented limitation: see rule.attachment.schedule-1.v2.json's
        # title for the over-cap case, proven separately below).
        ctx = self._context(
            sli_sources=[self.sli_box1_source("1000")],
            ug_sources=[],
            sli_answers=_yes_inputs(ALL_CONDITIONAL),
            scope_answers=_yes_inputs(SCOPE_IDS),
            total_income="50000",
            f1098e_closed=True,
            f1099g_closed=True,
        )
        result = run(ctx, self.schemas)
        self.assertEqual(self.published(result, UG_SUBTOTAL), "0")
        self.assertEqual(self.published(result, LINE21), "1000")
        disp = self.disposition_entry(result, ATTACHMENT_ID)
        self.assertIsNotNone(disp)
        assert disp is not None
        self.assertEqual(disp["disposition"], "published")

    def test_c_neither_triggers_nothing(self) -> None:
        ctx = self._context(
            sli_sources=[],
            ug_sources=[],
            sli_answers=[],
            scope_answers=[],
            total_income="50000",
            f1098e_closed=True,
            f1099g_closed=True,
        )
        result = run(ctx, self.schemas)
        self.assertEqual(self.published(result, UG_SUBTOTAL), "0")
        self.assertEqual(self.published(result, LINE21), "0")
        disp = self.disposition_entry(result, ATTACHMENT_ID)
        self.assertIsNotNone(disp)
        assert disp is not None
        self.assertEqual(disp["disposition"], "inapplicable")
        self.assertEqual(disp.get("guard_result"), False)

    def test_itemization_ties_out_at_the_cap_boundary(self) -> None:
        ctx = self._context(
            sli_sources=[self.sli_box1_source("2500")],
            ug_sources=[],
            sli_answers=_yes_inputs(ALL_CONDITIONAL),
            scope_answers=_yes_inputs(SCOPE_IDS),
            total_income="50000",
            f1098e_closed=True,
            f1099g_closed=True,
        )
        result = run(ctx, self.schemas)
        self.assertEqual(self.published(result, LINE1_SUBTOTAL), "2500")
        disp = self.disposition_entry(result, ATTACHMENT_ID)
        self.assertIsNotNone(disp)
        assert disp is not None
        self.assertEqual(disp["disposition"], "published")

    def test_over_cap_filer_itemization_no_longer_false_blocks(self) -> None:
        # Track 4b repair, proven not assumed: a filer with total box-1
        # interest over the $2,500 cap used to trip the runner's generic
        # itemization tie-out check, because the row_set subtotal was the
        # $2,500-capped worksheet figure while the raw member row-sum was
        # the true (higher) total. After Track 4b, the closure-authorized
        # subtotal (tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal)
        # is the RAW, uncapped sum -- so it now equals the itemization's raw
        # row-level sum by construction, and the $2,500 cap is applied only
        # inside the worksheet's own line-21 deduction arithmetic. The
        # attachment must now succeed, with line 21 still correctly capped
        # and phased out.
        ctx = self._context(
            sli_sources=[self.sli_box1_source("3000")],
            ug_sources=[],
            sli_answers=_yes_inputs(ALL_CONDITIONAL),
            scope_answers=_yes_inputs(SCOPE_IDS),
            total_income="50000",
            f1098e_closed=True,
            f1099g_closed=True,
        )
        result = run(ctx, self.schemas)
        # The closure-authorized subtotal is now the raw $3,000 sum, not the
        # capped $2,500 figure -- ties out exactly to the raw member row-sum.
        self.assertEqual(self.published(result, LINE1_SUBTOTAL), "3000")
        # Line 21 itself is unaffected: still capped at $2,500 and (at this
        # income/filing status, below the phaseout floor) not phased out.
        self.assertEqual(self.published(result, LINE21), "2500")
        self.assertIsNone(self.blocked_entry(result, ATTACHMENT_ID))
        disp = self.disposition_entry(result, ATTACHMENT_ID)
        self.assertIsNotNone(disp)
        assert disp is not None
        self.assertEqual(disp["disposition"], "published")


if __name__ == "__main__":
    unittest.main()
