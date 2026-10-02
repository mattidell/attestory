"""Live saved-file assertions for the one-package Track 6b demonstration."""
from __future__ import annotations

import importlib.util
import json
import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from typing import Any, cast

import pytest

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "tools/presentation_harness/examples/generate_track6b_saved_presentations.py"


def _live_custom_case(generator: Any, surface: Any, acts: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
    from packages.derivation.live import live_coordinate_run
    from packages.derivation.live_workspace import WorkspaceCapability

    with TemporaryDirectory(prefix="track6b-control-workspace-") as temp_dir:
        result = live_coordinate_run(
            WorkspaceCapability(Path(temp_dir) / "L"), repo_root=ROOT,
            authoritative_acts=acts, workspace_revision=len(acts), run_scope=generator.SCOPE,
            scope_user=generator.USER, request={"schema": "run-request.v1"}, run_id=run_id,
            governance_pins=[], surface=generator._surface(surface), output_name="out.json")
        if result.refusal is not None or result.presentation_path is None:
            raise AssertionError(f"synthetic control live run failed: {result.refusal}")
        return cast(dict[str, Any], json.loads(result.presentation_path.read_text("utf-8")))


@pytest.mark.live  # Drives one-package live coordinator runs through the saved-file writer.
class Track6bSavedModelFidelity(unittest.TestCase):
    def test_known_tuition_control_is_zero_and_keeps_narrow_statement_responsibility(self) -> None:
        spec = importlib.util.spec_from_file_location("track6b_saved_generator", GENERATOR)
        assert spec is not None and spec.loader is not None
        generator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generator)
        surface, acts, _members = generator._prepare_case("adverse", ROOT)
        claim_act = next(act for act in acts if act.get("kind") == "assertion"
                         and act.get("payload", {}).get("finding", {}).get("id") == "demo.finding.track6b.claim.adverse")
        claim_act["payload"]["finding"]["value"] = "tuition"
        for act in acts:
            entity = act.get("payload", {}).get("entity") if isinstance(act.get("payload"), dict) else None
            if isinstance(entity, dict) and entity.get("id") == "demo.sli.circumstance.adverse":
                entity["label"] = "S1 statement-wide tuition claim"
        model = _live_custom_case(generator, surface, generator._renumber(acts), "demo.track6b.control.tuition")
        s1 = next(g for g in model["calculationView"]["groups"] if g["statementLabel"]["statement"] == "S1")
        self.assertEqual(s1["value"], "400.0")
        self.assertEqual(str(s1["statementOutcome"]["statementScope"]["claims"][0]["value"]), "0")
        self.assertEqual(s1["statementOutcome"]["statementScope"]["interpretation"], "no-whole-amount-disqualifier")
        self.assertEqual(len(s1["responsibilities"]), 3)
        self.assertIn("lineNote", s1)

    def test_linked_s1_does_not_get_bare_conclusion_or_s2_effect(self) -> None:
        spec = importlib.util.spec_from_file_location("track6b_saved_generator", GENERATOR)
        assert spec is not None and spec.loader is not None
        generator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generator)
        surface, acts, _members = generator._prepare_case("ordinary", ROOT)
        adoption = acts.pop()
        acts.extend([
            {"schema": "act.v1", "act_id": "demo.track6b.link.entity", "actor": generator.USER,
             "at": "2026-09-27T12:03:00Z", "committed_against": len(acts), "kind": "entity-introduced",
             "payload": {"entity": {"schema": "entity.v1", "id": "demo.loan.linked-s1", "kind": "demo.sli-borrowing", "label": "S1 synthetic loan"}}},
            {"schema": "act.v1", "act_id": "demo.track6b.link.assertion", "actor": generator.USER,
             "at": "2026-09-27T12:04:00Z", "committed_against": len(acts) + 1, "kind": "assertion",
             "payload": {"finding": generator._attested(
                 "demo.finding.track6b.linked-s1",
                 f"{generator.LINKS}|lender=demo.lender.reader.s1,statement=demo.statement.reader.s1,tax-year=2025,borrowing=demo.loan.linked-s1", {})}},
        ])
        acts.append(adoption)
        model = _live_custom_case(generator, surface, generator._renumber(acts), "demo.track6b.control.linked-s1")
        groups = {g["statementLabel"]["statement"]: g for g in model["calculationView"]["groups"]}
        self.assertEqual(groups["S1"]["statementOutcome"]["route"]["interpretation"], "linked")
        self.assertNotEqual(groups["S1"]["statementOutcome"]["conclusion"]["interpretation"], "published")
        self.assertEqual(groups["S1"]["responsibilities"], [])
        self.assertEqual(groups["S2"]["statementOutcome"]["route"]["interpretation"], "bare")
        self.assertEqual(groups["S2"]["value"], "700.0")

    def test_forward_and_reference_runners_match_reader_outputs_for_all_cases(self) -> None:
        from packages.derivation.live import _resolve_run_authorization, _resolved_run_material
        from packages.derivation.loader import DerivationSchemas, load_canon
        from packages.derivation.marshal import marshal_live_run_context
        from packages.derivation.production_resolver import Refusal, resolve_production_package
        from packages.derivation.reference_runner import run_reference
        from packages.derivation.runner import run
        from packages.kernel.currency import compute_currency
        from packages.kernel.findings import project
        from packages.tax.loader import domain_companion_presence_pairs
        from packages.tax.loader import install_domain_companion_presence, install_domain_companion_equalities
        from packages.tax.loader import install_domain_declaration_signal_contradictions

        spec = importlib.util.spec_from_file_location("track6b_saved_generator", GENERATOR)
        assert spec is not None and spec.loader is not None
        generator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generator)
        for case in ("ordinary", "adverse", "unresolved"):
            surface, acts, members = generator._prepare_case(case, ROOT)
            schemas = DerivationSchemas()
            install_domain_companion_presence(schemas.registry)
            install_domain_companion_equalities(schemas.registry)
            install_domain_declaration_signal_contradictions(schemas.registry)
            resolved = resolve_production_package(
                acts, run_scope=generator.SCOPE, scope_user=generator.USER,
                workspace_revision=len(acts), surface=generator._surface(surface), schemas=schemas)
            if isinstance(resolved, Refusal):
                self.fail(f"{case}: package refused: {resolved}")
            state = project(tuple(dict(act) for act in acts), schemas.registry)
            currency = compute_currency(state)
            material = _resolved_run_material(resolved)
            rules, parameters, families, mappings, fact_types, bindings, collect_names = material
            authorization = _resolve_run_authorization(
                acts, run_scope=generator.SCOPE, scope_user=generator.USER, rules=rules,
                corpus={member["id"]: member for member in resolved.resolved_members}, package=resolved.package)
            context = marshal_live_run_context(
                run_id=f"demo.track6b.parity.{case}", state=state, currency=currency, rules=rules,
                parameters=parameters, canon=load_canon(schemas),
                adoption_pin={"role": "adoption", "id": resolved.package["id"], "version": resolved.package["version"]},
                governance_pins=[], family_declarations=families, closure_mappings=mappings,
                fact_types=fact_types, input_bindings=bindings, collect_source_names=collect_names,
                emission_only_source_names=list(material.emission_only_names),
                companion_presence_pairs=domain_companion_presence_pairs(), authorization=authorization,
                reporting_year=2025, parameter_index=material.parameter_index)
            forward = run(context._context, schemas)
            reference = run_reference(context._context, schemas)

            def reader_snapshot(result: Any) -> dict[tuple[str, str], tuple[Any, ...]]:
                disposition_pairs = [(d["artifact_id"], d.get("symbol", ""), d) for d in result.dispositions]
                disposition_map = {(artifact_id, symbol): row for artifact_id, symbol, row in disposition_pairs}
                if len(disposition_map) != len(disposition_pairs):
                    raise AssertionError("runner returned duplicate keyed dispositions")
                published = {p.finding["id"]: p.finding for p in result.publications}
                relevant = {}
                for rule in members:
                    if rule.get("reader_role") not in {"statement-amount", "link-count", "statement-scope-classifier", "statement-scope-disqualifier-count", "bare-statement-conclusion", "responsibility"}:
                        continue
                    for key, row in disposition_map.items():
                        if key[0] != rule["id"]:
                            continue
                        finding = published.get(row.get("finding_id"), {})
                        relevant[key] = (row["disposition"], finding.get("value"), finding.get("pins"), row.get("code"), row.get("missing"))
                return cast(dict[tuple[str, str], tuple[Any, ...]], relevant)
            forward_snapshot = reader_snapshot(forward)
            self.assertEqual(forward_snapshot, reader_snapshot(reference), case)
            rules_by_id = {member["id"]: member for member in members if "publishes" in member}
            amount_rows = [(symbol, values) for (rule_id, symbol), values in forward_snapshot.items()
                           if rules_by_id.get(rule_id, {}).get("reader_role") == "statement-amount"]
            self.assertEqual(len(amount_rows), 2)
            expected_symbols = {
                "S1": f"{generator.AMOUNT}|{generator._member_fact_id(generator.BOX1, 'demo.lender.reader.s1', 'demo.statement.reader.s1')}",
                "S2": f"{generator.AMOUNT}|{generator._member_fact_id(generator.BOX1, 'demo.lender.reader.s2', 'demo.statement.reader.s2')}",
            }
            amount_by_statement = {name: next(values for symbol, values in amount_rows if symbol == exact_symbol)
                                   for name, exact_symbol in expected_symbols.items()}
            self.assertEqual(set(amount_by_statement), {"S1", "S2"})
            if case == "unresolved":
                self.assertEqual(amount_by_statement["S1"][0], "blocked")
                self.assertIsNone(amount_by_statement["S1"][1])
            else:
                self.assertEqual(str(amount_by_statement["S1"][1]), "0" if case == "adverse" else "400.0")
            self.assertEqual(amount_by_statement["S2"][0], "published")
            self.assertEqual(str(amount_by_statement["S2"][1]), "700.0")

    def test_one_run_saved_models_preserve_worksheet_and_statement_locality(self) -> None:
        spec = importlib.util.spec_from_file_location("track6b_saved_generator", GENERATOR)
        assert spec is not None and spec.loader is not None
        generator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generator)
        paths: dict[str, Path] = {}
        models: dict[str, dict[str, Any]] = {}
        for case in ("ordinary", "adverse", "unresolved"):
            outcome, members, path = generator._run_case(case, ROOT)
            paths[case] = path
            if outcome.output_path is None or outcome.publications is None:
                raise AssertionError(f"{case}: live run did not retain report/publications")
            report = cast(dict[str, Any], json.loads(outcome.output_path.read_text("utf-8")))
            dispositions = report["dispositions"]
            publications = {p.finding["id"]: p.finding for p in outcome.publications}
            rules = {m["id"]: m for m in members if "publishes" in m}
            saved_before_drop = cast(dict[str, Any], json.loads(path.read_text("utf-8")))
            view = saved_before_drop["calculationView"]
            for group in view["groups"]:
                amount_rule = rules[group["ruleId"]]
                amount_row = next(d for d in dispositions if d.get("artifact_id") == group["ruleId"] and d.get("symbol") == group["symbol"])
                self.assertEqual(group["ruleVersion"], amount_rule["version"])
                self.assertEqual(amount_row["disposition"], group["disposition"])
                if group["disposition"] == "published":
                    self.assertEqual(amount_row["finding_id"], group["findingId"])
                    amount_finding = publications[group["findingId"]]
                    self.assertEqual(group["value"], amount_finding["value"])
                    self.assertEqual(group["pins"], amount_finding["pins"])
                else:
                    self.assertEqual(group["code"], amount_row["code"])
                    self.assertEqual(amount_row["missing"], [item.get("value", item.get("id", item.get("findingId"))) for item in group["missing"]])
                for axis_name in ("route", "statementScope", "conclusion"):
                    axis = group["statementOutcome"][axis_name]
                    if "findingId" in axis:
                        finding = publications[axis["findingId"]]
                        axis_row = next(d for d in dispositions if d.get("finding_id") == axis["findingId"])
                        producer = rules[axis_row["artifact_id"]]
                        self.assertEqual(axis["symbol"], finding["symbol"])
                        self.assertEqual(axis.get("value"), finding["value"])
                        self.assertEqual(axis.get("pins"), finding["pins"])
                        self.assertEqual(axis["ruleId"], producer["id"])
                        self.assertEqual(axis["ruleVersion"], producer["version"])
                    elif axis.get("disposition") == "blocked":
                        axis_row = next(d for d in dispositions if d.get("artifact_id") == axis.get("ruleId") and d.get("symbol") == axis.get("symbol"))
                        self.assertEqual(axis_row["code"], axis["code"])
                        self.assertEqual(axis_row["missing"], [item.get("value", item.get("id", item.get("findingId"))) for item in axis["missing"]])
                for claim in group["statementOutcome"]["statementScope"].get("claims", []):
                    if "findingId" in claim:
                        claim_finding = publications[claim["findingId"]]
                        claim_row = next(d for d in dispositions if d.get("finding_id") == claim["findingId"])
                        classifier = rules[claim_row["artifact_id"]]
                        self.assertEqual(claim["ruleId"], classifier["id"])
                        self.assertEqual(claim["value"], claim_finding["value"])
                        self.assertEqual(claim["pins"], claim_finding["pins"])
                for responsibility in group["responsibilities"]:
                    finding = publications[responsibility["findingId"]]
                    row = next(d for d in dispositions if d.get("finding_id") == responsibility["findingId"])
                    rule = rules[row["artifact_id"]]
                    self.assertEqual(responsibility["pins"], finding["pins"])
                    self.assertEqual(responsibility["value"], finding["value"])
                    self.assertEqual(responsibility["ruleId"], rule["id"])
                    self.assertEqual(responsibility.get("wording"), rule.get("wording", "").replace("{statement}", group["statementLabel"]["statement"]))
                if "lineNote" in group:
                    conclusion_rule = rules[group["statementOutcome"]["conclusion"]["ruleId"]]
                    self.assertEqual(group["lineNote"], conclusion_rule["lineNote"].replace("{statement}", group["statementLabel"]["statement"]))
                for assumption in group["assumptions"]:
                    declaration = next(m for m in members if m.get("schema") == "parameter-declaration.v1" and m.get("id") == assumption["id"] and m.get("version") == assumption["version"])
                    self.assertEqual(assumption["value"], declaration["values"])
                    if assumption["consumerFindingId"]:
                        consumer = publications[assumption["consumerFindingId"]]
                        self.assertIn({"role": "parameter", "id": assumption["id"], "version": assumption["version"]}, consumer["pins"])
                for source in group["sourceFindings"]:
                    if source["factId"] == group["factId"]:
                        self.assertEqual(source["value"], 400.0 if group["statementLabel"]["statement"] == "S1" else 700.0)
                    else:
                        claim_facts = {claim["factId"] for claim in group["statementOutcome"]["statementScope"].get("claims", [])}
                        self.assertIn(source["factId"], claim_facts)
                    all_pins = list(group["pins"])
                    all_pins.extend(pin for node in group["nodes"] for pin in node["pins"])
                    all_pins.extend(pin for axis in group["statementOutcome"].values() if isinstance(axis, dict) for pin in axis.get("pins", []))
                    all_pins.extend(pin for claim in group["statementOutcome"]["statementScope"].get("claims", []) for pin in claim.get("pins", []))
                    self.assertTrue(any(pin.get("id") == source["findingId"] for pin in all_pins))
                for claim in group["statementOutcome"]["statementScope"].get("claims", []):
                    self.assertTrue(claim.get("label", "").startswith("S1 statement-wide"))
            line21 = next(s for s in saved_before_drop["sections"] if s["id"] == "line-sch1-21")
            line21_finding_id = line21["resolved"]["act"]["finding"]["id"]
            self.assertEqual(str(line21["resolved"]["value"]), str(publications[line21_finding_id]["value"]))
            # Drop every in-memory live result before reopening the durable model.
            del publications, dispositions, report, saved_before_drop, outcome, members
            models[case] = cast(dict[str, Any], json.loads(path.read_text("utf-8")))
            self.assertEqual(models[case]["schema"], "presentation-model.v1")
            self.assertIn("calculationView", models[case])
            self.assertFalse(models[case]["calculationView"]["integrated"])
            self.assertEqual(len(models[case]["calculationView"]["groups"]), 2)

        def section(model: dict[str, Any], section_id: str) -> dict[str, Any]:
            found = [s for s in model["sections"] if s["id"] == section_id]
            if len(found) != 1:
                raise AssertionError(f"expected one {section_id} worksheet section")
            return cast(dict[str, Any], found[0])

        worksheet_sections = [section(model, "line-sch1-21") for model in models.values()]
        self.assertTrue(all(s["field"].get("binds_symbol") == "tax.us.2025.schedule1.line21-sli-deduction"
                            for s in worksheet_sections))
        self.assertTrue(all(s["resolved"].get("disposition") == "published_value" for s in worksheet_sections))
        self.assertEqual({str(s["resolved"].get("value")) for s in worksheet_sections}, {str(worksheet_sections[0]["resolved"].get("value"))})

        groups = {case: {g["statementLabel"]["statement"]: g for g in model["calculationView"]["groups"]}
                  for case, model in models.items()}
        for case in groups:
            self.assertEqual(set(groups[case]), {"S1", "S2"})
        canonical_s2 = json.dumps(groups["ordinary"]["S2"], sort_keys=True)
        self.assertTrue(all(json.dumps(by_statement["S2"], sort_keys=True) == canonical_s2 for by_statement in groups.values()))
        self.assertEqual(groups["ordinary"]["S1"]["statementOutcome"]["route"]["interpretation"], "bare")
        self.assertEqual(groups["adverse"]["S1"]["statementOutcome"]["statementScope"]["interpretation"], "whole-amount-disqualifier")
        self.assertEqual(groups["unresolved"]["S1"]["statementOutcome"]["conclusion"]["interpretation"], "unresolved")
        self.assertEqual(str(groups["ordinary"]["S1"]["value"]), "400.0")
        self.assertEqual(str(groups["adverse"]["S1"]["value"]), "0")
        self.assertEqual(groups["unresolved"]["S1"]["disposition"], "blocked")
        self.assertNotIn("value", groups["unresolved"]["S1"])
        self.assertEqual(str(groups["ordinary"]["S2"]["value"]), "700.0")
        self.assertEqual(len(groups["ordinary"]["S1"]["responsibilities"]), 3)
        self.assertEqual(len(groups["ordinary"]["S2"]["responsibilities"]), 3)
        self.assertTrue(groups["ordinary"]["S1"].get("lineNote"))
        for case in ("adverse", "unresolved"):
            self.assertEqual(groups[case]["S1"]["responsibilities"], [])
            self.assertNotIn("lineNote", groups[case]["S1"])
        self.assertTrue(all(str(s["resolved"]["value"]) == "1100" for s in worksheet_sections))
        self.assertNotEqual(str(worksheet_sections[1]["resolved"]["value"]), str(float(groups["adverse"]["S1"]["value"]) + float(groups["adverse"]["S2"]["value"])))


if __name__ == "__main__":
    unittest.main()
