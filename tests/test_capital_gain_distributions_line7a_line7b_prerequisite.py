"""Line-7b prerequisite: immutable v2/v8/v3 route and disposition proof.

The three disposition scenarios enter through ``live_coordinate_run`` from
the Track-2 production-shaped synthetic act log. Presentation is deliberately
stubbed at its existing call seam because this prerequisite ends at the
resolved-member/disposition boundary; Track 3 owns categorical projection.
"""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from unittest.mock import patch

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import (
    PublicationSurface,
    ResolvedGraph,
    resolve_production_package,
)
from tests.test_capital_gain_distributions_line7a_t2_coordinator import (
    C1,
    C2,
    C3,
    C4,
    LINE7B_RULE,
    _cgd_t2_acts,
)
from tools.generate_frrs_t3_fixtures import (
    LINE7B_FIELD_ID,
    LINE7B_SYMBOL,
    render_line7b_prerequisite_content_files,
)

REPO = Path(__file__).resolve().parent.parent
CONTENT = REPO / "packages" / "content" / "tax" / "2025"
T3 = REPO / "packages" / "sample_data" / "frrs_t3"
USER = "demo.user.filer-1"
V7_SCOPE = {"jurisdiction": "us", "year": "2056"}
V8_SCOPE = {"jurisdiction": "us", "year": "2057"}


def _surface(registry_version: str) -> PublicationSurface:
    return PublicationSurface(
        T3 / "publication_surface" / "releases",
        CONTENT / f"published-packages{registry_version}.json",
        CONTENT,
    )


def _v8_acts(
    *,
    components: dict[str, str | None] | None = None,
) -> list[dict[str, object]]:
    acts = _cgd_t2_acts(components=components)
    adoption = json.loads(
        (T3 / "adoptions" / "adopt-core-v8-current.json").read_text("utf-8")
    )
    adoption["committed_against"] = len(acts) - 1
    acts[-1] = adoption
    return acts


def _run_at_boundary(
    acts: list[dict[str, object]],
    *,
    scope: dict[str, str],
    registry_version: str,
    run_id: str,
) -> tuple[dict[str, Any], tuple[dict[str, Any], ...]]:
    captured: dict[str, tuple[dict[str, Any], ...]] = {}

    def capture_projection(
        *,
        run_id: str,
        resolved_members: tuple[dict[str, Any], ...],
        state: Any,
        publications: Any,
        dispositions: Any,
    ) -> dict[str, Any]:
        del state, publications, dispositions
        captured["members"] = resolved_members
        return {
            "schema": "presentation-model.v1",
            "runId": run_id,
            "pinLabels": {},
            "sections": [],
            "citationGroups": [],
        }

    with TemporaryDirectory() as tmp, patch(
        "packages.derivation.live.build_presentation_model",
        side_effect=capture_projection,
    ):
        result = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=REPO,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope=scope,
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=_surface(registry_version),
            output_name="out.json",
        )
        assert result.refusal is None, result.refusal
        assert result.output_path is not None
        report = json.loads(result.output_path.read_text("utf-8"))
    return report, captured["members"]


def _row(report: dict[str, Any]) -> dict[str, Any]:
    return next(
        row for row in report["dispositions"] if row["artifact_id"] == LINE7B_RULE
    )


class DeterministicSuccessors(unittest.TestCase):
    def test_committed_successor_content_matches_generator(self) -> None:
        for relative, expected in render_line7b_prerequisite_content_files().items():
            with self.subTest(relative=relative):
                self.assertEqual((CONTENT / relative).read_bytes(), expected)

    def test_successors_are_strictly_additive(self) -> None:
        field_v1 = json.loads(
            (CONTENT / "form1040.line-7b.form-field.json").read_text("utf-8")
        )
        field_v2 = json.loads(
            (CONTENT / "form1040.line-7b.form-field.v2.json").read_text("utf-8")
        )
        expected_field = copy.deepcopy(field_v1)
        expected_field["version"] = "v2"
        expected_field["binds_symbol"] = LINE7B_SYMBOL
        self.assertEqual(field_v2, expected_field)

        package_v7 = json.loads(
            (CONTENT / "package.core-calculations.v7.json").read_text("utf-8")
        )
        package_v8 = json.loads(
            (CONTENT / "package.core-calculations.v8.json").read_text("utf-8")
        )
        v8_without_successor_fields = copy.deepcopy(package_v8)
        v8_without_successor_fields["version"] = "v7"
        v8_without_successor_fields["package_checksum"] = package_v7["package_checksum"]
        v8_without_successor_fields["members"] = [
            member
            for member in v8_without_successor_fields["members"]
            if not (
                member["id"] == LINE7B_FIELD_ID and member["version"] == "v2"
            )
        ]
        self.assertEqual(v8_without_successor_fields, package_v7)

        registry_v2 = json.loads(
            (CONTENT / "published-packages.v2.json").read_text("utf-8")
        )
        registry_v3 = json.loads(
            (CONTENT / "published-packages.v3.json").read_text("utf-8")
        )
        registry_v3["citizens"] = [
            entry
            for entry in registry_v3["citizens"]
            if not (entry["id"] == LINE7B_FIELD_ID and entry["version"] == "v2")
        ]
        registry_v3["packages"] = [
            entry
            for entry in registry_v3["packages"]
            if not (
                entry["id"] == "tax.us.2025.package.core-calculations"
                and entry["version"] == "v8"
            )
        ]
        self.assertEqual(registry_v3, registry_v2)


class ResolvedGraphAndDispositions(unittest.TestCase):
    def test_v8_resolves_exactly_one_line7b_field_successor(self) -> None:
        acts = _v8_acts()
        resolved = resolve_production_package(
            acts,
            run_scope=V8_SCOPE,
            scope_user=USER,
            workspace_revision=len(acts),
            surface=_surface(".v3"),
        )
        self.assertIsInstance(resolved, ResolvedGraph)
        assert isinstance(resolved, ResolvedGraph)
        self.assertEqual(resolved.package["version"], "v8")
        fields = [
            member
            for member in resolved.resolved_members
            if member["id"] == LINE7B_FIELD_ID
        ]
        self.assertEqual(len(fields), 1)
        self.assertEqual(fields[0]["version"], "v2")
        rule = next(
            member
            for member in resolved.resolved_members
            if member["id"] == LINE7B_RULE
        )
        self.assertEqual(fields[0]["binds_symbol"], rule["publishes"])
        self.assertEqual(rule["publishes"], LINE7B_SYMBOL)

    def test_v8_live_run_exposes_all_existing_line7b_dispositions(self) -> None:
        cases = (
            (
                "eligible",
                {"C1": "yes", "C2": "yes", "C3": "yes", "C4": "yes"},
                "published",
            ),
            (
                "missing-authority",
                {"C1": "yes", "C2": "yes", "C3": "yes", "C4": None},
                "blocked",
            ),
            (
                "conclusion-yes",
                {"C1": "yes", "C2": "yes", "C3": "yes", "C4": "no"},
                "inapplicable",
            ),
        )
        for name, components, expected in cases:
            with self.subTest(name=name):
                report, members = _run_at_boundary(
                    _v8_acts(components=components),
                    scope=V8_SCOPE,
                    registry_version=".v3",
                    run_id=f"demo.cgd.line7b-prerequisite.{name}",
                )
                row = _row(report)
                self.assertEqual(row["disposition"], expected)
                if expected != "published":
                    self.assertNotIn("value", row)
                fields = [
                    member
                    for member in members
                    if member["id"] == LINE7B_FIELD_ID
                ]
                self.assertEqual(
                    [(field["version"], field["binds_symbol"]) for field in fields],
                    [("v2", LINE7B_SYMBOL)],
                )
                self.assertEqual(
                    fields[0]["dispositions"]["published_value"]["render"],
                    "checked",
                )

    def test_v7_live_control_remains_without_line7b_field_member(self) -> None:
        report, members = _run_at_boundary(
            _cgd_t2_acts(),
            scope=V7_SCOPE,
            registry_version=".v2",
            run_id="demo.cgd.line7b-prerequisite.v7-control",
        )
        self.assertEqual(_row(report)["disposition"], "published")
        self.assertFalse(any(member["id"] == LINE7B_FIELD_ID for member in members))


if __name__ == "__main__":
    unittest.main()
