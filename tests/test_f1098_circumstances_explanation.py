"""Track 3 saved mortgage explanation on the v44 coordinator path."""
from __future__ import annotations

import json
import unittest
from unittest.mock import patch
from typing import Any

from packages.derivation.presentation_projection import PresentationModelError, validate_presentation_model
import packages.derivation.presentation_projection as projection
from tests.test_f1098_circumstances_calculation import (
    _run,
)


class TestF1098CircumstancesExplanation(unittest.TestCase):
    def _saved_model(self, name: str, interest: float, **kwargs: Any) -> dict[str, Any]:
        # _run executes live_coordinate_run and reads the saved presentation
        # JSON before its temporary workspace is removed; this second JSON
        # round-trip models a fresh page load with no live result object.
        _report, saved_model, _result = _run(name, interest, **kwargs)
        reloaded = json.loads(json.dumps(saved_model))
        validate_presentation_model(reloaded)
        return reloaded

    def test_qualified_and_qualified_zero_show_exact_basis_and_payer(self) -> None:
        for name, amount in (("explain-qualified", 20000.0), ("explain-qualified-zero", 0.0)):
            with self.subTest(name=name):
                model = self._saved_model(name, amount)
                block = model["mortgageInterestExplanation"]
                account = block["accounts"][0]
                self.assertEqual(account["reason"], "qualified")
                self.assertEqual(account["deductibleAmount"], amount)
                self.assertEqual(account["reportedInterest"]["value"], amount)
                self.assertEqual(account["statementKeys"]["payer"], "demo.f1098.lender.a")
                self.assertEqual(account["statementLabel"]["lender"], "Synthetic lender")
                self.assertEqual(set(account["basis"]), {"said", "derived", "assumed", "left_with_person"})
                self.assertTrue(account["sourceDocuments"])
                self.assertTrue(account["personAnswers"])
                # Runtime publishes unused timing defaults, but the selected
                # purchase branch does not pin them; they are not account support.
                self.assertEqual(account["declaredDefaults"], [])
                self.assertTrue(all(row["title"] and row["origin"]["kind"] == "recorded" for row in account["personAnswers"]))

    def test_justified_zeros_use_their_own_content_not_qualified_basis(self) -> None:
        cases = (
            ("explain-zero-collateral", {"home-is-collateral": "no", "what-the-money-paid-for": "unrelated-personal-expense"}, "not-collateral"),
            ("explain-zero-payment", {"paid-the-interest": "no", "what-the-money-paid-for": "unrelated-personal-expense"}, "not-paid"),
            ("explain-zero-personal", {"what-the-money-paid-for": "unrelated-personal-expense", "loan-timing-relative-to-purchase": "no", "loan-timing-relative-to-building-or-improving": "no"}, "use-unrelated-personal-expense"),
        )
        for name, answers, expected in cases:
            with self.subTest(name=name):
                model = self._saved_model(name, 20000.0, answers=answers)
                account = model["mortgageInterestExplanation"]["accounts"][0]
                self.assertEqual(account["reason"], expected)
                self.assertEqual(account["deductibleAmount"], 0)
                self.assertEqual(account["reportedInterest"]["value"], 20000)
                self.assertNotIn("basis", account)
                self.assertTrue(account["description"])
                self.assertTrue(account["personAnswers"])

    def test_consumed_box9_default_keeps_exact_parameter_pin(self) -> None:
        model = self._saved_model("explain-box9-default", 20000.0, omit_box9=True)
        account = model["mortgageInterestExplanation"]["accounts"][0]
        defaults = [item for item in account["declaredDefaults"] if item["factType"].endswith("box9-number-of-properties")]
        self.assertEqual(len(defaults), 1)
        self.assertEqual(defaults[0]["response"], "1")
        self.assertEqual(defaults[0]["origin"]["parameter"], {
            "id": "tax.us.2025.parameter.f1098-box9-default-single-property", "version": "v1",
        })
        self.assertFalse(any(item["factType"].endswith("loan-timing-relative-to-purchase") for item in account["declaredDefaults"]))

    def test_incidental_parameter_pin_does_not_change_recorded_reason(self) -> None:
        original = projection._mortgage_interest_explanation

        def add_unrelated_parameter(**kwargs: Any) -> Any:
            for publication in kwargs["publications"]:
                finding = publication.finding
                if finding.get("symbol") == "tax.us.2025.schedule-a.line8a":
                    finding["pins"].append({"role": "parameter", "id": "tax.us.2025.f1098.mortgage-interest-limit", "version": "v1"})
            return original(**kwargs)

        with patch.object(projection, "_mortgage_interest_explanation", side_effect=add_unrelated_parameter):
            model = self._saved_model("explain-incidental-pin", 20000.0, answers={"home-is-collateral": "no"})
        account = model["mortgageInterestExplanation"]["accounts"][0]
        self.assertEqual(account["reason"], "not-collateral")
        self.assertEqual(account["deductibleAmount"], 0)

    def test_completed_singleton_with_broken_publication_identity_fails(self) -> None:
        original = projection._mortgage_interest_explanation

        def break_amount_identity(**kwargs: Any) -> Any:
            for publication in kwargs["publications"]:
                finding = publication.finding
                if finding.get("symbol") == "tax.us.2025.schedule-a.line8a":
                    for pin in finding.get("pins", []):
                        if pin.get("role") == "input" and pin.get("id") == "demo.f1098.box1.0":
                            pin["id"] = "demo.missing.box1"
            return original(**kwargs)

        with patch.object(projection, "_mortgage_interest_explanation", side_effect=break_amount_identity):
            with self.assertRaises(PresentationModelError):
                self._saved_model("explain-broken-identity", 20000.0)

    def test_unresolved_and_multiple_statements_have_no_completed_account(self) -> None:
        unresolved = self._saved_model("explain-unresolved", 20000.0, answers={"paid-the-interest": "cannot-tell"})
        self.assertNotIn("mortgageInterestExplanation", unresolved)
        unresolved_field = next(row for row in unresolved["sections"] if row["field"]["id"] == "tax.us.2025.form.f1098.residence-interest-unresolved")
        self.assertTrue(unresolved_field["resolved"]["reasons"])
        multiple = self._saved_model("explain-multiple", 15000.0, second_interest=5000.0)
        self.assertNotIn("mortgageInterestExplanation", multiple)
        closed_empty = self._saved_model("explain-closed-empty", None)
        self.assertNotIn("mortgageInterestExplanation", closed_empty)

    def test_withdrawn_timing_answer_is_not_current_account_support(self) -> None:
        model = self._saved_model(
            "explain-withdrawn-timing", 20000.0,
            answers={"what-the-money-paid-for": "unrelated-personal-expense", "loan-timing-relative-to-building-or-improving": "no"},
            answer_history={"loan-timing-relative-to-purchase": ["no"]},
            retract_answer="loan-timing-relative-to-purchase",
        )
        self.assertNotIn("mortgageInterestExplanation", model)
        unresolved = next(row for row in model["sections"] if row["field"]["id"] == "tax.us.2025.form.f1098.residence-interest-unresolved")
        self.assertTrue(unresolved["resolved"]["reasons"])

    def test_corrected_answer_replaces_old_support_in_saved_account(self) -> None:
        model = self._saved_model(
            "explain-correction", 20000.0,
            answer_history={"home-is-collateral": ["yes", "no"]},
        )
        account = model["mortgageInterestExplanation"]["accounts"][0]
        self.assertEqual(account["reason"], "not-collateral")
        collateral = [answer for answer in account["personAnswers"] if answer["factType"].endswith("home-is-collateral")]
        self.assertEqual(len(collateral), 1)
        self.assertEqual(collateral[0]["response"], "no")

    def test_cannot_tell_is_person_answer_and_default_is_not_promoted(self) -> None:
        unresolved = self._saved_model("explain-cannot-tell-timing", 20000.0, answers={
            "what-the-money-paid-for": "unrelated-personal-expense",
            "loan-timing-relative-to-purchase": "cannot-tell",
            "loan-timing-relative-to-building-or-improving": "no",
        })
        self.assertNotIn("mortgageInterestExplanation", unresolved)
        purchase = self._saved_model("explain-purchase-answer", 20000.0, answers={
            "what-the-money-paid-for": "unrelated-personal-expense",
            "loan-timing-relative-to-purchase": "no",
            "loan-timing-relative-to-building-or-improving": "no",
        })
        account = purchase["mortgageInterestExplanation"]["accounts"][0]
        timing = [item for item in account["personAnswers"] if item["factType"].endswith("loan-timing-relative-to-purchase")]
        self.assertEqual(len(timing), 1)
        self.assertEqual(timing[0]["response"], "no")
        self.assertFalse(any(item["factType"].endswith("loan-timing-relative-to-purchase") for item in account["declaredDefaults"]))

    def test_strict_saved_model_rejects_ambiguous_or_malformed_accounts(self) -> None:
        import copy

        model = self._saved_model("explain-strict", 20000.0)
        zero_model = self._saved_model("explain-strict-zero", 20000.0, answers={"home-is-collateral": "no"})
        malformed = copy.deepcopy(zero_model)
        malformed["mortgageInterestExplanation"]["accounts"][0]["deductibleAmount"] = 1
        with self.assertRaises(PresentationModelError):
            validate_presentation_model(malformed)
        for field in ("reportedInterest", "deductibleAmount"):
            for invalid in (float("nan"), float("inf")):
                malformed = copy.deepcopy(model)
                if field == "reportedInterest":
                    malformed["mortgageInterestExplanation"]["accounts"][0][field]["value"] = invalid
                else:
                    malformed["mortgageInterestExplanation"]["accounts"][0][field] = invalid
                with self.assertRaises(PresentationModelError):
                    validate_presentation_model(malformed)
        malformed = copy.deepcopy(model)
        malformed["mortgageInterestExplanation"]["accounts"][0]["declaredDefaults"].append({
            "findingId": "demo.default", "factType": "tax.us.2025.f1098.box9-number-of-properties",
            "title": "box 9", "response": "1", "origin": {"kind": "declared-default", "parameter": {"id": "demo.parameter"}},
        })
        with self.assertRaises(PresentationModelError):
            validate_presentation_model(malformed)
        malformed = copy.deepcopy(model)
        malformed["mortgageInterestExplanation"]["accounts"][0]["sourceDocuments"][0]["origin"]["findingId"] = "stale"
        with self.assertRaises(PresentationModelError):
            validate_presentation_model(malformed)

    def test_page_and_rehearsal_render_the_saved_account(self) -> None:
        from pathlib import Path

        root = Path(__file__).resolve().parents[1]
        for path in (
            root / "packages/presentation/pages/citation-walk.v1.html",
            root / "tools/presentation_harness/examples/pages/citation-walk.v1.html",
        ):
            content = path.read_text("utf-8")
            self.assertIn("renderMortgageExplanation", content)
            self.assertIn("mortgageInterestExplanation", content)
            self.assertIn("Current ordinary answers", content)
            self.assertIn("Schedule A line 8a deductible amount", content)


if __name__ == "__main__":
    unittest.main()
