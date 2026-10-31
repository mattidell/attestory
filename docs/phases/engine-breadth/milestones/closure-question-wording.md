<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "closure-question-wording",
  "status": "Closed on P0. A closure block shows a generic text and a family id; no family declares its closure question. The design (a source-closure-mapping.v3 with closure_question, 50 mapping successors, admission edits including the live coordinator, and a projector reason) is an open owner-held question.",
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
      "docs/milestone-retrospectives/2026-10-31-closure-question-wording.md",
      "docs/phases/engine-breadth/milestones/closure-question-wording.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-10-31-closure-question-wording.md"
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

P0 is in [trace and design](closure-question-wording-evidence/p0-trace-and-design.md),
with the probe and a wording survey beside it. Two stop conditions were met.

- **Today.** A section that blocks `SOURCE_SET_UNCLOSED` is saved with no
  reasons. The page shows the field's generic text, "Missing dependency
  code(s): SOURCE_SET_UNCLOSED" and "Remedy: contribute the missing
  dependency". When a subtotal is the root, as for an unconfirmed Form
  1099-INT box 1 family, no page line is the root, and 28 page lines block
  with no pointer to the question.
- **Wording.** None of the 50 closures in core v66 declares a question.
  Every closure fact type has a title, but 49 of them use internal terms
  ("membership horizon", ADR numbers). 38 family titles are plain noun
  phrases. Content has to come first (stop 1).
- **Design.** A `closure_question` string on a successor schema
  `source-closure-mapping.v3` (a mapping version is referenced by no
  workspace record), with 50 mapping successors. The projector would walk
  each blocked line's missing chain to its `SOURCE_SET_UNCLOSED` roots and
  attach the question as an existing `{sentence}` reason; the saved model
  and page already accept that shape, so no presentation-model successor is
  needed. Admitting a v3 mapping needs edits in `package_validation.py`,
  `authorization_closure.py`, `packages/tax/loader.py` and the live
  coordinator (`live.py` filters on exactly v2 and would drop v3 silently),
  which is stop 2.

## Decision

Foreman, 2026-10-31: closed on P0. The design needs a schema successor, a
coordinator admission change and 50 questions written in plain words. Those
go to the owner as one question rather than being built under this
milestone's ceiling.

## Outcome

No product change. The evidence records what a reader sees today and a
costed design for naming the closure question.
