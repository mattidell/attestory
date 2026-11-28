<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "reason-question-links",
  "status": "Open 2026-11-27. P0 chartered.",
  "retrospective": null,
  "scope": [
    "every reason on the saved page that asks the filer for an answer links to its question, so a reader (or probe) following the page's question links finds every question the page asks",
    "every recorded return keeps its numbers, dispositions and block codes"
  ],
  "non_goals": [
    "no kernel change; no edit to any published file",
    "no change to when a question is asked or to its wording",
    "no answer control on the saved page (questions stay display-only)",
    "no change to the ADR 0089 statement and sale labels"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/adr/0089-statement-question-labels.md",
      "docs/phases/engine-breadth/milestones/question-filter.md",
      "docs/phases/engine-breadth/milestones/reason-question-links.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/adr/0089-statement-question-labels.md",
      "docs/phases/engine-breadth/milestones/reason-question-links.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/reason-question-links.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-11-27-sale-question-names.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Every Asking Reason Links Its Question (2025)

Milestone key: reason-question-links.
Branch: milestone/reason-question-links-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-27.
Starting point: main at `5993ce933` (core v109, registry v107, release v107).
Expected target: a projection change under a new ADR or an amendment to
ADR 0089 (P0 says which), which the owner must accept before Track 1.

## What we are trying to accomplish

The question-filter milestone found that some reasons ask for an answer
but carry no question link (QF-R1, QF-R2), and the roadmap parks:

- "Some reasons ask for an answer but carry no question link, so a probe
  that reads links does not count them: a roster member's question
  (ADR 0087), a question whose answer target is not unique, and a
  question about a fact not yet recorded. The per-statement Form 1099-B
  box 4 prompt is one: on v89 it is the only reason on some line 25b and
  25d pages, with no link."

A filer reading the page sees a question, but the page does not say which
answer it wants, so neither the filer nor a probe can tell that question
apart from plain text.

## Stages

1. **P0 (design, no build).** On core v109, inventory every reason the
   saved page draws that asks for an answer and has no question link,
   across every recorded list and the synthetic `demo.*` lists, grouped
   by cause (roster member, non-unique target, unrecorded fact, the
   per-statement box 4 prompt, any other). For each cause, say what the
   question asks and what a link would point to, and whether the
   projection can name that target from the findings the row already
   read. Say what the page shows when no single target exists. Prove the
   route on a scratch build with a full-surface replay: no number,
   disposition or code change, only links added. The replay must assert
   each added link, in order, and the count of lists that change, with
   committed controls that fail when a link is removed, retargeted or
   added where it must not be, a pinned baseline outcome census and error
   set, and a control for every path by which the replay can accept a
   list. List each input the walk trusts and the test that removes or
   corrupts it, including on an older and a successor core, and name one
   shared rule for any text or identity comparison used by more than one
   layer. Resolve every baseline from history that survives curation,
   without requiring `origin/main`. Draft the ADR text and stop for the
   owner.
2. **Track 1 (build)**, fresh review, repair, closeout, final review,
   merge.
