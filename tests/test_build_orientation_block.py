from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools.build_orientation_block import extract_section  # noqa: E402


# Any deep-read target of the form "<path>#<anchor>" that a plan or charter
# may hand to the orientation builder.
ANCHORED_TARGET = re.compile(
    r'"((?:AGENTS\.md|PROJECT_PLANNING\.md|docs/[^"#]+)#[^"]+)"'
)


class ExtractSectionTests(unittest.TestCase):
    def test_atx_heading_runs_to_next_same_or_higher_heading(self) -> None:
        doc = "# Top\nintro\n\n## Wanted\nbody line\n\n## Next\nother\n"
        body, found = extract_section(doc, "Wanted")
        self.assertTrue(found)
        self.assertIn("body line", body)
        self.assertNotIn("other", body)

    def test_bold_lead_paragraph_is_addressable(self) -> None:
        """The governance set writes articles as bold leads, not ATX headings."""
        doc = (
            "## Articles\n\n"
            "**Article 17 — Other.** Unrelated text.\n\n"
            "**Article 18 — Quarantine.** Personal data lives in the workspace.\n\n"
            "**Article 19 — Next.** Also unrelated.\n"
        )
        body, found = extract_section(doc, "Article 18 — Quarantine")
        self.assertTrue(found, "bold-lead article must resolve, not fall back to whole file")
        self.assertIn("Personal data lives", body)
        self.assertNotIn("Article 17", body)
        self.assertNotIn("Article 19", body)

    def test_bold_lead_does_not_truncate_an_enclosing_atx_section(self) -> None:
        doc = (
            "## Shared invariants\n\n"
            "**CI is the gate of record.** Reference the check.\n\n"
            "**Data boundary.** Absolute.\n\n"
            "## Next section\nother\n"
        )
        body, found = extract_section(doc, "Shared invariants")
        self.assertTrue(found)
        self.assertIn("CI is the gate of record", body)
        self.assertIn("Data boundary", body)
        self.assertNotIn("other", body)

    def test_missing_anchor_reports_not_found(self) -> None:
        body, found = extract_section("# Top\nbody\n", "Nope")
        self.assertFalse(found)
        self.assertEqual(body, "")


class RepositoryAnchorTests(unittest.TestCase):
    """Every anchored deep read committed in this repo must resolve.

    A missing anchor does not fail the orientation builder — it degrades to
    inlining the whole file, which silently inflates a scoped read into a
    full-document one. This test is the gate that keeps that from happening
    when a heading is renamed.
    """

    def test_every_committed_deep_read_anchor_resolves(self) -> None:
        unresolved: list[str] = []
        for path in REPO_ROOT.rglob("*.md"):
            if "/archive/" in str(path):
                continue
            for match in ANCHORED_TARGET.finditer(path.read_text(encoding="utf-8")):
                target = match.group(1)
                doc_path, _, anchor = target.partition("#")
                source = (REPO_ROOT / doc_path)
                citer = path.relative_to(REPO_ROOT)
                if not source.exists():
                    unresolved.append(f"{target} (file missing; cited by {citer})")
                    continue
                _, found = extract_section(source.read_text(encoding="utf-8"), anchor)
                if not found:
                    unresolved.append(f"{target} (anchor missing; cited by {citer})")

        self.assertEqual(
            [],
            unresolved,
            "deep-read anchors that would silently expand to a full-file read:\n  "
            + "\n  ".join(unresolved),
        )


if __name__ == "__main__":
    unittest.main()
