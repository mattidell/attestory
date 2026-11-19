<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "eic-answer-questions",
  "status": "P0 chartered 2026-11-19.",
  "scope": [
    "every earned income credit answer the engine requires of a filer is either asked by a question the saved page shows, or derived from what the record already proves; no filer is blocked on the credit with no sentence",
    "every recorded return keeps its numbers"
  ],
  "non_goals": [
    "no change to which answers a path needs, or to the credit amounts",
    "no engine, schema, projection, page or kernel change unless P0 shows content cannot do it, and then only after the foreman decides",
    "no change to the questions published in core v98 or v99"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/eic-answer-questions.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/eic-answer-questions.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/eic-answer-questions.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/eic-answer-questions.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Every Earned Income Credit Answer Has a Question (2025)

Milestone key: eic-answer-questions.
Branch: milestone/eic-answer-questions-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-19.
Starting point: main at `8c08011b` (core v99, registry v97, release v97).
Expected target: core v100, registry v98, release v98.

## What we are trying to accomplish

The hoh-eic review (EIC-R1) found that the earned income credit's age
(`eic.age-25-under-65`) and main-home (`eic.main-home-in-us`) answers
have no input question. A filer who must give them and has not is
blocked on line 27a and the refund lines, and the saved page shows no
sentence. That has been true for single filers since before v98. Of the
eleven credit answer rules on v99, six have an input question; the age,
main-home, not-claimable-as-dependent, spouse-SSN and
no-qualifying-child answers may not. The useful outcome is that every
answer the credit requires is asked plainly or derived from the record,
with no change to any number.

## Stages

1. **P0.** Census every credit answer: which rule reads it, when it is
   required, whether it has a question, and whether the record (dates of
   birth, dependent status, SSN facts, the qualifying-child roster)
   already proves it. Reproduce the silent block. Name the smallest honest
   design and prototype it as a scratch successor with the full-surface
   replay.
2. **Track 1.** Publish it.
3. **Fresh review**, repair, closeout.

## Decisions

1. Questions are written from the 2025 Form 1040 line 27a instructions
   (Step 1, Step 4 and Worksheet steps) and checked against them by the
   foreman before Track 1 publishes them.
