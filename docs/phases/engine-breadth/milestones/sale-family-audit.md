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

6. **Track 0 owner questions**, foreman 2026-11-08, on recommendation:
   - A box 7 "yes" blocks Schedule D line 16 and Form 1040 while the sale's
     own Schedule D part line shows its recorded amount. Accepted: the
     collectibles and QOF refusals behave the same, and no total publishes.
   - A false Exception 1 "no" with no sale recorded refuses without a
     question, unchanged from v81. Accepted for this milestone and parked;
     Decision 2's rewording makes the honest answer the default path.
   - A box 7 "yes" refuses even beside a gain. Accepted: it over-refuses
     but never publishes a wrong number. Reading box 7 only beside a loss
     is parked.
   - Box 4 and box 7 are asked once per recorded Form 1099-B statement
     (repairs `statement_box4`, `statement_box7`), so 150 of the 174 pinned
     v81 sale returns now ask them. Accepted.

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

Charter: `docs/reviews/sale-family-audit/charter-track1.md`. Core v82,
registry v80 and release v80. No engine, schema, expression or recording
change was needed.

The fresh-reader review (`docs/reviews/sale-family-audit/review.md`) found
two blocking defects, and v82 was rebuilt in place to repair them. The
bullets below record Track 1 as built. The current counts are under "Review
repairs: result".

- **Decision 2 on the prototype.** The new repair `exception1_words` gives
  the four Exception 1 input questions v2 successors. Each asks its own
  fact, and its "yes" is the fact's "yes" (for example, "Is it true that
  you had no capital losses in 2025 ...?"). The Track 0 harness was rerun
  on the final design:
  - The 296 earlier case runs are unchanged.
  - A new case, `m_empty_exc1_unanswered`, shows the four questions on the
    blocked Form 1040 lines. The totals are now 122 right, 158 correctly
    blocked, 8 observed, 10 rejected at entry and none wrong.
  - The 213 v81 returns classify exactly as in Track 0
    (`track0-closure.md`, "Track 1 addendum").
- **Successors.** There are 33 member edits: 5 adds and 28 replacements.
  Each is byte-identical to `prototype.artifacts()` with every switch on,
  and no published citizen was edited. The package, registry and release
  were made with `python3 -m tools.package_successor` and are
  byte-identical to the prototype's scratch build. The tool reported no
  inherited inconsistency. `packages/tax/loader.py` gives v82 v81's
  companion declaration (code B pairs included) and v81's covered-flag
  refusal map.
- **Tests.**
  - `tests/test_sale_family_audit_v82_package.py` (fast) checks:
    - byte identity with the prototype, the exact member edits, registry
      v80 add-only, release v80 and the loader entries;
    - the words of the four v2 Exception 1 questions and of the
      per-statement box 4 and box 7 questions, each against its fact's
      proposition and the rule that reads it;
    - the audit itself. `tables.py` runs over v82: every sale field is read
      by a rule or has a recorded reason, and every refusing answer is
      declared and read by a rule. The audit fails 38 times on v81 and
      fails when a new unread field is added.
  - `tests/test_sale_family_audit_v82.py` (live) runs on the published v82.
    - **Track 0 cases.** It runs every case of the final design in each of
      its answer modes: 298 case runs, of which 283 have distinct act
      lists. Each run is held to the harness's hand values, pins and
      questions, and must reach Track 0's recorded verdict.
    - **v81 returns.** It runs all 213 v81 returns, built by their own
      harness in a subprocess. Each direct or code W sale's rows are moved
      onto its own transaction (Decision 3). Each return runs with its
      recorded answers, and also with honest Exception 1 answers when a
      sale is recorded (198 returns).
    - **What it pins.** Lines, attachments, questions, each blocked line's
      reasons, the preferential base, and every watched row.
- **The v81 returns on v82**, after the row correction. At regeneration,
  every corrected return also ran on v81, and each run equals the
  committed v81 table.
  - With the recorded answers:
    - 184 are identical;
    - 23 are D5: line 25b now waits on an unclosed sale family beside a
      Form 1040 that v81 already blocked;
    - 5 are D1 count rows: a box C or F count row waits on an unclosed
      family, and no line changes;
    - 1 is D3, `a_duplicate_on_direct`. It records a direct sale with no
      rows at all, so there is nothing to move. Its line 1a goes from 0
      to blocked beside a Form 1040 already blocked.
  - No published number changes (2,035 numbers compared with the v81
    table).
  - Track 0's 57 D3 returns came from the builders' misplaced rows. With
    the rows corrected, 50 are identical, 6 are D5, and 1 is the D3 above.
  - With honest Exception 1 answers, every v82 run equals its
    recorded-answer run. v81 refuses line 16 in 158 of the 198 (D1). On
    v82, 57 of those compute the tax and 101 wait on another input.
- **Checks**, run locally at `670bfac2` (CI remains the gate of record):
  - `pytest -m "not live"`: 1732 passed, 8 skipped.
  - The full `pytest`, run in two parts:
    - every module except the new live one: 4830 passed, 24 skipped;
    - `tests/test_sale_family_audit_v82.py`: 698 passed.
  - `python3 -m mypy`: no issues in 471 files.
- **Deviations.**
  - A Track 0 case was added (`m_empty_exc1_unanswered`) to show the
    reworded questions. No earlier case showed an Exception 1 question.
  - `track0.py` now resumes a rerun from its raw file. A partial `cases`
    run no longer overwrites the design summaries and field sentences.
  - `tables.py` named the return-level box 4 and box 7 answers, which
    Track 0's repairs removed. It now names the per-statement answers and
    requires each refusing answer to be read by a rule.
  - Four inherited per-core checks name v82, as the v81 build did: the
    covered-flag refusal map, the required-versus-read allowlist (line 16
    v7) and the two C11 basis-comparison counts.
  - "Both answer modes" for the v81 returns is read as their recorded
    answers plus honest ones. Honest mode applies only when a sale is
    recorded, because on a return with no sale it changes nothing.
  - In the item 1 rerun, the v81 runs were reused from the Track 0 raw
    runs of the same act lists, because v81 did not change.
  - Cost: the live module makes 694 coordinator runs per full suite, and
    its table is 1.8 MB.

### Review repairs: result

Charter: `docs/reviews/sale-family-audit/charter-repair.md`. Evidence:
`track0-closure.md`, "Review repair addendum". Core v82, registry v80 and
release v80 were rebuilt in place from v81 with `python3 -m
tools.package_successor` (`prototype.py --publish`). There is no v83, and no
engine, schema, expression or recording change.

- **F1, row with no sale (`row_needs_sale`).** The v82 loader entry adds a
  presence pair from each covered and code W proceeds, basis and column (g)
  row to its own sale, as the other three kinds have. A row beside another
  sale, a row alone, and a row left after its sale is removed are refused.
  No content changes.
- **F2, line 7b (`line7b_activity`).** Form 1040 line 7b v2 (rule) and its
  field v3. Line 7b is inapplicable when a sale is recorded. It reads the
  sale counts and covered proceeds that line 16 v7 reads, and the
  Schedule-D-required conclusion decides it only when no sale is recorded.
- **F3 and N4, words (`field_truth`).** The line 16 not-applicable sentence,
  the line 7a blocked sentence, and the four Schedule D sale-line blocked
  sentences are now true of their rules.
- **F4.** The audit has a row table, and every amount row must be paired
  with its sale. Line 7b is in the projection, the consumers and the route
  readers. Honest Exception 1 answers read the v2 questions literally
  (`audit_harness.honest_exception1`).
- **F5.** The v81 honest reruns are gone, and so are the Track 0 base-answer
  runs that repeat their honest run.
- **N1 to N3** are fixed as small edits. N5 and the rest are parked below.
- **Successors.** 35 member edits: 5 adds and 30 replacements. The two new
  ones are line 7b v2 and its field v3. Each is byte-identical to
  `prototype.artifacts()` with every switch on, and the package, registry
  and release are byte-identical to the prototype's scratch build.
- **Track 0** (final design, every run rerun after each repair):
  - 310 runs: 127 right, 158 correctly blocked, 8 observed, 17 rejected at
    entry or refused by the run, and none wrong.
  - Twelve new review cases (group R). The design the review read
    (`track1`) publishes a wrong return in nine of them.
  - Apart from line 7b, no earlier final run changed.
- **The 213 v81 returns** on the published v82, corrected as the live test
  corrects them (rows on their own sale's transaction, and a sale removed
  after its rows):
  - 16 identical;
  - 168 differ only in line 7b, which is no longer checked beside a
    recorded sale;
  - 29 in the earlier D1, D3 and D5 classes, each with line 7b as well;
  - none unclassified, and no published number changed (2,035 numbers).
- **The same returns uncorrected** (`track0-rerun-output.json`, F1 rerun):
  63 are refused at entry because a row has no sale of its own. Of those, 56
  have misplaced rows and 7 remove a sale before its rows. The rest classify
  as before.
- **The audit** fails 56 times on v81 and passes on v82: 38 failures from
  P0, 8 Form 1099-B counts that line 7b does not read, and 10 unpaired
  covered and code W rows.
- **Live test cost.** 389 coordinator runs per full suite (down from 694):
  176 Track 0 runs and 213 v81 returns. Its table is 989,693 bytes (down
  from 1,761,186).
- **Deviations.**
  - One more correction to the v81 act lists in the live test: a direct or
    code W sale is removed after its rows (`rows_removed_first`).
  - The scratch build leaves out the unpublished v82 files, so it builds
    from v81 while packages/ holds a v82.
  - One inherited check (`test_capital_gain_distributions_line7a_t1_citizens`)
    reads the newest line 7b field and now expects v3. It still checks v2
    as history.
  - Track 0's decided and v81 runs were not rerun. They predate the line 7b
    watch.
- **Checks**, run locally at `71309ca5` (CI remains the gate of record):
  - `pytest -m "not live"`: 1737 passed, 8 skipped.
  - The full `pytest`, run in two parts:
    - every module except the live one: 4835 passed, 24 skipped;
    - `tests/test_sale_family_audit_v82.py`: 393 passed.
  - `python3 -m mypy`: no issues in 471 files.
  - `python3 tools/envelope_scan.py --range 8ddaca14..HEAD`: no findings.

### Review repairs: parked

These are the review notes and findings this repair does not fix, with
reasons.

- **N2, box 13 (bartering).** It is not a sale reported on Schedule D, and
  which answer refuses it is not established here. Boxes 8 to 11 are now
  named with the unasked `no-other-schedule-d-sources` answer.
- **N5.** The per-statement box 4 and box 7 questions do not name the
  statement that is unanswered. The owner accepted this in Decision 6.
- **The v2 Exception 1 words beside a zero-net sale** (review F2, second
  bullet). "Is it true that you had no capital gains ...?" still invites
  "yes" from a filer whose only sale nets zero. Since line 7b v2, no rule
  reads the Exception 1 answers beside a recorded sale, so that "yes"
  changes nothing. Rewording the questions to say "with no sale recorded"
  is parked.
- **The kernel's reverse presence check** (found in this repair). When a
  sale is touched, `packages/kernel/findings.py` checks only one row per
  sale: the last pair declared. A sale removed after its basis row (with
  its proceeds row left) is therefore admitted. The run then refuses
  ("companion provenance missing"), so nothing publishes. The noncovered,
  no-1099-B and code B pairs behave the same way. Fixing this needs a
  kernel edit, which is out of scope.
- **F5's further cuts.** Two more cuts are parked as judgement calls: the
  10 negative-proceeds runs, which could become entry-validation tests with
  no coordinator run, and fewer of the 28 duplicate-pair runs.
