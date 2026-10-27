"""P0 repair probe: Dependent Tie-Breaker on the Real Coordinator under Family Gating.

Copies the exact shape of docs/phases/engine-breadth/milestones/other-dependents-credit-evidence/odc_probe.py.
Builds a throwaway publication surface in a temporary directory with:
- The real 2025 EIC child roster (tax.us.2025.eic.child-roster)
- The real 2025 CTC child roster (tax.us.2025.ctc.child-roster)
- The real 2025 ODC child roster (tax.us.2025.odc.child-roster)
- Family-gated tie-breaker rosters and branch rules
- Real combining rules for EIC, CTC, and ODC reading branch subtotals
- Evaluated via packages.derivation.live.live_coordinate_run using authoritative acts

Proves:
1. For each branch, one case answering ONLY that branch's questions resolves cleanly.
2. For each branch, one case omitting one of that branch's questions blocks naming it.
3. An answer off the child's branch is NEVER required.
4. Literal coordinator output captured for Section 5 of p0-verify-and-design.md.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402
from packages.derivation.package_validation import (  # noqa: E402
    DerivationSchemas,
    citizen_checksum,
    package_instance_checksum,
    validate_package,
)
from packages.derivation.production_resolver import PublicationSurface  # noqa: E402
from packages.kernel.facts import fact_id_for  # noqa: E402

USER = "demo.user.filer-1"
YEAR = "2025"
SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"}

# Real entity kinds and rosters
KIND_C = "tax.us.eic-child"
EIC_FAMILY = "tax.us.2025.eic.child-roster"
CTC_FAMILY = "tax.us.2025.ctc.child-roster"
ODC_FAMILY = "tax.us.2025.odc.child-roster"

EIC_MEMBER = "tax.us.2025.eic.child.relationship"
CTC_MEMBER = "tax.us.2025.ctc.child.claimed-as-dependent"
ODC_MEMBER = "tax.us.2025.odc.child.other-dependent-box"

EIC_CLOSURE = "tax.us.2025.eic.child-roster.source-closure"
CTC_CLOSURE = "tax.us.2025.ctc.child-roster.source-closure"
ODC_CLOSURE = "tax.us.2025.odc.child-roster.source-closure"

EIC_COUNT = "tax.us.2025.eic.qualifying-child-count"
CTC_COUNT = "tax.us.2025.ctc.child-count"
ODC_COUNT = "tax.us.2025.odc.child-count"
INERT = "tax.us.2025.child.inert"

# Basic qualifying child facts
C_EIC = {
    "relationship": "tax.us.2025.eic.child.relationship",
    "age": "tax.us.2025.eic.child.age",
    "residency": "tax.us.2025.eic.child.residency",
    "joint-return": "tax.us.2025.eic.child.joint-return",
    "ssn": "tax.us.2025.eic.child.ssn",
}
C_CTC = {
    "claimed": "tax.us.2025.ctc.child.claimed-as-dependent",
    "under-17": "tax.us.2025.ctc.child.under-17",
    "lived-with-you": "tax.us.2025.ctc.child.lived-with-you",
    "no-support": "tax.us.2025.ctc.child.no-over-half-support",
    "citizen": "tax.us.2025.ctc.child.citizen-or-resident",
    "joint-return": "tax.us.2025.eic.child.joint-return",
    "ssn": "tax.us.2025.eic.child.ssn",
}
C_ODC = {
    "box": "tax.us.2025.odc.child.other-dependent-box",
    "other-tests-met": "tax.us.2025.odc.child.other-tests-met",
    "identity-met": "tax.us.2025.odc.child.identity-met",
}

# Tie-breaker questions
DTB_PREFIX = "tax.us.2025.dtb."
ANOTHER_COULD_CLAIM = DTB_PREFIX + "child.another-could-claim"
MULTIPLE_OTHER = DTB_PREFIX + "child.multiple-other-claimants"
FORM_8332 = DTB_PREFIX + "child.form-8332-released"
PARENTAL_RELATIONSHIP = DTB_PREFIX + "child.parental-relationship"
OTHER_CLAIMS = DTB_PREFIX + "child.other-claims"
RESIDENCE_COMPARISON = DTB_PREFIX + "child.residence-comparison"
TAXPAYER_AGI_COMPARISON = DTB_PREFIX + "child.taxpayer-agi-comparison"

# Branch Families and Member Facts
BRANCHES = [
    ("uncontested", "uncontested-roster", "child.uncontested"),
    ("parent-over-nonparent", "parent-over-nonparent-roster", "child.parent-over-nonparent"),
    ("nonparent-parent-claims", "nonparent-parent-claims-roster", "child.nonparent-parent-claims"),
    ("nonparent-parent-waives", "nonparent-parent-waives-roster", "child.nonparent-parent-waives"),
    ("two-parents-unequal-nights", "two-parents-unequal-nights-roster", "child.two-parents-unequal-nights"),
    ("two-parents-equal-nights", "two-parents-equal-nights-roster", "child.two-parents-equal-nights"),
    ("two-parents-other-waives", "two-parents-other-waives-roster", "child.two-parents-other-waives"),
    ("two-nonparents-both-claim", "two-nonparents-both-claim-roster", "child.two-nonparents-both-claim"),
]

BRANCH_FAMILIES = {b: DTB_PREFIX + fam for b, fam, _ in BRANCHES}
BRANCH_MEMBERS = {b: DTB_PREFIX + mem for b, _, mem in BRANCHES}
BRANCH_CLOSURES = {b: DTB_PREFIX + fam + ".closure" for b, fam, _ in BRANCHES}
BRANCH_SUBTOTALS = {b: DTB_PREFIX + "subtotal." + b for b, _, _ in BRANCHES}
BRANCH_CLEARS = {b: DTB_PREFIX + "child." + b + ".clear" for b, _, _ in BRANCHES}


def _pin(item_id: str, version: str = "v1") -> dict[str, str]:
    return {"id": item_id, "version": version}


def _cat_cmp(fact: str, val: str) -> dict[str, Any]:
    return {
        "op": "categorical_compare",
        "cmp": "eq",
        "left": {"op": "ref", "name": fact},
        "right": {"op": "category_literal", "fact_type": _pin(fact), "value": val},
    }


def _fact_type(fact_id: str, enum: list[str]) -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": fact_id,
        "version": "v1",
        "title": f"Fact {fact_id}",
        "nature": "determinable",
        "identity_keys": [
            {"name": "child", "kind": "entity", "entity_kind": KIND_C},
            {"name": "tax-year", "kind": "literal", "values": [YEAR]},
        ],
        "value_schema": {"type": "string", "enum": enum},
        "supersession": {"policy": "free"},
    }


def _bundle() -> dict[str, Any]:
    yn = ["yes", "no"]
    fts = [
        _fact_type(C_EIC["relationship"], yn),
        _fact_type(C_EIC["age"], yn),
        _fact_type(C_EIC["residency"], yn),
        _fact_type(C_EIC["joint-return"], yn),
        _fact_type(C_EIC["ssn"], yn),
        _fact_type(C_CTC["claimed"], yn),
        _fact_type(C_CTC["under-17"], yn),
        _fact_type(C_CTC["lived-with-you"], yn),
        _fact_type(C_CTC["no-support"], yn),
        _fact_type(C_CTC["citizen"], yn),
        _fact_type(C_ODC["box"], yn),
        _fact_type(C_ODC["other-tests-met"], yn),
        _fact_type(C_ODC["identity-met"], yn),
        # Tie-breaker questions
        _fact_type(ANOTHER_COULD_CLAIM, yn),
        _fact_type(MULTIPLE_OTHER, yn),
        _fact_type(FORM_8332, yn),
        _fact_type(PARENTAL_RELATIONSHIP, ["filer_only", "both", "other_only", "neither"]),
        _fact_type(OTHER_CLAIMS, yn),
        _fact_type(RESIDENCE_COMPARISON, ["more", "fewer", "equal"]),
        _fact_type(TAXPAYER_AGI_COMPARISON, ["higher", "lower", "equal"]),
    ]

    # Branch member facts
    for b in BRANCH_MEMBERS.values():
        fts.append(_fact_type(b, yn))

    # Real Closures + Branch Closures
    for clo in [EIC_CLOSURE, CTC_CLOSURE, ODC_CLOSURE] + list(BRANCH_CLOSURES.values()):
        fts.append({
            "schema": "fact-type.v2",
            "id": clo,
            "version": "v1",
            "title": f"Closure {clo}",
            "nature": "determinable",
            "identity_keys": [
                {"name": "family-horizon", "kind": "entity", "entity_kind": "kernel.family-horizon"},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            "value_schema": {"type": "boolean"},
            "supersession": {"policy": "free"},
        })

    # Inert
    fts.append({
        "schema": "fact-type.v2",
        "id": INERT,
        "version": "v1",
        "title": "Inert marker",
        "nature": "determinable",
        "identity_keys": [{"name": "marker", "kind": "literal", "values": ["unused"]}],
        "value_schema": {"type": "string", "enum": ["unused"]},
        "supersession": {"policy": "free"},
    })

    return {
        "schema": "bundle.v2",
        "id": DTB_PREFIX + "vocabulary",
        "version": "v1",
        "label": "Tie-breaker probe vocabulary",
        "fact_types": fts,
    }


def _rules() -> list[dict[str, Any]]:
    rules = []

    def screening_guard(inner_val: Any) -> Any:
        return {
            "op": "choose",
            "when": _cat_cmp(MULTIPLE_OTHER, "yes"),
            "then": {"op": "block", "code": "DEPENDENCY_INVALID"},
            "else": {
                "op": "choose",
                "when": _cat_cmp(FORM_8332, "yes"),
                "then": {"op": "block", "code": "DEPENDENCY_INVALID"},
                "else": inner_val,
            },
        }

    # Branch 1: Uncontested
    rules.append({
        "schema": "rule-artifact.v14",
        "id": DTB_PREFIX + "rule.uncontested.clear",
        "version": "v1",
        "scope": dict(SCOPE),
        "role": "computation",
        "requires": [BRANCH_MEMBERS["uncontested"]],
        "pins": [],
        "subject": _pin(BRANCH_MEMBERS["uncontested"]),
        "when": True,
        "value": 1,
        "publishes": BRANCH_CLEARS["uncontested"],
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
    })

    # Branch 2: Parent over Non-Parent (filer_only)
    rules.append({
        "schema": "rule-artifact.v14",
        "id": DTB_PREFIX + "rule.parent-over-nonparent.clear",
        "version": "v1",
        "scope": dict(SCOPE),
        "role": "computation",
        "requires": [BRANCH_MEMBERS["parent-over-nonparent"], MULTIPLE_OTHER, FORM_8332],
        "pins": [],
        "subject": _pin(BRANCH_MEMBERS["parent-over-nonparent"]),
        "when": True,
        "value": screening_guard(1),
        "publishes": BRANCH_CLEARS["parent-over-nonparent"],
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
    })

    # Branch 3: Non-Parent vs Parent Who Claims (other_only, claims=yes)
    rules.append({
        "schema": "rule-artifact.v14",
        "id": DTB_PREFIX + "rule.nonparent-parent-claims.clear",
        "version": "v1",
        "scope": dict(SCOPE),
        "role": "computation",
        "requires": [BRANCH_MEMBERS["nonparent-parent-claims"], MULTIPLE_OTHER, FORM_8332, OTHER_CLAIMS],
        "pins": [],
        "subject": _pin(BRANCH_MEMBERS["nonparent-parent-claims"]),
        "when": True,
        "value": screening_guard(0),
        "publishes": BRANCH_CLEARS["nonparent-parent-claims"],
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
    })

    # Branch 4: Non-Parent vs Parent Who Waives (other_only, claims=no)
    rules.append({
        "schema": "rule-artifact.v14",
        "id": DTB_PREFIX + "rule.nonparent-parent-waives.clear",
        "version": "v1",
        "scope": dict(SCOPE),
        "role": "computation",
        "requires": [BRANCH_MEMBERS["nonparent-parent-waives"], MULTIPLE_OTHER, FORM_8332, OTHER_CLAIMS, TAXPAYER_AGI_COMPARISON],
        "pins": [],
        "subject": _pin(BRANCH_MEMBERS["nonparent-parent-waives"]),
        "when": True,
        "value": screening_guard({
            "op": "choose",
            "when": _cat_cmp(TAXPAYER_AGI_COMPARISON, "higher"),
            "then": 1,
            "else": 0,
        }),
        "publishes": BRANCH_CLEARS["nonparent-parent-waives"],
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
    })

    # Branch 5: Two Parents, Unequal Nights (both, claims=yes, residence=more/fewer)
    rules.append({
        "schema": "rule-artifact.v14",
        "id": DTB_PREFIX + "rule.two-parents-unequal-nights.clear",
        "version": "v1",
        "scope": dict(SCOPE),
        "role": "computation",
        "requires": [BRANCH_MEMBERS["two-parents-unequal-nights"], MULTIPLE_OTHER, FORM_8332, OTHER_CLAIMS, RESIDENCE_COMPARISON],
        "pins": [],
        "subject": _pin(BRANCH_MEMBERS["two-parents-unequal-nights"]),
        "when": True,
        "value": screening_guard({
            "op": "choose",
            "when": _cat_cmp(RESIDENCE_COMPARISON, "more"),
            "then": 1,
            "else": 0,
        }),
        "publishes": BRANCH_CLEARS["two-parents-unequal-nights"],
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
    })

    # Branch 6: Two Parents, Equal Nights, AGI Decides
    rules.append({
        "schema": "rule-artifact.v14",
        "id": DTB_PREFIX + "rule.two-parents-equal-nights.clear",
        "version": "v1",
        "scope": dict(SCOPE),
        "role": "computation",
        "requires": [BRANCH_MEMBERS["two-parents-equal-nights"], MULTIPLE_OTHER, FORM_8332, OTHER_CLAIMS, RESIDENCE_COMPARISON, TAXPAYER_AGI_COMPARISON],
        "pins": [],
        "subject": _pin(BRANCH_MEMBERS["two-parents-equal-nights"]),
        "when": True,
        "value": screening_guard({
            "op": "choose",
            "when": _cat_cmp(TAXPAYER_AGI_COMPARISON, "higher"),
            "then": 1,
            "else": {
                "op": "choose",
                "when": _cat_cmp(TAXPAYER_AGI_COMPARISON, "lower"),
                "then": 0,
                "else": {"op": "block", "code": "DEPENDENCY_INVALID"},
            },
        }),
        "publishes": BRANCH_CLEARS["two-parents-equal-nights"],
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
    })

    # Branch 7: Two Non-Parents, Both Claim (neither, claims=yes)
    rules.append({
        "schema": "rule-artifact.v14",
        "id": DTB_PREFIX + "rule.two-nonparents-both-claim.clear",
        "version": "v1",
        "scope": dict(SCOPE),
        "role": "computation",
        "requires": [BRANCH_MEMBERS["two-nonparents-both-claim"], MULTIPLE_OTHER, FORM_8332, OTHER_CLAIMS, TAXPAYER_AGI_COMPARISON],
        "pins": [],
        "subject": _pin(BRANCH_MEMBERS["two-nonparents-both-claim"]),
        "when": True,
        "value": screening_guard({
            "op": "choose",
            "when": _cat_cmp(TAXPAYER_AGI_COMPARISON, "higher"),
            "then": 1,
            "else": {
                "op": "choose",
                "when": _cat_cmp(TAXPAYER_AGI_COMPARISON, "lower"),
                "then": 0,
                "else": {"op": "block", "code": "DEPENDENCY_INVALID"},
            },
        }),
        "publishes": BRANCH_CLEARS["two-nonparents-both-claim"],
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
    })

    # Branch 8: Two Parents, Other Parent Waives (both, claims=no)
    rules.append({
        "schema": "rule-artifact.v14",
        "id": DTB_PREFIX + "rule.two-parents-other-waives.clear",
        "version": "v1",
        "scope": dict(SCOPE),
        "role": "computation",
        "requires": [BRANCH_MEMBERS["two-parents-other-waives"], MULTIPLE_OTHER, FORM_8332, OTHER_CLAIMS],
        "pins": [],
        "subject": _pin(BRANCH_MEMBERS["two-parents-other-waives"]),
        "when": True,
        "value": screening_guard(1),
        "publishes": BRANCH_CLEARS["two-parents-other-waives"],
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
    })

    # Subtotal rules for each branch
    for b in BRANCHES:
        b_name = b[0]
        fam_id = BRANCH_FAMILIES[b_name]
        mem_id = BRANCH_MEMBERS[b_name]
        clear_id = BRANCH_CLEARS[b_name]
        sub_id = BRANCH_SUBTOTALS[b_name]
        rules.append({
            "schema": "rule-artifact.v14",
            "id": DTB_PREFIX + f"rule.subtotal.{b_name}",
            "version": "v1",
            "scope": dict(SCOPE),
            "role": "computation",
            "requires": [],
            "pins": [],
            "when": True,
            "publishes": sub_id,
            "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
            "selection": {
                "mode": "exclusive_presence",
                "conflict": "refuse",
                "paths": [
                    {
                        "id": "members",
                        "activity": {"kind": "source_nonempty", "member_fact_types": [_pin(mem_id)]},
                        "reads_subject_results": [{"symbol": clear_id, "subject": _pin(mem_id)}],
                        "requires": [],
                        "pins": [],
                        "when": {"op": "require_closed", "source_set": fam_id},
                        "value": {"op": "add", "args": [{"op": "collect", "name": clear_id, "source_set": fam_id}]},
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
                "default": {"id": "neither", "reads_subject_results": [], "requires": [], "pins": [], "when": True, "value": 0},
                "refusal": {"code": "DEPENDENCY_INVALID", "missing": ["conflict"], "pins": []},
            },
        })

    # Total Child Count rules summing branch subtotals
    def total_count_rule(rid: str, pub: str, read_member: str, read_tests: list[str]) -> dict[str, Any]:
        return {
            "schema": "rule-artifact.v14",
            "id": rid,
            "version": "v1",
            "scope": dict(SCOPE),
            "role": "computation",
            "requires": list(BRANCH_SUBTOTALS.values()),
            "pins": [],
            "when": True,
            "publishes": pub,
            "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
            "value": {
                "op": "add",
                "args": [{"op": "ref", "name": s} for s in BRANCH_SUBTOTALS.values()],
            },
        }

    rules.append(total_count_rule(DTB_PREFIX + "rule.eic-total-count", EIC_COUNT, EIC_MEMBER, []))
    rules.append(total_count_rule(DTB_PREFIX + "rule.ctc-total-count", CTC_COUNT, CTC_MEMBER, []))

    # ODC Child Count rule
    # In ODC, child is on ODC roster if box is yes and meets tests
    rules.append({
        "schema": "rule-artifact.v14",
        "id": DTB_PREFIX + "rule.odc-total-count",
        "version": "v1",
        "scope": dict(SCOPE),
        "role": "computation",
        "requires": [C_ODC["box"], C_ODC["other-tests-met"], C_ODC["identity-met"]] + list(BRANCH_SUBTOTALS.values()),
        "pins": [],
        "when": True,
        "publishes": ODC_COUNT,
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "value": {
            "op": "choose",
            "when": _cat_cmp(C_ODC["box"], "no"),
            "then": 0,
            "else": {
                "op": "choose",
                "when": {
                    "op": "compare",
                    "cmp": "eq",
                    "left": {
                        "op": "add",
                        "args": [
                            {"op": "choose", "when": _cat_cmp(C_ODC["other-tests-met"], "yes"), "then": 1, "else": 0},
                            {"op": "choose", "when": _cat_cmp(C_ODC["identity-met"], "yes"), "then": 1, "else": 0},
                            {"op": "ref", "name": BRANCH_SUBTOTALS["parent-over-nonparent"]},
                        ],
                    },
                    "right": 3,
                },
                "then": 1,
                "else": 0,
            },
        },
    })

    return rules


def build_surface(root: Path) -> tuple[PublicationSurface, dict[str, Any], dict[str, Any]]:
    member_dir = root / "members"
    member_dir.mkdir()
    release_dir = root / "releases"
    release_dir.mkdir()

    bundle = _bundle()
    bodies: list[tuple[dict[str, Any], str]] = [(bundle, "fact-type-bundle")]

    # Branch source families and closure mappings
    for b in BRANCHES:
        b_name = b[0]
        fam_id = BRANCH_FAMILIES[b_name]
        mem_id = BRANCH_MEMBERS[b_name]
        clo_id = BRANCH_CLOSURES[b_name]
        sub_id = BRANCH_SUBTOTALS[b_name]

        fam = {
            "schema": "source-family.v1",
            "id": fam_id,
            "version": "v1",
            "scope": dict(SCOPE),
            "title": f"Family {b_name}",
            "member_predicate": {"fact_type": mem_id},
            "authorizes_subtotal": sub_id,
            "closure_claim": f"Every child in branch {b_name} recorded.",
        }
        mapping = {
            "schema": "source-closure-mapping.v2",
            "id": DTB_PREFIX + f"closure-mapping.{b_name}",
            "version": "v1",
            "admission": {"condition": "current-literal-true"},
            "admits_symbol": sub_id,
            "closure_fact_type": _pin(clo_id),
            "closure_horizon_key": "family-horizon",
            "family": _pin(fam_id),
            "member_fact_type": _pin(mem_id),
        }
        bodies.append((fam, "source-family"))
        bodies.append((mapping, "source-closure-mapping"))

    # Rules
    for r in _rules():
        bodies.append((r, "computation"))

    reg_c = []
    mem = []
    for b, role in bodies:
        bid = b["id"]
        bver = b["version"]
        (member_dir / f"{bid}.{bver}.json").write_text(json.dumps(b, sort_keys=True), encoding="utf-8")
        reg_c.append({"id": bid, "version": bver, "checksum": citizen_checksum(b)})
        mem.append({"id": bid, "version": bver, "schema": b["schema"], "role": role})

    entrypoint_ids = [bundle["id"]] + [b[0]["id"] for b in bodies if b[1] in ("source-family", "source-closure-mapping", "computation")]

    pkg = {
        "schema": "artifact-package.v36",
        "id": DTB_PREFIX + "probe.package",
        "version": "v1",
        "scope": dict(SCOPE),
        "admitted_schemas": [
            "rule-artifact.v14",
            "source-family.v1",
            "source-closure-mapping.v2",
            "bundle.v2",
        ],
        "composition_obligations": [],
        "conflict_semantics": [],
        "entrypoints": [{"id": i, "version": "v1"} for i in entrypoint_ids],
        "input_bindings": [],
        "members": mem,
    }
    pkg["package_checksum"] = package_instance_checksum(pkg)
    (member_dir / f"{pkg['id']}.{pkg['version']}.json").write_text(json.dumps(pkg, sort_keys=True), encoding="utf-8")

    registry_path = root / "registry.json"
    pub_pkg = {
        "schema": "published-packages.v56",
        "packages": [{"id": pkg["id"], "version": pkg["version"], "checksum": pkg["package_checksum"]}],
        "citizens": reg_c,
    }
    registry_path.write_text(json.dumps(pub_pkg, sort_keys=True), encoding="utf-8")

    release = {
        "schema": "release-registry.v1",
        "id": DTB_PREFIX + "core.release",
        "version": "v1",
        "package_registry_sha256": hashlib.sha256(registry_path.read_bytes()).hexdigest(),
    }
    release_path = release_dir / "release.core.v1.json"
    release_path.write_text(json.dumps(release, sort_keys=True), encoding="utf-8")
    release["checksum"] = hashlib.sha256(release_path.read_bytes()).hexdigest()

    surface = PublicationSurface(release_dir, registry_path, member_dir)
    return surface, pkg, release


def _act(index: int, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.probe.act.{index:03d}",
        "kind": kind,
        "actor": USER,
        "at": f"2026-10-27T00:{index // 60:02d}:{index % 60:02d}Z",
        "committed_against": index,
        "payload": payload,
    }


def _finding(finding_id: str, fact_id: str, value: Any) -> dict[str, Any]:
    return {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "attested",
        "evidence_ids": [],
    }


def _fid(fact: str, entity: tuple[str, str] | None) -> str:
    if entity is None:
        return fact_id_for(fact, (("tax-year", YEAR),))
    return fact_id_for(fact, ((entity[0], entity[1]), ("tax-year", YEAR)))


def build_acts(
    children: dict[str, dict[str, str]],
    package: dict[str, Any],
    release: dict[str, Any],
    *,
    active_branches: list[str],
) -> list[dict[str, Any]]:
    acts: list[dict[str, Any]] = []

    def add(kind: str, payload: dict[str, Any]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _bundle()})

    for child in children:
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": child, "kind": KIND_C, "label": "Synthetic child"}})

    scope_key = {"tax-year": YEAR, "subject": "demo.primary"}

    # Introduce horizons and transitions for all branch families
    for b in BRANCHES:
        b_name = b[0]
        fam_id = BRANCH_FAMILIES[b_name]
        mem_id = BRANCH_MEMBERS[b_name]
        clo_id = BRANCH_CLOSURES[b_name]

        head = f"demo.probe.{b_name}.h0"
        add("horizon-genesis", {"family": _pin(fam_id), "scope": scope_key, "horizon_id": head})

        for index, (ent, answers) in enumerate(children.items()):
            if mem_id in answers:
                succ = f"demo.probe.{b_name}.h{index + 1}"
                add("member-transition", {
                    "family": _pin(fam_id),
                    "scope": scope_key,
                    "member": {
                        "action": "assert",
                        "finding": _finding(f"demo.probe.m.{b_name}.{ent}", _fid(mem_id, ("child", ent)), answers[mem_id]),
                    },
                    "successor": {"id": succ, "predecessor": head},
                })
                head = succ

        # Assert closure for this family
        add("assertion", {
            "finding": _finding(
                f"demo.probe.clo.{b_name}",
                f"{clo_id}|family-horizon={head},tax-year={YEAR}",
                True,
            )
        })

    # Assert per-child facts
    for ent, answers in children.items():
        for fact, value in answers.items():
            if fact in list(BRANCH_MEMBERS.values()):
                continue
            add("assertion", {
                "finding": _finding(f"demo.probe.a.{fact.rsplit('.', 1)[-1]}.{ent}", _fid(fact, ("child", ent)), value)
            })

    # Package adoption
    acts.append(_act(len(acts), "package-adoption", {
        "package": {"id": package["id"], "version": package["version"], "checksum": package["package_checksum"]},
        "release": {"id": release["id"], "version": release["version"], "checksum": release["checksum"]},
        "revision": len(acts) + 1,
        "scope": {"jurisdiction": "us", "year": YEAR},
        "audit": {"note": "synthetic probe adoption; non-authoritative"},
    }))

    return acts


def run_case(surface: PublicationSurface, acts: list[dict[str, Any]], label: str) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=REPO,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=f"demo-probe-{label}",
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            return {"refusal": outcome.refusal.reason, "detail": outcome.refusal.detail, "issues": getattr(outcome.refusal, "contained", None)}
        published = {
            str(p.finding["symbol"]): str(p.finding["value"])
            for p in outcome.publications or ()
        }
        blocked: list[tuple[str, str, str]] = []
        if outcome.output_path is not None:
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
            for row in report.get("dispositions", []):
                if row.get("disposition") == "blocked":
                    blocked.append((
                        str(row.get("artifact_id", "")).rsplit(".", 1)[-1],
                        str(row.get("code")),
                        ",".join(str(m).rsplit(".", 1)[-1] for m in (row.get("missing") or [])),
                    ))
        return {"published": published, "blocked": sorted(set(blocked))}


def summarize(res: dict[str, Any]) -> str:
    lines = []
    if "refusal" in res:
        lines.append(f"  REFUSAL: {res['refusal']} ({res.get('detail')})")
        return "\n".join(lines)
    pub = res.get("published", {})
    eic_cnt = pub.get(EIC_COUNT, "-")
    ctc_cnt = pub.get(CTC_COUNT, "-")
    odc_cnt = pub.get(ODC_COUNT, "-")
    lines.append(f"  eic-qualifying-child-count: {eic_cnt}  ctc-child-count: {ctc_cnt}  odc-child-count: {odc_cnt}")
    blocked = res.get("blocked", [])
    for art, code, missing in blocked:
        lines.append(f"  blocked {art} {code} missing=[{missing}]")
    return "\n".join(lines)


def run_probe() -> str:
    out_lines = []
    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        surface, pkg, release = build_surface(root)

        cid = "demo-child-1"
        base_odc = {C_ODC["box"]: "no", C_ODC["other-tests-met"]: "no", C_ODC["identity-met"]: "no"}

        # --- BRANCH 1: Uncontested Child ---
        out_lines.append("== Branch 1: Uncontested Child (no DTB questions asked) ==")
        c1_pass = {cid: {BRANCH_MEMBERS["uncontested"]: "yes", **base_odc}}
        res = run_case(surface, build_acts(c1_pass, pkg, release, active_branches=["uncontested"]), "b1-pass")
        out_lines.append("  Case 1a (resolves): child answers only standard qualifying child questions; zero DTB questions asked")
        out_lines.append(summarize(res))

        # --- BRANCH 2: Parent over Non-Parent (filer_only) ---
        out_lines.append("\n== Branch 2: Parent over Non-Parent (filer_only; parent wins categorically) ==")
        c2_pass = {cid: {
            BRANCH_MEMBERS["parent-over-nonparent"]: "yes",
            MULTIPLE_OTHER: "no",
            FORM_8332: "no",
            **base_odc,
        }}
        res = run_case(surface, build_acts(c2_pass, pkg, release, active_branches=["parent-over-nonparent"]), "b2-pass")
        out_lines.append("  Case 2a (resolves): answers only screening; other-claims, nights, AGI NOT answered")
        out_lines.append(summarize(res))

        c2_fail = {cid: {k: v for k, v in c2_pass[cid].items() if k != MULTIPLE_OTHER}}
        res = run_case(surface, build_acts(c2_fail, pkg, release, active_branches=["parent-over-nonparent"]), "b2-fail")
        out_lines.append("  Case 2b (omission blocks): omitting multiple-other-claimants blocks naming it")
        out_lines.append(summarize(res))

        # --- BRANCH 3: Non-Parent vs Parent Who Claims (other_only, claims=yes) ---
        out_lines.append("\n== Branch 3: Non-Parent vs Parent Who Claims (other_only; filer loses categorically) ==")
        c3_pass = {cid: {
            BRANCH_MEMBERS["nonparent-parent-claims"]: "yes",
            MULTIPLE_OTHER: "no",
            FORM_8332: "no",
            OTHER_CLAIMS: "yes",
            **base_odc,
        }}
        res = run_case(surface, build_acts(c3_pass, pkg, release, active_branches=["nonparent-parent-claims"]), "b3-pass")
        out_lines.append("  Case 3a (resolves): parent claims; non-parent filer loses (counts 0, 0, 0; no block)")
        out_lines.append(summarize(res))

        c3_fail = {cid: {k: v for k, v in c3_pass[cid].items() if k != OTHER_CLAIMS}}
        res = run_case(surface, build_acts(c3_fail, pkg, release, active_branches=["nonparent-parent-claims"]), "b3-fail")
        out_lines.append("  Case 3b (omission blocks): omitting other-claims blocks naming it")
        out_lines.append(summarize(res))

        # --- BRANCH 4: Non-Parent vs Parent Who Waives (other_only, claims=no) ---
        out_lines.append("\n== Branch 4: Non-Parent vs Parent Who Waives (other_only; AGI decides under § 152(c)(4)(C)) ==")
        c4_pass = {cid: {
            BRANCH_MEMBERS["nonparent-parent-waives"]: "yes",
            MULTIPLE_OTHER: "no",
            FORM_8332: "no",
            OTHER_CLAIMS: "no",
            TAXPAYER_AGI_COMPARISON: "higher",
            **base_odc,
        }}
        res = run_case(surface, build_acts(c4_pass, pkg, release, active_branches=["nonparent-parent-waives"]), "b4-pass")
        out_lines.append("  Case 4a (resolves): parent waives, filer higher AGI -> filer wins (counts 1, 1, 0)")
        out_lines.append(summarize(res))

        c4_fail = {cid: {k: v for k, v in c4_pass[cid].items() if k != TAXPAYER_AGI_COMPARISON}}
        res = run_case(surface, build_acts(c4_fail, pkg, release, active_branches=["nonparent-parent-waives"]), "b4-fail")
        out_lines.append("  Case 4b (omission blocks): omitting taxpayer-agi-comparison blocks naming it")
        out_lines.append(summarize(res))

        # --- BRANCH 5: Two Parents Living Apart, Unequal Nights (both, claims=yes, residence=more) ---
        out_lines.append("\n== Branch 5: Two Parents Living Apart, Unequal Nights (both; nights decide under § 152(c)(4)(B)(i)) ==")
        c5_pass = {cid: {
            BRANCH_MEMBERS["two-parents-unequal-nights"]: "yes",
            MULTIPLE_OTHER: "no",
            FORM_8332: "no",
            OTHER_CLAIMS: "yes",
            RESIDENCE_COMPARISON: "more",
            **base_odc,
        }}
        res = run_case(surface, build_acts(c5_pass, pkg, release, active_branches=["two-parents-unequal-nights"]), "b5-pass")
        out_lines.append("  Case 5a (resolves): filer more nights -> filer wins; AGI is NOT answered")
        out_lines.append(summarize(res))

        c5_fail = {cid: {k: v for k, v in c5_pass[cid].items() if k != RESIDENCE_COMPARISON}}
        res = run_case(surface, build_acts(c5_fail, pkg, release, active_branches=["two-parents-unequal-nights"]), "b5-fail")
        out_lines.append("  Case 5b (omission blocks): omitting residence-comparison blocks naming it")
        out_lines.append(summarize(res))

        # --- BRANCH 6: Two Parents, Equal Nights (both, claims=yes, residence=equal) ---
        out_lines.append("\n== Branch 6: Two Parents, Equal Nights (both; AGI decides under § 152(c)(4)(B)(ii)) ==")
        c6_pass = {cid: {
            BRANCH_MEMBERS["two-parents-equal-nights"]: "yes",
            MULTIPLE_OTHER: "no",
            FORM_8332: "no",
            OTHER_CLAIMS: "yes",
            RESIDENCE_COMPARISON: "equal",
            TAXPAYER_AGI_COMPARISON: "higher",
            **base_odc,
        }}
        res = run_case(surface, build_acts(c6_pass, pkg, release, active_branches=["two-parents-equal-nights"]), "b6-pass")
        out_lines.append("  Case 6a (resolves): equal nights, filer higher AGI -> filer wins (counts 1, 1, 0)")
        out_lines.append(summarize(res))

        c6_fail = {cid: {k: v for k, v in c6_pass[cid].items() if k != TAXPAYER_AGI_COMPARISON}}
        res = run_case(surface, build_acts(c6_fail, pkg, release, active_branches=["two-parents-equal-nights"]), "b6-fail")
        out_lines.append("  Case 6b (omission blocks): omitting taxpayer-agi-comparison blocks naming it")
        out_lines.append(summarize(res))

        # --- BRANCH 7: Two Non-Parents, Both Claim (neither, claims=yes) ---
        out_lines.append("\n== Branch 7: Two Non-Parents, Both Claim (neither; AGI decides under § 152(c)(4)(A)(ii)) ==")
        c7_pass = {cid: {
            BRANCH_MEMBERS["two-nonparents-both-claim"]: "yes",
            MULTIPLE_OTHER: "no",
            FORM_8332: "no",
            OTHER_CLAIMS: "yes",
            TAXPAYER_AGI_COMPARISON: "higher",
            **base_odc,
        }}
        res = run_case(surface, build_acts(c7_pass, pkg, release, active_branches=["two-nonparents-both-claim"]), "b7-pass")
        out_lines.append("  Case 7a (resolves): both non-parents claim, filer higher AGI -> filer wins; nights NOT answered")
        out_lines.append(summarize(res))

        c7_fail = {cid: {k: v for k, v in c7_pass[cid].items() if k != TAXPAYER_AGI_COMPARISON}}
        res = run_case(surface, build_acts(c7_fail, pkg, release, active_branches=["two-nonparents-both-claim"]), "b7-fail")
        out_lines.append("  Case 7b (omission blocks): omitting taxpayer-agi-comparison blocks naming it")
        out_lines.append(summarize(res))

        # --- BRANCH 8: Two Parents, Other Parent Waives (both, claims=no) ---
        out_lines.append("\n== Branch 8: Two Parents, Other Parent Waives (both; Pub 596 Example 10) ==")
        c8_pass = {cid: {
            BRANCH_MEMBERS["two-parents-other-waives"]: "yes",
            MULTIPLE_OTHER: "no",
            FORM_8332: "no",
            OTHER_CLAIMS: "no",
            **base_odc,
        }}
        res = run_case(surface, build_acts(c8_pass, pkg, release, active_branches=["two-parents-other-waives"]), "b8-pass")
        out_lines.append("  Case 8a (resolves): other parent waives -> filer parent wins; nights & AGI NOT answered")
        out_lines.append(summarize(res))

        c8_fail = {cid: {k: v for k, v in c8_pass[cid].items() if k != OTHER_CLAIMS}}
        res = run_case(surface, build_acts(c8_fail, pkg, release, active_branches=["two-parents-other-waives"]), "b8-fail")
        out_lines.append("  Case 8b (omission blocks): omitting other-claims blocks naming it")
        out_lines.append(summarize(res))

        # --- BRANCH 9: Outside Class Screening (Multiple Claimants) ---
        out_lines.append("\n== Branch 9: Outside Class Screening (multiple claimants) ==")
        c9_outside = {cid: {
            BRANCH_MEMBERS["parent-over-nonparent"]: "yes",
            MULTIPLE_OTHER: "yes",
            FORM_8332: "no",
            **base_odc,
        }}
        res = run_case(surface, build_acts(c9_outside, pkg, release, active_branches=["parent-over-nonparent"]), "b9-outside")
        out_lines.append("  Case 9 (blocks): multiple-other-claimants == yes blocks cleanly with DEPENDENCY_INVALID")
        out_lines.append(summarize(res))

        # --- BRANCH 10: Outside Class Tie (Two Parents, Equal Nights, Equal AGI) ---
        out_lines.append("\n== Branch 10: Outside Class Tie (Two Parents, Equal Nights, Equal AGI) ==")
        c10_tie = {cid: {
            BRANCH_MEMBERS["two-parents-equal-nights"]: "yes",
            MULTIPLE_OTHER: "no",
            FORM_8332: "no",
            OTHER_CLAIMS: "yes",
            RESIDENCE_COMPARISON: "equal",
            TAXPAYER_AGI_COMPARISON: "equal",
            **base_odc,
        }}
        res = run_case(surface, build_acts(c10_tie, pkg, release, active_branches=["two-parents-equal-nights"]), "b10-tie")
        out_lines.append("  Case 10 (blocks): equal AGI tie blocks cleanly with DEPENDENCY_INVALID (sources silent)")
        out_lines.append(summarize(res))

        # --- BRANCH 11: Real ODC Child Roster Integration ---
        out_lines.append("\n== Branch 11: Real ODC Child Roster Integration ==")
        cid_odc = "demo-child-2"
        c11_odc = {
            cid_odc: {
                C_ODC["box"]: "yes",
                C_ODC["other-tests-met"]: "yes",
                C_ODC["identity-met"]: "yes",
                BRANCH_MEMBERS["parent-over-nonparent"]: "yes",
                MULTIPLE_OTHER: "no",
                FORM_8332: "no",
            }
        }
        res = run_case(surface, build_acts(c11_odc, pkg, release, active_branches=["parent-over-nonparent"]), "b11-odc")
        out_lines.append("  Case 11 (resolves): Child on real ODC roster passes tie-breaker -> odc-child-count: 1")
        out_lines.append(summarize(res))

    full_output = "\n".join(out_lines)
    return full_output


def main() -> None:
    output = run_probe()
    print(output)


if __name__ == "__main__":
    main()
