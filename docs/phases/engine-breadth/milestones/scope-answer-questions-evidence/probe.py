"""P0 probe for scope-answer-questions: withhold each yes/no scope answer and filing status on core v72.

Reuses the missing-input survey's probe (builders, summary walk) and its probe-output.json (to pick, for each
root, a return in which withholding it blocks a line). Re-runs each withheld case through ``live_coordinate_run``
on the committed core v72 / registry v70 / release v70. Run from the repository root:

    python3 docs/phases/engine-breadth/milestones/scope-answer-questions-evidence/probe.py

Writes ``probe-output.json`` beside itself. Synthetic ``demo.*`` data only.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))
HERE = Path(__file__).resolve().parent
SURVEY = REPO / "docs/phases/engine-breadth/milestones/missing-input-questions-evidence"
OUT = HERE / "probe-output.json"
AMOUNTS = {"f1099div.box4-withholding", "f1099g.box4-withholding", "f1099int.box4-withholding", "f1099r.ira-box4-withholding",
           "ssa1099.box6-voluntary-withholding", "w2.box2-withholding", "payments.estimated-and-prior-year-applied",
           "payments.overpayment-applied-to-2026", "f1098.residence-interest-reason", "f1099b.covered-w-lt",
           "f1099b.covered-w-st", "rounding.convention"}


def _survey():
    spec = importlib.util.spec_from_file_location("survey_probe", SURVEY / "probe.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["survey_probe"] = mod
    spec.loader.exec_module(mod)
    content = REPO / "packages/content/tax/2025"
    mod._PUBLISHES = None
    src = mod.publishes
    # point the publishes() index at the v72 package
    import re
    text = (SURVEY / "probe.py").read_text(encoding="utf-8")
    return mod


def _v72_publishes(mod):
    import glob
    content = REPO / "packages/content/tax/2025"
    package = json.loads((content / "package.core-calculations.v72.json").read_text(encoding="utf-8"))
    index = {}
    for name in glob.glob(str(content / "*.json")):
        try:
            body = json.loads(Path(name).read_text(encoding="utf-8"))
        except ValueError:
            continue
        if isinstance(body, dict) and "id" in body and "version" in body:
            index[(body["id"], body["version"])] = body
    out = {}
    for m in package["members"]:
        body = index[(m["id"], m["version"])]
        if "publishes" in body:
            out[str(body["id"])] = str(body["publishes"])
    mod._PUBLISHES = out


def run_case(args):
    run_id, spec, root = args
    mod = _survey()
    _v72_publishes(mod)
    from tests import test_statement_withholding_answer as swa
    swa.CORES["v72"] = ("package.core-calculations.v72.json", "v72", "demo.release.sli-worksheet-integration.2025.v70.json",
                        "v70", "published-packages.v70.json")
    try:
        summary = mod.summarize_run(swa.run(mod.build(spec), run_id, "v72"))
        held = [l for l in summary["blocked_lines"] if any(m and m[0] == root for _, m in l["leaves"])]
        return {"run_id": run_id, "spec": spec, "root": root, "status": "ran", "lines_held": held,
                "all_blocked": len(summary["blocked_lines"])}
    except Exception as exc:
        return {"run_id": run_id, "spec": spec, "root": root, "status": "error", "error": f"{type(exc).__name__}: {exc}"[:400]}


def main():
    old = json.loads((SURVEY / "probe-output.json").read_text(encoding="utf-8"))
    chosen = {}
    for c in sorted(old["cases"], key=lambda c: (not c["run_id"].startswith("demo.p0.mi.A."), c["run_id"])):
        if c["status"] != "ran":
            continue
        for l in c["blocked_lines"]:
            for code, m in l["leaves"]:
                if code == "ABSENT" and m[0] not in AMOUNTS and m[0] not in chosen and m[0] == c["spec"].split(":")[-1].replace("tax.us.2025.", ""):
                    chosen[m[0]] = c["spec"]
    todo = [(f"demo.p0.sa.{r}", s, r) for r, s in sorted(chosen.items())]
    print(len(todo), "roots", flush=True)
    results = []
    with ProcessPoolExecutor(max_workers=6) as pool:
        for res in pool.map(run_case, todo):
            results.append(res)
            print(res["run_id"], res["status"], len(res.get("lines_held", [])), flush=True)
    OUT.write_text(json.dumps({"core": "v72", "cases": results}, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
