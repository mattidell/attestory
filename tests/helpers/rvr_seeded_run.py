"""Seeded run for the required-versus-read path mode.

Publishes one synthetic computation rule through the real coordinator,
``packages.derivation.live.live_coordinate_run``, on a throwaway publication
surface. The rule requires an answer, ``ANSWER``, that it reads only inside a
``choose`` branch selected by a gate, ``GATE``:

    value = choose(gate == yes, then = choose(answer == yes, 1, 0), else 0)

With the gate ``no`` the answer is bound in the run but never read, so the
published finding carries it as absent from its pins. With the gate ``yes``
the answer is read and pinned.

This module is not collected by the default suite (its name does not start
with ``test_``). It is run only by ``tests/test_required_versus_read_path.py``
through the path mode's probe, which passes these test functions explicitly.
When ``RVR_SEEDED_ROOT`` is set, the throwaway surface is written there so the
caller can index the synthetic rule; otherwise a temporary directory is used.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402
from packages.derivation.package_validation import (  # noqa: E402
    citizen_checksum,
    package_instance_checksum,
)
from packages.derivation.production_resolver import PublicationSurface  # noqa: E402
from packages.kernel.facts import fact_id_for  # noqa: E402
from tools.required_versus_read import latest_core_package  # noqa: E402

USER = "demo.user.filer-1"
YEAR = "2025"
SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"}
P = "probe.rvr."
GATE = P + "gate"
ANSWER = P + "answer"
BUNDLE = P + "vocabulary"
RULE_ID = "probe.rule.rvr-branch"
RULE_VERSION = "v1"
SYMBOL = P + "branch-result"


def _fact_type(fact_id: str) -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": fact_id,
        "version": "v1",
        "title": f"Synthetic answer {fact_id}",
        "nature": "determinable",
        "identity_keys": [{"name": "tax-year", "kind": "literal", "values": [YEAR]}],
        "value_schema": {"type": "string", "enum": ["yes", "no"]},
        "supersession": {"policy": "free"},
    }


def _bundle() -> dict[str, Any]:
    return {
        "schema": "bundle.v2",
        "id": BUNDLE,
        "version": "v1",
        "label": "Synthetic required-versus-read vocabulary",
        "fact_types": [_fact_type(GATE), _fact_type(ANSWER)],
    }


def _yes(fact_id: str) -> dict[str, Any]:
    return {
        "op": "categorical_compare",
        "cmp": "eq",
        "left": {"op": "ref", "name": fact_id},
        "right": {"op": "category_literal", "fact_type": {"id": fact_id, "version": "v1"}, "value": "yes"},
    }


def _rule() -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v14",
        "id": RULE_ID,
        "version": RULE_VERSION,
        "scope": dict(SCOPE),
        "role": "computation",
        "requires": [GATE, ANSWER],
        "pins": [],
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "when": True,
        "value": {
            "op": "choose",
            "when": _yes(GATE),
            "then": {"op": "choose", "when": _yes(ANSWER), "then": 1, "else": 0},
            "else": 0,
        },
        "publishes": SYMBOL,
    }


def _surface(root: Path) -> tuple[PublicationSurface, dict[str, Any], dict[str, Any]]:
    _path, base = latest_core_package()
    member_dir = root / "members"
    member_dir.mkdir(parents=True)
    bodies = [(_bundle(), "fact-type-bundle"), (_rule(), "computation")]
    registry_citizens = []
    members = []
    for body, role in bodies:
        (member_dir / f"{body['id']}.{body['version']}.json").write_text(
            json.dumps(body, sort_keys=True), encoding="utf-8")
        registry_citizens.append({
            "id": body["id"], "version": body["version"], "checksum": citizen_checksum(body)})
        members.append({
            "id": body["id"], "version": body["version"], "schema": body["schema"], "role": role})
    package: dict[str, Any] = {
        "schema": base["schema"],
        "id": "probe.package.rvr-branch",
        "version": "v1",
        "scope": dict(base["scope"]),
        "admitted_schemas": list(base["admitted_schemas"]),
        "composition_obligations": [],
        "conflict_semantics": [],
        "entrypoints": [
            {"id": BUNDLE, "version": "v1"},
            {"id": RULE_ID, "version": RULE_VERSION},
        ],
        "input_bindings": [],
        "members": members,
    }
    package["package_checksum"] = package_instance_checksum(package)
    (member_dir / "package.json").write_text(json.dumps(package, sort_keys=True), encoding="utf-8")
    registry = {
        "citizens": registry_citizens,
        "packages": [{"id": package["id"], "version": package["version"],
                      "checksum": package["package_checksum"]}],
    }
    registry_path = root / "registry.json"
    registry_path.write_text(json.dumps(registry, sort_keys=True), encoding="utf-8")
    release = {
        "id": "probe.release.rvr-branch",
        "version": "v1",
        "schema": "release-registry.v1",
        "package_registry_sha256": hashlib.sha256(registry_path.read_bytes()).hexdigest(),
    }
    release_dir = root / "releases"
    release_dir.mkdir()
    release_path = release_dir / "probe.release.rvr-branch.v1.json"
    release_path.write_text(json.dumps(release, sort_keys=True), encoding="utf-8")
    release["checksum"] = hashlib.sha256(release_path.read_bytes()).hexdigest()
    return PublicationSurface(release_dir, registry_path, member_dir), package, release


def _act(index: int, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.rvr.act.{index:03d}",
        "kind": kind,
        "actor": USER,
        "at": f"2026-10-24T00:00:{index:02d}Z",
        "committed_against": index,
        "payload": payload,
    }


def _finding(finding_id: str, fact_type: str, value: str) -> dict[str, Any]:
    return {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": fact_id_for(fact_type, (("tax-year", YEAR),)),
        "value": value,
        "basis": "attested",
        "evidence_ids": [],
    }


def _acts(package: dict[str, Any], release: dict[str, Any], gate: str, answer: str) -> list[dict[str, Any]]:
    acts: list[dict[str, Any]] = [_act(0, "bundle-adoption", {"bundle": _bundle()})]
    for fact_type, value, finding_id in ((GATE, gate, "demo.rvr.gate"), (ANSWER, answer, "demo.rvr.answer")):
        acts.append(_act(len(acts), "assertion", {"finding": _finding(finding_id, fact_type, value)}))
    acts.append(_act(len(acts), "package-adoption", {
        "package": {"id": package["id"], "version": package["version"],
                    "checksum": package["package_checksum"]},
        "release": {"id": release["id"], "version": release["version"], "checksum": release["checksum"]},
        "revision": len(acts) + 1,
        "scope": {"jurisdiction": "us", "year": YEAR},
        "audit": {"note": "synthetic required-versus-read seeded run; non-authoritative"},
    }))
    return acts


def _run(gate: str, answer: str, label: str) -> str:
    """Publish the seeded rule through the coordinator; return its published value."""
    root_env = os.environ.get("RVR_SEEDED_ROOT")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(root_env) / label if root_env else Path(tmp) / "surface"
        root.mkdir(parents=True, exist_ok=True)
        surface, package, release = _surface(root)
        acts = _acts(package, release, gate, answer)
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=REPO,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=f"demo-rvr-{label}",
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        assert outcome.refusal is None, outcome.refusal
        published = {str(p.finding["symbol"]): str(p.finding["value"]) for p in outcome.publications or ()}
        assert SYMBOL in published, published
        return published[SYMBOL]


def test_gate_closed_answer_is_bound_but_never_read() -> None:
    assert _run(gate="no", answer="yes", label="gate-closed") == "0"


def test_gate_open_answer_is_read() -> None:
    assert _run(gate="yes", answer="yes", label="gate-open") == "1"
