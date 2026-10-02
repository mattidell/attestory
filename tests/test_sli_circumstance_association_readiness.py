"""Readiness-gate evidence for the Student Loan Circumstance Association
milestone (section 9 of ``outline-product-and-evidence.md``).

Disposable evidence, not a design. It raises two load-bearing claims from
evidence level ``read`` to ``run``:

- **check 1 (dereference)** -- whether the adopted per-pairing primitive,
  ``packages.derivation.pairing_dispatch.evaluate_pairing_scoped_rule``, can
  carry a Form 1098-E box-1 statement / schooling-circumstance relationship
  at all, and what happens when the prior milestone's cardinality-gated rule
  shape is attempted inside pairing scope.
- **check 2 (omission)** -- what a run does with a statement nobody
  associated, observed rather than designed.

Nothing here selects a representation. The "one finding, structured value"
circumstance shape used below is the shape ADR-0067's ``field`` selector
favours; it is explicitly provisional (outline U1) and is not adopted by
this module or by anything that imports it -- nothing does; per the
harness-precedent note, this module is not to be imported from.

Synthetic ``demo.*`` identities only. No fact type, rule, or environment
constructed here is a production citizen; the pairing-local ``Environment``
below is a disposable copy built to exercise the *generic* primitive, not a
generalisation of ``packages/tax/pairing_consequences.py`` (which is not
modified, and not imported for its private helper).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import unittest

from packages.derivation.evaluator import AccessLog, EvalBlocked, Environment, evaluate
from packages.derivation.loader import DerivationSchemas
from packages.derivation.marshal import marshal_run_context
from packages.derivation.pairing_dispatch import (
    PairingBinding,
    PairingBlock,
    PairingPublish,
    PairingScopedResult,
    evaluate_pairing_scoped_rule,
)
from packages.derivation.runner import RunContext
from packages.kernel.currency import CurrencyView
from packages.kernel.facts import fact_id_for

# Synthetic fact types. Names deliberately carry a ``demo.`` prefix and are
# not the real production fact-type ids -- this module adopts no content
# citizen. The box-1 identity keys (lender + statement + tax-year) mirror
# ``packages/content/tax/2025/f1098e.bundle.json``'s real box-1 fact type,
# per the charter's supporting-context pointer, and the box-1 value stays a
# bare nonnegative number as that fact type's own value_schema declares.
BOX1_TYPE = "demo.tax.f1098e.box1-student-loan-interest"
CIRCUMSTANCE_TYPE = "demo.tax.schooling-circumstance"
PAIRING_TYPE = "demo.association.statement~circumstance"

LENDER = "demo.lender.north"
YEAR = "2025"

ADOPTION_PIN = {
    "role": "adoption",
    "id": "demo.package.sli-circumstance-readiness",
    "version": "v1",
}
RULE_ID = "demo.rule.sli-circumstance-dereference"
RULE_VERSION = "v1"

# The single declared rule expression check 1 dispatches, pairing-scoped.
# It depends on both sides: the left symbol is bound to the bare box-1
# amount (a plain number, matching the real fact type's value_schema); the
# right symbol is bound to the provisional structured circumstance value,
# read here through ADR-0067's ``field`` selector.
VALUE_EXPR: dict[str, Any] = {
    "op": "multiply",
    "left": {"op": "ref", "name": BOX1_TYPE},
    "right": {"op": "ref", "name": CIRCUMSTANCE_TYPE, "field": "qualified_fraction"},
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


def _box1_fact_id(statement: str) -> str:
    return fact_id_for(
        BOX1_TYPE, (("lender", LENDER), ("statement", statement), ("tax-year", YEAR))
    )


def _circumstance_fact_id(period: str) -> str:
    return fact_id_for(CIRCUMSTANCE_TYPE, (("period", period),))


def _pairing_fact_id(statement: str, period: str) -> str:
    return fact_id_for(PAIRING_TYPE, (("left", statement), ("right", period)))


def _sources_for(findings: dict[str, dict[str, Any]]) -> RunContext:
    return marshal_run_context(
        run_id="demo.sli-circumstance-readiness",
        state=_State(findings),  # type: ignore[arg-type]
        currency=_currency(list(findings)),
        rules=[],
        parameters={},
        canon={},
        adoption_pin=ADOPTION_PIN,
        governance_pins=[],
        collect_source_names=[BOX1_TYPE, CIRCUMSTANCE_TYPE, PAIRING_TYPE],
    )


def _symbol_for(prefix: str) -> Callable[[PairingBinding], str]:
    def _symbol(binding: PairingBinding) -> str:
        return f"{prefix}.{binding.pairing_fact_id}"

    return _symbol


def _pairing_local_environment(binding: PairingBinding) -> Environment:
    """Disposable copy of the provisional pairing-local environment shape.

    Mirrors what ``packages/tax/pairing_consequences.py``'s
    ``_pairing_local_environment`` is documented to build (two symbols,
    empty sources, empty closed sets) -- rebuilt here rather than imported,
    per the charter's harness-precedent note, and exercised only against
    the generic ``evaluate_pairing_scoped_rule`` primitive, never against
    the production module.
    """
    symbols = {BOX1_TYPE: binding.left_value, CIRCUMSTANCE_TYPE: binding.right_value}
    return Environment(symbols, {}, frozenset(), {}, {})


def _evaluate_declared(binding: PairingBinding) -> PairingPublish | PairingBlock:
    """Evaluate-one: run the one declared expression pairing-scoped.

    ``evaluate``'s arithmetic ops return ``Decimal``, which the runner's
    content-addressed id hashing cannot serialize directly (the same
    reason ``pairing_consequences._evaluate_one_factory`` formats its
    published amount with ``format(amount, "f")`` rather than publishing
    the ``Decimal`` itself); this does the same, as a string.
    """
    env = _pairing_local_environment(binding)
    access = AccessLog()
    try:
        value = evaluate(VALUE_EXPR, env, access)
    except EvalBlocked as exc:
        return PairingBlock(code=exc.category, missing=tuple(exc.missing))
    return PairingPublish(value=format(value, "f"))


def _make_prior_consumer_shape(expr: dict[str, Any]) -> Callable[[PairingBinding], PairingPublish | PairingBlock]:
    """An evaluate-one that dispatches the named expression pairing-scoped.

    Used to exercise ``require_closed``/``count`` -- the prior milestone's
    cardinality-gated rule shape -- inside pairing scope, not to adopt it.
    """

    def _evaluate_one(binding: PairingBinding) -> PairingPublish | PairingBlock:
        env = _pairing_local_environment(binding)
        access = AccessLog()
        try:
            value = evaluate(expr, env, access)
        except EvalBlocked as exc:
            return PairingBlock(code=exc.category, missing=tuple(exc.missing))
        return PairingPublish(value=value)

    return _evaluate_one


class DereferenceCheck(unittest.TestCase):
    """Check 1 -- outline section 9(1). Ceiling: this raises sections 5 and

    6(a) of the outline from evidence level ``read`` to ``run``. It does
    not settle U1 (whether one structured circumstance finding is the right
    correction granularity for a person) -- that remains an owner decision.
    """

    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.box1_fact_id = _box1_fact_id("S-1")
        self.circumstance_fact_id = _circumstance_fact_id("2025-fall")
        self.pairing_fact_id = _pairing_fact_id("S-1", "2025-fall")

    def _dispatch(
        self,
        sources: list[Any],
        *,
        evaluate_one: Callable[[PairingBinding], PairingPublish | PairingBlock] = _evaluate_declared,
    ) -> PairingScopedResult:
        return evaluate_pairing_scoped_rule(
            sources=sources,
            pairing_type=PAIRING_TYPE,
            left_type=BOX1_TYPE,
            right_type=CIRCUMSTANCE_TYPE,
            rule_id=RULE_ID,
            rule_version=RULE_VERSION,
            symbol_for=_symbol_for("demo.pairing.sli-circumstance"),
            evaluate_one=evaluate_one,
            extra_pins=[ADOPTION_PIN],
            schemas=self.schemas,
        )

    def _base_findings(self, *, qualified_fraction: float) -> dict[str, dict[str, Any]]:
        return {
            "f.box1": _finding("f.box1", self.box1_fact_id, 2000.0),
            "f.circumstance": _finding(
                "f.circumstance",
                self.circumstance_fact_id,
                {"qualified_fraction": qualified_fraction},
            ),
            "f.pairing": _finding(
                "f.pairing",
                self.pairing_fact_id,
                {"left_fact_id": self.box1_fact_id, "right_fact_id": self.circumstance_fact_id},
            ),
        }

    def test_1_published_value_depends_on_both_sides(self) -> None:
        """Assertion 1: the value read, proven by changing the right side.

        A publication count alone proves nothing; this changes the right
        side's named property and observes a different published value.
        """
        ctx_full = _sources_for(self._base_findings(qualified_fraction=1.0))
        result_full = self._dispatch(ctx_full.sources)
        self.assertEqual(result_full.blocked, ())
        self.assertEqual(len(result_full.publications), 1)
        self.assertEqual(result_full.publications[0]["value"], "2000.00")

        ctx_half = _sources_for(self._base_findings(qualified_fraction=0.5))
        result_half = self._dispatch(ctx_half.sources)
        self.assertEqual(result_half.blocked, ())
        self.assertEqual(len(result_half.publications), 1)
        self.assertEqual(result_half.publications[0]["value"], "1000.00")

        # The published value genuinely differs -- dependence on the right
        # side's named property, not a constant echoing the left side alone.
        self.assertNotEqual(
            result_full.publications[0]["value"], result_half.publications[0]["value"]
        )

    def test_2_publication_pins_the_pairing_and_both_sides_by_exact_id(self) -> None:
        """Assertion 2: the exact pinned ids, not a count."""
        ctx = _sources_for(self._base_findings(qualified_fraction=1.0))
        result = self._dispatch(ctx.sources)
        self.assertEqual(len(result.publications), 1)
        pin_ids = {p["id"] for p in result.publications[0]["pins"]}
        self.assertIn("f.pairing", pin_ids)
        self.assertIn("f.box1", pin_ids)
        self.assertIn("f.circumstance", pin_ids)

    def test_3_missing_right_side_blocks_dependency_absent_naming_it(self) -> None:
        """Assertion 3: loss of the target -- the "surviving reference is

        not sufficient support" behaviour. Observed: this comes for free
        from ``evaluate_pairing_scoped_rule``'s own left/right resolution --
        it never reaches ``evaluate_one`` at all when the right side is
        absent, so no rule-author effort produces this disposition.
        """
        findings = self._base_findings(qualified_fraction=1.0)
        del findings["f.circumstance"]

        def should_not_run(_binding: PairingBinding) -> PairingPublish:
            raise AssertionError("evaluate_one must not run when the right side is absent")

        ctx = _sources_for(findings)
        result = self._dispatch(ctx.sources, evaluate_one=should_not_run)
        self.assertEqual(result.publications, ())
        self.assertEqual(len(result.blocked), 1)
        self.assertEqual(result.blocked[0].code, "DEPENDENCY_ABSENT")
        self.assertEqual(result.blocked[0].missing, (self.circumstance_fact_id,))

    def test_4a_require_closed_blocks_pairing_scoped(self) -> None:
        """Assertion 4 (require_closed half): the prior consumer's

        cardinality-gate machinery cannot enter pairing scope. Observed
        code: ``SOURCE_SET_UNCLOSED`` -- the pairing-local environment's
        ``closed_sets`` is the empty frozenset, so ``require_closed`` fails
        closed on any source-set name, not ``DEPENDENCY_ABSENT``.
        """
        ctx = _sources_for(self._base_findings(qualified_fraction=1.0))
        expr = {"op": "require_closed", "source_set": BOX1_TYPE}
        result = self._dispatch(ctx.sources, evaluate_one=_make_prior_consumer_shape(expr))
        self.assertEqual(result.publications, ())
        self.assertEqual(len(result.blocked), 1)
        self.assertEqual(result.blocked[0].code, "SOURCE_SET_UNCLOSED")

    def test_4b_count_blocks_pairing_scoped(self) -> None:
        """Assertion 4 (count half): same claim, second operator.

        Observed code: ``SOURCE_SET_UNCLOSED`` -- ``count`` also gates on
        ``source_set in env.closed_sets`` before it ever reads
        ``env.sources``, and pairing scope supplies neither.
        """
        ctx = _sources_for(self._base_findings(qualified_fraction=1.0))
        expr = {"op": "count", "name": BOX1_TYPE, "source_set": BOX1_TYPE}
        result = self._dispatch(ctx.sources, evaluate_one=_make_prior_consumer_shape(expr))
        self.assertEqual(result.publications, ())
        self.assertEqual(len(result.blocked), 1)
        self.assertEqual(result.blocked[0].code, "SOURCE_SET_UNCLOSED")


class OmissionCheck(unittest.TestCase):
    """Check 2 -- outline section 9(2). Ceiling: this observes what the

    dispatcher does with a statement nobody associated; it designs no
    completeness mechanism and settles no part of U2.

    Expected disposition, recorded before execution per the charter: one
    publication for the associated statement (S-1 / 2025-fall), and for the
    unassociated statement (S-2) no row of any kind -- neither a
    publication nor a blocked row.
    """

    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.box1_associated = _box1_fact_id("S-1")
        self.box1_unassociated = _box1_fact_id("S-2")
        self.circumstance_fact_id = _circumstance_fact_id("2025-fall")
        self.pairing_fact_id = _pairing_fact_id("S-1", "2025-fall")

    def test_unassociated_statement_produces_no_row_of_any_kind(self) -> None:
        findings = {
            "f.box1.associated": _finding("f.box1.associated", self.box1_associated, 2000.0),
            "f.box1.unassociated": _finding("f.box1.unassociated", self.box1_unassociated, 3000.0),
            "f.circumstance": _finding(
                "f.circumstance", self.circumstance_fact_id, {"qualified_fraction": 1.0}
            ),
            "f.pairing": _finding(
                "f.pairing",
                self.pairing_fact_id,
                {"left_fact_id": self.box1_associated, "right_fact_id": self.circumstance_fact_id},
            ),
        }
        ctx = _sources_for(findings)

        # The unassociated statement's box-1 source is genuinely present in
        # the run -- the silence to be observed is the dispatcher's
        # iteration, not a missing fixture.
        box1_sources = [s for s in ctx.sources if s.name == BOX1_TYPE]
        self.assertEqual(len(box1_sources), 2)
        self.assertIn(
            self.box1_unassociated, {s.fact_id for s in box1_sources}
        )

        result = evaluate_pairing_scoped_rule(
            sources=ctx.sources,
            pairing_type=PAIRING_TYPE,
            left_type=BOX1_TYPE,
            right_type=CIRCUMSTANCE_TYPE,
            rule_id=RULE_ID,
            rule_version=RULE_VERSION,
            symbol_for=_symbol_for("demo.pairing.sli-circumstance"),
            evaluate_one=_evaluate_declared,
            extra_pins=[ADOPTION_PIN],
            schemas=self.schemas,
        )

        # Exactly one publication, corresponding to the associated pairing.
        self.assertEqual(len(result.publications), 1)
        pin_ids = {p["id"] for p in result.publications[0]["pins"]}
        self.assertIn("f.pairing", pin_ids)
        self.assertIn("f.box1.associated", pin_ids)
        self.assertNotIn("f.box1.unassociated", pin_ids)

        # No blocked row names the unassociated statement's fact id, and
        # there is no blocked row at all -- the dispatcher iterates
        # pairings, and the unassociated statement is never a pairing's
        # named side.
        self.assertEqual(result.blocked, ())
        for blocked in result.blocked:
            self.assertNotIn(self.box1_unassociated, blocked.missing)

        # If this had come out otherwise -- a blocked row naming S-2 -- the
        # charter requires stopping and reporting it as a material finding
        # rather than adjusting this expectation. It did not.


if __name__ == "__main__":
    unittest.main()
