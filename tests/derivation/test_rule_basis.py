"""ADR 0077 Part 2: a rule's declared basis, and a reader that reaches it.

The basis lives on the rule. A published finding pins its producing rule
(role, id, version); a reader loads the adopted rule at that id and version
and shows ``said`` and ``derived`` beside the finding's input pins, and
``assumed`` and ``left_with_person`` with no pin. Package validation accepts
the four-group shape without judging the sentences, and requires a non-empty
``assumed`` and ``left_with_person`` on the rule that can publish
``plain-case-supported``.
"""

from __future__ import annotations

import copy
import unittest
from typing import Any, Iterable, Mapping

from packages.derivation.live import _resolved_run_material
from tests.derivation.test_shared_key_count import (
    BASIS,
    CONCLUSION_DEMO,
    PLAIN,
    STATEMENT_RULE,
    SUPPORT_DEMO,
    SUPPORT_RULE,
    _Graph,
    _rule,
    both_runners,
    chain_parts,
    codes,
    marshal,
    plain,
    validate,
    world,
)

_RULE_PIN_ROLES = {"computation", "applicability", "field-mapping", "cross-form-bridge"}


def rule_for(finding: Mapping[str, Any], adopted_rules: Iterable[Mapping[str, Any]]) -> Mapping[str, Any]:
    """The adopted rule a finding's rule pin names, by exact id and version."""
    rule_pins = [pin for pin in finding["pins"] if pin.get("role") in _RULE_PIN_ROLES]
    if len(rule_pins) != 1:
        raise AssertionError(f"expected one rule pin, got {rule_pins}")
    pin = rule_pins[0]
    matches = [
        rule for rule in adopted_rules
        if rule.get("id") == pin["id"] and rule.get("version") == pin["version"]
    ]
    if len(matches) != 1:
        raise AssertionError(f"rule pin {pin} names {len(matches)} adopted rules")
    return matches[0]


def account(finding: Mapping[str, Any], adopted_rules: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """What a reader shows for one published result.

    ``said`` and ``derived`` sit beside the input pins that evidence them;
    ``assumed`` and ``left_with_person`` have no pin and no finding. A rule
    without ``basis`` gives nothing for the four groups.
    """
    rule = rule_for(finding, adopted_rules)
    basis = rule.get("basis")
    shown: dict[str, Any] = {
        "value": finding["value"],
        "rule": (rule["id"], rule["version"]),
        "input_pins": sorted(pin["id"] for pin in finding["pins"] if pin.get("role") == "input"),
    }
    if isinstance(basis, dict):
        shown.update({group: list(basis[group]) for group in ("said", "derived", "assumed", "left_with_person")})
    return shown


class BasisValidation(unittest.TestCase):
    def _statement(self, parts: list[tuple[dict[str, Any], str]]) -> dict[str, Any]:
        return next(citizen for citizen, _ in parts if citizen["id"] == STATEMENT_RULE)

    def test_declared_basis_validates_without_judging_sentences(self) -> None:
        _package, validation = validate(chain_parts())
        self.assertTrue(validation.ok, validation.issues)
        odd = copy.deepcopy(BASIS)
        odd["said"] = ["Anything at all; the validator does not check truth."]
        odd["derived"] = []
        _package, validation = validate(chain_parts(basis=odd))
        self.assertTrue(validation.ok, validation.issues)

    def test_plain_case_rule_must_declare_basis(self) -> None:
        parts = chain_parts()
        self._statement(parts).pop("basis")
        _package, validation = validate(parts)
        self.assertIn("RULE_BASIS_REQUIRED", codes(validation))
        self.assertEqual(
            [issue.member_id for issue in validation.issues if issue.code == "RULE_BASIS_REQUIRED"],
            [STATEMENT_RULE],
        )

    def test_plain_case_rule_needs_assumed_and_left_with_person(self) -> None:
        for group in ("assumed", "left_with_person"):
            basis = copy.deepcopy(BASIS)
            basis[group] = []
            with self.subTest(group=group):
                _package, validation = validate(chain_parts(basis=basis))
                self.assertIn("RULE_BASIS_REQUIRED", codes(validation))

    def test_a_category_literal_plain_case_counts_too(self) -> None:
        parts = chain_parts()
        statement = self._statement(parts)
        statement.pop("basis")
        statement["value"]["then"] = {
            "op": "category_literal", "fact_type": {"id": "demo.tax.skc.conclusion", "version": "v1"},
            "value": PLAIN,
        }
        _package, validation = validate(parts)
        self.assertIn("RULE_BASIS_REQUIRED", codes(validation))

    def test_a_v12_rule_cannot_publish_plain_case_without_a_basis_field(self) -> None:
        parts = chain_parts()
        statement = self._statement(parts)
        statement.pop("basis")
        statement["schema"] = "rule-artifact.v12"
        _package, validation = validate(parts)
        self.assertIn("RULE_BASIS_REQUIRED", codes(validation))

    def test_basis_is_optional_elsewhere_and_allowed_on_a_return_level_rule(self) -> None:
        parts = chain_parts()
        support = next(citizen for citizen, _ in parts if citizen["id"] == SUPPORT_RULE)
        self.assertNotIn("basis", support)
        constant = _rule("demo.rule.skc.return-level-basis", subject=None,
                         publishes="demo.tax.skc.return-level-basis", value=1)
        constant["basis"] = {"said": [], "derived": [], "assumed": [], "left_with_person": []}
        parts.append((constant, "computation"))
        _package, validation = validate(parts)
        self.assertTrue(validation.ok, validation.issues)


class BasisReader(unittest.TestCase):
    def test_reader_reaches_basis_from_a_published_result_through_the_rule_pin(self) -> None:
        parts = chain_parts()
        package, validation = validate(parts)
        self.assertTrue(validation.ok, validation.issues)
        adopted_rules = _resolved_run_material(_Graph(list(validation.resolved_members), package))[0]
        state, current = world(plain())
        forward, reference = both_runners(marshal(parts, state, current))
        accounts = []
        for result in (forward, reference):
            finding = next(p.finding for p in result.publications if p.finding["symbol"] == CONCLUSION_DEMO)
            self.assertEqual(finding["value"], PLAIN)
            shown = account(finding, adopted_rules)
            self.assertEqual(shown["rule"], (STATEMENT_RULE, "v1"))
            for group in ("said", "derived", "assumed", "left_with_person"):
                self.assertEqual(shown[group], BASIS[group])
            # The pins evidence what was said and derived; the assumed and
            # left-with-person groups are not findings and have no pin.
            self.assertIn("demo.finding.box.demo-stmt", shown["input_pins"])
            self.assertIn("demo.finding.inclusion.demo-stmt.demo-loan", shown["input_pins"])
            for sentence in BASIS["assumed"] + BASIS["left_with_person"]:
                self.assertNotIn(sentence, [pin["id"] for pin in finding["pins"]])
            self.assertNotIn("basis", finding)
            accounts.append(shown)
        self.assertEqual(accounts[0], accounts[1])

    def test_a_rule_without_basis_gives_the_reader_nothing_for_the_groups(self) -> None:
        parts = chain_parts()
        package, validation = validate(parts)
        adopted_rules = _resolved_run_material(_Graph(list(validation.resolved_members), package))[0]
        state, current = world(plain())
        forward, _reference = both_runners(marshal(parts, state, current))
        finding = next(p.finding for p in forward.publications if p.finding["symbol"] == SUPPORT_DEMO)
        shown = account(finding, adopted_rules)
        self.assertEqual(shown["rule"], (SUPPORT_RULE, "v1"))
        for group in ("said", "derived", "assumed", "left_with_person"):
            self.assertNotIn(group, shown)


if __name__ == "__main__":
    unittest.main()
