"""Census on published v96 and strict replay against the scratch successor.

Run: python3 srp_replay.py <scratch-core.json> <results-outside-repo> [--keys k1,k2] [--classify-only]

Each worker runs one list on published v96 and on the scratch core through
live_coordinate_run, the real presentation projection and the production
saved-page renderer (plain-line-texts census.per_list), then classifies the
pair with plain-line-texts p0c_compare. Its two version-dependent helpers are
replaced in memory: versions() maps the declared successors, and
expected_model() replaces a declared old reason only where a page draws a
reason sentence. Siblings are loaded by path under unique names.
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
PLT = HERE.parent / "plain-line-texts-evidence"
sys.path.insert(0, str(REPO))


def load(name, path):
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec); sys.modules[name] = module; spec.loader.exec_module(module)
    return sys.modules[name]


census = load("srp_plt_census", PLT / "census.py")
compare = load("srp_plt_compare", PLT / "p0c_compare.py")
rr = census.rr
WORDING = json.loads((HERE / "wording.json").read_text())["replacements"]
OLD_TO_NEW = {r["old"]: r["new"] for r in WORDING}
CODES = ("HOLDING_PERIOD_MISMATCH", "ADJUSTMENT_EXCEEDS_LOSS")


def versions():
    build = json.loads((HERE / "build.json").read_text())
    mapping = {r["id"]: (r["old_version"], r["new_version"]) for r in build["successors"]}
    mapping["tax.us.2025.package.core-calculations"] = ("v96", "v97")
    return mapping


def expected_model(model):
    result = copy.deepcopy(model)
    for section in result.get("sections") or []:
        for reason in (section.get("resolved") or {}).get("reasons") or []:
            if reason.get("sentence") in OLD_TO_NEW:
                reason["sentence"] = OLD_TO_NEW[reason["sentence"]]
    return result


compare.versions = versions
compare.expected_model = expected_model


def classify(a, am, b, bm):
    """p0c classify, with the page-reason gate read against the expected v96 model.

    p0c compares page reasons exactly before any allowlist; here the declared
    reason sentences are the planned change, so the gates see the v96 model
    with only those sentences replaced. Every other reason property, row,
    value and field is still compared before the label.
    """
    if am is None or bm is None: return compare.classify(a, am, b, bm)
    expected = expected_model(am)
    verdict = compare.classify(a, expected, b, bm)
    if verdict["class"] == "identical_success" and not compare.exact(expected, am):
        verdict["class"] = "expected_sentences"
    return verdict


def other_texts():
    """Every other prose string in the eight wording citizens (titles, claims, meanings)."""
    out = {}
    for row in WORDING:
        body = json.loads((REPO / row["file"]).read_text())
        out.setdefault(body["title"], []).append(f'{body["id"]}@{body["version"]} title')
        out.setdefault(body["closure_claim"], []).append(f'{body["id"]}@{body["version"]} closure_claim')
        for i, c in enumerate(body["member_constraints"]):
            if c["meaning"] not in OLD_TO_NEW:
                out.setdefault(c["meaning"], []).append(f'{body["id"]}@{body["version"]} member_constraints.{i}.meaning ({c["block_code"]})')
    return out


OTHER = other_texts()


def scan(model, texts):
    """Where in a model each text appears as a whole string: section/field and JSON path."""
    hits = []
    def walk(node, path, section):
        if isinstance(node, dict):
            for k, v in node.items(): walk(v, path + (k,), section)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path + (i,), (v.get("field") or {}).get("id") if path == ("sections",) and isinstance(v, dict) else section)
        elif isinstance(node, str) and node in texts:
            hits.append({"text": node, "field": section, "path": ".".join(str(p) if isinstance(p, str) else "[]" for p in path)})
    walk(model, (), None)
    return hits


def trace_rows(rows):
    """Rows naming either block code, and the adjustment subtotal rows' state."""
    named = [{k: r.get(k) for k in ("artifact_id", "symbol", "disposition", "code", "missing")}
             for r in rows if r.get("code") in CODES or any(str(m) in CODES for m in r.get("missing") or [])]
    adjustment = [{k: r.get(k) for k in ("artifact_id", "symbol", "disposition", "code", "missing")}
                  for r in rows if "adjustment-subtotal" in str(r.get("artifact_id")) or str(r.get("symbol", "")).endswith("adjustment-subtotal")]
    return named, adjustment


def per_list(key, acts, cores):
    rr._get_harness()
    root = Path(os.environ["SRP_RESULTS"])
    out = {}
    for side, core in zip(("v96", "next"), cores):
        os.environ["PLT_CENSUS_SCRATCH"] = str(root / side)
        out[side] = census.per_list(key, acts, core)
    a, am = compare.read_pin(root / "v96", out["v96"])
    b, bm = compare.read_pin(root / "next", out["next"])
    verdict = classify(a, am, b, bm)
    record = {"class": verdict["class"], "comparison": verdict, "v96": out["v96"], "next": out["next"],
              "input_sha256": hashlib.sha256(compare.encoded(acts).encode()).hexdigest()}
    if am is not None:
        record["census"] = {"reasons": scan(am, OLD_TO_NEW), "other": scan(am, OTHER)}
        named, adjustment = trace_rows(a["rows"])
        record["trace"] = {"named_rows": named, "adjustment_rows": adjustment}
    if bm is not None:
        record["next_census"] = {"new": scan(bm, set(OLD_TO_NEW.values())), "old": scan(bm, OLD_TO_NEW)}
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("core", type=Path); parser.add_argument("results", type=Path)
    parser.add_argument("--keys", default=None); parser.add_argument("--synthetic", action="store_true")
    parser.add_argument("--shard", default=None, help="i/n: run the i-th of n contiguous slices (each under the foreground limit)")
    args = parser.parse_args()
    results = args.results.resolve(); assert REPO not in results.parents
    for side in ("v96", "next"): (results / side).mkdir(parents=True, exist_ok=True)
    os.environ.update({"SRP_RESULTS": str(results), "PLT_COMPACT_PART": "1"})
    old, new = rr.resolve_core("v96"), rr.resolve_core(args.core)
    cases = rr.recorded_lists(); assert len(cases) == 775
    if args.synthetic:
        cases += load("srp_cases", HERE / "srp_cases.py").cases()
    if args.keys:
        wanted = args.keys.split(","); cases = [c for c in cases if c[0] in wanted]
        assert len(cases) == len(wanted)
    if args.shard:
        i, n = (int(x) for x in args.shard.split("/"))
        size = -(-len(cases) // n); cases = cases[i * size:(i + 1) * size]
    from tests import evidence_loader
    owner = evidence_loader.current_owner()
    if owner: evidence_loader.release(owner)
    workers = max(1, (os.cpu_count() or 2) - 1)
    start = time.monotonic()
    found = rr.replay(cases, (old, new), per_list, workers=workers, part=results / "srp-part.json")
    wall = round(time.monotonic() - start, 3)
    timing = results / "timing.json"
    shards = json.loads(timing.read_text()) if timing.exists() else {}
    shards[args.shard or "all"] = {"wall_time_s": wall, "lists": len(found)}
    timing.write_text(json.dumps(shards))
    print(json.dumps({"lists": len(found), "wall_time_s": wall,
                      "classes": dict(Counter(r["class"] for r in found.values()))}))


if __name__ == "__main__": main()
