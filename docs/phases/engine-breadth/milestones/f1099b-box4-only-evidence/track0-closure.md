# Track 0 adversarial closure: Form 1099-B backup withholding without a sale

Evidence for `docs/phases/engine-breadth/milestones/f1099b-box4-only.md`.
Charter: `docs/reviews/f1099b-box4-only/charter-track0.md`.
Gate: `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate".

Scratch core v85 is the Decision 1–7 shape: a return-level yes/no, a
return-level amount when yes, line 25b v8, and field v6. The per-statement
box 4 question is unchanged. Decision 7 wording excludes a statement whose
box 4 was entered with its sales. Every case below is a `live_coordinate_run`.
Hand values come from `probe.hand_return` (wages 50,000, withholding 4,500,
standard deduction 15,750, 2025 Tax Table).

## Decision 7

`prototype-build.json` records the two return-level questions:

- Present: "Did you receive a Form 1099-B or substitute statement that shows federal income tax withheld in box 4 and reports no closed sale (for example, a short sale still open at year end)? Do not count a statement whose box 4 you already entered with its sales."
- Amount: "Enter the federal income tax withheld in box 4 of Form 1099-B or substitute statements that report no closed sale. Do not include a statement whose box 4 you already entered with its sales. If more than one remaining statement, enter the total. If box 4 is blank, enter $0."

The line 25b field blocked explanation names the same exclusion. Every Track 0
case checks those sentences.

## Authority-lifecycle table

`track0-authority.json`: 8 cases, 8 passed.

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| `f1099b.no-sale-box4-present` | The filer received a Form 1099-B that shows box 4 withholding and no closed sale, other than a statement whose box 4 was entered with its sales | The return (tax year 2025) | The filer's yes or no | A later assertion on the same fact id. `late_yes_to_no` records yes, then no. The current value is no and line 25b drops the return-level addend. Unanswered blocks and asks the question: `alc_present_unanswered`. |
| `f1099b.no-sale-box4-withholding` | One nonnegative total of those statements' box 4 | The return (tax year 2025) | Present is yes | A later assertion on the same fact id. `late_amount_corrected` records 150, then 80. Line 25b follows the later amount. Unanswered after yes blocks and asks the amount: `alc_present_yes_amount_unanswered`. Present no does not read it (`late_yes_to_no`). |
| `f1099b.statement-box4-withholding` with a sale | Box 4 on that statement, asked of every recorded sale | One statement (`statement`, tax year 2025) | The sale's statement key (`require_paired`) | `alc_stmt_with_sale` publishes 200 with present no. The sale question is unchanged (`reuse_box4_question`). |
| `f1099b.statement-box4-withholding` with no sale | The same amount fact on a statement that has no sale | One statement | A recorded amount; nothing asks for it | Decision 6: it still counts. `alc_stmt_without_sale` publishes 150 with present yes and return-level 0. `late_sale_removed` leaves 200 after the sale is gone. |
| Statement identity | One statement's box 4 is not another statement's | The statement key inside the amount fact id | That statement's own assertion | `alc_stmt_identity`: sale statement 200 plus return-level 150 is 350. The two copies are different statements. |

`alc_present_no` publishes line 25b 0 on a return with no Form 1099-B.
`alc_present_yes_amount` publishes 150 from the return-level amount alone.
`alc_double_count` publishes 300 from per-statement 150 plus return-level 150.
That is the dishonest two-copy answer Decision 7 names; the honest paths keep
one copy (`alc_stmt_without_sale`, `alc_present_yes_amount`,
`late_yes_then_sale_then_no`).

## Empty and nonempty matrix

`track0-matrix.json`: 25 cases, 25 passed. Four family states, each with the
yes/no unanswered, no, yes with amount, and yes with amount unanswered, plus
per-statement zero and nonzero.

| Family state | Universe | Eligibility | Feature result | Neighbor |
| --- | --- | --- | --- | --- |
| No Form 1099-B, present unanswered | Wage return, no 1099-B statement | The yes/no is required of every return | Line 25b blocked, missing `f1099b.no-sale-box4-present`, present question asked. `m_none_unanswered`. | Lines 25d, 33, 34, 37 blocked. Line 25a is 4500. |
| No Form 1099-B, present no | Same | Inapplicable; add nothing | Line 25b is 0. `m_none_no`. | 25d 4500, refund 625. |
| No Form 1099-B, present yes with amount | Same | Return-level withholding | Line 25b is 150. `m_none_yes_amount`. | 25d 4650, refund 775. |
| No Form 1099-B, present yes amount unanswered | Same | Amount required | Line 25b blocked, missing `f1099b.no-sale-box4-withholding`. `m_none_yes_amount_unanswered`. | Downstream blocked. |
| Sale statements only | One covered short-term sale | Present no adds nothing | `m_sale_no_stmt200` is 200. `m_sale_no_stmt0` is 0. Unanswered blocks (`m_sale_unanswered_stmt200`, `m_sale_unanswered_stmt0`). Yes plus 150 is 350 (`m_sale_yes_amount_stmt200`). | Line 7a is 1000. |
| No-sale statement only | One statement entity, no sale | Present no, or yes with one copy | `m_nosale_no` is 0. `m_nosale_yes_amount` is 150. Decision 6: `m_nosale_no_stmt150` is 150. Honest: `m_nosale_yes_amount0_stmt150` is 150. Zero: `m_nosale_no_stmt0`. | Downstream follows 25b. |
| Both | A sale and a no-sale statement | Same four present states | `m_both_no_sale200` is 200. `m_both_yes_amount_sale200` is 350. Decision 6: `m_both_no_sale200_stmt150` is 350. Honest: `m_both_yes_amount0_sale200_stmt150` is 350. | Line 7a is 1000. |

## Late-member lifecycle

`track0-late.json`: four traces, four passed. Paper trace: attest, close,
compute, change the authority, reclose, recompute.

| Trace | Before | After | What became unusable |
| --- | --- | --- | --- |
| `late_yes_then_sale_then_no` | Present yes, return-level 150, no sale. Line 25b 150. | A sale is added on that statement, per-statement box 4 is 150, present is superseded to no. Line 25b 150, line 7a 1000. Snapshot present values `yes`, then `no`. | The prior line 25b finding is absent. Present yes is not current. The return-level amount is not added. The per-statement amount is the one copy. |
| `late_sale_removed` | Sale with box 4 200, present no. Line 25b 200, line 7a 1000. | The sale is removed. Line 25b stays 200. Line 7a is 0. | The sale and its Schedule D lines. The leftover per-statement amount remains current (Decision 6). |
| `late_amount_corrected` | Present yes, amount 150. Line 25b 150. | A second amount assertion, value 80. Snapshot amounts 150, then 80. Line 25b 80. | The prior line 25b finding. The current amount is the later assertion. |
| `late_yes_to_no` | Present yes, amount 150. Line 25b 150. | A second present assertion, value no. Snapshot present `yes`, then `no`. Line 25b 0. | The prior line 25b finding. The amount finding remains on the log and is not added. |

## Claim reuse

`track0-reuse.json`: 11 live pairs, 11 passed. Package identity: the six line
25b subtotals, the per-statement box 4 question, and the box 7 checks keep
their v84 versions. The only version difference is `rule.form1040-line25b` v7
to v8 and `form1040.line-25b` v5 to v6.

| Case | Proposition | v84 | v85 (present no) |
| --- | --- | --- | --- |
| `reuse_int_alone` | Form 1099-INT box 4 50 | Line 25b 50 | Same line 25b, same published lines |
| `reuse_div_alone` | Form 1099-DIV box 4 75 | 75 | Same |
| `reuse_ira_alone` | Form 1099-R box 4 80 | 80 | Same |
| `reuse_unemp_alone` | Form 1099-G box 4 90 | 90 | Same |
| `reuse_ssa_alone` | Form SSA-1099 box 6 60 | 60 | Same |
| `reuse_all_five_alone` | Five legacy subtotals | 355 | Same |
| `reuse_all_with_b4` | Those five plus per-statement box 4 100 | 455 | Same |
| `reuse_b4_subtotal` | Per-statement box 4 200 on a sale | 200 | Same, including line 7a 1000 |
| `reuse_box4_question` | A sale with no box 4 amount | Asks the unchanged sale box 4 question; line 25b blocked | Same question, same block |
| `reuse_box7_check` | Box 7 yes beside a loss | Line 16 blocked | Line 16 blocked the same way; line 25b matches v84 |
| `reuse_no_equals_v84` | A wage return, present no | Line 25b 0 | Line 25b 0. Lines match. |

## Neighboring capability dependency diff

`track0-neighbour.json`: 298 recorded returns, each run live on published core
v84 and live on scratch v85 (596 coordinate runs), recorded answers not
substituted. Classification of v85 against v84: 207 `identical`, 91
`asks_no_sale_present`, 0 counterexamples.

The 91 are the returns that publish line 25b on v84, including 0. v85 blocks
until the yes/no is answered. Decision 4: every return is asked. The new
prerequisite of line 25b is `f1099b.no-sale-box4-present` answered yes or no.
On a return where no-sale box 4 has no work, answering no adds nothing, so
the v84 numbers are unchanged.

Restore: those 91 rerun on v85 with one added answer, present=no (687 live
runs in total). Every v84 published line is restored. Restore failed: none.

Direct new prerequisite of line 25b is the present fact. The six subtotal
prerequisites and the sale pairing are the v7 list. Line 25d still requires
line 25b. Lines 33, 34, and 37 require line 25d, not line 25b.

## Integration surface

`track0-surface.json`: 6 models, 6 passed. Presentation validation passed on
each. Line 25b has one disposition row on each.

| Consumer | Binding | Cardinality | Satisfied |
| --- | --- | --- | --- |
| `rule.form1040-line25d` v1 | requires `payments.line25b` | one disposition | Yes. Published paths compute 25d from 25a+25b+25c. Blocked paths leave 25d blocked. |
| `form1040.line-25b` form field v6 | binds `payments.line25b` | one presentation row | Yes. Field version v6. Blocked explain is the Decision 7 sentence on every model. |
| `rule.form1040-line33` v1 | requires line 25d | one disposition | Yes. Follows 25d. Blocked when 25b is blocked. |
| `rule.form1040-line34` v1 | requires line 33 and tax | one disposition | Yes. `surface_published_no` refund 625. `surface_published_yes` 775. `surface_published_sale` 705. |
| `rule.form1040-line37` v1 | requires tax and line 33 | one disposition | Yes. 0 on the three publishing paths. Blocked when 25b is blocked. |
| `f1099b.b4` source family v1 | authorizes the line 25b subtotal | unchanged | Yes. Existing family; not a new consumer. |

Presentation probe:

- Unanswered yes/no (`surface_blocked_present`): disposition blocked,
  `DEPENDENCY_ABSENT`, missing `f1099b.no-sale-box4-present`. The question
  text is the Decision 7 present question. Lines 25d, 33, 34, and 37 carry
  the same sentence. Line 25a is 4500.
- Unanswered amount (`surface_blocked_amount`): the same block, missing
  `f1099b.no-sale-box4-withholding`. The question text is the Decision 7
  amount question.
- Unanswered sale box 4 (`surface_blocked_sale_box4`): missing
  `f1099b.statement-box4-withholding`. The per-statement box 4 question is
  the unchanged v84 sentence.

## Stop

No stop. The decided shape passes every row on scratch content alone.
