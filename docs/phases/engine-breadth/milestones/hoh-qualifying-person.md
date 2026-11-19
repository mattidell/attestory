<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "hoh-qualifying-person",
  "status": "P0 chartered 2026-11-19.",
  "scope": [
    "a filer who answers head of household or qualifying surviving spouse is not given a return that silently takes that status's larger standard deduction and brackets when the record or the filer's own answers show it does not apply: the engine asks what the status needs, or refuses honestly by an answer the filer can see",
    "every recorded return keeps its numbers unless P0 shows a recorded return was silently wrong"
  ],
  "non_goals": [
    "no new filing-status computation and no change to the tax tables or standard deduction amounts",
    "no engine, schema, projection, page or kernel change unless P0 shows content cannot do it, and then only after the foreman decides",
    "no change to how single, married filing jointly or married filing separately are answered"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/hoh-qualifying-person.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/hoh-qualifying-person.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/hoh-qualifying-person.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/hoh-qualifying-person.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Head of Household Needs a Qualifying Person (2025)

Milestone key: hoh-qualifying-person.
Branch: milestone/hoh-qualifying-person-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-19.
Starting point: main at `ac445a22` (core v97, registry v95, release v95).
Expected target: core v98, registry v96, release v96 if a content
change is needed; tests only if P0 finds the engine already honest.

## What we are trying to accomplish

The filing-status question
(`input-question.filing-status.v1`) asks only which of the five
statuses applies. The cf-loss-limit P0 observed that head of household
and qualifying surviving spouse are accepted with no qualifying person
recorded. Both statuses carry a larger standard deduction and wider
brackets than single, and both require a qualifying person (and for
head of household, paying more than half the cost of keeping up a
home). If a filer picks one of them without meeting it, the return is
silently too favourable. The useful outcome is that the engine asks
what the status needs, or refuses honestly, rather than trusting a
bare label, while a filer who does qualify keeps the same numbers.

## Stages

1. **P0.** Trace what the engine does today with each status and what it
   already records that bears on it (dependents, the EIC and child tax
   credit qualifying-child answers, the other-dependent rosters). Read
   the 2025 Form 1040 instructions and Publication 501 in the local
   sources for the tests. Name the smallest honest design and prototype
   it as a scratch successor with the full-surface replay
   (`tools/recorded_replay.py full`).
2. **Track 1.** Publish it (or pin tests if already honest).
3. **Fresh review**, repair, closeout.

## Decisions

1. No change to which answers single, married filing jointly or married
   filing separately need.
