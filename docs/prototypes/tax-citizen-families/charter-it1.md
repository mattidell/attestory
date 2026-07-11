# Charter - Iteration 1

Version 1 (2026-07-11). Status: draft under round 0 review; builder seat not
open.

## What Iteration 1 Builds

One candidate content-contract design for the First Tax Slice's tax citizen
families. The prototype drafts concrete schemas or schema amendments, positive
instances, negative instances, and minimal projection examples for form fields,
tax fact types, source-set closure assertions, rendered absence, and source
citations. It may include throwaway validators or readers only to prove the
contracts are machine-checkable; prototype code lives only on
`prototypes/tax-citizen-families/it1`.

The rival design, if the process proceeds, answers this same charter in a clean
room.

## Fixture Set

All fixture values are synthetic. Legal/form source material comes from official
primary sources checked at build time.

- **F1 - W-2 source facts.** A synthetic taxpayer has two W-2 source instances
  with wages that aggregate to Form 1040 line 1a. The design must declare fact
  identity without making facts document-children.
- **F2 - 1099-INT source facts.** A synthetic taxpayer has one 1099-INT source
  instance with taxable interest that reaches Form 1040 line 2b. The design must
  distinguish source box meaning from form-line meaning.
- **F3 - Empty closed W-2 set.** A taxpayer with no W-2 sources asserts "all my
  W-2s are represented." A closure-backed zero wage value is publishable and
  pins the closure assertion.
- **F4 - Empty closed 1099-INT set.** A taxpayer with no 1099-INT sources
  asserts "I have no other interest income." A closure-backed zero interest
  value is publishable and pins the closure assertion.
- **F5 - Unclosed source set.** A taxpayer has no 1099-INT source facts and no
  1099-INT closure assertion. The dependent interest rule must block; no zero
  may be published.
- **F6 - Form 1040 core fields.** Lines 1a, 2b, 9, 11, 12, 15, and 16 are
  represented with enough declared meaning for rules, rendering, source
  citations, and explanation to reference them without relying on bare strings.
- **F7 - Rendered absence.** The same included line family must distinguish a
  computed zero, a closure-backed zero, and guard/non-existence. The design must
  place that rendering meaning somewhere declared.
- **F8 - Source citation placement.** W-2, 1099-INT, Form 1040 line, standard
  deduction, taxable income, and tax-table facts/rules each cite their official
  source without making citations hidden runner inputs.
- **F9 - Evolution probe.** One tax-year parameter change and one structural
  form/source-box change are sketched: which ids persist, which versions change,
  which new citizens appear, and whether generation or migration is implicated.
- **F10 - Supersession cascade.** Correcting one W-2 wage source finding
  displaces line 1a and downstream Form 1040 values through derivation edges;
  the design must make the edge and explanation paths recoverable.
- **F11 - Coverage/gap report.** Current-state coverage can say which W-2 and
  1099-INT source-set closure assertions remain open, without storing coverage
  as authoritative form state.
- **F12 - Positive and negative schema examples.** Every new or amended citizen
  family has at least one hand-written positive instance and one negative
  instance that catches a meaningful contract error.

## Questions Iteration 1 Must Answer

- **Q1.** Is existing `fact-type.v1` sufficient for real tax fact types in this
  slice, or does the content force a new version or companion family?
- **Q2.** Are form fields first-class citizens, rule-output symbols with richer
  package metadata, generated citizens, or something else? What lifecycle and
  versioning do they need?
- **Q3.** Where does rendered-absence meaning live, and can a fresh reader
  recover the difference between computed zero, closure-backed zero, and
  guard/non-existence from artifacts alone?
- **Q4.** How are source-set closure assertions modeled as facts: nature,
  identity keys, basis, supersession rules, and pins?
- **Q5.** How are official source citations represented so that they support
  adoption and explanation without becoming runner behavior or personal data?
- **Q6.** Does the design preserve Article 1 peerage: no fact identity is a
  child of, or foreign-keyed to, a source document?
- **Q7.** Does the design preserve Article 9/10 canon/declaration: every
  load-bearing noun has a schema before instances exist, and consumers reject
  undeclared shape?
- **Q8.** Does the design preserve Article 11 legibility: tax meaning,
  applicability, field mappings, rendering absence, and source bridges are
  declared content, not code?
- **Q9.** Does the design preserve Article 14: gap/coverage observations belong
  to records or derived reports and are recomputable, never stored as a second
  copy of form state?
- **Q10.** Is the decision Tier 2 with ADR evidence, or can it be honestly
  narrowed to Tier 1? State the rationale either way.

## Out Of Scope

Broad tax coverage, extraction/proposal workflows, UI rendering, filing,
Schedule B details beyond the interest bridge if needed for line 2b honesty,
withholding/payment lines, credits, itemized deductions, state taxes, redaction,
multi-party authority, and reserved stance/position doctrine.

## Evidence Expected

Draft schemas or amendments; positive and negative examples; a minimal synthetic
scenario for F1-F7 and F10-F11; a short examination note answering Q1-Q10 with
paths to exhibits; explicit negative results. If the design cannot make one of
the distinctions without lying or building on a reserved entry, that failure is
evidence.

