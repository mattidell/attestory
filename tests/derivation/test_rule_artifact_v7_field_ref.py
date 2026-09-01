"""ADR-0067: rule-artifact.v7 field-ref access.

Load-time fail-closed validation (FIELD_REF_UNKNOWN_FIELD /
FIELD_REF_NOT_OBJECT) and runtime resolution of a `ref` node with `field`
to `finding.value[field]` off the currently bound finding.
"""

from __future__ import annotations

import json
import unittest
from typing import Any

from packages.derivation.evaluator import BLOCK_INVALID, EvalBlocked, evaluate, Environment, AccessLog
from packages.derivation.loader import DERIVATION_SCHEMA_DIR, DerivationSchemas
from packages.derivation.marshal import marshal_run_context
from packages.derivation.package_validation import (
    FIELD_REF_NOT_OBJECT,
    FIELD_REF_UNKNOWN_FIELD,
    check_field_ref_bindings,
)
from packages.derivation.runner import InputFinding, RunContext, run
from packages.kernel.currency import CurrencyView
from packages.kernel.schema_registry import SchemaRegistry, SchemaValidationError

EXAMPLES = DERIVATION_SCHEMA_DIR.parent.parent / "sample_data" / "derivation" / "examples"
ACQUISITION_TYPE = "tax.us.obligation-acquisition-circumstance"
HOSTILE_TYPE = "demo.tax.hostile-scalar-interest"
FIELD = "accrued_interest_paid_to_seller"

ADOPTION = {"role": "adoption", "id": "demo.package.field-ref", "version": "v1"}
GOVERNANCE = [{"role": "governance", "id": "governance.constitution", "version": "v1"}]


def _example() -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads(
        (EXAMPLES / "rule-artifact.v7.field-ref.json").read_text("utf-8")
    )
    return loaded


def _object_fact_type() -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": ACQUISITION_TYPE,
        "version": "v1",
        "title": "Synthetic bond purchase acquisition",
        "nature": "determinable",
        "identity_keys": [{"name": "tax-year", "kind": "literal", "values": ["2025"]}],
        "value_schema": {
            "type": "object",
            "properties": {
                "purchase_price": {"type": "number"},
                "accrued_interest_paid_to_seller": {"type": "number"},
            },
            "required": ["purchase_price", "accrued_interest_paid_to_seller"],
        },
        "supersession": {"policy": "free"},
    }


def _scalar_fact_type() -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": "demo.tax.scalar-interest",
        "version": "v1",
        "title": "Synthetic scalar interest amount",
        "nature": "determinable",
        "identity_keys": [{"name": "tax-year", "kind": "literal", "values": ["2025"]}],
        "value_schema": {"type": "number"},
        "supersession": {"policy": "free"},
    }


def _no_properties_fact_type() -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": "demo.tax.opaque-object",
        "version": "v1",
        "title": "Synthetic object fact type without properties",
        "nature": "determinable",
        "identity_keys": [{"name": "tax-year", "kind": "literal", "values": ["2025"]}],
        "value_schema": {"type": "object"},
        "supersession": {"policy": "free"},
    }


def _rule_with_field(field: str, *, name: str = ACQUISITION_TYPE) -> dict[str, Any]:
    rule = _example()
    rule["requires"] = [name]
    rule["value"] = {"op": "ref", "name": name, "field": field}
    rule["blocked"] = {"code": "DEPENDENCY_ABSENT", "missing": [name]}
    return rule


class _HorizonState:
    def __init__(self) -> None:
        self.current_by_chain: dict[tuple[str, str, str], str] = {}


class _State:
    def __init__(self, findings: dict[str, dict[str, Any]]) -> None:
        self.findings = findings
        self.horizon_state = _HorizonState()


def _finding(fid: str, fact_id: str, value: Any) -> dict[str, Any]:
    return {"id": fid, "fact_id": fact_id, "value": value, "basis": "attested"}


def _currency(finding_ids: list[str]) -> CurrencyView:
    ids = frozenset(finding_ids)
    return CurrencyView(
        current_finding_ids=ids,
        displaced_finding_ids=frozenset(),
        current_evidence_ids=frozenset(),
        displaced_evidence_ids=frozenset(),
    )


class RuleArtifactV7Schema(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = SchemaRegistry([DERIVATION_SCHEMA_DIR])

    def test_committed_example_validates(self) -> None:
        self.registry.validate_declared(_example())

    def test_v6_still_rejects_any_field_key(self) -> None:
        artifact = _example()
        artifact["schema"] = "rule-artifact.v6"
        with self.assertRaises(SchemaValidationError):
            self.registry.validate("rule-artifact.v6", artifact)

    def test_v7_accepts_correct_and_misspelled_field_at_schema_layer(self) -> None:
        for field in (FIELD, "accrued_interest_paid_to_seler"):
            with self.subTest(field=field):
                self.registry.validate("rule-artifact.v7", _rule_with_field(field))

    def test_v6_manifest_entry_unchanged_and_v7_published(self) -> None:
        manifest = json.loads((DERIVATION_SCHEMA_DIR / "published.json").read_text("utf-8"))
        self.assertIn("rule-artifact.v7.schema.json", manifest)
        self.assertIn("artifact-package.v26.schema.json", manifest)
        self.assertEqual(
            manifest["rule-artifact.v6.schema.json"],
            "bd4bded179146a6666e526bb3e1ada16b636bed20f94cbff86476bbe12dfe92f",
        )


class FieldRefLoadTime(unittest.TestCase):
    def test_correctly_spelled_field_is_accepted(self) -> None:
        issues = check_field_ref_bindings(
            _rule_with_field(FIELD),
            {_object_fact_type()["id"]: _object_fact_type()},
            {},
        )
        self.assertEqual(issues, [])

    def test_misspelled_field_fails_closed(self) -> None:
        issues = check_field_ref_bindings(
            _rule_with_field("accrued_interest_paid_to_seler"),
            {_object_fact_type()["id"]: _object_fact_type()},
            {},
        )
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].code, FIELD_REF_UNKNOWN_FIELD)
        self.assertIn("accrued_interest_paid_to_seler", issues[0].detail)

    def test_field_on_scalar_fact_type_is_category_error(self) -> None:
        scalar = _scalar_fact_type()
        issues = check_field_ref_bindings(
            _rule_with_field(FIELD, name=scalar["id"]),
            {scalar["id"]: scalar},
            {},
        )
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].code, FIELD_REF_NOT_OBJECT)

    def test_field_without_value_schema_properties_is_category_error(self) -> None:
        opaque = _no_properties_fact_type()
        issues = check_field_ref_bindings(
            _rule_with_field(FIELD, name=opaque["id"]),
            {opaque["id"]: opaque},
            {},
        )
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].code, FIELD_REF_NOT_OBJECT)


class FieldRefRuntime(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()

    def test_correctly_spelled_field_resolves_to_the_scalar(self) -> None:
        rule = _rule_with_field(FIELD)
        ctx = RunContext(
            run_id="demo.field-ref.run",
            rules=[rule],
            parameters={},
            canon={},
            inputs=[
                InputFinding(
                    ACQUISITION_TYPE,
                    {"purchase_price": 10000, "accrued_interest_paid_to_seller": 800},
                    "f.acq",
                    "input",
                )
            ],
            sources=[],
            adoption_pin=ADOPTION,
            governance_pins=GOVERNANCE,
        )
        result = run(ctx, self.schemas)
        published = {pub.finding["symbol"]: pub.finding["value"] for pub in result.publications}
        self.assertEqual(published[rule["publishes"]], "800")
        self.assertEqual(result.blocked, [])

    def test_field_flows_through_existing_scalar_arithmetic(self) -> None:
        rule = _rule_with_field(FIELD)
        rule["value"] = {
            "op": "add",
            "args": [
                {"op": "ref", "name": ACQUISITION_TYPE, "field": FIELD},
                0,
            ],
        }
        ctx = RunContext(
            run_id="demo.field-ref.arith",
            rules=[rule],
            parameters={},
            canon={},
            inputs=[
                InputFinding(
                    ACQUISITION_TYPE,
                    {"purchase_price": 10000, "accrued_interest_paid_to_seller": 800},
                    "f.acq",
                    "input",
                )
            ],
            sources=[],
            adoption_pin=ADOPTION,
            governance_pins=GOVERNANCE,
        )
        result = run(ctx, self.schemas)
        published = {pub.finding["symbol"]: pub.finding["value"] for pub in result.publications}
        self.assertEqual(published[rule["publishes"]], "800")

    def test_runtime_miss_fails_closed_not_none_or_zero(self) -> None:
        env = Environment(
            symbols={ACQUISITION_TYPE: {"purchase_price": 10000, "accrued_interest_paid_to_seller": 800}},
            sources={},
            closed_sets=frozenset(),
            parameters={},
            canon={},
        )
        with self.assertRaises(EvalBlocked) as caught:
            evaluate(
                {"op": "ref", "name": ACQUISITION_TYPE, "field": "accrued_interest_paid_to_seler"},
                env,
                AccessLog(),
            )
        self.assertEqual(caught.exception.category, BLOCK_INVALID)
        self.assertNotIn(caught.exception.category, {None, 0, "0"})


class FieldRefMarshalGuards(unittest.TestCase):
    def _marshal(self, findings: dict[str, dict[str, Any]], rules: list[dict[str, Any]]) -> Any:
        state = _State(findings)
        return marshal_run_context(
            run_id="demo.field-ref.marshal",
            state=state,  # type: ignore[arg-type]
            currency=_currency(list(findings)),
            rules=rules,
            parameters={},
            canon={},
            adoption_pin=ADOPTION,
            governance_pins=[],
        )

    def test_disagreeing_acquisitions_leave_the_symbol_unbound(self) -> None:
        rule = _rule_with_field(FIELD)
        findings = {
            "f.acq1": _finding(
                "f.acq1",
                f"{ACQUISITION_TYPE}|ref=ACQ-1,tax-year=2025",
                {"purchase_price": 10000, "accrued_interest_paid_to_seller": 800},
            ),
            "f.acq2": _finding(
                "f.acq2",
                f"{ACQUISITION_TYPE}|ref=ACQ-2,tax-year=2025",
                {"purchase_price": 9000, "accrued_interest_paid_to_seller": 400},
            ),
        }
        ctx = self._marshal(findings, [rule])
        bound = {i.symbol: i.value for i in ctx.inputs}
        self.assertNotIn(ACQUISITION_TYPE, bound)

    def test_hostile_scalar_of_another_type_is_not_substituted(self) -> None:
        rule = _rule_with_field(FIELD)
        findings = {
            "f.acq": _finding(
                "f.acq",
                f"{ACQUISITION_TYPE}|ref=ACQ-1,tax-year=2025",
                {"purchase_price": 10000, "accrued_interest_paid_to_seller": 800},
            ),
            "f.hostile": _finding(
                "f.hostile",
                f"{HOSTILE_TYPE}|ref=H-1,tax-year=2025",
                50000,
            ),
        }
        ctx = self._marshal(findings, [rule])
        bound = {i.symbol: i.value for i in ctx.inputs}
        self.assertEqual(
            bound[ACQUISITION_TYPE],
            {"purchase_price": 10000, "accrued_interest_paid_to_seller": 800},
        )
        self.assertNotIn(HOSTILE_TYPE, bound)
        self.assertNotEqual(bound.get(ACQUISITION_TYPE), 50000)


if __name__ == "__main__":
    unittest.main()
