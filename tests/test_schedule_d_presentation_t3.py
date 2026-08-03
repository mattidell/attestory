"""Track 3 Schedule D presentation goldens: form-field projection through the
existing citation-walk presentation model, against package v13/v8.

Covers the ordinary form-field binds_symbol projection (line 8a column (h),
line 13, line 15, line 16; line 7a/9/16 unchanged from Track 2/ADR-0055) and
the attachment's own three-state disposition (ADR-0056): published,
blocked, and not-required are all now visible in the model's ``attachments``
list, while ``citationGroups`` continues to carry only published itemization
detail, unchanged.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from tests.test_schedule_d_covered_ltcg_8a_t2_coordinator import _sdcl_t2_acts, BOUNDARY_DECLARATIONS

REPO = Path(__file__).resolve().parent.parent
CONTENT = REPO / "packages" / "content" / "tax" / "2025"
FIXTURES = REPO / "packages" / "sample_data" / "schedule_d_covered_ltcg_8a_t2"
SD_ATTACHMENT_ID = "tax.us.2025.rule.attachment.schedule-d"


def _surface() -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases", CONTENT / "published-packages.v8.json", CONTENT
    )


def _run_model(run_id: str, acts: list[dict[str, object]]) -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO, authoritative_acts=acts,
            workspace_revision=len(acts), run_scope={"jurisdiction": "us", "year": "2059"},
            scope_user="demo.user.filer-1", request={"schema": "run-request.v1"}, run_id=run_id,
            governance_pins=[], surface=_surface(), output_name="out.json",
        )
        assert outcome.refusal is None, outcome.refusal
        assert outcome.presentation_path is not None
        return cast(dict[str, Any], json.loads(outcome.presentation_path.read_text("utf-8")))


def _sections_by_id(model: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {s["id"]: s for s in model["sections"]}


class EligibleScheduleDPublishes(unittest.TestCase):
    def test_line8a_13_15_16_and_line7a_9_16_all_publish(self) -> None:
        model = _run_model("demo.sdcl.t3.eligible", _sdcl_t2_acts(
            box2a=None, close_2a=True, eligible_txn=True, adoption_file="adopt-core-v13-current.json",
        ))
        sections = _sections_by_id(model)
        self.assertEqual(sections["line-8a-h"]["resolved"]["value"], 4000)
        self.assertEqual(sections["line-sch-d-13"]["resolved"]["value"], 0)
        self.assertEqual(sections["line-sch-d-15"]["resolved"]["value"], 4000)
        self.assertEqual(sections["line-sch-d-16"]["resolved"]["value"], 4000)
        self.assertEqual(sections["line-7a"]["resolved"]["value"], 4000)
        self.assertEqual(sections["line-9"]["resolved"]["disposition"], "published_value")
        self.assertEqual(sections["line-16"]["resolved"]["disposition"], "published_value")
        group_ids = {g["id"] for g in model["citationGroups"]}
        self.assertIn(SD_ATTACHMENT_ID, group_ids)
        attachment = next(g for g in model["citationGroups"] if g["id"] == SD_ATTACHMENT_ID)
        self.assertEqual(len(attachment["parts"]), 3)  # (d), (e), line 13
        attachments_by_id = {a["id"]: a for a in model["attachments"]}
        self.assertEqual(attachments_by_id[SD_ATTACHMENT_ID]["resolved"]["disposition"], "published")


class BothGainsNoDoubleCount(unittest.TestCase):
    def test_box2a_and_eligible_transaction_flow_through_once(self) -> None:
        model = _run_model("demo.sdcl.t3.both-gains", _sdcl_t2_acts(
            box2a=500, close_2a=True, eligible_txn=True, adoption_file="adopt-core-v13-current.json",
        ))
        sections = _sections_by_id(model)
        self.assertEqual(sections["line-sch-d-13"]["resolved"]["value"], 500)
        self.assertEqual(sections["line-sch-d-15"]["resolved"]["value"], 4500)


class NotRequiredCase(unittest.TestCase):
    """Eligible family closed-empty: the attachment is not-required. It stays
    out of citationGroups (no itemization detail to show), and ADR-0056 now
    shows it as a visible guard_inapplicable status entry rather than
    silence."""

    def test_no_eligible_transaction_omits_itemization_and_publishes_direct_route(self) -> None:
        model = _run_model("demo.sdcl.t3.not-required", _sdcl_t2_acts(
            box2a=1500, eligible_txn=False, adoption_file="adopt-core-v13-current.json",
        ))
        group_ids = {g["id"] for g in model["citationGroups"]}
        self.assertNotIn(SD_ATTACHMENT_ID, group_ids)
        attachments_by_id = {a["id"]: a for a in model["attachments"]}
        self.assertEqual(attachments_by_id[SD_ATTACHMENT_ID]["resolved"]["disposition"], "guard_inapplicable")
        self.assertEqual(attachments_by_id[SD_ATTACHMENT_ID]["resolved"]["activeCodes"], [])
        sections = _sections_by_id(model)
        self.assertEqual(sections["line-7a"]["resolved"]["value"], 1500)


class ViolatedAndMissingAreNowVisible(unittest.TestCase):
    """ADR-0056: a required-and-incomplete Schedule D attachment (violated or
    missing boundary declaration) no longer renders silently. It stays out of
    citationGroups (no itemization detail to show), but is now visible in the
    new attachments status list, naming the exact violated/missing code. The
    numeric lines still correctly redact, unaffected by this change."""

    def test_violated_declaration_attachment_now_visible(self) -> None:
        boundary: dict[str, str | None] = {name: "yes" for name in BOUNDARY_DECLARATIONS}
        boundary["tax.us.2025.schedule-d-boundary.no-current-capital-losses"] = "no"
        model = _run_model("demo.sdcl.t3.violated", _sdcl_t2_acts(
            box2a=None, close_2a=True, eligible_txn=True, boundary=boundary,
            adoption_file="adopt-core-v13-current.json",
        ))
        group_ids = {g["id"] for g in model["citationGroups"]}
        self.assertNotIn(SD_ATTACHMENT_ID, group_ids)
        attachments_by_id = {a["id"]: a for a in model["attachments"]}
        self.assertEqual(attachments_by_id[SD_ATTACHMENT_ID]["resolved"]["disposition"], "blocked")
        self.assertEqual(
            attachments_by_id[SD_ATTACHMENT_ID]["resolved"]["activeCodes"],
            ["COMPLETENESS_VALUE_VIOLATION"],
        )
        sections = _sections_by_id(model)
        # The numeric route still redacts correctly, unaffected by this ADR.
        self.assertEqual(sections["line-7a"]["resolved"]["disposition"], "blocked")

    def test_missing_declaration_attachment_now_visible(self) -> None:
        boundary: dict[str, str | None] = {name: "yes" for name in BOUNDARY_DECLARATIONS}
        boundary["tax.us.2025.schedule-d-boundary.no-form8949-sources"] = None
        model = _run_model("demo.sdcl.t3.missing", _sdcl_t2_acts(
            box2a=None, close_2a=True, eligible_txn=True, boundary=boundary,
            adoption_file="adopt-core-v13-current.json",
        ))
        group_ids = {g["id"] for g in model["citationGroups"]}
        self.assertNotIn(SD_ATTACHMENT_ID, group_ids)
        attachments_by_id = {a["id"]: a for a in model["attachments"]}
        self.assertEqual(attachments_by_id[SD_ATTACHMENT_ID]["resolved"]["disposition"], "blocked")
        self.assertEqual(attachments_by_id[SD_ATTACHMENT_ID]["resolved"]["activeCodes"], ["DEPENDENCY_ABSENT"])


if __name__ == "__main__":
    unittest.main()
