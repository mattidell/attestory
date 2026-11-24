"""Scratch successors of the 2025 qualified-dividends worksheet ceilings.

Lines 6 and 13 of the Qualified Dividends and Capital Gain Tax Worksheet
look up a ceiling from the filing status alone. These successors read the
existing head-of-household and qualifying-surviving-spouse answers the same
way Standard Deduction Worksheet line 3 does: only on that status, yes keeps
the published lookup, no refuses the line and names the answer, and an
unanswered answer blocks by naming it. Single, married filing jointly and
married filing separately keep the v1 lookup and read neither answer.

Nothing here is written under packages/. build.py copies published content
outside the repository and validates the successor with
tools.package_successor.generate_to_directory.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

P = "tax.us.2025."
HOH = P + "hoh.tests-met"
QSS = P + "qss.tests-met"
LINE6 = P + "rule.qdcg-worksheet.line-6"
LINE13 = P + "rule.qdcg-worksheet.line-13"
LINE6_FILE = "rule.qdcg-worksheet.line-6.v2.json"
LINE13_FILE = "rule.qdcg-worksheet.line-13.v2.json"

NOTES = {
    LINE6: (
        "Qualified Dividends and Capital Gain Tax Worksheet line 6. The 0% ceiling for the filing "
        "status, reusing tax.us.2025.parameter.preferential-zero-ceiling v1 ($48,350 single or married "
        "filing separately, $96,700 married filing jointly or qualifying surviving spouse, $64,750 head "
        "of household; 2025 Form 1040 instructions, worksheet line 6). v2 reads tax.us.2025.hoh.tests-met "
        "only when the filing status is head of household, and tax.us.2025.qss.tests-met only when it is "
        "qualifying surviving spouse. Yes publishes the same lookup as v1. No refuses the line "
        "(DEPENDENCY_INVALID, naming the answer so the page shows that question beside the refusal) "
        "rather than showing that status's ceiling. An unanswered answer blocks naming it. The worksheet "
        "states a ceiling for each filing status and does not give another status's ceiling when the "
        "checked status does not apply. Single, married filing jointly and married filing separately "
        "read nothing new."
    ),
    LINE13: (
        "Qualified Dividends and Capital Gain Tax Worksheet line 13. The 15% ceiling for the filing "
        "status, reusing tax.us.2025.parameter.preferential-fifteen-ceiling v1 ($533,400 single, "
        "$300,000 married filing separately, $600,050 married filing jointly or qualifying surviving "
        "spouse, $566,700 head of household; 2025 Form 1040 instructions, worksheet line 13). v2 reads "
        "tax.us.2025.hoh.tests-met only when the filing status is head of household, and "
        "tax.us.2025.qss.tests-met only when it is qualifying surviving spouse. Yes publishes the same "
        "lookup as v1. No refuses the line (DEPENDENCY_INVALID, naming the answer so the page shows that "
        "question beside the refusal) rather than showing that status's ceiling. An unanswered answer "
        "blocks naming it. The worksheet states a ceiling for each filing status and does not give "
        "another status's ceiling when the checked status does not apply. Single, married filing jointly "
        "and married filing separately read nothing new."
    ),
}


def _status_is(value: str) -> dict[str, Any]:
    return {"op": "categorical_compare", "cmp": "eq", "left": {"op": "ref", "name": "filing_status"},
            "right": {"op": "category_literal", "fact_type": {"id": P + "filing-status", "version": "v1"},
                      "value": value}}


def _answered_yes(fact: str) -> dict[str, Any]:
    return {"op": "categorical_compare", "cmp": "eq", "left": {"op": "ref", "name": fact},
            "right": {"op": "category_literal", "fact_type": {"id": fact, "version": "v1"}, "value": "yes"}}


def _refuse(fact: str) -> dict[str, Any]:
    """A no refuses the line and names the answer, so the page shows that question."""
    return {"op": "block", "code": "DEPENDENCY_INVALID", "missing": [fact]}


def successor(v1: dict[str, Any]) -> dict[str, Any]:
    """v1's lookup on every branch that publishes, under rule-artifact.v17.

    v17 is the published schema that allows an expression block to name the
    answer it refuses. v14, which lines 6 and 13 use today, does not.
    """
    lookup = copy.deepcopy(v1["value"])
    out = copy.deepcopy(v1)
    out["schema"] = "rule-artifact.v17"
    out["version"] = "v2"
    out["value"] = {
        "op": "choose", "when": _status_is("head_of_household"),
        "then": {"op": "choose", "when": _answered_yes(HOH), "then": copy.deepcopy(lookup), "else": _refuse(HOH)},
        "else": {"op": "choose", "when": _status_is("qualifying_surviving_spouse"),
                 "then": {"op": "choose", "when": _answered_yes(QSS), "then": copy.deepcopy(lookup),
                          "else": _refuse(QSS)},
                 "else": lookup},
    }
    out["notes"] = NOTES[v1["id"]]
    return out


def written(source: Path) -> dict[str, dict[str, Any]]:
    return {
        LINE6_FILE: successor(json.loads((source / "rule.qdcg-worksheet.line-6.json").read_text(encoding="utf-8"))),
        LINE13_FILE: successor(json.loads((source / "rule.qdcg-worksheet.line-13.json").read_text(encoding="utf-8"))),
    }


def dump(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"
