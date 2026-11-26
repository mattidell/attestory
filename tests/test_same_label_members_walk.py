"""ADR 0087: one question per member, even when members share a recorded label (unit tests, no run).

same-label-members Track 1. The walk keys a member's question by the member's
subject keys, not by its recorded label, so two members both recorded as
"Demo Sam" who each miss an answer get one reason each. Telling them apart
(an ordinal) is not part of this track. Synthetic demo.* graphs from
``test_eic_child_answers_walk``.
"""
from __future__ import annotations

import unittest
from typing import Any

from packages.kernel.facts import EntityLifecycle
from tests.test_eic_child_answers_walk import (
    CLEAR,
    COUNTS,
    FILER_PARENT,
    _key,
    _line,
    _member_row,
    _missing_age,
    _reasons,
    _state,
)

KIDS = ("demo-child-1", "demo-child-2", "demo-child-3")
SAM = "Demo Sam"
AGE_Q = "demo age question"
PARENT_Q = "demo parent question"


def _labels(*labels: str) -> Any:
    return _state(dict(zip(KIDS, labels)))


def _missing_parent(kid: str) -> dict[str, list[dict[str, Any]]]:
    """The kid's tie-breaker result names the filer-is-parent answer, which it lacks."""
    return {f"{COUNTS}|{_key(kid)}": [_member_row(kid, COUNTS, "demo.rule.counts", CLEAR)],
            f"{CLEAR}|{_key(kid)}": [_member_row(kid, CLEAR, "demo.rule.clear", FILER_PARENT)]}


class SameLabelMembers(unittest.TestCase):
    def test_two_members_with_one_label_each_missing_the_answer_get_two_reasons(self) -> None:
        by_symbol = {**_missing_age(KIDS[0]), **_missing_age(KIDS[1])}
        row = _line(by_symbol, KIDS[0], KIDS[1])
        for later in (False, True):
            with self.subTest(later_any_arm_refs=later):
                self.assertEqual(_reasons(row, by_symbol, state=_labels(SAM, SAM), later_any_arm_refs=later), [
                    {"sentence": AGE_Q, "memberLabel": SAM},
                    {"sentence": AGE_Q, "memberLabel": SAM},
                ])

    def test_three_members_with_one_label_get_three_reasons(self) -> None:
        by_symbol = {k: v for kid in KIDS for k, v in _missing_age(kid).items()}
        row = _line(by_symbol, *KIDS)
        self.assertEqual(_reasons(row, by_symbol, state=_labels(SAM, SAM, SAM)),
                         [{"sentence": AGE_Q, "memberLabel": SAM}] * 3)

    def test_one_of_two_same_label_members_missing_gets_one_reason(self) -> None:
        for missing in KIDS[:2]:
            with self.subTest(missing=missing):
                by_symbol = _missing_age(missing)
                row = _line(by_symbol, missing)
                self.assertEqual(_reasons(row, by_symbol, state=_labels(SAM, SAM)),
                                 [{"sentence": AGE_Q, "memberLabel": SAM}])

    def test_two_same_label_members_missing_different_answers_get_each_question(self) -> None:
        by_symbol = {**_missing_age(KIDS[0]), **_missing_parent(KIDS[1])}
        row = _line(by_symbol, KIDS[0], KIDS[1])
        self.assertEqual(_reasons(row, by_symbol, state=_labels(SAM, SAM)), [
            {"sentence": AGE_Q, "memberLabel": SAM},
            {"sentence": PARENT_Q, "memberLabel": SAM},
        ])

    def test_two_same_label_members_each_missing_two_answers_get_four_reasons(self) -> None:
        by_symbol: dict[str, list[dict[str, Any]]] = {}
        for kid in KIDS[:2]:
            by_symbol[f"{COUNTS}|{_key(kid)}"] = [_member_row(kid, COUNTS, "demo.rule.counts", "demo.child.age-met",
                                                              CLEAR)]
            by_symbol[f"{CLEAR}|{_key(kid)}"] = [_member_row(kid, CLEAR, "demo.rule.clear", FILER_PARENT)]
        row = _line(by_symbol, KIDS[0], KIDS[1])
        self.assertEqual(_reasons(row, by_symbol, state=_labels(SAM, SAM)), [
            {"sentence": AGE_Q, "memberLabel": SAM},
            {"sentence": AGE_Q, "memberLabel": SAM},
            {"sentence": PARENT_Q, "memberLabel": SAM},
            {"sentence": PARENT_Q, "memberLabel": SAM},
        ])

    def test_two_of_three_sharing_a_label(self) -> None:
        by_symbol = {k: v for kid in KIDS for k, v in _missing_age(kid).items()}
        row = _line(by_symbol, *KIDS)
        self.assertEqual(_reasons(row, by_symbol, state=_labels(SAM, "Demo Alex", SAM)), [
            {"sentence": AGE_Q, "memberLabel": "Demo Alex"},
            {"sentence": AGE_Q, "memberLabel": SAM},
            {"sentence": AGE_Q, "memberLabel": SAM},
        ])

    def test_distinct_labels_are_unchanged(self) -> None:
        by_symbol = {**_missing_age(KIDS[0]), **_missing_age(KIDS[1])}
        row = _line(by_symbol, KIDS[0], KIDS[1])
        self.assertEqual(_reasons(row, by_symbol, state=_labels(SAM, "Demo Alex")), [
            {"sentence": AGE_Q, "memberLabel": "Demo Alex"},
            {"sentence": AGE_Q, "memberLabel": SAM},
        ])

    def test_a_same_label_member_of_another_kind_is_its_own_member(self) -> None:
        state = _labels(SAM, SAM)
        second = state.fact_state.entities[KIDS[1]]
        state.fact_state.entities[KIDS[1]] = EntityLifecycle({**second.entity, "kind": "demo.relative"}, "current")
        by_symbol = {**_missing_age(KIDS[0]), **_missing_age(KIDS[1])}
        row = _line(by_symbol, KIDS[0], KIDS[1])
        self.assertEqual(_reasons(row, by_symbol, state=state), [{"sentence": AGE_Q, "memberLabel": SAM}] * 2)

    def test_the_same_member_reached_twice_is_asked_once(self) -> None:
        # Both count rows name the one member: still one reason for it.
        by_symbol = _missing_age(KIDS[0])
        row = _line(by_symbol, KIDS[0], KIDS[0])
        self.assertEqual(_reasons(row, by_symbol, state=_labels(SAM, SAM)), [{"sentence": AGE_Q, "memberLabel": SAM}])

    def test_no_reason_carries_more_than_sentence_and_label(self) -> None:
        by_symbol = {**_missing_age(KIDS[0]), **_missing_age(KIDS[1])}
        row = _line(by_symbol, KIDS[0], KIDS[1])
        for reason in _reasons(row, by_symbol, state=_labels(SAM, SAM)):
            self.assertEqual(set(reason), {"sentence", "memberLabel"})


if __name__ == "__main__":
    unittest.main()
