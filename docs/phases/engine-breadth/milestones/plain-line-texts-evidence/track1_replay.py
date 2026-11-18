"""Track 1 replay of published core v95 against published core v96.

The published validator carries the Decision 5 v96 entry, so nothing is injected
and the successor core is the published version string.

Run: python3 track1_replay.py <baseline> v96 <new-results-outside-repo> [--smoke]
The resumable comparison part references complete rows and models next to
it and in the preserved baseline directory. Track 0 can reclassify without
running either core again. All processes are joined before return.
"""
from __future__ import annotations
import argparse
from collections import Counter
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
def load(name, path):
    spec = importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec); sys.modules[name]=module; spec.loader.exec_module(module)
    return module

census = load("plt_p0c_live_census", HERE / "census.py")
runtime = load("plt_p0c_live_runtime", HERE / "p0c_runtime.py")
compare = load("plt_p0c_complete_compare", HERE / "p0c_compare.py")
rr = census.rr
_BASE = None

def baseline():
    global _BASE
    root=Path(os.environ["PLT_P0C_BASELINE"])
    if _BASE is None: _BASE=json.loads((root/"census-part.json").read_text())["results"]
    return root,_BASE

def per_list(key,acts,cores):
    rr._get_harness()
    result=census.per_list(key,acts,cores[1])
    root,base=baseline(); target=Path(os.environ["PLT_CENSUS_SCRATCH"])
    a,am=compare.read_pin(root,base[key]); b,bm=compare.read_pin(target,result)
    verdict=compare.classify(a,am,b,bm)
    return {"class":verdict["class"],"result":result,"comparison":verdict,
            "input_sha256":hashlib.sha256(compare.encoded(acts).encode()).hexdigest()}

def pairs(results,base_root,target):
    base=json.loads((base_root/"census-part.json").read_text())["results"]
    return {key:compare.classify(*compare.read_pin(base_root,base[key]),
                                *compare.read_pin(target,row["result"])) for key,row in results.items()}

def mutation_controls(results,base_root,target):
    base=json.loads((base_root/"census-part.json").read_text())["results"]
    key=next(k for k,r in results.items() if r["result"]["outcome"]=="success" and any(
        x.get("disposition")=="blocked" and x.get("missing") for x in compare.read_pin(target,r["result"])[0]["rows"]))
    a,am=compare.read_pin(base_root,base[key]); b,bm=compare.read_pin(target,results[key]["result"])
    assert compare.classify(a,am,b,bm)["class"]=="expected_sentences"
    controls={}
    for kind in ("value","page_value","boolean_value","disposition","code","missing_name","unplanned_sentence",
                 "question_identity","added_row","removed_row","added_field","removed_field","planned_text_wrong_property"):
        altered,model=copy.deepcopy(b),copy.deepcopy(bm)
        blocked=next(r for r in altered["rows"] if r.get("disposition")=="blocked" and r.get("missing"))
        if kind=="value": altered["values"][0]["value"]="demo.changed-value"
        if kind in ("page_value","boolean_value"):
            field=next(s for s in model["sections"] if isinstance(s["resolved"].get("value"),(int,float)))
            field["resolved"]["value"]=True if kind=="boolean_value" else 1234567
        if kind=="disposition": blocked["disposition"]="published"
        if kind=="code": blocked["code"]="demo.unplanned-code"
        if kind=="missing_name": blocked["missing"].append("demo.unplanned-missing")
        if kind=="unplanned_sentence": model["sections"][0]["field"]["label"] += " demo.unplanned sentence"
        if kind=="question_identity":
            reason=next(s["resolved"]["reasons"][0] for s in model["sections"] if s["resolved"].get("reasons"))
            reason["question_id"]="demo.unplanned-question"
        if kind=="added_row": altered["rows"].append({"artifact_id":"demo.extra-row","disposition":"blocked","missing":[]})
        if kind=="removed_row": altered["rows"].pop()
        if kind=="added_field": model["sections"].append(copy.deepcopy(model["sections"][0]))
        if kind=="removed_field": model["sections"].pop()
        if kind=="planned_text_wrong_property":
            text=json.loads((HERE/"p0c-wording.json").read_text())["replacements"][0]["new_shown"]
            model["sections"][0]["field"]["label"]=text
        verdict=compare.classify(a,am,altered,model)
        controls[kind]={"rejected":verdict["class"]=="unexpected","gate":verdict.get("gate")}
    assert all(v["rejected"] for v in controls.values()), controls
    mortgage="demo.plt.mortgage-detail"
    if mortgage in results:
        ma,mam=compare.read_pin(base_root,base[mortgage]); mb,mbm=compare.read_pin(target,results[mortgage]["result"])
        for kind in ("box_value", "added_box_observation", "removed_box_observation"):
            model=copy.deepcopy(mbm)
            records=model["mortgageBorrowingExplanation"]["reports"][0]["boxObservations"]
            if kind=="box_value": records[0]["value"]="demo.unplanned-value"
            if kind=="added_box_observation": records.append(copy.deepcopy(records[0]))
            if kind=="removed_box_observation": records.pop()
            verdict=compare.classify(ma,mam,mb,model)
            controls[kind]={"rejected":verdict["class"]=="unexpected","gate":verdict.get("gate")}
        assert all(v["rejected"] for v in controls.values())
    return {"case":key,"controls":controls}

def main():
    start=time.monotonic()
    parser=argparse.ArgumentParser(); parser.add_argument("baseline",type=Path); parser.add_argument("core",type=Path)
    parser.add_argument("target",type=Path); parser.add_argument("--smoke",action="store_true"); parser.add_argument("--classify-only",action="store_true")
    args=parser.parse_args(); target=args.target.resolve(); base_root=args.baseline.resolve()
    assert REPO not in target.parents and REPO not in base_root.parents
    target.mkdir(parents=True,exist_ok=True)
    os.environ.update({"PLT_P0C_BASELINE":str(base_root),"PLT_CENSUS_SCRATCH":str(target),"PLT_COMPACT_PART":"1"})
    core=rr.resolve_core(args.core); old=rr.resolve_core("v95")
    part=target/"strict-replay-part.json"
    if args.classify_only:
        saved=json.loads(part.read_text())
        assert saved["_metadata"]["cores"]==[rr.core_fingerprint(old),rr.core_fingerprint(core)]
        results=saved["results"]
        timing=json.loads((target/"timing.json").read_text())
    else:
        cases=census.synthetic(); h=rr._get_harness()
        cases += [("demo.plt.mortgage-detail",h.ccr.add_mortgage_itemizer(h.ccr.base_return(),18000.0)),
                  ("demo.plt.student-loan-detail",h.ccr.add_student_loan_interest_1098e(h.ccr.base_return(),[700.0]))]
        if not args.smoke:
            recorded=rr.recorded_lists(); assert len(recorded)==775; cases=recorded+cases
        from tests import evidence_loader
        owner=evidence_loader.current_owner()
        if owner: evidence_loader.release(owner)
        baseline_index=json.loads((base_root/"census-part.json").read_text())
        assert baseline_index["_metadata"]["cores"]==[rr.core_fingerprint(old)]
        assert all(k in baseline_index["results"] for k,_ in cases)
        replay_start=time.monotonic()
        results=rr.replay(cases,(old,core),per_list,workers=max(1,(os.cpu_count() or 2)-1),part=part)
        timing={"successor_replay_wall_time_s":round(time.monotonic()-replay_start,3),
                "invocation_wall_time_s":round(time.monotonic()-start,3)}
        (target/"timing.json").write_text(json.dumps(timing))
    classified=pairs(results,base_root,target)
    for key,row in results.items():
        row["class"]=classified[key]["class"]; row["comparison"]=classified[key]
    rr._write_part(part,results,{"cores":[rr.core_fingerprint(old),rr.core_fingerprint(core)],
        "format":"plain-line-texts.strict-replay.v1",
        "baseline_part":os.path.relpath(base_root/"census-part.json",target),
        "wording_sha256":hashlib.sha256((HERE/"p0c-wording.json").read_bytes()).hexdigest(),
        "validator_injection":"none: published validator carries the Decision 5 v96 graph"})
    counts=Counter(r["class"] for k,r in classified.items() if not k.startswith("demo.plt."))
    extra=Counter(r["class"] for k,r in classified.items() if k.startswith("demo.plt."))
    unexpected={k:r for k,r in classified.items() if r["class"]=="unexpected"}
    output={"recorded_lists":sum(not k.startswith("demo.plt.") for k in results),"counts":dict(counts),
            "synthetic_counts":dict(extra),"synthetic_lists":sum(k.startswith("demo.plt.") for k in results),
            "workers":max(1,(os.cpu_count() or 2)-1),**timing,"baseline_reused":True,
            "rows_compared":sum(r.get("rows_compared",0) for r in classified.values()),
            "page_fields_compared":sum(r.get("fields_compared",0) for r in classified.values()),
            "unexpected":unexpected,"classification_by_list":{k:v["class"] for k,v in classified.items()}}
    name="track1-smoke.json" if args.smoke else "track1-replay.json"
    census.write(HERE/name,output)
    print(json.dumps({k:v for k,v in output.items() if k!="classification_by_list"},indent=2))
    assert not unexpected, "unexpected comparison changes; inspect evidence summary"
    controls=mutation_controls(results,base_root,target)
    census.write(HERE/("track1-smoke-mutations.json" if args.smoke else "track1-mutations.json"),controls)
    # Manifest for optional actual-browser checks; the unmodified production
    # page bytes were already generated and schema-validated for every run.
    (target/"cases.json").write_text(json.dumps({"root":str(target),"cases":[{"id":k,"page":r["result"]["page"]}
        for k,r in results.items() if r["result"]["outcome"]=="success"]}))


if __name__=="__main__": main()
