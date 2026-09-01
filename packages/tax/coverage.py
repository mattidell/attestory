"""Record-derived source-coverage read model.

ADR-0016 decision 3: coverage presents the exact authoritative closure
claim, never shorthand, and a rollup cannot silently report a broader
universe complete. This model is derived entirely from projected record
state plus the adopted declarations and mappings — no second
authoritative store — and it reuses the runner's own admission
resolution, so coverage can never call a family closed that a run would
block on, or vice versa.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from packages.derivation.marshal import marshal_closure_authority
from packages.derivation.source_authority import resolve_closure_admissions
from packages.kernel.currency import CurrencyView
from packages.kernel.findings import FindingState

CLOSED = "closed"
OPEN = "open"


@dataclass(frozen=True)
class FamilyCoverage:
    """One family's coverage: the exact claim and its freshness state.

    ``status`` is CLOSED only while a current literal-true closure
    finding stands on the family's current horizon; a later membership
    transition reopens the family without any manual withdrawal
    (ADR-0017). The claim text is the declaration's, verbatim.
    """

    family_id: str
    exact_claim: str
    authorizes_subtotal: str
    current_horizon: str | None
    status: str
    closure_finding_id: str | None


def coverage_report(
    state: FindingState,
    currency: CurrencyView,
    families: dict[str, dict[str, Any]],
    mappings: dict[str, dict[str, Any]],
) -> list[FamilyCoverage]:
    """Every declared family's coverage, in family-id order."""
    mapping_list = list(mappings.values())
    records, current_horizons = marshal_closure_authority(
        state, currency, mapping_list
    )
    admissions = resolve_closure_admissions(
        mapping_list, list(families.values()), records, current_horizons
    )
    report: list[FamilyCoverage] = []
    for family_id in sorted(families):
        family = families[family_id]
        admission = admissions.get(family_id)
        report.append(
            FamilyCoverage(
                family_id=family_id,
                exact_claim=family["closure_claim"],
                authorizes_subtotal=family["authorizes_subtotal"],
                current_horizon=current_horizons.get(family_id),
                status=CLOSED if admission is not None else OPEN,
                closure_finding_id=(
                    admission.closure_finding_id if admission is not None else None
                ),
            )
        )
    return report


_BUNDLE_SCHEMAS = frozenset({"bundle.v1", "bundle.v2"})

# Expression-tree op shapes whose own ``name`` field genuinely names a fact
# type being read (verified against packages/schemas/derivation/rule-artifact
# .v1..v7 -- every version's ``collect``/``count`` node requires exactly
# ``{op, name, source_set}`` where ``name`` is the collected fact type and
# ``source_set`` is the family id; ``collect_categorical_all_equal`` requires
# ``{op, name, value}`` with the same ``name`` role, per
# packages/derivation/live.py's own ``_iter_collect_categorical_names``,
# which already walks this exact op for a different purpose). A plain
# ``ref`` node's ``name`` is excluded from this general-purpose,
# ordinary-rule-shaped scan: for every non-pairing-scoped rule, it names a
# published symbol or a pin id, never a fact type, so treating it as one
# would resurrect exactly the over-counting this traversal exists to
# prevent.
#
# Narrow exception, not covered by this traversal: this milestone's pairing-scoped
# consequence rules (``packages/tax/pairing_consequences.py``) bind the
# acquisition and report fact-type ids themselves as symbol names in a
# pairing-local ``Environment`` (see its ``_pairing_local_environment``
# construction), so a pairing-scoped rule's declared ``{"op": "ref",
# "name": <fact-type-id>}`` genuinely does read that fact type -- a real,
# committed counterexample to the general claim above. This scanner does
# not special-case pairing-local ``ref`` binding and currently under-counts
# it. This is safe today only because the committed acquisition fact type
# is not marked ``source_amount: true``; if a future pairing-scoped rule's
# ``ref``-bound fact type were marked ``source_amount``, this scanner would
# wrongly report it as unconsumed. Teaching this traversal to recognize a
# pairing-rule's ``ref``-bound fact-type ids specifically (rather than
# ``ref`` nodes in general) is named, not yet done.
_FACT_TYPE_COLLECT_OPS = frozenset({"collect", "count", "collect_categorical_all_equal"})


def _pin_input_fact_type_ids(pins: Any, out: set[str]) -> None:
    """A rule's own ``pins`` entries with ``role == "input"`` name a fact
    type read directly as a single pinned value, never through a family
    collect (e.g. a field-mapping/cross-form-bridge rule's scope pin, or a
    companion-authority pin). This is the genuine non-collect consumption
    edge the rule-artifact ``pin`` schema shape (``{role, id, version,
    origin}``) declares; a pin's ``role`` of ``parameter``, ``choice``,
    ``default``, ``composition``, ``citation``, or ``operation-semantics``
    is metadata or configuration, not a fact-type read, and is deliberately
    excluded."""
    if not isinstance(pins, list):
        return
    for pin in pins:
        if isinstance(pin, dict) and pin.get("role") == "input" and isinstance(pin.get("id"), str):
            out.add(pin["id"])


def _walk_semantic_fact_type_refs(value: Any, out: set[str]) -> None:
    """Recursively collect fact-type ids from exact semantic reference
    fields only -- the fields that create a real derivation or admission
    edge -- never free-text/metadata fields such as ``notes``, ``title``,
    a citation block's own identity, or any other string that merely
    happens to match a fact-type id (the exact reproduction an independent
    review used against the prior blanket-string scanner: a metadata-only
    member with an incidental ``subject`` field).

    Recognized shapes (verified against every rule-artifact, source-family,
    source-closure-mapping, attachment-rule, and checked-conclusion-binding
    schema version actually adopted by the production package):

    - A ``collect``/``count``/``collect_categorical_all_equal`` expression
      node's own ``name`` field.
    - Any key ending in ``fact_type`` (``fact_type``, ``member_fact_type``,
      ``conclusion_fact_type``, ``recorded_boxes_fact_type``, ...) whose
      value is either the fact-type id string directly (a source-family's
      ``member_predicate.fact_type``) or an ``{id, version}`` exact-pin
      object (a closure-mapping's ``member_fact_type``, a rule expression's
      ``category_literal.fact_type``, a checked-conclusion-binding's
      ``conclusion_fact_type``/``components[].fact_type``, an
      attachment-rule itemization row's ``member_fact_type``, or a
      completeness ``required_answers[].fact_type``).
    - A pin entry naming a fact type read as a genuine non-collect input
      (see ``_pin_input_fact_type_ids``).
    """
    if isinstance(value, dict):
        op = value.get("op")
        name = value.get("name")
        if op in _FACT_TYPE_COLLECT_OPS and isinstance(name, str):
            out.add(name)
        for key, nested in value.items():
            if key.endswith("fact_type"):
                if isinstance(nested, str):
                    out.add(nested)
                elif isinstance(nested, dict) and isinstance(nested.get("id"), str):
                    out.add(nested["id"])
            if key == "pins":
                _pin_input_fact_type_ids(nested, out)
            _walk_semantic_fact_type_refs(nested, out)
    elif isinstance(value, list):
        for item in value:
            _walk_semantic_fact_type_refs(item, out)


def _referenced_fact_type_ids(package_members: Iterable[Mapping[str, Any]]) -> set[str]:
    """Every fact-type id genuinely consumed by the adopted package's own
    non-bundle content: a family's member predicate, a closure mapping's
    member fact type, a rule's ``collect``/``count``/categorical-witness
    expression operand, a rule's own directly-pinned input, an attachment's
    itemization row or completeness answer, or a checked-conclusion-
    binding's component -- exactly the fields that create a real
    derivation or admission edge (see ``_walk_semantic_fact_type_refs``).
    Metadata-only fields (a citation's own identity, ``notes``, ``title``,
    or any other free-text/incidental field) are never traversed, so an
    unrelated member whose non-semantic field happens to contain a fact-
    type-id string can never manufacture a false consumption claim. A fact
    type's own declaring bundle is excluded so a fact type is never counted
    as its own consumer. This can still only under-count a real consumer
    that lives entirely outside the package's own declarative content (a
    Python-level check with no corresponding pin or field, if one exists);
    it never over-counts, so it never manufactures a false coverage claim
    (T9, milestone exit criterion 8)."""
    referenced: set[str] = set()
    for member in package_members:
        if member.get("schema") in _BUNDLE_SCHEMAS:
            continue
        _walk_semantic_fact_type_refs(member, referenced)
    return referenced


@dataclass(frozen=True)
class UntranslatedFinding:
    """One current finding of a fact type this product recognizes -- it is
    declared by a real, committed ``bundle-adoption`` act, so contributing
    it is never rejected as unrecognized input -- but that the adopted
    package's own rules, families, and mappings never read: no subtotal,
    consequence, or return line is computed from it, and it can never be
    silently folded into one that might look complete without it (T9,
    milestone exit criterion 8; extends ADR-0016 decision 3's own principle
    past closed families to fact types that have no family at all)."""

    fact_type_id: str
    fact_type_title: str
    finding_id: str
    fact_id: str
    value: Any


def untranslated_source_findings(
    state: FindingState,
    package_members: Iterable[Mapping[str, Any]],
) -> list[UntranslatedFinding]:
    """Every current source-amount finding whose fact type the workspace
    recognizes (``state.fact_state.fact_types``, populated only by a real
    ``bundle-adoption`` act -- never invented here) but the adopted
    package never consumes. Withdrawn fact ids are excluded exactly as
    ``findings._current_value_for_fact`` excludes them, and the
    last-inserted finding for a fact id wins, mirroring the same
    last-write rule."""
    referenced = _referenced_fact_type_ids(package_members)
    declared = {
        fact_type_id: fact_type
        for fact_type_id, fact_type in state.fact_state.fact_types.items()
        if fact_type.get("source_amount") is True
    }
    unsupported_ids = {fact_type_id for fact_type_id in declared if fact_type_id not in referenced}
    if not unsupported_ids:
        return []

    current_by_fact_id: dict[str, dict[str, Any]] = {}
    for finding in state.findings.values():
        fact_id = finding["fact_id"]
        fact_type_id = fact_id.split("|", 1)[0]
        if fact_type_id not in unsupported_ids:
            continue
        current_by_fact_id[fact_id] = finding

    results = [
        UntranslatedFinding(
            fact_type_id=fact_id.split("|", 1)[0],
            fact_type_title=declared[fact_id.split("|", 1)[0]]["title"],
            finding_id=finding["id"],
            fact_id=fact_id,
            value=finding["value"],
        )
        for fact_id, finding in current_by_fact_id.items()
        if fact_id not in state.withdrawn_fact_ids
    ]
    return sorted(results, key=lambda item: (item.fact_type_id, item.fact_id))
