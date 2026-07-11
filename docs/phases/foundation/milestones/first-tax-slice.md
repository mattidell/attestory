# Milestone: First Tax Slice

Audience: Agents (Objective and Scope are Shared)

Status: **planned; evidence gate pending**. This plan converts the planning
inputs in `first-tax-slice-inputs.md` into an executable milestone, but the
implementation branch must not start until Track 0's citizen-family decision is
complete and this plan is amended, if needed, with the ratified contract.

## Objective

The finished machinery computes a thin, real federal tax slice as content:
synthetic W-2 and 1099-INT facts flow through declared, adopted rule artifacts
into Form 1040 core values with golden outcomes, explanation chains, source-set
closure gaps, and a supersession cascade acceptance. The milestone proves the
Foundation phase thesis at tax-content scale: the engine stays thin, tax meaning
is data, and every value answers through findings, rules, parameters, adoption,
records, and governance pins.

## Current State

- Governance v0.1 is the contract authority.
- Workspace Kernel is complete: append-only act log, fact types, facts,
  findings, adoption, evidence, supersession, read models, and inspection.
- Rule Language Design is ratified by ADR-0006/0007/0008, with ADR-0005's
  prototype-evidence rule in force for consequential contract decisions.
- Derivation Machinery is complete: schema-backed rule artifacts, closed
  packages, operation-semantics canon, adoption gate, saturation runner,
  reference runner parity, records, explanation, and CLI.
- Derivation Cascade Reconciliation is complete under ADR-0010:
  derived-publication acts enter the act log and derived findings displace when
  pinned inputs are superseded.
- The carried obligation is unresolved: form-field and tax fact-type citizen
  families were intentionally deferred from Derivation Machinery §5.6 because
  the prototypes referenced them as bare ids.

## Scope

- A narrow federal individual-income-tax content corpus for one tax year,
  covering W-2 wages and 1099-INT taxable interest into Form 1040 core lines.
- Declared source-set closure facts for W-2 and 1099-INT source families, so an
  empty or missing source set is distinguishable from a closure-backed zero.
- Form-field and tax fact-type citizen contracts sufficient for this slice,
  with committed positive examples for any new schema family.
- Rule artifacts and parameters authored as real tax content, citing official
  source material verified at implementation time from primary sources.
- Synthetic workspaces and golden outcomes for: normal W-2 + 1099-INT,
  interest-only, wages-only, closure-backed zero interest, unclosed source-set
  gap, present-but-invalid source value, and supersession cascade.
- Rendering-content metadata for absence on included Form 1040 lines,
  distinguishing computed zero, closure-backed zero, and guard/non-existence.
- Coverage read model or report surface over current facts and derivation
  records that exposes open source-set closure assertions as first-class gaps.

## Non-Goals

- No UI or filing workflow.
- No personal data, uploaded real documents, or fixtures derived from personal
  records.
- No extraction, proposals, consultation grants, or nondeterministic model
  flows.
- No broad federal coverage beyond the proving slice; Schedule B behavior,
  withholding/payment lines, credits, itemized deductions, state taxes, and
  filing transmission are out of scope unless a narrow bridge is required to
  keep the included 1040 lines honest.
- No resolution of reserved stance/position doctrine or the fuller
  derived-finding authority construction.
- No new derivation machinery unless the content exposes a defect in the
  already-ratified machinery; such a defect becomes a separate decision or patch,
  not hidden content work.

## Contracts

- Existing kernel contracts: fact-type bundles, facts, assertion acts, evidence
  acts, act envelopes, currency, and read models.
- Existing derivation contracts: rule artifacts, parameters, artifact packages,
  operation-semantics canon, derived-publication acts, derivation records, and
  explanation pins.
- New or settled content contracts expected here:
  - `form-field` citizen family, if the evidence gate finds that form line
    identity, rendering absence, or form-source citations need first-class
    lifecycle beyond rule symbols.
  - Tax fact-type bundle content for W-2, 1099-INT, Form 1040 core facts,
    rounding convention, filing status, source-set closure assertions, and any
    source/document identities needed for fact individuation.
  - Rendering-absence metadata, either as form-field content or a separate
    declared family if Track 0 proves the concepts are not the same thing.
  - A coverage/gap report shape, derived from workspace state and records, not
    stored as authoritative form state.
- Payload Instantiation Gate: any track that adds a schema must commit a
  hand-written positive example alongside it before runner code consumes it.

## Evidence And Decision Gate

Track 0 is a gate, not tax implementation. The form-field/fact-type contract is
contract-foundational Tier 2 unless the gate argues a narrower Tier 1 exception.
Under ADR-0005, a Tier 2 contract-foundational decision needs prototype
evaluation evidence before an ADR is proposed.

The gate must answer:

- Whether existing `fact-type.v1` is sufficient for real tax fact types, or
  whether it needs a new version or companion citizens.
- Whether form fields are merely rule output symbols, first-class citizens, or
  generated content with lineage.
- Where rendered-absence semantics live, and how they avoid conflating computed
  zero, closure-backed zero, and guard-based non-existence.
- How source-set closure assertions are fact types: identity keys,
  supersession, basis, and rule pins.
- Which authoritative source citations live in rule artifacts, parameters,
  form-field citizens, or package metadata.

If the answer requires a Tier 2 ADR, the gate produces a prototype evaluation
analysis, ADR draft, accepted ADR, and any plan amendment before Track 1 starts.
If the answer is genuinely Tier 1, the gate records the exception rationale in
this plan or the retrospective before Track 1 starts.

## Fixtures

All committed fixtures are synthetic and publishable. Fixture taxpayers,
employers, payers, forms, and values use demo ids and manufactured values.

Planned scenarios:

- `w2_and_interest`: one W-2 and one 1099-INT produce wages, taxable interest,
  total income, adjusted gross income for the narrow no-adjustment case, taxable
  income, and tax.
- `wages_only_closed_interest`: W-2 wages plus an asserted complete 1099-INT
  source set with no interest sources publishes a closure-backed zero interest
  value.
- `interest_only_closed_w2`: 1099-INT interest plus an asserted complete W-2
  source set with no wage sources publishes a closure-backed zero wage value.
- `unclosed_interest`: missing 1099-INT closure blocks the interest-dependent
  total rather than publishing a zero.
- `invalid_source_value`: a present source finding outside the declared value
  domain blocks with a schema'd invalid-value code and no exception text.
- `supersession_cascade`: correcting a source finding displaces dependent 1040
  values through ADR-0010's derivation-currency layer; re-derivation may publish
  successors, but displacement itself is the required acceptance.
- `rendered_absence`: included form fields show distinct rendering instructions
  for computed zero, closure-backed zero, and guard/non-existence.

## Verification

- `python3 -m unittest`
- `python3 tools/governance_lint.py`
- `python3 -m mypy`
- Derivation CLI golden for the First Tax Slice scenario set.
- Reference-runner parity on every First Tax Slice scenario.
- Package validation proves all real-content rule/parameter/form artifacts are
  closed under exact versions and scope.
- Explanation-walk tests for every published Form 1040 value.
- Coverage/gap tests showing open W-2 and 1099-INT closure assertions as gaps.
- Supersession cascade golden proving source correction displaces dependent
  derived findings.
- Data-safety fixture scan for private markers, real personal names, real
  account identifiers, and absolute local paths.

## Data Safety

Tax law content and public form structure may be committed; taxpayer data may
not. Fixture values are manufactured and must not be copied from personal
records. Personal experiments remain under ignored paths such as `local-data/`,
`temp/`, `private-archive/`, `uploads/`, and `generated/user/`.

Official tax sources must be checked from primary sources at implementation
time. Do not rely on memory for current tax-year values, form instructions, or
thresholds.

## Exit Criteria

- Track 0 decision gate complete, with ADR evidence or an explicit Tier 1
  exception.
- Any new schema family has a committed positive example and negative schema
  tests before code consumes it.
- Adopted rule package covers the declared W-2 and 1099-INT to Form 1040 slice
  entirely as artifacts and parameters.
- All planned scenarios have committed synthetic fixtures and golden reports.
- Coverage reports identify unclosed source sets as gaps; derivation never
  silently treats missing source facts as zero.
- Explanation chains for every published 1040 value terminate at acts,
  findings, artifacts, records, and governance pins, never code.
- Full verification is green.
- Milestone retrospective written after non-fast-forward merge to `main`.

## Tracks

### Track 0 — Citizen-family evidence gate

Goal: settle the form-field, tax fact-type, source-set closure, and
rendered-absence content contracts before implementation depends on them.
Boundary: no production schemas or rule corpus are consumed by runner code in
this track.
Inputs: `first-tax-slice-inputs.md`, ADR-0005/0006/0009/0010, prototype
evidence §5.6, official-source examples selected for this slice.
Outputs: prototype charter/evaluation artifacts if Tier 2, ADR if required,
positive example sketches, and a plan amendment with the selected contract.
Verification: process conformance for any prototype; `python3
tools/governance_lint.py`; plan diff reviewed against ADR outcome.
Migration risk: high if skipped; low after ADR because implementation consumes
only ratified shapes.
Data safety: documents and synthetic examples only.

### Track 1 — Tax vocabulary and schema/content foundation

Goal: publish the selected citizen families and tax fact-type bundle content for
the slice.
Boundary: no derivation rules yet; no fixture workspaces beyond positive
examples needed for schema instantiation.
Inputs: Track 0 decision; kernel schema registry.
Outputs: schemas if required, positive examples, tax fact-type bundle(s), form
field or rendering content, schema tests, published manifests.
Verification: focused schema tests; registry immutability checks; full suite.
Migration risk: durable content contract begins here.
Data safety: synthetic examples only.

### Track 2 — Source-set closure and synthetic workspaces

Goal: instantiate W-2 and 1099-INT source facts plus closure assertions in
synthetic workspaces.
Boundary: no Form 1040 derived outputs yet.
Inputs: Track 1 fact types; kernel act log and assertion APIs.
Outputs: synthetic act logs or scenario inputs for the planned source-set
fixtures; coverage/gap tests for open and closed source families.
Verification: workspace inspection/read-model tests; data-safety fixture scan.
Migration risk: fact identity keys and closure fact shape become fixture
contracts.
Data safety: manufactured payers, employers, and amounts only.

### Track 3 — Rule artifacts and parameters for the tax slice

Goal: author the real-content rule package for W-2 wages, 1099-INT taxable
interest, total income, the narrow no-adjustment AGI path, standard deduction,
taxable income, and tax for the fixture ranges.
Boundary: no broad tax coverage; rules block outside declared source and
parameter coverage.
Inputs: Tracks 1-2; official IRS sources checked at implementation time;
operation-semantics canon.
Outputs: rule artifacts, parameters, artifact package, source citations, package
validation tests, reference-runner parity.
Verification: package closure and scope tests; derivation runner unit tests;
reference-runner byte equality.
Migration risk: tax content identities and version scopes become durable.
Data safety: public tax law content plus synthetic fixture values only.

### Track 4 — Golden scenarios, explanation, and rendered absence

Goal: make the slice inspectable: committed scenario goldens, explanation
goldens, rendered-absence metadata, and gap reports.
Boundary: no UI renderer; command/test output only.
Inputs: Track 3 rule package and scenario outputs.
Outputs: golden reports for all scenarios; CLI fixtures; tests distinguishing
computed zero, closure-backed zero, and guard/non-existence.
Verification: derivation CLI subprocess tests; explanation-walk tests; coverage
gap tests; full suite.
Migration risk: golden outcomes change only when content contracts change.
Data safety: fixture scan.

### Track 5 — Supersession cascade acceptance and documentation

Goal: prove the source-correction cascade over real slice content and document
how to run the milestone.
Boundary: no auto-re-derivation orchestration beyond explicit runner execution.
Inputs: Track 4 scenarios; ADR-0010 projection/currency layer.
Outputs: supersession cascade golden; README/phase documentation updates;
milestone completion status.
Verification: full suite, governance lint, mypy, derivation CLI, cascade golden.
Migration risk: none beyond accepted ADR-0010 behavior.
Data safety: synthetic only.
