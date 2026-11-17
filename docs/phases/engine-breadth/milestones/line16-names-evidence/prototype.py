"""Build only scratch content from published core v94. Never writes packages/.

Run: python3 prototype.py <new-scratch-directory> [--broad]
The broad comparison adds eight names to the personal-loss case too.
"""
from __future__ import annotations
import argparse
import copy
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
P = "tax.us.2025."


def failing_tree(builder, fallback, index=0, failed=()):
    """Enumerate the 15 nonempty subsets using admitted choose/block nodes.

    A required conclusion proves at least one criterion is no. When the first
    three pass, the last criterion must fail; omit the unreachable all-yes
    leaf and its comparison. No helper citizen is needed.
    """
    if index == len(builder.EXC):
        assert failed
        return {"op": "block", "code": "DEPENDENCY_ABSENT", "missing": list(failed)}
    name = builder.EXC[index]
    if index == len(builder.EXC) - 1 and not failed:
        return {"op": "block", "code": "DEPENDENCY_ABSENT", "missing": [name]}
    return {"op": "choose", "when": {"op": "categorical_compare", "cmp": "eq",
        "left": {"op": "ref", "name": name},
        "right": {"op": "category_literal", "fact_type": {"id": name, "version": "v1"}, "value": "no"}},
        "then": failing_tree(builder, fallback, index + 1, (*failed, name)),
        "else": failing_tree(builder, fallback, index + 1, failed)}


def build_track0b(builder, scratch):
    old16 = json.loads((builder.CONTENT / "rule.form1040-line16.v8.json").read_text())
    oldpref = json.loads((builder.CONTENT / "rule.selected-preferential-base.v11.json").read_text())
    line16, pref = copy.deepcopy(old16), copy.deepcopy(oldpref)
    fallback = copy.deepcopy(line16["when"]["else"])
    line16["version"] = "v9"
    line16["notes"] += " v9: required Schedule D, no represented sale and no-Form-8949 yes names only the Exception 1 criteria answered no. Other branches retain v8 behavior."
    eq = lambda name, value: {"op": "categorical_compare", "cmp": "eq", "left": {"op": "ref", "name": name},
        "right": {"op": "category_literal", "fact_type": {"id": name, "version": "v1"}, "value": value}}
    line16["when"]["else"] = {"op": "choose", "when": eq(builder.CONCLUSION, "yes"),
        "then": {"op": "choose", "when": eq(builder.NO_8949, "yes"),
                 "then": failing_tree(builder, fallback), "else": copy.deepcopy(fallback)},
        "else": copy.deepcopy(fallback)}
    pref["version"] = "v12"
    pref["notes"] = str(pref.get("notes") or "") + " v12: the existing required/no-activity block names exactly the Exception 1 criteria answered no."
    replacements = []

    def walk(node, path=()):
        if not isinstance(node, (dict, list)): return
        if isinstance(node, dict) and node.get("op") == "block" and node.get("missing") == builder.NAMED:
            replacements.append((path, copy.deepcopy(node)))
            changed = failing_tree(builder, node)
            node.clear(); node.update(changed)
            return
        for key, value in (node.items() if isinstance(node, dict) else enumerate(node)):
            walk(value, (*path, key))

    walk(pref["when"])
    assert len(replacements) == 1
    # Undo only the two declaring-block rewrites: the rest of each rule must
    # match the published predecessor structurally, including every value,
    # requires, pin, citation, other guard branch and fallback declaration.
    normalized16, normalizedpref = copy.deepcopy(line16), copy.deepcopy(pref)
    normalized16["when"]["else"] = copy.deepcopy(fallback)
    parent = normalizedpref["when"]
    path, original = replacements[0]
    for key in path[:-1]: parent = parent[key]
    parent[path[-1]] = original
    for normalized, old in ((normalized16, old16), (normalizedpref, oldpref)):
        normalized["version"], normalized["notes"] = old["version"], old["notes"]
        assert normalized == old
    written = [("rule.form1040-line16.v9.json", line16), ("rule.selected-preferential-base.v12.json", pref)]
    summary = builder.build(scratch, written, record=False)
    summary.update({"item": 1, "verdict": "PASS", "variant": "track0b-failing-criteria", "shape": "nested categorical choose over four existing criteria, nonempty literal block lists at leaves",
        "target": "required Schedule D, no represented sale, no-Form-8949 yes",
        "cost": {"helper_rules": 0, "new_schema_or_engine_ops": 0, "choose_nodes_per_criterion_tree": 14,
                 "nonempty_subsets_per_rule": 15, "criterion_tree_leaves_per_rule": 15,
                 "criterion_comparisons_on_selected_path_per_rule": {"min": 3, "max": 4},
                 "line16_target_gate_choose_nodes": 2},
        "unchanged_after_undoing_declaring_blocks": True,
        "named_questions": [name.removeprefix(P) for name in builder.EXC],
        "guard": "The two target blocks name only the current failing criteria; original outer guard outcomes and other branches remain.",
        "alternatives": {"helper_rules": "Adds citizens, package members and dependencies for a four-input finite choice; unnecessary.",
                         "first_failing_only": "Smaller tree but omits other failing criteria; violates the completeness requirement.",
                         "dynamic_missing_expression": "Not part of admitted v17; would need a schema/engine change and is out of scope."},
        "successor_rule_bytes": {name: len((json.dumps(body, indent=2) + "\n").encode()) for name, body in written}})
    (HERE / "track0b-build.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("scratch", type=Path)
    parser.add_argument("--broad", action="store_true")
    parser.add_argument("--track0b", action="store_true")
    args = parser.parse_args()
    path = HERE.parent / "preferential-base-reason-evidence/prototype.py"
    spec = importlib.util.spec_from_file_location("l16_published_content_builder", path)
    builder = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = builder
    spec.loader.exec_module(builder)
    builder.FROM = {"package": "v94", "registry": "v92", "release": "v92"}
    builder.TO = {"package": "v95", "registry": "v93", "release": "v93"}
    if args.track0b:
        assert not args.broad
        print(json.dumps(build_track0b(builder, args.scratch), indent=2))
        return
    body = builder.line16_body()
    # The existing outer guard proves no represented sale. The nested conclusion
    # compare restricts changes to required Schedule D. A known Form 8949 item
    # distinguishes the personal-loss case from an empty required return.
    if not args.broad:
        named = body["when"]["else"]["then"]
        body["when"]["else"]["then"] = {
            "op": "choose",
            "when": {"op": "categorical_compare", "cmp": "eq",
                     "left": {"op": "ref", "name": builder.NO_8949},
                     "right": {"op": "category_literal",
                               "fact_type": {"id": builder.NO_8949, "version": "v1"}, "value": "yes"}},
            "then": named,
            "else": {"op": "block", "code": "DEPENDENCY_ABSENT", "missing": builder.FOUR},
        }
        body["notes"] += " Eight names require the existing no-Form-8949 answer to be yes; known Form 8949 work keeps four."
    old = json.loads((builder.CONTENT / builder.LINE16_RULE).read_text())
    assert all(body[k] == old[k] for k in old if k not in ("when", "version", "notes"))
    summary = builder.build(args.scratch, [(builder.LINE16_SUCCESSOR, body)], record=False)
    summary.update({"variant": "broad" if args.broad else "narrow",
                    "guard": "existing no-sale block, required Schedule D" + ("" if args.broad else ", no-Form-8949 yes"),
                    "new_answer": False, "unchanged": ["value", "requires", "pins", "blocked", "refusal codes"],
                    "boundary_read": "none" if args.broad else "existing no-form8949-sources answer; absent answer blocks on its existing name"})
    (HERE / ("broad-build.json" if args.broad else "prototype-build.json")).write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
