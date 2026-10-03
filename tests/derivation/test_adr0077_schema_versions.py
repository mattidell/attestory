"""ADR 0077 "Schemas": the four successor versions and only what they add.

``rule-artifact.v13`` copies v12 and adds ``shared_key_count``, an optional
``basis``, and ``selection`` (with ``reads_subject_results`` and
``member_fact_types``) as an alternative to ``value``. ``artifact-package.v35``
copies v34 and admits v13. ``derived-finding.v3`` and
``derivation-record.v10`` copy their predecessors and add ``derived`` to the
pin ``origin`` enum. Every predecessor keeps rejecting what it rejected.
"""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.loader import DerivationSchemas
from packages.kernel.schema_registry import SchemaValidationError

SCHEMA_DIR = Path(__file__).resolve().parents[2] / "packages" / "schemas" / "derivation"
SCOPE = {"tax_year": 2025, "jurisdiction": "us", "family": "demo-student-loan"}
SUBJECT = {"id": "demo.tax.adr0077.inclusion", "version": "v1"}
BASIS = {
    "said": ["demo said sentence"],
    "derived": ["demo derived sentence"],
    "assumed": ["demo assumed sentence"],
    "left_with_person": ["demo responsibility sentence"],
}


def _rule(schema: str = "rule-artifact.v13", **overrides: Any) -> dict[str, Any]:
    rule: dict[str, Any] = {
        "schema": schema,
        "id": "demo.rule.adr0077.count",
        "version": "v1",
        "scope": dict(SCOPE),
        "subject": dict(SUBJECT),
        "role": "computation",
        "requires": [],
        "pins": [],
        "when": True,
        "value": {"op": "shared_key_count", "fact_type": "demo.tax.adr0077.financing", "key": "borrowing"},
        "publishes": "demo.tax.adr0077.count",
        "blocked": {"code": "DEPENDENCY_INVALID", "missing": []},
    }
    rule.update(overrides)
    return rule


def _path(path_id: str, **overrides: Any) -> dict[str, Any]:
    path: dict[str, Any] = {
        "id": path_id,
        "activity": {
            "kind": "source_nonempty",
            "member_fact_types": [{"id": f"demo.tax.adr0077.{path_id}", "version": "v1"}],
        },
        "reads_subject_results": [
            {"symbol": f"demo.tax.adr0077.{path_id}-result", "subject": {"id": "demo.tax.adr0077.box1", "version": "v1"}},
        ],
        "requires": [],
        "pins": [],
        "when": True,
        "value": 1,
    }
    path.update(overrides)
    return path


def _selection_rule() -> dict[str, Any]:
    rule = _rule()
    rule.pop("subject")
    rule.pop("value")
    rule["selection"] = {
        "mode": "exclusive_presence",
        "conflict": "refuse",
        "paths": [_path("old"), _path("new")],
        "default": {
            "id": "neither",
            "reads_subject_results": [],
            "requires": [],
            "pins": [],
            "when": True,
            "value": 0,
        },
        "refusal": {"code": "DEPENDENCY_INVALID", "missing": ["demo-both-present"], "pins": []},
    }
    return rule


class RuleArtifactV13(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()

    def test_shared_key_count_is_valid_on_v13_and_rejected_on_v12(self) -> None:
        self.assertEqual(self.schemas.validate_declared(_rule()), "rule-artifact.v13")
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate_declared(_rule("rule-artifact.v12"))

    def test_shared_key_count_node_carries_nothing_else(self) -> None:
        for extra in ({"links": "demo.tax.adr0077.financing"}, {"empty": 0}):
            value = {"op": "shared_key_count", "fact_type": "demo.tax.adr0077.financing", "key": "borrowing", **extra}
            with self.subTest(extra=extra), self.assertRaises(SchemaValidationError):
                self.schemas.validate_declared(_rule(value=value))
        for missing in ("fact_type", "key"):
            value = {"op": "shared_key_count", "fact_type": "demo.tax.adr0077.financing", "key": "borrowing"}
            value.pop(missing)
            with self.subTest(missing=missing), self.assertRaises(SchemaValidationError):
                self.schemas.validate_declared(_rule(value=value))

    def test_basis_requires_four_groups_of_non_empty_strings(self) -> None:
        self.schemas.validate_declared(_rule(basis=copy.deepcopy(BASIS)))
        empty_groups: dict[str, list[str]] = {key: [] for key in BASIS}
        self.schemas.validate_declared(_rule(basis=empty_groups))
        for key in BASIS:
            missing = copy.deepcopy(BASIS)
            missing.pop(key)
            with self.subTest(missing=key), self.assertRaises(SchemaValidationError):
                self.schemas.validate_declared(_rule(basis=missing))
            blank = copy.deepcopy(BASIS)
            blank[key] = [""]
            with self.subTest(blank=key), self.assertRaises(SchemaValidationError):
                self.schemas.validate_declared(_rule(basis=blank))
            non_string: dict[str, Any] = copy.deepcopy(BASIS)
            non_string[key] = [{"finding": "demo"}]
            with self.subTest(non_string=key), self.assertRaises(SchemaValidationError):
                self.schemas.validate_declared(_rule(basis=non_string))
        extra = {**copy.deepcopy(BASIS), "pins": ["demo"]}
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate_declared(_rule(basis=extra))
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate_declared(_rule("rule-artifact.v12", value=1, basis=copy.deepcopy(BASIS)))

    def test_selection_is_an_alternative_to_value(self) -> None:
        selection_rule = _selection_rule()
        self.assertEqual(self.schemas.validate_declared(selection_rule), "rule-artifact.v13")
        both = copy.deepcopy(selection_rule)
        both["value"] = 1
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate_declared(both)
        neither = copy.deepcopy(selection_rule)
        neither.pop("selection")
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate_declared(neither)
        aggregation = copy.deepcopy(selection_rule)
        aggregation["aggregation"] = {"mode": "sum"}
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate_declared(aggregation)

    def test_paths_and_default_carry_reads_subject_results(self) -> None:
        for where in ("path", "default"):
            rule = _selection_rule()
            target = rule["selection"]["paths"][0] if where == "path" else rule["selection"]["default"]
            target.pop("reads_subject_results")
            with self.subTest(where=where), self.assertRaises(SchemaValidationError):
                self.schemas.validate_declared(rule)
        rule = _selection_rule()
        rule["selection"]["paths"][0]["reads_subject_results"][0]["field"] = "value"
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate_declared(rule)
        rule = _selection_rule()
        rule["reads_subject_results"] = []
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate_declared(rule)

    def test_source_activity_names_one_member_or_member_list(self) -> None:
        one = _selection_rule()
        one["selection"]["paths"][0]["activity"] = {
            "kind": "source_nonempty",
            "member_fact_type": {"id": "demo.tax.adr0077.old", "version": "v1"},
            "source_family": {"id": "demo.family.adr0077.old", "version": "v1"},
        }
        self.schemas.validate_declared(one)
        both = copy.deepcopy(one)
        both["selection"]["paths"][0]["activity"]["member_fact_types"] = [{"id": "demo.tax.adr0077.old", "version": "v1"}]
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate_declared(both)
        neither = copy.deepcopy(one)
        neither["selection"]["paths"][0]["activity"].pop("member_fact_type")
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate_declared(neither)
        empty = _selection_rule()
        empty["selection"]["paths"][0]["activity"]["member_fact_types"] = []
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate_declared(empty)

    def test_selection_mode_and_conflict_are_closed(self) -> None:
        for field, value in (("mode", "first_present"), ("conflict", "prefer_new")):
            rule = _selection_rule()
            rule["selection"][field] = value
            with self.subTest(field=field), self.assertRaises(SchemaValidationError):
                self.schemas.validate_declared(rule)
        rule = _selection_rule()
        rule["selection"]["paths"] = rule["selection"]["paths"][:1]
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate_declared(rule)

    def test_declared_pin_origins_are_unchanged(self) -> None:
        pin = {"role": "input", "id": "demo.tax.adr0077.x", "version": "v1", "origin": "derived"}
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate_declared(_rule(pins=[pin]))

    def test_joined_still_needs_subject(self) -> None:
        rule = _rule(value=1, joined={"id": "demo.tax.adr0077.financing", "version": "v1"},
                     direction="joined_contains_subject")
        self.schemas.validate_declared(rule)
        rule.pop("subject")
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate_declared(rule)

    def test_v13_copies_v12_otherwise(self) -> None:
        v12 = json.loads((SCHEMA_DIR / "rule-artifact.v12.schema.json").read_text("utf-8"))
        v13 = json.loads((SCHEMA_DIR / "rule-artifact.v13.schema.json").read_text("utf-8"))
        added_properties = {"selection", "basis"}
        self.assertEqual(set(v13["properties"]) - set(v12["properties"]), added_properties)
        for name, body in v12["properties"].items():
            if name != "schema":
                self.assertEqual(v13["properties"][name], body, name)
        self.assertEqual(set(v12["required"]) - set(v13["required"]), {"subject", "value"})
        self.assertEqual(v13["$defs"]["pin"], v12["$defs"]["pin"])
        v12_ops = [branch for branch in v12["$defs"]["expr"]["oneOf"]]
        self.assertEqual(v13["$defs"]["expr"]["oneOf"][: len(v12_ops)], v12_ops)
        self.assertEqual(
            v13["$defs"]["expr"]["oneOf"][len(v12_ops)]["properties"]["op"],
            {"const": "shared_key_count"},
        )
        self.assertEqual(len(v13["$defs"]["expr"]["oneOf"]), len(v12_ops) + 1)
        self.assertNotIn("aggregation", v13["$defs"])


class ArtifactPackageV35(unittest.TestCase):
    def _package(self, schema: str, member_schema: str) -> dict[str, Any]:
        return {
            "schema": schema,
            "id": "demo.package.adr0077",
            "version": "v1",
            "scope": dict(SCOPE),
            "admitted_schemas": [member_schema],
            "members": [{"role": "computation", "schema": member_schema, "id": "demo.rule.adr0077.count", "version": "v1"}],
            "input_bindings": [],
            "entrypoints": [{"id": "demo.rule.adr0077.count", "version": "v1"}],
            "composition_obligations": [],
            "package_checksum": "0" * 64,
        }

    def test_v35_admits_v13_and_v12(self) -> None:
        schemas = DerivationSchemas()
        for member in ("rule-artifact.v13", "rule-artifact.v12", "rule-artifact.v6"):
            with self.subTest(member=member):
                schemas.validate_declared(self._package("artifact-package.v35", member))

    def test_v34_does_not_admit_v13(self) -> None:
        with self.assertRaises(SchemaValidationError):
            DerivationSchemas().validate_declared(self._package("artifact-package.v34", "rule-artifact.v13"))

    def test_v13_member_must_be_admitted(self) -> None:
        package = self._package("artifact-package.v35", "rule-artifact.v13")
        package["admitted_schemas"] = ["rule-artifact.v12"]
        with self.assertRaises(SchemaValidationError):
            DerivationSchemas().validate_declared(package)

    def test_v35_copies_v34_admissions(self) -> None:
        v34 = json.loads((SCHEMA_DIR / "artifact-package.v34.schema.json").read_text("utf-8"))
        v35 = json.loads((SCHEMA_DIR / "artifact-package.v35.schema.json").read_text("utf-8"))
        for path in (("$defs", "member", "properties", "schema", "enum"),
                     ("properties", "admitted_schemas", "items", "enum")):
            old: Any = v34
            new: Any = v35
            for key in path:
                old = old[key]
                new = new[key]
            self.assertEqual(new, [*old, "rule-artifact.v13"])
        self.assertEqual(v35["allOf"][:-1], v34["allOf"])


class DerivedEntryPinSuccessors(unittest.TestCase):
    def _finding(self, schema: str, version: str, origin: str) -> dict[str, Any]:
        return {
            "schema": schema,
            "id": "demo.finding.adr0077.line21",
            "symbol": "demo.tax.adr0077.line21",
            "value": "2500",
            "version": version,
            "pins": [
                {"role": "computation", "id": "demo.rule.adr0077.worksheet", "version": "v1"},
                {"role": "input", "id": "demo.finding.adr0077.statement", "version": "v2", "origin": origin},
            ],
        }

    def test_derived_finding_v3_admits_derived_origin_and_v2_does_not(self) -> None:
        schemas = DerivationSchemas()
        schemas.validate_declared(self._finding("derived-finding.v3", "v3", "derived"))
        schemas.validate_declared(self._finding("derived-finding.v3", "v3", "assertion"))
        with self.assertRaises(SchemaValidationError):
            schemas.validate_declared(self._finding("derived-finding.v2", "v2", "derived"))
        with self.assertRaises(SchemaValidationError):
            schemas.validate_declared(self._finding("derived-finding.v3", "v3", "inferred"))

    def test_derived_finding_v3_copies_v2_otherwise(self) -> None:
        v2 = json.loads((SCHEMA_DIR / "derived-finding.v2.schema.json").read_text("utf-8"))
        v3 = json.loads((SCHEMA_DIR / "derived-finding.v3.schema.json").read_text("utf-8"))
        v2["$defs"]["pin"]["properties"]["origin"]["enum"].append("derived")
        for key in ("$id", "title", "description"):
            v2.pop(key)
            v3.pop(key)
        v2["properties"]["schema"]["const"] = "derived-finding.v3"
        v2["properties"]["version"]["const"] = "v3"
        self.assertEqual(v3, v2)

    def _record(self, schema: str, origin: str) -> dict[str, Any]:
        record = {
            "schema": schema,
            "record_id": "demo.record.adr0077.completed",
            "run_id": "demo.run.adr0077",
            "phase": "completed",
            "workspace_revision": 3,
            "governance_pins": [{"role": "governance", "id": "demo.governance.adr0077", "version": "v1"}],
            "adoption_pin": {"role": "adoption", "id": "demo.package.adr0077", "version": "v1"},
            "stop_reason": "saturated",
            "dispositions": [{
                "artifact_id": "demo.rule.adr0077.worksheet",
                "disposition": "blocked",
                "code": "DEPENDENCY_INVALID",
                "missing": ["demo-both-present"],
                "pins": [{"role": "input", "id": "demo.finding.adr0077.statement", "version": "v2", "origin": origin}],
            }],
        }
        return record

    def test_derivation_record_v10_admits_derived_origin_and_v9_does_not(self) -> None:
        schemas = DerivationSchemas()
        schemas.validate_declared(self._record("derivation-record.v9", "assertion"))
        schemas.validate_declared(self._record("derivation-record.v10", "assertion"))
        schemas.validate_declared(self._record("derivation-record.v10", "derived"))
        with self.assertRaises(SchemaValidationError):
            schemas.validate_declared(self._record("derivation-record.v9", "derived"))

    def test_derivation_record_v10_copies_v9_otherwise(self) -> None:
        v9 = json.loads((SCHEMA_DIR / "derivation-record.v9.schema.json").read_text("utf-8"))
        v10 = json.loads((SCHEMA_DIR / "derivation-record.v10.schema.json").read_text("utf-8"))
        v9["$defs"]["pin"]["properties"]["origin"]["enum"].append("derived")
        for key in ("$id", "title", "description"):
            v9.pop(key)
            v10.pop(key)
        v9["properties"]["schema"]["const"] = "derivation-record.v10"
        self.assertEqual(v10, v9)


if __name__ == "__main__":
    unittest.main()
