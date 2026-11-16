"""Reproduce the box 4 amount question on published core v91.

Every case is one live_coordinate_run of synthetic demo.* acts through the
production coordinator and the presentation projection. Age and blindness
are stated false, the answers a filer under 65 who is not blind gives.
Nothing here edits packages/ or tests/.

    python3 probe.py
"""

from __future__ import annotations

import json
import multiprocessing
import os
import re
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tests import evidence_loader  # noqa: E402

OWNER = "b4_amount_p0"
BNQ = REPO / "docs/phases/engine-breadth/milestones/blocked-names-question-evidence"
CONTENT = REPO / "packages/content/tax/2025"
P = "tax.us.2025."
AMOUNT = P + "f1099b.statement-box4-withholding"
REPORTED = P + "f1099b.statement-box4-withholding-reported"
BOX7 = P + "f1099b.statement-box7-loss-not-allowed"
PRESENT = P + "f1099b.no-sale-box4-present"
RETURN_AMT = P + "f1099b.no-sale-box4-withholding"
W2_BOX2 = P + "w2.box2-withholding"
K_BOX4 = P + "f1099k.box4-federal-withholding"
W2G_BOX4 = P + "w2g.box4-withholding"
LINES = (
    "form1040.line-7a", "form1040.line-11a", "form1040.line-15", "form1040.line-16",
    "form1040.line-24", "form1040.line-25a", "form1040.line-25b", "form1040.line-25c",
    "form1040.line-25d", "form1040.line-33", "form1040.line-34", "form1040.line-37",
    "schedule-d.line-1b", "schedule-d.line-7", "schedule-d.line-16",
)


def scrub(text: str) -> str:
    text = text.replace(str(REPO), ".")
    return re.sub(r"/(?:Users|private|tmp|var|opt)/\S+", "<path>", text)


def short(name: Any) -> str:
    return str(name).removeprefix(P + "rule.").removeprefix(P)


def num(value: Any) -> Any:
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, (int, float)):
        return int(value) if float(value).is_integer() else value
    try:
        number = float(value)
    except (TypeError, ValueError):
        return value
    return int(number) if number.is_integer() else number


def _mods() -> tuple[Any, Any]:
    evidence_loader.activate(OWNER)
    common = evidence_loader.load(BNQ / "common.py", "common")
    return common.harness(), evidence_loader.load(BNQ / "probe.py", "probe")


def statements(acts: list[dict[str, Any]]) -> list[str]:
    found: list[str] = []
    for act in acts:
        entity = (act.get("payload") or {}).get("entity") or {}
        if act.get("kind") == "entity-introduced" and entity.get("kind") == "tax.us.f1099b-statement":
            ident = str(entity.get("id"))
            if ident not in found:
                found.append(ident)
    return found


def say_stmt(acts: list[dict[str, Any]], fact: str, statement: str, value: object, tag: str) -> list[dict[str, Any]]:
    h, _probe = _mods()
    fact_id = h.fact_id_for(fact, (("statement", statement), ("tax-year", h.YEAR)))
    kept = []
    for act in acts:
        finding = (act.get("payload") or {}).get("finding")
        if isinstance(finding, dict) and finding.get("fact_id") == fact_id:
            continue
        kept.append(act)
    body = h.bundle_for(fact, h.CONTENT)
    if body is None:
        raise RuntimeError("no bundle for " + short(fact))
    if not {item["id"] for item in body["fact_types"]} & h._adopted(kept):
        h._add(kept, "bundle-adoption", {"bundle": body})
    h._add(kept, "assertion", {"finding": h._attested(f"demo.b4.{tag}.{statement}", fact_id, value)})
    return h.renumber(kept)


def strip_fact(acts: list[dict[str, Any]], fact: str) -> list[dict[str, Any]]:
    h, _probe = _mods()
    prefix = fact + "|"
    kept = []
    for act in acts:
        payload = act.get("payload") or {}
        finding = payload.get("finding") if isinstance(payload, dict) else None
        member = payload.get("member") if isinstance(payload, dict) else None
        member_finding = member.get("finding") if isinstance(member, dict) else None
        current = finding if isinstance(finding, dict) else member_finding
        if isinstance(current, dict) and str(current.get("fact_id") or "").startswith(prefix):
            continue
        kept.append(act)
    return h.renumber(kept)


def person(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Under 65 and not blind. v91 asks both, and a wage return leaves them open."""
    h, _probe = _mods()
    acts = h.say(acts, P + "taxpayer-over-65", False, "age")
    return h.say(acts, P + "taxpayer-blind", False, "blind")


def prepare_covered(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    h, _probe = _mods()
    answers = h.honest({"covered"})
    answers.update(h.honest_exception1(acts))
    acts = h.answer(acts, **{key: value for key, value in answers.items() if value is not None})
    for statement in statements(acts):
        acts = say_stmt(acts, BOX7, statement, "no", "box7")
    return h.say(acts, PRESENT, "no", "present")


def covered(tag: str, *, proceeds: float, basis: float) -> list[dict[str, Any]]:
    h, _probe = _mods()
    acts = h.sale(h.opened(), "covered", "st", proceeds=proceeds, basis=basis, tag=tag)
    return prepare_covered(acts)


def introduce(acts: list[dict[str, Any]], tag: str) -> list[dict[str, Any]]:
    h, _probe = _mods()
    broker, statement = f"demo.sfa.{tag}.broker", f"demo.sfa.{tag}.statement"
    if broker not in h._entities(acts):
        h._introduce(acts, broker, "tax.us.f1099b-broker")
    if statement not in h._entities(acts):
        h._introduce(acts, statement, "tax.us.f1099b-statement")
    return h.renumber(acts)


def box4_of(acts: list[dict[str, Any]]) -> dict[str, Any]:
    reported: list[Any] = []
    amount: list[Any] = []
    present = None
    return_amount = None
    for act in acts:
        payload = act.get("payload") or {}
        finding = payload.get("finding") if isinstance(payload, dict) else None
        if not isinstance(finding, dict):
            continue
        fact = str(finding.get("fact_id") or "").split("|", 1)[0]
        value = finding.get("value")
        if fact == REPORTED:
            reported.append(value)
        elif fact == AMOUNT:
            amount.append(num(value))
        elif fact == PRESENT:
            present = value
        elif fact == RETURN_AMT:
            return_amount = num(value)
    return {"reported": reported, "amount": amount, "present": present, "return_amount": return_amount}


def build_lists() -> list[tuple[str, list[dict[str, Any]], str]]:
    h, probe = _mods()
    codeb = probe.CASES["codeb_amounts_disagree"][1]()
    beside = probe.CASES["codeb_sale_beside_8949_yes"][1]()
    wash = probe.CASES["wash_adjustment_open"][1]()
    codeb_stmt = "demo.sfa.bnq-codeb.statement"
    wash_stmt = "demo.sfa.bnq-sale.statement"
    yes = say_stmt(covered("yes1", proceeds=5000, basis=4000), REPORTED, "demo.sfa.yes1.statement", "yes", "reported")
    no = say_stmt(covered("no1", proceeds=5000, basis=4000), REPORTED, "demo.sfa.no1.statement", "no", "reported")
    open_sale = strip_fact(covered("open1", proceeds=5000, basis=4000), REPORTED)
    two = h.sale(h.opened(), "covered", "st", proceeds=5000, basis=4000, tag="s1")
    two = h.sale(two, "covered", "st", proceeds=3000, basis=2000, tag="s2")
    two = prepare_covered(two)
    two = say_stmt(two, REPORTED, "demo.sfa.s1.statement", "yes", "reported")
    two = say_stmt(two, REPORTED, "demo.sfa.s2.statement", "yes", "reported")
    level = say_stmt(covered("sale1", proceeds=5000, basis=4000), REPORTED, "demo.sfa.sale1.statement", "yes", "reported")
    level = say_stmt(level, AMOUNT, "demo.sfa.sale1.statement", 200, "amount")
    level = h.say(level, PRESENT, "yes", "present")
    level = h.say(level, RETURN_AMT, 150, "return-amount")
    orphan = introduce(covered("sale1", proceeds=5000, basis=4000), "orphan")
    orphan = say_stmt(orphan, REPORTED, "demo.sfa.sale1.statement", "no", "reported")
    orphan = say_stmt(orphan, AMOUNT, "demo.sfa.sale1.statement", 200, "amount")
    orphan = say_stmt(orphan, AMOUNT, "demo.sfa.orphan.statement", 150, "amount")
    orphan = h.say(orphan, PRESENT, "yes", "present")
    orphan = h.say(orphan, RETURN_AMT, 0, "return-amount")
    rows = [
        ("codeb_amounts_disagree", codeb, "Recorded code B sale. Reported no. Amount absent."),
        ("codeb_amounts_disagree_amount0", say_stmt(codeb, AMOUNT, codeb_stmt, 0, "amount"), "Same list with amount 0."),
        ("codeb_sale_beside_8949_yes", beside, "Recorded code B sale. Path B open. Amount absent."),
        ("codeb_sale_beside_8949_yes_amount0", say_stmt(beside, AMOUNT, codeb_stmt, 0, "amount"), "Same list with amount 0."),
        ("wash_adjustment_open", wash, "Recorded wash sale. Adjustment family open. Amount absent."),
        ("wash_adjustment_open_amount0", say_stmt(wash, AMOUNT, wash_stmt, 0, "amount"), "Same list with amount 0."),
        ("sale_box4_yes_no_amount", yes, "One covered sale. Reported yes. Amount absent."),
        ("sale_box4_yes_amount200", say_stmt(yes, AMOUNT, "demo.sfa.yes1.statement", 200, "amount"), "Same sale with amount 200."),
        ("sale_box4_no_no_amount", no, "One covered sale. Reported no. Amount absent."),
        ("sale_box4_no_amount0", say_stmt(no, AMOUNT, "demo.sfa.no1.statement", 0, "amount"), "Reported no and amount 0."),
        ("sale_box4_unanswered", open_sale, "One covered sale. Reported and amount both absent."),
        ("two_statements_one_amount", say_stmt(two, AMOUNT, "demo.sfa.s1.statement", 150, "amount"), "Two sales. s1 amount 150. s2 amount absent."),
        ("two_statements_both", say_stmt(say_stmt(two, AMOUNT, "demo.sfa.s1.statement", 150, "amount"), AMOUNT, "demo.sfa.s2.statement", 40, "amount"), "Amounts 150 and 40."),
        ("beside_return_level", level, "Sale amount 200 beside return-level 150."),
        ("orphan_beside_return_zero", orphan, "Sale 200 and a no-sale statement 150. Return-level 0."),
        ("no_1099b", probe.answered(h.opened()), "No Form 1099-B. Present no."),
        ("w2_box2_stripped", strip_fact(probe.answered(h.opened()), W2_BOX2), "Contrast: W-2 box 2 amount removed."),
    ]
    return [(case_id, person(acts), note) for case_id, acts, note in rows]


def _chain(row: dict[str, Any], by_symbol: dict[str, list[dict[str, Any]]], token: str, seen: set[str] | None = None) -> bool:
    seen = set() if seen is None else seen
    for item in row.get("missing") or []:
        key = str(item)
        if token in key:
            return True
        if key in seen:
            continue
        seen.add(key)
        for child in by_symbol.get(key, []):
            if child.get("disposition") == "blocked" and _chain(child, by_symbol, token, seen):
                return True
    return False


def summarize(outcome: Any, core: Any, sentence: str) -> dict[str, Any]:
    evidence_loader.activate(OWNER)
    common = evidence_loader.load(BNQ / "common.py", "common")
    if outcome.refusal is not None:
        return {"outcome": "refused", "reason": outcome.refusal.reason, "detail": scrub(str(outcome.refusal.detail))[:400]}
    publishes = common.rule_publishes(core)
    report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
    model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
    rows = report.get("dispositions") or []
    by_symbol: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        symbol = row.get("symbol") or publishes.get(str(row.get("artifact_id")))
        if symbol:
            by_symbol.setdefault(str(symbol), []).append(row)
    lines: dict[str, Any] = {}
    amount_fields = []
    page_has = False
    for section in model.get("sections") or []:
        field = section.get("field") or {}
        resolved = section.get("resolved") or {}
        field_id = short(field.get("id"))
        disposition = str(resolved.get("disposition"))
        value = resolved.get("value")
        if field_id in LINES:
            lines[field_id] = disposition if value is None or "blocked" in disposition else num(value)
        reasons = [scrub(str(item.get("sentence") or "").strip()) for item in resolved.get("reasons") or []
                   if isinstance(item, dict) and str(item.get("sentence") or "").strip()]
        if sentence in reasons:
            page_has = True
        if "blocked" not in disposition:
            continue
        symbol = str(field.get("binds_symbol") or "")
        own = [row for row in by_symbol.get(symbol, []) if row.get("disposition") == "blocked"]
        row = own[0] if own else {}
        if not row or not _chain(row, by_symbol, "f1099b.statement-box4-withholding") and not _chain(row, by_symbol, "w2.box2-withholding"):
            continue
        if "box4" not in field_id and "line-25" not in field_id and "line-3" not in field_id and "line-35" not in field_id and "line-37" not in field_id:
            if not _chain(row, by_symbol, "f1099b.statement-box4-withholding"):
                continue
        amount_fields.append({
            "field": field_id,
            "artifact": short(row.get("artifact_id")),
            "code": row.get("code"),
            "missing": [short(item) for item in row.get("missing") or []],
            "amount_sentence": sentence in reasons,
            "reason_count": len(reasons),
            "only_amount_sentence": reasons == [sentence],
        })
    focus = {}
    for symbol in (P + "payments.line25b", P + "payments.line25d", P + "payments.line25a"):
        found = [row for row in by_symbol.get(symbol, [])]
        focus[short(symbol)] = {
            "artifact": short(found[0].get("artifact_id")) if found else None,
            "disposition": found[0].get("disposition") if found else None,
            "code": found[0].get("code") if found else None,
            "missing": [short(item) for item in (found[0].get("missing") or [])] if found else [],
        }
    return {
        "outcome": "success",
        "stop": report.get("stop_reason"),
        "lines": lines,
        "amount_fields": amount_fields,
        "page_has_amount_sentence": page_has,
        "focus": focus,
        "amount_fact_blocked_rows": len([row for row in by_symbol.get(AMOUNT, []) if row.get("disposition") == "blocked"]),
    }


def run_one(case_id: str, acts: list[dict[str, Any]], sentence: str) -> dict[str, Any]:
    evidence_loader.activate(OWNER)
    common = evidence_loader.load(BNQ / "common.py", "common")
    h = common.harness()
    core = h.Core("v91", "v89", "v89")
    surface = core.surface()
    run_id = "demo.b4.p0." + case_id.replace("_", "-")
    try:
        with h.loader_entries(core):
            finished = h._handover(h._finish(
                json.loads(json.dumps(acts)), package_path=core.package_path, package_version=core.version,
                release_path=core.release_path, release_version=core.release_version, note=run_id,
            ), surface=surface, reconfirm=True)
            with tempfile.TemporaryDirectory() as tmp:
                outcome = h.live_coordinate_run(
                    h.WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO, authoritative_acts=finished,
                    workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": h.YEAR},
                    scope_user=h.ccr.USER, request={"schema": "run-request.v1"}, run_id=run_id,
                    governance_pins=[], surface=surface, output_name="out.json")
                return {"id": case_id, "box4": box4_of(acts), **summarize(outcome, core, sentence)}
    except Exception as exc:  # noqa: BLE001
        return {"id": case_id, "outcome": "error", "error": type(exc).__name__, "message": scrub(str(exc))[:500]}
    finally:
        evidence_loader.finish(OWNER)


def _worker(payload: tuple[str, list[tuple[str, list[dict[str, Any]]]]]) -> list[dict[str, Any]]:
    sentence, shard = payload
    out = []
    for case_id, acts in shard:
        out.append(run_one(case_id, acts, sentence))
    return out


def _index(pattern: str) -> dict[tuple[Any, Any], dict[str, Any]]:
    found: dict[tuple[Any, Any], dict[str, Any]] = {}
    for path in CONTENT.glob(pattern):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if isinstance(body, dict) and body.get("id"):
            found[(body.get("id"), body.get("version"))] = body
    return found


def _walk(node: Any, op: str, found: list[dict[str, Any]]) -> None:
    if isinstance(node, dict):
        if node.get("op") == op:
            found.append(node)
        for value in node.values():
            _walk(value, op, found)
    elif isinstance(node, list):
        for value in node:
            _walk(value, op, found)


def _refs(node: Any, name: str) -> bool:
    if isinstance(node, dict):
        if node.get("op") == "ref" and node.get("name") == name:
            return True
        return any(_refs(value, name) for value in node.values())
    if isinstance(node, list):
        return any(_refs(value, name) for value in node)
    return False


def shapes(sentence: str) -> dict[str, Any]:
    package = json.loads((CONTENT / "package.core-calculations.v91.json").read_text(encoding="utf-8"))
    rules = _index("rule*.json")
    questions = _index("input-question*.json")
    closures = _index("closure-mapping*.json")
    fields = _index("*.form-field*.json")
    question_for: dict[str, str] = {}
    for member in package["members"]:
        if not str(member.get("schema", "")).startswith("input-question."):
            continue
        body = questions.get((member.get("id"), member.get("version")))
        fact = ((body or {}).get("fact_type") or {}).get("id")
        if fact:
            question_for[str(fact)] = str(body.get("question") or "")
    closure_for: dict[str, str] = {}
    for member in package["members"]:
        if not str(member.get("schema", "")).startswith("source-closure-mapping."):
            continue
        body = closures.get((member.get("id"), member.get("version"))) or {}
        fact = ((body.get("member_fact_type") or {}).get("id"))
        if fact:
            closure_for[str(fact)] = str(body.get("closure_question") or "")
    visible: dict[str, list[str]] = {}
    for member in package["members"]:
        if not str(member.get("schema", "")).startswith("form-field."):
            continue
        body = fields.get((member.get("id"), member.get("version"))) or {}
        symbol = str(body.get("binds_symbol") or "")
        if symbol:
            visible.setdefault(symbol, []).append(short(body.get("id")))
    paired = []
    loaded: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for member in package["members"]:
        if member.get("role") != "computation":
            continue
        body = rules.get((member.get("id"), member.get("version")))
        if not body:
            continue
        loaded.append((member, body))
        nodes: list[dict[str, Any]] = []
        _walk(body, "require_paired", nodes)
        for node in nodes:
            fact = str(node.get("withholding"))
            if "withholding" not in fact and "box4" not in fact and "box2" not in fact and "box6" not in fact:
                continue
            paired.append({
                "rule": short(member["id"]) + "." + str(member["version"]),
                "publishes": short(body.get("publishes")),
                "fields": visible.get(str(body.get("publishes")), []),
                "key": node.get("key"),
                "withholding": short(fact),
                "input_question": fact in question_for,
                "closure": fact in closure_for,
            })
    k_rules = []
    k_symbols = []
    for member, body in loaded:
        if _refs(body, K_BOX4) or K_BOX4 in (body.get("requires") or []):
            k_rules.append(short(member["id"]) + "." + str(member["version"]))
            k_symbols.append(str(body.get("publishes") or ""))
    hop = []
    for member, body in loaded:
        requires = [str(item) for item in body.get("requires") or []]
        if any(symbol in requires for symbol in k_symbols):
            hop.extend(visible.get(str(body.get("publishes")), []))
    direct = []
    for symbol in k_symbols:
        direct.extend(visible.get(symbol, []))
    w2g_body = None
    for member, body in loaded:
        if member["id"].endswith("w2g-b4-subtotal"):
            w2g_body = body
    return {
        "amount_question_published": question_for.get(AMOUNT) == sentence,
        "reported_question_is_different_fact": REPORTED in question_for and REPORTED != AMOUNT,
        "paired_withholding": paired,
        "paired_without_question_and_closure": [row for row in paired if not row["input_question"] and not row["closure"]],
        "w2g_box4": {
            "input_question": W2G_BOX4 in question_for,
            "closure_question": closure_for.get(W2G_BOX4, ""),
            "subtotal_when": (w2g_body or {}).get("when", {}).get("op"),
            "line_25c_fields": visible.get(P + "payments.line25c", []),
        },
        "f1099k_box4": {
            "input_question": K_BOX4 in question_for,
            "closure": K_BOX4 in closure_for,
            "rules": k_rules,
            "form_fields": sorted(set(direct)),
            "one_hop_form_fields": sorted(set(hop)),
        },
    }


def write(payload: dict[str, Any]) -> None:
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit("probe output contains a local path")
    (HERE / "probe-output.json").write_text(text, encoding="utf-8")


def main() -> None:
    sentence = json.loads((CONTENT / "input-question.f1099b-box4.v1.json").read_text(encoding="utf-8"))["question"]
    shape = shapes(sentence)
    lists = build_lists()
    notes = {case_id: note for case_id, _acts, note in lists}
    evidence_loader.finish(OWNER)
    workers = max(1, (os.cpu_count() or 2) - 1)
    payload = [(case_id, acts) for case_id, acts, _note in lists]
    shards = [(sentence, payload[index::workers]) for index in range(workers) if payload[index::workers]]
    started = time.time()
    found: list[dict[str, Any]] = []
    with multiprocessing.get_context("spawn").Pool(workers) as pool:
        for part in pool.map(_worker, shards):
            found.extend(part)
    cases = {}
    for row in found:
        row["note"] = notes[row["id"]]
        cases[row.pop("id")] = row
    wall = round(time.time() - started, 1)
    write({
        "core": {"package": "v91", "registry": "v89", "release": "v89"},
        "workers": workers,
        "wall_time_s": wall,
        "amount_sentence": sentence,
        "cases": cases,
        "shapes": shape,
    })
    brief = {
        case_id: {
            "outcome": row.get("outcome"),
            "line25b": (row.get("lines") or {}).get("form1040.line-25b"),
            "line25d": (row.get("lines") or {}).get("form1040.line-25d"),
            "only": [field["field"] for field in row.get("amount_fields") or [] if field.get("only_amount_sentence")],
            "page": row.get("page_has_amount_sentence"),
        }
        for case_id, row in cases.items()
    }
    print(json.dumps({"wall_time_s": wall, "workers": workers, "cases": brief, "bare": shape["paired_without_question_and_closure"], "k": shape["f1099k_box4"]}, indent=2))


if __name__ == "__main__":
    main()
