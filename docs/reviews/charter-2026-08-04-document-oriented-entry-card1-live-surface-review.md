# Document-Oriented Entry — Card 1 Live-Surface Re-Review

Audience: Reviewer.

Status: **chartered for owner launch.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `milestone/document-oriented-entry`; resolve `HEAD` at launch and verify
  the SHA against Git before acting.
- **Exact object:** the unchanged Builder commit
  `7383729ecc3fe8b64a9cf6c41cf7085dd61296dc`, measured as its diff against
  parent `357140efaae46c58b92879c22706090fd3a60745`. Do not include either
  review record, this charter, or the phase-state pointer update in the object
  under review.
- **Role:** author-independent Reviewer for the live-surface portion of
  Document-Oriented Entry Card 1.
- **Purpose:** close or retain the one open measurement from the prior
  reviews: direct browser evidence for the committed synthetic workspace map.
- **Evidence ceiling:** the committed synthetic runtime and surface, a
  running local Chromium/Chrome session, focused browser-gated tests, direct
  Git diff, and the existing review records as orientation only. No real data,
  owner attestation, maturity movement, new ADR, repair, or architectural
  contract claim.
- **Environment preconditions:** the host must provide a Chromium- or
  Chrome-compatible executable and the vendored surface tree at
  `packages/sample_data/entry_loop_t1/surface/content/node_modules`. If a
  precondition is unavailable, stop and report **NOT-CONFIRMED** rather than
  substituting static inspection or an API-only probe.
- **Stop conditions:** stop and report a charter mismatch if the resolved
  commit is not the Builder commit named above, if the Builder object changed,
  if the browser run requires real or personal data, if the exercise requires
  repairing the surface, or if the review would require interpreting
  governance text. Do not modify implementation files, fixtures, manifests,
  review history, or phase state during the review.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`;
  `docs/adr/INDEX.md`; `docs/reviews/charter-2026-08-03-document-oriented-entry-card1-review.md`;
  `docs/reviews/review-2026-08-04-document-oriented-entry-card1.md`;
  `docs/reviews/charter-2026-08-02-document-oriented-entry-card1.md`;
  `docs/phases/legible-entry/milestones/document-oriented-entry.md`;
  `packages/sample_data/entry_loop_t1/surface/content/app/src/WorkspacePage.svelte`;
  `packages/sample_data/entry_loop_t1/surface/content/app/src/EntryPage.svelte`;
  `tests/test_entry_loop_t1.py`; and `AGENTS.md#Data Safety Rules`.

Before acting, echo the resolved commit, exact review object, scope, evidence
ceiling, environment preconditions, and stop conditions. This charter is the
controlling boundary.

## Measurements

1. **Environment readiness.** Confirm the browser executable and vendored
   surface dependencies are available. Record the exact commands and whether
   the fixture can be served locally. Missing prerequisites yield
   **NOT-CONFIRMED** for the live-surface measurement; do not install or alter
   project dependencies as part of the review.
2. **Rendered source-context map.** In the running synthetic workspace,
   observe the W-2, 1099-DIV, and question contexts, their labels, kinds,
   statuses, and related fields in the missing, partially answered, and fully
   answered fixture states where the harness supports them.
3. **Entry controls and accessibility.** Exercise every context control with
   keyboard traversal, visible focus, accessible names, and both entry orders.
   Confirm that each related-field control targets the existing contribution
   surface and that the browser does not silently skip or reorder the map.
4. **Round trip.** Open a context and return to the workspace. Confirm that
   the selected context and existing entry/explanation navigation remain
   usable. Do not submit real values or claim persistence beyond the synthetic
   fixture's existing behavior.

## Verdict standard

Return **READY** only if all four measurements have direct browser evidence
and the unchanged Builder object remains within Card 1. Return
**NOT-CONFIRMED** if the environment prevents a running browser measurement.
Return **NOT READY** only for a concrete product or charter failure observed
in the running synthetic surface. Do not repair the Builder unit.

## Review record

Write a new record under `docs/reviews/` naming the exact Builder commit and
parent. Report each measurement separately, include the environment
precondition result, distinguish READY from NOT-CONFIRMED, and state the
smallest owner-facing disposition. The review record must not advance the
phase-state pointer.

## Data safety

Use only the committed synthetic fixture and `demo.*` / `demo-*` identifiers.
Do not read, create, or report personal documents, values, dispositions,
workspace locations, screenshots, private outputs, or generated artifacts
derived from real data.
