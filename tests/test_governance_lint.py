"""Tests for the governance structural lint.

The positive case is the repository's own governance set: it must lint
clean. The negative cases mutate document text in memory and assert the
relevant check reports the defect — proving the checks are live rather
than vacuously passing.
"""

import unittest

from tools import governance_lint as gl


class TestGovernanceSetIsConformant(unittest.TestCase):
    def test_repository_governance_set_lints_clean(self) -> None:
        findings = gl.run()
        self.assertEqual(findings, [])


class TestHeaderChecks(unittest.TestCase):
    def test_all_artifacts_present_with_headers(self) -> None:
        findings: list[str] = []
        gl.check_headers(findings)
        self.assertEqual(findings, [])


class TestArticleChecks(unittest.TestCase):
    def setUp(self) -> None:
        self.constitution = gl.read_artifact("constitution")

    def test_finds_nineteen_articles(self) -> None:
        self.assertEqual(len(gl.article_names(self.constitution)), 19)

    def test_removed_article_is_reported(self) -> None:
        mutated = self.constitution.replace(
            "**Article 7 — Supersession.**", "**Removed.**"
        )
        findings: list[str] = []
        gl.check_articles(mutated, findings)
        self.assertTrue(any("expected 19 articles" in f for f in findings))

    def test_dangling_citation_is_reported(self) -> None:
        mutated = self.constitution + "\nSee Article 25 for details."
        findings: list[str] = []
        gl.check_articles(mutated, findings)
        self.assertIn(
            "constitution: citation to nonexistent Article 25", findings
        )


class TestEngKeyChecks(unittest.TestCase):
    def test_misnamed_key_is_reported(self) -> None:
        constraints = gl.read_artifact("engineering-constraints")
        articles = gl.article_names(gl.read_artifact("constitution"))
        mutated = constraints.replace("**E1.1 (Peerage)", "**E1.1 (Vocabulary)")
        findings: list[str] = []
        gl.check_eng_keys(mutated, articles, findings)
        self.assertTrue(any("E1.x keyed 'Vocabulary'" in f for f in findings))


class TestTermResolution(unittest.TestCase):
    def setUp(self) -> None:
        self.constitution = gl.read_artifact("constitution")
        self.ontology = gl.read_artifact("ontology")

    def test_operative_terms_are_extracted(self) -> None:
        terms = gl.constitutional_terms(self.constitution)
        # Spot-check terms the closure check traced, including a
        # sentence-initial capitalized one.
        for expected in ("finding", "evidence", "fact type", "derived finding"):
            self.assertIn(expected, terms)
        self.assertNotIn("forecloses", terms)

    def test_unresolvable_term_is_reported(self) -> None:
        mutated = self.constitution.replace("*finding*", "*unregistered thing*")
        findings: list[str] = []
        gl.check_term_resolution(mutated, self.ontology, findings)
        self.assertTrue(
            any("'unregistered thing' does not resolve" in f for f in findings)
        )

    def test_current_set_resolves_completely(self) -> None:
        findings: list[str] = []
        gl.check_term_resolution(self.constitution, self.ontology, findings)
        self.assertEqual(findings, [])


class TestParentage(unittest.TestCase):
    def setUp(self) -> None:
        self.principles = gl.read_artifact("principles")

    def test_fifteen_principles_cover_nineteen_articles_exactly_once(self) -> None:
        findings: list[str] = []
        gl.check_parentage(self.principles, findings)
        self.assertEqual(findings, [])

    def test_orphaned_article_is_reported(self) -> None:
        mutated = self.principles.replace("*(→ Art. 7)*", "*(→ Art. 1)*")
        findings: list[str] = []
        gl.check_parentage(mutated, findings)
        self.assertTrue(
            any("Article 7 descends from no principle" in f for f in findings)
        )
        self.assertTrue(any("Article 1 descends from principles" in f for f in findings))


class TestIntakeDrafts(unittest.TestCase):
    def test_no_intake_drafts_in_docs_root(self) -> None:
        findings: list[str] = []
        gl.check_no_intake_drafts(findings)
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
