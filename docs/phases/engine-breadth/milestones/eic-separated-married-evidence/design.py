"""Scratch successors for P0b: Step 3 question 3, asked only of a married head of household.

Written by build.py into a scratch copy of published core v102. Nothing in
packages/ is edited.

The new fact is tax.us.2025.eic.married-taxpayer. Yes means a married taxpayer
for the 2025 Form 1040 instructions, line 27a, Step 3 question 3. No means not
married at the end of 2025, so questions 4 and 5 are skipped.

exclusive_presence refuses when two paths are active, so the new fact is not
a second path. One path is active when a separated-spouse answer is already
recorded. That path does not read the new fact. The default (no separated
answer) publishes 2 only for a head of household with a qualifying child; the
ordinary answer rule then reads the new fact, and a missing fact blocks there
(ADR 0081: a conditional_dependency_set member is read only on that branch).
Married filing separately never reads the new fact. A recorded separated
answer, yes or no, is applied as on v102, so a recorded yes still passes.
"""
from __future__ import annotations

import copy
import json
from typing import Any

P = "tax.us.2025."
MARRIED = P + "eic.married-taxpayer"
INERT = P + "eic.married-taxpayer-inert"
RECORDED = P + "eic.married-taxpayer-recorded"
ANSWER = P + "eic.answer.married-taxpayer"
SEPARATED = P + "eic.separated-spouse"
QUESTIONS = P + "eic.questions-required"
CLASS = P + "eic.status-class"
COLUMN = P + "eic.column-count"
PRESENT = P + "eic.qualifying-child-present"
RULE_RECORDED = P + "rule.eic-married-taxpayer-recorded"
RULE_ANSWER = P + "rule.eic-answer.married-taxpayer"
RULE_SEPARATED = P + "rule.eic-answer.separated-spouse"
BUNDLE_ID = P + "eic-married-taxpayer.vocabulary"
BUNDLE_FILE = "eic-married-taxpayer.bundle.json"
QUESTION_FILE = "input-question.eic-married-taxpayer.v1.json"
SCOPE = {"family": "individual-income-tax", "jurisdiction": "US-federal", "tax_year": 2025}
CITATION = [{"id": P + "citation.form1040.line-27-31", "version": "v1"}]

TITLE = (
    "Are you a married taxpayer whose filing status is married filing separately or head of household "
    "(2025 Form 1040 instructions, line 27a, Step 3 question 3)? Yes means you were married at the end of "
    "2025. A person who files as head of household because they lived apart is still married for this credit "
    "(Publication 596, Rule 3: special rules for married taxpayers living apart). Yes continues to Step 3 "
    "questions 4 and 5: the credit is allowed only when a qualifying child lived with you for more than half "
    "of 2025 and either you lived apart for the last 6 months of 2025, or you were legally separated under "
    "state law under a written separation agreement or a decree of separate maintenance and you did not live "
    "in the same household at the end of 2025. No means you were not married at the end of 2025, questions 4 "
    "and 5 are skipped, and the credit is not stopped by this rule. Asked only of a head of household with a "
    "qualifying child when no separated-spouse answer is already recorded. Contributed categorical assertion, "
    "domain {yes, no}, no default, presence-before-value, free supersession."
)
QUESTION = (
    "You file as head of household and a child is your qualifying child for the earned income credit. "
    "Are you a married taxpayer whose filing status is married filing separately or head of household? "
    "Answer yes if you were married at the end of 2025. You are still married for this credit if you file "
    "as head of household because you are considered unmarried after living apart from your spouse: "
    "Publication 596 says a married person who qualifies to file as head of household under the special "
    "rules for married taxpayers living apart is still married, and Rule 3 still applies. Yes continues "
    "to the separated-spouse questions. You can take the credit only if the child lived with you for more "
    "than half of 2025 and either you lived apart from your spouse for the last 6 months of 2025, or you "
    "are legally separated according to your state law under a written separation agreement or a decree of "
    "separate maintenance and you did not live in the same household as your spouse at the end of 2025. "
    "Answer no if you were not married at the end of 2025. No skips those questions and you keep the credit."
)


def _pin(name: str, *, choice: bool = False) -> dict[str, Any]:
    if choice:
        return {"id": name, "role": "choice", "version": "v1"}
    return {"id": name, "origin": "assertion", "role": "input", "version": "v1"}


def _eq(name: str, right: int) -> dict[str, Any]:
    return {"cmp": "eq", "left": {"name": name, "op": "ref"}, "op": "compare", "right": right}


def _ne(name: str, right: int) -> dict[str, Any]:
    return {"cmp": "ne", "left": {"name": name, "op": "ref"}, "op": "compare", "right": right}


def _skip() -> dict[str, Any]:
    """The v2 reasons the separated-spouse answer is not read."""
    return {"args": [
        _ne(QUESTIONS, 1),
        {"args": [_eq(COLUMN, 0), _eq(PRESENT, 0)], "op": "all"},
        _ne(CLASS, 0),
    ], "op": "any"}


def _status_is(value: str) -> dict[str, Any]:
    return {"cmp": "eq", "left": {"name": "filing_status", "op": "ref"}, "op": "categorical_compare",
            "right": {"fact_type": {"id": P + "filing-status", "version": "v1"}, "op": "category_literal",
                      "value": value}}


def _answered_no(fact: str) -> dict[str, Any]:
    return {"args": [
        {"condition": True, "members": [{"name": fact, "op": "ref"}], "op": "conditional_dependency_set"},
        {"cmp": "eq", "left": {"name": fact, "op": "ref"}, "op": "categorical_compare",
         "right": {"fact_type": {"id": fact, "version": "v1"}, "op": "category_literal", "value": "no"}},
    ], "op": "all"}


_SKIP_NAMES = (QUESTIONS, COLUMN, PRESENT, CLASS)


def _decl(ident: str, value: dict[str, Any], names: tuple[str, ...], *, activity: dict[str, Any] | None) -> dict[str, Any]:
    body: dict[str, Any] = {
        "id": ident,
        "pins": [_pin(name, choice=(name == "filing_status")) for name in names],
        "reads_subject_results": [],
        "requires": list(names),
        "value": value,
        "when": True,
    }
    if activity is not None:
        body["activity"] = activity
    return body


def _fact(fact_id: str, title: str) -> dict[str, Any]:
    return {
        "id": fact_id,
        "identity_keys": [{"kind": "literal", "name": "tax-year", "values": ["2025"]}],
        "nature": "determinable",
        "schema": "fact-type.v2",
        "supersession": {"policy": "free"},
        "title": title,
        "value_schema": {"enum": ["yes", "no"]},
        "version": "v1",
    }


def bundle() -> dict[str, Any]:
    return {
        "fact_types": [
            _fact(MARRIED, TITLE),
            _fact(INERT, (
                "Inactive second path for the Step 3 question 3 selection. exclusive_presence requires two "
                "paths. Nothing asks this fact and no return records it. Contributed categorical assertion, "
                "domain {yes, no}, no default, presence-before-value, free supersession."
            )),
        ],
        "id": BUNDLE_ID,
        "label": "Earned income credit Step 3 question 3 for a head of household with a qualifying child, tax year 2025",
        "schema": "bundle.v2",
        "version": "v1",
    }


def question() -> dict[str, Any]:
    return {"fact_type": {"id": MARRIED, "version": "v1"}, "id": P + "input-question.eic-married-taxpayer",
            "question": QUESTION, "schema": "input-question.v1", "version": "v1"}


def recorded_rule() -> dict[str, Any]:
    """0 apply a recorded separated answer, 1 skip, 2 ask the new question.

    The path does not repeat the population skips. rule.eic-answer.separated-spouse
    v3 still has those skips, so a recorded answer outside the population publishes
    0 here and is not read there.
    """
    default_value = {"else": {"else": 2, "op": "choose", "then": 0, "when": _status_is("married_filing_separately")},
                     "op": "choose", "then": 1, "when": _skip()}
    return {
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "citations": CITATION,
        "id": RULE_RECORDED,
        "notes": (
            "0 applies a recorded separated answer or married filing separately. 1 skips. 2 asks Step 3 "
            "question 3 of a head of household with a qualifying child and no recorded answer. The new "
            "fact is not a second path, because exclusive_presence would refuse when both are present."
        ),
        "pins": [],
        "publishes": RECORDED,
        "requires": [],
        "role": "computation",
        "schema": "rule-artifact.v14",
        "scope": SCOPE,
        "selection": {
            "conflict": "refuse",
            "default": _decl("neither", default_value, ("filing_status",) + _SKIP_NAMES, activity=None),
            "mode": "exclusive_presence",
            "paths": [
                _decl(
                    "separated-recorded", {"else": 0, "op": "choose", "then": 0, "when": True}, (),
                    activity={"kind": "source_nonempty", "member_fact_type": {"id": SEPARATED, "version": "v1"}},
                ),
                _decl(
                    "inert", {"code": "DEPENDENCY_ABSENT", "op": "block"}, (),
                    activity={"kind": "source_nonempty", "member_fact_type": {"id": INERT, "version": "v1"}},
                ),
            ],
            "refusal": {"code": "DEPENDENCY_INVALID", "missing": ["eic-married-taxpayer-two-paths"], "pins": []},
        },
        "version": "v1",
        "when": True,
    }


def answer_rule() -> dict[str, Any]:
    return {
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": [RECORDED, MARRIED]},
        "citations": CITATION,
        "id": RULE_ANSWER,
        "notes": (
            "Step 3 question 3. Publishes the recorded-path value when that value is not 2. When it is 2, "
            "reads tax.us.2025.eic.married-taxpayer: no publishes 1 (skip questions 4 and 5) and yes "
            "publishes 0 (the separated-spouse question is required). A missing fact blocks with this "
            "fact named. The fact is not read when a separated-spouse answer is already recorded."
        ),
        "pins": [_pin(RECORDED)],
        "publishes": ANSWER,
        "requires": [RECORDED],
        "role": "computation",
        "schema": "rule-artifact.v14",
        "scope": SCOPE,
        "value": {
            "else": {"else": 0, "op": "choose", "then": 1, "when": _answered_no(MARRIED)},
            "op": "choose",
            "then": {"name": RECORDED, "op": "ref"},
            "when": _ne(RECORDED, 2),
        },
        "version": "v1",
        "when": True,
    }


def separated_successor(v2: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(v2)
    out["version"] = "v3"
    out["requires"] = list(v2["requires"]) + [ANSWER]
    out["pins"] = list(v2["pins"]) + [_pin(ANSWER)]
    out["blocked"] = {"code": "DEPENDENCY_ABSENT", "missing": list(v2["blocked"]["missing"]) + [ANSWER]}
    out["value"] = copy.deepcopy(v2["value"])
    out["value"]["when"]["args"] = list(v2["value"]["when"]["args"]) + [_eq(ANSWER, 1)]
    out["notes"] = (
        "Separated spouse answer. v3: also publishes 1 without reading the separated-spouse fact when "
        "tax.us.2025.eic.answer.married-taxpayer is 1 (not in the population, or a head of household who "
        "answered Step 3 question 3 no). A 0 applies the recorded answer or, when none is recorded, blocks "
        "on it. Married filing separately and a head of household who answered yes are the 0 cases. A "
        "recorded yes with no new answer still publishes 1."
    )
    return out


def written(v2: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        BUNDLE_FILE: bundle(),
        QUESTION_FILE: question(),
        "rule.eic-married-taxpayer-recorded.v1.json": recorded_rule(),
        "rule.eic-answer.married-taxpayer.v1.json": answer_rule(),
        "rule.eic-answer.separated-spouse.v3.json": separated_successor(v2),
    }


def dump(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"
