# Milestone: Core Tax Conditions And Presentation Integration

Audience: Agents (Objective and Scope are Shared)

Status: **proposed.** Next milestone after Source Completeness And Interest Slice (completed 2026-07-12).

## Objective

Prove the integration of downstream Form 1040 lines (2b, 9, 11, 12, 15, 16) and selection logic. This milestone turns the remaining foundational tax contracts from conversational questions into an operating substrate:
1. **Taxable-interest universe composition.** Establish the coextensive composition or broader taxable-interest universe required by ADR-0016 for Form 1040 line 2b publication.
2. **Standard-deduction/tax-method condition structure.** Establish how the conditional standard deduction and tax calculation method selections are modeled and derived (e.g., as aggregate facts, structured facts, or rule-driven derivations).
3. **Adopted-content manifests.** Build the complete manifest schema that closes over all rules, schemas, form-fields, and parameter constraints for version-locked derivation packages.
4. **Citation authority.** Settle the citation resolver schema and semantic attachment contract, replacing inert opaque strings with verifiable legal citations.
5. **Non-publication explanations.** Implement explanation walks and lineage representation for non-publication output states (`blocked`, `guard_inapplicable`, and `invalid`).

## Why This Is A Separate Milestone

The previous retrospective (`docs/milestone-retrospectives/2026-07-12-source-completeness-and-interest-slice.md`) and evaluation exclusions verified that downstream lines cannot be added as ordinary content breadth. Standard-deduction selection and tax method select logic are conditional computations that shape all downstream facts, and their modeling contracts are currently unresolved. In accordance with `PROJECT_PLANNING.md` and ADR-0013, these contract-foundational Tier 2/3 decisions must receive their own prototype-driven evidence before production implementation.

## Current State

- The W-2 box-1 wages (`tax.us.2025.wages.total-w2-box1` -> Form 1040 line 1a) and the Form 1099-INT box-1 subtotal (`tax.us.2025.interest.b1-subtotal`) calculations are stable and fully verified on synthetic workspaces.
- Atomic family horizons, horizon citizens, and member-transition acts are implemented and project through derivation currency (ADR-0017).
- No Form 1040 line 2b exists; interest aggregation blocks at the subtotal layer because no coextensive composition has been declared or mapped for the broader taxable-interest universe.
- Standard deduction, taxable income, and tax table calculations do not exist.
- Form-field citizens support the five ADR-0012 dispositions in content, but the explanation API only supports walks for published values (nonzero and computed/closure zeros).
- Citation references remain inert opaque strings.

## Scope

- **Track 0 decision processes:** Settle taxable-interest composition, condition structure for standard-deduction/tax-method selection, adopted-content manifests, citation resolution, and non-publication explanation walks. Ratify ADRs (Tier 2/3).
- **Tax year 2025, US federal individual income tax.**
- **Form 1040 Line 2b (Taxable Interest).** Implement the coextensive interest composition contract or broader taxable-interest universe.
- **Form 1040 Line 9 (Total Income), Line 11 (Adjusted Gross Income), Line 12 (Standard Deduction), Line 15 (Taxable Income), and Line 16 (Tax).**
- **Standard deduction selection logic.** Implement standard deduction lookups (Single, Married Filing Jointly) and age/blindness/dependency adjustments.
- **Tax computation select logic.** Implement selection of the correct tax calculation method (e.g., Tax Table bracket fold vs. Tax Computation Worksheet).
- **Adopted-content manifest schema.** Build the manifest runner loader that validates that a package's rules, schemas, parameters, and form-fields form a closed, version-locked graph.
- **Citation resolver and semantic pins.** Build the resolver contract and update form-field examples to bind validated citations.
- **Non-publication explanation walker.** Extend explanation walking to reconstruct the exact lineage and reason for blocked or inapplicable output dispositions.
- **Synthetic scenarios** covering filing status, age/blindness, itemization selection (asserted bypass), tax bracket boundaries, unclosed interest composition, and blocked downstream lines.

## Non-Goals And Deferred Boundaries

- No Schedule A (Itemized Deductions) line-by-line derivation; itemization is supported only as an asserted elective fact that overrides the standard deduction.
- No Schedule B (Interest and Ordinary Dividends) detailed reporting; only the Form 1040 line 2b rollup and composition.
- No other Form 1040 income types (dividends, pensions, capital gains, etc.) beyond wages and interest.
- No tax credits, tax payments, or refund/balance due lines (lines 17–38).
- No multi-year, multi-jurisdiction, or non-resident return structures.
- No UI, persistence changes, or document-extraction integrations.

## Contracts

### Existing
- Kernel: act log, facts, findings, horizon currency, member transitions.
- Derivation: rule artifacts, artifact packages, single-dispatch collect mapping, saturation runner, explanation walker.
- Tax: W-2 wages and 1099-INT box-1 subtotal content, Form 1040 line 1a form-field.

### Implemented Here
- Production schemas for adopted-content manifests, citation resolver mappings, and conditional select structures.
- Form 1040 lines 2b, 9, 11, 12, 15, and 16 form-field citizens and rule artifacts.
- Tax parameter declarations for 2025 standard deduction amounts and tax bracket tables.
- Semantic citation resolver bindings.
- Extended non-publication explanation API.

## Synthetic Fixtures

- `single_standard_deduction`: Single filer, W-2 only, standard deduction applied, tax table lookup.
- `mfj_standard_deduction`: Married Filing Jointly, combined W-2 and 1099-INT, standard deduction applied.
- `standard_deduction_age_blind`: Single filer over 65 and blind, asserting the increased standard deduction amount.
- `itemized_deduction_override`: Asserted elective fact for itemized deductions overriding the standard deduction.
- `unclosed_interest_composition`: 1099-INT family unclosed, causing line 2b and all downstream lines (9, 11, 12, 15, 16) to block.
- `tax_bracket_boundaries`: Workspaces crossing bracket thresholds to verify the bracket fold expression.

## Verification

- `python3 -m unittest`
- `python3 tools/governance_lint.py`
- `python3 -m mypy`
- Positive and isolated negative examples for all new schemas (manifests, citations, conditions).
- Package closure verification over the complete 2025 core package.
- Two-runner byte parity across all new synthetic scenarios.
- Extended explanation walk validation for `blocked` and `guard_inapplicable` form fields.
- Data-safety scan for private paths and account-identifier digit runs.

## Exit Criteria

- Track 0 evaluation analyses are written; ADRs for interest composition, condition structure, manifests, citations, and explanations are ratified.
- Form 1040 line 2b publishes correctly under the coextensive interest composition or blocks if the composition is unclosed.
- Downstream lines (9, 11, 12, 15, 16) derive correctly on all golden scenarios.
- Standard deduction is calculated based on filing status and age/blindness/dependency conditions, and can be overridden by itemization.
- Tax computation selects the correct bracket worksheet or tax table and calculates the correct tax.
- The adopted-content manifest validates package completeness and version locking.
- Citation references are verified and resolved semantically.
- Walkthroughs for non-publication states (blocked/inapplicable) report the exact missing dependencies or inapplicable guards.
- Full verification passes and commits are atomic, one per track.
- Milestone retrospective is written.

## Tracks

### Track 0 - Contract Decisions

Goal: Settle the five contract-foundational topics before implementation.
- Run prototype iterations and write evaluations for:
  - Taxable-interest composition (Form 1040 line 2b).
  - Conditional standard deduction and tax method selection.
  - Adopted-content manifests.
  - Citation resolution.
  - Non-publication explanation walks.
- Draft and ratify Tier 2/3 ADRs.
- Verification: prototype reviews, conformance verdicts, process logs.
- Commit: one planning update/ADR commit.

### Track 1 - Contract Schemas And Payload Instances

Goal: Publish the production contract schemas and payload instances ratified in Track 0.
- Publish schemas for adopted-content manifests, citation resolution, and conditional structures.
- Commit positive and negative payload instances for each schema.
- Verification: schema tests, isolated negatives, registry immutability.
- Commit: one Track 1 contract schema commit.

### Track 2 - Taxable Interest Composition and Line 2b

Goal: Implement interest composition and Form 1040 line 2b.
- Add line 2b form-field and rule artifact, consuming the B1 subtotal.
- Define interest composition mapping.
- Verification: forward/reference runner parity, scenario tests for empty/closed/unclosed interest.
- Commit: one Track 2 line-2b interest commit.

### Track 3 - Core Tax Conditions (Standard Deduction & Tax Method)

Goal: Implement the conditional selection logic for standard deduction and tax computation.
- Add standard deduction amount lookup tables and select rule.
- Add tax table lookup tables and select rule.
- Implement Form 1040 lines 9, 11, 12, 15, and 16.
- Verification: parity, unit tests for standard deduction selection and tax tables.
- Commit: one Track 3 core tax calculations commit.

### Track 4 - Adopted Content Manifests & Package Verification

Goal: Build the adopted-content manifests and enforce package verification.
- Implement package validation that reads the manifest and asserts version-locked graph completeness.
- Verification: package validation tests, missing dependency negatives.
- Commit: one Track 4 manifest commit.

### Track 5 - Citation Resolution & Non-Publication Explanations

Goal: Implement citation resolver and extended explanation walks.
- Add semantic citation resolver.
- Implement explanation walking for blocked and inapplicable form fields.
- Verification: explanation tests on blocked/inapplicable scenarios.
- Commit: one Track 5 citation and explanation commit.

### Track 6 - Integration and Lifecycle Verification

Goal: Verify the entire Cascade and scenarios.
- Add scenarios: `single_standard_deduction`, `mfj_standard_deduction`, `standard_deduction_age_blind`, `itemized_deduction_override`, `unclosed_interest_composition`, `tax_bracket_boundaries`.
- Verification: forward/reference parity, CLI goldens.
- Commit: one Track 6 integration scenario commit.

### Track 7 - Completion

Goal: Close the milestone.
- Update phase state and roadmap documents.
- Write the milestone retrospective.
- Confirm branch and history shape.
- Commit: one Track 7 completion-documentation commit.
