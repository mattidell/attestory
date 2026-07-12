"""Source-authority contract validation (Source Completeness, Track 1).

ADR-0014: source closure enters calculation only through an adopted mapping
citizen pinned to one source-family declaration version. ADR-0016: the
declaration's exact claim and canonical member predicate are the semantic
authority, and closure of a family may authorize only that family's declared
subtotal symbol.

This module holds the pair-level checks JSON Schema cannot express: a mapping
is valid only *against* the declaration it pins. Schema validation of each
citizen alone is the SchemaRegistry's job; runtime dispatch is Track 3. No
tolerant fallback exists — a mismatched pair is rejected, never repaired.
"""

from __future__ import annotations

from typing import Any


class SourceAuthorityError(Exception):
    """A mapping/declaration pair violates the ratified authority contract."""


def validate_mapping_against_family(
    mapping: dict[str, Any], family: dict[str, Any]
) -> None:
    """Reject any mapping that does not exactly honor its pinned declaration.

    Both citizens must already be schema-valid. Checks, in order:
    the pin matches the declaration's id and version; the mapping's member
    fact type equals the declaration's canonical predicate (a divergence is
    a claim/predicate mismatch, ADR-0016 consequence 1); and the admitted
    symbol equals the declaration's authorized subtotal (a broader or
    different symbol is narrow-subtotal substitution, ADR-0016 decision 4).
    """
    pin = mapping["family"]
    if pin["id"] != family["id"] or pin["version"] != family["version"]:
        raise SourceAuthorityError(
            f"mapping {mapping['id']} pins family {pin['id']} {pin['version']} "
            f"but was paired with {family['id']} {family['version']}"
        )
    declared = family["member_predicate"]["fact_type"]
    if mapping["member_fact_type"] != declared:
        raise SourceAuthorityError(
            f"claim/predicate mismatch: mapping {mapping['id']} names member "
            f"fact type {mapping['member_fact_type']} but declaration "
            f"{family['id']} {family['version']} declares {declared}"
        )
    authorized = family["authorizes_subtotal"]
    if mapping["admits_symbol"] != authorized:
        raise SourceAuthorityError(
            f"narrow-subtotal substitution: mapping {mapping['id']} admits "
            f"symbol {mapping['admits_symbol']} but declaration "
            f"{family['id']} {family['version']} authorizes only {authorized}"
        )
