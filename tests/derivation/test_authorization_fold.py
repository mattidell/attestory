"""Standing-authorization fold: Gate-2 cases, supersession, compose-over."""

from __future__ import annotations

import copy
import unittest

from packages.derivation.authorization import (
    ENTITY_SUPERSEDED_KIND,
    STATUS_ABSENT,
    STATUS_ADMITTED,
    STATUS_STALE,
    STATUS_SUBJECT_SUPERSEDED,
    STATUS_SUSPENDED,
    STATUS_TAXPAYER_MISMATCH,
    STATUS_UNIVERSE_SUPERSEDED,
    STATUS_WITHDRAWN,
    STATUS_YEAR_MISMATCH,
    project,
    resolve,
    resolve_for_composition,
)
from packages.derivation.authorization_closure import package_boundary_digest
from tests.derivation.test_authorization_closure import ROOT, _corpus


def _grant(
    grant_id: str,
    subject_id: str,
    tax_year: str,
    universe_id: str,
    supersedes: str | None = None,
) -> dict[str, object]:
    citizen: dict[str, str] = {
        "schema": "workspace-calculation-authorization.v1",
        "id": grant_id,
        "subject_id": subject_id,
        "tax_year": tax_year,
        "universe_id": universe_id,
    }
    if supersedes is not None:
        citizen["supersedes"] = supersedes
    return {"kind": "calculation-authorization", "payload": {"authorization": citizen}}


def _end(grant_id: str, ending: str) -> dict[str, object]:
    return {
        "kind": "calculation-authorization-end",
        "payload": {"authorization_id": grant_id, "ending": ending},
    }


def _entity_superseded(entity_id: str, replacement_id: str | None) -> dict[str, object]:
    payload: dict[str, object] = {"entity_id": entity_id}
    if replacement_id is not None:
        payload["replacement"] = {
            "id": replacement_id,
            "schema": "entity.v1",
            "kind": "taxpayer",
            "label": "demo successor",
        }
    return {"kind": ENTITY_SUPERSEDED_KIND, "payload": payload}


def _member_transition() -> dict[str, object]:
    return {"kind": "member-transition", "payload": {"family": "demo.family.ordinary", "op": "add"}}


def _assertion() -> dict[str, object]:
    return {"kind": "assertion", "payload": {"finding": {"id": "demo.finding.1"}}}


class Gate2Cases(unittest.TestCase):
    def setUp(self) -> None:
        self.corpus = _corpus()
        self.universe = package_boundary_digest(ROOT, self.corpus)

    def test_case1_correct_taxpayer_and_year_admits(self) -> None:
        state = project((_grant("demo.auth.g1", "demo.subject.a", "2025", self.universe),))
        resolution = resolve(state, "demo.subject.a", "2025", self.universe)
        self.assertTrue(resolution.admitted)
        self.assertEqual(resolution.status, STATUS_ADMITTED)
        self.assertEqual(resolution.grant_id, "demo.auth.g1")

    def test_case2_wrong_taxpayer_is_classified_mismatch(self) -> None:
        state = project((_grant("demo.auth.g1", "demo.subject.a", "2025", self.universe),))
        resolution = resolve(state, "demo.subject.b", "2025", self.universe)
        self.assertEqual(resolution.status, STATUS_TAXPAYER_MISMATCH)
        self.assertEqual(resolution.detail["expected_subject"], "demo.subject.a")
        self.assertEqual(resolution.detail["actual_subject"], "demo.subject.b")

    def test_case2_mismatch_is_not_gated_on_universe(self) -> None:
        """it1 defect: different taxpayers' boundaries must not degrade to absence."""
        other_universe = "b" * 64
        self.assertNotEqual(other_universe, self.universe)
        state = project((_grant("demo.auth.g1", "demo.subject.a", "2025", self.universe),))
        resolution = resolve(state, "demo.subject.b", "2025", other_universe)
        self.assertEqual(resolution.status, STATUS_TAXPAYER_MISMATCH)

    def test_case3_wrong_year_is_classified_mismatch(self) -> None:
        state = project((_grant("demo.auth.g1", "demo.subject.a", "2025", self.universe),))
        resolution = resolve(state, "demo.subject.a", "2026", self.universe)
        self.assertEqual(resolution.status, STATUS_YEAR_MISMATCH)
        self.assertEqual(resolution.detail["expected_year"], "2025")
        self.assertEqual(resolution.detail["actual_year"], "2026")

    def test_case3_year_mismatch_is_not_gated_on_universe(self) -> None:
        other_universe = "b" * 64
        state = project((_grant("demo.auth.g1", "demo.subject.a", "2025", self.universe),))
        resolution = resolve(state, "demo.subject.a", "2026", other_universe)
        self.assertEqual(resolution.status, STATUS_YEAR_MISMATCH)

    def test_case4_ordinary_membership_changes_do_not_require_renewal(self) -> None:
        acts = (
            _grant("demo.auth.g1", "demo.subject.a", "2025", self.universe),
            _member_transition(),
            _assertion(),
            _member_transition(),
        )
        state = project(acts)
        self.assertEqual(state.grants["demo.auth.g1"].subject_id, "demo.subject.a")
        resolution = resolve(state, "demo.subject.a", "2025", self.universe)
        self.assertTrue(resolution.admitted)

    def test_case5_suspension_withdrawal_and_absence_are_distinct(self) -> None:
        suspended = resolve(
            project(
                (
                    _grant("demo.auth.g1", "demo.subject.a", "2025", self.universe),
                    _end("demo.auth.g1", "suspend"),
                )
            ),
            "demo.subject.a",
            "2025",
            self.universe,
        )
        withdrawn = resolve(
            project(
                (
                    _grant("demo.auth.g1", "demo.subject.a", "2025", self.universe),
                    _end("demo.auth.g1", "withdraw"),
                )
            ),
            "demo.subject.a",
            "2025",
            self.universe,
        )
        absent = resolve(project(()), "demo.subject.a", "2025", self.universe)
        self.assertEqual(suspended.status, STATUS_SUSPENDED)
        self.assertEqual(withdrawn.status, STATUS_WITHDRAWN)
        self.assertEqual(absent.status, STATUS_ABSENT)
        self.assertEqual(len({suspended.status, withdrawn.status, absent.status}), 3)

    def test_case6_superseded_grant_is_stale_and_universe_drift_is_inert(self) -> None:
        acts = (
            _grant("demo.auth.g1", "demo.subject.a", "2025", self.universe),
            _grant(
                "demo.auth.g2",
                "demo.subject.a",
                "2025",
                self.universe,
                supersedes="demo.auth.g1",
            ),
        )
        state = project(acts)
        stale = resolve(
            state, "demo.subject.a", "2025", self.universe, named_authorization_id="demo.auth.g1"
        )
        current = resolve(
            state, "demo.subject.a", "2025", self.universe, named_authorization_id="demo.auth.g2"
        )
        self.assertEqual(stale.status, STATUS_STALE)
        self.assertTrue(current.admitted)

        corpus_after = copy.deepcopy(self.corpus)
        corpus_after["demo.scale.convention"]["version"] = "v2"
        drifted = package_boundary_digest(ROOT, corpus_after)
        self.assertNotEqual(drifted, self.universe)
        universe_state = project(
            (_grant("demo.auth.g1", "demo.subject.a", "2025", self.universe),)
        )
        drifted_resolution = resolve(universe_state, "demo.subject.a", "2025", drifted)
        self.assertEqual(drifted_resolution.status, STATUS_UNIVERSE_SUPERSEDED)
        self.assertEqual(
            drifted_resolution.detail, {"expected": self.universe, "actual": drifted}
        )


class TaxpayerEntitySupersession(unittest.TestCase):
    def setUp(self) -> None:
        self.universe = package_boundary_digest(ROOT, _corpus())

    def test_superseded_subject_is_inert_and_successor_does_not_inherit(self) -> None:
        acts = (
            _grant("demo.auth.g1", "demo.subject.a", "2025", self.universe),
            _entity_superseded("demo.subject.a", "demo.subject.a-successor"),
        )
        state = project(acts)
        original = resolve(state, "demo.subject.a", "2025", self.universe)
        self.assertEqual(original.status, STATUS_SUBJECT_SUPERSEDED)
        self.assertEqual(original.detail["successor"], "demo.subject.a-successor")
        successor = resolve(state, "demo.subject.a-successor", "2025", self.universe)
        self.assertFalse(successor.admitted)
        self.assertEqual(successor.status, STATUS_TAXPAYER_MISMATCH)

    def test_successor_admits_only_after_its_own_grant(self) -> None:
        acts = (
            _grant("demo.auth.g1", "demo.subject.a", "2025", self.universe),
            _entity_superseded("demo.subject.a", "demo.subject.a-successor"),
            _grant("demo.auth.g2", "demo.subject.a-successor", "2025", self.universe),
        )
        state = project(acts)
        self.assertTrue(resolve(state, "demo.subject.a-successor", "2025", self.universe).admitted)
        self.assertEqual(
            resolve(state, "demo.subject.a", "2025", self.universe).status,
            STATUS_SUBJECT_SUPERSEDED,
        )


class StaleSuspendWithdrawCrossProduct(unittest.TestCase):
    def setUp(self) -> None:
        self.universe = package_boundary_digest(ROOT, _corpus())
        self.drifted = "c" * 64

    def test_renewal_after_suspend_admits_new_grant_and_names_prior_stale(self) -> None:
        state = project(
            (
                _grant("demo.auth.g1", "demo.subject.a", "2025", self.universe),
                _end("demo.auth.g1", "suspend"),
                _grant(
                    "demo.auth.g2",
                    "demo.subject.a",
                    "2025",
                    self.universe,
                    supersedes="demo.auth.g1",
                ),
            )
        )
        self.assertTrue(resolve(state, "demo.subject.a", "2025", self.universe).admitted)
        self.assertEqual(
            resolve(
                state, "demo.subject.a", "2025", self.universe, named_authorization_id="demo.auth.g1"
            ).status,
            STATUS_STALE,
        )

    def test_renewal_after_withdraw_admits_new_grant(self) -> None:
        state = project(
            (
                _grant("demo.auth.g1", "demo.subject.a", "2025", self.universe),
                _end("demo.auth.g1", "withdraw"),
                _grant("demo.auth.g2", "demo.subject.a", "2025", self.universe),
            )
        )
        self.assertTrue(resolve(state, "demo.subject.a", "2025", self.universe).admitted)

    def test_superseding_grant_then_suspend_is_suspended_not_stale_for_current_id(self) -> None:
        state = project(
            (
                _grant("demo.auth.g1", "demo.subject.a", "2025", self.universe),
                _grant("demo.auth.g2", "demo.subject.a", "2025", self.universe),
                _end("demo.auth.g2", "suspend"),
            )
        )
        self.assertEqual(
            resolve(state, "demo.subject.a", "2025", self.universe).status, STATUS_SUSPENDED
        )
        self.assertEqual(
            resolve(
                state, "demo.subject.a", "2025", self.universe, named_authorization_id="demo.auth.g2"
            ).status,
            STATUS_SUSPENDED,
        )
        self.assertEqual(
            resolve(
                state, "demo.subject.a", "2025", self.universe, named_authorization_id="demo.auth.g1"
            ).status,
            STATUS_STALE,
        )

    def test_superseding_grant_then_withdraw_is_withdrawn(self) -> None:
        state = project(
            (
                _grant("demo.auth.g1", "demo.subject.a", "2025", self.universe),
                _grant("demo.auth.g2", "demo.subject.a", "2025", self.universe),
                _end("demo.auth.g2", "withdraw"),
            )
        )
        self.assertEqual(
            resolve(state, "demo.subject.a", "2025", self.universe).status, STATUS_WITHDRAWN
        )

    def test_superseding_grant_then_universe_drift(self) -> None:
        state = project(
            (
                _grant("demo.auth.g1", "demo.subject.a", "2025", self.universe),
                _grant("demo.auth.g2", "demo.subject.a", "2025", self.universe),
            )
        )
        self.assertEqual(
            resolve(state, "demo.subject.a", "2025", self.drifted).status,
            STATUS_UNIVERSE_SUPERSEDED,
        )
        self.assertEqual(
            resolve(
                state, "demo.subject.a", "2025", self.drifted, named_authorization_id="demo.auth.g1"
            ).status,
            STATUS_STALE,
        )

    def test_ended_grant_wins_over_universe_drift(self) -> None:
        state = project(
            (
                _grant("demo.auth.g1", "demo.subject.a", "2025", self.universe),
                _end("demo.auth.g1", "suspend"),
            )
        )
        self.assertEqual(
            resolve(state, "demo.subject.a", "2025", self.drifted).status, STATUS_SUSPENDED
        )

    def test_ended_grant_wins_over_subject_supersession(self) -> None:
        state = project(
            (
                _grant("demo.auth.g1", "demo.subject.a", "2025", self.universe),
                _entity_superseded("demo.subject.a", "demo.subject.a-successor"),
                _end("demo.auth.g1", "withdraw"),
            )
        )
        self.assertEqual(
            resolve(state, "demo.subject.a", "2025", self.universe).status, STATUS_WITHDRAWN
        )

    def test_superseding_grant_then_subject_supersession(self) -> None:
        state = project(
            (
                _grant("demo.auth.g1", "demo.subject.a", "2025", self.universe),
                _grant("demo.auth.g2", "demo.subject.a", "2025", self.universe),
                _entity_superseded("demo.subject.a", "demo.subject.a-successor"),
            )
        )
        self.assertEqual(
            resolve(state, "demo.subject.a", "2025", self.universe).status,
            STATUS_SUBJECT_SUPERSEDED,
        )
        self.assertEqual(
            resolve(
                state, "demo.subject.a", "2025", self.universe, named_authorization_id="demo.auth.g1"
            ).status,
            STATUS_STALE,
        )


class CompositionHelper(unittest.TestCase):
    def test_resolve_for_composition_computes_current_digest(self) -> None:
        corpus = _corpus()
        universe = package_boundary_digest(ROOT, corpus)
        acts = (_grant("demo.auth.g1", "demo.subject.a", "2025", universe),)
        resolution = resolve_for_composition(
            acts,
            subject_id="demo.subject.a",
            tax_year="2025",
            root_rule_ids=ROOT,
            corpus=corpus,
        )
        self.assertTrue(resolution.admitted)


if __name__ == "__main__":
    unittest.main()
