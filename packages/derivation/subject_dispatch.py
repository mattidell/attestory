"""Per-subject dispatch over the collected sources of one fact type.

The single-subject counterpart of pairing dispatch. Calling code invokes it
through ``_Run.evaluate_subject_scoped_rule``. Nothing in rule content
selects it. One declared rule is evaluated once per collected subject, and
that subject gets exactly one published finding, one inapplicable row, or
one blocked row. Another subject's findings are not bound, read, or pinned.

Other collected types join to a subject by agreeing values on shared key
names. The join is single-hop: a type connected to the subject only through
a third type is not reached. A type that shares no key names with the
subject is not joined. Missing keys fail closed.

Where a required type has no joined source and the run declares an
``optional_default`` for its symbol, that subject alone takes the declared
default, pinned with ``origin: declared_default``. The finding that pin
names is returned once per content id so the runner can record it.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from packages.derivation.evaluator import (
    KEYS_UNAVAILABLE,
    AccessLog,
    Environment,
    EvalBlocked,
    evaluate,
)
from packages.derivation.runner import (
    SourceFact,
    _Run,
    _content_id,
    _sorted_pins,
    _value_str,
)

DEPENDENCY_ABSENT = "DEPENDENCY_ABSENT"
DEPENDENCY_INVALID = "DEPENDENCY_INVALID"
LINK_COVERAGE_UNJOINABLE = "link-coverage-unjoinable"


@dataclass(frozen=True)
class SubjectInapplicable:
    """The rule's guard was false for this subject. No finding is published."""

    subject_fact_id: str
    symbol: str
    pins: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class SubjectBlocked:
    """A dependency was absent or invalid for this subject alone."""

    subject_fact_id: str
    symbol: str
    code: str
    missing: tuple[str, ...]
    pins: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class SubjectScopedResult:
    publications: tuple[dict[str, Any], ...]
    inapplicable: tuple[SubjectInapplicable, ...]
    blocked: tuple[SubjectBlocked, ...]
    # Parallel to ``publications``. The subject ``SourceFact``'s structured
    # keys at dispatch time. Not a field of the derived finding, and not
    # recovered from its rendered symbol.
    publication_subject_keys: tuple[tuple[tuple[str, str], ...] | None, ...]
    # One derived-finding.v2 per content id this dispatch pinned as a
    # declared default. Not a subject publication and not a disposition.
    declared_defaults: tuple[dict[str, Any], ...]


def _decode(raw: Any) -> Any:
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw
    return raw


def _keys(source: SourceFact) -> dict[str, str] | None:
    if source.keys is None:
        return None
    return {name: value for name, value in source.keys}


def _subject_id(source: SourceFact) -> str:
    return source.fact_id or source.finding_id


def _scope(
    subject: SourceFact, candidates: Sequence[SourceFact]
) -> list[SourceFact] | None:
    """Sources of one other type that belong to this subject.

    Join is agreeing values on shared key names. No shared key name means
    this type is not joined. ``None`` means identity is unavailable.
    Callers fail closed rather than parse ``fact_id`` or reuse another
    subject's finding. An empty list means the keys were readable and
    nothing joined.
    """
    if not candidates:
        return []
    subject_keys = _keys(subject)
    if subject_keys is None:
        return None
    keyed: list[tuple[SourceFact, dict[str, str]]] = []
    for candidate in candidates:
        keys = _keys(candidate)
        if keys is None:
            return None
        keyed.append((candidate, keys))
    shared: set[str] = set()
    for _, keys in keyed:
        shared.update(set(subject_keys).intersection(keys))
    if not shared:
        return []
    matched: list[SourceFact] = []
    for candidate, keys in keyed:
        if all(keys.get(name) == subject_keys[name] for name in shared):
            matched.append(candidate)
    return matched


def _fact_type_of(run: _Run, symbol: str) -> str:
    for binding in run.ctx.input_bindings:
        if binding.get("symbol") != symbol:
            continue
        fact_type = binding.get("fact_type")
        if isinstance(fact_type, dict) and fact_type.get("id"):
            return str(fact_type["id"])
    existing = run.symbol_fact_types.get(symbol)
    if existing:
        return str(existing)
    return symbol


def _optional_default(
    run: _Run, symbol: str
) -> tuple[Any, tuple[str, str, str, str | None], dict[str, Any]] | None:
    """The manufactured default for one symbol, or None.

    The finding id is the content id ``_Run`` mints for an
    ``optional_default`` binding: adoption, governance, and the declared
    parameter, hashed with ``resolved_input``. The finding is that same
    ``derived-finding.v2``. The caller records it.
    """
    binding: Mapping[str, Any] | None = None
    for candidate in run.ctx.input_bindings:
        if candidate.get("symbol") == symbol and candidate.get("mode") == "optional_default":
            binding = candidate
            break
    if binding is None:
        return None
    fact_type = binding.get("fact_type")
    if not isinstance(fact_type, dict) or not fact_type.get("id") or not fact_type.get("version"):
        return None
    fact_type_id = str(fact_type["id"])
    fact_type_version = str(fact_type["version"])
    # Track 5c Round 2 (Defect 4, same class as Defect 2): the exact pinned
    # (id, version), never the first id match. A weaker/undeclared version of
    # the same id declared earlier in `run.ctx.fact_types` must not silently
    # answer -- or fail to answer -- for the version the binding actually
    # pins.
    fact_def = next(
        (
            item for item in run.ctx.fact_types
            if item.get("id") == fact_type_id and item.get("version") == fact_type_version
        ),
        None,
    )
    if fact_def is None or "optional_default" not in fact_def:
        return None
    parameter = fact_def["optional_default"].get("parameter")
    if not isinstance(parameter, dict):
        return None
    param_id = parameter.get("id")
    param_version = parameter.get("version")
    if not isinstance(param_id, str) or not isinstance(param_version, str):
        return None
    param_val = run.ctx.parameters.get(param_id, {}).get("values")
    if param_val is None:
        return None
    pins = _sorted_pins([
        run.ctx.adoption_pin,
        *run.ctx.governance_pins,
        {"role": "parameter", "id": param_id, "version": param_version},
    ])
    body = {
        "symbol": symbol,
        "value": _value_str(param_val),
        "pins": pins,
        "resolved_input": {"fact_id": fact_type_id, "origin": "declared_default"},
    }
    finding_id = _content_id("finding:derived:", body)
    finding = {
        "schema": "derived-finding.v2",
        "id": finding_id,
        "symbol": symbol,
        "value": body["value"],
        "version": "v2",
        "pins": pins,
        "resolved_input": body["resolved_input"],
    }
    return param_val, (finding_id, "v2", "input", "declared_default"), finding


def _declared_link_coverage_names(
    expr: Any, fields: tuple[str, ...] = ("links", "reductions"),
) -> list[str]:
    """Named ``link_coverage`` fields from ``value``, in ``fields`` order.

    The node's own fields are not ``ref`` names. ``when`` is not walked.
    """
    names: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if node.get("op") == "link_coverage":
                for key in fields:
                    name = node.get(key)
                    if isinstance(name, str) and name and name not in names:
                        names.append(name)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(expr)
    return names


def _present_rows_share_no_key_name(
    subject: SourceFact, candidates: Sequence[SourceFact],
) -> bool:
    """Present rows whose key names are disjoint from the subject's.

    Zero candidates are not this case. A missing key tuple is not this
    case: ``_scope`` returns None and the slot is the keys-unavailable
    sentinel. A shared name whose values disagree is a join of nothing,
    not this case. ``_scope`` itself is not used and is not changed.
    """
    if not candidates:
        return False
    subject_keys = _keys(subject)
    if subject_keys is None:
        return False
    shared: set[str] = set()
    for candidate in candidates:
        keys = _keys(candidate)
        if keys is None:
            return False
        shared.update(set(subject_keys).intersection(keys))
    return not shared


def _requires(rule: Mapping[str, Any]) -> list[str]:
    raw = rule.get("requires", [])
    if not isinstance(raw, list):
        return []
    return [str(item) for item in raw]


def _identity_names(run: _Run, fact_type_id: str, fact_type_version: str) -> list[str]:
    """Declared ``identity_keys`` names for one fact-type citizen, by the
    exact pinned ``(id, version)``.

    Read from the run's fact-type declarations, never from a row -- ADR
    0076 Part 2. Static package validation resolves the same exact pin
    (``package_validation._subject_relationship_issues`` /
    ``_exact_pin_key``): a rule can declare a stronger identity at a later
    version while a weaker declaration of the same id is also present in
    the package (Track 5c Defect 2) -- matching by id alone would let
    whichever declaration a caller happened to list first silently govern
    the presence check regardless of which version the rule actually
    pinned. An id match at the wrong version is not a resolution; the
    caller's existing "identity unreadable" fail-closed path (an empty
    result) applies exactly as it does when the id is absent entirely.
    """
    for fact_type in run.ctx.fact_types:
        if fact_type.get("id") == fact_type_id and fact_type.get("version") == fact_type_version:
            return [
                key["name"]
                for key in fact_type.get("identity_keys", [])
                if isinstance(key, dict) and isinstance(key.get("name"), str)
            ]
    return []


def _presence_declaration(
    run: _Run, rule: Mapping[str, Any]
) -> tuple[str, list[str], str] | None:
    """ADR 0076 Part 2's runtime presence declaration.

    Returns the declared ``joined`` type's id, the identity-key names every
    present row of that type must carry to be classified, and the fact-type
    id those names were read from (the "reference" type: the subject type
    under ``joined_contains_subject``, the joined type under
    ``subject_contains_joined``) -- or ``None`` when the rule declares
    neither ``joined`` nor ``direction``. ``_scope`` then applies to every
    source type unchanged.

    The returned name list can be empty when the reference type is not in
    ``run.ctx.fact_types``, or is present but declares no identity-key
    names. The caller must not treat that as "nothing is required" --
    ``fact-type.v2`` always requires at least one named identity key, so an
    empty list here means the declaration could not be read, not that it
    was read as empty (Defect 1: an empty ``required`` makes every row
    trivially "complete" and every containment check vacuously true, which
    would join everything instead of failing closed).
    """
    direction = rule.get("direction")
    if direction not in ("joined_contains_subject", "subject_contains_joined"):
        return None
    joined = rule.get("joined")
    subject = rule.get("subject")
    if not isinstance(joined, Mapping) or not isinstance(subject, Mapping):
        return None
    joined_id = joined.get("id")
    joined_version = joined.get("version")
    subject_id = subject.get("id")
    subject_version = subject.get("version")
    if not isinstance(joined_id, str) or not isinstance(subject_id, str):
        return None
    if direction == "joined_contains_subject":
        reference_id, reference_version = subject_id, subject_version
    else:
        reference_id, reference_version = joined_id, joined_version
    if not isinstance(reference_version, str):
        # A malformed pin (no version) is the same "cannot be read" case as
        # an absent fact type: fail closed via the caller's empty-required-
        # names path rather than matching by id alone.
        return joined_id, [], reference_id
    return joined_id, _identity_names(run, reference_id, reference_version), reference_id


def _malformed_joined_rows(
    sources: Sequence[SourceFact], joined_id: str, required: Sequence[str],
) -> list[str]:
    """Present rows of ``joined_id`` lacking a required identity name.

    Finding ids, sorted. ADR 0076 Part 2: the row's owner cannot be
    determined, so every subject evaluating the rule blocks on it, naming
    the row -- it is not dropped and it is not the no-link parameter. A row
    sharing no key name at all with any subject is a special case of this:
    it necessarily lacks every required name too.
    """
    malformed: list[str] = []
    for row in sources:
        if row.name != joined_id:
            continue
        row_keys = _keys(row)
        if row_keys is None or any(name not in row_keys for name in required):
            malformed.append(row.finding_id)
    return sorted(malformed)


def _presence_matched(
    subject: SourceFact, candidates: Sequence[SourceFact], required: Sequence[str],
) -> list[SourceFact] | None:
    """This subject's complete, agreeing rows of the declared joined type.

    ``None`` when the subject's own keys are unavailable, or the subject's
    own keys do not carry every required name -- both fail closed the same
    way: the caller's existing "subject keys absent" handling applies
    unchanged (``link-coverage-keys-unavailable`` inside a ``link_coverage``
    rule; the ordinary required-source ``DEPENDENCY_INVALID``/``DEPENDENCY_
    ABSENT`` path otherwise). ADR 0076 Part 2: the no-link result is
    returned for a subject only "when its own keys are present" -- a
    subject missing one of its own required identity names is not the same
    as a subject with zero joined rows, and must not silently take the
    no-link default (Defect 2). A malformed *row* is never returned here:
    the caller has already blocked every subject on it before this runs
    (``_malformed_joined_rows`` above). A complete row whose required
    values disagree is silently excluded here: another subject's, not this
    one's, and it does not prevent this subject's no-link result.
    """
    subject_keys = _keys(subject)
    if subject_keys is None or any(name not in subject_keys for name in required):
        return None
    matched: list[SourceFact] = []
    for candidate in candidates:
        row_keys = _keys(candidate) or {}
        if any(name not in row_keys for name in required):
            continue
        if all(row_keys[name] == subject_keys.get(name) for name in required):
            matched.append(candidate)
    return matched


def _local_maps(
    run: _Run,
    subject_type: str,
    subject: SourceFact,
    scoped: Mapping[str, Sequence[SourceFact]],
) -> tuple[dict[str, list[str]], dict[str, list[str]], dict[str, list[str]]]:
    sources = {name: list(values) for name, values in run.sources.items()}
    fids = {name: list(values) for name, values in run.source_fids.items()}
    fact_ids = {name: list(values) for name, values in run.source_fact_ids.items()}

    def install(name: str, facts: Sequence[SourceFact]) -> None:
        sources[name] = [fact.value for fact in facts]
        fids[name] = [fact.finding_id for fact in facts]
        fact_ids[name] = [_subject_id(fact) for fact in facts]

    install(subject_type, [subject])
    for name, facts in scoped.items():
        install(name, facts)
    return sources, fids, fact_ids


def _assemble_pins(
    run: _Run,
    rule: Mapping[str, Any],
    access: AccessLog,
    symbol_pin: dict[str, tuple[str, str, str, str | None]],
    sources: dict[str, list[str]],
    source_fids: dict[str, list[str]],
    source_fact_ids: dict[str, list[str]],
    subject_type: str,
) -> list[dict[str, Any]]:
    """``pins_for`` against this subject's bindings, never the run-wide ones."""
    saved_pin = run.symbol_pin
    saved_sources = run.sources
    saved_fids = run.source_fids
    saved_fact_ids = run.source_fact_ids
    run.symbol_pin = symbol_pin
    run.sources = sources
    run.source_fids = source_fids
    run.source_fact_ids = source_fact_ids
    try:
        pins = list(run.pins_for(dict(rule), access))
        if subject_type in symbol_pin:
            pins.append(run._symbol_pin_entry(subject_type))
        for finding_id in access.link_coverage_findings:
            pin: dict[str, Any] = {"role": "input", "id": finding_id, "version": "v1"}
            if run.use_v2:
                pin["origin"] = "assertion"
            pins.append(pin)
        return _sorted_pins(pins)
    finally:
        run.symbol_pin = saved_pin
        run.sources = saved_sources
        run.source_fids = saved_fids
        run.source_fact_ids = saved_fact_ids


def _pins_naming(
    run: _Run,
    rule: Mapping[str, Any],
    names: Sequence[str],
    symbol_pin: dict[str, tuple[str, str, str, str | None]],
    sources: dict[str, list[str]],
    source_fids: dict[str, list[str]],
    source_fact_ids: dict[str, list[str]],
    subject_type: str,
) -> list[dict[str, Any]]:
    access = AccessLog()
    for name in names:
        if name in symbol_pin:
            access.refs.add(name)
    return _assemble_pins(
        run, rule, access, symbol_pin, sources, source_fids, source_fact_ids, subject_type
    )


def _publication(
    run: _Run, symbol: str, value: Any, pins: list[dict[str, Any]]
) -> dict[str, Any]:
    rendered = _value_str(value)
    body = {"symbol": symbol, "value": rendered, "pins": pins}
    finding = {
        "schema": "derived-finding.v2",
        "id": _content_id("finding:derived:", body),
        "symbol": symbol,
        "value": rendered,
        "version": "v2",
        "pins": pins,
    }
    run.schemas.validate_declared(finding)
    return finding


def _one_source(matched: Sequence[SourceFact]) -> SourceFact | None:
    """The only match, or the sort-first match when every value agrees.

    ``None`` when more than one match disagrees. The caller names those
    fact ids; this does not pick one of them.
    """
    if len(matched) == 1:
        return matched[0]
    ordered = sorted(matched, key=lambda source: source.finding_id)
    if len({source.value for source in ordered}) == 1:
        return ordered[0]
    return None


def evaluate_subject_scoped_rule(
    *,
    sources: Sequence[SourceFact],
    subject_type: str,
    rule: Mapping[str, Any],
    run: _Run,
) -> SubjectScopedResult:
    """Evaluate ``rule`` once per collected source of ``subject_type``."""
    subjects = sorted(
        (source for source in sources if source.name == subject_type),
        key=_subject_id,
    )
    publications: list[dict[str, Any]] = []
    publication_keys: list[tuple[tuple[str, str], ...] | None] = []
    declared_defaults: dict[str, dict[str, Any]] = {}
    inapplicable: list[SubjectInapplicable] = []
    blocked: list[SubjectBlocked] = []
    required = _requires(rule)
    coverage_names = _declared_link_coverage_names(rule.get("value"))
    link_type_names = _declared_link_coverage_names(rule.get("value"), ("links",))

    # ADR 0076 Part 2: a rule that declares `joined`/`direction` replaces
    # `_scope`'s shared-name union for that one declared type with a
    # presence check by identity-key names. Every other source type this
    # rule reads keeps `_scope`; an undeclared rule keeps `_scope` entirely
    # (`presence` is None, `joined_id` stays None, and every `name ==
    # joined_id` guard below is unreachable).
    presence = _presence_declaration(run, rule)
    joined_id: str | None = presence[0] if presence is not None else None
    required_names: list[str] = presence[1] if presence is not None else []
    # Track 5c Defect 3: a declared `joined` type is scoped here even when
    # zero rows of it exist anywhere in this run. Without this, a name with
    # no candidate rows never enters `other_names`, `scoped` has no key for
    # it, and the `required` loop below falls through to `run.symbol_pin`/
    # `run.symbols` -- a run-wide scalar an unrelated ordinary rule happens
    # to publish under the same symbol name, read as if it were the joined
    # row's own value. Scoping it unconditionally makes "zero rows" produce
    # `scoped[joined_id] == []` (an ordinary empty join, handled by the
    # existing optional_default/absent branch below) and also overwrites
    # the local sources map for that name (`_local_maps`), so the joined
    # type's value is not readable from the run-wide environment during
    # this subject's evaluation either.
    other_names = sorted(
        {source.name for source in sources if source.name != subject_type}
        | ({joined_id} if joined_id is not None else set())
    )
    # Defect 1: an unreadable reference type (absent from `run.ctx.
    # fact_types`, or declared with no identity-key names) must not be
    # treated as "nothing is required" -- that would make every row
    # trivially complete and every subject's containment check vacuously
    # true, joining everything. Fail closed instead: every subject
    # evaluating this rule blocks, naming the reference fact-type id (a
    # symbol/type id, not a finding id -- reader-contract section 4 class 3,
    # since it is a fact-type id in the resolved graph and not a finding id
    # in state).
    identity_unreadable_type: str | None = None
    if presence is not None and not required_names:
        identity_unreadable_type = presence[2]
    malformed_finding_ids = (
        _malformed_joined_rows(sources, joined_id, required_names)
        if joined_id is not None and identity_unreadable_type is None
        else []
    )

    for subject in subjects:
        subject_fact_id = _subject_id(subject)
        symbol = f"{rule['publishes']}|{subject_fact_id}"
        symbol_pin: dict[str, tuple[str, str, str, str | None]] = {
            subject_type: (subject.finding_id, "v1", "input", "assertion"),
        }
        local_symbols: dict[str, Any] = {subject_type: _decode(subject.value)}
        fact_types = dict(run.symbol_fact_types)
        fact_types[subject_type] = _fact_type_of(run, subject_type)

        if identity_unreadable_type is not None:
            blocked.append(SubjectBlocked(
                subject_fact_id=subject_fact_id,
                symbol=symbol,
                code=DEPENDENCY_INVALID,
                missing=(identity_unreadable_type,),
                pins=tuple(_pins_naming(
                    run, rule, (subject_type,), symbol_pin,
                    *_local_maps(run, subject_type, subject, {}), subject_type,
                )),
            ))
            continue

        if malformed_finding_ids:
            # A malformed row's owner cannot be determined, so it cannot be
            # excluded from any subject: every subject evaluating this rule
            # blocks on it, naming the row -- not dropped, never the
            # no-link parameter.
            blocked.append(SubjectBlocked(
                subject_fact_id=subject_fact_id,
                symbol=symbol,
                code=DEPENDENCY_INVALID,
                missing=tuple(malformed_finding_ids),
                pins=tuple(_pins_naming(
                    run, rule, (subject_type,), symbol_pin,
                    *_local_maps(run, subject_type, subject, {}), subject_type,
                )),
            ))
            continue

        invalid: list[str] = []
        absent: list[str] = []
        scoped: dict[str, list[SourceFact]] = {}

        for name in other_names:
            candidates = [source for source in sources if source.name == name]
            if joined_id is not None and name == joined_id:
                matched = _presence_matched(subject, candidates, required_names)
            else:
                matched = _scope(subject, candidates)
            if matched is None:
                scoped[name] = []
                if name in required:
                    invalid.append(name)
                continue
            scoped[name] = list(matched)

        for req in required:
            if req == subject_type or req in invalid:
                continue
            if req in scoped:
                matched = scoped[req]
                if not matched:
                    default = _optional_default(run, req)
                    if default is None:
                        absent.append(req)
                        continue
                    value, pin, finding = default
                    local_symbols[req] = value
                    symbol_pin[req] = pin
                    fact_types[req] = _fact_type_of(run, req)
                    declared_defaults.setdefault(finding["id"], finding)
                    continue
                chosen = _one_source(matched)
                if chosen is None:
                    invalid.extend(_subject_id(source) for source in matched)
                    continue
                local_symbols[req] = _decode(chosen.value)
                symbol_pin[req] = (chosen.finding_id, "v1", "input", "assertion")
                fact_types[req] = _fact_type_of(run, req)
                continue
            if req in run.symbol_pin and req in run.symbols:
                local_symbols[req] = run.symbols[req]
                symbol_pin[req] = run.symbol_pin[req]
                fact_types[req] = _fact_type_of(run, req)
                continue
            default = _optional_default(run, req)
            if default is None:
                absent.append(req)
                continue
            value, pin, finding = default
            local_symbols[req] = value
            symbol_pin[req] = pin
            fact_types[req] = _fact_type_of(run, req)
            declared_defaults.setdefault(finding["id"], finding)

        maps = _local_maps(run, subject_type, subject, scoped)
        # Both declared names, on every subject. Empty is a join that
        # found nothing; the sentinel is ``_scope`` returning None. The
        # sentinel is not written into the sources map above.
        keyed_sources: dict[str, Any] = {}
        for name in coverage_names:
            if subject.keys is None:
                # ADR 0075: the no-link default requires the subject's own
                # identity. `_scope` returns [] for zero candidates without
                # reading keys, which would let a subject of unknown identity
                # take the default. Refuse it here, for coverage names only.
                keyed_sources[name] = KEYS_UNAVAILABLE
                continue
            candidates = [source for source in sources if source.name == name]
            if joined_id is not None and name == joined_id:
                matched = _presence_matched(subject, candidates, required_names)
            else:
                matched = _scope(subject, candidates)
            keyed_sources[name] = list(matched) if matched is not None else KEYS_UNAVAILABLE

        if invalid:
            blocked.append(SubjectBlocked(
                subject_fact_id=subject_fact_id,
                symbol=symbol,
                code=DEPENDENCY_INVALID,
                missing=tuple(invalid),
                pins=tuple(_pins_naming(
                    run, rule, (subject_type,), symbol_pin, *maps, subject_type
                )),
            ))
            continue
        if absent:
            blocked.append(SubjectBlocked(
                subject_fact_id=subject_fact_id,
                symbol=symbol,
                code=DEPENDENCY_ABSENT,
                missing=tuple(absent),
                pins=tuple(_pins_naming(
                    run, rule, tuple(symbol_pin), symbol_pin, *maps, subject_type
                )),
            ))
            continue

        # The third positional slot is the run's resolved admissions.
        # Only the runner and the evaluator may name that field.
        env = Environment(
            local_symbols,
            maps[0],
            frozenset(run.admissions),
            dict(run.ctx.parameters),
            dict(run.ctx.canon),
            fact_types,
            dict(run.categorical_domains),
            keyed_sources=keyed_sources if coverage_names else {},
        )
        access = AccessLog()
        try:
            guard = bool(evaluate(rule["when"], env, access))
        except EvalBlocked as exc:
            blocked.append(SubjectBlocked(
                subject_fact_id=subject_fact_id,
                symbol=symbol,
                code=exc.category,
                missing=tuple(str(item) for item in exc.missing),
                pins=tuple(_assemble_pins(run, rule, access, symbol_pin, *maps, subject_type)),
            ))
            continue
        if not guard:
            inapplicable.append(SubjectInapplicable(
                subject_fact_id=subject_fact_id,
                symbol=symbol,
                pins=tuple(_assemble_pins(run, rule, access, symbol_pin, *maps, subject_type)),
            ))
            continue
        # Present unjoinable link rows are not the no-link default. The
        # joined slots are both [] in that case and in a real empty join,
        # so the operation cannot tell them apart. Orphan and keys-unavailable
        # slots are not [], and those earlier blocks still run in value.
        unjoinable = (
            bool(coverage_names)
            and all(keyed_sources.get(name) == [] for name in coverage_names)
            and any(
                _present_rows_share_no_key_name(
                    subject,
                    [source for source in sources if source.name == name],
                )
                for name in link_type_names
            )
        )
        if unjoinable:
            blocked.append(SubjectBlocked(
                subject_fact_id=subject_fact_id,
                symbol=symbol,
                code=DEPENDENCY_INVALID,
                missing=(LINK_COVERAGE_UNJOINABLE,),
                pins=tuple(_assemble_pins(
                    run, rule, access, symbol_pin, *maps, subject_type
                )),
            ))
            continue
        try:
            value = evaluate(rule["value"], env, access)
        except EvalBlocked as exc:
            blocked.append(SubjectBlocked(
                subject_fact_id=subject_fact_id,
                symbol=symbol,
                code=exc.category,
                missing=tuple(str(item) for item in exc.missing),
                pins=tuple(_assemble_pins(run, rule, access, symbol_pin, *maps, subject_type)),
            ))
            continue
        pins = _assemble_pins(run, rule, access, symbol_pin, *maps, subject_type)
        publications.append(_publication(run, symbol, value, pins))
        publication_keys.append(subject.keys)

    return SubjectScopedResult(
        publications=tuple(publications),
        inapplicable=tuple(inapplicable),
        blocked=tuple(blocked),
        publication_subject_keys=tuple(publication_keys),
        declared_defaults=tuple(declared_defaults.values()),
    )
