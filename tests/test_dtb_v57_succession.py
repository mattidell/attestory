"""Regression test for succession from core v57 to v58.

Under Contract item 5 (as amended):
A v57 answer set on v58 is asked the one root question,
'another person could also claim this child', for each child, and blocks
naming it until answered; with 'no' on every child it then keeps every v57 result.
The regression test runs the v57 answer set on v58, asserts the block names only
that question, adds 'no' per child, and asserts the published lines
(Form 1040 lines 19, 27a, and 28) equal v57's.
"""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from tests.test_other_dependents_credit_track1 import (
    LINE19,
    _complete,
    build,
    ctc_child,
)
from tests.test_refund_or_amount_owed_track1 import (
    _act,
    _attested,
    _finish,
    _load,
)

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages/content/tax/2025"
RELEASE_DIR = ROOT / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"

PACKAGE_V57 = CONTENT / "package.core-calculations.v57.json"
REGISTRY_V55 = CONTENT / "published-packages.v55.json"
RELEASE_V55 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v55.json"
SURFACE_V57 = PublicationSurface(RELEASE_DIR, REGISTRY_V55, CONTENT)

PACKAGE_V58 = CONTENT / "package.core-calculations.v58.json"
REGISTRY_V56 = CONTENT / "published-packages.v56.json"
RELEASE_V56 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v56.json"
SURFACE_V58 = PublicationSurface(RELEASE_DIR, REGISTRY_V56, CONTENT)

OD = "tax.us.2025.ctc.no-other-dependent"
LINE27A = "tax.us.2025.payments.line27a"
LINE28 = "tax.us.2025.ctc.form1040-line28"
ROOT_QUESTION = "tax.us.2025.dtb.child.another-could-claim"
DTB_RULE = "tax.us.2025.rule.dtb-child.tie-breaker-clear"


class V57SuccessionTest(unittest.TestCase):
    def test_v57_answer_set_on_v58_blocks_only_on_root_question_and_recovers_exact_lines(self) -> None:
        kids = {
            "demo-child-1": ctc_child(),
            "demo-child-2": ctc_child(),
        }
        acts = _complete(build(wages=30000.0, children=kids, return_answers={OD: "yes"}))

        # 1. Run v57 answer set on v57
        finished_v57 = _finish(
            acts,
            package_path=PACKAGE_V57,
            package_version="v57",
            release_path=RELEASE_V55,
            release_version="v55",
            note="v57-baseline",
        )
        with TemporaryDirectory() as tmp:
            outcome_v57 = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "L"),
                repo_root=ROOT,
                authoritative_acts=finished_v57,
                workspace_revision=len(finished_v57),
                run_scope={"jurisdiction": "us", "year": "2025"},
                scope_user="demo.user.filer-1",
                request={"schema": "run-request.v1"},
                run_id="v57-baseline",
                governance_pins=[],
                surface=SURFACE_V57,
                output_name="out.json",
            )
            pubs_v57 = {str(pub.finding["symbol"]): pub.finding for pub in outcome_v57.publications or ()}

        v57_l19 = pubs_v57[LINE19]["value"]
        v57_l27a = pubs_v57[LINE27A]["value"]
        v57_l28 = pubs_v57[LINE28]["value"]

        # 2. Run the exact same v57 answer set on v58 without DTB answers
        finished_v58_raw = _finish(
            acts,
            package_path=PACKAGE_V58,
            package_version="v58",
            release_path=RELEASE_V56,
            release_version="v56",
            note="v58-unanswered",
        )
        with TemporaryDirectory() as tmp:
            outcome_v58_raw = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "L"),
                repo_root=ROOT,
                authoritative_acts=finished_v58_raw,
                workspace_revision=len(finished_v58_raw),
                run_scope={"jurisdiction": "us", "year": "2025"},
                scope_user="demo.user.filer-1",
                request={"schema": "run-request.v1"},
                run_id="v58-unanswered",
                governance_pins=[],
                surface=SURFACE_V58,
                output_name="out.json",
            )
            assert outcome_v58_raw.output_path is not None
            report_v58_raw = json.loads(outcome_v58_raw.output_path.read_text(encoding="utf-8"))

        dtb_blocks = [
            disp for disp in report_v58_raw.get("dispositions", [])
            if disp.get("artifact_id") == DTB_RULE
        ]
        self.assertEqual(len(dtb_blocks), len(kids))
        for disp in dtb_blocks:
            self.assertEqual(disp.get("disposition"), "blocked")
            self.assertEqual(disp.get("code"), "DEPENDENCY_ABSENT")
            self.assertEqual(disp.get("missing"), [ROOT_QUESTION])

        # 3. Add DTB bundle adoption and 'no' to the root question for each child
        acts_with_dtb = list(acts)
        acts_with_dtb.append(_act(len(acts_with_dtb), "bundle-adoption", {"bundle": _load("dtb-questions.bundle.json")}))
        for child in kids:
            fid = f"{ROOT_QUESTION}|child={child},tax-year=2025"
            acts_with_dtb.append(_act(len(acts_with_dtb), "assertion", {
                "finding": _attested(f"demo.dtb.ans.{child}", fid, "no")
            }))

        finished_v58_answered = _finish(
            acts_with_dtb,
            package_path=PACKAGE_V58,
            package_version="v58",
            release_path=RELEASE_V56,
            release_version="v56",
            note="v58-answered",
        )
        with TemporaryDirectory() as tmp:
            outcome_v58_answered = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "L"),
                repo_root=ROOT,
                authoritative_acts=finished_v58_answered,
                workspace_revision=len(finished_v58_answered),
                run_scope={"jurisdiction": "us", "year": "2025"},
                scope_user="demo.user.filer-1",
                request={"schema": "run-request.v1"},
                run_id="v58-answered",
                governance_pins=[],
                surface=SURFACE_V58,
                output_name="out.json",
            )
            pubs_v58_answered = {str(pub.finding["symbol"]): pub.finding for pub in outcome_v58_answered.publications or ()}

        self.assertEqual(pubs_v58_answered[LINE19]["value"], v57_l19)
        self.assertEqual(pubs_v58_answered[LINE27A]["value"], v57_l27a)
        self.assertEqual(pubs_v58_answered[LINE28]["value"], v57_l28)

    def test_v57_childless_return_on_v58_asks_no_new_questions_and_lines_equal(self) -> None:
        """A childless v57 answer set on v58 is asked zero new questions and lines equal v57."""
        return_answers = {
            OD: "yes",
            "tax.us.2025.eic.age-25-under-65": "yes",
            "tax.us.2025.eic.main-home-in-us": "yes",
        }
        acts = _complete(build(wages=15000.0, children={}, return_answers=return_answers))

        finished_v57 = _finish(
            acts,
            package_path=PACKAGE_V57,
            package_version="v57",
            release_path=RELEASE_V55,
            release_version="v55",
            note="v57-childless",
        )
        with TemporaryDirectory() as tmp:
            outcome_v57 = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "L"),
                repo_root=ROOT,
                authoritative_acts=finished_v57,
                workspace_revision=len(finished_v57),
                run_scope={"jurisdiction": "us", "year": "2025"},
                scope_user="demo.user.filer-1",
                request={"schema": "run-request.v1"},
                run_id="v57-childless",
                governance_pins=[],
                surface=SURFACE_V57,
                output_name="out.json",
            )
            pubs_v57 = {str(pub.finding["symbol"]): pub.finding for pub in outcome_v57.publications or ()}

        finished_v58 = _finish(
            acts,
            package_path=PACKAGE_V58,
            package_version="v58",
            release_path=RELEASE_V56,
            release_version="v56",
            note="v58-childless",
        )
        with TemporaryDirectory() as tmp:
            outcome_v58 = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "L"),
                repo_root=ROOT,
                authoritative_acts=finished_v58,
                workspace_revision=len(finished_v58),
                run_scope={"jurisdiction": "us", "year": "2025"},
                scope_user="demo.user.filer-1",
                request={"schema": "run-request.v1"},
                run_id="v58-childless",
                governance_pins=[],
                surface=SURFACE_V58,
                output_name="out.json",
            )
            pubs_v58 = {str(pub.finding["symbol"]): pub.finding for pub in outcome_v58.publications or ()}
            assert outcome_v58.output_path is not None
            report_v58 = json.loads(outcome_v58.output_path.read_text(encoding="utf-8"))

        dtb_blocks = [
            disp for disp in report_v58.get("dispositions", [])
            if disp.get("artifact_id") == DTB_RULE
        ]
        self.assertEqual(len(dtb_blocks), 0)

        for line in (LINE19, LINE27A, LINE28):
            if line in pubs_v57:
                self.assertIn(line, pubs_v58)
                self.assertEqual(pubs_v58[line]["value"], pubs_v57[line]["value"])
            else:
                self.assertNotIn(line, pubs_v58)
