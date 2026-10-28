"""Suite shards fetch refs/heads/main before pytest and fail closed.

The historical parameter test returns without comparing when
``origin/main`` is missing, and it skips when the bytes differ. These
tests reproduce that on a depth-1 checkout and pin the workflow step.
They do not edit that test.
"""

from __future__ import annotations

import importlib.util
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
from types import ModuleType
import pytest

from tools.ci_historical_ref import (
    PARAMETER_PATH,
    REF_SPEC,
    HistoricalRefError,
    fetch_args,
    historical_refspec,
    main,
    prepare,
    run_git,
    verify_historical_parameter,
)

REPO = Path(__file__).resolve().parents[1]
WORKFLOW = REPO / ".github" / "workflows" / "ci.yml"
HISTORICAL_TEST = REPO / "tests" / "test_eic_table_child_columns.py"
ORIGINAL = (
    b'{\n  "schema": "parameter-declaration.v1",\n'
    b'  "id": "tax.us.2025.parameter.eic-table-2025",\n'
    b'  "version": "v1"\n}\n'
)
MUTATED = ORIGINAL.replace(b'"version": "v1"', b'"version": "v9"', 1)
UI = ORIGINAL.replace(b'"version": "v1"', b'"version": "ui"', 1)
_AUTHOR = [
    "-c",
    "user.email=demo@example.com",
    "-c",
    "user.name=demo",
]


def _load(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"could not load {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _git(repo: Path, args: list[str]) -> str:
    result = run_git(repo, args)
    if result.returncode != 0:
        raise AssertionError(result.stderr.decode("utf-8", "replace"))
    return result.stdout.decode("utf-8").strip()


def _commit(repo: Path, message: str) -> None:
    _git(repo, [*_AUTHOR, "add", PARAMETER_PATH])
    _git(repo, [*_AUTHOR, "commit", "-q", "-m", message])


def _init(path: Path) -> None:
    path.mkdir(parents=True)
    _git(path, ["init", "-q", "-b", "main"])


class RefspecTests(unittest.TestCase):
    def test_both_lines_fetch_refs_heads_main(self) -> None:
        events = (
            ("pull_request", "main", "226/merge"),
            ("pull_request", "main-ui", "15/merge"),
            ("push", "", "main"),
            ("push", "", "main-ui"),
        )
        for event_name, base_ref, ref_name in events:
            self.assertEqual(
                historical_refspec(event_name, base_ref, ref_name),
                REF_SPEC,
            )
        args = fetch_args()
        self.assertEqual(args[-1], REF_SPEC)
        self.assertNotIn("--force", args)
        self.assertFalse(any(arg.startswith("+") for arg in args))
        self.assertFalse(any("main-ui" in arg for arg in args))
        self.assertIn("--depth=1", args)

    def test_unaccounted_events_fail_closed(self) -> None:
        with self.assertRaises(HistoricalRefError):
            historical_refspec("pull_request", "", "main")
        with self.assertRaises(HistoricalRefError):
            historical_refspec("pull_request", "226/merge", "main")
        with self.assertRaises(HistoricalRefError):
            historical_refspec("push", "main", "feature")
        with self.assertRaises(HistoricalRefError):
            historical_refspec("workflow_dispatch", "main", "main")


class WorkflowTests(unittest.TestCase):
    def test_each_shard_prepares_the_ref_before_pytest(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("branches: [main, main-ui]", text)
        self.assertIn(
            "\n  verify:\n    needs: [precheck, suite-shard]\n    if: always()\n",
            text,
        )
        self.assertIn("shard: [0, 1, 2, 3]", text)
        self.assertIn("--count 4", text)
        self.assertIn("--shard-count 4", text)
        self.assertEqual(text.count("python3 -m tools.ci_historical_ref prepare"), 1)
        checkout = _load(
            Path(__file__).with_name("test_ci_shard_checkout.py"),
            "ci_shard_checkout_contract",
        )
        jobs = checkout.workflow_jobs(text)
        shard = jobs["suite-shard"]
        self.assertNotIn("fetch-depth:", shard)
        scripts = checkout.run_scripts(shard)
        prepare_script = "python3 -m tools.ci_historical_ref prepare"
        shard_run = next(
            script for script in scripts if "tools.ci_gate run-shard" in script
        )
        self.assertLess(scripts.index(prepare_script), scripts.index(shard_run))
        self.assertLess(
            scripts.index("python3 tools/install_envelope_hooks.py"),
            scripts.index(prepare_script),
        )
        self.assertIn("CI_EVENT_NAME: ${{ github.event_name }}", shard)
        self.assertIn("CI_BASE_REF: ${{ github.base_ref }}", shard)
        self.assertIn("CI_REF_NAME: ${{ github.ref_name }}", shard)
        self.assertIn("CI_BASE_SHA: ${{ github.event.pull_request.base.sha }}", shard)
        self.assertIn("CI_BEFORE_SHA: ${{ github.event.before }}", shard)
        self.assertIn("CI_AFTER_SHA: ${{ github.event.after }}", shard)
        self.assertNotIn("git push", shard)
        self.assertNotIn("--force", scripts[scripts.index(prepare_script)])
        self.assertNotIn("--deselect", shard_run)
        self.assertNotIn("pytest -m", shard_run)


class DepthOneCheckoutTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory()
        self.root = Path(self._temporary.name)

    def tearDown(self) -> None:
        self._temporary.cleanup()

    def _bare_with_branches(self) -> Path:
        bare = self.root / "remote.git"
        work = self.root / "work"
        bare.mkdir()
        _git(bare, ["init", "--bare", "-q"])
        _init(work)
        _git(work, ["remote", "add", "origin", str(bare)])
        destination = work / PARAMETER_PATH
        destination.parent.mkdir(parents=True)
        destination.write_bytes(ORIGINAL)
        _commit(work, "ratified file")
        _git(work, ["push", "-q", "origin", "main"])
        _git(work, ["checkout", "-q", "-b", "pr"])
        destination.write_bytes(MUTATED)
        _commit(work, "pr edit")
        _git(work, ["push", "-q", "origin", "HEAD:refs/heads/pr"])
        _git(work, ["checkout", "-q", "-b", "main-ui", "main"])
        destination.write_bytes(UI)
        _commit(work, "ui file")
        _git(work, ["push", "-q", "origin", "HEAD:refs/heads/main-ui"])
        return bare

    def _shard(self, bare: Path, sha: str) -> Path:
        shard = self.root / f"shard-{sha[:8]}-{len(list(self.root.iterdir()))}"
        _init(shard)
        _git(shard, ["remote", "add", "origin", str(bare)])
        _git(
            shard,
            [
                "-c",
                "protocol.version=2",
                "fetch",
                "--no-tags",
                "--prune",
                "--no-recurse-submodules",
                "--depth=1",
                "origin",
                f"+{sha}:refs/remotes/pull/226/merge",
            ],
        )
        _git(shard, ["checkout", "--force", "refs/remotes/pull/226/merge"])
        target = shard / "tests" / "test_eic_table_child_columns.py"
        target.parent.mkdir(parents=True)
        shutil.copy(HISTORICAL_TEST, target)
        return shard

    def _historical_outcome(self, shard: Path) -> str:
        module = _load(
            shard / "tests" / "test_eic_table_child_columns.py",
            f"historical_probe_{shard.name}",
        )
        try:
            module.TestEICTableV2().test_v1_unchanged_on_disk()
        except module.pytest.skip.Exception:
            return "skip"
        except AssertionError:
            return "fail"
        return "pass"

    def test_parameter_path_is_the_historical_tests_path(self) -> None:
        module = _load(HISTORICAL_TEST, "eic_table_child_columns_contract")
        relative = module.V1_PARAM.relative_to(module.REPO).as_posix()
        self.assertEqual(relative, PARAMETER_PATH)

    def _scenario(self, event: str, changed: bool) -> tuple[Path, dict[str, str], str]:
        index = len(list(self.root.iterdir()))
        bare = self.root / f"remote-{index}.git"
        work = self.root / f"work-{index}"
        bare.mkdir()
        _git(bare, ["init", "--bare", "-q"])
        _init(work)
        _git(work, ["remote", "add", "origin", str(bare)])
        path = work / PARAMETER_PATH
        path.parent.mkdir(parents=True)
        path.write_bytes(ORIGINAL)
        _commit(work, "base")
        base = _git(work, ["rev-parse", "HEAD"])
        _git(work, ["push", "-q", "origin", "main"])
        branch = "main-ui" if event in ("ui", "pr-ui") else "main"
        if branch == "main-ui":
            _git(work, ["checkout", "-q", "-b", branch])
            _git(work, ["push", "-q", "origin", branch])
        if event in ("pr", "pr-ui"):
            _git(work, ["checkout", "-q", "-b", "feature"])
        if changed:
            path.write_bytes(MUTATED)
            _commit(work, "change")
        else:
            _git(work, [*_AUTHOR, "commit", "-q", "--allow-empty", "-m", "unchanged"])
        if event in ("pr", "pr-ui"):
            _git(work, ["checkout", "-q", branch])
            _git(work, [*_AUTHOR, "merge", "--no-ff", "-q", "-m", "merge", "feature"])
            _git(work, ["push", "-q", "origin", "HEAD:refs/heads/test-merge"])
        else:
            _git(work, ["push", "-q", "origin", branch])
        head = _git(work, ["rev-parse", "HEAD"])
        shard = self._shard(bare, head)
        kwargs = ({"event_name": "pull_request", "base_ref": branch,
                   "ref_name": "226/merge", "base_sha": base} if event in ("pr", "pr-ui")
                  else {"event_name": "push", "base_ref": "", "ref_name": branch,
                        "before_sha": base, "after_sha": head})
        return shard, kwargs, base

    def assert_event_baseline(self, event: str, changed: bool) -> None:
        shard, kwargs, baseline = self._scenario(event, changed)
        if changed:
            with self.assertRaises(HistoricalRefError):
                prepare(shard, **kwargs)
            self.assertEqual(self._historical_outcome(shard), "skip")
        else:
            blob = prepare(shard, **kwargs)
            self.assertEqual(_git(shard, ["rev-parse", "origin/main"]), baseline)
            self.assertEqual(_git(shard, ["show", f"origin/main:{PARAMETER_PATH}"]), ORIGINAL.decode().strip())
            self.assertEqual(blob, _git(shard, ["rev-parse", f"{baseline}:{PARAMETER_PATH}"]))
            self.assertEqual(self._historical_outcome(shard), "pass")

    def assert_bad_revision(self, event: str, bad: str) -> None:
        shard, kwargs, _ = self._scenario(event, False)
        key = "base_sha" if event == "pr" else "before_sha"
        kwargs[key] = bad
        with self.assertRaises(HistoricalRefError):
            prepare(shard, **kwargs)

    def test_main_advances_after_push_without_changing_event_baseline(self) -> None:
        shard, kwargs, baseline = self._scenario("main", False)
        remote = _git(shard, ["remote", "get-url", "origin"])
        work = next(self.root.glob("work-*"))
        _git(work, [*_AUTHOR, "commit", "-q", "--allow-empty", "-m", "later"])
        _git(work, ["push", "-q", "origin", "main"])
        prepare(shard, **kwargs)
        self.assertEqual(_git(shard, ["rev-parse", "origin/main"]), baseline)
        self.assertNotEqual(_git(Path(remote), ["rev-parse", "refs/heads/main"]), baseline)

    def test_wrong_checkout_or_pr_base_is_rejected(self) -> None:
        for event in ("pr", "main", "ui"):
            shard, kwargs, _ = self._scenario(event, False)
            if event == "pr":
                kwargs["base_sha"] = _git(shard, ["rev-parse", "HEAD"])
            else:
                kwargs["after_sha"] = "f" * 40
            with self.assertRaises(HistoricalRefError):
                prepare(shard, **kwargs)

    def test_main_moving_during_ui_preparation_fails_closed(self) -> None:
        shard, kwargs, baseline = self._scenario("ui", False)
        with patch("tools.ci_historical_ref._remote_main", side_effect=[baseline, "f" * 40]):
            with self.assertRaises(HistoricalRefError):
                prepare(shard, **kwargs)

    def test_converged_main_moving_during_ui_preparation_fails_closed(self) -> None:
        shard, kwargs, _ = self._scenario("ui", False)
        work = next(self.root.glob("work-*"))
        _git(work, ["push", "-q", "origin", "HEAD:refs/heads/main"])
        head = _git(shard, ["rev-parse", "HEAD"])
        with patch("tools.ci_historical_ref._remote_main", side_effect=[head, "f" * 40]):
            with self.assertRaisesRegex(HistoricalRefError, "main moved"):
                prepare(shard, **kwargs)

    def assert_converged_ui(self, changed: bool) -> None:
        shard, kwargs, before = self._scenario("ui", changed)
        work = next(self.root.glob("work-*"))
        _git(work, ["push", "-q", "origin", "HEAD:refs/heads/main"])
        self.assertEqual(_git(shard, ["rev-parse", "HEAD"]),
                         _git(Path(_git(shard, ["remote", "get-url", "origin"])),
                              ["rev-parse", "refs/heads/main"]))
        if changed:
            with self.assertRaises(HistoricalRefError):
                prepare(shard, **kwargs)
            self.assertEqual(self._historical_outcome(shard), "skip")
        else:
            prepare(shard, **kwargs)
            self.assertEqual(_git(shard, ["rev-parse", "origin/main"]), before)
            self.assertEqual(self._historical_outcome(shard), "pass")

    def test_missing_ref_can_pass_historical_test_but_guard_rejects_change(self) -> None:
        shard, kwargs, _ = self._scenario("main", True)
        self.assertNotEqual(run_git(shard, ["show", f"origin/main:{PARAMETER_PATH}"]).returncode, 0)
        self.assertEqual(self._historical_outcome(shard), "pass")
        with self.assertRaises(HistoricalRefError):
            prepare(shard, **kwargs)

    def test_main_push_does_not_compare_new_tip_to_itself(self) -> None:
        shard, kwargs, baseline = self._scenario("main", True)
        _git(shard, ["update-ref", "refs/remotes/origin/main", "HEAD"])
        self.assertEqual(self._historical_outcome(shard), "pass")
        with self.assertRaises(HistoricalRefError):
            prepare(shard, **kwargs)
        self.assertEqual(_git(shard, ["rev-parse", "origin/main"]), baseline)
        self.assertEqual(self._historical_outcome(shard), "skip")

    def test_missing_historical_file_fails_closed(self) -> None:
        shard, kwargs, baseline = self._scenario("main", False)
        work = next(self.root.glob("work-*"))
        _git(work, [*_AUTHOR, "rm", PARAMETER_PATH])
        _git(work, [*_AUTHOR, "commit", "-q", "-m", "remove"])
        _git(work, ["push", "-q", "origin", "main"])
        removed = _git(work, ["rev-parse", "HEAD"])
        _git(work, [*_AUTHOR, "commit", "-q", "--allow-empty", "-m", "later"])
        _git(work, ["push", "-q", "origin", "main"])
        head = _git(work, ["rev-parse", "HEAD"])
        other = self._shard(Path(_git(shard, ["remote", "get-url", "origin"])), head)
        with self.assertRaises(HistoricalRefError):
            prepare(other, event_name="push", base_ref="", ref_name="main",
                    before_sha=removed, after_sha=head)

    def test_cli_reads_event_revisions(self) -> None:
        shard, kwargs, _ = self._scenario("main", False)
        env = {"CI_EVENT_NAME": kwargs["event_name"], "CI_BASE_REF": "",
               "CI_REF_NAME": kwargs["ref_name"], "CI_BEFORE_SHA": kwargs["before_sha"],
               "CI_AFTER_SHA": kwargs["after_sha"]}
        with patch.dict(os.environ, env, clear=True):
            self.assertEqual(main(["prepare", "--repo", str(shard)]), 0)

    def test_unrelated_existing_ref_is_rejected(self) -> None:
        shard, kwargs, _ = self._scenario("main", False)
        work = next(self.root.glob("work-*"))
        _git(work, ["checkout", "-q", "--orphan", "unrelated"])
        _git(work, [*_AUTHOR, "commit", "-q", "-m", "unrelated"])
        unrelated = _git(work, ["rev-parse", "HEAD"])
        _git(work, ["push", "-q", "origin", "unrelated"])
        _git(shard, ["fetch", "-q", "origin", unrelated])
        _git(shard, ["update-ref", "refs/remotes/origin/main", unrelated])
        with self.assertRaises(HistoricalRefError):
            prepare(shard, **kwargs)
        self.assertEqual(_git(shard, ["rev-parse", "origin/main"]), unrelated)

    def test_main_push_merge_uses_event_before_not_merge_parent(self) -> None:
        shard, kwargs, _ = self._scenario("main", False)
        work = next(self.root.glob("work-*"))
        before = _git(work, ["rev-parse", "HEAD"])
        _git(work, ["checkout", "-q", "-b", "feature"])
        _git(work, [*_AUTHOR, "commit", "-q", "--allow-empty", "-m", "feature"])
        _git(work, ["checkout", "-q", "main"])
        _git(work, [*_AUTHOR, "merge", "--no-ff", "-q", "-m", "merge", "feature"])
        _git(work, ["push", "-q", "origin", "main"])
        head = _git(work, ["rev-parse", "HEAD"])
        merge_shard = self._shard(Path(_git(shard, ["remote", "get-url", "origin"])), head)
        prepare(merge_shard, event_name="push", base_ref="", ref_name="main",
                before_sha=before, after_sha=head)
        self.assertEqual(_git(merge_shard, ["rev-parse", "origin/main"]), before)


@pytest.mark.parametrize("event", ["pr", "pr-ui", "main", "ui"])
@pytest.mark.parametrize("changed", [False, True])
def test_event_baselines(event: str, changed: bool) -> None:
    case = DepthOneCheckoutTests()
    case.setUp()
    try:
        case.assert_event_baseline(event, changed)
    finally:
        case.tearDown()


@pytest.mark.parametrize("changed", [False, True])
def test_converged_main_ui(changed: bool) -> None:
    case = DepthOneCheckoutTests()
    case.setUp()
    try:
        case.assert_converged_ui(changed)
    finally:
        case.tearDown()


@pytest.mark.parametrize("event", ["pr", "main", "ui"])
@pytest.mark.parametrize("bad", ["", "0" * 40, "f" * 40])
def test_bad_revisions(event: str, bad: str) -> None:
    case = DepthOneCheckoutTests()
    case.setUp()
    try:
        case.assert_bad_revision(event, bad)
    finally:
        case.tearDown()


if __name__ == "__main__":
    unittest.main()
