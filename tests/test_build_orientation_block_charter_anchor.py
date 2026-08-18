"""Regression: `current_prompt`'s own `#anchor` must scope the charter block.

Found on foreman review of the f1098e-student-loan-interest-agi milestone:
`build_block` split `current_prompt` on "#" to get the file path for
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
from tests.test_foreman_context import ContextFixture  # noqa: E402


class CharterAnchorScopingTests(ContextFixture):
    def test_charter_block_is_scoped_to_the_anchor_not_the_whole_file(self) -> None:
        import shutil
        import tempfile

        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root)
        self.git(root, "init", "-q")
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
        plan_path = root / "docs" / "phases" / "demo" / "milestones" / "demo.md"
        plan_path.parent.mkdir(parents=True, exist_ok=True)
        plan_path.write_text(plan_body, encoding="utf-8")

        phase = self.phase_metadata(
            include_seat=False,
            milestone_state="track-1",
            active_plan="docs/phases/demo/milestones/demo.md",
            current_role="Builder (Track 1)",
            current_prompt="docs/phases/demo/milestones/demo.md#Wanted section",
        )
        self.write_document(root, "docs/phase-state.md", phase)

        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "seed padded plan")

        result = subprocess.run(
            [sys.executable, str(TOOL), "--ref", "HEAD", "--role", "builder"],
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
            "-- current_prompt's #anchor is not scoping the read",
        )
        self.assertNotIn("Padding before", out)
        self.assertNotIn("filler line 0", out)
        self.assertNotIn("unrelated trailing content", out)


if __name__ == "__main__":
    import unittest

    unittest.main()
