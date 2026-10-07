"""Track 1a: the line 21 explanation block saved with the presentation.

Every case runs through the real path (``Return``/``run_live`` from
``tests.test_sli_track5_worksheet_integration``, which drives
``live_coordinate_run``) and asserts on the
``line21Explanation`` block of the presentation reloaded from disk. No case
hand-builds a presentation model.
"""

from __future__ import annotations

import unittest
from typing import Any

import tests.test_sli_track5_worksheet_integration as t5
from packages.tax.sli_relationship_recording import record_borrowing_answer_durably
from packages.derivation.presentation_projection import PresentationModelError, _validate_line21_explanation

SUPPORT_RULE_ID = "tax.us.2025.rule.sli-statement-loan-support"


def _rows_by_lender(outcome: t5.Outcome) -> dict[str, dict[str, Any]]:
    block = outcome.model.get("line21Explanation")
    assert block is not None, "expected a line21Explanation block"
    return {row["statementLabel"]["lender"]: row for row in block["rows"]}


def _finding_fact_ids(ws: t5.Return) -> dict[str, str]:
    """Each recorded finding's fact id, read from the saved acts themselves."""
    found: dict[str, str] = {}
    for row in ws.acts():
        finding = (row.get("payload") or {}).get("finding")
        if isinstance(finding, dict) and "id" in finding and "fact_id" in finding:
            found[finding["id"]] = finding["fact_id"]
    return found


def _assert_answers_belong_to(test: unittest.TestCase, ws: t5.Return, row: dict[str, Any],
                              statement: str, borrowing: str) -> None:
    """Every answer on the row names the row's own loan, and its inclusion names the row's statement."""
    fact_ids = _finding_fact_ids(ws)
    own_borrowing = f"borrowing={ws.borrowing[borrowing]}"
    own_statement = f"statement={dict(ws.statement_keys[statement])['statement']}"
    for answer in row["basis"]["answers"]:
        fact_id = fact_ids[answer["findingId"]]
        test.assertIn(own_borrowing, fact_id)
        if answer["factType"] == "tax.us.2025.sli.statement-inclusion-relationship":
            test.assertIn(own_statement, fact_id)


def _assert_reasons_belong_to(test: unittest.TestCase, ws: t5.Return, outcome: t5.Outcome,
                              row: dict[str, Any], statement: str) -> None:
    """Every reason the row links to names the row's own statement by identity."""
    keys = dict(ws.statement_keys[statement])
    reasons = outcome.line21["reasons"]
    for index in row["status"]["reasonIndices"]:
        fact_id = reasons[index]["factId"]
        test.assertIn(f"lender={keys['lender']}", fact_id)
        test.assertIn(f"statement={keys['statement']}", fact_id)


class C1PlainSupported(unittest.TestCase):
    def test_one_statement_shows_amount_basis_and_working(self) -> None:
        ws = t5.Return(wages=50000, amounts={"cedar": 3000.0})
        with ws.raw:
            ws.plain()
            outcome = t5.run_live(ws.acts(), "demo.run.t1a.c1")
            block = outcome.model["line21Explanation"]
            self.assertEqual(block["schema"], "line21-explanation.v1")
            self.assertEqual(block["runId"], outcome.model["runId"])
            self.assertIsInstance(block["workspaceRevision"], int)

            [row] = block["rows"]
            self.assertEqual(row["statementLabel"]["lender"], "Cedar Servicing")
            self.assertEqual(row["loans"], ["Autumn study loan"])
            self.assertEqual(row["amount"], 3000)
            self.assertEqual(row["status"], {"kind": "no-reason"})
            self.assertEqual(row["support"], "plain-case-supported")
            self.assertEqual(row["standing"], "none")

            basis = row["basis"]
            self.assertEqual(basis["ruleId"], SUPPORT_RULE_ID)
            self.assertEqual(len(basis["assumed"]), 5)
            self.assertEqual(len(basis["leftWithPerson"]), 4)
            answers = basis["answers"]
            self.assertEqual(len(answers), 4)
            self.assertEqual({a["factType"] for a in answers}, {
                "tax.us.2025.sli.financing-relationship",
                "tax.us.2025.sli.statement-inclusion-relationship",
                "tax.us.2025.sli.loan-paid-only-school-costs",
                "tax.us.2025.sli.enrolled-at-least-half-time",
            })
            for answer in answers:
                self.assertTrue(answer["proposition"])
                self.assertTrue(answer["response"])

            working = block["working"]
            self.assertEqual(working["lineOneSubtotal"], 3000)
            self.assertEqual(working["totalIncome"], 50000)
            self.assertEqual(working["value"], 2500)
            self.assertEqual(
                {p["id"] for p in working["parameters"]},
                {
                    "tax.us.2025.parameter.sli-interest-cap",
                    "tax.us.2025.parameter.sli-magi-phase-range",
                    "tax.us.2025.parameter.sli-magi-threshold",
                },
            )


class C10OldPathOnly(unittest.TestCase):
    def test_old_only_workspace_has_no_basis_but_shows_working(self) -> None:
        ws = t5.Return(wages=50000, amounts={"cedar": 3000.0})
        with ws.raw:
            ws.old_answers("cedar")
            outcome = t5.run_live(ws.acts(), "demo.run.t1a.c10")
            [row] = outcome.model["line21Explanation"]["rows"]
            self.assertEqual(row["status"], {"kind": "no-reason"})
            self.assertEqual(row["amount"], 3000)
            self.assertEqual(row["support"], "not-supported")
            self.assertNotIn("basis", row)
            self.assertEqual(outcome.model["line21Explanation"]["working"]["value"], 2500)


class MissingQuestionWording(unittest.TestCase):
    def test_recorder_context_gap_stays_local_to_one_statement(self) -> None:
        ws = t5.Return(amounts={"cedar": 1500.0, "birch": 800.0})
        with ws.raw:
            ws.link("financing", "autumn", "autumn")
            ws.link("statement-inclusion", "autumn", "cedar")
            record_borrowing_answer_durably(
                ws.log, ws.registry, question="loan-paid-only-school-costs",
                borrowing_ref=ws.borrowing["autumn"], response="yes",
                submission_id="demo.track2.no-wording.loan-cost",
                evidence_id="demo.evidence.track2.no-wording.loan-cost",
                actor=t5.USER, at="2026-10-04T10:00:00Z", recognition_context=None,
            )
            ws.answer("enroll", "autumn", "yes")
            ws.common_answers("cedar")
            ws.plain("spring", "spring", "birch")
            outcome = t5.run_live(ws.acts(), "demo.run.track2.missing-wording")
            rows = _rows_by_lender(outcome)
            cedar, birch = rows["Cedar Servicing"], rows["Birch Servicing"]
            cedar_missing = next(a for a in cedar["basis"]["answers"]
                                 if a["factType"] == "tax.us.2025.sli.loan-paid-only-school-costs")
            self.assertEqual(cedar_missing["response"], "yes")
            self.assertTrue(cedar_missing["findingId"])
            self.assertNotIn("proposition", cedar_missing)
            self.assertTrue(all(a.get("proposition") for a in birch["basis"]["answers"]))
            self.assertEqual(cedar["amount"], 1500)
            self.assertEqual(birch["amount"], 800)
            working = outcome.model["line21Explanation"]["working"]
            self.assertEqual((working["lineOneSubtotal"], working["value"]), (2300, 2300))

    def test_validator_allows_absent_but_rejects_invalid_present_proposition(self) -> None:
        block: dict[str, Any] = {
            "schema": "line21-explanation.v1", "runId": "demo.run.validator",
            "workspaceRevision": 1, "rows": [{
                "statementLabel": {"lender": "Demo Lender"}, "loans": [],
                "status": {"kind": "no-reason"}, "basis": {
                    "ruleId": "demo.rule", "ruleVersion": "v1", "assumed": [],
                    "leftWithPerson": [], "answers": [{"findingId": "demo.finding",
                        "factType": "demo.fact-type", "response": "yes", "proposition": "Asked text"}],
                },
            }],
        }
        answer = block["rows"][0]["basis"]["answers"][0]
        del answer["proposition"]
        _validate_line21_explanation(block)
        answer["proposition"] = ""
        with self.assertRaises(PresentationModelError):
            _validate_line21_explanation(block)


class R1RetainedAnswerMissing(unittest.TestCase):
    def test_supported_but_blocked_shows_no_basis(self) -> None:
        ws = t5.Return()
        with ws.raw:
            ws.link("financing", "autumn", "autumn")
            ws.link("statement-inclusion", "autumn", "cedar")
            ws.answer("loan", "autumn", "yes")
            ws.answer("enroll", "autumn", "yes")
            ws.common_answers("cedar", skip=("no-related-person-interest",))
            outcome = t5.run_live(ws.acts(), "demo.run.t1a.r1")
            self.assertEqual(outcome.line21["disposition"], "blocked")
            [row] = outcome.model["line21Explanation"]["rows"]
            self.assertEqual(row["support"], "plain-case-supported")
            self.assertEqual(row["status"]["kind"], "named-by-reason")
            self.assertNotIn("basis", row)
            self.assertNotIn("working", outcome.model["line21Explanation"])


class C8RemovedStatementBesideSupported(unittest.TestCase):
    def test_removed_statement_is_named_with_no_amount(self) -> None:
        ws = t5.Return(amounts={"cedar": 1500.0, "birch": 800.0})
        with ws.raw:
            ws.plain()
            ws.plain("spring", "spring", "birch")
            ws.retract_source(ws.statement["cedar"])
            outcome = t5.run_live(ws.acts(), "demo.run.t1a.c8")
            self.assertEqual(outcome.line21["disposition"], "blocked")
            rows = _rows_by_lender(outcome)
            cedar, birch = rows["Cedar Servicing"], rows["Birch Servicing"]
            self.assertEqual(cedar["status"]["kind"], "named-by-reason")
            self.assertNotIn("amount", cedar)
            self.assertNotIn("basis", cedar)
            self.assertEqual(birch["status"], {"kind": "no-reason"})
            self.assertEqual(birch["amount"], 800)
            self.assertIn("basis", birch)


class C3TwoSupportedStatements(unittest.TestCase):
    def test_each_statement_has_its_own_amount_and_answers(self) -> None:
        ws = t5.Return(amounts={"cedar": 1500.0, "birch": 800.0})
        with ws.raw:
            ws.plain()
            ws.plain("spring", "spring", "birch")
            outcome = t5.run_live(ws.acts(), "demo.run.t1a.c3")
            rows = _rows_by_lender(outcome)
            cedar, birch = rows["Cedar Servicing"], rows["Birch Servicing"]
            self.assertEqual(cedar["amount"], 1500)
            self.assertEqual(birch["amount"], 800)
            self.assertEqual(cedar["amount"] + birch["amount"],
                              outcome.model["line21Explanation"]["working"]["lineOneSubtotal"])
            cedar_findings = {a["findingId"] for a in cedar["basis"]["answers"]}
            birch_findings = {a["findingId"] for a in birch["basis"]["answers"]}
            self.assertEqual(cedar_findings & birch_findings, set())
            _assert_answers_belong_to(self, ws, cedar, "cedar", "autumn")
            _assert_answers_belong_to(self, ws, birch, "birch", "spring")


class M1TwoStatementsOneLoan(unittest.TestCase):
    def test_both_rows_named_by_reason_show_the_same_loan(self) -> None:
        ws = t5.Return(amounts={"cedar": 1500.0, "birch": 800.0})
        with ws.raw:
            ws.link("financing", "autumn", "autumn")
            ws.link("statement-inclusion", "autumn", "cedar")
            ws.link("statement-inclusion", "autumn", "birch")
            ws.answer("loan", "autumn", "yes")
            ws.answer("enroll", "autumn", "no")
            ws.common_answers("cedar")
            ws.common_answers("birch")
            outcome = t5.run_live(ws.acts(), "demo.run.t1a.m1")
            self.assertEqual(outcome.line21["disposition"], "blocked")
            rows = _rows_by_lender(outcome)
            cedar, birch = rows["Cedar Servicing"], rows["Birch Servicing"]
            self.assertEqual(cedar["status"]["kind"], "named-by-reason")
            self.assertEqual(birch["status"]["kind"], "named-by-reason")
            self.assertEqual(cedar["loans"], ["Autumn study loan"])
            self.assertEqual(birch["loans"], ["Autumn study loan"])
            self.assertNotIn("basis", cedar)
            self.assertNotIn("basis", birch)


class C4C5EnrollmentMissingOrNo(unittest.TestCase):
    def test_missing_enrollment_answer_is_named_by_reason(self) -> None:
        ws = t5.Return()
        with ws.raw:
            ws.link("financing", "autumn", "autumn")
            ws.link("statement-inclusion", "autumn", "cedar")
            ws.answer("loan", "autumn", "yes")
            ws.common_answers("cedar")
            outcome = t5.run_live(ws.acts(), "demo.run.t1a.c4")
            [row] = outcome.model["line21Explanation"]["rows"]
            self.assertEqual(row["status"]["kind"], "named-by-reason")
            self.assertNotIn("basis", row)
            self.assertNotIn("working", outcome.model["line21Explanation"])

    def test_explicit_no_enrollment_is_named_by_reason(self) -> None:
        ws = t5.Return()
        with ws.raw:
            ws.link("financing", "autumn", "autumn")
            ws.link("statement-inclusion", "autumn", "cedar")
            ws.answer("loan", "autumn", "yes")
            ws.answer("enroll", "autumn", "no")
            ws.common_answers("cedar")
            outcome = t5.run_live(ws.acts(), "demo.run.t1a.c5")
            [row] = outcome.model["line21Explanation"]["rows"]
            self.assertEqual(row["status"]["kind"], "named-by-reason")
            self.assertNotIn("basis", row)
            self.assertNotIn("working", outcome.model["line21Explanation"])


class C6InclusionCorrectedToNo(unittest.TestCase):
    def test_no_loan_link_and_no_basis(self) -> None:
        ws = t5.Return()
        with ws.raw:
            ws.plain()
            ws.outcome("statement-inclusion", "autumn", "cedar", "no")
            outcome = t5.run_live(ws.acts(), "demo.run.t1a.c6")
            [row] = outcome.model["line21Explanation"]["rows"]
            self.assertEqual(row["status"]["kind"], "named-by-reason")
            self.assertEqual(row["loans"], [])
            self.assertNotIn("basis", row)


class R2BothPathsPresent(unittest.TestCase):
    def test_both_present_refusal_is_named_by_reason_with_no_basis(self) -> None:
        ws = t5.Return()
        with ws.raw:
            ws.plain()
            ws.old_answers("cedar", skip=t5.COMMON)
            outcome = t5.run_live(ws.acts(), "demo.run.t1a.r2")
            self.assertEqual(outcome.line21["disposition"], "blocked")
            [row] = outcome.model["line21Explanation"]["rows"]
            self.assertEqual(row["support"], "plain-case-supported")
            self.assertEqual(row["status"]["kind"], "named-by-reason")
            self.assertNotIn("basis", row)


class R3TwoStatementsBothPathsPresent(unittest.TestCase):
    """Two statements each with both old and new inputs must each name their
    own reason, not both fall to ``no-reason`` with a wrongly shown basis."""

    def test_both_rows_named_by_reason_with_no_basis(self) -> None:
        ws = t5.Return(amounts={"cedar": 1500.0, "birch": 800.0})
        with ws.raw:
            ws.plain()
            ws.plain("spring", "spring", "birch")
            ws.old_answers("cedar", skip=t5.COMMON)
            ws.old_answers("birch", skip=t5.COMMON)
            outcome = t5.run_live(ws.acts(), "demo.run.t1a.r3")
            self.assertEqual(outcome.line21["disposition"], "blocked")
            rows = _rows_by_lender(outcome)
            cedar, birch = rows["Cedar Servicing"], rows["Birch Servicing"]
            self.assertEqual(cedar["support"], "plain-case-supported")
            self.assertEqual(birch["support"], "plain-case-supported")
            self.assertEqual(cedar["status"]["kind"], "named-by-reason")
            self.assertEqual(birch["status"]["kind"], "named-by-reason")
            self.assertNotIn("basis", cedar)
            self.assertNotIn("basis", birch)
            # Each row names its own reason; neither borrows the other's.
            reasons = outcome.line21["reasons"]
            self.assertEqual(len(reasons), 2)
            self.assertNotEqual(cedar["status"]["reasonIndices"], birch["status"]["reasonIndices"])
            _assert_reasons_belong_to(self, ws, outcome, cedar, "cedar")
            _assert_reasons_belong_to(self, ws, outcome, birch, "birch")


class R4IdenticalLabelsStayDistinct(unittest.TestCase):
    """Two distinct statements whose recorded labels read identically must
    not be merged by the refusal's reason matching, which is identity-only
    and must never fall back to the display label."""

    def test_distinct_statements_sharing_a_label_are_not_merged(self) -> None:
        import tests.test_sli_relationship_recording as track14
        from packages.kernel.facts import fact_id_for
        from tests.support import act, demo_entity

        ws = t5.Return(amounts={})
        with ws.raw:
            def add_entity(entity_id: str, label: str, kind: str) -> None:
                revision = ws.log.read().revision
                ws.log.append(act(revision, "entity-introduced",
                                  {"entity": demo_entity(entity_id, label, kind)}),
                              expected_revision=revision)

            add_entity("demo.track2.lender.twin1", "Twin Lender", "tax.us.student-loan-lender")
            add_entity("demo.track2.statement.twin1", "Twin Statement", "tax.us.1098e-statement")
            add_entity("demo.track2.lender.twin2", "Twin Lender", "tax.us.student-loan-lender")
            add_entity("demo.track2.statement.twin2", "Twin Statement", "tax.us.1098e-statement")

            keys1 = (("lender", "demo.track2.lender.twin1"), ("statement", "demo.track2.statement.twin1"),
                     ("tax-year", "2025"))
            keys2 = (("lender", "demo.track2.lender.twin2"), ("statement", "demo.track2.statement.twin2"),
                     ("tax-year", "2025"))
            for name, keys, amount in (("twin1", keys1, 1100.0), ("twin2", keys2, 1300.0)):
                track14._append_source(ws.log, ws.registry, t5.BOX2, keys, False, f"track2-box2-{name}")
                track14._append_source(ws.log, ws.registry, t5.BOX1, keys, amount, f"track2-box1-{name}")
                ws.statement_keys[name] = keys
                ws.statement[name] = fact_id_for(t5.BOX1, keys)

            ws.link("financing", "autumn", "autumn")
            ws.link("statement-inclusion", "autumn", "twin1")
            ws.answer("loan", "autumn", "yes")
            ws.answer("enroll", "autumn", "yes")
            ws.common_answers("twin1")
            ws.old_answers("twin1", skip=t5.COMMON)

            ws.link("financing", "spring", "spring")
            ws.link("statement-inclusion", "spring", "twin2")
            ws.answer("loan", "spring", "yes")
            ws.answer("enroll", "spring", "yes")
            ws.common_answers("twin2")
            ws.old_answers("twin2", skip=t5.COMMON)

            outcome = t5.run_live(ws.acts(), "demo.run.t1a.r4")
            self.assertEqual(outcome.line21["disposition"], "blocked")
            rows = outcome.model["line21Explanation"]["rows"]
            self.assertEqual(len(rows), 2)
            self.assertEqual({row["statementLabel"]["lender"] for row in rows}, {"Twin Lender"})
            self.assertEqual({row["statementLabel"]["statement"] for row in rows}, {"Twin Statement"})

            # Identical labels; distinguish rows by their own loans instead.
            by_loan = {tuple(row["loans"]): row for row in rows}
            self.assertEqual(set(by_loan), {("Autumn study loan",), ("Spring study loan",)})
            for row in rows:
                self.assertEqual(row["status"]["kind"], "named-by-reason")
                self.assertNotIn("basis", row)

            reasons = outcome.line21["reasons"]
            self.assertEqual(len(reasons), 2)
            autumn_row = by_loan[("Autumn study loan",)]
            spring_row = by_loan[("Spring study loan",)]
            self.assertNotEqual(autumn_row["status"]["reasonIndices"], spring_row["status"]["reasonIndices"])
            _assert_reasons_belong_to(self, ws, outcome, autumn_row, "twin1")
            _assert_reasons_belong_to(self, ws, outcome, spring_row, "twin2")


class C9ReplayMarkerBesideSupported(unittest.TestCase):
    def test_marked_statement_shows_the_current_pinned_amount(self) -> None:
        ws = t5.Return(amounts={"cedar": 1500.0, "birch": 800.0})
        with ws.raw:
            ws.plain()
            ws.unscoped_rewrite("cedar", 1800.0)
            ws.plain("spring", "spring", "birch")
            outcome = t5.run_live(ws.acts(), "demo.run.t1a.c9")
            self.assertEqual(outcome.line21["disposition"], "blocked")
            rows = _rows_by_lender(outcome)
            cedar, birch = rows["Cedar Servicing"], rows["Birch Servicing"]
            self.assertEqual(cedar["status"]["kind"], "named-by-reason")
            # Never the stale 1500; the current, rewritten amount the line 1
            # subtotal actually pins (review 0c F8).
            self.assertEqual(cedar["amount"], 1800)
            self.assertNotIn("basis", cedar)
            self.assertEqual(birch["status"], {"kind": "no-reason"})
            self.assertIn("basis", birch)


class Z1ClaimedAsDependent(unittest.TestCase):
    def test_computed_zero_shows_line_one_and_zero_with_no_parameters(self) -> None:
        from tests.support import act
        from tests.test_form1099g_box1_schedule1_line7 import _attested

        ws = t5.Return(wages=50000, amounts={"cedar": 3000.0})
        with ws.raw:
            ws.plain()
            revision = ws.log.read().revision
            ws.log.append(
                act(revision, "assertion", {"finding": _attested(
                    "demo.t1a.z1.dependent-override",
                    "tax.us.2025.sli-scope.not-claimed-as-dependent|tax-year=2025", "no",
                )}),
                expected_revision=revision,
            )
            outcome = t5.run_live(ws.acts(), "demo.run.t1a.z1")
            self.assertEqual(outcome.line21["disposition"], "computed_zero")
            [row] = outcome.model["line21Explanation"]["rows"]
            self.assertEqual(row["status"], {"kind": "no-reason"})
            self.assertIn("basis", row)
            working = outcome.model["line21Explanation"]["working"]
            self.assertEqual(working["lineOneSubtotal"], 3000)
            self.assertEqual(working["value"], 0)
            self.assertEqual(working["parameters"], [])
            self.assertNotIn("totalIncome", working)


class LateMember(unittest.TestCase):
    def test_first_saved_model_is_unchanged_when_a_second_statement_is_added(self) -> None:
        import tests.test_sli_relationship_recording as track14
        from packages.kernel.facts import fact_id_for

        ws = t5.Return(amounts={"cedar": 1500.0})
        with ws.raw:
            ws.plain()
            first = t5.run_live(ws.acts(), "demo.run.t1a.late1")
            [first_row] = first.model["line21Explanation"]["rows"]
            self.assertEqual(first_row["statementLabel"]["lender"], "Cedar Servicing")

            keys = t5.Return.STATEMENT_KEYS["birch"]
            track14._append_source(ws.log, ws.registry, t5.BOX2, keys, False, "late-box2-birch")
            track14._append_source(ws.log, ws.registry, t5.BOX1, keys, 800.0, "late-box1-birch")
            ws.statement_keys["birch"] = keys
            ws.statement["birch"] = fact_id_for(t5.BOX1, keys)
            ws.plain("spring", "spring", "birch")
            second = t5.run_live(ws.acts(), "demo.run.t1a.late2")

            # The first saved model, reloaded, is untouched by the later run.
            [first_row_again] = first.model["line21Explanation"]["rows"]
            self.assertEqual(first_row_again, first_row)
            self.assertEqual(len(second.model["line21Explanation"]["rows"]), 2)


class NoStatement(unittest.TestCase):
    def test_no_form_1098e_has_no_block(self) -> None:
        ws = t5.Return(amounts={})
        with ws.raw:
            outcome = t5.run_live(ws.acts(), "demo.run.t1a.none")
            self.assertEqual(outcome.line21["disposition"], "closure_backed_zero")
            self.assertNotIn("line21Explanation", outcome.model)


class GoldensUnchanged(unittest.TestCase):
    def test_v33_track8_goldens_carry_no_block(self) -> None:
        from tools import generate_f1098e_track8_presentation_goldens as goldens

        models = goldens.regenerate()
        self.assertTrue(models)
        for model in models.values():
            self.assertNotIn("line21Explanation", model)


class UnrelatedSectionsUnaffected(unittest.TestCase):
    def test_line_1a_is_unaffected_and_the_block_is_the_only_addition(self) -> None:
        ws = t5.Return(wages=50000, amounts={"cedar": 3000.0})
        with ws.raw:
            ws.plain()
            outcome = t5.run_live(ws.acts(), "demo.run.t1a.unrelated")
            self.assertIn("line21Explanation", outcome.model)

            # The wages line (unrelated to student loans) resolves exactly as
            # the Track 6 AGI milestone established, untouched by this change.
            [line1a] = [s for s in outcome.model["sections"]
                        if s["field"]["id"] == "tax.us.2025.form1040.line-1a"]
            self.assertEqual(line1a["resolved"]["disposition"], "published_value")
            self.assertEqual(line1a["resolved"]["value"], 50000)

            # The only top-level key this change can add.
            without_block = set(outcome.model) - {"line21Explanation"}
            self.assertEqual(without_block, {
                "schema", "runId", "pinLabels", "sections", "citationGroups",
                "attachments", "unsupportedSourceFindings", "authorization",
            })


if __name__ == "__main__":
    unittest.main()
