<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f8949-boxes-cf",
  "status": "Closed. On core v80 a sale of securities with no Form 1099-B (Form 8949 box C or F, code W allowed) computes Schedule D lines 3 and 10, Form 1040 line 7a and the tax from filer-supplied proceeds and basis. A second grouped question closes the new families; every v79 answer keeps its meaning. Lines 2, 3, 9 and 10 block on a missing, shared or disagreeing amount. Core v79 and earlier are unchanged.",
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
      "docs/milestone-retrospectives/2026-11-07-f8949-boxes-cf.md",
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
Closed 2026-11-07. Retrospective:
`docs/milestone-retrospectives/2026-11-07-f8949-boxes-cf.md`.

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

Foreman, 2026-11-06, on Track 0:

5. **Track 0's six content repairs are adopted** (B1 to B6 and the
   "entered only once" wording). The four further v79-computed returns
   that now block are accepted: `t0_q1_yes_nothing`,
   `t0_8949no_old_ic_yes_q1_no`, `t0_b_loss_8949_yes` and
   `t0_b_w_scalar_only_on_gain`. Each one was a silent omission or a
   wrong number on v79.
6. **The presentation limit in Decision 4 covers the five refused paths
   Track 0 named.** Each shows a true blocked reason but no question. A
   rule-artifact successor whose block names the question it waits on is
   parked for the roadmap.
7. **The new question is asked even on a return that answers Form 8949
   "yes"**, as v79 asks its own question. Not asking it would need an
   engine change.

## Track 0 adversarial closure

Evidence:
[track0-closure.md](f8949-boxes-cf-evidence/track0-closure.md). Scratch
core v80 through `live_coordinate_run`; `track0.py` writes
`track0-output.json`. Source ref (removed at closeout).

The decided design had seven counterexamples. The prototype now fixes six
with content-only repairs, and refuses the seventh by an answer:

- each box B/E sale needs its own amount rows (a count beside
  `require_paired`);
- the Form 8949 attachment reads lines 2 and 9;
- each sale's amount rows must equal its sale object (per-sale agreement
  rule, the 1099-K shape);
- a v79 "yes" needs a recorded sale;
- a v79 in-class "yes" admits a Form 8949 "no" only beside a v79 "yes";
- a recorded sale needs a Form 8949 "no";
- the new in-class answer now says "entered only once", so its "no" refuses
  a duplicate entry.

Lines 2 and 9 take Decision 3 as decided.

- Authority-lifecycle table: PASS — every contributed fact and its
  invalidating events, each with built cases. Code W on boxes C and F holds
  only with the amount-agreement repair (`w_c_scalar_only_on_gain`,
  `w_c_amounts_disagree`, `w_c_object_wash_no_row` publish on the decided
  design and block now). A reused transaction entity is caught
  (`d3_b_shared_transaction`).
- Empty/nonempty authority matrix: PASS — 24 rows over both group questions,
  including a "yes" with nothing recorded (`m_yes_nothing_no`,
  `m_no_yes_nothing`, `m_yes_yes_nothing`) and Form 8949 "no" with nothing
  admitted (`m_no_no_8949no*`). Every closed-empty, fully answered row is
  the wage return, 34250 / 3875. Every out-of-class row blocks Form 1040 and
  both attachments.
- Late-member lifecycle: PASS — `t1_stage0`–`4` (box F after a "no"),
  `t2_stage0`–`3` (box C after a computed v79-style return) and
  `q2_late_yes_*`. Each stale closure asks again. After a box C sale the
  false v79 in-class "yes" decides nothing (`t2_stage3_old_ic_no` is
  identical to `t2_stage3`).
- Neighboring capability dependency diff: PASS — the only new prerequisite
  on a return with no sales is the new question. It is justified by lines 3
  and 10's own closure under ADR 0084, as Q1 is on v79, and it cannot be
  derived from the Form 8949 answer without an engine change. Of the 28
  returns v79 computes in P0's set, 22 are identical, and 6 change as
  Decisions 2 and 3 accepted. Four Track 0 returns that v79 computes wrongly
  or silently now block (owner question 1).
- Reused-claim semantic/lifecycle equivalence: PASS — the v79 group
  question, the ADR-0061 pair and the v79 in-class answer keep their
  proposition, identity, lifecycle and scope. Their v79 carriers are
  unchanged members. The preferential gate is a successor (v8), not a reuse.
- Integration surface: PASS — exactly one disposition row per publisher of
  lines 2, 3, 7, 9, 10, 15, 16, 21, line 7a, the preferential base and both
  attachments in all 89 runs. Each of the four amount checks has one row
  per run. There is a built model per disposition path, and a
  presentation-model probe for lines 2, 3, 7, 9, 10 and 15.
- Known limitations affecting correctness: none. Owner disposition required
  for the four newly blocked v79-computed returns, and for the
  presentation-only block-without-question paths beyond Decision 4
  (track0-closure.md, "Owner questions").

## Track 1 result

Core v80, registry v78 and release v78 are published on this branch. They
are built from the Track 0 scratch v80 with every `REPAIRS` switch on.

- **Successors.** The 61 member edits (43 added, 18 replaced) are the files
  in `cf-prototype-rules/`, copied byte for byte into
  `packages/content/tax/2025/`. `tools.package_successor` produced the
  same package checksum (`3e5444b2…`) and release sha256 (`76c864bd…`)
  as the Track 0 scratch build. Registry v78 only adds entries. No
  published citizen or schema is edited.
- **Loader.** v80's companion declaration is v79's pairs plus the six box
  C and F scalar pairs. v80 names v79's covered-flag refusal map. These
  are the two entries the prototype patched in process.
- **Cases.** `tests/test_no1099b_sales_v80.py` runs the cases on the
  published v80 through `live_coordinate_run` and the presentation model:
  - All 71 Track 0 cases. 69 run. Two are rejected before a run, as
    recorded: `c_basis_object_missing` (the sale schema needs a basis) and
    `d3_b_orphan_basis` (ADR-0082 presence pair).
  - The 50 v79 returns under the new "no". 48 run. Two are rejected as on
    v79: `duplicate_horizon` and `probe_e_basis_object_missing`.

  Each run's lines, attachment dispositions and questions equal the
  Track 0 record. `cf_prototype.check`'s hand values hold. Each run also
  shows:
  - one disposition row per publisher of lines 2, 3, 7, 9, 10, 15, 16 and
    21, line 7a, the preferential base, both attachments and the four
    amount checks;
  - explain text on lines 2, 3, 7, 9, 10 and 15;
  - no blocked line without a blocked text or reason.

  Form 1040 lines 15 and 16 keep their v79 dollars, except the ten
  returns accepted as newly blocked:
  - Decision 2: four returns, including `boundary_no_without_member`;
  - Decision 3: two returns;
  - Decision 5: four returns.

  `tests/test_noncovered_sales_v79.py` is unchanged.
  `tests/test_no1099b_sales_v80_package.py` checks the successor and
  registry facts statically.
- **Other test updates the new members require:**
  - the refusal-map test names v80;
  - the broker-basis consumer trace names the noncovered amount-agreement
    rules and lines 2 and 9;
  - `tools/required_versus_read_allowlist.json` moves the line 1a and 8a
    witnesses to v5 and v6, and lists the amount-check witness that lines
    2, 3, 9 and 10 require but do not read.
- **Deviation from the prototype:** none in content, package or loader.
  The allowlist edit sits in `tools/`, outside the charter's literal list,
  as v79's did. The new live module loads the f8949 evidence `track0.py`
  under its own module name, because the noncovered evidence has a
  `track0.py` too. On the first full run that name clash failed 41 v79
  tests.
- **Checks:**
  - `pytest -m "not live"`: 1693 passed, 8 skipped.
  - Full `pytest`: 4563 passed, 24 skipped, 0 failed.
  - `python3 -m mypy`: no issues in 467 files.

### Repair

This repair covers the fresh-reader review
([review.md](../../../reviews/f8949-boxes-cf/review.md), charter
`docs/reviews/f8949-boxes-cf/charter-repair.md`). Core v80, registry v78
and release v78 are rebuilt in place, still from v79. The package
checksum stays `3e5444b2…`, because the member list is unchanged. The
changed members' registry entries and the release sha256 (`00d498fe…`)
are new. `cf_prototype.build` now removes the branch's v80 copies
before it builds, so the scratch build runs beside the published files.
All 61 `cf-prototype-rules/` files are still byte-identical to
`packages/content/tax/2025/`.

- **B1.** The in-class question now exempts a covered sale only when it
  has no adjustment other than a wash-sale loss. That matches the
  proposition ("beyond covered sales and code W").
  `test_the_in_class_question_asks_exactly_the_proposition` pins the
  wording to the bundle.
- **B2.** `test_collision_order_backtracking_and_duplicate_declared_id_boundary`
  is marked `live`, with its measured reason: 1.8 s locally and 3.9 s
  in CI. The budget is unchanged.
- **S1.** Lines 3 and 10 now `choose` on a count of their own sales.
  Each "a sale is recorded" test is a count, not a subtotal. So when a
  sale of the other term fails its own checks, the line stays at zero
  (`c_code_w_on_gain`, `f_holding_mismatch`, `d3_b_code_w_on_gain`).
  Two orderings keep the page honest:
  - The counts come before the answers. A count over a family that no
    answer confirms blocks on that family's closure, so every stale or
    missing answer is still asked again, now on the line's own block.
  - No count sits in an `any` ahead of an arm that reads an input
    question. So an answered question is never asked beside a closure.

  A line with no sale of its own no longer asks the new in-class
  question. On the ten returns that asked it, answering it could not
  admit the return (review N2). One of them is `boundary_no_without_member`;
  its test now pins that the question is not asked.
- **S2.** Each term's amounts-agree rule also requires that no sale of
  the other term is recorded for the same sale entity. One sale
  recorded as both box C and box F (`c_and_f_same_sale`) blocks both
  amount checks.
- **S3.** The live projection now pins two more things for each case:
  - the reason sentences of each blocked Schedule D line;
  - the (disposition, code, missing) of the rows for lines 2, 3, 9 and
    10 and the four amount checks.

  Review Q5's four exact duplicates (`m_c_no_yes`, `m_b_yes_no`,
  `m_no_no`, `m_no_unanswered`) are dropped by name. Their projections
  are still the same as the cases they duplicate. The two near
  duplicates differ only in answer order, so they are not exact
  duplicates and stay. `late_member_after_no`'s projection differs from
  `t1_stage1`'s. `late_member_reanswered_yes`'s equals `t1_stage4`'s.
- **S4.** Every v80 admission `any` that holds the guarded arm now reads
  it before the ADR-0061 Path B answer: lines 3 and 10, line 1a v5,
  line 8a v6 and the preferential base v8. On a box C or F return with
  Path B unanswered, lines 3 and 10 compute
  (`c_loss_path_b_unanswered` −6000, `f_gain_path_b_unanswered` 4000).
  A v79 return answers the new question "no" and reads Path B as
  before. No pinned case changes.
- **N1.** Form 8949 attachment v4 and Schedule D attachment v8 now carry
  their own version in the title, and name boxes C and F and lines 3
  and 10.
- **New limits.** These are pinned as they behave and parked with
  Decisions 4 and 6:
  - *Path B unanswered (S4).* The preferential base and both
    attachments require Path B through their own dependency set
    whenever Schedule D has activity and Form 8949 is "no". So line 7a
    and the Form 1040 still block, with no question, as on v79 for
    boxes B and E. Removing that requirement would change when the
    ADR-0061 pair is required. This repair does not do that.
  - *A late sale after a "yes" (S2).* In `q2_late_yes_stale`, a box C
    sale is recorded after a "yes" that a box F sale backs. The box F
    amount check now needs the box C family confirmed, so it blocks on
    that closure. The page cannot trace a per-sale check to its closure
    question, so it no longer asks the no-1099-B question again. Both
    lines show their blocked text, and answering "yes" again publishes.
- **Track 0 harness rerun** (`track0.py`, source ref (removed at closeout)):
  - Every hand value holds. The only mismatch is the expected
    `d3_b_orphan_basis` rejection, unchanged.
  - The 50 v79 returns on v80 differ from v79 in Form 1040 only for the
    same ten accepted blocks.
  - `code_w_on_gain` is now identical to v79 (line 7 zero).
  - The decided-design runs are unchanged.
- **Checks:**
  - `pytest -m "not live"`: 1694 passed, 8 skipped.
  - Full `pytest`: 4571 passed, 24 skipped, 0 failed.
  - `python3 -m mypy`: no issues in 467 files.
