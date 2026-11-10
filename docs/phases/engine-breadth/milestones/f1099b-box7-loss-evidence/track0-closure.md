# Track 0 adversarial closure: Form 1099-B box 7 beside a loss

Evidence for `docs/phases/engine-breadth/milestones/f1099b-box7-loss.md`.
Charter: `docs/reviews/f1099b-box7-loss/charter-track0.md`.
Gate: `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate".

Scratch core v84 is the Decision 5 shape: eight per-sale verdicts, eight family
checks, and Schedule D line 16 v4 still requiring the eight sale-count symbols.
Every case below is a `live_coordinate_run`. Hand values come from
`probe.hand_return` (wages 50,000, withholding 4,500, standard deduction 15,750,
2025 Tax Table and the 48,350 qualified-dividend band). A code B sale records a
shown basis 500 above the correct basis, so the sale is a real correction.

Decision 1 puts Schedule D Example 2 code L outside this class. The return
refuses line 16. It does not recompute column (h). The yes-loss cases are that
refusal.

## Decision 5

`decision5-rerun.json`: 298 recorded v83 runs on scratch v84, classified against
the fixture, 298 `identical`.

## Authority-lifecycle table

`track0-authority.json`: 21 cases, 21 passed.

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| `f1099b.statement-box7-loss-not-allowed` | Box 7 is checked on this Form 1099-B statement | One statement (`statement`, tax year 2025) | The filer's assertion for that statement | A later assertion on the same fact id. `late_yes_to_no` records yes, then no. The current value is no and the verdict becomes `clear`. An unanswered statement blocks and asks the question: `alc_covered_st_unanswered`. |
| `f1099b.{family}-txn.box7-verdict` | This sale is `clear` or `disallowed` | One sale (broker, statement, transaction, tax year) | That sale's column (h) and that statement's box 7 answer | Removing the sale drops the verdict (`late_loss_removed`). Adding a loss on a yes statement adds a `disallowed` verdict (`late_gain_then_loss`). A yes beside a gain or zero is `clear` (`alc_*_gain`). A yes beside a loss is `disallowed` (`alc_*_loss`). |
| `f1099b.{family}-txn.box7-loss-check` | 0 when every current sale in the family is clear; blocked with nothing missing when any is disallowed | The family's current members | Every current verdict in that family, and a box 7 answer for each statement that has a sale | A disallowed verdict blocks the check (`m_covered-st_yes_loss` missing `[]`). An empty family publishes 0 (`alc_closed_empty`, all eight checks 0). |
| Eight `f1099b.*-count` symbols | How many sales are in the family | The family's closure and its current members | The same closure as on v83 | A missing per-family closure blocks that count (`m_absence_covered-st`). A missing grouped closure blocks both terms (`m_absence_noncovered-st`, `m_absence_code-b-st`). Two current sales publish 2 (`alc_count_two`). |
| Statement identity | Box 7 on one statement does not apply to another | The statement key inside the sale fact id | The sale's own statement | `alc_statement_scope`: yes on the gain statement and no on the loss statement, both verdicts `clear`, check 0, line 16 is 600. `alc_same_statement`: gain and loss on one yes statement, verdicts `clear` and `disallowed`, line 16 blocked. |

Line 16 publishes line 7 plus line 15 when every check is 0 and the counts and
both lines are published. A gain on each family matches the hand, including
code B (`alc_code-b-st_gain` line 1b is 1,000; `alc_code-b-lt_gain` line 8b is
1,000). A closed empty return publishes line 16 as 0 and asks nothing
(`alc_closed_empty`).

## Empty and nonempty matrix

`track0-matrix.json`: 49 cases, 49 passed. Eight families, five sale states,
plus closed-empty and eight absence cases.

| Family state | Universe | Eligibility | Feature result | Neighbor |
| --- | --- | --- | --- | --- |
| Closed empty, closure present | Wage return, every count 0 | Inapplicable | Line 16 is 0. Every check is 0. No question. `m_closed_empty`. | Lines 7 and 15 are 0. |
| Closed empty, closure missing | Covered and code W: that family's source closure removed. Noncovered: `f1099b.noncovered-sold.source-closure` removed. Code B: `f1099b.code-b-sold.source-closure` removed. | Any | Line 16 blocked. Covered short-term names `schedule-d.line-7` and `f1099b.covered-st-count` (`m_absence_covered-st`) and asks the covered-sale question. Noncovered names both noncovered counts (`m_absence_noncovered-st`). Code B names both code B counts (`m_absence_code-b-st`). | The count and the line it feeds stay unpublished. The box 7 check is not the missing fact. |
| Nonempty, eligible | Box 7 no, or yes beside a gain, or yes beside zero | The loss check is 0 | The hand publishes. `m_covered-st_no` line 16 is −1,000. `m_covered-st_yes_gain` is 1,000. `m_covered-st_yes_zero` is 0. The same three states pass for the other seven families. | Lines 7, 15, 21 and Form 1040 follow the hand. |
| Nonempty, ineligible | Box 7 yes and column (h) below zero | Refused | Line 16 blocked, missing only that family's check, check missing `[]`, question not asked. `m_{family}_yes_loss` for all eight. | Line 21 and Form 1040 lines 7a, 15, 16, 24, 33, 34, 37 stay blocked. The loss still sits on line 1a, 1b, 2, 8a, 8b, or 9. |
| Nonempty, answer missing | A sale and no box 7 assertion | The check cannot close | Line 16 blocked on the check. The check names `f1099b.statement-box7-loss-not-allowed`. The box 7 question is asked. `m_{family}_unanswered` for all eight. | Downstream lines stay blocked. |

## Late-member lifecycle

`track0-late.json`: four traces, four passed. Paper trace: attest, close,
compute, change the authority, reclose, recompute.

| Trace | Before | After | What became unusable |
| --- | --- | --- | --- |
| `late_gain_then_loss` | Yes, one covered short-term gain. Line 16 finding `finding:derived:49946746c17ccdb127d425c8`. Closure `demo.sfa.g.f1099b.covered-st.closure`. | A loss added on that statement. Line 16 blocked. Verdicts `clear` and `disallowed`. | That line 16 finding is absent. The prior closure is not on the act list. The successor closure is `demo.sfa.loss.f1099b.covered-st.closure`. |
| `late_loss_removed` | Yes beside a loss. Line 16 blocked. | The sale is removed and the family reclosed. Line 16 finding `finding:derived:d095ce9840daafc715e6ead4` publishes 0. The check is 0. No verdict remains. | The disallowed verdict and the blocked check. The removal closure replaces the sale closure. |
| `late_yes_to_no` | Yes beside a loss. Line 16 blocked. | A second assertion, same fact id, value no. Snapshot values `yes`, then `no`. Verdict `clear`. Line 16 is −1,000. | The disallowed verdict. The current box 7 value is the later assertion. |
| `late_new_statement_unanswered` | Statement A answered yes, gain. Line 16 finding `finding:derived:e6643342b51b6fa45d677e2e`. | Statement B added with a gain and no box 7 answer. | That line 16 finding is absent. The new closure is `demo.sfa.b.f1099b.covered-st.closure`. Line 16 is blocked and the box 7 question is asked. |

## Claim reuse

`track0-reuse.json`: four live pairs, four passed. Package identity: line 7,
line 15, and the sale-count rules keep their v83 versions. The only version
difference is `rule.schedule-d-line16` v3 to v4 and `schedule-d.line-16` v3 to v4.

| Case | Proposition | v83 | v84 |
| --- | --- | --- | --- |
| `reuse_box7_no` | A loss on a statement answered no is an ordinary loss | Line 16 is −1,000. Lines match. | Same lines, same line 16 disposition. |
| `reuse_no_sale` | No sale, no box 7 activity | Line 16 is 0 | Line 16 is 0. Lines match. |
| `reuse_yes_gain` | Lines 7 and 15 and the eight counts are the sale facts, not the box 7 rule | Line 7 is 1,000. Line 16 is blocked, because v3 treats any yes as a refusal. | Line 7 is 1,000. Counts match. Line 16 is 1,000. |
| `reuse_covered_flag` | A covered sale whose basis was not reported still uses the covered-flag sentence | The sentence is in the reasons. | The same sentence is in the reasons. |

Exception 1 is the same answer set the probe already applies (`honest` and
`honest_exception1`). The late traces call it again after a member change.
`late_loss_removed` reaches a published zero only after that re-answer, which
is the v83 Exception 1 behavior on an empty sale set.

## Neighboring capability dependency diff

`track0-neighbour.json`: 298 recorded returns, each run live on published core
v83 and live on scratch v84 (596 coordinate runs). Classification of v84
against v83: 298 `identical`. Fixture support: v83 matches the recorded pin on
298, and v84 matches it on 298. Changes: none.

Direct new prerequisites of line 16 are the eight family checks. On a return
where box 7 has no work, each check publishes 0, so the checks are not missing
and the v83 pin is unchanged. The eight sale-count prerequisites are the v3
list, in the v3 order. Schedule D lines 17, 18, 19, 20, and 22 have no rule in
this package. The consumers that require line 16 are unchanged except that
their dependency can now publish when box 7 is yes and every sale is a gain or
zero (`reuse_yes_gain`).

## Integration surface

`track0-surface.json`: 7 models, 7 passed. Presentation validation passed on
each. Line 16 has one disposition row on each.

| Consumer | Binding | Cardinality | Satisfied |
| --- | --- | --- | --- |
| `rule.schedule-d-line21` v1 | requires `schedule-d.line-16` | one disposition | Yes. Published paths compute line 21 from the hand. Blocked paths leave line 21 blocked. |
| `rule.form1040-line7a` v9 | requires line 16 and line 21 | one disposition | Yes. `surface_published_gain` line 7a is 1,000. `surface_published_loss` is −1,000. Blocked when line 16 is blocked. |
| `rule.selected-preferential-base` v10 | requires line 16 | one disposition | Yes. Published on the three publishing paths. Blocked on `schedule-d.line-16` for yes-loss and unanswered, and also on `f1099b.covered-st-count` for `surface_blocked_count`. |
| `schedule-d.line-16` form field v4 | binds `schedule-d.line-16` | one presentation row | Yes. Field version v4. Blocked explain is the narrowed sentence on every model, including the publishing ones. |
| Schedule D lines 17, 18, 19, 20, 22 | no form field and no rule in the package | none | No binding to satisfy. |

Form 1040 lines 15, 16, 24, 33, 34, and 37 are downstream of line 7a. They have
no direct require of line 16. On `surface_published_gain` they are 35,250 /
3,995 / 3,995 / 4,500 / 505 / 0. On `surface_published_loss` (box 7 no) they
are 33,250 / 3,755 / 3,755 / 4,500 / 745 / 0. On `surface_published_zero` and
`surface_no_box7_activity` they are 34,250 / 3,875 / 3,875 / 4,500 / 625 / 0.
On `surface_blocked_yes_loss` and `surface_blocked_unanswered` all six are
blocked. Line 33 is blocked on those two paths because taxable income is
blocked. Its own rule does not require line 16.

Presentation probe:

- Yes beside a loss (`surface_blocked_yes_loss`): disposition blocked,
  `DEPENDENCY_ABSENT`, missing `f1099b.covered-st-txn.box7-loss-check`. The
  check row is blocked with missing `[]`. Line 16 reasons are empty. The
  question is not asked. The field's blocked explain is the narrowed sentence.
- Unanswered (`surface_blocked_unanswered`): the same missing check, and the
  check names the box 7 fact, so the question is attached. The question text is
  the unchanged box 7 question.
- Missing count (`surface_blocked_count`): missing `schedule-d.line-7` and
  `f1099b.covered-st-count`. The question is the covered short-term closure
  question.

## Smaller shape

Not adopted. `BOX7_SMALLER=verdicts-only` builds eight verdict rules and no
family checks (`track0-smaller.json`, `new_rules` 8). Line 16 requires the
eight verdict symbols. All four trial cases fail, and the decided rows were
not re-scored against this core.

`alc_closed_empty` blocks line 16 missing all eight verdict symbols.
`alc_covered-st_gain` publishes the covered short-term verdict and still
blocks missing all eight, including that one: a subject-scoped publication
does not satisfy a bare require. `alc_covered_st_unanswered` does not ask the
box 7 question, because the missing list is the verdict symbols. A single
selection cannot hold the eight families either. A rule selection in
`packages/schemas/derivation/rule-artifact.v15.schema.json` is mode
`exclusive_presence`, conflict `refuse`, and `paths` `minItems` 2 with no
maximum. Two nonempty paths refuse the rule, so one check cannot cover eight
families that can all be present. `minItems` 2 is why each check carries the
inert path on the never-written fact.

The 16-rule shape remains the default. This trial is a content-only failure.
It is not a Track 0 row failure, and it did not require an engine, schema, or
recording change to the decided shape.

## Stop

No stop. The decided shape passes every row on scratch content alone.
