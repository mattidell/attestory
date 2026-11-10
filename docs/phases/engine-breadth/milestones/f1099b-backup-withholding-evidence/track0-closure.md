# Track 0 Adversarial Closure: Form 1099-B Backup Withholding (Tax Year 2025)

Evidence for `docs/phases/engine-breadth/milestones/f1099b-backup-withholding.md`.
Charter: `docs/reviews/f1099b-backup-withholding/charter-track0.md`.
Gate: `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate".

Every claim cited below is produced by real coordinator runs (`live_coordinate_run`) and saved in committed JSON output files:
- `track0-output.json` (Scopes 0, 1, 2, 3, 4, 5, 7)
- `track0-rerun-output.json` (Scope 6, 213 returns from `expected.json`)

All summary fields are computed directly from run results, never typed as strings.

---

## 0. Redo of P0 Gaps (Scope 0)

All 21 probe cases were executed through real coordinator runs on core v82 and scratch core v83 (`decided`). Every case on v83 matches hand values computed from the IRS instructions (`matches_hand=True`).

| Case ID | Description | v82 Disposition | v83 Disposition | Lines 25b / 33 / 34 / 37 | Matches Hand |
| --- | --- | --- | --- | --- | --- |
| `b4_one_statement` | 1 statement covered ST ($1,000 gain), box 4 $240 | blocked | published_value | 240 / 4,740 / 745 / 0 | True |
| `b4_two_statements` | 2 statements covered ST ($1,500 total gain), box 4 $240 + $100 | blocked | published_value | 340 / 4,840 / 845 / 0 | True |
| `b4_st_and_lt` | 1 statement with both ST ($1,000) and LT ($1,000) sales, box 4 $300 | blocked | published_value | 300 / 4,800 / 925 / 0 | True |
| `b4_beside_int_div` | 1099-B ($200) beside 1099-INT ($50) and 1099-DIV ($75); total b4 $325 | blocked | published_value | 325 / 4,825 / 770 / 0 | True |
| `b4_statement_removed` | Sales removed, leaving orphan statement with $200 b4 amount; the $200 is added | computed_zero | published_value | 200 / 4,700 / 825 / 0 | True |
| `b4_amount_no_answer` | 1 statement covered ST, box 4 unanswered on both cores | blocked | blocked | None / None / None / None | True |
| `b4_answer_no_amount` | 1 statement covered ST, v82 'no', amount $0 on v83 | computed_zero | computed_zero | 0 / 4,500 / 505 / 0 | True |
| `b4_no_with_amount` | 1 statement covered ST, box 4 amount $0 | computed_zero | computed_zero | 0 / 4,500 / 505 / 0 | True |
| `b4_no_one_statement` | Standard covered ST, box 4 amount $0 | computed_zero | computed_zero | 0 / 4,500 / 505 / 0 | True |
| `b4_yes_covered` | Covered ST sale, box 4 yes on v82 (blocked); box 4 $240 on v83 | blocked | published_value | 240 / 4,740 / 745 / 0 | True |
| `b4_yes_w` | Covered-W ST sale, box 4 yes on v82 (blocked); box 4 $240 on v83 | blocked | published_value | 240 / 4,740 / 745 / 0 | True |
| `b4_yes_noncovered` | Noncovered ST sale, box 4 yes on v82 (blocked); box 4 $240 on v83 | blocked | published_value | 240 / 4,740 / 745 / 0 | True |
| `b4_yes_codeb` | Code B ST sale, box 4 yes on v82 (blocked); box 4 $240 on v83 | blocked | published_value | 240 / 4,740 / 745 / 0 | True |
| `b4_two_statements_one_yes` | 2 statements: s1 box 4 $240, s2 box 4 $0; withholding $240 | blocked | published_value | 240 / 4,740 / 745 / 0 | True |
| `b4_two_statements_both_yes` | 2 statements both box 4 yes on v82; amounts $240 + $100 on v83 | blocked | published_value | 340 / 4,840 / 845 / 0 | True |
| `b4_two_statements_both_no` | 2 statements both box 4 no on v82; amounts $0 on v83 | computed_zero | computed_zero | 0 / 4,500 / 505 / 0 | True |
| `b4_two_statements_one_unanswered` | 2 statements: s1 answered $0, s2 unanswered (blocked) | blocked | blocked | None / None / None / None | True |
| `b4_extra_statement_no_sales` | 1 statement with sale ($0 b4), 1 extra statement no sales ($0 b4) | computed_zero | computed_zero | 0 / 4,500 / 505 / 0 | True |
| `b4_no_sales` | 0 sales recorded, zero withholding; standard return computes and is asked nothing new | computed_zero | computed_zero | 0 / 4,500 / 625 / 0 | True |
| `b4_orphan_150` | No sale. Box 4 $150 on one statement is added | computed_zero | published_value | 150 / 4,650 / 775 / 0 | True |
| `b4_orphan_beside_sale` | Kept covered short-term sale, gain $1,000, its box 4 $0, plus an orphan statement at $150 | blocked | published_value | 150 / 4,650 / 655 / 0 | True |

Summary: 21/21 cases match hand values. The named missing case ids from P0 now exist in committed JSON output. A return with no Form 1099-B and no box 4 amount still publishes line 25b as computed zero and is asked nothing new. An amount whose statement has no sale is added on that same arm.

---

## 1. Decision 2 Evaluation (Scope 1)

**Result: FAIL for content-only repair `bridge_v82_no`; Decision 2 is confirmed.**

A content-only repair `bridge_v82_no` was implemented in `prototype.py` as an active switch in `REPAIRS`. It replaced the single `require_paired` node in rule 25b v7 with an `any` expression containing:
1. `require_paired(key=statement, withholding=statement-box4-withholding, income=...)`
2. `all` with `require_paired(key=statement, withholding=statement-box4-withholding-reported, income=...)` and `collect_categorical_all_equal("no")`.

Four cases were evaluated on `repair_d2` (v83 + `bridge_v82_no`) and `decided` (v83 without `bridge_v82_no`):

| Case ID | Description | repair_d2 25b | decided 25b | Repair Succeeded? |
| --- | --- | --- | --- | --- |
| `d2_single_v82_no` | 1 statement covered ST; v82 box 4 'no' recorded, no amount | blocked | blocked | False |
| `d2_two_statements_both_v82_no` | 2 statements with sales; both v82 'no' recorded, no amount | blocked | blocked | False |
| `d2_mixed_statements` | 2 statements: s1 has amount $240; s2 has legacy v82 'no' | blocked | blocked | False |
| `d2_unanswered_statement` | 1 statement with sale; neither answered (unanswered) | blocked | blocked | False |

### Failure Mechanism
The repair fails for two fundamental engine semantics:
1. **Eager Evaluation in `evaluator.py`:** Evaluator operations (`any`, `all`, `choose`) do not catch `EvalBlocked`. In `_require_paired`, when any income key is not covered by the single `withholding` fact type, it immediately raises `EvalBlocked(BLOCK_ABSENT, [withholding])`. When the first arm of `any` evaluates `statement-box4-withholding`, it raises `EvalBlocked` immediately before the fallback arm can execute.
2. **Mixed Statement Impossibility:** For mixed returns (e.g. `d2_mixed_statements`), neither arm alone covers all statements, so both arms raise `EvalBlocked`.
3. **Empty amount set:** The decided subtotal does not collect `statement-box4-withholding` when no row is recorded. A v82 return therefore is not blocked on closing `f1099b.b4`. The bridge still fails for the reason in item 1.

**Conclusion:** Content alone cannot let a recorded v82 "no" close its statement at $0. Workspaces upgrading from v82 that recorded Form 1099-B sales must be asked the numeric amount question `statement-box4-withholding`.

---

## 2. Artifact 1: Authority-Lifecycle Table (Scope 2)

**PASS.** Cites exact cases that would fail if any row were wrong.

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| `f1099b.statement-box4-withholding` | Federal income tax withheld in box 4 of one Form 1099-B statement | One Form 1099-B statement (`statement` key and `tax-year`) | The filer's assertion of that statement's box 4 amount | Free supersession: `alc_b4_amount_superseded` replaces $100 with $250. Missing amount blocks line 25b: `alc_b4_amount_missing`. Valid amount computes: `alc_b4_amount_valid` ($150). |
| `f1099b.statement-box4-withholding-reported` | Legacy v82 yes/no answer for statement box 4 | One Form 1099-B statement | The filer's answer under v82 vocabulary | Retired on v83. On v82, "no" allowed line 25b to compute $0 (`alc_v82_answer_on_v82`). On scratch v83, the legacy answer is ignored by line 25b and blocks until numeric amount is provided (`alc_v82_answer_on_v83`). |
| The eight Form 1099-B sale counts `f1099b.{covered,covered-w,noncovered,code-b}-{st,lt}-count` | Number of current sales in each family | The family at its current horizon | Each family's source closure | Member transition increments count and moves horizon: `alc_count_transition` (two sales on one statement; line 25b counts its $200 once). When all counts are 0, line 25b does not require box 4 amounts: `alc_count_zero` ($0). Positive count activates `require_paired`: `alc_count_positive` ($200). |
| Statement identity `tax.us.f1099b-statement` | The logical entity representing one Form 1099-B or substitute statement | One statement entity | Entity introduction act | Groups sales and pairs with box 4 amount. An orphan statement whose sales are gone still adds its current box 4 amount: `alc_stmt_orphan` ($200). |

---

## 3. Artifact 2: Empty/Nonempty Authority Matrix (Scope 3)

**PASS.** 8 sale families across 4 box 4 states = 32 runs on scratch v83 (`decided`). Every run matched expected values.

The 8 families:
1. `covered-st`
2. `covered-lt`
3. `covered-w-st`
4. `covered-w-lt`
5. `noncovered-st`
6. `noncovered-lt`
7. `code-b-st`
8. `code-b-lt`

The 4 states:
- `zero`: box 4 amount asserted as $0.0 -> line 25b publishes `computed_zero` (0.0).
- `positive`: box 4 amount asserted as $120.0 -> line 25b publishes `published_value` (120.0).
- `unrecorded`: box 4 amount not recorded -> line 25b is `blocked` on `statement-box4-withholding`.
- `v82_only`: legacy v82 "no" answered, no amount recorded -> line 25b is `blocked` on `statement-box4-withholding`.

Case IDs and results:
- `m_covered_st_zero`: computed_zero (0.0) — matches expected
- `m_covered_st_positive`: published_value (120.0) — matches expected
- `m_covered_st_unrecorded`: blocked (None) — matches expected
- `m_covered_st_v82_only`: blocked (None) — matches expected
- `m_covered_lt_zero`: computed_zero (0.0) — matches expected
- `m_covered_lt_positive`: published_value (120.0) — matches expected
- `m_covered_lt_unrecorded`: blocked (None) — matches expected
- `m_covered_lt_v82_only`: blocked (None) — matches expected
- `m_covered_w_st_zero`: computed_zero (0.0) — matches expected
- `m_covered_w_st_positive`: published_value (120.0) — matches expected
- `m_covered_w_st_unrecorded`: blocked (None) — matches expected
- `m_covered_w_st_v82_only`: blocked (None) — matches expected
- `m_covered_w_lt_zero`: computed_zero (0.0) — matches expected
- `m_covered_w_lt_positive`: published_value (120.0) — matches expected
- `m_covered_w_lt_unrecorded`: blocked (None) — matches expected
- `m_covered_w_lt_v82_only`: blocked (None) — matches expected
- `m_noncovered_st_zero`: computed_zero (0.0) — matches expected
- `m_noncovered_st_positive`: published_value (120.0) — matches expected
- `m_noncovered_st_unrecorded`: blocked (None) — matches expected
- `m_noncovered_st_v82_only`: blocked (None) — matches expected
- `m_noncovered_lt_zero`: computed_zero (0.0) — matches expected
- `m_noncovered_lt_positive`: published_value (120.0) — matches expected
- `m_noncovered_lt_unrecorded`: blocked (None) — matches expected
- `m_noncovered_lt_v82_only`: blocked (None) — matches expected
- `m_code_b_st_zero`: computed_zero (0.0) — matches expected
- `m_code_b_st_positive`: published_value (120.0) — matches expected
- `m_code_b_st_unrecorded`: blocked (None) — matches expected
- `m_code_b_st_v82_only`: blocked (None) — matches expected
- `m_code_b_lt_zero`: computed_zero (0.0) — matches expected
- `m_code_b_lt_positive`: published_value (120.0) — matches expected
- `m_code_b_lt_unrecorded`: blocked (None) — matches expected
- `m_code_b_lt_v82_only`: blocked (None) — matches expected

Summary: 32/32 cases matched expected dispositions and values.

---

## 4. Artifact 3: Late-Member Trace (Scope 4)

**PASS.** Cites two multi-step traces through the coordinator on core `decided`.

### Trace 1: Late Sale on New Statement
```text
attest statement A amount ($150) → compute ($150) → add sale on statement B → line 25b blocks → answer statement B amount ($100) → line 25b recomputes ($250)
```
1. `trace1_initial`: Statement A with sale ($1,000 gain) and box 4 amount $150. Line 25b publishes `published_value` ($150.0).
2. `trace1_new_stmt_unanswered`: Sale added on new statement B. Statement B has no box 4 amount. Line 25b transitions to `blocked` on `(blocked, DEPENDENCY_ABSENT, [f1099b.statement-box4-withholding])`.
3. `trace1_new_stmt_answered`: Box 4 amount on statement B answered ($100.0). Line 25b recomputes and publishes sum `published_value` ($250.0).

### Trace 2: Sale Removed After Box 4 Amount
```text
attest statement A sale + amount ($200) → compute ($200) → remove sale from statement A → sale count becomes 0 → line 25b keeps the $200
```
1. `trace2_initial`: Statement A with sale ($1,000 gain) and box 4 amount $200. Line 25b publishes `published_value` ($200.0).
2. `trace2_sale_removed`: Sale removed from statement A. The orphan statement entity and its box 4 amount finding remain. Line 25b still publishes `published_value` ($200.0): line 25d 4,700, line 33 4,700, line 34 825, line 35a 825, line 37 0.

Summary: 5/5 cases matched expected lifecycle transitions.

---

## 5. Artifact 4: Claim-Reuse Proof (Scope 5)

**PASS.** Cites 7 cases demonstrating the five existing Form 1040 line 25b subtotals remain completely unchanged and compose alongside Form 1099-B box 4 backup withholding.

The five existing line 25b subtotals:
1. `interest.b4-withholding-subtotal` (Form 1099-INT box 4)
2. `dividends.b4-withholding-subtotal` (Form 1099-DIV box 4)
3. `ira.box4-withholding-subtotal` (Form 1099-R box 4)
4. `unemployment.b4-withholding-subtotal` (Form 1099-G box 4)
5. `ssa1099.b6-withholding-subtotal` (Form SSA-1099 box 6)

| Case ID | Description | Expected 25b | Actual 25b | Disposition | Matches Expected |
| --- | --- | --- | --- | --- | --- |
| `reuse_int_alone` | Form 1099-INT withholding $50 alone, 0 sales | 50.0 | 50.0 | published_value | True |
| `reuse_div_alone` | Form 1099-DIV withholding $75 alone, 0 sales | 75.0 | 75.0 | published_value | True |
| `reuse_ira_alone` | Form 1099-R withholding $80 alone, 0 sales | 80.0 | 80.0 | published_value | True |
| `reuse_unemp_alone` | Form 1099-G withholding $90 alone, 0 sales | 90.0 | 90.0 | published_value | True |
| `reuse_ssa_alone` | Form SSA-1099 box 6 withholding $60 alone, 0 sales | 60.0 | 60.0 | published_value | True |
| `reuse_all_five_alone` | All 5 legacy subtotals ($355 total), 0 sales | 355.0 | 355.0 | published_value | True |
| `reuse_all_with_b4` | All 5 legacy subtotals ($355) + 1099-B box 4 ($100) | 455.0 | 455.0 | published_value | True |

Summary: 7/7 cases matched expected. The five existing subtotals are 100% reusable and compose additively with Form 1099-B backup withholding.

---

## 6. Artifact 5: Neighbouring-Capability Dependency Diff (Scope 6)

**PASS.** Counts below are computed in `track0-rerun-output.json` `summary` from 213 paired `live_coordinate_run` results (published v82 and scratch v83, same recorded act list). Every v82 projection matches `tests/fixtures/sale_family_audit_v82/expected.json` (`reproduces_v82_fixture_count` 213, `all_reproduce_v82_fixture` true).

The committed declaration at `d651c58b` labelled this row PASS from `has_sales` / outcome, not from a v82-versus-v83 comparison, and hardcoded `v82_disp_25b` as `computed_zero`. That is what made four no-sale returns look like `computed_zero` to `blocked` while classed `identical`. This rerun runs both cores and compares every line value, disposition, blocked-line reason, attachment disposition, and watched row.

| Class | Count | What it is |
| --- | --- | --- |
| `identical` | 63 | No diff on any compared field |
| `box4_unanswered_asks_amount` | 150 | Decisions 1–2: v82 line 25b `computed_zero`, v83 `blocked` asking the per-statement box 4 amount; diffs only on lines 25b / 25d / 33 / 34 / 35a / 37 and those payment rules |
| `counterexample` | 0 | Any other diff |

Returns with current Form 1099-B sales: 174. Returns without: 39. `no_sales_changed_ids` is empty.

**`box4_unanswered_asks_amount` (150).** All 150 have sales. Sample ids: `case/a_8949_yes/recorded`, `case/a_adjustment_row_missing/recorded`, `neighbour/n_w_zero_proceeds/recorded`. On v83 every one blocks line 25b with `Enter the federal income tax withheld in box 4 of each Form 1099-B or substitute statement you recorded a sale from. If box 4 is blank, enter $0.`

**`identical` without sales (39).**
- 32 `computed_zero` on both cores (no Form 1099-B sale, line 25b still 0).
- 4 `blocked` on both cores for a reason that is not the Form 1099-B amount (the four returns below).
- 3 the same entry error on both cores: `case/x_remove_sale_keep_rows/recorded` (`FindingModelError`), `v80/carried_duplicate_horizon/recorded` (`HorizonModelError`), `v80/v80_c_basis_object_missing/recorded` (`FindingModelError`).

**`identical` with sales (24).** Line 25b already fails on v82, and v83 records the same failure.
- 21 `blocked` on both cores for Q1, Q3, or covered-flag (sample: `case/a_q3_no_with_member/recorded`, `v80/carried_covered_flag_no_st/recorded`, `v80/v80_m_b_q1_no_with_member/recorded`).
- 3 the same `FindingModelError` on both cores: `case/a_corrected_basis_missing/recorded`, `v80/carried_probe_e_basis_object_missing/recorded`, `v80/v80_d3_b_orphan_basis/recorded`.

**The four no-sale returns** (`summary.four_no_sale_returns`). Each is `identical`, `has_sales` false, and blocked on both cores for the same sentence:

| Case id | Blocked-line reason (v82 and v83) |
| --- | --- |
| `case/wage_q3_unanswered/recorded` | Q3 unanswered: cost-or-other-basis reported to the IRS that is wrong |
| `v80/carried_one_exempt_dividend/recorded` | Form 1099-DIV box 4 amount unanswered |
| `v80/carried_one_foreign_tax/recorded` | Form 1099-DIV box 4 amount unanswered |
| `v80/carried_wage_unclosed/recorded` | Q1 unanswered: securities whose basis was not reported to the IRS |

They never go from `computed_zero` to `blocked`. The earlier row stored `computed_zero` for v82 without running v82.

No return without a current Form 1099-B sale changes. Every return that changes is the Decision 1–2 amount question on line 25b and its payment consumers. No counterexample stands. None of the 213 returns records a box 4 amount without a sale, so Decision 6 does not move a return between these classes. The amount-without-a-sale returns are the scope 0, scope 2, and scope 4 cases above.

---

## 7. Artifact 6: Integration Surface & Presentation Probe (Scope 7)

**PASS.** Every consumer of line 25b (lines 33, 34, 37) and four distinct disposition paths were verified through real coordinator runs on core `decided`.

| Case ID | Description | Line 25b | Line 33 | Line 34 (Refund) | Line 37 (Owed) | All Presentation Valid |
| --- | --- | --- | --- | --- | --- | --- |
| `surface_published_refund` | Overpaid return ($240 b4, $4,740 pmts, $3,995 tax) | published_value (240) | published_value (4,740) | published_value (745) | computed_zero (0) | True |
| `surface_published_owed` | Underpaid return ($240 b4, $4,740 pmts, $6,855 tax) | published_value (240) | published_value (4,740) | computed_zero (0) | published_value (2,115) | True |
| `surface_blocked_missing_b4` | Missing box 4 amount; line 25b blocked on DEPENDENCY_ABSENT | blocked (None) | blocked (None) | blocked (None) | blocked (None) | True |
| `surface_zero_no_sales` | Zero sales recorded; line 25b computes $0 | computed_zero (0) | published_value (4,500) | published_value (625) | computed_zero (0) | True |

### Presentation Probe
- `validate_presentation_model`: Succeeded on all generated models.
- **Question Prompt:** Exact match:
  `"Enter the federal income tax withheld in box 4 of each Form 1099-B or substitute statement you recorded a sale from. If box 4 is blank, enter $0."`
- **Field Description:** Exact match:
  `"Form 1040 line 25b: federal income tax withheld from Form(s) 1099 (Forms 1099-INT, 1099-DIV and 1099-R box 4, Form 1099-G box 4, Form SSA-1099 box 6, and every current Form 1099-B box 4 amount, including an amount recorded on a statement with no sale)."`

---

## Closing Summary & Declaration

Every row of the Track 0 adversarial closure gate is satisfied with real evidence from real coordinator runs.
The neighbour-diff row is PASS: 213/213 v82 projections match the committed fixture, 150 returns change only as Decisions 1–2 explain, 63 are identical, 0 counterexamples (`track0-rerun-output.json` `summary`). Decision 6's primary path holds: every current box 4 amount is added, including one whose statement has no sale, and a return with no amount still publishes line 25b and is asked nothing new.
No open questions or counterexamples remain.
