# Track 0f — mechanism rows

> **Curation note.** The disposable probe this report ran was removed when the milestone was prepared for publication. The commands below are kept as a record; the results recorded here are the evidence.

## Item 1 — stale targets wired in

Command: `PYTHONPATH=. python3 docs/phases/tax-concept-derivation/milestones/student-loan-deduction-completion-evidence/track0f_probe.py item1`. Exit 0. Both runners agreed on every case.

The Track 0d chain gains two joins. A financing subject requires the schooling fact, direction `subject_contains_joined`, and publishes `demo.tax.track0f.financing-schooling` as a ref of that fact. The inclusion support rule requires box 1 and that publication. Package validation of this wiring succeeded. The financing join does not use the stand-in. The support value still does, so a published support or conclusion is executed with the runtime stand-in operator. A block of the financing join, or a block that only says the publication is absent, is executed existing engine. The worksheet dollar that is fed a stand-in conclusion is executed with the runtime stand-in operator. Presentation is presentation only. Income is the harness figure `50000`. The box amount passed to the worksheet is the harness figure `3000`.

| Case | Financing join | Inclusion support | Statement | Worksheet | Presentation |
| --- | --- | --- | --- | --- | --- |
| Plain, schooling and box current | publishes `demo schooling` | 1 | plain-case-supported | 2500 | published value 2500 |
| Schooling row absent | `DEPENDENCY_ABSENT`, missing `tax.us.2025.sli.schooling-situation` | `DEPENDENCY_ABSENT`, missing `demo.tax.track0f.financing-schooling` | `DEPENDENCY_INVALID`, missing the inclusion finding; no conclusion | no line 21, `DEPENDENCY_ABSENT`, missing `demo.tax.track0d.statement-conclusion` | blocked, `DEPENDENCY_ABSENT` |
| Schooling finding not current | same block | same block | same block | same block | same |
| Statement finding not current | publishes `demo schooling` | `DEPENDENCY_ABSENT`, missing `tax.us.2025.f1098e.box1-student-loan-interest` | no conclusion and no statement block; the box is not a current subject | no line 21, `DEPENDENCY_ABSENT`, missing the conclusion symbol | blocked, `DEPENDENCY_ABSENT` |
| Statement row absent | publishes `demo schooling` | same box block | same; no statement subject | same block | same |

The plain case still deducts 2500. A stale schooling does not become `not-supported`. It blocks the financing subject, the inclusion then blocks because that publication is absent, and the statement blocks because the inclusion support row is absent. A stale statement blocks the inclusion on the missing box. The statement rule itself does not run, so it does not publish `not-supported` either. In every stale case the worksheet receives no conclusion and blocks `DEPENDENCY_ABSENT` rather than deducting. The presentation explain sentence was not captured by this call.

The authority-lifecycle joins are in the chain. A blocked subject still publishes no row. Item 2 is the worksheet check for that missing row.

## Item 2 — coverage of every statement

Command: `PYTHONPATH=. python3 docs/phases/tax-concept-derivation/milestones/student-loan-deduction-completion-evidence/track0f_probe.py item2`. Exit 0. Income is the harness figure `50000`.

A return-level rule cannot read subject-scoped publications on a path both runners agree on. The tried rule is `rule-artifact.v10`, which has no subject and has `collect_categorical_all_equal`. It sits in the same derivation run as the wired chain. Label for that rule: executed existing engine. The chain conclusions beside it are executed with the runtime stand-in operator.

| Return-level rule | One plain statement | Two plain statements | One plain and one blocked |
| --- | --- | --- | --- |
| No `requires`. Collects the conclusion symbol and expects `plain-case-supported` | Runners disagree. Forward blocks `DEPENDENCY_ABSENT`, missing the conclusion symbol, and publishes nothing. Reference publishes `true` and pins the conclusion finding | Same split. Reference publishes `true` and pins both conclusion findings. Forward blocks and publishes nothing | Same split. Reference publishes `true` and pins the one conclusion that exists. Forward blocks and publishes nothing |
| `requires` the conclusion symbol | Both runners block `DEPENDENCY_ABSENT`, missing that symbol, and publish nothing. The chain has published `plain-case-supported` | Both runners block the same way. The chain has published two `plain-case-supported` rows | Both runners block the same way |

The keyed publication never fills the unsuffixed symbol the return-level `requires` test waits on, so declaring the dependency blocks the rule instead of letting it read the rows. Leaving the dependency off lets one runner see the rows and the other miss them.

A later subject-scoped rule can read them. It is a box 1 subject, `joined` to a conclusion fact type with the box keys, direction `joined_contains_subject`, `requires` the conclusion symbol, value one `link_count` of that fact type. Both runners agree. Label: executed existing engine. One plain statement publishes count `1`. Two plain statements publish `1` and `1`. The statement whose chain blocked publishes no count and blocks `DEPENDENCY_ABSENT`, missing the conclusion symbol, subject that box. Two `link_count` nodes in one value do not validate: `LINK_COUNT_INVALID`, detail `link_count must appear exactly once in value and never in when`. That package was not run.

The worksheet mechanism uses those existing operators on the worksheet run, where the chain's publications are already sources. The candidate worksheet is cloned. Its closed-empty branch is unchanged: a box 1 count of `0` on source set `tax.us.2025.f1098e.1` still publishes `0`. On the nonempty branch the clone refuses unless that box count equals the count of result rows, read with the same `count` operator and the same source set, and `collect_categorical_all_equal` accepts only the favorable value. The refusal is `block` code `SLI_STATEMENT_COVERAGE`. Both worksheet runners agree on every case below. The count, the collect, and the block are executed existing engine. A line 21 dollar that is fed a stand-in conclusion is executed with the runtime stand-in operator. Presentation is presentation only.

New path. The chain is the wired Track 0f chain.

| Worksheet inputs | Line 21 | Runner blocked code | Presentation |
| --- | --- | --- | --- |
| One plain statement, box `3000` | 2500 | none | published value 2500 |
| Two plain statements, boxes `3000` and `3000` | 2500 | none | published value 2500 |
| `plain-case-supported` and `not-supported`, both boxes kept | no line 21 | `SLI_STATEMENT_COVERAGE`, missing empty | blocked, codes `DEPENDENCY_INVALID`, value absent |
| The `not-supported` row omitted, both boxes kept | no line 21 | `SLI_STATEMENT_COVERAGE`, missing empty | blocked, codes `DEPENDENCY_INVALID`, value absent |
| One statement blocked and published nothing, both boxes kept | no line 21 | `SLI_STATEMENT_COVERAGE`, missing empty | blocked, codes `DEPENDENCY_INVALID`, value absent |
| Closed empty family, no boxes and no conclusions | 0 | none | computed zero 0 |

The blocked statement is the second box with its schooling row absent. Its financing join blocks `DEPENDENCY_ABSENT`, missing `tax.us.2025.sli.schooling-situation`. The inclusion then blocks missing `demo.tax.track0f.financing-schooling`. The statement blocks `DEPENDENCY_INVALID`, missing the inclusion finding, and publishes no conclusion. The `not-supported` statement is a box with no inclusion. The chain publishes `plain-case-supported` and `not-supported`.

Old path. For each of the five answers, a box 1 subject does one real `link_count`, then publishes `missing` when the count is `0` and `answered` otherwise. Label: executed existing engine. There is no stand-in node. The same worksheet gate expects `answered`. Two boxes of `3000`. The same four results on every answer: `no-related-person-interest`, `no-non-qualified-loan-component`, `no-qualified-employer-plan-interest`, `no-employer-educational-assistance-interest`, `no-qtp-earnings-used`.

| Inputs | Status rows | Line 21 | Presentation |
| --- | --- | --- | --- |
| Both statements, one answer present | `answered`, `missing` | no line 21, `SLI_STATEMENT_COVERAGE` | blocked, `DEPENDENCY_INVALID` |
| The `missing` row omitted, both boxes kept | `answered` only | no line 21, `SLI_STATEMENT_COVERAGE` | blocked, `DEPENDENCY_INVALID` |
| One statement, its answer present | `answered` | 2500 | published value 2500 |
| The absent answer blocks instead of publishing `missing` | `answered` only, plus `DEPENDENCY_ABSENT` with empty missing on the other statement | no line 21, `SLI_STATEMENT_COVERAGE` | blocked, `DEPENDENCY_INVALID` |

The block op publishes nothing for the statement that has no answer. The runner records that block as `DEPENDENCY_ABSENT` with empty missing. The worksheet sees one `answered` row and two boxes and refuses.

`SLI_STATEMENT_COVERAGE` is the runner's blocked code. It is not a recorded disposition code, so the disposition and the presentation both show `DEPENDENCY_INVALID`. The presentation explain sentence is unchanged: "Schedule 1 line 21 is blocked because eligibility authority is incomplete, an excluded class is present, the filer is married filing separately, or the Form 1098-E box-1 family is unclosed." The person does not see the coverage code.

The plain deduction is still 2500. Two supported statements are still the cap, 2500. A closed empty family is still 0. The question wording is unchanged. The empty/nonempty row closes: omitting a statement's row no longer deducts. No new operator is required for that refusal. A same-run return-level reader would be a different requirement, and this worksheet check does not add one.

## Item 3 — presence detection for old and new inputs

Command: `PYTHONPATH=. python3 docs/phases/tax-concept-derivation/milestones/student-loan-deduction-completion-evidence/track0f_probe.py item3`. Exit 0. Both runners agree on every case that ran. Label: executed existing engine. There is no stand-in node in the selection clone. Presentation is presentation only.

The worksheet clone keeps the candidate worksheet's id and its line 21 publication. Selection is the line 2b shape: mode `exclusive_presence`, conflict `refuse`, paths `old` and `new`, each `source_nonempty`, default id `neither`, refusal code `DEPENDENCY_INVALID` with missing `old-and-new-sli-inputs-both-present`. The old path value is the candidate worksheet's value. The new path value is that value with the old-fact collect swapped to the chain conclusion. The default value is `0`. Top-level `value` is removed, because this schema allows selection or a value, not both. `when` is true, and `requires` and `pins` are empty.

| Clone | Validation |
| --- | --- |
| Worksheet schema `rule-artifact.v6`, value kept, selection added | rejected. `SchemaValidationError`: instance does not conform to rule-artifact.v6: `<root>`: Additional properties are not allowed (`selection` was unexpected) |
| Same clone moved to `rule-artifact.v9`, worksheet values on the paths | accepted |
| Same v9 shape with literal path values `2500`, `2500`, and `0` | accepted, and not run, because the worksheet-value clone already validated |

The v9 clone was run as old-only, new-only, both present, and neither, through the real runner and the line 21 presentation consumer. Old-only has the old fact and a box of `3000`. New-only has one `plain-case-supported` conclusion and a box of `3000`, and no old fact. Both has the old fact and the conclusion. Neither has neither, and no box.

All four cases produce the same block. No line 21 value is published. The runner blocked code is `DEPENDENCY_INVALID`, missing `v9-declarative-binding-unauthorized`. The disposition code is `DEPENDENCY_INVALID`. The presentation disposition is blocked, the value is absent, and the active code is `DEPENDENCY_INVALID`. The person-visible sentence in every blocked case is: "Schedule 1 line 21 is blocked because eligibility authority is incomplete, an excluded class is present, the filer is married filing separately, or the Form 1098-E box-1 family is unclosed." The presentation does not show `v9-declarative-binding-unauthorized` or `old-and-new-sli-inputs-both-present`.

The selection declaration is schema-valid and is not evaluated. The four presence inputs are not distinguished. The integration-surface row stays open. The smallest missing behavior is a runtime binding of this same `exclusive_presence` / `refuse` declaration for the worksheet rule. Old-only must evaluate the old path and may publish the deduction. New-only must evaluate the new path and may publish the deduction. Both present must block `DEPENDENCY_INVALID` with missing `old-and-new-sli-inputs-both-present`. Neither must evaluate the default path. The failing case is the validated clone above: every presence case blocks on `v9-declarative-binding-unauthorized` instead. The question wording is unchanged, and this item publishes no deduction.
