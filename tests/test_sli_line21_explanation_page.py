"""Track 2: render the saved line 21 explanation through the production page."""
from __future__ import annotations

import copy
import html
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Any

import pytest

from packages.derivation.live_session import _render_page
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.presentation_projection import validate_presentation_model
from tests.support import act
import tests.test_sli_track5_worksheet_integration as t5

ROOT = Path(__file__).resolve().parents[1]
LINE21 = "line-sch1-21"
GOLDEN = ROOT / "packages/sample_data/f1098e_student_loan_interest_track6/presentation/below-floor.presentation-model.v1.json"


def _browser() -> str | None:
    candidates = [
        *sorted(Path.home().glob("Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell"), reverse=True),
        *sorted(Path.home().glob(".cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell"), reverse=True),
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
    ]
    found = next((str(path) for path in candidates if path.is_file()), None)
    return found or shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")


BROWSER = _browser()


def _saved_model(case: str) -> dict[str, Any]:
    if case == "C1":
        ws = t5.Return(wages=50000, amounts={"cedar": 3000.0})
        with ws.raw:
            ws.plain()
            return t5.run_live(ws.acts(), "demo.run.track2.c1").model
    if case == "C3":
        ws = t5.Return(amounts={"cedar": 1500.0, "birch": 800.0})
        with ws.raw:
            ws.plain()
            ws.plain("spring", "spring", "birch")
            return t5.run_live(ws.acts(), "demo.run.track2.c3").model
    if case == "C8":
        ws = t5.Return(amounts={"cedar": 1500.0, "birch": 800.0})
        with ws.raw:
            ws.plain()
            ws.plain("spring", "spring", "birch")
            ws.retract_source(ws.statement["cedar"])
            return t5.run_live(ws.acts(), "demo.run.track2.c8").model
    if case == "C10":
        ws = t5.Return(wages=50000, amounts={"cedar": 3000.0})
        with ws.raw:
            ws.old_answers("cedar")
            return t5.run_live(ws.acts(), "demo.run.track2.c10").model
    if case == "Z1":
        from tests.test_form1099g_box1_schedule1_line7 import _attested

        ws = t5.Return(wages=50000, amounts={"cedar": 3000.0})
        with ws.raw:
            ws.plain()
            revision = ws.log.read().revision
            ws.log.append(act(revision, "assertion", {"finding": _attested(
                "demo.track2.z1.dependent-override",
                "tax.us.2025.sli-scope.not-claimed-as-dependent|tax-year=2025", "no",
            )}), expected_revision=revision)
            return t5.run_live(ws.acts(), "demo.run.track2.z1").model
    if case == "R1":
        ws = t5.Return()
        with ws.raw:
            ws.link("financing", "autumn", "autumn")
            ws.link("statement-inclusion", "autumn", "cedar")
            ws.answer("loan", "autumn", "yes")
            ws.answer("enroll", "autumn", "yes")
            ws.common_answers("cedar", skip=("no-related-person-interest",))
            return t5.run_live(ws.acts(), "demo.run.track2.r1").model
    if case == "Missing":
        from packages.tax.sli_relationship_recording import record_borrowing_answer_durably

        ws = t5.Return(amounts={"cedar": 1500.0})
        with ws.raw:
            ws.link("financing", "autumn", "autumn")
            ws.link("statement-inclusion", "autumn", "cedar")
            record_borrowing_answer_durably(
                ws.log, ws.registry, question="loan-paid-only-school-costs",
                borrowing_ref=ws.borrowing["autumn"], response="yes",
                submission_id="demo.track2.page-no-wording.loan-cost",
                evidence_id="demo.evidence.track2.page-no-wording.loan-cost", actor=t5.USER,
                at="2026-10-04T10:00:00Z", recognition_context=None,
            )
            ws.answer("enroll", "autumn", "yes")
            ws.common_answers("cedar")
            return t5.run_live(ws.acts(), "demo.run.track2.page-missing-wording").model
    raise AssertionError(case)


@pytest.mark.live
@unittest.skipIf(BROWSER is None, "no headless Chromium available")
class SavedLine21ExplanationPage(unittest.TestCase):
    models: dict[str, dict[str, Any]] = {}
    _temp: tempfile.TemporaryDirectory[str]
    workspace: Path

    @classmethod
    def setUpClass(cls) -> None:
        cls._temp = tempfile.TemporaryDirectory(prefix="sli-track2-page-")
        cls.workspace = Path(cls._temp.name) / "workspace"
        cls.workspace.mkdir()
        cls.models = {}
        cls.models["v33"] = json.loads(GOLDEN.read_text("utf-8"))

    @classmethod
    def _model(cls, case: str) -> dict[str, Any]:
        if case not in cls.models:
            cls.models[case] = _saved_model(case)
        return cls.models[case]

    @classmethod
    def tearDownClass(cls) -> None:
        cls._temp.cleanup()

    def _page(self, model: dict[str, Any]) -> str:
        validate_presentation_model(model)
        path = self.workspace / "model.json"
        path.write_text(json.dumps(model), "utf-8")
        output = self.workspace / "page.html"
        output.write_bytes(_render_page(ROOT, WorkspaceCapability(self.workspace), path))
        page = output.read_text("utf-8")
        if str(model.get("runId", "")).startswith("demo.run.track2."):
            artifact_root = ROOT / "temp/track2"
            artifact_root.mkdir(parents=True, exist_ok=True)
            run_id = str(model["runId"])
            (artifact_root / f"{run_id}.presentation.json").write_text(json.dumps(model, indent=2), "utf-8")
            (artifact_root / f"{run_id}.page.html").write_text(page, "utf-8")
        return page

    def _dump(self, page: str, *, suffix: str = "", width: int = 1440, height: int = 1800,
              screenshot: Path | None = None) -> str:
        path = self.workspace / ("view" + suffix + ".html")
        path.write_text(page, "utf-8")
        profile = self.workspace / ("profile" + suffix)
        command = [str(BROWSER), "--headless", "--disable-gpu", "--no-sandbox",
                   f"--user-data-dir={profile}", f"--window-size={width},{height}",
                   "--virtual-time-budget=5000", "--run-all-compositor-stages-before-draw"]
        if screenshot is None:
            command.extend(["--dump-dom", path.as_uri()])
        else:
            screenshot.parent.mkdir(parents=True, exist_ok=True)
            command.extend([f"--screenshot={screenshot}", path.as_uri()])
        result = subprocess.run(command, capture_output=True, text=True, timeout=60, check=True)
        return result.stdout

    def _line(self, case: str) -> tuple[str, str, list[str]]:
        page = self._page(copy.deepcopy(self._model(case)))
        script = """<script>(() => {
          const line = document.querySelector('#line-sch1-21 .line');
          const closed = line.innerText;
          line.querySelectorAll('details').forEach((item) => { item.open = true; });
          const opened = line.innerText;
          line.setAttribute('data-track2-row-texts', JSON.stringify(
            Array.from(line.querySelectorAll('.line21-row')).map((row) => row.innerText)));
          line.setAttribute('data-track2-group-texts', JSON.stringify(
            Array.from(line.querySelectorAll('.line21-group')).map((group) => ({
              title: group.querySelector('h4').innerText,
              items: Array.from(group.querySelectorAll('li')).map((item) => item.innerText),
            }))));
          const box = document.createElement('pre'); box.id = 'track2-visible';
          box.textContent = 'COLLAPSED\\n' + closed + '\\nEXPANDED\\n' + opened;
          document.body.appendChild(box);
        })();</script>"""
        page = page.replace("</body>", script + "</body>")
        dom = self._dump(page, suffix="-" + case)
        match = __import__("re").search(r'<pre id="track2-visible">(.*?)</pre>', dom, __import__("re").S)
        self.assertIsNotNone(match, "browser did not return the visible line text")
        content = html.unescape(match.group(1))
        collapsed, expanded = content.split("EXPANDED", 1)
        self.assertIn("COLLAPSED", collapsed)
        row_match = __import__("re").search(r'data-track2-row-texts="([^"]*)"', dom)
        self.assertIsNotNone(row_match)
        rows = json.loads(html.unescape(row_match.group(1)))
        self._group_texts = json.loads(html.unescape(__import__("re").search(
            r'data-track2-group-texts="([^"]*)"', dom).group(1)))
        return collapsed.split("COLLAPSED", 1)[1].strip(), expanded.strip(), rows

    def _screenshot(self, case: str, width: int, height: int, size: str) -> None:
        page = self._page(copy.deepcopy(self._model(case)))
        script = """<script>(() => {
          const line = document.querySelector('#line-sch1-21 .line');
          line.querySelectorAll('details').forEach((item) => { item.open = true; });
          line.scrollIntoView();
        })();</script>"""
        page = page.replace("</body>", script + "</body>")
        path = ROOT / "temp/track2" / f"{case.lower()}-line21-{size}-expanded.png"
        self._dump(page, suffix="-shot-" + case + "-" + size, width=width, height=height, screenshot=path)
        check_script = """<script>(() => {
          const line = document.querySelector('#line-sch1-21 .line');
          line.querySelectorAll('details').forEach((item) => { item.open = true; });
          const nodes = [line, ...line.querySelectorAll('*')];
          const overflow = nodes.filter((node) => node.scrollWidth > node.clientWidth + 1).length;
          line.setAttribute('data-track2-overflow-count', String(overflow));
        })();</script>"""
        dom = self._dump(page.replace("</body>", check_script + "</body>"),
                         suffix="-overflow-" + case + "-" + size, width=width, height=height)
        match = __import__("re").search(r'data-track2-overflow-count="(\d+)"', dom)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "0", f"line 21 content overflows at {width}px")

    def test_c1_shows_separate_answers_assumptions_working_and_run(self) -> None:
        collapsed, text, _rows = self._line("C1")
        self.assertIn("What this statement's loan link rests on", collapsed)
        self.assertNotIn("Recorded answer:", collapsed)
        self.assertIn("What you told us", text)
        self.assertIn("What the application took as given", text)
        self.assertIn("Conditions left with you", text)
        self.assertIn("3000 reported", text)
        self.assertIn("Autumn study loan", text)
        self.assertIn("Interest reported (worksheet line 1): 3000", text)
        self.assertIn("Income the worksheet used: 50000", text)
        for parameter_id in ("sli-interest-cap", "sli-magi-phase-range", "sli-magi-threshold"):
            self.assertIn(parameter_id, text)
        self.assertIn("Deduction: 2500", text)
        self.assertIn("run demo.run.track2.c1", text)
        self.assertNotIn("DEPENDENCY_INVALID", text)
        groups = self._group_texts
        self.assertEqual([group["title"] for group in groups], [
            "What you told us", "What the application took as given", "Conditions left with you",
        ])
        self.assertTrue(groups[0]["items"])
        self.assertTrue(groups[1]["items"])
        self.assertTrue(all(item not in groups[0]["items"] for item in groups[1]["items"]))
        for width, height, name in ((1440, 2200, "desktop"), (390, 3200, "mobile")):
            self._screenshot("C1", width, height, name)

    def test_c3_answers_stay_with_their_own_statement(self) -> None:
        _, text, rows = self._line("C3")
        self.assertIn("Cedar Servicing", text)
        self.assertIn("Birch Servicing", text)
        self.assertIn("1500 reported", text)
        self.assertIn("800 reported", text)
        self.assertIn("What this statement's loan link rests on", text)
        self.assertEqual(len(rows), 2)
        # Row order is not a contract; find each statement's own row by its
        # own content, not by position.
        cedar_index = next(index for index, row in enumerate(rows) if "Cedar Servicing" in row)
        birch_index = next(index for index, row in enumerate(rows) if "Birch Servicing" in row)
        self.assertNotEqual(cedar_index, birch_index)
        self.assertIn("Autumn study loan", rows[cedar_index])
        self.assertIn("Spring study loan", rows[birch_index])
        # The saved model's rows share the DOM's order, so the same index
        # into each pairs the right statement with its own answers.
        source_rows = self._model("C3")["line21Explanation"]["rows"]
        for index, source_row in enumerate(source_rows):
            self.assertIn(source_row["statementLabel"]["lender"], rows[index])
            for loan in source_row["loans"]:
                self.assertIn(loan, rows[index])
        answer_texts = []
        for source_row in source_rows:
            answer_texts.append([
                (answer.get("proposition") + " Recorded answer: " + answer["response"] + ".")
                if answer.get("proposition") else
                ("Recorded answer: " + answer["response"] + ". Question wording was not saved with this answer.")
                for answer in source_row["basis"]["answers"]
            ])
        for own_text in answer_texts[0]:
            self.assertIn(own_text, rows[0])
        for own_text in answer_texts[1]:
            self.assertIn(own_text, rows[1])
        cross_row_texts = set(answer_texts[0]) ^ set(answer_texts[1])
        for text_from_other_answer in cross_row_texts:
            if text_from_other_answer in answer_texts[0]:
                self.assertNotIn(text_from_other_answer, rows[1])
            if text_from_other_answer in answer_texts[1]:
                self.assertNotIn(text_from_other_answer, rows[0])

    def test_c8_reason_row_and_supported_row_remain_distinct(self) -> None:
        collapsed, text, rows = self._line("C8")
        self.assertIn("See the reason above", text)
        self.assertIn("800 reported", text)
        self.assertNotIn("Missing dependency code(s)", text)
        self.assertNotIn("1500 reported", text)
        self.assertEqual(len(rows), 2)
        cedar_index = next(index for index, row in enumerate(rows) if "Cedar Servicing" in row)
        birch_index = next(index for index, row in enumerate(rows) if "Birch Servicing" in row)
        self.assertNotEqual(cedar_index, birch_index)
        self.assertIn("See the reason above", rows[cedar_index])
        self.assertNotIn("1500 reported", rows[cedar_index])
        self.assertIn("800 reported", rows[birch_index])
        for width, height, name in ((1440, 2400, "desktop"), (390, 3400, "mobile")):
            self._screenshot("C8", width, height, name)

    def test_c10_working_has_no_statement_basis_details(self) -> None:
        collapsed, text, _rows = self._line("C10")
        self.assertIn("3000 reported", text)
        self.assertIn("How the amount was worked out", collapsed)
        self.assertNotIn("What this statement's loan link rests on", text)
        self.assertNotIn("no loan link", text.lower())
        for width, height, name in ((1440, 2200, "desktop"), (390, 3000, "mobile")):
            self._screenshot("C10", width, height, name)

    def test_missing_wording_message_is_visible_for_only_that_saved_answer(self) -> None:
        _, text, rows = self._line("Missing")
        self.assertIn("Recorded answer: yes. Question wording was not saved with this answer.", text)
        self.assertEqual(len(rows), 1)
        self.assertIn("Recorded answer: yes. Question wording was not saved with this answer.", rows[0])

    def test_z1_r1_and_v33_boundary(self) -> None:
        _, z1, _rows = self._line("Z1")
        self.assertIn("Interest reported (worksheet line 1): 3000", z1)
        self.assertIn("Deduction: 0", z1)
        self.assertNotIn("Limit ", z1)
        _, r1, _rows = self._line("R1")
        self.assertIn("See the reason above", r1)
        self.assertNotIn("What this statement's loan link rests on", r1)
        collapsed, expanded, rows = self._line("v33")
        self.assertEqual(collapsed, expanded)
        self.assertEqual(rows, [])
        self.assertNotIn("Statements on this line", expanded)

    def test_malformed_block_is_contained_to_line21(self) -> None:
        model = copy.deepcopy(self._model("C1"))
        valid_page = self._page(model)
        valid_payload = json.dumps(model, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
        malformed = copy.deepcopy(model)
        malformed["line21Explanation"]["working"]["parameters"] = "invalid"
        bad_payload = json.dumps(malformed, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
        boundary = """<script>
          const target = document.createElement('pre'); target.id = 'track2-boundary';
          const line21 = document.querySelector('#line-sch1-21 .line');
          const line10 = document.querySelector('#line-10 .line');
          target.textContent = JSON.stringify({line21Error: !!line21.querySelector('.section-error'),
            line10Error: !!line10.querySelector('.section-error'), line10Text: line10.innerText});
          document.body.appendChild(target);
        </script>"""
        dom = self._dump(valid_page.replace(valid_payload, bad_payload).replace("</body>", boundary + "</body>"),
                         suffix="-malformed")
        self.assertIn("This section's saved explanation could not be displayed safely.", dom)
        observed = __import__("re").search(r'<pre id="track2-boundary">(.*?)</pre>', dom, __import__("re").S)
        self.assertIsNotNone(observed)
        boundary_result = json.loads(html.unescape(observed.group(1)))
        self.assertTrue(boundary_result["line21Error"])
        self.assertFalse(boundary_result["line10Error"])


if __name__ == "__main__":
    unittest.main()
