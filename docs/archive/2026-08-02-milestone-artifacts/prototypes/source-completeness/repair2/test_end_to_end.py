"""Rung-3 end-to-end measurements for SC-P1 (charter-repair2).

The faithful two-layer `collect` copy consumes repair1's resolved authority.
Every case runs through PUBLICATION (not just resolver output), for BOTH
authority shapes (A dedicated mapping citizen, B embedded adopted-rule param).
All fixtures synthetic.

Run:  python3 -m unittest -v test_end_to_end
"""

from __future__ import annotations

import dataclasses
import os
import sys
import unittest
from decimal import Decimal

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, "..", "repair1"))

import prototype_eval as E   # noqa: E402
import resolver as R         # noqa: E402  (repair1)

YEAR = frozenset({("tax-year", "2097")})
FAM = "sf-demo-interest-2097"
CFT = "closure.demo.interest.source-closure"
MEMBER = "member.demo.interest.box1"
RULE = {"id": "rule.demo.interest", "version": "v1",
        "publishes": "sym.interest.total",
        "value": {"name": MEMBER, "source_set": FAM}}


def clo(value, fid, version="v1", supersedes=None):
    return R.ClosureFinding(CFT, YEAR, value, fid, version, supersedes)


def resolved_A(findings, admit=R.admit_current_true, entries=None):
    entries = entries or (R.MappingEntry(FAM, CFT, YEAR),)
    return R.resolve_A(R.MappingCitizen("map.demo.v1", "v1", tuple(entries)),
                       findings, admit=admit)


def resolved_B(findings, admit=R.admit_current_true, rules=None):
    rules = rules or (R.CollectingRule("rule.demo.interest", "v1", FAM, MEMBER,
                                       R.ClosureAuthorityParam(CFT, YEAR, True)),)
    return R.resolve_B(list(rules), frozenset(r.artifact_id for r in rules),
                       findings, admit=admit)


SHAPES = {"A": resolved_A, "B": resolved_B}


def publishes(env):
    """Return the Publication, or None if L2 blocked through to publication."""
    try:
        return E.run_rule(RULE, env)
    except E.EvalBlocked:
        return None


class Layer1(unittest.TestCase):
    def test_present_members_publish_without_consulting_closure(self):
        # members present -> aggregate; closure absent yet publication succeeds
        sources = {MEMBER: [("11", "fid-m1"), ("23", "fid-m2")]}
        for name, resolve in SHAPES.items():
            with self.subTest(shape=name):
                env = E.Env(sources, resolve([]))       # no closure finding
                pub = publishes(env)
                self.assertIsNotNone(pub)
                self.assertEqual(pub.value, Decimal(34))
                # no closure-authority pin: layer 2 never ran
                self.assertFalse(any(p.role == "closure-authority" for p in pub.pins))
                self.assertEqual(sum(p.role == "input" for p in pub.pins), 2)


class Layer2Admission(unittest.TestCase):
    def test_empty_publishes_zero_only_for_current_true(self):
        for name, resolve in SHAPES.items():
            with self.subTest(shape=name):
                env = E.Env({}, resolve([clo(True, "clo-true")]))
                pub = publishes(env)
                self.assertIsNotNone(pub)
                self.assertEqual(pub.value, Decimal(0))

    def test_negatives_block_through_publication(self):
        cases = {
            "false": [clo(False, "f1")],
            "absent": [],
            "displaced": [clo(True, "old"), clo(False, "new", supersedes="old")],
            "truthy-1": [clo(1, "t1")],
            "truthy-str": [clo("true", "t2")],
            "ambiguous": [clo(True, "a"), clo(True, "b")],
        }
        for name, resolve in SHAPES.items():
            for label, findings in cases.items():
                with self.subTest(shape=name, case=label):
                    env = E.Env({}, resolve(findings))
                    self.assertIsNone(publishes(env),
                                      f"{label} must block through publication")


class ExplanationPins(unittest.TestCase):
    def test_zero_pins_exact_current_true_finding(self):
        for name, resolve in SHAPES.items():
            with self.subTest(shape=name):
                env = E.Env({}, resolve([clo(True, "clo-true", version="v3")]))
                pub = publishes(env)
                pin = next(p for p in pub.pins if p.role == "closure-authority")
                self.assertEqual((pin.id, pin.version), ("clo-true", "v3"))

    def test_reattested_true_pins_new_not_displaced_finding(self):
        for name, resolve in SHAPES.items():
            with self.subTest(shape=name):
                env = E.Env({}, resolve([
                    clo(True, "old-true"),
                    clo(True, "new-true", version="v2", supersedes="old-true"),
                ]))
                pin = next(p for p in publishes(env).pins
                           if p.role == "closure-authority")
                self.assertEqual(pin.id, "new-true")


class Ambiguity(unittest.TestCase):
    def test_A_duplicate_mapping_entries_block_publication(self):
        env = E.Env({}, resolved_A([clo(True, "t")],
                                    entries=(R.MappingEntry(FAM, CFT, YEAR),
                                             R.MappingEntry(FAM, CFT, YEAR))))
        self.assertIsNone(publishes(env))

    def test_B_duplicate_adopted_rules_block_publication(self):
        rules = (R.CollectingRule("rule.demo.interest", "v1", FAM, MEMBER,
                                  R.ClosureAuthorityParam(CFT, YEAR, True)),
                 R.CollectingRule("rule.demo.interest2", "v1", FAM, MEMBER,
                                  R.ClosureAuthorityParam(CFT, YEAR, True)))
        env = E.Env({}, resolved_B([clo(True, "t")], rules=rules))
        self.assertIsNone(publishes(env))


class CallerInjection(unittest.TestCase):
    def test_env_has_no_caller_closed_set_field(self):
        self.assertEqual(E.env_field_names(), ["sources", "resolved"])
        with self.assertRaises(TypeError):
            E.Env({}, resolved_A([]), closed_sets=frozenset({FAM}))  # type: ignore

    def test_no_construction_path_admits_a_bare_family(self):
        # faithful path: absent closure -> blocked even though FAM is "wanted"
        for name, resolve in SHAPES.items():
            with self.subTest(shape=name):
                env = E.Env({}, resolve([]))
                self.assertIsNone(publishes(env))


class Mutants(unittest.TestCase):
    """Charter deliverable 4: end-to-end mutants killed per shape."""

    def test_caller_union_mutant_killed_by_injection(self):
        for name, resolve in SHAPES.items():
            with self.subTest(shape=name):
                env = E.Env({}, resolve([]))            # no authority for FAM
                self.assertIsNone(publishes(env), "faithful blocks")
                pub = E.run_rule_caller_union(RULE, env, {FAM})  # smuggle
                self.assertIsNotNone(pub, "mutant publishes injected zero -> kill")
                self.assertEqual(pub.value, Decimal(0))

    def test_presence_only_resolver_mutant_killed_by_false_closure(self):
        for name, resolve in SHAPES.items():
            with self.subTest(shape=name):
                findings = [clo(False, "f1")]
                faithful = E.Env({}, resolve(findings, admit=R.admit_current_true))
                mutant = E.Env({}, resolve(findings, admit=R.admit_presence_only))
                self.assertIsNone(publishes(faithful), "faithful blocks false")
                self.assertIsNotNone(publishes(mutant),
                                     "presence-only admits false -> publishes -> kill")


if __name__ == "__main__":
    unittest.main()
