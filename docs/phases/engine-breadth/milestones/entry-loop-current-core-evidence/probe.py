"""Trace: what the entry loop does for a workspace whose seed adopts which core.

Run from the repo root: ``python3 docs/phases/.../probe.py``. Synthetic data only.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))

from packages.derivation import entry_loop as el  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402
from packages.derivation.production_resolver import resolve_adopted_surface  # noqa: E402

CONTENT = ROOT / "packages/content/tax/2025"
FRRS = ROOT / "packages/sample_data/frrs_t3/publication_surface/releases"
SLI = ROOT / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def adoption(acts, pkg_file, pkg_ver, rel_dir, rel_file, rel_id, rel_ver, act_id):
    a = copy.deepcopy(next(x for x in reversed(acts) if x["kind"] == "package-adoption"))
    a["act_id"] = act_id
    a["committed_against"] = len(acts)
    a["payload"]["revision"] += 1
    a["payload"]["package"] = {
        "id": "tax.us.2025.package.core-calculations", "version": pkg_ver,
        "checksum": json.loads((CONTENT / pkg_file).read_text("utf-8"))["package_checksum"]}
    a["payload"]["release"] = {"id": rel_id, "version": rel_ver, "checksum": sha(rel_dir / rel_file)}
    return a


def run(label, acts):
    with TemporaryDirectory() as tmp:
        try:
            rt = el.SyntheticW2EntryRuntime(WorkspaceCapability(Path(tmp) / "L"), repo_root=ROOT, seed_acts=acts)
            snap = rt.snapshot().payload
            print(f"{label}: OK computed={snap['computed']} lines={[(l.get('line', l.get('lineId')), l['computed']) for l in snap['lines']]}")
        except Exception as exc:  # noqa: BLE001
            print(f"{label}: {type(exc).__name__}: {exc}")


seed = el.load_seed_acts(ROOT)
print("seed adoption release:", [a["payload"]["release"]["id"] + "@" + a["payload"]["release"]["version"]
                                 for a in seed if a["kind"] == "package-adoption"])
s = resolve_adopted_surface(seed, run_scope=el.RUN_SCOPE, scope_user=el.SCOPE_USER,
                            workspace_revision=len(seed), release_dir=FRRS, member_dir=CONTENT)
print("resolver on seed (frrs_t3 releases):", getattr(s, "package_registry_path", s))
print("fixed surface registry:", "published-packages.json")
run("seed as shipped", seed)

# Later adoption on the frrs_t3 surface (release v2, v3).
for ver in ("v2", "v3"):
    rel = FRRS / f"demo.release.2025.{ver}.json"
    pkg = json.loads(rel.read_text("utf-8"))
    print(ver, "release keys:", sorted(k for k in pkg if "package" in k or "registry" in k))

# Current core: package v66 / release v64 / registry v64 (SLI integration surface).
v66 = [*seed, adoption(seed, "package.core-calculations.v66.json", "v66", SLI,
                       "demo.release.sli-worksheet-integration.2025.v64.json",
                       "demo.release.sli-worksheet-integration.2025", "v64", "demo.trace.adopt.v66")]
run("seed + v66 adoption (fixed surface)", v66)
for label, rel_dir in (("frrs_t3 only", FRRS), ("sli releases", SLI)):
    r = resolve_adopted_surface(v66, run_scope=el.RUN_SCOPE, scope_user=el.SCOPE_USER,
                                workspace_revision=len(v66), release_dir=rel_dir, member_dir=CONTENT)
    print(f"resolver on v66 adoption, {label}:", getattr(r, "package_registry_path", r))


# What a run on the v66 core says for the same acts, offered the surface the adoption names.
from packages.derivation.live import live_coordinate_run  # noqa: E402

surface = resolve_adopted_surface(v66, run_scope=el.RUN_SCOPE, scope_user=el.SCOPE_USER,
                                  workspace_revision=len(v66), release_dir=SLI, member_dir=CONTENT)
with TemporaryDirectory() as tmp:
    out = live_coordinate_run(
        WorkspaceCapability(Path(tmp) / "L"), repo_root=ROOT, authoritative_acts=v66,
        workspace_revision=len(v66), run_scope=el.RUN_SCOPE, scope_user=el.SCOPE_USER,
        request={"schema": "run-request.v1"}, run_id="demo.trace.run", governance_pins=[],
        surface=surface, output_name="o.json")
    print("fresh run on v66 refusal:", out.refusal)
    if out.output_path:
        rep = json.loads(out.output_path.read_text("utf-8"))
        print("blocked rows:", sum(1 for r in rep.get("dispositions", []) if r.get("disposition") == "blocked"))
        from collections import Counter
        print("blocked codes:", Counter(r.get("code") for r in rep.get("dispositions", []) if r.get("disposition") == "blocked").most_common(5))
        model = json.loads(out.presentation_path.read_text("utf-8"))
        shown = {str(x.get("field", {}).get("line")): x.get("resolved", {}).get("disposition")
                 for x in model["sections"] if isinstance(x, dict) and isinstance(x.get("field"), dict)
                 and str(x["field"].get("line")) in el.EVALUATION_LINES}
        print("v66 lines starting 11/12:", sorted({str(x["field"].get("line")) for x in model["sections"]
              if isinstance(x, dict) and isinstance(x.get("field"), dict) and str(x["field"].get("line")).startswith(("11", "12"))}))
        print("evaluation lines present in the v66 model:", shown)
        try:
            print("lines:", {k: v["computed"] for k, v in el._line_values(model).items()})
        except el.EntryLoopError as exc:
            print("line view:", exc)
