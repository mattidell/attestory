<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "improvised-milestone",
  "status": "Closed by the owner 2026-07-31 before implementation began. No product behavior changed. The proposed unflattening prototype remains available for a later owner-directed milestone after main and main-ui begin from a clean shared base.",
  "retrospective": "docs/milestone-retrospectives/2026-07-31-improvised-milestone.md",
  "scope": [
    "make the entry surface a better place to understand and navigate the record",
    "begin with a small unflattening prototype using the existing synthetic W-2 entry loop",
    "reuse existing derivation and presentation lineage rather than derive the same meaning again",
    "adapt the work as the prototype reveals the next useful question"
  ],
  "non_goals": [
    "no fixed maturity claim",
    "no mandatory charter or predetermined track sequence",
    "no predetermined evaluation sheet or definition of done",
    "no real personal data unless the owner separately chooses a real-data exercise"
  ],
  "deep_reads": {
    "implementation": [
      "docs/phases/legible-entry/milestones/improvised-milestone.md",
      "packages/derivation/entry_loop.py",
      "packages/derivation/presentation_projection.py",
      "packages/sample_data/entry_loop_t1/surface/content/app/src/EntryPage.svelte",
      "AGENTS.md#Owner-directed mode",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/phases/legible-entry/milestones/improvised-milestone.md",
      "AGENTS.md#Owner-directed mode",
      "AGENTS.md#Data Safety Rules"
    ],
    "merge_or_records": [
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol"
    ]
  }
}
-->
# Improvised Milestone

Status: **closed without implementation, 2026-07-31.**

## Goal

Move the entry surface toward a walkable record: from anything shown, a person
should be able to understand what it is, where it came from, why it matters,
what changed, and what they can do next.

The existing W-2 loop is the starting point. It already accepts a contribution,
runs the return, and shows affected lines. It also receives a richer
presentation model and flattens most of that model into entry-specific status
rows. The first experiment is to stop throwing that meaning away.

## How we will work

This milestone uses owner-directed mode. It has no charters, fixed tracks,
up-front scoring sheet, or predetermined definition of done. Builders and
reviewers are optional tools, used when they help answer the question in
front of us.

We will keep a small working board, make one useful change at a time, and
revise direction from what the running surface teaches us. The owner decides
when the milestone has produced enough, which observations matter, and what
criteria should describe the result at close.

## Starting board

**Now**

- Prototype an unflattened explanation for Form 1040 line 1a in the synthetic
  W-2 entry loop.
- Reuse the existing presentation model and lineage. Add interaction state
  only where entry needs it; do not create a second tax explanation.

**Likely next**

- Let the person move from the changed line to the producing rule, accepted
  W-2 finding, evidence label, and correction action.
- Try a multi-step result after the direct line works, so the shape is not
  accidentally limited to one obvious connection.
- Decide whether the prototype reveals a useful reusable UI contract.

**Parked until they become useful**

- Revising the broader entry-usability criteria.
- Adding a second fact family.
- Exercising real entry.
- Repairing evaluator isolation before another independent evaluation.

## Boundaries

The work stays synthetic by default. It does not add tax logic, recalculate a
value in the UI, or invent explanation text that the record cannot support.
Existing data-safety and published-schema protections remain in force.

## Completion

There is no precommitted exit test. At a natural stopping point, the owner
will inspect what exists, decide what questions it answers, choose any final
criteria worth keeping, and either close, redirect, or continue the milestone.

## Close

The owner closed this milestone before implementation began so `main` and
`main-ui` can start their next, separate milestones from a clean shared base.
No product behavior changed. The unflattening prototype remains a candidate
for a later owner-directed milestone.
