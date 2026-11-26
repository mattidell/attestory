"""The evidence probes' shared question rule reads question links, not punctuation.

question-filter milestone, Decision 1: on presentation-model.v3 a blocked
line's reason is a question when ``resolved.questionRefs[].reasonIndices``
points at it; older models fall back to a question mark in the sentence.
"""

from __future__ import annotations

from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from tests import evidence_loader

REPO = Path(__file__).resolve().parents[1]
BNQ = REPO / "docs/phases/engine-breadth/milestones/blocked-names-question-evidence"

IMPERATIVE = "If box 1g is wrong, enter the correct amount for demo.sale-1."
UNLINKED_ASK = "Did demo.payer-1 report this sale?"
EXPLANATION = "This line waits on demo.line-1."


@pytest.fixture(scope="module")
def links() -> ModuleType:
    return evidence_loader.load(BNQ / "question_links.py", "qf_question_links")


def _resolved(refs: list[dict[str, Any]] | None) -> dict[str, Any]:
    resolved: dict[str, Any] = {
        "disposition": "blocked",
        "reasons": [{"sentence": EXPLANATION}, {"sentence": IMPERATIVE}, {"sentence": UNLINKED_ASK}],
    }
    if refs is not None:
        resolved["questionRefs"] = refs
    return resolved


def test_v3_counts_the_linked_imperative_and_not_the_unlinked_question_mark(links: ModuleType) -> None:
    resolved = _resolved([{"groupId": "question-demo", "reasonIndices": [1], "scopes": [{}]}])
    assert links.asked(resolved, "presentation-model.v3") == [IMPERATIVE]


def test_v3_without_links_asks_nothing(links: ModuleType) -> None:
    assert links.asked(_resolved(None), "presentation-model.v3") == []


def test_pre_v3_falls_back_to_the_question_mark(links: ModuleType) -> None:
    for schema in ("presentation-model.v2", "presentation-model.v1", None):
        assert links.asked(_resolved(None), schema) == [UNLINKED_ASK], schema


def test_clean_is_applied_to_each_question(links: ModuleType) -> None:
    resolved = _resolved([{"groupId": "question-demo", "reasonIndices": [1, 2], "scopes": [{}]}])
    assert links.asked(resolved, "presentation-model.v3", str.upper) == [IMPERATIVE.upper(), UNLINKED_ASK.upper()]
