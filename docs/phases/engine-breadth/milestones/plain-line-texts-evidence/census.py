"""P0: published v95 live runs and saved pages; no production changes.

Run: python3 census.py <outside-repository-directory> [--smoke]
The resumable part and complete models/pages stay outside the repository.
Only synthetic recorded lists and demo.* supplementary cases are used.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from tools import recorded_replay as rr
from packages.derivation.live_session import _render_page

P = "tax.us.2025."
TERMS = ["derived finding", "finding", "closed-empty", "closed with members",
         "authority", "authorizes", "subtotal 0", "publishes", "honest", "family",
         "citizen", "id", "version", "published", "closure", "guard", "dependency",
         "disposition", "pin", "computation", "applicability", "field-mapping",
         "cross-form-bridge", "source_nonempty", "source_empty"]


def load(name, path):
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


def matches(text):
    found = [term for term in TERMS if re.search(r"\b" + re.escape(term) + r"(?:s)?\b", text, re.I)]
    if re.search(r"\b(?:tax\.us\.|demo\.)", text): found.append("identifier")
    if re.search(r"\bv\d+\b|@[0-9]+", text): found.append("version string")
    return sorted(set(found))


def write(path, body):
    text = json.dumps(body, indent=2) + "\n"
    assert not re.search(r"/(?:Users|private|tmp|var)/", text)
    path.write_text(text)


def synthetic():
    l6b = load("plt_census_l6b", HERE.parent / "line6b-reason-evidence/probe.py")
    h = rr._get_harness()
    rows = []
    for status in ("single", "married_filing_jointly", "married_filing_separately"):
        rows.append(("demo.plt.wage." + status, l6b.base(status, benefits=False)))
    rows.append(("demo.plt.blocked-names", h.opened()))
    # A represented Schedule D sale with the previously reviewed answer set.
    acts = h.sale(h.opened(), "no1099b", "st", proceeds=2000, basis=8000, tag="demo.plt.sale")
    acts = h.answer(acts, **h.honest({"no1099b"}, loss=True, new_questions=True))
    acts = h.say(acts, P + "f1099b.no-sale-box4-present", "no", "demo.plt.box4")
    rows.append(("demo.plt.sale", acts))
    acts = h.ccr.add_tax_exempt_interest_1099int(h.ccr.base_return(), [400.0])
    acts = h.ccr.add_exempt_interest_dividends_1099div(acts, [200.0])
    acts = h.ccr.add_foreign_tax_1099div(acts, [10.0])
    rows.append(("demo.plt.interest-dividends", acts))
    rows.append(("demo.plt.refused", h.ccr.base_return()))
    # The refused case removes package adoption at the real resolver boundary.
    return rows


def per_list(key, acts, core):
    scratch = Path(os.environ["PLT_CENSUS_SCRATCH"])
    slug = hashlib.sha256(key.encode()).hexdigest()[:20]
    h = rr._get_harness()
    try:
        with h.loader_entries(core):
            finished = h._finish(acts, package_path=core.package_path, package_version=core.version,
                                 release_path=core.release_path, release_version=core.release_version,
                                 note="demo.plt." + slug)
            finished = h._handover(finished, surface=core.surface(), reconfirm=True)
            if key == "demo.plt.refused":
                finished = h.renumber([a for a in finished if a["kind"] != "package-adoption"])
            with tempfile.TemporaryDirectory() as tmp:
                capability = h.WorkspaceCapability(Path(tmp) / "L")
                outcome = h.live_coordinate_run(capability, repo_root=REPO,
                    authoritative_acts=finished, workspace_revision=len(finished),
                    run_scope={"jurisdiction": "us", "year": h.YEAR}, scope_user=h.ccr.USER,
                    request={"schema": "run-request.v1"}, run_id="demo.plt." + slug,
                    governance_pins=[], surface=core.surface(), output_name="out.json")
                if outcome.refusal:
                    return {"outcome": "refused", "reason": outcome.refusal.reason}
                model = json.loads(outcome.presentation_path.read_text())
                report = json.loads(outcome.output_path.read_text())
                write(scratch / (slug + ".model.json"), model)
                (scratch / (slug + ".html")).write_bytes(_render_page(REPO, capability, outcome.presentation_path))
                pin = {"outcome": "success", "stop": report.get("stop_reason"),
                        "page": slug + ".html", "model": slug + ".model.json",
                        "rows": report["dispositions"],
                        "values": [{"symbol": p.finding.get("symbol"), "value": p.finding.get("value")}
                                   for p in outcome.publications or ()]}
                if os.environ.get("PLT_COMPACT_PART") == "1":
                    write(scratch / (slug + ".pin.json"), pin)
                    return {k: v for k, v in {**pin, "pin": slug + ".pin.json"}.items() if k not in ("rows", "values")}
                return pin
    except Exception as exc:
        return {"outcome": "error", "error": type(exc).__name__,
                "message": re.sub(r"/(?:Users|private|tmp|var|opt)/\S+", "<path>", str(exc))[:600]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("scratch", type=Path)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--core", default="v95")
    parser.add_argument("--summary", default=None, help="Evidence output filename")
    parser.add_argument("--p0b", action="store_true", help="include mortgage and student-loan detail cases; compact resumable index")
    args = parser.parse_args()
    scratch = args.scratch.resolve()
    assert scratch != REPO and REPO not in scratch.parents
    scratch.mkdir(parents=True, exist_ok=True)
    os.environ["PLT_CENSUS_SCRATCH"] = str(scratch)
    rows = synthetic()
    if args.p0b:
        h = rr._get_harness()
        rows += [("demo.plt.mortgage-detail", h.ccr.add_mortgage_itemizer(h.ccr.base_return(), 18000.0)),
                 ("demo.plt.student-loan-detail", h.ccr.add_student_loan_interest_1098e(h.ccr.base_return(), [700.0]))]
        os.environ["PLT_COMPACT_PART"] = "1"
    if not args.smoke:
        recorded = rr.recorded_lists()
        assert len(recorded) == 775
        rows = recorded + rows
    from tests import evidence_loader
    owner = evidence_loader.current_owner()
    if owner: evidence_loader.release(owner)
    started = time.monotonic()
    workers = max(1, (os.cpu_count() or 2) - 1)
    core = rr.resolve_core(args.core)
    results = rr.replay(rows, core, per_list,
                        workers=workers, part=scratch / "census-part.json")
    wall = round(time.monotonic() - started, 3)
    # Browser manifest is private runtime configuration, never public evidence.
    (scratch / "cases.json").write_text(json.dumps({"root": str(scratch), "cases": [
        {"id": key, "page": r["page"]} for key, r in results.items() if r["outcome"] == "success"]}))
    summary_name = args.summary or ("smoke.json" if args.smoke else "live-summary.json")
    assert Path(summary_name).name == summary_name
    write(HERE / summary_name, {
        "source": {"core": core.version, "registry": core.registry, "release": core.release_version}, "workers": workers,
        "lists": len(results), "wall_time_s": wall,
        "recorded_outcomes": dict(Counter(r["outcome"] for k, r in results.items() if not k.startswith("demo.plt."))),
        "synthetic_outcomes": {k: {x: v for x, v in r.items() if x not in ("rows", "values", "model", "page")}
                               for k, r in results.items() if k.startswith("demo.plt.")},
        "stops": dict(Counter(str(r.get("stop")) for r in results.values() if r["outcome"] == "success")),
        "errors": dict(Counter(r.get("error") for r in results.values() if r["outcome"] == "error"))})
    print(json.dumps({"lists": len(results), "wall_time_s": wall, "outcomes": dict(Counter(r["outcome"] for r in results.values()))}))


if __name__ == "__main__":
    main()
