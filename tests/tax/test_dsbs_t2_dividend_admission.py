"""Track 2 deliverables 1-2: the 1099-DIV 1b <= 1a admission-time subset
invariant (ADR-0035 decision 4) and its same-batch ordering kill-test
(ADR-0035 adversary-minor production condition).

These are kernel/admission-level tests, not coordinator goldens: the
charter (docs/reviews/charter-2026-07-19-dsbs-t2-composition-conditional-
machinery.md, Verification item 6) names them as tests that "may be
runner/admission-level ... where the defect is not fact-log-observable,
but must be executed, not asserted by comment." The mechanism itself
(``registry.subset_invariant_pairs``, enforced generically in
``packages.kernel.findings``) is exercised through ordinary
``project()``/``apply_contribution_batch`` calls against the real
committed ``tax.us.2025.f1099div.*`` fact types and families - the same
admission surface the live coordinator's ``project()`` call uses.
"""

from __future__ import annotations

import json
import unittest
from typing import Any

from packages.kernel.contribution import ContributionError, apply_contribution_batch
from packages.kernel.findings import FindingModelError, project
from packages.tax.loader import TAX_CONTENT_DIR, tax_registry

BOX1A = "tax.us.2025.f1099div.box1a-ordinary"
BOX1B = "tax.us.2025.f1099div.box1b-qualified"
FAMILY_1A = {"id": "tax.us.2025.f1099div.1a", "version": "v1"}
FAMILY_1B = {"id": "tax.us.2025.f1099div.1b", "version": "v1"}
SCOPE = {"tax-year": "2025"}
PAYER = "demo.dsbs.t2.payer.alpha"
STATEMENT = "demo.dsbs.t2.stmt.alpha-1"


def _act(index: int, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.dsbs.t2.act.{index:03d}",
        "kind": kind,
        "actor": "demo.dsbs.t2.user",
        "at": f"2026-07-19T00:00:{index:02d}Z",
        "committed_against": index,
        "payload": payload,
    }


def _fact_id(fact_type: str) -> str:
    return f"{fact_type}|payer={PAYER},statement={STATEMENT},tax-year=2025"


def _finding(finding_id: str, fact_type: str, value: Any, **extra: Any) -> dict[str, Any]:
    finding: dict[str, Any] = {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": _fact_id(fact_type),
        "value": value,
        "basis": "attested",
        "evidence_ids": [],
    }
    finding.update(extra)
    return finding


def _member_act(
    index: int, family: dict[str, str], predecessor: str, successor: str, finding: dict[str, Any]
) -> dict[str, Any]:
    return _act(
        index,
        "member-transition",
        {
            "family": family,
            "scope": SCOPE,
            "member": {"action": "assert", "finding": finding},
            "successor": {"id": successor, "predecessor": predecessor},
        },
    )


class DividendAdmissionFixture(unittest.TestCase):
    """Base acts: the committed bundle, one payer/statement pair, both
    per-box horizon chains at genesis. Every test extends this tuple."""

    def setUp(self) -> None:
        self.registry = tax_registry()
        bundle = json.loads((TAX_CONTENT_DIR / "f1099div.bundle.json").read_text("utf-8"))
        self.base: tuple[dict[str, Any], ...] = (
            _act(0, "bundle-adoption", {"bundle": bundle}),
            _act(
                1,
                "entity-introduced",
                {"entity": {"schema": "entity.v1", "id": PAYER, "kind": "tax.us.dividend-payer", "label": "Demo payer"}},
            ),
            _act(
                2,
                "entity-introduced",
                {"entity": {"schema": "entity.v1", "id": STATEMENT, "kind": "tax.us.1099div-statement", "label": "Demo statement"}},
            ),
            _act(3, "horizon-genesis", {"family": FAMILY_1A, "scope": SCOPE, "horizon_id": "demo.h1a.0"}),
            _act(4, "horizon-genesis", {"family": FAMILY_1B, "scope": SCOPE, "horizon_id": "demo.h1b.0"}),
        )
        # sanity: the base acts alone admit cleanly.
        project(self.base, self.registry)


class SubsetInvariantAdmission(DividendAdmissionFixture):
    def test_qualified_present_ordinary_absent_rejects(self) -> None:
        act1b = _member_act(5, FAMILY_1B, "demo.h1b.0", "demo.h1b.1", _finding("f.1b.1", BOX1B, 40))
        with self.assertRaises(FindingModelError):
            project((*self.base, act1b), self.registry)

    def test_qualified_greater_than_ordinary_rejects(self) -> None:
        act1a = _member_act(5, FAMILY_1A, "demo.h1a.0", "demo.h1a.1", _finding("f.1a.1", BOX1A, 100))
        act1b = _member_act(6, FAMILY_1B, "demo.h1b.0", "demo.h1b.1", _finding("f.1b.1", BOX1B, 150))
        with self.assertRaises(FindingModelError):
            project((*self.base, act1a, act1b), self.registry)

    def test_qualified_less_than_or_equal_ordinary_admits(self) -> None:
        act1a = _member_act(5, FAMILY_1A, "demo.h1a.0", "demo.h1a.1", _finding("f.1a.1", BOX1A, 100))
        act1b = _member_act(6, FAMILY_1B, "demo.h1b.0", "demo.h1b.1", _finding("f.1b.1", BOX1B, 100))
        state = project((*self.base, act1a, act1b), self.registry)
        self.assertIn("f.1a.1", state.findings)
        self.assertIn("f.1b.1", state.findings)

    def test_correction_of_ordinary_rechecks_current_qualified(self) -> None:
        act1a = _member_act(5, FAMILY_1A, "demo.h1a.0", "demo.h1a.1", _finding("f.1a.1", BOX1A, 100))
        act1b = _member_act(6, FAMILY_1B, "demo.h1b.0", "demo.h1b.1", _finding("f.1b.1", BOX1B, 80))
        good = (*self.base, act1a, act1b)
        # A same-member correction goes through a plain assertion (SC-R1/R2):
        # the fact is already a current family member.
        correction = _act(7, "assertion", {"finding": _finding("f.1a.2", BOX1A, 50)})
        with self.assertRaises(FindingModelError):
            project((*good, correction), self.registry)
        # And the opposite direction admits cleanly: correcting ordinary
        # upward never violates the pair.
        widen = _act(7, "assertion", {"finding": _finding("f.1a.2", BOX1A, 200)})
        state = project((*good, widen), self.registry)
        self.assertIn("f.1a.2", state.findings)

    def test_removing_ordinary_while_qualified_remains_current_rejects(self) -> None:
        act1a = _member_act(5, FAMILY_1A, "demo.h1a.0", "demo.h1a.1", _finding("f.1a.1", BOX1A, 100))
        act1b = _member_act(6, FAMILY_1B, "demo.h1b.0", "demo.h1b.1", _finding("f.1b.1", BOX1B, 80))
        good = (*self.base, act1a, act1b)
        removal = _act(
            7,
            "member-transition",
            {
                "family": FAMILY_1A,
                "scope": SCOPE,
                "member": {"action": "remove", "fact_id": _fact_id(BOX1A)},
                "successor": {"id": "demo.h1a.2", "predecessor": "demo.h1a.1"},
            },
        )
        with self.assertRaises(FindingModelError):
            project((*good, removal), self.registry)

    def test_violating_pair_is_never_recorded(self) -> None:
        act1a = _member_act(5, FAMILY_1A, "demo.h1a.0", "demo.h1a.1", _finding("f.1a.1", BOX1A, 100))
        act1b = _member_act(6, FAMILY_1B, "demo.h1b.0", "demo.h1b.1", _finding("f.1b.1", BOX1B, 150))
        with self.assertRaises(FindingModelError):
            project((*self.base, act1a, act1b), self.registry)
        # The rejecting run's rejection is a raise, never a partial state a
        # caller could observe: a fresh run admitting only the ordinary act
        # never carries the rejected qualified finding forward.
        clean = project((*self.base, act1a), self.registry)
        self.assertNotIn("f.1b.1", clean.findings)


class SameBatchOrdering(DividendAdmissionFixture):
    """ADR-0035 adversary-minor: the paired check cannot be sequenced
    around when both boxes' findings for one statement arrive in the same
    contribution batch (ADR-0032 terminal contribution-batch failure)."""

    def _batch_state(self) -> Any:
        evidence_act = _act(
            5,
            "evidence-submitted",
            {
                "evidence": {
                    "schema": "evidence.v1",
                    "id": "demo.dsbs.t2.evidence",
                    "kind": "demo.statement",
                    "label": "Demo 1099-DIV",
                    "content": {"synthetic": True},
                }
            },
        )
        return project((*self.base, evidence_act), self.registry)

    def test_batch_admitting_qualified_before_ordinary_still_fails_closed(self) -> None:
        """Order box1b before box1a in one batch; the pair still violates
        (1b=150 > 1a=100). A stale-view check that only consulted state
        from before the batch (or only checked on box1a's own admission)
        could let this pass; the actual check must catch it regardless of
        which finding in the pair is admitted first."""
        state = self._batch_state()
        contribution_id = "demo.dsbs.t2.contribution"
        contribution_act = _act(
            6,
            "contribution",
            {
                "contribution": {
                    "schema": "contribution.v1",
                    "id": contribution_id,
                    "evidence_id": "demo.dsbs.t2.evidence",
                    "content": {"mode": "manual-entry", "synthetic": True},
                }
            },
        )
        act1b = _member_act(
            7, FAMILY_1B, "demo.h1b.0", "demo.h1b.1",
            _finding("f.1b.1", BOX1B, 150, contribution_id=contribution_id, evidence_ids=["demo.dsbs.t2.evidence"]),
        )
        act1a = _member_act(
            8, FAMILY_1A, "demo.h1a.0", "demo.h1a.1",
            _finding("f.1a.1", BOX1A, 100, contribution_id=contribution_id, evidence_ids=["demo.dsbs.t2.evidence"]),
        )
        with self.assertRaisesRegex(ContributionError, "subset invariant"):
            apply_contribution_batch(
                state,
                contribution_act=contribution_act,
                successor_acts=[act1b, act1a],
                registry=self.registry,
                record_id="demo.dsbs.t2.record",
            )

    def test_batch_admitting_dominant_before_subordinate_admits_a_conforming_pair(self) -> None:
        """The dominant-first order (1a then 1b) with a conforming pair
        (1b=80 <= 1a=100) completes in one batch - the check is not a
        blanket same-batch rejection, only a rejection of the invariant."""
        state = self._batch_state()
        contribution_id = "demo.dsbs.t2.contribution"
        contribution_act = _act(
            6,
            "contribution",
            {
                "contribution": {
                    "schema": "contribution.v1",
                    "id": contribution_id,
                    "evidence_id": "demo.dsbs.t2.evidence",
                    "content": {"mode": "manual-entry", "synthetic": True},
                }
            },
        )
        act1a = _member_act(
            7, FAMILY_1A, "demo.h1a.0", "demo.h1a.1",
            _finding("f.1a.1", BOX1A, 100, contribution_id=contribution_id, evidence_ids=["demo.dsbs.t2.evidence"]),
        )
        act1b = _member_act(
            8, FAMILY_1B, "demo.h1b.0", "demo.h1b.1",
            _finding("f.1b.1", BOX1B, 80, contribution_id=contribution_id, evidence_ids=["demo.dsbs.t2.evidence"]),
        )
        result = apply_contribution_batch(
            state,
            contribution_act=contribution_act,
            successor_acts=[act1a, act1b],
            registry=self.registry,
            record_id="demo.dsbs.t2.record",
        )
        self.assertEqual(result.terminal_record["phase"], "completed")
        self.assertIn("f.1a.1", result.state.findings)
        self.assertIn("f.1b.1", result.state.findings)

    def test_subordinate_first_order_fails_closed_even_when_conforming(self) -> None:
        """The subordinate (1b) cannot be admitted ahead of the dominant
        (1a) it depends on within one batch, even when the eventual pair
        would conform: presence is checked at each admission against the
        state folded so far, never against a value the batch has not
        reached yet. This is the same fail-closed posture as the kill-test
        above, documented so it is not mistaken for a defect."""
        state = self._batch_state()
        contribution_id = "demo.dsbs.t2.contribution"
        contribution_act = _act(
            6,
            "contribution",
            {
                "contribution": {
                    "schema": "contribution.v1",
                    "id": contribution_id,
                    "evidence_id": "demo.dsbs.t2.evidence",
                    "content": {"mode": "manual-entry", "synthetic": True},
                }
            },
        )
        act1b = _member_act(
            7, FAMILY_1B, "demo.h1b.0", "demo.h1b.1",
            _finding("f.1b.1", BOX1B, 80, contribution_id=contribution_id, evidence_ids=["demo.dsbs.t2.evidence"]),
        )
        act1a = _member_act(
            8, FAMILY_1A, "demo.h1a.0", "demo.h1a.1",
            _finding("f.1a.1", BOX1A, 100, contribution_id=contribution_id, evidence_ids=["demo.dsbs.t2.evidence"]),
        )
        with self.assertRaisesRegex(ContributionError, "subset invariant"):
            apply_contribution_batch(
                state,
                contribution_act=contribution_act,
                successor_acts=[act1b, act1a],
                registry=self.registry,
                record_id="demo.dsbs.t2.record",
            )


if __name__ == "__main__":
    unittest.main()
