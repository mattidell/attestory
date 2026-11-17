"""Track 0b live evidence on two scratch declaring-block successors.

Run: python3 track0b.py names|boundary|neighbours <scratch-core.json>
Names covers every nonempty failing subset on all three filing statuses,
the four recorded targets, and both individual answers to every shown name.
"""
from __future__ import annotations
from collections import Counter
import copy
import itertools
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
import importlib.util


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


t0 = module("l16_t0b_track0", HERE / "track0.py")
p0 = t0.p0
P = p0.P
EXC = p0.EXC
WATCH = p0.WATCH
QUESTIONS = {row["name"]: row["sentence"] for row in json.loads((HERE / "law.json").read_text())["questions"]}


def write(name, body):
    p0.write("track0b-" + name + ".json", body)


def failed_answers(acts):
    current = {}
    for act in acts:
        finding = (act.get("payload") or {}).get("finding") or {}
        name = p0.short(str(finding.get("fact_id", "")).split("|", 1)[0])
        if name in EXC: current[name] = finding.get("value")
    assert set(current) == set(EXC) and set(current.values()) <= {"yes", "no"}
    return [name for name in EXC if current[name] == "no"]


def states():
    base = dict(p0.lists())
    _, h, _ = t0.context(None)
    cases = [(key, base[key]) for key in t0.TARGETS[:4]]
    for status in t0.STATUSES:
        for mask in range(1, 16):
            acts = copy.deepcopy(base["status/" + status + "/required"])
            for i, name in enumerate(EXC):
                acts = h.say(acts, P + name, "no" if mask & (1 << i) else "yes", "t0b-" + name)
            cases.append(("subset/" + status + "/" + str(mask), acts))
    return cases


def affected_fields(result):
    by_symbol = {row["symbol"]: row for row in result["rows"]}
    target = "capital-gains.selected-preferential-base"

    def reaches(row, seen=frozenset()):
        if not row: return False
        if row["symbol"] == target: return True
        return any(name not in seen and reaches(by_symbol.get(name), seen | {name}) for name in row["missing"])

    return {name for name, field in result["fields"].items() if name in WATCH or reaches(field["row"])}


def check_fields(result, failed):
    expected = sorted(QUESTIONS[name] for name in failed)
    fields, fails = {}, []
    for name in sorted(affected_fields(result)):
        field = result["fields"][name]
        words = sorted(reason["sentence"] for reason in field["reasons"])
        criterion_words = sorted(w for w in words if w in {QUESTIONS[n] for n in EXC})
        forbidden = [w for w in words if w in {QUESTIONS[n] for n in p0.FOUR}]
        passed = words == expected and criterion_words == expected and not forbidden and bool(words)
        fields[name] = {"verdict": "PASS" if passed else "FAIL", "sentences": words,
                        "expected_criterion_sentences": expected, "forbidden_sale_or_boundary_sentences": forbidden}
        if not passed: fails.append({"field": name, "proposed_fix": "Correct the declaring-block routing; if the real projection cannot retain these exact criteria, stop without editing it."})
    assert WATCH <= set(fields)
    return fields, fails


def names(core):
    cases = states()
    base, wall_a = t0.parallel(core, cases)
    _, h, _ = t0.context(core)
    alternatives = []
    expected = {key: failed_answers(acts) for key, acts in cases}
    for key, acts in cases:
        for name in expected[key]:
            for answer in ("yes", "no"):
                alternatives.append((key + "/" + name + "/" + answer,
                    h.say(copy.deepcopy(acts), P + name, answer, "t0b-one-" + name)))
    changed, wall_b = t0.parallel(core, alternatives)
    rows, pairs, name_fails, field_fails = {}, [], [], []
    for key, _ in cases:
        original = t0.line16(base[key])
        failed = expected[key]
        pref = next(r for r in base[key]["rows"] if r["artifact"] == "selected-preferential-base")
        complete = original["row"]["missing"] == failed and pref["missing"] == failed
        fields, fails = check_fields(base[key], failed)
        rows[key] = {"failed_criteria": failed, "complete_exact_declarations": complete, "fields": fields}
        field_fails.extend({"case": key, **f} for f in fails)
        if not complete: name_fails.append({"case": key, "proposed_fix": "Both blocks must declare exactly the current no-valued criteria."})
        for name in failed:
            outcomes = {a: t0.line16(changed[key + "/" + name + "/" + a]) for a in ("yes", "no")}
            remaining = [n for n in failed if n != name]
            truthful_moves = not t0.exact(t0.signature(outcomes["yes"]), t0.signature(original))
            preserves_no = t0.exact(t0.signature(outcomes["no"]), t0.signature(original))
            exact_remaining = outcomes["yes"]["row"]["missing"] == remaining if remaining else True
            passed = truthful_moves and preserves_no and exact_remaining
            pairs.append({"case": key, "name": name, "truthful_correction": "yes", "verdict": "PASS" if passed else "FAIL",
                          "correcting_yes_moves_or_unblocks": truthful_moves, "no_keeps_current_block": preserves_no,
                          "remaining_names_exact": exact_remaining, "results": outcomes})
            if not passed: name_fails.append({"case": key, "name": name, "proposed_fix": "The corrected criterion must disappear and every remaining failing criterion must remain named."})
    write("names", {"item": 2, "verdict": "FAIL" if name_fails else "PASS", "states": len(cases),
        "name_pairs": len(pairs), "live_runs": len(cases) + len(alternatives), "wall_time_s": wall_a + wall_b,
        "truth_basis": "These synthetic worlds have no reportable transaction, QOF deferral, losses or non-box-2a gain. The no-valued answers are deliberately mistaken; yes corrects each. Multi-failure states move by removing exactly one failed name even while other failures keep the line blocked.",
        "rows": {k: {n: v for n, v in row.items() if n != "fields"} for k, row in rows.items()},
        "pairs": pairs, "fails": name_fails})
    write("fields", {"item": 3, "verdict": "FAIL" if field_fails else "PASS", "states": len(cases),
        "field_occurrences": sum(len(row["fields"]) for row in rows.values()),
        "rows": {k: row["fields"] for k, row in rows.items()}, "fails": field_fails,
        **t0.packed(base)})
    print(json.dumps({"states": len(cases), "pairs": len(pairs), "runs": len(cases) + len(alternatives),
        "name_fails": len(name_fails), "field_fails": len(field_fails)}, indent=2))


def boundary(core):
    t0.write = lambda name, body: write(name, body)
    t0.boundaries(core)
    path = HERE / "track0b-boundary.json"
    saved = json.loads(path.read_text())
    before = {k: p0.expand(v) for k, v in p0.read_cases(HERE / "track0-boundary.json").items()}
    after = {k: p0.expand(v) for k, v in p0.read_cases(path).items()}
    previous = json.loads((HERE / "track0-boundary.json").read_text())["actionability"]
    differences, fails = {}, []
    for key, row in after.items():
        changes = {name: {"old_narrow": before[key]["fields"].get(name), "track0b": row["fields"].get(name)}
            for name in set(row["fields"]) | set(before[key]["fields"])
            if not t0.exact(row["fields"].get(name), before[key]["fields"].get(name))}
        target = "/fully-required/yes" in key
        for name, change in changes.items():
            a, b = change["old_narrow"], change["track0b"]
            if not target or a["value"] != b["value"] or a["disposition"] != b["disposition"]:
                fails.append({"case": key, "field": name, "proposed_fix": "Keep non-target boundary states and all values/dispositions unchanged."})
        if target:
            _, problems = check_fields(row, [EXC[0]])
            fails.extend({"case": key, **problem} for problem in problems)
        for name, field in row["fields"].items():
            if field["disposition"] != "blocked": continue
            usable = set(previous[key][name]["actionable_sentences"])
            if not usable & {r["sentence"] for r in field["reasons"]}:
                fails.append({"case": key, "field": name, "proposed_fix": "Retain a truthful actionable question; stop if declared names cannot do it."})
        differences[key] = {"classification": "target_criterion_names" if target and changes else "identical" if not changes else "unexpected", "changed_fields": sorted(changes)}
    saved.update({"item": 4, "verdict": "FAIL" if fails or saved["fails"] else "PASS", "classification": differences,
                  "compatibility_fails": fails, "actionability": "Every blocked field retains an actionable sentence established by Track 0's same boundary-world assessment."})
    write("boundary", saved)
    print(json.dumps({"boundary_compatibility_fails": len(fails)}, indent=2))


def main():
    command, core = sys.argv[1:3]
    if command == "names": names(core)
    elif command == "boundary": boundary(core)
    elif command == "neighbours":
        t0.write = lambda name, body: write(name, body)
        t0.neighbours(core)
    else: raise SystemExit("usage: track0b.py names|boundary|neighbours <core.json>")


if __name__ == "__main__": main()
