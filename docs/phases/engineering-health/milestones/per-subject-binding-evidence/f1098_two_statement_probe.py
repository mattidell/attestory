"""Form 1098 two-statement cross-subject binding probe on production v54.

Demonstrates that a per-subject rule (tax.us.2025.rule.f1098-residence-interest-reason@v2)
evaluates for a second statement (demo.f1098.lender.b, demo.f1098.stmt.b) with NO
circumstance answers asserted for statement B, by silently binding the circumstance
answers asserted for statement A (demo.f1098.lender.a, demo.f1098.stmt.a) via the
run-wide fallback input mechanism in marshal.py and subject_dispatch.py.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from packages.tax.loader import TAX_CONTENT_DIR
from tests.test_f1098_v43_debt_limit_fix import RELEASE_DIR, _read_json
from tests.test_f1098_statement_review import _base_acts
from tests.test_f1098_circumstances_calculation import SCOPE, USER
from tests.test_f1098_mortgage_interest_line12e_track2 import _attested, _member_fact_id

CONTENT = TAX_CONTENT_DIR
PACKAGE_PATH = CONTENT / "package.core-calculations.v54.json"
REGISTRY_PATH = CONTENT / "published-packages.v52.json"
RELEASE_PATH = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v52.json"

V2_ANSWERS = {
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


def build_two_statement_acts() -> list[dict[str, Any]]:
    """Build acts for two 1098 statements where only Statement A has circumstance answers."""
    acts = _base_acts(second_interest=10000)
    pkg = _read_json(PACKAGE_PATH)
    release = _read_json(RELEASE_PATH)

    # Strip existing package adoption
    acts = [a for a in acts if a.get("kind") != "package-adoption"]

    # Adopt f1098-circumstances bundle v2
    acts.append({
        "schema": "act.v1",
        "act_id": "demo.f1098.t2.circumstances.bundle.v2",
        "kind": "bundle-adoption",
        "actor": USER,
        "at": "2026-10-14T20:30:00Z",
        "committed_against": len(acts),
        "payload": {"bundle": _read_json(CONTENT / "f1098-circumstances.bundle.v2.json")},
    })

    # Assert circumstances ONLY for Statement A
    for i, (suffix, val) in enumerate(V2_ANSWERS.items()):
        fact_id = _member_fact_id(f"tax.us.2025.f1098.{suffix}", "demo.f1098.lender.a", "demo.f1098.stmt.a")
        finding = _attested(f"demo.f1098.ans.a.{i}", fact_id, val)
        acts.append({
            "schema": "act.v1",
            "act_id": f"demo.f1098.ans.act.{i}",
            "kind": "assertion",
            "actor": USER,
            "at": "2026-10-14T20:30:01Z",
            "committed_against": len(acts),
            "payload": {"finding": finding},
        })

    # Append package adoption for v54
    acts.append({
        "schema": "act.v1",
        "act_id": "demo.f1098.adopt.v54",
        "kind": "package-adoption",
        "actor": USER,
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
            "scope": SCOPE,
            "audit": {"note": "two-statement cross-subject probe"},
        },
    })

    for idx, a in enumerate(acts):
        a["committed_against"] = idx

    return acts


def run_probe() -> dict[str, Any]:
    acts = build_two_statement_acts()
    with TemporaryDirectory() as tmp:
        cap = WorkspaceCapability(Path(tmp))
        outcome = live_coordinate_run(
            cap,
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope=SCOPE,
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id="demo.f1098.probe.v54",
            governance_pins=[],
            surface=PublicationSurface(RELEASE_DIR, REGISTRY_PATH, CONTENT),
            output_name="probe.json",
        )
        if outcome.refusal is not None:
            raise RuntimeError(f"Run refused: {outcome.refusal}")
        assert outcome.output_path is not None
        report = json.loads(Path(outcome.output_path).read_text("utf-8"))

    pubs = {}
    for p in outcome.publications or ():
        sym = p.finding.get("symbol")
        if sym:
            pubs[sym] = p.finding.get("value")

    dispositions = [
        d for d in report.get("dispositions", [])
        if d.get("artifact_id") == "tax.us.2025.rule.f1098-residence-interest-reason"
    ]

    return {
        "publications": pubs,
        "dispositions": dispositions,
    }


if __name__ == "__main__":
    result = run_probe()
    print("Found", len(result["dispositions"]), "dispositions for rule.f1098-residence-interest-reason:")
    for d in result["dispositions"]:
        sym = d["symbol"]
        pinned_input_ids = [p["id"] for p in d.get("pins", []) if p.get("role") == "input"]
        stmt_a_pins = [pid for pid in pinned_input_ids if "ans.a" in pid]
        print(f"  Symbol: {sym}")
        print(f"    Disposition: {d['disposition']}")
        print(f"    Total input pins: {len(pinned_input_ids)}")
        print(f"    Statement A answer pins: {stmt_a_pins}")
