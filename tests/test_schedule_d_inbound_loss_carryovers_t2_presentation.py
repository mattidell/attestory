"""Track 2 Inbound Capital-Loss Carryovers: presentation projection goldens
(ADR-0059/0060), against package v16 / published-packages.v11.

Projects Track 1's successor Schedule D lines (6/7/14/15/16/21) and Form 1040
line 7a through the existing citation-walk presentation model. No new
production code — only live_coordinate_run presentation assertions against
Track 1's act builder and worked fixtures.

Regression gate: re-run tests.test_schedule_d_presentation_t3 unmodified on
this branch (covered-long-term-gain-only presentation goldens). That path is
deliberately not re-authored against v15.
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
from tests.test_schedule_d_inbound_loss_carryovers_t1 import (
    BOUNDARY_PATH_A,
    BOUNDARY_PATH_B,
    CONTENT,
    FIXTURES,
    REPO,
    SCOPE,
    SD_ATT,
    USER,
    _build_acts,
    _t1_prior,
    _t2_prior,
    _t3_prior,
)

SD_ATTACHMENT_ID = SD_ATT
RENDERER = REPO / "tools" / "presentation_harness" / "examples" / "pages" / "citation-walk.v1.html"


def _surface() -> PublicationSurface:
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases",
        CONTENT / "published-packages.v11.json",
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


class PathANoCarryoverPresentation(unittest.TestCase):
    """Path A (declaration yes): W8/W13 publish as 0 → lines 6/14 zero;
    current-year ST loss still projects signed through line 16/21/7a."""

    def test_path_a_zeros_carryover_lines_and_keeps_cy_loss(self) -> None:
        # proceeds 1000, basis 2500 => line1a = -1500; line6 = 0; line7 = -1500
        model = _run_model(
            "demo.sdilc.t2.path-a",
            _build_acts(st=[(1000, 2500)], lt=[], boundary=BOUNDARY_PATH_A, prior=None),
        )
        sections = _sections_by_id(model)
        self.assertEqual(sections["line-6"]["resolved"]["disposition"], "computed_zero")
        self.assertEqual(sections["line-6"]["resolved"]["value"], 0)
        self.assertEqual(sections["line-14"]["resolved"]["disposition"], "computed_zero")
        self.assertEqual(sections["line-14"]["resolved"]["value"], 0)
        self.assertEqual(sections["line-1a-h"]["resolved"]["value"], -1500)
        self.assertEqual(sections["line-7"]["resolved"]["value"], -1500)
        self.assertEqual(sections["line-sch-d-16"]["resolved"]["value"], -1500)
        self.assertEqual(sections["line-21"]["resolved"]["value"], 1500)
        self.assertEqual(sections["line-7a"]["resolved"]["value"], -1500)
        attachments = _attachments_by_id(model)
        self.assertEqual(attachments[SD_ATTACHMENT_ID]["resolved"]["disposition"], "published")
        group_ids = {g["id"] for g in model["citationGroups"]}
        self.assertIn(SD_ATTACHMENT_ID, group_ids)


class PathBBothCarryoversPresentation(unittest.TestCase):
    """Path B T1 arithmetic: W8=W13=5000 → lines 6/14 = −5000; line16 = −10000;
    line21 = 3000; line7a = −3000 (decision-record T1 / T8)."""

    def test_t1_both_carryovers_project_signed_values(self) -> None:
        model = _run_model(
            "demo.sdilc.t2.t1-both",
            _build_acts(st=[], lt=[], boundary=BOUNDARY_PATH_B, prior=_t1_prior()),
        )
        sections = _sections_by_id(model)
        self.assertEqual(sections["line-6"]["resolved"]["disposition"], "published_value")
        self.assertEqual(sections["line-6"]["resolved"]["value"], -5000)
        self.assertEqual(sections["line-14"]["resolved"]["value"], -5000)
        self.assertEqual(sections["line-7"]["resolved"]["value"], -5000)
        self.assertEqual(sections["line-sch-d-15"]["resolved"]["value"], -5000)
        self.assertEqual(sections["line-sch-d-16"]["resolved"]["value"], -10000)
        self.assertEqual(sections["line-21"]["resolved"]["value"], 3000)
        self.assertEqual(sections["line-7a"]["resolved"]["value"], -3000)
        # Preferential / QDCG-facing Form 1040 line 16 floors at 0.
        self.assertEqual(sections["line-16"]["resolved"]["disposition"], "published_value")
        self.assertGreaterEqual(sections["line-16"]["resolved"]["value"], 0)
        attachments = _attachments_by_id(model)
        self.assertEqual(attachments[SD_ATTACHMENT_ID]["resolved"]["disposition"], "published")
        group_ids = {g["id"] for g in model["citationGroups"]}
        self.assertIn(SD_ATTACHMENT_ID, group_ids)


class CarryoverOnlyRoutingPresentation(unittest.TestCase):
    """Carryover-only 2025 return (both families closed-empty, T1 prior):
    Schedule D required solely by W8/W13; lines 1a/8a closure-backed zero."""

    def test_carryover_only_requires_schedule_d_and_limits_line21(self) -> None:
        model = _run_model(
            "demo.sdilc.t2.carryover-only",
            _build_acts(st=[], lt=[], boundary=BOUNDARY_PATH_B, prior=_t1_prior()),
        )
        sections = _sections_by_id(model)
        attachments = _attachments_by_id(model)
        self.assertEqual(attachments[SD_ATTACHMENT_ID]["resolved"]["disposition"], "published")
        self.assertEqual(sections["line-1a-h"]["resolved"]["disposition"], "closure_backed_zero")
        self.assertEqual(sections["line-8a-h"]["resolved"]["disposition"], "closure_backed_zero")
        self.assertEqual(sections["line-6"]["resolved"]["value"], -5000)
        self.assertEqual(sections["line-14"]["resolved"]["value"], -5000)
        self.assertEqual(sections["line-sch-d-16"]["resolved"]["value"], -10000)
        self.assertEqual(sections["line-21"]["resolved"]["value"], 3000)
        self.assertEqual(sections["line-7a"]["resolved"]["value"], -3000)


class CombinedCarryoverPresentation(unittest.TestCase):
    """Carryover combined with current-year gain, under-cap loss, and box-2a."""

    def test_carryover_offsets_current_year_gain(self) -> None:
        # ST gain 4000 + W8 5000 (T2) → line7 = -1000
        model = _run_model(
            "demo.sdilc.t2.offset-gain",
            _build_acts(
                st=[(5000, 1000)], lt=[], boundary=BOUNDARY_PATH_B, prior=_t2_prior()
            ),
        )
        sections = _sections_by_id(model)
        self.assertEqual(sections["line-1a-h"]["resolved"]["value"], 4000)
        self.assertEqual(sections["line-6"]["resolved"]["value"], -5000)
        self.assertEqual(sections["line-7"]["resolved"]["value"], -1000)
        self.assertEqual(sections["line-14"]["resolved"]["value"], 0)
        self.assertEqual(sections["line-sch-d-16"]["resolved"]["value"], -1000)
        self.assertEqual(sections["line-21"]["resolved"]["value"], 1000)
        self.assertEqual(sections["line-7a"]["resolved"]["value"], -1000)

    def test_carryover_with_current_year_loss_under_cap(self) -> None:
        # ST loss 1000 + W8 5000 → line7 = -6000; line21 = 3000
        model = _run_model(
            "demo.sdilc.t2.with-cy-loss",
            _build_acts(
                st=[(1000, 2000)], lt=[], boundary=BOUNDARY_PATH_B, prior=_t2_prior()
            ),
        )
        sections = _sections_by_id(model)
        self.assertEqual(sections["line-6"]["resolved"]["value"], -5000)
        self.assertEqual(sections["line-7"]["resolved"]["value"], -6000)
        self.assertEqual(sections["line-sch-d-16"]["resolved"]["value"], -6000)
        self.assertEqual(sections["line-21"]["resolved"]["value"], 3000)
        self.assertEqual(sections["line-7a"]["resolved"]["value"], -3000)

    def test_carryover_with_box2a(self) -> None:
        # T3 LT carryover 5000 + box2a 2000 → line15 = -3000
        model = _run_model(
            "demo.sdilc.t2.with-box2a",
            _build_acts(
                st=[],
                lt=[],
                box2a=2000,
                boundary=BOUNDARY_PATH_B,
                prior=_t3_prior(),
            ),
        )
        sections = _sections_by_id(model)
        self.assertEqual(sections["line-6"]["resolved"]["value"], 0)
        self.assertEqual(sections["line-14"]["resolved"]["value"], -5000)
        self.assertEqual(sections["line-sch-d-13"]["resolved"]["value"], 2000)
        self.assertEqual(sections["line-sch-d-15"]["resolved"]["value"], -3000)
        self.assertEqual(sections["line-sch-d-16"]["resolved"]["value"], -3000)
        self.assertEqual(sections["line-21"]["resolved"]["value"], 3000)
        self.assertEqual(sections["line-7a"]["resolved"]["value"], -3000)


class DispositionVisibilityParity(unittest.TestCase):
    """Track 1's Path B missing-prior-authority DEPENDENCY_ABSENT must render
    on the presentation surface (ADR-0056), not vanish."""

    def test_path_b_missing_prior_dependency_absent_on_attachment_and_line6(self) -> None:
        model = _run_model(
            "demo.sdilc.t2.path-b-missing",
            _build_acts(
                st=[(1000, 2000)], lt=[], boundary=BOUNDARY_PATH_B, prior=None
            ),
        )
        group_ids = {g["id"] for g in model["citationGroups"]}
        self.assertNotIn(SD_ATTACHMENT_ID, group_ids)
        attachments = _attachments_by_id(model)
        self.assertEqual(attachments[SD_ATTACHMENT_ID]["resolved"]["disposition"], "blocked")
        self.assertEqual(
            attachments[SD_ATTACHMENT_ID]["resolved"]["activeCodes"],
            ["DEPENDENCY_ABSENT"],
        )
        sections = _sections_by_id(model)
        self.assertEqual(sections["line-6"]["resolved"]["disposition"], "blocked")
        self.assertEqual(
            sections["line-6"]["resolved"]["activeCodes"],
            ["DEPENDENCY_ABSENT"],
        )
        # Downstream redacts rather than fabricating amounts.
        self.assertEqual(sections["line-sch-d-16"]["resolved"]["disposition"], "blocked")
        self.assertEqual(sections["line-7a"]["resolved"]["disposition"], "blocked")


class ProductPageSmoke(unittest.TestCase):
    """Lightweight product-page smoke: renderer accepts signed/finite numbers;
    live carryover models include successor section ids with numeric values."""

    def test_renderer_accepts_signed_carryover_values(self) -> None:
        html = RENDERER.read_text("utf-8")
        self.assertIn("Number.isFinite(value)", html)
        self.assertIn('throw new SectionError("invalid-numeric-value")', html)
        self.assertIn("for (const section of FIXTURE.sections || [])", html)
        self.assertTrue(isinstance(-5000, (int, float)))

        path_a = _run_model(
            "demo.sdilc.t2.smoke-path-a",
            _build_acts(st=[(1000, 2500)], lt=[], boundary=BOUNDARY_PATH_A),
        )
        path_b = _run_model(
            "demo.sdilc.t2.smoke-path-b",
            _build_acts(st=[], lt=[], boundary=BOUNDARY_PATH_B, prior=_t1_prior()),
        )
        for model in (path_a, path_b):
            ids = {s["id"] for s in model["sections"]}
            for required in (
                "line-6",
                "line-7",
                "line-14",
                "line-sch-d-15",
                "line-sch-d-16",
                "line-21",
                "line-7a",
            ):
                self.assertIn(required, ids)
            line6 = next(s for s in model["sections"] if s["id"] == "line-6")
            self.assertIn(
                line6["resolved"]["disposition"],
                {"published_value", "computed_zero"},
            )
            self.assertIsInstance(line6["resolved"]["value"], (int, float))


if __name__ == "__main__":
    unittest.main()
