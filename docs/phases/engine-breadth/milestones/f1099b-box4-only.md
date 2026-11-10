<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f1099b-box4-only",
  "status": "Open. Track 0 accepted; Track 1 (core v85) chartered.",
  "scope": [
    "a Form 1099-B statement that reports box 4 withholding and no sale (an open short at year end) has its box 4 amount asked, so line 25b is never short of withholding the filer received",
    "a statement with no sale and no withholding is asked nothing new beyond what establishes that",
    "every return core v84 computes correctly computes the same on the successor, and earlier cores render byte-identically"
  ],
  "non_goals": [
    "no short-sale computation, no other Form 1099-B boxes and no new Form 8949 codes",
    "no edit to packages/kernel/",
    "no edit to any published schema, adopted package or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/milestone-retrospectives/2026-11-10-f1099b-backup-withholding.md",
      "docs/milestone-retrospectives/2026-11-10-f1099b-box7-loss.md",
      "docs/phases/engine-breadth/milestones/f1099b-box4-only.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/f1099b-box4-only.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/f1099b-box4-only.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/f1099b-box4-only.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Form 1099-B Backup Withholding Without a Sale (2025)

Milestone key: f1099b-box4-only.
Branch: milestone/f1099b-box4-only-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-10.
Starting point: `github/main` at `5db600e7` (PR #267, core v84).

## What we are trying to accomplish

A broker can file a Form 1099-B that reports federal income tax withheld in
box 4 and no closed sale, for example an open short position at year end.
Core v83 counts a recorded box 4 amount on such a statement toward Form
1040 line 25b, but asks the box 4 amount only of statements with a recorded
sale. A filer holding only that statement is never asked, and line 25b can
publish short of withholding they received. The useful outcome is a core
v85 that cannot publish line 25b while such withholding may be unasked.

## What we know

- Core v83 asks one box 4 amount per Form 1099-B statement with a recorded
  sale (`input-question.f1099b-box4.v1.json`), and adds every current amount
  to line 25b, including one whose statement has no recorded sale
  (f1099b-backup-withholding Decision 6).
- A Form 1099-B statement is known to the engine today through its sales;
  whether a statement can be recorded with no sale is not known.
- **What we do not know.**
  - How a statement with no sale enters the record on core v84, if it can,
    and what closes "every Form 1099-B statement" for a return.
  - Whether a return-level question ("did you receive a Form 1099-B with
    no sale on it?") or a per-statement question is the smallest honest
    shape, and which existing closure or answer can carry it.
  - How many recorded v84 returns would newly be asked, and whether any
    published number changes.

## Actions the team will take

1. **P0: measure and design.** Table every rule, question and closure that
   reads Form 1099-B statements and box 4 on core v84. Probe v84 through
   `live_coordinate_run`. Compute by hand from the 2025 instructions.
   Prototype a content-only scratch core v85. Stop and report if the fix
   needs an engine, schema or recording change.
2. **Decide.** How a no-sale statement is asked for, and its refusal or
   block reason.
3. **Track 0 adversarial closure.** The six artifacts over the fix.
4. **Track 1: build.** Core v85 and its registry and release, with live
   and package tests.
5. **Close.** Fresh-reader review, repair, exact-head CI, retrospective,
   roadmap. Merge on green verify (owner standing approval, 2026-11-07).

## Cases that will shape the design

- One Form 1099-B with box 4 withholding and no sale, nothing else.
- That statement beside a W-2 with withholding, and beside a statement
  with a sale and its own box 4.
- A return with no Form 1099-B at all.
- A no-sale statement with box 4 of zero.
- A no-sale statement recorded, then a sale added to it; a sale removed so
  the statement has none.
- Every return core v84 computes: identical on v85, unless the new
  question is asked, and then no published number changes once answered
  as recorded.

## Process

Dispatch is through the grok CLI (owner, 2026-11-09). Each unit commits on
this branch as it goes. Track 0 hand values come from the instructions,
never from what a prototype publishes (f1099b-backup-withholding
retrospective). A sentence the filer reads on a blocked row is a claim:
P0 records the sentence the presentation actually shows
(f1099b-box7-loss retrospective).

## P0 result

Evidence: `docs/phases/engine-breadth/milestones/f1099b-box4-only-evidence/p0.md`.
The table is `statement-table.json`. The 2025 quotes and checksums are `law.json`.
The thirteen design cases are `probe-output-v84.json` and `probe-output-v85.json`.
The scratch successor is `prototype.py` with `prototype-build.json`. The 298
recorded v83 runs are `rerun-output.json`.

A Form 1099-B statement is an entity. Nothing closes the set of statements.
The box 4 amount is asked only of statements with a sale. A no-sale statement
can be introduced, and a recorded amount on it already counts, but nothing
asks for that amount. Core v84 publishes line 25b short of withholding on
`b4_only_unasked` (0 vs 150) and `b4_only_beside_sale_unasked` (200 vs 350).

The scratch core v85 is content only: a return-level yes/no, a return-level
amount when yes, line 25b v8, and field v6. The per-statement question is
unchanged. All thirteen probes match the hand on v85. Of the 298 recorded
runs, 207 are identical and 91 newly ask the yes/no. No published number
changes. No engine, schema, expression, or recording-surface change was
required.

Recommendation: adopt that shape.

Decisions:

1. A return-level yes/no, rather than a per-statement question that would need a new recording surface.
2. Keep the existing per-statement box 4 question for statements that have a sale.
3. When yes, ask one return-level amount and add it; when no, add nothing new.
4. Ask the yes/no of every return, including a return with no Form 1099-B.
5. Keep Decision 6: a per-statement amount with no sale still counts; do not also enter it at return level.
6. After a sale is added, present is no and the per-statement amount is the one copy.

## Decisions

Foreman, 2026-11-10, on P0. The owner's direction is to proceed on the
recommended choice; the owner adjusts after. Foreman check: every case id
the P0 tables cite is in both probe outputs, and the rerun replayed the
recorded answers.

1. **A return-level yes/no** asks whether the filer received a Form 1099-B
   or substitute statement showing box 4 withholding and no closed sale.
   A per-statement question would need a recording surface for a
   statement with no sale; that is not taken.
2. **The per-statement box 4 question is unchanged** and still asked of
   every statement with a sale.
3. **Yes asks one return-level amount**, the total of those statements'
   box 4, added to line 25b. No adds nothing and asks nothing more.
4. **Every return is asked the yes/no**, including one with no Form 1099-B,
   as the other return-level scope answers are. Of the 298 recorded runs,
   the 91 that publish line 25b on v84 newly block until it is answered;
   answering no must restore every v84 number (Track 0 measures it).
5. **Decision 6 of f1099b-backup-withholding stands**: a per-statement
   amount on a statement with no sale still counts.
6. **One copy of each dollar.** After a sale is added to a no-sale
   statement, that statement no longer answers yes; its per-statement
   amount is the one copy.
7. **The return-level questions exclude what is already entered.** The
   yes/no and the amount wording say not to include a statement whose box
   4 was entered with its sales. Track 0 pins the double count
   (`no_sale_then_sale_added_double`) as the dishonest answer it is, and
   the honest single-count paths.

## Track 0 adversarial closure

Foreman, 2026-11-10: accepted. Six rows PASS; the cited case ids are in
the committed outputs; the 91 newly asked returns restore every v84 number
when the yes/no is answered no. Track 1 is chartered in
docs/reviews/f1099b-box4-only/charter-track1.md.

Evidence: `docs/phases/engine-breadth/milestones/f1099b-box4-only-evidence/track0-closure.md`.
Scratch core v85 through `live_coordinate_run`; `track0.py` writes
`track0-authority.json`, `track0-matrix.json`, `track0-late.json`,
`track0-reuse.json`, `track0-neighbour.json`, and `track0-surface.json`.
Hand values come from `probe.hand_return`. Decision 7 wording is on the
two return-level questions and the line 25b field.

- Authority-lifecycle table: PASS — `track0-authority.json` (8 cases). Present unanswered blocks and asks the yes/no (`alc_present_unanswered`). Present no publishes 0 (`alc_present_no`). Present yes with 150 publishes 150 (`alc_present_yes_amount`). A sale statement's 200 is that statement (`alc_stmt_with_sale`). A no-sale per-statement 150 still counts (`alc_stmt_without_sale`). Two statements do not share an amount (`alc_stmt_identity`, 350). The dishonest two-copy answer publishes 300 (`alc_double_count`).
- Empty/nonempty authority matrix: PASS — `track0-matrix.json` (25 cases). No Form 1099-B, sale only, no-sale only, and both, each with present unanswered / no / yes with amount / yes amount unanswered, plus per-statement zero and nonzero. Unanswered blocks (`m_none_unanswered`, `m_sale_unanswered_stmt200`, `m_nosale_unanswered`, `m_both_unanswered_sale200`). Present no on a sale equals v84 (`m_sale_no_stmt200` is 200). Decision 6 still counts a no-sale per-statement amount (`m_nosale_no_stmt150`, `m_both_no_sale200_stmt150`).
- Late-member lifecycle: PASS — `track0-late.json`. Adding a sale and changing present to no keeps one copy (`late_yes_then_sale_then_no`, 150). Removing the sale leaves the per-statement amount (`late_sale_removed`, 200). Correcting the return-level amount from 150 to 80 drops the prior line 25b finding (`late_amount_corrected`). Superseding yes with no publishes 0 (`late_yes_to_no`).
- Neighboring capability dependency diff: PASS — `track0-neighbour.json`. 298 recorded returns, live on v84 and live on scratch v85, 207 `identical`, 91 `asks_no_sale_present`, 0 counterexamples. Those 91 rerun with present=no restore every v84 number (91/91).
- Reused-claim semantic/lifecycle equivalence: PASS — `track0-reuse.json`. The six line 25b subtotals match v84 on a present-no return (`reuse_int_alone` 50, `reuse_div_alone` 75, `reuse_ira_alone` 80, `reuse_unemp_alone` 90, `reuse_ssa_alone` 60, `reuse_all_five_alone` 355, `reuse_all_with_b4` 455, `reuse_b4_subtotal` 200). The per-statement box 4 question is unchanged (`reuse_box4_question`). Box 7 checks compose unchanged (`reuse_box7_check`). A present-no wage return equals v84 (`reuse_no_equals_v84`). Only line 25b's rule and form field move, v7 to v8 and v5 to v6.
- Integration surface: PASS — `track0-surface.json`. Bindings: line 25d requires line 25b; the line 25b field binds it; lines 33, 34, and 37 follow 25d. Six models, one disposition row each. Unanswered yes/no shows the Decision 7 present question (`surface_blocked_present`). Unanswered amount shows the Decision 7 amount question (`surface_blocked_amount`).
- Known limitations affecting correctness: none

