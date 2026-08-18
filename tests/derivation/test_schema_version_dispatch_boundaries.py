"""Track 1: fail-loud semantic version boundaries (ADR-0066 Decision 7)."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from packages.derivation.loader import DERIVATION_SCHEMA_DIR, DerivationSchemas, TAX_SCHEMA_DIR
from packages.derivation.package_validation import validate_package
from packages.derivation.presentation_projection import (
    PRESENTATION_MODEL_VERSION,
    PresentationModelError,
    build_presentation_model,
    validate_presentation_model,
)
from packages.derivation.runner import Publication
from packages.kernel.findings import EvidenceLifecycle, FindingState
from packages.kernel.schema_registry import KERNEL_SCHEMA_DIR, SchemaRegistryError, write_manifest

REPO = Path(__file__).resolve().parent.parent.parent
CONTENT = REPO / "packages" / "content" / "tax" / "2025"
CORE_PACKAGE = CONTENT / "package.core-calculations.v31.json"

UNSUPPORTED_SCHEMA = "unsupported-semantic.v1"
PROBE_PACKAGE_SCHEMA = "artifact-package.probe-admit-unsupported.v1"
FIELD_V99 = "form-field.v99"
ATTACHMENT_V99 = "attachment-rule.v99"

FIELD = {
    "schema": "form-field.v3",
    "id": "demo.field.line-x",
    "version": "v1",
    "form": {"authority": "IRS", "form_id": "1040", "tax_year": 2025, "jurisdiction": "US-federal"},
    "line": "x",
    "label": "Demo line",
    "description": "A synthetic demo field for unit-level projector tests.",
    "binds_symbol": "demo.symbol.line-x",
    "citation": {"id": "demo.citation.line-x", "version": "v1"},
    "dispositions": {
        "published_value": {"render": "{value}", "explain": "e"},
        "computed_zero": {"render": "0", "explain": "e"},
        "closure_backed_zero": {"render": "0", "explain": "e"},
        "blocked": {"render": "", "explain": "e", "codes": ["DEPENDENCY_ABSENT"]},
        "guard_inapplicable": {"render": "", "explain": "e"},
    },
}

RULE = {"id": "demo.rule.line-x", "schema": "rule-artifact.v2", "publishes": "demo.symbol.line-x"}

UNRELATED = {
    "schema": "bundle.v2",
    "id": "demo.bundle.unrelated",
    "version": "v1",
    "fact_types": [],
}

ATTACHMENT_V6 = {
    "schema": "attachment-rule.v6",
    "id": "demo.rule.attachment.v6",
    "version": "v1",
    "title": "Demo attachment",
    "publishes": "demo.symbol.attachment",
    "itemizations": [
        {
            "part_id": "part-a",
            "label": "Part A",
            "tie_out": {"line_symbol": "demo.symbol.line-x"},
            "adjustment_rows": [],
        }
    ],
}


def _load(path: Path) -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads(path.read_text("utf-8"))
    return loaded


def _corpus(citizens: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    return {(c["id"], c["version"]): c for c in citizens}


def _finding(finding_id: str, symbol: str, value: str, pins: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema": "derived-finding.v2",
        "id": finding_id,
        "symbol": symbol,
        "value": value,
        "version": "v2",
        "pins": pins,
    }


def _state(
    findings: dict[str, dict[str, Any]],
    evidence: dict[str, EvidenceLifecycle] | None = None,
) -> FindingState:
    return FindingState(findings=findings, evidence=evidence or {})


def _published_field_model_args() -> dict[str, Any]:
    raw = {
        "schema": "finding.v1",
        "id": "demo.raw.a",
        "fact_id": "demo.fact.a",
        "value": 7,
        "basis": "attested",
        "evidence_ids": ["demo.evidence.a"],
    }
    state = _state(
        {"demo.raw.a": raw},
        {
            "demo.evidence.a": EvidenceLifecycle(
                evidence={
                    "schema": "evidence.v1",
                    "id": "demo.evidence.a",
                    "kind": "demo.statement.x",
                    "label": "Demo source A",
                    "content": {},
                },
                status="current",
            )
        },
    )
    finding = _finding(
        "demo.derived.x",
        "demo.symbol.line-x",
        "7",
        [{"role": "input", "id": "demo.raw.a", "version": "v1"}],
    )
    row = {
        "artifact_id": "demo.rule.line-x",
        "disposition": "published",
        "finding_id": "demo.derived.x",
        "symbol": "demo.symbol.line-x",
        "pins": finding["pins"],
    }
    return {
        "run_id": "demo.run",
        "resolved_members": [FIELD, RULE],
        "state": state,
        "publications": [Publication(act={}, finding=finding)],
        "dispositions": [row],
    }


def _write_json(path: Path, document: dict[str, Any]) -> None:
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")


def _write_probe_registry(directory: Path) -> None:
    _write_json(
        directory / f"{UNSUPPORTED_SCHEMA}.schema.json",
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": f"derivation/{UNSUPPORTED_SCHEMA}",
            "title": "Synthetic unsupported semantic schema for Track 1",
            "type": "object",
            "additionalProperties": True,
            "required": ["schema", "id", "version"],
            "properties": {
                "schema": {"const": UNSUPPORTED_SCHEMA},
                "id": {"type": "string"},
                "version": {"type": "string"},
            },
        },
    )
    _write_json(
        directory / f"{PROBE_PACKAGE_SCHEMA}.schema.json",
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": f"derivation/{PROBE_PACKAGE_SCHEMA}",
            "title": "Temporary package schema that admits unsupported-semantic.v1",
            "type": "object",
            "additionalProperties": False,
            "required": ["schema", "id", "version", "scope", "admitted_schemas", "members"],
            "properties": {
                "schema": {"const": PROBE_PACKAGE_SCHEMA},
                "id": {"type": "string"},
                "version": {"type": "string"},
                "scope": {"type": "object"},
                "admitted_schemas": {
                    "type": "array",
                    "minItems": 1,
                    "uniqueItems": True,
                    "items": {"enum": [UNSUPPORTED_SCHEMA]},
                },
                "members": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["role", "id", "version"],
                        "properties": {
                            "role": {"type": "string"},
                            "id": {"type": "string"},
                            "version": {"type": "string"},
                        },
                    },
                },
            },
        },
    )
    write_manifest(directory)


def _extended_schemas(tmp: Path) -> DerivationSchemas:
    _write_probe_registry(tmp)
    return DerivationSchemas(
        [KERNEL_SCHEMA_DIR, DERIVATION_SCHEMA_DIR, TAX_SCHEMA_DIR, tmp]
    )


def _codes(result: Any) -> list[str]:
    return [issue.code for issue in result.issues]


class PackageUnsupportedSemanticSchema(unittest.TestCase):
    def test_admitted_registry_recognized_member_is_exactly_unsupported(self) -> None:
        with TemporaryDirectory() as raw:
            tmp = Path(raw)
            schemas = _extended_schemas(tmp)
            citizen = {
                "schema": UNSUPPORTED_SCHEMA,
                "id": "demo.unsupported.semantic-member",
                "version": "v1",
            }
            package = {
                "schema": PROBE_PACKAGE_SCHEMA,
                "id": "demo.package.unsupported-semantic",
                "version": "v1",
                "scope": {
                    "tax_year": 2025,
                    "jurisdiction": "US-federal",
                    "family": "individual-income-tax",
                },
                "admitted_schemas": [UNSUPPORTED_SCHEMA],
                "members": [
                    {"role": "parameter", "id": citizen["id"], "version": citizen["version"]},
                ],
            }
            self.assertEqual(schemas.validate_declared(package), PROBE_PACKAGE_SCHEMA)
            self.assertEqual(schemas.validate_declared(citizen), UNSUPPORTED_SCHEMA)
            result = validate_package(package, _corpus([citizen]), schemas)
            self.assertFalse(result.ok)
            self.assertEqual(_codes(result), ["MEMBER_SCHEMA_UNSUPPORTED"])
            issue = result.issues[0]
            self.assertEqual(issue.member_id, citizen["id"])
            self.assertIn(UNSUPPORTED_SCHEMA, issue.detail)
            self.assertIn(citizen["id"], issue.detail)
            self.assertNotIn("SCHEMA_NOT_ADMITTED", _codes(result))
            self.assertNotIn("MEMBER_SCHEMA_INVALID", _codes(result))
            self.assertNotIn("MEMBER_UNREACHABLE", _codes(result))

    def test_registry_unknown_schema_raises_registry_error(self) -> None:
        schemas = DerivationSchemas()
        citizen = {
            "schema": UNSUPPORTED_SCHEMA,
            "id": "demo.unsupported.unregistered",
            "version": "v1",
        }
        package = {
            "schema": "artifact-package.v1",
            "id": "demo.package.unregistered-schema",
            "version": "v1",
            "scope": {
                "tax_year": 2025,
                "jurisdiction": "US-federal",
                "family": "individual-income-tax",
                "effective_from": "2025-01-01",
            },
            "members": [
                {"role": "parameter", "id": citizen["id"], "version": citizen["version"]},
            ],
        }
        with self.assertRaises(SchemaRegistryError) as ctx:
            validate_package(package, _corpus([citizen]), schemas)
        self.assertIn(UNSUPPORTED_SCHEMA, str(ctx.exception))


class RegistryKnownUnhandledVersions(unittest.TestCase):
    def test_fact_type_v1_is_registry_known_and_semantically_unsupported(self) -> None:
        schemas = DerivationSchemas()
        citizen = {
            "schema": "fact-type.v1",
            "id": "demo.fact.unhandled-v1",
            "title": "Demo unhandled fact type v1",
            "nature": "determinable",
            "identity_keys": [{"name": "tax-year", "kind": "literal", "values": ["2025"]}],
            "value_schema": {"type": "number"},
            "supersession": {"policy": "free"},
        }
        self.assertEqual(schemas.validate_declared(citizen), "fact-type.v1")
        package = {
            "schema": "artifact-package.v1",
            "id": "demo.package.fact-type-v1",
            "version": "v1",
            "scope": {
                "tax_year": 2025,
                "jurisdiction": "US-federal",
                "family": "individual-income-tax",
                "effective_from": "2025-01-01",
            },
            "members": [{"role": "parameter", "id": citizen["id"], "version": "v1"}],
        }
        result = validate_package(package, {(citizen["id"], "v1"): citizen}, schemas)
        self.assertFalse(result.ok)
        self.assertEqual(_codes(result), ["MEMBER_SCHEMA_UNSUPPORTED"])
        self.assertIn("fact-type.v1", result.issues[0].detail)

    def test_source_closure_mapping_v1_is_registry_known_and_semantically_unsupported(self) -> None:
        schemas = DerivationSchemas()
        citizen = {
            "schema": "source-closure-mapping.v1",
            "id": "demo.mapping.unhandled-v1",
            "version": "v1",
            "family": {"id": "demo.family.unhandled", "version": "v1"},
            "member_fact_type": "demo.fact.unhandled-member",
            "closure_fact_type": "demo.fact.unhandled-closure",
            "closure_horizon_key": "family-horizon",
            "admits_symbol": "demo.symbol.unhandled-closed",
            "admission": {"condition": "current-literal-true"},
        }
        self.assertEqual(schemas.validate_declared(citizen), "source-closure-mapping.v1")
        package = {
            "schema": "artifact-package.v1",
            "id": "demo.package.mapping-v1",
            "version": "v1",
            "scope": {
                "tax_year": 2025,
                "jurisdiction": "US-federal",
                "family": "individual-income-tax",
                "effective_from": "2025-01-01",
            },
            "members": [{"role": "parameter", "id": citizen["id"], "version": citizen["version"]}],
        }
        result = validate_package(package, _corpus([citizen]), schemas)
        self.assertFalse(result.ok)
        self.assertEqual(_codes(result), ["MEMBER_SCHEMA_UNSUPPORTED"])
        self.assertIn("source-closure-mapping.v1", result.issues[0].detail)


class CorePackageSupportedSchemas(unittest.TestCase):
    def test_selected_core_package_has_no_unsupported_members(self) -> None:
        package = _load(CORE_PACKAGE)
        corpus: dict[tuple[str, str], dict[str, Any]] = {}
        for path in CONTENT.glob("*.json"):
            if path.name.startswith("package.") or path.name.startswith("published-"):
                continue
            citizen = _load(path)
            if not isinstance(citizen, dict) or "id" not in citizen or "version" not in citizen:
                continue
            corpus[(citizen["id"], citizen["version"])] = citizen
        result = validate_package(package, corpus, DerivationSchemas())
        unsupported = [issue for issue in result.issues if issue.code == "MEMBER_SCHEMA_UNSUPPORTED"]
        self.assertEqual(unsupported, [])
        member_schemas = {
            corpus[(pin["id"], pin["version"])]["schema"]
            for pin in package["members"]
            if (pin["id"], pin["version"]) in corpus
        }
        self.assertTrue(member_schemas)
        self.assertTrue(member_schemas <= set(package["admitted_schemas"]))
        self.assertIn("migration-artifact.v1", member_schemas)


class PresentationUnsupportedSuccessors(unittest.TestCase):
    def test_unknown_form_field_successor_fails_closed(self) -> None:
        args = _published_field_model_args()
        successor = dict(FIELD)
        successor["schema"] = FIELD_V99
        successor["id"] = "demo.field.line-x-v99"
        args["resolved_members"] = [successor, RULE]
        with self.assertRaises(PresentationModelError) as ctx:
            build_presentation_model(**args)
        message = str(ctx.exception)
        self.assertIn(FIELD_V99, message)
        self.assertIn(successor["id"], message)

    def test_unknown_attachment_successor_fails_closed(self) -> None:
        args = _published_field_model_args()
        attachment = {
            "schema": ATTACHMENT_V99,
            "id": "demo.rule.attachment.unknown",
            "version": "v1",
            "title": "Demo unknown attachment",
        }
        args["resolved_members"] = [FIELD, RULE, attachment]
        with self.assertRaises(PresentationModelError) as ctx:
            build_presentation_model(**args)
        message = str(ctx.exception)
        self.assertIn(ATTACHMENT_V99, message)
        self.assertIn(attachment["id"], message)

    def test_unrelated_non_presentation_citizen_is_ignored(self) -> None:
        args = _published_field_model_args()
        args["resolved_members"] = [FIELD, RULE, UNRELATED]
        model = build_presentation_model(**args)
        validate_presentation_model(model)
        self.assertEqual(model["schema"], PRESENTATION_MODEL_VERSION)
        self.assertEqual(len(model["sections"]), 1)

    def test_existing_field_model_remains_unchanged(self) -> None:
        args = _published_field_model_args()
        model = build_presentation_model(**args)
        validate_presentation_model(model)
        self.assertEqual(model["schema"], PRESENTATION_MODEL_VERSION)
        section = model["sections"][0]
        self.assertEqual(section["resolved"]["disposition"], "published_value")
        self.assertEqual(section["resolved"]["value"], 7)
        self.assertEqual(
            section["citationSites"],
            [{"siteId": "line-x-src-0", "pinId": "demo.raw.a", "pinVersion": "v1", "context": "Demo line"}],
        )
        self.assertEqual(model["pinLabels"], {"demo.raw.a": "Demo source A"})
        self.assertEqual(model["attachments"], [])
        self.assertEqual(model["citationGroups"], [])

    def test_supported_attachment_rule_v6_model_includes_attachments_and_citation_groups(self) -> None:
        raw_line = {
            "schema": "finding.v1",
            "id": "demo.raw.a",
            "fact_id": "demo.fact.a",
            "value": 7,
            "basis": "attested",
            "evidence_ids": ["demo.evidence.a"],
        }
        raw_row = {
            "schema": "finding.v1",
            "id": "demo.raw.row",
            "fact_id": "demo.fact.row",
            "value": 7,
            "basis": "attested",
            "evidence_ids": ["demo.evidence.row"],
        }
        state = _state(
            {"demo.raw.a": raw_line, "demo.raw.row": raw_row},
            {
                "demo.evidence.a": EvidenceLifecycle(
                    evidence={
                        "schema": "evidence.v1",
                        "id": "demo.evidence.a",
                        "kind": "demo.statement.x",
                        "label": "Demo source A",
                        "content": {},
                    },
                    status="current",
                ),
                "demo.evidence.row": EvidenceLifecycle(
                    evidence={
                        "schema": "evidence.v1",
                        "id": "demo.evidence.row",
                        "kind": "demo.statement.row",
                        "label": "Demo row A",
                        "content": {},
                    },
                    status="current",
                ),
            },
        )
        line_finding = _finding(
            "demo.derived.x",
            "demo.symbol.line-x",
            "7",
            [{"role": "input", "id": "demo.raw.a", "version": "v1"}],
        )
        attachment_finding = {
            "schema": "derived-finding.v2",
            "id": "demo.derived.attachment",
            "symbol": "demo.symbol.attachment",
            "version": "v2",
            "value": {
                "itemizations": [
                    {
                        "part_id": "part-a",
                        "row_sets": [{"rows": [{"finding_id": "demo.raw.row"}]}],
                        "adjustment_rows": [],
                    }
                ]
            },
            "pins": [],
        }
        dispositions = [
            {
                "artifact_id": "demo.rule.line-x",
                "disposition": "published",
                "finding_id": "demo.derived.x",
                "symbol": "demo.symbol.line-x",
                "pins": line_finding["pins"],
            },
            {
                "artifact_id": "demo.rule.attachment.v6",
                "disposition": "published",
                "finding_id": "demo.derived.attachment",
                "symbol": "demo.symbol.attachment",
                "pins": [],
            },
        ]
        model = build_presentation_model(
            run_id="demo.run",
            resolved_members=[FIELD, RULE, ATTACHMENT_V6],
            state=state,
            publications=[
                Publication(act={}, finding=line_finding),
                Publication(act={}, finding=attachment_finding),
            ],
            dispositions=dispositions,
        )
        validate_presentation_model(model)
        self.assertEqual(
            model["attachments"],
            [
                {
                    "id": "demo.rule.attachment.v6",
                    "title": "Demo attachment",
                    "resolved": {"disposition": "published", "activeCodes": [], "act": None},
                }
            ],
        )
        self.assertEqual(
            model["citationGroups"],
            [
                {
                    "id": "demo.rule.attachment.v6",
                    "title": "Demo attachment",
                    "parts": [
                        {
                            "heading": "Part A",
                            "citationSites": [
                                {
                                    "siteId": "part-a-src-0",
                                    "pinId": "demo.raw.row",
                                    "pinVersion": "v1",
                                    "context": "Part A",
                                }
                            ],
                            "tieOutText": "Reported subtotal: 7",
                        }
                    ],
                }
            ],
        )
        self.assertEqual(model["pinLabels"]["demo.raw.row"], "Demo row A")
