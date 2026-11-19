# Review: every earned income credit answer has a question (2025)

Charter: `docs/reviews/eic-answer-questions/charter-review.md`. Reviewer:
fresh context, oriented with `tools/build_orientation_block.py --ref HEAD`
at `76bd1569` on milestone/eic-answer-questions-2025. Range
`github/main..HEAD`: 5 commits, behind 0. Governance was not read.

## Verdict

**NOT READY.** The publication is clean. Core v100 adds exactly four
`input-question` members and four entrypoints. Registry v98 and release v98
only add entries. The loader's v100 entries carry v99's. A rerun replay found
no number or disposition change. Two things block READY. The age question
gives the wrong answer in a case Publication 596 describes (EAQ-R1). Nothing
records or tests the polarity of the dependent question (EAQ-R2). Both are
content or test repairs on files that are not yet on `main`. The `verify`
gate has not run on this head (EAQ-R8).

## Findings (ordered by consequence)

### EAQ-R1 (medium, semantic): the age question says "yes" for a decedent who died before reaching 25

`packages/content/tax/2025/input-question.eic-age-25-under-65.v1.json:7`
(and `eic-answer-questions-evidence/design.py:29`).

The question's second sentence is unconditional: "Answer yes if you, or your
spouse if you file a joint return, were born after December 31, 1960, and
before January 2, 2001." Its third sentence adds the death rule only as
another way to answer yes. Pub. 596 Rule 11 (p596 1728-1730, 1747-1749)
overrides the birth-date test for a person who died: "Even if your spouse was
born before January 2, 2001, they aren't considered at least age 25 at the
end of 2025 unless they were at least age 25 at the time of death." The same
override is stated for a taxpayer who died.

Failure scenario, Pub. 596's own Example 2 (p596 1736-1739). A joint return.
The surviving filer is 23. The spouse was born February 14, 2000 and died
February 12, 2025, so is not considered 25. Under the law the age test fails
and the credit is $0. A filer who reads the question literally answers yes
under the birth-date sentence, and the credit is allowed. A deceased filer
born in 2000 who died in 2025 before turning 25 hits the same case. P0 and
plan Decision 2 say the death rules were checked against Rule 11, but the
override sentence is missing.

Smallest repair: make the birth-date sentence apply only to a living person,
or add Pub. 596's override, for example "If the person died in 2025, answer by
their age at death instead: ...". The file is not yet published on `main`, so
the repair can reword this v1 and its design text before merge.

### EAQ-R2 (medium, evidence): the dependent question's polarity is recorded nowhere a test reads, and reversing it passes every test

`eic-answer-questions-evidence/design.py:57` (`POLARITY`, read by no test or
tool); `tests/test_eic_answer_questions_v100.py:37` (the comment promises a
"polarity" field, but the `ANSWERS` tuples have none);
`tests/test_scope_answer_questions.py` (`GROUPS`, which checks the convention
for EIC1-EIC4, does not list the four new questions).

The wording is correct. "Can you be claimed as a dependent ...?" follows
Step 4 question 6 (i1040gi 4583-4589). Under the published convention its yes
records `eic.not-claimable-as-dependent` = no, and the fact's title says "No
means the credit is $0". So a yes stops the credit, as the charter requires.
But `input-question.v1` has no polarity field. The convention lives only in
`design.py`, and nothing checks it. P0 section 6 recommended "a test that each
question's polarity matches its fact (as tests/test_scope_answer_questions.py
does for EIC1-EIC4)". Track 1 did not build it.

Mutation, run in a scratch copy and not committed: the question was reworded
positively ("Is it true that no one can claim you as a dependent on their 2025
tax return?"), `POLARITY` was flipped to `pos`, and v100, registry v98 and
release v98 were regenerated with `build.py`. Results:

- the two new test files: 25 passed;
- `test_scope_answer_questions`, `test_input_questions`,
  `test_all_questions_at_once`, `test_question_wording_v87` (both),
  `test_derived_answers`, `test_schema_registry` and `test_track1_memos`:
  471 passed.

A reversed or inconsistent polarity therefore reaches publication
undetected. Smallest repair: give each of the four questions an explicit
polarity in a test, either by adding them to `GROUPS` (with `abs` for the
dependent question and `pos` for the other three) or by an equivalent check
that ties the question's yes to the fact value that keeps the credit.

### EAQ-R3 (low, evidence): a sibling consumer of the spouse SSN fact gains the question; it is not in the census or the tests

`packages/content/tax/2025/rule.ctc-filer-ssn-gate.json:105,114` reads
`tax.us.2025.eic.spouse-valid-ssn`. P0's census
(`eic-answer-questions-evidence/p0.md:67-73`) lists only the earned income
credit rules that read it.

Reproduced in a scratch copy with the probe's builder: a joint return with a
child (wages 30,000), the taxpayer SSN answer set to no, and the spouse SSN
answer removed. On v99, Form 1040 lines 19, 24, 27a, 28 and 32-37,
Schedule 8812 lines 14 and 17, and tax after credits are blocked with no
sentence. On v100 every one of those lines shows the spouse SSN question.
The blocked rules are identical, and no value changes. For the child tax
credit this is an improvement, and the wording fits its SSN test. But the
change reaches beyond the credit the plan names. No recorded or probe list
covers it, so the replay's "question shown" expectation (which matches the
sentence on any line) was never exercised there.

Repair: name the child tax credit reader in the census or track notes, and
pin this case in the live test.

### EAQ-R4 (low, evidence): the census omits the tie-breaker roster answers the credit reads

`eic-answer-questions-evidence/p0.md:67-73`; plan
`docs/phases/engine-breadth/milestones/eic-answer-questions.md:85`.

The census table "every other fact a credit rule reads that no rule
publishes" lists `filing-status`, the roster closure and `eic.child.*`.
`rule.eic-child.counts` v2 also reads `dtb.child.tie-breaker-clear`, which
reads ten `dtb.child.*` answers per child. None of those has an
`input-question`. That was confirmed by an independent walk from
`payments.line27a` over v100 members. They are per-child roster answers in the
same class as the parked age and residency answers. The parked item names
only "counted-child age and residency" (Decision 3 adds "presumably SSN and
joint-return"), so the parked scope is understated. Whether a missing
tie-breaker answer blocks silently was not reproduced here.

Repair: list the `dtb.child.*` answers in the parked item. No change to v100.

### EAQ-R5 (low, semantic): the main-home military sentence covers only "you" and leaves "extended" undefined

`packages/content/tax/2025/input-question.eic-main-home-in-us.v1.json:7`.

The question asks about "your main home, and your spouse's if you file a
joint return". Its military sentence begins "If you were on extended active
military duty". Pub. 596 (p596 1865-1867) applies the rule to "U.S. military
personnel stationed outside the United States on extended active duty". The
instructions define extended active duty as orders for an indefinite period
or more than 90 days, counted from the start of duty (i1040gi 4802-4808).

Failure scenario: a joint return where the spouse, not the filer, was
stationed abroad all year on 12-month orders. A literal reader answers no for
the spouse's home, so the credit is $0 when it should be allowed. A member on
a 60-day deployment cannot tell from the question whether the rule applies.
The error only takes the credit away, never wrongly grants it.

Repair: "If you or your spouse were stationed outside the United States on
military orders for an indefinite period or more than 90 days, ..."

### EAQ-R6 (low, semantic): the spouse SSN question does not say what an ITIN means

`packages/content/tax/2025/input-question.eic-spouse-valid-ssn.v1.json:7`.

Pub. 596 Rule 2 (p596 507-510) says: "You can't get the EIC if, instead of an
SSN, you (or your spouse if filing a joint return) have an individual taxpayer
identification number (ITIN)." The question asks "Does your spouse's Social
Security number allow ...", which assumes the spouse has one. A filer whose
spouse has an ITIN, and who treats it as the spouse's "number", is not told
the answer is no.

The question is also stricter than the source in one case. It says yes only
if the card "is not marked 'Not Valid for Employment'". Pub. 596 (p596
501-506) allows the credit when, by the due date, the person became eligible
for a card without that legend, even if the card was not updated. That error
only takes the credit away. It copies the published EIC1 taxpayer wording.

Repair: add "If your spouse has an ITIN or no Social Security number, answer
no."

### EAQ-R7 (low, meaning): the age fact's published title is narrower than its question

`packages/content/tax/2025/eic-questions.bundle.json:19` (published v1, not
changed here). The fact's title asserts only the birth-date range. The new
question also records yes under the death rule. In Pub. 596 Example 1 (filer
67, spouse born in late 1960 who died in August 2025 at 64), the correct
answer is yes, but the fact's title is false for that household. The recorded
value is right for the credit, but an explanation that shows the title would
misdescribe it. Record this in the closeout as a known divergence. A bundle
successor is out of scope.

### EAQ-R8 (gate): `verify` has not run on this head

PR #296 is a draft at `76bd1569`. Its `verify` job fails by design with
"Draft PRs do not run the full gate". `quick` passed. The gate of record is
open. This review does not assume a future green result.

## Charter questions

1. **The four questions.** The main-home, dependent and spouse SSN questions
   match line 27a Step 4 questions 3 and 6 and Step 1 question 2, and their
   definitions, except as noted in EAQ-R5 and EAQ-R6. Cases checked:
   - Filer born January 1, 1961: yes, correctly. The 65th birthday falls in
     2026, and the birth-date bound includes that day.
   - Spouse who died in 2025 at 64: yes, correctly, through the death
     sentence (Pub. 596 Example 1).
   - Joint return where only one spouse meets the age test: yes, correctly
     ("you, or your spouse").
   - Military member abroad: see EAQ-R5.
   - Filer who could be claimed by someone who files only for a refund: the
     parenthetical leads to no, so the credit is allowed. That matches
     i1040gi 4585-4589.
   - Spouse with an ITIN: see EAQ-R6.
   - "Valid for Work Only With DHS Authorization": handled correctly.
   - Decedent under 25 at death but born before January 2, 2001: wrong
     (EAQ-R1).
   - Dependent polarity: yes records no, and that stops the credit. Correct,
     but unrecorded and untested (EAQ-R2).
2. **Census.** An independent walk of every fact reachable from
   `payments.line27a` on v99 and on v100 gave 202 leaves on each. The only
   difference is that the four facts now have questions. No other
   single-return credit answer lacks a question. The per-child roster
   answers, including `dtb.child.*` (EAQ-R4), are the remaining unasked
   answers. No rule changed, so no filer is newly required to answer
   anything. One sibling reader now shows a question on its own lines
   (EAQ-R3).
3. **Nothing else moved.** I reran `replay.py v100` through
   `tools/recorded_replay.py`. Probe lists: 32 of 32 pass, 0 unexpected, and
   the per-note counts match the committed file. Recorded lists, shard 0/4:
   194 pass, 0 unexpected (171 expected changes, 23 `error/error`). The
   committed summary's core fingerprints match the sha256 of the committed
   v99 and v100 packages and the v98 release. The live test's answered
   returns (537 / 887, 649 / 1,149) pass.
4. **Publication.** Checked against `github/main`:
   - Only two files are modified: `packages/tax/loader.py` (two added v100
     entries, identical in content to v99's) and the re-pinned
     `tests/test_noncovered_sales_v78_switch.py`. Every other file is new.
     No published file is modified.
   - Core v100 against v99: four members and four entrypoints are added.
     Only `version` and `package_checksum` differ otherwise.
   - Registry v98 against v97: four citizens and one package are added,
     nothing is changed.
   - The release v98 digest equals the sha256 of `published-packages.v98.json`.
   - The validator's successor-graph fallback (`package_validation.py`
     2899-2906) selects the highest table key at or below 100. v100 replaces
     no member, and `build.py`'s `generate_to_directory` validated it, so no
     new table entry is needed.
5. **Tests.** Three mutants were built in scratch copies, with v100, registry
   v98 and release v98 regenerated by `build.py`, and run against the two new
   test files:
   - The main-home question dropped from v100: 8 failed.
   - The age and main-home questions naming each other's fact: 9 failed.
   - The dependent polarity reversed: 0 failed (EAQ-R2).
   - Unmutated baseline: 25 passed.

## What I ran

- `tools/build_orientation_block.py --ref HEAD --charter ... --role reviewer`.
  The SHA matched `git rev-parse HEAD`.
- `git fetch github`. `git rev-list --left-right --count github/main...HEAD`
  gave `0 5`. Diffs of the package, registry, release and loader against
  `github/main`.
- `python3 tools/envelope_scan.py --range github/main..HEAD` and
  `--range main..HEAD`: both clean, exit 0.
- Read the source extractions (i1040gi line 27a Steps 1 and 4 and the
  Definitions; Pub. 596 Rules 2, 11, 12 and 14).
- An independent census script over v99 and v100 members, and a search for
  every rule that reads each of the four facts.
- Mutation runs of `tests/test_eic_answer_questions_v100.py` and
  `tests/test_eic_answer_questions_v100_package.py`. A wider question-test
  run on the polarity mutant.
- A child tax credit sibling probe through `live_coordinate_run` on v99 and
  v100.
- `replay.py v100 --probe` (all 32 lists) and `replay.py v100 --shard 0/4`.
- `gh pr checks 296`.
- No code was edited. Mutations stayed in scratch copies outside the
  repository.
