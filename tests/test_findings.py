"""Finding model tests: evidence lifecycle and asserted findings."""

import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.kernel.findings import (
    FindingModelError,
    apply_act,
    evidentiary_standing,
    initial_state,
    project,
)
from packages.kernel.schema_registry import SchemaValidationError
from tests.support import (
    act,
    demo_bundle,
    demo_entity,
    demo_evidence,
    demo_finding,
    demo_payment_fact_id,
    registry_with_demo_kinds,
)


class FindingsFixture(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.registry = registry_with_demo_kinds(Path(self._tmp.name))

    def base_acts(self) -> tuple[dict[str, Any], ...]:
        return (
            act(0, "bundle-adoption", {"bundle": demo_bundle()}),
            act(1, "entity-introduced", {"entity": demo_entity("demo-corp-a", "Corp A")}),
            act(2, "evidence-submitted", {"evidence": demo_evidence()}),
        )


class TestEvidenceLifecycle(FindingsFixture):
    def test_evidence_submission_adds_current_evidence(self) -> None:
        state = project(
            (act(0, "evidence-submitted", {"evidence": demo_evidence()}),),
            self.registry,
        )
        self.assertEqual(state.evidence["demo-evidence-001"].status, "current")

    def test_replacement_marks_old_evidence_and_adds_successor(self) -> None:
        state = project(
            (
                act(0, "evidence-submitted", {"evidence": demo_evidence()}),
                act(
                    1,
                    "evidence-replaced",
                    {
                        "evidence_id": "demo-evidence-001",
                        "replacement": demo_evidence(
                            "demo-evidence-002", "Corrected demo statement"
                        ),
                    },
                ),
            ),
            self.registry,
        )
        self.assertEqual(state.evidence["demo-evidence-001"].status, "replaced")
        self.assertEqual(
            state.evidence["demo-evidence-001"].successor_id,
            "demo-evidence-002",
        )
        self.assertEqual(state.evidence["demo-evidence-002"].status, "current")

    def test_withdrawal_marks_evidence_without_successor(self) -> None:
        state = project(
            (
                act(0, "evidence-submitted", {"evidence": demo_evidence()}),
                act(1, "evidence-replaced", {"evidence_id": "demo-evidence-001"}),
            ),
            self.registry,
        )
        self.assertEqual(state.evidence["demo-evidence-001"].status, "withdrawn")
        self.assertIsNone(state.evidence["demo-evidence-001"].successor_id)


class TestAssertionFindings(FindingsFixture):
    def test_assertion_creates_immutable_finding(self) -> None:
        finding = demo_finding(value=1200)
        state = project(
            self.base_acts()
            + (act(3, "assertion", {"finding": finding}),),
            self.registry,
        )
        self.assertEqual(state.findings["demo-finding-001"], finding)
        standing = evidentiary_standing(state)["demo-finding-001"]
        self.assertEqual(standing.finding, finding)
        self.assertEqual(standing.evidence[0].status, "current")

    def test_asserted_value_must_match_fact_type_value_schema(self) -> None:
        finding = demo_finding(value="not a number")
        with self.assertRaises(FindingModelError) as ctx:
            project(
                self.base_acts()
                + (act(3, "assertion", {"finding": finding}),),
                self.registry,
            )
        self.assertIn("does not conform", str(ctx.exception))

    def test_assertion_rejects_unknown_fact(self) -> None:
        finding = demo_finding(fact_id="demo.unknown|period=2025")
        with self.assertRaises(FindingModelError):
            project(
                self.base_acts()
                + (act(3, "assertion", {"finding": finding}),),
                self.registry,
            )

    def test_documentary_assertion_requires_current_evidence(self) -> None:
        finding = demo_finding(evidence_ids=["missing-evidence"])
        with self.assertRaises(FindingModelError) as ctx:
            project(
                self.base_acts()
                + (act(3, "assertion", {"finding": finding}),),
                self.registry,
            )
        self.assertIn("non-current evidence", str(ctx.exception))

    def test_documentary_assertion_requires_some_evidence(self) -> None:
        finding = demo_finding(evidence_ids=[])
        with self.assertRaises(FindingModelError) as ctx:
            project(
                self.base_acts()
                + (act(3, "assertion", {"finding": finding}),),
                self.registry,
            )
        self.assertIn("names no evidence", str(ctx.exception))

    def test_elective_fact_requires_elective_basis(self) -> None:
        # A report cannot close an election: the choice constitutes the
        # answer (Article 3).
        finding = demo_finding(
            finding_id="demo-finding-choice",
            fact_id="demo.rate-choice|period=2025",
            value="standard",
            evidence_ids=[],
            basis="attested",
        )
        with self.assertRaises(FindingModelError) as ctx:
            project(
                self.base_acts() + (act(3, "assertion", {"finding": finding}),),
                self.registry,
            )
        self.assertIn("constituted by choice", str(ctx.exception))

    def test_elective_basis_cannot_close_a_determinable_fact(self) -> None:
        finding = demo_finding(
            finding_id="demo-finding-fiat",
            value=1200,
            evidence_ids=[],
            basis="elective",
        )
        with self.assertRaises(FindingModelError) as ctx:
            project(
                self.base_acts() + (act(3, "assertion", {"finding": finding}),),
                self.registry,
            )
        self.assertIn("determinable", str(ctx.exception))

    def test_elective_assertion_closes_elective_fact(self) -> None:
        finding = demo_finding(
            finding_id="demo-finding-choice",
            fact_id="demo.rate-choice|period=2025",
            value="standard",
            evidence_ids=[],
            basis="elective",
        )
        state = project(
            self.base_acts() + (act(3, "assertion", {"finding": finding}),),
            self.registry,
        )
        self.assertIn("demo-finding-choice", state.findings)

    def test_supersession_policy_is_consulted_on_correction(self) -> None:
        # Plant a policy the published schema does not offer directly in
        # the projection: correction must be refused, proving the
        # declaration is read rather than decorative.
        import dataclasses
        import json as jsonlib

        state = project(
            self.base_acts()
            + (act(3, "assertion", {"finding": demo_finding("first")}),),
            self.registry,
        )
        locked = jsonlib.loads(
            jsonlib.dumps(state.fact_state.fact_types["demo.counterparty-payment"])
        )
        locked["supersession"]["policy"] = "locked"
        state = dataclasses.replace(
            state,
            fact_state=dataclasses.replace(
                state.fact_state,
                fact_types={
                    **state.fact_state.fact_types,
                    "demo.counterparty-payment": locked,
                },
            ),
        )
        with self.assertRaises(FindingModelError) as ctx:
            apply_act(
                state,
                act(4, "assertion", {"finding": demo_finding("second", value=1300)}),
                self.registry,
            )
        self.assertIn("supersession policy", str(ctx.exception))

    def test_attested_assertion_can_stand_without_evidence(self) -> None:
        finding = demo_finding(
            finding_id="demo-finding-attested",
            fact_id=demo_payment_fact_id(),
            value=42,
            evidence_ids=[],
            basis="attested",
        )
        state = project(
            self.base_acts()
            + (act(3, "assertion", {"finding": finding}),),
            self.registry,
        )
        self.assertEqual(state.findings["demo-finding-attested"], finding)

    def test_duplicate_finding_id_is_rejected(self) -> None:
        finding = demo_finding()
        state = project(
            self.base_acts()
            + (act(3, "assertion", {"finding": finding}),),
            self.registry,
        )
        with self.assertRaises(FindingModelError):
            apply_act(
                state,
                act(4, "assertion", {"finding": finding}),
                self.registry,
            )

    def test_malformed_evidence_is_rejected_not_repaired(self) -> None:
        evidence = demo_evidence()
        del evidence["content"]
        with self.assertRaises(SchemaValidationError):
            project(
                (act(0, "evidence-submitted", {"evidence": evidence}),),
                self.registry,
            )

    def test_malformed_finding_is_rejected_not_repaired(self) -> None:
        finding = demo_finding()
        del finding["basis"]
        with self.assertRaises(SchemaValidationError):
            project(
                self.base_acts()
                + (act(3, "assertion", {"finding": finding}),),
                self.registry,
            )

    def test_assertion_rejects_derived_pins_until_derivation_milestone(self) -> None:
        finding = demo_finding()
        finding["pins"] = {"finding_ids": ["old-finding"], "artifact_ids": ["rule.v1"]}
        with self.assertRaises(FindingModelError) as ctx:
            project(
                self.base_acts()
                + (act(3, "assertion", {"finding": finding}),),
                self.registry,
            )
        self.assertIn("not admitted", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
