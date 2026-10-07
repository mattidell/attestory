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
from packages.kernel.facts import fact_id_for
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


def _selection_declarations(rule: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    selection = rule.get("selection")
    if not isinstance(selection, Mapping):
        return []
    paths = [path for path in selection.get("paths") or [] if isinstance(path, Mapping)]
    default = selection.get("default")
    return [*paths, default] if isinstance(default, Mapping) else paths


def _activity_fact_type_ids(path: Mapping[str, Any]) -> list[str]:
    activity = path.get("activity")
    if not isinstance(activity, Mapping) or activity.get("kind") != "source_nonempty":
        raise PresentationModelError("selection path activity is not a declared source_nonempty activity")
    listed = activity.get("member_fact_types")
    pins = listed if isinstance(listed, list) else [activity.get("member_fact_type")]
    ids = [pin.get("id") for pin in pins if isinstance(pin, Mapping)]
    if not ids or not all(isinstance(item, str) for item in ids):
        raise PresentationModelError("selection path activity names no fact type")
    return [str(item) for item in ids]


def _favorable_values(declaration: Mapping[str, Any], symbol: str) -> set[str]:
    """The literal a declaration's ``collect_categorical_all_equal`` over ``symbol`` expects."""
    found: set[str] = set()

    def visit(node: Any) -> None:
        if isinstance(node, Mapping):
            if node.get("op") == "collect_categorical_all_equal" and node.get("name") == symbol:
                literal = node.get("value")
                if isinstance(literal, Mapping) and isinstance(literal.get("value"), str):
                    found.add(literal["value"])
            for child in node.values():
                visit(child)
        elif isinstance(node, list):
            for child in node:
                visit(child)

    visit(declaration.get("when"))
    visit(declaration.get("value"))
    return found


def _blocks_unconditionally(rule: Mapping[str, Any]) -> bool:
    """True when ``rule`` can only block: its value is a bare ``block``."""
    value = rule.get("value")
    return rule.get("when") is True and isinstance(value, Mapping) and value.get("op") == "block"


def _value_descriptions(resolved_members: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, str]]:
    """Fact type id -> value -> the description its value schema declares for that value."""
    fact_types: list[Mapping[str, Any]] = []
    for member in resolved_members:
        if str(member.get("schema", "")).startswith("fact-type."):
            fact_types.append(member)
        elif str(member.get("schema", "")).startswith("bundle."):
            fact_types.extend(ft for ft in member.get("fact_types") or [] if isinstance(ft, Mapping))
    out: dict[str, dict[str, str]] = {}
    for fact_type in fact_types:
        value_schema = fact_type.get("value_schema")
        entries = value_schema.get("oneOf") if isinstance(value_schema, Mapping) else None
        for entry in entries if isinstance(entries, list) else []:
            if isinstance(entry, Mapping) and isinstance(entry.get("const"), str) and isinstance(entry.get("description"), str):
                known = out.setdefault(str(fact_type.get("id")), {})
                if known.get(entry["const"], entry["description"]) != entry["description"]:
                    raise PresentationModelError(f"conflicting descriptions for {fact_type.get('id')!r} value {entry['const']!r}")
                known[entry["const"]] = entry["description"]
    return out


def _statement_label(keys: Mapping[str, str], state: FindingState) -> dict[str, str]:
    label: dict[str, str] = {}
    for key_name in ("lender", "statement"):
        entity_id = keys.get(key_name)
        lifecycle = state.fact_state.entities.get(entity_id) if entity_id else None
        if lifecycle is not None and lifecycle.status == "current":
            recorded = lifecycle.entity.get("label")
            if isinstance(recorded, str) and recorded:
                label[key_name] = recorded
    if "tax-year" in keys:
        label["taxYear"] = str(keys["tax-year"])
    return label


def _selection_blocked_reasons(
    row: Mapping[str, Any],
    rule: Mapping[str, Any],
    *,
    resolved_members: Sequence[Mapping[str, Any]],
    rules_by_id: Mapping[str, Mapping[str, Any]],
    state: FindingState,
    publications_by_id: Mapping[str, Mapping[str, Any]],
    dispositions: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Why a blocked ADR 0077 Part 4 selection line is blocked, statement by statement.

    Every sentence is declared content, never composed here: a value's
    ``description`` in its fact type's value schema (``oneOf``), or a rule's
    ``wording``. Which declaration applies is decided from the record:

    - Both paths active (the row carries the refusal's ``missing``): each
      statement holding an activity finding gets the description the read
      symbols' vocabulary declares for the refusal token.
    - The selected path, or the default: for each declared read and each
      current subject, a published value other than the one the declaration
      expects gives that value's description; a block, or no single result,
      gives the publishing rule's ``wording``.
    - A declared read whose publisher can only block (no expected value,
      a bare ``block``): each block row recorded for it gives the
      publisher's ``wording``, labelled by the one input the row pins. Its
      subjects may exist only in the run, so they are not looked up in the
      record. A published row for such a read refuses.
    - When the workspace has not adopted every fact type the selected path's
      activity names, it cannot record what that path decides on; each
      statement that has a reason gets the selection rule's ``wording``
      instead.

    The selected path is recomputed from the projected current findings the
    same way the runner decides activity; a row that disagrees fails closed.
    """
    from packages.kernel.currency import compute_currency
    from packages.kernel.facts import facts_of

    selection = rule.get("selection")
    if not isinstance(selection, Mapping):
        return []
    fact_map = facts_of(state.fact_state)
    current = compute_currency(state).current_finding_ids
    current_by_type: dict[str, list[str]] = {}
    current_findings_by_type: dict[str, list[str]] = {}
    for finding_id, finding in state.findings.items():
        fact = fact_map.get(str(finding.get("fact_id"))) if finding_id in current else None
        if fact is None:
            continue
        current_by_type.setdefault(fact.fact_type_id, []).append(str(finding["fact_id"]))
        current_findings_by_type.setdefault(fact.fact_type_id, []).append(finding_id)
    descriptions = _value_descriptions(resolved_members)
    paths = [path for path in selection.get("paths") or [] if isinstance(path, Mapping)]
    active = [path for path in paths
              if any(current_by_type.get(member) for member in _activity_fact_type_ids(path))]
    declared_refusal = selection.get("refusal")
    refusal: Mapping[str, Any] = declared_refusal if isinstance(declared_refusal, Mapping) else {}
    refused = list(row.get("missing") or []) == list(refusal.get("missing") or [None])
    if refused != (len(active) > 1):
        raise PresentationModelError(f"blocked {rule.get('id')!r} row disagrees with its recomputed selection")

    reasons: list[dict[str, Any]] = []
    seen: set[tuple[str, Any]] = set()

    def add(sentence: Any, keys: Mapping[str, str], fact_id: str | None) -> None:
        if not isinstance(sentence, str) or not sentence:
            return
        entry: dict[str, Any] = {"sentence": sentence}
        if fact_id is not None:
            entry["factId"] = fact_id
        label = _statement_label(keys, state)
        if label:
            entry["statementLabel"] = label
        # One line per statement per sentence: the same declared sentence
        # reached through two reads (a statement's standing, keyed by its
        # box 1 fact, and its replay marker, keyed by its inclusion fact)
        # says one thing to the person, so the first one stands. Identity is
        # the statement's (lender, statement, tax-year) keys, falling back to
        # the fact id; never its display label, since two distinct statements
        # may carry the same recorded label.
        key = (sentence, _sli_statement_identity(keys) or fact_id)
        if key not in seen:
            seen.add(key)
            reasons.append(entry)

    if refused:
        read_symbols = [read.get("symbol") for declaration in _selection_declarations(rule)
                        for read in declaration.get("reads_subject_results") or [] if isinstance(read, Mapping)]
        sentences = [descriptions.get(str(symbol), {}).get(str(token))
                     for token in refusal.get("missing") or [] for symbol in read_symbols]
        refusal_sentence = next((item for item in sentences if item), None)
        # Keep the statement's own fact id beside its keys: with both paths
        # active, the row's pins span every statement that made either path
        # active, and a reason with no fact id cannot be matched back to its
        # row. The identity tuple (never the display label) decides which
        # pins name the same statement; the first pin found for an identity
        # supplies the fact id, since any fact carrying that identity reads
        # back to the same statement.
        statements: dict[tuple[str, str, str], tuple[dict[str, str], str]] = {}
        for pin in row.get("pins") or []:
            pinned = state.findings.get(str(pin.get("id"))) if pin.get("role") == "input" else None
            pinned_fact = fact_map.get(str(pinned.get("fact_id"))) if pinned else None
            if pinned_fact is None:
                continue
            pinned_keys = dict(pinned_fact.keys)
            identity = _sli_statement_identity(pinned_keys)
            if identity is not None:
                statements.setdefault(identity, (pinned_keys, pinned_fact.fact_id))
        for identity, (statement_keys, fact_id) in sorted(statements.items()):
            add(refusal_sentence, statement_keys, fact_id)
        return reasons

    declaration: Mapping[str, Any] = active[0] if active else selection.get("default") or {}
    cannot_record = bool(active) and any(
        member not in state.fact_state.fact_types for member in _activity_fact_type_ids(active[0])
    )
    rows_by_symbol: dict[tuple[str, str], list[Mapping[str, Any]]] = {}
    for item in dispositions:
        if isinstance(item.get("symbol"), str) and isinstance(item.get("artifact_id"), str):
            rows_by_symbol.setdefault((item["artifact_id"], item["symbol"]), []).append(item)
    for read in declaration.get("reads_subject_results") or []:
        symbol = str(read.get("symbol"))
        subject_type = str((read.get("subject") or {}).get("id"))
        publishers = [r for r in rules_by_id.values()
                      if r.get("publishes") == symbol and (r.get("subject") or {}).get("id") == subject_type]
        if len(publishers) != 1:
            raise PresentationModelError(f"declared read {symbol!r} has no single publisher")
        publisher = publishers[0]
        favorable = _favorable_values(declaration, symbol)
        if not favorable and _blocks_unconditionally(publisher):
            # A blocked-only read: its publisher never publishes, so every
            # result is a block, and its subjects may be run material that is
            # not in the record (the Part 5 replay marker). Each block row
            # recorded for this symbol is explained by the publisher's
            # declared wording; the statement is the one its pinned input
            # names. A published row here cannot be interpreted and refuses.
            for result in [
                    item for (artifact_id, keyed), items in sorted(rows_by_symbol.items())
                    if artifact_id == publisher["id"] and (keyed == symbol or keyed.startswith(symbol + "|"))
                    for item in items]:
                if result.get("disposition") != "blocked":
                    raise PresentationModelError(f"blocked-only read {symbol!r} has a published result")
                pinned_facts = [
                    fact_map[str(finding.get("fact_id"))]
                    for pin in result.get("pins") or []
                    if isinstance(pin, Mapping) and pin.get("role") == "input"
                    for finding in [state.findings.get(str(pin.get("id")))]
                    if finding is not None and str(finding.get("fact_id")) in fact_map
                ]
                if len(pinned_facts) != 1:
                    raise PresentationModelError(f"blocked-only read {symbol!r} result names no single input")
                wording = publisher.get("wording")
                if wording and cannot_record:
                    wording = rule.get("wording")
                add(wording, dict(pinned_facts[0].keys), pinned_facts[0].fact_id)
            continue
        if len(favorable) != 1:
            raise PresentationModelError(f"declared read {symbol!r} has no single expected value")
        for subject in sorted(set(current_by_type.get(subject_type, []))):
            fact = fact_map.get(subject)
            keys = dict(fact.keys) if fact is not None else {}
            results = rows_by_symbol.get((str(publisher["id"]), f"{symbol}|{subject}"), [])
            sentence: Any = None
            if len(results) == 1 and results[0].get("disposition") == "published":
                published = publications_by_id.get(str(results[0].get("finding_id")))
                value = published.get("value") if published else None
                if value in favorable:
                    continue
                sentence = descriptions.get(symbol, {}).get(str(value))
            else:
                sentence = publisher.get("wording")
            if sentence and cannot_record:
                sentence = rule.get("wording")
            add(sentence, keys, subject)
    return reasons


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


def _calculation_view(
    *, resolved_members: Sequence[Mapping[str, Any]], state: FindingState,
    publications: Mapping[str, Mapping[str, Any]], dispositions: Sequence[Mapping[str, Any]],
) -> dict[str, Any] | None:
    """Project the bounded v12 statement reader from recorded run material."""
    from packages.kernel.facts import facts_of

    rules = _rules_by_id(resolved_members)
    rule_members = [m for m in resolved_members if "publishes" in m]
    roles: dict[str, list[Mapping[str, Any]]] = {}
    for rule in rules.values():
        role = rule.get("reader_role")
        if isinstance(role, str):
            roles.setdefault(role, []).append(rule)
    amount_rules = roles.get("statement-amount", [])
    if not amount_rules:
        return None
    if len(rules) != len(rule_members):
        raise PresentationModelError("calculation view has duplicate resolved rule ids")
    if len({str(r.get("publishes")) for r in amount_rules}) != 1:
        raise PresentationModelError("calculation view requires one shared statement amount symbol")
    rows_by_rule: dict[str, list[Mapping[str, Any]]] = {}
    for row in dispositions:
        artifact_id = row.get("artifact_id")
        if isinstance(artifact_id, str):
            rows_by_rule.setdefault(artifact_id, []).append(row)
    fact_map = facts_of(state.fact_state)
    from packages.kernel.currency import compute_currency
    current_finding_ids = compute_currency(state).current_finding_ids
    diagnostic_markers = {"link-coverage-scope-unbound", "link-coverage-keys-unavailable", "link-coverage-unjoinable"}
    parameter_ids = {str(m.get("id")) for m in resolved_members if m.get("schema") == "parameter-declaration.v1"}
    declared_symbols = {str(m.get("publishes")) for m in rule_members}
    fact_type_ids = {str(m.get("id")) for m in resolved_members if str(m.get("schema", "")).startswith("fact-type.")}
    source_set_ids = {str(m.get("id")) for m in resolved_members if str(m.get("schema", "")).startswith("source-set.")}

    def named_parameter_version(rule: Mapping[str, Any], parameter_id: str) -> str | None:
        versions: set[str] = set()

        def visit(node: Any) -> None:
            if isinstance(node, Mapping):
                parameter_ref = node.get("parameter")
                if (isinstance(parameter_ref, Mapping) and parameter_ref.get("id") == parameter_id
                    and isinstance(parameter_ref.get("version"), str)):
                    versions.add(parameter_ref["version"])
                if (node.get("role") == "parameter" and node.get("id") == parameter_id
                    and isinstance(node.get("version"), str)):
                    versions.add(node["version"])
                for child in node.values():
                    visit(child)
            elif isinstance(node, (list, tuple)):
                for child in node:
                    visit(child)

        for key in ("pins", "when", "value", "blocked"):
            visit(rule.get(key))
        if len(versions) > 1:
            raise PresentationModelError(f"blocking rule {rule.get('id')!r} names ambiguous versions of parameter {parameter_id!r}")
        return next(iter(versions)) if versions else None

    def named_rule_references(rule: Mapping[str, Any], names: set[str]) -> set[str]:
        """Collect identifiers only from the contract's declared reference slots."""
        found: set[str] = set()

        def visit(node: Any) -> None:
            if isinstance(node, Mapping):
                op = node.get("op")
                if op == "ref" and "ref" in names:
                    value = node.get("name")
                    if isinstance(value, str) and value:
                        found.add(value)
                if op in {"collect", "count"} and op in names:
                    for key in ("name", "source_set"):
                        if key == "name" or key in names:
                            value = node.get(key)
                            if isinstance(value, str) and value:
                                found.add(value)
                for key in ("parameter_id", "table_id"):
                    value = node.get(key)
                    if isinstance(value, str) and value:
                        found.add(value)
                for child in node.values():
                    visit(child)
            elif isinstance(node, (list, tuple)):
                for child in node:
                    visit(child)

        for key in ("pins", "requires", "when", "value", "blocked"):
            visit(rule.get(key))
        return found

    def classify_missing(value: Any, rule: Mapping[str, Any]) -> dict[str, Any]:
        if not isinstance(value, str):
            return {"kind": "text", "value": str(value)}
        if value in diagnostic_markers:
            return {"kind": "diagnostic", "value": value}
        rule_parameter_ids = named_rule_references(rule, {"parameter_id", "table_id"})
        # `link_coverage.empty.parameter.id` is a typed reference; do not
        # infer parameter identity from arbitrary prose or expression strings.
        def has_empty_parameter(node: Any) -> bool:
            if isinstance(node, Mapping):
                if node.get("op") == "link_coverage":
                    empty = node.get("empty")
                    if isinstance(empty, Mapping):
                        param = empty.get("parameter")
                        if isinstance(param, Mapping) and param.get("id") == value:
                            return True
                return any(has_empty_parameter(child) for child in node.values())
            if isinstance(node, (list, tuple)):
                return any(has_empty_parameter(child) for child in node)
            return False
        if value in parameter_ids or value in rule_parameter_ids or any(
            has_empty_parameter(rule.get(key)) for key in ("pins", "when", "value", "blocked")
        ):
            parameter: dict[str, Any] = {"kind": "parameter", "id": value}
            parameter_version = named_parameter_version(rule, value)
            if parameter_version is not None:
                parameter["version"] = parameter_version
            return parameter
        named_source_refs = named_rule_references(rule, {"ref", "collect", "count", "source_set"})
        if (value not in state.findings and value not in publications
            and (value in rule.get("requires", []) or value in declared_symbols or value in fact_type_ids
                 or value in source_set_ids or value in named_source_refs)):
            return {"kind": "symbol", "value": value}
        if value in state.findings:
            recorded = state.findings[value]
            fact_id = recorded.get("fact_id")
            if not isinstance(fact_id, str) or not fact_id:
                raise PresentationModelError(f"missing finding {value!r} has no recorded fact identity")
            return {"kind": "finding", "findingId": value, "factId": fact_id}
        publication = publications.get(value)
        if publication is not None:
            symbol = publication.get("symbol")
            if not isinstance(symbol, str) or not symbol:
                raise PresentationModelError(f"missing publication {value!r} has no recorded symbol")
            return {"kind": "finding", "findingId": value, "symbol": symbol}
        return {"kind": "text", "value": value}

    def copy_rule_text(template: str, group_label: Mapping[str, Any], finding_ids: Sequence[str]) -> str:
        def replace_slot(match: re.Match[str]) -> str:
            slot = match.group(1)
            if slot == "statement":
                value = group_label.get("statement")
                if not isinstance(value, str) or not value:
                    raise PresentationModelError("wording slot {statement} has no recorded statement label")
                return value
            for finding_id in finding_ids:
                finding = state.findings.get(finding_id)
                fact_id = finding.get("fact_id") if finding else None
                fact = fact_map.get(fact_id) if isinstance(fact_id, str) else None
                if fact is None:
                    continue
                key_values = dict(fact.keys)
                raw = key_values.get(slot)
                if raw is None:
                    continue
                entity = state.fact_state.entities.get(raw)
                fact_type = state.fact_state.fact_types.get(fact.fact_type_id, {})
                key_declaration: Mapping[str, Any] = next((k for k in fact_type.get("identity_keys", []) if k.get("name") == slot), {})
                if key_declaration.get("kind") == "entity":
                    resolved_label = entity.entity.get("label") if entity and entity.status == "current" else None
                else:
                    resolved_label = raw
                if isinstance(resolved_label, str) and resolved_label:
                    return resolved_label
            raise PresentationModelError(f"wording slot {{{slot}}} has no recorded pinned key")
        rendered = re.sub(r"\{(statement|institution|programme|period)\}", replace_slot, template)
        if re.search(r"\{[^{}]+\}", rendered):
            raise PresentationModelError("rule wording contains an unsupported unresolved slot")
        return rendered

    def result(rule: Mapping[str, Any] | None, fact_id: str) -> Mapping[str, Any] | None:
        if rule is None:
            return None
        keyed = f"{rule['publishes']}|{fact_id}"
        matches = [r for r in rows_by_rule.get(str(rule["id"]), []) if r.get("symbol") == keyed]
        if len(matches) > 1:
            raise PresentationModelError(f"ambiguous keyed disposition {keyed!r}")
        return matches[0] if matches else None

    def rule_info(row: Mapping[str, Any]) -> dict[str, Any]:
        rule = rules.get(str(row.get("artifact_id")))
        if rule is None:
            raise PresentationModelError(f"unknown calculation-view rule {row.get('artifact_id')!r}")
        out = {"ruleId": rule["id"], "ruleVersion": rule["version"], "readerRole": rule.get("reader_role"),
               "symbol": row.get("symbol"), "disposition": row.get("disposition"),
               "pins": [dict(p) for p in row.get("pins", [])]}
        if isinstance(row.get("code"), str):
            out["code"] = row["code"]
        return out

    def axis(rule: Mapping[str, Any] | None, fact_id: str, interpretation: str) -> dict[str, Any]:
        row = result(rule, fact_id) if rule is not None else None
        if row is None:
            if rule is None:
                return {"interpretation": "not-computed"}
            return {"interpretation": "not-computed", "ruleId": rule["id"],
                    "ruleVersion": rule["version"], "readerRole": rule.get("reader_role")}
        out = rule_info(row)
        out["interpretation"] = interpretation
        if row.get("disposition") == "published":
            fid = row.get("finding_id")
            finding = publications.get(str(fid))
            if finding is None:
                raise PresentationModelError(f"calculation view references absent publication {fid!r}")
            out["findingId"] = fid
            out["value"] = finding.get("value")
            out["pins"] = [dict(p) for p in finding.get("pins", [])]
        elif row.get("disposition") == "blocked":
            producer = rules.get(str(row.get("artifact_id")), {})
            out["missing"] = [classify_missing(v, producer) for v in row.get("missing", [])]
        return out

    def count_result(row: Mapping[str, Any], rule: Mapping[str, Any]) -> int:
        finding_id = row.get("finding_id")
        finding = publications.get(str(finding_id))
        if finding is None:
            raise PresentationModelError(f"count disposition lacks its publication {finding_id!r}")
        raw = _numeric_value(finding.get("value"), symbol=str(rule.get("publishes")))
        if raw < 0 or int(raw) != raw:
            raise PresentationModelError(f"count producer {rule.get('id')!r} published a non-count value")
        return int(raw)

    groups: list[dict[str, Any]] = []

    def one_role(role: str, subject: Mapping[str, Any], predicate: Any = None) -> Mapping[str, Any] | None:
        candidates = [r for r in roles.get(role, [])
                      if r.get("subject") == subject and (predicate is None or predicate(r))]
        if len(candidates) > 1:
            raise PresentationModelError(f"ambiguous {role!r} producer for subject {subject!r}")
        return candidates[0] if candidates else None

    for amount_rule in amount_rules:
        subject_type = amount_rule.get("subject", {}).get("id")
        if not isinstance(subject_type, str):
            raise PresentationModelError("statement-amount rule lacks a declared subject")
        for fact_id, fact in sorted(fact_map.items()):
            if fact.fact_type_id != subject_type:
                continue
            amount_row = result(amount_rule, fact_id)
            if amount_row is None or amount_row.get("disposition") not in {"published", "blocked"}:
                continue
            group: dict[str, Any] = {"symbol": amount_row.get("symbol"), "factId": fact_id,
                "ruleId": amount_rule["id"], "ruleVersion": amount_rule["version"],
                "disposition": amount_row.get("disposition"), "pins": [dict(p) for p in amount_row.get("pins", [])], "nodes": [],
                "responsibilities": []}
            key_values = dict(fact.keys)
            label: dict[str, Any] = {}
            for key_name, output_name in (("lender", "lender"), ("statement", "statement")):
                entity_id = key_values.get(key_name)
                lifecycle = state.fact_state.entities.get(entity_id) if entity_id else None
                if lifecycle is not None and lifecycle.status == "current":
                    recorded_label = lifecycle.entity.get("label")
                    if isinstance(recorded_label, str) and recorded_label:
                        label[output_name] = recorded_label
            if "tax-year" in key_values:
                label["taxYear"] = key_values["tax-year"]
            if label:
                group["statementLabel"] = label
            group["sourceFindings"] = []
            source_seen: set[str] = set()

            def record_source(finding_id: Any, origin: Any = None) -> None:
                if not isinstance(finding_id, str) or finding_id not in current_finding_ids or finding_id in source_seen:
                    return
                source = state.findings.get(finding_id)
                if source is None or not isinstance(source.get("fact_id"), str):
                    return
                source_fact = fact_map.get(source["fact_id"])
                fact_type = state.fact_state.fact_types.get(source_fact.fact_type_id) if source_fact is not None else None
                if source_fact is None or fact_type is None:
                    return
                entry: dict[str, Any] = {"findingId": finding_id, "factId": source["fact_id"], "value": source.get("value"),
                    "factTypeId": source_fact.fact_type_id, "factTypeVersion": fact_type.get("version"),
                    "factTypeTitle": fact_type.get("title")}
                evidence_label = _evidence_label(finding_id, state)
                if isinstance(evidence_label, str) and evidence_label:
                    entry["label"] = evidence_label
                if origin in {"assertion", "declared_default"}:
                    entry["origin"] = origin
                source_seen.add(finding_id)
                group["sourceFindings"].append(entry)
            if amount_row.get("disposition") == "published":
                fid = amount_row.get("finding_id")
                finding = publications.get(str(fid))
                if finding is None:
                    raise PresentationModelError(f"amount publication {fid!r} is absent")
                group.update({"findingId": fid, "value": finding.get("value"),
                              "pins": [dict(p) for p in finding.get("pins", [])]})
                for pin in group["pins"]:
                    if pin.get("role") == "input":
                        record_source(pin.get("id"), pin.get("origin"))
                chain: set[str] = set()
                pending = [p.get("id") for p in group["pins"] if p.get("role") in _DEPENDENCY_ROLES]
                while pending:
                    node_id = pending.pop()
                    if not isinstance(node_id, str) or node_id in chain:
                        continue
                    node = publications.get(node_id)
                    if node is None:
                        continue
                    chain.add(node_id)
                    producer_rows = [r for r in dispositions if r.get("finding_id") == node_id and r.get("disposition") == "published"]
                    if len(producer_rows) != 1:
                        raise PresentationModelError(f"intermediate finding {node_id!r} lacks one exact producer disposition")
                    node_rule = rules.get(str(producer_rows[0].get("artifact_id")))
                    node_symbol = node.get("symbol")
                    if (node_rule is None or not isinstance(node_symbol, str)
                        or not (node_symbol == node_rule.get("publishes") or node_symbol.startswith(f"{node_rule.get('publishes')}|"))
                        or producer_rows[0].get("symbol") != node_symbol):
                        raise PresentationModelError(f"intermediate finding {node_id!r} producer does not match its recorded symbol")
                    node_pins = [dict(p) for p in node.get("pins", [])]
                    projected_node = {"findingId": node_id, "ruleId": node_rule["id"],
                        "ruleVersion": node_rule["version"], "symbol": node.get("symbol"),
                        "value": node.get("value"), "pins": node_pins}
                    origins = {p.get("origin") for p in node_pins
                               if p.get("role") == "input" and p.get("origin") in {"assertion", "declared_default"}}
                    if len(origins) == 1:
                        projected_node["basisOrigin"] = origins.pop()
                    group["nodes"].append(projected_node)
                    pending.extend(p.get("id") for p in node_pins if p.get("role") in _DEPENDENCY_ROLES)
                chain.add(str(fid))
                group["_chainFindingIds"] = chain
            elif amount_row.get("disposition") == "blocked":
                if not isinstance(amount_row.get("code"), str) or not amount_row["code"]:
                    raise PresentationModelError("blocked amount lacks its recorded disposition code")
                group["code"] = amount_row["code"]
                group["missing"] = [classify_missing(value, amount_rule) for value in amount_row.get("missing", [])]

            subject_identity = amount_rule.get("subject", {})
            link_rule = one_role("link-count", subject_identity)
            disqualifier_rule = one_role("statement-scope-disqualifier-count", subject_identity)
            required_symbols = {str(r.get("publishes")) for r in (link_rule, disqualifier_rule) if r is not None}
            conclusion_rule = one_role("bare-statement-conclusion", subject_identity,
                                       lambda r: required_symbols.issubset(set(r.get("requires", []))))
            link_row = result(link_rule, fact_id) if link_rule else None
            scope_row = result(disqualifier_rule, fact_id) if disqualifier_rule else None
            conclusion_row = result(conclusion_rule, fact_id) if conclusion_rule else None
            route = "not-computed"
            if link_row is not None:
                if link_rule is None:
                    raise PresentationModelError("link-count disposition has no declared producer")
                route = "unresolved" if link_row.get("disposition") == "blocked" else "inapplicable" if link_row.get("disposition") == "inapplicable" else "bare" if count_result(link_row, link_rule) == 0 else "linked"
            scope = "not-computed"
            if scope_row is not None:
                if disqualifier_rule is None:
                    raise PresentationModelError("scope-count disposition has no declared producer")
                scope = "unresolved" if scope_row.get("disposition") == "blocked" else "inapplicable" if scope_row.get("disposition") == "inapplicable" else "no-whole-amount-disqualifier" if count_result(scope_row, disqualifier_rule) == 0 else "whole-amount-disqualifier"
            conclusion = "published" if conclusion_row and conclusion_row.get("disposition") == "published" else ("inapplicable" if conclusion_row and conclusion_row.get("disposition") == "inapplicable" else "unresolved" if conclusion_row and conclusion_row.get("disposition") == "blocked" else "not-computed")
            outcome: dict[str, Any] = {"route": axis(link_rule, fact_id, route), "statementScope": axis(disqualifier_rule, fact_id, scope),
                       "conclusion": axis(conclusion_rule, fact_id, conclusion), "responsibilityFailures": []}
            group["statementOutcome"] = outcome
            group["statementOutcome"]["route"]["interpretation"] = route
            group["statementOutcome"]["statementScope"]["interpretation"] = scope
            group["statementOutcome"]["conclusion"]["interpretation"] = conclusion
            claim_fact_type = None
            claim_subject: Mapping[str, Any] | None = None
            if disqualifier_rule is not None:
                joined = disqualifier_rule.get("joined")
                if isinstance(joined, Mapping):
                    claim_fact_type = joined.get("id")
                    claim_subject = joined
            if isinstance(claim_fact_type, str):
                statement_keys = dict(fact.keys)
                claim_rules = [r for r in roles.get("statement-scope-classifier", [])
                               if r.get("subject") == claim_subject]
                claims: list[dict[str, Any]] = []
                for claim_fact_id, claim_fact in fact_map.items():
                    claim_keys = dict(claim_fact.keys)
                    active_claim_type = state.fact_state.fact_types.get(claim_fact.fact_type_id, {})
                    if (claim_fact.fact_type_id != claim_fact_type
                        or active_claim_type.get("version") != (claim_subject or {}).get("version")
                        or any(claim_keys.get(k) != v for k, v in statement_keys.items())):
                        continue
                    if len(claim_rules) > 1:
                        raise PresentationModelError(f"ambiguous classifier for claim fact {claim_fact_id!r}")
                    classifier_rule = claim_rules[0] if claim_rules else None
                    claim_row = result(classifier_rule, claim_fact_id)
                    if claim_row is None:
                        continue
                    claim_outcome = axis(classifier_rule, claim_fact_id, "classified" if claim_row.get("disposition") == "published" else "unresolved")
                    claim_outcome["factId"] = claim_fact_id
                    claim_outcome["claimType"] = claim_fact_type
                    claim_outcome["claimTypeVersion"] = claim_subject.get("version") if claim_subject else None
                    claim_findings = [fid for fid, recorded in state.findings.items()
                                      if recorded.get("fact_id") == claim_fact_id and fid in current_finding_ids]
                    if len(claim_findings) == 1:
                        claim_outcome["suppliedFindingId"] = claim_findings[0]
                        claim_outcome["suppliedValue"] = state.findings[claim_findings[0]].get("value")
                        claim_source = [p for p in claim_outcome.get("pins", []) if p.get("id") == claim_findings[0]]
                        record_source(claim_findings[0], claim_source[0].get("origin") if claim_source else None)
                        recorded_label = _evidence_label(claim_findings[0], state)
                        if not (isinstance(recorded_label, str) and recorded_label):
                            claim_key_values = dict(claim_fact.keys)
                            claim_type = state.fact_state.fact_types.get(claim_fact.fact_type_id, {})
                            statement_key_names = set(statement_keys)
                            candidate_labels: list[str] = []
                            for key_declaration in claim_type.get("identity_keys", []):
                                key_name = key_declaration.get("name")
                                if key_name in statement_key_names:
                                    continue
                                raw_key = claim_key_values.get(key_name)
                                if key_declaration.get("kind") != "entity" or not isinstance(raw_key, str):
                                    continue
                                entity = state.fact_state.entities.get(raw_key)
                                candidate_label = entity.entity.get("label") if entity and entity.status == "current" else None
                                if isinstance(candidate_label, str) and candidate_label:
                                    candidate_labels.append(candidate_label)
                            if len(candidate_labels) == 1:
                                recorded_label = candidate_labels[0]
                        if isinstance(recorded_label, str) and recorded_label:
                            claim_outcome["label"] = recorded_label
                    claims.append(claim_outcome)
                group["statementOutcome"]["statementScope"]["claims"] = claims
            for pin in group.get("pins", []):
                if pin.get("role") == "input":
                    record_source(pin.get("id"), pin.get("origin"))
            for node in group.get("nodes", []):
                for pin in node.get("pins", []):
                    if pin.get("role") == "input":
                        record_source(pin.get("id"), pin.get("origin"))
            for axis_name in ("route", "statementScope", "conclusion"):
                for pin in group["statementOutcome"][axis_name].get("pins", []):
                    if pin.get("role") == "input":
                        record_source(pin.get("id"), pin.get("origin"))
            assumptions: list[dict[str, Any]] = []
            parameter_consumers: list[tuple[Mapping[str, Any], str | None, str | None]] = []
            for axis_name in ("route", "statementScope", "conclusion"):
                axis_row = group["statementOutcome"][axis_name]
                if isinstance(axis_row.get("pins"), list):
                    parameter_consumers.append((axis_row, axis_row.get("ruleId"), axis_row.get("findingId")))
            for node in group["nodes"]:
                parameter_consumers.append((node, node.get("ruleId"), node.get("findingId")))
            parameter_consumers.append((group, amount_rule.get("id"), group.get("findingId")))
            for consumer, consumer_rule_id, consumer_finding_id in parameter_consumers:
                for pin in consumer.get("pins", []):
                    if pin.get("role") != "parameter":
                        continue
                    parameter = next((m for m in resolved_members if m.get("schema") == "parameter-declaration.v1"
                                      and m.get("id") == pin.get("id") and m.get("version") == pin.get("version")), None)
                    if parameter is None:
                        raise PresentationModelError(f"parameter pin {pin.get('id')!r}@{pin.get('version')!r} has no exact resolved declaration")
                    assumption = {"id": pin["id"], "version": pin["version"], "value": parameter.get("values"),
                                  "consumerRuleId": consumer_rule_id, "consumerFindingId": consumer_finding_id}
                    if assumption not in assumptions:
                        assumptions.append(assumption)
            group["assumptions"] = assumptions
            conclusion_producer = rules.get(str(conclusion_row.get("artifact_id"))) if conclusion_row and conclusion_row.get("disposition") == "published" else None
            responsibility_candidates = [r for r in roles.get("responsibility", [])
                if conclusion_rule is not None and r.get("subject") == subject_identity
                and {str(amount_rule.get("publishes")), str(conclusion_rule.get("publishes"))}.issubset(set(r.get("requires", [])))]
            for responsibility_rule in responsibility_candidates:
                responsibility_row = result(responsibility_rule, fact_id)
                if responsibility_row is not None and responsibility_row.get("disposition") == "blocked":
                    outcome["responsibilityFailures"].append({
                        "ruleId": responsibility_rule["id"], "symbol": responsibility_row.get("symbol"),
                        "code": responsibility_row.get("code"),
                        "missing": [classify_missing(v, responsibility_rule) for v in responsibility_row.get("missing", [])],
                        "explainedBy": [
                            {"symbol": axis_outcome.get("symbol"), "interpretation": axis_outcome.get("interpretation")}
                            for missing_entry in [classify_missing(v, responsibility_rule) for v in responsibility_row.get("missing", [])]
                            if missing_entry.get("kind") == "symbol"
                            for axis_outcome in (outcome["route"], outcome["statementScope"], outcome["conclusion"])
                            if axis_outcome.get("symbol") == missing_entry.get("value")
                            or (isinstance(axis_outcome.get("symbol"), str) and axis_outcome["symbol"].startswith(f"{missing_entry.get('value')}|"))
                        ],
                    })
                    continue
                if not responsibility_row or responsibility_row.get("disposition") != "published":
                    continue
                fid = responsibility_row.get("finding_id")
                finding = publications.get(str(fid))
                if finding is None:
                    raise PresentationModelError(f"responsibility publication {fid!r} is absent")
                pins = [dict(p) for p in finding.get("pins", [])]
                chain_ids = group.get("_chainFindingIds", set())
                if not any(p.get("id") in chain_ids for p in pins) or not any(p.get("id") == outcome["conclusion"].get("findingId") for p in pins):
                    continue
                responsibility = {"ruleId": responsibility_rule["id"], "ruleVersion": responsibility_rule["version"],
                                  "symbol": responsibility_row.get("symbol"), "findingId": fid,
                                  "value": finding.get("value"), "pins": pins}
                if isinstance(responsibility_rule.get("wording"), str):
                    responsibility["wording"] = copy_rule_text(responsibility_rule["wording"], label, [str(fid)])
                group["responsibilities"].append(responsibility)
            if group["responsibilities"] and conclusion_producer is not None and isinstance(conclusion_producer.get("lineNote"), str):
                conclusion_fid = str(conclusion_row.get("finding_id")) if conclusion_row else ""
                if any(any(p.get("id") == conclusion_fid for p in r.get("pins", [])) for r in group["responsibilities"]):
                    group["lineNote"] = copy_rule_text(conclusion_producer["lineNote"], label, [conclusion_fid])
            group.pop("_chainFindingIds", None)
            groups.append(group)
    if not groups:
        return None
    return {"integrated": False, "amountSymbol": amount_rules[0].get("publishes"), "groups": groups}


# ---------------------------------------------------------------------------
# Schedule 1 line 21 (student loan interest) explanation data (Track 1a).
#
# One optional top-level block, additive to the presentation model, carrying
# exactly the data named by the milestone plan's provisional design (P1-P4):
# per-statement rows, the plain-case-supported basis on an unblocked row, and
# the published/zero line's own worked figures. Emitted only when the
# adopted package carries the statement-loan-support rule, so every model
# built from a package without it (including the v33 goldens) is unchanged.
# Every value here is read from what ``build_presentation_model`` already
# receives (``resolved_members``, ``state``, ``publications``, the already
# -built ``sections``) plus ``workspace_revision`` passed in by the caller;
# nothing is read from the workspace log after the run.
# ---------------------------------------------------------------------------

_SLI_SUPPORT_RULE_ID = "tax.us.2025.rule.sli-statement-loan-support"
_SLI_BOX1_FACT_TYPE = "tax.us.2025.f1098e.box1-student-loan-interest"
_SLI_INCLUSION_FACT_TYPE = "tax.us.2025.sli.statement-inclusion-relationship"
_SLI_FINANCING_FACT_TYPE = "tax.us.2025.sli.financing-relationship"
_SLI_LOAN_FACT_TYPE = "tax.us.2025.sli.loan-paid-only-school-costs"
_SLI_ENROLL_FACT_TYPE = "tax.us.2025.sli.enrolled-at-least-half-time"
_SLI_ANSWER_FACT_TYPES = frozenset({
    _SLI_FINANCING_FACT_TYPE, _SLI_INCLUSION_FACT_TYPE, _SLI_LOAN_FACT_TYPE, _SLI_ENROLL_FACT_TYPE,
})
_SLI_CONCLUSION_SYMBOL = "tax.us.2025.sli.statement-loan-support"
_SLI_STANDING_SYMBOL = "tax.us.2025.sli.statement-line21-standing"
_SLI_LINE21_SYMBOL = "tax.us.2025.schedule1.line21-sli-deduction"
_SLI_LINE1_SUBTOTAL_SYMBOL = "tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal"
_SLI_TOTAL_INCOME_SYMBOL = "tax.us.2025.income.total-income"
_SLI_FILING_STATUS_FACT_TYPE = "tax.us.2025.filing-status"
_SLI_SUPPORTED_VALUE = "plain-case-supported"
LINE21_EXPLANATION_VERSION = "line21-explanation.v1"


def _sli_statement_identity(raw_keys: Any) -> tuple[str, str, str] | None:
    keys = dict(raw_keys)
    lender, statement, tax_year = keys.get("lender"), keys.get("statement"), keys.get("tax-year")
    if not isinstance(lender, str) or not isinstance(statement, str) or not isinstance(tax_year, str):
        return None
    if not lender or not statement or not tax_year:
        return None
    return (lender, statement, tax_year)


def _sli_filing_status_value(state: FindingState) -> str:
    from packages.kernel.currency import compute_currency
    from packages.kernel.facts import facts_of

    fact_map = facts_of(state.fact_state)
    current = compute_currency(state).current_finding_ids
    candidates = []
    for finding_id in current:
        finding = state.findings.get(finding_id)
        if finding is None:
            continue
        fact = fact_map.get(str(finding.get("fact_id")))
        if fact is not None and fact.fact_type_id == _SLI_FILING_STATUS_FACT_TYPE:
            candidates.append(finding["value"])
    if len(candidates) != 1:
        raise PresentationModelError("line 21 explanation requires exactly one current filing status finding")
    return str(candidates[0])


def _sli_answer_proposition(finding: Mapping[str, Any], fact_type_id: str, state: FindingState) -> str | None:
    for evidence_id in finding.get("evidence_ids") or ():
        lifecycle = state.evidence.get(evidence_id)
        if lifecycle is None:
            continue
        body = lifecycle.evidence if isinstance(lifecycle.evidence, Mapping) else None
        content = body.get("content") if body is not None else None
        context = content.get("recognition_context") if isinstance(content, Mapping) else None
        if not isinstance(context, Mapping):
            continue
        if fact_type_id in (_SLI_FINANCING_FACT_TYPE, _SLI_INCLUSION_FACT_TYPE):
            propositions = context.get("propositions")
            key = "financing" if fact_type_id == _SLI_FINANCING_FACT_TYPE else "statement_inclusion"
            value = propositions.get(key) if isinstance(propositions, Mapping) else None
        else:
            value = context.get("proposition")
        if isinstance(value, str) and value:
            return value
    return None


def _sli_statement_loans(
    identity: tuple[str, str, str], *, state: FindingState, fact_map: Mapping[str, Any], current: frozenset[str],
) -> list[str]:
    lender, statement, tax_year = identity
    labels: set[str] = set()
    for finding_id in current:
        finding = state.findings.get(finding_id)
        if finding is None:
            continue
        fact = fact_map.get(str(finding.get("fact_id")))
        if fact is None or fact.fact_type_id != _SLI_INCLUSION_FACT_TYPE:
            continue
        keys = dict(fact.keys)
        if (keys.get("lender"), keys.get("statement"), keys.get("tax-year")) != (lender, statement, tax_year):
            continue
        borrowing_id = keys.get("borrowing")
        entity = state.fact_state.entities.get(borrowing_id) if isinstance(borrowing_id, str) else None
        if entity is not None and entity.status == "current":
            label = entity.entity.get("label")
            if isinstance(label, str) and label:
                labels.add(label)
    return sorted(labels)


def _sli_line1_amount_for(
    identity: tuple[str, str, str], *, line1_publication: Mapping[str, Any] | None,
    state: FindingState, fact_map: Mapping[str, Any],
) -> Any:
    if line1_publication is None:
        return None
    lender, statement, tax_year = identity
    for pin in line1_publication.get("pins", []) or []:
        if not isinstance(pin, Mapping) or pin.get("role") != "input":
            continue
        finding = state.findings.get(str(pin.get("id")))
        if finding is None:
            continue
        fact = fact_map.get(str(finding.get("fact_id")))
        if fact is None or fact.fact_type_id != _SLI_BOX1_FACT_TYPE:
            continue
        keys = dict(fact.keys)
        if (keys.get("lender"), keys.get("statement"), keys.get("tax-year")) == (lender, statement, tax_year):
            return finding.get("value")
    return None


def _sli_basis_answers(
    conclusion_finding: Mapping[str, Any], *, publications_by_id: Mapping[str, Mapping[str, Any]],
    state: FindingState, fact_map: Mapping[str, Any],
) -> list[dict[str, Any]]:
    leaves = _leaf_pins(
        conclusion_finding["pins"], publications_by_id=publications_by_id,
        seen=frozenset({conclusion_finding["id"]}),
    )
    answers: list[dict[str, Any]] = []
    for finding_id, _version in leaves:
        finding = state.findings.get(finding_id)
        if finding is None:
            raise PresentationModelError(f"basis walk references unrecorded finding {finding_id!r}")
        fact = fact_map.get(str(finding.get("fact_id")))
        if fact is None or fact.fact_type_id not in _SLI_ANSWER_FACT_TYPES:
            continue
        answer = {
            "findingId": finding_id,
            "factType": fact.fact_type_id,
            "response": str(finding.get("value")),
        }
        proposition = _sli_answer_proposition(finding, fact.fact_type_id, state)
        if proposition is not None:
            answer["proposition"] = proposition
        answers.append(answer)
    answers.sort(key=lambda entry: entry["findingId"])
    return answers


def _sli_line21_explanation(
    *,
    run_id: str,
    workspace_revision: int | None,
    resolved_members: Sequence[Mapping[str, Any]],
    state: FindingState,
    publications: Sequence[Any],
    publications_by_id: Mapping[str, Mapping[str, Any]],
    sections: Sequence[Mapping[str, Any]],
) -> dict[str, Any] | None:
    if workspace_revision is None:
        return None
    if not any(member.get("id") == _SLI_SUPPORT_RULE_ID for member in resolved_members):
        return None

    from packages.kernel.currency import compute_currency
    from packages.kernel.facts import facts_of

    line21_section = next(
        (s for s in sections if s["field"].get("binds_symbol") == _SLI_LINE21_SYMBOL), None,
    )
    if line21_section is None:
        return None
    resolved = line21_section["resolved"]
    reasons = resolved.get("reasons") or []

    fact_map = facts_of(state.fact_state)
    current = compute_currency(state).current_finding_ids

    publications_by_symbol: dict[str, Mapping[str, Any]] = {}
    for publication in publications:
        finding = publication.finding
        symbol = finding.get("symbol") if isinstance(finding, Mapping) else None
        if isinstance(symbol, str):
            publications_by_symbol[symbol] = finding

    identities: dict[tuple[str, str, str], dict[str, str]] = {}
    for finding_id in current:
        finding = state.findings.get(finding_id)
        if finding is None:
            continue
        fact = fact_map.get(str(finding.get("fact_id")))
        if fact is None or fact.fact_type_id != _SLI_BOX1_FACT_TYPE:
            continue
        identity = _sli_statement_identity(fact.keys)
        if identity is not None:
            identities.setdefault(identity, dict(fact.keys))

    reason_identities: dict[int, tuple[str, str, str] | None] = {}
    for index, reason in enumerate(reasons):
        fact_id = reason.get("factId") if isinstance(reason, Mapping) else None
        identity = None
        if isinstance(fact_id, str):
            fact = fact_map.get(fact_id)
            if fact is not None:
                identity = _sli_statement_identity(fact.keys)
                if identity is not None:
                    identities.setdefault(identity, dict(fact.keys))
        reason_identities[index] = identity

    if not identities:
        return None

    rows: list[dict[str, Any]] = []
    for identity in sorted(identities):
        keys = identities[identity]
        matching = sorted(index for index, found in reason_identities.items() if found == identity)
        if not matching and len(identities) == 1:
            matching = sorted(index for index, found in reason_identities.items() if found is None)
        status: dict[str, Any] = (
            {"kind": "named-by-reason", "reasonIndices": matching} if matching else {"kind": "no-reason"}
        )
        box1_fact_id = fact_id_for(_SLI_BOX1_FACT_TYPE, (
            ("lender", identity[0]), ("statement", identity[1]), ("tax-year", identity[2]),
        ))
        support_finding = publications_by_symbol.get(f"{_SLI_CONCLUSION_SYMBOL}|{box1_fact_id}")
        standing_finding = publications_by_symbol.get(f"{_SLI_STANDING_SYMBOL}|{box1_fact_id}")
        support_value = support_finding.get("value") if support_finding is not None else None
        standing_value = standing_finding.get("value") if standing_finding is not None else None
        line1_publication = publications_by_symbol.get(_SLI_LINE1_SUBTOTAL_SYMBOL)
        amount = _sli_line1_amount_for(
            identity, line1_publication=line1_publication, state=state, fact_map=fact_map,
        )
        row: dict[str, Any] = {
            "statementLabel": _statement_label(keys, state),
            "loans": _sli_statement_loans(identity, state=state, fact_map=fact_map, current=current),
            "status": status,
        }
        if amount is not None:
            row["amount"] = _numeric_value(amount, symbol=f"{_SLI_BOX1_FACT_TYPE}|{box1_fact_id}")
        if support_value is not None:
            row["support"] = str(support_value)
        if standing_value is not None:
            row["standing"] = str(standing_value)
        if support_value == _SLI_SUPPORTED_VALUE and status["kind"] == "no-reason":
            if support_finding is None:
                raise PresentationModelError("plain-case-supported row has no support publication to walk")
            rule_pin = next(
                (p for p in support_finding.get("pins", []) or []
                 if isinstance(p, Mapping) and p.get("role") == "computation" and p.get("id") == _SLI_SUPPORT_RULE_ID),
                None,
            )
            if rule_pin is None:
                raise PresentationModelError("support publication does not pin its own producing rule")
            rule = next(
                (m for m in resolved_members
                 if m.get("id") == _SLI_SUPPORT_RULE_ID and m.get("version") == rule_pin.get("version")),
                None,
            )
            basis = rule.get("basis") if rule is not None else None
            if not isinstance(basis, Mapping) or "assumed" not in basis or "left_with_person" not in basis:
                raise PresentationModelError(
                    f"{_SLI_SUPPORT_RULE_ID}@{rule_pin.get('version')} has no declared basis to show",
                )
            row["basis"] = {
                "ruleId": _SLI_SUPPORT_RULE_ID,
                "ruleVersion": str(rule_pin.get("version")),
                "assumed": list(basis["assumed"]),
                "leftWithPerson": list(basis["left_with_person"]),
                "answers": _sli_basis_answers(
                    support_finding, publications_by_id=publications_by_id, state=state, fact_map=fact_map,
                ),
            }
        rows.append(row)

    block: dict[str, Any] = {
        "schema": LINE21_EXPLANATION_VERSION,
        "runId": run_id,
        "workspaceRevision": workspace_revision,
        "rows": rows,
    }

    if resolved.get("disposition") in ("published_value", "computed_zero"):
        line1_publication = publications_by_symbol.get(_SLI_LINE1_SUBTOTAL_SYMBOL)
        if line1_publication is None:
            raise PresentationModelError("a published or zero line 21 requires the worksheet line 1 publication")
        line21_finding = (resolved.get("act") or {}).get("finding") or {}
        parameters: list[dict[str, Any]] = []
        total_income: Any = None
        for pin in line21_finding.get("pins", []) or []:
            if not isinstance(pin, Mapping):
                continue
            if pin.get("role") == "parameter":
                parameter = next(
                    (m for m in resolved_members if m.get("schema") == "parameter-declaration.v1"
                     and m.get("id") == pin.get("id") and m.get("version") == pin.get("version")),
                    None,
                )
                if parameter is None:
                    raise PresentationModelError(
                        f"parameter pin {pin.get('id')!r}@{pin.get('version')!r} has no exact resolved declaration",
                    )
                values = parameter.get("values")
                if isinstance(values, Mapping):
                    filing_status = _sli_filing_status_value(state)
                    if filing_status not in values:
                        raise PresentationModelError(
                            f"parameter {pin.get('id')!r} has no entry for filing status {filing_status!r}",
                        )
                    value = values[filing_status]
                else:
                    value = values
                parameter_entry: dict[str, Any] = {"id": pin["id"], "version": pin["version"], "value": value}
                for key in ("label", "title"):
                    if isinstance(parameter.get(key), str) and parameter[key]:
                        parameter_entry[key] = parameter[key]
                        break
                parameters.append(parameter_entry)
            elif isinstance(pin.get("id"), str) and pin["id"].startswith("finding:derived:"):
                publication = publications_by_id.get(pin["id"])
                if publication is not None and publication.get("symbol") == _SLI_TOTAL_INCOME_SYMBOL:
                    total_income = publication.get("value")
        working: dict[str, Any] = {
            "lineOneSubtotal": _numeric_value(line1_publication["value"], symbol=_SLI_LINE1_SUBTOTAL_SYMBOL),
            "parameters": parameters,
            "value": resolved["value"],
        }
        if total_income is not None:
            working["totalIncome"] = _numeric_value(total_income, symbol=_SLI_TOTAL_INCOME_SYMBOL)
        block["working"] = working

    return block


def _validate_line21_explanation(value: Any) -> None:
    path = "$.line21Explanation"
    _require_keys(
        value, frozenset({"schema", "runId", "workspaceRevision", "rows"}), frozenset({"working"}), path,
    )
    if value["schema"] != LINE21_EXPLANATION_VERSION:
        raise PresentationModelError(f"{path}.schema: expected {LINE21_EXPLANATION_VERSION!r}")
    if not isinstance(value["runId"], str) or not value["runId"]:
        raise PresentationModelError(f"{path}.runId: expected non-empty string")
    if isinstance(value["workspaceRevision"], bool) or not isinstance(value["workspaceRevision"], int):
        raise PresentationModelError(f"{path}.workspaceRevision: expected an integer")
    rows = value["rows"]
    if not isinstance(rows, list) or not rows:
        raise PresentationModelError(f"{path}.rows: expected a non-empty list")
    for index, row in enumerate(rows):
        rp = f"{path}.rows[{index}]"
        _require_keys(
            row, frozenset({"statementLabel", "loans", "status"}),
            frozenset({"amount", "support", "standing", "basis"}), rp,
        )
        label = row["statementLabel"]
        if not isinstance(label, dict) or not all(isinstance(v, str) and v for v in label.values()) \
                or set(label) - {"lender", "statement", "taxYear"}:
            raise PresentationModelError(f"{rp}.statementLabel: expected lender/statement/taxYear strings")
        if not isinstance(row["loans"], list) or not all(isinstance(v, str) and v for v in row["loans"]):
            raise PresentationModelError(f"{rp}.loans: expected a list of non-empty strings")
        status = row["status"]
        if not isinstance(status, dict) or status.get("kind") not in ("no-reason", "named-by-reason"):
            raise PresentationModelError(f"{rp}.status: expected a recognized status")
        if status["kind"] == "no-reason":
            _require_keys(status, frozenset({"kind"}), frozenset(), f"{rp}.status")
        else:
            _require_keys(status, frozenset({"kind", "reasonIndices"}), frozenset(), f"{rp}.status")
            indices = status["reasonIndices"]
            if not isinstance(indices, list) or not indices or not all(
                isinstance(i, int) and not isinstance(i, bool) and i >= 0 for i in indices
            ):
                raise PresentationModelError(f"{rp}.status.reasonIndices: expected a non-empty list of indices")
        if "amount" in row and (not isinstance(row["amount"], (int, float)) or isinstance(row["amount"], bool)):
            raise PresentationModelError(f"{rp}.amount: expected a number")
        for key in ("support", "standing"):
            if key in row and (not isinstance(row[key], str) or not row[key]):
                raise PresentationModelError(f"{rp}.{key}: expected non-empty string")
        if "basis" in row:
            basis = row["basis"]
            bp = f"{rp}.basis"
            _require_keys(basis, frozenset({"ruleId", "ruleVersion", "assumed", "leftWithPerson", "answers"}), frozenset(), bp)
            for key in ("ruleId", "ruleVersion"):
                if not isinstance(basis[key], str) or not basis[key]:
                    raise PresentationModelError(f"{bp}.{key}: expected non-empty string")
            for key in ("assumed", "leftWithPerson"):
                if not isinstance(basis[key], list) or not all(isinstance(v, str) and v for v in basis[key]):
                    raise PresentationModelError(f"{bp}.{key}: expected a list of non-empty strings")
            answers = basis["answers"]
            if not isinstance(answers, list):
                raise PresentationModelError(f"{bp}.answers: expected a list")
            for ai, answer in enumerate(answers):
                ap = f"{bp}.answers[{ai}]"
                _require_keys(answer, frozenset({"findingId", "factType", "response"}), frozenset({"proposition"}), ap)
                for key in ("findingId", "factType", "response"):
                    if not isinstance(answer[key], str) or not answer[key]:
                        raise PresentationModelError(f"{ap}.{key}: expected non-empty string")
                if "proposition" in answer and (not isinstance(answer["proposition"], str) or not answer["proposition"]):
                    raise PresentationModelError(f"{ap}.proposition: expected non-empty string")
    if "working" in value:
        working = value["working"]
        wp = f"{path}.working"
        _require_keys(working, frozenset({"lineOneSubtotal", "parameters", "value"}), frozenset({"totalIncome"}), wp)
        if not isinstance(working["lineOneSubtotal"], (int, float)) or isinstance(working["lineOneSubtotal"], bool):
            raise PresentationModelError(f"{wp}.lineOneSubtotal: expected a number")
        if "totalIncome" in working and (
            not isinstance(working["totalIncome"], (int, float)) or isinstance(working["totalIncome"], bool)
        ):
            raise PresentationModelError(f"{wp}.totalIncome: expected a number")
        if not isinstance(working["value"], (int, float)) or isinstance(working["value"], bool):
            raise PresentationModelError(f"{wp}.value: expected a number")
        parameters = working["parameters"]
        if not isinstance(parameters, list):
            raise PresentationModelError(f"{wp}.parameters: expected a list")
        for pi, parameter in enumerate(parameters):
            pp = f"{wp}.parameters[{pi}]"
            _require_keys(parameter, frozenset({"id", "version", "value"}), frozenset({"label", "title"}), pp)
            for key in ("id", "version"):
                if not isinstance(parameter[key], str) or not parameter[key]:
                    raise PresentationModelError(f"{pp}.{key}: expected non-empty string")
            if not isinstance(parameter["value"], (str, int, float)) or isinstance(parameter["value"], bool):
                raise PresentationModelError(f"{pp}.value: expected a string or number")
            for key in ("label", "title"):
                if key in parameter and (not isinstance(parameter[key], str) or not parameter[key]):
                    raise PresentationModelError(f"{pp}.{key}: expected non-empty string")


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
    workspace_revision: int | None = None,
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

    ``workspace_revision``, when supplied, is the workspace revision
    ``live_coordinate_run`` read for this run. It is the only addition this
    function reads from outside its own four coordinator-internal inputs,
    and only feeds the optional ``line21Explanation`` block (Track 1a); it is
    never read from the workspace log after the run.
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
        producer = rules_by_id.get(str(row.get("artifact_id")))
        if (resolved["disposition"] == "blocked" and producer is not None
                and producer.get("schema") == "rule-artifact.v13" and "selection" in producer):
            reasons = _selection_blocked_reasons(
                row, producer, resolved_members=resolved_members, rules_by_id=rules_by_id, state=state,
                publications_by_id=publications_by_id, dispositions=dispositions,
            )
            if reasons:
                resolved["reasons"] = reasons
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
    calculation_view = _calculation_view(
        resolved_members=resolved_members, state=state,
        publications=publications_by_id, dispositions=dispositions,
    )
    if calculation_view is not None:
        model["calculationView"] = calculation_view
    line21_explanation = _sli_line21_explanation(
        run_id=run_id, workspace_revision=workspace_revision, resolved_members=resolved_members,
        state=state, publications=publications, publications_by_id=publications_by_id, sections=sections,
    )
    if line21_explanation is not None:
        model["line21Explanation"] = line21_explanation
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
        _require_keys(resolved, frozenset({"disposition", "activeCodes", "act"}), frozenset({"reasons"}), path)
        if resolved["act"] is not None:
            raise PresentationModelError(f"{path}.act: must be null for a blocked line")
        if not isinstance(resolved["activeCodes"], list) or not all(isinstance(c, str) for c in resolved["activeCodes"]):
            raise PresentationModelError(f"{path}.activeCodes: expected a list of strings")
        if "reasons" in resolved:
            reasons = resolved["reasons"]
            if not isinstance(reasons, list) or not reasons:
                raise PresentationModelError(f"{path}.reasons: expected a non-empty list")
            for index, reason in enumerate(reasons):
                rp = f"{path}.reasons[{index}]"
                _require_keys(reason, frozenset({"sentence"}), frozenset({"factId", "statementLabel"}), rp)
                if not isinstance(reason["sentence"], str) or not reason["sentence"]:
                    raise PresentationModelError(f"{rp}.sentence: expected non-empty string")
                if "factId" in reason and (not isinstance(reason["factId"], str) or not reason["factId"]):
                    raise PresentationModelError(f"{rp}.factId: expected non-empty string")
                label = reason.get("statementLabel", {})
                if not isinstance(label, dict) or not all(isinstance(v, str) and v for v in label.values()) \
                        or set(label) - {"lender", "statement", "taxYear"}:
                    raise PresentationModelError(f"{rp}.statementLabel: expected lender/statement/taxYear strings")
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


def _validate_calculation_view(view: Any) -> None:
    path = "$.calculationView"
    _require_keys(view, frozenset({"integrated", "amountSymbol", "groups"}), frozenset(), path)
    if view["integrated"] is not False:
        raise PresentationModelError(f"{path}.integrated: must be false")
    if not isinstance(view["amountSymbol"], str) or not view["amountSymbol"]:
        raise PresentationModelError(f"{path}.amountSymbol: expected non-empty string")
    groups = view["groups"]
    if not isinstance(groups, list) or not groups:
        raise PresentationModelError(f"{path}.groups: expected a non-empty list")
    seen: set[str] = set()

    def check_missing(entries: Any, where: str) -> None:
        if not isinstance(entries, list):
            raise PresentationModelError(f"{where}: expected a list")
        shapes = {"diagnostic": {"kind", "value"}, "symbol": {"kind", "value"},
                  "text": {"kind", "value"}, "parameter": {"kind", "id"},
                  "finding": {"kind", "findingId"}}
        for mi, entry in enumerate(entries):
            mp = f"{where}[{mi}]"
            if not isinstance(entry, Mapping) or entry.get("kind") not in shapes:
                raise PresentationModelError(f"{mp}: invalid classified missing entry")
            kind = entry["kind"]
            optional = {"factId", "symbol"} if kind == "finding" else {"version"} if kind == "parameter" else set()
            _require_keys(entry, frozenset(shapes[kind]), frozenset(optional), mp)
            for key in (shapes[kind] - {"kind"}) | (set(entry) & optional):
                if not isinstance(entry[key], str):
                    raise PresentationModelError(f"{mp}.{key}: expected string")
                if not entry[key]:
                    raise PresentationModelError(f"{mp}.{key}: expected non-empty string")
            if kind == "finding" and not any(key in entry for key in ("factId", "symbol")):
                raise PresentationModelError(f"{mp}: finding missing entry requires recorded factId or symbol")

    def check_pins(pins: Any, where: str) -> None:
        if not isinstance(pins, list):
            raise PresentationModelError(f"{where}: expected a list")
        for pi, pin in enumerate(pins):
            if not isinstance(pin, Mapping):
                raise PresentationModelError(f"{where}[{pi}]: expected a pin object")
            if pin.get("role") == "parameter" and ("origin" in pin or "basisOrigin" in pin):
                raise PresentationModelError(f"{where}[{pi}]: parameter pin cannot carry origin")

    for index, group in enumerate(groups):
        p = f"{path}.groups[{index}]"
        required = {"symbol", "factId", "ruleId", "ruleVersion", "disposition", "pins", "nodes", "responsibilities", "statementOutcome", "sourceFindings", "assumptions"}
        optional = {"statementLabel", "findingId", "value", "missing", "lineNote", "code"}
        _require_keys(group, frozenset(required), frozenset(optional), p)
        for key in ("symbol", "factId", "ruleId", "ruleVersion"):
            if not isinstance(group[key], str) or not group[key]:
                raise PresentationModelError(f"{p}.{key}: expected non-empty string")
        if group["symbol"] != f"{view['amountSymbol']}|{group['factId']}":
            raise PresentationModelError(f"{p}.symbol: does not match the exact keyed amount symbol")
        if group["symbol"] in seen:
            raise PresentationModelError(f"{p}.symbol: duplicate keyed amount")
        seen.add(group["symbol"])
        disposition = group["disposition"]
        if disposition not in {"published", "blocked", "inapplicable"}:
            raise PresentationModelError(f"{p}.disposition: unknown disposition {disposition!r}")
        if disposition == "published":
            if not isinstance(group.get("findingId"), str) or "value" not in group:
                raise PresentationModelError(f"{p}: published amount requires findingId and value")
            if "missing" in group or "code" in group:
                raise PresentationModelError(f"{p}: missing and code are forbidden on a published amount")
        elif disposition == "blocked":
            if ("findingId" in group or "value" in group or not isinstance(group.get("missing"), list)
                or not isinstance(group.get("code"), str) or not group["code"]):
                raise PresentationModelError(f"{p}: blocked amount requires missing and code, and forbids a value")
            check_missing(group["missing"], f"{p}.missing")
        elif "code" in group:
            raise PresentationModelError(f"{p}.code: forbidden on a non-blocked amount")
        elif any(key in group for key in ("findingId", "value", "missing")):
            raise PresentationModelError(f"{p}: inapplicable amount cannot carry a value or missing list")
        if not isinstance(group["pins"], list) or not isinstance(group["nodes"], list) or not isinstance(group["responsibilities"], list):
            raise PresentationModelError(f"{p}: pins, nodes and responsibilities must be lists")
        check_pins(group["pins"], f"{p}.pins")
        if not isinstance(group["sourceFindings"], list) or not isinstance(group["assumptions"], list):
            raise PresentationModelError(f"{p}: sourceFindings and assumptions must be lists")
        source_ids: set[str] = set()
        for si, source in enumerate(group["sourceFindings"]):
            sp = f"{p}.sourceFindings[{si}]"
            _require_keys(source, frozenset({"findingId", "factId", "value", "factTypeId", "factTypeVersion", "factTypeTitle"}), frozenset({"label", "origin"}), sp)
            if not all(isinstance(source.get(k), str) and source[k] for k in ("findingId", "factId", "factTypeId", "factTypeVersion", "factTypeTitle")):
                raise PresentationModelError(f"{sp}: finding and fact-type identity fields must be non-empty strings")
            if source["findingId"] in source_ids:
                raise PresentationModelError(f"{sp}.findingId: duplicate source finding")
            source_ids.add(source["findingId"])
            if "label" in source and (not isinstance(source["label"], str) or not source["label"]):
                raise PresentationModelError(f"{sp}.label: expected non-empty recorded label")
            if source.get("origin") not in {None, "assertion", "declared_default"}:
                raise PresentationModelError(f"{sp}.origin: invalid origin")
        assumption_ids: set[tuple[str, str, str]] = set()
        for ai, assumption in enumerate(group["assumptions"]):
            ap = f"{p}.assumptions[{ai}]"
            _require_keys(assumption, frozenset({"id", "version", "value", "consumerRuleId", "consumerFindingId"}), frozenset(), ap)
            if not all(isinstance(assumption.get(k), str) and assumption[k] for k in ("id", "version", "consumerRuleId")):
                raise PresentationModelError(f"{ap}: malformed parameter assumption")
            if assumption["consumerFindingId"] is not None and not isinstance(assumption["consumerFindingId"], str):
                raise PresentationModelError(f"{ap}.consumerFindingId: expected string or null")
            identity = (assumption["id"], assumption["version"], assumption["consumerRuleId"])
            if identity in assumption_ids:
                raise PresentationModelError(f"{ap}: duplicate assumption consumer")
            assumption_ids.add(identity)
        for ni, node in enumerate(group["nodes"]):
            np = f"{p}.nodes[{ni}]"
            _require_keys(node, frozenset({"findingId", "ruleId", "ruleVersion", "symbol", "value", "pins"}), frozenset({"basisOrigin"}), np)
            if not isinstance(node["pins"], list) or node.get("basisOrigin") not in {None, "assertion", "declared_default"}:
                raise PresentationModelError(f"{np}: malformed pins or basisOrigin")
            check_pins(node["pins"], f"{np}.pins")
        if "statementLabel" in group:
            label = group["statementLabel"]
            _require_keys(label, frozenset(), frozenset({"lender", "statement", "taxYear"}), f"{p}.statementLabel")
            if not label or any(not isinstance(v, str) or not v for v in label.values()):
                raise PresentationModelError(f"{p}.statementLabel: expected non-empty recorded labels")
        if "lineNote" in group and (not isinstance(group["lineNote"], str) or not group["lineNote"]):
            raise PresentationModelError(f"{p}.lineNote: expected non-empty string")
        outcome = group["statementOutcome"]
        _require_keys(outcome, frozenset({"route", "statementScope", "conclusion", "responsibilityFailures"}), frozenset(), f"{p}.statementOutcome")
        for axis_name in ("route", "statementScope", "conclusion"):
            axis = outcome[axis_name]
            _require_keys(axis, frozenset({"interpretation"}), frozenset({"ruleId", "ruleVersion", "readerRole", "symbol", "disposition", "code", "pins", "findingId", "value", "missing", "claims", "factId", "label", "suppliedFindingId", "suppliedValue", "claimType", "claimTypeVersion"}), f"{p}.statementOutcome.{axis_name}")
            if not isinstance(axis["interpretation"], str) or not axis["interpretation"]:
                raise PresentationModelError(f"{p}.statementOutcome.{axis_name}.interpretation: expected string")
            if "ruleId" in axis and (not isinstance(axis.get("readerRole"), str) or not isinstance(axis.get("ruleVersion"), str)):
                raise PresentationModelError(f"{p}.statementOutcome.{axis_name}: producer identity is incomplete")
            disposition = axis.get("disposition")
            if disposition == "blocked":
                if "findingId" in axis or "value" in axis or "missing" not in axis:
                    raise PresentationModelError(f"{p}.statementOutcome.{axis_name}: malformed blocked outcome")
            elif disposition == "published":
                if not isinstance(axis.get("findingId"), str) or "value" not in axis or "missing" in axis:
                    raise PresentationModelError(f"{p}.statementOutcome.{axis_name}: malformed published outcome")
            elif disposition == "inapplicable":
                if any(k in axis for k in ("findingId", "value", "missing")):
                    raise PresentationModelError(f"{p}.statementOutcome.{axis_name}: inapplicable outcome carries a result")
            elif disposition is not None:
                raise PresentationModelError(f"{p}.statementOutcome.{axis_name}: unknown disposition")
            if "missing" in axis:
                if disposition != "blocked":
                    raise PresentationModelError(f"{p}.statementOutcome.{axis_name}.missing: only allowed for blocked outcomes")
                check_missing(axis["missing"], f"{p}.statementOutcome.{axis_name}.missing")
            if "claims" in axis:
                if not isinstance(axis["claims"], list):
                    raise PresentationModelError(f"{p}.statementOutcome.{axis_name}.claims: expected a list")
                for ci, claim in enumerate(axis["claims"]):
                    cp = f"{p}.statementOutcome.{axis_name}.claims[{ci}]"
                    claim_optional = {"ruleId", "ruleVersion", "readerRole", "symbol", "disposition", "code", "pins", "findingId", "value", "missing", "label", "claimType", "claimTypeVersion", "suppliedFindingId", "suppliedValue"}
                    _require_keys(claim, frozenset({"interpretation", "factId"}), frozenset(claim_optional), cp)
                    if not all(isinstance(claim[k], str) and claim[k] for k in ("interpretation", "factId")):
                        raise PresentationModelError(f"{cp}: interpretation and factId must be non-empty strings")
                    if "label" in claim and (not isinstance(claim["label"], str) or not claim["label"]):
                        raise PresentationModelError(f"{cp}.label: expected a recorded non-empty label")
                    if "missing" in claim:
                        check_missing(claim["missing"], f"{cp}.missing")
                    if "ruleId" in claim and (not isinstance(claim.get("readerRole"), str) or not isinstance(claim.get("ruleVersion"), str)):
                        raise PresentationModelError(f"{cp}: classifier producer identity is incomplete")
                    if "claimTypeVersion" in claim and not isinstance(claim["claimTypeVersion"], str):
                        raise PresentationModelError(f"{cp}.claimTypeVersion: expected string")
                    if "pins" in claim:
                        check_pins(claim["pins"], f"{cp}.pins")
        if not isinstance(outcome["responsibilityFailures"], list):
            raise PresentationModelError(f"{p}.statementOutcome.responsibilityFailures: expected a list")
        for fi, failure in enumerate(outcome["responsibilityFailures"]):
            fp = f"{p}.statementOutcome.responsibilityFailures[{fi}]"
            _require_keys(failure, frozenset({"ruleId", "symbol", "code", "missing", "explainedBy"}), frozenset(), fp)
            if not all(isinstance(failure[k], str) for k in ("ruleId", "symbol", "code")) or not isinstance(failure["explainedBy"], list):
                raise PresentationModelError(f"{fp}: malformed responsibility failure")
            check_missing(failure["missing"], f"{fp}.missing")
        for rindex, responsibility in enumerate(group["responsibilities"]):
            rp = f"{p}.responsibilities[{rindex}]"
            _require_keys(responsibility, frozenset({"ruleId", "ruleVersion", "symbol", "findingId", "value", "pins"}), frozenset({"wording"}), rp)
            for key in ("ruleId", "ruleVersion", "symbol", "findingId"):
                if not isinstance(responsibility[key], str) or not responsibility[key]:
                    raise PresentationModelError(f"{rp}.{key}: expected non-empty string")
            if not isinstance(responsibility["pins"], list):
                raise PresentationModelError(f"{rp}.pins: expected a list")
            check_pins(responsibility["pins"], f"{rp}.pins")
            if "wording" in responsibility and (not isinstance(responsibility["wording"], str) or not responsibility["wording"]):
                raise PresentationModelError(f"{rp}.wording: expected non-empty string")
        if (outcome["conclusion"].get("interpretation") != "published"
            and (group["responsibilities"] or "lineNote" in group)):
            raise PresentationModelError(f"{p}: responsibilities and lineNote require a published conclusion")
        if outcome["conclusion"].get("interpretation") == "published":
            if (outcome["route"].get("interpretation") != "bare"
                or outcome["statementScope"].get("interpretation") != "no-whole-amount-disqualifier"):
                raise PresentationModelError(f"{p}: published bare conclusion lacks its required outcome axes")
        if "lineNote" in group:
            conclusion_fid = outcome["conclusion"].get("findingId")
            if not isinstance(conclusion_fid, str) or not any(
                any(pin.get("id") == conclusion_fid for pin in resp.get("pins", []) if isinstance(pin, Mapping))
                for resp in group["responsibilities"]
            ):
                raise PresentationModelError(f"{p}.lineNote: requires a published responsibility pinned to the conclusion")


def validate_presentation_model(model: Mapping[str, Any]) -> None:
    """Strict structural validation: unknown keys and invalid combinations reject."""
    _require_keys(
        model,
        frozenset({
            "schema", "runId", "pinLabels", "sections", "citationGroups", "attachments",
            "unsupportedSourceFindings",
        }),
        frozenset({"authorization", "provenanceGroups", "calculationView", "line21Explanation"}),
        "$",
    )
    if "authorization" in model:
        _validate_authorization_provenance(model["authorization"], "$.authorization")
    if "calculationView" in model:
        _validate_calculation_view(model["calculationView"])
    if "line21Explanation" in model:
        _validate_line21_explanation(model["line21Explanation"])
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
