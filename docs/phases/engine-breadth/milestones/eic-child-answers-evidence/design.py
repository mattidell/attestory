"""The P0 scratch content: the routes by which content could put a question on a line that a member's missing answer blocks.

Evidence for docs/phases/engine-breadth/milestones/eic-child-answers.md (P0).
Charter: docs/reviews/eic-child-answers/charter-p0.md.

Two scratch successors of published core v100 (build.py), each tried with probe.py:

``q`` (route 2, an input question for each per-member fact type). One
``input-question.v1`` member per per-member answer that a roster's count
reads and that is not the membership fact itself: the five earned income
child answers (age, residency, joint return, SSN, the tie-breaker's
"another person could claim"), the four child tax credit answers, the
other-dependent child's TIN and the seven other-dependent relative answers.
No rule changes. The sentence is a **scratch placeholder**, not proposed
wording: the fact type's declared title up to "Yes means", prefixed so that
nobody mistakes it for a sourced question. P0 asks only whether the page
reaches it.

``g`` (route 1, declared ``missing`` names on the rule that blocks, ADR 0086).
``q`` plus ``rule.eic-qualifying-child-count`` v2 and ``rule.ctc-child-count``
v2 as ``rule-artifact.v17``. Each keeps v1's selection, refusal and default
unchanged; only the ``children`` path changes. It adds declared subject reads
of the per-child test results that have a per-answer subject (for the earned
income credit: age-met, residency-met, joint-return-met, ssn-met; for the
child tax credit: under-17-met, lived-with-you-met, no-support-met,
citizen-met, joint-return-met, ssn-met) and, before the old sum, a chain of
``choose`` guards: when fewer children have a result for a test than are on
the closed roster, a ``block`` (``DEPENDENCY_ABSENT``) declares the missing
answer's fact type as its ``missing`` name. Otherwise the value is v1's sum,
unchanged. A test that is missing for several children, or several tests
missing, name the first test in the chain only.

Route 3 (a closure mapping question) needs no successor: every one of the
four rosters already has a closure mapping with a declared closure question
on v100 (p0.md, section 3).
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

P = "tax.us.2025."
PREFIX = "[P0 scratch placeholder, not proposed wording] "

# Fact type -> its vocabulary bundle (each a v100 member).
FACTS: dict[str, str] = {
    P + "eic.child.age": P + "eic-child-roster.vocabulary",
    P + "eic.child.residency": P + "eic-child-roster.vocabulary",
    P + "eic.child.joint-return": P + "eic-child-roster.vocabulary",
    P + "eic.child.ssn": P + "eic-child-roster.vocabulary",
    P + "dtb.child.another-could-claim": P + "dtb-questions",
    P + "ctc.child.under-17": P + "ctc-child-roster.vocabulary",
    P + "ctc.child.lived-with-you": P + "ctc-child-roster.vocabulary",
    P + "ctc.child.no-over-half-support": P + "ctc-child-roster.vocabulary",
    P + "ctc.child.citizen-or-resident": P + "ctc-child-roster.vocabulary",
    P + "odc.child.tin": P + "odc-child-roster.vocabulary",
    P + "odc.dependent.relationship": P + "odc-relative-roster.vocabulary",
    P + "odc.dependent.not-qualifying-child": P + "odc-relative-roster.vocabulary",
    P + "odc.dependent.gross-income-under-limit": P + "odc-relative-roster.vocabulary",
    P + "odc.dependent.over-half-support": P + "odc-relative-roster.vocabulary",
    P + "odc.dependent.tin": P + "odc-relative-roster.vocabulary",
    P + "odc.dependent.citizen-or-resident": P + "odc-relative-roster.vocabulary",
    P + "odc.dependent.not-joint-return": P + "odc-relative-roster.vocabulary",
}

EIC_COUNT = P + "rule.eic-qualifying-child-count"
CTC_COUNT = P + "rule.ctc-child-count"
# (count rule, roster family, roster member fact type, [(test result symbol, its subject = the answer)])
GUARDS: dict[str, tuple[str, str, list[tuple[str, str]]]] = {
    EIC_COUNT: (P + "eic.child-roster", P + "eic.child.relationship", [
        (P + "eic.child.age-met", P + "eic.child.age"),
        (P + "eic.child.residency-met", P + "eic.child.residency"),
        (P + "eic.child.joint-return-met", P + "eic.child.joint-return"),
        (P + "eic.child.ssn-met", P + "eic.child.ssn"),
    ]),
    CTC_COUNT: (P + "ctc.child-roster", P + "ctc.child.claimed-as-dependent", [
        (P + "ctc.child.under-17-met", P + "ctc.child.under-17"),
        (P + "ctc.child.lived-with-you-met", P + "ctc.child.lived-with-you"),
        (P + "ctc.child.no-support-met", P + "ctc.child.no-over-half-support"),
        (P + "ctc.child.citizen-met", P + "ctc.child.citizen-or-resident"),
        (P + "ctc.child.joint-return-met", P + "eic.child.joint-return"),
        (P + "ctc.child.ssn-met", P + "eic.child.ssn"),
    ]),
}
COUNT_FILES = {EIC_COUNT: "rule.eic-qualifying-child-count.json", CTC_COUNT: "rule.ctc-child-count.json"}


def question_id(fact: str) -> str:
    return P + "input-question.p0-member-" + fact.removeprefix(P).replace(".", "-")


def question_file(fact: str) -> str:
    return "input-question.p0-member-" + fact.removeprefix(P).replace(".", "-") + ".v1.json"


def placeholder(title: str) -> str:
    head = title.split(" Yes means")[0].strip().rstrip(".")
    return PREFIX + "Is this true: " + head + "?"


def fact_titles(content: Path) -> dict[str, str]:
    titles: dict[str, str] = {}
    for path in content.glob("*.json"):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if isinstance(body, dict) and body.get("id") in set(FACTS.values()) and body.get("schema", "").startswith("bundle."):
            for fact_type in body.get("fact_types") or []:
                if fact_type.get("id") in FACTS:
                    titles[fact_type["id"]] = str(fact_type.get("title") or "")
    return titles


def questions(content: Path) -> dict[str, dict[str, Any]]:
    titles = fact_titles(content)
    missing = sorted(set(FACTS) - set(titles))
    assert not missing, missing
    return {question_file(fact): {"fact_type": {"id": fact, "version": "v1"}, "id": question_id(fact),
                                  "question": placeholder(titles[fact]), "schema": "input-question.v1", "version": "v1"}
            for fact in FACTS}


def guarded(rule: dict[str, Any]) -> dict[str, Any]:
    """The count rule's v2: rule-artifact.v17, the ``children`` path guarded by declared ``missing`` names."""
    family, member, tests = GUARDS[rule["id"]]
    new = copy.deepcopy(rule)
    new["schema"] = "rule-artifact.v17"
    new["version"] = "v2"
    path = next(p for p in new["selection"]["paths"] if p["id"] == "children")
    for symbol, subject in tests:
        path["reads_subject_results"].append({"symbol": symbol, "subject": {"id": subject, "version": "v1"}})
    roster = {"op": "count", "name": member, "source_set": family}
    value: Any = path["value"]
    for symbol, subject in reversed(tests):
        value = {"op": "choose",
                 "when": {"op": "compare", "left": {"op": "count", "name": symbol, "source_set": family},
                          "cmp": "lt", "right": copy.deepcopy(roster)},
                 "then": {"op": "block", "code": "DEPENDENCY_ABSENT", "missing": [subject]},
                 "else": value}
    path["value"] = value
    new["notes"] = (rule.get("notes") or "") + (" P0 scratch: when a test's answer is missing for a rostered child,"
                                                " the block names that answer's fact type (ADR 0086).")
    return new


def written(content: Path, variant: str) -> dict[str, dict[str, Any]]:
    out = questions(content)
    if variant == "g":
        for rule_id, name in COUNT_FILES.items():
            body = json.loads((content / name).read_text(encoding="utf-8"))
            assert body["id"] == rule_id and body["version"] == "v1"
            out[name.removesuffix(".json") + ".v2.json"] = guarded(body)
    return out


def dump(body: Any) -> str:
    return json.dumps(body, indent=2, ensure_ascii=False) + "\n"


if __name__ == "__main__":
    import sys
    for name, body in written(Path(sys.argv[1]), sys.argv[2] if len(sys.argv) > 2 else "g").items():
        print(name)
        print(dump(body)[:1500])
