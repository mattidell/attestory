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


class ForemanContextTests(unittest.TestCase):
    def make_repository(self, *, handoff_topic: str = "demo-topic", include_seat: bool = True) -> Path:
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root)
        self.git(root, "init", "-q")
        self.git(root, "config", "user.name", "Demo")
        self.git(root, "config", "user.email", "demo@example.test")
        phase = {
            "version": 1,
            "phase": "Demo Phase",
            "topic": "demo-topic",
            "active_plan": "docs/phases/demo/milestones/demo.md",
            "handoff": "docs/foreman-handoff.md",
        }
        if include_seat:
            phase["seat"] = "docs/prototypes/demo/SEAT.md"
        handoff = {
            "version": 1,
            "topic": handoff_topic,
            "status": "planning only",
            "current_role": "demo reviewer",
            "current_prompt": "docs/reviews/demo-review.md",
        }
        plan = {
            "version": 1,
            "topic": "demo-topic",
            "status": "draft",
            "scope": ["synthetic proof"],
            "non_goals": ["no real workspace"],
            "deep_reads": {
                "dispatch": ["docs/adr/0005.md#Decision"],
                "new_milestone": ["docs/milestone-retrospectives/demo.md"],
            },
        }
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
        self.write_document(root, "docs/foreman-handoff.md", handoff)
        self.write_document(root, "docs/phases/demo/milestones/demo.md", plan)
        self.write_plain(root, "docs/reviews/demo-review.md")
        if include_seat:
            self.write_document(root, "docs/prototypes/demo/SEAT.md", seat)
        self.write_plain(root, "docs/adr/0005.md")
        self.write_plain(root, "docs/milestone-retrospectives/demo.md")
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "seed")
        return root

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

    def test_renders_committed_context_with_source_blobs(self) -> None:
        root = self.make_repository()
        result = self.run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        capsule = json.loads(result.stdout)
        self.assertEqual(capsule["state"]["topic"], "demo-topic")
        self.assertEqual(capsule["state"]["current_role"], "demo reviewer")
        self.assertEqual(capsule["state"]["current_prompt"], "docs/reviews/demo-review.md")
        self.assertFalse(capsule["worktree"]["dirty"])
        self.assertEqual(len(capsule["source"]["documents"]), 5)
        self.assertTrue(all(document["blob"] for document in capsule["source"]["documents"]))

    def test_selected_ref_ignores_newer_commit(self) -> None:
        root = self.make_repository()
        handoff_path = root / "docs/foreman-handoff.md"
        metadata = {
            "version": 1,
            "topic": "demo-topic",
            "status": "newer status",
            "current_role": "newer role",
            "current_prompt": "docs/reviews/newer-review.md",
        }
        self.write_document(root, "docs/foreman-handoff.md", metadata)
        self.write_plain(root, "docs/reviews/newer-review.md")
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "newer")
        result = self.run_tool(root, "HEAD~1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["state"]["handoff_status"], "planning only")
        self.assertEqual(json.loads(result.stdout)["state"]["current_role"], "demo reviewer")
        self.assertNotIn("newer status", result.stdout)
        self.assertTrue(handoff_path.exists())

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
        root = self.make_repository(handoff_topic="wrong-topic")
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
        self.assertEqual(len(capsule["source"]["documents"]), 4)

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

    def test_rejects_missing_current_prompt(self) -> None:
        root = self.make_repository()
        metadata = {
            "version": 1,
            "topic": "demo-topic",
            "status": "planning only",
            "current_role": "demo reviewer",
            "current_prompt": "docs/reviews/missing.md",
        }
        self.write_document(root, "docs/foreman-handoff.md", metadata)
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "missing prompt")
        result = self.run_tool(root)
        self.assertEqual(result.returncode, 2)
        self.assertIn("missing required source docs/reviews/missing.md", result.stderr)


if __name__ == "__main__":
    unittest.main()
