"""ADR-0066 Track 2: the causal runtime path — current-member evaluation,
schema-validated member/family publication, cross-family identity
exclusivity, and the compiled prerequisite's load-bearing effect on
attachment scheduling. Constructs `RunContext` directly and drives it
through the real `run()` evaluator/schema boundary, the same pattern every
other runtime-level test in this suite uses (e.g. `test_dsbs_t2_schedule_b`'s
`WholeFormValueContent`).
"""

import copy
import json
import unittest
from pathlib import Path
from typing import Any, cast

from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import compile_validation_graph
from packages.derivation.runner import InputFinding, RunContext, SourceFact, run
from packages.derivation.source_authority import ClosureFindingRecord

SAMPLE_DIR = Path(__file__).resolve().parent.parent.parent / "packages" / "sample_data" / "declarative_validation_contract"

FAMILY_A_ID = "declarativevalidation.demo-family"
FAMILY_B_ID = "declarativevalidation.demo-family-b"
FAMILY_A_MEMBER_TYPE = "declarativevalidation.demo-family.member"
FAMILY_B_MEMBER_TYPE = "declarativevalidation.demo-family-b.member"
FAMILY_A_SYMBOL = f"{FAMILY_A_ID}.member-validation"


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((SAMPLE_DIR / name).read_text("utf-8")))


def _mapping(family: dict[str, Any], horizon_key: str) -> dict[str, Any]:
    return {
        "schema": "source-closure-mapping.v2",
        "id": f"{family['id']}.mapping",
        "version": "v1",
        "family": {"id": family["id"], "version": family["version"]},
        "member_fact_type": family["member_predicate"]["fact_type"],
        "closure_fact_type": f"{family['id']}.closure",
        "closure_horizon_key": horizon_key,
        "admits_symbol": family["authorizes_subtotal"],
    }


class DeclarativeValidationRuntimeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schemas = DerivationSchemas()

    def setUp(self) -> None:
        self.family_a = _load("source-family.declarativevalidation.demo-family.v1.json")
        self.family_b = _load("source-family.declarativevalidation.demo-family-b.v1.json")
        self.mapping_a = _mapping(self.family_a, "h")
        self.mapping_b = _mapping(self.family_b, "h")
        self.adoption_pin = {"role": "adoption", "id": "package.declarativevalidation", "version": "v1"}

        producers = compile_validation_graph(
            [], {self.family_a["id"]: self.family_a, self.family_b["id"]: self.family_b},
            {self.family_a["authorizes_subtotal"]: self.family_a["id"],
             self.family_b["authorizes_subtotal"]: self.family_b["id"]},
            self.schemas,
        )
        self.producer_rules = producers
        self.assertEqual([p["id"] for p in producers], [f"{FAMILY_A_ID}.member-validation.synthesized"])

    def _ctx(
        self,
        *,
        sources: list[SourceFact],
        rules: list[dict[str, Any]] | None = None,
        family_admitted: bool = True,
        family_b_admitted: bool = True,
        inputs: list[InputFinding] | None = None,
        parameters: dict[str, dict[str, Any]] | None = None,
    ) -> RunContext:
        closure_findings = []
        current_horizons = {}
        if family_admitted:
            closure_findings.append(ClosureFindingRecord("demo.closure.a", f"{FAMILY_A_ID}.closure", "h", True))
            current_horizons[FAMILY_A_ID] = "h"
        if family_b_admitted:
            closure_findings.append(ClosureFindingRecord("demo.closure.b", f"{FAMILY_B_ID}.closure", "h", True))
            current_horizons[FAMILY_B_ID] = "h"
        return RunContext(
            run_id="demo.declarative-validation.runtime",
            rules=list(rules if rules is not None else self.producer_rules),
            parameters=parameters or {},
            canon={},
            inputs=inputs or [],
            sources=sources,
            adoption_pin=self.adoption_pin,
            governance_pins=[],
            family_declarations=[self.family_a, self.family_b],
            closure_mappings=[self.mapping_a, self.mapping_b],
            closure_findings=closure_findings,
            current_horizons=current_horizons,
        )

    def _member_finding(self, result: Any, fact_id: str) -> dict[str, Any]:
        matches = [p.finding for p in result.publications if p.finding["symbol"].endswith(f".{fact_id}")]
        self.assertEqual(len(matches), 1, matches)
        return matches[0]

    # -- member constraints: valid / invalid / masking -----------------

    def test_single_valid_member_publishes_member_and_family_success(self) -> None:
        source = SourceFact(
            FAMILY_A_MEMBER_TYPE, json.dumps({"some_field": "x", "external_ref": "ref-a"}), "demo.f1",
            fact_id="demo.f1|taxpayer=alice",
        )
        ctx = self._ctx(sources=[source])
        result = run(ctx, self.schemas)

        self.assertEqual(result.blocked, [])
        member = self._member_finding(result, "demo.f1|taxpayer=alice")
        self.assertEqual(member["value"]["violations"], [])
        self.assertEqual(member["value"]["member_fact_id"], "demo.f1|taxpayer=alice")
        family_pub = [p for p in result.publications if p.finding["symbol"] == FAMILY_A_SYMBOL]
        self.assertEqual(len(family_pub), 1)

    def test_invalid_member_blocks_family_and_names_constraint(self) -> None:
        source = SourceFact(FAMILY_A_MEMBER_TYPE, json.dumps({}), "demo.f1", fact_id="demo.f1|taxpayer=alice")
        ctx = self._ctx(sources=[source])
        result = run(ctx, self.schemas)

        self.assertEqual(len(result.blocked), 1)
        self.assertEqual(result.blocked[0]["code"], "FAMILY_VALIDATION_BLOCKED")
        self.assertIn("MISSING_ATTACHMENT", result.blocked[0]["missing"])
        member = self._member_finding(result, "demo.f1|taxpayer=alice")
        self.assertEqual(
            member["value"]["violations"],
            [{"constraint_id": "c1", "block_code": "MISSING_ATTACHMENT", "meaning": "Attachment missing"}],
        )
        self.assertFalse(any(p.finding["symbol"] == FAMILY_A_SYMBOL for p in result.publications))

    def test_two_members_one_invalid_is_not_maskable(self) -> None:
        valid = SourceFact(FAMILY_A_MEMBER_TYPE, json.dumps({"some_field": "x"}), "demo.f1", fact_id="demo.f1|taxpayer=alice")
        invalid = SourceFact(FAMILY_A_MEMBER_TYPE, json.dumps({}), "demo.f2", fact_id="demo.f2|taxpayer=bob")
        ctx = self._ctx(sources=[valid, invalid])
        result = run(ctx, self.schemas)

        self.assertEqual(len(result.blocked), 1)
        self.assertIn("MISSING_ATTACHMENT", result.blocked[0]["missing"])
        good = self._member_finding(result, "demo.f1|taxpayer=alice")
        bad = self._member_finding(result, "demo.f2|taxpayer=bob")
        self.assertEqual(good["value"]["violations"], [])
        self.assertNotEqual(bad["value"]["violations"], [])
        self.assertFalse(any(p.finding["symbol"] == FAMILY_A_SYMBOL for p in result.publications))

    # -- result identity: change and restore ---------------------------

    def test_member_result_identity_changes_and_restores(self) -> None:
        source_v1 = SourceFact(FAMILY_A_MEMBER_TYPE, json.dumps({"some_field": "x"}), "demo.f1", fact_id="demo.f1|taxpayer=alice")
        result_1 = run(self._ctx(sources=[source_v1]), self.schemas)
        id_1 = self._member_finding(result_1, "demo.f1|taxpayer=alice")["id"]

        source_v2 = SourceFact(FAMILY_A_MEMBER_TYPE, json.dumps({"some_field": "y"}), "demo.f1.v2", fact_id="demo.f1|taxpayer=alice")
        result_2 = run(self._ctx(sources=[source_v2]), self.schemas)
        id_2 = self._member_finding(result_2, "demo.f1|taxpayer=alice")["id"]
        self.assertNotEqual(id_1, id_2)

        result_restored = run(self._ctx(sources=[source_v1]), self.schemas)
        id_restored = self._member_finding(result_restored, "demo.f1|taxpayer=alice")["id"]
        self.assertEqual(id_1, id_restored)

    # -- closure / horizon: unclosed vs closed-empty --------------------

    def test_unclosed_family_blocks_absent(self) -> None:
        ctx = self._ctx(sources=[], family_admitted=False)
        result = run(ctx, self.schemas)
        self.assertEqual(len(result.blocked), 1)
        from packages.derivation.evaluator import BLOCK_ABSENT
        self.assertEqual(result.blocked[0]["code"], BLOCK_ABSENT)
        self.assertFalse(any(p.finding["symbol"] == FAMILY_A_SYMBOL for p in result.publications))

    def test_closed_empty_family_publishes_success(self) -> None:
        ctx = self._ctx(sources=[])
        result = run(ctx, self.schemas)
        self.assertEqual(result.blocked, [])
        self.assertTrue(any(p.finding["symbol"] == FAMILY_A_SYMBOL for p in result.publications))

    # -- malformed member JSON: fail closed, never an untyped exception -

    def test_malformed_member_json_fails_closed(self) -> None:
        source = SourceFact(FAMILY_A_MEMBER_TYPE, "{not-json", "demo.f1", fact_id="demo.f1|taxpayer=alice")
        ctx = self._ctx(sources=[source])
        result = run(ctx, self.schemas)  # must not raise
        self.assertEqual(len(result.blocked), 1)
        self.assertIn("MEMBER_VALUE_MALFORMED", result.blocked[0]["missing"])

    # -- constraint evaluation failure: block, never a crashed run -----

    def _family_with_crash_constraint(self) -> dict[str, Any]:
        """`self.family_a` plus a `compare` constraint over an `amount`
        field with no declared `default` — reachable-in-principle inputs for
        that field raise inside `Evaluator` rather than producing a block,
        unless the call site guards for it (Track 4 Repair 2, defect 2)."""
        family = copy.deepcopy(self.family_a)
        family["member_constraints"].append({
            "id": "c2-crash",
            "block_code": "AMOUNT_NOT_POSITIVE",
            "meaning": "amount must be positive",
            "violated_when": {
                "op": "compare",
                "comparison": "gt",
                "left": {"op": "field", "field": "amount"},
                "right": {"op": "literal", "arg": 0},
            },
        })
        return family

    def _assert_single_constraint_evaluation_failure(self, result: Any, fact_id: str) -> None:
        member = self._member_finding(result, fact_id)
        violations = member["value"]["violations"]
        self.assertEqual(len(violations), 1, violations)
        violation = violations[0]
        self.assertEqual(violation["constraint_id"], "CONSTRAINT_EVALUATION_FAILED")
        self.assertEqual(violation["block_code"], "CONSTRAINT_EVALUATION_FAILED")
        self.assertIn("CONSTRAINT_EVALUATION_FAILED", result.blocked[0]["missing"])

    def test_absent_field_without_default_blocks_not_raises(self) -> None:
        self.family_a = self._family_with_crash_constraint()
        source = SourceFact(
            FAMILY_A_MEMBER_TYPE, json.dumps({"some_field": "x"}), "demo.f1",
            fact_id="demo.f1|taxpayer=alice",
        )
        result = run(self._ctx(sources=[source]), self.schemas)  # must not raise
        self._assert_single_constraint_evaluation_failure(result, "demo.f1|taxpayer=alice")

    def test_non_numeric_string_field_blocks_not_raises(self) -> None:
        self.family_a = self._family_with_crash_constraint()
        source = SourceFact(
            FAMILY_A_MEMBER_TYPE, json.dumps({"some_field": "x", "amount": "not-a-number"}), "demo.f1",
            fact_id="demo.f1|taxpayer=alice",
        )
        result = run(self._ctx(sources=[source]), self.schemas)  # must not raise
        self._assert_single_constraint_evaluation_failure(result, "demo.f1|taxpayer=alice")

    def test_deeply_nested_term_blocks_not_raises(self) -> None:
        # MemberConstraintTooDeep reachability finding (defect 2 follow-up):
        # `package_validation._predicate_depth` only walks predicate `args`
        # (`all`/`any` nesting) — it does not recurse into a `compare`
        # predicate's `left`/`right` *term* tree, so an `add`/`subtract`
        # chain nested past MAX_PREDICATE_DEPTH under a `compare` passes
        # content validation undetected and only raises at evaluation time.
        # Not foreclosed by content validation; must be guarded here too.
        def deep_term(n: int) -> dict[str, Any]:
            if n == 0:
                return {"op": "field", "field": "amount"}
            return {"op": "add", "left": deep_term(n - 1), "right": {"op": "literal", "arg": 0}}

        family = copy.deepcopy(self.family_a)
        family["member_constraints"].append({
            "id": "c3-too-deep",
            "block_code": "AMOUNT_NOT_POSITIVE",
            "meaning": "amount must be positive",
            "violated_when": {
                "op": "compare", "comparison": "gt",
                "left": deep_term(8), "right": {"op": "literal", "arg": 0},
            },
        })
        self.family_a = family
        source = SourceFact(
            FAMILY_A_MEMBER_TYPE, json.dumps({"some_field": "x", "amount": 5}), "demo.f1",
            fact_id="demo.f1|taxpayer=alice",
        )
        result = run(self._ctx(sources=[source]), self.schemas)  # must not raise
        self._assert_single_constraint_evaluation_failure(result, "demo.f1|taxpayer=alice")

    def test_json_null_field_blocks_not_raises(self) -> None:
        self.family_a = self._family_with_crash_constraint()
        source = SourceFact(
            FAMILY_A_MEMBER_TYPE, json.dumps({"some_field": "x", "amount": None}), "demo.f1",
            fact_id="demo.f1|taxpayer=alice",
        )
        result = run(self._ctx(sources=[source]), self.schemas)  # must not raise
        self._assert_single_constraint_evaluation_failure(result, "demo.f1|taxpayer=alice")

    # -- cross-family identity exclusivity ------------------------------

    def test_cross_family_identities_unique_publishes_success(self) -> None:
        a = SourceFact(FAMILY_A_MEMBER_TYPE, json.dumps({"some_field": "x", "external_ref": "ref-a"}), "demo.f1", fact_id="demo.f1|taxpayer=alice")
        b = SourceFact(FAMILY_B_MEMBER_TYPE, json.dumps({"external_ref": "ref-b"}), "demo.g1", fact_id="demo.g1|taxpayer=bob")
        result = run(self._ctx(sources=[a, b]), self.schemas)
        self.assertEqual(result.blocked, [])
        self.assertTrue(any(p.finding["symbol"] == FAMILY_A_SYMBOL for p in result.publications))

    def test_cross_family_identity_collision_blocks(self) -> None:
        a = SourceFact(FAMILY_A_MEMBER_TYPE, json.dumps({"some_field": "x", "external_ref": "same-ref"}), "demo.f1", fact_id="demo.f1|taxpayer=same")
        b = SourceFact(FAMILY_B_MEMBER_TYPE, json.dumps({"external_ref": "same-ref"}), "demo.g1", fact_id="demo.g1|taxpayer=same")
        result = run(self._ctx(sources=[a, b]), self.schemas)
        self.assertEqual(len(result.blocked), 1)
        self.assertIn("IDENTITY_EXCLUSIVITY_COLLISION", result.blocked[0]["missing"])
        self.assertFalse(any(p.finding["symbol"] == FAMILY_A_SYMBOL for p in result.publications))

    def test_cross_family_identity_collision_clears_on_removal(self) -> None:
        a = SourceFact(FAMILY_A_MEMBER_TYPE, json.dumps({"some_field": "x", "external_ref": "same-ref"}), "demo.f1", fact_id="demo.f1|taxpayer=same")
        b = SourceFact(FAMILY_B_MEMBER_TYPE, json.dumps({"external_ref": "same-ref"}), "demo.g1", fact_id="demo.g1|taxpayer=same")
        blocked_result = run(self._ctx(sources=[a, b]), self.schemas)
        self.assertEqual(len(blocked_result.blocked), 1)

        # Recompute from current members only: removing the colliding
        # member (never an accumulated history) clears the collision.
        cleared_result = run(self._ctx(sources=[a]), self.schemas)
        self.assertEqual(cleared_result.blocked, [])
        self.assertTrue(any(p.finding["symbol"] == FAMILY_A_SYMBOL for p in cleared_result.publications))

    def test_cross_family_missing_component_fails_closed(self) -> None:
        # No `external_ref` member field at all - the declared `member_field`
        # component cannot be extracted.
        a = SourceFact(FAMILY_A_MEMBER_TYPE, json.dumps({"some_field": "x"}), "demo.f1", fact_id="demo.f1|taxpayer=alice")
        result = run(self._ctx(sources=[a]), self.schemas)
        self.assertEqual(len(result.blocked), 1)
        self.assertIn("IDENTITY_COMPONENT_MISSING", result.blocked[0]["missing"])

    def test_cross_family_incompatible_family_absent_fails_closed(self) -> None:
        family_a_orphan = copy.deepcopy(self.family_a)
        a = SourceFact(FAMILY_A_MEMBER_TYPE, json.dumps({"some_field": "x", "external_ref": "ref-a"}), "demo.f1", fact_id="demo.f1|taxpayer=alice")
        ctx = RunContext(
            run_id="demo.declarative-validation.runtime.orphan",
            rules=list(compile_validation_graph(
                [], {family_a_orphan["id"]: family_a_orphan}, {family_a_orphan["authorizes_subtotal"]: family_a_orphan["id"]}, self.schemas,
            )),
            parameters={}, canon={}, inputs=[], sources=[a],
            adoption_pin=self.adoption_pin, governance_pins=[],
            family_declarations=[family_a_orphan],  # family B never declared
            closure_mappings=[self.mapping_a],
            closure_findings=[ClosureFindingRecord("demo.closure.a", f"{FAMILY_A_ID}.closure", "h", True)],
            current_horizons={FAMILY_A_ID: "h"},
        )
        result = run(ctx, self.schemas)
        self.assertEqual(len(result.blocked), 1)
        self.assertIn("IDENTITY_EXCLUSIVITY_FAMILY_ABSENT", result.blocked[0]["missing"])

    # -- attachment scheduling: the compiled prerequisite is load-bearing

    def test_attachment_blocks_until_family_validation_publishes(self) -> None:
        attachment = _load("attachment-rule.declarativevalidation.demo-attachment.v1.json")
        compiled_attachment = compile_validation_graph(
            [attachment],
            {self.family_a["id"]: self.family_a, self.family_b["id"]: self.family_b},
            {self.family_a["authorizes_subtotal"]: self.family_a["id"], self.family_b["authorizes_subtotal"]: self.family_b["id"]},
            self.schemas,
        )
        self.assertIn(FAMILY_A_SYMBOL, compiled_attachment[0].get("requires", []))
        rules = list(self.producer_rules) + compiled_attachment

        invalid_member = SourceFact(FAMILY_A_MEMBER_TYPE, json.dumps({}), "demo.f1", fact_id="demo.f1|taxpayer=alice")
        parameters = {"demo.param": {"values": 50}}
        inputs = [
            InputFinding("demo.subtotal", 100, "demo.subtotal.finding", "input"),
            InputFinding("demo.answer", "yes", "demo.answer.finding", "input"),
        ]
        blocked_ctx = self._ctx(sources=[invalid_member], rules=rules, inputs=inputs, parameters=parameters)
        blocked_result = run(blocked_ctx, self.schemas)
        self.assertFalse(any(p.finding["symbol"] == "demo.attachment" for p in blocked_result.publications))
        attachment_disposition = [d for d in blocked_result.dispositions if d["artifact_id"] == attachment["id"]][0]
        self.assertEqual(attachment_disposition["disposition"], "blocked")

        valid_member = SourceFact(
            FAMILY_A_MEMBER_TYPE, json.dumps({"some_field": "x", "external_ref": "ref-a"}), "demo.f1",
            fact_id="demo.f1|taxpayer=alice",
        )
        ok_ctx = self._ctx(sources=[valid_member], rules=rules, inputs=inputs, parameters=parameters)
        ok_result = run(ok_ctx, self.schemas)
        self.assertTrue(any(p.finding["symbol"] == "demo.attachment" for p in ok_result.publications))
        ok_attachment_disposition = [d for d in ok_result.dispositions if d["artifact_id"] == attachment["id"]][0]
        self.assertEqual(ok_attachment_disposition["disposition"], "published")


class AttachmentVersionDispatchTest(unittest.TestCase):
    """v8 must render the same inherited model as v6; v7/v99 stay unknown
    and fail loud rather than silently mis-dispatching through the generic
    rule path."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.schemas = DerivationSchemas()

    def _minimal_attachment(self, schema: str) -> dict[str, Any]:
        citizen = {
            "schema": schema,
            "id": "declarativevalidation.demo-version-attachment",
            "version": "v1",
            "title": "Demo",
            "scope": {"tax_year": 2025, "jurisdiction": "us", "family": "declarativevalidation.demo-family"},
            "attachment": {"authority": "IRS", "form_id": "1040", "jurisdiction": "us", "tax_year": 2025},
            "publishes": "demo.version-attachment",
            "requirement": {
                "subtotals": ["demo.subtotal"],
                "threshold_parameter": {"id": "demo.param", "version": "v1"},
                "comparison": "strictly_greater_than",
                "citation": {"id": "demo.citation", "version": "v1"},
            },
            "itemizations": [],
            "completeness": {"required_answers": []},
        }
        if schema == "attachment-rule.v8":
            citizen["accounts_for"] = []
        return citizen

    def _run_one(self, schema: str) -> Any:
        rule = self._minimal_attachment(schema)
        ctx = RunContext(
            run_id="demo.declarative-validation.version-dispatch",
            rules=[rule],
            parameters={"demo.param": {"values": 50}},
            canon={}, inputs=[InputFinding("demo.subtotal", 100, "demo.subtotal.finding", "input")],
            sources=[],
            adoption_pin={"role": "adoption", "id": "package.declarativevalidation", "version": "v1"},
            governance_pins=[],
        )
        return run(ctx, self.schemas)

    def test_v6_and_v8_render_the_same_inherited_model(self) -> None:
        v6_result = self._run_one("attachment-rule.v6")
        v8_result = self._run_one("attachment-rule.v8")
        v6_value = v6_result.publications[0].finding["value"]
        v8_value = v8_result.publications[0].finding["value"]
        self.assertEqual(v6_value, v8_value)

    def test_v7_is_unknown_and_fails_loud(self) -> None:
        with self.assertRaises(KeyError):
            self._run_one("attachment-rule.v7")

    def test_v99_is_unknown_and_fails_loud(self) -> None:
        with self.assertRaises(KeyError):
            self._run_one("attachment-rule.v99")


if __name__ == "__main__":
    unittest.main()
