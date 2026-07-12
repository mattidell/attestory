"""Rung-2 measurements for SC-P1 affirmative-only enforcement (charter-repair1).

Each authority shape (A = dedicated mapping citizen, B = embedded adopted-rule
parameter) is exercised INDEPENDENTLY through the same admission cases. All
fixtures are synthetic: manufactured families, payers, scopes, finding ids.

Run:  python3 -m unittest -v resolver_tests   (see examination-repair1.md)
"""

from __future__ import annotations

import unittest

import resolver as R

YEAR = frozenset({("tax-year", "2097")})           # synthetic scope
FAM = "sf-demo-interest-2097"
CFT = "closure.demo.interest.source-closure"


def clo(value, fid, version="v1", supersedes=None, fact_type=CFT, identity=YEAR):
    return R.ClosureFinding(fact_type, identity, value, fid, version, supersedes)


# --- shape adapters: build each shape's inputs and resolve with a chosen admit
def solve_A(findings, admit=R.admit_current_true, entries=None):
    entries = entries or (
        R.MappingEntry(FAM, CFT, YEAR),
    )
    mapping = R.MappingCitizen("map.demo.v1", "v1", tuple(entries))
    return R.resolve_A(mapping, findings, admit=admit)


def solve_B(findings, admit=R.admit_current_true, rules=None, adopted=None):
    rules = rules or (
        R.CollectingRule("rule.demo.v1", "v1", FAM, "member.demo.v1",
                         R.ClosureAuthorityParam(CFT, YEAR, True)),
    )
    adopted = frozenset(adopted or {r.artifact_id for r in rules})
    return R.resolve_B(list(rules), adopted, findings, admit=admit)


SHAPES = {"A": solve_A, "B": solve_B}


class AdmissionCases(unittest.TestCase):
    """Charter deliverable 2 + pre-declared checks 1 & 4, both shapes."""

    def test_one_current_true_admitted_with_exact_pin(self):
        for name, solve in SHAPES.items():
            with self.subTest(shape=name):
                m = solve([clo(True, "clo-true-1")])
                self.assertIn(FAM, m.closed_families)
                self.assertEqual(m.pin_for(FAM).finding_id, "clo-true-1")

    def test_current_false_blocked(self):
        for name, solve in SHAPES.items():
            with self.subTest(shape=name):
                m = solve([clo(False, "clo-false-1")])
                self.assertNotIn(FAM, m.closed_families)

    def test_absent_blocked(self):
        for name, solve in SHAPES.items():
            with self.subTest(shape=name):
                m = solve([])                       # no closure finding at all
                self.assertEqual(m.closed_families, frozenset())

    def test_displaced_true_then_false_blocked(self):
        # historical true, superseded by a current false -> block (currency)
        for name, solve in SHAPES.items():
            with self.subTest(shape=name):
                m = solve([
                    clo(True, "clo-old-true"),
                    clo(False, "clo-new-false", supersedes="clo-old-true"),
                ])
                self.assertNotIn(FAM, m.closed_families)

    def test_displaced_true_then_true_pins_the_current_finding(self):
        # re-attested true -> admitted, but the pin MUST be the current finding
        for name, solve in SHAPES.items():
            with self.subTest(shape=name):
                m = solve([
                    clo(True, "clo-old-true"),
                    clo(True, "clo-new-true", version="v2",
                        supersedes="clo-old-true"),
                ])
                self.assertIn(FAM, m.closed_families)
                self.assertEqual(m.pin_for(FAM).finding_id, "clo-new-true")
                self.assertEqual(m.pin_for(FAM).finding_version, "v2")

    def test_truthy_but_not_literal_true_blocked(self):
        # ADR-0011: only literal boolean true; 1 / "true" must not admit
        for name, solve in SHAPES.items():
            for bad in (1, "true", "yes"):
                with self.subTest(shape=name, value=bad):
                    m = solve([clo(bad, "clo-truthy")])
                    self.assertNotIn(FAM, m.closed_families)


class AmbiguityCases(unittest.TestCase):
    """Charter check 1 (ambiguity) + adversary A6 stale-pin."""

    def test_two_matching_current_findings_block_both_shapes(self):
        # two current findings for one authority identity -> AMBIGUOUS -> block
        for name, solve in SHAPES.items():
            with self.subTest(shape=name):
                m = solve([clo(True, "clo-a"), clo(True, "clo-b")])
                self.assertNotIn(FAM, m.closed_families)

    def test_A_duplicate_mapping_entries_block(self):
        m = solve_A([clo(True, "clo-true-1")],
                    entries=(R.MappingEntry(FAM, CFT, YEAR),
                             R.MappingEntry(FAM, CFT, YEAR)))
        self.assertNotIn(FAM, m.closed_families)

    def test_B_duplicate_adopted_rules_block(self):
        rules = (
            R.CollectingRule("rule.demo.v1", "v1", FAM, "member.demo.v1",
                             R.ClosureAuthorityParam(CFT, YEAR, True)),
            R.CollectingRule("rule.demo.v2", "v2", FAM, "member.demo.v1",
                             R.ClosureAuthorityParam(CFT, YEAR, True)),
        )
        m = solve_B([clo(True, "clo-true-1")], rules=rules)
        self.assertNotIn(FAM, m.closed_families)


class CallerInjectionCases(unittest.TestCase):
    """Charter check 3: no caller-controlled bare set can augment membership."""

    def test_membership_is_frozen(self):
        m = solve_A([clo(True, "clo-true-1")])
        with self.assertRaises(R.FrozenInstanceError):
            m.authority = tuple()                    # type: ignore[misc]

    def test_env_closed_sets_takes_no_caller_set(self):
        # The only producer of L2 membership has arity 1 (the resolved result).
        import inspect
        params = list(inspect.signature(R.env_closed_sets).parameters)
        self.assertEqual(params, ["resolved"])

    def test_bare_family_string_needs_a_finding_to_exist(self):
        # A caller cannot conjure a family: without an admitting finding the
        # resolver yields empty membership; there is no union-with-caller path.
        m = solve_B([])
        self.assertEqual(env_closed := R.env_closed_sets(m), frozenset())
        self.assertEqual(env_closed, frozenset())


class MutationMatrix(unittest.TestCase):
    """Charter deliverable 3 + check 2: named mutants die on named cases,
    deterministically, for BOTH shapes. A mutant is 'killed' when the correct
    resolver blocks a family that the mutant admits."""

    def _admits(self, solve, admit, findings):
        return FAM in solve(findings, admit=admit).closed_families

    def test_presence_only_mutant_killed_by_false_closure(self):
        findings = [clo(False, "clo-false-1")]
        for name, solve in SHAPES.items():
            with self.subTest(shape=name):
                self.assertFalse(self._admits(solve, R.admit_current_true, findings),
                                 "correct resolver must block false")
                self.assertTrue(self._admits(solve, R.admit_presence_only, findings),
                                "presence-only mutant admits false -> divergence = kill")

    def test_currency_blind_mutant_killed_by_displaced_true(self):
        findings = [
            clo(True, "clo-old-true"),
            clo(False, "clo-new-false", supersedes="clo-old-true"),
        ]
        for name, solve in SHAPES.items():
            with self.subTest(shape=name):
                self.assertFalse(self._admits(solve, R.admit_current_true, findings),
                                 "correct resolver reads current (false) -> block")
                self.assertTrue(self._admits(solve, R.admit_presence_any_history, findings),
                                "currency-blind mutant resurrects historical true -> kill")

    def test_truthy_mutant_killed_by_non_literal_true(self):
        findings = [clo(1, "clo-truthy")]                # truthy int, not True
        for name, solve in SHAPES.items():
            with self.subTest(shape=name):
                self.assertFalse(self._admits(solve, R.admit_current_true, findings),
                                 "correct resolver requires literal True -> block")
                self.assertTrue(self._admits(solve, R.admit_truthy, findings),
                                "truthy mutant admits 1 -> kill")


if __name__ == "__main__":
    unittest.main()
