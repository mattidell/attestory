# Attachment Disposition Visibility — Decision Unit Charter

Audience: Builder (paper spike + ADR draft, not implementation)

Status: **chartered for owner launch**

## Why this exists

Track 3 landed (`ef921d4`) with a named charter-stop finding, exactly per
its own stop condition: `_resolve_attachment` in
`packages/derivation/presentation_projection.py` returns `None` for both
the `inapplicable` (not-required) and `blocked` (required-and-incomplete)
attachment dispositions — only the `published` (required-and-complete)
state ever produces a `citationGroups` entry. `citation-walk.v1.html`
(both the product page and frozen harness copy) only ever iterates
`MODEL.citationGroups`, so a blocked or not-required attachment is
completely invisible: no signal it exists, is required, or is blocked, and
no missing/violated reason shown. This is a pre-existing gap, not
introduced by Schedule D — Schedule B's attachment simply never exercised
the blocked/not-required paths in a way that surfaced it before now.

This violates ADR-0046 Requirement 2's honest-blocking guarantee
("a blocked line shows what fact is missing") for the one citizen whose
entire purpose is to be the honest, walkable completeness account
(ADR-0036 Decision 1). Ordinary numeric/categorical fields already honor
this: `_resolve_field_row` produces `{"disposition": "blocked",
"activeCodes": codes, "act": None}` for a blocked field, and
`citation-walk.v1.html` renders that state. The attachment citizen has no
equivalent shape today.

## Gate 1 — eligibility score

- Future blast radius: **2** (every attachment-bearing schedule — Schedule
  B today, Schedule D now, any future schedule instantiating ADR-0036 —
  inherits invisible blocked/not-required states; this is the second time
  in this milestone a presentation/completeness gap in ADR-0036's
  generalized shape has surfaced against Schedule D specifically because it
  is the first schedule to actually exercise paths Schedule B never hit).
- Migration cost: **1** (additive: extend `presentation-model.v1`'s
  `citationGroups` entry shape with a disposition/blocked-code field
  mirroring the existing field-row shape; no existing entry's meaning
  changes).
- Residual paper uncertainty: **1** (the shape to mirror already exists
  and is proven — `_resolve_field_row`'s blocked shape — the main paper
  question is whether an attachment's blocked/not-required entry belongs
  in `citationGroups` alongside published attachments, or a new top-level
  model key, and what the rendering path needs to distinguish "not
  required" from "blocked").
- Inability to test cheaply: **1** (payload/rendering shape, testable via
  the existing presentation harness and unit tests without new
  infrastructure).

**Total 5 — paper-spike-plus-ADR-draft rung**, matching ADR-0055's
precedent on this same milestone. The known-shape precedent
(`_resolve_field_row`) makes this lower-uncertainty than ADR-0055 was, not
higher — no full prototype round is warranted absent a paper surprise.

## Scope

1. State the exact gap as a producer → authority → consumer → failure map:
   `_resolve_attachment`'s three-disposition branch, the `presentation-model.v1`
   schema's `citationGroups` shape, `citation-walk.v1.html`'s rendering
   loop, and the precise failure (blocked/not-required attachments produce
   no visible signal at all — not even "redacted," genuinely absent).
2. Two positive instances (published attachment renders correctly today —
   unaffected baseline) and two negatives (not-required attachment renders
   nothing; required-and-incomplete attachment, including an
   ADR-0055 `COMPLETENESS_VALUE_VIOLATION` case, renders nothing).
3. Evaluate the shape: extend the existing `citationGroups` entry
   (disposition-tagged, mirroring `_resolve_field_row`'s
   `{"disposition": "blocked", "activeCodes": ..., "act": None}`) versus a
   new top-level model key for attachment status distinct from published
   citation groups. State which better preserves ADR-0046's existing
   guarantees (blast containment, no rejected-value leakage, accessible
   rendering) with the least new surface.
4. Draft a proposed successor ADR (do not edit ADR-0036 or ADR-0046 in
   place) capturing the chosen extension: the `presentation-model.v1`
   (or successor) schema widening, the `_resolve_attachment` change to
   produce a value for all three dispositions, and the
   `citation-walk.v1.html` rendering addition (accessible markup for a
   blocked/not-required attachment banner, consistent with the existing
   accessibility bar this milestone's Track 3 already met for numeric
   fields).

## Non-goals

No code, no schema, no content changes, no test/golden changes, no closeout
work. Paper-and-ADR-draft only. No re-litigation of ADR-0036 or ADR-0046's
existing decisions outside this specific gap.

## Stop conditions

Stop and report if: the fix cannot be expressed as an additive model/schema
widening (would require editing ADR-0036 or ADR-0046 in place); the
rendering addition cannot meet the existing accessibility bar without a
new, unprecedented DOM mechanism; or the gap turns out to already have a
committed resolution elsewhere in the codebase.

## Deliverable

One proposed ADR draft (numbered successor, e.g. `docs/adr/0056-*.md`,
status **proposed**, not accepted) plus its paper evidence, for owner
review and ratification. Implementation is a separate, subsequent unit
once ratified — matching the ADR-0055 → implementation-charter precedent
already used twice on this milestone.

## Full reads before acting

`docs/adr/0036-schedule-attachment-ontology.md`,
`docs/adr/0046-presentation-surface-contract.md`,
`docs/adr/0055-attachment-completeness-violation-semantics.md` (the
nearest-precedent decision unit on this milestone),
`packages/derivation/presentation_projection.py` in full (especially
`_resolve_attachment`, `_resolve_field_row`, and the model assembly
around line 389), `packages/presentation/pages/citation-walk.v1.html`,
the Track 3 commit (`ef921d4`) message and diff in full,
`PROJECT_PLANNING.md` Gates 1-3, `docs/roles/builder.md`.
