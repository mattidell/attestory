"""Source-authority contract validation and closure dispatch.

ADR-0014: source closure enters calculation only through an adopted mapping
citizen pinned to one source-family declaration version. ADR-0016: the
declaration's exact claim and canonical member predicate are the semantic
authority, and closure of a family may authorize only that family's declared
subtotal symbol.

Track 1 gave this module the pair-level checks JSON Schema cannot express;
Track 3 adds the runner's single dispatch path: admission is resolved here,
internally, from the adopted mappings, the current literal-true closure
finding keyed on the current horizon, and nothing else. A rule's ``collect``
names the source-family declaration id as its ``source_set``; the admitted
family set is computed, never accepted from a caller. No tolerant fallback
exists — a mismatched pair or ambiguous authority is rejected, never
repaired.
"""

from __future__ import annotations

from dataclasses import dataclass
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


@dataclass(frozen=True)
class ClosureFindingRecord:
    """One closure finding as marshalled from current record state.

    ``horizon_id`` is the family horizon the finding's fact is keyed on
    (ADR-0017 decision 2); the runner admits it only when that horizon is
    the chain's current one, so a finding keyed on a superseded horizon is
    indistinguishable from an absent one on the dispatch path.
    """

    finding_id: str
    fact_type: str
    horizon_id: str
    value: Any


@dataclass(frozen=True)
class ClosureAdmission:
    """Why one source family is admitted into closed membership.

    Carries every identity a closure-backed zero must pin (ADR-0014
    decision 5): the exact mapping version, the declaration it honors, and
    the exact current closure finding. The horizon identity travels inside
    the closure finding's fact key.
    """

    family_id: str
    mapping_id: str
    mapping_version: str
    declaration_id: str
    declaration_version: str
    horizon_id: str
    closure_finding_id: str


def resolve_closure_admissions(
    mappings: list[dict[str, Any]],
    declarations: list[dict[str, Any]],
    closure_findings: list[ClosureFindingRecord],
    current_horizons: dict[str, str],
) -> dict[str, ClosureAdmission]:
    """The single dispatch path: compute the admitted family set internally.

    Content defects are loud errors: a mapping pinning an undeclared family
    (fabricated), a mapping/declaration mismatch, or two mappings claiming
    one family (ambiguous adopted authority) all raise. Finding-level
    defects are quiet non-admissions — false, absent, displaced,
    truthy-non-boolean, or duplicate closure findings leave the family out
    of the closed set, so the real two-layer ``collect`` check blocks
    rather than zeroes (ADR-0014 decision 3).
    """
    by_id: dict[str, dict[str, Any]] = {}
    for declaration in declarations:
        if declaration["id"] in by_id:
            raise SourceAuthorityError(
                f"ambiguous declaration: {declaration['id']} appears twice"
            )
        by_id[declaration["id"]] = declaration

    admissions: dict[str, ClosureAdmission] = {}
    claimed: set[str] = set()
    for mapping in mappings:
        family_id = mapping["family"]["id"]
        declared = by_id.get(family_id)
        if declared is None:
            raise SourceAuthorityError(
                f"fabricated mapping: {mapping['id']} pins family {family_id}, "
                "which no adopted declaration provides"
            )
        validate_mapping_against_family(mapping, declared)
        if family_id in claimed:
            raise SourceAuthorityError(
                f"duplicate mapping authority for family {family_id}"
            )
        claimed.add(family_id)

        current = current_horizons.get(family_id)
        if current is None:
            continue  # no horizon chain in scope: nothing can admit
        candidates = [
            record
            for record in closure_findings
            if record.fact_type == mapping["closure_fact_type"]
            and record.horizon_id == current
        ]
        if len(candidates) != 1:
            continue  # absent or duplicate authority: blocked, never zeroed
        candidate = candidates[0]
        if not isinstance(candidate.value, bool) or candidate.value is not True:
            continue  # false or truthy-non-boolean: blocked, never zeroed
        admissions[family_id] = ClosureAdmission(
            family_id=family_id,
            mapping_id=mapping["id"],
            mapping_version=mapping["version"],
            declaration_id=declared["id"],
            declaration_version=declared["version"],
            horizon_id=current,
            closure_finding_id=candidate.finding_id,
        )
    return admissions


def _collect_source_sets(expr: Any) -> set[str]:
    """Every source_set named by a collect anywhere in an expression tree."""
    found: set[str] = set()
    if isinstance(expr, dict):
        if expr.get("op") == "collect" and "source_set" in expr:
            found.add(expr["source_set"])
        for value in expr.values():
            found |= _collect_source_sets(value)
    elif isinstance(expr, list):
        for item in expr:
            found |= _collect_source_sets(item)
    return found


def audit_collect_authority(
    rules: list[dict[str, Any]],
    mappings: list[dict[str, Any]],
    declarations: list[dict[str, Any]],
) -> None:
    """Labels and symbols cannot broaden authority (ADR-0016 decisions 2-5).

    A rule collecting over a mapped family must publish exactly that
    family's authorized subtotal symbol; any other output symbol would let
    closure of the narrow family stand behind a broader result. Source
    sets with no adopted mapping are untouched — with no admission path
    they can only block when empty.
    """
    authorized = {
        declaration["id"]: declaration["authorizes_subtotal"]
        for declaration in declarations
    }
    mapped_families = {mapping["family"]["id"] for mapping in mappings}
    for rule in rules:
        named = _collect_source_sets(rule.get("when")) | _collect_source_sets(
            rule.get("value")
        )
        for family_id in sorted(named & mapped_families):
            if rule["publishes"] != authorized[family_id]:
                raise SourceAuthorityError(
                    f"rule {rule['id']} collects over family {family_id} but "
                    f"publishes {rule['publishes']}; that family's closure "
                    f"authorizes only {authorized[family_id]}"
                )
