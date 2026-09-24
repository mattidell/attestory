"""Disposable G2 probe: which key shapes join, and what the schedulers do.

Synthetic ``demo.*`` identities only. No production citizen. The dispatch
under test is the existing per-subject path, called by hand.
"""

from __future__ import annotations

import unittest
from typing import Any, Mapping

from packages.derivation.evaluator import LINK_COVERAGE_SCOPE_UNBOUND
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import SourceFact, _Run, run
from packages.derivation.subject_dispatch import SubjectScopedResult, _scope
from tests.derivation.test_link_coverage_contract import (
    BOX1,
    LINKS,
    PARAM_ID,
    REDUCTIONS,
    _coverage,
)
from tests.derivation.test_link_coverage_runtime import _row, _run

STATUS = "demo.tax.schooling-status"
ENROLMENT = "demo.tax.enrolment-circumstance"
FINANCING = "demo.tax.financing-claim"
STATUS_RULE_ID = "demo.rule.schooling-status"
AMOUNT = "demo.tax.statement-facing-amount"

LENDER_A = "demo-lender-a"
LENDER_B = "demo-lender-b"
STATEMENT_1 = "demo-statement-1"
STATEMENT_2 = "demo-statement-2"
STATEMENT_3 = "demo-statement-3"
STATEMENT_SHARED = "demo-statement-shared"
YEAR = "2025"
BORROW_X = "demo-borrowing-x"
BORROW_Y = "demo-borrowing-y"
BORROW_Z = "demo-borrowing-z"
PERIOD_A = "2024-autumn"
PERIOD_B = "2025-spring"
INST_A = "demo.institution.riverside"
INST_B = "demo.institution.other"
PROG_A = "demo.programme.bsc"
PROG_B = "demo.programme.other"

STATEMENT_IDENTITY = frozenset({"lender", "statement", "tax-year"})
FINANCING_IDENTITY = frozenset({"borrowing", "period", "institution", "programme"})
ENROLMENT_IDENTITY = frozenset({"period", "institution", "programme"})

BOX_S1 = "demo.fact.box1.s1"
BOX_S2 = "demo.fact.box1.s2"
BOX_S3 = "demo.fact.box1.s3"
BOX_S1_FINDING = "demo.finding.box1.s1"
BOX_S2_FINDING = "demo.finding.box1.s2"
BOX_S3_FINDING = "demo.finding.box1.s3"
LINK_X_FINDING = "demo.finding.link.x"
LINK_Y_FINDING = "demo.finding.link.y"
RED_X_FINDING = "demo.finding.reduction.x"
RED_Y_FINDING = "demo.finding.reduction.y"


def joined_contains_subject(subject: frozenset[str], joined: frozenset[str]) -> bool:
    """Candidate (a): the joined type's names contain every subject name."""
    return subject <= joined


def subject_contains_joined(subject: frozenset[str], joined: frozenset[str]) -> bool:
    """Candidate (b): the subject's names contain every joined-type name."""
    return joined <= subject


def row_binding(
    subject: Mapping[str, str],
    row: Mapping[str, str],
    required: frozenset[str],
) -> str:
    """Runtime check the production join does not perform.

    ``missing`` — a required name is absent on the row (fail closed).
    ``disagree`` — every required name is present and some value differs.
    ``join`` — every required name is present and agrees.
    """
    if any(name not in row for name in required):
        return "missing"
    if any(row[name] != subject[name] for name in required):
        return "disagree"
    return "join"


def _statement_keys(lender: str, statement: str) -> tuple[tuple[str, str], ...]:
    return (("lender", lender), ("statement", statement), ("tax-year", YEAR))


def _box(
    fact_id: str,
    finding_id: str,
    lender: str,
    statement: str,
    value: str,
) -> SourceFact:
    return _row(BOX1, finding_id, _statement_keys(lender, statement), value, fact_id=fact_id)


def _keyed(
    name: str,
    finding_id: str,
    keys: tuple[tuple[str, str], ...],
    value: str,
    *,
    fact_id: str,
) -> SourceFact:
    return _row(name, finding_id, keys, value, fact_id=fact_id)


def _joined_ids(subject: SourceFact, rows: list[SourceFact]) -> list[str]:
    matched = _scope(subject, rows)
    if matched is None:
        raise AssertionError(f"keys unavailable for {subject.fact_id}")
    return [row.finding_id for row in matched]


def _input_ids(pins: list[dict[str, Any]]) -> set[str]:
    return {str(pin["id"]) for pin in pins if pin.get("role") == "input"}


def _parameter_ids(pins: list[dict[str, Any]]) -> set[str]:
    return {str(pin["id"]) for pin in pins if pin.get("role") == "parameter"}


def _published(result: SubjectScopedResult) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for finding in result.publications:
        fact_id = str(finding["symbol"]).split("|", 1)[1]
        out[fact_id] = finding
    return out


def _dispatch(subject_type: str, rule: dict[str, Any], sources: list[SourceFact]) -> tuple[_Run, SubjectScopedResult]:
    prepared = _run([rule, _coverage()])
    prepared.live_sources = list(sources)
    result = prepared.evaluate_subject_scoped_rule(subject_type=subject_type, rule=rule)
    return prepared, result


def _status_rule(*, when: Any = True) -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v6",
        "id": STATUS_RULE_ID,
        "version": "v1",
        "role": "applicability",
        "requires": [ENROLMENT],
        "when": when,
        "value": {"op": "ref", "name": ENROLMENT},
        "publishes": STATUS,
        "citations": [{"id": "demo.citation.schooling-status", "version": "v1"}],
    }


def _reduction_rule() -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v6",
        "id": "demo.rule.link-reduction",
        "version": "v1",
        "role": "computation",
        "requires": [STATUS],
        "when": True,
        "value": {"op": "ref", "name": STATUS},
        "publishes": REDUCTIONS,
        "citations": [{"id": "demo.citation.link-reduction", "version": "v1"}],
    }


def _financing(
    fact_id: str,
    finding_id: str,
    borrowing: str,
    period: str,
    institution: str,
    programme: str,
    value: str,
) -> SourceFact:
    return _keyed(
        FINANCING,
        finding_id,
        (
            ("borrowing", borrowing),
            ("period", period),
            ("institution", institution),
            ("programme", programme),
        ),
        value,
        fact_id=fact_id,
    )


def _enrolment(
    fact_id: str,
    finding_id: str,
    keys: tuple[tuple[str, str], ...],
    value: str,
) -> SourceFact:
    return _keyed(ENROLMENT, finding_id, keys, value, fact_id=fact_id)


def _full_enrolment_keys(period: str, institution: str, programme: str) -> tuple[tuple[str, str], ...]:
    return (("period", period), ("institution", institution), ("programme", programme))


class CoverageKeyShapes(unittest.TestCase):
    """Two statements, one tax year. Link key names vary; reductions match them.

    Box values are 1000 and 400. Reduction values are 100 and 40. A cross-join
    publishes 860 and 260. A one-link join publishes 900 and 360.
    """

    def _statements(self, statement_2: str = STATEMENT_2) -> tuple[SourceFact, SourceFact]:
        return (
            _box(BOX_S1, BOX_S1_FINDING, LENDER_A, STATEMENT_1, "1000"),
            _box(BOX_S2, BOX_S2_FINDING, LENDER_B, statement_2, "400"),
        )

    def _run_case(
        self,
        link_keys: tuple[tuple[tuple[str, str], ...], tuple[tuple[str, str], ...]],
        *,
        statement_2: str = STATEMENT_2,
    ) -> tuple[SubjectScopedResult, list[str], list[str]]:
        first, second = self._statements(statement_2)
        link_x = _keyed(LINKS, LINK_X_FINDING, link_keys[0], "1", fact_id="demo.fact.link.x")
        link_y = _keyed(LINKS, LINK_Y_FINDING, link_keys[1], "1", fact_id="demo.fact.link.y")
        red_x = _keyed(REDUCTIONS, RED_X_FINDING, link_keys[0], "100", fact_id="demo.fact.reduction.x")
        red_y = _keyed(REDUCTIONS, RED_Y_FINDING, link_keys[1], "40", fact_id="demo.fact.reduction.y")
        _prepared, result = _dispatch(
            BOX1,
            _coverage(),
            [first, second, link_x, link_y, red_x, red_y],
        )
        return result, _joined_ids(first, [link_x, link_y]), _joined_ids(second, [link_x, link_y])

    def _assert_cross_join(self, result: SubjectScopedResult) -> None:
        published = _published(result)
        self.assertEqual(result.blocked, ())
        self.assertEqual(published[BOX_S1]["value"], "860")
        self.assertEqual(published[BOX_S2]["value"], "260")
        for fact_id in (BOX_S1, BOX_S2):
            pins = list(published[fact_id]["pins"])
            self.assertEqual(
                _input_ids(pins),
                {BOX_S1_FINDING if fact_id == BOX_S1 else BOX_S2_FINDING, LINK_X_FINDING, LINK_Y_FINDING, RED_X_FINDING, RED_Y_FINDING},
            )
            self.assertEqual(_parameter_ids(pins), set())

    def _assert_own_join(self, result: SubjectScopedResult) -> None:
        published = _published(result)
        self.assertEqual(result.blocked, ())
        self.assertEqual(published[BOX_S1]["value"], "900")
        self.assertEqual(published[BOX_S2]["value"], "360")
        pins_1 = list(published[BOX_S1]["pins"])
        pins_2 = list(published[BOX_S2]["pins"])
        self.assertEqual(_input_ids(pins_1), {BOX_S1_FINDING, LINK_X_FINDING, RED_X_FINDING})
        self.assertEqual(_input_ids(pins_2), {BOX_S2_FINDING, LINK_Y_FINDING, RED_Y_FINDING})
        self.assertEqual(_parameter_ids(pins_1) | _parameter_ids(pins_2), set())

    def test_tax_year_and_borrowing_joins_both_statements(self) -> None:
        keys = (
            (("tax-year", YEAR), ("borrowing", BORROW_X)),
            (("tax-year", YEAR), ("borrowing", BORROW_Y)),
        )
        result, joined_1, joined_2 = self._run_case(keys)
        self.assertEqual(joined_1, [LINK_X_FINDING, LINK_Y_FINDING])
        self.assertEqual(joined_2, [LINK_X_FINDING, LINK_Y_FINDING])
        self._assert_cross_join(result)
        link_names = frozenset({"tax-year", "borrowing"})
        self.assertFalse(joined_contains_subject(STATEMENT_IDENTITY, link_names))
        self.assertFalse(subject_contains_joined(STATEMENT_IDENTITY, link_names))

    def test_shared_statement_id_joins_both_lenders(self) -> None:
        first = _box(BOX_S1, BOX_S1_FINDING, LENDER_A, STATEMENT_SHARED, "1000")
        second = _box(BOX_S2, BOX_S2_FINDING, LENDER_B, STATEMENT_SHARED, "400")
        keys = (
            (("statement", STATEMENT_SHARED), ("borrowing", BORROW_X)),
            (("statement", STATEMENT_SHARED), ("borrowing", BORROW_Y)),
        )
        link_x = _keyed(LINKS, LINK_X_FINDING, keys[0], "1", fact_id="demo.fact.link.x")
        link_y = _keyed(LINKS, LINK_Y_FINDING, keys[1], "1", fact_id="demo.fact.link.y")
        red_x = _keyed(REDUCTIONS, RED_X_FINDING, keys[0], "100", fact_id="demo.fact.reduction.x")
        red_y = _keyed(REDUCTIONS, RED_Y_FINDING, keys[1], "40", fact_id="demo.fact.reduction.y")
        _prepared, result = _dispatch(BOX1, _coverage(), [first, second, link_x, link_y, red_x, red_y])
        self.assertEqual(_joined_ids(first, [link_x, link_y]), [LINK_X_FINDING, LINK_Y_FINDING])
        self.assertEqual(_joined_ids(second, [link_x, link_y]), [LINK_X_FINDING, LINK_Y_FINDING])
        self._assert_cross_join(result)
        link_names = frozenset({"statement", "borrowing"})
        self.assertFalse(joined_contains_subject(STATEMENT_IDENTITY, link_names))
        self.assertFalse(subject_contains_joined(STATEMENT_IDENTITY, link_names))

    def test_full_statement_identity_joins_only_its_statement(self) -> None:
        keys = (
            _statement_keys(LENDER_A, STATEMENT_1) + (("borrowing", BORROW_X),),
            _statement_keys(LENDER_B, STATEMENT_2) + (("borrowing", BORROW_Y),),
        )
        result, joined_1, joined_2 = self._run_case(keys)
        self.assertEqual(joined_1, [LINK_X_FINDING])
        self.assertEqual(joined_2, [LINK_Y_FINDING])
        self._assert_own_join(result)
        link_names = STATEMENT_IDENTITY | {"borrowing"}
        self.assertTrue(joined_contains_subject(STATEMENT_IDENTITY, link_names))
        self.assertFalse(subject_contains_joined(STATEMENT_IDENTITY, link_names))
        present = {"lender": LENDER_A, "statement": STATEMENT_1, "tax-year": YEAR, "borrowing": BORROW_X}
        self.assertEqual(row_binding({"lender": LENDER_A, "statement": STATEMENT_1, "tax-year": YEAR}, present, STATEMENT_IDENTITY), "join")
        self.assertEqual(row_binding({"lender": LENDER_B, "statement": STATEMENT_2, "tax-year": YEAR}, present, STATEMENT_IDENTITY), "disagree")

    def test_lender_and_tax_year_splits_these_two_lenders(self) -> None:
        keys = (
            (("lender", LENDER_A), ("tax-year", YEAR), ("borrowing", BORROW_X)),
            (("lender", LENDER_B), ("tax-year", YEAR), ("borrowing", BORROW_Y)),
        )
        result, joined_1, joined_2 = self._run_case(keys)
        self.assertEqual(joined_1, [LINK_X_FINDING])
        self.assertEqual(joined_2, [LINK_Y_FINDING])
        self._assert_own_join(result)
        link_names = frozenset({"lender", "tax-year", "borrowing"})
        self.assertFalse(joined_contains_subject(STATEMENT_IDENTITY, link_names))
        self.assertFalse(subject_contains_joined(STATEMENT_IDENTITY, link_names))

    def test_lender_and_tax_year_collides_for_one_lender(self) -> None:
        first = _box(BOX_S1, BOX_S1_FINDING, LENDER_A, STATEMENT_1, "1000")
        third = _box(BOX_S3, BOX_S3_FINDING, LENDER_A, STATEMENT_3, "400")
        keys = (
            (("lender", LENDER_A), ("tax-year", YEAR), ("borrowing", BORROW_X)),
            (("lender", LENDER_A), ("tax-year", YEAR), ("borrowing", BORROW_Y)),
        )
        link_x = _keyed(LINKS, LINK_X_FINDING, keys[0], "1", fact_id="demo.fact.link.x")
        link_y = _keyed(LINKS, LINK_Y_FINDING, keys[1], "1", fact_id="demo.fact.link.y")
        red_x = _keyed(REDUCTIONS, RED_X_FINDING, keys[0], "100", fact_id="demo.fact.reduction.x")
        red_y = _keyed(REDUCTIONS, RED_Y_FINDING, keys[1], "40", fact_id="demo.fact.reduction.y")
        _prepared, result = _dispatch(BOX1, _coverage(), [first, third, link_x, link_y, red_x, red_y])
        self.assertEqual(_joined_ids(first, [link_x, link_y]), [LINK_X_FINDING, LINK_Y_FINDING])
        self.assertEqual(_joined_ids(third, [link_x, link_y]), [LINK_X_FINDING, LINK_Y_FINDING])
        published = _published(result)
        self.assertEqual(result.blocked, ())
        self.assertEqual(published[BOX_S1]["value"], "860")
        self.assertEqual(published[BOX_S3]["value"], "260")

    def test_identical_statement_keys_join_both_facts(self) -> None:
        first = _box(BOX_S1, BOX_S1_FINDING, LENDER_A, STATEMENT_1, "1000")
        clone = _box("demo.fact.box1.s1-clone", "demo.finding.box1.s1-clone", LENDER_A, STATEMENT_1, "400")
        keys = _statement_keys(LENDER_A, STATEMENT_1) + (("borrowing", BORROW_X),)
        link = _keyed(LINKS, LINK_X_FINDING, keys, "1", fact_id="demo.fact.link.x")
        red = _keyed(REDUCTIONS, RED_X_FINDING, keys, "100", fact_id="demo.fact.reduction.x")
        _prepared, result = _dispatch(BOX1, _coverage(), [first, clone, link, red])
        self.assertEqual(_joined_ids(first, [link]), [LINK_X_FINDING])
        self.assertEqual(_joined_ids(clone, [link]), [LINK_X_FINDING])
        published = _published(result)
        self.assertEqual(published[BOX_S1]["value"], "900")
        self.assertEqual(published["demo.fact.box1.s1-clone"]["value"], "300")
        self.assertTrue(joined_contains_subject(STATEMENT_IDENTITY, frozenset(dict(keys))))

    def test_narrow_link_is_dropped_when_a_wide_link_widens_shared_names(self) -> None:
        first = _box(BOX_S1, BOX_S1_FINDING, LENDER_A, STATEMENT_1, "1000")
        second = _box(BOX_S2, BOX_S2_FINDING, LENDER_B, STATEMENT_2, "400")
        wide = _statement_keys(LENDER_A, STATEMENT_1) + (("borrowing", BORROW_X),)
        narrow = (("tax-year", YEAR), ("borrowing", BORROW_Y))
        link_wide = _keyed(LINKS, LINK_X_FINDING, wide, "1", fact_id="demo.fact.link.x")
        link_narrow = _keyed(LINKS, LINK_Y_FINDING, narrow, "1", fact_id="demo.fact.link.y")
        red_wide = _keyed(REDUCTIONS, RED_X_FINDING, wide, "100", fact_id="demo.fact.reduction.x")
        red_narrow = _keyed(REDUCTIONS, RED_Y_FINDING, narrow, "40", fact_id="demo.fact.reduction.y")
        _prepared, result = _dispatch(
            BOX1, _coverage(), [first, second, link_wide, link_narrow, red_wide, red_narrow]
        )
        self.assertEqual(_joined_ids(first, [link_wide, link_narrow]), [LINK_X_FINDING])
        self.assertEqual(_joined_ids(second, [link_wide, link_narrow]), [])
        published = _published(result)
        self.assertEqual(result.blocked, ())
        self.assertEqual(published[BOX_S1]["value"], "900")
        self.assertEqual(published[BOX_S2]["value"], "400")
        self.assertEqual(_parameter_ids(list(published[BOX_S2]["pins"])), {PARAM_ID})
        self.assertNotIn(LINK_Y_FINDING, _input_ids(list(published[BOX_S1]["pins"])))
        self.assertNotIn(LINK_Y_FINDING, _input_ids(list(published[BOX_S2]["pins"])))
        narrow_row = {"tax-year": YEAR, "borrowing": BORROW_Y}
        self.assertEqual(
            row_binding({"lender": LENDER_A, "statement": STATEMENT_1, "tax-year": YEAR}, narrow_row, STATEMENT_IDENTITY),
            "missing",
        )


class StatusKeyShapes(unittest.TestCase):
    """Financing subject, enrolment joined. Two borrowings share one situation."""

    def _subjects(self) -> tuple[SourceFact, SourceFact, SourceFact]:
        return (
            _financing("demo.fact.financing.x", "demo.finding.financing.x", BORROW_X, PERIOD_A, INST_A, PROG_A, "tuition"),
            _financing("demo.fact.financing.y", "demo.finding.financing.y", BORROW_Y, PERIOD_A, INST_A, PROG_A, "tuition"),
            _financing("demo.fact.financing.z", "demo.finding.financing.z", BORROW_Z, PERIOD_A, INST_B, PROG_B, "tuition"),
        )

    def test_full_enrolment_reaches_both_borrowings_of_one_situation(self) -> None:
        first, second, third = self._subjects()
        enrol_a = _enrolment(
            "demo.fact.enrolment.a",
            "demo.finding.enrolment.a",
            _full_enrolment_keys(PERIOD_A, INST_A, PROG_A),
            "not-adverse",
        )
        enrol_b = _enrolment(
            "demo.fact.enrolment.b",
            "demo.finding.enrolment.b",
            _full_enrolment_keys(PERIOD_A, INST_B, PROG_B),
            "adverse",
        )
        _prepared, result = _dispatch(
            FINANCING, _status_rule(), [first, second, third, enrol_a, enrol_b]
        )
        self.assertEqual(_joined_ids(first, [enrol_a, enrol_b]), ["demo.finding.enrolment.a"])
        self.assertEqual(_joined_ids(second, [enrol_a, enrol_b]), ["demo.finding.enrolment.a"])
        self.assertEqual(_joined_ids(third, [enrol_a, enrol_b]), ["demo.finding.enrolment.b"])
        published = _published(result)
        self.assertEqual(result.blocked, ())
        self.assertEqual(published["demo.fact.financing.x"]["value"], "not-adverse")
        self.assertEqual(published["demo.fact.financing.y"]["value"], "not-adverse")
        self.assertEqual(published["demo.fact.financing.z"]["value"], "adverse")
        self.assertEqual(
            _input_ids(list(published["demo.fact.financing.x"]["pins"])),
            {"demo.finding.financing.x", "demo.finding.enrolment.a"},
        )
        self.assertNotIn("demo.finding.enrolment.b", _input_ids(list(published["demo.fact.financing.x"]["pins"])))
        self.assertFalse(joined_contains_subject(FINANCING_IDENTITY, ENROLMENT_IDENTITY))
        self.assertTrue(subject_contains_joined(FINANCING_IDENTITY, ENROLMENT_IDENTITY))

    def test_period_only_enrolment_reaches_every_financing_in_that_period(self) -> None:
        first, second, third = self._subjects()
        enrol = _enrolment(
            "demo.fact.enrolment.period",
            "demo.finding.enrolment.period",
            (("period", PERIOD_A),),
            "not-adverse",
        )
        _prepared, result = _dispatch(FINANCING, _status_rule(), [first, second, third, enrol])
        for subject in (first, second, third):
            self.assertEqual(_joined_ids(subject, [enrol]), ["demo.finding.enrolment.period"])
        published = _published(result)
        self.assertEqual(result.blocked, ())
        for fact_id in ("demo.fact.financing.x", "demo.fact.financing.y", "demo.fact.financing.z"):
            self.assertEqual(published[fact_id]["value"], "not-adverse")
            self.assertIn("demo.finding.enrolment.period", _input_ids(list(published[fact_id]["pins"])))
        period_names = frozenset({"period"})
        self.assertFalse(joined_contains_subject(FINANCING_IDENTITY, period_names))
        self.assertTrue(subject_contains_joined(FINANCING_IDENTITY, period_names))
        self.assertEqual(
            row_binding(
                {"borrowing": BORROW_Z, "period": PERIOD_A, "institution": INST_B, "programme": PROG_B},
                {"period": PERIOD_A},
                ENROLMENT_IDENTITY,
            ),
            "missing",
        )

    def test_period_only_row_is_dropped_when_a_full_row_widens_shared_names(self) -> None:
        first, _second, _third = self._subjects()
        full = _enrolment(
            "demo.fact.enrolment.a",
            "demo.finding.enrolment.a",
            _full_enrolment_keys(PERIOD_A, INST_A, PROG_A),
            "not-adverse",
        )
        period_only = _enrolment(
            "demo.fact.enrolment.period",
            "demo.finding.enrolment.period",
            (("period", PERIOD_A),),
            "adverse",
        )
        _prepared, result = _dispatch(FINANCING, _status_rule(), [first, full, period_only])
        self.assertEqual(_joined_ids(first, [full, period_only]), ["demo.finding.enrolment.a"])
        published = _published(result)
        self.assertEqual(result.blocked, ())
        self.assertEqual(published["demo.fact.financing.x"]["value"], "not-adverse")
        self.assertNotIn(
            "demo.finding.enrolment.period",
            _input_ids(list(published["demo.fact.financing.x"]["pins"])),
        )


class PredecessorChain(unittest.TestCase):
    """Hand-called status, then link reduction, then statement coverage."""

    def _chain_sources(self, *, enrolments: list[SourceFact], financing_value_y: str = "tuition") -> list[SourceFact]:
        box = _box(BOX_S1, BOX_S1_FINDING, LENDER_A, STATEMENT_1, "1500")
        link_x = _keyed(
            LINKS,
            LINK_X_FINDING,
            _statement_keys(LENDER_A, STATEMENT_1) + (("borrowing", BORROW_X),),
            "1",
            fact_id="demo.fact.link.x",
        )
        link_y = _keyed(
            LINKS,
            LINK_Y_FINDING,
            _statement_keys(LENDER_A, STATEMENT_1) + (("borrowing", BORROW_Y),),
            "1",
            fact_id="demo.fact.link.y",
        )
        financing_x = _financing(
            "demo.fact.financing.x", "demo.finding.financing.x", BORROW_X, PERIOD_A, INST_A, PROG_A, "100"
        )
        financing_y = _financing(
            "demo.fact.financing.y", "demo.finding.financing.y", BORROW_Y, PERIOD_B, INST_B, PROG_B, financing_value_y
        )
        return [box, link_x, link_y, financing_x, financing_y, *enrolments]

    def _run_chain(
        self,
        sources: list[SourceFact],
        *,
        status_when: Any = True,
        call_status: bool = True,
        call_reduction: bool = True,
        call_amount: bool = True,
    ) -> _Run:
        prepared = _run([_status_rule(when=status_when), _reduction_rule(), _coverage()])
        prepared.live_sources = list(sources)
        if call_status:
            prepared.evaluate_subject_scoped_rule(subject_type=FINANCING, rule=_status_rule(when=status_when))
        if call_reduction:
            prepared.evaluate_subject_scoped_rule(subject_type=LINKS, rule=_reduction_rule())
        if call_amount:
            prepared.evaluate_subject_scoped_rule(subject_type=BOX1, rule=_coverage())
        return prepared

    def _row(self, prepared: _Run, symbol: str) -> dict[str, Any]:
        rows = [row for row in prepared.dispositions if row.get("symbol") == symbol]
        self.assertEqual(len(rows), 1, prepared.dispositions)
        return rows[0]

    def test_status_blocked_for_one_financing_blocks_that_link_and_the_statement(self) -> None:
        enrol = _enrolment(
            "demo.fact.enrolment.x",
            "demo.finding.enrolment.x",
            _full_enrolment_keys(PERIOD_A, INST_A, PROG_A),
            "100",
        )
        prepared = self._run_chain(self._chain_sources(enrolments=[enrol]))
        self.assertIn(STATUS_RULE_ID, prepared.resolved)
        status_x = self._row(prepared, f"{STATUS}|demo.fact.financing.x")
        status_y = self._row(prepared, f"{STATUS}|demo.fact.financing.y")
        self.assertEqual(status_x["disposition"], "published")
        self.assertEqual(status_y["disposition"], "blocked")
        self.assertEqual(status_y["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(status_y["missing"], [ENROLMENT])
        reduction_x = self._row(prepared, f"{REDUCTIONS}|demo.fact.link.x")
        reduction_y = self._row(prepared, f"{REDUCTIONS}|demo.fact.link.y")
        self.assertEqual(reduction_x["disposition"], "published")
        self.assertEqual(reduction_y["disposition"], "blocked")
        self.assertEqual(reduction_y["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(reduction_y["missing"], [STATUS])
        amount = self._row(prepared, f"{AMOUNT}|{BOX_S1}")
        self.assertEqual(amount["disposition"], "blocked")
        self.assertEqual(amount["code"], "DEPENDENCY_INVALID")
        self.assertEqual(amount["missing"], [LINK_Y_FINDING])
        self.assertNotIn(PARAM_ID, {pin["id"] for pin in amount["pins"]})
        self.assertFalse(prepared.is_eligible(_reduction_rule()))
        self.assertNotIn(STATUS, prepared.symbols)
        self.assertIn(f"{STATUS}|demo.fact.financing.x", prepared.symbols)

    def test_status_blocked_for_every_financing_blocks_every_link(self) -> None:
        prepared = self._run_chain(self._chain_sources(enrolments=[]))
        self.assertIn(STATUS_RULE_ID, prepared.resolved)
        self.assertEqual(self._row(prepared, f"{STATUS}|demo.fact.financing.x")["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(self._row(prepared, f"{STATUS}|demo.fact.financing.y")["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(self._row(prepared, f"{REDUCTIONS}|demo.fact.link.x")["missing"], [STATUS])
        self.assertEqual(self._row(prepared, f"{REDUCTIONS}|demo.fact.link.y")["missing"], [STATUS])
        amount = self._row(prepared, f"{AMOUNT}|{BOX_S1}")
        self.assertEqual(amount["disposition"], "blocked")
        self.assertEqual(amount["missing"], sorted([LINK_X_FINDING, LINK_Y_FINDING]))
        self.assertNotIn(PARAM_ID, {pin["id"] for pin in amount["pins"]})

    def test_status_inapplicable_for_one_financing_leaves_no_source(self) -> None:
        enrol_x = _enrolment(
            "demo.fact.enrolment.x",
            "demo.finding.enrolment.x",
            _full_enrolment_keys(PERIOD_A, INST_A, PROG_A),
            "100",
        )
        enrol_y = _enrolment(
            "demo.fact.enrolment.y",
            "demo.finding.enrolment.y",
            _full_enrolment_keys(PERIOD_B, INST_B, PROG_B),
            "40",
        )
        guard: dict[str, Any] = {
            "op": "compare",
            "cmp": "gt",
            "left": {"op": "ref", "name": FINANCING},
            "right": 0,
        }
        prepared = self._run_chain(
            self._chain_sources(enrolments=[enrol_x, enrol_y], financing_value_y="0"),
            status_when=guard,
        )
        self.assertEqual(self._row(prepared, f"{STATUS}|demo.fact.financing.y")["disposition"], "inapplicable")
        borrowings = {
            dict(source.keys)["borrowing"]
            for source in prepared.live_sources
            if source.name == STATUS and source.keys is not None
        }
        self.assertEqual(borrowings, {BORROW_X})
        self.assertEqual(self._row(prepared, f"{REDUCTIONS}|demo.fact.link.y")["missing"], [STATUS])
        self.assertEqual(self._row(prepared, f"{AMOUNT}|{BOX_S1}")["missing"], [LINK_Y_FINDING])

    def test_skipping_status_makes_every_reduction_absent(self) -> None:
        enrol = _enrolment(
            "demo.fact.enrolment.x",
            "demo.finding.enrolment.x",
            _full_enrolment_keys(PERIOD_A, INST_A, PROG_A),
            "100",
        )
        prepared = self._run_chain(self._chain_sources(enrolments=[enrol]), call_status=False)
        self.assertNotIn(STATUS_RULE_ID, prepared.resolved)
        self.assertEqual(self._row(prepared, f"{REDUCTIONS}|demo.fact.link.x")["missing"], [STATUS])
        self.assertEqual(self._row(prepared, f"{REDUCTIONS}|demo.fact.link.y")["missing"], [STATUS])
        self.assertEqual(
            self._row(prepared, f"{AMOUNT}|{BOX_S1}")["missing"],
            sorted([LINK_X_FINDING, LINK_Y_FINDING]),
        )

    def test_amount_before_reduction_blocks_uncovered_and_stays_resolved(self) -> None:
        enrol = _enrolment(
            "demo.fact.enrolment.x",
            "demo.finding.enrolment.x",
            _full_enrolment_keys(PERIOD_A, INST_A, PROG_A),
            "100",
        )
        prepared = _run([_status_rule(), _reduction_rule(), _coverage()])
        prepared.live_sources = self._chain_sources(enrolments=[enrol])
        prepared.evaluate_subject_scoped_rule(subject_type=FINANCING, rule=_status_rule())
        prepared.evaluate_subject_scoped_rule(subject_type=BOX1, rule=_coverage())
        amount_rule = _coverage()
        self.assertIn(amount_rule["id"], prepared.resolved)
        self.assertEqual(
            self._row(prepared, f"{AMOUNT}|{BOX_S1}")["missing"],
            sorted([LINK_X_FINDING, LINK_Y_FINDING]),
        )
        prepared.evaluate_subject_scoped_rule(subject_type=LINKS, rule=_reduction_rule())
        self.assertEqual(
            [row for row in prepared.dispositions if row.get("symbol") == f"{AMOUNT}|{BOX_S1}"],
            [self._row(prepared, f"{AMOUNT}|{BOX_S1}")],
        )
        self.assertEqual(self._row(prepared, f"{AMOUNT}|{BOX_S1}")["disposition"], "blocked")

    def test_two_statuses_for_one_borrowing_disagree_and_block(self) -> None:
        box = _box(BOX_S1, BOX_S1_FINDING, LENDER_A, STATEMENT_1, "1500")
        link = _keyed(
            LINKS,
            LINK_X_FINDING,
            _statement_keys(LENDER_A, STATEMENT_1) + (("borrowing", BORROW_X),),
            "1",
            fact_id="demo.fact.link.x",
        )
        autumn = _financing(
            "demo.fact.financing.autumn", "demo.finding.financing.autumn", BORROW_X, PERIOD_A, INST_A, PROG_A, "tuition"
        )
        spring = _financing(
            "demo.fact.financing.spring", "demo.finding.financing.spring", BORROW_X, PERIOD_B, INST_A, PROG_A, "tuition"
        )
        enrol_a = _enrolment(
            "demo.fact.enrolment.autumn",
            "demo.finding.enrolment.autumn",
            _full_enrolment_keys(PERIOD_A, INST_A, PROG_A),
            "100",
        )
        enrol_b = _enrolment(
            "demo.fact.enrolment.spring",
            "demo.finding.enrolment.spring",
            _full_enrolment_keys(PERIOD_B, INST_A, PROG_A),
            "40",
        )
        prepared = self._run_chain([box, link, autumn, spring, enrol_a, enrol_b])
        reduction = self._row(prepared, f"{REDUCTIONS}|demo.fact.link.x")
        self.assertEqual(reduction["disposition"], "blocked")
        self.assertEqual(reduction["code"], "DEPENDENCY_INVALID")
        self.assertEqual(
            set(reduction["missing"]),
            {"demo.fact.financing.autumn", "demo.fact.financing.spring"},
        )
        self.assertEqual(self._row(prepared, f"{AMOUNT}|{BOX_S1}")["missing"], [LINK_X_FINDING])

    def test_two_statuses_for_one_borrowing_agree_and_sort_first_publishes(self) -> None:
        box = _box(BOX_S1, BOX_S1_FINDING, LENDER_A, STATEMENT_1, "1500")
        link = _keyed(
            LINKS,
            LINK_X_FINDING,
            _statement_keys(LENDER_A, STATEMENT_1) + (("borrowing", BORROW_X),),
            "1",
            fact_id="demo.fact.link.x",
        )
        autumn = _financing(
            "demo.fact.financing.autumn", "demo.finding.financing.autumn", BORROW_X, PERIOD_A, INST_A, PROG_A, "tuition"
        )
        spring = _financing(
            "demo.fact.financing.spring", "demo.finding.financing.spring", BORROW_X, PERIOD_B, INST_A, PROG_A, "tuition"
        )
        enrol_a = _enrolment(
            "demo.fact.enrolment.autumn",
            "demo.finding.enrolment.autumn",
            _full_enrolment_keys(PERIOD_A, INST_A, PROG_A),
            "100",
        )
        enrol_b = _enrolment(
            "demo.fact.enrolment.spring",
            "demo.finding.enrolment.spring",
            _full_enrolment_keys(PERIOD_B, INST_A, PROG_A),
            "100",
        )
        prepared = self._run_chain([box, link, autumn, spring, enrol_a, enrol_b])
        status_sources = [source for source in prepared.live_sources if source.name == STATUS]
        self.assertEqual(len(status_sources), 2)
        chosen = sorted(status_sources, key=lambda source: source.finding_id)[0]
        other = sorted(status_sources, key=lambda source: source.finding_id)[1]
        reduction = self._row(prepared, f"{REDUCTIONS}|demo.fact.link.x")
        self.assertEqual(reduction["disposition"], "published")
        published = [
            pub.finding
            for pub in prepared.publications
            if pub.finding["symbol"] == f"{REDUCTIONS}|demo.fact.link.x"
        ]
        self.assertEqual(len(published), 1)
        self.assertIn(chosen.finding_id, _input_ids(list(published[0]["pins"])))
        self.assertNotIn(other.finding_id, _input_ids(list(published[0]["pins"])))
        amount = self._row(prepared, f"{AMOUNT}|{BOX_S1}")
        self.assertEqual(amount["disposition"], "published")
        amount_finding = [
            pub.finding for pub in prepared.publications if pub.finding["symbol"] == f"{AMOUNT}|{BOX_S1}"
        ]
        self.assertEqual(amount_finding[0]["value"], "1400")


class Schedulers(unittest.TestCase):
    """What the two runners do today. Neither dispatches per subject."""

    def test_both_runners_record_ordinary_absence_and_agree(self) -> None:
        prepared = _run([_status_rule(), _reduction_rule(), _coverage()])
        forward = run(prepared.ctx, prepared.schemas)
        backward = run_reference(prepared.ctx, prepared.schemas)

        def outcomes(result: Any) -> set[tuple[str, str, tuple[str, ...]]]:
            return {
                (str(row["artifact_id"]), str(row["code"]), tuple(row["missing"]))
                for row in result.dispositions
                if row["disposition"] == "blocked"
            }

        expected = {
            (STATUS_RULE_ID, "DEPENDENCY_ABSENT", (ENROLMENT,)),
            ("demo.rule.link-reduction", "DEPENDENCY_ABSENT", (STATUS,)),
            (_coverage()["id"], "DEPENDENCY_ABSENT", (BOX1,)),
        }
        self.assertEqual(outcomes(forward), expected)
        self.assertEqual(outcomes(backward), expected)
        self.assertEqual(forward.publications, [])
        self.assertEqual(backward.publications, [])
        for result in (forward, backward):
            for row in result.dispositions:
                self.assertNotIn("|", str(row.get("symbol", "")))

    def test_attempt_blocks_scope_unbound_when_box1_is_a_symbol(self) -> None:
        prepared = _run([_coverage()])
        rule = _coverage()
        prepared.symbols[BOX1] = 1000
        prepared.symbol_pin[BOX1] = ("demo.finding.box1.sched", "v1", "input", "assertion")
        self.assertTrue(prepared.is_eligible(rule))
        self.assertEqual(prepared.attempt(rule), "blocked")
        row = prepared.dispositions[-1]
        self.assertEqual(row["code"], "DEPENDENCY_INVALID")
        self.assertEqual(row["missing"], [LINK_COVERAGE_SCOPE_UNBOUND])
        self.assertNotIn("symbol", row)

    def test_finalize_unreached_evaluates_coverage_once_when_requires_are_met(self) -> None:
        prepared = _run([_coverage()])
        rule = _coverage()
        prepared.symbols[BOX1] = 1000
        prepared.symbol_pin[BOX1] = ("demo.finding.box1.sched", "v1", "input", "assertion")
        prepared.finalize_unreached()
        row = prepared.dispositions[-1]
        self.assertEqual(row["missing"], [LINK_COVERAGE_SCOPE_UNBOUND])
        self.assertNotIn(f"{AMOUNT}|", " ".join(str(item.get("symbol", "")) for item in prepared.dispositions))
        self.assertIn(rule["id"], prepared.resolved)
