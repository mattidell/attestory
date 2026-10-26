# Retrospective — The 2025 Child Tax Credit

## Result

- **Lines 19 and 28 compute from Schedule 8812 on core v55.** A joint return
  with two children and $75,000 of wages takes the whole $4,400 on line 19; a
  head of household with $18,000 of wages and no tax gets $1,700 on line 28
  beside a $7,152 earned income credit.
- **Each child is counted from answers about that child** on a closed credit
  roster over the EIC child kind, sharing the EIC's relationship, joint
  return, SSN and tie-breaker answers and adding this credit's own.
- **Three or more children are in the class.** Part II-B reads W-2 boxes 4 and
  6, asked only on its path.
- No schema, expression operation or engine change. Earlier packages and
  their goldens are unchanged.

## What the evidence changed

- **One roster could not carry two credits.** A family authorizes one
  subtotal and a fact belongs to one family, so the credit roster is a second
  family over the same child kind whose member is the "claimed as dependent"
  answer.
- **Part II-B is for every three-child family, not only Puerto Rico.** P0
  proposed refusing those returns below the 15 percent cap; the Foreman kept
  them in by adding W-2 boxes 4 and 6 in the box 2 pattern. In practice Part
  II-B rarely changes the result, because the earned income credit in its
  range exceeds payroll tax; computing it avoided refusing the families the
  credit matters most to.
- **The citizenship question carried the dependency test.** Its title
  included residents of Canada or Mexico, which would have let a parent of a
  child living in Mexico claim $2,200; the child tax credit test is U.S.
  citizen, national or resident alien. Third question-wording defect in the
  credit milestones, found by reading the title against the instruction step.
- **The final review found three defects the tests could not see.** The
  credit's filer gate reused the EIC's "cannot be claimed as a dependent"
  answer, which is asked only off joint returns, so every joint return with a
  child was blocked; it required the taxpayer's own SSN, where on a joint
  return either spouse's SSN suffices (the other needs an SSN or ITIN); and
  the direct foreign tax credit rule still required the old "line 19 is
  absent" answer. Each test fixture supplied every answer, so none saw a gate
  that required too much; the reviewer found them by omitting answers per
  filing status. The gate now reads the standard deduction's return-level
  dependent answer and either spouse's SSN, and the foreign tax credit rule
  has a successor without that requirement. Reusing an answer needs both its
  meaning and its asked-when checked.
- **The builder caught a charter error:** at $60,000 joint, tax is below the
  credit, so the first golden used $75,000.

## Process

- Every unit ran on one resumed Haiku 5.5 builder (P0, Tracks 1a, 1b and 2).
  It verified with probes and stated its arithmetic; the Foreman fixed one
  title and one plan statement. The final review ran on a fresh Haiku 5.5
  reviewer, whose omitted-answer probes found the three gate defects.

## Follow-ups

- The credit for other dependents ($500) and Credit Limit Worksheet B.
- A child another person may also claim (tie-breaker rules).
