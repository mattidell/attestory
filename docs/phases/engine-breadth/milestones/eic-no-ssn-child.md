<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "eic-no-ssn-child",
  "status": "Open 2026-11-23. P0 evidence recorded; foreman decisions next.",
  "retrospective": null,
  "scope": [
    "a married filer (head of household or married filing separately) whose qualifying child lacks a valid SSN is routed by the earned income credit as the 2025 Form 1040 instructions and Publication 596 say, instead of getting $0 because the child is not counted",
    "every other recorded return keeps its numbers"
  ],
  "non_goals": [
    "no change to the credit tables, the other credits, or which answers an unrelated path needs",
    "no kernel change; an engine, schema or projection change only if P0 shows content cannot do it, and then only after the foreman decides (a new ADR waits for the owner)",
    "no page change"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/eic-no-ssn-child.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/eic-no-ssn-child.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/eic-no-ssn-child.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/eic-no-ssn-child.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# A Child Without a Valid SSN Routes the Earned Income Credit Correctly (2025)

Milestone key: eic-no-ssn-child.
Branch: milestone/eic-no-ssn-child-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-23.
Starting point: main at `e3a4397f` (core v101, registry v99, release v99).
Expected target: core v102, registry v100, release v100 if content can do
it; otherwise a P0 decision for the foreman.

## What we are trying to accomplish

hoh-eic Decision 5 parked a gap. The earned income credit counts a
qualifying child only with a valid SSN. A married filer who files as head
of household, or married filing separately, and whose only qualifying
child lacks a valid SSN, is therefore treated as having no qualifying
child: the separated-spouse test (Step 4) is never reached, and the
credit is $0 or the no-child amount. The 2025 instructions decide such a
filer's eligibility with the child still counted for some tests (for
example "a qualifying child who lived with you for more than half the
year" for the separated-spouse rule, and the credit for a filer whose
child has no SSN). Which tests count a child without an SSN, and what the
filer may then claim, must come from the sources, not from this plan.

## Stages

1. **P0.** From the 2025 Form 1040 instructions (line 27a, Steps 1-6 and
   the worksheets) and Publication 596, state exactly how a qualifying
   child without a valid SSN counts: for the separated-spouse test, for
   the "qualifying child" class, and for the no-child credit, quoting each
   source line. Trace core v101 on synthetic demo.* returns (married head
   of household and married filing separately; one child with and one
   without a valid SSN; separated or not; lived-with-you more or less than
   half the year): what each answer path computes today and what the
   sources say it should. Find whether content can route it (successor
   rules, a per-child fact, an input question); if not, name the smallest
   engine change and stop. Full-surface replay of a scratch successor
   against v101 with expected changes declared.
2. **Decisions** by the foreman.
3. **Track 1.** Publish it.
4. **Fresh review**, repair, closeout.

## P0 result

Evidence: `docs/phases/engine-breadth/milestones/eic-no-ssn-child-evidence/p0.md`,
recorded at source head `b51994331d46b3f4c8e2843144c45e127131210d`.

A qualifying child for the earned income credit is relationship, age,
residency, and joint return. A valid SSN is not one of those tests. It
decides the amount. The 2025 instructions put the separated-spouse test in
Step 3, questions 3 through 5, and then skip Step 4. Step 4 is the
no-qualifying-child path, and its first question stops a married head of
household or a married filing separately return. Publication 596 says the
same, and a qualifying child without a valid SSN can still support a
self-only credit. The filer does not take the credit for a filer without a
qualifying child.

Published v101 counts only a child with a valid SSN, so the eight separated
married returns whose qualifying child lacks one get $0. The hand credit
from `parameter.eic-table-2025` v2 at wages 7,000 is the `other-0` amount,
537. A qualifying child with a valid SSN stays at 2,389. The scratch
successor does this in content: `rule.eic-child.qualifies` v1, a present
count, and successors of status class, early stop, questions required,
separated-spouse, not-married, age, and main home. All 50 synthetic
`live_coordinate_run` cases match the hand credit. The 775 recorded lists
pass with declared structural changes and no recorded number changed. No
engine change and no new ADR.

The foreman decides whether to publish core v102, registry v100, release
v100; whether single, qualifying surviving spouse, and married filing
jointly stays on Step 4 when the only qualifying child lacks a valid SSN;
and whether an unmarried head of household in that position should leave
Step 4 for the separated-spouse question.
