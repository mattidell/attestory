"""Track 2 verification: closed-package validation as a contained outcome.

Each test reruns a round-2 successful attack against the production validator;
every one must be caught here. Containment is itself under test: an invalid
member is reported without aborting the checks on its neighbours.
"""

import copy
import json
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import validate_package

EXAMPLES = Path(__file__).resolve().parent.parent.parent / "packages" / "sample_data" / "derivation" / "examples"

_CITIZEN_FILES = [
    "rule-artifact.wages-line1a.json",
    "rule-artifact.tax-table-line16.json",
    "parameter.standard-deduction.json",
    "parameter.regular-tax-split.json",
    "parameter.tax-table-sample.json",
]


def _load(name: str) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads((EXAMPLES / name).read_text("utf-8"))
    return loaded


def _corpus(citizens: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    return {(c["id"], c["version"]): c for c in citizens}


class PackageValidationFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.package = _load("artifact-package.json")
        self.citizens = [_load(name) for name in _CITIZEN_FILES]

    def validate(self) -> Any:
        return validate_package(self.package, _corpus(self.citizens), self.schemas)

    def codes(self, result: Any) -> list[str]:
        return sorted(issue.code for issue in result.issues)


class ValidPackage(PackageValidationFixture):
    def test_closes_cleanly(self) -> None:
        result = self.validate()
        self.assertTrue(result.ok, msg=str(result.issues))
        self.assertEqual(result.output_owners["demo.form1040.line1a"], "demo.rule.wages-to-1040-line1a")
        self.assertEqual(result.output_owners["demo.form1040.line16"], "demo.rule.tax-table-line16")


class Parity1Containment(PackageValidationFixture):
    def test_one_invalid_member_is_contained_not_fatal(self) -> None:
        # Smuggle an unknown op into one rule; the schema rejects it, but the
        # rest of the package must still be validated (blast-radius = 1).
        bad = copy.deepcopy(self.citizens[0])
        bad["value"] = {"op": "multiply", "args": [1, 2]}
        self.citizens[0] = bad
        result = self.validate()
        self.assertFalse(result.ok)
        self.assertEqual(self.codes(result), ["MEMBER_SCHEMA_INVALID"])
        offending = result.issues[0]
        self.assertEqual(offending.member_id, "demo.rule.wages-to-1040-line1a")
        # The healthy member still produced its symbol.
        self.assertEqual(result.output_owners["demo.form1040.line16"], "demo.rule.tax-table-line16")


class Parity3OutputOwnership(PackageValidationFixture):
    def test_duplicate_output_rejected(self) -> None:
        rival = copy.deepcopy(_load("rule-artifact.tax-table-line16.json"))
        rival["id"] = "demo.rule.tax-table-line16-rival"
        self.citizens.append(rival)
        self.package["members"].append({"role": "computation", "id": rival["id"], "version": "v1"})
        result = self.validate()
        self.assertIn("OUTPUT_OWNERSHIP_CONFLICT", self.codes(result))

    def test_declared_conflict_semantics_permits_shared_symbol(self) -> None:
        rival = copy.deepcopy(_load("rule-artifact.tax-table-line16.json"))
        rival["id"] = "demo.rule.tax-table-line16-rival"
        self.citizens.append(rival)
        self.package["members"].append({"role": "computation", "id": rival["id"], "version": "v1"})
        self.package["conflict_semantics"] = [
            {"symbol": "demo.form1040.line16", "resolution": "first-guarded-wins"}
        ]
        result = self.validate()
        self.assertNotIn("OUTPUT_OWNERSHIP_CONFLICT", self.codes(result))


class Parity6Closure(PackageValidationFixture):
    def test_referenced_parameter_absent_from_package_rejected(self) -> None:
        # Drop the tax-table parameter that tax-table-line16 range_lookups.
        self.package["members"] = [
            m for m in self.package["members"] if m["id"] != "demo.parameter.tax-table-sample.2025"
        ]
        self.citizens = [c for c in self.citizens if c["id"] != "demo.parameter.tax-table-sample.2025"]
        result = self.validate()
        self.assertIn("CLOSURE_MISSING_PARAMETER", self.codes(result))


class Attack5YearIdentity(PackageValidationFixture):
    def test_member_scope_disagreement_rejected(self) -> None:
        # Identity never rides in the id: a member whose scope year differs
        # from the package is a mismatch, caught by content not by string.
        drifted = copy.deepcopy(self.citizens[0])
        drifted["scope"]["tax_year"] = 2024
        self.citizens[0] = drifted
        result = self.validate()
        self.assertIn("SCOPE_MISMATCH", self.codes(result))


class RoleAndPresence(PackageValidationFixture):
    def test_package_role_disagreeing_with_artifact_role_rejected(self) -> None:
        for member in self.package["members"]:
            if member["id"] == "demo.rule.wages-to-1040-line1a":
                member["role"] = "computation"  # artifact says field-mapping
        result = self.validate()
        self.assertIn("ROLE_MISMATCH", self.codes(result))

    def test_absent_member_version_reported(self) -> None:
        for member in self.package["members"]:
            if member["id"] == "demo.parameter.standard-deduction.2025":
                member["version"] = "v2"  # no such version in corpus
        result = self.validate()
        self.assertIn("MEMBER_ABSENT", self.codes(result))


if __name__ == "__main__":
    unittest.main()
