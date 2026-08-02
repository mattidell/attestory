# Review Round 1 — Expressiveness and Implementation Results

Reviewer: Codex resume session, 2026-07-10.

Seat: `roles/reviewer-expressiveness.md`.

Artifacts reviewed: `prototypes/rule-language/it1` at `362f8a3`, directory `prototype-rule-language-it1/`.

Process disclosure: I did not open `reviews/round-1-governance.md`, but I saw the process log's one-line summary of that completed review during required re-entry, and I opened `examination-it1.md` before forming all independent run results. That is a reviewer-process defect. The measurements below are still reproducible from the commands and artifact paths named here.

## Check 1 — Coverage

Result: pass for fixture presence; partial for method-delegation semantics.

Exhibits:

- Charter fixture list: `docs/archive/2026-08-02-milestone-artifacts/prototypes/rule-language/charter-it1.md` F1-F14.
- Artifact corpus: `prototype-rule-language-it1/artifacts/federal-1040-core-2025.package.json`.
- Fixture files: `prototype-rule-language-it1/fixtures/*.fixture.json`.
- F10 paper section: `f10_evolution_probe` in the artifact corpus.

Measured coverage:

- F1: `rule.2025.w2.box1.to.f1040.line1a.v1`.
- F2: `rule.2025.1099int.box1.to.scheduleb.line1.v1`; `rule.2025.scheduleb.line4.to.f1040.line2b.v1`.
- F3a: `rule.2025.scheduleb.required.interest.v1`.
- F3b: `rule.2025.scheduleb.partiii.required.foreign.v1`; fixture `foreign-low-interest.fixture.json`.
- F4: `rule.2025.withholding.w2.line25a.v1`; `rule.2025.withholding.1099.line25b.v1`; `rule.2025.withholding.total.line25d.v1`.
- F5: `rule.2025.standard_deduction.line12e.v1`; parameter `param.2025.f1040.standard_deduction.v1`.
- F6: `rule.2025.taxable_income.line15.v1`.
- F7: `rule.2025.regular_tax.line16.v1`; parameter `param.2025.f1040.regular_tax.v1`; fixtures `happy-path-table.fixture.json` and `high-income-worksheet.fixture.json`.
- F8: `rule.2025.overpayment.line34.v1`; `rule.2025.amount_owed.line37.v1`.
- F9: rounding choice input `tax.choice.rounding_mode.2025` plus `round_money` expressions and `rounding_stage`.
- F10: `f10_evolution_probe`.
- F11: `rule.2025.scheduleb.line3.excludable.v1`; fixture `exclusion-open.fixture.json`.
- F12: `rule.2025.schedule1.line18.early_withdrawal_penalty.v1`; `rule.2025.schedule1.line26.adjustments.v1`; `rule.2025.agi.line10.v1`; `rule.2025.agi.line11a.v1`.
- F13: fixture `rounding-boundary.fixture.json`; evaluator `f13_wrong_stage_value`.
- F14: fixture `no-rounding-convention.fixture.json`.

Finding: F9 is only partially expressed. Artifacts declare which rules require `rounding_mode` and the stage `post_total`, but the evaluator hard-codes the only supported convention value: `whole_dollars_post_total` in `eval_expr` for `round_money`. There is no convention citizen or parameter artifact declaring that method's behavior. This does not invalidate the F13 stage check, but it means method delegation is not fully artifact-declared.

## Check 2 — Reproduction

Result: pass. I reran the evaluator from a detached worktree at `/private/tmp/rule-language-it1-review`.

Command:

```sh
python3 prototype-rule-language-it1/machinery/evaluator.py
```

Exit code: 0.

Measured output:

- `schema_validation`: `ok`.
- Every fixture had `double_run_equal: true`.
- Every fixture had `shuffle_equal: true`.
- F13 reported `correct_post_total: "3"`, `wrong_per_input: "2"`, `diverged: true`.
- Fixture summaries matched the examination: `exclusion_open` blocked with 11 published/10 blocked; `no_rounding_convention` blocked with 4 published/17 blocked; the other four fixtures saturated.

Environment note: each Python invocation emitted `pyenv: cannot rehash: /Users/<local-user>/.pyenv/shims isn't writable` before output. The command still returned 0 and produced valid JSON after that warning.

## Check 3 — Double-Run Equality

Result: pass.

Exhibit: evaluator output from the reproduction command.

All entries in `double_run_equal` were true:

- `fixture.exclusion_open`
- `fixture.foreign_low_interest`
- `fixture.happy_path_table`
- `fixture.high_income_worksheet`
- `fixture.no_rounding_convention`
- `fixture.rounding_boundary`

The evaluator compares canonical JSON for two consecutive `run_fixture` calls per fixture.

## Check 4 — Hard Classes

Result: mixed pass.

Rounding/ordering:

- Artifact-declared part: rules use `round_money` expressions with `"stage": "post_total"` and declare `rounding_stage`.
- Evaluator-carried part: `eval_expr` defines the behavior of `round_money`, including half-up rounding and support only for `whole_dollars_post_total`.
- F13 proves stage correctness for the declared stage by comparing the correct run to a deliberately mutated per-input run.

Tables/brackets:

- Artifact-declared. `rule.2025.regular_tax.line16.v1` uses `if`, `param_path`, `table_row_value`, `let_row`, `table_row`, `field`, `multiply`, and `subtract`.
- The evaluator carries generic expression operations and row lookup mechanics, but not the Form 1040 line 16 worksheet as a named builtin.

Applicability:

- Artifact-declared. `rule.2025.scheduleb.required.interest.v1` and `rule.2025.scheduleb.partiii.required.foreign.v1` are `applicability_rule` artifacts.
- Evaluator behavior for false applicability is generic: if the expression is not true, publish nothing and block nothing.

Bridges:

- Artifact-declared. `rule.2025.scheduleb.line4.to.f1040.line2b.v1` and `rule.2025.agi.line10.v1` are `cross_form_bridge` artifacts with bridge/input roles.

Method delegation:

- Partial. Missing convention blocks are artifact-declared through required choice inputs and block reasons; actual convention semantics are evaluator-carried for the only supported value. This is the main expressiveness finding.

## Check 5 — Blocking

Result: pass for open elective blocking.

Command:

```sh
python3 prototype-rule-language-it1/machinery/evaluator.py --fixture prototype-rule-language-it1/fixtures/no-rounding-convention.fixture.json
```

Measured result: `stop_reason: "blocked"`, `published` count 4, `blocked` count 17.

Direct missing-convention blocks:

- `rule.2025.w2.box1.to.f1040.line1a.v1`
- `rule.2025.scheduleb.line4.to.f1040.line2b.v1`
- `rule.2025.withholding.w2.line25a.v1`
- `rule.2025.withholding.1099.line25b.v1`
- `rule.2025.schedule1.line18.early_withdrawal_penalty.v1`

Each direct block named `reason: "missing_rounding_convention"` and `fact_id: "tax.choice.rounding_mode.2025"`. Dependent downstream rules then blocked on their missing derived inputs, not on operative defaults.

Additional blocking exhibit: `exclusion-open.fixture.json` blocked `rule.2025.scheduleb.line3.excludable.v1` with `reason: "open_savings_bond_exclusion_fact"` and then blocked downstream taxable-interest and AGI/tax rules that depended on the missing line 3/line 2b result.

## Check 6 — Honesty Audit

Result: partial pass.

The examination disclosed several negative results that I also saw:

- F7 table content is fixture-minimal, not a complete 2025 tax table.
- False applicability publishes no finding and no block.
- Supersession restrictions for changing a convention are not modeled.
- Label/id coherence is only partially expressed by one negative schema example.
- Fact types and form-field citizens remain referenced by strings, not full citizens.

Additional issue surfaced by this review: the examination says "whole-dollar rounding: an elected convention" is handled by `round_money` stage declarations and blocking, but it does not clearly disclose that the convention's behavior is hard-coded in evaluator code rather than declared as a convention/parameter artifact. This should be treated as an expressiveness gap for F9, not only an implementation detail.

## Observations

The prototype is useful evidence that expression trees can carry the line 16 worksheet and dependency saturation without form-specific scheduling. The biggest remaining question for the rival design is whether it can make rounding convention semantics and publication/run-record contracts first-class artifacts without making the expression vocabulary illegible.

## Dissent

I do not dissent from proceeding to the rival iteration; the measured prototype is strong enough to compare against. I dissent from treating it1 as ratifiable as-is because F9's method-delegation semantics are not fully artifact-declared, and because this review had process contamination that the foreman should conformance-check explicitly.
