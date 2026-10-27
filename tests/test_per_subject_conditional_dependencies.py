"""Tests for ADR-0081: Per-subject conditional dependencies.

Milestone: dependent-tie-breaker-2025
Track: 0 (per-subject conditional dependencies)
Decision: docs/adr/0081-per-subject-conditional-dependencies.md

Contracts verified through live_coordinate_run with synthetic two-subject surface:
1. Condition false, member absent: rule publishes; member is neither named nor pinned.
2. Condition true, member absent: blocks DEPENDENCY_ABSENT naming the member for that subject.
3. Condition true, member present: publishes, the member pinned.
4. Two subjects in one run, one on each branch: each resolves on its own answers;
   child 2's answer is never bound for child 1 (assert the pins).
5. A member answer present only for the other subject does not satisfy this subject.
6. Superseding a member or condition answer re-derives.
7. Mutation test: a member also listed in requires still behaves as required (unchanged).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
import unittest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.package_validation import (
    citizen_checksum,
    package_instance_checksum,
    validate_package,
)
from packages.derivation.loader import DerivationSchemas
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.facts import fact_id_for

REPO_ROOT = Path(__file__).resolve().parent.parent

YEAR = "2025"
USER = "demo.user"
PACKAGE_SCOPE = {"jurisdiction": "us", "tax_year": 2025, "family": "demo-child"}
RUN_SCOPE = {"jurisdiction": "us", "year": YEAR}

RULE_MAIN_ID = "demo.rule.child-tie-breaker"
RULE_MUTATION_ID = "demo.rule.child-mutation"
RULE_RUNWIDE_ID = "demo.rule.child-runwide"

FT_CHILD = "demo.child"
FT_COND = "demo.child.condition"
FT_MEMBER = "demo.child.conditional-member"
FT_MUTATION_MEMBER = "demo.child.required-member"
FT_RUNWIDE = "demo.runwide-setting"

PUB_OUTCOME = "demo.child.outcome"
PUB_MUTATION = "demo.child.mutation-outcome"
PUB_RUNWIDE = "demo.child.runwide-outcome"


def _build_synthetic_surface(
    root: Path,
) -> tuple[PublicationSurface, dict[str, Any], dict[str, Any], dict[str, Any]]:
    bundle = {
        "schema": "bundle.v2",
        "id": "demo.dtb.bundle",
        "version": "v1",
        "label": "DTB synthetic facts",
        "fact_types": [
            {
                "schema": "fact-type.v2",
                "id": FT_CHILD,
                "version": "v1",
                "title": "Synthetic child",
                "nature": "determinable",
                "identity_keys": [
                    {"name": "child", "kind": "entity", "entity_kind": FT_CHILD},
                    {"name": "tax-year", "kind": "literal", "values": [YEAR]},
                ],
                "value_schema": {"type": "string"},
                "supersession": {"policy": "free"},
            },
            {
                "schema": "fact-type.v2",
                "id": FT_COND,
                "version": "v1",
                "title": "Synthetic condition",
                "nature": "determinable",
                "identity_keys": [
                    {"name": "child", "kind": "entity", "entity_kind": FT_CHILD},
                    {"name": "tax-year", "kind": "literal", "values": [YEAR]},
                ],
                "value_schema": {"type": "string", "enum": ["yes", "no"]},
                "supersession": {"policy": "free"},
            },
            {
                "schema": "fact-type.v2",
                "id": FT_MEMBER,
                "version": "v1",
                "title": "Synthetic conditional member",
                "nature": "determinable",
                "identity_keys": [
                    {"name": "child", "kind": "entity", "entity_kind": FT_CHILD},
                    {"name": "tax-year", "kind": "literal", "values": [YEAR]},
                ],
                "value_schema": {"type": "string", "enum": ["yes", "no"]},
                "supersession": {"policy": "free"},
            },
            {
                "schema": "fact-type.v2",
                "id": FT_MUTATION_MEMBER,
                "version": "v1",
                "title": "Synthetic required member for mutation test",
                "nature": "determinable",
                "identity_keys": [
                    {"name": "child", "kind": "entity", "entity_kind": FT_CHILD},
                    {"name": "tax-year", "kind": "literal", "values": [YEAR]},
                ],
                "value_schema": {"type": "string", "enum": ["yes", "no"]},
                "supersession": {"policy": "free"},
            },
            {
                "schema": "fact-type.v2",
                "id": FT_RUNWIDE,
                "version": "v1",
                "title": "Synthetic run-wide setting",
                "nature": "determinable",
                "identity_keys": [
                    {"name": "tax-year", "kind": "literal", "values": [YEAR]},
                ],
                "value_schema": {"type": "string", "enum": ["yes", "no"]},
                "supersession": {"policy": "free"},
            },
        ],
    }

    rule = {
        "schema": "rule-artifact.v14",
        "id": RULE_MAIN_ID,
        "version": "v1",
        "scope": dict(PACKAGE_SCOPE),
        "role": "computation",
        "subject": {"id": FT_CHILD, "version": "v1"},
        "requires": [FT_COND],
        "publishes": PUB_OUTCOME,
        "pins": [],
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "when": {
            "op": "conditional_dependency_set",
            "condition": {
                "op": "categorical_compare",
                "cmp": "eq",
                "left": {"op": "ref", "name": FT_COND},
                "right": {
                    "op": "category_literal",
                    "fact_type": {"id": FT_COND, "version": "v1"},
                    "value": "yes",
                },
            },
            "members": [{"op": "ref", "name": FT_MEMBER}],
        },
        "value": {
            "op": "choose",
            "when": {
                "op": "categorical_compare",
                "cmp": "eq",
                "left": {"op": "ref", "name": FT_COND},
                "right": {
                    "op": "category_literal",
                    "fact_type": {"id": FT_COND, "version": "v1"},
                    "value": "yes",
                },
            },
            "then": {
                "op": "choose",
                "when": {
                    "op": "categorical_compare",
                    "cmp": "eq",
                    "left": {"op": "ref", "name": FT_MEMBER},
                    "right": {
                        "op": "category_literal",
                        "fact_type": {"id": FT_MEMBER, "version": "v1"},
                        "value": "yes",
                    },
                },
                "then": "contested-won",
                "else": "contested-lost",
            },
            "else": "uncontested",
        },
    }

    mutation_rule = {
        "schema": "rule-artifact.v14",
        "id": RULE_MUTATION_ID,
        "version": "v1",
        "scope": dict(PACKAGE_SCOPE),
        "role": "computation",
        "subject": {"id": FT_CHILD, "version": "v1"},
        "requires": [FT_COND, FT_MUTATION_MEMBER],
        "publishes": PUB_MUTATION,
        "pins": [],
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "when": {
            "op": "conditional_dependency_set",
            "condition": {
                "op": "categorical_compare",
                "cmp": "eq",
                "left": {"op": "ref", "name": FT_COND},
                "right": {
                    "op": "category_literal",
                    "fact_type": {"id": FT_COND, "version": "v1"},
                    "value": "yes",
                },
            },
            "members": [{"op": "ref", "name": FT_MUTATION_MEMBER}],
        },
        "value": "ok",
    }

    runwide_rule = {
        "schema": "rule-artifact.v14",
        "id": RULE_RUNWIDE_ID,
        "version": "v1",
        "scope": dict(PACKAGE_SCOPE),
        "role": "computation",
        "subject": {"id": FT_CHILD, "version": "v1"},
        "requires": [FT_COND],
        "publishes": PUB_RUNWIDE,
        "pins": [],
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "when": {
            "op": "conditional_dependency_set",
            "condition": {
                "op": "categorical_compare",
                "cmp": "eq",
                "left": {"op": "ref", "name": FT_COND},
                "right": {
                    "op": "category_literal",
                    "fact_type": {"id": FT_COND, "version": "v1"},
                    "value": "yes",
                },
            },
            "members": [{"op": "ref", "name": FT_RUNWIDE}],
        },
        "value": "ok",
    }

    package = {
        "schema": "artifact-package.v36",
        "id": "demo.package.dtb",
        "version": "v2",
        "scope": dict(PACKAGE_SCOPE),
        "admitted_schemas": ["bundle.v2", "rule-artifact.v14"],
        "composition_obligations": [],
        "conflict_semantics": [],
        "members": [
            {"role": "fact-type-bundle", "schema": "bundle.v2", "id": bundle["id"], "version": "v1"},
            {"role": "computation", "schema": "rule-artifact.v14", "id": rule["id"], "version": "v1"},
            {"role": "computation", "schema": "rule-artifact.v14", "id": mutation_rule["id"], "version": "v1"},
            {"role": "computation", "schema": "rule-artifact.v14", "id": runwide_rule["id"], "version": "v1"},
        ],
        "entrypoints": [
            {"id": rule["id"], "version": "v1"},
            {"id": mutation_rule["id"], "version": "v1"},
            {"id": runwide_rule["id"], "version": "v1"},
        ],
        "input_bindings": [
            {"symbol": FT_CHILD, "fact_type": {"id": FT_CHILD, "version": "v1"}, "mode": "required"},
            {"symbol": FT_COND, "fact_type": {"id": FT_COND, "version": "v1"}, "mode": "required"},
            {"symbol": FT_MEMBER, "fact_type": {"id": FT_MEMBER, "version": "v1"}, "mode": "required"},
            {"symbol": FT_MUTATION_MEMBER, "fact_type": {"id": FT_MUTATION_MEMBER, "version": "v1"}, "mode": "required"},
            {"symbol": FT_RUNWIDE, "fact_type": {"id": FT_RUNWIDE, "version": "v1"}, "mode": "required"},
        ],
    }
    package["package_checksum"] = package_instance_checksum(package)

    member_dir = root / "members"
    release_dir = root / "releases"
    member_dir.mkdir(parents=True, exist_ok=True)
    release_dir.mkdir(parents=True, exist_ok=True)

    for body in (bundle, rule, mutation_rule, runwide_rule, package):
        (member_dir / f"{body['id']}.{body['version']}.json").write_text(
            json.dumps(body, sort_keys=True, separators=(",", ":")), encoding="utf-8"
        )

    registry = {
        "citizens": [
            {"id": bundle["id"], "version": bundle["version"], "checksum": citizen_checksum(bundle)},
            {"id": rule["id"], "version": rule["version"], "checksum": citizen_checksum(rule)},
            {"id": mutation_rule["id"], "version": mutation_rule["version"], "checksum": citizen_checksum(mutation_rule)},
            {"id": runwide_rule["id"], "version": runwide_rule["version"], "checksum": citizen_checksum(runwide_rule)},
        ],
        "packages": [{"id": package["id"], "version": package["version"], "checksum": package["package_checksum"]}],
    }
    registry_path = root / "published-packages.json"
    registry_path.write_text(json.dumps(registry, sort_keys=True, separators=(",", ":")), encoding="utf-8")

    release = {
        "schema": "release-registry.v1",
        "id": "demo.release.dtb",
        "version": "v1",
        "package_registry_sha256": hashlib.sha256(registry_path.read_bytes()).hexdigest(),
    }
    release_bytes = json.dumps(release, sort_keys=True, separators=(",", ":")).encode("utf-8")
    (release_dir / "demo.release.dtb.v1.json").write_bytes(release_bytes)

    schemas = DerivationSchemas()
    citizens: dict[tuple[str, str], dict[str, Any]] = {
        (str(bundle["id"]), str(bundle["version"])): bundle,
        (str(rule["id"]), str(rule["version"])): rule,
        (str(mutation_rule["id"]), str(mutation_rule["version"])): mutation_rule,
        (str(runwide_rule["id"]), str(runwide_rule["version"])): runwide_rule,
    }
    validation = validate_package(package, citizens, schemas)
    assert validation.ok, validation.issues

    surface = PublicationSurface(release_dir, registry_path, member_dir)
    return surface, bundle, package, release


def _run_coordinate(
    workspace_dir: Path,
    surface: PublicationSurface,
    bundle: dict[str, Any],
    package: dict[str, Any],
    release: dict[str, Any],
    children_answers: dict[str, dict[str, Any]],
    *,
    extra_acts: list[dict[str, Any]] | None = None,
    run_id: str = "demo.dtb.run",
) -> tuple[Any, dict[str, Any]]:
    release_path = surface.release_dir / f"{release['id']}.{release['version']}.json"
    release_bytes = release_path.read_bytes()

    def act(idx: int, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "schema": "act.v1",
            "act_id": f"demo.act.{idx:03d}",
            "kind": kind,
            "actor": USER,
            "at": f"2026-10-27T00:00:{idx:02d}Z",
            "committed_against": idx,
            "payload": payload,
        }

    acts: list[dict[str, Any]] = [act(0, "bundle-adoption", {"bundle": bundle})]
    for child in children_answers:
        acts.append(act(len(acts), "entity-introduced", {
            "entity": {"schema": "entity.v1", "id": child, "kind": FT_CHILD, "label": f"Child {child}"}
        }))
        acts.append(act(len(acts), "assertion", {"finding": {
            "schema": "finding.v2",
            "id": f"demo.finding.child.{child}",
            "fact_id": fact_id_for(FT_CHILD, (("child", child), ("tax-year", YEAR))),
            "value": child,
            "basis": "attested",
            "evidence_ids": [],
        }}))
        for symbol, value in children_answers[child].items():
            suffix = symbol.rsplit(".", 1)[-1]
            acts.append(act(len(acts), "assertion", {"finding": {
                "schema": "finding.v2",
                "id": f"demo.finding.{suffix}.{child}",
                "fact_id": fact_id_for(symbol, (("child", child), ("tax-year", YEAR))),
                "value": value,
                "basis": "attested",
                "evidence_ids": [],
            }}))

    if extra_acts:
        for extra in extra_acts:
            extra_copy = dict(extra)
            extra_copy["committed_against"] = len(acts)
            extra_copy["act_id"] = f"demo.act.{len(acts):03d}"
            acts.append(extra_copy)

    acts.append(act(len(acts), "package-adoption", {
        "package": {"id": package["id"], "version": package["version"], "checksum": package["package_checksum"]},
        "release": {"id": release["id"], "version": release["version"], "checksum": hashlib.sha256(release_bytes).hexdigest()},
        "revision": len(acts) + 1,
        "scope": dict(RUN_SCOPE),
        "audit": {"note": "synthetic dtb adoption"},
    }))

    cap = WorkspaceCapability(workspace_dir)
    outcome = live_coordinate_run(
        cap,
        repo_root=REPO_ROOT,
        authoritative_acts=acts,
        workspace_revision=len(acts),
        run_scope={"jurisdiction": "us", "year": YEAR},
        scope_user=USER,
        request={"schema": "run-request.v1"},
        run_id=run_id,
        governance_pins=[],
        surface=surface,
        output_name=f"{run_id}.json",
    )
    report: dict[str, Any] = {}
    if outcome.output_path and outcome.output_path.exists():
        report = json.loads(outcome.output_path.read_text("utf-8"))
    return outcome, report


def _publications_by_child(
    outcome: Any, symbol_prefix: str
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for pub in (outcome.publications or ()):
        finding = pub.finding
        sym = str(finding.get("symbol", ""))
        if not sym.startswith(symbol_prefix):
            continue
        for child in ("demo-child-1", "demo-child-2"):
            if f"child={child}" in sym:
                result[child] = finding
    return result


def _dispositions_by_child(
    report: dict[str, Any], rule_id: str
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for d in report.get("dispositions", []):
        if d.get("artifact_id") != rule_id:
            continue
        sym = str(d.get("symbol", ""))
        for child in ("demo-child-1", "demo-child-2"):
            if f"child={child}" in sym:
                result[child] = d
    return result


class TestPerSubjectConditionalDependencies(unittest.TestCase):
    """Contract tests for per-subject conditional dependency set."""

    def test_condition_false_member_absent_publishes(self) -> None:
        """1. Condition false, member absent: rule publishes; member is neither named nor pinned."""
        with TemporaryDirectory() as s_dir, TemporaryDirectory() as w_dir:
            surface, bundle, package, release = _build_synthetic_surface(Path(s_dir))
            outcome, report = _run_coordinate(
                Path(w_dir),
                surface,
                bundle,
                package,
                release,
                {"demo-child-1": {FT_COND: "no"}},
            )
            self.assertIsNone(outcome.refusal)
            disps = _dispositions_by_child(report, RULE_MAIN_ID)
            self.assertIn("demo-child-1", disps)
            child_disp = disps["demo-child-1"]

            self.assertEqual(child_disp["disposition"], "published")
            pubs = _publications_by_child(outcome, PUB_OUTCOME)
            self.assertIn("demo-child-1", pubs)
            self.assertEqual(pubs["demo-child-1"].get("value"), "uncontested")

            # Condition finding must be pinned; member finding must NOT be pinned
            input_pins = [p["id"] for p in child_disp.get("pins", []) if p.get("role") == "input"]
            self.assertIn("demo.finding.condition.demo-child-1", input_pins)
            self.assertNotIn("demo.finding.conditional-member.demo-child-1", input_pins)

    def test_condition_false_member_present_is_not_pinned(self) -> None:
        """1b. Condition false, member present: the inactive member is not read or pinned."""
        with TemporaryDirectory() as s_dir, TemporaryDirectory() as w_dir:
            surface, bundle, package, release = _build_synthetic_surface(Path(s_dir))
            outcome, report = _run_coordinate(
                Path(w_dir),
                surface,
                bundle,
                package,
                release,
                {"demo-child-1": {FT_COND: "no", FT_MEMBER: "yes"}},
            )
            self.assertIsNone(outcome.refusal)
            child_disp = _dispositions_by_child(report, RULE_MAIN_ID)["demo-child-1"]
            self.assertEqual(child_disp["disposition"], "published")
            pubs = _publications_by_child(outcome, PUB_OUTCOME)
            self.assertEqual(pubs["demo-child-1"].get("value"), "uncontested")
            pin_ids = [p["id"] for p in child_disp.get("pins", [])]
            self.assertNotIn("demo.finding.conditional-member.demo-child-1", pin_ids)

    def test_condition_true_member_absent_blocks(self) -> None:
        """2. Condition true, member absent: blocks DEPENDENCY_ABSENT naming member for that subject."""
        with TemporaryDirectory() as s_dir, TemporaryDirectory() as w_dir:
            surface, bundle, package, release = _build_synthetic_surface(Path(s_dir))
            outcome, report = _run_coordinate(
                Path(w_dir),
                surface,
                bundle,
                package,
                release,
                {"demo-child-1": {FT_COND: "yes"}},
            )
            self.assertIsNone(outcome.refusal)
            disps = _dispositions_by_child(report, RULE_MAIN_ID)
            self.assertIn("demo-child-1", disps)
            child_disp = disps["demo-child-1"]

            self.assertEqual(child_disp["disposition"], "blocked")
            self.assertEqual(child_disp.get("code"), "DEPENDENCY_ABSENT")
            self.assertEqual(child_disp.get("missing"), [FT_MEMBER])

            # Active condition is pinned; missing member has no finding id to pin
            input_pins = [p["id"] for p in child_disp.get("pins", []) if p.get("role") == "input"]
            self.assertIn("demo.finding.condition.demo-child-1", input_pins)
            self.assertNotIn("demo.finding.conditional-member.demo-child-1", input_pins)

    def test_condition_true_member_present_publishes(self) -> None:
        """3. Condition true, member present: publishes, the member pinned."""
        with TemporaryDirectory() as s_dir, TemporaryDirectory() as w_dir:
            surface, bundle, package, release = _build_synthetic_surface(Path(s_dir))
            outcome, report = _run_coordinate(
                Path(w_dir),
                surface,
                bundle,
                package,
                release,
                {
                    "demo-child-1": {
                        FT_COND: "yes",
                        FT_MEMBER: "yes",
                    }
                },
            )
            self.assertIsNone(outcome.refusal)
            disps = _dispositions_by_child(report, RULE_MAIN_ID)
            self.assertIn("demo-child-1", disps)
            child_disp = disps["demo-child-1"]

            self.assertEqual(child_disp["disposition"], "published")
            pubs = _publications_by_child(outcome, PUB_OUTCOME)
            self.assertIn("demo-child-1", pubs)
            self.assertEqual(pubs["demo-child-1"].get("value"), "contested-won")

            input_pins = [p["id"] for p in child_disp.get("pins", []) if p.get("role") == "input"]
            self.assertIn("demo.finding.condition.demo-child-1", input_pins)
            self.assertIn("demo.finding.conditional-member.demo-child-1", input_pins)

    def test_two_subjects_one_on_each_branch(self) -> None:
        """4. Two subjects in one run, one on each branch: each resolves on its own answers;
        child 2's answer is never bound for child 1 (assert the pins).
        """
        with TemporaryDirectory() as s_dir, TemporaryDirectory() as w_dir:
            surface, bundle, package, release = _build_synthetic_surface(Path(s_dir))
            outcome, report = _run_coordinate(
                Path(w_dir),
                surface,
                bundle,
                package,
                release,
                {
                    "demo-child-1": {FT_COND: "no"},
                    "demo-child-2": {FT_COND: "yes", FT_MEMBER: "yes"},
                },
            )
            self.assertIsNone(outcome.refusal)
            disps = _dispositions_by_child(report, RULE_MAIN_ID)
            self.assertIn("demo-child-1", disps)
            self.assertIn("demo-child-2", disps)

            child_1 = disps["demo-child-1"]
            child_2 = disps["demo-child-2"]

            # Child 1: on false branch, publishes uncontested
            self.assertEqual(child_1["disposition"], "published")
            pubs = _publications_by_child(outcome, PUB_OUTCOME)
            self.assertIn("demo-child-1", pubs)
            self.assertEqual(pubs["demo-child-1"].get("value"), "uncontested")
            c1_pins = [p["id"] for p in child_1.get("pins", []) if p.get("role") == "input"]
            self.assertIn("demo.finding.condition.demo-child-1", c1_pins)
            # Crucial assertion: child 2's answer is NEVER pinned for child 1
            self.assertNotIn("demo.finding.condition.demo-child-2", c1_pins)
            self.assertNotIn("demo.finding.conditional-member.demo-child-2", c1_pins)

            # Child 2: on true branch, publishes contested-won
            self.assertEqual(child_2["disposition"], "published")
            self.assertIn("demo-child-2", pubs)
            self.assertEqual(pubs["demo-child-2"].get("value"), "contested-won")
            c2_pins = [p["id"] for p in child_2.get("pins", []) if p.get("role") == "input"]
            self.assertIn("demo.finding.condition.demo-child-2", c2_pins)
            self.assertIn("demo.finding.conditional-member.demo-child-2", c2_pins)
            # Child 1's condition is never pinned for child 2
            self.assertNotIn("demo.finding.condition.demo-child-1", c2_pins)

    def test_member_present_only_for_other_subject_does_not_satisfy(self) -> None:
        """5. A member answer present only for the other subject does not satisfy this subject."""
        with TemporaryDirectory() as s_dir, TemporaryDirectory() as w_dir:
            surface, bundle, package, release = _build_synthetic_surface(Path(s_dir))
            outcome, report = _run_coordinate(
                Path(w_dir),
                surface,
                bundle,
                package,
                release,
                {
                    # Child 1 needs member because condition is yes, but member is absent for child 1
                    "demo-child-1": {FT_COND: "yes"},
                    # Child 2 has member asserted, but condition is no
                    "demo-child-2": {FT_COND: "no", FT_MEMBER: "yes"},
                },
            )
            self.assertIsNone(outcome.refusal)
            disps = _dispositions_by_child(report, RULE_MAIN_ID)
            self.assertIn("demo-child-1", disps)
            self.assertIn("demo-child-2", disps)

            child_1 = disps["demo-child-1"]
            child_2 = disps["demo-child-2"]

            # Child 1 MUST block on its own missing member despite Child 2 having it
            self.assertEqual(child_1["disposition"], "blocked")
            self.assertEqual(child_1.get("code"), "DEPENDENCY_ABSENT")
            self.assertEqual(child_1.get("missing"), [FT_MEMBER])
            c1_pins = [p["id"] for p in child_1.get("pins", []) if p.get("role") == "input"]
            self.assertNotIn("demo.finding.conditional-member.demo-child-2", c1_pins)

            # Child 2 publishes uncontested
            self.assertEqual(child_2["disposition"], "published")
            pubs = _publications_by_child(outcome, PUB_OUTCOME)
            self.assertIn("demo-child-2", pubs)
            self.assertEqual(pubs["demo-child-2"].get("value"), "uncontested")

    def test_superseding_member_or_condition_rederives(self) -> None:
        """6. Superseding a member or condition answer re-derives."""
        with TemporaryDirectory() as s_dir, TemporaryDirectory() as w_dir:
            surface, bundle, package, release = _build_synthetic_surface(Path(s_dir))

            # Initial run: child 1 has condition yes, member absent -> blocks
            outcome_1, report_1 = _run_coordinate(
                Path(w_dir),
                surface,
                bundle,
                package,
                release,
                {"demo-child-1": {FT_COND: "yes"}},
                run_id="demo.dtb.run-1",
            )
            self.assertIsNone(outcome_1.refusal)
            disps_1 = _dispositions_by_child(report_1, RULE_MAIN_ID)
            self.assertEqual(disps_1["demo-child-1"]["disposition"], "blocked")

            # Second run: supply the missing member -> re-derives and publishes contested-won
            member_act = {
                "schema": "act.v1",
                "kind": "assertion",
                "actor": USER,
                "at": "2026-10-27T00:01:00Z",
                "payload": {
                    "finding": {
                        "schema": "finding.v2",
                        "id": "demo.finding.conditional-member.demo-child-1",
                        "fact_id": fact_id_for(FT_MEMBER, (("child", "demo-child-1"), ("tax-year", YEAR))),
                        "value": "yes",
                        "basis": "attested",
                        "evidence_ids": [],
                    }
                },
            }
            outcome_2, report_2 = _run_coordinate(
                Path(w_dir),
                surface,
                bundle,
                package,
                release,
                {"demo-child-1": {FT_COND: "yes"}},
                extra_acts=[member_act],
                run_id="demo.dtb.run-2",
            )
            self.assertIsNone(outcome_2.refusal)
            disps_2 = _dispositions_by_child(report_2, RULE_MAIN_ID)
            self.assertEqual(disps_2["demo-child-1"]["disposition"], "published")
            pubs_2 = _publications_by_child(outcome_2, PUB_OUTCOME)
            self.assertIn("demo-child-1", pubs_2)
            self.assertEqual(pubs_2["demo-child-1"].get("value"), "contested-won")
            c1_pins_2 = [p["id"] for p in disps_2["demo-child-1"].get("pins", []) if p.get("role") == "input"]
            self.assertIn("demo.finding.conditional-member.demo-child-1", c1_pins_2)

            # Third run: supersede condition from yes to no -> re-derives, publishes uncontested, member no longer pinned
            cond_supersede_act = {
                "schema": "act.v1",
                "kind": "assertion",
                "actor": USER,
                "at": "2026-10-27T00:02:00Z",
                "payload": {
                    "finding": {
                        "schema": "finding.v2",
                        "id": "demo.finding.condition.demo-child-1.successor",
                        "fact_id": fact_id_for(FT_COND, (("child", "demo-child-1"), ("tax-year", YEAR))),
                        "value": "no",
                        "basis": "attested",
                        "evidence_ids": [],
                    }
                },
            }
            outcome_3, report_3 = _run_coordinate(
                Path(w_dir),
                surface,
                bundle,
                package,
                release,
                {"demo-child-1": {FT_COND: "yes"}},
                extra_acts=[member_act, cond_supersede_act],
                run_id="demo.dtb.run-3",
            )
            self.assertIsNone(outcome_3.refusal)
            disps_3 = _dispositions_by_child(report_3, RULE_MAIN_ID)
            self.assertEqual(disps_3["demo-child-1"]["disposition"], "published")
            pubs_3 = _publications_by_child(outcome_3, PUB_OUTCOME)
            self.assertIn("demo-child-1", pubs_3)
            self.assertEqual(pubs_3["demo-child-1"].get("value"), "uncontested")
            c1_pins_3 = [p["id"] for p in disps_3["demo-child-1"].get("pins", []) if p.get("role") == "input"]
            self.assertIn("demo.finding.condition.demo-child-1.successor", c1_pins_3)
            self.assertNotIn("demo.finding.conditional-member.demo-child-1", c1_pins_3)

    def test_mutation_member_in_requires_remains_required(self) -> None:
        """7. Mutation test: a member also listed in requires still behaves as required (unchanged)."""
        with TemporaryDirectory() as s_dir, TemporaryDirectory() as w_dir:
            surface, bundle, package, release = _build_synthetic_surface(Path(s_dir))
            # Child 1: condition is 'no', required-member is omitted
            outcome, report = _run_coordinate(
                Path(w_dir),
                surface,
                bundle,
                package,
                release,
                {"demo-child-1": {FT_COND: "no"}},
            )
            self.assertIsNone(outcome.refusal)
            disps = _dispositions_by_child(report, RULE_MUTATION_ID)
            self.assertIn("demo-child-1", disps)
            child_disp = disps["demo-child-1"]

            # Because required-member is in requires, it MUST block even when condition is 'no'
            self.assertEqual(child_disp["disposition"], "blocked")
            self.assertEqual(child_disp.get("code"), "DEPENDENCY_ABSENT")
            self.assertEqual(child_disp.get("missing"), [FT_MUTATION_MEMBER])

    def test_conditional_member_not_pinned_when_required_input_absent(self) -> None:
        """Finding 4(a): A present conditional member must not be pinned when required input is absent."""
        with TemporaryDirectory() as s_dir, TemporaryDirectory() as w_dir:
            surface, bundle, package, release = _build_synthetic_surface(Path(s_dir))
            outcome, report = _run_coordinate(
                Path(w_dir),
                surface,
                bundle,
                package,
                release,
                {"c1": {FT_MEMBER: "yes"}},
            )
            disp = next(d for d in report["dispositions"] if d["artifact_id"] == RULE_MAIN_ID)
            self.assertEqual(disp["disposition"], "blocked")
            self.assertEqual(disp.get("code"), "DEPENDENCY_ABSENT")
            self.assertEqual(disp.get("missing"), [FT_COND])
            input_pins = [p["id"] for p in disp.get("pins", []) if p.get("role") == "input"]
            self.assertIn("demo.finding.child.c1", input_pins)
            self.assertNotIn("demo.finding.conditional-member.c1", input_pins)

    def test_conditional_member_does_not_fall_back_to_run_wide_symbol(self) -> None:
        """Finding 4(b): A conditional member in a subject rule must not fall back to a run-wide symbol."""
        with TemporaryDirectory() as s_dir, TemporaryDirectory() as w_dir:
            surface, bundle, package, release = _build_synthetic_surface(Path(s_dir))
            runwide_act = {
                "schema": "act.v1",
                "kind": "assertion",
                "actor": USER,
                "at": "2026-10-27T00:00:50Z",
                "payload": {
                    "finding": {
                        "schema": "finding.v2",
                        "id": "demo.finding.runwide",
                        "fact_id": f"{FT_RUNWIDE}|tax-year={YEAR}",
                        "value": "yes",
                        "basis": "attested",
                        "evidence_ids": [],
                    }
                },
            }
            outcome, report = _run_coordinate(
                Path(w_dir),
                surface,
                bundle,
                package,
                release,
                {"demo-child-1": {FT_COND: "yes"}},
                extra_acts=[runwide_act],
            )
            disps = _dispositions_by_child(report, RULE_RUNWIDE_ID)
            self.assertIn("demo-child-1", disps)
            child_disp = disps["demo-child-1"]
            # Because FT_RUNWIDE does not share subject identity keys, it is never bound from run-wide symbols
            self.assertEqual(child_disp["disposition"], "blocked")
            self.assertEqual(child_disp.get("code"), "DEPENDENCY_ABSENT")
            self.assertEqual(child_disp.get("missing"), [FT_RUNWIDE])


if __name__ == "__main__":
    unittest.main()
