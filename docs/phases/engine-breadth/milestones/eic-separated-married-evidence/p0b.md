# P0b: Step 3 question 3, asked only of a head of household with a qualifying child

P0b of eic-separated-married. Plan:
`docs/phases/engine-breadth/milestones/eic-separated-married.md`.
Charter: `docs/reviews/eic-separated-married/charter-p0b.md`.
Decisions 1 to 3 in the plan bind. Published baseline is core v102, registry
v100, release v100. The scratch successor is core v103, registry v101,
release v101. Nothing in packages/ or tests/ was edited.

| File | What it is |
| --- | --- |
| `design.py` | The new fact, the input question, and the three successor rules |
| `build.py` | Writes those into a scratch copy of v102 and validates the package |
| `build-p0b.json` | Validation result and rule-file sizes |
| `hand.py` | The 2025 table credit each synthetic case should keep |
| `probe_p0b.py` | Twenty-seven synthetic demo.* returns through `live_coordinate_run` |
| `trace-p0b.json` | Those twenty-seven runs on the scratch successor |
| `replay.py` | Full-surface replay of the 775 recorded lists, with the differences declared |
| `replay-p0b.json` | What that replay found |

## Question

The new fact is `tax.us.2025.eic.married-taxpayer`, modeled on
`eic.not-married`: its own bundle, its own input question, domain yes or no.
`eic.not-married` is not reused. On v102 that question is withheld when a
qualifying child is present, and its words treat a decree of separate
maintenance as unmarried without the year-end household test in Step 3
question 5.

Step 3 question 3 of the 2025 Form 1040 instructions, line 27a, printed page
41 (the quotes and the PDF checksums are in `p0.md`):

> Are you a married taxpayer whose filing status is married filing separately or head of household?

Yes continues. No skips questions 4 and 5 and goes to question 6.

Publication 596, Rule 3, printed page 5: if you are married, you must usually
file a joint return to claim the EIC, with a special rule for separated
spouses. The special rule, printed page 6, matches the instructions: married,
not filing a joint return, a qualifying child who lived with the filer for
more than half of 2025, and either the last-six-months prong or the
written-separation-or-decree prong with a different household at the end of
2025. The same publication, printed page 5, says a married person who
qualifies to file as head of household under the special rules for married
taxpayers living apart is still married for this credit.

The question a head of household with a qualifying child is asked:

> You file as head of household and a child is your qualifying child for the earned income credit. Are you a married taxpayer whose filing status is married filing separately or head of household? Answer yes if you were married at the end of 2025. You are still married for this credit if you file as head of household because you are considered unmarried after living apart from your spouse: Publication 596 says a married person who qualifies to file as head of household under the special rules for married taxpayers living apart is still married, and Rule 3 still applies. Yes continues to the separated-spouse questions. You can take the credit only if the child lived with you for more than half of 2025 and either you lived apart from your spouse for the last 6 months of 2025, or you are legally separated according to your state law under a written separation agreement or a decree of separate maintenance and you did not live in the same household as your spouse at the end of 2025. Answer no if you were not married at the end of 2025. No skips those questions and you keep the credit.

Married filing separately is not asked. Filing status already answers
question 3 yes. A person who files as head of household because they lived
apart answers yes. A decree of separate maintenance is still yes here;
question 5 is where that decree is tested. No means not married at the end
of 2025.

## How a recorded yes still passes

`exclusive_presence` refuses when two paths are active, and both a new
"married" answer and a separated-spouse answer can legitimately be present,
so the new fact is not a second path. The rule schema still requires two
paths. The second path watches `eic.married-taxpayer-inert`, a fact nothing
asks and no return records. It stays inactive.

`rule.eic-married-taxpayer-recorded` v1 then does this:

- The path `separated-recorded` is active when `eic.separated-spouse` is
  present. Presence is enough; the value is not read. The path publishes 0.
- The path `inert` is active only when the inert fact is present. It blocks,
  and it never activates on these returns.
- The default, when no separated-spouse answer is present, publishes 1 on the
  same skips as separated-spouse v2 (questions not required, no qualifying
  child, or status class not 0). It publishes 0 for married filing
  separately. It publishes 2 for what remains: a head of household with a
  qualifying child and no recorded separated-spouse answer.

`rule.eic-answer.married-taxpayer` v1 requires the recorded symbol, not the
new fact. When the symbol is not 2 it publishes that symbol and does not
read the new fact. When the symbol is 2 it reads
`eic.married-taxpayer` through a conditional dependency set (ADR 0081: the
fact is bound on that branch only). No publishes 1, which skips questions 4
and 5. Yes publishes 0, which makes the separated-spouse question required.
An absent fact blocks and names `eic.married-taxpayer`.

`rule.eic-answer.separated-spouse` v3 is v2 plus one more skip: it also
publishes 1 without reading `eic.separated-spouse` when the new answer
symbol is 1. A 0 falls through to the v2 read. A recorded yes therefore
publishes 1, the credit is kept, and the new question is not pinned.

A married yes together with a separated-spouse no does not pin the new
question either. The separated answer selects the path, so the new fact is
not read. The separated answer no still publishes 0 and the credit is $0.
That is the same result v102 gives a recorded no.

## Trace

Twenty-seven synthetic returns, wages 7,000, through `live_coordinate_run`
on the scratch successor. The twenty-one P0 cases still record a
separated-spouse answer and do not record the new fact. `q3-no` is an
unmarried head of household who answers the new question no and records no
separated-spouse answer. `q3-yes` answers yes and leaves questions 4 and 5
unanswered. `q3-yes-no` answers yes and then separated-spouse no. A question
counts as asked when the answer publication pins the fact.

Wall time 24.5 seconds. Zero errors. All twenty-seven line 27a amounts equal
the hand credit, and all twenty-seven asked flags match. The table amount at
these wages is 2,389 with one qualifying child who has a valid SSN
(`demo-esm-child-ssn`) and 537 when the child has no valid SSN
(`demo-esm-child-nossn`) or when the credit is the self-only column.

| Case | Line 27a | Instruction | Married asked | Separated asked |
| --- | --- | --- | --- | --- |
| hoh-married/none | 0 | 0 | no | no |
| hoh-married/nossn/apart | 537 | 537 | no | yes |
| hoh-married/nossn/no | 0 | 0 | no | yes |
| hoh-married/nossn/writing | 537 | 537 | no | yes |
| hoh-married/ssn/apart | 2,389 | 2,389 | no | yes |
| hoh-married/ssn/no | 0 | 0 | no | yes |
| hoh-married/ssn/writing | 2,389 | 2,389 | no | yes |
| hoh-unmarried/none | 537 | 537 | no | no |
| hoh-unmarried/nossn/apart | 537 | 537 | no | yes |
| hoh-unmarried/nossn/no | 0 | 537 | no | yes |
| hoh-unmarried/nossn/writing | 537 | 537 | no | yes |
| hoh-unmarried/ssn/apart | 2,389 | 2,389 | no | yes |
| hoh-unmarried/ssn/no | 0 | 2,389 | no | yes |
| hoh-unmarried/ssn/writing | 2,389 | 2,389 | no | yes |
| mfs/none | 0 | 0 | no | no |
| mfs/nossn/apart | 537 | 537 | no | yes |
| mfs/nossn/no | 0 | 0 | no | yes |
| mfs/nossn/writing | 537 | 537 | no | yes |
| mfs/ssn/apart | 2,389 | 2,389 | no | yes |
| mfs/ssn/no | 0 | 0 | no | yes |
| mfs/ssn/writing | 2,389 | 2,389 | no | yes |
| q3-no/nossn | 537 | 537 | yes | no |
| q3-no/ssn | 2,389 | 2,389 | yes | no |
| q3-yes-no/nossn | 0 | 0 | no | yes |
| q3-yes-no/ssn | 0 | 0 | no | yes |
| q3-yes/nossn | blocked | unanswered | yes | no |
| q3-yes/ssn | blocked | unanswered | yes | no |

The four unmarried head-of-household returns with a qualifying child and a
recorded separated-spouse yes (`apart` and `writing`) keep 2,389 or 537.
The new question is not asked. The recorded symbol is 0, the separated
answer publishes 1, and the credit is the table amount. That is the recorded
yes Decision 2 required.

`q3-no` is the unmarried filer with no separated-spouse answer. The recorded
symbol is 2, the answer symbol is 1, separated-spouse publishes 1 without
reading that fact, and the table credit is kept. Questions 4 and 5 are not
asked.

`q3-yes` blocks. The new question is pinned. The separated-spouse question is
not pinned, because the run blocks with `DEPENDENCY_ABSENT` before that
publication. The missing names include `eic.separated-spouse`, so questions
4 and 5 are required and unanswered. Worksheet A line 6 is still 2,389 or
537.

`q3-yes-no` records both answers. The separated answer selects the path, so
the new fact is not pinned. Separated-spouse no publishes 0 and line 27a
is $0.

`hoh-unmarried` with a qualifying child and a recorded separated-spouse no
stays at $0. The new question is not read, so a recorded no keeps the v102
result. The instruction credit for that filer is the table amount. None of
the 775 recorded lists is in this bucket.

Married filing separately never asks the new question. With a qualifying
child, one separated prong keeps 2,389 or 537 and a no keeps $0. With no
child, the early stop keeps line 27a at $0 and nothing is asked.

## Replay

Full-surface replay of the 775 recorded lists, published v102 against the
scratch successor. Every list is filing status single. None carries
`eic.separated-spouse`.

Outcomes: 691 success on both cores, 84 error on both cores. The 84 error
snapshots are identical on the two cores, so the successor does not add
them. No list moves from success to a blocked or error outcome. No list
changes a number.

The engine comparison ran once. The differences it reported, beyond the
package pin and the two new disposition rows, are structural, and each one
is stored in full. Declaring them leaves nothing unmatched: the package pin
v102 to v103, the two new rows and their place in disposition order, the
disposition nodes those rules add, the separated-spouse rule pin v2 to v3
where the explanation graph carries it (2 lists), and that rule's missing
list also naming `eic.answer.married-taxpayer`. 691 lists are then expected
changes and 84 are identical.

On 370 lists the two new rules block with `DEPENDENCY_ABSENT` because
`eic.questions-required` is absent, and the answer rule then misses the
recorded symbol. The separated-spouse disposition was already blocked on
`eic.questions-required` and stays blocked. The return outcome stays
success. These are single filers with no separated-spouse answer. They do
not block on the new question.

On the other 321 successful-or-matching lists the new rules do not add that
blocked node. One examined list, a single filer, publishes both new rules,
and no number on that list changes.

## Size

| File | Bytes |
| --- | --- |
| `rule.eic-married-taxpayer-recorded.v1.json` | 4,923 |
| `rule.eic-answer.married-taxpayer.v1.json` | 2,386 |
| `rule.eic-answer.separated-spouse.v3.json` | 4,305 |

The cap is 5,000 bytes. None is over it. The new files are not in the
7,000-byte exception list. `pytest tests/test_earned_income_credit_track1.py
tests/test_eic_qualifying_children_track1.py -k 5kb` passed: 2 tests.

## Decisions for the foreman

1. The rule language can say what Decision 2 asked. A recorded
   separated-spouse yes, with no new answer, still passes. The mechanism is
   the `exclusive_presence` path above. No engine change and no ADR.
2. A recorded separated-spouse no also keeps the v102 result, including $0
   for an unmarried head of household who already answered that question no.
   The new question is what lets that filer skip questions 4 and 5, and only
   when no separated-spouse answer is recorded.
3. A married yes and a separated-spouse no together do not pin the new
   question. Both answers select the separated path. The credit is $0.
4. No recorded list newly blocks, and no recorded list changes a number.
   All 775 are single filers. 370 of them gain a blocked disposition on the
   two new rules because `eic.questions-required` is absent. That block does
   not change the return. Track 1 can publish this shape.
5. The three rule files are under the 5,000-byte cap, and the live size
   tests passed.
