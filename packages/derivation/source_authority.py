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

import json
from dataclasses import dataclass
from typing import Any, Collection, Mapping, Sequence


class SourceAuthorityError(Exception):
    """A mapping/declaration pair violates the ratified authority contract."""


GROUP_MAPPING_SCHEMA = "source-closure-mapping.v4"


def is_group_mapping(mapping: Mapping[str, Any]) -> bool:
    """A v4 mapping admits several families from one yes/no fact."""
    return mapping.get("schema") == GROUP_MAPPING_SCHEMA


def mapping_family_rows(mapping: Mapping[str, Any]) -> list[dict[str, Any]]:
    """The families one mapping admits.

    v2 and v3 name one family on the mapping. v4 names them in ``families``.
    """
    if is_group_mapping(mapping):
        rows = mapping.get("families")
        if not isinstance(rows, list):
            return []
        return [row for row in rows if isinstance(row, dict)]
    return [
        {
            "family": mapping["family"],
            "member_fact_type": mapping["member_fact_type"],
            "admits_symbol": mapping["admits_symbol"],
        }
    ]


def pin_id(pin: Any) -> str:
    if isinstance(pin, dict):
        return str(pin.get("id", ""))
    return str(pin)


def validate_listed_family(
    mapping_id: str, row: Mapping[str, Any], family: Mapping[str, Any]
) -> None:
    """The v4 row honors its pinned declaration the way one v3 mapping does."""
    pin = row["family"]
    if pin["id"] != family["id"] or pin["version"] != family["version"]:
        raise SourceAuthorityError(
            f"mapping {mapping_id} pins family {pin['id']} {pin['version']} "
            f"but was paired with {family['id']} {family['version']}"
        )
    declared = family["member_predicate"]["fact_type"]
    member_fact_type = row["member_fact_type"]
    member_fact_type_id = pin_id(member_fact_type)
    if member_fact_type_id != declared:
        raise SourceAuthorityError(
            f"claim/predicate mismatch: mapping {mapping_id} names member "
            f"fact type {member_fact_type} but declaration "
            f"{family['id']} {family['version']} declares {declared}"
        )
    authorized = family["authorizes_subtotal"]
    if row["admits_symbol"] != authorized:
        raise SourceAuthorityError(
            f"narrow-subtotal substitution: mapping {mapping_id} admits "
            f"symbol {row['admits_symbol']} but declaration "
            f"{family['id']} {family['version']} authorizes only {authorized}"
        )


def group_member_counts(
    mappings: Sequence[Mapping[str, Any]], sources: Sequence[Any]
) -> dict[str, int]:
    """Current members of each family a v4 mapping lists.

    A source whose name is that family's member fact type is one current
    member. v2 and v3 mappings are not counted here.
    """
    names = [getattr(source, "name", None) for source in sources]
    counts: dict[str, int] = {}
    for mapping in mappings:
        if not is_group_mapping(mapping):
            continue
        for row in mapping_family_rows(mapping):
            family = row.get("family")
            if not isinstance(family, dict) or "id" not in family:
                continue
            member_type = pin_id(row.get("member_fact_type"))
            counts[str(family["id"])] = sum(1 for name in names if name == member_type)
    return counts


def stale_group_families(
    acts: Sequence[Mapping[str, Any]], mappings: Sequence[Mapping[str, Any]]
) -> frozenset[str]:
    """Families a later added member strips until the filer answers again.

    The current answer is the last assertion of the v4 closure fact. A
    member-transition that adds a member of a listed family after that
    assertion strips that family only. The recorded action is
    ``payload.member.action``; a flat ``payload.action`` is the same claim.
    A removal does not. Shared horizon ids are not involved.
    """
    families_by_fact: dict[str, set[str]] = {}
    for mapping in mappings:
        if not is_group_mapping(mapping):
            continue
        fact_type = pin_id(mapping.get("closure_fact_type"))
        if not fact_type:
            continue
        families_by_fact.setdefault(fact_type, set()).update(
            str(row["family"]["id"])
            for row in mapping_family_rows(mapping)
            if isinstance(row.get("family"), dict) and row["family"].get("id")
        )
    if not families_by_fact:
        return frozenset()
    answer_at: dict[str, int] = {}
    for index, act in enumerate(acts):
        if act.get("kind") != "assertion":
            continue
        payload = act.get("payload")
        finding = payload.get("finding") if isinstance(payload, dict) else None
        if not isinstance(finding, dict):
            continue
        fact_type = str(finding.get("fact_id") or "").split("|", 1)[0]
        if fact_type in families_by_fact:
            answer_at[fact_type] = index
    stale: set[str] = set()
    for index, act in enumerate(acts):
        if act.get("kind") != "member-transition":
            continue
        payload = act.get("payload")
        if not isinstance(payload, dict):
            continue
        member = payload.get("member")
        action = member.get("action") if isinstance(member, dict) else payload.get("action")
        if action not in {"assert", "reclassify"}:
            continue
        family = payload.get("family")
        family_id = family.get("id") if isinstance(family, dict) else None
        if not isinstance(family_id, str):
            continue
        for fact_type, families in families_by_fact.items():
            answered = answer_at.get(fact_type)
            if answered is not None and index > answered and family_id in families:
                stale.add(family_id)
    return frozenset(stale)


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
    member_fact_type = mapping["member_fact_type"]
    member_fact_type_id = member_fact_type["id"] if isinstance(member_fact_type, dict) else member_fact_type
    if member_fact_type_id != declared:
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


def families_refused_for_unreported_basis(
    sources: Sequence[Any],
    object_to_family: Mapping[str, str],
) -> frozenset[str]:
    """Families whose current covered sale says the broker did not report basis.

    ``object_to_family`` maps the sale object's fact type to the family id
    that sale would otherwise admit. A current member whose value is an
    object with ``basis_reported_to_irs`` equal to ``no`` refuses that family.
    """
    refused: set[str] = set()
    for source in sources:
        family_id = object_to_family.get(str(getattr(source, "name", "")))
        if family_id is None:
            continue
        value = getattr(source, "value", None)
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except ValueError:
                continue
        if isinstance(value, dict) and value.get("basis_reported_to_irs") == "no":
            refused.add(family_id)
    return frozenset(refused)


def covered_flag_block(
    code: str,
    missing: Sequence[str],
    refused_families: Collection[str],
    token: str,
) -> tuple[str, list[str]]:
    """Replace a refused family id in ``missing`` with the dedicated token.

    The recorded code becomes ``DEPENDENCY_INVALID``. A row that does not
    name a refused family is returned unchanged. An empty refusal set is a
    no-op, which is how earlier packages keep their recorded rows.
    """
    if not refused_families:
        return code, list(missing)
    rewritten: list[str] = []
    hit = False
    for item in missing:
        if str(item) in refused_families:
            hit = True
            if token not in rewritten:
                rewritten.append(token)
        else:
            rewritten.append(str(item))
    if not hit:
        return code, list(missing)
    return "DEPENDENCY_INVALID", rewritten


def resolve_closure_admissions(
    mappings: list[dict[str, Any]],
    declarations: list[dict[str, Any]],
    closure_findings: list[ClosureFindingRecord],
    current_horizons: dict[str, str],
    *,
    member_counts: Mapping[str, int] | None = None,
    acts: Sequence[Mapping[str, Any]] | None = None,
    refused_families: Collection[str] | None = None,
) -> dict[str, ClosureAdmission]:
    """The single dispatch path: compute the admitted family set internally.

    Content defects are loud errors: a mapping pinning an undeclared family
    (fabricated), a mapping/declaration mismatch, or two mappings claiming
    one family (ambiguous adopted authority) all raise. Finding-level
    defects are quiet non-admissions — false, absent, displaced,
    truthy-non-boolean, or duplicate closure findings leave the family out
    of the closed set, so the real two-layer ``collect`` check blocks
    rather than zeroes (ADR-0014 decision 3).

    A v4 mapping lists several families under one yes/no fact. ``no``
    admits a listed family with a current horizon and zero current members.
    ``yes`` admits each listed family with a current horizon unless ``acts``
    show a member added to that family after the current answer. v2 and v3
    mappings ignore ``member_counts`` and ``acts``.

    ``refused_families`` drops an otherwise-admitted family after that
    resolution. The caller passes it only when the adopted package names
    the covered-flag refusal map. An empty set leaves admission unchanged.
    """
    counts = dict(member_counts or {})
    stale = stale_group_families(acts or (), mappings)
    refused = set(refused_families or ())
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
        if is_group_mapping(mapping):
            _admit_group(
                mapping, by_id, claimed, admissions, closure_findings,
                current_horizons, counts, stale,
            )
            continue
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
        closure_fact_type = mapping["closure_fact_type"]
        closure_fact_type_id = closure_fact_type["id"] if isinstance(closure_fact_type, dict) else closure_fact_type
        candidates = [
            record
            for record in closure_findings
            if record.fact_type == closure_fact_type_id
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
    if refused:
        for family_id in list(admissions):
            if family_id in refused:
                del admissions[family_id]
    return admissions


def _admit_group(
    mapping: Mapping[str, Any],
    by_id: Mapping[str, dict[str, Any]],
    claimed: set[str],
    admissions: dict[str, ClosureAdmission],
    closure_findings: Sequence[ClosureFindingRecord],
    current_horizons: Mapping[str, str],
    member_counts: Mapping[str, int],
    stale: Collection[str],
) -> None:
    """Admit each family a v4 mapping lists from the one current answer."""
    fact_type_id = pin_id(mapping.get("closure_fact_type"))
    candidates = [
        record for record in closure_findings if record.fact_type == fact_type_id
    ]
    answer = candidates[0] if len(candidates) == 1 else None
    value = answer.value if answer is not None else None
    for row in mapping_family_rows(mapping):
        family_pin = row.get("family")
        if not isinstance(family_pin, dict) or "id" not in family_pin:
            raise SourceAuthorityError(
                f"mapping {mapping.get('id')} lists a family with no pin"
            )
        family_id = str(family_pin["id"])
        declared = by_id.get(family_id)
        if declared is None:
            raise SourceAuthorityError(
                f"fabricated mapping: {mapping.get('id')} pins family {family_id}, "
                "which no adopted declaration provides"
            )
        validate_listed_family(str(mapping.get("id")), row, declared)
        if family_id in claimed:
            raise SourceAuthorityError(
                f"duplicate mapping authority for family {family_id}"
            )
        claimed.add(family_id)
        current = current_horizons.get(family_id)
        if current is None or answer is None:
            continue
        admits = False
        if value == "no":
            admits = member_counts.get(family_id, 0) == 0
        elif value == "yes":
            admits = family_id not in stale
        if not admits:
            continue
        admissions[family_id] = ClosureAdmission(
            family_id=family_id,
            mapping_id=str(mapping["id"]),
            mapping_version=str(mapping["version"]),
            declaration_id=declared["id"],
            declaration_version=declared["version"],
            horizon_id=current,
            closure_finding_id=answer.finding_id,
        )


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
    mapped_families = {
        str(row["family"]["id"])
        for mapping in mappings
        for row in mapping_family_rows(mapping)
        if isinstance(row.get("family"), dict) and row["family"].get("id")
    }
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
