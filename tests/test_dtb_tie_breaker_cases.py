"""Tests for the 2025 dependent tie-breaker shaping cases and branching behavior.

Asserts on published Form 1040 lines (19, 27a, 28) through the real coordinator:
- Case 1a: Parent (filer) + grandparent; parent claims (filer parent wins categorically).
- Case 1b: Grandparent (filer) + parent; parent waives, grandparent higher AGI (filer wins).
- Case 1c: Grandparent (filer) + parent; parent waives, grandparent lower AGI (filer loses).
- Case 1d: Grandparent (filer) + parent; parent claims (filer loses categorically).
- Case 2: Two unmarried parents living together, filer lower AGI (child does not count for filer
  for any child credit; filer receives childless EIC).
- Case 3a: Two parents living apart, child with filer for more nights (filer wins).
- Case 3b: Two parents living apart, equal nights, filer higher AGI (filer wins).
- Case 3c: Two parents living apart, equal nights, equal AGI (blocks outside class).
- Case 4a: Form 8332 release of exemption (blocks outside class).
- Case 4b: More than one other claimant (blocks outside class).
- Case 6: Residency outside US (fails EIC residency, passes CTC tests and tie-breaker).
- Omitted-answer test per branch: omitting an active question blocks naming it.
- Off-branch test: answering questions off the branch is not required (omitted off-branch
  answers still allow lines 19, 27a, and 28 to publish).
"""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping
import unittest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from tests.test_other_dependents_credit_track1 import (
    LINE19,
    _complete,
    build,
    ctc_child,
    odc_child,
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

PACKAGE_V58 = CONTENT / "package.core-calculations.v58.json"
REGISTRY_V56 = CONTENT / "published-packages.v56.json"
RELEASE_V56 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v56.json"
SURFACE_V58 = PublicationSurface(RELEASE_DIR, REGISTRY_V56, CONTENT)

OD = "tax.us.2025.ctc.no-other-dependent"
LINE27A = "tax.us.2025.payments.line27a"
LINE28 = "tax.us.2025.ctc.form1040-line28"
DTB_RULE = "tax.us.2025.rule.dtb-child.tie-breaker-clear"
DTB_PREFIX = "tax.us.2025.dtb.child."


def _run_return(
    run_id: str,
    *,
    wages: float,
    child_overrides: Mapping[str, str] | None = None,
    dtb_answers: Mapping[str, str],
    extra_return_answers: Mapping[str, str] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    child_answers = ctc_child()
    if child_overrides:
        child_answers.update(child_overrides)
    kids = {"demo-child-1": child_answers}

    ret_answers: dict[str, str] = {
        OD: "yes",
        "tax.us.2025.eic.age-25-under-65": "yes",
        "tax.us.2025.eic.main-home-in-us": "yes",
    }
    if extra_return_answers:
        ret_answers.update(extra_return_answers)

    acts = _complete(build(wages=wages, children=kids, return_answers=ret_answers))

    # Apply EIC child residency override if specified
    if child_overrides and "tax.us.2025.eic.child.residency" in child_overrides:
        for a in acts:
            p = a.get("payload", {})
            if isinstance(p, dict) and "finding" in p:
                f = p["finding"]
                if f.get("fact_id", "").startswith("tax.us.2025.eic.child.residency"):
                    f["value"] = child_overrides["tax.us.2025.eic.child.residency"]

    acts.append(_act(len(acts), "bundle-adoption", {"bundle": _load("dtb-questions.bundle.json")}))
    for k, v in dtb_answers.items():
        fid = f"{DTB_PREFIX}{k}|child=demo-child-1,tax-year=2025"
        acts.append(_act(len(acts), "assertion", {"finding": _attested(f"demo.dtb.{k}", fid, v)}))

    finished = _finish(
        acts,
        package_path=PACKAGE_V58,
        package_version="v58",
        release_path=RELEASE_V56,
        release_version="v56",
        note=run_id,
    )
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=finished,
            workspace_revision=len(finished),
            run_scope={"jurisdiction": "us", "year": "2025"},
            scope_user="demo.user.filer-1",
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=SURFACE_V58,
            output_name="out.json",
        )
        pubs = {str(pub.finding["symbol"]): pub.finding for pub in outcome.publications or ()}
        report = json.loads(outcome.output_path.read_text(encoding="utf-8")) if outcome.output_path else {}
    return pubs, report


class TieBreakerShapingCases(unittest.TestCase):
    def test_case1a_parent_claims_filer_parent_wins(self) -> None:
        """Case 1a: Parent (filer) + grandparent; parent claims (parent wins under § 152(c)(4)(A)(i))."""
        pubs, report = _run_return("case1a", wages=30000.0, dtb_answers={
            "another-could-claim": "yes",
            "multiple-other-claimants": "no",
            "filer-is-parent": "yes",
            "other-is-parent": "no",
        })
        self.assertEqual(int(pubs[LINE19]["value"]), 1475)
        self.assertEqual(int(pubs[LINE27A]["value"]), 3261)
        self.assertEqual(int(pubs[LINE28]["value"]), 725)

    def test_case1b_nonparent_filer_parent_waives_higher_agi_wins(self) -> None:
        """Case 1b: Grandparent (filer) + parent; parent does not claim, grandparent AGI > parent."""
        pubs, report = _run_return("case1b", wages=30000.0, dtb_answers={
            "another-could-claim": "yes",
            "multiple-other-claimants": "no",
            "filer-is-parent": "no",
            "other-is-parent": "yes",
            "other-will-claim": "no",
            "filer-agi-higher": "yes",
        })
        self.assertEqual(int(pubs[LINE19]["value"]), 1475)
        self.assertEqual(int(pubs[LINE27A]["value"]), 3261)
        self.assertEqual(int(pubs[LINE28]["value"]), 725)

    def test_case1c_nonparent_filer_parent_waives_lower_agi_loses(self) -> None:
        """Case 1c: Grandparent (filer) + parent; parent does not claim, grandparent AGI not higher."""
        pubs, report = _run_return("case1c", wages=30000.0, dtb_answers={
            "another-could-claim": "yes",
            "multiple-other-claimants": "no",
            "filer-is-parent": "no",
            "other-is-parent": "yes",
            "other-will-claim": "no",
            "filer-agi-higher": "no",
        })
        self.assertEqual(int(pubs[LINE19]["value"]), 0)
        self.assertEqual(int(pubs[LINE27A]["value"]), 0)
        self.assertEqual(int(pubs[LINE28]["value"]), 0)

    def test_case1d_nonparent_filer_parent_claims_filer_loses(self) -> None:
        """Case 1d: Grandparent (filer) + parent; parent claims (filer loses under § 152(c)(4)(A)(i))."""
        pubs, report = _run_return("case1d", wages=30000.0, dtb_answers={
            "another-could-claim": "yes",
            "multiple-other-claimants": "no",
            "filer-is-parent": "no",
            "other-is-parent": "yes",
            "other-will-claim": "yes",
        })
        self.assertEqual(int(pubs[LINE19]["value"]), 0)
        self.assertEqual(int(pubs[LINE27A]["value"]), 0)
        self.assertEqual(int(pubs[LINE28]["value"]), 0)

    def test_case2_two_parents_living_together_lower_agi_loses_gets_childless_eic(self) -> None:
        """Case 2: Two unmarried parents living together, filer lower AGI.

        Child does not count for filer for any of the 3 child credits ($0 CTC, $0 ACTC).
        Filer receives statutory childless EIC ($542 at $12,000 wages).
        """
        pubs, report = _run_return("case2", wages=12000.0, dtb_answers={
            "another-could-claim": "yes",
            "multiple-other-claimants": "no",
            "filer-is-parent": "yes",
            "other-is-parent": "yes",
            "form-8332-released": "no",
            "more-nights-with-filer": "no",
            "same-nights": "yes",
            "filer-agi-higher": "no",
            "same-agi": "no",
            "other-will-claim": "yes",
        })
        self.assertEqual(int(pubs[LINE19]["value"]), 0)
        self.assertEqual(int(pubs[LINE28]["value"]), 0)
        self.assertEqual(int(pubs[LINE27A]["value"]), 542)

    def test_case3a_two_parents_living_apart_more_nights_wins(self) -> None:
        """Case 3a: Two parents living apart, child with filer for more nights (§ 152(c)(4)(B)(i))."""
        pubs, report = _run_return("case3a", wages=30000.0, dtb_answers={
            "another-could-claim": "yes",
            "multiple-other-claimants": "no",
            "filer-is-parent": "yes",
            "other-is-parent": "yes",
            "form-8332-released": "no",
            "more-nights-with-filer": "yes",
        })
        self.assertEqual(int(pubs[LINE19]["value"]), 1475)
        self.assertEqual(int(pubs[LINE27A]["value"]), 3261)
        self.assertEqual(int(pubs[LINE28]["value"]), 725)

    def test_case3b_two_parents_living_apart_equal_nights_higher_agi_wins(self) -> None:
        """Case 3b: Two parents living apart, equal nights, filer higher AGI (§ 152(c)(4)(B)(ii))."""
        pubs, report = _run_return("case3b", wages=30000.0, dtb_answers={
            "another-could-claim": "yes",
            "multiple-other-claimants": "no",
            "filer-is-parent": "yes",
            "other-is-parent": "yes",
            "form-8332-released": "no",
            "more-nights-with-filer": "no",
            "same-nights": "yes",
            "filer-agi-higher": "yes",
        })
        self.assertEqual(int(pubs[LINE19]["value"]), 1475)
        self.assertEqual(int(pubs[LINE27A]["value"]), 3261)
        self.assertEqual(int(pubs[LINE28]["value"]), 725)

    def test_case3c_two_parents_equal_nights_equal_agi_blocks_outside_class(self) -> None:
        """Case 3c: Two parents living apart, equal nights, equal AGI (sources silent on tie)."""
        pubs, report = _run_return("case3c", wages=30000.0, dtb_answers={
            "another-could-claim": "yes",
            "multiple-other-claimants": "no",
            "filer-is-parent": "yes",
            "other-is-parent": "yes",
            "form-8332-released": "no",
            "more-nights-with-filer": "no",
            "same-nights": "yes",
            "filer-agi-higher": "no",
            "other-will-claim": "yes",
            "same-agi": "yes",
        })
        disp = next(d for d in report["dispositions"] if d.get("artifact_id") == DTB_RULE)
        self.assertEqual(disp["disposition"], "blocked")
        self.assertEqual(disp["code"], "DEPENDENCY_INVALID")
        self.assertNotIn(LINE19, pubs)
        self.assertNotIn(LINE27A, pubs)
        self.assertNotIn(LINE28, pubs)

    def test_reproduction_two_parents_equal_nights_same_agi_other_waives_filer_wins(self) -> None:
        """Reproduction 1 (Row 12 + other-will-claim=no): filer wins, lines 19, 27a, 28 publish."""
        pubs, report = _run_return("rep1_two_parents_other_waives", wages=30000.0, dtb_answers={
            "another-could-claim": "yes",
            "multiple-other-claimants": "no",
            "filer-is-parent": "yes",
            "other-is-parent": "yes",
            "form-8332-released": "no",
            "more-nights-with-filer": "no",
            "same-nights": "yes",
            "filer-agi-higher": "no",
            "same-agi": "yes",
            "other-will-claim": "no",
        })
        self.assertIn(LINE19, pubs)
        self.assertIn(LINE27A, pubs)
        self.assertIn(LINE28, pubs)
        self.assertEqual(int(pubs[LINE19]["value"]), 1475)
        self.assertEqual(int(pubs[LINE27A]["value"]), 3261)
        self.assertEqual(int(pubs[LINE28]["value"]), 725)

    def test_reproduction_two_non_parents_same_agi_other_waives_filer_wins(self) -> None:
        """Reproduction 2 (Row 16 + other-will-claim=no): filer wins, lines 19, 27a, 28 publish."""
        pubs, report = _run_return("rep2_two_non_parents_other_waives", wages=30000.0, dtb_answers={
            "another-could-claim": "yes",
            "multiple-other-claimants": "no",
            "filer-is-parent": "no",
            "other-is-parent": "no",
            "filer-agi-higher": "no",
            "same-agi": "yes",
            "other-will-claim": "no",
        })
        self.assertIn(LINE19, pubs)
        self.assertIn(LINE27A, pubs)
        self.assertIn(LINE28, pubs)
        self.assertEqual(int(pubs[LINE19]["value"]), 1475)
        self.assertEqual(int(pubs[LINE27A]["value"]), 3261)
        self.assertEqual(int(pubs[LINE28]["value"]), 725)

    def test_reproduction_two_parents_equal_nights_other_waives_same_agi_omitted_filer_wins(self) -> None:
        """Reproduction 3 (Row 13 with same-agi omitted): filer wins, lines 19, 27a, 28 publish."""
        pubs, report = _run_return("rep3_same_agi_omitted", wages=30000.0, dtb_answers={
            "another-could-claim": "yes",
            "multiple-other-claimants": "no",
            "filer-is-parent": "yes",
            "other-is-parent": "yes",
            "form-8332-released": "no",
            "more-nights-with-filer": "no",
            "same-nights": "yes",
            "filer-agi-higher": "no",
            "other-will-claim": "no",
        })
        self.assertIn(LINE19, pubs)
        self.assertIn(LINE27A, pubs)
        self.assertIn(LINE28, pubs)
        self.assertEqual(int(pubs[LINE19]["value"]), 1475)
        self.assertEqual(int(pubs[LINE27A]["value"]), 3261)
        self.assertEqual(int(pubs[LINE28]["value"]), 725)

    def test_case4a_form_8332_released_blocks_outside_class(self) -> None:
        """Case 4a: Form 8332 released blocks cleanly outside class by answer."""
        pubs, report = _run_return("case4a", wages=30000.0, dtb_answers={
            "another-could-claim": "yes",
            "multiple-other-claimants": "no",
            "filer-is-parent": "yes",
            "other-is-parent": "yes",
            "form-8332-released": "yes",
        })
        disp = next(d for d in report["dispositions"] if d.get("artifact_id") == DTB_RULE)
        self.assertEqual(disp["disposition"], "blocked")
        self.assertEqual(disp["code"], "DEPENDENCY_INVALID")
        self.assertNotIn(LINE19, pubs)
        self.assertNotIn(LINE27A, pubs)
        self.assertNotIn(LINE28, pubs)

    def test_case4b_multiple_other_claimants_blocks_outside_class(self) -> None:
        """Case 4b: More than one other claimant blocks cleanly outside class by answer."""
        pubs, report = _run_return("case4b", wages=30000.0, dtb_answers={
            "another-could-claim": "yes",
            "multiple-other-claimants": "yes",
        })
        disp = next(d for d in report["dispositions"] if d.get("artifact_id") == DTB_RULE)
        self.assertEqual(disp["disposition"], "blocked")
        self.assertEqual(disp["code"], "DEPENDENCY_INVALID")
        self.assertNotIn(LINE19, pubs)
        self.assertNotIn(LINE27A, pubs)
        self.assertNotIn(LINE28, pubs)

    def test_case6_residency_outside_us_ctc_passes_eic_fails(self) -> None:
        """Case 6: US citizen child living outside US fails EIC residency, passes CTC & tie-breaker."""
        pubs, report = _run_return("case6", wages=30000.0, child_overrides={
            "tax.us.2025.eic.child.residency": "no",
        }, dtb_answers={
            "another-could-claim": "no",
        })
        # Passes CTC & ACTC, fails EIC
        self.assertEqual(int(pubs[LINE19]["value"]), 1475)
        self.assertEqual(int(pubs[LINE28]["value"]), 725)
        self.assertEqual(int(pubs[LINE27A]["value"]), 0)



    def test_case_odc_child_lost_to_tie_breaker_publishes_zero_and_line19(self) -> None:
        """Finding 2: A child marked for ODC who loses the tie-breaker publishes 0 and line 19 publishes."""
        acts = _complete(build(wages=30000.0, children={"demo-child-1": odc_child()}))
        acts.append(_act(len(acts), "bundle-adoption", {"bundle": _load("dtb-questions.bundle.json")}))
        for k, v in {
            "another-could-claim": "yes",
            "multiple-other-claimants": "no",
            "filer-is-parent": "no",
            "other-is-parent": "yes",
            "other-will-claim": "yes",
        }.items():
            acts.append(_act(len(acts), "assertion", {"finding": _attested(
                f"demo.dtb.{k}", f"{DTB_PREFIX}{k}|child=demo-child-1,tax-year=2025", v
            )}))
        fin = _finish(
            acts,
            package_path=PACKAGE_V58,
            package_version="v58",
            release_path=RELEASE_V56,
            release_version="v56",
            note="odc-lost-child",
        )
        with TemporaryDirectory() as tmp:
            out = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "L"),
                repo_root=ROOT,
                authoritative_acts=fin,
                workspace_revision=len(fin),
                run_scope={"jurisdiction": "us", "year": "2025"},
                scope_user="demo.user.filer-1",
                request={"schema": "run-request.v1"},
                run_id="odc-lost-child",
                governance_pins=[],
                surface=SURFACE_V58,
                output_name="out.json",
            )
            pubs = {str(p.finding["symbol"]): p.finding["value"] for p in out.publications or ()}
            assert out.output_path is not None
            rep = json.loads(out.output_path.read_text())

        dtb_disp = next(d for d in rep["dispositions"] if d["artifact_id"] == DTB_RULE)
        self.assertEqual(dtb_disp["disposition"], "published")

        odc_counts_disp = next(d for d in rep["dispositions"] if d["artifact_id"] == "tax.us.2025.rule.odc-child.counts")
        self.assertEqual(odc_counts_disp["disposition"], "published")

        odc_count_disp = next(d for d in rep["dispositions"] if d["artifact_id"] == "tax.us.2025.rule.odc-child-count")
        self.assertEqual(odc_count_disp["disposition"], "published")

        self.assertIn(LINE19, pubs)
        self.assertEqual(int(pubs[LINE19]), 0)
        self.assertIn(LINE27A, pubs)
        self.assertEqual(int(pubs[LINE27A]), 0)
        self.assertIn(LINE28, pubs)
        self.assertEqual(int(pubs[LINE28]), 0)


class TieBreakerBranchingAndOmission(unittest.TestCase):
    def test_omitted_active_question_on_branch_blocks_naming_it(self) -> None:
        cases: list[tuple[str, dict[str, str], str]] = [
            ("root", {}, "another-could-claim"),
            ("multi", {"another-could-claim": "yes"}, "multiple-other-claimants"),
            ("filer_is_parent", {
                "another-could-claim": "yes", "multiple-other-claimants": "no",
            }, "filer-is-parent"),
            ("other_parent", {
                "another-could-claim": "yes", "multiple-other-claimants": "no",
                "filer-is-parent": "yes",
            }, "other-is-parent"),
            ("8332", {
                "another-could-claim": "yes", "multiple-other-claimants": "no",
                "filer-is-parent": "yes", "other-is-parent": "yes",
            }, "form-8332-released"),
            ("more_nights", {
                "another-could-claim": "yes", "multiple-other-claimants": "no",
                "filer-is-parent": "yes", "other-is-parent": "yes", "form-8332-released": "no",
            }, "more-nights-with-filer"),
            ("same_nights", {
                "another-could-claim": "yes", "multiple-other-claimants": "no",
                "filer-is-parent": "yes", "other-is-parent": "yes", "form-8332-released": "no",
                "more-nights-with-filer": "no",
            }, "same-nights"),
            ("parent_fewer_nights_other_claim", {
                "another-could-claim": "yes", "multiple-other-claimants": "no",
                "filer-is-parent": "yes", "other-is-parent": "yes", "form-8332-released": "no",
                "more-nights-with-filer": "no", "same-nights": "no",
            }, "other-will-claim"),
            ("parent_agi", {
                "another-could-claim": "yes", "multiple-other-claimants": "no",
                "filer-is-parent": "yes", "other-is-parent": "yes", "form-8332-released": "no",
                "more-nights-with-filer": "no", "same-nights": "yes",
            }, "filer-agi-higher"),
            ("parent_equal_nights_other_claim", {
                "another-could-claim": "yes", "multiple-other-claimants": "no",
                "filer-is-parent": "yes", "other-is-parent": "yes", "form-8332-released": "no",
                "more-nights-with-filer": "no", "same-nights": "yes",
                "filer-agi-higher": "no",
            }, "other-will-claim"),
            ("parent_equal_nights_same_agi", {
                "another-could-claim": "yes", "multiple-other-claimants": "no",
                "filer-is-parent": "yes", "other-is-parent": "yes", "form-8332-released": "no",
                "more-nights-with-filer": "no", "same-nights": "yes",
                "filer-agi-higher": "no", "other-will-claim": "yes",
            }, "same-agi"),
            ("np_other_claim", {
                "another-could-claim": "yes", "multiple-other-claimants": "no",
                "filer-is-parent": "no", "other-is-parent": "yes",
            }, "other-will-claim"),
            ("np_agi", {
                "another-could-claim": "yes", "multiple-other-claimants": "no",
                "filer-is-parent": "no", "other-is-parent": "yes", "other-will-claim": "no",
            }, "filer-agi-higher"),
            ("two_non_parents_agi", {
                "another-could-claim": "yes", "multiple-other-claimants": "no",
                "filer-is-parent": "no", "other-is-parent": "no",
            }, "filer-agi-higher"),
            ("two_non_parents_other_claim", {
                "another-could-claim": "yes", "multiple-other-claimants": "no",
                "filer-is-parent": "no", "other-is-parent": "no",
                "filer-agi-higher": "no",
            }, "other-will-claim"),
            ("two_non_parents_same_agi", {
                "another-could-claim": "yes", "multiple-other-claimants": "no",
                "filer-is-parent": "no", "other-is-parent": "no",
                "filer-agi-higher": "no", "other-will-claim": "yes",
            }, "same-agi"),
        ]
        for name, answers, expected_missing in cases:
            with self.subTest(omitted=name):
                pubs, report = _run_return(f"omitted_{name}", wages=30000.0, dtb_answers=answers)
                disp = next(d for d in report["dispositions"] if d.get("artifact_id") == DTB_RULE)
                self.assertEqual(disp["disposition"], "blocked")
                self.assertEqual(disp["code"], "DEPENDENCY_ABSENT")
                self.assertIn(f"{DTB_PREFIX}{expected_missing}", disp["missing"])
                self.assertNotIn(LINE19, pubs)
                self.assertNotIn(LINE27A, pubs)
                self.assertNotIn(LINE28, pubs)

    def test_off_branch_answers_are_not_required_lines_publish_cleanly(self) -> None:
        """In winning or decided cases, answering questions off the branch is not required."""
        # Uncontested child: zero subordinate answers provided, lines publish cleanly
        pubs, report = _run_return("offbranch_uncontested", wages=30000.0, dtb_answers={
            "another-could-claim": "no",
        })
        self.assertEqual(int(pubs[LINE19]["value"]), 1475)
        self.assertEqual(int(pubs[LINE27A]["value"]), 3261)
        self.assertEqual(int(pubs[LINE28]["value"]), 725)

        # Parent over non-parent: residence, AGI, Form 8332, etc. all omitted, lines publish cleanly
        pubs, report = _run_return("offbranch_parent_wins", wages=30000.0, dtb_answers={
            "another-could-claim": "yes",
            "multiple-other-claimants": "no",
            "filer-is-parent": "yes",
            "other-is-parent": "no",
        })
        self.assertEqual(int(pubs[LINE19]["value"]), 1475)
        self.assertEqual(int(pubs[LINE27A]["value"]), 3261)
        self.assertEqual(int(pubs[LINE28]["value"]), 725)

        # Two parents, more nights: AGI, same nights, etc. omitted, lines publish cleanly
        pubs, report = _run_return("offbranch_nights_wins", wages=30000.0, dtb_answers={
            "another-could-claim": "yes",
            "multiple-other-claimants": "no",
            "filer-is-parent": "yes",
            "other-is-parent": "yes",
            "form-8332-released": "no",
            "more-nights-with-filer": "yes",
        })
        self.assertEqual(int(pubs[LINE19]["value"]), 1475)
        self.assertEqual(int(pubs[LINE27A]["value"]), 3261)
        self.assertEqual(int(pubs[LINE28]["value"]), 725)
