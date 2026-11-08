<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f8949-code-b",
  "status": "Open. P0 (law, state on core v80, design) first.",
  "scope": [
    "a return with a Form 1099-B sale whose reported basis is wrong computes Form 8949 with code B and the column (g) correction, Schedule D, Form 1040 line 7a and the tax, from a corrected basis the filer supplies, on boxes A, B, D and E as the instructions allow",
    "every return core v80 computes computes the same on the successor, and earlier cores render byte-identically",
    "what stays outside the class is refused by an answer, never computed partially"
  ],
  "non_goals": [
    "no adjustment codes other than B and W, and no rows carrying more than those",
    "no digital assets, no short sales, no other Schedule D sources",
    "no edit to packages/kernel/",
    "no edit to any published schema, adopted package or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/milestone-retrospectives/2026-11-07-f8949-boxes-cf.md",
      "docs/phases/engine-breadth/milestones/f8949-code-b.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/f8949-code-b.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/f8949-code-b.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/f8949-code-b.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Broker Basis Corrections (2025)

Milestone key: f8949-code-b.
Branch: milestone/f8949-code-b-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-07.
Starting point: `milestone/f8949-boxes-cf-2025` at `27fc2390` (PR #262,
core v80). It was rebased onto `github/main` at `dd81de67` after #262
merged.

## What we are trying to accomplish

Core v80 computes Form 1099-B sales in boxes A to F with code W. When a
broker reports a wrong basis, which often happens after a corporate action
or with employee stock, the filer reports the sale with code B and
corrects the gain or loss in column (g). Today the in-class answer
refuses that return. The useful outcome is that it computes, from a
corrected basis the filer supplies.

## What we know

- **What exists on v80.** Covered families (boxes A and D) and
  noncovered families (B and E), each with a code W path. Box C and F
  families. Two grouped closure questions (`source-closure-mapping.v4`,
  ADR 0084). The ADR-0061 Path B answer for codes other than W. Lines 2,
  3, 9 and 10, with paired-amount, count and amount-agreement checks.
- **Lessons.** The f8949-boxes-cf retrospective: check each input
  question's words against its proposition when it is written; pin each
  blocked line's reason and its row's (disposition, code, missing) from
  the first live test; load evidence harnesses under unique module names.
- **What we do not know.**
  - What the 2025 instructions require for code B. The relevant points
    include whether the broker's basis is shown in column (e) with the
    correction in (g), or the correct basis in (e). They also include how
    a basis-reported sale with code B moves from line 1a/8a direct
    reporting or box A/D to Form 8949, and how code B combines with W on
    one row.
  - Whether the v80 pattern carries over as content only.
  - What a v80 return with a wrong broker basis does today.

## Actions the team will take

1. **P0: law, state and design.**
   - Law from the 2025 instruction sources, with quotes.
   - State on core v80 through `live_coordinate_run`.
   - The smallest successor set, prototyped on scratch. Every case's
     attachment dispositions and block reasons are asserted, and the
     gain, loss and wash cases are computed by hand.
   - Stop and report if an engine, schema or recording change is needed.
2. **Decide.** The class and the question shape. The owner decides if a
   schema, ADR or recording change is needed.
3. **Track 0 adversarial closure.** The six artifacts, with built
   evidence. No row passes beside a standing counterexample.
4. **Track 1: build.** Successors, core v81 and its registry and release,
   cases through the real coordinator and the page, v80 and earlier
   pinned, full suite.
5. **Close.** Fresh-reader review with hand-computed lines, exact-head CI,
   retrospective, roadmap, frontier row and parked list. Merge on green
   verify (owner standing approval, renewed 2026-11-07).

## Cases that will shape the design

- A covered box A sale whose broker basis is too high (a smaller gain
  becomes a larger one), and a box D sale whose broker basis is too low.
- A code B correction that turns a gain into a loss (line 21 limit).
- A row with both B and W.
- A noncovered box B or E sale. Code B needs no correction there, since
  the basis is the filer's own, so the case is refused or not applicable.
- A code B sale with the corrected basis missing: it blocks and asks.
- Every return core v80 computes: identical on the successor.

## Process

Dispatch is to Opus and Sonnet sub-agents (owner, 2026-11-06, renewed
2026-11-07). Opus runs P0, Track 0 and the fresh review; Sonnet runs
content-only build units. Each unit commits on this branch as it goes.

## P0 result

Evidence: `f8949-code-b-evidence/p0-law-state-design.md`, with
`codeb_probe.py` / `codeb-probe-output.json` (core v80) and
`codeb_prototype.py` / `codeb-prototype-output.json` (scratch core v81).

- **Law.** On box A or D, column (e) is the basis the Form 1099-B shows,
  even though it is wrong. Column (g) is that basis minus the correct
  basis, from the Worksheet for Basis Adjustments. The sale stays in box A
  or D and goes on line 1b or 8b, never on line 1a or 8a. With code W the
  row's codes are "BW", and column (g) is the net: correction plus the
  wash-sale loss disallowed, measured on the corrected loss. On box B or E,
  code B applies with the correct basis in (e) and -0- in (g). On box C or
  F code B does not apply.
- **v80.** Honest answers refuse a code B return through the boundary
  answers (v80 check 3 on lines 3 and 10, and the line 1a/8a nonzero
  arms). The block has no question. If the filer follows the Form 1099-B
  and claims no Form 8949, v80 publishes the broker's wrong gain. If the
  corrected basis is recorded on line 1a/8a, on box B/E, or on code W with
  a false Path B, v80 publishes the right dollars on the wrong line or box.
  Box B/E code B already computes the right dollars, but no code is shown.
- **Design.** A content-only core v81 with 57 member edits (32 adds, 25
  replacements) and two loader entries:
  - code B sale families for box A and D, keyed like other Form 1099-B
    sales;
  - the correct basis on the sale, and a column (g) row that must equal
    the worksheet;
  - a third grouped question and a code B in-class answer, read through a
    guarded arm placed before the v80 one;
  - lines 1b and 8b add the code B column (h).

  All 30 v81 cases match their hand values and blocked states. All 143 v80
  returns are identical on v81 under the new "no". Unanswered, every one
  blocks and asks the new question. No engine, schema or recording change
  is needed.
- **Owner questions** (P0 document, "Questions for the owner"):
  1. the question shape and the one new answer on every workspace;
  2. whether the correct basis gets its own row, so that a missing one
     blocks and asks;
  3. how box B/E code B is marked;
  4. whether part labels are enough for column (f).

## Decisions

Foreman, 2026-11-07, on P0. The owner's direction is to proceed on the
recommended choice; the owner adjusts afterwards.

1. **The P0 design is adopted.** It adds new box A and D code B sale
   families, each with paired proceeds, basis and column (g) rows. A
   column (g) check requires (basis shown − correct basis + wash-sale
   amount). It adds one new grouped question ("Did any Form 1099-B …
   report … a basis that is wrong?") and a new in-class answer, read only
   after that "yes" and before the v80 in-class answer. Every v80
   workspace answers the new question once. With "no", all 143 v80
   returns are identical.
2. **The correct basis stays on the sale record.** A sale entered without
   it is rejected at entry. The column (g) row blocks and asks. A separate
   correct-basis row would add two families and two questions and would
   make no return more correct.
3. **Box B/E code B: option (a).** The existing in-class answers cover it:
   the filer enters the correct basis, and column (g) is -0-, so the
   dollars are right. The part labels do not show the letter B for these
   rows.
4. **Column (f) letters: part labels are enough for this milestone.** A
   per-row code letter on Form 8949 (B on box B/E rows, BW on combined
   rows) is parked for a later milestone that models column (f) letters
   for every code.

## Track 0 adversarial closure

Pending.

## Track 1 result

Pending.
