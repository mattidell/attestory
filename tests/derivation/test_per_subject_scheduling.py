"""Track 5b: ADR 0076 Part 1, the runtime half -- per-subject scheduling.

Every behaviour test here builds a ``rule-artifact.v11`` rule (declaring
``subject`` only -- Part 2's ``joined``/``direction`` is
``tests/derivation/test_relationship_presence.py``) and runs it through the
real schedulers, ``packages.derivation.runner.run`` and
``packages.derivation.reference_runner.run_reference``, never through
hand-called ``evaluate_subject_scoped_rule``. ``tests/test_sli_g2_binding_
probe.py``'s hand-dispatched probes are read for fixture shapes and are not
touched; its own tests, including the ``..._dropped_today`` ones, remain
evidence of today's *undeclared* (v1-v10) behaviour.
"""

from __future__ import annotations

import unittest
from typing import Any

from packages.derivation.loader import DerivationSchemas
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import RunContext, SourceFact, _Run, run
from tests.derivation.test_link_coverage_contract import (
    BOX1,
    COVERAGE_ID,
    LINKS,
    PARAM_ID,
    REDUCTIONS,
    _coverage as _coverage_v10,
    _parameter,
)
from tests.test_sli_g2_binding_probe import (
    AMOUNT,
    BORROW_X,
    BORROW_Y,
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
    PERIOD_B,
    PROG_A,
    PROG_B,
    STATEMENT_1,
    STATEMENT_2,
    STATUS,
    STATUS_RULE_ID,
    _box,
    _enrolment,
    _financing,
    _full_enrolment_keys,
    _keyed,
    _reduction_rule,
    _statement_keys,
    _status_rule,
)

ADOPTION = {"role": "adoption", "id": "demo.package.per-subject-scheduling", "version": "v1"}
GOVERNANCE = [{"role": "governance", "id": "demo.governance.per-subject-scheduling", "version": "v1"}]


def _ctx(rules: list[dict[str, Any]], sources: list[SourceFact]) -> RunContext:
    return RunContext(
        run_id="demo.run.per-subject-scheduling",
        rules=rules,
        parameters={PARAM_ID: _parameter()},
        canon={},
        inputs=[],
        sources=sources,
        adoption_pin=ADOPTION,
        governance_pins=GOVERNANCE,
    )


def _both_runners(rules: list[dict[str, Any]], sources: list[SourceFact]) -> tuple[Any, Any]:
    ctx = _ctx(rules, sources)
    schemas = DerivationSchemas()
    return run(ctx, schemas), run_reference(ctx, schemas)


def _echo_rule_v11() -> dict[str, Any]:
    """A minimal declared-subject rule: no ``link_coverage``, no ``joined``."""
    return {
        "schema": "rule-artifact.v11",
        "id": "demo.rule.echo-box1",
        "version": "v1",
        "subject": {"id": BOX1, "version": "v1"},
        "role": "computation",
        "requires": [BOX1],
        "when": True,
        "value": {"op": "ref", "name": BOX1},
        "publishes": "demo.tax.echo-box1",
    }


def _status_rule_v11(*, when: Any = True) -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v11",
        "id": STATUS_RULE_ID,
        "version": "v1",
        "subject": {"id": FINANCING, "version": "v1"},
        "role": "applicability",
        "requires": [ENROLMENT],
        "when": when,
        "value": {"op": "ref", "name": ENROLMENT},
        "publishes": STATUS,
        "citations": [{"id": "demo.citation.schooling-status", "version": "v1"}],
    }


def _reduction_rule_v11() -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v11",
        "id": "demo.rule.link-reduction",
        "version": "v1",
        "subject": {"id": LINKS, "version": "v1"},
        "role": "computation",
        "requires": [STATUS],
        "when": True,
        "value": {"op": "ref", "name": STATUS},
        "publishes": REDUCTIONS,
        "citations": [{"id": "demo.citation.link-reduction", "version": "v1"}],
    }


def _coverage_rule_v11() -> dict[str, Any]:
    """Declares ``subject`` only (Part 1). ``joined``/``direction`` are
    Part 2 and are exercised in ``test_relationship_presence.py``."""
    return {
        "schema": "rule-artifact.v11",
        "id": COVERAGE_ID,
        "version": "v2",
        "subject": {"id": BOX1, "version": "v1"},
        "role": "computation",
        "requires": [BOX1],
        "when": {
            "op": "compare",
            "cmp": "gt",
            "left": {"op": "ref", "name": BOX1},
            "right": 0,
        },
        "value": {
            "op": "subtract",
            "left": {"op": "ref", "name": BOX1},
            "right": {
                "op": "link_coverage",
                "links": LINKS,
                "reductions": REDUCTIONS,
                "empty": {"parameter": {"id": PARAM_ID, "version": "v1"}},
            },
        },
        "publishes": AMOUNT,
        "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
        "citations": [{"id": "demo.citation.statement-box-minus-reductions", "version": "v1"}],
    }


def _chain_sources(*, enrolments: list[SourceFact]) -> list[SourceFact]:
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
        "demo.fact.financing.y", "demo.finding.financing.y", BORROW_Y, PERIOD_B, INST_B, PROG_B, "100"
    )
    return [box, link_x, link_y, financing_x, financing_y, *enrolments]


class DeclaredSubjectDispatchesPerSubject(unittest.TestCase):
    """Both runners dispatch a declared-subject rule per subject and do not
    also evaluate it once (unsuffixed)."""

    def test_dispatches_per_subject_and_does_not_evaluate_once(self) -> None:
        s1 = _box(BOX_S1, BOX_S1_FINDING, LENDER_A, STATEMENT_1, "1000")
        s2 = _box(BOX_S2, BOX_S2_FINDING, LENDER_B, STATEMENT_2, "400")
        rule = _echo_rule_v11()
        forward, backward = _both_runners([rule], [s1, s2])
        for result in (forward, backward):
            symbols = {pub.finding["symbol"] for pub in result.publications}
            self.assertEqual(
                symbols,
                {f"demo.tax.echo-box1|{BOX_S1}", f"demo.tax.echo-box1|{BOX_S2}"},
            )
            self.assertNotIn("demo.tax.echo-box1", symbols)
            values = {pub.finding["symbol"]: pub.finding["value"] for pub in result.publications}
            self.assertEqual(values[f"demo.tax.echo-box1|{BOX_S1}"], "1000")
            self.assertEqual(values[f"demo.tax.echo-box1|{BOX_S2}"], "400")
            for row in result.dispositions:
                self.assertNotEqual(row.get("symbol"), "demo.tax.echo-box1")
        self.assertEqual(
            {p.finding["id"] for p in forward.publications},
            {p.finding["id"] for p in backward.publications},
        )


class PredecessorChainThroughRealSchedulers(unittest.TestCase):
    """Status (subject: financing), link reduction (subject: link), then the
    amount rule (subject: box 1) -- scheduled by ``run``/``run_reference``
    themselves, not hand-dispatched."""

    def _run_chain(
        self, rules: list[dict[str, Any]], sources: list[SourceFact]
    ) -> tuple[Any, Any]:
        return _both_runners(rules, sources)

    def _row(self, result: Any, symbol: str) -> dict[str, Any]:
        rows: list[dict[str, Any]] = [
            row for row in result.dispositions if row.get("symbol") == symbol
        ]
        self.assertEqual(len(rows), 1, result.dispositions)
        return rows[0]

    def test_blocked_predecessor_releases_successor_and_fails_closed(self) -> None:
        enrol = _enrolment(
            "demo.fact.enrolment.x",
            "demo.finding.enrolment.x",
            _full_enrolment_keys(PERIOD_A, INST_A, PROG_A),
            "100",
        )
        rules = [_status_rule_v11(), _reduction_rule_v11(), _coverage_rule_v11()]
        sources = _chain_sources(enrolments=[enrol])
        forward, backward = self._run_chain(rules, sources)
        for result in (forward, backward):
            status_x = self._row(result, f"{STATUS}|demo.fact.financing.x")
            status_y = self._row(result, f"{STATUS}|demo.fact.financing.y")
            self.assertEqual(status_x["disposition"], "published")
            self.assertEqual(status_y["disposition"], "blocked")
            self.assertEqual(status_y["code"], "DEPENDENCY_ABSENT")
            self.assertEqual(status_y["missing"], [ENROLMENT])
            reduction_x = self._row(result, f"{REDUCTIONS}|demo.fact.link.x")
            reduction_y = self._row(result, f"{REDUCTIONS}|demo.fact.link.y")
            self.assertEqual(reduction_x["disposition"], "published")
            self.assertEqual(reduction_y["disposition"], "blocked")
            self.assertEqual(reduction_y["code"], "DEPENDENCY_ABSENT")
            self.assertEqual(reduction_y["missing"], [STATUS])
            amount = self._row(result, f"{AMOUNT}|{BOX_S1}")
            self.assertEqual(amount["disposition"], "blocked")
            self.assertEqual(amount["code"], "DEPENDENCY_INVALID")
            self.assertEqual(amount["missing"], [LINK_Y_FINDING])
            self.assertNotIn(PARAM_ID, {pin["id"] for pin in amount["pins"]})
        self.assertEqual(
            {p.finding["id"] for p in forward.publications},
            {p.finding["id"] for p in backward.publications},
        )

    def test_inapplicable_predecessor_releases_successor(self) -> None:
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
            "demo.fact.financing.y", "demo.finding.financing.y", BORROW_Y, PERIOD_B, INST_B, PROG_B, "0"
        )
        sources = [box, link_x, link_y, financing_x, financing_y, enrol_x, enrol_y]
        rules = [_status_rule_v11(when=guard), _reduction_rule_v11(), _coverage_rule_v11()]
        forward, backward = self._run_chain(rules, sources)
        for result in (forward, backward):
            status_y = self._row(result, f"{STATUS}|demo.fact.financing.y")
            self.assertEqual(status_y["disposition"], "inapplicable")
            self.assertEqual(self._row(result, f"{REDUCTIONS}|demo.fact.link.y")["missing"], [STATUS])
            self.assertEqual(self._row(result, f"{AMOUNT}|{BOX_S1}")["missing"], [LINK_Y_FINDING])

    def test_reversed_declaration_order_still_waits_for_the_reduction_publisher(self) -> None:
        """Eligibility waits on the reductions publisher though that name is
        not in ``requires``. Listing the amount rule *first* would let a
        symbol-gated scheduler fire it before the reduction exists; a
        one-time-resolved rule can never retry, so a premature fire would
        stay wrongly blocked forever instead of the correct 900."""
        box = _box(BOX_S1, BOX_S1_FINDING, LENDER_A, STATEMENT_1, "1000")
        link_x = _keyed(
            LINKS,
            LINK_X_FINDING,
            _statement_keys(LENDER_A, STATEMENT_1) + (("borrowing", BORROW_X),),
            "1",
            fact_id="demo.fact.link.x",
        )
        financing_x = _financing(
            "demo.fact.financing.x", "demo.finding.financing.x", BORROW_X, PERIOD_A, INST_A, PROG_A, "tuition"
        )
        enrol = _enrolment(
            "demo.fact.enrolment.x",
            "demo.finding.enrolment.x",
            _full_enrolment_keys(PERIOD_A, INST_A, PROG_A),
            "100",
        )
        sources = [box, link_x, financing_x, enrol]
        rules = [_coverage_rule_v11(), _reduction_rule_v11(), _status_rule_v11()]
        forward, backward = self._run_chain(rules, sources)
        for result in (forward, backward):
            amount = self._row(result, f"{AMOUNT}|{BOX_S1}")
            self.assertEqual(amount["disposition"], "published")
            finding = next(
                p.finding for p in result.publications if p.finding["symbol"] == f"{AMOUNT}|{BOX_S1}"
            )
            self.assertEqual(finding["value"], "900")


class DontWaitWhenPublisherIsAbsent(unittest.TestCase):
    """If no rule in the package publishes a predecessor name, eligibility
    does not wait on it -- the same posture ``consequence_eligibility``
    takes when its named predecessor is absent."""

    def test_missing_predecessor_rule_does_not_block_eligibility(self) -> None:
        box = _box(BOX_S1, BOX_S1_FINDING, LENDER_A, STATEMENT_1, "1000")
        rule = _coverage_rule_v11()
        ctx = _ctx([rule], [box])
        prepared = _Run(ctx, DerivationSchemas())
        self.assertTrue(prepared.is_eligible(rule))

        forward, backward = run(ctx, DerivationSchemas()), run_reference(ctx, DerivationSchemas())
        for result in (forward, backward):
            finding = next(
                p.finding for p in result.publications if p.finding["symbol"] == f"{AMOUNT}|{BOX_S1}"
            )
            self.assertEqual(finding["value"], "1000")
            self.assertIn(PARAM_ID, {pin["id"] for pin in finding["pins"]})


class FinalizeUnreachedSubjectPath(unittest.TestCase):
    """``finalize_unreached`` takes the same per-subject call, before the
    ordinary guard/value fallback -- exercised directly, without a prior
    saturation loop, the same shape the pre-existing v10 finalize probe uses."""

    def test_finalize_unreached_dispatches_the_declared_subject_rule(self) -> None:
        box = _box(BOX_S1, BOX_S1_FINDING, LENDER_A, STATEMENT_1, "1000")
        rule = _coverage_rule_v11()
        ctx = _ctx([rule], [box])
        prepared = _Run(ctx, DerivationSchemas())
        self.assertNotIn(rule["id"], prepared.resolved)
        prepared.finalize_unreached()
        self.assertIn(rule["id"], prepared.resolved)
        rows = [row for row in prepared.dispositions if row.get("symbol") == f"{AMOUNT}|{BOX_S1}"]
        self.assertEqual(len(rows), 1, prepared.dispositions)
        self.assertEqual(rows[0]["disposition"], "published")


class V10Unaffected(unittest.TestCase):
    """A v1-v10 rule is unchanged -- same disposition bytes as before this
    unit. Reproduces ``tests.test_sli_g2_binding_probe.Schedulers.
    test_both_runners_record_ordinary_absence_and_agree`` after this unit's
    ``runner.py``/``subject_dispatch.py`` edits, to prove no drift."""

    def test_v10_rules_still_evaluate_once_unsuffixed_and_agree(self) -> None:
        ctx = _ctx([_status_rule(), _reduction_rule(), _coverage_v10()], [])
        schemas = DerivationSchemas()
        forward = run(ctx, schemas)
        backward = run_reference(ctx, schemas)

        def outcomes(result: Any) -> set[tuple[str, str, tuple[str, ...]]]:
            return {
                (str(row["artifact_id"]), str(row["code"]), tuple(row["missing"]))
                for row in result.dispositions
                if row["disposition"] == "blocked"
            }

        expected = {
            (STATUS_RULE_ID, "DEPENDENCY_ABSENT", (ENROLMENT,)),
            ("demo.rule.link-reduction", "DEPENDENCY_ABSENT", (STATUS,)),
            (COVERAGE_ID, "DEPENDENCY_ABSENT", (BOX1,)),
        }
        self.assertEqual(outcomes(forward), expected)
        self.assertEqual(outcomes(backward), expected)
        self.assertEqual(forward.publications, [])
        self.assertEqual(backward.publications, [])
        for result in (forward, backward):
            for row in result.dispositions:
                self.assertNotIn("|", str(row.get("symbol", "")))


if __name__ == "__main__":
    unittest.main()
