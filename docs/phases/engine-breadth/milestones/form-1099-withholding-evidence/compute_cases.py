"""Reproduces the coordinator and tax-table figures for the plan cases in Section 8.

Calculates Form 1040 line 24 (total tax), line 25a (W-2 withholding),
line 25b (Form 1099 withholding), line 25d (total withholding),
line 33 (total payments), line 35a (refund), and line 37 (amount owed)
under the 2025 IRS Tax Table (governing coordinator calculation via $50 bracket midpoints)
and notes the continuous rate schedule equivalents.

Run from repository root:
    python3 docs/phases/engine-breadth/milestones/form-1099-withholding-evidence/compute_cases.py
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

_BRACKETS_SINGLE_2025 = [
    (Decimal(0), Decimal("11925"), Decimal("0.10")),
    (Decimal("11925"), Decimal("48475"), Decimal("0.12")),
    (Decimal("48475"), Decimal("103350"), Decimal("0.22")),
    (Decimal("103350"), Decimal("197300"), Decimal("0.24")),
    (Decimal("197300"), Decimal("250525"), Decimal("0.32")),
    (Decimal("250525"), Decimal("626350"), Decimal("0.35")),
    (Decimal("626350"), None, Decimal("0.37")),
]

_BRACKETS_MFJ_2025 = [
    (Decimal(0), Decimal("23850"), Decimal("0.10")),
    (Decimal("23850"), Decimal("96950"), Decimal("0.12")),
    (Decimal("96950"), Decimal("206700"), Decimal("0.22")),
    (Decimal("206700"), Decimal("394600"), Decimal("0.24")),
    (Decimal("394600"), Decimal("501050"), Decimal("0.32")),
    (Decimal("501050"), Decimal("751600"), Decimal("0.35")),
    (Decimal("751600"), None, Decimal("0.37")),
]

STD_DEDUCTION_SINGLE = Decimal("15750")
STD_DEDUCTION_MFJ = Decimal("31500")


def round_dollar(val: Decimal) -> Decimal:
    return val.quantize(Decimal("1"), rounding=ROUND_HALF_UP)


def tax_single_continuous(taxable_income: Decimal) -> Decimal:
    if taxable_income <= 0:
        return Decimal("0")
    total = Decimal("0")
    for lower, upper, rate in _BRACKETS_SINGLE_2025:
        if taxable_income <= lower:
            continue
        top = taxable_income if upper is None else min(taxable_income, upper)
        total += (top - lower) * rate
    return round_dollar(total)


def tax_mfj_continuous(taxable_income: Decimal) -> Decimal:
    if taxable_income <= 0:
        return Decimal("0")
    total = Decimal("0")
    for lower, upper, rate in _BRACKETS_MFJ_2025:
        if taxable_income <= lower:
            continue
        top = taxable_income if upper is None else min(taxable_income, upper)
        total += (top - lower) * rate
    return round_dollar(total)


def tax_table_midpoint(taxable_income: Decimal) -> Decimal:
    """IRS Tax Table rule below $100,000: tax is figured on the $50 band midpoint."""
    if taxable_income < Decimal("100000"):
        band_start = (taxable_income // Decimal("50")) * Decimal("50")
        return band_start + Decimal("25")
    return taxable_income


def tax_single_coordinator(taxable_income: Decimal) -> Decimal:
    """Governing coordinator calculation matching rule.form1040-line16 and rule.form1040-line24."""
    midpoint = tax_table_midpoint(taxable_income)
    return tax_single_continuous(midpoint)


def tax_mfj_coordinator(taxable_income: Decimal) -> Decimal:
    """Governing coordinator calculation for MFJ."""
    midpoint = tax_table_midpoint(taxable_income)
    return tax_mfj_continuous(midpoint)


def evaluate_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []

    # Case 1: Unemployment with 10% withheld
    # Wages $50,000, W-2 box 2 $4,500. 1099-G box 1 $6,000, box 4 $600 (10%).
    # Taxable income = $40,250.
    # Coordinator (Tax Table midpoint $40,275): tax = $4,595. Payments = $5,100 ($4,500 + $600).
    # Refund = $505 (continuous schedule: tax $4,592, refund $508).
    wages1 = Decimal("50000")
    u1 = Decimal("6000")
    ti1 = wages1 + u1 - STD_DEDUCTION_SINGLE  # 40,250
    t1 = tax_single_coordinator(ti1)  # 4,595
    t1_cont = tax_single_continuous(ti1)  # 4,592
    w2_1 = Decimal("4500")
    g_b4_1 = Decimal("600")
    line25b_1 = g_b4_1
    line25d_1 = w2_1 + line25b_1  # 5,100
    line33_1 = line25d_1
    ref1 = max(Decimal("0"), line33_1 - t1)  # 505
    owed1 = max(Decimal("0"), t1 - line33_1)  # 0
    cases.append({
        "case": "Case 1",
        "description": "Unemployment with 10% withheld ($600 on $6,000 UI)",
        "line15_taxable_income": str(ti1),
        "line24_tax": str(t1),
        "line24_tax_continuous": str(t1_cont),
        "line25a": str(w2_1),
        "line25b": str(line25b_1),
        "line25d": str(line25d_1),
        "line33_payments": str(line33_1),
        "line35a_refund": str(ref1),
        "line37_owed": str(owed1),
        "notes": "Line 25b includes $600; bottom line moves by +$600 (from -$95 owed on v58 to +$505 refund)",
    })

    # Case 2A: Social Security with voluntary withholding in box 6 alone
    # Wages $40,000, W-2 box 2 $2,500. SSA-1099 box 5 $12,000 (taxable SS $8,700), box 6 $800.
    # Taxable income = $32,950.
    # Coordinator (Tax Table midpoint $32,975): tax = $3,719 (continuous: $3,716).
    wages2a = Decimal("40000")
    ss_taxable2a = Decimal("8700")
    ti2a = wages2a + ss_taxable2a - STD_DEDUCTION_SINGLE  # 32,950
    t2a = tax_single_coordinator(ti2a)  # 3,719
    t2a_cont = tax_single_continuous(ti2a)  # 3,716
    w2_2a = Decimal("2500")
    ssa_b6_2a = Decimal("800")
    line25b_2a = ssa_b6_2a  # 800
    line25d_2a = w2_2a + line25b_2a  # 3,300
    line33_2a = line25d_2a
    ref2a = max(Decimal("0"), line33_2a - t2a)  # 0
    owed2a = max(Decimal("0"), t2a - line33_2a)  # 419 (continuous: 416)
    cases.append({
        "case": "Case 2A",
        "description": "SSA-1099 box 6 voluntary withholding alone ($800)",
        "line15_taxable_income": str(ti2a),
        "line24_tax": str(t2a),
        "line24_tax_continuous": str(t2a_cont),
        "line25a": str(w2_2a),
        "line25b": str(line25b_2a),
        "line25d": str(line25d_2a),
        "line33_payments": str(line33_2a),
        "line35a_refund": str(ref2a),
        "line37_owed": str(owed2a),
        "notes": "SSA voluntary withholding credited to 25b, reducing amount owed from $1,219 to $419",
    })

    # Case 2B: SSA-1099 box 6 with 1099-R box 4 on same return
    # Same as 2A plus Form 1099-R gross distribution $10,000, box 4 withholding $1,200.
    # The additional $10,000 distribution is fully taxable income in the 12% bracket.
    # Taxable income rises from $32,950 to $42,950 (+ $10,000).
    # Tax rises by exactly 12% of $10,000 = $1,200 (from $3,719 to $4,919).
    # Withholding also rises by $1,200 (from $3,300 to $4,500), keeping net amount owed at $419.
    r_income = Decimal("10000")
    r_b4 = Decimal("1200")
    ti2b = ti2a + r_income  # 42,950
    t2b = tax_single_coordinator(ti2b)  # 4,919
    t2b_cont = tax_single_continuous(ti2b)  # 4,916
    line25b_2b = ssa_b6_2a + r_b4  # 800 + 1,200 = 2,000
    line25d_2b = w2_2a + line25b_2b  # 2,500 + 2,000 = 4,500
    line33_2b = line25d_2b
    ref2b = max(Decimal("0"), line33_2b - t2b)  # 0
    owed2b = max(Decimal("0"), t2b - line33_2b)  # 419 (continuous: 416)
    cases.append({
        "case": "Case 2B",
        "description": "SSA-1099 box 6 ($800) + 1099-R gross $10k with box 4 ($1,200)",
        "line15_taxable_income": str(ti2b),
        "line24_tax": str(t2b),
        "line24_tax_continuous": str(t2b_cont),
        "line25a": str(w2_2a),
        "line25b": str(line25b_2b),
        "line25d": str(line25d_2b),
        "line33_payments": str(line33_2b),
        "line35a_refund": str(ref2b),
        "line37_owed": str(owed2b),
        "notes": "1099-R gross adds $10,000 taxable income (12% tax = +$1,200); withholding also +$1,200; owed stays $419",
    })

    # Case 3: Form 1099-K with backup withholding in box 4
    cases.append({
        "case": "Case 3",
        "description": "Form 1099-K with backup withholding in box 4",
        "line15_taxable_income": "Refused",
        "line24_tax": "Refused",
        "line24_tax_continuous": "Refused",
        "line25a": "Refused",
        "line25b": "Refused",
        "line25d": "Refused",
        "line33_payments": "Refused",
        "line35a_refund": "Refused",
        "line37_owed": "Refused",
        "notes": "SC-R1 obstacle prevents member family; nonzero box 4 refused outside class (DEPENDENCY_ABSENT)",
    })

    # Case 4: Joint return with withholding on two 1099-Gs (taxpayer + spouse)
    # MFJ, standard deduction $31,500. Wages $80,000, W-2 box 2 $7,000.
    # Taxpayer 1099-G box 1 $5,000, box 4 $500. Spouse 1099-G box 1 $4,000, box 4 $400.
    # Taxable income = $57,500. Coordinator (Tax Table midpoint $57,525): tax = $6,426 (continuous: $6,423).
    # Withholding = $7,900. Refund = $1,474 (continuous: $1,477).
    wages4 = Decimal("80000")
    u4_tp = Decimal("5000")
    u4_sp = Decimal("4000")
    ti4 = wages4 + u4_tp + u4_sp - STD_DEDUCTION_MFJ  # 57,500
    t4 = tax_mfj_coordinator(ti4)  # 6,426
    t4_cont = tax_mfj_continuous(ti4)  # 6,423
    w2_4 = Decimal("7000")
    line25b_4 = Decimal("500") + Decimal("400")  # 900
    line25d_4 = w2_4 + line25b_4  # 7,900
    line33_4 = line25d_4
    ref4 = max(Decimal("0"), line33_4 - t4)  # 1,474
    owed4 = max(Decimal("0"), t4 - line33_4)  # 0
    cases.append({
        "case": "Case 4",
        "description": "MFJ return with two 1099-Gs ($500 + $400 withholding)",
        "line15_taxable_income": str(ti4),
        "line24_tax": str(t4),
        "line24_tax_continuous": str(t4_cont),
        "line25a": str(w2_4),
        "line25b": str(line25b_4),
        "line25d": str(line25d_4),
        "line33_payments": str(line33_4),
        "line35a_refund": str(ref4),
        "line37_owed": str(owed4),
        "notes": "1099-G subtotal sums both statements (500 + 400 = 900) across spouses into line 25b",
    })

    # Case 5A: v58 answer set without withholding on v59
    # Wages $50,000, W-2 box 2 $4,500. No 1099 withholding.
    # Taxable income = $34,250.
    # Coordinator (Tax Table midpoint $34,275): tax = $3,875 (continuous: $3,872).
    # Refund = $625 (continuous: $628).
    wages5a = Decimal("50000")
    ti5a = wages5a - STD_DEDUCTION_SINGLE  # 34,250
    t5a = tax_single_coordinator(ti5a)  # 3,875
    t5a_cont = tax_single_continuous(ti5a)  # 3,872
    w2_5a = Decimal("4500")
    line25b_5a = Decimal("0")
    line25d_5a = w2_5a + line25b_5a  # 4,500
    line33_5a = line25d_5a
    ref5a = max(Decimal("0"), line33_5a - t5a)  # 625
    owed5a = max(Decimal("0"), t5a - line33_5a)  # 0
    cases.append({
        "case": "Case 5A",
        "description": "v58-shaped answer set (zero 1099 withholding) on v59",
        "line15_taxable_income": str(ti5a),
        "line24_tax": str(t5a),
        "line24_tax_continuous": str(t5a_cont),
        "line25a": str(w2_5a),
        "line25b": str(line25b_5a),
        "line25d": str(line25d_5a),
        "line33_payments": str(line33_5a),
        "line35a_refund": str(ref5a),
        "line37_owed": str(owed5a),
        "notes": "Closed-empty families publish 0; exact preservation of v58 coordinator result ($3,875 tax, $625 refund)",
    })

    # Case 5B: Nonzero 1099-G box 4 transitions from refused to computed
    # Same income as Case 1 ($50k wages + $6k UI, $600 box 4).
    # On v58: refused by tax.us.2025.f1099g.box4-federal-withholding-authority.
    # On v59: computes line 25b = $600, refund = $505 (continuous: $508).
    cases.append({
        "case": "Case 5B",
        "description": "Nonzero 1099-G box 4 ($600) transition (v58 -> v59)",
        "line15_taxable_income": str(ti1),
        "line24_tax": str(t1),
        "line24_tax_continuous": str(t1_cont),
        "line25a": str(w2_1),
        "line25b": str(line25b_1),
        "line25d": str(line25d_1),
        "line33_payments": str(line33_1),
        "line35a_refund": str(ref1),
        "line37_owed": str(owed1),
        "notes": "Transitions from REFUSED on v58 to COMPUTED ($600) on v59; refund = $505",
    })

    # Case 6: Form 1099-INT recorded without box 4 answer
    # Wages $50,000, W-2 box 2 $4,500. Stmt 1: int $500, box 4 unanswered.
    # Stmt 2: int $300, box 4 $50. Total int $800.
    # Taxable income = $35,050.
    # Coordinator (Tax Table midpoint $35,075): tax = $3,971 (continuous: $3,968).
    # Withholding = $4,550 ($4,500 W-2 + $50 Line 25b). Refund = $579 (continuous: $582).
    wages6 = Decimal("50000")
    int6 = Decimal("800")
    ti6 = wages6 + int6 - STD_DEDUCTION_SINGLE  # 35,050
    t6 = tax_single_coordinator(ti6)  # 3,971
    t6_cont = tax_single_continuous(ti6)  # 3,968
    w2_6 = Decimal("4500")
    line25b_6 = Decimal("50")  # excludes unanswered statement, sums $50
    line25d_6 = w2_6 + line25b_6  # 4,550
    line33_6 = line25d_6
    ref6 = max(Decimal("0"), line33_6 - t6)  # 579
    owed6 = max(Decimal("0"), t6 - line33_6)  # 0
    cases.append({
        "case": "Case 6",
        "description": "Form 1099-INT with box 4 unanswered on one statement",
        "line15_taxable_income": str(ti6),
        "line24_tax": str(t6),
        "line24_tax_continuous": str(t6_cont),
        "line25a": str(w2_6),
        "line25b": str(line25b_6),
        "line25d": str(line25d_6),
        "line33_payments": str(line33_6),
        "line35a_refund": str(ref6),
        "line37_owed": str(owed6),
        "notes": "Unanswered statement excluded without error; subtotal sums $50; refund = $579",
    })

    return cases


def print_table(cases: list[dict[str, object]]) -> None:
    header = (
        f"{'Case':<8} | {'Description':<42} | {'Tax (24)':<8} | "
        f"{'25a':<6} | {'25b':<6} | {'25d':<6} | {'Paid (33)':<9} | "
        f"{'Refund (35a)':<12} | {'Owed (37)':<9}"
    )
    sep = "-" * len(header)
    print(header)
    print(sep)
    for c in cases:
        print(
            f"{str(c['case']):<8} | {str(c['description'])[:42]:<42} | "
            f"{str(c['line24_tax']):<8} | {str(c['line25a']):<6} | "
            f"{str(c['line25b']):<6} | {str(c['line25d']):<6} | "
            f"{str(c['line33_payments']):<9} | {str(c['line35a_refund']):<12} | "
            f"{str(c['line37_owed']):<9}"
        )
    print(sep)


if __name__ == "__main__":
    print("=== Section 8 Case Reproduction Figures (Coordinator Tax Table Midpoints) ===")
    cases = evaluate_cases()
    print_table(cases)
