"""Track 0 adversarial closure runs for Form 1099-B sales whose reported basis is wrong (code B).

Evidence for track0-closure.md beside this file. Builds the scratch core v81
of codeb_prototype.py in each worker process and runs every case through
live_coordinate_run. Nothing under packages/ is written. Writes
codeb-track0-output.json beside this file.

    python3 docs/phases/engine-breadth/milestones/f8949-code-b-evidence/codeb_track0.py [workers]
    python3 .../codeb_track0.py only <final|decided> case ...   # rerun named cases and merge them
    python3 .../codeb_track0.py surface                          # refresh the static integration surface

Two designs are built. ``final`` is codeb_prototype.REPAIRS as committed
(every Track 0 repair on). ``decided`` is Decisions 1-4 with no Track 0
repair; it runs every P0 and Track 0 case, so each counterexample a repair
fixes is shown beside its repaired result.

Modules are loaded under unique names (f8949-boxes-cf retrospective): this
file loads codeb_prototype as ``f8949_code_b_prototype``, which loads the
f8949-boxes-cf harness as ``f8949_boxes_cf_track0``.
"""

from __future__ import annotations

import atexit
import copy
import importlib.util
import json
import shutil
import sys
import tempfile
import time
import traceback
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
OUT = HERE / "codeb-track0-output.json"
Acts = list[dict[str, Any]]


def load(name: str, path: Path) -> Any:
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


cbp: Any = load("f8949_code_b_prototype", HERE / "codeb_prototype.py")
cfp, cp, probe, codeb_probe = cbp.cfp, cbp.cp, cbp.probe, cbp.codeb_probe
P = cbp.P
ccr = cbp.ccr
fact_id_for, _attested = cbp.fact_id_for, cbp._attested
Q1, Q2, Q3, IC2, IC3 = cbp.Q1, cbp.Q2, cbp.Q3, cbp.IC2, cbp.IC3
OLD_IC = cfp.OLD_IC
CLS = cbp.CLS
code_b, v81_return, say = cbp.code_b, cbp.v81_return, cbp.say

FIELDS = tuple(P + f"schedule-d.line-{n}" for n in ("1a", "1b", "2", "3", "7", "8a", "8b", "9", "10", "15", "16", "21")) + (
    P + "form1040.line-7a",)
PROBED_FIELDS = ("schedule-d.line-1b", "schedule-d.line-8b", "schedule-d.line-1a", "schedule-d.line-8a",
                 "schedule-d.line-2", "schedule-d.line-3", "schedule-d.line-9", "schedule-d.line-10")
# Publishers whose row count per run is the integration-surface cardinality.
PUBLISHERS = tuple(P + "rule." + n for n in (
    "schedule-d-line1a-gain", "schedule-d-line1b", "schedule-d-line2", "schedule-d-line3", "schedule-d-line7",
    "schedule-d-line8a-gain", "schedule-d-line8b", "schedule-d-line9", "schedule-d-line10", "schedule-d-line15",
    "schedule-d-line16", "schedule-d-line21", "form1040-line7a", "selected-preferential-base", "attachment.f8949",
    "attachment.schedule-d", "f1099b-code-b-st-gain", "f1099b-code-b-lt-gain", "f1099b.code-b-st-txn.amounts-check",
    "f1099b.code-b-lt-txn.amounts-check", "f1099b-code-b-st-count", "f1099b-code-b-lt-count",
    *(f"f1099b.{k}-{t}-txn.admission-check" for k in ("covered", "covered-w") for t in ("st", "lt")),
    *(f"f1099b.noncovered-{t}-txn.amounts-check" for t in ("st", "lt")),
    *(f"f1099b-{k}-{t}-count" for k in ("covered", "covered-w", "noncovered") for t in ("st", "lt"))))
codeb_probe.WHY_ROWS = tuple(dict.fromkeys(codeb_probe.WHY_ROWS + PUBLISHERS))


# ---- recording helpers --------------------------------------------------------


def identity(term: str, tag: str, *, transaction: str | None = None, acts: Acts | None = None) -> tuple[tuple[str, str], ...]:
    declared = []
    for key in cbp.sale_keys():
        if key["kind"] != "entity":
            declared.append((key["name"], key["values"][0]))
            continue
        entity = transaction if (transaction and key["name"] == "transaction") else f"demo.ns.{tag}.{key['name']}"
        if acts is not None and not cp.proto._known_entity(acts, entity):
            probe._introduce(acts, entity, key["entity_kind"])
        declared.append((key["name"], entity))
    return tuple(declared)


def record_raw(acts: Acts, term: str, kind: str | None, value: object, tag: str, *, transaction: str | None = None) -> None:
    """A code B member with an explicit transaction entity (cbp.record derives every entity from the tag)."""
    family_id = cbp.fam(term, kind)
    declared = identity(term, tag, transaction=transaction, acts=acts)
    head = probe.horizons(acts, family_id)[-1]
    slug = family_id.removeprefix(P + "f1099b.")
    n = len(probe.horizons(acts, family_id))
    probe._add(acts, "member-transition", {
        "family": {"id": family_id, "version": "v1"},
        "scope": {"tax-year": probe.YEAR, "subject": "demo.primary"},
        "member": {"action": "assert", "finding": _attested(
            f"demo.cb.{tag}.{slug}.member.h{n}", fact_id_for(cbp.member_fact(term, kind), declared), value)},
        "successor": {"id": f"demo.cb.{tag}.{slug}.h{n}", "predecessor": head},
    })


def correct_member(acts: Acts, term: str, kind: str | None, value: object, tag: str) -> Acts:
    """Same-member correction on the ordinary assertion path (free supersession)."""
    probe._add(acts, "assertion", {"finding": _attested(
        f"demo.cb.{tag}.{kind or 'sale'}.corrected", fact_id_for(cbp.member_fact(term, kind), identity(term, tag)), value)})
    return ccr._renumbered(acts)


def remove_member(acts: Acts, family_id: str, fact_id: str, tag: str, *, literal_closure: bool) -> Acts:
    """A member-transition that removes one member. Literal-closure families are closed again at the new horizon."""
    out = probe._strip_closure(copy.deepcopy(acts), family_id + ".source-closure") if literal_closure else copy.deepcopy(acts)
    head = probe.horizons(out, family_id)[-1]
    n = len(probe.horizons(out, family_id))
    successor = f"demo.rm.{tag}.h{n}"
    probe._add(out, "member-transition", {
        "family": {"id": family_id, "version": probe.family_version(out, family_id)},
        "scope": {"tax-year": probe.YEAR, "subject": "demo.primary"},
        "member": {"action": "remove", "fact_id": fact_id},
        "successor": {"id": successor, "predecessor": head},
    })
    if literal_closure:
        probe._close(out, family_id + ".source-closure", successor, f"demo.rm.{tag}.closure")
    return ccr._renumbered(out)


def covered_fact_id(acts: Acts, family_id: str, tag: str) -> str:
    fact_type_id, declared = probe._identity(acts, family_id, tag)
    return fact_id_for(fact_type_id, declared)


def covered_sale(acts: Acts, family: str, term: str, proceeds: float, basis: float, tag: str, *, wash: float | None = None) -> Acts:
    """A sale object on a v80 Form 1099-B family (covered-{term} or covered-w-{term}) keyed by ``tag``."""
    sale = probe.txn(proceeds=proceeds, basis=basis, long_term="yes" if term == "lt" else "no", wash=wash,
                     reported="yes", covered="yes")
    return probe.record(ccr._renumbered(acts), P + f"f1099b.{family}", sale, tag)


# ---- cases ------------------------------------------------------------------------


def ret(fn: Callable[[Acts], Any] | None = None, **kw: Any) -> Callable[[], Acts]:
    return lambda: v81_return(sales=fn, **{**CLS, **kw})


A_HIGH = (10000.0, 7000.0, 4000.0)
D_LOW = (6000.0, 2000.0, 3000.0)


def a_high(acts: Acts, tag: str = "ahigh") -> None:
    code_b(acts, "st", *A_HIGH, tag)


def d_low(acts: Acts, tag: str = "dlow") -> None:
    code_b(acts, "lt", *D_LOW, tag)


def basis_row_is_corrected(acts: Acts) -> None:
    """Rows carry the correct basis in column (e) and -0- in (g): right dollars, wrong column (e)."""
    cbp.record(acts, "st", None, {"proceeds": 10000.0, "basis": 7000.0, "corrected_basis": 4000.0, "long_term": "no",
                                  "wash_disallowed": 0.0}, "bce")
    for kind, value in (("proceeds", 10000.0), ("basis", 4000.0), ("adjustment", 0.0)):
        cbp.record(acts, "st", kind, value, "bce")


def shared_transaction(complete: bool) -> Callable[[Acts], None]:
    """Two code B sales on different statements that reuse one transaction entity."""
    def build(acts: Acts) -> None:
        code_b(acts, "st", *A_HIGH, "sh1")
        txn = "demo.ns.sh1.transaction"
        record_raw(acts, "st", None, {"proceeds": 5000.0, "basis": 3000.0, "corrected_basis": 9000.0, "long_term": "no",
                                      "wash_disallowed": 0.0}, "sh2", transaction=txn)
        rows = {"proceeds": 5000.0, "basis": 3000.0, "adjustment": -6000.0}
        for kind in (cbp.KINDS if complete else ("proceeds", "basis")):
            record_raw(acts, "st", kind, rows[kind], "sh2", transaction=txn)
    return build


def dup(family: str, term: str) -> Callable[[Acts], Acts]:
    """a_high, and the same transaction (same broker, statement and transaction entities) on a v80 family.

    codeb_probe.wash keys the sale object by ``tag + "o"``, so the code W duplicate records the code B sale under
    that tag too.
    """
    def build(acts: Acts) -> Acts:
        a_high(acts, "dupo" if family == "covered-w" else "dup")
        if family == "noncovered":
            cp.on_be(acts, term, 10000.0, 4000.0, "dup")
            return acts
        if family == "no1099b":
            cfp.cf_sale(acts, term, 10000.0, 4000.0, "dup")
            return acts
        if family == "covered":
            return codeb_probe.direct(ccr._renumbered(acts), term, 10000.0, 7000.0, "dup")
        # A code W row on the same transaction: 4000 / 5000 / W 300 (a loss, so the code W checks pass).
        return codeb_probe.wash(ccr._renumbered(acts), term, 4000.0, 5000.0, 300.0, "dup")
    return build


def nothing_beside(neighbour: str) -> Callable[[Acts], Any]:
    """A neighbouring family's sale on a return whose code B answer is yes with nothing recorded."""
    def build(acts: Acts) -> Any:
        if neighbour == "direct":
            return codeb_probe.direct(ccr._renumbered(acts), "st", 5000.0, 4000.0, "nbd")
        if neighbour == "w":
            return codeb_probe.wash(ccr._renumbered(acts), "st", 4000.0, 5000.0, 300.0, "nbw")
        if neighbour == "b":
            cp.on_be(acts, "st", 3000.0, 1000.0, "nbb")
            return None
        cfp.cf_sale(acts, "st", 2500.0, 1000.0, "nbc")
        return None
    return build


def late_trace(stage: int) -> Callable[[], Acts]:
    """T1: the wage return, harness Form 8949 'yes', code B 'no'; then the sale and each answer it needs."""
    def build() -> Acts:
        acts = v81_return(q1="no", q2="no", q3="no")
        if stage >= 1:
            a_high(acts, "t1")
        if stage >= 2:
            acts = say(acts, Q3, "yes", "t1q3")
        if stage >= 3:
            acts = probe.answer(ccr._renumbered(acts), IC3, "yes", "t1ic3")
        if stage >= 4:
            acts = probe.boundary(ccr._renumbered(acts), "no", "no")
        return ccr._renumbered(acts)
    return build


def correction_trace(stage: int, *, keep_covered: bool = False) -> Callable[[], Acts]:
    """T2: a covered box A sale reported on line 1a with the broker's wrong basis, corrected into a code B sale.

    Stage 0 is the v80 Exception 1 return (Form 8949 'yes', code B 'no'),
    which publishes the broker's gain. Stage 1 removes the covered sale and
    its rows and records the same transaction as a code B sale. Stages 2-4
    answer what that sale needs.
    """
    def build() -> Acts:
        acts = v81_return(q1="no", q2="no", q3="no",
                          sales=lambda a: codeb_probe.direct(ccr._renumbered(a), "st", 10000.0, 7000.0, "corr"))
        if stage >= 1:
            if not keep_covered:
                for family, tag in (("covered-st", "corr"), ("covered-st-proceeds", "corrp"), ("covered-st-basis", "corrb")):
                    family_id = P + f"f1099b.{family}"
                    acts = remove_member(acts, family_id, covered_fact_id(acts, family_id, tag), tag, literal_closure=True)
            a_high(acts, "corr")
        if stage >= 2:
            acts = say(acts, Q3, "yes", "corrq3")
        if stage >= 3:
            acts = probe.answer(ccr._renumbered(acts), IC3, "yes", "corric3")
        if stage >= 4:
            acts = probe.boundary(ccr._renumbered(acts), "no", "no")
        return ccr._renumbered(acts)
    return build


def w_to_bw_trace(stage: int) -> Callable[[], Acts]:
    """T3: a box A code W sale whose broker basis was wrong, corrected into a BW row (4000 / 4500 shown / 6000, W 1000)."""
    def build() -> Acts:
        acts = v81_return(q1="no", q2="no", q3="no", form8949="no", path_b="yes",
                          sales=lambda a: codeb_probe.wash(ccr._renumbered(a), "st", 4000.0, 4500.0, 300.0, "wbw"))
        if stage >= 1:
            for family, tag in (("covered-w-st", "wbwo"), ("covered-w-st-proceeds", "wbwp"), ("covered-w-st-basis", "wbwb"),
                                ("covered-w-st-adjustment", "wbwa")):
                family_id = P + f"f1099b.{family}"
                acts = remove_member(acts, family_id, covered_fact_id(acts, family_id, tag), tag, literal_closure=True)
            code_b(acts, "st", 4000.0, 4500.0, 6000.0, "wbwo", wash=1000.0)
        if stage >= 2:
            acts = say(acts, Q3, "yes", "wbwq3")
            acts = probe.answer(ccr._renumbered(acts), IC3, "yes", "wbwic3")
        if stage >= 3:
            acts = probe.answer(ccr._renumbered(acts), cfp.PATH_B, "no", "wbwpb")
        return ccr._renumbered(acts)
    return build


def q3_yes_late(reanswer: bool) -> Callable[[], Acts]:
    """Code B 'yes' with a box A sale, computed; then a box D sale arrives (and optionally 'yes' again)."""
    def build() -> Acts:
        acts = v81_return(sales=a_high, **CLS)
        d_low(acts)
        if reanswer:
            acts = say(acts, Q3, "yes", "q3again")
        return ccr._renumbered(acts)
    return build


def q3_no_late_both(reanswer: bool) -> Callable[[], Acts]:
    """The wage return with code B 'no', computed; then a box A and a box D code B sale (and 'yes')."""
    def build() -> Acts:
        acts = v81_return(q1="no", q2="no", q3="no")
        a_high(acts)
        d_low(acts)
        if reanswer:
            acts = say(acts, Q3, "yes", "q3both")
            acts = probe.answer(ccr._renumbered(acts), IC3, "yes", "q3bothic3")
            acts = probe.boundary(ccr._renumbered(acts), "no", "no")
        return ccr._renumbered(acts)
    return build


def corrected_basis_changes(fix_g: bool) -> Callable[[], Acts]:
    """a_high, then the correct basis is corrected to 5000 on the sale; the column (g) row is (or is not) corrected too."""
    def build() -> Acts:
        acts = v81_return(sales=a_high, **CLS)
        acts = correct_member(acts, "st", None, {"proceeds": 10000.0, "basis": 7000.0, "corrected_basis": 5000.0,
                                                  "long_term": "no", "wash_disallowed": 0.0}, "ahigh")
        if fix_g:
            acts = correct_member(acts, "st", "adjustment", 2000.0, "ahigh")
        return acts
    return build


def remove_sale_keep_rows() -> Acts:
    acts = v81_return(sales=a_high, **CLS)
    fact = fact_id_for(cbp.member_fact("st", None), identity("st", "ahigh"))
    return remove_member(acts, cbp.fam("st", None), fact, "ahighrm", literal_closure=False)


def track0_cases() -> dict[str, Callable[[], Acts]]:
    b_sale = lambda a: cp.on_be(a, "st", 3000.0, 1000.0, "mxb")  # noqa: E731
    e_sale = lambda a: cp.on_be(a, "lt", 6000.0, 2000.0, "mxe")  # noqa: E731
    c_sale = lambda a: cfp.cf_sale(a, "st", 2500.0, 1000.0, "mxc")  # noqa: E731
    cases: dict[str, Callable[[], Acts]] = {
        # Required adversarial cases.
        "x_bw_w_exceeds_correct_loss_within_shown": ret(lambda a: code_b(a, "st", 4000.0, 6000.0, 4500.0, "bwx", wash=1000.0)),
        "x_bw_w_equals_correct_loss": ret(lambda a: code_b(a, "st", 4000.0, 4500.0, 6000.0, "bwe", wash=2000.0)),
        "x_d_bw_w_exceeds_correct_loss": ret(lambda a: code_b(a, "lt", 7000.0, 7500.0, 7200.0, "dbwx", wash=500.0)),
        "x_no_correction_with_w": ret(lambda a: code_b(a, "st", 4000.0, 5000.0, 5000.0, "ncw", wash=500.0)),
        "x_g_sign_flipped": ret(lambda a: code_b(a, "st", *A_HIGH, "gflip", g=-3000.0)),
        "x_bw_g_omits_w": ret(lambda a: code_b(a, "st", 4000.0, 4500.0, 6000.0, "gnow", wash=1000.0, g=-1500.0)),
        "x_basis_row_is_corrected": ret(basis_row_is_corrected),
        "x_dup_covered_st": ret(dup("covered", "st")),
        "x_dup_covered_w_st": ret(dup("covered-w", "st")),
        "x_dup_noncovered_st": ret(dup("noncovered", "st"), q1="yes"),
        "x_dup_covered_lt": ret(dup("covered", "lt")),
        "x_dup_covered_w_lt": ret(dup("covered-w", "lt")),
        "x_dup_noncovered_lt": ret(dup("noncovered", "lt"), q1="yes"),
        "x_dup_box_c_ic3_no": ret(dup("no1099b", "st"), q2="yes", ic3="no"),
        "x_dup_box_c_ic3_yes": ret(dup("no1099b", "st"), q2="yes"),
        "x_a_gain_d_loss": ret(lambda a: [a_high(a), code_b(a, "lt", 6000.0, 5000.0, 9000.0, "agdl")] and None),
        "x_a_loss_d_gain": ret(lambda a: [code_b(a, "st", 5000.0, 3000.0, 9000.0, "aldg"), d_low(a)] and None),
        "x_a_loss_to_gain": ret(lambda a: code_b(a, "st", 5000.0, 7000.0, 3000.0, "l2g")),
        "x_d_loss_to_gain": ret(lambda a: code_b(a, "lt", 5000.0, 7000.0, 3000.0, "dl2g")),
        "x_d_gain_to_loss": ret(lambda a: code_b(a, "lt", 6000.0, 5000.0, 9000.0, "dg2l")),
        "x_d_proceeds_row_missing": ret(lambda a: code_b(a, "lt", *D_LOW, "dnop", rows=("basis", "adjustment"))),
        "x_d_basis_row_missing": ret(lambda a: code_b(a, "lt", *D_LOW, "dnob", rows=("proceeds", "adjustment"))),
        "x_d_adjustment_row_missing": ret(lambda a: code_b(a, "lt", *D_LOW, "dnoa", rows=("proceeds", "basis"))),
        "x_d_holding_mismatch": ret(lambda a: code_b(a, "lt", *D_LOW, "dhold", long_term="no")),
        "x_shared_transaction_missing_g": ret(shared_transaction(False)),
        "x_shared_transaction_complete": ret(shared_transaction(True)),
        "x_zero_proceeds_zero_shown": ret(lambda a: code_b(a, "st", 0.0, 0.0, 500.0, "zz")),
        "x_d_zero_proceeds_zero_shown": ret(lambda a: code_b(a, "lt", 0.0, 0.0, 500.0, "dzz")),
        "x_path_b_yes": ret(a_high, path_b="yes"),
        "x_remove_sale_keep_rows": remove_sale_keep_rows,
        "x_corrected_basis_changed_g_stale": corrected_basis_changes(False),
        "x_corrected_basis_changed_g_fixed": corrected_basis_changes(True),
        "x_q3_yes_late_member": q3_yes_late(False),
        "x_q3_no_late_both_terms": q3_no_late_both(False),
        "x_q3_no_late_both_terms_reanswered": q3_no_late_both(True),
        "x_q3_yes_late_member_reanswered": q3_yes_late(True),
        # Empty/nonempty matrix.
        "m_q3_yes_nothing_8949_yes": lambda: v81_return(q3="yes"),
        "m_q3_yes_nothing_beside_direct": ret(nothing_beside("direct")),
        "m_q3_yes_nothing_beside_w": ret(nothing_beside("w")),
        "m_q3_yes_nothing_beside_b": ret(nothing_beside("b"), q1="yes"),
        "m_q3_yes_nothing_beside_c": ret(nothing_beside("c"), q2="yes"),
        "m_d_q3_no_with_member": ret(d_low, q3="no"),
        "m_a_v80_ic_only": ret(a_high, ic3=None, new_ic="yes"),
        "m_a_v79_ic_only": ret(a_high, ic3=None, old_ic="yes"),
        "m_a_q3_no_v80_ic_yes": ret(a_high, q3="no", ic3=None, new_ic="yes"),
        "m_a_c_ic3_no_v80_ic_yes": ret(lambda a: [a_high(a), c_sale(a)] and None, q2="yes", ic3="no", new_ic="yes"),
        "m_a_c_ic3_unanswered_v80_ic_yes": ret(lambda a: [a_high(a), c_sale(a)] and None, q2="yes", ic3=None, new_ic="yes"),
        "m_a_c_ic3_yes_v80_ic_no": ret(lambda a: [a_high(a), c_sale(a)] and None, q2="yes", new_ic="no"),
        "m_a_c_ic3_yes_v80_ic_yes": ret(lambda a: [a_high(a), c_sale(a)] and None, q2="yes", new_ic="yes"),
        "m_a_and_b": ret(lambda a: [a_high(a), b_sale(a)] and None, q1="yes"),
        "m_d_and_e": ret(lambda a: [d_low(a), e_sale(a)] and None, q1="yes"),
        "m_a_and_b_q1_no": ret(lambda a: [a_high(a), b_sale(a)] and None, q1="no"),
        "m_d_ic3_no": ret(d_low, ic3="no"),
        "m_8949_no_ic3_yes_q3_no": ret(None, q3="no"),
    }
    for n in range(5):
        cases[f"t1_stage{n}"] = late_trace(n)
    for n in range(5):
        cases[f"t2_stage{n}"] = correction_trace(n)
    cases["t2_stage4_keep_covered"] = correction_trace(4, keep_covered=True)
    for n in range(4):
        cases[f"t3_stage{n}"] = w_to_bw_trace(n)
    return cases


# Hand values. Single, wages 50,000, standard deduction: taxable income 34,250
# before capital gains. Tax Table: 2025 single schedule at the row midpoint,
# rounded; a net capital gain under the 48,350 ceiling is taxed at 0%.
PUB = ("published", "published")
HAND: dict[str, dict[str, Any]] = {
    "x_bw_w_equals_correct_loss": {"schedule-d.line-1b": 0, "schedule-d.line-7": 0, "schedule-d.line-16": 0,
                                   "form1040.line-7a": 0, "form1040.line-15": 34250, "form1040.line-16": 3875,
                                   "attachments": PUB},
    # 6000 short-term and -3000 long-term: line 16 3000, no net capital gain, all ordinary.
    "x_a_gain_d_loss": {"schedule-d.line-1b": 6000, "schedule-d.line-8b": -3000, "schedule-d.line-7": 6000,
                        "schedule-d.line-15": -3000, "schedule-d.line-16": 3000, "form1040.line-7a": 3000,
                        "form1040.line-15": 37250, "form1040.line-16": 4235, "preferential": 0, "attachments": PUB},
    # -4000 short-term and 3000 long-term: line 16 -1000, limited loss 1000.
    "x_a_loss_d_gain": {"schedule-d.line-1b": -4000, "schedule-d.line-8b": 3000, "schedule-d.line-7": -4000,
                        "schedule-d.line-15": 3000, "schedule-d.line-16": -1000, "schedule-d.line-21": 1000,
                        "form1040.line-7a": -1000, "form1040.line-15": 33250, "form1040.line-16": 3755, "preferential": 0,
                        "attachments": PUB},
    "x_a_loss_to_gain": {"schedule-d.line-1b": 2000, "schedule-d.line-7": 2000, "schedule-d.line-16": 2000,
                         "form1040.line-7a": 2000, "form1040.line-15": 36250, "form1040.line-16": 4115, "preferential": 0,
                         "attachments": PUB},
    "x_d_loss_to_gain": {"schedule-d.line-8b": 2000, "schedule-d.line-15": 2000, "schedule-d.line-16": 2000,
                         "form1040.line-7a": 2000, "form1040.line-15": 36250, "form1040.line-16": 3875,
                         "preferential": 2000, "attachments": PUB},
    "x_d_gain_to_loss": {"schedule-d.line-8b": -3000, "schedule-d.line-15": -3000, "schedule-d.line-16": -3000,
                         "schedule-d.line-21": 3000, "form1040.line-7a": -3000, "form1040.line-15": 31250,
                         "form1040.line-16": 3515, "preferential": 0, "attachments": PUB},
    # 10000 - 7000 + 3000 = 6000, and 5000 - 3000 - 6000 = -4000: line 1b 2000.
    "x_shared_transaction_complete": {"schedule-d.line-1b": 2000, "schedule-d.line-7": 2000, "form1040.line-7a": 2000,
                                      "form1040.line-15": 36250, "form1040.line-16": 4115, "attachments": PUB},
    # 0 - 0 + (0 - 500) = -500.
    "x_zero_proceeds_zero_shown": {"schedule-d.line-1b": -500, "schedule-d.line-7": -500, "schedule-d.line-16": -500,
                                   "schedule-d.line-21": 500, "form1040.line-7a": -500, "form1040.line-15": 33750,
                                   "form1040.line-16": 3815, "attachments": PUB},
    "x_d_zero_proceeds_zero_shown": {"schedule-d.line-8b": -500, "schedule-d.line-15": -500, "schedule-d.line-16": -500,
                                     "schedule-d.line-21": 500, "form1040.line-7a": -500, "form1040.line-15": 33750,
                                     "form1040.line-16": 3815, "attachments": PUB},
    "x_corrected_basis_changed_g_fixed": {"schedule-d.line-1b": 5000, "schedule-d.line-7": 5000,
                                          "form1040.line-7a": 5000, "form1040.line-15": 39250, "form1040.line-16": 4475,
                                          "attachments": PUB},
    # a_high and d_low: 6000 ordinary, 3000 preferential.
    "x_q3_yes_late_member_reanswered": {"schedule-d.line-1b": 6000, "schedule-d.line-8b": 3000, "schedule-d.line-7": 6000,
                                        "schedule-d.line-15": 3000, "schedule-d.line-16": 9000, "form1040.line-7a": 9000,
                                        "form1040.line-15": 43250, "form1040.line-16": 4595, "preferential": 3000,
                                        "attachments": PUB},
    "m_a_and_b": {"schedule-d.line-1b": 6000, "schedule-d.line-2": 2000, "schedule-d.line-7": 8000,
                  "form1040.line-7a": 8000, "form1040.line-15": 42250, "form1040.line-16": 4835, "attachments": PUB},
    # a_high and box C 2500 / 1000: 7500 ordinary.
    "m_a_c_ic3_yes_v80_ic_no": {"schedule-d.line-1b": 6000, "schedule-d.line-3": 1500, "schedule-d.line-7": 7500,
                                "form1040.line-7a": 7500, "form1040.line-15": 41750, "form1040.line-16": 4775,
                                "attachments": PUB},
    "m_d_and_e": {"schedule-d.line-8b": 3000, "schedule-d.line-9": 4000, "schedule-d.line-15": 7000,
                  "form1040.line-7a": 7000, "form1040.line-15": 41250, "form1040.line-16": 3875, "preferential": 7000,
                  "attachments": PUB},
    "t1_stage0": {"form1040.line-15": 34250, "form1040.line-16": 3875,
                   "attachments": ("guard_inapplicable", "guard_inapplicable")},
    "t2_stage0": {"schedule-d.line-1a": 3000, "form1040.line-15": 37250, "form1040.line-16": 4235},
    # Correction of a code W row into BW: stage 0 is 4000 - 4500 + 300 = -200 on line 1b.
    "t3_stage0": {"schedule-d.line-1b": -200, "form1040.line-15": 34050, "form1040.line-16": 3851},
    "t3_stage3": {"schedule-d.line-1b": -1000, "schedule-d.line-21": 1000, "form1040.line-7a": -1000,
                  "form1040.line-15": 33250, "form1040.line-16": 3755, "attachments": PUB},
}
HAND["m_a_c_ic3_yes_v80_ic_yes"] = dict(HAND["m_a_c_ic3_yes_v80_ic_no"])
HAND["x_q3_no_late_both_terms_reanswered"] = dict(HAND["x_q3_yes_late_member_reanswered"])
# A Path B "yes" made false by the BW row decides nothing once the code B answers hold (as x_path_b_yes).
HAND["t3_stage2"] = dict(HAND["t3_stage3"])
for _name in ("t1_stage4", "t2_stage4"):
    HAND[_name] = dict(cbp.HAND["a_high"])
HAND["x_path_b_yes"] = dict(cbp.HAND["a_high"])
HAND["x_dup_box_c_ic3_yes"] = {}  # measured, not a pass condition: a false in-class "yes"


def gain_row(term: str, missing: list[str]) -> tuple[str, list[Any]]:
    return (f"f1099b-code-b-{term}-gain", ["blocked", "DEPENDENCY_ABSENT", missing])


BB = ("blocked", "blocked")
BLOCKED: dict[str, dict[str, Any]] = {
    "x_bw_w_exceeds_correct_loss_within_shown": {"attachments": BB, "constraint": "ADJUSTMENT_EXCEEDS_LOSS"},
    "x_d_bw_w_exceeds_correct_loss": {"attachments": BB, "constraint": "ADJUSTMENT_EXCEEDS_LOSS"},
    "x_no_correction_with_w": {"attachments": BB, "constraint": "CODE_B_WITHOUT_CORRECTION"},
    "x_g_sign_flipped": {"attachments": BB, "row": ("f1099b.code-b-st-txn.amounts-check", ["blocked", "DEPENDENCY_INVALID", []])},
    "x_bw_g_omits_w": {"attachments": BB, "row": ("f1099b.code-b-st-txn.amounts-check", ["blocked", "DEPENDENCY_INVALID", []])},
    "x_basis_row_is_corrected": {"attachments": BB,
                                 "row": ("f1099b.code-b-st-txn.amounts-check", ["blocked", "DEPENDENCY_INVALID", []])},
    "x_dup_covered_st": {"attachments": BB, "constraint": "IDENTITY_EXCLUSIVITY_COLLISION"},
    "x_dup_covered_w_st": {"attachments": BB, "constraint": "IDENTITY_EXCLUSIVITY_COLLISION"},
    "x_dup_noncovered_st": {"attachments": BB, "constraint": "IDENTITY_EXCLUSIVITY_COLLISION"},
    "x_dup_covered_lt": {"attachments": BB, "constraint": "IDENTITY_EXCLUSIVITY_COLLISION"},
    "x_dup_covered_w_lt": {"attachments": BB, "constraint": "IDENTITY_EXCLUSIVITY_COLLISION"},
    "x_dup_noncovered_lt": {"attachments": BB, "constraint": "IDENTITY_EXCLUSIVITY_COLLISION"},
    "x_dup_box_c_ic3_no": {"attachments": BB},
    "x_d_holding_mismatch": {"attachments": BB, "constraint": "HOLDING_PERIOD_MISMATCH"},
    "x_d_proceeds_row_missing": {"attachments": BB, "row": gain_row("lt", ["f1099b.code-b-lt-txn.proceeds"]), "questions": [
        "What are the proceeds shown on your Form 1099-B for each long-term sale you recorded whose reported basis is wrong?"]},
    "x_d_basis_row_missing": {"attachments": BB, "row": gain_row("lt", ["f1099b.code-b-lt-txn.basis"]), "questions": [
        "What basis does your Form 1099-B show for each long-term sale you recorded whose reported basis is wrong?"]},
    "x_d_adjustment_row_missing": {"attachments": BB, "row": gain_row("lt", ["f1099b.code-b-lt-txn.adjustment"]), "questions": [
        "What is the column (g) adjustment for each long-term sale you recorded whose reported basis is wrong: the basis "
        "shown minus the correct basis, plus any wash-sale loss disallowed?"]},
    # The count check blocks with no missing list (the v80 d3_b_shared_transaction mechanism).
    "x_shared_transaction_missing_g": {"attachments": BB, "row": gain_row("st", [])},
    "x_corrected_basis_changed_g_stale": {"attachments": BB,
                                          "row": ("f1099b.code-b-st-txn.amounts-check", ["blocked", "DEPENDENCY_INVALID", []])},
    "x_q3_yes_late_member": {"attachments": BB, "questions": [cbp.Q3_TEXT]},
    "x_q3_no_late_both_terms": {"attachments": BB, "questions": [cbp.Q3_TEXT]},
    "m_8949_no_ic3_yes_q3_no": {"attachments": BB},
    "m_q3_yes_nothing_8949_yes": {"attachments": BB, "row": gain_row("st", [])},
    "m_q3_yes_nothing_beside_direct": {"attachments": BB, "row": gain_row("st", [])},
    "m_q3_yes_nothing_beside_w": {"attachments": BB, "row": gain_row("st", [])},
    "m_q3_yes_nothing_beside_b": {"attachments": BB, "row": gain_row("st", [])},
    "m_q3_yes_nothing_beside_c": {"attachments": BB, "row": gain_row("st", [])},
    "m_d_q3_no_with_member": {"attachments": BB, "questions": [cbp.Q3_TEXT]},
    "m_a_v80_ic_only": {"attachments": BB, "questions": [cbp.IC3_TEXT]},
    "m_a_v79_ic_only": {"attachments": BB, "questions": [cbp.IC3_TEXT]},
    "m_a_q3_no_v80_ic_yes": {"attachments": BB, "questions": [cbp.Q3_TEXT]},
    "m_a_c_ic3_no_v80_ic_yes": {"attachments": BB},
    "m_a_c_ic3_unanswered_v80_ic_yes": {"attachments": BB, "questions": [cbp.IC3_TEXT]},
    "m_a_and_b_q1_no": {"attachments": BB, "questions": [cfp.Q1_TEXT] if hasattr(cfp, "Q1_TEXT") else []},
    "m_d_ic3_no": {"attachments": BB, "row": gain_row("lt", ["f1099b.code-b-lt-proceeds-subtotal", "f1099b.code-b-lt-basis-subtotal",
                                                            "f1099b.code-b-lt-adjustment-subtotal"])},
    "t1_stage1": {"attachments": BB, "questions": [cbp.Q3_TEXT]},
    "t1_stage1": {"attachments": BB, "questions": [cbp.Q3_TEXT]},
    "t1_stage2": {"attachments": BB, "questions": [cbp.IC3_TEXT]},
    "t1_stage3": {"attachments": BB, "row": gain_row("st", [])},
    "t2_stage1": {"attachments": BB, "questions": [cbp.Q3_TEXT]},
    "t2_stage4_keep_covered": {"attachments": BB, "constraint": "IDENTITY_EXCLUSIVITY_COLLISION"},
    "t2_stage2": {"attachments": BB, "questions": [cbp.IC3_TEXT]},
    "t2_stage3": {"attachments": BB, "row": gain_row("st", [])},
    "t3_stage1": {"attachments": BB, "questions": [cbp.Q3_TEXT]},
}
# x_remove_sale_keep_rows: either rejected before a run or blocked; recorded as measured.
MEASURED = {"x_remove_sale_keep_rows", "x_dup_box_c_ic3_yes"}


def check(name: str, result: dict[str, Any]) -> dict[str, Any]:
    if name in MEASURED:
        return {}
    saved_hand, saved_blocked = dict(cbp.HAND), dict(cbp.BLOCKED)
    try:
        cbp.HAND.update(HAND)
        cbp.BLOCKED.update(BLOCKED)
        return cbp.check(name, result)
    finally:
        cbp.HAND.clear()
        cbp.HAND.update(saved_hand)
        cbp.BLOCKED.clear()
        cbp.BLOCKED.update(saved_blocked)


# ---- v80 neighbour probes ------------------------------------------------------------
# Neighbouring v80 families, run on v80 and on v81 with the code B answer "no".
# Track 0 measured the first four as inherited v80 gaps (owner question 1).
# Decision 6 takes them into Track 1, so on v81 they now carry expectations
# (NEIGHBOUR_HAND, NEIGHBOUR_BLOCKED); the rest are Track 1's further probes of
# the same four patterns, and controls that must not change.


def sale_on(acts: Acts, kind: str, term: str, proceeds: float, basis: float, tag: str, *, wash: float | None = None,
            tsa: str = "no", flag: str | None = None) -> Acts:
    """One sale on a v80 Form 1099-B family whose sale object is keyed by ``tag``, with its amount rows.

    ``flag`` names one more eligibility flag of the sale object to set "yes".
    """
    acts = ccr._renumbered(acts)
    if kind == "noncovered":
        cp.on_be(acts, term, proceeds, basis, tag, wash)
        return ccr._renumbered(acts)
    sale = probe.txn(proceeds=proceeds, basis=basis, long_term="yes" if term == "lt" else "no", wash=wash,
                     reported="yes", covered="yes")
    sale["taxpayer_side_adjustment"] = tsa
    if flag is not None:
        assert sale[flag] == "no", flag
        sale[flag] = "yes"
    acts = record_keyed(acts, P + f"f1099b.{kind}-{term}", sale, tag)
    acts = record_keyed(acts, P + f"f1099b.{kind}-{term}-proceeds", proceeds, tag + "p")
    acts = record_keyed(acts, P + f"f1099b.{kind}-{term}-basis", basis, tag + "b")
    if kind == "covered-w":
        acts = record_keyed(acts, P + f"f1099b.{kind}-{term}-adjustment", wash or 0.0, tag + "a")
    return acts


def record_keyed(acts: Acts, family_id: str, value: object, tag: str) -> Acts:
    """probe.record with the family in the horizon ids, so one tag can key sales on two families."""
    slug = family_id.removeprefix(P + "f1099b.")
    out = probe._strip_closure(copy.deepcopy(acts), family_id + ".source-closure")
    version = probe.family_version(out, family_id)
    fact_type = probe.FACT_TYPES[str(probe.FAMILIES[(family_id, version)]["member_predicate"]["fact_type"])]
    probe._adopt(out, fact_type["id"])
    declared: list[tuple[str, str]] = []
    for key in fact_type["identity_keys"]:
        if key["kind"] == "entity":
            entity = f"demo.ns.{tag}.{key['name']}"
            if not cp.proto._known_entity(out, entity):
                probe._introduce(out, entity, key["entity_kind"])
            declared.append((key["name"], entity))
        else:
            declared.append((key["name"], key["values"][0]))
    head = probe.horizons(out, family_id)[-1]
    n = len(probe.horizons(out, family_id))
    successor = f"demo.ns.{tag}.{slug}.h{n}"
    probe._add(out, "member-transition", {
        "family": {"id": family_id, "version": version},
        "scope": {"tax-year": probe.YEAR, "subject": "demo.primary"},
        "member": {"action": "assert", "finding": _attested(
            f"demo.ns.{tag}.{slug}.member.h{n}", fact_id_for(fact_type["id"], tuple(declared)), value)},
        "successor": {"id": successor, "predecessor": head},
    })
    probe._close(out, family_id + ".source-closure", successor, f"demo.ns.{tag}.{slug}.closure")
    return ccr._renumbered(out)


def tsa_direct(acts: Acts) -> Acts:
    """A covered box A sale on line 1a whose filer flags taxpayer_side_adjustment yes."""
    return sale_on(acts, "covered", "st", 10000.0, 7000.0, "tsa", tsa="yes")


def b_and_covered_lt(acts: Acts) -> Acts:
    cp.on_be(acts, "st", 10000.0, 4000.0, "nbdup")
    return codeb_probe.direct(ccr._renumbered(acts), "lt", 10000.0, 7000.0, "nbdup")


Sale = tuple[str, str, float, float, float | None]  # kind, term, proceeds, basis, wash


def pair(first: Sale, second: Sale, *, same: bool = True) -> Callable[[Acts], Acts]:
    """Two sales, on one transaction (``same``) or on two."""
    def build(acts: Acts) -> Acts:
        acts = sale_on(acts, *first[:4], "pa", wash=first[4])
        return sale_on(acts, *second[:4], "pa" if same else "pb", wash=second[4])
    return build


ON_BE = {"q1": "yes", "q2": "no", "form8949": "no", "path_b": "no", "old_ic": "yes"}
ON_W = {"q1": "no", "q2": "no", "form8949": "no", "path_b": "yes"}
DIRECT = {"q1": "no", "q2": "no"}
B_ST: Sale = ("noncovered", "st", 10000.0, 4000.0, None)
E_LT: Sale = ("noncovered", "lt", 6000.0, 2000.0, None)
A_ST: Sale = ("covered", "st", 10000.0, 7000.0, None)
D_LT: Sale = ("covered", "lt", 10000.0, 7000.0, None)
W_ST: Sale = ("covered-w", "st", 4000.0, 5000.0, 300.0)
W_LT: Sale = ("covered-w", "lt", 4000.0, 5000.0, 300.0)
NEIGHBOUR: dict[str, Callable[[], Acts]] = {
    # Pattern 1 and 2: a zero-proceeds code W or box B/E row requires its attachments.
    "n_b_zero_proceeds": lambda: cfp.v80_return(sales=lambda a: cp.on_be(a, "st", 0.0, 500.0, "nbz"), **ON_BE),
    "n_e_zero_proceeds": lambda: cfp.v80_return(sales=lambda a: cp.on_be(a, "lt", 0.0, 500.0, "nez"), **ON_BE),
    "n_b_zero_proceeds_zero_basis": lambda: cfp.v80_return(sales=lambda a: cp.on_be(a, "st", 0.0, 0.0, "nbzz"), **ON_BE),
    "n_w_zero_proceeds": lambda: cfp.v80_return(
        sales=lambda a: codeb_probe.wash(ccr._renumbered(a), "st", 0.0, 500.0, 300.0, "nwz"), **ON_W),
    "n_w_lt_zero_proceeds": lambda: cfp.v80_return(
        sales=lambda a: codeb_probe.wash(ccr._renumbered(a), "lt", 0.0, 500.0, 300.0, "nwlz"), **ON_W),
    # Review B1: a line 1a or 8a sale with zero proceeds requires Schedule D and reaches line 7a.
    "n_covered_st_zero_proceeds": lambda: cfp.v80_return(
        sales=lambda a: sale_on(a, "covered", "st", 0.0, 500.0, "dzp"), **DIRECT),
    "n_covered_lt_zero_proceeds": lambda: cfp.v80_return(
        sales=lambda a: sale_on(a, "covered", "lt", 0.0, 500.0, "dzpl"), **DIRECT),
    "n_covered_st_zero_proceeds_zero_basis": lambda: cfp.v80_return(
        sales=lambda a: sale_on(a, "covered", "st", 0.0, 0.0, "dzz"), **DIRECT),
    # Pattern 3: one transaction on families of both terms.
    "n_dup_b_and_covered_lt": lambda: cfp.v80_return(sales=b_and_covered_lt, **ON_BE),
    "n_dup_b_and_e": lambda: cfp.v80_return(sales=pair(B_ST, E_LT), **ON_BE),
    "n_dup_e_and_covered_st": lambda: cfp.v80_return(sales=pair(A_ST, E_LT), **ON_BE),
    "n_dup_covered_st_and_covered_lt": lambda: cfp.v80_return(sales=pair(A_ST, D_LT), **DIRECT),
    "n_dup_w_st_and_covered_lt": lambda: cfp.v80_return(sales=pair(W_ST, D_LT), **ON_W),
    "n_dup_covered_st_and_w_lt": lambda: cfp.v80_return(sales=pair(A_ST, W_LT), **ON_W),
    "n_dup_w_st_and_w_lt": lambda: cfp.v80_return(sales=pair(W_ST, W_LT), **ON_W),
    # Pattern 4: a covered or code W sale flagged with a taxpayer-side adjustment.
    "n_covered_tsa_yes_no8949": lambda: cfp.v80_return(sales=tsa_direct, **DIRECT),
    "n_covered_lt_tsa_yes": lambda: cfp.v80_return(
        sales=lambda a: sale_on(a, "covered", "lt", 10000.0, 7000.0, "tsal", tsa="yes"), **DIRECT),
    "n_w_st_tsa_yes": lambda: cfp.v80_return(
        sales=lambda a: sale_on(a, "covered-w", "st", 4000.0, 5000.0, "tsaw", wash=300.0, tsa="yes"), **ON_W),
    # Review S5: each of the other four eligibility flags refuses a covered sale (and a code W sale).
    "n_covered_st_ordinary_yes": lambda: cfp.v80_return(
        sales=lambda a: sale_on(a, "covered", "st", 10000.0, 7000.0, "flor", flag="ordinary_indicated"), **DIRECT),
    "n_covered_lt_market_discount_yes": lambda: cfp.v80_return(
        sales=lambda a: sale_on(a, "covered", "lt", 10000.0, 7000.0, "flmd", flag="box_1f_market_discount"), **DIRECT),
    "n_covered_lt_qof_yes": lambda: cfp.v80_return(
        sales=lambda a: sale_on(a, "covered", "lt", 10000.0, 7000.0, "flqf", flag="qof_indicated"), **DIRECT),
    "n_covered_lt_collectibles_yes": lambda: cfp.v80_return(
        sales=lambda a: sale_on(a, "covered", "lt", 10000.0, 7000.0, "flco", flag="collectibles_or_special_rate"),
        **DIRECT),
    "n_w_lt_collectibles_yes": lambda: cfp.v80_return(
        sales=lambda a: sale_on(a, "covered-w", "lt", 4000.0, 5000.0, "flwc", wash=300.0,
                                flag="collectibles_or_special_rate"), **ON_W),
    # Controls: the same shapes on two transactions, and a flag of "no", compute as on v80.
    "n_two_b_and_covered_lt": lambda: cfp.v80_return(sales=pair(B_ST, D_LT, same=False), **ON_BE),
    "n_two_covered_st_and_covered_lt": lambda: cfp.v80_return(sales=pair(A_ST, D_LT, same=False), **DIRECT),
    "n_two_w_st_and_w_lt": lambda: cfp.v80_return(sales=pair(W_ST, W_LT, same=False), **ON_W),
    "n_covered_tsa_no": lambda: cfp.v80_return(
        sales=lambda a: sale_on(a, "covered", "st", 10000.0, 7000.0, "tsan"), **DIRECT),
}
# v81 expectations. Single, wages 50,000: taxable income 34,250 before capital gains.
NEIGHBOUR_HAND: dict[str, dict[str, Any]] = {
    # 0 - 500 + 300 = -200 on line 1b (8b): both attachments now required.
    "n_w_zero_proceeds": {"schedule-d.line-1b": -200, "schedule-d.line-16": -200, "form1040.line-7a": -200,
                          "form1040.line-15": 34050, "form1040.line-16": 3851, "attachments": PUB},
    "n_w_lt_zero_proceeds": {"schedule-d.line-8b": -200, "schedule-d.line-16": -200, "form1040.line-7a": -200,
                             "form1040.line-15": 34050, "form1040.line-16": 3851, "attachments": PUB},
    "n_b_zero_proceeds": {"schedule-d.line-2": -500, "schedule-d.line-16": -500, "form1040.line-7a": -500,
                          "form1040.line-15": 33750, "form1040.line-16": 3815, "attachments": PUB},
    "n_e_zero_proceeds": {"schedule-d.line-9": -500, "schedule-d.line-16": -500, "form1040.line-7a": -500,
                          "form1040.line-15": 33750, "form1040.line-16": 3815, "attachments": PUB},
    "n_b_zero_proceeds_zero_basis": {"schedule-d.line-2": 0, "schedule-d.line-16": 0, "form1040.line-7a": 0,
                                     "form1040.line-15": 34250, "form1040.line-16": 3875, "attachments": PUB},
    # B1: 0 - 500 on line 1a (8a). Line 16 -500, line 21 500, line 7a -500; taxable income 33,750, tax 3,815.
    # A direct sale needs Schedule D but not Form 8949.
    "n_covered_st_zero_proceeds": {"schedule-d.line-1a": -500, "schedule-d.line-7": -500, "schedule-d.line-16": -500,
                                   "schedule-d.line-21": 500, "form1040.line-7a": -500, "form1040.line-15": 33750,
                                   "form1040.line-16": 3815, "attachments": ("guard_inapplicable", "published")},
    "n_covered_lt_zero_proceeds": {"schedule-d.line-8a": -500, "schedule-d.line-15": -500, "schedule-d.line-16": -500,
                                   "schedule-d.line-21": 500, "form1040.line-7a": -500, "form1040.line-15": 33750,
                                   "form1040.line-16": 3815, "preferential": 0,
                                   "attachments": ("guard_inapplicable", "published")},
    "n_covered_st_zero_proceeds_zero_basis": {"schedule-d.line-1a": 0, "schedule-d.line-16": 0, "form1040.line-7a": 0,
                                              "form1040.line-15": 34250, "form1040.line-16": 3875,
                                              "attachments": ("guard_inapplicable", "published")},
    # 6000 short-term (box B) and 3000 long-term (line 8a): 3000 at 0%, 40,250 ordinary.
    "n_two_b_and_covered_lt": {"schedule-d.line-2": 6000, "schedule-d.line-8a": 3000, "schedule-d.line-16": 9000,
                               "form1040.line-7a": 9000, "form1040.line-15": 43250, "form1040.line-16": 4595,
                               "preferential": 3000, "attachments": PUB},
    "n_two_covered_st_and_covered_lt": {"schedule-d.line-1a": 3000, "schedule-d.line-8a": 3000,
                                        "schedule-d.line-16": 6000, "form1040.line-7a": 6000,
                                        "form1040.line-15": 40250, "form1040.line-16": 4235, "preferential": 3000},
    # -700 and -700: line 16 -1400, limited to itself.
    "n_two_w_st_and_w_lt": {"schedule-d.line-1b": -700, "schedule-d.line-8b": -700, "schedule-d.line-16": -1400,
                            "form1040.line-7a": -1400, "form1040.line-15": 32850, "form1040.line-16": 3707,
                            "attachments": PUB},
    "n_covered_tsa_no": {"schedule-d.line-1a": 3000, "form1040.line-7a": 3000, "form1040.line-15": 37250,
                         "form1040.line-16": 4235},
}


def check_row(kind: str, term: str) -> tuple[str, list[Any]]:
    name = "amounts-check" if kind == "noncovered" else "admission-check"
    return (f"f1099b.{kind}-{term}-txn.{name}", ["blocked", "DEPENDENCY_INVALID", []])


NEIGHBOUR_BLOCKED: dict[str, dict[str, Any]] = {
    "n_dup_b_and_covered_lt": {"attachments": BB, "row": check_row("noncovered", "st"), "published": ["schedule-d.line-8a"]},
    "n_dup_b_and_e": {"attachments": BB, "row": check_row("noncovered", "st"),
                      "also_rows": [check_row("noncovered", "lt")]},
    "n_dup_e_and_covered_st": {"attachments": BB, "row": check_row("noncovered", "lt"), "published": ["schedule-d.line-1a"]},
    "n_dup_covered_st_and_covered_lt": {"attachments": BB, "row": check_row("covered", "st"),
                                        "also_rows": [check_row("covered", "lt")]},
    # The code W row is required on Form 8949 and Schedule D whatever else is wrong.
    "n_dup_w_st_and_covered_lt": {"attachments": PUB, "row": check_row("covered-w", "st"), "published": ["schedule-d.line-8a"]},
    "n_dup_covered_st_and_w_lt": {"attachments": PUB, "row": check_row("covered-w", "lt"), "published": ["schedule-d.line-1a"]},
    "n_dup_w_st_and_w_lt": {"attachments": PUB, "row": check_row("covered-w", "st"),
                            "also_rows": [check_row("covered-w", "lt")]},
    "n_covered_tsa_yes_no8949": {"attachments": BB, "row": check_row("covered", "st")},
    "n_covered_lt_tsa_yes": {"attachments": BB, "row": check_row("covered", "lt")},
    "n_w_st_tsa_yes": {"attachments": PUB, "row": check_row("covered-w", "st")},
    "n_covered_st_ordinary_yes": {"attachments": BB, "row": check_row("covered", "st")},
    "n_covered_lt_market_discount_yes": {"attachments": BB, "row": check_row("covered", "lt")},
    "n_covered_lt_qof_yes": {"attachments": BB, "row": check_row("covered", "lt")},
    "n_covered_lt_collectibles_yes": {"attachments": BB, "row": check_row("covered", "lt")},
    "n_w_lt_collectibles_yes": {"attachments": PUB, "row": check_row("covered-w", "lt")},
}
# The field sentence each refused probe's blocked line shows.
NEIGHBOUR_FIELD: dict[str, str] = {
    "n_dup_b_and_covered_lt": "schedule-d.line-2", "n_dup_b_and_e": "schedule-d.line-2",
    "n_dup_e_and_covered_st": "schedule-d.line-9", "n_dup_covered_st_and_covered_lt": "schedule-d.line-1a",
    "n_dup_w_st_and_covered_lt": "schedule-d.line-1b", "n_dup_covered_st_and_w_lt": "schedule-d.line-8b",
    "n_dup_w_st_and_w_lt": "schedule-d.line-1b", "n_covered_tsa_yes_no8949": "schedule-d.line-1a",
    "n_covered_lt_tsa_yes": "schedule-d.line-8a", "n_w_st_tsa_yes": "schedule-d.line-1b",
    "n_covered_st_ordinary_yes": "schedule-d.line-1a", "n_covered_lt_market_discount_yes": "schedule-d.line-8a",
    "n_covered_lt_qof_yes": "schedule-d.line-8a", "n_covered_lt_collectibles_yes": "schedule-d.line-8a",
    "n_w_lt_collectibles_yes": "schedule-d.line-8b",
}


def check_neighbour(name: str, result: dict[str, Any]) -> dict[str, Any]:
    """A v81 neighbour run against NEIGHBOUR_HAND / NEIGHBOUR_BLOCKED (empty is a pass)."""
    if name in NEIGHBOUR_HAND:
        saved = dict(cbp.HAND)
        try:
            cbp.HAND[name] = NEIGHBOUR_HAND[name]
            return cbp.check(name, result)
        finally:
            cbp.HAND.clear()
            cbp.HAND.update(saved)
    want = NEIGHBOUR_BLOCKED[name]
    saved_b = dict(cbp.BLOCKED)
    try:
        cbp.BLOCKED[name] = {k: v for k, v in want.items() if k in ("attachments", "row")}
        bad = cbp.check(name, result)
    finally:
        cbp.BLOCKED.clear()
        cbp.BLOCKED.update(saved_b)
    rows = result.get("rows") or {}
    for row_name, row_want in want.get("also_rows", []):
        if rows.get(row_name) != row_want:
            bad["row:" + row_name] = {"want": row_want, "got": rows.get(row_name)}
    lines = result.get("lines") or {}
    for line in want.get("published", []):
        if (lines.get(line) or [None])[0] != "published_value":
            bad[line] = lines.get(line)
    field = (result.get("fields") or {}).get(NEIGHBOUR_FIELD[name]) or {}
    if field.get("disposition") != "blocked":
        bad["field"] = field
    return bad


# ---- worker ------------------------------------------------------------------------


STATE: dict[str, Any] = {}
P0_SUMMARY = cp.summarize  # codeb_probe.summary, installed by codeb_probe


def summary(outcome: Any) -> dict[str, Any]:
    """codeb_probe's summary, plus field sentences and the per-publisher row counts."""
    result: dict[str, Any] = P0_SUMMARY(outcome)
    if outcome.refusal is not None:
        return result
    report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
    model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
    counts = Counter(str(row.get("artifact_id", "")) for row in report.get("dispositions") or [])
    result["publisher_rows"] = {p.removeprefix(P + "rule."): counts.get(p, 0) for p in PUBLISHERS}
    fields: dict[str, Any] = {}
    for section in model.get("sections") or []:
        field = section.get("field") or {}
        if field.get("id") not in FIELDS:
            continue
        resolved = section.get("resolved") or {}
        disposition = str(resolved.get("disposition"))
        explain = ((field.get("dispositions") or {}).get(disposition) or {}).get("explain")
        reasons = [probe.scrub(str(r["sentence"])) for r in resolved.get("reasons") or []
                   if isinstance(r, dict) and r.get("sentence")]
        fields[str(field["id"]).removeprefix(P)] = {"disposition": disposition, "explain": explain, "reasons": reasons[:4]}
    result["fields"] = fields
    return result


def init(repairs: list[str]) -> None:
    cbp.REPAIRS.clear()
    cbp.REPAIRS.update(repairs)
    cp.summarize = summary
    codeb_probe.pin_v80()
    cbp.ORIGIN[:] = [probe.CONTENT, probe.RELEASE_DIR]
    tmp = tempfile.mkdtemp(prefix="codeb-t0-")
    atexit.register(shutil.rmtree, tmp, True)
    STATE["build"] = cbp.build(Path(tmp).resolve() / "scratch")
    STATE["content"] = Path(tmp).resolve() / "scratch" / "content"
    STATE["cases"] = {**cbp.new_cases(), **track0_cases()}


PARTS_KEPT = ("a_high", "a_bw", "x_zero_proceeds_zero_shown")


def trim(result: dict[str, Any], name: str = "") -> dict[str, Any]:
    keep = codeb_probe.keep(result)
    if name not in PARTS_KEPT:
        keep.pop("f8949_parts", None)
    if "blocked" in keep:
        keep["blocked"] = keep["blocked"][:8]
    for key in ("fields", "publisher_rows", "duplicate_field_ids"):
        if result.get(key) not in (None, [], {}):
            keep[key] = result[key]
    return keep


def run(task: tuple[str, str]) -> tuple[tuple[str, str], dict[str, Any]]:
    kind, name = task
    started = time.monotonic()
    try:
        if kind == "case":
            cbp.pin("v81")
            result = codeb_probe.execute(STATE["cases"][name], f"demo.codeb.t0.{name}")
            out = {"result": trim(result, name), "mismatch": check(name, result)}
        else:
            build = NEIGHBOUR[name] if name in NEIGHBOUR else cbp.v80_world()[name]
            if kind == "v80":
                cbp.pin("v80")
                result = codeb_probe.execute(build, f"demo.codeb.t0c80.{name}")
            else:
                cbp.pin("v81")
                answer = "no" if kind == "v81_q3_no" else None
                result = codeb_probe.execute(lambda: cbp.with_q3(build(), answer), f"demo.codeb.t0{kind}.{name}")
            out = trim(result)
            if kind == "v81_q3_no" and name in NEIGHBOUR and set(cbp.TRACK1_REPAIRS) <= cbp.REPAIRS:
                out["mismatch"] = check_neighbour(name, result)
    except Exception as exc:  # noqa: BLE001
        out = {"error": type(exc).__name__, "message": probe.scrub(str(exc))[:600],
               "trace": probe.scrub(traceback.format_exc())[-800:]}
    out["seconds"] = round(time.monotonic() - started, 1)
    return task, out


# ---- static integration surface ------------------------------------------------------


SURFACE_SYMBOLS = ["schedule-d.line-1a-gain", "schedule-d.line-8a-gain"] + [
    f"schedule-d.line-{n}" for n in ("1b", "2", "7", "8b", "9", "15", "16", "21")] + [
    "capital-gains.line7a-total", "capital-gains.selected-preferential-base", "form8949.disposition",
    "schedule-d.disposition", "f1099b.code-b-st-gain", "f1099b.code-b-lt-gain", "f1099b.code-b-st-count",
    "f1099b.code-b-lt-count"] + [f"f1099b.{k}-{t}-count" for k in ("covered", "covered-w", "noncovered")
                                 for t in ("st", "lt")] + [
    f"f1099b.{k}-{t}-txn.admission-check" for k in ("covered", "covered-w") for t in ("st", "lt")]


def surface(content: Path) -> dict[str, Any]:
    package = json.loads((content / "package.core-calculations.v81.json").read_text(encoding="utf-8"))
    wanted = {(m["id"], m["version"]) for m in package["members"]}
    bodies: dict[tuple[str, str], dict[str, Any]] = {}
    for path in content.glob("*.json"):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if isinstance(body, dict) and (body.get("id"), body.get("version")) in wanted:
            bodies[(body["id"], body["version"])] = body
    out: dict[str, Any] = {"members_resolved": len(bodies), "members_listed": len(wanted)}
    for short in SURFACE_SYMBOLS:
        symbol = P + short
        publishers, fields, consumers = [], [], []
        for (mid, ver), body in sorted(bodies.items()):
            tag = f"{mid.removeprefix(P)} {ver} ({body.get('schema')})"
            if body.get("publishes") == symbol:
                publishers.append(tag)
            elif body.get("binds_symbol") == symbol:
                fields.append(tag)
            elif cfp.mentions({k: v for k, v in body.items() if k not in ("id", "notes", "title")}, symbol):
                consumers.append(tag)
        out[short] = {"publishers": publishers, "form_fields": fields, "consumers": consumers}
    return out


# ---- main ----------------------------------------------------------------------------


def shrink_result(result: dict[str, Any], name: str) -> dict[str, Any]:
    """Keep what the closure document cites, so the output stays small.

    ``rows`` keeps every watched row that is not published (and both column
    (h) rows); ``blocked`` keeps only member-validation rows, which carry the
    constraint codes; ``publisher_rows`` keeps only publishers that did not
    record exactly one row (none, in every run); parts only for PARTS_KEPT.
    """
    out = dict(result)
    rows = out.get("rows") or {}
    out["rows"] = {k: v for k, v in rows.items() if v[0] != "published" or k.endswith("-gain")}
    out["blocked"] = [b for b in out.get("blocked") or [] if str(b.get("artifact", "")).endswith("member-validation.synthesized")]
    if "publisher_rows" in out:
        out["publisher_rows_not_one"] = sorted(k for k, v in out.pop("publisher_rows").items() if v != 1)
    if name not in PARTS_KEPT:
        out.pop("f8949_parts", None)
    # A field's disposition is in ``lines``; keep only the reasons a blocked field shows.
    out["field_reasons"] = {k: f["reasons"] for k, f in (out.pop("fields", None) or {}).items()
                            if isinstance(f, dict) and f.get("reasons")} | (out.get("field_reasons") or {})
    return {k: v for k, v in out.items() if v not in (None, [], {})}


def same(a: dict[str, Any], b: dict[str, Any]) -> bool:
    keys = ("error", "lines", "attachments", "questions", "rows", "blocked")
    return all((a.get(k) or None) == (b.get(k) or None) for k in keys)


def shrink(payload: dict[str, Any]) -> dict[str, Any]:
    for section in ("final", "decided"):
        for name, case in (payload.get(section) or {}).items():
            if isinstance(case.get("result"), dict):
                case["result"] = shrink_result(case["result"], name)
    final = payload.get("final") or {}
    for name, case in (payload.get("decided") or {}).items():
        if name in final and isinstance(case.get("result"), dict) and same(case["result"], final[name]["result"]):
            payload["decided"][name] = {"same_as_final": True, "mismatch": case.get("mismatch")}
    for name, probe_ in (payload.get("neighbour_probes") or {}).items():
        for kind in list(probe_):
            probe_[kind] = shrink_result(probe_[kind], name)
    return payload


def dump(payload: dict[str, Any]) -> str:
    payload = shrink(payload)
    lines = ["{"]
    keys = sorted(payload)
    for i, key in enumerate(keys):
        value = payload[key]
        end = "," if i < len(keys) - 1 else ""
        if isinstance(value, dict) and key in ("final", "decided", "v80_returns_on_v81", "neighbour_probes"):
            lines.append(f" {json.dumps(key)}: {{")
            names = sorted(value)
            for j, name in enumerate(names):
                comma = "," if j < len(names) - 1 else ""
                lines.append(f"  {json.dumps(name)}: {json.dumps(value[name], sort_keys=True, default=str)}{comma}")
            lines.append(f" }}{end}")
        else:
            lines.append(f" {json.dumps(key)}: {json.dumps(value, sort_keys=True, default=str)}{end}")
    lines.append("}")
    return probe.scrub("\n".join(lines)) + "\n"


def compact_case(case: dict[str, Any], sentences: dict[str, dict[str, str]]) -> dict[str, Any]:
    """Store each field's explanation once per disposition under ``field_sentences``."""
    result = case.get("result") or {}
    for field_name, field in list((result.get("fields") or {}).items()):
        if field_name not in PROBED_FIELDS:
            result["fields"].pop(field_name)
            continue
        explain = field.pop("explain", None)
        if explain is not None:
            sentences.setdefault(field_name, {})[field["disposition"]] = explain
    return case


def all_names() -> list[str]:
    return list({**cbp.new_cases(), **track0_cases()})


def pool_run(repairs: list[str], tasks: list[tuple[str, str]], workers: int, label: str) -> dict[str, dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {}
    with ProcessPoolExecutor(min(workers, max(1, len(tasks))), initializer=init, initargs=(repairs,)) as pool:
        for (kind, name), result in pool.map(run, tasks):
            results.setdefault(kind, {})[name] = result
            shown = result.get("mismatch") if "mismatch" in result else cbp.form1040(result)
            print(label, kind, name, result.get("error") or (result.get("result") or {}).get("error") or "",
                  shown if shown else "ok", flush=True)
    return results


def carry_table(results: dict[str, dict[str, Any]]) -> dict[str, Any]:
    carry = {}
    for name in sorted(results.get("v80", {})):
        before, after, untouched = (results[k][name] for k in ("v80", "v81_q3_no", "v81_q3_unanswered"))
        carry[name] = {
            "v80": {"form1040": cbp.form1040(before), "attachments": before.get("attachments"), "error": before.get("error")},
            "v81_q3_no_diff": cbp.compare(before, after),
            "v81_q3_no_lines_1b_8b": {k: (after.get("lines") or {}).get(k) for k in ("schedule-d.line-1b", "schedule-d.line-8b")},
            "v81_q3_no_publisher_rows": sorted({n for n, c in (after.get("publisher_rows") or {}).items() if c != 1}),
            "v81_q3_unanswered_form1040": cbp.form1040(untouched),
            "v81_q3_unanswered_asks_q3": cbp.Q3_TEXT in (untouched.get("questions") or []),
            "v81_q3_unanswered_error": untouched.get("error"),
        }
    return carry


def main() -> None:
    args = sys.argv[1:]
    final = sorted(cbp.ALL_REPAIRS)
    if args[:1] == ["shrink"]:  # rewrite the output through shrink() only
        OUT.write_text(dump(json.loads(OUT.read_text(encoding="utf-8"))), encoding="utf-8")
        return
    if args[:1] == ["surface"]:
        payload = json.loads(OUT.read_text(encoding="utf-8"))
        init(final)
        payload["surface"] = surface(STATE["content"])
        OUT.write_text(dump(payload), encoding="utf-8")
        return
    if args[:1] == ["neighbours"]:  # rerun the neighbour probes only and merge them
        payload = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
        results = pool_run(final, [(k, n) for n in NEIGHBOUR for k in ("v80", "v81_q3_no")], 8, "neighbour")
        payload["neighbour_probes"] = {n: {"v80": results["v80"][n], "v81_q3_no": results["v81_q3_no"][n]} for n in NEIGHBOUR}
        OUT.write_text(dump(payload), encoding="utf-8")
        return
    if args[:1] == ["only"]:
        design, names = args[1], args[2:]
        payload = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
        repairs = final if design == "final" else []
        results = pool_run(repairs, [("case", n) for n in names], 8, design)
        sentences = payload.setdefault("field_sentences", {}) if design == "final" else {}
        for name, case in results.get("case", {}).items():
            payload.setdefault(design, {})[name] = compact_case(case, sentences)
        OUT.write_text(dump(payload), encoding="utf-8")
        return
    # Two parts, each in its own foreground run: ``cases`` (both designs) and ``carry``
    # (every v80 return, and the neighbour probes). No argument runs both.
    workers = int(args[0]) if args and args[0].isdigit() else 8
    # ``carry`` may name a shard, ``carry 1/2``: every second carried return and probe, merged into the output.
    shard = next(((int(a.split("/")[0]), int(a.split("/")[1])) for a in args if "/" in a), None)
    parts = {a for a in args if not a.isdigit() and "/" not in a} or {"cases", "carry"}
    payload = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    payload.update({"source_ref": "milestone/f8949-code-b-2025", "repairs": final})
    init(final)
    payload["build"], payload["surface"] = STATE["build"], surface(STATE["content"])
    if "cases" in parts:
        names = all_names()
        results = pool_run(final, [("case", n) for n in names], workers, "final")
        decided = pool_run([], [("case", n) for n in names], workers, "decided").get("case", {})
        sentences: dict[str, dict[str, str]] = {}
        payload["final"] = {n: compact_case(c, sentences) for n, c in results["case"].items()}
        payload["decided"] = {n: compact_case(c, {}) for n, c in decided.items()}
        payload["field_sentences"] = sentences
    if "carry" in parts:
        carry_names = sorted(cbp.v80_world())
        probe_names = list(NEIGHBOUR)
        if shard is not None:
            index, count = shard
            carry_names = carry_names[index - 1::count]
            probe_names = probe_names[index - 1::count]
        tasks = [(k, n) for n in carry_names for k in ("v80", "v81_q3_no", "v81_q3_unanswered")]
        tasks += [(k, n) for n in probe_names for k in ("v80", "v81_q3_no")]
        results = pool_run(final, tasks, workers, "carry")
        carried = carry_table({k: {n: r for n, r in v.items() if n not in NEIGHBOUR} for k, v in results.items()})
        probed = {n: {"v80": results["v80"][n], "v81_q3_no": results["v81_q3_no"][n]} for n in probe_names}
        if shard is None:
            payload["v80_returns_on_v81"], payload["neighbour_probes"] = carried, probed
        else:
            payload.setdefault("v80_returns_on_v81", {}).update(carried)
            payload.setdefault("neighbour_probes", {}).update(probed)
    payload.pop("decided_design", None)
    OUT.write_text(dump(payload), encoding="utf-8")
    print(f"wrote {OUT.name}", flush=True)


if __name__ == "__main__":
    main()
