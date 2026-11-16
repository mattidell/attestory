<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "page-alerts",
  "status": "Open 2026-11-16. P0 done. Track 0 recorded. Matrix PASS and late-member PASS; the two SSA rows are case artifacts.",
  "scope": [
    "a saved citation-walk page for a return that computes shows no safe-render alert for Form 1040 line 6c or the Schedule 1 top entry",
    "line 6c is drawn in words a filer can read whether or not the election is made, and the Schedule 1 top entry shows where its amount comes from",
    "every recorded return computes the same numbers"
  ],
  "non_goals": [
    "no change to any number, required answer or refusal code",
    "no engine, schema, projection or kernel change; a page change only if P0 shows content cannot clear an alert, and then only after the foreman decides",
    "repeated shared questions on the page belong to the blocked-sale-pages milestone",
    "one section per line 12d box stays an owner page-design decision"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/page-alerts.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/page-alerts.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/page-alerts.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/page-alerts.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Saved Pages Without Alerts on Line 6c and Schedule 1 (2025)

Milestone key: page-alerts.
Branch: milestone/page-alerts-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-16.
Starting point: main at `0ba934b1` (core v91, registry v89, release v89).

## What we are trying to accomplish

The saved citation-walk page puts a safe-render alert where it cannot
draw a field. Two alerts were parked from observed pages: Form 1040 line
6c supplies `not_elected`, which the categorical renderer does not draw,
and the Schedule 1 top-entry field has no citation. A filer reading a
correct return sees warnings that mean nothing to them. The useful
outcome is that a computing return's saved page shows neither alert and
shows something true and readable in their place.

## What we know

- The parked item (sale-page-observation, cores v79 and v80): both
  alerts showed on the observed returns.
- line12d-boxes (core v90) taught the page to draw `not_checked` as "not
  checked"; line 6d's alert cleared and its roadmap entry says line 6c's
  `not_elected` alert stays.
- box4-amount-asked closed on P0 because its parked finding did not
  reproduce. These two alerts were last observed several cores ago.

**What we do not know.** Whether either alert still shows on core v91 and
on which returns; which other alerts a computing return's saved page
shows; whether a content successor can clear each (line 6c supplying a
value the page draws; a citation for the top entry) or the page must
change; whether line 6c's words for "not elected" would be true under
`not_checked`.

## Actions the team will take

1. **P0: measure and design** on v91 and a scratch v92.
2. **Decide.**
3. **Track 0 adversarial closure.**
4. **Track 1: build.**
5. **Close.** Review, repair, exact-head CI, retrospective, roadmap.

## Cases that will shape the design

- A wages-only return; a return with Social Security benefits and line
  6c not elected; one with the election made, if the published content
  reaches it.
- A return with a Schedule 1 top entry (Form 1099-K, gambling winnings)
  and one with no Schedule 1.
- The line12d-boxes Track 0 browser cases (alerts must not return).
- Every recorded return earlier milestones replay.

## P0 result

Both parked alerts reproduce on published core v91. Every saturated recorded
return would draw line 6c's missing-instruction alert (`not_elected`) and the
Schedule 1 top entry's missing-citation alert (closure-backed zero). No other
safe-render alert appeared. Scratch core v92, content successors only, draws
"not checked" when the election was not made and draws the top-entry amount
with a citation. The twelve plan pages then show no safe-render alert. When
the election is made the page still says "Not applicable." The recorded
replay of v91 against v92 classified all 775 lists identical (1344.95
seconds, 9 workers): no number changed and no return newly asked a question.
Recommendation: adopt the content successors. The elected-state wording is a
foreman decision. Evidence:
`docs/phases/engine-breadth/milestones/page-alerts-evidence/p0.md`.

## Decisions

Foreman, 2026-11-16, on P0 (`page-alerts-evidence/p0.md`), under the
owner's standing grant to apply recommended choices; the owner may
reverse any of them before merge.

1. **Content successors, no page change.** Line 6c: `rule.form1040-line6c`
   v2 publishes `not_checked` and `form1040.line-6c` v2 renders it.
   Schedule 1: a new citation `citation.schedule1.top-entry` v1 and
   `schedule1.top-entry.form-field` v2 carrying it. The page and the
   projection stay as published.
2. **Core v92, registry v90, release v90.**
3. **The elected state is in scope if it costs no question.** On v91 and
   on the P0 scratch a return that made the lump-sum election shows line
   6c as "Not applicable.", which is false. Track 0 prototypes a
   `checked` sibling on the line 6d pattern. It is built if no recorded
   return is newly asked a question and no field shows a question twice;
   otherwise it is parked with the measurement.
4. **The new citation must be checkable.** Its locator and words come
   from the 2025 Schedule 1 instructions in the local sources. If the
   local sources do not hold the passage, Track 0 says so and the
   citation names only what they do hold.
5. **The citation button's label is measured, not assumed.** P0 saw the
   raw citation id on the button. Track 0 compares with the buttons other
   fields draw; a new or newly shown button reads as theirs do.

Track 0 is chartered (`docs/reviews/page-alerts/charter-track0.md`).

## Track 0 adversarial closure

Evidence: `page-alerts-evidence/track0-closure.md` and
`page-alerts-evidence/track0-ssa-guard.json`. The empty/nonempty matrix and
the late-member lifecycle are PASS. The two SSA rows are case artifacts of
the harness reconfirm. This track does not change the page, a schema, the
projection, or the kernel, and it does not change `rule.form1040-line6a`.

- Authority-lifecycle table: PASS — `page-alerts-evidence/track0-authority.json`. Five design claims, 0 failing case ids. The election fact, `social-security.line6c-indicator`, `social-security.line6c-checked`, `schedule1.top-entry`, and `citation.schedule1.top-entry` each have a built disposition path. The SSA-1099 closure measurements sit beside that table and are settled as case artifacts in `page-alerts-evidence/track0-ssa-guard.json`.
- Empty/nonempty authority matrix: PASS — `page-alerts-evidence/track0-matrix.json`. 8 rows. Failing case ids: none. The harness-reconfirmed `ssa-closure-missing` page drew line 6a computed_zero 0 because `demo.fk.ssa.reconfirm` answered the closure. The wage return with that closure left on `demo.ssa.h0` blocks, and the page asks the SSA-1099 closure question. The Form 1099-K top entry blocks when its closure is removed.
- Late-member lifecycle: PASS — `page-alerts-evidence/track0-late.json`. Two family traces. Failing case ids: none. The harness-reconfirmed `ssa-member-before-reclose` page published line 6a 12000 from `demo.fk.ssa.reconfirm` at `demo.ssa.handover.h75`. The same member list with reconfirm left off blocks `SOURCE_SET_UNCLOSED`. Form 1099-K refuses the unreclosed member with `FindingModelError` and publishes 880 after reclose.
- Neighboring capability dependency diff: PASS — `page-alerts-evidence/track0-neighbour.json`. 775 identical against v92 (1344.95 seconds, 9 workers) and 775 identical against the checked sibling (1335.47 seconds, 9 workers). 0 changes. Failing case ids: none.
- Reused-claim semantic/lifecycle equivalence: PASS — `page-alerts-evidence/track0-reuse.json`. 0 failing case ids. The successors add no read, pin, or scheduling dependency. v90 and v79 still draw what they drew, alerts included.
- Integration surface: PASS — `page-alerts-evidence/track0-surface.json` and `track0-census-sibling.json`. 12 plan pages with 0 alerts; 6 line 12d cases draw all 8 checkbox fields with 0 alerts; 691 of 691 computing returns have no alert. The computing census took 650.3 seconds with 9 workers. A later resume of the completed part file took 0.0 seconds. Bindings are exactly one disposition row per symbol for line 6c, the checked sibling, and the Schedule 1 top entry. Failing case ids of this row: none. `neighbor_failures` is empty.
- Checked sibling: build. No recorded return is newly asked a question, and no field shows a question twice. The six unanswered cells list the lump-sum question on both line 6c sections. Replay class: identical, 775.
- Citation passage: in the local sources, `i1040gi-2025.txt:6366`, under the heading at `i1040gi-2025.txt:6338`. "If, for tax year 2025, you received a Form(s) 1099-K that shows payments that were included in error (for example, money for gifts or reimbursements) or for personal items that you sold at a loss (for example, an old refrigerator), enter the amount that was included in error or for personal items sold at a loss in the entry space at the top of Schedule 1." Field corrections: none. The successor did not change.
- Known limitations affecting correctness: the two SSA rows are case artifacts. `ssa-closure-missing` published line 6a computed zero 0 because the harness asserted `demo.fk.ssa.reconfirm` at the handover horizon after the strip. `ssa-member-before-reclose` published 12000 from that same assertion; the member transition left `demo.ssa.closure` on `demo.ssa.h0`. The corrected v91 runs block, and the page asks the SSA-1099 closure question. They are not a page-alert content edit, and this track does not change `rule.form1040-line6a`.

## Disposition

Foreman, 2026-11-16, on Track 0 and its follow-up.

6. **Track 0 is closed: every table PASS.** The two Social Security rows
   first reported FAIL were sent back and settled as case artifacts: the
   evidence harness reconfirmed the SSA-1099 closure after the case
   removed it. Built the way a filer records it, line 6a blocks and asks
   the closure question, as `tests/test_collect_closure.py` asserts.
7. **The checked sibling is built** (Decision 3's condition holds: 775
   identical, no new question, no field with a question twice). One core
   v92 carries all six citizens.
8. **Citation buttons keep their labels.** Every button on the page
   shows `id@version`; the two new ones match. A readable label is a
   projection or page change and is parked.
9. **Parked, to reproduce before any milestone opens on it:** on a
   return with a benefit statement Track 0 saw line 6b blocked
   `DEPENDENCY_ABSENT` with no reason sentence. The cases did not answer
   the worksheet's scope questions, so this may be another case shape.

Track 1 is chartered (`docs/reviews/page-alerts/charter-track1.md`).

## Track 1 result

Published core v92, registry v90, and release v90. Six citizens: `rule.form1040-line6c` v2 and `form1040.line-6c` v2 succeed v1; `citation.schedule1.top-entry` v1 and `rule.form1040-line6c-checked` v1 and `form1040.line-6c-checked` v1 are new; `schedule1.top-entry.form-field` v2 succeeds v1. The publishing rule for the top entry stays v3. v91 and earlier package bytes are unchanged. The loader entries for v92 carry v91's covered-flag map and companion declaration.

Replay of the 775 recorded lists, published v91 against published v92, 9 workers: 775 identical, 0 changes, 1354.6 seconds. Evidence: `page-alerts-evidence/track1-replay.json`.

Alert census on published v92, 9 workers: 691 computing returns, 0 with an alert, 84 errors, 650.1 seconds. Evidence: `page-alerts-evidence/track1-census.json`.

Checks: `pytest` on `tests/test_page_alerts_v92.py`, `tests/test_page_alerts_v92_package.py`, and `tests/test_noncovered_sales_v78_switch.py` — 13 passed in 45.55s. `pytest -m "not live"` — 1811 passed, 8 skipped, 4303 subtests passed in 16.11s. `python3 -m mypy` — Success: no issues found in 503 source files. `python3 tools/envelope_scan.py --range github/main..HEAD` — exit 0, no findings. The full suite remains the CI `verify` gate.

Deviation: the Track 0 checked field says "The checked lump-sum election disposition does not apply." The not-checked successor in the P0 prototype keeps "line 6c disposition is inapplicable for the current class." The saved page still draws the line value "Not applicable." from its own text, and this track does not edit the page. Both fields' `guard_inapplicable` explain is "This line 6c box does not apply to this return, or the box is the other checked/not-checked state." Every other byte of the six citizens matches the P0 prototype or the Track 0 sibling. Line 6b's empty blocked reason and the citation button labels stay parked (Decisions 8 and 9).
