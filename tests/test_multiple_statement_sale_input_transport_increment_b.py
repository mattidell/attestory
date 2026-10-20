"""Increment B focused tests: per-statement input transport and fail-closed refusal.

Validates:
1. Bounded emission discovery in _resolved_run_material discovers all 16 allowed
   Form 1099-K circumstance and Box 4 inputs into emission_only_names.
2. None of the 16 allowed inputs are placed into collect_names.
3. Fail-closed contract validation: TransportContractError is raised on:
   - Symbol alias (binding symbol != fact_type.id)
   - Binding mode != 'optional_default'
   - Binding fact_type version != 'v1'
   - Fact type declaration identity keys mismatch (not ['payer', 'statement', 'tax-year'])
   - Unpermitted input binding required by a subject-scoped rule
4. live_coordinate_run catches TransportContractError before reservation or execution,
   immediately returning Refusal(reason='TRANSPORT_CONTRACT_ERROR', detail=...).
5. Two sibling statements with different circumstance inputs preserve their own
   keyed inputs in marshaled sources without calculation leakage or cross-statement interference.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping, Sequence
import unittest

from packages.derivation.live import (
    F1099K_ALLOWED_PER_STATEMENT_INPUTS,
    F1099K_BOX1A_SUBJECT_ID,
    F1099K_STATEMENT_IDENTITY_KEYS,
    LiveCoordinatorOutcome,
    TransportContractError,
    _resolved_run_material,
    live_coordinate_run,
)
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.marshal import marshal_live_run_context
from packages.derivation.production_resolver import PublicationSurface, Refusal
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.findings import project
from packages.tax.f1099k_statement_recording import (
    answer_f1099k_statement_answer_durably,
    record_f1099k_statement_durably,
)
from packages.tax.loader import TAX_CONTENT_DIR, tax_registry
from tests.test_f1099k_personal_item_sale_track1 import (
    ROOT,
    SCOPE,
    SURFACE,
    USER,
    _finish_acts,
    _make_base_acts,
)


@dataclass(frozen=True)
class _Graph:
    resolved_members: Sequence[Mapping[str, Any]]
    package: Mapping[str, Any]


class MultipleStatementSaleInputTransportIncrementBTests(unittest.TestCase):
    def setUp(self) -> None:
        self.content_dir = TAX_CONTENT_DIR
        self.pkg_v49 = json.loads(
            (self.content_dir / "package.core-calculations.v49.json").read_text("utf-8")
        )
        corpus: dict[tuple[str, str], dict[str, Any]] = {}
        for path in self.content_dir.glob("*.json"):
            if path.name.startswith(("published-packages", "package.")):
                continue
            try:
                data = json.loads(path.read_text("utf-8"))
                if isinstance(data, dict) and "id" in data and "version" in data:
                    corpus[(data["id"], str(data["version"]))] = data
            except Exception:
                continue
        self.corpus_members = [
            corpus[(pin["id"], str(pin["version"]))]
            for pin in self.pkg_v49.get("members", [])
            if (pin["id"], str(pin["version"])) in corpus
        ]
        self.graph_v49 = _Graph(self.corpus_members, self.pkg_v49)

    def test_conforming_per_statement_input_transport(self) -> None:
        """All 16 allowed inputs are discovered into emission_only and excluded from collect_names."""
        material = _resolved_run_material(self.graph_v49)
        collect_names = material[6]
        emission_only = set(material.emission_only_names)

        # All 16 allowed inputs must be in emission_only
        self.assertTrue(
            F1099K_ALLOWED_PER_STATEMENT_INPUTS.issubset(emission_only),
            f"Missing inputs: {F1099K_ALLOWED_PER_STATEMENT_INPUTS - emission_only}",
        )

        # None of the 16 inputs may be in collect_names
        for sym in F1099K_ALLOWED_PER_STATEMENT_INPUTS:
            self.assertNotIn(sym, collect_names)

    def test_transport_contract_error_on_alias(self) -> None:
        """TransportContractError is raised if an input binding uses an alias."""
        pkg = copy.deepcopy(self.pkg_v49)
        # Point the fact_type id to a different name so symbol != fact_type.id
        for b in pkg["input_bindings"]:
            if b.get("symbol") == "tax.us.2025.f1099k.agreed-item-price":
                b["fact_type"]["id"] = "tax.us.2025.f1099k.aliased-underlying"
                break

        graph = _Graph(self.corpus_members, pkg)
        with self.assertRaises(TransportContractError) as ctx:
            _resolved_run_material(graph)
        self.assertIn("alias", str(ctx.exception))

    def test_transport_contract_error_on_non_v1_version(self) -> None:
        """TransportContractError is raised if an input binding fact_type version is not v1."""
        pkg = copy.deepcopy(self.pkg_v49)
        for b in pkg["input_bindings"]:
            if b.get("symbol") == "tax.us.2025.f1099k.agreed-item-price":
                b["fact_type"]["version"] = "v2"
                break

        graph = _Graph(self.corpus_members, pkg)
        with self.assertRaises(TransportContractError) as ctx:
            _resolved_run_material(graph)
        self.assertIn("version", str(ctx.exception))

    def test_transport_contract_error_on_non_optional_default_mode(self) -> None:
        """TransportContractError is raised if an input binding mode is not optional_default."""
        pkg = copy.deepcopy(self.pkg_v49)
        for b in pkg["input_bindings"]:
            if b.get("symbol") == "tax.us.2025.f1099k.agreed-item-price":
                b["mode"] = "required"
                break

        graph = _Graph(self.corpus_members, pkg)
        with self.assertRaises(TransportContractError) as ctx:
            _resolved_run_material(graph)
        self.assertIn("optional_default", str(ctx.exception))

    def test_transport_contract_error_on_identity_keys_mismatch(self) -> None:
        """TransportContractError is raised if a fact type's identity keys do not match statement keys."""
        members = copy.deepcopy(self.corpus_members)
        for m in members:
            if m.get("schema") in ("bundle.v1", "bundle.v2"):
                for ft in m.get("fact_types", []):
                    if ft.get("id") == "tax.us.2025.f1099k.agreed-item-price":
                        ft["identity_keys"] = [{"name": "payer"}, {"name": "tax-year"}]  # missing statement

        graph = _Graph(members, self.pkg_v49)
        with self.assertRaises(TransportContractError) as ctx:
            _resolved_run_material(graph)
        self.assertIn("identity keys", str(ctx.exception))

    def test_transport_contract_error_on_unpermitted_input_binding(self) -> None:
        """TransportContractError is raised if a subject-scoped rule requires an unpermitted input binding."""
        pkg = copy.deepcopy(self.pkg_v49)
        pkg["input_bindings"].append({
            "symbol": "tax.us.2025.f1099k.unpermitted-input",
            "fact_type": {"id": "tax.us.2025.f1099k.unpermitted-input", "version": "v1"},
            "mode": "optional_default",
        })
        members = copy.deepcopy(self.corpus_members)
        for m in members:
            if m.get("id") == "tax.us.2025.rule.f1099k-expected-box1a-gross-amount":
                m["requires"].append("tax.us.2025.f1099k.unpermitted-input")

        graph = _Graph(members, pkg)
        with self.assertRaises(TransportContractError) as ctx:
            _resolved_run_material(graph)
        self.assertIn("outside allowed per-statement input set", str(ctx.exception))

    def test_live_coordinate_run_catches_transport_contract_error(self) -> None:
        """live_coordinate_run catches TransportContractError and returns Refusal before run reservation."""
        with TemporaryDirectory(prefix="inc-b-coord-") as temp_dir:
            temp_path = Path(temp_dir)
            capability = WorkspaceCapability(temp_path)
            # Use base acts that resolve successfully through resolve_production_package
            acts = _make_base_acts()
            finish_acts = _finish_acts(acts)

            # Patch _resolved_run_material to raise TransportContractError
            from unittest.mock import patch
            with patch(
                "packages.derivation.live._resolved_run_material",
                side_effect=TransportContractError("Simulated contract violation"),
            ):
                outcome = live_coordinate_run(
                    capability,
                    repo_root=ROOT,
                    authoritative_acts=finish_acts,
                    workspace_revision=len(finish_acts),
                    run_scope=SCOPE,
                    scope_user=USER,
                    request={"schema": "run-request.v1"},
                    run_id="test.run.001",
                    governance_pins=[],
                    surface=SURFACE,
                    output_name="test_out.json",
                )

            self.assertIsInstance(outcome, LiveCoordinatorOutcome)
            self.assertIsNotNone(outcome.refusal)
            assert outcome.refusal is not None
            self.assertEqual(outcome.refusal.reason, "TRANSPORT_CONTRACT_ERROR")
            self.assertIn("Simulated contract violation", outcome.refusal.detail)
            self.assertIsNone(outcome.output_path)
            self.assertIsNone(outcome.run_id)

    def test_two_statement_input_isolation_in_run_context(self) -> None:
        """Two statements with different circumstance answers retain distinct keyed sources."""
        registry = tax_registry()
        with TemporaryDirectory(prefix="inc-b-isolation-") as temp_dir:
            log_path = Path(temp_dir) / "workspace"
            log = ActLog(log_path, registry)

            # Statement 1: Box 1a = $500, price = $500
            res1 = record_f1099k_statement_durably(
                log,
                registry,
                submission_id="sub.iso.1",
                payer_id="demo.payer.1",
                payer_label="Payer One",
                statement_ref="stmt.iso.1",
                statement_label="Statement 1",
                box1a=500.0,
                box4=0.0,
                evidence_id="ev.iso.1",
                actor="demo.taxpayer",
                at="2026-04-15T12:00:00Z",
                expected_revision=log.read().revision,
            )

            from packages.tax.f1099k_statement_recording import _find_current_statement_findings
            state1 = project(log.read().acts, registry)
            stmts1 = _find_current_statement_findings(state1)
            stmt1_keys = stmts1[0][2]

            answer_f1099k_statement_answer_durably(
                log,
                registry,
                statement_keys=stmt1_keys,
                question="tax.us.2025.f1099k.agreed-item-price",
                answer=500.0,
                submission_id="sub.ans.1",
                evidence_id="ev.ans.1",
                actor="demo.taxpayer",
                at="2026-04-15T12:01:00Z",
                expected_revision=log.read().revision,
            )

            # Statement 2: Box 1a = $1200, price = $1200
            res2 = record_f1099k_statement_durably(
                log,
                registry,
                submission_id="sub.iso.2",
                payer_id="demo.payer.2",
                payer_label="Payer Two",
                statement_ref="stmt.iso.2",
                statement_label="Statement 2",
                box1a=1200.0,
                box4=0.0,
                evidence_id="ev.iso.2",
                actor="demo.taxpayer",
                at="2026-04-15T12:02:00Z",
                expected_revision=log.read().revision,
            )

            state2 = project(log.read().acts, registry)
            stmts2 = _find_current_statement_findings(state2)
            stmt2_keys = next(keys for _, _, keys in stmts2 if keys["payer"] == "demo.payer.2")

            answer_f1099k_statement_answer_durably(
                log,
                registry,
                statement_keys=stmt2_keys,
                question="tax.us.2025.f1099k.agreed-item-price",
                answer=1200.0,
                submission_id="sub.ans.2",
                evidence_id="ev.ans.2",
                actor="demo.taxpayer",
                at="2026-04-15T12:03:00Z",
                expected_revision=log.read().revision,
            )

            state = project(log.read().acts, registry)
            currency = compute_currency(state)
            material = _resolved_run_material(self.graph_v49)
            rules, parameters, families, mappings, fact_types, bindings, collect_names = material

            schemas = DerivationSchemas()
            context = marshal_live_run_context(
                run_id="run.iso.001",
                state=state,
                currency=currency,
                rules=rules,
                parameters=parameters,
                claim_applicability=[],
                canon=load_canon(schemas),
                adoption_pin={"role": "adoption", "id": self.pkg_v49["id"], "version": self.pkg_v49["version"]},
                governance_pins=[],
                family_declarations=families,
                closure_mappings=mappings,
                fact_types=fact_types,
                input_bindings=bindings,
                collect_source_names=collect_names,
                emission_only_source_names=list(material.emission_only_names),
            )

            # In context._context.sources, inspect agreed-item-price sources
            price_sources = [
                s for s in context._context.sources
                if s.name == "tax.us.2025.f1099k.agreed-item-price"
            ]
            self.assertEqual(len(price_sources), 2)
            prices_by_payer = {dict(s.keys or ())["payer"]: json.loads(s.value) for s in price_sources}
            self.assertEqual(prices_by_payer["demo.payer.1"], 500.0)
            self.assertEqual(prices_by_payer["demo.payer.2"], 1200.0)


if __name__ == "__main__":
    unittest.main()
