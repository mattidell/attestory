"""Source Completeness Track 5: closure-backed zero, coverage, lifecycle.

One real act log exercises the accepted contracts end to end: attest
closure over the empty B1 family, publish the closure-backed zero, let
a late member's atomic horizon successor make the old closure and zero
noncurrent with no manual withdrawal, prove removal resurrects nothing,
and publish the successor zero only after re-attestation plus an
explicit rerun. Coverage reads the exact claim from records throughout.
"""

import json
import unittest
from typing import Any

from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.marshal import marshal_closure_authority
from packages.derivation.projection import (
    compute_derivation_currency,
    derived_findings_from_acts,
)
from packages.derivation.runner import InputFinding, RunContext, run
from packages.kernel import findings, horizons
from packages.kernel.currency import compute_currency
from packages.kernel.horizons import HorizonModelError
from packages.tax.coverage import CLOSED, OPEN, coverage_report
from packages.tax.loader import (
    TAX_CONTENT_DIR,
    load_closure_mappings,
    load_f1099int_bundle,
    load_source_families,
    tax_registry,
)

FAMILY_ID = "tax.us.2025.f1099int.b1"
FAMILY = {"id": FAMILY_ID, "version": "v1"}
SCOPE = {"tax-year": "2025", "subject": "taxpayer-primary"}
SUBTOTAL_SYMBOL = "tax.us.2025.interest.b1-subtotal"

CLOSURE_FACT_H0 = (
    "tax.us.2025.f1099int.b1.source-closure|family-horizon=b1.h0,tax-year=2025"
)
CLOSURE_FACT_H2 = (
    "tax.us.2025.f1099int.b1.source-closure|family-horizon=b1.h2,tax-year=2025"
)
MEMBER_FACT = (
    "tax.us.2025.f1099int.box1-interest|payer=demo-payer-bank-alpha,"
    "statement=stmt.demo-payer-bank-alpha.2025.a,tax-year=2025"
)


def act(kind: str, payload: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": f"b1-act-{index:03d}",
        "kind": kind,
        "actor": "user",
        "at": f"2026-07-12T02:{index:02d}:00Z",
        "committed_against": index,
        "payload": payload,
    }


def finding(finding_id: str, fact_id: str, value: Any) -> dict[str, Any]:
    return {
        "schema": "finding.v1",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "attested",
        "evidence_ids": [],
    }


def entity(entity_id: str, kind: str, label: str) -> dict[str, Any]:
    return {"schema": "entity.v1", "id": entity_id, "kind": kind, "label": label}


class LifecycleFixture(unittest.TestCase):
    registry: Any
    schemas: DerivationSchemas
    canon: dict[str, dict[str, Any]]
    families: dict[str, dict[str, Any]]
    mappings: dict[str, dict[str, Any]]
    rule: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = tax_registry()
        cls.schemas = DerivationSchemas()
        cls.canon = load_canon(cls.schemas)
        cls.families = load_source_families(cls.registry)
        cls.mappings = load_closure_mappings(cls.registry)
        cls.rule = json.loads(
            (TAX_CONTENT_DIR / "rule.f1099int-b1-subtotal.json").read_text("utf-8")
        )

    def opening_acts(self) -> list[dict[str, Any]]:
        """Adopt the vocabulary, open the chain, attest closure over nothing."""
        bundle = load_f1099int_bundle(self.registry)
        return [
            act("bundle-adoption", {"bundle": bundle}, 0),
            act(
                "horizon-genesis",
                {"family": FAMILY, "scope": SCOPE, "horizon_id": "b1.h0"},
                1,
            ),
            act(
                "assertion",
                {"finding": finding("b1.closure.h0", CLOSURE_FACT_H0, True)},
                2,
            ),
        ]

    def derive_zero(self, acts: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
        """Marshal record state, run, and return the derived-publication act."""
        state = findings.project(tuple(acts), self.registry)
        currency = compute_currency(state)
        records, current_horizons = marshal_closure_authority(
            state, currency, list(self.mappings.values())
        )
        ctx = RunContext(
            run_id=run_id,
            rules=[self.rule],
            parameters={},
            canon=self.canon,
            inputs=[
                InputFinding("rounding.convention", "half_up", "f.rounding", "input")
            ],
            sources=[],
            adoption_pin={
                "role": "adoption",
                "id": "tax.us.2025.package.interest-slice",
                "version": "v1",
            },
            governance_pins=[
                {"role": "governance", "id": "governance.constitution", "version": "v1"}
            ],
            family_declarations=list(self.families.values()),
            closure_mappings=list(self.mappings.values()),
            closure_findings=records,
            current_horizons=current_horizons,
        )
        result = run(ctx, self.schemas)
        self.assertEqual(len(result.publications), 1, msg=str(result.blocked))
        publication = result.publications[0]
        self.assertEqual(publication.finding["value"], "0")
        return act(
            "derived-publication", publication.act, len(acts)
        )

    def full_scenario(self) -> tuple[list[dict[str, Any]], str, str]:
        """The whole lifecycle; returns (acts, first zero id, successor zero id)."""
        acts = self.opening_acts()
        zero_act = self.derive_zero(acts, "tax.us.2025.run.b1-zero-1")
        first_zero = zero_act["payload"]["finding"]["id"]
        acts.append(zero_act)
        acts += [
            act(
                "entity-introduced",
                {"entity": entity("demo-payer-bank-alpha", "tax.us.interest-payer",
                                  "Bank Alpha Savings (synthetic interest payer)")},
                4,
            ),
            act(
                "entity-introduced",
                {"entity": entity("stmt.demo-payer-bank-alpha.2025.a",
                                  "tax.us.1099int-statement",
                                  "Bank Alpha 1099-INT statement instance (synthetic)")},
                5,
            ),
            act(
                "member-transition",
                {
                    "family": FAMILY,
                    "scope": SCOPE,
                    "member": {
                        "action": "assert",
                        "finding": finding("b1.member.a", MEMBER_FACT, 120),
                    },
                    "successor": {"id": "b1.h1", "predecessor": "b1.h0"},
                },
                6,
            ),
            act(
                "assertion",
                {"finding": finding("b1.member.a.corrected", MEMBER_FACT, 125)},
                7,
            ),
            act(
                "member-transition",
                {
                    "family": FAMILY,
                    "scope": SCOPE,
                    "member": {"action": "remove", "fact_id": MEMBER_FACT},
                    "successor": {"id": "b1.h2", "predecessor": "b1.h1"},
                },
                8,
            ),
            act(
                "assertion",
                {"finding": finding("b1.closure.h2", CLOSURE_FACT_H2, True)},
                9,
            ),
        ]
        rerun_act = self.derive_zero(acts, "tax.us.2025.run.b1-zero-2")
        successor_zero = rerun_act["payload"]["finding"]["id"]
        acts.append(rerun_act)
        return acts, first_zero, successor_zero

    def currencies(self, acts: list[dict[str, Any]]) -> tuple[Any, Any, Any]:
        state = findings.project(tuple(acts), self.registry)
        kernel_view = compute_currency(state)
        derived = derived_findings_from_acts(tuple(acts))
        return state, kernel_view, compute_derivation_currency(kernel_view, derived)

    def coverage(self, acts: list[dict[str, Any]]) -> dict[str, Any]:
        state, kernel_view, _ = self.currencies(acts)
        report = coverage_report(state, kernel_view, self.families, self.mappings)
        return {entry.family_id: entry for entry in report}


class ClosureBackedZero(LifecycleFixture):
    def test_zero_publishes_and_pins_the_full_authority_chain(self) -> None:
        acts = self.opening_acts()
        zero_act = self.derive_zero(acts, "tax.us.2025.run.b1-zero-1")
        pins = {(p["role"], p["id"]) for p in zero_act["payload"]["finding"]["pins"]}
        self.assertIn(("input", "b1.closure.h0"), pins)
        self.assertIn(("package", "tax.us.2025.closure-mapping.f1099int-b1"), pins)
        self.assertIn(("package", FAMILY_ID), pins)
        self.assertIn(("adoption", "tax.us.2025.package.interest-slice"), pins)
        # The horizon identity travels in the pinned closure finding's
        # fact key; the run identity in the publication payload.
        self.assertIn("family-horizon=b1.h0", CLOSURE_FACT_H0)
        self.assertEqual(zero_act["payload"]["run_id"], "tax.us.2025.run.b1-zero-1")

    def test_coverage_reports_the_exact_claim_closed(self) -> None:
        acts = self.opening_acts()
        entry = self.coverage(acts)[FAMILY_ID]
        self.assertEqual(entry.status, CLOSED)
        self.assertEqual(entry.current_horizon, "b1.h0")
        self.assertEqual(entry.closure_finding_id, "b1.closure.h0")
        self.assertEqual(entry.exact_claim, self.families[FAMILY_ID]["closure_claim"])
        self.assertIn("box 1 only", entry.exact_claim)
        self.assertNotIn("all taxable interest", entry.exact_claim.lower())


class LateMemberFreshness(LifecycleFixture):
    def test_late_member_displaces_zero_and_reopens_coverage(self) -> None:
        acts, first_zero, _ = self.full_scenario()
        mid = acts[:7]  # through the member transition, before correction
        state, kernel_view, derivation_view = self.currencies(mid)
        self.assertIn("b1.closure.h0", kernel_view.displaced_finding_ids)
        self.assertIn(first_zero, derivation_view.displaced_derived_ids)
        self.assertEqual(derivation_view.current_derived_ids, frozenset())
        self.assertEqual(
            horizons.current_horizon_id(state.horizon_state, FAMILY, SCOPE), "b1.h1"
        )
        self.assertEqual(self.coverage(mid)[FAMILY_ID].status, OPEN)

    def test_same_member_correction_does_not_advance_the_horizon(self) -> None:
        acts, _, _ = self.full_scenario()
        state, kernel_view, _ = self.currencies(acts[:8])  # through correction
        self.assertEqual(
            horizons.current_horizon_id(state.horizon_state, FAMILY, SCOPE), "b1.h1"
        )
        self.assertIn("b1.member.a", kernel_view.displaced_finding_ids)
        self.assertIn("b1.member.a.corrected", kernel_view.current_finding_ids)

    def test_removal_advances_again_but_resurrects_nothing(self) -> None:
        acts, first_zero, _ = self.full_scenario()
        through_removal = acts[:9]
        state, kernel_view, derivation_view = self.currencies(through_removal)
        self.assertEqual(
            horizons.current_horizon_id(state.horizon_state, FAMILY, SCOPE), "b1.h2"
        )
        self.assertIn(first_zero, derivation_view.displaced_derived_ids)
        self.assertIn("b1.closure.h0", kernel_view.displaced_finding_ids)
        self.assertEqual(self.coverage(through_removal)[FAMILY_ID].status, OPEN)

    def test_reattestation_plus_explicit_rerun_publishes_the_successor(self) -> None:
        acts, first_zero, successor_zero = self.full_scenario()
        _, _, derivation_view = self.currencies(acts)
        self.assertNotEqual(first_zero, successor_zero)
        self.assertEqual(
            derivation_view.current_derived_ids, frozenset({successor_zero})
        )
        self.assertIn(first_zero, derivation_view.displaced_derived_ids)
        self.assertEqual(self.coverage(acts)[FAMILY_ID].status, CLOSED)
        self.assertEqual(self.coverage(acts)[FAMILY_ID].current_horizon, "b1.h2")


class LifecycleIntegrity(LifecycleFixture):
    def test_incremental_and_full_rebuild_agree_after_every_act(self) -> None:
        acts, _, _ = self.full_scenario()
        incremental = findings.initial_state()
        for index, one_act in enumerate(acts):
            incremental = findings.apply_act(incremental, one_act, self.registry)
            self.assertEqual(
                incremental, findings.project(tuple(acts[: index + 1]), self.registry)
            )

    def test_malformed_transition_rejects_atomically_on_real_content(self) -> None:
        acts, _, _ = self.full_scenario()
        state = findings.project(tuple(acts), self.registry)
        malformed = act(
            "member-transition",
            {
                "family": FAMILY,
                "scope": SCOPE,
                "member": {"action": "remove", "fact_id": MEMBER_FACT},
                "successor": {"id": "b1.h3", "predecessor": "b1.h0"},
            },
            len(acts),
        )
        with self.assertRaisesRegex(HorizonModelError, "wrong predecessor"):
            findings.apply_act(state, malformed, self.registry)
        self.assertEqual(state, findings.project(tuple(acts), self.registry))

    def test_family_isolation_under_b1_transitions(self) -> None:
        acts, _, _ = self.full_scenario()
        other = {"id": "tax.us.2025.family.w2-box1", "version": "v1"}
        acts = acts[:3] + [
            act(
                "horizon-genesis",
                {"family": other, "scope": SCOPE, "horizon_id": "w2.h0"},
                3,
            ),
        ] + [
            {**one, "act_id": f"iso-{i}", "committed_against": 4 + i}
            for i, one in enumerate(acts[3:])
        ]
        state = findings.project(tuple(acts), self.registry)
        self.assertEqual(
            horizons.current_horizon_id(state.horizon_state, other, SCOPE), "w2.h0"
        )
        self.assertEqual(
            horizons.current_horizon_id(state.horizon_state, FAMILY, SCOPE), "b1.h2"
        )


class ScenarioGoldens(unittest.TestCase):
    """The closed-empty zero and open-empty block as pinned CLI reports."""

    NAMES = ("closure_backed_zero_1099int", "open_empty_1099int")

    def test_reports_match_the_committed_goldens(self) -> None:
        from pathlib import Path

        from packages.derivation.runners.derive import build_report

        for name in self.NAMES:
            with self.subTest(scenario=name):
                root = Path("packages/sample_data/tax/scenarios") / name
                scenario = json.loads((root / "scenario.json").read_text("utf-8"))
                expected = json.loads(
                    (root / "expected" / "report.json").read_text("utf-8")
                )
                self.assertEqual(build_report(scenario), expected)

    def test_the_two_empty_dispositions_are_distinct(self) -> None:
        from pathlib import Path

        from packages.derivation.runners.derive import build_report

        scenarios = Path("packages/sample_data/tax/scenarios")
        closed = build_report(json.loads(
            (scenarios / self.NAMES[0] / "scenario.json").read_text("utf-8")))
        opened = build_report(json.loads(
            (scenarios / self.NAMES[1] / "scenario.json").read_text("utf-8")))
        self.assertEqual(closed["published"][0]["value"], "0")
        self.assertEqual(closed["blocked"], [])
        self.assertEqual(opened["published"], [])
        self.assertEqual(opened["blocked"][0]["code"], "SOURCE_SET_UNCLOSED")
        # The closure-backed zero explains through the closure finding;
        # the block names the exact family left unclosed.
        explanation = json.dumps(closed["explanations"])
        self.assertIn("demo-finding-b1-closure-h0", explanation)
        self.assertIn(FAMILY_ID, opened["blocked"][0]["missing"])


if __name__ == "__main__":
    unittest.main()
