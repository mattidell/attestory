"""Tests for per-subject rule binding: a per-subject rule reads only its own subject.

Milestone: per-subject-binding.
Contract (docs/phases/engineering-health/milestones/per-subject-binding.md):
1. A required input whose fact type shares identity keys with the subject binds
   from the subject's own scope or blocks DEPENDENCY_ABSENT; nothing that names
   a per-subject fact type is read from the run-wide environment. Return-level
   inputs are unchanged.
2. Two Form 1098 statements on core v54 where only the first has circumstance
   answers: the second statement's residence-interest-reason blocks
   DEPENDENCY_ABSENT naming its own missing answers, and pins none of the first
   statement's findings.
3. Two EIC children in the flat shape where child 2 lacks residency answer:
   child 2 blocks DEPENDENCY_ABSENT and pins none of child 1's findings.
4. Return-level inputs (such as filing status or parameters) continue to bind
   to per-subject rules.
"""
from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import pytest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.package_validation import citizen_checksum, package_instance_checksum
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.facts import fact_id_for
from packages.tax.loader import TAX_CONTENT_DIR
from tests.test_f1098_v43_debt_limit_fix import RELEASE_DIR, _read_json
from tests.test_f1098_statement_review import _base_acts
from tests.test_f1098_circumstances_calculation import SCOPE as F1098_SCOPE, USER as F1098_USER
from tests.test_f1098_mortgage_interest_line12e_track2 import _attested, _member_fact_id

ROOT = Path(__file__).resolve().parent.parent
CONTENT = TAX_CONTENT_DIR
PACKAGE_PATH = CONTENT / "package.core-calculations.v54.json"
REGISTRY_PATH = CONTENT / "published-packages.v52.json"
RELEASE_PATH = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v52.json"

F1098_REASON_RULE = "tax.us.2025.rule.f1098-residence-interest-reason"

F1098_V2_ANSWERS = {
    "filing-unit-owns-home": "yes",
    "shared-main-home": "yes",
    "home-is-collateral": "yes",
    "owes-the-loan": "yes",
    "paid-the-interest": "yes",
    "no-one-else-owes-it": "yes",
    "what-the-money-paid-for": "bought-the-home",
    "this-is-the-original-loan": "yes",
    "mortgage-credit-certificate-received": "not-received",
}


def _build_two_statement_f1098_acts() -> list[dict[str, Any]]:
    """Build acts for two Form 1098 statements where only Statement A has circumstance answers."""
    acts = _base_acts(second_interest=10000)
    pkg = _read_json(PACKAGE_PATH)
    release = _read_json(RELEASE_PATH)

    # Strip existing package adoption from base acts
    acts = [a for a in acts if a.get("kind") != "package-adoption"]

    # Adopt f1098-circumstances bundle v2
    acts.append({
        "schema": "act.v1",
        "act_id": "demo.f1098.t2.circumstances.bundle.v2",
        "kind": "bundle-adoption",
        "actor": F1098_USER,
        "at": "2026-10-14T20:30:00Z",
        "committed_against": len(acts),
        "payload": {"bundle": _read_json(CONTENT / "f1098-circumstances.bundle.v2.json")},
    })

    # Assert circumstances ONLY for Statement A (lender.a, stmt.a)
    for i, (suffix, val) in enumerate(F1098_V2_ANSWERS.items()):
        fact_id = _member_fact_id(f"tax.us.2025.f1098.{suffix}", "demo.f1098.lender.a", "demo.f1098.stmt.a")
        finding = _attested(f"demo.f1098.ans.a.{i}", fact_id, val)
        acts.append({
            "schema": "act.v1",
            "act_id": f"demo.f1098.ans.act.{i}",
            "kind": "assertion",
            "actor": F1098_USER,
            "at": "2026-10-14T20:30:01Z",
            "committed_against": len(acts),
            "payload": {"finding": finding},
        })

    # Append package adoption for core calculations v54
    acts.append({
        "schema": "act.v1",
        "act_id": "demo.f1098.adopt.v54",
        "kind": "package-adoption",
        "actor": F1098_USER,
        "at": "2026-10-14T20:30:02Z",
        "committed_against": len(acts),
        "payload": {
            "package": {"id": pkg["id"], "version": pkg["version"], "checksum": pkg["package_checksum"]},
            "release": {
                "id": release["id"],
                "version": release["version"],
                "checksum": hashlib.sha256(RELEASE_PATH.read_bytes()).hexdigest(),
            },
            "revision": len(acts),
            "scope": F1098_SCOPE,
            "audit": {"note": "two-statement per-subject binding test"},
        },
    })

    for idx, a in enumerate(acts):
        a["committed_against"] = idx

    return acts


# Synthetic EIC probe definitions
SYNTH_USER = "demo.user.filer-1"
SYNTH_YEAR = "2025"
CHILD_KIND = "probe.child"
P = "probe.eic."
SYNTH_SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"}
REL = P + "child.relationship"
RES = P + "child.residency"
CLOSURE = P + "child-roster.source-closure"
INERT = P + "child.inert-path-unwritten"
FAMILY = P + "child-roster"
CLOSURE_MAPPING = P + "closure-mapping.child-roster"
BUNDLE = P + "child.vocabulary"
RULE_PREFIX = P + "rule."


def _pin(item_id: str, version: str = "v1") -> dict[str, str]:
    return {"id": item_id, "version": version}


def _synth_fact_type(fact_id: str) -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": fact_id,
        "version": "v1",
        "title": f"Synthetic per-child answer {fact_id}",
        "nature": "determinable",
        "identity_keys": [
            {"name": "child", "kind": "entity", "entity_kind": CHILD_KIND},
            {"name": "tax-year", "kind": "literal", "values": [SYNTH_YEAR]},
        ],
        "value_schema": {"type": "string", "enum": ["yes", "no"]},
        "supersession": {"policy": "free"},
    }


def _synth_bundle() -> dict[str, Any]:
    closure = {
        "schema": "fact-type.v2",
        "id": CLOSURE,
        "version": "v1",
        "title": "Closure of synthetic child roster",
        "nature": "determinable",
        "identity_keys": [
            {"name": "family-horizon", "kind": "entity", "entity_kind": "kernel.family-horizon"},
            {"name": "tax-year", "kind": "literal", "values": [SYNTH_YEAR]},
        ],
        "value_schema": {"type": "boolean"},
        "supersession": {"policy": "free"},
    }
    inert = {
        "schema": "fact-type.v2",
        "id": INERT,
        "version": "v1",
        "title": "Inert marker",
        "nature": "determinable",
        "identity_keys": [{"name": "marker", "kind": "literal", "values": ["unused"]}],
        "value_schema": {"type": "string", "enum": ["unused"]},
        "supersession": {"policy": "free"},
    }
    return {
        "schema": "bundle.v2",
        "id": BUNDLE,
        "version": "v1",
        "label": "Synthetic per-child vocabulary",
        "fact_types": [_synth_fact_type(REL), _synth_fact_type(RES), closure, inert],
    }


def _synth_family() -> dict[str, Any]:
    return {
        "schema": "source-family.v1",
        "id": FAMILY,
        "version": "v1",
        "scope": dict(SYNTH_SCOPE),
        "title": "Synthetic child roster",
        "member_predicate": {"fact_type": REL},
        "authorizes_subtotal": P + "child-count",
        "closure_claim": "Every qualifying-child candidate is recorded as a roster item.",
    }


def _synth_closure_mapping() -> dict[str, Any]:
    return {
        "schema": "source-closure-mapping.v2",
        "id": CLOSURE_MAPPING,
        "version": "v1",
        "admission": {"condition": "current-literal-true"},
        "admits_symbol": P + "child-count",
        "closure_fact_type": _pin(CLOSURE),
        "closure_horizon_key": "family-horizon",
        "family": _pin(FAMILY),
        "member_fact_type": _pin(REL),
    }


def _synth_rule(rule_id: str, **fields: Any) -> dict[str, Any]:
    body: dict[str, Any] = {
        "schema": "rule-artifact.v14",
        "id": rule_id,
        "version": "v1",
        "scope": dict(SYNTH_SCOPE),
        "role": "computation",
        "requires": [],
        "pins": [],
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
    }
    body.update(fields)
    return body


def _synth_rules() -> list[dict[str, Any]]:
    flat_rule = _synth_rule(
        f"{RULE_PREFIX}child-counts-flat",
        subject=_pin(REL),
        requires=[RES],
        when=True,
        value={
            "op": "choose",
            "when": {
                "op": "all",
                "args": [
                    {"op": "equal", "args": [{"op": "ref", "name": REL}, "yes"]},
                    {"op": "equal", "args": [{"op": "ref", "name": RES}, "yes"]},
                ],
            },
            "then": 1,
            "otherwise": 0,
        },
        publishes=P + "child.counts-flat",
    )
    read = P + "child.counts-flat"
    count_rule = _synth_rule(
        f"{RULE_PREFIX}qualifying-child-count-flat",
        when=True,
        selection={
            "mode": "exclusive_presence",
            "conflict": "refuse",
            "paths": [
                {
                    "id": "children",
                    "activity": {"kind": "source_nonempty", "member_fact_types": [_pin(REL)]},
                    "reads_subject_results": [{"symbol": read, "subject": _pin(REL)}],
                    "requires": [],
                    "pins": [],
                    "when": {"op": "require_closed", "source_set": FAMILY},
                    "value": {"op": "add", "args": [{"op": "collect", "name": read, "source_set": FAMILY}]},
                },
                {
                    "id": "inert",
                    "activity": {"kind": "source_nonempty", "member_fact_types": [_pin(INERT)]},
                    "reads_subject_results": [],
                    "requires": [],
                    "pins": [],
                    "when": True,
                    "value": {"op": "block", "code": "DEPENDENCY_ABSENT"},
                },
            ],
            "default": {
                "id": "neither",
                "reads_subject_results": [],
                "requires": [],
                "pins": [],
                "when": True,
                "value": {"op": "count", "name": REL, "source_set": FAMILY},
            },
            "refusal": {
                "code": "DEPENDENCY_INVALID",
                "missing": ["probe-inert-path-conflict"],
                "pins": [],
            },
        },
        publishes=P + "child.count-flat",
    )
    return [flat_rule, count_rule]


def _build_synth_package(rules: list[dict[str, Any]]) -> dict[str, Any]:
    members: list[dict[str, Any]] = [
        _synth_bundle(),
        _synth_family(),
        _synth_closure_mapping(),
        *rules,
    ]
    pkg: dict[str, Any] = {
        "schema": "package.v1",
        "id": "probe.package.eic-children",
        "version": "v1",
        "scope": dict(SYNTH_SCOPE),
        "admitted_schemas": [
            "bundle.v2", "source-family.v1", "source-closure-mapping.v2",
            "rule-artifact.v14", "fact-type.v2",
        ],
        "conflict_semantics": "refusal",
        "composition_obligations": [],
        "input_bindings": [],
        "entrypoints": [P + "child.count-flat"],
        "members": members,
    }
    for m in pkg["members"]:
        m["citizen_checksum"] = citizen_checksum(m)
    pkg["package_checksum"] = package_instance_checksum(pkg)
    return pkg


def _build_synth_eic_acts(pkg: dict[str, Any], release_sha: str) -> list[dict[str, Any]]:
    acts: list[dict[str, Any]] = [
        {
            "schema": "act.v1",
            "act_id": "demo.act.entity.child1",
            "kind": "entity-introduced",
            "actor": SYNTH_USER,
            "at": "2026-10-24T00:00:00Z",
            "committed_against": 0,
            "payload": {"entity": {"schema": "entity.v1", "id": "demo-child-1", "kind": CHILD_KIND, "label": "Child 1"}},
        },
        {
            "schema": "act.v1",
            "act_id": "demo.act.entity.child2",
            "kind": "entity-introduced",
            "actor": SYNTH_USER,
            "at": "2026-10-24T00:00:01Z",
            "committed_against": 1,
            "payload": {"entity": {"schema": "entity.v1", "id": "demo-child-2", "kind": CHILD_KIND, "label": "Child 2"}},
        },
        {
            "schema": "act.v1",
            "act_id": "demo.act.bundle.adopt",
            "kind": "bundle-adoption",
            "actor": SYNTH_USER,
            "at": "2026-10-24T00:00:02Z",
            "committed_against": 2,
            "payload": {"bundle": _synth_bundle()},
        },
        {
            "schema": "act.v1",
            "act_id": "demo.act.horizon.genesis",
            "kind": "horizon-genesis",
            "actor": SYNTH_USER,
            "at": "2026-10-24T00:00:03Z",
            "committed_against": 3,
            "payload": {"family": _pin(FAMILY), "horizon_id": "demo.probe.eic.horizon.0", "scope": dict(SYNTH_SCOPE)},
        },
        {
            "schema": "act.v1",
            "act_id": "demo.act.rel.child1",
            "kind": "assertion",
            "actor": SYNTH_USER,
            "at": "2026-10-24T00:00:04Z",
            "committed_against": 4,
            "payload": {
                "finding": {
                    "schema": "finding.v2",
                    "id": "demo.probe.rel.demo-child-1",
                    "fact_id": fact_id_for(REL, {"child": "demo-child-1", "tax-year": SYNTH_YEAR}),
                    "value": "yes",
                    "basis": "attested",
                    "evidence_ids": [],
                }
            },
        },
        {
            "schema": "act.v1",
            "act_id": "demo.act.residency.child1",
            "kind": "assertion",
            "actor": SYNTH_USER,
            "at": "2026-10-24T00:00:05Z",
            "committed_against": 5,
            "payload": {
                "finding": {
                    "schema": "finding.v2",
                    "id": "demo.probe.residency.demo-child-1",
                    "fact_id": fact_id_for(RES, {"child": "demo-child-1", "tax-year": SYNTH_YEAR}),
                    "value": "yes",
                    "basis": "attested",
                    "evidence_ids": [],
                }
            },
        },
        {
            "schema": "act.v1",
            "act_id": "demo.act.rel.child2",
            "kind": "assertion",
            "actor": SYNTH_USER,
            "at": "2026-10-24T00:00:06Z",
            "committed_against": 6,
            "payload": {
                "finding": {
                    "schema": "finding.v2",
                    "id": "demo.probe.rel.demo-child-2",
                    "fact_id": fact_id_for(REL, {"child": "demo-child-2", "tax-year": SYNTH_YEAR}),
                    "value": "yes",
                    "basis": "attested",
                    "evidence_ids": [],
                }
            },
        },
        # NOTE: demo-child-2 residency is UNANSWERED.
        {
            "schema": "act.v1",
            "act_id": "demo.act.closure",
            "kind": "assertion",
            "actor": SYNTH_USER,
            "at": "2026-10-24T00:00:07Z",
            "committed_against": 7,
            "payload": {
                "finding": {
                    "schema": "finding.v2",
                    "id": "demo.probe.eic.closure",
                    "fact_id": fact_id_for(CLOSURE, {"family-horizon": "demo.probe.eic.horizon.0", "tax-year": SYNTH_YEAR}),
                    "value": True,
                    "basis": "attested",
                    "evidence_ids": [],
                }
            },
        },
        {
            "schema": "act.v1",
            "act_id": "demo.act.pkg.adopt",
            "kind": "package-adoption",
            "actor": SYNTH_USER,
            "at": "2026-10-24T00:00:08Z",
            "committed_against": 8,
            "payload": {
                "package": {"id": pkg["id"], "version": pkg["version"], "checksum": pkg["package_checksum"]},
                "release": {"id": "demo.probe.release", "version": "v1", "checksum": release_sha},
                "revision": 8,
                "scope": dict(SYNTH_SCOPE),
                "audit": {"note": "synthetic child probe"},
            },
        },
    ]
    return acts


class TestPerSubjectBinding(unittest.TestCase):
    """Contract tests for per-subject rule input binding."""

    @pytest.mark.xfail(
        strict=True,
        reason="Before Track 1 fix, Statement B adopts Statement A's circumstance answers and publishes.",
    )
    def test_f1098_two_statement_second_statement_blocks(self) -> None:
        """With two Form 1098 statements where only Statement A has answers, Statement B blocks."""
        acts = _build_two_statement_f1098_acts()
        with TemporaryDirectory() as tmp:
            cap = WorkspaceCapability(Path(tmp))
            outcome = live_coordinate_run(
                cap,
                repo_root=ROOT,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=F1098_SCOPE,
                scope_user=F1098_USER,
                request={"schema": "run-request.v1"},
                run_id="demo.f1098.isolation.test",
                governance_pins=[],
                surface=PublicationSurface(RELEASE_DIR, REGISTRY_PATH, CONTENT),
                output_name="probe.json",
            )
            self.assertIsNone(outcome.refusal)
            assert outcome.output_path is not None
            report = json.loads(Path(outcome.output_path).read_text("utf-8"))

        dispositions = [
            d for d in report.get("dispositions", [])
            if d.get("artifact_id") == F1098_REASON_RULE
        ]
        self.assertEqual(len(dispositions), 2, "Expected 2 dispositions for residence-interest-reason")

        disp_by_stmt: dict[str, dict[str, Any]] = {}
        for d in dispositions:
            sym = str(d.get("symbol", ""))
            if "demo.f1098.stmt.a" in sym:
                disp_by_stmt["stmt_a"] = d
            elif "demo.f1098.stmt.b" in sym:
                disp_by_stmt["stmt_b"] = d

        self.assertIn("stmt_a", disp_by_stmt, "Missing Statement A disposition")
        self.assertIn("stmt_b", disp_by_stmt, "Missing Statement B disposition")

        # Statement A: published qualified
        stmt_a = disp_by_stmt["stmt_a"]
        self.assertEqual(stmt_a["disposition"], "published")

        # Statement B: must block DEPENDENCY_ABSENT naming its own missing answers
        stmt_b = disp_by_stmt["stmt_b"]
        self.assertEqual(
            stmt_b["disposition"],
            "blocked",
            "Statement B must block because its circumstance answers are unasserted",
        )
        self.assertEqual(stmt_b.get("code"), "DEPENDENCY_ABSENT")

        # Statement B must pin NONE of Statement A's circumstance finding IDs
        stmt_b_input_pins = [p["id"] for p in stmt_b.get("pins", []) if p.get("role") == "input"]
        stmt_a_leaked = [pid for pid in stmt_b_input_pins if "ans.a" in pid]
        self.assertEqual(
            stmt_a_leaked,
            [],
            f"Statement B pinned Statement A's circumstance findings: {stmt_a_leaked}",
        )

    @pytest.mark.xfail(
        strict=True,
        reason="Before Track 1 fix, Child 2 adopts Child 1's residency answer and publishes 1.",
    )
    def test_eic_flat_shape_missing_child_answer_blocks(self) -> None:
        """In flat per-child rule shape, a child lacking residency answer blocks."""
        pkg = _build_synth_package(_synth_rules())
        with TemporaryDirectory() as surface_dir:
            surface_path = Path(surface_dir)
            content_dir = surface_path / "content"
            releases_dir = surface_path / "releases"
            content_dir.mkdir(parents=True)
            releases_dir.mkdir(parents=True)

            (content_dir / "package.probe.v1.json").write_text(json.dumps(pkg, indent=2), "utf-8")
            registry = {
                "schema": "package-registry.v1",
                "packages": [
                    {
                        "id": pkg["id"],
                        "version": pkg["version"],
                        "checksum": pkg["package_checksum"],
                        "relative_path": "package.probe.v1.json",
                    }
                ],
            }
            reg_bytes = json.dumps(registry, indent=2).encode("utf-8")
            reg_sha = hashlib.sha256(reg_bytes).hexdigest()
            (content_dir / "published-packages.probe.json").write_bytes(reg_bytes)

            release = {
                "schema": "release-registry.v1",
                "id": "demo.probe.release",
                "version": "v1",
                "package_registry_sha256": reg_sha,
            }
            rel_bytes = json.dumps(release, indent=2).encode("utf-8")
            rel_sha = hashlib.sha256(rel_bytes).hexdigest()
            rel_path = releases_dir / "demo.release.probe.v1.json"
            rel_path.write_bytes(rel_bytes)

            acts = _build_synth_eic_acts(pkg, rel_sha)

            with TemporaryDirectory() as workspace_dir:
                cap = WorkspaceCapability(Path(workspace_dir))
                outcome = live_coordinate_run(
                    cap,
                    repo_root=ROOT,
                    authoritative_acts=acts,
                    workspace_revision=len(acts),
                    run_scope=SYNTH_SCOPE,
                    scope_user=SYNTH_USER,
                    request={"schema": "run-request.v1"},
                    run_id="demo.eic.isolation.test",
                    governance_pins=[],
                    surface=PublicationSurface(
                        releases_dir,
                        content_dir / "published-packages.probe.json",
                        content_dir,
                    ),
                    output_name="probe.json",
                )
                self.assertIsNone(outcome.refusal)
                assert outcome.output_path is not None
                report = json.loads(Path(outcome.output_path).read_text("utf-8"))

        flat_rule_id = f"{RULE_PREFIX}child-counts-flat"
        dispositions = [
            d for d in report.get("dispositions", [])
            if d.get("artifact_id") == flat_rule_id
        ]
        self.assertEqual(len(dispositions), 2, "Expected 2 dispositions for per-child rule")

        disp_by_child: dict[str, dict[str, Any]] = {}
        for d in dispositions:
            sym = str(d.get("symbol", ""))
            if "demo-child-1" in sym:
                disp_by_child["child1"] = d
            elif "demo-child-2" in sym:
                disp_by_child["child2"] = d

        self.assertIn("child1", disp_by_child)
        self.assertIn("child2", disp_by_child)

        # Child 1: published 1
        self.assertEqual(disp_by_child["child1"]["disposition"], "published")

        # Child 2: must block DEPENDENCY_ABSENT
        child2 = disp_by_child["child2"]
        self.assertEqual(
            child2["disposition"],
            "blocked",
            "Child 2 must block because residency is unanswered",
        )
        self.assertEqual(child2.get("code"), "DEPENDENCY_ABSENT")

        # Child 2 must not pin Child 1's residency finding
        child2_input_pins = [p["id"] for p in child2.get("pins", []) if p.get("role") == "input"]
        self.assertNotIn("demo.probe.residency.demo-child-1", child2_input_pins)

    def test_per_subject_rule_reads_return_level_input(self) -> None:
        """A per-subject rule that requires a return-level input (filing status) still binds it."""
        acts = _build_two_statement_f1098_acts()
        with TemporaryDirectory() as tmp:
            cap = WorkspaceCapability(Path(tmp))
            outcome = live_coordinate_run(
                cap,
                repo_root=ROOT,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=F1098_SCOPE,
                scope_user=F1098_USER,
                request={"schema": "run-request.v1"},
                run_id="demo.f1098.return_level.test",
                governance_pins=[],
                surface=PublicationSurface(RELEASE_DIR, REGISTRY_PATH, CONTENT),
                output_name="probe.json",
            )
            self.assertIsNone(outcome.refusal)
            assert outcome.output_path is not None
            report = json.loads(Path(outcome.output_path).read_text("utf-8"))

        # In core calculations v54, tax.us.2025.rule.f1098-residence-interest-reason
        # requires 'filing_status', which is a return-level fact.
        dispositions = [
            d for d in report.get("dispositions", [])
            if d.get("artifact_id") == F1098_REASON_RULE
        ]
        stmt_a = next((d for d in dispositions if "demo.f1098.stmt.a" in str(d.get("symbol", ""))), None)
        self.assertIsNotNone(stmt_a, "Statement A disposition must exist")
        assert stmt_a is not None

        # Statement A must have pinned the return-level filing status assertion
        pinned_input_ids = [p["id"] for p in stmt_a.get("pins", []) if p.get("role") == "input"]
        self.assertIn(
            "demo.cgd.t2.finding.status",
            pinned_input_ids,
            "Statement A must bind and pin the return-level filing_status input",
        )


if __name__ == "__main__":
    unittest.main()
