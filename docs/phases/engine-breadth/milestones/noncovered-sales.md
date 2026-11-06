<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "noncovered-sales",
  "status": "Open. P0 done: a content successor (core v79) with no engine or schema change. Owner decided the class, the misroute fix and C3. Track 0 adversarial closure runs before Track 1.",
  "scope": [
    "a return with a Form 1099-B sale whose basis the broker did not report to the IRS (Form 8949 box B or E) computes Schedule D and Form 1040 line 7 from a basis the filer supplies",
    "every return core v78 computes computes the same on the successor, and earlier cores render byte-identically",
    "what stays outside the class is refused by an answer, never computed partially"
  ],
  "non_goals": [
    "no digital assets, no short sales, no other Schedule D sources (K-1, Forms 2439, 4684, 4797, 6252, 6781, 8824)",
    "no basis worksheet or lot-selection tool beyond the amount the filer supplies",
    "no recording surface or entry-loop change unless P0 shows the class cannot be answered without one, and then only after owner direction",
    "no edit to packages/kernel/",
    "no edit to any published schema, adopted package or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/noncovered-sales.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/noncovered-sales.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/noncovered-sales.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/noncovered-sales.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Sales Whose Basis Was Not Reported (2025)

Milestone key: noncovered-sales.
Branch: milestone/noncovered-sales-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-06.
Starting point: `github/main` at `e73d32cf` (PR #260 merged; core v78 is
the latest).

## What we are trying to accomplish

The last ten milestones made the existing return honest and legible: every
missing answer is asked, each statement is checked for its own withholding,
and every line says what it adds. None added a filer the engine could not
serve before. This one returns to breadth. A brokerage filer who sold
shares bought before the broker had to track basis, or shares transferred
in, gets a Form 1099-B with box 12 (basis reported to the IRS) unchecked,
often with box 5 (noncovered) checked and box 1e blank. That
sale goes on Form 8949 box B (short-term) or E (long-term), with the basis
the filer supplies. Today such a return is refused by the Schedule D
boundary answer. The useful outcome is that it computes.

## What we know

- **The boundary.** `schedule-d-boundary-form8949-w.bundle.json` asks
  whether the return has no adjustment codes other than W, no multi-code
  rows, and no noncovered or basis-not-reported sources (ADR-0061
  Decision 4). A "no" refuses the return.
- **What exists.** Form 8949 attachment v2, Schedule D lines 1a, 1b, 7,
  8a, 8b, 15, 16 and 21, covered short- and long-term families, wash-sale
  adjustments (code W) on Form 8949 boxes A and D.
- **The frontier row.** `coverage-frontier.md` marks noncovered and
  basis-not-reported Form 8949 transactions "unblocked — requires re-cut
  contract" against ADR-0066's validation substrate, with an open closure
  gate question (C3). ADRs 0067-0071 (acquisition field access, acquisition
  report identity, basis consequences) landed after that row was written
  and may already supply part of it.
- **What we do not know.** What a noncovered sale does on core v78 through
  the real coordinator; whether the existing families can carry a
  filer-supplied basis or a new family is needed; what the 2025 Form 8949
  and Schedule D instructions require for boxes B and E (and C and F, no
  Form 1099-B); whether one return may mix covered and noncovered sales;
  what question the filer answers for the basis.

## Actions the team will take

1. **P0: law, state and design.** From the local 2025 Form 8949 and
   Schedule D instruction sources, what boxes B and E require. On core v78
   through `live_coordinate_run`, what each case does today. What the
   acquisition ADRs and the ADR-0066 substrate already provide, and what
   the frontier's C3 question is now. The smallest successor set, with a
   scratch prototype. Stop and report if an engine, schema or recording
   change is needed.
2. **Decide.** The class, the questions, and any contract (owner, if a
   schema, ADR or recording change is needed).
3. **Track 0 adversarial closure.** The six artifacts of
   `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate", over the
   decided design, each with built evidence. No row may pass beside a
   standing counterexample (C3). A `FAIL` returns to design or the owner.
4. **Track 1: build.** Successors, core v79 and its registry and release,
   cases through the real coordinator and the page, v78 and earlier
   pinned, full suite.
5. **Close.** Fresh-reader review, exact-head CI, retrospective, roadmap,
   frontier row and parked list.

## Cases that will shape the design

- One noncovered long-term sale at a gain, basis supplied: Form 8949 box
  E, Schedule D line 9, line 15, line 16, Form 1040 line 7, and the
  preferential tax.
- One noncovered short-term sale at a loss: box B, Schedule D line 2, and
  the $3,000 limit on line 21.
- A return with both covered and noncovered sales, one each term.
- A noncovered sale with a wash-sale adjustment.
- A noncovered sale whose basis the filer has not supplied: blocks and
  asks.
- Every return core v78 computes: identical on the successor.

## Process

Dispatch is to grok CLI agents in this worktree (owner direction). P0 and
Track 1 are builder units; the close is a fresh-reader review. Each unit
commits on this branch as it goes. Stop means stop.

## P0 result

Recorded in
`docs/phases/engine-breadth/milestones/noncovered-sales-evidence/p0-law-state-design.md`.
Core v78 has no line 2 or line 9. A sale whose basis was not reported,
placed on a covered family, publishes on line 1a or 8a and is not
refused. Answering both Form 8949 boundaries no blocks Form 1040 line
7a and leaves Schedule D published. A missing basis is a schema
rejection or the covered-family question. The smallest successor is
content only: new families, lines 2 and 9, the line 7 and 15 sums, a
third preferential arm, Form 8949 boxes B and E, one boundary fact, and
a line 7a successor the scratch v79 package did not yet include. No
engine, schema, expression, or recording-surface change. C3 remains an
open owner question. The scratch loss and wash runs match Schedule D
and not line 7a until that successor is re-measured.

## Decisions

Owner, 2026-11-06, on P0:

1. **C3: no counterexample may stand beside a `PASS`.** A Track 0 closure
   row passes only when each counterexample its evidence records is fixed
   or refused by an answer, and the row says which. Written into
   `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate". This
   milestone runs that gate before Track 1.
2. **Fix the v78 misroute and partial Schedule D on v79.** A sale recorded
   on a covered family with `basis_reported_to_irs` no is refused (or
   routed to box B or E), and a "no" to the Form 8949 boundary blocks
   Schedule D instead of publishing lines 8a, 15 and 16 while line 7a
   blocks.
3. **One question closes the new families.** "Did you sell any securities
   whose basis was not reported to the IRS?" A "no" closes all eight new
   families empty. If one answer cannot do that without an engine or
   schema change, Track 1 stops and reports.
4. **Code W is in the class** on boxes B and E, with the column (g)
   mechanics of boxes A and D. Other adjustment codes, boxes C and F,
   digital assets and short sales stay out, refused by answer.

Foreman:

5. Track 1 includes P0's line 7a successor so a pure noncovered loss is
   Schedule D activity, and re-measures the loss and wash cases (expected
   line 7a -3000 and tax 3515; -2000 and 3635).
6. Families use `source-family.v2` constraints and identity exclusivity
   against the covered families, with `accounts_for` extended to match.

## Track 0 adversarial closure

Pending.

## Track 1 result

Pending.
