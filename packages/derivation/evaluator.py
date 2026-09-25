"""Expression evaluation over the closed operation vocabulary.

The evaluator executes the ADR-0006 expression tree against an environment,
deferring the meaning of the three data operations to the operation-semantics
canon (decision 4) rather than baking arithmetic conventions in here. Every
read is recorded in an AccessLog so the runner can build publication pins
from what was actually consumed, never from invented constants (ADR-0007
decision 4).

Blocking is a typed, contained signal (decision 8), not an exception that
escapes the run: an absent dependency, a present-but-invalid value, and an
unclosed empty source set are distinct codes the runner records.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_EVEN, ROUND_HALF_UP, ROUND_UP
from typing import Any, Mapping

from packages.derivation.authorization import AuthorizationResolution

# Blocking categories (ADR-0006 decision 8). The vocabulary distinguishes a
# dependency that is absent from one that is present but invalid, and an
# unclosed source set from either.
BLOCK_ABSENT = "DEPENDENCY_ABSENT"
BLOCK_INVALID = "DEPENDENCY_INVALID"
BLOCK_CLOSURE = "SOURCE_SET_UNCLOSED"
BLOCK_LOOKUP_MISS = "LOOKUP_MISS"
BLOCK_CATEGORICAL_DOMAIN_MISMATCH = "CATEGORICAL_DOMAIN_MISMATCH"

# Slot value per-subject dispatch writes when ``_scope`` returns None for
# a name ``link_coverage`` declares. Not a row, and not an empty join.
KEYS_UNAVAILABLE = "keys_unavailable"
LINK_COVERAGE_SCOPE_UNBOUND = "link-coverage-scope-unbound"
LINK_COVERAGE_KEYS_UNAVAILABLE = "link-coverage-keys-unavailable"

_ROUND_MODES = {
    "half_up": ROUND_HALF_UP,
    "half_even": ROUND_HALF_EVEN,
    "down": ROUND_DOWN,
    "up": ROUND_UP,
}


class EvalBlocked(Exception):
    """Evaluation cannot proceed for a contained, categorized reason."""

    def __init__(self, category: str, missing: list[str]) -> None:
        self.category = category
        self.missing = missing
        super().__init__(f"{category}: {', '.join(missing)}")


_CATEGORICAL_VERSION_SEP = "\x1f"


def categorical_domain_key(fact_type_id: str, version: str) -> str:
    """Domain-map key for one fact-type version. Not an id-only key."""
    return f"{fact_type_id}{_CATEGORICAL_VERSION_SEP}{version}"


def _indexed_versions(
    index: Mapping[str, Mapping[str, Any]] | None, param_id: str,
) -> Mapping[str, Any] | None:
    """Versions of ``param_id`` in the exact index, or None when it does not list that id.

    An empty index lists nothing, so a hand-built context keeps the id-keyed
    citizen. An id the index does list is never answered by a sibling.
    """
    if not index:
        return None
    versions = index.get(param_id)
    return versions if isinstance(versions, dict) else None


def parameter_exact(
    parameters: Mapping[str, Any],
    param_id: str,
    version: str,
    index: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any] | None:
    """The citizen named by ``(id, version)``, or None. Never a sibling."""
    versions = _indexed_versions(index, param_id)
    if versions is not None:
        found = versions.get(version)
        return found if isinstance(found, dict) else None
    citizen = parameters.get(param_id)
    if not isinstance(citizen, dict) or "values" not in citizen:
        return None
    # A hand-built citizen may omit version. A citizen that names one is
    # that version only, never a stand-in for a different pin.
    citizen_version = citizen.get("version")
    if citizen_version is None or citizen_version == version:
        return citizen
    return None


def parameter_version_count(
    parameters: Mapping[str, Any],
    param_id: str,
    index: Mapping[str, Mapping[str, Any]] | None = None,
) -> int:
    versions = _indexed_versions(index, param_id)
    if versions is not None:
        return len(versions)
    citizen = parameters.get(param_id)
    if isinstance(citizen, dict) and isinstance(citizen.get("version"), str) and "values" in citizen:
        return 1
    return 0


def parameter_unversioned(
    parameters: Mapping[str, Any],
    param_id: str,
    index: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any] | None:
    """The only version of ``param_id``, or None when it is missing or ambiguous."""
    versions = _indexed_versions(index, param_id)
    if versions is not None:
        if len(versions) != 1:
            return None
        found = next(iter(versions.values()))
        return found if isinstance(found, dict) else None
    citizen = parameters.get(param_id)
    if isinstance(citizen, dict) and isinstance(citizen.get("version"), str) and "values" in citizen:
        return citizen
    return None


@dataclass
class AccessLog:
    """What an evaluation actually read, for truthful pinning."""

    refs: set[str] = field(default_factory=set)
    collects: set[str] = field(default_factory=set)
    parameters: set[str] = field(default_factory=set)
    tables: set[str] = field(default_factory=set)
    # ``(id, version)`` actually read. Pinning uses this rather than whichever
    # citizen an id-keyed map happens to hold.
    parameter_versions: set[tuple[str, str]] = field(default_factory=set)
    operations: set[str] = field(default_factory=set)
    # Families whose closure authority an empty collect actually stood on;
    # a closure-backed zero pins these, present-source aggregation never
    # populates it (ADR-0014 decision 5).
    closure_reads: set[str] = field(default_factory=set)
    # ADR-0074: names read through bound_sources. Never merged into
    # ``collects`` — dependency_pins_for_access pins every source_fids
    # entry for collects, which is the run-wide pin leak.
    bound_source_names: set[str] = field(default_factory=set)
    # Coverage contract: finding ids this operation matched or left
    # uncovered. Not merged into ``collects`` — that channel pins every
    # row of the source name, including other statements.
    link_coverage_findings: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class Environment:
    """Everything a rule may read, plus the canon that gives ops meaning."""

    symbols: dict[str, Any]                 # published/input symbol -> value
    sources: dict[str, list[str]]           # collectable raw fact name -> decimal-strings
    closed_sets: frozenset[str]             # source sets asserted complete (layer 2)
    parameters: dict[str, dict[str, Any]]   # parameter id -> parameter citizen
    canon: dict[str, dict[str, Any]]        # operation -> operation-semantics citizen
    symbol_fact_types: dict[str, str] = field(default_factory=dict)
    categorical_domains: dict[str, list[str]] = field(default_factory=dict)
    # ADR-0069: resolved standing-authorization disposition for this
    # composition. Evaluation of expression trees does not consult it (tax
    # arithmetic stays independent of currentness). Callers that need
    # currentness read ``authorization`` and pin it via
    # ``authorization_provenance`` / ``explain(..., authorization=...)``.
    authorization: AuthorizationResolution | None = None
    # ADR-0074: coordinator-selected nonempty groups, keyed by fact type.
    # Defaulted so the committed five-positional Environment construction
    # at pairing_consequences.py keeps working. Ordinary _Run.env() leaves
    # this empty; the operator then fail-closes.
    bound_sources: dict[str, list[Any]] = field(default_factory=dict)
    # Coverage contract. Defaulted like bound_sources so an ordinary
    # Environment leaves the slot unbound and the operation fail-closes.
    # Per-subject dispatch installs one entry per declared name: a list
    # of rows, or the keys_unavailable sentinel. The operation does not
    # read ``sources``.
    keyed_sources: dict[str, Any] = field(default_factory=dict)
    # Symbol name -> fact-type version the binding or declaration pinned.
    # Absent means the symbol named no version (a derived symbol's fallback).
    symbol_fact_versions: dict[str, str] = field(default_factory=dict)
    # Parameter id -> version -> citizen. Empty for a hand-built environment;
    # an id listed here is read by exact version and is not borrowed from
    # ``parameters``.
    parameter_index: dict[str, dict[str, dict[str, Any]]] = field(default_factory=dict)


def _as_decimal(value: Any) -> Decimal:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, bool):  # guard against bool-as-int surprises
        raise EvalBlocked(BLOCK_INVALID, [f"expected number, got boolean {value}"])
    try:
        return Decimal(str(value))
    except Exception as exc:  # noqa: BLE001 - contained as a block, not a crash
        raise EvalBlocked(BLOCK_INVALID, [f"not a number: {value!r}"]) from exc


def _lookup_rows(param: dict[str, Any], key: str) -> list[dict[str, Any]]:
    values = param["values"]
    if isinstance(values, dict) and key in values:
        rows = values[key]
        if isinstance(rows, list):
            return rows
    raise EvalBlocked(BLOCK_LOOKUP_MISS, [f"no rows for key {key!r} in {param['id']}"])


def _in_band(x: Decimal, lower: Decimal, upper: Decimal | None, boundary: str) -> bool:
    if boundary == "lower_inclusive_upper_exclusive":
        return x >= lower and (upper is None or x < upper)
    return x > lower and (upper is None or x <= upper)


def evaluate(expr: Any, env: Environment, access: AccessLog) -> Any:
    """Evaluate one expression node. Scalars are literals; objects are ops."""
    if not isinstance(expr, dict):
        return expr  # string/number/bool/null literal

    op = expr["op"]

    if op == "ref":
        access.refs.add(expr["name"])
        if expr["name"] not in env.symbols:
            raise EvalBlocked(BLOCK_ABSENT, [expr["name"]])
        val = env.symbols[expr["name"]]
        field = expr.get("field")
        if field is not None:
            # ADR-0067 Decision 2: a `field` selector resolves to
            # finding.value[field] off the currently bound finding, then
            # flows through the existing scalar path. Fail closed — never a
            # silent None/zero — if the bound value is not an object or the
            # named property is absent at runtime.
            if not isinstance(val, dict) or field not in val:
                raise EvalBlocked(BLOCK_INVALID, [f"{expr['name']}.{field}"])
            return val[field]
        fact_type_id = env.symbol_fact_types.get(expr["name"])
        if fact_type_id is not None:
            _validate_categorical_value(
                fact_type_id, str(val), env, env.symbol_fact_versions.get(expr["name"]),
            )
        return val

    if op == "collect":
        name = expr["name"]
        access.collects.add(name)
        rows = env.sources.get(name, [])
        if not rows:
            # Two-layer source-set closure (ADR-0006 decision 8, Track 4 note):
            # an empty set is zero only if the artifact declared a source set
            # AND that set is asserted complete. Otherwise, block.
            source_set = expr.get("source_set")
            if source_set is None or source_set not in env.closed_sets:
                raise EvalBlocked(BLOCK_CLOSURE, [source_set or name])
            access.closure_reads.add(source_set)
            return []
        return [_as_decimal(v) for v in rows]

    if op == "bound_sources":
        # ADR-0074 Decision 2f/2g: read only env.bound_sources; never
        # env.sources; never access.collects. Missing or empty raises
        # DEPENDENCY_ABSENT (not a manufactured zero, not SOURCE_SET_UNCLOSED).
        name = expr["name"]
        access.bound_source_names.add(name)
        rows = env.bound_sources.get(name, [])
        if not rows:
            raise EvalBlocked(BLOCK_ABSENT, [name])
        return [_as_decimal(v) for v in rows]

    if op == "count":
        name = expr["name"]
        access.collects.add(name)
        rows = env.sources.get(name, [])
        source_set = expr["source_set"]
        if source_set not in env.closed_sets:
            raise EvalBlocked(BLOCK_CLOSURE, [source_set])
        access.closure_reads.add(source_set)
        return len(rows)

    if op == "block":
        raise EvalBlocked(expr["code"], [])

    if op == "parameter":
        param_id = expr["parameter_id"]
        access.parameters.add(param_id)
        param = parameter_unversioned(env.parameters, param_id, env.parameter_index)
        if param is None:
            if parameter_version_count(env.parameters, param_id, env.parameter_index) > 1:
                raise EvalBlocked(BLOCK_INVALID, [param_id])
            raise EvalBlocked(BLOCK_ABSENT, [param_id])
        access.parameter_versions.add((param_id, str(param["version"])))
        values = param["values"]
        if "key" in expr:
            key = evaluate(expr["key"], env, access)
            if not isinstance(values, dict) or key not in values:
                raise EvalBlocked(BLOCK_LOOKUP_MISS, [f"{expr['parameter_id']}[{key!r}]"])
            return _as_decimal(values[key])
        return _as_decimal(values)

    if op == "add":
        return sum((_as_decimal(v) for v in _flatten(evaluate_args(expr["args"], env, access))), Decimal(0))

    if op == "subtract":
        return _as_decimal(evaluate(expr["left"], env, access)) - _as_decimal(evaluate(expr["right"], env, access))

    if op == "multiply":
        return _as_decimal(evaluate(expr["left"], env, access)) * _as_decimal(evaluate(expr["right"], env, access))

    if op == "divide":
        return _divide(expr, env, access)

    if op == "max":
        return max(_as_decimal(v) for v in _flatten(evaluate_args(expr["args"], env, access)))

    if op == "compare":
        left = _as_decimal(evaluate(expr["left"], env, access))
        right = _as_decimal(evaluate(expr["right"], env, access))
        return _compare(left, right, expr["cmp"])

    if op == "all":
        return all(bool(evaluate(a, env, access)) for a in expr["args"])

    if op == "any":
        return any(bool(evaluate(a, env, access)) for a in expr["args"])

    if op == "not":
        return not bool(evaluate(expr["value"], env, access))

    if op == "choose":
        branch = "then" if bool(evaluate(expr["when"], env, access)) else "else"
        return evaluate(expr[branch], env, access)

    if op == "round":
        access.operations.add("round")
        return _round(expr, env, access)

    if op == "range_lookup":
        access.operations.add("range_lookup")
        access.tables.add(expr["table_id"])
        return _range_lookup(expr, env, access)

    if op == "bracket_fold":
        access.operations.add("bracket_fold")
        access.tables.add(expr["table_id"])
        return _bracket_fold(expr, env, access)

    if op == "require_closed":
        source_set = expr["source_set"]
        if source_set not in env.closed_sets:
            raise EvalBlocked(BLOCK_CLOSURE, [source_set])
        access.closure_reads.add(source_set)
        return True

    if op == "categorical_compare":
        left_domain, left_val = _eval_categorical_operand(expr["left"], env, access)
        right_domain, right_val = _eval_categorical_operand(expr["right"], env, access)
        if left_domain != right_domain:
            raise EvalBlocked(BLOCK_CATEGORICAL_DOMAIN_MISMATCH, [f"{left_domain} != {right_domain}"])
        return left_val == right_val if expr["cmp"] == "eq" else left_val != right_val

    if op == "category_literal":
        return expr["value"]

    if op == "collect_categorical_all_equal":
        # Additive (Form 1098-E Student Loan Interest Deduction milestone
        # Track 6b repair): the corpus's `collect` op force-coerces every
        # row to Decimal (`_as_decimal`), so it cannot read a categorical
        # "yes"/"no" per-member witness. This op mirrors `collect`'s own
        # raw-row read of ``env.sources`` (never `env.symbols` -- an
        # unkeyed multi-member fact type has no single symbol value to
        # read) but keeps rows as plain strings and tests every row against
        # one expected category, rather than summing. A universal
        # per-statement witness (e.g. "no member answers 'no'") is
        # expressed as one node instead of an unkeyed `ref` that
        # `packages/derivation/marshal.py` would otherwise have to pick a
        # single arbitrary current finding for.
        name = expr["name"]
        access.collects.add(name)
        rows = env.sources.get(name, [])
        if not rows:
            raise EvalBlocked(BLOCK_ABSENT, [name])
        expected_domain, expected_val = _eval_categorical_operand(expr["value"], env, access)
        enum = env.categorical_domains.get(expected_domain)
        for row in rows:
            if enum is not None and row not in enum:
                raise EvalBlocked(BLOCK_INVALID, [row])
        return all(row == expected_val for row in rows)

    if op == "conditional_dependency_set":
        # ADR-0037: the condition is an ordinary evaluated input.  Only a
        # true condition activates members; inactive members are not read and
        # therefore cannot be named or pinned.  Evaluate every active member
        # so one dependency-absence disposition can honestly name the complete
        # declared list, while retaining the ordinary propagation of every
        # non-absence evaluator failure.
        if not bool(evaluate(expr["condition"], env, access)):
            return True
        absent: list[str] = []
        for member in expr["members"]:
            try:
                evaluate(member, env, access)
            except EvalBlocked as exc:
                if exc.category != BLOCK_ABSENT:
                    raise
                absent.extend(exc.missing)
        if absent:
            raise EvalBlocked(BLOCK_ABSENT, absent)
        return True

    if op == "link_coverage":
        return _link_coverage(expr, env, access)

    raise EvalBlocked(BLOCK_INVALID, [f"unknown op survived schema: {op}"])


def _coverage_key_map(row: Any) -> dict[str, str] | None:
    """Name-to-value map of one source's structured keys, or None.

    Tuple order is not the comparison. ``fact_id`` is not read.
    """
    keys = getattr(row, "keys", None)
    if keys is None:
        return None
    return {str(name): str(value) for name, value in keys}


def _coverage_decimal(value: Any) -> Decimal | None:
    """A numeric reduction, or None. Booleans are not numbers."""
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, Decimal):
        return value
    if isinstance(value, int | float):
        return Decimal(str(value))
    if isinstance(value, str):
        try:
            return Decimal(value)
        except Exception:
            return None
    return None


def _coverage_rows(slot: Any) -> list[tuple[Any, dict[str, str]]]:
    if slot == KEYS_UNAVAILABLE or not isinstance(slot, list):
        raise EvalBlocked(BLOCK_INVALID, [LINK_COVERAGE_KEYS_UNAVAILABLE])
    rows: list[tuple[Any, dict[str, str]]] = []
    for row in slot:
        key_map = _coverage_key_map(row)
        if key_map is None:
            raise EvalBlocked(BLOCK_INVALID, [LINK_COVERAGE_KEYS_UNAVAILABLE])
        rows.append((row, key_map))
    return rows


def _empty_coverage_parameter(expr: dict[str, Any], env: Environment, access: AccessLog) -> Decimal:
    parameter = expr["empty"]["parameter"]
    param_id = str(parameter["id"])
    param_version = str(parameter["version"])
    param = parameter_exact(env.parameters, param_id, param_version, env.parameter_index)
    if param is None:
        if parameter_version_count(env.parameters, param_id, env.parameter_index) > 0:
            raise EvalBlocked(BLOCK_INVALID, [param_id])
        raise EvalBlocked(BLOCK_ABSENT, [param_id])
    access.parameters.add(param_id)
    access.parameter_versions.add((param_id, str(param["version"])))
    return _as_decimal(param["values"])


def _link_coverage(expr: dict[str, Any], env: Environment, access: AccessLog) -> Decimal:
    """One statement's reduction total, or a contained block.

    Fail-closed checks run in contract table order, before the three
    outcomes. The match is key-map equality. Rows are not dropped, not
    treated as zero, and not paired by ``fact_id``.
    """
    links_name = expr["links"]
    reductions_name = expr["reductions"]
    keyed = env.keyed_sources
    if links_name not in keyed or reductions_name not in keyed:
        raise EvalBlocked(BLOCK_INVALID, [LINK_COVERAGE_SCOPE_UNBOUND])
    links_slot = keyed[links_name]
    reductions_slot = keyed[reductions_name]
    if links_slot == KEYS_UNAVAILABLE or reductions_slot == KEYS_UNAVAILABLE:
        raise EvalBlocked(BLOCK_INVALID, [LINK_COVERAGE_KEYS_UNAVAILABLE])

    links = _coverage_rows(links_slot)
    reductions = _coverage_rows(reductions_slot)
    link_maps = [key_map for _row, key_map in links]

    orphan_ids = [
        str(row.finding_id)
        for row, key_map in reductions
        if key_map not in link_maps
    ]
    if orphan_ids:
        raise EvalBlocked(BLOCK_INVALID, sorted(orphan_ids))

    grouped: dict[frozenset[tuple[str, str]], list[str]] = {}
    for row, key_map in links:
        grouped.setdefault(frozenset(key_map.items()), []).append(str(row.finding_id))
    duplicate_ids = [
        finding_id
        for finding_ids in grouped.values()
        if len(finding_ids) > 1
        for finding_id in finding_ids
    ]
    if duplicate_ids:
        raise EvalBlocked(BLOCK_INVALID, sorted(duplicate_ids))

    multi_link_ids = [
        str(row.finding_id)
        for row, key_map in links
        if sum(1 for _reduction, reduction_map in reductions if reduction_map == key_map) >= 2
    ]
    if multi_link_ids:
        raise EvalBlocked(BLOCK_INVALID, sorted(multi_link_ids))

    uncovered: list[str] = []
    non_numeric: list[str] = []
    total = Decimal(0)
    covered_ids: list[str] = []
    for row, key_map in links:
        matches = [reduction for reduction, reduction_map in reductions if reduction_map == key_map]
        if not matches:
            uncovered.append(str(row.finding_id))
            continue
        number = _coverage_decimal(matches[0].value)
        if number is None:
            non_numeric.append(str(row.finding_id))
            continue
        total += number
        covered_ids.append(str(row.finding_id))
        covered_ids.append(str(matches[0].finding_id))
    if non_numeric:
        raise EvalBlocked(BLOCK_INVALID, sorted(non_numeric))
    if not links:
        return _empty_coverage_parameter(expr, env, access)
    if uncovered:
        access.link_coverage_findings.update(uncovered)
        raise EvalBlocked(BLOCK_INVALID, sorted(uncovered))
    access.link_coverage_findings.update(covered_ids)
    return total


def evaluate_args(args: list[Any], env: Environment, access: AccessLog) -> list[Any]:
    return [evaluate(a, env, access) for a in args]


def _flatten(values: list[Any]) -> list[Any]:
    """collect yields a list of Decimals; add/max fold over a flat operand set."""
    flat: list[Any] = []
    for v in values:
        if isinstance(v, list):
            flat.extend(v)
        else:
            flat.append(v)
    return flat


def _compare(left: Decimal, right: Decimal, cmp: str) -> bool:
    return {
        "eq": left == right,
        "ne": left != right,
        "gt": left > right,
        "gte": left >= right,
        "lt": left < right,
        "lte": left <= right,
    }[cmp]


def _round(expr: dict[str, Any], env: Environment, access: AccessLog) -> Decimal:
    canon = env.canon["round"]["spec"]
    mode = evaluate(expr["mode"], env, access)
    if mode not in _ROUND_MODES or mode not in canon["modes"]:
        raise EvalBlocked(BLOCK_INVALID, [f"unknown rounding mode: {mode!r}"])
    value = _as_decimal(evaluate(expr["value"], env, access))
    unit = Decimal(canon["unit"])
    return (value / unit).quantize(Decimal(1), rounding=_ROUND_MODES[mode]) * unit


def _divide(expr: dict[str, Any], env: Environment, access: AccessLog) -> Decimal:
    """left / right, floored to at least `min_decimal_places` decimal digits.

    This is a precision floor on the ratio's own decimal representation,
    evaluated once immediately after division, categorically distinct from
    the `round` op's whole-dollar `rounding.convention` unit (T0-4/T0-9). A
    zero divisor blocks rather than raising ZeroDivisionError or producing
    Infinity, so the op is safe for any future consumer even though this
    milestone's divisor is always a fixed nonzero parameter.
    """
    left = _as_decimal(evaluate(expr["left"], env, access))
    right = _as_decimal(evaluate(expr["right"], env, access))
    if right == 0:
        raise EvalBlocked(BLOCK_INVALID, ["division by zero"])
    mode = expr["rounding"]
    if mode not in _ROUND_MODES:
        raise EvalBlocked(BLOCK_INVALID, [f"unknown rounding mode: {mode!r}"])
    min_decimal_places = expr["min_decimal_places"]
    quantum = Decimal(1).scaleb(-min_decimal_places)
    return (left / right).quantize(quantum, rounding=_ROUND_MODES[mode])


def _range_lookup(expr: dict[str, Any], env: Environment, access: AccessLog) -> Decimal:
    canon = env.canon["range_lookup"]["spec"]
    param = parameter_unversioned(env.parameters, expr["table_id"], env.parameter_index)
    if param is None:
        if parameter_version_count(env.parameters, expr["table_id"], env.parameter_index) > 1:
            raise EvalBlocked(BLOCK_INVALID, [expr["table_id"]])
        raise EvalBlocked(BLOCK_ABSENT, [expr["table_id"]])
    access.parameter_versions.add((expr["table_id"], str(param["version"])))
    key = evaluate(expr["key"], env, access)
    value = _as_decimal(evaluate(expr["value"], env, access))
    for row in _lookup_rows(param, str(key)):
        lower = Decimal(row["lower"])
        upper = None if row.get("upper") is None else Decimal(row["upper"])
        if _in_band(value, lower, upper, canon["boundary"]):
            return _as_decimal(row["value"])
    if canon["on_miss"] == "zero":
        return Decimal(0)
    raise EvalBlocked(BLOCK_LOOKUP_MISS, [f"{expr['table_id']}[{key}] @ {value}"])


def _bracket_fold(expr: dict[str, Any], env: Environment, access: AccessLog) -> Decimal:
    canon = env.canon["bracket_fold"]["spec"]
    param = parameter_unversioned(env.parameters, expr["table_id"], env.parameter_index)
    if param is None:
        if parameter_version_count(env.parameters, expr["table_id"], env.parameter_index) > 1:
            raise EvalBlocked(BLOCK_INVALID, [expr["table_id"]])
        raise EvalBlocked(BLOCK_ABSENT, [expr["table_id"]])
    access.parameter_versions.add((expr["table_id"], str(param["version"])))
    key = evaluate(expr["key"], env, access)
    value = _as_decimal(evaluate(expr["value"], env, access))
    total = Decimal(0)
    for row in _lookup_rows(param, str(key)):
        lower = Decimal(row["lower"])
        upper = None if row.get("upper") is None else Decimal(row["upper"])
        if value <= lower:
            continue
        top = value if upper is None else min(value, upper)
        total += (top - lower) * Decimal(row["rate"])
    return total


def _domain_versions(env: Environment, fact_type_id: str) -> list[str]:
    prefix = fact_type_id + _CATEGORICAL_VERSION_SEP
    return [key[len(prefix):] for key in env.categorical_domains if key.startswith(prefix)]


def _resolve_categorical_domain(
    env: Environment, fact_type_id: str, version: str | None,
) -> tuple[str, list[str]] | None:
    """The exact domain, or None when this id is not categorical.

    A named version that is absent while a sibling version is present blocks.
    Several versions and no named version block. One version keeps the bare
    id as its identity so a comparison against today's id-keyed domain still
    agrees. Two versions are different domains: their identities differ.
    """
    present = _domain_versions(env, fact_type_id)
    if version is not None:
        exact_key = categorical_domain_key(fact_type_id, version)
        enum = env.categorical_domains.get(exact_key)
        if enum is not None:
            identity = exact_key if len(present) > 1 else fact_type_id
            return identity, enum
        if present:
            raise EvalBlocked(
                BLOCK_CATEGORICAL_DOMAIN_MISMATCH, [f"{fact_type_id}@{version}"],
            )
        legacy = env.categorical_domains.get(fact_type_id)
        if legacy is not None:
            return fact_type_id, legacy
        return None
    if len(present) > 1:
        raise EvalBlocked(BLOCK_CATEGORICAL_DOMAIN_MISMATCH, [fact_type_id])
    if len(present) == 1:
        only = present[0]
        return fact_type_id, env.categorical_domains[categorical_domain_key(fact_type_id, only)]
    legacy = env.categorical_domains.get(fact_type_id)
    if legacy is not None:
        return fact_type_id, legacy
    return None


def _eval_categorical_operand(expr: Any, env: Environment, access: AccessLog) -> tuple[str, str]:
    if not isinstance(expr, dict):
        raise EvalBlocked(BLOCK_CATEGORICAL_DOMAIN_MISMATCH, [f"not a categorical expression: {expr}"])
    op = expr.get("op")
    if op == "category_literal":
        fact_type = expr["fact_type"]
        if isinstance(fact_type, dict):
            fact_type_id = str(fact_type["id"])
            raw_version = fact_type.get("version")
            version = str(raw_version) if isinstance(raw_version, str) else None
        else:
            fact_type_id = str(fact_type)
            version = None
        val = str(expr["value"])
        return _validate_categorical_value(fact_type_id, val, env, version), val
    if op == "ref":
        name = expr["name"]
        val = evaluate(expr, env, access)
        fact_type_id = str(env.symbol_fact_types.get(name, name))
        version = env.symbol_fact_versions.get(name)
        return _validate_categorical_value(fact_type_id, str(val), env, version), str(val)
    raise EvalBlocked(BLOCK_CATEGORICAL_DOMAIN_MISMATCH, [f"not a categorical expression: {expr}"])


def _validate_categorical_value(
    fact_type_id: str, val: str, env: Environment, version: str | None = None,
) -> str:
    """Check ``val`` against the exact domain. Return the domain identity.

    The identity is what ``categorical_compare`` treats as the domain. An
    unknown non-categorical id returns ``fact_type_id`` and checks nothing,
    matching a value that was never declared categorical.
    """
    resolved = _resolve_categorical_domain(env, fact_type_id, version)
    if resolved is None:
        return fact_type_id
    identity, enum = resolved
    if val not in enum:
        raise EvalBlocked(BLOCK_INVALID, [val])
    return identity
