"""Damage the projection inputs read by each route on admitted demo returns."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
from unittest.mock import patch

from probe import ALPHA, CORE, ZULU, build_sales, cases
import scratch
from packages.derivation import live
from tools import recorded_replay as rr


def amended_pin(row, fid, **changes):
    return {**row, "pins": [
        {**pin, **changes} if pin["id"] == fid else pin for pin in row["pins"]
    ]}


def drop_pin(row, fid):
    return {**row, "pins": [pin for pin in row["pins"] if pin["id"] != fid]}


def swap_mapping(items, key, **changes):
    return {**items, key: {**items[key], **changes}}


def replace_member(members, original, **changes):
    return [({**member, **changes} if member is original else member) for member in members]


def check_inputs(walker, traces, questions, other, route):
    original = walker.reasons(traces, questions, other)
    wanted = [ZULU] if route == "pairing" else [ALPHA, ZULU]
    if len(original) != 1 or [entry["saleLabel"] for entry in next(iter(original.values()))] != wanted:
        raise ValueError(f"{route}: expected exact names on authentic projection inputs")

    answer, row, leaf, declaration = traces[0]
    source = scratch.ANSWER_TYPES[answer]
    finding_id = next(
        fid for fid in walker.current[source][next(
            fact_id for fact_id in walker.current[source] if "sale-names.0.sale," in fact_id
        )]
    )
    fact_id = walker.state.findings[finding_id]["fact_id"]
    entity_id = dict(walker.facts[fact_id].keys)["sale"]
    stock = {
        "package": (scratch.PACKAGE, CORE), "state": walker.state, "current_ids": walker.current_ids,
        "members": walker.members, "publications": walker.publications, "by_symbol": walker.by_symbol,
    }
    checked = []

    def control(name, *, expected=None, new_traces=traces, new_questions=questions,
                new_other=other, **changes):
        altered = scratch.SaleQuestions(**{**stock, **changes})
        reached = [trace for trace in new_traces if altered.applies(trace[0])]
        outcome = altered.reasons(reached, new_questions, new_other)
        if outcome != (expected if expected is not None else {}):
            raise ValueError(f"{route}: {name} produced unexpected sale names")
        checked.append(name)

    def trace_control(name, **changes):
        damaged = [
            (ft, changes.get("row", blocked), changes.get("leaf", key), changes.get("declared", declared))
            for ft, blocked, key, declared in traces
        ]
        control(name, new_traces=damaged)

    def changed_entity(**changes):
        fact_state = walker.state.fact_state
        original = fact_state.entities[entity_id]
        entity = changes.pop("entity", original.entity)
        entities = {**fact_state.entities, entity_id: replace(original, entity=entity, **changes)}
        return replace(walker.state, fact_state=replace(fact_state, entities=entities))

    def changed_finding(**changes):
        return replace(walker.state, findings=swap_mapping(walker.state.findings, finding_id, **changes))

    control("older-core-gate", package=(scratch.PACKAGE, "v108"))
    control("wrong-package", package=("demo.other-package", CORE))
    control("absent-current-ids", current_ids=None)
    control("successor-retains-contract", expected=original, package=(scratch.PACKAGE, "v110"))
    control("gone-sale-finding", current_ids=walker.current_ids - {finding_id})
    control("wrong-canonical-year", state=changed_finding(fact_id=fact_id.removesuffix("2025") + "2024"))
    control("duplicate-current-sale-finding", state=replace(
        walker.state, findings={**walker.state.findings, "demo.duplicate-finding": {
            **walker.state.findings[finding_id], "id": "demo.duplicate-finding",
        }},
    ), current_ids=walker.current_ids | {"demo.duplicate-finding"})
    current_entity = walker.state.fact_state.entities[entity_id].entity
    control("displaced-sale-entity", state=changed_entity(status="superseded"))
    control("wrong-entity-kind", state=changed_entity(entity={**current_entity, "kind": "demo.other-kind"}))
    control("blank-target-label", state=changed_entity(entity={**current_entity, "label": " "}))
    control("absent-target-label", state=changed_entity(entity={
        key: value for key, value in current_entity.items() if key != "label"
    }))
    control("technical-label", state=changed_entity(entity={**current_entity, "label": entity_id}))
    control("no-question-sentence", new_questions={})
    control("same-sentence-on-non-sale-leaf", new_other=set(original))
    control("one-unattributed-leaf", new_traces=[*traces, (answer, None, answer, None)])
    trace_control("missing-block-row", row=None)
    trace_control("wrong-block-code", row={**row, "code": "DEMO_WRONG_CODE"})
    trace_control("wrong-block-disposition", row={**row, "disposition": "published"})
    trace_control("wrong-missing-leaf", leaf="demo.other-leaf")

    question = next(m for m in walker.members if m.get("fact_type") == {"id": answer, "version": "v1"}
                    and m.get("schema") == "input-question.v1")
    control("missing-adopted-question", members=[m for m in walker.members if m is not question])
    control("successor-changed-question-pin", package=(scratch.PACKAGE, "v110"),
            members=replace_member(walker.members, question, fact_type={"id": answer, "version": "v2"}))
    for name, ft in (("source", source), ("answer", answer)):
        state = walker.state
        declaration_fact = state.fact_state.fact_types[ft]
        altered_types = {**state.fact_state.fact_types, ft: {
            **declaration_fact, "identity_keys": declaration_fact["identity_keys"][:1],
        }}
        control(f"successor-changed-{name}-identity", package=(scratch.PACKAGE, "v110"),
                state=replace(state, fact_state=replace(state.fact_state, fact_types=altered_types)))

    artifact = row["artifact_id"]
    if route == "pairing":
        rule = walker.rules[artifact]
        control("missing-pairing-rule", members=[m for m in walker.members if m is not rule])
        altered = deepcopy(rule)
        node = scratch._StatementQuestions._paired_nodes(altered, answer)[0]
        node["key"] = "tax-year"
        control("successor-changed-pairing-key", package=(scratch.PACKAGE, "v110"),
                members=[altered if m is rule else m for m in walker.members])
        peer_answer_pin = next(pin["id"] for pin in row["pins"]
                               if walker.state.findings.get(pin["id"], {}).get("fact_id", "").startswith(answer + "|"))
        trace_control("lost-answered-peer-pin", row=drop_pin(row, peer_answer_pin))
        trace_control("lost-sale-pin", row=drop_pin(row, finding_id))
        trace_control("wrong-sale-pin-version", row=amended_pin(row, finding_id, version="v9"))
        trace_control("wrong-sale-pin-origin", row=amended_pin(row, finding_id, origin="derived"))
        trace_control("nonexistent-sale-pin", row=amended_pin(row, finding_id, id="demo.missing-pin"))
    elif route == "amounts-check":
        rule = walker.rules[artifact]
        control("successor-changed-amounts-check", package=(scratch.PACKAGE, "v110"),
                members=replace_member(walker.members, rule, version="v3"))
        producer = walker.rules[artifact.removesuffix(".amounts-check") + ".amounts-agree"]
        control("wrong-subject-declaration", members=replace_member(
            walker.members, producer, subject={"id": "demo.other-subject", "version": "v1"},
        ))
        result_id = next(pin["id"] for pin in row["pins"] if pin.get("origin") == "derived")
        result = walker.publications[result_id]
        symbol = result["symbol"]
        trace_control("lost-derived-result-pin", row=drop_pin(row, result_id))
        trace_control("wrong-derived-pin-version", row=amended_pin(row, result_id, version="v9"))
        trace_control("wrong-derived-pin-origin", row=amended_pin(row, result_id, origin="assertion"))
        control("missing-result-row", by_symbol={**walker.by_symbol, symbol: []})
        control("wrong-result-row-identity", by_symbol={**walker.by_symbol, symbol: [
            {**walker.by_symbol[symbol][0], "finding_id": "demo.other-finding"},
        ]})
        control("bad-amounts-result", publications=swap_mapping(walker.publications, result_id, value="wrong"))
        control("wrong-subject-symbol", publications=swap_mapping(walker.publications, result_id, symbol="demo.wrong"))
        control("missing-derived-result", publications={
            fid: pub for fid, pub in walker.publications.items() if fid != result_id
        })
    else:
        family = source.removesuffix("-txn")
        family_decl = next(m for m in walker.members if m.get("id") == family and "member_predicate" in m)
        control("wrong-family-member", members=replace_member(
            walker.members, family_decl, member_predicate={"fact_type": "demo.other-sale"},
        ))
        trace_control("wrong-fix-question-pin", declared={**declaration, "fact_type": {"id": "demo.wrong"}})
        trace_control("lost-family-code", row={**row, "missing": []})
        result_id, result = next((fid, pub) for fid, pub in walker.publications.items()
                                 if pub["symbol"] == artifact + "." + fact_id)
        control("missing-validation-publication", publications={
            fid: pub for fid, pub in walker.publications.items() if fid != result_id
        })
        control("wrong-validation-member", publications=swap_mapping(walker.publications, result_id, value={
            **result["value"], "member_fact_id": "demo.other-member",
        }))
        control("missing-violation-codes", publications=swap_mapping(walker.publications, result_id, value={
            **result["value"], "violations": [],
        }))
        control("lost-validation-sale-pin", publications={
            **walker.publications, result_id: drop_pin(result, finding_id),
        })
    return checked


def run(route, key):
    seen = []
    method = scratch.SaleQuestions.reasons

    def observe(walker, traces, questions, other):
        traces = list(traces)
        if traces and not seen:
            # Use the live walk's first reached sale-question leaf set. Calling
            # the original method on altered copies exercises only attribution.
            with patch.object(scratch.SaleQuestions, "reasons", method):
                seen.extend(check_inputs(walker, traces, questions, other, route))
        return method(walker, traces, questions, other)

    _, candidate = scratch.projectors()
    with patch.object(scratch.SaleQuestions, "reasons", observe), patch.object(
        live, "build_presentation_model", candidate.build_presentation_model,
    ):
        result = rr.saved_output(CORE, build_sales(cases()[key]), key)
    if not seen or result["outcome"] != "success":
        raise ValueError(f"{route}: controls did not complete: {result.get('message')}")
    return seen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    tests = {
        "pairing": "demo.missing-basis",
        "amounts-check": "demo.amounts-disagree",
        "validation-fix": "demo.two-fixes",
    }
    with ProcessPoolExecutor(max_workers=len(tests)) as pool:
        results = dict(zip(tests, pool.map(run, tests, tests.values()), strict=True))
    summary = {"checked": sum(map(len, results.values())), "controls_by_route": results}
    args.out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
