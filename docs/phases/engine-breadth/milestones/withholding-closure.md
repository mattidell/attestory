<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "withholding-closure",
  "status": "Closed. On core v61 line 25b, and every line behind it, waits until each Form 1099 withholding family is confirmed complete; a complete return computes exactly as on v60. Earlier packages keep the gap.",
  "scope": [
    "a withholding amount that is not known to be complete stops line 25 and every line behind it, on a successor core package",
    "a return whose withholding is complete keeps every result it has today",
    "cover every withholding family the engine reads: Form W-2 box 2, Forms 1099-INT, 1099-DIV, 1099-R and 1099-G box 4, Form SSA-1099 box 6",
    "keep earlier packages, saved presentations and their goldens unchanged"
  ],
  "non_goals": [
    "no new withholding source: no Form 1099-K box 4 (SC-R1), no Form W-2G or other line 25c source, no line 26",
    "no change to what a complete withholding family computes",
    "no change to income families or their closure",
    "no edit to any published schema, adopted package, parameter or rule version; only successors",
    "no new schema, expression operation or engine change unless P0 shows one is required, and then only after owner direction"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/milestone-retrospectives/2026-10-28-form-1099-withholding.md",
      "docs/milestone-retrospectives/2026-10-29-form-1099-k-income.md",
      "docs/phases/engine-breadth/milestones/withholding-closure.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/withholding-closure.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/withholding-closure.md"
    ],
    "new_milestone": [
      "docs/milestone-retrospectives/2026-10-30-withholding-closure.md",
      "docs/phases/engine-breadth/milestones/withholding-closure.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-10-30-withholding-closure.md"
}
-->

# Withholding Waits for Every Statement (2025)

Milestone key: withholding-closure.
Branch: milestone/withholding-closure-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-10-30.
Starting point: `github/main` at `045211c6` (PRs #230, #231 and #232 merged;
core v60, registry v58, release v58 are the latest). PR #229 is open and
touches explanation and presentation code, not tax content.

## What we are trying to accomplish

The form-1099-withholding review found, and parked, this: *a filer who
records one 1099-G's withholding and not another's gets a smaller line 25b
with no block. Every withholding family already behaves this way.* A smaller
line 25b means a smaller refund or a larger amount owed, published as if it
were the answer.

The Form 1099-K milestone fixed the same kind of gap for income: a value the
engine cannot know is complete now stops the bottom line instead of being
left out. This milestone applies that rule to payments. The useful outcome: a
return whose withholding is not known to be complete names what is missing
and does not publish lines 25 through 37; a return whose withholding is
complete computes exactly as on v60.

## What we know

- **Engine (core v60).** `tax.us.2025.rule.form1040-line25b` v2 adds five
  subtotals (Forms 1099-INT, 1099-DIV, 1099-R, 1099-G box 4 and SSA-1099
  box 6). Each subtotal `collect`s one source set, such as
  `tax.us.2025.f1099g.b4`. Line 25a reads Form W-2 box 2 the same way
  (to confirm in P0).
- **Closure answers exist.** Core v59 asks that every 1099-G box 4 and
  every SSA-1099 box 6 amount is recorded.
- **What we do not know.** Which incompleteness actually reaches the line:
  a statement recorded without its withholding answer, a family whose
  closure is unanswered, or both; whether the `collect` waits for closure
  or sums whatever is recorded; whether the W-2 family behaves the same;
  and whether the fix is content-only (successor subtotal or line 25 rules)
  or needs an engine change.

## Actions the team will take

1. **P0 — trace and design.** Reproduce the gap through
   `live_coordinate_run` on v60 for each family and each cause. Trace from
   content how each subtotal decides to publish. Design the smallest
   successor set that blocks line 25 (and everything behind it) while any
   withholding family is incomplete, and leaves complete returns
   byte-identical. Hand-computed cases. No content changes. If the fix needs
   an engine, schema or operation change, stop and report.
2. **Decide.** The block point and the successors.
3. **Track 1 — block.** The successor rules; core v61, registry v59 and
   release v59 built with `tools/package_successor.py`; cases through the
   real coordinator; v60 and earlier pinned to today's behaviour.
4. **Close.** Fresh-reader review, full lane and mypy before ready,
   exact-head CI, retrospective, roadmap and parked list.

## Cases that will shape the design

- Two Forms 1099-G, both with box 4 withholding; only one amount recorded.
- A Form 1099-G recorded without its box 4 answer.
- A family whose closure question is unanswered, for each of the six
  families.
- A complete return with withholding in every family: unchanged from v60,
  byte for byte.
- A return with no withholding anywhere: unchanged.
- A joint return with withholding for each spouse, one spouse incomplete.

## Process

Dispatch is to Sonnet 5.5 Agent sub-agents (owner direction, 2026-10-30).
P0 and Track 1 are builder units; the close is a fresh-reader review. Each
unit commits on this branch as it goes. Stop means stop.

## P0 result

P0 is in [trace and design](withholding-closure-evidence/p0-trace-and-design.md),
with the probe and its output beside it.

- **The gap is real for five families and absent for one.** On v60, a
  recorded Form 1099-INT, 1099-DIV, 1099-R or 1099-G box 4 amount, or an
  SSA-1099 box 6 amount, counts on line 25b while that family's closure is
  unanswered or stale. With 600 of 1,000 of 1099-G withholding recorded, the
  refund publishes as 25 instead of 425. Form W-2 box 2 already blocks in
  every cause, so line 25a needs no change.
- **Why.** `collect` (`packages/derivation/evaluator.py`, `evaluate`) reads
  closure only when its set is empty; with any member it sums what is
  present. `require_closed` reads closure always. Line 2b v6 already guards
  its subtotals with `all` of `require_closed`; line 25b does not.
- **Design.** One successor: `tax.us.2025.rule.form1040-line25b` v2 → v3,
  same schema, `when` becomes `all` of `require_closed` over the five
  withholding source sets. Lines 25d and 33 through 37 wait behind it; 24 and
  25a still publish. No new question on adoption. A prototype outside the
  repository matched v60 on every complete case across 55 paired runs.
- **Residual.** A closure attested true over an amount never recorded still
  publishes the smaller number. The engine cannot see it without asking every
  statement for its box 4 answer, which would change complete returns.

## Decisions

Foreman, 2026-10-30, on P0's recommendations:

1. **Block at line 25b alone** (one citizen). It names one unclosed family at
   a time; per-subtotal successors would name all of them at once for five
   more citizens. Not worth it here.
2. **The residual is parked**, not designed.
3. **The v61 entry in `domain_package_companion_declarations()`
   (`packages/tax/loader.py`) is in scope.** It is a per-package loader
   registration, not an engine change; the 1099-K milestone made the same v60
   entry.
4. **Parked engine question:** 49 rules `collect` without a `require_closed`
   guard. Whether any of them publish a partial income sum is not surveyed
   here.

## Tracks

1. **Track 1 — block.** Line 25b v3; core v61, registry v59, release v59 with
   `tools/package_successor.py`; the v61 companion entry; cases through the
   real coordinator; v60 pinned.

## Review dispositions

Fresh-reader review of P0 and Track 1: no required findings. The reviewer
ran eight further incomplete cases on v61 (closure attested false; a later
false closure over the same horizon; a member removed after closure; an
amount outside the family with the closure unanswered), all blocked, and five
further complete returns, all identical to v60 across every published value.

1. *The v61 companion entry has no test naming it* (note). The entry is
   load-bearing (without it a v61 1099-G return is refused at recording).
   Fixed: a test pins that v61 shares v60's declaration.
2. *Only one pair of the guard's naming order was pinned* (recommended).
   Fixed: a test closes the five families in turn and checks each is named
   in guard order.
3. *The block names a family id, not the question to answer* (note). The
   id is the family whose existing closure question the filer answers; the
   line 25b form-field text is the generic "missing or not yet closed", as
   for line 2b. Kept; parked as a presentation follow-up.
4. *No v61 adoption file* (decision check). Confirmed: the v60 one is used
   by one test only.

## Execution record

- Dispatch was to Sonnet 5.5 Agent sub-agents (owner direction).
  P0 took about 30 minutes and found the cause in the evaluator; Track 1
  took about 5 minutes with `tools/package_successor.py`, its first use in
  a milestone; the review took about 9 minutes.
- The foreman added the two review tests.

## Outcome

On core v61, a recorded withholding amount on Form 1099-INT, 1099-DIV,
1099-R or 1099-G box 4, or SSA-1099 box 6, does not reach line 25b until its
family is confirmed complete at the current horizon. Until then line 25b
blocks `SOURCE_SET_UNCLOSED` naming the family, and lines 25d and 33 through
37 do not publish; lines 24 and 25a do. A complete return, a closed-empty
family and a return with no withholding publish exactly v60's values. Core
v60 and earlier are unchanged. One successor rule; no engine or schema
change; no new question.
