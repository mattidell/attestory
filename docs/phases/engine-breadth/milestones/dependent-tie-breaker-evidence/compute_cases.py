"""P0 case table: hand-computed results for the plan's tie-breaker cases.

Reproduces all figures directly from parameters on main:
- packages/content/tax/2025/parameter.ctc-2025.json
- packages/content/tax/2025/parameter.eic-2025.json

Includes:
- Cases 1a, 1b, 1c, 1d (Parent vs Non-Parent, including equal AGI loss under § 152(c)(4)(C))
- Case 2 (Unmarried parents living together, higher AGI wins)
- Cases 3a, 3b, 3c (Two parents living apart: unequal nights, equal nights with higher AGI, and equal nights with equal AGI outside class)
- Cases 4a, 4b (Outside class: Form 8332 and multiple competing claimants)
- Cases 5a, 5b (Succession: v57 return answering 'no' vs unmigrated answers)
- Case 6 (Cross-credit independence: failure of EIC residency does not bar CTC)

Run from any directory:
    python3 docs/phases/engine-breadth/milestones/dependent-tie-breaker-evidence/compute_cases.py
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Optional

REPO = Path(__file__).resolve().parents[5]

# Load official parameters from main
with open(REPO / "packages/content/tax/2025/parameter.ctc-2025.json", encoding="utf-8") as f:
    CTC_PARAMS = json.load(f)["values"]

with open(REPO / "packages/content/tax/2025/parameter.eic-2025.json", encoding="utf-8") as f:
    EIC_PARAMS = json.load(f)["values"]

CTC_PER_CHILD = int(CTC_PARAMS["credit_per_child"])  # $2,200
ODC_PER_DEP = int(CTC_PARAMS["other_dependent_credit"])  # $500
THRESHOLD = {
    "single": int(CTC_PARAMS["phaseout_single"]),  # $200,000
    "joint": int(CTC_PARAMS["phaseout_joint"]),    # $400,000
}


def half_up(val: Decimal) -> int:
    return int(val.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def compute_ctc(qualifying_children: int, odc_dependents: int, agi: int, tax: int, filing_status: str = "single") -> dict[str, int]:
    l5 = CTC_PER_CHILD * qualifying_children
    l7 = ODC_PER_DEP * odc_dependents
    l8 = l5 + l7
    thresh = THRESHOLD.get(filing_status, THRESHOLD["single"])
    excess = max(0, agi - thresh)
    if excess > 0 and excess % 1000:
        excess = (excess // 1000 + 1) * 1000
    l10 = excess
    l11 = half_up(Decimal(l10) * Decimal("0.05"))
    l12 = max(0, l8 - l11)
    l19 = min(l12, tax)
    return {"l4": qualifying_children, "l5": l5, "l7": l7, "l8": l8, "l12": l12, "l19": l19}


def compute_eic(qualifying_children: int, earned_income: int, agi: int, filing_status: str = "single") -> int:
    kids = min(3, qualifying_children)
    prefix = "mfj" if filing_status == "joint" else "other"
    earned_limit = Decimal(EIC_PARAMS[f"{prefix}.{kids}.earned_income_amount"])
    max_credit = Decimal(EIC_PARAMS[f"{prefix}.{kids}.maximum"])
    phaseout_thresh = Decimal(EIC_PARAMS[f"{prefix}.{kids}.phaseout_threshold"])
    credit_rate = Decimal(EIC_PARAMS[f"{prefix}.{kids}.credit_rate"])
    phaseout_rate = Decimal(EIC_PARAMS[f"{prefix}.{kids}.phaseout_rate"])

    tentative = half_up(min(Decimal(earned_income), earned_limit) * credit_rate)
    tentative = min(int(max_credit), tentative)

    excess_income = max(Decimal(0), max(Decimal(earned_income), Decimal(agi)) - phaseout_thresh)
    phaseout = half_up(excess_income * phaseout_rate)
    return max(0, tentative - phaseout)


@dataclass(frozen=True)
class TieBreakerCase:
    case_id: str
    description: str
    filing_status: str
    earned_income: int
    agi: int
    tax: int
    dtb_winner: str
    eic_children: int
    ctc_children: int
    odc_children: int
    outside_class: bool = False
    disposition_note: str = ""


CASES = (
    TieBreakerCase(
        case_id="1a",
        description="Parent (filer) + grandparent; parent claims (parent wins categorically under § 152(c)(4)(A)(i))",
        filing_status="single",
        earned_income=30_000,
        agi=30_000,
        tax=1_500,
        dtb_winner="taxpayer",
        eic_children=1,
        ctc_children=1,
        odc_children=0,
        disposition_note="Filer parent wins over non-parent",
    ),
    TieBreakerCase(
        case_id="1b",
        description="Grandparent (filer) + parent; parent does not claim, grandparent AGI ($35k) > parent ($25k)",
        filing_status="single",
        earned_income=35_000,
        agi=35_000,
        tax=2_000,
        dtb_winner="taxpayer",
        eic_children=1,
        ctc_children=1,
        odc_children=0,
        disposition_note="Non-parent filer wins under § 152(c)(4)(C)",
    ),
    TieBreakerCase(
        case_id="1c",
        description="Grandparent (filer) + parent; parent does not claim, grandparent AGI ($20k) < parent ($25k)",
        filing_status="single",
        earned_income=20_000,
        agi=20_000,
        tax=500,
        dtb_winner="other",
        eic_children=0,
        ctc_children=0,
        odc_children=0,
        disposition_note="Non-parent filer loses under § 152(c)(4)(C); receives childless EIC only",
    ),
    TieBreakerCase(
        case_id="1d",
        description="Grandparent (filer) + parent; parent does not claim, grandparent AGI ($25k) == parent ($25k)",
        filing_status="single",
        earned_income=25_000,
        agi=25_000,
        tax=800,
        dtb_winner="other",
        eic_children=0,
        ctc_children=0,
        odc_children=0,
        disposition_note="Statute requires strictly higher AGI (§ 152(c)(4)(C)); equal AGI is explicit loss",
    ),
    TieBreakerCase(
        case_id="2",
        description="Two unmarried parents living together; filer lower AGI ($12k vs $14k); filer loses",
        filing_status="single",
        earned_income=12_000,
        agi=12_000,
        tax=0,
        dtb_winner="other",
        eic_children=0,
        ctc_children=0,
        odc_children=0,
        disposition_note="Higher AGI parent wins (§ 152(c)(4)(B)(ii)); filer receives 0 for all 3 child credits",
    ),
    TieBreakerCase(
        case_id="3a",
        description="Two parents living apart; child lived with filer for more nights (200 vs 165)",
        filing_status="single",
        earned_income=28_000,
        agi=28_000,
        tax=1_200,
        dtb_winner="taxpayer",
        eic_children=1,
        ctc_children=1,
        odc_children=0,
        disposition_note="Filer wins under longer residence test (§ 152(c)(4)(B)(i))",
    ),
    TieBreakerCase(
        case_id="3b",
        description="Two parents living apart; equal nights; filer higher AGI ($40k vs $35k)",
        filing_status="single",
        earned_income=40_000,
        agi=40_000,
        tax=2_500,
        dtb_winner="taxpayer",
        eic_children=1,
        ctc_children=1,
        odc_children=0,
        disposition_note="Equal nights; filer wins under higher AGI test (§ 152(c)(4)(B)(ii))",
    ),
    TieBreakerCase(
        case_id="3c",
        description="Two parents living apart; equal nights; equal AGI ($35k vs $35k)",
        filing_status="single",
        earned_income=35_000,
        agi=35_000,
        tax=2_000,
        dtb_winner="outside_class",
        eic_children=0,
        ctc_children=0,
        odc_children=0,
        outside_class=True,
        disposition_note="Sources silent on tie; blocks as outside class by answer",
    ),
    TieBreakerCase(
        case_id="4a",
        description="Divorced custodial parent releasing claim via Form 8332",
        filing_status="single",
        earned_income=25_000,
        agi=25_000,
        tax=1_000,
        dtb_winner="outside_class",
        eic_children=0,
        ctc_children=0,
        odc_children=0,
        outside_class=True,
        disposition_note="Blocks as outside class by answer (form-8332-released == yes)",
    ),
    TieBreakerCase(
        case_id="4b",
        description="Child living with filer, other parent, and grandparent (>1 other claimant)",
        filing_status="single",
        earned_income=25_000,
        agi=25_000,
        tax=1_000,
        dtb_winner="outside_class",
        eic_children=0,
        ctc_children=0,
        odc_children=0,
        outside_class=True,
        disposition_note="Blocks as outside class by answer (multiple-other-claimants == yes)",
    ),
    TieBreakerCase(
        case_id="5a",
        description="Succession: v57 return answering 'no' to another-may-claim",
        filing_status="single",
        earned_income=32_000,
        agi=32_000,
        tax=1_700,
        dtb_winner="taxpayer",
        eic_children=1,
        ctc_children=1,
        odc_children=0,
        disposition_note="another-could-claim == no; clears immediately, 0 subordinate questions asked",
    ),
    TieBreakerCase(
        case_id="5b",
        description="Succession: return with another-could-claim == yes, subordinate questions omitted",
        filing_status="single",
        earned_income=32_000,
        agi=32_000,
        tax=1_700,
        dtb_winner="blocked",
        eic_children=0,
        ctc_children=0,
        odc_children=0,
        outside_class=True,
        disposition_note="Blocks on DEPENDENCY_ABSENT naming missing tie-breaker facts",
    ),
    TieBreakerCase(
        case_id="6",
        description="Separate credit boundaries: child living outside US all year (US citizen child)",
        filing_status="single",
        earned_income=35_000,
        agi=35_000,
        tax=2_000,
        dtb_winner="taxpayer",
        eic_children=0,
        ctc_children=1,
        odc_children=0,
        disposition_note="Fails EIC residency (0 EIC child); passes CTC tests & tie-breaker (1 CTC child)",
    ),
)


def main() -> None:
    print("| Case | Description | Winner | EIC Kids | CTC Kids | EIC Credit | CTC (Sch 8812 L19) | Total Benefits | Disposition Note |")
    print("| :---: | :--- | :---: | :---: | :---: | ---: | ---: | ---: | :--- |")
    for c in CASES:
        if c.outside_class:
            print(f"| {c.case_id} | {c.description} | **{c.dtb_winner}** | - | - | - | - | - | {c.disposition_note} |")
            continue
        ctc = compute_ctc(c.ctc_children, c.odc_children, c.agi, c.tax, c.filing_status)
        eic = compute_eic(c.eic_children, c.earned_income, c.agi, c.filing_status)
        tot = eic + ctc["l19"]
        print(f"| {c.case_id} | {c.description} | **{c.dtb_winner}** | {c.eic_children} | {c.ctc_children} | ${eic:,} | ${ctc['l19']:,} | ${tot:,} | {c.disposition_note} |")


if __name__ == "__main__":
    main()
