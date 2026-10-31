# Retrospective — Withholding Waits for Every Statement (2025)

## Result

- **On core v61 the bottom line waits for every withholding family.** A
  recorded Form 1099-INT, 1099-DIV, 1099-R or 1099-G box 4 amount, or an
  SSA-1099 box 6 amount, no longer counts on line 25b while its family is
  unconfirmed or stale. Line 25b blocks naming the family; lines 25d and 33
  through 37 wait behind it. Before, 600 of 1,000 of 1099-G withholding
  recorded published a refund of 25 instead of 425.
- **A complete return computes exactly as on v60.** One successor rule (line
  25b v3); no engine, schema or expression-operation change; no new
  question, because each family's closure question already exists.
- **Form W-2 box 2 already blocked** in every cause; line 25a is unchanged.
- **Core v60 and earlier keep the gap**, pinned by tests.

## What the evidence changed

- **The gap was in an operation, not in the families.** `collect` reads
  closure only when its set is empty; with any member present it sums what
  is there. `require_closed` always reads it. Line 2b already guarded its
  subtotals; line 25b did not. The fix is the guard, not a change to
  `collect`, which every family uses.
- **The same shape may exist elsewhere.** 49 rules `collect` without a
  guard. Many feed a guarded line, as the withholding subtotals now do; the
  rest are unsurveyed and parked as one engine question.
- **One incompleteness stays invisible.** A closure attested true over an
  amount never recorded publishes the smaller number. Catching it would mean
  asking every statement for its box 4 answer, which changes complete
  returns.

## Process

- Dispatch moved to Sonnet 5.5 Agent sub-agents by owner direction at the
  start. P0 took about 30 minutes, Track 1 about 5, the review about 9.
- `tools/package_successor.py` built core v61, registry v59 and release v59
  from a 33-line change set in its first milestone use. The per-package
  companion declaration in `packages/tax/loader.py` still had to be added by
  hand; the review showed that without it a v61 1099-G return is refused at
  recording.

## Follow-ups

- Survey the 49 unguarded `collect` rules for any that publish a partial
  income sum.
- Per-statement box 4 answers for the Form 1099 withholding families, if the
  residual matters.
- Name the closure question, not the family id, when line 25b or 2b blocks.
- Package companion declarations in package content (carried).
