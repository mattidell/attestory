"""Track 11: execute admitted declaration variants over Track 10 sources."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.package_validation import package_instance_checksum, validate_package
from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.kernel.act_log import ActLog
from packages.kernel.facts import facts_of
from packages.kernel.findings import project
from packages.kernel.currency import compute_currency
from packages.derivation.loader import workspace_registry
from tools.sli_saved_account_evidence import capture, dumps, loads
from tests.test_sli_track10_saved_account_evidence import (
    FINANCE, FINANCE_RESULT, FINANCE_RULE, MEMBERSHIP, MEMBERSHIP_RULE, SCHOOL,
    ROOT, _track10_live_chain,
)
from tests.test_sli_track8_relationship_evidence import _track6b_generator, _runner_parity
from tests.support import act

EXPECTED = "demo.sli.track11.financing-expected"
AVAILABLE = "demo.sli.track11.financing-available"
EXPECTED_RULE = "demo.rule.sli.track11.financing-expected"
AVAILABLE_RULE = "demo.rule.sli.track11.financing-available"
EXPECTED_FAMILY = "demo.family.sli.track11.financing-expected"
AVAILABLE_FAMILY = "demo.family.sli.track11.financing-available"


def _reseal(surface: Any, acts: list[dict[str, Any]], *, reverse: bool) -> tuple[str, ...]:
    """Change a test-local declaration, then run ordinary package admission."""
    generator = __import__(
        "tools.presentation_harness.examples.generate_track6b_saved_presentations",
        fromlist=["_bytes"],
    )
    package_path = surface.members / generator.PACKAGE_FILE
    package = json.loads(package_path.read_text("utf-8"))
    consumer_path = surface.members / f"{MEMBERSHIP_RULE}.json"
    consumer = json.loads(consumer_path.read_text("utf-8"))
    if consumer.get("requires") != [FINANCE_RESULT]:
        raise AssertionError(f"unexpected Track 10 control declaration: {consumer.get('requires')!r}")
    consumer["requires"] = []
    consumer["value"]["value"]["fact_type"] = {"id": SCHOOL, "version": "v1"}
    consumer_path.write_bytes(generator._bytes(consumer))

    registry_path = surface.members / generator.REGISTRY_FILE
    registry = json.loads(registry_path.read_text("utf-8"))
    citizen = next(row for row in registry["citizens"]
                   if row["id"] == MEMBERSHIP_RULE and row["version"] == "v1")
    citizen["checksum"] = generator._citizen_checksum(consumer)

    if reverse:
        package["members"].sort(key=lambda row: 0 if row["id"] == MEMBERSHIP_RULE else 1)
        package["entrypoints"].sort(key=lambda row: 0 if row["id"] == MEMBERSHIP_RULE else 1)
    package.pop("package_checksum", None)
    package["package_checksum"] = package_instance_checksum(package)
    package_entry = next(row for row in registry["packages"]
                        if row["id"] == package["id"] and row["version"] == package["version"])
    package_entry["checksum"] = package["package_checksum"]
    registry_bytes = generator._bytes(registry)
    registry_path.write_bytes(registry_bytes)
    package_path.write_bytes(generator._bytes(package))

    release_path = surface.releases / generator.RELEASE_FILE
    release = json.loads(release_path.read_text("utf-8"))
    import hashlib
    release["package_registry_sha256"] = hashlib.sha256(registry_bytes).hexdigest()
    release_bytes = generator._bytes(release)
    release_path.write_bytes(release_bytes)
    surface.adoption["payload"]["package"]["checksum"] = package["package_checksum"]
    surface.adoption["payload"]["release"]["checksum"] = hashlib.sha256(release_bytes).hexdigest()
    for act_row in acts:
        if act_row.get("kind") == "package-adoption":
            act_row["payload"]["package"]["checksum"] = package["package_checksum"]
            act_row["payload"]["release"]["checksum"] = hashlib.sha256(release_bytes).hexdigest()

    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for path in surface.members.glob("*.json"):
        row = json.loads(path.read_text("utf-8"))
        if isinstance(row, dict) and isinstance(row.get("id"), str) and isinstance(row.get("version"), str):
            corpus[(row["id"], row["version"])] = row
    result = validate_package(package, corpus, DerivationSchemas())
    if not result.ok:
        raise AssertionError("candidate package admission failed: " + "; ".join(
            f"{issue.code}: {issue.detail}" for issue in result.issues))
    return tuple(member["id"] for member in result.resolved_members
                 if member.get("schema", "").startswith("rule-artifact"))


def _reseal_readiness_candidate(surface: Any, acts: list[dict[str, Any]], *,
                                consumer_first: bool) -> tuple[str, ...]:
    """Add expected/available witnesses using admitted v12 rules and ops."""
    generator = __import__("tools.presentation_harness.examples.generate_track6b_saved_presentations",
                           fromlist=["_reader_rule"])
    package_path = surface.members / generator.PACKAGE_FILE
    package = json.loads(package_path.read_text("utf-8"))
    registry_path = surface.members / generator.REGISTRY_FILE
    registry = json.loads(registry_path.read_text("utf-8"))
    bundle_path = surface.members / f"{generator.CLAIM_BUNDLE}.json"
    bundle = json.loads(bundle_path.read_text("utf-8"))
    source_types = {row["id"]: row for row in bundle["fact_types"]}
    witnesses: list[dict[str, Any]] = []
    for type_id, source_id, title in (
        (EXPECTED, FINANCE, "Expected synthetic financing member"),
        (AVAILABLE, FINANCE_RESULT, "Available synthetic financing result"),
    ):
        source_type = source_types[source_id]
        witnesses.append({
            "schema": "fact-type.v2", "id": type_id, "version": "v1", "title": title,
            "nature": "determinable", "identity_keys": copy.deepcopy(source_type["identity_keys"]),
            "value_schema": {"type": "number"}, "supersession": {"policy": "free"},
        })
    bundle["fact_types"] = list(bundle["fact_types"]) + witnesses
    bundle_path.write_bytes(generator._bytes(bundle))

    expected_rule = generator._reader_rule(EXPECTED_RULE, EXPECTED, subject=FINANCE, value=1)
    available_rule = generator._reader_rule(
        AVAILABLE_RULE, AVAILABLE, subject=FINANCE, requires=[FINANCE_RESULT],
        joined=FINANCE_RESULT, direction="subject_contains_joined",
        value={
            "op": "choose",
            "when": {"op": "categorical_compare", "cmp": "eq",
                     "left": {"op": "ref", "name": FINANCE_RESULT},
                     "right": {"op": "ref", "name": FINANCE_RESULT}},
            "then": 1,
            "else": {"op": "block", "code": "DEPENDENCY_INVALID"},
        },
    )
    consumer_path = surface.members / f"{MEMBERSHIP_RULE}.json"
    consumer = json.loads(consumer_path.read_text("utf-8"))
    consumer["requires"] = [EXPECTED, AVAILABLE]
    consumer["value"] = {
        "op": "choose",
        "when": {"op": "compare", "cmp": "eq",
                 "left": {"op": "add", "args": [{"op": "collect", "name": EXPECTED,
                                                       "source_set": EXPECTED_FAMILY}]},
                 "right": {"op": "add", "args": [{"op": "collect", "name": AVAILABLE,
                                                        "source_set": AVAILABLE_FAMILY}]}},
        "then": {"op": "collect_categorical_all_equal", "name": FINANCE_RESULT,
                 "value": {"op": "category_literal", "fact_type": {"id": SCHOOL, "version": "v1"},
                           "value": "demo.schooling.same-observation"}},
        "else": {"op": "block", "code": "DEPENDENCY_INVALID"},
    }
    consumer_path.write_bytes(generator._bytes(consumer))

    new_rules = (expected_rule, available_rule)
    existing_ids = {(row["id"], row["version"]) for row in package["members"]}
    for rule in new_rules:
        if (rule["id"], rule["version"]) in existing_ids:
            raise AssertionError(f"readiness candidate member collision: {rule['id']}")
        (surface.members / f"{rule['id']}.json").write_bytes(generator._bytes(rule))
        package["members"].append({"id": rule["id"], "role": "computation",
                                   "schema": rule["schema"], "version": rule["version"]})
        entry = {"id": rule["id"], "version": rule["version"]}
        package["entrypoints"].append(entry)
    families = (
        {"schema": "source-family.v1", "id": EXPECTED_FAMILY, "version": "v1",
         "title": "Synthetic expected financing witness family", "scope": copy.deepcopy(expected_rule["scope"]),
         "closure_claim": "Contains the expected-witness rows emitted for current financing source claims in this fixture.",
         "member_predicate": {"fact_type": EXPECTED}, "authorizes_subtotal": EXPECTED},
        {"schema": "source-family.v1", "id": AVAILABLE_FAMILY, "version": "v1",
         "title": "Synthetic available financing witness family", "scope": copy.deepcopy(available_rule["scope"]),
         "closure_claim": "Contains the available-witness rows emitted for financing results in this fixture.",
         "member_predicate": {"fact_type": AVAILABLE}, "authorizes_subtotal": AVAILABLE},
    )
    for family in families:
        (surface.members / f"{family['id']}.json").write_bytes(generator._bytes(family))
        package["members"].append({"id": family["id"], "role": "source-family",
                                   "schema": family["schema"], "version": family["version"]})
        package["entrypoints"].append({"id": family["id"], "version": family["version"]})
        registry["citizens"].append({"id": family["id"], "version": family["version"],
                                     "checksum": generator._citizen_checksum(family)})
    package["admitted_schemas"] = sorted(set(package["admitted_schemas"]) |
                                         {"rule-artifact.v12", "source-family.v1"})
    if not consumer_first:
        # Put both readiness producers before the consumer in the admitted
        # declaration sequence. Their meaning and dependencies stay identical.
        producer_ids = {EXPECTED_RULE, AVAILABLE_RULE}
        package["members"].sort(key=lambda row: (
            0 if row["id"] in producer_ids else 2 if row["id"] == MEMBERSHIP_RULE else 1,
        ))
        package["entrypoints"].sort(key=lambda row: (
            0 if row["id"] in producer_ids else 2 if row["id"] == MEMBERSHIP_RULE else 1,
        ))

    bundle_row = next(row for row in registry["citizens"]
                      if row["id"] == generator.CLAIM_BUNDLE and row["version"] == "v1")
    bundle_row["checksum"] = generator._citizen_checksum(bundle)
    consumer_row = next(row for row in registry["citizens"]
                        if row["id"] == MEMBERSHIP_RULE and row["version"] == "v1")
    consumer_row["checksum"] = generator._citizen_checksum(consumer)
    for rule in new_rules:
        registry["citizens"].append({"id": rule["id"], "version": rule["version"],
                                     "checksum": generator._citizen_checksum(rule)})
    package.pop("package_checksum", None)
    package["package_checksum"] = package_instance_checksum(package)
    package_entry = next(row for row in registry["packages"]
                        if row["id"] == package["id"] and row["version"] == package["version"])
    package_entry["checksum"] = package["package_checksum"]
    registry_bytes = generator._bytes(registry)
    registry_path.write_bytes(registry_bytes)
    package_path.write_bytes(generator._bytes(package))
    import hashlib
    release_path = surface.releases / generator.RELEASE_FILE
    release = json.loads(release_path.read_text("utf-8"))
    release["package_registry_sha256"] = hashlib.sha256(registry_bytes).hexdigest()
    release_bytes = generator._bytes(release)
    release_path.write_bytes(release_bytes)
    surface.adoption["payload"]["package"]["checksum"] = package["package_checksum"]
    surface.adoption["payload"]["release"]["checksum"] = hashlib.sha256(release_bytes).hexdigest()
    for act_row in acts:
        if act_row.get("kind") == "package-adoption":
            act_row["payload"]["package"]["checksum"] = package["package_checksum"]
            act_row["payload"]["release"]["checksum"] = hashlib.sha256(release_bytes).hexdigest()
    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for path in surface.members.glob("*.json"):
        row = json.loads(path.read_text("utf-8"))
        if isinstance(row, dict) and isinstance(row.get("id"), str) and isinstance(row.get("version"), str):
            corpus[(row["id"], row["version"])] = row
    result = validate_package(package, corpus, DerivationSchemas())
    if not result.ok:
        raise AssertionError("readiness candidate admission failed: " + "; ".join(
            f"{issue.code}: {issue.detail}" for issue in result.issues))
    return tuple(member["id"] for member in result.resolved_members
                 if member.get("schema", "").startswith("rule-artifact"))


def _current_source_members(acts: list[dict[str, Any]]) -> set[str]:
    state = project(tuple(copy.deepcopy(row) for row in acts), DerivationSchemas().registry)
    currency = compute_currency(state)
    lattice = facts_of(state.fact_state)
    finance_fact_ids = {fact_id for fact_id, fact in lattice.items() if fact.fact_type_id == FINANCE}
    return {finding_id for finding_id, finding in state.findings.items()
            if finding_id in currency.current_finding_ids and finding.get("fact_id") in finance_fact_ids}


def _source_finance_map(acts: list[dict[str, Any]]) -> dict[str, dict[str, str]]:
    state = project(tuple(copy.deepcopy(row) for row in acts), DerivationSchemas().registry)
    currency = compute_currency(state)
    lattice = facts_of(state.fact_state)
    return {
        finding_id: {"fact_id": str(finding["fact_id"]), **dict(lattice[finding["fact_id"]].keys)}
        for finding_id, finding in state.findings.items()
        if finding_id in currency.current_finding_ids
        and finding.get("fact_id") in lattice
        and lattice[finding["fact_id"]].fact_type_id == FINANCE
    }


def _execute_track11(name: str, acts: list[dict[str, Any]], surface: Any,
                     resolved_rule_sequence: tuple[str, ...] = ()) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Run actual coordinator and both runners; save under this track's scratch."""
    helper = __import__("tests.test_sli_track8_relationship_evidence", fromlist=["_track8"])
    track8 = helper
    generator = _track6b_generator()
    scratch = ROOT / "temp" / "track11"
    scratch.mkdir(parents=True, exist_ok=True)
    output: dict[str, Any]
    with tempfile.TemporaryDirectory(prefix=f"track11-{name}-") as raw:
        authoritative = ActLog(Path(raw) / "authoritative", workspace_registry())
        for act_row in acts:
            authoritative.append(act_row, expected_revision=act_row["committed_against"])
        recovered = ActLog(Path(raw) / "authoritative", workspace_registry()).read().acts
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(raw) / "workspace"), repo_root=ROOT,
            authoritative_acts=recovered, workspace_revision=len(recovered),
            run_scope={"jurisdiction": "us", "year": "2025"},
            scope_user=generator.USER, request={"schema": "run-request.v1"},
            run_id=f"demo.track11.{name}", governance_pins=[],
            surface=track8.generator_surface(surface), output_name=f"{name}.json",
        )
        if outcome.refusal is not None or outcome.output_path is None or outcome.publications is None:
            raise AssertionError(f"Track 11 live coordinator failed: {outcome.refusal!r}")
        output = json.loads(outcome.output_path.read_text("utf-8"))
        recovered_rows = [dict(row) for row in recovered]
        forward, reference = _runner_parity(recovered_rows, surface)
        source_finance_ids = _current_source_members(recovered_rows)
        source_finance_map = _source_finance_map(recovered_rows)
        live_rows = sorted(
            [(item.finding["symbol"], item.finding.get("value"), item.finding.get("pins"))
             for item in outcome.publications], key=lambda row: json.dumps(row, sort_keys=True))
        live_dispositions = [
            (row.get("artifact_id"), row.get("symbol"), row["disposition"], row.get("finding_id"),
             row.get("code"), row.get("missing")) for row in output["dispositions"]
        ]
        live_dispositions.sort(key=lambda row: json.dumps(row, sort_keys=True))
        live_matches_forward = live_rows == forward["publications"]
        live_dispositions_match_forward = live_dispositions == forward["dispositions"]
        if not live_matches_forward or not live_dispositions_match_forward:
            raise AssertionError(
                f"{name}: live coordinator output does not match forward runner "
                f"(publications={live_matches_forward}, dispositions={live_dispositions_match_forward})"
            )
        state = project(tuple(dict(row) for row in recovered), DerivationSchemas().registry)
        currency = compute_currency(state)
        lattice = facts_of(state.fact_state)
        current = {key: row for key, row in state.findings.items() if key in currency.current_finding_ids}
        keys = {fact_id: {"fact_type_id": fact.fact_type_id, "bindings": dict(fact.keys),
                          "individuated_by": list(fact.individuated_by)}
                for fact_id, fact in lattice.items()}
        evidence = {key: lifecycle.evidence for key, lifecycle in state.evidence.items()}
        adoption = next(pin for publication in outcome.publications
                        for pin in publication.finding.get("pins", []) if pin.get("role") == "adoption")
        saved = capture(
            run_id=outcome.run_id or "", package=adoption,
            publications=outcome.publications, dispositions=output["dispositions"],
            current_findings=current,
            fact_keys={fact_id: {"fact_type_id": fact.fact_type_id, "bindings": dict(fact.keys),
                                 "individuated_by": list(fact.individuated_by)}
                       for fact_id, fact in lattice.items()},
            evidence_by_id=evidence, selected_producer_ids=(
                FINANCE_RULE, MEMBERSHIP_RULE, EXPECTED_RULE, AVAILABLE_RULE,
            ),
            all_findings=state.findings,
            displacement_reasons={finding_id: [{"kind": reason.kind, "by": reason.by}
                                               for reason in reasons]
                                  for finding_id, reasons in currency.reasons.items()},
            lineage_acts=[row for row in recovered if row.get("kind") == "finding-retracted"],
            experiment_metadata={"declaration_order": name, "status": "unadopted"},
        )
        save_path = scratch / f"{name}.saved-account.json"
        save_path.write_bytes(dumps(saved))
        del outcome
        del state, current, lattice, evidence, recovered
    reopened = loads(save_path.read_bytes())
    path = scratch / f"{name}.execution.json"
    record = {"forward": forward, "reference": reference, "output": output,
              "resolved_rule_sequence": list(resolved_rule_sequence),
              "source_finance_ids": sorted(source_finance_ids),
              "source_finance_map": source_finance_map,
              "live_dispositions": live_dispositions,
              "live_matches_forward": live_matches_forward,
              "live_dispositions_match_forward": live_dispositions_match_forward,
              "live_publications": live_rows, "saved": reopened}
    path.write_text(json.dumps(record, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return record, forward, reference


def _saved_source_closure(saved: dict[str, Any], finding_id: str) -> set[str]:
    finding = next(row["finding"] for row in saved["publications"]
                   if row["finding"]["id"] == finding_id)
    return _saved_input_closure(saved, finding.get("pins", []))


def _saved_input_closure(saved: dict[str, Any], pins: list[dict[str, Any]]) -> set[str]:
    publications = {row["finding"]["id"]: row["finding"] for row in saved["publications"]}
    support = {row["finding"]["id"] for row in saved["evaluated_support"]}
    pending = [pin["id"] for pin in pins if pin.get("role") == "input"]
    visited: set[str] = set()
    leaves: set[str] = set()
    while pending:
        current = pending.pop()
        if current in visited:
            continue
        visited.add(current)
        if current not in publications:
            if current in support:
                leaves.add(current)
            else:
                raise AssertionError(f"saved input pin has no publication or evaluated support: {current}")
            continue
        finding = publications[current]
        for pin in finding.get("pins", []):
            if pin.get("role") != "input":
                continue
            target = pin["id"]
            if target in publications:
                pending.append(target)
            elif target in support:
                leaves.add(target)
            else:
                raise AssertionError(f"saved nested input pin has no publication or evaluated support: {target}")
    return leaves


class Track11CollectionDeclarations(unittest.TestCase):
    def test_removing_requires_preserves_only_actual_results_in_both_orders(self) -> None:
        # Track 10's control uses two finance rows for each of A and B.  Values
        # differ after the shared schooling correction; expected membership is
        # established from current source claims, independently of publications.
        surface, acts, _types, school = _track10_live_chain(equal_pair=True)
        correction = dict(school)
        correction.update({
            "id": "demo.finding.track11.school.shared.corrected",
            "value": "demo.schooling.corrected-observation",
            "evidence_ids": ["demo.evidence.track11.school.shared.corrected"],
            "contribution_id": "demo.contribution.track11.school.shared.corrected",
        })
        from tests.test_sli_track10_saved_account_evidence import _append_contributed_claim
        _append_contributed_claim(acts, DerivationSchemas().registry, correction,
                                  correction["evidence_ids"][0], correction["contribution_id"])
        expected_finance = _current_source_members(acts)
        self.assertEqual(len(expected_finance), 5)

        # Run the unchanged required-source declaration as the actual control.
        control, control_forward, control_reference = _execute_track11(
            "track11-required-control", acts, surface,
        )
        self.assertEqual(control_forward, control_reference)
        control_blocked = [row for row in control["saved"]["recorded_blocked_dependencies"]
                           if row.get("artifact_id") == MEMBERSHIP_RULE]
        self.assertEqual(len(control_blocked), 2)
        self.assertTrue(all(row.get("code") == "DEPENDENCY_INVALID" for row in control_blocked))
        self.assertEqual(len({row.get("symbol") for row in control_blocked}), 2)
        self.assertTrue(all(len(row.get("missing", [])) == 2 for row in control_blocked))

        observed: list[tuple[str, set[str], set[str], set[str]]] = []
        execution_orders: list[tuple[str, ...]] = []
        for reverse, label in ((False, "track11-consumer-last"), (True, "track11-consumer-first")):
            variant_surface, variant_acts, _types, variant_school = _track10_live_chain(equal_pair=True)
            variant_correction = dict(variant_school)
            variant_correction.update(correction)
            _append_contributed_claim(variant_acts, DerivationSchemas().registry, variant_correction,
                                      variant_correction["evidence_ids"][0], variant_correction["contribution_id"])
            ordered_ids = _reseal(variant_surface, variant_acts, reverse=reverse)
            relevant_order = tuple(item for item in ordered_ids if item in {FINANCE_RULE, MEMBERSHIP_RULE})
            execution_orders.append(relevant_order)
            record, forward, reference = _execute_track11(label, variant_acts, variant_surface, ordered_ids)
            saved = record["saved"]
            self.assertTrue(record["live_matches_forward"])
            self.assertTrue(record["live_dispositions_match_forward"])
            self.assertEqual(set(record["source_finance_ids"]), expected_finance)
            publications = [row["finding"] for row in saved["publications"]]
            finance_outputs = [row for row in publications if {"role": "computation", "id": FINANCE_RULE,
                                                               "version": "v1"} in row.get("pins", [])]
            consumer_outputs = [row for row in publications if {"role": "computation", "id": MEMBERSHIP_RULE,
                                                                "version": "v1"} in row.get("pins", [])]
            blocked = [row for row in saved["recorded_blocked_dependencies"]
                       if row.get("artifact_id") == MEMBERSHIP_RULE]
            producer_blocked = [row for row in saved["recorded_blocked_dependencies"]
                                if row.get("artifact_id") == FINANCE_RULE]
            produced_subjects = {
                pin["id"] for row in finance_outputs + producer_blocked
                for pin in row.get("pins", []) if pin.get("role") == "input"
                and pin["id"] in expected_finance
            }
            self.assertEqual(produced_subjects, expected_finance)
            missing_refs = {missing for row in blocked for missing in row.get("missing", [])}
            if label == "track11-consumer-first":
                self.assertTrue(blocked)
                self.assertEqual(missing_refs, {FINANCE_RESULT})
                self.assertNotEqual(forward, reference)
            else:
                self.assertFalse(blocked)
                self.assertEqual(forward, reference)
                self._assert_complete_subject_pins(saved, consumer_outputs, finance_outputs)
            observed.append((label, expected_finance, produced_subjects,
                             {row["id"] for row in consumer_outputs}))

        self.assertEqual(observed[0][1], observed[1][1])
        self.assertEqual(observed[0][2], observed[1][2])
        self.assertNotEqual(execution_orders[0], execution_orders[1],
                            "the two package variants must alter actual resolved rule order")

    def test_available_subset_does_not_prove_expected_financing_membership(self) -> None:
        surface, acts, _types, _school = _track10_live_chain(equal_pair=True)
        # The two independent-school financing rows for A/B remain current but
        # their producer cannot publish after the schooling source is retracted.
        # C's only financing claim is itself retracted, leaving an empty source
        # set for its still-current statement-membership subject.
        acts.append(act(len(acts), "finding-retracted", {
            "finding_id": "demo.finding.track10.school.independent",
        }))
        acts.append(act(len(acts), "finding-retracted", {
            "finding_id": "demo.finding.track10.financing.3",
        }))
        ordered_ids = _reseal(surface, acts, reverse=False)
        record, forward, reference = _execute_track11("track11-partial-and-empty", acts, surface, ordered_ids)
        saved = record["saved"]
        self.assertEqual(forward, reference)
        expected_finance = set(record["source_finance_ids"])
        self.assertEqual(len(expected_finance), 4)
        publications = [row["finding"] for row in saved["publications"]]
        finance_outputs = [row for row in publications if {"role": "computation", "id": FINANCE_RULE,
                                                           "version": "v1"} in row.get("pins", [])]
        producer_blocked = [row for row in saved["recorded_blocked_dependencies"]
                            if row.get("artifact_id") == FINANCE_RULE]
        consumer_outputs = [row for row in publications if {"role": "computation", "id": MEMBERSHIP_RULE,
                                                            "version": "v1"} in row.get("pins", [])]
        produced_subjects = {
            pin["id"] for row in finance_outputs + producer_blocked
            for pin in row.get("pins", []) if pin.get("role") == "input" and pin["id"] in expected_finance
        }
        self.assertEqual(produced_subjects, expected_finance)
        self.assertEqual(len(finance_outputs), 2)
        self.assertEqual(len(producer_blocked), 2)

        for borrowing in ("demo.track8.borrowing.a", "demo.track8.borrowing.b"):
            result = next(row for row in consumer_outputs if f"borrowing={borrowing}" in row["symbol"])
            consumed = [pin["id"] for pin in result.get("pins", []) if pin.get("role") == "input"
                        and pin["id"] in {row["id"] for row in finance_outputs}]
            self.assertEqual(len(consumed), 1)
        c_row = next((row for row in consumer_outputs if "borrowing=demo.track10.borrowing.c" in row["symbol"]), None)
        c_block = [row for row in saved["recorded_blocked_dependencies"]
                   if row.get("artifact_id") == MEMBERSHIP_RULE
                   and "borrowing=demo.track10.borrowing.c" in str(row.get("symbol"))]
        self.assertIsNone(c_row)
        self.assertTrue(c_block)
        self.assertEqual({missing for row in c_block for missing in row.get("missing", [])}, {FINANCE_RESULT})

    def test_numeric_expected_and_available_witnesses_preserve_expected_members(self) -> None:
        from tests.test_sli_track10_saved_account_evidence import _append_contributed_claim

        def prepare(*, corrected: bool, consumer_first: bool) -> tuple[Any, list[dict[str, Any]], tuple[str, ...]]:
            surface, acts, _types, school = _track10_live_chain(equal_pair=True)
            if corrected:
                correction = dict(school)
                correction.update({
                    "id": "demo.finding.track11.readiness.school.shared.corrected",
                    "value": "demo.schooling.corrected-observation",
                    "evidence_ids": ["demo.evidence.track11.readiness.school.shared.corrected"],
                    "contribution_id": "demo.contribution.track11.readiness.school.shared.corrected",
                })
                _append_contributed_claim(acts, DerivationSchemas().registry, correction,
                                          correction["evidence_ids"][0], correction["contribution_id"])
            return surface, acts, _reseal_readiness_candidate(surface, acts,
                                                               consumer_first=consumer_first)

        def rule_rows(saved: dict[str, Any], rule_id: str) -> list[dict[str, Any]]:
            return [row["finding"] for row in saved["publications"]
                    if {"role": "computation", "id": rule_id, "version": "v1"}
                    in row["finding"].get("pins", [])]

        def assert_positive(record: dict[str, Any], borrowing: str,
                            value: str) -> dict[str, Any]:
            saved = record["saved"]
            supports = {row["finding"]["id"]: row for row in saved["evaluated_support"]}
            source_map = record["source_finance_map"]
            source_ids = {finding_id for finding_id, keys in source_map.items()
                          if keys.get("borrowing") == borrowing}
            self.assertEqual(len(source_ids), 2 if borrowing != "demo.track10.borrowing.c" else 1)
            for finding_id in source_ids:
                source = supports[finding_id]
                self.assertEqual(source["fact"]["fact_type_id"], FINANCE)
                self.assertEqual(source["fact"]["fact_id"], source_map[finding_id]["fact_id"])
                self.assertEqual(source["fact"]["bindings"],
                                 {key: val for key, val in source_map[finding_id].items()
                                  if key != "fact_id"})

            finance_rows = [row for row in rule_rows(saved, FINANCE_RULE)
                            if any(pin.get("id") in source_ids for pin in row.get("pins", []))]
            expected_rows = [row for row in rule_rows(saved, EXPECTED_RULE)
                             if any(pin.get("id") in source_ids for pin in row.get("pins", []))]
            available_rows = [row for row in rule_rows(saved, AVAILABLE_RULE)
                              if any(pin.get("id") in source_ids for pin in row.get("pins", []))]
            self.assertEqual((len(finance_rows), len(expected_rows), len(available_rows)),
                             (len(source_ids), len(source_ids), len(source_ids)))
            finance_ids = {row["id"] for row in finance_rows}
            expected_input_ids = {
                pin["id"] for row in expected_rows for pin in row.get("pins", [])
                if pin.get("role") == "input" and pin["id"] in source_ids
            }
            self.assertEqual(expected_input_ids, source_ids)
            self.assertEqual({pin["id"] for row in available_rows for pin in row.get("pins", [])
                              if pin.get("role") == "input" and pin["id"] in source_ids}, source_ids)
            self.assertEqual({pin["id"] for row in finance_rows for pin in row.get("pins", [])
                              if pin.get("role") == "input" and pin["id"] in source_ids}, source_ids)
            for row in finance_rows:
                direct = {pin["id"] for pin in row.get("pins", []) if pin.get("role") == "input"}
                raw_source = direct & source_ids
                self.assertEqual(len(raw_source), 1)
                keys = source_map[next(iter(raw_source))]
                expected_school = {finding_id for finding_id, support in supports.items()
                                   if support["fact"]["fact_type_id"] == SCHOOL
                                   and support["fact"]["bindings"].get("situation") == keys["situation"]}
                self.assertEqual(direct, raw_source | expected_school)
            for row in expected_rows:
                direct = {pin["id"] for pin in row.get("pins", []) if pin.get("role") == "input"}
                self.assertEqual(len(direct & source_ids), 1)
                self.assertEqual(direct, direct & source_ids)
            for row in available_rows:
                direct = {pin["id"] for pin in row.get("pins", []) if pin.get("role") == "input"}
                raw_source = direct & source_ids
                self.assertEqual(len(raw_source), 1)
                matching_finance = {item["id"] for item in finance_rows
                                    if any(pin.get("id") in raw_source for pin in item.get("pins", []))}
                self.assertEqual(direct, raw_source | matching_finance)

            consumer = next(row for row in rule_rows(saved, MEMBERSHIP_RULE)
                            if f"borrowing={borrowing}" in row["symbol"])
            member_source = next(pin["id"] for pin in consumer.get("pins", [])
                                 if pin.get("role") == "input"
                                 and pin["id"].startswith("demo.finding.track10.membership."))
            expected_inputs = {member_source, *finance_ids,
                               *(row["id"] for row in expected_rows + available_rows)}
            direct_inputs = {pin["id"] for pin in consumer.get("pins", []) if pin.get("role") == "input"}
            self.assertEqual(direct_inputs, expected_inputs)
            self.assertEqual(consumer["value"], value)

            situations = {source_map[finding_id]["situation"] for finding_id in source_ids}
            school_ids = {finding_id for finding_id, row in supports.items()
                          if row["fact"]["fact_type_id"] == SCHOOL
                          and row["fact"]["bindings"].get("situation") in situations}
            self.assertEqual(_saved_source_closure(saved, consumer["id"]),
                             {member_source, *source_ids, *school_ids})
            return consumer

        equal_surface, equal_acts, equal_order = prepare(corrected=False, consumer_first=True)
        equal, equal_forward, equal_reference = _execute_track11(
            "track11-readiness-equal", equal_acts, equal_surface, equal_order,
        )
        self.assertEqual(equal_forward, equal_reference)
        self.assertTrue(equal["live_matches_forward"])
        self.assertTrue(equal["live_dispositions_match_forward"])
        self.assertEqual(set(equal["source_finance_ids"]), _current_source_members(equal_acts))
        self.assertEqual(len(rule_rows(equal["saved"], EXPECTED_RULE)), 5)
        self.assertEqual(len(rule_rows(equal["saved"], AVAILABLE_RULE)), 5)
        equal_a = assert_positive(equal, "demo.track8.borrowing.a", "true")
        equal_b = assert_positive(equal, "demo.track8.borrowing.b", "true")
        equal_c = assert_positive(equal, "demo.track10.borrowing.c", "true")

        corrected_first_surface, corrected_first_acts, corrected_first_order = prepare(
            corrected=True, consumer_first=True)
        corrected_first, first_forward, first_reference = _execute_track11(
            "track11-readiness-corrected-consumer-first", corrected_first_acts,
            corrected_first_surface, corrected_first_order,
        )
        self.assertEqual(first_forward, first_reference)
        self.assertTrue(corrected_first["live_matches_forward"])
        corrected_first_a = assert_positive(corrected_first, "demo.track8.borrowing.a", "false")
        corrected_first_b = assert_positive(corrected_first, "demo.track8.borrowing.b", "false")
        corrected_first_c = assert_positive(corrected_first, "demo.track10.borrowing.c", "true")

        corrected_last_surface, corrected_last_acts, corrected_last_order = prepare(
            corrected=True, consumer_first=False)
        corrected_last, last_forward, last_reference = _execute_track11(
            "track11-readiness-corrected-producer-first", corrected_last_acts,
            corrected_last_surface, corrected_last_order,
        )
        self.assertEqual(last_forward, last_reference)
        self.assertTrue(corrected_last["live_matches_forward"])
        corrected_last_a = assert_positive(corrected_last, "demo.track8.borrowing.a", "false")
        corrected_last_b = assert_positive(corrected_last, "demo.track8.borrowing.b", "false")
        corrected_last_c = assert_positive(corrected_last, "demo.track10.borrowing.c", "true")
        self.assertNotEqual(corrected_first["resolved_rule_sequence"],
                            corrected_last["resolved_rule_sequence"])
        self.assertEqual((corrected_first_a["value"], corrected_first_b["value"],
                          corrected_first_c["value"]),
                         (corrected_last_a["value"], corrected_last_b["value"],
                          corrected_last_c["value"]))
        self.assertLess(corrected_first["resolved_rule_sequence"].index(MEMBERSHIP_RULE),
                        corrected_first["resolved_rule_sequence"].index(EXPECTED_RULE))
        self.assertLess(corrected_last["resolved_rule_sequence"].index(EXPECTED_RULE),
                        corrected_last["resolved_rule_sequence"].index(MEMBERSHIP_RULE))
        self.assertEqual(corrected_first_a, corrected_last_a)
        self.assertEqual(corrected_first_b, corrected_last_b)
        self.assertEqual(corrected_first_c, corrected_last_c)
        self.assertEqual(equal_c, corrected_first_c)

        retract_shared = act(len(corrected_last_acts), "finding-retracted", {
            "finding_id": "demo.finding.track11.readiness.school.shared.corrected",
        })
        corrected_last_acts.append(retract_shared)
        retracted, retract_forward, retract_reference = _execute_track11(
            "track11-readiness-shared-retracted", corrected_last_acts,
            corrected_last_surface, corrected_last_order,
        )
        self.assertEqual(retract_forward, retract_reference)
        retracted_c = assert_positive(retracted, "demo.track10.borrowing.c", "true")
        self.assertEqual(equal_c, retracted_c)
        retracted_blocked = [row for row in retracted["saved"]["recorded_blocked_dependencies"]
                             if row.get("artifact_id") == MEMBERSHIP_RULE]
        self.assertEqual(len(retracted_blocked), 2)
        for borrowing in ("demo.track8.borrowing.a", "demo.track8.borrowing.b"):
            blocked = next(row for row in retracted_blocked if f"borrowing={borrowing}" in row["symbol"])
            self.assertEqual((blocked["code"], blocked["missing"]), ("DEPENDENCY_INVALID", []))
            source_ids = {finding_id for finding_id, keys in retracted["source_finance_map"].items()
                          if keys.get("borrowing") == borrowing}
            expected_for_subject = {row["id"] for row in rule_rows(retracted["saved"], EXPECTED_RULE)
                                    if any(pin.get("id") in source_ids for pin in row.get("pins", []))}
            available_for_subject = {row["id"] for row in rule_rows(retracted["saved"], AVAILABLE_RULE)
                                     if any(pin.get("id") in source_ids for pin in row.get("pins", []))}
            membership_source = next(pin["id"] for pin in blocked["pins"]
                                     if pin.get("role") == "input"
                                     and pin["id"].startswith("demo.finding.track10.membership."))
            direct_ids = {pin["id"] for pin in blocked["pins"] if pin.get("role") == "input"}
            self.assertEqual(direct_ids, {membership_source, *expected_for_subject, *available_for_subject})
            self.assertFalse(direct_ids & {row["id"] for row in rule_rows(retracted["saved"], FINANCE_RULE)})
            situations = {retracted["source_finance_map"][item]["situation"] for item in source_ids}
            support_rows = {row["finding"]["id"]: row for row in retracted["saved"]["evaluated_support"]}
            schools = {finding_id for finding_id, row in support_rows.items()
                       if row["fact"]["fact_type_id"] == SCHOOL
                       and row["fact"]["bindings"].get("situation") in situations}
            self.assertEqual(_saved_input_closure(retracted["saved"], blocked["pins"]),
                             {membership_source, *source_ids, *schools})
        self.assertNotIn("demo.finding.track11.readiness.school.shared.corrected",
                         {pin["id"] for row in retracted["saved"]["publications"]
                          for pin in row["finding"].get("pins", []) if pin.get("role") == "input"})

        partial_surface, partial_acts, partial_order = prepare(corrected=False, consumer_first=False)
        partial_acts.append(act(len(partial_acts), "finding-retracted", {
            "finding_id": "demo.finding.track10.school.independent",
        }))
        partial, partial_forward, partial_reference = _execute_track11(
            "track11-readiness-independent-school-retracted", partial_acts,
            partial_surface, partial_order,
        )
        self.assertEqual(partial_forward, partial_reference)
        partial_blocked = [row for row in partial["saved"]["recorded_blocked_dependencies"]
                           if row.get("artifact_id") == MEMBERSHIP_RULE]
        self.assertEqual(len(partial_blocked), 3)
        for borrowing in ("demo.track8.borrowing.a", "demo.track8.borrowing.b"):
            blocked = next(row for row in partial_blocked if f"borrowing={borrowing}" in row["symbol"])
            self.assertEqual((blocked["code"], blocked["missing"]), ("DEPENDENCY_INVALID", []))
            support_ids = {row["finding"]["id"] for row in partial["saved"]["evaluated_support"]}
            pins = [pin for pin in blocked.get("pins", []) if pin.get("role") == "input"]
            self.assertTrue(pins)
            input_ids = {pin["id"] for pin in pins}
            self.assertNotIn("demo.finding.track10.school.independent", input_ids)
            self.assertEqual(len(input_ids & {row["id"] for row in rule_rows(partial["saved"], EXPECTED_RULE)}), 2)
            self.assertEqual(len(input_ids & {row["id"] for row in rule_rows(partial["saved"], AVAILABLE_RULE)}), 1)
            self.assertFalse(input_ids & {row["id"] for row in rule_rows(partial["saved"], FINANCE_RULE)})
            self.assertTrue(input_ids & support_ids)
            source_ids = {finding_id for finding_id, keys in partial["source_finance_map"].items()
                          if keys.get("borrowing") == borrowing}
            member_source = next(pin["id"] for pin in pins
                                 if pin["id"].startswith("demo.finding.track10.membership."))
            expected_for_subject = {row["id"] for row in rule_rows(partial["saved"], EXPECTED_RULE)
                                    if any(pin.get("id") in source_ids for pin in row.get("pins", []))}
            available_for_subject = {row["id"] for row in rule_rows(partial["saved"], AVAILABLE_RULE)
                                     if any(pin.get("id") in source_ids for pin in row.get("pins", []))}
            self.assertEqual(input_ids, {member_source, *expected_for_subject, *available_for_subject})
            situations = {partial["source_finance_map"][finding_id]["situation"] for finding_id in source_ids}
            school_ids = {finding_id for finding_id, row in
                          ((item["finding"]["id"], item) for item in partial["saved"]["evaluated_support"])
                          if row["fact"]["fact_type_id"] == SCHOOL
                          and row["fact"]["bindings"].get("situation") in situations}
            self.assertEqual(_saved_input_closure(partial["saved"], blocked["pins"]),
                             {member_source, *source_ids, *school_ids})
        c_block = next(row for row in partial_blocked if "borrowing=demo.track10.borrowing.c" in row["symbol"])
        self.assertEqual((c_block["code"], c_block["missing"]),
                         ("DEPENDENCY_ABSENT", [AVAILABLE]))

        empty_surface, empty_acts, empty_order = prepare(corrected=False, consumer_first=False)
        empty_acts.append(act(len(empty_acts), "finding-retracted", {
            "finding_id": "demo.finding.track10.financing.3",
        }))
        empty, empty_forward, empty_reference = _execute_track11(
            "track11-readiness-empty-c", empty_acts, empty_surface, empty_order,
        )
        self.assertEqual(empty_forward, empty_reference)
        c_block = next(row for row in empty["saved"]["recorded_blocked_dependencies"]
                       if row.get("artifact_id") == MEMBERSHIP_RULE
                       and "borrowing=demo.track10.borrowing.c" in row.get("symbol", ""))
        self.assertEqual((c_block["code"], c_block["missing"]),
                         ("DEPENDENCY_ABSENT", [EXPECTED, AVAILABLE]))
        self.assertEqual({pin["id"] for pin in c_block["pins"] if pin.get("role") == "input"},
                         {"demo.finding.track10.membership.2"})

    def _assert_complete_subject_pins(self, saved: dict[str, Any], consumer_rows: list[dict[str, Any]],
                                      finance_rows: list[dict[str, Any]]) -> None:
        available_publications = {row["finding"]["id"] for row in saved["publications"]}
        support_ids = {row["finding"]["id"] for row in saved["evaluated_support"]}
        for result in consumer_rows:
            borrowing = result["symbol"].split("borrowing=", 1)[1]
            membership_source = next(
                pin["id"] for pin in result.get("pins", [])
                if pin.get("role") == "input" and pin["id"].startswith("demo.finding.track10.membership.")
            )
            expected_finance_rows = [row for row in finance_rows if f"borrowing={borrowing}," in row["symbol"]]
            expected_direct = {membership_source, *(row["id"] for row in expected_finance_rows)}
            actual_direct = {pin["id"] for pin in result.get("pins", []) if pin.get("role") == "input"}
            self.assertEqual(actual_direct, expected_direct)
            self.assertTrue(expected_direct.issubset(available_publications | support_ids))
            self.assertEqual(result["value"], "false" if len(expected_finance_rows) == 2 else "true")
            for finance in expected_finance_rows:
                source_pins = {pin["id"] for pin in finance.get("pins", []) if pin.get("role") == "input"}
                self.assertEqual(len(source_pins), 2)
                self.assertTrue(any(item.startswith("demo.finding.track10.financing.") for item in source_pins))
                self.assertTrue(source_pins.issubset(support_ids))


if __name__ == "__main__":
    unittest.main()
