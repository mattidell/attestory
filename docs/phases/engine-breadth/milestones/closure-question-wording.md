<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "closure-question-wording",
  "status": "Open. P0 traces what a reader is told when a line blocks because a family is not confirmed complete, and designs naming the question that unblocks it.",
  "scope": [
    "when a line blocks because a source family is not confirmed complete, a saved presentation names the closure question the filer must answer, in declared wording",
    "the wording comes from content (the closure fact type or family), never composed in code",
    "every other presentation, explanation and earlier saved file is unchanged"
  ],
  "non_goals": [
    "no change to any computed value, disposition or block code",
    "no general rewrite of blocked texts beyond the closure case",
    "no edit to any published schema or citizen; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/closure-question-wording.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/closure-question-wording.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/closure-question-wording.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/closure-question-wording.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# A Blocked Line Names Its Question (2025)

Milestone key: closure-question-wording.
Branch: milestone/closure-question-wording-2025, stacked on
`milestone/itemization-cents-2025` (`fe6487fa`, PR #238).
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-31.

## What we are trying to accomplish

The last four milestones made many lines block `SOURCE_SET_UNCLOSED` until
a family is confirmed complete: line 25b, line 2b, the Schedule 1, B and D
subtotals, the Form W-2G lines. That is honest. A reader of the saved
return, though, sees a family id such as `tax.us.2025.f1099g.b4`, or a
field's generic "blocked because an input it needs is missing". The filer is
never told the one thing that would unblock the line: answer "Have you
recorded every Form 1099-G box 4 amount?"

`_selection_blocked_reasons` in `packages/derivation/presentation_projection.py`
already gives per-statement reasons for selection lines, using declared
wording only. A closure block has no equivalent.

The useful outcome: when a line blocks because a family is unconfirmed, its
saved presentation names that family's closure question, in content's own
words, and the reader can act on it.

## Actions the team will take

1. **P0 — trace and design.** What a saved presentation, the CLI and the
   explanation show today for a `SOURCE_SET_UNCLOSED` block, on a real run.
   Where declared wording for each closure question lives (closure fact
   type, family, closure mapping), and whether every family in the latest
   core has it. The design: where the projector gets it, the reason shape,
   whether `presentation-model` needs a successor schema, how the browser
   page shows it, and what happens for a block that passes through several
   lines (show it at the root, or at each line). Stop if wording is missing
   for most families (then content first), or if the change needs a kernel
   or runner change.
2. **Decide.**
3. **Track 1.** Projector, schema successor if needed, page, tests.
4. **Close.** Fresh-reader review, curated history, retrospective, roadmap.

## Process

Dispatch to Sonnet 5.5 Agent sub-agents. This touches
`packages/derivation/`, so the full suite runs before handoff. Stop means
stop.

## P0 result

Pending.
