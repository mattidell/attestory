"""P0 probe, part 2: record the OPPOSITE answer for each yes/no scope answer on core v72 and show what changes.

For each root, the survey's return (the one where withholding it blocks a line) is run twice through
``live_coordinate_run``: as built, and with that one fact's recorded value flipped (yes<->no). The lines whose
disposition or value differ are recorded. This is the empirical half of "what each value does"; the rule text is
traced in p0-questions.md. Run from the repository root:

    python3 docs/phases/engine-breadth/milestones/scope-answer-questions-evidence/probe_flip.py

Writes ``probe-flip-output.json`` beside itself. Synthetic ``demo.*`` data only.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))
HERE = Path(__file__).resolve().parent
P = "tax.us.2025."


def _load(path):
    spec = importlib.util.spec_from_file_location(path.stem + "_m", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[path.stem + "_m"] = mod
    spec.loader.exec_module(mod)
    return mod


def lines(r):
    out = {}
    for s in r.model["sections"]:
        res = s["resolved"]
        out[s["id"]] = {"label": s["field"].get("label"), "form": s["field"].get("form", {}).get("form_id"),
                        "disposition": res["disposition"], "value": res.get("value"), "codes": res.get("activeCodes")}
    return out


def run_case(args):
    run_id, spec, root, other = args
    survey = _load(HERE.parent / "missing-input-questions-evidence" / "probe.py")
    from tests import test_statement_withholding_answer as swa
    from tests.helpers import current_core_returns as c
    swa.CORES["v72"] = ("package.core-calculations.v72.json", "v72", "demo.release.sli-worksheet-integration.2025.v70.json",
                        "v70", "published-packages.v70.json")
    # the survey's spec is withhold:<return>:<fact>; rebuild the same return with the fact present
    _, ret, _ = spec.split(":", 2)
    ret = spec.split(":")[1]
    acts = copy.deepcopy(c.base_return() if ret == "base" else survey._adder(ret))
    ft = P + root
    hits = [a for a in acts if str(a["payload"].get("finding", {}).get("fact_id", "")).split("|")[0] == ft]
    try:
        before = hits[0]["payload"]["finding"]["value"]
        after = other
        if after is None or after == before:
            after = {"yes": "no", "no": "yes"}[before]
        base = lines(swa.run(copy.deepcopy(acts), run_id + ".as-built", "v72"))
        flipped_acts = copy.deepcopy(acts)
        for a in flipped_acts:
            f = a["payload"].get("finding")
            if f and str(f["fact_id"]).split("|")[0] == ft:
                f["value"] = after
        flip = lines(swa.run(flipped_acts, run_id + ".flipped", "v72"))
        diff = {k: {"as_built": base[k], "flipped": flip[k]} for k in base
                if (base[k]["disposition"], base[k]["value"]) != (flip[k]["disposition"], flip[k]["value"])}
        return {"root": root, "return": ret, "as_built_value": before, "flipped_value": after, "status": "ran", "changed": diff}
    except Exception as exc:
        return {"root": root, "return": ret, "status": "error", "error": f"{type(exc).__name__}: {exc}"[:500]}


def main():
    out = json.loads((HERE / "probe-output.json").read_text(encoding="utf-8"))
    todo = [(f"demo.p0.sa.flip.{c['root']}", c["spec"], c["root"], None) for c in out["cases"]]
    res = []
    with ProcessPoolExecutor(max_workers=6) as pool:
        for r in pool.map(run_case, todo):
            res.append(r)
            print(r["root"], r["status"], r.get("as_built_value"), "->", r.get("flipped_value"), len(r.get("changed", {})), flush=True)
    (HERE / "probe-flip-output.json").write_text(json.dumps({"core": "v72", "cases": res}, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
