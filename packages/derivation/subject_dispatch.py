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
default, pinned with ``origin: declared_default``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from packages.derivation.evaluator import AccessLog, Environment, EvalBlocked, evaluate
from packages.derivation.runner import (
    SourceFact,
    _Run,
    _content_id,
    _sorted_pins,
    _value_str,
)

DEPENDENCY_ABSENT = "DEPENDENCY_ABSENT"
DEPENDENCY_INVALID = "DEPENDENCY_INVALID"


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
) -> tuple[Any, tuple[str, str, str, str | None]] | None:
    """The ordinary manufactured default for one unbound symbol, or None.

    The finding id is the same content id ``_Run`` mints when an
    ``optional_default`` binding fills a symbol: adoption, governance, and
    the declared parameter, hashed with ``resolved_input``.
    """
    binding: Mapping[str, Any] | None = None
    for candidate in run.ctx.input_bindings:
        if candidate.get("symbol") == symbol and candidate.get("mode") == "optional_default":
            binding = candidate
            break
    if binding is None:
        return None
    fact_type = binding.get("fact_type")
    if not isinstance(fact_type, dict) or not fact_type.get("id"):
        return None
    fact_type_id = str(fact_type["id"])
    fact_def = next(
        (item for item in run.ctx.fact_types if item.get("id") == fact_type_id),
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
    return param_val, (finding_id, "v2", "input", "declared_default")


def _requires(rule: Mapping[str, Any]) -> list[str]:
    raw = rule.get("requires", [])
    if not isinstance(raw, list):
        return []
    return [str(item) for item in raw]


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
    inapplicable: list[SubjectInapplicable] = []
    blocked: list[SubjectBlocked] = []
    required = _requires(rule)
    other_names = sorted({source.name for source in sources if source.name != subject_type})

    for subject in subjects:
        subject_fact_id = _subject_id(subject)
        symbol = f"{rule['publishes']}|{subject_fact_id}"
        symbol_pin: dict[str, tuple[str, str, str, str | None]] = {
            subject_type: (subject.finding_id, "v1", "input", "assertion"),
        }
        local_symbols: dict[str, Any] = {subject_type: _decode(subject.value)}
        fact_types = dict(run.symbol_fact_types)
        fact_types[subject_type] = _fact_type_of(run, subject_type)
        invalid: list[str] = []
        absent: list[str] = []
        scoped: dict[str, list[SourceFact]] = {}

        for name in other_names:
            candidates = [source for source in sources if source.name == name]
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
                    value, pin = default
                    local_symbols[req] = value
                    symbol_pin[req] = pin
                    fact_types[req] = _fact_type_of(run, req)
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
            value, pin = default
            local_symbols[req] = value
            symbol_pin[req] = pin
            fact_types[req] = _fact_type_of(run, req)

        maps = _local_maps(run, subject_type, subject, scoped)

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

    return SubjectScopedResult(
        publications=tuple(publications),
        inapplicable=tuple(inapplicable),
        blocked=tuple(blocked),
    )
