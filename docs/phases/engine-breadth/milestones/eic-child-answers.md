<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "eic-child-answers",
  "status": "Repair chartered 2026-11-20; ADR 0087 awaits owner acceptance.",
  "scope": [
    "when a child counted for the earned income credit is missing an answer the credit needs (age, residency or another per-child test), the saved page asks that question for that child instead of blocking the credit and refund lines with no sentence",
    "every recorded return keeps its numbers"
  ],
  "non_goals": [
    "no change to which answers a path needs, or to the credit amounts",
    "no kernel change; an engine, schema or projection change only if P0 shows content cannot do it, and then only after the foreman decides (a new ADR waits for the owner)",
    "no page design change beyond showing a question that already exists"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/eic-child-answers.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/eic-child-answers.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/eic-child-answers.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/eic-child-answers.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# A Counted Child's Missing Credit Answer Is Asked (2025)

Milestone key: eic-child-answers.
Branch: milestone/eic-child-answers-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-19.
Starting point: main at `97507165` (core v100, registry v98, release v98).
Expected target: core v101, registry v99, release v99 if content can do
it; otherwise a P0 decision for the foreman.

## What we are trying to accomplish

The eic-answer-questions P0 found that when a child counted for the
earned income credit has no age or residency answer, nine page lines
(Form 1040 lines 27a to 37 and Worksheet A lines 2, 5 and 6) block with
no sentence. `rule.eic-child.age-met` publishes nothing for that child,
`rule.eic-child.counts` blocks naming `eic.child.age-met`, and
`rule.eic-qualifying-child-count` blocks `DEPENDENCY_INVALID` naming a
roster member key. The page's question walk stops at a root that is
neither a closure family nor a fact type with a question. Filers with
children are common, so this dead end matters more than its size.

The child tax credit and other-dependent rosters may have the same gap.

## Stages

1. **P0.** Trace the walk from each blocked line to its roots for each
   per-child answer. Find whether content can reach a question:
   ADR-0086 declared `missing` names on a block expression, an input
   question for the per-child fact, or a closure mapping question, as
   other rosters use. Check the child tax credit and other-dependent
   rosters for the same gap. If content cannot do it, name the smallest
   projection or schema change and whether it needs an ADR, and stop.
2. **Track 1.** Publish it.
3. **Fresh review**, repair, closeout.

## P0 result

P0 is complete in `eic-child-answers-evidence/p0.md`. It stopped at scope
item 4: content cannot meet Decision 1. On core v100, a missing per-member
answer is never asked on any of the four rosters. That covers the earned
income child tests, the tie-breaker answers, the child tax credit tests, the
other-dependent child's TIN and the seven relative answers. Each leaves 9 to
18 page lines blocked with no sentence. The walk stops where each roster's
count rule blocks `DEPENDENCY_INVALID` naming the member's subject key
(`evaluator.py:283-285`; `presentation_projection.py:609-669`). An input
question per member fact and the existing closure questions are not reached.
ADR 0086 `missing` names on a guarded count rule (scratch v101 `g`) reach a
question for the earned income and child tax credit tests. But that question
cannot name the child. It leaves the tie-breaker and other-dependent answers
silent, and it changes the explanation of every return with a rostered child:
new count inputs, so downstream structure changes, and extra citations where
a child fails a test early. The recorded replay passes 773 of 775. The two
failures are the only recorded lists with a child, and they differ in that
structure only. No number changes. The smallest change that meets Decision 1
is in the projection's question walk. It would follow a blocked member key to
the member's own rows, resolve each missing test to its answer's input
question, and label the reason with the member's recorded name. It adds no
published schema version, but in the builder's reading it needs an ADR.
Decisions for the foreman are in p0.md, section 7.

## Decisions

1. A question for a child names that child (or is shown in that child's
   roster entry), so a filer with two children knows which one is
   missing the answer.
2. The projection change (P0 recommendation 1), recorded as ADR 0087,
   which is **proposed** and awaits the owner. Track 1 may build it, but
   the PR does not go ready until the owner accepts the ADR.
3. A new optional reason field, `memberLabel`, holds the member's
   recorded label (P0 recommendation 2). It shows an existing recorded
   label beside an existing kind of question, so it is within the "no
   page design change" non-goal.
4. All four rosters (earned income credit, child tax credit,
   other-dependent child, relative) are in scope, since they share the fix
   (P0 recommendation 3).
5. Every missing member answer is asked at once (P0 recommendation 4).
6. Per-member questions are written from the 2025 Form 1040 instructions
   (line 27a, Schedule 8812, and the dependents and other-dependents
   sections), each with its source lines quoted. A question must not
   change which answer a path needs.
7. Repair before merge (review ECA-R1, R2, R4, R5, R6, R8). The residency,
   lived-with-you and relative support questions state the kidnapped-child
   rule; the age question's student definition states the training,
   correspondence and internet-only exclusions; the military note says
   extended duty counts even if fewer than 90 days are served. The reason
   field is `memberLabel` (camelCase, like `statementLabel`). A test pins
   that a member with two labels stays silent. ADR 0087 says the walk
   follows any per-subject member, which is what the code does. v101 is not
   on main, so its files are regenerated in place.
8. Parked: questions that tell the filer to answer no where the fact is
   narrower than the instructions (the sheltered-workshop and multiple
   support agreement cases compute a smaller credit instead of blocking,
   ECA-R3); two members with the same recorded label share one reason
   (ECA-R7); question polarity is recorded only in the evidence design and
   tests, not in published content (ECA-R9).
