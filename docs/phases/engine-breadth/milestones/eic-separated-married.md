<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "eic-separated-married",
  "status": "Open 2026-11-23. P0 stopped on a new question; P0b next.",
  "retrospective": null,
  "scope": [
    "the earned income credit asks the separated-spouse question (Step 3 questions 4 and 5 of the 2025 Form 1040 instructions) only of a married filer whose status is head of household or married filing separately, as the instructions do",
    "an unmarried head of household with a qualifying child is not asked it and keeps the credit the sources give",
    "every other recorded return keeps its numbers"
  ],
  "non_goals": [
    "no change to the credit tables, the other credits, or which answers an unrelated path needs",
    "no kernel or engine change; a new question only if P0 shows the record cannot tell whether a head of household was married, and then from the 2025 instructions",
    "no page change"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/eic-separated-married.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/eic-separated-married.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/eic-separated-married.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/eic-separated-married.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# The Separated-Spouse Question Is Asked Only of a Married Filer (2025)

Milestone key: eic-separated-married.
Branch: milestone/eic-separated-married-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-23.
Starting point: the eic-no-ssn-child branch (core v102, registry v100,
release v100; PR #301), stacked; rebased onto main once #301 merges.
Expected target: core v103, registry v101, release v101 if content can do
it; otherwise a P0 decision for the foreman.

## What we are trying to accomplish

eic-no-ssn-child parked ENS-R1. On core v101 and v102 a head of household
with a qualifying child is asked the earned income credit's
separated-spouse question, whose "yes" includes "not married at the end of
2025". The 2025 instructions ask Step 3 questions 4 and 5 only of "a
married taxpayer whose filing status is married filing separately or head
of household" (Step 3 question 3). An unmarried head of household who
answers the question as worded "no" (they were not separated; they were
never married) gets $0. The record may already say whether the filer was
married (for example the head-of-household or not-married answers); if it
does, the question can be skipped for an unmarried filer.

## Stages

1. **P0.** Quote Step 3 questions 3 to 5 and the special rule for
   separated spouses (2025 Form 1040 instructions, line 27a) and the
   matching Publication 596 text. Trace published core v102 on synthetic
   demo.* returns: head of household married or not married, with a
   qualifying child with and without a valid SSN, separated or not; and
   married filing separately. Name which recorded answer, if any, already
   says the head of household was married at the end of 2025, and where
   it comes from. Find a content route that asks questions 4 and 5 only of
   a married filer; if the record cannot tell, name the smallest question
   from the instructions and stop. Full-surface replay of a scratch
   successor against v102 with expected changes declared.
2. **Decisions** by the foreman.
3. **Track 1.** Publish it.
4. **Fresh review**, repair, closeout.

## P0 result

Evidence: `docs/phases/engine-breadth/milestones/eic-separated-married-evidence/p0.md`.

Published core v102 cannot tell whether a head of household with a qualifying
child was married at the end of 2025. `eic.not-married` is asked only when no
qualifying child is present, and its words do not match Step 3 question 3.
`hoh.tests-met` yes covers an unmarried filer and a married filer who lived
apart for the last six months. The separated-spouse question is asked of
every head of household with a qualifying child. Twenty-one synthetic
demo.* returns on the live coordinator match the 2025 table except the two
unmarried head-of-household returns that answer that question no: line 27a
is $0 where the instructions give 2,389 (valid SSN) or 537 (no valid SSN)
at wages of 7,000. The other four unmarried returns with a qualifying child
keep those table amounts only because the published yes includes "not
married," and they are still asked.

No scratch successor was built and the 775 recorded lists were not replayed.
The smallest new question is Step 3 question 3, asked of a head of household
who has a qualifying child. Married filing separately is already a married
taxpayer by filing status. A yes continues to questions 4 and 5. A no skips
them and keeps the table credit. No engine change and no new ADR.

## Decisions

1. Accept the P0 stop: no fact on a v102 return says whether a head of
   household with a qualifying child was married at the end of 2025
   (`eic.not-married` is withheld when a qualifying child is present and
   counts a decree as "yes"; `hoh.tests-met` "yes" covers both). The route
   is a new input question taken from Step 3 question 3 of the 2025
   instructions, asked only of a head of household with a qualifying
   child, with its own fact type. Married filing separately needs no new
   fact. No engine change and no ADR.
2. A return must not newly block on the new question when it already
   carries an answer that decides the credit the same way: a recorded
   separated-spouse "yes" passes on v102 and must still pass. P0b designs
   the successors so the separated-spouse question is asked only after a
   "married" answer, and so that a recorded separated-spouse "yes" without
   the new answer still passes if the rule language can express it
   (selection on which answers are present). If it cannot, P0b measures
   how many of the 775 recorded lists, and which kinds of filer, would
   newly block, and stops for a foreman decision.
3. P0b reports each new or successor rule file's size against the
   5,000-byte cap, and runs the live size tests.
