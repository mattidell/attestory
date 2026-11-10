"""P0 probes for Form 1099-B box 4 with no sale on core v84, and on a scratch core.

Evidence for docs/phases/engine-breadth/milestones/f1099b-box4-only.md.
Charter: docs/reviews/f1099b-box4-only/charter-p0.md.

    python3 probe.py
    python3 probe.py /path/outside/core.json

Hand values are computed here from the 2025 instructions and the adopted rate
parameters. They are not copied from a run. Synthetic demo.* facts only.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import math
import os
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

HARNESS = "f1099b_b4only_p0_harness"
spec = importlib.util.spec_from_file_location(
    HARNESS, REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/audit_harness.py")
assert spec is not None and spec.loader is not None
h = importlib.util.module_from_spec(spec)
sys.modules[HARNESS] = h
spec.loader.exec_module(h)

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402

P = "tax.us.2025."
YEAR = "2025"
BOX4 = P + "f1099b.statement-box4-withholding"
BOX7 = P + "f1099b.statement-box7-loss-not-allowed"
PRESENT = P + "f1099b.no-sale-box4-present"
AMOUNT = P + "f1099b.no-sale-box4-withholding"
V84 = h.Core("v84", "v82", "v82")
LINES = (
    "form1040.line-25a", "form1040.line-25b", "form1040.line-25c", "form1040.line-25d",
    "form1040.line-33", "form1040.line-34", "form1040.line-37",
    "form1040.line-7a", "form1040.line-15", "form1040.line-16",
)


def _bracket(amount: float) -> float:
    tax = 0.10 * min(amount, 11925)
    if amount > 11925:
        tax += 0.12 * (min(amount, 48475) - 11925)
    if amount > 48475:
        tax += 0.22 * (min(amount, 103350) - 48475)
    return tax


def tax_table(taxable: float) -> int:
    """2025 Tax Table, single: tax on the band midpoint, rounded half up."""
    if taxable <= 0:
        return 0
    if taxable >= 3000:
        midpoint = math.floor(taxable / 50) * 50 + 25
    else:
        midpoint = math.floor(taxable / 25) * 25 + 12.5
    return int(math.floor(_bracket(midpoint) + 0.5))


def qdcg(taxable: float, preferential: float) -> int:
    if preferential <= 0:
        return tax_table(taxable)
    ordinary = taxable - preferential
    zero_band = max(0.0, min(taxable, 48350) - ordinary)
    fifteen = max(0.0, preferential - zero_band)
    combined = tax_table(ordinary) + 0.15 * fifteen
    return min(tax_table(taxable), int(math.floor(combined + 0.5)))


def hand_return(*, st_gain: float = 0, lt_gain: float = 0, line25b: float | None = 0,
                blocked: bool = False) -> dict[str, Any]:
    """Form 1040 lines from the 2025 instructions. A blocked case has no published hand lines."""
    if blocked or line25b is None:
        return {"disposition": "blocked"}
    line7a = st_gain + lt_gain
    taxable = max(0.0, 34250 + line7a)
    preferential = 0.0 if line7a <= 0 or lt_gain <= 0 else min(lt_gain, line7a)
    tax = qdcg(taxable, preferential)
    line25a = 4500
    line25c = 0
    line25d = line25a + int(line25b) + line25c
    line33 = line25d
    return {
        "disposition": "published",
        "form1040.line-25a": line25a,
        "form1040.line-25b": int(line25b),
        "form1040.line-25c": line25c,
        "form1040.line-25d": line25d,
        "form1040.line-33": line33,
        "form1040.line-34": max(0, line33 - tax),
        "form1040.line-37": max(0, tax - line33),
        "form1040.line-7a": int(line7a),
        "form1040.line-15": int(taxable),
        "form1040.line-16": tax,
    }


def has_no_sale_vocab(core: Any) -> bool:
    return (core.content / "f1099b-no-sale-box4.bundle.json").exists()


def say_statement(acts: list[dict[str, Any]], core: Any, fact_type: str, statement: str,
                  value: object) -> list[dict[str, Any]]:
    fact_id = h.fact_id_for(fact_type, (("statement", statement), ("tax-year", YEAR)))
    kept = []
    for act in acts:
        finding = (act.get("payload") or {}).get("finding") if isinstance(act.get("payload"), dict) else None
        if isinstance(finding, dict) and finding.get("fact_id") == fact_id:
            continue
        kept.append(act)
    acts = kept
    body = h.bundle_for(fact_type, core.content)
    if body is not None and not {fact["id"] for fact in body["fact_types"]} & h._adopted(acts):
        h._add(acts, "bundle-adoption", {"bundle": body})
    h._add(acts, "assertion", {"finding": h._attested(
        f"demo.b4only.{fact_type.split('.')[-1]}.{statement.split('.')[-2]}", fact_id, value)})
    return h.renumber(acts)


def say_return(acts: list[dict[str, Any]], core: Any, fact_type: str, value: object,
               tag: str) -> list[dict[str, Any]]:
    return h.say(acts, fact_type, value, tag, core.content)


def introduce_statement(acts: list[dict[str, Any]], tag: str) -> list[dict[str, Any]]:
    broker = f"demo.sfa.{tag}.broker"
    statement = f"demo.sfa.{tag}.statement"
    if broker not in h._entities(acts):
        h._introduce(acts, broker, "tax.us.f1099b-broker")
    if statement not in h._entities(acts):
        h._introduce(acts, statement, "tax.us.f1099b-statement")
    return h.renumber(acts)


def statements_of(acts: list[dict[str, Any]]) -> list[str]:
    found: list[str] = []
    for act in acts:
        payload = act.get("payload") or {}
        if act.get("kind") != "member-transition":
            continue
        member = payload.get("member") or {}
        finding = member.get("finding") or {}
        fact_id = str(finding.get("fact_id") or "")
        if "statement=" not in fact_id or not str((payload.get("family") or {}).get("id", "")).startswith(P + "f1099b."):
            continue
        statement = fact_id.split("statement=", 1)[1].split(",", 1)[0]
        if statement not in found and member.get("action") == "assert":
            found.append(statement)
    return found


def box4_zero_sales(acts: list[dict[str, Any]], core: Any) -> list[dict[str, Any]]:
    for statement in statements_of(acts):
        acts = say_statement(acts, core, BOX4, statement, 0)
        acts = say_statement(acts, core, BOX7, statement, "no")
    return acts


def remove_sale(acts: list[dict[str, Any]], kind: str, term: str, tag: str) -> list[dict[str, Any]]:
    per_family = h.SALE_KINDS[kind]["grouped"] is None
    out = copy.deepcopy(acts)
    for scalar in (*h.SALE_KINDS[kind]["kinds"], None):
        fam = h.family_id(kind, term, scalar)
        member = h.member_fact(kind, term, scalar)
        fact_ids = [
            str(act["payload"]["member"]["finding"]["fact_id"])
            for act in out
            if act.get("kind") == "member-transition" and act["payload"]["family"]["id"] == fam
            and (act["payload"]["member"].get("finding") or {}).get("fact_id", "").startswith(member + "|")
            and f"demo.sfa.{tag}." in str(act["payload"]["member"]["finding"]["fact_id"])
        ]
        for fact_id in fact_ids:
            if per_family:
                out = h.strip(out, fam + ".source-closure")
            head = h.horizons(out, fam)[-1]
            successor = f"demo.b4only.rm.{tag}.{fam.removeprefix(P)}.h{len(h.horizons(out, fam))}"
            h._add(out, "member-transition", {
                "family": {"id": fam, "version": h.SALE_KINDS[kind]["version"]},
                "scope": {"tax-year": YEAR, "subject": "demo.primary"},
                "member": {"action": "remove", "fact_id": fact_id},
                "successor": {"id": successor, "predecessor": head},
            })
            if per_family:
                h._close(out, fam + ".source-closure", successor,
                         f"demo.b4only.rm.{tag}.{fam.removeprefix(P)}.closure")
    return h.renumber(out)


def sale_on(acts: list[dict[str, Any]], kind: str, term: str, tag: str, *, statement_tag: str,
            **kw: Any) -> list[dict[str, Any]]:
    acts = h.sale(acts, kind, term, tag=tag, **kw)
    mapping = {
        f"demo.sfa.{tag}.broker": f"demo.sfa.{statement_tag}.broker",
        f"demo.sfa.{tag}.statement": f"demo.sfa.{statement_tag}.statement",
    }
    out = []
    for act in acts:
        if act.get("kind") == "entity-introduced" and act["payload"]["entity"]["id"] in mapping:
            continue
        text = json.dumps(act)
        for old, new in mapping.items():
            text = text.replace(old + ",", new + ",").replace(old + '"', new + '"')
        out.append(json.loads(text))
    return h.renumber(out)


def prepare(acts: list[dict[str, Any]], core: Any, kinds: set[str], *, loss: bool = False) -> list[dict[str, Any]]:
    answers = h.honest(kinds, loss=loss, new_questions=False)
    answers.update(h.honest_exception1(acts))
    acts = h.answer(acts, core.content, **{key: value for key, value in answers.items() if value is not None})
    return box4_zero_sales(acts, core)


def run_case(core: Any, acts: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
    with h.loader_entries(core):
        surface = core.surface()
        try:
            finished = h._handover(h._finish(
                copy.deepcopy(acts), package_path=core.package_path, package_version=core.version,
                release_path=core.release_path, release_version=core.release_version, note=run_id,
            ), surface=surface, reconfirm=True)
        except Exception as exc:  # noqa: BLE001 — a rejected act list is a measured result
            return {"outcome": "error", "error": type(exc).__name__, "message": h.scrub(str(exc))[:400]}
        with tempfile.TemporaryDirectory() as tmp:
            outcome = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO, authoritative_acts=finished,
                workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": YEAR},
                scope_user=h.ccr.USER, request={"schema": "run-request.v1"}, run_id=run_id,
                governance_pins=[], surface=surface, output_name="out.json")
            if outcome.refusal is not None:
                return {"outcome": "refusal", "reason": outcome.refusal.reason,
                        "message": h.scrub(str(outcome.refusal.detail))[:400]}
            model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
    lines: dict[str, Any] = {}
    questions: list[str] = []
    reasons: dict[str, list[str]] = {}
    for section in model.get("sections") or []:
        field_id = str((section.get("field") or {}).get("id") or "")
        short = field_id.removeprefix(P)
        resolved = section.get("resolved") or {}
        sentences = [str(reason.get("sentence") or "") for reason in resolved.get("reasons") or []
                     if isinstance(reason, dict) and reason.get("sentence")]
        for sentence in sentences:
            if sentence and sentence not in questions and (
                    sentence.endswith("?") or sentence.startswith("Enter ")):
                questions.append(sentence)
        if short in LINES:
            value = resolved.get("value")
            disposition = str(resolved.get("disposition"))
            if value is None or "blocked" in disposition:
                lines[short] = disposition
            elif isinstance(value, float) and value.is_integer():
                lines[short] = int(value)
            else:
                lines[short] = value
            if "blocked" in disposition:
                reasons[short] = [h.scrub(sentence)[:240] for sentence in sentences]
    blocked = []
    for row in report.get("dispositions") or []:
        artifact = str(row.get("artifact_id") or "")
        if row.get("disposition") == "blocked" and "line25b" in artifact:
            blocked.append({
                "artifact": artifact.removeprefix(P + "rule."),
                "code": row.get("code"),
                "missing": [str(item).removeprefix(P) for item in (row.get("missing") or [])][:8],
            })
    line25b = lines.get("form1040.line-25b")
    if line25b == "blocked" or (isinstance(line25b, str) and "blocked" in str(line25b)):
        disposition = "blocked"
    elif isinstance(line25b, (int, float)):
        disposition = "published"
    else:
        disposition = "other"
    return {
        "outcome": "success",
        "stop": report.get("stop_reason"),
        "disposition": disposition,
        "lines": lines,
        "questions": [h.scrub(question)[:240] for question in questions],
        "reasons": reasons,
        "blocked": blocked[:8],
    }


def _one(item: tuple[str, Any, list[dict[str, Any]]]) -> tuple[str, dict[str, Any]]:
    case_id, core, acts = item
    return case_id, run_case(core, acts, "demo.b4only." + case_id)


def build_cases(core: Any) -> list[dict[str, Any]]:
    successor = has_no_sale_vocab(core)

    def add(case_id: str, acts: list[dict[str, Any]], kinds: set[str], *,
            present: str | None, amount: float | None, stmt_amounts: dict[str, float],
            hand: dict[str, Any], expect: str, note: str, after: Any = None) -> dict[str, Any]:
        acts = prepare(acts, core, kinds)
        if after is not None:
            acts = after(acts)
            fresh = h.honest_exception1(acts)
            if fresh.get("exc1_only_2a") is None and fresh.get("exc1_no_losses") is None:
                fresh = {"exc1_only_2a": "yes", "exc1_no_losses": "yes"}
            acts = h.answer(acts, core.content, **{
                key: value for key, value in fresh.items() if value is not None})
            acts = box4_zero_sales(acts, core)
        for statement, value in stmt_amounts.items():
            acts = say_statement(acts, core, BOX4, statement, value)
            acts = say_statement(acts, core, BOX7, statement, "no")
        if successor:
            if present is not None:
                acts = say_return(acts, core, PRESENT, present, "present")
            if amount is not None:
                acts = say_return(acts, core, AMOUNT, amount, "amount")
        return {
            "id": case_id, "expect": expect, "note": note, "acts": acts, "hand": hand,
            "present": present, "amount": amount, "stmt_amounts": stmt_amounts,
        }

    specs: list[dict[str, Any]] = []
    orphan = "demo.sfa.orphan.statement"
    sale_stmt = "demo.sfa.sale1.statement"

    empty = h.opened()
    specs.append(add(
        "no_1099b", empty, set(), present="no", amount=None, stmt_amounts={},
        hand=hand_return(line25b=0), expect="published",
        note="No Form 1099-B at all. v84 publishes line 25b 0. v85 asks the present question unless answered no.",
    ))

    only_entity = introduce_statement(h.opened(), "orphan")
    specs.append(add(
        "b4_only_unasked", only_entity, set(), present=None, amount=None, stmt_amounts={},
        hand=hand_return(line25b=150, blocked=successor),
        expect="blocked" if successor else "published",
        note=(
            "One statement entity, no sale, box 4 unasked. The filer received $150. "
            "v84 publishes 0, short of that withholding. v85 blocks and asks the present question."
        ),
    ))

    only_recorded = introduce_statement(h.opened(), "orphan")
    specs.append(add(
        "b4_only_recorded", only_recorded, set(), present="yes", amount=0,
        stmt_amounts={orphan: 150},
        hand=hand_return(line25b=150), expect="published",
        note=(
            "No-sale statement with box 4 $150 already recorded. v84 counts it (Decision 6). "
            "On v85 present is yes and the return-level amount is 0 so the statement amount is not counted twice."
        ),
    ))

    specs.append(add(
        "b4_only_return_level", introduce_statement(h.opened(), "orphan"), set(),
        present="yes", amount=150, stmt_amounts={},
        hand=hand_return(line25b=150 if successor else 0),
        expect="published",
        note=(
            "No-sale withholding answered only at return level, no per-statement amount. "
            "v84 publishes 0. v85 publishes 150."
        ),
    ))

    specs.append(add(
        "b4_only_zero_present_no", introduce_statement(h.opened(), "orphan"), set(),
        present="no", amount=None, stmt_amounts={},
        hand=hand_return(line25b=0), expect="published",
        note="No-sale statement, box 4 blank or zero. Answering present=no establishes that. Nothing more is asked.",
    ))

    specs.append(add(
        "b4_only_zero_amount", introduce_statement(h.opened(), "orphan"), set(),
        present="yes", amount=0, stmt_amounts={orphan: 0},
        hand=hand_return(line25b=0), expect="published",
        note="No-sale statement with box 4 of zero recorded.",
    ))

    beside_sale = h.opened()
    beside_sale = h.sale(beside_sale, "covered", "st", proceeds=5000, basis=4000, tag="sale1")
    beside_sale = introduce_statement(beside_sale, "orphan")
    specs.append(add(
        "b4_only_beside_sale_unasked", beside_sale, {"covered"}, present=None, amount=None,
        stmt_amounts={sale_stmt: 200},
        hand=hand_return(st_gain=1000, line25b=350, blocked=successor),
        expect="blocked" if successor else "published",
        note="No-sale $150 unasked beside a sale statement with box 4 $200. v84 publishes 200, short $150.",
    ))

    beside_sale2 = h.opened()
    beside_sale2 = h.sale(beside_sale2, "covered", "st", proceeds=5000, basis=4000, tag="sale1")
    beside_sale2 = introduce_statement(beside_sale2, "orphan")
    specs.append(add(
        "b4_only_beside_sale", beside_sale2, {"covered"}, present="yes", amount=0,
        stmt_amounts={sale_stmt: 200, orphan: 150},
        hand=hand_return(st_gain=1000, line25b=350), expect="published",
        note=(
            "No-sale $150 and a sale statement $200, both recorded per-statement. Return-level "
            "amount is 0. Line 25b is 350 beside W-2 $4500."
        ),
    ))

    mixed_return_level = h.opened()
    mixed_return_level = h.sale(mixed_return_level, "covered", "st", proceeds=5000, basis=4000, tag="sale1")
    specs.append(add(
        "b4_only_beside_sale_return_level", mixed_return_level, {"covered"}, present="yes", amount=150,
        stmt_amounts={sale_stmt: 200},
        hand=hand_return(st_gain=1000, line25b=350 if successor else 200),
        expect="published",
        note="Sale statement $200 plus return-level no-sale $150. v85 publishes 350. v84 publishes 200.",
    ))

    added = introduce_statement(h.opened(), "orphan")
    added = say_statement(added, core, BOX4, orphan, 150)

    def add_sale(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return sale_on(acts, "covered", "st", "later", statement_tag="orphan",
                       proceeds=5000, basis=4000)

    specs.append(add(
        "no_sale_then_sale_added", added, set(), present="no", amount=None,
        stmt_amounts={orphan: 150},
        hand=hand_return(st_gain=1000, line25b=150), expect="published",
        note=(
            "No-sale $150 recorded, then a sale is added to that statement. Present is no "
            "because the statement now has a sale. The per-statement amount still counts once."
        ),
        after=add_sale,
    ))

    double = introduce_statement(h.opened(), "orphan")

    def add_sale_keep_return_level(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return sale_on(acts, "covered", "st", "later", statement_tag="orphan",
                       proceeds=5000, basis=4000)

    specs.append(add(
        "no_sale_then_sale_added_double", double, set(), present="yes", amount=150,
        stmt_amounts={orphan: 150},
        hand=hand_return(st_gain=1000, line25b=300 if successor else 150),
        expect="published",
        note=(
            "Same as the added-sale case, but present stays yes with return-level $150. "
            "v85 would add both amounts (300). That is the double-count the design must name."
        ),
        after=add_sale_keep_return_level,
    ))

    removed = h.opened()
    removed = h.sale(removed, "covered", "st", proceeds=5000, basis=4000, tag="sale1")
    specs.append(add(
        "sale_removed_to_none", removed, {"covered"}, present="yes" if successor else None,
        amount=0 if successor else None,
        stmt_amounts={sale_stmt: 200},
        hand=hand_return(line25b=200), expect="published",
        note=(
            "A sale with box 4 $200 is removed. The per-statement amount remains and still "
            "counts. Present yes with return-level $0 adds nothing extra."
        ),
        after=lambda acts: remove_sale(acts, "covered", "st", "sale1"),
    ))

    specs.append(add(
        "present_yes_amount_missing", introduce_statement(h.opened(), "orphan"), set(),
        present="yes", amount=None, stmt_amounts={},
        hand=hand_return(line25b=150, blocked=successor),
        expect="blocked" if successor else "published",
        note="Present yes and the amount unanswered. v85 blocks and asks the amount question.",
    ))
    return specs


def compare(spec: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    if result.get("outcome") != "success":
        return {"matches_hand": False, "why": result.get("outcome")}
    if spec["expect"] == "blocked":
        return {
            "matches_hand": result["disposition"] == "blocked",
            "why": "blocked" if result["disposition"] == "blocked" else result["disposition"],
        }
    diffs = []
    for line, expected in (spec["hand"] or {}).items():
        if line == "disposition":
            if result["disposition"] != expected:
                diffs.append({"line": "disposition", "hand": expected, "got": result["disposition"]})
            continue
        got = (result.get("lines") or {}).get(line)
        if got != expected:
            diffs.append({"line": line, "hand": expected, "got": got})
    return {"matches_hand": not diffs, "diffs": diffs[:12]}


def main() -> None:
    core = V84
    label = "v84"
    if len(sys.argv) > 1:
        body = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        core = h.Core(body["version"], body["registry"], body["release_version"],
                      content=Path(body["content"]), releases=Path(body["releases"]),
                      loader_from=body.get("loader_from"))
        label = body["version"]
    specs = build_cases(core)
    only = os.environ.get("B4ONLY_ONLY")
    if only:
        specs = [spec for spec in specs if spec["id"] in only.split(",")]
    workers = int(os.environ.get("B4ONLY_WORKERS") or min(6, os.cpu_count() or 2))
    print(f"running {len(specs)} cases on {label}", flush=True)
    found: dict[str, dict[str, Any]] = {}
    work = [(spec["id"], core, spec["acts"]) for spec in specs]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for case_id, result in pool.map(_one, work):
            found[case_id] = result
            print(f"{case_id} {result.get('disposition') or result.get('outcome')}", flush=True)
    rows = []
    for spec in specs:
        result = found[spec["id"]]
        compared = compare(spec, result)
        rows.append({
            "id": spec["id"],
            "note": spec["note"],
            "expect": spec["expect"],
            "hand": {key: value for key, value in (spec["hand"] or {}).items() if key != "disposition"}
            if spec["expect"] == "published" else None,
            "present": spec["present"],
            "amount": spec["amount"],
            "stmt_amounts": spec["stmt_amounts"],
            "result": {key: result[key] for key in
                       ("outcome", "disposition", "lines", "questions", "reasons", "blocked",
                        "error", "message")
                       if key in result},
            "compare": compared,
        })
    payload = {
        "core": label,
        "cases": rows,
        "matches": sum(1 for row in rows if row["compare"].get("matches_hand")),
        "total": len(rows),
    }
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"probe output contains {needle}")
    out = HERE / f"probe-output-{label}.json"
    out.write_text(text, encoding="utf-8")
    print(json.dumps({"core": label, "matches": payload["matches"], "total": payload["total"],
                      "output": out.name}, indent=2))


if __name__ == "__main__":
    main()
