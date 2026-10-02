"""Track 13: explicit synthetic claims enter through ordinary contribution admission."""
from __future__ import annotations

import copy
import unittest
from typing import Any

from packages.derivation.loader import DerivationSchemas
from packages.kernel.currency import compute_currency
from packages.kernel.facts import facts_of
from packages.kernel.findings import project
from tests.test_sli_track10_saved_account_evidence import (
    FINANCE, FINANCE_RULE, MEMBERSHIP, MEMBERSHIP_RULE, SCHOOL,
)
from tests.test_sli_track12_account_reference_boundary import (
    ACCOUNT_FINDING, _assemble_reference_only_case, _correct_account,
)
from tests.test_sli_track11_collection_declarations import (
    AVAILABLE, EXPECTED, _execute_track11, _reseal_readiness_candidate, _saved_input_closure,
)
from tests.support import act
from tools.sli_explicit_relationship_recording_experiment import RecordingRefused, record_explicit_claim


class ExplicitRelationshipRecording(unittest.TestCase):
    def _unclaimed(self, *, equal_pair: bool = False) -> tuple[Any, list[dict[str, Any]], dict[str, Any]]:
        surface, acts = _assemble_reference_only_case(include_diagnostic=False, equal_pair=equal_pair)
        registry = DerivationSchemas().registry
        state = project(tuple(copy.deepcopy(row) for row in acts), registry)
        currency = compute_currency(state)
        lattice = facts_of(state.fact_state)
        current = {fid: row for fid, row in state.findings.items() if fid in currency.current_finding_ids}
        self.assertIn(ACCOUNT_FINDING, current)
        self.assertFalse(any(lattice[row["fact_id"]].fact_type_id in {FINANCE, MEMBERSHIP}
                             for row in current.values() if row["fact_id"] in lattice))
        account = current[ACCOUNT_FINDING]["value"]
        school_id = account["schooling_reference"]
        statement_id = account["statement_reference"]
        adoption = acts.pop()
        return surface, acts, {"registry": registry, "school": school_id,
                               "statement": statement_id, "borrowing": account["borrowing_reference"],
                               "adoption": adoption}

    def test_explicit_claims_are_admitted_and_reopened_through_real_consumers(self) -> None:
        surface, acts, refs = self._unclaimed()
        registry = refs["registry"]
        claim_rows = [
            {"claim_id": "demo.sli.track13.claim.finance-a", "kind": "financing", "attestation": True,
             "evidence_id": "demo.evidence.sli.track13.finance-a",
             "references": {"borrowing": refs["borrowing"], "schooling_fact_id": refs["school"]}},
            {"claim_id": "demo.sli.track13.claim.member-a-s1", "kind": "statement-membership",
             "attestation": True, "scope": "named-statement",
             "evidence_id": "demo.evidence.sli.track13.member-a-s1",
             "references": {"borrowing": refs["borrowing"],
                            "statement_fact_id": refs["statement"]}},
        ]
        recorded = [record_explicit_claim(acts, row, registry) for row in claim_rows]
        assert all(row is not None for row in recorded)
        admitted_claims = [row for row in recorded if row is not None]
        refs["adoption"]["committed_against"] = len(acts)
        acts.append(refs["adoption"])
        self.assertEqual(len({row["claim_id"] for row in admitted_claims}), 2)
        self.assertTrue(all(row["finding_id"] != row["claim_id"] for row in admitted_claims))

        order = _reseal_readiness_candidate(surface, acts, consumer_first=False)
        record, forward, reference = _execute_track11("track13-explicit", acts, surface, order)
        self.assertEqual(forward, reference)
        self.assertTrue(record["live_matches_forward"])
        self.assertTrue(record["live_dispositions_match_forward"])
        saved = record["saved"]
        support = {row["finding"]["id"]: row for row in saved["evaluated_support"]}
        self.assertTrue(all(row["finding_id"] in support for row in admitted_claims))
        self.assertEqual(support[admitted_claims[0]["finding_id"]]["fact"]["fact_type_id"], FINANCE)
        self.assertEqual(support[admitted_claims[1]["finding_id"]]["fact"]["fact_type_id"], MEMBERSHIP)
        self.assertEqual(support[admitted_claims[0]["finding_id"]]["finding"]["value"], "demo.financing.observed")
        self.assertEqual(support[admitted_claims[1]["finding_id"]]["finding"]["value"], "demo.membership.observed")
        for claim, admitted in zip(claim_rows, admitted_claims):
            evidence = support[admitted["finding_id"]]["evidence"][0]
            self.assertEqual(evidence["id"], claim["evidence_id"])
            self.assertEqual(evidence["content"]["claim_id"], claim["claim_id"])
            self.assertEqual(evidence["content"]["references"], claim["references"])
            if claim["kind"] == "statement-membership":
                self.assertEqual(evidence["content"]["scope"], "named-statement")
        neutral = [row["finding"] for row in saved["publications"]
                   if {"role": "computation", "id": MEMBERSHIP_RULE, "version": "v1"}
                   in row["finding"].get("pins", [])]
        self.assertTrue(neutral)
        assert all(any(pin.get("id") == admitted_claims[1]["finding_id"] and pin.get("role") == "input"
                       for pin in row.get("pins", [])) for row in neutral)
        finance_rows = [row["finding"] for row in saved["publications"]
                        if {"role": "computation", "id": FINANCE_RULE, "version": "v1"}
                        in row["finding"].get("pins", [])]
        self.assertEqual(len(finance_rows), 1)
        finance_leaves = _saved_input_closure(saved, finance_rows[0].get("pins", []))
        school_finding = next(fid for fid, row in support.items()
                              if row["fact"]["fact_type_id"] == SCHOOL and
                              row["fact"]["fact_id"] == refs["school"])
        self.assertEqual(finance_leaves, {admitted_claims[0]["finding_id"], school_finding})
        membership_leaves = _saved_input_closure(saved, neutral[0].get("pins", []))
        self.assertEqual(membership_leaves, {admitted_claims[0]["finding_id"], admitted_claims[1]["finding_id"],
                                             school_finding})
        self.assertFalse(saved["complete"])  # Existing carrier records unrelated whole-run horizon pins.
        self.assertTrue(saved["scope"]["selected_publication_ids"])
        self.assertFalse(any(row["finding"]["id"] == ACCOUNT_FINDING
                             for row in saved["publications"]))

    def test_nonaffirmative_and_wrong_scope_refuse_without_source_assertion(self) -> None:
        _surface, acts, refs = self._unclaimed()
        registry = refs["registry"]
        claim = {"claim_id": "demo.sli.track13.claim.unconfirmed", "kind": "financing",
                 "attestation": None, "evidence_id": "demo.evidence.sli.track13.unconfirmed",
                 "references": {"borrowing": refs["borrowing"], "schooling_fact_id": refs["school"]}}
        self.assertIsNone(record_explicit_claim(acts, claim, registry))
        bad = dict(claim, claim_id="demo.sli.track13.claim.bad-scope", kind="statement-membership",
                   attestation=True, evidence_id="demo.evidence.sli.track13.bad-scope")
        with self.assertRaisesRegex(RecordingRefused, "named-statement"):
            record_explicit_claim(acts, bad, registry)
        state = project(tuple(copy.deepcopy(row) for row in acts), registry)
        self.assertFalse(any(row["fact_id"].startswith(f"{FINANCE}|") or
                             row["fact_id"].startswith(f"{MEMBERSHIP}|")
                             for row in state.findings.values()))
        stale = dict(claim, claim_id="demo.sli.track13.claim.stale-school",
                     evidence_id="demo.evidence.sli.track13.stale-school", attestation=True,
                     references={"borrowing": refs["borrowing"],
                                 "schooling_fact_id": "demo.sli.track10.schooling|situation=demo.stale"})
        with self.assertRaisesRegex(RecordingRefused, "schooling referent"):
            record_explicit_claim(acts, stale, registry)

    def test_membership_needs_no_schooling_and_wrong_kind_borrowing_is_atomic_refusal(self) -> None:
        _surface, acts, refs = self._unclaimed()
        registry = refs["registry"]
        membership = {"claim_id": "demo.sli.track13.claim.member-only", "kind": "statement-membership",
                      "attestation": True, "scope": "named-statement",
                      "evidence_id": "demo.evidence.sli.track13.member-only",
                      "references": {"borrowing": refs["borrowing"],
                                     "statement_fact_id": refs["statement"]}}
        recorded = record_explicit_claim(acts, membership, registry)
        assert recorded is not None
        state = project(tuple(copy.deepcopy(row) for row in acts), registry)
        self.assertEqual(state.findings[recorded["finding_id"]]["fact_id"].split("|", 1)[0], MEMBERSHIP)
        before = copy.deepcopy(acts)
        invalid = dict(membership, claim_id="demo.sli.track13.claim.wrong-borrowing",
                       evidence_id="demo.evidence.sli.track13.wrong-borrowing",
                       references={"borrowing": "demo.sli.track12.account.references-present",
                                   "statement_fact_id": refs["statement"]})
        with self.assertRaisesRegex(RecordingRefused, "borrowing referent"):
            record_explicit_claim(acts, invalid, registry)
        self.assertEqual(acts, before)
        duplicate = dict(membership, claim_id="demo.sli.track13.claim.duplicate-membership",
                         evidence_id="demo.evidence.sli.track13.duplicate-membership")
        with self.assertRaisesRegex(RecordingRefused, "duplicate active relationship"):
            record_explicit_claim(acts, duplicate, registry)
        self.assertEqual(acts, before)

    def test_active_claim_and_evidence_addresses_cannot_be_reused(self) -> None:
        _surface, acts, refs = self._unclaimed(equal_pair=True)
        registry = refs["registry"]
        state = project(tuple(copy.deepcopy(row) for row in acts), registry)
        currency = compute_currency(state)
        lattice = facts_of(state.fact_state)
        alternate = next(
            fact for fact in lattice.values()
            if fact.fact_type_id == SCHOOL and fact.fact_id != refs["school"] and
            any(fid in currency.current_finding_ids and row["fact_id"] == fact.fact_id
                for fid, row in state.findings.items())
        )
        claim = {"claim_id": "demo.sli.track13.claim.stable-address", "kind": "financing",
                 "attestation": True, "evidence_id": "demo.evidence.sli.track13.stable-address",
                 "references": {"borrowing": refs["borrowing"],
                                "schooling_fact_id": refs["school"]}}
        first = record_explicit_claim(acts, claim, registry)
        assert first is not None
        before = copy.deepcopy(acts)
        retargeted = dict(claim, evidence_id="demo.evidence.sli.track13.stable-address-retargeted",
                          references={"borrowing": refs["borrowing"],
                                      "schooling_fact_id": alternate.fact_id})
        with self.assertRaisesRegex(RecordingRefused, "claim ID is already active"):
            record_explicit_claim(acts, retargeted, registry)
        same_evidence_new_claim = dict(claim, claim_id="demo.sli.track13.claim.new-address")
        with self.assertRaisesRegex(RecordingRefused, "evidence identity is already active"):
            record_explicit_claim(acts, same_evidence_new_claim, registry)
        self.assertEqual(acts, before)

    def test_two_statement_claim_lifecycles_keep_exact_consumer_support(self) -> None:
        from tests.test_sli_track10_saved_account_evidence import _append_contributed_claim

        surface, acts, refs = self._unclaimed(equal_pair=True)
        registry = refs["registry"]
        initial = project(tuple(copy.deepcopy(row) for row in acts), registry)
        initial_currency = compute_currency(initial)
        initial_lattice = facts_of(initial.fact_state)
        current_ids = initial_currency.current_finding_ids
        alternate_school = next(
            fact for fact in initial_lattice.values()
            if fact.fact_type_id == SCHOOL and fact.fact_id != refs["school"] and
            any(fid in current_ids and row["fact_id"] == fact.fact_id
                for fid, row in initial.findings.items())
        )
        shared_school_finding = next(row for finding_id, row in initial.findings.items()
                                     if finding_id in current_ids and row["fact_id"] == refs["school"])
        alternate_school_finding = next(row for finding_id, row in initial.findings.items()
                                        if finding_id in current_ids and
                                        row["fact_id"] == alternate_school.fact_id)
        self.assertEqual(alternate_school_finding["value"], shared_school_finding["value"])
        statement_two = next(
            fact for fact in initial_lattice.values()
            if fact.fact_type_id == "tax.us.2025.f1098e.box1-student-loan-interest" and
            dict(fact.keys).get("statement") == "demo.statement.reader.s2" and
            any(fid in current_ids and row["fact_id"] == fact.fact_id
                for fid, row in initial.findings.items())
        )
        claim_specs = [
            ("finance-a", "financing", "demo.track8.borrowing.a", refs["school"], None),
            ("finance-b", "financing", "demo.track8.borrowing.b", refs["school"], None),
            ("member-a-s1", "statement-membership", "demo.track8.borrowing.a", refs["school"],
             refs["statement"]),
            ("member-b-s2", "statement-membership", "demo.track8.borrowing.b", refs["school"],
             statement_two.fact_id),
        ]

        def record_specs(targets: list[tuple[str, str, str, str, str | None]]) -> dict[str, dict[str, str]]:
            result: dict[str, dict[str, str]] = {}
            for slug, kind, borrowing, schooling, statement in targets:
                claim_id = f"demo.sli.track13.claim.{slug}"
                claim: dict[str, Any] = {
                    "claim_id": claim_id, "kind": kind, "attestation": True,
                    "evidence_id": f"demo.evidence.sli.track13.{slug}",
                    "references": {"borrowing": borrowing},
                }
                if kind == "financing":
                    claim["references"]["schooling_fact_id"] = schooling
                if kind == "statement-membership":
                    claim["scope"] = "named-statement"
                    claim["references"]["statement_fact_id"] = statement
                admitted = record_explicit_claim(acts, claim, registry)
                assert admitted is not None
                result[slug] = admitted
            return result

        recorded = record_specs(claim_specs)
        adoption = refs["adoption"]
        adoption["committed_against"] = len(acts)
        acts.append(adoption)
        order = _reseal_readiness_candidate(surface, acts, consumer_first=False)

        def run(name: str, run_acts: list[dict[str, Any]]) -> dict[str, Any]:
            result, forward, reference = _execute_track11(name, run_acts, surface, order)
            self.assertEqual(forward, reference)
            self.assertTrue(result["live_matches_forward"])
            self.assertTrue(result["live_dispositions_match_forward"])
            return result

        baseline = run("track13-two-statements-baseline", acts)

        def neutral_by_statement(result: dict[str, Any]) -> dict[str, dict[str, Any]]:
            memberships = [row["finding"] for row in result["saved"]["publications"]
                           if {"role": "computation", "id": MEMBERSHIP_RULE, "version": "v1"}
                           in row["finding"].get("pins", [])]
            output: dict[str, dict[str, Any]] = {}
            for key, slug in (("a", "member-a-s1"), ("b", "member-b-s2")):
                row = next((row for row in memberships if any(
                    pin.get("id") == recorded[slug]["finding_id"] for pin in row.get("pins", []))), None)
                if row is not None:
                    output[key] = row
            return output

        def snapshot(row: dict[str, Any]) -> tuple[Any, Any, Any]:
            return row.get("symbol"), row.get("value"), row.get("pins")

        baseline_neutral = neutral_by_statement(baseline)
        saved_baseline = baseline["saved"]
        support_baseline = {row["finding"]["id"]: row for row in saved_baseline["evaluated_support"]}
        self.assertEqual(_saved_input_closure(saved_baseline, baseline_neutral["a"].get("pins", [])),
                         {recorded["member-a-s1"]["finding_id"], recorded["finance-a"]["finding_id"],
                          next(fid for fid, row in support_baseline.items()
                               if row["fact"]["fact_type_id"] == SCHOOL and
                               row["fact"]["fact_id"] == refs["school"])})
        self.assertEqual(_saved_input_closure(saved_baseline, baseline_neutral["b"].get("pins", [])),
                         {recorded["member-b-s2"]["finding_id"], recorded["finance-b"]["finding_id"],
                          next(fid for fid, row in support_baseline.items()
                               if row["fact"]["fact_type_id"] == SCHOOL and
                               row["fact"]["fact_id"] == refs["school"])})
        self.assertFalse(any(row["finding"]["id"] == ACCOUNT_FINDING
                             for row in saved_baseline["publications"]))

        corrected = copy.deepcopy(acts)
        corrected_adoption = corrected.pop()
        corrected.append(act(len(corrected), "finding-retracted",
                             {"finding_id": recorded["finance-a"]["finding_id"]}))
        successor = record_explicit_claim(corrected, {
            "claim_id": "demo.sli.track13.claim.finance-a", "kind": "financing", "attestation": True,
            "evidence_id": "demo.evidence.sli.track13.finance-a-corrected",
            "references": {"borrowing": "demo.track8.borrowing.a",
                           "schooling_fact_id": alternate_school.fact_id},
        }, registry)
        assert successor is not None
        corrected_adoption["committed_against"] = len(corrected)
        corrected.append(corrected_adoption)
        after_correction = run("track13-two-statements-claim-corrected", corrected)
        corrected_neutral = neutral_by_statement(after_correction)
        self.assertEqual(snapshot(corrected_neutral["b"]), snapshot(baseline_neutral["b"]))
        self.assertNotEqual(snapshot(corrected_neutral["a"]), snapshot(baseline_neutral["a"]))
        lineage = {row["finding"]["id"]: row["status"] for row in after_correction["saved"]["lineage"]}
        self.assertEqual(lineage[recorded["finance-a"]["finding_id"]], "displaced")
        corrected_support = {row["finding"]["id"]: row for row in
                             after_correction["saved"]["evaluated_support"]}
        corrected_school_finding = next(fid for fid, row in corrected_support.items()
                                        if row["fact"]["fact_type_id"] == SCHOOL and
                                        row["fact"]["fact_id"] == alternate_school.fact_id)
        shared_school_findings = {fid for fid, row in corrected_support.items()
                                  if row["fact"]["fact_type_id"] == SCHOOL and
                                  row["fact"]["fact_id"] == refs["school"]}
        corrected_leaves = _saved_input_closure(after_correction["saved"],
                                                corrected_neutral["a"].get("pins", []))
        self.assertEqual(corrected_leaves, {recorded["member-a-s1"]["finding_id"],
                                            successor["finding_id"], corrected_school_finding})
        self.assertNotIn(recorded["finance-a"]["finding_id"], corrected_leaves)
        self.assertFalse(corrected_leaves & shared_school_findings)
        self.assertEqual(corrected_support[corrected_school_finding]["finding"]["value"],
                         shared_school_finding["value"])

        withdrawn = copy.deepcopy(corrected)
        withdrawn_adoption = withdrawn.pop()
        withdrawn.append(act(len(withdrawn), "finding-retracted",
                             {"finding_id": successor["finding_id"]}))
        withdrawn_adoption["committed_against"] = len(withdrawn)
        withdrawn.append(withdrawn_adoption)
        after_withdrawal = run("track13-two-statements-claim-withdrawn", withdrawn)
        withdrawn_neutral = neutral_by_statement(after_withdrawal)
        self.assertEqual(snapshot(withdrawn_neutral["b"]), snapshot(baseline_neutral["b"]))
        self.assertNotIn("a", withdrawn_neutral)
        withdrawn_dispositions = after_withdrawal["saved"]["dispositions"]
        baseline_s2_disposition = next(row for row in saved_baseline["dispositions"]
                                        if row.get("artifact_id") == MEMBERSHIP_RULE and
                                        row.get("symbol") == baseline_neutral["b"]["symbol"])
        s1_block = next(row for row in withdrawn_dispositions
                        if row.get("artifact_id") == MEMBERSHIP_RULE and
                        row.get("symbol") == baseline_neutral["a"]["symbol"])
        s2_publication_disposition = next(row for row in withdrawn_dispositions
                                          if row.get("artifact_id") == MEMBERSHIP_RULE and
                                          row.get("symbol") == baseline_neutral["b"]["symbol"])
        self.assertEqual((s1_block["disposition"], s1_block["code"], s1_block["missing"]),
                         ("blocked", "DEPENDENCY_ABSENT", [EXPECTED, AVAILABLE]))
        self.assertEqual(s2_publication_disposition["disposition"], "published")
        self.assertEqual(s2_publication_disposition["pins"], baseline_s2_disposition["pins"])
        self.assertFalse(any(row["finding"]["symbol"] == baseline_neutral["a"]["symbol"]
                             for row in after_withdrawal["saved"]["publications"]))

        account_corrected = _correct_account(acts)
        after_account_correction = run("track13-account-corrected", account_corrected)
        corrected_account_neutral = neutral_by_statement(after_account_correction)
        self.assertEqual({key: snapshot(corrected_account_neutral[key]) for key in ("a", "b")},
                         {key: snapshot(baseline_neutral[key]) for key in ("a", "b")})
        account_retracted = copy.deepcopy(account_corrected)
        account_adoption = account_retracted.pop()
        account_retracted.append(act(len(account_retracted), "finding-retracted",
                                     {"finding_id": "demo.finding.sli.track12.account.corrected"}))
        account_adoption["committed_against"] = len(account_retracted)
        account_retracted.append(account_adoption)
        after_account_retraction = run("track13-account-retracted", account_retracted)
        retracted_account_neutral = neutral_by_statement(after_account_retraction)
        self.assertEqual({key: snapshot(retracted_account_neutral[key]) for key in ("a", "b")},
                         {key: snapshot(baseline_neutral[key]) for key in ("a", "b")})

        source_correction = copy.deepcopy(acts)
        source_adoption = source_correction.pop()
        school_source = next(row for row in initial.findings.values()
                             if row["fact_id"] == refs["school"])
        corrected_school = dict(school_source)
        corrected_school.update({"id": "demo.finding.sli.track13.school.shared.corrected",
                                 "value": "demo.schooling.corrected-observation",
                                 "evidence_ids": ["demo.evidence.sli.track13.school.shared.corrected"],
                                 "contribution_id": "demo.contribution.sli.track13.school.shared.corrected"})
        _append_contributed_claim(source_correction, registry, corrected_school,
                                  corrected_school["evidence_ids"][0], corrected_school["contribution_id"])
        source_adoption["committed_against"] = len(source_correction)
        source_correction.append(source_adoption)
        after_school_correction = run("track13-source-school-corrected", source_correction)
        corrected_lineage = {row["finding"]["id"]: row["status"]
                             for row in after_school_correction["saved"]["lineage"]}
        self.assertEqual(corrected_lineage[school_source["id"]], "displaced")
        corrected_neutral_rows = neutral_by_statement(after_school_correction)
        self.assertEqual(set(corrected_neutral_rows), {"a", "b"})
        relationship_ids = {recorded[key]["finding_id"] for key in
                            ("finance-a", "finance-b", "member-a-s1", "member-b-s2")}
        corrected_support = {row["finding"]["id"]: row for row in
                             after_school_correction["saved"]["evaluated_support"]}
        corrected_support_ids = set(corrected_support)
        self.assertTrue(relationship_ids <= corrected_support_ids)
        corrected_school_id = "demo.finding.sli.track13.school.shared.corrected"
        for key, member_slug, finance_slug in (("a", "member-a-s1", "finance-a"),
                                               ("b", "member-b-s2", "finance-b")):
            leaves = _saved_input_closure(after_school_correction["saved"],
                                          corrected_neutral_rows[key].get("pins", []))
            self.assertEqual(leaves, {recorded[member_slug]["finding_id"],
                                      recorded[finance_slug]["finding_id"], corrected_school_id})
            self.assertNotIn(school_source["id"], leaves)

        source_retracted = copy.deepcopy(source_correction)
        retraction_adoption = source_retracted.pop()
        source_retracted.append(act(len(source_retracted), "finding-retracted",
                                    {"finding_id": corrected_school["id"]}))
        retraction_adoption["committed_against"] = len(source_retracted)
        source_retracted.append(retraction_adoption)
        after_school_retraction = run("track13-source-school-retracted", source_retracted)
        retracted_support_ids = {row["finding"]["id"] for row in
                                 after_school_retraction["saved"]["evaluated_support"]}
        self.assertTrue(relationship_ids <= retracted_support_ids)
        self.assertNotIn(corrected_school["id"], retracted_support_ids)
        finance_refusals = [row for row in after_school_retraction["saved"]["dispositions"]
                            if row.get("artifact_id") == FINANCE_RULE and
                            row.get("disposition") == "blocked"]
        self.assertEqual(len(finance_refusals), 2)
        baseline_finance_symbols = {
            row["finding"]["symbol"] for row in baseline["saved"]["publications"]
            if {"role": "computation", "id": FINANCE_RULE, "version": "v1"}
            in row["finding"].get("pins", [])
        }
        self.assertEqual({row["symbol"] for row in finance_refusals}, baseline_finance_symbols)
        self.assertTrue(all(row.get("code") == "DEPENDENCY_ABSENT" and row.get("missing") == [SCHOOL]
                            for row in finance_refusals))
        membership_refusals = [row for row in after_school_retraction["saved"]["dispositions"]
                               if row.get("artifact_id") == MEMBERSHIP_RULE and
                               row.get("disposition") == "blocked"]
        self.assertEqual(len(membership_refusals), 2)
        self.assertEqual({row["symbol"] for row in membership_refusals},
                         {baseline_neutral[key]["symbol"] for key in ("a", "b")})
        self.assertTrue(all(row.get("code") == "DEPENDENCY_ABSENT" and row.get("missing") == [AVAILABLE]
                            for row in membership_refusals))
        affected_symbols = {row["symbol"] for row in membership_refusals}
        blocked_finance_symbols = {row["symbol"] for row in finance_refusals}
        self.assertFalse(any(row["finding"]["symbol"] in affected_symbols | blocked_finance_symbols
                             for row in after_school_retraction["saved"]["publications"]))


if __name__ == "__main__":
    unittest.main()
