"""Track 1 identity dump: replay every recorded list on core v96 and hash the outcome.

Run:  python3 track1_dump.py <label> <scratch-outside-repo> [--limit N]

Per list it records SHA-256 of the canonical result (report, published values,
refusal), SHA-256 of the saved page bytes, and for an erroring list the
exception class and message (with the temporary directory name masked).
It also records package validation's full ordered error list for the published
v96 package and for several invalid mutations.

The full dump (``dump-<label>.json``) is written to the scratch directory,
outside the repository. ``summary-<label>.json`` beside this file carries only
counts and digests. Compare two labels with ``track1_compare.py``.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import time
from typing import Any

HERE = Path(__file__).resolve().parent


def load(name: str, path: Path):  # type: ignore[no-untyped-def]
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
        sys.modules[name] = module
        spec.loader.exec_module(module)  # type: ignore[union-attr]
    return sys.modules[name]


wl = load("rke_t1_workload", HERE / "p0_workload.py")
rr = wl.rr
REPO = wl.REPO


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=repr).encode("utf-8")


def per_list(key: str, acts: list[dict[str, Any]], core: Any) -> dict[str, Any]:
    """Replay one list and return hashes (no timings, so reruns are comparable)."""
    from packages.derivation.live_session import _render_page
    h = rr._get_harness()
    slug = hashlib.sha256(key.encode()).hexdigest()[:20]
    tmp_name = ""
    try:
        with h.loader_entries(core):
            finished = wl.prepare(key, acts, core)
            with tempfile.TemporaryDirectory() as tmp:
                tmp_name = tmp
                capability = h.WorkspaceCapability(Path(tmp) / "L")
                outcome = h.live_coordinate_run(
                    capability, repo_root=REPO, authoritative_acts=finished,
                    workspace_revision=len(finished),
                    run_scope={"jurisdiction": "us", "year": h.YEAR}, scope_user=h.ccr.USER,
                    request={"schema": "run-request.v1"}, run_id="demo.rke." + slug,
                    governance_pins=[], surface=core.surface(), output_name="out.json")
                if outcome.refusal:
                    refusal = outcome.refusal
                    body = {"refusal": repr(refusal).replace(tmp, "<TMP>")}
                    return {"outcome": "refused", "result_sha": _sha(_canon(body)), "page_sha": None,
                            "detail": body["refusal"][:400]}
                page = _render_page(REPO, capability, outcome.presentation_path)
                report = json.loads(outcome.output_path.read_text())
                values = sorted(json.dumps(p.finding, sort_keys=True) for p in outcome.publications or ())
                presentation = Path(outcome.presentation_path).read_bytes() if outcome.presentation_path else b""
                body = {"report": report, "values": values}
                text = _canon(body).decode("utf-8").replace(tmp, "<TMP>")
                page_bytes = page if isinstance(page, bytes) else str(page).encode("utf-8")
                return {"outcome": "success", "result_sha": _sha(text.encode("utf-8")),
                        "page_sha": _sha(page_bytes.replace(tmp.encode(), b"<TMP>")),
                        "presentation_sha": _sha(presentation.replace(tmp.encode(), b"<TMP>")),
                        "rows": len(report["dispositions"])}
    except Exception as exc:  # recorded lists that error on the core are compared too
        message = str(exc)
        if tmp_name:
            message = message.replace(tmp_name, "<TMP>")
        return {"outcome": "error", "error": type(exc).__name__, "message": message,
                "result_sha": _sha(_canon([type(exc).__name__, message]))}


def validation_errors() -> dict[str, Any]:
    """Full ordered validation issue lists: published v96 plus invalid mutations."""
    from packages.derivation.loader import DerivationSchemas
    from packages.derivation.package_validation import (
        load_published_citizen_checksums, validate_package)
    from tools.package_successor import load_corpus

    content = rr.CONTENT
    core = rr.resolve_core(wl.CORE)
    corpus, _ = load_corpus(content)
    schemas = DerivationSchemas()
    checks = load_published_citizen_checksums(core.content / f"published-packages.{core.registry}.json")
    package = json.loads(core.package_path.read_text(encoding="utf-8"))
    members = package["members"]

    def issues_of(pkg: dict[str, Any], corp: dict[Any, Any]) -> dict[str, Any]:
        result = validate_package(pkg, corp, schemas, checks)
        rows = [[i.member_id, i.version, i.code, i.detail] for i in result.issues]
        return {"ok": result.ok, "count": len(rows), "issues": rows,
                "output_owners_sha": _sha(_canon(result.output_owners)),
                "resolved_members_sha": _sha(_canon(result.resolved_members))}

    out: dict[str, Any] = {"members": len(members)}
    out["published_v96"] = issues_of(package, corpus)

    # m1: remove every source-family member pin
    pkg1 = copy.deepcopy(package)
    pkg1["members"] = [m for m in pkg1["members"]
                       if not (corpus.get((m["id"], m["version"])) or {}).get("schema", "").startswith("source-family")]
    out["mutation_remove_source_families"] = issues_of(pkg1, corpus)

    # m2: remove every 7th member pin
    pkg2 = copy.deepcopy(package)
    pkg2["members"] = [m for i, m in enumerate(pkg2["members"]) if i % 7 != 3]
    out["mutation_drop_every_seventh"] = issues_of(pkg2, corpus)

    # m3: a member pinned at a version the corpus does not hold
    pkg3 = copy.deepcopy(package)
    pkg3["members"][5]["version"] = "v999"
    pkg3["members"][len(pkg3["members"]) // 2]["version"] = "v998"
    out["mutation_unknown_versions"] = issues_of(pkg3, corpus)

    # m4: corpus bodies edited so published checksums no longer match
    corp4 = dict(corpus)
    for index in (1, 17, 41, 103):
        pin = members[index]
        body = copy.deepcopy(corp4[(pin["id"], pin["version"])])
        body["demo_tamper"] = index
        corp4[(pin["id"], pin["version"])] = body
    out["mutation_tampered_citizens"] = issues_of(package, corp4)
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("label")
    parser.add_argument("scratch", type=Path)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--validation-only", action="store_true",
                        help="only the validation error lists; run with PYTHONHASHSEED=0 so set order is fixed")
    args = parser.parse_args()
    scratch = args.scratch.resolve()
    assert REPO not in scratch.parents
    scratch.mkdir(parents=True, exist_ok=True)
    if args.validation_only:
        validation = validation_errors()
        (scratch / f"validation-{args.label}.json").write_text(json.dumps(validation, indent=1, sort_keys=True) + "\n")
        vsum = {name: {"ok": v["ok"], "count": v["count"], "issues_digest": _sha(_canon(v["issues"])),
                       "output_owners_sha": v["output_owners_sha"], "resolved_members_sha": v["resolved_members_sha"]}
                for name, v in validation.items() if isinstance(v, dict) and "issues" in v}
        wl.write(HERE / f"track1-validation-{args.label}.json", {"label": args.label, "hashseed": os.environ.get("PYTHONHASHSEED"), "validation": vsum})
        print(json.dumps(vsum, indent=1))
        return
    lists = rr.recorded_lists()
    assert len(lists) == 775, len(lists)
    if args.limit:
        lists = lists[: args.limit]
    from tests import evidence_loader
    owner = evidence_loader.current_owner()
    if owner:
        evidence_loader.release(owner)
    core = rr.resolve_core(wl.CORE)
    workers = max(1, (os.cpu_count() or 2) - 1)
    part = scratch / f"dump-part-{args.label}.json"
    t0 = time.monotonic()
    results = rr.replay(lists, core, per_list, workers=workers, part=part)
    wall = round(time.monotonic() - t0, 1)
    validation = validation_errors()
    full = {"label": args.label, "lists": results, "validation": validation}
    (scratch / f"dump-{args.label}.json").write_text(json.dumps(full, indent=1, sort_keys=True) + "\n")
    lines = [f"{k}\t{r['outcome']}\t{r.get('result_sha')}\t{r.get('page_sha')}\t{r.get('presentation_sha')}\t{r.get('error')}\t{r.get('message')}"
             for k, r in sorted(results.items())]
    summary = {
        "label": args.label, "core": core.version, "lists": len(results),
        "outcomes": {o: sum(r["outcome"] == o for r in results.values()) for o in ("success", "error", "refused")},
        "errors": sorted({r["error"] for r in results.values() if r["outcome"] == "error"}),
        "per_list_digest": _sha("\n".join(lines).encode("utf-8")),
        "validation": {name: {"ok": v["ok"], "count": v["count"],
                              "issues_digest": _sha(_canon(v["issues"])),
                              "output_owners_sha": v["output_owners_sha"],
                              "resolved_members_sha": v["resolved_members_sha"]}
                       for name, v in validation.items() if isinstance(v, dict) and "issues" in v},
        "members": validation["members"],
        "replay_wall_s": wall,
    }
    wl.write(HERE / f"track1-summary-{args.label}.json", summary)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
