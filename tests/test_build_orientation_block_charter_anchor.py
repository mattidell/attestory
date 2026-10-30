"""Regression: the charter's own `#anchor` must scope the charter block.

Found on foreman review of the f1098e-student-loan-interest-agi milestone:
`build_block` split the charter pointer on "#" to get the file path for
`blob_for_path`/`content_for_path`, but never passed the anchor fragment to
`extract_section` -- unlike the deep_reads loop just below it, which does.
The charter block therefore always inlined the whole file from byte 0,
capped at `max_bytes`. On a long plan (front matter + prior tracks' settled
prose before the current `## Tracks` heading), the cap can truncate the
actual charter out of the block entirely before it starts.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "build_orientation_block.py"

sys.path.insert(0, str(REPO_ROOT))
from tests.test_foreman_context import PLAN, ContextFixture  # noqa: E402


class CharterAnchorScopingTests(ContextFixture):
    def test_charter_block_is_scoped_to_the_anchor_not_the_whole_file(self) -> None:
        import shutil
        import tempfile

        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root)
        self.git(root, "init", "-q", "-b", "milestone/demo-topic-2025")
        self.git(root, "config", "user.name", "Demo")
        self.git(root, "config", "user.email", "demo@example.test")

        # A long "before" section pads the plan past the default byte cap, so
        # an unscoped read would truncate before ever reaching the wanted
        # section -- reproducing the bug's actual failure mode, not just its
        # shape.
        padding = "\n\n".join(f"filler line {i} " * 20 for i in range(400))
        plan_metadata = {
            "version": 1,
            "topic": "demo-topic",
            "status": "draft",
            "scope": ["prove anchor scoping"],
            "non_goals": ["no real workspace"],
            "deep_reads": {"implementation": []},
        }
        plan_body = (
            "<!-- foreman-context-v1\n"
            + json.dumps(plan_metadata)
            + "\n-->\n"
            "# Demo plan\n\n"
            "## Padding before\n\n"
            f"{padding}\n\n"
            "## Wanted section\n\n"
            "THE ACTUAL CHARTER CONTENT MUST APPEAR IN THE ORIENTATION BLOCK.\n\n"
            "## Padding after\n\n"
            "unrelated trailing content that must not leak into the charter block\n"
        )
        plan_path = root / PLAN
        plan_path.parent.mkdir(parents=True, exist_ok=True)
        plan_path.write_text(plan_body, encoding="utf-8")

        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "seed padded plan")

        result = subprocess.run(
            [sys.executable, str(TOOL), "--ref", "HEAD", "--role", "builder",
             "--charter", f"{PLAN}#Wanted section"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
        out = result.stdout
        self.assertIn(
            "THE ACTUAL CHARTER CONTENT MUST APPEAR IN THE ORIENTATION BLOCK.",
            out,
            "the anchored section was truncated out of the charter block "
            "-- the charter's #anchor is not scoping the read",
        )
        self.assertNotIn("Padding before", out)
        self.assertNotIn("filler line 0", out)
        self.assertNotIn("unrelated trailing content", out)


class ExplicitRoleTests(ContextFixture):
    """Role and clean-room mode are stated by whoever launches the unit; the
    tool no longer infers them from a shared state file."""

    def block(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOL), "--ref", "HEAD", "--charter", "docs/reviews/demo-charter.md", *args],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )

    def repository(self) -> Path:
        root = self.make_repository(deep_reads={"review": ["docs/adr/0005.md"]})
        self.write_plain(root, "docs/reviews/demo-charter.md")
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "charter")
        return root

    def test_requires_a_role_or_action(self) -> None:
        result = self.block(self.repository())
        self.assertEqual(result.returncode, 1)
        self.assertIn("pass --role", result.stderr)

    def test_clean_room_lists_reads_without_inlining_them(self) -> None:
        result = self.block(self.repository(), "--role", "reviewer", "--clean-room")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("CLEAN ROOM", result.stdout)
        self.assertIn("- `docs/adr/0005.md` @ `", result.stdout)
        self.assertNotIn("### read `docs/adr/0005.md`", result.stdout)

    def test_off_a_milestone_branch_the_plan_must_be_named(self) -> None:
        root = self.repository()
        self.git(root, "switch", "-qc", "process/other")
        refused = self.block(root, "--role", "reviewer")
        self.assertEqual(refused.returncode, 1)
        self.assertIn("pass --plan", refused.stderr)
        named = self.block(root, "--role", "reviewer", "--plan", PLAN)
        self.assertEqual(named.returncode, 0, named.stderr)
        self.assertIn("### read `docs/adr/0005.md`", named.stdout)


if __name__ == "__main__":
    import unittest

    unittest.main()
