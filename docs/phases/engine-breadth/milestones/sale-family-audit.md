<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "sale-family-audit",
  "status": "Open. P0 (audit of every sale family on core v81) first.",
  "scope": [
    "every field a Form 1099-B or Form 8949 sale record carries is either read by a rule or refused by an answer when it would change the return",
    "no sale family on the successor publishes a wrong number, a missing attachment or a double count from honest answers",
    "every return core v81 computes correctly computes the same on the successor, and earlier cores render byte-identically"
  ],
  "non_goals": [
    "no new Form 8949 codes, boxes or Schedule D sources",
    "no column (f) letters and no block-names-its-question rule successor",
    "no edit to packages/kernel/",
    "no edit to any published schema, adopted package or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/milestone-retrospectives/2026-11-07-f8949-code-b.md",
      "docs/milestone-retrospectives/2026-11-07-f8949-boxes-cf.md",
      "docs/phases/engine-breadth/milestones/sale-family-audit.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/sale-family-audit.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/sale-family-audit.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/sale-family-audit.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Sale Family Audit (2025)

Milestone key: sale-family-audit.
Branch: milestone/sale-family-audit-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-07.
Starting point: `milestone/f8949-code-b-2025` at `1e8de2e3` (PR #264, core
v81). Rebased onto `github/main` at `9a29b1ed` after #264 merged.

## What we are trying to accomplish

Each of the last three milestones found more inherited wrong-number paths
in the sale families. Examples include zero proceeds without attachments,
one transaction counted twice, line 7a not reading lines 1a and 8a, and
eligibility flags no rule reads. The code B retrospective asked for one
audit of every sale family instead of one discovery per milestone. The
useful outcome is a core v82 on which no sale family publishes a wrong
return from honest answers, and an audit table that later sale work
extends.

## What we know

- **The families on v81:**
  - covered direct (lines 1a and 8a);
  - covered code W (lines 1b and 8b);
  - code B (boxes A and D);
  - noncovered (boxes B and E, with W);
  - no-1099-B (boxes C and F, with W).
- **The questions on v81:** three grouped `source-closure-mapping.v4`
  questions; the in-class answers (v79, v80, v81); ADR-0061 Path B; the
  Form 8949 boundary.
- **Fixed already.** Zero proceeds, cross-term duplicates, five
  eligibility flags on covered and code W, amount agreement, paired
  amounts.
- **What we do not know.**
  - Which fields each sale schema carries that no rule reads. Candidates
    include box 1f market discount on noncovered sales, box 1d proceeds
    type, gross versus net proceeds, box 2 ordinary, box 3 collectibles,
    box 5 noncovered, box 7 loss-not-allowed, and federal withholding in
    box 4.
  - Which value edge cases still publish: negative proceeds, basis above
    proceeds with W, a holding period on the boundary day.
  - Whether every family's subtotals reach every consumer.

## Actions the team will take

1. **P0: the audit.** Build a table of every sale fact type's fields
   against the rules that read them, and of every family against each
   consumer: lines 1a to 10, 15, 16, 21, line 7a, the preferential base,
   both attachments, and line 25b withholding. For each unread field or
   unreached consumer, build a case on core v81 through
   `live_coordinate_run` and say whether a wrong return publishes. Compute
   the right answer by hand from the 2025 instructions. Prototype content
   fixes on a scratch core v82. Stop and report if a fix needs an engine,
   schema or recording change.
2. **Decide.** Which defects are fixed, and which are refused by answer
   or parked.
3. **Track 0 adversarial closure.** The six artifacts over the fixes.
4. **Track 1: build.** Core v82 and its registry and release. The audit
   table becomes a committed test that fails when a new sale field is
   left unread.
5. **Close.** Fresh-reader review, exact-head CI, retrospective, roadmap.
   Merge on green verify (owner standing approval, renewed 2026-11-07).

## Cases that will shape the design

- One case per unread field set to a value that changes the tax.
- Zero, negative and equal amounts on every family.
- One transaction recorded on every pair of families, within a term and
  across terms.
- Every return core v81 computes: identical on the successor, unless it
  was wrong and the plan accepts the change.

## Process

Dispatch is to Opus and Sonnet sub-agents (owner, 2026-11-06, renewed
2026-11-07). Each unit commits on this branch as it goes.

## P0 result

Evidence: `sale-family-audit-evidence/audit.md`. It covers 81 probes on v81
and on a scratch v82 (`probe.py`), the field and consumer tables
(`tables.py`), the v82 prototype (`prototype.py`), and the 213 pinned v81
returns rerun on v82 (`export_v81_returns.py`, `rerun_v81.py`). All runs go
through `live_coordinate_run`. The harness is self-contained.

- **Wrong returns on v81** (hand values in the audit):
  - A line 1a sale with box 1g checked publishes the whole loss (D4).
  - A covered or code W sale's `long_term` flag is unread, so a long-term
    sale on line 1a is taxed as short-term (D5).
  - A covered or code W sale's rows can differ from the sale, or be
    missing, and the lines sum the rows (D6).
  - Form 1099-B box 4 withholding never reaches line 25b (D7).
  - A box 7 loss publishes (D8).
  - A box C/F sale for 0 with basis 0 requires no attachment (D3).
- **Blocks on v81 with no true reason:**
  - With the Exception 1 question answered truthfully, Form 1040 line 16
    has no tax for any return whose sales are only on code W, box B/E, box
    C/F or code B (D1). Every earlier case kept the base's false Exception 1
    answers.
  - Zero-net sales are not Schedule D activity for the preferential base and
    line 7a (D2). Under the false Exception 1 answers this also gives a wrong
    base beside a box 2a distribution.
- **Not defects:**
  - box 5;
  - box 6 / gross proceeds, box 2 Ordinary, box 1f and box 3 on the
    non-covered kinds, which are refused by answers (three of those answers
    are never asked);
  - negative proceeds, which are rejected at entry;
  - all 28 cross-family duplicate pairs, which block.
- **Design:**
  - Scratch v82, content only: 27 member edits (5 adds, 22 replacements),
    seven switches.
  - No engine, schema, expression or recording change. The two loader
    entries are needed, as for v81.
  - All 81 cases match their hand values or block as intended, in both
    answer modes.
- **v81 returns:**
  - 134 of 213 are identical.
  - 57 change only through the `paired_rows` switch, because the earlier
    harnesses record a direct or code W sale's rows on other transactions.
    Without that switch, 51 of the 57 are identical.
  - 23 already-blocked returns also block line 25b.
  - 5 add a blocked count row.
  - No return publishes a different number.
- **Audit test:** the `tables.py` check fails 38 times on v81 and passes on
  v82.
- **Owner questions** (audit, "Questions for the owner"):
  1. Exception 1 question polarity.
  2. Take `paired_rows`.
  3. Box 4 and box 7 by answer now.
  4. The unasked boundary answers.
  5. Line 25b blocking on unclosed families.

## Decisions

Foreman, 2026-11-08, on P0. The owner's direction is to proceed on the
recommended choice; the owner adjusts after.

1. **All seven fixes are taken:** `tax_activity`, `no1099b_count`,
   `base_activity`, `admission_reads`, `paired_rows`, `box4_question` and
   `box7_question`. D1 comes first. On v81 no Form 8949 return answered
   truthfully gets a tax.
2. **The Exception 1 questions are reworded in Track 1.** Each question's
   "yes" must mean what its fact's "yes" means, so that an entry screen
   recording the reply literally gives the right tax. The words are pinned
   against their propositions.
3. **`paired_rows` is taken.** A sale whose rows sit on another transaction
   publishes as if the rows were absent, so the 57 changed v81 returns
   are accepted. The earlier harness builders that record rows on a
   different transaction are corrected in the new tests. Published v81
   pins stay as they are.
4. **Box 4 and box 7 are refused by answer.** A real Form 1099-B box 4
   withholding family is parked.
5. **Accepted limits:**
   - The unasked boundary answers (lines 18-19, QOF, Path B, no Form 8949)
     stay unasked. This extends Decision 7 of f8949-code-b.
   - Line 25b blocks while a sale family is unclosed.

## Track 0 adversarial closure

Evidence: `sale-family-audit-evidence/track0-closure.md` (`track0.py`,
`track0-output.json`, `track0-rerun-output.json`). Every run goes through
`live_coordinate_run` on the scratch v82, in both answer modes, on the
decided design (FIXES) and the final design (FIXES plus three Track 0
repairs). Final: 122 right, 156 correctly blocked, 8 observed and 10 rejected
at entry (negative proceeds), with none wrong. Decided: 6 wrong runs, the
counterexample below.

- **Counterexample, fixed.** The decided box 4 and box 7 answers are one per
  return. They stay current when a sale from a new Form 1099-B statement is
  recorded: `t2_s2` publishes line 25b 0 beside 1,440 of box 4
  withholding, `t2c_s1` the same on line 1a, and `t3_s2` a box 7 loss.
  Repairs `statement_box4` and `statement_box7` ask once per recorded
  statement. Line 25b v6 and Schedule D line 16 v3 require an answer for
  every Form 1099-B sale's statement (`require_paired` on `statement`) and
  block on any "yes".
- **Presentation repair.** `field_words`: Form 1040 line 16 (field v3) and
  line 7a (field v2) now say they also wait for the sale answers.
- Final scratch v82: 29 member edits (5 adds, 24 replacements). No engine,
  schema, expression or recording change.

- Authority-lifecycle table: PASS — every fact the fixes read (sale counts,
  `long_term`, direct box 1g, row pairing, the per-statement box 4 and box 7
  answers, Exception 1) with its invalidating events, each cited to cases;
  the decided return-level answers are the counterexample, now unread.
- Empty/nonempty authority matrix: PASS — every family closed empty,
  authority missing, nonempty eligible and ineligible; Exception 1 in all
  four polarities beside five families (20 cases, identical results);
  box 4 / box 7 yes, no and unanswered per statement.
- Late-member lifecycle: PASS — T1 (wage → box E sale → Schedule D route:
  TI 38,250, tax 3,875; v81 honest `gi`), T2 (box 4 "no" then a sale on a
  new statement: blocks and asks; same statement computes), T3 (box 7),
  T4 (removed sale), T5 (box C 0/0).
- Neighboring capability dependency diff: PASS — prerequisites before and
  after for each consumer, each justified by its own meaning; all 213 v81
  returns classified: 134 identical, 51 D3, 6 D3 + D5, 17 D5, 5 D1 count
  rows, 0 unclassified, no published number changed, all 79 changes equal
  to P0's decided v82.
- Reused-claim semantic/lifecycle equivalence: PASS — Exception 1 paths of
  line 16 and the base narrowed (read only with no sale), line 25b's
  subtotals and the eight counts unchanged; the new counts, answers and
  admission values are not reused.
- Integration surface: PASS — 974 of 974 members resolved; every consumer
  of line 16, 24, 25b, 33, 34, 37, 7a, the base, Schedule D line 16 and both
  attachments listed with cardinality; 45 watched publishers record exactly
  one row in every saturated run; one built model per disposition path with
  pinned (disposition, code, missing); presentation probe of every changed
  field and new question.
- Known limitations affecting correctness: none. Owner disposition is asked
  on four presentation and refusal-posture questions
  (`track0-closure.md`, "Owner questions"): Schedule D part lines beside a
  box 7 refusal, the question-less refusal of a false Exception 1 "no" with
  nothing recorded (unchanged from v81), box 7 over-refusal on a gain, and
  the per-statement question shape.

## Track 1 result

Pending.
