<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "sale-reasons-plain",
  "status": "P0 chartered 2026-11-18.",
  "scope": [
    "the two shared sale blocked reasons a filer can see (the holding-period mismatch and the wash-sale reason naming floor_zero(basis - proceeds) and its block code) say in plain words what is wrong and what to check",
    "every recorded return keeps its numbers, dispositions, refusal codes, missing names and questions; only those sentences change"
  ],
  "non_goals": [
    "no engine, schema, projection, page or kernel change",
    "no change to which answer a path needs, a refusal code or a missing name",
    "page-owned wording (captions, badges, banners) stays with the blocked-sale-pages milestone, which owns the saved sale page",
    "undrawn rule descriptions and notes stay parked"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/sale-reasons-plain.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/sale-reasons-plain.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/sale-reasons-plain.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/sale-reasons-plain.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Sale Reasons Speak Plainly (2025)

Milestone key: sale-reasons-plain.
Branch: milestone/sale-reasons-plain-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-18.
Starting point: main at `f6a6e47e` (core v96, registry v94, release v94).
Expected target: core v97, registry v95, release v95.

## What we are trying to accomplish

Every Line Speaks Plainly (core v96) replaced engine words in the texts
a filer sees, but parked two shared sale reasons as content (its
Decision 13): "The holding period does not match this short-term or
long-term family." and a wash-sale reason that names
`floor_zero(basis - proceeds)` and its block code. A filer who reads
either learns that something failed, not what to check on their Form
1099-B or Form 8949. The useful outcome is that both say, in plain
words checked against the 2025 Form 8949 and Schedule D instructions,
what is wrong and what the filer can look at, on every state where a
page draws them, with the same numbers and blocks as today.

## Stages

1. **P0.** Census where each reason is drawn (all 775 recorded lists
   and synthetic cases), trace each to its content file and field,
   draft replacements, build a scratch core successor, and replay
   strictly with mutation controls. Precedent and tooling:
   plain-line-texts-evidence/ (census.py, p0c_compare.py,
   track1_replay.py, track0_validate.py).
2. **Track 1.** Publish the successors in core v97 (registry v95,
   release v95), tests, strict replay.
3. **Fresh review**, adversarial: build the states where each new
   sentence would be false (Track 0 of plain-line-texts found 22 such
   sentences). Repair, closeout.

No Track 0 stage of its own: two sentences, and the review carries the
adversarial check.

## Decisions

Pending P0.
