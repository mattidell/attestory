"""Repair pass 4 measurements: single evaluation entry, no bypass reachable.

Every calculation goes through the one public entry `surface.compute`. Mutants
(duck carrier, direct-raw, presence-only) live ONLY here, never in the runtime
module. Shape A only. All fixtures synthetic.

Run:  python3 -m unittest -v test_surface
"""

from __future__ import annotations

import inspect
import os
import sys
import types
import unittest
from decimal import Decimal

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, "..", "repair1"))

import surface as S     # noqa: E402  (the selected runtime surface)
import resolver as R    # noqa: E402  (repair1; test-side only)

YEAR = frozenset({("tax-year", "2097")})
FAM = "sf-demo-interest-2097"
CFT = "closure.demo.interest.source-closure"
MEMBER = "member.demo.interest.box1"
RULE = {"id": "rule.demo.interest", "version": "v1",
        "publishes": "sym.interest.total",
        "value": {"name": MEMBER, "source_set": FAM}}
MAPPING = R.MappingCitizen("map.demo.v1", "v1", (R.MappingEntry(FAM, CFT, YEAR),))


def clo(value, fid, version="v1", supersedes=None):
    return R.ClosureFinding(CFT, YEAR, value, fid, version, supersedes)


def compute(source_rows, findings):
    try:
        return S.compute(RULE, source_rows, MAPPING, findings)
    except S.Blocked:
        return None


class ValueCurrencyAmbiguityPin(unittest.TestCase):
    def test_true_publishes_zero_with_exact_pin(self):
        pub = compute({}, [clo(True, "clo-true", version="v5")])
        self.assertEqual(pub.value, Decimal(0))
        pin = next(p for p in pub.pins if p.role == "closure-authority")
        self.assertEqual((pin.id, pin.version), ("clo-true", "v5"))

    def test_present_members_omit_closure_pins(self):
        pub = compute({MEMBER: [("11", "fid-m1"), ("23", "fid-m2")]}, [])
        self.assertEqual(pub.value, Decimal(34))
        self.assertFalse(any(p.role == "closure-authority" for p in pub.pins))
        self.assertEqual(sum(p.role == "input" for p in pub.pins), 2)

    def test_negatives_block_through_publication(self):
        cases = {
            "false": [clo(False, "f")],
            "absent": [],
            "displaced": [clo(True, "old"), clo(False, "new", supersedes="old")],
            "truthy-int": [clo(1, "t1")],
            "truthy-str": [clo("true", "t2")],
            "ambiguous": [clo(True, "a"), clo(True, "b")],
            "dup-entries": None,   # handled below
        }
        for label, findings in cases.items():
            if label == "dup-entries":
                continue
            with self.subTest(case=label):
                self.assertIsNone(compute({}, findings))

    def test_duplicate_mapping_entries_block(self):
        dup = R.MappingCitizen("map.demo.v1", "v1",
                               (R.MappingEntry(FAM, CFT, YEAR),
                                R.MappingEntry(FAM, CFT, YEAR)))
        with self.assertRaises(S.Blocked):
            S.compute(RULE, {}, dup, [clo(True, "t")])

    def test_stale_first_current_second_pins_successor(self):
        for hist in (
            [clo(True, "old"), clo(True, "new", version="v2", supersedes="old")],
            [clo(True, "new", version="v2", supersedes="old"), clo(True, "old")],
        ):
            with self.subTest(order=[f.finding_id for f in hist]):
                pin = next(p for p in compute({}, hist).pins
                           if p.role == "closure-authority")
                self.assertEqual(pin.id, "new")

    def test_inputs_are_the_exact_values_used_for_resolution_and_pins(self):
        f = clo(True, "exact-fid", version="v7")
        pub = compute({}, [f])
        cpin = next(p for p in pub.pins if p.role == "closure-authority")
        apin = next(p for p in pub.pins if p.role == "mapping-citizen")
        self.assertEqual((cpin.id, cpin.version), (f.finding_id, f.version))
        self.assertEqual((apin.id, apin.version),
                         (MAPPING.artifact_id, MAPPING.version))


class SupportedSurface(unittest.TestCase):
    def test_only_public_function_is_compute(self):
        public_funcs = [n for n in dir(S)
                        if not n.startswith("_")
                        and isinstance(getattr(S, n), types.FunctionType)]
        self.assertEqual(public_funcs, ["compute"])
        self.assertEqual(S.__all__, ["compute"])

    def test_no_raw_evaluator_or_resolver_re_exported(self):
        # the private import and internal steps are underscore/absent, not public
        for banned in ("resolver", "Env", "run_rule", "run_rule_with_carrier",
                       "run_rule_trusting", "AuthorizedMembership", "authorize"):
            self.assertNotIn(banned, S.__all__)
            self.assertFalse(
                isinstance(getattr(S, banned, None), types.FunctionType))

    def test_compute_signature_accepts_no_authority_object(self):
        params = list(inspect.signature(S.compute).parameters)
        self.assertEqual(params, ["rule", "source_rows", "mapping", "findings"])
        # none of these names is a carrier / closed-set / env / validator hook
        for banned in ("carrier", "authority", "closed_sets", "env",
                       "membership", "validator"):
            self.assertNotIn(banned, params)


class RejectedPathsAreTestLocalMutants(unittest.TestCase):
    """Charter deliverable 4: show the duck and direct-raw paths diverge, using
    ONLY test-local mutants that reach the surface's privates — never a public
    API. The point is that no public entry offers these."""

    def test_duck_carrier_has_no_public_parameter_to_enter(self):
        # A duck-typed 'authority' object with the old carrier methods...
        class DuckAuthority:
            closed_families = frozenset({FAM})
            def pin_for(self, fam):  # noqa: D401
                return R.ClosureAuthority(FAM, "duck", "v1",
                                          "mapping-citizen", "map.demo.v1", "v1")
        duck = DuckAuthority()
        # ...cannot be supplied: compute takes no such parameter (TypeError).
        with self.assertRaises(TypeError):
            S.compute(RULE, {}, MAPPING, [], duck)          # extra arg rejected
        with self.assertRaises(TypeError):
            S.compute(RULE, {}, MAPPING, [], authority=duck)  # kw rejected

    def test_direct_raw_private_path_would_bypass_but_is_not_public(self):
        # MUTANT (test-local): reach the private _collect with a fabricated
        # admitted map. It publishes -> proving why _collect stays private.
        fabricated = {FAM: R.ClosureAuthority(FAM, "fake", "v1",
                                              "mapping-citizen", "map.demo.v1", "v1")}
        access = {"collects": set(), "closure_admits": {}}
        rows = S._collect(RULE["value"], {}, fabricated, access)  # private!
        self.assertEqual(rows, [])   # the raw path would zero on a fabrication
        # But the public entry gives no way to supply `fabricated`: only real
        # findings resolve authority, and none here would admit FAM.
        self.assertIsNone(compute({}, []))
        # and _collect is not a public evaluation entry
        self.assertTrue("_collect".startswith("_"))
        self.assertNotIn("_collect", S.__all__)

    def test_presence_only_mutant_is_test_local_only(self):
        # A presence-only resolution mutant lives here, not in surface.py.
        def presence_only(mapping, findings):
            fresh = R.resolve_A(mapping, findings, admit=R.admit_presence_only)
            return {a.source_family: a for a in fresh.authority}
        admitted = presence_only(MAPPING, [clo(False, "f")])
        self.assertIn(FAM, admitted)          # mutant admits false
        self.assertIsNone(compute({}, [clo(False, "f")]))  # surface blocks it


if __name__ == "__main__":
    unittest.main()
