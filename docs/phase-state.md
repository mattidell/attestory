<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "document-oriented-entry",
  "active_plan": "docs/phases/legible-entry/milestones/document-oriented-entry.md",
  "milestone_state": "track-1",
  "status": "**LEGIBLE ENTRY / DOCUMENT-ORIENTED ENTRY — TRACK 1 REVIEW CHARTERED on `milestone/document-oriented-entry` 2026-08-03.** Card 1's source-context map build is committed; an author-independent review now measures its synthetic state, live surface, accessibility, manifest, and data-safety evidence.",
  "current_role": "Reviewer (Document-Oriented Entry Card 1)",
  "current_prompt": "docs/reviews/charter-2026-08-03-document-oriented-entry-card1-review.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Detailed history, review records, and architectural decisions live in
Git, `docs/reviews/`, and `docs/adr/`.

<!-- brief high level plain language overview of the state of the milestone, exclude result and finding specifics -->
## High Level Milestone Briefing

The entry surface can accept and correct synthetic W-2 and 1099-DIV facts,
run the return, and see the full record explained rather than flattened into
status rows. Every evaluation line can expand into a walkable explanation
built entirely from data the presentation model already computed, and the
explanation trail does not collapse as a reader navigates deeper.

The Workspace Prototype added a separate landing surface for orientation:
fact families, entered versus missing facts, current state, and attention
reasons are sourced from the existing model. Selecting a record item opens
the existing entry or explanation surface, and the field-keyed UI now holds
up when a second fact family is present.

The next milestone asks whether the workspace should organize entry around a
named source context. Usually that context is a document. When it is not, the
surface must name the applicable question, decision, or taxpayer context.
Opening a context should present its related fields together.

## Operational State: Legible Entry

* **Active Milestone:** Document-Oriented Entry, Track 1 under independent
  review on `milestone/document-oriented-entry` 2026-08-03.
* **Product change so far:** Card 1 adds a synthetic source-context map for
  W-2, 1099-DIV, and one question context; review has not yet measured the
  result.
* **Plan:** `docs/phases/legible-entry/milestones/document-oriented-entry.md`.
* **Carried forward:** correction still resets scroll position, silently
  relocating the reader away from open explanation panels. The workspace
  prototype did not change that behavior.
* **Next:** run the independent review described in
  `docs/reviews/charter-2026-08-03-document-oriented-entry-card1-review.md`.
* **Branch line:** UI work continues on `main-ui`.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
