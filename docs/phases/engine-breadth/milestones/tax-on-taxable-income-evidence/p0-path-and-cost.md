# P0 Increment B — the current path and the cost of change

Continues `p0-law-and-inventory.md`. Investigation only; no production,
content, schema, test, or golden edit. The probe script
(`probe.py`, in this directory) runs the real coordinator
(`live_coordinate_run`) against the adopted production package
(core-calculations v49) on five synthetic single-filer returns; its output
stays under `temp/tax-on-taxable-income/probe-output.json` (git-ignored).
Reproduce with:

```sh
python3 docs/phases/engine-breadth/milestones/tax-on-taxable-income-evidence/probe.py
```

## 1. What the traced rules compute today

- **`tax.us.2025.rule.form1040-line16` v5** publishes `tax.us.2025.tax.total-tax`.
  When there is no qualified-dividend or preferential amount, it is a plain
  `bracket_fold` of taxable income against `demo.parameter.tax-brackets.2025`.
  Otherwise it computes two numbers and takes the smaller, exactly matching
  the 2025 QDCG Worksheet's own lines 22-25 ("tax on all taxable income;
  enter the smaller"):
  1. `bracket_fold(ordinary brackets, taxable_income - qualified_total -
     selected_preferential_base)` + `bracket_fold(qdcg brackets, qualified_total
     + selected_preferential_base)`
  2. `bracket_fold(ordinary brackets, taxable_income)` alone (the "tax on all
     taxable income" comparison figure)

  The **mechanism** (bracket-fold-and-take-smaller) is sound and structurally
  matches the worksheet. The **defect is entirely in its two input
  parameters** (§2, §3 of the inventory) and in `selected-preferential-base`'s
  own amount (§2 below) — not in this rule's own arithmetic. Its note says
  "QDCG arithmetic unchanged since earlier versions," consistent with that
  reading.

  It never bands taxable income or looks anything up in a Tax-Table-shaped
  structure: every taxable-income level, including far below $100,000, goes
  through the same raw marginal `bracket_fold`. The 2025 instructions require
  the Tax Table below $100,000 (Increment A §2); this rule departs from that
  at every return below $100,000.

- **`tax.us.2025.rule.selected-preferential-base` v4** publishes
  `tax.us.2025.capital-gains.selected-preferential-base`. When any Schedule D
  trigger is present (covered ST/LT proceeds, loss carryovers, lines 1b/8b),
  its value is:

  ```
  max(tax.us.2025.schedule-d.line-16, 0)
  ```

  where `schedule-d.line-16 = schedule-d.line-7 (net short-term) +
  schedule-d.line-15 (net long-term)` (`rule.schedule-d-line16` v2). **This is
  the short-term defect**: the 2025 QDCG Worksheet line 3 says, verbatim,
  "Enter the smaller of line 15 or line 16 of Schedule D. If either line 15
  or line 16 is blank or a loss, enter -0-" (Increment A §2/the QDCG
  worksheet text). The rule uses line 16 (the short-term-plus-long-term
  total) directly, floored at zero, instead of `min(line-15, line-16)` with a
  zero floor when either is a loss. Any return where short-term gain makes
  line 16 larger than line 15 lets short-term gain into the preferential
  base.

- **`tax.us.2025.rule.form1040-standard-deduction` v1** adds the base amount
  (`demo.parameter.standard-deduction-base.2025`) to zero or more additions
  of `demo.parameter.additional-deduction-rate.2025` for age-65/blindness,
  taxpayer and spouse, reading `taxpayer_over_65`, `taxpayer_blind`,
  `spouse_over_65`, `spouse_blind`. The **mechanism already supports** married
  filers with a spouse's age/blindness addition and a dependent's limited
  standard deduction is a separate, unrelated worksheet this rule does not
  implement at all (there is no dependent-specific branch; it always applies
  the base-plus-additions formula). Both of its two parameters are wrong or
  partly wrong (Increment A §4-5); its own arithmetic is not.

## 2. The short-term defect: an exact synthetic case

Probe case 5: single filer, wages $90,000, one short-term sale (proceeds
$5,000, basis $0 → $5,000 short-term gain), one long-term sale (proceeds
$1,000, basis $0 → $1,000 long-term gain). No dividends.

- Schedule D line 7 (net short-term) = $5,000; line 15 (net long-term) =
  $1,000; line 16 = $6,000.
- **Today's engine**: `selected-preferential-base = max(6000, 0) = 6000` —
  all $6,000 (including the $5,000 short-term gain) treated as preferential.
- **2025 worksheet rule**: `min(line 15, line 16) = min(1000, 6000) = 1000`
  — only the $1,000 long-term gain is preferential; the $5,000 short-term
  gain is ordinary income.
- Taxable income (engine-computed) = $81,000.
- Isolating this one defect from the separate rate-schedule mismatch (using
  today's own, still-wrong, 3-bracket demo rates on both sides of the
  comparison so only the preferential-base selection differs):
  - Today's defective preferential base ($6,000): combined tax = **$12,453**
    (hand-computed, matches the live-coordinator run exactly).
  - Corrected preferential base ($1,000) per the 2025 worksheet: combined
    tax = **$12,803**.
  - **Delta from this defect alone: $350** (= the $5,000 wrongly-preferential
    short-term gain × the 7-point rate gap between today's 22% ordinary top
    bracket and the 15% flat preferential rate, at this income level).

This is a minimum, not a worst case: the gap scales with the short-term
amount and the marginal-rate gap at the taxpayer's bracket, and grows further
once the rate schedule and preferential bands are also corrected (Increment
A §1/§3), since the real top ordinary brackets (32/35/37%) are further from
15/20% than today's capped-at-22% demo schedule is.

## 3. The real path on synthetic returns ($50k / $150k / $600k / 0%-band)

All single filers, wages-only unless noted, via `probe.py`, reusing the SSA
worksheet / Form 1099-K / Schedule D coordinator seeding helpers already
committed under `tests/` (see the probe script's module docstring for the
exact helpers reused). Taxable income values are the engine's own Form 1040
line 15 output (wages minus today's — unverified — $15,000 standard
deduction); the wage inputs were chosen to land near each target.

| Case | Taxable income | Line 16 (engine, today) | Hand check |
| --- | --- | --- | --- |
| 1. ~$50k | $46,850 | **$5,390** | Below $100,000: the 2025 instructions require the Tax Table (banded $50 midpoints), not a raw marginal formula, so no single hand number is the "right" comparison here — see §4. Using today's own (wrong) 3-bracket schedule as a raw marginal formula, $5,390 is arithmetically consistent with that wrong schedule; it is not the 2025 Tax Table answer under either the wrong or the right rate schedule. |
| 2. ~$150k | $146,850 | **$27,360** | $100,000+: the Tax Computation Worksheet (exact formula, Increment A §2) applies directly. Hand, with the **verified 2025** rate schedule: $146,850 × 24% − $7,153 = **$28,091**. Engine is $731 low, entirely attributable to the wrong rate schedule (today's schedule caps at 22% with no 24/32/35/37% brackets at all). |
| 3. ~$600k | $596,850 | **$126,360** | Verified 2025 formula: $596,850 × 35% − $30,452.75 = **$178,445** (rounded). Engine is $52,085 low — the gap widens sharply above $100,000 because today's demo schedule has no bracket above 22%, exactly as the milestone plan anticipated ("badly wrong above about $100,000"). |
| 4. Qualified dividends in the 0% band | $10,000 (wages $20,000, qualified dividends $5,000, no Schedule D) | **$1,000** | Verified 2025 bands: at $10,000 taxable income the $48,350 single 0%-breakpoint is far above taxable income, so the entire $5,000 preferential amount is in the 0% band. Hand (verified bands, today's wrong ordinary schedule held constant to isolate this one mismatch): ordinary tax on $5,000 = $500; preferential tax = $0; total = **$500**. The engine's $1,000 equals the all-ordinary comparison figure (today's flat-15% preferential rate makes the split worse than no split at this income, so the rule's own "smaller of the two" logic reverts to all-ordinary) — coincidentally closer to correct than a flat 15% would have been, but still $500 high because there is no 0% band to select. |

(Case 5, the short-term defect, is reported in §2 above rather than this
table, since its interesting comparison is the preferential-base amount, not
the income level.)

## 4. Tax Table expressibility

**Verdict: yes, expressible exactly with the existing expression language —
no new operation is needed.**

The Tax Table is, by construction and independently re-verified here
(Increment A §2), "tax on the band midpoint, rounded to the nearest dollar,"
where the band is $25 wide below $3,000 and $50 wide from $3,000 up to
$100,000. Every primitive this needs already exists in
`packages/schemas/derivation/rule-artifact.v14.schema.json` /
`packages/derivation/evaluator.py`:

1. `divide(taxable_income, 50, rounding="down", min_decimal_places=0)` →
   `floor(taxable_income / 50)` for nonnegative income (`ROUND_DOWN` toward
   zero equals floor for positive numbers; confirmed in
   `packages/derivation/evaluator.py::_divide`).
2. `multiply(that, 50)` → the band's floor.
3. `add(that, 25)` → the band's midpoint.
4. `bracket_fold(ordinary-rate-table, filing_status, midpoint)` → the
   marginal tax on the midpoint (the same op already used for the ordinary
   bracket computation today).
5. `round(that, "half_up")` (the project's existing whole-dollar rounding
   convention, already used throughout `rule.form1040-line16`) → the
   published Tax Table entry.

Below $3,000 the same five steps apply with `25` in place of `50` and `12.5`
(or the nearest whole-dollar convention the existing `round` op already
applies) in place of `25`; a `choose` on `taxable_income < 3000` selects
which composition runs — an ordinary conditional, not a new primitive.

This was spot-checked against two real published table entries
(single-filer $46,800-$46,850 band, and $950-$975 band) in Increment A §2;
both match exactly. No `floor`, `mod`, or table-specific operation needs to
be added to the rule language; the existing `divide` + `multiply` + `add` +
`bracket_fold` + `round` operations compose exactly, and `range_lookup`
(already in the language) would also work as a direct literal-table lookup
if a committed lookup table were preferred to the composed formula — a
choice this investigation does not make.

## 5. Cost of change

Searched for the affected rule/parameter ids by exact string and for
committed saved presentation goldens carrying a `line-16` section.

- **11 test files** cite the affected ids
  (`rule.form1040-line16`, `rule.selected-preferential-base`,
  `demo.parameter.tax-brackets.2025`,
  `demo.parameter.qdcg-preferential-brackets.2025`) directly by name:
  `test_capital_gain_distributions_line7a_t2_coordinator.py`,
  `test_dsbs_t3_line16_coordinator.py`, `test_dsbs_t3_qdcg_declarations.py`,
  `test_dsbs_t4_dividend_live_integration.py`,
  `test_form1099div_box7_direct_ftc.py`, `test_live_authorization_wiring.py`,
  `test_schedule_d_covered_ltcg_8a_t2_coordinator.py`,
  `test_schedule_d_current_year_losses_t1.py`,
  `test_schedule_d_form8949_covered_wash_sale_t1.py`,
  `test_schedule_d_inbound_loss_carryovers_t1.py`,
  `test_ssa1099_benefits_line6_track2.py`. These cover the Schedule D
  current-year-loss, wash-sale, inbound-carryover, covered-LTCG, direct-FTC,
  capital-gain-distributions, DSBS line-16/QDCG, and SSA-benefits routes.
  No test among these was found hard-coding a 2025-law-correct value today
  (expected, since no 2025-law-correct content exists yet); several hard-code
  specific numeric Form 1040 line-16 amounts computed under today's wrong
  parameters, which is exactly what a successor-content change must revisit.
- **20 committed saved presentation-model goldens** under
  `packages/sample_data/**/presentation/*.json` structurally include a
  `"id": "line-16"` section. **9 of the 20 currently publish a nonzero
  value** (`schedule_d_covered_ltcg_8a_t2` × 3,
  `form1099div_box7_direct_ftc` × 1, `capital_gain_distributions_line7a_t3`
  × 1, `market_discount_interest` × 1, `k1_interest_breadth` × 2,
  `form1099g_box1_schedule1_line7` × 1); every one of these 9 would need
  re-verification against the corrected parameters, since each was computed
  through `rule.form1040-line16` v5 using today's wrong rate schedule and/or
  preferential brackets. The other 11 are `blocked`/`None` today; whether a
  standard-deduction or bracket change flips any of those to a published
  value was not checked here (Track-level work, not P0).
- **78 test files** call `live_coordinate_run` at all (a broad upper bound on
  "could reach line 16"); the 11 and 9 figures above are the subset
  confirmed by this investigation to name the affected ids or carry an
  affected published value. A full per-test audit of every hard-coded
  expected number that depends on today's wrong parameters is Track 1/2
  work; P0 establishes the order of magnitude (dozens of files, a handful of
  committed goldens) and the two concrete, verified anchors above, not an
  exhaustive list.
- No test in the searched set was found hard-coding a *2025-law-correct*
  demo value that this round would need to leave alone — every numeric
  dependency found traces back to one of the four mismatched parameters in
  Increment A, or to the short-term defect, or to both.

## Owner-visible choices this investigation surfaces (none decided here)

1. **Tax Table representation**: a composed five-op expression (§4) versus a
   large committed literal lookup table via `range_lookup` (thousands of
   rows across five filing statuses) — both are expressible today; no new
   expression operation is required either way. This is a successor-content
   design choice, not an engine-capability gap.
2. **The married additional standard-deduction figure** ($1,550 → $1,600) is
   a correction independent of the Pub. L. 119-21 standard-deduction change
   and independent of the rate-schedule/preferential-band work; it could be
   fixed in this round or treated as its own minimal successor.
3. **The capital-loss limit** (Increment A §6) is recorded as verified
   against general tax-law knowledge, not against a freshly downloaded 2025
   primary source; a reviewer should confirm it against the 2025 Schedule D
   instructions or 26 U.S.C. §1211(b) text before treating it as closed.
