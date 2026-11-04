# Review: P0 and Track 1, a blocked line asks its yes-or-no question

Reviewer: fresh reader. Object: `github/main..HEAD` at `9536b6ec` on
milestone/scope-answer-questions-2025 (read from committed state; governance and
builder threads not read). Charter: `charter-review.md`.

## Verdict

**Mechanics: clean. Wording: not ready as written.** The build matches its
design (80 citizens, verbatim sentences, additive successors, earlier cores
byte-identical). One question (S1A) is wrong for a common filer and should be
repaired before release; nine more are recommended wording repairs, mostly
asking a filer what a filer cannot know. No required finding touches
computation.

## Verified (reusable by a bounded repair)

- Citizens: 80 `input-question.v1` files, one per fact. I parsed the P0 table's
  facts column and compared every citizen sentence to it: 80/80 present, 76
  verbatim; the four differences are the two intended or implied changes (EIC1
  per decision 1; FTC10 split, see F9). 40 distinct sentences.
- Successors only: v73 vs v72 adds 80 members, removes none, same bindings,
  same schema. Registry v71 vs v70: citizens 1099 -> 1179 (+80, 0 removed),
  packages 76 -> 77 (+v73 only). No file under `packages/schemas` changed. Release
  v71 is new. `tools/envelope_scan.py --range github/main..HEAD`: exit 0, no output.
- Projection: only `filing_status` maps to a different fact type id (all other
  bindings map a symbol to itself), and the map is consulted only in the
  not-blocked-row branch, so the change reaches no other symbol. A symbol the
  map does not name is looked up as given. No path attaches a question to a
  fact other than the one the missing id names.
- Earlier cores: I ran 3 cases x v68..v72 (15 saved presentation models) on a
  `git archive` of `github/main` and on HEAD and compared SHA-256 of the models:
  all 15 identical (probe in my scratch space, `rv5/`).
- `pytest tests/test_scope_answer_questions.py tests/test_input_questions.py
  tests/test_schema_registry.py`: 97 passed, 107 subtests.
- Inversion table sampled against fact titles and reading rules (21 facts across
  groups): FTC1, FTC4, FTC5, FTC7, FTC8, FTC11, DEP1 (both facts), SLI1, EIC1,
  EIC2, EIC3, CG1 (all four), CG2, CTC1, M1, M2, M3, SS1, S1E, L2A1. Each "yes
  records / no records" cell matches the fact's own yes/no gloss.

## Findings

### Required

**R1. S1A tells a student-loan filer to answer "yes" to a question whose "no" the engine needs.**
Sentence (all 12 `schedule1-adjustments-scope.*` citizens): "... an IRA deduction;
an Archer MSA deduction; or any other Schedule 1 adjustment?"
The twelve facts cover Schedule 1 lines 11-20, 23 and 25. Student loan interest
(Schedule 1 line 21) is computed by `rule.sli-worksheet` and has no fact in the
group. A filer whose only adjustment is student loan interest reads "any other
Schedule 1 adjustment", answers "yes", and the question cannot record the "no"
the engine is waiting for, so a computable return stays blocked. Reproduction:
read the sentence against `rule.sli-worksheet.v6` notes (live whenever a Form
1098-E exists) and the fact list in the S1A row of the P0 table; line 21 is
absent from both.
Proposed replacement: "In 2025, did you have any of these adjustments to income:
... an IRA deduction; an Archer MSA deduction; or any other adjustment listed on
Schedule 1 line 24 (not counting student loan interest)?" (check "line 24" against
the form; the fact title says "line 25 other adjustments", the total of line 24.)

### Recommended

**W1. FTC11 asks what a filer cannot know.** "Are you required to file Form 1116
for your foreign tax?" Whether Form 1116 is required turns on the $300 / $600
total (which the return already records) and on the conditions the other FTC
questions ask. A filer guesses. Proposed: "Is your total foreign tax from all
sources more than $300 ($600 if you file jointly), or is there any other reason
you must file Form 1116?"

**W2. M2 asks a filer to compute a penalty.** "Do you owe an estimated tax
penalty for 2025 (Form 2210)?" `rule.form1040-line38` publishes $0 on a "no"; a
filer who has not run Form 2210 answers "no" by default and the return carries
$0. Proposed: "Did you pay less than the required amount of tax during 2025
through withholding and estimated payments, so that you may owe an estimated tax
penalty (Form 2210)?" "Yes" is then the only honest answer for a filer who is
unsure.

**W3. L2A3 asks which credits "depend on" tax-exempt interest.** "Does your 2025
return include a Form 6251 ..., a credit, a deduction, or a child-income election
(Form 8814) that depends on your tax-exempt interest?" A filer cannot know which
credits or deductions add back tax-exempt interest. Proposed: "Does your 2025
return include Form 6251 (alternative minimum tax), Form 8814 (election to report
your child's interest and dividends), or a credit or deduction whose income limit
adds back your tax-exempt interest (for example the Social Security benefits
worksheet, an IRA deduction, or an education credit)?" (examples to be confirmed
against `line2a-scope.no-credit-using-tax-exempt` readers).

**W4. L2A2 reads two ways.** "Did you receive tax-exempt interest or original
issue discount on a Form 1099-OID, ..." can be read as "any OID", so a filer with
ordinary taxable OID answers "yes" while the fact title ("tax-exempt interest or
OID source") may mean only the tax-exempt kind. Confirm what the rule reads;
then say it: "Did you receive a Form 1099-OID, tax-exempt interest that was not
reported on any form, or have a bond premium adjustment on tax-exempt bonds?" or
"... tax-exempt interest on a Form 1099-OID ...".

**W5. FTC12 names only line 1z; its source names 1a and 1z.** "Does your 2025
Schedule 2 show an amount on Part I line 1z, an addition to your regular tax?"
The fact title is "Schedule 2 line 1a/1z amounts that would change regular tax"
and the milestone's own quoted instruction (`form1099div-box7-direct-ftc.md`,
source 5) says "Form 1040 line 16 + Schedule 2 line 1a". A filer with an amount
on 1a and none on 1z answers "no". Charter-track1 item 1 asked for a trace
report; none is committed (no retrospective, test or note records what lines 1a
and 1z are). Proposed: confirm 1a/1z against the form, then "... show an amount on
Part I line 1a or line 1z (an addition to your regular tax)?"; commit the trace.

**W6. M6 lists examples only of gambling and leaves 8a-8z unknown.** "...did you
have any other Schedule 1 income on lines 8a through 8z (for example gambling
winnings not on a W-2G, ...)?" A filer cannot recall what the lines are.
Proposed: "...any other income that goes on Schedule 1 lines 8a through 8z (for
example gambling winnings not on a W-2G, prizes and awards, jury duty pay, an
Alaska Permanent Fund dividend, or canceled debt)?"

**W7. DEP1 folds "can" with "is".** One sentence ("Can someone else claim you
(or your spouse, on a joint return) as a dependent ...?") records both
`standard-deduction.can-be-claimed-as-dependent` ("someone else can claim") and
`sli-scope.not-claimed-as-dependent` (title: "not claimed as a dependent by
another taxpayer"). A filer whom a parent could claim but who is not claimed
answers "yes" and the SLI fact records "no" (a legal $0 deduction). Confirm that
the student-loan rule means "can"; if it means "is claimed", ask two questions.

**W8. EIC1's added clause is hard to parse.** "(issued by the Social Security
Administration on or before the due date of your 2025 return, and not marked
"Not Valid for Employment", or marked "Valid for Work Only With DHS
Authorization" and you have that authorization)": the "or" attaches ambiguously,
and the fact says the due date includes extensions. The DHS clause itself is
right. Proposed: "Does your Social Security number allow you to work in the
United States? Answer yes if it was issued by the Social Security Administration
on or before the due date of your 2025 return (including extensions) and is not
marked "Not Valid for Employment", or if it is marked "Valid for Work Only With
DHS Authorization" and that authorization is still valid."

**W9. M3 and M4 ask "are you claiming" of a filer who may not know there is
anything to claim.** M3 (QBI): "Are you claiming the qualified business income
deduction for 2025?" A filer with only qualified REIT dividends (Form 1099-DIV
box 5) answers "no" and the return carries a $0 line 13a
(`rule.form1040-line13a`). Proposed: "Do you have qualified business income, qualified REIT dividends (Form
1099-DIV box 5) or publicly traded partnership income that could give you a
qualified business income deduction in 2025?" M4 has the same shape for tips and
overtime (a filer who received them but did not know of the deduction); consider
"Did you receive qualified tips, qualified overtime pay, or pay interest on a
qualified passenger vehicle loan in 2025 (Schedule 1-A Parts II through IV)?"

### Notes

**N1. FTC3 and FTC4 and FTC5 point "yes" the other way from FTC2 and FTC6-FTC10.**
Under one blocked line a filer sees "yes = good" and "yes = problem" sentences
side by side. The owner's rule (yes means present) holds in every one; the mix is
inherent, but FTC3's trailing "which you were legally responsible for and paid
yourself" attaches to either the tax or the country. Proposed: "... paid to a
country the United States recognizes and that does not support terrorism? Were you
also legally responsible for that tax, and did you pay it yourself?" is two
questions (FTC3's three facts would then need a different grouping); otherwise
leave.

**N2. EIC4 is a ten-item sentence** (six situations, several with form jargon
such as "Schedule 1 line 8s"). It is accurate; it is the likeliest to be read
past. Left as flagged in P0.

**N3. FTC10 was reworded after P0** (P0: "Does your 2025 return include tax from
a lump-sum distribution (Form 4972) or any other tax added on Form 1040 line 17
(Schedule 2 Part I)?"; built: "Does the tax on your 2025 Form 1040 line 16
include tax from a lump-sum distribution (Form 4972), or do you have any
additional tax on Form 1040 line 17 (from Schedule 2)?"). Against the rule
(`rule.schedule3-line1-direct-ftc.v3`) the built wording is the better match to
`no-form-4972-on-line16` ("Form 4972 tax included on line 16") and
`no-line17-schedule2-additional`, and the third fact now has FTC12, so the split
is justified. No decision records the reword.

**N4. Evidence gaps (not wrong behaviour).**
- No test reads the inversion. `GROUPS` in `tests/test_scope_answer_questions.py`
  carries 'abs' / 'choice' per fact but nothing asserts it; the table lives only
  in prose under `docs/phases/.../scope-answer-questions-evidence/p0-questions.md`.
  A recording milestone must find it there; a content-side home would make it
  survive.
- The group tests exercise `members[0]` of each group; the other members' citizens
  are covered by the verbatim comparison, not by a blocked line. S1A is the
  exception (all 12).
- `EarlierCoresAreUnchanged` compares the new function with and without the
  binding map, not the pre-change function. My probe against `github/main` (above)
  closes it for 15 models.
- The "asks whether the thing is present" test is a three-word regex; it cannot
  see the failures in R1 and W1-W9.

**N5. Stale plan text.** The plan's Track 1 says "81 citizens (80 facts plus
filing status)"; the 80 facts already include filing status and 80 were built;
the plan header says 39 questions, built 40. P0 `p0-questions.md` has shell
expansion damage: "above /bin/bash" (section 5, item 7: should read "$0") and
"00 / 00 threshold" (section 6: "$300 / $600").

**N6. M1 (Form 1098) is asked of a filer whose Form 1098 is already recorded.**
Answerable but silly; P0 already lists it as derivable. No action in this
milestone.

## Charter questions

1. Wording: R1, W1-W9, N1-N2 above. Checked: FTC10 matches the rule's reads of
   `no-form-4972-on-line16` and `no-line17-schedule2-additional`; FTC12 does not
   match its fact title (W5); EIC1's DHS clause is substantively right (W8 on
   parsing). "Yes" means present in all 40 under the owner's rule; the positive
   conditions (FTC1, FTC3-FTC5, SLI1, EIC1) are "the qualifying thing holds".
2. Citizens carry the group's sentence verbatim (80/80 against the table, apart
   from the two intended changes); inversion cells match the facts (sample of 21).
3. Binding map: no wrong attachment, no hidden cause; v68-v72 byte-identical (15
   models vs `github/main`).
4. Successors only; registry adds 80 citizens and v73 and changes nothing else.
5. Qualitative review: "what does the claim mean" is where the findings are
   (R1, W1-W9); the evidence tests verify attachment, not meaning (N4).

## Repair 1 confirmation

Object: `513958bd` (repair) with trace `5825990a`, on top of `7ca17213`. 88 citizens
on the branch for 41 filer questions (49 distinct sentences include the earlier
amount questions). Read from committed state.

**Verdict: R1 and W1-W9 are resolved. No sentence is still wrong. Two residual
notes below. Mechanics unchanged and clean.**

1. Resolution
- R1 (S1A): ends "or any other adjustment listed on Schedule 1 lines 24a through
  24z (do not count student loan interest)". Matches the trace (line 21 is
  computed by `rule.sli-worksheet`; 24a-24y have no fact). Resolved.
- W1 (FTC11): "Is your total foreign tax from all sources more than $300 ($600 if
  you file jointly), or is there any other reason you must file Form 1116?" A
  filer can check it. Resolved.
- W2 (M2): "Do you owe $1,000 or more in tax for 2025 after subtracting your
  withholding and refundable credits, and did you pay less ... than both 90% of
  your 2025 tax and 100% of your 2024 tax (110% ... above $150,000 of 2024
  AGI)?" Facts a filer can check; "less than both" is the right conjunction for
  the penalty case. Resolved (see N-a).
- W3 (L2A3): now names Form 6251, Form 8814 and "a credit or deduction that counts
  your tax-exempt interest as part of your income", no invented examples. Resolved
  as far as the repo's sources go (see N-b).
- W4 (L2A2): "tax-exempt interest or tax-exempt original issue discount shown on a
  Form 1099-OID" removes the taxable-OID reading, matching the trace (taxable OID
  is a separate recorded family and line 2b). Resolved.
- W5 (FTC12): "an amount on Part I line 1a or line 1z (an addition to your regular
  tax)" matches the fact title; the trace is committed and says plainly that the
  repo's two sources disagree on 1a versus 1z. Resolved.
- W6 (M6): lists prizes and awards, jury duty pay, Alaska Permanent Fund dividend,
  canceled debt. Resolved.
- W7 (DEP1): split. DEP1 "Can someone else claim you (or your spouse, on a joint
  return) ..." records only the standard-deduction fact; DEP2 "Is someone else
  claiming you as a dependent on their 2025 return?" records only the student loan
  fact (filer-only, as that fact's title says). Resolved.
- W8 (EIC1): rewritten as a question plus "Answer yes if ... (including extensions)
  ... or if it is marked 'Valid for Work Only With DHS Authorization' and that
  authorization is still valid". Resolved.
- W9 (M3, M4): both now ask whether the filer had the income or payments. Resolved.
- N4 (inversion unread): a test now reads each fact's polarity against the supported
  value (`test_the_question_yes_value_is_unsupported_for_abs_and_supported_for_pos`).
  Not re-run by me.

2. As a filer: "yes" means present in every re-read sentence. S1A, L2A2, L2A3, FTC12,
DEP1, DEP2, M3, M4, M6 and M2 ask whether the thing exists or holds; FTC11 and EIC1
ask whether the qualifying condition holds. Each of the twelve matches its trace
entry where the trace has one (S1A, L2A2, L2A3, FTC12, DEP1/DEP2); FTC11, M2, M3,
M4, M6 and EIC1 match the plan's "Decisions (after review)" items 3, 5.
- N-a (note). M2 is a long, two-part sentence and "owe $1,000 or more" is only
  knowable once the return is computed. It is checkable, unlike the earlier wording.
- N-b (note). L2A3 still asks the filer to know which credits or deductions count
  tax-exempt interest as income. The repo does not list them (trace says so);
  a later milestone that records answers should add examples once sourced.

3. Mechanics
- Registry v71 vs v70: citizens 1099 -> 1179, packages 76 -> 77; zero changed or
  removed checksums, 80 + 1 added. v71 and the v73 core are not on `github/main`,
  so regenerating them in place on this branch changes no published history.
- No file under `packages/schemas` touched; `envelope_scan --range github/main..HEAD`
  exit 0.
- v68, v70, v72, two cases each (withhold filing status; withhold the line 2a
  Form 6251 answer), SHA-256 of the saved presentation models on a `git archive` of
  `github/main` versus HEAD: 6 of 6 identical. (My first run had exit 127 and
  compared empty files; the figures here are from the rerun.)
