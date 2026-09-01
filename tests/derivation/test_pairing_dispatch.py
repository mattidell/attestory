"""Per-pairing dispatch primitive (ADR-0070/0071 shared production machinery).

Reuses the relationship-constraints rung-2 spike fixtures as a starting
point, re-validated against production schema ids. Proves:

- two pairings each get independent per-pairing dispatch (no
  cross-contamination)
- an unrelated peer fact of the same type is never bound (masking
  prevention)
- two separate rules can each apply the same primitive to the same
  pairings (Seam 5's two-rule shape: one finding per pairing per rule id)
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import unittest

from packages.derivation.loader import DerivationSchemas
from packages.derivation.marshal import marshal_run_context
from packages.derivation.pairing_dispatch import (
    PairingBinding,
    PairingBlock,
    PairingPublish,
    PairingScopedResult,
    evaluate_pairing_scoped_rule,
)
from packages.derivation.runner import RunContext, _Run
from packages.kernel.currency import CurrencyView
from packages.kernel.facts import fact_id_for

ACQUISITION_TYPE = "tax.us.obligation-acquisition-circumstance"
REPORT_TYPE = "demo.tax.report-1099int-box1"
PAIRING_TYPE = "demo.association.acquisition~report"
PAYER = "demo.payer.north"
YEAR = "2025"
ADOPTION_PIN = {
    "role": "adoption",
    "id": "demo.package.pairing-dispatch",
    "version": "v1",
}
RULE_A = "demo.rule.pairing-scoped-a"
RULE_B = "demo.rule.pairing-scoped-b"


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


def _acq_fact_id(ref: str) -> str:
    return fact_id_for(ACQUISITION_TYPE, (("payer", PAYER), ("reference", ref), ("tax-year", YEAR)))


def _report_fact_id(statement: str) -> str:
    return fact_id_for(REPORT_TYPE, (("payer", PAYER), ("statement", statement), ("tax-year", YEAR)))


def _pairing_fact_id(left_ref: str, right_statement: str) -> str:
    return fact_id_for(PAIRING_TYPE, (("left", left_ref), ("right", right_statement)))


def _sources_for(findings: dict[str, dict[str, Any]]) -> RunContext:
    return marshal_run_context(
        run_id="demo.pairing-dispatch",
        state=_State(findings),  # type: ignore[arg-type]
        currency=_currency(list(findings)),
        rules=[],
        parameters={},
        canon={},
        adoption_pin=ADOPTION_PIN,
        governance_pins=[],
        collect_source_names=[ACQUISITION_TYPE, REPORT_TYPE, PAIRING_TYPE],
    )


def _publish_reported_amount(binding: PairingBinding) -> PairingPublish:
    amount = binding.right_value["interest_income"]
    return PairingPublish(value=amount)


def _symbol_for(prefix: str) -> Callable[[PairingBinding], str]:
    def _symbol(binding: PairingBinding) -> str:
        return f"{prefix}.{binding.pairing_fact_id}"

    return _symbol


class PairingDispatch(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.acq1 = _acq_fact_id("ACQ-1")
        self.acq2 = _acq_fact_id("ACQ-2")
        self.rpt1 = _report_fact_id("s1")
        self.rpt2 = _report_fact_id("s2")
        self.pairing_1 = _pairing_fact_id("ACQ-1", "s1")
        self.pairing_2 = _pairing_fact_id("ACQ-2", "s1")

    def _dispatch(
        self,
        sources: list[Any],
        *,
        rule_id: str = RULE_A,
        evaluate_one: Callable[[PairingBinding], PairingPublish | PairingBlock] = _publish_reported_amount,
    ) -> PairingScopedResult:
        return evaluate_pairing_scoped_rule(
            sources=sources,
            pairing_type=PAIRING_TYPE,
            left_type=ACQUISITION_TYPE,
            right_type=REPORT_TYPE,
            rule_id=rule_id,
            rule_version="v1",
            symbol_for=_symbol_for(f"demo.pairing.{rule_id}"),
            evaluate_one=evaluate_one,
            extra_pins=[ADOPTION_PIN],
            schemas=self.schemas,
        )

    def test_masking_unrelated_peer_of_same_type_is_never_bound(self) -> None:
        findings = {
            "f.acq1": _finding(
                "f.acq1", self.acq1, {"accrued_interest_paid_to_seller": 800.0}
            ),
            "f.rpt1": _finding("f.rpt1", self.rpt1, {"interest_income": 1000.0}),
            "f.rpt2": _finding("f.rpt2", self.rpt2, {"interest_income": 50000.0}),
            "f.pair1": _finding(
                "f.pair1",
                self.pairing_1,
                {"left_fact_id": self.acq1, "right_fact_id": self.rpt1},
            ),
        }
        ctx = _sources_for(findings)
        report_sources = [s for s in ctx.sources if s.name == REPORT_TYPE]
        self.assertEqual(len(report_sources), 2)

        result = self._dispatch(ctx.sources)
        self.assertEqual(result.blocked, ())
        self.assertEqual(len(result.publications), 1)
        finding = result.publications[0]
        self.assertEqual(finding["value"], 1000.0)
        pin_ids = {p["id"] for p in finding["pins"]}
        self.assertIn("f.rpt1", pin_ids)
        self.assertNotIn("f.rpt2", pin_ids)
        self.assertIn("f.acq1", pin_ids)
        self.assertIn("f.pair1", pin_ids)

    def test_two_pairings_dispatch_independently(self) -> None:
        findings = {
            "f.acq1": _finding(
                "f.acq1", self.acq1, {"accrued_interest_paid_to_seller": 600.0}
            ),
            "f.acq2": _finding(
                "f.acq2", self.acq2, {"accrued_interest_paid_to_seller": 600.0}
            ),
            "f.rpt1": _finding("f.rpt1", self.rpt1, {"interest_income": 1000.0}),
            "f.pair1": _finding(
                "f.pair1",
                self.pairing_1,
                {"left_fact_id": self.acq1, "right_fact_id": self.rpt1},
            ),
            "f.pair2": _finding(
                "f.pair2",
                self.pairing_2,
                {"left_fact_id": self.acq2, "right_fact_id": self.rpt1},
            ),
        }
        ctx = _sources_for(findings)
        pairing_sources = [s for s in ctx.sources if s.name == PAIRING_TYPE]
        self.assertEqual(len(pairing_sources), 2)

        result = self._dispatch(ctx.sources)
        self.assertEqual(result.blocked, ())
        self.assertEqual(len(result.publications), 2)
        symbols = {f["symbol"] for f in result.publications}
        self.assertEqual(
            symbols,
            {
                f"demo.pairing.{RULE_A}.{self.pairing_1}",
                f"demo.pairing.{RULE_A}.{self.pairing_2}",
            },
        )
        for finding in result.publications:
            pin_ids = {p["id"] for p in finding["pins"]}
            self.assertFalse({"f.acq1", "f.acq2"} <= pin_ids)
            self.assertIn("f.rpt1", pin_ids)
            self.assertTrue({"f.acq1", "f.acq2"} & pin_ids)

    def test_two_rules_each_publish_one_finding_per_pairing(self) -> None:
        findings = {
            "f.acq1": _finding(
                "f.acq1", self.acq1, {"accrued_interest_paid_to_seller": 600.0}
            ),
            "f.rpt1": _finding("f.rpt1", self.rpt1, {"interest_income": 1000.0}),
            "f.pair1": _finding(
                "f.pair1",
                self.pairing_1,
                {"left_fact_id": self.acq1, "right_fact_id": self.rpt1},
            ),
        }
        ctx = _sources_for(findings)
        first = self._dispatch(ctx.sources, rule_id=RULE_A)
        second = self._dispatch(ctx.sources, rule_id=RULE_B)
        self.assertEqual(len(first.publications), 1)
        self.assertEqual(len(second.publications), 1)
        self.assertNotEqual(
            first.publications[0]["symbol"], second.publications[0]["symbol"]
        )
        first_ids = {p["id"] for p in first.publications[0]["pins"]}
        second_ids = {p["id"] for p in second.publications[0]["pins"]}
        self.assertIn(RULE_A, first_ids)
        self.assertNotIn(RULE_B, first_ids)
        self.assertIn(RULE_B, second_ids)
        self.assertNotIn(RULE_A, second_ids)
        self.assertTrue({"f.acq1", "f.rpt1", "f.pair1"} <= first_ids)
        self.assertTrue({"f.acq1", "f.rpt1", "f.pair1"} <= second_ids)
        self.assertEqual(len(first.publications) + len(second.publications), 2)

    def test_runner_records_one_publication_per_pairing(self) -> None:
        findings = {
            "f.acq1": _finding(
                "f.acq1", self.acq1, {"accrued_interest_paid_to_seller": 600.0}
            ),
            "f.acq2": _finding(
                "f.acq2", self.acq2, {"accrued_interest_paid_to_seller": 400.0}
            ),
            "f.rpt1": _finding("f.rpt1", self.rpt1, {"interest_income": 1000.0}),
            "f.pair1": _finding(
                "f.pair1",
                self.pairing_1,
                {"left_fact_id": self.acq1, "right_fact_id": self.rpt1},
            ),
            "f.pair2": _finding(
                "f.pair2",
                self.pairing_2,
                {"left_fact_id": self.acq2, "right_fact_id": self.rpt1},
            ),
        }
        ctx = _sources_for(findings)
        run_state = _Run(ctx, self.schemas)
        run_state.evaluate_pairing_scoped_rule(
            pairing_type=PAIRING_TYPE,
            left_type=ACQUISITION_TYPE,
            right_type=REPORT_TYPE,
            rule_id=RULE_A,
            rule_version="v1",
            symbol_for=_symbol_for(f"demo.pairing.{RULE_A}"),
            evaluate_one=_publish_reported_amount,
        )
        self.assertEqual(len(run_state.publications), 2)
        self.assertEqual(run_state.blocked, [])
        self.assertIn(RULE_A, run_state.resolved)

    def test_missing_named_peer_blocks_without_binding_another(self) -> None:
        findings = {
            "f.acq1": _finding(
                "f.acq1", self.acq1, {"accrued_interest_paid_to_seller": 800.0}
            ),
            "f.rpt2": _finding("f.rpt2", self.rpt2, {"interest_income": 50000.0}),
            "f.pair1": _finding(
                "f.pair1",
                self.pairing_1,
                {"left_fact_id": self.acq1, "right_fact_id": self.rpt1},
            ),
        }
        ctx = _sources_for(findings)

        def should_not_run(_binding: PairingBinding) -> PairingPublish:
            raise AssertionError("evaluate_one must not run when the named peer is absent")

        result = self._dispatch(ctx.sources, evaluate_one=should_not_run)
        self.assertEqual(result.publications, ())
        self.assertEqual(len(result.blocked), 1)
        self.assertEqual(result.blocked[0].code, "DEPENDENCY_ABSENT")
        self.assertEqual(result.blocked[0].missing, (self.rpt1,))
        pin_ids = {p["id"] for p in result.blocked[0].pins}
        self.assertNotIn("f.rpt2", pin_ids)

    def test_evaluate_one_block_is_per_pairing(self) -> None:
        findings = {
            "f.acq1": _finding(
                "f.acq1", self.acq1, {"accrued_interest_paid_to_seller": 1200.0}
            ),
            "f.acq2": _finding(
                "f.acq2", self.acq2, {"accrued_interest_paid_to_seller": 400.0}
            ),
            "f.rpt1": _finding("f.rpt1", self.rpt1, {"interest_income": 1000.0}),
            "f.pair1": _finding(
                "f.pair1",
                self.pairing_1,
                {"left_fact_id": self.acq1, "right_fact_id": self.rpt1},
            ),
            "f.pair2": _finding(
                "f.pair2",
                self.pairing_2,
                {"left_fact_id": self.acq2, "right_fact_id": self.rpt1},
            ),
        }
        ctx = _sources_for(findings)

        def supportability(binding: PairingBinding) -> PairingPublish | PairingBlock:
            accrued = binding.left_value["accrued_interest_paid_to_seller"]
            reported = binding.right_value["interest_income"]
            if accrued > reported:
                return PairingBlock(code="ACCRUED_EXCEEDS_ASSOCIATED_REPORT")
            return PairingPublish(value=True)

        result = self._dispatch(ctx.sources, evaluate_one=supportability)
        self.assertEqual(len(result.publications), 1)
        self.assertEqual(len(result.blocked), 1)
        self.assertEqual(result.blocked[0].code, "ACCRUED_EXCEEDS_ASSOCIATED_REPORT")
        self.assertEqual(result.publications[0]["value"], True)
        published_pins = {p["id"] for p in result.publications[0]["pins"]}
        blocked_pins = {p["id"] for p in result.blocked[0].pins}
        self.assertIn("f.acq2", published_pins)
        self.assertNotIn("f.acq1", published_pins)
        self.assertIn("f.acq1", blocked_pins)
        self.assertNotIn("f.acq2", blocked_pins)


if __name__ == "__main__":
    unittest.main()
