"""Selectable line explanations on core v78 are not the v77 generic sentences.

The banned words, the internal-id check, the two-sentence limit, and the
double-negative pattern apply to explains this track replaced. Decision 2
keeps specific v77 sentences, including ones that still say "derived
finding", and it keeps a generic sentence the bound rule cannot select.
Those bytes are not this track's text.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

CONTENT = Path(__file__).resolve().parents[1] / "packages" / "content" / "tax" / "2025"
DISPOSITIONS = (
    "published_value",
    "computed_zero",
    "closure_backed_zero",
    "blocked",
    "guard_inapplicable",
)
# The v77 generic sentences. The test computes the same set from the v77
# package and checks the count, so a new generic cannot hide in the corpus.
STOCK = frozenset({
    "blocked",
    "guard false",
    "closure zero",
    "computed zero",
    "Blocked.",
    "Inapplicable.",
    "Computed zero.",
    "Closure-backed zero.",
    "Not used.",
    "Not evaluated.",
    "This field does not publish a value.",
    "Current derived finding publishes this line.",
    "A current derived finding publishes this line.",
    "A current derived finding publishes this nonzero amount.",
    "A current derived finding publishes a numeric zero.",
    "No published value exists because required state is absent.",
    "No value exists because the declared rule guard is false.",
    "No value exists because the rule guard is false.",
    "A current derived finding publishes a computed zero.",
    "A current derived finding publishes a computed zero under complete authority.",
    "A current derived finding publishes a computed zero from present inputs that net to zero.",
    "A current derived finding publishes zero because the supporting source family is attested closed-empty under complete authority.",
    "A current derived finding publishes a zero from closure-backed inputs with no recorded members.",
    "A current derived finding publishes zero through honest closed-empty or zero-credit authority on the direct-election path.",
    "No value is published because a completeness or guard condition is not satisfied.",
    "No value is published because a scope, election, threshold, or creditability component is not satisfied for the bounded class.",
})
ROUTE_ONLY = re.compile(r"^No line \S+ value exists for this route\.?$")
BARE_PUBLISHED = re.compile(r"^published .+$", re.IGNORECASE)
BARE_PUBLISHED_KEEP = re.compile(r"because|equals|always|zero|closed", re.IGNORECASE)
DOUBLE_NEGATIVE = "not say that you have no"
BANNED = (
    "derived finding",
    "closure",
    "honest",
    "guard",
    "route",
    "calculation comes to zero",
)
ID_LEAK = re.compile(r"\b(?:tax\.us|demo)\.[A-Za-z0-9_.|-]+")
STAYED = (
    "tax.us.2025.form.f1098.residence-interest-unresolved",
    "tax.us.2025.form.f1099k.unresolved.form-field",
    "tax.us.2025.form1040.line-3a",
    "tax.us.2025.form1040.line-3b",
    "tax.us.2025.schedule-d.line-8a",
)


def _load(name: str) -> dict[str, Any]:
    body = json.loads((CONTENT / name).read_text(encoding="utf-8"))
    assert isinstance(body, dict)
    return body


def _index() -> dict[tuple[str, str], dict[str, Any]]:
    found: dict[tuple[str, str], dict[str, Any]] = {}
    for path in CONTENT.glob("*.json"):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(body, dict) and isinstance(body.get("id"), str) and isinstance(body.get("version"), str):
            found[(body["id"], body["version"])] = body
    return found


def _classify(text: str, shared: int) -> str:
    stripped = text.strip()
    if stripped in STOCK or shared > 1:
        return "generic"
    if BARE_PUBLISHED.match(stripped) and not BARE_PUBLISHED_KEEP.search(stripped):
        return "generic"
    if ROUTE_ONLY.match(stripped):
        return "generic"
    return "specific"


def _generics(v77: dict[str, Any], index: dict[tuple[str, str], dict[str, Any]]) -> frozenset[str]:
    fields = [index[(member["id"], member["version"])] for member in v77["members"] if member["role"] == "form-field"]
    owners: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for field in fields:
        for row in field["dispositions"].values():
            owners[row["explain"]].add((field["form"]["form_id"], field["line"]))
    found = {
        row["explain"]
        for field in fields
        for row in field["dispositions"].values()
        if _classify(row["explain"], len(owners[row["explain"]])) == "generic"
    }
    return frozenset(found)


def _rules(v78: dict[str, Any], index: dict[tuple[str, str], dict[str, Any]]) -> dict[str, dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}
    for member in v78["members"]:
        body = index[(member["id"], member["version"])]
        if isinstance(body.get("publishes"), str) and str(body.get("schema", "")).startswith("rule-artifact"):
            found[body["publishes"]] = body
    return found


def _when_false(node: object) -> bool:
    """True when some return can make this guard false without blocking.

    ``require_closed`` and ``conditional_dependency_set`` are true or blocked,
    never false. ``any`` is false only when every argument can be false,
    because a blocked argument raises before a later false one is read.
    """
    if node is True or node is None:
        return False
    if node is False:
        return True
    if not isinstance(node, dict):
        return False
    op = node.get("op")
    if op in {"require_closed", "conditional_dependency_set"}:
        return False
    if op == "all":
        return any(_when_false(arg) for arg in node.get("args") or [])
    if op == "any":
        args = node.get("args") or []
        return bool(args) and all(_when_false(arg) for arg in args)
    if op == "choose":
        return _when_false(node.get("then")) or _when_false(node.get("else"))
    if op in {"compare", "categorical_compare", "not"}:
        return True
    return False


def _numeric(node: object) -> bool:
    if isinstance(node, bool) or node is None:
        return False
    if isinstance(node, (int, float)):
        return True
    if isinstance(node, dict):
        return node.get("op") not in {"block", "false"}
    return False


def _publishing(rule: dict[str, Any]) -> list[dict[str, Any]]:
    if "selection" not in rule:
        return [rule] if _numeric(rule.get("value")) else []
    paths = list(rule["selection"].get("paths") or [])
    default = rule["selection"].get("default")
    if isinstance(default, dict):
        paths.append(default)
    return [path for path in paths if _numeric(path.get("value"))]


def _closure_blocked(rule: dict[str, Any], rules: dict[str, dict[str, Any]], seen: frozenset[str] = frozenset()) -> bool:
    """A zero cannot be closure-backed when some leaf is always a real answer.

    A categorical or filing-status pin is such a leaf. A pin that is another
    rule's result is walked, and one always-real leaf anywhere in that walk
    is enough.
    """
    rule_id = str(rule.get("id"))
    if rule_id in seen:
        return False
    nodes = _publishing(rule)
    if not nodes:
        return True

    def node_blocked(node: dict[str, Any]) -> bool:
        pins = rule.get("pins") or [] if node is rule else node.get("pins") or []
        for pin in pins:
            if pin.get("role") not in {"input", "choice"}:
                continue
            pin_id = pin.get("id")
            if pin_id not in rules:
                return True
            child = rules.get(pin_id)
            if child is not None and _closure_blocked(child, rules, seen | {rule_id}):
                return True
        return False

    if "selection" in rule:
        return all(node_blocked(node) for node in nodes)
    return node_blocked(rule)


def _selects(rule: dict[str, Any], code: str, rules: dict[str, dict[str, Any]]) -> bool:
    if code == "guard_inapplicable":
        return _when_false(rule.get("when"))
    if code == "blocked":
        return True
    if not _publishing(rule):
        return False
    if code == "published_value":
        return rule.get("value") not in (0, 0.0)
    if code == "computed_zero":
        return True
    if code == "closure_backed_zero":
        return not _closure_blocked(rule, rules)
    return False


def test_v78_selectable_explains_are_not_the_v77_generics() -> None:
    index = _index()
    v77 = _load("package.core-calculations.v77.json")
    v78 = _load("package.core-calculations.v78.json")
    generics = _generics(v77, index)
    assert len(generics) == 37
    rules = _rules(v78, index)
    pin77 = {member["id"]: member["version"] for member in v77["members"] if member["role"] == "form-field"}
    pin78 = {member["id"]: member["version"] for member in v78["members"] if member["role"] == "form-field"}
    for citizen_id in STAYED:
        assert pin78[citizen_id] == pin77[citizen_id]
    failures: list[str] = []
    for citizen_id, version in pin78.items():
        field = index[(citizen_id, version)]
        previous = index[(citizen_id, pin77[citizen_id])]
        rule = rules[field["binds_symbol"]]
        for code in DISPOSITIONS:
            text = field["dispositions"][code]["explain"]
            if _selects(rule, code, rules) and text in generics:
                failures.append(f"{citizen_id} {code} still generic")
            if text == previous["dispositions"][code]["explain"]:
                continue
            lowered = text.lower()
            if any(word in lowered for word in BANNED) or ID_LEAK.search(text) or text in generics:
                failures.append(f"{citizen_id} {code} replaced text is banned or generic")
            if not text.endswith(".") or text.count(".") > 2:
                failures.append(f"{citizen_id} {code} is more than two sentences")
            if DOUBLE_NEGATIVE in lowered:
                failures.append(f"{citizen_id} {code} uses a double negative")
    assert failures == []
