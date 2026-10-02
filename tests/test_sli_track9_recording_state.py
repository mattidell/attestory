"""Track 9 test-only account prototype for unresolved SLI relationships.

This is an experimental answer mapper, not a production schooling or financing
producer. It probes whether an addressable account with explicit knownness can
survive existing contribution admission and act-log recovery without putting a
borrower into its identity.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas, workspace_registry
from packages.derivation.presentation_projection import PresentationModelError
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.act_log import ActLog
from packages.kernel.contribution import apply_contribution_batch
from packages.kernel.currency import compute_currency
from packages.kernel.findings import project
from tests.support import act, demo_entity, demo_evidence


ACCOUNT_TYPE = "demo.sli.relationship-account"
ACCOUNT_ID = "demo.sli.account.unresolved-a"
EVIDENCE_ID = "demo.evidence.sli.account-a"
CONTRIBUTION_ID = "demo.contribution.sli.account-a"
FINDING_ID = "demo.finding.sli.account-a"


def _fact_type() -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": ACCOUNT_TYPE,
        "version": "v1",
        "title": "Synthetic SLI relationship account (prototype only)",
        "nature": "determinable",
        "identity_keys": [
            {"name": "account", "kind": "entity", "entity_kind": "demo.sli-relationship-account"},
            {"name": "tax-year", "kind": "literal", "values": ["2025"]},
        ],
        "value_schema": {
            "type": "object",
            "properties": {
                "borrowing_identity": {"enum": ["unknown", "known"]},
                "schooling_fact": {"enum": ["missing", "supplied"]},
                "statement_scope": {"enum": ["unknown", "known", "not-applicable"]},
                "supplied_claim": {"type": "string"},
                "borrowing_reference": {"type": ["string", "null"]},
                "schooling_reference": {"type": ["string", "null"]},
                "statement_reference": {"type": ["string", "null"]},
            },
            "required": ["borrowing_identity", "schooling_fact", "statement_scope", "supplied_claim",
                         "borrowing_reference", "schooling_reference", "statement_reference"],
            "additionalProperties": False,
        },
        "supersession": {"policy": "free"},
    }


def _fact_id() -> str:
    return f"{ACCOUNT_TYPE}|account={ACCOUNT_ID},tax-year=2025"


def _map_test_answer(answer: dict[str, Any]) -> dict[str, Any]:
    """Minimal test-only ordinary-answer mapping; no product recorder exists."""
    return {
        "borrowing_identity": answer["borrowing_identity"],
        "schooling_fact": answer["schooling_fact"],
        "statement_scope": answer["statement_scope"],
        "supplied_claim": answer["supplied_claim"],
        "borrowing_reference": answer["borrowing_reference"],
        "schooling_reference": answer["schooling_reference"],
        "statement_reference": answer["statement_reference"],
    }


def _finding(finding_id: str, contribution_id: str, value: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": _fact_id(),
        "value": value,
        "basis": "attested",
        "evidence_ids": [EVIDENCE_ID],
        "contribution_id": contribution_id,
    }


def _append_account_answer(generator: Any, acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Append one synthetic unresolved account before the current adoption."""
    package_adoption = acts.pop()
    acts.extend([
        act(len(acts), "bundle-adoption", {"bundle": {
            "schema": "bundle.v2", "id": "demo.sli.track9.account-vocabulary", "version": "v1",
            "label": "Synthetic Track 9 relationship account declaration", "fact_types": [_fact_type()],
        }}),
        act(len(acts) + 1, "entity-introduced", {"entity": demo_entity(
            ACCOUNT_ID, "Synthetic account address", "demo.sli-relationship-account"
        )}),
        act(len(acts) + 2, "evidence-submitted", {"evidence": demo_evidence(
            EVIDENCE_ID, "Synthetic unresolved account answer", {"claim": "unknown connection"}
        )}),
        act(len(acts) + 3, "contribution", {"contribution": {
            "schema": "contribution.v1", "id": CONTRIBUTION_ID, "evidence_id": EVIDENCE_ID,
            "content": {"mode": "manual-entry", "synthetic": True},
        }}),
    ])
    value = _map_test_answer({
        "borrowing_identity": "unknown", "schooling_fact": "missing", "statement_scope": "unknown",
        "supplied_claim": "synthetic answer supplied; connection not identified",
        "borrowing_reference": None, "schooling_reference": None, "statement_reference": None,
    })
    acts.append(act(len(acts), "assertion", {"finding": _finding(FINDING_ID, CONTRIBUTION_ID, value)}))
    package_adoption["committed_against"] = len(acts)
    acts.append(package_adoption)
    return cast(list[dict[str, Any]], generator._renumber(acts))


class UnresolvedAccountRecovery(unittest.TestCase):
    def test_unknown_referents_remain_a_current_addressable_account_after_reopen(self) -> None:
        with tempfile.TemporaryDirectory(prefix="track9-account-") as directory:
            root = Path(directory)
            schemas = DerivationSchemas()
            registry = workspace_registry()
            acts = [
                act(0, "bundle-adoption", {"bundle": {
                    "schema": "bundle.v2",
                    "id": "demo.sli.relationship-prototype",
                    "version": "v1",
                    "label": "Synthetic test-only relationship account declarations",
                    "fact_types": [_fact_type()],
                }}),
                act(1, "entity-introduced", {"entity": demo_entity(
                    ACCOUNT_ID, "Synthetic account address", "demo.sli-relationship-account"
                )}),
                act(2, "evidence-submitted", {"evidence": demo_evidence(
                    EVIDENCE_ID, "Synthetic unresolved relationship answer", {"claim": "unknown connection"}
                )}),
            ]
            base = project(tuple(acts), schemas.registry)
            contribution_act = act(3, "contribution", {"contribution": {
                "schema": "contribution.v1",
                "id": CONTRIBUTION_ID,
                "evidence_id": EVIDENCE_ID,
                "content": {"mode": "manual-entry", "synthetic": True},
            }})
            ordinary_answer = {
                "borrowing_identity": "unknown",
                "schooling_fact": "missing",
                "statement_scope": "unknown",
                "supplied_claim": "synthetic answer supplied; connection not identified",
                "borrowing_reference": None,
                "schooling_reference": None,
                "statement_reference": None,
            }
            value = _map_test_answer(ordinary_answer)
            assertion = act(4, "assertion", {"finding": _finding(FINDING_ID, CONTRIBUTION_ID, value)})
            admitted = apply_contribution_batch(
                base,
                contribution_act=contribution_act,
                successor_acts=[assertion],
                registry=schemas.registry,
                record_id="demo.contribution-record.sli.account-a",
            )
            self.assertEqual(admitted.terminal_record["phase"], "completed")
            self.assertEqual(admitted.asserted[0]["fact_id"], _fact_id())

            log = ActLog(root / "workspace", registry)
            for item in [*acts, contribution_act, assertion]:
                log.append(item, expected_revision=item["committed_against"])
            recovered_acts = ActLog(root / "workspace", workspace_registry()).read().acts
            self.assertEqual(len(recovered_acts), 5)
            # Recovery uses a fresh registry/projection and only the reopened
            # act log, not the contribution result or original value object.
            reopened_schemas = DerivationSchemas()
            recovered = project(recovered_acts, reopened_schemas.registry)
            currency = compute_currency(recovered)
            current = recovered.findings[FINDING_ID]
            self.assertIn(FINDING_ID, currency.current_finding_ids)
            self.assertEqual(current["fact_id"], _fact_id())
            self.assertEqual(current["value"], value)
            self.assertNotIn("borrowing", current["fact_id"])
            self.assertIsNone(current["value"]["borrowing_reference"])
            self.assertEqual(current["evidence_ids"], [EVIDENCE_ID])

    def test_account_reference_reaches_neutral_consumer_and_writer_records_disposition(self) -> None:
        """Exercise one neutral account output through package admission and recovery.

        The temporary v12 rule reads one declared status field from the account
        subject. Both runners compute it and the durable run records its exact
        source pin. The standard saved presentation does not copy this unbound
        neutral publication's value; no real-world join or tax consequence is
        established.
        """
        repo_root = Path(__file__).resolve().parent.parent
        output_root = repo_root / "temp" / "track9"
        output_root.mkdir(parents=True, exist_ok=True)
        harness = repo_root / "tools" / "presentation_harness" / "examples" / "generate_track6b_saved_presentations.py"
        spec = importlib.util.spec_from_file_location("track9_disposable_reader", harness)
        self.assertIsNotNone(spec)
        assert spec is not None and spec.loader is not None
        generator = cast(Any, importlib.util.module_from_spec(spec))
        sys.modules[spec.name] = generator
        spec.loader.exec_module(generator)

        original_members = generator._package_members
        original_seal = generator._seal_disposable_reader_package
        account_bundle = {
            "schema": "bundle.v2",
            "id": "demo.sli.track9.account-vocabulary",
            "version": "v1",
            "label": "Synthetic Track 9 relationship account declaration",
            "fact_types": [_fact_type()],
        }
        account_rule = generator._reader_rule(
            "demo.rule.sli.track9.account-state",
            "demo.sli.track9.account-evidence",
            subject=ACCOUNT_TYPE,
            value={"op": "ref", "name": ACCOUNT_TYPE, "field": "borrowing_identity"},
        )
        def extended_members() -> tuple[list[tuple[dict[str, Any], str]], list[dict[str, str]]]:
            members, entrypoints = original_members()
            members.extend(((account_bundle, "fact-type-bundle"), (account_rule, "computation")))
            entrypoints.extend({"id": citizen["id"], "version": citizen["version"]} for citizen, _ in members[-2:])
            return members, entrypoints

        def seal_with_account_binding(surface: Any) -> Any:
            package_path = surface.members / generator.PACKAGE_FILE
            package = json.loads(package_path.read_text("utf-8"))
            package["input_bindings"].append({
                "symbol": ACCOUNT_TYPE,
                "fact_type": {"id": ACCOUNT_TYPE, "version": "v1"},
                "mode": "required",
            })
            package_path.write_bytes(generator._bytes(package))
            return original_seal(surface)

        generator._package_members = extended_members
        generator._seal_disposable_reader_package = seal_with_account_binding
        try:
            surface, acts, _resolved = generator._prepare_case("ordinary", output_root)
        finally:
            generator._package_members = original_members
            generator._seal_disposable_reader_package = original_seal

        acts = _append_account_answer(generator, acts)
        surface_view = PublicationSurface(surface.releases, surface.members / generator.REGISTRY_FILE, surface.members)

        with tempfile.TemporaryDirectory(prefix="track9-saved-workspace-") as raw_workspace:
            workspace = Path(raw_workspace)
            log = ActLog(workspace / "authoritative", workspace_registry())
            for item in acts:
                log.append(item, expected_revision=item["committed_against"])
            reopened_log = ActLog(workspace / "authoritative", workspace_registry())
            recovered_acts = reopened_log.read().acts
            # The Track 8 helper drives the same byte-verified package
            # resolver, marshaller, and both runners from reopened acts.
            from tests.test_sli_track8_relationship_evidence import _runner_parity

            forward, reference = _runner_parity(list(recovered_acts), surface)
            self.assertEqual(forward, reference)
            exact_symbol = f"demo.sli.track9.account-evidence|{_fact_id()}"
            account_publication = next(row for row in forward["publications"] if row[0] == exact_symbol)
            self.assertEqual(account_publication[1], "unknown")
            account_input_pins = {pin["id"] for pin in account_publication[2] if pin.get("role") == "input"}
            self.assertEqual(account_input_pins, {FINDING_ID})
            self.assertIn({"id": account_rule["id"], "role": "computation", "version": account_rule["version"]}, account_publication[2])
            # The live consumer receives only the persisted/reopened acts.
            result = live_coordinate_run(
                WorkspaceCapability(workspace / "live"), repo_root=repo_root,
                authoritative_acts=recovered_acts, workspace_revision=len(recovered_acts),
                run_scope={"jurisdiction": "us", "year": "2025"}, scope_user=generator.USER,
                request={"schema": "run-request.v1"}, run_id="demo.track9.account-saved-reader",
                governance_pins=[], surface=surface_view, output_name="account.json",
            )
            self.assertIsNone(result.refusal)
            self.assertIsNotNone(result.presentation_path)
            self.assertIsNotNone(result.output_path)
            live_publications = result.publications
            assert live_publications is not None
            live_account_finding = next(
                publication.finding for publication in live_publications
                if publication.finding.get("symbol") == exact_symbol
            )
            self.assertEqual(live_account_finding["value"], "unknown")
            self.assertIn({"id": account_rule["id"], "role": "computation", "version": account_rule["version"]}, live_account_finding["pins"])
            saved_path = output_root / "account-neutral-reader.presentation.json"
            result_path = output_root / "account-neutral-reader.result.json"
            assert result.presentation_path is not None
            saved_path.write_bytes(result.presentation_path.read_bytes())
            assert result.output_path is not None
            result_path.write_bytes(result.output_path.read_bytes())
            del result, live_publications, recovered_acts, log, reopened_log, forward, reference, account_publication
            del account_input_pins, live_account_finding, acts

        saved = json.loads(saved_path.read_text("utf-8"))
        run_record = json.loads(result_path.read_text("utf-8"))
        saved_disposition = next(row for row in run_record["dispositions"] if row.get("artifact_id") == account_rule["id"])
        self.assertEqual(saved_disposition["disposition"], "published")
        self.assertEqual(saved_disposition["symbol"], f"demo.sli.track9.account-evidence|{_fact_id()}")
        self.assertIn({"id": FINDING_ID, "origin": "assertion", "role": "input", "version": "v1"}, saved_disposition["pins"])
        self.assertNotIn("value", saved_disposition)
        self.assertFalse(any("demo.sli.track9.account-evidence" in json.dumps(section) for section in saved["sections"]))

    def test_field_binding_attempts_retain_exact_suffix_and_base_failures(self) -> None:
        """Record the two attempted field-binding routes for this subject rule."""
        repo_root = Path(__file__).resolve().parent.parent
        output_root = repo_root / "temp" / "track9" / "field-binding-attempts"
        harness = repo_root / "tools" / "presentation_harness" / "examples" / "generate_track6b_saved_presentations.py"

        def build_generator(name: str) -> Any:
            spec = importlib.util.spec_from_file_location(name, harness)
            assert spec is not None and spec.loader is not None
            module = cast(Any, importlib.util.module_from_spec(spec))
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            return module

        for binding_kind in ("suffixed", "base"):
            with self.subTest(binding_kind=binding_kind):
                generator = build_generator(f"track9_field_binding_{binding_kind}")
                original_members = generator._package_members
                original_seal = generator._seal_disposable_reader_package
                account_bundle = {
                    "schema": "bundle.v2", "id": "demo.sli.track9.account-vocabulary", "version": "v1",
                    "label": "Synthetic Track 9 relationship account declaration", "fact_types": [_fact_type()],
                }
                account_rule = generator._reader_rule(
                    "demo.rule.sli.track9.account-state", "demo.sli.track9.account-evidence",
                    subject=ACCOUNT_TYPE,
                    value={"op": "ref", "name": ACCOUNT_TYPE, "field": "borrowing_identity"},
                )
                field = {
                    "schema": "form-field.v2", "id": "demo.sli.track9.account-state-field", "version": "v1",
                    "form": {"authority": "demo", "form_id": "relationship-prototype", "tax_year": 2025, "jurisdiction": "demo"},
                    "line": "account-state", "label": "Synthetic account state",
                    "description": "Test-only neutral field binding probe.",
                    "binds_symbol": (
                        f"demo.sli.track9.account-evidence|{_fact_id()}"
                        if binding_kind == "suffixed" else "demo.sli.track9.account-evidence"
                    ),
                    "dispositions": {
                        "published_value": {"render": "unknown", "explain": "Synthetic status."},
                        "computed_zero": {"render": "0", "explain": "No amount."},
                        "closure_backed_zero": {"render": "0", "explain": "No amount."},
                        "blocked": {"render": "", "explain": "No status.", "codes": ["DEPENDENCY_ABSENT", "DEPENDENCY_INVALID"]},
                        "guard_inapplicable": {"render": "", "explain": "Neutral rule inapplicable."},
                    },
                }

                def extended_members() -> tuple[list[tuple[dict[str, Any], str]], list[dict[str, str]]]:
                    members, entrypoints = original_members()
                    members.extend(((account_bundle, "fact-type-bundle"), (account_rule, "computation"), (field, "form-field")))
                    entrypoints.extend({"id": citizen["id"], "version": citizen["version"]} for citizen, _ in members[-3:])
                    return members, entrypoints

                def seal_with_account_binding(surface: Any) -> Any:
                    package_path = surface.members / generator.PACKAGE_FILE
                    package = json.loads(package_path.read_text("utf-8"))
                    package["input_bindings"].append({
                        "symbol": ACCOUNT_TYPE, "fact_type": {"id": ACCOUNT_TYPE, "version": "v1"}, "mode": "required",
                    })
                    package_path.write_bytes(generator._bytes(package))
                    return original_seal(surface)

                generator._package_members = extended_members
                generator._seal_disposable_reader_package = seal_with_account_binding
                try:
                    variant_root = output_root / binding_kind
                    variant_root.mkdir(parents=True, exist_ok=True)
                    surface, acts, _resolved = generator._prepare_case("ordinary", variant_root)
                except RuntimeError as exc:
                    self.assertEqual(binding_kind, "suffixed")
                    self.assertIn("FORM_FIELD_BINDING_MISSING", str(exc))
                    self.assertIn(field["binds_symbol"], str(exc))
                    continue
                finally:
                    generator._package_members = original_members
                    generator._seal_disposable_reader_package = original_seal

                self.assertEqual(binding_kind, "base")
                acts = _append_account_answer(generator, acts)
                surface_view = PublicationSurface(surface.releases, surface.members / generator.REGISTRY_FILE, surface.members)
                with tempfile.TemporaryDirectory(prefix="track9-field-base-workspace-") as raw:
                    with self.assertRaises(PresentationModelError) as raised:
                        live_coordinate_run(
                            WorkspaceCapability(Path(raw) / "live"), repo_root=repo_root,
                            authoritative_acts=acts, workspace_revision=len(acts),
                            run_scope={"jurisdiction": "us", "year": "2025"}, scope_user=generator.USER,
                            request={"schema": "run-request.v1"}, run_id="demo.track9.account.base-field-attempt",
                            governance_pins=[], surface=surface_view, output_name="base-field.json",
                        )
                self.assertIn("missing or ambiguous disposition join", str(raised.exception))
                self.assertIn("'demo.sli.track9.account-evidence': 0 row(s)", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
