"""Synthetic evidence tests for the recorded-horizon reducer."""

from __future__ import annotations

import inspect
import unittest

from reducer import Reject, State, apply, currency, replay_check


def h(ident: str, family: str, scope: str, previous: str | None) -> dict[str, object]:
    return {"id": ident, "family": family, "scope": scope, "previous": previous}


F, G, SCOPE = "demo-B1", "demo-B3", "tax-year-2025"


def scenario() -> list[dict[str, object]]:
    return [
        {"kind": "open_family", "family": F, "scope": SCOPE, "horizon": h("H0", F, SCOPE, None)},
        {"kind": "open_family", "family": G, "scope": SCOPE, "horizon": h("G0", G, SCOPE, None)},
        {"kind": "closure_attested", "id": "K0", "family": F, "scope": SCOPE, "horizon": "H0", "value": True},
        {"kind": "run_zero", "id": "Z0", "closure": "K0"},
        {"kind": "closure_attested", "id": "KG0", "family": G, "scope": SCOPE, "horizon": "G0", "value": True},
        {"kind": "run_zero", "id": "ZG0", "closure": "KG0"},
        {"kind": "member_change", "family": F, "scope": SCOPE, "operation": "add", "member": "M1", "relevant": True, "horizon": h("H1", F, SCOPE, "H0")},
        {"kind": "member_change", "family": F, "scope": SCOPE, "operation": "value_correction", "member": "M1", "relevant": True},
        {"kind": "member_change", "family": F, "scope": SCOPE, "operation": "predicate_change", "member": "M1", "relevant": False, "horizon": h("H2", F, SCOPE, "H1")},
        {"kind": "member_change", "family": F, "scope": SCOPE, "operation": "add", "member": "M2", "relevant": True, "horizon": h("H3", F, SCOPE, "H2")},
        {"kind": "member_change", "family": F, "scope": SCOPE, "operation": "remove", "member": "M2", "relevant": None, "horizon": h("H4", F, SCOPE, "H3")},
        {"kind": "closure_attested", "id": "K4", "family": F, "scope": SCOPE, "horizon": "H4", "value": True},
        {"kind": "run_zero", "id": "Z4", "closure": "K4"},
    ]


class RecordedHorizonReducerTests(unittest.TestCase):
    def test_replay_after_every_act_and_required_cases(self) -> None:
        views = replay_check(scenario())
        self.assertIn("Z0", views[3].current)  # fresh empty zero
        late_member = views[6]
        self.assertEqual(late_member.roots, frozenset({"H0"}))
        self.assertTrue({"K0", "Z0"} <= late_member.displaced)
        self.assertEqual(late_member.reasons["K0"], (("individuation", "H0"),))
        self.assertEqual(late_member.reasons["Z0"], (("derivation", "K0"),))
        self.assertEqual(views[7], late_member)  # same-member value correction
        self.assertIn("ZG0", views[10].current)  # family G isolation
        self.assertNotIn("Z0", views[10].current)  # removal did not resurrect it
        self.assertIn("Z4", views[-1].current)  # only re-attestation/rerun replaces it

    def test_missing_successor_mutant_is_killed(self) -> None:
        acts = scenario()[:6]
        mutant = {"kind": "member_change", "family": F, "scope": SCOPE, "operation": "add", "member": "M1", "relevant": True}
        with self.assertRaisesRegex(Reject, "requires exactly one horizon successor"):
            replay_check(acts + [mutant])

    def test_rejected_member_change_is_atomic(self) -> None:
        state = State()
        for act in scenario()[:2]:
            apply(state, act)
        half = {"kind": "member_change", "family": F, "scope": SCOPE, "operation": "add", "member": "M1", "relevant": True, "horizon": h("H1", F, SCOPE, "not-H0")}
        with self.assertRaises(Reject):
            apply(state, half)
        self.assertEqual(state.current_horizon[(F, SCOPE)], "H0")
        self.assertNotIn(((F, SCOPE), "M1"), state.members)

    def test_direct_stale_root_or_flag_mutant_is_killed(self) -> None:
        state = State()
        for act in scenario()[:4]:
            apply(state, act)
        self.assertIn("Z0", currency(state).current)
        # Test-local mutation attempt: the reducer exposes no injected-root/flag input.
        self.assertEqual(list(inspect.signature(currency).parameters), ["state"])
        with self.assertRaises(TypeError):
            currency(state, {"Z0"})  # type: ignore[call-arg]
        with self.assertRaisesRegex(Reject, "unknown/caller authority fields"):
            apply(state, {"kind": "run_zero", "id": "bad", "closure": "K0", "stale": True})

    def test_fabricated_future_replayed_misscoped_and_half_transitions_reject(self) -> None:
        prefix = scenario()[:6]
        bads = [
            {"kind": "closure_attested", "id": "future", "family": F, "scope": SCOPE, "horizon": "H99", "value": True},
            {"kind": "member_change", "family": F, "scope": SCOPE, "operation": "add", "member": "M1", "relevant": True, "horizon": h("H1", G, SCOPE, "H0")},
            {"kind": "member_change", "family": F, "scope": SCOPE, "operation": "add", "member": "M1", "relevant": True, "horizon": h("H1", F, SCOPE, "H99")},
            {"kind": "derived_closure"},
            {"kind": "member_change", "family": F, "scope": SCOPE, "operation": "remove", "member": "M1", "relevant": None, "horizon": h("H2", F, SCOPE, "H1")},
            {"kind": "open_family", "family": "GLOBAL", "scope": SCOPE, "horizon": h("ALL", "GLOBAL", SCOPE, None)},
        ]
        for bad in bads:
            with self.subTest(bad=bad), self.assertRaises(Reject):
                replay_check(prefix + [bad])
        accepted = prefix + [scenario()[6]]
        with self.assertRaises(Reject):
            replay_check(accepted + [scenario()[6]])  # replayed horizon/member act


if __name__ == "__main__":
    unittest.main()
