"""Census of every earned income credit answer on published core v99, and of what the recorded lists carry.

Evidence for docs/phases/engine-breadth/milestones/eic-answer-questions.md (P0).

Part 1 (static, from the published package): for every ``rule.eic-answer.*``
member of core v99, the fact it reads, the conditions under which the rule
publishes 1 without the answer (so the answer is required otherwise), and
whether an ``input-question`` member names that fact type. Then every other
fact a credit rule reads that no rule publishes (the filer's or the roster's
inputs), with the same question check.

Part 2 (``--recorded``): for each of those facts, how many of the recorded act
lists (tools/recorded_replay.recorded_lists) carry it and with which value,
plus two cross-tabulations the derivation question needs: the standard
deduction's "someone can claim you as a dependent" answer against the credit's
not-claimable answer, and the 65-or-older answer against the credit's age
answer.

Run: python3 census.py [--recorded] --out census.json
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

CONTENT = REPO / "packages/content/tax/2025"
P = "tax.us.2025."
CORE = "v99"


def _corpus() -> dict[tuple[str, str], tuple[str, dict[str, Any]]]:
    found = {}
    for path in CONTENT.glob("*.json"):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if isinstance(body, dict) and isinstance(body.get("id"), str) and isinstance(body.get("version"), str):
            found[(body["id"], body["version"])] = (path.name, body)
    return found


def _strings(node: Any, out: set[str]) -> None:
    if isinstance(node, str):
        out.add(node)
    elif isinstance(node, dict):
        for value in node.values():
            _strings(value, out)
    elif isinstance(node, list):
        for value in node:
            _strings(value, out)


def _short(name: str) -> str:
    return name.removeprefix(P)


def _expr(e: Any) -> str:
    """A compact reading of a rule-language expression."""
    if not isinstance(e, dict):
        return json.dumps(e)
    op = e.get("op")
    if op == "ref":
        return _short(e["name"])
    if op in ("compare", "categorical_compare"):
        right = e["right"]
        if isinstance(right, dict) and right.get("op") == "category_literal":
            right = right["value"]
        elif isinstance(right, dict) and right.get("op") == "parameter":
            right = "param:" + right["key"]
        elif isinstance(right, dict):
            right = _expr(right)
        return f"{_expr(e['left'])} {e['cmp']} {right}"
    if op in ("any", "all"):
        return op + "(" + "; ".join(_expr(a) for a in e["args"]) + ")"
    if op == "choose":
        return f"if {_expr(e['when'])} then {_expr(e['then'])} else {_expr(e['else'])}"
    if op == "conditional_dependency_set":
        return "needs(" + ", ".join(_expr(m) for m in e["members"]) + ")"
    if op == "block":
        return "block:" + str(e.get("code"))
    return str(op)


def static() -> dict[str, Any]:
    corpus = _corpus()
    package = corpus[(P + "package.core-calculations", CORE)][1]
    published: dict[str, str] = {}
    questions: dict[str, str] = {}
    titles: dict[str, str] = {}
    rules = []
    for member in package["members"]:
        name, body = corpus[(member["id"], member["version"])]
        if body.get("publishes"):
            published[body["publishes"]] = member["id"]
        if member["role"] == "input-question":
            questions[body["fact_type"]["id"]] = body["id"]
        for fact_type in body.get("fact_types") or []:
            titles[fact_type["id"]] = fact_type.get("title", "")
        if member["role"] == "computation" and (".rule.eic" in member["id"] or member["id"].endswith("form1040-line27a")):
            rules.append((member, name, body))
    answers = []
    inputs: dict[str, set[str]] = {}
    for member, name, body in sorted(rules, key=lambda r: r[0]["id"]):
        seen: set[str] = set()
        _strings({k: v for k, v in body.items() if k in ("value", "requires", "selection", "subject")}, seen)
        read = sorted(s for s in seen if s.startswith(P) and s not in published and "parameter." not in s
                      and not s.endswith(".source-closure") and "inert-path" not in s)
        for fact in read:
            inputs.setdefault(fact, set()).add(_short(member["id"]))
        if ".rule.eic-answer." in member["id"]:
            fact = P + "eic." + member["id"].split(".rule.eic-answer.")[1]
            answers.append({
                "rule": _short(member["id"]) + " " + member["version"],
                "file": name,
                "fact": _short(fact),
                "reads": [_short(r) for r in body.get("requires", [])],
                "value": _expr(body["value"]),
                "question": _short(questions[fact]) if fact in questions else None,
            })
    others = [{"fact": _short(f), "read_by": sorted(by), "question": _short(questions[f]) if f in questions else None,
               "title": titles.get(f, "")[:200]}
              for f, by in sorted(inputs.items()) if not any(a["fact"] == _short(f) for a in answers)]
    return {"core": CORE, "answer_rules": answers, "answer_rule_count": len(answers),
            "with_question": sum(1 for a in answers if a["question"]),
            "other_inputs": others,
            "retired_answer_rules_not_on_core": sorted(
                {_short(i) for (i, _v) in corpus if ".rule.eic-answer." in i}
                - {_short(m["id"]) for m in package["members"]})}


TRACKED = ("eic.age-25-under-65", "eic.main-home-in-us", "eic.not-claimable-as-dependent", "eic.spouse-valid-ssn",
           "eic.taxpayer-valid-ssn", "eic.not-nonresident-alien", "eic.not-qualifying-child-of-another",
           "eic.no-unsupported-situations", "eic.not-married", "eic.separated-spouse", "eic.no-qualifying-child",
           "standard-deduction.can-be-claimed-as-dependent", "taxpayer-over-65", "spouse-over-65",
           "senior-deduction.spouse-valid-ssn", "filing-status")


def recorded() -> dict[str, Any]:
    from tools import recorded_replay as rr

    lists = rr.recorded_lists()
    carried: dict[str, Counter] = {f: Counter() for f in TRACKED}
    sd_vs_dep: Counter = Counter()
    over65_vs_age: Counter = Counter()
    for _key, acts in lists:
        last: dict[str, Any] = {}
        for act in acts:
            payload = act.get("payload") or {}
            finding = payload.get("finding") or (payload.get("member") or {}).get("finding") or {}
            fid = str(finding.get("fact_id", ""))
            fact = fid.split("|", 1)[0].removeprefix(P)
            if fact in carried:
                last[fact] = finding.get("value")
        for fact in TRACKED:
            carried[fact][str(last[fact]) if fact in last else "absent"] += 1
        sd_vs_dep[f"sd-can-be-claimed={last.get('standard-deduction.can-be-claimed-as-dependent', 'absent')} / "
                  f"eic-not-claimable={last.get('eic.not-claimable-as-dependent', 'absent')}"] += 1
        over65_vs_age[f"taxpayer-over-65={last.get('taxpayer-over-65', 'absent')} / "
                      f"eic-age-25-under-65={last.get('eic.age-25-under-65', 'absent')}"] += 1
    return {"lists": len(lists), "last_value_by_fact": {f: dict(c.most_common()) for f, c in carried.items()},
            "standard_deduction_dependent_vs_eic_not_claimable": dict(sd_vs_dep.most_common()),
            "over_65_vs_eic_age": dict(over65_vs_age.most_common())}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--recorded", action="store_true")
    parser.add_argument("--out")
    args = parser.parse_args()
    body = {"static": static()}
    if args.recorded:
        body["recorded"] = recorded()
    text = json.dumps(body, indent=1) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    print(text[:12000])


if __name__ == "__main__":
    main()
