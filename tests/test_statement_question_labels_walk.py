"""Statement attribution through the closure question walk (ADR 0089)."""

from __future__ import annotations

from typing import Any

import pytest

from packages.derivation.presentation_projection import (
    _StatementQuestions,
    _answer_explanation_sentences,
    _closure_question_reasons,
)
from packages.kernel.facts import EntityLifecycle, KernelState, fact_id_for
from packages.kernel.findings import FindingState
from packages.tax.loader import labels_statement_questions

KIND = "demo.statement"
SALE = "demo.sale"
ANSWER = "demo.answer"
PAIR = "demo.rule.pair"
NEED = "demo.amount-needed"
SENTENCE = "Enter the demo statement answer."
PLAIN = [{"sentence": SENTENCE}]
BOX7 = "tax.us.2025.f1099b.statement-box7-loss-not-allowed"
EXPLANATION = "You answered no for the demo statement."


def _walk(
    labels: tuple[str, ...], *, answered: tuple[int, ...] = (),
    needs: tuple[str, ...] | None = None, pairing: bool = True,
    extra_cause: bool = False, version: str = "v108",
    answer_type: str = ANSWER, answer_sentences: set[str] | None = None,
) -> list[dict[str, Any]]:
    statements = {f"demo.statement-{n}": EntityLifecycle({"kind": KIND, "label": label}, "current")
                  for n, label in enumerate(labels, 1)}
    keys = [{"kind": "entity", "name": "statement", "entity_kind": KIND},
            {"kind": "literal", "name": "tax-year", "values": ["2025"]}]
    state = FindingState(fact_state=KernelState(
        entities=statements,
        fact_types={name: {"id": name, "version": "v1", "nature": "ordinary", "identity_keys": keys}
                    for name in (SALE, answer_type)},
    ))
    members = [{"schema": "input-question.v1", "fact_type": {"id": answer_type}, "question": SENTENCE}]
    current_answers = set()
    references = []
    pins = []
    by_symbol: dict[str, list[dict[str, Any]]] = {}
    publications = {}
    for index, statement in enumerate(statements):
        identity = (("statement", statement), ("tax-year", "2025"))
        sale_id = fact_id_for(SALE, identity)
        sources = {f"demo.finding-sale-{index}": sale_id}
        answer_id = fact_id_for(answer_type, identity)
        references.append({"targetFactId": answer_id})
        if index in answered:
            finding_id = f"demo.finding-answer-{index}"
            sources[finding_id] = answer_id
            current_answers.add(finding_id)
        for finding_id, fact_id in sources.items():
            state.findings[finding_id] = {"fact_id": fact_id, "value": "no"}
            pins.append({"role": "input", "id": finding_id})
        if needs is not None:
            result_id = f"demo.need-{index}"
            by_symbol[f"{NEED}|{sale_id}"] = [{"disposition": "published", "finding_id": result_id}]
            publications[result_id] = {"value": needs[index]}
    by_symbol["demo.pair"] = [{"disposition": "blocked", "code": "DEPENDENCY_ABSENT",
                               "artifact_id": PAIR, "missing": [answer_type], "pins": pins}]
    line = {"disposition": "blocked", "code": "DEPENDENCY_ABSENT",
            "missing": ["demo.pair", answer_type] if extra_cause else ["demo.pair"]}
    rules = {PAIR: {"value": {"op": "require_paired", "key": "statement",
                              "income": [SALE], "withholding": answer_type}}} if pairing else {}
    questions = None
    if labels_statement_questions("tax.us.2025.package.core-calculations", version):
        questions = _StatementQuestions(
            rules_by_id=rules, state=state, resolved_members=members,
            publications_by_id=publications, by_symbol=by_symbol, entity_kinds=frozenset({KIND}),
            needs={answer_type: frozenset({NEED})} if needs is not None else {},
        )
    explanations = None
    if answer_sentences is not None:
        members.append({"schema": "answer-explanation.v1", "id": "demo.answer-explanation",
                        "fact_type": {"id": answer_type, "version": "v1"},
                        "value": "no", "explanation": EXPLANATION})
        explanations = _answer_explanation_sentences(
            members, state, current_finding_ids=frozenset(current_answers),
        )
        assert explanations[answer_type] == EXPLANATION
    return _closure_question_reasons(
        line, resolved_members=members, by_symbol=by_symbol,
        statement_questions=questions, later_any_arm_refs=True,
        question_refs_by_fact_type={answer_type: references},
        answer_explanations=explanations, answer_sentences_out=answer_sentences,
    )


def _labelled(*labels: str) -> list[dict[str, Any]]:
    return [{"sentence": SENTENCE, "statementLabel": {"statement": label, "taxYear": "2025"}}
            for label in labels]


@pytest.mark.parametrize("labels", [
    ("demo A",),
    ("demo A", "demo B"),
    ("demo A", "demo B", "demo C"),
    ("demo A", "demo A"),
])
def test_each_statement_gets_one_reason(labels: tuple[str, ...]) -> None:
    assert _walk(labels) == _labelled(*labels)


def test_current_answer_covers_only_its_statement() -> None:
    assert _walk(("demo A", "demo B", "demo C"), answered=(0, 2)) == _labelled("demo B")


@pytest.mark.parametrize(("version", "expected"), [
    ("v108", _labelled("demo B")),
    ("v105", PLAIN),
])
def test_box7_answer_explanation_does_not_cross_statements(
    version: str, expected: list[dict[str, Any]],
) -> None:
    explanations: set[str] = set()
    reasons = _walk(("demo A", "demo B"), answered=(0,), version=version,
                    answer_type=BOX7, answer_sentences=explanations)
    assert reasons == expected
    assert explanations == set()


def test_unambiguous_type_question_can_explain_its_current_answer() -> None:
    explanations: set[str] = set()
    reasons = _walk(("demo A",), answered=(0,), version="v105", answer_sentences=explanations)
    assert reasons == PLAIN
    assert explanations == {EXPLANATION}


def test_box4_no_is_filtered_by_published_need() -> None:
    assert _walk(("demo A", "demo B"), needs=("0", "1")) == _labelled("demo B")


@pytest.mark.parametrize("kwargs", [
    {"pairing": False},
    {"answered": (0, 1)},
    {"needs": ("0", "NaN")},
    {"extra_cause": True},
    {"version": "v105"},
])
def test_unattributed_question_keeps_the_original_sentence(kwargs: dict[str, Any]) -> None:
    assert _walk(("demo A", "demo B"), **kwargs) == PLAIN


def test_missing_label_keeps_the_original_sentence() -> None:
    assert _walk(("demo A", "")) == PLAIN
