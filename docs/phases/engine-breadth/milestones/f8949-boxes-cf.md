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

Recorded in
[p0-law-state-design.md](f8949-boxes-cf-evidence/p0-law-state-design.md),
with `cf_probe.py` / `cf-probe-output.json` (core v79) and
`cf_prototype.py` / `cf-prototype-output.json` / `cf-prototype-rules/`
(scratch core v80).

- **Law.** Box C and box F are short- and long-term sales with no Form
  1099-B or substitute statement. They feed Schedule D lines 3 and 10.
  Column (d) is net proceeds, column (e) is the filer's basis, and code W
  works as on B and E. The 2025 sources are local IRS PDFs in a scratch
  directory, not in the repository.
- **v79.** Recording the sale on box B or E with the v79 in-class answer
  yes gives the right dollars on the wrong line. The in-class "no" refuses
  it. Left unrecorded with every Form 8949 boundary answered "no", v79
  publishes the wage return: no answer refuses it, and v78 does the same.
  A box E sale missing its basis or proceeds amount computes silently.
- **Design.** A content-only successor of 48 member edits plus the two
  per-core loader entries.
  - A second grouped question: "Did you sell any stocks or other
    securities for which you did not receive a Form 1099-B or substitute
    statement?" It keeps every v79 answer's meaning.
  - A new in-class answer for boxes B, C, E and F, read through a guarded
    arm so v79 returns never need it.
  - Lines 3 and 10 carry three checks:
    1. each sale has its own proceeds and basis (`require_paired`);
    2. a "yes" is backed by a recorded sale;
    3. a Form 8949 "no" is admitted by some answer.

  The gain, loss, wash and mixed cases match the hand values.
- **v79 returns on v80.** Without the new answer, all 46 block. With a
  "no", 24 of the 28 v79 computes are identical. The other 4 (8949 "no",
  nothing admitted, nothing recorded) now block, including the pinned
  `boundary_no_without_member`.
- **No engine, schema, or recording change** is needed.
- **Owner questions:**
  1. Accept those 4 newly blocked returns.
  2. Decide whether lines 2 and 9 take the same missing-amount check.

## Decisions

Foreman, 2026-11-06, on P0 (owner direction: proceed on the recommended
choice; the owner adjusts after):

1. **The P0 design is adopted.** A second grouped question for sales with
   no Form 1099-B, a new in-class answer for boxes B, C, E and F read
   through a guarded arm, and the three checks on lines 3 and 10. The v79
   question and answers keep their meaning.
2. **The four newly blocked v79 returns are accepted.** Each is a Form
   8949 "no" that no answer admits, with nothing recorded. v79 publishes
   it silently, so blocking it is the fix. Track 1 changes the
   current-core expectation for `boundary_no_without_member`. The v79
   pin in `tests/test_noncovered_sales_v79.py` stays as it is, because it
   pins the published v79 package.
3. **Lines 2 and 9 take the same missing-amount check.** A box B or E
   sale missing its proceeds or basis amount blocks and asks for it,
   instead of computing a wrong line. It is the same defect as on lines 3
   and 10, and it is fixed in the same successor.
4. **Accepted limits.** These are parked in the roadmap at closeout, not
   fixed here:
   - A "yes" with nothing recorded behind it shows only the line's blocked
     text, with no question. Showing a question would need a rule-schema
     successor.
   - A sale entered both on a 1099-B family and as a no-statement sale is
     not caught.
   - The married-filing-separately $1,500 limit and the 2026 carryover are
     not exercised.

## Track 0 adversarial closure

Pending.

## Track 1 result

Pending.
