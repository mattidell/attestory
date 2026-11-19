<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "hoh-eic",
  "status": "P0 chartered 2026-11-19.",
  "scope": [
    "an unmarried head of household with no qualifying child is figured the earned income credit as the 2025 instructions allow, instead of being given $0 because of the filing status",
    "a married head of household (considered unmarried) without a qualifying child still gets no credit, and every other filer keeps their numbers"
  ],
  "non_goals": [
    "no change to the earned income credit tables, the qualifying-child tests or the credit for other filing statuses",
    "no engine, schema, projection, page or kernel change unless P0 shows content cannot do it, and then only after the foreman decides",
    "no change to the head of household questions published in core v98"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/hoh-eic.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/hoh-eic.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/hoh-eic.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/hoh-eic.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# The Earned Income Credit for a Head of Household (2025)

Milestone key: hoh-eic.
Branch: milestone/hoh-eic-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-19.
Starting point: main at `d3a65aff` (core v98, registry v96, release v96).
Expected target: core v99, registry v97, release v97.

## What we are trying to accomplish

The hoh-qualifying-person P0 found that `rule.eic-status-class` puts
every head of household in class 0, with married filing separately, so
a head of household with no qualifying child gets no earned income
credit. The 2025 Form 1040 line 27a instructions stop only a *married*
taxpayer filing as head of household or separately (Step 4, question 1).
An unmarried head of household whose qualifying person is, for example,
a dependent parent can be entitled to the credit with no qualifying
child. The engine gives that filer $0, which errs against the filer
(hoh/relative/low: 0 where single gets 542 on v97).

Core v98 now asks every head of household whether the status's tests
are met, and that question separates "unmarried on December 31" from
"married but considered unmarried" only in its wording, not in the
recorded answer. The engine may need a further answer to tell them
apart.

## Stages

1. **P0.** Trace the credit for each filing status and qualifying-child
   case on v98. Read the 2025 line 27a instructions and Publication 596
   (if in the local sources) for how a married head of household is
   treated, with and without a qualifying child, including the
   separated-spouse rule. Name the smallest honest design and prototype
   it as a scratch successor with the full-surface replay.
2. **Track 1.** Publish it.
3. **Fresh review**, repair, closeout.

## Decisions

1. No change to the head of household or surviving spouse questions
   published in core v98; a new fact, if needed, is a new question.
