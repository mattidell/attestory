# Retrospective — The 2025 Earned Income Credit

## Result

- **A filer with no qualifying child gets the 2025 earned income credit on
  core v53.** Line 27a is EIC Worksheet A on W-2 box 1 earned income and AGI,
  read from the printed 2025 EIC Table's 0-child columns. A single filer with
  $12,000 of wages and $2,000 of interest gets $389, and a joint return with
  $16,000 of wages gets $649.
- **Each question is asked only where it can change line 27a.** Investment
  income over $11,950 asks only the unsupported-situations answer. AGI at or
  above $68,675 asks no EIC question. W-2 box 1 at or above $68,675 while AGI
  is below it asks that answer, because a clergy or church-employee Schedule
  SE amount can put worksheet earned income below box 1. Otherwise the
  qualifying-child answer is asked. Married filing separately and head of
  household with no qualifying child are $0. After that answer, AGI at or
  above the 0-child completed amount asks no further EIC question (Step 1
  tests line 11b). Box 1 at or above that amount while AGI is below it asks
  the unsupported-situations answer, except for married filing separately
  and head of household, which filing status alone stops. The remaining questions are asked only
  for single, married filing jointly, or qualifying surviving spouse when
  both amounts are below that completed amount. Six unsupported situations
  share one answer.
- **Lines 28-31 have their own absence answer**, replacing v52's combined
  lines 27a-31 answer. That answer is required on every successor-package
  return. A v52 workspace is not blocked on every new EIC answer: when AGI
  is at or above $68,675, v53 still publishes line 27a as $0 without the EIC
  answers and blocks only the lines 28-31 total on the new fact. When the
  new EIC answers are required, a workspace that only answered the old
  combined question is blocked until it answers the new ones.
- No schema, expression operation or engine change. Earlier packages and
  their goldens are unchanged.

## What the evidence changed

- **P0 recovered the table's construction and checked all of it.** The 2025
  table does not print its rates. P0 found them, wrote the table as a formula
  with three corner cases, and matched every one of the 1,374 printed bands.
- **A formula that verifies is not one that explains.** Track 1 built the
  formula as 47 rules, evaluated once at earned income and once at AGI. Track
  2's readability check measured the explanation from line 27a at 13,227 tree
  nodes over 231 findings, with banding and midpoint steps where a reader
  expects Worksheet A. The repair put the printed 0-child columns in a
  `range_lookup` parameter, cut the rules to 22, and kept the formula as a
  test of every row. Every amount in both goldens stayed identical.
- **Three review rounds found one defect class: an answer required where no
  publishing path read it.** First, the unsupported-situations answer was
  required on the credit path but never evaluated, so correcting it would not
  have displaced a computed credit; and the $11,950 stop skipped the
  instructions' Form 4797 and Schedule E questions. Second, the Foreman's
  contract let a $0 stop on W-2 box 1 skip that answer, although a clergy or
  church-employee amount can put worksheet earned income below box 1; only a
  stop on AGI is safe without it. Third, the answer was still required for
  married filing separately and head of household, which filing status alone
  stops. Declared requirements are not provenance; only what evaluation
  reads is. A test now covers each case where the answer is required, and
  the married filing separately and head of household cases where it is not.
- **Reuse was checked and declined.** The senior deduction's SSN and age
  answers, and the standard deduction's dependent answer, each mean something
  slightly different from the EIC's tests, so the EIC asks its own.

## Process

- **The Foreman cut the question burden from P0's proposal.** P0 proposed
  fourteen questions on every return. The contract merged six
  outside-the-class situations into one answer and required each EIC
  question only on the path where that answer can change line 27a.
- **One grok session ran every build unit** (P0, both tracks and the repairs),
  resumed each time with a short brief and a file report. The final review
  ran in a fresh grok session.

## What it cost

All on the grok headless CLI: P0 56 turns ($1.65), Track 1 240 turns
($6.71), Track 2 61 turns ($1.59), the table repair 63 turns ($1.86); the final review and two re-reviews 82
turns ($2.51) and their three repairs 137 turns ($4.08). Track 1
was the expensive unit, and most of it built machinery the repair removed.
Asking "will this explain?" in the Track 1 charter, not only in Track 2's,
would have saved that.

## Follow-ups

- The credit with qualifying children: per-child facts, the separated-spouse
  rule, and a refusal when another person can claim the same child. The
  parameter already holds every child count's amounts; the table parameter
  would add those columns.
- A corpus-wide check that every required input a rule declares is read on
  some evaluated path, since an unread requirement is invisible to
  correction.
- `explain()` re-expands shared inputs at each use, so a walk over 218
  findings is a 9,885-node tree.
- Worksheet B, Form 8862, combat pay, the Medicaid waiver exclusion and
  Worksheet 1; lines 28-31; a citation artifact for revenue procedures.
