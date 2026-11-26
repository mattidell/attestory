"""ADR 0087 and ADR 0090: one question per member, told apart by entry order (unit tests, no run).

The walk keys a member's question by the member's subject keys, not by its
recorded label (same-label-members), so two members both recorded as
"Demo Sam" who each miss an answer get one reason each. When another current
entity of the member's kind has the same label, each of its reasons carries
``memberOrdinal``, the member's 1-based place in the order the workspace
introduced them (same-label-ordinal, ADR 0090). Member reasons sort by label,
then ordinal, then sentence, so one person's questions sit together. A
member's question is never matched to another reason by sentence alone
(SLM-R3). Synthetic demo.* graphs from ``test_eic_child_answers_walk``.
"""
from __future__ import annotations

import copy
import unittest
from typing import Any

from packages.derivation.presentation_projection import (
    PresentationModelError,
    _finalize_question_references,
    _reasons_beside,
    _validate_resolved,
)
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
ALEX = "Demo Alex"
AGE_Q = "demo age question"
PARENT_Q = "demo parent question"


def _labels(*labels: str) -> Any:
    return _state(dict(zip(KIDS, labels)))


def _sam(ordinal: int, sentence: str = AGE_Q) -> dict[str, Any]:
    return {"sentence": sentence, "memberLabel": SAM, "memberOrdinal": ordinal}


def _missing_parent(kid: str) -> dict[str, list[dict[str, Any]]]:
    """The kid's tie-breaker result names the filer-is-parent answer, which it lacks."""
    return {f"{COUNTS}|{_key(kid)}": [_member_row(kid, COUNTS, "demo.rule.counts", CLEAR)],
            f"{CLEAR}|{_key(kid)}": [_member_row(kid, CLEAR, "demo.rule.clear", FILER_PARENT)]}


def _all_missing_age(*kids: str) -> dict[str, list[dict[str, Any]]]:
    return {k: v for kid in kids for k, v in _missing_age(kid).items()}


class SameLabelMembers(unittest.TestCase):
    def test_two_members_with_one_label_each_missing_the_answer_get_two_ordinal_reasons(self) -> None:
        by_symbol = _all_missing_age(*KIDS[:2])
        row = _line(by_symbol, *KIDS[:2])
        for later in (False, True):
            with self.subTest(later_any_arm_refs=later):
                self.assertEqual(_reasons(row, by_symbol, state=_labels(SAM, SAM), later_any_arm_refs=later),
                                 [_sam(1), _sam(2)])

    def test_three_members_with_one_label_get_three_ordinals(self) -> None:
        by_symbol = _all_missing_age(*KIDS)
        row = _line(by_symbol, *KIDS)
        self.assertEqual(_reasons(row, by_symbol, state=_labels(SAM, SAM, SAM)), [_sam(1), _sam(2), _sam(3)])

    def test_one_of_two_same_label_members_missing_says_which(self) -> None:
        for ordinal, missing in enumerate(KIDS[:2], start=1):
            with self.subTest(missing=missing):
                by_symbol = _missing_age(missing)
                row = _line(by_symbol, missing)
                self.assertEqual(_reasons(row, by_symbol, state=_labels(SAM, SAM)), [_sam(ordinal)])

    def test_two_same_label_members_missing_different_answers_say_which(self) -> None:
        by_symbol = {**_missing_parent(KIDS[0]), **_missing_age(KIDS[1])}
        row = _line(by_symbol, *KIDS[:2])
        self.assertEqual(_reasons(row, by_symbol, state=_labels(SAM, SAM)),
                         [_sam(1, PARENT_Q), _sam(2, AGE_Q)])

    def test_each_persons_questions_sit_together(self) -> None:
        # SLM-R4: sorted by label, then ordinal, then sentence.
        by_symbol: dict[str, list[dict[str, Any]]] = {}
        for kid in KIDS[:2]:
            by_symbol[f"{COUNTS}|{_key(kid)}"] = [_member_row(kid, COUNTS, "demo.rule.counts", "demo.child.age-met",
                                                              CLEAR)]
            by_symbol[f"{CLEAR}|{_key(kid)}"] = [_member_row(kid, CLEAR, "demo.rule.clear", FILER_PARENT)]
        row = _line(by_symbol, *KIDS[:2])
        self.assertEqual(_reasons(row, by_symbol, state=_labels(SAM, SAM)), [
            _sam(1, AGE_Q), _sam(1, PARENT_Q), _sam(2, AGE_Q), _sam(2, PARENT_Q),
        ])

    def test_two_of_three_sharing_a_label(self) -> None:
        by_symbol = _all_missing_age(*KIDS)
        row = _line(by_symbol, *KIDS)
        self.assertEqual(_reasons(row, by_symbol, state=_labels(SAM, ALEX, SAM)), [
            {"sentence": AGE_Q, "memberLabel": ALEX}, _sam(1), _sam(2),
        ])
        # Only the third member missing: it is the second "Demo Sam" added.
        third = _missing_age(KIDS[2])
        self.assertEqual(_reasons(_line(third, KIDS[2]), third, state=_labels(SAM, ALEX, SAM)), [_sam(2)])

    def test_distinct_labels_carry_no_ordinal(self) -> None:
        by_symbol = _all_missing_age(*KIDS[:2])
        row = _line(by_symbol, *KIDS[:2])
        self.assertEqual(_reasons(row, by_symbol, state=_labels(SAM, ALEX)), [
            {"sentence": AGE_Q, "memberLabel": ALEX},
            {"sentence": AGE_Q, "memberLabel": SAM},
        ])

    def test_a_same_label_entity_of_another_kind_is_not_counted(self) -> None:
        state = _labels(SAM, SAM)
        second = state.fact_state.entities[KIDS[1]]
        state.fact_state.entities[KIDS[1]] = EntityLifecycle({**second.entity, "kind": "demo.relative"}, "current")
        by_symbol = _all_missing_age(*KIDS[:2])
        row = _line(by_symbol, *KIDS[:2])
        self.assertEqual(_reasons(row, by_symbol, state=state), [{"sentence": AGE_Q, "memberLabel": SAM}] * 2)

    def test_a_superseded_same_label_entity_is_not_counted(self) -> None:
        state = _labels(SAM, SAM)
        first = state.fact_state.entities[KIDS[0]]
        state.fact_state.entities[KIDS[0]] = EntityLifecycle(first.entity, "superseded", "demo-child-9")
        by_symbol = _missing_age(KIDS[1])
        row = _line(by_symbol, KIDS[1])
        self.assertEqual(_reasons(row, by_symbol, state=state), [{"sentence": AGE_Q, "memberLabel": SAM}])

    def test_a_replaced_member_moves_to_the_end(self) -> None:
        # The first "Demo Sam" is corrected: its successor is introduced after the second.
        state = _labels(SAM, SAM)
        entities = state.fact_state.entities
        first = entities[KIDS[0]]
        entities[KIDS[0]] = EntityLifecycle(first.entity, "superseded", KIDS[2])
        entities[KIDS[2]] = EntityLifecycle({**first.entity, "id": KIDS[2]}, "current")
        by_symbol = _all_missing_age(KIDS[1], KIDS[2])
        row = _line(by_symbol, KIDS[1], KIDS[2])
        self.assertEqual(_reasons(row, by_symbol, state=state), [_sam(1), _sam(2)])
        replaced = _missing_age(KIDS[2])
        self.assertEqual(_reasons(_line(replaced, KIDS[2]), replaced, state=state), [_sam(2)])

    def test_the_same_member_reached_twice_is_asked_once(self) -> None:
        by_symbol = _missing_age(KIDS[0])
        row = _line(by_symbol, KIDS[0], KIDS[0])
        self.assertEqual(_reasons(row, by_symbol, state=_labels(SAM, SAM)), [_sam(1)])


class MemberReasonsAreNotMatchedBySentence(unittest.TestCase):
    """SLM-R3: a member's question is never merged with, or linked as, another reason by sentence."""

    SELECTION = [{"sentence": AGE_Q, "factId": "demo.fact.one"}, {"sentence": "demo selection reason"}]

    def test_a_member_reason_with_a_selection_sentence_is_kept(self) -> None:
        closure = [{"sentence": "demo closure question"}, _sam(1), _sam(2)]
        ordered, indices = _reasons_beside(self.SELECTION, closure)
        self.assertEqual(ordered, [
            {"sentence": AGE_Q, "factId": "demo.fact.one"},
            {"sentence": "demo closure question"},
            {"sentence": "demo selection reason"},
            _sam(1), _sam(2),
        ])
        self.assertEqual(indices, {"demo closure question": [1]})

    def test_a_plain_closure_question_is_still_not_repeated(self) -> None:
        ordered, indices = _reasons_beside(self.SELECTION, [{"sentence": AGE_Q}])
        self.assertEqual([r["sentence"] for r in ordered], [AGE_Q, "demo selection reason"])
        self.assertEqual(indices, {AGE_Q: []})

    def test_a_closure_question_index_never_points_at_a_member_reason(self) -> None:
        closure = [{"sentence": AGE_Q}, _sam(1)]
        ordered, indices = _reasons_beside([{"sentence": "demo selection reason"}], closure)
        self.assertEqual(ordered, [{"sentence": AGE_Q}, {"sentence": "demo selection reason"}, _sam(1)])
        self.assertEqual(indices[AGE_Q], [0])

    def test_without_member_reasons_the_order_is_unchanged(self) -> None:
        closure = [{"sentence": "demo b"}, {"sentence": "demo a"}]
        ordered, _ = _reasons_beside([{"sentence": "demo c"}], closure)
        self.assertEqual([r["sentence"] for r in ordered], ["demo a", "demo b", "demo c"])

    def test_a_question_reference_drops_a_member_reason_index(self) -> None:
        reasons = [{"sentence": AGE_Q}, _sam(1)]
        reference = {"groupId": "question-" + "0" * 64, "question": AGE_Q, "reasonIndices": [0, 1],
                     "scope": {"kind": "fact", "id": "demo.child.age"}}
        self.assertEqual(_finalize_question_references([reference], reasons)[0]["reasonIndices"], [0])
        only_member = dict(reference, reasonIndices=[1])
        self.assertEqual(_finalize_question_references([only_member], reasons), [])


class OrdinalValidator(unittest.TestCase):
    BLOCKED: dict[str, Any] = {"disposition": "blocked", "activeCodes": ["DEPENDENCY_ABSENT"], "act": None,
                               "reasons": [_sam(2)]}

    def test_an_ordinal_beside_a_label_is_admitted(self) -> None:
        _validate_resolved(self.BLOCKED, "demo")

    def test_a_bad_ordinal_is_refused(self) -> None:
        bad: Any
        for bad in (0, -1, True, 1.5, "2", None):
            resolved = copy.deepcopy(self.BLOCKED)
            resolved["reasons"][0]["memberOrdinal"] = bad
            with self.subTest(bad=bad), self.assertRaises(PresentationModelError):
                _validate_resolved(resolved, "demo")

    def test_an_ordinal_without_a_label_is_refused(self) -> None:
        resolved = copy.deepcopy(self.BLOCKED)
        del resolved["reasons"][0]["memberLabel"]
        with self.assertRaises(PresentationModelError):
            _validate_resolved(resolved, "demo")


if __name__ == "__main__":
    unittest.main()
