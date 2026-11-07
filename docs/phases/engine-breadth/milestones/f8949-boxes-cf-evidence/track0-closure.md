# Track 0 adversarial closure: sales without a Form 1099-B

Evidence for `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate", over
Decisions 1-3 in `docs/phases/engine-breadth/milestones/f8949-boxes-cf.md`.
Charter: `docs/reviews/f8949-boxes-cf/charter-track0.md`. Scratch prototype
only. No production, test or content edits. Synthetic `demo.*` findings.

Source ref: `eb02b548` on `milestone/f8949-boxes-cf-2025`.

## How the evidence was built

- `cf_prototype.py` builds the scratch core v80, registry v78 and release
  v78 from v79 in a temporary copy of the content tree, with
  `tools.package_successor`. Members are in `cf-prototype-rules/`. The final
  build has 61 member edits (43 adds, 18 replacements). It reports no
  inherited inconsistency, and no file that already existed changed.
- `track0.py` runs every case through `live_coordinate_run` and writes
  `track0-output.json`. It covers:
  - the 20 P0 cases and 51 Track 0 cases on v80;
  - every v79 return P0 ran (46), plus 4 Track 0 v79 returns, on v79 and
    again on v80;
  - 20 cases rebuilt on the **decided design** (Decisions 1-3 with none of
    the repairs below), to show each counterexample a repair fixes.
- Every completed run stopped `saturated` and passed
  `validate_presentation_model`, with no duplicate form-field id. Two cases
  fail before a run, as on v79: `c_basis_object_missing` and
  `d3_b_orphan_basis` (`FindingModelError`).
- The 20 P0 cases still match the hand values in `cf_prototype.py`
  (`HAND`, `BLOCKED`).
- `cf-prototype-output.json` is P0's record of the design before Decision 3.
  `track0-output.json` supersedes it for every case it reran.

Case names below are keys of `track0-output.json`:

- `v80_cases`: the final design;
- `decided_design`: the design before the repairs;
- `v79_returns_on_v80`: each v79 return, on v79 and then on v80.

In the tables, `cbz` is `closure_backed_zero`, `cz` is `computed_zero`,
`B` is blocked, and `gi` is `guard_inapplicable`. TI is Form 1040 line 15
and tax is line 16.

**Result: all six artifacts PASS on the changed prototype.** Track 0 found
seven counterexamples on the decided design, listed in the table below.
Six are fixed by content repairs. The seventh, a duplicate entry, is put
outside the class by the in-class answer. No engine, schema or recording
change is needed. Four of the fixes also change returns v79 computes, and
those changes need the owner's acceptance; see "Owner questions".

## Design changes made to the prototype

**Decision 3** is added as decided:

- lines 2 and 9 v2 move to `rule-artifact.v15` and take `require_paired`
  for proceeds and basis, on the `transaction` key;
- four input questions ask for a missing box B or E proceeds or basis
  amount.

Track 0 then found the counterexamples below on that decided design. Each
repair is a switch in `cf_prototype.REPAIRS`, and all are on.

| Repair | Counterexample on the decided design | After the repair |
| --- | --- | --- |
| `nc_count_pairing` | `d3_b_shared_transaction`: two box B sales on different statements reuse one transaction entity; the second has no basis row. `require_paired` reads one key, so the first sale's basis row covers it. Line 2 publishes 4000 (true value −1000), TI 38250, tax 4355 | Lines 2 and 9 also need as many proceeds rows and as many basis rows as sale objects. The ADR-0082 presence pairs refuse a row without its own sale (`d3_b_orphan_basis`: `FindingModelError`), so equal counts mean each sale has its own rows. Line 2 blocks |
| `f8949_reads_lines_2_9` | `d3_b_basis_missing`: line 2 blocks, but the Form 8949 attachment **publishes** (its v3 requirement reads neither line 2 nor line 9) | The attachment requirement reads lines 2 and 9. Both attachments block |
| `amounts_agree` | The line reads the amount rows. The code W, loss and holding-period checks read the sale object. Nothing compares the two. `w_c_scalar_only_on_gain`: a box C gain with a 500 wash row publishes line 3 = 4500. `w_c_amounts_disagree`: the object says a 2000/8000 loss, the rows say 6000/2000; line 3 = 5000. `w_c_object_wash_no_row`: W 1000 on the object with no row gives line 3 = −3000 (true −2000). `w_b_scalar_only_on_gain`: same on box B, line 2 = 4500, and v79 does the same (`t0_b_w_scalar_only_on_gain`, v79 TI 38750, tax 4415) | For each sale type, two rules. A per-sale rule (the sale object is the subject) publishes `agree` when each present row equals the object's amount, and when a wash row exists exactly when the object's wash amount is nonzero. A return-level selection rule publishes 0 when every sale agrees or none is recorded, and blocks otherwise. Lines 2, 3, 9 and 10 require it. The shape is the Form 1099-K `statement-loss-reason` / `unresolved` pair. All four cases block. A missing row is not compared, so the line's `require_paired` still asks for it |
| `q1_unbacked_yes` | `m_yes_nothing_no`: the v79 noncovered answer "yes" with nothing recorded publishes the wage return (34250 / 3875). v79 does the same (`t0_q1_yes_nothing`). This is the check P0 put on lines 3 and 10 for the new question, missing for the v79 one. `m_f_q1_yes_nothing` is the same with a box F sale | Lines 3 and 10 are zero only when the v79 answer is "no" or a box B or E sale is recorded. The check sits on lines 3 and 10, not 2 and 9, because reading the other term's subtotals on line 2 or 9 turns their `closure_backed_zero` into `computed_zero`. Its sentence would then say "your box E proceeds... net to zero" on a return with no box E sale (measured on `lt_gain` and `st_loss` before the move) |
| `old_ic_backed` | `m_no_no_8949no_old_ic_yes`: Form 8949 "no", Path B "no", v79 in-class "yes", both group questions "no", nothing recorded. Publishes the wage return. v79 does the same (`t0_8949no_old_ic_yes_q1_no`) | The v79 in-class "yes" admits a Form 8949 "no" on lines 3 and 10 only beside a v79 "yes". Blocks |
| `sale_needs_8949_no` | `m_c_8949_yes`: a box C sale beside Form 8949 "yes" (no Form 8949 transactions). **Form 1040 publishes** 31250 / 3515 while the Form 8949 attachment blocks on Path B. `m_b_8949_yes` and v79 do the same for box B (`t0_b_loss_8949_yes`). `t1_stage3` reaches it in the late-member trace | Lines 2, 3, 9 and 10 publish a recorded sale only beside a Form 8949 "no". All block |
| In-class proposition | `dup_b_and_c_ic_yes`: one sale entered on box B and again on box C is counted twice (line 7 −12000). The identities share no key, so content cannot detect it (Decision 4) | The new in-class fact and question now say "each sale entered only once", under the one box its statement gives it. The "no" refuses it (`dup_b_and_c_ic_no`: lines 3, 7 and Form 1040 blocked). A "yes" with a duplicate is a false answer, like any false attestation |

The three-check design of lines 3 and 10 is unchanged otherwise. The blocked
sentence of the line 3 and line 10 fields now names "sales whose basis was
not reported" and "Form 8949 to agree with the sales you recorded".

## 1. Authority-lifecycle table

**PASS.** Each row names the cases that would fail if the row were wrong.

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| `f8949.no1099b-{st,lt}-txn` (sale object) | One short- or long-term sale of securities with no Form 1099-B or substitute statement: net proceeds, basis, holding period, wash-sale amount | One sale entity (`tax.us.f8949-sale`) and tax year, as a member of its family horizon | The filer's assertion; the family horizon; the new question's closure | Correction (free supersession) or member removal, which displaces lines 3 and 10 through their pins. A holding period that does not match the term blocks the line (`f_holding_mismatch`). Code W on a gain blocks (`c_code_w_on_gain`) |
| `f8949.no1099b-{st,lt}-txn.{proceeds,basis}` | The sale's net proceeds (gross minus selling expenses) and basis, as amount rows | The same sale identity | The sale object (ADR-0082 presence pair: a row without its sale is rejected, as `c_basis_object_missing` and `d3_b_orphan_basis` show). Each row must equal the object (`amounts_agree`) | Correction of the row or the object. A missing row blocks and asks (`c_basis_missing`, `c_proceeds_missing`, `d3_c_two_sales_one_missing`). A row that differs from its object blocks (`w_c_amounts_disagree`) |
| `f8949.no1099b-{st,lt}-txn.adjustment` (code W on boxes C and F) | The nondeductible wash-sale loss, positive, no larger than the sale's own loss | The same sale identity | The object's `wash_disallowed`, checked by `CODE_W_ON_GAIN` and `ADJUSTMENT_EXCEEDS_LOSS`. The row must exist exactly when the object's amount is nonzero, and must equal it | Correction that makes the sale a gain (blocks, `c_code_w_on_gain`). A row on a sale whose object has none (`w_c_scalar_only_on_gain`), or the reverse (`w_c_object_wash_no_row`), blocks. `c_wash` computes −2000 |
| `f8949.no1099b-sold.source-closure` (the new question) | "Did you sell any stocks or other securities for which you did not receive a Form 1099-B or substitute statement?" | Keyed by tax year. Its authority is the eight box C/F family horizons named by `closure-mapping.f8949.no1099b` (v4) | `source-closure-mapping.v4` admission: "no" is closed-empty, "yes" holds until a later member | Free supersession (a new answer). A later member in any of the eight families makes a "no" stale (`late_member_after_no`, `t1_stage1`) and a "yes" stale (`q2_late_yes_stale`). Either way the page asks the question again. A "yes" with no box C or F sale recorded is refused (`q2_yes_nothing_recorded`, `m_no_yes_nothing`) |
| `schedule-d-boundary.form8949-in-class` (new in-class answer) | Form 8949 work beyond covered sales and code W is only boxes B, C, E and F: securities, each entered once under its one box, a basis you supply (net proceeds on C and F), at most a wash-sale adjustment | The return (tax year) | The filer's statement about all of the return's Form 8949 work | Free supersession only. It does not go stale on a later member: an in-class sale does not change its truth (`t1_stage3`, `t2_stage3`: answered after the sale, same result). It is read only when the new question is "yes" (guarded arm) and on the box C/F publishing path. A "no" refuses (`f_gain_new_ic_no`, `m_c_new_ic_no`, `dup_b_and_c_ic_no`) |
| `schedule-d-boundary.noncovered-in-class` (v79 in-class answer) | Only boxes B and E | The return | The filer's statement | Free supersession. It is false once a box C or F sale exists. v80 reads it only when the guarded arm is false, which means no box C/F sale is admitted, and on lines 3 and 10 only beside a v79 "yes" (`old_ic_backed`). `t2_stage3_old_ic_no` matches `t2_stage3` exactly, so after a box C sale the false "yes" decides nothing |
| `f1099b.noncovered-sold.source-closure` (v79 question) | "Did you sell any securities whose basis was not reported to the IRS?" | Tax year, over the eight v79 box B/E families | The v79 mapping, unchanged | As on v79 (`late_member_*`, `late_yes_*` reproduce v79 exactly). In addition, lines 3 and 10 now refuse a "yes" with nothing recorded (`q1_unbacked_yes`) |
| Lines 2 and 9 amount check (Decision 3) | Every box B or E sale has its own proceeds and basis rows | The v79 sale identity (broker, statement, transaction) | `require_paired` on `transaction` (asks the question), the count check (`nc_count_pairing`) and the per-sale agreement (`amounts_agree`) | A missing row blocks and asks (`d3_b_basis_missing`, `d3_e_proceeds_missing`, and the v79 `probe_e_*` returns). A row covered only through a reused transaction entity blocks (`d3_b_shared_transaction`) |

The `sale` key of a box C or F row is the whole identity apart from the tax
year. So `require_paired` on `sale` is exact for boxes C and F; only boxes
B and E needed the count check.

## 2. Empty/nonempty authority matrix

**PASS.** "8949" is `no-form8949-sources`. The harness wage return answers
it "yes". Q1 is the v79 group question; Q2 is the new one.

| Case | Family state | Q1 / Q2 / other answers | Expected | Lines 2, 3, 9, 10 | TI / tax, attachments |
| --- | --- | --- | --- | --- | --- |
| `m_no_no` | Both groups closed empty | no / no | Explicit zero, neighbour unchanged | cbz, cz, cbz, cz | 34250 / 3875; gi / gi |
| `m_no_no_8949no_pathb_yes` | Both closed empty | no / no; 8949 no, Path B yes | Zero: Path B is the covered-sales boundary (ADR 0061) and admits it | cbz, cz, cbz, cz | 34250 / 3875; gi / gi |
| `m_no_unanswered` (`wage_q2_unanswered`) | C/F authority missing | no / — | Blocked, asks Q2 | cbz, B, cbz, B | B; B / B |
| `m_unanswered_no` | B/E authority missing | — / no | Blocked, asks Q1 | B, B, B, B | B |
| `m_yes_nothing_no` | B/E "yes", nothing recorded | yes / no | Refused | cbz, B, cbz, B | B; B / B |
| `m_yes_nothing_no_old_ic_yes` | Same, v79 in-class yes | yes / no | Refused | cbz, B, cbz, B | B |
| `m_no_yes_nothing` (`q2_yes_nothing_recorded`) | C/F "yes", nothing recorded | no / yes | Refused | cbz, B, cbz, B | B |
| `m_yes_yes_nothing` | Both "yes", nothing | yes / yes | Refused | cbz, B, cbz, B | B |
| `m_no_no_8949no` (`unrecorded_8949_no_only`) | Both closed empty | no / no; 8949 no, Path B no | Refused: 8949 "no" and nothing admits it | cbz, B, cbz, B | B |
| `m_no_no_8949no_old_ic_yes` | Both closed empty | + v79 in-class yes | Refused (`old_ic_backed`) | cbz, B, cbz, B | B |
| `m_no_no_8949no_new_ic_yes` | Both closed empty | + new in-class yes | Refused: the guarded arm needs Q2 yes | cbz, B, cbz, B | B |
| `m_b_yes_no` (`d3_b_loss`) | B nonempty, eligible | yes / no; v79 in-class yes | Computed | −6000, cz, cbz, cz | 31250 / 3515; published |
| `m_c_no_yes` (`c_loss`) | C nonempty, eligible | no / yes; new in-class yes | Computed | cbz, −6000, cbz, cz | 31250 / 3515; published |
| `m_bf_yes_yes` | B and F nonempty | yes / yes | Computed | −6000, cz, cbz, 4000 | 32250 / 3635; published |
| `mixed_abcf` | A, B, C short; F long | yes / yes | Computed | −500, 1500, cbz, 4000 | 40250 / 4115; preferential 4000 |
| `m_b_old_ic_no` | B nonempty, ineligible | v79 in-class no | Refused | B, B, cbz, B | B |
| `m_c_new_ic_no` (`f_gain_new_ic_no`) | C or F nonempty, ineligible | new in-class no | Refused | cbz, B, cbz, B | B |
| `m_b_q1_no_with_member` | B nonempty, Q1 "no" | no | Blocked, asks Q1 | B, B, cbz, B | B |
| `m_c_q2_no_with_member` | C nonempty, Q2 "no" | no | Blocked, asks Q2 | cbz, B, cbz, B | B |
| `m_e_yes_q2_yes_nothing` | E nonempty; C/F "yes" with nothing | yes / yes | Refused (check 2) | cbz, B, 4000, B | B |
| `m_f_q1_yes_nothing` | F nonempty; B/E "yes" with nothing | yes / yes | Refused (`q1_unbacked_yes`) | cbz, B, cbz, 4000 | B |
| `m_c_8949_yes`, `m_c_8949_yes_pathb_no`, `m_b_8949_yes` | Nonempty beside 8949 "yes" | | Refused (`sale_needs_8949_no`) | the sale's line B | B; B / B |

Hand values: B 2000/8000 is a −6000 loss limited to 3000, giving TI 31250
and tax 3515 (Tax Table row 31250-31300). B −6000 with F +4000 gives line 16
−2000, TI 32250 and tax 3635. The mixed case is P0's.

Each "Refused" row is refused by an answer, not computed partly: Form 1040
and both attachments block on every one. The neighbouring result on every
closed-empty, fully answered row is the wage return, 34250 / 3875.

## 3. Late-member trace

**PASS.** `attest → close → compute → add member → reclose → recompute`,
built stage by stage. Each stage is a fresh `live_coordinate_run` over the
act log at that point. "Unusable" means the next run neither reads nor
publishes it.

**T1: box F after a "no"** (`t1_stage0` to `t1_stage4`)

| Stage | Change | Result | What became unusable, and why |
| --- | --- | --- | --- |
| 0 | Wage return, Q2 "no" | 34250 / 3875; lines 3 and 10 cz; gi / gi | — |
| 1 | Add a box F sale 6000/2000 | Lines 3, 10, 15, 16, Form 1040 and both attachments block. The page asks Q2 | The Q2 "no" is stale: a member arrived after it (closed-empty no longer admits the families). Stage 0's zero lines 3 and 10, and everything from them, are not reproduced |
| 2 | Q2 "yes" | Still blocked; the page asks the new in-class question | The families are admitted again. Line 10's publishing path needs the new in-class "yes" |
| 3 | New in-class "yes" | Line 10 blocks; Form 1040 blocks; both attachments block | The Form 8949 "yes" from stage 0 is now contradicted by a recorded sale. `sale_needs_8949_no` refuses it. On the decided design this stage published Form 1040 at 38250 / 3875 with the Form 8949 attachment blocked (`decided_design.t1_stage3`) |
| 4 | Form 8949 "no", Path B "no" | Line 10 4000, 15 4000, 16 4000, 7a 4000, preferential 4000, 38250 / 3875; both published | — |

The new in-class answer did not need re-answering after stage 2. Its
proposition did not change, because the sale is in class.

**T2: box C after a computed v79-style return** (`t2_stage0` to
`t2_stage3`, plus `t2_stage3_old_ic_no`)

| Stage | Change | Result | What became unusable, and why |
| --- | --- | --- | --- |
| 0 | Box B 3000/3500; Q1 "yes"; 8949 "no", Path B "no"; v79 in-class "yes"; Q2 "no" | Line 2 −500, TI 33750, tax 3815; both published | — |
| 1 | Add a box C sale 2500/1000 | Line 3 and everything after blocks; the page asks Q2. Line 2 still −500 | The Q2 "no" is stale. The v79 in-class "yes" is now false, but nothing reads it yet |
| 2 | Q2 "yes" | Line 2 also blocks; the page asks the new in-class question | The guarded arm runs first and needs the new in-class answer, so line 2 no longer rests on the false v79 answer |
| 3 | New in-class "yes" | Line 2 −500, line 3 1500, line 7 1000, TI 35250, tax 3995; both published | — |
| 3b | `t2_stage3_old_ic_no`: v79 in-class corrected to "no" | Identical to stage 3 | Shows the false v79 "yes" decides nothing once the guarded arm holds |

Hand check: 1000 of short-term gain is ordinary, so TI is 35250 and tax is
3995 (Tax Table row 35250-35300).

**The other aggregate declarations:**

- Q2 "yes" goes stale on a later member (`q2_late_yes_stale`, asks Q2). It
  recomputes on a fresh "yes" (`q2_late_yes_reanswered`: F +4000 and C
  −6000, TI 32250, tax 3635).
- Q1's v79 traces (`late_member_unclosed`, `late_member_reopened`,
  `late_yes_stale`, `late_yes_reanswered`, `yes_then_no_with_member`) match
  v79 on every line v79 shows. The only difference is one more blocked line
  (line 7) on the three that v79 already blocks.
- The return-level amount check (`amounts_agree`) is recomputed from the
  current rows on every run. It holds no state that a later member could
  leave stale.

## 4. Claim reuse

**PASS.** Three claims are reused. One is not.

| Claim | Same real-world proposition | Same identity and lifecycle | Same scope and explanation |
| --- | --- | --- | --- |
| v79 group question `f1099b.noncovered-sold.source-closure` | Yes. The question text is unchanged. v80 reads "no" as "no box B/E sale", the same as v79's closed-empty admission. On lines 3 and 10 it also reads "yes" as "I sold such a sale", which is the question's literal meaning | Yes. Same fact type, version and tax-year key, free supersession. `closure-mapping.f1099b.noncovered` v1 and the eight family members are unchanged in v80: none is in the 18 replacements (`cf-prototype-rules/_members.json`). Staleness traces reproduce v79 | Yes. The same eight families. Its input question is unchanged |
| ADR-0061 boundary pair (`no-form8949-sources`, `no-other-form8949-adjustments`) | Yes. "8949 yes" = no Form 8949 transactions or adjustments; v80 refuses a recorded sale beside it, which is that meaning. "Path B yes" = no adjustment codes other than W, no multi-code rows, no basis-not-reported sources. v80 reads it only on the zero path of lines 3 and 10, as one admission of a Form 8949 "no", and never as admitting a recorded box C/F sale | Yes. Unchanged fact types, tax-year key, free supersession | Yes. The return-level scope; the bundle and question are unchanged |
| v79 in-class answer `noncovered-in-class` | Yes. "Only boxes B and E". v80 reads it only where no box C/F sale is admitted (the guarded arm comes first; `t2_stage3_old_ic_no`) and beside a Q1 "yes" | Yes. Unchanged fact type and lifecycle | Yes. v80 never widens it. The new in-class answer is a separate fact (P0 table, "the first column fails by construction") |
| Preferential-base gate | **Not reused.** `rule.selected-preferential-base` v8 is a successor that adds lines 3 and 10 to "Schedule D activity", as v7 added lines 2 and 9. Measured: `f_gain` 4000, `mixed_abcf` 4000, `c_loss` 0, `m_bf_yes_yes` 0 | — | — |

One reading is new: a v79 "yes" with no sale recorded no longer supports a
zero return. That narrows what the answer supports; it does not widen its
proposition. It does change a return v79 computes (owner question 1).

## 5. Neighboring-capability dependency diff

**PASS.**

**Prerequisites before and after.** On v79, a return with no sales needs
Q1 and the Schedule D boundary answers. On v80 it needs the same plus one
new answer, Q2 ("no"). No other new answer is read:

- the new in-class answer is read only beside Q2 "yes";
- the amount checks read only recorded rows.

Without Q2, all 50 v79 returns block Form 1040, and the 48 that run ask Q2.
The other two fail before a run, as on v79.

**Why Q2 is justified by Schedule D's own meaning.** A zero on Schedule D
lines 3 and 10 says no sale without a Form 1099-B exists. Under the closure
contract the v79 lines already follow (ADR 0084, one grouped closure answer
per group of families), a zero line rests on the closure of the families it
sums. Lines 2 and 9 need Q1 on every v79 return for the same reason
(`wage_unclosed` blocks on v79).

The v79 probe also shows why the generic Form 8949 answers are not enough:
`probe_c_unrecorded_*` publishes the wage return with a box C sale left out.

**Removing Q2 is not possible content-only.** On a return that answers Form
8949 "yes", Q2's "no" is logically implied. But admission reads only each
mapping's own closure fact (`_admit_group`). `collect` and `count` on an
unclosed empty family block, so lines 3 and 10 cannot be zero without Q2.
Deriving the closure from the Form 8949 answer would be an engine change.
This is the same cost v79 accepted for Q1 (noncovered-sales Track 0,
neighbouring-capability row).

**Returns v79 computes (28 of P0's 46, plus 4 Track 0 returns), with Q2
"no":**

| Group | Count | On v80 |
| --- | --- | --- |
| Identical: every line v79 shows and both attachment dispositions | 22 | The wage return; the eight current-core neighbours (`one_*`) and `one_finding`; covered-flag returns; box B/E gain, loss, wash, mixed and late-member returns; the probe's box B/E-recorded returns. Lines 3 and 10 are `computed_zero` 0 |
| Decision 2 (accepted): a Form 8949 "no" with nothing admitted | 4 | `boundary_no_without_member`, `probe_c_unrecorded_8949_no`, `_other_no`, `_all_no` block |
| Decision 3 (accepted): a box E sale missing an amount | 2 | `probe_e_basis_scalar_missing` (v79 40250 / 3875) and `probe_e_proceeds_scalar_missing` (v79 32250 / 3635) block and ask for the amount |
| New in Track 0: each a silent omission or wrong number on v79 | 4 | `t0_q1_yes_nothing` (Q1 "yes", nothing recorded); `t0_8949no_old_ic_yes_q1_no` (Form 8949 "no" admitted only by an unbacked v79 in-class "yes"); `t0_b_loss_8949_yes` (a box B sale beside Form 8949 "yes"; v79 published Form 1040 with Form 8949 blocked); `t0_b_w_scalar_only_on_gain` (a wash row on a box B gain; v79 TI 38750, tax 4415). All block. **Owner question 1** |

**Returns v79 already refuses:**

- 9 block one more Schedule D line, line 7 or 15. Lines 3 and 10 now read
  the box B/E subtotals, so a blocked box B/E sale blocks them too.
  `covered_both_boundaries_no` also moves its Form 8949 attachment from
  `guard_inapplicable` to `blocked`.
- Form 1040 stays blocked on all 9. Seven are otherwise unchanged.
- Two fail before a run, as on v79.

**Earlier cores are untouched:** the scratch build changed no existing file.

## 6. Integration surface

**PASS.** Bindings are from the built v80 package (`track0-output.json`,
`surface`; 919 members resolved). The per-run counts are over 89 saturated
runs (69 in `v80_cases`, 20 in `decided_design`).

| Consumer | Binding | Cardinality expected | Satisfied |
| --- | --- | --- | --- |
| Lines 2, 3, 9, 10 | One publisher each: `rule.schedule-d-line{2,9}` v2 and `line{3,10}` v1 (`rule-artifact.v15`). Read by line 7 v5 (lines 2 and 3), line 15 v7 (lines 9 and 10), line 7a v7, preferential base v8, Form 8949 attachment v4, Schedule D attachment v8 | Exactly one row per symbol on every path | Yes. Exactly one disposition row per publisher in all 89 runs, on the published, zero, blocked and guard-false paths |
| Line 7, line 15 | One publisher each. Read by line 16 (both) and the preferential base (line 15) | Exactly one | Yes, as above |
| Line 16, line 21 | `rule.schedule-d-line16` v2, `line21` v1, unchanged. Read by line 7a, line 21, preferential base | Exactly one | Yes |
| Form 1040 line 7a | `rule.form1040-line7a` v7 publishes `capital-gains.line7a-total`. Form field `form1040.line-7a`. Read by `form1040-line9`, `eic-investment-income`, `ss-benefits-worksheet` | Exactly one | Yes |
| Preferential base | `rule.selected-preferential-base` v8. Read by `form1040-line16`, `form1040-line7a`, `qdcg-worksheet.line-4`, `line-5` | Exactly one | Yes |
| Form 8949 attachment | `rule.attachment.f8949` v4 publishes `form8949.disposition`. Box C and F parts; requirement reads the C/F proceeds and basis subtotals and lines 2, 3, 9, 10 | Exactly one attachment per return | Yes: published 26, blocked 55, inapplicable 8 |
| Schedule D attachment | `rule.attachment.schedule-d` v8 publishes `schedule-d.disposition` | Exactly one | Yes: published 28, blocked 53, inapplicable 8 |
| Form fields | One field per line symbol: `schedule-d.line-2` v1, `-3` v1, `-7` v4, `-9` v1, `-10` v1, `-15` v4, `-16` v2, `-21` v2 | Exactly one field per symbol | Yes. No duplicate field id in any run |

**One built model per disposition path** (all `v80_cases`):

| Path | Model | Attachments (Form 8949 / Schedule D) |
| --- | --- | --- |
| Box F gain published | `f_gain` (line 10 4000, 38250 / 3875) | published / published |
| Box C loss published, line 21 limit | `c_loss` (line 3 −6000, 21 3000, 7a −3000) | published / published |
| Box C code W | `c_wash` (line 3 −2000) | published / published |
| Mixed boxes | `mixed_abcf`, `m_bf_yes_yes`, `t2_stage3` | published / published |
| Zero, no sales | `m_no_no` (lines 3 and 10 cz; 2 and 9 cbz) | gi / gi |
| Zero line beside a sale of the other term | `f_gain` line 3 cz; `c_loss` line 10 cz | published / published |
| Blocked, asks a question | `c_basis_missing`, `d3_b_basis_missing`, `m_no_unanswered`, `f_gain_new_ic_unanswered` | blocked / blocked |
| Refused by an answer | `f_gain_new_ic_no`, `m_b_old_ic_no`, `dup_b_and_c_ic_no`, `unrecorded_out_of_class` | blocked / blocked |
| Blocked by a sale's checks | `c_code_w_on_gain`, `f_holding_mismatch`, `w_c_amounts_disagree` | blocked / blocked |
| Rejected before a run | `c_basis_object_missing`, `d3_b_orphan_basis` (`FindingModelError`) | — |

**Precedent check.** The amount check copies the Form 1099-K pair:
`rule.f1099k-statement-loss-reason`, per subject, and
`rule.f1099k-unresolved` v3, a return-level selection over
`reads_subject_results` with `collect_categorical_all_equal`. The property
the consumers care about here is one result per sale and one result per
return. That holds: in each of the 69 saturated v80 runs, each of the four check
rules records exactly one row (265 published, 11 blocked; the
`amounts-check` rows in `dispositions`). The sale here is a
source-family member object; for 1099-K it is a statement amount. The
join is by identity-key names, and on boxes B and E it uses broker,
statement and transaction together, so a reused transaction entity does not
cross-join (`d3_b_shared_transaction`, `w_b_scalar_only_on_gain`).

**Presentation-model probe.** Each case's disposition, value and reasons
are under `v80_cases.<case>.result.fields`. The sentence for each field and
disposition is under `field_sentences`.

| Field | Path (case) | Value | Explanation sentence | Blocked reason / question shown |
| --- | --- | --- | --- | --- |
| Line 3 (new) | published (`c_loss`) | −6000 | "...is your short-term Form 8949 box C gain or loss, proceeds minus basis plus adjustments." | — |
| | computed_zero (`m_no_no`) | 0 | "...is zero. Either no short-term sale you received no Form 1099-B for is recorded and your Form 8949 answers confirm it, or your box C proceeds, basis, and adjustments net to zero." | — |
| | blocked (`c_basis_missing`) | — | "...has no value yet. It waits for your answers about sales you received no Form 1099-B for, sales whose basis was not reported, and Form 8949 to agree with the sales you recorded, or for each recorded short-term sale of that kind to have its proceeds and basis and pass its checks." | "What is the basis of each short-term sale you recorded without a Form 1099-B?" |
| | blocked (`f_gain_new_ic_unanswered`) | — | same | The new in-class question |
| | blocked (`q2_yes_nothing_recorded`, `w_c_amounts_disagree`) | — | same | None: `block` carries no missing list (Decision 4) |
| Line 10 (new) | published (`f_gain`) | 4000 | "...long-term Form 8949 box F gain or loss..." | — |
| | computed_zero (`m_no_no`) | 0 | the long-term form of the line 3 sentence | — |
| | blocked (`f_holding_mismatch`) | — | as line 3 | "The holding period does not match this short-term or long-term family." |
| Line 2 (producer changed) | published (`d3_b_loss`) | −6000 | unchanged v79 sentence | — |
| | closure_backed_zero (`m_no_no`) | 0 | unchanged v79 sentence | — |
| | blocked (`d3_b_basis_missing`) | — | unchanged v79 sentence | "What is the basis of each short-term sale you recorded whose basis was not reported to the IRS?" |
| | blocked (`d3_b_shared_transaction`) | — | unchanged | None (Decision 4 mechanism) |
| Line 9 (producer changed) | blocked (`d3_e_proceeds_missing`) | — | unchanged | "What are the proceeds of each long-term sale you recorded whose basis was not reported to the IRS?" |
| Line 7 v4 (sentence changed) | published (`c_loss`), zero (`m_no_no`), blocked (`c_proceeds_missing`) | −6000 / 0 / — | "Schedule D line 7 adds lines 1a, 1b, 2, 3, and 6." / "...add to zero." / "...waiting for whichever of lines 1a, 1b, 2, 3, and 6 is still open." | Blocked: "What are the net proceeds of each short-term sale you recorded without a Form 1099-B?" |
| Line 15 v4 (sentence changed) | published (`f_gain`), zero (`m_no_no`), blocked (`d3_e_basis_missing`) | 4000 / 0 / — | "...adds lines 8a, 8b, 9, 10, 13, and 14." and the matching zero and blocked forms | Blocked: the box E basis question |

## Presentation limits (not correctness)

Each of these returns is refused. Form 1040 and both attachments block. On
each, the page shows the line's blocked sentence and no question, because
`block` carries no missing list (P0 "Engine, schema, or recording change"):

- a Q2 "yes" with nothing recorded (Decision 4, accepted);
- a Q1 "yes" with nothing recorded;
- a Form 8949 "no" that nothing admits (with Path B "no", the page shows
  the new in-class question, which alone cannot admit it);
- a sale beside a Form 8949 "yes";
- a box B/E row covered only through a reused transaction entity;
- amount rows that disagree with their sale.

Decision 4 accepted the first. The others use the same mechanism. Showing
a question would need a `rule-artifact` successor whose `block` names what
it waits on (owner question 2).

Decision 4's other items:

- **Duplicate entry.** Now refused by the in-class "no" (see the design
  changes above).
- **Married filing separately and the 2026 carryover.** Not exercised.
  Line 21 v1 is unchanged and reads `filing_status`; this design does not
  touch it. That is untested neighbour behaviour, not a counterexample this
  evidence records.

## Owner questions

1. **Accept four more v79-computed returns that now block.** These are in
   addition to the Decision 2 and 3 sets, and each was a silent omission or
   a wrong number on v79:
   - `t0_q1_yes_nothing`;
   - `t0_8949no_old_ic_yes_q1_no`;
   - `t0_b_loss_8949_yes`;
   - `t0_b_w_scalar_only_on_gain`.

   None is a pinned v79 test expectation. Track 1 should check the
   current-core expectations for these patterns.
2. **Extend Decision 4's accepted presentation limit** to the five other
   block-only paths listed above, or fund the `rule-artifact` successor
   that lets `block` name a question.
3. **Q2 on returns that answer Form 8949 "yes".** The answer is logically
   implied there, and asking it is the price of closure by each mapping's
   own fact, as for Q1 on v79. Removing it would be an engine change.
