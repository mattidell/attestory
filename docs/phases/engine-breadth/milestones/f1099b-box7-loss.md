<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f1099b-box7-loss",
  "status": "Open. P0 measured on scratch core v84. Decisions are in the P0 result.",
  "scope": [
    "a Form 1099-B statement whose box 7 is checked refuses only where the box 7 rule can change the result: a sale from that statement reported at a loss",
    "a box 7 statement whose sales are all gains or zero computes, and no loss from a box 7 statement is ever published",
    "every return core v83 computes correctly computes the same on the successor, and earlier cores render byte-identically"
  ],
  "non_goals": [
    "no computation of the disallowed loss itself (reportable change in control or capital structure)",
    "no box 13 bartering, no other Form 1099-B boxes and no new Form 8949 codes",
    "no edit to packages/kernel/",
    "no edit to any published schema, adopted package or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/milestone-retrospectives/2026-11-10-f1099b-backup-withholding.md",
      "docs/milestone-retrospectives/2026-11-09-sale-family-audit.md",
      "docs/phases/engine-breadth/milestones/f1099b-box7-loss.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/f1099b-box7-loss.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/f1099b-box7-loss.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/f1099b-box7-loss.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Form 1099-B Box 7 Read Only Beside a Loss (2025)

Milestone key: f1099b-box7-loss.
Branch: milestone/f1099b-box7-loss-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-10.
Starting point: `github/main` at `66b8cc81` (PR #266, core v83).

## What we are trying to accomplish

Form 1099-B box 7 ("loss not allowed based on amount in 1d") tells the
filer a loss on that sale may not be taken from the reported proceeds. On
core v83 a box 7 "yes" on any statement refuses the return, even when every
sale from that statement is a gain, where box 7 changes nothing. The
useful outcome is a core v84 that refuses only where box 7 can matter, and
computes the rest.

## What we know

- Core v82 asks box 7 once per recorded Form 1099-B statement
  (`input-question.f1099b-statement-box7-loss-not-allowed.json`) and
  refuses on any "yes" (sale-family-audit Decision 4; accepted as an
  over-refusal that never publishes a wrong number).
- Box 7 is a statement answer; gains and losses are per sale, and each
  sale family carries its own proceeds, basis and adjustment amounts.
- **What we do not know.**
  - What the 2025 Form 8949 and Form 1099-B instructions require when box
    7 is checked: whether a gain is reported as usual, and whether "loss"
    means the sale's column (h) after adjustments or proceeds below basis.
  - Whether content can test "this statement has a sale at a loss" with
    the existing operators, across all eight sale families, without a
    closure the filer was never asked.
  - Whether a box 7 sale can carry a wash or other adjustment that turns
    a loss into zero, and what box 7 then means.

## Actions the team will take

1. **P0: measure and design.** Table every rule that reads the box 7
   answer on core v83 and every sale amount a loss test would read. Probe
   v83 through `live_coordinate_run`. Compute by hand from the 2025
   instructions. Prototype a content-only scratch core v84. Stop and
   report if the fix needs an engine, schema or recording change.
2. **Decide.** The loss test and the refusal's true reason.
3. **Track 0 adversarial closure.** The six artifacts over the fix.
4. **Track 1: build.** Core v84 and its registry and release, with live
   and package tests.
5. **Close.** Fresh-reader review, repair, exact-head CI, retrospective,
   roadmap. Merge on green verify (owner standing approval, 2026-11-07).

## Cases that will shape the design

- Box 7 "yes" on a statement with one gain sale; one loss sale; one sale
  at exactly zero; a gain and a loss on both terms.
- A loss sale with a wash adjustment (code W) that brings column (h) to
  zero.
- Box 7 "yes" on one statement and a loss on another statement.
- Box 7 unanswered beside a gain, and beside a loss.
- A sale removed after box 7 was answered; a sale changed from gain to
  loss.
- Every return core v83 computes: identical on v84, unless it was refused
  by a box 7 "yes" and now computes.

## Process

Dispatch is through the grok CLI (owner, 2026-11-09). Each unit commits on
this branch as it goes. Track 0 hand values come from the instructions,
never from what a prototype publishes (f1099b-backup-withholding
retrospective).

## P0 result

Evidence: `docs/phases/engine-breadth/milestones/f1099b-box7-loss-evidence/p0.md`.
The table is `box7-table.json`. The 2025 quotes and checksums are `law.json`.
The twenty design cases are `probe-output-v83.json` and `probe-output-v84.json`.
The scratch successor is `prototype.py` with `prototype-build.json`. The 298
recorded v83 runs are `rerun-output.json`.

Core v83's only reader of the box 7 answer is `rule.schedule-d-line16` v3.
Any yes blocks line 16 while a sale count is above zero, including a gain or
a zero. No loader entry reads the fact.

The scratch core v84 is content only: eight per-sale verdicts, eight loss
checks, line 16 v4 equal to line 7 plus line 15, and a narrowed form-field
explanation. The question is unchanged. A loss is column (h) strictly below
zero. All twenty probes match that hand on v84. Of the 298 recorded runs, 275
are identical and 23 stay blocked with the sale-count symbols dropped from
line 16's missing list. No published value changed.

Recommendation: adopt that shape. No engine, schema, expression, or
recording-surface change was required.

Decisions:

1. Refuse line 16 on a checked statement with column (h) below zero, rather than computing code L so column (h) is zero.
2. Keep the existing box 7 question on every statement that has a sale.
3. The form-field explanation is the yes-plus-loss sentence. The covered-flag map stays as it is.
4. A gain and a loss on the same checked statement refuse the whole line.
5. Whether line 16 v4 should keep requiring the eight sale-count symbols so the 23 already-blocked rows stay identical.

## Decisions

Foreman, 2026-11-10, on P0. The owner's direction is to proceed on the
recommended choice; the owner adjusts after. Foreman check: every case id
the P0 table cites is in both probe outputs, and the rerun used the
recorded answers.

1. **Refuse, do not adjust.** A sale on a box 7 "yes" statement whose
   column (h) is below zero blocks Schedule D line 16 with a true reason
   and no question. The Schedule D Example 2 code L adjustment (column (h)
   to zero) is not computed; it stays parked. A gain, a zero, and a wash
   to zero are not losses.
2. **The box 7 question is unchanged** and still asked of every statement
   with a sale.
3. **The refusal's reason is the line 16 field explanation**; the
   covered-flag refusal map is unchanged.
4. **One loss on a checked statement refuses the whole of line 16**,
   including that statement's gains. A loss on a statement answered "no"
   publishes, beside a "yes" statement with only gains.
5. **Line 16 v4 keeps requiring the eight sale-count symbols**, so every
   recorded v83 return is identical on v84 (the 23 blocked rows keep their
   missing list). The change stays limited to box 7.
6. **Verdict per sale, check per family**, as prototyped: eight derived
   per-sale verdicts and eight family checks. Track 0 tries whether fewer
   members do the same, but the prototype shape is acceptable.

## Track 0 adversarial closure

Foreman, 2026-11-10: accepted. Six rows PASS with no counterexample;
hand values come from `probe.hand_return`, computed from the
instructions. The 16-rule shape stays (the 8-rule trial fails). Track 1
is chartered in docs/reviews/f1099b-box7-loss/charter-track1.md.

- Authority-lifecycle table: PASS — `track0-authority.json` (21 cases). A yes beside a loss blocks line 16 with the family check missing nothing and asks no question (`alc_covered-st_loss` and the other seven `alc_*_loss` cases). A yes beside a gain publishes the hand, including code B (`alc_code-b-st_gain`, `alc_code-b-lt_gain`). Two statements do not share an answer (`alc_statement_scope`, line 16 is 600). One statement with a gain and a loss refuses the whole line (`alc_same_statement`).
- Empty/nonempty authority matrix: PASS — `track0-matrix.json` (49 cases). Closed empty publishes 0 (`m_closed_empty`). A missing per-family closure blocks that count (`m_absence_covered-st`). A missing grouped closure blocks both terms (`m_absence_noncovered-st`, `m_absence_code-b-st`). Yes beside a loss blocks on the check (`m_{family}_yes_loss`). Unanswered asks the box 7 question (`m_{family}_unanswered`).
- Late-member lifecycle: PASS — `track0-late.json`. Adding a loss drops the prior line 16 finding (`late_gain_then_loss`). Removing the loss publishes a new zero (`late_loss_removed`). Superseding yes with no clears the verdict (`late_yes_to_no`). A new unanswered statement drops the prior finding (`late_new_statement_unanswered`).
- Neighboring capability dependency diff: PASS — `track0-neighbour.json`. 298 recorded returns, live on v83 and live on scratch v84, 298 `identical`, 0 changes. The eight sale-count requirements stay. Each new check publishes 0 when box 7 has no work.
- Reused-claim semantic/lifecycle equivalence: PASS — `track0-reuse.json`. Lines 7 and 15 and the eight counts match v83 (`reuse_yes_gain`, `reuse_box7_no`, `reuse_no_sale`). The covered-flag sentence is unchanged (`reuse_covered_flag`). Only line 16's rule and form field move from v3 to v4.
- Integration surface: PASS — `track0-surface.json`. Bindings: line 21, Form 1040 line 7a, and the preferential base require line 16; the line 16 field binds it; Schedule D lines 17, 18, 19, 20, and 22 have no rule. Seven models, one disposition row each. Yes-loss shows the narrowed sentence and asks nothing (`surface_blocked_yes_loss`). Unanswered asks the box 7 question (`surface_blocked_unanswered`).
- Known limitations affecting correctness: none

The eight-verdict trial (`track0-smaller.json`, 8 new rules) fails closed-empty and one-family returns and is not adopted. Detail is in `f1099b-box7-loss-evidence/track0-closure.md`.

## Track 1 result

Published core `tax.us.2025.package.core-calculations` v84, registry v82, and release v82, from the decided design. The citizens are byte-identical to `prototype.artifacts()` with the smaller shape unset: seventeen adds (the verdict bundle, eight per-sale verdict rules, and eight family checks) and two replacements (Schedule D line 16 rule v3 to v4, and its form field v3 to v4). The v84 loader entry copies the v83 companion declaration and the v83 covered-flag refusal map, and adds no sale object or amount. The build stayed in content, the loader, the sale-fact audit, and tests.

**Decided cases.** `tests/test_f1099b_box7_loss_v84.py` runs 89 Track 0 coordinate runs on published core v84 through `live_coordinate_run` and the presentation model: authority 21, matrix 49, late 8 (four traces, two steps each), reuse 4, and surface 7. Reuse also runs those four act lists on published core v83. Hand values come from `probe.hand_return`. Each pin records Schedule D lines 1a through 16 and line 21, Form 1040 lines 7a, 15, 16, 24, 33, 34, and 37, each blocked line's reason sentences, and the blocked row's disposition, code, and missing. The fixture `tests/fixtures/f1099b_box7_loss_v84/expected.json` is 309,613 bytes and records those 89 cases. The module records the fixture write as 89 runs in 114.0 s with 6 workers.

**The 298 recorded v83 runs.** Compared in place with `tests/fixtures/f1099b_backup_withholding_v83/expected.json`. They were not copied into the new fixture. The 298 are 79 Track 0 pins, 213 returns (98 case, 88 v80, 27 neighbour), and 6 zero-sample restores. On published core v84, 298 identical and 0 diffs.

**Sale-fact audit.** On core v84 the box 7 answer is a value-side read of the eight verdict rules only. The eight family checks and line 16 v4 do not value-read it. On core v83 the only value-side reader is still line 16. The committed table is `sale-family-audit-evidence/tables-v84.json`.

**Checks.** `pytest -m "not live"`: 1756 passed, 8 skipped, 4225 subtests passed (17.10s). Full `pytest`, split into 22 shards and summed, each of the 5949 collected tests once: 5925 passed, 24 skipped, 8913 subtests passed, 0 failed. The shard walls sum to 3747.0 s. `python3 -m mypy`: no issues in 475 source files. `python3 tools/envelope_scan.py --range github/main..HEAD`: clean.

**Live module.** A full pass of the module is 391 coordinate runs: 89 on published v84, 4 reuse runs on published v83, and the 298 recorded runs. Item 4 ran that pass in four shards. The 80 Track 0 tests passed in 159.28 s. The 298 recorded tests passed in 451.44 s.

**Deviation.** `tests/test_noncovered_sales_v78_switch.py` now expects cores v79 through v84 to name the covered-flag refusal map. v84 names the same map as v83, and v79 through v83 are unchanged. `track0.py` `execute` takes an optional `extra_lines` so the live test can watch Schedule D lines 6, 13, and 14; the default is empty. Line 16 v4 still requires the eight sale counts and the eight box 7 loss checks, and its value does not read them (Decision 5). Those sixteen symbols are recorded in `tools/required_versus_read_allowlist.json`. Three returns in the live test are cast so mypy accepts them; the cast does not change the value. No kernel, derivation, or schema edit, and no recording change.

**Repair.** The yes-loss sentence is the line 16 blocked explanation. A selection reason is attached only from the field producer's selection, and line 16 v4 is a value rule whose eighteen requires stay (Decision 5). Emptying those requires so the rule could become a selection would be an engine change, so the explanation is a disjunction of the causes that can block the line. Reasons on a yes-loss stay empty, and the citation page still shows the generic remedy: contribute the missing dependency to unblock this line. The sentence the filer sees is: "Schedule D line 16 has no value yet because one of these is true: line 7 or line 15 is not ready, a sale count this line requires is not ready, a recorded Form 1099-B statement has no box 7 answer, or box 7 is checked and a sale on that statement is at a loss. This return does not compute a disallowed loss. Where that loss is the cause, the result changes if the broker reports the loss on a separate statement, or if box 7 is not checked." A presentation probe of all eight families on a yes-loss showed that sentence, an empty reason list, line 16 missing only that family's check, and the loss unpublished. An unanswered box 7 still asks the unchanged box 7 question.

The sale-fact audit now names each verdict rule, and one verdict that drops its value-side read of the box 7 answer fails the audit. The eight-id list stays. The closure note cites `conflict: refuse` and `paths` `minItems` 2 in `rule-artifact.v15`.

The live grid is 363 coordinate runs: 61 on published v84, 4 reuse runs on published v83, and the 298 recorded runs. The 61 are the 3 authority rows the matrix does not cover, the 49 matrix rows, both steps of each late trace, and the covered-flag reuse row. Twenty-eight v84 rows repeat a matrix act list, and that matrix run asserts each duplicate fixture row. The covered-flag v84 run remains, because that fixture row's act list and view are its own. Regenerating `tests/fixtures/f1099b_box7_loss_v84/expected.json` from the 61 runs took 86.2 s with 6 workers, kept all 89 cases, and left the file at 309,613 bytes.

`pytest -m "not live"`: 1757 passed, 8 skipped, 4225 subtests passed (17.19 s). Full `pytest`, split into 18 shards and summed, each of the 5925 collected tests once: 5901 passed, 24 skipped, 8913 subtests passed, 0 failed. The shard walls sum to 3576.0 s. `python3 -m mypy`: no issues in 475 source files. `python3 tools/envelope_scan.py --range github/main..HEAD`: clean. No kernel, derivation, or schema edit, and no recording change.

