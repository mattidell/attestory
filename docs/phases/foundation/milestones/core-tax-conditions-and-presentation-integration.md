# Milestone: Core Tax Conditions And Presentation Integration

Audience: Agents (Objective and Scope are Shared)

Status: **in progress — implementation (Track 1 active; Tracks 2–7 open, sequenced).** Next milestone after Source Completeness And Interest Slice (completed 2026-07-12).

## Revision note (2026-07-14, principal foreman)

**Update (same day, post ADR-0026):** Track 0.a closed — ADR-0026 accepted. Track 0 is **3 of 5**. Track 0.b plan drafted and proposed to owner.


**Update (2026-07-15):** ADR-0027 + ADR-0028 accepted (manifests). **ADR-0029 accepted** (citations). **Track 0 complete (5/5).** Implementation tracks **opened**; Track 1 (contract schemas) active first.

This plan was revised after the governance remediation. Two corrections to the original:

1. **Track 0 was never complete.** Only two of the five contract topics carry conforming, rival-backed evidence and ratified ADRs: conditional structures (**ADR-0024**) and its expression-language extensions (**ADR-0025**), and non-publication explanations (**ADR-0020**), all ratified 2026-07-13/14. The other three — taxable-interest composition (ADR-0021), adopted-content manifests (ADR-0022), citation resolution (ADR-0018) — exist only as **single-author paper spikes with no clean-room rival, committee review, or evaluation analysis** (0018 has no prototype artifact at all). Under the ADR-0013 amendment (non-accepted ADRs are inert; every prototype round requires independently-contexted rival evidence), those three proposed ADRs are inert drafts, not decisions. The owner directed (2026-07-14) that **all three be remediated** with conforming rounds before their implementation tracks.

2. **Implementation was reset.** Track work built on proposed ADRs was removed from the milestone branch (pre-reset history at `archive/core-tax-conditions-pre-reset`; Track 3 WIP parked at `wip/track3-core-conditions`, reference only). Implementation tracks rebuild on the ratified ADRs and inherit their production conditions (listed per track below).

Sequencing: **Track 0 complete (2026-07-15).** Implementation tracks may open; each inherits production conditions from the ratified ADRs. Each remediation follows the pattern just used for conditional-selectors/expression-language-extensions/non-publication-explanations — owner-launched incumbent + clean-room rival exhibits under foreman custody, owner-launched committee (Governance + Adversary), foreman evaluation analysis, owner ratification of a conforming ADR that supersedes the inert draft.

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
- **Ratified Track-0 decisions (implementation open 2026-07-15):** ADR-0024 (conditional structures in the rule language) + ADR-0025 (expression-language extensions: declared optional defaults and categorical comparison); ADR-0020 (non-publication explanation walking — durable run disposition ledger). Implementation rebuilds under these; see the per-track production conditions.
- **Settled this remediation cycle:** ADR-0026 (taxable-interest composition) accepted 2026-07-14, superseding inert ADR-0021.
- **Non-conforming proposed drafts (inert, need remediation):** ADR-0022 (manifests — plan drafted), ADR-0018 (citations) — paper spikes only, no rival evidence.
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

- All five Track-0 topics carry conforming rival-backed evidence and ratified ADRs: condition structure (0024/0025) and explanations (0020) are done; interest composition (0021 successor), manifests (0022 successor), and citations (0018 successor) are remediated with incumbent + clean-room rival + committee rounds and ratified, superseding the inert spike drafts.
- The ratified ADRs' production conditions are met: ELX PC1 (transitive `origin` pins), PC2 (`CATEGORICAL_DOMAIN_MISMATCH` added to ADR-0012 vocabulary), PC3 (default-resolution correction-fold validation, parity, ELX fixtures); NPE-G10 (single-surface fold + fixture repair landed with the schema); NPE-A21 (mixed multi-publisher projection defined).
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

Goal: Settle all five contract-foundational topics with conforming, rival-backed evidence before implementation.

**Settled (ratified, conforming):**
- ✅ Conditional standard-deduction / tax-method selection → **ADR-0024** (conditional structures) + **ADR-0025** (declared optional defaults, categorical comparison). Evidence: `docs/prototypes/conditional-selectors/`, `docs/prototypes/expression-language-extensions/`.
- ✅ Non-publication explanation walks → **ADR-0020** (durable run disposition ledger). Evidence: `docs/prototypes/non-publication-explanations/`.

**Remediation outstanding (owner directive 2026-07-14 — remediate all three; inert drafts are superseded, never silently ratified):**
- ✅ **0.a Taxable-interest composition → ADR-0026 accepted** (Track 0.a closed 2026-07-14). Mechanism + honest-partial OID-inclusive line-2b boundary; supersedes inert ADR-0021. Evidence: `docs/prototypes/taxable-interest-composition/`.
- ✅ **0.b Adopted-content manifests → ADR-0027 + ADR-0028 accepted** (2026-07-15; supersedes inert ADR-0022). Floor + fact-surface + composition-obligation. Track 4 full membership closure unblocked.
- ✅ **0.c Citation resolution → ADR-0029 accepted** (2026-07-15; supersedes inert ADR-0018). Structural/adoption-only resolver; single form-field pin; rule pin array; four discriminated authority families.
- Verification per topic: conformance verdicts, committee reviews, evaluation analysis, process log.
- Commit: one governance commit per ratified ADR (foreman custody).

### Track 1 - Contract Schemas And Payload Instances

**Status: in progress** (opened 2026-07-15).

Goal: Publish the production contract schemas ratified in Track 0. Opens only after Track 0 is fully ratified.
- Publish the ADR-0024/0025 conditional-structure schemas: `fact-type.v2` (`optional_default`), `artifact-package.v2` (`input_bindings`), `derived-finding.v2` (`resolved_input` branch), pin-schema (`default` role, `input`-pin `origin`), `rule-artifact.v2` (`categorical_compare`, `category_literal`), `operation-semantics.v2`. **ELX PC1:** the `input`-pin `origin` field is required and copied transitively. **ELX PC2:** add `CATEGORICAL_DOMAIN_MISMATCH` to the ADR-0012 disposition vocabulary (a vocabulary amendment, not just a schema).
- Publish the ADR-0020 record change: the single-surface disposition ledger fold on `derivation-record.v1` (ledger authoritative, `blocked[]` derived) **and repair the self-contradictory `derivation-record.completed.json` fixture concurrently (NPE-G10 prerequisite)**; the `npe-walk.v1` schema with `rule_references[]` arrays.
- Publish the manifest and citation schemas ratified in Track 0.a–0.c.
- Commit positive and negative payload instances for each schema.
- Verification: schema tests, isolated negatives, registry immutability.
- Commit: one Track 1 contract schema commit.

### Track 2 - Taxable Interest Composition and Line 2b

**Status: open** (blocked only on Track 1 schemas it consumes).

Goal: Implement interest composition and Form 1040 line 2b, per the ratified ADR-0021 successor.
- Add line 2b form-field and rule artifact, consuming the B1 subtotal.
- Define interest composition mapping as ratified.
- Verification: forward/reference runner parity, scenario tests for empty/closed/unclosed interest.
- Commit: one Track 2 line-2b interest commit.

### Track 3 - Core Tax Conditions (Standard Deduction & Tax Method)

**Status: open** (rebuild on ADR-0024/0025; `wip/track3-core-conditions` reference only).

Goal: Implement the conditional selection logic for standard deduction and tax computation under ADR-0024 + ADR-0025 (rebuild; the `wip/track3-core-conditions` parking is reference-only and built on the rejected ADR-0019).
- Add standard deduction amount lookup tables (parameter citizens `p.standard-deduction`, `p.additional-deduction`) and the guarded selection rules; filing status as a first-class categorical domain (ADR-0025 decision 5), migrating off ADR-0024's interim numeric-string codes via the governed successor-claim path.
- Add tax table lookup tables (`p.brackets`) and the bracket-fold select rule.
- Optional demographic scalars (`taxpayer_age65`, `taxpayer_blind`) use ADR-0025 declared optional defaults (`optional_default` on `fact-type.v2`).
- Implement Form 1040 lines 9, 11, 12, 15, and 16.
- **ELX PC3:** mixed-family correction-fold validation for default-resolution findings; two-runner parity; the five ELX Gate-2 cases as synthetic fixtures.
- Verification: parity, unit tests for standard-deduction selection, categorical guards, and tax tables.
- Commit: one Track 3 core tax calculations commit.

### Track 4 - Adopted Content Manifests & Package Verification

**Status: open** (implements ADR-0027/0028).

Goal: Build the adopted-content manifests and enforce package verification.
- Implement package validation that reads the manifest and asserts version-locked graph completeness.
- Verification: package validation tests, missing dependency negatives.
- Commit: one Track 4 manifest commit.

### Track 5 - Citation Resolution & Non-Publication Explanations

**Status: open** (implements ADR-0029 + ADR-0020).

Goal: Implement the citation resolver (ratified ADR-0018 successor) and the ADR-0020 non-publication explanation walker.
- Add the semantic citation resolver as ratified.
- Implement the run disposition ledger: the runner writes one row per package rule artifact using ADR-0020 decision 1a's classification order (absent dependency → `blocked`; else already-published conflict-loser → `inapplicable` with a `superseded_by` reference and no synthetic guard; else evaluate), applied identically by the saturation runner and the reference runner's `finalize_unreached()`.
- Implement the `npe-walk.v1` walker as a pure projection with ADR-0020 decision 4 run-scoped finding selection (ledger published-ref for the run → run-scoped act-log `derived-publication` → ledger non-published row → `no_disposition_recorded`), cycle detection, and the shared memoization table.
- Modify `explanation.py` to accept the additive optional shared-memoization parameter (ADR-0020 decision 2); committed single-branch behavior preserved when the parameter is absent.
- Define the mixed-disposition projection for multi-publisher symbol nodes (NPE-A21 production condition).
- Verification: explanation tests on blocked/inapplicable/conflict-loser scenarios; interrupted-run recovery walk; two-runner ledger parity; multi-run same-symbol run-scoped selection.
- Commit: one Track 5 citation and explanation commit.

### Track 6 - Integration and Lifecycle Verification

**Status: open** (after Tracks 2–5 content lands).

Goal: Verify the entire Cascade and scenarios.
- Add scenarios: `single_standard_deduction`, `mfj_standard_deduction`, `standard_deduction_age_blind`, `itemized_deduction_override`, `unclosed_interest_composition`, `tax_bracket_boundaries`.
- Verification: forward/reference parity, CLI goldens.
- Commit: one Track 6 integration scenario commit.

### Track 7 - Completion

**Status: open** (milestone close).

Goal: Close the milestone.
- Update phase state and roadmap documents.
- Write the milestone retrospective.
- Confirm branch and history shape.
- Commit: one Track 7 completion-documentation commit.
