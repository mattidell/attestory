"""Synthetic fidelity probes for the bounded v12 calculation view."""
from __future__ import annotations

import unittest
from copy import deepcopy
from typing import Any, cast

from packages.derivation.presentation_projection import (
    PresentationModelError,
    _calculation_view,
    _validate_calculation_view,
)
from packages.kernel.facts import EntityLifecycle, KernelState
from packages.kernel.findings import FindingState


STMT = "demo.tax.reader.statement"
AMOUNT = "demo.tax.reader.amount"
COUNT = "demo.tax.reader.link-count"
SCOPE_COUNT = "demo.tax.reader.scope-count"
CONCLUSION = "demo.tax.reader.conclusion"
RESP = "demo.tax.reader.responsibility"
FACT_ID = f"{STMT}|lender=demo-lender,statement=demo-s1,tax-year=2025"


def _rule(rule_id: str, role: str, publishes: str) -> dict[str, Any]:
    return {"schema": "rule-artifact.v12", "id": rule_id, "version": "v1",
            "reader_role": role, "subject": {"id": STMT, "version": "v1"},
            "publishes": publishes}


class CalculationViewProjection(unittest.TestCase):
    def test_exact_key_joins_copy_labels_values_pins_and_rule_text(self) -> None:
        rules = [
            _rule("demo.rule.amount", "statement-amount", AMOUNT),
            _rule("demo.rule.count", "link-count", COUNT),
            _rule("demo.rule.scope", "statement-scope-disqualifier-count", SCOPE_COUNT),
            _rule("demo.rule.conclusion", "bare-statement-conclusion", CONCLUSION),
        ]
        rules[3]["requires"] = [COUNT, SCOPE_COUNT]
        rules[-1]["lineNote"] = "demo note from the conclusion rule"
        responsibility = _rule("demo.rule.responsibility", "responsibility", RESP)
        responsibility["requires"] = [CONCLUSION, AMOUNT]
        responsibility["wording"] = "No borrowing is currently linked to {statement}."
        rules.append(responsibility)
        parameter = {"schema": "parameter-declaration.v1", "id": "demo.param.assumed-zero", "version": "v1", "values": "0"}
        amount_id, count_id, scope_id, conclusion_id, resp_id = (
            f"demo.finding.{name}" for name in ("amount", "count", "scope", "conclusion", "responsibility")
        )
        source_id = "demo.source.box1"
        publications = {
            amount_id: {"id": amount_id, "symbol": f"{AMOUNT}|{FACT_ID}", "value": "120", "pins": [{"role": "input", "id": source_id, "version": "v1", "origin": "assertion"}, {"role": "parameter", "id": parameter["id"], "version": "v1"}, {"role": "input", "id": count_id, "version": "v1"}]},
            count_id: {"id": count_id, "symbol": f"{COUNT}|{FACT_ID}", "value": "0", "pins": [{"role": "input", "id": "demo.source.box1", "version": "v1"}]},
            scope_id: {"id": scope_id, "symbol": f"{SCOPE_COUNT}|{FACT_ID}", "value": "0", "pins": [{"role": "input", "id": "demo.source.box1", "version": "v1"}]},
            conclusion_id: {"id": conclusion_id, "symbol": f"{CONCLUSION}|{FACT_ID}", "value": "demo-bare", "pins": [{"role": "input", "id": count_id, "version": "v1"}]},
            resp_id: {"id": resp_id, "symbol": f"{RESP}|{FACT_ID}", "value": "demo-responsibility", "pins": [{"role": "input", "id": amount_id, "version": "v1"}, {"role": "input", "id": conclusion_id, "version": "v1"}]},
        }
        dispositions = [
            {"artifact_id": rule["id"], "symbol": f"{rule['publishes']}|{FACT_ID}", "disposition": "published", "finding_id": fid}
            for rule, fid in zip(rules, publications, strict=True)
        ]
        kernel_state = KernelState(
            fact_types={STMT: {"id": STMT, "version": "v1", "title": "Demo Statement", "nature": "record", "identity_keys": [
                {"name": "lender", "kind": "entity", "entity_kind": "demo.lender"},
                {"name": "statement", "kind": "entity", "entity_kind": "demo.statement"},
                {"name": "tax-year", "kind": "literal", "values": ["2025"]},
            ]}, "demo.source.box1": {"id": "demo.source.box1", "version": "v1", "title": "Synthetic Form 1098-E Box 1", "nature": "determinable", "identity_keys": [
                {"name": "lender", "kind": "entity", "entity_kind": "demo.lender"},
                {"name": "statement", "kind": "entity", "entity_kind": "demo.statement"},
                {"name": "tax-year", "kind": "literal", "values": ["2025"]},
            ]}},
            entities={
                "demo-lender": EntityLifecycle({"id": "demo-lender", "kind": "demo.lender", "label": "Demo Lender"}, "current"),
                "demo-s1": EntityLifecycle({"id": "demo-s1", "kind": "demo.statement", "label": "Demo Statement One"}, "current"),
            },
        )
        state = FindingState(fact_state=kernel_state, findings={source_id: {"fact_id": "demo.source.box1|lender=demo-lender,statement=demo-s1,tax-year=2025", "value": "120"}})
        view = _calculation_view(resolved_members=[*rules, parameter], state=state,
                                 publications=publications, dispositions=dispositions)
        assert view is not None
        _validate_calculation_view(view)
        group = view["groups"][0]
        self.assertEqual(group["symbol"], f"{AMOUNT}|{FACT_ID}")
        self.assertEqual(group["value"], publications[amount_id]["value"])
        self.assertEqual(group["pins"], publications[amount_id]["pins"])
        self.assertEqual(group["statementLabel"], {"lender": "Demo Lender", "statement": "Demo Statement One", "taxYear": "2025"})
        self.assertEqual(group["statementOutcome"]["route"]["interpretation"], "bare")
        self.assertEqual(group["statementOutcome"]["conclusion"]["findingId"], conclusion_id)
        self.assertEqual(group["responsibilities"][0]["findingId"], resp_id)
        self.assertEqual(group["responsibilities"][0]["wording"], "No borrowing is currently linked to Demo Statement One.")
        self.assertEqual(group["lineNote"], rules[3]["lineNote"])
        self.assertEqual(group["nodes"][0]["findingId"], count_id)
        wrong_axes = deepcopy(view)
        wrong_axes["groups"][0]["statementOutcome"]["route"]["interpretation"] = "linked"
        with self.assertRaises(PresentationModelError):
            _validate_calculation_view(wrong_axes)
        self.assertEqual(group["sourceFindings"], [{"findingId": source_id, "factId": "demo.source.box1|lender=demo-lender,statement=demo-s1,tax-year=2025", "value": "120", "factTypeId": "demo.source.box1", "factTypeVersion": "v1", "factTypeTitle": "Synthetic Form 1098-E Box 1", "origin": "assertion"}])
        self.assertEqual(group["assumptions"], [{"id": parameter["id"], "version": "v1", "value": "0", "consumerRuleId": "demo.rule.amount", "consumerFindingId": amount_id}])

        # A second statement receives only its own source finding, despite
        # using the same producer rules and output shapes.
        fact2 = f"{STMT}|lender=demo-lender,statement=demo-s2,tax-year=2025"
        source2 = "demo.source.box1.s2"
        extra_entities = dict(kernel_state.entities)
        extra_entities["demo-s2"] = EntityLifecycle(
            {"id": "demo-s2", "kind": "demo.statement", "label": "Demo Statement Two"}, "current")
        two_state = FindingState(fact_state=KernelState(fact_types=kernel_state.fact_types, entities=extra_entities), findings={
            **state.findings, source2: {"fact_id": f"demo.source.box1|lender=demo-lender,statement=demo-s2,tax-year=2025", "value": "900"}
        })
        two_publications: dict[str, dict[str, Any]] = dict(publications)
        two_rows = list(dispositions)
        suffix = ".s2"
        id_map = {fid: fid + suffix for fid in publications}
        for fid, publication in cast(dict[str, dict[str, Any]], publications).items():
            cloned = deepcopy(publication)
            cloned["id"] = id_map[fid]
            cloned["symbol"] = cloned["symbol"].replace(FACT_ID, fact2)
            for pin in cloned["pins"]:
                if pin.get("id") in id_map:
                    pin["id"] = id_map[pin["id"]]
                elif pin.get("id") == source_id:
                    pin["id"] = source2
            two_publications[id_map[fid]] = cloned
        for row in dispositions:
            cloned_row = dict(row)
            cloned_row["symbol"] = str(row["symbol"]).replace(FACT_ID, fact2)
            cloned_row["finding_id"] = id_map[str(row["finding_id"])]
            two_rows.append(cloned_row)
        two_view = _calculation_view(resolved_members=[*rules, parameter], state=two_state,
                                     publications=two_publications, dispositions=two_rows)
        assert two_view is not None
        two_groups = {item["factId"]: item for item in two_view["groups"]}
        self.assertEqual(set(two_groups), {FACT_ID, fact2})
        self.assertEqual({x["findingId"] for x in two_groups[FACT_ID]["sourceFindings"]}, {source_id})
        self.assertEqual({x["findingId"] for x in two_groups[fact2]["sourceFindings"]}, {source2})

        wrong_parameter_pin = deepcopy(publications)
        cast(dict[str, Any], wrong_parameter_pin[amount_id])["pins"][1]["version"] = "v2"
        with self.assertRaises(PresentationModelError):
            _calculation_view(resolved_members=[*rules, parameter], state=state,
                              publications=wrong_parameter_pin, dispositions=dispositions)

        default_input = deepcopy(publications)
        cast(dict[str, Any], default_input[amount_id])["pins"][0]["origin"] = "declared_default"
        default_view = _calculation_view(resolved_members=[*rules, parameter], state=state,
                                         publications=default_input, dispositions=dispositions)
        assert default_view is not None
        self.assertEqual(default_view["groups"][0]["sourceFindings"][0]["origin"], "declared_default")

        decimal_zero = deepcopy(publications)
        decimal_zero[count_id]["value"] = "0.0"
        zero_view = _calculation_view(resolved_members=[*rules, parameter], state=state,
                                      publications=decimal_zero, dispositions=dispositions)
        assert zero_view is not None
        self.assertEqual(zero_view["groups"][0]["statementOutcome"]["route"]["interpretation"], "bare")
        invalid_count = deepcopy(publications)
        invalid_count[count_id]["value"] = "0.5"
        with self.assertRaises(PresentationModelError):
            _calculation_view(resolved_members=[*rules, parameter], state=state,
                              publications=invalid_count, dispositions=dispositions)

        # The same box-1 leaf does not make an unrelated responsibility part
        # of the amount chain, and cannot carry the conclusion note.
        raw_only = deepcopy(publications)
        raw_only[resp_id]["pins"] = [{"role": "input", "id": "demo.source.box1", "version": "v1"}]
        raw_only_view = _calculation_view(resolved_members=[*rules, parameter], state=state,
                                          publications=raw_only, dispositions=dispositions)
        assert raw_only_view is not None
        raw_group = raw_only_view["groups"][0]
        self.assertEqual(raw_group["responsibilities"], [])
        self.assertNotIn("lineNote", raw_group)

        unlabeled_state = KernelState(fact_types=kernel_state.fact_types, entities={
            "demo-lender": kernel_state.entities["demo-lender"],
            "demo-s1": EntityLifecycle({"id": "demo-s1", "kind": "demo.statement"}, "current"),
        })
        with self.assertRaises(PresentationModelError):
            _calculation_view(resolved_members=[*rules, parameter], state=FindingState(fact_state=unlabeled_state, findings=state.findings),
                              publications=publications, dispositions=dispositions)

        # A blocked producer remains unresolved with its exact recorded code
        # and classified diagnostic instead of becoming a favorable count.
        blocked_dispositions = deepcopy(dispositions)
        blocked_dispositions[1].update(disposition="blocked", code="DEPENDENCY_INVALID",
                                       missing=["link-coverage-unjoinable"])
        blocked_dispositions[1].pop("finding_id")
        blocked_publications = deepcopy(publications)
        blocked_publications[amount_id]["pins"] = [{"role": "input", "id": "demo.source.box1", "version": "v1"}]
        blocked_view = _calculation_view(resolved_members=[*rules, parameter], state=state,
                                         publications=blocked_publications, dispositions=blocked_dispositions)
        assert blocked_view is not None
        blocked_route = blocked_view["groups"][0]["statementOutcome"]["route"]
        self.assertEqual(blocked_route["interpretation"], "unresolved")
        self.assertEqual(blocked_route["code"], "DEPENDENCY_INVALID")
        self.assertEqual(blocked_route["missing"], [{"kind": "diagnostic", "value": "link-coverage-unjoinable"}])

        parameter_rule = deepcopy(rules[1])
        parameter_rule["value"] = {"op": "link_count", "links": "demo.tax.reader.links",
                                    "empty": {"parameter": {"id": parameter["id"], "version": parameter["version"]}}}
        parameter_rules = [rules[0], parameter_rule, *rules[2:]]
        parameter_blocked = deepcopy(dispositions)
        parameter_blocked[1].update(disposition="blocked", code="DEPENDENCY_INVALID", missing=[parameter["id"]])
        parameter_blocked[1].pop("finding_id")
        parameter_blocked_publications = deepcopy(publications)
        parameter_pins = cast(list[dict[str, Any]], parameter_blocked_publications[amount_id]["pins"])
        parameter_blocked_publications[amount_id]["pins"] = [
            pin for pin in parameter_pins
            if pin.get("id") != count_id
        ]
        parameter_view = _calculation_view(resolved_members=[*parameter_rules, parameter], state=state,
                                           publications=parameter_blocked_publications, dispositions=parameter_blocked)
        assert parameter_view is not None
        self.assertEqual(parameter_view["groups"][0]["statementOutcome"]["route"]["missing"],
                         [{"kind": "parameter", "id": parameter["id"], "version": parameter["version"]}])
        absent_parameter_rule = deepcopy(rules[1])
        absent_parameter_rule["value"] = {"op": "demo", "parameter_id": "demo.parameter.absent"}
        absent_parameter_rows = deepcopy(dispositions)
        absent_parameter_rows[1].update(disposition="blocked", code="DEPENDENCY_ABSENT", missing=["demo.parameter.absent"])
        absent_parameter_rows[1].pop("finding_id")
        absent_parameter_view = _calculation_view(
            resolved_members=[rules[0], absent_parameter_rule, *rules[2:], parameter], state=state,
            publications=parameter_blocked_publications, dispositions=absent_parameter_rows)
        assert absent_parameter_view is not None
        self.assertEqual(absent_parameter_view["groups"][0]["statementOutcome"]["route"]["missing"],
                         [{"kind": "parameter", "id": "demo.parameter.absent"}])
        absent_table_rule = deepcopy(rules[1])
        absent_table_rule["value"] = {"lookup": {"table_id": "demo.table.absent"}}
        absent_table_rows = deepcopy(absent_parameter_rows)
        absent_table_rows[1]["missing"] = ["demo.table.absent"]
        absent_table_view = _calculation_view(
            resolved_members=[rules[0], absent_table_rule, *rules[2:], parameter], state=state,
            publications=parameter_blocked_publications, dispositions=absent_table_rows)
        assert absent_table_view is not None
        self.assertEqual(absent_table_view["groups"][0]["statementOutcome"]["route"]["missing"],
                         [{"kind": "parameter", "id": "demo.table.absent"}])
        absent_source_rule = deepcopy(rules[1])
        absent_source_rule["value"] = {"op": "collect", "name": "demo.source-set.absent"}
        absent_source_rows = deepcopy(absent_parameter_rows)
        absent_source_rows[1]["missing"] = ["demo.source-set.absent"]
        absent_source_view = _calculation_view(
            resolved_members=[rules[0], absent_source_rule, *rules[2:], parameter], state=state,
            publications=parameter_blocked_publications, dispositions=absent_source_rows)
        assert absent_source_view is not None
        self.assertEqual(absent_source_view["groups"][0]["statementOutcome"]["route"]["missing"],
                         [{"kind": "symbol", "value": "demo.source-set.absent"}])
        absent_ref_rule = deepcopy(rules[1])
        absent_ref_rule["value"] = {"op": "ref", "name": "demo.ref.absent"}
        absent_ref_rows = deepcopy(absent_parameter_rows)
        absent_ref_rows[1]["missing"] = ["demo.ref.absent"]
        absent_ref_view = _calculation_view(
            resolved_members=[rules[0], absent_ref_rule, *rules[2:], parameter], state=state,
            publications=parameter_blocked_publications, dispositions=absent_ref_rows)
        assert absent_ref_view is not None
        self.assertEqual(absent_ref_view["groups"][0]["statementOutcome"]["route"]["missing"],
                         [{"kind": "symbol", "value": "demo.ref.absent"}])
        for operation in ("collect", "count"):
            absent_named_source = f"demo.{operation}.name.absent"
            named_source_rule = deepcopy(rules[1])
            named_source_rule["value"] = {"op": operation, "name": absent_named_source}
            named_source_rows = deepcopy(absent_parameter_rows)
            named_source_rows[1]["missing"] = [absent_named_source]
            named_source_view = _calculation_view(
                resolved_members=[rules[0], named_source_rule, *rules[2:], parameter], state=state,
                publications=parameter_blocked_publications, dispositions=named_source_rows)
            assert named_source_view is not None
            self.assertEqual(named_source_view["groups"][0]["statementOutcome"]["route"]["missing"],
                             [{"kind": "symbol", "value": absent_named_source}])
        empty_parameter_rule = deepcopy(rules[1])
        empty_parameter_rule["value"] = {"op": "link_coverage", "empty": {"parameter": {"id": "demo.parameter.empty"}}}
        empty_parameter_rows = deepcopy(absent_parameter_rows)
        empty_parameter_rows[1]["missing"] = ["demo.parameter.empty"]
        empty_parameter_view = _calculation_view(
            resolved_members=[rules[0], empty_parameter_rule, *rules[2:], parameter], state=state,
            publications=parameter_blocked_publications, dispositions=empty_parameter_rows)
        assert empty_parameter_view is not None
        self.assertEqual(empty_parameter_view["groups"][0]["statementOutcome"]["route"]["missing"],
                         [{"kind": "parameter", "id": "demo.parameter.empty"}])
        invalid_finding_missing = deepcopy(blocked_view)
        invalid_finding_missing["groups"][0]["statementOutcome"]["route"]["missing"] = [
            {"kind": "finding", "findingId": COUNT}
        ]
        with self.assertRaises(PresentationModelError):
            _validate_calculation_view(invalid_finding_missing)

        blocked_amount_rows = deepcopy(dispositions)
        blocked_amount_rows[0].update(disposition="blocked", code="DEPENDENCY_ABSENT", missing=["demo-marker"])
        blocked_amount_rows[0].pop("finding_id")
        blocked_amount = _calculation_view(resolved_members=[*rules, parameter], state=state,
                                           publications=publications, dispositions=blocked_amount_rows)
        assert blocked_amount is not None
        self.assertEqual(blocked_amount["groups"][0]["disposition"], "blocked")
        self.assertEqual(blocked_amount["groups"][0]["code"], "DEPENDENCY_ABSENT")
        self.assertNotIn("value", blocked_amount["groups"][0])

        # A token that collides with a declared output symbol is still a
        # finding when the run records that finding id.
        collision_rows = deepcopy(blocked_dispositions)
        collision_rows[1]["missing"] = [COUNT]
        collision_state = FindingState(fact_state=kernel_state, findings={
            **state.findings, COUNT: {"fact_id": "demo.source.collision|lender=demo-lender,statement=demo-s1,tax-year=2025", "value": "recorded"}
        })
        collision_view = _calculation_view(resolved_members=[*rules, parameter], state=collision_state,
                                           publications=blocked_publications, dispositions=collision_rows)
        assert collision_view is not None
        self.assertEqual(collision_view["groups"][0]["statementOutcome"]["route"]["missing"],
                         [{"kind": "finding", "findingId": COUNT, "factId": "demo.source.collision|lender=demo-lender,statement=demo-s1,tax-year=2025"}])

        failed_responsibility = deepcopy(dispositions)
        failed_responsibility[4].update(disposition="blocked", code="DEPENDENCY_ABSENT", missing=[CONCLUSION])
        failed_responsibility[4].pop("finding_id")
        failure_view = _calculation_view(resolved_members=[*rules, parameter], state=state,
                                         publications=publications, dispositions=failed_responsibility)
        assert failure_view is not None
        failure_group = failure_view["groups"][0]
        self.assertEqual(failure_group["responsibilities"], [])
        self.assertEqual(failure_group["statementOutcome"]["responsibilityFailures"][0]["explainedBy"],
                         [{"symbol": f"{CONCLUSION}|{FACT_ID}", "interpretation": "published"}])

        # A finding's symbol suffix cannot override its recorded producer.
        wrong_producer = deepcopy(dispositions)
        wrong_producer[1]["artifact_id"] = "demo.rule.not-count"
        with self.assertRaises(PresentationModelError):
            _calculation_view(resolved_members=[*rules, parameter], state=state,
                              publications=publications, dispositions=wrong_producer)

    def test_validator_rejects_integrated_or_unkeyed_amount(self) -> None:
        view = {"integrated": False, "amountSymbol": AMOUNT, "groups": [{
            "symbol": f"{AMOUNT}|{FACT_ID}", "factId": FACT_ID, "ruleId": "demo.rule.amount",
            "ruleVersion": "v1", "disposition": "blocked", "pins": [], "nodes": [],
            "responsibilities": [], "missing": [{"kind": "diagnostic", "value": "demo-marker"}],
            "sourceFindings": [], "assumptions": [], "code": "demo-blocked",
            "statementOutcome": {"route": {"interpretation": "not-computed"},
                "statementScope": {"interpretation": "not-computed"},
                "conclusion": {"interpretation": "not-computed"}, "responsibilityFailures": []},
        }]}
        _validate_calculation_view(view)
        view["integrated"] = True
        with self.assertRaises(PresentationModelError):
            _validate_calculation_view(view)

    def test_legacy_model_without_calculation_view_remains_valid(self) -> None:
        from packages.derivation.presentation_projection import validate_presentation_model

        validate_presentation_model({"schema": "presentation-model.v1", "runId": "demo.run.old",
            "pinLabels": {}, "sections": [], "citationGroups": [], "attachments": [],
            "unsupportedSourceFindings": []})


if __name__ == "__main__":
    unittest.main()
