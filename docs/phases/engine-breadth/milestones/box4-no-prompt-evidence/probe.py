"""P0 matrix through real live coordination and presentation, with no sentence filter."""
from __future__ import annotations
import argparse
import copy
import importlib.util
import json
import multiprocessing
import os
from pathlib import Path
import re
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
P = "tax.us.2025."
AMOUNT = P + "f1099b.statement-box4-withholding"
REPORTED = P + "f1099b.statement-box4-withholding-reported"
PRESENT = P + "f1099b.no-sale-box4-present"
STATUSES = ("single", "married_filing_jointly", "married_filing_separately")

def load(name, path):
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]

def old():
    return load("b4n_amount_precedent", HERE.parent / "box4-amount-asked-evidence/probe.py")

def write(path, body):
    text = json.dumps(body, indent=2) + "\n"
    if re.search(r"/(Users|private|tmp|var)/", text):
        raise ValueError("public evidence contains a local path")
    path.write_text(text)

def cases():
    b = old()
    h, _ = b._mods()
    rows = []
    for status in STATUSES:
        for label, answers, present, level in (
            ("yes-200", [("yes", 200)], "no", None),
            ("yes-absent", [("yes", None)], "no", None),
            ("no-absent", [("no", None)], "no", None),
            ("no-zero", [("no", 0)], "no", None),
            ("no-200", [("no", 200)], "no", None),
            ("unanswered", [(None, None)], "no", None),
            ("unanswered-200", [(None, 200)], "no", None),
            ("mixed-no-yes-200", [("no", None), ("yes", 200)], "no", None),
            ("mixed-no-yes-absent", [("no", None), ("yes", None)], "no", None),
            ("mixed-no-unanswered", [("no", None), (None, None)], "no", None),
            ("two-no", [("no", None), ("no", None)], "no", None),
            ("return-yes-150", [("no", None)], "yes", 150),
            ("return-yes-absent", [("no", None)], "yes", None),
            ("no-1099b", [], "no", None),
        ):
            acts = h.opened()
            for i, _answer in enumerate(answers):
                acts = h.sale(acts, "covered", "st", proceeds=5000, basis=4000, tag=f"b4n{i}")
            acts = b.prepare_covered(acts)
            acts = b.strip_fact(acts, REPORTED)
            for i, (answer, amount) in enumerate(answers):
                stmt = f"demo.sfa.b4n{i}.statement"
                if answer is not None:
                    acts = b.say_stmt(acts, REPORTED, stmt, answer, "b4n.reported")
                if amount is not None:
                    acts = b.say_stmt(acts, AMOUNT, stmt, amount, "b4n.amount")
            acts = h.say(acts, PRESENT, present, "b4n.present")
            if level is not None:
                acts = h.say(acts, b.RETURN_AMT, level, "b4n.return")
            for fact, value in (("filing-status", status), ("taxpayer-over-65", False),
                                ("taxpayer-blind", False), ("spouse-over-65", False),
                                ("spouse-blind", False), ("mfs-lived-apart-all-year", "yes")):
                acts = h.say(acts, P + fact, value, "b4n." + fact)
            rows.append({"id": status + "." + label, "answers": answers,
                         "present": present, "return_amount": level,
                         "truthful": label != "no-200", "acts": acts})
    for ident, acts, note in b.build_lists()[:6]:
        rows.append({"id":"recorded."+ident, "answers":b.box4_of(acts),
                     "truthful":True, "note":note, "acts":acts})
    return rows

def run(row, spec):
    b = old()
    h, _ = b._mods()
    from tools.recorded_replay import resolve_core
    core = resolve_core(spec)
    # Reuse the real live-run entry, selecting the core explicitly.
    l6 = load("b4n_live_entry", HERE.parent / "line6b-reason-evidence/probe.py")
    result = l6.run(copy.deepcopy(row["acts"]), "demo.b4n." + core.version + "." + row["id"], core)
    if result["outcome"] != "success":
        return {**{k:v for k,v in row.items() if k != "acts"}, **result}
    from tests import evidence_loader
    evidence_loader.activate(b.OWNER)
    common = evidence_loader.load(b.BNQ / "common.py", "common")
    publishes = common.rule_publishes(core)
    by_symbol = {}
    for r in result["report"].get("dispositions", []):
        by_symbol.setdefault(r.get("symbol") or publishes.get(r.get("artifact_id")), []).append(r)
    lines = {}
    sentences = []
    for section in result["model"].get("sections", []):
        field, resolved = section.get("field", {}), section.get("resolved", {})
        reasons = resolved.get("reasons", [])
        sentences.extend(r["sentence"] for r in reasons if isinstance(r, dict) and "sentence" in r)
        ident = field.get("id", "").removeprefix(P + "form1040.line-")
        if ident not in ("25b", "25d", "33", "37"):
            continue
        lines[ident] = {"disposition": resolved.get("disposition"), "value": resolved.get("value"),
                        "active_codes": resolved.get("activeCodes"), "reasons": reasons,
                        "instructions": field.get("dispositions", {}).get(resolved.get("disposition")),
                        "rows": [{k:r.get(k) for k in ("artifact_id", "disposition", "code", "missing", "value")}
                                 for r in by_symbol.get(field.get("binds_symbol"), [])]}
    prompt = json.loads((b.CONTENT / "input-question.f1099b-box4.v1.json").read_text())["question"]
    evidence_loader.finish(b.OWNER)
    return {**{k:v for k,v in row.items() if k != "acts"}, "outcome": "success", "lines": lines,
            "page_sentences": list(dict.fromkeys(sentences)), "page_has_amount_prompt": prompt in sentences}

def worker(payload):
    row, spec = payload
    try:
        return run(row, spec)
    except Exception as exc:
        return {"id": row["id"], "outcome": "error", "error": type(exc).__name__,
                "message": re.sub(r"/(?:Users|private|tmp|var)/\S+", "<path>", str(exc))[:600]}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", default="v93")
    parser.add_argument("--out", default="probe-output.json")
    parser.add_argument("--supplement", action="store_true")
    args = parser.parse_args()
    rows = cases()
    if args.supplement:
        rows = [r for r in rows if r["id"].startswith("recorded.")]
    from tests import evidence_loader
    owner = evidence_loader.current_owner()
    if owner:
        evidence_loader.release(owner)
    workers = max(1, (os.cpu_count() or 2)-1)
    started = time.monotonic()
    with multiprocessing.get_context("spawn").Pool(workers) as pool:
        results = pool.map(worker, [(r, args.core) for r in rows])
    elapsed = round(time.monotonic()-started, 3)
    if args.supplement:
        previous = json.loads((HERE / args.out).read_text())
        results = [r for r in previous["cases"] if not r["id"].startswith("recorded.")] + results
        elapsed += previous["wall_time_s"]
    from tools.recorded_replay import core_fingerprint, resolve_core
    write(HERE / args.out, {"core": core_fingerprint(resolve_core(args.core)), "workers": workers,
                           "wall_time_s": elapsed, "cases": results})
    print(json.dumps({"cases": len(results), "outcomes": {x:sum(r["outcome"]==x for r in results)
          for x in {r["outcome"] for r in results}}, "no_absent": [
              {"id":r["id"], "lines":{k:v["disposition"] for k,v in r.get("lines",{}).items()},
               "prompt": r.get("page_has_amount_prompt")} for r in results if r["id"].endswith(".no-absent")]}, indent=2))

if __name__ == "__main__":
    main()
