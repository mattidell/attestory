# Review: a counted child's missing credit answer is asked

Reviewer, fresh context. Charter: `docs/reviews/eic-child-answers/charter-review.md`.
Object: `github/main..HEAD` on `milestone/eic-child-answers-2025`, HEAD
`290536f1` (0 behind, 9 ahead of `github/main`). Orientation block verified at
that SHA. Governance not read. ADR 0087 acceptance is the owner's and is not
part of this verdict.

## Verdict

**READY with notes.** The walk does what ADR 0087 Decision 1 says on every
roster shape measured. It changes nothing on cores up to v100, which I tested
directly. Every fully answered return computes as on v100. Publication is
add-only. The tests kill every mutant the charter names. Two question texts
leave out a condition their own cited source lines state (ECA-R1, ECA-R2).
Both fixes are wording only. v101, registry v99 and release v99 are not on
main yet, so they can be regenerated in place, as Track 1 already did for the
joint-return wording. I recommend that repair before the PR goes ready. The
rest are notes.

## Findings

### ECA-R1 (medium): residency and lived-with-you leave out the kidnapped-child rule

`packages/content/tax/2025/input-question.eic-child-residency.v1.json:6`,
`input-question.ctc-child-lived-with-you.v1.json:6`. The EIC TIP (i1040gi
4462-4464) lists kidnapping beside temporary absence, birth, death and
placement. The exceptions Track 1 quotes point to it (i1040gi 4756, 1886). The
rule itself is at i1040gi 1916-1920 and p596 1241-1254: a child presumed
kidnapped by a non-family member is treated as living with you for more than
half the year if it lived with you for more than half of the part of the year
before the kidnapping. Both questions list every other exception and leave
this one out. The fact titles leave it out too, but do not exclude it.
Scenario: a filer whose child (demo) was kidnapped in August, after living
with them since January, reads "Answer no if not" and answers no. The child is
not counted, and the earned income credit and child tax credit compute lower,
with no block. Repair: add the kidnapped-child sentence, or say plainly that
this return does not handle it. The over-half-support question
(`input-question.odc-dependent-over-half-support.v1.json:6`) has the same gap
against i1040gi 1673-1675 ("But see ... Kidnapped child").

### ECA-R2 (medium): the age question's full-time-student definition drops its exclusions

`input-question.eic-child-age.v1.json:6`. The question quotes i1040gi
4788-4792, but not the next sentence (4792-4794): "A school includes a
technical, trade, or mechanical school. It doesn't include an on-the-job
training course, correspondence school, or school offering courses only
through the Internet." Track 1 cites 4788-4794. Scenario: a filer's
21-year-old (demo) was enrolled full time only in an internet-only program.
The filer answers yes, the child counts for the earned income credit, and the
credit is overstated: an improper claim. Repair: add the sentence.

### ECA-R3 (low): "answer no" narrowings compute a smaller credit instead of blocking

`input-question.odc-dependent-gross-income-under-limit.v1.json:6` ("even if
the person was permanently and totally disabled") and
`input-question.odc-dependent-over-half-support.v1.json:6` (multiple support
agreement). Both follow the fact titles' declared class, so they do not change
which answer a path needs. But i1040gi 1874-1877 lets sheltered-workshop
income be excluded for this test, and 1925-1933 can treat the filer as
providing over half the support. Scenario: a disabled dependent parent (demo)
has $6,000 gross income, $2,000 of it from a sheltered workshop. The filer is
told to answer no, and the credit for other dependents is silently $500 lower.
Changing this is outside this milestone's non-goals. Record it for a later
one. A wording option that keeps the same answer would be "this return does
not handle ...; answer no".

### ECA-R4 (low): the military parenthetical leaves out the short-service rule

`input-question.eic-child-residency.v1.json:6`. "(duty ordered for an
indefinite period or for more than 90 days)" drops i1040gi 4806-4808: once
extended duty begins, it counts even if fewer than 90 days are served.
Scenario: a filer with 120-day orders cut short at 60 days reads the
parenthetical as excluding them.

### ECA-R5 (low): name the field `memberLabel`, not `member_label`

`packages/derivation/presentation_projection.py:5254` (validator),
`:829-832`; `packages/presentation/pages/citation-walk.v1.html:1045-1046`;
ADR 0087 Decision 2 (`docs/adr/0087-question-walk-follows-roster-members.md:40`).
Every other key on a reason, and on the model around it, is camelCase:
`factId`, `statementLabel`, `responseLabel`, `valueLabel`, `activeCodes`.
Scenario: the next page or consumer author writes `reason.memberLabel` by
analogy. It reads undefined, and the page silently falls back to the
statement label, or to no name. Recommendation: `memberLabel`. The ADR is
still proposed, so its text can change before acceptance at no history cost.

### ECA-R6 (low): the two-labels guard is untested

`presentation_projection.py:520` (`labels[0] if len(labels) == 1 else None`).
Mutant `labels[0] if labels else None` survives
`tests/test_eic_child_answers_walk.py`, `tests/test_eic_child_answers_v101_package.py`
and `tests/test_input_questions.py` (47 passed). The charter asks whether a
member with two labels stays silent. It does today, but nothing holds it.
Scenario: a later edit lets a key that names two labelled entities show the
first one's label, which attaches the question to the wrong person, and no
test fails. Add a unit case with two labelled entities in the member keys.

### ECA-R7 (low): two members with the same recorded label merge into one reason

`presentation_projection.py:829-832`: reasons are a set of
`(label, sentence)`. Measured on the unit fixture: two children both labelled
"Synthetic child", both missing the age answer, produce one reason. Scenario:
twins both labelled "Child". The page asks once, the filer answers for one,
reruns, and is asked again. Decision 1 cannot be met when the labels are
identical, but the merge also hides that two answers are needed. Key the set
on the member, or record the behaviour in the docstring and a test.

### ECA-R8 (low): the follow is wider than "roster member" and is not version-gated

`presentation_projection.py:486-508`, `:754-763`, `:4952`. `_RosterMembers`
is built for every package and core. `follow_member` follows any key whose
blocked row's rule declares `reads_subject_results` for that subject type.
In v101 that also covers the 1099-B transaction checks, 1099-K, 1098, the SLI
worksheet and `f1099b-box4-amounts-ready`, not only the four rosters ADR 0087
names. Measured: zero walk differences (walk with the follow against the same
walk without it) across all 775 recorded lists on v100, and across the 101
probe lists on v100. On v101 the probe lists show 89 differing lists (the
positive control). So nothing moves today. Scenario: a later core adopts an
input question for a transaction-keyed fact. A sale line blocked on a
transaction subject then gains a sentence labelled with the transaction's
entity label, on a shape no test covers. Either widen the ADR text to "a
per-subject read", or restrict the follow to the roster subject types, and
add a non-roster case.

### ECA-R9 (low): polarity is held only in the evidence script

`docs/phases/engine-breadth/milestones/eic-child-answers-evidence/track1_design.py:213-215`;
`tests/test_eic_child_answers_v101_package.py:111`. I checked the three
questions whose yes records the fact's no against their fact titles:

- `ctc.child.no-over-half-support`: "yes means the child meets the test",
  that is, did not provide.
- `odc.dependent.not-qualifying-child`: yes means no taxpayer may claim the
  person.
- `odc.dependent.not-joint-return`: yes means the person did not file
  jointly.

All three are right. Mutants that flip `POLARITY`, or reverse one of the three
texts, fail the package test. The polarity itself is not in any published
artifact (`input-question.v1` has no field for it). For the other 23
questions, a consistent rewording that reverses meaning (design, file and
registry together) fails no semantic test. Unlike v100's
`test_dependent_question_polarity_live`, no live test runs a recorded value
through the coordinator. This is a convention carried over from v100, so it
is a note.

## Answers to the charter questions

1. **Walk against ADR 0087.** A member key is followed only when no blocked
   row and no input question explains it, and the row is not
   `SOURCE_SET_UNCLOSED`. The walk then visits only that member's blocked rows
   under `<symbol>|<member key>`. Each reason's label comes from the member
   row's own keys. A line is answered only if every root, including each
   followed member, resolves. A key with no rows, no label, or another
   member's rows stays silent (unit tests, and mutants M1 and M5 killed).
   Two labels: silent, but untested (ECA-R6). A partial explanation was not
   found across members. Within one member, an and-chain asks only the
   evaluator's first missing answer (live: `rel-tin@p1+rel-citizen@p1` asks
   only the TIN). That is what the path requires, not a defect. Cores up to
   v100: tested directly. The probe on v100 under the `github/main`
   projection and page, against HEAD's, gave 63 of 63 identical results. The
   walk-difference run gave 0 of 775 recorded lists and 0 of 101 probe lists
   (ECA-R8).
2. **Label.** It is only the current entity's recorded `label`, never an id,
   value or path, and there is no fallback. The page inserts it as a text
   node (`el()`), and `_check_no_unsafe_strings` rejects `</script` and
   `<!--` before embedding. Name: `memberLabel` (ECA-R5).
3. **The 26 questions.** Each was checked against i1040gi (Steps 1-5,
   exceptions, line 27a Step 3, EIC definitions, qualifying child of more
   than one person, children of divorced or separated parents), i1040s8
   45-200 and p596 1241-1254. The following match their sources and their
   fact titles: born or died, temporary absence, adoption or foster
   placement, the adopted-child citizen exception, disabled at any age, the
   parent definition, Form 8332 and pre-1985, nights, AGI, "do not know"
   counted as will claim, the TINs and the SSN validity legends. Gaps:
   kidnapping (ECA-R1), the student exclusions (ECA-R2), the sheltered
   workshop and multiple support narrowings (ECA-R3, by design), and the
   military short-service rule (ECA-R4). Polarity: ECA-R9.
4. **Nothing else moved.** I reran `track1_replay.py` over the 775 recorded
   lists (published v100 against v101): 775 pass, 691 differ in the package
   version only, 84 are `error/error`, 0 unexpected. The 7 answered probe
   returns are held by the live test. Nobody is asked anything new: a
   question appears only for a name the evaluator reports missing on a
   blocked line, and the v100 walk-difference count is 0.
5. **Publication.** Within `packages/content` and the release directory,
   every file is new (28). No file is modified, and the 26 questions,
   package v101, registry v99 and release v99 are add-only (package tests).
   The modified files are the projection, the page (not a published schema),
   the loader, two tests and the ADR index. The loader v101 entries equal
   v100's (test). `envelope_scan` exits 0 on `github/main..HEAD` and
   `main..HEAD`.
6. **Tests.** Mutants, made in a scratch copy and not committed:
   - stop following members: killed (6 failures);
   - rotate labels between members: killed;
   - drop the age question: killed (4);
   - take the label from another member: killed (2);
   - drop the "existing test row" check: killed;
   - drop the member-keyed check: killed;
   - follow unclosed rows: killed;
   - flip `POLARITY`: killed;
   - reverse the no-over-half-support text: killed;
   - accept two labels: **survived** (ECA-R6).

## What I ran

- `tools/build_orientation_block.py --ref HEAD --charter ... --role reviewer`;
  `git fetch github`; `git rev-list --left-right --count github/main...HEAD`
  gave `0 9`.
- `tools/envelope_scan.py --range github/main..HEAD` and `--range main..HEAD`:
  both exit 0.
- `track1_probe.py --core v100` (63 cases) in two scratch copies of HEAD, one
  with `github/main`'s `presentation_projection.py` and `citation-walk.v1.html`:
  identical.
- A walk-difference harness. It wraps `_closure_question_reasons` and compares
  each result with `roster_members=None`. Runs: v100 over 775 recorded lists,
  0 differences; v100 over 101 probe lists, 0; v101 over 101 probe lists, 89
  (control).
- `track1_replay.py --shard 0/1` (recorded, v100 against v101): 775 of 775
  pass.
- `track1_probe.py --core v101` on combined omissions: `age+res`, `age+u17`,
  `age+ssn+joint` for one child; `u17@1+lived@2`; `res+dtb-another`; and
  `rel-tin+rel-citizen` for one relative. Every blocked line had a sentence,
  with one label per member.
- The mutants above, against `tests/test_eic_child_answers_walk.py`,
  `tests/test_eic_child_answers_v101_package.py` and
  `tests/test_input_questions.py`.
- Source reads in the ignored `temp/` extractions: i1040gi 1470-1980,
  4418-4475, 4750-4915; i1040s8 45-200; p596 1241-1254.
- I did not run the full suite; CI `verify` is the gate of record.
