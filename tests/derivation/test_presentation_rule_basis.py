from __future__ import annotations

import unittest

from packages.derivation.presentation_projection import PresentationModelError, _exact_rule_basis


class TestExactRuleBasis(unittest.TestCase):
    def test_loads_all_four_groups_from_exact_pinned_version(self) -> None:
        older = {"id": "demo.rule", "version": "v1", "publishes": "demo.value", "basis": {"said": ["old"], "derived": [], "assumed": [], "left_with_person": []}}
        pinned = {"id": "demo.rule", "version": "v2", "publishes": "demo.value", "basis": {"said": ["new"], "derived": ["derived"], "assumed": ["assumed"], "left_with_person": ["left"]}}
        finding = {"id": "demo.finding", "pins": [{"role": "computation", "id": "demo.rule", "version": "v2"}]}
        basis, pin = _exact_rule_basis(finding, resolved_members=[older, pinned])
        self.assertEqual(pin["version"], "v2")
        self.assertEqual(basis, pinned["basis"])

    def test_unknown_resolved_rule_and_no_basis(self) -> None:
        rule = {"id": "demo.unfamiliar", "version": "v9", "publishes": "demo.value"}
        finding = {"id": "demo.finding", "pins": [{"role": "computation", "id": "demo.unfamiliar", "version": "v9"}]}
        basis, pin = _exact_rule_basis(finding, resolved_members=[rule])
        self.assertIsNone(basis)
        self.assertEqual(pin["id"], "demo.unfamiliar")

    def test_missing_or_ambiguous_exact_producer_refuses(self) -> None:
        finding = {"id": "demo.finding", "pins": [{"role": "computation", "id": "demo.rule", "version": "v1"}]}
        with self.assertRaises(PresentationModelError):
            _exact_rule_basis(finding, resolved_members=[])
        duplicated = [
            {"id": "demo.rule", "version": "v1", "publishes": "demo.value"},
            {"id": "demo.rule", "version": "v1", "publishes": "demo.value"},
        ]
        with self.assertRaises(PresentationModelError):
            _exact_rule_basis(finding, resolved_members=duplicated)


if __name__ == "__main__":
    unittest.main()
