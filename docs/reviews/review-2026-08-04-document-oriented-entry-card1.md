# Review — Document-Oriented Entry Card 1 (Source-Context Map)

- **Reviewer seat:** author-independent Reviewer, chartered by
  `docs/reviews/charter-2026-08-03-document-oriented-entry-card1-review.md`.
- **Resolved HEAD at review:** `7a57848` (includes prior review record and
  review charter; those are **not** part of the review object).
- **Review object:** Builder commit
  `7383729ecc3fe8b64a9cf6c41cf7085dd61296dc`
  (`Build Document-Oriented Entry Card 1: Source-Context Map`).
- **Diff base (parent of object):**
  `357140efaae46c58b92879c22706090fd3a60745`.
- **Scope measured:** organize workspace input by named source contexts;
  document as normal context; honest non-document question context; related
  fields under each context; preserve contribution-only entry, explanation
  walk, and return-to-workspace shape. Card 2 grouped entry, correction-flow
  redesign, universal taxonomy, and new tax meaning remain out of scope.
- **Evidence ceiling:** committed synthetic runtime, surface, manifests,
  focused tests, live local browser behavior, direct Git diff, envelope scan.
  No real data, owner attestation, maturity movement, new ADR, or contract
  claim.
- **Environment limitations:** this host has Node (`v20.20.2`) but **no**
  Chromium/Chrome binary and **no** surface `content/node_modules` vendored
  tree. All `unittest` cases gated on Node+browser+vendored tree are
  **skipped** (7 skips). Live DOM, keyboard traversal, and rendered
  interaction on `workspace.html` are therefore **NOT-CONFIRMED** here.

A prior review record exists at
`docs/reviews/review-2026-08-03-document-oriented-entry-card1.md`. This record
is an independent re-measurement of the same Builder unit; it does not rely
on that record as evidence.

## Measurements

### 1. Charter conformance

- **Result:** READY
- **Evidence:** `git diff --stat 357140e..7383729` and full diff of the seven
  paths in the Builder commit.
- **Finding:** The unit adds a synthetic `source_contexts` view-model in
  `packages/derivation/entry_loop.py`, renders it on
  `WorkspacePage.svelte`, and covers the three required map states in
  `SourceContextMapCard1`. It does **not** open a grouped context entry page
  (Card 2), redesign correction, publish a document citizen, or introduce tax
  meaning. Document contexts are Form W-2 and Form 1099-DIV; the non-document
  context is kind `question` with an explicit question label rather than a
  blank or generic document label. Entry from the map uses the existing
  `./index.html#field=<key>` contribution surface links. Scope matches Card 1
  questions, required cases (except live keyboard, see §3), and deliverables.

### 2. State evidence

- **Result:** READY
- **Evidence:**
  - `python3 -m unittest tests.test_entry_loop_t1` → **50 tests, 0 failures,
    7 skipped** (browser/vendored). All three
    `SourceContextMapCard1` cases pass:
    both-missing, one-answered/one-missing, both-answered.
  - Direct HTTP probe of the synthetic loopback server’s `/api/state` (runtime
    + `EntryLoopServer`, not a browser) returns the same three contexts with
    synthetic ids `demo.source-context.w2`,
    `demo.source-context.div1099`, and
    `demo.source-context.question.unanswered-facts`.
  - Code inspection of `_source_contexts`: document labels are read from
    `fields[...].source.document` (field contract), not from UI string
    literals; statuses are derived from the missing-fact set; question status
    is `attention` vs `complete` from the same set. UI renders
    `ctx.label` / `ctx.kind` / `ctx.status` / `ctx.field_keys` from state and
    field membership text from `state.field_contract[key]`.
- **Finding:** Missing / partial / full map states are covered. Document
  labels and field membership are state-sourced. The question **label** text
  is a fixed synthetic string in the view-model builder (not field metadata);
  its **status and field_keys** are still derived from existing missing state.
  That matches the Card 1 allowance to name a non-document context honestly
  without inventing tax meaning or a document citizen. No duplicated tax
  meaning in the UI.

### 3. Live surface evidence

- **Result:** NOT-CONFIRMED (environment limitation)
- **Evidence attempted:**
  - Browser-gated suite skipped: no Chromium/Chrome; no
    `packages/sample_data/entry_loop_t1/surface/content/node_modules`.
  - Static source inspection of the committed `WorkspacePage.svelte` map
    section: section labelled via `aria-labelledby="contexts-title"`; each
    context exposes kind, label, status; related-field Enter controls are
    native links with **distinct** `aria-label` values of the form
    `Enter {document} {box} ({ctx.label})`; global `:focus-visible` and
    `.button-link` `min-height: 44px` styles already present on the page.
  - Loopback `/api/state` confirms the payload the page would load (see §2).
- **Finding:** Charter requires exercising the workspace in a **running local
  browser** (keyboard traversal, both entry orders, rendered labels). That
  measurement could not be completed on this host. Static markup and API
  payload are **not** substituted as proof of interaction. Accessible-name
  construction looks correct in source, but keyboard order and focus behavior
  of the new context controls remain unproven here.

### 4. Boundary and artifact evidence

- **Result:** READY
- **Evidence:**
  - Diff introduces no new act kind, no direct fact write path, and no change
    to contribution admission. Workspace surface only `fetch`es `./api/state`
    and links to `./index.html#field=...` (existing entry path).
  - Manifest / adoption / release / registry updates are checksum and byte
    identity for the changed `WorkspacePage.svelte` package only.
  - Independent hash of the Builder-commit blob for
    `src/WorkspacePage.svelte`:
    `sha256=89e13a638fd179586d5610c6a0129b7af14a887850472aca68bddf8770ade5fb`,
    `bytes=15392`, matches the surface-artifact manifest entry at `7383729`.
  - `FixtureRegeneration.test_surface_publication_regenerates_byte_for_byte`
    and related fixture tests pass under the suite in §2.
  - `$id` handling: production validator and three field-contract tests strip
    schema `$id` before `Draft202012Validator` / `jsonschema.validate`. The
    entry-field schema’s `$ref`s are all local (`#/$defs/...`); stripping `$id`
    does not drop constraints or broaden acceptance. Paired with
    `check_schema(document)` still run on the full document. No validation
    weakening observed.
- **Finding:** Contribution boundary preserved. Artifact identity updates are
  exact and limited to the Card 1 surface change. Schema `$id` strip is a
  registry/hygiene accommodation, not a soft open of the contract.

### 5. Safety evidence

- **Result:** READY
- **Evidence:**
  - `python3 tools/envelope_scan.py --range 357140e..7383729` → exit 0, no
    violations.
  - New identifiers use `demo.source-context.*` / existing synthetic field
    keys (`w2-box1`, `div1b-qualified`).
  - `DataSafety.test_fixture_and_implementation_are_synthetic_and_locator_free`
    passes. Diff review shows no absolute paths, personal documents, or
    real-data artifacts.
- **Finding:** Unit remains synthetic and locator-free within the Builder
  range.

## Verdict

**READY**, with **measurement 3 (live surface) NOT-CONFIRMED** on this host
because Chromium and the surface vendored tree are absent. State, charter
scope, boundary, artifact identity, and data-safety measurements have direct
rerun evidence. The unit answers Card 1’s map questions without expanding into
Card 2 or weakening the contribution boundary.

### Owner-facing disposition (smallest)

1. Accept Card 1 as READY for Track 1 map scope, **or**
2. If live keyboard proof is required before acceptance, re-run measurement 3
   on a host with Chromium + vendored surface tree (or supply that
   environment) and treat only that measurement as still open.

No repair of the Builder unit is recommended from this review’s confirmed
measurements. Phase-state pointer is intentionally **not** moved (Foreman
owns that).

## Commands rerun

```sh
git rev-parse HEAD
# 7a578489dd51a88366d8c79ede9b86c6644f48d4

git rev-parse 7383729^
# 357140efaae46c58b92879c22706090fd3a60745

python3 -m unittest tests.test_entry_loop_t1
# Ran 50 tests ... OK (skipped=7)

python3 tools/envelope_scan.py --range 357140e..7383729
# exit 0
```
