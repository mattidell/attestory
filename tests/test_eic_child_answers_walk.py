"""ADR 0087: the question walk follows a blocked roster member (unit tests, no run).

A roster count blocks ``DEPENDENCY_INVALID`` naming a member's subject key.
The walk follows the key to the member's own blocked rows, recorded under
``<subject-result symbol>|<subject fact id>``, and asks the member's missing
answers, each labelled with the member's recorded entity label. Synthetic
demo.* graphs shaped like the earned income credit roster on core v101.
"""
from __future__ import annotations

import copy
import unittest
from types import SimpleNamespace
from typing import Any

from packages.derivation.presentation_projection import (
    PresentationModelError,
    _closure_question_reasons,
    _RosterMembers,
    _validate_resolved,
)
from packages.kernel.facts import EntityLifecycle

ROSTER = "demo.child.relationship"  # the roster member fact type (the count's subject)
COUNTS = "demo.child.counts"  # the per-member result the count reads
AGE_MET = "demo.child.age-met"  # a per-member test published per subject of AGE
AGE = "demo.child.age"  # the answer the test's rule takes as its subject
CLEAR = "demo.child.tie-breaker-clear"  # a per-member result published per roster subject
FILER_PARENT = "demo.child.filer-is-parent"  # an answer a member row names directly
KIDS = ("demo-child-1", "demo-child-2")
QUESTIONS = {AGE: "demo age question", FILER_PARENT: "demo parent question"}


def _key(kid: str) -> str:
    return f"{ROSTER}|child={kid},tax-year=2025"


def _keyed(fact_type: str) -> dict[str, Any]:
    return {"id": fact_type, "identity_keys": [{"kind": "entity", "name": "child"},
                                              {"kind": "literal", "name": "tax-year"}]}


def _state(labels: dict[str, str] | None = None) -> Any:
    labels = {kid: f"Synthetic {kid}" for kid in KIDS} if labels is None else labels
    entities = {kid: EntityLifecycle({"schema": "entity.v1", "id": kid, "kind": "demo.child", "label": label},
                                     "current") for kid, label in labels.items()}
    fact_types = {fact: _keyed(fact) for fact in (ROSTER, AGE, FILER_PARENT)}
    fact_types["demo.return-answer"] = {"id": "demo.return-answer",
                                        "identity_keys": [{"kind": "literal", "name": "tax-year"}]}
    return SimpleNamespace(fact_state=SimpleNamespace(entities=entities, fact_types=fact_types))


RULES: dict[str, dict[str, Any]] = {
    "demo.rule.count": {"id": "demo.rule.count", "publishes": "demo.child-count",
                        "selection": {"paths": [{"id": "children", "reads_subject_results": [
                            {"symbol": COUNTS, "subject": {"id": ROSTER, "version": "v1"}}]}],
                                      "default": {"id": "neither", "reads_subject_results": []}}},
    "demo.rule.counts": {"id": "demo.rule.counts", "publishes": COUNTS, "subject": {"id": ROSTER, "version": "v1"}},
    "demo.rule.age-met": {"id": "demo.rule.age-met", "publishes": AGE_MET, "subject": {"id": AGE, "version": "v1"}},
    "demo.rule.clear": {"id": "demo.rule.clear", "publishes": CLEAR, "subject": {"id": ROSTER, "version": "v1"}},
}
MEMBERS = [{"schema": "input-question.v1", "fact_type": {"id": fact}, "question": question}
           for fact, question in QUESTIONS.items()]


def _count_row(*kids: str) -> dict[str, Any]:
    return {"disposition": "blocked", "code": "DEPENDENCY_INVALID", "artifact_id": "demo.rule.count",
            "missing": [_key(kid) for kid in kids]}


def _member_row(kid: str, symbol: str, artifact: str, *missing: str) -> dict[str, Any]:
    return {"disposition": "blocked", "code": "DEPENDENCY_ABSENT", "artifact_id": artifact,
            "symbol": f"{symbol}|{_key(kid)}", "missing": list(missing)}


def _line(by_symbol: dict[str, list[dict[str, Any]]], *kids: str) -> dict[str, Any]:
    """A page line blocked on the count, which blocks naming each kid's key."""
    by_symbol["demo.child-count"] = [_count_row(*kids)]
    return {"disposition": "blocked", "code": "DEPENDENCY_ABSENT", "artifact_id": "demo.rule.line",
            "missing": ["demo.child-count"]}


def _reasons(row: dict[str, Any], by_symbol: dict[str, list[dict[str, Any]]], *, state: Any = None,
             follow: bool = True, later_any_arm_refs: bool = False) -> list[dict[str, Any]]:
    members = _RosterMembers(RULES, _state() if state is None else state) if follow else None
    return _closure_question_reasons(row, resolved_members=MEMBERS, by_symbol=by_symbol,
                                     roster_members=members, later_any_arm_refs=later_any_arm_refs)


def _missing_age(kid: str) -> dict[str, list[dict[str, Any]]]:
    """The kid has no age answer: no age-met row of its own, and its counts row names age-met."""
    return {f"{COUNTS}|{_key(kid)}": [_member_row(kid, COUNTS, "demo.rule.counts", AGE_MET)]}


class MemberWalk(unittest.TestCase):
    def test_a_member_key_resolves_to_the_members_question_with_its_label(self) -> None:
        by_symbol = _missing_age(KIDS[0])
        row = _line(by_symbol, KIDS[0])
        for later in (False, True):
            with self.subTest(later_any_arm_refs=later):
                self.assertEqual(_reasons(row, by_symbol, later_any_arm_refs=later),
                                 [{"sentence": "demo age question", "member_label": "Synthetic demo-child-1"}])

    def test_a_member_row_naming_an_answer_directly_is_asked_for_that_member(self) -> None:
        kid = KIDS[1]
        by_symbol = {f"{COUNTS}|{_key(kid)}": [_member_row(kid, COUNTS, "demo.rule.counts", CLEAR)],
                     f"{CLEAR}|{_key(kid)}": [_member_row(kid, CLEAR, "demo.rule.clear", FILER_PARENT)]}
        row = _line(by_symbol, kid)
        self.assertEqual(_reasons(row, by_symbol),
                         [{"sentence": "demo parent question", "member_label": "Synthetic demo-child-2"}])

    def test_a_member_key_with_no_rows_leaves_the_line_silent(self) -> None:
        by_symbol: dict[str, list[dict[str, Any]]] = {}
        row = _line(by_symbol, KIDS[0])
        self.assertEqual(_reasons(row, by_symbol), [])
        # Rows of another member do not stand in for this one.
        by_symbol.update(_missing_age(KIDS[1]))
        self.assertEqual(_reasons(row, by_symbol), [])

    def test_two_members_each_missing_an_answer_get_two_labelled_reasons(self) -> None:
        by_symbol = {**_missing_age(KIDS[0]), **_missing_age(KIDS[1])}
        row = _line(by_symbol, *KIDS)
        self.assertEqual(_reasons(row, by_symbol), [
            {"sentence": "demo age question", "member_label": "Synthetic demo-child-1"},
            {"sentence": "demo age question", "member_label": "Synthetic demo-child-2"},
        ])
        # Different answers for different members: each member's own question.
        kid = KIDS[1]
        by_symbol[f"{COUNTS}|{_key(kid)}"] = [_member_row(kid, COUNTS, "demo.rule.counts", CLEAR)]
        by_symbol[f"{CLEAR}|{_key(kid)}"] = [_member_row(kid, CLEAR, "demo.rule.clear", FILER_PARENT)]
        self.assertEqual(_reasons(row, by_symbol), [
            {"sentence": "demo age question", "member_label": "Synthetic demo-child-1"},
            {"sentence": "demo parent question", "member_label": "Synthetic demo-child-2"},
        ])

    def test_one_member_missing_two_answers_is_asked_both(self) -> None:
        kid = KIDS[0]
        by_symbol = {f"{COUNTS}|{_key(kid)}": [_member_row(kid, COUNTS, "demo.rule.counts", AGE_MET, CLEAR)],
                     f"{CLEAR}|{_key(kid)}": [_member_row(kid, CLEAR, "demo.rule.clear", FILER_PARENT)]}
        row = _line(by_symbol, kid)
        self.assertEqual([r["sentence"] for r in _reasons(row, by_symbol)],
                         ["demo age question", "demo parent question"])

    def test_every_root_must_have_a_question(self) -> None:
        # One member answerable, the other missing an answer with no question: nothing is attached.
        kid = KIDS[1]
        by_symbol = {**_missing_age(KIDS[0]),
                     f"{COUNTS}|{_key(kid)}": [_member_row(kid, COUNTS, "demo.rule.counts", "demo.child.unasked")]}
        row = _line(by_symbol, *KIDS)
        self.assertEqual(_reasons(row, by_symbol), [])

    def test_an_existing_age_row_is_not_read_as_a_missing_age(self) -> None:
        kid = KIDS[0]
        by_symbol = _missing_age(kid)
        by_symbol[f"{AGE_MET}|{AGE}|child={kid},tax-year=2025"] = [
            {"disposition": "published", "artifact_id": "demo.rule.age-met"}]
        row = _line(by_symbol, kid)
        self.assertEqual(_reasons(row, by_symbol), [])

    def test_a_return_level_answer_reached_from_a_member_is_not_labelled(self) -> None:
        kid = KIDS[0]
        members = [*MEMBERS, {"schema": "input-question.v1", "fact_type": {"id": "demo.return-answer"},
                              "question": "demo return question"}]
        by_symbol = {f"{COUNTS}|{_key(kid)}": [_member_row(kid, COUNTS, "demo.rule.counts", "demo.return-answer")]}
        row = _line(by_symbol, kid)
        got = _closure_question_reasons(row, resolved_members=members, by_symbol=by_symbol,
                                        roster_members=_RosterMembers(RULES, _state()))
        self.assertEqual(got, [{"sentence": "demo return question"}])

    def test_a_member_with_no_recorded_label_leaves_the_line_silent(self) -> None:
        by_symbol = _missing_age(KIDS[0])
        row = _line(by_symbol, KIDS[0])
        self.assertEqual(_reasons(row, by_symbol, state=_state({})), [])

    def test_without_roster_members_the_walk_is_the_earlier_one(self) -> None:
        by_symbol = _missing_age(KIDS[0])
        row = _line(by_symbol, KIDS[0])
        self.assertEqual(_reasons(row, by_symbol, follow=False), [])

    def test_a_count_whose_rule_reads_no_member_results_is_not_followed(self) -> None:
        by_symbol = _missing_age(KIDS[0])
        row = _line(by_symbol, KIDS[0])
        by_symbol["demo.child-count"][0]["artifact_id"] = "demo.rule.counts"
        self.assertEqual(_reasons(row, by_symbol), [])

    def test_an_unclosed_roster_row_is_not_followed(self) -> None:
        by_symbol = _missing_age(KIDS[0])
        row = _line(by_symbol, KIDS[0])
        by_symbol["demo.child-count"][0]["code"] = "SOURCE_SET_UNCLOSED"
        self.assertEqual(_reasons(row, by_symbol, later_any_arm_refs=True), [])


class ReasonValidator(unittest.TestCase):
    BLOCKED = {"disposition": "blocked", "activeCodes": ["DEPENDENCY_ABSENT"], "act": None,
               "reasons": [{"sentence": "demo age question", "member_label": "Synthetic demo-child-1"}]}

    def test_a_member_label_is_admitted(self) -> None:
        _validate_resolved(self.BLOCKED, "demo")

    def test_a_malformed_member_label_is_refused(self) -> None:
        for bad in ("", 3, None, {"name": "x"}):
            resolved = copy.deepcopy(self.BLOCKED)
            resolved["reasons"][0]["member_label"] = bad
            with self.subTest(bad=bad), self.assertRaises(PresentationModelError):
                _validate_resolved(resolved, "demo")


if __name__ == "__main__":
    unittest.main()
