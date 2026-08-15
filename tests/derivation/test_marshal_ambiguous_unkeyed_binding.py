"""Track 6b repair (f1098e-student-loan-interest-agi): the marshal.py
ambiguity guard.

Direct unit tests against ``marshal_run_context`` with a hand-built
``FindingState``/``CurrencyView``, constructing a synthetic unkeyed binding
that matches two or more current findings for a symbol that is not a
collect source name -- the guard's own trigger condition -- and confirming
the symbol is left unbound (an ordinary blocked disposition downstream),
never an unguarded pick and never a raise.

Exercises both marshal.py code paths that resolve an unkeyed symbol
(fact-type-id-keyed, no per-member key):

- the explicit ``input_bindings`` loop (``binding["symbol"] ==
  binding["fact_type"]["id"]``)
- the "legacy demo path" fallback loop (an unbound current finding whose
  fact type is required by some rule's own symbol surface), which is the
  actual live mechanism for both this milestone's witnesses and Form 1098's
  latent 14 refs (neither has an explicit package-level ``input_bindings``
  entry) before Track 6b's own content repair moved this milestone's
  witnesses off it entirely.

Also proves the refinement documented in ``marshal.py``'s own guard
comments: ambiguity is about *disagreement*, not mere multiplicity -- two or
more current findings that all agree on one value are bound normally (no
regression for `tests/test_f1098_mortgage_interest_lifecycle.py`'s
multi-statement-but-agreeing fixtures).
"""

from __future__ import annotations

import unittest
from typing import Any

from packages.derivation.marshal import marshal_run_context
from packages.kernel.currency import CurrencyView

ADOPTION_PIN = {"role": "adoption", "id": "demo.package", "version": "v1"}
GOV_PINS: list[dict[str, Any]] = []
FACT_TYPE = "tax.us.2025.demo.no-witness"


class _HorizonState:
    def __init__(self) -> None:
        self.current_by_chain: dict[tuple[str, str, str], str] = {}


class _State:
    """Minimal stand-in for FindingState: marshal_run_context only reads
    ``.findings`` (a mapping of finding id -> finding dict) and
    ``.horizon_state.current_by_chain`` (closure-authority marshalling,
    empty here -- these tests exercise symbol binding only)."""

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


def _rule(*, requires: list[str]) -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v4",
        "id": "demo.rule",
        "version": "v1",
        "requires": requires,
        "when": True,
        "value": 0,
    }


class ExplicitBindingLoopGuard(unittest.TestCase):
    """The ``input_bindings``-list-driven loop (``marshal.py`` lines ~233-270)."""

    def _bindings(self) -> list[dict[str, Any]]:
        return [
            {
                "symbol": FACT_TYPE,
                "fact_type": {"id": FACT_TYPE, "version": "v1"},
                "mode": "required",
            }
        ]

    def test_two_disagreeing_matches_are_left_unbound(self) -> None:
        findings = {
            "f.1": _finding("f.1", f"{FACT_TYPE}|lender=a,statement=a,tax-year=2025", "no"),
            "f.2": _finding("f.2", f"{FACT_TYPE}|lender=b,statement=b,tax-year=2025", "yes"),
        }
        state = _State(findings)
        currency = _currency(["f.1", "f.2"])
        ctx = marshal_run_context(
            run_id="run.1",
            state=state,  # type: ignore[arg-type]
            currency=currency,
            rules=[],
            parameters={},
            canon={},
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOV_PINS,
            input_bindings=self._bindings(),
        )
        self.assertEqual([i for i in ctx.inputs if i.symbol == FACT_TYPE], [])

    def test_two_agreeing_matches_bind_normally(self) -> None:
        findings = {
            "f.1": _finding("f.1", f"{FACT_TYPE}|lender=a,statement=a,tax-year=2025", "yes"),
            "f.2": _finding("f.2", f"{FACT_TYPE}|lender=b,statement=b,tax-year=2025", "yes"),
        }
        state = _State(findings)
        currency = _currency(["f.1", "f.2"])
        ctx = marshal_run_context(
            run_id="run.1",
            state=state,  # type: ignore[arg-type]
            currency=currency,
            rules=[],
            parameters={},
            canon={},
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOV_PINS,
            input_bindings=self._bindings(),
        )
        matches = [i for i in ctx.inputs if i.symbol == FACT_TYPE]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].value, "yes")

    def test_single_match_binds_normally(self) -> None:
        findings = {
            "f.1": _finding("f.1", f"{FACT_TYPE}|lender=a,statement=a,tax-year=2025", "no"),
        }
        state = _State(findings)
        currency = _currency(["f.1"])
        ctx = marshal_run_context(
            run_id="run.1",
            state=state,  # type: ignore[arg-type]
            currency=currency,
            rules=[],
            parameters={},
            canon={},
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOV_PINS,
            input_bindings=self._bindings(),
        )
        matches = [i for i in ctx.inputs if i.symbol == FACT_TYPE]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].value, "no")

    def test_disagreeing_matches_do_not_raise(self) -> None:
        """The trap the owner named explicitly: refuse to bind, never raise."""
        findings = {
            "f.1": _finding("f.1", f"{FACT_TYPE}|lender=a,statement=a,tax-year=2025", "no"),
            "f.2": _finding("f.2", f"{FACT_TYPE}|lender=b,statement=b,tax-year=2025", "yes"),
        }
        state = _State(findings)
        currency = _currency(["f.1", "f.2"])
        try:
            marshal_run_context(
                run_id="run.1",
                state=state,  # type: ignore[arg-type]
                currency=currency,
                rules=[],
                parameters={},
                canon={},
                adoption_pin=ADOPTION_PIN,
                governance_pins=GOV_PINS,
                input_bindings=self._bindings(),
            )
        except Exception as exc:  # noqa: BLE001 - the assertion below is the point
            self.fail(f"marshal_run_context raised instead of leaving the symbol unbound: {exc!r}")

    def test_collect_source_name_symbol_is_never_touched_by_this_loop(self) -> None:
        findings = {
            "f.1": _finding("f.1", f"{FACT_TYPE}|lender=a,statement=a,tax-year=2025", "no"),
            "f.2": _finding("f.2", f"{FACT_TYPE}|lender=b,statement=b,tax-year=2025", "yes"),
        }
        state = _State(findings)
        currency = _currency(["f.1", "f.2"])
        ctx = marshal_run_context(
            run_id="run.1",
            state=state,  # type: ignore[arg-type]
            currency=currency,
            rules=[],
            parameters={},
            canon={},
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOV_PINS,
            input_bindings=self._bindings(),
            collect_source_names=[FACT_TYPE],
        )
        # Never bound as a single-value input (ambiguous or not -- a
        # collect source name is read via sources, not this loop).
        self.assertEqual([i for i in ctx.inputs if i.symbol == FACT_TYPE], [])
        self.assertEqual(sorted(s.value for s in ctx.sources if s.name == FACT_TYPE), ["no", "yes"])


class FallbackLoopGuard(unittest.TestCase):
    """The "legacy demo path" fallback loop (``marshal.py`` lines ~299-378):
    an unbound current finding whose fact type is required by some rule's
    own symbol surface, matched with no explicit ``input_bindings`` entry
    at all -- the actual live mechanism for this milestone's witnesses and
    for Form 1098's own latent 14 refs, prior to this milestone's content
    repair moving its own witnesses off it entirely."""

    def test_two_disagreeing_matches_are_left_unbound(self) -> None:
        findings = {
            "f.1": _finding("f.1", f"{FACT_TYPE}|lender=a,statement=a,tax-year=2025", "no"),
            "f.2": _finding("f.2", f"{FACT_TYPE}|lender=b,statement=b,tax-year=2025", "yes"),
        }
        state = _State(findings)
        currency = _currency(["f.1", "f.2"])
        ctx = marshal_run_context(
            run_id="run.1",
            state=state,  # type: ignore[arg-type]
            currency=currency,
            rules=[_rule(requires=[FACT_TYPE])],
            parameters={},
            canon={},
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOV_PINS,
        )
        self.assertEqual([i for i in ctx.inputs if i.symbol == FACT_TYPE], [])

    def test_two_agreeing_matches_bind_normally(self) -> None:
        findings = {
            "f.1": _finding("f.1", f"{FACT_TYPE}|lender=a,statement=a,tax-year=2025", "yes"),
            "f.2": _finding("f.2", f"{FACT_TYPE}|lender=b,statement=b,tax-year=2025", "yes"),
        }
        state = _State(findings)
        currency = _currency(["f.1", "f.2"])
        ctx = marshal_run_context(
            run_id="run.1",
            state=state,  # type: ignore[arg-type]
            currency=currency,
            rules=[_rule(requires=[FACT_TYPE])],
            parameters={},
            canon={},
            adoption_pin=ADOPTION_PIN,
            governance_pins=GOV_PINS,
        )
        matches = [i for i in ctx.inputs if i.symbol == FACT_TYPE]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].value, "yes")

    def test_disagreeing_matches_do_not_raise(self) -> None:
        findings = {
            "f.1": _finding("f.1", f"{FACT_TYPE}|lender=a,statement=a,tax-year=2025", "no"),
            "f.2": _finding("f.2", f"{FACT_TYPE}|lender=b,statement=b,tax-year=2025", "yes"),
        }
        state = _State(findings)
        currency = _currency(["f.1", "f.2"])
        try:
            marshal_run_context(
                run_id="run.1",
                state=state,  # type: ignore[arg-type]
                currency=currency,
                rules=[_rule(requires=[FACT_TYPE])],
                parameters={},
                canon={},
                adoption_pin=ADOPTION_PIN,
                governance_pins=GOV_PINS,
            )
        except Exception as exc:  # noqa: BLE001 - the assertion below is the point
            self.fail(f"marshal_run_context raised instead of leaving the symbol unbound: {exc!r}")


if __name__ == "__main__":
    unittest.main()
