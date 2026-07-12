"""Loader for the tax content family (First Tax Slice, Track 1).

ADR-0011: the W-2 vocabulary is ordinary kernel ``fact-type.v1`` content
carried in a ``bundle.v1`` — no specialized tax-fact-type schema exists.
ADR-0012: an official form field is a first-class versioned content citizen
validated against the published tax schema directory, distinct from the
derivation output symbol it presents.

Like the derivation loader, every citizen is validated against the
*published* schema files via the kernel SchemaRegistry; a schema mutated out
from under its checksum is a registry defect, never a silent pass. This
module loads declared content only — it contains no runner, no workspace,
and no form-identifier-aware scheduling (E11.3 posture).
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
TAX_SCHEMA_DIR = _PACKAGES_DIR / "schemas" / "tax"
TAX_CONTENT_DIR = _PACKAGES_DIR / "content" / "tax" / "2025"

FORM_FIELD_SCHEMA = "form-field.v1"
W2_BUNDLE_FILE = "w2.bundle.json"


def tax_registry() -> SchemaRegistry:
    """A registry spanning the kernel and tax schema families.

    Bundle and fact-type content validate against the kernel family;
    form-field content validates against the tax family. Schema ids are
    unique across the directories (enforced on load).
    """
    return SchemaRegistry([KERNEL_SCHEMA_DIR, TAX_SCHEMA_DIR])


def load_w2_bundle(registry: SchemaRegistry | None = None) -> dict[str, Any]:
    """Load and strictly validate the 2025 W-2 vocabulary bundle.

    The bundle envelope and every nested fact type validate against their
    declared schema versions. Nested fact-type ids must be unique.
    """
    reg = registry if registry is not None else tax_registry()
    bundle: dict[str, Any] = json.loads(
        (TAX_CONTENT_DIR / W2_BUNDLE_FILE).read_text("utf-8")
    )
    reg.validate_declared(bundle)
    seen: set[str] = set()
    for fact_type in bundle["fact_types"]:
        reg.validate_declared(fact_type)
        if fact_type["id"] in seen:
            raise SchemaValidationError(
                "bundle.v1", [f"duplicate fact-type id in bundle: {fact_type['id']}"]
            )
        seen.add(fact_type["id"])
    return bundle


def load_form_fields(registry: SchemaRegistry | None = None) -> dict[str, dict[str, Any]]:
    """Load every committed form-field citizen, mapped id -> citizen.

    Each citizen validates against the published ``form-field.v1`` schema.
    A duplicate id is a content defect: two published fields with one id
    would make the printed-locator identity ambiguous.
    """
    reg = registry if registry is not None else tax_registry()
    by_id: dict[str, dict[str, Any]] = {}
    for path in sorted(TAX_CONTENT_DIR.glob("*.form-field.json")):
        citizen: dict[str, Any] = json.loads(path.read_text("utf-8"))
        declared = reg.validate_declared(citizen)
        if declared != FORM_FIELD_SCHEMA:
            raise SchemaValidationError(
                FORM_FIELD_SCHEMA,
                [f"{path.name} declares {declared}, not {FORM_FIELD_SCHEMA}"],
            )
        if citizen["id"] in by_id:
            raise SchemaValidationError(
                FORM_FIELD_SCHEMA, [f"duplicate form-field id: {citizen['id']}"]
            )
        by_id[citizen["id"]] = citizen
    return by_id
