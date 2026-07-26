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
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import GuardIntegrityError, InstalledEnvelopeGuards, ResidencyViolation, WorkspaceCapability, bootstrap_workspace
from packages.derivation.loader import DerivationSchemas
from packages.derivation.loader import load_canon
from packages.derivation.marshal import MarshalledRunContext
from packages.derivation.package_validation import load_published_citizen_checksums, validate_package
from packages.derivation.production_resolver import PublicationSurface, Refusal, ResolvedGraph, resolve_production_package
from packages.derivation.source_authority import ClosureFindingRecord, resolve_closure_admissions
from packages.derivation.runner import InputFinding, RunContext, SourceFact, run
from packages.kernel.findings import FindingModelError, project
from packages.tax.loader import load_closure_mappings
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


def _live_act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.live.act.{index:03d}",
        "kind": kind,
        "actor": USER,
        "at": f"2026-07-18T00:00:{index:02d}Z",
        "committed_against": index,
        "payload": payload,
    }


def _attested_finding(finding_id: str, fact_id: str, value: object) -> dict[str, object]:
    return {
        "schema": "finding.v1",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "attested",
        "evidence_ids": [],
    }


def _v3_authoritative_acts(*, with_w2_member: bool = True) -> list[dict[str, object]]:
    """A complete synthetic live record: facts, horizons, closures, adoption."""
    acts: list[dict[str, object]] = []

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_live_act(len(acts), kind, payload))

    for name in (
        "w2.bundle.v3.json",
        "f1099int.bundle.json",
        "interest_composition.bundle.json",
        "core_calculations.bundle.v2.json",
    ):
        add("bundle-adoption", {"bundle": json.loads((CONTENT / name).read_text())})

    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.live.employer", "kind": "tax.us.employer", "label": "Synthetic employer"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.live.w2", "kind": "tax.us.w2-slip", "label": "Synthetic W-2 slip"}})

    scope = {"tax-year": "2025", "subject": "demo.primary"}
    families = (
        ("tax.us.2025.w2", "v2", "demo.live.w2.h0"),
        ("tax.us.2025.f1099int.b1", "v1", "demo.live.int-b1.h0"),
        ("tax.us.2025.f1099int.b3", "v1", "demo.live.int-b3.h0"),
        ("tax.us.2025.f1099oid.b1", "v1", "demo.live.oid-b1.h0"),
        ("tax.us.2025.non-form-interest", "v1", "demo.live.nonform.h0"),
    )
    for family_id, version, horizon_id in families:
        add("horizon-genesis", {"family": {"id": family_id, "version": version}, "scope": scope, "horizon_id": horizon_id})

    if with_w2_member:
        evidence_id = "demo.live.evidence.w2"
        contribution_id = "demo.live.contribution.w2"
        add("evidence-submitted", {"evidence": {"schema": "evidence.v1", "id": evidence_id, "kind": "demo.statement", "label": "Synthetic W-2", "content": {"box1": 100}}})
        add("contribution", {"contribution": {"schema": "contribution.v1", "id": contribution_id, "evidence_id": evidence_id, "content": {"mode": "manual-entry", "synthetic": True}}})
        add("member-transition", {
            "family": {"id": "tax.us.2025.w2", "version": "v2"},
            "scope": scope,
            "member": {"action": "assert", "finding": {
                "schema": "finding.v2", "id": "demo.live.finding.w2", "fact_id": "tax.us.2025.w2.box1-wages|employer=demo.live.employer,w2-slip=demo.live.w2,tax-year=2025", "value": 100, "basis": "documentary", "evidence_ids": [evidence_id], "contribution_id": contribution_id,
            }},
            "successor": {"id": "demo.live.w2.h1", "predecessor": "demo.live.w2.h0"},
        })

    add("assertion", {"finding": _attested_finding("demo.live.finding.rounding", "rounding.convention|tax-year=2025", "half_up")})
    add("assertion", {"finding": _attested_finding("demo.live.finding.status", "tax.us.2025.filing-status|tax-year=2025", "single")})
    for finding_id, fact_type, horizon_id in (
        ("demo.live.closure.w2", "tax.us.2025.w2.source-closure", "demo.live.w2.h1" if with_w2_member else "demo.live.w2.h0"),
        ("demo.live.closure.int-b1", "tax.us.2025.f1099int.b1.source-closure", "demo.live.int-b1.h0"),
        ("demo.live.closure.int-b3", "tax.us.2025.f1099int.b3.source-closure", "demo.live.int-b3.h0"),
        ("demo.live.closure.oid-b1", "tax.us.2025.f1099oid.b1.source-closure", "demo.live.oid-b1.h0"),
        ("demo.live.closure.nonform", "tax.us.2025.non-form-interest.source-closure", "demo.live.nonform.h0"),
    ):
        add("assertion", {"finding": _attested_finding(finding_id, f"{fact_type}|family-horizon={horizon_id},tax-year=2025", True)})

    adoption = _act("adopt-core-v3-current.json")
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts


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

    def test_v3_repairs_live_input_and_w2_closure_without_rewriting_v2(self) -> None:
        package = json.loads((CONTENT / "package.core-calculations.v3.json").read_text())
        corpus = {
            (body["id"], body.get("version", "v1")): body
            for path in CONTENT.glob("*.json")
            if isinstance((body := json.loads(path.read_text())), dict) and "id" in body
        }
        validation = validate_package(package, corpus, DerivationSchemas(), load_published_citizen_checksums(CONTENT / "published-packages.json"))
        self.assertTrue(validation.ok, validation.issues)
        rounding = next(fact for fact in json.loads((CONTENT / "core_calculations.bundle.v2.json").read_text())["fact_types"] if fact["id"] == "rounding.convention")
        self.assertEqual(rounding["value_schema"], {"enum": ["half_up"]})
        closure = next(fact for fact in json.loads((CONTENT / "w2.bundle.v3.json").read_text())["fact_types"] if fact["id"] == "tax.us.2025.w2.source-closure")
        self.assertEqual(closure["identity_keys"][0]["name"], "family-horizon")
        self.assertEqual(load_closure_mappings()["tax.us.2025.closure-mapping.w2"]["version"], "v3")


class W2Closure(unittest.TestCase):
    def setUp(self) -> None:
        self.family = json.loads((CONTENT / "family.w2.v2.json").read_text())
        self.mapping = json.loads((CONTENT / "closure-mapping.w2.v3.json").read_text())

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

    def test_w2_and_taxable_interest_have_distinct_declared_quantities(self) -> None:
        w2 = next(fact for fact in json.loads((CONTENT / "w2.bundle.v2.json").read_text())["fact_types"] if fact["id"] == "tax.us.2025.w2.box1-wages")
        interest = next(fact for fact in json.loads((CONTENT / "f1099int.bundle.json").read_text())["fact_types"] if fact["id"] == "tax.us.2025.f1099int.box1-interest")
        self.assertEqual(w2["quantity"], {"id": "tax.us.2025.quantity.wages", "version": "v1"})
        self.assertNotEqual(w2["quantity"], interest["quantity"])

    def test_v2_w2_closure_with_a_horizon_is_the_former_unknown_fact_rejection(self) -> None:
        acts = [
            _live_act(0, "bundle-adoption", {"bundle": json.loads((CONTENT / "w2.bundle.v2.json").read_text())}),
            _live_act(1, "horizon-genesis", {"family": {"id": "tax.us.2025.w2", "version": "v2"}, "scope": {"tax-year": "2025"}, "horizon_id": "demo.v2.w2.h0"}),
            _live_act(2, "assertion", {"finding": _attested_finding("demo.v2.w2.closure", "tax.us.2025.w2.source-closure|family-horizon=demo.v2.w2.h0,tax-year=2025", True)}),
        ]
        with self.assertRaisesRegex(FindingModelError, "unknown fact"):
            project(tuple(acts), DerivationSchemas().registry)


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
            self.assertEqual(
                sorted(path.relative_to(root / "L").as_posix() for path in (root / "L").rglob("*") if path.is_file()),
                [
                    ".residency-envelope-gates/commit.gate",
                    ".residency-envelope-gates/manifest.json",
                    ".residency-envelope-gates/push.gate",
                    "outputs/demo.json",
                    "outputs/demo.presentation.json",
                    "records/derivation_records.jsonl",
                ],
            )

    def test_v3_live_path_publishes_all_covered_lines_from_recorded_facts(self) -> None:
        acts = _v3_authoritative_acts()
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = live_coordinate_run(WorkspaceCapability(root / "L"), repo_root=REPO, authoritative_acts=acts, workspace_revision=len(acts), run_scope={"jurisdiction": "us", "year": "2052"}, scope_user=USER, request={"schema": "run-request.v1"}, run_id="demo.t4c.v3", governance_pins=[], surface=_surface(), output_name="v3.json")
            self.assertIsNone(result.refusal)
            assert result.output_path is not None
            report = json.loads(result.output_path.read_text())
            published = {row["symbol"] for row in report["dispositions"] if row["disposition"] == "published"}
            graph = resolve_production_package(acts, run_scope={"jurisdiction": "us", "year": "2052"}, scope_user=USER, workspace_revision=len(acts), surface=_surface())
            self.assertIsInstance(graph, ResolvedGraph)
            assert isinstance(graph, ResolvedGraph)
            fields = {
                member["id"]: member["binds_symbol"]
                for member in graph.resolved_members
                if member.get("schema") == "form-field.v2"
            }
            for field_id in (
                "tax.us.2025.form1040.line-1a",
                "tax.us.2025.form1040.line-2b",
                "tax.us.2025.form1040.line-9",
                "tax.us.2025.form1040.line-11",
                "tax.us.2025.form1040.line-12",
                "tax.us.2025.form1040.line-15",
                "tax.us.2025.form1040.line-16",
            ):
                self.assertIn(fields[field_id], published)
            records = (root / "L" / "records" / "derivation_records.jsonl").read_text().splitlines()
            self.assertEqual([json.loads(line)["phase"] for line in records], ["started", "completed"])

    def test_v3_without_rounding_preserves_the_named_dependency_block(self) -> None:
        acts = [
            act for act in _v3_authoritative_acts()
            if not (
                act["kind"] == "assertion"
                and act["payload"]["finding"]["fact_id"] == "rounding.convention|tax-year=2025"  # type: ignore[index]
            )
        ]
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = live_coordinate_run(WorkspaceCapability(root / "L"), repo_root=REPO, authoritative_acts=acts, workspace_revision=len(acts), run_scope={"jurisdiction": "us", "year": "2052"}, scope_user=USER, request={"schema": "run-request.v1"}, run_id="demo.t4c.no-rounding", governance_pins=[], surface=_surface(), output_name="no-rounding.json")
            self.assertIsNone(result.refusal)
            assert result.output_path is not None
            report = json.loads(result.output_path.read_text())
            wage_disposition = next(row for row in report["dispositions"] if row["artifact_id"] == "tax.us.2025.rule.w2-box1-to-line1a")
            self.assertEqual(wage_disposition["disposition"], "blocked")
            self.assertEqual(wage_disposition["code"], "DEPENDENCY_ABSENT")
            self.assertEqual(wage_disposition["missing"], ["rounding.convention"])

    def test_v3_empty_w2_family_publishes_through_its_recorded_closure(self) -> None:
        acts = _v3_authoritative_acts(with_w2_member=False)
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = live_coordinate_run(WorkspaceCapability(root / "L"), repo_root=REPO, authoritative_acts=acts, workspace_revision=len(acts), run_scope={"jurisdiction": "us", "year": "2052"}, scope_user=USER, request={"schema": "run-request.v1"}, run_id="demo.t4c.empty-w2", governance_pins=[], surface=_surface(), output_name="empty-w2.json")
            self.assertIsNone(result.refusal)
            assert result.output_path is not None
            report = json.loads(result.output_path.read_text())
            wage_disposition = next(row for row in report["dispositions"] if row["artifact_id"] == "tax.us.2025.rule.w2-box1-to-line1a")
            self.assertEqual(wage_disposition["disposition"], "published")

    def test_marshaled_token_and_uninstalled_transport_cannot_be_forged(self) -> None:
        with self.assertRaises(TypeError):
            MarshalledRunContext(None, object())  # type: ignore[arg-type]
        with TemporaryDirectory() as tmp:
            workspace = bootstrap_workspace(WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO)
            with self.assertRaises(GuardIntegrityError):
                workspace.guarded_push(object(), [])  # type: ignore[arg-type]
            with self.assertRaises(TypeError):
                InstalledEnvelopeGuards(Path(tmp) / "L", "fabricated", object())
            guard = workspace.install_envelope_guards()
            workspace.guarded_commit(guard, [])
            workspace.guarded_push(guard, [])
            with self.assertRaises(GuardIntegrityError):
                workspace.guarded_commit(guard, [], no_verify=True)
            with self.assertRaises(GuardIntegrityError):
                workspace.guarded_push(guard, [], raw_transport=True)
            gate = workspace.location / ".residency-envelope-gates" / "push.gate"
            gate.write_text("tampered\n")
            manifest = workspace.location / ".residency-envelope-gates" / "manifest.json"
            body = json.loads(manifest.read_text())
            body["digests"]["push"] = "0" * 64
            manifest.write_text(json.dumps(body))
            with self.assertRaises(GuardIntegrityError):
                workspace.guarded_push(guard, [])
        with TemporaryDirectory() as tmp:
            workspace = bootstrap_workspace(WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO)
            guard = workspace.install_envelope_guards()
            (workspace.location / ".residency-envelope-gates" / "commit.gate").unlink()
            with self.assertRaises(GuardIntegrityError):
                workspace.guarded_commit(guard, [])

    def test_both_gates_scan_the_complete_declared_envelope(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = bootstrap_workspace(WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO)
            guard = workspace.install_envelope_guards()
            envelope: list[dict[str, Any]] = [
                {"name": "public", "kind": "public-origin code", "public_origin_proof": "published"},
                {"name": "private", "kind": "public-origin code", "public_origin_proof": "published", "describes_personal": True},
            ]
            for crossing in (workspace.guarded_commit, workspace.guarded_push):
                with self.subTest(crossing=crossing.__name__), self.assertRaises(ResidencyViolation):
                    crossing(guard, envelope)

    def test_escaping_output_creates_neither_records_nor_output(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(ResidencyViolation):
                live_coordinate_run(WorkspaceCapability(root / "L"), repo_root=REPO, authoritative_acts=[_act("adopt-core-v2-current.json")], workspace_revision=10, run_scope={"jurisdiction": "us", "year": "2051"}, scope_user=USER, request={"schema": "run-request.v1"}, run_id="demo.t4.escape", governance_pins=[], surface=_surface(), output_name="../../escape.json")
            self.assertFalse((root / "L" / "records").exists())
            self.assertFalse((root / "L" / "outputs").exists())
            self.assertFalse((root / "escape.json").exists())


class ResolverCounterProbes(unittest.TestCase):
    def test_member_substitution_has_exact_refusal_and_layout_is_inert(self) -> None:
        with TemporaryDirectory() as tmp:
            content = Path(tmp) / "content"
            shutil.copytree(CONTENT, content)
            # Tamper one explicit, named member of the interest-slice package
            # this scenario adopts (adopt-interest-v2-current.json):
            # tax.us.2025.rule.form1040-line2b v1, the package's own terminal
            # line-output rule -- a fixed, semantically meaningful choice, not
            # the lexicographically-first rule.*.json (content from unrelated
            # slices can sort first) and not the first of several qualifying
            # "computation" candidates.
            TARGET_ID = "tax.us.2025.rule.form1040-line2b"
            TARGET_VERSION = "v1"
            package = json.loads((content / "package.interest-slice.json").read_text())
            assert any(
                m.get("id") == TARGET_ID
                and str(m.get("version", "v1")) == TARGET_VERSION
                and m.get("role") == "computation"
                for m in package["members"]
            ), f"named target {(TARGET_ID, TARGET_VERSION)} is not a computation member of interest-slice"
            rule = content / "rule.form1040-line2b.json"
            assert rule.is_file(), f"named target file missing: {rule}"
            body = json.loads(rule.read_text())
            assert (body.get("id"), str(body.get("version", "v1"))) == (TARGET_ID, TARGET_VERSION), (
                "named target file's declared (id, version) does not match "
                f"expected ({TARGET_ID!r}, {TARGET_VERSION!r}); found "
                f"({body.get('id')!r}, {body.get('version')!r})"
            )
            body["_tamper"] = True
            rule.write_text(json.dumps(body, sort_keys=True) + "\n")
            refusal = resolve_production_package([_act("adopt-interest-v2-current.json")], run_scope={"jurisdiction": "us", "year": "2025"}, scope_user=USER, workspace_revision=10, surface=_surface(content))
            self.assertIsInstance(refusal, Refusal)
            assert isinstance(refusal, Refusal)
            self.assertEqual(refusal.reason, "MEMBER_ABSENT_OR_MISMATCH")
