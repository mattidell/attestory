"""Track 1 — synthetic W-2 entry loop through the existing product paths."""

from __future__ import annotations

import copy
import io
import json
import shutil
import subprocess
import unittest
import urllib.error
import urllib.request
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast
from unittest.mock import patch

import packages.derivation.live as live_module
from packages.derivation.authorization import (
    STATUS_ABSENT,
    STATUS_ADMITTED,
    STATUS_YEAR_MISMATCH,
)
from packages.derivation.authorization_closure import package_boundary_digest
from packages.derivation.entry_loop import (
    COMPARISON_LINES,
    CURRENT_CORE_ENTRY_FIXTURE,
    ENTRY_CORE_PROFILES,
    ENTRY_PACKAGE_MEMBER_DIR,
    ENTRY_PACKAGE_RELEASE_DIRS,
    ENTRY_RUN_SCOPES,
    ENTRY_SEED_FIXTURES,
    ENTRY_FIELD_SCHEMA,
    EXPECTED_IMPACT_LINES,
    EntryLoopError,
    EntryLoopServer,
    SyntheticW2EntryRuntime,
    RUN_SCOPE,
    SCOPE_USER,
    W2_CLOSURE_FACT_ID,
    W2_FACT_ID,
    W2_PREDECESSOR,
    W2_SUCCESSOR,
    _line_values,
    _resolve_adopted_core_surface,
    _select_entry_core_profile,
    _parse_box1_with_format,
    build_entry_surface,
    load_seed_acts,
    resolve_entry_surface,
)
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.live import live_coordinate_run
from packages.derivation.surface_resolver import ResolvedSurface
from packages.derivation.production_resolver import (
    PublicationSurface,
    Refusal,
    ResolvedGraph,
    resolve_adopted_surface,
    resolve_production_package,
)
from packages.kernel.act_log import ActLog
from packages.derivation.loader import DerivationSchemas
from packages.derivation.runners.entry_loop_evaluation import _print_instructions
from tools.generate_entry_loop_t1_fixtures import (
    CONTENT,
    content_stats,
    render_fixture_files,
    seed_acts,
)
from tools.generate_entry_loop_v70_fixture import (
    render_fixture_files as render_v70_fixture_files,
)


REPO = Path(__file__).resolve().parent.parent
FIXTURE = REPO / "packages" / "sample_data" / "entry_loop_t1"
SOURCE = FIXTURE / "surface" / "content" / "app" / "src" / "EntryPage.svelte"
FIELD_DECLARATION = (
    FIXTURE / "surface" / "content" / "app" / "src" / "w2-box1-field.js"
)
_VENDORED = (CONTENT / "node_modules").is_dir()
_NODE = shutil.which("node")
_BROWSER = next(
    (
        str(path)
        for path in (
            Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
            Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
            Path("/usr/bin/google-chrome"),
            Path("/usr/bin/google-chrome-stable"),
            Path("/usr/bin/chromium"),
            Path("/usr/bin/chromium-browser"),
        )
        if path.is_file()
    ),
    None,
)


def _event(snapshot: dict[str, Any], value: object) -> dict[str, Any]:
    event = cast(dict[str, Any], json.loads(json.dumps(snapshot["contribution"])))
    event["payload"]["contribution"]["content"]["w2_box1"] = value
    return event


def _lines(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {line["line"]: line for line in snapshot["lines"]}


def _entry_package_boundary(
    acts: list[dict[str, Any]],
    *,
    run_scope: dict[str, str],
    surface: PublicationSurface,
) -> str:
    graph = resolve_production_package(
        acts,
        run_scope=run_scope,
        scope_user=SCOPE_USER,
        workspace_revision=len(acts),
        surface=surface,
        schemas=DerivationSchemas(),
    )
    if isinstance(graph, Refusal):
        raise AssertionError(f"adopted package refused: {graph.reason}")
    if not isinstance(graph, ResolvedGraph):
        raise AssertionError("adopted package graph is unavailable")
    corpus = {str(member["id"]): member for member in graph.resolved_members}
    entrypoint_ids = {
        str(entry["id"])
        for entry in graph.package.get("entrypoints", [])
        if isinstance(entry, dict) and isinstance(entry.get("id"), str)
    }
    root_rule_ids = {
        str(member["id"])
        for member in graph.resolved_members
        if member.get("id") in entrypoint_ids
        and isinstance(member.get("schema"), str)
        and (
            member["schema"].startswith("rule-artifact")
            or member["schema"].startswith("attachment-rule")
        )
    }
    return package_boundary_digest(root_rule_ids, corpus, package=graph.package)


def _authorization_grant_act(
    index: int,
    *,
    tax_year: str,
    universe_id: str,
) -> dict[str, Any]:
    grant_id = f"demo.entry-loop.auth.v70.{tax_year}"
    return {
        "schema": "act.v1",
        "act_id": f"demo.entry-loop.auth-act.{index}",
        "kind": "calculation-authorization",
        "actor": SCOPE_USER,
        "at": "2026-10-31T00:00:00Z",
        "committed_against": index,
        "payload": {
            "authorization": {
                "schema": "workspace-calculation-authorization.v1",
                "id": grant_id,
                "subject_id": SCOPE_USER,
                "tax_year": tax_year,
                "universe_id": universe_id,
            }
        },
    }


def _run_live_with_reporting_year_capture(
    acts: list[dict[str, Any]],
    *,
    run_scope: dict[str, str],
    surface: PublicationSurface,
    run_id: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[Any]]:
    reporting_years: list[Any] = []
    original_marshal = getattr(live_module, "marshal_live_run_context")

    def capture_reporting_year(*args: Any, **kwargs: Any) -> Any:
        reporting_years.append(kwargs.get("reporting_year"))
        return original_marshal(*args, **kwargs)

    with TemporaryDirectory(prefix="demo-entry-auth-run-") as temporary:
        capability = WorkspaceCapability(Path(temporary) / "workspace")
        with patch.object(
            live_module,
            "marshal_live_run_context",
            side_effect=capture_reporting_year,
        ):
            outcome = live_coordinate_run(
                capability,
                repo_root=REPO,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=run_scope,
                scope_user=SCOPE_USER,
                request={"schema": "run-request.v1"},
                run_id=run_id,
                governance_pins=[],
                surface=surface,
                output_name=f"{run_id}.json",
                schemas=DerivationSchemas(),
            )
        if outcome.refusal is not None:
            raise AssertionError(f"live coordinator refused: {outcome.refusal.reason}")
        if outcome.output_path is None:
            raise AssertionError("live coordinator did not write a durable report")
        if outcome.presentation_path is None:
            raise AssertionError("live coordinator did not write a presentation")
        report = json.loads(outcome.output_path.read_text("utf-8"))
        presentation = json.loads(outcome.presentation_path.read_text("utf-8"))
        outcome_status = {
            "current": outcome.current,
            "status": outcome.authorization_status,
        }
        return report, presentation, outcome_status, reporting_years


class FixtureRegeneration(unittest.TestCase):
    def test_workspace_seed_regenerates_byte_for_byte(self) -> None:
        expected = b"".join(
            json.dumps(act, sort_keys=True, separators=(",", ":")).encode("utf-8")
            + b"\n"
            for act in seed_acts()
        )
        self.assertEqual((FIXTURE / "workspace" / "acts.jsonl").read_bytes(), expected)
        self.assertEqual(load_seed_acts(REPO), seed_acts())

    @unittest.skipUnless(_VENDORED, "surface artifact vendored tree is absent")
    def test_surface_publication_regenerates_byte_for_byte(self) -> None:
        rendered = render_fixture_files()
        for relative, expected in rendered.items():
            with self.subTest(relative=relative):
                self.assertEqual((FIXTURE / relative).read_bytes(), expected)

    def test_generated_build_output_is_not_a_shipped_input(self) -> None:
        manifest = json.loads(
            (
                FIXTURE
                / "surface"
                / "manifest"
                / "surface-artifact.entry-loop.v1.json"
            ).read_text("utf-8")
        )
        self.assertFalse(
            any(entry["path"].startswith("dist/") for entry in manifest["entries"])
        )

    def test_seed_retains_w2_evidence_but_no_w2_fact_or_closure(self) -> None:
        acts = seed_acts()
        rendered = json.dumps(acts, sort_keys=True)
        self.assertIn("demo.presentation-l2.evidence.w2", rendered)
        self.assertNotIn("demo.presentation-l2.contribution.w2", rendered)
        self.assertNotIn("demo.presentation-l2.finding.wages", rendered)
        self.assertNotIn("demo.presentation-l2.closure.w2", rendered)

    def test_v70_seed_regenerates_and_leaves_only_box1_open(self) -> None:
        rendered = render_v70_fixture_files()
        for relative, expected in rendered.items():
            with self.subTest(relative=relative):
                self.assertEqual(
                    (CURRENT_CORE_ENTRY_FIXTURE / relative).read_bytes(), expected
                )
        self.assertEqual(
            load_seed_acts(REPO, seed_profile="v70"),
            [
                json.loads(line)
                for line in (CURRENT_CORE_ENTRY_FIXTURE / "workspace/acts.jsonl")
                .read_text("utf-8")
                .splitlines()
            ],
        )
        self.assertEqual(load_seed_acts(REPO), seed_acts())
        current_seed = json.dumps(
            load_seed_acts(REPO, seed_profile="v70"), sort_keys=True
        )
        self.assertIn("tax.us.2025.w2.box2-withholding", current_seed)
        self.assertNotIn("tax.us.2025.w2.box1-wages|", current_seed)
        self.assertNotIn("tax.us.2025.w2.source-closure|", current_seed)
        adoption = next(
            act for act in load_seed_acts(REPO, seed_profile="v70")
            if act.get("kind") == "package-adoption"
        )
        self.assertEqual(adoption["payload"]["scope"], ENTRY_RUN_SCOPES["v70"])
        self.assertEqual(ENTRY_RUN_SCOPES["v6"], {"jurisdiction": "us", "year": "2055"})


class EvaluationLauncherGuidance(unittest.TestCase):
    def _instructions(self, seed_profile: str) -> str:
        evaluation = json.loads(
            (
                REPO
                / ENTRY_SEED_FIXTURES[seed_profile]
                / "evaluation-w2.json"
            ).read_text("utf-8")
        )
        output = io.StringIO()
        with redirect_stdout(output):
            _print_instructions(
                url="http://127.0.0.1:8000/",
                fingerprint="demo-fingerprint",
                evaluation=evaluation,
                seed_profile=seed_profile,
            )
        return output.getvalue()

    def test_v6_launcher_guidance_is_unchanged(self) -> None:
        self.assertEqual(
            self._instructions("v6"),
            "Synthetic W-2 entry evaluation\n"
            "URL: http://127.0.0.1:8000/\n"
            "Evidence pack: docs/phases/legible-entry/entry-loop-synthetic-evidence-pack.md\n"
            "W-2 Box 1 figure to enter: 90000\n"
            "W-2 Box 1 corrected figure: 91000\n"
            "Starting-state fingerprint: sha256:demo-fingerprint\n"
            "Stop: press Ctrl-C in this terminal.\n"
            "Clean restart: stop this command, then run the same command again.\n",
        )

    def test_v70_launcher_is_technical_only_and_names_its_line_sets(self) -> None:
        output = self._instructions("v70")
        self.assertIn(
            "Mode: technical exercise only; not scoreable with the accepted v6 usability pack.",
            output,
        )
        self.assertIn(
            "Selected expected-impact Form 1040 lines: 1a, 9, 11a, 11b, 15, 16",
            output,
        )
        self.assertIn(
            "Selected untouched-comparison Form 1040 lines: 2b, 3a, 3b, 12e",
            output,
        )
        self.assertNotIn("Evidence pack:", output)


class CoreProfileSelection(unittest.TestCase):
    def test_run_scopes_keep_v6_and_align_v70_with_tax_year(self) -> None:
        self.assertEqual(RUN_SCOPE, {"jurisdiction": "us", "year": "2055"})
        self.assertEqual(ENTRY_RUN_SCOPES["v6"], RUN_SCOPE)
        self.assertEqual(
            ENTRY_RUN_SCOPES["v70"],
            {"jurisdiction": "us", "year": "2025"},
        )

    def test_profiles_name_exact_members_and_roles(self) -> None:
        v6 = ENTRY_CORE_PROFILES[("tax.us.2025.package.core-calculations", "v6")]
        v70 = ENTRY_CORE_PROFILES[("tax.us.2025.package.core-calculations", "v70")]
        self.assertEqual(
            [(field.id.rsplit("line-", 1)[-1], field.version) for field in v6.fields],
            [
                ("1a", "v1"),
                ("9", "v1"),
                ("11", "v1"),
                ("15", "v1"),
                ("16", "v1"),
                ("2b", "v1"),
                ("3a", "v1"),
                ("3b", "v1"),
                ("12", "v1"),
            ],
        )
        agi_fields = [field for field in v70.fields if field.line in {"11a", "11b"}]
        self.assertEqual(len(agi_fields), 2)
        self.assertNotEqual(agi_fields[0].id, agi_fields[1].id)
        self.assertEqual(
            [(field.line, field.version) for field in v70.fields],
            [
                ("1a", "v1"),
                ("9", "v1"),
                ("11a", "v1"),
                ("11b", "v1"),
                ("15", "v1"),
                ("16", "v1"),
                ("2b", "v6"),
                ("3a", "v1"),
                ("3b", "v1"),
                ("12e", "v1"),
            ],
        )

    def test_selected_members_read_exact_bindings_from_both_packages(self) -> None:
        expected_bindings = {
            "v6": {
                "1a": "tax.us.2025.wages.total-w2-box1",
                "9": "tax.us.2025.income.total-income",
                "11": "tax.us.2025.income.agi",
                "15": "tax.us.2025.income.taxable-income",
                "16": "tax.us.2025.tax.total-tax",
                "2b": "tax.us.2025.interest.taxable-total",
                "3a": "tax.us.2025.dividends.qualified-total",
                "3b": "tax.us.2025.dividends.ordinary-total",
                "12": "tax.us.2025.deductions.total",
            },
            "v70": {
                "1a": "tax.us.2025.wages.total-w2-box1",
                "9": "tax.us.2025.income.total-income",
                "11a": "tax.us.2025.income.agi",
                "11b": "tax.us.2025.income.agi",
                "15": "tax.us.2025.income.taxable-income",
                "16": "tax.us.2025.tax.total-tax",
                "2b": "tax.us.2025.interest.line-2b",
                "3a": "tax.us.2025.dividends.qualified-total",
                "3b": "tax.us.2025.dividends.ordinary-total",
                "12e": "tax.us.2025.deductions.line-12e",
            },
        }
        for seed_profile, expected in expected_bindings.items():
            profile = ENTRY_CORE_PROFILES[
                ("tax.us.2025.package.core-calculations", seed_profile)
            ]
            acts = load_seed_acts(REPO, seed_profile=seed_profile)
            run_scope = ENTRY_RUN_SCOPES[seed_profile]
            surface = _resolve_adopted_core_surface(
                acts,
                run_scope=run_scope,
                workspace_revision=len(acts),
                repo_root=REPO,
                schemas=DerivationSchemas(),
            )
            graph = resolve_production_package(
                acts,
                run_scope=run_scope,
                scope_user=SCOPE_USER,
                workspace_revision=len(acts),
                surface=surface,
                schemas=DerivationSchemas(),
            )
            if isinstance(graph, Refusal):
                self.fail(f"adopted package refused: {graph.reason}")
            resolved = {
                (str(member.get("id")), str(member.get("version"))): member
                for member in graph.resolved_members
                if member.get("schema") in {"form-field.v2", "form-field.v3"}
            }
            self.assertEqual(
                {(field.id, field.version) for field in profile.fields},
                {
                    key
                    for key in resolved
                    if key in {(field.id, field.version) for field in profile.fields}
                },
            )
            for field_profile in profile.fields:
                field = resolved[(field_profile.id, field_profile.version)]
                self.assertEqual(field["schema"], field_profile.schema)
                self.assertEqual(field["line"], field_profile.line)
                self.assertEqual(field["binds_symbol"], expected[field_profile.line])
                self.assertEqual(field["form"]["form_id"], "1040")
                self.assertEqual(field["form"]["authority"], "IRS")
                self.assertEqual(field["form"]["jurisdiction"], "US-federal")
                self.assertEqual(field["form"]["tax_year"], profile.tax_year)

    def test_unknown_adoption_and_mismatched_field_refuse(self) -> None:
        acts = load_seed_acts(REPO, seed_profile="v70")
        adoption = next(act for act in acts if act.get("kind") == "package-adoption")
        adoption["payload"]["package"]["version"] = "v71"
        with self.assertRaisesRegex(EntryLoopError, "entry-core-profile-unsupported"):
            _select_entry_core_profile(
                acts,
                run_scope=ENTRY_RUN_SCOPES["v70"],
                workspace_revision=len(acts),
                schemas=DerivationSchemas(),
            )

        profile = ENTRY_CORE_PROFILES[("tax.us.2025.package.core-calculations", "v70")]
        sections = []
        for member in profile.fields:
            sections.append(
                {
                    "field": {
                        "schema": member.schema,
                        "id": member.id,
                        "version": member.version,
                        "line": member.line,
                        "label": f"Form 1040 line {member.line}",
                        "binds_symbol": "demo.synthetic.package-binding",
                        "form": {
                            "authority": "IRS",
                            "form_id": "1040",
                            "jurisdiction": "US-federal",
                            "tax_year": profile.tax_year,
                        },
                    },
                    "resolved": {"disposition": "computed_zero", "value": 0},
                }
            )
        cast(dict[str, Any], sections[0])["field"]["line"] = "not-the-adopted-line"
        with self.assertRaisesRegex(EntryLoopError, "entry-state-unavailable"):
            _line_values({"sections": sections}, profile)

    def test_surface_selection_follows_each_adoption_and_refuses_wrong_root(self) -> None:
        for seed_profile, expected_root, expected_registry in (
            (
                "v6",
                "packages/sample_data/frrs_t3/publication_surface/releases",
                "packages/content/tax/2025/published-packages.json",
            ),
            (
                "v70",
                "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases",
                "packages/content/tax/2025/published-packages.v68.json",
            ),
        ):
            acts = load_seed_acts(REPO, seed_profile=seed_profile)
            surface = _resolve_adopted_core_surface(
                acts,
                run_scope=ENTRY_RUN_SCOPES[seed_profile],
                workspace_revision=len(acts),
                repo_root=REPO,
                schemas=DerivationSchemas(),
            )
            self.assertEqual(surface.release_dir, REPO / expected_root)
            self.assertEqual(
                surface.package_registry_path.relative_to(REPO).as_posix(),
                expected_registry,
            )

        current_acts = load_seed_acts(REPO, seed_profile="v70")
        wrong_root = resolve_adopted_surface(
            current_acts,
            run_scope=ENTRY_RUN_SCOPES["v70"],
            scope_user=SCOPE_USER,
            workspace_revision=len(current_acts),
            release_dir=REPO / ENTRY_PACKAGE_RELEASE_DIRS[0],
            member_dir=REPO / ENTRY_PACKAGE_MEMBER_DIR,
            schemas=DerivationSchemas(),
        )
        if not isinstance(wrong_root, Refusal):
            self.fail("wrong release root unexpectedly resolved")
        self.assertEqual(wrong_root.reason, "RELEASE_ABSENT_OR_MISMATCH")

    def test_seed_and_adoption_profiles_must_match(self) -> None:
        with TemporaryDirectory(prefix="demo-entry-profile-mismatch-") as temporary:
            capability = WorkspaceCapability(Path(temporary) / "L")
            v70_acts = copy.deepcopy(load_seed_acts(REPO, seed_profile="v70"))
            adoption = next(
                act for act in v70_acts if act.get("kind") == "package-adoption"
            )
            cast(dict[str, Any], adoption["payload"])["scope"] = dict(RUN_SCOPE)
            with self.assertRaisesRegex(EntryLoopError, "entry-seed-profile-mismatch"):
                SyntheticW2EntryRuntime(
                    capability,
                    repo_root=REPO,
                    seed_acts=v70_acts,
                )


class RuntimeFixture(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = TemporaryDirectory(prefix="demo-entry-loop-")
        self.addCleanup(self._tmp.cleanup)
        self.capability = WorkspaceCapability(Path(self._tmp.name) / "L")
        self.runtime = SyntheticW2EntryRuntime(
            self.capability,
            repo_root=REPO,
        )

    def enter(self, value: object = 90000) -> dict[str, Any]:
        initial = self.runtime.snapshot().payload
        return self.runtime.contribute(_event(initial, value)).payload


class PhaseADependencies(RuntimeFixture):
    def test_dependency_1_w2_is_the_only_prompt_and_entry_reaches_complete(self) -> None:
        initial = self.runtime.snapshot().payload
        self.assertEqual(
            initial["missing"],
            [
                {
                    "id": "w2-box1",
                    "label": "W-2 from Demo Workshop — Box 1 wages",
                    "document": "Form W-2",
                    "box": "Box 1",
                    "target": "w2-box1",
                }
            ],
        )
        self.assertFalse(initial["complete"])
        entered = self.enter()
        self.assertEqual(entered["missing"], [])
        self.assertEqual(len(entered["answered"]), 1)
        self.assertTrue(entered["computed"])
        self.assertTrue(entered["complete"])

    def test_dependency_2_loopback_post_uses_admitted_contribution_acts(self) -> None:
        with TemporaryDirectory(prefix="demo-entry-static-") as tmp:
            static = Path(tmp)
            (static / "index.html").write_text(
                "<!doctype html><title>Synthetic W-2 entry</title>",
                encoding="utf-8",
            )
            with EntryLoopServer(self.runtime, static) as server:
                root = server.url.rsplit("/", 1)[0]
                with urllib.request.urlopen(server.url, timeout=5) as response:
                    self.assertEqual(response.status, 200)
                with urllib.request.urlopen(f"{root}/api/state", timeout=5) as response:
                    initial = json.load(response)
                request = urllib.request.Request(
                    f"{root}/api/contributions",
                    data=json.dumps(_event(initial, 90000)).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(request, timeout=10) as response:
                    entered = json.load(response)
        self.assertTrue(entered["complete"])
        log = ActLog(self.capability.location, DerivationSchemas().registry, read_only=True)
        added = list(log.read().acts)[-3:]
        self.assertEqual(
            [act["kind"] for act in added],
            ["contribution", "member-transition", "assertion"],
        )
        self.assertEqual(added[0]["payload"]["contribution"]["schema"], "contribution.v1")
        self.assertEqual(
            added[1]["payload"]["member"]["finding"]["contribution_id"],
            added[0]["payload"]["contribution"]["id"],
        )

    def test_dependency_3_fixed_sets_and_completion_are_observable(self) -> None:
        initial = self.runtime.snapshot().payload
        self.assertEqual(set(_lines(initial)), set(EXPECTED_IMPACT_LINES + COMPARISON_LINES))
        entered = self.enter()
        self.assertEqual(entered["missing"], [])
        self.assertTrue(entered["complete"])
        self.assertTrue(all(line["computed"] for line in entered["lines"]))

    def test_dependency_4_entry_and_correction_move_exactly_the_fixed_set(self) -> None:
        initial = self.runtime.snapshot().payload
        entered = self.runtime.contribute(_event(initial, 90000)).payload
        corrected = self.runtime.contribute(_event(entered, 91000)).payload
        for snapshot in (entered, corrected):
            lines = _lines(snapshot)
            self.assertEqual(
                {line for line in EXPECTED_IMPACT_LINES if lines[line]["change"] == "changed"},
                set(EXPECTED_IMPACT_LINES),
            )
            self.assertEqual(
                {line for line in COMPARISON_LINES if lines[line]["change"] == "unchanged"},
                set(COMPARISON_LINES),
            )
        before = _lines(entered)
        after = _lines(corrected)
        for line in EXPECTED_IMPACT_LINES:
            self.assertNotEqual(before[line]["value"], after[line]["value"])
        for line in COMPARISON_LINES:
            self.assertEqual(before[line]["value"], after[line]["value"])


class EntryAndCorrection(RuntimeFixture):
    def test_correction_is_new_contribution_plus_plain_assertion(self) -> None:
        entered = self.enter()
        corrected = self.runtime.contribute(_event(entered, 91000)).payload
        self.assertTrue(corrected["complete"])
        self.assertEqual(corrected["last_action"], "corrected")
        log = ActLog(self.capability.location, DerivationSchemas().registry, read_only=True)
        added = list(log.read().acts)[-2:]
        self.assertEqual([act["kind"] for act in added], ["contribution", "assertion"])
        finding = added[-1]["payload"]["finding"]
        self.assertEqual(finding["value"], 91000)
        self.assertEqual(
            finding["contribution_id"],
            added[0]["payload"]["contribution"]["id"],
        )

    def test_format_declaration_and_validator_accept_the_same_forms(self) -> None:
        spec = self.runtime._w2_box1_format
        self.assertEqual(spec["commaGrouping"], "accepted")
        self.assertEqual(spec["currencyPrefix"], "accepted")
        self.assertEqual(spec["maxFractionDigits"], 2)
        self.assertTrue(spec["requirePositive"])
        self.assertEqual(spec["maxValue"], "999999999.99")

        entered = self.enter("90,000")
        self.assertTrue(entered["complete"])
        self.assertEqual(entered["answered"][0]["value"], 90000)

        corrected = self.runtime.contribute(_event(entered, "$90,000.50")).payload
        self.assertTrue(corrected["complete"])
        self.assertEqual(corrected["last_action"], "corrected")
        self.assertEqual(corrected["answered"][0]["value"], 90000.5)

    def test_validator_uses_all_declared_numeric_controls(self) -> None:
        spec = dict(self.runtime._w2_box1_format)
        spec["maxFractionDigits"] = 3
        spec["requirePositive"] = False
        spec["maxValue"] = "1000.000"

        self.assertEqual(_parse_box1_with_format("1.234", spec), 1.234)
        self.assertEqual(_parse_box1_with_format("0", spec), 0)
        self.assertEqual(_parse_box1_with_format("-1.000", spec), -1)
        with self.assertRaisesRegex(EntryLoopError, "entry-value-invalid"):
            _parse_box1_with_format("1.2345", spec)
        with self.assertRaisesRegex(EntryLoopError, "entry-value-invalid"):
            _parse_box1_with_format("1000.001", spec)

    def test_parser_rejects_malformed_max_value_ceilings(self) -> None:
        """Parser fails closed on non-positive / non-finite maxValue (Track 2d F1)."""
        base = dict(self.runtime._w2_box1_format)
        base["requirePositive"] = False

        for bad_ceiling in ("0", "-1", "-0.01", "NaN", "Infinity", "-Infinity"):
            with self.subTest(maxValue=bad_ceiling):
                spec = dict(base, maxValue=bad_ceiling)
                with self.assertRaisesRegex(EntryLoopError, "entry-format-unavailable"):
                    _parse_box1_with_format("0", spec)
                with self.assertRaisesRegex(EntryLoopError, "entry-format-unavailable"):
                    _parse_box1_with_format("-1", spec)

        with self.assertRaisesRegex(EntryLoopError, "entry-format-unavailable"):
            _parse_box1_with_format("1", dict(base, maxValue="not-a-number"))

    def test_malformed_entry_is_visible_redacted_and_does_not_advance(self) -> None:
        initial = self.runtime.snapshot().payload
        original_revision = initial["revision"]
        with TemporaryDirectory(prefix="demo-entry-static-") as tmp:
            static = Path(tmp)
            (static / "index.html").write_text("<!doctype html>", encoding="utf-8")
            with EntryLoopServer(self.runtime, static) as server:
                root = server.url.rsplit("/", 1)[0]
                rejected_value = "synthetic-not-an-amount"
                request = urllib.request.Request(
                    f"{root}/api/contributions",
                    data=json.dumps(_event(initial, rejected_value)).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    urllib.request.urlopen(request, timeout=5)
                body = caught.exception.read().decode("utf-8")
                caught.exception.close()
        self.assertEqual(caught.exception.code, 422)
        self.assertNotIn(rejected_value, body)
        self.assertIn("positive dollar amount", body)
        self.assertEqual(self.runtime.snapshot().revision, original_revision)
        self.assertFalse(self.runtime.snapshot().payload["complete"])


class CurrentCoreEntryAndCorrection(unittest.TestCase):
    def test_v70_first_entry_correction_and_fresh_coordinator_agree(self) -> None:
        profile = ENTRY_CORE_PROFILES[("tax.us.2025.package.core-calculations", "v70")]
        with TemporaryDirectory(prefix="demo-entry-loop-v70-") as temporary:
            capability = WorkspaceCapability(Path(temporary) / "runtime")
            runtime = SyntheticW2EntryRuntime(
                capability,
                repo_root=REPO,
                seed_profile="v70",
            )
            initial = runtime.snapshot().payload
            initial_lines = _lines(initial)
            self.assertEqual(
                set(initial_lines), {field.line for field in profile.fields}
            )
            self.assertEqual(
                initial["missing"][0]["id"],
                "w2-box1",
            )
            self.assertFalse(initial["complete"])
            for line in ("1a", "9", "11a", "11b", "15", "16"):
                self.assertFalse(initial_lines[line]["computed"], line)
            for line in ("2b", "3a", "3b"):
                self.assertTrue(initial_lines[line]["computed"], line)
            self.assertFalse(initial_lines["12e"]["computed"])

            entered = runtime.contribute(_event(initial, 50000)).payload
            entered_lines = _lines(entered)
            self.assertEqual(entered["last_action"], "entered")
            self.assertEqual(entered["missing"], [])
            self.assertTrue(entered["complete"])
            self.assertEqual(entered_lines["1a"]["value"], 50000)
            self.assertEqual(entered_lines["11a"]["value"], entered_lines["11b"]["value"])

            corrected = runtime.contribute(_event(entered, 91000)).payload
            corrected_lines = _lines(corrected)
            self.assertEqual(corrected["last_action"], "corrected")
            self.assertTrue(corrected["complete"])
            for field in profile.fields:
                before = entered_lines[field.line]
                after = corrected_lines[field.line]
                if field.group == "expected-impact":
                    self.assertNotEqual(before["value"], after["value"], field.line)
                    self.assertEqual(after["change"], "changed", field.line)
                else:
                    self.assertEqual(before["value"], after["value"], field.line)
                    self.assertEqual(after["change"], "unchanged", field.line)

            log = ActLog(
                capability.location,
                DerivationSchemas().registry,
                read_only=True,
            )
            acts = list(log.read().acts)
            seed_count = len(load_seed_acts(REPO, seed_profile="v70"))
            added = acts[seed_count:]
            self.assertEqual(
                [act["kind"] for act in added],
                ["contribution", "member-transition", "assertion", "contribution", "assertion"],
            )
            first_member = added[1]["payload"]
            self.assertEqual(first_member["family"]["id"], "tax.us.2025.w2")
            self.assertEqual(
                first_member["successor"],
                {"id": W2_SUCCESSOR, "predecessor": W2_PREDECESSOR},
            )
            self.assertEqual(first_member["member"]["finding"]["fact_id"], W2_FACT_ID)
            self.assertEqual(
                first_member["member"]["finding"]["contribution_id"],
                added[0]["payload"]["contribution"]["id"],
            )
            self.assertEqual(
                added[2]["payload"]["finding"]["fact_id"],
                W2_CLOSURE_FACT_ID,
            )
            self.assertEqual(added[3]["payload"]["contribution"]["content"]["w2_box1"], 91000)
            self.assertEqual(added[4]["payload"]["finding"]["value"], 91000)
            supplied_box2 = [
                act["payload"]["finding"]
                for act in acts
                if act.get("kind") == "assertion"
                and str(act.get("payload", {}).get("finding", {}).get("fact_id", "")).startswith(
                    "tax.us.2025.w2.box2-withholding|"
                )
            ]
            self.assertEqual(len(supplied_box2), 1)
            self.assertEqual(supplied_box2[0]["value"], 4500)

            surface = _resolve_adopted_core_surface(
                acts,
                run_scope=ENTRY_RUN_SCOPES["v70"],
                workspace_revision=len(acts),
                repo_root=REPO,
                schemas=DerivationSchemas(),
            )
            fresh_report, fresh_model, fresh_status, reporting_years = (
                _run_live_with_reporting_year_capture(
                    acts,
                    run_scope=ENTRY_RUN_SCOPES["v70"],
                    surface=surface,
                    run_id="demo.entry-loop.fresh-v70-comparison",
                )
            )
            self.assertEqual(reporting_years, [2025])
            self.assertFalse(fresh_report["current"])
            self.assertEqual(fresh_report["authorization_status"], STATUS_ABSENT)
            self.assertEqual(fresh_status["current"], fresh_report["current"])
            self.assertEqual(fresh_status["status"], fresh_report["authorization_status"])
            fresh_lines = _line_values(fresh_model, profile)
            fields_by_line = {
                section["field"]["line"]: section["field"]
                for section in fresh_model["sections"]
                if section.get("field", {}).get("line")
                in {field.line for field in profile.fields}
            }
            self.assertEqual(
                fields_by_line["11a"]["binds_symbol"],
                fields_by_line["11b"]["binds_symbol"],
            )
            self.assertEqual(
                fields_by_line["2b"]["binds_symbol"],
                "tax.us.2025.interest.line-2b",
            )
            for line, fresh in fresh_lines.items():
                for key in ("title", "computed", "value"):
                    self.assertEqual(
                        corrected_lines[line][key],
                        fresh[key],
                        f"{line}.{key}",
                    )

            # Reproduce the reviewed wrong-year case: the adoption and
            # coordinator both use the legacy synthetic 2055 scope, but the
            # matching synthetic grant is for the Form 1040 tax year 2025.
            wrong_year_acts = copy.deepcopy(acts)
            wrong_year_adoption = next(
                act for act in wrong_year_acts
                if act.get("kind") == "package-adoption"
            )
            cast(dict[str, Any], wrong_year_adoption["payload"])["scope"] = dict(RUN_SCOPE)
            wrong_year_surface = _resolve_adopted_core_surface(
                wrong_year_acts,
                run_scope=RUN_SCOPE,
                workspace_revision=len(wrong_year_acts),
                repo_root=REPO,
                schemas=DerivationSchemas(),
            )
            wrong_year_universe = _entry_package_boundary(
                wrong_year_acts,
                run_scope=RUN_SCOPE,
                surface=wrong_year_surface,
            )
            wrong_year_grant = _authorization_grant_act(
                len(wrong_year_acts),
                tax_year="2025",
                universe_id=wrong_year_universe,
            )
            wrong_year_acts.append(wrong_year_grant)
            wrong_report, wrong_model, wrong_status, wrong_reporting_years = (
                _run_live_with_reporting_year_capture(
                    wrong_year_acts,
                    run_scope=RUN_SCOPE,
                    surface=wrong_year_surface,
                    run_id="demo.entry-loop.wrong-year-control",
                )
            )
            self.assertEqual(wrong_reporting_years, [2055])
            self.assertFalse(wrong_report["current"])
            self.assertEqual(wrong_report["authorization_status"], STATUS_YEAR_MISMATCH)
            self.assertEqual(wrong_status["current"], wrong_report["current"])
            self.assertEqual(wrong_status["status"], wrong_report["authorization_status"])

            # With the v70 profile's matching 2025 adoption and run scope, a
            # 2025 grant is admitted and that currentness is persisted.
            current_year_acts = copy.deepcopy(acts)
            current_year_surface = _resolve_adopted_core_surface(
                current_year_acts,
                run_scope=ENTRY_RUN_SCOPES["v70"],
                workspace_revision=len(current_year_acts),
                repo_root=REPO,
                schemas=DerivationSchemas(),
            )
            current_year_universe = _entry_package_boundary(
                current_year_acts,
                run_scope=ENTRY_RUN_SCOPES["v70"],
                surface=current_year_surface,
            )
            current_year_grant = _authorization_grant_act(
                len(current_year_acts),
                tax_year="2025",
                universe_id=current_year_universe,
            )
            current_year_acts.append(current_year_grant)
            current_report, current_model, current_status, current_reporting_years = (
                _run_live_with_reporting_year_capture(
                    current_year_acts,
                    run_scope=ENTRY_RUN_SCOPES["v70"],
                    surface=current_year_surface,
                    run_id="demo.entry-loop.current-year-grant",
                )
            )
            self.assertEqual(current_reporting_years, [2025])
            self.assertTrue(current_report["current"])
            self.assertEqual(current_report["authorization_status"], STATUS_ADMITTED)
            self.assertEqual(
                current_report["authorization_grant_id"],
                "demo.entry-loop.auth.v70.2025",
            )
            self.assertEqual(current_status["current"], current_report["current"])
            self.assertEqual(current_status["status"], current_report["authorization_status"])
            wrong_year_lines = _line_values(wrong_model, profile)
            current_year_lines = _line_values(current_model, profile)
            self.assertTrue(wrong_year_lines["1a"]["computed"])
            self.assertEqual(wrong_year_lines["1a"]["value"], 91000)
            self.assertEqual(
                wrong_year_lines["1a"]["value"],
                current_year_lines["1a"]["value"],
            )


class FieldContract(RuntimeFixture):
    """Track 3: 2.1 and 2.2 checked against the entry-field.v1 declaration."""

    def test_snapshot_exposes_the_declared_field_contract(self) -> None:
        contract = self.runtime.snapshot().payload["field_contract"]["w2-box1"]
        self.assertEqual(contract["schema"], "entry-field.v1")
        # 2.1 -- source document and exact box, checkable as data.
        self.assertEqual(contract["source"]["document"], "Form W-2")
        self.assertEqual(contract["source"]["box"], "Box 1")
        self.assertEqual(contract["source"]["label"], "Wages, tips, other compensation")
        # 2.2 -- return destination and completion purpose, checkable as data.
        self.assertEqual(contract["destination"]["form"], "Form 1040")
        self.assertEqual(contract["destination"]["line"], "1a")
        self.assertNotEqual(contract["purpose"].strip().lower(), "required")
        self.assertIn("wages", contract["purpose"])
        # Correction affordance: same field, no restart.
        self.assertEqual(contract["correction"]["kind"], "same-field-reuse")
        # The format sub-object is Track 2d's declaration, reused rather than
        # duplicated; the runtime's own validator dict is that same object.
        self.assertEqual(contract["format"], self.runtime._w2_box1_format)

    def test_field_contract_validates_against_its_schema(self) -> None:
        import jsonschema

        schema = json.loads(
            (
                REPO
                / "packages"
                / "schemas"
                / "entry"
                / "entry-field.v1.schema.json"
            ).read_text("utf-8")
        )
        contract = self.runtime.snapshot().payload["field_contract"]["w2-box1"]
        jsonschema.validate(contract, schema)

    def test_malformed_field_declaration_fails_closed(self) -> None:
        from packages.derivation.entry_loop import (
            EntryLoopError,
            _load_w2_box1_field,
            _load_w2_box1_format,
        )

        format_spec = _load_w2_box1_format(REPO)
        with TemporaryDirectory(prefix="demo-entry-field-") as tmp:
            broken_root = Path(tmp)
            target = (
                broken_root
                / "packages"
                / "sample_data"
                / "entry_loop_t1"
                / "surface"
                / "content"
                / "app"
                / "src"
                / "w2-box1-field.js"
            )
            target.parent.mkdir(parents=True)
            target.write_text(
                'export const W2_BOX1_FIELD = {"schema": "entry-field.v1"};\n',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(EntryLoopError, "entry-field-unavailable"):
                _load_w2_box1_field(broken_root, format_spec)

    @staticmethod
    def _write_field_declaration(
        root: Path,
        declaration_without_format: dict[str, Any],
    ) -> None:
        # Real files reference the imported W2_BOX1_FORMAT binding rather
        # than inlining it, and the loader's marker-substitution only fires
        # on that exact bare-identifier convention -- so these regression
        # cases use it too, rather than a fully-inlined literal, to exercise
        # the actual load path.
        #
        # Track 3 repair 2, F2: the loader's closing-marker search requires
        # "\n};\n" -- a newline, then the closing brace, then the semicolon,
        # then a newline. A compact single-line JSON body followed directly
        # by "};\n" (no newline before the brace) never matches that and
        # fails at the marker step every time, before schema validation runs
        # at all -- which is exactly how the prior version of this helper
        # made every case using it pass for the wrong reason. The object
        # literal must close on its own line, as the real file does.
        target = (
            root
            / "packages"
            / "sample_data"
            / "entry_loop_t1"
            / "surface"
            / "content"
            / "app"
            / "src"
            / "w2-box1-field.js"
        )
        target.parent.mkdir(parents=True, exist_ok=True)
        body = json.dumps(declaration_without_format)
        assert body.endswith("}")
        text = (
            "export const W2_BOX1_FIELD = "
            + body[:-1]
            + ', "format": W2_BOX1_FORMAT\n};\n'
        )
        target.write_text(text, encoding="utf-8")

        # Track 3 repair 2, F2: the loader also reads entry-field.v1 from
        # this same repo_root; a temporary root with no schema file fails
        # there regardless of the declaration, which was the prior version's
        # second, independent way to pass for the wrong reason.
        schema_target = root / ENTRY_FIELD_SCHEMA
        schema_target.parent.mkdir(parents=True, exist_ok=True)
        schema_target.write_text(
            (REPO / ENTRY_FIELD_SCHEMA).read_text("utf-8"), encoding="utf-8"
        )

    def test_loader_now_rejects_what_the_schema_rejects(self) -> None:
        """Track 3 repair F2: schema validation replaces hand-rolled checks."""
        from packages.derivation.entry_loop import (
            EntryLoopError,
            _load_w2_box1_field,
            _load_w2_box1_format,
        )

        format_spec = _load_w2_box1_format(REPO)
        base = {
            "schema": "entry-field.v1",
            "id": "tax.us.2025.w2.box1-wages",
            "version": "v1",
            "source": {
                "document": "Form W-2",
                "box": "Box 1",
                "label": "Wages, tips, other compensation",
            },
            "destination": {"form": "Form 1040", "line": "1a"},
            "purpose": "resolves the missing wages needed to compute income",
            "correction": {"kind": "same-field-reuse", "affordance": "x"},
        }

        missing_id_bad_version = dict(base, version="not-a-version")
        del missing_id_bad_version["id"]
        cases: dict[str, dict[str, Any]] = {
            "missing_id_bad_version": missing_id_bad_version,
            "unknown_top_level_key": dict(base, extra_unknown_key=True),
            "unknown_correction_kind": dict(
                base,
                correction={"kind": "modal-reopen", "affordance": "x"},
            ),
        }
        for name, declaration in cases.items():
            with self.subTest(case=name):
                with TemporaryDirectory(prefix="demo-entry-field-") as tmp:
                    root = Path(tmp)
                    self._write_field_declaration(root, declaration)
                    with self.assertRaisesRegex(
                        EntryLoopError, "entry-field-unavailable"
                    ):
                        _load_w2_box1_field(root, format_spec)

    def test_schema_does_not_relate_format_to_source_or_destination(self) -> None:
        """Track 3 repair 2, F1: the schema's actual, narrow boundary.

        entry-field.v1 checks that a declaration is well-formed and that its
        format names a *supported* variant -- today, only currency-amount.
        It does not, and structurally cannot from this shape alone, check
        that the declared format is the *correct* one for the field's own
        source/destination: a declaration for a checkbox, an employer name,
        a date, or a filing-status choice validates unchanged as long as it
        still carries the ten-key currency-amount object. That is a false
        declaration, not a malformed one, and nothing in this schema -- or
        this milestone -- catches it.
        """
        import jsonschema

        schema = json.loads(
            (
                REPO
                / "packages"
                / "schemas"
                / "entry"
                / "entry-field.v1.schema.json"
            ).read_text("utf-8")
        )
        base_contract = json.loads(
            json.dumps(self.runtime.snapshot().payload["field_contract"]["w2-box1"])
        )
        non_money_sources = {
            "W-2 Box 13 checkbox": {
                "document": "Form W-2",
                "box": "Box 13",
                "label": "Retirement plan",
            },
            "employer name/EIN": {
                "document": "Form W-2",
                "box": "c",
                "label": "Employer identification number",
            },
            "date": {
                "document": "Form W-2",
                "box": "Box 15",
                "label": "Date of hire",
            },
            "filing-status choice": {
                "document": "Form 1040",
                "box": "Filing status",
                "label": "Single, married filing jointly, ...",
            },
        }
        for name, source in non_money_sources.items():
            with self.subTest(field=name):
                declaration = dict(base_contract, source=source)
                # Still schema-valid: nothing here relates 'kind' to source.
                jsonschema.validate(declaration, schema)

    def test_format_schema_rejects_a_currency_object_missing_the_discriminator(
        self,
    ) -> None:
        """Track 3 repair F1: 'kind' is load-bearing, not decorative."""
        import jsonschema

        schema = json.loads(
            (
                REPO
                / "packages"
                / "schemas"
                / "entry"
                / "entry-field.v1.schema.json"
            ).read_text("utf-8")
        )
        contract = json.loads(
            json.dumps(self.runtime.snapshot().payload["field_contract"]["w2-box1"])
        )
        del contract["format"]["kind"]
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(contract, schema)


class AdversarialEntryBoundary(RuntimeFixture):
    def setUp(self) -> None:
        super().setUp()
        self._static = TemporaryDirectory(prefix="demo-entry-static-")
        self.addCleanup(self._static.cleanup)
        static = Path(self._static.name)
        (static / "index.html").write_text("<!doctype html>", encoding="utf-8")
        self._server = EntryLoopServer(self.runtime, static)
        self.addCleanup(self._server.close)
        self._endpoint = (
            self._server.url.rsplit("/", 1)[0] + "/api/contributions"
        )

    def _post(
        self,
        body: bytes,
        *,
        content_type: str = "application/json",
    ) -> tuple[int, bytes]:
        request = urllib.request.Request(
            self._endpoint,
            data=body,
            headers={"Content-Type": content_type},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                return response.status, response.read()
        except urllib.error.HTTPError as exc:
            try:
                return exc.code, exc.read()
            finally:
                exc.close()

    def _assert_fails_closed(
        self,
        body: bytes,
        *,
        status: int,
        marker: bytes,
        content_type: str = "application/json",
    ) -> None:
        revision = self.runtime.snapshot().revision
        actual_status, response = self._post(
            body,
            content_type=content_type,
        )
        self.assertEqual(actual_status, status)
        self.assertNotIn(marker, response)
        self.assertEqual(self.runtime.snapshot().revision, revision)

    def test_wrong_content_type_fails_closed(self) -> None:
        marker = b"demo-wrong-content-type"
        self._assert_fails_closed(
            marker,
            status=415,
            marker=marker,
            content_type="text/plain",
        )

    def test_oversized_body_fails_closed(self) -> None:
        marker = b"demo-oversized-body"
        body = json.dumps(
            {
                "marker": marker.decode("ascii"),
                "padding": "x" * 16_384,
            }
        ).encode("utf-8")
        self._assert_fails_closed(body, status=400, marker=marker)

    def test_malformed_json_fails_closed(self) -> None:
        marker = b"demo-malformed-json"
        self._assert_fails_closed(
            b'{"marker":"' + marker,
            status=400,
            marker=marker,
        )

    def test_json_type_confusion_fails_closed(self) -> None:
        marker = b"demo-json-type-confusion"
        body = json.dumps([marker.decode("ascii")]).encode("utf-8")
        self._assert_fails_closed(body, status=400, marker=marker)

    def test_template_tampering_fails_closed(self) -> None:
        marker = b"demo-template-tampering"
        submitted = _event(self.runtime.snapshot().payload, 80_123.45)
        submitted["actor"] = marker.decode("ascii")
        self._assert_fails_closed(
            json.dumps(submitted).encode("utf-8"),
            status=422,
            marker=marker,
        )

    def test_duplicate_submission_fails_closed(self) -> None:
        marker = b"80123.45"
        submitted = _event(self.runtime.snapshot().payload, marker.decode("ascii"))
        body = json.dumps(submitted).encode("utf-8")
        accepted_status, _ = self._post(body)
        self.assertEqual(accepted_status, 200)
        self._assert_fails_closed(body, status=422, marker=marker)

    def test_out_of_order_submission_fails_closed(self) -> None:
        snapshot = self.runtime.snapshot().payload
        first = _event(snapshot, 81_123.45)
        marker = b"82123.45"
        later = _event(snapshot, marker.decode("ascii"))
        accepted_status, _ = self._post(json.dumps(first).encode("utf-8"))
        self.assertEqual(accepted_status, 200)
        self._assert_fails_closed(
            json.dumps(later).encode("utf-8"),
            status=422,
            marker=marker,
        )

    def test_bad_grouping_variants_still_fail_closed(self) -> None:
        for bad in ("9,0,0", "$$90000", "90,00.5"):
            with self.subTest(bad=bad):
                current = self.runtime.snapshot().payload
                self._assert_fails_closed(
                    json.dumps(_event(current, bad)).encode("utf-8"),
                    status=422,
                    marker=bad.encode("utf-8"),
                )


@unittest.skipUnless(
    _NODE and _VENDORED,
    "needs Node and the surface artifact vendored tree",
)
class SurfaceArtifactBuild(unittest.TestCase):
    def test_surface_resolves_and_builds_inside_the_synthetic_workspace(self) -> None:
        resolved = resolve_entry_surface(REPO)
        self.assertIsInstance(resolved, ResolvedSurface)
        count, total = content_stats()
        self.assertEqual(resolved.entry_count, count)
        self.assertEqual(resolved.total_bytes, total)
        with TemporaryDirectory(prefix="demo-entry-build-") as tmp:
            capability = WorkspaceCapability(Path(tmp) / "L")
            dist = build_entry_surface(capability, repo_root=REPO)
            html = (dist / "index.html").read_text("utf-8")
            self.assertIn("W-2 entry · Attestory", html)
            self.assertTrue((dist / "EntryPage.js").is_file())


@unittest.skipUnless(
    _NODE and _BROWSER and _VENDORED,
    "needs Node, a local Chrome/Chromium, and the surface artifact vendored tree",
)
class CompiledClientIntegration(RuntimeFixture):
    def test_compiled_client_drives_the_real_entry_api(self) -> None:
        assert _NODE is not None
        dist = build_entry_surface(self.capability, repo_root=REPO)
        with EntryLoopServer(self.runtime, dist) as server:
            result = subprocess.run(
                [
                    _NODE,
                    str(REPO / "tests" / "helpers" / "entry_loop_browser_client.mjs"),
                    server.url,
                ],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        observed = json.loads(result.stdout)
        self.assertEqual(
            observed,
            {
                "complete": True,
                "contributionRequest": True,
                "stateRequest": True,
            },
        )
        self.assertTrue(self.runtime.snapshot().payload["complete"])


@unittest.skipUnless(
    _NODE and _BROWSER and _VENDORED,
    "needs Node, a local Chrome/Chromium, and the surface artifact vendored tree",
)
class RenderedFieldDerivation(RuntimeFixture):
    """Track 3 repair F3: the DOM text changes when the declaration does.

    Builds the real surface from a copy of the fixture whose field
    declaration carries distinct synthetic text in place of the shipped
    source label, destination line, and purpose, then asserts the compiled,
    browser-rendered page shows the new text and not the original -- proving
    derivation rather than the presence of matching characters somewhere in
    the source file.
    """

    def test_dom_text_follows_a_mutated_declaration(self) -> None:
        assert _NODE is not None
        original = (
            CONTENT / "src" / "w2-box1-field.js"
        ).read_text("utf-8")
        replacements = {
            '"box": "Box 1"': '"box": "SYNTH-BOX-77"',
            '"label": "Wages, tips, other compensation"': (
                '"label": "Synthetic Track3 Field Label"'
            ),
            '"line": "1a"': '"line": "SYNTH-LINE-77"',
            (
                '"purpose": "resolves the missing wages needed to '
                'compute income"'
            ): '"purpose": "synthetic track3 purpose fragment"',
        }
        mutated = original
        for before, after in replacements.items():
            self.assertEqual(
                original.count(before),
                1,
                f"expected exactly one occurrence of {before!r} to mutate",
            )
            mutated = mutated.replace(before, after)

        with TemporaryDirectory(prefix="demo-entry-derivation-") as tmp:
            content_copy = Path(tmp) / "app"
            shutil.copytree(CONTENT, content_copy)
            (content_copy / "src" / "w2-box1-field.js").write_text(
                mutated, encoding="utf-8"
            )
            build = subprocess.run(
                [_NODE, "build.mjs"],
                cwd=content_copy,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60,
                check=False,
            )
            self.assertEqual(build.returncode, 0, build.stderr)
            dist = content_copy / "dist"

            with EntryLoopServer(self.runtime, dist) as server:
                result = subprocess.run(
                    [
                        _NODE,
                        str(
                            REPO
                            / "tests"
                            / "helpers"
                            / "entry_loop_field_derivation_client.mjs"
                        ),
                        server.url,
                        json.dumps(
                            [
                                "SYNTH-BOX-77",
                                "Synthetic Track3 Field Label",
                                "SYNTH-LINE-77",
                                "synthetic track3 purpose fragment",
                            ]
                        ),
                        json.dumps(
                            [
                                "Wages, tips, other compensation",
                                "feeds Form 1040 line 1a",
                            ]
                        ),
                    ],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=30,
                    check=False,
                )
        self.assertEqual(result.returncode, 0, result.stderr)
        observed = json.loads(result.stdout)
        self.assertEqual(observed, {"present": True, "absent": True})


@unittest.skipUnless(
    _NODE and _BROWSER and _VENDORED,
    "needs Node, a local Chrome/Chromium, and the surface artifact vendored tree",
)
class FocusIndicators(RuntimeFixture):
    """Track 4: one durable, per-control focus-indicator invariant.

    Enumerates every focusable control reachable by Tab from the real,
    compiled, browser-rendered page -- in both the incomplete state and the
    complete state reached by actually submitting the W-2 Box 1 amount --
    and asserts the general rule for each one, computed from live rendered
    colours: the focus style differs from the resting style, and some
    component of the focus indicator (outline or box-shadow) measures at
    least 3:1 against the background adjacent to the control. No control is
    named here; a control added later inherits the same check by simply
    being reachable by Tab, and the test fails for it the same way it would
    have failed for `#w2-box1` before this track's CSS fix.
    """

    def test_every_focusable_control_has_a_distinct_indicator(self) -> None:
        assert _NODE is not None
        dist = build_entry_surface(self.capability, repo_root=REPO)
        with EntryLoopServer(self.runtime, dist) as server:
            result = subprocess.run(
                [
                    _NODE,
                    str(
                        REPO
                        / "tests"
                        / "helpers"
                        / "entry_loop_focus_indicator_client.mjs"
                    ),
                    server.url,
                ],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        findings = json.loads(result.stdout)
        # A guard against a vacuous pass: if Tab traversal or the page
        # itself broke, the probe would report no findings at all rather
        # than failing findings, and an empty list would trivially satisfy
        # "every finding passes." The six controls the charter enumerated
        # (wordmark, Enter this fact, the amount input, the submit button in
        # both its Add and Update states, Correct this fact, Review W-2
        # Box 1) must all be found; the probe records the button under
        # whichever phase it was captured in, so Add and Update need not
        # both appear in the same run.
        self.assertGreaterEqual(len(findings), 6, findings)
        self.assertTrue(
            any("w2-box1" in finding["key"] for finding in findings), findings
        )
        for finding in findings:
            with self.subTest(control=finding["key"], phase=finding["phase"]):
                self.assertTrue(finding["differsFromResting"], finding)
                self.assertTrue(
                    any(ratio["ratio"] >= 3.0 for ratio in finding["ratios"]),
                    finding,
                )


@unittest.skipUnless(
    _NODE and _BROWSER and _VENDORED,
    "needs Node, a local Chrome/Chromium, and the surface artifact vendored tree",
)
class KeyboardOperability(RuntimeFixture):
    """Track 1: the accessibility row's unmeasured half, made mechanical.

    Runs `entry_loop_keyboard_operability_client.mjs` against the real,
    compiled, browser-rendered page and checks three durable, rule-based
    properties -- none of them a hard-coded control list -- for both the
    incomplete and the complete state: (1) the set of controls reachable by
    Tab forward equals the set reachable by Shift+Tab backward from the
    last one; (2) every control classified as actionable by its own DOM
    shape (link, button, submit/button/reset input, role="button")
    activates with its standard key and produces an observed change in a
    page-level fingerprint, not merely the absence of an exception; (3) the
    entire run drives the page exclusively through
    `Input.dispatchKeyEvent` -- zero `Input.dispatchMouseEvent` calls.
    """

    def _run(self, defect: str | None = None) -> dict[str, Any]:
        assert _NODE is not None
        dist = build_entry_surface(self.capability, repo_root=REPO)
        args = [
            _NODE,
            str(
                REPO
                / "tests"
                / "helpers"
                / "entry_loop_keyboard_operability_client.mjs"
            ),
        ]
        with EntryLoopServer(self.runtime, dist) as server:
            args.append(server.url)
            if defect:
                args.append(defect)
            result = subprocess.run(
                args,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        return cast(dict[str, Any], json.loads(result.stdout))

    def test_reverse_traversal_matches_and_activation_bites_by_effect(self) -> None:
        findings = self._run()

        # Vacuous-pass guard: a broken probe (dead page, broken Tab
        # traversal) reports empty lists, which would trivially satisfy
        # "every finding passes." Both phases must actually have run, and
        # w2-box1's own controls must be among what was found -- the same
        # shape of guard FocusIndicators uses.
        self.assertEqual(
            {entry["phase"] for entry in findings["reverseTraversal"]},
            {"incomplete", "complete"},
        )
        self.assertGreaterEqual(len(findings["activation"]), 5, findings)
        self.assertTrue(
            any("w2-box1" in entry["key"] for entry in findings["activation"]),
            findings,
        )
        self.assertTrue(findings["navigation"], findings)

        # Check 1: reverse traversal. No control forward-only or
        # backward-only, positional order matches forward reversed, and
        # backward walk terminates by returning to seed in both states.
        for entry in findings["reverseTraversal"]:
            with self.subTest(phase=entry["phase"]):
                self.assertTrue(entry["returnedToSeed"], entry)
                self.assertEqual(entry["forwardOnly"], [], entry)
                self.assertEqual(entry["backwardOnly"], [], entry)
                self.assertTrue(entry["setMatches"], entry)
                self.assertTrue(entry["orderMatches"], entry)
                self.assertIsNone(entry["mismatchIndex"], entry)
                self.assertTrue(entry["matches"], entry)

        # Check 2: activation by observed effect. Every control this run
        # classified as actionable must have activated with its standard
        # key; a control the probe found but judged not actionable (a bare
        # text input) is exempt from this half.
        for entry in findings["activation"]:
            with self.subTest(control=entry["key"], phase=entry["phase"]):
                if not entry["actionable"]:
                    continue
                self.assertIsNotNone(entry["activatedWith"], entry)

        # The wordmark link: Enter must actually navigate.
        for entry in findings["navigation"]:
            with self.subTest(control=entry["key"], phase=entry["phase"]):
                self.assertTrue(entry["navigated"], entry)

        # Check 3: no mouse. The entire run -- both phases, every check --
        # never dispatched a synthetic pointer event.
        self.assertEqual(findings["mouseEventsDispatched"], 0, findings)

    def test_reverse_traversal_check_bites_when_backward_reachability_breaks(
        self,
    ) -> None:
        """Demonstration: disable backward reachability, confirm the check
        catches it.

        Injects a capturing Shift+Tab listener on "Enter this fact" that
        preventDefaults the browser's own focus-move, trapping backward
        traversal there. Forward Tab still reaches every control normally
        -- only Shift+Tab breaks -- so the wordmark link (earlier in the
        order) becomes reachable forward but not backward. Observed:
        `forwardOnly` for the incomplete phase names the wordmark link and
        `matches` is False. Restoring the clean run (the test above)
        confirms the check passes once the trap is gone.
        """
        findings = self._run(defect="break-reverse-traversal")
        incomplete = next(
            entry
            for entry in findings["reverseTraversal"]
            if entry["phase"] == "incomplete"
        )
        self.assertFalse(incomplete["matches"], incomplete)
        self.assertFalse(incomplete["setMatches"], incomplete)
        self.assertTrue(
            any("wordmark" in key for key in incomplete["forwardOnly"]),
            incomplete,
        )

    def test_reverse_traversal_check_bites_when_order_is_scrambled(
        self,
    ) -> None:
        """Demonstration: scramble backward traversal order while preserving
        the set of reachable controls, confirming the order check catches it.

        Injects a Shift+Tab handler that visits every control in a scrambled
        sequence. Observed: `setMatches` is True (`forwardOnly: []`,
        `backwardOnly: []`), but `orderMatches` is False with a non-null
        `mismatchIndex`, proving the order check catches an order defect that
        set membership alone misses.
        """
        findings = self._run(defect="scramble-order")
        incomplete = next(
            entry
            for entry in findings["reverseTraversal"]
            if entry["phase"] == "incomplete"
        )
        self.assertTrue(incomplete["setMatches"], incomplete)
        self.assertEqual(incomplete["forwardOnly"], [], incomplete)
        self.assertEqual(incomplete["backwardOnly"], [], incomplete)
        self.assertFalse(incomplete["orderMatches"], incomplete)
        self.assertFalse(incomplete["matches"], incomplete)
        self.assertIsNotNone(incomplete["mismatchIndex"], incomplete)
        # The probe itself still never touched the mouse to compensate.
        self.assertEqual(findings["mouseEventsDispatched"], 0, findings)

    def test_activation_check_bites_when_a_control_swallows_its_key(self) -> None:
        """Demonstration: disable a control's Enter/Space handling, confirm
        the check catches it.

        Injects a capturing keydown listener on "Enter this fact" that
        preventDefaults and stops propagation for Enter and Space --
        exactly the charter's named failure shape, a button that silently
        swallows its activation key with no exception raised. Observed:
        that control's activation finding has `activatedWith: null` where
        the clean run above has a real key name. Restoring the clean run
        confirms the check passes once the swallow is gone.
        """
        findings = self._run(defect="swallow-activation")
        target = next(
            entry
            for entry in findings["activation"]
            if entry["phase"] == "incomplete" and "Enter this fact" in entry["key"]
        )
        self.assertIsNone(target["activatedWith"], target)
        # The probe itself still never touched the mouse to compensate.
        self.assertEqual(findings["mouseEventsDispatched"], 0, findings)


class SurfaceCriteria(unittest.TestCase):
    source: str
    field_declaration: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.source = SOURCE.read_text("utf-8")
        cls.field_declaration = FIELD_DECLARATION.read_text("utf-8")

    def test_missing_item_navigates_directly_to_its_input(self) -> None:
        self.assertIn("Enter this fact", self.source)
        self.assertIn("goToWages", self.source)
        self.assertIn('id="w2-box1"', self.source)

    def test_field_names_source_box_purpose_and_format_before_entry(self) -> None:
        # Criteria 2.1 and 2.2 are checkable against the entry-field.v1
        # declaration (Track 3) rather than against rendered template text:
        # the surface renders {formatSourceLabel()}, {W2_BOX1_FIELD.source.label},
        # and {formatDestinationPurpose()}, all derived from this declaration.
        for text in (
            '"document": "Form W-2"',
            '"box": "Box 1"',
            '"label": "Wages, tips, other compensation"',
            '"form": "Form 1040"',
            '"line": "1a"',
        ):
            self.assertIn(text, self.field_declaration)
        for text in (
            "formatSourceLabel",
            "formatDestinationPurpose",
            "W2_BOX1_FIELD.source.label",
            "formatW2Box1Hint",
        ):
            self.assertIn(text, self.source)
        self.assertIn(
            'import { formatW2Box1Hint } from "./w2-box1-format.js";', self.source
        )
        self.assertIn(
            'import {\n    W2_BOX1_FIELD,\n    formatSourceLabel,\n'
            "    formatDestinationPurpose\n  } from \"./w2-box1-field.js\";",
            self.source,
        )

    def test_accessibility_and_fail_loud_markers_are_present(self) -> None:
        for marker in (
            "<main",
            'aria-label="W-2 Box 1 entry"',
            'role="alert"',
            ":focus-visible",
            "min-height: 44px",
        ):
            self.assertIn(marker, self.source)

    def test_completion_and_correction_remain_reachable(self) -> None:
        self.assertIn("0 missing facts · fully computed", self.source)
        self.assertIn("Correct this fact", self.source)
        self.assertIn("Review W-2 Box 1", self.source)


class DataSafety(unittest.TestCase):
    def test_fixture_and_implementation_are_synthetic_and_locator_free(self) -> None:
        paths = [
            REPO / "packages" / "derivation" / "entry_loop.py",
            REPO / "tools" / "generate_entry_loop_t1_fixtures.py",
            *FIXTURE.rglob("*.json"),
            *FIXTURE.rglob("*.jsonl"),
            *FIXTURE.rglob("*.svelte"),
            *FIXTURE.rglob("*.js"),
            *FIXTURE.rglob("*.mjs"),
        ]
        forbidden = (
            "/Users/",
            "/home/",
            "local-data/",
            "private-archive/",
            "uploads/",
            "generated/user/",
        )
        for path in paths:
            with self.subTest(path=path):
                body = path.read_text("utf-8")
                self.assertFalse(any(marker in body for marker in forbidden))


if __name__ == "__main__":
    unittest.main()
