"""Summarize the saved replay part: census, classification, change causes, mutation controls.

Run: python3 srp_summarize.py <results-outside-repo>
Reads only the saved part and its result files; runs no core.
"""
from __future__ import annotations
from collections import Counter, defaultdict
import copy
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
spec = importlib.util.spec_from_file_location("srp_replay_summary", HERE / "srp_replay.py")
replay = importlib.util.module_from_spec(spec); sys.modules["srp_replay_summary"] = replay; spec.loader.exec_module(replay)
compare, census = replay.compare, replay.census
SALE_FAMILY_IDS = sorted({r["id"] for r in replay.WORDING})


def synthetic(key): return key.startswith("demo.")


def main():
    root = Path(sys.argv[1]).resolve()
    results = json.loads((root / "srp-part.json").read_text())["results"]
    timing = json.loads((root / "timing.json").read_text())
    assert len(results) == 784
    # Reclassify every saved pair with the current classifier (no core runs).
    for key, r in results.items():
        r["comparison"] = replay.classify(*compare.read_pin(root / "v96", r["v96"]), *compare.read_pin(root / "next", r["next"]))
        r["class"] = r["comparison"]["class"]
    # ---- census on v96 ------------------------------------------------------
    per_text = defaultdict(lambda: {"lists": [], "fields": Counter(), "paths": Counter(), "origins": Counter(), "states": Counter()})
    other = defaultdict(lambda: {"lists": set(), "fields": Counter(), "source": None})
    for key, r in results.items():
        c = r.get("census")
        if not c: continue
        named = r["trace"]["named_rows"]
        for text in {h["text"] for h in c["reasons"]}:
            row = per_text[text]; row["lists"].append(key)
            for h in c["reasons"]:
                if h["text"] == text: row["fields"][h["field"]] += 1; row["paths"][h["path"]] += 1
            for n in named:
                codes = [m for m in n["missing"] or [] if m in replay.CODES]
                row["origins"][f'{n["artifact_id"]} {n["disposition"]} {n["code"]} {sorted(codes)}'] += 1
            if text.startswith("The wash-sale"):
                adj = sorted({f'{a["disposition"]}:{a["code"]}' for a in r["trace"]["adjustment_rows"]
                              if "covered-w" in str(a["artifact_id"])})
                row["states"][" ".join(adj)] += 1
        for h in c["other"]:
            o = other[h["text"]]; o["lists"].add(key); o["fields"][h["field"]] += 1
            o["source"] = replay.OTHER[h["text"]]
    census_out = {"source": "published core v96 / registry v94 / release v94; every whole-string occurrence in the real presentation model",
        "lists": {"recorded": sum(not synthetic(k) for k in results), "synthetic": sum(synthetic(k) for k in results)},
        "pages": {"recorded": sum(r["v96"]["outcome"] == "success" for k, r in results.items() if not synthetic(k)),
                  "synthetic": sum(r["v96"]["outcome"] == "success" for k, r in results.items() if synthetic(k))},
        "reasons": [{"text": t, "recorded_lists": sorted(k for k in v["lists"] if not synthetic(k)),
                     "synthetic_lists": sorted(k for k in v["lists"] if synthetic(k)),
                     "page_fields": len(v["fields"]), "occurrences": sum(v["fields"].values()),
                     "fields": sorted(v["fields"]), "paths": dict(v["paths"]),
                     "origin_rows": dict(v["origins"]), "covered_w_adjustment_row_states": dict(v["states"])}
                    for t, v in sorted(per_text.items())],
        "other_texts_same_citizens": [{"text": t, "source": v["source"], "recorded_lists": sum(not synthetic(k) for k in v["lists"]), "engine_terms": None,
                                       "synthetic_lists": sorted(k for k in v["lists"] if synthetic(k)),
                                       "example_lists": sorted(v["lists"])[:4], "page_fields": len(v["fields"])}
                                      for t, v in sorted(other.items())]}
    census.write(HERE / "census.json", census_out)
    # ---- classification ----------------------------------------------------
    classes = Counter(r["class"] for k, r in results.items() if not synthetic(k))
    syn = Counter(r["class"] for k, r in results.items() if synthetic(k))
    gates = Counter(r["comparison"].get("gate") for r in results.values() if r["class"] == "unexpected")
    errors = Counter((r["v96"].get("error"), r["next"].get("error")) for r in results.values() if r["v96"]["outcome"] == "error")
    # Cause: rows whose disposition/code changed, by the new code; values lost.
    causes, lost, unclosed_lists, val_changed = Counter(), Counter(), 0, 0
    validation_value_meaning = 0
    for key, r in results.items():
        if r["class"] != "unexpected" or r["v96"]["outcome"] != "success": continue
        a, _ = compare.read_pin(root / "v96", r["v96"]); b, _ = compare.read_pin(root / "next", r["next"])
        da = {(x.get("artifact_id"), x.get("symbol")): x for x in a["rows"]}
        db = {(x.get("artifact_id"),): x for x in b["rows"]}
        by_art_b = defaultdict(list)
        for x in b["rows"]: by_art_b[x.get("artifact_id")].append(x)
        any_unclosed = False
        for x in a["rows"]:
            ys = by_art_b.get(x.get("artifact_id")) or []
            y = ys[0] if ys else None
            if y is None: causes["row absent"] += 1; continue
            if (x.get("disposition"), x.get("code")) != (y.get("disposition"), y.get("code")):
                causes[f'{x.get("disposition")}:{x.get("code")} -> {y.get("disposition")}:{y.get("code")}'] += 1
                if y.get("code") == "SOURCE_SET_UNCLOSED" and any(m in SALE_FAMILY_IDS or str(m).startswith(tuple(SALE_FAMILY_IDS)) for m in y.get("missing") or []):
                    any_unclosed = True
        unclosed_lists += any_unclosed
        va = {(v["symbol"]): v["value"] for v in a["values"]}; vb = {(v["symbol"]): v["value"] for v in b["values"]}
        lost["values only on v96"] += len(set(va) - set(vb)); lost["values only on next"] += len(set(vb) - set(va))
        if any(va.get(s) != vb.get(s) for s in set(va) & set(vb)): val_changed += 1
        if any(isinstance(v, dict) and any(isinstance(x, dict) and x.get("meaning") in replay.OLD_TO_NEW for x in v.get("violations") or []) for v in va.values()):
            validation_value_meaning += 1
    pages_new = sum(1 for r in results.values() if (r.get("next_census") or {}).get("new"))
    replay_out = {"cores": ["published v96 (registry v94, release v94)", "scratch v97 (registry v95, release v95), loader entries copied from v96"],
        "workers": 9, "shards": timing, "wall_time_s": round(sum(v["wall_time_s"] for v in timing.values()), 3),
        "recorded_lists": sum(not synthetic(k) for k in results), "recorded_counts": dict(classes),
        "synthetic_lists": sum(synthetic(k) for k in results), "synthetic_counts": dict(syn),
        "unexpected_gates": dict(gates), "error_pairs": {f"{a} / {b}": n for (a, b), n in errors.items()},
        "successful_unexpected_lists_with_a_sale_family_now_unclosed": unclosed_lists,
        "row_changes_by_transition": dict(causes.most_common(25)), "publication_values": dict(lost),
        "lists_with_a_shared_symbol_value_changed": val_changed,
        "lists_whose_v96_publication_values_carry_an_old_reason": validation_value_meaning,
        "successor_pages_drawing_a_new_sentence": pages_new,
        "classification_by_list": {k: r["class"] for k, r in sorted(results.items())}}
    census.write(HERE / "replay.json", replay_out)
    # ---- mutation controls on an ideal successor ----------------------------
    key = sorted(k for k, r in results.items() if r.get("census") and r["census"]["reasons"] and not synthetic(k))[0]
    a, am = compare.read_pin(root / "v96", results[key]["v96"])
    ideal = replay.expected_model(am)
    verdict = replay.classify(a, am, copy.deepcopy(a), ideal)
    assert verdict["class"] == "expected_sentences", verdict
    controls = {}
    new_text = replay.WORDING[0]["new"]
    for kind in ("value", "page_value", "boolean_value", "disposition", "code", "missing_name", "unplanned_sentence",
                 "question_identity", "added_row", "removed_row", "added_field", "removed_field",
                 "planned_text_wrong_property", "old_reason_kept", "wrong_reason_sentence"):
        altered, model = copy.deepcopy(a), copy.deepcopy(ideal)
        blocked = next(x for x in altered["rows"] if x.get("disposition") == "blocked" and x.get("missing"))
        reasons = [s["resolved"]["reasons"] for s in model["sections"] if s["resolved"].get("reasons")]
        if kind == "value": altered["values"][0]["value"] = "demo.changed-value"
        if kind in ("page_value", "boolean_value"):
            field = next(s for s in model["sections"] if isinstance(s["resolved"].get("value"), (int, float)))
            field["resolved"]["value"] = True if kind == "boolean_value" else 1234567
        if kind == "disposition": blocked["disposition"] = "published"
        if kind == "code": blocked["code"] = "demo.unplanned-code"
        if kind == "missing_name": blocked["missing"].append("demo.unplanned-missing")
        if kind == "unplanned_sentence": model["sections"][0]["field"]["label"] += " demo.unplanned sentence"
        if kind == "question_identity": reasons[0][0]["question_id"] = "demo.unplanned-question"
        if kind == "added_row": altered["rows"].append({"artifact_id": "demo.extra-row", "disposition": "blocked", "missing": []})
        if kind == "removed_row": altered["rows"].pop()
        if kind == "added_field": model["sections"].append(copy.deepcopy(model["sections"][0]))
        if kind == "removed_field": model["sections"].pop()
        if kind == "planned_text_wrong_property": model["sections"][0]["field"]["label"] = new_text
        if kind == "old_reason_kept":
            target = next(x for rs in reasons for x in rs if x.get("sentence") in set(replay.OLD_TO_NEW.values()))
            target["sentence"] = next(o for o, n in replay.OLD_TO_NEW.items() if n == target["sentence"])
        if kind == "wrong_reason_sentence":
            target = next(x for rs in reasons for x in rs if x.get("sentence") in set(replay.OLD_TO_NEW.values()))
            target["sentence"] = next(n for n in set(replay.OLD_TO_NEW.values()) if n != target["sentence"])
        v = replay.classify(a, am, altered, model)
        controls[kind] = {"rejected": v["class"] == "unexpected", "gate": v.get("gate")}
    assert all(c["rejected"] for c in controls.values()), controls
    census.write(HERE / "mutations.json", {"case": key, "positive_control": verdict["class"],
        "basis": "No scratch pair is admissible (every successful pair fails an integrity gate), so the controls run on an ideal successor: the v96 rows and model with only the declared reason sentences replaced. The classifier admits it, then rejects each mutation.",
        "controls": controls})
    print(json.dumps({k: v for k, v in replay_out.items() if k != "classification_by_list"}, indent=1))
    print(json.dumps([{k: v for k, v in r.items() if k not in ("recorded_lists", "fields")} | {"recorded": len(r["recorded_lists"])} for r in census_out["reasons"]], indent=1))
    print(json.dumps(census_out["other_texts_same_citizens"], indent=1)[:4000])
    print(json.dumps(controls))


if __name__ == "__main__": main()
