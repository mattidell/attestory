<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "eic-child-answers",
  "status": "P0 chartered 2026-11-19.",
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

## Decisions

1. A question for a child names that child (or is shown in that child's
   roster entry), so a filer with two children knows which one is
   missing the answer.
