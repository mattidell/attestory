"""Rung-2 spike, Seam 1 (Canonical Value Extraction), case 6 only.

PROTOTYPE. Not production code. Never imported by `tests/`, never wired into
`packages/derivation/package_validation.py`. All fixture ids/values below are
synthetic.

Purpose: settle the one question `docs/prototypes/canonical-value-extraction/
plan.md` Gate 3 names as requiring more than paper — does a misspelled
`field` selector on candidate C's widened `ref_expr` actually fail closed
against the *real* schema-validation mechanism, given today's `rule-
artifact.v6` `ref_expr` has `additionalProperties: false` (confirmed by
`reviews/adversary-r1.md`)?

This script imports and drives the real `packages.kernel.schema_registry`
module (the exact mechanism `packages/derivation/loader.py`'s
`DerivationSchemas`/`schemas.validate_declared` calls in
`package_validation.py`'s `validate_package`) against:

  1. the real, unmodified `rule-artifact.v6` schema (to reproduce the
     committee's diagnosis: today's shape rejects the mechanism itself), and
  2. a draft `rule-artifact.v7` schema (this directory's
     `rule-artifact.v7.schema.json`, a spike-local copy, never touching
     `packages/schemas/`) that adds an optional `field` string to `ref_expr`
     with `additionalProperties: false` preserved.

It then runs a narrowly-scoped equivalent of the semantic check
`package_validation.py` does not yet have (no `field`-existence check exists
in production today, confirmed by `reviews/adversary-r1.md` reading
`validate_package`'s `input_bindings` section) — walking a v7 citizen's
`value`/`when` expression tree for `ref` nodes carrying `field`, and
rejecting any `field` absent from the bound fact type's
`value_schema.properties`, in the same style `package_validation.py` already
uses elsewhere (e.g. its `_is_yes_no_domain` reading `value_schema`).

Run: `python3 docs/prototypes/canonical-value-extraction/spike/case6_spike.py`
from the repo root. Exits 0 and prints PASS lines iff every assertion holds;
raises/exits non-zero on any unexpected acceptance or rejection.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT))

from packages.kernel.schema_registry import (  # noqa: E402
    KERNEL_SCHEMA_DIR,
    SchemaRegistry,
    SchemaValidationError,
)

SPIKE_DIR = Path(__file__).resolve().parent
DERIVATION_SCHEMA_DIR = REPO_ROOT / "packages" / "schemas" / "derivation"

# ---------------------------------------------------------------------------
# Synthetic fixtures. No real account numbers, names, or amounts.
# ---------------------------------------------------------------------------

BOND_PURCHASE_FACT_TYPE: dict[str, Any] = {
    "schema": "fact-type.v2",
    "id": "tax.us.2025.acquisition.bond-purchase",
    "version": "v1",
    "title": "Synthetic bond purchase acquisition (Seam 1 spike fixture)",
    "nature": "determinable",
    "identity_keys": [
        {"name": "broker", "kind": "entity", "entity_kind": "broker"},
        {"name": "statement", "kind": "entity", "entity_kind": "statement"},
        {"name": "transaction", "kind": "entity", "entity_kind": "transaction"},
        {"name": "tax-year", "kind": "literal", "values": ["2025"]},
    ],
    "value_schema": {
        "type": "object",
        "properties": {
            "purchase_price": {"type": "number"},
            "trade_date": {"type": "string"},
            "quantity": {"type": "number"},
            "accrued_interest_paid_to_seller": {"type": "number"},
        },
        "required": ["purchase_price", "trade_date", "quantity"],
    },
    "supersession": {"policy": "free"},
}


def _rule_artifact_v7(field: str) -> dict[str, Any]:
    """A synthetic rule-artifact.v7 citizen with a field-ref ``value`` expr.

    ``requires`` names the bare fact-type id (marshal.py's existing legacy
    "symbol == fact type id" fallback path, confirmed at
    `packages/derivation/marshal.py` ~326-380 by `reviews/adversary-r1.md`
    case 2), so this fixture needs no ``requires``/``pins`` schema growth —
    only ``ref_expr`` widens.
    """
    return {
        "schema": "rule-artifact.v7",
        "id": "tax.us.2025.rule.scheduleb-adjustment.accrued-interest-from-acquisition",
        "version": "v1",
        "scope": {"tax_year": 2025, "jurisdiction": "us", "family": "scheduleb-adjustment"},
        "role": "computation",
        "requires": ["tax.us.2025.acquisition.bond-purchase"],
        "pins": [],
        "when": True,
        "value": {
            "op": "ref",
            "name": "tax.us.2025.acquisition.bond-purchase",
            "field": field,
        },
        "publishes": "tax.us.2025.scheduleb-adjustment.accrued-interest-from-acquisition",
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
    }


def _rule_artifact_v6_with_field(field: str) -> dict[str, Any]:
    """Same shape, declared under the real, unmodified v6 schema, to
    reproduce the committee's diagnosis that today's shape rejects the
    mechanism itself (not the field spelling)."""
    artifact = _rule_artifact_v7(field)
    artifact["schema"] = "rule-artifact.v6"
    return artifact


# ---------------------------------------------------------------------------
# Semantic field-existence check: package_validation.py has no field concept
# today (confirmed), so this is new spike-local code, written in the same
# style as that module's existing value_schema readers (e.g.
# `_is_yes_no_domain`). It is the thing a real `v7` successor's
# `validate_package` would need to add.
# ---------------------------------------------------------------------------

class FieldRefValidationError(Exception):
    """A rule-artifact.v7 citizen names a field absent from the bound fact
    type's value_schema.properties. Fails closed: never a silent None/zero."""


def _iter_ref_field_bindings(expr: Any) -> Iterable[tuple[str, str]]:
    """Yield (bound_symbol, field) for every ``ref`` node carrying ``field``,
    walking the same shapes `package_validation.py`'s own `_iter_ref_names`
    walks (dict nodes with "op", recursing through args/left/right/etc.)."""
    if isinstance(expr, dict):
        if expr.get("op") == "ref" and "field" in expr:
            yield (expr["name"], expr["field"])
        for value in expr.values():
            yield from _iter_ref_field_bindings(value)
    elif isinstance(expr, list):
        for item in expr:
            yield from _iter_ref_field_bindings(item)


def check_field_ref_bindings(
    citizen: dict[str, Any],
    fact_types_by_id: dict[str, dict[str, Any]],
) -> None:
    """Fail closed on any field-ref binding naming a field absent from the
    bound fact type's ``value_schema.properties`` — the check case 6 says
    must exist and today does not (confirmed by reading `validate_package`'s
    `input_bindings` section, which has no sub-field concept)."""
    for expr_key in ("when", "value"):
        for symbol, field in _iter_ref_field_bindings(citizen.get(expr_key)):
            fact_type = fact_types_by_id.get(symbol)
            if fact_type is None:
                raise FieldRefValidationError(
                    f"{citizen['id']}: field-ref binds symbol {symbol!r}, "
                    f"which is not a known fact type in this package's surface"
                )
            properties = fact_type.get("value_schema", {}).get("properties", {})
            if field not in properties:
                raise FieldRefValidationError(
                    f"{citizen['id']}: field-ref names {field!r} on "
                    f"{symbol!r}, which has no such property in its "
                    f"value_schema (known: {sorted(properties)}) "
                    f"[FIELD_REF_UNKNOWN_FIELD]"
                )


# ---------------------------------------------------------------------------
# The spike itself.
# ---------------------------------------------------------------------------

def main() -> None:
    real_v6_registry = SchemaRegistry(DERIVATION_SCHEMA_DIR)
    spike_v7_registry = SchemaRegistry([KERNEL_SCHEMA_DIR, SPIKE_DIR])

    # --- Baseline: today's real, unmodified v6 rejects the mechanism itself,
    # correctly-spelled field included. This reproduces
    # `reviews/adversary-r1.md`'s diagnosis against real code, not prose.
    try:
        real_v6_registry.validate(
            "rule-artifact.v6",
            _rule_artifact_v6_with_field("accrued_interest_paid_to_seller"),
        )
    except SchemaValidationError as exc:
        assert "field" in str(exc) or "additionalProperties" in str(exc) or exc.errors, exc
        print("PASS baseline: real unmodified rule-artifact.v6 rejects any "
              "`field` key on ref_expr (correct or misspelled alike) — "
              f"{exc.errors[0] if exc.errors else exc}")
    else:
        raise AssertionError(
            "FAIL baseline: real v6 unexpectedly accepted a `field` key on "
            "ref_expr — the committee's diagnosis does not hold"
        )

    # --- Draft v7: schema-level acceptance of the widened ref_expr shape,
    # for both a correctly-spelled and a misspelled field. Schema validation
    # alone cannot distinguish them (that is exactly the point of case 6):
    # both must pass the *schema* gate, then diverge at the *semantic* gate.
    for field in ("accrued_interest_paid_to_seller", "accrued_interest_paid_to_seler"):
        spike_v7_registry.validate("rule-artifact.v7", _rule_artifact_v7(field))
        spike_v7_registry.validate("fact-type.v2", BOND_PURCHASE_FACT_TYPE)
    print("PASS: draft rule-artifact.v7 schema accepts the widened `ref_expr` "
          "`field` key at the schema-validation stage for both a correctly-"
          "spelled and a misspelled field name (schema alone cannot tell them "
          "apart — this is the gap case 6 asks about).")

    fact_types_by_id = {BOND_PURCHASE_FACT_TYPE["id"]: BOND_PURCHASE_FACT_TYPE}

    # --- Positive case: correctly-spelled field passes the semantic check.
    good_citizen = _rule_artifact_v7("accrued_interest_paid_to_seller")
    check_field_ref_bindings(good_citizen, fact_types_by_id)
    print("PASS positive: correctly-spelled field "
          "'accrued_interest_paid_to_seller' accepted by the semantic "
          "value_schema.properties check.")

    # --- Negative case: misspelled field is rejected, never silently None.
    bad_citizen = _rule_artifact_v7("accrued_interest_paid_to_seler")
    try:
        check_field_ref_bindings(bad_citizen, fact_types_by_id)
    except FieldRefValidationError as exc:
        print(f"PASS negative: misspelled field rejected at load time — {exc}")
    else:
        raise AssertionError(
            "FAIL negative: misspelled field silently passed the semantic "
            "check — case 6 would remain unsettled"
        )

    print("\nAll case-6 rung-2 assertions passed.")


if __name__ == "__main__":
    main()
