"""P0 probes for Form 1099-B box 7 on core v83, and on a scratch core when one is named.

Evidence for docs/phases/engine-breadth/milestones/f1099b-box7-loss.md.
Charter: docs/reviews/f1099b-box7-loss/charter-p0.md.

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

HARNESS = "f1099b_box7_audit_harness"
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
BOX4_AMOUNT = P + "f1099b.statement-box4-withholding"
V83 = h.Core("v83", "v81", "v81")
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
    """Schedule D and Form 1040 from column (h) amounts. A refused case is not this dict."""
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


def say_statement(acts: list[dict[str, Any]], core: Any, fact_type: str, statement: str, value: object) -> list[dict[str, Any]]:
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
        f"demo.b7.{fact_type.split('.')[-1]}.{statement.split('.')[-2]}", fact_id, value)})
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


def box4_zero(acts: list[dict[str, Any]], core: Any) -> list[dict[str, Any]]:
    for statement in statements_of(acts):
        acts = say_statement(acts, core, BOX4_AMOUNT, statement, 0)
    return acts


def box7(acts: list[dict[str, Any]], core: Any, answers: dict[str, str | None]) -> list[dict[str, Any]]:
    """``answers`` maps a statement id, or ``*``, to yes, no, or None (leave unanswered)."""
    for statement in statements_of(acts):
        value = answers.get(statement, answers.get("*"))
        if value is not None:
            acts = say_statement(acts, core, BOX7, statement, value)
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
            successor = f"demo.b7.rm.{tag}.{fam.removeprefix(P)}.h{len(h.horizons(out, fam))}"
            h._add(out, "member-transition", {
                "family": {"id": fam, "version": h.SALE_KINDS[kind]["version"]},
                "scope": {"tax-year": YEAR, "subject": "demo.primary"},
                "member": {"action": "remove", "fact_id": fact_id},
                "successor": {"id": successor, "predecessor": head},
            })
            if per_family:
                h._close(out, fam + ".source-closure", successor, f"demo.b7.rm.{tag}.{fam.removeprefix(P)}.closure")
    return h.renumber(out)


def supersede_basis(acts: list[dict[str, Any]], kind: str, term: str, tag: str, basis: float) -> list[dict[str, Any]]:
    """Correct the same sale on the ordinary assertion path. The fact id stays; the finding id is new.

    A member-transition that asserts a fact already in the family is rejected. Same-member
    correction is a plain assertion, and the family stays closed.
    """
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
            if kind == "codeb":
                value["corrected_basis"] = basis
        else:
            value = basis
        h._add(out, "assertion", {"finding": h._attested(
            f"demo.b7.ch.{tag}.{fam.removeprefix(P)}.{scalar or 'sale'}",
            prior["fact_id"],
            value,
        )})
    return h.renumber(out)


def prepare(acts: list[dict[str, Any]], core: Any, kinds: set[str], loss: bool) -> list[dict[str, Any]]:
    answers = h.honest(kinds, loss=loss, new_questions=False)
    answers.update(h.honest_exception1(acts))
    acts = h.answer(acts, core.content, **{key: value for key, value in answers.items() if value is not None})
    return box4_zero(acts, core)


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
            if sentence.endswith("?") and sentence not in questions:
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
        if row.get("disposition") == "blocked" and (
                "box7" in artifact or artifact.endswith("schedule-d-line16")):
            blocked.append({
                "artifact": artifact.removeprefix(P + "rule."),
                "code": row.get("code"),
                "missing": [str(item).removeprefix(P) for item in (row.get("missing") or [])][:6],
            })
    line16 = lines.get("schedule-d.line-16")
    if line16 == "blocked" or (isinstance(line16, str) and "blocked" in line16):
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
        "questions": [h.scrub(question)[:240] for question in questions],
        "reasons": reasons,
        "blocked": blocked[:12],
    }


def _one(item: tuple[str, Any, list[dict[str, Any]]]) -> tuple[str, dict[str, Any]]:
    case_id, core, acts = item
    return case_id, run_case(core, acts, "demo.b7." + case_id)


def build_cases(core: Any) -> list[dict[str, Any]]:
    """Every case in the plan's 'Cases that will shape the design'."""
    def base(*sales: tuple) -> list[dict[str, Any]]:
        acts = h.opened()
        for kind, term, tag, kw in sales:
            acts = h.sale(acts, kind, term, tag=tag, **kw)
        return acts

    specs: list[dict[str, Any]] = []

    def add(case_id: str, acts: list[dict[str, Any]], kinds: set[str], loss: bool,
            answers: dict[str, str | None], sales: list[tuple[str, str, float]],
            *, expect: str, note: str, after: Any = None) -> None:
        acts = prepare(acts, core, kinds, loss)
        if after is not None:
            acts = after(acts)
            fresh = h.honest_exception1(acts)
            # With no sale left, the harness leaves the earlier answers standing.
            # A removed sale is no longer a gain or a loss, so both Exception 1 answers are yes.
            if fresh.get("exc1_only_2a") is None and fresh.get("exc1_no_losses") is None:
                fresh = {"exc1_only_2a": "yes", "exc1_no_losses": "yes"}
            acts = h.answer(acts, core.content, **{
                key: value for key, value in fresh.items() if value is not None})
        acts = box7(acts, core, answers)
        hand = hand_return(sales) if expect == "published" else None
        specs.append({
            "id": case_id, "expect": expect, "note": note, "acts": acts,
            "hand": hand, "column_h": [{"kind": kind, "term": term, "h": amount} for kind, term, amount in sales],
        })

    gain = {"proceeds": 5000, "basis": 4000}
    loss = {"proceeds": 4000, "basis": 5000}
    zero = {"proceeds": 4000, "basis": 4000}
    add("yes_gain_covered_st", base(("covered", "st", "g", gain)), {"covered"}, False, {"*": "yes"},
        [("covered", "st", 1000)], expect="published",
        note="Box 7 yes, one covered short-term gain. The gain is allowed.")
    add("yes_loss_covered_st", base(("covered", "st", "ls", loss)), {"covered"}, True, {"*": "yes"},
        [("covered", "st", -1000)], expect="blocked",
        note="Box 7 yes and column (h) is -1000. The loss is not published.")
    add("yes_loss_covered_lt", base(("covered", "lt", "ll", loss)), {"covered"}, True, {"*": "yes"},
        [("covered", "lt", -1000)], expect="blocked", note="Box 7 yes, one covered long-term loss.")
    add("yes_loss_covered_w_st", base(("w", "st", "ws", {**loss, "wash": 400})), {"w"}, True, {"*": "yes"},
        [("w", "st", -600)], expect="blocked",
        note="Code W wash of 400 leaves column (h) at -600. Still a loss.")
    add("yes_loss_covered_w_lt", base(("w", "lt", "wl", {**loss, "wash": 400})), {"w"}, True, {"*": "yes"},
        [("w", "lt", -600)], expect="blocked", note="Code W long-term, wash leaves a loss.")
    add("yes_loss_noncovered_st", base(("noncovered", "st", "ns", loss)), {"noncovered"}, True, {"*": "yes"},
        [("noncovered", "st", -1000)], expect="blocked", note="Box 7 yes, noncovered short-term loss, wash zero.")
    add("yes_loss_noncovered_lt", base(("noncovered", "lt", "nl", loss)), {"noncovered"}, True, {"*": "yes"},
        [("noncovered", "lt", -1000)], expect="blocked", note="Box 7 yes, noncovered long-term loss.")
    add("yes_loss_code_b_st", base(("codeb", "st", "bs", loss)), {"codeb"}, True, {"*": "yes"},
        [("codeb", "st", -1000)], expect="blocked",
        note="Code B short-term. Corrected basis equals basis, so column (h) is proceeds minus basis.")
    add("yes_loss_code_b_lt", base(("codeb", "lt", "bl", loss)), {"codeb"}, True, {"*": "yes"},
        [("codeb", "lt", -1000)], expect="blocked", note="Code B long-term loss.")
    add("yes_zero_covered_st", base(("covered", "st", "z", zero)), {"covered"}, False, {"*": "yes"},
        [("covered", "st", 0)], expect="published",
        note="Box 7 yes and column (h) is exactly zero. Zero is not a loss.")
    same = h.opened()
    same = h.sale(same, "covered", "st", tag="mixg", **gain)
    same = sale_on(same, "covered", "st", "mixl", statement_tag="mixg", **loss)
    add("yes_gain_and_loss_same_statement", same, {"covered"}, True, {"*": "yes"},
        [("covered", "st", 1000), ("covered", "st", -1000)], expect="blocked",
        note="One statement, box 7 yes, a gain and a loss. The loss must not be published, so line 16 is refused.")
    both = h.opened()
    both = h.sale(both, "covered", "st", tag="btg", **gain)
    both = sale_on(both, "covered", "lt", "btl", statement_tag="btg", **loss)
    add("yes_gain_and_loss_both_terms", both, {"covered"}, True, {"*": "yes"},
        [("covered", "st", 1000), ("covered", "lt", -1000)], expect="blocked",
        note="Box 7 yes, short-term gain and long-term loss on the same statement.")
    add("yes_wash_to_zero", base(("w", "st", "wz", {**loss, "wash": 1000})), {"w"}, False, {"*": "yes"},
        [("w", "st", 0)], expect="published",
        note="Code W wash brings column (h) from -1000 to zero. Box 7 yes does not change the result.")
    cross = h.opened()
    cross = h.sale(cross, "covered", "st", tag="ya", **gain)
    cross = h.sale(cross, "covered", "st", tag="nb", proceeds=2000, basis=2400)
    add("yes_on_gain_statement_loss_on_other", cross, {"covered"}, True,
        {"demo.sfa.ya.statement": "yes", "demo.sfa.nb.statement": "no"},
        [("covered", "st", 1000), ("covered", "st", -400)], expect="published",
        note="Box 7 yes on the gain statement only. The loss is on a statement answered no, so it is allowed. Net +600.")
    add("unanswered_beside_gain", base(("covered", "st", "ug", gain)), {"covered"}, False, {},
        [("covered", "st", 1000)], expect="blocked",
        note="A gain with no box 7 answer. The question is still asked.")
    add("unanswered_beside_loss", base(("covered", "st", "ul", loss)), {"covered"}, True, {},
        [("covered", "st", -1000)], expect="blocked",
        note="A loss with no box 7 answer. The question is asked and no loss is published.")
    removed = base(("covered", "st", "rm", gain))
    add("sale_removed_after_box7_yes", removed, {"covered"}, False, {"*": "yes"}, [],
        expect="published",
        note="Box 7 was answered yes, then the only sale was removed. No sale remains for box 7 to change.",
        after=lambda acts: remove_sale(acts, "covered", "st", "rm"))
    changed = base(("covered", "st", "ch", gain))
    add("sale_changed_gain_to_loss", changed, {"covered"}, False, {"*": "yes"},
        [("covered", "st", -1000)], expect="blocked",
        note="Box 7 was answered yes on a gain, then the same sale's basis was superseded to 6000, so column (h) is -1000.",
        after=lambda acts: supersede_basis(acts, "covered", "st", "ch", 6000))
    add("no_with_loss", base(("covered", "st", "ok", loss)), {"covered"}, True, {"*": "no"},
        [("covered", "st", -1000)], expect="published",
        note="Control. Box 7 no beside a loss. Core v83 publishes this loss.")
    add("yes_both_terms_both_gains", base(("covered", "st", "sg", gain), ("covered", "lt", "lg", gain)),
        {"covered"}, False, {"*": "yes"},
        [("covered", "st", 1000), ("covered", "lt", 1000)], expect="published",
        note="Box 7 yes, a short-term gain and a long-term gain. Both are allowed, and the long-term gain is preferential.")
    return specs


def compare(spec: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    if result.get("outcome") != "success":
        return {"matches_hand": False, "why": result.get("outcome")}
    if spec["expect"] == "blocked":
        published_loss = result["disposition"] == "published" and any(row["h"] < 0 for row in spec["column_h"])
        return {
            "matches_hand": result["disposition"] == "blocked" and not published_loss,
            "why": "blocked" if result["disposition"] == "blocked" else result["disposition"],
        }
    diffs = []
    for line, expected in (spec["hand"] or {}).items():
        got = (result.get("lines") or {}).get(line)
        if got != expected:
            diffs.append({"line": line, "hand": expected, "got": got})
    return {"matches_hand": not diffs, "diffs": diffs[:12]}


def main() -> None:
    core = V83
    label = "v83"
    if len(sys.argv) > 1:
        body = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        core = h.Core(body["version"], body["registry"], body["release_version"],
                      content=Path(body["content"]), releases=Path(body["releases"]),
                      loader_from=body.get("loader_from"))
        label = "v84"
    specs = build_cases(core)
    only = os.environ.get("BOX7_ONLY")
    if only:
        specs = [spec for spec in specs if spec["id"] in only.split(",")]
    workers = int(os.environ.get("BOX7_WORKERS") or min(4, os.cpu_count() or 2))
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
            "expect": spec["expect"],
            "column_h": spec["column_h"],
            "hand": spec["hand"],
            "result": {key: value for key, value in result.items()},
            "comparison": compare(spec, result),
        })
    payload = {"core": label, "cases": rows}
    text = h.scrub(json.dumps(payload, indent=2) + "\n")
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"probe output contains {needle}")
    out = HERE / f"probe-output-{label}.json"
    out.write_text(text, encoding="utf-8")
    bad = [row["id"] for row in rows if not row["comparison"].get("matches_hand")]
    print(json.dumps({"core": label, "cases": len(rows), "differ_from_hand": bad}, indent=2))


if __name__ == "__main__":
    # Spawned workers re-import this file as __main__. The env var stops them from running the suite.
    if os.environ.get("BOX7_PROBE_WORKER") != "1":
        os.environ["BOX7_PROBE_WORKER"] = "1"
        main()
