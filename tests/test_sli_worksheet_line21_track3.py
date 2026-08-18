"""Track 3: the Student Loan Interest Deduction Worksheet rule citizen.

Exercises ``tax.us.2025.rule.sli-worksheet`` (rule-artifact.v6, publishing
``tax.us.2025.schedule1.line21-sli-deduction``) directly through the saturation
runner's own ``RunContext``/``run`` entry point (``packages.derivation.runner``),
the same lightweight, non-kernel harness ``tests/derivation/test_runner.py``
uses -- mirroring Track 2's fact/projection-level idiom one layer up, at the
rule-evaluation layer, since this track's job is proving the worksheet's own
arithmetic (particularly that ``multiply``/``divide`` compose correctly
through a real MAGI phaseout), not the full kernel act-log/live_coordinate_run
production surface Track 6 is chartered to build.

See ``docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md``
T0-4 (worksheet), T0-9 (substrate sequencing) for the settled design this
rule implements.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any, cast

from packages.derivation.evaluator import BLOCK_ABSENT, BLOCK_CLOSURE
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.runner import InputFinding, RunContext, SourceFact, run
from packages.derivation.source_authority import ClosureFindingRecord

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"

RULE_FILE = "rule.sli-worksheet.json"
SUBTOTAL_RULE_FILE = "rule.sli-worksheet-line1-subtotal.json"
FAMILY_FILE = "family.f1098e-1.json"

FAMILY = "tax.us.2025.f1098e.1"
BOX1 = "tax.us.2025.f1098e.box1-student-loan-interest"
CLOSURE_TYPE = "tax.us.2025.f1098e.1.source-closure"
LINE21 = "tax.us.2025.schedule1.line21-sli-deduction"

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
SCHED1_ABSENCES = [
    f"tax.us.2025.schedule1-adjustments-scope.no-line{n}"
    for n in [
        "11-educator", "12-business-expenses", "13-hsa", "14-moving",
        "15-deductible-se", "16-se-retirement", "17-se-health", "18-penalty",
        "19-alimony-paid", "20-ira-deduction", "23-archer-msa", "25-other-adjustments",
    ]
]
LEGAL_ZERO = [
    "tax.us.2025.sli-scope.not-claimed-as-dependent",
    "tax.us.2025.sli-scope.legally-obligated-for-interest",
]
ALL_CONDITIONAL = UNIVERSAL_FILER + UNIVERSAL_STATEMENT + SCHED1_ABSENCES + LEGAL_ZERO
assert len(ALL_CONDITIONAL) == 22

ADOPTION_PIN = {"role": "adoption", "id": "demo.package.sli-worksheet.2025", "version": "v1"}
GOV_PINS = [{"role": "governance", "id": "governance.constitution", "version": "v1"}]


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))


def _closure_authority(*, closed: bool) -> dict[str, Any]:
    family = _load(FAMILY_FILE)
    mapping = {
        "schema": "source-closure-mapping.v1",
        "id": "tax.us.2025.mapping.f1098e.1",
        "version": "v1",
        "family": {"id": family["id"], "version": family["version"]},
        "member_fact_type": BOX1,
        "closure_fact_type": CLOSURE_TYPE,
        "closure_horizon_key": "family-horizon",
        "admits_symbol": family["authorizes_subtotal"],
        "admission": {"condition": "current-literal-true"},
    }
    findings = (
        [ClosureFindingRecord("f.sli.closure", CLOSURE_TYPE, "h0", True)] if closed else []
    )
    return {
        "family_declarations": [family],
        "closure_mappings": [mapping],
        "closure_findings": findings,
        "current_horizons": {FAMILY: "h0"},
    }


def _yes_inputs(components: list[str], *, offset: int = 0, answers: dict[str, str] | None = None) -> list[InputFinding]:
    answers = answers or {}
    findings = []
    for i, component in enumerate(components):
        value = answers.get(component, "yes")
        findings.append(InputFinding(component, value, f"f.sli.component.{offset + i}", "input"))
    return findings


def _split_witness_inputs(inputs: list[InputFinding]) -> tuple[list[InputFinding], list[SourceFact]]:
    """Route the five per-statement universal witnesses to ``sources``.

    Track 6b repair: ``rule.sli-worksheet.json`` now reads these five
    (``UNIVERSAL_STATEMENT``) via the new ``collect_categorical_all_equal``
    op over ``env.sources``, never a single unkeyed ``ref`` over
    ``env.symbols`` (production marshals them the same way, registering
    them as collect source names -- see ``packages/derivation/live.py``).
    This harness still builds every test scenario the same way it always
    has, via ``InputFinding`` lists keyed by component id; this helper is
    the one place that translates a witness ``InputFinding`` into the
    ``SourceFact`` the rule now actually reads, so every existing call
    site and test method is unchanged and the computed worksheet dollar
    values stay byte-identical for every single-statement input.
    """
    kept: list[InputFinding] = []
    witness_sources: list[SourceFact] = []
    for finding in inputs:
        if finding.symbol in UNIVERSAL_STATEMENT:
            fact_id = (
                f"{finding.symbol}|lender=demo.sli.lender.0,"
                f"statement=demo.sli.stmt.0,tax-year=2025"
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


class SliWorksheetRunnerFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.canon = load_canon(self.schemas)
        self.rule = _load(RULE_FILE)
        self.subtotal_rule = _load(SUBTOTAL_RULE_FILE)
        self.schemas.validate_declared(self.rule)
        self.schemas.validate_declared(self.subtotal_rule)
        self.parameters = {
            p["id"]: p
            for p in [
                _load("parameter.sli-interest-cap.json"),
                _load("parameter.sli-magi-threshold.json"),
                _load("parameter.sli-magi-phase-range.json"),
            ]
        }

    def base_inputs(self, *, filing_status: str = "single", total_income: str = "50000") -> list[InputFinding]:
        return [
            InputFinding("rounding.convention", "half_up", "f.sli.rounding", "input"),
            InputFinding("filing_status", filing_status, "f.sli.filing", "choice"),
            InputFinding("tax.us.2025.income.total-income", total_income, "f.sli.income", "input"),
        ]

    def context(self, **overrides: Any) -> RunContext:
        base: dict[str, Any] = dict(
            run_id="run.sli.1",
            rules=[self.rule, self.subtotal_rule],
            parameters=self.parameters,
            canon=self.canon,
            inputs=self.base_inputs(),
            sources=[],
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOV_PINS,
            # Production marshals the "filing_status" choice symbol against the
            # tax.us.2025.filing-status fact type via an input binding
            # (packages.derivation.marshal); this direct-RunContext harness
            # supplies the same binding explicitly so the rule's MFS
            # categorical_compare's domain-match check sees the real fact
            # type identity rather than the bare symbol name.
            input_bindings=[
                {
                    "symbol": "filing_status",
                    "fact_type": {"id": "tax.us.2025.filing-status", "version": "v1"},
                    "mode": "required",
                }
            ],
        )
        base.update(overrides)
        kept_inputs, witness_sources = _split_witness_inputs(list(base["inputs"]))
        base["inputs"] = kept_inputs
        base["sources"] = list(base["sources"]) + witness_sources
        return RunContext(**base)

    def box1_source(self, amount: str, *, index: int = 0) -> SourceFact:
        fact_id = f"{BOX1}|lender=demo.sli.lender.{index},statement=demo.sli.stmt.{index},tax-year=2025"
        return SourceFact(name=BOX1, value=amount, finding_id=f"f.sli.box1.{index}", fact_id=fact_id)

    def published_line21(self, result: Any) -> str | None:
        for pub in result.publications:
            if pub.finding["symbol"] == LINE21:
                return cast(str, pub.finding["value"])
        return None

    def blocked_entry(self, result: Any) -> dict[str, Any] | None:
        for entry in result.blocked:
            if entry["artifact_id"] == self.rule["id"]:
                return cast(dict[str, Any], entry)
        return None


class ClosedEmptyFamily(SliWorksheetRunnerFixture):
    def test_closed_empty_family_computes_zero(self) -> None:
        ctx = self.context(sources=[], **_closure_authority(closed=True))
        result = run(ctx, self.schemas)
        self.assertEqual(self.published_line21(result), "0")
        self.assertIsNone(self.blocked_entry(result))

    def test_unclosed_family_blocks_on_closure(self) -> None:
        ctx = self.context(
            sources=[self.box1_source("1000")],
            **_closure_authority(closed=False),
        )
        result = run(ctx, self.schemas)
        blocked = self.blocked_entry(result)
        self.assertIsNotNone(blocked)
        assert blocked is not None
        self.assertEqual(blocked["code"], BLOCK_CLOSURE)
        self.assertIsNone(self.published_line21(result))


class EligibleComputation(SliWorksheetRunnerFixture):
    def test_single_statement_below_phaseout_floor_gets_full_capped_deduction(self) -> None:
        # box1 = 3000 (over the $2,500 cap) -> line1 = 2500; total-income = 50000
        # <= 85000 single threshold -> line6 = 0 -> line7 = 0 -> line9 = line1.
        ctx = self.context(
            inputs=self.base_inputs(total_income="50000")
            + _yes_inputs(ALL_CONDITIONAL),
            sources=[self.box1_source("3000")],
            **_closure_authority(closed=True),
        )
        result = run(ctx, self.schemas)
        self.assertIsNone(self.blocked_entry(result))
        self.assertEqual(self.published_line21(result), "2500")

    def test_single_statement_in_phaseout_band_reduces_the_deduction(self) -> None:
        # box1 = 2000 (under cap) -> line1 = 2000; total-income = 90000, single
        # threshold 85000, range 15000 -> line6 = 5000, line7 = 5000/15000 =
        # 0.333 (half_up, 3 places), line8 = 2000*0.333 = 666.000,
        # line9 = 2000 - 666.000 = 1334.000 -> rounded 1334. Proves
        # multiply/divide compose correctly through a real MAGI phaseout.
        ctx = self.context(
            inputs=self.base_inputs(total_income="90000")
            + _yes_inputs(ALL_CONDITIONAL),
            sources=[self.box1_source("2000")],
            **_closure_authority(closed=True),
        )
        result = run(ctx, self.schemas)
        self.assertIsNone(self.blocked_entry(result))
        self.assertEqual(self.published_line21(result), "1334")

    def test_magi_at_or_above_ceiling_computes_zero_not_blocked(self) -> None:
        # total-income 110000, single: line6 = max(110000-85000,0)=25000 >=
        # 15000 range -> ratio capped at 1.000 -> line9 = line1 - line1 = 0.
        ctx = self.context(
            inputs=self.base_inputs(total_income="110000")
            + _yes_inputs(ALL_CONDITIONAL),
            sources=[self.box1_source("1000")],
            **_closure_authority(closed=True),
        )
        result = run(ctx, self.schemas)
        self.assertIsNone(self.blocked_entry(result))
        self.assertEqual(self.published_line21(result), "0")


class BlockingDispositions(SliWorksheetRunnerFixture):
    def test_universal_component_violation_blocks_the_whole_route(self) -> None:
        answers = {"tax.us.2025.f1098e.no-related-person-interest": "no"}
        ctx = self.context(
            inputs=self.base_inputs(total_income="50000")
            + _yes_inputs(ALL_CONDITIONAL, answers=answers),
            sources=[self.box1_source("1000")],
            **_closure_authority(closed=True),
        )
        result = run(ctx, self.schemas)
        blocked = self.blocked_entry(result)
        self.assertIsNotNone(blocked)
        assert blocked is not None
        self.assertEqual(blocked["code"], "SLI_UNIVERSAL_COMPONENT_VIOLATION")
        self.assertIsNone(self.published_line21(result))

    def test_schedule1_part_ii_activity_blocks_out_of_scope(self) -> None:
        # A "no" on any of the twelve Schedule-1-native absence facts means
        # this return has a Part II adjustment this milestone cannot
        # compute (no producer exists for lines 11-20/23/25 yet) -- the
        # worksheet's own line 3 could not be honestly treated as $0, so
        # the whole route must block rather than silently underweight the
        # taxpayer's true MAGI base.
        answers = {"tax.us.2025.schedule1-adjustments-scope.no-line13-hsa": "no"}
        ctx = self.context(
            inputs=self.base_inputs(total_income="50000")
            + _yes_inputs(ALL_CONDITIONAL, answers=answers),
            sources=[self.box1_source("1000")],
            **_closure_authority(closed=True),
        )
        result = run(ctx, self.schemas)
        blocked = self.blocked_entry(result)
        self.assertIsNotNone(blocked)
        assert blocked is not None
        self.assertEqual(blocked["code"], "SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE")
        self.assertIsNone(self.published_line21(result))

    def test_mfs_filing_status_blocks_the_whole_route(self) -> None:
        ctx = self.context(
            inputs=self.base_inputs(filing_status="married_filing_separately", total_income="50000")
            + _yes_inputs(ALL_CONDITIONAL),
            sources=[self.box1_source("1000")],
            **_closure_authority(closed=True),
        )
        result = run(ctx, self.schemas)
        blocked = self.blocked_entry(result)
        self.assertIsNotNone(blocked)
        assert blocked is not None
        self.assertEqual(blocked["code"], "SLI_MFS_INELIGIBLE")

    def test_missing_eligibility_component_blocks_dependency_absent(self) -> None:
        # Drop one of the twenty-two conditional-dependency-set members
        # entirely (never asserted) -- proves conditional_dependency_set
        # reports absence rather than all's short-circuit silence.
        components = [c for c in ALL_CONDITIONAL if c != "tax.us.2025.sli-scope.no-form-2555"]
        ctx = self.context(
            inputs=self.base_inputs(total_income="50000") + _yes_inputs(components),
            sources=[self.box1_source("1000")],
            **_closure_authority(closed=True),
        )
        result = run(ctx, self.schemas)
        blocked = self.blocked_entry(result)
        self.assertIsNotNone(blocked)
        assert blocked is not None
        self.assertEqual(blocked["code"], BLOCK_ABSENT)
        self.assertIn("tax.us.2025.sli-scope.no-form-2555", blocked["missing"])


class LegalZeroComputation(SliWorksheetRunnerFixture):
    def test_claimed_as_dependent_computes_zero_not_blocked(self) -> None:
        answers = {"tax.us.2025.sli-scope.not-claimed-as-dependent": "no"}
        ctx = self.context(
            inputs=self.base_inputs(total_income="50000")
            + _yes_inputs(ALL_CONDITIONAL, answers=answers),
            sources=[self.box1_source("1000")],
            **_closure_authority(closed=True),
        )
        result = run(ctx, self.schemas)
        self.assertIsNone(self.blocked_entry(result))
        self.assertEqual(self.published_line21(result), "0")

    def test_not_legally_obligated_computes_zero_not_blocked(self) -> None:
        answers = {"tax.us.2025.sli-scope.legally-obligated-for-interest": "no"}
        ctx = self.context(
            inputs=self.base_inputs(total_income="50000")
            + _yes_inputs(ALL_CONDITIONAL, answers=answers),
            sources=[self.box1_source("1000")],
            **_closure_authority(closed=True),
        )
        result = run(ctx, self.schemas)
        self.assertIsNone(self.blocked_entry(result))
        self.assertEqual(self.published_line21(result), "0")


if __name__ == "__main__":
    unittest.main()
