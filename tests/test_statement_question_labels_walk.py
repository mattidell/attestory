"""Statement attribution through the closure question walk (ADR 0089)."""

from __future__ import annotations

from typing import Any

import pytest

from packages.derivation.presentation_projection import _StatementQuestions, _closure_question_reasons
from packages.kernel.facts import EntityLifecycle, KernelState, fact_id_for
from packages.kernel.findings import FindingState
from packages.tax.loader import labels_statement_questions

KIND = "demo.statement"
SALE = "demo.sale"
ANSWER = "demo.answer"
PAIR = "demo.rule.pair"
NEED = "demo.amount-needed"
SENTENCE = "Enter the demo statement answer."
MEMBERS = [{"schema": "input-question.v1", "fact_type": {"id": ANSWER}, "question": SENTENCE}]
PLAIN = [{"sentence": SENTENCE}]


def _walk(
    labels: tuple[str, ...], *, answered: tuple[int, ...] = (),
    needs: tuple[str, ...] | None = None, pairing: bool = True,
    extra_cause: bool = False, version: str = "v108",
) -> list[dict[str, Any]]:
    statements = {f"demo.statement-{n}": EntityLifecycle({"kind": KIND, "label": label}, "current")
                  for n, label in enumerate(labels, 1)}
    keys = [{"kind": "entity", "name": "statement", "entity_kind": KIND},
            {"kind": "literal", "name": "tax-year", "values": ["2025"]}]
    state = FindingState(fact_state=KernelState(
        entities=statements,
        fact_types={name: {"id": name, "nature": "ordinary", "identity_keys": keys}
                    for name in (SALE, ANSWER)},
    ))
    pins = []
    by_symbol: dict[str, list[dict[str, Any]]] = {}
    publications = {}
    for index, statement in enumerate(statements):
        identity = (("statement", statement), ("tax-year", "2025"))
        sale_id = fact_id_for(SALE, identity)
        sources = {f"demo.finding-sale-{index}": sale_id}
        if index in answered:
            sources[f"demo.finding-answer-{index}"] = fact_id_for(ANSWER, identity)
        for finding_id, fact_id in sources.items():
            state.findings[finding_id] = {"fact_id": fact_id}
            pins.append({"role": "input", "id": finding_id})
        if needs is not None:
            result_id = f"demo.need-{index}"
            by_symbol[f"{NEED}|{sale_id}"] = [{"disposition": "published", "finding_id": result_id}]
            publications[result_id] = {"value": needs[index]}
    by_symbol["demo.pair"] = [{"disposition": "blocked", "code": "DEPENDENCY_ABSENT",
                               "artifact_id": PAIR, "missing": [ANSWER], "pins": pins}]
    line = {"disposition": "blocked", "code": "DEPENDENCY_ABSENT",
            "missing": ["demo.pair", ANSWER] if extra_cause else ["demo.pair"]}
    rules = {PAIR: {"value": {"op": "require_paired", "key": "statement",
                              "income": [SALE], "withholding": ANSWER}}} if pairing else {}
    questions = None
    if labels_statement_questions("tax.us.2025.package.core-calculations", version):
        questions = _StatementQuestions(
            rules_by_id=rules, state=state, resolved_members=MEMBERS,
            publications_by_id=publications, by_symbol=by_symbol, entity_kinds=frozenset({KIND}),
            needs={ANSWER: frozenset({NEED})} if needs is not None else {},
        )
    return _closure_question_reasons(
        line, resolved_members=MEMBERS, by_symbol=by_symbol,
        statement_questions=questions, later_any_arm_refs=True,
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
