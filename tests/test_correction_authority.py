"""Correction-authority policy regression goldens (ADR-0041 Track 1).

Proves the enforcement side of ADR-0041's closed supersession-policy
vocabulary: ``free`` (unchanged default), ``locked`` (correction forbidden
unconditionally once any finding exists), and ``closed-on-attestation``
(correction forbidden only while a named gate closure fact is currently
attested ``true``; reopened by ADR-0017 horizon succession exactly as
closure-backed derived results already reopen - no new mechanism).

All fact/entity content here is synthetic test-only vocabulary (mirrors
``tests/support.py`` and ``tests/source_completeness/test_track2_horizon_projection.py``'s
demo-fixture convention); it never touches production tax content, per
ADR-0041's own note that no existing fact type needs to change.
"""

import unittest
from typing import Any

from packages.kernel import facts, findings
from packages.kernel.findings import FindingModelError
from packages.kernel.schema_registry import SchemaRegistry

# --- Family A: a single-shot "locked" fact, no horizon involved. -----------

LOCKED_FACT_TYPE: dict[str, Any] = {
    "schema": "fact-type.v3",
    "id": "ca.single-shot-declaration",
    "title": "A one-time declaration for a filer that must never be corrected",
    "nature": "elective",
    "identity_keys": [
        {"name": "filer", "kind": "entity", "entity_kind": "ca.filer"},
        {"name": "year", "kind": "literal", "values": ["2025"]},
    ],
    "value_schema": {"enum": ["method-a", "method-b"]},
    "supersession": {"policy": "locked"},
}

# --- Family B: a family-horizon-keyed election gated by a closure fact. ----

FAMILY = {"id": "ca.family.election", "version": "v1"}
SCOPE = {"subject": "s1"}

CLOSURE_FACT_TYPE: dict[str, Any] = {
    "schema": "fact-type.v1",
    "id": "ca.family.closure",
    "title": "Demo family closure gating the election below",
    "nature": "determinable",
    "identity_keys": [
        {"name": "family-horizon", "kind": "entity", "entity_kind": "kernel.family-horizon"},
        {"name": "year", "kind": "literal", "values": ["2025"]},
    ],
    "value_schema": {"type": "boolean"},
    "supersession": {"policy": "free"},
}

MEMBER_FACT_TYPE: dict[str, Any] = {
    "schema": "fact-type.v1",
    "id": "ca.family.member",
    "title": "Demo family member amount, used only to drive horizon succession",
    "nature": "determinable",
    "identity_keys": [
        {"name": "slip", "kind": "entity", "entity_kind": "ca.slip"},
        {"name": "year", "kind": "literal", "values": ["2025"]},
    ],
    "value_schema": {"type": "number"},
    "supersession": {"policy": "free"},
}

GATED_FACT_TYPE: dict[str, Any] = {
    "schema": "fact-type.v3",
    "id": "ca.family.election-rate",
    "title": "Family-level rate election, free to revise until the family closes",
    "nature": "elective",
    "identity_keys": [
        {"name": "family-horizon", "kind": "entity", "entity_kind": "kernel.family-horizon"},
        {"name": "year", "kind": "literal", "values": ["2025"]},
    ],
    "value_schema": {"enum": ["standard", "reduced"]},
    "supersession": {
        "policy": "closed-on-attestation",
        "gate": {"fact_type": "ca.family.closure"},
    },
}


def gated_fact_id(horizon_id: str) -> str:
    return f"ca.family.election-rate|family-horizon={horizon_id},year=2025"


def closure_fact_id(horizon_id: str) -> str:
    return f"ca.family.closure|family-horizon={horizon_id},year=2025"


def act(kind: str, payload: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": f"ca-act-{index:03d}",
        "kind": kind,
        "actor": "user",
        "at": f"2026-07-22T01:{index:02d}:00Z",
        "committed_against": index,
        "payload": payload,
    }


def finding(finding_id: str, fact_id: str, value: Any, basis: str = "elective") -> dict[str, Any]:
    return {
        "schema": "finding.v1",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": basis,
        "evidence_ids": [],
    }


def closure_finding(finding_id: str, fact_id: str, value: bool) -> dict[str, Any]:
    return {
        "schema": "finding.v1",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "attested",
        "evidence_ids": [],
    }


class CorrectionAuthorityFixture(unittest.TestCase):
    registry: SchemaRegistry

    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = SchemaRegistry()

    def project(self, acts: list[dict[str, Any]]) -> findings.FindingState:
        return findings.project(tuple(acts), self.registry)


class LockedPolicy(CorrectionAuthorityFixture):
    """(a) unauthorized correction under ``locked`` is rejected."""

    def base_acts(self) -> list[dict[str, Any]]:
        return [
            act(
                "bundle-adoption",
                {
                    "bundle": {
                        "schema": "bundle.v3",
                        "id": "ca.locked.vocabulary",
                        "label": "Correction-authority locked-policy demo vocabulary",
                        "fact_types": [LOCKED_FACT_TYPE],
                    }
                },
                0,
            ),
            act(
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": "ca.filer-1",
                        "kind": "ca.filer",
                        "label": "Demo filer 1",
                    }
                },
                1,
            ),
        ]

    def test_first_answer_is_accepted(self) -> None:
        fact_id = "ca.single-shot-declaration|filer=ca.filer-1,year=2025"
        state = self.project(
            self.base_acts()
            + [
                act(
                    "assertion",
                    {"finding": finding("ca.decl.1", fact_id, "method-a")},
                    2,
                )
            ]
        )
        self.assertEqual(state.findings["ca.decl.1"]["value"], "method-a")

    def test_second_answer_is_rejected_unconditionally(self) -> None:
        fact_id = "ca.single-shot-declaration|filer=ca.filer-1,year=2025"
        state = self.project(
            self.base_acts()
            + [act("assertion", {"finding": finding("ca.decl.1", fact_id, "method-a")}, 2)]
        )
        with self.assertRaises(FindingModelError) as ctx:
            findings.apply_act(
                state,
                act("assertion", {"finding": finding("ca.decl.2", fact_id, "method-b")}, 3),
                self.registry,
            )
        self.assertIn("supersession policy 'locked'", str(ctx.exception))


class ClosedOnAttestationPolicy(CorrectionAuthorityFixture):
    """(b), (c), (d): the gated ``closed-on-attestation`` election."""

    def genesis_acts(self) -> list[dict[str, Any]]:
        return [
            act(
                "bundle-adoption",
                {
                    "bundle": {
                        "schema": "bundle.v3",
                        "id": "ca.gated.vocabulary",
                        "label": "Correction-authority closed-on-attestation demo vocabulary",
                        "fact_types": [CLOSURE_FACT_TYPE, GATED_FACT_TYPE, MEMBER_FACT_TYPE],
                    }
                },
                0,
            ),
            act(
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": "ca.slip-1",
                        "kind": "ca.slip",
                        "label": "Demo slip 1",
                    }
                },
                1,
            ),
            act(
                "horizon-genesis",
                {"family": FAMILY, "scope": SCOPE, "horizon_id": "ca.h0"},
                2,
            ),
        ]

    def test_correction_permitted_when_gate_absent(self) -> None:
        # (c) no closure attestation at all: correction permitted.
        state = self.project(
            self.genesis_acts()
            + [
                act(
                    "assertion",
                    {"finding": finding("ca.rate.1", gated_fact_id("ca.h0"), "standard")},
                    3,
                )
            ]
        )
        state = findings.apply_act(
            state,
            act(
                "assertion",
                {"finding": finding("ca.rate.2", gated_fact_id("ca.h0"), "reduced")},
                4,
            ),
            self.registry,
        )
        self.assertEqual(state.findings["ca.rate.2"]["value"], "reduced")

    def test_correction_permitted_when_gate_explicitly_false(self) -> None:
        # (c) closure attested false: correction permitted.
        state = self.project(
            self.genesis_acts()
            + [
                act(
                    "assertion",
                    {"finding": finding("ca.rate.1", gated_fact_id("ca.h0"), "standard")},
                    3,
                ),
                act(
                    "assertion",
                    {
                        "finding": closure_finding(
                            "ca.closure.h0", closure_fact_id("ca.h0"), False
                        )
                    },
                    4,
                ),
            ]
        )
        state = findings.apply_act(
            state,
            act(
                "assertion",
                {"finding": finding("ca.rate.2", gated_fact_id("ca.h0"), "reduced")},
                5,
            ),
            self.registry,
        )
        self.assertEqual(state.findings["ca.rate.2"]["value"], "reduced")

    def test_correction_rejected_once_gate_is_true(self) -> None:
        # (b) closure attested true: correction rejected.
        state = self.project(
            self.genesis_acts()
            + [
                act(
                    "assertion",
                    {"finding": finding("ca.rate.1", gated_fact_id("ca.h0"), "standard")},
                    3,
                ),
                act(
                    "assertion",
                    {
                        "finding": closure_finding(
                            "ca.closure.h0", closure_fact_id("ca.h0"), True
                        )
                    },
                    4,
                ),
            ]
        )
        with self.assertRaises(FindingModelError) as ctx:
            findings.apply_act(
                state,
                act(
                    "assertion",
                    {"finding": finding("ca.rate.2", gated_fact_id("ca.h0"), "reduced")},
                    5,
                ),
                self.registry,
            )
        self.assertIn("closed-on-attestation", str(ctx.exception))
        self.assertIn(closure_fact_id("ca.h0"), str(ctx.exception))

    def test_horizon_succession_reopens_correction_on_successor_horizon(self) -> None:
        # (d) closed on h0; a membership transition to h1 (ADR-0017) does
        # not touch the h0 finding history, but the election's own fact id
        # is individuated on the family-horizon entity, so the successor
        # horizon names a distinct, freshly-unanswered fact - exactly the
        # reopening ADR-0017 decision 7 already requires for closure-backed
        # results, reused here rather than built anew.
        closed_acts = self.genesis_acts() + [
            act(
                "assertion",
                {"finding": finding("ca.rate.1", gated_fact_id("ca.h0"), "standard")},
                3,
            ),
            act(
                "assertion",
                {"finding": closure_finding("ca.closure.h0", closure_fact_id("ca.h0"), True)},
                4,
            ),
        ]
        state = self.project(closed_acts)
        # Confirm h0 is indeed closed before succession.
        with self.assertRaises(FindingModelError):
            findings.apply_act(
                state,
                act(
                    "assertion",
                    {"finding": finding("ca.rate.2", gated_fact_id("ca.h0"), "reduced")},
                    5,
                ),
                self.registry,
            )

        # An ordinary member-transition (ADR-0017) advances the horizon to
        # h1, the same mechanism tests/source_completeness/
        # test_track2_horizon_projection.py already proves in isolation;
        # this test only needs the successor horizon id it produces.
        state = findings.apply_act(
            state,
            act(
                "member-transition",
                {
                    "family": FAMILY,
                    "scope": SCOPE,
                    "member": {
                        "action": "assert",
                        "finding": finding(
                            "ca.member.1",
                            "ca.family.member|slip=ca.slip-1,year=2025",
                            100,
                            basis="attested",
                        ),
                    },
                    "successor": {"id": "ca.h1", "predecessor": "ca.h0"},
                },
                5,
            ),
            self.registry,
        )

        lattice = facts.facts_of(state.fact_state)
        self.assertIn(gated_fact_id("ca.h1"), lattice)
        self.assertNotIn(gated_fact_id("ca.h1"), {f["fact_id"] for f in state.findings.values()})

        # The successor horizon's election is a fresh, unanswered fact:
        # the first answer on h1 is unconditionally accepted...
        state = findings.apply_act(
            state,
            act(
                "assertion",
                {"finding": finding("ca.rate.h1.1", gated_fact_id("ca.h1"), "standard")},
                6,
            ),
            self.registry,
        )
        self.assertEqual(state.findings["ca.rate.h1.1"]["value"], "standard")

        # ...and, because h1's own closure has not been attested, a second
        # answer on h1 is a permitted correction (reopened, not locked).
        state = findings.apply_act(
            state,
            act(
                "assertion",
                {"finding": finding("ca.rate.h1.2", gated_fact_id("ca.h1"), "reduced")},
                7,
            ),
            self.registry,
        )
        self.assertEqual(state.findings["ca.rate.h1.2"]["value"], "reduced")


class FreePolicyUnchanged(CorrectionAuthorityFixture):
    """(e) ``free`` behavior is completely unchanged."""

    def test_free_fact_still_permits_unlimited_correction(self) -> None:
        free_fact_type: dict[str, Any] = {
            "schema": "fact-type.v1",
            "id": "ca.free-declaration",
            "title": "An ordinary free-policy fact, unaffected by ADR-0041",
            "nature": "determinable",
            "identity_keys": [
                {"name": "filer", "kind": "entity", "entity_kind": "ca.filer"},
                {"name": "year", "kind": "literal", "values": ["2025"]},
            ],
            "value_schema": {"type": "number"},
            "supersession": {"policy": "free"},
        }
        fact_id = "ca.free-declaration|filer=ca.filer-1,year=2025"
        acts = [
            act(
                "bundle-adoption",
                {
                    "bundle": {
                        "schema": "bundle.v1",
                        "id": "ca.free.vocabulary",
                        "label": "Correction-authority free-policy demo vocabulary",
                        "fact_types": [free_fact_type],
                    }
                },
                0,
            ),
            act(
                "entity-introduced",
                {
                    "entity": {
                        "schema": "entity.v1",
                        "id": "ca.filer-1",
                        "kind": "ca.filer",
                        "label": "Demo filer 1",
                    }
                },
                1,
            ),
            act("assertion", {"finding": finding("ca.free.1", fact_id, 100, basis="attested")}, 2),
        ]
        state = self.project(acts)
        for index, value in enumerate((200, 300, 400), start=3):
            state = findings.apply_act(
                state,
                act(
                    "assertion",
                    {"finding": finding(f"ca.free.{index}", fact_id, value, basis="attested")},
                    index,
                ),
                self.registry,
            )
        self.assertEqual(state.findings["ca.free.5"]["value"], 400)


if __name__ == "__main__":
    unittest.main()
