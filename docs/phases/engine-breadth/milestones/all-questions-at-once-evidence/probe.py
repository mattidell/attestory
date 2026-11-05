"""P0 probe: how many answer rounds a core v75 return takes.

Evidence only. Synthetic demo.* facts. Writes probe-output.json beside this file.
Does not modify package content. No absolute paths in the output.

A round runs live_coordinate_run, reads the question sentences on blocked lines,
and answers exactly those sentences from a complete persona. The next round
shows whatever that answer revealed.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import time
import traceback
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

_HERE = Path(__file__).resolve().parent
for _candidate in _HERE.parents:
    if (_candidate / "packages" / "derivation" / "live.py").is_file():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from tests import test_collect_closure as cc
from tests.helpers import current_core_returns as c
from tests.test_form_1099_k_income import _handover
from tests.test_form_1099_withholding import YEAR
from tests.test_refund_or_amount_owed_track1 import _finish

HERE = Path(__file__).resolve().parent
ROOT = next(path for path in HERE.parents if (path / "packages" / "derivation" / "live.py").is_file())
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
RELEASE_DIR = ROOT / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
OUTPUT = HERE / "probe-output.json"
P = "tax.us.2025."
CORE = (
    "package.core-calculations.v75.json",
    "v75",
    "published-packages.v73.json",
    "demo.release.sli-worksheet-integration.2025.v73.json",
    "v73",
)
MAX_ROUNDS = 8


def scrub(text: str) -> str:
    text = text.replace(str(ROOT), ".")
    text = re.sub(r"/(?:Users|private|tmp|var)/\S+", "<path>", text)
    return text


def scrub_tree(node: Any) -> Any:
    if isinstance(node, str):
        return scrub(node)
    if isinstance(node, dict):
        return {str(key): scrub_tree(value) for key, value in node.items()}
    if isinstance(node, list):
        return [scrub_tree(value) for value in node]
    return node


def short(identifier: str) -> str:
    return identifier.replace(P, "")


def load_catalog() -> dict[str, Any]:
    package = json.loads((CONTENT / CORE[0]).read_text(encoding="utf-8"))
    index: dict[tuple[str, str], dict[str, Any]] = {}
    for path in CONTENT.glob("*.json"):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if isinstance(body, dict) and "id" in body and "version" in body:
            index[(body["id"], body["version"])] = body
    members = [index[(row["id"], row["version"])] for row in package["members"]]
    fact_types: dict[str, dict[str, Any]] = {}
    rules: dict[str, dict[str, Any]] = {}
    for member in members:
        for fact_type in member.get("fact_types") or []:
            fact_types[fact_type["id"]] = fact_type
        if isinstance(member.get("id"), str):
            rules[member["id"]] = member
    fact_sentence: dict[str, str] = {}
    number_facts: set[str] = set()
    scope_facts: set[str] = set()
    for member in members:
        if not str(member.get("schema", "")).startswith("input-question."):
            continue
        fact_id = str(member["fact_type"]["id"])
        fact_sentence[fact_id] = str(member["question"])
        if fact_types[fact_id]["value_schema"].get("type") == "number":
            number_facts.add(fact_id)
        else:
            scope_facts.add(fact_id)
    closure_sentence: dict[str, str] = {}
    closure_family: dict[str, str] = {}
    family_sentence: dict[str, str] = {}
    for member in members:
        if not str(member.get("schema", "")).startswith("source-closure-mapping."):
            continue
        fact_id = str(member["closure_fact_type"]["id"])
        family_id = str(member["family"]["id"])
        question = str(member.get("closure_question") or "")
        closure_sentence[fact_id] = question
        closure_family[fact_id] = family_id
        family_sentence[family_id] = question
    symbol_fact: dict[str, str] = {}
    for binding in package.get("input_bindings") or []:
        fact = binding.get("fact_type") or {}
        symbol = binding.get("symbol")
        fact_id = fact.get("id")
        if isinstance(symbol, str) and isinstance(fact_id, str):
            symbol_fact[symbol] = fact_id
    sentence_targets: dict[str, set[str]] = {}
    for fact_id, sentence in fact_sentence.items():
        sentence_targets.setdefault(sentence, set()).add(fact_id)
    for symbol, fact_id in symbol_fact.items():
        sentence = fact_sentence.get(fact_id)
        if sentence:
            sentence_targets.setdefault(sentence, set()).add(symbol)
    for family_id, sentence in family_sentence.items():
        sentence_targets.setdefault(sentence, set()).add(family_id)
    question_symbols = set(fact_sentence) | {
        symbol for symbol, fact_id in symbol_fact.items() if fact_id in fact_sentence
    }
    return {
        "fact_sentence": fact_sentence,
        "number_facts": number_facts,
        "scope_facts": scope_facts,
        "closure_sentence": closure_sentence,
        "closure_family": closure_family,
        "family_sentence": family_sentence,
        "sentence_targets": sentence_targets,
        "question_symbols": question_symbols,
        "rules": rules,
    }


def findings_of(act: dict[str, Any]) -> list[dict[str, Any]]:
    payload = act.get("payload") or {}
    found: list[dict[str, Any]] = []
    finding = payload.get("finding") if isinstance(payload, dict) else None
    if isinstance(finding, dict):
        found.append(finding)
    member = payload.get("member") if isinstance(payload, dict) else None
    if isinstance(member, dict) and isinstance(member.get("finding"), dict):
        found.append(member["finding"])
    return found


def fact_type_of(finding: dict[str, Any]) -> str:
    return str(finding.get("fact_id", "")).split("|", 1)[0]


def act_fact_types(act: dict[str, Any]) -> set[str]:
    return {fact_type_of(finding) for finding in findings_of(act)}


def act_sentences(act: dict[str, Any], catalog: dict[str, Any]) -> set[str]:
    sentences: set[str] = set()
    for fact_type in act_fact_types(act):
        sentence = catalog["fact_sentence"].get(fact_type) or catalog["closure_sentence"].get(fact_type)
        if sentence:
            sentences.add(sentence)
    return sentences


def withhold(persona: list[dict[str, Any]], catalog: dict[str, Any], mode: str) -> set[int]:
    """Indexes of persona acts that are present at the start of the loop."""
    kept: set[int] = set()
    for index, act in enumerate(persona):
        fact_types = act_fact_types(act)
        drop = False
        if mode == "scope":
            drop = any(fact_type in catalog["scope_facts"] for fact_type in fact_types)
        elif mode == "amounts":
            drop = any(
                fact_type in catalog["number_facts"] or fact_type in catalog["closure_sentence"]
                for fact_type in fact_types
            )
        elif mode == "empty":
            drop = any(
                fact_type in catalog["scope_facts"]
                or fact_type in catalog["number_facts"]
                or fact_type in catalog["closure_sentence"]
                for fact_type in fact_types
            )
        else:
            raise KeyError(mode)
        if not drop:
            kept.add(index)
    return kept


def materialize(persona: list[dict[str, Any]], indexes: set[int]) -> list[dict[str, Any]]:
    acts = [copy.deepcopy(persona[index]) for index in sorted(indexes)]
    return c._renumbered(acts)


def line_questions(model: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for section in model.get("sections") or []:
        resolved = section.get("resolved") or {}
        if resolved.get("disposition") != "blocked":
            continue
        field = section.get("field") or {}
        reasons = resolved.get("reasons") or []
        sentences = [
            str(reason["sentence"])
            for reason in reasons
            if isinstance(reason, dict) and isinstance(reason.get("sentence"), str)
        ]
        rows.append({
            "line": str(field.get("line") or field.get("id")),
            "sentences": sentences,
        })
    return rows


def scalar_publications(outcome: Any) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for item in outcome.publications or ():
        symbol = str(item.finding.get("symbol"))
        value = item.finding.get("value")
        if isinstance(value, (str, int, float, bool)) or value is None:
            values[symbol] = value
    return values


def run_acts(acts: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
    package_name, package_version, registry_name, release_name, release_version = CORE
    surface = PublicationSurface(RELEASE_DIR, CONTENT / registry_name, CONTENT)
    finished = _handover(
        _finish(
            copy.deepcopy(acts),
            package_path=CONTENT / package_name,
            package_version=package_version,
            release_path=RELEASE_DIR / release_name,
            release_version=release_version,
            note=run_id,
        ),
        surface=surface,
        reconfirm=True,
    )
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=finished,
            workspace_revision=len(finished),
            run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=c.USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            raise AssertionError(scrub(f"{run_id} refused: {outcome.refusal.reason} {outcome.refusal.detail}"))
        assert outcome.output_path is not None and outcome.presentation_path is not None
        report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
        model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
        blocked = []
        for row in report.get("dispositions") or []:
            if row.get("disposition") != "blocked":
                continue
            blocked.append({
                "artifact_id": str(row.get("artifact_id")),
                "code": row.get("code"),
                "missing": [str(item) for item in row.get("missing") or []],
            })
        return {
            "lines": line_questions(model),
            "blocked": blocked,
            "values": scalar_publications(outcome),
        }


def answer(indexes: set[int], persona: list[dict[str, Any]], sentences: set[str], catalog: dict[str, Any]) -> list[str]:
    added: list[str] = []
    for index, act in enumerate(persona):
        if index in indexes:
            continue
        if act_sentences(act, catalog) & sentences:
            indexes.add(index)
            added.extend(sorted(short(fact_type) for fact_type in act_fact_types(act)))
    return added


def headline(values: dict[str, Any]) -> dict[str, Any]:
    wanted = (
        "income.agi",
        "income.taxable-income",
        "tax.line16",
        "tax.line24",
        "payments.line25d",
        "payments.line33",
        "payments.line34",
        "payments.line35a-refunded",
        "payments.line37-amount-owed",
        "schedule-d.line-1a-gain",
        "schedule-d.line-7",
        "schedule3.line1-direct-ftc",
        "schedule-a.line-8a",
        "ctc.sch8812.line-21",
    )
    found: dict[str, Any] = {}
    by_short = {short(symbol): value for symbol, value in values.items()}
    for name in wanted:
        if name in by_short:
            found[name] = by_short[name]
    return found


def loop_scenario(name: str, mode: str, persona: list[dict[str, Any]], catalog: dict[str, Any]) -> dict[str, Any]:
    indexes = withhold(persona, catalog, mode)
    shown: set[str] = set()
    rounds: list[dict[str, Any]] = []
    stop = "round-cap"
    final_values: dict[str, Any] = {}
    for number in range(1, MAX_ROUNDS + 1):
        started = time.monotonic()
        payload = run_acts(materialize(persona, indexes), f"demo.aq.{name}.r{number}")
        elapsed = round(time.monotonic() - started, 1)
        lines = payload["lines"]
        sentences = sorted({sentence for line in lines for sentence in line["sentences"]})
        new = [sentence for sentence in sentences if sentence not in shown]
        question_lines = sum(1 for line in lines if line["sentences"])
        generic_lines = sum(1 for line in lines if not line["sentences"])
        print(
            f"{name} round {number}: questions {len(sentences)} new {len(new)} "
            f"lines {question_lines} generic {generic_lines} blocked-rules {len(payload['blocked'])} "
            f"{elapsed}s",
            flush=True,
        )
        record = {
            "round": number,
            "sentences": sentences,
            "new": new,
            "question_lines": question_lines,
            "generic_lines": generic_lines,
            "blocked_lines": len(lines),
            "blocked_rules": len(payload["blocked"]),
            "seconds": elapsed,
            "blocked": payload["blocked"],
        }
        final_values = payload["values"]
        if not sentences:
            record["answers_added"] = []
            rounds.append(record)
            stop = "no-filer-question"
            break
        if number > 1 and not new:
            record["answers_added"] = []
            rounds.append(record)
            stop = "nothing-new"
            break
        added = answer(indexes, persona, set(sentences), catalog)
        record["answers_added"] = added
        rounds.append(record)
        shown.update(sentences)
        if not added:
            stop = "could-not-answer"
            break
    else:
        stop = "round-cap"
    with_questions = sum(1 for item in rounds if item["sentences"])
    return {
        "rounds": rounds,
        "rounds_with_questions": with_questions,
        "stop": stop,
        "final_values": final_values,
        "withheld_acts": len(persona) - len(indexes) + sum(len(item["answers_added"]) for item in rounds),
    }


def value_dependent(node: Any) -> bool:
    if isinstance(node, list):
        return any(value_dependent(item) for item in node)
    if not isinstance(node, dict):
        return False
    if node.get("op") in ("categorical_compare", "choose"):
        return True
    return any(value_dependent(value) for value in node.values())


def occurrences(rule: dict[str, Any]) -> list[tuple[str, str, str]]:
    found: list[tuple[str, str, str]] = []

    def walk(node: Any, ctx: str) -> None:
        if isinstance(node, list):
            for item in node:
                walk(item, ctx)
            return
        if not isinstance(node, dict) or "op" not in node:
            return
        op = node["op"]
        if op == "ref":
            found.append((ctx, "ref", str(node.get("name"))))
            return
        if op == "require_closed":
            found.append((ctx, "require_closed", str(node.get("source_set"))))
            return
        if op in ("collect", "count"):
            if node.get("source_set"):
                found.append((ctx, "source_set", str(node["source_set"])))
            if node.get("name"):
                found.append((ctx, "collect", str(node["name"])))
        if op == "choose":
            walk(node.get("when"), ctx + "/choose-when")
            walk(node.get("then"), ctx + "/choose-then")
            walk(node.get("else"), ctx + "/choose-else")
            return
        if op == "conditional_dependency_set":
            walk(node.get("condition"), ctx + "/cond")
            member_ctx = ctx + ("/cond-member-true" if node.get("condition") is True else "/cond-member")
            for member in node.get("members") or []:
                walk(member, member_ctx)
            return
        if op == "all":
            for index, arg in enumerate(node.get("args") or []):
                walk(arg, f"{ctx}/all[{index}]")
            return
        if op == "any":
            for index, arg in enumerate(node.get("args") or []):
                walk(arg, f"{ctx}/any[{index}]")
            return
        for key, value in node.items():
            if key != "op":
                walk(value, ctx)

    for req in rule.get("requires") or []:
        found.append(("requires", "requires", str(req)))
    walk(rule.get("when"), "when")
    walk(rule.get("value"), "value")
    return found


def _conditional(ctx: str) -> bool:
    if "choose-then" in ctx or "choose-else" in ctx:
        return True
    if "/cond-member" in ctx and "cond-member-true" not in ctx:
        return True
    if "/any[" in ctx and not ctx.endswith("/any[0]"):
        return True
    return False


def label_mechanism(
    rule: dict[str, Any] | None, targets: set[str]
) -> tuple[str, str, list[str]]:
    if rule is None:
        return "no rule body", "unknown", []
    hits = [item for item in occurrences(rule) if item[2] in targets]
    contexts = sorted({item[0] for item in hits})
    if not hits:
        return "static requires checked after another", "knowable", contexts
    if all(_conditional(item[0]) for item in hits):
        if any("choose-then" in item[0] or "choose-else" in item[0] for item in hits):
            return "choose branch", "conditional", contexts
        return "guard", "conditional", contexts
    if any(item[0] == "requires" for item in hits):
        return "static requires checked after another", "knowable", contexts
    if any(item[1] == "require_closed" or "/all[" in item[0] for item in hits):
        return "guard", "knowable", contexts
    if any(item[0].startswith("value") for item in hits) and value_dependent(rule.get("when")):
        if not any(item[0].startswith("when") or item[0] == "requires" for item in hits):
            return "guard", "conditional", contexts
    if any(item[1] == "ref" for item in hits):
        return "raised ref inside an expression", "knowable", contexts
    return "unclassified", "unknown", contexts


def classify(scenario: dict[str, Any], catalog: dict[str, Any]) -> list[dict[str, Any]]:
    rounds = scenario["rounds"]
    if not rounds:
        return []
    shown: set[str] = set()
    round1_rows = rounds[0]["blocked"]
    round1_missing: dict[str, set[str]] = {}
    for row in round1_rows:
        round1_missing.setdefault(row["artifact_id"], set()).update(row["missing"])
    hidden: list[dict[str, Any]] = []
    rules = catalog["rules"]
    for index, item in enumerate(rounds):
        new = [sentence for sentence in item["sentences"] if sentence not in shown]
        if index == 0:
            shown.update(item["sentences"])
            continue
        prior = {row["artifact_id"]: row for row in rounds[index - 1]["blocked"]}
        for sentence in new:
            targets = catalog["sentence_targets"].get(sentence, set())
            recorded_early = sorted(
                short(rule_id)
                for rule_id, missing in round1_missing.items()
                if missing & targets
            )
            revealers = []
            for row in item["blocked"]:
                hit = sorted(short(name) for name in row["missing"] if name in targets)
                if hit:
                    revealers.append((row, hit))
            if recorded_early:
                rule_id = next(rule for rule, missing in round1_missing.items() if missing & targets)
                mechanism, kind, contexts = "projection", "knowable", []
                rule = rules.get(rule_id)
                if rule is not None:
                    _mechanism, _kind, contexts = label_mechanism(rule, targets)
            else:
                chosen = None
                for row, _hit in revealers:
                    previous = prior.get(row["artifact_id"])
                    if previous is not None and not (set(previous["missing"]) & targets):
                        chosen = row
                        break
                if chosen is None and revealers:
                    chosen = revealers[0][0]
                rule_id = chosen["artifact_id"] if chosen is not None else ""
                rule = rules.get(rule_id)
                mechanism, kind, contexts = label_mechanism(rule, targets)
                if chosen is not None and rule_id not in prior:
                    if mechanism == "raised ref inside an expression":
                        mechanism = "static requires checked after another"
            previous = prior.get(rule_id, {})
            hidden.append({
                "question": sentence,
                "round": item["round"],
                "rule": short(rule_id) if rule_id else "",
                "mechanism": mechanism,
                "classification": kind,
                "contexts": contexts,
                "prior_code": previous.get("code"),
                "prior_missing": [short(name) for name in previous.get("missing") or []][:12],
                "recorded_in_round_one": recorded_early[:8],
            })
        shown.update(item["sentences"])
    return hidden


def persona_1099b() -> list[dict[str, Any]]:
    acts = c.base_return()
    c._set_answer(acts, P + "exception1.only-box2a-capital-gains", "no")
    acts = cc._add_member(acts, P + "f1099b.covered-st-proceeds", 1000.0, close=True, tag="aq-st-p")
    acts = cc._add_member(acts, P + "f1099b.covered-st-basis", 800.0, close=True, tag="aq-st-b")
    return c._renumbered(acts)


def build_personas() -> dict[str, list[dict[str, Any]]]:
    base = c.base_return()
    return {
        "base": base,
        "mortgage": c.add_mortgage_itemizer(copy.deepcopy(base), 8400.0),
        "form-1099b": persona_1099b(),
        "dependent": c.part_ii_b_return(box4=300.0, box6=200.0),
        "foreign-tax": c.add_foreign_tax_1099div(copy.deepcopy(base), [30.0]),
    }


SCENARIOS = (
    ("scope-withheld", "scope", "base",
     "Every categorical scope answer withheld. Amount answers and closures stay."),
    ("amounts-open", "amounts", "base",
     "Every numeric input-question withheld and every source family left open. Scope answers stay."),
    ("mortgage-empty", "empty", "mortgage",
     "Mortgage return with every filer question and every closure withheld. The Form 1098 statement stays."),
    ("form-1099b-empty", "empty", "form-1099b",
     "Form 1099-B return with every filer question and every closure withheld. The covered sale stays."),
    ("dependent-empty", "empty", "dependent",
     "Dependent return with every filer question and every closure withheld. The children stay."),
    ("foreign-tax-empty", "empty", "foreign-tax",
     "Foreign-tax return with every filer question and every closure withheld. The Form 1099-DIV box 7 statement stays."),
)


def public_round(item: dict[str, Any]) -> dict[str, Any]:
    """Drop the blocked-rule dump from the on-disk round once classification has read it.

    The dump stays available on the in-memory round. The file keeps a count and
    the missing ids that are questions, which is what the note cites.
    """
    return {
        "round": item["round"],
        "sentences": item["sentences"],
        "new": item["new"],
        "question_lines": item["question_lines"],
        "generic_lines": item["generic_lines"],
        "blocked_lines": item["blocked_lines"],
        "blocked_rules": item["blocked_rules"],
        "seconds": item["seconds"],
        "answers_added": item.get("answers_added") or [],
    }


def write_output(payload: dict[str, Any]) -> None:
    OUTPUT.write_text(json.dumps(scrub_tree(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", action="append", default=[])
    args = parser.parse_args()
    selected = set(args.scenario)
    print("loading catalog", flush=True)
    catalog = load_catalog()
    print(
        f"questions {len(catalog['fact_sentence'])} closures {len(catalog['closure_sentence'])} "
        f"scope {len(catalog['scope_facts'])} amounts {len(catalog['number_facts'])}",
        flush=True,
    )
    print("building personas", flush=True)
    personas = build_personas()
    document: dict[str, Any] = {"core": "v75", "scenarios": []}
    if OUTPUT.is_file() and selected:
        previous = json.loads(OUTPUT.read_text(encoding="utf-8"))
        document["scenarios"] = [
            row for row in previous.get("scenarios") or [] if row.get("name") not in selected
        ]
    for name, mode, persona_name, description in SCENARIOS:
        if selected and name not in selected:
            continue
        persona = personas[persona_name]
        print(f"persona {name} acts {len(persona)}", flush=True)
        entry: dict[str, Any] = {"name": name, "mode": mode, "description": description}
        try:
            started = time.monotonic()
            complete = run_acts(persona, f"demo.aq.{name}.persona")
            entry["persona_seconds"] = round(time.monotonic() - started, 1)
            entry["persona_blocked_rules"] = len(complete["blocked"])
            entry["persona_question_lines"] = sum(1 for line in complete["lines"] if line["sentences"])
            entry["persona_generic_lines"] = sum(1 for line in complete["lines"] if not line["sentences"])
            entry["persona_headline"] = headline(complete["values"])
            print(
                f"{name} persona blocked-rules {entry['persona_blocked_rules']} "
                f"questions {entry['persona_question_lines']} {entry['persona_seconds']}s",
                flush=True,
            )
            measured = loop_scenario(name, mode, persona, catalog)
            entry["hidden"] = classify(measured, catalog)
            entry["rounds_with_questions"] = measured["rounds_with_questions"]
            entry["stop"] = measured["stop"]
            entry["headline"] = headline(measured["final_values"])
            entry["persona_value_mismatches"] = sorted(
                short(symbol)
                for symbol in set(complete["values"]) | set(measured["final_values"])
                if complete["values"].get(symbol) != measured["final_values"].get(symbol)
            )
            entry["rounds"] = [public_round(item) for item in measured["rounds"]]
        except Exception as exc:  # one scenario must not drop the others
            entry["error"] = scrub(f"{type(exc).__name__}: {exc}")
            entry["trace"] = scrub(traceback.format_exc())
            print(f"{name} FAILED {entry['error']}", flush=True)
        document["scenarios"].append(entry)
        write_output(document)
    write_output(document)
    print("wrote probe-output.json", flush=True)


if __name__ == "__main__":
    main()
