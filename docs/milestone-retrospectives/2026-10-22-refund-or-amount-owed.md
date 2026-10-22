# Retrospective — Refund or Amount Owed: Finishing the 2025 Return

## Result

- **Every computed return now ends in a refund or an amount owed on core
  v52.** Form 1040 lines 23-38 are published one rule per line: total tax,
  withholding, estimated payments, total payments, the overpayment split
  between a refund and 2026 estimated tax, and the amount owed.
- **Withholding is recorded** from W-2 box 2 (line 25a) and Forms 1099-INT,
  1099-DIV and 1099-R box 4 (line 25b), each per statement and summed like
  W-2 box 1. Line 25a blocks unless every W-2 has a box 2 answer.
- **A return without foreign tax reaches line 22 without foreign-tax
  questions.** Before, line 20 required the direct foreign tax credit's
  election and about twenty eligibility answers on every return.
- **Five new questions**, the 2026 amount asked only when there is an
  overpayment. Taxes and credits the engine does not compute are declared
  absent, never assumed zero.
- No schema, expression operation or engine change. Earlier packages and
  their goldens are unchanged.

## What the evidence changed

- **A probe workaround was the finding.** P0's probe overrode the foreign tax
  credit election to reach line 22 and called the block "by design". From a
  person's side it was a wall of irrelevant questions in front of every
  bottom line; it became Track 1's first item.
- **P0 left Form 1099-K's line open; the instructions settle it.** Line 25b
  covers any Form 1099 showing tax withheld on other income. Building it then
  stopped on a different ground: giving the published fact its own source
  family would change membership rules for every existing use on `main`.
  It is parked with the reason.
- **Count is enough to catch a missing answer, not a mismatched one.** The
  W-2 box 2 check compares statement counts with the existing `count`
  operation. It catches a missing box 2 answer; pairing each answer with its
  own W-2 would need a join the rule language does not have.

## Process

- **Successor rules apply to `main`, not to the branch.** Track 1's repair
  published line 25a as v2 beside a v1 that never merged; Track 2 folded it
  back so no orphan version lands.
- **A time budget in the brief kept a unit bounded.** Track 2 committed what
  was complete and tested and reported the goldens as remaining; they ran as
  a separate short unit.
- **One builder ran every unit**, resumed across P0, both tracks, two repairs
  and the goldens, at the cost of a growing context.

## What it cost

All units ran on one resumed Sonnet builder: P0 about 14 minutes (117 tool
calls), Track 1 about 42 minutes (237), its repair about 8 minutes (46),
Track 2 about 22 minutes (106) and the goldens about 27 minutes (134). The
final review ran on a fresh Sonnet reviewer.

## Follow-ups

- Form 1099-K, 1099-G and SSA-1099 withholding on line 25b, and a 1099
  statement recorded without its box 4 answer.
- Refundable credits (lines 27-31), Schedule 2 Part II taxes and the
  estimated tax penalty.
- The age questions' wording and the SLI dependent answer, carried from the
  previous milestone.
