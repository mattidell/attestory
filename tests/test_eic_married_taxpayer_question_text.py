"""Published Step 3 question 3 keeps every marital clause.

The check reads the question and the fact description. It names no live-lane
token. Losing a clause, or putting the yes list ahead of the no list, fails.
"""
from __future__ import annotations

import json
from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1] / "packages" / "content" / "tax" / "2025"
QUESTION_FILE = CONTENT / "input-question.eic-married-taxpayer.v1.json"
BUNDLE_FILE = CONTENT / "eic-married-taxpayer.bundle.json"
MARRIED = "tax.us.2025.eic.married-taxpayer"

CLAUSES = (
    "never married",
    "widowed before January 1, 2025",
    "final decree",
    "interlocutory decree",
    "spouse died in 2025",
    "spouse died in 2026",
    "nonresident alien",
    "live apart",
    "Rule 3",
)


def require_clauses(text: str) -> None:
    missing = [clause for clause in CLAUSES if clause not in text]
    assert not missing, missing
    assert text.index("Answer no") < text.index("Otherwise answer yes")


def test_question_and_description_keep_every_rule_clause() -> None:
    question = json.loads(QUESTION_FILE.read_text(encoding="utf-8"))["question"]
    facts = json.loads(BUNDLE_FILE.read_text(encoding="utf-8"))["fact_types"]
    title = next(fact["title"] for fact in facts if fact["id"] == MARRIED)
    require_clauses(question)
    require_clauses(title)
