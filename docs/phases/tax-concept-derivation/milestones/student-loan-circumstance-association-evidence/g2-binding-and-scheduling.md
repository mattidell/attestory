# G2 scheduling — the join, the binding, the runners

Branch `milestone/student-loan-circumstance-association`, HEAD `b558da4e097367319816568f41091d4fbab5d0b5` (ADR 0075 repair: subject identity is enforced; the disconnected-type check is not a binding proof). Read at that commit: ADR 0075, `g2-path-investigation.md` Question 1, `subject_dispatch._scope` and the coverage-slot fill, `runner.is_eligible` / `attempt` / `finalize_unreached` / `evaluate_subject_scoped_rule`, `reference_runner.run_reference`.

No production code, schema, or content was changed. Probes are `tests/test_sli_g2_binding_probe.py`. Identities are synthetic `demo.*`. "Executed" means that test called the existing hand-dispatch or the existing runners. "Traced" means it was read off the source and not run.

The owner favours a subject declaration on each rule, and rejects one shared key name as a binding proof. Sharing tax year alone is the case that makes that concrete.

The production join is `subject_dispatch._scope`. Shared names are the **union**, across every candidate row, of the names that row has in common with the subject. A row matches when every one of those names agrees. A name no row carries is not required. A row that lacks a name some other row carried fails the comparison (`None` is not the subject's value) and is dropped. It is not a block. An empty join with an empty reduction slot is the no-link parameter. `_scope` does not read `identity_keys`.

Coverage figures below use box 1 of 1000 and 400, and reductions of 100 and 40, with each reduction keyed identically to its link so a joined link can complete a match. A cross-join publishes **860** and **260**. A one-link join publishes **900** and **360**.

## Part 1 — what joins

Subjects S1 (`demo-lender-a`, `demo-statement-1`, 2025) and S2 (`demo-lender-b`, `demo-statement-2`, 2025), except case 2, where both statements use `demo-statement-shared` and keep different lenders. Link X is borrowing `demo-borrowing-x`. Link Y is `demo-borrowing-y`.

| Case | Joins | Outcome | Test |
| --- | --- | --- | --- |
| 1. Link keyed tax-year + borrowing | X and Y join **both** S1 and S2. The only shared name is tax-year, and both statements are 2025. | Both publish the sum. S1 **860**, S2 **260**. Pins are both links and both reductions. No parameter. | `test_tax_year_and_borrowing_joins_both_statements` |
| 2. Link keyed statement + borrowing, and S1/S2 share a statement id | X and Y join **both** statements. The shared name is statement, and the id was made the same. | Same cross-join: **860** and **260**, both links and both reductions pinned, no parameter. | `test_shared_statement_id_joins_both_lenders` |
| 3. Link keyed lender + statement + tax-year + borrowing | X joins only S1. Y joins only S2. Borrowing is not a statement key, so it does not decide the join; it keeps the two links distinct from each other. | S1 **900** (pins X and its reduction). S2 **360** (pins Y and its reduction). No parameter. | `test_full_statement_identity_joins_only_its_statement` |
| 4. Link keyed lender + tax-year + borrowing | On **this** pair, X joins only S1 and Y joins only S2, because the lenders differ. Statement is not in the key, so the split is the lender values, not the statement identity. | Looks like case 3: **900** and **360**. It is not the same relationship. | `test_lender_and_tax_year_splits_these_two_lenders` |

Case 4 with the lender held constant is a cross-join of the same key names. S1 (`demo-statement-1`) and a third statement (`demo-statement-3`), both `demo-lender-a`, both 2025: X and Y join **both** statements, which publish **860** and **260**. Test: `test_lender_and_tax_year_collides_for_one_lender`.

Status subject: a financing claim keyed borrowing + period + institution + programme. Two claims, borrowings X and Y, share period `2024-autumn`, `demo.institution.riverside`, `demo.programme.bsc`. A third claim, borrowing Z, has the same period and a different institution and programme, so a situation-shaped join and a period-shaped join are distinguishable.

| Case | Joins | Outcome | Test |
| --- | --- | --- | --- |
| Enrolment keyed period + institution + programme. One enrolment for the shared situation (`not-adverse`), one for Z's situation (`adverse`). | The shared enrolment joins X and Y, not Z. Z's enrolment joins Z only. | X and Y publish `not-adverse` and pin the shared enrolment. Z publishes `adverse` and pins its own. Nothing is blocked. Both borrowings of one situation taking one enrolment is the join this rule wants. | `test_full_enrolment_reaches_both_borrowings_of_one_situation` |
| One enrolment, keyed period only, value `not-adverse`. Same three claims. | That enrolment joins X, Y, **and** Z. | All three publish `not-adverse` and pin that one finding. Z's different institution and programme do not keep it out. | `test_period_only_enrolment_reaches_every_financing_in_that_period` |

Two further joins, executed because they change what "fail closed" has to mean:

- A fully keyed link for S1 beside a tax-year-and-borrowing link. The wide row widens the shared-name set to lender + statement + tax-year. The narrow row then matches **nobody** and is not a block. S1 publishes **900** and does not pin the narrow link. S2 publishes **400**, the no-link parameter (`demo.param.no-link-reduction`), and does not pin the narrow link either. A present link was dropped. Test: `test_narrow_link_is_dropped_when_a_wide_link_widens_shared_names`.
- The same drop on the status side. A full enrolment beside a period-only enrolment: the period-only row matches nobody, the financing publishes the full enrolment, and nothing blocks. Test: `test_period_only_row_is_dropped_when_a_full_row_widens_shared_names`.
- Two statement **facts** with the same lender, statement id, and tax year, and different fact ids. One fully keyed link joins **both**. They publish **900** and **300** (the second box is 400). Containment of names accepts this, because the values agree. Test: `test_identical_statement_keys_join_both_facts`.

## Part 2 — the binding relationship

Candidates, applied to the key **names** each Part 1 case actually used:

| Case | (a) joined names contain every subject name | (b) subject names contain every joined name | Right? |
| --- | --- | --- | --- |
| 1. tax-year + borrowing | Reject (no lender, no statement) | Reject (subject has no borrowing) | Reject is right. Both statements took both links. |
| 2. shared statement id | Reject (no lender, no tax-year) | Reject (no borrowing on the subject) | Reject is right. Same cross-join. |
| 3. full statement identity | Accept | Reject (borrowing is not a statement key) | Accept is right. (b) is wrong: this is the join that did not cross. |
| 4. lender + tax-year + borrowing | Reject (no statement) | Reject (no borrowing on the subject) | Reject is right. The different-lender pair happened to split; the same names cross-join when the lender matches. |
| Status, full enrolment | Reject (enrolment has no borrowing) | Accept | Accept is right. X and Y should share that enrolment, and Z should not. (a) would reject the rule. |
| Status, period only | Reject | Accept (`period` is a financing key) | Accept is wrong. Z took an enrolment that does not name its institution or programme. |

(a) alone is the coverage relationship and the wrong status relationship. (b) alone is the status relationship and the wrong coverage relationship: it cannot accept case 3. (c) is (a) or (b) chosen per rule. On these names, coverage declared as (a) and status declared as (b) gives the right answer on cases 1–4 and on the full enrolment, and the **wrong** answer on the period-only enrolment. (c) applied to whatever names a row happens to carry does not rule out every Part 1 cross-join. It is not a proof.

What makes (c) hold for the rows that were run, and what still does not:

**Package validation can check declared names.** `fact-type.v2` requires `identity_keys`, each with a `name`. Bare `fact-type.v2` members are added to the validation fact surface and to `fact_types_by_key` (`package_validation`, the fact-surface walk over `bundle.v1` / `bundle.v2` and over `schema == "fact-type.v2"`). That surface is where a v11 rule's subject pin and joined-type pin can be resolved. The check is name containment in the declared direction, and nothing weaker: one shared name is not a pass. It cannot see values. It cannot see a row that omits a declared key. This walk was read, not executed.

**Runtime has to check every required name on every present row.** Required names are the subject's identity names under (a), and the joined type's declared identity names under (b). A present row that lacks one fails closed: `DEPENDENCY_INVALID`, not an empty join, and not the parameter. A row that has them joins only when every value agrees; disagreement is "not this subject." Today's `_scope` does not do this. Case 1 is a cross-join because the missing names were never required. The narrow-link case is the other failure: the row is dropped, and S2 takes the parameter while the link still exists. The same function, `row_binding`, on that narrow row against the statement identity returns `missing`. On the period-only enrolment against the declared enrolment identity (`period`, `institution`, `programme`) it also returns `missing`. On the full link it returns `join` for S1 and `disagree` for S2.

That presence check rules out every cross-join this probe executed, **if** the declared identities are the ones this brief used: statement `lender` + `statement` + `tax-year`, enrolment `period` + `institution` + `programme`. One malformed row then blocks every subject that sees the candidate list, including a subject that also has a well-keyed row. That is the cost of failing closed instead of dropping the row. It is still not a proof. Three residuals remain:

1. **A weaker declaration.** If the enrolment type's `identity_keys` are only `period`, (b) passes at validation and the presence check passes at runtime. The period-only cross-join comes back as a content decision the check cannot see.
2. **Identical values.** Two statement facts with the same lender, statement id, and tax year both receive the fully keyed link. Containment and presence both accept it. The facts are not distinguishable by identity. The lattice already collapses a rendered-id collision before a consumer sees it; this probe kept the fact ids distinct and the join still hit both.
3. **The reduction's join to status is neither (a) nor (b).** The link's identity is lender + statement + tax-year + borrowing. The status source carries the financing subject's keys: borrowing + period + institution + programme. Neither set contains the other. The live shared name is `borrowing` alone. See Part 3. (c) does not bind that edge.

## Part 3 — scheduling

### Where the intercept goes

Nothing in rule content selects per-subject dispatch. `evaluate_subject_scoped_rule` is only reached when a caller names the subject type. `attempt` does not call it. Its first intercept is the pairing id test (`_try_pairing_scoped`); the rest of the special cases are id tests too; everything else is evaluated once. `is_eligible`'s ordinary answer is `all(req in self.symbols for req in requires)`. `finalize_unreached` does not call `attempt` for an ordinary rule. It evaluates `when` and `value` itself, or records one unsuffixed absence.

`run_reference` indexes producers by the unsuffixed `publishes`. `resolve` returns immediately when that string is in `state.symbols`, skips a rule id already in `resolved`, recurses on `requires`, then calls the same `is_eligible` and `attempt`. It always finishes with `finalize_unreached`. It does not call `try_publish_on_run`.

The per-subject intercept therefore has to land in the three functions both schedulers already share:

- **`is_eligible`**, before the unsuffixed-symbol return. A rule with a declared subject is eligible when every predecessor **rule** is in `resolved`. A predecessor is a rule in this run whose `publishes` equals one of this rule's `requires` entries, or equals this rule's `link_coverage.reductions`. If no rule in the package publishes that name, do not wait. That is the posture `consequence_eligibility` already takes when the supportability rule is absent (traced). Subject facts and other collected sources are not a symbol gate. Do not wait for the unsuffixed name to appear in `self.symbols`.
- **`attempt`**, beside the pairing intercept and instead of the single evaluation. Call `evaluate_subject_scoped_rule` with the declared subject. Do not also evaluate `value` once.
- **`finalize_unreached`**, before the ordinary guard and value fallback. The same call. Otherwise a rule the loop never finds eligible is evaluated once, unsuffixed.

`run_reference` needs no fourth copy if those three change. Its early return on the unsuffixed symbol does not see a keyed publication, and its `rule id in resolved` skip is what stops a second fire. Keyed publication stores `publishes|fact_id` and does not insert the unsuffixed name. That was executed after a one-subject status publish: `is_eligible` on the reduction was false, `demo.tax.schooling-status` was absent from `symbols`, and `demo.tax.schooling-status|demo.fact.financing.x` was present (`test_status_blocked_for_one_financing_blocks_that_link_and_the_statement`). A gate written only against `self.symbols` fixes neither scheduler.

The reductions edge is load-bearing, and it is not `requires`. The amount rule requires box 1 only. Executed (`test_amount_before_reduction_blocks_uncovered_and_stays_resolved`): status ran, then the amount rule, with both links present and no reduction published yet. The statement blocked `DEPENDENCY_INVALID` with both link finding ids, and the amount rule id was resolved. The reduction ran after that. The statement's blocked row stayed the blocked row. An empty reduction slot is an uncovered link, not "the reduction has not run."

### What a predecessor does to the chain

Hand-called order was status (subject: financing), link reduction (subject: the link, `requires` status, value is a ref of status), then the v10 amount rule (subject: box 1). One statement, box 1500, two fully keyed links, borrowings X and Y. The inapplicable guard is `financing > 0`, a numeric stand-in so one subject fails the guard without a categorical domain. The join itself does not depend on that guard.

| Predecessor | Executed? | What the link reduction and the statement see |
| --- | --- | --- |
| Status blocked for borrowing Y only (no enrolment). X publishes. | Executed. `test_status_blocked_for_one_financing_blocks_that_link_and_the_statement` | The status rule id **is** in `resolved` anyway. Y's reduction blocks `DEPENDENCY_ABSENT` / `missing: [status]`. X's reduction publishes. The statement blocks `DEPENDENCY_INVALID` / `missing: [demo.finding.link.y]`. It does not publish 1500−100, and it does not take the parameter. Current `is_eligible` still says the reduction is not eligible. |
| Status blocked for both financings. | Executed. `test_status_blocked_for_every_financing_blocks_every_link` | Rule id still resolved. Both reductions `DEPENDENCY_ABSENT`. The statement blocks both link findings, sorted. Not the parameter. |
| Status inapplicable for Y (guard false) even though Y has an enrolment. | Executed. `test_status_inapplicable_for_one_financing_leaves_no_source` | No status source carries borrowing Y. The only status source is X. Y's reduction is `DEPENDENCY_ABSENT`. The statement blocks `demo.finding.link.y`. From the successor, inapplicable and blocked are the same: no keyed source. |
| Status not called at all. | Executed as data, not as a scheduler. `test_skipping_status_makes_every_reduction_absent` | Status rule id is not resolved. Both reductions `DEPENDENCY_ABSENT`. The statement is uncovered on both links. This is what a successor sees if it runs with no predecessor sources. |
| Predecessor rule absent from the package. | Traced only. | `consequence_eligibility` stays eligible when the predecessor id is not in `ctx.rules`, so the successor runs and records the absence instead of waiting. Current `is_eligible` does the opposite: the symbol is missing, the rule never becomes eligible, and `finalize_unreached` records one unsuffixed `DEPENDENCY_ABSENT`. The don't-wait branch is not in `is_eligible`, so it was not run. |

`evaluate_subject_scoped_rule` adds the rule id to `resolved` after the per-subject rows, including when some or all of them blocked. The blocked runs assert that. Under the predecessor gate, "blocked for one" and "blocked for all" both release the successor. The successor then sees only the published keyed sources. That release is not what the current schedulers do.

### Whether the schedulers agree

They agree with each other, and both miss the chain.

Executed (`test_both_runners_record_ordinary_absence_and_agree`): `run` and `run_reference` on the status rule, the reduction rule, and the amount rule, with none of those symbols present. Both record the same three blocked rows and no publications, none of them keyed:

- status rule, `DEPENDENCY_ABSENT`, missing the enrolment symbol
- reduction rule, `DEPENDENCY_ABSENT`, missing the status symbol
- amount rule, `DEPENDENCY_ABSENT`, missing box 1

Executed (`test_attempt_blocks_scope_unbound_when_box1_is_a_symbol`): with box 1 in `symbols`, `is_eligible` is true and `attempt` evaluates the amount rule once. It blocks `DEPENDENCY_INVALID` / `link-coverage-scope-unbound`. The disposition has no keyed symbol.

Executed (`test_finalize_unreached_evaluates_coverage_once_when_requires_are_met`): the same rule, requires already satisfied, passed only to `finalize_unreached`. Same unsuffixed `link-coverage-scope-unbound`. The ordinary fallback is a real evaluation, not a call to `attempt`.

So: both schedulers share the gap. A change to `is_eligible`, `attempt`, and `finalize_unreached` reaches both. The proposed "not in the package, so do not wait" branch was traced from the pairing helper and was not executed on this chain.

### The reduction joins on borrowing alone

Two financing claims, one borrowing, two periods, two enrolments. The link carries that borrowing and the statement's full identity.

- Values 100 and 40. The reduction blocks `DEPENDENCY_INVALID` and names **both** financing fact ids. The statement blocks uncovered on that link. Test: `test_two_statuses_for_one_borrowing_disagree_and_block`.
- Values both 100. `_one_source` publishes the sort-first status by finding id and does not pin the other. The statement publishes **1400** (1500−100) as if one status had been this link's. Test: `test_two_statuses_for_one_borrowing_agree_and_sort_first_publishes`.

Disagreeing duplicates block. Agreeing duplicates do not. One shared name plus sort-first is the shape the owner rejected.

### ADR 0076 shape

`rule-artifact.v10` is published and `additionalProperties` is false. It has no subject field. `artifact-package.v31`'s member schema enum admits v10 and not a successor. The declaration is a new rule schema and a new package schema.

**`rule-artifact.v11` must declare**, all required, so a v11 rule is per-subject and a v1–v10 rule is not:

- `subject`: a fact-type pin (`id`, `version`). The three rules in the chain do not share a grain. Status is the financing claim. The reduction is the link. The amount is box 1.
- `joined`: a fact-type pin of the type the direction below applies to. `requires` does not identify it. The status rule's subject is one of two requirements. The reduction's subject is not in `requires` at all. The amount rule's subject is box 1, while the type it joins is `link_coverage.links`.
- `direction`: `joined_contains_subject` or `subject_contains_joined`.
  - Amount rule: `joined_contains_subject`, and `joined` is the link fact type. The operator already matches a reduction to a link by the whole key map; the reduction source has to carry that same map, which it does today only because the reduction rule's subject is the link and the published source copies the subject's keys.
  - Status rule: `subject_contains_joined`, and `joined` is the enrolment fact type.

**`artifact-package.v32` must declare** `rule-artifact.v11` in the member schema enum. It does not need a package-level subject map. One map entry can be omitted, and the status rule is the entry that would be omitted: nothing in its bytes currently says it is per-subject. v31 packages stay as they are.

**Package validation**, next to the existing `link_coverage` shape checks, on the fact surface that already includes bare fact types:

- Both pins resolve.
- `joined_contains_subject`: the joined type's `identity_keys` names contain every subject identity name.
- `subject_contains_joined`: the subject type's `identity_keys` names contain every joined-type identity name.
- A `link_coverage` rule's direction is `joined_contains_subject` and its `joined` pin is the `links` type.
- One shared name is not a pass.

**Runtime**, in addition to that, inside per-subject dispatch for a v11 rule:

- Every present row of the joined type carries every required name. A missing name is `DEPENDENCY_INVALID` for that evaluation. It is not dropped, and it is not the no-link parameter.
- A complete row joins only when the required values agree.
- The no-link parameter remains only when no row of the joined type is present.

**The middle of the chain is not this relationship.** The link-reduction rule cannot declare either direction against status and have it pass: the key sets do not contain each other. ADR 0076 should say that explicitly rather than let `_scope` keep joining on `borrowing`. If that edge stays a borrowing join, the runtime obligation is: zero statuses with that borrowing → `DEPENDENCY_ABSENT` (executed); two or more → `DEPENDENCY_INVALID` even when the values agree (not what the code does today; the agreeing pair published 1400). Validation can only check that both types declare the name `borrowing`. That is one shared name. It does not prove the one remaining status is this link's, and two loans that share a borrowing id are one identity.

**Scheduling**, in the same record, because a direction check never runs if production evaluates the rule once:

- Eligibility waits on predecessor rule ids, including the rule that publishes `link_coverage.reductions`, and does not wait when that publisher is absent from the package.
- `attempt` and `finalize_unreached` both dispatch the declared subject, and neither falls through into one unsuffixed evaluation.
- No new record code. `resolved` is already set when some subjects block, which is what lets the successor run and then fail closed per subject.

Until that binding is in force, a result of the v10 operator — including a returned parameter — still does not support a statement-specific claim. ADR 0075 already says so. This probe is the reason: tax year alone, a shared statement id, and a lender without the statement id each put another statement's reduction into the published number, or, when a narrow row sits beside a wide one, drop a present link and return the parameter.

## Verification

```
python3 -m pytest tests/test_sli_g2_binding_probe.py -q
....................                                                     [100%]
20 passed in 2.94s

python3 -m mypy tests/test_sli_g2_binding_probe.py
Success: no issues found in 1 source file
```
