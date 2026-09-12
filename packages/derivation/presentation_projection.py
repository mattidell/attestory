"""Internal presentation projector (Presentation L2 Integration Grounding, Track 1).

Builds the citation-walk renderer's input model from exactly the four things
already available inside a successful ``live_coordinate_run``: the resolved
exclusive graph, the projected record state, ``RunResult.publications``, and
``RunResult.dispositions``. This is an internal implementation shape with its
own version and strict validator (below) — never a published schema, citizen,
or caller-facing contract (ADR-0046 is unchanged; this module does not
instantiate it).

The model's ``unsupportedSourceFindings`` list is the same two inputs this
projector already holds (``state`` and ``resolved_members``) run through
``packages.tax.coverage.untranslated_source_findings`` (T9, milestone exit
criterion 9): every current source-amount finding whose fact type the
workspace recognizes but the adopted package's own content never genuinely
consumes. This makes the unsupported boundary recoverable from the durable
run's own presentation output, not only from a caller invoking the coverage
helper directly against a separately reconstructed state.

The projector performs no tax arithmetic and invents no display value,
citation, attachment state, diagnostic, or label: every string that reaches
the model is either a value the coordinator itself published/recorded, or
content already declared on a resolved citizen (a form-field's own label/
description/citation, an attachment's own title/itemization label, or a raw
finding's own evidence label). Joins are by declared symbol and exact pin;
any missing or ambiguous join, unknown disposition, or invalid numeric
publication raises :class:`PresentationModelError` (fail closed, ADR-0046
zero-authority) rather than guessing or rendering a fabricated value.
"""

from __future__ import annotations

import re
import inspect
from decimal import Decimal, InvalidOperation
from typing import Any, Mapping, Sequence, cast

from packages.derivation.derived_enumeration import derived_activity_present, fact_type_matches_symbol
from packages.kernel.findings import FindingState
from packages.tax.coverage import untranslated_source_findings

PRESENTATION_MODEL_VERSION = "presentation-model.v1"

# form-field.v2 and .v3 share an identical renderer-facing shape (schema,
# id, version, form, line, label, description, binds_symbol, citation,
# dispositions); v3 only reconciles the blocked-code enum
# (SOURCE_SET_UNCLOSED, the code the runner actually emits) and is not a
# distinct presentation contract. Both are recognized field citizens.
FIELD_SCHEMAS = frozenset({"form-field.v2", "form-field.v3"})
ATTACHMENT_SCHEMAS = frozenset(
    {"attachment-rule.v1", "attachment-rule.v2", "attachment-rule.v3", "attachment-rule.v4", "attachment-rule.v5", "attachment-rule.v6", "attachment-rule.v8", "attachment-rule.v11", "attachment-rule.v10"}
)

_NUMERIC_DISPOSITIONS = frozenset({"published_value", "computed_zero", "closure_backed_zero"})
# A field may declare one fixed, non-numeric publication instruction.  This is
# deliberately a presentation disposition rather than a value kind: the
# renderer receives only the field's declared instruction and never the
# categorical value which made the rule publish.
_CATEGORICAL_DISPOSITIONS = frozenset({"published_categorical"})
_KNOWN_DISPOSITIONS = _NUMERIC_DISPOSITIONS | _CATEGORICAL_DISPOSITIONS | {"blocked", "guard_inapplicable"}
_DEPENDENCY_ROLES = frozenset({"input", "choice"})
_CLOSURE_FACT_MARKER = ".source-closure"

# Defense-in-depth against the __FIXTURE_JSON__ literal-text splice
# (tools/presentation_harness/lib/server.mjs): the model is spliced into a
# <script> block as raw bytes, never through JSON.parse, so any string
# containing a script-closing or comment-opening sequence could break out of
# that context. No content this projector forwards should ever legitimately
# contain one; a match is a rejection, not a repair.
_UNSAFE_STRING_PATTERN = re.compile(r"</script|<!--", re.IGNORECASE)


class PresentationModelError(Exception):
    """The presentation model cannot be constructed or fails strict validation."""


def _presentation_bound_family(schema: str) -> str | None:
    """Return the presentation-bound family name, or None if not bound.

    Family membership is the explicit ``form-field.`` / ``attachment-rule.``
    prefix required by ADR-0066 Decision 7. Support itself is the closed
    ``FIELD_SCHEMAS`` / ``ATTACHMENT_SCHEMAS`` sets, not numeric version parsing.
    """
    if schema.startswith("form-field."):
        return "form-field"
    if schema.startswith("attachment-rule."):
        return "attachment-rule"
    return None


def _reject_unsupported_presentation_schemas(resolved_members: Sequence[Mapping[str, Any]]) -> None:
    """Fail closed on unknown form-field or attachment-rule successors."""
    for member in resolved_members:
        schema = member.get("schema")
        if not isinstance(schema, str):
            continue
        family = _presentation_bound_family(schema)
        if family is None:
            continue
        supported = FIELD_SCHEMAS if family == "form-field" else ATTACHMENT_SCHEMAS
        if schema not in supported:
            raise PresentationModelError(
                f"unsupported {family} schema {schema!r} on {member.get('id')!r}"
            )


def _rules_by_id(members: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {member["id"]: member for member in members if "publishes" in member}


def _dispositions_by_symbol(
    dispositions: Sequence[Mapping[str, Any]], rules_by_id: Mapping[str, Mapping[str, Any]]
) -> dict[str, list[Mapping[str, Any]]]:
    by_symbol: dict[str, list[Mapping[str, Any]]] = {}
    for row in dispositions:
        symbol = row.get("symbol")
        if symbol is None:
            rule = rules_by_id.get(row["artifact_id"])
            if rule is None:
                raise PresentationModelError(f"disposition cites unknown rule {row['artifact_id']!r}")
            symbol = rule["publishes"]
        by_symbol.setdefault(symbol, []).append(row)
    return by_symbol


def _one_row(rows: Sequence[Mapping[str, Any]], *, symbol: str) -> Mapping[str, Any]:
    if len(rows) != 1:
        raise PresentationModelError(
            f"missing or ambiguous disposition join for symbol {symbol!r}: {len(rows)} row(s)"
        )
    return rows[0]


def _is_closure_finding(finding_id: str, state: FindingState) -> bool:
    finding = state.findings.get(finding_id)
    return finding is not None and _CLOSURE_FACT_MARKER in finding.get("fact_id", "")


def _leaf_pins(
    pins: Sequence[Mapping[str, Any]],
    *,
    publications_by_id: Mapping[str, Mapping[str, Any]],
    seen: frozenset[str],
) -> set[tuple[str, str]]:
    """Walk 'input'/'choice' pins down to non-derived leaves, as (id, version).

    A leaf whose id is itself a derived finding is recursed into; any other
    leaf is returned verbatim, carrying the exact version its own pin already
    declared (never re-derived or invented here).
    """
    leaves: set[tuple[str, str]] = set()
    for pin in pins:
        if pin["role"] not in _DEPENDENCY_ROLES:
            continue
        finding_id = pin["id"]
        if finding_id in seen:
            continue
        derived = publications_by_id.get(finding_id)
        if derived is not None:
            leaves |= _leaf_pins(derived["pins"], publications_by_id=publications_by_id, seen=seen | {finding_id})
        else:
            leaves.add((finding_id, pin["version"]))
    return leaves


def _raw_leaves(
    pins: Sequence[Mapping[str, Any]],
    *,
    publications_by_id: Mapping[str, Mapping[str, Any]],
    state: FindingState,
    root_id: str,
) -> set[tuple[str, str]]:
    leaves = _leaf_pins(pins, publications_by_id=publications_by_id, seen=frozenset({root_id}))
    for finding_id, _version in leaves:
        if finding_id not in state.findings:
            raise PresentationModelError(f"citation lineage references unrecorded finding {finding_id!r}")
    return leaves


def _numeric_value(raw: Any, *, symbol: str) -> int | float:
    try:
        decimal_value = Decimal(str(raw))
    except (InvalidOperation, ValueError) as exc:
        raise PresentationModelError(f"invalid numeric publication for symbol {symbol!r}: {raw!r}") from exc
    as_int = int(decimal_value)
    return as_int if Decimal(as_int) == decimal_value else float(decimal_value)


def _classify_numeric(
    value: int | float, leaves: set[tuple[str, str]], state: FindingState
) -> tuple[str, set[tuple[str, str]]]:
    source_leaves = {leaf for leaf in leaves if not _is_closure_finding(leaf[0], state)}
    closure_leaves = leaves - source_leaves
    if value != 0:
        return "published_value", source_leaves
    if source_leaves:
        return "computed_zero", source_leaves
    if closure_leaves:
        return "closure_backed_zero", set()
    raise PresentationModelError("zero-valued publication has neither source nor closure evidence")


def _evidence_label(finding_id: str, state: FindingState) -> str | None:
    """The finding's own current evidence label, or None (no invented text).

    A directly attested finding with no evidence reference is legitimate
    (``basis: "attested"``, no documentary backing) — the renderer's own
    ``pinLabel()`` fallback already displays ``pinId@pinVersion`` when no
    label is declared, so an absent label is not a rejection.
    """
    finding = state.findings[finding_id]
    for evidence_id in finding.get("evidence_ids") or ():
        lifecycle = state.evidence.get(evidence_id)
        if lifecycle is not None:
            return cast(str, lifecycle.evidence["label"])
    return None


def _citation_site(site_id: str, finding_id: str, version: str, context: str) -> dict[str, Any]:
    return {"siteId": site_id, "pinId": finding_id, "pinVersion": version, "context": context}


def _resolve_field_row(
    row: Mapping[str, Any],
    field: Mapping[str, Any],
    *,
    section_id: str,
    publications_by_id: Mapping[str, Mapping[str, Any]],
    state: FindingState,
    run_id: str,
    pin_labels: dict[str, str],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    disposition = row["disposition"]
    if disposition == "blocked":
        codes = [row["code"]] if "code" in row else []
        return {"disposition": "blocked", "activeCodes": codes, "act": None}, []
    if disposition == "inapplicable":
        if row.get("guard_result") is False:
            return {"disposition": "guard_inapplicable", "act": None}, []
        raise PresentationModelError(f"unrecognized inapplicable disposition for field {field['id']!r}")
    if disposition != "published":
        raise PresentationModelError(f"unknown disposition {disposition!r} for field {field['id']!r}")

    finding_id = row["finding_id"]
    finding = publications_by_id.get(finding_id)
    if finding is None:
        raise PresentationModelError(f"published row cites unrecorded finding {finding_id!r}")
    instruction = field.get("dispositions", {}).get("published_value")
    if not isinstance(instruction, Mapping) or not isinstance(instruction.get("render"), str):
        raise PresentationModelError(f"published field {field['id']!r} lacks a declared render instruction")
    # Numeric fields are the established ``{value}`` form.  A fixed
    # categorical instruction is admitted only for the declared affirmative
    # checkbox form; its source value is deliberately not copied to the model.
    if instruction["render"] != "{value}":
        if not isinstance(finding.get("value"), str) or finding["value"] != instruction["render"]:
            raise PresentationModelError(f"invalid categorical publication for field {field['id']!r}")
        _raw_leaves(finding["pins"], publications_by_id=publications_by_id, state=state, root_id=finding_id)
        return {"disposition": "published_categorical", "act": {"run_id": run_id, "finding": finding}}, []

    value = _numeric_value(finding["value"], symbol=finding["symbol"])
    leaves = _raw_leaves(finding["pins"], publications_by_id=publications_by_id, state=state, root_id=finding_id)
    kind, citation_leaves = _classify_numeric(value, leaves, state)

    citation_sites: list[dict[str, Any]] = []
    for index, (leaf_id, leaf_version) in enumerate(sorted(citation_leaves)):
        label = _evidence_label(leaf_id, state)
        if label is not None:
            # The renderer's pinLabel() looks up FIXTURE.pinLabels by bare
            # pin id only (never id@version) — match that lookup exactly.
            if leaf_id in pin_labels and pin_labels[leaf_id] != label:
                raise PresentationModelError(f"conflicting citation labels for pin {leaf_id!r}")
            pin_labels[leaf_id] = label
        citation_sites.append(_citation_site(f"{section_id}-src-{index}", leaf_id, leaf_version, field["label"]))

    act = {"run_id": run_id, "finding": finding}
    return {"disposition": kind, "value": value, "act": act}, citation_sites


def _section_id(field: Mapping[str, Any]) -> str:
    return f"line-{field['line']}"


def _citation_identity(citation: Any, *, owner: str) -> tuple[str, str]:
    """Return one declared citation identity, rejecting malformed references."""
    if not isinstance(citation, Mapping):
        raise PresentationModelError(f"{owner} lacks a well-formed citation")
    citation_id, citation_version = citation.get("id"), citation.get("version")
    if not isinstance(citation_id, str) or not citation_id or not isinstance(citation_version, str) or not citation_version:
        raise PresentationModelError(f"{owner} has an invalid citation")
    return citation_id, citation_version


def _require_declared_field_citation_chain(
    field: Mapping[str, Any], row: Mapping[str, Any], rules_by_id: Mapping[str, Mapping[str, Any]],
    citations: Mapping[tuple[str, str], Mapping[str, Any]],
) -> None:
    """Validate a field → owning-rule → graph citation chain when declared.

    Historical rules with no ``citations`` declaration remain on their
    established presentation path.  Once a rule declares citations, however,
    the chain is exact and fail-closed for every field without tax-specific
    identifiers or branches.
    """
    artifact_id = row.get("artifact_id")
    rule = rules_by_id.get(artifact_id) if isinstance(artifact_id, str) else None
    if rule is None or rule.get("publishes") != field.get("binds_symbol"):
        raise PresentationModelError(f"field {field['id']!r} lacks a joined owning rule")
    rule_citations = rule.get("citations")
    if not rule_citations:
        return
    if not isinstance(rule_citations, list):
        raise PresentationModelError(f"owning rule {rule['id']!r} has invalid citations")
    identity = _citation_identity(field.get("citation"), owner=f"field {field['id']!r}")
    exact = sum(_citation_identity(item, owner=f"owning rule {rule['id']!r}") == identity for item in rule_citations)
    if exact != 1:
        raise PresentationModelError(f"owning rule {rule['id']!r} must declare the field citation exactly once")
    if identity not in citations:
        raise PresentationModelError(f"field {field['id']!r} cites an unresolved field citation")


def _recorded_derived_pin_identities(
    finding_id: str,
    publications_by_id: Mapping[str, Mapping[str, Any]],
    *,
    seen: frozenset[str],
) -> set[tuple[str, str]]:
    finding = publications_by_id.get(finding_id)
    if finding is None:
        return set()
    identities: set[tuple[str, str]] = set()
    next_seen = seen | {finding_id}
    for pin in finding.get("pins") or []:
        if not isinstance(pin, Mapping):
            continue
        pin_id = pin.get("id")
        version = pin.get("version") or "v1"
        role = pin.get("role")
        if not isinstance(pin_id, str) or not pin_id:
            continue
        if pin_id in next_seen:
            continue
        if role in {"citation", "computation"}:
            identities.add((pin_id, str(version)))
        elif role in {"input", "choice"}:
            if pin_id in publications_by_id:
                identities |= _recorded_derived_pin_identities(
                    pin_id, publications_by_id, seen=next_seen
                )
            else:
                identities.add((pin_id, str(version)))
    return identities


def _reader_label_for_finding(finding: Mapping[str, Any], adjustment_label: str) -> str:
    symbol = finding.get("symbol")
    if isinstance(symbol, str):
        tail = symbol.rsplit("|", 1)[-1]
        for piece in tail.split(","):
            piece = piece.strip()
            if piece.startswith("payer="):
                return f"{adjustment_label} — {piece.split('=', 1)[1]}"
    return f"{adjustment_label} report group"


def _pin_identity(value: Any) -> tuple[str, str] | None:
    if not isinstance(value, Mapping):
        return None
    pin_id, version = value.get("id"), value.get("version")
    if not isinstance(pin_id, str) or not pin_id or not isinstance(version, str) or not version:
        return None
    return pin_id, version


def _declared_adjustment_specs(adjustment: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Flatten direct/selected declarations into presentation join specs."""
    common = {
        "kind": adjustment.get("kind"),
        "label": adjustment.get("label"),
        "sign": adjustment.get("sign"),
    }
    selection = adjustment.get("selection")
    if isinstance(selection, Mapping):
        specs: list[dict[str, Any]] = []
        for path in selection.get("paths") or []:
            if not isinstance(path, Mapping):
                continue
            spec = dict(common)
            spec.update({
                "path_id": path.get("id"),
                "rows": path.get("rows"),
                "subtotal_symbol": path.get("subtotal_symbol"),
            })
            specs.append(spec)
        return specs
    spec = dict(common)
    spec.update({
        "rows": adjustment.get("rows"),
        "subtotal_symbol": adjustment.get("subtotal_symbol"),
    })
    return [spec]


def _serialized_row_matches(
    serialized: Mapping[str, Any],
    declared: Mapping[str, Any],
    publications_by_id: Mapping[str, Mapping[str, Any]],
) -> bool:
    """Join one serialized adjustment row to its declared producer shape."""
    for key in ("kind", "label", "sign"):
        if serialized.get(key) != declared.get(key):
            return False
    subtotal = serialized.get("subtotal")
    if not isinstance(subtotal, Mapping) or subtotal.get("symbol") != declared.get("subtotal_symbol"):
        return False
    rows_spec = declared.get("rows")
    if not isinstance(rows_spec, Mapping):
        return False
    operation = rows_spec.get("op")
    if operation == "collect_members":
        return _pin_identity(serialized.get("source_family")) == _pin_identity(rows_spec.get("source_family"))
    if operation != "enumerate_published":
        return False
    fact_type = rows_spec.get("fact_type")
    serialized_fact_type = serialized.get("fact_type")
    if _pin_identity(fact_type) == _pin_identity(serialized_fact_type):
        return True
    prefix = rows_spec.get("symbol_prefix")
    if not isinstance(prefix, str) or not prefix:
        return False
    serialized_rows = serialized.get("rows")
    if not isinstance(serialized_rows, list) or not serialized_rows:
        return False
    for row in serialized_rows:
        if not isinstance(row, Mapping) or not isinstance(row.get("finding_id"), str):
            return False
        finding = publications_by_id.get(row["finding_id"])
        if finding is None or not isinstance(finding.get("symbol"), str) or not finding["symbol"].startswith(prefix):
            return False
    return True


def _declared_adjustment_active(
    declared: Mapping[str, Any],
    *,
    current_finding_ids: frozenset[str],
    state: FindingState,
    publications_by_id: Mapping[str, Mapping[str, Any]],
    dispositions: Sequence[Mapping[str, Any]],
) -> bool:
    rows_spec = declared.get("rows")
    if not isinstance(rows_spec, Mapping):
        return False
    operation = rows_spec.get("op")
    if operation == "collect_members":
        member_pin = _pin_identity(rows_spec.get("member_fact_type"))
        if member_pin is None:
            return False
        fact_type_id, _version = member_pin
        prefix = f"{fact_type_id}|"
        return any(
            finding_id in current_finding_ids
            and isinstance(state.findings.get(finding_id, {}).get("fact_id"), str)
            and (
                state.findings[finding_id]["fact_id"] == fact_type_id
                or state.findings[finding_id]["fact_id"].startswith(prefix)
            )
            for finding_id in current_finding_ids
        )
    if operation == "enumerate_published":
        fact_pin = _pin_identity(rows_spec.get("fact_type"))
        if fact_pin is not None:
            fact_type_id, _version = fact_pin
            return derived_activity_present(
                publications=list(publications_by_id.values()),
                dispositions=dispositions,
                fact_type_id=fact_type_id,
            )
        symbol_prefix: Any = rows_spec.get("symbol_prefix")
        return isinstance(symbol_prefix, str) and any(
            isinstance(finding.get("symbol"), str) and finding["symbol"].startswith(symbol_prefix)
            for finding in publications_by_id.values()
        )
    return False


def _current_adjustment_contributor_ids(
    declared: Mapping[str, Any],
    *,
    current_finding_ids: frozenset[str],
    state: FindingState,
    publications_by_id: Mapping[str, Mapping[str, Any]],
) -> frozenset[str]:
    rows_spec = declared.get("rows")
    if not isinstance(rows_spec, Mapping):
        return frozenset()
    if rows_spec.get("op") == "collect_members":
        member_pin = _pin_identity(rows_spec.get("member_fact_type"))
        if member_pin is None:
            return frozenset()
        fact_type_id, _version = member_pin
        return frozenset(
            finding_id
            for finding_id in current_finding_ids
            if isinstance(state.findings.get(finding_id, {}).get("fact_id"), str)
            and (
                state.findings[finding_id]["fact_id"] == fact_type_id
                or state.findings[finding_id]["fact_id"].startswith(f"{fact_type_id}|")
            )
        )
    if rows_spec.get("op") == "enumerate_published":
        fact_pin = _pin_identity(rows_spec.get("fact_type"))
        prefix = fact_pin[0] if fact_pin is not None else rows_spec.get("symbol_prefix")
        if not isinstance(prefix, str):
            return frozenset()
        return frozenset(
            finding_id
            for finding_id, finding in publications_by_id.items()
            if isinstance(finding.get("symbol"), str)
            and (
                fact_type_matches_symbol(finding["symbol"], prefix)
                if fact_pin is not None
                else finding["symbol"].startswith(prefix)
            )
        )
    return frozenset()


def _serialized_adjustment_contributors_match(
    serialized: Mapping[str, Any],
    declared: Mapping[str, Any],
    *,
    current_finding_ids: frozenset[str],
    state: FindingState,
    publications_by_id: Mapping[str, Mapping[str, Any]],
) -> bool:
    rows = serialized.get("rows")
    if not isinstance(rows, list):
        return False
    contributor_ids: list[str] = []
    for row in rows:
        if not isinstance(row, Mapping) or not isinstance(row.get("finding_id"), str):
            return False
        contributor_ids.append(row["finding_id"])
    if len(contributor_ids) != len(set(contributor_ids)):
        return False
    return frozenset(contributor_ids) == _current_adjustment_contributor_ids(
        declared,
        current_finding_ids=current_finding_ids,
        state=state,
        publications_by_id=publications_by_id,
    )


def _validate_serialized_adjustment_correspondence(
    attachment: Mapping[str, Any],
    itemization: Mapping[str, Any],
    value_itemization: Mapping[str, Any],
    publications_by_id: Mapping[str, Mapping[str, Any]],
    state: FindingState,
    dispositions: Sequence[Mapping[str, Any]],
) -> list[Mapping[str, Any]]:
    """Require serialized adjustment rows to be declared and, for v11, selected."""
    declared_adjustments = [
        adjustment for adjustment in itemization.get("adjustment_rows", [])
        if isinstance(adjustment, Mapping)
    ]
    serialized = value_itemization.get("adjustment_rows")
    if not isinstance(serialized, list):
        raise PresentationModelError("attachment finding has malformed adjustment_rows")
    serialized_rows: list[Mapping[str, Any]] = []
    for index, row in enumerate(serialized):
        if not isinstance(row, Mapping):
            raise PresentationModelError(f"serialized adjustment row {index} is not an object")
        serialized_rows.append(row)

    needs_activity = attachment.get("schema") == "attachment-rule.v11"
    if needs_activity:
        from packages.kernel.currency import compute_currency

        current_finding_ids = compute_currency(state).current_finding_ids
    else:
        current_finding_ids = frozenset()
    used: set[int] = set()
    row_claims: dict[int, int] = {}
    for adjustment in declared_adjustments:
        claim_key = id(adjustment)
        specs = _declared_adjustment_specs(adjustment)
        if not specs:
            raise PresentationModelError("adjustment declaration has no joinable row or selection path")
        is_selection = isinstance(adjustment.get("selection"), Mapping)
        if is_selection:
            active_specs = [
                spec for spec in specs
                if _declared_adjustment_active(
                    spec,
                    current_finding_ids=current_finding_ids,
                    state=state,
                    publications_by_id=publications_by_id,
                    dispositions=dispositions,
                )
            ]
            if len(active_specs) > 1:
                raise PresentationModelError(
                    f"selected adjustment {adjustment.get('label')!r} has multiple active paths"
                )
            matched_rows: list[tuple[int, Any]] = []
            for index, row in enumerate(serialized_rows):
                matching_specs = [
                    spec for spec in specs
                    if _serialized_row_matches(row, spec, publications_by_id)
                ]
                if len(matching_specs) > 1:
                    raise PresentationModelError(
                        f"serialized adjustment row {index} ambiguously matches selected paths"
                    )
                if matching_specs:
                    matched_rows.append((index, matching_specs[0].get("path_id")))
            selected_paths = {path_id for _index, path_id in matched_rows}
            if len(selected_paths) > 1:
                raise PresentationModelError(
                    f"selected adjustment {adjustment.get('label')!r} has multiple serialized paths"
                )
            if len(active_specs) == 1:
                active_path_id: Any = active_specs[0].get("path_id")
                active_spec = active_specs[0]
                active_contributors = _current_adjustment_contributor_ids(
                    active_spec,
                    current_finding_ids=current_finding_ids,
                    state=state,
                    publications_by_id=publications_by_id,
                )
                active_fact_pin = _pin_identity(active_spec.get("rows", {}).get("fact_type"))
                if (
                    active_spec.get("rows", {}).get("op") == "enumerate_published"
                    and not active_contributors
                    and active_fact_pin is not None
                    and any(
                        row.get("disposition") == "blocked"
                        and isinstance(row.get("symbol"), str)
                        and fact_type_matches_symbol(row["symbol"], active_fact_pin[0])
                        for row in dispositions
                    )
                ):
                    raise PresentationModelError(
                        f"active adjustment path {active_path_id!r} is blocked and cannot publish contributors"
                    )
                active_rows = [
                    index for index, path_id in matched_rows if path_id == active_path_id
                ]
                if len(active_rows) != 1:
                    raise PresentationModelError(
                        f"active adjustment path {active_path_id!r} lacks exactly one serialized row"
                    )
                if not _serialized_adjustment_contributors_match(
                    serialized_rows[active_rows[0]],
                    active_spec,
                    current_finding_ids=current_finding_ids,
                    state=state,
                    publications_by_id=publications_by_id,
                ):
                    raise PresentationModelError(
                        f"active adjustment path {active_path_id!r} has incorrect contributors"
                    )
            elif matched_rows:
                raise PresentationModelError(
                    f"serialized adjustment {adjustment.get('label')!r} has no active declared path"
                )
            for index, _path_id in matched_rows:
                prior_claim = row_claims.get(index)
                if prior_claim is not None and prior_claim != claim_key:
                    raise PresentationModelError(
                        f"serialized adjustment row {index} satisfies multiple declarations"
                    )
                row_claims[index] = claim_key
                used.add(index)
            continue
        matches = [
            index for index, row in enumerate(serialized_rows)
            if _serialized_row_matches(row, specs[0], publications_by_id)
        ]
        if len(matches) != 1:
            raise PresentationModelError(
                f"serialized adjustment rows do not correspond exactly to declared {adjustment.get('label')!r}"
            )
        row_index = matches[0]
        if row_index in row_claims:
            raise PresentationModelError(
                f"serialized adjustment row {row_index} satisfies multiple declarations"
            )
        if attachment.get("schema") == "attachment-rule.v11" and not _serialized_adjustment_contributors_match(
            serialized_rows[row_index],
            specs[0],
            current_finding_ids=current_finding_ids,
            state=state,
            publications_by_id=publications_by_id,
        ):
            raise PresentationModelError(
                f"direct adjustment {adjustment.get('label')!r} has incorrect contributors"
            )
        row_claims[row_index] = claim_key
        used.add(row_index)

    if len(used) != len(serialized_rows):
        raise PresentationModelError("serialized adjustment rows contain an undeclared adjustment")
    return serialized_rows


def _resolve_attachment(
    attachment: Mapping[str, Any],
    *,
    dispositions_by_symbol: Mapping[str, list[Mapping[str, Any]]],
    publications_by_id: Mapping[str, Mapping[str, Any]],
    state: FindingState,
    pin_labels: dict[str, str],
    dispositions: Sequence[Mapping[str, Any]] | None = None,
    provenance_out: list[dict[str, Any]] | None = None,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    """Resolve one attachment citizen to its status entry and, only when
    published, its itemization detail (ADR-0056).

    Returns ``(status, citation_group)``. ``status`` is always present -
    one of the three atomic dispositions (ADR-0036 Decision 1), never
    silence - and feeds the model's ``attachments`` list. ``citation_group``
    is non-``None`` only for the published case and feeds the unchanged
    ``citationGroups`` list, exactly as before this ADR.
    """
    symbol = attachment["publishes"]
    row = _one_row(dispositions_by_symbol.get(symbol, []), symbol=symbol)
    attachment_id = attachment["id"]
    title = attachment["title"].split(":", 1)[0].strip()

    if row["disposition"] == "inapplicable":
        if row.get("guard_result") is not False:
            raise PresentationModelError(f"unrecognized inapplicable disposition for attachment {attachment['id']!r}")
        status = {
            "id": attachment_id, "title": title,
            "resolved": {"disposition": "guard_inapplicable", "activeCodes": [], "act": None},
        }
        return status, None
    if row["disposition"] == "blocked":
        codes = [row["code"]] if "code" in row else []
        status = {
            "id": attachment_id, "title": title,
            "resolved": {"disposition": "blocked", "activeCodes": codes, "act": None},
        }
        return status, None
    if row["disposition"] != "published":
        raise PresentationModelError(f"unknown disposition {row['disposition']!r} for attachment {attachment['id']!r}")

    attachment_finding = publications_by_id.get(row.get("finding_id", ""))
    if attachment_finding is None:
        raise PresentationModelError(f"attachment cites unrecorded finding {row.get('finding_id')!r}")
    parts: list[dict[str, Any]] = []
    for itemization in attachment["itemizations"]:
        tie_symbol = itemization["tie_out"]["line_symbol"]
        tie_row = _one_row(dispositions_by_symbol.get(tie_symbol, []), symbol=tie_symbol)
        if tie_row["disposition"] != "published":
            raise PresentationModelError(f"itemization tie-out {tie_symbol!r} is not published")
        finding = publications_by_id.get(tie_row["finding_id"])
        if finding is None:
            raise PresentationModelError(f"itemization tie-out cites unrecorded finding {tie_row['finding_id']!r}")
        value = _numeric_value(finding["value"], symbol=tie_symbol)
        part_id = itemization["part_id"]
        value_itemization = None
        if isinstance(attachment_finding.get("value"), dict):
            value_itemization = next(
                (entry for entry in attachment_finding["value"].get("itemizations", []) if entry.get("part_id") == part_id),
                None,
            )
        if attachment.get("schema") in ("attachment-rule.v6", "attachment-rule.v8", "attachment-rule.v11", "attachment-rule.v10"):
            if value_itemization is None:
                raise PresentationModelError(f"attachment finding omits itemization value for {part_id!r}")
            assert isinstance(value_itemization, dict)
            positive_ids = {
                row["finding_id"]
                for row_set in value_itemization.get("row_sets", [])
                for row in row_set.get("rows", [])
            }
            leaves = {(finding_id, "v1") for finding_id in positive_ids}
            for finding_id, _version in leaves:
                if finding_id not in state.findings:
                    raise PresentationModelError(f"citation lineage references unrecorded finding {finding_id!r}")
        else:
            leaves = _raw_leaves(
                finding["pins"], publications_by_id=publications_by_id, state=state, root_id=finding["id"]
            )
        sites: list[dict[str, Any]] = []
        for index, (leaf_id, leaf_version) in enumerate(sorted(leaves)):
            if _is_closure_finding(leaf_id, state):
                continue
            label = _evidence_label(leaf_id, state)
            if label is not None:
                if leaf_id in pin_labels and pin_labels[leaf_id] != label:
                    raise PresentationModelError(f"conflicting citation labels for pin {leaf_id!r}")
                pin_labels[leaf_id] = label
            sites.append(_citation_site(f"{part_id}-src-{index}", leaf_id, leaf_version, itemization["label"]))
        parts.append({
            "heading": itemization["label"],
            "citationSites": sites,
            "tieOutText": f"Reported subtotal: {value}",
        })
        if attachment.get("schema") in ("attachment-rule.v6", "attachment-rule.v8", "attachment-rule.v11", "attachment-rule.v10"):
            assert isinstance(value_itemization, dict)
            selected_adjustments = _validate_serialized_adjustment_correspondence(
                attachment,
                itemization,
                value_itemization,
                publications_by_id,
                state,
                dispositions or [row for rows in dispositions_by_symbol.values() for row in rows],
            )
            for adjustment_value in selected_adjustments:
                if not isinstance(adjustment_value, dict):
                    continue
                adj_label = str(adjustment_value.get("label") or "")
                adj_kind = str(adjustment_value.get("kind") or "")
                adjustment_sites: list[dict[str, Any]] = []
                existing_adjustment_part = next(
                    (
                        part for part in parts
                        if attachment.get("schema") == "attachment-rule.v11"
                        and part.get("heading") == adj_label
                        and part.get("adjustmentKind") == adj_kind
                    ),
                    None,
                )
                site_offset = len(existing_adjustment_part.get("citationSites", [])) if existing_adjustment_part else 0
                for index, row in enumerate(adjustment_value.get("rows", [])):
                    leaf_id = row["finding_id"]
                    # v11's derived nominee path itemizes a published finding
                    # rather than a projected source assertion.  Keep the
                    # row-level citation on that published finding; the
                    # provenance walk below expands it to the recorded source
                    # leaves.  Direct/legacy rows still require a projected
                    # finding, as before.
                    if leaf_id not in state.findings and not (
                        attachment.get("schema") == "attachment-rule.v11"
                        and leaf_id in publications_by_id
                        and str(leaf_id).startswith("finding:derived:")
                    ):
                        raise PresentationModelError(f"citation lineage references unrecorded finding {leaf_id!r}")
                    label = _evidence_label(leaf_id, state) if leaf_id in state.findings else None
                    if label is not None:
                        if leaf_id in pin_labels and pin_labels[leaf_id] != label:
                            raise PresentationModelError(f"conflicting citation labels for pin {leaf_id!r}")
                        pin_labels[leaf_id] = label
                    adjustment_sites.append(
                        _citation_site(
                            f"{part_id}-adjustment-{site_offset + index}",
                            leaf_id,
                            "v1",
                            adj_label,
                        )
                    )
                adjustment_part = {
                    "heading": adj_label,
                    "citationSites": adjustment_sites,
                    "tieOutText": f"Adjustment: -{adjustment_value['row_sum']}",
                }
                if attachment.get("schema") == "attachment-rule.v11":
                    # Preserve the producer's declared kind beside the
                    # displayed adjustment so standalone payload validation
                    # can check the group relationship without tax-specific
                    # labels or ids.
                    adjustment_part["adjustmentKind"] = adj_kind
                if existing_adjustment_part is None:
                    parts.append(adjustment_part)
                else:
                    # The form displays one aggregate adjustment label while
                    # provenanceGroups retain one group per report finding.
                    existing_adjustment_part["citationSites"].extend(adjustment_sites)
                    existing_adjustment_part["tieOutText"] += f"; {adjustment_part['tieOutText']}"
                if provenance_out is None:
                    continue
                for index, row in enumerate(adjustment_value.get("rows") or []):
                    fid = row.get("finding_id")
                    if not isinstance(fid, str) or not fid.startswith("finding:derived:"):
                        continue
                    finding = publications_by_id.get(fid)
                    if finding is None:
                        continue
                    finding_pins = finding.get("pins") or []
                    if not any(pin.get("role") == "citation" for pin in finding_pins if isinstance(pin, Mapping)):
                        raise PresentationModelError(
                            f"derived adjustment finding {fid!r} is missing citation lineage"
                        )
                    if not any(pin.get("role") == "computation" for pin in finding_pins if isinstance(pin, Mapping)):
                        raise PresentationModelError(
                            f"derived adjustment finding {fid!r} is missing rule lineage"
                        )
                    if not any(
                        pin.get("role") in {"input", "choice"}
                        for pin in finding_pins
                        if isinstance(pin, Mapping)
                    ):
                        raise PresentationModelError(
                            f"derived adjustment finding {fid!r} is missing contributing input lineage"
                        )
                    identities = _recorded_derived_pin_identities(
                        fid, publications_by_id, seen=frozenset()
                    )
                    if not identities:
                        raise PresentationModelError(
                            f"derived adjustment finding {fid!r} has empty recorded lineage"
                        )
                    reader = _reader_label_for_finding(finding, adj_label)
                    sites = []
                    for site_index, (leaf_id, leaf_version) in enumerate(sorted(identities)):
                        if leaf_id in state.findings:
                            elabel = _evidence_label(leaf_id, state)
                            if elabel is not None:
                                if leaf_id in pin_labels and pin_labels[leaf_id] != elabel:
                                    raise PresentationModelError(
                                        f"conflicting citation labels for pin {leaf_id!r}"
                                    )
                                pin_labels[leaf_id] = elabel
                        sites.append(
                            _citation_site(
                                f"provenance-{fid}-{site_index}",
                                leaf_id,
                                leaf_version,
                                reader,
                            )
                        )
                    provenance_out.append({
                        "id": fid,
                        "attachmentId": attachment_id,
                        "adjustmentKind": adj_kind,
                        "adjustmentLabel": adj_label,
                        "label": reader,
                        "citationSites": sites,
                        "tieOutText": f"Recorded contributing reduction {finding.get('value')}",
                    })

    group = {"id": attachment_id, "title": title, "parts": parts}
    status = {
        "id": attachment_id, "title": title,
        "resolved": {"disposition": "published", "activeCodes": [], "act": None},
    }
    return status, group


def build_presentation_model(
    *,
    run_id: str,
    resolved_members: Sequence[Mapping[str, Any]],
    state: FindingState,
    publications: Sequence[Any],
    dispositions: Sequence[Mapping[str, Any]],
    authorization: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the presentation-model.v1 payload from coordinator-internal state only.

    ``publications`` is ``RunResult.publications`` (a sequence of objects with
    an ``.act``/``.finding`` pair); ``dispositions`` is ``RunResult.dispositions``.
    Raises :class:`PresentationModelError` on any missing/ambiguous join,
    unknown disposition, invalid numeric publication, or untraceable citation
    lineage — never on a guess.

    ``authorization``, when supplied, is the production
    ``authorization.authorization_provenance(resolution)`` payload for this
    run's resolved standing authorization, so the resolved authorization
    reaches the production presentation/explanation root, not only the
    in-memory ``LiveCoordinatorOutcome``. Optional and omitted entirely from
    the model when ``None``, so existing callers that never resolve an
    authorization are unaffected.
    """
    _reject_unsupported_presentation_schemas(resolved_members)
    fields = [m for m in resolved_members if m.get("schema") in FIELD_SCHEMAS]
    attachments = [m for m in resolved_members if m.get("schema") in ATTACHMENT_SCHEMAS]
    rules_by_id = _rules_by_id(resolved_members)
    citations: dict[tuple[str, str], Mapping[str, Any]] = {}
    for member in resolved_members:
        if member.get("schema") == "citation.v1":
            identity = _citation_identity(member, owner="resolved citation citizen")
            if identity in citations:
                raise PresentationModelError(f"duplicate resolved citation identity {identity!r}")
            citations[identity] = member
    publications_by_id: dict[str, Mapping[str, Any]] = {}
    for publication in publications:
        finding = publication.finding
        finding_id = finding.get("id") if isinstance(finding, Mapping) else None
        if not isinstance(finding_id, str) or not finding_id:
            raise PresentationModelError("publication finding is missing a non-empty id")
        if finding_id in publications_by_id:
            raise PresentationModelError(f"duplicate publication finding id {finding_id!r}")
        publications_by_id[finding_id] = finding
    by_symbol = _dispositions_by_symbol(dispositions, rules_by_id)

    pin_labels: dict[str, str] = {}
    sections: list[dict[str, Any]] = []
    for field in sorted(fields, key=lambda f: f["id"]):
        symbol = field["binds_symbol"]
        row = _one_row(by_symbol.get(symbol, []), symbol=symbol)
        section_id = _section_id(field)
        resolved, citation_sites = _resolve_field_row(
            row, field, section_id=section_id, publications_by_id=publications_by_id,
            state=state, run_id=run_id, pin_labels=pin_labels,
        )
        if resolved["disposition"] in _NUMERIC_DISPOSITIONS | _CATEGORICAL_DISPOSITIONS:
            _require_declared_field_citation_chain(field, row, rules_by_id, citations)
        sections.append({
            "id": section_id,
            "field": dict(field),
            "resolved": resolved,
            "citationSites": citation_sites,
        })

    citation_groups: list[dict[str, Any]] = []
    attachments_out: list[dict[str, Any]] = []
    provenance_groups: list[dict[str, Any]] = []
    for attachment in sorted(attachments, key=lambda a: a["id"]):
        resolver_kwargs: dict[str, Any] = {
            "dispositions_by_symbol": by_symbol,
            "publications_by_id": publications_by_id,
            "state": state,
            "pin_labels": pin_labels,
            "dispositions": dispositions,
        }
        # The contract-unit prototype installs a temporary resolver wrapper
        # with the pre-carrier signature. Keep that exploratory harness
        # runnable while the production resolver receives the new collector
        # explicitly; no prototype behavior is part of admission.
        if "provenance_out" in inspect.signature(_resolve_attachment).parameters:
            resolver_kwargs["provenance_out"] = provenance_groups
        status, group = _resolve_attachment(attachment, **resolver_kwargs)
        attachments_out.append(status)
        if group is not None:
            citation_groups.append(group)

    unsupported_source_findings = [
        {
            "factTypeId": finding.fact_type_id,
            "factTypeTitle": finding.fact_type_title,
            "findingId": finding.finding_id,
            "factId": finding.fact_id,
            "value": finding.value,
        }
        for finding in untranslated_source_findings(state, resolved_members)
    ]

    model = {
        "schema": PRESENTATION_MODEL_VERSION,
        "runId": run_id,
        "pinLabels": pin_labels,
        "sections": sections,
        "citationGroups": citation_groups,
        "attachments": attachments_out,
        "unsupportedSourceFindings": unsupported_source_findings,
    }
    if provenance_groups:
        model["provenanceGroups"] = provenance_groups
    if authorization is not None:
        model["authorization"] = dict(authorization)
    validate_presentation_model(model)
    return model


def _check_no_unsafe_strings(value: Any, path: str) -> None:
    if isinstance(value, str):
        if _UNSAFE_STRING_PATTERN.search(value):
            raise PresentationModelError(f"{path}: contains an unsafe serialization sequence")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _check_no_unsafe_strings(item, f"{path}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str) or _UNSAFE_STRING_PATTERN.search(key):
                raise PresentationModelError(f"{path}: unsafe or non-string key {key!r}")
            _check_no_unsafe_strings(item, f"{path}.{key}")


def _require_keys(obj: Mapping[str, Any], required: frozenset[str], optional: frozenset[str], path: str) -> None:
    if not isinstance(obj, dict):
        raise PresentationModelError(f"{path}: expected an object")
    keys = set(obj)
    missing = required - keys
    if missing:
        raise PresentationModelError(f"{path}: missing key(s) {sorted(missing)}")
    unknown = keys - required - optional
    if unknown:
        raise PresentationModelError(f"{path}: unknown key(s) {sorted(unknown)}")


def _validate_citation_site(site: Mapping[str, Any], path: str) -> None:
    _require_keys(site, frozenset({"siteId", "pinId", "pinVersion", "context"}), frozenset(), path)
    for key in ("siteId", "pinId", "pinVersion", "context"):
        if not isinstance(site[key], str) or not site[key]:
            raise PresentationModelError(f"{path}.{key}: expected non-empty string")


def _validate_authorization_provenance(authorization: Any, path: str) -> None:
    """The optional ``authorization.authorization_provenance(...)`` payload.

    The resolved standing authorization is represented on the production
    presentation root, not only on the in-memory coordinator outcome.
    """
    _require_keys(
        authorization,
        frozenset({"kind", "role", "status", "grant_id", "detail", "admitted"}),
        frozenset(),
        path,
    )
    if authorization["kind"] != "authorization" or authorization["role"] != "authorization":
        raise PresentationModelError(f"{path}: expected kind/role 'authorization'")
    if not isinstance(authorization["status"], str) or not authorization["status"]:
        raise PresentationModelError(f"{path}.status: expected non-empty string")
    if authorization["grant_id"] is not None and not isinstance(authorization["grant_id"], str):
        raise PresentationModelError(f"{path}.grant_id: expected string or null")
    if not isinstance(authorization["detail"], dict):
        raise PresentationModelError(f"{path}.detail: expected an object")
    if not isinstance(authorization["admitted"], bool):
        raise PresentationModelError(f"{path}.admitted: expected boolean")


def _validate_resolved(resolved: Mapping[str, Any], path: str) -> None:
    if not isinstance(resolved, dict) or "disposition" not in resolved:
        raise PresentationModelError(f"{path}: missing disposition")
    disposition = resolved["disposition"]
    if disposition not in _KNOWN_DISPOSITIONS:
        raise PresentationModelError(f"{path}.disposition: unknown disposition {disposition!r}")
    if disposition in _NUMERIC_DISPOSITIONS:
        _require_keys(resolved, frozenset({"disposition", "value", "act"}), frozenset(), path)
        if not isinstance(resolved["value"], (int, float)) or isinstance(resolved["value"], bool):
            raise PresentationModelError(f"{path}.value: expected a number")
        if not isinstance(resolved["act"], dict):
            raise PresentationModelError(f"{path}.act: expected an object")
    elif disposition == "published_categorical":
        _require_keys(resolved, frozenset({"disposition", "act"}), frozenset(), path)
        if not isinstance(resolved["act"], dict):
            raise PresentationModelError(f"{path}.act: expected an object")
    elif disposition == "blocked":
        _require_keys(resolved, frozenset({"disposition", "activeCodes", "act"}), frozenset(), path)
        if resolved["act"] is not None:
            raise PresentationModelError(f"{path}.act: must be null for a blocked line")
        if not isinstance(resolved["activeCodes"], list) or not all(isinstance(c, str) for c in resolved["activeCodes"]):
            raise PresentationModelError(f"{path}.activeCodes: expected a list of strings")
    else:  # guard_inapplicable
        _require_keys(resolved, frozenset({"disposition", "act"}), frozenset(), path)
        if resolved["act"] is not None:
            raise PresentationModelError(f"{path}.act: must be null for a guard-inapplicable line")


_ATTACHMENT_DISPOSITIONS = frozenset({"published", "blocked", "guard_inapplicable"})


def _validate_attachment_resolved(resolved: Mapping[str, Any], path: str) -> None:
    """An attachment status entry (ADR-0056): always the same three keys,
    across all three dispositions - unlike a field row, an attachment has no
    single numeric/categorical value of its own to carry."""
    _require_keys(resolved, frozenset({"disposition", "activeCodes", "act"}), frozenset(), path)
    disposition = resolved.get("disposition")
    if disposition not in _ATTACHMENT_DISPOSITIONS:
        raise PresentationModelError(f"{path}.disposition: unknown attachment disposition {disposition!r}")
    if not isinstance(resolved["activeCodes"], list) or not all(isinstance(c, str) for c in resolved["activeCodes"]):
        raise PresentationModelError(f"{path}.activeCodes: expected a list of strings")
    if resolved["act"] is not None:
        raise PresentationModelError(f"{path}.act: must be null for an attachment status entry")


def validate_presentation_model(model: Mapping[str, Any]) -> None:
    """Strict structural validation: unknown keys and invalid combinations reject."""
    _require_keys(
        model,
        frozenset({
            "schema", "runId", "pinLabels", "sections", "citationGroups", "attachments",
            "unsupportedSourceFindings",
        }),
        frozenset({"authorization", "provenanceGroups"}),
        "$",
    )
    if "authorization" in model:
        _validate_authorization_provenance(model["authorization"], "$.authorization")
    if model["schema"] != PRESENTATION_MODEL_VERSION:
        raise PresentationModelError(f"$.schema: expected {PRESENTATION_MODEL_VERSION!r}")
    if not isinstance(model["runId"], str) or not model["runId"]:
        raise PresentationModelError("$.runId: expected non-empty string")
    if not isinstance(model["pinLabels"], dict) or not all(
        isinstance(k, str) and isinstance(v, str) and v for k, v in model["pinLabels"].items()
    ):
        raise PresentationModelError("$.pinLabels: expected a string-to-non-empty-string mapping")

    if not isinstance(model["sections"], list):
        raise PresentationModelError("$.sections: expected a list")
    seen_section_ids: set[str] = set()
    for index, section in enumerate(model["sections"]):
        path = f"$.sections[{index}]"
        _require_keys(section, frozenset({"id", "field", "resolved", "citationSites"}), frozenset(), path)
        if not isinstance(section["id"], str) or not section["id"]:
            raise PresentationModelError(f"{path}.id: expected non-empty string")
        if section["id"] in seen_section_ids:
            raise PresentationModelError(f"{path}.id: duplicate section id {section['id']!r}")
        seen_section_ids.add(section["id"])
        if not isinstance(section["field"], dict) or section["field"].get("schema") not in FIELD_SCHEMAS:
            raise PresentationModelError(f"{path}.field: expected a form-field citizen")
        _validate_resolved(section["resolved"], f"{path}.resolved")
        if not isinstance(section["citationSites"], list):
            raise PresentationModelError(f"{path}.citationSites: expected a list")
        for site_index, site in enumerate(section["citationSites"]):
            _validate_citation_site(site, f"{path}.citationSites[{site_index}]")

    if not isinstance(model["citationGroups"], list):
        raise PresentationModelError("$.citationGroups: expected a list")
    for index, group in enumerate(model["citationGroups"]):
        path = f"$.citationGroups[{index}]"
        _require_keys(group, frozenset({"id", "title", "parts"}), frozenset(), path)
        if not isinstance(group["id"], str) or not group["id"]:
            raise PresentationModelError(f"{path}.id: expected non-empty string")
        if not isinstance(group["title"], str) or not group["title"]:
            raise PresentationModelError(f"{path}.title: expected non-empty string")
        if not isinstance(group["parts"], list) or not group["parts"]:
            raise PresentationModelError(f"{path}.parts: expected a non-empty list")
        for part_index, part in enumerate(group["parts"]):
            part_path = f"{path}.parts[{part_index}]"
            _require_keys(
                part,
                frozenset({"heading", "citationSites", "tieOutText"}),
                frozenset({"adjustmentKind"}),
                part_path,
            )
            if not isinstance(part["heading"], str) or not part["heading"]:
                raise PresentationModelError(f"{part_path}.heading: expected non-empty string")
            if not isinstance(part["tieOutText"], str) or not part["tieOutText"]:
                raise PresentationModelError(f"{part_path}.tieOutText: expected non-empty string")
            if not isinstance(part["citationSites"], list):
                raise PresentationModelError(f"{part_path}.citationSites: expected a list")
            for site_index, site in enumerate(part["citationSites"]):
                _validate_citation_site(site, f"{part_path}.citationSites[{site_index}]")

    if not isinstance(model["attachments"], list):
        raise PresentationModelError("$.attachments: expected a list")
    seen_attachment_ids: set[str] = set()
    for index, attachment in enumerate(model["attachments"]):
        path = f"$.attachments[{index}]"
        _require_keys(attachment, frozenset({"id", "title", "resolved"}), frozenset(), path)
        if not isinstance(attachment["id"], str) or not attachment["id"]:
            raise PresentationModelError(f"{path}.id: expected non-empty string")
        if attachment["id"] in seen_attachment_ids:
            raise PresentationModelError(f"{path}.id: duplicate attachment id {attachment['id']!r}")
        seen_attachment_ids.add(attachment["id"])
        if not isinstance(attachment["title"], str) or not attachment["title"]:
            raise PresentationModelError(f"{path}.title: expected non-empty string")
        _validate_attachment_resolved(attachment["resolved"], f"{path}.resolved")

    if "provenanceGroups" in model:
        groups = model["provenanceGroups"]
        if not isinstance(groups, list):
            raise PresentationModelError("$.provenanceGroups: expected a list")
        published_group_ids = {
            group["id"]
            for group in model.get("citationGroups") or []
            if isinstance(group, Mapping) and isinstance(group.get("id"), str)
        }
        parts_by_attachment: dict[str, list[dict[str, Any]]] = {}
        for citation_group in model.get("citationGroups") or []:
            if not isinstance(citation_group, Mapping):
                continue
            gid = citation_group.get("id")
            if isinstance(gid, str):
                parts_by_attachment[gid] = [
                    part for part in (citation_group.get("parts") or []) if isinstance(part, dict)
                ]
        required = frozenset({
            "id", "attachmentId", "adjustmentKind", "adjustmentLabel",
            "label", "citationSites", "tieOutText",
        })
        seen_ids: set[str] = set()
        kinds_by_part: dict[tuple[str, str], str] = {}
        expected_ids_by_part: dict[tuple[str, str], set[str]] = {}
        groups_by_part: dict[tuple[str, str], set[str]] = {}
        for index, group in enumerate(groups):
            path = f"$.provenanceGroups[{index}]"
            _require_keys(group, required, frozenset(), path)
            for key in (
                "id", "attachmentId", "adjustmentKind", "adjustmentLabel", "label", "tieOutText",
            ):
                if not isinstance(group[key], str) or not group[key]:
                    raise PresentationModelError(f"{path}.{key}: expected non-empty string")
            if group["id"] in seen_ids:
                raise PresentationModelError(f"{path}.id: duplicate provenance group id {group['id']!r}")
            seen_ids.add(group["id"])
            attachment_id = group["attachmentId"]
            if attachment_id not in published_group_ids:
                raise PresentationModelError(
                    f"{path}.attachmentId: {attachment_id!r} is not a published citation group"
                )
            part_key = (attachment_id, group["adjustmentLabel"])
            prior_kind = kinds_by_part.get(part_key)
            if prior_kind is not None and prior_kind != group["adjustmentKind"]:
                raise PresentationModelError(
                    f"{path}: adjustmentKind {group['adjustmentKind']!r} conflicts with the other groups for adjustmentLabel {group['adjustmentLabel']!r}"
                )
            kinds_by_part[part_key] = group["adjustmentKind"]
            matching_parts = [
                part for part in parts_by_attachment.get(attachment_id, [])
                if part.get("heading") == group["adjustmentLabel"]
            ]
            if len(matching_parts) != 1:
                raise PresentationModelError(
                    f"{path}.adjustmentLabel: {group['adjustmentLabel']!r} does not uniquely identify an adjustment part on {attachment_id!r}"
                )
            displayed_kind = matching_parts[0].get("adjustmentKind")
            if not isinstance(displayed_kind, str) or not displayed_kind:
                raise PresentationModelError(
                    f"{path}.adjustmentKind: displayed adjustment does not declare its producer kind"
                )
            if group["adjustmentKind"] != displayed_kind:
                raise PresentationModelError(
                    f"{path}.adjustmentKind: does not match the displayed adjustment kind"
                )
            sites = group["citationSites"]
            if not isinstance(sites, list) or not sites:
                raise PresentationModelError(f"{path}.citationSites: expected a non-empty list")
            site_ids: set[str] = set()
            for site_index, site in enumerate(sites):
                _validate_citation_site(site, f"{path}.citationSites[{site_index}]")
                site_id = site["siteId"]
                if site_id in site_ids:
                    raise PresentationModelError(f"{path}.citationSites: duplicate site id {site_id!r}")
                site_ids.add(site_id)
            if group["id"] in {site["pinId"] for site in sites}:
                raise PresentationModelError(f"{path}: grouping id must not be presented as a citation pin")
            groups_by_part.setdefault(part_key, set()).add(group["id"])

        # Each derived adjustment row is one and only one provenance group.
        # The row's citation sites are the structural join available in this
        # presentation-only model; this keeps cardinality checking generic
        # and avoids teaching the validator tax-specific fact identities.
        for attachment_id, parts in parts_by_attachment.items():
            for part in parts:
                label = part.get("heading")
                if not isinstance(label, str):
                    continue
                part_key = (attachment_id, label)
                expected = {
                    site["pinId"]
                    for site in part.get("citationSites", [])
                    if isinstance(site, Mapping)
                    and isinstance(site.get("pinId"), str)
                    and site["pinId"].startswith("finding:derived:")
                }
                if expected:
                    expected_ids_by_part[part_key] = expected
                    actual = groups_by_part.get(part_key, set())
                    if actual != expected:
                        raise PresentationModelError(
                            f"$.provenanceGroups: expected exactly one group for each contributing finding on {attachment_id!r}/{label!r}"
                        )
        for part_key in groups_by_part:
            if part_key not in expected_ids_by_part:
                raise PresentationModelError(
                    f"$.provenanceGroups: group has no contributing finding on {part_key[0]!r}/{part_key[1]!r}"
                )

    if not isinstance(model["unsupportedSourceFindings"], list):
        raise PresentationModelError("$.unsupportedSourceFindings: expected a list")
    for index, entry in enumerate(model["unsupportedSourceFindings"]):
        path = f"$.unsupportedSourceFindings[{index}]"
        _require_keys(
            entry,
            frozenset({"factTypeId", "factTypeTitle", "findingId", "factId", "value"}),
            frozenset(),
            path,
        )
        for key in ("factTypeId", "factTypeTitle", "findingId", "factId"):
            if not isinstance(entry[key], str) or not entry[key]:
                raise PresentationModelError(f"{path}.{key}: expected non-empty string")

    _check_no_unsafe_strings(model, "$")


__all__ = [
    "PRESENTATION_MODEL_VERSION",
    "PresentationModelError",
    "build_presentation_model",
    "validate_presentation_model",
]
