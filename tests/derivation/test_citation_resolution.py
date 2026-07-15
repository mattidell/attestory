"""Track 5 structural, adoption-only citation resolution checks (ADR-0029)."""

import copy
import unittest
from typing import Any

from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import PackageValidation, validate_package
from packages.derivation.runner import InputFinding, RunContext, run


SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "demo"}
CITATION: dict[str, Any] = {
    "schema": "citation.v1", "id": "demo.citation", "version": "v1",
    "authority": {"family": "irs-form", "form_id": "1040", "tax_year": 2025},
}
RULE: dict[str, Any] = {
    "schema": "rule-artifact.v2", "id": "demo.rule", "version": "v1", "scope": SCOPE,
    "role": "computation", "requires": [], "pins": [], "when": True, "value": 7,
    "publishes": "demo.output", "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
    "citations": [{"id": "demo.citation", "version": "v1"}],
}
PACKAGE: dict[str, Any] = {
    "schema": "artifact-package.v2", "id": "demo.package", "version": "v1", "scope": SCOPE,
    "admitted_schemas": ["rule-artifact.v2", "citation.v1"],
    "members": [
        {"role": "computation", "schema": "rule-artifact.v2", "id": "demo.rule", "version": "v1"},
        {"role": "citation", "schema": "citation.v1", "id": "demo.citation", "version": "v1"},
    ],
    "input_bindings": [], "entrypoints": [{"id": "demo.rule", "version": "v1"}],
    "composition_obligations": [], "package_checksum": "0" * 64,
}


class CitationResolution(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()

    def validate(
        self,
        *,
        package: dict[str, Any] | None = None,
        rule: dict[str, Any] | None = None,
        citation: dict[str, Any] | None = None,
    ) -> PackageValidation:
        package = copy.deepcopy(PACKAGE if package is None else package)
        rule = copy.deepcopy(RULE if rule is None else rule)
        citation = copy.deepcopy(CITATION if citation is None else citation)
        corpus: dict[tuple[str, str], dict[str, Any]] = {
            (str(rule["id"]), str(rule["version"])): rule,
            (str(citation["id"]), str(citation["version"])): citation,
        }
        return validate_package(package, corpus, self.schemas)

    def test_resolves_exact_citation_member_structurally(self) -> None:
        result = self.validate()
        self.assertTrue(result.ok, result.issues)
        self.assertEqual(result.citation_resolutions[0].status, "statically_resolved")

    def test_rejects_rule_attachment_with_wrong_citation_version(self) -> None:
        rule = copy.deepcopy(RULE)
        rule["citations"][0]["version"] = "v2"
        result = self.validate(rule=rule)
        self.assertIn("CITATION_ABSENT", {issue.code for issue in result.issues})

    def test_citation_metadata_does_not_change_runner_output(self) -> None:
        without_citation = copy.deepcopy(RULE)
        del without_citation["citations"]
        def context(rule: dict[str, Any]) -> RunContext:
            return RunContext(
                run_id="demo.citation.run", rules=[rule], parameters={}, canon={},
                inputs=[], sources=[],
                adoption_pin={"role": "adoption", "id": "demo.package", "version": "v1"},
                governance_pins=[],
            )

        with_citation = run(context(RULE), self.schemas).publications[0].finding["value"]
        without_citation_value = run(context(without_citation), self.schemas).publications[0].finding["value"]
        self.assertEqual(with_citation, without_citation_value)
