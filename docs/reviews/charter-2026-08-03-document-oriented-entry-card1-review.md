# Document-Oriented Entry — Card 1 Review

Audience: Reviewer.

Status: **chartered for owner launch.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `milestone/document-oriented-entry`; resolve `HEAD` at launch and verify
  the SHA against Git before acting.
- **Exact object:** the Builder commit named `Build Document-Oriented Entry
  Card 1: Source-Context Map`, reviewed as its diff against its parent. Do not
  include this review charter or the Foreman pointer update in the object
  under review.
- **Role:** author-independent Reviewer for Document-Oriented Entry Card 1.
- **Scope and evidence-rung ceiling:** the committed synthetic runtime,
  surface, manifests, focused tests, live local browser behavior, direct Git
  diff, and envelope scan. No real data, owner attestation, maturity movement,
  new ADR, or architectural contract claim.
- **Stop conditions:** stop and report a charter mismatch if the resolved
  commit is not the Builder commit named above, if the unit contains changes
  outside the Card 1 charter without an explicit disposition, if the review
  would require interpreting governance text, or if any real value, document,
  workspace location, screenshot, private output, or personal artifact
  appears. Do not repair the build or change phase state.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`;
  `docs/adr/INDEX.md`;
  `docs/reviews/charter-2026-08-02-document-oriented-entry-card1.md`;
  `docs/phases/legible-entry/milestones/document-oriented-entry.md`;
  `docs/phases/legible-entry/milestones/workspace-prototype.md`;
  `docs/milestone-retrospectives/2026-08-02-workspace-prototype.md`;
  `packages/derivation/entry_loop.py`;
  `packages/derivation/presentation_projection.py`;
  `packages/sample_data/entry_loop_t1/surface/content/app/src/WorkspacePage.svelte`;
  `packages/sample_data/entry_loop_t1/surface/content/app/src/EntryPage.svelte`;
  `tests/test_entry_loop_t1.py`;
  the changed surface adoption and release manifests;
  `AGENTS.md#Data Safety Rules`; and `AGENTS.md#Fixture Rules`.

Before acting, echo the resolved commit, exact review object, scope, evidence
ceiling, and stop conditions. The review charter is the controlling boundary.

## Measurements

1. **Charter conformance.** Compare the committed diff to Card 1's questions,
   required cases, deliverables, and stop conditions. Confirm that grouped
   context entry, correction-flow redesign, universal taxonomy, and new tax
   meaning remain outside this unit.
2. **State evidence.** Run
   `python3 -m unittest tests.test_entry_loop_t1` and verify the missing,
   one-answered, and both-answered source-context cases. Confirm that context
   labels, kinds, field membership, and statuses come from the expected
   synthetic state rather than duplicated UI literals.
3. **Live surface evidence.** Exercise the workspace in a running local
   browser. Measure the rendered W-2, 1099-DIV, and question contexts, their
   related fields, entry links, accessible names, keyboard traversal, and
   both entry orders. Static markup is not sufficient.
4. **Boundary and artifact evidence.** Trace an entry control through the
   existing contribution endpoint and confirm no direct fact write or new act
   kind was introduced. Inspect the adoption, release, registry, and manifest
   changes for exact synthetic artifact identity and no unrelated published
   history mutation. Examine the `$id` handling change in schema validation
   for any weakening of validation rather than accepting its test edits.
5. **Safety evidence.** Run
   `python3 tools/envelope_scan.py --range <base>..HEAD` with the correct base
   for the Builder unit, and confirm all identifiers and fixtures remain
   synthetic and locator-free.

## Verdict standard

Return **READY** only if each measurement has direct evidence and the unit
answers Card 1 without expanding its scope. Return **NOT READY** with a
concrete finding when a required case fails, a boundary is weakened, a
label/status is fabricated, accessibility is ambiguous, or the artifact
changes exceed the charter. Record what was measured, the evidence location,
and the smallest owner-facing disposition; do not repair the unit.

## Review record

Write the measured result to a new review record under `docs/reviews/`. The
record must name the exact Builder unit, list each check and result, disclose
any environment limitation, and distinguish READY from untested or
NOT-CONFIRMED claims.
