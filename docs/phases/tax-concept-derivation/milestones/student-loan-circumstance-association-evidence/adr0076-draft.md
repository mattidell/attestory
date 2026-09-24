# ADR 0076 — Per-subject scheduling and the two binding relationships

- Status: **proposed**. Parts 1 and 2 are the proposal. Part 3 is not a decision.
- Tier: Parts 1 and 2 are tier 2 — runner and rule-language contracts later rules are written against, the same class as ADR 0075. Part 3 is a tax-conclusion question. It is not tiered, because nothing here selects it.
- Date: 2026-09-24
- Read at: branch `milestone/student-loan-circumstance-association`, HEAD `f0f1dd7630c330f5f1c6c840b8270152641eb8d2`. The probe write-up records itself at `b558da4e`. This draft does not re-run the probes.

This record does not publish a schema. `rule-artifact.v11` and `artifact-package.v32` are names the investigation used for a single package that would have carried scheduling, both relationships, and, by silence, a reading of several statuses on one borrowing. That package is not adopted. The three parts below are separate. Parts 1 and 2 may later be implemented in either order. Neither waits on Part 3. Neither edits `rule-artifact.v10` or `artifact-package.v31`.

## Context

ADR 0075 accepted `link_coverage` as an operator over one bound subject. It returns a reduction total or it blocks. It is not a binding proof. Link rows that share a key name with two statements join to both. Whether a joined list is this statement's links is a property of how the rule is scheduled and of what the link type's identity must contain. Until that binding is established, a result of the operator — including a returned parameter — does not support a statement-specific claim.

The probes in `tests/test_sli_g2_binding_probe.py` are hand-dispatched. They call `evaluate_subject_scoped_rule` directly, or they call the existing runners and record that those runners do not. No production run schedules these rules. `evaluate_subject_scoped_rule` runs only when a caller names the subject type. `runner._execute` never names it. `reference_runner.run_reference` calls the same `is_eligible`, `attempt`, and `finalize_unreached` as `_execute`, and those three do not call it either. A v10 coverage rule that reaches ordinary `attempt` or the ordinary `finalize_unreached` fallback is evaluated once and blocks `link-coverage-scope-unbound`. A status rule, which has no such operator, is evaluated once against the run-wide environment.

The owner wants a subject declaration on each per-subject rule, and wants that scheduling decision kept apart from the relationship check and from the still-open question of what a set of statuses for one borrowing does to the interest. One shared key name is not a binding. Sharing tax year alone is the case that makes that concrete: both statements publish the other statement's reduction.

The chain the probes assemble by hand is three rules and three grains. Status is per financing claim. The link reduction is per link. The amount is per statement (box 1). `requires` does not identify the subject. The status rule's subject is one of two requirements. The reduction's subject is not in `requires` at all. The amount rule's subject is box 1, while the type the operator joins is `link_coverage.links`. The reductions edge is load-bearing and is not a `requires` entry: the amount rule requires box 1 only. An empty reduction slot beside a present link is an uncovered link, not "the reduction has not run" (`test_amount_before_reduction_blocks_uncovered_and_stays_resolved`).

Keyed publication stores `publishes|fact_id` and does not insert the unsuffixed name. A gate written only against `self.symbols` fixes neither scheduler.

## Publication plan (foreman decision, 2026-09-24 — for the owner's review)

**Rule: a published schema version carries only fields whose authorizing decision is accepted before that
version is published. No field is added to a published version; a later field is a later version.** Nothing
below is published by this record.

| Version (names are the next unused ones at publication time) | Fields | Authorizing decision | Published when |
| --- | --- | --- | --- |
| **First rule successor** (currently `rule-artifact.v11`) | `subject` (fact-type pin, required) | ADR 0076 **Part 1** | Only after **both** Part 1 and Part 2 are accepted |
| same | `joined` (fact-type pin), `direction` (`joined_contains_subject` / `subject_contains_joined`) | ADR 0076 **Part 2** | same |
| **First package successor** (currently `artifact-package.v32`) | admits the first rule successor | Parts 1 and 2 | with the first rule successor |
| **Second rule successor** (the version after) | `wording`, `lineNote` (optional strings) | The **reader contract** accepted, and the owner's approval of the sentences | Only after both; never added to the first successor |
| **Second package successor** | admits the second rule successor | same | with the second rule successor |

**Why Parts 1 and 2 ship together.** Part 1 alone would let a production run schedule per-subject rules
over today's `_scope` join, which is the join the hand-dispatched probe showed cross-joining two statements
on tax year alone. Scheduling without the binding would produce statement-shaped results ADR 0075 says
cannot be statement-specific. So the first successor is not published until the binding it needs is
accepted too. The two parts remain separate *decisions*; this is a publication choice.

**Why wording waits for a later version.** The sentences are a separate owner act, and the binding must not
wait on them. Until the second successor exists, per-subject rules carry no sentence, and the reader case
is not complete.

**Part 3** adds no field to either successor. A selected set-level rule is its own rule content.

## Decision — Part 1

**A rule that runs once per subject declares the subject fact type on itself. Both schedulers honour that declaration. They wait until predecessor rules have resolved, not until an unsuffixed symbol appears.**

### What is declared, and where

The declaration is one fact-type pin, `subject`, with `id` and `version`. It is required on the successor and absent on v1–v10, so a rule that carries it is per-subject and a rule that does not is not. The three rules in the chain do not share a grain, so one subject for the package would be false for two of them.

`rule-artifact.v10` is published. `additionalProperties` is false. It has no subject field. The pin is a new rule schema. It is not added to v10. The new schema copies the v10 grammar, including `link_coverage`, and adds `subject`. It does not add `joined` or `direction`. Those are Part 2.

A package schema admits the new rule schema by naming it in the member `schema` enum. `artifact-package.v31` lists `rule-artifact.v10` and has no free string, so admission is a new package schema. That schema does not grow a package-level subject map. v31 packages and v1–v10 rules stay as they are. Forgetting a map entry is how a status rule — nothing in whose bytes today says it is per-subject — would be evaluated once. The pin is on the rule so that omission is not available.

The alternative of a Python identity test, on the pattern of pairing, is not adopted. Pairing's ids are a closed vertical. This operator is a grammar ADR 0075 says a later rule may use. A content rule that passed package validation and was then evaluated once would be the gap ADR 0075 already names: a schema-valid package has not established coverage.

### How both schedulers run it

`runner._execute` and `reference_runner.run_reference` share `is_eligible`, `attempt`, and `finalize_unreached`. `run_reference` needs no fourth copy. Its early return when the unsuffixed symbol is in `state.symbols` does not see a keyed publication. Its skip when the rule id is already in `resolved` is what stops a second fire. It always finishes with `finalize_unreached`.

`is_eligible`, before the ordinary `all(req in self.symbols for req in self._requires(rule))` return, and without disturbing the pairing and nominee identity tests that already sit above that return:

- A rule with a declared subject is not made eligible by the unsuffixed name being in `self.symbols`.
- It is eligible when every predecessor rule is in `resolved`.
- A predecessor is a rule in this run whose `publishes` equals one of this rule's `requires` entries, or equals this rule's `link_coverage.reductions`.
- If no rule in the package publishes that name, do not wait. That is the posture `consequence_eligibility` already takes when the supportability rule is absent. **Traced, not executed** on this chain. The don't-wait branch is not in `is_eligible` today.
- Subject facts and other collected sources are not a symbol gate.

`attempt`, beside the pairing intercept and instead of the single evaluation: call `evaluate_subject_scoped_rule` with the declared subject. Do not also evaluate `value` once.

`finalize_unreached`, before the ordinary guard and value fallback: the same call. A rule the loop never finds eligible is otherwise evaluated once, unsuffixed. Executed today: `test_finalize_unreached_evaluates_coverage_once_when_requires_are_met` returns `link-coverage-scope-unbound` with no keyed symbol. The fallback is a real evaluation. It does not call `attempt`.

No new record code. `evaluate_subject_scoped_rule` already adds the rule id to `resolved` after the per-subject rows, including when some or all of them blocked. Under this gate, "blocked for one" and "blocked for all" both release the successor. The successor then sees only the published keyed sources and fails closed per subject. That release is not what the current schedulers do.

### What a predecessor does, and which tests executed it

Hand-called order was status (subject: the financing claim), link reduction (subject: the link), then the amount rule (subject: box 1). The probes are not the production loop. They are the evidence that the successor's view of a blocked, inapplicable, or missing predecessor is already determined, and that the current schedulers never take that view.

| Predecessor | Test | Executed as | What the successor sees |
| --- | --- | --- | --- |
| Status blocked for one financing | `test_status_blocked_for_one_financing_blocks_that_link_and_the_statement` | Hand-dispatch, then `is_eligible` observed | Status rule id is in `resolved`. That financing's reduction is `DEPENDENCY_ABSENT`, missing the status. The statement is `DEPENDENCY_INVALID`, missing that link. It does not publish a partial subtraction and does not take the parameter. The unsuffixed status symbol is absent; the keyed symbol is present; current `is_eligible` still says the reduction is not eligible. |
| Status blocked for every financing | `test_status_blocked_for_every_financing_blocks_every_link` | Hand-dispatch | Rule id resolved. Both reductions absent. The statement blocks both link findings, sorted. Not the parameter. |
| Status inapplicable for one financing | `test_status_inapplicable_for_one_financing_leaves_no_source` | Hand-dispatch | No keyed source for that financing. Its reduction is `DEPENDENCY_ABSENT`. The statement blocks that link. From the successor, inapplicable and blocked are the same. |
| Status not called | `test_skipping_status_makes_every_reduction_absent` | Data, not a scheduler | Status rule id is not resolved. Both reductions absent. The statement is uncovered on both links. |
| Amount rule before any reduction | `test_amount_before_reduction_blocks_uncovered_and_stays_resolved` | Hand-dispatch | Statement blocks `DEPENDENCY_INVALID` with both link finding ids. The amount rule id stays resolved. The blocked row stays the blocked row. |
| Predecessor rule not in the package | — | **Traced only**, from `consequence_eligibility` | Do not wait; the successor runs and records the absence. Not run on this chain. |
| Both runners, no symbols present | `test_both_runners_record_ordinary_absence_and_agree` | `run` and `run_reference` | The same three unsuffixed `DEPENDENCY_ABSENT` rows. No keyed publication. The schedulers agree with each other and both miss the chain. |
| Box 1 already a symbol | `test_attempt_blocks_scope_unbound_when_box1_is_a_symbol` | `attempt` | One unsuffixed `link-coverage-scope-unbound`. |

Part 1 does not make a joined list this statement's links. ADR 0075's sentence stands until Part 2 is in force as well: a result of the operator, including a returned parameter, still does not support a statement-specific claim. Part 1 makes a production run evaluate the declared subject. It does not decide the tax question in Part 3.

### What Part 1 requires, and what it leaves open

Schema: `subject` on the first rule successor, published together with Part 2's fields once both parts are accepted (publication plan above); a package successor admits it. a new package schema that admits that rule schema and does not carry a subject map. Checksums appended with `packages.kernel.schema_registry.write_manifest` for the new filenames only. Published v10 and v31 bytes stay put. Every closed schema-name set that lists `rule-artifact.v10` has to admit the successor or a successor rule never runs. The investigation names `live._resolved_run_material`, `package_validation`, `authorization_closure`, the runner's rule-schema tuples, and `marshal._rule_required_symbols`. That list was traced at the investigation's commit. It was not re-derived at this HEAD.

Code: the three functions above. Pairing is unchanged. Ordinary rules keep today's `requires` test against `self.symbols`.

Tests, which the hand probes are not: both runners dispatch a declared-subject rule and do not also evaluate it once; eligibility waits on the reductions publisher even though that name is not in `requires`; a blocked predecessor and an inapplicable predecessor each release the successor, which then fails closed per subject and does not take the no-link parameter while a link row exists; `finalize_unreached` takes the same path; the don't-wait branch, today only traced, is executed when the publisher is absent from the package; a v1–v10 rule is unchanged.

Left open by this part: `joined` and `direction`; the reduction-to-status edge; what several statuses do to the interest; the return-level aggregator that would read keyed statement amounts after the per-subject rule has resolved (inferred in Question 1, not one of the three chain rules, not decided); the reader. Scheduling does not show anyone the result.

## Decision — Part 2

**Two relationships are declared on the rule and checked by containment of identity-key names, one direction each. One shared name is not a pass. At runtime every present row carries every required name or the evaluation fails closed. This part does not schedule the rule, and it does not decide Part 3.**

It can be accepted without Part 3. It does not depend on Part 1's eligibility rule. Until Part 1 is also in force, production still evaluates the rule once and these checks do not run. Until this part is in force, Part 1's per-subject result is still not a statement-specific claim.

### The two relationships

The direction is declared because neither direction is right for both joins. The probe applied both to the key names each case actually used.

**Statement to link: `joined_contains_subject`.** The link type's declared `identity_keys` names contain every subject identity name. Extra names on the link, including borrowing, do not have to be statement keys.

This is the relationship that accepts the join which did not cross and rejects the joins which did.

- Full statement identity (lender + statement + tax-year + borrowing) joins each link only to its statement. 900 and 360. `joined_contains_subject` accepts. `subject_contains_joined` rejects, because borrowing is not a statement key, and that rejection is wrong. `test_full_statement_identity_joins_only_its_statement`. `row_binding` returns `join` for that statement and `disagree` for the other.
- Tax year plus borrowing joins both links to both statements. 860 and 260. Both directions reject. Reject is right. `test_tax_year_and_borrowing_joins_both_statements`.
- A shared statement id, with no lender and no tax year on the link, is the same cross-join. Both directions reject. `test_shared_statement_id_joins_both_lenders`.
- Lender plus tax year plus borrowing, without the statement id, splits the two different lenders (900 and 360, `test_lender_and_tax_year_splits_these_two_lenders`) and cross-joins when the lender is the same (860 and 260, `test_lender_and_tax_year_collides_for_one_lender`). The split is the values. The relationship is the same, and containment rejects it. One shared name would have accepted the tax-year case.

A `link_coverage` rule's direction is `joined_contains_subject`, and its `joined` pin is the `links` type. The operator already matches a reduction to a link by the whole key map. This direction is what makes the joined links the subject's.

**Financing to enrolment: `subject_contains_joined`.** The financing subject's declared identity names contain every enrolment identity name.

- Enrolment keyed period + institution + programme reaches both borrowings of that situation and not the third. `test_full_enrolment_reaches_both_borrowings_of_one_situation`. `subject_contains_joined` accepts. `joined_contains_subject` rejects, because the enrolment has no borrowing key, and that rejection is wrong.
- Enrolment keyed period only reaches every financing in the period, including one with a different institution and programme. `test_period_only_enrolment_reaches_every_financing_in_that_period`. `subject_contains_joined` accepts. That acceptance is wrong for a situation-shaped enrolment, and it is what a weak declaration looks like. The check does not correct it. See the residuals.

### Package validation

On the fact surface that already includes bare `fact-type.v2` members. That walk was **read, not executed**. `fact-type.v2` requires `identity_keys`, each with a `name`.

- Both pins resolve: `subject`, and `joined`.
- `joined_contains_subject`: the joined type's identity names contain every subject identity name.
- `subject_contains_joined`: the subject type's identity names contain every joined-type identity name.
- Nothing weaker. One shared name is not a pass. The tax-year cross-join, the shared-statement-id cross-join, and the lender-without-statement cross-join are the tests that sentence is for.
- A `link_coverage` rule whose direction is not `joined_contains_subject`, or whose `joined` pin is not the `links` type, is rejected.

The check sees declared names. It does not see values. It does not see a row that omits a declared key. It does not invent a stronger identity than the fact type declares.

### Runtime presence

Inside per-subject dispatch, in addition to the static check. Required names are the subject's identity names under `joined_contains_subject`, and the joined type's declared identity names under `subject_contains_joined`.

- Every present row of the joined type carries every required name. A present row that lacks one is `DEPENDENCY_INVALID` for that evaluation. It is not dropped. It is not the no-link parameter.
- A complete row joins only when the required values agree. Disagreement is not this subject.
- The no-link parameter remains only when no row of the joined type is present.

Today's `_scope` does not do this. Shared names are the union, across every candidate row, of the names that row has in common with the subject. A row that lacks a name some other row carried fails the comparison and is dropped. It is not a block. An empty join with an empty reduction slot is the parameter. Executed:

- `test_narrow_link_is_dropped_when_a_wide_link_widens_shared_names`. S1 publishes 900 and does not pin the narrow link. S2 publishes 400, the parameter `demo.param.no-link-reduction`, and does not pin the narrow link either. A present link was dropped. `row_binding` of that narrow row against the statement identity returns `missing`.
- `test_period_only_row_is_dropped_when_a_full_row_widens_shared_names`. The period-only enrolment matches nobody. Nothing blocks.

`row_binding` of the period-only enrolment against the declared enrolment identity (period, institution, programme) returns `missing` (`test_period_only_enrolment_reaches_every_financing_in_that_period`). On the full link it returns `join` for one statement and `disagree` for the other, as cited above.

Failing closed has a cost the drop does not: one malformed row blocks every subject that sees the candidate list, including a subject that also has a well-keyed row. That cost is accepted. Dropping the row and returning the parameter is the defect the probes measured.

The presence check rules out every cross-join this probe executed **if** the declared identities are the ones the probe used: statement `lender` + `statement` + `tax-year`; enrolment `period` + `institution` + `programme`. This part does not publish those lists. It enforces whatever the fact types declare. A5's keying is a content decision. A weaker declaration is the first residual.

### Residuals, which this part does not close

1. **A weaker declaration.** If the enrolment type's `identity_keys` are only `period`, `subject_contains_joined` passes at validation and the presence check passes at runtime. The period-only cross-join comes back as a content decision the check cannot see. The check's job is the declaration, not a guess that the declaration was too small.
2. **Identical values.** `test_identical_statement_keys_join_both_facts`: two statement facts, same lender, statement id, and tax year, different fact ids. One fully keyed link joins both. They publish 900 and 300. Containment and presence both accept it. The facts are not distinguishable by identity.
3. **The reduction's join to status is neither direction.** The link's identity is lender + statement + tax-year + borrowing. The status source carries the financing subject's keys: borrowing + period + institution + programme. Neither set contains the other. The live shared name is `borrowing` alone. Part 2 does not validate that edge, and it does not authorize leaving `_scope` to join it on `borrowing`. One shared name is the relationship this part rejects. What several statuses for one borrowing do to the interest is Part 3. It is not a third containment, and it is not "both types declare the name `borrowing`."

### What Part 2 requires, and what it leaves open

Schema: `subject`, `joined` (a fact-type pin), and `direction` (`joined_contains_subject` or `subject_contains_joined`), on the first rule successor, published with Part 1's `subject` once both parts are accepted — see the publication plan above. Neither part edits a published file.

Code: the validation checks next to the existing `link_coverage` shape checks; the presence check inside per-subject dispatch for a rule that declares a direction. `_scope` for rules without that declaration stays as it is. No new record code: a missing required name is `DEPENDENCY_INVALID`.

Tests: the cross-join name sets fail both directions; full statement identity passes only `joined_contains_subject`; full enrolment passes only `subject_contains_joined`; a period-only enrolment declaration passes `subject_contains_joined` and the test asserts that pass, so the residual is not "fixed" by accident; a present narrow row and a present period-only row against the full declared identity are `DEPENDENCY_INVALID`, not a drop and not the parameter; identical key values still join both facts; a `link_coverage` rule with the wrong direction or the wrong `joined` pin is rejected. The existing probe file shows today's joins. It is not these tests.

Left open: the three residuals; Part 3; production scheduling, which is Part 1; the reader.

## Decision — Part 3

**Not made.** How a set of statuses for one borrowing affects the tax conclusion is a decision for the owner. This ADR does not select an option. The options are not implied by the join, and they are not implied by one example.

`test_two_statuses_for_one_borrowing_disagree_and_block` blocks, and names both financing fact ids, when two statuses for one borrowing disagree. `test_two_statuses_for_one_borrowing_agree_and_sort_first_publishes` publishes the sort-first status and the statement publishes 1400 when the two values agree. That pair is a borrowing-only join plus sort-first. It is not § 221. Disagreeing duplicates block; agreeing duplicates do not. "Any adverse status disqualifies the loan" cannot be taken from it, and cannot be taken from the spring-2025 case alone.

The workings, the full quotations, and the scoring are in [`adr0076-notes.md`](adr0076-notes.md). The operative text, quoted from the sources named there:

§ 221(a) allows "the interest paid by the taxpayer during the taxable year on any qualified education loan."

§ 221(d)(1): a qualified education loan is "any indebtedness incurred by the taxpayer solely to pay qualified higher education expenses" that meet (A), (B), and (C). (C) is expenses "attributable to education furnished during a period during which the recipient was an eligible student." "Solely" qualifies the indebtedness. (C) qualifies the expenses. Neither sentence says that any adverse status in a set disqualifies the loan.

§ 221(d)(2) defines qualified higher education expenses as the cost of attendance at an eligible educational institution, reduced by the amounts (A) and (B) name. It does not mention the eligible student and does not split a loan across periods.

§ 221(d)(3) gives "eligible student" the meaning in § 25A(b)(3): with respect to any academic period, a student who meets HEA § 484(a)(1) as in effect on 5 August 1997, and who is carrying at least half the normal full-time workload for the course of study pursued. The historical HEA sentence was not quoted in this pass. Where a case stipulates that the person was not an eligible student, (C) is applied to that stipulation.

§ 1.221-1(e)(3)(i) repeats "solely" and places the eligible-student condition on the academic period. Its parenthetical — "a degree candidate carrying at least half the normal full-time workload" — is a gloss, not the HEA sentence, and not Publication 970's wider "degree, certificate, or other recognized educational credential." Those three wordings are not reconciled here.

§ 1.221-1(e)(3)(ii) makes the reasonable period facts and circumstances, with two safe harbors. The second is per academic period: proceeds disbursed from 90 days before that period to 90 days after it. None of the cases states a disbursement date, so none of them is decided on this paragraph. Example 4 is one promissory note covering two semesters, both inside the qualified class, held to meet the safe harbor disbursement by disbursement. It treats the note as one loan. It does not authorize a split, and it does not decide an ineligible semester.

§ 1.221-1(e)(4), Example 6, is the only mixed-use decision: part of the proceeds pay qualified higher education expenses and part pay for improvements to a residence, and "the loan is not a qualified education loan." The other use is not an ineligible academic period. There is no fraction.

§ 1.221-1(f)(1) deducts interest paid on a qualified education loan. § 1.221-1(f)(3) allocates a payment between interest and principal. It does not allocate interest between qualified and unqualified uses, or between academic periods. § 1.221-1(g)(1): interest paid while the loan is not in repayment can still be deducted. The year of payment is not the eligible-student test.

§ 1.221-1(e)(3)(v)(B), treatment of refinanced and consolidated indebtedness, is reserved. It is not a portion rule and not a set rule. § 1.221-1(a)(1) and (h) still recite a 2010 applicability limit. This draft does not resolve whether that limit is spent. Publication 970 (2025) is secondary and is not used to decide a case.

### The cases, against that text

**(a) One loan finances autumn 2024 (eligible) and spring 2025 (not an eligible student: no credential-programme enrolment anywhere that term).** Spring expenses fail (C). Autumn expenses do not fail (C) on the stipulated status. The indebtedness then paid some expenses inside that condition and some outside it. If an expense that fails (C) is a non-qualified use in the sense of Example 6, the chapeau's "solely" means the loan is not a qualified education loan at all, and § 221(a) allows none of the interest. That step crosses a gap: Example 6 is a home improvement, not a second academic period, and no sentence allocates the interest the other way. The loan is not shown to be "partly" a qualified education loan. Reasonable-period is undetermined.

**(b) One loan finances two concurrent situations in one period: a degree programme at one school, non-credential classes at another.** (C) and § 25A(b)(3) put eligible student on the student for the academic period, not on each programme. A degree programme in that period can satisfy the status. Nothing quoted says the second enrolment revokes it or subtracts from it. Whether the non-credential expenses are themselves qualified higher education expenses under § 221(d)(2) is not in the facts (eligible institution, cost of attendance, the reductions). Half-time is not in the facts. The loan is not shown to fail (C), and it is not shown to be a qualified education loan. Carving the classes out, or disqualifying the loan because one situation is non-credential, adds a rule the text does not have. This is the reading A5 withdrew for the Metro enrolment. The withdrawal is consistent with the quoted sentences. It is not itself the decision.

**(c) One loan finances only an ineligible period.** (C) fails for the expenses that indebtedness was incurred to pay. It is not a qualified education loan. No interest paid on it is allowed under § 221(a). Describing it as a qualified loan with a zero portion uses a classification the term does not. Treating the classification as unresolved refuses a conclusion the statute makes.

**(d) Two loans, each financing one period.** Each indebtedness is tested alone. The loan that financed only an ineligible period is (c). The loan that financed only an eligible period is a qualified education loan only if its own expenses also meet "solely," (A), (B), and § 221(d)(2); (C) does not fail for it, and the other loan's failure does not move. § 221(a) is interest on any qualified education loan, per loan. A set of statuses pooled across loans gets this case wrong. Consolidation is a different indebtedness, and its treatment is reserved. These facts are not a consolidation.

**(e) A loan whose status for one period is unknown.** (C) requires that the recipient was an eligible student during that period. An absent account does not make (C) true and does not make it false. Example 6 does not apply, because a non-qualified use is not known. No default is in § 221. The product's existing posture — a favourable eligible-student value where no enumerated disqualifier is supported, recorded as default-supported, and not the same thing as adverse information of unresolved scope — is a candidate answer to this silence and is not selected, extended, or withdrawn. Whole-loan disqualification reaches (e) only by relabeling unknown as failure.

### Options, none selected

**Whole-loan disqualification.** A known use outside (A), (B), and (C) means the indebtedness was not incurred solely to pay qualified higher education expenses, so it is not a qualified education loan and none of its interest is allowed. Tracks the chapeau and Example 6 for a known non-qualified use. Gets (c) right, and gets (d) right only per loan. Gets (a) right only across the Example 6 gap. Does not disqualify (b) on the facts given. Does not decide (e).

**Portion-based.** Deduct the interest in proportion to the proceeds that paid expenses meeting (A), (B), and (C). No quoted sentence states that proportion. Example 6 decides the loan rather than a part of the interest. (f)(3) is interest versus principal. Does not get (a), (b), or (e) right on the text. Reaches zero on (c) by calling the loan partly qualified, which is not what the term says. Is not what separates the two loans in (d).

**Unresolved-blocks.** Where the statuses do not determine "solely," the interest treatment for that indebtedness is not determined and no deduction proceeds on it. Matches the silence in (e), and matches what (b) actually leaves open (cost of attendance, half-time, institutional eligibility). It is a response to the text, not a sentence in the text. It is the wrong posture for (c), and for (a) if the Example 6 application is accepted. It is the wrong posture for (d)'s ineligible loan, and for (d)'s eligible loan if that loan is blocked because the other failed.

No option gets every case right on the text alone. The owner decides. Until one is decided, the reduction-to-status edge has no accepted relationship: Part 2 does not bind it, and this part does not replace the borrowing-only join with a selected tax rule.

### What Part 3 would require, once an option is selected

Not required by this proposed record, and not to be built from it.

A selected option is a tax contract, not a field on the Part 1 or Part 2 schema. It needs its own rule, over the financing claims of one indebtedness, and tests that state which of (a)–(e) that rule gets right and which it refuses. It does not need a new record code unless the selected option is unresolved-blocks and a later reader decision says `DEPENDENCY_INVALID` is the wrong shape — ADR 0075 already left a distinct code unmade on the coverage evidence, and this part does not reopen that. It does not need a schema successor of its own unless the selected rule cannot be written in the grammar Parts 1 and 2 leave. That cannot be known before the selection.

Adopting the product's default for (e) is an owner decision about an existing posture, not a consequence of Part 1 or Part 2. Adopting whole-loan disqualification for (a) should say, in the selecting record, that Example 6's other use is a residence and that the academic-period case is an application of "solely." Adopting a portion rule should say where the fraction is written, because it is not in § 221 or § 1.221-1.

## Evidence boundary

The probes are hand-dispatched. Calling `evaluate_subject_scoped_rule` with a subject type, or calling `run` and `run_reference` and recording an unsuffixed absence, is not production behaviour. No production path schedules a status rule, a link-reduction rule, or a coverage rule onto per-subject dispatch. The join results (860 against 260, the dropped narrow link, the parameter returned while a link still exists, the two-status block, the sort-first 1400) are measurements of the current hand-called machinery. They are not what a production run records today, because a production run does not evaluate these rules per subject.

Part 1 and Part 2, once implemented, are what would make a production run do the scheduling and the presence check. They are not implemented by this draft. Part 3 is not a description of either. A green suite on the current tree would not be evidence for any of the three: the tree does not contain them.

`row_binding`'s `join`, `disagree`, and `missing` results cited above are assertions inside the named probe tests, not a separate traced note. The don't-wait predecessor branch, the package-validation fact-surface walk, and the closed schema-name sets are traced. The authority quotations were fetched this pass; the case applications are workings, not executed tax results.

## Links

- Notes and quotations: [`adr0076-notes.md`](adr0076-notes.md)
- Predecessor: `docs/adr/0075-link-coverage-operation.md`
- Probes: `docs/phases/tax-concept-derivation/milestones/student-loan-circumstance-association-evidence/g2-binding-and-scheduling.md`, `tests/test_sli_g2_binding_probe.py`
- Scheduling trace: `g2-path-investigation.md` Question 1
- Facts and keying: `a0-tax-concept-facts.md` (F5, F6, F9); `a5-stage2-circumstances-and-keying.md` (tests 1–3 and the adverse case); `whose-deduction-model.md`
- Authority: 26 U.S.C. § 221(a), (d)(1), (d)(2), (d)(3); 26 U.S.C. § 25A(b)(3); 26 CFR § 1.221-1(e)(3), (e)(4) Examples 4 and 6, (f)(1), (f)(3), (g)(1). Publication 970 is secondary and is confined to the notes.
