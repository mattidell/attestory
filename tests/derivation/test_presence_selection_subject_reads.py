"""ADR 0077 Parts 3 and 4 at runtime: presence selection with same-run subject reads.

The Track 1a-4 worksheet declaration is a real ``rule-artifact.v13`` rule in
an ``artifact-package.v35`` package (``adr0077_worksheet_fixture``). Every
runtime case goes through package validation, resolution, marshalling from
a kernel state, and both runners, which must agree on values, pins, and
blocked rows. Only the guard cases at the end edit a marshalled rule, to
reach contract failures package validation already refuses.
"""

from __future__ import annotations

import copy
import unittest
from typing import Any

from packages.derivation.loader import DerivationSchemas
from packages.derivation.runner import RunContext, RunResult
from tests.derivation import adr0077_worksheet_fixture as fx


def codes(validation: Any) -> list[str]:
    return [issue.code for issue in validation.issues]


def run_case(rows: list[dict[str, Any]], citizens: list[tuple[dict[str, Any], str]] | None = None,
             **kwargs: Any) -> tuple[RunResult, RunResult]:
    ctx = fx.marshal(citizens or fx.parts(), rows, **kwargs)
    return fx.both_runners(ctx)


def derived_pins(pins: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [pin for pin in pins if pin.get("origin") == "derived"]


def published_ids(result: RunResult, prefix: str) -> dict[str, str]:
    """Keyed symbol -> finding id for one per-subject publisher."""
    return {
        pub.finding["symbol"]: pub.finding["id"]
        for pub in result.publications
        if pub.finding["symbol"].startswith(prefix + "|")
    }


def blocked_symbols(result: RunResult, prefix: str) -> list[str]:
    return sorted(
        str(row.get("symbol")) for row in result.dispositions
        if row.get("disposition") == "blocked" and str(row.get("symbol", "")).startswith(prefix + "|")
    )


class Agreeing(unittest.TestCase):
    def assert_agree(self, forward: RunResult, reference: RunResult) -> None:
        self.assertEqual(fx.signature(forward), fx.signature(reference))


class WorksheetValidates(unittest.TestCase):
    """Part 4 "Validation" and Part 3 "Validation" on the real declaration."""

    def test_the_track_1a4_declaration_validates_as_v13_in_a_v35_package(self) -> None:
        _package, validation = fx.validate(fx.parts())
        self.assertTrue(validation.ok, validation.issues)

    def test_reachability_from_the_worksheet_alone(self) -> None:
        # The declared reads and the activity are edges: the worksheet reaches
        # every status rule, the conclusion chain, the activity facts and the
        # family without listing them. (A standalone fact type reached only
        # by a ref name is unreachable for every rule today; not this track.)
        _package, validation = fx.validate(fx.parts(), entrypoints=[fx.WORKSHEET, fx.COUNT_RULE])
        unreachable = {issue.member_id for issue in validation.issues if issue.code == "MEMBER_UNREACHABLE"}
        expected_reached = {
            *fx.STATUS_RULE.values(), *fx.ANSWERS, fx.STATEMENT_RULE, fx.SUPPORT_RULE,
            fx.INCL, fx.FIN, fx.FAMILY, fx.BOX1, "tax.us.2025.rule.sli-worksheet-line1-subtotal",
        }
        self.assertEqual(unreachable & expected_reached, set())

    def _worksheet_issue(self, edit: Any) -> list[str]:
        sheet = fx.worksheet()
        edit(sheet)
        _package, validation = fx.validate(fx.parts(worksheet_rule=sheet))
        return codes(validation)

    def test_a_rule_with_subject_and_selection_is_rejected(self) -> None:
        def edit(sheet: dict[str, Any]) -> None:
            sheet["subject"] = {"id": fx.BOX1, "version": "v1"}
        self.assertIn("RULE_SELECTION_SUBJECT_INVALID", self._worksheet_issue(edit))

    def test_top_level_must_be_neutral(self) -> None:
        def edit(sheet: dict[str, Any]) -> None:
            sheet["requires"] = ["rounding.convention"]
        self.assertIn("RULE_DECLARATIVE_TOP_LEVEL_INVALID", self._worksheet_issue(edit))

    def test_path_ids_are_unique_and_neither_is_reserved(self) -> None:
        def duplicate(sheet: dict[str, Any]) -> None:
            sheet["selection"]["paths"][1]["id"] = "old"
        self.assertIn("RULE_SELECTION_PATH_IDS_NOT_UNIQUE", self._worksheet_issue(duplicate))

        def reserved(sheet: dict[str, Any]) -> None:
            sheet["selection"]["paths"][1]["id"] = "neither"
        self.assertIn("RULE_SELECTION_PATH_IDS_NOT_UNIQUE", self._worksheet_issue(reserved))

    def test_activity_members_resolve_on_the_fact_surface(self) -> None:
        def edit(sheet: dict[str, Any]) -> None:
            sheet["selection"]["paths"][1]["activity"]["member_fact_types"] = [
                {"id": "demo.tax.adr0077.undeclared", "version": "v1"},
            ]
        self.assertIn("RULE_SELECTION_ACTIVITY_SURFACE_INVALID", self._worksheet_issue(edit))

    def test_requires_are_the_refs_and_undeclared_collects(self) -> None:
        def missing_ref(sheet: dict[str, Any]) -> None:
            path = sheet["selection"]["paths"][0]
            path["requires"] = path["requires"][1:]
            path["pins"] = path["pins"][1:]
        self.assertIn("RULE_SELECTION_DEPENDENCIES_INVALID", self._worksheet_issue(missing_ref))

        def declared_symbol_as_requires(sheet: dict[str, Any]) -> None:
            path = sheet["selection"]["paths"][1]
            path["requires"] = [*path["requires"], fx.CONCLUSION]
            path["pins"] = [*path["pins"], {"role": "input", "id": fx.CONCLUSION, "version": "v1", "origin": "assertion"}]
        self.assertIn("RULE_SELECTION_DEPENDENCIES_INVALID", self._worksheet_issue(declared_symbol_as_requires))

    def test_path_pins_are_one_per_requires_in_order(self) -> None:
        def reordered(sheet: dict[str, Any]) -> None:
            path = sheet["selection"]["paths"][0]
            path["pins"] = list(reversed(path["pins"]))
        self.assertIn("RULE_SELECTION_PINS_INVALID", self._worksheet_issue(reordered))

        def relabelled(sheet: dict[str, Any]) -> None:
            path = sheet["selection"]["paths"][0]
            path["pins"][1] = {**path["pins"][1], "origin": "declared_default"}
        self.assertIn("RULE_SELECTION_PINS_INVALID", self._worksheet_issue(relabelled))

    def test_a_declared_read_needs_a_publisher_with_that_subject(self) -> None:
        def no_publisher(sheet: dict[str, Any]) -> None:
            sheet["selection"]["paths"][1]["reads_subject_results"] = [
                {"symbol": "demo.tax.adr0077.unpublished", "subject": {"id": fx.BOX1, "version": "v1"}},
            ]
        self.assertIn("RULE_SUBJECT_RESULTS_INVALID", self._worksheet_issue(no_publisher))

        def wrong_subject(sheet: dict[str, Any]) -> None:
            sheet["selection"]["paths"][1]["reads_subject_results"] = [
                {"symbol": fx.CONCLUSION, "subject": {"id": fx.INCL, "version": "v1"}},
            ]
        self.assertIn("RULE_SUBJECT_RESULTS_INVALID", self._worksheet_issue(wrong_subject))


class TrackOneA4Cases(Agreeing):
    """The five Track 1a-4 cases under one declaration (ADR 0077 Part 4)."""

    def test_old_only_publishes_2500_pinning_five_derived_entries(self) -> None:
        forward, reference = run_case(fx.case_rows("old-only"))
        self.assert_agree(forward, reference)
        status_ids = {
            finding_id
            for answer in fx.ANSWERS
            for finding_id in published_ids(forward, fx.STATUS[answer]).values()
        }
        self.assertEqual(len(status_ids), 5)
        for result in (forward, reference):
            outcome = fx.line21(result)
            self.assertEqual(outcome["value"], "2500")
            finding = outcome["finding"]
            self.assertEqual(finding["schema"], "derived-finding.v3")
            self.assertEqual(finding["version"], "v3")
            self.assertEqual(
                derived_pins(finding["pins"]),
                [{"role": "input", "id": fid, "version": "v2", "origin": "derived"} for fid in sorted(status_ids)],
            )
            # The entry is pinned once, as derived, never as an asserted input.
            self.assertFalse(any(
                pin["id"] in status_ids and pin.get("origin") != "derived" for pin in finding["pins"]
            ))
            DerivationSchemas().validate_declared(finding)

    def test_new_only_publishes_2500_while_the_inactive_path_is_blocked(self) -> None:
        forward, reference = run_case(fx.case_rows("new-only"))
        self.assert_agree(forward, reference)
        conclusions = published_ids(forward, fx.CONCLUSION)
        self.assertEqual(list(conclusions), [f"{fx.CONCLUSION}|{fx.box_fact_id('demo-stmt')}"])
        for result in (forward, reference):
            # Every old-path status blocked; none of those blocks is the worksheet's result.
            for answer in fx.ANSWERS:
                self.assertEqual(blocked_symbols(result, fx.STATUS[answer]),
                                 [f"{fx.STATUS[answer]}|{fx.box_fact_id('demo-stmt')}"])
            outcome = fx.line21(result)
            self.assertEqual(outcome["value"], "2500")
            self.assertEqual(
                derived_pins(outcome["finding"]["pins"]),
                [{"role": "input", "id": next(iter(conclusions.values())), "version": "v2", "origin": "derived"}],
            )

    def test_both_present_blocks_on_the_named_token_and_pins_activity(self) -> None:
        forward, reference = run_case(fx.case_rows("both"))
        self.assert_agree(forward, reference)
        for result in (forward, reference):
            outcome = fx.line21(result)
            self.assertEqual(outcome["disposition"], "blocked")
            self.assertEqual(outcome["code"], "DEPENDENCY_INVALID")
            self.assertEqual(outcome["missing"], [fx.BOTH_TOKEN])
            inputs = {pin["id"] for pin in outcome["pins"] if pin["role"] == "input"}
            self.assertEqual(inputs, {
                *(f"demo.finding.answer.{tail}.demo-stmt" for tail in fx.ANSWER_TAILS),
                "demo.finding.inclusion.demo-stmt.demo-loan",
            })
            self.assertEqual(derived_pins(outcome["pins"]), [])

    def test_closed_empty_publishes_zero_with_no_derived_pin(self) -> None:
        forward, reference = run_case(fx.case_rows("closed-empty"))
        self.assert_agree(forward, reference)
        for result in (forward, reference):
            outcome = fx.line21(result)
            self.assertEqual(outcome["value"], "0")
            self.assertEqual(outcome["finding"]["schema"], "derived-finding.v2")
            self.assertEqual(derived_pins(outcome["finding"]["pins"]), [])
            self.assertIn("demo.finding.f1098e-closure", {pin["id"] for pin in outcome["finding"]["pins"]})

    def test_nonempty_neither_blocks_naming_the_statements(self) -> None:
        rows = [*fx.case_rows("nonempty-neither"), fx.box("demo-stmt-b", "1000")]
        forward, reference = run_case(rows)
        self.assert_agree(forward, reference)
        for result in (forward, reference):
            outcome = fx.line21(result)
            self.assertEqual(outcome["disposition"], "blocked")
            self.assertEqual(outcome["code"], "DEPENDENCY_INVALID")
            self.assertEqual(outcome["missing"], sorted([fx.box_fact_id("demo-stmt"), fx.box_fact_id("demo-stmt-b")]))


class SelectedPathEntries(Agreeing):
    """Part 3 "Runtime" and "Coverage" on the selected path."""

    def test_a_blocked_statement_on_the_selected_path_refuses_and_names_it(self) -> None:
        rows = [
            *fx.return_inputs(),
            fx.box("demo-stmt"), *fx.links("demo-stmt", "demo-loan"),
            fx.box("demo-stmt-b"), *fx.links("demo-stmt-b", "demo-loan-b", loan_answer=None),
        ]
        forward, reference = run_case(rows)
        self.assert_agree(forward, reference)
        for result in (forward, reference):
            self.assertEqual(blocked_symbols(result, fx.CONCLUSION),
                             [f"{fx.CONCLUSION}|{fx.box_fact_id('demo-stmt-b')}"])
            outcome = fx.line21(result)
            self.assertEqual(outcome["disposition"], "blocked")
            self.assertEqual(outcome["code"], "DEPENDENCY_INVALID")
            self.assertEqual(outcome["missing"], [fx.box_fact_id("demo-stmt-b")])

    def test_a_statement_with_no_result_refuses_and_names_it(self) -> None:
        # A false per-subject guard records neither a publication nor a block.
        statement = fx.rule(
            fx.STATEMENT_RULE, subject=fx.BOX1, joined=fx.INCL, direction="joined_contains_subject",
            publishes=fx.CONCLUSION, value=fx._statement_value(),
            when={"op": "compare", "cmp": "gt", "left": {"op": "ref", "name": fx.BOX1}, "right": 0},
        )
        rows = [
            *fx.return_inputs(),
            fx.box("demo-stmt"), *fx.links("demo-stmt", "demo-loan"),
            fx.box("demo-stmt-b", "0"), *fx.links("demo-stmt-b", "demo-loan-b"),
        ]
        forward, reference = run_case(rows, fx.parts(statement_rule=statement))
        self.assert_agree(forward, reference)
        for result in (forward, reference):
            self.assertEqual(sorted(published_ids(result, fx.CONCLUSION)),
                             [f"{fx.CONCLUSION}|{fx.box_fact_id('demo-stmt')}"])
            self.assertEqual(blocked_symbols(result, fx.CONCLUSION), [])
            outcome = fx.line21(result)
            self.assertEqual(outcome["disposition"], "blocked")
            self.assertEqual(outcome["code"], "DEPENDENCY_INVALID")
            self.assertEqual(outcome["missing"], [fx.box_fact_id("demo-stmt-b")])

    def test_two_supported_statements_publish_with_both_entries_pinned(self) -> None:
        rows = [
            *fx.return_inputs(),
            fx.box("demo-stmt", "1000"), *fx.links("demo-stmt", "demo-loan"),
            fx.box("demo-stmt-b", "800"), *fx.links("demo-stmt-b", "demo-loan-b"),
        ]
        forward, reference = run_case(rows)
        self.assert_agree(forward, reference)
        conclusions = published_ids(forward, fx.CONCLUSION)
        self.assertEqual(len(conclusions), 2)
        for result in (forward, reference):
            outcome = fx.line21(result)
            self.assertEqual(outcome["value"], "1800")
            self.assertEqual(
                [pin["id"] for pin in derived_pins(outcome["finding"]["pins"])],
                sorted(conclusions.values()),
            )

    def test_a_not_supported_entry_reads_and_the_worksheet_refuses_on_its_own_value(self) -> None:
        # Two current financing rows: the statement publishes not-supported.
        rows = [*fx.return_inputs(), fx.box(), *fx.links()]
        rows.append(fx.row(
            "demo.finding.financing.demo-loan.second", fx.FIN,
            (("borrowing", "demo-loan"), ("period", "demo-2023"), ("institution", "demo-college"),
             ("programme", "demo-programme")),
            "sli.financing.affirmed",
        ))
        forward, reference = run_case(rows)
        self.assert_agree(forward, reference)
        conclusions = {pub.finding["value"] for pub in forward.publications
                       if pub.finding["symbol"].startswith(fx.CONCLUSION + "|")}
        self.assertEqual(conclusions, {fx.NOT})
        for result in (forward, reference):
            outcome = fx.line21(result)
            self.assertNotIn("value", outcome)
            self.assertEqual(outcome["disposition"], "blocked")


class LazyRead(Agreeing):
    """The declared read refuses only when the selected expression reaches it."""

    def test_married_filing_separately_blocks_before_reading_the_entries(self) -> None:
        rows = [
            *fx.return_inputs(filing_status="married_filing_separately"),
            fx.box(), *fx.links(loan_answer=None),
        ]
        forward, reference = run_case(rows)
        self.assert_agree(forward, reference)
        for result in (forward, reference):
            outcome = fx.line21(result)
            self.assertEqual(outcome["code"], "SLI_MFS_INELIGIBLE")
            self.assertEqual(derived_pins(outcome["pins"]), [])


class ActivityOnlySource(Agreeing):
    """A selection whose activity fact type appears nowhere else in any rule.

    The current row must reach marshalling and select its path, not
    silently take the default. It is registered as a source only: it binds
    no scalar input and is not a collect name.
    """

    ONLY_A = "demo.tax.adr0077.activity-only-a"
    ONLY_B = "demo.tax.adr0077.activity-only-b"
    SYMBOL = "demo.tax.adr0077.activity-only-result"

    def _citizens(self) -> list[tuple[dict[str, Any], str]]:
        def path(path_id: str, member: str, value: int) -> dict[str, Any]:
            return {
                "id": path_id,
                "activity": {"kind": "source_nonempty", "member_fact_types": [{"id": member, "version": "v1"}]},
                "reads_subject_results": [], "requires": [], "pins": [], "when": True, "value": value,
            }
        selector = fx.rule("demo.rule.adr0077.activity-only", publishes=self.SYMBOL, value=0)
        selector.pop("value")
        selector["selection"] = {
            "mode": "exclusive_presence",
            "conflict": "refuse",
            "paths": [path("a", self.ONLY_A, 1), path("b", self.ONLY_B, 2)],
            "default": {"id": "neither", "reads_subject_results": [], "requires": [], "pins": [],
                        "when": True, "value": 0},
            "refusal": {"code": "DEPENDENCY_INVALID", "missing": ["demo-activity-only-both"], "pins": []},
        }
        return [
            (fx.fact_type(self.ONLY_A, fx.YEAR_KEYS, ["present"]), "fact-type"),
            (fx.fact_type(self.ONLY_B, fx.YEAR_KEYS, ["present"]), "fact-type"),
            (selector, "computation"),
        ]

    def _row(self, member: str) -> dict[str, Any]:
        return fx.row(f"demo.finding.{member.rsplit('.', 1)[-1]}", member, (("tax-year", "2025"),), "present")

    def _run_rows(self, rows: list[dict[str, Any]]) -> tuple[RunContext, dict[str, Any]]:
        ctx = fx.marshal(self._citizens(), rows, closed=False)
        forward, reference = fx.both_runners(ctx)
        self.assert_agree(forward, reference)
        found = [pub.finding for pub in forward.publications if pub.finding["symbol"] == self.SYMBOL]
        rows_out = [row for row in forward.dispositions if row.get("artifact_id") == "demo.rule.adr0077.activity-only"]
        return ctx, {"value": found[0]["value"] if found else None, "row": rows_out[0]}

    def test_the_current_row_selects_its_path(self) -> None:
        ctx, outcome = self._run_rows([self._row(self.ONLY_A)])
        self.assertEqual(outcome["value"], "1")
        self.assertIn(self.ONLY_A, {source.name for source in ctx.sources})
        # Source delivery only: no scalar input, no collect read.
        self.assertNotIn(self.ONLY_A, {item.symbol for item in ctx.inputs})
        _ctx, outcome = self._run_rows([self._row(self.ONLY_B)])
        self.assertEqual(outcome["value"], "2")

    def test_no_row_takes_the_default_and_both_refuse(self) -> None:
        _ctx, outcome = self._run_rows([])
        self.assertEqual(outcome["value"], "0")
        _ctx, outcome = self._run_rows([self._row(self.ONLY_A), self._row(self.ONLY_B)])
        self.assertIsNone(outcome["value"])
        self.assertEqual(outcome["row"]["missing"], ["demo-activity-only-both"])
        self.assertEqual(
            sorted(pin["id"] for pin in outcome["row"]["pins"] if pin["role"] == "input"),
            ["demo.finding.activity-only-a", "demo.finding.activity-only-b"],
        )


def _marshalled() -> RunContext:
    return fx.marshal(fx.parts(), fx.case_rows("old-only"))


def _with_worksheet(ctx: RunContext, edit: Any) -> RunContext:
    rules = copy.deepcopy(ctx.rules)
    for item in rules:
        if item["id"] == fx.WORKSHEET:
            edit(item)
    return RunContext(**{**ctx.__dict__, "rules": rules})


class SelectionNeverFallsThrough(Agreeing):
    """A contract failure blocks with the existing token; ``rule["value"]`` is never read."""

    def _blocked(self, edit: Any, token: str) -> None:
        forward, reference = fx.both_runners(_with_worksheet(_marshalled(), edit))
        self.assert_agree(forward, reference)
        for result in (forward, reference):
            outcome = fx.line21(result)
            self.assertEqual(outcome["disposition"], "blocked")
            self.assertEqual(outcome["code"], "DEPENDENCY_INVALID")
            self.assertEqual(outcome["missing"], [token])

    def test_top_level_contract(self) -> None:
        def edit(sheet: dict[str, Any]) -> None:
            sheet["when"] = False
        self._blocked(edit, "declarative-top-level-contract-invalid")

    def test_duplicate_path_ids(self) -> None:
        def edit(sheet: dict[str, Any]) -> None:
            sheet["selection"]["paths"][1]["id"] = "old"
        self._blocked(edit, "selection-path-id-duplicate")

    def test_path_pin_contract(self) -> None:
        def edit(sheet: dict[str, Any]) -> None:
            sheet["selection"]["paths"][0]["pins"] = []
        self._blocked(edit, "selection-path-pin-contract-invalid")

    def test_a_selection_on_another_schema_is_never_evaluated_as_a_value_rule(self) -> None:
        def edit(sheet: dict[str, Any]) -> None:
            sheet["schema"] = "rule-artifact.v12"
        self._blocked(edit, "declarative-top-level-contract-invalid")


if __name__ == "__main__":
    unittest.main()
