"""Track 17: source applicability at a normally admitted neutral consumer."""
from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.live import _resolve_run_authorization, _resolved_run_material
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.marshal import marshal_live_run_context
from packages.derivation.package_validation import citizen_checksum, package_instance_checksum, validate_package
from packages.derivation.production_resolver import PublicationSurface, Refusal, resolve_production_package
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import run
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import fact_id_for, facts_of
from packages.kernel.findings import FindingModelError, project
from packages.tax.sli_relationship_recording import (
    FINANCING, INCLUSION_APPLICABILITY_UNESTABLISHED, SCHOOLING, STATEMENT_INCLUSION, STATEMENT_TYPE,
    correct_relationship_claim_durably, current_claim_applicability,
    record_submission_durably, withdraw_relationship_claim_durably,
)
from packages.tax.sli_relationship_review import prepare_review, save_review
from tests.support import act, demo_entity
import tests.test_sli_relationship_recording as track14
import tests.test_sli_track15_versioned_source_consumer as track15


def _pre_step_writer(log: ActLog) -> ActLog:
    """A test-only log without the ADR 0077 Part 5 declaration.

    It writes what ``ActLog.append`` now refuses, to model a history written
    before the step existed. ``project`` replays it unchanged; marshalling
    does not join an inclusion whose applicability it no longer establishes.
    """
    return ActLog(log.path.parent, DerivationSchemas().registry, undeclared_test_log=True)

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages/content/tax/2025"
FIXTURE = ROOT / "packages/sample_data/student_loan_relationship_source"
USER = "demo.user.filer"
SCOPE = {"jurisdiction": "us", "year": "2025"}
PACKAGE_ID = "demo.tax.2025.package.sli-relationship-source-diagnostic"
FINANCE_RULE = "demo.rule.tax.2025.sli.guarded-financing-observation"
INCLUSION_RULE = "demo.rule.tax.2025.sli.guarded-statement-inclusion-observation"
FINANCE_OUTPUT = "demo.tax.2025.sli.financing-observation"
INCLUSION_OUTPUT = "demo.tax.2025.sli.statement-inclusion-observation"
V35_REGISTRY = CONTENT / "published-packages.v35.json"
V35_PACKAGE = FIXTURE / "package.sli-relationship-source-diagnostic.v3.json"
V35_RELEASE = FIXTURE / "publication_surface/releases/demo.release.sli-relationship-source.2025.v35.json"


def _append_adoption(log: ActLog, registry: Any, package_path: Path, release_path: Path) -> None:
    package = json.loads(package_path.read_text("utf-8"))
    release = json.loads(release_path.read_text("utf-8"))
    revision = log.read().revision
    item = act(revision, "package-adoption", {
        "package": {"id": package["id"], "version": package["version"],
                    "checksum": package["package_checksum"]},
        "release": {"id": release["id"], "version": release["version"],
                    "checksum": hashlib.sha256(release_path.read_bytes()).hexdigest()},
        "scope": SCOPE, "revision": 1,
    })
    item["actor"] = USER
    log.append(item, expected_revision=revision)


def _run_v35(acts: tuple[dict[str, Any], ...], run_id: str) -> tuple[Any, Any, Any]:
    resolved, context = _marshal_v35(acts, run_id)
    return resolved, run(context, DerivationSchemas()), run_reference(context, DerivationSchemas())


def _marshal_v35(acts: tuple[dict[str, Any], ...], run_id: str) -> tuple[Any, Any]:
    """Marshal as ``live_coordinate_run`` does, with the ADR 0077 Part 5 replay reading."""
    registry = DerivationSchemas().registry
    surface = PublicationSurface(FIXTURE / "publication_surface/releases", V35_REGISTRY, ROOT / "packages")
    resolved = resolve_production_package(
        acts, run_scope=SCOPE, scope_user=USER, workspace_revision=len(acts),
        surface=surface, schemas=DerivationSchemas(),
    )
    if isinstance(resolved, Refusal):
        raise AssertionError(f"v35 relationship package refused: {resolved!r}")
    if resolved.release_id != "demo.release.sli-relationship-source.2025":
        raise AssertionError(f"unexpected release identity: {resolved.release_id}")
    if (resolved.package["id"], resolved.package["version"]) != (PACKAGE_ID, "v3"):
        raise AssertionError("resolver selected an unexpected guarded package")
    adoption = next(row for row in acts if row.get("kind") == "package-adoption")
    if adoption["payload"]["release"] != {
        "id": resolved.release_id, "version": "v35",
        "checksum": hashlib.sha256(V35_RELEASE.read_bytes()).hexdigest(),
    }:
        raise AssertionError("adoption does not pin exact v35 release bytes")
    state = project(acts, registry)
    currency = compute_currency(state)
    material = _resolved_run_material(resolved)
    rules, parameters, families, mappings, fact_types, bindings, collect_names = material
    authorization = _resolve_run_authorization(
        acts, run_scope=SCOPE, scope_user=USER, rules=rules,
        corpus={member["id"]: member for member in resolved.resolved_members},
        package=resolved.package,
    )
    context = marshal_live_run_context(
        run_id=run_id, state=state, currency=currency, rules=rules, parameters=parameters,
        canon=load_canon(DerivationSchemas()),
        adoption_pin={"role": "adoption", "id": PACKAGE_ID, "version": "v3"},
        governance_pins=[], family_declarations=families, closure_mappings=mappings,
        fact_types=fact_types, input_bindings=bindings, collect_source_names=collect_names,
        emission_only_source_names=list(material.emission_only_names),
        authorization=authorization, reporting_year=2025,
        parameter_index=material.parameter_index,
        claim_applicability=current_claim_applicability(acts, registry),
    )
    return resolved, context._context


def _assert_replay_omits(case: unittest.TestCase, context: Any, acts: tuple[dict[str, Any], ...],
                        registry: Any, omitted: list[dict[str, str]]) -> None:
    """ADR 0077 Part 5 replay: each omitted inclusion is a marker, not a source."""
    lattice = facts_of(project(acts, registry).fact_state)
    markers = [source for source in context.sources if source.name == INCLUSION_APPLICABILITY_UNESTABLISHED]
    case.assertEqual(
        [(source.finding_id, source.value, source.fact_id, source.keys) for source in markers],
        [(claim["finding_id"], "sli.statement-inclusion.applicability-unestablished",
          fact_id_for(INCLUSION_APPLICABILITY_UNESTABLISHED, tuple(lattice[claim["fact_id"]].keys)),
          tuple(lattice[claim["fact_id"]].keys))
         for claim in sorted(omitted, key=lambda claim: claim["finding_id"])],
    )
    joined = {source.finding_id for source in context.sources if source.name == STATEMENT_INCLUSION}
    case.assertFalse(joined & {claim["finding_id"] for claim in omitted})


def _published(result: Any) -> dict[str, dict[str, Any]]:
    return {row.finding["symbol"]: row.finding for row in result.publications}


def _surface(result: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    return (
        sorted((copy.deepcopy(row.finding) for row in result.publications), key=lambda row: row["symbol"]),
        sorted((copy.deepcopy(row) for row in result.dispositions), key=lambda row: (
            row.get("artifact_id", ""), row.get("symbol", ""), row.get("disposition", ""))),
        sorted((copy.deepcopy(row) for row in result.blocked), key=lambda row: (
            row.get("artifact_id", ""), row.get("subject_fact_id", ""))),
    )


def _current_source_finding(acts: tuple[dict[str, Any], ...], registry: Any, fact_id: str) -> dict[str, Any]:
    state = project(acts, registry)
    current = compute_currency(state).current_finding_ids
    rows = [finding for finding_id, finding in state.findings.items()
            if finding_id in current and finding.get("fact_id") == fact_id]
    if len(rows) != 1:
        raise AssertionError(f"expected one current source finding for {fact_id}, got {len(rows)}")
    return rows[0]


def _expected_pins(package_version: str, rule_id: str, relation_finding: str,
                   target_finding: str | None) -> list[dict[str, str]]:
    rows = [
        {"role": "adoption", "id": PACKAGE_ID, "version": package_version},
        {"role": "computation", "id": rule_id, "version": "v1"},
        {"role": "input", "id": relation_finding, "version": "v1", "origin": "assertion"},
    ]
    if target_finding is not None:
        rows.append({"role": "input", "id": target_finding, "version": "v1", "origin": "assertion"})
    return sorted(rows, key=lambda row: json.dumps(row, sort_keys=True))


class Track17RelationshipApplicability(unittest.TestCase):
    def test_v35_registry_release_and_package_are_exactly_admitted(self) -> None:
        old = json.loads((CONTENT / "published-packages.v34.json").read_text("utf-8"))
        current = json.loads(V35_REGISTRY.read_text("utf-8"))
        for section in ("citizens", "packages"):
            old_by_key = {(row["id"], row["version"]): row for row in old[section]}
            current_by_key = {(row["id"], row["version"]): row for row in current[section]}
            self.assertEqual({key: current_by_key[key] for key in old_by_key}, old_by_key)
            additions = set(current_by_key) - set(old_by_key)
            self.assertEqual(len(additions), 2 if section == "citizens" else 1)
            if section == "citizens":
                self.assertEqual({identity for identity, _version in additions},
                                 {FINANCE_RULE, INCLUSION_RULE})
            else:
                self.assertEqual(additions, {(PACKAGE_ID, "v3")})
        release = json.loads(V35_RELEASE.read_text("utf-8"))
        self.assertEqual(release["package_registry_sha256"],
                         hashlib.sha256(V35_REGISTRY.read_bytes()).hexdigest())
        package = json.loads(V35_PACKAGE.read_text("utf-8"))
        self.assertEqual(package["package_checksum"], package_instance_checksum(package))
        corpus: dict[tuple[str, str], dict[str, Any]] = {}
        for path in [*CONTENT.glob("*.json"), *FIXTURE.glob("*.json")]:
            try:
                body = json.loads(path.read_text("utf-8"))
            except (OSError, ValueError):
                continue
            if isinstance(body, dict) and isinstance(body.get("id"), str) and isinstance(body.get("version"), str):
                corpus[(body["id"], body["version"])] = body
        admission = validate_package(package, corpus, DerivationSchemas())
        self.assertTrue(admission.ok, [issue.detail for issue in admission.issues])
        self.assertEqual({(row["id"], row["version"], row["checksum"])
                          for row in current["citizens"]
                          if row["id"] in {FINANCE_RULE, INCLUSION_RULE}},
                         {(member["id"], member["version"], citizen_checksum(member))
                          for member in admission.resolved_members
                          if member["id"] in {FINANCE_RULE, INCLUSION_RULE}})

    def _scenario(self) -> tuple[tempfile.TemporaryDirectory[str], ActLog, Any, dict[str, Any]]:
        raw, log, registry, refs = track14.OrdinaryRelationshipRecording()._workspace()
        second_borrowing = "demo.track17.borrowing.second"
        from packages.tax.sli_relationship_recording import introduce_borrowing_reference_durably
        introduce_borrowing_reference_durably(
            log, registry, reference_id=second_borrowing, description="Second study borrowing",
            actor=USER, at="2026-09-30T12:00:00Z",
        )
        entities = [
            ("demo.track17.period.second", "Spring 2025", "tax.us.educational-period"),
            ("demo.track17.institution.second", "Harbor College", "tax.us.educational-institution"),
            ("demo.track17.programme.second", "AA", "tax.us.educational-programme"),
            ("demo.track17.lender.second", "Pine Servicing", "tax.us.student-loan-lender"),
            ("demo.track17.statement.second", "Second 2025 Form 1098-E", "tax.us.1098e-statement"),
        ]
        for identity, label, kind in entities:
            revision = log.read().revision
            log.append(act(revision, "entity-introduced", {"entity": demo_entity(identity, label, kind)}),
                       expected_revision=revision)
        second_school = track14._append_source(
            log, registry, SCHOOLING,
            (("period", entities[0][0]), ("institution", entities[1][0]), ("programme", entities[2][0])),
            "Harbor College, AA, spring 2025", "track17-second-school",
        )
        second_statement = track14._append_source(
            log, registry, STATEMENT_TYPE,
            (("lender", entities[3][0]), ("statement", entities[4][0]), ("tax-year", "2025")),
            850.0, "track17-second-statement",
        )
        first_claims = record_submission_durably(log, {
            "submission_id": "demo.track17.answer.first", "evidence_id": "demo.evidence.track17.answer.first",
            "actor": USER, "at": "2026-09-30T12:01:00Z", "borrowing_ref": refs["borrowing"],
            "schooling_fact_id": refs["school"], "statement_fact_id": refs["statement"],
            "financing_response": "yes", "inclusion_response": "yes", "interest_portion_response": "unknown",
        }, registry)["claims"]
        second_claims = record_submission_durably(log, {
            "submission_id": "demo.track17.answer.second", "evidence_id": "demo.evidence.track17.answer.second",
            "actor": USER, "at": "2026-09-30T12:02:00Z", "borrowing_ref": second_borrowing,
            "schooling_fact_id": second_school, "statement_fact_id": second_statement,
            "financing_response": "yes", "inclusion_response": "yes", "interest_portion_response": "unknown",
        }, registry)["claims"]
        return raw, log, registry, {
            "first": {**refs, **first_claims},
            "second": {"borrowing": second_borrowing, "school": second_school,
                        "statement": second_statement, **second_claims},
        }

    def test_v34_reproduction_then_guarded_recovery_and_target_changes(self) -> None:
        raw, log, registry, subjects = self._scenario()
        with raw:
            track15._add_adoption(log)
            first = subjects["first"]
            target_finding = _current_source_finding(log.read().acts, registry, first["school"])
            target_finding_id = target_finding["id"]
            source_target_id = fact_id_for(SCHOOLING, tuple(
                (key, value) for key, value in facts_of(project(log.read().acts, registry).fact_state)[
                    first["financing"]["fact_id"]].keys if key != "borrowing"))
            self.assertEqual(source_target_id, first["school"])
            log.append(act(log.read().revision, "finding-retracted", {"finding_id": target_finding_id}),
                       expected_revision=log.read().revision)
            v34_log = ActLog(log.path.parent, registry)
            _resolved, forward34, reference34 = track15._run_both(
                v34_log.read().acts, "demo.track17.v34-unguarded")
            self.assertEqual(_surface(forward34), _surface(reference34))
            old = _published(forward34)
            unguarded_symbol = f"{track15.FINANCE_OUTPUT}|{first['financing']['fact_id']}"
            self.assertIn(unguarded_symbol, old)
            self.assertEqual(old[unguarded_symbol]["value"], "sli.financing.observed")
            applicability = {row["finding_id"]: row for row in
                             current_claim_applicability(v34_log.read().acts, registry)}
            self.assertEqual(applicability[first["financing"]["finding_id"]]["applicability"],
                             "unresolved-applicability")

        raw, log, registry, subjects = self._scenario()
        with raw:
            _append_adoption(log, registry, V35_PACKAGE, V35_RELEASE)
            first, second = subjects["first"], subjects["second"]

            def recovered(name: str) -> tuple[Any, Any, dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
                fresh = ActLog(log.path.parent, registry)
                acts = fresh.read().acts
                _resolved, forward, reference = _run_v35(acts, f"demo.track17.{name}")
                self.assertEqual(_surface(forward), _surface(reference))
                return forward, reference, _published(forward), _published(reference)

            initial_result, _initial_ref, initial, _ = recovered("initial")
            claims = [
                (first["financing"], FINANCE_OUTPUT, FINANCE_RULE, first["school"], "financing"),
                (second["financing"], FINANCE_OUTPUT, FINANCE_RULE, second["school"], "financing"),
                (first["statement-inclusion"], INCLUSION_OUTPUT, INCLUSION_RULE,
                 first["statement"], "statement-inclusion"),
                (second["statement-inclusion"], INCLUSION_OUTPUT, INCLUSION_RULE,
                 second["statement"], "statement-inclusion"),
            ]
            initial_pins: dict[str, list[dict[str, str]]] = {}
            for claim, output, rule_id, source_id, kind in claims:
                symbol = f"{output}|{claim['fact_id']}"
                finding = initial[symbol]
                target = _current_source_finding(log.read().acts, registry, source_id)
                source_type = SCHOOLING if kind == "financing" else STATEMENT_TYPE
                relation_fact = facts_of(project(log.read().acts, registry).fact_state)[claim["fact_id"]]
                source_fact_id = fact_id_for(source_type, tuple(
                    (key, value) for key, value in relation_fact.keys if key != "borrowing"))
                self.assertEqual(source_fact_id, source_id)
                expected = _expected_pins("v3", rule_id, claim["finding_id"], target["id"])
                self.assertEqual(sorted(finding["pins"], key=lambda row: json.dumps(row, sort_keys=True)), expected)
                self.assertEqual(finding["value"], f"sli.{kind}.observed")

            # Same statement identity, changed amount, with no reviewed scope.
            # ADR 0077 Part 5 refuses this write on the recorder's log; it is
            # written as pre-step history. Replay keeps the new box 1 but does
            # not join the inclusion: its applicability is not established, so
            # a marker stands in its place. The unaffected second statement is
            # stable.
            first_statement_keys = (("lender", "demo.track14.lender.cedar"),
                                    ("statement", "demo.track14.statement.2025"), ("tax-year", "2025"))
            track14._append_source(_pre_step_writer(log), registry, STATEMENT_TYPE, first_statement_keys,
                                   1775.0, "track17-first-statement-amount-corrected")
            amount_result, _amount_ref, amount, _ = recovered("amount-corrected")
            first_inclusion = f"{INCLUSION_OUTPUT}|{first['statement-inclusion']['fact_id']}"
            second_inclusion = f"{INCLUSION_OUTPUT}|{second['statement-inclusion']['fact_id']}"
            amount_acts = ActLog(log.path.parent, registry).read().acts
            current_statement = _current_source_finding(amount_acts, registry, first["statement"])
            self.assertEqual(current_statement["value"], 1775.0)
            self.assertNotIn(first_inclusion, amount)
            _resolved_amount, amount_context = _marshal_v35(amount_acts, "demo.track17.amount-corrected")
            _assert_replay_omits(self, amount_context, amount_acts, registry, [first["statement-inclusion"]])
            self.assertIn(current_statement["id"],
                          {source.finding_id for source in amount_context.sources} |
                          {item.finding_id for item in amount_context.inputs})
            self.assertEqual((amount[second_inclusion]["id"], amount[second_inclusion]["value"],
                              amount[second_inclusion]["pins"]),
                             (initial[second_inclusion]["id"], initial[second_inclusion]["value"],
                              initial[second_inclusion]["pins"]))

            # Same schooling identity, corrected description: the financing
            # observation stays on the same relation and follows new source support.
            school_keys = (("period", "demo.track14.period.autumn24"),
                           ("institution", "demo.track14.institution.river"),
                           ("programme", "demo.track14.programme.bsc"))
            track14._append_source(log, registry, SCHOOLING, school_keys,
                                   "Riverside College, BSc, autumn 2024, corrected course load",
                                   "track17-first-school-corrected")
            school_result, _school_ref, school, _ = recovered("schooling-corrected")
            first_finance = f"{FINANCE_OUTPUT}|{first['financing']['fact_id']}"
            second_finance = f"{FINANCE_OUTPUT}|{second['financing']['fact_id']}"
            current_school = _current_source_finding(log.read().acts, registry, first["school"])
            self.assertEqual(school[first_finance]["value"], "sli.financing.observed")
            self.assertEqual(sorted(school[first_finance]["pins"], key=lambda row: json.dumps(row, sort_keys=True)),
                             _expected_pins("v3", FINANCE_RULE, first["financing"]["finding_id"],
                                            current_school["id"]))
            self.assertEqual((school[second_finance]["id"], school[second_finance]["value"],
                              school[second_finance]["pins"]),
                             (initial[second_finance]["id"], initial[second_finance]["value"],
                              initial[second_finance]["pins"]))
            self.assertNotEqual(school[first_finance]["id"], initial[first_finance]["id"])

            # Retract the first relationship's exact current targets. Its old
            # relationship history remains current. The financing rule now has
            # a blocked disposition. The inclusion was already not joined
            # (above); it stays a marker. The second subject stays identical.
            for source_id in (first["school"], first["statement"]):
                target = _current_source_finding(log.read().acts, registry, source_id)
                revision = log.read().revision
                log.append(act(revision, "finding-retracted", {"finding_id": target["id"]}),
                           expected_revision=revision)
            guarded_result, _guarded_ref, guarded, _ = recovered("targets-retracted")
            self.assertNotIn(first_finance, guarded)
            self.assertNotIn(first_inclusion, guarded)
            for symbol in (second_finance, second_inclusion):
                self.assertEqual((guarded[symbol]["id"], guarded[symbol]["value"], guarded[symbol]["pins"]),
                                 (school[symbol]["id"], school[symbol]["value"], school[symbol]["pins"]))

            guarded_acts = ActLog(log.path.parent, registry).read().acts
            _resolved_guarded, guarded_context = _marshal_v35(guarded_acts, "demo.track17.targets-retracted")
            _assert_replay_omits(self, guarded_context, guarded_acts, registry, [first["statement-inclusion"]])
            self.assertFalse(any(row.get("symbol") == first_inclusion for row in guarded_result.dispositions))
            self.assertFalse(any(row.get("subject_fact_id") == first["statement-inclusion"]["fact_id"]
                                 for row in guarded_result.blocked))
            inclusion_applicability = {item["finding_id"]: item for item in current_claim_applicability(
                guarded_acts, registry)}[first["statement-inclusion"]["finding_id"]]
            self.assertEqual((inclusion_applicability["source_fact_id"], inclusion_applicability["applicability"]),
                             (first["statement"], "unresolved-applicability"))

            for claim, rule_id, source_type, source_id, symbol in (
                (first["financing"], FINANCE_RULE, SCHOOLING, first["school"], first_finance),
            ):
                blocked = [row for row in guarded_result.dispositions
                           if row.get("artifact_id") == rule_id and row.get("symbol") == symbol]
                self.assertEqual(len(blocked), 1)
                row = blocked[0]
                self.assertEqual((row["disposition"], row["code"], row["missing"]),
                                 ("blocked", "DEPENDENCY_ABSENT", [source_type]))
                expected_blocked_pins = sorted([
                    {"role": "adoption", "id": PACKAGE_ID, "version": "v3"},
                    {"role": "input", "id": claim["finding_id"], "version": "v1",
                     "origin": "assertion"},
                ], key=lambda pin: json.dumps(pin, sort_keys=True))
                self.assertEqual(sorted(row["pins"], key=lambda pin: json.dumps(pin, sort_keys=True)),
                                 expected_blocked_pins)
                # The blocked row names the exact relationship subject; its
                # structured keys determine the exact absent source identity.
                subject_fact = facts_of(project(log.read().acts, registry,).fact_state,
                                       include_displaced=True)[claim["fact_id"]]
                source_fact_id = fact_id_for(source_type, tuple(
                    (key, value) for key, value in subject_fact.keys if key != "borrowing"))
                self.assertEqual(source_fact_id, source_id)
                self.assertTrue(any(row.get("subject_fact_id") == claim["fact_id"] and
                                    row.get("missing") == [source_type]
                                    for row in guarded_result.blocked))
                applicability = {item["finding_id"]: item for item in current_claim_applicability(
                    log.read().acts, registry)}
                self.assertEqual(applicability[claim["finding_id"]]["source_fact_id"], source_id)
                self.assertEqual(applicability[claim["finding_id"]]["applicability"],
                                 "unresolved-applicability")

    def test_relationship_correction_and_withdrawal_change_only_dependent_observations(self) -> None:
        raw, log, registry, subjects = self._scenario()
        with raw:
            first, second = subjects["first"], subjects["second"]
            _append_adoption(log, registry, V35_PACKAGE, V35_RELEASE)

            def recovered(name: str) -> tuple[tuple[dict[str, Any], ...], Any, Any, dict[str, dict[str, Any]]]:
                fresh = ActLog(log.path.parent, registry)
                acts = fresh.read().acts
                _resolved, forward, reference = _run_v35(acts, f"demo.track17.relationship-lifecycle.{name}")
                self.assertEqual(_surface(forward), _surface(reference))
                return acts, forward, reference, _published(forward)

            initial_acts, initial_result, _initial_reference, initial = recovered("initial")
            initial_symbols = {
                "first_finance": f"{FINANCE_OUTPUT}|{first['financing']['fact_id']}",
                "first_inclusion": f"{INCLUSION_OUTPUT}|{first['statement-inclusion']['fact_id']}",
                "second_finance": f"{FINANCE_OUTPUT}|{second['financing']['fact_id']}",
                "second_inclusion": f"{INCLUSION_OUTPUT}|{second['statement-inclusion']['fact_id']}",
            }
            self.assertEqual(set(initial_symbols.values()), set(initial))

            correction = correct_relationship_claim_durably(
                log, registry, finding_id=first["financing"]["finding_id"],
                successor={
                    "submission_id": "demo.track17.relationship-correction",
                    "evidence_id": "demo.evidence.track17.relationship-correction",
                    "actor": USER, "at": "2026-09-30T12:30:00Z",
                    "borrowing_ref": first["borrowing"],
                    "schooling_fact_id": second["school"],
                    "statement_fact_id": "",
                    "financing_response": "yes", "inclusion_response": "unanswered",
                    "interest_portion_response": "unknown",
                },
                actor=USER, at="2026-09-30T12:30:00Z",
            )
            successor = correction["claims"]["financing"]
            corrected_acts, corrected_result, _corrected_reference, corrected = recovered("corrected")
            successor_symbol = f"{FINANCE_OUTPUT}|{successor['fact_id']}"
            self.assertNotIn(initial_symbols["first_finance"], corrected)
            self.assertIn(successor_symbol, corrected)
            successor_source = _current_source_finding(corrected_acts, registry, second["school"])
            self.assertEqual(corrected[successor_symbol]["value"], "sli.financing.observed")
            self.assertEqual(
                sorted(corrected[successor_symbol]["pins"], key=lambda pin: json.dumps(pin, sort_keys=True)),
                _expected_pins("v3", FINANCE_RULE, successor["finding_id"], successor_source["id"]),
            )
            for key in ("first_inclusion", "second_finance", "second_inclusion"):
                symbol = initial_symbols[key]
                self.assertEqual((corrected[symbol]["id"], corrected[symbol]["value"], corrected[symbol]["pins"]),
                                 (initial[symbol]["id"], initial[symbol]["value"], initial[symbol]["pins"]))
            correction_state = project(corrected_acts, registry)
            correction_current = compute_currency(correction_state).current_finding_ids
            self.assertIn(first["financing"]["finding_id"], correction_state.findings)
            self.assertNotIn(first["financing"]["finding_id"], correction_current)
            self.assertTrue(any(row.get("symbol") == initial_symbols["first_finance"] and
                                row.get("disposition") == "published"
                                for row in initial_result.dispositions))
            self.assertFalse(any(row.get("symbol") == initial_symbols["first_finance"]
                                 for row in corrected_result.dispositions))

            withdraw_relationship_claim_durably(
                log, registry, finding_id=first["statement-inclusion"]["finding_id"],
                actor=USER, at="2026-09-30T12:31:00Z",
            )
            withdrawn_acts, withdrawn_result, _withdrawn_reference, withdrawn = recovered("withdrawn")
            self.assertNotIn(initial_symbols["first_inclusion"], withdrawn)
            for key in ("second_finance", "second_inclusion"):
                symbol = initial_symbols[key]
                self.assertEqual((withdrawn[symbol]["id"], withdrawn[symbol]["value"], withdrawn[symbol]["pins"]),
                                 (corrected[symbol]["id"], corrected[symbol]["value"], corrected[symbol]["pins"]))
            self.assertEqual((withdrawn[successor_symbol]["id"], withdrawn[successor_symbol]["value"],
                              withdrawn[successor_symbol]["pins"]),
                             (corrected[successor_symbol]["id"], corrected[successor_symbol]["value"],
                              corrected[successor_symbol]["pins"]))
            withdrawal_state = project(withdrawn_acts, registry)
            withdrawal_current = compute_currency(withdrawal_state).current_finding_ids
            self.assertIn(first["statement-inclusion"]["finding_id"], withdrawal_state.findings)
            self.assertNotIn(first["statement-inclusion"]["finding_id"], withdrawal_current)
            self.assertFalse(any(row.get("symbol") == initial_symbols["first_inclusion"]
                                 for row in withdrawn_result.dispositions))

    def test_same_key_statement_record_has_no_composition_answer(self) -> None:
        raw, log, registry, subjects = self._scenario()
        with raw:
            first, second = subjects["first"], subjects["second"]
            _append_adoption(log, registry, V35_PACKAGE, V35_RELEASE)
            review = prepare_review(
                log, registry, review_id="demo.track17.review.composition",
                shown_at="2026-09-30T12:10:00Z", borrowing_refs=(second["borrowing"],),
                schooling_fact_ids=(second["school"],), statement_fact_ids=(first["statement"],),
            )
            statement_card = review["statement_choices"][0]
            self.assertEqual(set(statement_card), {
                "choice_ref", "shown_as", "tax_year", "issuer_as_printed", "box_1_reported_total",
                "recognition_clues", "support",
            })
            saved = save_review(
                log, registry, review, borrowing_ref=second["borrowing"],
                schooling_fact_id=second["school"], statement_fact_id=first["statement"],
                financing_response="unanswered", inclusion_response="yes", actor=USER,
                at="2026-09-30T12:11:00Z", submission_id="demo.track17.submission.composition",
                evidence_id="demo.evidence.track17.submission.composition",
                interest_portion_response="unknown",
            )
            fresh = ActLog(log.path.parent, registry)
            recovered = project(fresh.read().acts, registry)
            content = recovered.evidence[saved["evidence_id"]].evidence["content"]
            self.assertEqual(content["responses"]["inclusion_response"], "yes")
            self.assertEqual(content["interest_portion_response"], "unknown")
            self.assertNotIn("composition_response", content)
            self.assertNotIn("included_borrowings", content["recognition_context"])
            fact = facts_of(recovered.fact_state)[first["statement"]]
            self.assertEqual(set(dict(fact.keys)), {"lender", "statement", "tax-year"})
            self.assertEqual(fact_id_for(STATEMENT_TYPE, tuple(fact.keys)), first["statement"])
            old_value = next(finding["value"] for finding in recovered.findings.values()
                             if finding.get("fact_id") == first["statement"] and
                             finding["id"] in compute_currency(recovered).current_finding_ids)
            self.assertEqual(old_value, 1250.0)

            # Two borrowing relationships now share this exact statement.
            before_log = ActLog(log.path.parent, registry)
            before_acts = before_log.read().acts
            _resolved, before_forward, before_reference = _run_v35(
                before_acts, "demo.track17.same-statement-before-correction")
            self.assertEqual(_surface(before_forward), _surface(before_reference))
            before_publications = _published(before_forward)
            inclusion_symbols = [
                f"{INCLUSION_OUTPUT}|{first['statement-inclusion']['fact_id']}",
                f"{INCLUSION_OUTPUT}|{saved['claims']['statement-inclusion']['fact_id']}",
            ]
            shared_target = _current_source_finding(before_acts, registry, first["statement"])
            relation_finding_ids = (first["statement-inclusion"]["finding_id"],
                                    saved["claims"]["statement-inclusion"]["finding_id"])
            for relation_finding_id, symbol in zip(relation_finding_ids, inclusion_symbols, strict=True):
                self.assertIn(symbol, before_publications)
                pins = before_publications[symbol]["pins"]
                self.assertIn({"role": "input", "id": relation_finding_id, "version": "v1",
                               "origin": "assertion"}, pins)
                self.assertIn({"role": "input", "id": shared_target["id"], "version": "v1",
                               "origin": "assertion"}, pins)

            # The ordinary same-key correction changes only the existing box-1
            # source value. Its statement identity and the answer's inclusion
            # assertion do not tell whether composition stayed the same.
            keys = tuple(fact.keys)
            # ADR 0077 Part 5: on the recorder's log this unscoped append is refused.
            with self.assertRaisesRegex(FindingModelError, "scoped supersession violated"):
                track14._append_source(log, registry, STATEMENT_TYPE, keys, 1800.0,
                                       "track17-composition-ambiguous-correction-refused")
            self.assertNotIn("demo.finding.track14.track17-composition-ambiguous-correction-refused",
                             project(log.read().acts, registry).findings)
            # A history written before the step can still hold it; project replays it unchanged.
            track14._append_source(_pre_step_writer(log), registry, STATEMENT_TYPE, keys, 1800.0,
                                   "track17-composition-ambiguous-correction")
            recovered_again = ActLog(log.path.parent, registry)
            state = project(recovered_again.read().acts, registry)
            current_ids = compute_currency(state).current_finding_ids
            statement_findings = [finding for finding_id, finding in state.findings.items()
                                  if finding_id in current_ids and finding.get("fact_id") == first["statement"]]
            self.assertEqual(len(statement_findings), 1)
            self.assertEqual(statement_findings[0]["value"], 1800.0)
            saved_again = state.evidence[saved["evidence_id"]].evidence["content"]
            self.assertEqual(saved_again["references"]["statement_fact_id"], first["statement"])
            self.assertEqual(saved_again["responses"]["inclusion_response"], "yes")
            self.assertNotIn("composition_response", saved_again)
            _resolved, after_forward, after_reference = _run_v35(
                recovered_again.read().acts, "demo.track17.same-statement-after-correction")
            self.assertEqual(_surface(after_forward), _surface(after_reference))
            after_publications = _published(after_forward)
            corrected_target = statement_findings[0]
            self.assertNotEqual(corrected_target["id"], shared_target["id"])
            # ADR 0077 Part 5 replay: neither inclusion is joined to the
            # unreviewed 1800. Each is a marker; the 1800 box 1 is still read.
            for symbol in inclusion_symbols:
                self.assertNotIn(symbol, after_publications)
            composition_claim = saved["claims"]["statement-inclusion"]
            after_acts = recovered_again.read().acts
            _resolved_after, after_context = _marshal_v35(after_acts, "demo.track17.same-statement-after-correction")
            _assert_replay_omits(self, after_context, after_acts, registry,
                                 [first["statement-inclusion"], composition_claim])
            self.assertIn(corrected_target["id"],
                          {source.finding_id for source in after_context.sources} |
                          {item.finding_id for item in after_context.inputs})
            applicability = current_claim_applicability(recovered_again.read().acts, registry)
            self.assertEqual(
                {row["applicability"] for row in applicability
                 if row["finding_id"] in {composition_claim["finding_id"],
                                           first["statement-inclusion"]["finding_id"]}},
                # Track 6 read-side tie (ADR 0077 Part 5): a direct unscoped box 1
                # append leaves the old inclusions unresolved, not applicable.
                {"unresolved-applicability"},
            )


if __name__ == "__main__":
    unittest.main()
