"""Mechanical routing checks for standing Reviewer and Foreman instructions."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def _section(document: str, heading: str) -> str:
    marker = f"## {heading}"
    start = document.index(marker)
    remainder = document[start + len(marker) :]
    next_heading = remainder.find("\n## ")
    return remainder if next_heading < 0 else remainder[:next_heading]


class ReviewerGuidanceRoutingCases(unittest.TestCase):
    def test_reviewer_boot_always_routes_qualitative_standard(self) -> None:
        seed = _section(_read("docs/roles/reviewer.md"), "Seed set (read on boot)")
        self.assertIn("docs/roles/qualitative-review.md", seed)
        self.assertTrue((ROOT / "docs/roles/qualitative-review.md").is_file())

    def test_authority_table_names_qualitative_standard(self) -> None:
        authority = _section(_read("AGENTS.md"), "Where authority lives")
        self.assertIn("docs/roles/qualitative-review.md", authority)
        self.assertIn("Reviewer, on boot", authority)


class ForemanPublicationRoutingCases(unittest.TestCase):
    def test_publication_launch_routes_to_controlling_procedure(self) -> None:
        foreman = _read("docs/roles/foreman.md")
        self.assertIn(
            "prepare the current milestone PR for publication",
            foreman,
        )
        self.assertIn("Milestone Publication Curation", foreman)
        self.assertIn("Milestone Closeout", foreman)

    def test_planning_contains_publication_and_semantic_ledger_procedures(self) -> None:
        planning = _read("PROJECT_PLANNING.md")
        publication = _section(planning, "Milestone Publication Curation")
        self.assertIn("Owner-directed semantic ledger", publication)
        self.assertIn("--force-with-lease", publication)
        self.assertIn("local-data/milestone-ledgers/", publication)  # envelope-scan: allow
        self.assertIn("The owner performs the merge", " ".join(publication.split()))


if __name__ == "__main__":
    unittest.main()
