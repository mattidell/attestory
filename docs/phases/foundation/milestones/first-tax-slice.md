# Milestone: First Tax Slice

Audience: Agents (Objective and Scope are Shared)

Status: **in execution on `milestone/first-tax-slice`**. Track 0's
prototype process concluded with accepted Tier 2 ADR-0011 and ADR-0012. This
2026-07-11 scope amendment replaces the original W-2 + 1099-INT/core-return
implementation scope with a W-2 -> Form 1040 line 1a vertical slice. The
broader planning input remains preserved in `first-tax-slice-inputs.md`.

## Objective

Prove the Foundation thesis at the smallest real tax-content scale: synthetic
W-2 box-1 findings flow through an adopted rule artifact into a first-class 2025
Form 1040 line-1a field, with trustworthy identity, explanation for published
values, correction/displacement, explicit re-derivation, and two-runner parity.

This milestone implements the contracts actually ratified after Track 0. It is
not a complete return, readiness calculation, or source-completeness workflow.

## Planning Amendment Rationale

The original milestone combined W-2 and 1099-INT source identity, closure-backed
zeros, core Form 1040 lines, standard deduction, line-16 method selection,
coverage, citation resolution, and all-state explanations. Prototype review
showed that several of those depend on unresolved authority or machinery
contracts. See:

- `docs/prototypes/tax-citizen-families/evaluation-analysis.md`;
- `docs/prototypes/tax-citizen-families/process-retrospective.md`;
- ADR-0011 (tax fact identity and closure); and
- ADR-0012 (form-field citizens and rendered dispositions).

The scope is narrowed so production work can begin without turning unresolved
prototype exclusions into code authority.

## Current State

- Governance v0.1 is the contract authority.
- Workspace Kernel, Rule Language, Derivation Machinery, and ADR-0010 composed
  currency are complete.
- Derived-publication acts enter the act log; source correction can displace a
  dependent derived chain.
- ADR-0011 ratifies kernel `fact-type.v1` reuse, W-2-slip peer identity,
  mechanical correction, and determinable/attested closure with
  affirmative-only closure authority.
- ADR-0012 ratifies first-class form-field citizens and five rendered
  dispositions.
- Prototype code remains evidence only under exhibit tags; nothing from it is
  merged or adopted as production implementation.

## Scope

- Tax year 2025, US federal individual income tax.
- W-2-slip entity content peer to evidence.
- W-2 box-1 wage fact type using kernel `fact-type.v1`, keyed by employer,
  tax year, and W-2-slip citizen within the workspace/taxpayer scope.
- W-2 source-set closure fact type implementing ADR-0011 nature, basis, and
  affirmative-only authority as schema/content examples only.
- Production `form-field.v1` schema and a Form 1040 line-1a citizen implementing
  ADR-0012.
- One real rule artifact aggregating current W-2 box-1 findings into the line-1a
  output symbol.
- One adopted artifact package containing the bounded line-1a rule and only the
  existing machinery members it requires.
- Synthetic scenarios for one W-2, two same-employer slips, a present numeric
  zero, correction/displacement, and explicit re-derivation.
- Explanation walks for published nonzero and computed-zero line-1a findings.
- Form-field content for all five ADR-0012 dispositions, while runtime
  acceptance in this milestone is limited to states the included line-1a path
  actually produces.
- Official IRS source references checked at implementation time. Form-field
  content may carry an opaque citation reference; semantic citation resolution
  is deferred.

## Non-Goals And Deferred Boundaries

- No 1099-INT or other interest content.
- No Form 1040 line 1z, line 9, line 11, line 12, line 15, or line 16.
- No closure-backed empty-source zero and no operational source-family mapping.
- No caller-supplied `closed_sets` contract or replacement.
- No coverage/readiness report.
- No standard-deduction eligibility or tax-method condition model.
- No complete adopted manifest spanning form fields, citations, bindings, and
  resolver citizens; the package uses the existing ADR-0006 rule/parameter
  boundary only.
- No citation resolver or citation semantic-attachment contract.
- No explanation API for blocked, invalid, or guard-inapplicable fields.
- No W-2c documentary workflow; the milestone proves same-fact mechanical
  correction with synthetic evidence only.
- No UI, filing workflow, personal data, extraction, proposals, persistence
  beyond existing workspace/record contracts, or reserved ontology work.

These are not accidental omissions. They are the explicit exclusions in the
narrow evaluation analysis and become separately planned work only after their
own economic/decision gates.

## Contracts

### Existing

- Kernel: schema registry, bundle adoption, entities, facts, findings, assertion
  and evidence acts, act log, currency, and read models.
- Derivation: rule artifacts, artifact package, operation-semantics canon,
  adoption gate, run records, publication acts, explanation pins, reference
  runner, and ADR-0010 composed currency.

### Implemented Here

- Production form-field schema/instances under ADR-0012.
- 2025 W-2-slip and box-1 fact-type content under ADR-0011.
- 2025 W-2 closure fact-type content and examples under ADR-0011, without an
  operational closure-to-collect mapping.
- Form 1040 line-1a form-field content with output-symbol binding, inert source
  reference, and disposition instructions.
- W-2 box-1 -> line-1a rule and bounded package content.

### Payload Instantiation Gate

Every new schema or materially changed relationship gets a hand-written
positive instance and isolated negative instance before runner code consumes
it. Prototype instances may guide production examples but are not copied
without re-validation against the accepted ADRs and production schema ids.

## Synthetic Fixtures

- `single_w2`: one W-2 box-1 finding publishes line 1a.
- `two_w2_same_employer`: two W-2-slip citizens from the same employer/year
  remain distinct and aggregate.
- `present_zero_w2`: a present W-2 finding with numeric zero publishes a
  computed zero, not a closure-backed zero.
- `w2_correction`: a later finding for the same W-2 fact displaces the original
  and the dependent line-1a finding; the second slip, if present, remains
  current.
- `w2_rederive`: an explicit subsequent run publishes the corrected line-1a
  successor.

All fixtures are synthetic and publishable. No value, identifier, or evidence
artifact derives from a real person.

## Verification

- `python3 -m unittest`
- `python3 tools/governance_lint.py`
- `python3 -m mypy`
- Focused schema positive/negative tests and published-manifest immutability.
- Package closure and unique-output validation over the bounded package.
- Forward/reference runner byte parity for every scenario.
- Derivation CLI goldens for `single_w2`, `two_w2_same_employer`, and
  `present_zero_w2`.
- Published-finding explanation walks for nonzero and computed-zero line 1a.
- ADR-0010 correction/displacement and explicit re-derivation golden.
- Data-safety scan for private markers, personal names, account identifiers, and
  absolute local paths.

## Exit Criteria

- ADR-0011 and ADR-0012 are reflected in production schemas/content and tests.
- No specialized tax-fact-type schema is introduced.
- W-2 fact identity contains no evidence/document key and distinguishes two
  same-employer/year slips.
- Same-fact correction displaces the original finding and derived line 1a;
  explicit rerun publishes the successor.
- Form 1040 line 1a is a first-class versioned form-field citizen distinct from
  its output symbol.
- The form-field schema carries all five disposition instructions; implemented
  runtime states never conflate present zero with missing/closed sources.
- The bounded package validates and both runners agree on every scenario.
- Full verification passes; committed data is synthetic.
- Milestone retrospective is written before the next milestone plan.
- The milestone branch merges non-fast-forward to `main` with one implementation
  commit per completed track.

## Tracks

### Track 0 - Citizen-Family Evidence Gate (Complete)

Goal: settle contract-foundational fact/form decisions before implementation.
Inputs: original planning input, governance, ADR-0005, prototype charters and
fixtures. Outputs: four exhibits, committee reviews, process retrospective,
narrow evaluation analysis, accepted ADR-0011 and ADR-0012, and this scope
amendment. Verification: process conformance and governance lint.
Migration risk: discharged for the accepted scope; excluded decisions remain
deferred. Data safety: documents and synthetic exhibits only.

### Track 1 - W-2 Vocabulary And Form-Field Contract

Goal: publish production schema/content implementing ADR-0011 and ADR-0012.
Boundary: no derivation rule or runnable workspace.
Inputs: ADR-0003, ADR-0011, ADR-0012, kernel schemas.
Outputs: production `form-field.v1` schema; positive/negative form-field
instances; W-2-slip entity examples; W-2 box-1 and closure fact-type bundle
content; line-1a form-field content; published schema manifest updates.
Verification: schema tests, isolated negatives, registry immutability, full
suite, governance lint.
Migration risk: creates durable production content ids and form-field contract.
Data safety: public form metadata and synthetic ids only.

### Track 2 - Synthetic W-2 Workspace And Correction

Goal: instantiate the ratified identity and lifecycle through the real kernel.
Boundary: no derived Form 1040 output yet.
Inputs: Track 1 bundle/content; kernel act log, evidence, assertion, projection,
and currency APIs.
Outputs: synthetic workspaces/fixtures for one slip, two same-employer slips,
present zero, and same-fact correction; current/displaced-state goldens.
Verification: workspace projection/read-model tests, identity collision
negative, correction/displacement tests, fixture data-safety scan.
Migration risk: fixture contract fixes W-2-slip identity and correction usage.
Data safety: manufactured employers, slips, evidence, and amounts only.

### Track 3 - Line-1a Rule Package And Integration

Goal: derive Form 1040 line 1a from current W-2 box-1 findings through adopted
machinery.
Boundary: nonempty present-source paths only; no closure-backed empty-source
publication, downstream Form 1040 lines, or new machinery.
Inputs: Tracks 1-2; ADR-0006 rule language; current derivation APIs; official
2025 Form 1040 and W-2 primary sources checked at implementation time.
Outputs: line-1a rule artifact, bounded package, source-reference content,
normal/two-slip/zero scenario runs, forward/reference parity, CLI goldens, and
published-value explanation goldens.
Verification: package validation, schema authority, runner parity, determinism,
CLI subprocess tests, explanation pin walks, full suite.
Migration risk: durable tax rule/package ids begin here.
Data safety: public tax law plus synthetic fixture values only.

### Track 4 - Correction Cascade, Documentation, And Completion

Goal: prove correction through derived displacement and explicit re-derivation,
then close the milestone cleanly.
Boundary: no auto-rerun orchestration and no W-2c documentary semantics.
Inputs: Track 3 package/scenarios; ADR-0010 workspace currency.
Outputs: correction/displacement/re-derivation golden; README, phase state,
roadmap status, and milestone retrospective.
Verification: correction golden, both runners, full unittest/mypy/governance
lint suite, data-safety scan, clean worktree.
Migration risk: none beyond accepted ADR-0010 and ADR-0011 behavior.
Data safety: synthetic only.

## Implementation Branch And Commit Shape

After this planning commit, create `milestone/first-tax-slice` from `main`.
Implementation history must contain one commit for each completed Track 1-4.
When all exit criteria pass, merge non-fast-forward into `main` with the
milestone name in the merge commit, delete the merged branch/worktree, and
write the milestone retrospective before planning follow-on work.
