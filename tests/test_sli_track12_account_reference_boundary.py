"""Track 12: supplied account references do not assert relationship claims."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas, workspace_registry
from packages.tax.loader import install_domain_scoped_supersession
from packages.kernel.act_log import ActLog
from packages.kernel.contribution import apply_contribution_batch
from packages.kernel.currency import compute_currency
from packages.kernel.facts import facts_of, fact_id_for
from packages.kernel.findings import project
from tests.test_sli_track10_saved_account_evidence import (
    FINANCE, FINANCE_RESULT, FINANCE_RULE, MEMBERSHIP, MEMBERSHIP_RULE,
    SCHOOL, ROOT, _track10_live_chain,
)
from tests.test_sli_track8_relationship_evidence import _runner_parity, generator_surface
from tests.support import act, demo_entity, demo_evidence
from tools.sli_saved_account_evidence import capture, dumps, loads

ACCOUNT = "demo.sli.track12.account"
ACCOUNT_ID = "demo.sli.track12.account.references-present"
ACCOUNT_FINDING = "demo.finding.sli.track12.account.references-present"
ACCOUNT_CONTRIBUTION = "demo.contribution.sli.track12.account.references-present"
ACCOUNT_EVIDENCE = "demo.evidence.sli.track12.account.references-present"
ACCOUNT_REF_RESULT = "demo.sli.track12.account-borrowing-reference"
ACCOUNT_REF_RULE = "demo.rule.sli.track12.account-borrowing-reference"
ACCOUNT_FINANCE_RULE = "demo.rule.sli.track12.account-finance-diagnostic"
TRACK11_EXPECTED = "demo.rule.sli.track11.financing-expected"
TRACK11_AVAILABLE = "demo.rule.sli.track11.financing-available"


def _account_type(track9: Any) -> dict[str, Any]:
    return cast(dict[str, Any], track9._fact_type() | {"id": ACCOUNT})


def _account_value(*, borrowing: str | None, schooling: str | None, statement: str | None,
                   unresolved: bool = False) -> dict[str, Any]:
    return {
        "borrowing_identity": "unknown" if unresolved else "known",
        "schooling_fact": "missing" if unresolved else "supplied",
        "statement_scope": "unknown" if unresolved else "known",
        "supplied_claim": ("synthetic answer supplied; connection not identified" if unresolved
                           else "synthetic supplied references; relationship not asserted"),
        "borrowing_reference": borrowing,
        "schooling_reference": schooling,
        "statement_reference": statement,
    }


def _append_account(acts: list[dict[str, Any]], registry: Any, value: dict[str, Any]) -> None:
    acts.append(act(len(acts), "entity-introduced", {"entity": demo_entity(
        ACCOUNT_ID, "Synthetic relationship account", "demo.sli-relationship-account")}))
    acts.append(act(len(acts), "evidence-submitted", {"evidence": demo_evidence(
        ACCOUNT_EVIDENCE, "Synthetic supplied account references", {"claim": value["supplied_claim"]})}))
    contribution = act(len(acts), "contribution", {"contribution": {
        "schema": "contribution.v1", "id": ACCOUNT_CONTRIBUTION,
        "evidence_id": ACCOUNT_EVIDENCE,
        "content": {"mode": "manual-entry", "synthetic": True},
    }})
    finding = {
        "schema": "finding.v2", "id": ACCOUNT_FINDING,
        "fact_id": fact_id_for(ACCOUNT, (("account", ACCOUNT_ID), ("tax-year", "2025"))),
        "value": value, "basis": "attested", "evidence_ids": [ACCOUNT_EVIDENCE],
        "contribution_id": ACCOUNT_CONTRIBUTION,
    }
    assertion = act(len(acts) + 1, "assertion", {"finding": finding})
    base = project(tuple(copy.deepcopy(row) for row in acts), registry)
    admitted = apply_contribution_batch(base, contribution_act=contribution,
                                        successor_acts=[assertion], registry=registry,
                                        record_id="demo.contribution-record.sli.track12.account")
    if admitted.terminal_record["phase"] != "completed":
        raise AssertionError(f"account contribution admission failed: {admitted.terminal_record}")
    acts.extend((contribution, assertion))


def _correct_account(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    updated = copy.deepcopy(acts)
    adoption = updated.pop()
    evidence_id = "demo.evidence.sli.track12.account.corrected"
    contribution_id = "demo.contribution.sli.track12.account.corrected"
    finding_id = "demo.finding.sli.track12.account.corrected"
    updated.append(act(len(updated), "evidence-submitted", {"evidence": demo_evidence(
        evidence_id, "Synthetic corrected account reference", {"claim": "corrected synthetic borrowing reference"})}))
    contribution = act(len(updated), "contribution", {"contribution": {
        "schema": "contribution.v1", "id": contribution_id, "evidence_id": evidence_id,
        "content": {"mode": "manual-entry", "synthetic": True},
    }})
    finding = {
        "schema": "finding.v2", "id": finding_id,
        "fact_id": fact_id_for(ACCOUNT, (("account", ACCOUNT_ID), ("tax-year", "2025"))),
        "value": _account_value(
            borrowing="demo.track8.borrowing.b",
            schooling="demo.sli.track10.schooling|situation=demo.sli.schooling.shared,period=2024,"
            "institution=demo.sli.schooling.institution.shared,programme=demo.sli.schooling.programme.shared",
            statement="tax.us.2025.f1098e.box1-student-loan-interest|lender=demo.lender.reader.s1,"
            "statement=demo.statement.reader.s1,tax-year=2025",
        ),
        "basis": "attested", "evidence_ids": [evidence_id], "contribution_id": contribution_id,
    }
    assertion = act(len(updated) + 1, "assertion", {"finding": finding})
    registry = DerivationSchemas().registry
    base = project(tuple(copy.deepcopy(row) for row in updated), registry)
    admitted = apply_contribution_batch(base, contribution_act=contribution,
                                        successor_acts=[assertion], registry=registry,
                                        record_id="demo.contribution-record.sli.track12.account.corrected")
    if admitted.terminal_record["phase"] != "completed":
        raise AssertionError(f"account correction admission failed: {admitted.terminal_record}")
    updated.extend((contribution, assertion))
    adoption["committed_against"] = len(updated)
    updated.append(adoption)
    return updated


def _assemble_reference_only_case(*, include_relationship_claims: bool = False,
                                  unresolved_account: bool = False,
                                  equal_pair: bool = False,
                                  include_diagnostic: bool | None = None) -> tuple[Any, list[dict[str, Any]]]:
    """Extend the Track 10 package while omitting FINANCE/MEMBERSHIP claims pre-admission."""
    import importlib.util
    import sys

    track10 = sys.modules["tests.test_sli_track10_saved_account_evidence"]
    track10 = cast(Any, track10)
    track8 = track10._track8()
    generator = track8._track6b_generator()
    track9_spec = importlib.util.spec_from_file_location(
        "track12_track9_account_vocabulary", ROOT / "tests" / "test_sli_track9_recording_state.py")
    assert track9_spec and track9_spec.loader
    track9 = importlib.util.module_from_spec(track9_spec)
    sys.modules[track9_spec.name] = track9
    track9_spec.loader.exec_module(track9)

    original_members = generator._package_members
    original_seal = generator._seal_disposable_reader_package
    original_track8_factory = track10._track8
    account_type = _account_type(track9)
    account_ref_type = {
        "schema": "fact-type.v2", "id": ACCOUNT_REF_RESULT, "version": "v1",
        "title": "Synthetic supplied borrowing reference read", "nature": "determinable",
        "identity_keys": copy.deepcopy(account_type["identity_keys"]),
        "value_schema": {"type": "string"}, "supersession": {"policy": "free"},
    }
    account_ref_rule = generator._reader_rule(
        ACCOUNT_REF_RULE, ACCOUNT_REF_RESULT, subject=ACCOUNT,
        value={"op": "ref", "name": ACCOUNT, "field": "borrowing_reference"},
    )
    reference_guards = {"op": "all", "args": [
        {"op": "ref", "name": ACCOUNT, "field": "borrowing_reference"},
        {"op": "ref", "name": ACCOUNT, "field": "schooling_reference"},
        {"op": "ref", "name": ACCOUNT, "field": "statement_reference"},
    ]}
    account_finance_rule = generator._reader_rule(
        ACCOUNT_FINANCE_RULE, FINANCE, subject=ACCOUNT, when=reference_guards,
        value={"op": "category_literal", "fact_type": {"id": FINANCE, "version": "v1"},
               "value": "demo.financing.observed"},
    )

    def extended_members() -> tuple[list[tuple[dict[str, Any], str]], list[dict[str, str]]]:
        members, entrypoints = original_members()
        for index, (citizen, kind) in enumerate(members):
            if citizen.get("id") == generator.CLAIM_BUNDLE:
                replacement = dict(citizen)
                replacement["fact_types"] = list(citizen["fact_types"]) + [account_type, account_ref_type]
                members[index] = (replacement, kind)
                break
        additions = [(account_ref_rule, "computation")]
        if include_diagnostic if include_diagnostic is not None else not include_relationship_claims:
            additions.append((account_finance_rule, "computation"))
        members.extend(additions)
        entrypoints.extend({"id": row["id"], "version": row["version"]} for row, _ in additions)
        return members, entrypoints

    def seal_with_account(surface: Any) -> Any:
        package_path = surface.members / generator.PACKAGE_FILE
        package = json.loads(package_path.read_text("utf-8"))
        package["input_bindings"].append({
            "symbol": ACCOUNT, "fact_type": {"id": ACCOUNT, "version": "v1"}, "mode": "required",
        })
        package_path.write_bytes(generator._bytes(package))
        return original_seal(surface)

    generator._package_members = extended_members
    generator._seal_disposable_reader_package = seal_with_account
    original_append = track10._append_contributed_claim

    def omit_relationship_claims(acts: list[dict[str, Any]], registry: Any, finding: dict[str, Any],
                                evidence_id: str, contribution_id: str) -> None:
        fact_type = str(finding["fact_id"]).split("|", 1)[0]
        if fact_type in {FINANCE, MEMBERSHIP} or (unresolved_account and fact_type == SCHOOL):
            return
        original_append(acts, registry, finding, evidence_id, contribution_id)

    if not include_relationship_claims:
        track10._append_contributed_claim = omit_relationship_claims
    class Track8Proxy:
        _track6b_generator = staticmethod(lambda: generator)
        _prototype_relationship_acts = staticmethod(track8._prototype_relationship_acts)

    track10._track8 = lambda: Track8Proxy
    try:
        surface, acts, types, school = _track10_live_chain(equal_pair=equal_pair)
    finally:
        generator._package_members = original_members
        generator._seal_disposable_reader_package = original_seal
        track10._append_contributed_claim = original_append
        track10._track8 = original_track8_factory

    registry = DerivationSchemas().registry
    school_fact_id = fact_id_for(SCHOOL, (
        ("situation", "demo.sli.schooling.shared"), ("period", "2024"),
        ("institution", "demo.sli.schooling.institution.shared"),
        ("programme", "demo.sli.schooling.programme.shared"),
    ))
    statement_fact_id = (
        f"tax.us.2025.f1098e.box1-student-loan-interest|lender=demo.lender.reader.s1,"
        "statement=demo.statement.reader.s1,tax-year=2025"
    )
    account_value = _account_value(
        borrowing=None if unresolved_account else "demo.track8.borrowing.a",
        schooling=None if unresolved_account else school_fact_id,
        statement=None if unresolved_account else statement_fact_id,
        unresolved=unresolved_account,
    )
    adoption = acts.pop()
    _append_account(acts, registry, account_value)
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    acts = track8._track6b_generator()._renumber(acts)
    return surface, acts


class AccountReferenceBoundary(unittest.TestCase):
    def test_unresolved_answer_keeps_missing_fact_unknown_connection_and_unadopted_treatment_separate(self) -> None:
        surface, acts = _assemble_reference_only_case(unresolved_account=True)
        with tempfile.TemporaryDirectory(prefix="track12-unresolved-") as raw:
            root = Path(raw)
            log = ActLog(root / "authoritative", install_domain_scoped_supersession(workspace_registry()))
            for item in acts:
                log.append(item, expected_revision=item["committed_against"])
            recovered = ActLog(root / "authoritative", workspace_registry(), read_only=True).read().acts
            state = project(tuple(copy.deepcopy(row) for row in recovered), DerivationSchemas().registry)
            currency = compute_currency(state)
            lattice = facts_of(state.fact_state)
            current = {key: row for key, row in state.findings.items()
                       if key in currency.current_finding_ids}
            account = current[ACCOUNT_FINDING]
            self.assertEqual(account["value"]["borrowing_identity"], "unknown")
            self.assertEqual(account["value"]["schooling_fact"], "missing")
            self.assertEqual(account["value"]["statement_scope"], "unknown")
            self.assertEqual([account["value"][key] for key in (
                "borrowing_reference", "schooling_reference", "statement_reference")], [None, None, None])
            self.assertEqual(account["evidence_ids"], [ACCOUNT_EVIDENCE])
            self.assertFalse(any(row["fact_id"].startswith(f"{SCHOOL}|")
                                 for key, row in current.items()))
            forward, reference = _runner_parity(list(recovered), surface)
            self.assertEqual(forward, reference)
            generator = __import__(
                "tests.test_sli_track8_relationship_evidence", fromlist=["_track6b_generator"]
            )._track6b_generator()
            outcome = live_coordinate_run(
                WorkspaceCapability(root / "live"), repo_root=ROOT,
                authoritative_acts=recovered, workspace_revision=len(recovered),
                run_scope={"jurisdiction": "us", "year": "2025"}, scope_user=generator.USER,
                request={"schema": "run-request.v1"}, run_id="demo.track12.unresolved-account",
                governance_pins=[], surface=generator_surface(surface), output_name="unresolved.json",
            )
            self.assertIsNone(outcome.refusal)
            assert outcome.output_path is not None and outcome.publications is not None
            output = json.loads(outcome.output_path.read_text("utf-8"))
            live_publications = sorted(
                [(row.finding["symbol"], row.finding.get("value"), row.finding.get("pins"))
                 for row in outcome.publications], key=lambda row: json.dumps(row, sort_keys=True))
            self.assertEqual(live_publications, forward["publications"])
            live_dispositions = sorted(
                [(row.get("artifact_id"), row.get("symbol"), row["disposition"], row.get("finding_id"),
                  row.get("code"), row.get("missing")) for row in output["dispositions"]],
                key=lambda row: json.dumps(row, sort_keys=True),
            )
            self.assertEqual(live_dispositions, forward["dispositions"])
            package_pin = next(pin for publication in outcome.publications
                               for pin in publication.finding["pins"] if pin.get("role") == "adoption")
            saved_doc = capture(
                run_id=outcome.run_id or "", package=package_pin, publications=outcome.publications,
                dispositions=output["dispositions"], current_findings=current,
                fact_keys={fact_id: {"fact_type_id": fact.fact_type_id, "bindings": dict(fact.keys),
                                     "individuated_by": list(fact.individuated_by)}
                           for fact_id, fact in lattice.items()},
                evidence_by_id={key: row.evidence for key, row in state.evidence.items()},
                selected_producer_ids=(ACCOUNT_REF_RULE, ACCOUNT_FINANCE_RULE, FINANCE_RULE, MEMBERSHIP_RULE),
                all_findings=state.findings,
                displacement_reasons={finding_id: [{"kind": reason.kind, "by": reason.by}
                                                   for reason in reasons]
                                      for finding_id, reasons in currency.reasons.items()},
                experiment_metadata={"application_treatment": "unadopted"},
            )
            path = ROOT / "temp" / "track12" / "unresolved-account.saved-account.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(dumps(saved_doc))
            del outcome, state, current, lattice, recovered, log
        reopened = loads(path.read_bytes())
        self.assertTrue(any(row["finding"]["id"] == ACCOUNT_FINDING
                            and row["finding"]["value"]["borrowing_reference"] is None
                            for row in reopened["evaluated_support"]))
        self.assertEqual(reopened["experiment_metadata"]["application_treatment"], "unadopted")
        from tests.test_sli_track11_collection_declarations import _saved_input_closure

        saved_publications = {row["finding"]["id"]: row["finding"] for row in reopened["publications"]}
        for finding_id in reopened["scope"]["selected_publication_ids"]:
            self.assertIn(ACCOUNT_FINDING, _saved_input_closure(
                reopened, saved_publications[finding_id].get("pins", [])))

    def test_references_read_as_account_context_and_do_not_construct_financing(self) -> None:
        surface, acts = _assemble_reference_only_case()
        schooling_target = fact_id_for(SCHOOL, (
            ("situation", "demo.sli.schooling.shared"), ("period", "2024"),
            ("institution", "demo.sli.schooling.institution.shared"),
            ("programme", "demo.sli.schooling.programme.shared"),
        ))

        with tempfile.TemporaryDirectory(prefix="track12-reference-only-") as raw:
            root = Path(raw)
            log = ActLog(root / "authoritative", install_domain_scoped_supersession(workspace_registry()))
            for item in acts:
                log.append(item, expected_revision=item["committed_against"])
            recovered = ActLog(root / "authoritative", workspace_registry(), read_only=True).read().acts
            state = project(tuple(copy.deepcopy(row) for row in recovered), DerivationSchemas().registry)
            currency = compute_currency(state)
            lattice = facts_of(state.fact_state)
            current = {key: row for key, row in state.findings.items()
                       if key in currency.current_finding_ids}
            self.assertIn(ACCOUNT_FINDING, current)
            self.assertFalse(any(finding["fact_id"].startswith(f"{FINANCE}|") for finding in current.values()))
            self.assertFalse(any(finding["fact_id"].startswith(f"{MEMBERSHIP}|") for finding in current.values()))
            self.assertEqual(current[ACCOUNT_FINDING]["evidence_ids"], [ACCOUNT_EVIDENCE])
            self.assertTrue(any(row["fact_id"] == schooling_target for row in current.values()))
            account_statement_target = current[ACCOUNT_FINDING]["value"]["statement_reference"]
            self.assertTrue(any(row["fact_id"] == account_statement_target for row in current.values()))
            self.assertIn("demo.track8.borrowing.a", state.fact_state.entities)
            runner, reference = _runner_parity(list(recovered), surface)
            self.assertEqual(runner, reference)
            ref_publication = next(row for row in runner["publications"]
                                   if row[0].startswith(f"{ACCOUNT_REF_RESULT}|"))
            self.assertEqual(ref_publication[1], "demo.track8.borrowing.a")
            self.assertEqual({pin["id"] for pin in ref_publication[2] if pin.get("role") == "input"},
                             {ACCOUNT_FINDING})
            diagnostic = [row for row in runner["publications"] if row[0].startswith(f"{FINANCE}|")]
            self.assertEqual(len(diagnostic), 1)
            self.assertEqual(diagnostic[0][1], "demo.financing.observed")
            diagnostic_fact_id = diagnostic[0][0].split("|", 1)[1]
            self.assertTrue(diagnostic_fact_id.startswith(f"{ACCOUNT}|"), diagnostic_fact_id)
            self.assertNotIn("borrowing=", diagnostic_fact_id)
            self.assertEqual({pin["id"] for pin in diagnostic[0][2] if pin.get("role") == "input"},
                             {ACCOUNT_FINDING})
            finance_subject_dispositions = [row for row in runner["dispositions"]
                                            if row[0] == FINANCE_RULE]
            expected_subject_symbol = f"{FINANCE_RESULT}|{diagnostic_fact_id}"
            observed_block = next(row for row in finance_subject_dispositions
                                  if row[1] == expected_subject_symbol)
            self.assertEqual(observed_block[2], "blocked")
            self.assertEqual(observed_block[4], "DEPENDENCY_INVALID")
            self.assertEqual(observed_block[5], [SCHOOL])
            account_producer = next(row for row in runner["dispositions"]
                                    if row[0] == ACCOUNT_FINANCE_RULE and row[1] == diagnostic[0][0])
            diagnostic_finding_id = account_producer[3]
            state = project(tuple(copy.deepcopy(row) for row in recovered), DerivationSchemas().registry)
            currency = compute_currency(state)
            lattice = facts_of(state.fact_state)
            current = {key: row for key, row in state.findings.items() if key in currency.current_finding_ids}
            from tests.test_sli_track8_relationship_evidence import _track6b_generator

            generator = _track6b_generator()
            outcome = live_coordinate_run(
                WorkspaceCapability(root / "live"), repo_root=ROOT,
                authoritative_acts=recovered, workspace_revision=len(recovered),
                run_scope={"jurisdiction": "us", "year": "2025"}, scope_user=generator.USER,
                request={"schema": "run-request.v1"}, run_id="demo.track12.references-present",
                governance_pins=[], surface=generator_surface(surface), output_name="references.json",
            )
            self.assertIsNone(outcome.refusal)
            self.assertIsNotNone(outcome.output_path)
            self.assertIsNotNone(outcome.publications)
            assert outcome.output_path is not None and outcome.publications is not None
            output = json.loads(outcome.output_path.read_text("utf-8"))
            live_rows = sorted([(item.finding["symbol"], item.finding.get("value"), item.finding.get("pins"))
                                for item in outcome.publications], key=lambda row: json.dumps(row, sort_keys=True))
            self.assertEqual(live_rows, runner["publications"])
            self.assertEqual(sorted((row.get("artifact_id"), row.get("symbol"), row["disposition"],
                                     row.get("finding_id"), row.get("code"), row.get("missing"))
                                    for row in output["dispositions"]), runner["dispositions"])
            live_block = next(row for row in output["dispositions"]
                              if row.get("artifact_id") == FINANCE_RULE
                              and row.get("symbol") == expected_subject_symbol)
            self.assertEqual(live_block["disposition"], "blocked")
            self.assertEqual(live_block["code"], "DEPENDENCY_INVALID")
            self.assertEqual({pin["id"] for pin in live_block["pins"] if pin.get("role") == "input"},
                             {diagnostic_finding_id})
            package_pin = next(pin for row in outcome.publications for pin in row.finding["pins"]
                               if pin.get("role") == "adoption")
            contextual = {finding_id: finding for finding_id, finding in current.items()
                          if finding["fact_id"] in {schooling_target, account_statement_target}}
            saved = capture(
                run_id=outcome.run_id or "", package=package_pin, publications=outcome.publications,
                dispositions=output["dispositions"], current_findings=current,
                contextual_findings=contextual,
                fact_keys={fact_id: {"fact_type_id": fact.fact_type_id, "bindings": dict(fact.keys),
                                     "individuated_by": list(fact.individuated_by)}
                           for fact_id, fact in lattice.items()},
                evidence_by_id={key: row.evidence for key, row in state.evidence.items()},
                selected_producer_ids=(ACCOUNT_REF_RULE, ACCOUNT_FINANCE_RULE, FINANCE_RULE, MEMBERSHIP_RULE),
                all_findings=state.findings, experiment_metadata={"application_treatment": "unadopted"},
            )
            save_path = ROOT / "temp" / "track12" / "references-present.saved-account.json"
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_bytes(dumps(saved))
            del outcome
            del recovered, log, state, current, lattice
        reopened = loads(save_path.read_bytes())
        self.assertTrue(any(row["finding"]["id"] == ACCOUNT_FINDING for row in reopened["evaluated_support"]))
        self.assertFalse(any(row["fact"]["fact_type_id"] in {FINANCE, MEMBERSHIP}
                             for row in reopened["evaluated_support"]))
        from tests.test_sli_track11_collection_declarations import _saved_input_closure

        saved_publications = {row["finding"]["id"]: row["finding"] for row in reopened["publications"]}
        selected_ids = reopened["scope"]["selected_publication_ids"]
        self.assertTrue(selected_ids)
        for finding_id in selected_ids:
            resolved_leaves = _saved_input_closure(reopened, saved_publications[finding_id].get("pins", []))
            self.assertIn(ACCOUNT_FINDING, resolved_leaves)
        for disposition in reopened["dispositions"]:
            if disposition.get("artifact_id") in {ACCOUNT_FINANCE_RULE, FINANCE_RULE} and disposition.get("pins"):
                self.assertIn(ACCOUNT_FINDING, _saved_input_closure(reopened, disposition["pins"]))
        context_fact_ids = {row["fact"]["fact_id"] for row in reopened["context_only"]}
        self.assertIn(schooling_target, context_fact_ids)
        account_related_pins = {
            pin["id"]
            for row in reopened["publications"]
            if any(pin.get("id") in {ACCOUNT_REF_RULE, ACCOUNT_FINANCE_RULE, FINANCE_RULE}
                   and pin.get("role") == "computation" for pin in row["finding"].get("pins", []))
            for pin in row["finding"].get("pins", []) if pin.get("role") == "input"
        }
        self.assertNotIn(account_statement_target, account_related_pins)

    def test_account_correction_and_retraction_change_only_account_supported_results(self) -> None:
        surface, acts = _assemble_reference_only_case()
        corrected = _correct_account(acts)
        corrected_id = "demo.finding.sli.track12.account.corrected"
        school_id = fact_id_for(SCHOOL, (
            ("situation", "demo.sli.schooling.shared"), ("period", "2024"),
            ("institution", "demo.sli.schooling.institution.shared"),
            ("programme", "demo.sli.schooling.programme.shared"),
        ))

        def run_fresh(name: str, source_acts: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
            with tempfile.TemporaryDirectory(prefix=f"track12-{name}-") as raw:
                root = Path(raw)
                log = ActLog(root / "authoritative", install_domain_scoped_supersession(workspace_registry()))
                for row in source_acts:
                    log.append(row, expected_revision=row["committed_against"])
                recovered = ActLog(root / "authoritative", workspace_registry(), read_only=True).read().acts
                forward, reference = _runner_parity(list(recovered), surface)
                self.assertEqual(forward, reference)
                generator = __import__(
                    "tests.test_sli_track8_relationship_evidence",
                    fromlist=["_track6b_generator"],
                )._track6b_generator()
                outcome = live_coordinate_run(
                    WorkspaceCapability(root / "live"), repo_root=ROOT,
                    authoritative_acts=recovered, workspace_revision=len(recovered),
                    run_scope={"jurisdiction": "us", "year": "2025"}, scope_user=generator.USER,
                    request={"schema": "run-request.v1"}, run_id=f"demo.track12.{name}",
                    governance_pins=[], surface=generator_surface(surface), output_name=f"{name}.json",
                )
                self.assertIsNone(outcome.refusal)
                self.assertIsNotNone(outcome.output_path)
                self.assertIsNotNone(outcome.publications)
                assert outcome.output_path is not None and outcome.publications is not None
                output = json.loads(outcome.output_path.read_text("utf-8"))
                live_publications = sorted(
                    [(row.finding["symbol"], row.finding.get("value"), row.finding.get("pins"))
                     for row in outcome.publications], key=lambda row: json.dumps(row, sort_keys=True))
                self.assertEqual(live_publications, forward["publications"])
                live_dispositions = [
                    (row.get("artifact_id"), row.get("symbol"), row["disposition"], row.get("finding_id"),
                     row.get("code"), row.get("missing")) for row in output["dispositions"]
                ]
                live_dispositions.sort(key=lambda row: json.dumps(row, sort_keys=True))
                self.assertEqual(live_dispositions, forward["dispositions"])
                state = project(tuple(copy.deepcopy(row) for row in recovered), DerivationSchemas().registry)
                currency = compute_currency(state)
                lattice = facts_of(state.fact_state)
                current_ids = set(currency.current_finding_ids)
                current_findings = {key: row for key, row in state.findings.items() if key in current_ids}
                self.assertIn(school_id, {row["fact_id"] for key, row in state.findings.items()
                                          if key in current_ids})
                package_pin = next(pin for publication in outcome.publications
                                   for pin in publication.finding["pins"] if pin.get("role") == "adoption")
                contextual_findings: dict[str, dict[str, Any]] = {}
                account_finding = next((row for row in current_findings.values()
                                        if row["fact_id"] == fact_id_for(
                                            ACCOUNT, (("account", ACCOUNT_ID), ("tax-year", "2025")))), None)
                if account_finding is not None:
                    target_ids = {account_finding["value"].get("schooling_reference"),
                                  account_finding["value"].get("statement_reference")}
                    contextual_findings = {finding_id: row for finding_id, row in current_findings.items()
                                           if row["fact_id"] in target_ids}
                saved_doc = capture(
                    run_id=outcome.run_id or "", package=package_pin,
                    publications=outcome.publications, dispositions=output["dispositions"],
                    current_findings=current_findings,
                    contextual_findings=contextual_findings,
                    fact_keys={fact_id: {"fact_type_id": fact.fact_type_id, "bindings": dict(fact.keys),
                                         "individuated_by": list(fact.individuated_by)}
                               for fact_id, fact in lattice.items()},
                    evidence_by_id={key: row.evidence for key, row in state.evidence.items()},
                    selected_producer_ids=(ACCOUNT_REF_RULE, ACCOUNT_FINANCE_RULE, FINANCE_RULE, MEMBERSHIP_RULE),
                    all_findings=state.findings,
                    displacement_reasons={finding_id: [{"kind": reason.kind, "by": reason.by}
                                                       for reason in reasons]
                                          for finding_id, reasons in currency.reasons.items()},
                    lineage_acts=[row for row in recovered if row.get("kind") == "finding-retracted"],
                    experiment_metadata={"application_treatment": "unadopted"},
                )
                path = ROOT / "temp" / "track12" / f"{name}.saved-account.json"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(dumps(saved_doc))
                del outcome, state, currency, lattice, recovered, log
            return forward, output, loads(path.read_bytes())

        corrected_result, corrected_output, corrected_saved = run_fresh("account-corrected", corrected)
        corrected_ref = next(row for row in corrected_result["publications"]
                             if row[0].startswith(f"{ACCOUNT_REF_RESULT}|"))
        self.assertEqual(corrected_ref[1], "demo.track8.borrowing.b")
        corrected_state = project(tuple(copy.deepcopy(row) for row in corrected), DerivationSchemas().registry)
        corrected_currency = compute_currency(corrected_state)
        self.assertIn(corrected_id, corrected_currency.current_finding_ids)
        self.assertNotIn(ACCOUNT_FINDING, corrected_currency.current_finding_ids)
        corrected_support_ids = {row["finding"]["id"] for row in corrected_saved["evaluated_support"]}
        self.assertIn(corrected_id, corrected_support_ids)
        self.assertNotIn(ACCOUNT_FINDING, corrected_support_ids)
        corrected_lineage = {row["finding"]["id"]: row["status"] for row in corrected_saved["lineage"]}
        self.assertEqual(corrected_lineage[ACCOUNT_FINDING], "displaced")

        retracted = copy.deepcopy(corrected)
        adoption = retracted.pop()
        retracted.append(act(len(retracted), "finding-retracted", {"finding_id": corrected_id}))
        adoption["committed_against"] = len(retracted)
        retracted.append(adoption)
        retracted_result, _retracted_output, retracted_saved = run_fresh("account-retracted", retracted)
        self.assertFalse(any(row[0].startswith(f"{ACCOUNT_REF_RESULT}|")
                             for row in retracted_result["publications"]))
        retracted_state = project(tuple(copy.deepcopy(row) for row in retracted), DerivationSchemas().registry)
        retracted_currency = compute_currency(retracted_state)
        self.assertNotIn(corrected_id, retracted_currency.current_finding_ids)
        self.assertTrue(any(row["fact_id"] == school_id for key, row in retracted_state.findings.items()
                            if key in retracted_currency.current_finding_ids))
        retracted_support_ids = {row["finding"]["id"] for row in retracted_saved["evaluated_support"]}
        self.assertNotIn(corrected_id, retracted_support_ids)
        retracted_lineage = {row["finding"]["id"]: row["status"] for row in retracted_saved["lineage"]}
        self.assertEqual(retracted_lineage[corrected_id], "displaced")

    def test_explicit_relationship_control_uses_track11_expected_available_declarations(self) -> None:
        from tests.test_sli_track11_collection_declarations import (
            AVAILABLE_RULE, EXPECTED_RULE, _execute_track11, _reseal_readiness_candidate,
            _saved_input_closure, _source_finance_map,
        )

        surface, acts = _assemble_reference_only_case(include_relationship_claims=True, equal_pair=True)
        order = _reseal_readiness_candidate(surface, acts, consumer_first=False)
        record, forward, reference = _execute_track11(
            "track12-explicit-relationship-control", acts, surface, order,
        )
        self.assertEqual(forward, reference)
        self.assertTrue(record["live_matches_forward"])
        self.assertTrue(record["live_dispositions_match_forward"])
        self.assertFalse(record["saved"]["complete"])  # Carrier also captures known unrelated Track 8 horizon pins.
        self.assertTrue(record["saved"]["scope"]["selected_publication_ids"])
        expected_source_ids = set(record["source_finance_ids"])
        finance_claims = {row["finding"]["id"] for row in record["saved"]["evaluated_support"]
                          if row["fact"]["fact_type_id"] == FINANCE}
        self.assertEqual(len(expected_source_ids), 5)
        self.assertEqual(finance_claims, expected_source_ids)
        self.assertNotIn(ACCOUNT_FINDING, finance_claims)
        for rule_id in (EXPECTED_RULE, AVAILABLE_RULE):
            witness_rows = [row["finding"] for row in record["saved"]["publications"]
                            if {"role": "computation", "id": rule_id, "version": "v1"}
                            in row["finding"].get("pins", [])]
            witness_inputs = {pin["id"] for row in witness_rows for pin in row.get("pins", [])
                              if pin.get("role") == "input" and pin["id"] in expected_source_ids}
            self.assertEqual(witness_inputs, expected_source_ids)
        neutral_rows = [row["finding"] for row in record["saved"]["publications"]
                        if {"role": "computation", "id": MEMBERSHIP_RULE, "version": "v1"}
                        in row["finding"].get("pins", [])]
        self.assertEqual(len(neutral_rows), 3)
        self.assertEqual({row["value"] for row in neutral_rows}, {"true"})

        def assert_chain_closure(run: dict[str, Any], source_acts: list[dict[str, Any]]) -> None:
            saved = run["saved"]
            publication_by_id = {row["finding"]["id"]: row["finding"] for row in saved["publications"]}
            support_ids = {row["finding"]["id"] for row in saved["evaluated_support"]}
            support_rows = {row["finding"]["id"]: row for row in saved["evaluated_support"]}
            selected_rules = {FINANCE_RULE, MEMBERSHIP_RULE, EXPECTED_RULE, AVAILABLE_RULE}
            for finding in publication_by_id.values():
                if any(pin.get("id") in selected_rules and pin.get("role") == "computation"
                       for pin in finding.get("pins", [])):
                    self.assertTrue(_saved_input_closure(saved, finding.get("pins", [])) <= support_ids)
            for disposition in saved["dispositions"]:
                if disposition.get("artifact_id") in selected_rules and disposition.get("pins"):
                    self.assertTrue(_saved_input_closure(saved, disposition["pins"]) <= support_ids)

            finance_map = _source_finance_map(source_acts)
            memberships = {finding_id: row for finding_id, row in support_rows.items()
                           if row["fact"]["fact_type_id"] == MEMBERSHIP}
            schools = {finding_id: row for finding_id, row in support_rows.items()
                       if row["fact"]["fact_type_id"] == SCHOOL}
            membership_results = [finding for finding in publication_by_id.values()
                                  if {"role": "computation", "id": MEMBERSHIP_RULE, "version": "v1"}
                                  in finding.get("pins", [])]
            for result in membership_results:
                member_inputs = {pin["id"] for pin in result.get("pins", [])
                                 if pin.get("role") == "input" and pin.get("id") in memberships}
                self.assertEqual(len(member_inputs), 1)
                membership_id = next(iter(member_inputs))
                borrowing = memberships[membership_id]["fact"]["bindings"]["borrowing"]
                finance_ids = {finding_id for finding_id, keys in finance_map.items()
                               if keys.get("borrowing") == borrowing}
                self.assertTrue(finance_ids)
                school_ids: set[str] = set()
                for finance_id in finance_ids:
                    finance_keys = {key: value for key, value in finance_map[finance_id].items()
                                    if key != "fact_id" and key != "borrowing"}
                    matched_schools = {school_id for school_id, row in schools.items()
                                       if row["fact"]["bindings"] == finance_keys}
                    self.assertEqual(len(matched_schools), 1)
                    school_ids.update(matched_schools)
                expected_leaves = {membership_id} | finance_ids | school_ids
                actual_leaves = _saved_input_closure(saved, result.get("pins", []))
                self.assertEqual(actual_leaves, expected_leaves)
                self.assertNotIn(ACCOUNT_FINDING, actual_leaves)

        assert_chain_closure(record, acts)

        def source_ids_by_type(source_acts: list[dict[str, Any]]) -> dict[str, set[str]]:
            source_state = project(tuple(copy.deepcopy(row) for row in source_acts), DerivationSchemas().registry)
            source_currency = compute_currency(source_state)
            source_lattice = facts_of(source_state.fact_state)
            output: dict[str, set[str]] = {type_id: set() for type_id in (FINANCE, MEMBERSHIP, SCHOOL)}
            for finding_id, finding in source_state.findings.items():
                if finding_id not in source_currency.current_finding_ids:
                    continue
                fact = source_lattice.get(finding["fact_id"])
                if fact is not None and fact.fact_type_id in output:
                    output[fact.fact_type_id].add(finding_id)
            return output

        source_ids = source_ids_by_type(acts)
        self.assertEqual({key: len(value) for key, value in source_ids.items()},
                         {FINANCE: 5, MEMBERSHIP: 3, SCHOOL: 2})

        def chain_findings(run: dict[str, Any]) -> list[dict[str, Any]]:
            relevant = {FINANCE_RULE, MEMBERSHIP_RULE, EXPECTED_RULE, AVAILABLE_RULE}
            rows = [row["finding"] for row in run["saved"]["publications"]
                    if any(pin.get("role") == "computation" and pin.get("id") in relevant
                           for pin in row["finding"].get("pins", []))]
            return sorted(rows, key=lambda row: row["symbol"])

        def account_ref_row(run: dict[str, Any]) -> dict[str, Any] | None:
            rows = [row["finding"] for row in run["saved"]["publications"]
                    if {"role": "computation", "id": ACCOUNT_REF_RULE, "version": "v1"}
                    in row["finding"].get("pins", [])]
            self.assertLessEqual(len(rows), 1)
            return rows[0] if rows else None

        corrected = _correct_account(acts)
        corrected_record, corrected_forward, corrected_reference = _execute_track11(
            "track12-account-corrected-with-independent-claims", corrected, surface, order,
        )
        self.assertEqual(corrected_forward, corrected_reference)
        self.assertTrue(corrected_record["live_matches_forward"])
        self.assertEqual(chain_findings(corrected_record), chain_findings(record))
        self.assertEqual(source_ids_by_type(corrected), source_ids)
        assert_chain_closure(corrected_record, corrected)
        self.assertEqual({row["finding"]["id"] for row in corrected_record["saved"]["evaluated_support"]
                          if row["fact"]["fact_type_id"] == FINANCE}, expected_source_ids)
        self.assertEqual({row["finding"]["id"] for row in corrected_record["saved"]["evaluated_support"]
                          if row["fact"]["fact_type_id"] == MEMBERSHIP}, source_ids[MEMBERSHIP])
        self.assertEqual({row["finding"]["id"] for row in corrected_record["saved"]["evaluated_support"]
                          if row["fact"]["fact_type_id"] == SCHOOL}, source_ids[SCHOOL])
        corrected_lineage = {row["finding"]["id"]: row["status"]
                             for row in corrected_record["saved"]["lineage"]}
        self.assertEqual(corrected_lineage[ACCOUNT_FINDING], "displaced")
        corrected_ref = account_ref_row(corrected_record)
        assert corrected_ref is not None
        self.assertEqual(corrected_ref["value"], "demo.track8.borrowing.b")
        self.assertEqual({pin["id"] for pin in corrected_ref["pins"] if pin.get("role") == "input"},
                         {"demo.finding.sli.track12.account.corrected"})
        self.assertIn("demo.finding.sli.track12.account.corrected",
                      _saved_input_closure(corrected_record["saved"], corrected_ref["pins"]))
        assert_chain_closure(corrected_record, corrected)

        corrected_id = "demo.finding.sli.track12.account.corrected"
        retracted = copy.deepcopy(corrected)
        adoption = retracted.pop()
        retracted.append(act(len(retracted), "finding-retracted", {"finding_id": corrected_id}))
        adoption["committed_against"] = len(retracted)
        retracted.append(adoption)
        retracted_record, retracted_forward, retracted_reference = _execute_track11(
            "track12-account-retracted-with-independent-claims", retracted, surface, order,
        )
        self.assertEqual(retracted_forward, retracted_reference)
        self.assertTrue(retracted_record["live_matches_forward"])
        self.assertEqual(chain_findings(retracted_record), chain_findings(record))
        self.assertEqual(source_ids_by_type(retracted), source_ids)
        self.assertEqual({row["finding"]["id"] for row in retracted_record["saved"]["evaluated_support"]
                          if row["fact"]["fact_type_id"] == FINANCE}, expected_source_ids)
        self.assertEqual({row["finding"]["id"] for row in retracted_record["saved"]["evaluated_support"]
                          if row["fact"]["fact_type_id"] == MEMBERSHIP}, source_ids[MEMBERSHIP])
        self.assertEqual({row["finding"]["id"] for row in retracted_record["saved"]["evaluated_support"]
                          if row["fact"]["fact_type_id"] == SCHOOL}, source_ids[SCHOOL])
        retracted_lineage = {row["finding"]["id"]: row["status"]
                             for row in retracted_record["saved"]["lineage"]}
        self.assertEqual(retracted_lineage["demo.finding.sli.track12.account.corrected"], "displaced")
        self.assertIsNone(account_ref_row(retracted_record))


if __name__ == "__main__":
    unittest.main()
