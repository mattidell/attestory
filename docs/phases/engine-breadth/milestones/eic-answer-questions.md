<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "eic-answer-questions",
  "status": "Repair chartered 2026-11-19.",
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
ten credit answer rules on v99, six have an input question; the age,
main-home, not-claimable-as-dependent and spouse-SSN answers do not
(P0 census; the plan first said eleven and five). The useful outcome is that every
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
2. P0's design: four input questions (age, main home, not claimable as a
   dependent, spouse SSN), exactly as `eic-answer-questions-evidence/p0.md`
   words them, and no rule change. Core v100, registry v98, release v98.
   The foreman checked the age question's birth-date bounds and death
   rules against Publication 596 Rule 11 and the other three against
   line 27a Step 1 question 2 and Step 4 questions 3 and 6.
3. The dependent question follows Step 4 question 6 ("Can you be
   claimed..."), so a yes records the fact's no, as the existing
   qualifying-child-of-another question does.
4. Parked: deriving the not-claimable answer from the line 12a "someone
   can claim you" answer (a rule cannot prefer an explicit answer and
   fall back to another), and the counted-child age and residency answers,
   which block nine page lines with no sentence because the projection
   cannot reach a question there (a projection change).
5. Repair before merge (review EAQ-R1, R2, R5, R6). The age question
   states Publication 596's exception for a death in 2025 before age 25;
   the main-home question's military sentence covers a spouse and defines
   extended active duty from the instructions; the spouse SSN question
   says an ITIN is a no. A test pins that a yes to the dependent question
   records the not-claimable fact as no. v100 is not on main, so its files
   are regenerated in place.
6. Recorded at closeout, not repaired: the spouse SSN question also
   appears on the child tax credit lines, which read the same answer
   (EAQ-R3, helps the filer, no number changes); the per-child tie-breaker
   answers (`dtb.child.*`) have no question (EAQ-R4, parked); the age
   fact's title states only the birth-date range (EAQ-R7, a bundle
   change).

## P0 result

Evidence: `eic-answer-questions-evidence/p0.md`. Core v99 has ten credit
answer rules. `rule.eic-answer.no-qualifying-child` is not a v99 member.
Four answers have no question: age, main home, not claimable as a
dependent, and spouse SSN. Missing any one of them where it is required
(single, qualifying surviving spouse, unmarried head of household and joint
filers, reproduced live) blocks lines 27a-37, and the saved page shows no
sentence. Nothing on the record proves any of them soundly and simply.
(The line 12a dependent answer matches the not-claimable answer in meaning,
per Pub. 596 Rule 12, but content cannot prefer an explicit answer.) The
design is content only: four `input-question` members naming the existing
fact types, written from line 27a Steps 1 and 4 with the source lines
quoted. No rule change, so no path needs a different answer. Scratch core
v100 on v99 validates. On it each blocked line shows the missing
question(s). The strict full-surface replay passes 775/775 recorded lists
and 32/32 probe lists (answers removed, nothing pre-filled), with 0
unexpected differences. Unused expectations on the recorded lists: the
question sentences (no recorded list leaves one of these answers missing
where required). Recommendation: publish as core v100, registry v98, release
v98. Out of reach of content: a counted child's missing roster answer (age,
residency) also blocks silently, and needs a projection change. Reported for
the foreman's decision, not built (p0.md, Decisions 1-5).
