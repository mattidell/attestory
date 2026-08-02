# Charter - Iteration 3 Targeted Repair

Version 1 (2026-07-11). Status: approved for owner-launched builder.

Iteration 3 is not a clean-room rival and not a full replacement prototype. It
is a targeted repair-and-decision pass based on the it2 exhibit
`exhibits/tax-citizen-families/it2` at `989d9fe`, with clean-room mini-spikes
only for disputed design boundaries where patching it2 would entrench an
unproven assumption.

## What Iteration 3 Builds

The builder works on branch `prototypes/tax-citizen-families/it3`.

The final candidate artifacts for this iteration must live under
`docs/archive/2026-08-02-milestone-artifacts/prototypes/tax-citizen-families/it3/` on that branch. The builder may copy
the it2 artifact tree as a starting point, but the examination must distinguish
reused it2 design, patched it2 design, and any clean-room mini-spike result.

The builder writes `docs/archive/2026-08-02-milestone-artifacts/prototypes/tax-citizen-families/examination-it3.md` on
the it3 branch. The examination must report every required gate below as one of:
closed with artifact evidence, explicitly failed with evidence, or deferred
because it would require a governance or owner decision.

## Non-Repetition Rule

Iteration 3 must not answer by rerunning the it2 harness or by producing another
general-purpose plausible contract. For each gate, the builder must add a
committed fixture, artifact, negative example, validation check, explanation
walk, or mini-spike note that directly addresses the named round-2 gap.

If an it2 result is reused, the examination must name the it2 evidence and state
what new it3 artifact or check makes the conclusion stronger than it2.

## Required Repair Gates

- **R1 - Two-source W-2 identity pressure.** Add a fixture with two distinct W-2
  source instances for the same employee, employer, and tax year, or a
  corrected/reissued-source fixture that pressures the same collision. The
  design must show how fact identity remains peer to source documents while
  separate source-instance questions or corrections stay distinguishable.
- **R2 - Closure semantics decision.** Decide whether source-set completeness is
  modeled as reuse of `fact-type.v1`, a new source-set-completeness citizen
  family, or an explicit machinery projection contract. The decision must state
  nature, identity keys, basis or attestation, lifecycle/supersession, and pins.
  If the builder keeps it2's elective-fact reuse, it must answer the round-2
  semantic dissent directly.
- **R3 - Closure load-bearing check.** Demonstrate whether empty-source
  publication depends on an authoritative closure finding or on a runner
  projection such as `closed_sets`. If machinery remains load-bearing, declare
  the machinery contract rather than treating it as a projection.
- **R4 - Coverage from records.** Replace or supplement the it2 fixture-boolean
  coverage helper with coverage rebuilt from authoritative records, read models,
  and derivation records. The stale-projection probe must show that contradictory
  stored coverage cannot override current records.
- **R5 - Citation attachment model.** Attach or otherwise bind official source
  citations for W-2, 1099-INT, standard deduction, taxable income, tax method,
  and Form 1040 fields to the citizens they support. Validation must reject a
  valid citation id attached to the wrong form line, tax year, or content role.
- **R6 - Cross-citizen package and year checks.** Mixed-year negatives must cover
  the package boundary across form fields, citations, facts or fact types, rules,
  and parameters, not only one parameter-member case. Include old-year and
  later-year positives where the slice makes the later-year citizen meaningful.
- **R7 - Form 1040 line 1z boundary.** Either model line 1z honestly in the
  included slice or declare a boundary that prevents line 9 from pretending that
  omitted line 1 siblings are included. The examination must explain why the
  resulting line 9 contract is honest.
- **R8 - Standard deduction eligibility boundary.** Declare the line 12 standard
  deduction eligibility inputs or guard boundary. The ordinary base-table path
  must not silently publish for taxpayers whose dependency, age, blindness,
  spouse-itemizing, dual-status, or related conditions are unknown if those
  conditions are in scope for the included line.
- **R9 - Line 16 method boundary.** Declare when the rate-schedule method is
  eligible versus when the Tax Table or alternate worksheets are required. If the
  prototype keeps only a narrow ordinary path, add fixtures or guards that block
  or exclude omitted methods honestly.
- **R10 - All-elective-open saturation.** Add a fixture or probe in which filing
  status, rounding, itemize choice, and closure choices are open. Dependent
  rules must block without defaults becoming operative.
- **R11 - Complete absence and rendered-absence explanations.** Provide
  explanation walks for present numeric zero, closure-backed zero, no source and
  no closure, invalid source value, and false guard/inapplicability. Each walk
  must terminate at declared content and records, not renderer convention.
- **R12 - Scenario and package provenance.** Give scenarios a declared
  attachment to the package, bundle/content scope, tax year, and jurisdiction so
  a fresh reader can follow scenario -> package -> facts -> rules -> citations
  -> form fields without importing machinery knowledge.
- **R13 - Committed positive and negative examples.** Every new or materially
  changed citizen family or relationship has hand-written positive and negative
  examples. Harness-local mutations may supplement but not replace committed
  examples.

## Clean-Room Mini-Spikes

Mini-spikes are allowed only for design boundaries that may need an alternative
to the it2 shape:

- closure semantics;
- citation attachment across citizens;
- line 1z, line 12, or line 16 boundary strategy;
- source-instance identity and correction semantics.

A mini-spike must be small, live under the it3 artifact tree, and end with one
of: adopt into the repaired design, reject with reason, or escalate to owner
decision. It must not become a third broad prototype.

## Evidence Expected

Expected evidence includes patched schemas or schema amendments, committed
positive and negative examples, synthetic fixtures, mutation results, harness or
validator output, coverage rebuild output, explanation walks, and explicit
negative results.

The examination must include a checklist mapping R1-R13 to file paths and
commands. A passing harness is not sufficient unless the checklist ties the
passes to the named gates.
