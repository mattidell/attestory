"""P0 probes for Form 8949 code L on core v85.

Evidence for docs/phases/engine-breadth/milestones/f8949-code-l.md.
Charter: docs/reviews/f8949-code-l/charter-p0.md.

    python3 probe.py

Hand values are computed here from the 2025 instructions and the adopted rate
parameters. They are not copied from a run. Synthetic demo.* facts only.
The audit harness is loaded under a name reserved for this milestone.
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

HARNESS = "f8949_code_l_audit_harness"
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
BOX7 = P + "f1099b.statement-box7-loss-not-allowed"
BOX4_REPORTED = P + "f1099b.statement-box4-withholding-reported"
BOX4_AMOUNT = P + "f1099b.statement-box4-withholding"
NO_SALE_BOX4 = P + "f1099b.no-sale-box4-present"
V85 = h.Core("v85", "v83", "v83")
LINES = (
    "schedule-d.line-1a", "schedule-d.line-1b", "schedule-d.line-2", "schedule-d.line-3",
    "schedule-d.line-7", "schedule-d.line-8a", "schedule-d.line-8b", "schedule-d.line-9",
    "schedule-d.line-10", "schedule-d.line-15", "schedule-d.line-16", "schedule-d.line-21",
    "form1040.line-7a", "form1040.line-15", "form1040.line-16", "form1040.line-24",
    "form1040.line-33", "form1040.line-34", "form1040.line-37",
)
POSTS = {
    ("covered", "st"): "1a", ("covered", "lt"): "8a",
    ("w", "st"): "1b", ("w", "lt"): "8b",
    ("noncovered", "st"): "2", ("noncovered", "lt"): "9",
    ("codeb", "st"): "1b", ("codeb", "lt"): "8b",
}
# A code L sale leaves the direct-report line and posts column (h) of zero
# on the Form 8949 line for its box. Box A/D when basis was reported.
CODE_L_LINE = {
    ("covered", "st"): "1b", ("covered", "lt"): "8b",
    ("w", "st"): "1b", ("w", "lt"): "8b",
    ("noncovered", "st"): "2", ("noncovered", "lt"): "9",
    ("codeb", "st"): "1b", ("codeb", "lt"): "8b",
}
CODE_L_BOX = {
    ("covered", "st"): "A", ("covered", "lt"): "D",
    ("w", "st"): "A", ("w", "lt"): "D",
    ("noncovered", "st"): "B", ("noncovered", "lt"): "E",
    ("codeb", "st"): "A", ("codeb", "lt"): "D",
}


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


def column_h(kind: str, proceeds: float, basis: float, wash: float = 0.0, corrected: float | None = None) -> float:
    if kind == "codeb":
        return proceeds - (basis if corrected is None else corrected) + wash
    if kind == "covered":
        return proceeds - basis
    return proceeds - basis + wash


def hand_return(sales: list[tuple[str, str, float]]) -> dict[str, Any]:
    """Schedule D and Form 1040 from the column (h) amounts the instructions post."""
    boxes = {name: 0.0 for name in ("1a", "1b", "2", "3", "8a", "8b", "9", "10")}
    for kind, term, amount in sales:
        boxes[POSTS[(kind, term)]] += amount
    line7 = boxes["1a"] + boxes["1b"] + boxes["2"] + boxes["3"]
    line15 = boxes["8a"] + boxes["8b"] + boxes["9"] + boxes["10"]
    line16 = line7 + line15
    line21 = min(3000.0, -line16) if line16 < 0 else 0.0
    line7a = line16 if line16 >= 0 else -line21
    taxable = max(0.0, 34250 + line7a)
    preferential = 0.0 if (line15 <= 0 or line16 <= 0) else min(line15, line16)
    tax = qdcg(taxable, preferential)
    payments = 4500
    values = {
        "schedule-d.line-1a": boxes["1a"], "schedule-d.line-1b": boxes["1b"],
        "schedule-d.line-2": boxes["2"], "schedule-d.line-3": boxes["3"],
        "schedule-d.line-7": line7, "schedule-d.line-8a": boxes["8a"],
        "schedule-d.line-8b": boxes["8b"], "schedule-d.line-9": boxes["9"],
        "schedule-d.line-10": boxes["10"], "schedule-d.line-15": line15,
        "schedule-d.line-16": line16, "schedule-d.line-21": line21,
        "form1040.line-7a": line7a, "form1040.line-15": taxable,
        "form1040.line-16": tax, "form1040.line-24": tax,
        "form1040.line-33": payments,
        "form1040.line-34": max(0, payments - tax),
        "form1040.line-37": max(0, tax - payments),
    }
    return {key: int(value) if float(value).is_integer() else value for key, value in values.items()}


def code_l_row(kind: str, term: str, proceeds: float, basis: float, wash: float, corrected: float | None) -> dict[str, Any]:
    """Example 2's row. Column (g) is the whole pre-existing loss, so column (h) is zero.

    A wash or a code B correction is already in column (h). Code L's amount is that
    remaining loss. The code letters are the foreman decision named in the case.
    """
    before = column_h(kind, proceeds, basis, wash, corrected)
    adjustment = -before
    shown = basis
    code_b = 0.0 if kind != "codeb" else shown - (shown if corrected is None else corrected)
    return {
        "box": CODE_L_BOX[(kind, term)],
        "schedule_d_line": CODE_L_LINE[(kind, term)],
        "d": proceeds,
        "e": shown,
        "g_before_code_l": code_b + wash,
        "g_code_l": adjustment,
        "g": code_b + wash + adjustment,
        "h": proceeds - shown + code_b + wash + adjustment,
    }


def say_statement(acts: list[dict[str, Any]], core: Any, fact_type: str, statement: str,
                  value: object, *, tag: str, replace: bool) -> list[dict[str, Any]]:
    fact_id = h.fact_id_for(fact_type, (("statement", statement), ("tax-year", YEAR)))
    if replace:
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
    h._add(acts, "assertion", {"finding": h._attested(f"demo.cl.{tag}.{statement.split('.')[-2]}", fact_id, value)})
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


def box4_no(acts: list[dict[str, Any]], core: Any) -> list[dict[str, Any]]:
    """Core v85 asks the box 4 yes/no and the box 4 amount. These statements show neither."""
    for statement in statements_of(acts):
        acts = say_statement(acts, core, BOX4_REPORTED, statement, "no", tag="box4yn", replace=True)
        acts = say_statement(acts, core, BOX4_AMOUNT, statement, 0, tag="box4amt", replace=True)
    return acts


def box7(acts: list[dict[str, Any]], core: Any, answers: dict[str, str | None]) -> list[dict[str, Any]]:
    for statement in statements_of(acts):
        value = answers.get(statement, answers.get("*"))
        if value is not None:
            acts = say_statement(acts, core, BOX7, statement, value, tag="box7", replace=True)
    return acts


def supersede_box7(acts: list[dict[str, Any]], core: Any, value: str) -> list[dict[str, Any]]:
    """A later assertion of the same fact. The earlier answer stays in the act list."""
    for statement in statements_of(acts):
        acts = say_statement(acts, core, BOX7, statement, value, tag="box7b", replace=False)
    return acts


def sale_on(acts: list[dict[str, Any]], kind: str, term: str, tag: str, *, statement_tag: str, **kw: Any) -> list[dict[str, Any]]:
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
            successor = f"demo.cl.rm.{tag}.{fam.removeprefix(P)}.h{len(h.horizons(out, fam))}"
            h._add(out, "member-transition", {
                "family": {"id": fam, "version": h.SALE_KINDS[kind]["version"]},
                "scope": {"tax-year": YEAR, "subject": "demo.primary"},
                "member": {"action": "remove", "fact_id": fact_id},
                "successor": {"id": successor, "predecessor": head},
            })
            if per_family:
                h._close(out, fam + ".source-closure", successor, f"demo.cl.rm.{tag}.{fam.removeprefix(P)}.closure")
    return h.renumber(out)


def supersede_basis(acts: list[dict[str, Any]], kind: str, term: str, tag: str, basis: float) -> list[dict[str, Any]]:
    out = copy.deepcopy(acts)
    for scalar in (None, "basis"):
        fam = h.family_id(kind, term, scalar)
        member = h.member_fact(kind, term, scalar)
        found = [
            act["payload"]["member"]["finding"]
            for act in out
            if act.get("kind") == "member-transition" and act["payload"]["family"]["id"] == fam
            and (act["payload"]["member"].get("finding") or {}).get("fact_id", "").startswith(member + "|")
            and f"demo.sfa.{tag}." in str(act["payload"]["member"]["finding"]["fact_id"])
        ]
        if not found:
            continue
        prior = found[-1]
        if scalar is None:
            value = dict(prior["value"])
            value["basis"] = basis
        else:
            value = basis
        h._add(out, "assertion", {"finding": h._attested(
            f"demo.cl.ch.{tag}.{fam.removeprefix(P)}.{scalar or 'sale'}", prior["fact_id"], value)})
    return h.renumber(out)


def prepare(acts: list[dict[str, Any]], core: Any, kinds: set[str], loss: bool) -> list[dict[str, Any]]:
    answers = h.honest(kinds, loss=loss, new_questions=False)
    answers.update(h.honest_exception1(acts))
    acts = h.answer(acts, core.content, **{key: value for key, value in answers.items() if value is not None})
    return box4_no(acts, core)


def _num(value: Any) -> Any:
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


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
    explains: dict[str, Any] = {}
    questions: list[str] = []
    for section in model.get("sections") or []:
        field = section.get("field") or {}
        field_id = str(field.get("id") or "")
        short = field_id.removeprefix(P)
        resolved = section.get("resolved") or {}
        sentences = [str(reason.get("sentence") or "") for reason in resolved.get("reasons") or []
                     if isinstance(reason, dict) and reason.get("sentence")]
        for sentence in sentences:
            if sentence.endswith("?") and sentence not in questions:
                questions.append(sentence)
        if short in LINES:
            value = resolved.get("value")
            disposition = str(resolved.get("disposition"))
            lines[short] = disposition if value is None or "blocked" in disposition else _num(value)
            instruction = (field.get("dispositions") or {}).get(disposition) or {}
            explain = instruction.get("explain")
            if "blocked" in disposition or explain or sentences:
                explains[short] = {
                    "explain": None if explain is None else h.scrub(str(explain))[:1200],
                    "reasons": [h.scrub(sentence)[:240] for sentence in sentences[:4]],
                }
    blocked = []
    for row in report.get("dispositions") or []:
        artifact = str(row.get("artifact_id") or "")
        if row.get("disposition") == "blocked" and (
                "box7" in artifact or "schedule-d" in artifact or "8949" in artifact or "line7a" in artifact):
            blocked.append({
                "artifact": artifact.removeprefix(P + "rule."),
                "code": row.get("code"),
                "missing": [str(item).removeprefix(P) for item in (row.get("missing") or [])][:6],
            })
    parts = []
    for group in model.get("citationGroups") or []:
        if "8949" not in str(group.get("id")):
            continue
        parts.extend(str(part.get("heading") or part.get("label") or "") for part in group.get("parts") or [])
    line16 = lines.get("schedule-d.line-16")
    if isinstance(line16, str) and "blocked" in line16:
        disposition = "blocked"
    elif isinstance(line16, (int, float)):
        disposition = "published"
    else:
        disposition = "other"
    return {
        "outcome": "success",
        "stop": report.get("stop_reason"),
        "disposition": disposition,
        "lines": lines,
        "explains": explains,
        "questions": [h.scrub(question)[:300] for question in questions],
        "blocked": blocked[:16],
        "f8949_parts": parts,
        "code_l_part": any("code l" in part.lower() for part in parts),
    }


def _one(item: tuple[str, Any, list[dict[str, Any]]]) -> tuple[str, dict[str, Any]]:
    case_id, core, acts = item
    return case_id, run_case(core, acts, "demo.cl." + case_id)


def build_cases(core: Any) -> list[dict[str, Any]]:
    """Every case in the plan's 'Cases that will shape the design', except the v86 rerun."""
    def base(*sales: tuple) -> list[dict[str, Any]]:
        acts = h.opened()
        for kind, term, tag, kw in sales:
            acts = h.sale(acts, kind, term, tag=tag, **kw)
        return acts

    specs: list[dict[str, Any]] = []

    def add(case_id: str, acts: list[dict[str, Any]], kinds: set[str], loss: bool,
            answers: dict[str, str | None], posted: list[tuple[str, str, float]],
            *, rows: list[dict[str, Any]], settled: bool, note: str,
            after: Any = None) -> None:
        acts = prepare(acts, core, kinds, loss)
        acts = box7(acts, core, answers)
        if after is not None:
            acts = after(acts)
            fresh = h.honest_exception1(acts)
            if fresh.get("exc1_only_2a") is None and fresh.get("exc1_no_losses") is None:
                fresh = {"exc1_only_2a": "yes", "exc1_no_losses": "yes"}
            acts = h.answer(acts, core.content, **{key: value for key, value in fresh.items() if value is not None})
            acts = box4_no(acts, core)
        acts = h.say(acts, NO_SALE_BOX4, "no", "nosalebox4", core.content)
        specs.append({
            "id": case_id,
            "note": note,
            "instruction_settled": settled,
            "form_8949_rows": rows,
            "hand": hand_return(posted),
            "acts": acts,
        })

    loss = {"proceeds": 4000, "basis": 5000}
    gain = {"proceeds": 5000, "basis": 4000}
    add("yes_loss_covered_st", base(("covered", "st", "ls", loss)), {"covered"}, True, {"*": "yes"},
        [("covered", "st", 0)],
        rows=[{"code": "L", **code_l_row("covered", "st", 4000, 5000, 0, None)}],
        settled=True,
        note="Box 7 yes, one covered short-term loss. Example 2 puts it on Form 8949 box A with code L and column (h) zero, so it leaves line 1a.")
    add("yes_loss_covered_lt", base(("covered", "lt", "ll", loss)), {"covered"}, True, {"*": "yes"},
        [("covered", "lt", 0)],
        rows=[{"code": "L", **code_l_row("covered", "lt", 4000, 5000, 0, None)}],
        settled=True,
        note="Box 7 yes, one covered long-term loss. Same arithmetic on box D, line 8b.")
    same = h.opened()
    same = h.sale(same, "covered", "st", tag="mixg", **gain)
    same = sale_on(same, "covered", "st", "mixl", statement_tag="mixg", **loss)
    add("yes_loss_beside_gain_same_statement", same, {"covered"}, True, {"*": "yes"},
        [("covered", "st", 1000), ("covered", "st", 0)],
        rows=[{"code": "L", "which": "the loss", **code_l_row("covered", "st", 4000, 5000, 0, None)}],
        settled=True,
        note="One checked statement holds a $1,000 gain and a $1,000 loss. The gain stays on line 1a. The loss is the code L row.")
    wash_row = code_l_row("w", "st", 4000, 5000, 400, None)
    add("yes_loss_with_code_w", base(("w", "st", "ws", {**loss, "wash": 400})), {"w"}, True, {"*": "yes"},
        [("w", "st", 0)],
        rows=[{"code": "LW", "reading": "code L is the loss remaining after the wash", **wash_row}],
        settled=False,
        note="Wash of 400 leaves column (h) at -600 before code L. Code L excludes a loss indicated by code W, and a combined row is not exemplified. Recommended reading: codes LW, code L amount 600, column (h) zero.")
    codeb_row = code_l_row("codeb", "st", 4000, 5000, 0, 4500)
    add("yes_loss_with_code_b", base(("codeb", "st", "bs", {**loss, "corrected": 4500})), {"codeb"}, True, {"*": "yes"},
        [("codeb", "st", 0)],
        rows=[{"code": "BL", "reading": "code L is the loss remaining after the basis correction", **codeb_row}],
        settled=False,
        note="Basis shown 5000, corrected basis 4500, proceeds 4000. Code B's adjustment is 500 and column (h) is still -500. Recommended reading: code L disallows that remaining loss. If the correction had removed the loss, code L would not apply.")
    add("yes_loss_noncovered", base(("noncovered", "st", "ns", loss)), {"noncovered"}, True, {"*": "yes"},
        [("noncovered", "st", 0)],
        rows=[{"code": "L", **code_l_row("noncovered", "st", 4000, 5000, 0, None)}],
        settled=True,
        note="Box 7 yes on a noncovered short-term sale, box B. The sale is already on Form 8949. Column (h) becomes zero.")
    add("no_beside_loss", base(("covered", "st", "ok", loss)), {"covered"}, True, {"*": "no"},
        [("covered", "st", -1000)],
        rows=[],
        settled=True,
        note="Box 7 no beside a covered short-term loss. The loss is allowed and stays on line 1a. No code L row.")
    add("loss_changed_to_gain", base(("covered", "st", "ch", loss)), {"covered"}, True, {"*": "yes"},
        [("covered", "st", 1000)],
        rows=[],
        settled=True,
        note="Box 7 yes on a loss, then the same sale's basis is superseded to 3000, so column (h) is +1000. A gain is not code L.",
        after=lambda acts: supersede_basis(acts, "covered", "st", "ch", 3000))
    add("sale_removed", base(("covered", "st", "rm", loss)), {"covered"}, True, {"*": "yes"},
        [],
        rows=[],
        settled=True,
        note="Box 7 yes, then the only sale is removed. Nothing remains to disallow.",
        after=lambda acts: remove_sale(acts, "covered", "st", "rm"))
    add("box7_yes_superseded_to_no", base(("covered", "st", "su", loss)), {"covered"}, True, {"*": "yes"},
        [("covered", "st", -1000)],
        rows=[],
        settled=True,
        note="Box 7 answered yes, then superseded to no, on one covered short-term loss. The current answer allows the loss.",
        after=lambda acts: supersede_box7(acts, core, "no"))
    return specs


def compare(spec: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    if result.get("outcome") != "success":
        return {"matches_instruction": False, "why": result.get("outcome")}
    diffs = []
    for line, expected in spec["hand"].items():
        got = (result.get("lines") or {}).get(line)
        if got != expected:
            diffs.append({"line": line, "hand": expected, "got": got})
    return {
        "matches_instruction": not diffs and not result.get("code_l_part") and result.get("disposition") == "published",
        "disposition": result.get("disposition"),
        "code_l_part": result.get("code_l_part"),
        "diffs": diffs[:14],
    }


def main() -> None:
    core = V85
    specs = build_cases(core)
    only = os.environ.get("CODEL_ONLY")
    if only:
        specs = [spec for spec in specs if spec["id"] in only.split(",")]
    workers = int(os.environ.get("CODEL_WORKERS") or min(4, os.cpu_count() or 2))
    items = [(spec["id"], core, spec["acts"]) for spec in specs]
    found: dict[str, dict[str, Any]] = {}
    with ProcessPoolExecutor(max_workers=workers) as pool:
        done = 0
        for case_id, result in pool.map(_one, items):
            found[case_id] = result
            done += 1
            print(f"{done}/{len(items)} {case_id} {result.get('disposition') or result.get('outcome')}", flush=True)
    rows = []
    for spec in specs:
        result = found[spec["id"]]
        rows.append({
            "id": spec["id"],
            "note": spec["note"],
            "instruction_settled": spec["instruction_settled"],
            "form_8949_rows": spec["form_8949_rows"],
            "hand": spec["hand"],
            "result": result,
            "comparison": compare(spec, result),
        })
    out = {
        "core": {"package": "v85", "registry": "v83", "release": "v83"},
        "harness_module": HARNESS,
        "cases": rows,
    }
    (HERE / "probe-output-v85.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    matched = sum(1 for row in rows if row["comparison"].get("matches_instruction"))
    print(f"wrote {len(rows)} cases, instruction match {matched}")


if __name__ == "__main__":
    main()
