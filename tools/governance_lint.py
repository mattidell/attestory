"""Structural lint for the governance set under docs/governance/.

Checks the mechanical integrity the closure check specifies: version
headers, article count, citation resolution, constitutional term
resolution against the ontology register, article-principle parentage,
and that no intake draft remains unpromoted under docs/ root.

Doctrine semantics are out of scope; this tool reads structure only.
Exit status: 0 when the set is structurally conformant, 1 otherwise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GOVERNANCE_DIR = REPO_ROOT / "docs" / "governance"
DOCS_DIR = REPO_ROOT / "docs"

ARTIFACTS = (
    "constitution",
    "ontology",
    "engineering-constraints",
    "principles",
    "commentary",
)

EXPECTED_ARTICLE_COUNT = 19
EXPECTED_PRINCIPLE_COUNT = 15

HEADER_FIELDS = ("artifact", "version", "status", "date")

# Constitutional italicized terms that resolve to a register entry under
# a different or inflected name. Aliases are declared, not guessed.
TERM_ALIASES = {
    "adopted": "adoption",
    "claims": "claim",
    "proposals": "proposal",
    "rule artifacts": "rule artifact",
    "derivation edges": "derivation edge",
    "individuation edges": "individuation edge",
}

# Italic spans that are article-local emphasis, not operative terms.
NON_TERMS = {"forecloses"}

_ITALIC = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")
_ARTICLE_HEADING = re.compile(r"^\*\*Article (\d+) — ([^.]+)\.\*\*", re.MULTILINE)
_ARTICLE_CITATION = re.compile(r"Article (\d+)")
_ENG_ENTRY = re.compile(r"^\*\*E(\d+)\.\d+ \(([^)]+)\)", re.MULTILINE)
_PRINCIPLE = re.compile(
    r"^\*\*([IVX]+)\. [^*]+\*\* \*\(→ Art\. ([0-9, ]+)\)\*", re.MULTILINE
)
_REGISTER_ROW = re.compile(r"^\| ([^|]+) \| [^|]+ \| [^|]+ \| [^|]+ \|$", re.MULTILINE)


def read_artifact(name: str) -> str:
    return (GOVERNANCE_DIR / f"{name}.md").read_text(encoding="utf-8")


def check_headers(findings: list[str]) -> None:
    for name in ARTIFACTS:
        path = GOVERNANCE_DIR / f"{name}.md"
        if not path.exists():
            findings.append(f"missing governance artifact: {path.relative_to(REPO_ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            findings.append(f"{name}: missing version header")
            continue
        header = text.split("---", 2)[1]
        for field in HEADER_FIELDS:
            if not re.search(rf"^{field}: \S", header, re.MULTILINE):
                findings.append(f"{name}: header missing field '{field}'")
        declared = re.search(r"^artifact: (\S+)", header, re.MULTILINE)
        if declared and declared.group(1) != name:
            findings.append(
                f"{name}: header declares artifact '{declared.group(1)}'"
            )


def article_names(constitution: str) -> dict[int, str]:
    return {
        int(number): title
        for number, title in _ARTICLE_HEADING.findall(constitution)
    }


def check_articles(constitution: str, findings: list[str]) -> dict[int, str]:
    articles = article_names(constitution)
    if len(articles) != EXPECTED_ARTICLE_COUNT:
        findings.append(
            f"constitution: expected {EXPECTED_ARTICLE_COUNT} articles, found {len(articles)}"
        )
    for cited in _ARTICLE_CITATION.findall(constitution):
        if int(cited) not in articles:
            findings.append(f"constitution: citation to nonexistent Article {cited}")
    return articles


def check_eng_keys(constraints: str, articles: dict[int, str], findings: list[str]) -> None:
    entries = _ENG_ENTRY.findall(constraints)
    if not entries:
        findings.append("engineering-constraints: no E-entries found")
    for number, keyed_name in entries:
        expected = articles.get(int(number))
        if expected is None:
            findings.append(
                f"engineering-constraints: E{number}.x keys to nonexistent Article {number}"
            )
        elif keyed_name != expected:
            findings.append(
                f"engineering-constraints: E{number}.x keyed '{keyed_name}', "
                f"Article {number} is '{expected}'"
            )


def register_entries(ontology: str) -> set[str]:
    entries: set[str] = set()
    for raw in _REGISTER_ROW.findall(ontology):
        name = raw.strip().lower()
        if name in {"entry", "---"}:
            continue
        entries.add(name)
        if " (" in name:
            entries.add(name.split(" (")[0])
    return entries


def constitutional_terms(constitution: str) -> set[str]:
    """Italicized operative terms: short, lowercase spans inside articles."""
    body = constitution.split("## Part I", 1)[-1]
    terms: set[str] = set()
    for span in _ITALIC.findall(body):
        # Sentence-initial terms are capitalized (e.g. "*Evidence* grounds
        # *claims*"); aphorisms and labels are still excluded by the
        # length, charset, and NON_TERMS filters.
        candidate = span.strip().lower()
        if not re.fullmatch(r"[a-z][a-z ]*", candidate):
            continue
        if candidate in NON_TERMS or len(candidate.split()) > 3:
            continue
        terms.add(candidate)
    return terms


def check_term_resolution(
    constitution: str, ontology: str, findings: list[str]
) -> None:
    entries = register_entries(ontology)
    if not entries:
        findings.append("ontology: register table not found or empty")
        return
    for term in sorted(constitutional_terms(constitution)):
        resolved = TERM_ALIASES.get(term, term)
        if resolved in entries:
            continue
        if resolved.endswith("s") and resolved[:-1] in entries:
            continue
        findings.append(
            f"closure: constitutional term '{term}' does not resolve to a register entry"
        )


def check_parentage(principles: str, findings: list[str]) -> None:
    parsed = _PRINCIPLE.findall(principles)
    if len(parsed) != EXPECTED_PRINCIPLE_COUNT:
        findings.append(
            f"principles: expected {EXPECTED_PRINCIPLE_COUNT} principles, found {len(parsed)}"
        )
    claimed: dict[int, str] = {}
    for numeral, articles_list in parsed:
        cited = [int(n) for n in re.findall(r"\d+", articles_list)]
        if not cited:
            findings.append(f"principles: principle {numeral} generates no articles")
        for number in cited:
            if number in claimed:
                findings.append(
                    f"parentage: Article {number} descends from principles "
                    f"{claimed[number]} and {numeral}"
                )
            claimed[number] = numeral
    for number in range(1, EXPECTED_ARTICLE_COUNT + 1):
        if number not in claimed:
            findings.append(f"parentage: Article {number} descends from no principle")


def check_no_intake_drafts(findings: list[str]) -> None:
    for path in DOCS_DIR.glob("INTAKE_*.md"):
        findings.append(
            f"unpromoted intake draft in docs root: {path.relative_to(REPO_ROOT)}"
        )


ALWAYS_LIVE = (
    "AGENTS.md",
    "PROJECT_PLANNING.md",
    "docs/phase-state.md",
)

# "the owner authorized X" in a document still carrying authority. Excludes the
# ADR-0044 trust domain `Owner Authorization`, which is a product term about the
# owner's acts inside the tax system and never about dispatch.
_OWNER_ASSENT = re.compile(
    r"owner-authoriz\w*|\bowner (?:has )?authoriz(?:e|es|ed)\b|authoriz\w+ by the owner",
    re.IGNORECASE,
)
_CODE_SPAN = re.compile(r"`[^`]*`")
_MILESTONE_STATE = re.compile(r'"milestone_state"\s*:\s*"([^"]+)"')
_CURRENT_PROMPT = re.compile(r'"current_prompt"\s*:\s*"([^"#]+)')


def live_authority_documents() -> list[Path]:
    """Documents that still bind. Closed milestone plans and retired or
    superseded ADRs record what was said at the time; they are history, and
    linting them would only pressure agents to rewrite the past."""
    paths = [REPO_ROOT / name for name in ALWAYS_LIVE]
    paths.extend(sorted((REPO_ROOT / "docs" / "roles").glob("*.md")))
    for plan in sorted(DOCS_DIR.glob("phases/*/milestones/*.md")):
        state = _MILESTONE_STATE.search(plan.read_text(encoding="utf-8"))
        if state and state.group(1) != "closed":
            paths.append(plan)
    phase_state = REPO_ROOT / "docs" / "phase-state.md"
    if phase_state.exists():
        # Exactly one charter is current, and phase state is what names it.
        prompt = _CURRENT_PROMPT.search(phase_state.read_text(encoding="utf-8"))
        if prompt:
            charter = REPO_ROOT / prompt.group(1)
            if charter.exists() and charter not in paths:
                paths.append(charter)
    return [path for path in paths if path.exists()]


def check_owner_assent(findings: list[str]) -> None:
    for path in live_authority_documents():
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            # Backticks mark a mention, not a use: the norm has to be able to
            # name the phrase it forbids, and a pointer may cite the AGENTS.md
            # heading, without either one asserting that the owner authorized
            # anything.
            match = _OWNER_ASSENT.search(_CODE_SPAN.sub("", line))
            if match:
                findings.append(
                    f"{path.relative_to(REPO_ROOT)}:{number}: {match.group(0)!r} — "
                    "owner assent is recorded by the merge, not by prose; "
                    "'authorize' is reserved for dispatch "
                    "(PROJECT_PLANNING.md, 'Recording Owner Assent')"
                )


def run() -> list[str]:
    findings: list[str] = []
    check_headers(findings)
    if findings:
        # Header failures may mean artifacts are missing; content checks
        # would only cascade noise.
        missing = [f for f in findings if f.startswith("missing governance artifact")]
        if missing:
            return findings
    constitution = read_artifact("constitution")
    ontology = read_artifact("ontology")
    constraints = read_artifact("engineering-constraints")
    principles = read_artifact("principles")
    articles = check_articles(constitution, findings)
    check_eng_keys(constraints, articles, findings)
    check_term_resolution(constitution, ontology, findings)
    check_parentage(principles, findings)
    check_no_intake_drafts(findings)
    check_owner_assent(findings)
    return findings


def main() -> int:
    findings = run()
    if findings:
        print(f"governance lint: {len(findings)} finding(s)")
        for finding in findings:
            print(f"  - {finding}")
        return 1
    print("governance lint: conformant")
    return 0


if __name__ == "__main__":
    sys.exit(main())
