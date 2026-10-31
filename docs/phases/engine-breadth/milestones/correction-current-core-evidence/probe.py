"""P0 probe: which core does a correction recalculate on?

Run from the repository root:  python3 docs/phases/engine-breadth/milestones/correction-current-core-evidence/probe.py
Writes probe-output.json next to this file. Synthetic demo.* data only. Writes no repo content.

For three returns (Form 1099-G withholding, an unconfirmed 1099-G family, a Form W-2G)
it compares, on each, a fresh ``live_coordinate_run`` on core v66 against the correction
session's public entry point (``CorrectionRuntime.open`` then ``.calculate``) over a
workspace that holds the same acts, adopting (A) core v66 and (B) core v42 (the
session's own seed adoption). It also probes (C) the session's refusal for a workspace
whose adoption its surface does not contain.
"""

from __future__ import annotations

import copy
import json
import sys
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

from packages.derivation.correction_session import (  # noqa: E402
    SCOPE_USER, RUN_SCOPE, CorrectionRuntime, core_calculations_surface,
)
from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability, bootstrap_workspace  # noqa: E402
from packages.derivation.loader import DerivationSchemas  # noqa: E402
from packages.derivation.production_resolver import PublicationSurface  # noqa: E402
from packages.kernel.act_log import ActLog  # noqa: E402
from packages.tax.loader import install_domain_scoped_supersession  # noqa: E402
from tests.test_form_1099_k_income import _handover  # noqa: E402
from tests.test_refund_or_amount_owed_track1 import _finish  # noqa: E402
from tests import test_w2g_gambling as w2g  # noqa: E402
from tests import test_withholding_closure as wc  # noqa: E402

CONTENT = ROOT / "packages/content/tax/2025"
RELEASES = ROOT / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
REL = "demo.release.sli-worksheet-integration.2025."

# core -> (package file, package version, release version, registry file)
CORES = {
    "v66": ("package.core-calculations.v66.json", "v66", "v64", "published-packages.v64.json"),
    "v42": ("package.core-calculations.v42.json", "v42", "v40", "published-packages.v40.json"),
}
USER_IN_TESTS = "demo.user.filer-1"


def surface_for(core: str) -> PublicationSurface:
    return PublicationSurface(RELEASES, CONTENT / CORES[core][3], CONTENT)


def finish(acts: list[dict[str, object]], core: str, note: str) -> list[dict[str, object]]:
    pkg, ver, rel, _ = CORES[core]
    return _finish(
        copy.deepcopy(acts), package_path=CONTENT / pkg, package_version=ver,
        release_path=RELEASES / f"{REL}{rel}.json", release_version=rel, note=note)


def to_session_user(acts: list[dict[str, object]]) -> list[dict[str, object]]:
    out = json.loads(json.dumps(acts).replace(USER_IN_TESTS, SCOPE_USER))
    for i, a in enumerate(out):
        a["committed_against"] = i
    return out


def values(pubs: Any) -> dict[str, str]:
    return {str(p.finding["symbol"]): str(p.finding["value"]) for p in pubs or ()
            if isinstance(p.finding.get("value"), (int, float, str)) and not isinstance(p.finding["value"], bool)}


def fresh(acts: list[dict[str, object]], run_id: str, surface: PublicationSurface) -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        o = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"), repo_root=ROOT, authoritative_acts=acts,
            workspace_revision=len(acts), run_scope=RUN_SCOPE, scope_user=USER_IN_TESTS,
            request={"schema": "run-request.v1"}, run_id=run_id, governance_pins=[],
            surface=surface, output_name="out.json")
        blocked: list[str] = []
        if o.output_path is not None:
            rep = json.loads(o.output_path.read_text("utf-8"))
            blocked = sorted(f"{str(r.get('artifact_id')).replace('tax.us.2025.', '')}:{r.get('code')}"
                             for r in rep.get("dispositions", []) if r.get("disposition") == "blocked")
        return {"refusal": None if o.refusal is None else f"{o.refusal.reason}",
                "values": values(o.publications), "blocked": blocked}


def session(acts: list[dict[str, object]]) -> dict[str, Any]:
    """The public path: write the log, ``CorrectionRuntime.open``, ``.calculate``, read the saved result."""
    with TemporaryDirectory() as tmp:
        cap = WorkspaceCapability(Path(tmp) / "L")
        schemas = DerivationSchemas()
        reg = install_domain_scoped_supersession(schemas.registry)
        ws = bootstrap_workspace(cap, repo_root=ROOT)
        log = ActLog(ws.location, reg)
        for i, a in enumerate(acts):
            row = dict(a)
            row["committed_against"] = i
            log.append(row, expected_revision=i)
        rt = CorrectionRuntime.open(cap, repo_root=ROOT)
        calc = rt.calculate()
        out: dict[str, Any] = {"calculated": calc.get("calculated")}
        # Why: the same call calculate() makes, to read the typed refusal (probe only).
        with TemporaryDirectory() as t2:
            contents = ActLog(ws.location, reg).read()
            o = live_coordinate_run(
                WorkspaceCapability(Path(t2) / "L"), repo_root=ROOT, authoritative_acts=contents.acts,
                workspace_revision=contents.revision, run_scope=RUN_SCOPE, scope_user=SCOPE_USER,
                request={"schema": "run-request.v1"}, run_id="demo.probe.session", governance_pins=[],
                surface=core_calculations_surface(ROOT), output_name="p.json")
            out["refusal"] = None if o.refusal is None else f"{o.refusal.reason}"
            out["values"] = values(o.publications)
            blocked: list[str] = []
            if o.output_path is not None:
                rep = json.loads(o.output_path.read_text("utf-8"))
                blocked = sorted(f"{str(r.get('artifact_id')).replace('tax.us.2025.', '')}:{r.get('code')}"
                                 for r in rep.get("dispositions", []) if r.get("disposition") == "blocked")
            out["blocked"] = blocked
        return out


def diff(a: dict[str, str], b: dict[str, str]) -> dict[str, Any]:
    keys = sorted(set(a) | set(b))
    only_a = [k for k in keys if k in a and k not in b]
    only_b = [k for k in keys if k in b and k not in a]
    changed = {k: [a[k], b[k]] for k in keys if k in a and k in b and Decimal(a[k]) != Decimal(b[k])
               } if all(_num(a.get(k)) and _num(b.get(k)) for k in keys if k in a and k in b) else {}
    return {"only_in_first": only_a, "only_in_second": only_b, "changed": changed}


def _num(v: Any) -> bool:
    try:
        Decimal(str(v))
        return True
    except Exception:
        return False


def numeric_only(v: dict[str, str]) -> dict[str, str]:
    return {k: x for k, x in v.items() if _num(x)}


def _g_return(amounts: list[float], close: bool) -> list[dict[str, object]]:
    """A complete v66-era return with two Form 1099-G (box 1) and the given box 4 withholding."""
    from tests.test_form_1099_withholding import _base, _social_security_withholding, _unemployment, _unemployment_withholding
    acts = _base(wages=50000.0, w2_withheld=4500.0)
    _unemployment(acts, [6000.0, 4000.0], authority=None)
    _unemployment_withholding(acts, amounts, close=close)
    _social_security_withholding(acts, [])
    w2g._w2g(acts, [])
    return acts


CASES = {
    "1099g_withholding_closed": lambda: _g_return([600.0, 400.0], True),
    "1099g_family_unconfirmed": lambda: _g_return([600.0, 400.0], False),
    "w2g_winnings": lambda: w2g._w2g_return([(1000.0, 200.0)]),
}


def _exc_text(fn: Any) -> Any:
    try:
        return fn()
    except Exception as exc:
        return {"exception": type(exc).__name__, "message": str(exc)[:160]}


def _seed() -> list[dict[str, Any]]:
    path = ROOT / "packages/sample_data/sli_correction_t1/workspace/acts.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines()]


def _adopt(acts: list[dict[str, Any]], core: str, act_id: str, *, release_checksum: str | None = None,
           release_version: str | None = None) -> list[dict[str, Any]]:
    pkg, ver, rel, _ = CORES[core]
    out = copy.deepcopy(acts)
    ad = copy.deepcopy(next(a for a in reversed(out) if a["kind"] == "package-adoption"))
    ad["act_id"] = act_id
    ad["committed_against"] = len(out)
    ad["payload"]["revision"] = max(a["payload"]["revision"] for a in out if a["kind"] == "package-adoption") + 1
    ad["payload"]["package"] = {"id": "tax.us.2025.package.core-calculations", "version": ver,
                                "checksum": json.loads((CONTENT / pkg).read_text("utf-8"))["package_checksum"]}
    import hashlib
    ad["payload"]["release"] = {
        "id": "demo.release.sli-worksheet-integration.2025", "version": release_version or rel,
        "checksum": release_checksum or hashlib.sha256((RELEASES / f"{REL}{rel}.json").read_bytes()).hexdigest()}
    out.append(ad)
    return out


def seed_comparison() -> dict[str, Any]:
    """The session's own v42-era seed workspace: recalculated by the session (v42), and the same acts
    after the filer adopts v66, run fresh on v66."""
    base = _seed()
    with_v66 = _adopt(base, "v66", "demo.probe.adopt.v66")
    sess_v42 = session(base)
    sess_v66 = session(with_v66)
    with TemporaryDirectory() as tmp:
        o = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"), repo_root=ROOT, authoritative_acts=with_v66,
            workspace_revision=len(with_v66), run_scope=RUN_SCOPE, scope_user=SCOPE_USER,
            request={"schema": "run-request.v1"}, run_id="demo.probe.seed.v66", governance_pins=[],
            surface=surface_for("v66"), output_name="o.json")
        blocked: list[str] = []
        if o.output_path is not None:
            rep = json.loads(o.output_path.read_text("utf-8"))
            blocked = sorted(f"{str(r.get('artifact_id')).replace('tax.us.2025.', '')}:{r.get('code')}"
                             for r in rep.get("dispositions", []) if r.get("disposition") == "blocked")
        f66 = {"refusal": None if o.refusal is None else o.refusal.reason, "values": values(o.publications), "blocked": blocked}
    d = diff(numeric_only(sess_v42["values"]), numeric_only(f66["values"]))
    return {
        "session_on_seed_v42": {"calculated": sess_v42["calculated"], "refusal": sess_v42["refusal"],
                                "n_values": len(sess_v42["values"]), "n_blocked": len(sess_v42["blocked"])},
        "session_after_adopting_v66": {"calculated": sess_v66["calculated"], "refusal": sess_v66["refusal"]},
        "fresh_v66_same_acts": {"refusal": f66["refusal"], "n_values": len(f66["values"]),
                                "blocked": f66["blocked"][:12], "n_blocked": len(f66["blocked"])},
        "session_v42_vs_fresh_v66": {
            "only_in_session_v42": d["only_in_first"][:15], "n_only_in_session_v42": len(d["only_in_first"]),
            "only_in_fresh_v66": d["only_in_second"][:15], "n_only_in_fresh_v66": len(d["only_in_second"]),
            "changed_values_[session_v42, fresh_v66]": d["changed"]},
    }


def adoption_refusals() -> dict[str, Any]:
    """What the session does today for adoptions its surface does not contain (calculate returns only calculated:false)."""
    base = _seed()
    out: dict[str, Any] = {}
    out["release_not_on_surface"] = session(_adopt(base, "v42", "demo.probe.adopt.badrel", release_checksum="0" * 64))["refusal"]
    out["no_adoption_in_scope"] = session([a for a in base if a["kind"] != "package-adoption"])["refusal"]
    out["release_v64_registry_v40"] = session(_adopt(base, "v66", "demo.probe.adopt.v66b"))["refusal"]
    return out


def main() -> None:
    result: dict[str, Any] = {"surface_pins": {
        "registry": "published-packages.v40.json", "release_dir": "student_loan_worksheet_integration/publication_surface/releases"},
        "cases": {}}
    for name, build in CASES.items():
        acts = build()
        f66 = finish(acts, "v66", name)
        f66 = _handover(f66, surface=surface_for("v66"), reconfirm=True)
        fresh66 = fresh(f66, f"demo.probe.{name}.fresh66", surface_for("v66"))
        # A: workspace adopts v66; corrected through the session.
        sess_a = session(to_session_user(f66))
        # B: the same return still adopting v42 (the session seed's adoption); fresh on v42 for reference.
        f42 = _handover(finish(acts, "v42", name), surface=surface_for("v42"), reconfirm=True) \
            if False else finish(acts, "v42", name)
        try:
            fresh42 = fresh(f42, f"demo.probe.{name}.fresh42", surface_for("v42"))
        except Exception as exc:  # recorded, not hidden
            fresh42 = {"exception": type(exc).__name__}
        try:
            sess_b = session(to_session_user(f42))
        except Exception as exc:
            sess_b = {"exception": type(exc).__name__}
        case: dict[str, Any] = {
            "fresh_v66": {"refusal": fresh66["refusal"], "blocked": fresh66["blocked"], "n_values": len(fresh66["values"])},
            "session_adopting_v66": {k: sess_a.get(k) for k in ("calculated", "refusal", "blocked")} | {"n_values": len(sess_a.get("values", {}))},
            "fresh_v42": {k: v for k, v in fresh42.items() if k != "values"} | {"n_values": len(fresh42.get("values", {}))},
            "session_adopting_v42": {k: sess_b.get(k) for k in ("calculated", "refusal", "blocked", "exception")} | {"n_values": len(sess_b.get("values", {}))},
        }
        if "values" in sess_b and fresh66["values"]:
            d = diff(numeric_only(sess_b["values"]), numeric_only(fresh66["values"]))
            case["session_v42_vs_fresh_v66"] = {
                "only_in_session_v42": d["only_in_first"], "only_in_fresh_v66": d["only_in_second"],
                "changed_values_[session_v42, fresh_v66]": d["changed"]}
        result["cases"][name] = case
        print(name, json.dumps(case)[:400], flush=True)
    result["seed_workspace"] = seed_comparison()
    result["unrecognised_adoptions"] = adoption_refusals()
    out = Path(__file__).with_name("probe-output.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
