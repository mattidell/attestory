# Document-Oriented Entry — Card 1: Source-Context Map

Audience: Builder.

Status: **chartered for owner launch.**

## Context Capsule

- **Source ref and resolved launch commit:** `main-ui` at
  `29e2e5c` (`Plan Document-Oriented Entry milestone`). Resolve `HEAD` at
  launch and verify that it matches the committed source ref before acting.
- **Exact object:** Card 1, the source-context map experiment. Build only the
  smallest synthetic map and its supporting view-model shape; do not implement
  the grouped entry page from Card 2.
- **Role:** Document-Oriented Entry Card 1 Builder, owner-launched.
- **Scope and evidence-rung ceiling:** committed synthetic fixtures, focused
  tests, and a running local browser against the existing entry-loop surface.
  No real data, owner attestation, maturity movement, ADR, or architectural
  contract claim.
- **Stop conditions:** stop and report if the experiment requires new tax
  logic, a published schema or citizen, direct fact writes, a new act kind,
  real or personal data, a new persistence contract, interpretation of
  governance text, or a context label that cannot be grounded in existing
  synthetic state. Stop if implementing grouped entry, correction-flow
  redesign, or a universal document taxonomy is necessary to answer Card 1.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/roles/craft-notes.md#Builder`;
  `docs/adr/INDEX.md`;
  `docs/phases/legible-entry/milestones/document-oriented-entry.md`;
  `docs/phases/legible-entry/milestones/workspace-prototype.md`;
  `docs/milestone-retrospectives/2026-08-02-workspace-prototype.md`;
  `packages/derivation/entry_loop.py`;
  `packages/derivation/presentation_projection.py`;
  `packages/sample_data/entry_loop_t1/surface/content/app/src/WorkspacePage.svelte`;
  `packages/sample_data/entry_loop_t1/surface/content/app/src/EntryPage.svelte`;
  `tests/test_entry_loop_t1.py`;
  `AGENTS.md#Data Safety Rules`; and `AGENTS.md#Fixture Rules`.

Before writing, echo the resolved commit, scope, evidence ceiling, and stop
conditions. The charter is the controlling boundary for this unit.

## Questions to answer

1. Can the existing field contract support a small, stable source-context map
   without duplicating field declarations or inventing tax meaning?
2. Can the synthetic workspace name and distinguish the two document
   contexts — Form W-2 and Form 1099-DIV — while showing their related field
   keys and current attention state?
3. Can one non-document context be named honestly from existing synthetic
   state, using a question, decision, or taxpayer label rather than a blank or
   generic document label?

## Required experiment cases

- Both document contexts with their fields missing.
- One document answered while the other remains missing.
- Both documents answered.
- A question context derived only from existing missing/attention state; if
  no honest non-document context exists without new tax meaning, stop with
  that finding instead of fabricating one.
- Keyboard traversal and accessible names for every context control.

## Deliverables

- A synthetic source-context view-model or equivalent local surface shape,
  keyed by stable demo identifiers and containing context kind, label, and
  related field keys.
- A workspace map that renders the two document contexts and the grounded
  non-document question context, with missing/answered attention state sourced
  from the existing model.
- Focused tests proving context membership and labels are sourced and remain
  stable across the required fixture states.
- A builder commit containing only the Card 1 implementation, tests, and
  synthetic fixture changes required by those cases.

## Verification

- Run `python3 -m unittest tests.test_entry_loop_t1`.
- Exercise the resulting page through the fixture's running-browser journeys,
  including keyboard operability and both entry orders.
- Inspect the rendered context labels and related-field membership in the
  running browser; static markup alone is not evidence of the interaction.
- Run `git diff --check` before reporting the unit ready.

## Data safety

Use only committed synthetic fixtures and `demo.*` / `demo-*` identifiers.
Do not read, create, or report personal documents, values, dispositions,
workspace locations, screenshots, or generated artifacts derived from real
data.
