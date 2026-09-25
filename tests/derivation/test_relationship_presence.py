"""Track 5b: ADR 0076 Part 2, the runtime half -- presence inside per-subject
dispatch, for a rule that declares ``joined`` and ``direction``.

Every behaviour test here builds a ``rule-artifact.v11`` rule declaring
``subject``, ``joined``, and ``direction`` and runs it through the real
schedulers (``packages.derivation.runner.run`` and
``packages.derivation.reference_runner.run_reference``); Part 1's scheduling
(``subject`` alone) is ``test_per_subject_scheduling.py``, whose v11 rule
builders this file reuses and extends with ``joined``/``direction``.
``tests/test_sli_g2_binding_probe.py`` is read for fixture shapes and is not
touched. Its ``..._dropped_today`` tests remain evidence of today's
*undeclared* (v10) behaviour; the two matching tests here that hand-dispatch
a v10 rule on the same fixtures exist only to prove that old path is
untouched by this unit -- they are not "the new declarations."
"""

from __future__ import annotations

import unittest
from typing import Any

from packages.derivation.evaluator import LINK_COVERAGE_KEYS_UNAVAILABLE
from packages.derivation.loader import DerivationSchemas
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import RunContext, SourceFact, _Run, run
from tests.derivation.test_link_coverage_contract import (
    BOX1,
    LINKS,
    PARAM_ID,
    REDUCTIONS,
    _coverage as _coverage_v10,
    _parameter,
)
from tests.derivation.test_per_subject_scheduling import (
    _coverage_rule_v11,
    _status_rule_v11,
)
from tests.test_sli_g2_binding_probe import (
    AMOUNT,
    BORROW_X,
    BORROW_Y,
    BORROW_Z,
    BOX_S1,
    BOX_S1_FINDING,
    BOX_S2,
    BOX_S2_FINDING,
    ENROLMENT,
    FINANCING,
    INST_A,
    INST_B,
    LENDER_A,
    LENDER_B,
    LINK_X_FINDING,
    LINK_Y_FINDING,
    PERIOD_A,
    PROG_A,
    PROG_B,
    RED_X_FINDING,
    RED_Y_FINDING,
    STATEMENT_1,
    STATEMENT_2,
    STATEMENT_IDENTITY,
    STATUS,
    YEAR,
    _box,
    _enrolment,
    _financing,
    _full_enrolment_keys,
    _keyed,
    _statement_keys,
)

ADOPTION = {"role": "adoption", "id": "demo.package.relationship-presence", "version": "v1"}
GOVERNANCE = [{"role": "governance", "id": "demo.governance.relationship-presence", "version": "v1"}]


def _fact_type(fact_id: str, key_names: list[str]) -> dict[str, Any]:
    """A ``fact-type.v2`` citizen whose identity is exactly ``key_names``.

    Only the names matter to the presence check under test; each key is
    declared ``literal`` with a placeholder domain, the same shape
    ``tests.derivation.test_subject_relationship_declarations._fact_type``
    (Track 5a) uses for the static containment check this runtime check
    complements.
    """
    return {
        "schema": "fact-type.v2",
        "id": fact_id,
        "version": "v1",
        "title": fact_id,
        "nature": "determinable",
        "identity_keys": [
            {"name": name, "kind": "literal", "values": ["placeholder"]} for name in key_names
        ],
        "value_schema": {"type": "object"},
        "supersession": {"policy": "free"},
    }


def _ctx(
    rules: list[dict[str, Any]],
    sources: list[SourceFact],
    fact_types: list[dict[str, Any]],
) -> RunContext:
    return RunContext(
        run_id="demo.run.relationship-presence",
        rules=rules,
        parameters={PARAM_ID: _parameter()},
        canon={},
        inputs=[],
        sources=sources,
        adoption_pin=ADOPTION,
        governance_pins=GOVERNANCE,
        fact_types=fact_types,
    )


def _both_runners(
    rules: list[dict[str, Any]],
    sources: list[SourceFact],
    fact_types: list[dict[str, Any]],
) -> tuple[Any, Any]:
    ctx = _ctx(rules, sources, fact_types)
    schemas = DerivationSchemas()
    return run(ctx, schemas), run_reference(ctx, schemas)


def _coverage_rule_with_relationship() -> dict[str, Any]:
    """Part 1's declared-subject coverage rule, plus Part 2's declared
    ``joined``/``direction`` -- ``joined`` is the ``links`` fact type,
    direction ``joined_contains_subject`` (ADR 0076 Part 2's admission
    requirement for a ``link_coverage`` rule)."""
    rule = _coverage_rule_v11()
    rule["joined"] = {"id": LINKS, "version": "v1"}
    rule["direction"] = "joined_contains_subject"
    return rule


def _status_rule_with_relationship() -> dict[str, Any]:
    """Part 1's declared-subject status rule, plus Part 2's
    ``subject_contains_joined`` over the enrolment type."""
    rule = _status_rule_v11()
    rule["joined"] = {"id": ENROLMENT, "version": "v1"}
    rule["direction"] = "subject_contains_joined"
    return rule


def _publications(result: Any) -> dict[str, dict[str, Any]]:
    return {p.finding["symbol"]: p.finding for p in result.publications}


def _blocked_rows(result: Any, symbol: str) -> list[dict[str, Any]]:
    return [row for row in result.dispositions if row.get("symbol") == symbol]


class FullStatementIdentityJoinsOnlyItsStatement(unittest.TestCase):
    """``joined_contains_subject``: full statement identity plus borrowing
    joins each link only to its own statement."""

    def test_full_statement_identity_joins_only_its_statement(self) -> None:
        first = _box(BOX_S1, BOX_S1_FINDING, LENDER_A, STATEMENT_1, "1000")
        second = _box(BOX_S2, BOX_S2_FINDING, LENDER_B, STATEMENT_2, "400")
        link_x = _keyed(
            LINKS, LINK_X_FINDING,
            _statement_keys(LENDER_A, STATEMENT_1) + (("borrowing", BORROW_X),),
            "1", fact_id="demo.fact.link.x",
        )
        link_y = _keyed(
            LINKS, LINK_Y_FINDING,
            _statement_keys(LENDER_B, STATEMENT_2) + (("borrowing", BORROW_Y),),
            "1", fact_id="demo.fact.link.y",
        )
        red_x = _keyed(
            REDUCTIONS, RED_X_FINDING,
            _statement_keys(LENDER_A, STATEMENT_1) + (("borrowing", BORROW_X),),
            "100", fact_id="demo.fact.reduction.x",
        )
        red_y = _keyed(
            REDUCTIONS, RED_Y_FINDING,
            _statement_keys(LENDER_B, STATEMENT_2) + (("borrowing", BORROW_Y),),
            "40", fact_id="demo.fact.reduction.y",
        )
        rule = _coverage_rule_with_relationship()
        fact_types = [_fact_type(BOX1, sorted(STATEMENT_IDENTITY))]
        forward, backward = _both_runners(
            [rule], [first, second, link_x, link_y, red_x, red_y], fact_types
        )
        for result in (forward, backward):
            published = _publications(result)
            self.assertEqual(published[f"{AMOUNT}|{BOX_S1}"]["value"], "900")
            self.assertEqual(published[f"{AMOUNT}|{BOX_S2}"]["value"], "360")


class MalformedLinksBlockEverySubject(unittest.TestCase):
    """A malformed present link -- lacking a required identity name --
    blocks every subject evaluating the rule, naming the row. Not dropped,
    never the no-link parameter. The same fixtures, with the undeclared v10
    rule, still drop the row today (proved separately below)."""

    def _base(self) -> list[SourceFact]:
        s1 = _box(BOX_S1, BOX_S1_FINDING, LENDER_A, STATEMENT_1, "1000")
        s2 = _box(BOX_S2, BOX_S2_FINDING, LENDER_B, STATEMENT_2, "400")
        keys = _statement_keys(LENDER_A, STATEMENT_1) + (("borrowing", BORROW_X),)
        link_x = _keyed(LINKS, LINK_X_FINDING, keys, "1", fact_id="demo.fact.link.x")
        red_x = _keyed(REDUCTIONS, RED_X_FINDING, keys, "100", fact_id="demo.fact.reduction.x")
        return [s1, s2, link_x, red_x]

    def _fact_types(self) -> list[dict[str, Any]]:
        return [_fact_type(BOX1, sorted(STATEMENT_IDENTITY))]

    def _assert_blocked_for_both(self, forward: Any, backward: Any) -> None:
        for result in (forward, backward):
            for symbol in (f"{AMOUNT}|{BOX_S1}", f"{AMOUNT}|{BOX_S2}"):
                rows = _blocked_rows(result, symbol)
                self.assertEqual(len(rows), 1, result.dispositions)
                self.assertEqual(rows[0]["disposition"], "blocked")
                self.assertEqual(rows[0]["code"], "DEPENDENCY_INVALID")
                self.assertEqual(rows[0]["missing"], [LINK_Y_FINDING])
                self.assertNotIn(PARAM_ID, {pin["id"] for pin in rows[0]["pins"]})

    def test_link_missing_statement_blocks_every_subject(self) -> None:
        malformed_keys = (("lender", LENDER_B), ("tax-year", "2025"), ("borrowing", BORROW_Y))
        malformed = _keyed(LINKS, LINK_Y_FINDING, malformed_keys, "1", fact_id="demo.fact.link.y")
        forward, backward = _both_runners(
            [_coverage_rule_with_relationship()], self._base() + [malformed], self._fact_types()
        )
        self._assert_blocked_for_both(forward, backward)

    def test_link_keyed_on_borrowing_only_blocks_every_subject(self) -> None:
        unjoinable = _keyed(LINKS, LINK_Y_FINDING, (("borrowing", BORROW_Y),), "1", fact_id="demo.fact.link.y")
        forward, backward = _both_runners(
            [_coverage_rule_with_relationship()], self._base() + [unjoinable], self._fact_types()
        )
        self._assert_blocked_for_both(forward, backward)

    def test_v10_rule_still_drops_the_same_malformed_rows(self) -> None:
        """The undeclared v10 rule is untouched: hand-dispatch, the same
        shape ``tests.test_sli_g2_binding_probe.SubjectLocalNoLink`` uses,
        since no production path schedules a v10 rule per subject."""
        malformed_keys = (("lender", LENDER_B), ("tax-year", "2025"), ("borrowing", BORROW_Y))
        malformed = _keyed(LINKS, LINK_Y_FINDING, malformed_keys, "1", fact_id="demo.fact.link.y")
        unjoinable = _keyed(LINKS, "demo.finding.link.z", (("borrowing", "demo-borrowing-z"),), "1", fact_id="demo.fact.link.z")
        ctx = _ctx([_coverage_v10()], self._base() + [malformed, unjoinable], [])
        prepared = _Run(ctx, DerivationSchemas())
        prepared.live_sources = list(ctx.sources)
        result = prepared.evaluate_subject_scoped_rule(subject_type=BOX1, rule=_coverage_v10())
        published = {f["symbol"].split("|", 1)[1]: f for f in result.publications}
        self.assertEqual(result.blocked, ())
        self.assertEqual(published[BOX_S1]["value"], "900")
        self.assertEqual(published[BOX_S2]["value"], "400")
        s2_inputs = {p["id"] for p in published[BOX_S2]["pins"] if p["role"] == "input"}
        self.assertEqual(s2_inputs, {BOX_S2_FINDING})
        self.assertIn(PARAM_ID, {p["id"] for p in published[BOX_S2]["pins"] if p["role"] == "parameter"})


class AnotherSubjectsCompleteLinkDoesNotBlockThisSubjectsNoLink(unittest.TestCase):
    """The two-statement case: S1 has its own complete link; S2 has none.
    S1's link disagrees with S2's identity and is ignored for S2 -- it does
    not block S2 and does not prevent S2's no-link result."""

    def test_other_statements_complete_link_does_not_block_this_statements_no_link(self) -> None:
        s1 = _box(BOX_S1, BOX_S1_FINDING, LENDER_A, STATEMENT_1, "1000")
        s2 = _box(BOX_S2, BOX_S2_FINDING, LENDER_B, STATEMENT_2, "400")
        keys = _statement_keys(LENDER_A, STATEMENT_1) + (("borrowing", BORROW_X),)
        link_x = _keyed(LINKS, LINK_X_FINDING, keys, "1", fact_id="demo.fact.link.x")
        red_x = _keyed(REDUCTIONS, RED_X_FINDING, keys, "100", fact_id="demo.fact.reduction.x")
        forward, backward = _both_runners(
            [_coverage_rule_with_relationship()],
            [s1, s2, link_x, red_x],
            [_fact_type(BOX1, sorted(STATEMENT_IDENTITY))],
        )
        for result in (forward, backward):
            published = _publications(result)
            self.assertEqual(result.blocked, [])
            self.assertEqual(published[f"{AMOUNT}|{BOX_S1}"]["value"], "900")
            self.assertEqual(published[f"{AMOUNT}|{BOX_S2}"]["value"], "400")
            s2_inputs = {p["id"] for p in published[f"{AMOUNT}|{BOX_S2}"]["pins"] if p["role"] == "input"}
            self.assertEqual(s2_inputs, {BOX_S2_FINDING})
            self.assertIn(
                PARAM_ID,
                {p["id"] for p in published[f"{AMOUNT}|{BOX_S2}"]["pins"] if p["role"] == "parameter"},
            )


class IdenticalKeyValuesStillJoinBothFacts(unittest.TestCase):
    """Residual 2: two statement facts, identical identity values, are not
    distinguishable by identity. One fully-keyed link joins both. Presence
    accepts it -- this is a named residual, not a defect this part closes."""

    def test_identical_statement_keys_join_both_facts(self) -> None:
        first = _box(BOX_S1, BOX_S1_FINDING, LENDER_A, STATEMENT_1, "1000")
        clone = _box("demo.fact.box1.s1-clone", "demo.finding.box1.s1-clone", LENDER_A, STATEMENT_1, "400")
        keys = _statement_keys(LENDER_A, STATEMENT_1) + (("borrowing", BORROW_X),)
        link = _keyed(LINKS, LINK_X_FINDING, keys, "1", fact_id="demo.fact.link.x")
        red = _keyed(REDUCTIONS, RED_X_FINDING, keys, "100", fact_id="demo.fact.reduction.x")
        forward, backward = _both_runners(
            [_coverage_rule_with_relationship()],
            [first, clone, link, red],
            [_fact_type(BOX1, sorted(STATEMENT_IDENTITY))],
        )
        for result in (forward, backward):
            published = _publications(result)
            self.assertEqual(published[f"{AMOUNT}|{BOX_S1}"]["value"], "900")
            self.assertEqual(published[f"{AMOUNT}|demo.fact.box1.s1-clone"]["value"], "300")


class SubjectContainsJoinedAppliesTheSameClassification(unittest.TestCase):
    """``subject_contains_joined``: a status rule over financing subjects,
    joined to enrolment rows, applies the same three-way classification."""

    def _subjects(self) -> tuple[SourceFact, SourceFact, SourceFact]:
        return (
            _financing("demo.fact.financing.x", "demo.finding.financing.x", BORROW_X, PERIOD_A, INST_A, PROG_A, "tuition"),
            _financing("demo.fact.financing.y", "demo.finding.financing.y", BORROW_Y, PERIOD_A, INST_A, PROG_A, "tuition"),
            _financing("demo.fact.financing.z", "demo.finding.financing.z", BORROW_Z, PERIOD_A, INST_B, PROG_B, "tuition"),
        )

    def _fact_types(self) -> list[dict[str, Any]]:
        return [_fact_type(ENROLMENT, ["period", "institution", "programme"])]

    def test_full_enrolment_reaches_both_borrowings_of_one_situation(self) -> None:
        first, second, third = self._subjects()
        enrol_a = _enrolment(
            "demo.fact.enrolment.a", "demo.finding.enrolment.a",
            _full_enrolment_keys(PERIOD_A, INST_A, PROG_A), "not-adverse",
        )
        enrol_b = _enrolment(
            "demo.fact.enrolment.b", "demo.finding.enrolment.b",
            _full_enrolment_keys(PERIOD_A, INST_B, PROG_B), "adverse",
        )
        forward, backward = _both_runners(
            [_status_rule_with_relationship()],
            [first, second, third, enrol_a, enrol_b],
            self._fact_types(),
        )
        for result in (forward, backward):
            published = _publications(result)
            self.assertEqual(result.blocked, [])
            self.assertEqual(published[f"{STATUS}|demo.fact.financing.x"]["value"], "not-adverse")
            self.assertEqual(published[f"{STATUS}|demo.fact.financing.y"]["value"], "not-adverse")
            self.assertEqual(published[f"{STATUS}|demo.fact.financing.z"]["value"], "adverse")

    def test_malformed_enrolment_row_blocks_every_subject(self) -> None:
        first, second, third = self._subjects()
        malformed = _enrolment(
            "demo.fact.enrolment.malformed", "demo.finding.enrolment.malformed",
            (("period", PERIOD_A), ("institution", INST_A)),  # missing "programme"
            "adverse",
        )
        forward, backward = _both_runners(
            [_status_rule_with_relationship()], [first, second, third, malformed], self._fact_types()
        )
        for result in (forward, backward):
            for financing_fact_id in (
                "demo.fact.financing.x", "demo.fact.financing.y", "demo.fact.financing.z",
            ):
                rows = _blocked_rows(result, f"{STATUS}|{financing_fact_id}")
                self.assertEqual(len(rows), 1, result.dispositions)
                self.assertEqual(rows[0]["code"], "DEPENDENCY_INVALID")
                self.assertEqual(rows[0]["missing"], ["demo.finding.enrolment.malformed"])


class UnreadableReferenceIdentityFailsClosed(unittest.TestCase):
    """Defect 1 (foreman review): an undeclared reference fact type must not
    make presence join everything. When the reference type's identity names
    cannot be read (absent from ``run.ctx.fact_types``, or declared with no
    names), every subject evaluating the rule blocks -- fail closed, never
    an empty (vacuously-true) requirement."""

    def test_missing_fact_type_blocks_every_subject_naming_the_type_id(self) -> None:
        first = _box(BOX_S1, BOX_S1_FINDING, LENDER_A, STATEMENT_1, "1000")
        second = _box(BOX_S2, BOX_S2_FINDING, LENDER_B, STATEMENT_2, "400")
        keys = _statement_keys(LENDER_A, STATEMENT_1) + (("borrowing", BORROW_X),)
        link_x = _keyed(LINKS, LINK_X_FINDING, keys, "1", fact_id="demo.fact.link.x")
        red_x = _keyed(REDUCTIONS, RED_X_FINDING, keys, "100", fact_id="demo.fact.reduction.x")
        # fact_types=[] -- BOX1 (the subject type, the reference type under
        # joined_contains_subject) is not declared anywhere in this package.
        forward, backward = _both_runners(
            [_coverage_rule_with_relationship()], [first, second, link_x, red_x], []
        )
        for result in (forward, backward):
            for symbol, box_finding in (
                (f"{AMOUNT}|{BOX_S1}", BOX_S1_FINDING),
                (f"{AMOUNT}|{BOX_S2}", BOX_S2_FINDING),
            ):
                rows = _blocked_rows(result, symbol)
                self.assertEqual(len(rows), 1, result.dispositions)
                self.assertEqual(rows[0]["disposition"], "blocked")
                self.assertEqual(rows[0]["code"], "DEPENDENCY_INVALID")
                # A fact-type id, not a finding id -- reader-contract section
                # 4 class 3 ("a fact-type id in the resolved graph, and it
                # is not a finding id in state").
                self.assertEqual(rows[0]["missing"], [BOX1])
                self.assertNotIn(LINK_X_FINDING, rows[0]["missing"])
                self.assertNotIn(box_finding, rows[0]["missing"])
            self.assertEqual(result.publications, [])


class SubjectMissingOwnRequiredNameFailsClosed(unittest.TestCase):
    """Defect 2 (foreman review): the no-link parameter is returned for a
    subject only "when its own keys are present" (ADR 0076 Part 2). A
    subject whose own keys omit one of the required identity names must not
    silently look like a subject with zero joined rows and take the
    default -- it blocks, and only it."""

    def test_joined_contains_subject_variant(self) -> None:
        first = _box(BOX_S1, BOX_S1_FINDING, LENDER_A, STATEMENT_1, "1000")
        # S2 carries only statement + tax-year -- no lender, one of the
        # subject's own declared identity names.
        second = _keyed(
            BOX1, BOX_S2_FINDING, (("statement", STATEMENT_2), ("tax-year", YEAR)),
            "400", fact_id=BOX_S2,
        )
        keys = _statement_keys(LENDER_A, STATEMENT_1) + (("borrowing", BORROW_X),)
        link_x = _keyed(LINKS, LINK_X_FINDING, keys, "1", fact_id="demo.fact.link.x")
        red_x = _keyed(REDUCTIONS, RED_X_FINDING, keys, "100", fact_id="demo.fact.reduction.x")
        forward, backward = _both_runners(
            [_coverage_rule_with_relationship()],
            [first, second, link_x, red_x],
            [_fact_type(BOX1, sorted(STATEMENT_IDENTITY))],
        )
        for result in (forward, backward):
            published = _publications(result)
            self.assertEqual(published[f"{AMOUNT}|{BOX_S1}"]["value"], "900")
            self.assertNotIn(f"{AMOUNT}|{BOX_S2}", published)
            rows = _blocked_rows(result, f"{AMOUNT}|{BOX_S2}")
            self.assertEqual(len(rows), 1, result.dispositions)
            self.assertEqual(rows[0]["code"], "DEPENDENCY_INVALID")
            self.assertEqual(rows[0]["missing"], [LINK_COVERAGE_KEYS_UNAVAILABLE])
            self.assertNotIn(PARAM_ID, {pin["id"] for pin in rows[0]["pins"]})

    def test_subject_contains_joined_variant(self) -> None:
        # A financing subject missing "programme" from its own keys -- the
        # joined enrolment type's own declared identity requires it.
        malformed_subject = _keyed(
            FINANCING, "demo.finding.financing.malformed",
            (("borrowing", BORROW_X), ("period", PERIOD_A), ("institution", INST_A)),
            "tuition", fact_id="demo.fact.financing.malformed",
        )
        whole = _financing(
            "demo.fact.financing.whole", "demo.finding.financing.whole",
            BORROW_Y, PERIOD_A, INST_A, PROG_A, "tuition",
        )
        enrol = _enrolment(
            "demo.fact.enrolment.a", "demo.finding.enrolment.a",
            _full_enrolment_keys(PERIOD_A, INST_A, PROG_A), "not-adverse",
        )
        forward, backward = _both_runners(
            [_status_rule_with_relationship()],
            [malformed_subject, whole, enrol],
            [_fact_type(ENROLMENT, ["period", "institution", "programme"])],
        )
        for result in (forward, backward):
            published = _publications(result)
            self.assertEqual(published[f"{STATUS}|demo.fact.financing.whole"]["value"], "not-adverse")
            rows = _blocked_rows(result, f"{STATUS}|demo.fact.financing.malformed")
            self.assertEqual(len(rows), 1, result.dispositions)
            self.assertEqual(rows[0]["code"], "DEPENDENCY_INVALID")
            self.assertEqual(rows[0]["missing"], [ENROLMENT])


if __name__ == "__main__":
    unittest.main()
