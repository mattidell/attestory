# Examination — Iteration 1 Builder

Builder: Codex resume session, 2026-07-10.

Branch: `prototypes/rule-language/it1`.

Prototype directory: `prototype-rule-language-it1/`.

## What Was Built

Iteration 1 built a primary design using expression-tree rule artifacts rather
than a closed tax-operation enum. The drafted corpus includes schema-versioned
rule artifacts, parameter declarations, an artifact package, derived-publication
act shape, derivation-record shape, synthetic fixtures, and a standalone
evaluator.

Verification command:

```sh
python3 prototype-rule-language-it1/machinery/evaluator.py
```

Result: passed. The run validated schemas, rejected the negative label/output
mismatch example, produced byte-equal double runs, produced equal findings under
shuffled artifact order, and detected F13 stage divergence (`3` post-total
rounding versus `2` per-input rounding).

## Evidence Paths

- Schemas: `prototype-rule-language-it1/schemas/`
- Artifact corpus: `prototype-rule-language-it1/artifacts/federal-1040-core-2025.package.json`
- Fixtures: `prototype-rule-language-it1/fixtures/`
- Evaluator: `prototype-rule-language-it1/machinery/evaluator.py`
- Verification output: rerunnable with the command above.

## Fixture Coverage

- F1: `rule.2025.w2.box1.to.f1040.line1a.v1`
- F2: `rule.2025.1099int.box1.to.scheduleb.line1.v1`, `rule.2025.scheduleb.line4.to.f1040.line2b.v1`
- F3a: `rule.2025.scheduleb.required.interest.v1`
- F3b: `rule.2025.scheduleb.partiii.required.foreign.v1`, fixture `foreign-low-interest`
- F4: `rule.2025.withholding.w2.line25a.v1`, `rule.2025.withholding.1099.line25b.v1`, `rule.2025.withholding.total.line25d.v1`
- F5: `rule.2025.standard_deduction.line12e.v1`, parameter `param.2025.f1040.standard_deduction.v1`
- F6: `rule.2025.taxable_income.line15.v1`
- F7: `rule.2025.regular_tax.line16.v1`, parameter `param.2025.f1040.regular_tax.v1`, fixtures `happy-path-table` and `high-income-worksheet`
- F8: `rule.2025.overpayment.line34.v1`, `rule.2025.amount_owed.line37.v1`
- F9/F13/F14: rounding convention input and `round_money` stage declarations; fixtures `rounding-boundary` and `no-rounding-convention`
- F10: `f10_evolution_probe` in the artifact corpus
- F11: `rule.2025.scheduleb.line3.excludable.v1`, fixture `exclusion-open`
- F12: `rule.2025.schedule1.line18.early_withdrawal_penalty.v1`, `rule.2025.schedule1.line26.adjustments.v1`, `rule.2025.agi.line10.v1`, `rule.2025.agi.line11a.v1`

## Q1 — One Grammar, Zero Special Cases

Positive result with a caveat. One expression grammar covered F1-F9 and F11-F14,
including the line 16 worksheet. F7 is not an evaluator builtin: the artifact
declares a conditional branch, row lookup, row binding, multiplication, and
subtraction. Deleting the line 16 artifact removes only line 16 and downstream
tax/refund behavior.

Negative evidence: row selection and expression evaluation are generic, but the
current sample tax-table rows are fixture-minimal rather than full IRS table
coverage. The language shape survived the fixture; the content corpus is not a
complete 2025 tax table.

## Q2 — Parameters and Effective Scope

Parameters are separate citizens with `parameter_id`, `version`, schema version,
source, and scope. Rules cite them by parameter id. The package declares tax
year, jurisdiction, family, and purpose; every artifact also declares tax year,
jurisdiction, and family. The evaluator does not infer tax meaning from path,
branch, or run arguments.

Negative evidence: the 2026 F10 parameters are paper placeholders for identity
and versioning only, explicitly not adopted law.

## Q3 — Applicability and Blocking

Applicability is represented as rule artifacts producing applicability facts
only when their expression is true. Blocking is schema-shaped in run records:
each block names artifact id, reason, input, and missing fact id or type. The
`no-rounding-convention` fixture blocks all rules that require the rounding
choice with `missing_rounding_convention`; the `exclusion-open` fixture blocks
Schedule B line 3 with `open_savings_bond_exclusion_fact`.

Negative evidence: blocks are per missing input. The design has not yet modeled
compound legal explanations for why a condition was false; false applicability
currently publishes no finding and no block.

## Q4 — F7 Expression Form

F7 forced expression trees. A fixed operation enum either grows into tax-specific
operations or hides worksheet meaning in code. The expression form used here is
more verbose but keeps the worksheet formula in artifacts:
`if`, `table_row`, `let_row`, `field`, `multiply`, and `subtract`.

Negative evidence: legibility cost is real. A fresh reader can recover the
worksheet, but only by reading nested expression nodes. A later design should
test whether a constrained worksheet DSL improves readability without becoming
sealed executor behavior.

## Q5 — Order Stability and Stage Correctness

Passed. The evaluator reports double-run equality and shuffled-artifact equality
for all six fixtures. F13 distinguishes stable-but-wrong placement: correct
post-total rounding of two `$1.49` wages publishes `3`; deliberate per-input
rounding gives `2`.

## Q6 — Elective Dependence

Filing status and rounding mode are explicit choice inputs. If filing status is
missing, standard deduction and line 16 block. If rounding mode is missing, every
money rule that declares `round_money` blocks before publishing.

Negative evidence: this prototype does not encode supersession restrictions for
changing a convention. It only proves derivation dependence on the asserted
choice.

## Q7 — Fresh-Reader Recovery Across Artifact Kinds

The corpus includes all represented artifact kinds: field mappings,
cross-form bridges, applicability rules, derivation rules, parameter
declarations, package envelope, publication act, and derivation record. Labels,
output fact ids, artifact kind, source, declared dependencies, and scope are
visible in the artifacts.

Negative evidence: schema-level label/id coherence is only partially expressed.
The negative example proves the schema can reject one known misleading label for
Form 1040 line 2b, but it is not a general ontology of form-line labels. A
production design would need declared form-field citizens or generated
constraints to make this complete.

## Q8 — Pins

Pins need roles. Published findings include finding ids, artifact ids, parameter
ids, and `pin_roles` copied from inputs. The roles make explanation walking
clearer than bare id lists because the record can distinguish input, choice,
parameter, bridge, and condition dependencies.

## Q9 — Publication Act and Run Record Timing

The prototype keeps `derived_publication` distinct from assertion. Each published
finding includes a derived-publication act shape that pins input findings,
artifacts, parameters, workspace revision, adoption act, actor id, and a
run-start record id. The derivation record is a completion record listing
published findings and blocks.

Negative evidence: this supports the it0 concern that a final-only run record is
not enough. The design implies a start/completion pair: publication acts can
refer to a start record even if interruption prevents completion. This evaluates
record timing and publication vocabulary only; it does not resolve reserved T1
derived-finding authority beyond the existing instrument framing.

## Q10 — Deterministic IDs

Passed in fixture mode. Derived finding ids, derived-publication act ids, and
completion record ids are deterministic hashes of revision, rule/output, pins,
parameters, and published/blocked sets. Double-run equality passed for all
fixtures.

## Q11 — Citizens and Schemas

Draft schema-level shapes exist for every proposed kind:

- `rule-artifact.v1.prototype-it1`
- `parameter-declaration.v1.prototype-it1`
- `artifact-package.v1.prototype-it1`
- `derived-publication-act.v1.prototype-it1`
- `derivation-record.v1.prototype-it1`

Every drafted artifact and parameter names its schema version. The negative
validation example `negative-label-id-mismatch.example.json` fails as expected.

Negative evidence: fact types and form-field citizens are referenced by id
strings, not drafted as full schemas in this iteration. That was enough to test
the rule language, but a ratified ADR should require form-field/fact-type schema
families before production adoption.

## Builder Conclusion

This primary design is expressive enough for the charter fixtures, and the
evaluator checks did not require form-specific scheduler behavior. The main
tradeoff is legibility: expression trees avoid sealed operations but become
harder to read around worksheet logic and branch outputs. The strongest next
comparison point for the rival design is whether it can improve fresh-reader
recovery while preserving the same purity, blocking, and no-orchestrated-
traversal guarantees.
