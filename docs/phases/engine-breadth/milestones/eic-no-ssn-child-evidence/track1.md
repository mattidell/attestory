# Track 1: a qualifying child without a valid SSN keeps every filing status off Step 4

Core v102, registry v100, release v100. Wages in the hand cases are 7,000.
The table is `parameter.eic-table-2025` v2. At that wage the joint column
and the other column publish the same dollars: column 0 is 537, column 1
is 2,389, and column 2 is 2,810. Married filing jointly still uses `joint-N`.

## Sources

Searched the 2025 Form 1040 instructions (Steps 1 through 6) and the 2025
Schedule EIC instructions, and Publication 596 chapters 2 and 3, including
the examples that name a child. No sentence sends a filer whose qualifying
children all lack a valid SSN to Step 4 or to chapter 3.

Schedule EIC (Form 1040) 2025, page 2, says the opposite. A child who meets
the qualifying-child conditions but does not have a valid SSN still supports
the self-only credit, and the filer attaches Schedule EIC:

> Qualifying child doesn’t have an SSN. If you have a child who meets the
> conditions to be your qualifying child for purposes of claiming the EIC,
> but that child doesn’t have an SSN as defined in the instructions for
> Form 1040, line 27a, and you are otherwise eligible, you can claim the
> self-only EIC. To claim the self-only EIC with a qualifying child,
> complete and attach Schedule EIC to your Form 1040 or 1040-SR.

The qualifying-child definition on that same page is relationship, age,
joint return, and lived in the United States more than half of 2025. A
valid SSN is not one of those tests. Line 2 of the schedule asks for the
child's SSN unless the filer is claiming the self-only EIC.

Publication 596 chapter 3, page 17, opens with who uses that chapter:

> Use this chapter if you don’t have a qualifying child and have met all
> the rules in chapter 1. ... If you have a qualifying child. If you meet
> Rule 8, you have a qualifying child. If you meet Rule 8 and don’t claim
> the EIC with a qualifying child, you can claim the EIC without a
> qualifying child.

That sentence does not mention an SSN. The other Step 4 and chapter 3
hits are the same kind of sentence: the filer has no qualifying child
(Step 3 question 1, or Rule 8 failed), the tiebreaker treats the child as
someone else's qualifying child, Form 8862, or the joint return skips
Step 4. None of them is caused by a qualifying child who lacks a valid SSN.

## Scope

Widened. For every filing status, a filer whose qualifying children all
lack a valid SSN is a filer with a qualifying child, skips Step 4, and
takes the self-only column (`other-0`, or `joint-0` when married filing
jointly). The amount column is still the count of qualifying children who
have a valid SSN.

`rule.eic-answer.age-25-under-65` v4 and `rule.eic-answer.main-home-in-us`
v4 skip when a qualifying child is present, and they do not read status
class. `rule.eic-answer.not-claimable-as-dependent` v4 skips on that same
fact. `rule.eic-answer.not-qualifying-child-of-another` stays v3, so a
non-joint filer with a qualifying child is still asked it. The other
successors are the P0 route: qualifies, present, status class v3, early
stop v3, questions required v3, separated-spouse v2, and not-married v2.
An unmarried head of household with a qualifying child is asked the
existing separated-spouse question. No new question. No new operation,
schema, or projection.

## Files published

New files only. The published v101 citizens are unchanged.

- `rule.eic-child.qualifies.json` and `rule.eic-qualifying-child-present.json`
- successors: status class v3, early stop v3, questions required v3,
  separated-spouse v2, not-married v2, age v4, main home v4, not-claimable v4
- `package.core-calculations.v102.json`
- `published-packages.v100.json`
- `demo.release.sli-worksheet-integration.2025.v100.json`
- loader entries for core v102 carry the v101 covered-flag map and the v101
  companion declaration

The package and the registry are larger than 200 KB, as v101 and registry
v99 already are. No schema manifest changed.

## Replay

Strict full-surface replay of the 775 recorded lists, published v101
against published v102, with the widened expectations. 775 passing, 0
unexpected. 691 lists are `expected_changes` (`success/success`). 84 lists
are identical `error/error`, the same recorded failures as on v101. No
numeric expectation was declared, and no recorded number changed.

18 expectations declared, 14 used. Unused, as on the P0 replay: the
disposition node of `child.qualifies`, its fields, its explanation graph,
and the pin expectation for `qualifying-child-present`. Those pins show
up as inserted children on the rules that read the new count. The age,
main-home, and not-claimable children lists are that insert and nothing
else. Section roots that moved did so by exactly one.

## Hand credits

A child counts as qualifying only with the age test met and residency of
more than half the year. The column counts only those who also have a
valid SSN. `apart` and `writing` are the same yes on the published
separated-spouse fact.

| Situation | Asked | Credit |
| --- | --- | --- |
| Married head of household or married filing separately, qualifying child, separated yes | separated-spouse; not-qualifying-child except the amount | table of the SSN column (537 when the column is 0) |
| Those two statuses, qualifying child, separated no | the same questions | 0 |
| Those two statuses, no qualifying child | married head of household: not-married, and a no stops the credit. Married filing separately: the column-0 class-0 stop | 0 |
| Single, qualifying surviving spouse, or married filing jointly, qualifying child | not-qualifying-child, except married filing jointly already skips it. Step 4 is not asked. The separated answer does not change the credit | `other-N` or `joint-N` |
| Single, qualifying surviving spouse, or unmarried head of household, no qualifying child, Step 4 answered yes | age, main home, not-claimable, not-qualifying-child. Unmarried head of household is also asked not-married | 537 |
| Married filing jointly, no qualifying child, Step 4 answered yes | age and main home | `joint-0`, 537 |
| Unmarried head of household, qualifying child, separated yes (the published yes includes not married) | separated-spouse and not-qualifying-child | table of the SSN column |
| Unmarried head of household, qualifying child, separated no | the same questions | 0 |

The live cases are the 50 P0 keys plus single, qualifying surviving spouse,
married filing jointly, and unmarried head of household: each child pattern
(SSN, no SSN, both), separated yes and no, lived more and less, and the
age-test failure. Each matched this table, including `eic.table-key`.

## Tests

`pytest tests/test_eic_no_ssn_child_v102_package.py` and
`tests/test_noncovered_sales_v78_switch.py`: 10 passed.
`pytest tests/test_eic_no_ssn_child_v102.py`: 95 passed. That file calls
`live_coordinate_run`.
`pytest -m "not live"`: 1957 passed, 8 skipped, 5985 subtests passed.
`python3 -m mypy`: no issues in 536 source files.

`test_ssn_test_stays_on_the_amount_and_off_the_qualifying_child` pins
`hoh/nossn/apart/more` at 537, with that child counting 0 and qualifying 1,
and the married-filing-jointly case on `joint-0`. On scratch copies only,
adding the SSN test to `rule.eic-child.qualifies` makes the same return
credit 0 and present 0. Dropping the SSN test from `rule.eic-child.counts`
and removing the then-unreachable `rule.eic-child.ssn-met` member makes
the credit 2,389 and the column 1. Dropping the test and leaving that
member in the package is refused: the member is unreachable from the
entrypoints. Those copies were not committed.
