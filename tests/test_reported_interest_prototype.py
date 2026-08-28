"""Iteration 6 executed comparison.

Prototype evidence. Uses the production expression evaluator. Access modes are
explicit capability grants. Distributed shapes evaluate separate rules.
Source-report support is the exact statement reads; tax authority and coverage
are omitted there. Task 5 recovers the recorded partition explanation.
"""

from __future__ import annotations

import unittest
from dataclasses import replace
from decimal import Decimal

from prototype.reported_interest.model import (
    CASES,
    OBLIGATION_ID,
    OBLIGATION_ID_B,
    OBLIGATION_ID_THIRD,
    Workspace,
    case_ti_b2,
)
from prototype.reported_interest.rubric import (
    ACCESS_MODES,
    RUBRIC,
    TASK5,
    TASK6,
    LaterYearConsumer,
    ShapeRun,
    grant,
    independent_lifecycle,
    later_year_probe,
    mutate_payload,
    run_shape,
)
from prototype.reported_interest.shapes import (
    AUTHORITY,
    BLOCK_ITEM_MISMATCH,
    BLOCK_UNSUPPORTED,
    COVERAGE_ID,
    COVERAGE_VERSION,
    Blocked,
    Displaced,
    ObjectStore,
    Provenance,
    basis_artifact,
    evaluate_basis,
    evaluate_includible,
    evaluate_reported,
    project_line_2b,
)

SHAPES = ("A", "C", "E", "B")


def _assert_source_report_provenance(test: unittest.TestCase, art, ws, amount) -> None:
    """Complete source-report provenance: exact reads, empty tax authority, no coverage."""
    names = ws.names
    expected_reads = {
        names.reported_amount,
        names.reported_payer,
        names.reported_obligation,
    }
    test.assertEqual(art.kind, "source-report")
    test.assertEqual(art.payload["amount"], Decimal(amount))
    test.assertEqual(set(art.provenance.reads), expected_reads)
    test.assertEqual(dict(art.provenance.versions), {n: ws.facts[n].version for n in expected_reads})
    test.assertEqual(art.provenance.authority, ())
    test.assertEqual(tuple(art.provenance.authority), ())
    test.assertIsNone(art.provenance.coverage_id)
    test.assertIsNone(art.provenance.coverage_version)
    accounted = art.provenance.accounted()
    test.assertEqual(expected_reads, expected_reads & accounted)
    test.assertTrue(expected_reads <= accounted)
    authority_tokens = {t for t in accounted if t.startswith("authority:")}
    coverage_tokens = {t for t in accounted if t.startswith("coverage:")}
    test.assertEqual(authority_tokens, {"authority:omitted"})
    test.assertEqual(coverage_tokens, {"coverage:omitted"})
    test.assertNotIn(f"coverage:{COVERAGE_ID}.v{COVERAGE_VERSION}", accounted)
    test.assertNotIn(COVERAGE_ID, accounted)
    test.assertFalse(any("IRC" in t or "Pub. 550" in t for t in accounted))


def _assert_treatment_tax_authority(test: unittest.TestCase, art) -> None:
    expected = {a["citation"] for a in AUTHORITY}
    cites = {c["citation"] for c in art.provenance.authority}
    test.assertEqual(cites, expected)
    test.assertEqual(art.provenance.coverage_id, COVERAGE_ID)
    test.assertEqual(art.provenance.coverage_version, COVERAGE_VERSION)
    accounted = art.provenance.accounted()
    test.assertNotIn("authority:omitted", accounted)
    test.assertNotIn("coverage:omitted", accounted)
    test.assertIn(f"coverage:{COVERAGE_ID}.v{COVERAGE_VERSION}", accounted)
    test.assertTrue({f"authority:{c}" for c in expected} <= accounted)


def refusal(run: ShapeRun):
    assert run.blocked is not None, f"expected a refusal, got artifacts {list(run.keys)}"
    return run.blocked


def line_2b(shape: str, ws: Workspace) -> Decimal | None:
    run = run_shape(shape, ws)
    if run.is_blocked:
        return None
    assert run.item is not None
    return project_line_2b(run.store, run.item, run.workspace)


class RequiredCaseOutcomes(unittest.TestCase):
    def test_ti_b1_reports_the_whole_amount(self) -> None:
        ws = CASES["TI-B1"]()
        for shape in SHAPES:
            with self.subTest(shape=shape):
                self.assertEqual(line_2b(shape, ws), Decimal(1200))

    def test_ti_b2_derives_900_and_300_basis(self) -> None:
        ws = CASES["TI-B2"]()
        for shape in SHAPES:
            with self.subTest(shape=shape):
                self.assertEqual(line_2b(shape, ws), Decimal(900))
                run = run_shape(shape, ws)
                art = basis_artifact(run.store, OBLIGATION_ID)
                assert art is not None
                amount = art.payload.get("basis-reduction", art.payload.get("amount"))
                self.assertEqual(amount, Decimal(300))

    def test_ti_n1_blocks_and_names_the_outstanding_question(self) -> None:
        ws = CASES["TI-N1"]()
        for shape in SHAPES:
            with self.subTest(shape=shape):
                run = run_shape(shape, ws)
                self.assertTrue(run.is_blocked)
                assert run.blocked is not None
                self.assertEqual(run.blocked.code, "DEPENDENCY_ABSENT")
                self.assertIn("accrued-interest-paid-to-seller", run.blocked.missing[0])
                kinds = {a.kind for a in run.store.artifacts.values()}
                self.assertEqual(kinds, {"source-report"})
                src = next(iter(run.store.artifacts.values()))
                self.assertEqual(src.payload["amount"], Decimal(1200))

    def test_ti_l1_source_correction_gives_700(self) -> None:
        for shape in SHAPES:
            with self.subTest(shape=shape):
                self.assertEqual(line_2b(shape, CASES["TI-L1"]()), Decimal(700))

    def test_ti_l2_circumstance_correction_gives_950(self) -> None:
        for shape in SHAPES:
            with self.subTest(shape=shape):
                self.assertEqual(line_2b(shape, CASES["TI-L2"]()), Decimal(950))

    def test_ti_a1_is_the_box_3_fixture_without_section_135_facts(self) -> None:
        ws = CASES["TI-A1"]()
        self.assertEqual(ws.names.reported_box, "box 3")
        self.assertEqual(ws.facts[ws.names.reported_amount].value, 840)
        self.assertEqual(ws.facts[ws.names.reported_obligation].value, OBLIGATION_ID_B)
        self.assertEqual(ws.facts[ws.names.obligation_kind].value, "series-ee-savings-bond")
        self.assertEqual(ws.facts[ws.names.education_expenses].value, "yes")
        self.assertNotIn(CASES["TI-B1"]().names.reported_amount, ws.facts)
        joined = " ".join(f.question for f in ws.facts.values()).lower()
        for extra in ("issued after", "modified agi", "redemption proceeds", "filing status"):
            self.assertNotIn(extra, joined)

    def test_ti_a1_source_report_survives_treatment_refusal(self) -> None:
        ws = CASES["TI-A1"]()
        outcome = evaluate_reported(ws)
        self.assertNotIsInstance(outcome, Blocked)
        self.assertEqual(outcome.values["reported"], Decimal(840))
        before = ws.facts[ws.names.reported_amount]
        for shape in SHAPES:
            with self.subTest(shape=shape):
                run = run_shape(shape, ws)
                self.assertTrue(run.is_blocked)
                self.assertEqual(run.blocked.code, BLOCK_UNSUPPORTED)
                src = [a for a in run.store.artifacts.values() if a.kind == "source-report"]
                self.assertEqual(len(src), 1)
                self.assertEqual(src[0].payload["amount"], Decimal(840))
                self.assertEqual(ws.facts[ws.names.reported_amount], before)

    def test_ti_a1_refuses_coverage(self) -> None:
        for shape in SHAPES:
            with self.subTest(shape=shape):
                run = run_shape(shape, CASES["TI-A1"]())
                self.assertTrue(run.is_blocked)
                assert run.blocked is not None
                self.assertEqual(run.blocked.code, BLOCK_UNSUPPORTED)
                kinds = {a.kind for a in run.store.artifacts.values()}
                self.assertEqual(kinds, {"source-report"})
                src = next(iter(run.store.artifacts.values()))
                self.assertEqual(src.payload["amount"], Decimal(840))
                fact = run.workspace.facts[run.workspace.names.reported_amount]
                self.assertEqual(fact.value, 840)
                self.assertEqual(fact.version, 1)


class SeparateRules(unittest.TestCase):
    def test_includible_and_basis_are_distinct_evaluations(self) -> None:
        ws = case_ti_b2()
        inc = evaluate_includible(ws)
        basis = evaluate_basis(ws)
        self.assertNotIsInstance(inc, Blocked)
        self.assertNotIsInstance(basis, Blocked)
        self.assertEqual(inc.provenance.rule_id, "demo.rule.includible-interest")
        self.assertEqual(basis.provenance.rule_id, "demo.rule.basis-reduction")
        self.assertIn(ws.names.reported_amount, inc.provenance.reads)
        self.assertNotIn(ws.names.reported_amount, basis.provenance.reads)
        self.assertIn(ws.names.reported_payer, inc.provenance.reads)
        self.assertNotIn(ws.names.reported_payer, basis.provenance.reads)
        self.assertIn(ws.names.accrued_paid_to_seller, basis.provenance.reads)

    def test_published_rule_ids_match_the_expression_that_ran(self) -> None:
        for shape in ("A", "C", "E"):
            run = run_shape(shape, case_ti_b2())
            kinds = {a.kind: a.provenance.rule_id for a in run.artifacts()}
            with self.subTest(shape=shape):
                self.assertEqual(kinds["includible-interest"], "demo.rule.includible-interest")
                self.assertEqual(kinds["basis-reduction"], "demo.rule.basis-reduction")
                self.assertEqual(kinds["source-report"], "demo.rule.source-report")

    def test_b_is_one_composite_evaluation(self) -> None:
        run = run_shape("B", case_ti_b2())
        tax = [a for a in run.artifacts() if a.kind == "determination"]
        self.assertEqual(len(tax), 1)
        self.assertEqual(tax[0].provenance.rule_id, "demo.rule.accrued-interest-at-purchase")


class EvidenceRubric(unittest.TestCase):
    def test_every_check_on_every_case(self) -> None:
        observed: set[tuple[str, str, str]] = set()
        for case, make in CASES.items():
            ws = make()
            for shape in SHAPES:
                run = run_shape(shape, ws)
                for label, check in RUBRIC.items():
                    with self.subTest(case=case, shape=shape, check=label):
                        passed, detail = check(run)
                        if not passed:
                            observed.add((case, shape, label))
        self.assertEqual(observed, set())

    def test_statement_report_is_never_written_back(self) -> None:
        ws = case_ti_b2()
        before = ws.facts[ws.names.reported_amount]
        for shape in SHAPES:
            run_shape(shape, ws)
        self.assertEqual(ws.facts[ws.names.reported_amount], before)


class Adversarial(unittest.TestCase):
    """Post-publication correction of every declared fact, plus relationship fields."""

    FACTS = (
        "reported_amount",
        "reported_payer",
        "reported_obligation",
        "bought_between_dates",
        "accrued_paid_to_seller",
        "accrued_relates_to",
        "obligation_kind",
        "education_expenses",
    )

    VALUES = {
        "reported_amount": 1000,
        "reported_payer": "demo.payer.bank-2",
        "reported_obligation": OBLIGATION_ID_THIRD,
        "bought_between_dates": "no",
        "accrued_paid_to_seller": 250,
        "accrued_relates_to": OBLIGATION_ID_THIRD,
        "obligation_kind": "series-ee-savings-bond",
        "education_expenses": "yes",
    }

    def test_each_declared_fact_displaces_exactly_the_artifacts_that_read_it(self) -> None:
        for shape in SHAPES:
            ws, run = case_ti_b2(), None
            run = run_shape(shape, ws)
            self.assertFalse(run.is_blocked)
            for attr in self.FACTS:
                name = getattr(ws.names, attr)
                corrected = ws.with_correction(name, self.VALUES[attr])
                with self.subTest(shape=shape, fact=attr):
                    for art in run.artifacts():
                        in_prov = name in art.provenance.reads
                        displaced = art.provenance.displaced_by(corrected)
                        self.assertEqual(
                            displaced,
                            in_prov,
                            f"{art.kind}: in_provenance={in_prov} displaced={displaced}",
                        )
                        if displaced:
                            with self.assertRaises(Displaced):
                                run.store.serve(art.key, corrected)
                        else:
                            served = run.store.serve(art.key, corrected)
                            self.assertEqual(served.item, art.item)

    def test_recompute_after_each_correction(self) -> None:
        ws = case_ti_b2()
        for shape in SHAPES:
            for attr, expect_block in (
                ("obligation_kind", BLOCK_UNSUPPORTED),
                ("education_expenses", BLOCK_UNSUPPORTED),
                ("accrued_relates_to", BLOCK_ITEM_MISMATCH),
                ("reported_obligation", BLOCK_ITEM_MISMATCH),
            ):
                with self.subTest(shape=shape, fact=attr):
                    name = getattr(ws.names, attr)
                    corrected = ws.with_correction(name, self.VALUES[attr])
                    again = run_shape(shape, corrected)
                    self.assertTrue(again.is_blocked)
                    self.assertEqual(refusal(again).code, expect_block)
            with self.subTest(shape=shape, fact="accrued_paid_to_seller"):
                corrected = ws.with_correction(ws.names.accrued_paid_to_seller, 250)
                again = run_shape(shape, corrected)
                self.assertFalse(again.is_blocked)
                assert again.item is not None
                self.assertEqual(project_line_2b(again.store, again.item, corrected), Decimal(950))
            with self.subTest(shape=shape, fact="reported_amount"):
                corrected = ws.with_correction(ws.names.reported_amount, 1000)
                again = run_shape(shape, corrected)
                self.assertFalse(again.is_blocked)
                assert again.item is not None
                self.assertEqual(project_line_2b(again.store, again.item, corrected), Decimal(700))
            with self.subTest(shape=shape, fact="reported_payer"):
                run = run_shape(shape, ws)
                corrected = ws.with_correction(ws.names.reported_payer, "demo.payer.bank-2")
                again = run_shape(shape, corrected)
                self.assertFalse(again.is_blocked)
                assert again.item is not None
                self.assertEqual(again.item, OBLIGATION_ID)
                self.assertEqual({a.item for a in run.artifacts()}, {OBLIGATION_ID})
            with self.subTest(shape=shape, fact="bought_between_dates"):
                corrected = ws.with_correction(ws.names.bought_between_dates, "no")
                again = run_shape(shape, corrected)
                self.assertFalse(again.is_blocked)
                assert again.item is not None
                self.assertEqual(project_line_2b(again.store, again.item, corrected), Decimal(1200))
            with self.subTest(shape=shape, fact="relation_removed"):
                run = run_shape(shape, ws)
                corrected = ws.without(ws.names.accrued_relates_to)
                for art in run.artifacts():
                    if ws.names.accrued_relates_to in art.provenance.reads:
                        with self.assertRaises(Displaced):
                            run.store.serve(art.key, corrected)
                again = run_shape(shape, corrected)
                self.assertTrue(again.is_blocked)
                self.assertEqual(refusal(again).code, "DEPENDENCY_ABSENT")
                self.assertIn(ws.names.accrued_relates_to, refusal(again).missing)


class AccessModels(unittest.TestCase):
    def test_artifact_object_only_cannot_detect_amendment(self) -> None:
        probe = later_year_probe()
        for shape in SHAPES:
            with self.subTest(shape=shape):
                ok, detail = probe[f"{shape}/artifact-object-only: after amendment, task 4"]
                self.assertFalse(ok)
                self.assertIn("no currentness service", detail)
                ok6, detail6 = probe[f"{shape}/artifact-object-only: after amendment, task 6"]
                self.assertFalse(ok6)
                self.assertIn("no currentness service", detail6)

    def test_currentness_detects_amendment_without_a_workspace(self) -> None:
        probe = later_year_probe()
        for shape in SHAPES:
            with self.subTest(shape=shape):
                ok, detail = probe[f"{shape}/currentness: after amendment, task 4"]
                self.assertTrue(ok)
                self.assertIn("carried_displaced=True", detail)
                _, usable = probe[f"{shape}/currentness: after amendment, task 6"]
                self.assertIn("fact_version_current=False", usable)

    def test_partition_recovery_by_access(self) -> None:
        """Task 5 under each access mode. The interesting rows are asserted exactly."""
        probe = later_year_probe()
        self.assertEqual(probe["A/artifact-object-only: passed"], "3/6")
        self.assertEqual(probe["C/artifact-object-only: passed"], "4/6")
        self.assertEqual(probe["E/artifact-object-only: passed"], "3/6")
        self.assertEqual(probe["B/artifact-object-only: passed"], "4/6")
        self.assertEqual(probe["A/object-store-access: passed"], "3/6")
        self.assertEqual(probe["C/object-store-access: passed"], "4/6")
        self.assertEqual(probe["E/object-store-access: passed"], "4/6")
        self.assertEqual(probe["B/object-store-access: passed"], "4/6")
        self.assertEqual(probe["A/full-workspace: passed"], "6/6")
        self.assertEqual(probe["C/full-workspace: passed"], "6/6")
        self.assertEqual(probe["E/full-workspace: passed"], "6/6")
        self.assertEqual(probe["B/full-workspace: passed"], "6/6")
        failed = [
            task
            for task, (ok, _) in probe["A/artifact-object-only: source year unamended"].items()
            if not ok
        ]
        self.assertEqual(
            failed,
            [
                "4 detect a corrected or displaced source-year fact",
                TASK5,
                "6 decide fact-version currentness of used dependencies",
            ],
        )
        e_object_fail = [
            task
            for task, (ok, _) in probe["E/artifact-object-only: source year unamended"].items()
            if not ok
        ]
        self.assertIn(TASK5, e_object_fail)
        e_store = probe["E/object-store-access: source year unamended"]
        self.assertTrue(e_store[TASK5][0])
        a_store = probe["A/object-store-access: source year unamended"]
        self.assertFalse(a_store[TASK5][0])

    def test_task5_is_recorded_partition_not_a_currentness_grant(self) -> None:
        probe = later_year_probe()
        c_obj = probe["C/artifact-object-only: source year unamended"]
        self.assertTrue(c_obj[TASK5][0], c_obj[TASK5][1])
        self.assertFalse(c_obj[TASK6][0], c_obj[TASK6][1])
        self.assertIn("unknown", c_obj[TASK6][1])
        b_obj = probe["B/artifact-object-only: source year unamended"]
        self.assertTrue(b_obj[TASK5][0], b_obj[TASK5][1])
        self.assertFalse(b_obj[TASK6][0], b_obj[TASK6][1])
        e_store = probe["E/object-store-access: source year unamended"]
        self.assertTrue(e_store[TASK5][0], e_store[TASK5][1])
        self.assertFalse(e_store[TASK6][0], e_store[TASK6][1])
        self.assertIn("unknown", e_store[TASK6][1])
        c_full = probe["C/full-workspace: source year unamended"]
        self.assertTrue(c_full[TASK5][0], c_full[TASK5][1])
        self.assertTrue(c_full[TASK6][0], c_full[TASK6][1])
        self.assertIn("fact_version_current=True", c_full[TASK6][1])
        self.assertIn("Reconstruction is not a currentness grant", c_obj[TASK5][1])


class EdgeMutations(unittest.TestCase):
    """Removing, corrupting, or misdirecting claimed relationship fields."""

    def _e_consumer(self, payload_changes: dict) -> LaterYearConsumer:
        run = run_shape("E", case_ti_b2())
        assert run.item is not None
        carried = basis_artifact(run.store, run.item)
        assert carried is not None
        mutated = mutate_payload(carried, **payload_changes)
        return LaterYearConsumer(mutated, "object-store-access", store=run.store.as_object_store())

    def test_e_passes_task_5_with_store_and_intact_pointers(self) -> None:
        run = run_shape("E", case_ti_b2())
        rep = grant(run, "object-store-access", None).run("E")
        ok, detail = rep.results[TASK5]
        self.assertTrue(ok, detail)

    def test_e_fails_when_sibling_is_removed(self) -> None:
        rep = self._e_consumer({"sibling": None}).run("E")
        ok, detail = rep.results[TASK5]
        self.assertFalse(ok, detail)
        self.assertIn("includible", detail)

    def test_e_fails_when_reported_key_is_removed(self) -> None:
        rep = self._e_consumer({"reported_key": None}).run("E")
        ok, detail = rep.results[TASK5]
        self.assertFalse(ok, detail)
        self.assertIn("reported", detail)

    def test_e_fails_when_sibling_is_corrupted(self) -> None:
        rep = self._e_consumer({"sibling": "demo.missing"}).run("E")
        ok, _ = rep.results[TASK5]
        self.assertFalse(ok)

    def test_e_fails_when_reported_key_is_misdirected(self) -> None:
        run = run_shape("E", case_ti_b2())
        assert run.item is not None
        carried = basis_artifact(run.store, run.item)
        assert carried is not None
        # Point reported_key at the includible artifact: amount 900, not 1200.
        mutated = mutate_payload(carried, reported_key=f"{OBLIGATION_ID}.includible-interest")
        rep = LaterYearConsumer(mutated, "object-store-access", store=run.store.as_object_store()).run("E")
        ok, detail = rep.results[TASK5]
        self.assertFalse(ok, detail)

    def test_e_fails_when_the_store_is_empty(self) -> None:
        run = run_shape("E", case_ti_b2())
        assert run.item is not None
        carried = basis_artifact(run.store, run.item)
        assert carried is not None
        rep = LaterYearConsumer(carried, "object-store-access", store=ObjectStore({})).run("E")
        ok, _ = rep.results[TASK5]
        self.assertFalse(ok)

    def test_c_survives_pointer_corruption_because_it_does_not_use_pointers(self) -> None:
        run = run_shape("C", case_ti_b2())
        assert run.item is not None
        carried = basis_artifact(run.store, run.item)
        assert carried is not None
        mutated = mutate_payload(carried, sibling="demo.missing", reported_key="demo.missing")
        rep = LaterYearConsumer(mutated, "artifact-object-only").run("C")
        ok, detail = rep.results[TASK5]
        self.assertTrue(ok, detail)

    def test_c_fails_when_copied_amounts_are_removed(self) -> None:
        run = run_shape("C", case_ti_b2())
        assert run.item is not None
        carried = basis_artifact(run.store, run.item)
        assert carried is not None
        mutated = mutate_payload(carried, reported=None, includible=None)
        rep = LaterYearConsumer(mutated, "artifact-object-only").run("C")
        ok, detail = rep.results[TASK5]
        self.assertFalse(ok, detail)

    def test_e_rejects_same_valued_foreign_item_targets(self) -> None:
        run = run_shape("E", case_ti_b2())
        assert run.item is not None
        carried = basis_artifact(run.store, run.item)
        assert carried is not None
        store = run.store.as_object_store()
        reported = store.get(f"{OBLIGATION_ID}.source-report")
        includible = store.get(f"{OBLIGATION_ID}.includible-interest")
        assert reported is not None and includible is not None
        foreign_r = replace(reported, key="foreign.reported", item="demo.obligation-other")
        foreign_i = replace(includible, key="foreign.includible", item="demo.obligation-other")
        store.artifacts[foreign_r.key] = foreign_r
        store.artifacts[foreign_i.key] = foreign_i
        mutated = mutate_payload(carried, sibling=foreign_i.key, reported_key=foreign_r.key)
        rep = LaterYearConsumer(mutated, "object-store-access", store=store).run("E")
        ok, detail = rep.results[TASK5]
        self.assertFalse(ok, detail)
        self.assertIn("foreign-item", detail)

    def test_e_rejects_wrong_kind_target(self) -> None:
        run = run_shape("E", case_ti_b2())
        assert run.item is not None
        carried = basis_artifact(run.store, run.item)
        assert carried is not None
        mutated = mutate_payload(carried, sibling=f"{OBLIGATION_ID}.source-report")
        rep = LaterYearConsumer(mutated, "object-store-access", store=run.store.as_object_store()).run("E")
        ok, detail = rep.results[TASK5]
        self.assertFalse(ok, detail)
        self.assertIn("wrong-kind", detail)

    def test_e_rejects_wrong_producer_rule(self) -> None:
        run = run_shape("E", case_ti_b2())
        assert run.item is not None
        carried = basis_artifact(run.store, run.item)
        assert carried is not None
        store = run.store.as_object_store()
        inc = store.get(f"{OBLIGATION_ID}.includible-interest")
        assert inc is not None
        wrong = replace(inc, provenance=replace(inc.provenance, rule_id="demo.rule.basis-reduction"))
        store.artifacts[inc.key] = wrong
        rep = LaterYearConsumer(carried, "object-store-access", store=store).run("E")
        ok, detail = rep.results[TASK5]
        self.assertFalse(ok, detail)
        self.assertIn("wrong-rule", detail)

    def test_e_rejects_wrong_producer_rule_version(self) -> None:
        run = run_shape("E", case_ti_b2())
        assert run.item is not None
        carried = basis_artifact(run.store, run.item)
        assert carried is not None
        store = run.store.as_object_store()
        inc = store.get(f"{OBLIGATION_ID}.includible-interest")
        assert inc is not None
        wrong = replace(inc, provenance=replace(inc.provenance, rule_version=99))
        store.artifacts[inc.key] = wrong
        rep = LaterYearConsumer(carried, "object-store-access", store=store).run("E")
        ok, detail = rep.results[TASK5]
        self.assertFalse(ok, detail)
        self.assertIn("wrong-rule-version", detail)

    def test_e_rejects_store_key_differing_from_self_key(self) -> None:
        run = run_shape("E", case_ti_b2())
        assert run.item is not None
        carried = basis_artifact(run.store, run.item)
        assert carried is not None
        store = run.store.as_object_store()
        lookup = f"{OBLIGATION_ID}.includible-interest"
        inc = store.get(lookup)
        assert inc is not None
        store.artifacts[lookup] = replace(inc, key="other-self-key")
        rep = LaterYearConsumer(carried, "object-store-access", store=store).run("E")
        ok, detail = rep.results[TASK5]
        self.assertFalse(ok, detail)
        self.assertIn("self-key-mismatch", detail)

    def test_c_rejects_mutated_component_producer(self) -> None:
        run = run_shape("C", case_ti_b2())
        assert run.item is not None
        carried = basis_artifact(run.store, run.item)
        assert carried is not None
        comps = dict(carried.payload["components"])
        comps["reported"] = comps["amount"]
        mutated = mutate_payload(carried, components=comps)
        rep = LaterYearConsumer(mutated, "artifact-object-only").run("C")
        ok, detail = rep.results[TASK5]
        self.assertFalse(ok, detail)
        self.assertIn("wrong producer", detail)


class SourceCorrectionThroughConsumer(unittest.TestCase):
    """Reported-amount correction must not leave stale partition fields current."""

    def test_c_identifies_copied_partition_as_historical(self) -> None:
        ws = case_ti_b2()
        run = run_shape("C", ws)
        corrected = ws.with_correction(ws.names.reported_amount, 1000)
        rep = grant(run, "currentness", corrected).run("C")
        ok5, detail5 = rep.results[TASK5]
        self.assertTrue(ok5, detail5)
        ok6, detail6 = rep.results[TASK6]
        self.assertTrue(ok6)
        self.assertIn("fact_version_current=False", detail6)
        self.assertIn("historical", detail6)
        ok4, detail4 = rep.results["4 detect a corrected or displaced source-year fact"]
        self.assertTrue(ok4)
        self.assertIn("carried_displaced=False", detail4)

    def test_b_is_wholly_displaced_by_the_same_correction(self) -> None:
        ws = case_ti_b2()
        run = run_shape("B", ws)
        corrected = ws.with_correction(ws.names.reported_amount, 1000)
        rep = grant(run, "currentness", corrected).run("B")
        _, detail4 = rep.results["4 detect a corrected or displaced source-year fact"]
        self.assertIn("carried_displaced=True", detail4)
        ok5, detail5 = rep.results[TASK5]
        self.assertTrue(ok5, detail5)
        _, detail6 = rep.results[TASK6]
        self.assertIn("fact_version_current=False", detail6)
        self.assertIn("historical", detail6)

    def test_e_full_workspace_recovers_recorded_partition_as_historical(self) -> None:
        ws = case_ti_b2()
        run = run_shape("E", ws)
        corrected = ws.with_correction(ws.names.reported_amount, 1000)
        rep = grant(run, "full-workspace", corrected).run("E")
        ok5, detail5 = rep.results[TASK5]
        self.assertTrue(ok5, detail5)
        _, detail6 = rep.results[TASK6]
        self.assertIn("fact_version_current=False", detail6)
        self.assertIn("historical", detail6)


class SourceReportIndependence(unittest.TestCase):
    """Source-report provenance is the exact statement reads, not tax treatment."""

    def test_ti_b2_source_report_provenance_is_untaxed(self) -> None:
        ws = case_ti_b2()
        before = ws.facts[ws.names.reported_amount]
        for shape in SHAPES:
            with self.subTest(shape=shape):
                run = run_shape(shape, ws)
                self.assertFalse(run.is_blocked)
                reports = [a for a in run.artifacts() if a.kind == "source-report"]
                self.assertEqual(len(reports), 1)
                _assert_source_report_provenance(self, reports[0], ws, 1200)
                treatments = [a for a in run.artifacts() if a.kind != "source-report"]
                self.assertTrue(treatments)
                for art in treatments:
                    _assert_treatment_tax_authority(self, art)
                self.assertEqual(ws.facts[ws.names.reported_amount], before)

    def test_ti_a1_source_report_survives_with_untaxed_provenance(self) -> None:
        ws = CASES["TI-A1"]()
        before = ws.facts[ws.names.reported_amount]
        self.assertEqual(before.value, 840)
        for shape in SHAPES:
            with self.subTest(shape=shape):
                run = run_shape(shape, ws)
                self.assertTrue(run.is_blocked)
                self.assertEqual(refusal(run).code, BLOCK_UNSUPPORTED)
                reports = [a for a in run.store.artifacts.values() if a.kind == "source-report"]
                self.assertEqual(len(reports), 1)
                _assert_source_report_provenance(self, reports[0], ws, 840)
                treatments = [a for a in run.store.artifacts.values() if a.kind != "source-report"]
                self.assertEqual(treatments, [])
                self.assertEqual(ws.facts[ws.names.reported_amount], before)
                self.assertEqual(reports[0].payload["amount"], Decimal(840))

    def test_evaluate_reported_omits_tax_authority_and_coverage(self) -> None:
        for case in ("TI-B2", "TI-A1"):
            with self.subTest(case=case):
                ws = CASES[case]()
                outcome = evaluate_reported(ws)
                self.assertNotIsInstance(outcome, Blocked)
                expected = Decimal(1200 if case == "TI-B2" else 840)
                self.assertEqual(outcome.values["reported"], expected)
                self.assertEqual(outcome.provenance.authority, ())
                self.assertIsNone(outcome.provenance.coverage_id)
                self.assertIsNone(outcome.provenance.coverage_version)
                accounted = outcome.provenance.accounted()
                self.assertIn("authority:omitted", accounted)
                self.assertIn("coverage:omitted", accounted)
                self.assertNotIn(f"coverage:{COVERAGE_ID}.v{COVERAGE_VERSION}", accounted)


class LifecycleMatchesProvenance(unittest.TestCase):
    def test_every_observation_is_in_provenance_iff_displaced(self) -> None:
        for label, (passed, detail) in independent_lifecycle().items():
            with self.subTest(observation=label):
                self.assertTrue(passed, detail)


if __name__ == "__main__":
    unittest.main()
