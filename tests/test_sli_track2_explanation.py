"""Track 2: what each form's line 21 result used and assumed, under v42.

Each case is recorded through the Track 1 populations, adopted on core
calculations v42, and run through ``live_coordinate_run`` with both runners.
The presentation is reloaded from disk and the page is rendered to
``temp/track2/``.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any, cast
from unittest import mock

import pytest

import packages.derivation.live as live_module
import tests.test_sli_relationship_recording as track14
import tests.test_sli_track1_combined_standing as track1
import tests.test_sli_track4_support_chain as track4
import tests.test_sli_track5_worksheet_integration as track5
from packages.derivation.live import live_coordinate_run
from packages.derivation.live_session import _render_page
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.marshal import marshal_live_run_context
from packages.derivation.production_resolver import PublicationSurface
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import run
from packages.kernel.facts import fact_id_for
from tests.support import act, demo_entity

pytestmark = pytest.mark.live

ROOT = track5.ROOT
BOX2 = track5.BOX2
BOX1 = track5.BOX1
REPLACED = track5.REPLACED
PAGES = ROOT / "temp" / "track2"
QUOTES = PAGES / "quotes"
METHOD = "The older yes is the method for this form. No current loan link was recorded."
BOX_SENTENCE = "Box 1 holds no loan the person did not record"
DENIAL = "This form does not include that borrowing."
OLDER_YES = "Recorded, not used. Older yes on this form."
INCLUSION = "tax.us.2025.sli.statement-inclusion-relationship"
WITHDRAWN = "tax.us.2025.sli.statement-inclusion-withdrawn"
DENIED = "tax.us.2025.sli.statement-inclusion-denied"


def _run(ws: track5.Return, name: str) -> track5.Outcome:
    """v42, both runners, presentation reloaded, page rendered from that model."""
    captured: list[Any] = []

    def spy(**kwargs: Any) -> Any:
        marshalled = marshal_live_run_context(**kwargs)
        captured.append(marshalled._context)
        return marshalled

    acts = tuple(ws.acts())
    with mock.patch.object(live_module, "marshal_live_run_context", side_effect=spy), \
            tempfile.TemporaryDirectory(prefix="sli-track2-live-") as work:
        capability = WorkspaceCapability(Path(work) / "workspace")
        outcome = live_coordinate_run(
            capability, repo_root=ROOT, authoritative_acts=acts,
            workspace_revision=len(acts), run_scope=track5.SCOPE, scope_user=track5.USER,
            request={"schema": "run-request.v1"}, run_id=f"demo.run.track2.{name}", governance_pins=[],
            surface=PublicationSurface(track5.RELEASE_DIR, track1.V40_REGISTRY, track5.CONTENT),
            output_name="track2.json",
        )
        if outcome.refusal is not None or outcome.presentation_path is None:
            raise AssertionError(f"{name} refused: {outcome.refusal!r}")
        model = json.loads(outcome.presentation_path.read_text("utf-8"))
        page_html = _render_page(ROOT, capability, outcome.presentation_path).decode("utf-8")
    [context] = captured
    schemas = DerivationSchemas()
    forward, reference = run(context, schemas), run_reference(context, schemas)
    if track4.surface(forward) != track4.surface(reference):
        raise AssertionError(f"{name}: runners disagree")
    assert outcome.publications is not None
    if sorted(json.dumps(p.finding, sort_keys=True) for p in outcome.publications) != sorted(
            json.dumps(p.finding, sort_keys=True) for p in forward.publications):
        raise AssertionError(f"{name}: reloaded publications differ")
    PAGES.mkdir(parents=True, exist_ok=True)
    (PAGES / f"{name}.html").write_text(page_html, encoding="utf-8")
    return track5.Outcome(forward, reference, model, page_html)


def _row(outcome: track5.Outcome, ws: track5.Return, statement: str) -> dict[str, Any]:
    keys = dict(ws.statement_keys[statement])
    want = {"lender": keys["lender"], "statement": keys["statement"], "taxYear": keys["tax-year"]}
    matches = [row for row in outcome.model["line21Explanation"]["rows"] if row.get("statementKeys") == want]
    if len(matches) != 1:
        raise AssertionError(f"{statement} matched {len(matches)} rows")
    return cast(dict[str, Any], matches[0])


def _prepare_row(name: str) -> tuple[track5.Outcome, dict[str, dict[str, Any]]]:
    spec = track1.SPECS[name]
    ws = track5.Return(wages=spec.wages, amounts=spec.amounts)
    with ws.raw:
        spec.populate(ws)
        track1.adopt_v42(ws)
        outcome = _run(ws, name)
        return outcome, {statement: _row(outcome, ws, statement) for statement in spec.amounts}


def _quote(name: str, line: str) -> None:
    QUOTES.mkdir(parents=True, exist_ok=True)
    (QUOTES / f"{name}.txt").write_text(line + "\n", encoding="utf-8")


def _said_types(row: dict[str, Any]) -> set[str]:
    said = row["account"]["said"]
    return {item["factType"] for item in said["current"] + said["history"]}


def _assert_form_witnesses_stay_out(test: unittest.TestCase, row: dict[str, Any]) -> None:
    test.assertNotIn(BOX1, _said_types(row))
    test.assertNotIn(BOX2, _said_types(row))
    older = row["account"]["said"]["olderAnswer"]
    if older["currency"] == "current":
        test.assertNotEqual(older["findingId"], older["sourceFindingId"])
    test.assertNotIn("replaced", " ".join(item["text"] for item in row["account"]["recordedNotUsed"]))


def _assert_reason_keys(test: unittest.TestCase, outcome: track5.Outcome, row: dict[str, Any]) -> None:
    keys = row["statementKeys"]
    reasons = outcome.line21["reasons"]
    test.assertTrue(row["status"]["reasonIndices"])
    for index in row["status"]["reasonIndices"]:
        fact_id = reasons[index]["factId"]
        test.assertIn(f"lender={keys['lender']}", fact_id)
        test.assertIn(f"statement={keys['statement']}", fact_id)


def _kind(row: dict[str, Any]) -> str:
    return str(row["account"]["used"]["kind"])


def _recorded(row: dict[str, Any]) -> list[str]:
    return [item["text"] for item in row["account"]["recordedNotUsed"]]


class Track2Explanation(unittest.TestCase):
    def test_k0a_old_only_is_the_method(self) -> None:
        outcome, rows = _prepare_row("K0a")
        self.assertEqual(outcome.line21["disposition"], "published_value")
        self.assertEqual(outcome.line21["value"], 2500)
        self.assertFalse(outcome.line21.get("reasons"))
        self.assertIn("working", outcome.model["line21Explanation"])
        for row in rows.values():
            self.assertEqual(row["account"]["said"]["olderAnswer"]["value"], "yes")
            self.assertEqual(row["account"]["said"]["olderAnswer"]["currency"], "current")
            self.assertEqual(_kind(row), "older-method")
            self.assertEqual(row["account"]["used"]["combined"], "none")
            self.assertEqual(row["basis"]["standsInFor"], [METHOD])
            self.assertEqual(row["basis"]["ruleId"], "tax.us.2025.rule.sli-statement-combined-standing")
            self.assertNotIn(BOX_SENTENCE, " ".join(row["basis"]["assumed"]))
            self.assertEqual(_recorded(row), [])
            self.assertNotIn(DENIED, _said_types(row))
            _assert_form_witnesses_stay_out(self, row)
        self.assertEqual(rows["cedar"]["amount"], 3000)
        self.assertEqual(rows["birch"]["amount"], 1800)
        assert outcome.page_html is not None
        self.assertIn("Form 1098-E box 1:", outcome.page_html)
        self.assertIn("What this form accounts for", outcome.page_html)
        self.assertIn(METHOD, outcome.page_html)
        _quote("K0a", "K0a published 2500; both forms older-method, combined none, method sentence, recorded none; box 2 not said")

    def test_k0b_plain_case_uses_the_support_basis(self) -> None:
        outcome, rows = _prepare_row("K0b")
        self.assertEqual(outcome.line21["value"], 2500)
        for row in rows.values():
            self.assertEqual(row["account"]["said"]["olderAnswer"]["value"], "absent")
            self.assertEqual(row["account"]["said"]["olderAnswer"]["currency"], "absent")
            self.assertEqual(_kind(row), "plain-case")
            self.assertEqual(row["account"]["used"]["combined"], "none")
            self.assertEqual(row["basis"]["ruleId"], "tax.us.2025.rule.sli-statement-loan-support")
            self.assertNotIn("standsInFor", row["basis"])
            self.assertTrue(any(BOX_SENTENCE in sentence for sentence in row["basis"]["assumed"]))
            self.assertEqual(_recorded(row), [])
            _assert_form_witnesses_stay_out(self, row)
        _quote("K0b", "K0b published 2500; both forms plain-case on the support basis, including the box 1 sentence; recorded none")

    def test_k1_unused_older_yes_beside_a_plain_case(self) -> None:
        outcome, rows = _prepare_row("K1")
        self.assertEqual(outcome.line21["value"], 2500)
        cedar, birch = rows["cedar"], rows["birch"]
        self.assertEqual(_kind(cedar), "plain-case")
        self.assertTrue(any(BOX_SENTENCE in sentence for sentence in cedar["basis"]["assumed"]))
        self.assertEqual(_recorded(cedar), [OLDER_YES])
        self.assertEqual(_kind(birch), "older-method")
        self.assertEqual(birch["basis"]["standsInFor"], [METHOD])
        self.assertEqual(_recorded(birch), [])
        _assert_form_witnesses_stay_out(self, cedar)
        _assert_form_witnesses_stay_out(self, birch)
        _quote("K1", "K1 published 2500; cedar plain-case records older yes as not used; birch older-method")

    def test_k2_older_no_blocks_and_keeps_the_sibling(self) -> None:
        outcome, rows = _prepare_row("K2")
        self.assertEqual(outcome.line21["disposition"], "blocked")
        self.assertNotIn("working", outcome.model["line21Explanation"])
        cedar, birch = rows["cedar"], rows["birch"]
        self.assertEqual(cedar["account"]["said"]["olderAnswer"]["value"], "no")
        self.assertEqual(_kind(cedar), "nothing")
        self.assertEqual(cedar["account"]["used"]["combined"], "older-no")
        self.assertNotIn("basis", cedar)
        _assert_reason_keys(self, outcome, cedar)
        sentence = outcome.line21["reasons"][cedar["status"]["reasonIndices"][0]]["sentence"]
        self.assertIn("answered no", sentence)
        self.assertNotIn(OLDER_YES, _recorded(cedar))
        for fragment in (
            "The loan-cost answer is yes.",
            "The enrollment answer is yes.",
            "The financing answer is affirmed.",
            "The inclusion answer is affirmed.",
        ):
            self.assertTrue(any(fragment in text for text in _recorded(cedar)), _recorded(cedar))
        self.assertEqual(_kind(birch), "older-method")
        self.assertEqual(_recorded(birch), [])
        _assert_form_witnesses_stay_out(self, cedar)
        _quote("K2", "K2 blocked, no worked figures; cedar nothing/older-no by its own keys; birch older-method")

    def test_k3_plain_case_beside_an_old_only_sibling(self) -> None:
        outcome, rows = _prepare_row("K3")
        self.assertEqual(outcome.line21["value"], 2500)
        self.assertEqual(_kind(rows["cedar"]), "plain-case")
        self.assertEqual(rows["cedar"]["account"]["said"]["olderAnswer"]["value"], "absent")
        self.assertEqual(_recorded(rows["cedar"]), [])
        self.assertEqual(_kind(rows["birch"]), "older-method")
        self.assertEqual(rows["birch"]["basis"]["standsInFor"], [METHOD])
        _quote("K3", "K3 published 2500; cedar plain-case, older absent; birch older-method")

    def test_l9a_missing_loan_cost_and_box2_is_not_said(self) -> None:
        outcome, rows = _prepare_row("L9a")
        self.assertEqual(outcome.line21["value"], 2500)
        self.assertFalse(outcome.line21.get("reasons"))
        cedar, birch = rows["cedar"], rows["birch"]
        self.assertEqual(cedar["standing"], "loan-cost-answer-missing")
        self.assertEqual(_kind(cedar), "older-yes-cover")
        self.assertEqual(
            cedar["basis"]["standsInFor"],
            ["The older yes stands in for the missing loan-cost answer."],
        )
        self.assertFalse(any(BOX_SENTENCE in sentence for sentence in cedar["basis"]["assumed"]))
        self.assertEqual(_recorded(cedar), [])
        self.assertEqual(_kind(birch), "older-method")
        self.assertEqual(birch["basis"]["standsInFor"], [METHOD])
        _assert_form_witnesses_stay_out(self, cedar)
        _assert_form_witnesses_stay_out(self, birch)
        _quote("L9a", "L9a published 2500; cedar covers the missing loan-cost answer; box 2 is not said; birch older-method")

    def test_k9_after_withdrawn_inclusion_stays_history(self) -> None:
        outcome, rows = _prepare_row("K9-after")
        self.assertEqual(outcome.line21["value"], 2500)
        cedar = rows["cedar"]
        self.assertEqual(_kind(cedar), "older-yes-cover")
        self.assertEqual(
            cedar["basis"]["standsInFor"],
            ["The older yes stands in for the withdrawn inclusion."],
        )
        current = {item["factType"] for item in cedar["account"]["said"]["current"]}
        history = {item["factType"] for item in cedar["account"]["said"]["history"]}
        self.assertIn(WITHDRAWN, current)
        self.assertNotIn(INCLUSION, current)
        self.assertIn(INCLUSION, history)
        self.assertEqual(_recorded(cedar), [])
        self.assertEqual(_kind(rows["birch"]), "older-method")
        _quote("K9-after", "K9-after published 2500; cedar covers the withdrawn inclusion; ended inclusion is history; birch older-method")

    def test_denied_loan_no_names_the_denial(self) -> None:
        outcome, rows = _prepare_row("denied-loan-no")
        self.assertEqual(outcome.line21["value"], 2500)
        self.assertFalse(outcome.line21.get("reasons"))
        cedar, birch = rows["cedar"], rows["birch"]
        self.assertEqual(cedar["standing"], "no-loan-link")
        self.assertEqual(birch["standing"], "no-loan-link")
        denial = next(item for item in cedar["account"]["said"]["current"] if item["factType"] == DENIED)
        self.assertEqual(denial["proposition"], DENIAL)
        self.assertEqual(_kind(cedar), "older-yes-cover")
        self.assertEqual(
            cedar["basis"]["standsInFor"],
            ["The older yes stands in for the denial that this form does not include that borrowing."],
        )
        history = {item["factType"] for item in cedar["account"]["said"]["history"]}
        self.assertIn(INCLUSION, history)
        recorded = set(_recorded(cedar))
        self.assertIn("Recorded, not used. The loan-cost answer is no on a borrowing this form denied.", recorded)
        self.assertIn("Recorded, not used. The enrollment answer is yes on a borrowing this form denied.", recorded)
        self.assertNotIn(DENIED, _said_types(birch))
        self.assertEqual(_kind(birch), "older-method")
        self.assertEqual(_recorded(birch), [])
        _quote("denied-loan-no", "denied-loan-no published 2500; cedar denial is the cover; loan-cost no and enrollment yes recorded not used; birch older-method")

    def test_u3_cannot_tell_uses_nothing(self) -> None:
        outcome, rows = _prepare_row("U3")
        self.assertEqual(outcome.line21["disposition"], "blocked")
        self.assertNotIn("working", outcome.model["line21Explanation"])
        cedar = rows["cedar"]
        self.assertEqual(_kind(cedar), "nothing")
        self.assertEqual(cedar["account"]["used"]["combined"], "statement-loan-cannot-tell")
        self.assertNotIn("basis", cedar)
        _assert_reason_keys(self, outcome, cedar)
        sentence = outcome.line21["reasons"][cedar["status"]["reasonIndices"][0]]["sentence"]
        self.assertIn("cannot tell", sentence)
        self.assertEqual(_recorded(cedar), [OLDER_YES])
        self.assertEqual(_kind(rows["birch"]), "older-method")
        _quote("U3", "U3 blocked, no worked figures; cedar nothing/cannot-tell by its own keys, older yes recorded not used; birch older-method")

    def test_m1_contradiction_uses_nothing(self) -> None:
        outcome, rows = _prepare_row("M1")
        self.assertEqual(outcome.line21["disposition"], "blocked")
        self.assertNotIn("working", outcome.model["line21Explanation"])
        cedar = rows["cedar"]
        self.assertEqual(_kind(cedar), "nothing")
        self.assertEqual(cedar["account"]["used"]["combined"], "contradicts-loan-cost-no")
        self.assertNotIn("basis", cedar)
        _assert_reason_keys(self, outcome, cedar)
        sentence = outcome.line21["reasons"][cedar["status"]["reasonIndices"][0]]["sentence"]
        self.assertIn("school costs", sentence)
        self.assertEqual(_recorded(cedar), [OLDER_YES])
        self.assertEqual(_kind(rows["birch"]), "older-method")
        _quote("M1", "M1 blocked, no worked figures; cedar nothing on the loan-cost contradiction, only older yes recorded not used; birch older-method")

    def test_k6_component_block_records_the_plain_detail(self) -> None:
        outcome, rows = _prepare_row("K6")
        self.assertEqual(outcome.line21["disposition"], "blocked")
        self.assertEqual(outcome.line21.get("activeCodes"), ["SLI_UNIVERSAL_COMPONENT_VIOLATION"])
        self.assertNotIn("working", outcome.model["line21Explanation"])
        cedar = rows["cedar"]
        self.assertEqual(_kind(cedar), "nothing")
        self.assertEqual(cedar["account"]["used"]["combined"], "none")
        self.assertEqual(cedar["support"], "plain-case-supported")
        self.assertNotIn("basis", cedar)
        _assert_reason_keys(self, outcome, cedar)
        sentence = outcome.line21["reasons"][cedar["status"]["reasonIndices"][0]]["sentence"]
        self.assertIn("related person", sentence)
        recorded = _recorded(cedar)
        self.assertIn(OLDER_YES, recorded)
        for fragment in (
            "The loan-cost answer is yes.",
            "The enrollment answer is yes.",
            "The financing answer is affirmed.",
            "The inclusion answer is affirmed.",
        ):
            self.assertTrue(any(fragment in text for text in recorded), recorded)
        self.assertEqual(_kind(rows["birch"]), "older-method")
        _quote("K6", "K6 blocked by the related-person component, no worked figures; cedar nothing records the older yes and the four link answers; birch older-method")

    def test_two_forms_one_label_match_by_statement_keys(self) -> None:
        ws = track5.Return(wages=50000, amounts={})
        with ws.raw:
            def add_entity(entity_id: str, label: str, kind: str) -> None:
                revision = ws.log.read().revision
                ws.log.append(
                    act(revision, "entity-introduced", {"entity": demo_entity(entity_id, label, kind)}),
                    expected_revision=revision,
                )

            add_entity("demo.track2.lender.twin1", "Twin Lender", "tax.us.student-loan-lender")
            add_entity("demo.track2.statement.twin1", "Twin Statement", "tax.us.1098e-statement")
            add_entity("demo.track2.lender.twin2", "Twin Lender", "tax.us.student-loan-lender")
            add_entity("demo.track2.statement.twin2", "Twin Statement", "tax.us.1098e-statement")
            keys = {
                "twin1": (("lender", "demo.track2.lender.twin1"), ("statement", "demo.track2.statement.twin1"), ("tax-year", "2025")),
                "twin2": (("lender", "demo.track2.lender.twin2"), ("statement", "demo.track2.statement.twin2"), ("tax-year", "2025")),
            }
            for name, amount in (("twin1", 1100.0), ("twin2", 1300.0)):
                track14._append_source(ws.log, ws.registry, BOX2, keys[name], False, f"track2-box2-{name}")
                track14._append_source(ws.log, ws.registry, BOX1, keys[name], amount, f"track2-box1-{name}")
                ws.statement_keys[name] = keys[name]
                ws.statement[name] = fact_id_for(BOX1, keys[name])
                ws.old_answers(name, values={REPLACED: "no"})
            track1._link_complete(ws, "autumn", "autumn", "twin1")
            track1._link_complete(ws, "spring", "spring", "twin2")
            track1.adopt_v42(ws)
            outcome = _run(ws, "same-label")
            rows = [_row(outcome, ws, name) for name in ("twin1", "twin2")]
        self.assertEqual(outcome.line21["disposition"], "blocked")
        self.assertNotIn("working", outcome.model["line21Explanation"])
        self.assertEqual({row["statementLabel"]["statement"] for row in rows}, {"Twin Statement"})
        self.assertNotEqual(rows[0]["statementKeys"], rows[1]["statementKeys"])
        for row in rows:
            self.assertEqual(_kind(row), "nothing")
            self.assertEqual(row["account"]["used"]["combined"], "older-no")
            self.assertNotIn("basis", row)
            _assert_reason_keys(self, outcome, row)
            _assert_form_witnesses_stay_out(self, row)
        self.assertNotEqual(rows[0]["status"]["reasonIndices"], rows[1]["status"]["reasonIndices"])
        _quote("same-label", "same-label blocked; two forms share one display label and each reason matches its own statement keys")


if __name__ == "__main__":
    unittest.main()
