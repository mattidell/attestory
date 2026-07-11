# Charter - Iteration 1

Version 3 (2026-07-11). Status: approved for iteration 1; round 0 review and
delta-confirmation complete; builder seat open.

Revision history: v1 reviewed in round 0 (`reviews/round-0-governance.md`,
`reviews/round-0-adversary.md`). v2 incorporates the governance evidence
conditions and the adversary fixture attacks: evidence peerage mutation,
strict positive/negative validation results, 1099-INT box distinctions,
identity-collision pressure, absence/invalidity matrix, resolved-citation
mutation, cross-year versioning negative, and coverage rebuild/stale-projection
check. v3 incorporates the adversary delta's remaining A3 evidence-shape
condition: every absence/invalidity matrix state needs explanation-walk
evidence.

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
primary sources checked at build time. The main positive slice is tax year 2025;
the evolution probe uses a later-year source/form change only to test versioning
boundaries.

- **F1 - W-2 source facts and peerage mutation.** A synthetic taxpayer has two
  W-2 source instances with wages that aggregate to Form 1040 line 1a. At least
  one fixture must pressure identity by using same employee, same employer, and
  same tax year with distinct source instances or a corrected/reissued source.
  The design must declare fact identity without making facts document-children,
  then demonstrate that replacing or removing evidence changes only evidentiary
  standing, not fact identity or finding content.
- **F2 - 1099-INT source facts and box distinctions.** A synthetic taxpayer has
  one 1099-INT box 1 taxable-interest source instance that reaches Form 1040
  line 2b. A paired negative or blocked fixture must exercise a non-box-1
  federal meaning inside the 1099-INT family, such as early-withdrawal penalty,
  U.S. Savings Bond/Treasury interest, tax-exempt interest, or nominee
  allocation. The design must distinguish source-box meaning from form-line
  meaning instead of relying on "taxable interest" as an unstated filter.
- **F3 - Empty closed W-2 set.** A taxpayer with no W-2 sources asserts "all my
  W-2s are represented." A closure-backed zero wage value is publishable and
  pins the closure assertion.
- **F4 - Empty closed 1099-INT set.** A taxpayer with no 1099-INT sources
  asserts "I have no other interest income." A closure-backed zero interest
  value is publishable and pins the closure assertion.
- **F5 - Absence and invalidity matrix.** For at least one included source set,
  show four states: a present source finding whose value is zero, an empty source
  set with a closure assertion, no source and no closure assertion, and a
  present but schema-invalid source value. The dependent rules must publish only
  where the state honestly supports publication; unclosed and invalid states
  must block with distinct declared reasons and no exception text. The
  examination must include explanation-walk evidence for each state: what act,
  finding, closure assertion, block record, or validation result explains the
  state.
- **F6 - Form 1040 core fields.** Lines 1a, 2b, 9, 11, 12, 15, and 16 are
  represented with enough declared meaning for rules, rendering, source
  citations, and explanation to reference them without relying on bare strings.
- **F7 - Rendered absence and false guard.** The same included line family must
  distinguish a computed zero, a closure-backed zero, a blocked unclosed source,
  a blocked invalid source, and guard/non-existence. The false-guard case must
  name the artifact guard and its inapplicable disposition; no finding may be
  published for blocked or false-guard non-existence. Each rendered-absence
  state must have an explanation path that terminates at declared content and
  records, never at renderer convention.
- **F8 - Source citation placement and mutation.** W-2, 1099-INT, Form 1040
  line, standard deduction, taxable income, and tax-table facts/rules each cite
  their official source without making citations hidden runner inputs. At least
  one citation instance must be fully resolved with document identity, tax-year
  applicability, and precise locator. A negative mutation must remove or alter
  the locator or tax year, and a parity check must show citation text cannot
  change evaluation output.
- **F9 - Evolution and mixed-year probe.** One tax-year parameter change and one
  structural form/source-box change are exercised with an old-year positive, a
  later-year positive, a mixed-year negative, and an immutability check that old
  schemas/artifacts are not edited. The examination must state which ids
  persist, which versions change, which new citizens appear, and whether
  generation or migration is implicated.
- **F10 - Supersession cascade.** Correcting one W-2 wage source finding
  displaces line 1a and downstream Form 1040 values through derivation edges;
  the design must make the edge and explanation paths recoverable.
- **F11 - Coverage/gap report and stale-projection probe.** Current-state
  coverage can say which W-2 and 1099-INT source-set closure assertions remain
  open, without storing coverage as authoritative form state. The prototype must
  delete and rebuild any coverage projection from the act log/read models and
  derivation records, compare bytes, then inject or sketch a stale "closed"
  projection while the source-set closure act remains open; the stale projection
  must be ignored or rejected.
- **F12 - Positive and negative schema examples.** Every new or amended citizen
  family has at least one hand-written positive instance and one negative
  instance that catches a meaningful contract error. The prototype must run a
  strict validator or equivalent checker: positives validate, negatives fail for
  the declared reason, and no consumer repairs or coerces malformed shape. At
  least one negative must cover an undeclared shape or wrong schema version.

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
  What locator precision, tax-year binding, and non-operative parity checks are
  required?
- **Q6.** Does the design preserve Article 1 peerage: no fact identity is a
  child of, or foreign-keyed to, a source document? Does the evidence
  replacement/removal mutation leave fact identity and finding content stable?
- **Q7.** Does the design preserve Article 9/10 canon/declaration: every
  load-bearing noun has a schema before instances exist, and consumers reject
  undeclared shape? Do positive and negative examples actually validate/fail
  under the declared runtime authority?
- **Q8.** Does the design preserve Article 11 legibility: tax meaning,
  applicability, field mappings, rendering absence, and source bridges are
  declared content, not code?
- **Q9.** Does the design preserve Article 14: gap/coverage observations belong
  to records or derived reports and are recomputable, never stored as a second
  copy of form state? Does the stale-projection probe fail safely?
- **Q10.** Is the decision Tier 2 with ADR evidence, or can it be honestly
  narrowed to Tier 1? State the rationale either way.

## Out Of Scope

Broad tax coverage, extraction/proposal workflows, UI rendering, filing,
Schedule B details beyond the interest bridge if needed for line 2b honesty,
withholding/payment lines, credits, itemized deductions, state taxes, redaction,
multi-party authority, and reserved stance/position doctrine.

## Evidence Expected

Draft schemas or amendments; positive and negative examples with validation
results; a minimal synthetic scenario for F1-F8 and F10-F11; mutation results
for evidence replacement/removal, citation locator/year, mixed-year package
membership, and stale coverage projection; explanation-walk evidence for every
absence/invalidity/rendered-absence state in F5 and F7; a short examination note
answering Q1-Q10 with paths to exhibits; explicit negative results. If the
design cannot make one of the distinctions without lying or building on a
reserved entry, that failure is evidence.
