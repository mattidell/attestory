"""The prototype's new and successor content, written by build.py into a scratch copy of core v97.

Variant ``q``: two return-level yes/no answers, one per status, each read only
when the filing status is that status, and a successor of the one rule that
looks up the 2025 standard deduction base for the filing status
(Standard Deduction Worksheet for Dependents line 3, which both branches of
the Form 1040 line 12e standard deduction read). On head of household the
successor reads the head of household answer, on qualifying surviving spouse
the qualifying surviving spouse answer; yes publishes the same parameter
lookup as v1, no refuses the line, unanswered asks the question. Single,
married filing jointly and married filing separately read nothing new.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

P = "tax.us.2025."
HOH = P + "hoh.tests-met"
QSS = P + "qss.tests-met"
BUNDLE_ID = P + "filing-status-tests.vocabulary"
BUNDLE_FILE = "filing-status-tests.bundle.json"
RULE_ID = P + "rule.dependents-worksheet-line-3"

HOH_TITLE = (
    "You meet the 2025 head of household tests: on December 31, 2025 you were unmarried or considered "
    "unmarried; you paid more than half the cost of keeping up a home for 2025; and a qualifying person lived "
    "with you in that home for more than half of 2025, or the qualifying person is your parent whom you can "
    "claim as a dependent and you paid more than half the cost of keeping up your parent's main home for all of "
    "2025 (2025 Form 1040 instructions, Head of Household, Tests 1 and 2; Pub. 501, Head of Household and "
    "Table 4). Yes means head of household applies. No means it does not, and the standard deduction and "
    "everything that reads it are refused rather than figured on head of household amounts; file with the "
    "status that applies instead. Read only when the filing status is head of household. Contributed "
    "categorical assertion, domain {yes, no}, no default, presence-before-value, free supersession."
)
QSS_TITLE = (
    "You meet the 2025 qualifying surviving spouse tests: your spouse died in 2023 or 2024 and you did not "
    "remarry before the end of 2025; you could have filed a joint return with your spouse for the year your "
    "spouse died; you have a child or stepchild (not a foster child) whom you can claim as a dependent, or could "
    "claim except that the child had gross income of $5,200 or more, filed a joint return, or you could be "
    "claimed as a dependent on someone else's return; that child lived in your home for all of 2025; and you "
    "paid more than half the cost of keeping up that home (2025 Form 1040 instructions, Qualifying Surviving "
    "Spouse; Pub. 501, Qualifying Surviving Spouse). Yes means qualifying surviving spouse applies. No means "
    "it does not, and the standard deduction and everything that reads it are refused rather than figured on "
    "joint return amounts; file with the status that applies instead. Read only when the filing status is "
    "qualifying surviving spouse. Contributed categorical assertion, domain {yes, no}, no default, "
    "presence-before-value, free supersession."
)
HOH_QUESTION = (
    "You chose head of household. Do all of these apply to you for 2025: on December 31, 2025 you were "
    "unmarried, or considered unmarried (for example, married but your spouse did not live in your home for "
    "the last 6 months of 2025); you paid more than half the cost of keeping up your home for 2025; and a "
    "qualifying person, such as your child or a relative you can claim as a dependent, lived with you there "
    "for more than half of 2025 (a dependent parent need not live with you if you paid more than half the cost "
    "of your parent's main home for all of 2025)? If any of these does not apply, you cannot file as head of "
    "household; change your filing status."
)
QSS_QUESTION = (
    "You chose qualifying surviving spouse. Do all of these apply to you: your spouse died in 2023 or 2024 and "
    "you did not remarry before the end of 2025; you could have filed a joint return with your spouse for the "
    "year your spouse died; you have a child or stepchild (not a foster child) you can claim as a dependent "
    "who lived in your home all of 2025; and you paid more than half the cost of keeping up that home? If any of "
    "these does not apply, you cannot file as a qualifying surviving spouse; change your filing status (if your "
    "spouse died in 2025, you can file a joint return for 2025)."
)
NOTES_V2 = (
    "Standard Deduction Worksheet for Dependents, line 3: the basic 2025 standard deduction for the filing "
    "status ($15,750 single/MFS, $31,500 MFJ/QSS, $23,625 HoH), reusing tax.us.2025.parameter."
    "standard-deduction-base v1. v2: head of household and qualifying surviving spouse each require the filer's "
    "answer that the status's tests are met (tax.us.2025.hoh.tests-met, tax.us.2025.qss.tests-met), read only "
    "on that status; yes publishes the same lookup as v1, no refuses the line (DEPENDENCY_INVALID, naming the "
    "answer so the page shows its question beside the refusal) so the "
    "standard deduction, taxable income and the tax are not figured on that status's amounts, and an "
    "unanswered answer blocks naming it. This is the only rule that reads the standard deduction base, and "
    "line 12e reads the standard deduction on every route, so every larger amount either status carries "
    "(standard deduction, Tax Table column and rate schedule, preferential-rate ceilings) is downstream of it. "
    "Single, married filing jointly and married filing separately read nothing new."
)


def _fact(fact_id: str, title: str) -> dict[str, Any]:
    return {"id": fact_id, "identity_keys": [{"kind": "literal", "name": "tax-year", "values": ["2025"]}],
            "nature": "determinable", "schema": "fact-type.v2", "supersession": {"policy": "free"},
            "title": title, "value_schema": {"enum": ["yes", "no"]}, "version": "v1"}


def bundle() -> dict[str, Any]:
    return {"fact_types": [_fact(HOH, HOH_TITLE), _fact(QSS, QSS_TITLE)], "id": BUNDLE_ID,
            "label": "2025 head of household and qualifying surviving spouse tests", "schema": "bundle.v2",
            "version": "v1"}


def questions() -> dict[str, dict[str, Any]]:
    return {
        "input-question.hoh-tests-met.v1.json": {"fact_type": {"id": HOH, "version": "v1"},
                                                  "id": P + "input-question.hoh-tests-met",
                                                  "question": HOH_QUESTION, "schema": "input-question.v1",
                                                  "version": "v1"},
        "input-question.qss-tests-met.v1.json": {"fact_type": {"id": QSS, "version": "v1"},
                                                  "id": P + "input-question.qss-tests-met",
                                                  "question": QSS_QUESTION, "schema": "input-question.v1",
                                                  "version": "v1"},
    }


def _status_is(value: str) -> dict[str, Any]:
    return {"op": "categorical_compare", "cmp": "eq", "left": {"op": "ref", "name": "filing_status"},
            "right": {"op": "category_literal", "fact_type": {"id": P + "filing-status", "version": "v1"},
                      "value": value}}


def _answered_yes(fact: str) -> dict[str, Any]:
    return {"op": "categorical_compare", "cmp": "eq", "left": {"op": "ref", "name": fact},
            "right": {"op": "category_literal", "fact_type": {"id": fact, "version": "v1"}, "value": "yes"}}


def _refuse(fact: str) -> dict[str, Any]:
    """A "no" refuses the line and names the answer, so the page shows that question beside the refusal."""
    return {"op": "block", "code": "DEPENDENCY_INVALID", "missing": [fact]}


def rule_successor(v1: dict[str, Any]) -> dict[str, Any]:
    """v1 with the lookup kept as the value on every branch that publishes."""
    lookup = copy.deepcopy(v1["value"])
    out = copy.deepcopy(v1)
    out["schema"] = "rule-artifact.v17"  # an expression block may name the answer it refuses on (ADR-0086)
    out["version"] = "v2"
    out["value"] = {
        "op": "choose", "when": _status_is("head_of_household"),
        "then": {"op": "choose", "when": _answered_yes(HOH), "then": copy.deepcopy(lookup), "else": _refuse(HOH)},
        "else": {"op": "choose", "when": _status_is("qualifying_surviving_spouse"),
                 "then": {"op": "choose", "when": _answered_yes(QSS), "then": copy.deepcopy(lookup),
                          "else": _refuse(QSS)},
                 "else": lookup},
    }
    out["notes"] = NOTES_V2
    return out


def dump(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    v1 = json.loads((here.parents[4] / "packages/content/tax/2025/rule.dependents-worksheet-line-3.json").read_text())
    print(dump(rule_successor(v1))[:4000])
