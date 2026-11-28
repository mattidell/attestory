<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "sale-question-names",
  "status": "Open 2026-11-27. P0 chartered.",
  "retrospective": null,
  "scope": [
    "when a return has more than one sale with no Form 1099-B (Form 8949 boxes C and F) and the saved page asks a per-sale question, each question names the sale by what the filer recorded (description, dates or label), so the filer can tell which sale it asks about",
    "every recorded return keeps its numbers, dispositions and block codes"
  ],
  "non_goals": [
    "no kernel change; no edit to any published file",
    "no change to when a sale question is asked or to its answer target",
    "no answer control on the saved page (questions stay display-only)",
    "no change to the Form 1099-B statement labels ADR 0089 fixed"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/adr/0089-statement-question-labels.md",
      "docs/phases/engine-breadth/milestones/sale-question-names.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/adr/0089-statement-question-labels.md",
      "docs/phases/engine-breadth/milestones/sale-question-names.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/sale-question-names.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-11-27-statement-label-payer.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Each Sale Question Names Its Sale (2025)

Milestone key: sale-question-names.
Branch: milestone/sale-question-names-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-27.
Starting point: main at `0172559ab` (core v109, registry v107, release v107).
Expected target: a projection change under an amendment to ADR 0089 (or a
new ADR if P0 shows the shape differs), which the owner must accept before
Track 1.

## What we are trying to accomplish

ADR 0089 and its two amendments make each per-statement question name its
statement, and its payer when labels repeat. Sales with no Form 1099-B
(Form 8949 boxes C and F, core v80 onward) have no statement, and the
roadmap parks:

- "Questions about a sale with no Form 1099-B do not name the sale
  (ADR 0089, Parked)."

## Stages

1. **P0 (design, no build).** On synthetic `demo.*` returns with two and
   three no-1099-B sales, inventory every per-sale question the walk
   reaches and what the page shows for each today, on core v109. Find what
   the filer records that could name a sale (description, acquired and
   sold dates, a label, the sale entity) and whether the projection can
   reach it from the findings the blocked row already read. Say what the
   page shows when that name is missing or repeats. Run the inventory over
   every recorded list. Prove the route on a scratch build with a
   full-surface replay: no number, disposition or code change, only names
   added. The replay must assert each expected name, in order, and the
   count of lists that change, with committed controls that fail when a
   name is removed, swapped or added where it must not be, and a control
   for every path by which the replay can accept a list. List each input
   the walk trusts and the test that removes or corrupts it, including on
   an older and a successor core. Resolve every baseline from history that
   survives curation, without requiring `origin/main`. Draft the amendment
   and stop for the owner.
2. **Track 1 (build)**, fresh review, repair, closeout, final review,
   merge.

## Decisions

- **Owner** — Accept or reject the amendment P0 drafts, before Track 1.
