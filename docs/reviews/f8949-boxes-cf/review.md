# Review: sales without a Form 1099-B (Form 8949 boxes C and F), core v80

Reviewer: fresh reader, author-independent.
Charter: `docs/reviews/f8949-boxes-cf/charter-review.md` @ (removed at closeout).
Object: `milestone/f8949-boxes-cf-2025` at (removed at closeout)
(the Orientation Block SHA matches `git rev-parse HEAD`), diffed against
`github/main`. After `git fetch`: 0 commits behind, 17 ahead. PR #262 is open
as a draft and has not merged.
Sources read: the plan, P0, Track 0 closure, `cf_prototype.py`, `track0.py`,
the new content members, `packages/tax/loader.py` and the two new test
modules. Governance was not read.

Method: I ran cases on published core v80 through the module's own harness
(`tests/test_no1099b_sales_v80.py::_run`, which calls `live_coordinate_run`
and reads the presentation model). That covered 5 Track 0 cases and 17 new
ones of my own, all synthetic `demo.*` data. I also ran v79 through
`cf_probe.execute` for one comparison. Scratch scripts are under the session
scratchpad; nothing was written to the repo, and `git status` is clean. I
did not run `pytest`.

## Findings, by consequence

### B1. Blocking: the new in-class question is worded so that a truthful "yes" admits a covered sale with an adjustment code other than W

- **Where.** `packages/content/tax/2025/input-question.schedule-d-boundary-form8949-in-class.json:9`
  says: "Apart from sales your broker reported with their basis, is every
  sale … with … no adjustment other than a wash-sale loss?"
  The proposition it asks about,
  `schedule-d-boundary-form8949-in-class.bundle.json:5,11`, is: "Form 8949
  work **beyond covered sales and code W** is only boxes B, C, E and F …".
- **Violated claim.** The scope line "what stays outside the class is refused
  by an answer, never computed partially".
- **Mechanism.** A Path B "no" (`no-other-form8949-adjustments`, the ADR-0061
  answer meaning "I have codes other than W, multi-code rows or
  basis-not-reported sources") is admitted on lines 3 and 10, on both
  attachments, and on the preferential base by Q2 "yes" plus new in-class
  "yes". Branch 2 of `rule.schedule-d-line3.json` does not read Path B at
  all.
  - The question's opening clause takes every broker-basis-reported sale out
    of the "no adjustment other than a wash-sale loss" test.
  - So a filer with a box C sale and a covered box A sale carrying code D, O
    or similar reads the question truthfully and answers "yes".
  - The covered families have no field for that code, so the engine sees the
    same return as `c_loss` or `mixed_abcf`. Both publish (31250 / 3515 and
    40250 / 4115) without the adjustment.
- **Reproduction.** Run `mixed_abcf` (Path B "no", new in-class "yes", one
  box A sale): Form 1040 lines 15 and 16 and both attachments publish. Under
  the question's wording, the truthful answer for "box A sale with code D,
  plus a box C sale" is "yes", and that is exactly this act list.
- **Why it is new.** v79's in-class answer has no input question; its
  proposition text says "beyond covered sales and code W". v80 is the first
  time a filer is asked this in words, and the words are wider than the
  proposition.
- **Fix.** Reword the question so covered sales are exempt only when they
  have no adjustment or only code W. For example: "Is every sale on your
  Form 8949 either a sale your broker reported with its basis and no
  adjustment other than a wash-sale loss, or a sale of stocks or other
  securities, entered only once, with a basis you supply (and net proceeds
  you supply when you got no Form 1099-B) and no adjustment other than a
  wash-sale loss?" v80 and registry v78 have not reached `main`, so they can
  be regenerated before merge. Otherwise ship an input-question v2 in a
  successor. Add a test that pins the question text against the bundle
  proposition.

### B2. Blocking (publication gate): `quick` is red at the exact head

- **Where.** `tests/test_incremental_lattice.py:564`
  (`test_collision_order_backtracking_and_duplicate_declared_id_boundary`).
- **Reproduction.** `gh pr checks 262`: `quick` fails, job 128301328055 of
  run 42338671606, head (removed at closeout). The log reads "fast-lane budget
  exceeded: 3.9s > 3.0s", 1 failed and 1692 passed. `verify` also shows
  "fail", but that is the expected first-step stop on a draft. The fast lane
  that `verify` runs will hit the same test.
- **Context.** This branch already moved a sibling test in the same file to
  the live lane for the same CI-load reason. That edit was outside the
  charter's file list.
- **Fix.** Make the test fast, or mark it `@pytest.mark.live` with a
  measured reason as the sibling was. Do not raise
  `FAST_LANE_BUDGET_SECONDS`. Then get a green exact-head `verify`.

### S1. Should-fix: a failing sale of one term blocks the other term's line, and the page blames a sale that does not exist

- **Where.** `rule.schedule-d-line10.json:247,256` reads the box C (ST)
  subtotals in its unbacked-"yes" guard. `rule.schedule-d-line3.json:247,256`
  reads the box F (LT) subtotals the same way. The blocked text is at
  `schedule-d.line-10.form-field.json:34` and
  `schedule-d.line-3.form-field.json:34`.
- **Reproduction.**
  - My case `rv_c_adj_exceeds_loss` (one box C sale 4000/5000 with W 2000,
    CLS answers): line 10 is blocked. Its explain says "…or for each recorded
    long-term sale of that kind to have its proceeds and basis and pass its
    checks". Its reason is "The wash-sale disallowance exceeds this sale's
    own loss." No long-term sale is recorded.
  - The same happens on `c_code_w_on_gain` and, in the other direction, on
    `f_holding_mismatch`, where line 3 blocks.
- **Consequence.** No wrong number is published (Form 1040 blocks anyway).
  The page's explain on the other-term line is false about which sale is
  waiting.
- **Fix.** In the guard, read the other term's member count (the `count`
  over the source set, as the amounts-agree rules do), not its subtotal, if
  `count` is not blocked by member constraints. Otherwise add "or for a
  recorded sale of the other term to pass its checks" to both blocked
  sentences.

### S2. Should-fix: one sale entity recorded as both a box C and a box F sale is counted twice

- **Reproduction.** My case `rv_same_entity_st_lt` records
  `cf_sale(st, 2000, 8000, "rvdup")` and `cf_sale(lt, 2000, 8000, "rvdup")`,
  which share the entity `demo.cf.rvdup.sale`, with CLS answers. It publishes
  line 3 −6000, line 10 −6000, line 16 −12000, line 21 3000, and 31250 /
  3515. With gains instead of losses it would double the gain.
- **Why it differs from Decision 4.** Decision 4's accepted duplicate (box B
  plus box C) has no shared key. Here the two facts share the `sale` key
  (`tax.us.f8949-sale`), so content can see the duplicate. Today only the
  "entered only once" attestation refuses it.
- **Fix.** Have each term's `amounts-agree` rule (per subject) also require
  that the other term's `txn` count for the same sale is 0, which gives
  "disagree" and blocks. Alternatively, record this explicitly as covered by
  the in-class attestation and park it beside Decision 4.

### S3. Should-fix (evidence): the live test cannot tell why a case blocks

- **Where.** `tests/test_no1099b_sales_v80.py:212-219` (`_projection`) pins
  only lines, attachment dispositions and sentences ending in "?". `:154`
  also de-duplicates questions page-wide.
- **Reproduction.** Group `EXPECTED["v80"]` by projection. Twelve cases on
  different disposition paths have byte-identical projections, including
  `c_code_w_on_gain`, `f_holding_mismatch`, `unrecorded_out_of_class`,
  `q2_yes_nothing_recorded`, `m_c_new_ic_no` and `m_yes_nothing_no`. Five
  more share one projection: `m_c_8949_yes`, `w_c_amounts_disagree`,
  `w_c_object_wash_no_row`, `w_c_scalar_only_on_gain` and
  `m_c_8949_yes_pathb_no`.
- **Consequence.** If a sale-check case started blocking for an unrelated
  reason, the test would still pass. The "blocked by a sale's checks" and
  "refused by an answer" paths are not distinguished in the merge-gate
  evidence. `_assert_sound` only proves some text exists.
- **Fix.** Add these to the projection:
  - the non-question reason sentences per blocked Schedule D line;
  - the `(disposition, code, missing)` of the lines 2, 3, 9 and 10 rows and
    the four amount-check rows. `track0.summarize` already collects them as
    `dispositions`.

  This also lets the merges in Q5 happen without losing distinctions.

### S4. Should-fix: an unanswered Path B silently blocks a box C-only return, and nothing in the battery covers it

- **Reproduction.** My case `rv_c_loss_pathb_unanswered` (`c_loss` with
  `path_b=None`):
  - line 3 publishes −6000;
  - line 10 is blocked with `DEPENDENCY_ABSENT`, missing
    `schedule-d-boundary.no-other-form8949-adjustments`;
  - Form 1040 and both attachments block;
  - the page shows **no question**.
- **Cause.** Line 10's zero path is an `any` that already has a true
  disjunct (Q2 "yes" and new in-class "yes"). It still blocks on the absent
  Path B reference (`rule.schedule-d-line10.json:136`).
- **Inherited part.** The same return on v79 (box B, Path B unanswered) also
  blocks with no question. The ADR-0061 pair has no input question.
- **New part.** For boxes C and F, Path B is logically unnecessary. Every
  case in the module answers Path B, so this path is unevidenced.
- **Fix.** Split the zero-path admission into `choose` arms so the
  Q2/new-in-class arm is evaluated without reading Path B. Or park it with
  the other block-without-question limits, and add the case to the battery.

### N1. Note: the attachment titles are stale and appear on the page

`attachment.schedule-d.v8.json:309` is titled "Schedule D attachment v7 …"
and names lines 2 and 9 but not 3 and 10. The presentation model's
attachment list shows "Schedule D attachment v7" on v80.
`attachment.f8949.v4.json:5` names boxes A, D, B and E only. Both rules do
read lines 3 and 10 and the box C/F subtotals, as verified by grep. Fix:
retitle at the next successor, or now if B1 regenerates v80.

### N2. Note: the page asks a question that cannot unblock the return

On `m_no_no_8949no`, every blocked line's reason is the new in-class
question. Answering it "yes" (`m_no_no_8949no_new_ic_yes`) still blocks, and
then no question is shown. This is inside Decision 6's accepted limit and
the parked `rule-artifact` successor. I record it because the shown question
is a false lead, not just a missing one.

### N3. Note: a Form 8949 "no" with nothing recorded publishes when Path B is "yes"

`m_no_no_8949no_pathb_yes` publishes the wage return. This is the v79
pattern: the ADR-0061 meaning admits it, and Q1 and Q2 "no" are the
filer's own answers. It is consistent with Decision 2 as written ("that no
answer admits"). No action unless the owner wants Path B "yes" to need a
recorded covered W sale.

### N4. Note: a recorded 0/0 sale blocks with no question

`rv_c_zero_zero` (box C, proceeds 0, basis 0, Q2 "yes"): both line 3
branches fail, so the return blocks with no question. It is conservative
and rare. Park or ignore.

## Q1. Tax correctness, computed by hand

The base return is single, taxable income 34,250, tax 3,875 (2025 Tax
Table, row 34,250–34,300). Tax-table rows use the midpoint; 0% LTCG top for
single is 48,350; line 21 limit is $3,000. The column (h) rule is (d) − (e)
+ (g) (i1040sd as quoted in P0).

| Case | Hand values | v80 run |
| --- | --- | --- |
| Box F gain 6000/2000 (`f_gain`) | L10 4000, L15 4000, L16 4000, L21 0, 7a 4000, 1040 L15 38250. Ordinary 34250 → 3875; 4000 at 0% → L16 3875. Pref base 4000 | identical; 8949 and Sch D published |
| Box C loss 2000/8000 (`c_loss`) | L3 −6000, L7 −6000, L16 −6000, L21 (3000), 7a −3000, 1040 L15 31250. Tax at 31275: 1192.50 + 0.12×19350 = 3514.50 → 3515 | identical |
| Box C, code W: 4000/7000, W 1000 (`c_wash`) | L3 −3000 + 1000 = −2000, L21 (2000), 7a −2000, 1040 L15 32250 → 3635 | identical |
| Mixed A/B/C + F (`mixed_abcf`) | L1a 1000, L2 −500, L3 1500, L7 2000, L10 4000, L15 4000, L16 6000, 7a 6000, 1040 L15 40250. Ordinary 36250 → 4115; 4000 at 0% → 4115. Pref base 4000 | identical |

Extra cases I added and computed:

| Case | Hand values | v80 run |
| --- | --- | --- |
| `rv_f_wash` (box F 4000/7000, W 1000) | L10 −2000, L15 −2000, L21 2000, 32250 / 3635 | identical |
| `rv_c_loss_f_gain` | L7 −6000, L15 4000, L16 −2000, L21 2000, pref 0, 32250 / 3635 | identical |
| `rv_c_gain_f_loss` | L7 5000, L15 −2000, L16 3000, pref 0, 37250; tax at 37275 = 4234.50 → 4235 | identical |
| `rv_f_big_gain` (22000/2000) | 54250; 3875 + 0% on 14100 + 15% on 5900 (885) = 4760; pref 20000 | identical |
| `rv_c_worthless` (0/5000) | L3 −5000, L21 3000, 31250 / 3515 | identical |
| `rv_c_wash_equals_loss` (4000/5000, W 1000) | L3 0, 34250 / 3875 | identical |
| `rv_c_adj_exceeds_loss` | blocks (`ADJUSTMENT_EXCEEDS_LOSS`) | blocks |
| `rv_f_w_scalar_only_on_gain` | blocks | blocks |
| `rv_f_basis_missing`, `rv_f_proceeds_missing` | block and ask the long-term no-1099-B questions | block and ask; this path was unexercised in the module before |

No expected value in `tests/test_no1099b_sales_v80.py` is wrong for these
cases. The married-filing-separately $1,500 limit and the carryover are not
exercised (Decision 4, accepted).

## Q2. Admission

- **Can a box C/F sale be left unrecorded and the return publish?** Only
  through a false answer: Q2 "no", or Form 8949 "yes" beside Q2 "no".
  - Q2 "yes" with nothing recorded blocks both lines
    (`q2_yes_nothing_recorded`, `m_no_yes_nothing`).
  - A Form 8949 "no" that nothing admits blocks.
  - A recorded sale beside Form 8949 "yes" blocks.
  - A late member makes either Q2 answer stale (`late_member_after_no`,
    `q2_late_yes_stale`).
  - An **unrecorded out-of-class adjustment** is the exception: B1 publishes
    under a truthful "yes".
- **Can a recorded sale publish a wrong number?**
  - Shared records: within one term, the identity is `(sale, tax-year)`, so
    a second record supersedes the first. Across terms, see S2 (counted
    twice). Box B/E reuse of a transaction entity blocks
    (`d3_b_shared_transaction`).
  - Disagreeing amounts block (`w_c_amounts_disagree`,
    `w_c_object_wash_no_row`).
  - Code W on a gain blocks, through the object (`c_code_w_on_gain`) or a
    scalar only (`w_c_scalar_only_on_gain`, `rv_f_w_scalar_only_on_gain`).
    W above the loss blocks (`rv_c_adj_exceeds_loss`).
  - A missing proceeds or basis row blocks and asks, for C, F, B and E. A
    missing basis on the object is rejected by the schema.
  - Negative amounts are rejected by `minimum: 0`.
- **Does any v79 answer change meaning?** No proposition, identity or
  lifecycle changes. Admission effects narrow, all accepted:
  - Q1 "yes" now needs a recorded B/E sale on lines 3 and 10.
  - v79 in-class "yes" admits a Form 8949 "no" only beside Q1 "yes".
  - Every v79 return newly needs Q2.

  The ten newly blocked returns match Decisions 2, 3 and 5.

## Q3. Immutability

- `git diff github/main --name-status` shows only additions (`A`) under
  `packages/content` (63 files) and nothing under `packages/schemas`.
  Modified files are `packages/tax/loader.py`, three tests and
  `tools/required_versus_read_allowlist.json`.
- Registry v78 against v77, compared as sets of `(id, version, checksum)`:
  0 removed or changed, 61 citizens and 1 package (core v80, `3e5444b2…`)
  added, no duplicate `(id, version)`. It is add-only.
- All 61 `cf-prototype-rules/*.json` files are byte-identical to their
  `packages/content/tax/2025/` copies (`cmp`).
- The loader adds `no1099b_scalar_presence_pairs()` and two per-core v80
  entries: the companion declaration (v79 pairs plus six C/F pairs) and the
  covered-flag refusal map. It also edits a docstring. v79 and earlier
  entries are unchanged.
- The allowlist replaces the latest-core witnesses for line 1a v4→v5 and
  line 8a v5→v6. This is correct because `tools/required_versus_read.py`
  scopes to `latest_core_package` and flags stale entries. It adds four
  amount-check witnesses.

## Q4. What the filer sees

- **Is the page reason non-empty and true?** Non-empty on every blocked
  line I ran. It is not true on the other-term line (S1), and it gives no
  question on Path B unanswered (S4) or on the Decision 6 paths (N2).
  Carried-over 1040 lines keep pre-existing texts, such as line 7a's
  "Exception-1 authority …", which are not this milestone's.
- **Is every new `explain` true of its rule's `when`?**
  - Lines 3 and 10 published and `computed_zero` are true. The zero
    sentence's "or … net to zero" disjunct covers `rv_c_wash_equals_loss`.
  - The blocked sentence is not true on the other term (S1).
  - The lines 3 and 10 `closure_backed_zero` sentence is unreachable,
    because the rule always computes.
  - Attachment titles are stale (N1).
- **Is each question asked once?** Within a section, yes. Across the page,
  a blocking question repeats as a reason on every downstream blocked line
  (33 sections on `m_no_no_8949no`). That is the page's reason-propagation
  mechanism, not new here, but the test's page-wide de-duplication (`:154`)
  hides it.
- **Is the new question plain, and true for a filer who sold something
  other than securities?**
  - Q2 ("Did you sell any stocks or other securities for which you did not
    receive a Form 1099-B or substitute statement?") is plain. It is true
    for such a filer: they answer "no", and the in-class "no" ("a sale of
    stocks or other securities") refuses the return.
  - The in-class question is a five-clause compound and wrong in scope
    (B1).

## Q5. CI cost

There are 121 parametrized cases: 117 coordinator runs plus 4 rejected
before a run. The prototype's slowest were `c_code_w_on_gain` (37 s) and
`f_holding_mismatch` (23 s), both member-constraint blocks; most cases are
about 5 s.

- **Exact duplicates (same act list, at most a tag differs).** Drop one of
  each pair; no path is lost:
  - `m_c_no_yes` ≡ `c_loss`;
  - `m_b_yes_no` ≡ `d3_b_loss` (identical builder);
  - `m_no_no` ≡ `wage_q2_no`;
  - `m_no_unanswered` ≡ `wage_q2_unanswered`.
- **Near duplicates (same path, answer order differs).**
  `late_member_after_no` ~ `t1_stage1` and `late_member_reanswered_yes` ~
  `t1_stage4`. Keep one of each pair unless answer order is a claimed
  property.
- **Keep.**
  - The two slow sale-check cases (distinct constraint paths).
  - `mixed_abcf_old_ic_unanswered` (the guarded arm).
  - `t2_stage3_old_ic_no` (its equality with `t2_stage3` is the claim).
  - The 50 carried v79 returns. They are the "every v79 return" evidence.
    The 11 non-capital `one_*` returns share one Schedule D path, but they
    differ on the preferential-base inputs, so sampling them is the owner's
    call.
- **Caveat.** Merging projection-identical cases is unsafe until S3 makes
  the projection distinguish block reasons.

## Q6. Data safety

- `python3 tools/envelope_scan.py --range github/main..HEAD` exits 0 with no
  output.
- Grepping the changed files for absolute local paths finds nothing.

- The evidence `__pycache__` is untracked and ignored.
- The IRS PDFs are cited by checksum and are not committed.
- All case data is `demo.*`.

## Verified and reusable

- The hand values in Q1, including nine extra cases.
- Registry add-only and byte-identity of the copied members.
- Loader scope.
- The amount-agreement, holding-period, code-W-on-gain and
  adjustment-exceeds-loss blocks.
- The long-term missing-amount questions.
- v79 Path B unanswered blocking (inherited).

## Verdict

**Not ready.** Blocking:

1. **B1**: reword the new in-class input question so covered sales are
   exempt only with no adjustment or only code W, and regenerate or succeed
   v80.
2. **B2**: get the `quick` fast lane green at the exact head (handle
   `test_collision_order_backtracking_and_duplicate_declared_id_boundary`
   without raising the budget), then a green exact-head `verify`.

Recommended before merge: S1 to S4. Notes N1 to N4 can be parked.
