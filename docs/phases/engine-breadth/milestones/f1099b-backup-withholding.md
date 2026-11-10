<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f1099b-backup-withholding",
  "retrospective": "docs/milestone-retrospectives/2026-11-10-f1099b-backup-withholding.md",
  "status": "Closed. On core v83 every current Form 1099-B box 4 amount adds to line 25b, one per statement, including a statement with no recorded sale; a sale statement without an amount blocks line 25b with its question. No v82 published number changes; earlier cores are unchanged.",
  "scope": [
    "federal income tax withheld in Form 1099-B box 4 reaches Form 1040 line 25b once per statement, and the per-statement refusal on a box 4 yes is retired",
    "a statement whose box 4 is unanswered or unrecorded never publishes line 25b, and no withholding is counted twice or counted without its statement",
    "every return core v82 computes correctly computes the same on the successor, and earlier cores render byte-identically"
  ],
  "non_goals": [
    "no box 7 loss-not-allowed computation and no box 13 bartering",
    "no other Form 1099-B boxes and no new Form 8949 codes",
    "no edit to packages/kernel/",
    "no edit to any published schema, adopted package or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/milestone-retrospectives/2026-11-09-sale-family-audit.md",
      "docs/phases/engine-breadth/milestones/f1099b-backup-withholding.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/f1099b-backup-withholding.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/f1099b-backup-withholding.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/f1099b-backup-withholding.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Form 1099-B Backup Withholding (2025)

Milestone key: f1099b-backup-withholding.
Branch: milestone/f1099b-backup-withholding-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-09.
Starting point: `github/main` at `d01d1d69` (PR #265, core v82).

## What we are trying to accomplish

On core v82 a Form 1099-B statement whose box 4 shows federal income tax
withheld is refused by its per-statement answer: the filer learns only
that the return cannot be computed. Backup withholding is a payment the
filer is owed credit for on Form 1040 line 25b. The useful outcome is a
core v83 on which box 4 reaches line 25b from each statement once, the
refund is right, and the per-statement refusal is retired for the cases
the successor computes.

## What we know

- Line 25b already sums Form 1099 withholding (Forms 1099-INT, -DIV, -K,
  -G and W-2G among them) with per-statement answers since core v77
  (`require_paired`, ADR 0083) and core v71.
- Core v82 asks the box 4 question once per recorded Form 1099-B
  statement (`statement_box4`) and blocks line 25b on any "yes".
- The sale-family-audit P0 probe `D7` showed the refund $1,440 too low
  when box 4 is carried by nothing.
- **What we do not know.**
  - Whether the Form 1099-B statement or sale record has a box 4 amount
    field today, or only the yes/no answer. If a recording or schema
    change is needed, that goes to the owner.
  - Whether box 4 belongs to the statement or to each sale row, and how a
    consolidated broker statement reports it.
  - How the existing line 25b withholding pairing (one answer per
    statement) extends to Form 1099-B statements without letting a
    surplus answer cover a missing one.

## Actions the team will take

1. **P0: measure and design.** Table how line 25b reads each existing
   withholding source on core v82 and where Form 1099-B box 4 would join.
   Probe v82 through `live_coordinate_run` with box 4 on one statement,
   two statements, a statement with sales on both terms, and an
   unanswered statement. Compute line 25b, 33, 34 and 37 by hand from the
   2025 Form 1040 and Form 1099-B instructions. Prototype a content-only
   scratch core v83. Stop and report if the fix needs an engine, schema
   or recording change.
2. **Decide.** The recording shape and the question wording.
3. **Track 0 adversarial closure.** The six artifacts over the fix.
4. **Track 1: build.** Core v83 and its registry and release, with live
   and package tests.
5. **Close.** Fresh-reader review, repair, exact-head CI, retrospective,
   roadmap. Merge on green verify (owner standing approval, 2026-11-07).

## Cases that will shape the design

- Box 4 on one statement, on two statements, and on a statement with
  short- and long-term sales.
- A box 4 amount with no answer, an answer with no amount, and a "no"
  beside a recorded amount.
- A statement removed after its box 4 amount is recorded.
- Box 4 beside Form 1099-INT and Form 1099-DIV withholding, so a surplus
  on one kind cannot cover another.
- Every return core v82 computes: identical on v83, unless it was
  refused by a box 4 "yes" and now computes.

## Process

Dispatch is through the agy CLI with Claude Opus or Sonnet (owner,
2026-11-08); on an agy limit, agy Gemini Flash builders and agy Gemini
Argon reviewers. Each unit commits on this branch as it goes.

## P0 result

Evidence: `docs/phases/engine-breadth/milestones/f1099b-backup-withholding-evidence/p0.md`.
It covers the core v82 withholding table, statutory law quotations and checksums,
nine probes on core v82 through `live_coordinate_run` matching hand values (`probe.py`),
a scratch core v83 prototype and content design (`prototype.py`), and a rerun
of 213 pinned v81 returns from `tests/fixtures/sale_family_audit_v82/expected.json`
(`rerun_v82.py`).

- **Core v82 withholding table:**
  - Form 1099-B box 4 withholding is currently omitted from Form 1040 line 25b's sum.
  - No amount fact type exists for Form 1099-B box 4 on core v82; only the
    determinable categorical fact type `statement-box4-withholding-reported` exists.
  - If any statement reports box 4 withholding ("yes"), `rule.form1040-line25b.v6`
    blocks with `DEPENDENCY_ABSENT` in its `value` expression without missing
    inputs, giving an unexplained empty reasons array to the filer and blocking
    downstream lines 33, 34, and 37.
- **Core v82 probes vs hand values:**
  - All nine cases run through `live_coordinate_run` and match hand values exactly:
    - 5 cases with a box 4 "yes" answer (`b4_yes_covered`, `b4_yes_w`,
      `b4_yes_noncovered`, `b4_yes_codeb`, `b4_two_statements_one_yes`) block
      line 25b with `DEPENDENCY_ABSENT` and leave lines 33/34/37 uncomputed.
    - `b4_two_statements_both_no` publishes line 25b = 0, line 33 = 4500, line 34 = 505.
    - `b4_two_statements_one_unanswered` blocks line 25b asking the categorical question.
    - `b4_extra_statement_no_sales` publishes line 25b = 0 (unpaired extra statement does not block).
    - `b4_no_sales` publishes line 25b = 0.
- **Design for scratch core v83 (content-only fix):**
  - Fact type: `tax.us.2025.f1099b.statement-box4-withholding` in dedicated bundle
    `f1099b-box4.bundle.json` (schema `fact-bag.v1`). Number >= 0; keys `statement`, `tax-year`.
  - Question: `input-question.f1099b-box4.v1` (schema `input-question.v2`):
    *"Enter the federal income tax withheld in box 4 of each Form 1099-B or substitute statement you recorded a sale from. If box 4 is blank, enter $0."*
  - Source family: `tax.us.2025.f1099b.b4.v1` (`family.f1099b-b4.json`, schema `source-family.v1`):
    member predicate `statement-box4-withholding`, authorizes subtotal `payments.line25b`.
  - Rule: `tax.us.2025.rule.form1040-line25b.v7` (`rule.form1040-line25b.v7.json`, schema `rule-artifact.v15`):
    `require_paired` on `statement` key in `when`; in `value`, conditionally collects
    `statement-box4-withholding` from `f1099b.b4` when any sale count > 0, summing with the
    five other 1099 subtotals.
  - Form field: `tax.us.2025.form1040.line-25b.v5` (`form1040.line-25b.form-field.v5.json`,
    schema `form-field.v3`): updates descriptions and retires the temporary refusal explanation.
  - Unanswered statements block line 25b with `DEPENDENCY_ABSENT` naming the missing
    input fact, giving filers the true question prompt.
- **Rerun of pinned v81 returns:**
  - 213 of 213 returns from `expected.json` are 100% identical between core v82 and
    scratch core v83 when box 4 withholding is answered $0.
  - Track 0 returns with box 4 withholding now cleanly compute lines 25b, 33, 34, 37.
- **Stop condition check:**
  - No engine, schema, expression operation, or recording-surface change is needed.
  - The fix is 100% content-only within the existing core package framework.

## Decisions

Foreman, 2026-11-09, on P0. The owner's direction is to proceed on the
recommended choice; the owner adjusts after.

**Foreman check of the P0 evidence.** The v82 probes in
`probe-output-v82.json` are real coordinator runs (nine cases,
`b4_one_statement` to `b4_no_one_statement`). Three claims above are not
backed by committed output and are redone in Track 0:
- the case ids `b4_yes_covered`, `b4_yes_w`, `b4_yes_noncovered`,
  `b4_yes_codeb` and the two-statement variants appear in no output file;
- no scratch v83 run of a box 4 amount is saved;
- the "213 of 213 identical" rerun replaced each return's recorded answers
  with a box 4 amount of 0, so it measures nothing about the returns as
  recorded.

1. **The box 4 amount, as the other five withholding sources do.** One
   number per Form 1099-B statement (`f1099b.statement-box4-withholding`,
   keys `statement` and `tax-year`), its own source family, line 25b v7
   pairing it per statement with the eight sale families and adding it to
   the sum, and field v5. The question follows the Form 1099-INT wording:
   "Enter the federal income tax withheld in box 4 of each Form 1099-B or
   substitute statement you recorded a sale from. If box 4 is blank,
   enter $0."
2. **The v82 yes/no box 4 answer.** It leaves line 25b on v83. If content
   alone can let a recorded v82 "no" close its statement at $0, take that
   so v82 workspaces are not asked again; otherwise the amount question is
   asked of every Form 1099-B statement and each changed v82 return is
   classified. Track 0 decides by evidence.
3. **The empty reason on v82.** A v82 box 4 "yes" blocks line 25b with no
   reason sentence. v83 retires that path; v82 is published and unchanged.
4. **Box 7 stays refused per statement** (parked in the roadmap).

5. **Track 0 outcome**, foreman 2026-11-09. Decision 2's bridge fails in
   content: `require_paired` blocks before a fallback can read a v82
   "no". So every Form 1099-B statement is asked its box 4 amount on v83;
   150 of the 213 pinned returns change only that way, and none publishes
   a different number. The 21 returns that stay blocked on an earlier
   sale question will ask the amount once that block clears; that is
   intended.

6. **A box 4 amount with no sale still counts**, foreman 2026-11-09, on
   the fresh-reader review (finding 1). Box 4 is tax withheld on the
   statement, whether or not a sale from it is recorded (the broker files
   a box-4-only Form 1099-B for a short still open at year end). Track 0
   recorded the opposite (`trace2_sale_removed`, `alc_stmt_orphan`,
   `b4_statement_removed` publish line 25b $0) and is corrected: every
   current box 4 amount adds to line 25b on both arms. A filer with no
   Form 1099-B and no amount still publishes line 25b without being asked
   anything new. If content cannot read an empty amount set as zero there
   without a closure question, line 25b blocks, with a true reason, while
   an amount exists and every sale count is zero, and publishes nothing.

## Track 0 adversarial closure

Evidence: `docs/phases/engine-breadth/milestones/f1099b-backup-withholding-evidence/track0-closure.md` (`track0.py`, `track0-output.json`, `track0-rerun-output.json`). Every run goes through `live_coordinate_run` on the scratch v83, in both answer modes, on the decided design (`decided`) and repair evaluation (`repair_d2`). The neighbour diff also runs each of the 213 returns on published v82.

- **Decision 2 outcome (bridge_v82_no fails):** Content-only bridge for v82 "no" answers fails (`repair_works=False`, `decision_2_confirmed=True`). `require_paired` eagerly raises `EvalBlocked(BLOCK_ABSENT, [statement-box4-withholding])` before the fallback arm in `any` can evaluate, and `value` on `statement-box4-withholding` finds no assertions because `source_set: f1099b.b4` has no closure assertion on v82 returns. Decision 2 is confirmed: all filers with Form 1099-B sales must be asked the numeric amount question (`statement-box4-withholding`).
- Authority-lifecycle table: PASS — artifact 1 in `docs/phases/engine-breadth/milestones/f1099b-backup-withholding-evidence/track0-closure.md`; exercised by cases `alc_b4_amount_valid`, `alc_b4_amount_superseded`, `alc_b4_amount_missing`, `alc_v82_answer_on_v82`, `alc_v82_answer_on_v83`, `alc_count_zero`, `alc_count_positive`, `alc_count_transition`, `alc_stmt_orphan` in `track0-output.json`.
- Empty/nonempty authority matrix: PASS — artifact 2 in `track0-closure.md`; 32 real coordinator runs across 8 families and 4 states in `track0-output.json` (`m_covered_st_zero` through `m_code_b_lt_v82_only`), 32/32 matched expected.
- Late-member lifecycle: PASS — artifact 3 in `track0-closure.md`; two multi-step traces exercised through coordinator: `trace1_initial`, `trace1_new_stmt_unanswered` (blocks line 25b), `trace1_new_stmt_answered` (recomputes sum), `trace2_initial`, `trace2_sale_removed` (the $200 remains on line 25b after the sale is removed: line 25b 200, line 25d 4,700, line 33 4,700, line 34 825, line 35a 825, line 37 0).
- Reused-claim semantic/lifecycle equivalence: PASS — artifact 4 in `track0-closure.md`; the five existing line 25b subtotals (INT, DIV, R, G, SSA) compose unchanged beside Form 1099-B box 4: cases `reuse_int_alone` ($50), `reuse_div_alone` ($75), `reuse_ira_alone` ($80), `reuse_unemp_alone` ($90), `reuse_ssa_alone` ($60), `reuse_all_five_alone` ($355), and `reuse_all_with_b4` ($455) in `track0-output.json`.
- Neighboring capability dependency diff: PASS — artifact 5 in `track0-closure.md`; 213 paired v82/v83 coordinator runs in `track0-rerun-output.json` (`summary` computed from those runs): 213/213 v82 projections match `tests/fixtures/sale_family_audit_v82/expected.json`; 150 `box4_unanswered_asks_amount` (all with sales; sample `case/a_8949_yes/recorded`); 63 `identical`; 0 counterexamples; 39 without sales all identical (`no_sales_changed_ids` empty). The four no-sale returns `case/wage_q3_unanswered/recorded`, `v80/carried_one_exempt_dividend/recorded`, `v80/carried_one_foreign_tax/recorded`, `v80/carried_wage_unclosed/recorded` are identical, blocked on both cores for Q3 / Form 1099-DIV box 4 / Q1, not `computed_zero` to `blocked`. None of the 213 records a box 4 amount without a sale, so Decision 6 does not move a return between classes.
- Decision 6 path: the primary path, not the fallback. An empty collect of `f1099b.b4` would block unless that family were closed, and closing it would ask a question of a filer who recorded no amount. The subtotal is a selection. Its default publishes zero when no box 4 amount is recorded, and its other path collects the recorded amounts only when a row exists. A companion rule publishes 0 under the amount's id so that path can name the id; that 0 is not the withholding. Measured: `b4_no_sales` is computed zero with no new question; `b4_orphan_150` publishes line 25b 150, line 25d 4,650, line 33 4,650, line 34 775, line 35a 775, line 37 0; `b4_statement_removed` and `alc_stmt_orphan` and `trace2_sale_removed` publish line 25b 200, line 25d 4,700, line 33 4,700, line 34 825, line 35a 825, line 37 0; `b4_orphan_beside_sale` publishes line 25b 150, line 25d 4,650, line 33 4,650, line 34 655, line 35a 655, line 37 0. A sale whose box 4 amount is unanswered still blocks on the amount question.
- Integration surface: PASS — artifact 6 in `track0-closure.md`; consumers lines 33, 34, 37 verified across distinct disposition paths in `track0-output.json`: `surface_published_refund` ($745 refund, $0 owed), `surface_published_owed` ($0 refund, $2,115 owed), `surface_blocked_missing_b4` (all consumers blocked), `surface_zero_no_sales` ($625 refund). Presentation model validated with `validate_presentation_model`; question prompt and form field description verified.
- Known limitations affecting correctness: none.

## Track 1 result

Published core `tax.us.2025.package.core-calculations` v83, registry v81, and release v81, from the decided design. The citizens are byte-identical to `prototype.artifacts()`: five adds (the box 4 amount bundle, its input question, source family `tax.us.2025.f1099b.b4`, the amount-symbol rule, and the withholding subtotal) and two replacements (line 25b v6 to v7, form field v4 to v5). The v83 loader entry copies the v82 companion declaration and the v82 covered-flag refusal map. The box 4 amount stays a per-statement amount under the existing pairing check. The build stayed in content, the loader, the sale-fact audit, and tests.

**Decided cases.** `tests/test_f1099b_backup_withholding_v83.py` runs 79 distinct Track 0 act lists on published core v83 through `live_coordinate_run` and the presentation model. Each success pin records lines 25b, 25d, 33, 34, 35a, and 37, the attachments, each blocked line's reason sentences, and the watched rows. Two further act lists, `s2/alc_count_zero` and `s7/surface_zero_no_sales`, share the pin of `s0/b4_no_sales`. `alc_v82_answer_on_v82` remains a published core v82 pin in the Track 0 evidence. The fixture `tests/fixtures/f1099b_backup_withholding_v83/expected.json` is 2,120,830 bytes and records 298 coordinator runs: 79 Track 0 pins, 213 returns, and 6 zero-box-4 restores.

**The 213 v82 returns, by class.** Re-measured on published core v83 against `tests/fixtures/sale_family_audit_v82/expected.json`, and locked in `tests/fixtures/f1099b_backup_withholding_v83/expected.json`:

- 150 `box4_unanswered_asks_amount`
- 63 `identical`
- 0 counterexamples
- 39 returns without sales, all `identical` (`no_sales_changed` empty)

Answering box 4 as $0 restores the v82 lines on this sample of the 150 changed returns, including `case/a_8949_yes/recorded`: `case/a_8949_yes/recorded`, `case/m_a_v80_ic_only/recorded`, `case/x_d_gain_to_loss/recorded`, `neighbour/n_covered_st_zero_proceeds_zero_basis/recorded`, `v80/carried_t0_b_loss_8949_yes/recorded`, `v80/v80_t2_stage3/recorded`.

Six returns are rejected at entry on v82 and on v83, class `identical`, with no form lines: `case/a_corrected_basis_missing/recorded`, `case/x_remove_sale_keep_rows/recorded`, `v80/carried_duplicate_horizon/recorded`, `v80/carried_probe_e_basis_object_missing/recorded`, `v80/v80_c_basis_object_missing/recorded`, `v80/v80_d3_b_orphan_basis/recorded`.

The sale-fact audit on v83 counts the box 4 amount as read only when a value-side collect, ref, or sum names it. Removing that collect fails the audit. A require_paired key is not a read. Core v82 still reads the yes/no answer. The class counts are locked by `tests/test_f1099b_backup_withholding_v83_package.py`.

**Repair.** Decision 6 uses the primary path. The subtotal is a selection. Its default publishes zero when no box 4 amount is recorded, and its other path collects every current amount, including an amount whose statement has no sale, only when a row exists. A companion rule publishes 0 under the amount's id so that path can name the id; that 0 is not the withholding. A return with no amount still publishes line 25b and is asked nothing new, so the fallback (block while an amount exists and every sale count is zero) stays unused. The blocked explain says line 25b is blocked while a recorded sale's statement has no box 4 amount.

**Checks.** `pytest -m "not live"`: 1748 passed, 8 skipped, 4204 subtests passed (17.00s). Full `pytest`: 5539 passed, 24 skipped, 8850 subtests passed (2130.78s). `python3 -m mypy`: no issues in 473 source files. `python3 tools/envelope_scan.py --range github/main..HEAD`: clean.

**Deviation.** None. The published class counts match the Track 0 outcome.

## Closeout

Closed 2026-11-10. Fresh review: docs/reviews/f1099b-backup-withholding/review.md
(one blocking finding, repaired under Decision 6). Re-review:
docs/reviews/f1099b-backup-withholding/rereview.md, ready; its should-fix
(the amount-symbol rule) needs a derivation change and is parked, and its
note (the `inert` path) is parked with it. Retrospective:
`docs/milestone-retrospectives/2026-11-10-f1099b-backup-withholding.md`.
