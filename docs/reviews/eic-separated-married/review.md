# Review: the separated-spouse question is asked only of a married filer

Reviewer, fresh reader. Charter: `docs/reviews/eic-separated-married/charter-review.md`.
Object: `github/main` (`974cb1a1`) `..` HEAD (`4ac6b8a6`) on
`milestone/eic-separated-married-2025`. Orientation block verified at
`4ac6b8a6c863c21aa3e58b97b701664876db0049`. Governance not read.

**Verdict: NOT READY.**

The box. A head of household with a qualifying child may answer
`tax.us.2025.eic.married-taxpayer` (yes or no). A recorded
`eic.separated-spouse` answer may already be on the return. Filing status,
the qualifying-child facts, and the earlier earned-income-credit gates are
the other inputs. Core v103 may publish line 27a from the 2025 table when
Step 3 question 3 is no, and $0 or a block when the separated-spouse rule
still applies. Married filing separately keeps the v102 path and is not
asked the new question. Single filers, joint filers, the credit tables, and
the other credits stay outside the change. `eic.married-taxpayer-inert` is
a stored fact, not an observed answer: nothing asks it, and a stored value
is not the same thing as the question being skipped.

The published rules do that routing. The published question does not state
the marital test the 2025 instructions state, and one sentence of it is
false.

## Findings

### ESM-R1 (high). The question's yes/no gloss is not the instructions' marital test

- **Claim.** Decision 6: the question is checked against Step 3 question 3
  and Publication 596, Rule 3, and it says who is married for the credit,
  including a filer considered unmarried for head of household and a decree
  of divorce or separate maintenance.
- **Where.** `packages/content/tax/2025/input-question.eic-married-taxpayer.v1.json:7`
  and the same gloss in `eic-married-taxpayer.bundle.json:19`.
- **What the sources say.** Instructions, Head of Household (i1040gi,
  sha256 `482e9c48…8364a`, printed page 14): a person is considered
  unmarried for head of household when legally separated under a decree of
  divorce or of separate maintenance at the end of 2025, and an
  interlocutory decree still means considered married. Step 3 question 3
  (printed page 41) is "Are you a married taxpayer whose filing status is
  married filing separately or head of household?" Yes continues to
  questions 4 and 5. No skips those two and goes to question 6. Question 5
  No stops the credit. A decree of separate maintenance is also a question
  5 prong, and only together with living apart at the end of 2025.
- **Consequence.** Semantic. The engine follows the stored yes/no. Answering
  from the gloss, rather than from those two instruction rules, publishes
  the wrong line 27a.
- **Reproduction.** On published v103, `live_coordinate_run`, wages 7,000,
  head of household, one qualifying child with a valid SSN, new answer no,
  no separated-spouse answer (`q3-no/ssn`): line 27a is 2,389, the
  separated-spouse fact is not pinned, and `eic.answer.married-taxpayer` is
  1. The same no at 5,000, 18,000, and 30,000 publishes the table amounts
  1,709, 4,328, and 3,261. So a no keeps the table credit whenever question
  6 and the other gates pass.
  1. Interlocutory decree, same principal residence for the last six months
     of 2025, no written separation agreement. The instructions treat the
     filer as married. Question 3 is yes, question 4 is yes, question 5 is
     no, and the credit stops. The gloss says answer no if you were not
     married at the end of 2025 and does not mention an interlocutory
     decree. A no publishes the table credit.
  2. Final decree of separate maintenance, same household at year end. The
     head-of-household rule treats the filer as unmarried, so question 3 is
     no and question 5 is never reached. The gloss does not say the decree
     means not married. A yes continues into the separated-spouse question,
     whose no (the decree prong also requires living apart) publishes $0.
     Measured on `q3-yes-no/ssn`: line 27a is 0.
- **Repair.** State the instruction rules in the question: an interlocutory
  decree is still married; a final decree of divorce or of separate
  maintenance is not married for question 3. Keep the Rule 3 sentence for a
  head of household who lived apart and is still married. Do not leave
  "married at the end of 2025" as the whole test.

### ESM-R2 (medium). "No … you keep the credit" is false

- **Claim.** The question tells a filer who answers no that questions 4 and
  5 are skipped and the credit is kept.
- **Where.** `input-question.eic-married-taxpayer.v1.json:7`, the clause
  "No skips those questions and you keep the credit."
- **What the sources say.** Question 3 No skips questions 4 and 5 and goes
  to question 6. Question 6 Yes stops the credit ("You can't take the
  credit").
- **Consequence.** The sentence is false. The computation still applies
  question 6, so this sentence does not by itself pay a credit the
  instructions stop. A filer who relies on the sentence is told the wrong
  result.
- **Reproduction.** Same `q3-no/ssn` return. Removing
  `eic.not-qualifying-child-of-another` blocks line 27a
  (`eic-answer.not-qualifying-child-of-another:DEPENDENCY_ABSENT` and
  `form1040-line27a:DEPENDENCY_ABSENT`). Answering that fact no publishes
  line 27a as `computed_zero` 0. The new question's no did not keep 2,389.
  On the supplied return the question-6 fact is pinned (`asked` not-qc
  true) while the separated-spouse fact is not.
- **Repair.** Say that no skips questions 4 and 5 and continues to question
  6. Drop "you keep the credit."

### ESM-R3 (medium). A stored inert fact blocks the credit

- **Claim.** Decision 5: the inert path stays only because validation
  requires a second path, and the fact is never offered as a question. The
  path is described as inert.
- **Where.** `rule.eic-married-taxpayer-recorded.v1.json:162` (path `inert`,
  value `block`) and `:175` (`eic.married-taxpayer-inert`). The same path is
  in `rule.eic-married-taxpayer-from-separated.v1.json:154`. The fact type
  is `eic-married-taxpayer.bundle.json:29`. No `input-question*.json`
  offers it.
- **Consequence.** A saved return can carry the fact and change line 27a
  from the table credit to a block. Two active paths refuse. The schema
  does require two paths: a one-path copy of the recorded rule fails
  `rule-artifact.v14` with `selection/paths` "is too short".
- **Reproduction.** `q3-no/ssn` with `eic.married-taxpayer-inert` asserted
  yes: line 27a is blocked, including
  `eic-married-taxpayer-recorded:DEPENDENCY_ABSENT`, where the unasserted
  return publishes 2,389. Pointing the inert activity at a fact the return
  already stores (`eic.not-married`) makes `q3-no/ssn` block the same way.
  On `hoh-unmarried/ssn/apart`, where a separated-spouse yes is also
  stored, both paths are active and the run refuses
  (`DEPENDENCY_INVALID`, missing `eic-married-taxpayer-two-paths` and
  `eic-married-from-separated`).
- **Repair.** Keep two paths. Give the second path a value that publishes
  the same result as the default, or reject a stored inert fact at the
  assertion boundary, so a stored value cannot block line 27a or trip the
  exclusive-presence refusal.

## What holds

Decision 4's routing matches the published rules and the live runs.

`rule.eic-married-taxpayer-recorded` publishes 0 when any separated-spouse
answer is stored, 0 for married filing separately with no stored answer, 2
for a head of household with a qualifying child and no stored answer, and 1
otherwise. `rule.eic-married-taxpayer-from-separated` turns a stored yes
into 0 without reading the new fact, and a stored no into 2 only for a head
of household with a qualifying child. `rule.eic-answer.married-taxpayer`
reads the new fact only when that symbol is 2: no publishes 1, yes publishes
0. `rule.eic-answer.separated-spouse` v3 adds one disjunct,
`eic.answer.married-taxpayer` equals 1, beside the v2 skip conditions. The
v102-to-v103 member diff is that version pin plus the five new citizens.
Registry v101 keeps every v100 row and adds those citizens and package
v103. The release differs from v100 only in `version` and
`package_registry_sha256`, and that digest is the v101 file. Loader
declarations, the covered-flag map, and the three family switches for v103
equal v102. No file under `packages/schemas` changes. The four new
`rule.eic-*` files are 4,733, 4,797, 2,422, and 4,305 bytes.

The Rule 3 sentence in the question matches Publication 596 (sha256
`29e8c669…f51dbf`): a person who is married and files as head of household
under the special rules for married taxpayers living apart is still married
for the credit (community-property paragraph, which cites Rule 3). Rule 3
itself is the joint-return requirement plus the special rule for separated
spouses. A head of household who lived apart for the last six months
answers yes and then meets question 4's no. That path kept the table credit
(`hoh-married` with `apart` or `writing` in the 31).

Married filing separately is not asked the new question. With a qualifying
child, a separated-spouse yes kept the table credit and a no published $0,
at 7,000 and again at 5,000, 18,000, and 30,000. A joint filer is outside
Step 3 question 3 because question 2 already skipped it; status class 2
takes the skip. Neither fetched publication defines a spouse who died in
2025 as married or unmarried for question 3. Death is its own married-filing
jointly bullet, and a joint return does not reach question 3.

Hand credits from the 2025 EIC table, single / head of household / qualifying
surviving spouse columns, and the same amounts from `live_coordinate_run`:

| Wages | Band | No valid-SSN child | One valid-SSN child |
| --- | --- | --- | --- |
| 5,000 | phase-in | 384 | 1,709 |
| 7,000 | phase-in | 537 | 2,389 |
| 18,000 | phase-out / plateau | 83 | 4,328 |
| 30,000 | phase-out / past the limit | 0 | 3,261 |

`q3-no`, a recorded separated-spouse yes, and a recorded no followed by
married-taxpayer no matched that table. A married yes followed by a
separated-spouse no, and a married-filing-separately no, stayed 0 while
worksheet line 6 still held the table amount. At 30,000 with a qualifying
child and no valid SSN, `eic.married-taxpayer-recorded` is 1 and the new
question is not asked; line 27a is 0. That is the existing
questions-required skip once the no-child limit has passed. All 31 synthetic
returns at 7,000 matched the hand credit, the blocked flag, and the asked
flags.

The live comparison fails on each Decision 4 mutation and when the inert
path is made reachable, against the same credit and asked-flag assertion as
`tests/test_eic_separated_married_v103.py`:

- A stored no publishes 0 for every status: `recorded-no/ssn/unmarried`
  becomes 0 instead of 2,389.
- A stored yes publishes 2: `hoh-unmarried/ssn/apart` blocks on
  `eic.married-taxpayer` instead of publishing 2,389.
- A married-taxpayer no publishes 0: `q3-no/ssn` blocks on
  `eic.separated-spouse` instead of publishing 2,389.
- A separated-spouse no publishes 1: `q3-yes-no/ssn` and `mfs/ssn/no`
  publish 2,389 instead of 0.
- The inert activity watches `eic.not-married`: `q3-no/ssn` blocks.

The declared replay expectations do not hide a value change. A model diff
whose attribute is `value`, whose identity is line 27a, and whose change is
`changed` from 2,389 to 0 matches none of the eight expectations in
`eic-separated-married-evidence/replay.py`. They name the package version,
the separated-spouse version pin, added rows and nodes for the three new
rules, and one missing-list change from `eic.questions-required` to that
fact plus `eic.answer.married-taxpayer`. `replay-track1.json` reports 775
lists, 0 unexpected, 691 success/success, 84 error/error, and 0 number
changes. Two of those lists were re-run here: both classified as
expected changes, with 0 unexpected. The other 773 were not.

`python3 tools/envelope_scan.py --range github/main..HEAD` exited 0.

## What I ran

- Orientation at HEAD `4ac6b8a6c863c21aa3e58b97b701664876db0049`.
- `git diff --name-status github/main..HEAD` and a structural compare of
  package v102 to v103, registry v100 to v101, release v100 to v101, and
  the v103 loader entries to v102.
- Fetched i1040gi and Publication 596. The PDF sha256 values are the ones
  recorded in `eic-separated-married-evidence/p0.md`. Read Step 3 questions
  3 to 6, the head-of-household marital rules, the special rule for
  separated spouses, Publication 596 Rule 3, and the eligibility checklist.
- Read the 2025 EIC table rows for 5,000, 7,000, 10,000, 12,700, 18,000,
  and 30,000 and compared them with `parameter.eic-table-2025.v2.json`.
- `live_coordinate_run` for all 31 probe keys at wages 7,000; the eight
  keys above at 5,000, 18,000, and 30,000; the question-6 removal and the
  question-6 no; the inert assertion; and the five mutants. Mutants were
  scratch copies. No product file was edited.
- `jsonschema` on `rule-artifact.v14` for the recorded rule and a one-path
  copy.
- The replay expectation matcher against a synthetic line 27a change, and a
  two-list `replay.py v103 --limit 2` run: 2 expected changes, 0 unexpected.
- `python3 tools/envelope_scan.py --range github/main..HEAD`.

## Re-review

Re-review at `c02ad8aea2e9e94777fad51a01db35cda7e64307`, after Decision 8.

**Verdict: NOT READY.**

ESM-R1, ESM-R2, and ESM-R3 are repaired on the measured returns. The question
still does not lead a filer whose spouse died in 2025 to the answer the
instructions give.

### ESM-R4 (high). A spouse who died in 2025 is not led to yes

- **Where.** `packages/content/tax/2025/input-question.eic-married-taxpayer.v1.json:7`
  and the same gloss in `eic-married-taxpayer.bundle.json:19`. The yes
  instruction is "Answer yes if those rules treat you as married." Those
  rules are the interlocutory decree, the final decree, and Publication 596
  Rule 3 for living apart. None of them is the year-of-death rule.
- **What the sources say.** Instructions, Married Filing Jointly: you may
  file jointly if your spouse died in 2025 and you did not remarry. Single
  is for a filer widowed before January 1, 2025. Head of household
  "considered unmarried" does not include that death. Step 3 question 3 yes
  continues. Question 4 yes and question 5 no stop the credit. Death is not
  a decree of separate maintenance.
- **Consequence.** A filer who answers from the gloss, rather than from the
  year-of-death rule, answers no and keeps the table credit. The sources
  stop it.
- **Reproduction.** Head of household, one qualifying child with a valid
  SSN, spouse died on the last day of 2025, same home all year, no decree,
  did not remarry. The instructions treat the filer as married. Question 3
  is yes, question 4 is yes, question 5 is no, and the credit stops. The
  gloss does not say that death means married, and the no sentence names
  only a final decree. A no is the measured `q3-no/ssn` path at wages
  7,000: line 27a is 2,389, the separated-spouse fact is not pinned, and
  question 6 can pass.
- **Repair.** State the year-of-death rule in the question: a spouse who
  died in 2025, if you did not remarry, still means married for question 3.
  Keep the decree and living-apart sentences.

## What holds on re-review

The interlocutory path and the final-decree path now follow the sources.
`test_interlocutory_decree_answers_yes_and_the_credit_stops` passes:
question 3 yes and separated-spouse no, line 27a is 0, and both facts are
pinned. `test_final_decree_shared_household_answers_no_and_keeps_the_table`
passes: question 3 no, line 27a is 2,389, and the separated-spouse fact is
not pinned. A person who was never married is not a married taxpayer, and
none of the added rules treat them as married, so the question's own no is
the answer. A head of household who lived apart and is considered unmarried
is told to answer yes. A final decree is told to answer no. The question
does not say the credit is kept. Question 3 no and question 6 no publishes
line 27a as 0.

A return that does not record `eic.married-taxpayer-inert` still publishes
2,389 on `q3-no/ssn` and on `hoh-unmarried/ssn/apart`, with no two-path
refusal. Asserting any tried value is refused at admission
(`FindingModelError`, `'yes' should not be valid under {}`). The schema
`{"not": {}}` also rejects no, null, an empty string, 0, an object, and a
list. No input question offers the fact, and no other content citizen
records it. The selection paths still name it only as the second activity.

Citizen checksums of the question, the bundle, the four rules, and core
v103 match registry v101. The release digest is the registry file. Loader
v103 still carries v102's covered-flag map, companion declaration, and the
three family switches. The four rule files are unchanged and are 4,733,
4,797, 2,422, and 4,305 bytes.

Each earlier mutant fails a published test. A stored no that publishes 0
fails `recorded-no/ssn/unmarried`. A stored yes that publishes 2 fails
`hoh-unmarried/ssn/apart`. A married-taxpayer no that publishes 0 fails the
final-decree test. A separated-spouse no that publishes 1 fails the
interlocutory test. Pointing the inert activity at `eic.not-married` fails
the final-decree test. `tests/test_content_file_sizes.py` and
`tests/test_eic_separated_married_v103_package.py` passed (6 passed).

## What I ran on re-review

- The repaired question and bundle, the inert `value_schema`, and the
  filing-status and Step 3 text in the 2025 Form 1040 instructions and
  Publication 596 already fetched for the first review.
- The five repair tests and the hand tests for `q3-no/ssn`,
  `q3-yes-no/ssn`, `mfs/ssn/no`, `recorded-no/ssn/unmarried`, and
  `hoh-unmarried/ssn/apart`, through `live_coordinate_run`.
- The same five mutants, in scratch copies, each against the published test
  that asserts the unmutated credit.
- `pytest tests/test_content_file_sizes.py tests/test_eic_separated_married_v103_package.py`
  (6 passed).
- Checksums, the release digest, and the v103 loader entries against v102.
- `python3 tools/envelope_scan.py --range 3a7140624..HEAD` exited 0.

## Second re-review

Second re-review at `6ea305eb44197aed384d2b2aafc65bc189100e38`. That commit
rewrote the question. Governance not read.

**Verdict: NOT READY.**

The body leads every named filer to the Step 3 question 3 answer the 2025
instructions give, and it promises no result. The closing yes list can be
read to answer yes where the body answers no. The new live test stays green
when the 2025 year-of-death sentence is removed.

### ESM-R5 (medium). The closing yes list drops the 2026 marriage limit

- **Where.** `packages/content/tax/2025/input-question.eic-married-taxpayer.v1.json:7`.
  The bundle title states the 2026 rule as one conjunction with marriage at
  the end of 2025. It has no closing yes list.
- **What the question says.** The body, under Married Filing Jointly: "if
  you were married at the end of 2025 and your spouse died in 2026 before
  filing a 2025 return." The close is a list of separate ifs: "Answer yes
  if you were married at the end of 2025, if your spouse died in 2025 and
  you did not remarry in 2025, if your spouse died in 2026 before filing a
  2025 return, ..." The 2026 item stands on its own.
- **What the sources say.** Instructions, Married Filing Jointly, third
  bullet: married at the end of 2025 and the spouse died in 2026 before
  filing a 2025 return. A final decree of divorce or of separate
  maintenance at the end of 2025 means considered unmarried. Step 3
  question 3 no skips questions 4 and 5 and goes to question 6.
- **Consequence.** A filer can follow the broader yes and stop the credit
  the sources still allow. The closing no still names the decree, so the
  two instructions conflict. "Your spouse" after a 2025 divorce is a
  stretch, which is why this is medium.
- **Reproduction.** Final decree of divorce during 2025, same home all
  year, former spouse dies in 2026 before the 2025 return is filed. The
  body answers no: the decree means considered unmarried, and the 2026
  clause applies together with marriage at the end of 2025. The closing
  list answers yes on the 2026 death alone and no on the decree. The yes
  path is question 4 yes and question 5 no. This turn's live call of
  `q3-yes-no/ssn` stops at line 27a of 0. The no path is `q3-no/ssn`. The
  published final-decree test asserts line 27a is 2,389 there, and
  question 6 is still reachable.
- **Repair.** Keep the 2026 death in the same sentence as marriage at the
  end of 2025. State each rule once.

### ESM-R6 (low). The new live test stays green when the year-of-death sentence is removed

- **Where.** `tests/test_eic_separated_married_v103.py:50`.
  `test_spouse_died_in_2025_answers_yes_and_the_credit_stops` calls
  `_row("q3-yes-no/ssn")` and asserts credit 0 with both facts pinned.
  `test_interlocutory_decree_answers_yes_and_the_credit_stops` at line 58
  is the same call.
- **Consequence.** The call passed on the published tree. It passed again
  after both copies of "your spouse died in 2025 and you did not remarry
  in 2025" were removed from a question copy and that citizen checksum and
  the release digest were rewritten. The call never reads the question.
  `tests/test_eic_separated_married_v103_package.py:75` is the assert that
  names the sentence. This turn did not run that file.
- **Repair.** Make a test fail when that sentence is absent.

### What holds

Each named filer, reading the body, reaches the Step 3 question 3 answer
the instructions give.

- Never married: the Single sentence and the closing no. Question 3 no.
- Widowed before January 1, 2025, and did not remarry before the end of
  2025: both say no. Remarriage is "married at the end of 2025," which is
  yes.
- Spouse died in 2025 and did not remarry in 2025: the Married Filing
  Jointly sentence and the closing yes. "A spouse who died is not a decree
  of separate maintenance" blocks the decree no. ESM-R4's filer is led to
  yes, then questions 4 and 5. A shared home and no decree is question 4
  yes, question 5 no, and the credit stops. The question does not promise
  that result.
- Married at the end of 2025 and the spouse died in 2026: the body says
  yes. The closing list also says yes, and says it more broadly (ESM-R5).
- Interlocutory decree: the Head of Household sentence says still married.
  The closing yes agrees.
- Final decree of divorce or of separate maintenance at the end of 2025:
  the body and the closing no say considered unmarried. Question 3 no.
  ESM-R5 is the extra 2026 reading on top of that decree.
- Lived apart and considered unmarried for head of household: Publication
  596, Rule 3, still treats you as married, and the closing yes repeats
  that. Question 3 yes.
- Nonresident-alien spouse, election not made: "You remain married for this
  question" when you are married, the spouse was a nonresident alien at any
  time during the year, and the election was not made. The closing yes
  names that spouse and the missing election. The sentence is about this
  question. Head of household still calls that filer considered unmarried
  for filing status.
- Election made: that sentence does not apply. "Married at the end of 2025"
  is yes. The no list has no election item.

The added sentences match those Single, Married Filing Jointly, and Head
of Household bullets, or they are true on their own: a death is not a
decree of separate maintenance, and the nonresident-alien head-of-household
facts leave the filer married for question 3. The Rule 3 sentence matches
Publication 596's community-property paragraph, which still calls the
person married when they qualify to file as head of household under the
special rules for married taxpayers living apart. "Yes continues to the
separated-spouse questions" and "No skips questions 4 and 5 and continues
to question 6" name routing only. The question does not contain "keep the
credit."

Citizen checksums of the question and the bundle match registry v101. The
v103 package checksum matches its instance. The release digest is the
registry file.

### A shorter question

A shorter text would carry the same rules. The published question is 391
words and states each rule twice. The second statement is where the 2026
limiter is dropped. One statement, 223 words:

> You file as head of household and a child is your qualifying child for the earned income credit. Are you a married taxpayer whose filing status is married filing separately or head of household? Answer yes if any of these is true. You were married at the end of 2025, even if you did not live with your spouse. Your spouse died in 2025 and you did not remarry in 2025. You were married at the end of 2025 and your spouse died in 2026 before filing a 2025 return. An interlocutory decree was in effect at the end of 2025, so you are still married. You are married, your spouse was a nonresident alien at any time during 2025, and the election to treat that spouse as a resident was not made. You lived apart and are considered unmarried for head of household; Publication 596, Rule 3, still treats you as married. Yes continues to the separated-spouse questions. Answer no if you were never married, if you were widowed before January 1, 2025, and did not remarry before the end of 2025, or if a final decree of divorce or of separate maintenance at the end of 2025 means you are considered unmarried. A spouse who died is not that decree. No skips questions 4 and 5 and continues to question 6.

### What I ran on the second re-review

- HEAD `6ea305eb44197aed384d2b2aafc65bc189100e38`. The tree was clean before
  this section.
- The published question and the bundle title.
- Single, Married Filing Jointly, and Head of Household in the fetched 2025
  Form 1040 instructions, and the Publication 596 community-property
  sentence that points at Rule 3.
- A direct call of `test_spouse_died_in_2025_answers_yes_and_the_credit_stops`:
  passed.
- The same call after both copies of the 2025 year-of-death clause were
  removed from a question copy, with that citizen checksum and the release
  digest rewritten: passed. The clause was absent from the copy.
- Citizen checksums of the question and the bundle against registry v101,
  the v103 package checksum, and the release digest against the registry
  file. All three matched.
- The 775 replay and the full suite were left as the builder left them.
