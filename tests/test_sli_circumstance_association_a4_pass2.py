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


if __name__ == "__main__":
    unittest.main()
