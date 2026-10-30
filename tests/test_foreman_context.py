from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "foreman_context.py"
FOLLOWUP_TOOL = REPO_ROOT / "tools" / "foreman_context_followup.py"


PLAN = "docs/phases/demo/milestones/demo-topic.md"
RETROSPECTIVE = "docs/milestone-retrospectives/2026-01-01-demo.md"
BRANCH = "milestone/demo-topic-2025"


class ContextFixture(unittest.TestCase):
    """Shared synthetic repository builder; holds no tests of its own.

    `main` is published to a bare origin, then the milestone branch is checked
    out, so the plan is found from the branch name as it is in practice."""

    def plan_metadata(self, **overrides: Any) -> dict[str, Any]:
        plan: dict[str, Any] = {
            "version": 1,
            "phase": "Demo Phase",
            "topic": "demo-topic",
            "status": "draft",
            "scope": ["synthetic proof"],
            "non_goals": ["no real workspace"],
            "deep_reads": {
                "dispatch": ["docs/adr/0005.md#Decision"],
                "new_milestone": [RETROSPECTIVE],
            },
        }
        plan.update(overrides)
        return plan

    def make_repository(
        self,
        *,
        with_origin: bool = True,
        branch: str | None = BRANCH,
        **plan_overrides: Any,
    ) -> Path:
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root)
        self.git(root, "init", "-q", "-b", "main")
        self.git(root, "config", "user.name", "Demo")
        self.git(root, "config", "user.email", "demo@example.test")
        self.write_document(root, PLAN, self.plan_metadata(**plan_overrides))
        self.write_plain(root, "docs/adr/0005.md")
        self.write_plain(root, RETROSPECTIVE)
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "seed")
        if with_origin:
            self.publish_to_origin(root)
        if branch is not None:
            self.git(root, "switch", "-qc", branch)
        return root

    def amend_plan(self, root: Path, message: str, **overrides: Any) -> None:
        text = (root / PLAN).read_text(encoding="utf-8")
        metadata = json.loads(text[text.index("{") : text.index("\n-->")])
        metadata.update(overrides)
        self.write_document(root, PLAN, metadata)
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", message)

    def publish_to_origin(self, root: Path) -> None:
        """Give the fixture a ratified target line for divergence reporting."""
        origin = Path(tempfile.mkdtemp()) / "origin.git"
        self.addCleanup(shutil.rmtree, origin.parent)
        subprocess.run(["git", "init", "--bare", "-q", str(origin)], check=True)
        self.git(root, "remote", "add", "origin", str(origin))
        self.git(root, "push", "-q", "origin", "HEAD:refs/heads/main")
        self.git(root, "fetch", "-q", "origin")

    def git(self, root: Path, *args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(root), *args], check=True, capture_output=True, text=True
        ).stdout.strip()

    def write_document(self, root: Path, relative_path: str, metadata: dict[str, Any]) -> None:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "<!-- foreman-context-v1\n" + json.dumps(metadata) + "\n-->\n# Demo\n",
            encoding="utf-8",
        )

    def write_plain(self, root: Path, relative_path: str) -> None:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Demo\n", encoding="utf-8")

    def run_tool(
        self,
        root: Path,
        ref: str = "HEAD",
        *,
        output_format: str = "json",
        extra: tuple[str, ...] = (),
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(TOOL),
                "--repo",
                str(root),
                "--ref",
                ref,
                "--format",
                output_format,
                "--no-fetch",
                *extra,
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def add_briefing_follow_up(
        self,
        root: Path,
        *,
        blob_override: str | None = None,
    ) -> tuple[str, str]:
        grounding_commit = self.git(root, "rev-parse", "HEAD")
        source_path = "docs/adr/0005.md"
        source_blob = self.git(root, "rev-parse", f"{grounding_commit}:{source_path}")
        follow_up = {
            "version": 1,
            "expires": "milestone-close",
            "grounding_commit": grounding_commit,
            "notes": ["The initial context needed one targeted contract read."],
            "sources": [
                {
                    "path": source_path,
                    "blob": blob_override or source_blob,
                }
            ],
        }
        self.amend_plan(root, "add temporary briefing follow-up", initial_briefing_follow_up=follow_up)
        return grounding_commit, source_blob

    def run_followup_tool(
        self, root: Path, ref: str = "HEAD", *, output_format: str = "json"
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(FOLLOWUP_TOOL),
                "--repo",
                str(root),
                "--ref",
                ref,
                "--format",
                output_format,
                "--no-fetch",
            ],
            check=False,
            capture_output=True,
            text=True,
        )


class ForemanContextTests(ContextFixture):
    def capsule(self, root: Path, ref: str = "HEAD", extra: tuple[str, ...] = ()) -> dict[str, Any]:
        result = self.run_tool(root, ref, extra=extra)
        self.assertEqual(result.returncode, 0, result.stderr)
        capsule: dict[str, Any] = json.loads(result.stdout)
        return capsule

    def test_finds_the_plan_from_the_branch_name(self) -> None:
        capsule = self.capsule(self.make_repository())
        self.assertEqual(capsule["state"]["active_plan"], PLAN)
        self.assertEqual(capsule["state"]["topic"], "demo-topic")
        self.assertEqual(capsule["state"]["phase"], "Demo Phase")
        self.assertFalse(capsule["worktree"]["dirty"])
        paths = [document["path"] for document in capsule["source"]["documents"]]
        self.assertEqual(paths, [PLAN, RETROSPECTIVE])
        self.assertTrue(all(document["blob"] for document in capsule["source"]["documents"]))

    def test_the_longest_matching_key_wins_and_temp_branches_match(self) -> None:
        root = self.make_repository(branch=None)
        self.write_document(root, "docs/phases/demo/milestones/demo.md", self.plan_metadata(topic="demo"))
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "shorter key")
        self.git(root, "switch", "-qc", "temp/milestone/demo-topic-repair")
        self.assertEqual(self.capsule(root)["state"]["active_plan"], PLAN)
        self.git(root, "switch", "-qc", "milestone/demo-other")
        self.assertEqual(
            self.capsule(root)["state"]["active_plan"], "docs/phases/demo/milestones/demo.md"
        )

    def test_a_plan_without_a_phase_field_takes_its_directory(self) -> None:
        root = self.make_repository()
        self.amend_plan(root, "no phase", phase="")
        self.assertEqual(self.capsule(root)["state"]["phase"], "demo")

    def test_no_plan_off_a_milestone_branch(self) -> None:
        capsule = self.capsule(self.make_repository(branch="process/other"))
        self.assertIsNone(capsule["state"])
        self.assertEqual(capsule["milestone"]["state"], "none")
        self.assertEqual(capsule["deep_reads"], {})
        self.assertEqual([d["path"] for d in capsule["source"]["documents"]], [RETROSPECTIVE])

    def test_an_explicit_plan_overrides_the_branch(self) -> None:
        root = self.make_repository(branch="process/other")
        capsule = self.capsule(root, extra=("--plan", PLAN))
        self.assertEqual(capsule["state"]["active_plan"], PLAN)

    def test_selected_ref_ignores_newer_commit(self) -> None:
        root = self.make_repository()
        self.amend_plan(root, "newer", status="newer status")
        capsule = self.capsule(root, "HEAD~1")
        self.assertEqual(capsule["state"]["plan_status"], "draft")
        self.assertNotIn("newer status", json.dumps(capsule))

    def test_dirty_worktree_is_reported_but_not_read(self) -> None:
        root = self.make_repository()
        (root / PLAN).write_text("uncommitted private-looking placeholder\n", encoding="utf-8")
        capsule = self.capsule(root)
        self.assertTrue(capsule["worktree"]["dirty"])
        self.assertIn(PLAN, capsule["worktree"]["dirty_paths"])
        self.assertEqual(capsule["state"]["topic"], "demo-topic")
        self.assertNotIn("private-looking", json.dumps(capsule))

    def test_rejects_malformed_metadata_and_missing_ref(self) -> None:
        root = self.make_repository()
        (root / PLAN).write_text("<!-- foreman-context-v1\nnot-json\n-->\n", encoding="utf-8")
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "malformed")
        malformed = self.run_tool(root)
        self.assertEqual(malformed.returncode, 2)
        self.assertIn("invalid JSON front matter", malformed.stderr)
        missing = self.run_tool(root, "does-not-exist")
        self.assertEqual(missing.returncode, 2)
        self.assertIn("cannot be resolved", missing.stderr)

    def test_rejects_a_missing_deep_read(self) -> None:
        root = self.make_repository()
        self.amend_plan(root, "missing read", deep_reads={"review": ["docs/reviews/missing.md"]})
        result = self.run_tool(root)
        self.assertEqual(result.returncode, 2)
        self.assertIn("missing required source docs/reviews/missing.md", result.stderr)


class MilestoneStateTests(ContextFixture):
    """The selected commit's plan says whether its milestone is open or closed;
    the target line is reported separately as current Git state."""

    def capsule(self, root: Path, ref: str = "HEAD") -> dict[str, Any]:
        result = self.run_tool(root, ref)
        self.assertEqual(result.returncode, 0, result.stderr)
        capsule: dict[str, Any] = json.loads(result.stdout)
        return capsule

    def test_a_plan_without_a_retrospective_is_open(self) -> None:
        milestone = self.capsule(self.make_repository())["milestone"]
        self.assertEqual(milestone["state"], "open")
        self.assertIn("next unfinished track", milestone["next_transition"])
        self.assertIsNotNone(milestone["ratified_ref"])
        self.assertEqual([check["path"] for check in milestone["checks"]], [PLAN])

    def test_a_plan_naming_its_landed_retrospective_is_closed(self) -> None:
        milestone = self.capsule(self.make_repository(retrospective=RETROSPECTIVE))["milestone"]
        self.assertEqual(milestone["state"], "closed")
        self.assertIn("selecting a new milestone", milestone["next_transition"])
        self.assertEqual(milestone["checks"][1]["path"], RETROSPECTIVE)

    def test_a_named_retrospective_must_be_in_the_selected_commit(self) -> None:
        result = self.run_tool(
            self.make_repository(retrospective="docs/milestone-retrospectives/missing.md")
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("absent from the selected commit", result.stderr)

    def test_reports_divergence_from_the_ratified_record(self) -> None:
        root = self.make_repository()
        self.write_plain(root, "docs/reviews/later.md")
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "unpublished work")
        divergence = self.capsule(root)["worktree"]["divergence"]
        self.assertEqual(divergence["ref"], "origin/main")
        self.assertEqual((divergence["behind"], divergence["ahead"]), (0, 1))

    def test_reports_spent_when_non_main_branch_tip_is_already_on_main(self) -> None:
        root = self.make_repository()
        self.write_plain(root, "docs/reviews/topic.md")
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "topic work")
        self.git(root, "switch", "-q", "main")
        self.git(root, "merge", "--no-ff", "-qm", "merge topic", BRANCH)
        self.git(root, "push", "-q", "origin", "main")
        self.git(root, "switch", "-q", BRANCH)
        result = self.run_tool(root, ref="main")
        self.assertEqual(result.returncode, 0, result.stderr)
        worktree = json.loads(result.stdout)["worktree"]
        self.assertEqual(worktree["divergence"]["ahead"], 0)
        self.assertGreater(worktree["divergence"]["behind"], 0)
        self.assertTrue(worktree["branch_tip_reachable_from_ratified"])
        self.assertTrue(worktree["spent"])

    def test_derives_state_without_a_ratified_record(self) -> None:
        milestone = self.capsule(self.make_repository(with_origin=False))["milestone"]
        self.assertEqual(milestone["state"], "open")
        self.assertIsNone(milestone["ratified_ref"])
        self.assertTrue(milestone["checks"])
        self.assertIn("target-line comparison is unavailable", milestone["note"])


class RatifiedLineTests(ContextFixture):
    """The repository carries more than one ratified line — `main` for the
    derivation work, `main-ui` for the surface work — and a milestone that closes
    on one never reaches the other. So the line a capsule corroborates against is
    derived from the checked-out work rather than fixed at `origin/main`."""

    def commit(self, root: Path, name: str) -> None:
        self.write_plain(root, f"docs/reviews/{name}.md")
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", name)

    def make_two_line_repository(self) -> Path:
        """`main` published by the fixture, then `main-ui` branched off it and
        published with a commit of its own."""
        root = self.make_repository()
        self.git(root, "switch", "-qc", "main-ui")
        self.commit(root, "ui-line")
        self.git(root, "push", "-q", "origin", "main-ui")
        self.git(root, "fetch", "-q", "origin")
        return root

    def test_derives_the_surface_line_for_work_cut_from_it(self) -> None:
        root = self.make_two_line_repository()
        self.git(root, "switch", "-qc", "unit")
        self.commit(root, "unit-work")
        capsule = self.capsule(root)
        self.assertEqual(capsule["milestone"]["ratified_line"], "origin/main-ui")
        self.assertEqual(capsule["worktree"]["divergence"]["ref"], "origin/main-ui")

    def test_derives_the_derivation_line_for_work_cut_from_it(self) -> None:
        # Same repository, but this unit branched from `main`. Both lines are one
        # commit away, so the tie falls to the line HEAD is itself closest to.
        root = self.make_two_line_repository()
        self.git(root, "switch", "-q", "main")
        self.git(root, "switch", "-qc", "unit")
        self.commit(root, "unit-work")
        capsule = self.capsule(root)
        self.assertEqual(capsule["milestone"]["ratified_line"], "origin/main")

    def test_an_explicit_ref_overrides_the_derivation(self) -> None:
        root = self.make_two_line_repository()
        result = self.run_tool(root, extra=("--ratified-ref", "origin/main"))
        self.assertEqual(result.returncode, 0, result.stderr)
        capsule = json.loads(result.stdout)
        self.assertEqual(capsule["milestone"]["ratified_line"], "origin/main")

    def capsule(self, root: Path, ref: str = "HEAD") -> dict[str, Any]:
        result = self.run_tool(root, ref)
        self.assertEqual(result.returncode, 0, result.stderr)
        capsule: dict[str, Any] = json.loads(result.stdout)
        return capsule


class InitialBriefingTests(ContextFixture):
    def test_closed_milestone_markdown_stops_before_follow_up_reads(self) -> None:
        root = self.make_repository(retrospective=RETROSPECTIVE)
        result = self.run_tool(root, output_format="markdown")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("## Initial briefing checkpoint", result.stdout)
        self.assertIn("recommend the", result.stdout)
        self.assertIn("smallest useful retrieval, and stop", result.stdout)
        self.assertIn("## Candidate follow-up context", result.stdout)
        self.assertNotIn("## Read in full before acting", result.stdout)

    def test_active_milestone_advertises_and_renders_follow_up(self) -> None:
        root = self.make_repository()
        grounding_commit, source_blob = self.add_briefing_follow_up(root)
        context_result = self.run_tool(root, output_format="markdown")
        self.assertEqual(context_result.returncode, 0, context_result.stderr)
        self.assertIn("Initial briefing follow-up: **available**", context_result.stdout)

        result = self.run_followup_tool(root, output_format="markdown")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Initial briefing follow-up (temporary)", result.stdout)
        self.assertIn("one targeted contract read", result.stdout)
        self.assertIn(grounding_commit, result.stdout)
        self.assertIn(source_blob, result.stdout)

    def test_follow_up_requires_exact_grounding_blob(self) -> None:
        root = self.make_repository()
        self.add_briefing_follow_up(root, blob_override="0" * 40)
        result = self.run_tool(root)
        self.assertEqual(result.returncode, 2)
        self.assertIn("blob mismatch", result.stderr)

    def test_follow_up_loader_refuses_without_a_plan(self) -> None:
        result = self.run_followup_tool(self.make_repository(branch="process/other"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("no milestone plan is active", result.stderr)

    def test_follow_up_loader_refuses_when_no_capsule_is_active(self) -> None:
        root = self.make_repository()
        result = self.run_followup_tool(root)
        self.assertEqual(result.returncode, 2)
        self.assertIn("has no active initial briefing follow-up capsule", result.stderr)

    def test_open_milestone_markdown_lists_reads_to_take(self) -> None:
        result = self.run_tool(self.make_repository(), output_format="markdown")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("## Read in full before acting", result.stdout)
        self.assertIn("`dispatch`: `docs/adr/0005.md#Decision`", result.stdout)

    def test_closed_milestone_must_remove_temporary_follow_up(self) -> None:
        root = self.make_repository(retrospective=RETROSPECTIVE)
        self.add_briefing_follow_up(root)
        result = self.run_tool(root)
        self.assertEqual(result.returncode, 2)
        self.assertIn("closed but still carries", result.stderr)
        self.assertIn("remove the temporary capsule", result.stderr)


if __name__ == "__main__":
    unittest.main()
