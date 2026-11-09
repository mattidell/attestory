"""P0 probes of the sale family audit: every case on a core, against hand values.

Evidence for docs/phases/engine-breadth/milestones/sale-family-audit.md.
Synthetic demo.* returns built by ``audit_harness.py`` (loaded under a unique
module name; no other evidence module is imported or changed). Each case runs
through ``live_coordinate_run`` on the core given (the published v81 by
default, or the scratch v82 that ``prototype.py`` builds).

    python3 docs/phases/engine-breadth/milestones/sale-family-audit-evidence/probe.py [workers] [case ...]

Writes probe-output.json beside this file. Hand values come from ``hand``:
the harness wage return is single, wages 50,000, W-2 withholding 4,500,
standard deduction 15,750, so taxable income is 34,250 plus Form 1040 line
7a. Tax is the 2025 Tax Table (the tax on the midpoint of each $50 row,
rounded) and, with a preferential base, the Qualified Dividends and Capital
Gain Tax Worksheet (0% up to 48,350 of taxable income for a single filer).
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
OUT = HERE / "probe-output.json"
HARNESS = "sale_family_audit_harness"


def harness() -> Any:
    module = sys.modules.get(HARNESS)
    if module is None:
        spec = importlib.util.spec_from_file_location(HARNESS, HERE / "audit_harness.py")
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[HARNESS] = module
        spec.loader.exec_module(module)
    return module


h = harness()
Acts = list[dict[str, Any]]

# ---- hand values ------------------------------------------------------------------


def _bracket(x: float) -> float:
    tax = 0.10 * min(x, 11925)
    if x > 11925:
        tax += 0.12 * (min(x, 48475) - 11925)
    if x > 48475:
        tax += 0.22 * (min(x, 103350) - 48475)
    return tax


def table(ti: float) -> int:
    """2025 Tax Table for a single filer: the tax on the row's midpoint, rounded half up."""
    if ti <= 0:
        return 0
    mid = math.floor(ti / 50) * 50 + 25 if ti >= 3000 else math.floor(ti / 25) * 25 + 12.5
    return int(math.floor(_bracket(mid) + 0.5))


def qdcg(ti: float, pref: float) -> int:
    if pref <= 0:
        return table(ti)
    ordinary = ti - pref
    zero_band = max(0.0, min(ti, 48350) - ordinary)
    fifteen = max(0.0, pref - zero_band)
    return min(table(ti), int(math.floor(table(ordinary) + 0.15 * fifteen + 0.5)))


def hand(st: float = 0, lt: float = 0, *, cgd: float = 0, b25: float = 0, f8949: bool | None = None,
         schedule_d: bool | None = True) -> dict[str, Any]:
    """The correct return: Schedule D Part I net ``st``, Part II net ``lt`` (before line 13)."""
    line7, line15 = st, lt + cgd
    line16 = line7 + line15
    line21 = min(3000.0, -line16) if line16 < 0 else 0.0
    line7a = line16 if line16 >= 0 else -line21
    ti = max(0.0, 34250 + line7a)
    pref = 0.0 if (line15 < 0 or line16 < 0) else min(line15, line16)
    tax = qdcg(ti, pref)
    payments = 4500 + b25
    out: dict[str, Any] = {
        "schedule-d.line-7": line7, "schedule-d.line-15": line15, "schedule-d.line-16": line16,
        "form1040.line-7a": line7a, "form1040.line-15": ti, "form1040.line-16": tax,
        "form1040.line-25b": b25, "form1040.line-34": max(0, payments - tax), "form1040.line-37": max(0, tax - payments),
    }
    out = {k: int(v) if float(v).is_integer() else v for k, v in out.items()}
    if f8949 is not None:
        out["attach.f8949"] = f8949
    if schedule_d is not None:
        out["attach.schedule-d"] = schedule_d
        # Line 7b, "Schedule D not required", is checked exactly when Schedule D is not (review F2).
        out["form1040.line-7b"] = "guard_inapplicable" if schedule_d else "published_categorical"
    return out


# ---- cases -------------------------------------------------------------------------

CASES: dict[str, dict[str, Any]] = {}


def case(name: str, *, kinds: set[str], sales: Callable[[Acts], Acts], expect: str, hand_values: dict[str, Any] | None,
         loss: bool = False, answers: dict[str, str | None] | None = None, extra: Callable[[Acts], Acts] | None = None,
         group: str, note: str) -> None:
    """``expect``: "values" (the hand values must publish) or "block" (a correct core refuses)."""
    CASES[name] = {"kinds": sorted(kinds), "sales": sales, "expect": expect, "hand": hand_values, "loss": loss,
                   "answers": answers or {}, "extra": extra, "group": group, "note": note}


MODES = ("honest", "base_exception1")


def build(spec: dict[str, Any], mode: str = "honest", core: Any = None) -> Acts:
    """``mode`` "honest" answers the Exception 1 question as a filer with these sales does
    (yes: another capital gain or loss). "base_exception1" keeps the harness base's answers
    (only box 2a gains, no capital losses), as every earlier sale milestone's cases did."""
    acts = h.opened()
    if spec["extra"] is not None:
        acts = spec["extra"](acts)
    acts = spec["sales"](acts)
    core = core or h.V81
    new_questions = (core.content / "f1099b-statement-boxes.bundle.json").exists()
    answers = {**h.honest(set(spec["kinds"]), loss=spec["loss"], new_questions=new_questions), **spec["answers"]}
    if not new_questions:
        answers = {k: v for k, v in answers.items() if k not in ("box4", "box7")}
    if mode == "base_exception1":
        answers = {k: v for k, v in answers.items() if not k.startswith("exc1")}
    return h.answer(acts, core.content, **answers)


def S(kind: str, term: str, tag: str, **kw: Any) -> Callable[[Acts], Acts]:
    return lambda acts: h.sale(acts, kind, term, tag=tag, **kw)


def seq(*steps: Callable[[Acts], Acts]) -> Callable[[Acts], Acts]:
    def run(acts: Acts) -> Acts:
        for step in steps:
            acts = step(acts)
        return acts
    return run


def with_2a(amount: float) -> Callable[[Acts], Acts]:
    """A Form 1099-DIV box 2a capital gain distribution with its box 4 row (0), both families closed."""
    def add(acts: Acts) -> Acts:
        from tests import test_collect_closure as cc
        acts = cc._add_member(acts, h.P + "f1099div.2a", amount, close=True, tag="sfacgd")
        acts = h.renumber(acts)
        stmt = (("payer", "demo.cc.sfacgd.payer"), ("statement", "demo.cc.sfacgd.statement"))
        fam = h.P + "f1099div.b4"
        acts = h.strip(acts, fam + ".source-closure")
        head = h.horizons(acts, fam)[-1]
        h._add(acts, "member-transition", {
            "family": {"id": fam, "version": "v1"}, "scope": {"tax-year": h.YEAR, "subject": "demo.primary"},
            "member": {"action": "assert", "finding": h._attested(
                "demo.sfa.cgd.b4", h.fact_id_for(h.P + "f1099div.box4-withholding", (*stmt, ("tax-year", h.YEAR))), 0.0)},
            "successor": {"id": "demo.sfa.cgd.b4.h1", "predecessor": head}})
        h._close(acts, fam + ".source-closure", "demo.sfa.cgd.b4.h1", "demo.sfa.cgd.b4.closure")
        acts = h.say(acts, h.P + "capital-gain-distributions", "yes", "cgd")
        return h.renumber(acts)
    return add


ALL8949 = {"f8949": True, "schedule_d": True}

# A. Fields the sale records carry that no rule reads.
case("a1_direct_flagged_wash", kinds={"w"}, group="A", expect="block", loss=True,
     sales=S("covered", "st", "a1", proceeds=4000, basis=5000, box_1g_wash_sale_adjustment="yes"),
     hand_values=hand(st=-700, **ALL8949),
     note="Box A sale recorded on the line 1a family with box 1g checked (box 1g 300, which the record cannot "
          "carry). Exception 1 excludes it; on Form 8949 box A with code W it is 4,000 - 5,000 + 300 = -700.")
case("a2_direct_st_family_long_term", kinds={"covered"}, group="A", expect="block",
     sales=S("covered", "st", "a2", proceeds=10000, basis=7000, long_term="yes"),
     hand_values=hand(lt=3000),
     note="A long-term sale (box 2 long-term, long_term yes) recorded on the short-term line 1a family. "
          "Correct: line 8a 3,000, taxed at 0%.")
case("a3_w_st_family_long_term", kinds={"covered", "w"}, group="A", expect="block", loss=True,
     sales=seq(S("covered", "lt", "a3l", proceeds=10000, basis=5000), S("covered", "st", "a3s", proceeds=4000, basis=2000),
               S("w", "st", "a3w", proceeds=4000, basis=5000, wash=300, long_term="yes")),
     hand_values=hand(st=2000, lt=4300, f8949=True),
     note="A long-term code W loss (-700) recorded on the short-term code W family beside a 2,000 short-term "
          "and a 5,000 long-term gain. Correct: line 7 2,000, line 15 4,300, preferential base 4,300.")
case("a4_covered_security_no", kinds={"covered"}, group="A", expect="values",
     sales=S("covered", "st", "a4", proceeds=10000, basis=7000, covered_security="no"),
     hand_values=hand(st=3000),
     note="Box 5 checked but basis reported (box 12): Form 8949 box A follows box 12, so the return is unchanged.")
case("a5_covered_basis_not_reported", kinds={"covered"}, group="A", expect="block",
     sales=S("covered", "st", "a5", proceeds=10000, basis=7000, basis_reported_to_irs="no"),
     hand_values=None,
     note="A covered-family sale whose basis was not reported: the engine's covered-flag refusal.")

# B. Form 1099-B boxes no sale record carries.
case("b1_box4_backup_withholding", kinds={"noncovered"}, group="B", expect="block",
     sales=S("noncovered", "lt", "b1", proceeds=6000, basis=2000), answers={"box4": "yes"},
     hand_values=hand(lt=4000, b25=1440, f8949=True),
     note="Form 1099-B box 4 shows 1,440 backup withholding. No record or question carries it. Correct: "
          "line 25b 1,440, refund 2,065.")
case("b2_box7_loss_not_allowed", kinds={"noncovered"}, group="B", expect="block", loss=True,
     sales=S("noncovered", "lt", "b2", proceeds=3000, basis=5000), answers={"box7": "yes"},
     hand_values=None,
     note="Box 7 checked: no loss may be taken on the box 1d gross proceeds of a reportable change in control. "
          "The record has no box 7; the honest in-class answers are given.")
case("b3_code_e_on_direct_refused", kinds={"covered"}, group="B", expect="block",
     sales=S("covered", "st", "b3", proceeds=10000, basis=7000),
     answers={"form8949": "no", "path_b": "no"},
     hand_values=hand(st=2900, **ALL8949),
     note="A 100 selling expense not reflected in box 1d (code E). The honest Path B answer is no.")
case("b4_collectibles_box_b", kinds={"noncovered"}, group="B", expect="block",
     sales=S("noncovered", "lt", "b4", proceeds=6000, basis=2000), answers={"lines_18_19": "no"},
     hand_values=None, note="Box 3 collectibles on a box E sale: the honest lines 18-19 answer is no.")
case("b5_ordinary_box_e", kinds={"noncovered"}, group="B", expect="block",
     sales=S("noncovered", "lt", "b5", proceeds=6000, basis=2000), answers={"ic79": "no"},
     hand_values=None, note="Box 2 Ordinary (code O) on a box E sale: the honest in-class answer is no.")
case("b6_qof_box_e", kinds={"noncovered"}, group="B", expect="block",
     sales=S("noncovered", "lt", "b6", proceeds=6000, basis=2000), answers={"no_da_qof": "no"},
     hand_values=None, note="Box 3 QOF on a box E sale: the honest QOF answer is no.")

# C. Consumers a family does not reach.
case("c1_direct_zero_proceeds", kinds={"covered"}, group="C", expect="values", loss=True,
     sales=S("covered", "st", "c1", proceeds=0, basis=500), hand_values=hand(st=-500),
     note="A direct sale with zero proceeds, honest Exception 1 answer.")
case("c2_w_full_disallowance", kinds={"w"}, group="C", expect="values", loss=True,
     sales=S("w", "st", "c2", proceeds=4000, basis=5000, wash=1000), hand_values=hand(st=0, **ALL8949),
     note="A code W loss fully disallowed: column (h) 0.")
case("c3_direct_zero_proceeds_with_2a", kinds={"covered"}, group="C", expect="values", loss=True,
     extra=with_2a(1000), sales=S("covered", "lt", "c3", proceeds=0, basis=500),
     hand_values=hand(lt=-500, cgd=1000),
     note="A zero-proceeds direct long-term loss beside a 1,000 capital gain distribution. Line 15 500, line 16 "
          "500, preferential base 500.")
case("c4_no1099b_zero_zero", kinds={"no1099b"}, group="C", expect="values",
     sales=S("no1099b", "st", "c4", proceeds=0, basis=0), hand_values=hand(**ALL8949),
     note="A box C sale for 0 with basis 0: Form 8949 box C and Schedule D line 3 report it.")

# D. Value edges on every family.
FAMILY_EDGE: dict[str, dict[str, Any]] = {
    "covered": {}, "w": {}, "noncovered": {}, "no1099b": {}, "codeb": {"corrected": None},
}
for kind in ("covered", "w", "noncovered", "no1099b", "codeb"):
    f8949 = None if kind == "covered" else True
    case(f"d1_{kind}_negative_proceeds", kinds={kind}, group="D", expect="block", loss=True,
         sales=S(kind, "st", f"d1{kind}", proceeds=-500, basis=100, **({"corrected": 200} if kind == "codeb" else {})),
         hand_values=None, note="Box 1d in parentheses (a loss on a forward or non-1256 option): outside the class.")
    kw: dict[str, Any] = {"corrected": 600} if kind == "codeb" else {}
    case(f"d2_{kind}_zero_proceeds", kinds={kind}, group="D", expect="values", loss=True,
         sales=S(kind, "st", f"d2{kind}", proceeds=0, basis=500, **({"wash": 0} if kind == "w" else {}), **kw),
         hand_values=hand(st=-600 if kind == "codeb" else -500, f8949=f8949),
         note="Zero proceeds, basis 500 (code B: shown 500, correct 600).")
    kw = {"corrected": 100} if kind == "codeb" else {}
    case(f"d3_{kind}_zero_zero", kinds={kind}, group="D", expect="values", loss=kind == "codeb",
         sales=S(kind, "st", f"d3{kind}", proceeds=0, basis=0, **kw),
         hand_values=hand(st=-100 if kind == "codeb" else 0, f8949=f8949),
         note="Zero proceeds and zero basis (code B: correct basis 100).")
    kw = {"corrected": 5000, "basis": 4000} if kind == "codeb" else {"basis": 5000}
    case(f"d4_{kind}_equal", kinds={kind}, group="D", expect="values",
         sales=S(kind, "st", f"d4{kind}", proceeds=5000, **kw), hand_values=hand(st=0, f8949=f8949),
         note="Proceeds equal to basis (code B: shown 4,000, correct 5,000).")
    if kind != "covered":
        kw = {"corrected": 5000, "basis": 4500} if kind == "codeb" else {"basis": 5000}
        case(f"d5_{kind}_wash_full", kinds={kind}, group="D", expect="values", loss=True,
             sales=S(kind, "st", f"d5{kind}", proceeds=4000, wash=1000, **kw), hand_values=hand(st=0, f8949=True),
             note="Basis above proceeds with the whole loss disallowed (code W, or BW).")
case("d6_w_adjustment_row_disagrees", kinds={"w"}, group="D", expect="block", loss=True,
     sales=S("w", "st", "d6", proceeds=4000, basis=5000, wash=300, rows={"adjustment": 3000}),
     hand_values=None, note="The sale says box 1g 300; its column (g) row says 3,000, more than the 1,000 loss.")
case("d7_covered_rows_disagree", kinds={"covered"}, group="D", expect="block",
     sales=S("covered", "st", "d7", proceeds=10000, basis=7000, rows={"basis": 4000}),
     hand_values=None, note="The sale says basis 7,000; its basis row says 4,000.")
case("d8_covered_rows_missing", kinds={"covered"}, group="D", expect="block",
     sales=S("covered", "st", "d8", proceeds=10000, basis=7000, rows={"proceeds": None, "basis": None}),
     hand_values=None, note="The sale is recorded; its proceeds and basis rows are not.")

# E. One transaction on two families (same broker, statement and transaction).
SLOTS = [(k, t) for k in ("covered", "w", "noncovered", "codeb") for t in ("st", "lt")]


def _dup_sale(kind: str, term: str) -> Callable[[Acts], Acts]:
    kw: dict[str, Any] = {"proceeds": 10000, "basis": 7000}
    if kind == "w":
        kw = {"proceeds": 4000, "basis": 5000, "wash": 300}
    if kind == "codeb":
        kw = {"proceeds": 10000, "basis": 7000, "corrected": 4000}
    return S(kind, term, "dup", **kw)


for i, (k1, t1) in enumerate(SLOTS):
    for k2, t2 in SLOTS[i + 1:]:
        case(f"e_{k1}_{t1}__{k2}_{t2}", kinds={k1, k2}, group="E", expect="block", loss=True,
             sales=seq(_dup_sale(k1, t1), _dup_sale(k2, t2)), hand_values=None,
             note="The same transaction recorded on two families.")

# F. Controls: one sale per family and term.
CONTROLS = {
    "covered": ({"proceeds": 10000, "basis": 7000}, 3000), "w": ({"proceeds": 4000, "basis": 5000, "wash": 300}, -700),
    "noncovered": ({"proceeds": 6000, "basis": 2000}, 4000), "no1099b": ({"proceeds": 2500, "basis": 1000}, 1500),
    "codeb": ({"proceeds": 10000, "basis": 7000, "corrected": 4000}, 6000),
}
for kind, (kw, gain) in CONTROLS.items():
    for term in ("st", "lt"):
        case(f"f_{kind}_{term}", kinds={kind}, group="F", expect="values", loss=gain < 0,
             sales=S(kind, term, f"f{kind}{term}", **kw),
             hand_values=hand(**({term: gain}), f8949=None if kind == "covered" else True),
             note="Control.")
case("f_two_unrelated_covered", kinds={"covered"}, group="F", expect="values",
     sales=seq(S("covered", "st", "fu1", proceeds=10000, basis=7000), S("covered", "lt", "fu2", proceeds=6000, basis=2000)),
     hand_values=hand(st=3000, lt=4000), note="Two different transactions, one per term: not a duplicate.")


# ---- run ----------------------------------------------------------------------------


def core_from(arg: str | None) -> Any:
    if not arg:
        return h.V81
    spec = json.loads(arg)
    return h.Core(spec["version"], spec["registry"], spec["release_version"], Path(spec["content"]),
                  Path(spec["releases"]), spec.get("loader_from"),
                  tuple(tuple(p) for p in spec.get("presence_pairs") or ()))


def verdict(spec: dict[str, Any], result: dict[str, Any]) -> str:
    if "error" in result or "refusal" in result:
        return "rejected at entry"
    lines = result.get("lines") or {}
    published = all(isinstance(lines.get(k), int) for k in ("form1040.line-16", "form1040.line-34", "form1040.line-37"))
    if spec["expect"] == "block":
        if not published:
            return "blocks (correct)"
        if spec["hand"] is not None and not mismatches(spec, result):
            return "publishes the right values (a block was expected)"
        return "WRONG RETURN PUBLISHED"
    if not published:
        return "BLOCKS A RETURN IT SHOULD COMPUTE"
    return "right" if not mismatches(spec, result) else "WRONG RETURN PUBLISHED"


def mismatches(spec: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    lines = result.get("lines") or {}
    attachments = result.get("attachments") or {}
    for key, want in (spec["hand"] or {}).items():
        if key.startswith("attach."):
            got = attachments.get(key.removeprefix("attach.")) == "published"
        else:
            got = lines.get(key)
        if got != want:
            out[key] = [got, want]
    return out


KEPT_LINES = ("schedule-d.line-1a", "schedule-d.line-1b", "schedule-d.line-2", "schedule-d.line-3", "schedule-d.line-7",
              "schedule-d.line-8a", "schedule-d.line-8b", "schedule-d.line-9", "schedule-d.line-10",
              "schedule-d.line-15", "schedule-d.line-16", "schedule-d.line-21", "form1040.line-7a", "form1040.line-7b",
              "form1040.line-15", "form1040.line-16", "form1040.line-25b", "form1040.line-34", "form1040.line-37")


def compact(result: dict[str, Any]) -> dict[str, Any]:
    """The run, small: the error, or the watched lines, attachments, base, questions and first blocked rows."""
    if "error" in result or "refusal" in result:
        return {k: result[k] for k in ("error", "message", "refusal") if k in result}
    lines = result.get("lines") or {}
    return {"lines": {k: lines.get(k) for k in KEPT_LINES if k in lines}, "attachments": result.get("attachments"),
            "base": (result.get("symbols") or {}).get("capital-gains.selected-preferential-base"),
            "questions": result.get("questions"), "blocked": (result.get("blocked") or [])[:3]}


def execute(task: tuple[str, str, str | None]) -> tuple[str, str, dict[str, Any]]:
    name, mode, core_arg = task
    spec = CASES[name]
    core = core_from(core_arg)
    started = time.monotonic()
    try:
        acts = build(spec, mode, core)
    except Exception as exc:  # noqa: BLE001 — an act list the harness cannot build is a result
        result: dict[str, Any] = {"error": type(exc).__name__, "message": h.scrub(str(exc))[:300]}
    else:
        result = h.run(core, acts, f"demo.sfa.p0.{name}.{mode}")
    result["seconds"] = round(time.monotonic() - started, 1)
    return name, mode, result


def main() -> None:
    args = sys.argv[1:]
    workers = int(args.pop(0)) if args and args[0].isdigit() else 4
    core_arg = None
    if args and args[0].startswith("--core="):
        core_arg = args.pop(0).removeprefix("--core=")
    out_path = OUT if core_arg is None else HERE / f"probe-output-{json.loads(core_arg)['version']}.json"
    names = [n for n in CASES if not args or any(n.startswith(a) for a in args)]
    results: dict[str, Any] = {}
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for name, mode, result in pool.map(execute, [(n, m, core_arg) for n in names for m in MODES]):
            spec = CASES[name]
            entry = results.setdefault(name, {"group": spec["group"], "note": spec["note"], "expect": spec["expect"],
                                              "hand": spec["hand"]})
            entry[mode] = {"verdict": verdict(spec, result),
                           "mismatches": mismatches(spec, result) if spec["hand"] else {},
                           "result": compact(result)}
            print(f"{name:42s} {mode:16s} {entry[mode]['verdict']:42s} {result.get('seconds')}", flush=True)
    previous = json.loads(out_path.read_text(encoding="utf-8")) if args and out_path.exists() else {"cases": {}}
    previous["cases"].update(results)
    previous["core"] = "core-calculations " + (core_from(core_arg).version)
    out_path.write_text(h.scrub(json.dumps(previous, indent=1, sort_keys=True)) + "\n", encoding="utf-8")
    print(f"wrote {out_path.name}: {len(previous['cases'])} cases")


if __name__ == "__main__":
    main()
