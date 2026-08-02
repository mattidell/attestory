"""Repair pass 3 measurements: shape-A authority construction/invariant boundary.

Closes the round-2 carrier-fabrication finding: a caller can no longer make an
evaluator-accepted authority, because the mandatory gate re-derives from declared
inputs. Shape A only (the selected shape). All fixtures synthetic.

Run:  python3 -m unittest -v test_authority
"""

from __future__ import annotations

import os
import sys
import unittest
from decimal import Decimal

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, "..", "repair1"))
sys.path.insert(0, os.path.join(_HERE, "..", "repair2"))

import authorized_eval as A   # noqa: E402
import resolver as R          # noqa: E402

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


def authored(source_family, finding_id, finding_version="v1",
             mapping_id="map.demo.v1", mapping_version="v1"):
    """Hand-fabricate a carrier the way the round-2 attack did."""
    auth = R.ClosureAuthority(source_family, finding_id, finding_version,
                              "mapping-citizen", "map.demo.v1", "v1")
    return A.AuthorizedMembership((auth,), mapping_id, mapping_version)


def publishes_authorized(sources, findings):
    try:
        return A.run_rule_authorized(RULE, sources, MAPPING, findings)
    except A.E.EvalBlocked:
        return None


class GenuinePath(unittest.TestCase):
    def test_true_closure_publishes_zero_with_exact_pin(self):
        pub = publishes_authorized({}, [clo(True, "clo-true", version="v5")])
        self.assertEqual(pub.value, Decimal(0))
        pin = next(p for p in pub.pins if p.role == "closure-authority")
        self.assertEqual((pin.id, pin.version), ("clo-true", "v5"))

    def test_present_members_do_not_consult_or_pin_closure(self):
        sources = {MEMBER: [("11", "fid-m1"), ("23", "fid-m2")]}
        pub = publishes_authorized(sources, [])          # no closure at all
        self.assertEqual(pub.value, Decimal(34))
        self.assertFalse(any(p.role == "closure-authority" for p in pub.pins))


class NegativesBlockedThroughPublication(unittest.TestCase):
    def test_all_negatives_block(self):
        cases = {
            "false": [clo(False, "f")],
            "absent": [],
            "displaced": [clo(True, "old"), clo(False, "new", supersedes="old")],
            "truthy-int": [clo(1, "t1")],
            "truthy-str": [clo("true", "t2")],
            "ambiguous": [clo(True, "a"), clo(True, "b")],
        }
        for label, findings in cases.items():
            with self.subTest(case=label):
                self.assertIsNone(publishes_authorized({}, findings))

    def test_bare_family_cannot_publish(self):
        # nothing resolves FAM -> authorized path blocks at layer 2
        self.assertIsNone(publishes_authorized({}, []))


class CarrierFabrication(unittest.TestCase):
    """The round-2 finding, now rejected before publication."""

    def test_fabricated_authority_rejected(self):
        # empty real findings, but a hand-built carrier claims a true finding
        carrier = authored(FAM, "totally-fake-finding")
        with self.assertRaises(A.AuthorityInvalid):
            A.run_rule_with_carrier(RULE, {}, carrier, MAPPING, findings=[])

    def test_genuine_carrier_accepted(self):
        # a carrier equal to real resolver output validates and publishes
        findings = [clo(True, "clo-true")]
        carrier = A.authorize(MAPPING, findings)
        pub = A.run_rule_with_carrier(RULE, {}, carrier, MAPPING, findings)
        self.assertEqual(pub.value, Decimal(0))

    def test_mapping_provenance_mismatch_rejected(self):
        findings = [clo(True, "clo-true")]
        carrier = A.authorize(MAPPING, findings)
        other = R.MappingCitizen("map.OTHER", "v9", (R.MappingEntry(FAM, CFT, YEAR),))
        with self.assertRaises(A.AuthorityInvalid):
            A.run_rule_with_carrier(RULE, {}, carrier, other, findings)


class DuplicateAndStale(unittest.TestCase):
    def test_duplicate_same_family_rejected_either_order(self):
        a1 = R.ClosureAuthority(FAM, "clo-x", "v1", "mapping-citizen", "map.demo.v1", "v1")
        a2 = R.ClosureAuthority(FAM, "clo-y", "v1", "mapping-citizen", "map.demo.v1", "v1")
        for order in ((a1, a2), (a2, a1)):
            with self.subTest(order=[a.finding_id for a in order]):
                carrier = A.AuthorizedMembership(order, "map.demo.v1", "v1")
                with self.assertRaises(A.AuthorityInvalid):
                    A.run_rule_with_carrier(RULE, {}, carrier, MAPPING, findings=[clo(True, "clo-x")])

    def test_stale_first_current_second_cannot_select_stale_pin(self):
        # both orderings of the finding history: current is the successor
        for hist in (
            [clo(True, "old-true"), clo(True, "new-true", version="v2", supersedes="old-true")],
            [clo(True, "new-true", version="v2", supersedes="old-true"), clo(True, "old-true")],
        ):
            with self.subTest(order=[f.finding_id for f in hist]):
                pub = publishes_authorized({}, hist)
                pin = next(p for p in pub.pins if p.role == "closure-authority")
                self.assertEqual(pin.id, "new-true")          # never the stale one
                # a carrier claiming the stale pin is rejected
                stale = authored(FAM, "old-true")
                with self.assertRaises(A.AuthorityInvalid):
                    A.run_rule_with_carrier(RULE, {}, stale, MAPPING, hist)


class ConstructorBypassMutant(unittest.TestCase):
    """Charter deliverable 4: the unsafe (unvalidated) path publishes the
    fabrication that the validated paths reject -> killed."""

    def test_bypass_mutant_killed_by_fabricated_authority(self):
        fabricated = authored(FAM, "fake-finding")
        # validated path rejects
        with self.assertRaises(A.AuthorityInvalid):
            A.run_rule_with_carrier(RULE, {}, fabricated, MAPPING, findings=[])
        # bypass mutant trusts it and publishes -> kill
        pub = A.run_rule_trusting(RULE, {}, fabricated)
        self.assertEqual(pub.value, Decimal(0))

    def test_bypass_mutant_killed_by_duplicate_authority(self):
        a1 = R.ClosureAuthority(FAM, "clo-x", "v1", "mapping-citizen", "map.demo.v1", "v1")
        a2 = R.ClosureAuthority(FAM, "clo-y", "v1", "mapping-citizen", "map.demo.v1", "v1")
        dup = A.AuthorizedMembership((a1, a2), "map.demo.v1", "v1")
        with self.assertRaises(A.AuthorityInvalid):
            A.run_rule_with_carrier(RULE, {}, dup, MAPPING, findings=[clo(True, "clo-x")])
        pub = A.run_rule_trusting(RULE, {}, dup)          # unvalidated -> publishes
        self.assertEqual(pub.value, Decimal(0))


if __name__ == "__main__":
    unittest.main()
