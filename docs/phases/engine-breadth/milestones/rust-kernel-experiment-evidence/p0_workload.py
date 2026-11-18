"""P0 workload: one recorded list, run as the plain-line-texts census runs it.

Shared by p0_timing.py and p0_profile.py. Mirrors census.per_list on a
published core (finish, SSA handover with reconfirm, live_coordinate_run,
page render) with stage timings and sizes. No production code is changed;
nothing is written inside the repository.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import tempfile
import time
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools import recorded_replay as rr  # noqa: E402

CORE = "v96"


def sizes(finished: list[dict[str, Any]]) -> dict[str, int]:
    kinds: dict[str, int] = {}
    facts = set()
    for act in finished:
        kinds[act["kind"]] = kinds.get(act["kind"], 0) + 1
        if act["kind"] == "assertion":
            fid = ((act.get("payload") or {}).get("finding") or {}).get("fact_id")
            if fid:
                facts.add(fid)
    return {"acts": len(finished), "assertions": kinds.get("assertion", 0),
            "distinct_asserted_facts": len(facts), "bundle_adoptions": kinds.get("bundle-adoption", 0)}


def prepare(key: str, acts: list[dict[str, Any]], core: Any) -> list[dict[str, Any]]:
    h = rr._get_harness()
    slug = hashlib.sha256(key.encode()).hexdigest()[:20]
    finished = h._finish(acts, package_path=core.package_path, package_version=core.version,
                         release_path=core.release_path, release_version=core.release_version,
                         note="demo.rke." + slug)
    return h._handover(finished, surface=core.surface(), reconfirm=True)  # type: ignore[no-any-return]


def run(key: str, finished: list[dict[str, Any]], core: Any) -> dict[str, Any]:
    """live_coordinate_run plus page render; returns timings and a small pin."""
    from packages.derivation.live_session import _render_page
    h = rr._get_harness()
    slug = hashlib.sha256(key.encode()).hexdigest()[:20]
    with tempfile.TemporaryDirectory() as tmp:
        capability = h.WorkspaceCapability(Path(tmp) / "L")
        t0 = time.perf_counter()
        outcome = h.live_coordinate_run(capability, repo_root=REPO,
            authoritative_acts=finished, workspace_revision=len(finished),
            run_scope={"jurisdiction": "us", "year": h.YEAR}, scope_user=h.ccr.USER,
            request={"schema": "run-request.v1"}, run_id="demo.rke." + slug,
            governance_pins=[], surface=core.surface(), output_name="out.json")
        t1 = time.perf_counter()
        if outcome.refusal:
            return {"outcome": "refused", "run_s": t1 - t0, "render_s": 0.0}
        page = _render_page(REPO, capability, outcome.presentation_path)
        t2 = time.perf_counter()
        report = json.loads(outcome.output_path.read_text())
        rows = report["dispositions"]
        return {"outcome": "success", "run_s": t1 - t0, "render_s": t2 - t1,
                "rows": len(rows), "publications": len(outcome.publications or ()),
                "page_bytes": len(page),
                "pin_sha256": hashlib.sha256(json.dumps(
                    {"rows": rows, "values": sorted(json.dumps(p.finding, sort_keys=True)
                                                    for p in outcome.publications or ())},
                    sort_keys=True).encode()).hexdigest()}


def per_list(key: str, acts: list[dict[str, Any]], core: Any) -> dict[str, Any]:
    h = rr._get_harness()
    try:
        with h.loader_entries(core):
            t0 = time.perf_counter()
            finished = prepare(key, acts, core)
            prep = time.perf_counter() - t0
            out = run(key, finished, core)
    except Exception as exc:  # recorded lists that error on the core are timed too
        return {"outcome": "error", "error": type(exc).__name__,
                "total_s": round(time.perf_counter() - t0, 4)}
    out["prep_s"] = prep
    out.update(sizes(finished))
    out["total_s"] = prep + out["run_s"] + out["render_s"]
    for k in ("prep_s", "run_s", "render_s", "total_s"):
        out[k] = round(out[k], 4)
    return out


def write(path: Path, body: Any) -> None:
    text = json.dumps(body, indent=1, sort_keys=True) + "\n"
    rr._check_no_local_paths(text, path.name)
    path.write_text(text, encoding="utf-8")
