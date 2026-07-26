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


class ContextFixture(unittest.TestCase):
    """Shared synthetic repository builder; holds no tests of its own."""

    def phase_metadata(self, *, include_seat: bool = True, **overrides: Any) -> dict[str, Any]:
        """Phase state is the single re-entry document: pointers plus the live
        status/role/prompt that used to live in the separate handoff note."""
        phase: dict[str, Any] = {
            "version": 1,
            "phase": "Demo Phase",
            "topic": "demo-topic",
            "active_plan": "docs/phases/demo/milestones/demo.md",
            "status": "planning only",
            "current_role": "demo reviewer",
            "current_prompt": "docs/reviews/demo-review.md",
        }
        if include_seat:
            phase["seat"] = "docs/prototypes/demo/SEAT.md"
        phase.update(overrides)
        return phase

    def make_repository(
        self,
        *,
        plan_topic: str = "demo-topic",
        include_seat: bool = True,
        with_origin: bool = True,
        **plan_overrides: Any,
    ) -> Path:
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root)
        self.git(root, "init", "-q")
        self.git(root, "config", "user.name", "Demo")
        self.git(root, "config", "user.email", "demo@example.test")
        phase = self.phase_metadata(include_seat=include_seat)
        plan = {
            "version": 1,
            "topic": plan_topic,
            "milestone_state": "track-1",
            "status": "draft",
            "scope": ["synthetic proof"],
            "non_goals": ["no real workspace"],
            "deep_reads": {
                "dispatch": ["docs/adr/0005.md#Decision"],
                "new_milestone": ["docs/milestone-retrospectives/demo.md"],
            },
        }
        plan.update(plan_overrides)
        if include_seat:
            plan["seat"] = "docs/prototypes/demo/SEAT.md"
        seat = {
            "version": 1,
            "topic": "demo-topic",
            "role": "prototype foreman",
            "status": "active",
            "rung": "paper",
            "stop_conditions": ["synthetic evidence only"],
        }
        self.write_document(root, "docs/phase-state.md", phase)
        self.write_document(root, "docs/phases/demo/milestones/demo.md", plan)
        self.write_plain(root, "docs/reviews/demo-review.md")
        if include_seat:
            self.write_document(root, "docs/prototypes/demo/SEAT.md", seat)
        self.write_plain(root, "docs/adr/0005.md")
        self.write_plain(root, "docs/milestone-retrospectives/demo.md")
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "seed")
        if with_origin:
            self.publish_to_origin(root)
        return root

    def publish_to_origin(self, root: Path) -> None:
        """Give the fixture a ratified record. The milestone-state checks ask
        whether the plan and the retrospective are present on `origin/main`, so
        a repository with no origin exercises the uncorroborated path instead."""
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

    def run_tool(self, root: Path, ref: str = "HEAD") -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOL), "--repo", str(root), "--ref", ref],
            check=False,
            capture_output=True,
            text=True,
        )


class ForemanContextTests(ContextFixture):
    def test_renders_committed_context_with_source_blobs(self) -> None:
        root = self.make_repository()
        result = self.run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        capsule = json.loads(result.stdout)
        self.assertEqual(capsule["state"]["topic"], "demo-topic")
        self.assertEqual(capsule["state"]["current_role"], "demo reviewer")
        self.assertEqual(capsule["state"]["current_prompt"], "docs/reviews/demo-review.md")
        self.assertFalse(capsule["worktree"]["dirty"])
        self.assertEqual(len(capsule["source"]["documents"]), 4)
        self.assertTrue(all(document["blob"] for document in capsule["source"]["documents"]))

    def test_selected_ref_ignores_newer_commit(self) -> None:
        root = self.make_repository()
        self.write_document(
            root,
            "docs/phase-state.md",
            self.phase_metadata(
                status="newer status",
                current_role="newer role",
                current_prompt="docs/reviews/newer-review.md",
            ),
        )
        self.write_plain(root, "docs/reviews/newer-review.md")
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "newer")
        result = self.run_tool(root, "HEAD~1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["state"]["status"], "planning only")
        self.assertEqual(json.loads(result.stdout)["state"]["current_role"], "demo reviewer")
        self.assertNotIn("newer status", result.stdout)

    def test_dirty_worktree_is_reported_but_not_read(self) -> None:
        root = self.make_repository()
        phase_path = root / "docs/phase-state.md"
        phase_path.write_text("uncommitted private-looking placeholder\n", encoding="utf-8")
        result = self.run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        capsule = json.loads(result.stdout)
        self.assertTrue(capsule["worktree"]["dirty"])
        self.assertIn("docs/phase-state.md", capsule["worktree"]["dirty_paths"])
        self.assertEqual(capsule["state"]["topic"], "demo-topic")
        self.assertNotIn("private-looking", result.stdout)

    def test_rejects_topic_mismatch(self) -> None:
        root = self.make_repository(plan_topic="wrong-topic")
        result = self.run_tool(root)
        self.assertEqual(result.returncode, 2)
        self.assertIn("topic mismatch", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_renders_nonprototype_context_without_a_seat(self) -> None:
        root = self.make_repository(include_seat=False)
        result = self.run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        capsule = json.loads(result.stdout)
        self.assertIsNone(capsule["state"]["seat"])
        self.assertEqual(len(capsule["source"]["documents"]), 3)

    def test_rejects_malformed_metadata_and_missing_ref(self) -> None:
        root = self.make_repository()
        (root / "docs/phase-state.md").write_text("<!-- foreman-context-v1\nnot-json\n-->\n", encoding="utf-8")
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "malformed")
        malformed = self.run_tool(root)
        self.assertEqual(malformed.returncode, 2)
        self.assertIn("invalid JSON front matter", malformed.stderr)
        missing = self.run_tool(root, "does-not-exist")
        self.assertEqual(missing.returncode, 2)
        self.assertIn("cannot be resolved", missing.stderr)

    def test_current_prompt_may_name_a_section_of_its_file(self) -> None:
        # A plan section can be the charter, so `current_prompt` carries the
        # same `path#Heading` spelling `deep_reads` already accepts. Only the
        # path addresses a blob; resolving the whole string looks to git like a
        # missing file, which sends the reader hunting for one.
        root = self.make_repository()
        self.write_document(
            root,
            "docs/phase-state.md",
            self.phase_metadata(current_prompt="docs/phases/demo/milestones/demo.md#Tracks"),
        )
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "anchored prompt")
        result = self.run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        capsule = json.loads(result.stdout)
        self.assertEqual(
            capsule["state"]["current_prompt"],
            "docs/phases/demo/milestones/demo.md#Tracks",
        )
        paths = [document["path"] for document in capsule["source"]["documents"]]
        self.assertIn("docs/phases/demo/milestones/demo.md", paths)

    def test_rejects_missing_current_prompt(self) -> None:
        root = self.make_repository()
        self.write_document(
            root,
            "docs/phase-state.md",
            self.phase_metadata(current_prompt="docs/reviews/missing.md"),
        )
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "missing prompt")
        result = self.run_tool(root)
        self.assertEqual(result.returncode, 2)
        self.assertIn("missing required source docs/reviews/missing.md", result.stderr)


class MilestoneStateTests(ContextFixture):
    """The lifecycle state a foreman resumes into is declared by the plan and
    corroborated against the ratified record, because the two states that were
    routinely misread — 'the plan PR merged' and 'the closing PR merged' — are
    facts about `origin/main`, not about the document doing the declaring."""

    def capsule(self, root: Path, ref: str = "HEAD") -> dict[str, Any]:
        result = self.run_tool(root, ref)
        self.assertEqual(result.returncode, 0, result.stderr)
        capsule: dict[str, Any] = json.loads(result.stdout)
        return capsule

    def test_reports_a_corroborated_state_and_its_next_transition(self) -> None:
        milestone = self.capsule(self.make_repository())["milestone"]
        self.assertEqual(milestone["state"], "track-1")
        self.assertIn("Track 2 or the closing unit", milestone["next_transition"])
        self.assertIsNotNone(milestone["ratified_ref"])
        self.assertTrue(all(check["expected"] == check["actual"] for check in milestone["checks"]))

    def test_refuses_a_state_the_ratified_record_contradicts(self) -> None:
        # 'planning' claims the plan has not merged, but the fixture published it.
        root = self.make_repository(milestone_state="planning")
        result = self.run_tool(root)
        self.assertEqual(result.returncode, 2)
        self.assertIn("contradicts the ratified record", result.stderr)
        self.assertIn("absent from origin/main", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_refuses_closing_once_the_retrospective_has_landed(self) -> None:
        # A merged retrospective means the closing PR merged: the milestone is
        # closed, not closing. This is the end-boundary case.
        root = self.make_repository(
            milestone_state="closing",
            retrospective="docs/milestone-retrospectives/demo.md",
        )
        result = self.run_tool(root)
        self.assertEqual(result.returncode, 2)
        self.assertIn("contradicts the ratified record", result.stderr)

    def test_accepts_closed_when_the_retrospective_has_landed(self) -> None:
        root = self.make_repository(
            milestone_state="closed",
            retrospective="docs/milestone-retrospectives/demo.md",
        )
        milestone = self.capsule(root)["milestone"]
        self.assertEqual(milestone["state"], "closed")
        self.assertIn("selecting a new milestone", milestone["next_transition"])

    def test_closing_and_closed_require_a_retrospective_path(self) -> None:
        result = self.run_tool(self.make_repository(milestone_state="closed"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("requires a 'retrospective' path", result.stderr)

    def test_rejects_an_unknown_state(self) -> None:
        result = self.run_tool(self.make_repository(milestone_state="mostly done"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("is not one of", result.stderr)
        self.assertIn("track-<n>", result.stderr)

    def test_reports_divergence_from_the_ratified_record(self) -> None:
        root = self.make_repository()
        self.write_plain(root, "docs/reviews/later.md")
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "unpublished work")
        divergence = self.capsule(root)["worktree"]["divergence"]
        self.assertEqual(divergence["ref"], "origin/main")
        self.assertEqual((divergence["behind"], divergence["ahead"]), (0, 1))

    def test_declares_state_uncorroborated_without_a_ratified_record(self) -> None:
        milestone = self.capsule(self.make_repository(with_origin=False))["milestone"]
        self.assertEqual(milestone["state"], "track-1")
        self.assertIsNone(milestone["ratified_ref"])
        self.assertEqual(milestone["checks"], [])
        self.assertIn("NOT corroborated", milestone["note"])


if __name__ == "__main__":
    unittest.main()
