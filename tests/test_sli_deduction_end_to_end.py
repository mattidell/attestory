"""Plan sentence 8, told as one person's story.

A synthetic filer earns 50,000 in wages and paid 3,000 of student loan
interest to Cedar Servicing. Their Schedule 1 line 21 student loan interest
deduction is 2,500 (the worksheet's limit) when what they say supports it.
It blocks, with a sentence they can act on, when they correct or withdraw
what it rests on, and returns when they restore it.

Everything goes through the real path on one saved workspace: answers are
saved through the relationship recorder and its reviews, the log is recovered
fresh before every run, core calculations v41 is resolved through its
release, and ``live_coordinate_run`` produces line 21. The coordinator's own
marshalled context is also run on the reference runner, and both runners must
agree (Track 5's ``run_live``).

Every result is traced: a published line 21 is followed through its pins to
each answer the person gave and to the rule whose declared basis says what the
conclusion rests on. A blocked line 21 names the statement and the sentence.
Where a saved answer or withdrawal caused the block, the statement's standing
is followed to it.
"""
from __future__ import annotations

import json
import unittest
from typing import Any, Sequence
from unittest import mock

import pytest

from packages.kernel.act_log import ActLog
from packages.tax import sli_relationship_review as review_mod
import tests.test_sli_relationship_recording as track14
import tests.test_sli_track4_support_chain as T4
import tests.test_sli_track5_worksheet_integration as t5
from tests.test_sli_track7_interruption_safety import _Interrupted, interrupt_at

# Integration by construction: every step recovers a saved log and runs the
# whole core calculations package on both runners.
pytestmark = pytest.mark.live

USER = t5.USER
AT = "2026-10-03T14:00:00Z"
CEDAR = "2025 Form 1098-E from Cedar / Cedar Servicing"
SUPPORT_RULE = "tax.us.2025.rule.sli-statement-loan-support"
WORKSHEET_RULE = "tax.us.2025.rule.sli-worksheet"
QUESTION = {"loan": "loan-paid-only-school-costs", "enroll": "enrolled-at-least-half-time"}
ANSWER_TYPE = {"loan": T4.LOAN, "enroll": T4.ENROLL}

NO_LOAN_LINK = (f"{CEDAR}: No student loan is linked to this statement. "
                "Say which student loan this statement covers.")
NOT_ENROLLED = (f"{CEDAR}: You said the student was not enrolled at least half-time in a degree or certificate "
                "program during the schooling this loan paid for. The deduction is worked out here only when "
                "they were. If that answer is wrong, change it.")
ENROLLMENT_MISSING = (f"{CEDAR}: The loan on this statement has no answer yet to: was the student enrolled at least "
                      "half-time in a degree or certificate program during the schooling it paid for? Answer that "
                      "question. A missing answer is not treated as no.")
SCHOOLING_WITHDRAWN = (f"{CEDAR}: A link between the loan on this statement and a schooling was withdrawn and "
                       "not answered again. Say which schooling the loan paid for.")


class Person(t5.Return):
    """Track 5's synthetic return before any Form 1098-E is entered."""

    def __init__(self) -> None:
        super().__init__(wages=50000, amounts={})

    def enter_statement(self, amount: float) -> None:
        """Enter Cedar's Form 1098-E: box 2 first, then box 1."""
        keys = self.STATEMENT_KEYS["cedar"]
        track14._append_source(self.log, self.registry, t5.BOX2, keys, False, "track8-box2-cedar")
        self.statement_keys = {"cedar": keys}
        self.statement = {"cedar": track14._append_source(
            self.log, self.registry, t5.BOX1, keys, amount, "track8-box1-cedar")}

    def answer_id(self, question: str) -> str:
        return self.current_finding(ANSWER_TYPE[question], (("borrowing", self.borrowing["autumn"]),))

    def correct_answer(self, question: str, response: str) -> None:
        """Change the current answer to one of the two loan questions."""
        name = self._name(f"track8-correct-{question}-{response}")
        review = review_mod.prepare_borrowing_answer_review(
            self.log, self.registry, review_id=f"demo.track8.review.{name}", shown_at=AT,
            borrowing_refs=tuple(self.borrowing.values()))
        review_mod.correct_borrowing_answer_review(
            self.log, self.registry, review, finding_id=self.answer_id(question),
            borrowing_ref=self.borrowing["autumn"], question=QUESTION[question], response=response,
            actor=USER, at=AT, submission_id=f"demo.track8.submission.{name}",
            evidence_id=f"demo.evidence.track8.{name}")


def trace(outcome: t5.Outcome, finding: dict[str, Any]) -> tuple[set[str], set[str]]:
    """Follow a finding's pins through this run's publications.

    Returns the input findings it rests on, directly or through derived
    findings, and the rules that computed any step.
    """
    by_id = {pub.finding["id"]: pub.finding for pub in outcome.forward.publications}
    inputs: set[str] = set()
    rules: set[str] = set()
    pending = [finding]
    while pending:
        for pin in pending.pop()["pins"]:
            if pin["role"] == "computation":
                rules.add(pin["id"])
            elif pin["role"] == "input" and pin["id"] not in inputs:
                inputs.add(pin["id"])
                if pin["id"] in by_id:
                    pending.append(by_id[pin["id"]])
    return inputs, rules


class TheDeductionFollowsWhatThePersonSays(unittest.TestCase):

    def setUp(self) -> None:
        self.person = Person()
        self.addCleanup(self.person.raw.cleanup)
        self.step = 0

    def run_return(self) -> t5.Outcome:
        """Recover the saved log fresh and run the return; runners must agree."""
        self.step += 1
        return t5.run_live(self.person.acts(), f"demo.run.track8.story.{self.step:02d}")

    def standing(self, outcome: t5.Outcome) -> dict[str, Any]:
        standing: dict[str, Any] = T4.published(outcome.forward, t5.STANDING)[self.person.statement["cedar"]]
        return standing

    def assert_deducts(self, outcome: t5.Outcome, amount: int) -> None:
        self.assertEqual((outcome.line21["disposition"], outcome.value()), ("published_value", amount))
        self.assertNotIn("reasons", outcome.line21)
        self.assertEqual(self.standing(outcome)["value"], "none")
        finding = outcome.line21["act"]["finding"]
        self.assertIn({"role": "adoption", "id": "tax.us.2025.package.core-calculations", "version": "v41"},
                      finding["pins"])
        inputs, rules = trace(outcome, finding)
        ws = self.person
        said = {
            "statement box 1": ws.current_finding(t5.BOX1, ws.statement_keys["cedar"]),
            "loan paid for the schooling": ws.claims[("financing", "autumn", "autumn")],
            "statement covers the loan": ws.claims[("statement-inclusion", "autumn", "cedar")],
            "loan paid only school costs": ws.answer_id("loan"),
            "enrolled at least half-time": ws.answer_id("enroll"),
            **{tail: ws.current_finding(f"tax.us.2025.f1098e.{tail}", ws.statement_keys["cedar"])
               for tail in t5.COMMON},
        }
        for what, finding_id in said.items():
            self.assertIn(finding_id, inputs, f"line 21 does not trace to: {what}")
        self.assertTrue({WORKSHEET_RULE, t5.STANDING_RULE, SUPPORT_RULE} <= rules, rules)
        # The rule that concludes `plain-case-supported` declares what that
        # conclusion rests on beyond what was said: no finding carries it.
        basis = t5._load("rule.sli-statement-loan-support.json")["basis"]
        self.assertEqual(set(basis), {"said", "derived", "assumed", "left_with_person"})
        self.assertTrue(basis["assumed"] and basis["left_with_person"])

    def assert_blocks(self, outcome: t5.Outcome, reason: str, sentence: str,
                      because: Sequence[str] = ()) -> None:
        self.assertEqual(outcome.line21["disposition"], "blocked")
        self.assertNotIn("value", outcome.line21)
        self.assertEqual(t5.line21_text(outcome), [sentence])
        standing = self.standing(outcome)
        self.assertEqual(standing["value"], reason)
        inputs, _ = trace(outcome, standing)
        for finding_id in because:
            self.assertIn(finding_id, inputs, f"the {reason} standing does not trace to {finding_id}")

    def test_the_story(self) -> None:
        ws = self.person

        # No Form 1098-E yet: the family is closed and empty, line 21 is 0.
        empty = self.run_return()
        self.assertEqual((empty.line21["disposition"], empty.value()), ("closure_backed_zero", 0))

        # They enter Cedar's Form 1098-E. Nothing yet says which loan it covers.
        ws.enter_statement(3000.0)
        self.assert_blocks(self.run_return(), "no-loan-link", NO_LOAN_LINK)

        # They link the loan, its schooling and the statement, answer the two
        # loan questions and the four yes/no questions the statement keeps.
        ws.plain()
        self.assert_deducts(self.run_return(), 2500)

        # They correct the statement link: it does not cover that loan. With
        # no link left, the standing rests on the statement alone; it does not
        # pin the saved "no" (see the Track 8 report).
        ws.outcome("statement-inclusion", "autumn", "cedar", "no")
        self.assert_blocks(self.run_return(), "no-loan-link", NO_LOAN_LINK)

        # They restore it.
        ws.link("statement-inclusion", "autumn", "cedar", "yes")
        self.assert_deducts(self.run_return(), 2500)

        # They change their enrollment answer to no.
        ws.correct_answer("enroll", "no")
        self.assert_blocks(self.run_return(), "enrollment-no", NOT_ENROLLED, because=[ws.answer_id("enroll")])

        # They change it back to yes.
        ws.correct_answer("enroll", "yes")
        self.assert_deducts(self.run_return(), 2500)

        # They withdraw the link between the loan and its schooling.
        ws.outcome("financing", "autumn", "autumn", "withdrawn")
        withdrawal = ws.current_finding("tax.us.2025.sli.financing-withdrawn",
                                        (("borrowing", ws.borrowing["autumn"]), *ws.SCHOOL_KEYS["autumn"]))
        withdrawn = self.run_return()
        self.assert_blocks(withdrawn, "financing-withdrawn", SCHOOLING_WITHDRAWN, because=[withdrawal])

        # They restore it, and the save is interrupted partway through.
        before = ws.acts()
        sizes: list[int] = []
        real_batch = ActLog.append_batch

        def counted(log: ActLog, items: Sequence[dict[str, Any]], expected_revision: int) -> int:
            sizes.append(len(items))
            return real_batch(log, items, expected_revision)

        with mock.patch.object(ActLog, "append_batch", counted), \
                interrupt_at(lambda line: line == sizes[-1] // 2, torn=True), \
                self.assertRaises(_Interrupted):
            ws.link("financing", "autumn", "autumn", "yes")
        self.assertEqual(len(sizes), 1)
        self.assertGreater(sizes[0], 1, "the save wrote one act; nothing was interrupted midway")
        # Recovered fresh, none of the save is there and nothing is more
        # favorable than before it: the line is still blocked, for the same reason.
        self.assertEqual(ws.acts(), before)
        recovered = self.run_return()
        self.assert_blocks(recovered, "financing-withdrawn", SCHOOLING_WITHDRAWN, because=[withdrawal])
        self.assertEqual(json.dumps(recovered.line21, sort_keys=True).replace(recovered.model["runId"], ""),
                         json.dumps(withdrawn.line21, sort_keys=True).replace(withdrawn.model["runId"], ""))

        # They save it again. The withdrawal changed which schooling the loan
        # paid for, so it ended the enrollment answer given about that
        # schooling (ADR 0077 Part 2): they are asked it again.
        ws.link("financing", "autumn", "autumn", "yes")
        self.assert_blocks(self.run_return(), "enrollment-answer-missing", ENROLLMENT_MISSING)

        # They answer it again, and the deduction returns.
        ws.answer("enroll", "autumn", "yes")
        self.assert_deducts(self.run_return(), 2500)


if __name__ == "__main__":
    unittest.main()
