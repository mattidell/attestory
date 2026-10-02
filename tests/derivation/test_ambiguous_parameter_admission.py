"""Track 5e rejects only unversioned readers with ambiguous versions."""
from __future__ import annotations

import unittest
from copy import deepcopy
from packages.derivation.package_validation import _iter_parameter_and_table_refs, _rule_expression_nodes
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import package_instance_checksum, validate_package

from tests.derivation.test_exact_version_authority import (
    UnversionedParameterReference,
    _codes,
    _entries,
    _order,
    _parameter,
)
from tests.derivation.test_exact_version_authority import _resolve  # type: ignore[attr-defined]
from tests.derivation.test_bounded_nominee_selection_contract import (
    DERIVATION_PACKAGE, LINE2B, _content_corpus, _load,
)


class AmbiguousParameterAdmission(unittest.TestCase):
    def test_expression_walk_reaches_selection_paths_and_defaults(self) -> None:
        selection_rule = {
            "schema": "rule-artifact.v9",
            "when": True,
            "value": {"op": "parameter", "parameter_id": "demo.param.root"},
            "selection": {
                "paths": [{
                    "when": {"op": "range_lookup", "table_id": "demo.param.path-when", "key": "x", "value": 1},
                    "value": {"op": "bracket_fold", "table_id": "demo.param.path-value", "key": "x", "value": 1},
                }],
                "default": {
                    "when": {"op": "parameter", "parameter_id": "demo.param.default-when"},
                    "value": {"op": "parameter", "parameter_id": "demo.param.default-value"},
                },
            },
        }
        refs = {
            ref for expression in _rule_expression_nodes(selection_rule)
            for ref in _iter_parameter_and_table_refs(expression)
        }
        self.assertEqual(refs, {
            "demo.param.root", "demo.param.path-when", "demo.param.path-value",
            "demo.param.default-when", "demo.param.default-value",
        })

    def test_unversioned_parameter_reader_rejected_in_either_order(self) -> None:
        case = UnversionedParameterReference()
        for v1_first in (True, False):
            parts = [(case._rule(), "computation")] + [
                (citizen, "parameter") for citizen in _order(
                    _parameter(case.PARAM, "v1", "same"),
                    _parameter(case.PARAM, "v2", "same"),
                    v1_first=v1_first,
                )
            ]
            validation, _package = _resolve(parts, entrypoints=_entries(parts), bindings=[])
            self.assertFalse(validation.ok, validation.issues)
            self.assertIn("AMBIGUOUS_UNVERSIONED_PARAMETER", _codes(validation))

    def test_two_versions_are_allowed_when_no_unversioned_reader_exists(self) -> None:
        parts = [
            (_parameter("demo.param.unused", "v1", "same"), "parameter"),
            (_parameter("demo.param.unused", "v2", "same"), "parameter"),
        ]
        # Both citizens can coexist; the prohibition is attached to a reader.
        validation, _package = _resolve(parts, entrypoints=_entries(parts), bindings=[])
        self.assertTrue(validation.ok, validation.issues)

    def test_range_lookup_and_bracket_fold_reject_ambiguous_tables_through_admission(self) -> None:
        case = UnversionedParameterReference()
        for operation in ("range_lookup", "bracket_fold"):
            table_id = f"demo.param.admission-{operation}"
            rule = case._rule()
            rule["value"] = {"op": operation, "table_id": table_id, "key": 1, "value": 1}
            for v1_first in (True, False):
                parameters = _order(
                    _parameter(table_id, "v1", "same"),
                    _parameter(table_id, "v2", "same"),
                    v1_first=v1_first,
                )
                parts = [(rule, "computation"), *((param, "parameter") for param in parameters)]
                validation, _package = _resolve(parts, entrypoints=_entries(parts), bindings=[])
                self.assertFalse(validation.ok, validation.issues)
                self.assertIn("AMBIGUOUS_UNVERSIONED_PARAMETER", _codes(validation))

    def test_selection_path_and_default_expressions_reject_ambiguous_refs_after_valid_admission(self) -> None:
        for target in ("path_when", "path_value", "default_when", "default_value"):
            with self.subTest(target=target):
                line = _load(LINE2B)
                package = deepcopy(_load(DERIVATION_PACKAGE))
                corpus = _content_corpus()
                corpus[(line["id"], line["version"])] = line
                validation = validate_package(package, corpus, DerivationSchemas())
                self.assertTrue(validation.ok, validation.issues)

                param_id = f"demo.param.selection-{target}"
                param_members = [
                    _parameter(param_id, "v1", "same"),
                    _parameter(param_id, "v2", "same"),
                ]
                for citizen in param_members:
                    citizen["scope"] = dict(package["scope"])
                    corpus[(citizen["id"], citizen["version"])] = citizen
                    package["members"].append({
                        "role": "parameter", "schema": citizen["schema"],
                        "id": citizen["id"], "version": citizen["version"],
                    })
                if "parameter-declaration.v1" not in package["admitted_schemas"]:
                    package["admitted_schemas"].append("parameter-declaration.v1")

                expression = {"op": "parameter", "parameter_id": param_id}
                selection = line["selection"]
                if target == "path_when":
                    selection["paths"][0]["when"] = {"op": "all", "args": [selection["paths"][0]["when"], expression]}
                elif target == "path_value":
                    selection["paths"][0]["value"] = {"op": "add", "args": [selection["paths"][0]["value"], expression]}
                elif target == "default_when":
                    selection["default"]["when"] = expression
                else:
                    selection["default"]["value"] = {"op": "add", "args": [selection["default"]["value"], expression]}
                package.pop("package_checksum", None)
                package["package_checksum"] = package_instance_checksum(package)
                validation = validate_package(package, corpus, DerivationSchemas())
                self.assertIn("AMBIGUOUS_UNVERSIONED_PARAMETER", _codes(validation), validation.issues)
                # v9 deliberately excludes dynamic table/parameter readers
                # from its selected path and default grammar. Admission sees
                # the ambiguity at each nested expression while preserving
                # that independent contract refusal.
                self.assertEqual(
                    set(_codes(validation)),
                    {"AMBIGUOUS_UNVERSIONED_PARAMETER", "RULE_SELECTION_DYNAMIC_DEPENDENCY_INVALID"},
                    validation.issues,
                )
