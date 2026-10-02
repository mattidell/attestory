"""Source-level guardrails for the synthetic saved-file reader surface."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "tools/presentation_harness/examples/pages/statement-calculation.experimental.v1.html"
MANIFEST = ROOT / "tools/presentation_harness/examples/manifests/statement-calculation-track6b.v1.json"


class SavedStatementReaderPage(unittest.TestCase):
    def test_page_is_saved_model_only_and_uses_safe_text_nodes(self) -> None:
        page = PAGE.read_text(encoding="utf-8")
        self.assertIn("Object.freeze(__FIXTURE_JSON__)", page)
        self.assertIn("synthetic", page.lower())
        self.assertIn("demo-*", page)
        self.assertNotRegex(page, re.compile(r"\b(?:fetch|XMLHttpRequest|localStorage|sessionStorage)\s*\("))
        self.assertNotRegex(page, re.compile(r"\b(?:innerHTML|outerHTML|insertAdjacentHTML|document\.write)\b"))
        self.assertIn("document.createTextNode", page)
        self.assertNotIn("JSON.parse", page)

    def test_page_has_no_condition_entry_controls_or_alerts(self) -> None:
        page = PAGE.read_text(encoding="utf-8").lower()
        self.assertNotRegex(page, re.compile(r"<\s*(?:input|textarea|select|form)\b"))
        self.assertNotIn('createelement("input")', page)
        self.assertNotIn('createelement("textarea")', page)
        self.assertNotIn('setattribute("role", "alert")', page)
        self.assertNotIn('role="alert"', page)
        self.assertIn('createelement("details")', page)
        self.assertIn('add(record, "summary"', page)

    def test_four_readings_are_separate_and_technical_source_text_is_disclosed(self) -> None:
        page = PAGE.read_text(encoding="utf-8")
        self.assertIn("group.statementLabel && group.statementLabel.statement", page)
        self.assertNotIn("factId.split", page)
        self.assertIn("group.sourceFindings", page)
        self.assertIn('source.factTypeId === BOX1_TYPE', page)
        self.assertIn('source.factTypeId === CLAIM_TYPE', page)
        self.assertIn('className = "technical-source"', page)
        self.assertIn('"Technical description"', page)
        self.assertIn("group.assumptions", page)
        self.assertIn("group.statementOutcome", page)
        self.assertIn("group.responsibilities", page)
        self.assertIn('item.id === "line-sch1-21"', page)
        self.assertIn('source.origin !== "declared_default"', page)
        self.assertIn('item.origin === "declared_default"', page)
        self.assertIn('group.nodes || []', page)
        self.assertIn('group.pins', page)
        self.assertIn('group.lineNote', page)
        self.assertIn('sameAmountRepresentation(suppliedAmount.value, group.value)', page)
        self.assertIn('source.factId === group.factId', page)
        self.assertNotIn('addPins(assumed', page)
        self.assertNotIn('for (const node of group.nodes || [])', page)
        self.assertIn('id="worksheet-section"', page)
        self.assertIn('id="calculation-view"', page)
        self.assertIn("Not Schedule 1 line 21. The worksheet does not read these figures.", page)
        self.assertNotIn("reduce(", page)

    def test_named_keyboard_evidence_disclosures_cover_saved_axes_and_diagnostics(self) -> None:
        page = PAGE.read_text(encoding="utf-8")
        for label in (
            "Statement amount", "Borrowing route", "Statement-wide scope", "Claim classifier ",
            "Intermediate finding ", "Statement conclusion", "Published responsibility ",
            "Responsibility diagnostic ", "Selected parameter ", "Published rule-stated basis",
        ):
            self.assertIn(label, page)
        self.assertIn('className = "reader-evidence"', page)
        self.assertIn('add(details, "summary"', page)
        self.assertIn('"disposition", "Original disposition"', page)
        self.assertIn('addPins(block, record.pins)', page)
        self.assertIn('addMissing(block, record.missing)', page)
        self.assertIn('JSON.stringify({ amount: group, outcome })', page)

    def test_manifest_uses_the_three_ignored_saved_files_and_no_hand_golden(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(
            {item["id"]: item["path"] for item in manifest["fixtures"]},
            {
                "ordinary": "temp/track6b/ordinary/presentation.json",
                "adverse": "temp/track6b/adverse/presentation.json",
                "unresolved": "temp/track6b/unresolved/presentation.json",
            },
        )
        self.assertTrue(all(item["synthetic"] is True for item in manifest["fixtures"]))
        self.assertEqual({entry["fixture_id"] for entry in manifest["matrix"]}, {"ordinary", "adverse", "unresolved"})
        self.assertEqual(len(manifest["fixtures"]), 3)
        self.assertTrue(all(path.startswith("temp/track6b/") for path in (f["path"] for f in manifest["fixtures"])))
        criterion_ids = {criterion["id"] for criterion in manifest["criteria"]}
        self.assertIn("ordinary-link-wording", criterion_ids)
        self.assertIn("ordinary-line-note", criterion_ids)
        self.assertIn("ordinary-answer", criterion_ids)
        self.assertIn("adverse-answer", criterion_ids)
        self.assertIn("unresolved-axis", criterion_ids)
        self.assertTrue((ROOT / "tools/presentation_harness/examples/verify_track6b_reader.mjs").is_file())


if __name__ == "__main__":
    unittest.main()
