"""The prototype's new and successor content, written by build.py into a scratch copy of core v98.

Variant ``m``: one return-level yes/no answer, "you were not married at the end
of 2025", asked only on a head of household return with no qualifying child
counted for the earned income credit when the remaining credit questions are
required (the credit could be more than $0). Three rules change:

- ``rule.eic-status-class`` v1 to v2: a head of household with no counted
  qualifying child is class 1 (as single), so the credit's Step 4 path is
  taken instead of the class 0 stop; a head of household with a counted child
  stays class 0, so the separated-spouse answer is asked exactly as on v98.
  Every other status publishes v1's class.
- ``rule.eic-answer.not-married`` v1 (new): publishes 1 when the answer is not
  required or is yes, 0 when it is no, and blocks naming the answer when it is
  required and missing (the pattern of the other ``eic-answer`` rules).
- ``rule.eic-gate-result`` v2 to v3: v2 with the new answer read after the
  separated-spouse answer; 0 when it is 0.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

P = "tax.us.2025."
FACT = P + "eic.not-married"
ANSWER = P + "eic.answer.not-married"
BUNDLE_ID = P + "eic-marital-status.vocabulary"
BUNDLE_FILE = "eic-marital-status.bundle.json"
QUESTION_FILE = "input-question.eic-not-married.v1.json"
QUESTION_ID = P + "input-question.eic-not-married"
CLASS_RULE = P + "rule.eic-status-class"
ANSWER_RULE = P + "rule.eic-answer.not-married"
ANSWER_RULE_FILE = "rule.eic-answer.not-married.json"
GATE_RULE = P + "rule.eic-gate-result"
CLASS_FILE = "rule.eic-status-class.v2.json"
GATE_FILE = "rule.eic-gate-result.v3.json"
QR = P + "eic.questions-required"
COUNT = P + "eic.column-count"
STATUS = P + "filing-status"

TITLE = (
    "You were not married at the end of 2025: on December 31, 2025 you had never married, your spouse had died "
    "before 2025 and you had not remarried, your divorce or annulment was final, or you were legally separated "
    "from your spouse under a decree of divorce or separate maintenance. No means you were married at the end of 2025, including if you lived "
    "apart from your spouse and file as head of household because you are considered unmarried, or your "
    "divorce was not final (an interlocutory decree). A married taxpayer whose filing status is head of "
    "household cannot take the earned income credit without a qualifying child, so no means the credit is $0 "
    "(2025 Form 1040 instructions, line 27a Step 4 question 1; Pub. 596, Rule 3 and EIC Eligibility Checklist "
    "question 3; Pub. 501, Marital Status). Asked only on a head of household return with no qualifying child "
    "counted for the credit, when the credit could otherwise be more than $0. Contributed categorical "
    "assertion, domain {yes, no}, no default, presence-before-value, free supersession."
)
QUESTION = (
    "You file as head of household and no child is counted as your qualifying child for the earned income "
    "credit. Were you unmarried at the end of 2025? Answer yes if, on December 31, 2025, you had never married, "
    "your spouse had died before 2025 and you had not remarried, your divorce or annulment was final, or you "
    "were legally separated from your spouse under a decree of divorce or separate maintenance. Answer no if you "
    "were still married then, even if you lived apart from your spouse and file as head of household because you "
    "are considered unmarried: a married taxpayer filing as head of household cannot take the earned income "
    "credit without a qualifying child."
)
SEP_FACT = P + "eic.separated-spouse"
SEP_QUESTION_FILE = "input-question.eic-separated-spouse.v1.json"
SEP_QUESTION_ID = P + "input-question.eic-separated-spouse"
# 2025 Form 1040 instructions, line 27a, Step 3 questions 3 to 5 (the fact's yes means the credit can go on).
SEP_QUESTION = (
    "You file as head of household or married filing separately and a child is counted as your qualifying child "
    "for the earned income credit. Does the separated-spouse rule let you take the credit? Answer yes if you were "
    "not married at the end of 2025; or you were married and you and your spouse did not have the same principal "
    "residence for the last 6 months of 2025; or you were legally separated according to your state law under a "
    "written separation agreement or a decree of separate maintenance and you lived apart from your spouse at the "
    "end of 2025. Answer no if you were married, you and your spouse had the same principal residence for the last "
    "6 months of 2025, and you were not legally separated and living apart as described: you cannot take the "
    "credit, so it is $0."
)
CLASS_NOTES = (
    "0 married filing separately, or head of household with a qualifying child counted for the credit; 1 single, "
    "qualifying surviving spouse, or head of household with no counted qualifying child; 2 married filing "
    "jointly. v2: a head of household with no counted qualifying child takes Step 4 like a single filer, and "
    "tax.us.2025.rule.eic-answer.not-married asks whether the filer was married at the end of 2025 (Step 4 "
    "question 1 stops only a married taxpayer filing as head of household). A head of household with a counted "
    "child stays 0, so the separated-spouse answer (Step 3 questions 3-5) is asked exactly as in v1. Every "
    "other status publishes v1's class and reads nothing new."
)
ANSWER_NOTES = (
    "Step 4 question 1 for a head of household with no counted qualifying child: publishes 1 when the answer is "
    "not required (the remaining credit questions are not required, a qualifying child is counted, or the "
    "status is not head of household) or the filer answers yes (not married at the end of 2025); a no publishes "
    "0 ($0 credit). A missing required answer blocks with this fact named."
)
GATE_NOTES = (
    "Gate result: 0 at first failing answer, else worksheet line 6 when unsupported situations is clear. v3: "
    "also 0 when tax.us.2025.eic.answer.not-married is 0 (a married head of household with no qualifying child, "
    "line 27a Step 4 question 1)."
)


def _ref(name: str) -> dict[str, Any]:
    return {"op": "ref", "name": name}


def _status_is(value: str, cmp: str = "eq") -> dict[str, Any]:
    return {"op": "categorical_compare", "cmp": cmp, "left": _ref("filing_status"),
            "right": {"op": "category_literal", "fact_type": {"id": STATUS, "version": "v1"}, "value": value}}


def _pin(fact: str) -> dict[str, Any]:
    return {"id": fact, "origin": "assertion", "role": "input", "version": "v1"}


def bundle() -> dict[str, Any]:
    fact = {"id": FACT, "identity_keys": [{"kind": "literal", "name": "tax-year", "values": ["2025"]}],
            "nature": "determinable", "schema": "fact-type.v2", "supersession": {"policy": "free"},
            "title": TITLE, "value_schema": {"enum": ["yes", "no"]}, "version": "v1"}
    return {"fact_types": [fact], "id": BUNDLE_ID,
            "label": "Earned income credit marital status for a head of household without a qualifying child, tax year 2025",
            "schema": "bundle.v2", "version": "v1"}


def question() -> dict[str, Any]:
    return {"fact_type": {"id": FACT, "version": "v1"}, "id": QUESTION_ID, "question": QUESTION,
            "schema": "input-question.v1", "version": "v1"}


def class_successor(v1: dict[str, Any]) -> dict[str, Any]:
    """v1, with head of household split on the counted qualifying children."""
    out = copy.deepcopy(v1)
    out["version"] = "v2"
    out["requires"] = ["filing_status", COUNT]
    out["pins"] = [*copy.deepcopy(v1["pins"]), _pin(COUNT)]
    v1_value = copy.deepcopy(v1["value"])
    # v1: if any[MFS, HoH] then 0 else ...; v2: if MFS then 0, if HoH then (count = 0 -> 1, else 0), else v1's rest.
    out["value"] = {
        "op": "choose", "when": _status_is("married_filing_separately"), "then": 0,
        "else": {"op": "choose", "when": _status_is("head_of_household"),
                 "then": {"op": "choose", "when": {"op": "compare", "cmp": "eq", "left": _ref(COUNT), "right": 0},
                          "then": 1, "else": 0},
                 "else": v1_value["else"]},
    }
    out["blocked"] = {"code": "DEPENDENCY_ABSENT", "missing": ["filing_status", COUNT]}
    out["notes"] = CLASS_NOTES
    return out


def answer_rule(template: dict[str, Any]) -> dict[str, Any]:
    """A new ``eic-answer`` rule in the shape of ``rule.eic-answer.separated-spouse`` v1."""
    out = copy.deepcopy(template)
    out["id"] = ANSWER_RULE
    out["version"] = "v1"
    out["publishes"] = ANSWER
    out["requires"] = [QR, COUNT, "filing_status"]
    out["pins"] = [_pin(QR), _pin(COUNT), _pin(STATUS)]
    out["blocked"] = {"code": "DEPENDENCY_ABSENT", "missing": [QR, COUNT, "filing_status", FACT]}
    out["value"] = {
        "op": "choose",
        "when": {"op": "any", "args": [
            {"op": "compare", "cmp": "ne", "left": _ref(QR), "right": 1},
            {"op": "compare", "cmp": "gt", "left": _ref(COUNT), "right": 0},
            _status_is("head_of_household", "ne"),
        ]},
        "then": 1,
        "else": {"op": "choose",
                 "when": {"op": "all", "args": [
                     {"op": "conditional_dependency_set", "condition": True, "members": [_ref(FACT)]},
                     {"op": "categorical_compare", "cmp": "eq", "left": _ref(FACT),
                      "right": {"op": "category_literal", "fact_type": {"id": FACT, "version": "v1"}, "value": "no"}},
                 ]},
                 "then": 0, "else": 1},
    }
    out["notes"] = ANSWER_NOTES
    return out


def gate_successor(v2: dict[str, Any]) -> dict[str, Any]:
    """v2 with the new answer checked right after the separated-spouse answer."""
    out = copy.deepcopy(v2)
    out["version"] = "v3"
    sep = P + "eic.answer.separated-spouse"
    at = out["requires"].index(sep) + 1
    out["requires"].insert(at, ANSWER)
    pin_at = [p["id"] for p in out["pins"]].index(sep) + 1
    out["pins"].insert(pin_at, _pin(ANSWER))

    def splice(node: dict[str, Any]) -> dict[str, Any]:
        when = node.get("when") or {}
        if node.get("op") == "choose" and when.get("left") == _ref(sep):
            node["else"] = {"op": "choose",
                            "when": {"op": "compare", "cmp": "eq", "left": _ref(ANSWER), "right": 0},
                            "then": 0, "else": node["else"]}
            return node
        node["else"] = splice(node["else"])
        return node

    out["value"] = splice(out["value"])
    out["notes"] = GATE_NOTES
    return out


def sep_question() -> dict[str, Any]:
    return {"fact_type": {"id": SEP_FACT, "version": "v1"}, "id": SEP_QUESTION_ID, "question": SEP_QUESTION,
            "schema": "input-question.v1", "version": "v1"}


def dump(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def written(content: Path) -> dict[str, dict[str, Any]]:
    """Every new file, keyed by file name, built from the published v98 members in ``content``."""
    read = lambda name: json.loads((content / name).read_text(encoding="utf-8"))  # noqa: E731
    return {BUNDLE_FILE: bundle(), QUESTION_FILE: question(), SEP_QUESTION_FILE: sep_question(),
            CLASS_FILE: class_successor(read("rule.eic-status-class.json")),
            ANSWER_RULE_FILE: answer_rule(read("rule.eic-answer.separated-spouse.json")),
            GATE_FILE: gate_successor(read("rule.eic-gate-result.v2.json"))}


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    for name, body in written(here.parents[4] / "packages/content/tax/2025").items():
        print("=====", name)
        print(dump(body)[:3000])
