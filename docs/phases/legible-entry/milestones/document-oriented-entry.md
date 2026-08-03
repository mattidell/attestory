<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "document-oriented-entry",
  "milestone_state": "track-1",
  "status": "Track 1 chartered on main-ui 2026-08-02. Card 1 tests the smallest source-context map over the existing synthetic fields.",
  "scope": [
    "organize workspace input by named source contexts rather than an undifferentiated fact list",
    "use a document as the normal source context and name a question, decision, or taxpayer context when no document applies",
    "open a source context to present its related fields together",
    "preserve the existing contribution-only entry path, explanation walk, and return-to-workspace context"
  ],
  "non_goals": [
    "no real personal documents or real-data entry",
    "no new tax logic or direct fact writes",
    "no published document citizen or persistence contract",
    "no universal document taxonomy or filing workflow",
    "no dashboard expansion beyond source-context orientation and entry"
  ],
  "deep_reads": {
    "implementation": [
      "docs/phases/legible-entry/milestones/document-oriented-entry.md",
      "docs/phases/legible-entry/milestones/workspace-prototype.md",
      "packages/derivation/entry_loop.py",
      "packages/derivation/presentation_projection.py",
      "packages/sample_data/entry_loop_t1/surface/content/app/src/WorkspacePage.svelte",
      "packages/sample_data/entry_loop_t1/surface/content/app/src/EntryPage.svelte",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/phases/legible-entry/milestones/document-oriented-entry.md",
      "docs/milestone-retrospectives/2026-08-02-workspace-prototype.md",
      "AGENTS.md#Data Safety Rules"
    ],
    "new_milestone": [
      "PROJECT_PLANNING.md#Required Milestone Plan Contents",
      "docs/phases/legible-entry/legible-entry-roadmap.md",
      "docs/milestone-retrospectives/2026-08-02-workspace-prototype.md"
    ],
    "merge_or_records": [
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol"
    ]
  }
}
-->
# Document-Oriented Entry

Status: **Track 1 chartered on `main-ui`, 2026-08-02.** The planning boundary
is committed directly; Card 1 is ready for owner launch and implementation has
not started.

Card 1 is chartered for owner launch in
`docs/reviews/charter-2026-08-02-document-oriented-entry-card1.md`.

## Objective

Prove a more natural starting point for entry: a person begins from the
source context that caused the work, usually a document. Opening that context
presents its related fields together. When the source is not a document, the
surface names the applicable question, decision, or taxpayer context so the
person knows what the entry is about.

The milestone is successful if the synthetic workspace can move from its
source-context map into a coherent grouped entry view, submit through the
existing contribution path, and return to the same context without losing the
explanation or entry state already opened.

## Current state

The Workspace Prototype provides a separate landing page over the synthetic
entry loop. It reads field-keyed state, shows fact families and attention
reasons, and links to the existing entry and explanation pages. The synthetic
fixture has two enterable facts: Form W-2 Box 1 and Form 1099-DIV Box 1b.
Each field already carries a source-document label, a destination, and the
state needed to show missing or answered input.

Entry uses the existing contribution-only admission path. The explanation
walk already preserves open panels across the workspace round trip, and
fragments provide the current deep-link shape without changing the entry
request boundary. No general source-context grouping contract exists yet.

## Scope

- Add a prototype source-context view model over the existing field contract;
  a document is the normal context, with explicit labels for non-document
  contexts.
- Organize the workspace by those contexts and show the related fields under
  the selected context together.
- Let a selected context open the existing entry controls, including missing
  and correction states, without duplicating contribution or explanation
  logic.
- Exercise at least one document context and one named non-document context
  using synthetic data or metadata already present in the fixture. If the
  existing fixture cannot honestly supply the latter without new tax meaning,
  record that boundary as a finding rather than inventing a context.
- Preserve return navigation, deep links, accessible names, and the existing
  field-keyed behavior when more than one fact family is present.

## Non-goals

- No personal documents, personal values, real workspace locations, or
  owner-attested real-data run.
- No direct fact writes, new act kinds, or changes to the contribution
  admission boundary.
- No new tax calculations, tax rules, or inferred zero values.
- No published schema for a document or source-context citizen. A view-model
  shape may be explored locally and discarded.
- No attempt to enumerate every document type or every possible question,
  decision, or taxpayer context.
- No filing, transmission, upload, OCR, document storage, or broad dashboard
  work.

## Contracts

- Existing field declarations and `state.field_contract` remain the source
  for field identity, source document, destination, and accepted input shape.
- A source context has a stable synthetic key, a named kind (`document`,
  `question`, `decision`, or `taxpayer`), a human-readable label, and an
  ordered set of related field keys. This is a prototype view model, not a
  published citizen.
- Opening a context selects its related fields as a group; it must not make a
  second copy of the field declaration or derive tax meaning from labels.
- Submission continues through the existing `act-contribution.v1` admission
  path. The surface does not write facts directly.
- Explanations and correction actions continue to use the existing
  presentation data and entry targets. Context navigation may add a fragment
  or other browser-local state only if the existing request boundary remains
  unchanged.
- Context labels must be honest: a document is named as a document, and a
  non-document entry names the applicable question, decision, or taxpayer
  context rather than presenting a blank or generic document label.

## Fixtures

- Extend the committed synthetic entry-loop fixture only as needed to expose
  the two existing document contexts and one non-document source context.
- Cover missing, partially answered, and fully answered context states.
- Cover opening each context, entering or correcting its related fields, and
  returning to the workspace with the selected context and open explanation
  state intact.
- Cover both fact entry orders and keyboard traversal across context controls
  and grouped fields.
- Keep all identifiers obviously synthetic (`demo.*` / `demo-*`) and keep
  generated or ad hoc output under ignored paths.

## Verification

- Focused Python tests: `python3 -m unittest tests.test_entry_loop_t1`.
- Run the fixture's browser journeys against a running local server, including
  keyboard operability, focus indication, and both entry orders.
- Verify the rendered context labels and related-field membership directly in
  the running synthetic surface; do not treat static markup as proof of the
  navigation behavior.
- Before the planning or implementation PR is opened, run
  `git diff --check`, `python3 tools/governance_lint.py`, and
  `python3 tools/envelope_scan.py --range <base>..HEAD`. CI's `verify` check
  remains the merge gate.

## Data safety

Only committed synthetic fixtures and demo identifiers may be used. Personal
documents, values, dispositions, workspace locations, screenshots, and
generated artifacts derived from personal data remain outside the repository,
branches, reviews, and output. The prototype does not access or request real
documents.

## Exit criteria

The milestone closes when the owner has a working synthetic prototype that:

1. starts from a source-context map rather than an ungrouped fact list;
2. names document and non-document contexts honestly;
3. opens one context with its related fields together;
4. enters and corrects through the existing contribution path;
5. returns to the same context without losing the relevant entry or
   explanation state; and
6. leaves a clear finding about whether this shape is worth carrying forward.

No maturity cell moves and no real-data claim is made at close.

## Tracks / experiment cards

This is owner-directed prototype work, so these are bounded experiment cards,
not a fixed implementation sequence or a promise that every card will run.

### Card 1 — source-context map

Show the existing W-2 and 1099-DIV source documents as separate contexts,
with their related field keys and attention state. Establish the smallest
view-model shape that can support a non-document label without inventing a new
citizen.

### Card 2 — grouped context entry

Open one document context into a grouped entry view. Enter and correct its
fields, preserve the existing explanation links, and return to the same
context. Use the browser journeys to expose navigation and accessibility
defects.

### Card 3 — non-document context

Test the explicit question, decision, or taxpayer-context label against a
synthetic case the existing model can support honestly. Decide whether the
context abstraction clarifies entry or whether the document-only shape is the
better next boundary.

## How we will work

The milestone stays owner-directed. Each card is small, synthetic, and
exercised before the next decision. A card may be discarded or replaced when
its result changes the question. No builder or reviewer charter is prepared
until a card produces a question that benefits from role separation.
