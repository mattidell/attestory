<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "same-label-members",
  "status": "Open 2026-11-25. P0 next.",
  "retrospective": null,
  "scope": [
    "when two roster members (children or relatives) have the same recorded label and each is missing an answer, the saved page asks the question once per member and the filer can tell them apart",
    "every recorded return keeps its numbers, dispositions and block codes"
  ],
  "non_goals": [
    "no kernel change; no edit to any published file",
    "no change to when a member question is asked or to its answer target",
    "ECA-R3 and ECA-R9 stay parked"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/adr/0087-question-walk-follows-roster-members.md",
      "docs/phases/engine-breadth/milestones/same-label-members.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/same-label-members.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/same-label-members.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-11-20-eic-child-answers.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Two Members With the Same Name Each Get Their Question (2025)

Milestone key: same-label-members.
Branch: milestone/same-label-members-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-25.
Starting point: main at `9f4b7116` (core v107).
Expected target: a projection change, or a proposed ADR if it needs a
contract the owner must accept.

## What we are trying to accomplish

ADR 0087 carries a roster member's recorded label on its question reason
(`memberLabel`). eic-child-answers parked ECA-R7: two members with the same
recorded label share one reason, so a filer with two children both entered
as "Sam" (or two relatives with an empty or repeated label) sees one
question where two answers are missing. The page should ask once per
member and let the filer tell them apart without inventing a name.

## Stages

1. **P0 (design, no build).** On synthetic `demo.*` returns, show the
   current behavior for two and three members sharing a label, a shared
   label where only one member is missing the answer, and members with
   distinct labels (control). Find where reasons are merged (sentence and
   label dedupe in `presentation_projection.py`) and design the smallest
   change that keeps one reason per member: for example keying by the
   member's fact id and adding an ordinal or another recorded attribute
   the filer entered (never an id). Check the page renders each reason and
   links its question group. Prove on a scratch build with a full-surface
   replay (no number, disposition or code change). If the design changes
   the `presentation-model` schema or what ADR 0087 decided, draft a
   proposed ADR and stop for the owner; otherwise write the Track 1 scope
   into the plan.
2. **Track 1 (build)**, fresh review, repair, closeout, final review,
   merge.

## Decisions

(None yet.)
