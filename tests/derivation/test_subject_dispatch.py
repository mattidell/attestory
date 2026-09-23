"""Per-subject dispatch: one outcome per collected subject.

P1's questions, now required to pass. Synthetic ``demo.*`` identities only.
Subjects are the collected sources marshal already keeps; the dispatch
evaluates the declared rule once each. A period with no circumstance
finding takes that symbol's declared not-adverse default, and only that
period's. Sort order of finding ids does not choose the outcome.
"""

from __future__ import annotations

import json
import unittest
from typing import Any

from packages.derivation.evaluator import AccessLog
from packages.derivation.loader import DerivationSchemas
from packages.derivation.marshal import marshal_run_context
from packages.derivation.records import closing_record
from packages.derivation.runner import RunContext, _Run, _content_id, _sorted_pins, _value_str
from packages.kernel.currency import CurrencyView
from packages.kernel.facts import KernelState, fact_id_for

FINANCING = "demo.tax.financing-claim"
CIRCUMSTANCE = "demo.tax.schooling-circumstance"
SUPPORT = "demo.tax.period-support"
BOX1 = "demo.tax.f1098e.box1-student-loan-interest"
WITNESS = "demo.tax.box1-witness"
CONCLUSION = "demo.tax.no-enumerated-adverse"
RULE_ID = "demo.rule.no-enumerated-adverse"
RULE_VERSION = "v1"
CITATION_A = "demo.citation.no-enumerated-adverse"
CITATION_B = "demo.citation.no-enumerated-adverse.second"
FAVOURABLE = "no-enumerated-adverse"
PARAM_ID = "demo.parameter.circumstance-default"
ADOPTION_PIN = {"role": "adoption", "id": "demo.package.subject-dispatch", "version": "v1"}
GOVERNANCE_PINS = [{"role": "governance", "id": "demo.governance.probe", "version": "v1"}]

BORROWING = "demo.borrowing.one"
INSTITUTION = "demo.institution.riverside"
PROGRAMME = "demo.programme.bsc"
STUDENT = "demo.student.filer"
LENDER = "demo.lender.north"
YEAR = "2025"
PERIOD_AUTUMN = "2024-autumn"
PERIOD_SPRING = "2025-spring"
PERIOD_SUMMER = "2025-summer"

AUTUMN_FINDING = "demo.finding.financing.1-autumn"
SPRING_FINDING = "demo.finding.financing.2-spring"
SUMMER_FINDING = "demo.finding.financing.3-summer"
CIRCUMSTANCE_FINDING = "demo.finding.circumstance.adverse"
SUPPORT_AUTUMN_FINDING = "demo.finding.support.autumn"
SUPPORT_SPRING_FINDING = "demo.finding.support.spring"

BOX_S1_FINDING = "demo.finding.box1.1-s1"
BOX_S2_FINDING = "demo.finding.box1.2-s2"
STATEMENT_S1 = "demo.statement.s1"
STATEMENT_S2 = "demo.statement.s2"

BOX_BLOCKED_FINDING = "demo.finding.box1.1-blocked"
BOX_PUBLISHED_FINDING = "demo.finding.box1.2-published"
WITNESS_FINDING = "demo.finding.witness.published"
STATEMENT_BLOCKED = "demo.statement.1-blocked"
STATEMENT_PUBLISHED = "demo.statement.2-published"

SCHEMAS = DerivationSchemas()


class _HorizonState:
    def __init__(self) -> None:
        self.current_by_chain: dict[tuple[str, str, str], str] = {}


class _State:
    def __init__(
        self,
        findings: dict[str, dict[str, Any]],
        lattice: dict[str, dict[str, Any]],
    ) -> None:
        self.findings = findings
        self.horizon_state = _HorizonState()
        self.fact_state = KernelState(fact_types=lattice)


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


def _literal_type(
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


def _support_fact_id(period: str) -> str:
    return fact_id_for(SUPPORT, (("period", period),))


def _box_fact_id(statement: str) -> str:
    return fact_id_for(
        BOX1,
        (("lender", LENDER), ("statement", statement), ("tax-year", YEAR)),
    )


def _witness_fact_id(statement: str) -> str:
    return fact_id_for(
        WITNESS,
        (("lender", LENDER), ("statement", statement), ("tax-year", YEAR)),
    )


def _eq(name: str, fact_type: str, value: str) -> dict[str, Any]:
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


def _gt(name: str) -> dict[str, Any]:
    return {
        "op": "compare",
        "cmp": "gt",
        "left": {"op": "ref", "name": name},
        "right": 0,
    }


def _all(*terms: dict[str, Any]) -> dict[str, Any]:
    return {"op": "all", "args": list(terms)}


def _rule(*, requires: list[str], when: dict[str, Any]) -> dict[str, Any]:
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
        "citations": [
            {"id": CITATION_A, "version": "v1"},
            {"id": CITATION_B, "version": "v2"},
        ],
    }


def _run_fact(type_id: str, values: list[str], *, default: bool = False) -> dict[str, Any]:
    fact: dict[str, Any] = {
        "id": type_id,
        "version": "v1",
        "value_schema": {"enum": values},
    }
    if default:
        fact["optional_default"] = {"parameter": {"id": PARAM_ID, "version": "v1"}}
    return fact


def _default_finding_id(ctx: RunContext) -> str:
    """The ordinary optional-default content id for the circumstance symbol."""
    pins = _sorted_pins([
        ctx.adoption_pin,
        *ctx.governance_pins,
        {"role": "parameter", "id": PARAM_ID, "version": "v1"},
    ])
    body = {
        "symbol": CIRCUMSTANCE,
        "value": _value_str(ctx.parameters[PARAM_ID]["values"]),
        "pins": pins,
        "resolved_input": {"fact_id": CIRCUMSTANCE, "origin": "declared_default"},
    }
    return _content_id("finding:derived:", body)


def _ids(pins: list[dict[str, Any]], role: str) -> set[str]:
    return {str(pin["id"]) for pin in pins if pin["role"] == role}


def _origins(pins: list[dict[str, Any]]) -> dict[str, str]:
    return {
        str(pin["id"]): str(pin["origin"])
        for pin in pins
        if pin["role"] == "input"
    }


def _symbol(fact_id: str) -> str:
    return f"{CONCLUSION}|{fact_id}"


def _dispatch(
    findings: dict[str, dict[str, Any]],
    rule: dict[str, Any],
    *,
    subject_type: str,
    collect: list[str],
    lattice: dict[str, dict[str, Any]],
    fact_types: list[dict[str, Any]] | None = None,
    bindings: list[dict[str, Any]] | None = None,
    parameters: dict[str, dict[str, Any]] | None = None,
) -> tuple[RunContext, _Run, Any]:
    ctx = marshal_run_context(
        run_id="demo.subject-dispatch",
        state=_State(findings, lattice),  # type: ignore[arg-type]
        currency=_currency(list(findings)),
        rules=[rule],
        parameters={} if parameters is None else parameters,
        canon={},
        adoption_pin=ADOPTION_PIN,
        governance_pins=GOVERNANCE_PINS,
        fact_types=fact_types,
        input_bindings=bindings,
        collect_source_names=collect,
    )
    run = _Run(ctx, SCHEMAS)
    result = run.evaluate_subject_scoped_rule(subject_type=subject_type, rule=rule)
    return ctx, run, result


def _row(run: _Run, disposition: str, symbol: str) -> dict[str, Any]:
    matches = [
        row for row in run.dispositions
        if row["disposition"] == disposition and row.get("symbol") == symbol
    ]
    if len(matches) != 1:
        raise AssertionError(f"{disposition} {symbol}: {run.dispositions!r}")
    return matches[0]


def _publication(run: _Run, symbol: str) -> dict[str, Any]:
    matches = [pub.finding for pub in run.publications if pub.finding["symbol"] == symbol]
    if len(matches) != 1:
        raise AssertionError(f"publication {symbol}: {[pub.finding['symbol'] for pub in run.publications]!r}")
    return matches[0]


class StudentAndPeriod(unittest.TestCase):
    """Two financing claims. The adverse circumstance follows its period, not sort order."""

    def _period(self, adverse_period: str) -> tuple[RunContext, _Run, str, str]:
        autumn = _financing_fact_id(PERIOD_AUTUMN)
        spring = _financing_fact_id(PERIOD_SPRING)
        adverse_fact = _circumstance_fact_id(adverse_period)
        findings = {
            AUTUMN_FINDING: _finding(AUTUMN_FINDING, autumn, "tuition"),
            SPRING_FINDING: _finding(SPRING_FINDING, spring, "tuition"),
            CIRCUMSTANCE_FINDING: _finding(CIRCUMSTANCE_FINDING, adverse_fact, "adverse"),
        }
        periods = (PERIOD_AUTUMN, PERIOD_SPRING)
        lattice = {
            FINANCING: _literal_type(FINANCING, (
                ("borrowing", (BORROWING,)),
                ("period", periods),
                ("institution", (INSTITUTION,)),
                ("programme", (PROGRAMME,)),
            )),
            CIRCUMSTANCE: _literal_type(CIRCUMSTANCE, (
                ("student", (STUDENT,)),
                ("period", periods),
            )),
        }
        rule = _rule(
            requires=[FINANCING, CIRCUMSTANCE],
            when=_all(
                _eq(FINANCING, FINANCING, "tuition"),
                _eq(CIRCUMSTANCE, CIRCUMSTANCE, "not-adverse"),
            ),
        )
        ctx, run, _result = _dispatch(
            findings,
            rule,
            subject_type=FINANCING,
            collect=[FINANCING, CIRCUMSTANCE],
            lattice=lattice,
            fact_types=[
                _run_fact(FINANCING, ["tuition"]),
                _run_fact(CIRCUMSTANCE, ["adverse", "not-adverse"], default=True),
            ],
            bindings=[{
                "symbol": CIRCUMSTANCE,
                "fact_type": {"id": CIRCUMSTANCE, "version": "v1"},
                "mode": "optional_default",
            }],
            parameters={
                PARAM_ID: {"id": PARAM_ID, "version": "v1", "values": "not-adverse"},
            },
        )
        return ctx, run, autumn, spring

    def test_student_and_period_follows_the_adverse_period_not_sort_order(self) -> None:
        self.assertLess(AUTUMN_FINDING, SPRING_FINDING)
        for adverse_period, published_period, published_finding, withheld_finding in (
            (PERIOD_SPRING, PERIOD_AUTUMN, AUTUMN_FINDING, SPRING_FINDING),
            (PERIOD_AUTUMN, PERIOD_SPRING, SPRING_FINDING, AUTUMN_FINDING),
        ):
            with self.subTest(adverse=adverse_period):
                ctx, run, autumn, spring = self._period(adverse_period)
                published_fact = autumn if published_period == PERIOD_AUTUMN else spring
                withheld_fact = spring if published_fact == autumn else autumn
                published_symbol = _symbol(published_fact)
                withheld_symbol = _symbol(withheld_fact)
                default_id = _default_finding_id(ctx)

                financing = [source for source in ctx.sources if source.name == FINANCING]
                self.assertEqual(
                    {source.finding_id for source in financing},
                    {AUTUMN_FINDING, SPRING_FINDING},
                )
                self.assertTrue(all(source.keys is not None for source in financing))
                self.assertEqual(
                    [item.finding_id for item in ctx.inputs if item.symbol == CIRCUMSTANCE],
                    [CIRCUMSTANCE_FINDING],
                )

                finding = _publication(run, published_symbol)
                self.assertEqual(finding["value"], FAVOURABLE)
                self.assertEqual(_origins(finding["pins"]), {
                    published_finding: "assertion",
                    default_id: "declared_default",
                })
                self.assertNotIn(withheld_finding, _ids(finding["pins"], "input"))
                self.assertNotIn(CIRCUMSTANCE_FINDING, _ids(finding["pins"], "input"))
                self.assertEqual(_ids(finding["pins"], "adoption"), {ADOPTION_PIN["id"]})
                self.assertEqual(_ids(finding["pins"], "governance"), {GOVERNANCE_PINS[0]["id"]})
                self.assertEqual(_ids(finding["pins"], "citation"), {CITATION_A, CITATION_B})

                published_row = _row(run, "published", published_symbol)
                self.assertEqual(published_row["finding_id"], finding["id"])
                self.assertIn(published_fact, published_row["symbol"])

                withheld = _row(run, "inapplicable", withheld_symbol)
                self.assertIs(withheld["guard_result"], False)
                self.assertNotIn("finding_id", withheld)
                self.assertEqual(_origins(withheld["pins"]), {
                    withheld_finding: "assertion",
                    CIRCUMSTANCE_FINDING: "assertion",
                })
                self.assertNotIn(published_finding, _ids(withheld["pins"], "input"))
                self.assertIn(withheld_fact, withheld["symbol"])
                self.assertEqual(
                    {row.get("symbol") for row in run.dispositions},
                    {published_symbol, withheld_symbol},
                )
                self.assertNotIn(
                    withheld_symbol,
                    {pub.finding["symbol"] for pub in run.publications},
                )


class StatementSubjects(unittest.TestCase):
    def test_each_box1_statement_pins_only_its_own_finding(self) -> None:
        s1 = _box_fact_id(STATEMENT_S1)
        s2 = _box_fact_id(STATEMENT_S2)
        findings = {
            BOX_S1_FINDING: _finding(BOX_S1_FINDING, s1, 1500),
            BOX_S2_FINDING: _finding(BOX_S2_FINDING, s2, 2500),
        }
        lattice = {
            BOX1: _literal_type(BOX1, (
                ("lender", (LENDER,)),
                ("statement", (STATEMENT_S1, STATEMENT_S2)),
                ("tax-year", (YEAR,)),
            )),
        }
        rule = _rule(requires=[BOX1], when=_gt(BOX1))
        ctx, run, _result = _dispatch(
            findings,
            rule,
            subject_type=BOX1,
            collect=[BOX1],
            lattice=lattice,
        )
        self.assertEqual(
            {source.finding_id for source in ctx.sources if source.name == BOX1},
            {BOX_S1_FINDING, BOX_S2_FINDING},
        )
        by_symbol = {pub.finding["symbol"]: pub.finding for pub in run.publications}
        self.assertEqual(set(by_symbol), {_symbol(s1), _symbol(s2)})
        self.assertEqual(_origins(by_symbol[_symbol(s1)]["pins"]), {BOX_S1_FINDING: "assertion"})
        self.assertEqual(_origins(by_symbol[_symbol(s2)]["pins"]), {BOX_S2_FINDING: "assertion"})
        self.assertNotEqual(by_symbol[_symbol(s1)]["id"], by_symbol[_symbol(s2)]["id"])
        self.assertNotIn(STATEMENT_S1, by_symbol[_symbol(s2)]["symbol"])
        self.assertNotIn(STATEMENT_S2, by_symbol[_symbol(s1)]["symbol"])

    def test_published_conclusions_carry_the_rule_citations_pins_for_yields(self) -> None:
        s1 = _box_fact_id(STATEMENT_S1)
        s2 = _box_fact_id(STATEMENT_S2)
        findings = {
            BOX_S1_FINDING: _finding(BOX_S1_FINDING, s1, 1500),
            BOX_S2_FINDING: _finding(BOX_S2_FINDING, s2, 2500),
        }
        lattice = {
            BOX1: _literal_type(BOX1, (
                ("lender", (LENDER,)),
                ("statement", (STATEMENT_S1, STATEMENT_S2)),
                ("tax-year", (YEAR,)),
            )),
        }
        rule = _rule(requires=[BOX1], when=_gt(BOX1))
        _ctx, run, result = _dispatch(
            findings,
            rule,
            subject_type=BOX1,
            collect=[BOX1],
            lattice=lattice,
        )
        expected = [pin for pin in run.pins_for(rule, AccessLog()) if pin["role"] == "citation"]
        self.assertEqual(
            [(pin["id"], pin["version"]) for pin in expected],
            [(CITATION_A, "v1"), (CITATION_B, "v2")],
        )
        symbols = {finding["symbol"] for finding in result.publications}
        self.assertEqual(symbols, {_symbol(s1), _symbol(s2)})
        for finding in result.publications:
            got = [pin for pin in finding["pins"] if pin["role"] == "citation"]
            self.assertEqual(got, expected)


class UnrelatedCollectedType(unittest.TestCase):
    """A period-keyed circumstance shares no key name with a statement."""

    def test_adverse_circumstance_is_not_read_or_pinned_by_either_statement(self) -> None:
        s1 = _box_fact_id(STATEMENT_S1)
        s2 = _box_fact_id(STATEMENT_S2)
        circumstance_fact = _circumstance_fact_id(PERIOD_SPRING)
        statements = {
            BOX_S1_FINDING: _finding(BOX_S1_FINDING, s1, 1500),
            BOX_S2_FINDING: _finding(BOX_S2_FINDING, s2, 2500),
        }
        circumstance = _finding(CIRCUMSTANCE_FINDING, circumstance_fact, "adverse")
        lattice = {
            BOX1: _literal_type(BOX1, (
                ("lender", (LENDER,)),
                ("statement", (STATEMENT_S1, STATEMENT_S2)),
                ("tax-year", (YEAR,)),
            )),
            CIRCUMSTANCE: _literal_type(CIRCUMSTANCE, (
                ("student", (STUDENT,)),
                ("period", (PERIOD_SPRING,)),
            )),
        }
        rule = _rule(
            requires=[BOX1, CIRCUMSTANCE],
            when=_all(_gt(BOX1), _eq(CIRCUMSTANCE, CIRCUMSTANCE, "not-adverse")),
        )
        fact_types = [
            _run_fact(CIRCUMSTANCE, ["adverse", "not-adverse"], default=True),
        ]
        bindings = [{
            "symbol": CIRCUMSTANCE,
            "fact_type": {"id": CIRCUMSTANCE, "version": "v1"},
            "mode": "optional_default",
        }]
        parameters = {PARAM_ID: {"id": PARAM_ID, "version": "v1", "values": "not-adverse"}}
        with_ctx, with_run, with_result = _dispatch(
            {**statements, CIRCUMSTANCE_FINDING: circumstance},
            rule,
            subject_type=BOX1,
            collect=[BOX1, CIRCUMSTANCE],
            lattice=lattice,
            fact_types=fact_types,
            bindings=bindings,
            parameters=parameters,
        )
        _without_ctx, without_run, without_result = _dispatch(
            dict(statements),
            rule,
            subject_type=BOX1,
            collect=[BOX1],
            lattice=lattice,
            fact_types=fact_types,
            bindings=bindings,
            parameters=parameters,
        )

        box_keys = {
            name
            for source in with_ctx.sources if source.name == BOX1
            for name, _value in (source.keys or ())
        }
        circumstance_keys = {
            name
            for source in with_ctx.sources if source.name == CIRCUMSTANCE
            for name, _value in (source.keys or ())
        }
        self.assertEqual(box_keys, {"lender", "statement", "tax-year"})
        self.assertEqual(circumstance_keys, {"student", "period"})
        self.assertEqual(box_keys & circumstance_keys, set())
        self.assertEqual(
            [source.value for source in with_ctx.sources if source.name == CIRCUMSTANCE],
            ["adverse"],
        )

        def outcome(run: _Run, result: Any, fact_id: str) -> str:
            symbol = _symbol(fact_id)
            findings = [item for item in result.publications if item["symbol"] == symbol]
            rows = [row for row in run.dispositions if row.get("symbol") == symbol]
            return json.dumps(
                {"findings": findings, "dispositions": rows},
                sort_keys=True,
            )

        for fact_id in (s1, s2):
            rendered = outcome(with_run, with_result, fact_id)
            self.assertEqual(rendered, outcome(without_run, without_result, fact_id))
            payload = json.loads(rendered)
            self.assertEqual(len(payload["findings"]), 1)
            self.assertEqual([row["disposition"] for row in payload["dispositions"]], ["published"])
            pin_ids = {
                pin["id"]
                for row in payload["findings"] + payload["dispositions"]
                for pin in row["pins"]
            }
            self.assertNotIn(CIRCUMSTANCE_FINDING, pin_ids)


class Isolation(unittest.TestCase):
    def test_one_subjects_absent_dependency_does_not_change_the_other_publication(self) -> None:
        published_fact = _box_fact_id(STATEMENT_PUBLISHED)
        blocked_fact = _box_fact_id(STATEMENT_BLOCKED)
        witness_fact = _witness_fact_id(STATEMENT_PUBLISHED)
        self.assertLess(BOX_BLOCKED_FINDING, BOX_PUBLISHED_FINDING)
        self.assertLess(blocked_fact, published_fact)
        rule = _rule(
            requires=[BOX1, WITNESS],
            when=_all(_gt(BOX1), _gt(WITNESS)),
        )
        lattice = {
            BOX1: _literal_type(BOX1, (
                ("lender", (LENDER,)),
                ("statement", (STATEMENT_BLOCKED, STATEMENT_PUBLISHED)),
                ("tax-year", (YEAR,)),
            )),
            WITNESS: _literal_type(WITNESS, (
                ("lender", (LENDER,)),
                ("statement", (STATEMENT_BLOCKED, STATEMENT_PUBLISHED)),
                ("tax-year", (YEAR,)),
            )),
        }
        published_finding = _finding(BOX_PUBLISHED_FINDING, published_fact, 1500)
        witness_finding = _finding(WITNESS_FINDING, witness_fact, 1)
        _paired_ctx, paired_run, _paired_result = _dispatch(
            {
                BOX_BLOCKED_FINDING: _finding(BOX_BLOCKED_FINDING, blocked_fact, 2500),
                BOX_PUBLISHED_FINDING: published_finding,
                WITNESS_FINDING: witness_finding,
            },
            rule,
            subject_type=BOX1,
            collect=[BOX1, WITNESS],
            lattice=lattice,
        )
        _alone_ctx, alone_run, _alone_result = _dispatch(
            {
                BOX_PUBLISHED_FINDING: published_finding,
                WITNESS_FINDING: witness_finding,
            },
            rule,
            subject_type=BOX1,
            collect=[BOX1, WITNESS],
            lattice=lattice,
        )
        published_symbol = _symbol(published_fact)
        blocked_symbol = _symbol(blocked_fact)
        paired_finding = _publication(paired_run, published_symbol)
        alone_finding = _publication(alone_run, published_symbol)
        self.assertEqual(paired_finding["id"], alone_finding["id"])
        self.assertEqual(paired_finding["pins"], alone_finding["pins"])
        self.assertEqual(_origins(paired_finding["pins"]), {
            BOX_PUBLISHED_FINDING: "assertion",
            WITNESS_FINDING: "assertion",
        })
        self.assertNotIn(BOX_BLOCKED_FINDING, _ids(paired_finding["pins"], "input"))
        blocked = _row(paired_run, "blocked", blocked_symbol)
        self.assertEqual(blocked["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(blocked["missing"], [WITNESS])
        self.assertEqual(_origins(blocked["pins"]), {BOX_BLOCKED_FINDING: "assertion"})
        self.assertNotIn(BOX_PUBLISHED_FINDING, _ids(blocked["pins"], "input"))
        self.assertNotIn(WITNESS_FINDING, _ids(blocked["pins"], "input"))
        self.assertEqual(
            {pub.finding["symbol"] for pub in alone_run.publications},
            {published_symbol},
        )
        self.assertEqual(
            [row["disposition"] for row in alone_run.dispositions],
            ["published"],
        )


class DurableRecord(unittest.TestCase):
    def test_dispositions_validate_against_derivation_record_v9_and_name_the_subject(self) -> None:
        autumn = _financing_fact_id(PERIOD_AUTUMN)
        spring = _financing_fact_id(PERIOD_SPRING)
        summer = _financing_fact_id(PERIOD_SUMMER)
        periods = (PERIOD_AUTUMN, PERIOD_SPRING, PERIOD_SUMMER)
        findings = {
            AUTUMN_FINDING: _finding(AUTUMN_FINDING, autumn, "tuition"),
            SPRING_FINDING: _finding(SPRING_FINDING, spring, "tuition"),
            SUMMER_FINDING: _finding(SUMMER_FINDING, summer, "tuition"),
            CIRCUMSTANCE_FINDING: _finding(
                CIRCUMSTANCE_FINDING, _circumstance_fact_id(PERIOD_SPRING), "adverse"
            ),
            SUPPORT_AUTUMN_FINDING: _finding(
                SUPPORT_AUTUMN_FINDING, _support_fact_id(PERIOD_AUTUMN), "present"
            ),
            SUPPORT_SPRING_FINDING: _finding(
                SUPPORT_SPRING_FINDING, _support_fact_id(PERIOD_SPRING), "present"
            ),
        }
        lattice = {
            FINANCING: _literal_type(FINANCING, (
                ("borrowing", (BORROWING,)),
                ("period", periods),
                ("institution", (INSTITUTION,)),
                ("programme", (PROGRAMME,)),
            )),
            CIRCUMSTANCE: _literal_type(CIRCUMSTANCE, (
                ("student", (STUDENT,)),
                ("period", periods),
            )),
            SUPPORT: _literal_type(SUPPORT, (("period", periods),)),
        }
        rule = _rule(
            requires=[FINANCING, CIRCUMSTANCE, SUPPORT],
            when=_all(
                _eq(FINANCING, FINANCING, "tuition"),
                _eq(CIRCUMSTANCE, CIRCUMSTANCE, "not-adverse"),
                _eq(SUPPORT, SUPPORT, "present"),
            ),
        )
        ctx, run, _result = _dispatch(
            findings,
            rule,
            subject_type=FINANCING,
            collect=[FINANCING, CIRCUMSTANCE, SUPPORT],
            lattice=lattice,
            fact_types=[
                _run_fact(FINANCING, ["tuition"]),
                _run_fact(CIRCUMSTANCE, ["adverse", "not-adverse"], default=True),
                _run_fact(SUPPORT, ["present"]),
            ],
            bindings=[{
                "symbol": CIRCUMSTANCE,
                "fact_type": {"id": CIRCUMSTANCE, "version": "v1"},
                "mode": "optional_default",
            }],
            parameters={
                PARAM_ID: {"id": PARAM_ID, "version": "v1", "values": "not-adverse"},
            },
        )
        default_id = _default_finding_id(ctx)
        published = _publication(run, _symbol(autumn))
        published_row = _row(run, "published", _symbol(autumn))
        inapplicable = _row(run, "inapplicable", _symbol(spring))
        blocked = _row(run, "blocked", _symbol(summer))

        self.assertEqual(published_row["finding_id"], published["id"])
        self.assertEqual(published_row["symbol"], _symbol(autumn))
        self.assertIn(autumn, published_row["symbol"])
        self.assertEqual(_origins(published["pins"]), {
            AUTUMN_FINDING: "assertion",
            default_id: "declared_default",
            SUPPORT_AUTUMN_FINDING: "assertion",
        })

        self.assertIs(inapplicable["guard_result"], False)
        self.assertNotIn("finding_id", inapplicable)
        self.assertEqual(inapplicable["symbol"], _symbol(spring))
        self.assertIn(spring, inapplicable["symbol"])
        self.assertEqual(_origins(inapplicable["pins"]), {
            SPRING_FINDING: "assertion",
            CIRCUMSTANCE_FINDING: "assertion",
        })

        self.assertEqual(blocked["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(blocked["missing"], [SUPPORT])
        self.assertEqual(blocked["symbol"], _symbol(summer))
        self.assertIn(summer, blocked["symbol"])
        self.assertEqual(_origins(blocked["pins"]), {
            SUMMER_FINDING: "assertion",
            default_id: "declared_default",
        })
        self.assertEqual(
            {(row["disposition"], row["symbol"]) for row in run.dispositions},
            {
                ("published", _symbol(autumn)),
                ("inapplicable", _symbol(spring)),
                ("blocked", _symbol(summer)),
            },
        )

        record = closing_record(
            record_id="demo.record.subject-dispatch",
            run_id=ctx.run_id,
            phase="completed",
            workspace_revision=1,
            governance_pins=list(ctx.governance_pins),
            adoption_pin=dict(ctx.adoption_pin),
            stop_reason="saturated",
            published=[],
            blocked=[],
            dispositions=run.dispositions,
            use_v2=True,
        )
        SCHEMAS.validate("derivation-record.v9", record)


if __name__ == "__main__":
    unittest.main()
