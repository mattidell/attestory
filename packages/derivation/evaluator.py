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
from typing import Any

# Blocking categories (ADR-0006 decision 8). The vocabulary distinguishes a
# dependency that is absent from one that is present but invalid, and an
# unclosed source set from either.
BLOCK_ABSENT = "DEPENDENCY_ABSENT"
BLOCK_INVALID = "DEPENDENCY_INVALID"
BLOCK_CLOSURE = "SOURCE_SET_UNCLOSED"
BLOCK_LOOKUP_MISS = "LOOKUP_MISS"
BLOCK_CATEGORICAL_DOMAIN_MISMATCH = "CATEGORICAL_DOMAIN_MISMATCH"

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


@dataclass
class AccessLog:
    """What an evaluation actually read, for truthful pinning."""

    refs: set[str] = field(default_factory=set)
    collects: set[str] = field(default_factory=set)
    parameters: set[str] = field(default_factory=set)
    tables: set[str] = field(default_factory=set)
    operations: set[str] = field(default_factory=set)
    # Families whose closure authority an empty collect actually stood on;
    # a closure-backed zero pins these, present-source aggregation never
    # populates it (ADR-0014 decision 5).
    closure_reads: set[str] = field(default_factory=set)


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
        fact_type_id = env.symbol_fact_types.get(expr["name"])
        if fact_type_id is not None:
            _validate_categorical_value(fact_type_id, str(val), env)
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

    if op == "parameter":
        access.parameters.add(expr["parameter_id"])
        param = env.parameters.get(expr["parameter_id"])
        if param is None:
            raise EvalBlocked(BLOCK_ABSENT, [expr["parameter_id"]])
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

    raise EvalBlocked(BLOCK_INVALID, [f"unknown op survived schema: {op}"])


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


def _range_lookup(expr: dict[str, Any], env: Environment, access: AccessLog) -> Decimal:
    canon = env.canon["range_lookup"]["spec"]
    param = env.parameters.get(expr["table_id"])
    if param is None:
        raise EvalBlocked(BLOCK_ABSENT, [expr["table_id"]])
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
    param = env.parameters.get(expr["table_id"])
    if param is None:
        raise EvalBlocked(BLOCK_ABSENT, [expr["table_id"]])
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


def _eval_categorical_operand(expr: Any, env: Environment, access: AccessLog) -> tuple[str, str]:
    if not isinstance(expr, dict):
        raise EvalBlocked(BLOCK_CATEGORICAL_DOMAIN_MISMATCH, [f"not a categorical expression: {expr}"])
    op = expr.get("op")
    if op == "category_literal":
        fact_type = expr["fact_type"]
        fact_type_id = fact_type["id"] if isinstance(fact_type, dict) else fact_type
        val = expr["value"]
        _validate_categorical_value(fact_type_id, val, env)
        return fact_type_id, val
    if op == "ref":
        name = expr["name"]
        val = evaluate(expr, env, access)
        fact_type_id = str(env.symbol_fact_types.get(name, name))
        _validate_categorical_value(fact_type_id, str(val), env)
        return fact_type_id, str(val)
    raise EvalBlocked(BLOCK_CATEGORICAL_DOMAIN_MISMATCH, [f"not a categorical expression: {expr}"])


def _validate_categorical_value(fact_type_id: str, val: str, env: Environment) -> None:
    valid_values = env.categorical_domains.get(fact_type_id)
    if valid_values is not None and val not in valid_values:
        raise EvalBlocked(BLOCK_INVALID, [val])
