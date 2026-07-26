"""Internal presentation projector (Presentation L2 Integration Grounding, Track 1).

Builds the citation-walk renderer's input model from exactly the four things
already available inside a successful ``live_coordinate_run``: the resolved
exclusive graph, the projected record state, ``RunResult.publications``, and
``RunResult.dispositions``. This is an internal implementation shape with its
own version and strict validator (below) — never a published schema, citizen,
or caller-facing contract (ADR-0046 is unchanged; this module does not
instantiate it).

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
from decimal import Decimal, InvalidOperation
from typing import Any, Mapping, Sequence, cast

from packages.kernel.findings import FindingState

PRESENTATION_MODEL_VERSION = "presentation-model.v1"

# form-field.v2 and .v3 share an identical renderer-facing shape (schema,
# id, version, form, line, label, description, binds_symbol, citation,
# dispositions); v3 only reconciles the blocked-code enum
# (SOURCE_SET_UNCLOSED, the code the runner actually emits) and is not a
# distinct presentation contract. Both are recognized field citizens.
FIELD_SCHEMAS = frozenset({"form-field.v2", "form-field.v3"})
ATTACHMENT_SCHEMA = "attachment-rule.v1"

_NUMERIC_DISPOSITIONS = frozenset({"published_value", "computed_zero", "closure_backed_zero"})
_KNOWN_DISPOSITIONS = _NUMERIC_DISPOSITIONS | {"blocked", "guard_inapplicable"}
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


def _resolve_attachment(
    attachment: Mapping[str, Any],
    *,
    dispositions_by_symbol: Mapping[str, list[Mapping[str, Any]]],
    publications_by_id: Mapping[str, Mapping[str, Any]],
    state: FindingState,
    pin_labels: dict[str, str],
) -> dict[str, Any] | None:
    symbol = attachment["publishes"]
    row = _one_row(dispositions_by_symbol.get(symbol, []), symbol=symbol)
    if row["disposition"] == "inapplicable":
        if row.get("guard_result") is not False:
            raise PresentationModelError(f"unrecognized inapplicable disposition for attachment {attachment['id']!r}")
        return None
    if row["disposition"] == "blocked":
        return None
    if row["disposition"] != "published":
        raise PresentationModelError(f"unknown disposition {row['disposition']!r} for attachment {attachment['id']!r}")

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
        leaves = _raw_leaves(
            finding["pins"], publications_by_id=publications_by_id, state=state, root_id=finding["id"]
        )
        part_id = itemization["part_id"]
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

    title = attachment["title"].split(":", 1)[0].strip()
    return {"id": attachment["id"], "title": title, "parts": parts}


def build_presentation_model(
    *,
    run_id: str,
    resolved_members: Sequence[Mapping[str, Any]],
    state: FindingState,
    publications: Sequence[Any],
    dispositions: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Build the presentation-model.v1 payload from coordinator-internal state only.

    ``publications`` is ``RunResult.publications`` (a sequence of objects with
    an ``.act``/``.finding`` pair); ``dispositions`` is ``RunResult.dispositions``.
    Raises :class:`PresentationModelError` on any missing/ambiguous join,
    unknown disposition, invalid numeric publication, or untraceable citation
    lineage — never on a guess.
    """
    fields = [m for m in resolved_members if m.get("schema") in FIELD_SCHEMAS]
    attachments = [m for m in resolved_members if m.get("schema") == ATTACHMENT_SCHEMA]
    rules_by_id = _rules_by_id(resolved_members)
    publications_by_id = {pub.finding["id"]: pub.finding for pub in publications}
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
        sections.append({
            "id": section_id,
            "field": dict(field),
            "resolved": resolved,
            "citationSites": citation_sites,
        })

    citation_groups: list[dict[str, Any]] = []
    for attachment in sorted(attachments, key=lambda a: a["id"]):
        group = _resolve_attachment(
            attachment, dispositions_by_symbol=by_symbol, publications_by_id=publications_by_id,
            state=state, pin_labels=pin_labels,
        )
        if group is not None:
            citation_groups.append(group)

    model = {
        "schema": PRESENTATION_MODEL_VERSION,
        "runId": run_id,
        "pinLabels": pin_labels,
        "sections": sections,
        "citationGroups": citation_groups,
    }
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


def validate_presentation_model(model: Mapping[str, Any]) -> None:
    """Strict structural validation: unknown keys and invalid combinations reject."""
    _require_keys(model, frozenset({"schema", "runId", "pinLabels", "sections", "citationGroups"}), frozenset(), "$")
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
            _require_keys(part, frozenset({"heading", "citationSites", "tieOutText"}), frozenset(), part_path)
            if not isinstance(part["heading"], str) or not part["heading"]:
                raise PresentationModelError(f"{part_path}.heading: expected non-empty string")
            if not isinstance(part["tieOutText"], str) or not part["tieOutText"]:
                raise PresentationModelError(f"{part_path}.tieOutText: expected non-empty string")
            if not isinstance(part["citationSites"], list):
                raise PresentationModelError(f"{part_path}.citationSites: expected a list")
            for site_index, site in enumerate(part["citationSites"]):
                _validate_citation_site(site, f"{part_path}.citationSites[{site_index}]")

    _check_no_unsafe_strings(model, "$")


__all__ = [
    "PRESENTATION_MODEL_VERSION",
    "PresentationModelError",
    "build_presentation_model",
    "validate_presentation_model",
]
