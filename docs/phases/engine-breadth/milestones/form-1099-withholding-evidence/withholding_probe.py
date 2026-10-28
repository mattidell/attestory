"""P0 probe: Form 1099-G and SSA-1099 withholding reaching Form 1040 line 25b.

Builds a throwaway publication surface in a temporary directory and runs synthetic
withholding statements through packages.derivation.live.live_coordinate_run.
Statements are recorded as a filer would: member-transitions with companions,
advancing family horizons from h0 to h1, with family closures asserted at the active horizon.
Nothing in the repository is modified.

Demonstrates:
1. Form 1099-G box 4 withholding reaches line 25b.
2. Form SSA-1099 box 6 voluntary withholding reaches line 25b.
3. A v58-shaped answer set with no withholding gives the same line 25b as on v58 (both publish 0).
4. An unclosed new family blocks with the fact named.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
from decimal import Decimal
from pathlib import Path
from typing import Any

REPO = Path(".").resolve()
sys.path.insert(0, str(REPO))

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.package_validation import citizen_checksum, package_instance_checksum
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.facts import fact_id_for

USER = "demo.user.filer-1"
YEAR = "2025"
SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"}
SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}

# Entity Kinds
KIND_INT_PAYER = "tax.us.interest-payer"
KIND_INT_STMT = "tax.us.1099int-statement"
KIND_DIV_PAYER = "tax.us.dividend-payer"
KIND_DIV_STMT = "tax.us.1099div-statement"
KIND_IRA_PAYER = "tax.us.ira-payer"
KIND_IRA_STMT = "tax.us.1099r-statement"
KIND_G_PAYER = "tax.us.unemployment-payer"
KIND_G_STMT = "tax.us.1099g-statement"
KIND_SSA_STMT = "tax.us.ssa1099-statement"
KIND_HORIZON = "kernel.family-horizon"

# Fact Types
FACT_INT_B1 = "tax.us.2025.f1099int.box1-interest"
FACT_INT_B4 = "tax.us.2025.f1099int.box4-withholding"
FACT_INT_CLOSURE = "tax.us.2025.f1099int.b4.source-closure"

FACT_DIV_B1A = "tax.us.2025.f1099div.box1a-ordinary"
FACT_DIV_B4 = "tax.us.2025.f1099div.box4-withholding"
FACT_DIV_CLOSURE = "tax.us.2025.f1099div.b4.source-closure"

FACT_R_B1 = "tax.us.2025.f1099r.ira-box1-taxable-distribution"
FACT_R_B2A = "tax.us.2025.f1099r.ira-box2a-taxable-amount"
FACT_R_DIST_CODE = "tax.us.2025.f1099r.distribution-code"
FACT_R_IRA_CHECKBOX = "tax.us.2025.f1099r.ira-sep-simple-checkbox"
FACT_R_B2B_NOT_DET = "tax.us.2025.f1099r.box2b-not-determined"
FACT_R_B4 = "tax.us.2025.f1099r.ira-box4-withholding"
FACT_R_CLOSURE = "tax.us.2025.f1099r.box4.source-closure"

FACT_G_B1 = "tax.us.2025.f1099g.box1-unemployment"
FACT_G_AUTH = "tax.us.2025.f1099g.box4-federal-withholding-authority"
FACT_G_B4 = "tax.us.2025.f1099g.box4-withholding"
FACT_G_CLOSURE = "tax.us.2025.f1099g.b4.source-closure"

FACT_SSA_B5 = "tax.us.2025.ssa1099.box5-net-benefits"
FACT_SSA_B3 = "tax.us.2025.ssa1099.box3-benefits-paid"
FACT_SSA_B4 = "tax.us.2025.ssa1099.box4-repayment"
FACT_SSA_RECIPIENT = "tax.us.2025.ssa1099.recipient"
FACT_SSA_KIND = "tax.us.2025.ssa1099.statement-kind"
FACT_SSA_LUMP_SUM = "tax.us.2025.ssa1099.lump-sum-election"
FACT_SSA_AUTH = "tax.us.2025.ssa1099.box6-withholding"
FACT_SSA_B6 = "tax.us.2025.ssa1099.box6-voluntary-withholding"
FACT_SSA_CLOSURE = "tax.us.2025.ssa1099.b6.source-closure"

FACT_ROUNDING = "rounding.convention"

# Families
FAMILY_INT = "tax.us.2025.f1099int.b4"
FAMILY_DIV = "tax.us.2025.f1099div.b4"
FAMILY_R = "tax.us.2025.f1099r.box4"
FAMILY_G = "tax.us.2025.f1099g.b4"
FAMILY_SSA = "tax.us.2025.ssa1099.b6"

# Subtotals
SUBTOTAL_INT = "tax.us.2025.interest.b4-withholding-subtotal"
SUBTOTAL_DIV = "tax.us.2025.dividends.b4-withholding-subtotal"
SUBTOTAL_R = "tax.us.2025.ira.box4-withholding-subtotal"
SUBTOTAL_G = "tax.us.2025.unemployment.b4-withholding-subtotal"
SUBTOTAL_SSA = "tax.us.2025.ssa1099.b6-withholding-subtotal"

LINE25B = "tax.us.2025.payments.line25b"
LINE25B_V58 = "tax.us.2025.payments.line25b.v58"


def _fact_type(
    fid: str,
    identity_keys: list[dict[str, Any]],
    value_schema: dict[str, Any],
    title: str,
) -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": fid,
        "version": "v1",
        "title": title,
        "nature": "determinable",
        "identity_keys": identity_keys,
        "value_schema": value_schema,
        "supersession": {"policy": "free"},
    }


def _closure_fact(closure_id: str, title: str) -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": closure_id,
        "version": "v1",
        "title": title,
        "nature": "determinable",
        "identity_keys": [
            {"name": "family-horizon", "kind": "entity", "entity_kind": KIND_HORIZON},
            {"name": "tax-year", "kind": "literal", "values": [YEAR]},
        ],
        "value_schema": {"type": "boolean"},
        "supersession": {"policy": "free"},
    }


def _bundle() -> dict[str, Any]:
    fts = [
        # Companions / income facts
        _fact_type(
            FACT_INT_B1,
            [
                {"name": "payer", "kind": "entity", "entity_kind": KIND_INT_PAYER},
                {"name": "statement", "kind": "entity", "entity_kind": KIND_INT_STMT},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            {"type": "number", "minimum": 0},
            "1099-INT box 1",
        ),
        _fact_type(
            FACT_DIV_B1A,
            [
                {"name": "payer", "kind": "entity", "entity_kind": KIND_DIV_PAYER},
                {"name": "statement", "kind": "entity", "entity_kind": KIND_DIV_STMT},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            {"type": "number", "minimum": 0},
            "1099-DIV box 1a",
        ),
        _fact_type(
            FACT_R_B1,
            [
                {"name": "payer", "kind": "entity", "entity_kind": KIND_IRA_PAYER},
                {"name": "statement", "kind": "entity", "entity_kind": KIND_IRA_STMT},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            {"type": "number", "minimum": 0},
            "1099-R box 1",
        ),
        _fact_type(
            FACT_R_B2A,
            [
                {"name": "payer", "kind": "entity", "entity_kind": KIND_IRA_PAYER},
                {"name": "statement", "kind": "entity", "entity_kind": KIND_IRA_STMT},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            {"type": "number", "minimum": 0},
            "1099-R box 2a",
        ),
        _fact_type(
            FACT_R_DIST_CODE,
            [
                {"name": "payer", "kind": "entity", "entity_kind": KIND_IRA_PAYER},
                {"name": "statement", "kind": "entity", "entity_kind": KIND_IRA_STMT},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            {"type": "string"},
            "1099-R distribution code",
        ),
        _fact_type(
            FACT_R_IRA_CHECKBOX,
            [
                {"name": "payer", "kind": "entity", "entity_kind": KIND_IRA_PAYER},
                {"name": "statement", "kind": "entity", "entity_kind": KIND_IRA_STMT},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            {"type": "boolean"},
            "1099-R IRA checkbox",
        ),
        _fact_type(
            FACT_R_B2B_NOT_DET,
            [
                {"name": "payer", "kind": "entity", "entity_kind": KIND_IRA_PAYER},
                {"name": "statement", "kind": "entity", "entity_kind": KIND_IRA_STMT},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            {"type": "boolean"},
            "1099-R box 2b not determined",
        ),
        _fact_type(
            FACT_G_B1,
            [
                {"name": "payer", "kind": "entity", "entity_kind": KIND_G_PAYER},
                {"name": "statement", "kind": "entity", "entity_kind": KIND_G_STMT},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            {"type": "number", "minimum": 0},
            "1099-G box 1",
        ),
        _fact_type(
            FACT_G_AUTH,
            [
                {"name": "payer", "kind": "entity", "entity_kind": KIND_G_PAYER},
                {"name": "statement", "kind": "entity", "entity_kind": KIND_G_STMT},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            {"type": ["number", "null"]},
            "1099-G box 4 authority",
        ),
        _fact_type(
            FACT_SSA_B5,
            [
                {"name": "statement", "kind": "entity", "entity_kind": KIND_SSA_STMT},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            {"type": "number", "minimum": 0},
            "SSA-1099 box 5 net benefits",
        ),
        _fact_type(
            FACT_SSA_B3,
            [
                {"name": "statement", "kind": "entity", "entity_kind": KIND_SSA_STMT},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            {"type": "number", "minimum": 0},
            "SSA-1099 box 3 benefits paid",
        ),
        _fact_type(
            FACT_SSA_B4,
            [
                {"name": "statement", "kind": "entity", "entity_kind": KIND_SSA_STMT},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            {"type": "number", "minimum": 0},
            "SSA-1099 box 4 repayment",
        ),
        _fact_type(
            FACT_SSA_RECIPIENT,
            [
                {"name": "statement", "kind": "entity", "entity_kind": KIND_SSA_STMT},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            {"type": "string"},
            "SSA-1099 recipient",
        ),
        _fact_type(
            FACT_SSA_KIND,
            [
                {"name": "statement", "kind": "entity", "entity_kind": KIND_SSA_STMT},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            {"type": "string"},
            "SSA-1099 statement kind",
        ),
        _fact_type(
            FACT_SSA_LUMP_SUM,
            [
                {"name": "statement", "kind": "entity", "entity_kind": KIND_SSA_STMT},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            {"type": "boolean"},
            "SSA-1099 lump sum election",
        ),
        _fact_type(
            FACT_SSA_AUTH,
            [
                {"name": "statement", "kind": "entity", "entity_kind": KIND_SSA_STMT},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            {"type": ["number", "null"]},
            "SSA-1099 box 6 authority",
        ),
        # Withholding and closures
        _fact_type(
            FACT_INT_B4,
            [
                {"name": "payer", "kind": "entity", "entity_kind": KIND_INT_PAYER},
                {"name": "statement", "kind": "entity", "entity_kind": KIND_INT_STMT},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            {"type": "number", "minimum": 0},
            "1099-INT box 4",
        ),
        _closure_fact(FACT_INT_CLOSURE, "1099-INT box 4 closure"),
        _fact_type(
            FACT_DIV_B4,
            [
                {"name": "payer", "kind": "entity", "entity_kind": KIND_DIV_PAYER},
                {"name": "statement", "kind": "entity", "entity_kind": KIND_DIV_STMT},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            {"type": "number", "minimum": 0},
            "1099-DIV box 4",
        ),
        _closure_fact(FACT_DIV_CLOSURE, "1099-DIV box 4 closure"),
        _fact_type(
            FACT_R_B4,
            [
                {"name": "payer", "kind": "entity", "entity_kind": KIND_IRA_PAYER},
                {"name": "statement", "kind": "entity", "entity_kind": KIND_IRA_STMT},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            {"type": "number", "minimum": 0},
            "1099-R box 4",
        ),
        _closure_fact(FACT_R_CLOSURE, "1099-R box 4 closure"),
        _fact_type(
            FACT_G_B4,
            [
                {"name": "payer", "kind": "entity", "entity_kind": KIND_G_PAYER},
                {"name": "statement", "kind": "entity", "entity_kind": KIND_G_STMT},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            {"type": "number", "minimum": 0},
            "1099-G box 4",
        ),
        _closure_fact(FACT_G_CLOSURE, "1099-G box 4 closure"),
        _fact_type(
            FACT_SSA_B6,
            [
                {"name": "statement", "kind": "entity", "entity_kind": KIND_SSA_STMT},
                {"name": "tax-year", "kind": "literal", "values": [YEAR]},
            ],
            {"type": "number", "minimum": 0},
            "SSA-1099 box 6 voluntary withholding",
        ),
        _closure_fact(FACT_SSA_CLOSURE, "SSA-1099 box 6 closure"),
        _fact_type(
            FACT_ROUNDING,
            [{"name": "tax-year", "kind": "literal", "values": [YEAR]}],
            {"type": "string"},
            "Rounding convention",
        ),
    ]
    return {
        "schema": "bundle.v2",
        "id": "probe.withholding.vocabulary",
        "version": "v1",
        "label": "Withholding vocabulary bundle",
        "fact_types": fts,
    }


def _family(fid: str, member: str, subtotal: str, title: str) -> dict[str, Any]:
    return {
        "schema": "source-family.v1",
        "id": fid,
        "version": "v1",
        "scope": dict(SCOPE),
        "title": title,
        "member_predicate": {"fact_type": member},
        "authorizes_subtotal": subtotal,
        "closure_claim": f"Every item in {fid} is recorded as of the horizon.",
    }


def _mapping(mid: str, fid: str, member: str, closure_fact: str, subtotal: str) -> dict[str, Any]:
    return {
        "schema": "source-closure-mapping.v2",
        "id": mid,
        "version": "v1",
        "admission": {"condition": "current-literal-true"},
        "admits_symbol": subtotal,
        "closure_fact_type": {"id": closure_fact, "version": "v1"},
        "closure_horizon_key": "family-horizon",
        "family": {"id": fid, "version": "v1"},
        "member_fact_type": {"id": member, "version": "v1"},
    }


def _subtotal_rule(rule_id: str, family: str, member_fact: str, publishes: str) -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v3",
        "id": rule_id,
        "version": "v1",
        "scope": dict(SCOPE),
        "role": "computation",
        "requires": [FACT_ROUNDING],
        "pins": [{"id": FACT_ROUNDING, "origin": "assertion", "role": "input", "version": "v1"}],
        "publishes": publishes,
        "when": True,
        "value": {
            "op": "round",
            "mode": {"op": "ref", "name": FACT_ROUNDING},
            "value": {
                "op": "add",
                "args": [{"op": "collect", "name": member_fact, "source_set": family}],
            },
        },
        "blocked": {"code": "OPEN_DEPENDENCY", "missing": [FACT_ROUNDING]},
    }


def _line25b_v2_rule() -> dict[str, Any]:
    """Successor rule summing 5 withholding subtotals."""
    subtotals = [SUBTOTAL_INT, SUBTOTAL_DIV, SUBTOTAL_R, SUBTOTAL_G, SUBTOTAL_SSA]
    return {
        "schema": "rule-artifact.v3",
        "id": "tax.us.2025.rule.form1040-line25b.v2",
        "version": "v2",
        "scope": dict(SCOPE),
        "role": "computation",
        "requires": [*subtotals, FACT_ROUNDING],
        "pins": [
            {"id": s, "origin": "assertion", "role": "input", "version": "v1"}
            for s in [*subtotals, FACT_ROUNDING]
        ],
        "publishes": LINE25B,
        "when": True,
        "value": {
            "op": "round",
            "mode": {"op": "ref", "name": FACT_ROUNDING},
            "value": {"op": "add", "args": [{"op": "ref", "name": s} for s in subtotals]},
        },
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": [*subtotals, FACT_ROUNDING]},
    }


def _line25b_v58_baseline_rule() -> dict[str, Any]:
    """Baseline v58 rule summing only INT, DIV, 1099-R."""
    subtotals = [SUBTOTAL_INT, SUBTOTAL_DIV, SUBTOTAL_R]
    return {
        "schema": "rule-artifact.v3",
        "id": "tax.us.2025.rule.form1040-line25b.v1",
        "version": "v1",
        "scope": dict(SCOPE),
        "role": "computation",
        "requires": [*subtotals, FACT_ROUNDING],
        "pins": [
            {"id": s, "origin": "assertion", "role": "input", "version": "v1"}
            for s in [*subtotals, FACT_ROUNDING]
        ],
        "publishes": LINE25B_V58,
        "when": True,
        "value": {
            "op": "round",
            "mode": {"op": "ref", "name": FACT_ROUNDING},
            "value": {"op": "add", "args": [{"op": "ref", "name": s} for s in subtotals]},
        },
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": [*subtotals, FACT_ROUNDING]},
    }


def build_surface(root: Path) -> tuple[PublicationSurface, dict[str, Any], dict[str, Any]]:
    base = json.loads((REPO / "packages/content/tax/2025/package.core-calculations.v58.json").read_text("utf-8"))
    member_dir = root / "members"
    member_dir.mkdir(parents=True, exist_ok=True)

    bundle = _bundle()
    bodies: list[tuple[dict[str, Any], str]] = [
        (bundle, "fact-type-bundle"),
        (_family(FAMILY_INT, FACT_INT_B4, SUBTOTAL_INT, "1099-INT box 4 family"), "source-family"),
        (_family(FAMILY_DIV, FACT_DIV_B4, SUBTOTAL_DIV, "1099-DIV box 4 family"), "source-family"),
        (_family(FAMILY_R, FACT_R_B4, SUBTOTAL_R, "1099-R box 4 family"), "source-family"),
        (_family(FAMILY_G, FACT_G_B4, SUBTOTAL_G, "1099-G box 4 family"), "source-family"),
        (_family(FAMILY_SSA, FACT_SSA_B6, SUBTOTAL_SSA, "SSA-1099 box 6 family"), "source-family"),
        (
            _mapping(
                "tax.us.2025.closure-mapping.f1099int-b4",
                FAMILY_INT,
                FACT_INT_B4,
                FACT_INT_CLOSURE,
                SUBTOTAL_INT,
            ),
            "source-closure-mapping",
        ),
        (
            _mapping(
                "tax.us.2025.closure-mapping.f1099div-b4",
                FAMILY_DIV,
                FACT_DIV_B4,
                FACT_DIV_CLOSURE,
                SUBTOTAL_DIV,
            ),
            "source-closure-mapping",
        ),
        (
            _mapping(
                "tax.us.2025.closure-mapping.f1099r-box4",
                FAMILY_R,
                FACT_R_B4,
                FACT_R_CLOSURE,
                SUBTOTAL_R,
            ),
            "source-closure-mapping",
        ),
        (
            _mapping(
                "tax.us.2025.closure-mapping.f1099g-b4",
                FAMILY_G,
                FACT_G_B4,
                FACT_G_CLOSURE,
                SUBTOTAL_G,
            ),
            "source-closure-mapping",
        ),
        (
            _mapping(
                "tax.us.2025.closure-mapping.ssa1099-b6",
                FAMILY_SSA,
                FACT_SSA_B6,
                FACT_SSA_CLOSURE,
                SUBTOTAL_SSA,
            ),
            "source-closure-mapping",
        ),
        (
            _subtotal_rule(
                "tax.us.2025.rule.f1099int-b4-subtotal", FAMILY_INT, FACT_INT_B4, SUBTOTAL_INT
            ),
            "computation",
        ),
        (
            _subtotal_rule(
                "tax.us.2025.rule.f1099div-b4-subtotal", FAMILY_DIV, FACT_DIV_B4, SUBTOTAL_DIV
            ),
            "computation",
        ),
        (
            _subtotal_rule(
                "tax.us.2025.rule.f1099r-box4-subtotal", FAMILY_R, FACT_R_B4, SUBTOTAL_R
            ),
            "computation",
        ),
        (
            _subtotal_rule(
                "tax.us.2025.rule.f1099g-b4-subtotal", FAMILY_G, FACT_G_B4, SUBTOTAL_G
            ),
            "computation",
        ),
        (
            _subtotal_rule(
                "tax.us.2025.rule.ssa1099-b6-subtotal", FAMILY_SSA, FACT_SSA_B6, SUBTOTAL_SSA
            ),
            "computation",
        ),
        (_line25b_v2_rule(), "computation"),
        (_line25b_v58_baseline_rule(), "computation"),
    ]

    registry_citizens: list[dict[str, Any]] = []
    members: list[dict[str, Any]] = []
    for body, role in bodies:
        (member_dir / f"{body['id']}.{body['version']}.json").write_text(
            json.dumps(body, sort_keys=True), encoding="utf-8"
        )
        registry_citizens.append(
            {
                "id": body["id"],
                "version": body["version"],
                "checksum": citizen_checksum(body),
            }
        )
        members.append(
            {
                "id": body["id"],
                "version": body["version"],
                "schema": body["schema"],
                "role": role,
            }
        )

    entrypoints = [
        {"id": bundle["id"], "version": bundle["version"]},
        {"id": FAMILY_INT, "version": "v1"},
        {"id": FAMILY_DIV, "version": "v1"},
        {"id": FAMILY_R, "version": "v1"},
        {"id": FAMILY_G, "version": "v1"},
        {"id": FAMILY_SSA, "version": "v1"},
        {"id": "tax.us.2025.closure-mapping.f1099int-b4", "version": "v1"},
        {"id": "tax.us.2025.closure-mapping.f1099div-b4", "version": "v1"},
        {"id": "tax.us.2025.closure-mapping.f1099r-box4", "version": "v1"},
        {"id": "tax.us.2025.closure-mapping.f1099g-b4", "version": "v1"},
        {"id": "tax.us.2025.closure-mapping.ssa1099-b6", "version": "v1"},
        {"id": "tax.us.2025.rule.form1040-line25b.v2", "version": "v2"},
        {"id": "tax.us.2025.rule.form1040-line25b.v1", "version": "v1"},
    ]

    package: dict[str, Any] = {
        "schema": base["schema"],
        "id": "probe.package.withholding",
        "version": "v1",
        "scope": dict(SCOPE),
        "admitted_schemas": list(base["admitted_schemas"]),
        "composition_obligations": [],
        "conflict_semantics": [],
        "entrypoints": entrypoints,
        "input_bindings": [],
        "members": members,
    }
    package["package_checksum"] = package_instance_checksum(package)
    (member_dir / "package.json").write_text(
        json.dumps(package, sort_keys=True), encoding="utf-8"
    )

    registry_path = root / "registry.json"
    registry_path.write_text(
        json.dumps(
            {
                "citizens": registry_citizens,
                "packages": [
                    {
                        "id": package["id"],
                        "version": package["version"],
                        "checksum": package["package_checksum"],
                    }
                ],
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    release_dir = root / "releases"
    release_dir.mkdir(parents=True, exist_ok=True)
    release = {
        "id": "probe.release.withholding",
        "version": "v1",
        "schema": "release-registry.v1",
        "package_registry_sha256": hashlib.sha256(registry_path.read_bytes()).hexdigest(),
    }
    release_path = release_dir / "probe.release.withholding.v1.json"
    release_path.write_text(json.dumps(release, sort_keys=True), encoding="utf-8")
    release["checksum"] = hashlib.sha256(release_path.read_bytes()).hexdigest()

    return PublicationSurface(release_dir, registry_path, member_dir), package, release


def _act(index: int, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.probe.act.{index:03d}",
        "kind": kind,
        "actor": USER,
        "at": f"2026-10-27T12:{index // 60:02d}:{index % 60:02d}Z",
        "committed_against": index,
        "payload": payload,
    }


def _attested(finding_id: str, fact_id: str, value: Any) -> dict[str, Any]:
    return {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "attested",
        "evidence_ids": [],
    }


def run_case(
    surface: PublicationSurface,
    package: dict[str, Any],
    release: dict[str, Any],
    case_name: str,
    *,
    amounts: dict[str, float],
    closed_families: set[str],
) -> tuple[dict[str, str], list[dict[str, Any]]]:
    acts: list[dict[str, Any]] = []

    def add(kind: str, payload: dict[str, Any]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _bundle()})
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.rounding", f"{FACT_ROUNDING}|tax-year={YEAR}", "half_up"
            )
        },
    )

    # Establish initial horizon genesis for each family
    family_meta = {
        "int": (FAMILY_INT, FACT_INT_CLOSURE),
        "div": (FAMILY_DIV, FACT_DIV_CLOSURE),
        "r": (FAMILY_R, FACT_R_CLOSURE),
        "g": (FAMILY_G, FACT_G_CLOSURE),
        "ssa": (FAMILY_SSA, FACT_SSA_CLOSURE),
    }
    current_horizons: dict[str, str] = {}
    for k, (fid, _) in family_meta.items():
        h0 = f"demo.h.{k}.0"
        add(
            "horizon-genesis",
            {
                "family": {"id": fid, "version": "v1"},
                "scope": dict(SCOPE_KEY),
                "horizon_id": h0,
            },
        )
        current_horizons[k] = h0

    # Statements recorded as a filer would:
    # Entities introduced -> statement companions asserted -> withholding asserted via member-transition

    if "int" in amounts:
        p, s = "demo.payer.int", "demo.stmt.int"
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": p, "kind": KIND_INT_PAYER, "label": "INT Payer"}})
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": s, "kind": KIND_INT_STMT, "label": "INT Stmt"}})
        # Companion: Box 1 interest income
        fid_b1 = fact_id_for(FACT_INT_B1, (("payer", p), ("statement", s), ("tax-year", YEAR)))
        add("assertion", {"finding": _attested("demo.f.int.b1", fid_b1, 1000.0)})
        # Member transition for box 4 withholding
        fid_b4 = fact_id_for(FACT_INT_B4, (("payer", p), ("statement", s), ("tax-year", YEAR)))
        h1 = f"demo.h.int.1"
        add("member-transition", {
            "family": {"id": FAMILY_INT, "version": "v1"},
            "scope": dict(SCOPE_KEY),
            "member": {"action": "assert", "finding": _attested("demo.f.int.b4", fid_b4, amounts["int"])},
            "successor": {"id": h1, "predecessor": current_horizons["int"]},
        })
        current_horizons["int"] = h1

    if "div" in amounts:
        p, s = "demo.payer.div", "demo.stmt.div"
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": p, "kind": KIND_DIV_PAYER, "label": "DIV Payer"}})
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": s, "kind": KIND_DIV_STMT, "label": "DIV Stmt"}})
        # Companion: Box 1a ordinary dividends
        fid_b1a = fact_id_for(FACT_DIV_B1A, (("payer", p), ("statement", s), ("tax-year", YEAR)))
        add("assertion", {"finding": _attested("demo.f.div.b1a", fid_b1a, 2000.0)})
        # Member transition for box 4 withholding
        fid_b4 = fact_id_for(FACT_DIV_B4, (("payer", p), ("statement", s), ("tax-year", YEAR)))
        h1 = f"demo.h.div.1"
        add("member-transition", {
            "family": {"id": FAMILY_DIV, "version": "v1"},
            "scope": dict(SCOPE_KEY),
            "member": {"action": "assert", "finding": _attested("demo.f.div.b4", fid_b4, amounts["div"])},
            "successor": {"id": h1, "predecessor": current_horizons["div"]},
        })
        current_horizons["div"] = h1

    if "r" in amounts:
        p, s = "demo.payer.r", "demo.stmt.r"
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": p, "kind": KIND_IRA_PAYER, "label": "R Payer"}})
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": s, "kind": KIND_IRA_STMT, "label": "R Stmt"}})
        # Companions: Box 1, Box 2a, distribution code 7, IRA checkbox True, Box 2b not determined False
        fid_b1 = fact_id_for(FACT_R_B1, (("payer", p), ("statement", s), ("tax-year", YEAR)))
        fid_b2a = fact_id_for(FACT_R_B2A, (("payer", p), ("statement", s), ("tax-year", YEAR)))
        fid_code = fact_id_for(FACT_R_DIST_CODE, (("payer", p), ("statement", s), ("tax-year", YEAR)))
        fid_ira = fact_id_for(FACT_R_IRA_CHECKBOX, (("payer", p), ("statement", s), ("tax-year", YEAR)))
        fid_b2b = fact_id_for(FACT_R_B2B_NOT_DET, (("payer", p), ("statement", s), ("tax-year", YEAR)))
        add("assertion", {"finding": _attested("demo.f.r.b2a", fid_b2a, 5000.0)})
        add("assertion", {"finding": _attested("demo.f.r.code", fid_code, "7")})
        add("assertion", {"finding": _attested("demo.f.r.ira", fid_ira, True)})
        add("assertion", {"finding": _attested("demo.f.r.b2b", fid_b2b, False)})
        add("assertion", {"finding": _attested("demo.f.r.b1", fid_b1, 5000.0)})
        # Member transition for box 4 withholding
        fid_b4 = fact_id_for(FACT_R_B4, (("payer", p), ("statement", s), ("tax-year", YEAR)))
        h1 = f"demo.h.r.1"
        add("member-transition", {
            "family": {"id": FAMILY_R, "version": "v1"},
            "scope": dict(SCOPE_KEY),
            "member": {"action": "assert", "finding": _attested("demo.f.r.b4", fid_b4, amounts["r"])},
            "successor": {"id": h1, "predecessor": current_horizons["r"]},
        })
        current_horizons["r"] = h1

    if "g" in amounts:
        p, s = "demo.payer.g", "demo.stmt.g"
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": p, "kind": KIND_G_PAYER, "label": "G Payer"}})
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": s, "kind": KIND_G_STMT, "label": "G Stmt"}})
        # Companions: Box 1 unemployment compensation and zero authority companion
        fid_b1 = fact_id_for(FACT_G_B1, (("payer", p), ("statement", s), ("tax-year", YEAR)))
        fid_auth = fact_id_for(FACT_G_AUTH, (("payer", p), ("statement", s), ("tax-year", YEAR)))
        add("assertion", {"finding": _attested("demo.f.g.auth", fid_auth, 0.0)})
        add("assertion", {"finding": _attested("demo.f.g.b1", fid_b1, 6000.0)})
        # Member transition for box 4 withholding
        fid_b4 = fact_id_for(FACT_G_B4, (("payer", p), ("statement", s), ("tax-year", YEAR)))
        h1 = f"demo.h.g.1"
        add("member-transition", {
            "family": {"id": FAMILY_G, "version": "v1"},
            "scope": dict(SCOPE_KEY),
            "member": {"action": "assert", "finding": _attested("demo.f.g.b4", fid_b4, amounts["g"])},
            "successor": {"id": h1, "predecessor": current_horizons["g"]},
        })
        current_horizons["g"] = h1

    if "ssa" in amounts:
        s = "demo.stmt.ssa"
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": s, "kind": KIND_SSA_STMT, "label": "SSA Stmt"}})
        # Companions: Box 5, Box 3, Box 4, recipient, statement-kind, lump-sum-election, authority companion
        fid_b5 = fact_id_for(FACT_SSA_B5, (("statement", s), ("tax-year", YEAR)))
        fid_b3 = fact_id_for(FACT_SSA_B3, (("statement", s), ("tax-year", YEAR)))
        fid_b4_rep = fact_id_for(FACT_SSA_B4, (("statement", s), ("tax-year", YEAR)))
        fid_rec = fact_id_for(FACT_SSA_RECIPIENT, (("statement", s), ("tax-year", YEAR)))
        fid_k = fact_id_for(FACT_SSA_KIND, (("statement", s), ("tax-year", YEAR)))
        fid_lump = fact_id_for(FACT_SSA_LUMP_SUM, (("statement", s), ("tax-year", YEAR)))
        fid_auth = fact_id_for(FACT_SSA_AUTH, (("statement", s), ("tax-year", YEAR)))
        add("assertion", {"finding": _attested("demo.f.ssa.auth", fid_auth, 0.0)})
        add("assertion", {"finding": _attested("demo.f.ssa.b3", fid_b3, 12000.0)})
        add("assertion", {"finding": _attested("demo.f.ssa.b4", fid_b4_rep, 0.0)})
        add("assertion", {"finding": _attested("demo.f.ssa.rec", fid_rec, "taxpayer")})
        add("assertion", {"finding": _attested("demo.f.ssa.k", fid_k, "ssa-1099")})
        add("assertion", {"finding": _attested("demo.f.ssa.lump", fid_lump, False)})
        add("assertion", {"finding": _attested("demo.f.ssa.b5", fid_b5, 12000.0)})
        # Member transition for box 6 voluntary withholding
        fid_b6 = fact_id_for(FACT_SSA_B6, (("statement", s), ("tax-year", YEAR)))
        h1 = f"demo.h.ssa.1"
        add("member-transition", {
            "family": {"id": FAMILY_SSA, "version": "v1"},
            "scope": dict(SCOPE_KEY),
            "member": {"action": "assert", "finding": _attested("demo.f.ssa.b6", fid_b6, amounts["ssa"])},
            "successor": {"id": h1, "predecessor": current_horizons["ssa"]},
        })
        current_horizons["ssa"] = h1

    # Family Closures: closed at current horizon (h1 if member added, h0 if empty)
    for k, (fid, cl_fact) in family_meta.items():
        if fid in closed_families:
            h = current_horizons[k]
            add(
                "assertion",
                {
                    "finding": _attested(
                        f"demo.cl.{k}",
                        f"{cl_fact}|family-horizon={h},tax-year={YEAR}",
                        True,
                    )
                },
            )

    # Package adoption
    add(
        "package-adoption",
        {
            "package": {
                "id": package["id"],
                "version": package["version"],
                "checksum": package["package_checksum"],
            },
            "release": {
                "id": release["id"],
                "version": release["version"],
                "checksum": release["checksum"],
            },
            "revision": len(acts) + 1,
            "scope": {"jurisdiction": "us", "year": YEAR},
            "audit": {"note": f"run {case_name}"},
        },
    )

    with tempfile.TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=REPO,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=f"demo.run.{case_name}",
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        pubs: dict[str, str] = {}
        blocked: list[dict[str, Any]] = []
        for p in outcome.publications or ():
            pubs[str(p.finding["symbol"])] = str(p.finding["value"])
        if outcome.output_path is not None:
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
            for r in report.get("dispositions", []):
                if r.get("disposition") == "blocked":
                    blocked.append(r)
        return pubs, blocked


def main():
    print("=== Withholding Real Coordinator Probe ===")
    with tempfile.TemporaryDirectory() as tmp:
        surface, package, release = build_surface(Path(tmp))
        ALL_CLOSED = {FAMILY_INT, FAMILY_DIV, FAMILY_R, FAMILY_G, FAMILY_SSA}

        # Case 1: 1099-G withholding reaches line 25b
        print("\n--- Case 1: 1099-G withholding reaches line 25b ---")
        pubs1, blk1 = run_case(
            surface, package, release, "case1_1099g",
            amounts={"g": 250.0},
            closed_families=ALL_CLOSED,
        )
        print(f"1099-G Subtotal ({SUBTOTAL_G}): {pubs1.get(SUBTOTAL_G)}")
        print(f"Line 25b ({LINE25B}): {pubs1.get(LINE25B)}")
        print("pubs1:", pubs1)
        print("blk1:", blk1)
        assert pubs1.get(SUBTOTAL_G) == "250"
        assert pubs1.get(LINE25B) == "250"
        print("PASS: 1099-G withholding reaches line 25b.")

        # Case 2: SSA-1099 box 6 voluntary withholding reaches line 25b
        print("\n--- Case 2: SSA-1099 box 6 reaches line 25b (along with 1099-R) ---")
        pubs2, blk2 = run_case(
            surface, package, release, "case2_ssa1099",
            amounts={"ssa": 380.0, "r": 120.0},
            closed_families=ALL_CLOSED,
        )
        print(f"SSA-1099 Subtotal ({SUBTOTAL_SSA}): {pubs2.get(SUBTOTAL_SSA)}")
        print(f"1099-R Subtotal ({SUBTOTAL_R}): {pubs2.get(SUBTOTAL_R)}")
        print(f"Line 25b ({LINE25B}): {pubs2.get(LINE25B)}")
        assert pubs2.get(SUBTOTAL_SSA) == "380"
        assert pubs2.get(SUBTOTAL_R) == "120"
        assert pubs2.get(LINE25B) == "500"
        print("PASS: SSA-1099 box 6 withholding reaches line 25b.")

        # Case 3: v58-shaped answer set with no withholding gives same line 25b as v58
        print("\n--- Case 3: v58-shaped answer set with no withholding ---")
        pubs3, blk3 = run_case(
            surface, package, release, "case3_v58_comparison",
            amounts={},
            closed_families=ALL_CLOSED,
        )
        print(f"Line 25b successor ({LINE25B}): {pubs3.get(LINE25B)}")
        print(f"Line 25b v58 baseline ({LINE25B_V58}): {pubs3.get(LINE25B_V58)}")
        assert pubs3.get(LINE25B) == "0"
        assert pubs3.get(LINE25B_V58) == "0"
        print("PASS: v58 answer set without withholding matches v58 baseline (both 0).")

        # Case 4: An unclosed new family blocks with the fact named
        print("\n--- Case 4: Unclosed new family blocks with fact named ---")
        unclosed_g = ALL_CLOSED - {FAMILY_G}
        pubs4, blk4 = run_case(
            surface, package, release, "case4_unclosed",
            amounts={},
            closed_families=unclosed_g,
        )
        print(f"Line 25b published: {pubs4.get(LINE25B)}")
        blocked_subtotal = [b for b in blk4 if b.get("artifact_id") == "tax.us.2025.rule.f1099g-b4-subtotal"]
        blocked_line25b = [b for b in blk4 if b.get("artifact_id") == "tax.us.2025.rule.form1040-line25b.v2"]
        print(f"1099-G Subtotal disposition: {blocked_subtotal[0]['disposition']}, code: {blocked_subtotal[0]['code']}, missing: {blocked_subtotal[0]['missing']}")
        print(f"Line 25b disposition: {blocked_line25b[0]['disposition']}, code: {blocked_line25b[0]['code']}, missing: {blocked_line25b[0]['missing']}")
        assert len(blocked_subtotal) > 0 and blocked_subtotal[0]["code"] == "SOURCE_SET_UNCLOSED"
        assert FAMILY_G in blocked_subtotal[0]["missing"]
        assert len(blocked_line25b) > 0 and blocked_line25b[0]["code"] == "DEPENDENCY_ABSENT"
        assert SUBTOTAL_G in blocked_line25b[0]["missing"]
        print("PASS: Unclosed family blocks subtotal and Line 25b with fact/family named.")


if __name__ == "__main__":
    main()
