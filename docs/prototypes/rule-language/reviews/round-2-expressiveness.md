# Review Round 2 — Expressiveness and Implementation Results

Reviewer: Codex resume session, 2026-07-10.

Seat: `roles/reviewer-expressiveness.md`.

Artifacts reviewed: `prototypes/rule-language/it2` at `623957c`, directory `rival-rule-language/`.

Comparison baseline: `exhibits/rule-language/it1` and round-1 expressiveness results.

Process disclosure: I did not read `reviews/round-2-governance.md`, `reviews/round-2-adversary.md`, or same-round commit-message bodies before submitting. I did read `examination-it2.md` before running the reproduction checks, although the expressiveness role says to compare the examination after forming independent run results. That ordering defect is disclosed here for the foreman's conformance check. The measurements below are reproducible from the commands and artifact paths named here.

## Check 1 — Coverage

Result: pass for drafted fixture coverage; partial for production-ready operation semantics.

Exhibits:

- Charter fixture list: `docs/prototypes/rule-language/charter-it1.md` F1-F14.
- Rule corpus: `rival-rule-language/artifacts/rules.json`.
- Parameters: `rival-rule-language/artifacts/parameters.json`.
- Fixtures: `rival-rule-language/fixtures/workspaces.json`.
- F10 paper exercise: `rival-rule-language/evolution-probe.md`.
- Package closure: `rival-rule-language/artifacts/package.json`.

Measured coverage:

- F1/F13: `rule:f1.wages-to-1040-line1a`; fixture `f13-post-total-rounding`.
- F2: `rule:f2.interest-gross`, `rule:f2.interest-to-schedule-b-line1`, `rule:f2.schedule-b-line4`, `rule:f2.schedule-b-to-1040-line2b`.
- F3a: `rule:f3a.schedule-b-part-i-applicability`, `rule:f3a.direct-interest-to-1040-line2b`.
- F3b: `rule:f3b.part-iii-applicability`, `rule:f3b.part-iii-questions`; fixture `f1-f3b-f4-f5-f7-table-f8-overpay-f12`.
- F4: `rule:f4.w2-withholding-to-line25a`, `rule:f4.interest-withholding-to-line25b`, `rule:f4.withholding-components-to-line25d`.
- F5: `rule:f5.standard-deduction`, parameter `parameter:standard-deduction.2025`, fixture `f5-open-election`.
- F6: `rule:f6.taxable-income-floor`, fixture `f6-zero-floor`.
- F7: `rule:f7.tax-table-line16`, `rule:f7.worksheet-line16`, parameters `parameter:tax-table-sample.2025`, `parameter:tax-brackets.2025`, fixture `f7-worksheet`.
- F8: `rule:f8.overpayment-line34`, `rule:f8.amount-owed-line37`.
- F9/F14: asserted fact `rounding.convention`, `round` expressions with `stage`, fixtures `f13-post-total-rounding` and `f14-open-rounding-convention`.
- F10: `rival-rule-language/evolution-probe.md`.
- F11: `rule:f11.taxable-interest-no-box3`, `rule:f11.taxable-interest-with-exclusion`, `rule:f11.exclusion-to-schedule-b-line3`, fixture `f11-open-exclusion`.
- F12: `rule:f12.total-income-line9`, `rule:f12.penalty-to-schedule1-line26`, `rule:f12.schedule1-to-1040-line10`, `rule:f12.agi-line11`.

Finding: it2 covers every charter fixture in artifacts and fixtures. The main caveat is not missing coverage but the contract boundary: `round`, `range_lookup`, and `bracket_fold` are declared operation names with artifact-supplied operands and parameter rows, while their exact operation semantics still live in evaluator code pending a versioned semantic specification.

Compared to it1: it2 is tighter. It1 also covered the fixture set, but F9's convention semantics were only partly artifact-declared. It2 names the convention as a fact, names rounding stage inside the expression, enumerates expression operations in schema, and closes the adopted package. The remaining gap is narrower: operation semantics need canon, not hidden tax-specific evaluator branches.

## Check 2 — Reproduction

Result: pass.

Worktree:

```sh
git worktree add /private/tmp/rule-language-it2-expressiveness prototypes/rule-language/it2
```

Command:

```sh
python3 -m unittest discover -s rival-rule-language/tests -v
```

Result from two runs:

- `Ran 8 tests`.
- `OK`.
- Test names: fixture expectations and schema blocking; double-run byte equality; shuffled-artifact byte equality; F13 stage divergence; package closure and scope-as-content; negative kind/id mismatch; bridge deletion attribution; evaluator tax-identifier absence.

This matches the examination's verification claim.

## Check 3 — Double-Run Equality

Result: pass.

Exhibit: `rival-rule-language/tests/test_prototype.py`, `test_double_run_byte_equality`.

The test compares canonical JSON for two consecutive `run_case(case)` calls for every case in `fixtures/workspaces.json`. Both reproduction runs passed.

Compared to it1: equal on the measured property. Both designs passed byte-equal double runs.

## Check 4 — Hard Classes

Result: pass for charter expressiveness; partial for fully canonized operation semantics.

Rounding/ordering:

- Artifact-declared mechanism: `round` expressions name `stage` and take their `mode` from asserted fact `rounding.convention`; affected rules list `rounding.convention` in `requires`.
- Evaluator-carried mechanism: `evaluate_expr` implements `whole_after_aggregate` as `Decimal.quantize(..., ROUND_HALF_UP)`.
- F13 exhibit: `test_f13_stage_divergence` publishes `3` for two `1.49` wages and independently computes the wrong per-input result `2`.
- Comparison: tighter than it1 because stage and mode are inside a schema-enumerated expression shape, but still needs a versioned semantics contract for the operation.

Tables/brackets:

- Artifact-declared mechanism: `parameter:tax-table-sample.2025` supplies row ranges; `parameter:tax-brackets.2025` supplies bracket rows; rules use `range_lookup` below the split and `bracket_fold` at or above it.
- Evaluator-carried mechanism: generic range search and bracket folding over declared rows.
- Comparison: tighter than it1's nested expression evidence because the package separately declares table/bracket parameter citizens and exact member versions. Still not a second-runner portability proof.

Applicability:

- Artifact-declared mechanism: applicability rules publish facts such as `schedule_b.part_i.applicable` and `schedule_b.part_iii.applicable`; false guards publish nothing; unresolved guards become structured blocks.
- Comparison: at least equal to it1, and clearer because applicability uses the same single-publication clause shape as computations and mappings.

Bridges:

- Artifact-declared mechanism: bridge rules have role `cross-form-bridge`, e.g. `rule:f2.schedule-b-to-1040-line2b` and `rule:f12.schedule1-to-1040-line10`.
- Deletion exhibit: `test_bridge_deletion_attribution_under_new_package_version` removes the Schedule B bridge from a new package version; Schedule B line 4 remains while Form 1040 line 2b disappears.
- Comparison: tighter than it1 because the bridge deletion is attributed under a closed package rather than by ad hoc artifact removal.

Method delegation:

- Artifact-declared mechanism: the convention is an asserted choice fact; rules needing it list it in `requires`; F14 with no convention publishes no derived facts and blocks direct amount rules on `rounding.convention`.
- Evaluator-carried mechanism: the meaning of the convention value `whole_after_aggregate` is still the evaluator's implementation of the `round` operation.
- Comparison: stronger than it1 on blocking and stage declaration, but not yet production-ratifiable without a versioned operation-semantics artifact or equivalent schema-level canon.

## Check 5 — Blocking

Result: pass for open elective blocking.

Commands:

```sh
python3 rival-rule-language/evaluator.py --case f5-open-election
python3 rival-rule-language/evaluator.py --case f14-open-rounding-convention
```

Measured results:

- `f5-open-election`: `rule:f5.standard-deduction` blocks with `code: OPEN_ELECTIVE_FACT` and missing `filing_status`; no standard deduction publishes.
- `f14-open-rounding-convention`: no derived facts publish; direct missing-convention blocks include `rule:f1.wages-to-1040-line1a`, `rule:f2.interest-gross`, `rule:f4.w2-withholding-to-line25a`, `rule:f4.interest-withholding-to-line25b`, `rule:f12.penalty-to-schedule1-line26`, `rule:f5.standard-deduction`, and `rule:f7.worksheet-line16`; downstream rules then block on their missing derived inputs.

The no-convention case therefore has no operative default. The open-filing-status case also blocks the dependent standard deduction rather than choosing a filing-status default.

Observation: as in it1, empty source collections can publish zero for facts whose source forms are absent in a fixture. That is not the elective-default failure tested by F5/F14, but it remains relevant to the broader optional-many-to-zero concern.

## Check 6 — Honesty Audit

Result: pass.

The examination disclosed the negative results I observed:

- The below-$100,000 tax-table corpus is fixture-minimal and not deployable law.
- Raw JSON remains unpleasant to read, especially around F7.
- JSON Schema enumerates the operation vocabulary but does not express every operation-specific required-field combination.
- Portability against a second evaluator remains unproven.
- Start/completion records are conceptual evidence, not storage-level fault-injection evidence.
- Operation semantics such as `round`, `range_lookup`, and `bracket_fold` still need versioned semantic specification.

I did not find an additional expressiveness problem omitted by the examination. The main caveat above is already present in its negative result 6.

## Observations

it2 is materially stronger comparative evidence than it1 on contract tightness: closed package membership, schema-enumerated operation names, one publication per rule artifact, bridge deletion attribution, and start/completion record shapes make the behavior easier to isolate. It also independently converges with it1 on expression trees, parameter/rule separation, pin roles, and a derived-publication act kind.

The remaining expressiveness risk is not whether the charter fixtures can be represented. They can. The risk is where to canonize generic operation semantics so the runner remains thin without pretending an enum name alone carries the meaning of rounding, row lookup, and bracket folding.

## Dissent

I do not dissent from treating it2 as stronger than it1 for expressiveness and contract tightness.

I dissent from treating it2 as production-ratifiable as-is because operation semantics are not yet separately versioned canon and because this review has the disclosed examination-before-reproduction ordering defect. I do not dissent from concluding the prototype round if the evaluation analysis records that production ratification requires a versioned operation-semantics contract and second-runner portability evidence later.

## Sign-off — Evaluation Analysis Delta Confirmation (2026-07-11)

Scope: bounded delta-confirmation against `evaluation-analysis.md` and this review only. I performed no new review work and did not re-read peer round-2 reviews for this sign-off.

Result: sign off.

The evaluation analysis faithfully traces this review's expressiveness findings and conditions:

- The review's main production-ratification condition — separately versioned canon for `round`, `range_lookup`, and `bracket_fold` semantics — is recorded in C9 and ratification condition §5.2.
- The review's portability condition — second-runner evidence remains future work — is recorded in ratification condition §5.4 and preserved in the dissent record.
- The review's positive findings on drafted fixture coverage, no-operative-default blocking for open elections, and it2's comparative tightening over it1 are reflected without overstating it2 as production-ratifiable as-is.

No dispute.
