"""Core v103 successors: Step 3 question 3, asked of a head of household with a qualifying child.

A recorded separated-spouse yes passes without the new fact. A recorded no from
that same filer asks the new question: no keeps the table credit, yes keeps $0.
Married filing separately never reads the new fact.

exclusive_presence refuses when two paths are active, so the new fact is not a
second path. The separated-spouse path reads that answer. Yes publishes 0. No
publishes 2 only for a head of household with a qualifying child, and 0
otherwise. The default (no separated answer) publishes 2 for that same
population. The answer rule reads the new fact only when the symbol is 2
(ADR 0081: a conditional_dependency_set member is read only on that branch).
"""
from __future__ import annotations

import copy
import json
from typing import Any

P = "tax.us.2025."
MARRIED = P + "eic.married-taxpayer"
INERT = P + "eic.married-taxpayer-inert"
RECORDED = P + "eic.married-taxpayer-recorded"
FROM_SEPARATED = P + "eic.married-taxpayer-from-separated"
ANSWER = P + "eic.answer.married-taxpayer"
SEPARATED = P + "eic.separated-spouse"
QUESTIONS = P + "eic.questions-required"
CLASS = P + "eic.status-class"
COLUMN = P + "eic.column-count"
PRESENT = P + "eic.qualifying-child-present"
RULE_RECORDED = P + "rule.eic-married-taxpayer-recorded"
RULE_FROM = P + "rule.eic-married-taxpayer-from-separated"
RULE_ANSWER = P + "rule.eic-answer.married-taxpayer"
RULE_SEPARATED = P + "rule.eic-answer.separated-spouse"
BUNDLE_ID = P + "eic-married-taxpayer.vocabulary"
BUNDLE_FILE = "eic-married-taxpayer.bundle.json"
QUESTION_FILE = "input-question.eic-married-taxpayer.v1.json"
SCOPE = {"family": "individual-income-tax", "jurisdiction": "US-federal", "tax_year": 2025}
CITATION = [{"id": P + "citation.form1040.line-27-31", "version": "v1"}]

# rule-artifact.v14 selection paths have minItems 2. The second path is inert
# unless a build without it validates. Track 1 sets this from that result.
KEEP_INERT = True
TITLE = (
    "Are you a married taxpayer whose filing status is married filing separately or head of household "
    "(2025 Form 1040 instructions, line 27a, Step 3 question 3)? Yes means married at the end of 2025. "
    "Publication 596, Rule 3, still treats a head of household who lived apart as married. Yes continues "
    "to the separated-spouse questions. No means not married at the end of 2025, so those questions are "
    "skipped. Asked of a head of household with a qualifying child, including one who already answered "
    "the separated-spouse question no. Contributed categorical assertion, domain {yes, no}, no default, "
    "presence-before-value, free supersession."
)
QUESTION = (
    "You file as head of household and a child is your qualifying child for the earned income credit. "
    "Are you a married taxpayer whose filing status is married filing separately or head of household? "
    "Answer yes if you were married at the end of 2025. Publication 596, Rule 3, still treats you as "
    "married when you file as head of household under the special rules for married taxpayers living "
    "apart. Yes continues to the separated-spouse questions. Answer no if you were not married at the "
    "end of 2025. No skips those questions and you keep the credit."
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


def _answered(fact: str, value: str) -> dict[str, Any]:
    return {"args": [
        {"condition": True, "members": [{"name": fact, "op": "ref"}], "op": "conditional_dependency_set"},
        {"cmp": "eq", "left": {"name": fact, "op": "ref"}, "op": "categorical_compare",
         "right": {"fact_type": {"id": fact, "version": "v1"}, "op": "category_literal", "value": value}},
    ], "op": "all"}


def _answered_no(fact: str) -> dict[str, Any]:
    return _answered(fact, "no")


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
    facts = [_fact(MARRIED, TITLE)]
    if KEEP_INERT:
        facts.append(_fact(INERT, (
            "Inactive second path for the Step 3 question 3 selection. Nothing asks this fact and no "
            "return records it. Contributed categorical assertion, domain {yes, no}, no default, "
            "presence-before-value, free supersession."
        )))
    return {
        "fact_types": facts,
        "id": BUNDLE_ID,
        "label": "Earned income credit Step 3 question 3 for a head of household with a qualifying child, tax year 2025",
        "schema": "bundle.v2",
        "version": "v1",
    }


def question() -> dict[str, Any]:
    return {"fact_type": {"id": MARRIED, "version": "v1"}, "id": P + "input-question.eic-married-taxpayer",
            "question": QUESTION, "schema": "input-question.v1", "version": "v1"}


def _inert_path() -> dict[str, Any]:
    return _decl(
        "inert", {"code": "DEPENDENCY_ABSENT", "op": "block"}, (),
        activity={"kind": "source_nonempty", "member_fact_type": {"id": INERT, "version": "v1"}},
    )


def _selection(publishes: str, rule_id: str, notes: str, default: dict[str, Any], path: dict[str, Any], missing: str) -> dict[str, Any]:
    paths = [path]
    if KEEP_INERT:
        paths.append(_inert_path())
    return {
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "citations": CITATION,
        "id": rule_id,
        "notes": notes,
        "pins": [],
        "publishes": publishes,
        "requires": [],
        "role": "computation",
        "schema": "rule-artifact.v14",
        "scope": SCOPE,
        "selection": {
            "conflict": "refuse",
            "default": default,
            "mode": "exclusive_presence",
            "paths": paths,
            "refusal": {"code": "DEPENDENCY_INVALID", "missing": [missing], "pins": []},
        },
        "version": "v1",
        "when": True,
    }


def recorded_rule() -> dict[str, Any]:
    """0 a separated answer is recorded or the filer is married filing separately. 1 skip. 2 ask."""
    default_value = {"else": {"else": 2, "op": "choose", "then": 0, "when": _status_is("married_filing_separately")},
                     "op": "choose", "then": 1, "when": _skip()}
    path = _decl(
        "separated-recorded", {"else": 0, "op": "choose", "then": 0, "when": True}, (),
        activity={"kind": "source_nonempty", "member_fact_type": {"id": SEPARATED, "version": "v1"}},
    )
    return _selection(
        RECORDED, RULE_RECORDED,
        "0 a separated answer is recorded, or married filing separately. 1 skips. 2 asks.",
        _decl("neither", default_value, ("filing_status",) + _SKIP_NAMES, activity=None),
        path, "eic-married-taxpayer-two-paths",
    )


def from_separated_rule() -> dict[str, Any]:
    """A recorded no asks only a head of household with a qualifying child. A recorded yes stays 0."""
    ask = {"args": [_status_is("head_of_household"), _eq(PRESENT, 1)], "op": "all"}
    no_branch = {"else": 0, "op": "choose", "then": 2, "when": ask}
    path_value = {"else": no_branch, "op": "choose", "then": 0, "when": _answered(SEPARATED, "yes")}
    names = (SEPARATED, PRESENT, "filing_status")
    path = _decl(
        "separated-recorded", path_value, names,
        activity={"kind": "source_nonempty", "member_fact_type": {"id": SEPARATED, "version": "v1"}},
    )
    return _selection(
        FROM_SEPARATED, RULE_FROM,
        "Recorded yes stays 0. Recorded no asks a head of household with a qualifying child.",
        _decl("neither", {"name": RECORDED, "op": "ref"}, (RECORDED,), activity=None),
        path, "eic-married-from-separated",
    )


def answer_rule() -> dict[str, Any]:
    return {
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": [FROM_SEPARATED, MARRIED]},
        "citations": CITATION,
        "id": RULE_ANSWER,
        "notes": (
            "Step 3 question 3. Publishes the recorded-path value when that value is not 2. When it is 2, "
            "reads tax.us.2025.eic.married-taxpayer: no publishes 1 (skip questions 4 and 5) and yes "
            "publishes 0 (the separated-spouse question is required). A missing fact blocks with this "
            "fact named. A recorded separated yes publishes 0 and this rule does not read the new fact."
        ),
        "pins": [_pin(FROM_SEPARATED)],
        "publishes": ANSWER,
        "requires": [FROM_SEPARATED],
        "role": "computation",
        "schema": "rule-artifact.v14",
        "scope": SCOPE,
        "value": {
            "else": {"else": 0, "op": "choose", "then": 1, "when": _answered_no(MARRIED)},
            "op": "choose",
            "then": {"name": FROM_SEPARATED, "op": "ref"},
            "when": _ne(FROM_SEPARATED, 2),
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
        "rule.eic-married-taxpayer-from-separated.v1.json": from_separated_rule(),
        "rule.eic-answer.married-taxpayer.v1.json": answer_rule(),
        "rule.eic-answer.separated-spouse.v3.json": separated_successor(v2),
    }


def dump(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"
