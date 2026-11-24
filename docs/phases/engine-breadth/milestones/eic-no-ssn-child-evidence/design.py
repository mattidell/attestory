"""Scratch successors on published core v101 for a qualifying child without a valid SSN.

A child who meets relationship, age, residency and joint return is a qualifying
child for the separated-spouse rule even when ``eic.child.ssn-met`` is 0. The
amount column stays the count of qualifying children who have a valid SSN.
Nothing here is a new operation. The new symbols are derived, like
``eic.child.counts``, and are pinned as assertion version v1.

- ``rule.eic-child.qualifies`` v1: ``rule.eic-child.counts`` v2 without the SSN test.
- ``rule.eic-qualifying-child-present`` v1: ``rule.eic-qualifying-child-count`` v1
  collecting ``eic.child.qualifies``.
- ``rule.eic-status-class`` v2 to v3: head of household is class 0 when a
  qualifying child is present, including one who has no valid SSN.
- ``rule.eic-early-stop`` v2 to v3: the column-0 class-0 stop also requires
  that no qualifying child is present.
- ``rule.eic-questions-required`` v2 to v3: questions are required when a
  qualifying child is present.
- ``rule.eic-answer.separated-spouse`` v1 to v2: the answer is read when a
  qualifying child is present and the column is 0.
- ``rule.eic-answer.not-married`` v1 to v2: Step 4 question 1 is not asked
  when a qualifying child is present.
- ``rule.eic-answer.age-25-under-65`` v3 to v4 and
  ``rule.eic-answer.main-home-in-us`` v3 to v4: those Step 4 questions are
  not asked when a qualifying child is present and the status class is 0
  (married filing separately, or head of household once v3 classifies it).
  Single, qualifying surviving spouse and married filing jointly keep the
  v101 question.

``rule.eic-gate-result`` v3 and ``rule.eic-answer.not-claimable-as-dependent``
v3 stay. The gate already stops on separated-spouse 0 and on not-married 0.
Not-claimable already publishes 1 when the status class is not 1.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

P = "tax.us.2025."
COUNT = P + "eic.column-count"
PRESENT = P + "eic.qualifying-child-present"
STATUS_CLASS = P + "eic.status-class"
COUNTS = P + "eic.child.counts"
QUALIFIES = P + "eic.child.qualifies"
SSN_MET = P + "eic.child.ssn-met"

QUALIFIES_RULE = P + "rule.eic-child.qualifies"
PRESENT_RULE = P + "rule.eic-qualifying-child-present"
CLASS_RULE = P + "rule.eic-status-class"
EARLY_RULE = P + "rule.eic-early-stop"
QUESTIONS_RULE = P + "rule.eic-questions-required"
SEP_RULE = P + "rule.eic-answer.separated-spouse"
NOT_MARRIED_RULE = P + "rule.eic-answer.not-married"
AGE_RULE = P + "rule.eic-answer.age-25-under-65"
HOME_RULE = P + "rule.eic-answer.main-home-in-us"

QUALIFIES_FILE = "rule.eic-child.qualifies.json"
PRESENT_FILE = "rule.eic-qualifying-child-present.json"
CLASS_FILE = "rule.eic-status-class.v3.json"
EARLY_FILE = "rule.eic-early-stop.v3.json"
QUESTIONS_FILE = "rule.eic-questions-required.v3.json"
SEP_FILE = "rule.eic-answer.separated-spouse.v2.json"
NOT_MARRIED_FILE = "rule.eic-answer.not-married.v2.json"
AGE_FILE = "rule.eic-answer.age-25-under-65.v4.json"
HOME_FILE = "rule.eic-answer.main-home-in-us.v4.json"

REPLACED = {
    CLASS_RULE: "v2",
    EARLY_RULE: "v2",
    QUESTIONS_RULE: "v2",
    SEP_RULE: "v1",
    NOT_MARRIED_RULE: "v1",
    AGE_RULE: "v3",
    HOME_RULE: "v3",
}
SOURCES = {
    CLASS_FILE: "rule.eic-status-class.v2.json",
    EARLY_FILE: "rule.eic-early-stop.v2.json",
    QUESTIONS_FILE: "rule.eic-questions-required.v2.json",
    SEP_FILE: "rule.eic-answer.separated-spouse.json",
    NOT_MARRIED_FILE: "rule.eic-answer.not-married.json",
    AGE_FILE: "rule.eic-answer.age-25-under-65.v3.json",
    HOME_FILE: "rule.eic-answer.main-home-in-us.v3.json",
    QUALIFIES_FILE: "rule.eic-child.counts.v2.json",
    PRESENT_FILE: "rule.eic-qualifying-child-count.json",
}


def _pin(fact: str) -> dict[str, Any]:
    return {"id": fact, "origin": "assertion", "role": "input", "version": "v1"}


def _ref_name(node: dict[str, Any]) -> str | None:
    left = node.get("left")
    if isinstance(left, dict):
        return left.get("name")
    return None


def _depend(out: dict[str, Any], *names: str) -> None:
    """Append derived inputs the way the published rule already lists its requires."""
    for name in names:
        if name not in out["requires"]:
            out["requires"].append(name)
        if not any(pin.get("id") == name for pin in out["pins"]):
            out["pins"].append(_pin(name))
        missing = out["blocked"]["missing"]
        if missing and name not in missing:
            required = set(out["requires"])
            at = next((i for i, item in enumerate(missing) if item not in required), len(missing))
            missing.insert(at, name)


def _eq(name: str, right: int) -> dict[str, Any]:
    return {"op": "compare", "cmp": "eq", "left": {"op": "ref", "name": name}, "right": right}


def _gt(name: str, right: int) -> dict[str, Any]:
    return {"op": "compare", "cmp": "gt", "left": {"op": "ref", "name": name}, "right": right}


def qualifies_rule(counts: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(counts)
    out["id"] = QUALIFIES_RULE
    out["version"] = "v1"
    out["publishes"] = QUALIFIES
    out["requires"] = [name for name in out["requires"] if name != SSN_MET]
    args = out["value"]["when"]["args"]
    kept = [arg for arg in args if _ref_name(arg) != SSN_MET]
    assert len(kept) == len(args) - 1 and len(kept) == 5
    out["value"]["when"]["args"] = kept
    assert out["value"]["when"]["op"] == "all" and out["value"]["then"] == 1 and out["value"]["else"] == 0
    out["notes"] = (
        "1 when relationship, age, residency, joint return and the tie-breaker are met, "
        "whether or not the child has a valid SSN. The amount column still uses "
        "tax.us.2025.rule.eic-child.counts, which requires the SSN test."
    )
    return out


def _swap_symbol(node: Any) -> int:
    found = 0
    if isinstance(node, dict):
        if node.get("symbol") == COUNTS:
            node["symbol"] = QUALIFIES
            found += 1
        if node.get("op") == "collect" and node.get("name") == COUNTS:
            node["name"] = QUALIFIES
            found += 1
        for value in node.values():
            found += _swap_symbol(value)
    elif isinstance(node, list):
        for value in node:
            found += _swap_symbol(value)
    return found


def present_rule(count_rule: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(count_rule)
    out["id"] = PRESENT_RULE
    out["version"] = "v1"
    out["publishes"] = PRESENT
    swapped = _swap_symbol(out["selection"])
    assert swapped == 2
    assert COUNTS not in json.dumps(out)
    out["notes"] = (
        "How many qualifying children are present, including a child with no valid SSN. "
        "An empty roster counts relationship rows and does not read the per-child rule. "
        "The amount column remains tax.us.2025.eic.qualifying-child-count."
    )
    return out


def class_successor(v2: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(v2)
    out["version"] = "v3"
    _depend(out, PRESENT)
    branch = out["value"]["else"]["then"]
    assert _ref_name(branch["when"]) == COUNT and branch["when"]["cmp"] == "eq" and branch["then"] == 1
    branch["when"] = {"op": "all", "args": [_eq(COUNT, 0), _eq(PRESENT, 0)]}
    out["notes"] = v2["notes"] + (
        " v3: head of household is class 0 when a qualifying child is present, "
        "including a child who has no valid SSN, and class 1 only when the column "
        "is 0 and no qualifying child is present. Every other status is unchanged."
    )
    return out


def _walk(node: Any, pred, found: list) -> None:
    if isinstance(node, dict):
        if pred(node):
            found.append(node)
        for value in node.values():
            _walk(value, pred, found)
    elif isinstance(node, list):
        for value in node:
            _walk(value, pred, found)


def early_successor(v2: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(v2)
    out["version"] = "v3"
    _depend(out, PRESENT)

    def is_stop(node: dict[str, Any]) -> bool:
        if node.get("op") != "all" or len(node.get("args") or []) != 2:
            return False
        names = {_ref_name(arg) for arg in node["args"]}
        return names == {COUNT, STATUS_CLASS} and all(arg.get("cmp") == "eq" and arg.get("right") == 0 for arg in node["args"])

    found: list = []
    _walk(out["value"], is_stop, found)
    assert len(found) == 1
    found[0]["args"].append(_eq(PRESENT, 0))
    out["notes"] = v2["notes"] + (
        " v3: the column-0 status-class-0 stop also requires that no qualifying child is present, "
        "so a married filing separately return with a qualifying child who has no valid SSN is not stopped here."
    )
    return out


def questions_successor(v2: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(v2)
    out["version"] = "v3"
    _depend(out, PRESENT)

    def is_gate(node: dict[str, Any]) -> bool:
        if node.get("op") != "any" or len(node.get("args") or []) != 2:
            return False
        names = {_ref_name(arg) for arg in node["args"]}
        return names == {COUNT, STATUS_CLASS}

    found: list = []
    _walk(out["value"], is_gate, found)
    assert len(found) == 1
    found[0]["args"].append(_gt(PRESENT, 0))
    out["notes"] = v2["notes"] + (
        " v3: the remaining questions are also required when a qualifying child is present, "
        "including when the amount column is 0 and the status class is 0."
    )
    return out


def _skip_any(out: dict[str, Any]) -> list:
    when = out["value"]["when"]
    assert out["value"]["op"] == "choose" and out["value"]["then"] == 1 and when["op"] == "any"
    return when["args"]


def separated_successor(v1: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(v1)
    out["version"] = "v2"
    _depend(out, PRESENT)
    args = _skip_any(out)
    index = next(
        i for i, arg in enumerate(args)
        if arg.get("op") == "compare" and _ref_name(arg) == COUNT and arg.get("cmp") == "eq" and arg.get("right") == 0
    )
    args[index] = {"op": "all", "args": [args[index], _eq(PRESENT, 0)]}
    out["notes"] = v1["notes"] + (
        " v2: a column of 0 does not skip the answer when a qualifying child is present. "
        "The published question's yes is either statutory prong (apart the last six months, "
        "or a written separation agreement or decree of separate maintenance and apart at year end) "
        "or not married."
    )
    return out


def not_married_successor(v1: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(v1)
    out["version"] = "v2"
    _depend(out, PRESENT)
    _skip_any(out).append(_gt(PRESENT, 0))
    out["notes"] = v1["notes"] + (
        " v2: also 1 (not asked) when a qualifying child is present, so Step 4 question 1 "
        "is not asked of a head of household who has a qualifying child with no valid SSN."
    )
    return out


def _step4_successor(prior: dict[str, Any], version: str, sentence: str) -> dict[str, Any]:
    out = copy.deepcopy(prior)
    out["version"] = version
    _depend(out, PRESENT, STATUS_CLASS)
    _skip_any(out).append({"op": "all", "args": [_gt(PRESENT, 0), _eq(STATUS_CLASS, 0)]})
    out["notes"] = prior["notes"] + " " + sentence
    return out


def age_successor(v3: dict[str, Any]) -> dict[str, Any]:
    return _step4_successor(
        v3, "v4",
        "v4: also 1 when a qualifying child is present and the status class is 0, "
        "so Step 4 question 2 is not asked of married filing separately or of head of household "
        "with a qualifying child. Single, qualifying surviving spouse and married filing jointly "
        "are unchanged.",
    )


def home_successor(v3: dict[str, Any]) -> dict[str, Any]:
    return _step4_successor(
        v3, "v4",
        "v4: also 1 when a qualifying child is present and the status class is 0, "
        "so Step 4 question 3 is not asked of married filing separately or of head of household "
        "with a qualifying child. Single, qualifying surviving spouse and married filing jointly "
        "are unchanged.",
    )


def dump(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def written(content: Path) -> dict[str, dict[str, Any]]:
    read = lambda name: json.loads((content / name).read_text(encoding="utf-8"))  # noqa: E731
    bodies = {
        QUALIFIES_FILE: qualifies_rule(read(SOURCES[QUALIFIES_FILE])),
        PRESENT_FILE: present_rule(read(SOURCES[PRESENT_FILE])),
        CLASS_FILE: class_successor(read(SOURCES[CLASS_FILE])),
        EARLY_FILE: early_successor(read(SOURCES[EARLY_FILE])),
        QUESTIONS_FILE: questions_successor(read(SOURCES[QUESTIONS_FILE])),
        SEP_FILE: separated_successor(read(SOURCES[SEP_FILE])),
        NOT_MARRIED_FILE: not_married_successor(read(SOURCES[NOT_MARRIED_FILE])),
        AGE_FILE: age_successor(read(SOURCES[AGE_FILE])),
        HOME_FILE: home_successor(read(SOURCES[HOME_FILE])),
    }
    assert set(bodies) == set(SOURCES)
    return bodies


if __name__ == "__main__":
    content = Path(__file__).resolve().parent.parents[4] / "packages/content/tax/2025"
    bodies = written(content)
    print(json.dumps({name: {"id": body["id"], "version": body["version"]} for name, body in bodies.items()}, indent=2))
