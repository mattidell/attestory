"""Track 10 saved evidence over real live synthetic relationship results."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.kernel.currency import compute_currency
from packages.kernel.facts import facts_of
from packages.kernel.findings import project
from packages.kernel.act_log import ActLog
from packages.derivation.loader import workspace_registry
from packages.kernel.contribution import apply_contribution_batch
from tools.sli_saved_account_evidence import SavedEvidenceError, capture, dumps, loads
from packages.kernel.facts import fact_id_for
from tests.support import act, demo_entity, demo_evidence


ROOT = Path(__file__).resolve().parent.parent
TRACK8 = ROOT / "tests" / "test_sli_track8_relationship_evidence.py"
SCHOOL = "demo.sli.track10.schooling"
FINANCE = "demo.sli.track10.financing"
MEMBERSHIP = "demo.sli.track10.statement-membership"
FINANCE_RESULT = "demo.sli.track10.financing-observation"
FINANCE_RULE = "demo.rule.sli.track10.financing-observation"
MEMBERSHIP_RESULT = "demo.sli.track10.statement-borrowing-observation"
MEMBERSHIP_RULE = "demo.rule.sli.track10.statement-borrowing-observation"
MEMBERSHIP_COUNT = "demo.sli.track10.statement-membership-count"
MEMBERSHIP_COUNT_RULE = "demo.rule.sli.track10.statement-membership-count"


def _track8() -> Any:
    spec = importlib.util.spec_from_file_location("track10_track8_helpers", TRACK8)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _save(name: str, acts: list[dict[str, Any]], surface: Any,
          selected_producers: tuple[str, ...] = (),
          experiment_metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    helper = _track8()
    generator = helper._track6b_generator()
    save_root = ROOT / "temp" / "track10"
    save_root.mkdir(parents=True, exist_ok=True)
    save_path = save_root / f"{name}.saved-account.json"
    with tempfile.TemporaryDirectory(prefix=f"track10-{name}-") as raw:
        authoritative = ActLog(Path(raw) / "authoritative", workspace_registry())
        for act in acts:
            authoritative.append(act, expected_revision=act["committed_against"])
        del authoritative
        reopened_log = ActLog(Path(raw) / "authoritative", workspace_registry())
        recovered_acts = reopened_log.read().acts
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(raw) / "workspace"), repo_root=ROOT,
            authoritative_acts=recovered_acts, workspace_revision=len(recovered_acts),
            run_scope={"jurisdiction": "us", "year": "2025"},
            scope_user=generator.USER, request={"schema": "run-request.v1"},
            run_id=f"demo.track10.{name}", governance_pins=[],
            surface=helper.generator_surface(surface), output_name=f"{name}.json",
        )
        if outcome.refusal is not None or outcome.output_path is None or outcome.publications is None:
            raise AssertionError(f"live account run failed: {outcome.refusal!r}")
        output = json.loads(outcome.output_path.read_text("utf-8"))
        forward, reference = helper._runner_parity(recovered_acts, surface)
        if forward != reference:
            raise AssertionError("forward and reference runners disagree on freshly reopened acts")
        live_publications = sorted(
            [(item.finding["symbol"], item.finding.get("value"), item.finding.get("pins"))
             for item in outcome.publications], key=lambda row: json.dumps(row, sort_keys=True),
        )
        if live_publications != forward["publications"]:
            raise AssertionError("both runners disagree with live publications from recovered acts")
        live_dispositions = [
            (row.get("artifact_id"), row.get("symbol"), row["disposition"], row.get("finding_id"),
             row.get("code"), row.get("missing")) for row in output["dispositions"]
        ]
        live_dispositions.sort(key=lambda row: json.dumps(row, sort_keys=True))
        if live_dispositions != forward["dispositions"]:
            raise AssertionError("both runners disagree with live dispositions from recovered acts")
        schemas = DerivationSchemas()
        state = project(tuple(dict(act) for act in recovered_acts), schemas.registry)
        currency = compute_currency(state)
        lattice = facts_of(state.fact_state)
        current = {key: row for key, row in state.findings.items() if key in currency.current_finding_ids}
        keys = {fact_id: {"fact_type_id": fact.fact_type_id, "bindings": dict(fact.keys),
                          "individuated_by": list(fact.individuated_by)}
                for fact_id, fact in lattice.items()}
        evidence = {key: lifecycle.evidence for key, lifecycle in state.evidence.items()}
        package = next(
            pin for publication in outcome.publications for pin in publication.finding.get("pins", [])
            if pin.get("role") == "adoption"
        )
        saved = capture(
            run_id=outcome.run_id or "", package=package,
            publications=outcome.publications, dispositions=output["dispositions"],
            current_findings=current, fact_keys=keys, evidence_by_id=evidence,
            selected_producer_ids=selected_producers,
            all_findings=state.findings,
            displacement_reasons={finding_id: [{"kind": reason.kind, "by": reason.by}
                                               for reason in reasons]
                                  for finding_id, reasons in currency.reasons.items()},
            lineage_acts=[act for act in recovered_acts if act.get("kind") == "finding-retracted"],
            experiment_metadata=experiment_metadata,
        )
        encoded = dumps(saved)
        del outcome, state, current, lattice, evidence, recovered_acts, reopened_log
    save_path.write_bytes(encoded)
    return loads(save_path.read_bytes())


def _identity_type(type_id: str, title: str, keys: list[dict[str, Any]], values: list[str]) -> dict[str, Any]:
    return {"schema": "fact-type.v2", "id": type_id, "version": "v1", "title": title,
            "nature": "determinable", "identity_keys": keys,
            "value_schema": {"enum": values}, "supersession": {"policy": "free"}}


def _statement_keys() -> list[dict[str, Any]]:
    return [
        {"name": "lender", "kind": "entity", "entity_kind": "tax.us.student-loan-lender"},
        {"name": "statement", "kind": "entity", "entity_kind": "tax.us.1098e-statement"},
        {"name": "tax-year", "kind": "literal", "values": ["2025"]},
    ]


def _answer_finding(
    finding_id: str, fact_type: str, key_pairs: tuple[tuple[str, str], ...], value: str,
    evidence_id: str, contribution_id: str,
) -> dict[str, Any]:
    return {"schema": "finding.v2", "id": finding_id,
            "fact_id": fact_id_for(fact_type, key_pairs), "value": value,
            "basis": "attested", "evidence_ids": [evidence_id], "contribution_id": contribution_id}


def _append_contributed_claim(
    acts: list[dict[str, Any]], registry: Any, finding: dict[str, Any], evidence_id: str,
    contribution_id: str,
) -> None:
    acts.append(act(len(acts), "evidence-submitted", {"evidence": demo_evidence(
        evidence_id, "Synthetic Track 10 ordinary answer", {"claim": finding["value"]}
    )}))
    contribution_act = act(len(acts), "contribution", {"contribution": {
        "schema": "contribution.v1", "id": contribution_id, "evidence_id": evidence_id,
        "content": {"mode": "manual-entry", "synthetic": True},
    }})
    assertion = act(len(acts) + 1, "assertion", {"finding": finding})
    base = project(tuple(dict(row) for row in acts), registry)
    admitted = apply_contribution_batch(base, contribution_act=contribution_act,
                                        successor_acts=[assertion], registry=registry,
                                        record_id=f"demo.contribution-record.{contribution_id}")
    if admitted.terminal_record["phase"] != "completed":
        raise AssertionError(f"test answer failed contribution admission: {admitted.terminal_record}")
    acts.extend((contribution_act, assertion))


def _track10_live_chain(*, equal_pair: bool = True) -> tuple[Any, list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    helper = _track8()
    generator = helper._track6b_generator()
    original_members, original_seal, original_f1098e = (
        generator._package_members, generator._seal_disposable_reader_package, generator._f1098e_acts
    )

    def f1098e_with_s3(**kwargs: Any) -> Any:
        statements = list(kwargs.get("statements") or [])
        statements.append(generator.Statement(
            lender="demo.lender.reader.s3", stmt="demo.statement.reader.s3", box1=125.0, box2=False,
        ))
        kwargs["statements"] = statements
        return original_f1098e(**kwargs)

    school_type = _identity_type(SCHOOL, "Synthetic schooling circumstance", [
        {"name": "situation", "kind": "entity", "entity_kind": "demo.sli-schooling-situation"},
        {"name": "period", "kind": "literal", "values": ["2024", "2025"]},
        {"name": "institution", "kind": "entity", "entity_kind": "demo.sli-schooling-institution"},
        {"name": "programme", "kind": "entity", "entity_kind": "demo.sli-schooling-programme"},
    ], ["demo.schooling.same-observation", "demo.schooling.corrected-observation"])
    finance_type = _identity_type(FINANCE, "Synthetic financing claim", [
        {"name": "borrowing", "kind": "entity", "entity_kind": "demo.sli-borrowing"},
        {"name": "situation", "kind": "entity", "entity_kind": "demo.sli-schooling-situation"},
        {"name": "period", "kind": "literal", "values": ["2024", "2025"]},
        {"name": "institution", "kind": "entity", "entity_kind": "demo.sli-schooling-institution"},
        {"name": "programme", "kind": "entity", "entity_kind": "demo.sli-schooling-programme"},
    ], ["demo.financing.observed"])
    membership_type = _identity_type(MEMBERSHIP, "Synthetic statement-to-borrowing membership claim",
        _statement_keys() + [
            {"name": "borrowing", "kind": "entity", "entity_kind": "demo.sli-borrowing"},
        ], ["demo.membership.observed"])
    status_type = _identity_type(FINANCE_RESULT, "Neutral financing observation", finance_type["identity_keys"],
        ["demo.schooling.same-observation", "demo.schooling.corrected-observation"])
    membership_result_type = _identity_type(MEMBERSHIP_RESULT, "Neutral statement-borrowing observation",
        membership_type["identity_keys"], ["false", "true"])
    count_type = _identity_type(MEMBERSHIP_COUNT, "Neutral statement membership count",
        _statement_keys(), ["0", "1", "2", "3"])
    bundle_types = [school_type, finance_type, membership_type, status_type, membership_result_type, count_type]

    finance_rule = generator._reader_rule(
        FINANCE_RULE, FINANCE_RESULT, subject=FINANCE, requires=[SCHOOL],
        joined=SCHOOL, direction="subject_contains_joined",
        value={"op": "ref", "name": SCHOOL},
    )
    membership_rule = generator._reader_rule(
        MEMBERSHIP_RULE, MEMBERSHIP_RESULT, subject=MEMBERSHIP, requires=[FINANCE_RESULT],
        value={"op": "collect_categorical_all_equal", "name": FINANCE_RESULT,
              "value": {"op": "category_literal", "fact_type": {"id": FINANCE_RESULT, "version": "v1"},
                        "value": "demo.schooling.same-observation"}},
    )
    count_rule = generator._reader_rule(
        MEMBERSHIP_COUNT_RULE, MEMBERSHIP_COUNT, subject=generator.BOX1, joined=MEMBERSHIP_RESULT,
        direction="joined_contains_subject", requires=[MEMBERSHIP_RESULT],
        value={"op": "link_count", "links": MEMBERSHIP_RESULT},
    )
    def extended_members() -> tuple[list[tuple[dict[str, Any], str]], list[dict[str, str]]]:
        members, entrypoints = original_members()
        for index, (citizen, _) in enumerate(members):
            if citizen.get("id") == generator.CLAIM_BUNDLE:
                citizen = dict(citizen)
                citizen["fact_types"] = list(citizen["fact_types"]) + bundle_types
                members[index] = (citizen, "fact-type-bundle")
                break
        additions = [(finance_rule, "computation"), (membership_rule, "computation"), (count_rule, "computation")]
        members.extend(additions)
        entrypoints.extend({"id": citizen["id"], "version": citizen["version"]}
                           for citizen, _ in additions)
        return members, entrypoints

    def seal_with_track10(surface: Any) -> Any:
        path = surface.members / generator.PACKAGE_FILE
        package = json.loads(path.read_text("utf-8"))
        for symbol in (SCHOOL, FINANCE, MEMBERSHIP):
            package["input_bindings"].append({
                "symbol": symbol, "fact_type": {"id": symbol, "version": "v1"}, "mode": "required",
            })
        path.write_bytes(generator._bytes(package))
        return original_seal(surface)

    generator._package_members = extended_members
    generator._seal_disposable_reader_package = seal_with_track10
    generator._f1098e_acts = f1098e_with_s3
    try:
        surface, _members, _before, acts, _retracted = helper._prototype_relationship_acts(generator)
    finally:
        generator._package_members, generator._seal_disposable_reader_package, generator._f1098e_acts = (
            original_members, original_seal, original_f1098e
        )

    # Add three independently recorded relationship claims: two borrowings
    # share one schooling situation; a third path uses a distinct, equal-valued
    # schooling situation for borrowing A.
    situation_shared, situation_independent = "demo.sli.schooling.shared", "demo.sli.schooling.independent"
    situation_details = {
        situation_shared: ("2024", "demo.sli.schooling.institution.shared", "demo.sli.schooling.programme.shared"),
        situation_independent: ("2025", "demo.sli.schooling.institution.independent", "demo.sli.schooling.programme.independent"),
    }
    for situation, label in ((situation_shared, "Synthetic shared schooling situation"),
                             (situation_independent, "Synthetic independent schooling situation")):
        acts.append(act(len(acts), "entity-introduced", {"entity": demo_entity(
            situation, label, "demo.sli-schooling-situation")}))
        _period, institution, programme = situation_details[situation]
        acts.append(act(len(acts), "entity-introduced", {"entity": demo_entity(
            institution, "Synthetic schooling institution", "demo.sli-schooling-institution")}))
        acts.append(act(len(acts), "entity-introduced", {"entity": demo_entity(
            programme, "Synthetic schooling programme", "demo.sli-schooling-programme")}))
    # The extended answer bundle is already present in the package's ordinary
    # acts. Use an explicitly named fact type from it during real admission.
    registry = DerivationSchemas().registry
    shared_keys = (("situation", situation_shared), ("period", "2024"),
                   ("institution", situation_details[situation_shared][1]),
                   ("programme", situation_details[situation_shared][2]))
    independent_keys = (("situation", situation_independent), ("period", "2025"),
                        ("institution", situation_details[situation_independent][1]),
                        ("programme", situation_details[situation_independent][2]))
    school_shared = _answer_finding("demo.finding.track10.school.shared", SCHOOL, shared_keys,
                                    "demo.schooling.same-observation", "demo.evidence.track10.school.shared",
                                    "demo.contribution.track10.school.shared")
    school_independent = _answer_finding("demo.finding.track10.school.independent", SCHOOL, independent_keys,
                                         "demo.schooling.same-observation", "demo.evidence.track10.school.independent",
                                         "demo.contribution.track10.school.independent")
    for finding in (school_shared, school_independent):
        _append_contributed_claim(acts, registry, finding, finding["evidence_ids"][0], finding["contribution_id"])

    statements = {
        "s1": ("demo.lender.reader.s1", "demo.statement.reader.s1"),
        "s2": ("demo.lender.reader.s2", "demo.statement.reader.s2"),
    }
    # An independently addressed third statement and borrowing isolate the
    # comparison path while two statement paths share one schooling claim.
    lender_c, statement_c = "demo.lender.reader.s3", "demo.statement.reader.s3"
    borrowing_c = "demo.track10.borrowing.c"
    acts.append(act(len(acts), "entity-introduced", {"entity": demo_entity(
        borrowing_c, "Synthetic borrowing C", "demo.sli-borrowing")}))
    finance_rows = [
        ("demo.track8.borrowing.a", situation_shared),
        ("demo.track8.borrowing.b", situation_shared),
        (borrowing_c, situation_independent),
    ]
    if equal_pair:
        finance_rows.insert(1, ("demo.track8.borrowing.a", situation_independent))
        finance_rows.append(("demo.track8.borrowing.b", situation_independent))
    for index, (borrowing, situation) in enumerate(finance_rows):
        period, institution, programme = situation_details[situation]
        finance_keys = (("borrowing", borrowing), ("situation", situation), ("period", period),
                        ("institution", institution), ("programme", programme))
        finance_finding = _answer_finding(
            f"demo.finding.track10.financing.{index}", FINANCE, finance_keys,
            "demo.financing.observed", f"demo.evidence.track10.financing.{index}",
            f"demo.contribution.track10.financing.{index}",
        )
        _append_contributed_claim(acts, registry, finance_finding,
                                  finance_finding["evidence_ids"][0], finance_finding["contribution_id"])
    membership_rows = [
        ("s1", "demo.track8.borrowing.a"),
        ("s2", "demo.track8.borrowing.b"),
        ("s3", borrowing_c),
    ]
    for index, (label, borrowing) in enumerate(membership_rows):
        lender, statement = statements.get(label, (lender_c, statement_c))
        membership_keys = (("lender", lender), ("statement", statement), ("tax-year", "2025"),
                           ("borrowing", borrowing))
        membership_finding = _answer_finding(
            f"demo.finding.track10.membership.{index}", MEMBERSHIP, membership_keys,
            "demo.membership.observed", f"demo.evidence.track10.membership.{index}",
            f"demo.contribution.track10.membership.{index}",
        )
        _append_contributed_claim(acts, registry, membership_finding,
                                  membership_finding["evidence_ids"][0], membership_finding["contribution_id"])
    return surface, acts, bundle_types, school_shared


def _track9_unknown_case(name: str, *, supplied: bool) -> tuple[Any, list[dict[str, Any]], str, str]:
    helper = _track8()
    generator = helper._track6b_generator()
    track9_path = ROOT / "tests" / "test_sli_track9_recording_state.py"
    spec = importlib.util.spec_from_file_location(f"track10_track9_{name}", track9_path)
    assert spec and spec.loader
    track9 = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = track9
    spec.loader.exec_module(track9)
    original_members, original_seal = generator._package_members, generator._seal_disposable_reader_package
    account_bundle = {"schema": "bundle.v2", "id": "demo.sli.track9.account-vocabulary", "version": "v1",
                      "label": "Synthetic Track 9 relationship account declaration",
                      "fact_types": [track9._fact_type()]}
    rule_id = "demo.rule.sli.track9.account-state"
    account_rule = generator._reader_rule(
        rule_id, "demo.sli.track9.account-evidence", subject=track9.ACCOUNT_TYPE,
        value={"op": "ref", "name": track9.ACCOUNT_TYPE, "field": "borrowing_identity"},
    )

    def extended_members() -> tuple[list[tuple[dict[str, Any], str]], list[dict[str, str]]]:
        members, entrypoints = original_members()
        members.extend(((account_bundle, "fact-type-bundle"), (account_rule, "computation")))
        entrypoints.extend({"id": citizen["id"], "version": citizen["version"]} for citizen, _ in members[-2:])
        return members, entrypoints

    def seal_with_account_binding(surface: Any) -> Any:
        package_path = surface.members / generator.PACKAGE_FILE
        package = json.loads(package_path.read_text("utf-8"))
        package["input_bindings"].append({"symbol": track9.ACCOUNT_TYPE,
                                          "fact_type": {"id": track9.ACCOUNT_TYPE, "version": "v1"},
                                          "mode": "required"})
        package_path.write_bytes(generator._bytes(package))
        return original_seal(surface)

    generator._package_members = extended_members
    generator._seal_disposable_reader_package = seal_with_account_binding
    try:
        output_root = ROOT / "temp" / "track10" / name
        output_root.mkdir(parents=True, exist_ok=True)
        surface, acts, _resolved = generator._prepare_case("ordinary", output_root)
    finally:
        generator._package_members = original_members
        generator._seal_disposable_reader_package = original_seal
    if supplied:
        acts = track9._append_account_answer(generator, acts)
        adoption = acts.pop()
        assertion = acts.pop()
        contribution = acts.pop()
        base = project(tuple(dict(row) for row in acts), DerivationSchemas().registry)
        admitted = apply_contribution_batch(
            base, contribution_act=contribution, successor_acts=[assertion],
            registry=DerivationSchemas().registry,
            record_id=f"demo.contribution-record.track10.{name}",
        )
        if admitted.terminal_record["phase"] != "completed":
            raise AssertionError(f"Track 10 ordinary answer failed contribution admission: {admitted.terminal_record}")
        acts.extend((contribution, assertion))
        adoption["committed_against"] = len(acts)
        acts.append(adoption)
        acts = generator._renumber(acts)
    return surface, acts, rule_id, track9.FINDING_ID


def _track9_module(name: str) -> Any:
    path = ROOT / "tests" / "test_sli_track9_recording_state.py"
    spec = importlib.util.spec_from_file_location(f"track10_track9_api_{name}", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class SavedAccountEvidence(unittest.TestCase):
    def test_no_answer_and_supplied_unknown_account_are_distinct_saved_states(self) -> None:
        empty_surface, empty_acts, producer, source_id = _track9_unknown_case("empty-account", supplied=False)
        supplied_surface, supplied_acts, _producer, _source_id = _track9_unknown_case(
            "supplied-unknown-account", supplied=True)
        empty = _save("no-answer", empty_acts, empty_surface, (producer,))
        supplied = _save("supplied-unknown", supplied_acts, supplied_surface, (producer,))
        self.assertEqual(empty["scope"]["selected_publication_ids"], [])
        self.assertEqual(empty["provenance"]["package"]["id"],
                         supplied["provenance"]["package"]["id"])
        self.assertTrue(supplied["scope"]["selected_publication_ids"])
        selected = {row["finding"]["id"]: row["finding"] for row in supplied["publications"]
                    if row["finding"]["id"] in supplied["scope"]["selected_publication_ids"]}
        account = next(row for row in selected.values() if row.get("value") == "unknown")
        source = next(row["finding"] for row in supplied["evaluated_support"]
                      if row["finding"]["id"] == source_id)
        self.assertEqual(source["value"]["borrowing_identity"], "unknown")
        self.assertEqual(source["value"]["statement_scope"], "unknown")
        self.assertEqual({pin["id"] for pin in account.get("pins", []) if pin.get("role") == "input"},
                         {source_id})
        self.assertEqual(supplied["provenance"]["run_id"], "demo.track10.supplied-unknown")
        # The empty selected result has provenance but supports no claim about tax defaults.
        self.assertFalse(any(row["finding"]["id"] == source_id for row in empty["evaluated_support"]))

    def test_resolve_then_retract_preserves_actual_lineage_and_removes_current_support(self) -> None:
        surface, acts, producer, source_id = _track9_unknown_case("resolve-retract", supplied=True)
        _track9_module("resolve-retract")
        old = next(row["payload"]["finding"] for row in acts
                   if row.get("kind") == "assertion" and row["payload"].get("finding", {}).get("id") == source_id)
        borrowing = "demo.track10.borrowing.resolved"
        acts.append(act(len(acts), "entity-introduced", {"entity": demo_entity(
            borrowing, "Synthetic resolved borrowing", "demo.sli-borrowing")}))
        value = dict(old["value"])
        value.update({"borrowing_identity": "known", "borrowing_reference": borrowing})
        correction = dict(old)
        correction.update({"id": "demo.finding.sli.account-a.resolved", "value": value,
                           "evidence_ids": ["demo.evidence.sli.account-a.resolved"],
                           "contribution_id": "demo.contribution.sli.account-a.resolved"})
        _append_contributed_claim(acts, DerivationSchemas().registry, correction,
                                  correction["evidence_ids"][0], correction["contribution_id"])
        resolved = _save("resolved-account", acts, surface, (producer,))
        self.assertTrue(resolved["scope"]["selected_publication_ids"])
        resolved_result = next(row["finding"] for row in resolved["publications"]
                               if row["finding"]["id"] in resolved["scope"]["selected_publication_ids"])
        self.assertEqual(resolved_result["value"], "known")
        resolved_source = next(row["finding"] for row in resolved["evaluated_support"]
                               if row["finding"]["id"] == correction["id"])
        self.assertEqual(resolved_source["value"]["borrowing_reference"], borrowing)
        self.assertEqual(resolved_source["value"]["schooling_fact"], "missing")
        self.assertIsNone(resolved_source["value"]["schooling_reference"])
        self.assertEqual(resolved_source["value"]["statement_scope"], "unknown")
        self.assertIsNone(resolved_source["value"]["statement_reference"])
        retract = act(len(acts), "finding-retracted", {"finding_id": correction["id"]})
        retract["act_id"] = "demo.track10.account-resolution-retraction"
        acts.append(retract)
        retracted = _save("retracted-account", acts, surface, (producer,))
        self.assertEqual(retracted["scope"]["selected_publication_ids"], [])
        historical = {row["finding"]["id"]: row for row in retracted["lineage"]}
        self.assertEqual(historical[source_id]["status"], "displaced")
        self.assertEqual(historical[correction["id"]]["status"], "displaced")
        self.assertIn({"kind": "correction", "by": correction["id"]},
                      historical[source_id]["displacement_reasons"])
        self.assertIn({"kind": "retraction", "by": retract["act_id"]},
                      historical[correction["id"]]["displacement_reasons"])
        self.assertEqual(retracted["lineage_acts"], [retract])
        self.assertNotIn(source_id, {row["finding"]["id"] for row in retracted["evaluated_support"]})
        self.assertNotIn(correction["id"], {row["finding"]["id"] for row in retracted["evaluated_support"]})

    def test_real_staged_schooling_financing_statement_chain(self) -> None:
        import copy

        surface, acts, _declared_types, school = _track10_live_chain(equal_pair=False)
        corrected_acts = copy.deepcopy(acts)
        correction = dict(school)
        correction.update({"id": "demo.finding.track10.school.shared.corrected",
                           "value": "demo.schooling.corrected-observation",
                           "evidence_ids": ["demo.evidence.track10.school.shared.corrected"],
                           "contribution_id": "demo.contribution.track10.school.shared.corrected"})
        _append_contributed_claim(
            corrected_acts, DerivationSchemas().registry, correction,
            correction["evidence_ids"][0], correction["contribution_id"],
        )
        selected_producers = (FINANCE_RULE, MEMBERSHIP_RULE, MEMBERSHIP_COUNT_RULE)
        saved_before = _save("staged-chain-before", acts, surface, selected_producers)
        saved_after = _save("staged-chain-after", corrected_acts, surface, selected_producers)
        before_publications = [row["finding"] for row in saved_before["publications"]]
        publications = [row["finding"] for row in saved_after["publications"]]
        finance_before = [finding for finding in before_publications if
                          {"role": "computation", "id": FINANCE_RULE, "version": "v1"} in finding.get("pins", [])]
        finance_rows = [finding for finding in publications if
                        {"role": "computation", "id": FINANCE_RULE, "version": "v1"} in finding.get("pins", [])]
        membership_before = [finding for finding in before_publications if
                             {"role": "computation", "id": MEMBERSHIP_RULE, "version": "v1"} in finding.get("pins", [])]
        membership_rows = [finding for finding in publications if
                           {"role": "computation", "id": MEMBERSHIP_RULE, "version": "v1"} in finding.get("pins", [])]
        count_rows = [finding for finding in publications if
                      {"role": "computation", "id": MEMBERSHIP_COUNT_RULE, "version": "v1"}
                      in finding.get("pins", [])]
        self.assertEqual((len(finance_rows), len(membership_rows), len(count_rows)), (3, 3, 3))
        self.assertEqual(set(saved_after["scope"]["selected_producer_ids"]),
                         {FINANCE_RULE, MEMBERSHIP_RULE, MEMBERSHIP_COUNT_RULE})
        self.assertEqual(set(saved_after["scope"]["selected_publication_ids"]),
                         {row["id"] for row in finance_rows + membership_rows + count_rows})
        self.assertTrue(saved_after["scope"]["other_run_publication_ids"])
        self.assertEqual(sorted(str(row["value"]) for row in count_rows), ["1", "1", "1"])

        before_source = {row["finding"]["id"]: row["finding"] for row in saved_before["evaluated_support"]}
        after_source = {row["finding"]["id"]: row["finding"] for row in saved_after["evaluated_support"]}
        self.assertNotIn(school["id"], after_source)
        self.assertEqual(after_source[correction["id"]]["value"], "demo.schooling.corrected-observation")
        self.assertEqual(before_source[school["id"]]["value"], "demo.schooling.same-observation")

        def finance_result(rows: list[dict[str, Any]], source_id: str) -> dict[str, Any]:
            return next(row for row in rows if any(pin.get("role") == "input" and pin.get("id") == source_id
                                                   for pin in row.get("pins", [])))

        shared_a_before = finance_result(finance_before, "demo.finding.track10.financing.0")
        shared_a_after = finance_result(finance_rows, "demo.finding.track10.financing.0")
        shared_b_before = finance_result(finance_before, "demo.finding.track10.financing.1")
        shared_b_after = finance_result(finance_rows, "demo.finding.track10.financing.1")
        independent_before = finance_result(finance_before, "demo.finding.track10.financing.2")
        independent_after = finance_result(finance_rows, "demo.finding.track10.financing.2")
        for before, after in ((shared_a_before, shared_a_after), (shared_b_before, shared_b_after)):
            self.assertEqual(after["value"], "demo.schooling.corrected-observation")
            self.assertIn(correction["id"], {pin.get("id") for pin in after["pins"] if pin.get("role") == "input"})
            self.assertNotIn(school["id"], {pin.get("id") for pin in after["pins"] if pin.get("role") == "input"})
            self.assertEqual(before["value"], "demo.schooling.same-observation")
        self.assertEqual(independent_before["value"], independent_after["value"])
        self.assertEqual(independent_before["pins"], independent_after["pins"])

        # Statement S1 reads its single admitted financing observation.
        s1_result_before = next(row for row in membership_before if any(
            pin.get("role") == "input" and pin.get("id") == shared_a_before["id"] for pin in row.get("pins", [])))
        s1_result_after = next(row for row in membership_rows if any(
            pin.get("role") == "input" and pin.get("id") == shared_a_after["id"] for pin in row.get("pins", [])))
        self.assertEqual(s1_result_before["value"], "true")
        self.assertEqual(s1_result_after["value"], "false")
        s2_before = next(row for row in membership_before if any(
            pin.get("id") == "demo.finding.track10.membership.1" for pin in row.get("pins", [])))
        s2_after = next(row for row in membership_rows if any(
            pin.get("id") == "demo.finding.track10.membership.1" for pin in row.get("pins", [])))
        self.assertEqual((s2_before["value"], s2_after["value"]), ("true", "false"))
        # Statement S3 consumes only the independent financing result; its
        # saved value and pins remain byte-identical across correction.
        s3_before = next(row for row in membership_before if any(
            pin.get("role") == "input" and pin.get("id") == independent_before["id"] for pin in row.get("pins", [])))
        s3_after = next(row for row in membership_rows if any(
            pin.get("role") == "input" and pin.get("id") == independent_after["id"] for pin in row.get("pins", [])))
        self.assertEqual(s3_before["value"], "true")
        self.assertEqual(s3_after["value"], "true")
        self.assertEqual(json.dumps(s3_before, sort_keys=True), json.dumps(s3_after, sort_keys=True))

        def source_ids(document: dict[str, Any], output: dict[str, Any]) -> set[str]:
            pub_map = {row["finding"]["id"]: row["finding"] for row in document["publications"]}
            supported = {row["finding"]["id"] for row in document["evaluated_support"]}
            todo, visited, result = [output["id"]], set(), set()
            while todo:
                current = todo.pop()
                if current in visited:
                    continue
                visited.add(current)
                for pin in pub_map[current].get("pins", []):
                    if pin.get("role") != "input":
                        continue
                    if pin["id"] in supported:
                        result.add(pin["id"])
                    elif pin["id"] in pub_map:
                        todo.append(pin["id"])
            return result

        expected_support = {
            "demo.finding.track10.membership.0": {"demo.finding.track10.membership.0", "demo.finding.track10.financing.0", correction["id"]},
            "demo.finding.track10.membership.1": {"demo.finding.track10.membership.1", "demo.finding.track10.financing.1", correction["id"]},
            "demo.finding.track10.membership.2": {"demo.finding.track10.membership.2", "demo.finding.track10.financing.2", "demo.finding.track10.school.independent"},
        }
        for input_id, expected in expected_support.items():
            result = next(row for row in membership_rows if any(pin.get("id") == input_id for pin in row.get("pins", [])))
            self.assertEqual(source_ids(saved_after, result), expected)
            if input_id.endswith(".2"):
                before_result = next(row for row in membership_before if any(
                    pin.get("id") == input_id for pin in row.get("pins", [])))
                self.assertEqual(source_ids(saved_before, before_result), expected)
                support_before = {row["finding"]["id"]: row for row in saved_before["evaluated_support"]}
                support_after = {row["finding"]["id"]: row for row in saved_after["evaluated_support"]}
                self.assertEqual({key: support_before[key] for key in expected},
                                 {key: support_after[key] for key in expected})

    def test_equal_valued_situations_are_collected_with_exact_support(self) -> None:
        surface, acts, _declared_types, _school = _track10_live_chain(equal_pair=True)
        saved = _save("equal-valued-two-situations", acts, surface,
                      (FINANCE_RULE, MEMBERSHIP_RULE, MEMBERSHIP_COUNT_RULE),
                      experiment_metadata={"kind": "application-capability-experiment",
                                           "capability": "mixed-period student-loan treatment",
                                           "status": "unadopted",
                                           "basis": "Track 10 charter experiment scope"})
        pubs = [row["finding"] for row in saved["publications"]]
        finance = [row for row in pubs if {"role": "computation", "id": FINANCE_RULE, "version": "v1"}
                   in row.get("pins", [])]
        membership = [row for row in pubs if {"role": "computation", "id": MEMBERSHIP_RULE, "version": "v1"}
                      in row.get("pins", [])]
        self.assertEqual((len(finance), len(membership)), (5, 3))
        s1 = next(row for row in membership if any(pin.get("id") == "demo.finding.track10.membership.0"
                                                   for pin in row.get("pins", [])))
        finance_ids = {row["id"] for row in finance if any(pin.get("id") in {
            "demo.finding.track10.financing.0", "demo.finding.track10.financing.1"
        } for pin in row.get("pins", []))}
        self.assertEqual({pin["id"] for pin in s1["pins"] if pin.get("role") == "input"},
                         {"demo.finding.track10.membership.0", *finance_ids})
        self.assertEqual(s1["value"], "true")
        self.assertEqual({row["fact"]["bindings"]["period"] for row in saved["evaluated_support"]
                          if row["finding"]["id"] in {"demo.finding.track10.school.shared",
                                                        "demo.finding.track10.school.independent"}},
                         {"2024", "2025"})
        self.assertEqual(saved["experiment_metadata"]["status"], "unadopted")
        self.assertEqual(saved["experiment_metadata"]["capability"], "mixed-period student-loan treatment")
        self.assertNotIn("application-capability-experiment",
                         {row.get("artifact_id") for row in saved["dispositions"]})
        support = {row["finding"]["id"]: row for row in saved["evaluated_support"]}
        self.assertEqual({support[key]["finding"]["value"] for key in (
            "demo.finding.track10.financing.0", "demo.finding.track10.financing.1")},
            {"demo.financing.observed"})
        bindings = {tuple(sorted(support[key]["fact"]["bindings"].items())) for key in (
            "demo.finding.track10.financing.0", "demo.finding.track10.financing.1")}
        self.assertEqual(bindings, {
            tuple(sorted((("borrowing", "demo.track8.borrowing.a"), ("situation", "demo.sli.schooling.shared"),
                          ("period", "2024"), ("institution", "demo.sli.schooling.institution.shared"),
                          ("programme", "demo.sli.schooling.programme.shared")))),
            tuple(sorted((("borrowing", "demo.track8.borrowing.a"), ("situation", "demo.sli.schooling.independent"),
                          ("period", "2025"), ("institution", "demo.sli.schooling.institution.independent"),
                          ("programme", "demo.sli.schooling.programme.independent")))),
        })
        school_rows = {row["finding"]["id"]: row for row in saved["evaluated_support"]
                       if row["finding"]["id"] in {"demo.finding.track10.school.shared",
                                                     "demo.finding.track10.school.independent"}}
        self.assertEqual({row["finding"]["value"] for row in school_rows.values()},
                         {"demo.schooling.same-observation"})
        self.assertEqual({tuple(sorted(row["fact"]["bindings"].items())) for row in school_rows.values()}, {
            tuple(sorted((("situation", "demo.sli.schooling.shared"), ("period", "2024"),
                          ("institution", "demo.sli.schooling.institution.shared"),
                          ("programme", "demo.sli.schooling.programme.shared")))),
            tuple(sorted((("situation", "demo.sli.schooling.independent"), ("period", "2025"),
                          ("institution", "demo.sli.schooling.institution.independent"),
                          ("programme", "demo.sli.schooling.programme.independent")))),
        })
        count_only = _save("count-only-selection", acts, surface, (MEMBERSHIP_COUNT_RULE,))
        selected_ids = set(count_only["scope"]["selected_publication_ids"])
        required_ids = set(count_only["scope"]["required_support_publication_ids"])
        self.assertTrue(selected_ids)
        self.assertTrue(required_ids)
        self.assertTrue(all(any(pin.get("id") in required_ids for pin in row["finding"].get("pins", []))
                            for row in count_only["publications"] if row["finding"]["id"] in selected_ids))
        required_finance_ids = {row["finding"]["id"] for row in count_only["publications"]
                                if {"role": "computation", "id": FINANCE_RULE, "version": "v1"}
                                in row["finding"].get("pins", [])}
        self.assertTrue(required_finance_ids)
        self.assertTrue(required_finance_ids.issubset(required_ids))
        self.assertTrue(any(any(pin.get("id") in required_finance_ids for pin in row["finding"].get("pins", []))
                            for row in count_only["publications"]
                            if {"role": "computation", "id": MEMBERSHIP_RULE, "version": "v1"}
                            in row["finding"].get("pins", [])))
        self.assertTrue(required_ids.isdisjoint(set(count_only["scope"]["other_run_publication_ids"])))

    def test_differing_values_block_required_consumer_with_recorded_missing_inputs(self) -> None:
        import copy

        surface, acts, _declared_types, school = _track10_live_chain(equal_pair=True)
        corrected = copy.deepcopy(acts)
        claim = dict(school)
        claim.update({"id": "demo.finding.track10.school.shared.corrected",
                      "value": "demo.schooling.corrected-observation",
                      "evidence_ids": ["demo.evidence.track10.school.shared.corrected"],
                      "contribution_id": "demo.contribution.track10.school.shared.corrected"})
        _append_contributed_claim(corrected, DerivationSchemas().registry, claim,
                                  claim["evidence_ids"][0], claim["contribution_id"])
        saved = _save("differing-finance-values-block", corrected, surface,
                      (FINANCE_RULE, MEMBERSHIP_RULE, MEMBERSHIP_COUNT_RULE))
        blocked = [row for row in saved["dispositions"]
                   if row.get("disposition") == "blocked"
                   and row.get("artifact_id") == MEMBERSHIP_RULE]
        self.assertEqual(len(blocked), 2)
        symbols = {row["symbol"] for row in blocked}
        self.assertTrue(any("borrowing=demo.track8.borrowing.a" in symbol for symbol in symbols))
        self.assertTrue(any("borrowing=demo.track8.borrowing.b" in symbol for symbol in symbols))
        self.assertEqual(len(symbols), 2)
        source_by_id = {row["finding"]["id"]: row for row in saved["evaluated_support"]}
        finance_sources = [row for row in saved["evaluated_support"]
                           if row["fact"].get("fact_type_id") == FINANCE]
        for row in blocked:
            subject_pins = {pin["id"] for pin in row.get("pins", []) if pin.get("role") == "input"}
            self.assertEqual(len(subject_pins), 1)
            subject_id = next(iter(subject_pins))
            subject = source_by_id[subject_id]
            borrowing = subject["fact"]["bindings"]["borrowing"]
            expected_missing_for_subject = {source["fact"]["fact_id"] for source in finance_sources
                                             if source["fact"]["bindings"].get("borrowing") == borrowing}
            self.assertEqual(len(expected_missing_for_subject), 2)
            self.assertEqual(set(row.get("missing", [])), expected_missing_for_subject)
            self.assertTrue(all(item.startswith(FINANCE + "|") for item in expected_missing_for_subject))
            self.assertEqual({pin.get("role") for pin in row.get("pins", [])}, {"adoption", "input"})
        recorded = [row for row in saved["recorded_blocked_dependencies"]
                    if row.get("artifact_id") == MEMBERSHIP_RULE]
        self.assertEqual(recorded, blocked)
        self.assertEqual({row["symbol"] for row in recorded}, symbols)
        self.assertFalse(any(item.get("owner", {}).get("artifact_id") == MEMBERSHIP_RULE
                             for item in saved["unresolved_support"]))
        self.assertTrue(all(any(row["finding"]["id"] == pin["id"]
                                for row in saved["evaluated_support"])
                            for disposition in blocked for pin in disposition["pins"]
                            if pin.get("role") == "input"))
        self.assertFalse(saved["complete"])
        self.assertEqual({item["pin"]["id"] for item in saved["unresolved_support"]},
                         {"demo.ug.wlt.h0", "demo.ug.wst.h0"})
        tampered = json.loads(dumps(saved))
        target = next(row for row in tampered["recorded_blocked_dependencies"]
                      if row.get("artifact_id") == MEMBERSHIP_RULE)
        target["symbol"] = "demo.rule.sli.track10.statement-borrowing-observation|wrong-subject"
        with self.assertRaises(SavedEvidenceError):
            loads(json.dumps(tampered))


    def test_actual_coordinator_publications_reopen_with_exact_source_support(self) -> None:
        helper = _track8()
        generator = helper._track6b_generator()
        surface, _members, before, corrected, retracted = helper._prototype_relationship_acts(generator)
        saved_before = _save("before", before, surface)
        saved_after = _save("after", corrected, surface)

        before_ids = {row["finding"]["id"] for row in saved_before["evaluated_support"]}
        after_ids = {row["finding"]["id"] for row in saved_after["evaluated_support"]}
        self.assertIn(retracted, before_ids)
        self.assertNotIn(retracted, after_ids)
        # Track 8's broader publication contains family-horizon pins. This
        # experimental carrier currently does not serialize those target
        # citizen types, so it retains them as unresolved.
        self.assertFalse(saved_after["complete"])
        unresolved = {(item["owner"]["type"], item["owner"]["id"],
                       item["owner"].get("artifact_id"), item["owner"].get("symbol"), item["pin"]["id"])
                      for item in saved_after["unresolved_support"] if "pin" in item}
        self.assertEqual(unresolved, {
            ("publication", "finding:derived:ed622c42ac5f7193c51a71e1", None,
             "tax.us.2025.f1099b.covered-w-lt.member-validation", "demo.ug.wlt.h0"),
            ("publication", "finding:derived:4cf69710d37f24c016ea901a", None,
             "tax.us.2025.f1099b.covered-w-st.member-validation", "demo.ug.wst.h0"),
            ("disposition", "tax.us.2025.f1099b.covered-w-lt.member-validation.synthesized",
             "tax.us.2025.f1099b.covered-w-lt.member-validation.synthesized",
             "tax.us.2025.f1099b.covered-w-lt.member-validation", "demo.ug.wlt.h0"),
            ("disposition", "tax.us.2025.f1099b.covered-w-st.member-validation.synthesized",
             "tax.us.2025.f1099b.covered-w-st.member-validation.synthesized",
             "tax.us.2025.f1099b.covered-w-st.member-validation", "demo.ug.wst.h0"),
        })
        self.assertTrue(saved_after["recorded_blocked_dependencies"])
        self.assertTrue(saved_after["publications"])
        self.assertTrue(saved_after["dispositions"])
        self.assertTrue(all(row["fact"]["bindings"] for row in saved_after["evaluated_support"]))
        altered = json.loads(dumps(saved_after))
        altered["unresolved_support"][0]["owner"]["id"] = "finding:derived:wrong-owner"
        with self.assertRaises(SavedEvidenceError):
            loads(json.dumps(altered))

        route = next(row["finding"] for row in saved_after["publications"]
                     if any(pin.get("id") == generator.LINKER for pin in row["finding"].get("pins", [])))
        self.assertTrue(route["value"])
        direct_input_ids = {pin["id"] for pin in route["pins"] if pin.get("role") == "input"}
        self.assertTrue(direct_input_ids)
        # The saved transitive source support retains the corrected current
        # link rows and their actual values; context was not promoted to support.
        saved_findings = {row["finding"]["id"]: row["finding"] for row in saved_after["evaluated_support"]}
        self.assertIn("demo.finding.track8.statement-borrowing.s1.b", saved_findings)
        self.assertEqual(saved_findings["demo.finding.track8.statement-borrowing.s1.b"]["value"], {})

    def test_missing_support_and_cross_run_publication_are_refused(self) -> None:
        helper = _track8()
        generator = helper._track6b_generator()
        surface, _members, _before, corrected, _retracted = helper._prototype_relationship_acts(generator)
        saved = _save("negative", corrected, surface)
        altered = json.loads(dumps(saved))
        altered["evaluated_support"].pop()
        with self.assertRaises(SavedEvidenceError):
            loads(json.dumps(altered))

        altered = json.loads(dumps(saved))
        altered["provenance"]["run_id"] = "demo.track10.other-run"
        with self.assertRaises(SavedEvidenceError):
            loads(json.dumps(altered))


if __name__ == "__main__":
    unittest.main()
