# Review: broker basis corrections (Form 8949 code B), core v81

Reviewer: fresh reader, author-independent.
Charter: `docs/reviews/f8949-code-b/charter-review.md` @ (removed at closeout).
Object: `milestone/f8949-code-b-2025` at (removed at closeout).
The Orientation Block SHA matches `git rev-parse HEAD`. It is diffed against
`github/main`. After `git fetch`: 0 behind, 15 ahead. PR #264 is open as a
draft and has not merged.
Sources read: the plan; P0; the Track 0 closure; `codeb_prototype.py` and
`codeb_track0.py` (case builders, hand values and checks); the new and
replaced content members; `packages/tax/loader.py`; both new test modules;
`expected.json`. Governance was not read.

Method: I loaded `tests/test_code_b_sales_v81.py::build_world` and ran
cases on the published core v81 / registry v79 / release v79 through
`codeb_probe.execute`, which calls `live_coordinate_run` and reads the
presentation model. I added a summarizer that reads the Form 8949 parts'
tie-outs and the Schedule D field text. That covered 6 charter cases, 10
cases of my own, and 2 of them repeated on v80. All data is synthetic
`demo.*`. Scratch scripts stayed in the session scratchpad. Nothing was
written to the repo, and `git status` is clean. I did not run `pytest`.

## Findings, by consequence

### B1. Blocking: a covered direct sale with zero proceeds publishes Form 1040 line 7a as 0 beside a Schedule D loss

- **Where.**
  - `packages/content/tax/2025/attachment.schedule-d.v9.json:276`: the
    requirement subtotals read only `covered-st/lt-proceeds-subtotal` and
    `line-1a/8a-gain` (`strictly_greater_than` 0) for the direct families.
  - `rule.form1040-line7a.v7.json:17-18,34`: the Schedule D activity test
    reads the covered proceeds subtotals and lines 1b, 8b, 2, 3, 9 and 10.
    It never reads lines 1a or 8a.
- **Violated claim.** Decision 6, patterns 1 and 2 ("a zero-proceeds row
  requires its attachments") are said to be closed, and the charter asks
  whether any honest answers publish a wrong number on a recorded sale. They
  do. The pattern is closed for code W and box B/E, but not for the line
  1a/8a families.
- **Reproduction.** A v80-shaped return with Q3 "no", Q1 "no" and Q2 "no",
  and one covered box A sale on `f1099b.covered-st`: proceeds 0, basis
  500, every flag "no". This is `codeb_track0.sale_on(a, "covered", "st",
  0.0, 500.0, …)` under `DIRECT`. On v81:
  - Schedule D line 1a is (500), line 7 (500), line 16 (500), line 21 500.
  - Form 1040 line 7a is `computed_zero` 0, line 15 is 34250 and line 16
    is 3875.
  - Both attachments are `guard_inapplicable`.

  The box D variant has the same result (line 8a (500)). By hand, line 7a
  should be (500), taxable income 33,750 and tax 3,815. The published return
  overstates tax by $60 and contradicts its own Schedule D. v80 gives exactly
  the same result, so the defect is inherited.
- **Consequence.** A wrong published Form 1040 from honest answers (semantic).
- **Fix (content only, as Decision 6 was).**
  - Add per-term covered direct counts (or the covered basis subtotals) to
    the Schedule D attachment requirement. Use the same count pattern the
    W and B/E fixes use.
  - Add a successor to line 7a that also treats `line-1a-gain != 0` and
    `line-8a-gain != 0` as Schedule D activity.
  - Pin both terms as Decision 6 probes.

  If the owner would rather park it, record it as a known limitation that
  affects correctness. The plan currently says "none".

### B2. Blocking (mechanical gate): `quick` is red on HEAD

- **Where.** PR #264, run 42431818760, job `quick`:
  `tests/test_incremental_lattice.py::test_speculative_refusal_then_retry_and_gated_retraction_are_atomic`
  exceeded the fast-lane time limit (7.2s > 3.0s). The branch did not
  touch this test.
- **Context.** `github/main` at `dd81de67` is red on the sibling test
  `test_construction_count_is_delta_not_repeated_full_product[1]`. This
  branch moved that sibling to the live lane (removed at closeout), and the next
  slow test in the same module now trips the limit. The candidate is not
  `READY` while a required gate is red.
- **Fix.** Make this test fast, or mark it `live` with the same comment as
  its sibling. Do not raise the limit. Then rerun `verify` on the exact head.

### S1. Should-fix: lines 1b and 8b say "net to zero" when the term has no sales

- **Where.**
  `packages/content/tax/2025/schedule-d.line-1b.form-field.v3.json:26` and
  `schedule-d.line-8b.form-field.v3.json:26`.
- **Reproduction.** On `a_high`, line 8b is `computed_zero` with the
  explain "…is zero because your Form 8949 box D proceeds, basis, and
  adjustments net to zero". On `d_low`, line 1b says the same for box A.
  Neither return has any sale in that box. The grouped Q3 "yes" makes the
  empty term compute zero instead of `closure_backed_zero`, a state v80
  never reached.
- **Consequence.** In the two most common code B shapes (a code B sale in
  only one term), the explain sentence is not true of its rule's state
  (presentation).
- **Fix.** Reword `computed_zero` to cover both cases, for example: "…is
  zero: you have no box A sales of these kinds, or their proceeds, basis
  and adjustments net to zero." Both fields are new in this milestone.

### S2. Should-fix: the line 1b/8b blocked text says "waiting for your answers" when an answer or a check has refused the sale

- **Where.** `schedule-d.line-1b.form-field.v3.json:34` and
  `schedule-d.line-8b.form-field.v3.json:34`.
- **Reproduction.** In `a_ic3_no` (IC3 answered "no"), `a_g_disagrees`
  (column (g) row 2000 against a worksheet value of 3000) and
  `x_dup_covered_st`, line 1b is blocked with no reason sentence and no
  question. The only text is "…It is waiting for your Form 8949 box A
  proceeds, basis, and adjustments, including the column (g) correction…,
  and your answers about those sales."
  - Every amount and answer is recorded, so nothing is being waited for.
  - Unlike line 1a, the text has no "or for each sale recorded there to
    pass its checks".
- **Consequence.** The reason is non-empty but not true for refused
  states. Decision 7 parks the missing question; it does not license an
  untrue sentence.
- **Fix.** Add the line 1a clause and the refusal:
  "…or for each sale recorded there to pass its checks (its column (g)
  must equal the basis shown minus the correct basis plus any wash-sale
  loss disallowed). A sale your answers place outside this return, or one
  with an adjustment you make yourself…, is outside what this return
  computes."

### S3. Should-fix: the new line 8a field keeps internal jargon

- **Where.** `packages/content/tax/2025/schedule-d.line-8a.form-field.v2.json:22,26,30`.
- **Reproduction.** Every `a_high` and `d_low` page shows, for line 8a: "A
  current derived finding publishes a zero because the proceeds and basis
  families are attested closed on their current horizons with no recorded
  members." This milestone's line 1a v3 says the same thing in plain words
  ("You said you have no short-term sales reported directly on Schedule
  D…").
- **Fix.** Rewrite the `published_value`, `computed_zero` and
  `closure_backed_zero` explains in v2 to match line 1a v3's wording.

### S4. Should-fix: the blocked text on lines 1a, 8a, 1b and 8b now contradicts what the return can compute

- **Where.** `schedule-d.line-1a.form-field.v3.json:34` (and the 8a, 1b and
  8b fields): "A sale with an adjustment you make yourself … is outside
  what this return computes."
- **Mechanism.** A covered sale flagged `taxpayer_side_adjustment` "yes" is
  often exactly a basis correction. That is what this milestone computes,
  as a code B sale (`n_covered_tsa_yes_no8949`).
- **Fix.** Name the route: "…outside what this return computes, unless the
  adjustment corrects a wrong basis the Form 1099-B reported; record that
  sale as a sale whose reported basis is wrong."

### S5. Should-fix: Decision 6 pattern 4 reads one of five flags that the same record says need different treatment

- **Where.** `rule.f1099b.covered-st-txn.admission.json:22-35` (and the
  lt, w-st and w-lt versions) read only `taxpayer_side_adjustment`. No
  rule in the package reads `ordinary_indicated`,
  `box_1f_market_discount`, `qof_indicated` or
  `collectibles_or_special_rate`. ADR-0052 Decision 1 lists all five in the
  same eligible-sale predicate.
- **Reproduction.** On v81 with Q3 "no", one covered sale (proceeds 10000,
  basis 7000) and one flag "yes", every case publishes:
  - `collectibles_or_special_rate` "yes" on a box D direct sale: line 8a
    3000, preferential base 3000, line 16 3875. The 28% gain should be
    taxed at 12% here, giving 4235, so the return understates tax by $360.
  - `qof_indicated` (lt), `box_1f_market_discount` (lt) and
    `ordinary_indicated` (st) "yes" behave the same way.
  - v80 gives the same result for the collectibles case.
- **Mitigation.** Collectibles and QOF also contradict the filer's own
  `no-lines-18-19-sources` and `no-1099da-or-qof` answers, which the
  preferential base reads, so for those two this is a false attestation the
  engine could catch. Ordinary and market discount have no such answer.
- **Fix.** Have the same admission rule refuse when any of the five flags
  is "yes", through the existing yes/no parameter. Or have the owner park
  the other four explicitly, with Decision 6's reasoning.

### S6. Should-fix (evidence): the table does not pin the Form 8949 code B columns

- **Where.** `tests/test_code_b_sales_v81.py:183`: `projection` pins lines,
  attachments, questions, reasons and rows, not the Form 8949 parts.
- **Consequence.** A successor that put the correct basis in column (e)
  and 0 in (g) would keep column (h) and every pinned line unchanged.
  `x_basis_row_is_corrected` catches that only by way of the amount check,
  not on the form.
- **Fix.** Add the Form 8949 parts' tie-out text to the projection for the
  publishing cases and regenerate. The values I read (below) are the
  expected ones.

### S7. Should-fix (CI cost): 51 of the 135 v80 runs duplicate another run's v81 projection

- **Where.** `tests/test_code_b_sales_v81.py:112` runs every v80 return on
  v81: about 252 coordinator runs at about 6 CPU-s each in steady state,
  roughly 25 CPU-minutes.
- **Measurement.** Grouping `expected.json` by the v81 projection:
  - **v80 group.** 84 distinct projections for 135 runs, so 51 runs are
    redundant. One group has 15 wage-only answer shapes (`v80_m_no_no_8949no`,
    `v80_m_yes_nothing_no`, …). Another has 8 single non-capital findings
    (`carried_one_mortgage`, `carried_one_exempt_dividend`, …) that never
    reach a code B or Decision 6 path.
  - **Track 0 cases.** 30 duplicates by projection, but most are deliberate
    lifecycle equivalences (`t2_stage4` = `a_high`, `x_path_b_yes` =
    `a_high`). Keep those.
- **Fix.** In the v80 group, keep one return per distinct v81 projection
  plus the five `ATTACHMENT_ROW_CHANGES`, and list the dropped names with
  the name they share a projection with, as `DUPLICATES` does. This saves
  about 5 CPU-minutes and about a third of the v80 group's share of the
  fixture.

### N1. Note: a false in-class "yes" beside a box C duplicate publishes a doubled gain

`x_dup_box_c_ic3_yes` publishes line 15 46250 and line 16 5315 (6000 code
B plus 6000 box C, on one transaction). The two families share no identity
key, so content cannot see the duplicate, and the IC3 "yes" is false
("entered only once"). This is accepted as a false attestation, as the
Track 0 closure records. Measured, not a defect.

### N2. Note: the IC3 question is one sentence of about 80 words

`input-question.schedule-d-boundary-form8949-code-b-in-class.json:9`. Its
words are true to the proposition, with one omission: the proposition's
"under the one box its statement gives it" becomes only "entered only once".
It is not plain. Consider two sentences, or a short list of the two kinds of
sale.

### N3. Note: Q3's wording is ambiguous

`input-question.f1099b-code-b-sold.json:9`: "…report to the IRS a cost or
other basis for a sale that is wrong" can be read with "wrong" applying to
the sale. Suggested: "…show a cost or other basis, reported to the IRS,
that is wrong?" The meaning is unchanged; the test pins the question and
the title together.

### N4. Note: refusals of a duplicate on lines 2 and 9 do not name the duplicate

In `n_dup_b_and_covered_lt` and `n_dup_e_and_covered_st`, lines 2 and 9
show only "…or for a recorded short-term sale of that kind to pass its
checks." This is true, and those fields were not successored. Line 8a or
1a publishes the other copy while Form 1040 blocks, so nothing wrong is
published.

### N5. Note: the v80 side of the table is regenerated, not rerun in CI

`test_every_v80_return_computes_the_same_on_v81`
(`tests/test_code_b_sales_v81.py:288`) checks only the committed table's
stored v80 differences. The live tests rerun v81 alone. This is acceptable,
because v80 is immutable and older modules pin it. But the claim rests on
regenerating the table, and the tests also depend on harness code under
`docs/`.

## Answers to the charter

1. **Tax correctness.** All values agree. Taxpayer is single, wages 50,000,
   standard deduction: taxable income 34,250 before capital gains, tax 3,875
   (Tax Table midpoint, rounded). Results from the real coordinator on v81:

   | Case | 8949 (d) / (e) / (g) | (h) | Schedule D | 1040 7a / 15 / 16 |
   | --- | --- | --- | --- | --- |
   | `a_high`, A: 10000, shown 7000, correct 4000 | 10000 / 7000 / 3000 | 6000 | 1b 6000, 7 6000, 16 6000 | 6000 / 40250 / 4595 |
   | `d_low`, D: 6000, shown 2000, correct 3000 | 6000 / 2000 / -1000 | 3000 | 8b 3000, 15 3000, 16 3000; pref 3000 at 0% | 3000 / 37250 / 3875 |
   | `a_gain_to_loss`, A: 5000, shown 3000, correct 9000 | 5000 / 3000 / -6000 | -4000 | 1b -4000, 16 -4000, 21 3000 | -3000 / 31250 / 3515 |
   | `a_bw`, A: 4000, shown 4500, correct 6000, W 1000 | 4000 / 4500 / -500 | -1000 | 1b -1000, 21 1000 | -1000 / 33250 / 3755 |
   | `b_code_b_v80_route`, B: 3000, correct basis 1000 | box B 3000 / 1000 / 0 | 2000 | 2 2000, 7 2000 | 2000 / 36250 / 4115 |
   | `mixed_a_d_c_direct` | A as `a_high`; D as `d_low`; C 2500 / 1000 | 6000; 3000; 1500 | 1a 1000, 1b 6000, 3 1500, 7 8500, 8b 3000, 15 3000, 16 11500 | 11500 / 45750 / 4895 |

   In every case, lines 1a, 2, 8a, 9 and the other lines not listed are 0,
   and both attachments are published. On a BW row, column (g) is the net
   (basis shown − correct basis) + W, and W is limited by the corrected
   loss. That matches the column (g) "More than one code" rule and the
   worksheet. I also checked these Track 0 values by hand:
   `x_a_gain_d_loss`, `x_a_loss_d_gain`, `x_bw_w_equals_correct_loss`,
   `x_d_loss_to_gain`, `x_zero_proceeds_zero_shown`,
   `x_corrected_basis_changed_g_fixed`, `x_q3_yes_late_member_reanswered`,
   `m_a_and_b`, `m_d_and_e`, `t2_stage0`, `t3_stage0`,
   `n_two_w_st_and_w_lt` and `n_two_covered_st_and_covered_lt`.
   **No expected value in `expected.json` is wrong.**
2. **Admission.**
   - **Code B class: no.** Every attempt blocks: a duplicate across or
     within terms on every family pair (I enumerated all 16 cross-term
     pairs; each is closed by family exclusivity, a per-sale admission rule
     or the amounts-agree check); a column (g) row that disagrees with the
     worksheet; a swapped column (g) between two sales; W above the
     corrected loss; W on a corrected gain; correct basis equal to the
     shown basis; a column (g) row on a transaction with no sale (rejected
     at entry, companion presence); and the taxpayer-side flag (blocks on
     covered and code W; a code B sale has no such field).
   - **Zero proceeds.** Code B computes, and both attachments are required
     (`x_zero_proceeds_zero_shown`, and my `0 / 500 / 0` case).
   - **Outside the class: yes.** B1 (zero-proceeds direct sale) and S5
     (unread eligibility flags) publish wrong numbers. Both are inherited
     from v80.
   - **A wrong broker basis left uncorrected** can be published only on a
     false answer: Q3 "no", or a code B sale recorded under a different
     transaction. A Q3 "yes" with nothing recorded, or with the same
     transaction kept on line 1a, is refused.
   - **No v80 answer changes meaning.** Q1, Q2, IC79, IC80, Path B and the
     Form 8949 answer keep their vocabularies, and none of them is read
     under the guarded IC3 arm. The noncovered `amounts-agree` vocabulary
     now also returns "disagree" for a duplicate. That is a derived fact,
     not an answer (a recorded deviation).
3. **Decision 6.**
   - **Correct.** All four fixes work as built.
   - **Duplicates: complete.** The cross-term duplicate fix covers every
     pair.
   - **Taxpayer-side flag: incomplete in kind** (S5).
   - **Zero proceeds: incomplete** for the line 1a/8a families (B1).
   - **No other v80 changes.** Beyond the listed patterns, only the five
     listed returns change, and only in a blocked attachment row's
     `missing` list. The test asserts exactly that.
4. **Immutability.**
   - `git diff github/main --name-status -- packages/` shows only additions
     except `packages/tax/loader.py`. Nothing under `packages/schemas`
     changed.
   - **Registry v79 is add-only.** Compared with v78: 77 citizens and one
     package added, none removed or changed. Release v79 pins its sha256.
   - **The loader change is limited to v81.** It adds the v81 companion
     declaration (v80's pairs plus six code B pairs) and the v81 entry for
     the covered-flag refusal map, which is v80's map.
5. **What the filer sees.**
   - **Blocked lines.** Every blocked line has a non-empty explain or
     reason. The constraint reasons (no correction, W above the loss,
     holding period) are true and specific. S1, S2 and S4 are untrue or
     misleading in specific states, and S3 is jargon.
   - **Questions.** The new questions match their propositions; the
     package test pins this. IC3 is not plain (N2), and Q3 is ambiguous
     (N3).
6. **CI cost.**
   - **Redundant runs.** See S7.
   - **Fixture size.** The 447 KB fixture is one line per case: Track 0
     cases 172 KB, v80 group 231 KB (90 KB of it pinned rows), neighbours
     44 KB.
   - **Justified apart from the 51 redundant v80 entries.** The pinned rows
     are what the f8949-boxes-cf lesson asks for.
7. **Data safety.**
   - **Scan.** `python3 tools/envelope_scan.py --range github/main..HEAD`
     exits 0.
   - **No paths committed.** A grep of every changed file found no absolute
     or temp-directory path. The evidence harnesses create temp
     directories only at run time.
   - **Synthetic data only.** All entities are `demo.*`.

## Verified and reusable

- Law: P0's reading of code B on boxes A/D (column (e) is the basis shown,
  column (g) is shown − correct) and on boxes B/E (correct basis in (e),
  -0- in (g)) is right. So is BW netting with W limited by the corrected
  loss.
- The live tests run on the published v81 (`run` asserts the package,
  registry and release file names, and `build_world` asserts the content
  directory) through `live_coordinate_run`. The package test proves the 77
  published members are the prototype's bytes.

## Verdict

**Not ready.** Blocking:

1. **B1.** A zero-proceeds covered direct sale publishes Form 1040 line 7a
   as 0 beside a Schedule D line 21 loss. It is inherited from v80 and is
   the same pattern as Decision 6 patterns 1 and 2. Fix it by content, or
   have the owner park it as a known limitation that affects correctness.
2. **B2.** The `quick` job is red on HEAD
   (`test_speculative_refusal_then_retry_and_gated_retraction_are_atomic`
   over the fast-lane limit). Then rerun `verify` on the exact head.

S1 to S7 should be repaired or dispositioned before closeout. N1 to N5 are
recorded only.
