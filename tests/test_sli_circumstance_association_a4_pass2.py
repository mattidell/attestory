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
from packages.derivation.runner import RunContext, RunResult, run
from packages.kernel.currency import CurrencyView
from packages.kernel.facts import fact_id_for

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


if __name__ == "__main__":
    unittest.main()
