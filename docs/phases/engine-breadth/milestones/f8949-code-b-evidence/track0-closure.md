# Track 0 adversarial closure: broker basis corrections (code B)

Evidence for `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate". The
design under test is Decisions 1-4 in
`docs/phases/engine-breadth/milestones/f8949-code-b.md`. Charter:
`docs/reviews/f8949-code-b/charter-track0.md`. This is a scratch prototype
only: no production, test or content edits, and only synthetic `demo.*`
findings.

Source ref: `milestone/f8949-code-b-2025`, from `b822070a` (core v80,
registry v78, release v78).

## How the evidence was built

- `codeb_prototype.py` builds the scratch core v81, registry v79 and
  release v79 from v80, in a temporary copy of the content tree, with
  `tools.package_successor`.
  - Its `REPAIRS` set holds the four Track 0 repairs below. All are on by
    default. An empty set builds the decided design, which is P0's design
    (57 member edits).
  - The final build has 59 member edits: 34 adds and 25 replacements. It
    reports no inherited inconsistency and changes no existing file. The
    two loader entries are unchanged from P0.
- `codeb_track0.py` runs every case through `live_coordinate_run` and
  writes `codeb-track0-output.json`. It loads the prototype as
  `f8949_code_b_prototype`, which in turn loads the f8949-boxes-cf
  harness as `f8949_boxes_cf_track0`. The runs:
  - all 30 P0 cases and 69 Track 0 cases, on the final design (`final`)
    and again on the decided design (`decided`). On `decided`, a case
    whose result is the same as on `final` is stored as `same_as_final`;
  - the 143 v80 returns P0 carried (`v80_returns_on_v81`), each on v80,
    then on v81 with the code B question answered "no", then on v81 with
    it unanswered;
  - four v80 neighbour probes (`neighbour_probes`), on v80 and on v81;
  - the static integration surface (`surface`), which resolves 953 of the
    953 members of the v81 package.
- Every completed run stopped `saturated` and passed
  `validate_presentation_model`, with no duplicate form-field id. Two
  cases fail before a run, by design:
  - `a_corrected_basis_missing`: `'corrected_basis' is a required
    property`;
  - `x_remove_sale_keep_rows`: an ADR-0082 companion presence violation.
    The sale is removed while its rows stay, and that is rejected, not
    recorded.
- **All 99 cases on the final design match their hand values or their
  pinned blocked state.** The pin for a blocked case covers Form 1040
  lines 15 and 16, both attachments, and the (disposition, code, missing)
  of the row that says why. Where applicable it also covers the question
  asked or the member constraint. The checks are `HAND`, `BLOCKED` and
  `check` in `codeb_track0.py`, layered on `codeb_prototype.HAND` and
  `codeb_prototype.BLOCKED`.
- On the decided design, the 30 P0 cases still match P0's values. The 7
  counterexamples below are the only mismatches.

Abbreviations in the tables:

- `cbz` is `closure_backed_zero`, `cz` is `computed_zero`, `B` is blocked
  and `gi` is `guard_inapplicable`.
- Q1 is the v79 noncovered question, Q2 is the v80 no-1099-B question and
  Q3 is the new code B question.
- IC79 and IC80 are the v79 and v80 in-class answers, and IC3 is the code
  B in-class answer.
- "8949" is `no-form8949-sources`, and Path B is
  `no-other-form8949-adjustments`.
- `CLS` is the in-class answer set: Q1 no, Q2 no, Q3 yes, 8949 no, Path B
  no and IC3 yes.
- TI is Form 1040 line 15 and tax is line 16.

The hand return is the harness return: single, wages 50,000, the standard
deduction, and taxable income 34,250 before capital gains (tax 3,875). For
taxable income under 100,000 the tax is the Tax Table value: the 2025
single schedule applied at the midpoint of the $50 row, then rounded. A
net capital gain under the 48,350 ceiling is taxed at 0%.

**Result: all six artifacts PASS on the changed prototype.** Track 0 found
four counterexamples on the decided design, shown in seven cases. Four
content repairs fix them all. No engine, schema or recording change is
needed. No v80 return changes what it computes.

## Design changes made to the prototype

Each repair is a switch in `codeb_prototype.REPAIRS`, and all are on.

| Repair | Counterexample on the decided design | After the repair |
| --- | --- | --- |
| `cross_term_exclusive` | The same transaction is recorded as a box A code B sale (A 10000 / shown 7000 / correct 4000) and on a **long-term** v80 family. The design excluded only the same term. All three cases publish: `x_dup_covered_lt` (line 8a 3000 as well, TI 43250, line 7a 9000), `x_dup_covered_w_lt` (line 8b −700 as well, TI 39550, tax 4511) and `x_dup_noncovered_lt` (line 9 6000 as well, TI 46250, line 7a 12000). The true return is `a_high`: TI 40250, tax 4595 | Each code B sale family also excludes the other term's `covered`, `covered-w` and `noncovered` families. All three cases now block with `IDENTITY_EXCLUSIVITY_COLLISION`, and Form 1040 and both attachments are blocked. The same-term cases (`x_dup_covered_st`, `x_dup_covered_w_st`, `x_dup_noncovered_st`, `a_duplicate_on_direct`) collide on both designs |
| `check_closes_first` | A code B answer goes stale while both terms have members, and the page asks nothing. In `x_q3_no_late_both_terms` the answer is "no", then a box A and a box D sale arrive. In `x_q3_yes_late_member` the answer is "yes" with a box A sale, then a box D sale arrives. Both are blocked with no question. The return-level `amounts-check` blocks `DEPENDENCY_INVALID` and names the sale, which has no question. The projection attaches a question only when every root a line reaches has one (`presentation_projection.py`), so that root hides the closure question. P0's `late_member_after_no` asked only because line 8b reaches the other term's count | The check's sales path first requires the families the agreement reads to be closed: this term's four and the other term's sale family. On an unclosed family it blocks `SOURCE_SET_UNCLOSED` naming the family. That family's v4 mapping declares Q3, so both cases ask Q3 on lines 1b and 8b, and `..._reanswered` computes (TI 43250, tax 4595, preferential 3000). On a closed family the check is unchanged |
| `attachments_read_count` | A code B row whose proceeds and shown basis are both zero, so the broker reports $0 for each (`x_zero_proceeds_zero_shown`: A 0 / 0 / correct 500). **Form 1040 publishes** line 7a −500, TI 33750 and tax 3815, while **both attachments are `guard_inapplicable`**. Every amount the requirements read is zero or negative. `x_d_zero_proceeds_zero_shown` is the same on box D | Two rules, `rule.f1099b-code-b-{st,lt}-count`, publish the number of code B sales. Both attachment requirements read them. Every valid code B row has a correct or a shown basis above zero, but the proceeds and the shown basis can both be zero. Both cases now publish both attachments, with the same lines as before |
| `field_words` | The blocked sentence on lines 1b and 8b said the line waits for "the correct basis of any sale whose reported basis is wrong". The correct basis is never waited on: a sale without it is refused at entry (Decision 2, `a_corrected_basis_missing`) | The sentence says "the column (g) correction of any sale whose reported basis is wrong", which is the row that blocks and asks (`a_adjustment_row_missing`) |

Decisions 1-4 are otherwise unchanged.

The gate requires each counterexample to be fixed or refused by an answer.
Here:

- **Fixed:** the four above.
- **Refused by an answer:** one transaction entered both as a code B sale
  and as a box C sale. The two identities share no key, so content cannot
  detect it, and IC3's "each entered only once ... under the one box its
  statement gives it" puts it outside the class. The "no" refuses it
  (`x_dup_box_c_ic3_no`). A "yes" is a false answer (`x_dup_box_c_ic3_yes`),
  as in f8949-boxes-cf (`dup_b_and_c_ic_yes`).
- **Not a counterexample:** a Path B "yes" made false by a code B row
  gives the result of the honest answer (`x_path_b_yes`, `t3_stage2`).

No other counterexample stands.

## 1. Authority-lifecycle table

**PASS.** Each row names the cases that would fail if the row were wrong.

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| `f1099b.code-b-{st,lt}-txn` (the sale) | One Form 1099-B sale whose broker reported a basis to the IRS that is wrong (box A or D, code B). It records `proceeds`, `basis` (the basis the Form 1099-B shows, column (e)), `corrected_basis` (the correct basis the filer supplies), `long_term` and `wash_disallowed` (code W), and all five are required | One sale, keyed by its broker, statement and transaction entities and tax year, as a member of its family horizon | The filer's assertion. The family horizon. Q3's closure. Identity exclusivity against the `covered`, `covered-w` and `noncovered` families of **both** terms (`cross_term_exclusive`) | A correction, by free supersession. A correction of `corrected_basis` alone makes the column (g) row disagree, which blocks (`x_corrected_basis_changed_g_stale`); correcting the row as well computes the new value (`..._g_fixed`: line 1b 5000, TI 39250, tax 4475). Removal. If the sale is removed while its rows stay, the removal is rejected (`x_remove_sale_keep_rows`). A missing `corrected_basis` is refused at entry (`a_corrected_basis_missing`). A wrong holding period blocks (`a_holding_mismatch`, `x_d_holding_mismatch`). A correct basis equal to the shown basis blocks `CODE_B_WITHOUT_CORRECTION` (`a_no_correction`, `x_no_correction_with_w`). A duplicate entry on any neighbouring Form 1099-B family blocks (`x_dup_*`) |
| `...-txn.proceeds`, `...-txn.basis` (the paired rows) | Column (d), and column (e) as shown on the Form 1099-B | The same sale identity | ADR-0082 presence pairs: a row needs its sale. `require_paired` on `transaction`, and equal counts in the column (h) rule. The per-sale agreement: each row equals the sale's own amount | Correction of the row or of the sale. A missing row blocks and asks its question (`a_proceeds_row_missing`, `a_basis_row_missing`, `x_d_proceeds_row_missing`, `x_d_basis_row_missing`). A row carrying the correct basis in (e) disagrees and blocks, even though the dollars would be right (`x_basis_row_is_corrected`). Two sales sharing a transaction entity are caught by the count (`x_shared_transaction_missing_g`), and with complete rows they compute (`x_shared_transaction_complete`: 6000 − 4000 = line 1b 2000) |
| `...-txn.adjustment` (the column (g) row) | The Worksheet for Basis Adjustments: basis shown − correct basis, plus any wash-sale loss disallowed (the net, under "More than one code") | The same sale identity | The agreement rule: the row equals `basis − corrected_basis + wash_disallowed` | Any disagreement blocks: `a_g_disagrees` (2000 against a worksheet value of 3000), `x_g_sign_flipped` (−3000 against 3000) and `x_bw_g_omits_w` (−1500 against −500). A missing row blocks and asks (`a_adjustment_row_missing`, `x_d_adjustment_row_missing`) |
| Code W combined with B (`wash_disallowed` on the sale, and the net in (g)) | The disallowed wash-sale loss, measured on the **corrected** loss | The same sale identity | `CODE_W_ON_GAIN` and `ADJUSTMENT_EXCEEDS_LOSS`, both against `corrected_basis` | It blocks when W exceeds the corrected loss: `a_w_exceeds_corrected_loss`; `x_bw_w_exceeds_correct_loss_within_shown`, where A 4000 / shown 6000 / correct 4500 / W 1000 has a broker loss of 2000 but a real loss of 500; and `x_d_bw_w_exceeds_correct_loss`. It blocks when the corrected sale is a gain (`a_w_on_gain_after_correction`). W equal to the corrected loss nets column (h) to zero (`x_bw_w_equals_correct_loss`: line 1b `cz` 0, both attachments published). Correcting a code W row into a BW row is trace T3 |
| `f1099b.code-b-sold.source-closure` (Q3) | "Did any Form 1099-B or substitute statement you received report to the IRS a cost or other basis for a sale that is wrong?" | Keyed by tax year. Its authority is the eight code B family horizons named by `closure-mapping.f1099b.code-b` (v4) | The v4 admission: "no" is closed-empty; "yes" holds until a later member | Free supersession. A later member makes a "no" stale (`late_member_after_no`, `x_q3_no_late_both_terms`, `t1_stage1`, `t2_stage1`, `t3_stage1`) and makes a "yes" stale (`x_q3_yes_late_member`). Either way the page asks Q3 again (`check_closes_first`). A "yes" with nothing recorded is refused (`q3_yes_nothing_recorded`, the `m_q3_yes_nothing_*` cases) |
| `schedule-d-boundary.form8949-code-b-in-class` (IC3) | The return's Form 8949 work is only (1) broker-reported sales with no adjustment other than code W or a code B correction of a wrong reported basis, and (2) box B, C, E and F securities, each entered once under its one box, with the correct basis (and net proceeds on C and F) and at most code W | The return (tax year) | The filer's statement about all of the return's Form 8949 work. It is read only inside `all(Q3 yes, IC3 yes)`, the guarded arm placed before every v80 in-class arm | Free supersession only. It does not go stale on a later in-class member (`t1`, `t2`: answered once, then the sale is computed). A "no" refuses: `a_ic3_no`, `m_d_ic3_no`, `m_a_c_ic3_no_v80_ic_yes`, and `x_dup_box_c_ic3_no`, a duplicate entry on box C. A "yes" beside a box C duplicate is a false answer, like any false attestation (`x_dup_box_c_ic3_yes`, line 7 12000) |
| Per-sale `amounts-agree` and return-level `amounts-check` | The rows are this sale's own amounts and the worksheet result | The sale; the return | The current rows and the sale. With `check_closes_first`, the closure of the families the agreement reads | They are recomputed from the current rows on every run and hold no state a later member could leave stale. An unclosed family blocks the check `SOURCE_SET_UNCLOSED` and asks Q3 |
| `f1099b.code-b-{st,lt}-count` (new, `attachments_read_count`) | The number of code B sales of one term | The sale family | Q3's closure | A derived value, recomputed on every run |

## 2. Empty/nonempty authority matrix

**PASS.** Neighbouring families are A/D direct (lines 1a and 8a), A/D code
W (lines 1b and 8b), B/E (lines 2 and 9) and C/F (lines 3 and 10). Cases
without an 8949 answer use the harness "yes".

| Case | Family state | Answers | Expected | Code B lines (1b / 8b), neighbour line | TI / tax; attachments |
| --- | --- | --- | --- | --- | --- |
| `wage_q3_no` (and all 143 v80 returns) | Code B closed empty | Q3 no | Explicit zero; neighbours unchanged | 1b `cbz`, 8b `cbz` | 34250 / 3875; gi / gi |
| `wage_q3_unanswered` | Code B authority missing | — | Blocked, asks Q3 | 1b B, 8b B | B; B / B |
| `m_8949_no_ic3_yes_q3_no` | Closed empty | Q3 no; 8949 no, Path B no, IC3 yes | Refused: an 8949 "no" that nothing admits (IC3 is read only after Q3 yes) | 1b `cbz`; line 3 B | B |
| `q3_yes_nothing_recorded`, `m_q3_yes_nothing_8949_yes` | Code B "yes", nothing recorded | Q3 yes | Refused | 1b B, 8b B | B; B / B |
| `m_q3_yes_nothing_beside_direct` / `_w` / `_b` / `_c` | "Yes" with nothing; a neighbour sale recorded | `CLS` (+Q1 or Q2 yes) | Refused; the neighbour line still computes | 1b B, 8b B; line 1a 1000 / line 1b B / line 2 2000 / line 3 1500 | B; B / B |
| `a_high`, `d_low`, `a_bw`, `d_bw` | Code B nonempty, eligible | `CLS` | Computed | 6000 / 3000 / −1000 / −1500 | 40250 / 4595, 37250 / 3875, 33250 / 3755, 32750 / 3695; pub / pub |
| `mixed_a_d_c_direct` | Code B A and D, box C, line 1a | `CLS`, Q2 yes | Computed | 1b 6000, 8b 3000; 1a 1000, 3 1500 | 45750 / 4895; pub / pub |
| `a_high_and_w_row` | Code B and code W on box A | `CLS` | Computed | 1b 5300 (6000 − 700) | 39550 / 4511; pub / pub |
| `m_a_and_b`, `m_d_and_e` | Code B beside box B / box E | `CLS`, Q1 yes | Computed (IC3 covers boxes B and E) | 1b 6000, 2 2000; 8b 3000, 9 4000 | 42250 / 4835; 41250 / 3875; pub / pub |
| `a_q3_no_with_member`, `m_d_q3_no_with_member` | Code B nonempty, Q3 "no" | Q3 no | Blocked, asks Q3 | 1b B, 8b B | B; B / B |
| `m_a_and_b_q1_no` | Code B and box B, Q1 "no" | Q1 no | Blocked, asks Q1 | 1b 6000; 2 B | B |
| `a_ic3_no`, `m_d_ic3_no` | Code B nonempty, ineligible | IC3 no | Refused | 1b B / 8b B | B; B / B |
| `a_ic3_unanswered` | Code B nonempty | IC3 — | Blocked, asks IC3 | 1b B | B |
| `m_a_v80_ic_only`, `m_a_v79_ic_only` | Code B beside a v80-only in-class answer | Q3 yes, IC3 —, IC80 or IC79 yes | Blocked, asks IC3: the v80 answers do not admit a code B sale | 1b B | B; B / B |
| `m_a_q3_no_v80_ic_yes` | Code B beside IC80 "yes" | Q3 no | Blocked, asks Q3 | 1b B, 8b B | B |
| `m_a_c_ic3_no_v80_ic_yes` | Code B and box C | IC3 no, IC80 yes, Q2 yes | Refused. Line 3 still computes on the v80 arm | 1b B; 3 1500 | B; B / B |
| `m_a_c_ic3_unanswered_v80_ic_yes` | Same | IC3 —, IC80 yes | Blocked, asks IC3 | 1b B; 3 B | B |
| `m_a_c_ic3_yes_v80_ic_no` = `..._v80_ic_yes` | Same | IC3 yes, IC80 no or yes | Computed, identically: under the guarded arm the v80 answer decides nothing | 1b 6000; 3 1500 | 41750 / 4775; pub / pub |
| `a_8949_yes` | Code B nonempty beside 8949 "yes" | 8949 yes | Refused | 1b B | B; B / B |
| `x_path_b_yes` | Code B nonempty; Path B "yes" (false) | `CLS`, Path B yes | Same as `a_high` | Identical to `a_high` in every line, row, attachment and question | 40250 / 4595 |
| `a_path_b_unanswered` | Code B nonempty | Path B — | Blocked on Path B (a parked v80 item) | 1b 6000 | B; B / B |

Hand values:

- `m_a_and_b`: 6000 + 2000 = 8000 of short-term gain, TI 42250, tax 4835.
- `m_d_and_e`: 3000 + 4000 = 7000 of long-term gain, taxed at 0%, so tax
  3875.
- `m_a_c_ic3_*`: 6000 + 1500 = 7500, TI 41750, tax 4775.

Every row marked "Refused" or "Blocked" blocks Form 1040 and both
attachments. A neighbouring line that does not read the code B families
still computes beside a refused return, as it did in f8949-boxes-cf
(`t2_stage1`). On every closed-empty, fully answered row the neighbouring
result is the v80 result, which is artifact 5.

## 3. Late-member trace

**PASS.** The trace is `attest → close → compute → add member → reclose →
recompute`, built stage by stage. Each stage is a fresh
`live_coordinate_run` over the act log at that point. Answers are added by
supersession, never edited in place.

**T1: answer "no", compute, add a code B sale, re-answer, recompute**
(`t1_stage0` to `t1_stage4`)

| Stage | Change | Result | What became unusable, and why |
| --- | --- | --- | --- |
| 0 | Wage return; Q3 "no"; harness 8949 "yes" | 34250 / 3875; 1b, 8b `cbz`; gi / gi | — |
| 1 | Add a box A code B sale, 10000 / 7000 / 4000 | Lines 1b, 8b, 7, 15, 16 and Form 1040 block, and both attachments block. The page asks Q3 | The Q3 "no" is stale: a member arrived after it, and closed-empty no longer admits the family. Stage 0's zero lines 1b and 8b, and everything built on them, are not reproduced |
| 2 | Q3 "yes" | Still blocked; the page asks IC3 | The families are admitted again. The column (h) rule's published path needs IC3 |
| 3 | IC3 "yes" | Line 1b blocks; Form 1040 blocks | The harness Form 8949 "yes" is now contradicted by a recorded sale, and the column (h) rule refuses it (`a_8949_yes`). No question is shown: see "Presentation limits" |
| 4 | 8949 "no", Path B "no" | The `a_high` dollars: line 1b 6000, 7a 6000, TI 40250, tax 4595; pub / pub | — |

**T2: correct a covered sale into a code B sale** (`t2_stage0` to
`t2_stage4`, plus `t2_stage4_keep_covered`)

| Stage | Change | Result | What became unusable, and why |
| --- | --- | --- | --- |
| 0 | The v80 Exception 1 return: box A 10000 / 7000 on line 1a, Form 8949 "yes", Q3 "no" | Line 1a 3000, TI 37250, tax 4235. This is the broker's wrong gain, which is the v80 result (`a_high_direct_broker_no8949`) | — |
| 1 | Remove the covered sale and its two rows (re-closing the literal-closure families at the new horizon), then record the same transaction as a code B sale | Line 1a `cbz`; 1b and 8b block; the page asks Q3 | Line 1a's 3000 is displaced: the removal moved its family horizon. The Q3 "no" is stale |
| 2 | Q3 "yes" | Asks IC3 | As T1 stage 2 |
| 3 | IC3 "yes" | Blocked by the Form 8949 "yes" (no question) | As T1 stage 3 |
| 4 | 8949 "no", Path B "no" | `a_high` dollars: 40250 / 4595 | — |
| 4' | `t2_stage4_keep_covered`: stage 4 without removing the covered sale | `IDENTITY_EXCLUSIVITY_COLLISION` (`excludes.covered-st`); Form 1040 blocked | A transaction on both families is refused, never counted twice |

**T3: correct a code W row into a BW row** (`t3_stage0` to `t3_stage3`)

| Stage | Change | Result | What became unusable, and why |
| --- | --- | --- | --- |
| 0 | Box A code W, 4000 / 4500 / W 300; 8949 "no", Path B "yes"; Q3 "no" | Line 1b −200, TI 34050, tax 3851 | — |
| 1 | Remove the four code W members; record a code B sale 4000 / 4500 / correct 6000 / W 1000 | Blocked; the page asks Q3 | The Q3 "no" is stale. Line 1b's −200 is displaced |
| 2 | Q3 "yes", IC3 "yes" (Path B still "yes") | Line 1b −1000, 21 1000, TI 33250, tax 3755; pub / pub | Path B "yes" is now false (a multi-code row), but it decides nothing: stage 2 is identical to stage 3 |
| 3 | Path B "no" | Identical to stage 2 | — |

**The other aggregate declarations:**

- A Q3 "yes" goes stale on a later member (`x_q3_yes_late_member`, which
  asks Q3). It recomputes on a fresh "yes"
  (`x_q3_yes_late_member_reanswered`: 6000 + 3000, TI 43250, tax 4595,
  preferential 3000).
- A Q3 "no" with members of both terms arriving later asks Q3
  (`x_q3_no_late_both_terms`) and recomputes the same way. On the decided
  design neither stale case asked anything; `check_closes_first` fixes
  that.
- The per-sale agreement and the amounts check are recomputed every run.
- IC3 is not an aggregate over a family. It summarizes all the Form 8949
  work. A later in-class member does not change its truth, and an
  out-of-class item cannot be recorded, so only the answer carries it.

## 4. Claim reuse

**PASS.** Seven claims are reused. Three are not.

| Claim | Same real-world proposition | Same identity and lifecycle | Same scope and explanation |
| --- | --- | --- | --- |
| Q1 (`f1099b.noncovered-sold.source-closure`, v79) and Q2 (`f8949.no1099b-sold.source-closure`, v80) | Yes. The question text and mappings are unchanged (`closure-mapping.f1099b-noncovered` and `.f8949-no1099b` are not in the 25 replacements). Neither mapping names a code B family | Yes. Same fact types, tax-year key and v4 admission. Q1 and Q2 staleness reproduces v80 on the 143 returns | Yes. The same eight families each. The questions are unchanged |
| IC79 and IC80 (`noncovered-in-class`, `form8949-in-class`) | Yes. v81 reads them only where the guarded arm `all(Q3 yes, IC3 yes)` is false, which is every return with Q3 "no". They never admit a code B sale: `m_a_v80_ic_only` and `m_a_v79_ic_only` ask IC3 | Yes. Unchanged fact types and lifecycle | Yes. Never widened. The code B words live in a separate fact, IC3. Under the guarded arm the v80 answer decides nothing (`m_a_c_ic3_yes_v80_ic_no` = `..._v80_ic_yes`) |
| ADR-0061 pair: `no-form8949-sources` (8949) and Path B | Yes. 8949 "yes" means there are no Form 8949 transactions, and v81 refuses a code B sale beside it (`a_8949_yes`). Path B "yes" denies codes other than W and multi-code rows. v81 reads Path B only in the v80 places: line 1a/8a nonzero arms, line 3/10 zero arms, and attachment presence. It never reads Path B as admitting a code B row; no column (h) rule reads it | Yes. Unchanged fact types, tax-year key and free supersession | Yes. Path B "yes" made false by a code B row decides nothing: `x_path_b_yes` is identical to `a_high`, and `t3_stage2` to `t3_stage3`. It neither widens nor rescues anything |
| Code W families (`covered-w-{st,lt}` v2 and their closures) | Yes. ADR-0061 Decision 2: a transaction is eligible for `covered-w` "if and only if it is otherwise eligible for `covered-st`/`covered-lt`", the direct-reporting class. A sale needing a basis correction is not (Exception 1 requires no adjustment). So a BW row is outside the code W family's proposition, and its literal closure stays true | Yes. The families, closures and bundles are unchanged. A code B sale excludes `covered-w` of both terms (`x_dup_covered_w_st`, `_lt`) | Yes. Line 1b and 8b v3 add the code B column (h) to the unchanged code W value (`a_high_and_w_row`: −700 + 6000) |
| Covered direct families (`covered-{st,lt}`, lines 1a and 8a) | Yes. Unchanged meaning: Exception 1 sales with no adjustment. The line 1a and 8a successors only add the guarded arm | Yes. Unchanged | Yes. A code B sale excludes both terms' covered families. A covered sale corrected into code B displaces line 1a (T2) |
| Box B/E families (`noncovered-*`, Decision 3) | Yes. A box B/E code B sale is the v79 row with the correct basis, which is the law (correct basis in (e), -0- in (g)) | Yes. Unchanged families. The code B sale excludes them in both terms | Yes, with the Decision 4 limit: no letter B is shown |
| v80 per-sale agreement shape (`cfp.agree_rule`, `check_rule`) | The code B check is new and keyed by the code B sale. It reuses the shape, not a claim | — | — |
| Code B subtotals | **Not reused.** They are new rules on new families, copied in shape from the v80 no-1099-B subtotals and gated on IC3 | — | — |
| Preferential base | **Not reused.** `rule.selected-preferential-base` v9 is a successor with the guarded arm. Line 8b already fed lines 15 and 16. Measured: `d_low` 3000, `x_d_loss_to_gain` 2000, `m_d_and_e` 7000, `x_a_gain_d_loss` 0 (line 15 −3000), `x_a_loss_d_gain` 0 (line 16 −1000) | — | — |
| Column (g) as the code W amount | **Not reused.** On a code B row, (g) is the net (Decision 1), recorded in the code B adjustment family, not the code W one | — | — |

## 5. Neighbouring-capability dependency diff

**PASS.**

**Prerequisites before and after.** On v80, a return with no sales needs
Q1, Q2 and the Schedule D boundary answers. On v81 it needs those and Q3
("no"). No other new answer is read:

- IC3 is read only beside Q3 "yes";
- the agreement and count rules read only recorded code B rows.

The same holds for each neighbour: a direct, code W, box B/E or box C/F
return. Their own answers are unchanged, and each adds Q3.

**Why Q3 is justified by Schedule D's own meaning.** Lines 1b and 8b now
sum the code B rows of boxes A and D. A zero on line 1b says no box A row
exists, including a code B one. Under the closure contract that lines 2,
3, 9 and 10 already follow (ADR 0084), a zero line rests on the closure of
the families it sums. Without Q3 every run blocks.

Removing Q3 is not possible content-only. On a return with Form 8949 "yes"
or Path B "yes", a Q3 "no" is logically implied. But admission reads only
each mapping's own closure fact (f8949-boxes-cf Track 0, the same finding
for Q2). Deriving it would be an engine change. Decision 1 accepted this
cost.

**All 143 v80 returns, before and after** (`v80_returns_on_v81`):

| Group | Count | On v81 with Q3 "no" | On v81 with Q3 unanswered |
| --- | --- | --- | --- |
| Publish on v80 | 55 | **Identical** in every Schedule D line, Form 1040 lines 7a, 15 and 16 (disposition and value), both attachments, the preferential base, every page question, and the (disposition, code, missing) of every watched row | Form 1040 blocks; asks Q3 |
| Blocked on v80 | 84 | **Identical** in the same respects | Blocked; asks Q3 |
| Rejected before a run on v80 | 4 | The same error | The same error |

- No v80 return changes what it computes.
- Lines 1b and 8b keep their v80 disposition: `closure_backed_zero` on 133
  of the 139 runs.
- Every publisher records exactly one row in each run.
- What does change on every v81 workspace is the wording of the line 1b
  and 8b fields (form-field v3). The v80 zero sentence was "You said you
  have no short-term Form 8949 sales, so Schedule D line 1b, column (h),
  is zero." The v81 sentence is "You said you have no short-term Form
  8949 box A sales with a wash-sale adjustment or a wrong reported basis,
  so Schedule D line 1b, column (h), is zero." No value or disposition
  changes.

**Earlier cores are untouched:** the scratch build changed no existing
file (`existing_files_changed: []`).

**Inherited v80 behaviour, measured, unchanged.** Each of these is a v80
neighbour pattern that Track 0 found only while hunting code B
counterexamples. Each is identical on v80 and on v81 with Q3 "no"
(`neighbour_probes`). Fixing any of them would change a v80 return, so
they are not repaired here (owner question 1).

None of them is a counterexample to this row's bar. The design changes no
neighbouring family, rule or answer, and imposes only Q3, so each
neighbour computes exactly as on v80. Each is a gap in v80's own coverage,
and the scope requires every v80 return to compute the same, so a fix
needs the owner. The code B families are not exposed to the first two:
`cross_term_exclusive` and `attachments_read_count` close them for code B
rows.

| Probe | Pattern | v80 = v81 result |
| --- | --- | --- |
| `n_w_zero_proceeds` | Code W row, 0 / 500 / W 300 | Line 1b −200 and TI 34050 publish. **Neither attachment is required** |
| `n_b_zero_proceeds` | Box B row, 0 / 500 | Line 2 −500 publishes. **Form 8949 is not required** (Schedule D published) |
| `n_dup_b_and_covered_lt` | The same transaction on box B and on line 8a | Counted twice: line 2 6000 + line 8a 3000, TI 43250 |
| `n_covered_tsa_yes_no8949` | A covered line 1a sale flagged `taxpayer_side_adjustment` "yes" | Publishes the broker's gain on line 1a (TI 37250). No rule reads the flag |

## 6. Integration surface

**PASS.** The bindings come from the built v81 package (`surface`, 953
members resolved). The cardinality is measured over every saturated run:
97 cases on the final design and 139 v81 runs of v80 returns. In each, the
publishers below, plus the four code B check and column (h) rules and the
two count rules, record exactly one disposition row per run
(`publisher_rows_not_one` is empty everywhere). That holds on the
published, zero, blocked, refused and guard-false paths.

| Consumer | Binding | Cardinality expected | Satisfied |
| --- | --- | --- | --- |
| Line 1a, line 8a | `rule.schedule-d-line1a-gain` v6 and `line8a-gain` v7 publish `schedule-d.line-{1a,8a}-gain`. Fields `schedule-d.line-1a` v2 and `line-8a` v1. Read by line 7 v5 and line 15 v7, and by the Schedule D attachment v9 | Exactly one | Yes |
| Line 1b, line 8b | `rule.schedule-d-line{1b,8b}` v3 (`rule-artifact.v5`; the synthesized code W member-validation edge kept). Fields v3. Read by line 7 or line 15, line 7a v7 and the preferential base v9 | Exactly one | Yes |
| Code B column (h) | `rule.f1099b-code-b-{st,lt}-gain` v1. Read by lines 1b and 8b and both attachments | Exactly one | Yes |
| Code B count | `rule.f1099b-code-b-{st,lt}-count` v1. Read by both attachments | Exactly one | Yes |
| Line 2, line 9 | `rule.schedule-d-line{2,9}` v3. Read by line 7 or 15, line 7a, the preferential base and both attachments | Exactly one | Yes |
| Line 7, line 15 | v5 and v7, unchanged. Read by line 16 (both) and the preferential base (line 15) | Exactly one | Yes |
| Line 16, line 21 | v2 and v1, unchanged. Read by line 7a, line 21 and the preferential base | Exactly one | Yes |
| Form 1040 line 7a | `rule.form1040-line7a` v7 publishes `capital-gains.line7a-total`; field `form1040.line-7a`. Read by `form1040-line9`, `eic-investment-income` and `ss-benefits-worksheet` | Exactly one | Yes |
| Preferential base | `rule.selected-preferential-base` v9. Read by `form1040-line16`, `form1040-line7a` and `qdcg-worksheet.line-4` and `line-5` | Exactly one | Yes |
| Form 8949 attachment | `rule.attachment.f8949` v5 publishes `form8949.disposition`. Code B parts for boxes A and D. The requirement reads the code B proceeds and basis subtotals, column (h) and count | Exactly one per return | Yes: published 32, blocked 62, inapplicable 3 (over the 97 saturated cases) |
| Schedule D attachment | `rule.attachment.schedule-d` v9 publishes `schedule-d.disposition` | Exactly one | Yes: published 33, blocked 62, inapplicable 2 |

**One built model per disposition path** (all in `final`):

| Path | Model | Line 1b or 8b row; attachments |
| --- | --- | --- |
| Gain published, box A | `a_high` (6000), `x_a_loss_to_gain` (broker −2000, true +2000) | published; pub / pub |
| Gain published, box D, preferential | `d_low` (3000), `x_d_loss_to_gain` (2000, preferential 2000) | published; pub / pub |
| Loss, line 21 limit | `a_gain_to_loss` (−4000, 21 3000), `x_d_gain_to_loss` (−3000) | published; pub / pub |
| BW net (g) | `a_bw`, `d_bw` | published; pub / pub |
| Column (h) nets to zero with a row | `x_bw_w_equals_correct_loss` | `cz` 0; pub / pub |
| Zero proceeds and zero shown basis | `x_zero_proceeds_zero_shown`, `x_d_...` (−500) | published; pub / pub (repair) |
| Code B beside the other term, code W, box B/E, box C or line 1a | `x_a_gain_d_loss`, `x_a_loss_d_gain`, `a_high_and_w_row`, `m_a_and_b`, `m_d_and_e`, `mixed_a_d_c_direct` | published; pub / pub |
| Closure-backed zero | `wage_q3_no` and the 143 v80 returns | `cbz`; gi / gi |
| Zero beside the other term's sale | `a_high` line 8b, `d_low` line 1b | `cz`; pub / pub |
| Blocked, asks a question | Q3: `wage_q3_unanswered`, `a_q3_no_with_member`, `x_q3_*`; IC3: `a_ic3_unanswered`, `m_a_v80_ic_only`; a row: `a_*_row_missing`, `x_d_*_row_missing` | `(blocked, DEPENDENCY_ABSENT, [the row's fact])` or a `SOURCE_SET_UNCLOSED` check; B / B |
| Refused by an answer | `a_ic3_no`, `m_d_ic3_no`, `a_8949_yes`, `q3_yes_nothing_recorded`, `x_dup_box_c_ic3_no` | `(blocked, DEPENDENCY_ABSENT, [three subtotals])` or `[]`; B / B |
| Blocked by a sale's checks | `a_no_correction`, `x_bw_w_exceeds_correct_loss_within_shown`, `a_w_on_gain_after_correction`, `x_d_holding_mismatch` | member validation names the code; B / B |
| Blocked by the agreement | `a_g_disagrees`, `x_g_sign_flipped`, `x_bw_g_omits_w`, `x_basis_row_is_corrected`, `a_same_sale_both_terms` | `amounts-check (blocked, DEPENDENCY_INVALID, [])`; B / B |
| Blocked by a duplicate | `x_dup_*`, `a_duplicate_on_direct`, `t2_stage4_keep_covered` | `IDENTITY_EXCLUSIVITY_COLLISION`; B / B |
| Rejected before a run | `a_corrected_basis_missing`, `x_remove_sale_keep_rows` | `FindingModelError` |

**Precedent check.** The agreement copies the f8949-boxes-cf pair, which
copies the Form 1099-K pair. The property the consumers care about is one
result per sale and one per return. Every saturated run records exactly
one `amounts-check` row per term. The `check_closes_first` change adds a
`when` to the sales path only. That property was never tested by either
precedent, because neither had a stale-closure case that reached the check
first. It is measured here instead: `x_q3_*` and `t1_stage1` block
`SOURCE_SET_UNCLOSED` and ask Q3, and every closed run is unchanged. The
join of a sale to its rows uses all three entity keys, so a reused
transaction entity cannot cross-join (`x_shared_transaction_*`).

**Presentation-model probe.** The sentences are in `field_sentences`, and
each case's blocked reasons are in `field_reasons`.

| Field | Path (case) | Value | Explanation | Reason or question shown |
| --- | --- | --- | --- | --- |
| Line 1b v3 (changed) | published (`a_high`) | 6000 | "...is your short-term gain or loss from Form 8949 box A, proceeds minus basis plus adjustments. Column (g) carries any wash-sale adjustment and any code B correction of a wrong reported basis." | — |
| | `computed_zero` (`x_bw_w_equals_correct_loss`, `d_low`) | 0 | "...is zero because your Form 8949 box A proceeds, basis, and adjustments net to zero." | — |
| | `closure_backed_zero` (`wage_q3_no`) | 0 | "You said you have no short-term Form 8949 box A sales with a wash-sale adjustment or a wrong reported basis, so..." | — |
| | blocked (`a_adjustment_row_missing`) | — | "...waiting for your Form 8949 box A proceeds, basis, and adjustments, including the column (g) correction of any sale whose reported basis is wrong, and your answers about those sales." (`field_words`) | "What is the column (g) adjustment for each short-term sale you recorded whose reported basis is wrong: the basis shown minus the correct basis, plus any wash-sale loss disallowed?" |
| | blocked (`x_q3_no_late_both_terms`) | — | same | Q3 |
| | blocked (`a_holding_mismatch`, `a_no_correction`, `x_bw_w_exceeds_correct_loss_within_shown`) | — | same | The family's constraint meaning, for example "The correct basis equals the basis the Form 1099-B shows, so there is nothing to correct. Record the sale as a sale with no adjustment (or with code W only)." |
| Line 8b v3 (changed) | published (`d_low`), zero (`a_high`), `cbz` (`wage_q3_no`), blocked (`x_d_basis_row_missing`) | 3000 / 0 / 0 / — | The long-term box D forms of the above | "What basis does your Form 1099-B show for each long-term sale you recorded whose reported basis is wrong?" |
| Lines 1a, 2, 3, 8a, 9, 10 (producers changed, fields unchanged) | as on v80 | — | Unchanged v80 sentences | `m_a_and_b_q1_no` asks Q1 on lines 3 and 10; `a_ic3_unanswered` asks IC3 on lines 1b, 3 and 10 |
| Form 8949 attachment v5 parts (new) | published (`a_high`, `a_bw`) | — | "Part I box A column (d), code B: short-term proceeds"; "... column (e), code B: short-term basis shown on Form 1099-B"; "... column (g), code B: short-term basis correction plus any wash-sale adjustment"; and the Part II box D forms | — |

## Presentation limits (not correctness)

Each of these returns is refused: Form 1040 and both attachments block.
On each, the line shows its blocked sentence and no question, because
`block` carries no missing list (the f8949-boxes-cf Decision 4
mechanism):

- a code B sale beside Form 8949 "yes" (`a_8949_yes`, `t1_stage3`,
  `t2_stage3`). The filer must change the Form 8949 answer, and nothing
  on the page says so;
- a Q3 "yes" with nothing recorded (`q3_yes_nothing_recorded`,
  `m_q3_yes_nothing_*`);
- an IC3 "no" (`a_ic3_no`, `m_d_ic3_no`);
- an amount row that disagrees with its sale or with the worksheet
  (`a_g_disagrees`, `x_g_sign_flipped`, `x_bw_g_omits_w`,
  `x_basis_row_is_corrected`, `x_corrected_basis_changed_g_stale`,
  `a_same_sale_both_terms`);
- two sales sharing one transaction entity with a row missing
  (`x_shared_transaction_missing_g`);
- a duplicate entry (`x_dup_*`, `a_duplicate_on_direct`). The collision
  code has no declared meaning, so no sentence is shown.

Other limits P0 already recorded stand: no column (f) letters (Decision
4); Path B still required (`a_path_b_unanswered`); one filer only, so no
married-filing-separately limit, Schedule D Tax Worksheet or carryover;
the code W amount not checked against Form 1099-B box 1g; and the loader
entries patched in process.

## Owner questions

1. **Four inherited v80 neighbour behaviours** (artifact 5,
   `neighbour_probes`), none caused by this design:
   - a code W or box B row with zero proceeds does not require Form 8949
     (and, for code W, not Schedule D either);
   - one transaction recorded on two v80 families of different terms is
     counted twice;
   - a covered sale flagged `taxpayer_side_adjustment` "yes" still
     publishes the broker's gain.

   The code B families are repaired for the first two. Fixing the v80
   families would change returns v80 computes. Park them, or take one in
   Track 1 as a v81 change to returns v80 computes?
2. **Extend the accepted presentation limit** (f8949-boxes-cf Decision 4)
   to the code B block-only paths above. The alternative is to fund the
   `rule-artifact` successor whose `block` names what it waits on.
3. **Path B "yes" beside a code B row** decides nothing (`x_path_b_yes`,
   `t3_stage2`, both identical to the honest answer). Track 0 accepts this
   on the f8949-boxes-cf precedent (`t2_stage3_old_ic_no`). The
   alternative is to refuse it with one more arm in each column (h) rule,
   with no question shown.
