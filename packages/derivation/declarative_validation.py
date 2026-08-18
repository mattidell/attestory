from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, NamedTuple

TERM_OPS = frozenset({"field", "literal", "add", "subtract", "floor_zero"})
PREDICATE_OPS = frozenset({
    "field_present", "field_absent", "field_equals", "field_not_equals",
    "compare", "all", "any",
})
COMPARISONS = {
    "gt": lambda a, b: a > b,
    "ge": lambda a, b: a >= b,
    "lt": lambda a, b: a < b,
    "le": lambda a, b: a <= b,
    "eq": lambda a, b: a == b,
    "ne": lambda a, b: a != b,
}

MAX_PREDICATE_DEPTH = 6

_ABSENT = object()

class GrammarError(Exception):
    """A term or predicate is outside the closed grammar."""

class MemberConstraintTooDeep(Exception):
    """A member constraint exceeded the maximum depth."""

class Violation(NamedTuple):
    constraint_id: str
    block_code: str
    meaning: str

class Evaluator:
    def _dec(self, value: Any) -> Decimal:
        if isinstance(value, Decimal):
            return value
        if isinstance(value, bool):
            raise GrammarError(f"boolean is not a numeric term value: {value!r}")
        if isinstance(value, (int, str)):
            return Decimal(str(value))
        if isinstance(value, float):
            return Decimal(str(value))
        raise GrammarError(f"not a numeric term value: {value!r}")

    def evaluate_term(self, term: Mapping[str, Any], member: Mapping[str, Any], depth: int = 1) -> Decimal:
        if depth > MAX_PREDICATE_DEPTH:
            raise MemberConstraintTooDeep("Term depth exceeded")
        op = term.get("op")
        if op not in TERM_OPS:
            raise GrammarError(f"unknown term op {op!r}; the grammar is closed")
        if op == "literal":
            return self._dec(term["arg"])
        if op == "field":
            value = member.get(term["field"], _ABSENT)
            if value is _ABSENT:
                if "default" not in term:
                    raise GrammarError(
                        f"field {term['field']!r} is absent and the term declares no default"
                    )
                return self._dec(term["default"])
            return self._dec(value)
        if op == "add":
            return self.evaluate_term(term["left"], member, depth + 1) + self.evaluate_term(term["right"], member, depth + 1)
        if op == "subtract":
            return self.evaluate_term(term["left"], member, depth + 1) - self.evaluate_term(term["right"], member, depth + 1)
        if op == "floor_zero":
            return max(self.evaluate_term(term["value"], member, depth + 1), Decimal(0))
        raise GrammarError(f"unhandled term op {op!r}")

    def evaluate_predicate(self, pred: Mapping[str, Any], member: Mapping[str, Any], depth: int = 1) -> bool:
        if depth > MAX_PREDICATE_DEPTH:
            raise MemberConstraintTooDeep("Predicate depth exceeded")
        op = pred.get("op")
        if op not in PREDICATE_OPS:
            raise GrammarError(f"unknown predicate op {op!r}; the grammar is closed")
        if op == "field_present":
            return pred["field"] in member
        if op == "field_absent":
            return pred["field"] not in member
        if op == "field_equals":
            return bool(member.get(pred["field"], _ABSENT) == pred["arg"])
        if op == "field_not_equals":
            value = member.get(pred["field"], _ABSENT)
            return bool(value is not _ABSENT and value != pred["arg"])
        if op == "compare":
            comparison = COMPARISONS.get(pred["comparison"])
            if comparison is None:
                raise GrammarError(f"unknown comparison {pred['comparison']!r}")
            return bool(comparison(
                self.evaluate_term(pred["left"], member, depth + 1), 
                self.evaluate_term(pred["right"], member, depth + 1)
            ))
        if op == "all":
            return all(self.evaluate_predicate(arg, member, depth + 1) for arg in pred["args"])
        if op == "any":
            return any(self.evaluate_predicate(arg, member, depth + 1) for arg in pred["args"])
        raise GrammarError(f"unhandled predicate op {op!r}")

    def evaluate_member(self, constraints: list[Mapping[str, Any]], member: Mapping[str, Any]) -> list[Violation]:
        violations: list[Violation] = []
        for constraint in constraints:
            if self.evaluate_predicate(constraint["violated_when"], member):
                violations.append(Violation(
                    constraint["id"], constraint["block_code"], constraint["meaning"]
                ))
        return violations


class IdentityBindingError(ValueError):
    """A declared binding cannot be read from the current member."""

def extract_bound_keys(fact_id: str) -> dict[str, str]:
    """Read the ADR-0011 `key=value` suffix. The type prefix is discarded."""
    _, _, suffix = fact_id.partition("|")
    pairs: dict[str, str] = {}
    if not suffix:
        return pairs
    for part in suffix.split(","):
        if "=" not in part:
            continue
        name, value = part.split("=", 1)
        pairs[name] = value
    return pairs

def extract_component(
    *,
    fact_id: str,
    member_value: Mapping[str, Any] | None,
    component: Mapping[str, Any],
) -> str:
    if "fact_id_bound_key" in component:
        key = component["fact_id_bound_key"]
        pairs = extract_bound_keys(fact_id)
        if key not in pairs:
            raise IdentityBindingError(
                f"fact-id bound key {key!r} absent from {fact_id!r}"
            )
        return pairs[key]
    if "member_field" in component:
        path = component["member_field"]
        if member_value is None or path not in member_value:
            raise IdentityBindingError(
                f"member field {path!r} absent from current member value"
            )
        return str(member_value[path])
    raise IdentityBindingError(f"unsupported identity binding component: {list(component.keys())}")

def identity_tuple(
    *,
    fact_id: str,
    member_value: Mapping[str, Any] | None,
    components: list[Mapping[str, Any]],
) -> tuple[str, ...]:
    return tuple(
        extract_component(fact_id=fact_id, member_value=member_value, component=component)
        for component in components
    )
def evaluate_constraints(constraints: list[Mapping[str, Any]], members: list[Mapping[str, Any]]) -> list[dict[str, str]]:
    evaluator = Evaluator()
    issues = []
    for member in members:
        violations = evaluator.evaluate_member(constraints, member)
        for v in violations:
            issues.append({"constraint_id": v.constraint_id, "block_code": v.block_code, "meaning": v.meaning})
    return issues
