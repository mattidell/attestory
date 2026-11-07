<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f8949-boxes-cf",
  "status": "Open. P0 (law, state on core v79, design) first.",
  "scope": [
    "a return with a sale of securities the filer did not receive a Form 1099-B (or substitute statement) for computes Form 8949 box C (short-term) or F (long-term), Schedule D lines 3 and 10, Form 1040 line 7a and the tax, from proceeds and basis the filer supplies, with code W allowed as on boxes B and E",
    "every return core v79 computes computes the same on the successor, and earlier cores render byte-identically",
    "what stays outside the class is refused by an answer, never computed partially"
  ],
  "non_goals": [
    "no digital assets (Form 1099-DA, boxes G-L), no short sales, no other adjustment codes, no broker-basis corrections",
    "no other Schedule D sources (K-1, Forms 2439, 4684, 4797, 6252, 6781, 8824)",
    "no edit to packages/kernel/",
    "no edit to any published schema, adopted package or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/milestone-retrospectives/2026-11-06-noncovered-sales.md",
      "docs/phases/engine-breadth/milestones/f8949-boxes-cf.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/f8949-boxes-cf.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/f8949-boxes-cf.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/f8949-boxes-cf.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Sales Without a Form 1099-B (2025)

Milestone key: f8949-boxes-cf.
Branch: milestone/f8949-boxes-cf-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-06.
Starting point: `github/main` at `87b05daf` (PR #261 merged; core v79 is
the latest).

## What we are trying to accomplish

Core v79 computes sales reported on a Form 1099-B, whether or not the
broker reported basis (Form 8949 boxes A, B, D, E). A filer who sold
securities and received no Form 1099-B or substitute statement — a private
sale of stock, shares held directly with a transfer agent that issued no
statement — reports it on Form 8949 box C or F. Today the boundary answer
refuses that return. The useful outcome is that it computes.

## What we know

- **What exists on v79.** Noncovered families (boxes B and E) with one
  grouped closure question (`source-closure-mapping.v4`, ADR 0084), the
  stale-yes rule, code W on B and E, Schedule D lines 2 and 9, Form 8949
  attachment v3, Schedule D attachment v7, line 7a v6, the preferential
  base v7.
- **The boundary.** Boxes C and F are refused by the in-class boundary
  answer. The noncovered-sales retrospective names "expected attachment
  dispositions in every case" and "hand-computed review from the start" as
  lessons.
- **What we do not know.** What the 2025 Form 8949 and Schedule D
  instructions require for boxes C and F (proceeds and basis both from the
  filer; Schedule D lines 3 and 10); whether the v79 noncovered pattern
  carries over as content only, including whether one grouped question can
  cover both B/E and C/F or a second question is cleaner; what a v79
  return with a box C or F sale does today.

## Actions the team will take

1. **P0: law, state and design.** Law from the local instruction sources,
   with quotes. State on core v79 through `live_coordinate_run`. The
   smallest successor set, prototyped on scratch, with every case's
   attachment dispositions asserted and the gain, loss and wash cases
   computed by hand. Stop and report if an engine, schema or recording
   change is needed.
2. **Decide.** The class and the question shape (owner, if a schema, ADR
   or recording change is needed).
3. **Track 0 adversarial closure.** The six artifacts of
   `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate", with built
   evidence; no row passes beside a standing counterexample.
4. **Track 1: build.** Successors, core v80 and its registry and release,
   cases through the real coordinator and the page, v79 and earlier
   pinned, full suite.
5. **Close.** Fresh-reader review with hand-computed lines, exact-head CI,
   retrospective, roadmap, frontier row and parked list. Merge on green
   verify (owner standing approval, 2026-11-06).

## Cases that will shape the design

- One box F long-term sale at a gain; one box C short-term sale at a loss
  (line 21 limit); a box C sale with code W.
- A return with sales in boxes A, B and C together, one each term.
- A box C or F sale with proceeds or basis missing: blocks and asks.
- Every return core v79 computes: identical on the successor.

## Process

Dispatch is to Opus and Sonnet sub-agents (owner, 2026-11-06): Opus for
P0, Track 0 and the fresh review; Sonnet for content-only build units.
Each unit commits on this branch as it goes.

## P0 result

Pending.

## Decisions

Pending.

## Track 0 adversarial closure

Pending.

## Track 1 result

Pending.
