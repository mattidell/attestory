<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "line16-next-step",
  "status": "Open 2026-11-26. P0 chartered.",
  "retrospective": null,
  "scope": [
    "on a return where Schedule D is required, no sale is recorded and the Exception 1 answers are right, the saved page tells the filer the next step (record the sale, or that the return needs work the engine does not support)",
    "where the page asks an Exception 1 question, the filer can see the answer they gave",
    "every recorded return keeps its numbers, dispositions and block codes"
  ],
  "non_goals": [
    "no kernel change; no edit to any published file",
    "no new answer control or question entry (line6b-reason Decision 8)",
    "no change to when Schedule D is required or to the Exception 1 rules"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/line16-names.md",
      "docs/phases/engine-breadth/milestones/line16-next-step.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/line16-next-step.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/line16-next-step.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-11-17-line16-names.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# A Required Schedule D With No Sale Says What To Do Next (2025)

Milestone key: line16-next-step.
Branch: milestone/line16-next-step-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-26.
Starting point: main at `b9d529f7` (core v108, registry v106, release v106).
Expected target: content (core v109) or a projection change; a proposed
ADR if it needs a contract the owner must accept.

## What we are trying to accomplish

line16-names parked L16-R2. On a return where Schedule D is required and
no sale is recorded, line 16 and the lines that explain through it name
the four sale questions and the four Exception 1 questions. When the
Exception 1 answers the filer gave are right (so Exception 1 really does
not apply), no answer on the page unblocks the line: the filer must
record the sale, or the return needs work the engine does not support.
The page names the criteria but does not say that, and it does not show
the answer the filer gave to each Exception 1 question, so the filer
cannot tell whether to change an answer or do something else.

## Stages

1. **P0 (design, no build).** On synthetic `demo.*` returns on core v108
   (start from the line16-names and preferential-base-reason probes),
   show what the saved page says today for: a required Schedule D with no
   sale and each way Exception 1 fails; the personal-loss Form 8949 case
   (`exception1_personal_loss_8949`); and controls where Exception 1
   holds or a sale is recorded. For each, list the page text, the
   questions named and whether the page shows the filer's current answer.
   Find where the line's explanation and remedy text come from (content
   citizen, projection or page) and design the smallest change that (a)
   adds a true next step for the state where the answers are right and
   (b) shows each Exception 1 question's current answer where the page
   asks it. Check every sentence against the 2025 Schedule D and Form
   8949 instructions. Prove on a scratch build with a full-surface replay
   (no number, disposition or block-code change). If the design needs a
   schema or a contract no accepted ADR covers, draft a proposed ADR as
   evidence (do not file it) and stop for the owner; otherwise write the
   Track 1 scope into the plan.
2. **Track 1 (build)**, fresh review, repair, closeout, final review,
   merge.
