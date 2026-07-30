"""Schema-consuming loader for the derivation citizen family.

ADR-0006 decision 3: the declared schema is the runtime authority. This
loader validates every citizen against the *published* schema files via the
kernel SchemaRegistry — it never hand-rolls a duplicate of the grammar, and
a schema mutated out from under its checksum is a registry defect, not a
silent pass. Validation failure is surfaced as a typed error the runner can
contain and record (never a run-aborting crash).

The one role vocabulary (ADR-0006 decision 9) is asserted here rather than
trusted per-schema: `role_vocabulary_report` proves every role enum across
rule-artifact, package member, and pin positions is a subset of a single
master vocabulary, so a `mapping`/`field-mapping` divergence (round-2
legibility finding L-8) cannot reappear.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from packages.kernel.schema_registry import (
    KERNEL_SCHEMA_DIR,
    SchemaRegistry,
    SchemaValidationError,
)

_PACKAGES_DIR = Path(__file__).resolve().parent.parent
DERIVATION_SCHEMA_DIR = _PACKAGES_DIR / "schemas" / "derivation"
TAX_SCHEMA_DIR = _PACKAGES_DIR / "schemas" / "tax"
CANON_DIR = _PACKAGES_DIR / "canon" / "derivation"



def workspace_registry() -> SchemaRegistry:
    """A registry spanning both act families a workspace act log stores.

    ADR-0010: the act log admits kernel acts and derived-publication acts, so
    the registry that validates it must span the kernel and derivation schema
    directories. Schema ids are unique across the two families.
    """
    return SchemaRegistry([KERNEL_SCHEMA_DIR, DERIVATION_SCHEMA_DIR])

RULE_ARTIFACT_SCHEMA = "rule-artifact.v1"
PARAMETER_SCHEMA = "parameter-declaration.v1"
PACKAGE_SCHEMA = "artifact-package.v1"
PUBLICATION_ACT_SCHEMA = "act-derived-publication.v1"
DERIVED_FINDING_SCHEMA = "derived-finding.v1"
DERIVATION_RECORD_SCHEMA = "derivation-record.v1"
OPERATION_SEMANTICS_SCHEMA = "operation-semantics.v1"

# The single role vocabulary (ADR-0006 decision 9). Every role enum in the
# published schemas must be a subset of this set.
ROLE_VOCABULARY = frozenset(
    {
        "parameter",
        "computation",
        "applicability",
        "field-mapping",
        "cross-form-bridge",
        "input",
        "choice",
        "default",
        "composition",
        "citation",
        "adoption",
        "governance",
        "engine",
        "package",
        "operation-semantics",
        "form-field",
        "source-family",
        "source-closure-mapping",
        "fact-type",
        "fact-type-bundle",
        "dividend-universe",
        "attachment-rule",
        "checked-conclusion-binding",
    }
)

# The closed operation vocabulary (ADR-0006 decision 2), and the subset whose
# meaning is versioned canon rather than a bare enum name (decision 4).
OPERATION_VOCABULARY = frozenset(
    {
        "ref",
        "collect",
        "parameter",
        "add",
        "subtract",
        "max",
        "compare",
        "all",
        "any",
        "not",
        "choose",
        "range_lookup",
        "bracket_fold",
        "round",
    }
)
CANON_OPERATIONS = frozenset({"round", "range_lookup", "bracket_fold"})


class DerivationSchemas:
    """The published derivation schema set, loaded once and validated against."""

    def __init__(self, schema_dir: Path | list[Path] | None = None) -> None:
        if schema_dir is not None:
            self._registry = SchemaRegistry(schema_dir)
        else:
            self._registry = SchemaRegistry([KERNEL_SCHEMA_DIR, DERIVATION_SCHEMA_DIR, TAX_SCHEMA_DIR])

    def schema_ids(self) -> list[str]:
        return self._registry.schema_ids()

    @property
    def registry(self) -> SchemaRegistry:
        """The published registry for projections that consume this schema set."""
        return self._registry

    def get(self, schema_id: str) -> dict[str, Any]:
        return self._registry.get(schema_id)

    def validate(self, schema_id: str, instance: object) -> None:
        """Strictly validate against a named published schema version."""
        self._registry.validate(schema_id, instance)

    def validate_declared(self, instance: dict[str, Any]) -> str:
        """Validate a self-declaring citizen against the schema it names."""
        return self._registry.validate_declared(instance)


def load_canon(schemas: DerivationSchemas, canon_dir: Path | None = None) -> dict[str, dict[str, Any]]:
    """Load and validate the operation-semantics canon citizens.

    Returns a mapping operation -> citizen. Every operation whose meaning is
    canon (ADR-0006 decision 4) must be present exactly once; a missing or
    duplicated operation is a canon defect, surfaced as SchemaValidationError
    so callers treat it as a contained outcome.
    """
    directory = canon_dir if canon_dir is not None else CANON_DIR
    by_operation: dict[str, dict[str, Any]] = {}
    for path in sorted(directory.glob("*.json")):
        citizen: dict[str, Any] = json.loads(path.read_text("utf-8"))
        schemas.validate_declared(citizen)
        operation = citizen["operation"]
        if operation in by_operation:
            raise SchemaValidationError(
                OPERATION_SEMANTICS_SCHEMA,
                [f"duplicate operation-semantics canon for {operation}"],
            )
        by_operation[operation] = citizen
    missing = CANON_OPERATIONS - set(by_operation)
    if missing:
        raise SchemaValidationError(
            OPERATION_SEMANTICS_SCHEMA,
            [f"missing operation-semantics canon: {name}" for name in sorted(missing)],
        )
    return by_operation


def _role_enums(document: dict[str, Any]) -> list[list[str]]:
    """Collect every ``role`` enum declared anywhere in a schema document."""
    found: list[list[str]] = []

    def walk(node: Any, key: str | None) -> None:
        if isinstance(node, dict):
            if key == "role" and isinstance(node.get("enum"), list):
                found.append([str(v) for v in node["enum"]])
            for child_key, child in node.items():
                walk(child, child_key)
        elif isinstance(node, list):
            for child in node:
                walk(child, key)

    walk(document, None)
    return found


def role_vocabulary_report(schemas: DerivationSchemas) -> dict[str, set[str]]:
    """Every role enum across the schema set, mapped schema_id -> role tokens.

    Operationalizes ADR-0006 decision 9: the returned tokens must all be a
    subset of ROLE_VOCABULARY. Callers (the conformance test) assert that.
    """
    report: dict[str, set[str]] = {}
    for schema_id in schemas.schema_ids():
        tokens: set[str] = set()
        for enum in _role_enums(schemas.get(schema_id)):
            tokens.update(enum)
        if tokens:
            report[schema_id] = tokens
    return report
