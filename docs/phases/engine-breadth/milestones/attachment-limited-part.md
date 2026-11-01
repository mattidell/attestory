<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "attachment-limited-part",
  "status": "Open. P0 designed attachment-rule.v12 (applies_when, tie_out.limited_to); Track 1 builds it and the Schedule A successor on core v70.",
  "scope": [
    "an attachment-rule schema successor that lets a part apply only when a named line is nonzero, and tie out against a limited line rather than the raw row sum",
    "the runner's attachment code interprets it; every existing attachment behaves as before",
    "the Schedule A attachment itemizes line 16 for a gambling-loss itemizer, and a losses-only itemizer's attachment no longer blocks on line 8a"
  ],
  "non_goals": [
    "no change to how any existing attachment is required, tied out or published",
    "no change to any computed value",
    "no edit to any published schema or citizen; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/gambling-losses.md",
      "docs/phases/engine-breadth/milestones/attachment-limited-part.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/gambling-losses.md",
      "docs/phases/engine-breadth/milestones/attachment-limited-part.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/attachment-limited-part.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/attachment-limited-part.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Schedule A Shows Gambling Losses (2025)

Milestone key: attachment-limited-part.
Branch: milestone/attachment-limited-part-2025, stacked on
`milestone/closure-questions-2025` (PR #247), so a successor package is core
v70, registry v68, release v68.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-31.

## What we are trying to accomplish

The gambling-losses milestone (#245) left the Schedule A attachment short:
for an itemizer with gambling losses it lists line 8a while line 12e counts
line 16 too, and a losses-only itemizer (no Form 1098) gets correct figures
but an attachment blocked on line 8a. Attachment parts always run and tie out
exactly to raw row sums (`attachment-rule.v4` to `v11`, `attempt_attachment`
in `packages/derivation/runner.py`), so a part cannot be conditional or tie
to a line limited to winnings. The owner approved an attachment-rule schema
successor and the runner change (2026-10-31).

The useful outcome: a filed Schedule A that matches the itemized total.

## Actions the team will take

1. **P0 — design.** Read the attachment-rule schemas and `attempt_attachment`.
   Design the smallest successor shape: a part (or row set) that applies
   only when a named line is nonzero, and a tie-out that compares against a
   declared line (so a part can show the raw loss rows and the limited line
   16). Say how a part that does not apply is shown (absent, or present with
   no rows) and how the explanation reads. Name the schema version, the
   runner change, and the Schedule A successor; the v69 → v70 change set; and
   prove on paper that every existing attachment is unaffected. Hand-computed
   cases from #245's tests. No code changes. Stop if the design needs a kernel
   change or changes any existing attachment.
2. **Decide.**
3. **Track 1.** Schema, runner, Schedule A successor, core v70, tests.
4. **Close.** Fresh-reader review, curated history, retrospective, roadmap.

## Process

Dispatch to Sonnet 5.5 Agent sub-agents. Track 1 touches
`packages/derivation/`, so the full suite runs before handoff. Stop means
stop.

## P0 result

P0 is in [design](attachment-limited-part-evidence/p0-design.md), with a probe
of today's behaviour.

- **Today.** `attempt_attachment` evaluates every part. Presence and
  scheduling require every part's symbols, the tie-out is an exact raw sum,
  and the projector raises on an unpublished part line. The two #245 gaps
  reproduce on v69.
- **Design: `attachment-rule.v12`,** v4 plus two optional fields.
  `applies_when` per part (`always`, `line_nonzero`, `family_nonempty`): a
  part that does not apply is omitted and its symbols are not required; the
  condition is read from the part's own line or family, so an omission
  cannot hide a nonzero figure, and an omitted part with a nonzero line is a
  tie-out violation. `tie_out.limited_to {symbol, label}`: the rows stay as
  reported and the check is `line == min(part sum, limit)`, with the limit
  and the amount not counted recorded. Every runner branch is guarded by the
  schema name; the validator, marshalling, live coordinator, closure
  authorization and projector admit v12. No new block code, no kernel
  change, no presentation-model change.
- **Schedule A on core v70.** `attachment.schedule-a` v4 on v12: the line 8a
  part applies when the Form 1098 family is nonempty; a new line 16 part
  applies when line 16 is nonzero, with the losses as rows and limited to
  the winnings. Every other attachment keeps its schema version and file.

## Decisions

Foreman, 2026-10-31:

1. **Build `attachment-rule.v12` as designed** (owner-approved schema and
   runner change).
2. **Losses with no W-2G leave the line 16 part out.** With no winnings
   nothing is deductible and line 16 is 0; the figures already show it.
3. **The limited part pins the winnings subtotal,** so its source appears in
   the explanation.

## Tracks

1. **Track 1 — v12 and Schedule A.** The schema, the runner and admission
   changes, the projector sentence, `attachment.schedule-a` v4, core v70 /
   registry v68 / release v68, and tests: P0's cases, and per-attachment
   payload equality between v69 and v70 for every attachment except Schedule A.
