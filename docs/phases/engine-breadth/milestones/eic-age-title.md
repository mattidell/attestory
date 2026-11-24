<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "eic-age-title",
  "status": "Open 2026-11-24. P0 next.",
  "retrospective": null,
  "scope": [
    "the eic.age-25-under-65 fact's title says what its question asks: the birth-date range, and age at death for a filer or spouse who died in 2025",
    "no saved answer loses its meaning or its pin, and every recorded return keeps its numbers"
  ],
  "non_goals": [
    "no change to the question, the rule that reads the fact, or the credit",
    "no kernel, engine, schema, projection or page change",
    "if a title change would unpin saved answers or cannot be published as a successor, stop: the title is parked rather than forced"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/eic-age-title.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/eic-age-title.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/eic-age-title.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/eic-age-title.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# The Age Fact's Title Says What Its Question Asks (2025)

Milestone key: eic-age-title.
Branch: milestone/eic-age-title-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-24.
Starting point: main at `6dcec44f` (core v103, registry v101, release v101).
hoh-no-worksheet-ceilings (#305, core v104) is in flight; a publication
here takes the next free version after it.

## What we are trying to accomplish

eic-answer-questions review EAQ-R7 noted that the `eic.age-25-under-65`
fact type's title states only the birth-date range, while its input
question also counts a filer (or spouse) who died in 2025 by age at death.
The title is published bytes in `eic-questions.bundle.json`, so it can only
change through a successor, and the sale-reasons-plain P0 showed that a
successor of a pinned citizen can unpin every saved record that used it.

## Stages

1. **P0.** Where the title is shown (page, explanations, question groups)
   and whether a filer sees it. How saved answers pin the fact type and the
   bundle (by version), and what a bundle or fact-type successor would do
   to a saved return that answered on the current version (re-answer,
   block, keep). The 2025 Form 1040 instructions' wording on age at death
   for the earned income credit (quote it). A scratch successor and a
   full-surface replay against v103. If a title change would unpin or
   block saved answers, or the title is never shown, stop and recommend
   parking it with the reason.
2. **Decisions** by the foreman.
3. **Track 1** if P0 shows a safe route.
4. **Fresh review**, repair, closeout.
