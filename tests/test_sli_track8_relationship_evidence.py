"""Track 8 evidence boundary for borrowing relationships.

The supported production surface records Form 1098-E statement amounts and
the statement-level witnesses in ``f1098e.bundle.json``. These tests run that
existing statement path through the live coordinator and reopen its saved
presentation. The synthetic act list is assembled by the existing Track 6
test helper; it is not a production ordinary-fact producer for schooling or
borrowing relationships.
"""

from __future__ import annotations

import json
import importlib.util
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import (
    _resolve_run_authorization,
    _resolved_run_material,
    live_coordinate_run,
)
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.marshal import marshal_live_run_context
from packages.derivation.production_resolver import Refusal, resolve_production_package
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import run
from packages.kernel.currency import compute_currency
from packages.kernel.findings import FindingModelError, project
from packages.tax.loader import (
    domain_companion_presence_pairs,
    install_domain_companion_equalities,
    install_domain_companion_presence,
    install_domain_declaration_signal_contradictions,
)
ROOT = Path(__file__).resolve().parent.parent
SCRATCH = ROOT / "temp" / "track8"
TRACK6B_GENERATOR = ROOT / "tools/presentation_harness/examples/generate_track6b_saved_presentations.py"


def _track6b_generator() -> Any:
    spec = importlib.util.spec_from_file_location("track6b_track8_relationship", TRACK6B_GENERATOR)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load prototype package helper at {TRACK6B_GENERATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _prototype_relationship_acts(
    generator: Any,
) -> tuple[Any, list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], str]:
    """Add manually supplied statement-to-borrowing claims to a validated demo surface.

    The added claims are synthetic prototype inputs. There is no ordinary
    schooling/financing recorder behind them.
    """
    surface, acts, members = generator._prepare_case("ordinary", ROOT)
    adoption = acts.pop()
    relationships = (
        ("s1", "a"), ("s1", "b"), ("s2", "a"),
    )
    finding_ids: dict[tuple[str, str], str] = {}
    introduced_borrowings: set[str] = set()
    for index, (statement, borrowing_suffix) in enumerate(relationships):
        borrowing = f"demo.track8.borrowing.{borrowing_suffix}"
        lender = f"demo.lender.reader.{statement}"
        statement_id = f"demo.statement.reader.{statement}"
        if borrowing not in introduced_borrowings:
            acts.append({
                "schema": "act.v1", "act_id": f"demo.track8.relationship.entity.{index}",
                "actor": generator.USER, "at": f"2026-09-28T12:0{index}:00Z",
                "committed_against": len(acts), "kind": "entity-introduced",
                "payload": {"entity": {"schema": "entity.v1", "id": borrowing,
                                         "kind": "demo.sli-borrowing", "label": "Synthetic borrowing"}},
            })
            introduced_borrowings.add(borrowing)
        finding_id = f"demo.finding.track8.statement-borrowing.{statement}.{borrowing_suffix}"
        finding_ids[(statement, borrowing_suffix)] = finding_id
        fact_id = (
            f"{generator.LINKS}|lender={lender},statement={statement_id},tax-year=2025,"
            f"borrowing={borrowing}"
        )
        acts.append({
            "schema": "act.v1", "act_id": f"demo.track8.relationship.assertion.{index}",
            "actor": generator.USER, "at": f"2026-09-28T12:1{index}:00Z",
            "committed_against": len(acts), "kind": "assertion",
            "payload": {"finding": generator._attested(finding_id, fact_id, {})},
        })
    acts.append(adoption)
    initial = generator._renumber(list(acts))
    # Retraction removes only S1 -> borrowing A. The same borrowing remains
    # connected to S2, and S1 -> borrowing B remains current.
    acts.append({
        "schema": "act.v1", "act_id": "demo.track8.relationship.retract-s1-a",
        "actor": generator.USER, "at": "2026-09-28T12:40:00Z",
        "committed_against": len(acts), "kind": "finding-retracted",
        "payload": {"finding_id": finding_ids[("s1", "a")]},
    })
    return surface, members, initial, generator._renumber(acts), finding_ids[("s1", "a")]


def _runner_parity(acts: list[dict[str, Any]], surface: Any) -> tuple[dict[str, Any], dict[str, Any]]:
    """Resolve, admit, marshal and compare both runners on the same acts."""
    generator = _track6b_generator()
    schemas = DerivationSchemas()
    install_domain_companion_presence(schemas.registry)
    install_domain_companion_equalities(schemas.registry)
    install_domain_declaration_signal_contradictions(schemas.registry)
    resolved = resolve_production_package(
        acts, run_scope={"jurisdiction": "us", "year": "2025"},
        scope_user=generator.USER, workspace_revision=len(acts),
        surface=generator_surface(surface), schemas=schemas,
    )
    if isinstance(resolved, Refusal):
        raise AssertionError(f"prototype package was not admitted: {resolved!r}")
    state = project(tuple(dict(act) for act in acts), schemas.registry)
    currency = compute_currency(state)
    material = _resolved_run_material(resolved)
    rules, parameters, families, mappings, fact_types, bindings, collect_names = material
    authorization = _resolve_run_authorization(
        acts, run_scope={"jurisdiction": "us", "year": "2025"},
        scope_user=generator.USER, rules=rules,
        corpus={member["id"]: member for member in resolved.resolved_members},
        package=resolved.package,
    )
    context = marshal_live_run_context(
        run_id="demo.track8.relationship.parity", state=state, currency=currency,
        rules=rules, parameters=parameters, canon=load_canon(schemas),
        adoption_pin={"role": "adoption", "id": resolved.package["id"], "version": resolved.package["version"]},
        governance_pins=[], family_declarations=families, closure_mappings=mappings,
        fact_types=fact_types, input_bindings=bindings, collect_source_names=collect_names,
        emission_only_source_names=list(material.emission_only_names),
        companion_presence_pairs=domain_companion_presence_pairs(), authorization=authorization,
        reporting_year=2025, parameter_index=material.parameter_index,
    )
    forward, reference = run(context._context, schemas), run_reference(context._context, schemas)

    def snapshot(result: Any) -> dict[str, Any]:
        return {
            "dispositions": sorted(
                [(row.get("artifact_id"), row.get("symbol"), row["disposition"],
                  row.get("finding_id"), row.get("code"), row.get("missing"))
                 for row in result.dispositions],
                key=lambda row: json.dumps(row, sort_keys=True),
            ),
            "publications": sorted(
                [(item.finding["symbol"], item.finding.get("value"), item.finding.get("pins"))
                 for item in result.publications],
                key=lambda row: json.dumps(row, sort_keys=True),
            ),
        }
    return snapshot(forward), snapshot(reference)


def generator_surface(surface: Any) -> Any:
    return _track6b_generator()._surface(surface)


def _route_publication(snapshot: dict[str, Any], generator: Any, statement: str) -> tuple[Any, ...]:
    statement_fact_id = (
        f"{generator.BOX1}|lender=demo.lender.reader.{statement.lower()},"
        f"statement=demo.statement.reader.{statement.lower()},tax-year=2025"
    )
    symbol = f"{generator.COUNT}|{statement_fact_id}"
    return next(row for row in snapshot["publications"] if row[0] == symbol)


def _saved_prototype_run(name: str, acts: list[dict[str, Any]], surface: Any) -> dict[str, Any]:
    """Execute and reopen saved output from the existing experimental reader.

    The live workspace correctly refuses any output directory under the
    repository, including ignored temp/ paths. Copy the coordinator's saved
    model into ignored synthetic scratch, discard live objects and the
    restricted workspace, then reopen that copy.
    """
    SCRATCH.mkdir(parents=True, exist_ok=True)
    retained = SCRATCH / f"{name}.presentation-model.v1.json"
    with TemporaryDirectory(prefix=f"track8-{name}-") as raw:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(raw) / "workspace"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope={"jurisdiction": "us", "year": "2025"},
            scope_user=_track6b_generator().USER,
            request={"schema": "run-request.v1"},
            run_id=f"demo.track8.relationship.{name}",
            governance_pins=[],
            surface=generator_surface(surface),
            output_name=f"{name}.json",
        )
        if outcome.refusal is not None or outcome.presentation_path is None:
            raise AssertionError(f"prototype live run did not save: {outcome.refusal!r}")
        retained.write_bytes(outcome.presentation_path.read_bytes())
        del outcome
    # The run workspace and outcome are gone; recovery uses only saved JSON.
    return cast(dict[str, Any], json.loads(retained.read_text("utf-8")))


class CurrentStatementPath(unittest.TestCase):
    def test_two_equal_manual_link_rows_correct_and_recover_with_statement_isolation(self) -> None:
        generator = _track6b_generator()
        surface, _members, initial_acts, corrected_acts, retracted_finding = _prototype_relationship_acts(generator)
        link_rule = next(member for member in _members if member.get("id") == generator.LINKER)

        # These claims are distinct records with equal values. Before the
        # correction, the admitted package and both runners retain both rows.
        before_forward, before_reference = _runner_parity(initial_acts, surface)
        self.assertEqual(before_forward, before_reference)
        before_s1 = _route_publication(before_forward, generator, "S1")
        self.assertEqual(before_s1[1], "2")
        before_s1_pins = {pin["id"] for pin in before_s1[2] if pin.get("role") == "input"}
        self.assertEqual(before_s1_pins, {
            "demo.f1098e.box1.0",
            "demo.finding.track8.statement-borrowing.s1.a",
            "demo.finding.track8.statement-borrowing.s1.b",
        })
        self.assertIn({"role": "computation", "id": generator.LINKER, "version": link_rule["version"]}, before_s1[2])
        self.assertEqual(
            [act["payload"]["finding"]["value"] for act in initial_acts
             if act.get("kind") == "assertion"
             and act.get("payload", {}).get("finding", {}).get("id") in before_s1_pins
             and "statement-borrowing.s1." in act["payload"]["finding"]["id"]],
            [{}, {}],
        )

        after_forward, after_reference = _runner_parity(corrected_acts, surface)
        self.assertEqual(after_forward, after_reference)
        route_s1 = _route_publication(after_forward, generator, "S1")
        route_s2 = _route_publication(after_forward, generator, "S2")
        s1_pins = {pin["id"] for pin in route_s1[2] if pin.get("role") == "input"}
        self.assertEqual(route_s1[1], "1")
        self.assertEqual(s1_pins, {"demo.f1098e.box1.0", "demo.finding.track8.statement-borrowing.s1.b"})
        self.assertNotIn(retracted_finding, s1_pins)
        self.assertEqual(route_s2[1], "1")
        self.assertEqual({pin["id"] for pin in route_s2[2] if pin.get("role") == "input"},
                         {"demo.f1098e.box1.1", "demo.finding.track8.statement-borrowing.s2.a"})
        self.assertIn({"role": "computation", "id": generator.LINKER, "version": link_rule["version"]}, route_s1[2])
        self.assertIn({"role": "computation", "id": generator.LINKER, "version": link_rule["version"]}, route_s2[2])

        saved_before = _saved_prototype_run("before-correction", initial_acts, surface)
        saved_after = _saved_prototype_run("after-correction", corrected_acts, surface)
        before_groups = {group["statementLabel"]["statement"]: group
                         for group in saved_before["calculationView"]["groups"]}
        groups = {group["statementLabel"]["statement"]: group
                  for group in saved_after["calculationView"]["groups"]}
        self.assertEqual(before_groups["S1"]["statementOutcome"]["route"]["value"], "2")
        before_s1_route = before_groups["S1"]["statementOutcome"]["route"]
        self.assertEqual(
            {pin["id"] for pin in before_s1_route["pins"] if pin.get("role") == "input"},
            {"demo.f1098e.box1.0", "demo.finding.track8.statement-borrowing.s1.a",
             "demo.finding.track8.statement-borrowing.s1.b"},
        )
        self.assertIn({"role": "computation", "id": generator.LINKER, "version": link_rule["version"]},
                      before_s1_route["pins"])
        s1, s2 = groups["S1"], groups["S2"]
        s1_route_pins = {pin["id"] for pin in s1["statementOutcome"]["route"]["pins"]
                         if pin.get("role") == "input"}
        s2_route_pins = {pin["id"] for pin in s2["statementOutcome"]["route"]["pins"]
                         if pin.get("role") == "input"}
        self.assertEqual(s1_route_pins, {"demo.f1098e.box1.0", "demo.finding.track8.statement-borrowing.s1.b"})
        self.assertEqual(s2_route_pins, {"demo.f1098e.box1.1", "demo.finding.track8.statement-borrowing.s2.a"})
        self.assertIn("borrowing=demo.track8.borrowing.a", json.dumps(s2))
        self.assertEqual(s1["statementOutcome"]["route"]["value"], "1")
        self.assertEqual(s2["statementOutcome"]["route"]["value"], "1")
        self.assertEqual(s2["value"], "700.0")
        self.assertEqual(before_groups["S2"], s2)
        # These snapshots have a current connection and its input identity,
        # but no schooling record or adopted mixed-period tax result. The
        # route meaning "linked" does not imply a tax classification.

    def test_genuine_silence_differs_from_present_link_without_borrowing_identity(self) -> None:
        generator = _track6b_generator()
        surface, acts, _members = generator._prepare_case("ordinary", ROOT)
        adoption = acts.pop()
        malformed_fact_id = (
            f"{generator.LINKS}|lender=demo.lender.reader.s1,"
            "statement=demo.statement.reader.s1,tax-year=2025"
        )
        acts.append({
            "schema": "act.v1", "act_id": "demo.track8.unresolved-link",
            "actor": generator.USER, "at": "2026-09-28T14:00:00Z",
            "committed_against": len(acts), "kind": "assertion",
            "payload": {"finding": generator._attested(
                "demo.finding.track8.unresolved-link", malformed_fact_id, {})},
        })
        acts.append(adoption)
        acts = generator._renumber(acts)

        schemas = DerivationSchemas()
        resolved = resolve_production_package(
            acts, run_scope=generator.SCOPE, scope_user=generator.USER,
            workspace_revision=len(acts), surface=generator._surface(surface), schemas=schemas,
        )
        self.assertNotIsInstance(resolved, Refusal)
        # Package resolution accepts the graph; kernel projection then
        # rejects a present link without the fact type's required borrowing
        # key. It cannot become a saved unresolved-link disposition.
        with self.assertRaisesRegex(FindingModelError, "finding references unknown fact"):
            project(tuple(dict(act) for act in acts), schemas.registry)

        # In the no-link control the same package runs and records the
        # existing zero-link route, which is genuine silence.
        no_link_surface, no_link_acts, _ = generator._prepare_case("ordinary", ROOT)
        no_link_forward, no_link_reference = _runner_parity(no_link_acts, no_link_surface)
        self.assertEqual(no_link_forward, no_link_reference)
        no_link_route = _route_publication(no_link_forward, generator, "S1")
        self.assertEqual(no_link_route[1], "0")
        self.assertEqual({pin["id"] for pin in no_link_route[2] if pin.get("role") == "input"},
                         {"demo.f1098e.box1.0"})
        silence_model = _saved_prototype_run("genuine-silence", no_link_acts, no_link_surface)
        silence_s1 = next(group for group in silence_model["calculationView"]["groups"]
                          if group["statementLabel"]["statement"] == "S1")
        # The bare route is this prototype reader's no-link route, not a
        # schooling eligibility conclusion or proof of the milestone default.
        self.assertEqual(silence_s1["statementOutcome"]["route"]["interpretation"], "bare")


if __name__ == "__main__":
    unittest.main()
