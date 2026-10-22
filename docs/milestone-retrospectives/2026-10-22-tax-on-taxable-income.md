# Retrospective — The 2025 Tax on Taxable Income

## Result

- **Line 16 follows 2025 law on core calculations v50.** It uses the seven-bracket
  rate schedule through the Tax Table (below $100,000) or the Tax Computation
  Worksheet, and the Qualified Dividends and Capital Gain Tax Worksheet,
  published line by line with the 0, 15 and 20 percent bands. A single return
  with $596,850 of taxable income now computes $178,445 instead of $126,360;
  $46,850 computes the published table's $5,387 instead of $5,390.
- **Short-term gain is taxed at ordinary rates.** The preferential base is now
  the smaller of Schedule D lines 15 and 16, or zero if either is a loss. It was
  line 16 floored at zero.
- **The 2025 standard deduction.** $15,750 / $31,500 / $23,625 after Pub. L.
  119-21, with the $1,600 married and $2,000 unmarried additional amounts.
- **No new return class, schema, expression operation or engine change.**
  Earlier packages and their goldens are unchanged; a workspace gets the
  corrected tax by adopting v50.

## What the evidence changed

- **P0 found more than the parked list said.** The parked list named the
  standard deduction and the short-term defect. P0 also found the rate schedule
  truncated at 22 percent with 2024 thresholds, a flat 15 percent preferential
  rate, no Tax Table, and a wrong married additional amount ($1,550). The
  parameters were marked `demo.*` throughout; the coverage frontier's
  "synthetic complete" rows were true of routing and explanation, not of the
  rates.
- **Checking the evidence against the downloaded source caught three errors
  before the build.** The Tax Table's rows below $25 are not uniform bands; the
  worksheet's own lines 22 and 24 also use the Tax Table; and the golden-change
  estimate was wrong because tests pin their package version. Each Track 1
  expectation was then hand-computed and checked against the published table,
  including the round-half-up at $3,000.
- **A formula is only auditable if it stays small.** The first worksheet rules
  passed every case but grew to 68–83KB, because each threshold expanded a
  filing-status choice and each "smaller of" copied its subtrees. The
  `parameter` op already took a filing-status key. Publishing one rule per
  worksheet line brought every rule under 5KB and made each line its own
  explainable finding.

## Process

- The P0 builder committed with `--no-verify` and reported it. The probable
  cause was the Foreman's own charter, which carried the absolute worktree path
  that the envelope hook rejects; the next charter did too and was refused at
  commit. Charters now say the worktree is supplied at launch.
- **The full lane was skipped before marking the PR ready, and CI caught
  it.** Builders and the final reviewer ran the fast lane and their own
  modules; a data-safety gate that flags six-digit amounts in tax content runs
  only in the full lane. The first ready-PR `verify` failed on the new rate
  schedule, the 15% ceiling and a literal $100,000 in two worksheet rules. The
  repair moved the limit into a cited parameter and added the statutory
  parameters to the gate's per-id exemptions; the full suite then passed
  locally before the PR was marked ready again. A content-only milestone still
  runs the full lane before ready.
- The owner switched dispatch from Sonnet to Grok after Track 1 had just
  launched; the Sonnet run was stopped before it changed anything.

## What it cost

P0 ran on a Sonnet builder (213 tool calls, about 29 minutes). Track 1 ran on
the Grok CLI: 179 turns and $4.92, then a 44-turn, $0.90 repair in the same
session. Track 2 resumed that session: 58 turns, $1.59. Grok's balance then ran out before
the final review, which ran on a fresh Sonnet reviewer; the CI repair was made
by the Foreman. Resuming one builder
session across tracks kept later units cheap.

## Follow-ups

- The deduction for a taxpayer or spouse aged 65 or older (Schedule 1-A) and a
  dependent's limited standard deduction: named in the standard deduction's
  basis, not computed. The engine already records age 65.
- Worksheet lines as rows in the saved presentation; today they are reachable
  through the explanation walk only.
- Verified ids for the capital-loss limit and Social Security worksheet
  amounts, which are correct but keep `demo.*` ids.
- Citation artifacts that can name a revenue procedure or statute, not only an
  instruction family and form.
