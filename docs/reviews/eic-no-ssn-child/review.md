# Fresh review: a child without a valid SSN routes the earned income credit

Charter: `docs/reviews/eic-no-ssn-child/charter-review.md`. Object:
`github/main..HEAD` on `milestone/eic-no-ssn-child-2025` at `4da876408854`
(8 commits). Fresh context. Governance was not read. Builder threads were
not read.

## Verdict

**READY with notes.** The widened reading matches the 2025 Form 1040
instructions, Schedule EIC, and Publication 596: a qualifying child who
lacks a valid SSN keeps the filer off Step 4 and on the self-only column,
for every filing status. Recorded returns keep their numbers. The tests
fail closed on the three chartered mutations. One low note: an unmarried
head of household in that position is asked the separated-spouse question,
which Decision 3 accepts and which the instructions do not ask.

## Capability box

Facts that may enter are the filing status, the child roster (relationship,
age, residency, joint return, tie-breaker, and whether the SSN test is met),
and the existing earned-income-credit answers. The authority for the route
is the 2025 instructions (line 27a, Steps 1–5, Worksheet A) and Publication
596 chapters 2 and 3, as adopted by Decisions 1–4. The box publishes
`eic.child.qualifies`, `eic.qualifying-child-present`, the status class, the
amount column, and line 27a. The amount column still counts only children
whose SSN test is met. The credit table, other credits, the kernel, and the
page are outside the change. A return with a counted child, and a return
with no qualifying child, keep the v101 result.

`eic.child.qualifies` is a derived fact (relationship, age, residency, joint
return, tie-breaker). `eic.child.counts` is that same derivation plus the
SSN test, and it alone selects the table column. The two stay distinct.

## Findings

**ENS-R1 (Low).** An unmarried head of household whose only qualifying child
lacks a valid SSN is asked the separated-spouse question. A recorded "no"
publishes a credit of 0. The 2025 instructions do not ask that person
Step 3 questions 4 and 5.

`rule.eic-status-class.v3.json:74-100` publishes class 0 for head of
household unless the column count and `eic.qualifying-child-present` are
both 0. The predecessor (`rule.eic-status-class.v2.json:68-79`) publishes
class 1 whenever the column count is 0, so this filer was class 1 on v101
and the separated-spouse rule skipped them. `rule.eic-answer.separated-spouse.v2.json:99-144`
asks the question when questions are required, the status class is 0, and
the filer is not in the (column 0 and present 0) case.
`input-question.eic-separated-spouse.v1.json:6` still says the child "is
counted," and its yes includes "not married at the end of 2025."

Scenario, wages 7000, synthetic `uhoh/nossn/no/more`: the child qualifies
and is not counted (column 0, present 1, class 0). Separated-spouse is
asked. The recorded answer is no. Line 27a is 0. The same return with the
question's own yes (`uhoh/nossn/apart/more`) publishes 537, table key
`other-0`, and does not ask Step 4. Step 3 question 6 is asked.
`uhoh/ssn/no/more` also publishes 0; asking an unmarried head of household
who has a counted child is the v101 shape Decision 3 copies.

Decision 3 (`eic-no-ssn-child.md:130-133`) records this encoding and adds
no new question. A filer who answers the published sentence truthfully
(yes, because they were not married) receives the self-only credit.
Smallest repair, if the foreman wants the instructions' question list:
require the separated-spouse answer only when the filer is married.

## Answers

### 1. The sources

The widened reading is right.

Form 1040 instructions (2025), Steps 1–5, read with the worksheet and the
Schedule EIC instructions: a child who meets the qualifying-child conditions
is still a qualifying child when the child has no valid SSN. The filer
completes Schedule EIC. Step 3 question 1 Yes stays in Step 3. Question 2
Yes (joint return) skips the rest of Step 3 and all of Step 4. Question 3
asks whether the filer is a married taxpayer whose status is married filing
separately or head of household. No skips questions 4 and 5 and goes to
question 6. Questions 4 and 5 are the separated-spouse test; a No on
question 5 stops the credit. Question 6 (could you be a qualifying child of
another person?) is still on that path. Yes stops the credit. No skips
Step 4 and goes to Step 5. Step 4 is titled for filers without a qualifying
child. Worksheet A and the Step 1 and Step 5 limits count children who have
valid SSNs, so zero such children uses the self-only column and the
self-only earned-income cap (19,104, or 26,214 if married filing jointly).

Publication 596 (2025), chapter 2, says to follow that chapter even when the
child who qualifies the filer has no valid SSN, and that the filer may claim
the self-only credit. Chapter 3 opens for a person who does not have a
qualifying child. The sentence that allows the credit without a qualifying
child sits with the tie-breaker rule for a person who meets Rule 8 and does
not claim the child. No sentence in those sections sends a filer whose
qualifying children all lack a valid SSN to Step 4 or to chapter 3.

Schedule EIC (2025) says the same thing in its own words: a child who meets
the qualifying-child conditions and has no SSN still supports the self-only
credit, and the filer attaches Schedule EIC. Its qualifying-child definition
on that page is relationship, age, joint return, and residency.

One exception sits beside that rule and is unchanged in this range. A child
who was born and died in 2025 can support the higher amount without an SSN.
`rule.eic-child.counts` still requires the SSN test. This range does not
modify that rule. That gap is older than v102.

Measured on v102 through the live coordinator, wages 7000 unless noted.
Step 4 (age, main home, not claimable) stays unasked whenever a qualifying
child is present. Step 3 question 6 is asked for single, qualifying
surviving spouse, and both head-of-household shapes, and is not asked for
married filing jointly. A married head of household and a married filing
separately filer are asked the separated-spouse question; a recorded no
publishes 0 (`hoh/nossn/no/more` column 0 credit 0; `mfs/ssn/no/more`
column 1 credit 0). At wages 20000 a single filer with only a no-SSN
qualifying child is already in the open zero band of `other-0` (the
published band starts at 19104) and is not asked Step 3 question 6. The
same wages on a joint return still publish `joint-0` credit 473, and
question 6 stays unasked because the return is joint.

### 2. Each successor

For a married filer, and for single, qualifying surviving spouse, and
married filing jointly, the successor condition is the source condition.
`eic.child.qualifies` is the qualifying-child tests without the SSN test.
`eic.qualifying-child-present` is 1 when any such child exists. The column
count still comes from `eic.child.counts`, which requires the SSN test.
Status class, early stop, questions required, separated-spouse, not-married,
age, main home, and not-claimable each gain a present arm. On a return
whose column count is already above 0, and on a return with no qualifying
child (present 0 and column 0), that arm is redundant with the predecessor
condition. Head of household with a counted child stays class 0. Head of
household with no child stays class 1. Married filing separately stays 0,
married filing jointly stays 2, and single and qualifying surviving spouse
stay 1. The independent replay below is the check that those returns do
not move.

The one new question is ENS-R1. Nothing the sources require is dropped:
Step 4 is skipped because the sources skip it, question 6 remains for a
non-joint filer who reaches Step 3, and a married filer with a qualifying
child still has to pass the separated-spouse test.

### 3. Amounts

Hand-read from Publication 596 (2025), the EIC table. Bands are lower
inclusive, upper exclusive. The published `parameter.eic-table-2025.v2.json`
matches these rows. Live v102 credits match the same rows.

| Earned income | Column | Publication 596 | Live |
| --- | --- | --- | --- |
| 1,000–1,050 | other-0 / other-1 | 78 / 349 | single, no-SSN child, 78; single, SSN child, 349 |
| 7,000–7,050 | other-0 / other-1 | 537 / 2,389 | married head of household, no-SSN child, apart, 537 |
| 9,000–9,050 | other-0 / joint-0 | 649 / 649 | single 649; joint 649 |
| 12,000–12,050 | other-0 / joint-0 / other-1 / joint-1 | 542 / 649 / 4,089 / 4,089 | single no-SSN 542; joint no-SSN 649; one SSN child and one no-SSN child, both qualifying, head of household 4,089 `other-1` present 2; joint 4,089 `joint-1` |
| 12,000–12,050 | other-0, mixed residency | 542 | SSN child lived half a year or less, no-SSN child lived more, single, 542, present 1 |
| 17,700–17,750 | other-0 / joint-0 | 105 / 649 | single 105; joint 649 |
| 20,000–20,050 | other-0 / joint-0 / other-1 / joint-1 | 0 / 473 / 4,328 / 4,328 | single no-SSN 0; joint no-SSN 473; single with one SSN child 4,328; mixed roster, single and joint, 4,328 on column 1 |
| 23,350–23,400 | other-1 / joint-1 | 4,324 / 4,328 | mixed roster, single 4,324 present 2; joint 4,328 present 2 |

The 7,000 one-child figure 2,389 is the live counted-child case in
`test_ssn_test_stays_on_the_amount_and_off_the_qualifying_child`. Joint
no-SSN at 7,000 is 537 (`joint-0`). Phase-in, plateau, phase-out, both
filing-status columns, and a mixed roster are all in the table above.

### 4. Nothing else moved

Independent full-surface replay of the 775 recorded lists, v101 against
v102, with the widened expectations: 691 `expected_changes`, 84 `identical`,
775 passing, 0 failing, 0 unexpected. Outcomes are success/success on the
691 and error/error on the 84, so the lists that already failed still fail
the same way.

The declared expectations do not hide a value change. `version_change`
matches only a `version` or `pinVersion` attribute. Every other expectation
is scoped to `eic.qualifying-child-present` or `eic.child.qualifies` (a
report row, a disposition node, a pin, or an explanation graph). The four
expectations the committed summary marks unused are that same kind of
scoped add; an unused scoped add blesses nothing. The three normalizers
rewrite a list only when stripping the new-rule tokens restores the prior
list, drop an input digest only when a symbol has one finding on each core,
and move a section-root index back only when every changed index moved by
exactly one and the new finding is present. A change to an existing credit
field survives all three and matches none of the expectations, so it would
have been unexpected.

`git diff --name-status github/main..HEAD` adds the new rule files, core
v102, `published-packages.v100.json`, and the v100 release. It modifies
`packages/tax/loader.py` and `tests/test_noncovered_sales_v78_switch.py`.
No existing content file and no published schema file is modified. The
loader's v102 covered-flag map is `dict(COVERED_FLAG_REFUSAL_OBJECTS)`, the
same expression as v101 (`loader.py:271-274`). The v102 companion
declaration repeats v101's presence pairs and value domains
(`loader.py:815-836`). The switch test's allowlist now runs v79 through
v102 and expects that same map.

`python3 tools/envelope_scan.py --range github/main..HEAD` exits 0.

### 5. Tests

Each mutation was applied in a scratch copy of the tree, the citizen
checksum and the release digest were recomputed so the coordinator would
load the mutated rule, and the tree was restored afterward. Nothing
mutated was committed.

- SSN test moved off `counts` and onto `qualifies`. The package test fails
  in `qualifies_rule` (`design.py:131`), which requires the counts rule to
  still contain exactly one SSN compare. The live test fails at
  `tests/test_eic_no_ssn_child_v102.py:77`: `hoh/nossn/apart/more` publishes
  2,389, and the test expects 537.
- Step 4 question 1 applied to a no-SSN-child filer, by dropping the
  present arm from `rule.eic-answer.not-married.v2.json`. The live test
  fails at `tests/test_eic_no_ssn_child_v102.py:58` on
  `hoh/nossn/apart/more`: credit 0, expected 537.
- Separated-spouse test skipped for a married filer, by publishing 1
  whenever that rule is reached. The live test fails at the same assertion
  on `hoh/nossn/no/more` (537, expected 0) and on `mfs/ssn/no/more` (2,389,
  expected 0). An earlier scratch edit that renamed the "no" category
  unpublished line 27a entirely; that result is a broken rule, and the
  numbers above are the rerun that actually skips the test.

## What I ran

- `python3 tools/envelope_scan.py --range github/main..HEAD` — exit 0.
- `pytest -m "not live" tests/test_eic_no_ssn_child_v102_package.py tests/test_noncovered_sales_v78_switch.py` — 10 passed.
- Full-surface replay of v102 over the 775 recorded lists — 0 unexpected, as summarized in answer 4.
- Live coordinator cases at the incomes in the amount table, plus the unmarried head-of-household cases in ENS-R1. The wages-20000 set (single and joint, no-SSN child, counted child, and mixed roster, and a married head of household with a no-SSN child) matched the table on all six returns.
- The three scratch mutations in answer 5. Each live pytest exited 1 on the assertions named there, and the scratch tree was restored.
