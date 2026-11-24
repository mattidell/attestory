# Track 1: Step 3 question 3 on core v103

Track 1 of eic-separated-married. Plan:
`docs/phases/engine-breadth/milestones/eic-separated-married.md`.
Charter: `docs/reviews/eic-separated-married/charter-track1.md`.
Decisions 1 to 7 bind. Published baseline on main is core v102, registry
v100, release v100. This track publishes core v103, registry v101, and
release v101. No kernel change and no engine change.

## Design as built

A recorded separated-spouse answer and the new fact can both be present, so
the new fact is not a second selection path. `exclusive_presence` would
refuse two active paths. The yes-or-no tree also does not fit in one rule
file under the 5,000-byte cap, so the work is three rules.

`rule.eic-married-taxpayer-recorded` v1 publishes
`eic.married-taxpayer-recorded`. Any recorded separated-spouse answer
publishes 0 and does not read the value. With no separated answer, the
default publishes 1 when the separated-spouse question is skipped, 0 for
married filing separately, and 2 for a head of household with a qualifying
child.

`rule.eic-married-taxpayer-from-separated` v1 publishes
`eic.married-taxpayer-from-separated`. When a separated answer is present it
reads the value. Yes publishes 0. No publishes 2 only when filing status is
head of household and `eic.qualifying-child-present` is 1; every other
recorded no publishes 0. When no separated answer is present, the default
publishes the recorded symbol, so married filing separately stays 0, a skip
stays 1, and an unanswered head of household with a qualifying child stays 2.

`rule.eic-answer.married-taxpayer` v1 reads `eic.married-taxpayer` only when
that from-separated symbol is 2. No publishes 1, which skips questions 4 and
5. Yes publishes 0, so the separated-spouse rule reads the separated answer.
Any other symbol is published through and the new fact is not read. A
recorded separated-spouse yes therefore still passes with no new answer.

`rule.eic-answer.separated-spouse` v3 adds the new answer symbol beside v2.
A 1 skips the separated-spouse fact. A 0 falls through to the recorded
answer, or blocks on it when none is recorded.

The inert fact `eic.married-taxpayer-inert` stays in the bundle and is not
an input question. A one-path selection was rejected. `SchemaValidationError`
on that rule is `MEMBER_SCHEMA_INVALID`: `instance does not conform to
rule-artifact.v14: selection/paths: ` followed by the single path and ending
` is too short`. `rule-artifact.v14` sets `selection.paths` `minItems` to 2.
The second path is active only when that inert fact is recorded. Nothing
records it and nothing asks it.

## Question

Fact `tax.us.2025.eic.married-taxpayer`. Domain yes or no. No default.

Step 3 question 3 of the 2025 Form 1040 instructions, line 27a, printed page
41 (quotes and PDF checksums are in `p0.md`):

> Are you a married taxpayer whose filing status is married filing separately or head of household?

Yes continues. No skips questions 4 and 5 and goes to question 6.

Publication 596, printed page 5, lines 454-460, still treats a head of
household who lived apart as married for the credit. Rule 3, printed page 5,
lines 531-537, says a married person must usually file a joint return, with
the special rule for separated spouses. Questions 4 and 5 are that special
rule. The new question does not repeat them.

The input question:

> You file as head of household and a child is your qualifying child for the earned income credit. Are you a married taxpayer whose filing status is married filing separately or head of household? Answer yes if you were married at the end of 2025. Publication 596, Rule 3, still treats you as married when you file as head of household under the special rules for married taxpayers living apart. Yes continues to the separated-spouse questions. Answer no if you were not married at the end of 2025. No skips those questions and you keep the credit.

Asked of a head of household with a qualifying child, including one who
already answered the separated-spouse question no. Married filing separately
is already married by filing status and is not asked.

## Files

New citizens, each under the 2025 content directory:

| File | Bytes |
| --- | --- |
| `rule.eic-married-taxpayer-recorded.v1.json` | 4,733 |
| `rule.eic-married-taxpayer-from-separated.v1.json` | 4,797 |
| `rule.eic-answer.married-taxpayer.v1.json` | 2,422 |
| `rule.eic-answer.separated-spouse.v3.json` | 4,305 |
| `eic-married-taxpayer.bundle.json` | 2,057 |
| `input-question.eic-married-taxpayer.v1.json` | 766 |

`package.core-calculations.v103.json` is 241,297 bytes.
`published-packages.v101.json` is 321,119 bytes. Both are larger than 200 KB
because v102 and v100 already are. Release
`demo.release.sli-worksheet-integration.2025.v101.json` differs from v100
only in version and the registry digest. The v103 loader entries carry the
v102 companion declaration and covered-flag map. No schema manifest changed.
Published v102 files were not edited.

## Hand credit

Wages are 7,000. The 2025 table's other-0 column is 537 and other-1 is
2,389. Thirty-one synthetic demo.* returns match those credits and the asked
flags through `live_coordinate_run`.

A qualifying child with a valid SSN keeps 2,389. A qualifying child without
one keeps 537. Married filing separately keeps 0 and is not asked the new
question. A recorded separated-spouse yes, whether the filer lived apart or
has a written separation, keeps that table credit and is not asked the new
question. A recorded separated-spouse no with the new answer no keeps 2,389
or 537 and is not asked questions 4 and 5. The same recorded no with the new
answer yes keeps 0, and questions 4 and 5 are asked. Leaving the new answer
off that recorded-no return blocks on `eic.married-taxpayer`. Answering the
new question yes and leaving the separated-spouse answer off also blocks on
that fact. Answering yes and then no keeps 0.

## Replay

Strict full-surface replay of the 775 recorded lists, published v102 against
published v103. All 775 are filing status single. None carries a
separated-spouse answer. 691 are success on both cores and 84 error on both
cores with the same snapshot. Zero lists fail the declared expectations.
Zero expectations are unused. Zero lists change outcome, so none newly
block. Zero recorded numbers change. The declared differences are the
package pin v102 to v103, the separated-spouse pin v2 to v3, disposition
rows and nodes for the three new rules, and the separated-spouse missing
list also naming the new answer symbol. `replay-track1.json` is that
summary.

## Tests

`tests/test_eic_separated_married_v103_package.py` checks the published
bytes, the add-only registry, the release digest, and the v103 loader
entries. `tests/test_eic_separated_married_v103.py` runs all 31 cases
through `live_coordinate_run`. The covered-flag refusal list now includes
v103 because the loader entry carries v102's map.

Three scratch mutants of the from-separated rule fail that hand assertion.
A recorded no that always publishes 2 makes `mfs/ssn/no` block on
`eic.married-taxpayer` instead of credit 0. A recorded no that always
publishes 0 makes `recorded-no/ssn/unmarried` credit 0 instead of 2,389 and
does not ask the new question. A recorded yes that publishes 2 makes
`hoh-unmarried/ssn/apart` block on `eic.married-taxpayer` instead of credit
2,389.

`pytest -m "not live"` passed (1,962 passed, 8 skipped, 5,993 subtests; the
count is the rerun after the refusal-list edit). `tests/test_content_file_sizes.py`
is not on this branch. The two live size tests, `-k 5kb` in
`tests/test_earned_income_credit_track1.py` and
`tests/test_eic_qualifying_children_track1.py`, passed. `python3 -m mypy`
reported no issues in 538 source files. The live 31 passed.
