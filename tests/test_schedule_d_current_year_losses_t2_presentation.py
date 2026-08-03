"""Track 2 Current-Year Capital Losses: presentation projection goldens
(ADR-0057/0058), against package v14 / published-packages.v9.

Projects the successor Schedule D lines (1a/7/8a/13/15/16 signed, 21) and
disposition states through the existing citation-walk presentation model.
No new production code in this track — only live_coordinate_run presentation
assertions against Track 1's act builder.

Regression gate: re-run tests.test_schedule_d_presentation_t3 on this
branch (prior milestone, package v13/v8). That path is deliberately not
re-authored against v14, which dual-excludes the gain-only LTCG stack.
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
from tests.test_schedule_d_current_year_losses_t1 import (
    BOUNDARY_5,
    CONTENT,
    FIXTURES,
    REPO,
    SCOPE,
    SD_ATTACHMENT,
    USER,
    _build_acts,
)

SD_ATTACHMENT_ID = SD_ATTACHMENT
RENDERER = REPO / "tools" / "presentation_harness" / "examples" / "pages" / "citation-walk.v1.html"


def _surface() -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases",
        CONTENT / "published-packages.v9.json",
        CONTENT,
    )


def _run_model(run_id: str, acts: list[dict[str, object]]) -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=REPO,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope=SCOPE,
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=_surface(),
            output_name="out.json",
        )
        assert outcome.refusal is None, outcome.refusal
        assert outcome.presentation_path is not None
        return cast(dict[str, Any], json.loads(outcome.presentation_path.read_text("utf-8")))


def _sections_by_id(model: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {s["id"]: s for s in model["sections"]}


def _attachments_by_id(model: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {a["id"]: a for a in model["attachments"]}


class NetLossPresentation(unittest.TestCase):
    """Net short-term loss below the $3,000 cap: line 16 signed negative,
    line 21 populated with the limited deductible amount."""

    def test_st_loss_signed_line16_and_populated_line21(self) -> None:
        # proceeds 1000, basis 2500 => line1a/7/16 = -1500; line21 = 1500
        model = _run_model("demo.sdcyl.t2.st-loss", _build_acts(st=[(1000, 2500)], lt=[]))
        sections = _sections_by_id(model)
        self.assertEqual(sections["line-1a-h"]["resolved"]["disposition"], "published_value")
        self.assertEqual(sections["line-1a-h"]["resolved"]["value"], -1500)
        self.assertEqual(sections["line-7"]["resolved"]["value"], -1500)
        self.assertEqual(sections["line-sch-d-16"]["resolved"]["disposition"], "published_value")
        self.assertEqual(sections["line-sch-d-16"]["resolved"]["value"], -1500)
        self.assertEqual(sections["line-21"]["resolved"]["disposition"], "published_value")
        self.assertEqual(sections["line-21"]["resolved"]["value"], 1500)
        self.assertEqual(sections["line-7a"]["resolved"]["value"], -1500)
        # Preferential / QDCG-facing Form 1040 line 16 still publishes (floored base).
        self.assertEqual(sections["line-16"]["resolved"]["disposition"], "published_value")
        self.assertIsInstance(sections["line-16"]["resolved"]["value"], (int, float))
        self.assertGreaterEqual(sections["line-16"]["resolved"]["value"], 0)
        attachments = _attachments_by_id(model)
        self.assertEqual(attachments[SD_ATTACHMENT_ID]["resolved"]["disposition"], "published")
        group_ids = {g["id"] for g in model["citationGroups"]}
        self.assertIn(SD_ATTACHMENT_ID, group_ids)


class NetGainLine21Zero(unittest.TestCase):
    """Net-gain return: line 21 is a computed zero, not a fabricated positive
    limited-loss amount."""

    def test_mixed_net_gain_line21_is_computed_zero(self) -> None:
        # ST +2000, LT -500 => net +1500
        model = _run_model(
            "demo.sdcyl.t2.mixed-gain",
            _build_acts(st=[(5000, 3000)], lt=[(1000, 1500)]),
        )
        sections = _sections_by_id(model)
        self.assertEqual(sections["line-1a-h"]["resolved"]["value"], 2000)
        self.assertEqual(sections["line-8a-h"]["resolved"]["value"], -500)
        self.assertEqual(sections["line-sch-d-16"]["resolved"]["value"], 1500)
        self.assertEqual(sections["line-7a"]["resolved"]["value"], 1500)
        self.assertEqual(sections["line-21"]["resolved"]["disposition"], "computed_zero")
        self.assertEqual(sections["line-21"]["resolved"]["value"], 0)
        # Preferential-facing surface remains nonnegative.
        self.assertGreaterEqual(sections["line-16"]["resolved"]["value"], 0)


class QPositiveWithNetLossPresentation(unittest.TestCase):
    """Q>0 with Schedule D net loss: QDCG-consuming Form 1040 line 16 still
    publishes; Schedule D signed loss remains honest on the model."""

    def test_q_positive_floored_base_still_publishes_line16(self) -> None:
        model = _run_model(
            "demo.sdcyl.t2.qpos-net-loss",
            _build_acts(st=[(1000, 2500)], lt=[], box1a=600, box1b=600),
        )
        sections = _sections_by_id(model)
        self.assertEqual(sections["line-3a"]["resolved"]["value"], 600)
        self.assertEqual(sections["line-3b"]["resolved"]["value"], 600)
        self.assertEqual(sections["line-sch-d-16"]["resolved"]["value"], -1500)
        self.assertEqual(sections["line-21"]["resolved"]["value"], 1500)
        self.assertEqual(sections["line-16"]["resolved"]["disposition"], "published_value")
        self.assertGreaterEqual(sections["line-16"]["resolved"]["value"], 0)


class DirectRouteBothEmptyPresentation(unittest.TestCase):
    """Both families closed-empty with box-2a only: direct route; Schedule D
    attachment is not-required (guard_inapplicable), matching the prior
    milestone's not-required presentation shape."""

    def test_both_empty_direct_route_matches_prior_shape(self) -> None:
        model = _run_model(
            "demo.sdcyl.t2.direct",
            _build_acts(st=[], lt=[], box2a=1500),
        )
        sections = _sections_by_id(model)
        group_ids = {g["id"] for g in model["citationGroups"]}
        self.assertNotIn(SD_ATTACHMENT_ID, group_ids)
        attachments = _attachments_by_id(model)
        self.assertEqual(
            attachments[SD_ATTACHMENT_ID]["resolved"]["disposition"],
            "guard_inapplicable",
        )
        self.assertEqual(attachments[SD_ATTACHMENT_ID]["resolved"]["activeCodes"], [])
        self.assertEqual(sections["line-7a"]["resolved"]["value"], 1500)
        self.assertEqual(sections["line-sch-d-13"]["resolved"]["value"], 1500)
        # Empty families still project as closure-backed zeros, not fabricated
        # transaction amounts; line 21 is computed zero on a net-gain path.
        self.assertEqual(sections["line-1a-h"]["resolved"]["disposition"], "closure_backed_zero")
        self.assertEqual(sections["line-8a-h"]["resolved"]["disposition"], "closure_backed_zero")
        self.assertEqual(sections["line-21"]["resolved"]["disposition"], "computed_zero")
        self.assertEqual(sections["line-21"]["resolved"]["value"], 0)


class DispositionVisibilityParity(unittest.TestCase):
    """Track 1 coordinator dispositions are visible on the presentation
    surface (attachments / section activeCodes), per ADR-0056's three-code
    allowlist — no new code invented here."""

    def test_unclosed_family_source_set_unclosed_on_line1a(self) -> None:
        model = _run_model(
            "demo.sdcyl.t2.unclosed-st",
            _build_acts(st=[(1000, 2500)], lt=[], close_st=False),
        )
        sections = _sections_by_id(model)
        self.assertEqual(sections["line-1a-h"]["resolved"]["disposition"], "blocked")
        self.assertEqual(
            sections["line-1a-h"]["resolved"]["activeCodes"],
            ["SOURCE_SET_UNCLOSED"],
        )
        # Downstream numeric route redacts (blocked), not a fabricated amount.
        self.assertEqual(sections["line-sch-d-16"]["resolved"]["disposition"], "blocked")
        self.assertEqual(sections["line-7a"]["resolved"]["disposition"], "blocked")

    def test_violated_inbound_completeness_value_violation_on_attachment(self) -> None:
        boundary: dict[str, str | None] = {n: "yes" for n in BOUNDARY_5}
        boundary["tax.us.2025.schedule-d-boundary.no-inbound-capital-loss-carryovers"] = "no"
        model = _run_model(
            "demo.sdcyl.t2.violated-inbound",
            _build_acts(st=[(1000, 2000)], lt=[], boundary=boundary),
        )
        group_ids = {g["id"] for g in model["citationGroups"]}
        self.assertNotIn(SD_ATTACHMENT_ID, group_ids)
        attachments = _attachments_by_id(model)
        self.assertEqual(attachments[SD_ATTACHMENT_ID]["resolved"]["disposition"], "blocked")
        self.assertEqual(
            attachments[SD_ATTACHMENT_ID]["resolved"]["activeCodes"],
            ["COMPLETENESS_VALUE_VIOLATION"],
        )

    def test_missing_inbound_dependency_absent_on_attachment(self) -> None:
        boundary: dict[str, str | None] = {n: "yes" for n in BOUNDARY_5}
        boundary["tax.us.2025.schedule-d-boundary.no-inbound-capital-loss-carryovers"] = None
        model = _run_model(
            "demo.sdcyl.t2.missing-inbound",
            _build_acts(st=[(1000, 2000)], lt=[], boundary=boundary),
        )
        group_ids = {g["id"] for g in model["citationGroups"]}
        self.assertNotIn(SD_ATTACHMENT_ID, group_ids)
        attachments = _attachments_by_id(model)
        self.assertEqual(attachments[SD_ATTACHMENT_ID]["resolved"]["disposition"], "blocked")
        self.assertEqual(
            attachments[SD_ATTACHMENT_ID]["resolved"]["activeCodes"],
            ["DEPENDENCY_ABSENT"],
        )


class OverCapLossPresentation(unittest.TestCase):
    """Net loss over the $3,000 single-filer cap: line 16 remains the full
    signed net; line 21 is the capped deductible amount."""

    def test_over_cap_preserves_signed_net_and_caps_line21(self) -> None:
        # ST -3000 + LT -2000 = net -5000; line21 = 3000; line7a = -3000
        model = _run_model(
            "demo.sdcyl.t2.over-cap",
            _build_acts(st=[(1000, 4000)], lt=[(1000, 3000)]),
        )
        sections = _sections_by_id(model)
        self.assertEqual(sections["line-sch-d-16"]["resolved"]["value"], -5000)
        self.assertEqual(sections["line-21"]["resolved"]["value"], 3000)
        self.assertEqual(sections["line-7a"]["resolved"]["value"], -3000)


class ProductPageSmoke(unittest.TestCase):
    """Lightweight product-page smoke without new infrastructure: the
    citation-walk renderer accepts finite numbers (including negatives) via
    Number.isFinite, and live net-loss / net-gain models carry the new
    section ids with numeric dispositions the renderer already knows."""

    def test_renderer_accepts_signed_numeric_values(self) -> None:
        html = RENDERER.read_text("utf-8")
        self.assertIn("Number.isFinite(value)", html)
        self.assertIn('throw new SectionError("invalid-numeric-value")', html)
        self.assertIn("for (const section of FIXTURE.sections || [])", html)
        # Sanity: negatives are finite numbers; the renderer uses String(value).
        self.assertTrue(isinstance(-1500, (int, float)))
        # Live models for net-loss and net-gain include the successor sections.
        loss = _run_model("demo.sdcyl.t2.smoke-loss", _build_acts(st=[(1000, 2500)], lt=[]))
        gain = _run_model(
            "demo.sdcyl.t2.smoke-gain",
            _build_acts(st=[(5000, 3000)], lt=[(1000, 1500)]),
        )
        for model in (loss, gain):
            ids = {s["id"] for s in model["sections"]}
            for required in (
                "line-1a-h",
                "line-7",
                "line-8a-h",
                "line-sch-d-13",
                "line-sch-d-15",
                "line-sch-d-16",
                "line-21",
            ):
                self.assertIn(required, ids)
            sch16 = next(s for s in model["sections"] if s["id"] == "line-sch-d-16")
            self.assertEqual(sch16["resolved"]["disposition"], "published_value")
            self.assertIsInstance(sch16["resolved"]["value"], (int, float))


if __name__ == "__main__":
    unittest.main()
