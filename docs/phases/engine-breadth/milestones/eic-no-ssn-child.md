<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "eic-no-ssn-child",
  "status": "Open 2026-11-23. Track 1 published core v102; closeout next.",
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
Starting point: main at `e3a4397f` (core v101, registry v99, release v99); rebased onto `394db518` after #300.
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

Evidence: `docs/phases/engine-breadth/milestones/eic-no-ssn-child-evidence/p0.md`.

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

## Decisions

1. Publish the content route (P0 recommendation 1): `rule.eic-child.qualifies`
   and `rule.eic-qualifying-child-present`, and successors of status class,
   early stop, questions required and the Step 3/Step 4 answer rules, as
   core v102, registry v100, release v100. No engine change, no new ADR.
2. The scope follows the sources for every filing status, not only the
   married head of household and married filing separately filer (P0
   decision 2): a filer whose qualifying children all lack a valid SSN is a
   filer with a qualifying child (Publication 596 chapter 2), skips Step 4,
   and takes the self-only (`other-0` / `joint-0`) column. Track 1 first
   searches the 2025 Form 1040 instructions (Steps 1-6, Schedule EIC
   instructions) and Publication 596 (chapters 2 and 3, and every example
   that names a child without an SSN) for any sentence that sends such a
   filer to Step 4 or chapter 3. If one exists, quote it, keep Step 4 for
   the statuses it covers, and say so in track1.md; otherwise widen as
   above. Either way, every traced case has a hand credit.
3. The unmarried head of household whose only qualifying child lacks a
   valid SSN is handled like a head of household with a counted child
   today (P0 decision 3): asked the separated-spouse question, whose
   published "yes" already includes "not married". No new question.
4. Track 1 keeps the P0's strict full-surface replay with declared
   expectations, and a test pins every changed or new rule through the
   live coordinator, including a case that fails if the SSN test is
   dropped from `rule.eic-child.counts` (the amount column) or added to
   `rule.eic-child.qualifies`.
5. Review ENS-R1 is accepted as recorded: an unmarried head of household
   whose only qualifying child lacks a valid SSN is asked the
   separated-spouse question, as a head of household with a counted child
   already is on v101 (Decision 3); the question's "yes" includes "not
   married", so a truthful answer gets the self-only credit. Asking it
   only of a married filer is parked for both cases.

## Track 1 result

Evidence: `docs/phases/engine-breadth/milestones/eic-no-ssn-child-evidence/track1.md`.

No sentence in the 2025 Form 1040 instructions or Publication 596 sends a filer whose qualifying children all lack a valid SSN to Step 4 or chapter 3. Schedule EIC says that filer claims the self-only credit and attaches Schedule EIC. The published route is the widened one: every filing status, Step 4 skipped when a qualifying child is present, self-only column when none of those children has a valid SSN.

Core v102, registry v100, and release v100 are published. The loader entries carry v101. The 775 recorded lists replay with declared structural changes and no recorded number changed. Ninety-five live coordinator cases match the 2025 table. No engine change and no new ADR.
