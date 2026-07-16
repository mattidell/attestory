"""Verification of the non-publication explanation walker (walk_npe).

Tests cover published, blocked, guard_inapplicable, and no_disposition_recorded
scenarios, including cycle detection, memoization, and run-scoped selection.
"""

import unittest
from typing import Any

from packages.derivation.explanation import walk_npe, CyclicDependencyError
from packages.derivation.loader import DerivationSchemas


class TestNpeWalk(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.rules = [
            {"id": "rule.s1", "version": "v1", "publishes": "s1", "requires": ["s2", "s3"], "role": "computation"},
            {"id": "rule.s2", "version": "v1", "publishes": "s2", "requires": ["param.p1"], "role": "computation"},
            {"id": "rule.s3", "version": "v1", "publishes": "s3", "requires": [], "role": "computation"},
            # S4 has two rules (conflict)
            {"id": "rule.s4_winner", "version": "v1", "publishes": "s4", "requires": ["s1"], "role": "computation"},
            {"id": "rule.s4_loser", "version": "v1", "publishes": "s4", "requires": ["s2"], "role": "computation"},
            # Cycle rules
            {"id": "rule.cycle_a", "version": "v1", "publishes": "cycle_a", "requires": ["cycle_b"], "role": "computation"},
            {"id": "rule.cycle_b", "version": "v1", "publishes": "cycle_b", "requires": ["cycle_a"], "role": "computation"},
        ]

    def test_walk_npe_published(self) -> None:
        # A completed run where s1 is published
        records = [
            {"run_id": "run.1", "phase": "started", "workspace_revision": 10, "governance_pins": [], "adoption_pin": {"role": "adoption", "id": "p", "version": "v1"}},
            {
                "run_id": "run.1",
                "phase": "completed",
                "workspace_revision": 10,
                "governance_pins": [],
                "adoption_pin": {"role": "adoption", "id": "p", "version": "v1"},
                "stop_reason": "saturated",
                "dispositions": [
                    {"artifact_id": "rule.s1", "disposition": "published", "pins": [{"role": "input", "id": "fid.s2", "version": "v1"}, {"role": "input", "id": "fid.s3", "version": "v1"}], "finding_id": "fid.s1", "act_id": "act.1", "symbol": "s1"},
                    {"artifact_id": "rule.s2", "disposition": "published", "pins": [], "finding_id": "fid.s2", "act_id": "act.2", "symbol": "s2"},
                    {"artifact_id": "rule.s3", "disposition": "published", "pins": [], "finding_id": "fid.s3", "act_id": "act.3", "symbol": "s3"},
                ],
            }
        ]

        derived = {
            "fid.s1": {"id": "fid.s1", "symbol": "s1", "value": "100", "version": "v1", "pins": [{"role": "computation", "id": "rule.s1", "version": "v1"}, {"role": "input", "id": "fid.s2", "version": "v1"}, {"role": "input", "id": "fid.s3", "version": "v1"}]},
            "fid.s2": {"id": "fid.s2", "symbol": "s2", "value": "40", "version": "v1", "pins": [{"role": "computation", "id": "rule.s2", "version": "v1"}]},
            "fid.s3": {"id": "fid.s3", "symbol": "s3", "value": "60", "version": "v1", "pins": [{"role": "computation", "id": "rule.s3", "version": "v1"}]},
        }

        walk = walk_npe(
            run_id="run.1",
            symbol="s1",
            rules=self.rules,
            records=records,
            derived=derived,
        )

        self.assertEqual(walk["schema"], "npe-walk.v1")
        self.assertEqual(walk["run_id"], "run.1")
        self.assertEqual(walk["workspace_revision"], 10)
        
        root = walk["root"]
        self.assertEqual(root["node_id"], "s1")
        self.assertEqual(root["node_kind"], "published")
        self.assertEqual(root["finding_id"], "fid.s1")
        self.assertEqual(root["rule_references"], [{"id": "rule.s1", "version": "v1"}])
        
        children = {c["node_id"]: c for c in root["children"]}
        self.assertIn("s2", children)
        self.assertIn("s3", children)
        self.assertEqual(children["s2"]["node_kind"], "published")
        self.assertEqual(children["s3"]["node_kind"], "published")
        self.schemas.validate_declared(walk)

    def test_walk_npe_blocked(self) -> None:
        records = [
            {"run_id": "run.1", "phase": "started", "workspace_revision": 10, "governance_pins": [], "adoption_pin": {"role": "adoption", "id": "p", "version": "v1"}},
            {
                "run_id": "run.1",
                "phase": "completed",
                "workspace_revision": 10,
                "governance_pins": [],
                "adoption_pin": {"role": "adoption", "id": "p", "version": "v1"},
                "stop_reason": "saturated",
                "dispositions": [
                    {"artifact_id": "rule.s2", "disposition": "blocked", "pins": [], "code": "DEPENDENCY_ABSENT", "missing": ["param.p1"]},
                ],
            }
        ]

        walk = walk_npe(
            run_id="run.1",
            symbol="s2",
            rules=self.rules,
            records=records,
        )

        root = walk["root"]
        self.assertEqual(root["node_kind"], "blocked")
        self.assertEqual(root["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(root["unmet_references"], ["param.p1"])

    def test_walk_npe_inapplicable(self) -> None:
        records = [
            {"run_id": "run.1", "phase": "started", "workspace_revision": 10, "governance_pins": [], "adoption_pin": {"role": "adoption", "id": "p", "version": "v1"}},
            {
                "run_id": "run.1",
                "phase": "completed",
                "workspace_revision": 10,
                "governance_pins": [],
                "adoption_pin": {"role": "adoption", "id": "p", "version": "v1"},
                "stop_reason": "saturated",
                "dispositions": [
                    {"artifact_id": "rule.s3", "disposition": "inapplicable", "pins": [], "guard_result": False},
                ],
            }
        ]

        walk = walk_npe(
            run_id="run.1",
            symbol="s3",
            rules=self.rules,
            records=records,
        )

        root = walk["root"]
        self.assertEqual(root["node_kind"], "guard_inapplicable")

    def test_walk_npe_conflict_loser(self) -> None:
        records = [
            {"run_id": "run.1", "phase": "started", "workspace_revision": 10, "governance_pins": [], "adoption_pin": {"role": "adoption", "id": "p", "version": "v1"}},
            {
                "run_id": "run.1",
                "phase": "completed",
                "workspace_revision": 10,
                "governance_pins": [],
                "adoption_pin": {"role": "adoption", "id": "p", "version": "v1"},
                "stop_reason": "saturated",
                "dispositions": [
                    {"artifact_id": "rule.s4_winner", "disposition": "published", "pins": [{"role": "input", "id": "fid.s1", "version": "v1"}], "finding_id": "fid.s4", "act_id": "act.4", "symbol": "s4"},
                    {"artifact_id": "rule.s4_loser", "disposition": "inapplicable", "pins": [], "superseded_by": {"role": "package", "id": "rule.s4_winner", "version": "v1"}},
                    {"artifact_id": "rule.s1", "disposition": "published", "pins": [], "finding_id": "fid.s1", "act_id": "act.1", "symbol": "s1"},
                ],
            }
        ]

        derived = {
            "fid.s4": {"id": "fid.s4", "symbol": "s4", "value": "100", "version": "v1", "pins": [{"role": "computation", "id": "rule.s4_winner", "version": "v1"}, {"role": "input", "id": "fid.s1", "version": "v1"}]},
            "fid.s1": {"id": "fid.s1", "symbol": "s1", "value": "100", "version": "v1", "pins": [{"role": "computation", "id": "rule.s1", "version": "v1"}]},
        }

        walk = walk_npe(
            run_id="run.1",
            symbol="s4",
            rules=self.rules,
            records=records,
            derived=derived,
        )

        root = walk["root"]
        self.assertEqual(root["node_kind"], "published")
        self.assertEqual(len(root["rule_references"]), 2)
        # Winner and loser sorted by ID
        self.assertEqual(root["rule_references"][0]["id"], "rule.s4_loser")
        self.assertEqual(root["rule_references"][1]["id"], "rule.s4_winner")

    def test_walk_npe_no_disposition_recorded(self) -> None:
        records = [
            {"run_id": "run.2", "phase": "started", "workspace_revision": 12, "governance_pins": [], "adoption_pin": {"role": "adoption", "id": "p", "version": "v1"}},
            {"run_id": "run.2", "phase": "interrupted", "workspace_revision": 12, "governance_pins": [], "adoption_pin": {"role": "adoption", "id": "p", "version": "v1"}, "stop_reason": "interrupted", "dispositions": []}
        ]

        walk = walk_npe(
            run_id="run.2",
            symbol="s1",
            rules=self.rules,
            records=records,
        )

        root = walk["root"]
        self.assertEqual(root["node_kind"], "no_disposition_recorded")
        self.assertEqual(root["closing_phase"], "interrupted")

    def test_walk_npe_cycle_detection(self) -> None:
        records = [
            {"run_id": "run.1", "phase": "started", "workspace_revision": 10, "governance_pins": [], "adoption_pin": {"role": "adoption", "id": "p", "version": "v1"}},
            {
                "run_id": "run.1",
                "phase": "completed",
                "workspace_revision": 10,
                "governance_pins": [],
                "adoption_pin": {"role": "adoption", "id": "p", "version": "v1"},
                "stop_reason": "saturated",
                "dispositions": [
                    {"artifact_id": "rule.cycle_a", "disposition": "blocked", "pins": [], "code": "DEPENDENCY_ABSENT", "missing": ["cycle_b"]},
                    {"artifact_id": "rule.cycle_b", "disposition": "blocked", "pins": [], "code": "DEPENDENCY_ABSENT", "missing": ["cycle_a"]},
                ],
            }
        ]

        with self.assertRaises(CyclicDependencyError):
            walk_npe(
                run_id="run.1",
                symbol="cycle_a",
                rules=self.rules,
                records=records,
            )

    def test_walk_npe_memoization(self) -> None:
        # Diamond dependency graph: s1 depends on s2 and s3, both depend on s4.
        rules = [
            {"id": "rule.s1", "version": "v1", "publishes": "s1", "requires": ["s2", "s3"], "role": "computation"},
            {"id": "rule.s2", "version": "v1", "publishes": "s2", "requires": ["s4"], "role": "computation"},
            {"id": "rule.s3", "version": "v1", "publishes": "s3", "requires": ["s4"], "role": "computation"},
            {"id": "rule.s4", "version": "v1", "publishes": "s4", "requires": [], "role": "computation"},
        ]

        records = [
            {"run_id": "run.1", "phase": "started", "workspace_revision": 10, "governance_pins": [], "adoption_pin": {"role": "adoption", "id": "p", "version": "v1"}},
            {
                "run_id": "run.1",
                "phase": "completed",
                "workspace_revision": 10,
                "governance_pins": [],
                "adoption_pin": {"role": "adoption", "id": "p", "version": "v1"},
                "stop_reason": "saturated",
                "dispositions": [
                    {"artifact_id": "rule.s1", "disposition": "inapplicable", "pins": [], "guard_result": False},
                    {"artifact_id": "rule.s2", "disposition": "inapplicable", "pins": [], "guard_result": False},
                    {"artifact_id": "rule.s3", "disposition": "inapplicable", "pins": [], "guard_result": False},
                    {"artifact_id": "rule.s4", "disposition": "inapplicable", "pins": [], "guard_result": False},
                ],
            }
        ]

        walk = walk_npe(
            run_id="run.1",
            symbol="s1",
            rules=rules,
            records=records,
        )

        root = walk["root"]
        s2_node = next(c for c in root["children"] if c["node_id"] == "s2")
        s3_node = next(c for c in root["children"] if c["node_id"] == "s3")
        s4_under_s2 = s2_node["children"][0]
        s4_under_s3 = s3_node["children"][0]

        # Verify both sub-walks point to the identical memoized object reference
        self.assertIs(s4_under_s2, s4_under_s3)

    def test_walk_npe_run_scoped_selection(self) -> None:
        # Run 1: s2 is published
        # Run 2: s2 is blocked
        records = [
            {"run_id": "run.1", "phase": "started", "workspace_revision": 10, "governance_pins": [], "adoption_pin": {"role": "adoption", "id": "p", "version": "v1"}},
            {
                "run_id": "run.1",
                "phase": "completed",
                "workspace_revision": 10,
                "governance_pins": [],
                "adoption_pin": {"role": "adoption", "id": "p", "version": "v1"},
                "stop_reason": "saturated",
                "dispositions": [
                    {"artifact_id": "rule.s2", "disposition": "published", "pins": [], "finding_id": "fid.s2.r1", "act_id": "act.r1", "symbol": "s2"},
                ],
            },
            {"run_id": "run.2", "phase": "started", "workspace_revision": 11, "governance_pins": [], "adoption_pin": {"role": "adoption", "id": "p", "version": "v1"}},
            {
                "run_id": "run.2",
                "phase": "completed",
                "workspace_revision": 11,
                "governance_pins": [],
                "adoption_pin": {"role": "adoption", "id": "p", "version": "v1"},
                "stop_reason": "saturated",
                "dispositions": [
                    {"artifact_id": "rule.s2", "disposition": "blocked", "pins": [], "code": "DEPENDENCY_ABSENT", "missing": ["param.p1"]},
                ],
            }
        ]

        derived = {
            "fid.s2.r1": {"id": "fid.s2.r1", "symbol": "s2", "value": "40", "version": "v1", "pins": [{"role": "computation", "id": "rule.s2", "version": "v1"}]},
        }

        walk_r1 = walk_npe(
            run_id="run.1",
            symbol="s2",
            rules=self.rules,
            records=records,
            derived=derived,
        )
        self.assertEqual(walk_r1["root"]["node_kind"], "published")
        self.assertEqual(walk_r1["root"]["finding_id"], "fid.s2.r1")

        walk_r2 = walk_npe(
            run_id="run.2",
            symbol="s2",
            rules=self.rules,
            records=records,
        )
        self.assertEqual(walk_r2["root"]["node_kind"], "blocked")
        self.assertEqual(walk_r2["root"]["unmet_references"], ["param.p1"])


if __name__ == "__main__":
    unittest.main()
