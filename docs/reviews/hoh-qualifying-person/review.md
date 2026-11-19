# Review: head of household needs a qualifying person (core v98)

Reviewer, fresh context. Charter: `docs/reviews/hoh-qualifying-person/charter-review.md`.
Object: `github/main..HEAD` on milestone/hoh-qualifying-person-2025, head
`994d8116` (8 commits; behind `github/main` 0). Orientation block SHA verified
against Git. Governance not read.

## Verdict

**NOT READY.** The rule, package, registry, release and tests are sound and
reproducible, and every mutant I built was caught. Two things block it.
First, the published head of household question, which is the only thing
this milestone adds between a filer and the larger amounts, has two
wordings that lead a filer who does not qualify to answer yes (HOH-R1,
HOH-R2). That leaves part of the defect the milestone exists to close in
place. The wording is cheap to fix before the v98 bytes merge and becomes
published history once they do. Second, the required `verify` gate has not
run on this head (HOH-R7).

## Findings

Ordered by consequence.

### HOH-R1 (Medium, semantic, too favourable): the "considered unmarried" example drops the child requirement

`packages/content/tax/2025/input-question.hoh-tests-met.v1.json:7`: "considered
unmarried (for example, married but your spouse did not live in your home for
the last 6 months of 2025)". Both sources make lived-apart only one of several
conditions. The filer must also file separately, pay over half the cost of
the home, have a home that was the main home of their child, stepchild or
foster child for more than half the year, and be able to claim that child
(2025 Form 1040 instructions, "Married persons who live apart"; Pub. 501,
"Considered Unmarried", tests 1-5).

Scenario: a demo filer is married, the spouse moved out in May 2025, there is
no child, and the filer pays all the costs of a dependent parent's apartment
(Test 1). The example tells the filer they are considered unmarried, so they
answer yes. Line 12e becomes 23,625 and the tax is figured in the head of
household column. The filer is not considered unmarried and should file
married filing separately (15,750). Nothing else on the record contradicts
the yes, so the refund is silently too favourable.

Smallest repair: give the full condition in the example (married, lived apart
the last 6 months, and your child, stepchild or foster child whom you can
claim lived with you more than half the year), or remove the example. Do this
before merge by regenerating v98, or later with a question successor. The
foreman decides which.

### HOH-R2 (Medium, semantic, too favourable): "a relative you can claim as a dependent" admits people who are not qualifying persons

Same file and line: "a qualifying person, such as your child or a relative you
can claim as a dependent, lived with you there for more than half of 2025".
Test 2 of the 2025 instructions excludes "any person who is your dependent
only because the person lived with you for all of 2025" and any dependent
claimed under a multiple support agreement. Pub. 501 Table 4 also limits a
qualifying relative other than a parent to the listed relationships. The
example in the question invites both kinds of filer to answer yes.

Scenario: an unmarried filer's cousin lived with them all of 2025 and is
claimed as a qualifying relative under the member-of-household test. A cousin
is "a relative you can claim as a dependent", so the filer answers yes and
gets head of household. The cousin is not a qualifying person, and the filer
is single. The same happens with a sibling claimed under a multiple support
agreement.

Smallest repair: narrow the example to the listed relationships and name the
two exclusions, or replace the example with "a qualifying person (see Pub. 501
Table 4)".

### HOH-R3 (Low, semantic, against the filer): the surviving spouse question is narrower than its own answer and the sources

`packages/content/tax/2025/input-question.qss-tests-met.v1.json:7` says "a
child or stepchild ... you can claim as a dependent who lived in your home all
of 2025". The answer's fact-type title
(`packages/content/tax/2025/filing-status-tests.bundle.json:44`) and both
sources also accept a child you could claim except that the child had gross
income of $5,200 or more, filed a joint return, or you could be claimed by
someone else. The sources also count temporary absences, and a birth or death
during the year, as living in the home. So the question and the answer it
records mean different things.

Scenario: the filer's spouse died in 2024. Their 20-year-old child, not a
student, lived at home all year and earned 6,000. The filer cannot claim the
child, answers no, and is told "you cannot file as a qualifying surviving
spouse". That is false. The 31,500 deduction and the joint-return column are
refused, and the filer is pushed to a worse status. The same happens with a
child born in March 2025.

This fails closed, but it misdirects the filer. Repair: carry the fact title's
three exceptions, plus "except temporary absences, birth or death", into the
question.

### HOH-R4 (Low, semantic, against the filer and next step): three head of household cases the question handles poorly

Same file as HOH-R1.

- **(a) Parent-only filer.** The main clause requires "you paid more than half
  the cost of keeping up your home". A filer whose only qualifying person is
  a dependent parent in a rest home, and who shares their own home equally,
  fails that clause as written and answers no. Test 1 only needs over half
  the cost of the parent's home. The fact title gets this right.
- **(b) Spouse died in 2025.** Pub. 501 says that filer is considered married
  for the whole year. The question asks whether they were "unmarried" on
  December 31 and does not mention a 2025 death or a joint return. The
  surviving spouse question does. This is not too favourable, because a joint
  return gives more than head of household.
- **(c) What to do after "no".** "Change your filing status" does not say that
  a married filer who fails head of household usually files married filing
  separately, not single.

Repair: reword when HOH-R1 and HOH-R2 are fixed.

### HOH-R5 (Low, claim accuracy): the preferential-rate ceilings are not all downstream of line 3

The rule notes (`packages/content/tax/2025/rule.dependents-worksheet-line-3.v2.json:150`)
and the plan's P0 result say that every larger amount either status carries,
"preferential-rate ceilings" included, is downstream of this rule. That is not
true of the ceilings themselves. `rule.qdcg-worksheet.line-6` and
`rule.qdcg-worksheet.line-13` require only `filing_status`.

I ran live on published v98 with the answer "no":

| Case | Line 6 | Line 13 |
| --- | --- | --- |
| head of household | 64,750 | 566,700 |
| qualifying surviving spouse | 96,700 | 600,050 |
| single control | 48,350 | 533,400 |

Every worksheet line that combines a ceiling with taxable income (line 7
onward) blocks, so no amount on the return changes. The behaviour is
acceptable. The claim is overstated in a published note. Repair: correct the
plan and p0.md wording. The rule note is published bytes, so it can only be
fixed by regenerating before merge, or else left with this review on record.

### HOH-R6 (Low, documentation): Decision 6 misstates the earned income credit

`docs/phases/engine-breadth/milestones/hoh-qualifying-person.md:94-96` says
that AGI and the earned income credit "equal the single amounts" on a refused
or unanswered status. For a head of household with no qualifying child,
`rule.eic-status-class` gives class 0, so the credit is $0 where single gets
one (`probe-v97.json`: hoh/relative/low 0 against single/none/low 542). The
conclusion, that these amounts are not too favourable, still holds. Repair:
say "equal to or less than".

### HOH-R7 (Low, publication gate): `verify` has not run on this head

PR #294's `verify` check at `994d8116` concluded FAILURE because the PR is a
draft: "Draft PR: the full suite has not run on this head". `track1.md` does
not report the full-suite and mypy result lines that its charter asked for.
My own mypy and fast-lane runs were green (below). They do not stand in for
the gate. Repair: mark the PR ready and reference a green `verify` on the
exact head.

## What was verified (reusable by a repair)

- **Sources.** The local 2025 Form 1040 instructions and Pub. 501 PDFs match
  the sha256 values in p0.md. I re-extracted them with `pdftotext` and read
  them independently: i1040gi Head of Household, Tests 1-2, "Married persons
  who live apart", Qualifying Surviving Spouse; Pub. 501 Head of Household,
  Considered Unmarried, Qualifying Person and Table 4, Qualifying Surviving
  Spouse, and "Spouse died during the year".
- **Q1, the cases the charter named.** A dependent parent living elsewhere is
  handled by the parenthetical (but see HOH-R4a). A qualifying child claimed
  by the other parent is handled: "such as your child" does not require a
  dependent, and the custodial child lives with the filer. A foster child is
  correctly excluded for the surviving spouse status. A spouse who died in
  2025 is handled in the surviving spouse question but not in the head of
  household question (HOH-R4b). A considered-unmarried filer is misled
  (HOH-R1).
- **Q2, other routes to the larger amounts.** All 36 v98 members that mention
  filing status were enumerated, and every status-keyed parameter they read
  was checked:
  - Only line 3 reads `tax.us.2025.parameter.standard-deduction-base`.
  - The rate schedule (qdcg lines 22 and 24) needs taxable income.
  - Line 12e v4 requires the standard deduction on every route, itemizing
    included (`requires`, no default), so an itemizer is refused too.
  - The additional deduction, capital-loss limit, mortgage limit, Social
    Security, student loan, Schedule 1-A, child tax credit, direct foreign tax
    credit and earned income credit tables give head of household and
    qualifying surviving spouse the single amount or less.
  - The only exception is HOH-R5, which reaches no amount. No other rule gives
    a larger amount for either status without passing through line 3.
- **Q3, nothing else moved.** On single, joint and separate returns the rule
  takes v1's lookup unchanged. The probes show yes keeps every watched line
  of v97 on all six cases. Decision 5 is accurate: Step 4 question 1 of the
  2025 instructions stops only a married filer whose status is married filing
  separately or head of household, while `rule.eic-status-class` puts every
  head of household in class 0.
- **Q4, publication.**
  - The only modified files are `packages/tax/loader.py` and
    `tests/test_noncovered_sales_v78_switch.py`. Everything under
    `packages/content` and the release is new.
  - Registry v96 is add-only: four citizens and one package.
  - Release v96 differs from v95 only in its version and registry digest.
  - The loader's v98 entries are textually identical to v97's.
  - `_successor_graphs` falls back to the v96 entry, whose interest members
    v98 does not touch, so no new entry is needed.
  - Byte reproduction: a scratch copy of HEAD without the six v98 files,
    rebuilt from v97 plus `design.py` through
    `tools.package_successor.generate_to_directory`, which validates package,
    registry and release, gives byte-identical package v98, registry v96,
    release v96, rule v2, bundle and both questions.
- **Q5, replay.** `replay-published-v98.json`: 775 pass, 0 unexpected, 691
  expected-change lists and 84 identical (`error/error` on both cores). The
  `version_change` expectations match only `version` and `pinVersion`
  attributes of the named ids, so they could not hide a value change. All 775
  lists are single (`census.json`), so the replay shows nothing changed for
  single filers only. Joint, separate, head of household and surviving spouse
  rest on the probes and the live tests. The two unused question expectations
  are explained by that census.
- **Q5, mutants.** Each mutant was rebuilt and validated through
  `generate_to_directory`, so it was a valid package rather than a checksum
  break, then run against both milestone test modules in a scratch copy:

  | Mutant | Result | Tests that failed |
  | --- | --- | --- |
  | head of household "no" publishes the lookup | caught | 3: the no-refuses test on both cases, and the successor-shape test |
  | qualifying surviving spouse yes takes the head of household amount | caught | 3 |
  | single, joint and separate read the head of household answer | caught | 4: both controls, separate, shape |
  | qualifying surviving spouse branch reads the head of household answer | caught | 7 |
  | "no" blocks as DEPENDENCY_ABSENT | caught | 2 |
  | v98 adds one extra entrypoint | caught | 1: exact-admission test |

  The unmutated rebuild passes.
- **Limits.**
  - Correcting the answer from yes to no is not exercised end to end. The
    dependency edge exists: `replay-paired.json` shows the line 3 finding now
    pins the answer.
  - The itemizing route is established from the rule structure, not from a
    live run.

## What I ran

- `python3 tools/build_orientation_block.py --ref HEAD --charter docs/reviews/hoh-qualifying-person/charter-review.md --role reviewer`, then `git fetch github --prune` and `git rev-list --left-right --count github/main...HEAD`, which gave 0 behind and 8 ahead.
- `python3 tools/envelope_scan.py --range github/main..HEAD`: exit 0, clean.
- `python3 tools/governance_lint.py`: conformant.
- `pytest tests/test_hoh_qualifying_person_v98.py tests/test_hoh_qualifying_person_v98_package.py tests/test_noncovered_sales_v78_switch.py tests/test_schema_registry.py`: 42 passed.
- `python3 -m mypy`: no issues in 524 files.
- `pytest -m "not live"`: 1906 passed, 8 skipped.
- `gh pr view 294` checks and `gh run view --log-failed`: the draft-PR `verify` failure.
- A live `live_coordinate_run` on published v98 (head of household no, surviving spouse no, single) reading the publications of qdcg lines 6 and 13.
- The six mutants and the unmutated rebuild, in a scratch copy of HEAD outside the repository. No mutation was committed.
- `pdftotext` re-extraction of both source PDFs, and a direct read of the content files, tests, loader diff, validator table and evidence.
