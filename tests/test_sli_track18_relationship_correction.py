"""Integrated Track 18 relationship correction lifecycle demonstration."""
from __future__ import annotations

import unittest
import hashlib
import json
import tempfile
from typing import Any, Sequence
from pathlib import Path

from packages.derivation.live import _resolve_run_authorization, _resolved_run_material
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.marshal import marshal_live_run_context
from packages.derivation.package_validation import package_instance_checksum, validate_package
from packages.derivation.production_resolver import PublicationSurface, Refusal, resolve_production_package
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import run
from packages.kernel.act_log import ActLog, ActLogError
from packages.kernel.currency import compute_currency
from packages.kernel.facts import fact_id_for, facts_of
from packages.kernel.findings import project
from packages.tax.sli_relationship_recording import (
    INCLUSION_UNRESOLVED, RelationshipRecordingRefused, STATEMENT_TYPE, current_claim_applicability,
    record_submission_durably,
)
from packages.tax.sli_relationship_review import (
    answer_review_claim, apply_statement_correction_review, correct_review_claim, prepare_review,
)
from tests.test_sli_track17_relationship_applicability import (
    FINANCE_OUTPUT, INCLUSION_OUTPUT, USER, _published, _surface,
)
import tests.test_sli_track17_relationship_applicability as track17
import tests.test_sli_relationship_recording as track14
from tests.support import act

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "packages/sample_data/student_loan_relationship_source"
CONTENT = ROOT / "packages/content/tax/2025"
V36_PACKAGE = FIXTURE / "package.sli-relationship-source-diagnostic.v4.json"
V36_RELEASE = FIXTURE / "publication_surface/releases/demo.release.sli-relationship-source.2025.v36.json"
V36_REGISTRY = CONTENT / "published-packages.v36.json"
UNRESOLVED_RULE = "demo.rule.tax.2025.sli.statement-inclusion-unresolved-observation"
UNRESOLVED_OUTPUT = "demo.tax.2025.sli.statement-inclusion-unresolved-observation"


def _append_v36_adoption(log: ActLog, registry: Any) -> None:
    package = json.loads(V36_PACKAGE.read_text("utf-8"))
    release = json.loads(V36_RELEASE.read_text("utf-8"))
    revision = log.read().revision
    adoption = act(revision, "package-adoption", {
        "package": {"id": package["id"], "version": package["version"],
                    "checksum": package["package_checksum"]},
        "release": {"id": release["id"], "version": release["version"],
                    "checksum": hashlib.sha256(V36_RELEASE.read_bytes()).hexdigest()},
        "scope": {"jurisdiction": "us", "year": "2025"}, "revision": 1,
    })
    adoption["actor"] = USER
    log.append(adoption, expected_revision=revision)
    bundle_path = FIXTURE / "demo.tax.2025.sli-relationship-unresolved-vocabulary.v1.json"
    bundle = json.loads(bundle_path.read_text("utf-8"))
    revision = log.read().revision
    bundle_adoption = act(revision, "bundle-adoption", {"bundle": bundle})
    bundle_adoption["actor"] = USER
    log.append(bundle_adoption, expected_revision=revision)


def _run_v36(acts: tuple[dict[str, Any], ...], run_id: str) -> tuple[Any, Any, Any]:
    resolved, context = _marshal_v36(acts, run_id)
    schemas = DerivationSchemas()
    return resolved, run(context, schemas), run_reference(context, schemas)


def _marshal_v36(acts: tuple[dict[str, Any], ...], run_id: str) -> tuple[Any, Any]:
    """Marshal as ``live_coordinate_run`` does, with the ADR 0077 Part 5 replay reading."""
    schemas = DerivationSchemas()
    surface = PublicationSurface(FIXTURE / "publication_surface/releases", V36_REGISTRY, ROOT / "packages")
    resolved = resolve_production_package(
        acts, run_scope={"jurisdiction": "us", "year": "2025"}, scope_user=USER,
        workspace_revision=len(acts), surface=surface, schemas=schemas,
    )
    if isinstance(resolved, Refusal):
        raise AssertionError(f"v36 unresolved relationship package refused: {resolved!r}")
    if resolved.release_id != "demo.release.sli-relationship-source.2025" or resolved.package["version"] != "v4":
        raise AssertionError("resolver did not select the v36 diagnostic package")
    package = json.loads(V36_PACKAGE.read_text("utf-8"))
    release = json.loads(V36_RELEASE.read_text("utf-8"))
    adoption = next(row for row in acts if row.get("kind") == "package-adoption")
    if release.get("version") != "v36" or release.get("package_registry_sha256") != hashlib.sha256(
            V36_REGISTRY.read_bytes()).hexdigest():
        raise AssertionError("v36 release does not pin exact registry bytes")
    if adoption.get("payload", {}).get("release") != {
            "id": resolved.release_id, "version": "v36",
            "checksum": hashlib.sha256(V36_RELEASE.read_bytes()).hexdigest()}:
        raise AssertionError("workspace adoption does not pin exact v36 release bytes")
    if package["package_checksum"] != package_instance_checksum(package):
        raise AssertionError("v36 diagnostic package checksum is invalid")
    old_registry = json.loads((CONTENT / "published-packages.v35.json").read_text("utf-8"))
    new_registry = json.loads(V36_REGISTRY.read_text("utf-8"))
    for section in ("citizens", "packages"):
        new_by_key = {(row["id"], row["version"]): row for row in new_registry[section]}
        for row in old_registry[section]:
            if new_by_key.get((row["id"], row["version"])) != row:
                raise AssertionError(f"v36 registry changed a v35 {section} entry")
    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for path in [*CONTENT.glob("*.json"), *FIXTURE.glob("*.json")]:
        try:
            body = json.loads(path.read_text("utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(body, dict) and isinstance(body.get("id"), str) and isinstance(body.get("version"), str):
            corpus[(body["id"], body["version"])] = body
    admission = validate_package(package, corpus, schemas)
    if not admission.ok:
        raise AssertionError([issue.detail for issue in admission.issues])
    state = project(acts, schemas.registry)
    currency = compute_currency(state)
    material = _resolved_run_material(resolved)
    rules, parameters, families, mappings, fact_types, bindings, collect_names = material
    authorization = _resolve_run_authorization(
        acts, run_scope={"jurisdiction": "us", "year": "2025"}, scope_user=USER,
        rules=rules, corpus={member["id"]: member for member in resolved.resolved_members},
        package=resolved.package,
    )
    context = marshal_live_run_context(
        run_id=run_id, state=state, currency=currency, rules=rules, parameters=parameters,
        canon=load_canon(schemas),
        adoption_pin={"role": "adoption", "id": package["id"], "version": "v4"},
        governance_pins=[], family_declarations=families, closure_mappings=mappings,
        fact_types=fact_types, input_bindings=bindings, collect_source_names=collect_names,
        emission_only_source_names=list(material.emission_only_names), authorization=authorization,
        reporting_year=2025, parameter_index=material.parameter_index,
        claim_applicability=current_claim_applicability(acts, schemas.registry),
    )
    return resolved, context._context


class Track18RelationshipCorrection(unittest.TestCase):
    def test_correction_and_answer_lifecycle_through_saved_recovery_and_consumption(self) -> None:
        raw, log, registry, subjects = track17.Track17RelationshipApplicability()._scenario()
        with raw:
            first, second = subjects["first"], subjects["second"]
            # Both identified borrowings are on the first statement; the
            # second statement remains an independent inclusion.
            added = record_submission_durably(log, {
                "submission_id": "demo.track18.answer.second-on-first",
                "evidence_id": "demo.evidence.track18.answer.second-on-first",
                "actor": USER, "at": "2026-09-30T13:00:00Z",
                "borrowing_ref": second["borrowing"], "schooling_fact_id": second["school"],
                "statement_fact_id": first["statement"], "financing_response": "unanswered",
                "inclusion_response": "yes", "interest_portion_response": "unknown",
            }, registry)["claims"]["statement-inclusion"]
            _append_v36_adoption(log, registry)

            def recovered(tag: str) -> tuple[tuple[dict[str, Any], ...], dict[str, dict[str, Any]]]:
                fresh = ActLog(log.path.parent, registry)
                acts = fresh.read().acts
                _resolved, forward, reference = _run_v36(acts, f"demo.track18.{tag}")
                self.assertEqual(_surface(forward), _surface(reference))
                return acts, _published(forward)

            first_old, second_old = first["statement-inclusion"], added
            first_symbol = f"{INCLUSION_OUTPUT}|{first_old['fact_id']}"
            second_symbol = f"{INCLUSION_OUTPUT}|{second_old['fact_id']}"
            unaffected_symbol = f"{INCLUSION_OUTPUT}|{second['statement-inclusion']['fact_id']}"
            before_acts, before = recovered("before-correction")
            self.assertTrue({first_symbol, second_symbol, unaffected_symbol}.issubset(before))

            # A known amount-only correction is explicitly identified in this
            # action. Existing inclusion claims stay usable and re-pin the new
            # current statement finding; the other statement stays identical.
            statement_fact = facts_of(project(before_acts, registry).fact_state)[first["statement"]]
            stale_amount_review = prepare_review(
                log, registry, review_id="demo.track18.review.stale-amount-only",
                shown_at="2026-09-30T13:00:20Z", borrowing_refs=(first["borrowing"], second["borrowing"]),
                schooling_fact_ids=(first["school"], second["school"]),
                statement_fact_ids=(first["statement"], second["statement"]),
            )
            # ADR 0077 Part 5 refuses this unscoped write on the recorder's log; it is
            # written as pre-step history to reach the stale-review refusal.
            track14._append_source(track17._pre_step_writer(log), registry, STATEMENT_TYPE,
                                   tuple(statement_fact.keys), 1600.0,
                                   "track18-stale-review-source-change")
            with self.assertRaisesRegex(RelationshipRecordingRefused, "prepared review changed"):
                apply_statement_correction_review(
                    log, registry, review=stale_amount_review, statement_fact_id=first["statement"],
                    scope="amount-only", borrowing_ref=None, finding_id=None, actor=USER,
                    at="2026-09-30T13:00:25Z", submission_id="demo.track18.stale-amount-scope",
                    evidence_id="demo.evidence.track18.stale-amount-scope",
                    corrected_box1_total=1775.0,
                    source_correction_id="demo.track18.stale-amount-correction",
                )
            stale_acts, stale_observations = recovered("source-changed-before-scope")
            stale_state = project(stale_acts, registry)
            self.assertIn(first["statement-inclusion"]["finding_id"],
                          compute_currency(stale_state).current_finding_ids)
            # ADR 0077 Part 5 replay: both inclusions on the changed statement
            # are current but not joined to the unreviewed 1600; each is a
            # marker. The other statement's inclusion is joined as before.
            self.assertNotIn(first_symbol, stale_observations)
            self.assertNotIn(second_symbol, stale_observations)
            self.assertEqual(stale_observations[unaffected_symbol], before[unaffected_symbol])
            _stale_resolved, stale_context = _marshal_v36(stale_acts, "demo.track18.source-changed-before-scope")
            track17._assert_replay_omits(self, stale_context, stale_acts, registry, [first_old, second_old])
            amount_review = prepare_review(
                log, registry, review_id="demo.track18.review.amount-only",
                shown_at="2026-09-30T13:00:30Z", borrowing_refs=(first["borrowing"], second["borrowing"]),
                schooling_fact_ids=(first["school"], second["school"]),
                statement_fact_ids=(first["statement"], second["statement"]),
            )
            original_batch = log.append_batch
            intermediate: dict[str, Any] = {}

            # Track 7: the scope evidence and the corrected source are one
            # batch. A crash during it leaves the log as it is just before it.
            def inspect_before_the_save(items: Sequence[dict[str, Any]], expected_revision: int) -> int:
                if not intermediate:
                    fresh = ActLog(log.path.parent, registry)
                    intermediate["acts"] = fresh.read().acts
                    intermediate["batch"] = list(items)
                    _resolved, forward, reference = _run_v36(
                        intermediate["acts"], "demo.track18.amount-only-before-the-save")
                    self.assertEqual(_surface(forward), _surface(reference))
                    intermediate["observations"] = _published(forward)
                    intermediate["current_value"] = [
                        finding["value"] for finding_id, finding in
                        project(intermediate["acts"], registry).findings.items()
                        if finding_id in compute_currency(project(intermediate["acts"], registry)).current_finding_ids
                        and finding.get("fact_id") == first["statement"]
                    ][0]
                return original_batch(items, expected_revision)

            setattr(log, "append_batch", inspect_before_the_save)
            amount_answer = apply_statement_correction_review(
                log, registry, review=amount_review, statement_fact_id=first["statement"],
                scope="amount-only", borrowing_ref=None, finding_id=None, actor=USER,
                at="2026-09-30T13:00:31Z", submission_id="demo.track18.amount-only-scope",
                evidence_id="demo.evidence.track18.amount-only-scope",
                corrected_box1_total=1775.0, source_correction_id="demo.track18.amount-only-correction",
            )
            setattr(log, "append_batch", original_batch)
            self.assertEqual(intermediate["current_value"], 1600.0)
            self.assertEqual(intermediate["observations"], stale_observations)
            # The scope evidence leads the save, ahead of the corrected source;
            # the log before the save holds neither.
            self.assertNotIn("demo.evidence.track18.amount-only-scope",
                             project(intermediate["acts"], registry).evidence)
            first_act = intermediate["batch"][0]
            self.assertEqual(first_act["kind"], "evidence-submitted")
            intermediate_evidence = first_act["payload"]["evidence"]["content"]
            self.assertEqual(intermediate_evidence["recognition_context"]["statement_correction"]
                             ["included_borrowings_changed"], False)
            self.assertEqual([row["kind"] for row in intermediate["batch"]][-1], "assertion")
            amount_acts, amount = recovered("amount-only")
            # The reviewed correction re-binds both inclusions: no marker remains.
            _amount_resolved, amount_context = _marshal_v36(amount_acts, "demo.track18.amount-only")
            track17._assert_replay_omits(self, amount_context, amount_acts, registry, [])
            amount_evidence = project(amount_acts, registry).evidence[amount_answer["evidence_id"]]
            self.assertEqual(amount_evidence.evidence["content"]["recognition_context"]
                             ["statement_correction"]["included_borrowings_changed"], False)
            self.assertEqual(set(amount), set(before))
            self.assertEqual(amount[unaffected_symbol], before[unaffected_symbol])
            current_statement = [finding for fid, finding in project(amount_acts, registry).findings.items()
                                 if fid in compute_currency(project(amount_acts, registry)).current_finding_ids
                                 and finding.get("fact_id") == first["statement"]][0]
            self.assertIn({"role": "input", "id": current_statement["id"], "version": "v1",
                           "origin": "assertion"}, amount[first_symbol]["pins"])
            self.assertIn({"role": "input", "id": current_statement["id"], "version": "v1",
                           "origin": "assertion"}, amount[second_symbol]["pins"])
            self.assertIn(amount_answer["evidence_id"], current_statement["evidence_ids"])

            # Prove the current defect before repair: another ordinary no is
            # stored, but does not end the old affirmative support.
            record_submission_durably(log, {
                "submission_id": "demo.track18.ordinary-no-defect",
                "evidence_id": "demo.evidence.track18.ordinary-no-defect",
                "actor": USER, "at": "2026-09-30T13:01:00Z",
                "borrowing_ref": first["borrowing"], "schooling_fact_id": first["school"],
                "statement_fact_id": first["statement"], "financing_response": "unanswered",
                "inclusion_response": "no", "interest_portion_response": "unknown",
            }, registry)
            defect_acts, defect = recovered("ordinary-no-defect")
            self.assertIn(first_symbol, defect)
            defect_state = project(defect_acts, registry)
            old_current = compute_currency(defect_state).current_finding_ids
            self.assertIn(first_old["finding_id"], old_current)
            self.assertEqual(defect_state.evidence["demo.evidence.track18.ordinary-no-defect"]
                             .evidence["content"]["responses"]["inclusion_response"], "no")

            # A reviewed yes corrects the prior affirmative with new answer
            # provenance. The old finding remains historical and the exact
            # pair becomes current under a new finding identity.
            yes_review = prepare_review(
                log, registry, review_id="demo.track18.review.yes-correction",
                shown_at="2026-09-30T13:01:30Z", borrowing_refs=(first["borrowing"],),
                schooling_fact_ids=(first["school"],), statement_fact_ids=(first["statement"],),
            )
            yes_correction = correct_review_claim(
                log, registry, finding_id=first_old["finding_id"], review=yes_review,
                borrowing_ref=first["borrowing"], schooling_fact_id=first["school"],
                statement_fact_id=first["statement"], financing_response="unanswered",
                inclusion_response="yes", actor=USER, at="2026-09-30T13:01:31Z",
                submission_id="demo.track18.yes-correction", evidence_id="demo.evidence.track18.yes-correction",
            )
            yes_acts, after_yes = recovered("yes-correction")
            yes_claim = yes_correction["claims"]["statement-inclusion"]
            self.assertIn(first_symbol, after_yes)
            self.assertIn({"role": "input", "id": yes_claim["finding_id"], "version": "v1",
                           "origin": "assertion"}, after_yes[first_symbol]["pins"])
            self.assertNotIn({"role": "input", "id": first_old["finding_id"], "version": "v1",
                              "origin": "assertion"}, after_yes[first_symbol]["pins"])
            yes_state = project(yes_acts, registry)
            self.assertIn(first_old["finding_id"], yes_state.findings)
            self.assertNotIn(first_old["finding_id"], compute_currency(yes_state).current_finding_ids)

            # An explicit removal names exactly one statement/borrowing pair.
            removal_review = prepare_review(
                log, registry, review_id="demo.track18.review.explicit-removal",
                shown_at="2026-09-30T13:02:00Z", borrowing_refs=(first["borrowing"], second["borrowing"]),
                schooling_fact_ids=(first["school"], second["school"]),
                statement_fact_ids=(first["statement"], second["statement"]),
            )
            removed = apply_statement_correction_review(
                log, registry, review=removal_review, statement_fact_id=first["statement"],
                scope="inclusion-removed", borrowing_ref=first["borrowing"],
                finding_id=yes_claim["finding_id"], actor=USER, at="2026-09-30T13:03:00Z",
                submission_id="demo.track18.explicit-removal", evidence_id="demo.evidence.track18.explicit-removal",
                corrected_box1_total=1880.0,
                source_correction_id="demo.track18.explicit-removal-source",
            )
            removed_acts, after_no = recovered("explicit-removal")
            no_state = project(removed_acts, registry)
            self.assertNotIn(yes_claim["finding_id"], compute_currency(no_state).current_finding_ids)
            self.assertNotIn(first_old["finding_id"], compute_currency(no_state).current_finding_ids)
            self.assertIn(first_old["finding_id"], no_state.findings)
            self.assertEqual(no_state.evidence[removed["evidence_id"]].evidence["content"]
                             ["responses"]["inclusion_response"], "no")
            self.assertNotIn(first_symbol, after_no)
            self.assertIn(second_symbol, after_no)
            self.assertIn(f"{FINANCE_OUTPUT}|{first['financing']['fact_id']}", after_no)
            self.assertEqual(no_state.evidence["demo.evidence.track17.answer.first"].evidence["content"]
                             ["interest_portion_response"], "unknown")
            self.assertEqual(after_no[unaffected_symbol], before[unaffected_symbol])

            # An explicitly added inclusion is recorded after source admission;
            # the intermediate recovered state cannot consume it against the
            # previous composition.
            addition_review = prepare_review(
                log, registry, review_id="demo.track18.review.explicit-addition",
                shown_at="2026-09-30T13:03:30Z", borrowing_refs=(first["borrowing"], second["borrowing"]),
                schooling_fact_ids=(first["school"], second["school"]),
                statement_fact_ids=(first["statement"], second["statement"]),
            )
            addition_intermediate: dict[str, Any] = {}
            original_batch = log.append_batch

            # Track 7: scope, corrected source and the added yes are one batch.
            # A crash during it leaves the log as it is just before it.
            def inspect_addition_before_the_save(items: Sequence[dict[str, Any]], expected_revision: int) -> int:
                if not addition_intermediate:
                    fresh = ActLog(log.path.parent, registry)
                    acts = fresh.read().acts
                    _resolved, forward, reference = _run_v36(acts, "demo.track18.addition-before-the-save")
                    self.assertEqual(_surface(forward), _surface(reference))
                    addition_intermediate["published"] = _published(forward)
                    addition_intermediate["kinds"] = [row["kind"] for row in items]
                return original_batch(items, expected_revision)

            setattr(log, "append_batch", inspect_addition_before_the_save)
            added_correction = apply_statement_correction_review(
                log, registry, review=addition_review, statement_fact_id=first["statement"],
                scope="inclusion-added", borrowing_ref=first["borrowing"], finding_id=None,
                actor=USER, at="2026-09-30T13:03:31Z", submission_id="demo.track18.explicit-addition",
                evidence_id="demo.evidence.track18.explicit-addition-scope", corrected_box1_total=1900.0,
                source_correction_id="demo.track18.explicit-addition-source",
            )
            setattr(log, "append_batch", original_batch)
            self.assertNotIn(first_symbol, addition_intermediate["published"])
            # Scope evidence; corrected-source evidence, contribution, box 1;
            # the added pair's evidence, contribution and yes.
            self.assertEqual(addition_intermediate["kinds"], [
                "evidence-submitted", "evidence-submitted", "contribution", "assertion",
                "evidence-submitted", "contribution", "assertion"])
            added_acts, after_addition = recovered("explicit-addition")
            added_claim = added_correction["claims"]["statement-inclusion"]
            self.assertIn(first_symbol, after_addition)
            self.assertEqual(added_claim["evidence_id"], "demo.evidence.track18.explicit-addition-scope.affirmative")
            source_finding = project(added_acts, registry).findings[
                added_correction["source_correction"]["source_finding_id"]]
            self.assertIn("demo.evidence.track18.explicit-addition-scope", source_finding["evidence_ids"])

            # For a genuinely uncertain correction, hold the identified pair
            # before appending the corrected statement source. No consumer can
            # observe stale support in the gap or after source recovery.
            uncertain_review = prepare_review(
                log, registry, review_id="demo.track18.review.uncertain",
                shown_at="2026-09-30T13:04:00Z", borrowing_refs=(first["borrowing"], second["borrowing"]),
                schooling_fact_ids=(first["school"], second["school"]),
                statement_fact_ids=(first["statement"], second["statement"]),
            )
            pre_uncertain_log = log.path.read_bytes()
            held = apply_statement_correction_review(
                log, registry, review=uncertain_review, statement_fact_id=first["statement"],
                scope="inclusion-uncertain", borrowing_ref=second["borrowing"],
                finding_id=second_old["finding_id"], actor=USER, at="2026-09-30T13:05:00Z",
                submission_id="demo.track18.uncertain-answer", evidence_id="demo.evidence.track18.uncertain-answer",
                corrected_box1_total=1999.0,
                source_correction_id="demo.track18.uncertain-source-correction",
            )
            held_acts, after_uncertain = recovered("uncertain")
            held_state = project(held_acts, registry)
            held_current = compute_currency(held_state).current_finding_ids
            self.assertIn(second_old["finding_id"], held_state.findings)
            self.assertNotIn(second_old["finding_id"], held_current)
            self.assertEqual(held_state.evidence[held["evidence_id"]].evidence["content"]
                             ["responses"]["inclusion_response"], "cannot-tell")
            self.assertNotIn(second_symbol, after_uncertain)
            self.assertIn(unaffected_symbol, after_uncertain)

            unresolved_fact_id = fact_id_for(INCLUSION_UNRESOLVED, tuple(
                facts_of(held_state.fact_state, include_displaced=True)[second_old["fact_id"]].keys))
            unresolved_rows = [finding for finding_id, finding in held_state.findings.items()
                               if finding_id in held_current and finding.get("fact_id") == unresolved_fact_id]
            self.assertEqual(len(unresolved_rows), 1)
            self.assertEqual(unresolved_rows[0]["value"], "sli.statement-inclusion.unresolved")
            self.assertEqual(unresolved_rows[0]["evidence_ids"], [held["evidence_id"]])
            unresolved_symbol = f"{UNRESOLVED_OUTPUT}|{unresolved_fact_id}"
            self.assertIn(unresolved_symbol, after_uncertain)
            unresolved_finding = unresolved_rows[0]
            unresolved_finding_id = next(fid for fid, row in held_state.findings.items()
                                         if row is unresolved_finding)
            unresolved_source = [finding for finding_id, finding in held_state.findings.items()
                                 if finding_id in held_current and finding.get("fact_id") == first["statement"]][0]
            self.assertIn({"role": "input", "id": unresolved_finding["id"], "version": "v1",
                           "origin": "assertion"}, after_uncertain[unresolved_symbol]["pins"])
            self.assertIn({"role": "input", "id": unresolved_source["id"], "version": "v1",
                           "origin": "assertion"}, after_uncertain[unresolved_symbol]["pins"])
            self.assertIn(first_symbol, after_uncertain)
            self.assertNotIn(unresolved_symbol, after_no)
            self.assertIn(held["evidence_id"], held_state.evidence)
            self.assertIn(unaffected_symbol, after_uncertain)
            self.assertIn(held["evidence_id"], unresolved_source.get("evidence_ids", []))

            # A later yes resolves that exact unresolved pair. Its ordinary
            # reviewed successor retires the neutral status while preserving
            # that status and answer in history.
            yes_after_uncertain_review = prepare_review(
                log, registry, review_id="demo.track18.review.yes-after-uncertain",
                shown_at="2026-09-30T13:05:30Z", borrowing_refs=(second["borrowing"],),
                schooling_fact_ids=(second["school"],), statement_fact_ids=(first["statement"],),
            )
            yes_after_uncertain = correct_review_claim(
                log, registry, finding_id=second_old["finding_id"], review=yes_after_uncertain_review,
                borrowing_ref=second["borrowing"], schooling_fact_id=second["school"],
                statement_fact_id=first["statement"], financing_response="unanswered",
                inclusion_response="yes", actor=USER, at="2026-09-30T13:05:31Z",
                submission_id="demo.track18.yes-after-uncertain",
                evidence_id="demo.evidence.track18.yes-after-uncertain",
            )
            resolved_acts, after_yes_uncertain = recovered("yes-after-uncertain")
            resolved_state = project(resolved_acts, registry)
            self.assertIn(unresolved_finding_id, resolved_state.findings)
            self.assertNotIn(unresolved_finding_id, compute_currency(resolved_state).current_finding_ids)
            self.assertNotIn(unresolved_symbol, after_yes_uncertain)
            self.assertIn(second_symbol, after_yes_uncertain)
            self.assertIn(unaffected_symbol, after_yes_uncertain)
            self.assertEqual(yes_after_uncertain["claims"]["statement-inclusion"]["evidence_id"],
                             "demo.evidence.track18.yes-after-uncertain")

            # A replacement whose current source subject was not shown remains
            # unresolved: the workflow refuses to bind it by a supplied label,
            # amount, order, or opaque address.
            replacement_review = prepare_review(
                log, registry, review_id="demo.track18.review.unidentified-replacement",
                shown_at="2026-09-30T13:05:40Z", borrowing_refs=(second["borrowing"],),
                schooling_fact_ids=(second["school"],), statement_fact_ids=(first["statement"],),
            )
            with self.assertRaisesRegex(RelationshipRecordingRefused, "was not shown in the review"):
                apply_statement_correction_review(
                    log, registry, review=replacement_review,
                    statement_fact_id="demo.track18.unidentified-replacement-statement",
                    scope="amount-only", borrowing_ref=None, finding_id=None,
                    corrected_box1_total=2100.0, source_correction_id="demo.track18.unidentified-replacement",
                    actor=USER, at="2026-09-30T13:05:41Z",
                    submission_id="demo.track18.unidentified-replacement", evidence_id="demo.evidence.track18.unidentified-replacement",
                )

            # Compare no and cannot-tell for the same previously affirmative
            # pair from the same saved pre-uncertainty revision. Both runners
            # agree; no has no unresolved observation, while cannot-tell has
            # an exact-pair unresolved observation with answer and source pins.
            with tempfile.TemporaryDirectory(prefix="sli-track18-no-variant-") as directory:
                (Path(directory) / "acts.jsonl").write_bytes(pre_uncertain_log)
                no_log = ActLog(Path(directory), registry)
                no_review = prepare_review(
                    no_log, registry, review_id="demo.track18.review.same-pair-no",
                    shown_at="2026-09-30T13:04:30Z", borrowing_refs=(second["borrowing"],),
                    schooling_fact_ids=(second["school"],), statement_fact_ids=(first["statement"],),
                )
                no_answer = answer_review_claim(
                    no_log, registry, finding_id=second_old["finding_id"], review=no_review,
                    borrowing_ref=second["borrowing"], schooling_fact_id=second["school"],
                    statement_fact_id=first["statement"], financing_response="unanswered",
                    inclusion_response="no", actor=USER, at="2026-09-30T13:04:31Z",
                    submission_id="demo.track18.same-pair-no", evidence_id="demo.evidence.track18.same-pair-no",
                )
                no_acts = ActLog(no_log.path.parent, registry).read().acts
                _resolved, no_forward, no_reference = _run_v36(no_acts, "demo.track18.same-pair-no-forward")
                self.assertEqual(_surface(no_forward), _surface(no_reference))
                no_state = project(no_acts, registry)
                no_current = compute_currency(no_state).current_finding_ids
                self.assertIn(second_old["finding_id"], no_state.findings)
                self.assertNotIn(second_old["finding_id"], no_current)
                self.assertEqual(no_state.evidence[no_answer["evidence_id"]].evidence["content"]
                                 ["responses"]["inclusion_response"], "no")
                no_publications = _published(no_forward)
                self.assertNotIn(second_symbol, no_publications)
                self.assertNotIn(unresolved_symbol, no_publications)
                self.assertIn(unaffected_symbol, no_publications)
                self.assertNotEqual(set(no_publications), set(after_uncertain))

            # A later explicit no resolves an already-current cannot-tell
            # status for the same pair, preserving both answers and all
            # predecessor history while leaving the independent pair usable.
            with tempfile.TemporaryDirectory(prefix="sli-track18-no-after-uncertain-") as directory:
                (Path(directory) / "acts.jsonl").write_bytes(pre_uncertain_log)
                resolved_no_log = ActLog(Path(directory), registry)
                uncertain_variant_review = prepare_review(
                    resolved_no_log, registry, review_id="demo.track18.review.uncertain-before-no",
                    shown_at="2026-09-30T13:04:10Z", borrowing_refs=(second["borrowing"],),
                    schooling_fact_ids=(second["school"],), statement_fact_ids=(first["statement"],),
                )
                uncertain_variant = apply_statement_correction_review(
                    resolved_no_log, registry, review=uncertain_variant_review,
                    statement_fact_id=first["statement"], scope="inclusion-uncertain",
                    borrowing_ref=second["borrowing"], finding_id=second_old["finding_id"],
                    corrected_box1_total=1999.0,
                    source_correction_id="demo.track18.uncertain-before-no-source",
                    actor=USER, at="2026-09-30T13:04:11Z",
                    submission_id="demo.track18.uncertain-before-no",
                    evidence_id="demo.evidence.track18.uncertain-before-no",
                )
                no_after_review = prepare_review(
                    resolved_no_log, registry, review_id="demo.track18.review.no-after-uncertain",
                    shown_at="2026-09-30T13:04:20Z", borrowing_refs=(second["borrowing"],),
                    schooling_fact_ids=(second["school"],), statement_fact_ids=(first["statement"],),
                )
                resolved_no = apply_statement_correction_review(
                    resolved_no_log, registry, review=no_after_review,
                    statement_fact_id=first["statement"], scope="inclusion-removed",
                    borrowing_ref=second["borrowing"], finding_id=second_old["finding_id"],
                    corrected_box1_total=1999.0,
                    source_correction_id="demo.track18.no-after-uncertain-source",
                    actor=USER, at="2026-09-30T13:04:21Z",
                    submission_id="demo.track18.no-after-uncertain",
                    evidence_id="demo.evidence.track18.no-after-uncertain",
                )
                no_after_acts = ActLog(resolved_no_log.path.parent, registry).read().acts
                no_after_state = project(no_after_acts, registry)
                _resolved, no_after_forward, no_after_reference = _run_v36(
                    no_after_acts, "demo.track18.no-after-uncertain")
                self.assertEqual(_surface(no_after_forward), _surface(no_after_reference))
                no_after_publications = _published(no_after_forward)
                self.assertNotIn(second_symbol, no_after_publications)
                self.assertNotIn(unresolved_symbol, no_after_publications)
                self.assertIn(unaffected_symbol, no_after_publications)
                self.assertIn(second_old["finding_id"], no_after_state.findings)
                self.assertIn(uncertain_variant["evidence_id"], no_after_state.evidence)
                self.assertEqual(no_after_state.evidence[resolved_no["evidence_id"]].evidence["content"]
                                 ["responses"]["inclusion_response"], "no")
                no_unresolved_finding = next(
                    fid for fid, row in no_after_state.findings.items()
                    if row.get("fact_id") == unresolved_fact_id)
                self.assertIn(no_unresolved_finding, no_after_state.findings)
                self.assertNotIn(no_unresolved_finding, compute_currency(no_after_state).current_finding_ids)

    def test_answer_write_failure_saves_nothing(self) -> None:
        # Track 7: the retraction, the cannot-tell answer and its unresolved
        # status are one batch. A failed write leaves the affirmation current
        # and nothing of the answer.
        raw, log, registry, subjects = track17.Track17RelationshipApplicability()._scenario()
        with raw:
            first = subjects["first"]
            _append_v36_adoption(log, registry)
            review = prepare_review(
                log, registry, review_id="demo.track18.review.answer-append-failure",
                shown_at="2026-09-30T14:00:00Z", borrowing_refs=(first["borrowing"],),
                schooling_fact_ids=(first["school"],), statement_fact_ids=(first["statement"],),
            )
            before_acts = ActLog(log.path.parent, registry).read().acts
            _resolved, before_forward, _reference = _run_v36(before_acts, "demo.track18.before-failed-answer")
            original_batch = log.append_batch

            def fail_answer_batch(items: Sequence[dict[str, Any]], expected_revision: int) -> int:
                raise ActLogError("synthetic answer write interruption")

            setattr(log, "append_batch", fail_answer_batch)
            with self.assertRaisesRegex(ActLogError, "synthetic answer write interruption"):
                answer_review_claim(
                    log, registry, finding_id=first["statement-inclusion"]["finding_id"],
                    review=review, borrowing_ref=first["borrowing"],
                    schooling_fact_id=first["school"], statement_fact_id=first["statement"],
                    financing_response="unanswered", inclusion_response="cannot-tell",
                    actor=USER, at="2026-09-30T14:00:01Z",
                    submission_id="demo.track18.interrupted-cannot-tell",
                    evidence_id="demo.evidence.track18.interrupted-cannot-tell",
                )
            setattr(log, "append_batch", original_batch)
            fresh = ActLog(log.path.parent, registry)
            acts = fresh.read().acts
            self.assertEqual(acts, before_acts)
            state = project(acts, registry)
            current_ids = compute_currency(state).current_finding_ids
            predecessor = first["statement-inclusion"]["finding_id"]
            self.assertIn(predecessor, current_ids)
            self.assertNotIn("demo.evidence.track18.interrupted-cannot-tell", state.evidence)
            _resolved, forward, reference = _run_v36(acts, "demo.track18.interrupted-recovery")
            self.assertEqual(_surface(forward), _surface(reference))
            self.assertEqual(_published(forward), _published(before_forward))
            inclusion_symbol = f"{INCLUSION_OUTPUT}|{first['statement-inclusion']['fact_id']}"
            unresolved_fact = facts_of(state.fact_state, include_displaced=True)[
                first["statement-inclusion"]["fact_id"]
            ]
            unresolved_symbol = (f"{UNRESOLVED_OUTPUT}|" + fact_id_for(
                INCLUSION_UNRESOLVED, tuple(unresolved_fact.keys)))
            self.assertIn(inclusion_symbol, _published(forward))
            self.assertNotIn(unresolved_symbol, _published(forward))

    def test_no_after_unresolved_write_failure_saves_nothing(self) -> None:
        # Track 7: ending the unresolved status and saving the no are one
        # batch. A failed write leaves the unresolved status current.
        raw, log, registry, subjects = track17.Track17RelationshipApplicability()._scenario()
        with raw:
            first, second = subjects["first"], subjects["second"]
            _append_v36_adoption(log, registry)
            uncertain_review = prepare_review(
                log, registry, review_id="demo.track18.review.partial-no-seed",
                shown_at="2026-09-30T15:00:00Z", borrowing_refs=(first["borrowing"],),
                schooling_fact_ids=(first["school"],), statement_fact_ids=(first["statement"],),
            )
            uncertain = answer_review_claim(
                log, registry, finding_id=first["statement-inclusion"]["finding_id"],
                review=uncertain_review, borrowing_ref=first["borrowing"],
                schooling_fact_id=first["school"], statement_fact_id=first["statement"],
                financing_response="unanswered", inclusion_response="cannot-tell",
                actor=USER, at="2026-09-30T15:00:01Z",
                submission_id="demo.track18.partial-no-seed",
                evidence_id="demo.evidence.track18.partial-no-seed",
            )
            no_review = prepare_review(
                log, registry, review_id="demo.track18.review.partial-no",
                shown_at="2026-09-30T15:00:02Z", borrowing_refs=(first["borrowing"],),
                schooling_fact_ids=(first["school"],), statement_fact_ids=(first["statement"],),
            )
            before_acts = ActLog(log.path.parent, registry).read().acts
            original_batch = log.append_batch

            def fail_no_batch(items: Sequence[dict[str, Any]], expected_revision: int) -> int:
                raise ActLogError("synthetic no answer write interruption")

            setattr(log, "append_batch", fail_no_batch)
            with self.assertRaisesRegex(ActLogError, "synthetic no answer write interruption"):
                answer_review_claim(
                    log, registry, finding_id=first["statement-inclusion"]["finding_id"],
                    review=no_review, borrowing_ref=first["borrowing"],
                    schooling_fact_id=first["school"], statement_fact_id=first["statement"],
                    financing_response="unanswered", inclusion_response="no",
                    actor=USER, at="2026-09-30T15:00:03Z",
                    submission_id="demo.track18.partial-no-answer",
                    evidence_id="demo.evidence.track18.partial-no-answer",
                )
            setattr(log, "append_batch", original_batch)
            recovered_acts = ActLog(log.path.parent, registry).read().acts
            self.assertEqual(recovered_acts, before_acts)
            state = project(recovered_acts, registry)
            current_ids = compute_currency(state).current_finding_ids
            self.assertIn(first["statement-inclusion"]["finding_id"], state.findings)
            self.assertNotIn(first["statement-inclusion"]["finding_id"], current_ids)
            self.assertIn(uncertain["evidence_id"], state.evidence)
            self.assertNotIn("demo.evidence.track18.partial-no-answer", state.evidence)
            unresolved_fact = facts_of(state.fact_state, include_displaced=True)[
                first["statement-inclusion"]["fact_id"]]
            unresolved_id = fact_id_for(INCLUSION_UNRESOLVED, tuple(unresolved_fact.keys))
            unresolved_findings = [fid for fid, row in state.findings.items()
                                  if row.get("fact_id") == unresolved_id]
            self.assertEqual(len(unresolved_findings), 1)
            self.assertIn(unresolved_findings[0], current_ids)
            _resolved, forward, reference = _run_v36(recovered_acts, "demo.track18.partial-no-recovery")
            self.assertEqual(_surface(forward), _surface(reference))
            publications = _published(forward)
            self.assertNotIn(f"{INCLUSION_OUTPUT}|{first['statement-inclusion']['fact_id']}", publications)
            self.assertIn(f"{UNRESOLVED_OUTPUT}|{unresolved_id}", publications)
            self.assertIn(f"{INCLUSION_OUTPUT}|{second['statement-inclusion']['fact_id']}", publications)


if __name__ == "__main__":
    unittest.main()
