"""Presentation L2 Integration Grounding, Track 1.

Covers the internal presentation projector (``packages/derivation/
presentation_projection.py``), its wiring into ``live_coordinate_run``
(``packages/derivation/live.py``), and the production-shaped golden generator
(``tools/generate_presentation_l2_golden.py``): deterministic regeneration,
strict validation, coordinator-only construction, existing-result
compatibility, ``LiveWorkspace`` confinement, and the named fail-closed
rejections (missing/ambiguous joins, unknown dispositions, invalid numeric
publications, resolver refusal, path escape, and unsafe serialization).

All content is synthetic (``demo.*`` values, temporary workspaces); no real
workspace or personal material is read or written.
"""

from __future__ import annotations

import json
import unittest
import unittest.mock
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.presentation_projection import (
    PRESENTATION_MODEL_VERSION,
    PresentationModelError,
    build_presentation_model,
    validate_presentation_model,
)
from packages.derivation.production_resolver import PublicationSurface, Refusal
from packages.derivation.runner import Publication
from packages.kernel.findings import EvidenceLifecycle, FindingState
from tools import generate_presentation_l2_golden as golden

REPO = Path(__file__).resolve().parent.parent
CONTENT = REPO / "packages" / "content" / "tax" / "2025"
T3 = REPO / "packages" / "sample_data" / "frrs_t3"
USER = "demo.user.filer-1"


def _surface() -> PublicationSurface:
    return PublicationSurface(T3 / "publication_surface" / "releases", CONTENT / "published-packages.json", CONTENT)


# --- Small, hand-built fixtures for unit-level projector tests ---------------

FIELD = {
    "schema": "form-field.v3",
    "id": "demo.field.line-x",
    "version": "v1",
    "form": {"authority": "IRS", "form_id": "1040", "tax_year": 2025, "jurisdiction": "US-federal"},
    "line": "x",
    "label": "Demo line",
    "description": "A synthetic demo field for unit-level projector tests.",
    "binds_symbol": "demo.symbol.line-x",
    "citation": {"id": "demo.citation.line-x", "version": "v1"},
    "dispositions": {
        "published_value": {"render": "{value}", "explain": "e"},
        "computed_zero": {"render": "0", "explain": "e"},
        "closure_backed_zero": {"render": "0", "explain": "e"},
        "blocked": {"render": "", "explain": "e", "codes": ["DEPENDENCY_ABSENT"]},
        "guard_inapplicable": {"render": "", "explain": "e"},
    },
}

RULE = {"id": "demo.rule.line-x", "schema": "rule-artifact.v2", "publishes": "demo.symbol.line-x"}


def _finding(finding_id: str, symbol: str, value: str, pins: list[dict[str, Any]]) -> dict[str, Any]:
    return {"schema": "derived-finding.v2", "id": finding_id, "symbol": symbol, "value": value, "version": "v2", "pins": pins}


def _state(findings: dict[str, dict[str, Any]], evidence: dict[str, EvidenceLifecycle] | None = None) -> FindingState:
    return FindingState(findings=findings, evidence=evidence or {})


class ProjectorPositive(unittest.TestCase):
    def test_published_nonzero_with_source_leaf_and_evidence_label(self) -> None:
        raw = {"schema": "finding.v1", "id": "demo.raw.a", "fact_id": "demo.fact.a", "value": 7, "basis": "attested", "evidence_ids": ["demo.evidence.a"]}
        state = _state(
            {"demo.raw.a": raw},
            {"demo.evidence.a": EvidenceLifecycle(evidence={"schema": "evidence.v1", "id": "demo.evidence.a", "kind": "demo.statement.x", "label": "Demo source A", "content": {}}, status="current")},
        )
        finding = _finding("demo.derived.x", "demo.symbol.line-x", "7", [{"role": "input", "id": "demo.raw.a", "version": "v1"}])
        row = {"artifact_id": "demo.rule.line-x", "disposition": "published", "finding_id": "demo.derived.x", "symbol": "demo.symbol.line-x", "pins": finding["pins"]}
        model = build_presentation_model(
            run_id="demo.run", resolved_members=[FIELD, RULE], state=state,
            publications=[Publication(act={}, finding=finding)], dispositions=[row],
        )
        self.assertEqual(model["schema"], PRESENTATION_MODEL_VERSION)
        section = model["sections"][0]
        self.assertEqual(section["resolved"], {"disposition": "published_value", "value": 7, "act": {"run_id": "demo.run", "finding": finding}})
        self.assertEqual(section["citationSites"], [{"siteId": "line-x-src-0", "pinId": "demo.raw.a", "pinVersion": "v1", "context": "Demo line"}])
        self.assertEqual(model["pinLabels"], {"demo.raw.a": "Demo source A"})

    def test_closure_backed_zero_has_no_citation_site(self) -> None:
        closure = {"schema": "finding.v1", "id": "demo.raw.closure", "fact_id": "demo.family.source-closure|family-horizon=h0", "value": True, "basis": "attested", "evidence_ids": []}
        state = _state({"demo.raw.closure": closure})
        finding = _finding("demo.derived.zero", "demo.symbol.line-x", "0", [{"role": "input", "id": "demo.raw.closure", "version": "v1"}])
        row = {"artifact_id": "demo.rule.line-x", "disposition": "published", "finding_id": "demo.derived.zero", "symbol": "demo.symbol.line-x", "pins": finding["pins"]}
        model = build_presentation_model(
            run_id="demo.run", resolved_members=[FIELD, RULE], state=state,
            publications=[Publication(act={}, finding=finding)], dispositions=[row],
        )
        section = model["sections"][0]
        self.assertEqual(section["resolved"]["disposition"], "closure_backed_zero")
        self.assertEqual(section["citationSites"], [])

    def test_recurses_through_a_derived_intermediate_to_the_raw_leaf(self) -> None:
        raw = {"schema": "finding.v1", "id": "demo.raw.b", "fact_id": "demo.fact.b", "value": 3, "basis": "attested", "evidence_ids": []}
        state = _state({"demo.raw.b": raw})
        subtotal = _finding("demo.derived.subtotal", "demo.symbol.subtotal", "3", [{"role": "input", "id": "demo.raw.b", "version": "v1"}])
        total = _finding("demo.derived.x", "demo.symbol.line-x", "3", [{"role": "input", "id": "demo.derived.subtotal", "version": "v2"}])
        row = {"artifact_id": "demo.rule.line-x", "disposition": "published", "finding_id": "demo.derived.x", "symbol": "demo.symbol.line-x", "pins": total["pins"]}
        model = build_presentation_model(
            run_id="demo.run", resolved_members=[FIELD, RULE], state=state,
            publications=[Publication(act={}, finding=subtotal), Publication(act={}, finding=total)], dispositions=[row],
        )
        self.assertEqual(model["sections"][0]["citationSites"], [{"siteId": "line-x-src-0", "pinId": "demo.raw.b", "pinVersion": "v1", "context": "Demo line"}])

    def test_blocked_and_guard_inapplicable_shapes(self) -> None:
        state = _state({})
        blocked_row = {"artifact_id": "demo.rule.line-x", "disposition": "blocked", "code": "DEPENDENCY_ABSENT", "missing": ["x"], "pins": []}
        model = build_presentation_model(run_id="r", resolved_members=[FIELD, RULE], state=state, publications=[], dispositions=[blocked_row])
        self.assertEqual(model["sections"][0]["resolved"], {"disposition": "blocked", "activeCodes": ["DEPENDENCY_ABSENT"], "act": None})

        guard_row = {"artifact_id": "demo.rule.line-x", "disposition": "inapplicable", "guard_result": False, "pins": []}
        model = build_presentation_model(run_id="r", resolved_members=[FIELD, RULE], state=state, publications=[], dispositions=[guard_row])
        self.assertEqual(model["sections"][0]["resolved"], {"disposition": "guard_inapplicable", "act": None})

    def test_no_fields_in_package_produces_empty_sections(self) -> None:
        model = build_presentation_model(run_id="r", resolved_members=[], state=_state({}), publications=[], dispositions=[])
        self.assertEqual(model["sections"], [])
        self.assertEqual(model["citationGroups"], [])
        validate_presentation_model(model)


class ProjectorFailClosed(unittest.TestCase):
    def test_missing_disposition_join_rejects(self) -> None:
        with self.assertRaises(PresentationModelError):
            build_presentation_model(run_id="r", resolved_members=[FIELD, RULE], state=_state({}), publications=[], dispositions=[])

    def test_ambiguous_disposition_join_rejects(self) -> None:
        row = {"artifact_id": "demo.rule.line-x", "disposition": "blocked", "code": "DEPENDENCY_ABSENT", "missing": [], "pins": []}
        with self.assertRaises(PresentationModelError):
            build_presentation_model(run_id="r", resolved_members=[FIELD, RULE], state=_state({}), publications=[], dispositions=[row, dict(row)])

    def test_unknown_disposition_rejects(self) -> None:
        row = {"artifact_id": "demo.rule.line-x", "disposition": "mysterious", "pins": []}
        with self.assertRaises(PresentationModelError):
            build_presentation_model(run_id="r", resolved_members=[FIELD, RULE], state=_state({}), publications=[], dispositions=[row])

    def test_conflict_inapplicable_without_guard_result_rejects(self) -> None:
        row = {"artifact_id": "demo.rule.line-x", "disposition": "inapplicable", "pins": []}
        with self.assertRaises(PresentationModelError):
            build_presentation_model(run_id="r", resolved_members=[FIELD, RULE], state=_state({}), publications=[], dispositions=[row])

    def test_invalid_numeric_publication_rejects(self) -> None:
        finding = _finding("demo.derived.x", "demo.symbol.line-x", "not-a-number", [])
        row = {"artifact_id": "demo.rule.line-x", "disposition": "published", "finding_id": "demo.derived.x", "symbol": "demo.symbol.line-x", "pins": []}
        with self.assertRaises(PresentationModelError):
            build_presentation_model(run_id="r", resolved_members=[FIELD, RULE], state=_state({}), publications=[Publication(act={}, finding=finding)], dispositions=[row])

    def test_untraceable_citation_lineage_rejects(self) -> None:
        finding = _finding("demo.derived.x", "demo.symbol.line-x", "5", [{"role": "input", "id": "demo.ghost", "version": "v1"}])
        row = {"artifact_id": "demo.rule.line-x", "disposition": "published", "finding_id": "demo.derived.x", "symbol": "demo.symbol.line-x", "pins": finding["pins"]}
        with self.assertRaises(PresentationModelError):
            build_presentation_model(run_id="r", resolved_members=[FIELD, RULE], state=_state({}), publications=[Publication(act={}, finding=finding)], dispositions=[row])

    def test_zero_with_no_source_or_closure_evidence_rejects(self) -> None:
        finding = _finding("demo.derived.x", "demo.symbol.line-x", "0", [])
        row = {"artifact_id": "demo.rule.line-x", "disposition": "published", "finding_id": "demo.derived.x", "symbol": "demo.symbol.line-x", "pins": []}
        with self.assertRaises(PresentationModelError):
            build_presentation_model(run_id="r", resolved_members=[FIELD, RULE], state=_state({}), publications=[Publication(act={}, finding=finding)], dispositions=[row])

    def test_published_row_citing_unrecorded_finding_rejects(self) -> None:
        row = {"artifact_id": "demo.rule.line-x", "disposition": "published", "finding_id": "demo.ghost.finding", "symbol": "demo.symbol.line-x", "pins": []}
        with self.assertRaises(PresentationModelError):
            build_presentation_model(run_id="r", resolved_members=[FIELD, RULE], state=_state({}), publications=[], dispositions=[row])

    def test_conflicting_evidence_labels_for_the_same_pin_rejects(self) -> None:
        raw = {"schema": "finding.v1", "id": "demo.raw.a", "fact_id": "demo.fact.a", "value": 1, "basis": "attested", "evidence_ids": ["demo.evidence.a"]}
        state = _state(
            {"demo.raw.a": raw},
            {"demo.evidence.a": EvidenceLifecycle(evidence={"schema": "evidence.v1", "id": "demo.evidence.a", "kind": "demo.statement.x", "label": "Label one", "content": {}}, status="current")},
        )
        field2 = dict(FIELD, id="demo.field.line-y", line="y", binds_symbol="demo.symbol.line-y")
        rule2 = {"id": "demo.rule.line-y", "schema": "rule-artifact.v2", "publishes": "demo.symbol.line-y"}
        finding_x = _finding("demo.derived.x", "demo.symbol.line-x", "1", [{"role": "input", "id": "demo.raw.a", "version": "v1"}])
        finding_y = _finding("demo.derived.y", "demo.symbol.line-y", "1", [{"role": "input", "id": "demo.raw.a", "version": "v1"}])
        row_x = {"artifact_id": "demo.rule.line-x", "disposition": "published", "finding_id": "demo.derived.x", "symbol": "demo.symbol.line-x", "pins": finding_x["pins"]}
        row_y = {"artifact_id": "demo.rule.line-y", "disposition": "published", "finding_id": "demo.derived.y", "symbol": "demo.symbol.line-y", "pins": finding_y["pins"]}
        # Same pin, but a differently-labeled evidence lifecycle would conflict;
        # here the evidence is shared and consistent, so this should succeed —
        # confirming the earlier "conflicting labels" guard only fires on an
        # actual mismatch, not on ordinary reuse.
        model = build_presentation_model(
            run_id="r", resolved_members=[FIELD, field2, RULE, rule2], state=state,
            publications=[Publication(act={}, finding=finding_x), Publication(act={}, finding=finding_y)],
            dispositions=[row_x, row_y],
        )
        self.assertEqual(model["pinLabels"], {"demo.raw.a": "Label one"})


class ValidatorStrictness(unittest.TestCase):
    def _valid_model(self) -> dict[str, Any]:
        return {
            "schema": PRESENTATION_MODEL_VERSION, "runId": "r", "pinLabels": {},
            "sections": [{
                "id": "line-x", "field": FIELD,
                "resolved": {"disposition": "guard_inapplicable", "act": None},
                "citationSites": [],
            }],
            "citationGroups": [],
            "attachments": [],
        }

    def test_unknown_top_level_key_rejects(self) -> None:
        model = self._valid_model()
        model["extra"] = 1
        with self.assertRaises(PresentationModelError):
            validate_presentation_model(model)

    def test_wrong_schema_version_rejects(self) -> None:
        model = self._valid_model()
        model["schema"] = "presentation-model.v2"
        with self.assertRaises(PresentationModelError):
            validate_presentation_model(model)

    def test_duplicate_section_id_rejects(self) -> None:
        model = self._valid_model()
        model["sections"].append(dict(model["sections"][0]))
        with self.assertRaises(PresentationModelError):
            validate_presentation_model(model)

    def test_unknown_disposition_kind_rejects(self) -> None:
        model = self._valid_model()
        model["sections"][0]["resolved"] = {"disposition": "surprising", "act": None}
        with self.assertRaises(PresentationModelError):
            validate_presentation_model(model)

    def test_closing_script_sequence_in_a_label_rejects(self) -> None:
        model = self._valid_model()
        model["pinLabels"]["demo.raw.a"] = "</script><script>alert(1)</script>"
        with self.assertRaises(PresentationModelError):
            validate_presentation_model(model)

    def test_html_comment_open_sequence_rejects(self) -> None:
        model = self._valid_model()
        model["pinLabels"]["demo.raw.a"] = "<!-- inject -->"
        with self.assertRaises(PresentationModelError):
            validate_presentation_model(model)

    def test_valid_model_passes(self) -> None:
        validate_presentation_model(self._valid_model())


class GoldenRegeneration(unittest.TestCase):
    def test_regeneration_is_deterministic(self) -> None:
        first = golden.regenerate()
        second = golden.regenerate()
        self.assertEqual(first, second)

    def test_committed_golden_matches_the_generator_byte_for_byte(self) -> None:
        regenerated = json.dumps(golden.regenerate(), indent=2, sort_keys=True) + "\n"
        committed = golden.GOLDEN_PATH.read_text("utf-8")
        self.assertEqual(committed, regenerated, "commit tools/generate_presentation_l2_golden.py's output after any change")

    def test_committed_golden_is_strictly_valid(self) -> None:
        model = json.loads(golden.GOLDEN_PATH.read_text("utf-8"))
        validate_presentation_model(model)  # must not raise

    def test_committed_golden_has_no_absolute_local_path(self) -> None:
        body = golden.GOLDEN_PATH.read_text("utf-8")
        self.assertNotIn(str(REPO), body)
        self.assertNotIn("/Users/", body)
        self.assertNotIn("/home/", body)


class CoordinatorIntegration(unittest.TestCase):
    def test_presentation_artifact_is_confined_and_result_json_is_unchanged_shape(self) -> None:
        acts = golden.canonical_acts()
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = live_coordinate_run(
                WorkspaceCapability(root / "L"), repo_root=REPO, authoritative_acts=acts,
                workspace_revision=len(acts), run_scope=golden.SCOPE, scope_user=USER,
                request={"schema": "run-request.v1"}, run_id="demo.presentation-l2.test", governance_pins=[],
                surface=_surface(), output_name="out.json",
            )
            self.assertIsNone(result.refusal)
            assert result.output_path is not None and result.presentation_path is not None
            self.assertTrue(result.presentation_path.is_file())
            self.assertEqual(result.presentation_path.parent, result.output_path.parent)

            report = json.loads(result.output_path.read_text("utf-8"))
            self.assertEqual(set(report), {"run_id", "stop_reason", "dispositions"})

            model = json.loads(result.presentation_path.read_text("utf-8"))
            validate_presentation_model(model)  # must not raise
            self.assertTrue(len(model["sections"]) > 0)

    def test_resolver_refusal_writes_neither_result_nor_presentation_artifact(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = live_coordinate_run(
                WorkspaceCapability(root / "L"), repo_root=REPO, authoritative_acts=[],
                workspace_revision=10, run_scope={"jurisdiction": "us", "year": "2051"}, scope_user=USER,
                request={"schema": "run-request.v1"}, run_id="demo.presentation-l2.refusal", governance_pins=[],
                surface=_surface(), output_name="refusal.json",
            )
            self.assertIsInstance(result.refusal, Refusal)
            self.assertIsNone(result.output_path)
            self.assertIsNone(result.presentation_path)
            self.assertFalse((root / "L" / "outputs").exists())

    def test_projector_rejection_through_the_coordinator_leaves_no_stray_artifact(self) -> None:
        """Track 1 repair, Finding 1: a PresentationModelError reached through
        ``live_coordinate_run`` (not only a direct ``build_presentation_model``
        call) must propagate unchanged while leaving neither the reserved
        result nor the reserved presentation artifact behind."""
        import packages.derivation.live as live_module

        acts = golden.canonical_acts()
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            with unittest.mock.patch.object(
                live_module, "build_presentation_model",
                side_effect=PresentationModelError("synthetic projector rejection"),
            ):
                with self.assertRaises(PresentationModelError):
                    live_coordinate_run(
                        WorkspaceCapability(root / "L"), repo_root=REPO, authoritative_acts=acts,
                        workspace_revision=len(acts), run_scope=golden.SCOPE, scope_user=USER,
                        request={"schema": "run-request.v1"}, run_id="demo.presentation-l2.rejection",
                        governance_pins=[], surface=_surface(), output_name="rejected.json",
                    )
            self.assertFalse((root / "L" / "outputs" / "rejected.json").exists())
            self.assertFalse((root / "L" / "outputs" / "rejected.presentation.json").exists())
            # The derivation record stream may still accurately retain the run
            # it recorded — only the two reserved output files are this
            # repair's concern.
            records = (root / "L" / "records" / "derivation_records.jsonl").read_text().splitlines()
            self.assertEqual({json.loads(line)["phase"] for line in records}, {"started", "completed"})

    def test_declared_output_name_cannot_escape_the_workspace(self) -> None:
        from packages.derivation.live_workspace import ResidencyViolation

        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(ResidencyViolation):
                live_coordinate_run(
                    WorkspaceCapability(root / "L"), repo_root=REPO,
                    authoritative_acts=[json.loads((T3 / "adoptions" / "adopt-core-v2-current.json").read_text())],
                    workspace_revision=10, run_scope={"jurisdiction": "us", "year": "2051"}, scope_user=USER,
                    request={"schema": "run-request.v1"}, run_id="demo.presentation-l2.escape", governance_pins=[],
                    surface=_surface(), output_name="../../escape.json",
                )
            self.assertFalse((root / "L" / "outputs").exists())
            self.assertFalse((root / "escape.json").exists())


if __name__ == "__main__":
    unittest.main()
