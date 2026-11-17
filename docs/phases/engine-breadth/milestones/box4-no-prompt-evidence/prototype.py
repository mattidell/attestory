"""Build a content-only scratch core v94 from published core v93.

The scratch directory must be outside this repository. No production writes.
Eight sale-subject count rules feed eight requirement rules (1 or 0); a
return-level count bypasses the original pairing only when all sales are satisfied.
"""
from __future__ import annotations
import argparse
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from tools.package_successor import generate_to_directory
P = "tax.us.2025."
CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
STEM = "demo.release.sli-worksheet-integration.2025"
AMOUNT = P + "f1099b.statement-box4-withholding"
REPORTED = P + "f1099b.statement-box4-withholding-reported"
GUARD = P + "f1099b.box4-amounts-ready"

def ref(name):
    return {"op": "ref", "name": name}

def count(name):
    return {"op": "shared_key_count", "fact_type": name, "key": "statement"}

def compare(left, cmp, right):
    return {"op": "compare", "left": left, "cmp": cmp, "right": right}

def choose(when, then, otherwise):
    return {"op": "choose", "when": when, "then": then, "else": otherwise}

def pin(body, role):
    return {"id": body["id"], "version": body["version"], "schema": body["schema"], "role": role}

def artifacts():
    line = json.loads((CONTENT / "rule.form1040-line25b.v8.json").read_text())
    oldpair = line["when"]["args"][1]
    sales = oldpair["income"]
    rules, facts = [], []
    for sale in sales:
        symbol = sale + ".box4-amount-needed"
        # Reuse the actual subject vocabulary's complete identity keys.
        matches = []
        for path in CONTENT.glob("*.bundle*.json"):
            body = json.loads(path.read_text())
            matches.extend(f for f in body.get("fact_types", []) if f["id"] == sale and f["version"] == "v1")
        assert matches
        facts.append({"schema": "fact-type.v2", "id": symbol, "version": "v1",
                      "title": "Whether this sale's statement still needs a box 4 amount (1 or 0)",
                      "nature": "determinable", "identity_keys": matches[0]["identity_keys"],
                      "value_schema": {"type": "number", "enum": [0, 1]},
                      "supersession": {"policy": "free"}})
        count_symbol = sale + ".box4-amount-count"
        count_fact = copy.deepcopy(facts[-1])
        count_fact.update(id=count_symbol, title="Number of box 4 amounts on this sale's statement")
        count_fact["value_schema"] = {"type":"number", "minimum":0}
        facts.append(count_fact)
        rules.append({"schema":"rule-artifact.v17", "id":P+"rule."+count_symbol.removeprefix(P),
                      "version":"v1", "scope":line["scope"], "role":"computation",
                      "subject":{"id":sale,"version":"v1"}, "requires":[sale], "pins":[], "when":True,
                      "value":count(AMOUNT), "publishes":count_symbol,
                      "blocked":{"code":"DEPENDENCY_ABSENT","missing":[]}, "citations":line["citations"],
                      "notes":"Scratch: count existing box 4 rows by statement, without reading amounts."})
        is_no = {"op":"collect_categorical_all_equal", "name":REPORTED,
                 "value":{"op":"category_literal", "fact_type":{"id":REPORTED,"version":"v1"},"value":"no"}}
        rules.append({"schema":"rule-artifact.v17", "id":P+"rule."+symbol.removeprefix(P),
                      "version":"v1", "scope":line["scope"], "role":"computation",
                      "subject":{"id":sale,"version":"v1"}, "requires":[sale,count_symbol], "pins":[], "when":True,
                      "joined":{"id":REPORTED,"version":"v1"}, "direction":"subject_contains_joined",
                      "value":choose(compare(ref(count_symbol),"gt",0),0,
                          choose(compare(count(REPORTED),"eq",0),1,choose(is_no,0,1))),
                      "publishes":symbol, "blocked":{"code":"DEPENDENCY_ABSENT","missing":[]},
                      "citations":line["citations"],
                      "notes":"Scratch: explicit amount wins. Without an amount, only this statement's no satisfies the amount requirement. 1 means amount needed; 0 does not publish an amount."})
    facts.append({"schema": "fact-type.v2", "id": GUARD, "version": "v1",
                  "title": "Number of recorded sales whose statement still needs a box 4 amount",
                  "nature": "determinable", "identity_keys": [{"name":"tax-year", "kind":"literal", "values":["2025"]}],
                  "value_schema": {"type":"number", "minimum":0}, "supersession": {"policy":"free"}})
    bundle = {"schema":"bundle.v2", "id":P+"f1099b.box4-amount-requirement.vocabulary", "version":"v1",
              "label":"Scratch box 4 amount requirement by sale", "fact_types":facts}
    checks = [r for r in rules if r["publishes"].endswith(".box4-amount-needed")]
    declarations = [{"symbol":r["publishes"], "subject":r["subject"]} for r in checks]
    needed_total = {"op":"add", "args":[{"op":"collect", "name":r["publishes"], "source_set":r["subject"]["id"].removesuffix("-txn")} for r in checks]}
    branch = {"id":"sales", "activity":{"kind":"source_nonempty", "member_fact_types":[{"id":s,"version":"v1"} for s in sales]},
              "reads_subject_results": declarations, "requires":[], "pins":[], "when":True,
              "value":needed_total}
    guard = {"schema":"rule-artifact.v17", "id":P+"rule.f1099b-box4-amounts-ready", "version":"v1",
             "scope":line["scope"], "role":"computation", "requires":[], "pins":[], "when":True,
             "selection":{"mode":"exclusive_presence", "conflict":"refuse", "paths":[branch],
                          "default":{"id":"neither", "reads_subject_results":[], "requires":[], "pins":[], "when":True, "value":0},
                          "refusal":{"code":"DEPENDENCY_INVALID", "missing":["f1099b.box4-amounts-ready-conflict"], "pins":[]}},
             "publishes":GUARD, "blocked":{"code":"DEPENDENCY_ABSENT", "missing":[]},
             "citations":line["citations"], "notes":"Scratch: count sales whose statement still needs an amount. Line 25b keeps the published amount missing name and refusal code."}
    line["version"] = "v9"
    line["schema"] = "rule-artifact.v17"
    line["when"]["args"][1] = choose(compare(ref(GUARD), "eq", 0), True, oldpair)
    line["requires"].append(GUARD)
    line["pins"].append({"id":guard["id"], "version":"v1", "origin":"assertion", "role":"input"})
    line["notes"] += " Scratch v9: replace amount-only pairing with a per-sale guard that accepts this statement's no when its amount is absent. Explicit amounts and all subtotal and return-level arithmetic are unchanged."
    return [("f1099b-box4-amount-requirement.bundle.json", bundle, "fact-type-bundle"),
            *[(r["id"].removeprefix(P)+".json",r,"computation") for r in rules],
            ("rule.f1099b-box4-amounts-ready.json",guard,"computation"),
            ("rule.form1040-line25b.v9.json",line,"computation")]

def build(scratch):
    scratch.mkdir(parents=True, exist_ok=False)
    content, releases = scratch/"content", scratch/"releases"
    shutil.copytree(CONTENT, content)
    shutil.copytree(RELEASES, releases)
    package = json.loads((content/"package.core-calculations.v93.json").read_text())
    old = next(m for m in package["members"] if m["id"] == P+"rule.form1040-line25b")
    changes, entries, bodies = [], [], artifacts()
    for filename, body, role in bodies:
        (content/filename).write_text(json.dumps(body,indent=2)+"\n")
        new = pin(body, role)
        changes.append({"op":"replace", "old":old, "new":new} if body["id"] == old["id"] else {"op":"add", "new":new})
        entry = {"id":body["id"], "version":body["version"]}
        old_entry = {"id":old["id"], "version":old["version"]}
        if role == "fact-type-bundle":
            entries.append({"op":"add", "value":entry})
        if body["id"] == old["id"] and old_entry in package["entrypoints"]:
            entries.append({"op":"replace", "old":old_entry, "new":entry})
    config = {"package_version":"v94", "release_version":"v92", "members":changes,
              "entrypoints":entries, "registry_sort":"id_version", "registry_new_key_order":["checksum","id","version"]}
    (scratch/"changes.json").write_text(json.dumps(config,indent=2)+"\n")
    result = generate_to_directory(content/"package.core-calculations.v93.json", content/"published-packages.v91.json",
                                   releases/f"{STEM}.v91.json", content, scratch/"changes.json", scratch/"out")
    for src,dest in (("package.json",content/"package.core-calculations.v94.json"),
                     ("registry.json",content/"published-packages.v92.json"),("release.json",releases/f"{STEM}.v92.json")):
        shutil.copyfile(scratch/"out"/src,dest)
    (scratch/"core.json").write_text(json.dumps({"version":"v94", "registry":"v92", "release_version":"v92",
                 "content":str(content), "releases":str(releases), "loader_from":"v93"},indent=2)+"\n")
    return {"baseline":"core v93 / registry v91 / release v91", "scratch":"core v94 / registry v92 / release v92",
            "artifacts":[{"filename":n,**pin(b,r)} for n,b,r in bodies],
            "inherited_inconsistencies":[list(r) for r in result.get("inherited_inconsistencies",[])]}

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("scratch",type=Path)
    args=parser.parse_args()
    scratch=args.scratch.resolve()
    if scratch==REPO or REPO in scratch.parents:
        raise SystemExit("scratch must be outside the repository")
    result=build(scratch)
    spec=importlib.util.spec_from_file_location("b4n_prototype_writer",HERE/"probe.py")
    module=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=module
    spec.loader.exec_module(module)
    module.write(HERE/"prototype-build.json",result)
    print(json.dumps(result,indent=2))
