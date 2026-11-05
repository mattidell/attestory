"""Scratch prototype for the round-one question design.

Evidence only. Does not edit package content or the runner on disk.
Installs an in-process patch on the runner's blocked-row recording.

Two layers, selected with --mode:

- closures: unconditional closure families only. This is the content shape.
  A pure require_closed guard is recorded with the missing requires, including
  on the unreached-rule path, which does not go through _record_blocked.
  A sibling family in the same all or the same count comparison is recorded
  when that comparison raises.
- full: closures, plus a withholding ref that sits in a later arm of any
  when an earlier arm blocked and one of the compared sets already has a
  member. That second step is evaluator behavior. It is not a content
  successor. It runs only when the expression is evaluated, so a rule still
  blocked on requires does not gain the ref.

Writes prototype-output.json beside this file. Synthetic demo.* runs only.
"""

from __future__ import annotations

import argparse
import json
from typing import Any

import probe
from packages.derivation.runner import _Run

HERE = probe.HERE
OUTPUT = HERE / "prototype-output.json"
CHECK = ".aq-check"

ACTIVE = False
MODE = "full"
FAMILY_SENTENCE: dict[str, str] = {}
QUESTION_SYMBOLS: set[str] = set()
_ORIGINAL = _Run._record_blocked
_ORIGINAL_FINALIZE = _Run.finalize_unreached


def _op(node: Any) -> str | None:
    return node.get("op") if isinstance(node, dict) else None


def _children(node: dict[str, Any]) -> list[Any]:
    return [value for key, value in node.items() if key != "op"]


def mentions_family(node: Any, families: set[str]) -> bool:
    if isinstance(node, list):
        return any(mentions_family(item, families) for item in node)
    if not isinstance(node, dict) or "op" not in node:
        return False
    op = node["op"]
    if op in ("require_closed", "count") and node.get("source_set") in families:
        return True
    if op == "choose":
        return mentions_family(node.get("when"), families)
    if op == "conditional_dependency_set":
        return mentions_family(node.get("condition"), families)
    return any(mentions_family(value, families) for value in _children(node))


def question_refs(node: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(node, list):
        for item in node:
            found |= question_refs(item)
        return found
    if not isinstance(node, dict) or "op" not in node:
        return found
    op = node["op"]
    if op == "ref":
        name = str(node.get("name"))
        if name in QUESTION_SYMBOLS:
            found.add(name)
        return found
    if op == "choose":
        return found
    if op == "conditional_dependency_set":
        if node.get("condition") is True:
            for member in node.get("members") or []:
                found |= question_refs(member)
        return found
    for value in _children(node):
        found |= question_refs(value)
    return found


def _count_has_members(node: Any, sources: dict[str, Any]) -> bool:
    if isinstance(node, list):
        return any(_count_has_members(item, sources) for item in node)
    if not isinstance(node, dict) or "op" not in node:
        return False
    if node["op"] == "count":
        return bool(sources.get(node.get("name")))
    if node["op"] == "choose":
        return _count_has_members(node.get("when"), sources)
    return any(_count_has_members(value, sources) for value in _children(node))


def later_any_refs(node: Any, raised: set[str], sources: dict[str, Any]) -> set[str]:
    """Withholding refs in a later any-arm, and only when a compared set has members."""
    found: set[str] = set()
    if isinstance(node, list):
        for item in node:
            found |= later_any_refs(item, raised, sources)
        return found
    if not isinstance(node, dict) or "op" not in node:
        return found
    op = node["op"]
    if op == "choose":
        return later_any_refs(node.get("when"), raised, sources)
    if op == "conditional_dependency_set":
        return later_any_refs(node.get("condition"), raised, sources)
    if op == "any":
        args = node.get("args") or []
        hit = next((index for index, arg in enumerate(args) if mentions_family(arg, raised)), None)
        if hit is not None and _count_has_members(args[hit], sources):
            for arg in args[hit + 1 :]:
                found |= question_refs(arg)
    for value in _children(node):
        found |= later_any_refs(value, raised, sources)
    return found


def sibling_families(node: Any, raised: set[str]) -> set[str]:
    """Other families in the same all(require_closed) or the same count comparison."""
    found: set[str] = set()
    if isinstance(node, list):
        for item in node:
            found |= sibling_families(item, raised)
        return found
    if not isinstance(node, dict) or "op" not in node:
        return found
    op = node["op"]
    if op == "choose":
        return sibling_families(node.get("when"), raised)
    if op == "conditional_dependency_set":
        return sibling_families(node.get("condition"), raised)
    if op == "all":
        args = node.get("args") or []
        families = [arg.get("source_set") for arg in args if _op(arg) == "require_closed"]
        if any(family in raised for family in families):
            found.update(family for family in families if isinstance(family, str))
    if op == "compare":
        sides = [node.get("left"), node.get("right")]
        if all(_op(side) == "count" for side in sides):
            families = [side.get("source_set") for side in sides]
            if any(family in raised for family in families):
                found.update(family for family in families if isinstance(family, str))
    for value in _children(node):
        found |= sibling_families(value, raised)
    return found


def pure_closure(node: Any) -> bool:
    if node is True:
        return True
    if not isinstance(node, dict) or "op" not in node:
        return False
    op = node["op"]
    if op == "require_closed":
        return True
    if op in ("all", "any"):
        return all(pure_closure(arg) for arg in (node.get("args") or []))
    return False


def closure_families(node: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(node, list):
        for item in node:
            found |= closure_families(item)
        return found
    if not isinstance(node, dict) or "op" not in node:
        return found
    if node["op"] == "require_closed" and isinstance(node.get("source_set"), str):
        found.add(node["source_set"])
    for value in _children(node):
        found |= closure_families(value)
    return found


def _extras(rule: dict[str, Any], code: str, missing: list[str], sources: dict[str, Any], closed: set[str]) -> tuple[set[str], set[str]]:
    raised = set(missing)
    bodies = [rule.get("when"), rule.get("value")]
    families: set[str] = set()
    refs: set[str] = set()
    if code == "SOURCE_SET_UNCLOSED":
        for body in bodies:
            families |= sibling_families(body, raised)
            if MODE == "full":
                refs |= later_any_refs(body, raised, sources)
    elif code == "DEPENDENCY_ABSENT" and pure_closure(rule.get("when")):
        families |= closure_families(rule.get("when"))
    families = {
        family
        for family in families
        if family in FAMILY_SENTENCE and family not in closed and family not in raised
    }
    refs = {
        name
        for name in refs
        if name in QUESTION_SYMBOLS and name not in raised
    }
    return families, refs


def _check_row(rule_id: str, pins: list[Any], family: str) -> dict[str, Any]:
    return {
        "artifact_id": rule_id,
        "disposition": "blocked",
        "pins": list(pins),
        "code": "SOURCE_SET_UNCLOSED",
        "missing": [family],
        "symbol": family + CHECK,
    }


def _augment(self: _Run, rule: dict[str, Any], code: str, missing: list[str]) -> None:
    if not self.dispositions:
        return
    row = self.dispositions[-1]
    if row.get("artifact_id") != rule.get("id") or row.get("disposition") != "blocked":
        return
    closed = set(getattr(self, "admissions", {}))
    sources = getattr(self, "sources", {})
    present = set(getattr(self, "symbols", {}))
    families, refs = _extras(rule, code, missing, sources, closed)
    refs = {name for name in refs if name not in present}
    if not families and not refs:
        return
    pins = list(row.get("pins") or [])
    rule_id = str(rule["id"])
    if code == "SOURCE_SET_UNCLOSED" and not refs:
        row["missing"] = list(missing) + sorted(families)
    else:
        original_families = list(missing) if code == "SOURCE_SET_UNCLOSED" else []
        if any(family not in FAMILY_SENTENCE for family in original_families):
            if families and code == "SOURCE_SET_UNCLOSED":
                row["missing"] = list(missing) + sorted(families)
            return
        checks = []
        for family in sorted(set(original_families) | families):
            checks.append(family + CHECK)
            self.dispositions.append(_check_row(rule_id, pins, family))
        added = checks + sorted(refs)
        base = list(missing) if code == "DEPENDENCY_ABSENT" else []
        row["code"] = "DEPENDENCY_ABSENT"
        row["missing"] = base + added
    if self.blocked and self.blocked[-1].get("artifact_id") == rule_id:
        self.blocked[-1]["code"] = row["code"]
        self.blocked[-1]["missing"] = list(row["missing"])


def _patched(self: _Run, rule: dict[str, Any], access: Any, code: str, missing: list[str]) -> None:
    _ORIGINAL(self, rule, access, code, missing)
    if ACTIVE:
        _augment(self, rule, code, missing)


def _augment_requires_blocks(self: _Run) -> None:
    """The unreached-rule path records a missing requires list without _record_blocked.

    A pure require_closed guard on that rule is the content case: the successor
    puts a closure-check symbol in requires, and this pass records the same cause.
    """
    rules = {rule["id"]: rule for rule in self.ctx.rules}
    closed = set(getattr(self, "admissions", {}))
    for row in list(self.dispositions):
        if row.get("disposition") != "blocked" or row.get("code") != "DEPENDENCY_ABSENT":
            continue
        if str(row.get("symbol") or "").endswith(CHECK):
            continue
        missing = [str(item) for item in row.get("missing") or []]
        if any(item.endswith(CHECK) for item in missing):
            continue
        rule = rules.get(row.get("artifact_id"))
        if rule is None or not pure_closure(rule.get("when")):
            continue
        families = {
            family
            for family in closure_families(rule.get("when"))
            if family in FAMILY_SENTENCE and family not in closed
        }
        if not families:
            continue
        pins = list(row.get("pins") or [])
        checks = []
        for family in sorted(families):
            checks.append(family + CHECK)
            self.dispositions.append(_check_row(str(rule["id"]), pins, family))
        row["missing"] = missing + checks


def _patched_finalize(self: _Run) -> None:
    _ORIGINAL_FINALIZE(self)
    if ACTIVE:
        _augment_requires_blocks(self)


def install(catalog: dict[str, Any]) -> None:
    global FAMILY_SENTENCE, QUESTION_SYMBOLS
    FAMILY_SENTENCE = catalog["family_sentence"]
    QUESTION_SYMBOLS = set(catalog["question_symbols"])
    _Run._record_blocked = _patched  # type: ignore[method-assign]
    _Run.finalize_unreached = _patched_finalize  # type: ignore[method-assign]


def _public(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "round": item["round"],
        "new": item["new"],
        "sentences": len(item["sentences"]),
        "question_lines": item["question_lines"],
        "blocked_rules": item["blocked_rules"],
        "answers_added": len(item["answers_added"]),
    }


def _leftover(item: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in item.get("blocked") or []:
        missing = [probe.short(name) for name in row.get("missing") or [] if not str(name).endswith(CHECK)]
        if str(row.get("symbol") or "").endswith(CHECK):
            continue
        rows.append({
            "rule": probe.short(str(row.get("artifact_id"))),
            "code": row.get("code"),
            "missing": missing[:8],
        })
    return rows


def run_scenario(name: str, mode: str, persona: list[dict[str, Any]], catalog: dict[str, Any]) -> dict[str, Any]:
    result = probe.loop_scenario(name, mode, persona, catalog)
    hidden = probe.classify(result, catalog)
    return {
        "name": name,
        "rounds_with_questions": result["rounds_with_questions"],
        "stop": result["stop"],
        "rounds": [_public(item) for item in result["rounds"]],
        "hidden": [
            {
                "round": item["round"],
                "classification": item["classification"],
                "mechanism": item["mechanism"],
                "rule": item["rule"],
                "question": item["question"],
            }
            for item in hidden
        ],
        "headline": probe.headline(result["final_values"]),
        "leftover_blocked": _leftover(result["rounds"][-1]) if result["rounds"] else [],
    }


def persona_values(persona: list[dict[str, Any]], name: str) -> dict[str, Any]:
    payload = probe.run_acts(persona, f"demo.aq.{name}.persona-{MODE}")
    return payload["values"]


def differ(left: dict[str, Any], right: dict[str, Any]) -> list[str]:
    keys = set(left) | set(right)
    return sorted(probe.short(key) for key in keys if left.get(key) != right.get(key))


def main() -> None:
    global ACTIVE, MODE
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("full", "closures"), default="full")
    parser.add_argument("--scenario", action="append", default=[])
    parser.add_argument("--dry", action="store_true")
    args = parser.parse_args()
    MODE = args.mode
    catalog = probe.load_catalog()
    install(catalog)
    if args.dry:
        _dry(catalog)
        return
    selected = set(args.scenario) or {name for name, _mode, _persona, _text in probe.SCENARIOS}
    personas = probe.build_personas()
    print("persona baseline", flush=True)
    ACTIVE = False
    baseline = {key: persona_values(value, key) for key, value in personas.items() if key != "base" or True}
    print("persona patched", flush=True)
    ACTIVE = True
    patched = {key: persona_values(value, key + "-patched") for key, value in personas.items()}
    persona_diff = {key: differ(baseline[key], patched[key]) for key in baseline}
    print("persona diffs", {key: len(value) for key, value in persona_diff.items()}, flush=True)
    scenarios = []
    for name, mode, persona_name, _text in probe.SCENARIOS:
        if name not in selected:
            continue
        print("scenario", name, MODE, flush=True)
        scenarios.append(run_scenario(name, mode, personas[persona_name], catalog))
    payload = {
        "mode": MODE,
        "persona_scalar_diffs": persona_diff,
        "scenarios": scenarios,
    }
    if OUTPUT.is_file() and args.scenario:
        previous = json.loads(OUTPUT.read_text(encoding="utf-8"))
        kept = [row for row in previous.get("scenarios") or [] if row.get("name") not in selected or previous.get("mode") != MODE]
        # One file holds the latest full run. A partial rerun replaces those scenarios.
        if previous.get("mode") == MODE:
            payload["scenarios"] = kept + scenarios
            payload["persona_scalar_diffs"] = previous.get("persona_scalar_diffs") or persona_diff
    OUTPUT.write_text(json.dumps(probe.scrub_tree(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for row in scenarios:
        print(row["name"], "rounds", row["rounds_with_questions"], "stop", row["stop"], "leftover", len(row["leftover_blocked"]))


def _dry(catalog: dict[str, Any]) -> None:
    wanted = (
        "tax.us.2025.rule.form1040-line25a",
        "tax.us.2025.rule.schedule-d-line1a-gain",
        "tax.us.2025.rule.f1099b-covered-w-st-basis-subtotal",
        "tax.us.2025.rule.form1040-line25b",
        "tax.us.2025.rule.form1040-line12e",
        "tax.us.2025.rule.form1040-line36",
        "tax.us.2025.rule.w2-box4-total",
        "tax.us.2025.rule.schedule3-line1-direct-ftc",
    )
    wages = "tax.us.2025.w2.box1-wages"
    for rule_id in wanted:
        rule = catalog["rules"][rule_id]
        print("\n", probe.short(rule_id))
        for code, missing, sources in (
            ("SOURCE_SET_UNCLOSED", ["tax.us.2025.w2-box2"], {wages: [1]}),
            ("DEPENDENCY_ABSENT", ["tax.us.2025.f1099b.covered-st-proceeds-subtotal"], {}),
            ("DEPENDENCY_ABSENT", ["tax.us.2025.f1099b.covered-w-st.member-validation"], {}),
            ("SOURCE_SET_UNCLOSED", ["tax.us.2025.f1099div.b4"], {"tax.us.2025.f1099div.box1a-ordinary": [1]}),
        ):
            families, refs = _extras(rule, code, missing, sources, set())
            if families or refs:
                print(" ", code, [probe.short(item) for item in missing])
                print("   families", sorted(probe.short(item) for item in families))
                print("   refs", sorted(probe.short(item) for item in refs))


if __name__ == "__main__":
    main()
