"""ADR-0037 production evidence for declared multi-member non-publication."""

from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.evaluator import BLOCK_INVALID, AccessLog, Environment, EvalBlocked, evaluate
from packages.derivation.explanation import walk_npe
from packages.derivation.loader import DerivationSchemas, load_canon
from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.package_validation import citizen_checksum, package_instance_checksum, validate_package
from packages.derivation.production_resolver import PublicationSurface
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import InputFinding, RunContext, run
from packages.kernel.schema_registry import SchemaValidationError


ROOT = Path(__file__).resolve().parents[2] / "packages" / "sample_data" / "conditional_multi_dependency"
SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "demo"}


def _load(relative: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((ROOT / relative).read_text("utf-8")))


def _rule() -> dict[str, Any]:
    return _load("examples/rule-artifact.v3.json")


def _context(*, condition: bool, members: list[InputFinding]) -> RunContext:
    return RunContext(
        run_id="demo.cmdn.run",
        rules=[_rule()],
        parameters={},
        canon=load_canon(DerivationSchemas()),
        inputs=[
            InputFinding("demo.condition", condition, "demo.finding.condition", "input"),
            InputFinding("demo.result", 17, "demo.finding.result", "input"),
            *members,
        ],
        sources=[],
        adoption_pin={"role": "adoption", "id": "demo.package.conditional-dependency-set", "version": "v1"},
        governance_pins=[],
    )


class ConditionalDependencySchema(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()

    def test_positive_rule_and_package_are_published_schema_instances(self) -> None:
        rule = _rule()
        package = _load("examples/artifact-package.v3.json")
        self.schemas.validate_declared(rule)
        self.schemas.validate_declared(package)
        validation = validate_package(package, {(rule["id"], rule["version"]): rule}, self.schemas)
        self.assertTrue(validation.ok, validation.issues)

    def test_empty_and_non_ref_members_are_rejected(self) -> None:
        for name in (
            "negatives/rule-artifact.v3.empty-members.json",
            "negatives/rule-artifact.v3.non-ref-member.json",
        ):
            with self.subTest(name=name):
                with self.assertRaises(SchemaValidationError):
                    self.schemas.validate_declared(_load(name))

    def test_runner_private_conditional_requires_shape_is_rejected(self) -> None:
        malformed = copy.deepcopy(_rule())
        malformed["when"] = {
            "op": "conditional_requires",
            "condition": {"op": "ref", "name": "demo.condition"},
            "members": [{"op": "ref", "name": "demo.member.alpha"}],
        }
        with self.assertRaises(SchemaValidationError):
            self.schemas.validate_declared(malformed)


class ConditionalDependencyEvaluation(unittest.TestCase):
    def setUp(self) -> None:
        self.schemas = DerivationSchemas()

    def test_inactive_members_are_neither_missing_nor_pinned(self) -> None:
        result = run(_context(condition=False, members=[]), self.schemas)
        self.assertEqual(result.blocked, [])
        publication = result.publications[0].finding
        input_ids = {pin["id"] for pin in publication["pins"] if pin["role"] == "input"}
        self.assertEqual(input_ids, {"demo.finding.condition", "demo.finding.result"})

    def test_active_members_publish_and_pin_every_evaluated_ref(self) -> None:
        result = run(_context(condition=True, members=[
            InputFinding("demo.member.alpha", 0, "demo.finding.alpha", "input"),
            InputFinding("demo.member.beta", 0, "demo.finding.beta", "input"),
        ]), self.schemas)
        self.assertEqual(result.blocked, [])
        input_ids = {pin["id"] for pin in result.publications[0].finding["pins"] if pin["role"] == "input"}
        self.assertEqual(input_ids, {
            "demo.finding.condition", "demo.finding.result", "demo.finding.alpha", "demo.finding.beta",
        })

    def test_active_multi_and_partial_absence_preserve_declared_member_order(self) -> None:
        cases: tuple[tuple[list[InputFinding], list[str]], ...] = (
            ([], ["demo.member.alpha", "demo.member.beta"]),
            ([InputFinding("demo.member.alpha", 0, "demo.finding.alpha", "input")], ["demo.member.beta"]),
        )
        for members, expected_missing in cases:
            with self.subTest(expected_missing=expected_missing):
                result = run(_context(condition=True, members=members), self.schemas)
                self.assertEqual(result.blocked, [{
                    "artifact_id": "demo.rule.conditional-dependency-set",
                    "code": "DEPENDENCY_ABSENT",
                    "missing": expected_missing,
                }])

    def test_blocked_disposition_pins_present_reads_but_never_invents_absent_member_pins(self) -> None:
        result = run(_context(condition=True, members=[
            InputFinding("demo.member.alpha", 0, "demo.finding.alpha", "input"),
        ]), self.schemas)
        input_ids = {pin["id"] for pin in result.dispositions[0]["pins"] if pin["role"] == "input"}
        self.assertEqual(input_ids, {"demo.finding.condition", "demo.finding.alpha"})

    def test_successor_condition_or_member_changes_the_published_pin_identity(self) -> None:
        original = run(_context(condition=True, members=[
            InputFinding("demo.member.alpha", 0, "demo.finding.alpha", "input"),
            InputFinding("demo.member.beta", 0, "demo.finding.beta", "input"),
        ]), self.schemas).publications[0].finding
        member_successor = run(_context(condition=True, members=[
            InputFinding("demo.member.alpha", 0, "demo.finding.alpha.successor", "input"),
            InputFinding("demo.member.beta", 0, "demo.finding.beta", "input"),
        ]), self.schemas).publications[0].finding
        condition_successor_context = _context(condition=True, members=[
            InputFinding("demo.member.alpha", 0, "demo.finding.alpha", "input"),
            InputFinding("demo.member.beta", 0, "demo.finding.beta", "input"),
        ])
        condition_successor_context.inputs[0] = InputFinding(
            "demo.condition", True, "demo.finding.condition.successor", "input"
        )
        condition_successor = run(condition_successor_context, self.schemas).publications[0].finding
        self.assertNotEqual(original["id"], member_successor["id"])
        self.assertNotEqual(original["id"], condition_successor["id"])

    def test_non_absence_member_failure_propagates_unchanged(self) -> None:
        expression = _rule()["when"]
        environment = Environment(
            symbols={"demo.condition": True, "demo.member.alpha": "outside-domain", "demo.member.beta": "ok"},
            sources={}, closed_sets=frozenset(), parameters={}, canon={},
            symbol_fact_types={"demo.member.alpha": "demo.member-type"},
            categorical_domains={"demo.member-type": ["ok"]},
        )
        with self.assertRaises(EvalBlocked) as caught:
            evaluate(expression, environment, AccessLog())
        self.assertEqual(caught.exception.category, BLOCK_INVALID)

    def test_primary_and_reference_runners_are_byte_equal(self) -> None:
        contexts = (
            _context(condition=False, members=[]),
            _context(condition=True, members=[]),
            _context(condition=True, members=[
                InputFinding("demo.member.alpha", 0, "demo.finding.alpha", "input"),
                InputFinding("demo.member.beta", 0, "demo.finding.beta", "input"),
            ]),
        )
        for context in contexts:
            with self.subTest(context=context):
                primary = run(context, self.schemas)
                reference = run_reference(context, self.schemas)
                self.assertEqual(
                    json.dumps(primary.blocked, sort_keys=True),
                    json.dumps(reference.blocked, sort_keys=True),
                )
                self.assertEqual(
                    json.dumps([p.finding for p in primary.publications], sort_keys=True),
                    json.dumps([p.finding for p in reference.publications], sort_keys=True),
                )


class ConditionalDependencyNpe(unittest.TestCase):
    def test_walk_preserves_the_durable_ordered_missing_list(self) -> None:
        rule = _rule()
        records = [
            {"schema": "derivation-record.v2", "record_id": "demo.cmdn.started", "run_id": "demo.cmdn.run", "phase": "started", "workspace_revision": 1, "governance_pins": [], "adoption_pin": {"role": "adoption", "id": "demo.package", "version": "v1"}},
            {"schema": "derivation-record.v2", "record_id": "demo.cmdn.completed", "run_id": "demo.cmdn.run", "phase": "completed", "workspace_revision": 1, "governance_pins": [], "adoption_pin": {"role": "adoption", "id": "demo.package", "version": "v1"}, "stop_reason": "saturated", "dispositions": [{"artifact_id": rule["id"], "disposition": "blocked", "pins": [], "code": "DEPENDENCY_ABSENT", "missing": ["demo.member.alpha", "demo.member.beta"]}]},
        ]
        walk = walk_npe(run_id="demo.cmdn.run", symbol="demo.conditional.output", rules=[rule], records=records)
        self.assertEqual(walk["root"]["unmet_references"], ["demo.member.alpha", "demo.member.beta"])
        DerivationSchemas().validate_declared(walk)


class ConditionalDependencyLiveCoordinator(unittest.TestCase):
    """The declared node is exercised from facts on record, not a RunContext."""

    @staticmethod
    def _fact_type(identifier: str, value_schema: dict[str, Any]) -> dict[str, Any]:
        return {
            "schema": "fact-type.v2", "id": identifier, "version": "v1",
            "title": f"Synthetic {identifier}", "nature": "determinable",
            "identity_keys": [{"name": "tax-year", "kind": "literal", "values": ["2025"]}],
            "value_schema": value_schema, "supersession": {"policy": "free"},
        }

    def _surface_and_acts(self, root: Path, values: dict[str, Any]) -> tuple[PublicationSurface, list[dict[str, Any]]]:
        member_dir = root / "members"
        release_dir = root / "releases"
        member_dir.mkdir()
        release_dir.mkdir()
        rule = _rule()
        bundle = {
            "schema": "bundle.v2", "id": "demo.bundle.cmdn", "version": "v1", "label": "CMDN synthetic facts",
            "fact_types": [
                self._fact_type("demo.condition", {"type": "boolean"}),
                self._fact_type("demo.result", {"type": "number"}),
                self._fact_type("demo.member.alpha", {"type": "number"}),
                self._fact_type("demo.member.beta", {"type": "number"}),
            ],
        }
        package = _load("examples/artifact-package.v3.json")
        package["members"] = [
            {"role": "fact-type-bundle", "schema": "bundle.v2", "id": bundle["id"], "version": "v1"},
            {"role": "computation", "schema": "rule-artifact.v3", "id": rule["id"], "version": "v1"},
        ]
        package["admitted_schemas"] = ["bundle.v2", "rule-artifact.v3"]
        package["input_bindings"] = [
            {"symbol": symbol, "fact_type": {"id": symbol, "version": "v1"}, "mode": "required"}
            for symbol in ("demo.condition", "demo.result", "demo.member.alpha", "demo.member.beta")
        ]
        package["package_checksum"] = package_instance_checksum(package)
        for body in (rule, bundle, package):
            (member_dir / f"{body['id']}.{body['version']}.json").write_text(
                json.dumps(body, sort_keys=True, separators=(",", ":")), encoding="utf-8"
            )
        registry = {
            "packages": [{"id": package["id"], "version": package["version"], "checksum": package["package_checksum"]}],
            "citizens": [
                {"id": rule["id"], "version": rule["version"], "checksum": citizen_checksum(rule)},
                {"id": bundle["id"], "version": bundle["version"], "checksum": citizen_checksum(bundle)},
            ],
        }
        registry_path = root / "published-packages.json"
        registry_path.write_text(json.dumps(registry, sort_keys=True, separators=(",", ":")), encoding="utf-8")
        release = {
            "schema": "release-registry.v1", "id": "demo.release.cmdn", "version": "v1",
            "package_registry_sha256": hashlib.sha256(registry_path.read_bytes()).hexdigest(),
        }
        release_bytes = json.dumps(release, sort_keys=True, separators=(",", ":")).encode("utf-8")
        (release_dir / "demo.release.cmdn.v1.json").write_bytes(release_bytes)

        def act(index: int, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
            return {"schema": "act.v1", "act_id": f"demo.cmdn.act.{index}", "kind": kind, "actor": "demo.user", "at": f"2026-07-18T00:00:{index:02d}Z", "committed_against": index, "payload": payload}

        acts: list[dict[str, Any]] = [act(0, "bundle-adoption", {"bundle": bundle})]
        for symbol, value in values.items():
            acts.append(act(len(acts), "assertion", {"finding": {
                "schema": "finding.v1", "id": f"demo.cmdn.finding.{symbol.rsplit('.', 1)[-1]}",
                "fact_id": f"{symbol}|tax-year=2025", "value": value,
                "basis": "attested", "evidence_ids": [],
            }}))
        acts.append(act(len(acts), "package-adoption", {
            "package": {"id": package["id"], "version": package["version"], "checksum": package["package_checksum"]},
            "release": {"id": release["id"], "version": release["version"], "checksum": hashlib.sha256(release_bytes).hexdigest()},
            "scope": {"jurisdiction": "us", "year": "2052"}, "revision": 1,
        }))
        return PublicationSurface(release_dir, registry_path, member_dir), acts

    def test_authoritative_fact_goldens_cover_inactive_and_active_missing_paths(self) -> None:
        cases: tuple[tuple[str, dict[str, Any], list[str], set[str]], ...] = (
            ("inactive", {"demo.condition": False, "demo.result": 17}, [], {"demo.cmdn.finding.condition", "demo.cmdn.finding.result"}),
            ("active-all", {"demo.condition": True, "demo.result": 17, "demo.member.alpha": 0, "demo.member.beta": 0}, [], {"demo.cmdn.finding.condition", "demo.cmdn.finding.result", "demo.cmdn.finding.alpha", "demo.cmdn.finding.beta"}),
            ("active-two-absent", {"demo.condition": True, "demo.result": 17}, ["demo.member.alpha", "demo.member.beta"], set()),
            ("active-one-absent", {"demo.condition": True, "demo.result": 17, "demo.member.alpha": 0}, ["demo.member.beta"], set()),
        )
        for name, values, expected_missing, expected_inputs in cases:
            with self.subTest(name=name), TemporaryDirectory() as tmp:
                root = Path(tmp)
                surface, acts = self._surface_and_acts(root, values)
                outcome = live_coordinate_run(
                    WorkspaceCapability(root / "workspace"), repo_root=Path(__file__).resolve().parents[2],
                    authoritative_acts=acts, workspace_revision=len(acts), run_scope={"jurisdiction": "us", "year": "2052"},
                    scope_user="demo.user", request={"schema": "run-request.v1"}, run_id=f"demo.cmdn.{name}",
                    governance_pins=[], surface=surface, output_name=f"{name}.json",
                )
                self.assertIsNone(outcome.refusal)
                records = [json.loads(line) for line in (root / "workspace" / "records" / "derivation_records.jsonl").read_text().splitlines()]
                closing = records[-1]
                row = closing["dispositions"][0]
                if expected_missing:
                    self.assertEqual(row["missing"], expected_missing)
                    walk = walk_npe(run_id=f"demo.cmdn.{name}", symbol="demo.conditional.output", rules=[_rule()], records=records)
                    self.assertEqual(walk["root"]["unmet_references"], expected_missing)
                else:
                    input_ids = {pin["id"] for pin in closing["dispositions"][0]["pins"] if pin["role"] == "input"}
                    self.assertEqual(input_ids, expected_inputs)


if __name__ == "__main__":
    unittest.main()
