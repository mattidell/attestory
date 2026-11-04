"""Scratch-v73 verification (P0). Run with cwd = a repository root (the real one or the scratch copy).

    python3 verify_v73.py v73 <out.json>   # withhold each fact on core v73; record the reasons on every blocked line
    python3 verify_v73.py v72 <out.json>   # same cases on core v72; record a hash of each saved presentation model

The cases are the survey's: the return in which withholding the fact blocks a line (probe-output.json).
Only ``v73`` needs the scratch tree (it carries the citizens and the prototype projection change).
"""
import hashlib
import importlib.util
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

REPO = Path.cwd().resolve()
sys.path.insert(0, str(REPO))
SURVEY = REPO / "docs/phases/engine-breadth/milestones/missing-input-questions-evidence/probe.py"
EVID = Path(__file__).resolve().parent
CORES = {"v72": ("package.core-calculations.v72.json", "v72", "demo.release.sli-worksheet-integration.2025.v70.json", "v70", "published-packages.v70.json"),
         "v73": ("package.core-calculations.v73.json", "v73", "demo.release.sli-worksheet-integration.2025.v71.json", "v71", "published-packages.v71.json")}


def _survey():
    spec = importlib.util.spec_from_file_location("survey_probe", SURVEY)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["survey_probe"] = mod
    spec.loader.exec_module(mod)
    return mod


def cases():
    out = json.loads((EVID / "probe-output.json").read_text(encoding="utf-8"))["cases"]
    rows = [(c["root"], c["spec"]) for c in out]
    rows.append(("filing-status", "withhold:base:tax.us.2025.filing-status"))
    return rows


def run_case(args):
    core, root, spec = args
    mod = _survey()
    from tests import test_statement_withholding_answer as swa
    swa.CORES.update(CORES)
    pkg = CORES[core][0]
    import glob
    content = REPO / "packages/content/tax/2025"
    package = json.loads((content / pkg).read_text(encoding="utf-8"))
    index = {}
    for name in glob.glob(str(content / "*.json")):
        try:
            body = json.loads(Path(name).read_text(encoding="utf-8"))
        except ValueError:
            continue
        if isinstance(body, dict) and "id" in body and "version" in body:
            index[(body["id"], body["version"])] = body
    mod._PUBLISHES = {str(index[(m["id"], m["version"])]["id"]): str(index[(m["id"], m["version"])]["publishes"])
                      for m in package["members"] if "publishes" in index[(m["id"], m["version"])]}
    try:
        r = swa.run(mod.build(spec), f"demo.p0.sa.verify.{root}", core)
        summary = mod.summarize_run(r)
        digest = hashlib.sha256(json.dumps(r.model, sort_keys=True).encode()).hexdigest()
        return {"root": root, "core": core, "status": "ran", "model_sha256": digest, "lines": summary["blocked_lines"]}
    except Exception as exc:
        return {"root": root, "core": core, "status": "error", "error": f"{type(exc).__name__}: {exc}"[:300]}


def main():
    core, dest = sys.argv[1], Path(sys.argv[2])
    todo = [(core, r, s) for r, s in cases()]
    res = []
    with ProcessPoolExecutor(max_workers=6) as pool:
        for r in pool.map(run_case, todo):
            res.append(r)
            print(r["root"], r["status"], flush=True)
    dest.write_text(json.dumps({"core": core, "cases": res}, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
