"""Track 15: versioned admission and neutral per-claim SLI observations."""
from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.live import _resolve_run_authorization, _resolved_run_material
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.marshal import marshal_live_run_context
from packages.derivation.package_validation import (
    citizen_checksum, load_published_citizen_checksums, package_instance_checksum, validate_package,
)
from packages.derivation.production_resolver import PublicationSurface, Refusal, resolve_production_package
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import run
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import facts_of
from packages.kernel.findings import project
from packages.tax.sli_relationship_recording import (
    FINANCING, SCHOOLING, STATEMENT_INCLUSION, correct_relationship_claim_durably,
    current_claim_applicability, record_submission_durably,
    withdraw_relationship_claim_durably,
)
from tests.support import act, demo_entity
import tests.test_sli_relationship_recording as track14

ROOT = Path(__file__).resolve().parents[1]
CONTENT = track14.CONTENT
FIXTURE = ROOT / "packages/sample_data/student_loan_relationship_source"
REGISTRY = CONTENT / "published-packages.v34.json"
RELEASES = FIXTURE / "publication_surface/releases"
PACKAGE_FILE = FIXTURE / "package.sli-relationship-source-diagnostic.v2.json"
PACKAGE_ID = "demo.tax.2025.package.sli-relationship-source-diagnostic"
FINANCE_RULE = "demo.rule.tax.2025.sli.financing-observation"
INCLUSION_RULE = "demo.rule.tax.2025.sli.statement-inclusion-observation"
FINANCE_OUTPUT = "demo.tax.2025.sli.financing-observation"
INCLUSION_OUTPUT = "demo.tax.2025.sli.statement-inclusion-observation"
USER = "demo.user.filer"
SCOPE = {"jurisdiction": "us", "year": "2025"}


def _surface() -> PublicationSurface:
    return PublicationSurface(RELEASES, REGISTRY, ROOT / "packages")


def _add_adoption(log: ActLog) -> None:
    package = json.loads(PACKAGE_FILE.read_text("utf-8"))
    release_path = RELEASES / "demo.release.sli-relationship-source.2025.v34.json"
    release = json.loads(release_path.read_text("utf-8"))
    item = act(log.read().revision, "package-adoption", {
        "package": {"id": package["id"], "version": package["version"],
                    "checksum": package["package_checksum"]},
        "release": {"id": release["id"], "version": release["version"],
                    "checksum": hashlib.sha256(release_path.read_bytes()).hexdigest()},
        "scope": SCOPE, "revision": 1,
    })
    item["actor"] = USER
    log.append(item, expected_revision=log.read().revision)


def _run_both(acts: tuple[dict[str, Any], ...], run_id: str) -> tuple[Any, Any, Any]:
    schemas = DerivationSchemas()
    resolved = resolve_production_package(
        acts, run_scope=SCOPE, scope_user=USER, workspace_revision=len(acts),
        surface=_surface(), schemas=schemas,
    )
    if isinstance(resolved, Refusal):
        raise AssertionError(f"versioned relationship package refused: {resolved!r}")
    if resolved.release_id != "demo.release.sli-relationship-source.2025":
        raise AssertionError(f"unexpected release identity: {resolved.release_id}")
    if (resolved.package["id"], resolved.package["version"]) != (PACKAGE_ID, "v2"):
        raise AssertionError("resolver selected an unexpected diagnostic package")
    adoption = next(row for row in acts if row.get("kind") == "package-adoption")
    release_file = RELEASES / "demo.release.sli-relationship-source.2025.v34.json"
    if adoption["payload"]["release"] != {
        "id": resolved.release_id, "version": "v34",
        "checksum": hashlib.sha256(release_file.read_bytes()).hexdigest(),
    }:
        raise AssertionError("adoption does not pin the exact verified release bytes")
    state = project(acts, schemas.registry)
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
        canon=load_canon(schemas),
        adoption_pin={"role": "adoption", "id": resolved.package["id"],
                      "version": resolved.package["version"]},
        governance_pins=[], family_declarations=families, closure_mappings=mappings,
        fact_types=fact_types, input_bindings=bindings, collect_source_names=collect_names,
        emission_only_source_names=list(material.emission_only_names),
        authorization=authorization, reporting_year=2025,
        parameter_index=material.parameter_index,
    )
    return resolved, run(context._context, schemas), run_reference(context._context, schemas)


def _published(result: Any) -> dict[str, dict[str, Any]]:
    return {item.finding["symbol"]: item.finding for item in result.publications}


def _assert_same_result(test: unittest.TestCase, before: dict[str, dict[str, Any]],
                        after: dict[str, dict[str, Any]], symbol: str) -> None:
    prior, current = before[symbol], after[symbol]
    test.assertEqual((prior["id"], prior["value"], prior["pins"]),
                     (current["id"], current["value"], current["pins"]))


class VersionedSourceConsumer(unittest.TestCase):
    def test_publication_is_exact_and_package_is_normally_admitted(self) -> None:
        registry = json.loads(REGISTRY.read_text("utf-8"))
        release_path = RELEASES / "demo.release.sli-relationship-source.2025.v34.json"
        release = json.loads(release_path.read_text("utf-8"))
        self.assertEqual((release["schema"], release["id"], release["version"]),
                         ("release-registry.v1", "demo.release.sli-relationship-source.2025", "v34"))
        self.assertEqual(len(hashlib.sha256(release_path.read_bytes()).hexdigest()), 64)
        bundle = json.loads((CONTENT / "sli-relationship-source.bundle.json").read_text("utf-8"))
        citizen = next(row for row in registry["citizens"]
                       if row["id"] == bundle["id"] and row["version"] == "v1")
        self.assertEqual(citizen["checksum"], citizen_checksum(bundle))
        self.assertEqual(release["package_registry_sha256"],
                         hashlib.sha256(REGISTRY.read_bytes()).hexdigest())
        self.assertEqual(load_published_citizen_checksums(REGISTRY)[(bundle["id"], "v1")],
                         citizen_checksum(bundle))
        package = json.loads(PACKAGE_FILE.read_text("utf-8"))
        self.assertEqual(package["package_checksum"], package_instance_checksum(package))
        corpus: dict[tuple[str, str], dict[str, Any]] = {}
        for path in [*CONTENT.glob("*.json"), *FIXTURE.glob("*.json")]:
            try:
                body = json.loads(path.read_text("utf-8"))
            except (OSError, ValueError):
                continue
            if isinstance(body, dict) and isinstance(body.get("id"), str) and isinstance(body.get("version"), str):
                corpus[(body["id"], body["version"])] = body
        admitted = validate_package(package, corpus, DerivationSchemas())
        self.assertTrue(admitted.ok, [issue.detail for issue in admitted.issues])
        self.assertEqual({row["id"] for row in admitted.resolved_members}, {
            "tax.us.2025.sli-relationship-source",
            "demo.tax.2025.sli-relationship-observation-vocabulary",
            FINANCE_RULE, INCLUSION_RULE,
        })
        self.assertEqual({row["id"] for row in registry["citizens"] if row["id"].startswith("demo.rule.tax.2025.sli.")},
                         {FINANCE_RULE, INCLUSION_RULE})
        citizen_pins = {(row["id"], row["version"]): row["checksum"] for row in registry["citizens"]}
        for member in admitted.resolved_members:
            key = (member["id"], member["version"])
            self.assertEqual(citizen_pins[key], citizen_checksum(member))
        package_pins = {(row["id"], row["version"]): row["checksum"] for row in registry["packages"]}
        self.assertEqual(package_pins[(package["id"], package["version"])],
                         package_instance_checksum(package))

    def test_actlog_recovery_both_runners_and_independent_claim_lifecycles(self) -> None:
        helper = track14.OrdinaryRelationshipRecording()
        raw, log, registry, refs = helper._workspace()
        with raw:
            # Add a second, distinct borrowing, school and statement with descriptions
            # equal to the first. No name, amount, label or position selects a subject.
            second_borrowing = "demo.track14.borrowing.autumn-twin"
            from packages.tax.sli_relationship_recording import introduce_borrowing_reference_durably
            introduce_borrowing_reference_durably(
                log, registry, reference_id=second_borrowing, description="Autumn borrowing",
                actor=USER, at="2026-09-29T12:10:00Z",
            )
            twin_period = "demo.track14.period.autumn-twin"
            twin_lender = "demo.track14.lender.cedar-twin"
            twin_statement = "demo.track14.statement.2025-twin"
            for identity, label, kind in (
                (twin_period, "Autumn 2024", "tax.us.educational-period"),
                (twin_lender, "Cedar Servicing", "tax.us.student-loan-lender"),
                (twin_statement, "2025 Form 1098-E", "tax.us.1098e-statement"),
            ):
                log.append(act(log.read().revision, "entity-introduced",
                               {"entity": demo_entity(identity, label, kind)}),
                           expected_revision=log.read().revision)
            twin_school = track14._append_source(
                log, registry, SCHOOLING,
                (("period", twin_period), ("institution", "demo.track14.institution.river"),
                 ("programme", "demo.track14.programme.bsc")),
                "Riverside College, BSc, autumn 2024", "twin-school",
            )
            twin_statement_fact = track14._append_source(
                log, registry, "tax.us.2025.f1098e.box1-student-loan-interest",
                (("lender", twin_lender), ("statement", twin_statement), ("tax-year", "2025")),
                1250.0, "twin-statement-box1",
            )
            first = record_submission_durably(log, {
                "submission_id": "demo.track15.answer.first", "evidence_id": "demo.evidence.track15.answer.first",
                "actor": USER, "at": "2026-09-29T12:11:00Z", "borrowing_ref": refs["borrowing"],
                "schooling_fact_id": refs["school"], "statement_fact_id": refs["statement"],
                "financing_response": "yes", "inclusion_response": "yes",
                "interest_portion_response": "unknown",
            }, registry)
            second = record_submission_durably(log, {
                "submission_id": "demo.track15.answer.second", "evidence_id": "demo.evidence.track15.answer.second",
                "actor": USER, "at": "2026-09-29T12:12:00Z", "borrowing_ref": second_borrowing,
                "schooling_fact_id": twin_school, "statement_fact_id": twin_statement_fact,
                "financing_response": "yes", "inclusion_response": "yes",
                "interest_portion_response": "unknown",
            }, registry)
            self.assertEqual(set(first["claims"]), {"financing", "statement-inclusion"})
            self.assertEqual(set(second["claims"]), {"financing", "statement-inclusion"})
            _add_adoption(log)

            def recovered_run(name: str) -> dict[str, dict[str, Any]]:
                fresh = ActLog(log.path.parent, registry)
                acts = fresh.read().acts
                _resolved, forward, reference = _run_both(acts, f"demo.track15.{name}")
                self.assertEqual(_published(forward), _published(reference))
                return _published(forward)

            initial = recovered_run("initial")
            self.assertEqual(set(initial), {
                f"{FINANCE_OUTPUT}|{first['claims']['financing']['fact_id']}",
                f"{FINANCE_OUTPUT}|{second['claims']['financing']['fact_id']}",
                f"{INCLUSION_OUTPUT}|{first['claims']['statement-inclusion']['fact_id']}",
                f"{INCLUSION_OUTPUT}|{second['claims']['statement-inclusion']['fact_id']}",
            })
            current_acts = ActLog(log.path.parent, registry).read().acts
            current_state = project(current_acts, registry)
            lattice = facts_of(current_state.fact_state)
            self.assertEqual(
                current_state.evidence[first["evidence_id"]].evidence["content"]["interest_portion_response"],
                "unknown",
            )
            for kind, claim in (
                ("financing", first["claims"]["financing"]),
                ("financing", second["claims"]["financing"]),
                ("statement-inclusion", first["claims"]["statement-inclusion"]),
                ("statement-inclusion", second["claims"]["statement-inclusion"]),
            ):
                fact = lattice[claim["fact_id"]]
                self.assertEqual(fact.fact_type_id, FINANCING if kind == "financing" else STATEMENT_INCLUSION)
                output_symbol = f"{FINANCE_OUTPUT if kind == 'financing' else INCLUSION_OUTPUT}|{claim['fact_id']}"
                row = initial[output_symbol]
                self.assertEqual(row["value"], f"sli.{kind}.observed")
                self.assertEqual(sorted(json.dumps(pin, sort_keys=True) for pin in row["pins"]), sorted(
                    json.dumps(pin, sort_keys=True) for pin in [
                    {"role":"adoption","id":PACKAGE_ID,"version":"v2"},
                    {"role":"computation","id":FINANCE_RULE if kind == "financing" else INCLUSION_RULE,
                     "version":"v1"},
                    {"role":"input","id":claim["finding_id"],"version":"v1","origin":"assertion"},
                ]))
            finance_facts = [lattice[claim["fact_id"]] for claim in
                             (first["claims"]["financing"], second["claims"]["financing"])]
            self.assertNotEqual(dict(finance_facts[0].keys)["borrowing"], dict(finance_facts[1].keys)["borrowing"])
            self.assertNotEqual(dict(finance_facts[0].keys)["period"], dict(finance_facts[1].keys)["period"])

            # A statement amount correction changes its value, not the keyed inclusion observation.
            statement_keys = (("lender", "demo.track14.lender.cedar"),
                              ("statement", "demo.track14.statement.2025"), ("tax-year", "2025"))
            track14._append_source(log, registry, "tax.us.2025.f1098e.box1-student-loan-interest",
                           statement_keys, 1750.0, "first-statement-corrected-amount")
            amount_corrected = recovered_run("amount-correction")
            self.assertEqual(amount_corrected[f"{INCLUSION_OUTPUT}|{first['claims']['statement-inclusion']['fact_id']}"]["id"],
                             initial[f"{INCLUSION_OUTPUT}|{first['claims']['statement-inclusion']['fact_id']}"]["id"])
            self.assertEqual(amount_corrected[f"{INCLUSION_OUTPUT}|{second['claims']['statement-inclusion']['fact_id']}"]["id"],
                             initial[f"{INCLUSION_OUTPUT}|{second['claims']['statement-inclusion']['fact_id']}"]["id"])
            amount_applicability = {row["finding_id"]: row["applicability"]
                                    for row in current_claim_applicability(log.read().acts, registry)}
            # Track 6 read-side tie (ADR 0077 Part 5): a direct unscoped box 1 append
            # leaves the old inclusion unresolved, not applicable.
            self.assertEqual(amount_applicability[first["claims"]["statement-inclusion"]["finding_id"]],
                             "unresolved-applicability")

            # Correct and then withdraw the financing assertion for the first borrowing only.
            correction = correct_relationship_claim_durably(
                log, registry, finding_id=first["claims"]["financing"]["finding_id"],
                successor={"submission_id":"demo.track15.answer.finance-correction",
                           "evidence_id":"demo.evidence.track15.finance-correction",
                           "actor":USER,"at":"2026-09-29T12:13:00Z","borrowing_ref":refs["borrowing"],
                           "schooling_fact_id":twin_school,"statement_fact_id":"",
                           "financing_response":"yes","inclusion_response":"unanswered"},
                actor=USER, at="2026-09-29T12:13:00Z",
            )
            corrected = recovered_run("finance-corrected")
            old_finance_symbol = f"{FINANCE_OUTPUT}|{first['claims']['financing']['fact_id']}"
            self.assertNotIn(old_finance_symbol, corrected)
            self.assertIn(f"{FINANCE_OUTPUT}|{correction['claims']['financing']['fact_id']}", corrected)
            self.assertIn(f"{FINANCE_OUTPUT}|{second['claims']['financing']['fact_id']}", corrected)
            self.assertIn(f"{INCLUSION_OUTPUT}|{first['claims']['statement-inclusion']['fact_id']}", corrected)
            _assert_same_result(self, amount_corrected, corrected,
                                f"{FINANCE_OUTPUT}|{second['claims']['financing']['fact_id']}")
            for kind in ("statement-inclusion",):
                for claim in (first["claims"][kind], second["claims"][kind]):
                    _assert_same_result(self, amount_corrected, corrected,
                                        f"{INCLUSION_OUTPUT}|{claim['fact_id']}")
            withdraw_relationship_claim_durably(
                log, registry, finding_id=correction["claims"]["financing"]["finding_id"],
                actor=USER, at="2026-09-29T12:14:00Z",
            )
            after_finance_withdrawal = recovered_run("finance-withdrawn")
            self.assertNotIn(f"{FINANCE_OUTPUT}|{correction['claims']['financing']['fact_id']}",
                             after_finance_withdrawal)
            self.assertIn(f"{FINANCE_OUTPUT}|{second['claims']['financing']['fact_id']}", after_finance_withdrawal)
            self.assertIn(f"{INCLUSION_OUTPUT}|{first['claims']['statement-inclusion']['fact_id']}", after_finance_withdrawal)
            _assert_same_result(self, corrected, after_finance_withdrawal,
                                f"{FINANCE_OUTPUT}|{second['claims']['financing']['fact_id']}")
            for claim in (first["claims"]["statement-inclusion"], second["claims"]["statement-inclusion"]):
                _assert_same_result(self, corrected, after_finance_withdrawal,
                                    f"{INCLUSION_OUTPUT}|{claim['fact_id']}")

            # Correct and withdraw one statement-inclusion claim independently.
            corrected_inclusion = correct_relationship_claim_durably(
                log, registry, finding_id=first["claims"]["statement-inclusion"]["finding_id"],
                successor={"submission_id":"demo.track15.answer.inclusion-correction",
                           "evidence_id":"demo.evidence.track15.inclusion-correction",
                           "actor":USER,"at":"2026-09-29T12:15:00Z","borrowing_ref":second_borrowing,
                           "schooling_fact_id":"","statement_fact_id":refs["statement"],
                           "financing_response":"unanswered","inclusion_response":"yes"},
                actor=USER, at="2026-09-29T12:15:00Z",
            )
            inclusion_successor = corrected_inclusion["claims"]["statement-inclusion"]
            inclusion_corrected = recovered_run("inclusion-corrected")
            self.assertNotIn(f"{INCLUSION_OUTPUT}|{first['claims']['statement-inclusion']['fact_id']}",
                             inclusion_corrected)
            self.assertIn(f"{INCLUSION_OUTPUT}|{inclusion_successor['fact_id']}", inclusion_corrected)
            self.assertIn(f"{INCLUSION_OUTPUT}|{second['claims']['statement-inclusion']['fact_id']}", inclusion_corrected)
            _assert_same_result(self, after_finance_withdrawal, inclusion_corrected,
                                f"{INCLUSION_OUTPUT}|{second['claims']['statement-inclusion']['fact_id']}")
            withdraw_relationship_claim_durably(
                log, registry, finding_id=inclusion_successor["finding_id"], actor=USER,
                at="2026-09-29T12:16:00Z",
            )
            inclusion_withdrawn = recovered_run("inclusion-withdrawn")
            self.assertNotIn(f"{INCLUSION_OUTPUT}|{inclusion_successor['fact_id']}", inclusion_withdrawn)
            self.assertIn(f"{INCLUSION_OUTPUT}|{second['claims']['statement-inclusion']['fact_id']}", inclusion_withdrawn)
            _assert_same_result(self, inclusion_corrected, inclusion_withdrawn,
                                f"{INCLUSION_OUTPUT}|{second['claims']['statement-inclusion']['fact_id']}")

            # Target retraction leaves a current claim finding and observation; explicit guard says unresolved.
            target = next(fid for fid, finding in project(log.read().acts, registry).findings.items()
                          if finding["fact_id"] == twin_school)
            log.append(act(log.read().revision, "finding-retracted", {"finding_id": target}),
                       expected_revision=log.read().revision)
            applicability = {row["finding_id"]: row["applicability"]
                             for row in current_claim_applicability(log.read().acts, registry)}
            self.assertEqual(applicability[second["claims"]["financing"]["finding_id"]],
                             "unresolved-applicability")
            guarded = recovered_run("source-target-retracted")
            self.assertIn(f"{FINANCE_OUTPUT}|{second['claims']['financing']['fact_id']}", guarded)
            _assert_same_result(self, inclusion_withdrawn, guarded,
                                f"{FINANCE_OUTPUT}|{second['claims']['financing']['fact_id']}")

            # Nonaffirmative answers stay only in evidence and never create an observation.
            no_answer = record_submission_durably(log, {
                "submission_id":"demo.track15.answer.no","evidence_id":"demo.evidence.track15.answer.no",
                "actor":USER,"at":"2026-09-29T12:17:00Z","borrowing_ref":refs["borrowing"],
                "schooling_fact_id":refs["school"],"statement_fact_id":refs["statement"],
                "financing_response":"no","inclusion_response":"cannot-tell",
            }, registry)
            self.assertEqual(no_answer["claims"], {})
            after_no = recovered_run("nonaffirmative-answer")
            self.assertEqual(set(after_no), set(guarded))


if __name__ == "__main__":
    unittest.main()
