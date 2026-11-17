"""Strict complete-pin classifier. Run: python3 classify.py <part> <time-log>.

Checks all rows, additions/removals, values, dispositions and refusal codes
before allowing only the declared line-16 name/sentence substitution.
"""
from __future__ import annotations
import argparse
from collections import Counter
import copy
import importlib.util
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("l16_classifier_probe", HERE / "probe.py")
probe = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = probe
spec.loader.exec_module(probe)


def exact(a, b):
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def exception_sentences():
    content = probe.REPO / "packages/content/tax/2025"
    return [json.loads((content / ("input-question." + name.replace("exception1.", "exception1-") + "." + version + ".json")).read_text())["question"]
            for name, version in zip(probe.EXC, ("v3", "v2", "v2", "v2"))]


def classify_pair(a, b):
    ar, br = a.get("rows", {}), b.get("rows", {})
    # Universal integrity gates, before contextual labels.
    if ar.keys() != br.keys() or not exact(a.get("lines"), b.get("lines")):
        return "unexpected"
    for name in ar:
        if not exact(ar[name][:2], br[name][:2]):
            return "unexpected"
    if exact(a, b):
        return "same_error" if a.get("error") else "identical_success"
    if a.get("error") or b.get("error"):
        return "unexpected"
    before = ["blocked", "DEPENDENCY_ABSENT", probe.FOUR]
    after = ["blocked", "DEPENDENCY_ABSENT", probe.FOUR + probe.EXC]
    changed = [name for name in ar if not exact(ar[name], br[name])]
    if (changed != ["form1040-line16"] or not exact(ar[changed[0]], before)
            or not exact(br[changed[0]], after)
            or not exact(ar.get("selected-preferential-base"), after)):
        return "unexpected"
    expected = copy.deepcopy(a)
    expected["rows"]["form1040-line16"] = after
    exc = exception_sentences()
    for collection in ("reasons", "blocked_reasons"):
        for field in probe.WATCH:
            if field in expected.get(collection, {}):
                expected[collection][field] = sorted(set(expected[collection][field]) | set(exc))
    # On the recorded target returns these sentences are already on the page.
    # Allow only these exact additions if the shared collection does change.
    if "questions" in expected:
        expected["questions"] = sorted(set(expected["questions"]) | set(exc))
    return "expected_line16_names" if exact(expected, b) else "unexpected"


def failing_criteria(acts):
    """Current return-level answers from the recorded input, not candidate rows.

    Retraction never revives an earlier same-fact answer. An incomplete or
    malformed set cannot authorize the contextual expected label.
    """
    current = {}
    for act in acts:
        payload = act.get("payload") or {}
        finding = payload.get("finding") or (payload.get("member") or {}).get("finding") or {}
        name = probe.short(str(finding.get("fact_id", "")).split("|", 1)[0])
        if name in probe.EXC: current[name] = (finding.get("id"), finding.get("value"))
        if act.get("kind") == "finding-retracted":
            for key, (ident, value) in list(current.items()):
                if ident == payload.get("finding_id"): current[key] = (ident, None)
    if set(current) != set(probe.EXC) or any(v not in ("yes", "no") for _, v in current.values()): return None
    return [name for name in probe.EXC if current[name][1] == "no"]


def classify_criteria_pair(a, b, failed):
    ar, br = a.get("rows", {}), b.get("rows", {})
    # These universal gates precede every expected label, including errors.
    if ar.keys() != br.keys() or not exact(a.get("lines"), b.get("lines")): return "unexpected"
    if any(not exact(ar[name][:2], br[name][:2]) for name in ar): return "unexpected"
    if exact(a, b): return "same_error" if a.get("error") else "identical_success"
    if a.get("error") or b.get("error") or not failed: return "unexpected"
    if failed != [name for name in probe.EXC if name in failed]: return "unexpected"
    before16 = ["blocked", "DEPENDENCY_ABSENT", probe.FOUR]
    beforepref = ["blocked", "DEPENDENCY_ABSENT", probe.FOUR + probe.EXC]
    # The published preferential-base block is reachable only in the exact
    # required/no-activity/no-Form-8949-yes state. Couple it with v8's block.
    if not exact(ar.get("form1040-line16"), before16) or not exact(ar.get("selected-preferential-base"), beforepref): return "unexpected"
    changed = {name for name in ar if not exact(ar[name], br[name])}
    if changed != {"form1040-line16", "selected-preferential-base"}: return "unexpected"
    after = ["blocked", "DEPENDENCY_ABSENT", failed]
    if not all(exact(br[name], after) for name in changed): return "unexpected"
    expected = copy.deepcopy(a)
    for name in changed: expected["rows"][name] = copy.deepcopy(after)
    law = json.loads((HERE / "law.json").read_text())
    words = {row["name"]: row["sentence"] for row in law["questions"]}
    old_words = set(words.values())
    new_words = {words[name] for name in failed}
    # This committed reproduction names precisely the 28 fields in the
    # recorded target's explanation chain; it is not a candidate-derived list.
    base = probe.read_cases(HERE / "baseline.json")
    target_fields = set(probe.expand(base["recorded/t4_s1_removed"])["fields"])
    for collection in ("reasons", "blocked_reasons"):
        for field, sentences in expected.get(collection, {}).items():
            if field in target_fields:
                expected[collection][field] = sorted((set(sentences) - old_words) | new_words)
    if "questions" in expected:
        expected["questions"] = sorted((set(expected["questions"]) - old_words) | new_words)
    return "expected_failing_criteria" if exact(expected, b) else "unexpected"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("part", type=Path)
    parser.add_argument("time_log", type=Path)
    parser.add_argument("--track0b", action="store_true")
    parser.add_argument("--out", help="Evidence output filename beside this script")
    parser.add_argument("--item", type=int, help="Charter item number recorded in the summary")
    args = parser.parse_args()
    from tools.recorded_replay import recorded_lists
    results = json.loads(args.part.read_text())["results"]
    recorded = dict(recorded_lists())
    assert set(results) == set(recorded)
    failed_by_key = {key: failing_criteria(acts) for key, acts in recorded.items()} if args.track0b else {}

    def label_for(key, a, b):
        return classify_criteria_pair(a, b, failed_by_key[key]) if args.track0b else classify_pair(a, b)
    rows = {}
    tool_counts = Counter()
    row_changes = Counter()
    for key, result in sorted(results.items()):
        a, b = result["pins"]["v94"], result["pins"]["v95"]
        label = label_for(key, a, b)
        tool_counts[result["class"]] += 1
        changes = {name: {"v94": a.get("rows", {}).get(name), "v95": b.get("rows", {}).get(name)}
                   for name in set(a.get("rows", {})) | set(b.get("rows", {}))
                   if name not in a.get("rows", {}) or name not in b.get("rows", {})
                   or not exact(a["rows"][name], b["rows"][name])}
        row_changes.update(changes.keys())
        rows[key] = {"classification": label}
        if not exact(a, b):
            rows[key].update({"row_changes": changes,
                              "sentence_fields": [f for f in ("questions", "reasons", "blocked_reasons") if not exact(a.get(f), b.get(f))]})
    counts = Counter(r["classification"] for r in rows.values())
    # Adversarial checks use an actual allowed result, so a permissive contextual
    # shortcut cannot conceal added rows, lost rows, changed money or new errors.
    allowed_label = "expected_failing_criteria" if args.track0b else "expected_line16_names"
    changed_entry = next(((key, r) for key, r in results.items() if label_for(key, r["pins"]["v94"], r["pins"]["v95"]) == allowed_label), None)
    controls = {}
    if changed_entry:
        changed_key, changed = changed_entry
        a, b = changed["pins"]["v94"], changed["pins"]["v95"]
        for kind in ("added_row", "removed_row", "disposition", "refusal_code", "line_value", "boolean_value", "extra_sentence", "new_error"):
            altered = copy.deepcopy(b)
            if kind == "added_row": altered["rows"]["demo.extra"] = ["published", None, []]
            if kind == "removed_row": altered["rows"].pop(next(iter(altered["rows"])))
            if kind == "disposition": altered["rows"]["form1040-line16"][0] = "published"
            if kind == "refusal_code": altered["rows"]["form1040-line16"][1] = "DEPENDENCY_INVALID"
            if kind == "line_value": altered["lines"][next(iter(altered["lines"]))] = 12345
            if kind == "boolean_value": altered["lines"][next(iter(altered["lines"]))] = True
            if kind == "extra_sentence": altered["questions"].append("demo unrelated sentence")
            if kind == "new_error": altered["error"] = "demo.error"
            controls[kind] = label_for(changed_key, a, altered) == "unexpected"
        if args.track0b:
            failed = failed_by_key[changed_key]
            altered = copy.deepcopy(b)
            passing = next(name for name in probe.EXC if name not in failed)
            altered["rows"]["form1040-line16"][2].append(passing)
            altered["rows"]["selected-preferential-base"][2].append(passing)
            controls["passing_criterion_name"] = label_for(changed_key, a, altered) == "unexpected"
            altered = copy.deepcopy(b)
            altered.setdefault("blocked_reasons", {})["form1040.line-1a"] = ["demo unrelated sentence"]
            controls["unrelated_field_sentence"] = label_for(changed_key, a, altered) == "unexpected"
            controls["missing_input_context"] = classify_criteria_pair(a, b, None) == "unexpected"
        assert all(controls.values())
    wall = float(re.findall(r"^real\s+([0-9.]+)", args.time_log.read_text(), flags=re.M)[-1])
    output = {"lists": len(rows), "workers": max(1, (__import__('os').cpu_count() or 2) - 1),
              "wall_time_s": wall, "counts": dict(counts), "tool_counts": dict(tool_counts),
              "changed_row_names": dict(row_changes), "classifier_controls": controls,
              "added_rows": sum(v["v94"] is None for r in rows.values() for v in r.get("row_changes", {}).values()),
              "removed_rows": sum(v["v95"] is None for r in rows.values() for v in r.get("row_changes", {}).values()),
              "results": rows}
    if args.track0b:
        output.update({"item": 5, "verdict": "FAIL" if counts["unexpected"] else "PASS",
            "line_value_changes": sum(not exact(r["pins"]["v94"].get("lines"), r["pins"]["v95"].get("lines")) for r in results.values()),
            "disposition_or_code_changes": sum(any(not exact(r["pins"]["v94"].get("rows", {}).get(name, [])[:2], r["pins"]["v95"].get("rows", {}).get(name, [])[:2])
                for name in set(r["pins"]["v94"].get("rows", {})) | set(r["pins"]["v95"].get("rows", {}))) for r in results.values())})
    if args.item is not None: output["item"] = args.item
    output_name = args.out or ("track0b-replay.json" if args.track0b else "rerun.json")
    assert Path(output_name).name == output_name, "output must be a filename"
    probe.write(output_name, output)
    print(json.dumps({k: v for k, v in output.items() if k != "results"}, indent=2))
    assert not counts["unexpected"], "unexpected replay change; see " + output_name


if __name__ == "__main__":
    main()
