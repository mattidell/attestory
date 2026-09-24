"""A4 second pass, probe P1 — one categorical conclusion per key of one subject.

Disposable evidence, not a design. It asks whether the existing engine, with
no production change, can publish one favourable categorical conclusion per
key of a single subject: a student-and-period taken from a financing claim,
or a Form 1098-E statement. Synthetic ``demo.*`` identities only. Nothing
here is a production citizen, and this module is not imported.

The ordinary path is ``marshal_run_context`` then ``runner.run`` — no
hand-built ``Environment``. The pairing path calls
``evaluate_pairing_scoped_rule`` and does not copy the rule's citations into
``extra_pins``; doing so would be the test performing ``pins_for``. The stub
record has no kernel fact lattice, so marshalled ``SourceFact.keys`` is
``None``. Identity is carried only by ``fact_id``.
"""

from __future__ import annotations

import json
import unittest
from typing import Any

from packages.derivation.loader import DerivationSchemas
from packages.derivation.marshal import marshal_run_context
from packages.derivation.pairing_dispatch import (
    PairingBinding,
    PairingBlock,
    PairingPublish,
    PairingScopedResult,
    evaluate_pairing_scoped_rule,
)
from packages.derivation.runner import (
    RunContext,
    RunResult,
    _Run,
    _content_id,
    _sorted_pins,
    _value_str,
    run,
)
from packages.kernel.currency import CurrencyView, compute_currency
from packages.kernel.facts import KernelState, fact_id_for
from packages.kernel.findings import FindingState
from tests.derivation.test_link_coverage_contract import (
    SCOPE as COVERAGE_SCOPE,
    _citation,
    _coverage,
    _fact_type,
    _parameter,
    _validate,
)

FINANCING = "demo.tax.financing-claim"
CIRCUMSTANCE = "demo.tax.schooling-circumstance"
BOX1 = "demo.tax.f1098e.box1-student-loan-interest"
PAIRING = "demo.association.financing~circumstance"
CONCLUSION = "demo.tax.no-enumerated-adverse"
RULE_ID = "demo.rule.no-enumerated-adverse"
RULE_VERSION = "v1"
CITATION_ID = "demo.citation.no-enumerated-adverse"
FAVOURABLE = "no-enumerated-adverse"
ADOPTION_PIN = {"role": "adoption", "id": "demo.package.sli-a4-pass2", "version": "v1"}
GOVERNANCE_PINS = [{"role": "governance", "id": "demo.governance.probe", "version": "v1"}]

BORROWING = "demo.borrowing.one"
INSTITUTION = "demo.institution.riverside"
PROGRAMME = "demo.programme.bsc"
STUDENT = "demo.student.filer"
LENDER = "demo.lender.north"
YEAR = "2025"
PERIOD_AUTUMN = "2024-autumn"
PERIOD_SPRING = "2025-spring"
STATEMENT_S1 = "demo.statement.s1"
STATEMENT_S2 = "demo.statement.s2"

# Finding ids encode sort order on purpose. Marshal binds agreeing values to
# ``sorted(finding id)[0]``, not to a period or a statement. Autumn sorts
# first and is the favourable period; spring sorts second and is the only
# period with an adverse circumstance. A pin that follows autumn is the sort,
# not a match of the adverse period.
AUTUMN_FINDING = "demo.finding.financing.1-autumn"
SPRING_FINDING = "demo.finding.financing.2-spring"
CIRCUMSTANCE_FINDING = "demo.finding.circumstance.spring"
BOX_S1_FINDING = "demo.finding.box1.1-s1"
BOX_S2_FINDING = "demo.finding.box1.2-s2"
PAIRING_FINDING = "demo.finding.pairing.spring"

CALLER_BLOCK = "demo.ADVERSE_SUPPORTED"
SCHEMAS = DerivationSchemas()

_WHEN_SUBJECT_AND_NOT_ADVERSE: dict[str, Any] = {
    "op": "all",
    "args": [
        {
            "op": "categorical_compare",
            "left": {"op": "ref", "name": FINANCING},
            "right": {
                "op": "category_literal",
                "fact_type": {"id": FINANCING, "version": "v1"},
                "value": "tuition",
            },
            "cmp": "eq",
        },
        {
            "op": "categorical_compare",
            "left": {"op": "ref", "name": CIRCUMSTANCE},
            "right": {
                "op": "category_literal",
                "fact_type": {"id": CIRCUMSTANCE, "version": "v1"},
                "value": "not-adverse",
            },
            "cmp": "eq",
        },
    ],
}

_WHEN_BOX1_PRESENT: dict[str, Any] = {
    "op": "compare",
    "cmp": "gt",
    "left": {"op": "ref", "name": BOX1},
    "right": 0,
}

_WHEN_BOX1_COLLECTED: dict[str, Any] = {
    "op": "compare",
    "cmp": "gt",
    "left": {"op": "add", "args": [{"op": "collect", "name": BOX1}]},
    "right": 0,
}


class _HorizonState:
    def __init__(self) -> None:
        self.current_by_chain: dict[tuple[str, str, str], str] = {}


class _State:
    def __init__(self, findings: dict[str, dict[str, Any]]) -> None:
        self.findings = findings
        self.horizon_state = _HorizonState()


def _finding(fid: str, fact_id: str, value: Any) -> dict[str, Any]:
    return {"id": fid, "fact_id": fact_id, "value": value, "basis": "attested"}


def _currency(finding_ids: list[str]) -> CurrencyView:
    ids = frozenset(finding_ids)
    return CurrencyView(
        current_finding_ids=ids,
        displaced_finding_ids=frozenset(),
        current_evidence_ids=frozenset(),
        displaced_evidence_ids=frozenset(),
    )


def _financing_fact_id(period: str) -> str:
    return fact_id_for(
        FINANCING,
        (
            ("borrowing", BORROWING),
            ("period", period),
            ("institution", INSTITUTION),
            ("programme", PROGRAMME),
        ),
    )


def _circumstance_fact_id(period: str) -> str:
    return fact_id_for(CIRCUMSTANCE, (("student", STUDENT), ("period", period)))


def _box1_fact_id(statement: str) -> str:
    return fact_id_for(
        BOX1,
        (("lender", LENDER), ("statement", statement), ("tax-year", YEAR)),
    )


def _rule(*, requires: list[str], when: Any) -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v6",
        "id": RULE_ID,
        "version": RULE_VERSION,
        "role": "applicability",
        "requires": requires,
        "when": when,
        "value": {
            "op": "category_literal",
            "fact_type": {"id": CONCLUSION, "version": "v1"},
            "value": FAVOURABLE,
        },
        "publishes": CONCLUSION,
        "citations": [{"id": CITATION_ID, "version": "v1"}],
    }


def _circumstance_default() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]]]:
    fact_types = [
        {
            "id": CIRCUMSTANCE,
            "version": "v1",
            "value_schema": {"enum": ["adverse", "not-adverse"]},
            "optional_default": {
                "parameter": {"id": "demo.parameter.circumstance-default", "version": "v1"}
            },
        },
        {
            "id": FINANCING,
            "version": "v1",
            "value_schema": {"enum": ["tuition"]},
        },
    ]
    bindings = [
        {
            "symbol": CIRCUMSTANCE,
            "fact_type": {"id": CIRCUMSTANCE, "version": "v1"},
            "mode": "optional_default",
        },
        {
            "symbol": FINANCING,
            "fact_type": {"id": FINANCING, "version": "v1"},
            "mode": "required",
        },
    ]
    parameters = {
        "demo.parameter.circumstance-default": {
            "id": "demo.parameter.circumstance-default",
            "version": "v1",
            "values": "not-adverse",
        }
    }
    return fact_types, bindings, parameters


def _execute(
    findings: dict[str, dict[str, Any]],
    rules: list[dict[str, Any]],
    *,
    collect: list[str] | None = None,
    bindings: list[dict[str, Any]] | None = None,
    fact_types: list[dict[str, Any]] | None = None,
    parameters: dict[str, dict[str, Any]] | None = None,
) -> tuple[RunContext, RunResult]:
    ctx = marshal_run_context(
        run_id="demo.sli-a4-pass2",
        state=_State(findings),  # type: ignore[arg-type]
        currency=_currency(list(findings)),
        rules=rules,
        parameters={} if parameters is None else parameters,
        canon={},
        adoption_pin=ADOPTION_PIN,
        governance_pins=GOVERNANCE_PINS,
        fact_types=fact_types,
        input_bindings=bindings,
        collect_source_names=collect,
    )
    return ctx, run(ctx, SCHEMAS)


def _conclusions(result: RunResult) -> list[dict[str, Any]]:
    return [pub.finding for pub in result.publications if pub.finding["symbol"] == CONCLUSION]


def _pins(finding_or_row: dict[str, Any]) -> list[dict[str, Any]]:
    pins = finding_or_row["pins"]
    assert isinstance(pins, list)
    return pins


def _ids(pins: list[dict[str, Any]], role: str) -> set[str]:
    return {str(pin["id"]) for pin in pins if pin["role"] == role}


def _input_ids(pins: list[dict[str, Any]]) -> set[str]:
    return _ids(pins, "input")


def _financing_findings(spring_value: str, *, circumstance: bool) -> dict[str, dict[str, Any]]:
    findings = {
        AUTUMN_FINDING: _finding(AUTUMN_FINDING, _financing_fact_id(PERIOD_AUTUMN), "tuition"),
        SPRING_FINDING: _finding(SPRING_FINDING, _financing_fact_id(PERIOD_SPRING), spring_value),
    }
    if circumstance:
        findings[CIRCUMSTANCE_FINDING] = _finding(
            CIRCUMSTANCE_FINDING, _circumstance_fact_id(PERIOD_SPRING), "adverse"
        )
    return findings


def _box_findings(s2_amount: int) -> dict[str, dict[str, Any]]:
    return {
        BOX_S1_FINDING: _finding(BOX_S1_FINDING, _box1_fact_id(STATEMENT_S1), 1500),
        BOX_S2_FINDING: _finding(BOX_S2_FINDING, _box1_fact_id(STATEMENT_S2), s2_amount),
    }


def _bound_finding_ids(ctx: RunContext, symbol: str) -> list[str]:
    return [item.finding_id for item in ctx.inputs if item.symbol == symbol]


class StudentAndPeriodKeys(unittest.TestCase):
    """Scenario (a): one borrowing, autumn 2024 and spring 2025.

    Spring alone has an adverse enrolment circumstance. The financing claims
    share the value ``tuition``; the period is only in the fact id.
    """

    def setUp(self) -> None:
        self.autumn_fact = _financing_fact_id(PERIOD_AUTUMN)
        self.spring_fact = _financing_fact_id(PERIOD_SPRING)
        self.circumstance_fact = _circumstance_fact_id(PERIOD_SPRING)
        self.rule = _rule(requires=[FINANCING, CIRCUMSTANCE], when=_WHEN_SUBJECT_AND_NOT_ADVERSE)
        self.assertLess(AUTUMN_FINDING, SPRING_FINDING)
        for fact_id, period in (
            (self.autumn_fact, PERIOD_AUTUMN),
            (self.spring_fact, PERIOD_SPRING),
        ):
            self.assertIn(f"borrowing={BORROWING}", fact_id)
            self.assertIn(f"period={period}", fact_id)
            self.assertIn(f"institution={INSTITUTION}", fact_id)
            self.assertIn(f"programme={PROGRAMME}", fact_id)
        self.assertIn(f"period={PERIOD_SPRING}", self.circumstance_fact)

    def test_a_adverse_spring_is_one_rule_inapplicable_not_one_conclusion(self) -> None:
        """Both financing claims are current. Marshal keeps the sort-first one.

        The guard then sees that one bound value plus the spring circumstance
        and records one ``inapplicable`` row for the rule. Autumn is not
        published. Spring is not given its own row.
        """
        findings = _financing_findings("tuition", circumstance=True)
        ctx, result = _execute(findings, [self.rule])

        self.assertEqual(_bound_finding_ids(ctx, FINANCING), [AUTUMN_FINDING])
        self.assertEqual(_bound_finding_ids(ctx, CIRCUMSTANCE), [CIRCUMSTANCE_FINDING])
        self.assertEqual(_conclusions(result), [])
        self.assertEqual(result.blocked, [])
        self.assertEqual(len(result.dispositions), 1)
        row = result.dispositions[0]
        self.assertEqual(row["artifact_id"], RULE_ID)
        self.assertEqual(row["disposition"], "inapplicable")
        self.assertIs(row["guard_result"], False)
        self.assertNotIn("symbol", row)
        pins = _pins(row)
        self.assertEqual(_ids(pins, "citation"), {CITATION_ID})
        self.assertEqual(_input_ids(pins), {AUTUMN_FINDING, CIRCUMSTANCE_FINDING})
        self.assertNotIn(SPRING_FINDING, _input_ids(pins))
        self.assertNotIn(PERIOD_AUTUMN, str(row))
        self.assertNotIn(self.spring_fact, str(row))

    def test_a_absence_of_circumstance_blocks_instead_of_publishing(self) -> None:
        """No circumstance finding. The same rule does not treat absence as favourable."""
        findings = _financing_findings("tuition", circumstance=False)
        ctx, result = _execute(findings, [self.rule])

        self.assertEqual(_bound_finding_ids(ctx, FINANCING), [AUTUMN_FINDING])
        self.assertEqual(_bound_finding_ids(ctx, CIRCUMSTANCE), [])
        self.assertEqual(_conclusions(result), [])
        self.assertEqual(len(result.dispositions), 1)
        row = result.dispositions[0]
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(row["missing"], [CIRCUMSTANCE])
        self.assertEqual(row["pins"], [])
        self.assertEqual(len(result.blocked), 1)
        self.assertEqual(result.blocked[0]["code"], "DEPENDENCY_ABSENT")

    def test_a_declared_default_still_publishes_one_conclusion_for_two_periods(self) -> None:
        """``optional_default`` fills a missing circumstance symbol once.

        Both periods are favourable. One conclusion is published, pinned to
        the sort-first financing finding and to the manufactured default, not
        to each period.
        """
        findings = _financing_findings("tuition", circumstance=False)
        fact_types, bindings, parameters = _circumstance_default()
        ctx, result = _execute(
            findings,
            [self.rule],
            bindings=bindings,
            fact_types=fact_types,
            parameters=parameters,
        )

        self.assertEqual(_bound_finding_ids(ctx, FINANCING), [AUTUMN_FINDING])
        self.assertNotIn(SPRING_FINDING, [item.finding_id for item in ctx.inputs])
        conclusions = _conclusions(result)
        self.assertEqual(len(conclusions), 1)
        conclusion = conclusions[0]
        self.assertEqual(conclusion["value"], FAVOURABLE)
        self.assertEqual(conclusion["symbol"], CONCLUSION)
        self.assertNotIn(PERIOD_AUTUMN, str(conclusion["symbol"]))
        self.assertNotIn(PERIOD_SPRING, str(conclusion["symbol"]))
        self.assertNotIn(PERIOD_SPRING, str(conclusion["value"]))
        pins = _pins(conclusion)
        self.assertEqual(_ids(pins, "citation"), {CITATION_ID})
        self.assertIn(AUTUMN_FINDING, _input_ids(pins))
        self.assertNotIn(SPRING_FINDING, _input_ids(pins))
        origins = {str(pin["id"]): pin.get("origin") for pin in pins if pin["role"] == "input"}
        self.assertEqual(origins[AUTUMN_FINDING], "assertion")
        self.assertIn("declared_default", origins.values())
        published = [row for row in result.dispositions if row["disposition"] == "published"]
        conclusion_rows = [row for row in published if row.get("symbol") == CONCLUSION]
        self.assertEqual(len(conclusion_rows), 1)
        self.assertEqual(_ids(_pins(conclusion_rows[0]), "citation"), {CITATION_ID})

    def test_a_disagreeing_financing_values_never_reach_the_guard(self) -> None:
        """Different telling values leave the financing symbol unbound.

        The spring circumstance is current and still produces no
        ``inapplicable`` row. The rule blocks ``DEPENDENCY_ABSENT`` with
        empty pins.
        """
        findings = _financing_findings("fees", circumstance=True)
        ctx, result = _execute(findings, [self.rule])

        self.assertEqual(_bound_finding_ids(ctx, FINANCING), [])
        self.assertEqual(_bound_finding_ids(ctx, CIRCUMSTANCE), [CIRCUMSTANCE_FINDING])
        self.assertEqual(_conclusions(result), [])
        self.assertEqual(len(result.dispositions), 1)
        row = result.dispositions[0]
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(row["missing"], [FINANCING])
        self.assertEqual(row["pins"], [])
        self.assertNotIn(CIRCUMSTANCE_FINDING, str(row["pins"]))


class StatementKeys(unittest.TestCase):
    """Scenario (b): two statements, no financing claims."""

    def setUp(self) -> None:
        self.s1_fact = _box1_fact_id(STATEMENT_S1)
        self.s2_fact = _box1_fact_id(STATEMENT_S2)
        self.assertLess(BOX_S1_FINDING, BOX_S2_FINDING)
        self.assertIn(f"lender={LENDER}", self.s1_fact)
        self.assertIn(f"statement={STATEMENT_S1}", self.s1_fact)
        self.assertIn(f"tax-year={YEAR}", self.s1_fact)
        self.assertIn(f"statement={STATEMENT_S2}", self.s2_fact)
        self.assertNotEqual(self.s1_fact, self.s2_fact)

    def test_b_disagreeing_box1_amounts_block_with_no_pins(self) -> None:
        """Two different box-1 amounts are not one symbol and not two conclusions."""
        findings = _box_findings(2500)
        ctx, result = _execute(
            findings, [_rule(requires=[BOX1], when=_WHEN_BOX1_PRESENT)]
        )

        self.assertEqual(ctx.inputs, [])
        self.assertEqual(ctx.sources, [])
        self.assertEqual(_conclusions(result), [])
        self.assertEqual(len(result.dispositions), 1)
        row = result.dispositions[0]
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(row["missing"], [BOX1])
        self.assertEqual(row["pins"], [])
        self.assertNotIn(STATEMENT_S1, str(row))
        self.assertNotIn(STATEMENT_S2, str(row))

    def test_b_agreeing_amounts_pin_only_the_sort_first_statement(self) -> None:
        """Equal amounts bind one finding. The conclusion cites the rule and pins that one."""
        findings = _box_findings(1500)
        ctx, result = _execute(
            findings, [_rule(requires=[BOX1], when=_WHEN_BOX1_PRESENT)]
        )

        self.assertEqual(_bound_finding_ids(ctx, BOX1), [BOX_S1_FINDING])
        conclusions = _conclusions(result)
        self.assertEqual(len(conclusions), 1)
        conclusion = conclusions[0]
        self.assertEqual(conclusion["symbol"], CONCLUSION)
        self.assertEqual(conclusion["value"], FAVOURABLE)
        self.assertNotIn(STATEMENT_S1, str(conclusion["symbol"]))
        self.assertNotIn(STATEMENT_S2, str(conclusion["symbol"]))
        pins = _pins(conclusion)
        self.assertEqual(_input_ids(pins), {BOX_S1_FINDING})
        self.assertEqual(_ids(pins, "citation"), {CITATION_ID})
        self.assertNotIn(BOX_S2_FINDING, _input_ids(pins))

    def test_b_collect_publishes_one_conclusion_pinning_both_statements(self) -> None:
        """Collect keeps both amounts and still publishes one symbol."""
        findings = _box_findings(2500)
        ctx, result = _execute(
            findings,
            [_rule(requires=[], when=_WHEN_BOX1_COLLECTED)],
            collect=[BOX1],
        )

        self.assertEqual(
            [source.finding_id for source in ctx.sources if source.name == BOX1],
            [BOX_S1_FINDING, BOX_S2_FINDING],
        )
        conclusions = _conclusions(result)
        self.assertEqual(len(conclusions), 1)
        pins = _pins(conclusions[0])
        self.assertEqual(_input_ids(pins), {BOX_S1_FINDING, BOX_S2_FINDING})
        self.assertEqual(_ids(pins, "citation"), {CITATION_ID})
        self.assertEqual(conclusions[0]["symbol"], CONCLUSION)
        self.assertNotIn(STATEMENT_S1, str(conclusions[0]["symbol"]))
        published = [row for row in result.dispositions if row["disposition"] == "published"]
        self.assertEqual(len(published), 1)
        self.assertEqual(published[0]["symbol"], CONCLUSION)


class PairingDispatchIsNotASingleSubject(unittest.TestCase):
    """The per-item primitive iterates pairing findings. A subject with no pairing is skipped."""

    def _dispatch(
        self,
        sources: list[Any],
        *,
        evaluate_one: Any,
        pairing_type: str,
        left_type: str,
        right_type: str,
    ) -> PairingScopedResult:
        return evaluate_pairing_scoped_rule(
            sources=sources,
            pairing_type=pairing_type,
            left_type=left_type,
            right_type=right_type,
            rule_id=RULE_ID,
            rule_version=RULE_VERSION,
            rule_role="applicability",
            symbol_for=lambda binding: f"{CONCLUSION}|{binding.left_fact_id}",
            evaluate_one=evaluate_one,
            extra_pins=[ADOPTION_PIN],
            schemas=SCHEMAS,
        )

    def test_single_subject_sources_publish_nothing(self) -> None:
        """Financing claims, a circumstance, and two statements are current. No pairing is."""
        period_findings = _financing_findings("tuition", circumstance=True)
        box_findings = _box_findings(2500)
        findings = {**period_findings, **box_findings}
        ctx, _result = _execute(
            findings,
            [],
            collect=[FINANCING, CIRCUMSTANCE, BOX1],
        )
        names = {source.name for source in ctx.sources}
        self.assertEqual(names, {FINANCING, CIRCUMSTANCE, BOX1})
        self.assertEqual(len([s for s in ctx.sources if s.name == FINANCING]), 2)
        self.assertEqual(len([s for s in ctx.sources if s.name == BOX1]), 2)

        def _publish(binding: PairingBinding) -> PairingPublish:
            raise AssertionError(f"evaluate_one must not run, got {binding.pairing_fact_id}")

        period = self._dispatch(
            ctx.sources,
            evaluate_one=_publish,
            pairing_type=PAIRING,
            left_type=FINANCING,
            right_type=CIRCUMSTANCE,
        )
        statements = self._dispatch(
            ctx.sources,
            evaluate_one=_publish,
            pairing_type=PAIRING,
            left_type=BOX1,
            right_type=BOX1,
        )
        self.assertEqual(period.publications, ())
        self.assertEqual(period.blocked, ())
        self.assertEqual(statements.publications, ())
        self.assertEqual(statements.blocked, ())

    def test_a_pairing_publication_pins_both_sides_and_omits_citations(self) -> None:
        """One spring pairing. The callback publishes. Citations are not read off any rule.

        The published symbol is the test's ``symbol_for`` string, copied
        through. It is not a student-and-period key the engine derived.
        """
        spring_fact = _financing_fact_id(PERIOD_SPRING)
        circumstance_fact = _circumstance_fact_id(PERIOD_SPRING)
        pairing_fact = fact_id_for(PAIRING, (("left", spring_fact), ("right", circumstance_fact)))
        findings = _financing_findings("tuition", circumstance=True)
        findings[PAIRING_FINDING] = _finding(
            PAIRING_FINDING,
            pairing_fact,
            {"left_fact_id": spring_fact, "right_fact_id": circumstance_fact},
        )
        ctx, _result = _execute(
            findings, [], collect=[FINANCING, CIRCUMSTANCE, PAIRING]
        )

        def _publish(_binding: PairingBinding) -> PairingPublish:
            return PairingPublish(value=FAVOURABLE)

        result = self._dispatch(
            ctx.sources,
            evaluate_one=_publish,
            pairing_type=PAIRING,
            left_type=FINANCING,
            right_type=CIRCUMSTANCE,
        )
        self.assertEqual(result.blocked, ())
        self.assertEqual(len(result.publications), 1)
        published = result.publications[0]
        self.assertEqual(published["symbol"], f"{CONCLUSION}|{spring_fact}")
        pins = _pins(published)
        self.assertEqual(_input_ids(pins), {SPRING_FINDING, CIRCUMSTANCE_FINDING, PAIRING_FINDING})
        self.assertNotIn(AUTUMN_FINDING, _input_ids(pins))
        self.assertNotIn(CITATION_ID, _ids(pins, "citation"))
        self.assertEqual({pin["role"] for pin in pins}, {"adoption", "applicability", "input"})

    def test_caller_block_is_not_an_inapplicable_disposition(self) -> None:
        """Withholding the adverse pair is the callback. The primitive records a block.

        ``PairingScopedResult`` has publications and blocked rows only.
        """
        spring_fact = _financing_fact_id(PERIOD_SPRING)
        circumstance_fact = _circumstance_fact_id(PERIOD_SPRING)
        pairing_fact = fact_id_for(PAIRING, (("left", spring_fact), ("right", circumstance_fact)))
        findings = _financing_findings("tuition", circumstance=True)
        findings[PAIRING_FINDING] = _finding(
            PAIRING_FINDING,
            pairing_fact,
            {"left_fact_id": spring_fact, "right_fact_id": circumstance_fact},
        )
        ctx, _result = _execute(
            findings, [], collect=[FINANCING, CIRCUMSTANCE, PAIRING]
        )

        def _block(binding: PairingBinding) -> PairingBlock:
            self.assertEqual(binding.right_value, "adverse")
            return PairingBlock(code=CALLER_BLOCK, missing=(binding.right_fact_id,))

        result = self._dispatch(
            ctx.sources,
            evaluate_one=_block,
            pairing_type=PAIRING,
            left_type=FINANCING,
            right_type=CIRCUMSTANCE,
        )
        self.assertEqual(result.publications, ())
        self.assertEqual(len(result.blocked), 1)
        blocked = result.blocked[0]
        self.assertEqual(blocked.code, CALLER_BLOCK)
        self.assertNotEqual(blocked.code, "inapplicable")
        self.assertEqual(blocked.missing, (circumstance_fact,))
        self.assertNotIn(CITATION_ID, _ids(list(blocked.pins), "citation"))
        autumn_fact = _financing_fact_id(PERIOD_AUTUMN)
        self.assertNotIn(autumn_fact, blocked.missing)
        self.assertNotIn(AUTUMN_FINDING, _input_ids(list(blocked.pins)))


# --- P2. Enrolment keyed on the schooling situation, not on a borrowing. ---

ENROLMENT = "demo.tax.enrolment-circumstance"
STATEMENT_BORROWING = "demo.tax.statement-to-borrowing"
P2_BORROWING_INST = "demo.borrowing.institutional"
P2_BORROWING_PRIV = "demo.borrowing.private"
P2_LENDER_SOUTH = "demo.lender.south"
P2_INST_FINDING = "demo.finding.financing.institutional"
P2_PRIV_FINDING = "demo.finding.financing.private"
P2_ENROL_EARLIER = "demo.finding.enrolment.1-not-adverse"
P2_ENROL_LATER = "demo.finding.enrolment.2-adverse"
P2_BOX_NORTH = "demo.finding.box1.north"
P2_BOX_SOUTH = "demo.finding.box1.south"
P2_LINK_NORTH = "demo.finding.link.north"
P2_LINK_SOUTH = "demo.finding.link.south"

_WHEN_FINANCING_NOT_ADVERSE: dict[str, Any] = {
    "op": "all",
    "args": [
        {
            "op": "categorical_compare",
            "left": {"op": "ref", "name": FINANCING},
            "right": {
                "op": "category_literal",
                "fact_type": {"id": FINANCING, "version": "v1"},
                "value": "tuition",
            },
            "cmp": "eq",
        },
        {
            "op": "categorical_compare",
            "left": {"op": "ref", "name": ENROLMENT},
            "right": {
                "op": "category_literal",
                "fact_type": {"id": ENROLMENT, "version": "v1"},
                "value": "not-adverse",
            },
            "cmp": "eq",
        },
    ],
}

_WHEN_STATEMENT_NOT_ADVERSE: dict[str, Any] = {
    "op": "all",
    "args": [
        _WHEN_BOX1_PRESENT,
        {
            "op": "categorical_compare",
            "left": {"op": "ref", "name": STATEMENT_BORROWING},
            "right": {
                "op": "category_literal",
                "fact_type": {"id": STATEMENT_BORROWING, "version": "v1"},
                "value": "reported",
            },
            "cmp": "eq",
        },
        {
            "op": "categorical_compare",
            "left": {"op": "ref", "name": ENROLMENT},
            "right": {
                "op": "category_literal",
                "fact_type": {"id": ENROLMENT, "version": "v1"},
                "value": "not-adverse",
            },
            "cmp": "eq",
        },
    ],
}

_WHEN_PUBLISHED_CONCLUSION: dict[str, Any] = {
    "op": "categorical_compare",
    "left": {"op": "ref", "name": CONCLUSION},
    "right": {
        "op": "category_literal",
        "fact_type": {"id": CONCLUSION, "version": "v1"},
        "value": FAVOURABLE,
    },
    "cmp": "eq",
}


def _p2_literal(
    type_id: str, keys: tuple[tuple[str, tuple[str, ...]], ...]
) -> dict[str, Any]:
    return {
        "id": type_id,
        "nature": "record",
        "identity_keys": [
            {"name": name, "kind": "literal", "values": list(values)}
            for name, values in keys
        ],
    }


def _p2_financing_fact_id(borrowing: str) -> str:
    return fact_id_for(
        FINANCING,
        (
            ("borrowing", borrowing),
            ("period", PERIOD_AUTUMN),
            ("institution", INSTITUTION),
            ("programme", PROGRAMME),
        ),
    )


def _p2_enrolment_fact_id() -> str:
    return fact_id_for(
        ENROLMENT,
        (
            ("period", PERIOD_AUTUMN),
            ("institution", INSTITUTION),
            ("programme", PROGRAMME),
        ),
    )


def _p2_box_fact_id(lender: str, statement: str) -> str:
    return fact_id_for(
        BOX1,
        (("lender", lender), ("statement", statement), ("tax-year", YEAR)),
    )


def _p2_link_fact_id(lender: str, statement: str, borrowing: str) -> str:
    return fact_id_for(
        STATEMENT_BORROWING,
        (
            ("lender", lender),
            ("statement", statement),
            ("tax-year", YEAR),
            ("borrowing", borrowing),
        ),
    )


def _p2_lattice() -> dict[str, dict[str, Any]]:
    borrowings = (P2_BORROWING_INST, P2_BORROWING_PRIV)
    lenders = (LENDER, P2_LENDER_SOUTH)
    statements = (STATEMENT_S1, STATEMENT_S2)
    return {
        FINANCING: _p2_literal(FINANCING, (
            ("borrowing", borrowings),
            ("period", (PERIOD_AUTUMN,)),
            ("institution", (INSTITUTION,)),
            ("programme", (PROGRAMME,)),
        )),
        ENROLMENT: _p2_literal(ENROLMENT, (
            ("period", (PERIOD_AUTUMN,)),
            ("institution", (INSTITUTION,)),
            ("programme", (PROGRAMME,)),
        )),
        BOX1: _p2_literal(BOX1, (
            ("lender", lenders),
            ("statement", statements),
            ("tax-year", (YEAR,)),
        )),
        STATEMENT_BORROWING: _p2_literal(STATEMENT_BORROWING, (
            ("lender", lenders),
            ("statement", statements),
            ("tax-year", (YEAR,)),
            ("borrowing", borrowings),
        )),
    }


def _p2_fact_types() -> list[dict[str, Any]]:
    return [
        {"id": FINANCING, "version": "v1", "value_schema": {"enum": ["tuition"]}},
        {
            "id": ENROLMENT,
            "version": "v1",
            "value_schema": {"enum": ["adverse", "not-adverse"]},
        },
        {
            "id": STATEMENT_BORROWING,
            "version": "v1",
            "value_schema": {"enum": ["reported"]},
        },
        {
            "id": CONCLUSION,
            "version": "v1",
            "value_schema": {"enum": [FAVOURABLE]},
        },
    ]


def _p2_findings(*, corrected: bool, statements: bool) -> dict[str, dict[str, Any]]:
    # compute_currency walks findings in record order. The earlier enrolment
    # answer has to be inserted before the later one or it is not a correction.
    enrol_fact = _p2_enrolment_fact_id()
    findings = {
        P2_INST_FINDING: _finding(
            P2_INST_FINDING, _p2_financing_fact_id(P2_BORROWING_INST), "tuition"
        ),
        P2_PRIV_FINDING: _finding(
            P2_PRIV_FINDING, _p2_financing_fact_id(P2_BORROWING_PRIV), "tuition"
        ),
        P2_ENROL_EARLIER: _finding(P2_ENROL_EARLIER, enrol_fact, "not-adverse"),
    }
    if corrected:
        findings[P2_ENROL_LATER] = _finding(P2_ENROL_LATER, enrol_fact, "adverse")
    if statements:
        findings[P2_BOX_NORTH] = _finding(
            P2_BOX_NORTH, _p2_box_fact_id(LENDER, STATEMENT_S1), 1500
        )
        findings[P2_BOX_SOUTH] = _finding(
            P2_BOX_SOUTH, _p2_box_fact_id(P2_LENDER_SOUTH, STATEMENT_S2), 800
        )
        findings[P2_LINK_NORTH] = _finding(
            P2_LINK_NORTH,
            _p2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_INST),
            "reported",
        )
        findings[P2_LINK_SOUTH] = _finding(
            P2_LINK_SOUTH,
            _p2_link_fact_id(P2_LENDER_SOUTH, STATEMENT_S2, P2_BORROWING_PRIV),
            "reported",
        )
    return findings


def _p2_execute(
    findings: dict[str, dict[str, Any]],
    rules: list[dict[str, Any]],
    *,
    collect: list[str],
) -> tuple[FindingState, CurrencyView, RunContext, _Run]:
    state = FindingState(
        findings=dict(findings),
        fact_state=KernelState(fact_types=_p2_lattice()),
    )
    currency = compute_currency(state)
    ctx = marshal_run_context(
        run_id="demo.sli-a4-pass2-p2",
        state=state,
        currency=currency,
        rules=rules,
        parameters={},
        canon={},
        adoption_pin=ADOPTION_PIN,
        governance_pins=GOVERNANCE_PINS,
        fact_types=_p2_fact_types(),
        collect_source_names=collect,
    )
    return state, currency, ctx, _Run(ctx, SCHEMAS)


def _p2_symbol(fact_id: str) -> str:
    return f"{CONCLUSION}|{fact_id}"


def _p2_row(run: _Run, fact_id: str) -> dict[str, Any]:
    symbol = _p2_symbol(fact_id)
    rows = [row for row in run.dispositions if row.get("symbol") == symbol]
    if len(rows) != 1:
        raise AssertionError(f"{symbol}: {run.dispositions!r}")
    return rows[0]


def _p2_published(run: _Run, fact_id: str) -> dict[str, Any]:
    symbol = _p2_symbol(fact_id)
    matches = [pub.finding for pub in run.publications if pub.finding["symbol"] == symbol]
    if len(matches) != 1:
        raise AssertionError(f"{symbol}: {[pub.finding['symbol'] for pub in run.publications]!r}")
    return matches[0]


def _p2_key_names(sources: list[Any], name: str) -> set[str]:
    names: set[str] = set()
    seen = False
    for source in sources:
        if source.name != name:
            continue
        seen = True
        keys = source.keys
        if keys is None:
            raise AssertionError(f"{name} source {source.finding_id} has no keys")
        names.update(key for key, _value in keys)
    if not seen:
        raise AssertionError(f"no {name} source")
    return names


class CorrectedEnrolmentReachesBothBorrowings(unittest.TestCase):
    """Two borrowings, one autumn enrolment. A later finding corrects it.

    Financing subjects are keyed borrowing + period + institution + programme.
    The enrolment is keyed period + institution + programme. Currency, not the
    test, decides which enrolment finding is current.
    """

    def setUp(self) -> None:
        self.inst_fact = _p2_financing_fact_id(P2_BORROWING_INST)
        self.priv_fact = _p2_financing_fact_id(P2_BORROWING_PRIV)
        self.enrol_fact = _p2_enrolment_fact_id()
        self.rule = _rule(requires=[FINANCING, ENROLMENT], when=_WHEN_FINANCING_NOT_ADVERSE)
        self.assertLess(P2_ENROL_EARLIER, P2_ENROL_LATER)
        self.assertNotEqual(self.inst_fact, self.priv_fact)
        self.assertNotIn("borrowing=", self.enrol_fact)
        self.assertIn(f"period={PERIOD_AUTUMN}", self.enrol_fact)
        self.assertIn(f"institution={INSTITUTION}", self.enrol_fact)
        self.assertIn(f"programme={PROGRAMME}", self.enrol_fact)

    def _run(self, *, corrected: bool) -> tuple[FindingState, CurrencyView, RunContext, _Run]:
        findings = _p2_findings(corrected=corrected, statements=False)
        state, currency, ctx, run = _p2_execute(
            findings,
            [self.rule],
            collect=[FINANCING, ENROLMENT],
        )
        run.evaluate_subject_scoped_rule(subject_type=FINANCING, rule=self.rule)
        return state, currency, ctx, run

    def test_both_borrowings_follow_the_corrected_enrolment(self) -> None:
        """Run 1 publishes both subjects off the favourable finding.

        Run 2 is a fresh marshal over the same record plus a later adverse
        finding for that same enrolment fact. Both subjects become
        inapplicable and pin the later finding. The earlier finding is still
        in the record and in neither pin set.
        """
        first_state, first_currency, first_ctx, first_run = self._run(corrected=False)
        self.assertNotIn(P2_ENROL_LATER, first_state.findings)
        self.assertEqual(first_currency.displaced_finding_ids, frozenset())
        self.assertEqual(
            first_currency.current_finding_ids,
            frozenset({P2_INST_FINDING, P2_PRIV_FINDING, P2_ENROL_EARLIER}),
        )
        self.assertEqual(
            _p2_key_names(first_ctx.sources, FINANCING) & _p2_key_names(first_ctx.sources, ENROLMENT),
            {"period", "institution", "programme"},
        )
        self.assertEqual(first_run.blocked, [])
        self.assertEqual(
            {source.finding_id for source in first_ctx.sources if source.name == ENROLMENT},
            {P2_ENROL_EARLIER},
        )
        for fact_id, finding_id in (
            (self.inst_fact, P2_INST_FINDING),
            (self.priv_fact, P2_PRIV_FINDING),
        ):
            with self.subTest(run=1, borrowing=fact_id):
                row = _p2_row(first_run, fact_id)
                published = _p2_published(first_run, fact_id)
                self.assertEqual(row["disposition"], "published")
                self.assertEqual(published["value"], FAVOURABLE)
                self.assertEqual(
                    _input_ids(_pins(published)),
                    {finding_id, P2_ENROL_EARLIER},
                )
                self.assertNotIn(P2_ENROL_LATER, _input_ids(_pins(published)))
                self.assertNotIn(P2_ENROL_LATER, _input_ids(_pins(row)))

        second_state, second_currency, second_ctx, second_run = self._run(corrected=True)
        self.assertIn(P2_ENROL_EARLIER, second_state.findings)
        self.assertIn(P2_ENROL_LATER, second_state.findings)
        self.assertEqual(second_currency.displaced_finding_ids, frozenset({P2_ENROL_EARLIER}))
        self.assertEqual(
            second_currency.current_finding_ids,
            frozenset({P2_INST_FINDING, P2_PRIV_FINDING, P2_ENROL_LATER}),
        )
        self.assertEqual(
            [(reason.kind, reason.by) for reason in second_currency.reasons[P2_ENROL_EARLIER]],
            [("correction", P2_ENROL_LATER)],
        )
        self.assertEqual(
            {source.finding_id for source in second_ctx.sources if source.name == ENROLMENT},
            {P2_ENROL_LATER},
        )
        self.assertNotIn(
            P2_ENROL_EARLIER,
            {source.finding_id for source in second_ctx.sources},
        )
        self.assertEqual(second_run.blocked, [])
        self.assertEqual(len(second_run.publications), 0)
        for fact_id, finding_id in (
            (self.inst_fact, P2_INST_FINDING),
            (self.priv_fact, P2_PRIV_FINDING),
        ):
            with self.subTest(run=2, borrowing=fact_id):
                row = _p2_row(second_run, fact_id)
                self.assertEqual(row["disposition"], "inapplicable")
                self.assertIs(row["guard_result"], False)
                self.assertNotIn("finding_id", row)
                self.assertEqual(row["symbol"], _p2_symbol(fact_id))
                self.assertEqual(
                    _input_ids(_pins(row)),
                    {finding_id, P2_ENROL_LATER},
                )
                self.assertNotIn(P2_ENROL_EARLIER, _input_ids(_pins(row)))
                other = self.priv_fact if fact_id == self.inst_fact else self.inst_fact
                self.assertNotIn(other, row["symbol"])


class StatementSubjectDoesNotReachCorrectedEnrolment(unittest.TestCase):
    """A statement subject, a statement-to-borrowing claim, then re-derivation.

    The claim is keyed on the statement's keys plus borrowing. The enrolment
    correction is the same record as Part A. This class records what the
    statement rule actually pins.
    """

    def setUp(self) -> None:
        self.inst_fact = _p2_financing_fact_id(P2_BORROWING_INST)
        self.priv_fact = _p2_financing_fact_id(P2_BORROWING_PRIV)
        self.north_fact = _p2_box_fact_id(LENDER, STATEMENT_S1)
        self.south_fact = _p2_box_fact_id(P2_LENDER_SOUTH, STATEMENT_S2)
        self.financing_rule = _rule(
            requires=[FINANCING, ENROLMENT], when=_WHEN_FINANCING_NOT_ADVERSE
        )
        self.link_rule = _rule(
            requires=[BOX1, STATEMENT_BORROWING, ENROLMENT],
            when=_WHEN_STATEMENT_NOT_ADVERSE,
        )
        self.conclusion_rule = _rule(
            requires=[BOX1, CONCLUSION], when=_WHEN_PUBLISHED_CONCLUSION
        )
        self.collect = [FINANCING, ENROLMENT, BOX1, STATEMENT_BORROWING]

    def _open(self, *, corrected: bool) -> tuple[CurrencyView, RunContext, _Run]:
        _state, currency, ctx, run = _p2_execute(
            _p2_findings(corrected=corrected, statements=True),
            [self.financing_rule, self.link_rule, self.conclusion_rule],
            collect=self.collect,
        )
        return currency, ctx, run

    def test_statement_does_not_join_enrolment_through_the_borrowing_claim(self) -> None:
        """The claim joins. The enrolment does not. Correction does not change that.

        Both statement rows block ``DEPENDENCY_ABSENT`` for the enrolment on
        the favourable record and again after the correction. Each pins its
        own box-1 finding and its own statement-to-borrowing finding. Neither
        pins either enrolment finding, though the corrected finding is current
        and is what both financing subjects pin.
        """
        favourable_currency, favourable_ctx, favourable = self._open(corrected=False)
        favourable.evaluate_subject_scoped_rule(
            subject_type=FINANCING, rule=self.financing_rule
        )
        favourable.evaluate_subject_scoped_rule(subject_type=BOX1, rule=self.link_rule)

        corrected_currency, corrected_ctx, corrected = self._open(corrected=True)
        corrected.evaluate_subject_scoped_rule(
            subject_type=FINANCING, rule=self.financing_rule
        )
        corrected.evaluate_subject_scoped_rule(subject_type=BOX1, rule=self.link_rule)

        self.assertEqual(
            corrected_currency.displaced_finding_ids, frozenset({P2_ENROL_EARLIER})
        )
        self.assertIn(P2_ENROL_LATER, corrected_currency.current_finding_ids)
        self.assertEqual(
            {source.finding_id for source in corrected_ctx.sources if source.name == ENROLMENT},
            {P2_ENROL_LATER},
        )
        for fact_id, finding_id in (
            (self.inst_fact, P2_INST_FINDING),
            (self.priv_fact, P2_PRIV_FINDING),
        ):
            financing_row = _p2_row(corrected, fact_id)
            self.assertEqual(financing_row["disposition"], "inapplicable")
            self.assertEqual(
                _input_ids(_pins(financing_row)),
                {finding_id, P2_ENROL_LATER},
            )

        statement_keys = _p2_key_names(corrected_ctx.sources, BOX1)
        self.assertEqual(statement_keys, {"lender", "statement", "tax-year"})
        self.assertEqual(
            statement_keys & _p2_key_names(corrected_ctx.sources, ENROLMENT),
            set(),
        )
        self.assertEqual(
            statement_keys & _p2_key_names(corrected_ctx.sources, FINANCING),
            set(),
        )
        self.assertEqual(
            statement_keys & _p2_key_names(corrected_ctx.sources, STATEMENT_BORROWING),
            {"lender", "statement", "tax-year"},
        )
        self.assertEqual(favourable_currency.displaced_finding_ids, frozenset())

        for fact_id, box_finding, link_finding in (
            (self.north_fact, P2_BOX_NORTH, P2_LINK_NORTH),
            (self.south_fact, P2_BOX_SOUTH, P2_LINK_SOUTH),
        ):
            with self.subTest(statement=fact_id):
                before = _p2_row(favourable, fact_id)
                after = _p2_row(corrected, fact_id)
                self.assertEqual(before["disposition"], "blocked")
                self.assertEqual(before["code"], "DEPENDENCY_ABSENT")
                self.assertEqual(before["missing"], [ENROLMENT])
                self.assertEqual(after["disposition"], before["disposition"])
                self.assertEqual(after["code"], before["code"])
                self.assertEqual(after["missing"], before["missing"])
                self.assertEqual(
                    _input_ids(_pins(before)),
                    {box_finding, link_finding},
                )
                self.assertEqual(_input_ids(_pins(after)), _input_ids(_pins(before)))
                for enrolment_finding in (P2_ENROL_EARLIER, P2_ENROL_LATER):
                    self.assertNotIn(enrolment_finding, _input_ids(_pins(after)))
                    self.assertNotIn(enrolment_finding, _input_ids(_pins(before)))
                self.assertNotIn(P2_INST_FINDING, _input_ids(_pins(after)))
                self.assertNotIn(P2_PRIV_FINDING, _input_ids(_pins(after)))

    def test_published_financing_conclusion_does_not_join_a_statement_directly(self) -> None:
        """A statement cannot skip the link, keys or no keys.

        Recorded at P2 when same-run conclusions carried no keys: requiring
        the published name then failed closed as DEPENDENCY_INVALID. Since
        Track 2 the per-subject publication's same-run source carries its
        subject's structured keys, but those key names (borrowing, period,
        institution, programme) share nothing with a statement's (lender,
        statement, tax-year), so the join finds no match and the require is
        DEPENDENCY_ABSENT on both records. Carrying keys does not let a
        statement reach a financing conclusion without the statement-to-
        borrowing link -- the chain in KeyedSameRunStatementChain is what
        reaches it. Still never the enrolment finding.
        """
        _favourable_currency, _favourable_ctx, favourable = self._open(corrected=False)
        favourable.evaluate_subject_scoped_rule(
            subject_type=FINANCING, rule=self.financing_rule
        )
        published_sources = [
            source for source in favourable.live_sources if source.name == CONCLUSION
        ]
        self.assertEqual(
            {source.fact_id for source in published_sources},
            {self.inst_fact, self.priv_fact},
        )
        for source in published_sources:
            self.assertIsNotNone(source.keys)
            self.assertFalse({name for name, _ in source.keys or ()} & {"lender", "statement", "tax-year"})
        self.assertIn(_p2_symbol(self.inst_fact), favourable.symbols)
        self.assertNotIn(
            _p2_symbol(self.inst_fact),
            {source.name for source in favourable.live_sources},
        )
        favourable.evaluate_subject_scoped_rule(subject_type=BOX1, rule=self.conclusion_rule)

        _corrected_currency, _corrected_ctx, corrected = self._open(corrected=True)
        corrected.evaluate_subject_scoped_rule(
            subject_type=FINANCING, rule=self.financing_rule
        )
        self.assertEqual(
            [source for source in corrected.live_sources if source.name == CONCLUSION],
            [],
        )
        for fact_id in (self.inst_fact, self.priv_fact):
            self.assertEqual(_p2_row(corrected, fact_id)["disposition"], "inapplicable")
            self.assertIn(P2_ENROL_LATER, _input_ids(_pins(_p2_row(corrected, fact_id))))
        corrected.evaluate_subject_scoped_rule(subject_type=BOX1, rule=self.conclusion_rule)

        for fact_id, box_finding in (
            (self.north_fact, P2_BOX_NORTH),
            (self.south_fact, P2_BOX_SOUTH),
        ):
            with self.subTest(statement=fact_id):
                before = _p2_row(favourable, fact_id)
                after = _p2_row(corrected, fact_id)
                self.assertEqual(before["disposition"], "blocked")
                self.assertEqual(before["code"], "DEPENDENCY_ABSENT")
                self.assertEqual(before["missing"], [CONCLUSION])
                self.assertEqual(_input_ids(_pins(before)), {box_finding})
                self.assertEqual(after["disposition"], "blocked")
                self.assertEqual(after["code"], "DEPENDENCY_ABSENT")
                self.assertEqual(after["missing"], [CONCLUSION])
                self.assertEqual(_input_ids(_pins(after)), {box_finding})
                for enrolment_finding in (P2_ENROL_EARLIER, P2_ENROL_LATER):
                    self.assertNotIn(enrolment_finding, _input_ids(_pins(before)))
                    self.assertNotIn(enrolment_finding, _input_ids(_pins(after)))
                self.assertNotIn(self.inst_fact, before["symbol"])
                self.assertNotEqual(before["disposition"], "inapplicable")
                self.assertNotEqual(after["disposition"], "inapplicable")


# --- Track 2. Keyed same-run sources, one hop at a time, out to the statement. ---

T2_PARAM = "demo.parameter.enrolment-default"
STATUS = "demo.tax.schooling-status"
LINK_CONSEQUENCE = "demo.tax.link-consequence"
STATEMENT_AMOUNT = "demo.tax.statement-facing-amount"
T2_STATUS_RULE = "demo.rule.schooling-status"
T2_LINK_RULE = "demo.rule.link-consequence"
T2_AMOUNT_RULE = "demo.rule.statement-facing-amount"
T2_LENDER_WEST = "demo.lender.west"
STATEMENT_S3 = "demo.statement.s3"
STATEMENT_MISSING = "demo.statement.missing"
T2_FIN_INST = "demo.finding.financing.institutional"
T2_FIN_PRIV = "demo.finding.financing.private"
T2_ENROL_EARLIER = "demo.finding.enrolment.1-not-adverse"
T2_ENROL_LATER = "demo.finding.enrolment.2-adverse"
T2_BOX_NORTH = "demo.finding.box1.north"
T2_BOX_SOUTH = "demo.finding.box1.south"
T2_BOX_WEST = "demo.finding.box1.west"
T2_LINK_NORTH = "demo.finding.link.north"
T2_LINK_SOUTH = "demo.finding.link.south"
T2_LINK_WEST = "demo.finding.link.west"
T2_LINK_MISSING = "demo.finding.link.missing"
T2_LINK_SPLIT = "demo.finding.link.north-private"


def _t2_eq(name: str, fact_type: str, value: str) -> dict[str, Any]:
    return {
        "op": "categorical_compare",
        "left": {"op": "ref", "name": name},
        "right": {
            "op": "category_literal",
            "fact_type": {"id": fact_type, "version": "v1"},
            "value": value,
        },
        "cmp": "eq",
    }


def _t2_rule(
    *,
    rule_id: str,
    citation_id: str,
    role: str,
    requires: list[str],
    when: dict[str, Any],
    value: Any,
    publishes: str,
) -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v6",
        "id": rule_id,
        "version": "v1",
        "role": role,
        "requires": requires,
        "when": when,
        "value": value,
        "publishes": publishes,
        "citations": [{"id": citation_id, "version": "v1"}],
    }


def _t2_rules() -> list[dict[str, Any]]:
    return [
        _t2_rule(
            rule_id=T2_STATUS_RULE,
            citation_id="demo.citation.schooling-status",
            role="applicability",
            requires=[FINANCING, ENROLMENT],
            when=_t2_eq(FINANCING, FINANCING, "tuition"),
            value={"op": "ref", "name": ENROLMENT},
            publishes=STATUS,
        ),
        _t2_rule(
            rule_id=T2_LINK_RULE,
            citation_id="demo.citation.link-consequence",
            role="applicability",
            requires=[STATEMENT_BORROWING, STATUS],
            when=_t2_eq(STATEMENT_BORROWING, STATEMENT_BORROWING, "reported"),
            value={"op": "ref", "name": STATUS},
            publishes=LINK_CONSEQUENCE,
        ),
        _t2_rule(
            rule_id=T2_AMOUNT_RULE,
            citation_id="demo.citation.statement-facing-amount",
            role="computation",
            requires=[BOX1, LINK_CONSEQUENCE],
            when={
                "op": "compare",
                "cmp": "gt",
                "left": {"op": "ref", "name": BOX1},
                "right": 0,
            },
            value={
                "op": "choose",
                "when": _t2_eq(LINK_CONSEQUENCE, LINK_CONSEQUENCE, "adverse"),
                "then": 0,
                "else": {"op": "ref", "name": BOX1},
            },
            publishes=STATEMENT_AMOUNT,
        ),
    ]


def _t2_fact_types() -> list[dict[str, Any]]:
    return [
        {"id": FINANCING, "version": "v1", "value_schema": {"enum": ["tuition"]}},
        {
            "id": ENROLMENT,
            "version": "v1",
            "value_schema": {"enum": ["adverse", "not-adverse"]},
            "optional_default": {"parameter": {"id": T2_PARAM, "version": "v1"}},
        },
        {
            "id": STATEMENT_BORROWING,
            "version": "v1",
            "value_schema": {"enum": ["reported"]},
        },
        {
            "id": STATUS,
            "version": "v1",
            "value_schema": {"enum": ["adverse", "not-adverse"]},
        },
        {
            "id": LINK_CONSEQUENCE,
            "version": "v1",
            "value_schema": {"enum": ["adverse", "not-adverse"]},
        },
    ]


def _t2_lattice() -> dict[str, dict[str, Any]]:
    borrowings = (P2_BORROWING_INST, P2_BORROWING_PRIV)
    periods = (PERIOD_AUTUMN, PERIOD_SPRING)
    lenders = (LENDER, P2_LENDER_SOUTH, T2_LENDER_WEST)
    statements = (STATEMENT_S1, STATEMENT_S2, STATEMENT_S3, STATEMENT_MISSING)
    return {
        FINANCING: _p2_literal(FINANCING, (
            ("borrowing", borrowings),
            ("period", periods),
            ("institution", (INSTITUTION,)),
            ("programme", (PROGRAMME,)),
        )),
        ENROLMENT: _p2_literal(ENROLMENT, (
            ("period", periods),
            ("institution", (INSTITUTION,)),
            ("programme", (PROGRAMME,)),
        )),
        BOX1: _p2_literal(BOX1, (
            ("lender", lenders),
            ("statement", statements),
            ("tax-year", (YEAR,)),
        )),
        STATEMENT_BORROWING: _p2_literal(STATEMENT_BORROWING, (
            ("lender", lenders),
            ("statement", statements),
            ("tax-year", (YEAR,)),
            ("borrowing", borrowings),
        )),
    }


def _t2_financing_fact_id(borrowing: str, period: str) -> str:
    return fact_id_for(
        FINANCING,
        (
            ("borrowing", borrowing),
            ("period", period),
            ("institution", INSTITUTION),
            ("programme", PROGRAMME),
        ),
    )


def _t2_enrolment_fact_id() -> str:
    return fact_id_for(
        ENROLMENT,
        (
            ("period", PERIOD_AUTUMN),
            ("institution", INSTITUTION),
            ("programme", PROGRAMME),
        ),
    )


def _t2_box_fact_id(lender: str, statement: str) -> str:
    return fact_id_for(
        BOX1,
        (("lender", lender), ("statement", statement), ("tax-year", YEAR)),
    )


def _t2_link_fact_id(lender: str, statement: str, borrowing: str) -> str:
    return fact_id_for(
        STATEMENT_BORROWING,
        (
            ("lender", lender),
            ("statement", statement),
            ("tax-year", YEAR),
            ("borrowing", borrowing),
        ),
    )


def _t2_default_id(ctx: RunContext) -> str:
    pins = _sorted_pins([
        ctx.adoption_pin,
        *ctx.governance_pins,
        {"role": "parameter", "id": T2_PARAM, "version": "v1"},
    ])
    body = {
        "symbol": ENROLMENT,
        "value": _value_str(ctx.parameters[T2_PARAM]["values"]),
        "pins": pins,
        "resolved_input": {"fact_id": ENROLMENT, "origin": "declared_default"},
    }
    return _content_id("finding:derived:", body)


def _t2_symbol(publishes: str, fact_id: str) -> str:
    return f"{publishes}|{fact_id}"


def _t2_finding(run: _Run, publishes: str, fact_id: str) -> dict[str, Any]:
    symbol = _t2_symbol(publishes, fact_id)
    matches = [pub.finding for pub in run.publications if pub.finding["symbol"] == symbol]
    if len(matches) != 1:
        raise AssertionError(
            f"{symbol}: {[pub.finding['symbol'] for pub in run.publications]!r}"
        )
    return matches[0]


def _t2_row(run: _Run, fact_id: str, publishes: str) -> dict[str, Any]:
    symbol = _t2_symbol(publishes, fact_id)
    rows = [row for row in run.dispositions if row.get("symbol") == symbol]
    if len(rows) != 1:
        raise AssertionError(f"{symbol}: {run.dispositions!r}")
    return rows[0]


def _t2_canonical(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _t2_walk(run: _Run, finding: dict[str, Any]) -> set[str]:
    by_id = {pub.finding["id"]: pub.finding for pub in run.publications}
    seen: set[str] = set()
    stack = [finding]
    while stack:
        current = stack.pop()
        for pin in current["pins"]:
            if pin.get("role") != "input":
                continue
            fid = str(pin["id"])
            if fid in seen:
                continue
            seen.add(fid)
            nxt = by_id.get(fid)
            if nxt is not None:
                stack.append(nxt)
    return seen


def _t2_execute(
    findings: dict[str, dict[str, Any]],
) -> tuple[FindingState, CurrencyView, RunContext, _Run]:
    state = FindingState(
        findings=dict(findings),
        fact_state=KernelState(fact_types=_t2_lattice()),
    )
    currency = compute_currency(state)
    rules = _t2_rules()
    ctx = marshal_run_context(
        run_id="demo.sli-a4-pass2-track2",
        state=state,
        currency=currency,
        rules=rules,
        parameters={T2_PARAM: {"id": T2_PARAM, "version": "v1", "values": "not-adverse"}},
        canon={},
        adoption_pin=ADOPTION_PIN,
        governance_pins=GOVERNANCE_PINS,
        fact_types=_t2_fact_types(),
        input_bindings=[{
            "symbol": ENROLMENT,
            "fact_type": {"id": ENROLMENT, "version": "v1"},
            "mode": "optional_default",
        }],
        collect_source_names=[FINANCING, ENROLMENT, BOX1, STATEMENT_BORROWING],
    )
    run = _Run(ctx, SCHEMAS)
    by_id = {rule["id"]: rule for rule in rules}
    run.evaluate_subject_scoped_rule(subject_type=FINANCING, rule=by_id[T2_STATUS_RULE])
    run.evaluate_subject_scoped_rule(
        subject_type=STATEMENT_BORROWING, rule=by_id[T2_LINK_RULE]
    )
    run.evaluate_subject_scoped_rule(subject_type=BOX1, rule=by_id[T2_AMOUNT_RULE])
    return state, currency, ctx, run


def _t2_chain_findings(*, corrected: bool, dangling: bool) -> dict[str, dict[str, Any]]:
    # Enrolment findings, when present, stay in record order: the earlier
    # not-adverse answer is inserted before the later adverse one.
    findings = {
        T2_FIN_INST: _finding(
            T2_FIN_INST,
            _t2_financing_fact_id(P2_BORROWING_INST, PERIOD_AUTUMN),
            "tuition",
        ),
        T2_FIN_PRIV: _finding(
            T2_FIN_PRIV,
            _t2_financing_fact_id(P2_BORROWING_PRIV, PERIOD_SPRING),
            "tuition",
        ),
        T2_BOX_NORTH: _finding(
            T2_BOX_NORTH, _t2_box_fact_id(LENDER, STATEMENT_S1), 1500
        ),
        T2_BOX_SOUTH: _finding(
            T2_BOX_SOUTH, _t2_box_fact_id(P2_LENDER_SOUTH, STATEMENT_S2), 800
        ),
        T2_BOX_WEST: _finding(
            T2_BOX_WEST, _t2_box_fact_id(T2_LENDER_WEST, STATEMENT_S3), 400
        ),
        T2_LINK_NORTH: _finding(
            T2_LINK_NORTH,
            _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_INST),
            "reported",
        ),
        T2_LINK_SOUTH: _finding(
            T2_LINK_SOUTH,
            _t2_link_fact_id(P2_LENDER_SOUTH, STATEMENT_S2, P2_BORROWING_INST),
            "reported",
        ),
        T2_LINK_WEST: _finding(
            T2_LINK_WEST,
            _t2_link_fact_id(T2_LENDER_WEST, STATEMENT_S3, P2_BORROWING_PRIV),
            "reported",
        ),
    }
    if corrected:
        enrol = _t2_enrolment_fact_id()
        findings[T2_ENROL_EARLIER] = _finding(T2_ENROL_EARLIER, enrol, "not-adverse")
        findings[T2_ENROL_LATER] = _finding(T2_ENROL_LATER, enrol, "adverse")
    if dangling:
        findings[T2_LINK_MISSING] = _finding(
            T2_LINK_MISSING,
            _t2_link_fact_id(LENDER, STATEMENT_MISSING, P2_BORROWING_INST),
            "reported",
        )
    return findings


def _t2_split_findings(*, adverse: bool) -> dict[str, dict[str, Any]]:
    """One statement, two links, two borrowings. Statuses agree or differ."""
    findings = {
        T2_FIN_INST: _finding(
            T2_FIN_INST,
            _t2_financing_fact_id(P2_BORROWING_INST, PERIOD_AUTUMN),
            "tuition",
        ),
        T2_FIN_PRIV: _finding(
            T2_FIN_PRIV,
            _t2_financing_fact_id(P2_BORROWING_PRIV, PERIOD_SPRING),
            "tuition",
        ),
        T2_BOX_NORTH: _finding(
            T2_BOX_NORTH, _t2_box_fact_id(LENDER, STATEMENT_S1), 1500
        ),
        T2_LINK_NORTH: _finding(
            T2_LINK_NORTH,
            _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_INST),
            "reported",
        ),
        T2_LINK_SPLIT: _finding(
            T2_LINK_SPLIT,
            _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_PRIV),
            "reported",
        ),
    }
    if adverse:
        findings[T2_ENROL_LATER] = _finding(
            T2_ENROL_LATER, _t2_enrolment_fact_id(), "adverse"
        )
    return findings


class KeyedSameRunStatementChain(unittest.TestCase):
    """Status, link consequence, then the statement amount. Three dispatches.

    The institutional borrowing is autumn, so the autumn enrolment joins it.
    The private borrowing is spring, so that enrolment does not. North and
    south are two statements on the institutional borrowing. West is the
    private borrowing's statement.
    """

    def setUp(self) -> None:
        self.inst = _t2_financing_fact_id(P2_BORROWING_INST, PERIOD_AUTUMN)
        self.priv = _t2_financing_fact_id(P2_BORROWING_PRIV, PERIOD_SPRING)
        self.north = _t2_box_fact_id(LENDER, STATEMENT_S1)
        self.south = _t2_box_fact_id(P2_LENDER_SOUTH, STATEMENT_S2)
        self.west = _t2_box_fact_id(T2_LENDER_WEST, STATEMENT_S3)
        self.link_north = _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_INST)
        self.link_south = _t2_link_fact_id(
            P2_LENDER_SOUTH, STATEMENT_S2, P2_BORROWING_INST
        )
        self.link_west = _t2_link_fact_id(T2_LENDER_WEST, STATEMENT_S3, P2_BORROWING_PRIV)
        self.link_missing = _t2_link_fact_id(
            LENDER, STATEMENT_MISSING, P2_BORROWING_INST
        )
        self.enrol = _t2_enrolment_fact_id()
        self.assertLess(T2_ENROL_EARLIER, T2_ENROL_LATER)
        self.assertNotEqual(self.inst, self.priv)
        self.assertNotIn("borrowing=", self.enrol)
        self.assertIn(f"period={PERIOD_AUTUMN}", self.inst)
        self.assertIn(f"period={PERIOD_AUTUMN}", self.enrol)
        self.assertIn(f"period={PERIOD_SPRING}", self.priv)

    def test_favourable_path_publishes_each_reported_amount_and_pins_the_default(self) -> None:
        """No enrolment finding. Each statement publishes its reported amount.

        The pin walk reaches that statement's link consequence, the financing
        status, and the declared not-adverse default. It does not reach an
        enrolment finding.
        """
        state, currency, ctx, run = _t2_execute(
            _t2_chain_findings(corrected=False, dangling=False)
        )
        self.assertNotIn(T2_ENROL_EARLIER, state.findings)
        self.assertNotIn(T2_ENROL_LATER, state.findings)
        self.assertEqual(currency.displaced_finding_ids, frozenset())
        self.assertEqual(
            [source for source in ctx.sources if source.name == ENROLMENT],
            [],
        )
        default_id = _t2_default_id(ctx)
        statements = (
            (self.north, T2_BOX_NORTH, self.link_north, self.inst, "1500"),
            (self.south, T2_BOX_SOUTH, self.link_south, self.inst, "800"),
            (self.west, T2_BOX_WEST, self.link_west, self.priv, "400"),
        )
        for box_fact, box_finding, link_fact, financing_fact, amount in statements:
            with self.subTest(statement=box_fact):
                finding = _t2_finding(run, STATEMENT_AMOUNT, box_fact)
                status = _t2_finding(run, STATUS, financing_fact)
                link = _t2_finding(run, LINK_CONSEQUENCE, link_fact)
                self.assertEqual(
                    _t2_row(run, box_fact, STATEMENT_AMOUNT)["disposition"], "published"
                )
                self.assertEqual(finding["value"], amount)
                self.assertEqual(status["value"], "not-adverse")
                self.assertEqual(
                    _t2_row(run, financing_fact, STATUS)["disposition"], "published"
                )
                self.assertEqual(link["value"], "not-adverse")
                walk = _t2_walk(run, finding)
                self.assertIn(link["id"], walk)
                self.assertIn(status["id"], walk)
                self.assertIn(default_id, walk)
                self.assertIn(box_finding, walk)
                self.assertEqual(
                    next(
                        pin["origin"]
                        for pin in status["pins"]
                        if pin["role"] == "input" and pin["id"] == default_id
                    ),
                    "declared_default",
                )
                self.assertNotIn(T2_ENROL_EARLIER, walk)
                self.assertNotIn(T2_ENROL_LATER, walk)

    def test_corrected_adverse_path_publishes_a_changed_amount(self) -> None:
        """A later adverse finding displaces the earlier one. The amount changes.

        The affected statement publishes zero, not a block. Its pin walk
        reaches the corrected enrolment finding and not the displaced one.
        """
        _before_state, _before_currency, before_ctx, before = _t2_execute(
            _t2_chain_findings(corrected=False, dangling=False)
        )
        state, currency, ctx, run = _t2_execute(
            _t2_chain_findings(corrected=True, dangling=False)
        )
        self.assertIn(T2_ENROL_EARLIER, state.findings)
        self.assertIn(T2_ENROL_LATER, state.findings)
        self.assertEqual(currency.displaced_finding_ids, frozenset({T2_ENROL_EARLIER}))
        self.assertIn(T2_ENROL_LATER, currency.current_finding_ids)
        self.assertEqual(
            [(reason.kind, reason.by) for reason in currency.reasons[T2_ENROL_EARLIER]],
            [("correction", T2_ENROL_LATER)],
        )
        self.assertEqual(
            {source.finding_id for source in ctx.sources if source.name == ENROLMENT},
            {T2_ENROL_LATER},
        )
        self.assertNotIn(
            T2_ENROL_EARLIER,
            {source.finding_id for source in ctx.sources},
        )
        before_finding = _t2_finding(before, STATEMENT_AMOUNT, self.north)
        finding = _t2_finding(run, STATEMENT_AMOUNT, self.north)
        row = _t2_row(run, self.north, STATEMENT_AMOUNT)
        status = _t2_finding(run, STATUS, self.inst)
        link = _t2_finding(run, LINK_CONSEQUENCE, self.link_north)
        self.assertEqual(before_finding["value"], "1500")
        self.assertEqual(finding["value"], "0")
        self.assertNotEqual(finding["value"], before_finding["value"])
        self.assertEqual(row["disposition"], "published")
        self.assertNotEqual(row["disposition"], "blocked")
        self.assertNotEqual(row["disposition"], "inapplicable")
        self.assertEqual(status["value"], "adverse")
        self.assertEqual(_t2_row(run, self.inst, STATUS)["disposition"], "published")
        self.assertEqual(link["value"], "adverse")
        walk = _t2_walk(run, finding)
        self.assertIn(link["id"], walk)
        self.assertIn(status["id"], walk)
        self.assertIn(T2_ENROL_LATER, walk)
        self.assertNotIn(T2_ENROL_EARLIER, walk)
        self.assertNotIn(_t2_default_id(before_ctx), walk)
        self.assertNotIn(T2_ENROL_EARLIER, _input_ids(_pins(status)))
        self.assertIn(T2_ENROL_LATER, _input_ids(_pins(status)))

    def test_servicer_transfer_both_statements_follow_the_correction(self) -> None:
        """Two statements on the corrected borrowing both publish zero.

        Each walk reaches the corrected enrolment finding and not the
        displaced one. Each favourable amount was that statement's own
        reported amount.
        """
        _before_state, _before_currency, _before_ctx, before = _t2_execute(
            _t2_chain_findings(corrected=False, dangling=False)
        )
        _state, _currency, _ctx, run = _t2_execute(
            _t2_chain_findings(corrected=True, dangling=False)
        )
        for box_fact, link_fact, reported in (
            (self.north, self.link_north, "1500"),
            (self.south, self.link_south, "800"),
        ):
            with self.subTest(statement=box_fact):
                before_finding = _t2_finding(before, STATEMENT_AMOUNT, box_fact)
                finding = _t2_finding(run, STATEMENT_AMOUNT, box_fact)
                self.assertEqual(before_finding["value"], reported)
                self.assertEqual(finding["value"], "0")
                self.assertEqual(
                    _t2_row(run, box_fact, STATEMENT_AMOUNT)["disposition"], "published"
                )
                walk = _t2_walk(run, finding)
                self.assertIn(_t2_finding(run, LINK_CONSEQUENCE, link_fact)["id"], walk)
                self.assertIn(_t2_finding(run, STATUS, self.inst)["id"], walk)
                self.assertIn(T2_ENROL_LATER, walk)
                self.assertNotIn(T2_ENROL_EARLIER, walk)

    def test_statement_linked_to_an_unaffected_borrowing_is_byte_identical(self) -> None:
        """Spring does not join the autumn enrolment. West's finding is unchanged.

        The institutional statement changes in the same pair of runs, so the
        identical bytes are not a run that ignored the correction.
        """
        _before_state, _before_currency, _before_ctx, before = _t2_execute(
            _t2_chain_findings(corrected=False, dangling=False)
        )
        _after_state, _after_currency, _after_ctx, after = _t2_execute(
            _t2_chain_findings(corrected=True, dangling=False)
        )
        before_finding = _t2_finding(before, STATEMENT_AMOUNT, self.west)
        after_finding = _t2_finding(after, STATEMENT_AMOUNT, self.west)
        self.assertEqual(before_finding["value"], "400")
        self.assertEqual(_t2_canonical(before_finding), _t2_canonical(after_finding))
        self.assertEqual(
            _t2_canonical(_t2_row(before, self.west, STATEMENT_AMOUNT)),
            _t2_canonical(_t2_row(after, self.west, STATEMENT_AMOUNT)),
        )
        self.assertEqual(
            _t2_finding(before, STATUS, self.priv)["value"],
            _t2_finding(after, STATUS, self.priv)["value"],
        )
        self.assertNotEqual(
            _t2_finding(before, STATEMENT_AMOUNT, self.north)["value"],
            _t2_finding(after, STATEMENT_AMOUNT, self.north)["value"],
        )

    def test_link_naming_a_statement_that_does_not_exist_changes_no_statement(self) -> None:
        """The dangling link publishes. No statement's bytes or pin walk include it."""
        _plain_state, _plain_currency, _plain_ctx, plain = _t2_execute(
            _t2_chain_findings(corrected=False, dangling=False)
        )
        _state, _currency, ctx, run = _t2_execute(
            _t2_chain_findings(corrected=False, dangling=True)
        )
        self.assertNotIn(
            self.link_missing,
            {source.fact_id for source in ctx.sources if source.name == BOX1},
        )
        link = _t2_finding(run, LINK_CONSEQUENCE, self.link_missing)
        self.assertEqual(
            _t2_row(run, self.link_missing, LINK_CONSEQUENCE)["disposition"],
            "published",
        )
        for box_fact in (self.north, self.south, self.west):
            with self.subTest(statement=box_fact):
                self.assertEqual(
                    _t2_canonical(_t2_finding(plain, STATEMENT_AMOUNT, box_fact)),
                    _t2_canonical(_t2_finding(run, STATEMENT_AMOUNT, box_fact)),
                )
                self.assertNotIn(
                    link["id"],
                    _t2_walk(run, _t2_finding(run, STATEMENT_AMOUNT, box_fact)),
                )


class ObservedScalarJoin(unittest.TestCase):
    """One statement, two borrowings. Observed, not solved.

    Equal status values: the scalar join publishes once and pins the
    sort-first link consequence. Differing values: it blocks
    ``DEPENDENCY_INVALID`` and publishes nothing for that statement.
    """

    def test_one_statement_over_two_borrowings_selects_one_equal_value_or_blocks(self) -> None:
        box = _t2_box_fact_id(LENDER, STATEMENT_S1)
        link_inst = _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_INST)
        link_priv = _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_PRIV)
        self.assertNotEqual(link_inst, link_priv)

        _equal_state, _equal_currency, _equal_ctx, equal = _t2_execute(
            _t2_split_findings(adverse=False)
        )
        inst_link = _t2_finding(equal, LINK_CONSEQUENCE, link_inst)
        priv_link = _t2_finding(equal, LINK_CONSEQUENCE, link_priv)
        self.assertEqual(inst_link["value"], "not-adverse")
        self.assertEqual(priv_link["value"], "not-adverse")
        joined = [
            source for source in equal.live_sources
            if source.name == LINK_CONSEQUENCE and source.fact_id in {link_inst, link_priv}
        ]
        self.assertEqual({source.fact_id for source in joined}, {link_inst, link_priv})
        self.assertEqual({source.value for source in joined}, {"not-adverse"})
        chosen = min(joined, key=lambda source: source.finding_id)
        other = next(source for source in joined if source.finding_id != chosen.finding_id)
        published = _t2_finding(equal, STATEMENT_AMOUNT, box)
        self.assertEqual(published["value"], "1500")
        self.assertEqual(
            _t2_row(equal, box, STATEMENT_AMOUNT)["disposition"], "published"
        )
        self.assertEqual(
            _input_ids(_pins(published)),
            {T2_BOX_NORTH, chosen.finding_id},
        )
        self.assertNotIn(other.finding_id, _input_ids(_pins(published)))

        _state, currency, ctx, differing = _t2_execute(_t2_split_findings(adverse=True))
        self.assertEqual(currency.displaced_finding_ids, frozenset())
        self.assertEqual(
            {source.finding_id for source in ctx.sources if source.name == ENROLMENT},
            {T2_ENROL_LATER},
        )
        inst_fact = _t2_financing_fact_id(P2_BORROWING_INST, PERIOD_AUTUMN)
        priv_fact = _t2_financing_fact_id(P2_BORROWING_PRIV, PERIOD_SPRING)
        self.assertEqual(_t2_finding(differing, STATUS, inst_fact)["value"], "adverse")
        self.assertEqual(_t2_finding(differing, STATUS, priv_fact)["value"], "not-adverse")
        self.assertEqual(_t2_finding(differing, LINK_CONSEQUENCE, link_inst)["value"], "adverse")
        self.assertEqual(
            _t2_finding(differing, LINK_CONSEQUENCE, link_priv)["value"], "not-adverse"
        )
        row = _t2_row(differing, box, STATEMENT_AMOUNT)
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "DEPENDENCY_INVALID")
        self.assertEqual(row["missing"], sorted([link_inst, link_priv]))
        self.assertNotIn(
            _t2_symbol(STATEMENT_AMOUNT, box),
            {pub.finding["symbol"] for pub in differing.publications},
        )
        self.assertNotEqual(row["disposition"], "published")
        self.assertNotEqual(row["disposition"], "inapplicable")


# --- P3. Partial reduction: collected link portions, one statement. ---

P3_LINK_PORTION = "demo.tax.link-portion"
P3_LINK_RULE = "demo.rule.link-portion"
P3_AMOUNT_RULE = "demo.rule.statement-portion-sum"
P3_LINK_INST = "demo.finding.link.p3-inst"
P3_LINK_PRIV = "demo.finding.link.p3-priv"
P3_LINK_SOUTH = "demo.finding.link.p3-south"
P3_MEMBERSHIP = "included"


def _p3_fact_types() -> list[dict[str, Any]]:
    # The link value is the portion, a number, or the membership token.
    # No enum: a categorical domain would reject both shapes on ref.
    return [
        {"id": FINANCING, "version": "v1", "value_schema": {"enum": ["tuition"]}},
        {
            "id": ENROLMENT,
            "version": "v1",
            "value_schema": {"enum": ["adverse", "not-adverse"]},
            "optional_default": {"parameter": {"id": T2_PARAM, "version": "v1"}},
        },
        {"id": STATEMENT_BORROWING, "version": "v1", "value_schema": {"type": "number"}},
        {
            "id": STATUS,
            "version": "v1",
            "value_schema": {"enum": ["adverse", "not-adverse"]},
        },
    ]


def _p3_rules() -> list[dict[str, Any]]:
    return [
        _t2_rule(
            rule_id=T2_STATUS_RULE,
            citation_id="demo.citation.schooling-status",
            role="applicability",
            requires=[FINANCING, ENROLMENT],
            when=_t2_eq(FINANCING, FINANCING, "tuition"),
            value={"op": "ref", "name": ENROLMENT},
            publishes=STATUS,
        ),
        _t2_rule(
            rule_id=P3_LINK_RULE,
            citation_id="demo.citation.link-portion",
            role="computation",
            requires=[STATEMENT_BORROWING, STATUS],
            when={
                "op": "any",
                "args": [
                    _t2_eq(STATUS, STATUS, "adverse"),
                    _t2_eq(STATUS, STATUS, "not-adverse"),
                ],
            },
            value={
                "op": "choose",
                "when": _t2_eq(STATUS, STATUS, "adverse"),
                "then": 0,
                "else": {"op": "ref", "name": STATEMENT_BORROWING},
            },
            publishes=P3_LINK_PORTION,
        ),
        _t2_rule(
            rule_id=P3_AMOUNT_RULE,
            citation_id="demo.citation.statement-portion-sum",
            role="computation",
            requires=[BOX1],
            when={
                "op": "compare",
                "cmp": "gt",
                "left": {"op": "ref", "name": BOX1},
                "right": 0,
            },
            value={
                "op": "add",
                "args": [{"op": "collect", "name": P3_LINK_PORTION}],
            },
            publishes=STATEMENT_AMOUNT,
        ),
    ]


def _p3_findings(
    *,
    corrected: bool,
    inst_portion: Any = 1000,
    priv_portion: Any = 500,
) -> dict[str, dict[str, Any]]:
    # Enrolment findings stay in record order when present: earlier
    # not-adverse, then the later adverse correction.
    findings = {
        T2_FIN_INST: _finding(
            T2_FIN_INST,
            _t2_financing_fact_id(P2_BORROWING_INST, PERIOD_AUTUMN),
            "tuition",
        ),
        T2_FIN_PRIV: _finding(
            T2_FIN_PRIV,
            _t2_financing_fact_id(P2_BORROWING_PRIV, PERIOD_SPRING),
            "tuition",
        ),
        T2_BOX_NORTH: _finding(
            T2_BOX_NORTH, _t2_box_fact_id(LENDER, STATEMENT_S1), 1500
        ),
        T2_BOX_SOUTH: _finding(
            T2_BOX_SOUTH, _t2_box_fact_id(P2_LENDER_SOUTH, STATEMENT_S2), 800
        ),
        T2_BOX_WEST: _finding(
            T2_BOX_WEST, _t2_box_fact_id(T2_LENDER_WEST, STATEMENT_S3), 400
        ),
        P3_LINK_INST: _finding(
            P3_LINK_INST,
            _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_INST),
            inst_portion,
        ),
        P3_LINK_PRIV: _finding(
            P3_LINK_PRIV,
            _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_PRIV),
            priv_portion,
        ),
        P3_LINK_SOUTH: _finding(
            P3_LINK_SOUTH,
            _t2_link_fact_id(P2_LENDER_SOUTH, STATEMENT_S2, P2_BORROWING_PRIV),
            800,
        ),
    }
    if corrected:
        enrol = _t2_enrolment_fact_id()
        findings[T2_ENROL_EARLIER] = _finding(T2_ENROL_EARLIER, enrol, "not-adverse")
        findings[T2_ENROL_LATER] = _finding(T2_ENROL_LATER, enrol, "adverse")
    return findings


def _p3_execute(
    findings: dict[str, dict[str, Any]],
) -> tuple[FindingState, CurrencyView, RunContext, _Run]:
    state = FindingState(
        findings=dict(findings),
        fact_state=KernelState(fact_types=_t2_lattice()),
    )
    currency = compute_currency(state)
    rules = _p3_rules()
    ctx = marshal_run_context(
        run_id="demo.sli-a4-pass2-p3",
        state=state,
        currency=currency,
        rules=rules,
        parameters={T2_PARAM: {"id": T2_PARAM, "version": "v1", "values": "not-adverse"}},
        canon={},
        adoption_pin=ADOPTION_PIN,
        governance_pins=GOVERNANCE_PINS,
        fact_types=_p3_fact_types(),
        input_bindings=[{
            "symbol": ENROLMENT,
            "fact_type": {"id": ENROLMENT, "version": "v1"},
            "mode": "optional_default",
        }],
        collect_source_names=[FINANCING, ENROLMENT, BOX1, STATEMENT_BORROWING],
    )
    run = _Run(ctx, SCHEMAS)
    by_id = {rule["id"]: rule for rule in rules}
    run.evaluate_subject_scoped_rule(subject_type=FINANCING, rule=by_id[T2_STATUS_RULE])
    run.evaluate_subject_scoped_rule(
        subject_type=STATEMENT_BORROWING, rule=by_id[P3_LINK_RULE]
    )
    run.evaluate_subject_scoped_rule(subject_type=BOX1, rule=by_id[P3_AMOUNT_RULE])
    return state, currency, ctx, run


class CollectedPortionReduction(unittest.TestCase):
    """One statement, two route-(b) portions, summed with ``collect``.

    North's box is 1500: 1000 on the institutional borrowing, 500 on the
    private one. The institutional enrolment is autumn, so a correction
    there reaches only that portion. South is the private borrowing's own
    statement. West has a box and no link.
    """

    def setUp(self) -> None:
        self.north = _t2_box_fact_id(LENDER, STATEMENT_S1)
        self.south = _t2_box_fact_id(P2_LENDER_SOUTH, STATEMENT_S2)
        self.west = _t2_box_fact_id(T2_LENDER_WEST, STATEMENT_S3)
        self.link_inst = _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_INST)
        self.link_priv = _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_PRIV)
        self.link_south = _t2_link_fact_id(
            P2_LENDER_SOUTH, STATEMENT_S2, P2_BORROWING_PRIV
        )
        self.inst = _t2_financing_fact_id(P2_BORROWING_INST, PERIOD_AUTUMN)
        self.priv = _t2_financing_fact_id(P2_BORROWING_PRIV, PERIOD_SPRING)
        self.enrol = _t2_enrolment_fact_id()
        amount = next(rule for rule in _p3_rules() if rule["id"] == P3_AMOUNT_RULE)
        collected = amount["value"]["args"][0]
        self.assertNotIn(P3_LINK_PORTION, amount["requires"])
        self.assertEqual(collected["op"], "collect")
        self.assertNotIn("source_set", collected)
        self.assertNotEqual(self.link_inst, self.link_priv)

    def test_joined_portions_sum_and_every_link_is_pinned(self) -> None:
        """Before the correction the statement publishes 1500. After, 500.

        Both link portions are pinned each time, including once their values
        disagree. The walk reaches the institutional chain and the private
        chain, and not the other statement's link.
        """
        _before_state, before_currency, before_ctx, before = _p3_execute(
            _p3_findings(corrected=False)
        )
        state, currency, ctx, run = _p3_execute(_p3_findings(corrected=True))
        self.assertEqual(before_currency.displaced_finding_ids, frozenset())
        self.assertIn(T2_ENROL_EARLIER, state.findings)
        self.assertIn(T2_ENROL_LATER, state.findings)
        self.assertEqual(currency.displaced_finding_ids, frozenset({T2_ENROL_EARLIER}))
        self.assertIn(T2_ENROL_LATER, currency.current_finding_ids)
        self.assertEqual(
            [(reason.kind, reason.by) for reason in currency.reasons[T2_ENROL_EARLIER]],
            [("correction", T2_ENROL_LATER)],
        )
        self.assertEqual(
            {source.finding_id for source in ctx.sources if source.name == ENROLMENT},
            {T2_ENROL_LATER},
        )
        default_id = _t2_default_id(before_ctx)
        self.assertEqual(default_id, _t2_default_id(ctx))

        before_inst = _t2_finding(before, P3_LINK_PORTION, self.link_inst)
        before_priv = _t2_finding(before, P3_LINK_PORTION, self.link_priv)
        inst_portion = _t2_finding(run, P3_LINK_PORTION, self.link_inst)
        priv_portion = _t2_finding(run, P3_LINK_PORTION, self.link_priv)
        south_portion = _t2_finding(run, P3_LINK_PORTION, self.link_south)
        self.assertEqual(before_inst["value"], "1000")
        self.assertEqual(before_priv["value"], "500")
        self.assertEqual(inst_portion["value"], "0")
        self.assertEqual(priv_portion["value"], "500")
        self.assertNotEqual(inst_portion["value"], priv_portion["value"])
        carried = next(
            source for source in run.live_sources
            if source.name == P3_LINK_PORTION and source.fact_id == self.link_inst
        )
        self.assertEqual(
            dict(carried.keys or ()),
            {
                "lender": LENDER,
                "statement": STATEMENT_S1,
                "tax-year": YEAR,
                "borrowing": P2_BORROWING_INST,
            },
        )

        before_amount = _t2_finding(before, STATEMENT_AMOUNT, self.north)
        amount = _t2_finding(run, STATEMENT_AMOUNT, self.north)
        self.assertEqual(before_amount["value"], "1500")
        self.assertEqual(amount["value"], "500")
        self.assertEqual(
            _t2_row(run, self.north, STATEMENT_AMOUNT)["disposition"], "published"
        )
        self.assertEqual(
            _input_ids(_pins(before_amount)),
            {T2_BOX_NORTH, before_inst["id"], before_priv["id"]},
        )
        self.assertEqual(
            _input_ids(_pins(amount)),
            {T2_BOX_NORTH, inst_portion["id"], priv_portion["id"]},
        )
        self.assertNotIn(south_portion["id"], _input_ids(_pins(amount)))

        before_status = _t2_finding(before, STATUS, self.inst)
        before_priv_status = _t2_finding(before, STATUS, self.priv)
        inst_status = _t2_finding(run, STATUS, self.inst)
        priv_status = _t2_finding(run, STATUS, self.priv)
        self.assertEqual(before_status["value"], "not-adverse")
        self.assertEqual(inst_status["value"], "adverse")
        self.assertEqual(priv_status["value"], "not-adverse")
        for status in (before_status, before_priv_status, priv_status):
            self.assertEqual(
                next(
                    pin["origin"]
                    for pin in status["pins"]
                    if pin["role"] == "input" and pin["id"] == default_id
                ),
                "declared_default",
            )
        self.assertEqual(
            _input_ids(_pins(inst_status)),
            {T2_FIN_INST, T2_ENROL_LATER},
        )
        self.assertNotIn(default_id, _input_ids(_pins(inst_status)))
        self.assertNotIn(T2_ENROL_EARLIER, _input_ids(_pins(inst_status)))

        before_walk = _t2_walk(before, before_amount)
        walk = _t2_walk(run, amount)
        for link_id in (before_inst["id"], before_priv["id"], P3_LINK_INST, P3_LINK_PRIV):
            self.assertIn(link_id, before_walk)
        self.assertIn(default_id, before_walk)
        self.assertNotIn(T2_ENROL_EARLIER, before_walk)
        self.assertNotIn(T2_ENROL_LATER, before_walk)
        for link_id in (inst_portion["id"], priv_portion["id"], P3_LINK_INST, P3_LINK_PRIV):
            self.assertIn(link_id, walk)
        self.assertIn(inst_status["id"], walk)
        self.assertIn(priv_status["id"], walk)
        self.assertIn(T2_ENROL_LATER, walk)
        self.assertIn(default_id, walk)
        self.assertNotIn(T2_ENROL_EARLIER, walk)
        self.assertNotIn(south_portion["id"], walk)
        self.assertNotIn(P3_LINK_SOUTH, walk)

    def test_no_joined_link_blocks_on_an_unclosed_collection(self) -> None:
        """West shares no link. Empty ``collect`` blocks; it does not publish 0.

        Link portions exist in the run. None join this statement, and the
        collect names no closed source set.
        """
        _state, _currency, _ctx, run = _p3_execute(_p3_findings(corrected=True))
        portions = [source for source in run.live_sources if source.name == P3_LINK_PORTION]
        self.assertGreater(len(portions), 0)
        self.assertFalse(
            any(
                dict(source.keys or ()).get("statement") == STATEMENT_S3
                for source in portions
            )
        )
        row = _t2_row(run, self.west, STATEMENT_AMOUNT)
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "SOURCE_SET_UNCLOSED")
        self.assertEqual(row["missing"], [P3_LINK_PORTION])
        self.assertNotIn(
            _t2_symbol(STATEMENT_AMOUNT, self.west),
            {pub.finding["symbol"] for pub in run.publications},
        )
        self.assertNotEqual(row["disposition"], "published")
        self.assertNotEqual(row["code"], "DEPENDENCY_ABSENT")

    def test_unaffected_statement_is_byte_identical(self) -> None:
        """South's only borrowing is the private one. Its bytes do not move.

        North changes in the same pair of runs.
        """
        _before_state, _before_currency, _before_ctx, before = _p3_execute(
            _p3_findings(corrected=False)
        )
        _state, _currency, _ctx, after = _p3_execute(_p3_findings(corrected=True))
        self.assertEqual(
            _t2_canonical(_t2_finding(before, STATEMENT_AMOUNT, self.south)),
            _t2_canonical(_t2_finding(after, STATEMENT_AMOUNT, self.south)),
        )
        self.assertEqual(
            _t2_canonical(_t2_row(before, self.south, STATEMENT_AMOUNT)),
            _t2_canonical(_t2_row(after, self.south, STATEMENT_AMOUNT)),
        )
        self.assertEqual(
            _t2_finding(before, STATEMENT_AMOUNT, self.south)["value"], "800"
        )
        self.assertEqual(
            _t2_finding(before, P3_LINK_PORTION, self.link_south)["value"], "800"
        )
        self.assertNotEqual(
            _t2_finding(before, STATEMENT_AMOUNT, self.north)["value"],
            _t2_finding(after, STATEMENT_AMOUNT, self.north)["value"],
        )


class MembershipWithoutPortion(unittest.TestCase):
    """Route (c): the link names the borrowing and carries no portion.

    The value is the membership token ``included``. The portion rules are
    the same rules as ``CollectedPortionReduction``.
    """

    def setUp(self) -> None:
        self.north = _t2_box_fact_id(LENDER, STATEMENT_S1)
        self.west = _t2_box_fact_id(T2_LENDER_WEST, STATEMENT_S3)
        self.link_inst = _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_INST)
        self.link_priv = _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_PRIV)

    def test_non_numeric_portion_blocks_instead_of_publishing(self) -> None:
        """A not-adverse membership link is collected and is not a number.

        The statement does not publish the sibling's 1000, or 1500, or 0.
        The block is not the empty-collection block.
        """
        _state, _currency, _ctx, run = _p3_execute(
            _p3_findings(corrected=False, priv_portion=P3_MEMBERSHIP)
        )
        inst_portion = _t2_finding(run, P3_LINK_PORTION, self.link_inst)
        priv_portion = _t2_finding(run, P3_LINK_PORTION, self.link_priv)
        self.assertEqual(inst_portion["value"], "1000")
        self.assertEqual(priv_portion["value"], P3_MEMBERSHIP)
        self.assertNotEqual(priv_portion["value"], "0")
        row = _t2_row(run, self.north, STATEMENT_AMOUNT)
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "DEPENDENCY_INVALID")
        self.assertEqual(row["missing"], ["not a number: 'included'"])
        self.assertEqual(
            _input_ids(_pins(row)),
            {T2_BOX_NORTH, inst_portion["id"], priv_portion["id"]},
        )
        self.assertNotIn(
            _t2_symbol(STATEMENT_AMOUNT, self.north),
            {pub.finding["symbol"] for pub in run.publications},
        )
        self.assertNotEqual(row["disposition"], "published")
        west = _t2_row(run, self.west, STATEMENT_AMOUNT)
        self.assertEqual(west["code"], "SOURCE_SET_UNCLOSED")
        self.assertNotEqual(row["code"], west["code"])
        self.assertNotEqual(row["missing"], west["missing"])

    def test_adverse_branch_matches_a_known_zero_portion(self) -> None:
        """Adverse ``choose`` returns 0 without reading the link value.

        The statement publishes 500, the same finding as the route-(b)
        correction, where the institutional portion was the known number
        1000. The raw link values differ. The published figure does not.
        """
        known_state, known_currency, _known_ctx, known = _p3_execute(
            _p3_findings(corrected=True)
        )
        state, currency, _ctx, unknown = _p3_execute(
            _p3_findings(corrected=True, inst_portion=P3_MEMBERSHIP)
        )
        self.assertEqual(currency.displaced_finding_ids, frozenset({T2_ENROL_EARLIER}))
        self.assertEqual(
            known_currency.displaced_finding_ids, currency.displaced_finding_ids
        )
        self.assertEqual(state.findings[P3_LINK_INST]["value"], P3_MEMBERSHIP)
        self.assertEqual(known_state.findings[P3_LINK_INST]["value"], 1000)
        self.assertNotEqual(
            state.findings[P3_LINK_INST]["value"],
            known_state.findings[P3_LINK_INST]["value"],
        )
        unknown_portion = _t2_finding(unknown, P3_LINK_PORTION, self.link_inst)
        known_portion = _t2_finding(known, P3_LINK_PORTION, self.link_inst)
        self.assertEqual(unknown_portion["value"], "0")
        self.assertEqual(known_portion["value"], "0")
        self.assertEqual(_t2_canonical(unknown_portion), _t2_canonical(known_portion))
        unknown_amount = _t2_finding(unknown, STATEMENT_AMOUNT, self.north)
        known_amount = _t2_finding(known, STATEMENT_AMOUNT, self.north)
        self.assertEqual(unknown_amount["value"], "500")
        self.assertEqual(_t2_canonical(unknown_amount), _t2_canonical(known_amount))
        self.assertEqual(
            _t2_canonical(_t2_row(unknown, self.north, STATEMENT_AMOUNT)),
            _t2_canonical(_t2_row(known, self.north, STATEMENT_AMOUNT)),
        )
        self.assertEqual(
            _t2_row(unknown, self.north, STATEMENT_AMOUNT)["disposition"], "published"
        )
        self.assertNotEqual(
            _t2_row(unknown, self.north, STATEMENT_AMOUNT)["disposition"], "blocked"
        )


# --- P3b. The link publishes the reduction; the statement subtracts the sum. ---

P3B_LINK_REDUCTION = "demo.tax.link-reduction"
P3B_LINK_RULE = "demo.rule.link-reduction"
P3B_AMOUNT_RULE = "demo.rule.statement-box-minus-reductions"


def _p3b_rules() -> list[dict[str, Any]]:
    status = next(rule for rule in _p3_rules() if rule["id"] == T2_STATUS_RULE)
    return [
        status,
        _t2_rule(
            rule_id=P3B_LINK_RULE,
            citation_id="demo.citation.link-reduction",
            role="computation",
            requires=[STATEMENT_BORROWING, STATUS],
            when={
                "op": "any",
                "args": [
                    _t2_eq(STATUS, STATUS, "adverse"),
                    _t2_eq(STATUS, STATUS, "not-adverse"),
                ],
            },
            value={
                "op": "choose",
                "when": _t2_eq(STATUS, STATUS, "adverse"),
                "then": {"op": "ref", "name": STATEMENT_BORROWING},
                "else": 0,
            },
            publishes=P3B_LINK_REDUCTION,
        ),
        _t2_rule(
            rule_id=P3B_AMOUNT_RULE,
            citation_id="demo.citation.statement-box-minus-reductions",
            role="computation",
            requires=[BOX1],
            when={
                "op": "compare",
                "cmp": "gt",
                "left": {"op": "ref", "name": BOX1},
                "right": 0,
            },
            value={
                "op": "subtract",
                "left": {"op": "ref", "name": BOX1},
                "right": {
                    "op": "add",
                    "args": [{"op": "collect", "name": P3B_LINK_REDUCTION}],
                },
            },
            publishes=STATEMENT_AMOUNT,
        ),
    ]


def _p3b_execute(
    findings: dict[str, dict[str, Any]],
) -> tuple[FindingState, CurrencyView, RunContext, _Run]:
    state = FindingState(
        findings=dict(findings),
        fact_state=KernelState(fact_types=_t2_lattice()),
    )
    currency = compute_currency(state)
    rules = _p3b_rules()
    ctx = marshal_run_context(
        run_id="demo.sli-a4-pass2-p3b",
        state=state,
        currency=currency,
        rules=rules,
        parameters={T2_PARAM: {"id": T2_PARAM, "version": "v1", "values": "not-adverse"}},
        canon={},
        adoption_pin=ADOPTION_PIN,
        governance_pins=GOVERNANCE_PINS,
        fact_types=_p3_fact_types(),
        input_bindings=[{
            "symbol": ENROLMENT,
            "fact_type": {"id": ENROLMENT, "version": "v1"},
            "mode": "optional_default",
        }],
        collect_source_names=[FINANCING, ENROLMENT, BOX1, STATEMENT_BORROWING],
    )
    run = _Run(ctx, SCHEMAS)
    by_id = {rule["id"]: rule for rule in rules}
    run.evaluate_subject_scoped_rule(subject_type=FINANCING, rule=by_id[T2_STATUS_RULE])
    run.evaluate_subject_scoped_rule(
        subject_type=STATEMENT_BORROWING, rule=by_id[P3B_LINK_RULE]
    )
    run.evaluate_subject_scoped_rule(subject_type=BOX1, rule=by_id[P3B_AMOUNT_RULE])
    return state, currency, ctx, run


def _scenario_reduction() -> dict[str, Any]:
    """Validated v10 reduction. Refs the link; does not require it."""
    return {
        "schema": "rule-artifact.v10",
        "id": P3B_LINK_RULE,
        "version": "v1",
        "scope": dict(COVERAGE_SCOPE),
        "role": "computation",
        "requires": [STATUS],
        "pins": [],
        "when": {
            "op": "any",
            "args": [
                _t2_eq(STATUS, STATUS, "adverse"),
                _t2_eq(STATUS, STATUS, "not-adverse"),
            ],
        },
        "value": {
            "op": "choose",
            "when": _t2_eq(STATUS, STATUS, "adverse"),
            "then": {"op": "ref", "name": STATEMENT_BORROWING},
            "else": 0,
        },
        "publishes": P3B_LINK_REDUCTION,
        "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
    }


def _coverage_rules() -> list[dict[str, Any]]:
    status = next(rule for rule in _p3_rules() if rule["id"] == T2_STATUS_RULE)
    return [status, _scenario_reduction(), _coverage()]


def _status_surface_bundle() -> dict[str, Any]:
    """Puts schooling status on the fact surface without a second coverage name.

    The bundle also names the link type, so the coverage edge reaches it.
    """
    return {
        "schema": "bundle.v2",
        "id": "demo.bundle.statement-links",
        "version": "v1",
        "label": "Demo statement links",
        "fact_types": [
            {"schema": "fact-type.v2", "id": STATEMENT_BORROWING, "version": "v1"},
            {"schema": "fact-type.v2", "id": STATUS, "version": "v1"},
        ],
    }


def _assert_validated_coverage(rules: list[dict[str, Any]]) -> None:
    """The coverage and reduction rules pass validate_package. The status rule does not."""
    coverage = next(rule for rule in rules if rule["id"] == P3B_AMOUNT_RULE)
    reduction = next(rule for rule in rules if rule["id"] == P3B_LINK_RULE)
    result, _package = _validate([
        (coverage, "computation"),
        (reduction, "computation"),
        (_parameter(), "parameter"),
        (_fact_type(STATEMENT_BORROWING, "Demo statement to borrowing link"), "fact-type"),
        (_status_surface_bundle(), "fact-type-bundle"),
        (_citation(), "citation"),
    ])
    if not result.ok:
        raise AssertionError(result.issues)


def _coverage_execute(
    findings: dict[str, dict[str, Any]],
    *,
    withdrawn: tuple[str, ...] = (),
    rules: list[dict[str, Any]] | None = None,
    statement: bool = True,
) -> tuple[FindingState, CurrencyView, RunContext, _Run]:
    """Hand-assembled run of validated coverage rules.

    Calling code selects per-subject dispatch. That scheduling is not settled.
    """
    rules = list(rules) if rules is not None else _coverage_rules()
    _assert_validated_coverage(rules)
    state = FindingState(
        findings=dict(findings),
        fact_state=KernelState(fact_types=_t2_lattice()),
        withdrawn_fact_ids=frozenset(withdrawn),
    )
    currency = compute_currency(state)
    ctx = marshal_run_context(
        run_id="demo.sli-a4-pass2-p3b-coverage",
        state=state,
        currency=currency,
        rules=rules,
        parameters={
            T2_PARAM: {"id": T2_PARAM, "version": "v1", "values": "not-adverse"},
            _parameter()["id"]: _parameter(),
        },
        canon={},
        adoption_pin=ADOPTION_PIN,
        governance_pins=GOVERNANCE_PINS,
        fact_types=_p3_fact_types(),
        input_bindings=[{
            "symbol": ENROLMENT,
            "fact_type": {"id": ENROLMENT, "version": "v1"},
            "mode": "optional_default",
        }],
        collect_source_names=[FINANCING, ENROLMENT, BOX1, STATEMENT_BORROWING],
    )
    run = _Run(ctx, SCHEMAS)
    by_id = {rule["id"]: rule for rule in rules}
    run.evaluate_subject_scoped_rule(subject_type=FINANCING, rule=by_id[T2_STATUS_RULE])
    run.evaluate_subject_scoped_rule(
        subject_type=STATEMENT_BORROWING, rule=by_id[P3B_LINK_RULE]
    )
    if statement:
        run.evaluate_subject_scoped_rule(subject_type=BOX1, rule=by_id[P3B_AMOUNT_RULE])
    return state, currency, ctx, run


class ReductionShapedRules(unittest.TestCase):
    """The link publishes the reduction. The statement subtracts the sum.

    Adverse publishes the portion. Not-adverse publishes 0. The statement
    publishes box 1 minus ``collect`` of those reductions, and does not
    ``requires`` the reduction. North's box is 1500. The same scenario and
    findings as ``CollectedPortionReduction``.
    """

    def setUp(self) -> None:
        self.north = _t2_box_fact_id(LENDER, STATEMENT_S1)
        self.west = _t2_box_fact_id(T2_LENDER_WEST, STATEMENT_S3)
        self.link_inst = _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_INST)
        self.link_priv = _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_PRIV)
        self.link_south = _t2_link_fact_id(
            P2_LENDER_SOUTH, STATEMENT_S2, P2_BORROWING_PRIV
        )
        self.inst = _t2_financing_fact_id(P2_BORROWING_INST, PERIOD_AUTUMN)
        self.priv = _t2_financing_fact_id(P2_BORROWING_PRIV, PERIOD_SPRING)
        link = next(rule for rule in _p3b_rules() if rule["id"] == P3B_LINK_RULE)
        amount = next(rule for rule in _p3b_rules() if rule["id"] == P3B_AMOUNT_RULE)
        choose = link["value"]
        self.assertEqual(choose["op"], "choose")
        self.assertEqual(choose["when"], _t2_eq(STATUS, STATUS, "adverse"))
        self.assertEqual(choose["then"], {"op": "ref", "name": STATEMENT_BORROWING})
        self.assertEqual(choose["else"], 0)
        self.assertEqual(amount["requires"], [BOX1])
        self.assertNotIn(P3B_LINK_REDUCTION, amount["requires"])
        subtract = amount["value"]
        self.assertEqual(subtract["op"], "subtract")
        self.assertEqual(subtract["left"], {"op": "ref", "name": BOX1})
        self.assertEqual(subtract["right"]["op"], "add")
        collected = subtract["right"]["args"][0]
        self.assertEqual(collected, {"op": "collect", "name": P3B_LINK_REDUCTION})
        self.assertNotIn("source_set", collected)
        self.assertNotEqual(self.link_inst, self.link_priv)

    def test_exhausting_portions(self) -> None:
        """Portions 1000 and 500 on box 1500. 1500 before, 500 after.

        Both published reductions are in the pin walk. After the correction
        the walk also reaches the later enrolment finding, not the displaced
        one, and not the other statement's reduction.
        """
        _before_state, before_currency, _before_ctx, before = _p3b_execute(
            _p3_findings(corrected=False)
        )
        _state, currency, _ctx, run = _p3b_execute(_p3_findings(corrected=True))
        self.assertEqual(before_currency.displaced_finding_ids, frozenset())
        self.assertEqual(currency.displaced_finding_ids, frozenset({T2_ENROL_EARLIER}))
        self.assertEqual(
            [(reason.kind, reason.by) for reason in currency.reasons[T2_ENROL_EARLIER]],
            [("correction", T2_ENROL_LATER)],
        )

        before_inst = _t2_finding(before, P3B_LINK_REDUCTION, self.link_inst)
        before_priv = _t2_finding(before, P3B_LINK_REDUCTION, self.link_priv)
        inst_reduction = _t2_finding(run, P3B_LINK_REDUCTION, self.link_inst)
        priv_reduction = _t2_finding(run, P3B_LINK_REDUCTION, self.link_priv)
        south_reduction = _t2_finding(run, P3B_LINK_REDUCTION, self.link_south)
        self.assertEqual(before_inst["value"], "0")
        self.assertEqual(before_priv["value"], "0")
        self.assertEqual(inst_reduction["value"], "1000")
        self.assertEqual(priv_reduction["value"], "0")
        self.assertNotEqual(inst_reduction["value"], "0")
        self.assertNotEqual(priv_reduction["value"], "500")

        before_amount = _t2_finding(before, STATEMENT_AMOUNT, self.north)
        amount = _t2_finding(run, STATEMENT_AMOUNT, self.north)
        self.assertEqual(before_amount["value"], "1500")
        self.assertEqual(amount["value"], "500")
        self.assertEqual(
            _t2_row(before, self.north, STATEMENT_AMOUNT)["disposition"], "published"
        )
        self.assertEqual(
            _t2_row(run, self.north, STATEMENT_AMOUNT)["disposition"], "published"
        )
        self.assertEqual(
            _input_ids(_pins(before_amount)),
            {T2_BOX_NORTH, before_inst["id"], before_priv["id"]},
        )
        self.assertEqual(
            _input_ids(_pins(amount)),
            {T2_BOX_NORTH, inst_reduction["id"], priv_reduction["id"]},
        )
        self.assertNotIn(south_reduction["id"], _input_ids(_pins(amount)))

        before_walk = _t2_walk(before, before_amount)
        walk = _t2_walk(run, amount)
        self.assertIn(before_inst["id"], before_walk)
        self.assertIn(before_priv["id"], before_walk)
        self.assertNotIn(T2_ENROL_LATER, before_walk)
        self.assertNotIn(T2_ENROL_EARLIER, before_walk)
        self.assertIn(inst_reduction["id"], walk)
        self.assertIn(priv_reduction["id"], walk)
        self.assertIn(T2_ENROL_LATER, walk)
        self.assertNotIn(T2_ENROL_EARLIER, walk)
        self.assertNotIn(south_reduction["id"], walk)
        self.assertNotIn(P3_LINK_SOUTH, walk)

    def test_undershoot(self) -> None:
        """Portions 1000 and 300 on box 1500. Before 1500. After, 500.

        The institutional correction subtracts 1000. The private reduction
        stays 0. The unpublished 200 is still inside the published 500.
        """
        _before_state, before_currency, _before_ctx, before = _p3b_execute(
            _p3_findings(corrected=False, priv_portion=300)
        )
        state, currency, _ctx, run = _p3b_execute(
            _p3_findings(corrected=True, priv_portion=300)
        )
        self.assertEqual(before_currency.displaced_finding_ids, frozenset())
        self.assertEqual(currency.displaced_finding_ids, frozenset({T2_ENROL_EARLIER}))
        self.assertEqual(state.findings[P3_LINK_INST]["value"], 1000)
        self.assertEqual(state.findings[P3_LINK_PRIV]["value"], 300)
        self.assertEqual(_t2_finding(run, STATUS, self.inst)["value"], "adverse")
        self.assertEqual(_t2_finding(run, STATUS, self.priv)["value"], "not-adverse")

        before_inst = _t2_finding(before, P3B_LINK_REDUCTION, self.link_inst)
        before_priv = _t2_finding(before, P3B_LINK_REDUCTION, self.link_priv)
        inst_reduction = _t2_finding(run, P3B_LINK_REDUCTION, self.link_inst)
        priv_reduction = _t2_finding(run, P3B_LINK_REDUCTION, self.link_priv)
        self.assertEqual(before_inst["value"], "0")
        self.assertEqual(before_priv["value"], "0")
        self.assertEqual(inst_reduction["value"], "1000")
        self.assertEqual(priv_reduction["value"], "0")
        self.assertNotEqual(priv_reduction["value"], "300")

        before_amount = _t2_finding(before, STATEMENT_AMOUNT, self.north)
        amount = _t2_finding(run, STATEMENT_AMOUNT, self.north)
        unassigned = 1500 - 1000 - 300
        self.assertEqual(unassigned, 200)
        self.assertEqual(before_amount["value"], "1500")
        self.assertEqual(amount["value"], "500")
        self.assertEqual(int(amount["value"]), 300 + unassigned)
        self.assertNotEqual(amount["value"], "300")
        self.assertNotEqual(amount["value"], "200")
        self.assertEqual(
            _t2_row(run, self.north, STATEMENT_AMOUNT)["disposition"], "published"
        )

    def test_route_c_unknown_portion_adverse(self) -> None:
        """Adverse membership token: the statement publishes no figure.

        The reduction is the token, which is not a number. A known portion
        of 1000 on the same correction publishes 500. These outcomes differ.
        """
        known_state, known_currency, _known_ctx, known = _p3b_execute(
            _p3_findings(corrected=True)
        )
        state, currency, _ctx, unknown = _p3b_execute(
            _p3_findings(corrected=True, inst_portion=P3_MEMBERSHIP)
        )
        self.assertEqual(currency.displaced_finding_ids, frozenset({T2_ENROL_EARLIER}))
        self.assertEqual(
            known_currency.displaced_finding_ids, currency.displaced_finding_ids
        )
        self.assertEqual(state.findings[P3_LINK_INST]["value"], P3_MEMBERSHIP)
        self.assertEqual(known_state.findings[P3_LINK_INST]["value"], 1000)
        self.assertNotEqual(
            state.findings[P3_LINK_INST]["value"],
            known_state.findings[P3_LINK_INST]["value"],
        )

        unknown_reduction = _t2_finding(unknown, P3B_LINK_REDUCTION, self.link_inst)
        known_reduction = _t2_finding(known, P3B_LINK_REDUCTION, self.link_inst)
        unknown_private = _t2_finding(unknown, P3B_LINK_REDUCTION, self.link_priv)
        self.assertEqual(unknown_reduction["value"], P3_MEMBERSHIP)
        self.assertEqual(known_reduction["value"], "1000")
        self.assertNotEqual(unknown_reduction["value"], known_reduction["value"])
        self.assertNotEqual(unknown_reduction["value"], "0")
        self.assertEqual(unknown_private["value"], "0")

        known_amount = _t2_finding(known, STATEMENT_AMOUNT, self.north)
        known_row = _t2_row(known, self.north, STATEMENT_AMOUNT)
        self.assertEqual(known_amount["value"], "500")
        self.assertEqual(known_row["disposition"], "published")

        row = _t2_row(unknown, self.north, STATEMENT_AMOUNT)
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "DEPENDENCY_INVALID")
        self.assertEqual(row["missing"], ["not a number: 'included'"])
        self.assertEqual(
            _input_ids(_pins(row)),
            {T2_BOX_NORTH, unknown_reduction["id"], unknown_private["id"]},
        )
        self.assertNotIn(
            _t2_symbol(STATEMENT_AMOUNT, self.north),
            {pub.finding["symbol"] for pub in unknown.publications},
        )
        self.assertNotEqual(row["disposition"], "published")
        self.assertNotEqual(_t2_canonical(row), _t2_canonical(known_row))
        self.assertNotEqual(row["disposition"], known_row["disposition"])

    def test_route_c_unknown_portion_not_adverse(self) -> None:
        """The same membership link, with no correction, publishes 1500.

        Neither reduction is adverse, so both publish 0. The token is never
        read. The unknown portion is not required.
        """
        state, currency, _ctx, run = _p3b_execute(
            _p3_findings(corrected=False, inst_portion=P3_MEMBERSHIP)
        )
        self.assertEqual(currency.displaced_finding_ids, frozenset())
        self.assertEqual(state.findings[P3_LINK_INST]["value"], P3_MEMBERSHIP)
        self.assertNotEqual(state.findings[P3_LINK_INST]["value"], 1000)
        inst_reduction = _t2_finding(run, P3B_LINK_REDUCTION, self.link_inst)
        priv_reduction = _t2_finding(run, P3B_LINK_REDUCTION, self.link_priv)
        self.assertEqual(inst_reduction["value"], "0")
        self.assertEqual(priv_reduction["value"], "0")
        self.assertNotEqual(inst_reduction["value"], P3_MEMBERSHIP)
        amount = _t2_finding(run, STATEMENT_AMOUNT, self.north)
        row = _t2_row(run, self.north, STATEMENT_AMOUNT)
        self.assertEqual(amount["value"], "1500")
        self.assertEqual(row["disposition"], "published")
        self.assertNotEqual(row["disposition"], "blocked")
        self.assertEqual(
            _input_ids(_pins(amount)),
            {T2_BOX_NORTH, inst_reduction["id"], priv_reduction["id"]},
        )

    def test_no_joined_link(self) -> None:
        """West has a box and no link. Record the statement outcome.

        Reductions exist on the run. None is keyed to this statement.
        """
        _state, _currency, _ctx, run = _p3b_execute(_p3_findings(corrected=True))
        reductions = [
            source for source in run.live_sources if source.name == P3B_LINK_REDUCTION
        ]
        self.assertGreater(len(reductions), 0)
        self.assertFalse(
            any(
                dict(source.keys or ()).get("statement") == STATEMENT_S3
                for source in reductions
            )
        )
        row = _t2_row(run, self.west, STATEMENT_AMOUNT)
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "SOURCE_SET_UNCLOSED")
        self.assertEqual(row["missing"], [P3B_LINK_REDUCTION])
        self.assertNotIn(
            _t2_symbol(STATEMENT_AMOUNT, self.west),
            {pub.finding["symbol"] for pub in run.publications},
        )
        self.assertNotEqual(row["disposition"], "published")
        self.assertNotEqual(row["code"], "DEPENDENCY_ABSENT")
        self.assertNotEqual(row["code"], "DEPENDENCY_INVALID")


class UnresolvedLinkBlocksTheStatement(unittest.TestCase):
    """A recorded link whose reduction never became a number blocks that statement.

    The coverage and reduction rules are validated v10 citizens. The run is
    still hand-assembled: the test calls per-subject dispatch itself. The
    status rule remains the v6 probe and is not in the validated package.
    """

    def setUp(self) -> None:
        self.north = _t2_box_fact_id(LENDER, STATEMENT_S1)
        self.south = _t2_box_fact_id(P2_LENDER_SOUTH, STATEMENT_S2)
        self.west = _t2_box_fact_id(T2_LENDER_WEST, STATEMENT_S3)
        self.link_inst = _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_INST)
        self.link_priv = _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_PRIV)
        self.link_south = _t2_link_fact_id(
            P2_LENDER_SOUTH, STATEMENT_S2, P2_BORROWING_PRIV
        )
        self.inst = _t2_financing_fact_id(P2_BORROWING_INST, PERIOD_AUTUMN)
        self.priv = _t2_financing_fact_id(P2_BORROWING_PRIV, PERIOD_SPRING)
        rules = _coverage_rules()
        link = next(rule for rule in rules if rule["id"] == P3B_LINK_RULE)
        amount = next(rule for rule in rules if rule["id"] == P3B_AMOUNT_RULE)
        self.assertEqual(link["schema"], "rule-artifact.v10")
        self.assertEqual(link["requires"], [STATUS])
        self.assertNotIn(STATEMENT_BORROWING, link["requires"])
        self.assertEqual(link["value"]["else"], 0)
        self.assertEqual(link["value"]["then"], {"op": "ref", "name": STATEMENT_BORROWING})
        self.assertEqual(amount["requires"], [BOX1])
        self.assertNotIn(P3B_LINK_REDUCTION, amount["requires"])
        node = amount["value"]["right"]
        self.assertEqual(node["op"], "link_coverage")
        self.assertEqual(node["links"], STATEMENT_BORROWING)
        self.assertEqual(node["reductions"], P3B_LINK_REDUCTION)
        self.assertNotIn("source_set", node)
        _assert_validated_coverage(rules)

    def test_one_of_two_links_unresolved(self) -> None:
        """One of North's two links has no financing claim.

        Both links stay. The institutional reduction blocks and is not a
        live source. North blocks ``DEPENDENCY_INVALID`` and ``missing``
        is exactly that link's finding id. The private reduction is not
        the whole reduction, and 1500 is not published.
        """
        intact = _p3_findings(corrected=False)
        missing = _p3_findings(corrected=False)
        del missing[T2_FIN_INST]
        self.assertIn(P3_LINK_INST, missing)
        self.assertIn(P3_LINK_PRIV, missing)
        self.assertNotIn(T2_FIN_INST, missing)

        _intact_state, intact_currency, _intact_ctx, intact_run = _coverage_execute(intact)
        state, currency, _ctx, run = _coverage_execute(missing)
        self.assertEqual(intact_currency.displaced_finding_ids, frozenset())
        self.assertEqual(currency.displaced_finding_ids, frozenset())
        self.assertNotIn(T2_FIN_INST, state.findings)
        self.assertEqual(state.findings[P3_LINK_INST]["value"], 1000)
        self.assertEqual(state.findings[P3_LINK_PRIV]["value"], 500)

        inst_row = _t2_row(run, self.link_inst, P3B_LINK_REDUCTION)
        self.assertEqual(inst_row["disposition"], "blocked")
        self.assertEqual(inst_row["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(inst_row["missing"], [STATUS])
        self.assertEqual(_input_ids(_pins(inst_row)), {P3_LINK_INST})
        inst_symbol = _t2_symbol(P3B_LINK_REDUCTION, self.link_inst)
        self.assertNotIn(
            inst_symbol, {pub.finding["symbol"] for pub in run.publications}
        )
        self.assertNotIn(inst_symbol, run.symbols)
        self.assertEqual(
            [
                entry for entry in run.blocked
                if entry.get("subject_fact_id") == self.link_inst
            ],
            [{
                "artifact_id": P3B_LINK_RULE,
                "code": "DEPENDENCY_ABSENT",
                "missing": [STATUS],
                "subject_fact_id": self.link_inst,
            }],
        )
        self.assertFalse(any(
            source.name == P3B_LINK_REDUCTION and source.fact_id == self.link_inst
            for source in run.live_sources
        ))
        self.assertTrue(any(
            source.name == STATEMENT_BORROWING and source.finding_id == P3_LINK_INST
            for source in run.live_sources
        ))
        self.assertTrue(any(
            source.name == P3B_LINK_REDUCTION and source.fact_id == self.link_priv
            for source in run.live_sources
        ))

        priv_reduction = _t2_finding(run, P3B_LINK_REDUCTION, self.link_priv)
        self.assertEqual(priv_reduction["value"], "0")
        self.assertEqual(
            _t2_row(run, self.link_priv, P3B_LINK_REDUCTION)["disposition"],
            "published",
        )
        self.assertNotIn(
            _t2_symbol(STATUS, self.inst),
            {pub.finding["symbol"] for pub in run.publications},
        )

        intact_amount = _t2_finding(intact_run, STATEMENT_AMOUNT, self.north)
        row = _t2_row(run, self.north, STATEMENT_AMOUNT)
        self.assertEqual(intact_amount["value"], "1500")
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "DEPENDENCY_INVALID")
        self.assertEqual(row["missing"], [P3_LINK_INST])
        self.assertNotEqual(row["code"], "SOURCE_SET_UNCLOSED")
        self.assertNotIn(P3B_LINK_REDUCTION, row["missing"])
        self.assertNotIn(STATUS, row["missing"])
        self.assertNotIn(P3_LINK_PRIV, row["missing"])
        self.assertNotIn(priv_reduction["id"], row["missing"])
        self.assertIn(P3_LINK_INST, _input_ids(_pins(row)))
        self.assertNotIn(P3_LINK_PRIV, _input_ids(_pins(row)))
        self.assertNotIn(priv_reduction["id"], _input_ids(_pins(row)))
        self.assertNotIn(_parameter()["id"], {pin["id"] for pin in _pins(row)})
        self.assertNotIn(
            _t2_symbol(STATEMENT_AMOUNT, self.north),
            {pub.finding["symbol"] for pub in run.publications},
        )
        self.assertNotEqual(row["disposition"], "published")
        intact_inputs = _input_ids(_pins(intact_amount))
        intact_inst = _t2_finding(intact_run, P3B_LINK_REDUCTION, self.link_inst)
        intact_priv = _t2_finding(intact_run, P3B_LINK_REDUCTION, self.link_priv)
        self.assertEqual(intact_inst["value"], "0")
        self.assertEqual(intact_priv["value"], "0")
        self.assertIn(P3_LINK_INST, intact_inputs)
        self.assertIn(P3_LINK_PRIV, intact_inputs)
        self.assertIn(intact_inst["id"], intact_inputs)
        self.assertIn(intact_priv["id"], intact_inputs)
        self.assertNotIn(
            _parameter()["id"],
            {pin["id"] for pin in _pins(intact_amount) if pin["role"] == "parameter"},
        )

        self.assertEqual(
            _t2_canonical(_t2_finding(intact_run, STATEMENT_AMOUNT, self.south)),
            _t2_canonical(_t2_finding(run, STATEMENT_AMOUNT, self.south)),
        )
        self.assertEqual(
            _t2_canonical(_t2_row(intact_run, self.south, STATEMENT_AMOUNT)),
            _t2_canonical(_t2_row(run, self.south, STATEMENT_AMOUNT)),
        )
        self.assertEqual(
            _t2_finding(run, STATEMENT_AMOUNT, self.south)["value"], "800"
        )

    def test_only_recorded_link_unresolved(self) -> None:
        """North's only recorded link is uncovered.

        The private link is absent in both runs. The defect run also drops
        the institutional financing claim. North blocks ``DEPENDENCY_INVALID``
        naming that link. It does not block ``SOURCE_SET_UNCLOSED`` and it
        does not take the no-link default. West, which recorded no link,
        publishes its own default in the same run.
        """
        resolved_findings = _p3_findings(corrected=False)
        del resolved_findings[P3_LINK_PRIV]
        unresolved_findings = _p3_findings(corrected=False)
        del unresolved_findings[P3_LINK_PRIV]
        del unresolved_findings[T2_FIN_INST]
        self.assertIn(P3_LINK_INST, unresolved_findings)
        self.assertNotIn(P3_LINK_PRIV, unresolved_findings)
        self.assertNotIn(T2_FIN_INST, unresolved_findings)

        _resolved_state, _resolved_currency, _resolved_ctx, resolved = _coverage_execute(
            resolved_findings
        )
        state, _currency, _ctx, run = _coverage_execute(unresolved_findings)
        self.assertEqual(
            _t2_finding(resolved, STATEMENT_AMOUNT, self.north)["value"], "1500"
        )
        self.assertEqual(
            _t2_row(resolved, self.north, STATEMENT_AMOUNT)["disposition"],
            "published",
        )
        self.assertIn(
            P3_LINK_INST,
            _t2_walk(resolved, _t2_finding(resolved, STATEMENT_AMOUNT, self.north)),
        )

        self.assertEqual(state.findings[P3_LINK_INST]["value"], 1000)
        self.assertTrue(any(
            source.name == STATEMENT_BORROWING and source.finding_id == P3_LINK_INST
            for source in run.live_sources
        ))
        self.assertFalse(any(
            source.name == P3B_LINK_REDUCTION and source.fact_id == self.link_inst
            for source in run.live_sources
        ))
        inst_row = _t2_row(run, self.link_inst, P3B_LINK_REDUCTION)
        self.assertEqual(inst_row["disposition"], "blocked")
        self.assertEqual(inst_row["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(inst_row["missing"], [STATUS])
        self.assertEqual(_input_ids(_pins(inst_row)), {P3_LINK_INST})
        self.assertNotIn(
            _t2_symbol(P3B_LINK_REDUCTION, self.link_inst),
            {pub.finding["symbol"] for pub in run.publications},
        )

        row = _t2_row(run, self.north, STATEMENT_AMOUNT)
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "DEPENDENCY_INVALID")
        self.assertEqual(row["missing"], [P3_LINK_INST])
        self.assertNotEqual(row["code"], "SOURCE_SET_UNCLOSED")
        self.assertNotEqual(row["missing"], [P3B_LINK_REDUCTION])
        self.assertNotIn(self.link_inst, row["missing"])
        self.assertNotIn(STATUS, row["missing"])
        self.assertNotEqual(row["disposition"], "published")
        self.assertIn(P3_LINK_INST, _input_ids(_pins(row)))
        self.assertIn(T2_BOX_NORTH, _input_ids(_pins(row)))
        self.assertNotIn(_parameter()["id"], {pin["id"] for pin in _pins(row)})
        self.assertNotIn(
            _t2_symbol(STATEMENT_AMOUNT, self.north),
            {pub.finding["symbol"] for pub in run.publications},
        )

        west_amount = _t2_finding(run, STATEMENT_AMOUNT, self.west)
        west = _t2_row(run, self.west, STATEMENT_AMOUNT)
        self.assertEqual(west["disposition"], "published")
        self.assertEqual(west_amount["value"], "400")
        self.assertNotEqual(west.get("code"), row["code"])
        self.assertNotIn("resolved_input", west_amount)
        self.assertEqual(
            {pin["id"] for pin in _pins(west_amount) if pin["role"] == "parameter"},
            {_parameter()["id"]},
        )
        self.assertEqual(_input_ids(_pins(west_amount)), {T2_BOX_WEST})
        self.assertFalse(any(pin["role"] == "package" for pin in _pins(west_amount)))
        self.assertFalse(any(
            source.name == STATEMENT_BORROWING
            and dict(source.keys or ()).get("statement") == STATEMENT_S3
            for source in run.live_sources
        ))

        self.assertEqual(
            _t2_canonical(_t2_finding(resolved, STATEMENT_AMOUNT, self.south)),
            _t2_canonical(_t2_finding(run, STATEMENT_AMOUNT, self.south)),
        )
        self.assertEqual(
            _t2_canonical(_t2_row(resolved, self.south, STATEMENT_AMOUNT)),
            _t2_canonical(_t2_row(run, self.south, STATEMENT_AMOUNT)),
        )
        self.assertEqual(
            _t2_finding(run, STATEMENT_AMOUNT, self.south)["value"], "800"
        )


class LinkCoverageStatementOutcomes(unittest.TestCase):
    """The three outcomes on the same statements the probes already use.

    Coverage and reduction rules pass ``validate_package``. The run is
    hand-assembled. Nothing here is the durable reader.
    """

    def setUp(self) -> None:
        self.north = _t2_box_fact_id(LENDER, STATEMENT_S1)
        self.south = _t2_box_fact_id(P2_LENDER_SOUTH, STATEMENT_S2)
        self.west = _t2_box_fact_id(T2_LENDER_WEST, STATEMENT_S3)
        self.link_inst = _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_INST)
        self.link_priv = _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_PRIV)
        self.link_south = _t2_link_fact_id(
            P2_LENDER_SOUTH, STATEMENT_S2, P2_BORROWING_PRIV
        )

    def test_all_links_resolved_subtracts_the_sum_and_pins_each(self) -> None:
        _state, _currency, _ctx, run = _coverage_execute(_p3_findings(corrected=True))
        inst = _t2_finding(run, P3B_LINK_REDUCTION, self.link_inst)
        priv = _t2_finding(run, P3B_LINK_REDUCTION, self.link_priv)
        self.assertEqual(inst["value"], "1000")
        self.assertEqual(priv["value"], "0")
        amount = _t2_finding(run, STATEMENT_AMOUNT, self.north)
        self.assertEqual(amount["value"], "500")
        self.assertEqual(_t2_row(run, self.north, STATEMENT_AMOUNT)["disposition"], "published")
        inputs = _input_ids(_pins(amount))
        self.assertIn(P3_LINK_INST, inputs)
        self.assertIn(P3_LINK_PRIV, inputs)
        self.assertIn(inst["id"], inputs)
        self.assertIn(priv["id"], inputs)
        self.assertIn(T2_BOX_NORTH, inputs)
        self.assertFalse(any(pin["role"] == "parameter" for pin in _pins(amount)))
        self.assertFalse(any(pin["role"] == "package" for pin in _pins(amount)))
        self.assertNotIn("resolved_input", amount)

    def test_inapplicable_reduction_blocks_naming_the_link(self) -> None:
        rules = _coverage_rules()
        link = next(rule for rule in rules if rule["id"] == P3B_LINK_RULE)
        link["when"] = {"op": "compare", "cmp": "gt", "left": 0, "right": 1}
        _state, _currency, _ctx, run = _coverage_execute(
            _p3_findings(corrected=False), rules=rules
        )
        self.assertFalse(any(source.name == P3B_LINK_REDUCTION for source in run.live_sources))
        row = _t2_row(run, self.north, STATEMENT_AMOUNT)
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "DEPENDENCY_INVALID")
        self.assertEqual(row["missing"], [P3_LINK_INST, P3_LINK_PRIV])
        self.assertNotIn(STATUS, row["missing"])
        self.assertNotIn(
            _t2_symbol(STATEMENT_AMOUNT, self.north),
            {pub.finding["symbol"] for pub in run.publications},
        )
        south = _t2_row(run, self.south, STATEMENT_AMOUNT)
        self.assertEqual(south["missing"], [P3_LINK_SOUTH])
        west = _t2_finding(run, STATEMENT_AMOUNT, self.west)
        self.assertEqual(west["value"], "400")

    def test_false_guard_does_not_publish_the_default_or_block_uncovered(self) -> None:
        rules = _coverage_rules()
        amount_rule = next(rule for rule in rules if rule["id"] == P3B_AMOUNT_RULE)
        amount_rule["when"] = {"op": "compare", "cmp": "gt", "left": 0, "right": 1}
        _state, _currency, _ctx, run = _coverage_execute(
            _p3_findings(corrected=False), rules=rules
        )
        row = _t2_row(run, self.north, STATEMENT_AMOUNT)
        self.assertEqual(row["disposition"], "inapplicable")
        self.assertNotIn("code", row)
        self.assertNotIn(
            _t2_symbol(STATEMENT_AMOUNT, self.north),
            {pub.finding["symbol"] for pub in run.publications},
        )

    def test_correction_pins_the_successor_link(self) -> None:
        successor = "demo.finding.link.p3-inst-successor"
        findings = _p3_findings(corrected=False)
        findings[successor] = _finding(successor, findings[P3_LINK_INST]["fact_id"], 1000)
        _base_state, _base_currency, _base_ctx, baseline = _coverage_execute(
            _p3_findings(corrected=False)
        )
        state, currency, _ctx, run = _coverage_execute(findings)
        self.assertIn(P3_LINK_INST, currency.displaced_finding_ids)
        self.assertNotIn(successor, currency.displaced_finding_ids)
        self.assertIn(P3_LINK_INST, state.findings)
        self.assertFalse(any(source.finding_id == P3_LINK_INST for source in run.live_sources))
        self.assertTrue(any(
            source.name == STATEMENT_BORROWING and source.finding_id == successor
            for source in run.live_sources
        ))
        amount = _t2_finding(run, STATEMENT_AMOUNT, self.north)
        inputs = _input_ids(_pins(amount))
        walk = _t2_walk(run, amount)
        self.assertIn(successor, inputs)
        self.assertIn(successor, walk)
        self.assertNotIn(P3_LINK_INST, inputs)
        self.assertNotIn(P3_LINK_INST, walk)
        self.assertEqual(
            _t2_canonical(_t2_finding(baseline, STATEMENT_AMOUNT, self.south)),
            _t2_canonical(_t2_finding(run, STATEMENT_AMOUNT, self.south)),
        )
        self.assertEqual(
            _t2_canonical(_t2_row(baseline, self.south, STATEMENT_AMOUNT)),
            _t2_canonical(_t2_row(run, self.south, STATEMENT_AMOUNT)),
        )

    def test_withdrawal_takes_the_default(self) -> None:
        findings = _p3_findings(corrected=False)
        _base_state, _base_currency, _base_ctx, baseline = _coverage_execute(findings)
        north_links = (
            findings[P3_LINK_INST]["fact_id"],
            findings[P3_LINK_PRIV]["fact_id"],
        )
        state, currency, _ctx, run = _coverage_execute(findings, withdrawn=north_links)
        self.assertIn(P3_LINK_INST, currency.displaced_finding_ids)
        self.assertIn(P3_LINK_PRIV, currency.displaced_finding_ids)
        self.assertFalse(any(
            source.finding_id in {P3_LINK_INST, P3_LINK_PRIV} for source in run.live_sources
        ))
        amount = _t2_finding(run, STATEMENT_AMOUNT, self.north)
        self.assertEqual(amount["value"], "1500")
        self.assertEqual(_t2_row(run, self.north, STATEMENT_AMOUNT)["disposition"], "published")
        self.assertNotIn("resolved_input", amount)
        self.assertEqual(
            {pin["id"] for pin in _pins(amount) if pin["role"] == "parameter"},
            {_parameter()["id"]},
        )
        inputs = _input_ids(_pins(amount))
        self.assertEqual(inputs, {T2_BOX_NORTH})
        self.assertNotIn(P3_LINK_INST, inputs)
        self.assertNotIn(P3_LINK_PRIV, inputs)
        self.assertFalse(any(pin["role"] == "package" for pin in _pins(amount)))
        self.assertEqual(
            _t2_canonical(_t2_finding(baseline, STATEMENT_AMOUNT, self.south)),
            _t2_canonical(_t2_finding(run, STATEMENT_AMOUNT, self.south)),
        )
        self.assertEqual(
            _t2_canonical(_t2_row(baseline, self.south, STATEMENT_AMOUNT)),
            _t2_canonical(_t2_row(run, self.south, STATEMENT_AMOUNT)),
        )

    def test_orphan_reduction_still_joined_blocks_naming_the_reduction(self) -> None:
        """Observed when a reduction survives the link in the same run.

        The statement blocks ``DEPENDENCY_INVALID`` and ``missing`` is the
        reduction finding ids. The default is not published. The block is
        not reported as a missing displacement edge.
        """
        _state, _currency, _ctx, run = _coverage_execute(
            _p3_findings(corrected=False), statement=False
        )
        inst = _t2_finding(run, P3B_LINK_REDUCTION, self.link_inst)
        priv = _t2_finding(run, P3B_LINK_REDUCTION, self.link_priv)
        run.live_sources = [
            source for source in run.live_sources
            if not (
                source.name == STATEMENT_BORROWING
                and source.fact_id in {self.link_inst, self.link_priv}
            )
        ]
        rule = next(rule for rule in _coverage_rules() if rule["id"] == P3B_AMOUNT_RULE)
        run.evaluate_subject_scoped_rule(subject_type=BOX1, rule=rule)
        row = _t2_row(run, self.north, STATEMENT_AMOUNT)
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "DEPENDENCY_INVALID")
        self.assertEqual(row["missing"], sorted([inst["id"], priv["id"]]))
        self.assertNotIn(P3_LINK_INST, row["missing"])
        self.assertNotIn(
            _t2_symbol(STATEMENT_AMOUNT, self.north),
            {pub.finding["symbol"] for pub in run.publications},
        )
        south = _t2_finding(run, STATEMENT_AMOUNT, self.south)
        self.assertEqual(south["value"], "800")
        west = _t2_finding(run, STATEMENT_AMOUNT, self.west)
        self.assertEqual(west["value"], "400")


class ObservedMechanismLimits(unittest.TestCase):
    """Observation of the engine as it is, not a design.

    Where a blocked or inapplicable per-subject outcome goes, and what
    ``collect`` and ``count`` can express about a recorded link.
    """

    def setUp(self) -> None:
        self.north = _t2_box_fact_id(LENDER, STATEMENT_S1)
        self.link_inst = _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_INST)
        self.link_priv = _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_PRIV)
        self.link_south = _t2_link_fact_id(
            P2_LENDER_SOUTH, STATEMENT_S2, P2_BORROWING_PRIV
        )

    def _execute_false_guard(
        self, findings: dict[str, dict[str, Any]]
    ) -> _Run:
        rules = _p3b_rules()
        link = next(rule for rule in rules if rule["id"] == P3B_LINK_RULE)
        link["when"] = {"op": "compare", "cmp": "gt", "left": 0, "right": 1}
        state = FindingState(
            findings=dict(findings),
            fact_state=KernelState(fact_types=_t2_lattice()),
        )
        currency = compute_currency(state)
        ctx = marshal_run_context(
            run_id="demo.sli-a4-pass2-p3c-observe",
            state=state,
            currency=currency,
            rules=rules,
            parameters={
                T2_PARAM: {"id": T2_PARAM, "version": "v1", "values": "not-adverse"}
            },
            canon={},
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOVERNANCE_PINS,
            fact_types=_p3_fact_types(),
            input_bindings=[{
                "symbol": ENROLMENT,
                "fact_type": {"id": ENROLMENT, "version": "v1"},
                "mode": "optional_default",
            }],
            collect_source_names=[FINANCING, ENROLMENT, BOX1, STATEMENT_BORROWING],
        )
        run = _Run(ctx, SCHEMAS)
        by_id = {rule["id"]: rule for rule in rules}
        run.evaluate_subject_scoped_rule(
            subject_type=FINANCING, rule=by_id[T2_STATUS_RULE]
        )
        run.evaluate_subject_scoped_rule(
            subject_type=STATEMENT_BORROWING, rule=by_id[P3B_LINK_RULE]
        )
        run.evaluate_subject_scoped_rule(
            subject_type=BOX1, rule=by_id[P3B_AMOUNT_RULE]
        )
        return run

    def test_inapplicable_reduction_is_absent_from_later_sources(self) -> None:
        """Observation, not a design. A false guard is not a later source.

        Every recorded link's reduction is inapplicable. The statement
        rule still blocks on an empty collection. It does not see the
        inapplicable rows.
        """
        run = self._execute_false_guard(_p3_findings(corrected=False))
        for fact_id in (self.link_inst, self.link_priv, self.link_south):
            row = _t2_row(run, fact_id, P3B_LINK_REDUCTION)
            self.assertEqual(row["disposition"], "inapplicable")
            self.assertNotIn("code", row)
            self.assertTrue(any(
                source.name == STATEMENT_BORROWING and source.fact_id == fact_id
                for source in run.live_sources
            ))
        self.assertFalse(any(
            source.name == P3B_LINK_REDUCTION for source in run.live_sources
        ))
        self.assertFalse(any(
            symbol.startswith(P3B_LINK_REDUCTION + "|") for symbol in run.symbols
        ))
        self.assertFalse(any(
            entry.get("artifact_id") == P3B_LINK_RULE for entry in run.blocked
        ))
        north = _t2_row(run, self.north, STATEMENT_AMOUNT)
        self.assertEqual(north["disposition"], "blocked")
        self.assertEqual(north["code"], "SOURCE_SET_UNCLOSED")
        self.assertEqual(north["missing"], [P3B_LINK_REDUCTION])
        self.assertNotIn(P3_LINK_INST, north["missing"])
        self.assertNotIn(P3_LINK_INST, _input_ids(_pins(north)))

    def test_count_blocks_unless_the_source_set_is_closed(self) -> None:
        """Observation, not a design. Present rows do not satisfy ``count``.

        Comparing a link count with a reduction count blocks
        ``SOURCE_SET_UNCLOSED`` on the source set, before the comparison
        runs. The rows are present. The set is not admitted.
        """
        from packages.derivation.evaluator import AccessLog, Environment, EvalBlocked, evaluate

        env = Environment(
            {},
            {STATEMENT_BORROWING: ["1000", "500"], P3B_LINK_REDUCTION: ["0"]},
            frozenset(),
            {},
            {},
        )
        with self.assertRaises(EvalBlocked) as caught:
            evaluate(
                {
                    "op": "compare",
                    "cmp": "eq",
                    "left": {
                        "op": "count",
                        "name": STATEMENT_BORROWING,
                        "source_set": "demo.family.links",
                    },
                    "right": {
                        "op": "count",
                        "name": P3B_LINK_REDUCTION,
                        "source_set": "demo.family.reductions",
                    },
                },
                env,
                AccessLog(),
            )
        self.assertEqual(caught.exception.category, "SOURCE_SET_UNCLOSED")
        self.assertEqual(caught.exception.missing, ["demo.family.links"])

    def test_closed_counts_compare_as_a_bool_and_block_names_nothing(self) -> None:
        """Observation, not a design. Closure yields a bool, not a link id.

        Stuffing ``closed_sets`` is not how a run admits a family. Even
        then, unequal counts compare to false, and ``block`` records an
        empty missing list.
        """
        from packages.derivation.evaluator import AccessLog, Environment, EvalBlocked, evaluate

        env = Environment(
            {},
            {STATEMENT_BORROWING: ["1000", "500"], P3B_LINK_REDUCTION: ["0"]},
            frozenset({"demo.family.links", "demo.family.reductions"}),
            {},
            {},
        )
        compared = evaluate(
            {
                "op": "compare",
                "cmp": "eq",
                "left": {
                    "op": "count",
                    "name": STATEMENT_BORROWING,
                    "source_set": "demo.family.links",
                },
                "right": {
                    "op": "count",
                    "name": P3B_LINK_REDUCTION,
                    "source_set": "demo.family.reductions",
                },
            },
            env,
            AccessLog(),
        )
        self.assertIs(compared, False)
        with self.assertRaises(EvalBlocked) as caught:
            evaluate({"op": "block", "code": "DEPENDENCY_ABSENT"}, env, AccessLog())
        self.assertEqual(caught.exception.category, "DEPENDENCY_ABSENT")
        self.assertEqual(caught.exception.missing, [])

    def test_admitted_empty_collect_returns_empty_and_ignores_sibling_rows(self) -> None:
        """Observation, not a design. An admitted empty ``collect`` is [].

        A sibling link row is in the same environment and is not read.
        Subtracting that empty sum from 1500 yields 1500. A non-empty
        ``collect`` does not consult the source set at all, admitted or
        not. An unadmitted empty ``collect`` blocks on the source set.
        """
        from decimal import Decimal

        from packages.derivation.evaluator import AccessLog, Environment, EvalBlocked, evaluate

        family = "demo.family.reductions"
        admitted = Environment(
            {},
            {P3B_LINK_REDUCTION: [], STATEMENT_BORROWING: ["1000"]},
            frozenset({family}),
            {},
            {},
        )
        access = AccessLog()
        collected = evaluate(
            {"op": "collect", "name": P3B_LINK_REDUCTION, "source_set": family},
            admitted,
            access,
        )
        self.assertEqual(collected, [])
        self.assertEqual(access.collects, {P3B_LINK_REDUCTION})
        self.assertNotIn(STATEMENT_BORROWING, access.collects)
        self.assertEqual(access.closure_reads, {family})
        published = evaluate(
            {
                "op": "subtract",
                "left": 1500,
                "right": {
                    "op": "add",
                    "args": [{
                        "op": "collect",
                        "name": P3B_LINK_REDUCTION,
                        "source_set": family,
                    }],
                },
            },
            admitted,
            AccessLog(),
        )
        self.assertEqual(published, Decimal("1500"))

        present = evaluate(
            {"op": "collect", "name": P3B_LINK_REDUCTION, "source_set": family},
            Environment({}, {P3B_LINK_REDUCTION: ["0"]}, frozenset(), {}, {}),
            AccessLog(),
        )
        self.assertEqual(present, [Decimal("0")])

        with self.assertRaises(EvalBlocked) as caught:
            evaluate(
                {"op": "collect", "name": P3B_LINK_REDUCTION, "source_set": family},
                Environment(
                    {},
                    {P3B_LINK_REDUCTION: [], STATEMENT_BORROWING: ["1000"]},
                    frozenset(),
                    {},
                    {},
                ),
                AccessLog(),
            )
        self.assertEqual(caught.exception.category, "SOURCE_SET_UNCLOSED")
        self.assertEqual(caught.exception.missing, [family])


# --- P4. What a durable reader can recover. The run stays hand-driven. ---

_P4_RESPONSIBILITY = "demo.tax.responsibility.eligible-institution"
_P4_RESPONSIBILITY_RULE = "demo.rule.responsibility-eligible-institution"
_P4_RESPONSIBILITY_CITATION = "demo.citation.responsibility-eligible-institution"
_P4_DUPLICATE_LINK = "demo.finding.link.p3-inst-duplicate"


def _p4_completed_record(run: _Run) -> dict[str, Any]:
    """The live closing record. v9 omits the v1 published and blocked lists."""
    from packages.derivation.records import closing_record

    record = closing_record(
        record_id="record:demo.sli-a4-pass2-p4:completed",
        run_id=run.ctx.run_id,
        phase="completed",
        workspace_revision=0,
        governance_pins=list(GOVERNANCE_PINS),
        adoption_pin=dict(ADOPTION_PIN),
        stop_reason="saturated",
        published=[],
        blocked=list(run.blocked),
        dispositions=run.dispositions,
        use_v2=True,
    )
    SCHEMAS.validate_declared(record)
    return record


def _p4_out_document(run: _Run) -> dict[str, Any]:
    """The object ``live_coordinate_run`` writes, filled from this run.

    Standing authorization is not folded: there is no act log. The three
    authorization keys are the writer's, from an absent resolution.
    ``stop_reason`` is the completed-run value the writer stores; ``_Run``
    does not compute one. ``workspace_revision`` is not in this object.
    """
    from packages.derivation.authorization import STATUS_ABSENT, AuthorizationResolution

    resolution = AuthorizationResolution(STATUS_ABSENT)
    return {
        "run_id": run.ctx.run_id,
        "stop_reason": "saturated",
        "dispositions": run.dispositions,
        "current": resolution.admitted,
        "authorization_status": resolution.status,
        "authorization_grant_id": resolution.grant_id,
    }


def _p4_out_text(document: dict[str, Any]) -> str:
    return json.dumps(document, indent=2, sort_keys=True) + "\n"


def _p4_amount_field(symbol: str) -> dict[str, Any]:
    return {
        "schema": "form-field.v3",
        "id": "demo.field.statement-amount",
        "version": "v1",
        "form": {
            "authority": "IRS",
            "form_id": "1040",
            "tax_year": 2025,
            "jurisdiction": "US-federal",
        },
        "line": "1",
        "label": "Demo student loan interest",
        "description": "Synthetic statement amount for the durable-reader probe.",
        "binds_symbol": symbol,
        "citation": {"id": "demo.citation.statement-box-minus-reductions", "version": "v1"},
        "dispositions": {
            "published_value": {"render": "{value}", "explain": "e"},
        },
    }


def _p4_amount_members(symbol: str, *, join: bool) -> list[dict[str, Any]]:
    """Field plus the smallest members the projector asked for.

    ``join`` rewrites ``publishes`` to the keyed disposition symbol. The
    rule that ran publishes the unsuffixed name, and a published field
    rejects that pair. A blocked field does not consult it.
    """
    rule = next(rule for rule in _coverage_rules() if rule["id"] == P3B_AMOUNT_RULE)
    if join:
        rule = dict(rule)
        rule["publishes"] = symbol
    members: list[dict[str, Any]] = [_p4_amount_field(symbol), rule]
    if join:
        members.append(_citation())
    return members


def _p4_present(
    run: _Run,
    state: FindingState,
    symbol: str,
    *,
    join: bool,
) -> dict[str, Any]:
    from packages.derivation.presentation_projection import build_presentation_model

    return build_presentation_model(
        run_id=run.ctx.run_id,
        resolved_members=_p4_amount_members(symbol, join=join),
        state=state,
        publications=run.publications,
        dispositions=run.dispositions,
    )


def _p4_responsibility_rule() -> dict[str, Any]:
    """One condition, per the stage-4 candidate. Nothing reads it."""
    return _t2_rule(
        rule_id=_P4_RESPONSIBILITY_RULE,
        citation_id=_P4_RESPONSIBILITY_CITATION,
        role="applicability",
        requires=[STATUS],
        when=_t2_eq(STATUS, STATUS, "not-adverse"),
        value={
            "op": "category_literal",
            "fact_type": {"id": _P4_RESPONSIBILITY, "version": "v1"},
            "value": "applies",
        },
        publishes=_P4_RESPONSIBILITY,
    )


def _p4_row_by_symbol(rows: list[dict[str, Any]], symbol: str) -> dict[str, Any]:
    matched = [row for row in rows if row.get("symbol") == symbol]
    if len(matched) != 1:
        raise AssertionError(f"{symbol}: {[row.get('symbol') for row in rows]!r}")
    return matched[0]


class DurableReaderCoverageBlock(unittest.TestCase):
    """One uncovered link, then the three other ``DEPENDENCY_INVALID`` shapes.

    The run is ``_coverage_execute``. The readers are ``closing_record``,
    the ``out.json`` object, and ``build_presentation_model``.
    """

    def setUp(self) -> None:
        self.north = _t2_box_fact_id(LENDER, STATEMENT_S1)
        self.link_inst = _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_INST)
        self.link_priv = _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_PRIV)
        self.keyed = _t2_symbol(STATEMENT_AMOUNT, self.north)

    def _uncovered(self) -> tuple[FindingState, _Run]:
        findings = _p3_findings(corrected=False)
        del findings[T2_FIN_INST]
        state, _currency, _ctx, run = _coverage_execute(findings)
        return state, run

    def _non_numeric(self) -> tuple[FindingState, _Run]:
        state, _currency, _ctx, run = _coverage_execute(
            _p3_findings(corrected=True, inst_portion=P3_MEMBERSHIP)
        )
        return state, run

    def _orphan(self) -> tuple[FindingState, _Run]:
        state, _currency, _ctx, run = _coverage_execute(
            _p3_findings(corrected=False), statement=False
        )
        run.live_sources = [
            source for source in run.live_sources
            if not (
                source.name == STATEMENT_BORROWING
                and source.fact_id in {self.link_inst, self.link_priv}
            )
        ]
        rule = next(rule for rule in _coverage_rules() if rule["id"] == P3B_AMOUNT_RULE)
        run.evaluate_subject_scoped_rule(subject_type=BOX1, rule=rule)
        return state, run

    def _duplicate(self) -> tuple[FindingState, _Run]:
        """A second live source with the same keys. Not a second current finding.

        Currency keeps one current finding per fact. The duplicate-link
        shape is two sources, as the orphan test removes sources.
        """
        from packages.derivation.runner import SourceFact

        state, _currency, _ctx, run = _coverage_execute(
            _p3_findings(corrected=False), statement=False
        )
        original = next(source for source in run.live_sources if source.finding_id == P3_LINK_INST)
        run.live_sources.append(SourceFact(
            name=original.name,
            value=original.value,
            finding_id=_P4_DUPLICATE_LINK,
            fact_id="demo.fact.link.p3-inst-duplicate",
            keys=original.keys,
        ))
        rule = next(rule for rule in _coverage_rules() if rule["id"] == P3B_AMOUNT_RULE)
        run.evaluate_subject_scoped_rule(subject_type=BOX1, rule=rule)
        return state, run

    def test_one_code_and_the_link_id_do_not_survive_the_field(self) -> None:
        """The statement blocked, and which link, at each reader.

        Record and ``out.json``: identity of the uncovered link in
        ``missing`` and in the row's input pins. The other three shapes
        use the same code. Presentation keeps the code and drops both.
        """
        from packages.derivation.presentation_projection import PresentationModelError

        uncovered_state, uncovered = self._uncovered()
        nonnum_state, nonnum = self._non_numeric()
        orphan_state, orphan = self._orphan()
        duplicate_state, duplicate = self._duplicate()

        uncovered_row = _t2_row(uncovered, self.north, STATEMENT_AMOUNT)
        nonnum_row = _t2_row(nonnum, self.north, STATEMENT_AMOUNT)
        orphan_row = _t2_row(orphan, self.north, STATEMENT_AMOUNT)
        duplicate_row = _t2_row(duplicate, self.north, STATEMENT_AMOUNT)
        inst_reduction = _t2_finding(nonnum, P3B_LINK_REDUCTION, self.link_inst)
        orphan_inst = _t2_finding(orphan, P3B_LINK_REDUCTION, self.link_inst)
        orphan_priv = _t2_finding(orphan, P3B_LINK_REDUCTION, self.link_priv)

        self.assertEqual(uncovered_row["disposition"], "blocked")
        self.assertEqual(uncovered_row["code"], "DEPENDENCY_INVALID")
        self.assertEqual(uncovered_row["missing"], [P3_LINK_INST])
        self.assertNotIn("finding_id", uncovered_row)
        self.assertNotIn("value", uncovered_row)
        self.assertEqual(
            _input_ids(_pins(uncovered_row)),
            {T2_BOX_NORTH, P3_LINK_INST},
        )
        blocked_reduction = _t2_row(uncovered, self.link_inst, P3B_LINK_REDUCTION)
        self.assertEqual(blocked_reduction["disposition"], "blocked")
        self.assertEqual(blocked_reduction["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(blocked_reduction["missing"], [STATUS])
        self.assertIn(P3_LINK_INST, _input_ids(_pins(blocked_reduction)))

        self.assertEqual(nonnum_row["code"], "DEPENDENCY_INVALID")
        self.assertEqual(nonnum_row["missing"], [P3_LINK_INST])
        self.assertEqual(nonnum_row["missing"], uncovered_row["missing"])
        self.assertEqual(_input_ids(_pins(nonnum_row)), {T2_BOX_NORTH})
        self.assertNotIn(P3_LINK_INST, _input_ids(_pins(nonnum_row)))
        published_reduction = _t2_row(nonnum, self.link_inst, P3B_LINK_REDUCTION)
        self.assertEqual(published_reduction["disposition"], "published")
        self.assertEqual(published_reduction["finding_id"], inst_reduction["id"])
        self.assertEqual(inst_reduction["value"], P3_MEMBERSHIP)
        self.assertNotIn("value", published_reduction)
        self.assertIn(P3_LINK_INST, _input_ids(_pins(published_reduction)))

        self.assertEqual(orphan_row["code"], "DEPENDENCY_INVALID")
        self.assertEqual(orphan_row["missing"], sorted([orphan_inst["id"], orphan_priv["id"]]))
        self.assertNotIn(P3_LINK_INST, orphan_row["missing"])
        self.assertEqual(_input_ids(_pins(orphan_row)), {T2_BOX_NORTH})
        self.assertEqual(
            sorted(orphan_row["missing"]),
            sorted(
                row["finding_id"]
                for row in orphan.dispositions
                if row.get("finding_id") in set(orphan_row["missing"])
            ),
        )

        self.assertEqual(duplicate_row["code"], "DEPENDENCY_INVALID")
        self.assertEqual(duplicate_row["missing"], [P3_LINK_INST, _P4_DUPLICATE_LINK])
        self.assertEqual(_input_ids(_pins(duplicate_row)), {T2_BOX_NORTH})
        self.assertNotIn(_P4_DUPLICATE_LINK, uncovered_state.findings)
        self.assertNotIn(
            _P4_DUPLICATE_LINK,
            {pin["id"] for row in duplicate.dispositions for pin in _pins(row)},
        )

        for run in (uncovered, nonnum, orphan, duplicate):
            record = _p4_completed_record(run)
            document = _p4_out_document(run)
            self.assertEqual(record["schema"], "derivation-record.v9")
            self.assertNotIn("published", record)
            self.assertNotIn("blocked", record)
            self.assertNotIn("subject_fact_id", json.dumps(record))
            self.assertEqual(document["dispositions"], record["dispositions"])
            self.assertEqual(
                set(document),
                {
                    "run_id",
                    "stop_reason",
                    "dispositions",
                    "current",
                    "authorization_status",
                    "authorization_grant_id",
                },
            )
            self.assertIs(document["current"], False)
            self.assertEqual(document["authorization_status"], "AUTHORIZATION_ABSENT")
            self.assertIsNone(document["authorization_grant_id"])
            self.assertEqual(document["stop_reason"], "saturated")
            parsed = json.loads(_p4_out_text(document))
            self.assertEqual(parsed["dispositions"], record["dispositions"])
            self.assertNotIn("value", json.dumps(record["dispositions"]))

        self.assertNotIn(P3_MEMBERSHIP, json.dumps(_p4_completed_record(nonnum)))

        with self.assertRaises(PresentationModelError) as unsuffixed:
            _p4_present(uncovered, uncovered_state, STATEMENT_AMOUNT, join=False)
        self.assertIn("0 row(s)", str(unsuffixed.exception))

        models = [
            _p4_present(uncovered, uncovered_state, self.keyed, join=False),
            _p4_present(nonnum, nonnum_state, self.keyed, join=False),
            _p4_present(orphan, orphan_state, self.keyed, join=False),
            _p4_present(duplicate, duplicate_state, self.keyed, join=False),
        ]
        resolved = {"disposition": "blocked", "activeCodes": ["DEPENDENCY_INVALID"], "act": None}
        for model in models:
            self.assertEqual(model["sections"][0]["resolved"], resolved)
            self.assertEqual(model["sections"][0]["citationSites"], [])
            self.assertNotIn("provenanceGroups", model)
        dumped = [json.dumps(model) for model in models]
        for blob in dumped:
            self.assertNotIn(P3_LINK_INST, blob)
            self.assertNotIn(_P4_DUPLICATE_LINK, blob)
            self.assertNotIn(P3_MEMBERSHIP, blob)
            self.assertNotIn("missing", blob)
        self.assertEqual(dumped[0], dumped[1])
        self.assertEqual(dumped[0], dumped[2])
        self.assertEqual(dumped[0], dumped[3])


class DurableReaderNoLinkDefault(unittest.TestCase):
    """West has a box and no link. The amount is the declared parameter."""

    def setUp(self) -> None:
        self.west = _t2_box_fact_id(T2_LENDER_WEST, STATEMENT_S3)
        self.keyed = _t2_symbol(STATEMENT_AMOUNT, self.west)
        self.parameter_id = _parameter()["id"]

    def test_citation_walk_names_the_box_and_not_the_parameter(self) -> None:
        """The parameter pin is on the row and on the embedded finding.

        ``citationSites`` does not carry it. The unsuffixed amount symbol
        joins nothing. The rule that ran does not own the keyed symbol.
        """
        from packages.derivation.presentation_projection import PresentationModelError

        state, _currency, _ctx, run = _coverage_execute(_p3_findings(corrected=False))
        row = _t2_row(run, self.west, STATEMENT_AMOUNT)
        finding = _t2_finding(run, STATEMENT_AMOUNT, self.west)
        record = _p4_completed_record(run)
        document = _p4_out_document(run)
        recorded = _p4_row_by_symbol(record["dispositions"], self.keyed)

        self.assertEqual(row["disposition"], "published")
        self.assertEqual(finding["value"], "400")
        self.assertNotIn("value", recorded)
        self.assertEqual(recorded["finding_id"], finding["id"])
        self.assertEqual(
            {pin["id"] for pin in _pins(recorded) if pin["role"] == "parameter"},
            {self.parameter_id},
        )
        self.assertEqual(_input_ids(_pins(recorded)), {T2_BOX_WEST})
        self.assertNotIn(P3_LINK_INST, _input_ids(_pins(recorded)))
        self.assertNotIn("resolved_input", finding)
        self.assertEqual(document["dispositions"], record["dispositions"])
        self.assertTrue(all("value" not in row for row in record["dispositions"]))

        with self.assertRaises(PresentationModelError) as unsuffixed:
            _p4_present(run, state, STATEMENT_AMOUNT, join=False)
        self.assertIn("0 row(s)", str(unsuffixed.exception))
        with self.assertRaises(PresentationModelError) as unjoined:
            _p4_present(run, state, self.keyed, join=False)
        self.assertIn("lacks a joined owning rule", str(unjoined.exception))

        model = _p4_present(run, state, self.keyed, join=True)
        section = model["sections"][0]
        self.assertEqual(section["resolved"]["disposition"], "published_value")
        self.assertEqual(section["resolved"]["value"], 400)
        self.assertEqual(
            [site["pinId"] for site in section["citationSites"]],
            [T2_BOX_WEST],
        )
        embedded = section["resolved"]["act"]["finding"]
        self.assertEqual(
            {pin["id"] for pin in embedded["pins"] if pin["role"] == "parameter"},
            {self.parameter_id},
        )
        self.assertNotIn(self.parameter_id, {site["pinId"] for site in section["citationSites"]})
        self.assertNotIn("provenanceGroups", model)
        self.assertEqual(model["citationGroups"], [])


class DurableReaderCoveredReduction(unittest.TestCase):
    """Box 1 minus both reductions, after the enrolment correction.

    The private status pins a declared default. That finding is recorded
    once, so the two-link walk can finish. The one-link chain below has
    no default hop.
    """

    def setUp(self) -> None:
        self.north = _t2_box_fact_id(LENDER, STATEMENT_S1)
        self.keyed = _t2_symbol(STATEMENT_AMOUNT, self.north)
        self.link_inst = _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_INST)
        self.link_priv = _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_PRIV)
        self.inst = _t2_financing_fact_id(P2_BORROWING_INST, PERIOD_AUTUMN)
        self.priv = _t2_financing_fact_id(P2_BORROWING_PRIV, PERIOD_SPRING)

    def test_the_chain_is_a_join_and_the_two_link_walk_is_rejected(self) -> None:
        """Record: amount, reduction, status, corrected enrolment, by pin id.

        No values. Presentation of that same run used to refuse: the private
        status pinned a declared-default id that was not a recorded finding.
        That refusal was a defect, now repaired. The field's citation sites
        are the recorded leaves, and the default id is a recorded finding.
        A chain whose leaves are all recorded flattens to those leaves and
        does not emit the status or the reduction.
        """
        from packages.derivation.presentation_projection import PresentationModelError

        state, _currency, _ctx, run = _coverage_execute(_p3_findings(corrected=True))
        amount = _t2_finding(run, STATEMENT_AMOUNT, self.north)
        inst_reduction = _t2_finding(run, P3B_LINK_REDUCTION, self.link_inst)
        priv_reduction = _t2_finding(run, P3B_LINK_REDUCTION, self.link_priv)
        inst_status = _t2_finding(run, STATUS, self.inst)
        priv_status = _t2_finding(run, STATUS, self.priv)
        record = _p4_completed_record(run)
        document = _p4_out_document(run)
        self.assertEqual(document["dispositions"], record["dispositions"])

        amount_row = _p4_row_by_symbol(record["dispositions"], self.keyed)
        inst_reduction_row = _p4_row_by_symbol(
            record["dispositions"], _t2_symbol(P3B_LINK_REDUCTION, self.link_inst)
        )
        priv_reduction_row = _p4_row_by_symbol(
            record["dispositions"], _t2_symbol(P3B_LINK_REDUCTION, self.link_priv)
        )
        inst_status_row = _p4_row_by_symbol(
            record["dispositions"], _t2_symbol(STATUS, self.inst)
        )
        priv_status_row = _p4_row_by_symbol(
            record["dispositions"], _t2_symbol(STATUS, self.priv)
        )

        self.assertEqual(amount["value"], "500")
        self.assertEqual(inst_reduction["value"], "1000")
        self.assertEqual(priv_reduction["value"], "0")
        self.assertEqual(inst_status["value"], "adverse")
        self.assertEqual(priv_status["value"], "not-adverse")
        self.assertNotIn("value", amount_row)
        self.assertEqual(
            _input_ids(_pins(amount_row)),
            {T2_BOX_NORTH, P3_LINK_INST, P3_LINK_PRIV, inst_reduction["id"], priv_reduction["id"]},
        )
        self.assertNotIn(inst_status["id"], _input_ids(_pins(amount_row)))
        self.assertNotIn(T2_ENROL_LATER, _input_ids(_pins(amount_row)))
        self.assertEqual(inst_reduction_row["finding_id"], inst_reduction["id"])
        self.assertEqual(priv_reduction_row["finding_id"], priv_reduction["id"])
        self.assertEqual(
            _input_ids(_pins(inst_reduction_row)),
            {P3_LINK_INST, inst_status["id"]},
        )
        self.assertEqual(
            _input_ids(_pins(priv_reduction_row)),
            {P3_LINK_PRIV, priv_status["id"]},
        )
        self.assertEqual(inst_status_row["artifact_id"], T2_STATUS_RULE)
        self.assertEqual(inst_status_row["finding_id"], inst_status["id"])
        self.assertEqual(
            _input_ids(_pins(inst_status_row)),
            {T2_FIN_INST, T2_ENROL_LATER},
        )
        self.assertNotIn(T2_ENROL_EARLIER, _input_ids(_pins(inst_status_row)))
        self.assertEqual(
            next(
                pin["origin"]
                for pin in _pins(inst_status_row)
                if pin["id"] == T2_ENROL_LATER
            ),
            "assertion",
        )
        default_id = next(
            pin["id"] for pin in _pins(priv_status_row) if pin.get("origin") == "declared_default"
        )
        self.assertNotIn(default_id, state.findings)
        recorded = [pub.finding for pub in run.publications if pub.finding["id"] == default_id]
        self.assertEqual(len(recorded), 1)
        self.assertEqual(recorded[0]["schema"], "derived-finding.v2")
        self.assertEqual(recorded[0]["symbol"], ENROLMENT)
        self.assertEqual(recorded[0]["value"], "not-adverse")
        self.assertEqual(
            recorded[0]["resolved_input"],
            {"fact_id": ENROLMENT, "origin": "declared_default"},
        )
        self.assertFalse(any(row.get("finding_id") == default_id for row in record["dispositions"]))
        self.assertTrue(all("value" not in row for row in record["dispositions"]))

        with self.assertRaises(PresentationModelError) as unjoined:
            _p4_present(run, state, self.keyed, join=False)
        self.assertIn("lacks a joined owning rule", str(unjoined.exception))

        model = _p4_present(run, state, self.keyed, join=True)
        section = model["sections"][0]
        self.assertEqual(section["resolved"]["disposition"], "published_value")
        self.assertEqual(section["resolved"]["value"], 500)
        citation_ids = {site["pinId"] for site in section["citationSites"]}
        self.assertEqual(
            citation_ids,
            {
                T2_BOX_NORTH,
                P3_LINK_INST,
                P3_LINK_PRIV,
                T2_FIN_INST,
                T2_FIN_PRIV,
                T2_ENROL_LATER,
            },
        )
        self.assertNotIn(default_id, citation_ids)
        self.assertNotIn(T2_ENROL_EARLIER, citation_ids)
        self.assertIn(default_id, {pub.finding["id"] for pub in run.publications})
        top_pins = section["resolved"]["act"]["finding"]["pins"]
        self.assertIn(inst_reduction["id"], {pin["id"] for pin in top_pins})
        self.assertIn(priv_reduction["id"], {pin["id"] for pin in top_pins})
        blob = json.dumps(model)
        self.assertNotIn(inst_status["id"], blob)
        self.assertNotIn(priv_status["id"], blob)
        self.assertNotIn(default_id, blob)
        self.assertNotIn(STATUS, blob)
        self.assertNotIn(P3B_LINK_REDUCTION, blob)

        one_link = _p3_findings(corrected=True)
        del one_link[P3_LINK_PRIV]
        del one_link[P3_LINK_SOUTH]
        del one_link[T2_FIN_PRIV]
        one_state, _one_currency, _one_ctx, one_run = _coverage_execute(one_link)
        one_amount = _t2_finding(one_run, STATEMENT_AMOUNT, self.north)
        one_reduction = _t2_finding(one_run, P3B_LINK_REDUCTION, self.link_inst)
        one_status = _t2_finding(one_run, STATUS, self.inst)
        self.assertEqual(one_amount["value"], "500")
        self.assertNotIn(
            default_id,
            {pin["id"] for pin in one_status["pins"]},
        )
        with self.assertRaises(PresentationModelError) as unjoined:
            _p4_present(one_run, one_state, self.keyed, join=False)
        self.assertIn("lacks a joined owning rule", str(unjoined.exception))

        model = _p4_present(one_run, one_state, self.keyed, join=True)
        section = model["sections"][0]
        self.assertEqual(section["resolved"]["disposition"], "published_value")
        self.assertEqual(section["resolved"]["value"], 500)
        self.assertEqual(
            {site["pinId"] for site in section["citationSites"]},
            {T2_BOX_NORTH, P3_LINK_INST, T2_FIN_INST, T2_ENROL_LATER},
        )
        self.assertNotIn(T2_ENROL_EARLIER, {site["pinId"] for site in section["citationSites"]})
        top_pins = section["resolved"]["act"]["finding"]["pins"]
        self.assertIn(one_reduction["id"], {pin["id"] for pin in top_pins})
        blob = json.dumps(model)
        self.assertNotIn(one_status["id"], blob)
        self.assertNotIn(STATUS, blob)
        self.assertNotIn(P3B_LINK_REDUCTION, blob)
        self.assertNotIn(one_reduction["value"], blob)
        self.assertNotIn("provenanceGroups", model)


class DurableReaderNamedConclusion(unittest.TestCase):
    """The status rule is already in the coverage chain.

    One disposable responsibility rule publishes when that status is
    not-adverse. It is not an input of the amount. No field is bound to it.
    """

    def setUp(self) -> None:
        self.north = _t2_box_fact_id(LENDER, STATEMENT_S1)
        self.west = _t2_box_fact_id(T2_LENDER_WEST, STATEMENT_S3)
        self.keyed = _t2_symbol(STATEMENT_AMOUNT, self.north)
        self.west_keyed = _t2_symbol(STATEMENT_AMOUNT, self.west)
        self.inst = _t2_financing_fact_id(P2_BORROWING_INST, PERIOD_AUTUMN)
        self.priv = _t2_financing_fact_id(P2_BORROWING_PRIV, PERIOD_SPRING)
        self.link_inst = _t2_link_fact_id(LENDER, STATEMENT_S1, P2_BORROWING_INST)

    def test_the_conclusion_and_the_responsibility_are_not_on_the_field(self) -> None:
        """Status: identity on its own row, value nowhere durable.

        The responsibility row is the same shape. The amount's presentation
        does not contain it. A statement subject does not publish one.
        """
        state, _currency, _ctx, run = _coverage_execute(_p3_findings(corrected=True))
        rule = _p4_responsibility_rule()
        run.evaluate_subject_scoped_rule(subject_type=FINANCING, rule=rule)
        run.evaluate_subject_scoped_rule(subject_type=BOX1, rule=rule)

        inst_status = _t2_finding(run, STATUS, self.inst)
        priv_status = _t2_finding(run, STATUS, self.priv)
        responsibility = _t2_finding(run, _P4_RESPONSIBILITY, self.priv)
        record = _p4_completed_record(run)
        document = _p4_out_document(run)
        self.assertEqual(document["dispositions"], record["dispositions"])

        status_row = _p4_row_by_symbol(record["dispositions"], _t2_symbol(STATUS, self.inst))
        self.assertEqual(inst_status["value"], "adverse")
        self.assertEqual(status_row["artifact_id"], T2_STATUS_RULE)
        self.assertEqual(status_row["symbol"], _t2_symbol(STATUS, self.inst))
        self.assertEqual(status_row["finding_id"], inst_status["id"])
        self.assertNotIn("value", status_row)
        self.assertTrue(all("value" not in row for row in record["dispositions"]))

        priv_responsibility = _p4_row_by_symbol(
            record["dispositions"], _t2_symbol(_P4_RESPONSIBILITY, self.priv)
        )
        inst_responsibility = _p4_row_by_symbol(
            record["dispositions"], _t2_symbol(_P4_RESPONSIBILITY, self.inst)
        )
        self.assertEqual(responsibility["value"], "applies")
        self.assertEqual(priv_responsibility["disposition"], "published")
        self.assertEqual(priv_responsibility["artifact_id"], _P4_RESPONSIBILITY_RULE)
        self.assertEqual(priv_responsibility["finding_id"], responsibility["id"])
        self.assertNotIn("value", priv_responsibility)
        self.assertEqual(
            _input_ids(_pins(priv_responsibility)),
            {T2_FIN_PRIV, priv_status["id"]},
        )
        self.assertEqual(inst_responsibility["disposition"], "inapplicable")
        self.assertIs(inst_responsibility["guard_result"], False)
        self.assertNotIn("finding_id", inst_responsibility)
        self.assertIn(inst_status["id"], _input_ids(_pins(inst_responsibility)))
        self.assertNotIn("applies", json.dumps(record))
        self.assertFalse(any(
            responsibility["id"] in {pin["id"] for pin in _pins(row)}
            for row in record["dispositions"]
            if row.get("symbol") != priv_responsibility["symbol"]
        ))

        amount_row = _p4_row_by_symbol(record["dispositions"], self.keyed)
        reduction_row = _p4_row_by_symbol(
            record["dispositions"], _t2_symbol(P3B_LINK_REDUCTION, self.link_inst)
        )
        self.assertIn(reduction_row["finding_id"], _input_ids(_pins(amount_row)))
        self.assertIn(inst_status["id"], _input_ids(_pins(reduction_row)))
        self.assertNotIn(responsibility["id"], _input_ids(_pins(amount_row)))

        for fact_id in (self.north, self.west):
            statement_row = _p4_row_by_symbol(
                record["dispositions"], _t2_symbol(_P4_RESPONSIBILITY, fact_id)
            )
            self.assertEqual(statement_row["disposition"], "blocked")
            self.assertEqual(statement_row["code"], "DEPENDENCY_ABSENT")
            self.assertEqual(statement_row["missing"], [STATUS])
            self.assertNotIn("finding_id", statement_row)

        west_model = _p4_present(run, state, self.west_keyed, join=True)
        blob = json.dumps(west_model)
        self.assertNotIn(_P4_RESPONSIBILITY, blob)
        self.assertNotIn(_P4_RESPONSIBILITY_RULE, blob)
        self.assertNotIn(responsibility["id"], blob)
        self.assertNotIn(inst_status["id"], blob)
        self.assertNotIn("applies", blob)
        self.assertNotIn("provenanceGroups", west_model)
        self.assertEqual(
            [site["pinId"] for site in west_model["sections"][0]["citationSites"]],
            [T2_BOX_WEST],
        )


if __name__ == "__main__":
    unittest.main()
