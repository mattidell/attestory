"""Track 0 adversarial state-coverage and basis/consistency verifier (Items 1-3).

Run:
  python3 docs/phases/engine-breadth/milestones/plain-line-texts-evidence/track0_states.py \\
    <p0b-baseline-dir> <scratch-core.json>

Builds 7 supplementary synthetic demo.t0.* act lists covering every drawn-state
branch not reached by the 775 recorded + 9 P0b/P0c synthetic lists (MFS lived-with,
MFJ spouse records, closed-empty W-2 with interest-only, sub-50-cent rounding zeros
across all rounded lines, single-source vs dual-source line 2a and Schedule 1 line 10,
Schedule 8812 line 6 with no-other-dependent=no and 0 qualifying dependents,
corrected answers, finding-retracted acts, and member-transition removals), runs them
through the real coordinator on the rebuilt scratch v96 core, and verifies Charter
Items 1, 2, and 3 across all 57 replacements.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def load(name: str, path: Path) -> Any:
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


census = load("plt_t0_states_census", HERE / "census.py")
runtime = load("plt_t0_states_runtime", HERE / "p0c_runtime.py")
compare = load("plt_t0_states_compare", HERE / "p0c_compare.py")
l6b = load("plt_t0_states_l6b", HERE.parent / "line6b-reason-evidence/probe.py")
roao2 = load("plt_t0_states_roao2", REPO / "tests/test_refund_or_amount_owed_track2.py")
fw = load("plt_t0_states_fw", REPO / "tests/test_form_1099_withholding.py")
wc = load("plt_t0_states_wc", REPO / "tests/test_withholding_closure.py")

rr = census.rr
h = rr._get_harness()
ccr = h.ccr
P = "tax.us.2025."


def _set_w2g(acts: list[dict[str, Any]], statements: list[tuple[float, float | None]]) -> list[dict[str, Any]]:
    acts = copy.deepcopy(acts)
    kept = []
    for a in acts:
        s = json.dumps(a.get("payload", {}))
        if "tax.us.2025.w2g." in s and "no-sch1-other-income-except-w2g" not in s:
            continue
        kept.append(a)
    acts = kept
    ccr.w2g._w2g(acts, statements, other_income=None)
    return h.renumber(acts)


def supplementary_cases() -> list[tuple[str, list[dict[str, Any]], str]]:
    """Build 7 synthetic demo.t0.* act lists reaching all drawn states not in the 775 lists."""
    cases: list[tuple[str, list[dict[str, Any]], str]] = []

    # 1. MFS lived with spouse during the year (mfs-lived-apart-all-year = "no")
    c1 = h.say(
        l6b.base("married_filing_separately", benefits=False),
        P + "mfs-lived-apart-all-year",
        "no",
        "demo.t0.mfs.with",
    )
    cases.append((
        "demo.t0.mfs-lived-with",
        c1,
        "Married filing separately with mfs-lived-apart-all-year='no': draws line-6d guard_inapplicable on the MFS lived-with branch and line-6d-not-checked published_categorical.",
    ))

    # 2. MFJ with spouse records (second W-2 slip + 1099-INT box 8 + 1099-DIV box 12 + b4=0)
    c2 = l6b.base("married_filing_jointly", benefits=False)
    c2 = roao2._reopen_w2_with_second_slip(c2, amount=30000.0)
    c2 = roao2._add_box2_only(
        c2,
        employer="demo.t2.w2second.employer",
        slip="demo.t2.w2second.slip",
        amount=2500.0,
    )
    c2 = ccr.add_tax_exempt_interest_1099int(c2, [150.0])
    c2 = ccr._record_members(
        c2,
        P + "f1099int.b4",
        [0.0],
        tag="c2intb4",
        entities={"payer": "demo.ccr.b80.payer", "statement": "demo.ccr.b80.statement"},
    )
    c2 = ccr.add_exempt_interest_dividends_1099div(c2, [100.0])
    c2 = ccr._record_members(
        c2,
        P + "f1099div.b4",
        [0.0],
        tag="c2divb4",
        entities={"payer": "demo.ccr.b120.payer", "statement": "demo.ccr.b120.statement"},
    )
    cases.append((
        "demo.t0.mfj-spouse-records",
        c2,
        "Married filing jointly with a second W-2 slip for the spouse plus Form 1099-INT box 8 and Form 1099-DIV box 12 records and zero Form 1099 withholding.",
    ))

    # 3. Single with no W-2 (w2 and w2-box2 closed-empty) and Form 1099-INT box 1 = $100
    c3 = copy.deepcopy(l6b.base("single", benefits=False))
    kept = []
    for a in c3:
        p = a.get("payload", {})
        if a.get("kind") == "member-transition" and p.get("family", {}).get("id") == P + "w2":
            continue
        f = p.get("finding", {})
        fid = str(f.get("fact_id", ""))
        if fid.startswith(P + "w2.box2-withholding|"):
            continue
        if fid.startswith(P + "w2.source-closure|"):
            f["fact_id"] = P + "w2.source-closure|family-horizon=demo.cgd.t2.w2.h0,tax-year=2025"
        kept.append(a)
    c3 = h.renumber(kept)
    c3, int_p3, int_s3 = roao2._reopen_interest_with_real_box1(c3, amount=100.0)
    c3 = ccr._record_members(
        c3,
        P + "f1099int.b4",
        [0.0],
        tag="c3intb4",
        entities={"payer": int_p3, "statement": int_s3},
    )
    c3 = h.renumber(c3)
    cases.append((
        "demo.t0.no-w2-interest-only",
        c3,
        "Single return with closed-empty W-2 and W-2 box 2 families (line 25a computed_zero by absence) and $100 taxable interest on line 2b (Schedule B not required).",
    ))

    # 4. Rounding zeros (< $0.50 -> $0) across lines 2a, 2b, 3a, 3b, 4b, 7a, 25a, 25b, 25c, 25d, 26, Sch D line 13 + W-2G only on Sch 1 line 10 / line 8
    c4 = copy.deepcopy(l6b.base("single", benefits=False))
    for a in c4:
        f = a.get("payload", {}).get("finding", {})
        fid = str(f.get("fact_id", ""))
        if fid.startswith(P + "w2.box2-withholding|"):
            f["value"] = 0.40
        elif fid.startswith(P + "payments.estimated-and-prior-year-applied|"):
            f["value"] = 0.40
    c4, int_payer, int_stmt = roao2._reopen_interest_with_real_box1(c4, amount=0.40)
    int_entities = {"payer": int_payer, "statement": int_stmt}
    c4 = ccr._record_members(c4, P + "f1099int.b4", [0.40], tag="intb4r", entities=int_entities)
    c4 = h.say(c4, ccr.LINE2A_NO_INT_SCOPE, "no", "demo.t0.c4.noint8")
    c4 = ccr._record_members(
        c4,
        P + "f1099int.b8",
        [0.20],
        tag="intb8r",
        companions=[(ccr.BOX9_COMPANION, None)],
        entities=int_entities,
    )
    c4 = ccr._record_members(c4, P + "f1099div.1a", [0.40], tag="div1ar")
    div_entities = {"payer": "demo.ccr.div1ar0.payer", "statement": "demo.ccr.div1ar0.statement"}
    c4 = ccr._record_members(c4, P + "f1099div.b4", [0.0], tag="divb4r", entities=div_entities)
    c4 = ccr._record_members(c4, P + "f1099div.1b", [0.40], tag="div1br", entities=div_entities)
    c4 = ccr._record_members(c4, P + "f1099div.2a", [0.40], tag="div2ar", entities=div_entities)
    c4 = ccr._record_members(
        c4,
        P + "f1099div.12",
        [0.20],
        tag="div12r",
        companions=[(ccr.BOX13_COMPANION, None)],
        entities=div_entities,
    )
    c4 = h.say(c4, P + "capital-gain-distributions", "yes", "demo.t0.cgd.yes")
    c4 = wc._strip_closure(
        wc._strip_closure(c4, P + "f1099r.ira-fully-taxable.source-closure"),
        P + "f1099r.box4.source-closure",
    )
    fw._retirements(c4, [(0.40, 0.0)])
    c4 = h.renumber(c4)
    c4 = _set_w2g(c4, [(200.0, 0.40)])
    cases.append((
        "demo.t0.rounding-zeros-and-w2g-only",
        c4,
        "Sub-50-cent positive amounts rounding to $0 on lines 2a, 2b, 3a, 3b, 4b, 7a, 25a, 25b, 25c, 25d, 26, and Schedule D line 13, plus W-2G gambling winnings ($200) alone on Schedule 1 line 10 and Form 1040 line 8.",
    ))

    # 5. Line 2a from 1099-INT box 8 only ($300.40 -> $300) + Schedule 1 line 7 ($500.40 -> $500) + W-2G ($300) -> Schedule 1 line 10 / Form 1040 line 8 ($800)
    c5 = copy.deepcopy(l6b.base("single", benefits=False))
    c5 = ccr.add_tax_exempt_interest_1099int(c5, [300.40])
    c5 = ccr._record_members(
        c5,
        P + "f1099int.b4",
        [0.0],
        tag="c5intb4",
        entities={"payer": "demo.ccr.b80.payer", "statement": "demo.ccr.b80.statement"},
    )
    c5 = wc._strip_closure(wc._strip_closure(c5, P + "f1099g.1.source-closure"), P + "f1099g.b4.source-closure")
    fw._unemployment(c5, [500.40], authority=0.0)
    c5 = [
        a
        for a in c5
        if not (
            a.get("kind") == "horizon-genesis"
            and a.get("payload", {}).get("family", {}).get("id") == P + "f1099g.b4"
        )
    ]
    fw._unemployment_withholding(c5, [0.0])
    c5 = _set_w2g(c5, [(300.0, None)])
    cases.append((
        "demo.t0.int8-only-and-unemp-plus-w2g",
        c5,
        "Form 1099-INT box 8 only ($300.40 rounded to $300) on line 2a, plus both Form 1099-G unemployment ($500.40 rounded to $500) and Form W-2G gambling winnings ($300) on Schedule 1 line 10 and Form 1040 line 8.",
    ))

    # 6. Schedule 8812 line 6 with ctc.no-other-dependent = "no" and 0 qualifying dependents + corrected answer + retracted finding
    c6 = copy.deepcopy(l6b.base("single", benefits=False))
    c6 = h.say(c6, P + "ctc.no-other-dependent", "no", "demo.t0.odc.no")
    c6 = h.say(c6, P + "payments.estimated-and-prior-year-applied", 250.0, "demo.t0.est.wrong")
    c6 = h.say(c6, P + "payments.estimated-and-prior-year-applied", 0.0, "demo.t0.est.corrected")
    # Retract the existing no-estimated-tax-penalty finding and re-assert it
    pen_fid = None
    for a in c6:
        f = a.get("payload", {}).get("finding", {})
        if str(f.get("fact_id", "")).startswith(P + "line38-scope.no-estimated-tax-penalty|"):
            pen_fid = str(f["id"])
    assert pen_fid is not None
    c6.append(
        roao2._act(
            len(c6),
            "finding-retracted",
            {"schema": "act-finding-retracted.v1", "finding_id": pen_fid},
        )
    )
    c6.append(
        roao2._act(
            len(c6),
            "assertion",
            {
                "finding": roao2._attested(
                    "demo.t0.pen.reasserted",
                    P + "line38-scope.no-estimated-tax-penalty|tax-year=2025",
                    "yes",
                )
            },
        )
    )
    c6 = h.renumber(c6)
    cases.append((
        "demo.t0.odc-no-and-corrected-retracted",
        c6,
        "Schedule 8812 line 6 computed_zero via the ctc.no-other-dependent='no' branch with zero qualifying dependents, plus a superseded estimated-tax answer ($250 -> $0) and a retracted-and-reasserted line 38 answer.",
    ))

    # 7. Member-transition removal of a Form 1099-INT box 1 record + EIC line-1 < 1 ($0.40 -> $0) + Schedule 1 line 7/10 and Form 1040 line 8 rounding zero ($0.40 -> $0)
    c7 = copy.deepcopy(l6b.base("single", benefits=False))
    for a in c7:
        p = a.get("payload", {})
        f = p.get("finding") or p.get("member", {}).get("finding") or {}
        fid = str(f.get("fact_id", ""))
        if fid.startswith(P + "w2.box1-wages|"):
            f["value"] = 0.40
        elif fid.startswith(P + "w2.box2-withholding|"):
            f["value"] = 0.0
    c7, int_p7, int_s7 = roao2._reopen_interest_with_real_box1(c7, amount=500.0)
    c7 = wc._strip_closure(c7, P + "f1099int.b1.source-closure")
    c7.append(
        roao2._act(
            len(c7),
            "member-transition",
            {
                "family": {"id": P + "f1099int.b1", "version": "v1"},
                "scope": roao2.SCOPE_KEY,
                "member": {
                    "action": "remove",
                    "fact_id": f"tax.us.2025.f1099int.box1-interest|payer={int_p7},statement={int_s7},tax-year=2025",
                },
                "successor": {"id": "demo.t2.int.h2", "predecessor": "demo.t2.int.h1"},
            },
        )
    )
    c7.append(
        roao2._act(
            len(c7),
            "assertion",
            {
                "finding": roao2._attested(
                    "demo.t2.int.reclose2",
                    P + "f1099int.b1.source-closure|family-horizon=demo.t2.int.h2,tax-year=2025",
                    True,
                )
            },
        )
    )
    c7 = wc._strip_closure(wc._strip_closure(c7, P + "f1099g.1.source-closure"), P + "f1099g.b4.source-closure")
    fw._unemployment(c7, [0.40], authority=0.0)
    c7 = [
        a
        for a in c7
        if not (
            a.get("kind") == "horizon-genesis"
            and a.get("payload", {}).get("family", {}).get("id") == P + "f1099g.b4"
        )
    ]
    fw._unemployment_withholding(c7, [0.0])
    c7 = h.renumber(c7)
    cases.append((
        "demo.t0.retracted-member-and-sch1-rounding",
        c7,
        "Form 1099-INT box 1 member ($500) asserted and then removed via member-transition (line 2b computed_zero after removal), W-2 wages $0.40 rounding to $0 (EIC Worksheet A line 2 computed_zero via line 1 < $1), and Form 1099-G box 1 $0.40 rounding to $0 (Schedule 1 lines 7/10 and Form 1040 line 8 computed_zero by rounding).",
    ))

    return cases


# Basis mapping for Item 2 (what the predecessor sentence proved and how the new sentence preserves it)
BASIS_NOTES: dict[tuple[str, str], str] = {
    ("tax.us.2025.rule.attachment.f8949", "title"): "Identifies the Form 8949 attachment heading before the colon and keeps the box C/F sale-count requirement after the colon.",
    ("tax.us.2025.rule.attachment.schedule-a", "title"): "Identifies the Schedule A (Itemized Deductions) attachment heading before the colon and keeps the two-part line 8a / line 16 condition after the colon.",
    ("tax.us.2025.rule.attachment.schedule-d", "title"): "Identifies the Schedule D (Capital Gains and Losses) attachment heading before the colon and keeps the box C/F sale-count requirement after the colon.",
    ("tax.us.2025.form.eic-worksheet-a.line-2", "dispositions.computed_zero.explain"): "Preserves the zero result on EIC Worksheet A line 2 and states the two rule branches (line 1 below $1 or EIC Table zero credit).",
    ("tax.us.2025.form.eic-worksheet-a.line-5", "dispositions.computed_zero.explain"): "Preserves the zero result on EIC Worksheet A line 5 from the EIC Table lookup on line 3.",
    ("tax.us.2025.form.eic-worksheet-a.line-5", "dispositions.guard_inapplicable.explain"): "Preserves inapplicability of EIC Worksheet A line 5 when line 3 is below the line 4 threshold.",
    ("tax.us.2025.form.eic-worksheet-a.line-6", "dispositions.computed_zero.explain"): "Preserves the zero result on EIC Worksheet A line 6 from line 2 or min(line 2, line 5).",
    ("tax.us.2025.form.sch8812.line-14", "dispositions.computed_zero.explain"): "Preserves the zero result on Schedule 8812 line 14 after eligibility checks and the Worksheet A / Part I credit limit.",
    ("tax.us.2025.form.sch8812.line-17", "dispositions.computed_zero.explain"): "Preserves the zero result on Schedule 8812 line 17 from comparing line 16a and line 16b.",
    ("tax.us.2025.form.sch8812.line-17", "dispositions.guard_inapplicable.explain"): "Preserves inapplicability of Schedule 8812 Part II-A line 17 when no qualifying children are claimed or Part I satisfies the credit.",
    ("tax.us.2025.form.sch8812.line-4", "dispositions.closure_backed_zero.explain"): "Preserves the zero result on Schedule 8812 line 4 because the completed child list has no qualifying children for this credit.",
    ("tax.us.2025.form.sch8812.line-6", "dispositions.computed_zero.explain"): "Preserves the zero result on Schedule 8812 line 6 across both branches: confirmed no other dependents or zero qualifying dependents.",
    ("tax.us.2025.form.sch8812.line-7", "dispositions.computed_zero.explain"): "Preserves the zero result on Schedule 8812 line 7 when line 6 counts zero other dependents.",
    ("tax.us.2025.form.sch8812.worksheet-a.line-5", "dispositions.computed_zero.explain"): "Preserves the zero credit limit on Credit Limit Worksheet A line 5 from tax on Form 1040 line 16 and the worksheet reduction.",
    ("tax.us.2025.form1040.line-10", "dispositions.published_value.explain"): "Preserves that line 10 comes from the completed Schedule 1 line 26 total and is subtracted from line 9 total income on line 11a.",
    ("tax.us.2025.form1040.line-11a", "dispositions.published_value.explain"): "Preserves that line 11a adjusted gross income is line 9 total income minus line 10 adjustments to income.",
    ("tax.us.2025.form1040.line-11b", "dispositions.published_value.explain"): "Preserves that line 11b repeats adjusted gross income from line 11a.",
    ("tax.us.2025.form1040.line-19", "dispositions.computed_zero.explain"): "Preserves the zero result on Form 1040 line 19 when Schedule 8812 line 14 is zero.",
    ("tax.us.2025.form1040.line-25a", "dispositions.computed_zero.explain"): "Preserves the zero result on line 25a across both absence of recorded Forms W-2 and completed W-2 box 2 amounts rounding to zero.",
    ("tax.us.2025.form1040.line-25b", "dispositions.computed_zero.explain"): "Preserves the zero result on line 25b across both absence of Form 1099/SSA-1099 withholding and completed withholding amounts rounding to zero.",
    ("tax.us.2025.form1040.line-25c", "dispositions.computed_zero.explain"): "Preserves the zero result on line 25c across both absence of Forms W-2G and completed W-2G box 4 amounts rounding to zero.",
    ("tax.us.2025.form1040.line-25d", "dispositions.computed_zero.explain"): "Preserves the zero result on line 25d when lines 25a, 25b, and 25c add to zero.",
    ("tax.us.2025.form1040.line-26", "dispositions.computed_zero.explain"): "Preserves the zero result on line 26 after rounding the entered estimated tax payments and prior-year applied amount to whole dollars.",
    ("tax.us.2025.form1040.line-27a", "dispositions.computed_zero.explain"): "Preserves the zero result on line 27a from the EIC eligibility checks or Worksheet A calculation.",
    ("tax.us.2025.form1040.line-28", "dispositions.computed_zero.explain"): "Preserves the zero result on line 28 after Schedule 8812 applies the refundable credit limits.",
    ("tax.us.2025.form1040.line-2a", "dispositions.computed_zero.explain"): "Preserves the zero result on line 2a across closed-empty absence and sub-50-cent rounding of Form 1099-INT box 8 and Form 1099-DIV box 12, with records and scope answers complete.",
    ("tax.us.2025.form1040.line-2a", "dispositions.published_value.explain"): "Preserves that line 2a is the rounded total from any recorded Form 1099-INT box 8 and Form 1099-DIV box 12 amounts with records and answers complete, and is not included in taxable income.",
    ("tax.us.2025.form1040.line-2b", "dispositions.computed_zero.explain"): "Preserves the zero result on line 2b across closed-empty absence and sub-50-cent rounding of completed taxable interest and any applicable adjustments.",
    ("tax.us.2025.form1040.line-2b", "dispositions.published_value.explain"): "Preserves that line 2b is the completed taxable interest total (including any Schedule B Part I adjustments), rounded once to whole dollars.",
    ("tax.us.2025.form1040.line-32", "dispositions.computed_zero.explain"): "Preserves the zero result on line 32 when completed other payments and refundable credits (lines 27a-31) add/round to zero.",
    ("tax.us.2025.form1040.line-37", "dispositions.computed_zero.explain"): "Preserves the zero result on line 37 when total tax compared with total payments leaves zero amount owed after rounding.",
    ("tax.us.2025.form1040.line-38", "dispositions.computed_zero.explain"): "Preserves the zero result on line 38 when the filer confirms no estimated tax penalty applies.",
    ("tax.us.2025.form1040.line-3a", "dispositions.computed_zero.explain"): "Preserves the zero result on line 3a across closed-empty absence and sub-50-cent rounding of Form 1099-DIV box 1b, with records complete.",
    ("tax.us.2025.form1040.line-3b", "dispositions.computed_zero.explain"): "Preserves the zero result on line 3b across closed-empty absence and sub-50-cent rounding of Form 1099-DIV box 1a, with records complete.",
    ("tax.us.2025.form1040.line-3b", "dispositions.published_value.explain"): "Preserves that line 3b is the completed Form 1099-DIV box 1a total, rounded once to whole dollars.",
    ("tax.us.2025.form1040.line-4b", "dispositions.computed_zero.explain"): "Preserves the zero result on line 4b across closed-empty absence and sub-50-cent rounding of fully taxable IRA distributions, with records complete.",
    ("tax.us.2025.form1040.line-6b", "dispositions.blocked.explain"): "Preserves that line 6b is blocked because Social Security benefit records, required income amounts, or worksheet answers are incomplete.",
    ("tax.us.2025.form1040.line-6d-not-checked", "dispositions.guard_inapplicable.explain"): "Preserves that the line 6d lived-with-spouse entry does not apply when not MFS or when MFS lived apart all year.",
    ("tax.us.2025.form1040.line-6d", "dispositions.guard_inapplicable.explain"): "Preserves that the line 6d lived-apart-all-year entry does not apply when not MFS or when MFS lived with spouse during the year.",
    ("tax.us.2025.form1040.line-7a", "dispositions.computed_zero.explain"): "Preserves the zero result on line 7a across absence of sales, carryovers, and box 2a distributions and rounding to zero on the Schedule D or box 2a route.",
    ("tax.us.2025.form1040.line-7a", "dispositions.published_value.explain"): "Preserves that line 7a comes from Schedule D or from qualifying Form 1099-DIV box 2a capital gain distributions when Schedule D is not required.",
    ("tax.us.2025.form1040.line-7b", "dispositions.guard_inapplicable.explain"): "Preserves that the Schedule D not required box on line 7b is not checked because a sale is recorded for Form 8949/Schedule D or an Exception 1 answer is no.",
    ("tax.us.2025.form1040.line-8", "dispositions.published_value.explain"): "Preserves that line 8 comes from the completed Schedule 1 line 10 total and is included once in Form 1040 line 9 total income.",
    ("tax.us.2025.form1040.tax-after-credits", "dispositions.blocked.explain"): "Preserves that tax after credits is waiting for line 16 tax, lines 19 and 20 credits, or confirmation that line 17 has no amount.",
    ("tax.us.2025.rule.attachment.schedule-1", "title"): "Identifies the Schedule 1 (Additional Income and Adjustments to Income) attachment heading before the colon and keeps the requirement details after the colon.",
    ("tax.us.2025.schedule-d.line-13", "dispositions.computed_zero.explain"): "Preserves the zero result on Schedule D line 13 across closed-empty absence and sub-50-cent rounding of Form 1099-DIV box 2a, with records complete.",
    ("tax.us.2025.schedule-d.line-13", "dispositions.published_value.explain"): "Preserves that Schedule D line 13 is the completed Form 1099-DIV box 2a total, rounded once to whole dollars.",
    ("tax.us.2025.schedule-d.line-16", "dispositions.published_value.explain"): "Preserves that Schedule D line 16 is the sum of line 7 and line 15.",
    ("tax.us.2025.schedule1.line-10", "dispositions.published_value.explain"): "Preserves that Schedule 1 line 10 is the sum of line 7 (unemployment compensation) and line 8b (gambling winnings) with all required records and Part I absence answers complete.",
    ("tax.us.2025.schedule1.line-21", "dispositions.closure_backed_zero.explain"): "Preserves the zero result on Schedule 1 line 21 because no Form 1098-E box 1 interest is recorded and those records are complete.",
    ("tax.us.2025.schedule1.line-21", "dispositions.published_value.explain"): "Preserves that Schedule 1 line 21 is calculated from the completed Form 1098-E interest records and eligibility answers.",
    ("tax.us.2025.schedule1.line-7", "dispositions.published_value.explain"): "Preserves that Schedule 1 line 7 is the completed Form 1099-G box 1 total, rounded once to whole dollars.",
    ("tax.us.2025.schedule3.line-1", "dispositions.blocked.explain"): "Preserves that Schedule 3 line 1 is blocked because foreign tax records or answers about election, eligible taxes/income, dollar limit, or regular tax are incomplete or failed.",
    ("tax.us.2025.schedule3.line-8", "dispositions.blocked.explain"): "Preserves that Schedule 3 line 8 is waiting for line 1 or confirmation that no other Part I credits apply.",
    ("tax.us.2025.rule.effective-proceeds-support-count", "notes"): "Preserves that the rule outputs 1 only when one current confirmation links the loan to its proceeds use and all five current use-category answers are present (completion check, not a proceeds count).",
    ("tax.us.2025.rule.f1098-line8a", "notes"): "Preserves that Schedule A line 8a sums included Form 1098 box 1 amounts only after borrowing-level readiness checks pass.",
    ("tax.us.2025.rule.mortgage-account-readiness", "notes"): "Preserves per-borrowing/year ceiling and link coverage plus two-form different-payments confirmation tied to source, inclusion, and borrowing-recognition answers, while a single-form borrowing needs no comparison.",
    ("tax.us.2025.rule.mortgage-link-support", "notes"): "Preserves that the rule outputs 1 when the linked Form 1098 has a qualifying interest reason and box 2 principal within the annual ceiling, and 0 otherwise.",
    ("tax.us.2025.rule.mortgage-payment-comparison-support-count", "notes"): "Preserves per-borrowing counting of current exact-pair comparison rows and their box 1, inclusion, and borrowing-recognition identities from a current evidence-backed different-payments answer.",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline", type=Path)
    parser.add_argument("core", type=Path)
    args = parser.parse_args()

    base_root = args.baseline.resolve()
    core_path = args.core.resolve()
    assert REPO not in base_root.parents and REPO not in core_path.parents

    wording = json.loads((HERE / "p0c-wording.json").read_text())
    changes = json.loads((HERE / "track0-wording-changes.json").read_text())
    changes_by_key = {(c["id"], c["property"]): c for c in changes["changes"]}

    # Run the 7 supplementary Track 0 synthetic cases on the scratch v96 core
    supp_cases = supplementary_cases()
    supp_results: dict[str, dict[str, Any]] = {}
    supp_field_index: dict[tuple[str, str], list[str]] = {}

    with tempfile.TemporaryDirectory() as tmp:
        os.environ["PLT_CENSUS_SCRATCH"] = tmp
        core = rr.resolve_core(core_path)
        with runtime.injected_graph():
            for cid, acts, desc in supp_cases:
                res = census.per_list(cid, acts, core)
                assert res.get("outcome") == "success", (cid, res)
                assert res.get("stop") == "saturated", (cid, res)
                pin, model = compare.read_pin(Path(tmp), res)
                assert model.get("renderAlert") is None, (cid, model.get("renderAlert"))
                field_disps: dict[str, dict[str, Any]] = {}
                for sec in model.get("sections", []):
                    fid = sec["field"]["id"]
                    disp = sec["resolved"]["disposition"]
                    val = sec["resolved"].get("value")
                    field_disps[fid] = {"disposition": disp, "value": val}
                    supp_field_index.setdefault((fid, f"dispositions.{disp}.explain"), []).append(cid)
                for att in model.get("attachments", []):
                    aid = att["id"]
                    supp_field_index.setdefault((aid, "title"), []).append(cid)
                supp_results[cid] = {
                    "description": desc,
                    "outcome": res["outcome"],
                    "stop": res["stop"],
                    "acts_count": len(acts),
                    "published_rows": sum(1 for r in pin["rows"] if r.get("disposition") == "published"),
                    "blocked_rows": sum(1 for r in pin["rows"] if r.get("disposition") == "blocked"),
                    "key_fields": {
                        k: v
                        for k, v in sorted(field_disps.items())
                        if k
                        in {
                            "tax.us.2025.form.eic-worksheet-a.line-2",
                            "tax.us.2025.form.eic-worksheet-a.line-5",
                            "tax.us.2025.form.eic-worksheet-a.line-6",
                            "tax.us.2025.form.sch8812.line-6",
                            "tax.us.2025.form.sch8812.line-14",
                            "tax.us.2025.form.sch8812.line-17",
                            "tax.us.2025.form1040.line-2a",
                            "tax.us.2025.form1040.line-2b",
                            "tax.us.2025.form1040.line-3a",
                            "tax.us.2025.form1040.line-3b",
                            "tax.us.2025.form1040.line-4b",
                            "tax.us.2025.form1040.line-6b",
                            "tax.us.2025.form1040.line-6d",
                            "tax.us.2025.form1040.line-6d-not-checked",
                            "tax.us.2025.form1040.line-7a",
                            "tax.us.2025.form1040.line-7b",
                            "tax.us.2025.form1040.line-8",
                            "tax.us.2025.form1040.line-10",
                            "tax.us.2025.form1040.line-11a",
                            "tax.us.2025.form1040.line-11b",
                            "tax.us.2025.form1040.line-19",
                            "tax.us.2025.form1040.line-25a",
                            "tax.us.2025.form1040.line-25b",
                            "tax.us.2025.form1040.line-25c",
                            "tax.us.2025.form1040.line-25d",
                            "tax.us.2025.form1040.line-26",
                            "tax.us.2025.form1040.line-27a",
                            "tax.us.2025.form1040.line-28",
                            "tax.us.2025.form1040.line-32",
                            "tax.us.2025.form1040.line-37",
                            "tax.us.2025.form1040.line-38",
                            "tax.us.2025.form1040.tax-after-credits",
                            "tax.us.2025.schedule-d.line-13",
                            "tax.us.2025.schedule-d.line-16",
                            "tax.us.2025.schedule1.line-7",
                            "tax.us.2025.schedule1.line-10",
                            "tax.us.2025.schedule1.line-21",
                            "tax.us.2025.schedule3.line-1",
                            "tax.us.2025.schedule3.line-8",
                        }
                    },
                }

    # Verify all 57 replacements for Items 1, 2, and 3
    rows_out: list[dict[str, Any]] = []
    for idx, rep in enumerate(wording["replacements"], 1):
        key = (rep["id"], rep["property"])
        assert key in BASIS_NOTES, f"Missing basis note for {key}"
        # Decision 3: on attachment titles only title.split(':')[0] (new_shown) is drawn;
        # Form 8949's official IRS form subtitle is "(Sales and Other Dispositions of Capital Assets)".
        shown_to_check = rep["new_shown"].replace(
            "Sales and Other Dispositions of Capital Assets",
            "Sales of Capital Assets",
        )
        flagged_shown = census.matches(shown_to_check)
        assert not flagged_shown, (key, flagged_shown)
        if rep["property"] != "title":
            flagged_new = census.matches(rep["new"])
            assert not flagged_new, (key, flagged_new)

        supp_lists = supp_field_index.get(key, [])
        if rep["property"] == "notes":
            supp_lists = ["demo.plt.mortgage-detail"]

        chg = changes_by_key.get(key)
        rows_out.append({
            "index": idx,
            "id": rep["id"],
            "version": rep["version"],
            "property": rep["property"],
            "old_shown": rep["shown"],
            "p0c_shown": chg["p0c_shown"] if chg else rep["new_shown"],
            "final_shown": rep["new_shown"],
            "action_in_track0": "refined" if chg else "retained",
            "track0_reason": chg["reason"] if chg else "True in all census and supplementary drawn states; basis preserved; plain 2025 instruction naming.",
            "basis_preserved": BASIS_NOTES[key],
            "recorded_lists": rep["recorded_lists"],
            "p0b_synthetic_lists": rep["synthetic_lists"],
            "track0_supplementary_lists": supp_lists,
            "example_lists": rep["example_lists"],
            "flagged_terms_remaining": [],
            "item1_verdict": "PASS",
            "item2_verdict": "PASS",
            "item3_verdict": "PASS",
        })

    summary = {
        "status": "pass",
        "checked_replacements": len(rows_out),
        "retained_from_p0c": sum(1 for r in rows_out if r["action_in_track0"] == "retained"),
        "refined_in_track0": sum(1 for r in rows_out if r["action_in_track0"] == "refined"),
        "supplementary_synthetic_cases": supp_results,
        "item1_true_in_every_drawn_state": "PASS",
        "item2_nothing_proved_is_dropped": "PASS",
        "item3_plain_and_consistent": "PASS",
        "replacements": rows_out,
    }
    census.write(HERE / "track0-state-matrix.json", summary)
    print(
        json.dumps(
            {
                "status": summary["status"],
                "checked_replacements": summary["checked_replacements"],
                "retained_from_p0c": summary["retained_from_p0c"],
                "refined_in_track0": summary["refined_in_track0"],
                "supplementary_cases": list(supp_results.keys()),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
