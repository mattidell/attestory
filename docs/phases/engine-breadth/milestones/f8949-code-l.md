<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f8949-code-l",
  "status": "Open. P0 chartered.",
  "scope": [
    "a sale at a loss on a Form 1099-B statement whose box 7 is checked is reported on Form 8949 with code L and the adjustment the 2025 instructions require, instead of refusing Schedule D line 16",
    "no loss from a box 7 statement reaches Schedule D unless the instructions allow it, and no other code or box changes",
    "every return core v85 computes correctly computes the same on the successor, and earlier cores render byte-identically"
  ],
  "non_goals": [
    "no other Form 8949 code, no box 13 bartering, no other Form 1099-B box",
    "no edit to packages/kernel/",
    "no edit to any published schema, adopted package or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/milestone-retrospectives/2026-11-10-f1099b-box7-loss.md",
      "docs/milestone-retrospectives/2026-11-10-f1099b-box4-only.md",
      "docs/phases/engine-breadth/milestones/f8949-code-l.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/f8949-code-l.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/f8949-code-l.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/f8949-code-l.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Form 8949 Code L for a Box 7 Loss (2025)

Milestone key: f8949-code-l.
Branch: milestone/f8949-code-l-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-10.
Starting point: `github/main` at `6e3bae8c` (PR #268, core v85).

## What we are trying to accomplish

Core v84 stopped refusing a checked Form 1099-B box 7 on gains, but a sale
at a loss on a checked statement still refuses Schedule D line 16 (the
f1099b-box7-loss milestone, Decision 1). The 2025 Form 8949 instructions
give a code for a nondeductible loss. The useful outcome is a core v86
that reports that sale as the instructions require and computes the
return, so the last box 7 refusal retires.

## What we know

- Core v84 derives a per-sale box 7 verdict in each of the eight sale
  families and a loss check per family; one loss on a checked statement
  blocks line 16 with no question.
- Codes B and W already route a sale to Form 8949 with a column (g)
  adjustment (f8949-code-b, the wash-sale milestones). Other codes are
  refused by answer.
- **What we do not know.**
  - What the 2025 Form 1099-B, Form 8949 and Schedule D instructions
    require for a box 7 loss: whether code L applies, whether the whole
    loss or only part is disallowed, and whether a filer may establish a
    different basis that allows it.
  - Whether a code L row needs a filer answer the engine does not ask
    today (for example, an allowed portion), or whether the adjustment
    follows from recorded amounts alone.
  - How code L combines with code W or code B on one sale.

## Actions the team will take

0. **Opening fix.** `tests/test_integration_checkpoint.py` t1 trips the
   3.0 s fast-lane budget on every PR's `quick` job. P0 measures why and
   makes it fast or an honest integration test, without raising the
   budget.
1. **P0: measure and design.** Quote the 2025 instructions. Table every
   rule that reads the box 7 verdicts and checks on core v85 and every
   Form 8949 code path. Probe v85 through `live_coordinate_run`. Compute
   by hand. Prototype a content-only scratch core v86. Stop and report if
   the fix needs an engine, schema or recording change.
2. **Decide.** The code L row, its adjustment, and what stays refused.
3. **Track 0 adversarial closure.** The six artifacts over the fix.
4. **Track 1: build.** Core v86 and its registry and release, with live
   and package tests.
5. **Close.** Fresh-reader review, repair, exact-head CI, retrospective,
   roadmap. Merge on green verify (owner standing approval, 2026-11-07).

## Cases that will shape the design

- Box 7 "yes", one covered short-term loss; one long-term loss.
- A box 7 loss beside a gain on the same statement.
- A box 7 loss with a code W wash amount; with a code B basis correction.
- A box 7 loss on a noncovered (box B/E) sale.
- Box 7 "no" beside a loss (unchanged).
- A loss changed to a gain; a sale removed; box 7 superseded.
- Every return core v85 computes: identical on v86.

## Process

Dispatch is through the grok CLI (owner, 2026-11-09). Each unit commits on
this branch as it goes. Track 0 hand values come from the instructions,
never from what a prototype publishes. P0 records the sentence the
presentation actually shows on each blocked row, and walks every
late-member path against any question wording.

## P0 result

Stopped. A box 7 loss is wholly disallowed. Example 2 reports it on Form 8949
with code L, column (g) the whole loss as a positive number, and column (h)
zero. Core v85 still posts the loss and blocks Schedule D line 16, with no
code L row. A content-only successor cannot emit that row: Form 8949 rows are
recorded family members, and the published attachment schemas cannot filter
them or add code L. The smallest change is a recording-surface change that
records the disallowed sale the way a code B sale is recorded, then a
successor package. Evidence: `f8949-code-l-evidence/p0.md`. No scratch core
v86 was generated. The recorded-return rerun was not run.
