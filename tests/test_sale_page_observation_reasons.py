"""Fast checks for blocked-reason text the sale page observer expects.

These follow the blocked branch of ``renderLine`` in
``packages/presentation/pages/citation-walk.v1.html``. No browser.
"""
from __future__ import annotations

from typing import Any

from tools.sale_page_observation import (
    _compare_model_and_dom,
    _expected_blocked_reason_texts,
)


LINK = "See the question and affected lines above"
SENTENCE = "Demo sale needs an answer."
GROUP_ID = "demo.question-group.one"
OTHER_GROUP_ID = "demo.question-group.two"


def _group(group_id: str, question: str = SENTENCE) -> dict[str, Any]:
    return {"id": group_id, "question": question}


def _ref(group_id: str, indices: list[int]) -> dict[str, Any]:
    return {
        "groupId": group_id,
        "reasonIndices": indices,
        "scopes": [{"kind": "fact", "id": "demo.fact.one", "status": "stale"}],
    }


def _model(
    reasons: list[dict[str, Any]],
    *,
    schema: str = "presentation-model.v3",
    groups: list[dict[str, Any]] | None = None,
    refs: list[dict[str, Any]] | None = None,
    include_refs: bool = True,
) -> dict[str, Any]:
    resolved: dict[str, Any] = {"disposition": "blocked", "reasons": reasons}
    if include_refs:
        resolved["questionRefs"] = [] if refs is None else refs
    model: dict[str, Any] = {
        "schema": schema,
        "questionGroups": [] if groups is None else groups,
        "sections": [{
            "id": "demo-line",
            "field": {
                "id": "demo.field.line",
                "dispositions": {"blocked": {"explain": "Demo explain."}},
            },
            "resolved": resolved,
        }],
        "attachments": [],
    }
    return model


def _dom(reasons: list[str]) -> dict[str, Any]:
    return {
        "lines": [{
            "id": "demo-line",
            "disposition": "No result",
            "disposition_raw": "blocked",
            "value": "This line has no result.",
            "blocked_reasons": reasons,
        }],
        "attachments": [],
    }


def _reason_outcome(model: dict[str, Any], observed: list[str]) -> tuple[bool, list[str]]:
    differences, checks = _compare_model_and_dom(model, _dom(observed))
    reason_checks = [row for row in checks if row.get("kind") == "blocked-reasons"]
    assert len(reason_checks) == 1
    reason_differences = [
        row for row in differences if row.endswith("model explanation/reasons differ from the rendered DOM")
    ]
    other = [row for row in differences if row not in reason_differences]
    assert other == []
    return bool(reason_checks[0]["matches"]), reason_differences


def test_plain_sentence_matches_and_disagrees_in_both_directions() -> None:
    model = _model([{"sentence": SENTENCE}], include_refs=False)
    assert _expected_blocked_reason_texts(model, model["sections"][0]["resolved"]) == [SENTENCE]
    assert _reason_outcome(model, [SENTENCE]) == (True, [])
    matches, differences = _reason_outcome(model, ["A different demo sentence."])
    assert matches is False and differences
    matches, differences = _reason_outcome(model, [LINK])
    assert matches is False and differences


def test_statement_label_prefix_omits_tax_year() -> None:
    reason = {
        "sentence": SENTENCE,
        "statementLabel": {
            "statement": "Demo statement",
            "lender": "Demo lender",
            "taxYear": "2025",
        },
    }
    model = _model([reason], include_refs=False)
    expected = f"Demo statement, Demo lender: {SENTENCE}"
    assert _expected_blocked_reason_texts(model, model["sections"][0]["resolved"]) == [expected]
    assert _reason_outcome(model, [expected]) == (True, [])
    matches, differences = _reason_outcome(model, [SENTENCE])
    assert matches is False and differences
    matches, differences = _reason_outcome(model, [f"Demo lender, Demo statement: {SENTENCE}"])
    assert matches is False and differences


def test_statement_only_and_lender_only_prefixes() -> None:
    statement_only = _model(
        [{"sentence": SENTENCE, "statementLabel": {"statement": "Demo statement", "lender": ""}}],
        include_refs=False,
    )
    lender_only = _model(
        [{"sentence": SENTENCE, "statementLabel": {"lender": "Demo lender"}}],
        include_refs=False,
    )
    assert _expected_blocked_reason_texts(
        statement_only, statement_only["sections"][0]["resolved"]
    ) == [f"Demo statement: {SENTENCE}"]
    assert _expected_blocked_reason_texts(
        lender_only, lender_only["sections"][0]["resolved"]
    ) == [f"Demo lender: {SENTENCE}"]


def test_member_label_prefix_wins_over_statement_label() -> None:
    reason = {
        "sentence": SENTENCE,
        "memberLabel": "Demo member",
        "statementLabel": {"statement": "Demo statement", "lender": "Demo lender"},
    }
    model = _model([reason], include_refs=False)
    expected = f"Demo member: {SENTENCE}"
    statement_text = f"Demo statement, Demo lender: {SENTENCE}"
    assert _expected_blocked_reason_texts(model, model["sections"][0]["resolved"]) == [expected]
    assert _reason_outcome(model, [expected]) == (True, [])
    matches, differences = _reason_outcome(model, [statement_text])
    assert matches is False and differences

    unlabeled_member = _model(
        [{
            "sentence": SENTENCE,
            "memberLabel": "",
            "statementLabel": {"statement": "Demo statement"},
        }],
        include_refs=False,
    )
    assert _expected_blocked_reason_texts(
        unlabeled_member, unlabeled_member["sections"][0]["resolved"]
    ) == [f"Demo statement: {SENTENCE}"]
    matches, differences = _reason_outcome(unlabeled_member, [f"Demo member: {SENTENCE}"])
    assert matches is False and differences


def test_one_question_group_link_and_raw_sentence_still_differ() -> None:
    model = _model(
        [{"sentence": SENTENCE, "statementLabel": {"statement": "Demo statement"}}],
        groups=[_group(GROUP_ID)],
        refs=[_ref(GROUP_ID, [0])],
    )
    assert _expected_blocked_reason_texts(model, model["sections"][0]["resolved"]) == [LINK]
    assert _reason_outcome(model, [LINK]) == (True, [])
    matches, differences = _reason_outcome(model, [f"Demo statement: {SENTENCE}"])
    assert matches is False and differences
    matches, differences = _reason_outcome(model, [SENTENCE])
    assert matches is False and differences


def test_several_question_groups_join_with_the_page_separator() -> None:
    model = _model(
        [{"sentence": SENTENCE}],
        groups=[_group(GROUP_ID), _group(OTHER_GROUP_ID)],
        refs=[_ref(GROUP_ID, [0]), _ref(OTHER_GROUP_ID, [0])],
    )
    expected = f"{LINK}; {LINK}"
    assert _expected_blocked_reason_texts(model, model["sections"][0]["resolved"]) == [expected]
    assert _reason_outcome(model, [expected]) == (True, [])
    matches, differences = _reason_outcome(model, [LINK])
    assert matches is False and differences


def test_raw_sentence_page_disagrees_when_the_model_names_no_group() -> None:
    """The other direction: a link on the page is not accepted for an unlabeled reason."""
    model = _model(
        [{"sentence": SENTENCE}],
        groups=[_group(GROUP_ID)],
        include_refs=False,
    )
    assert _expected_blocked_reason_texts(model, model["sections"][0]["resolved"]) == [SENTENCE]
    assert _reason_outcome(model, [SENTENCE]) == (True, [])
    matches, differences = _reason_outcome(model, [LINK])
    assert matches is False and differences


def test_member_ordinal_names_which_same_label_member() -> None:
    """ADR 0090: the observer's prefix matches the page's wording for a shared label."""
    model = _model([
        {"sentence": SENTENCE, "memberLabel": "Demo Sam", "memberOrdinal": 2},
        {"sentence": SENTENCE, "memberLabel": "Demo Sam", "memberOrdinal": 11},
        {"sentence": SENTENCE, "memberLabel": "Demo Alex"},
    ], include_refs=False)
    expected = [
        f"Demo Sam (the second one you added with this name): {SENTENCE}",
        f"Demo Sam (the number 11 one you added with this name): {SENTENCE}",
        f"Demo Alex: {SENTENCE}",
    ]
    assert _expected_blocked_reason_texts(model, model["sections"][0]["resolved"]) == expected
    assert _reason_outcome(model, expected) == (True, [])
    matches, differences = _reason_outcome(model, [f"Demo Sam: {SENTENCE}", *expected[1:]])
    assert matches is False and differences


def test_older_schema_keeps_the_sentence_when_refs_are_present() -> None:
    model = _model(
        [{"sentence": SENTENCE, "memberLabel": "Demo member"}],
        schema="presentation-model.v2",
        groups=[_group(GROUP_ID)],
        refs=[_ref(GROUP_ID, [0])],
    )
    expected = f"Demo member: {SENTENCE}"
    assert _expected_blocked_reason_texts(model, model["sections"][0]["resolved"]) == [expected]
    assert _reason_outcome(model, [expected]) == (True, [])
    matches, differences = _reason_outcome(model, [LINK])
    assert matches is False and differences


def test_grouped_and_ungrouped_reasons_on_one_line() -> None:
    other = "Demo second reason."
    model = _model(
        [
            {"sentence": other, "memberLabel": "Demo member"},
            {"sentence": SENTENCE},
        ],
        groups=[_group(GROUP_ID)],
        refs=[_ref(GROUP_ID, [1])],
    )
    expected = [f"Demo member: {other}", LINK]
    assert _expected_blocked_reason_texts(model, model["sections"][0]["resolved"]) == expected
    assert _reason_outcome(model, expected) == (True, [])
    matches, differences = _reason_outcome(model, [f"Demo member: {other}", SENTENCE])
    assert matches is False and differences


def test_malformed_question_ref_does_not_accept_the_link() -> None:
    model = _model(
        [{"sentence": SENTENCE}],
        groups=[_group(GROUP_ID, question="A different demo question.")],
        refs=[_ref(GROUP_ID, [0])],
    )
    assert _expected_blocked_reason_texts(model, model["sections"][0]["resolved"]) == [SENTENCE]
    matches, differences = _reason_outcome(model, [LINK])
    assert matches is False and differences
    assert _reason_outcome(model, []) == (False, [
        "demo-line: model explanation/reasons differ from the rendered DOM",
    ])
