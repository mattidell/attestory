"""Track 1 — synthetic W-2 entry loop through the existing product paths."""

from __future__ import annotations

import json
import shutil
import subprocess
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.entry_loop import (
    COMPARISON_LINES,
    EXPECTED_IMPACT_LINES,
    EntryLoopServer,
    SyntheticW2EntryRuntime,
    build_entry_surface,
    load_seed_acts,
    resolve_entry_surface,
)
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.surface_resolver import ResolvedSurface
from packages.kernel.act_log import ActLog
from packages.derivation.loader import DerivationSchemas
from tools.generate_entry_loop_t1_fixtures import (
    CONTENT,
    content_stats,
    render_fixture_files,
    seed_acts,
)


REPO = Path(__file__).resolve().parent.parent
FIXTURE = REPO / "packages" / "sample_data" / "entry_loop_t1"
SOURCE = FIXTURE / "surface" / "content" / "app" / "src" / "EntryPage.svelte"
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
        log = ActLog(self.capability.location, DerivationSchemas().registry)
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
        log = ActLog(self.capability.location, DerivationSchemas().registry)
        added = list(log.read().acts)[-2:]
        self.assertEqual([act["kind"] for act in added], ["contribution", "assertion"])
        finding = added[-1]["payload"]["finding"]
        self.assertEqual(finding["value"], 91000)
        self.assertEqual(
            finding["contribution_id"],
            added[0]["payload"]["contribution"]["id"],
        )

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


class SurfaceCriteria(unittest.TestCase):
    source: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.source = SOURCE.read_text("utf-8")

    def test_missing_item_navigates_directly_to_its_input(self) -> None:
        self.assertIn("Enter this fact", self.source)
        self.assertIn("goToWages", self.source)
        self.assertIn('id="w2-box1"', self.source)

    def test_field_names_source_box_purpose_and_format_before_entry(self) -> None:
        for text in (
            "Form W-2 · Box 1",
            "Wages, tips, other compensation",
            "feeds Form 1040 line 1a",
            "Enter dollars and cents",
        ):
            self.assertIn(text, self.source)

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
