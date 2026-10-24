"""Smallest failing case probe: cross-subject binding on the live path.

Reduced from child_dispatch_probe.py (flat-alone).
One per-child rule requiring one per-child answer (child residency).
Two children:
  child-1 has relationship=yes, residency=yes.
  child-2 has relationship=yes, residency UNANSWERED.

Outcome:
  child-2 evaluates with child-1's residency answer and publishes 1,
  recording child-1's residency finding in its pins.
"""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.package_validation import citizen_checksum, package_instance_checksum
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.facts import fact_id_for

USER = "demo.user.filer-1"
YEAR = "2025"
CHILD_KIND = "probe.child"
P = "probe.eic."
SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"}

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


def _fact_type(fact_id: str) -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": fact_id,
        "version": "v1",
        "title": f"Synthetic per-child answer {fact_id}",
        "nature": "determinable",
        "identity_keys": [
            {"name": "child", "kind": "entity", "entity_kind": CHILD_KIND},
            {"name": "tax-year", "kind": "literal", "values": [YEAR]},
        ],
        "value_schema": {"type": "string", "enum": ["yes", "no"]},
        "supersession": {"policy": "free"},
    }


def _bundle() -> dict[str, Any]:
    closure = {
        "schema": "fact-type.v2",
        "id": CLOSURE,
        "version": "v1",
        "title": "Closure of the synthetic child roster",
        "nature": "determinable",
        "identity_keys": [
            {"name": "family-horizon", "kind": "entity", "entity_kind": "kernel.family-horizon"},
            {"name": "tax-year", "kind": "literal", "values": [YEAR]},
        ],
        "value_schema": {"type": "boolean"},
        "supersession": {"policy": "free"},
    }
    inert = {
        "schema": "fact-type.v2",
        "id": INERT,
        "version": "v1",
        "title": "Internal marker used only to complete an inert rule path",
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
        "fact_types": [_fact_type(REL), _fact_type(RES), closure, inert],
    }


def _family() -> dict[str, Any]:
    return {
        "schema": "source-family.v1",
        "id": FAMILY,
        "version": "v1",
        "scope": dict(SCOPE),
        "title": "Synthetic child roster",
        "member_predicate": {"fact_type": REL},
        "authorizes_subtotal": P + "child-count",
        "closure_claim": "Every qualifying-child candidate is recorded as a roster item.",
    }


def _closure_mapping() -> dict[str, Any]:
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


def _rule(rule_id: str, schema: str = "rule-artifact.v14", **fields: Any) -> dict[str, Any]:
    body: dict[str, Any] = {
        "schema": schema,
        "id": rule_id,
        "version": "v1",
        "scope": dict(SCOPE),
        "role": "computation",
        "requires": [],
        "pins": [],
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
    }
    body.update(fields)
    return body


def _count_rule() -> dict[str, Any]:
    read = P + "child.counts-flat"
    return _rule(
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
                "missing": ["probe-eic-child-roster-inert-path-conflict"],
                "pins": [],
            },
        },
        publishes=P + "child.count-flat",
    )


def _rules() -> list[dict[str, Any]]:
    # The flat rule: requires ONLY residency (RES)
    flat_rule = _rule(
        f"{RULE_PREFIX}child-counts-flat",
        subject=_pin(REL),
        requires=[RES],
        when=True,
        value={
            "op": "choose",
            "when": {
                "op": "all",
                "args": [
                    {
                        "op": "categorical_compare",
                        "cmp": "eq",
                        "left": {"op": "ref", "name": REL},
                        "right": {"op": "category_literal", "fact_type": _pin(REL), "value": "yes"},
                    },
                    {
                        "op": "categorical_compare",
                        "cmp": "eq",
                        "left": {"op": "ref", "name": RES},
                        "right": {"op": "category_literal", "fact_type": _pin(RES), "value": "yes"},
                    },
                ],
            },
            "then": 1,
            "else": 0,
        },
        publishes=P + "child.counts-flat",
    )
    return [flat_rule, _count_rule()]


def build_surface(root: Path) -> tuple[PublicationSurface, dict[str, Any], dict[str, Any]]:
    base = json.loads((REPO / "packages/content/tax/2025/package.core-calculations.v53.json").read_text("utf-8"))
    member_dir = root / "members"
    member_dir.mkdir()
    citizens = [
        (_bundle(), "fact-type-bundle"),
        (_family(), "source-family"),
        (_closure_mapping(), "source-closure-mapping"),
    ]
    citizens.extend((r, "computation") for r in _rules())
    registry_citizens = []
    members = []
    for body, role in citizens:
        (member_dir / f"{body['id']}.{body['version']}.json").write_text(
            json.dumps(body, sort_keys=True), encoding="utf-8"
        )
        registry_citizens.append({
            "id": body["id"], "version": body["version"], "checksum": citizen_checksum(body)
        })
        members.append({
            "id": body["id"], "version": body["version"], "schema": body["schema"], "role": role
        })

    package = {
        "schema": base["schema"],
        "id": "probe.package.eic-children",
        "version": "v1",
        "scope": dict(base["scope"]),
        "admitted_schemas": list(base["admitted_schemas"]),
        "composition_obligations": [],
        "conflict_semantics": [],
        "entrypoints": [
            {"id": m["id"], "version": m["version"]}
            for m in members
            if m["role"] in ("source-family", "source-closure-mapping", "fact-type-bundle")
            or "qualifying-child-count" in m["id"]
        ],
        "input_bindings": [],
        "members": members,
    }
    package["package_checksum"] = package_instance_checksum(package)
    (member_dir / "package.json").write_text(json.dumps(package, sort_keys=True), encoding="utf-8")
    registry = {
        "citizens": registry_citizens,
        "packages": [{"id": package["id"], "version": package["version"], "checksum": package["package_checksum"]}],
    }
    registry_path = root / "registry.json"
    registry_path.write_text(json.dumps(registry, sort_keys=True), encoding="utf-8")
    release = {
        "id": "probe.release.eic-children",
        "version": "v1",
        "schema": "release-registry.v1",
        "package_registry_sha256": hashlib.sha256(registry_path.read_bytes()).hexdigest(),
    }
    release_dir = root / "releases"
    release_dir.mkdir()
    release_path = release_dir / "probe.release.eic-children.v1.json"
    release_path.write_text(json.dumps(release, sort_keys=True), encoding="utf-8")
    release["checksum"] = hashlib.sha256(release_path.read_bytes()).hexdigest()
    return PublicationSurface(release_dir, registry_path, member_dir), package, release


def build_acts(package: dict[str, Any], release: dict[str, Any]) -> list[dict[str, Any]]:
    acts: list[dict[str, Any]] = []

    def add(kind: str, payload: dict[str, Any]) -> None:
        acts.append({
            "schema": "act.v1",
            "act_id": f"demo.probe.act.{len(acts):03d}",
            "kind": kind,
            "actor": USER,
            "at": f"2026-10-24T00:{len(acts) // 60:02d}:{len(acts) % 60:02d}Z",
            "committed_against": len(acts),
            "payload": payload,
        })

    add("bundle-adoption", {"bundle": _bundle()})
    for child in ("demo-child-1", "demo-child-2"):
        add("entity-introduced", {
            "entity": {"schema": "entity.v1", "id": child, "kind": CHILD_KIND, "label": "Synthetic child"}
        })

    scope_key = {"tax-year": YEAR, "subject": "demo.primary"}
    add("horizon-genesis", {"family": _pin(FAMILY), "scope": scope_key, "horizon_id": "demo.probe.h0"})
    horizon = "demo.probe.h0"
    for index, child in enumerate(("demo-child-1", "demo-child-2")):
        successor = f"demo.probe.h{index + 1}"
        add("member-transition", {
            "family": _pin(FAMILY),
            "scope": scope_key,
            "member": {
                "action": "assert",
                "finding": {
                    "schema": "finding.v2",
                    "id": f"demo.probe.rel.{child}",
                    "fact_id": fact_id_for(REL, (("child", child), ("tax-year", YEAR))),
                    "value": "yes",
                    "basis": "attested",
                    "evidence_ids": [],
                },
            },
            "successor": {"id": successor, "predecessor": horizon},
        })
        horizon = successor

    # ONLY demo-child-1 asserts residency!
    add("assertion", {
        "finding": {
            "schema": "finding.v2",
            "id": "demo.probe.residency.demo-child-1",
            "fact_id": fact_id_for(RES, (("child", "demo-child-1"), ("tax-year", YEAR))),
            "value": "yes",
            "basis": "attested",
            "evidence_ids": [],
        }
    })
    add("assertion", {
        "finding": {
            "schema": "finding.v2",
            "id": "demo.probe.closure",
            "fact_id": f"{CLOSURE}|family-horizon={horizon},tax-year={YEAR}",
            "value": True,
            "basis": "attested",
            "evidence_ids": [],
        }
    })
    add("package-adoption", {
        "package": {"id": package["id"], "version": package["version"], "checksum": package["package_checksum"]},
        "release": {"id": release["id"], "version": release["version"], "checksum": release["checksum"]},
        "revision": len(acts) + 1,
        "scope": {"jurisdiction": "us", "year": YEAR},
        "audit": {"note": "synthetic probe adoption; non-authoritative"},
    })
    return acts


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        surface, package, release = build_surface(Path(tmp))
        acts = build_acts(package, release)
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=REPO,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id="demo-probe-smallest-failing-case",
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            print(f"REFUSAL: {outcome.refusal.reason}: {outcome.refusal.detail}")
            return 1

        print("Publications:")
        for pub in outcome.publications or []:
            f = pub.finding
            sym = f["symbol"]
            val = f["value"]
            if "counts-flat" in sym or "count-flat" in sym:
                print(f"  {sym} = {val}")
                for p in f["pins"]:
                    print(f"    pin: {p.get('role')} id={p.get('id')}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
