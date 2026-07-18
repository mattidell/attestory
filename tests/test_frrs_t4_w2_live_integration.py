"""Track 4: immutable core-v2 closure and capability-gated live integration.

All bodies are synthetic.  These tests never create a real workspace or carry
an external locator: temporary directories receive only the demo analogue.
"""

from __future__ import annotations

import json
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import GuardIntegrityError, WorkspaceCapability, bootstrap_workspace
from packages.derivation.loader import DerivationSchemas
from packages.derivation.loader import load_canon
from packages.derivation.marshal import MarshalledRunContext
from packages.derivation.package_validation import load_published_citizen_checksums, validate_package
from packages.derivation.production_resolver import PublicationSurface, Refusal, ResolvedGraph, resolve_production_package
from packages.derivation.source_authority import ClosureFindingRecord, resolve_closure_admissions
from packages.derivation.runner import InputFinding, RunContext, SourceFact, run
from tools.generate_frrs_t3_fixtures import render_fixture_files
from tools.generate_frrs_t4_content import render


REPO = Path(__file__).resolve().parent.parent
CONTENT = REPO / "packages" / "content" / "tax" / "2025"
T3 = REPO / "packages" / "sample_data" / "frrs_t3"
USER = "demo.user.filer-1"


def _act(name: str) -> dict[str, object]:
    return cast(dict[str, object], json.loads((T3 / "adoptions" / name).read_text("utf-8")))


def _surface(member_dir: Path | None = None) -> PublicationSurface:
    return PublicationSurface(T3 / "publication_surface" / "releases", CONTENT / "published-packages.json", member_dir or CONTENT)


class CoreV2Publication(unittest.TestCase):
    def test_generated_v2_bytes_and_track_three_pins_are_current(self) -> None:
        for relative, expected in render().items():
            self.assertEqual((CONTENT / relative).read_bytes(), expected)
        rendered_t3 = render_fixture_files()
        committed = {path.relative_to(T3).as_posix(): path.read_bytes() for path in T3.rglob("*.json")}
        self.assertEqual(committed, rendered_t3)

    def test_v2_resolves_cleanly_and_v1_remains_historical_hard_gate_refusal(self) -> None:
        clean = resolve_production_package([_act("adopt-core-v2-current.json")], run_scope={"jurisdiction": "us", "year": "2051"}, scope_user=USER, workspace_revision=10, surface=_surface())
        self.assertIsInstance(clean, ResolvedGraph)
        historical = resolve_production_package([_act("adopt-core-current.json")], run_scope={"jurisdiction": "us", "year": "2050"}, scope_user=USER, workspace_revision=10, surface=_surface())
        self.assertIsInstance(historical, Refusal)
        assert isinstance(historical, Refusal)
        self.assertEqual(historical.reason, "HARD_GATE_REFUSED")
        self.assertEqual(len(historical.issues), 8)

    def test_v2_validator_has_no_issue_allowlist(self) -> None:
        package = json.loads((CONTENT / "package.core-calculations.v2.json").read_text())
        corpus = {}
        for path in CONTENT.glob("*.json"):
            body = json.loads(path.read_text())
            if "id" in body:
                corpus[(body["id"], body.get("version", "v1"))] = body
        validation = validate_package(package, corpus, DerivationSchemas(), load_published_citizen_checksums(CONTENT / "published-packages.json"))
        self.assertTrue(validation.ok)
        self.assertEqual(validation.issues, ())


class W2Closure(unittest.TestCase):
    def setUp(self) -> None:
        self.family = json.loads((CONTENT / "family.w2.v2.json").read_text())
        self.mapping = json.loads((CONTENT / "closure-mapping.w2.v2.json").read_text())

    def _admission(self, records: list[ClosureFindingRecord]) -> bool:
        return self.family["id"] in resolve_closure_admissions([self.mapping], [self.family], records, {self.family["id"]: "demo.w2.h0"})

    def test_literal_true_single_current_closure_is_the_only_empty_set_authority(self) -> None:
        self.assertTrue(self._admission([ClosureFindingRecord("demo.w2.closed", "tax.us.2025.w2.source-closure", "demo.w2.h0", True)]))
        for records in (
            [],
            [ClosureFindingRecord("demo.w2.false", "tax.us.2025.w2.source-closure", "demo.w2.h0", False)],
            [ClosureFindingRecord("demo.w2.displaced", "tax.us.2025.w2.source-closure", "demo.w2.old", True)],
            [ClosureFindingRecord("demo.w2.truthy", "tax.us.2025.w2.source-closure", "demo.w2.h0", "true")],
            [ClosureFindingRecord("demo.w2.a", "tax.us.2025.w2.source-closure", "demo.w2.h0", True), ClosureFindingRecord("demo.w2.b", "tax.us.2025.w2.source-closure", "demo.w2.h0", True)],
        ):
            with self.subTest(records=records):
                self.assertFalse(self._admission(list(records)))

    def test_present_wages_aggregate_without_closure_and_empty_true_closure_zeros(self) -> None:
        rule = json.loads((CONTENT / "rule.wages-line1a.v2.json").read_text())
        schemas = DerivationSchemas()
        def context(sources: list[SourceFact], findings: list[ClosureFindingRecord] | None = None) -> RunContext:
            return RunContext(
                run_id="demo.w2.closure", rules=[rule], parameters={}, canon=load_canon(schemas),
                inputs=[InputFinding("rounding.convention", "half_up", "demo.round", "input")], sources=sources,
                adoption_pin={"role": "adoption", "id": "tax.us.2025.package.core-calculations", "version": "v2"},
                governance_pins=[], family_declarations=[self.family], closure_mappings=[self.mapping],
                closure_findings=list(findings or []), current_horizons={self.family["id"]: "demo.w2.h0"},
            )
        present = run(context([SourceFact("tax.us.2025.w2.box1-wages", "12.5", "demo.w2.present")]), schemas)
        self.assertEqual(present.symbols["tax.us.2025.wages.total-w2-box1"], 13)
        zero = run(context([], [ClosureFindingRecord("demo.w2.closed", "tax.us.2025.w2.source-closure", "demo.w2.h0", True)]), schemas)
        self.assertEqual(zero.symbols["tax.us.2025.wages.total-w2-box1"], 0)


class LiveCoordinator(unittest.TestCase):
    def test_refusal_writes_no_run_record(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = live_coordinate_run(WorkspaceCapability(root / "L"), repo_root=REPO, authoritative_acts=[], workspace_revision=10, run_scope={"jurisdiction": "us", "year": "2051"}, scope_user=USER, request={"schema": "run-request.v1"}, run_id="demo.t4.refusal", governance_pins=[], surface=_surface(), output_name="refusal.json")
            self.assertIsInstance(result.refusal, Refusal)
            self.assertFalse((root / "L" / "records").exists())
            self.assertFalse((root / "L" / "outputs").exists())

    def test_resolved_run_writes_only_paired_records_and_declared_output_below_l(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = live_coordinate_run(WorkspaceCapability(root / "L"), repo_root=REPO, authoritative_acts=[_act("adopt-core-v2-current.json")], workspace_revision=10, run_scope={"jurisdiction": "us", "year": "2051"}, scope_user=USER, request={"schema": "run-request.v1"}, run_id="demo.t4.synthetic", governance_pins=[], surface=_surface(), output_name="demo.json")
            self.assertIsNone(result.refusal)
            assert result.output_path is not None
            self.assertTrue(result.output_path.is_file())
            records = (root / "L" / "records" / "derivation_records.jsonl").read_text().splitlines()
            self.assertEqual(len(records), 2)
            self.assertEqual({json.loads(line)["phase"] for line in records}, {"started", "completed"})
            self.assertEqual(sorted(path.relative_to(root / "L").as_posix() for path in (root / "L").rglob("*") if path.is_file()), ["outputs/demo.json", "records/derivation_records.jsonl"])

    def test_marshaled_token_and_uninstalled_transport_cannot_be_forged(self) -> None:
        with self.assertRaises(TypeError):
            MarshalledRunContext(None, object())  # type: ignore[arg-type]
        with TemporaryDirectory() as tmp:
            workspace = bootstrap_workspace(WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO)
            with self.assertRaises(GuardIntegrityError):
                workspace.guarded_push(object(), [])  # type: ignore[arg-type]
            guard = workspace.install_envelope_guards()
            workspace.guarded_commit(guard, [])
            workspace.guarded_push(guard, [])


class ResolverCounterProbes(unittest.TestCase):
    def test_member_substitution_has_exact_refusal_and_layout_is_inert(self) -> None:
        with TemporaryDirectory() as tmp:
            content = Path(tmp) / "content"
            shutil.copytree(CONTENT, content)
            rule = next(content.glob("rule.*.json"))
            body = json.loads(rule.read_text())
            body["_tamper"] = True
            rule.write_text(json.dumps(body, sort_keys=True) + "\n")
            refusal = resolve_production_package([_act("adopt-interest-v2-current.json")], run_scope={"jurisdiction": "us", "year": "2025"}, scope_user=USER, workspace_revision=10, surface=_surface(content))
            self.assertIsInstance(refusal, Refusal)
            assert isinstance(refusal, Refusal)
            self.assertEqual(refusal.reason, "MEMBER_ABSENT_OR_MISMATCH")
