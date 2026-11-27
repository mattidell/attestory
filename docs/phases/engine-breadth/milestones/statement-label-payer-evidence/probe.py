"""Remove or corrupt inputs of the scratch walk using real replayed inputs."""

from __future__ import annotations

from copy import copy, deepcopy
from dataclasses import replace
import json
from unittest.mock import patch

import replay
import scratch
from packages.derivation import live
from tests import evidence_loader
from tools import recorded_replay as rr


def fork(walker, *, mutate_entity=None, remove_findings=(), mutate_fact=None):
    clone = copy(walker)
    vars(clone).pop("_p0_cohorts", None)
    clone._current_finding_ids = walker._current_ids().difference(remove_findings)
    if mutate_entity:
        entity_id, status, fields = mutate_entity
        entities = dict(walker._state.fact_state.entities)
        original = entities[entity_id]
        entities[entity_id] = replace(
            original, status=status, entity={**original.entity, **fields},
        )
        clone._state = replace(walker._state, fact_state=replace(walker._state.fact_state, entities=entities))
    if mutate_fact:
        fact, keys = mutate_fact
        clone._fact_map = dict(walker._facts())
        clone._fact_map[fact.fact_id] = replace(fact, keys=tuple(keys.items()))
    return clone


def probe_inputs(fact_type, walker, identity, rows, expected):
    party_key = "broker" if fact_type == scratch.BOX4 else "payer"
    spec = scratch.B_SPEC if party_key == "broker" else scratch.WITHHOLDING[fact_type]
    year, statement = identity["tax-year"], identity["statement"]
    label = scratch.entity_label(walker, statement, spec[0])
    cohort = scratch.cohort(walker, spec, year, label, party_key)
    party_id, name = cohort[statement]
    assert expected == name
    peer, (peer_party, peer_name) = next((s, p) for s, p in cohort.items() if s != statement)

    records = [
        (finding_id, fact, dict(fact.keys))
        for finding_id in walker._current_ids()
        if (finding := walker._state.findings.get(finding_id))
        and (fact := walker._facts().get(finding["fact_id"])) is not None
        and fact.fact_type_id in spec[2]
    ]
    peer_findings = {fid for fid, _, keys in records if keys.get("statement") == peer}
    assert peer_findings
    peer_fid, peer_fact, peer_keys = next(entry for entry in records if entry[0] in peer_findings)
    other_peer_findings = peer_findings - {peer_fid}
    tests = {
        "disabled_core": (fork(walker), identity, rows),
        "target_year_missing": (walker, {k: v for k, v in identity.items() if k != "tax-year"}, rows),
        "target_year_wrong": (walker, {**identity, "tax-year": "2024"}, rows),
        "target_statement_missing": (walker, {k: v for k, v in identity.items() if k != "statement"}, rows),
        "target_statement_label_blank": (fork(walker, mutate_entity=(statement, "current", {"label": " "})), identity, rows),
        "peer_wrong_statement_kind": (fork(walker, mutate_entity=(peer, "current", {"kind": "demo.other-form"})), identity, rows),
        "peer_superseded": (fork(walker, mutate_entity=(peer, "superseded", {})), identity, rows),
        "peer_different_label": (fork(walker, mutate_entity=(peer, "current", {"label": label.lower()})), identity, rows),
        "peer_findings_noncurrent": (fork(walker, remove_findings=peer_findings), identity, rows),
        "peer_source_wrong_tax_year": (fork(
            walker, remove_findings=other_peer_findings,
            mutate_fact=(peer_fact, {**peer_keys, "tax-year": "2024"}),
        ), identity, rows),
        "same_party_entity": (fork(
            walker, remove_findings=other_peer_findings,
            mutate_fact=(peer_fact, {**peer_keys, party_key: party_id}),
        ), identity, rows),
        "payer_wrong_kind": (fork(walker, mutate_entity=(party_id, "current", {"kind": "demo.other-party"})), identity, rows),
        "payer_missing_label": (fork(walker, mutate_entity=(party_id, "current", {"label": None})), identity, rows),
        "payer_noncurrent": (fork(walker, mutate_entity=(party_id, "superseded", {})), identity, rows),
        "same_display_name": (fork(walker, mutate_entity=(party_id, "current", {"label": peer_name})), identity, rows),
        "near_same_display_name": (fork(walker, mutate_entity=(party_id, "current", {"label": "  " + peer_name.upper()})), identity, rows),
    }
    tests["disabled_core"][0]._p0_enabled = False
    if fact_type == scratch.BOX4:
        matching = {fid for fid, _, keys in records if keys.get("statement") == statement}
        finding_id, fact, keys = next((fid, fact, keys) for fid, fact, keys in records if fid in matching)
        assert any(pin["id"] == finding_id for row in rows for pin in row["pins"])
        tests.update({
            "sale_input_pin_removed": (walker, identity, [
                {**row, "pins": [pin for pin in row["pins"] if pin["id"] not in matching]} for row in rows
            ]),
            "sale_input_pin_unresolved": (walker, identity, [
                {**row, "pins": [dict(pin, id="demo.missing.pin") if pin["id"] == finding_id else pin
                                 for pin in row["pins"]]} for row in rows
            ]),
            "sale_input_finding_noncurrent": (fork(walker, remove_findings=matching), identity, rows),
            "sale_input_broker_key_removed": (fork(
                walker, mutate_fact=(fact, {k: v for k, v in keys.items() if k != "broker"}),
            ), identity, rows),
            "sale_input_broker_key_conflicts": (fork(
                walker, mutate_fact=(fact, {**keys, "broker": peer_party}),
            ), identity, rows),
        })
        anchor = {"fact_id": fact.fact_id, "value": {"broker_name": "demo Different Anchor"}}
        anchored = fork(walker)
        anchored._state = replace(
            walker._state, findings={**walker._state.findings, finding_id: anchor},
        )
        assert scratch.party_label(anchored, fact_type, identity, rows) == name
        pinned = deepcopy(rows[0])
        pinned["code"] = "DEPENDENCY_INVALID"
        assert walker.targets(pinned, fact_type) is None
        without_need_publications = fork(walker)
        without_need_publications._publications = {}
        assert all(without_need_publications.targets(row, fact_type) is None for row in rows)
        tests["publication_input_no_longer_resolves"] = (without_need_publications, identity, rows)
    else:
        tests["answer_identity_payer_removed"] = (walker, {k: v for k, v in identity.items() if k != "payer"}, rows)
        tests["answer_identity_payer_swapped"] = (walker, {**identity, "payer": peer_party}, rows)
        pinned = deepcopy(rows[0])
        pinned["missing"] = ["demo.different.question"]
        assert walker.targets(pinned, fact_type) is None
    without_rule = fork(walker)
    without_rule._rules = {}
    assert all(without_rule.targets(row, fact_type) is None for row in rows)
    for control, (modified, keys, source_rows) in tests.items():
        if scratch.party_label(modified, fact_type, keys, source_rows) is not None:
            raise ValueError(f"{fact_type}: displayed a name after {control}")
    extra = ["box4_need_publications_removed", "nonidentity_sale_value_ignored"] if fact_type == scratch.BOX4 else []
    return ["blocked_row_gate", "attribution_rule_removed", *extra, *sorted(tests)]


def main():
    scratch.check_baseline()
    test = rr._get_test()
    precedent = test.track0().build_scope0_cases()
    base = next(case["acts_v83"] for case in precedent if case["case_id"] == "b4_two_statements")
    cases = replay.synthetic({"v83/track0/s0/b4_two_statements": base})
    if owner := evidence_loader.current_owner():
        evidence_loader.release(owner)
    _, builder = scratch.projectors()
    core = rr.resolve_core(replay.CORE)
    verified = {}
    for key in ("demo.int.duplicate", "demo.box4.duplicate"):
        case = cases[key]

        def instrument(walker, fact_type, identity, rows):
            name = scratch.party_label(walker, fact_type, identity, rows)
            if key not in verified and fact_type == case.question and name is not None:
                verified[key] = probe_inputs(fact_type, walker, identity, rows, name)
            return name

        with patch.dict(builder.__globals__, p0_party_label=instrument):
            with patch.object(live, "build_presentation_model", builder):
                saved = rr.saved_output(core, case.acts, key)
        if saved["outcome"] != "success" or key not in verified:
            raise ValueError(f"{key}: trust controls did not all execute ({saved.get('message')})")
    print(json.dumps(verified, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
