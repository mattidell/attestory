<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "code-w-gain-question",
  "status": "Open 2026-11-24. P0 next.",
  "retrospective": null,
  "scope": [
    "a Form 8949 row whose code W wash-sale adjustment (box 1g) sits on a gain or break-even sale, which blocks by ADR-0062 Decision 2, tells the filer what to answer or correct, not only why it blocks",
    "every recorded return keeps its numbers"
  ],
  "non_goals": [
    "no change to ADR-0062 or to when a code W row blocks",
    "no kernel change; an engine, schema or projection change only if P0 shows content cannot do it, and then only after the foreman decides (a new ADR waits for the owner)",
    "no rewording of the sale family meaning text that saved sale records pin (sale-reasons-plain)"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/code-w-gain-question.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/code-w-gain-question.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/code-w-gain-question.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/code-w-gain-question.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# A Blocked Code W Gain Asks the Filer Something (2025)

Milestone key: code-w-gain-question.
Branch: milestone/code-w-gain-question-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-24.
Starting point: main at `6dcec44f` (core v103, registry v101, release v101).
hoh-no-worksheet-ceilings (#305, core v104) is in flight; a publication
here takes the next free version after it.

## What we are trying to accomplish

gain-break-even found that a Form 8949 row with a code W adjustment on a
gain or break-even sale blocks (ADR-0062 Decision 2), and the saved page
shows only the reason; no question tells the filer what to answer or
correct. sale-reasons-plain found that the covered-W reason text itself is
pinned meaning text on sale families, so it cannot simply be reworded.

## Stages

1. **P0.** Trace published core v103 on synthetic demo.* sale returns
   (covered and noncovered, short and long term, code W on a gain, on a
   break-even and on a loss): what blocks, the root tuples, the page
   sentence and any question group. From the 2025 Form 8949 instructions
   (code W, box 1g) and ADR-0062, what the filer should be asked or told
   to correct. Find whether content can attach a question the page's
   question walk reaches (an input question for the fact the block reads,
   ADR 0086 declared missing names, a closure question) without touching
   pinned family meaning text. Scratch successor and full-surface replay
   against v103. If content cannot, name the smallest projection or
   schema change and whether it needs an ADR, and stop.
2. **Decisions** by the foreman.
3. **Track 1** if content can.
4. **Fresh review**, repair, closeout.
