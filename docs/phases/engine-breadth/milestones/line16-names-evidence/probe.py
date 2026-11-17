"""P0 live evidence. Run: python3 probe.py [scratch-core.json].

All sentences come from the real page model, without punctuation filtering.
Sibling harnesses are loaded by path into this evidence owner's namespace.
"""
from __future__ import annotations

import copy
import json
import multiprocessing
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from tests import evidence_loader

OWNER = "line16_names_p0"
P = "tax.us.2025."
MILESTONES = HERE.parent
BNQ = MILESTONES / "blocked-names-question-evidence"
PBR = MILESTONES / "preferential-base-reason-evidence"
# Existing BNQ harnesses have legacy bare imports; the owner loader isolates
# those imports. This script's own imports always use an explicit path.
sys.path.insert(0, str(BNQ))
FOUR = ["f1099b.noncovered-sold.source-closure", "f8949.no1099b-sold.source-closure",
        "schedule-d-boundary.no-form8949-sources", "schedule-d-boundary.no-other-form8949-adjustments"]
EXC = ["exception1.only-box2a-capital-gains", "exception1.no-capital-losses",
       "exception1.no-qof-deferral", "exception1.no-boxes-2b-2c-2d"]
WATCH = {"form1040.line-16", "form1040.line-20", "schedule3.line-1", "schedule3.line-8",
         "form.sch8812.worksheet-a.line-5"}


def load(path, name):
    evidence_loader.activate(OWNER)
    return evidence_loader.load(path, "l16_" + name)


def write(name, body):
    text = json.dumps(body, indent=2) + "\n"
    for root in ("Users", "private", "tmp", "var"):
        assert "/" + root + "/" not in text, "local path in evidence"
    (HERE / name).write_text(text)


def compact(result):
    groups = {}
    for field, detail in result["fields"].items():
        key = json.dumps(detail, sort_keys=True)
        groups.setdefault(key, {"fields": [], **detail})["fields"].append(field)
    return {"field_groups": list(groups.values()),
            "rows": [r for r in result["rows"] if r["disposition"] == "blocked"
                     or r["artifact"] in ("selected-preferential-base", "schedule-d-required.conclusion", "form1040-line16")],
            "publications": {k: v for k, v in result["publications"].items()
                             if k in ("tax.total-tax", "schedule-d-required.conclusion", "capital-gains.selected-preferential-base")}}


def expand(result):
    return {"fields": {name: {k: v for k, v in group.items() if k != "fields"}
                       for group in result["field_groups"] for name in group["fields"]},
            "rows": result["rows"], "publications": result["publications"]}


def pack_cases(cases):
    """Share repeated complete states, retaining every field and sentence."""
    field_states, row_states = [], []
    field_ids, row_ids = {}, {}

    def intern(value, states, ids):
        key = json.dumps(value, sort_keys=True)
        if key not in ids:
            ids[key] = len(states)
            states.append(value)
        return ids[key]

    packed = {}
    for key, result in cases.items():
        result = expand(result)
        packed[key] = {
            "fields": {name: intern(value, field_states, field_ids) for name, value in result["fields"].items()},
            "rows": [intern(row, row_states, row_ids) for row in result["rows"]],
            "publications": result["publications"],
        }
    return {"storage": "shared-state-tables-v1", "field_states": field_states,
            "row_states": row_states, "cases": packed}


def read_cases(path):
    body = json.loads(path.read_text())
    if body.get("storage") != "shared-state-tables-v1":
        return body["cases"]
    return {key: compact({"fields": {name: body["field_states"][index] for name, index in row["fields"].items()},
                          "rows": [body["row_states"][i] for i in row["rows"]],
                          "publications": row["publications"]}) for key, row in body["cases"].items()}


def short(name):
    return str(name).removeprefix(P + "rule.").removeprefix(P)


def summarize(core, outcome):
    assert outcome.refusal is None, str(outcome.refusal)
    report = json.loads(outcome.output_path.read_text())
    page = json.loads(outcome.presentation_path.read_text())
    common = load(BNQ / "common.py", "common")
    publishes = common.rule_publishes(core)
    rows = [{"artifact": short(r.get("artifact_id")),
             "symbol": short(r.get("symbol") or publishes.get(r.get("artifact_id"))),
             "disposition": r.get("disposition"), "code": r.get("code"),
             "missing": [short(n) for n in r.get("missing") or []]}
            for r in report["dispositions"]]
    fields = {}
    for section in page["sections"]:
        field, resolved = section.get("field") or {}, section.get("resolved") or {}
        name = short(field.get("id"))
        if "blocked" not in str(resolved.get("disposition")) and name not in WATCH:
            continue
        own = [r for r in rows if r["symbol"] == short(field.get("binds_symbol"))]
        assert len(own) <= 1, name
        fields[name] = {"disposition": resolved.get("disposition"), "value": resolved.get("value"),
                        "row": own[0] if own else None,
                        "reasons": resolved.get("reasons") or []}
    return {"fields": fields, "rows": rows,
            "publications": {short(p.finding.get("symbol")): p.finding.get("value")
                             for p in outcome.publications or ()}}


def lists():
    common = load(BNQ / "common.py", "common")
    bnq = load(BNQ / "probe.py", "bnq_probe")
    pbr = load(PBR / "probe.py", "pbr_probe")
    cases = [(key, acts) for key, acts in pbr.build_lists()
             if not key.startswith("internal-subtotal/")]
    # build_lists temporarily activates its own owner; restore this one.
    evidence_loader.activate(OWNER)
    common = load(BNQ / "common.py", "common")
    bnq = load(BNQ / "probe.py", "bnq_probe")
    h = common.harness()
    for status in ("single", "married_filing_jointly", "married_filing_separately"):
        for required in (False, True):
            acts = bnq.empty(exc1_only_2a="no" if required else "yes")
            acts = h.say(acts, P + "filing-status", status, "l16-status")
            cases.append(("status/" + status + ("/required" if required else "/exception-yes"), acts))
    personal = bnq.personal_loss_8949()
    for name in FOUR + EXC:
        for value in ("yes", "no"):
            cases.append(("protected/" + name + "/" + value,
                          h.say(copy.deepcopy(personal), P + name, value, "l16-one-answer")))
    cumulative = copy.deepcopy(personal)
    for name in EXC:
        cumulative = h.say(cumulative, P + name, "yes", "l16-" + name)
        cases.append(("protected/cumulative/" + name, copy.deepcopy(cumulative)))
    # No change to the original ten builders; separately include a represented sale.
    cases.append(("neighbour/recorded-sale", bnq.sale("no1099b")))
    # Explicit synthetic age/blindness answers make the sale/no-Schedule-D
    # neighbours computing returns rather than unrelated age-question blocks.
    prepared = []
    for key, acts in cases:
        status = [a.get("payload", {}).get("finding", {}).get("value") for a in acts
                  if a.get("payload", {}).get("finding", {}).get("fact_id", "").startswith(P + "filing-status|")][-1]
        facts = {a.get("payload", {}).get("finding", {}).get("fact_id", "").split("|", 1)[0]
                 for a in acts}
        age_facts = ["taxpayer-over-65", "taxpayer-blind"]
        if status in ("married_filing_jointly", "married_filing_separately"):
            age_facts += ["spouse-over-65", "spouse-blind"]
        for fact in age_facts:
            if P + fact not in facts:
                acts = h.say(acts, P + fact, False, "l16-" + fact)
        if status == "married_filing_separately":
            h._add(acts, "bundle-adoption", {"bundle": json.loads(
                (h.CONTENT / "core_calculations.bundle.v4.json").read_text())})
            acts = h.say(acts, P + "standard-deduction.spouse-separate-condition", False, "l16-separate")
        prepared.append((key, acts))
    evidence_loader.finish_all()
    return prepared


def worker(args):
    core_json, shard = args
    common = load(BNQ / "common.py", "common")
    common.summarize = summarize
    core = common.scratch(Path(core_json)) if core_json else common.harness().Core("v94", "v92", "v92")
    h = common.harness()
    output = []
    for key, acts in shard:
        result = common.run(core, acts, "demo.l16.p0." + key.replace("/", "."))
        assert "fields" in result, (key, result)
        output.append((key, result))
    evidence_loader.finish_all()
    return output


def main():
    cases = lists()
    workers = max(1, (os.cpu_count() or 2) - 1)
    core = sys.argv[1] if len(sys.argv) == 2 else None
    with multiprocessing.get_context("spawn").Pool(workers) as pool:
        parts = pool.map(worker, [(core, cases[i::workers]) for i in range(workers) if cases[i::workers]])
    found = dict(pair for part in parts for pair in part)
    write("candidate.json" if core else "baseline.json", {"core": "scratch-v95" if core else "v94",
          **pack_cases({key: compact(value) for key, value in sorted(found.items())})})
    print(json.dumps({"cases": len(found), "core": "scratch-v95" if core else "v94"}))


if __name__ == "__main__":
    main()
