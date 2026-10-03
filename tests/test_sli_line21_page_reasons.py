"""A blocked line that says why is not also given the generic explanation.

The citation-walk page (``packages/presentation/pages/citation-walk.v1.html``)
shows a blocked line's "Why:" list when the presentation model carries
reasons for it. That list is the line's explanation. The field's generic
blocked sentence and the generic "Remedy: contribute the missing dependency"
would contradict it, for example when the person answered "no" and nothing is
missing, so the page omits both on that line only. A blocked line without
reasons keeps both.

The page is filled by ``live_session._render_page``, as a live session fills
it, and opened in a headless Chromium. The test is skipped when no Chromium is
present.
"""
from __future__ import annotations

import copy
import html
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.live_session import _render_page
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.presentation_projection import validate_presentation_model

ROOT = Path(__file__).resolve().parents[1]
MODEL = (ROOT / "packages" / "sample_data" / "f1098e_student_loan_interest_track6" / "presentation"
         / "universal-violation.presentation-model.v1.json")
LINE21 = "line-sch1-21"
OTHER_BLOCKED = "line-10"
REMEDY = "Remedy:"
SENTENCE = ("You said the student was not enrolled at least half-time in a degree or certificate program "
            "during the schooling this loan paid for. The deduction is worked out here only when they were. "
            "If that answer is wrong, change it.")


def _browser() -> str | None:
    candidates = [
        *sorted(Path.home().glob("Library/Caches/ms-playwright/chromium_headless_shell-*/"
                                 "chrome-headless-shell-*/chrome-headless-shell"), reverse=True),
        *sorted(Path.home().glob(".cache/ms-playwright/chromium_headless_shell-*/"
                                 "chrome-headless-shell-*/chrome-headless-shell"), reverse=True),
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
    ]
    found = next((str(path) for path in candidates if path.is_file()), None)
    return found or shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")


BROWSER = _browser()


def _line_text(dom: str, label: str) -> str:
    """The visible text of the one section whose heading starts with ``label``."""
    for chunk in re.findall(r"<section\b.*?</section>", dom, re.S):
        heading = re.search(r"<h2[^>]*>(.*?)</h2>", chunk, re.S)
        if heading and re.sub(r"<[^>]+>", "", heading.group(1)).startswith(label):
            return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", chunk))).strip()
    raise AssertionError(f"no rendered section for {label!r}")


@unittest.skipIf(BROWSER is None, "no headless Chromium available")
class BlockedLineExplanation(unittest.TestCase):

    def setUp(self) -> None:
        self.model: dict[str, Any] = json.loads(MODEL.read_text("utf-8"))
        self.sections = {section["id"]: section for section in self.model["sections"]}
        self.assertEqual(self.sections[LINE21]["resolved"]["disposition"], "blocked")
        self.assertEqual(self.sections[OTHER_BLOCKED]["resolved"]["disposition"], "blocked")

    def _render(self, model: dict[str, Any]) -> str:
        validate_presentation_model(model)
        with tempfile.TemporaryDirectory(prefix="sli-line21-page-") as work:
            workspace = Path(work) / "workspace"
            workspace.mkdir()
            model_path = workspace / "model.json"
            model_path.write_text(json.dumps(model), "utf-8")
            page = Path(work) / "page.html"
            page.write_bytes(_render_page(ROOT, WorkspaceCapability(workspace), model_path))
            done = subprocess.run(
                [str(BROWSER), "--headless", "--disable-gpu", "--no-sandbox", f"--user-data-dir={work}/profile",
                 "--virtual-time-budget=5000", "--dump-dom", page.as_uri()],
                capture_output=True, text=True, timeout=60, check=True)
        self.assertIn("<section", done.stdout)
        return done.stdout

    def _label(self, section_id: str) -> str:
        field = self.sections[section_id]["field"]
        return f"{field['label']} (Line {field['line']})"

    def _explain(self, section_id: str) -> str:
        explain: str = self.sections[section_id]["field"]["dispositions"]["blocked"]["explain"]
        return explain

    def test_a_blocked_line_with_reasons_shows_only_its_reasons(self) -> None:
        model = copy.deepcopy(self.model)
        [line21] = [section for section in model["sections"] if section["id"] == LINE21]
        line21["resolved"]["reasons"] = [{
            "sentence": SENTENCE,
            "statementLabel": {"statement": "2025 Form 1098-E from Cedar", "lender": "Cedar Servicing"},
        }]
        dom = self._render(model)

        text = _line_text(dom, self._label(LINE21))
        self.assertIn("No value published — cannot compute.", text)
        self.assertIn(f"Why: 2025 Form 1098-E from Cedar, Cedar Servicing: {SENTENCE}", text)
        self.assertNotIn(self._explain(LINE21), text)
        self.assertNotIn(REMEDY, text)

        # Another blocked line, without reasons, is unchanged.
        other = _line_text(dom, self._label(OTHER_BLOCKED))
        self.assertIn(self._explain(OTHER_BLOCKED), other)
        self.assertIn(REMEDY, other)
        self.assertNotIn("Why:", other)

    def test_a_blocked_line_without_reasons_keeps_the_generic_explanation(self) -> None:
        text = _line_text(self._render(self.model), self._label(LINE21))
        self.assertIn("No value published — cannot compute.", text)
        self.assertIn(self._explain(LINE21), text)
        self.assertIn(REMEDY, text)
        self.assertNotIn("Why:", text)


if __name__ == "__main__":
    unittest.main()
