"""Track 0 display-only closure under foreman Decisions 8 and 9.

Run: python3 <this-file> <P0-core.json> --instructions <local-1040-text>
The existing scratch citizens are read, never rewritten. Synthetic facts are
set using Decision 8 and compared through real coordinate runs and pages.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from functools import lru_cache

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))


def module(name: str, path: Path):
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, path)
        loaded = importlib.util.module_from_spec(spec)
        sys.modules[name] = loaded
        spec.loader.exec_module(loaded)
    return sys.modules[name]


probe = module("l6b_t0_probe", HERE / "probe.py")
proto = module("l6b_t0_proto", HERE / "prototype.py")
from tools import recorded_replay as rr
from packages.derivation.live_session import _render_page



def read(path: Path):
    return json.loads(path.read_text())


def refs(node):
    if isinstance(node, dict):
        found = {node["name"]} if node.get("op") == "ref" else set()
        return found | set().union(*(refs(v) for v in node.values()))
    if isinstance(node, list):
        return set().union(*(refs(v) for v in node))
    return set()


def catalog(core, instructions: Path):
    laws = read(HERE / "law.json")
    text = instructions.read_text().splitlines()
    assert hashlib.sha256(instructions.read_bytes()).hexdigest() == laws["source"]["text_sha256"]
    facts = {}
    for name in ("ss-benefits-scope.bundle.json", "schedule1-adjustments-scope.bundle.json", "ssa1099.bundle.v2.json"):
        for fact in read(probe.CONTENT / name)["fact_types"]:
            facts[fact["id"]] = (name, fact)
    package = read(core.package_path)
    rules = []
    for member in package["members"]:
        if member["role"] != "computation":
            continue
        slug = member["id"].removeprefix(probe.P)
        for path in (core.content / f"{slug}.{member['version']}.json", core.content / f"{slug}.json"):
            if path.is_file():
                body = read(path)
                if body.get("id") == member["id"] and body.get("version") == member["version"]:
                    rules.append((path.name, body))
                    break
    # Positions in the exact local extract retained by P0. Printed pages 31-32.
    spans = {
        "no-unsupported-line1-entries": (2075, 2075),
        "no-pension-annuity-line5b": (2075, 2075),
        "no-traditional-ira-deduction": (2038, 2045),
        "no-form-2555": (1981, 1985), "no-form-4563": (1981, 1985),
        "no-form-8815": (1981, 1985), "no-excluded-adoption-benefits": (1981, 1985),
        "no-puerto-rico-or-samoa-income": (1981, 1985),
        "no-line24z-writein": (2063, 2064), "mfs-lived-apart-all-year": (2085, 2092),
    }
    result = []
    for name, expected in proto.artifacts():
        raw = (core.content / name).read_bytes()
        assert raw == (json.dumps(expected, indent=2) + "\n").encode(), "P0 citizen bytes must remain unchanged"
        citizen = json.loads(raw)
        fact_id = citizen["fact_type"]["id"]
        bundle, fact = facts[fact_id]
        suffix = fact_id.rsplit(".", 1)[-1]
        start, end = spans[suffix]
        negative = suffix.startswith("no-")
        readers = [{"file": path, "id": r["id"], "version": r["version"],
                    "publishes": r["publishes"],
                    "needed_to_publish": "yes (the excluded class is absent)" if negative else
                        "no (lived with spouse at some time)" if r["id"].endswith("line6d-not-checked") else
                        "yes (apart all year)" if r["id"].endswith("line6d") else
                        "yes (apart all year) or no (lived with spouse at some time); chooses worksheet branch"}
                   for path, r in rules if fact_id in refs(r.get("when")) | refs(r.get("value"))]
        result.append({
            "citizen": citizen, "citizen_sha256": hashlib.sha256(raw).hexdigest(),
            "fact": fact, "fact_source": bundle,
            "readers": readers,
            "source": {"filename": "i1040gi-2025.txt", "start_line": start, "end_line": end,
                       "quote_from_layout_extract": text[start-1:end],
                       "assessment": next(c["assessment"] for c in laws["checks"] if c["fact"] == fact_id)},
            "expected_filer_meaning": {"yes": "no" if negative else "yes", "no": "yes" if negative else "no"},
            "wording_verdict": "PASS",
            "convention": "positive question about excluded circumstance: no means absence fact yes" if negative else "positive question matching the affirmative living-apart fact",
            "proposed_words": None,
        })
    return {"source_text_sha256": laws["source"]["text_sha256"], "questions": result}


def reuse(core, core_path):
    part = read(core_path.with_name("recorded-part.json"))
    expected = [rr.core_fingerprint(rr.resolve_core("v91")), rr.core_fingerprint(core)]
    assert part["_metadata"]["cores"] == expected
    summary = read(HERE / "rerun-output.json")
    assert len(part["results"]) == summary["distinct_lists"] == 775
    return {"status": "PASS", "action": "reuse; no replay executed", "citizens_changed": False,
            "core_fingerprints_match": True, "part_sha256": hashlib.sha256(core_path.with_name("recorded-part.json").read_bytes()).hexdigest(),
            "counts": summary["counts"], "original_wall_time_s": summary["wall_time_s"],
            "successful_runs_per_core": summary["successful_coordinate_runs_per_core"],
            "same_errors_per_core": summary["same_errors_per_core"], "baseline_computing": 0}


def question_id(sentence):
    return "demo.question." + hashlib.sha256(sentence.encode()).hexdigest()[:12]


@lru_cache(maxsize=1)
def binding_facts():
    """The adopted symbol-to-fact join the real projection also performs."""
    return {b["symbol"]: b["fact_type"]["id"] for b in
            read(probe.CONTENT / "package.core-calculations.v91.json")["input_bindings"]}


def question_index(core):
    result = {}
    for member in read(core.package_path)["members"]:
        if member["role"] != "input-question":
            continue
        slug = member["id"].removeprefix(probe.P)
        for path in (core.content / f"{slug}.{member['version']}.json", core.content / f"{slug}.json"):
            if path.is_file():
                body = read(path)
                if body.get("id") == member["id"] and body.get("version") == member["version"]:
                    sentence = body["question"]
                    row = result.setdefault(question_id(sentence), {"sentence": sentence, "facts": [], "citizens": []})
                    row["facts"].append(body["fact_type"]["id"])
                    row["citizens"].append({"id": body["id"], "version": body["version"]})
                    break
        else:
            raise AssertionError("adopted question file not found: " + member["id"])
    return result


def predicate_value(fact, spoken):
    """Decision 8's explicit convention; this is synthetic case setup."""
    if fact.rsplit(".", 1)[-1].startswith("no-"):
        return {"yes": "no", "no": "yes"}[spoken]
    return spoken


def current_answers(acts, status):
    h = probe.harness()
    if status == "married_filing_separately":
        h._add(acts, "bundle-adoption", {"bundle": read(probe.CONTENT / "core_calculations.bundle.v4.json")})
        acts = h.say(h.renumber(acts), probe.P + "standard-deduction.spouse-separate-condition", False, "l6b.t0b.condition")
    return acts


def complete_ssa(status):
    """An actual zero box-6 member and closure, not its old legacy witness."""
    h = probe.harness()
    fw = probe.load("l6b_t0b_fw", REPO / "tests/test_form_1099_withholding.py")
    acts = h.strip(current_answers(probe.base(status), status), fw.SSA_B6_CLOSURE)
    horizon = "demo.l6b.t0b.ssa6.h1"
    fw._transition(acts, (fw.SSA_B6_FAMILY, "v1"), fw._head(acts, fw.SSA_B6_FAMILY), horizon,
        "demo.l6b.t0b.ssa6.zero", fw.SSA_B6, (("statement", "demo.l6b.ssa.statement"),), 0.0)
    fw._close(acts, fw.SSA_B6_CLOSURE, horizon, "demo.l6b.t0b.ssa6.closed")
    return h.renumber(acts)


def case_grid():
    from itertools import combinations
    h = probe.harness()
    rows = []
    for row in probe.cases():
        rows.append({"id": "p0/" + row["id"], "group": "p0", "acts": row["acts"],
                     "reconfirm": row["vary"] not in {"ssa-open", "no-benefits-open"}})
    # These are exactly the seven P0 computing_neighbours inputs.
    for status in probe.STATUSES:
        stem = status.replace("married_filing_", "")
        for benefits in (False, True):
            acts = current_answers(probe.base(status, benefits=benefits), status)
            key = "computing/" + stem + (".ssa" if benefits else ".no-ssa")
            rows.append({"id": key, "group": "computing", "acts": acts})
            if status == "married_filing_separately" and not benefits:
                rows.append({"id": key + ".living-unanswered", "group": "computing",
                             "acts": h.strip(acts, probe.P + "mfs-lived-apart-all-year")})
        rows.append({"id": "complete/" + stem, "group": "complete", "acts": complete_ssa(status)})
    facts = [probe.P + slug for slug in proto.QUESTIONS]
    for fact in facts:
        status = "married_filing_separately" if fact.endswith("mfs-lived-apart-all-year") else "single"
        for spoken in ("yes", "no"):
            value = predicate_value(fact, spoken)
            acts = h.say(complete_ssa(status), fact, value, "l6b.t0b.words." + fact.removeprefix(probe.P))
            rows.append({"id": "meaning/" + fact.removeprefix(probe.P) + "/" + spoken,
                         "group": "meaning", "acts": acts, "fact": fact,
                         "spoken_answer": spoken, "fact_value": value})
        rows.append({"id": "single-root/" + fact.removeprefix(probe.P), "group": "single-root",
                     "acts": h.strip(complete_ssa(status), fact), "unanswered": [fact]})
    for a, b in combinations(facts, 2):
        status = "married_filing_separately" if any(f.endswith("mfs-lived-apart-all-year") for f in (a, b)) else "single"
        acts = h.strip(h.strip(complete_ssa(status), a), b)
        rows.append({"id": "pair/" + a.removeprefix(probe.P) + "+" + b.removeprefix(probe.P),
                     "group": "pair", "acts": acts, "unanswered": [a, b]})
    assert len(rows) == 253
    return rows


def page_pin(result):
    if result["outcome"] != "success":
        return result
    by_symbol = {}
    symbols = probe.producer_symbols()
    ledger = []
    for row in result["report"]["dispositions"]:
        symbol = row.get("symbol") or symbols.get(row["artifact_id"])
        if symbol:
            by_symbol.setdefault(symbol, []).append(row)
        ledger.append({k: row[k] for k in ("artifact_id", "disposition", "code", "missing", "guard_result", "symbol") if k in row})

    def terminals(name, seen=frozenset()):
        if name in seen:
            return set()
        blocked = [r for r in by_symbol.get(name, []) if r["disposition"] == "blocked"]
        if not blocked:
            return {name}
        return set().union(*(terminals(m, seen | {name}) for r in blocked for m in r.get("missing", [])))

    fields = {}
    for section in result["model"]["sections"]:
        field, resolved = section["field"], section["resolved"]
        fid, symbol = field["id"], field["binds_symbol"]
        assert fid not in fields
        value = resolved.get("value")
        if resolved["disposition"] == "published_categorical":
            value = resolved["act"]["finding"]["value"]
        missing = sorted({m for r in by_symbol.get(symbol, []) if r["disposition"] == "blocked" for m in r.get("missing", [])})
        fields[fid] = {"section_id": section["id"], "disposition": resolved["disposition"],
            "value": value, "codes": resolved.get("activeCodes", []),
            "questions": [question_id(r["sentence"]) for r in resolved.get("reasons", [])],
            "missing": missing, "terminal_missing": sorted(terminals(symbol)) if resolved["disposition"] == "blocked" else [],
            "generic_explain": (field["dispositions"].get("blocked") or {}).get("explain")}
    return {"outcome": "success", "fields": fields, "ledger": ledger, "stop": result["report"].get("stop_reason")}


def capture(core, acts, run_id, reconfirm=True, page=None):
    h = probe.harness()
    with h.loader_entries(core):
        finished = h._handover(h._finish(acts, package_path=core.package_path,
            package_version=core.version, release_path=core.release_path,
            release_version=core.release_version, note=run_id), surface=core.surface(), reconfirm=reconfirm)
        with tempfile.TemporaryDirectory() as folder:
            cap = h.WorkspaceCapability(Path(folder) / "L")
            outcome = h.live_coordinate_run(cap, repo_root=REPO, authoritative_acts=finished,
                workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": h.YEAR},
                scope_user=h.ccr.USER, request={"schema": "run-request.v1"}, run_id=run_id,
                governance_pins=[], surface=core.surface(), output_name="out.json")
            if outcome.refusal:
                return {"outcome": "refused", "reason": outcome.refusal.reason}
            result = {"outcome": "success", "model": read(outcome.presentation_path), "report": read(outcome.output_path)}
            if page:
                page.parent.mkdir(exist_ok=True)
                page.write_bytes(_render_page(REPO, cap, outcome.presentation_path))
    return page_pin(result)


def matrix_run(key, acts, cores):
    import re
    a, b = cores
    reconfirm = not (key.endswith(".ssa-open") or key.endswith(".no-benefits-open"))
    token = hashlib.sha256(key.encode()).hexdigest()[:16]
    output = {}
    for label, core in (("v91", a), ("successor", b)):
        try:
            output[label] = capture(core, acts, "demo.l6b.t0b." + label + "." + token, reconfirm,
                b.content.parent / "track0b-pages" / ("demo." + token + ".html") if label == "successor" else None)
        except Exception as exc:
            output[label] = {"outcome": "error", "error": type(exc).__name__,
                "message": re.sub(r"/(?:Users|private|tmp|var)/\S+", "<path>", str(exc))[:600]}
    return output


def analyse(key, raw, meta, questions):
    a, b = raw["v91"], raw["successor"]
    row = {k: v for k, v in meta.items() if k != "acts"}
    if a["outcome"] != "success" or b["outcome"] != "success":
        return {**row, "classification": "same_admission_refusal" if a == b else "unexpected_outcome_change", "v91": a, "successor": b}
    af, bf = a["fields"], b["fields"]
    # A blocked row may name a package binding symbol rather than a fact id.
    # Normalize all declared aliases, not a special case for one spouse fact.
    bindings = binding_facts()
    for fields in (af, bf):
        for f in fields.values():
            f["terminal_missing"] = sorted({bindings.get(name, name) for name in f["terminal_missing"]})
    changes, gains, violations = [], [], []
    state_changes = []
    for fid in sorted(set(af) | set(bf)):
        before, after = af.get(fid), bf.get(fid)
        if before is None or after is None:
            state_changes.append({"field": fid, "before": before, "after": after})
            continue
        if any(before[k] != after[k] for k in ("disposition", "value", "codes", "missing", "terminal_missing")):
            state_changes.append({"field": fid, "before": before, "after": after})
        if before["questions"] != after["questions"]:
            changes.append({"field": fid, "before": before["questions"], "after": after["questions"]})
        added = sorted(set(after["questions"]) - set(before["questions"]))
        if added:
            certificates = []
            for qid in added:
                facts = questions.get(qid, {}).get("facts", [])
                matching = sorted(set(facts) & set(before["terminal_missing"]))
                ok = before["disposition"] == "blocked" and bool(matching)
                certificate = {"question": qid, "question_facts": facts, "matching_missing_facts": matching, "pass": ok}
                certificates.append(certificate)
                if not ok:
                    violations.append({"field": fid, **certificate})
            gains.append({"field": fid, "v91_disposition": before["disposition"], "v91_value": before["value"],
                "v91_missing": before["missing"], "v91_terminal_missing": before["terminal_missing"],
                "added": certificates})
    row.update({"classification": "state_change" if state_changes or a["ledger"] != b["ledger"] else "questions_only" if changes else "identical",
                "state_changes": state_changes, "ledger_equal": a["ledger"] == b["ledger"],
                "question_changes": changes, "gains": gains, "placement_failures": violations,
                "line6b": {"v91": af[probe.P + "form1040.line-6b"], "successor": bf[probe.P + "form1040.line-6b"]},
                "balances": {"v91": {fid: af.get(probe.P + fid) for fid in ("form1040.line-34", "form1040.line-37")},
                             "successor": {fid: bf.get(probe.P + fid) for fid in ("form1040.line-34", "form1040.line-37")}}})
    if row["group"] == "meaning":
        negative = row["fact"].rsplit(".", 1)[-1].startswith("no-")
        expected = "guard_inapplicable" if negative and row["fact_value"] == "no" else "published_value"
        row["meaning_pass"] = (row["line6b"]["successor"]["disposition"] == expected and
                                row["classification"] == "identical")
    if row["group"] in {"single-root", "pair"}:
        wanted = set(row["unanswered"])
        expected_qids = {qid for qid, q in questions.items() if set(q["facts"]) & wanted}
        all_shown = set().union(*(set(f["questions"]) for f in bf.values()))
        blocked = []
        for fid, f in bf.items():
            if f["disposition"] != "blocked":
                continue
            active = set(f["terminal_missing"]) & wanted
            expected_here = {qid for qid, q in questions.items() if set(q["facts"]) & active}
            blocked.append({"field": fid, "missing": f["missing"], "terminal_missing": f["terminal_missing"],
                "questions": f["questions"], "expected_active_questions": sorted(expected_here),
                "pass": set(f["questions"]) == expected_here and bool(expected_here)})
        row["root_check"] = {"page_shows_all_requested_questions": expected_qids <= all_shown,
            "line6b_shows_all_requested_questions": expected_qids <= set(row["line6b"]["successor"]["questions"]),
            "active_fields_only_expected_questions": all(f["pass"] for f in blocked),
            "blocked_fields": blocked,
            "pass": expected_qids <= set(row["line6b"]["successor"]["questions"]) and all(f["pass"] for f in blocked)}
    return row


DRAW_JS = r'''
import {readFile,writeFile} from "node:fs/promises";
import {join} from "node:path";
const [repo,configFile,output] = process.argv.slice(2);
const {launchChrome} = await import(join(repo,"tools/presentation_harness/lib/chrome.mjs"));
const {startLoopbackServer} = await import(join(repo,"tools/presentation_harness/lib/server.mjs"));
const {CDPClient} = await import(join(repo,"tools/presentation_harness/lib/cdp.mjs"));
const config=JSON.parse(await readFile(configFile,"utf8"));
const server=await startLoopbackServer(config.root,new Set(config.cases.map(c=>c.page)));
let chrome,client;
const cases=[];
try {
 chrome=await launchChrome(null,{});client=await CDPClient.connect(chrome.wsUrl);
 const version=await client.send("Browser.getVersion");
 for(const item of config.cases){
  const {browserContextId}=await client.send("Target.createBrowserContext",{});let targetId,off;
  try {
   ({targetId}=await client.send("Target.createTarget",{url:"about:blank",browserContextId}));
   const {sessionId}=await client.send("Target.attachToTarget",{targetId,flatten:true});
   await client.send("Page.enable",{},sessionId);await client.send("Runtime.enable",{},sessionId);
   await client.send("Fetch.enable",{patterns:[{urlPattern:"*"}]},sessionId);
   off=client.on("Fetch.requestPaused",p=>client.send(p.request.url.startsWith(server.origin)?"Fetch.continueRequest":"Fetch.failRequest",
      p.request.url.startsWith(server.origin)?{requestId:p.requestId}:{requestId:p.requestId,errorReason:"BlockedByClient"},sessionId).catch(()=>{}),sessionId);
   const loaded=client.waitFor("Page.loadEventFired",sessionId,15000);
   await client.send("Page.navigate",{url:server.origin+"/"+item.page},sessionId);await loaded;
   const expression=`(() => new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(()=>{
    const targets=${JSON.stringify(item.targets)};
    const text=n=>(n?.innerText||"").replace(/\\s+/g," ").trim();
    const fields=targets.map(t=>{
      const s=document.getElementById(t.section_id)?.querySelector("section.line");
      if(!s)return {...t,missing_section:true};
      const reasons=Array.from(s.querySelectorAll(".blocked-reasons li")).map(text);
      return {field:t.field,section_id:t.section_id,expected:t.expected,reasons,
       questions_drawn:t.expected.every(q=>reasons.includes(q)),
       generic_explain_drawn:!!t.generic_explain&&s.innerText.includes(t.generic_explain),
       generic_remedy:s.querySelectorAll(".remedy-box").length,
       alerts:Array.from(s.querySelectorAll(".section-error")).map(text)};
    });
    resolve({fields,alerts:Array.from(document.querySelectorAll(".section-error")).map(n=>({id:n.closest("[id]")?.id,text:text(n)}))});
   }))))()`;
   const result=await client.send("Runtime.evaluate",{expression,returnByValue:true,awaitPromise:true},sessionId);
   if(result.exceptionDetails)throw new Error("DOM observation failed");
   cases.push({id:item.id,...result.result.value});
  }finally{off?.();if(targetId)await client.send("Target.closeTarget",{targetId}).catch(()=>{});
    await client.send("Target.disposeBrowserContext",{browserContextId}).catch(()=>{});}
 }
 await writeFile(output,JSON.stringify({browser:version.product,node:process.versions.node,cases},null,2)+"\n");
}finally{client?.close();if(chrome)await chrome.dispose();await server.close();}
'''


def draw(core, rows, raw_results, questions):
    gaining = {g["field"] for r in rows for g in r.get("gains", [])}
    selected = []
    # Required reproduced scope and separate-filing samples, then cover every
    # distinct field which gained a question anywhere in the complete grid.
    for key in ("single-root/ss-benefits-scope.no-form-2555", "single-root/mfs-lived-apart-all-year"):
        selected.append(next(r for r in rows if r["id"] == key))
    covered = {g["field"] for r in selected for g in r.get("gains", [])}
    while gaining - covered:
        choice = max(rows, key=lambda r: len({g["field"] for g in r.get("gains", [])} - covered))
        assert choice not in selected
        selected.append(choice)
        covered.update(g["field"] for g in choice["gains"])
    folder = core.content.parent / "track0b-pages"
    config_cases = []
    for row in selected:
        fields = raw_results[row["id"]]["successor"]["fields"]
        targets = []
        for gain in row["gains"]:
            f = fields[gain["field"]]
            targets.append({"field": gain["field"], "section_id": f["section_id"],
                "expected": [questions[q]["sentence"] for q in f["questions"]], "generic_explain": f["generic_explain"]})
        token = hashlib.sha256(row["id"].encode()).hexdigest()[:16]
        config_cases.append({"id": row["id"], "page": "demo." + token + ".html", "targets": targets})
    config, script, output = folder / "config.json", folder / "observe.mjs", folder / "drawn.json"
    config.write_text(json.dumps({"root": str(folder), "cases": config_cases}))
    script.write_text(DRAW_JS)
    subprocess.run(["node", str(script), str(REPO), str(config), str(output)], check=True, timeout=240)
    result = read(output)
    parked = {"line-6c", "line-sch1-top"}
    result["gaining_fields"] = sorted(gaining)
    result["covered_fields"] = sorted(covered)
    result["failures"] = [{"case": c["id"], **f} for c in result["cases"] for f in c["fields"]
        if f.get("missing_section") or not f["questions_drawn"] or f["generic_explain_drawn"] or f["generic_remedy"] or f["alerts"]]
    result["unexpected_alerts"] = [{"case": c["id"], **a} for c in result["cases"] for a in c["alerts"] if a["id"] not in parked]
    result["pass"] = not result["failures"] and not result["unexpected_alerts"] and covered == gaining
    return result


def main():
    from collections import Counter
    import os
    import time
    parser = argparse.ArgumentParser()
    parser.add_argument("core", type=Path)
    parser.add_argument("--instructions", required=True, type=Path)
    parser.add_argument("--summarize-only", action="store_true")
    args = parser.parse_args()
    core = rr.resolve_core(args.core)
    data = catalog(core, args.instructions)
    questions = question_index(core)
    examples = [row for row in questions.values() if any(c["id"].endswith(s) for c in row["citizens"] for s in (
        "ss-benefits-scope-no-lump-sum-election", "sli-scope-no-form-2555", "schedule1-adjustments-scope-no-line11-educator", "exception1-no-capital-losses"))]
    data["decision"] = "Decision 8: display only; synthetic facts are set by the published positive-question or assertion-question convention, not through an entry path."
    data["published_sibling_examples"] = examples
    data["proposed_question_words"] = {}
    probe.write_json(HERE / "track0-questions.json", data)
    probe.write_json(HERE / "track0-replay.json", reuse(core, args.core))
    grid = case_grid()
    meta = {row["id"]: row for row in grid}
    from tests import evidence_loader
    owner = evidence_loader.current_owner()
    if owner:
        evidence_loader.release(owner)
    part = args.core.parent / "track0b-part.json"
    clock = args.core.parent / "track0b-wall.json"
    spent = read(clock) if clock.is_file() else []
    workers = max(1, (os.cpu_count() or 2) - 1)
    if args.summarize_only:
        raw_results = read(part)["results"]
    else:
        start = time.monotonic()
        try:
            raw_results = rr.replay([(r["id"], r["acts"]) for r in grid],
                (rr.resolve_core("v91"), core), matrix_run, workers=workers, part=part)
        finally:
            spent.append(round(time.monotonic() - start, 3))
            clock.write_text(json.dumps(spent) + "\n")
    rows = [analyse(key, raw, meta[key], questions) for key, raw in sorted(raw_results.items())]
    matrix = {"workers": workers, "cases": len(rows), "live_attempts": 2*len(rows), "wall_time_s": round(sum(spent), 3),
        "counts": dict(Counter(r["classification"] for r in rows)), "input_binding_aliases": binding_facts(),
        "questions": questions, "results": rows}
    probe.write_json(HERE / "track0-matrix.json", matrix)
    roots = [r for r in rows if r["group"] in {"single-root", "pair"}]
    probe.write_json(HERE / "track0-roots.json", {"cases": len(roots), "results": [
        {"id": r["id"], "unanswered": r["unanswered"], **r.get("root_check", {"pass": False})} for r in roots]})
    meaning = [r for r in rows if r["group"] == "meaning"]
    probe.write_json(HERE / "track0-meaning.json", {"convention": data["decision"], "results": [
        {k: r.get(k) for k in ("id", "fact", "spoken_answer", "fact_value", "line6b", "meaning_pass")} for r in meaning]})
    if args.summarize_only and (HERE / "track0-drawn.json").is_file():
        drawn = read(HERE / "track0-drawn.json")
        assert set(drawn["covered_fields"]) == {g["field"] for r in rows for g in r.get("gains", [])}
    else:
        drawn = draw(core, rows, raw_results, questions)
        probe.write_json(HERE / "track0-drawn.json", drawn)
    print(json.dumps({"counts": matrix["counts"], "wall_time_s": matrix["wall_time_s"],
        "placement_failures": sum(len(r.get("placement_failures", [])) for r in rows),
        "meaning_passes": sum(r.get("meaning_pass", False) for r in meaning),
        "root_passes": sum(r.get("root_check", {}).get("pass", False) for r in roots),
        "drawn_pass": drawn["pass"]}, indent=2))


if __name__ == "__main__":
    main()
