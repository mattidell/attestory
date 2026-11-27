"""Display-only payer and broker names on attributed statement questions."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from typing import Any

import pytest

from packages.derivation.presentation_projection import (
    PresentationModelError,
    _StatementQuestions,
    _closure_question_reasons,
    _validate_resolved,
)
from packages.kernel.facts import EntityLifecycle, KernelState, fact_id_for
from packages.kernel.findings import FindingState
from packages.tax.loader import withholding_statement_question_entities

TAX = "tax.us.2025."
CORE = TAX + "package.core-calculations"
LINE = TAX + "rule.form1040-line25b"
BOX4 = TAX + "f1099b.statement-box4-withholding"
BOX7 = TAX + "f1099b.statement-box7-loss-not-allowed"
INT = TAX + "f1099int.box4-withholding"
SSA = TAX + "ssa1099.box6-voluntary-withholding"
ANCHOR = TAX + "f1099b.statement-anchor"
LABEL = "demo Statement"
NAMES = ("demo  Zulu & Sons", "demo Alpha")
SENTENCE = "Enter the demo statement answer."
FIELD = "statementPayerLabel"

FORMS = {
    INT: ("f1099int", ("box1-interest", "box3-interest", "box8-tax-exempt-interest", "box10-market-discount")),
    TAX + "f1099div.box4-withholding": (
        "f1099div", ("box1a-ordinary", "box2a-capital-gain-distribution", "box12-exempt-interest-dividends"),
    ),
    TAX + "f1099r.ira-box4-withholding": ("f1099r", ("ira-box1-taxable-distribution",)),
    TAX + "f1099g.box4-withholding": ("f1099g", ("box1-unemployment",)),
    SSA: ("ssa1099", ("box5-net-benefits",)),
    BOX4: ("f1099b", ("covered-st-txn",)),
    BOX7: ("f1099b", ("covered-st-txn",)),
}


class WalkCase:
    def __init__(self, answer: str, second_label: str = LABEL) -> None:
        self.answer = answer
        form, boxes = FORMS[answer]
        self.income = [TAX + form + "." + box for box in boxes]
        broker = answer in (BOX4, BOX7)
        self.party_key = "broker" if broker else "payer"
        self.entities = ({"statement": "tax.us.f1099b-statement", "broker": "tax.us.f1099b-broker"} if broker
                         else withholding_statement_question_entities(CORE, "v109")[answer])
        self.actors = ("demo.party-a", "demo.party-b")
        self.statements = ("demo.statement-a", "demo.statement-b")
        self.answer_keys = {key: kind for key, kind in self.entities.items() if key != "broker"}
        self.declarations = {name: self.declaration(name, self.entities) for name in self.income}
        self.declarations[answer] = self.declaration(answer, self.answer_keys)
        self.declarations[ANCHOR] = self.declaration(ANCHOR, self.entities)
        self.members: list[dict[str, Any]] = [
            {"schema": "bundle.v1", "fact_types": list(self.declarations.values())},
            {"schema": "input-question.v1", "fact_type": {"id": answer, "version": "v1"}, "question": SENTENCE},
        ]
        entities = {statement: EntityLifecycle({"kind": self.entities["statement"], "label": label}, "current")
                    for statement, label in zip(self.statements, (LABEL, second_label), strict=True)}
        if self.party_key in self.entities:
            entities.update({party: EntityLifecycle({"kind": self.entities[self.party_key], "label": name}, "current")
                             for party, name in zip(self.actors, NAMES, strict=True)})
        self.state = FindingState(fact_state=KernelState(entities=entities, fact_types=self.declarations))
        self.node = {"op": "require_paired", "key": "statement", "income": self.income, "withholding": answer}
        self.rule: dict[str, Any] = {"value": self.node}
        self.row: dict[str, Any] = {
            "disposition": "blocked", "code": "DEPENDENCY_ABSENT", "artifact_id": LINE,
            "missing": [answer], "pins": [],
        }
        self.by_symbol = {"demo.pair": [self.row]}
        self.current: set[str] = set()
        self.source_ids = [self.add(self.income[0], index) for index in range(2)]

    @staticmethod
    def declaration(name: str, entities: Mapping[str, str]) -> dict[str, Any]:
        return {"id": name, "version": "v1", "nature": "ordinary", "identity_keys": [
            *({"kind": "entity", "name": key, "entity_kind": kind} for key, kind in entities.items()),
            {"kind": "literal", "name": "tax-year", "values": ["2025", "2024"]},
        ]}

    def keys(self, index: int, fact_type: str, **changes: str) -> dict[str, str]:
        keys = {"statement": self.statements[index], self.party_key: self.actors[index], "tax-year": "2025"}
        return {key["name"]: changes.get(key["name"], keys[key["name"]])
                for key in self.declarations[fact_type]["identity_keys"]}

    def add(self, fact_type: str, index: int, *, pinned: bool = True,
            keys: dict[str, str] | None = None) -> str:
        identity = self.keys(index, fact_type, **(keys or {}))
        fact_id = fact_id_for(fact_type, tuple(identity.items()))
        fid = f"demo.finding-{len(self.state.findings)}"
        self.state.findings[fid] = {"fact_id": fact_id, "version": "v1", "value": 0}
        self.current.add(fid)
        if pinned:
            self.row["pins"].append({"role": "input", "id": fid, "version": "v1", "origin": "assertion"})
        return fid

    def alter_entity(self, entity_id: str, *, status: str = "current", **changes: Any) -> None:
        original = self.state.fact_state.entities[entity_id]
        self.state.fact_state.entities[entity_id] = EntityLifecycle({**original.entity, **changes}, status)

    def walker(self, *, version: str = "v109", currency: bool = True) -> _StatementQuestions:
        return _StatementQuestions(
            rules_by_id={LINE: self.rule}, state=self.state, resolved_members=self.members, publications_by_id={},
            by_symbol=self.by_symbol, needs={}, entity_kinds=frozenset({"tax.us.f1099b-statement"}),
            withholding_entities=withholding_statement_question_entities(CORE, version),
            current_finding_ids=frozenset(self.current) if currency else None,
        )

    def reasons(self, walker: _StatementQuestions | None = None) -> list[dict[str, Any]]:
        line = {"disposition": "blocked", "code": "DEPENDENCY_ABSENT", "missing": ["demo.pair"]}
        withholding: dict[str, list[dict[str, Any]]] = {}
        reasons = _closure_question_reasons(
            line, resolved_members=self.members, by_symbol=self.by_symbol, later_any_arm_refs=True,
            statement_questions=walker or self.walker(), withholding_reasons_out=withholding,
        )
        return withholding.get(SENTENCE, reasons)


@pytest.mark.parametrize("answer", FORMS)
@pytest.mark.parametrize("peer", ["exact", "answered", "case", "spaces"])
def test_only_exact_current_statement_peers_need_party_names(answer: str, peer: str) -> None:
    second_label = {"case": LABEL.lower(), "spaces": LABEL + " "}.get(peer, LABEL)
    case = WalkCase(answer, second_label)
    if peer == "answered":
        case.add(answer, 1)
    labels = [LABEL] if peer == "answered" else sorted([LABEL, second_label])
    reasons = case.reasons()
    assert [r["statementLabel"]["statement"] for r in reasons] == labels
    expected: list[str | None] = [None] * len(labels)
    if answer != SSA and peer in {"exact", "answered"}:
        expected = list(NAMES[:len(labels)])
    assert [r.get(FIELD) for r in reasons] == expected


@pytest.mark.parametrize("answer", [INT, BOX7])
@pytest.mark.parametrize("fault", [
    "missing-party-name", "blank-party-name", "stale-party", "wrong-party-kind",
    "equal-party-names", "near-party-names", "same-party", "conflicting-party",
    "stale-peer-finding", "different-year", "blank-statement-label", "wrong-statement-kind",
    "missing-pin", "unresolved-pin", "missing-pin-version", "wrong-pin-version", "wrong-pin-origin",
    "stale-pin", "unversioned-question", "successor-identity", "inactive-pairing",
    "missing-year", "wrong-year", "missing-party-key", "missing-statement-key",
])
def test_party_names_fail_closed(answer: str, fault: str) -> None:
    case = WalkCase(answer)
    walker = case.walker(version="v110")
    identity = case.keys(0, answer)
    assert walker.party_label(answer, identity, [case.row]) == NAMES[0]
    first, second = case.actors
    currency = True
    fact_changes: dict[str, Any] = {}
    last_pin = case.row["pins"][-1]
    if fault == "missing-party-name":
        case.alter_entity(second, label=None)
    elif fault == "blank-party-name":
        case.alter_entity(second, label=" \t ")
    elif fault == "stale-party":
        case.alter_entity(second, status="displaced")
    elif fault == "wrong-party-kind":
        case.alter_entity(second, kind="demo.other-party")
    elif fault == "equal-party-names":
        case.alter_entity(second, label=NAMES[0])
    elif fault == "near-party-names":
        case.alter_entity(second, label="  demo zulu & SONS\t")
    elif fault in {"same-party", "conflicting-party"}:
        index = 1 if fault == "same-party" else 0
        substitute = first if fault == "same-party" else second
        case.add(case.income[0], index, keys={case.party_key: substitute})
        if fault == "same-party":
            case.current.remove(case.source_ids[1])
            case.row["pins"].remove(last_pin)
    elif fault == "stale-peer-finding":
        case.state = replace(case.state, retracted_finding_ids=frozenset({case.source_ids[1]}))
        currency = False
    elif fault == "different-year":
        case.current.remove(case.source_ids[1])
        case.row["pins"].remove(last_pin)
        case.add(case.income[0], 1, keys={"tax-year": "2024"})
    elif fault == "blank-statement-label":
        case.alter_entity(case.statements[0], label=" ")
    elif fault == "wrong-statement-kind":
        case.alter_entity(case.statements[1], kind="demo.other-form")
    elif fault == "missing-pin":
        case.row["pins"].remove(last_pin)
    elif fault == "unresolved-pin":
        last_pin["id"] = "demo.missing"
    elif fault == "missing-pin-version":
        del last_pin["version"]
    elif fault == "wrong-pin-version":
        last_pin["version"] = "v2"
    elif fault == "wrong-pin-origin":
        last_pin["origin"] = "derived"
    elif fault == "stale-pin":
        case.current.discard(case.source_ids[0])
    elif fault == "unversioned-question":
        del case.members[1]["fact_type"]["version"]
    elif fault == "successor-identity":
        successor = {**case.declarations[answer], "version": "v2"}
        successor["identity_keys"] = [*successor["identity_keys"], {"kind": "literal", "name": "demo.extra"}]
        case.members[0]["fact_types"].append(successor)
        case.members[1]["fact_type"]["version"] = "v2"
    elif fault == "inactive-pairing":
        case.rule["value"] = {"op": "choose", "when": True, "else": case.node,
                              "then": {"op": "block", "code": "DEPENDENCY_ABSENT", "missing": [answer]}}
    elif fault == "missing-year":
        del identity["tax-year"]
    elif fault == "wrong-year":
        identity["tax-year"] = "2026"
    elif fault == "missing-statement-key":
        del identity["statement"]
    elif fault == "missing-party-key":
        if answer == INT:
            del identity["payer"]
        else:
            fact_changes[case.party_key] = None
    walker = case.walker(version="v110", currency=currency)
    if fact_changes:
        fact_id = case.state.findings[case.source_ids[0]]["fact_id"]
        fact = walker._facts()[fact_id]
        walker._facts()[fact_id] = replace(fact, keys=tuple((k, v) for k, v in fact.keys if k not in fact_changes))
    assert walker.party_label(answer, identity, [case.row]) is None


def test_broker_peer_can_be_recorded_only_by_a_current_statement_anchor() -> None:
    case = WalkCase(BOX7)
    case.row["pins"].pop()
    case.current.remove(case.source_ids[1])
    case.add(ANCHOR, 1, pinned=False)
    assert [r[FIELD] for r in case.reasons()] == [NAMES[0]]
    assert [r.get(FIELD) for r in case.reasons(case.walker(version="v108"))] == [None]


def test_all_sale_findings_contribute_to_broker_agreement_and_must_be_pinned() -> None:
    case = WalkCase(BOX7)
    case.income.append(TAX + "f1099b.covered-lt-txn")
    sale = case.income[-1]
    case.state.fact_state.fact_types[sale] = case.declaration(sale, case.entities)
    case.add(sale, 0)
    identity = case.keys(0, BOX7)
    assert case.walker().party_label(BOX7, identity, [case.row]) == NAMES[0]
    assert case.walker().party_label(BOX7, identity, [{**case.row, "pins": case.row["pins"][:-1]}]) is None
    case.add(sale, 0, keys={"broker": case.actors[1]})
    assert case.walker().party_label(BOX7, identity, [case.row]) is None


@pytest.mark.parametrize("overrides", [
    {FIELD: 5}, {FIELD: "  "}, {"statementLabel": {}},
    {"statementLabel": {"statement": " ", "taxYear": "2025"}},
    {"statementLabel": {"statement": LABEL}}, {"factId": "demo.answer"}, {"memberLabel": "demo Person"},
])
def test_validator_requires_a_display_only_statement_reason(overrides: dict[str, Any]) -> None:
    reason = {"sentence": SENTENCE, FIELD: NAMES[0], "statementLabel": {"statement": LABEL, "taxYear": "2025"}}
    resolved = {"disposition": "blocked", "activeCodes": ["DEPENDENCY_ABSENT"], "act": None, "reasons": [reason]}
    _validate_resolved(resolved, "demo.resolved")
    reason.update(overrides)
    with pytest.raises(PresentationModelError, match=FIELD):
        _validate_resolved(resolved, "demo.resolved")
