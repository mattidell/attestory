"""Executable v9 bounded nominee-selection contract evidence.

This is a contract-unit test surface, not production v37 coverage.  The
fixtures deliberately exercise the adopted rule-artifact.v9 selection and its
distinct aggregate producer directly through schema validation, package
closure, and the real saturation runner.
"""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any, cast

from packages.derivation.authorization_closure import rule_scoped_closure
from packages.derivation.loader import DERIVATION_SCHEMA_DIR, DerivationSchemas
from packages.derivation.package_validation import (
    package_instance_checksum,
    validate_package,
)
from packages.derivation.runner import InputFinding, RunContext, SourceFact, run
from packages.kernel.schema_registry import SchemaValidationError
from packages.tax.nominee_allocation_recording import derive_nominee_allocation_fact_id
from packages.tax.nominee_consequences import (
    DERIVED_NOMINEE_SYMBOL,
    NOMINEE_AGGREGATE_RULE_ID,
    NOMINEE_ALLOCATIONS_EXCEED_REPORT,
    PUBLISHES,
    RULE_ID,
)
from packages.tax.report_statement_identity import (
    REPORT_FACT_TYPE,
    derive_1099int_box1_fact_id,
    derive_reported_payer_entity_id,
    derive_reported_statement_entity_id,
)


ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
EXAMPLES = ROOT / "packages" / "sample_data" / "derivation" / "examples"
DERIVATION_PACKAGE = EXAMPLES / "artifact-package.v30.nominee-contract.positive.json"
LINE2B = EXAMPLES / "rule-artifact.v9.nominee-line2b-selection.json"
AGGREGATE = EXAMPLES / "rule-artifact.v9.nominee-aggregate.json"

ADOPTION = {"role": "adoption", "id": "demo.package.nominee-v9", "version": "v1"}
YEAR = 2025
PAYER = "Demo Bank"
STATEMENT = "acct 123"
RECIPIENT = "demo.recipient.pat"

BASE_SYMBOLS = (
    "tax.us.2025.interest.b1-subtotal",
    "tax.us.2025.interest.b3-subtotal",
    "tax.us.2025.interest.oid-subtotal",
    "tax.us.2025.interest.non-form-subtotal",
    "tax.us.2025.interest.form1065-k1-box5-subtotal",
    "tax.us.2025.interest.b10-market-discount-subtotal",
    "tax.us.2025.interest.oid-b5-market-discount-subtotal",
)
ADJUSTMENT_SYMBOLS = (
    "tax.us.2025.interest.scheduleb-abp-adjustment-subtotal",
    "tax.us.2025.interest.current-year-adjustment-subtotal",
)
LEGACY_AMOUNT = "tax.us.2025.scheduleb.adjustment.nominee.amount"
LEGACY_SUBTOTAL = "tax.us.2025.interest.scheduleb-nominee-subtotal"


def _load(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text("utf-8")))


def _content_corpus() -> dict[tuple[str, str], dict[str, Any]]:
    corpus: dict[tuple[str, str], dict[str, Any]] = {}
    for path in sorted(CONTENT.glob("*.json")):
        try:
            citizen = _load(path)
        except (OSError, json.JSONDecodeError):
            continue
        if (
            isinstance(citizen, dict)
            and isinstance(citizen.get("id"), str)
            and isinstance(citizen.get("version"), str)
            and not ("citizens" in citizen and "packages" in citizen)
        ):
            corpus[(citizen["id"], citizen["version"])] = citizen
    for path in (LINE2B, AGGREGATE):
        citizen = _load(path)
        corpus[(citizen["id"], citizen["version"])] = citizen
    return corpus


def _id_corpus() -> dict[str, dict[str, Any]]:
    return {
        (citizen["id"]): citizen
        for citizen in _content_corpus().values()
    }


def _report_keys() -> tuple[tuple[str, str], ...]:
    return (
        ("payer", derive_reported_payer_entity_id(PAYER)),
        (
            "statement",
            derive_reported_statement_entity_id(
                payer_name=PAYER, statement_reference=STATEMENT
            ),
        ),
        ("tax-year", str(YEAR)),
    )


def _allocation_keys() -> tuple[tuple[str, str], ...]:
    return _report_keys() + (("recipient", RECIPIENT),)


def _report_source(value: str = "1200") -> SourceFact:
    return SourceFact(
        REPORT_FACT_TYPE,
        value,
        "demo.report.box1",
        derive_1099int_box1_fact_id(
            payer_name=PAYER, statement_reference=STATEMENT, tax_year=YEAR
        ),
        keys=_report_keys(),
    )


def _allocation_source(value: str = "10") -> SourceFact:
    return SourceFact(
        "tax.us.nominee-allocation.amount",
        value,
        "demo.allocation.pat",
        derive_nominee_allocation_fact_id(
            payer_name=PAYER,
            statement_reference=STATEMENT,
            tax_year=YEAR,
            recipient_id=RECIPIENT,
        ),
        keys=_allocation_keys(),
    )


def _inputs(*, legacy: str | None = None) -> list[InputFinding]:
    values = {symbol: "100" for symbol in BASE_SYMBOLS + ADJUSTMENT_SYMBOLS}
    if legacy is not None:
        values[LEGACY_SUBTOTAL] = legacy
    return [
        InputFinding(symbol, value, f"demo.input.{index:02d}", "input")
        for index, (symbol, value) in enumerate(values.items())
    ]


def _rules() -> list[dict[str, Any]]:
    return [
        _load(CONTENT / "rule.interest.nominee-reduction.json"),
        _load(AGGREGATE),
        _load(LINE2B),
    ]


def _context(
    *,
    sources: list[SourceFact],
    inputs: list[InputFinding] | None = None,
    rules: list[dict[str, Any]] | None = None,
) -> RunContext:
    return RunContext(
        run_id="demo.run.nominee-v9-contract",
        rules=_rules() if rules is None else rules,
        parameters={},
        canon={},
        inputs=_inputs() if inputs is None else inputs,
        sources=sources,
        adoption_pin=ADOPTION,
        governance_pins=[],
        reporting_year=YEAR,
    )


def _validate_candidate(citizen: dict[str, Any]) -> Any:
    package = _load(DERIVATION_PACKAGE)
    corpus = _content_corpus()
    corpus[(citizen["id"], citizen["version"])] = citizen
    return validate_package(package, corpus, DerivationSchemas())


def _findings(result: Any, symbol: str) -> list[dict[str, Any]]:
    return [pub.finding for pub in result.publications if pub.finding["symbol"] == symbol]


class BoundedNomineeRuntime(unittest.TestCase):
    """I0/I1/I7/I8 plus the selected-path adversarial runtime probes."""

    def setUp(self) -> None:
        self.schemas = DerivationSchemas()

    def test_i0_neither_has_ordinary_result_and_no_invented_zero(self) -> None:
        result = run(_context(sources=[]), self.schemas)

        total = _findings(result, "tax.us.2025.interest.taxable-total")
        self.assertEqual(len(total), 1)
        self.assertEqual(total[0]["value"], "500")
        self.assertEqual(_findings(result, DERIVED_NOMINEE_SYMBOL), [])
        self.assertEqual(
            _findings(result, PUBLISHES),
            [],
            "absence is an inapplicable outcome, not a zero finding",
        )
        aggregate_rows = [
            row
            for row in result.dispositions
            if row["artifact_id"] == NOMINEE_AGGREGATE_RULE_ID
        ]
        self.assertEqual(len(aggregate_rows), 1)
        self.assertEqual(aggregate_rows[0]["disposition"], "inapplicable")
        self.assertTrue(aggregate_rows[0]["no_source_activity"])

    def test_i1_new_only_publishes_one_owned_aggregate_and_subtracts_once(self) -> None:
        result = run(
            _context(sources=[_report_source(), _allocation_source()]), self.schemas
        )

        reduction = _findings(
            result,
            f"{PUBLISHES}|tax.us.2025.f1099int.box1-interest|"
            f"payer={derive_reported_payer_entity_id(PAYER)},"
            f"statement={derive_reported_statement_entity_id(payer_name=PAYER, statement_reference=STATEMENT)},"
            f"tax-year={YEAR}",
        )
        self.assertEqual(len(reduction), 1)
        self.assertEqual(reduction[0]["value"], "10")
        aggregate = _findings(result, DERIVED_NOMINEE_SYMBOL)
        self.assertEqual(len(aggregate), 1)
        self.assertEqual(aggregate[0]["value"], "10")
        self.assertEqual(
            aggregate[0]["pins"]
            and {
                pin["id"] for pin in aggregate[0]["pins"] if pin["role"] == "input"
            },
            {reduction[0]["id"]},
        )
        total = _findings(result, "tax.us.2025.interest.taxable-total")
        self.assertEqual(len(total), 1)
        self.assertEqual(total[0]["value"], "490")
        self.assertEqual(
            [pub.finding["symbol"] for pub in result.publications].count(
                "tax.us.2025.interest.taxable-total"
            ),
            1,
        )
        self.assertEqual(
            {
                row["artifact_id"]
                for row in result.dispositions
                if row["disposition"] == "published"
                and row.get("symbol") == DERIVED_NOMINEE_SYMBOL
            },
            {NOMINEE_AGGREGATE_RULE_ID},
        )

    def test_i7_legacy_only_uses_legacy_path_without_report_or_aggregate(self) -> None:
        legacy = SourceFact(LEGACY_AMOUNT, "5", "demo.legacy.nominee")
        result = run(
            _context(sources=[legacy], inputs=_inputs(legacy="5")), self.schemas
        )

        total = _findings(result, "tax.us.2025.interest.taxable-total")
        self.assertEqual(len(total), 1)
        self.assertEqual(total[0]["value"], "495")
        self.assertEqual(_findings(result, DERIVED_NOMINEE_SYMBOL), [])
        self.assertFalse(
            any(
                finding["symbol"].startswith(PUBLISHES + "|")
                for pub in result.publications
                for finding in [pub.finding]
            )
        )
        line = next(
            row
            for row in result.dispositions
            if row["artifact_id"] == "tax.us.2025.rule.form1040-line2b"
        )
        self.assertEqual(line["disposition"], "published")
        self.assertIn(
            "demo.input.09",
            {pin["id"] for pin in line["pins"] if pin["role"] == "input"},
        )

    def test_i8_both_present_refuses_without_line_subtraction(self) -> None:
        legacy = SourceFact(LEGACY_AMOUNT, "5", "demo.legacy.nominee")
        result = run(
            _context(
                sources=[legacy, _report_source(), _allocation_source()],
                inputs=_inputs(legacy="5"),
            ),
            self.schemas,
        )

        line_rows = [
            row
            for row in result.dispositions
            if row["artifact_id"] == "tax.us.2025.rule.form1040-line2b"
        ]
        self.assertEqual(len(line_rows), 1)
        self.assertEqual(line_rows[0]["disposition"], "blocked")
        self.assertEqual(line_rows[0]["code"], "DEPENDENCY_INVALID")
        self.assertEqual(
            line_rows[0]["missing"], ["legacy-and-derived-nominee-both-present"]
        )
        self.assertEqual(_findings(result, "tax.us.2025.interest.taxable-total"), [])
        self.assertEqual(len(_findings(result, DERIVED_NOMINEE_SYMBOL)), 1)

    def test_inactive_path_dependency_does_not_gate_selected_legacy_path(self) -> None:
        rules = _rules()
        line = rules[-1]
        new_path = next(
            path for path in line["selection"]["paths"] if path["id"] == "new"
        )
        new_path["requires"].append("demo.never-present-inactive-path")
        legacy = SourceFact(LEGACY_AMOUNT, "5", "demo.legacy.nominee")

        result = run(
            _context(
                sources=[legacy], inputs=_inputs(legacy="5"), rules=rules
            ),
            self.schemas,
        )

        total = _findings(result, "tax.us.2025.interest.taxable-total")
        self.assertEqual(len(total), 1)
        self.assertEqual(total[0]["value"], "495")
        self.assertNotIn(
            "demo.never-present-inactive-path",
            [missing for row in result.blocked for missing in row["missing"]],
        )

    def test_selected_expression_is_the_expression_evaluated(self) -> None:
        rules = _rules()
        line = rules[-1]
        legacy_path = next(
            path for path in line["selection"]["paths"] if path["id"] == "legacy"
        )
        legacy_path["value"] = {"op": "ref", "name": BASE_SYMBOLS[0]}
        legacy = SourceFact(LEGACY_AMOUNT, "5", "demo.legacy.nominee")

        result = run(
            _context(
                sources=[legacy], inputs=_inputs(legacy="5"), rules=rules
            ),
            self.schemas,
        )

        total = _findings(result, "tax.us.2025.interest.taxable-total")
        self.assertEqual(len(total), 1)
        self.assertEqual(
            total[0]["value"],
            "100",
            "a runtime-rewritten selected expression must be observable",
        )

    def test_malformed_aggregate_identity_blocks_under_aggregate_rule(self) -> None:
        rules = _rules()
        aggregate = rules[1]
        aggregate["aggregation"]["source_symbol_prefix"] = "demo.wrong-prefix|"

        result = run(_context(sources=[], rules=rules), self.schemas)

        rows = [
            row
            for row in result.dispositions
            if row["artifact_id"] == NOMINEE_AGGREGATE_RULE_ID
        ]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "blocked")
        self.assertEqual(rows[0]["code"], "DEPENDENCY_INVALID")
        self.assertEqual(rows[0]["missing"], ["nominee-aggregate-contract-invalid"])

    def test_top_level_declarations_are_neutral_and_runtime_rejects_mutations(self) -> None:
        mutations = ("when", "requires", "pins")
        for rule_index in (1, 2):
            for mutation in mutations:
                with self.subTest(rule_index=rule_index, mutation=mutation):
                    rules = _rules()
                    rule = rules[rule_index]
                    if mutation == "when":
                        rule["when"] = False
                    elif mutation == "requires":
                        rule["requires"] = ["demo.ghost-top-level-requirement"]
                    else:
                        rule["pins"] = [{
                            "role": "input",
                            "id": "demo.ghost-top-level-pin",
                            "version": "v1",
                            "origin": "assertion",
                        }]

                    runtime = run(
                        _context(sources=[], rules=rules), self.schemas
                    )
                    rows = [
                        row for row in runtime.dispositions
                        if row["artifact_id"] == rule["id"]
                    ]
                    self.assertEqual(len(rows), 1)
                    self.assertEqual(rows[0]["disposition"], "blocked")
                    self.assertEqual(rows[0]["code"], "DEPENDENCY_INVALID")
                    self.assertEqual(
                        rows[0]["missing"],
                        ["declarative-top-level-contract-invalid"],
                    )

                    package_result = _validate_candidate(rule)
                    self.assertIn(
                        "RULE_DECLARATIVE_TOP_LEVEL_INVALID",
                        {issue.code for issue in package_result.issues},
                    )

    def test_duplicate_selection_path_ids_fail_before_runtime(self) -> None:
        rules = _rules()
        line = rules[-1]
        line["selection"]["paths"][1]["id"] = line["selection"]["paths"][0]["id"]

        runtime = run(_context(sources=[], rules=rules), self.schemas)
        rows = [
            row for row in runtime.dispositions
            if row["artifact_id"] == line["id"]
        ]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "blocked")
        self.assertEqual(rows[0]["missing"], ["selection-path-id-duplicate"])

        package_result = _validate_candidate(line)
        self.assertIn(
            "RULE_SELECTION_PATH_IDS_NOT_UNIQUE",
            {issue.code for issue in package_result.issues},
        )

    def test_path_guard_refs_are_declared_and_guard_is_evaluated(self) -> None:
        rules = _rules()
        line = rules[-1]
        legacy_path = next(
            path for path in line["selection"]["paths"] if path["id"] == "legacy"
        )
        legacy_path["when"] = {
            "op": "ref",
            "name": "demo.undeclared-selection-guard",
        }

        package_result = _validate_candidate(line)
        self.assertIn(
            "RULE_SELECTION_EXPRESSION_INVALID",
            {issue.code for issue in package_result.issues},
        )

        # The same declaration rule applies to the neither/default branch and
        # to source-set nodes that are not representable by this bounded
        # requires/pins surface.
        default_candidate = _load(LINE2B)
        default_candidate["selection"]["default"]["when"] = {
            "op": "ref",
            "name": "demo.undeclared-default-guard",
        }
        default_result = _validate_candidate(default_candidate)
        self.assertIn(
            "RULE_SELECTION_EXPRESSION_INVALID",
            {issue.code for issue in default_result.issues},
        )

        dynamic_candidate = _load(LINE2B)
        dynamic_path = next(
            path
            for path in dynamic_candidate["selection"]["paths"]
            if path["id"] == "legacy"
        )
        dynamic_path["when"] = {
            "op": "count",
            "name": "demo.dynamic-source",
            "source_set": "demo.dynamic-family",
        }
        dynamic_result = _validate_candidate(dynamic_candidate)
        self.assertIn(
            "RULE_SELECTION_DYNAMIC_DEPENDENCY_INVALID",
            {issue.code for issue in dynamic_result.issues},
        )

        # A declared existing dependency is evaluated, rather than ignored.
        rules = _rules()
        line = rules[-1]
        legacy_path = next(
            path for path in line["selection"]["paths"] if path["id"] == "legacy"
        )
        legacy_path["when"] = {
            "op": "compare",
            "left": {"op": "ref", "name": BASE_SYMBOLS[0]},
            "right": 1,
            "cmp": "gt",
        }
        legacy = SourceFact(LEGACY_AMOUNT, "5", "demo.legacy.nominee")
        inputs = _inputs(legacy="5")
        inputs[0] = InputFinding(BASE_SYMBOLS[0], "0", "demo.input.guard-zero", "input")
        runtime = run(
            _context(sources=[legacy], inputs=inputs, rules=rules), self.schemas
        )
        line_rows = [
            row for row in runtime.dispositions
            if row["artifact_id"] == line["id"]
        ]
        self.assertEqual(len(line_rows), 1)
        self.assertEqual(line_rows[0]["disposition"], "inapplicable")
        self.assertEqual(_findings(runtime, "tax.us.2025.interest.taxable-total"), [])

    def test_both_present_refusal_pins_current_causes_only(self) -> None:
        legacy = SourceFact(LEGACY_AMOUNT, "5", "demo.legacy.nominee")
        both = run(
            _context(
                sources=[legacy, _report_source(), _allocation_source()],
                inputs=_inputs(legacy="5"),
            ),
            self.schemas,
        )
        line_row = next(
            row for row in both.dispositions
            if row["artifact_id"] == "tax.us.2025.rule.form1040-line2b"
        )
        input_pin_ids = {
            pin["id"] for pin in line_row["pins"] if pin["role"] == "input"
        }
        reduction_ids = {
            pub.finding["id"]
            for pub in both.publications
            if pub.finding["symbol"].startswith(PUBLISHES + "|")
        }
        self.assertEqual(line_row["disposition"], "blocked")
        self.assertIn("demo.legacy.nominee", input_pin_ids)
        self.assertTrue(reduction_ids & input_pin_ids)

        # The current projection after legacy retraction has no stale legacy
        # cause and therefore selects the new path rather than refusing.
        new_only = run(
            _context(sources=[_report_source(), _allocation_source()]), self.schemas
        )
        new_line = next(
            row for row in new_only.dispositions
            if row["artifact_id"] == "tax.us.2025.rule.form1040-line2b"
        )
        self.assertEqual(new_line["disposition"], "published")
        self.assertNotIn("demo.legacy.nominee", {
            pin["id"] for pin in new_line["pins"] if pin["role"] == "input"
        })

        # The current projection after reduction retraction has no new cause
        # and remains compatible with the legacy path.
        legacy_only = run(
            _context(sources=[legacy], inputs=_inputs(legacy="5")), self.schemas
        )
        legacy_line = next(
            row for row in legacy_only.dispositions
            if row["artifact_id"] == "tax.us.2025.rule.form1040-line2b"
        )
        self.assertEqual(legacy_line["disposition"], "published")
        self.assertFalse(
            any(
                pub.finding["symbol"].startswith(PUBLISHES + "|")
                for pub in legacy_only.publications
            )
        )

    def test_path_pin_version_origin_and_identity_are_admission_contracts(self) -> None:
        mutations = ("version", "origin", "id")
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                line = _load(LINE2B)
                legacy_path = next(
                    path for path in line["selection"]["paths"]
                    if path["id"] == "legacy"
                )
                if mutation == "version":
                    legacy_path["pins"][0]["version"] = "v999"
                elif mutation == "origin":
                    legacy_path["pins"][0]["origin"] = "declared_default"
                else:
                    legacy_path["pins"][0]["id"] = "demo.unbound-input"
                package_result = _validate_candidate(line)
                self.assertIn(
                    "RULE_SELECTION_PINS_INVALID",
                    {issue.code for issue in package_result.issues},
                )

        line = _load(LINE2B)
        line["selection"]["default"]["pins"][0]["origin"] = "declared_default"
        package_result = _validate_candidate(line)
        self.assertIn(
            "RULE_SELECTION_DEFAULT_INVALID",
            {issue.code for issue in package_result.issues},
        )

        rules = _rules()
        rules[-1]["selection"]["paths"][0]["pins"][0]["version"] = "v999"
        runtime = run(
            _context(
                sources=[SourceFact(LEGACY_AMOUNT, "5", "demo.legacy.nominee")],
                inputs=_inputs(legacy="5"),
                rules=rules,
            ),
            self.schemas,
        )
        line_rows = [
            row for row in runtime.dispositions
            if row["artifact_id"] == "tax.us.2025.rule.form1040-line2b"
        ]
        self.assertEqual(len(line_rows), 1)
        self.assertEqual(line_rows[0]["disposition"], "blocked")
        self.assertEqual(
            line_rows[0]["missing"], ["selection-path-pin-contract-invalid"]
        )


class BoundedNomineeContractValidation(unittest.TestCase):
    """I0/I1/I7/I8 contract artifacts and negative package controls."""

    def setUp(self) -> None:
        self.schemas = DerivationSchemas()
        self.package = _load(DERIVATION_PACKAGE)
        self.line = _load(LINE2B)
        self.aggregate = _load(AGGREGATE)

    def _result(
        self,
        package: dict[str, Any] | None = None,
        corpus: dict[tuple[str, str], dict[str, Any]] | None = None,
    ) -> Any:
        return validate_package(
            self.package if package is None else package,
            _content_corpus() if corpus is None else corpus,
            self.schemas,
        )

    def test_positive_schemas_manifest_package_and_corpus_validate(self) -> None:
        self.schemas.validate_declared(self.line)
        self.schemas.validate_declared(self.aggregate)
        self.schemas.validate_declared(self.package)
        self.assertEqual(
            package_instance_checksum(self.package), self.package["package_checksum"]
        )
        result = self._result()
        self.assertTrue(result.ok, result.issues)

        manifest = json.loads(
            (DERIVATION_SCHEMA_DIR / "published.json").read_text("utf-8")
        )
        self.assertEqual(
            manifest["artifact-package.v29.schema.json"],
            "840d306a55ba66574f51134b54200c3cc3bbb5bd914553f1380850f51def6b8a",
        )
        self.assertEqual(
            manifest["rule-artifact.v8.schema.json"],
            "67c3e075d1d0f806dfabcb2dd7afde1603e70d6fc87a55c128b1aeecdd5bba17",
        )
        self.assertIn("artifact-package.v30.schema.json", manifest)
        self.assertIn("rule-artifact.v9.schema.json", manifest)

    def test_predecessor_schemas_reject_the_additive_v9_shapes(self) -> None:
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate("rule-artifact.v8", self.line)
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate("artifact-package.v29", self.package)

    def test_missing_aggregate_producer_is_rejected(self) -> None:
        package = copy.deepcopy(self.package)
        package["members"] = [
            member
            for member in package["members"]
            if member["id"] != self.aggregate["id"]
        ]
        package["package_checksum"] = package_instance_checksum(package)

        result = self._result(package=package)
        codes = {issue.code for issue in result.issues}
        self.assertIn("NOMINEE_AGGREGATE_PRODUCER_MISSING", codes)

    def test_aggregate_requires_exact_source_and_fact_surface(self) -> None:
        package = copy.deepcopy(self.package)
        corpus = _content_corpus()
        aggregate = copy.deepcopy(self.aggregate)
        aggregate["aggregation"]["source_fact_type"]["id"] = "demo.undeclared.nominee-fact"
        corpus[(aggregate["id"], aggregate["version"])] = aggregate

        result = self._result(package=package, corpus=corpus)
        codes = {issue.code for issue in result.issues}
        self.assertIn("NOMINEE_AGGREGATION_SOURCE_INVALID", codes)
        self.assertIn("NOMINEE_AGGREGATION_FACT_TYPE_ABSENT", codes)

    def test_unreachable_aggregate_is_rejected_by_closed_package_graph(self) -> None:
        package = copy.deepcopy(self.package)
        corpus = _content_corpus()
        line = copy.deepcopy(self.line)
        new_path = next(
            path for path in line["selection"]["paths"] if path["id"] == "new"
        )
        new_path["requires"].remove(DERIVED_NOMINEE_SYMBOL)
        new_path["value"] = {"op": "ref", "name": BASE_SYMBOLS[0]}
        corpus[(line["id"], line["version"])] = line

        result = self._result(package=package, corpus=corpus)
        codes = {issue.code for issue in result.issues}
        self.assertIn("RULE_SELECTION_DEPENDENCIES_INVALID", codes)
        self.assertIn("MEMBER_UNREACHABLE", codes)

    def test_copied_selection_syntax_has_no_runtime_or_package_authority(self) -> None:
        copied = copy.deepcopy(self.line)
        copied["id"] = "demo.rule.copied-selection"
        package = copy.deepcopy(self.package)
        for member in package["members"]:
            if member["id"] == self.line["id"]:
                member["id"] = copied["id"]
        package["entrypoints"] = [{"id": copied["id"], "version": copied["version"]}]
        package["package_checksum"] = package_instance_checksum(package)
        corpus = _content_corpus()
        corpus[(copied["id"], copied["version"])] = copied

        result = self._result(package=package, corpus=corpus)
        self.assertIn(
            "RULE_SELECTION_UNAUTHORIZED", {issue.code for issue in result.issues}
        )

        rules = _rules()
        rules[-1] = copied
        runtime = run(_context(sources=[], rules=rules), self.schemas)
        rows = [
            row for row in runtime.dispositions if row["artifact_id"] == copied["id"]
        ]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "blocked")
        self.assertEqual(rows[0]["code"], "DEPENDENCY_INVALID")
        self.assertEqual(rows[0]["missing"], ["v9-declarative-binding-unauthorized"])

    def test_authorization_closure_reaches_declared_family_bundles_and_producers(self) -> None:
        package = self.package
        closure = rule_scoped_closure(
            {self.line["id"]}, _id_corpus(), package=package
        )
        ids = {citizen_id for citizen_id, _version in closure}
        self.assertIn(self.line["id"], ids)
        self.assertIn(self.aggregate["id"], ids)
        self.assertIn(RULE_ID, ids)
        self.assertIn("tax.us.2025.scheduleb.adjustment.nominee", ids)
        self.assertIn("tax.us.2025.scheduleb.adjustment.nominee.vocabulary", ids)
        self.assertIn("tax.us.2025.interest.nominee-reduction.vocabulary", ids)
        self.assertIn("tax.us.nominee-allocation.vocabulary", ids)


if __name__ == "__main__":
    unittest.main()
