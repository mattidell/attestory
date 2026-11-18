"""Strict whole-row, whole-model comparison with an explicit prose allowlist.

Admission checks run before expected labels. Only adopted-version metadata,
deterministic generated finding/publication-act/graph identifiers, unordered
pin/edge sets and keyed mortgage box-observation records are canonicalized.
The observation-order premise is proved on v95 in p0c-order-check.json.
No value, disposition, code, missing name, reason,
question identity or unplanned text is removed from comparison.
"""
from __future__ import annotations
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def exact(a, b):
    return json.dumps(a, sort_keys=True, separators=(",", ":")) == json.dumps(b, sort_keys=True, separators=(",", ":"))

def encoded(value): return json.dumps(value, sort_keys=True, separators=(",", ":"))

def read_pin(root, row):
    pin = json.loads((root / row["pin"]).read_text()) if "pin" in row else row
    model = json.loads((root / row["model"]).read_text()) if row.get("outcome") == "success" else None
    return pin, model

def versions():
    rows = json.loads((HERE / "p0c-validation.json").read_text())["successors"]
    mapping = {r["id"]: (r["old_version"], r["new_version"]) for r in rows}
    mapping["tax.us.2025.package.core-calculations"] = ("v95", "v96")
    for row in json.loads((HERE / "repair-validation.json").read_text())["successors"]:
        mapping[row["id"]] = (row["old_version"], row["new_version"])
    return mapping

def reference_versions(node, mapping):
    if not isinstance(node, dict): return node
    node = dict(node)
    for ident, ver in (("id", "version"), ("pinId", "pinVersion")):
        pair = mapping.get(node.get(ident))
        if pair and node.get(ver) == pair[1]: node[ver] = pair[0]
    return node

def aliases(pin, model, mapping):
    nodes = model.get("explanationGraph", {}).get("nodes", {})
    memo, active, rename = {}, set(), {}
    def shape(key):
        if key in memo: return memo[key]
        assert key not in active, "cyclic graph"
        active.add(key)
        node = reference_versions(nodes[key], mapping)
        if node["kind"] != "derived":
            result = node["id"]
        else:
            value = {k:v for k,v in node.items() if k not in ("id", "edges")}
            if isinstance(value.get("produced_by"), dict): value["produced_by"] = reference_versions(value["produced_by"], mapping)
            edges = []
            for edge in node["edges"]:
                target = nodes[edge["target"]]
                edge_pin = reference_versions(edge["pin"], mapping)
                if edge_pin.get("id") == target["id"]: edge_pin["id"] = shape(edge["target"])
                edges.append({**edge, "pin": edge_pin, "target": shape(edge["target"])})
            value["edges"] = sorted(edges, key=encoded)
            result = "demo.p0c.derived." + hashlib.sha256(encoded(value).encode()).hexdigest()
        memo[key] = result; active.remove(key)
        return result
    for key, node in nodes.items():
        ident = shape(key)
        normalized = reference_versions(node, mapping)
        rename[key] = node["kind"] + ":" + ident + "@" + str(normalized.get("version"))
        if node["kind"] == "derived": rename[node["id"]] = ident
    # Rows for computations outside the section graph still retain their
    # complete payload; only their generated result ID gets a stable label.
    for row in pin["rows"]:
        ident = row.get("finding_id")
        if ident and ident not in rename:
            rename[ident] = "demo.p0c.row." + encoded([row.get("artifact_id"), row.get("symbol")])
        if ident and row.get("act_id"):
            rename[row["act_id"]] = "demo.p0c.publication-act." + rename[ident]
    return rename

def canonical(node, mapping, rename, path=()):
    if isinstance(node, str): return rename.get(node, node)
    if isinstance(node, list):
        values = [canonical(v, mapping, rename, path) for v in node]
        return sorted(values, key=encoded) if path and path[-1] in ("pins", "edges", "boxObservations") else values
    if isinstance(node, dict):
        node = reference_versions(node, mapping)
        result = {}
        for key, value in node.items():
            normalized_key = rename.get(key, key)
            assert normalized_key not in result, "canonical graph-key collision"
            result[normalized_key] = canonical(value, mapping, rename, (*path, key))
        return result
    return node

def expected_model(model):
    result = copy.deepcopy(model)
    replacements = json.loads((HERE / "p0c-wording.json").read_text())["replacements"]
    replacements += json.loads((HERE / "repair-wording.json").read_text())["replacements"]
    by_id = {}
    for row in replacements: by_id.setdefault(row["id"], []).append(row)
    def visit(node):
        if isinstance(node, list):
            for value in node: visit(value)
        elif isinstance(node, dict):
            for row in by_id.get(node.get("id"), []):
                keys = row["property"].split("."); parent = node
                for key in keys[:-1]:
                    parent = parent.get(key) if isinstance(parent, dict) else None
                if isinstance(parent, dict) and parent.get(keys[-1]) == row["old"]:
                    parent[keys[-1]] = row["new"]
                # Attachment projection deliberately copies only this prefix.
                elif row["property"] == "title" and node.get("title") == row["shown"]:
                    node["title"] = row["new_shown"]
            for value in node.values(): visit(value)
    visit(result)
    return result

def row_key(row): return encoded([row.get("artifact_id"), row.get("symbol")])

def semantic_rows(rows):
    return sorted(([row_key(r), r.get("disposition"), r.get("code"), r.get("missing", []), r.get("guard_result")]
                  for r in rows), key=encoded)

def classify(a, am, b, bm):
    if a.get("outcome") != b.get("outcome"): return {"class": "unexpected", "gate": "outcome"}
    if a.get("outcome") != "success":
        return {"class": ("same_error" if a.get("outcome") == "error" else "same_refusal") if exact(a,b) else "unexpected", "gate": "non-success equality"}
    # Universal integrity gates precede all contextual expected labels.
    if Counter(row_key(r) for r in a["rows"]) != Counter(row_key(r) for r in b["rows"]): return {"class":"unexpected", "gate":"added/removed row"}
    if not exact(semantic_rows(a["rows"]), semantic_rows(b["rows"])): return {"class":"unexpected", "gate":"disposition/code/missing/guard"}
    if not exact(sorted(a["values"], key=encoded), sorted(b["values"], key=encoded)): return {"class":"unexpected", "gate":"publication value or symbol"}
    if not exact(a["stop"], b["stop"]): return {"class":"unexpected", "gate":"stop"}
    af, bf = am["sections"], bm["sections"]
    if [(s["id"], s["field"]["id"]) for s in af] != [(s["id"], s["field"]["id"]) for s in bf]: return {"class":"unexpected", "gate":"added/removed page field"}
    for left, right in zip(af, bf):
        for prop in ("value", "disposition", "activeCodes", "reasons"):
            if (prop in left["resolved"]) != (prop in right["resolved"]) or not exact(left["resolved"].get(prop),right["resolved"].get(prop)):
                return {"class":"unexpected", "gate":"page value/disposition/code/reason/question", "field":left["field"]["id"], "property":prop}
    mapping = versions(); ar = aliases(a, am, mapping); br = aliases(b, bm, mapping)
    arows = sorted([canonical(r, mapping, ar) for r in a["rows"]], key=encoded)
    brows = sorted([canonical(r, mapping, br) for r in b["rows"]], key=encoded)
    if not exact(arows, brows): return {"class":"unexpected", "gate":"whole row", "diff":differences(arows,brows)[:6]}
    actual_base = canonical(am, mapping, ar)
    actual_next = canonical(bm, mapping, br)
    expected = canonical(expected_model(am), mapping, ar)
    if not exact(expected, actual_next): return {"class":"unexpected", "gate":"whole model allowlist", "diff":differences(expected,actual_next)[:8]}
    return {"class":"expected_sentences" if not exact(actual_base, actual_next) else "identical_success",
            "rows_compared":len(a["rows"]), "fields_compared":len(af),
            "model_sha256":hashlib.sha256(encoded(actual_next).encode()).hexdigest()}

def differences(a, b, path=""):
    if exact(a,b): return []
    if isinstance(a,dict) and isinstance(b,dict):
        result=[]
        for key in sorted(a.keys()|b.keys()):
            if key not in a or key not in b: result.append(path+"."+key+" (added/removed)")
            else: result.extend(differences(a[key],b[key],path+"."+key))
            if len(result)>=10: break
        return result
    if isinstance(a,list) and isinstance(b,list) and len(a)==len(b):
        result=[]
        for i,(left,right) in enumerate(zip(a,b)):
            result.extend(differences(left,right,path+f"[{i}]"))
            if len(result)>=10: break
        return result
    return [path]
