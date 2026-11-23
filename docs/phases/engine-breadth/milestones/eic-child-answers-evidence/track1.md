# Track 1: A Counted Child's Missing Credit Answer Is Asked (2025)

The probe scripts the tests load (`probe.py`, `track1_probe.py`, `track1_design.py`) are kept beside this note. The other build and replay scripts and their raw JSON outputs named below were working artifacts and were removed at publication; the milestone's tests reproduce the behavior, and `tools/recorded_replay.py` reruns the replay.

Plan:
`docs/phases/engine-breadth/milestones/eic-child-answers.md`. ADR:
`docs/adr/0087-question-walk-follows-roster-members.md` (proposed; built to
its Decision). P0: `p0.md` beside this note.

## Result

On core v101 every per-member answer of the four rosters that v100 never
asked is asked, on every page line it blocks, beside the member's recorded
label. The probe leaves each of the 26 answers out for one member (and
some for two members at once): no blocked page line is left without a
sentence, each line still blocks, and each sentence names the right
member. Every recorded return keeps its numbers (775 of 775 recorded lists,
v100 against v101), and a return with every answer given computes exactly as
on v100.

## Projection (ADR 0087)

`packages/derivation/presentation_projection.py`:

- `_RosterMembers` (new, read-only): the count rule's declared
  `reads_subject_results`, the per-subject publisher of a symbol, a fact
  type's declared entity identity keys, and a member's recorded entity label
  (`state.fact_state.entities`, the `label` the filer gave when adding the
  member; `entity.v1` requires it). No schema or kernel change was needed.
- `_closure_question_reasons` takes `roster_members`. Where a missing name
  has no blocked row, no family question and no input question, and the row
  is not `SOURCE_SET_UNCLOSED`, a name of the shape `<fact type>|<keys>`
  whose fact type is the subject of a subject result the row's rule reads is
  followed to the member's own blocked rows (`<symbol>|<name>`). A member row
  is walked by `reach_member`: a missing name published per subject is looked
  up as the member's own row (`<name>|<subject>|<keys>`) and walked; if the
  member has no such row and the name has one publisher, its subject fact is
  the missing answer. A missing fact individuated on the member (by its
  declared entity keys) is asked with `memberLabel`; a return-level fact
  reached from a member is asked without one. A member key with no blocked
  rows, or no single current labelled entity in its keys, leaves the line
  without a sentence, as before; every root must still have a question.
- One reason per member and question: `{"sentence", "memberLabel"}`, after
  the plain reasons, ordered by label then sentence. The walk memo carries
  the member questions like the others (`_WalkFrame.member_facts`).
- The blocked-reason validator admits the optional `memberLabel` (a
  non-empty string).

`packages/presentation/pages/citation-walk.v1.html`: a reason's
`memberLabel`, when present, is shown as the bold prefix the page already
draws for a statement label ("Synthetic demo-eicc-child-2: <question>").

The walk is not switched by package version. On v100 and every earlier core
no per-member answer has a question, so the followed walk finds a root
without one and the line stays silent: `track1-probe-v100.json` (current
code, v100) shows no reason on any of the 63 probe returns, exactly as P0's
trace. `tests/test_input_questions.py`'s v69 reference walk accepts and
ignores the new argument.

## Published

Core v101, registry v99, release v99, on published core v100 (registry v98,
release v98). New files only; nothing on main was edited.

- 26 `input-question.v1` files in `packages/content/tax/2025/`, each named
  `input-question.<fact without the tax.us.2025. prefix, dots as dashes>.v1.json`,
  each also an entrypoint, written by `track1_build.py` from
  `track1_design.py` and validated by
  `tools/package_successor.generate_to_directory` (`track1-build.json`).
- `package.core-calculations.v101.json`, `published-packages.v99.json`
  (add-only: 26 citizens and the package),
  `demo.release.sli-worksheet-integration.2025.v99.json` (version and
  registry digest only).
- `packages/tax/loader.py`: v101 entries carry v100's covered-flag refusal
  map and companion declaration.
- The joint-return question was reworded after the first build (it named
  one credit; the child tax credit reads the same fact) and the relative
  joint-return source line corrected. v101, v99 and v99 are not on main, so
  they were regenerated in place: the diff is that question's text, its
  registry checksum and the release digest; the package is byte-identical.

The 26 questions: the earned income child's age, residency, joint-return and
SSN tests (4); the ten tie-breaker answers (P0 traced two; the other eight are
read on the paths those open, and are equally unasked); the child tax
credit's under-17, lived-with-you, support and citizenship tests (4); the
other-dependent child's TIN (1); the seven relative answers (7).
`eic.child.another-may-claim` is not read by any v100 rule, so it gets none.

Each question is a plain question, then "Answer yes if ..." and "Answer no
if ...". `POLARITY` in `track1_design.py`: a fact stated as an absence
(`ctc.child.no-over-half-support`, `odc.dependent.not-qualifying-child`,
`odc.dependent.not-joint-return`) is asked about the thing itself, so the
filer's yes records the fact's no, as the published v100 questions do; the
other 23 record yes as yes. Where a fact's declared title narrows the class
("A multiple support agreement is outside the class: answer no", "A
permanently and totally disabled person whose gross income is $5,200 or
more ... answer no", "yes means they will claim or you do not know"), the
question says the same, so no question changes which answer a path needs.

Sources (`pdftotext -raw`, line numbers as `sed -n` counts them; the files
are in the ignored `temp/` directory, never committed):

- i1040gi: 2025 Instructions for Form 1040, sha256
  `482e9c487c608f1bbeaceef35bc3c0933e8b35443cfff447e4279d590468364a`
  (PDF), `21f04d445eda145d9c05eb696460286c2f981fd9cafa0b692ade4c16cf34409a`
  (extraction).
- i1040s8: 2025 Instructions for Schedule 8812, fetched from irs.gov for
  this track, sha256
  `bb9788cdf068f9d3a666b2fc351b6bd963e1e848f295d0d01df63848628e1794` (PDF),
  `a825886797a5f9d25022db0be44dba5fc76fe4f3d2c7c4c3ab1e7dacb3e87224`
  (extraction).
- p596: 2025 Publication 596, sha256
  `29e8c6695912318253743210fcd68aaa10ad874c76edcab4aa7dc4b23ff51dbf` (PDF),
  `3a426ba54f1be73739741a7fb5094c2de39bee75ed93ec65a282727936aacbaa`
  (extraction).

## Tests

- `tests/test_eic_child_answers_walk.py` (fast, unit): a member key resolves
  to the member's question with its label (both walks); a member row that
  names an answer directly; a member key with no rows (or only another
  member's rows) leaves the line silent; two members each missing an answer
  get two labelled reasons (same answer, and different answers); one member
  missing two answers is asked both; every root must have a question; an
  existing test row is not read as a missing answer; a return-level answer
  reached from a member is not labelled; no recorded label, no
  `roster_members`, a count rule that reads no member results, and an
  unclosed roster row all stay as before; the validator admits
  `memberLabel` and refuses a malformed one.
- `tests/test_eic_child_answers_v101.py` (live): the real coordinator and
  saved page (`track1_probe.py`), nothing pre-filled that a test is about.
  For each roster, one member and the second of two, 44 returns each leaving
  one answer out for one member (all 26 answers): every blocked page line shows exactly the member's
  label and the answer's published question, and the credit lines still
  block. Two members each missing an answer (same answer, different answers,
  relatives): both are asked by name on every line. One case per roster also
  on v100: v101 blocks the same rules and lines with the same numbers, and
  asks exactly on the lines v100 left silent. Seven answered returns compute
  exactly as on v100. The saved page, opened in headless Chromium, shows
  "<label>: <question>" for each member on each of the nine earned income
  credit lines.
- `tests/test_eic_child_answers_v101_package.py` (fast): v101 admits exactly
  the 26 questions against v100 and changes nothing else; each names a
  declared, member-individuated fact of its bundle that no v100 question
  names, with the designed wording and sources; each says what yes and no
  mean, with the polarity above; registry v99 add-only; release v99;
  loader entries carry v100.
- Re-pinned: `tests/test_noncovered_sales_v78_switch.py` (cores that name
  the covered-flag refusal now run through v101).

## Replay

`track1_replay.py` over `tools/recorded_replay.py` unchanged (strict
full-surface comparison), published v100 against published v101, both on
the Track 1 projection. Expectations: the package version, each of the 26
question sentences added, `memberLabel` added, and a reasons list added on
a line that had none.

| Set | Lists | Pass | Unexpected | Unused expectations |
| --- | --- | --- | --- | --- |
| recorded (`track1-replay.json`) | 775 | 775 (691 package version only, 84 identical `error/error` as in earlier milestones) | 0 | 28: every question, the label and the reasons list (no recorded list leaves a member answer out) |
| probe (`track1-replay-probe.json`): P0's 38 lists and Track 1's 63 | 101 | 101 | 0 | none |

No number, disposition or row changes on any list.

Probe outputs: `track1-probe-v100.json` and `track1-probe-v101.json` (63
returns each). On every return v101 publishes the same lines, symbols and
blocked rules as v100, and the lines v101 asks are exactly the lines v100
left silent.

## Repair

The fresh review's findings ECA-R1, R2, R4, R5 and R6 (summarized in the retrospective). Core v101,
registry v99 and release v99 are not on main, so they were regenerated in
place through `track1_build.py` (validated by
`tools/package_successor.generate_to_directory`) and keep their numbers.
Diff against the previous build: four question files, their four registry
checksums, and the release's registry digest. The package file is
byte-identical and no other question changed.

Questions changed, each by adding the source's own words (sources quoted in
the section for each question below):

- ECA-R1, `eic.child.residency` and `ctc.child.lived-with-you`: a kidnapped
  child is treated as living with you for more than half of the year if the
  child lived with you for more than half the part of the year before the
  date of the kidnapping or following the date of the child's return; the
  child must be presumed by law enforcement authorities to have been
  kidnapped by someone who isn't a member of your family or the child's
  family; the treatment applies for all years until the child is returned,
  but the last year is the earlier of the year there is a determination that
  the child is dead or the year the child would have reached age 18
  (i1040gi 1916-1920, 4462-4464; Pub. 596 1241-1254).
- ECA-R1, `odc.dependent.over-half-support`: if the person is your child
  presumed by law enforcement authorities to have been kidnapped by someone
  who isn't a family member, you may be able to take the child into account
  for the credit for other dependents (i1040gi 1673-1675, 1916-1920). The
  source states no support-specific condition, so none is added.
- ECA-R2, `eic.child.age`: a school includes a technical, trade, or
  mechanical school and doesn't include an on-the-job training course,
  correspondence school, or school offering courses only through the
  Internet (i1040gi 4792-4794).
- ECA-R4, `eic.child.residency`: once you begin serving extended active duty,
  you are considered to be on extended active duty even if you don't serve
  more than 90 days (i1040gi 4806-4808).

ECA-R5: the reason field `member_label` is now `memberLabel` in the
projection, the blocked-reason validator, the page and the tests.

ECA-R6: `test_a_member_with_two_recorded_labels_leaves_the_line_silent` (a
member whose keys name two current entities leaves the line silent; the same
member keyed on one entity is asked). On a scratch copy with the one-label
guard in `_RosterMembers.label` removed it fails (`[{'memberLabel': ...,
'sentence': ...}] != []`); with the guard it passes.

Replay after the repair (same expectations): recorded 775 of 775 pass (691
package version only, 84 identical `error/error`), 0 unexpected, 28 unused
as before; probe 101 of 101 pass, 0 unexpected, none unused.
`track1-probe-v101.json` was regenerated: only the sentences of the lines
that show the changed questions differ.

Checks after the repair:

- `pytest tests/test_eic_child_answers_walk.py`: `15 passed, 6 subtests passed in 1.19s`
- `pytest tests/test_eic_child_answers_v101_package.py`: `6 passed in 1.26s`
- `pytest tests/test_eic_child_answers_v101.py`: `59 passed in 38.30s`
- `pytest tests/test_input_questions.py`: `27 passed, 49 subtests passed in 108.64s`
- `pytest tests/test_schema_registry.py`: `14 passed in 1.22s`
- `pytest tests/test_noncovered_sales_v78_switch.py`: `5 passed in 1.15s`
- `pytest -m "not live"`: `1941 passed, 8 skipped, 5970 subtests passed in 15.56s`
- `python3 -m mypy`: `Success: no issues found in 531 source files`

## Questions and their sources

Each question as published, its polarity, and the source lines it is written
from, quoted from the extraction (column breaks of the PDF join some lines).

### `eic.child.age` (pos)

Question: Does this child meet the age test for the earned income credit? Answer yes if, at the end of 2025, the child was under age 19 and younger than you (or your spouse if you file a joint return); or was under age 24, a full-time student, and younger than you (or your spouse if you file a joint return); or was any age and permanently and totally disabled. A full-time student is a child who during any part of 5 calendar months of 2025 was enrolled as a full-time student at a school or took a full-time, on-farm training course given by a school or a state, county, or local government agency. A school includes a technical, trade, or mechanical school. It doesn't include an on-the-job training course, correspondence school, or school offering courses only through the Internet. A person is permanently and totally disabled if, at any time in 2025, the person couldn't engage in any substantial gainful activity because of a physical or mental condition and a doctor has determined that this condition has lasted or can be expected to last continuously for at least a year, or can be expected to lead to death. Answer no if none of these applies.

- i1040gi 4424-4436 (line 27a Step 3, qualifying child: age): "was ... Under age 19 at the end of 2025 and younger than you (or your spouse if filing jointly) or Under age 24 at the end of 2025, a full-time student (defined later), and younger than you (or your spouse if filing jointly). If the child is a full-time student, check the “Full-time student” box on row (6) of the Dependents section on page 1 of Form 1040 or 1040-SR or Any age and permanently and totally disabled (defined later). If the child is permanently and totally disabled, check the “Permanently and totally disabled” box on row (6) of the Dependents section on page 1 of Form 1040 or 1040-SR."
- i1040gi 4788-4794 (Full-time student): "Full-time student. A full-time student is a child who during any part of 5 calendar months of 2025 was enrolled as a full-time student at a school or took a full-time, on-farm training course given by a school or a state, county, or local government agency. A school includes a technical, trade, or mechanical school. It doesn't include an on-the-job training course, correspondence school, or school offering courses only through the Internet."
- i1040gi 4813-4817 (Permanently and totally disabled): "Permanently and totally disabled. A person is permanently and totally disabled if, at any time in 2025, the person couldn’t engage in any substantial gainful activity because of a physical or mental condition and a doctor has determined that this condition (a) has lasted or can be expected to last continuously for at least a year, or (b) can be expected to lead to death."

### `eic.child.residency` (pos)

Question: Did this child live with you in the United States for more than half of 2025? Count temporary absences for special circumstances, such as school, vacation, business, medical care, military service, or detention in a juvenile facility, as time the child lived with you. A child who was born or died in 2025 lived with you for more than half of 2025 if your home was the child's home for more than half the time the child was alive in 2025. A child you adopted in 2025, who was lawfully placed with you for legal adoption in 2025, or who was an eligible foster child placed with you during 2025, lived with you for more than half of 2025 if your main home was the child's main home for more than half the time since the adoption or placement. A kidnapped child is treated as living with you for more than half of the year if the child lived with you for more than half the part of the year before the date of the kidnapping or following the date of the child's return. The child must be presumed by law enforcement authorities to have been kidnapped by someone who isn't a member of your family or the child's family. This treatment applies for all years until the child is returned, but the last year it can apply is the earlier of the year there is a determination that the child is dead or the year the child would have reached age 18. If you were on extended active military duty outside the United States (duty ordered for an indefinite period or for more than 90 days), your main home is considered to be in the United States during that duty. Once you begin serving extended active duty, you are considered to be on extended active duty even if you don't serve more than 90 days. The United States means the 50 states and the District of Columbia, not Puerto Rico or a U.S. territory. Answer yes if the child lived with you in the United States for more than half of 2025. Answer no if not, even if you paid most of the child's living expenses.

- i1040gi 4444-4449: "Who lived with you in the United States for more than half of 2025. If the child lived with you in the United States for more than half of 2025, check both boxes (box (a) and box (b)) on row (5) of the Dependents section on page 1 of Form 1040 or 1040-SR. Also, make sure to check the box to the right of the address block on page 1 of Form 1040 or 1040-SR. See Main home and United States, later."
- i1040gi 4453-4454 (line 27a Step 3: lived with you in the United States): "You can’t take the credit for a child who didn’t live with you for more than half the year, even if you paid most of the child’s living expenses. The"
- i1040gi 4753-4763 (Exception to time lived with you): "Exception to time lived with you. Temporary absences by you or the child for special circumstances, such as school, vacation, business, medical care, military service, or detention in a juvenile facility, count as time the child lived with you. Also see Kidnapped child under Who Qualifies as Your Dependent, earlier, and Members of the military, later. A child is considered to have lived with you for more than half of 2025 if the child was born or died in 2025 and your home was this child’s home for more than half the time the child was alive in 2025 or, if you adopted the child in 2025, the child was lawfully placed with you for legal adoption by you in 2025, or if the child was an eligible foster child placed with you during 2025 and your main home was the child’s main home for more than half the time since the child was adopted or placed with you in 2025."
- i1040gi 4802-4808 (Members of the military): "Members of the military. If you were on extended active duty outside the United States, your main home is considered to be in the United States during that duty period. Extended active duty is military duty ordered for an indefinite period or for a period of more than 90 days. Once you begin serving extended active duty, you are considered to be on extended active duty even if you don’t serve more than 90 days."
- i1040gi 4911-4912 (United States): "United States. The United States means the 50 states and the District of Columbia. It doesn’t include Puerto Rico or U.S. ter-"
- i1040gi 4462-4464 (line 27a Step 3: kidnapping): "If the child didn’t live with you for more than half of 2025 because of a temporary absence, birth, death, placement with you for foster or adoption, or kidnapping, see Exception to time lived with you, later."
- p596 1241-1254 (Kidnapped child): "Kidnapped child. A kidnapped child is treated as living with you for more than half of the year if the child lived with you for more than half the part of the year before the date of the kidnapping or following the date of the child’s return. The child must be presumed by law enforcement authorities to have been kidnapped by someone who isn’t a member of your family or the child’s family. This treatment applies for all years until the child is returned. However, the last year this treatment can apply is the earlier of: 1. The year there is a determination that the child is dead, or 2. The year the child would have reached age 18. If your qualifying child has been kidnapped and meets these requirements, enter “KC,” instead of a number, on line 6 of Schedule EIC."

### `eic.child.joint-return` (pos)

Question: Does this child meet the joint return test? Answer yes if the child did not file a joint return for 2025, or filed one only to claim a refund of withheld income tax or estimated tax paid, and, if the child was married at the end of 2025, you can claim the child as your dependent (or could, except for the special rule for children of divorced or separated parents). Answer no otherwise.

- i1040gi 4439-4441 (line 27a Step 3: joint return): "Who isn't filing a joint return for 2025 or is filing a joint return for 2025 only to claim a refund of withheld income tax or estimated tax paid (see Pub. 596 for examples)."
- i1040gi 4799-4801 (Married child): "Married child. A child who was married at the end of 2025 is a qualifying child only if (a) you can claim the child as your dependent, or (b) you could have claimed the child as your dependent except for the special rule for Children of divorced or separated parents under Who Qualifies as Your Dependent, earlier."

### `eic.child.ssn` (pos)

Question: Does this child have a social security number (SSN) issued by the Social Security Administration on or before the due date of your 2025 return (including extensions) that is valid for employment? Answer yes if so. A number with "Not Valid for Employment" printed on the card, issued solely to apply for or receive a federally funded benefit, does not count; a number with "Valid for Work Only With DHS Authorization" counts only while that authorization is still valid. Answer no if the child had no such number by that date; an ITIN or ATIN is not an SSN.

- i1040gi 4876-4889: "Social security number (SSN). For the EIC, a valid SSN is a number issued by the Social Security Administration unless “Not Valid for Employment” is printed on the social security card and the number was issued solely to allow the recipient of the SSN to apply for or receive a federally funded benefit. If “Not Valid for Employment” is printed on the social security Need more information or forms? Visit IRS.gov. card and the cardholder’s immigration status has changed so that they are now a U.S. citizen or permanent resident, ask the SSA for a new social security card without the legend. However, if “Valid for Work Only With DHS Authorization” is printed on your social security card, your SSN is valid for EIC purposes only as long as the DHS authorization is still valid."
- i1040gi 4894-4898 (Social security number (SSN): "If you didn’t have an SSN issued on or before the due date of your 2025 return (including extensions), you can’t claim the EIC on your original or an amended 2025 return. If a child didn’t have an SSN issued on or before the due date of your return (including extensions), you can’t count that child as a qualifying child in figuring the amount of the EIC on your original or an amended 2025 return."
- i1040s8 50-51 (TIN types): "• TIN means taxpayer identification number. A TIN may be an ATIN, an ITIN, or an SSN."
- i1040s8 70-82 (Valid SSN; qualifying child required to have an SSN): "Valid SSN. For the CTC and ACTC, a valid SSN is one that is valid for employment and that is issued by the Social Security Administration before the due date of your 2025 return (including extensions). Qualifying child required to have an SSN. If you have a qualifying child who does not have a valid SSN, you can’t use the child to claim the CTC or ACTC on either your original or an amended 2025 return. See Valid SSN, earlier. If your qualifying child does not have a valid SSN, but has another type of taxpayer identification number issued on or before the due date of your 2025 return (including extensions), you may be able to claim the ODC for that child. See Credit for Other Dependents (ODC), later."

### `dtb.child.another-could-claim` (pos)

Question: Does this child also meet the conditions to be a qualifying child of any other person for 2025, other than your spouse if you file a joint return? Answer yes if another person could also claim the child as a qualifying child. Answer no if no other person could.

- i1040gi 1499-1501: "If the child meets the conditions to be a qualifying child of any other person (other than your spouse if filing jointly) for 2025, see Qualifying child of more than one person, later."
- i1040gi 4468-4470 (another person's qualifying child): "If the child meets the conditions to be a qualifying child of any other person (other than your spouse, if filing a joint return) for 2025, see Qualifying child of more than one person, later. If the child was married, see"
- i1040gi 1943-1976: "Qualifying child of more than one person. Even if a child meets the conditions to be the qualifying child of more than one person, only one person can claim the child as a qualifying child for all of the following tax benefits, unless the special rule for Children of divorced or separated parents, described earlier, applies. 1. Child tax credit and credit for other dependents (line 19) and additional child tax credit (line 28). 2. Head of household filing status. 3. Credit for child and dependent care expenses (Schedule 3, line 2). 4. Exclusion for dependent care benefits (Form 2441, Part III). 5. Earned income credit (line 27a). No other person can take any of the five tax benefits just listed based on the qualifying child. If you and any other person can claim the child as a qualifying child, the following rules apply. For purposes of these rules, the term “parent” means a biological or adoptive parent of an individual. It doesn’t include a stepparent or foster parent unless that person has adopted the individual. • If only one of the persons is the child’s parent, the child is treated as the qualifying child of the parent. • If the parents file a joint return together and can claim the child as a qualifying child, the child is treated as the qualifying child of the parents. • If the parents don’t file a joint return together but both parents claim the child as a qualifying child, the IRS will treat the child as the qualifying child of the parent with whom the child lived for the longer period of time in 2025. If the child lived with each parent for the same amount of time, the IRS will treat the child as the qualifying child of the parent who had the higher adjusted gross income (AGI) for 2025. • If no parent can claim the child as a qualifying child, the child is treated as the qualifying child of the person who had the highest AGI for 2025. • If a parent can claim the child as a qualifying child but no parent does so claim the child, the child is treated as the qualifying child of the person who had the highest AGI for 2025, but only if that person’s AGI is higher than the highest AGI of any parent of the child who can claim the child."
- i1040gi 4828-4864 (Qualifying child of more than one person): "Qualifying child of more than one person. Even if a child meets the conditions to be the qualifying child of more than one person, only one person can claim the child as a qualifying child for all of the following tax benefits, unless the special rule for Children of divorced or separated parents under Who Qualifies as Your Dependent, earlier, applies. 44 1. Child tax credit, credit for other dependents, and additional child tax credit (lines 19 and 28). 2. Head of household filing status. 3. Credit for child and dependent care expenses (Schedule 3, line 2). 4. Exclusion for dependent care benefits (Form 2441, Part III). 5. Earned income credit (line 27a). No other person can take any of the five tax benefits just listed based on the qualifying child. If you and any other person can claim the child as a qualifying child, the following rules apply. For purposes of these rules, the term “parent” means a biological or adoptive parent of an individual. It doesn’t include a stepparent or foster parent unless that person has adopted the individual. • If only one of the persons is the child’s parent, the child is treated as the qualifying child of the parent. • If the parents file a joint return together and can claim the child as a qualifying child, the child is treated as the qualifying child of the parents. • If the parents don’t file a joint return together but both parents claim the child as a qualifying child, the IRS will treat the child as the qualifying child of the parent with whom the child lived for the longer period of time in 2025. If the child lived with each parent for the same amount of time, the IRS will treat the child as the qualifying child of the parent who had the higher adjusted gross income (AGI) for 2025. • If no parent can claim the child as a qualifying child, the child is treated as the qualifying child of the person who had the highest AGI for 2025. • If a parent can claim the child as a qualifying child but no parent does so claim the child, the child is treated as the qualifying child of the person who had the highest AGI for 2025, but only if that person’s AGI is higher than the highest AGI of any parent of the child who can claim the child."

### `dtb.child.multiple-other-claimants` (pos)

Question: Does this child meet the conditions to be a qualifying child of more than one other person for 2025, not counting your spouse if you file a joint return? Answer yes if two or more other people could also claim the child as a qualifying child. Answer no if only one other person could.

- i1040gi 1943-1976: "Qualifying child of more than one person. Even if a child meets the conditions to be the qualifying child of more than one person, only one person can claim the child as a qualifying child for all of the following tax benefits, unless the special rule for Children of divorced or separated parents, described earlier, applies. 1. Child tax credit and credit for other dependents (line 19) and additional child tax credit (line 28). 2. Head of household filing status. 3. Credit for child and dependent care expenses (Schedule 3, line 2). 4. Exclusion for dependent care benefits (Form 2441, Part III). 5. Earned income credit (line 27a). No other person can take any of the five tax benefits just listed based on the qualifying child. If you and any other person can claim the child as a qualifying child, the following rules apply. For purposes of these rules, the term “parent” means a biological or adoptive parent of an individual. It doesn’t include a stepparent or foster parent unless that person has adopted the individual. • If only one of the persons is the child’s parent, the child is treated as the qualifying child of the parent. • If the parents file a joint return together and can claim the child as a qualifying child, the child is treated as the qualifying child of the parents. • If the parents don’t file a joint return together but both parents claim the child as a qualifying child, the IRS will treat the child as the qualifying child of the parent with whom the child lived for the longer period of time in 2025. If the child lived with each parent for the same amount of time, the IRS will treat the child as the qualifying child of the parent who had the higher adjusted gross income (AGI) for 2025. • If no parent can claim the child as a qualifying child, the child is treated as the qualifying child of the person who had the highest AGI for 2025. • If a parent can claim the child as a qualifying child but no parent does so claim the child, the child is treated as the qualifying child of the person who had the highest AGI for 2025, but only if that person’s AGI is higher than the highest AGI of any parent of the child who can claim the child."
- i1040gi 4828-4864 (Qualifying child of more than one person): "Qualifying child of more than one person. Even if a child meets the conditions to be the qualifying child of more than one person, only one person can claim the child as a qualifying child for all of the following tax benefits, unless the special rule for Children of divorced or separated parents under Who Qualifies as Your Dependent, earlier, applies. 44 1. Child tax credit, credit for other dependents, and additional child tax credit (lines 19 and 28). 2. Head of household filing status. 3. Credit for child and dependent care expenses (Schedule 3, line 2). 4. Exclusion for dependent care benefits (Form 2441, Part III). 5. Earned income credit (line 27a). No other person can take any of the five tax benefits just listed based on the qualifying child. If you and any other person can claim the child as a qualifying child, the following rules apply. For purposes of these rules, the term “parent” means a biological or adoptive parent of an individual. It doesn’t include a stepparent or foster parent unless that person has adopted the individual. • If only one of the persons is the child’s parent, the child is treated as the qualifying child of the parent. • If the parents file a joint return together and can claim the child as a qualifying child, the child is treated as the qualifying child of the parents. • If the parents don’t file a joint return together but both parents claim the child as a qualifying child, the IRS will treat the child as the qualifying child of the parent with whom the child lived for the longer period of time in 2025. If the child lived with each parent for the same amount of time, the IRS will treat the child as the qualifying child of the parent who had the higher adjusted gross income (AGI) for 2025. • If no parent can claim the child as a qualifying child, the child is treated as the qualifying child of the person who had the highest AGI for 2025. • If a parent can claim the child as a qualifying child but no parent does so claim the child, the child is treated as the qualifying child of the person who had the highest AGI for 2025, but only if that person’s AGI is higher than the highest AGI of any parent of the child who can claim the child."
- p596 1343-1368 (Rule 9): "Sometimes a child meets the tests to be a qualifying child of more than one person. However, only one of these Rules if You Have a Qualifying Child 13 persons can actually treat the child as a qualifying child. Only that person can use the child as a qualifying child to take all of the following tax benefits (provided the person is eligible for each benefit). 1. The child tax credit, credit for other dependents, or additional child tax credit. 2. Head of household filing status. 3. The credit for child and dependent care expenses. 4. The exclusion for dependent care benefits. 5. The EIC. The other person can’t take any of these benefits based on this qualifying child. In other words, you and the other person can’t agree to divide these tax benefits between you. The other person can’t take any of these tax benefits unless that person has a different qualifying child. The tiebreaker rules, which follow, explain who, if anyone, can claim the EIC when more than one person has the same qualifying child. However, the tiebreaker rules don’t apply if the other person is your spouse and you file a joint return."

### `dtb.child.filer-is-parent` (pos)

Question: Are you, or your spouse if you file a joint return, this child's parent? For this question, a parent is a biological or adoptive parent; a stepparent or foster parent who has not adopted the child is not a parent. Answer yes if you or your spouse is the child's parent. Answer no if not.

- i1040gi 1943-1976: "Qualifying child of more than one person. Even if a child meets the conditions to be the qualifying child of more than one person, only one person can claim the child as a qualifying child for all of the following tax benefits, unless the special rule for Children of divorced or separated parents, described earlier, applies. 1. Child tax credit and credit for other dependents (line 19) and additional child tax credit (line 28). 2. Head of household filing status. 3. Credit for child and dependent care expenses (Schedule 3, line 2). 4. Exclusion for dependent care benefits (Form 2441, Part III). 5. Earned income credit (line 27a). No other person can take any of the five tax benefits just listed based on the qualifying child. If you and any other person can claim the child as a qualifying child, the following rules apply. For purposes of these rules, the term “parent” means a biological or adoptive parent of an individual. It doesn’t include a stepparent or foster parent unless that person has adopted the individual. • If only one of the persons is the child’s parent, the child is treated as the qualifying child of the parent. • If the parents file a joint return together and can claim the child as a qualifying child, the child is treated as the qualifying child of the parents. • If the parents don’t file a joint return together but both parents claim the child as a qualifying child, the IRS will treat the child as the qualifying child of the parent with whom the child lived for the longer period of time in 2025. If the child lived with each parent for the same amount of time, the IRS will treat the child as the qualifying child of the parent who had the higher adjusted gross income (AGI) for 2025. • If no parent can claim the child as a qualifying child, the child is treated as the qualifying child of the person who had the highest AGI for 2025. • If a parent can claim the child as a qualifying child but no parent does so claim the child, the child is treated as the qualifying child of the person who had the highest AGI for 2025, but only if that person’s AGI is higher than the highest AGI of any parent of the child who can claim the child."
- i1040gi 4828-4864 (Qualifying child of more than one person): "Qualifying child of more than one person. Even if a child meets the conditions to be the qualifying child of more than one person, only one person can claim the child as a qualifying child for all of the following tax benefits, unless the special rule for Children of divorced or separated parents under Who Qualifies as Your Dependent, earlier, applies. 44 1. Child tax credit, credit for other dependents, and additional child tax credit (lines 19 and 28). 2. Head of household filing status. 3. Credit for child and dependent care expenses (Schedule 3, line 2). 4. Exclusion for dependent care benefits (Form 2441, Part III). 5. Earned income credit (line 27a). No other person can take any of the five tax benefits just listed based on the qualifying child. If you and any other person can claim the child as a qualifying child, the following rules apply. For purposes of these rules, the term “parent” means a biological or adoptive parent of an individual. It doesn’t include a stepparent or foster parent unless that person has adopted the individual. • If only one of the persons is the child’s parent, the child is treated as the qualifying child of the parent. • If the parents file a joint return together and can claim the child as a qualifying child, the child is treated as the qualifying child of the parents. • If the parents don’t file a joint return together but both parents claim the child as a qualifying child, the IRS will treat the child as the qualifying child of the parent with whom the child lived for the longer period of time in 2025. If the child lived with each parent for the same amount of time, the IRS will treat the child as the qualifying child of the parent who had the higher adjusted gross income (AGI) for 2025. • If no parent can claim the child as a qualifying child, the child is treated as the qualifying child of the person who had the highest AGI for 2025. • If a parent can claim the child as a qualifying child but no parent does so claim the child, the child is treated as the qualifying child of the person who had the highest AGI for 2025, but only if that person’s AGI is higher than the highest AGI of any parent of the child who can claim the child."
- i1040gi 1959-1959: "For purposes of these rules, the term “parent” means a biological or adoptive parent of an individual. It doesn’t include a stepparent or foster parent unless that person has adopted the individual."
- i1040gi 4847-4847 (parent): "For purposes of these rules, the term “parent” means a biological or adoptive parent of an individual. It doesn’t include a stepparent or foster parent unless that person has adopted the individual."

### `dtb.child.other-is-parent` (pos)

Question: Is the other person who could claim this child the child's parent? For this question, a parent is a biological or adoptive parent; a stepparent or foster parent who has not adopted the child is not a parent. Answer yes if the other person is the child's parent. Answer no if not.

- i1040gi 1943-1976: "Qualifying child of more than one person. Even if a child meets the conditions to be the qualifying child of more than one person, only one person can claim the child as a qualifying child for all of the following tax benefits, unless the special rule for Children of divorced or separated parents, described earlier, applies. 1. Child tax credit and credit for other dependents (line 19) and additional child tax credit (line 28). 2. Head of household filing status. 3. Credit for child and dependent care expenses (Schedule 3, line 2). 4. Exclusion for dependent care benefits (Form 2441, Part III). 5. Earned income credit (line 27a). No other person can take any of the five tax benefits just listed based on the qualifying child. If you and any other person can claim the child as a qualifying child, the following rules apply. For purposes of these rules, the term “parent” means a biological or adoptive parent of an individual. It doesn’t include a stepparent or foster parent unless that person has adopted the individual. • If only one of the persons is the child’s parent, the child is treated as the qualifying child of the parent. • If the parents file a joint return together and can claim the child as a qualifying child, the child is treated as the qualifying child of the parents. • If the parents don’t file a joint return together but both parents claim the child as a qualifying child, the IRS will treat the child as the qualifying child of the parent with whom the child lived for the longer period of time in 2025. If the child lived with each parent for the same amount of time, the IRS will treat the child as the qualifying child of the parent who had the higher adjusted gross income (AGI) for 2025. • If no parent can claim the child as a qualifying child, the child is treated as the qualifying child of the person who had the highest AGI for 2025. • If a parent can claim the child as a qualifying child but no parent does so claim the child, the child is treated as the qualifying child of the person who had the highest AGI for 2025, but only if that person’s AGI is higher than the highest AGI of any parent of the child who can claim the child."
- i1040gi 4828-4864 (Qualifying child of more than one person): "Qualifying child of more than one person. Even if a child meets the conditions to be the qualifying child of more than one person, only one person can claim the child as a qualifying child for all of the following tax benefits, unless the special rule for Children of divorced or separated parents under Who Qualifies as Your Dependent, earlier, applies. 44 1. Child tax credit, credit for other dependents, and additional child tax credit (lines 19 and 28). 2. Head of household filing status. 3. Credit for child and dependent care expenses (Schedule 3, line 2). 4. Exclusion for dependent care benefits (Form 2441, Part III). 5. Earned income credit (line 27a). No other person can take any of the five tax benefits just listed based on the qualifying child. If you and any other person can claim the child as a qualifying child, the following rules apply. For purposes of these rules, the term “parent” means a biological or adoptive parent of an individual. It doesn’t include a stepparent or foster parent unless that person has adopted the individual. • If only one of the persons is the child’s parent, the child is treated as the qualifying child of the parent. • If the parents file a joint return together and can claim the child as a qualifying child, the child is treated as the qualifying child of the parents. • If the parents don’t file a joint return together but both parents claim the child as a qualifying child, the IRS will treat the child as the qualifying child of the parent with whom the child lived for the longer period of time in 2025. If the child lived with each parent for the same amount of time, the IRS will treat the child as the qualifying child of the parent who had the higher adjusted gross income (AGI) for 2025. • If no parent can claim the child as a qualifying child, the child is treated as the qualifying child of the person who had the highest AGI for 2025. • If a parent can claim the child as a qualifying child but no parent does so claim the child, the child is treated as the qualifying child of the person who had the highest AGI for 2025, but only if that person’s AGI is higher than the highest AGI of any parent of the child who can claim the child."
- i1040gi 1959-1959: "For purposes of these rules, the term “parent” means a biological or adoptive parent of an individual. It doesn’t include a stepparent or foster parent unless that person has adopted the individual."
- i1040gi 4847-4847 (parent): "For purposes of these rules, the term “parent” means a biological or adoptive parent of an individual. It doesn’t include a stepparent or foster parent unless that person has adopted the individual."

### `dtb.child.form-8332-released` (pos)

Question: Does the special rule for children of divorced or separated parents apply to this child for 2025 through a release of the claim to the child: the custodial parent signs Form 8332 or a substantially similar statement that they won't claim the child as a dependent for 2025 (or, for a decree or agreement that went into effect after 1984 and before 2009, certain pages from it), or a pre-1985 decree of divorce or separate maintenance or written separation agreement provides that the noncustodial parent can claim the child and the noncustodial parent provides at least $600 for the child's support during 2025? Answer yes if such a release applies. Answer no if none does.

- i1040gi 1800-1823 (Children of divorced or separated parents): "Children of divorced or separated parents. A child will be treated as the qualifying child or qualifying relative of the child’s noncustodial parent (defined later) if all of the following conditions apply. 1. The parents are divorced, legally separated, separated under a written separation agreement, or lived apart at all times during the last 6 months of 2025 (whether or not they are or were married). 2. The child received over half of the child’s support for 2025 from the parents (and the rules on Multiple support agreements, later, don’t apply). Support of a child received from a parent’s spouse is treated as provided by the parent. 3. The child is in custody of one or both of the parents for more than half of 2025. 4. Either of the following applies. a. The custodial parent signs Form 8332 or a substantially similar statement that they won’t claim the child as a dependent for 2025, and the noncustodial parent includes a copy of the form or statement with their return. If the divorce decree or separation agreement went into effect after 1984 and before 2009, the noncustodial parent may be able to include certain pages from the decree or agreement instead of Form 8332. See Post-1984 and pre-2009 decree or agreement and Post-2008 decree or agreement. b. A pre-1985 decree of divorce or separate maintenance or written separation agreement between the parents provides that the noncustodial parent can claim the child as a dependent, and the noncustodial parent provides at least $600 for support of the child during 2025."
- i1040gi 1859-1866 (Post-2008 decree or agreement): "Post-2008 decree or agreement. If the divorce decree or separation agreement went into effect after 2008, the noncustodial parent can’t include pages from the decree or agreement instead of Form 8332. The custodial parent must sign either Form 8332 or a substantially similar statement the only purpose of which is to release the custodial parent’s claim to certain tax benefits for a child, and the noncustodial parent must include a copy with their return. The form or statement must release the custodial parent’s claim to the child without any conditions. For example, the release must not depend on the noncustodial parent paying support."

### `dtb.child.more-nights-with-filer` (pos)

Question: Did this child live with you for more nights in 2025 than with the other parent? Answer yes if the child lived with you for the greater number of nights. Answer no if not.

- i1040gi 1832-1835 (Custodial and noncustodial parents): "Custodial and noncustodial parents. The custodial parent is the parent with whom the child lived for the greater number of nights in 2025. The noncustodial parent is the other parent. If the child was with each parent for an equal number of nights,"
- i1040gi 1965-1967 (lived with the parent for the longer period): "• If the parents don’t file a joint return together but both parents claim the child as a qualifying child, the IRS will treat the child as the qualifying child of the parent with whom the child lived for the longer period of time in 2025. If the child lived"

### `dtb.child.same-nights` (pos)

Question: Did this child live with you and with the other parent for the same number of nights in 2025? Answer yes if the number of nights was equal. Answer no if the child lived with the other parent for more nights.

- i1040gi 1834-1837 (equal number of nights): "nights in 2025. The noncustodial parent is the other parent. If the child was with each parent for an equal number of nights, the custodial parent is the parent with the higher adjusted gross income. See Pub. 501 for an exception for a parent who works"
- i1040gi 1967-1969 (same amount of time: the higher AGI): "lived for the longer period of time in 2025. If the child lived with each parent for the same amount of time, the IRS will treat the child as the qualifying child of the parent who had the higher adjusted gross income (AGI) for 2025."

### `dtb.child.filer-agi-higher` (pos)

Question: Was your adjusted gross income (AGI) for 2025 higher than the other person's AGI for 2025? Answer yes if your AGI was higher. Answer no if it was the same or lower.

- i1040gi 1967-1976 (the higher or highest AGI): "lived for the longer period of time in 2025. If the child lived with each parent for the same amount of time, the IRS will treat the child as the qualifying child of the parent who had the higher adjusted gross income (AGI) for 2025. • If no parent can claim the child as a qualifying child, the child is treated as the qualifying child of the person who had the highest AGI for 2025. • If a parent can claim the child as a qualifying child but no parent does so claim the child, the child is treated as the qualifying child of the person who had the highest AGI for 2025, but only if that person’s AGI is higher than the highest AGI of any parent of the child who can claim the child."

### `dtb.child.same-agi` (pos)

Question: Was your adjusted gross income (AGI) for 2025 the same as the other person's AGI for 2025? Answer yes if the two were equal. Answer no if yours was lower.

- i1040gi 1967-1976 (the higher or highest AGI): "lived for the longer period of time in 2025. If the child lived with each parent for the same amount of time, the IRS will treat the child as the qualifying child of the parent who had the higher adjusted gross income (AGI) for 2025. • If no parent can claim the child as a qualifying child, the child is treated as the qualifying child of the person who had the highest AGI for 2025. • If a parent can claim the child as a qualifying child but no parent does so claim the child, the child is treated as the qualifying child of the person who had the highest AGI for 2025, but only if that person’s AGI is higher than the highest AGI of any parent of the child who can claim the child."
- p596 1384-1405 (tiebreaker rules): "• If the parents don’t file a joint return together but both parents claim the child as a qualifying child, the IRS will treat the child as the qualifying child of the parent with whom the child lived for the longer period of time during the year. If the child lived with each parent for the same amount of time, the IRS will treat the child as the qualifying child of the parent who had the higher AGI for the year. • If no parent can claim the child as a qualifying child, the child is treated as the qualifying child of the person who had the highest AGI for the year. • If a parent can claim the child as a qualifying child but no parent claims the child, the child is treated as the qualifying child of the person who had the highest AGI for the year, but only if that person’s AGI is higher than the highest AGI of any of the child’s parents who can claim the child."

### `dtb.child.other-will-claim` (pos)

Question: Will the other person claim this child as a qualifying child on their 2025 tax return? Answer yes if they will claim the child, or if you do not know. Answer no if they will not.

- i1040gi 1973-1976 (a parent can claim but no parent does so claim): "• If a parent can claim the child as a qualifying child but no parent does so claim the child, the child is treated as the qualifying child of the person who had the highest AGI for 2025, but only if that person’s AGI is higher than the highest AGI of any parent of the child who can claim the child."
- p596 1399-1405: "• If a parent can claim the child as a qualifying child but no parent claims the child, the child is treated as the qualifying child of the person who had the highest AGI for the year, but only if that person’s AGI is higher than the highest AGI of any of the child’s parents who can claim the child."
- p596 1417-1419 (you and the other person may choose who claims): "Subject to these tiebreaker rules, you and the other person may be able to choose which of you claims the child as a qualifying child. See Example 1 through Example 12, later."

### `ctc.child.under-17` (pos)

Question: Was this child under age 17 at the end of 2025? Answer yes if so. Answer no if the child was age 17 or older at the end of 2025.

- i1040gi 1586-1586 (Step 3 question 3): "3. Was the child under age 17 at the end of 2025?"
- i1040s8 140-150 (Credits for Qualifying Children): "Credits for Qualifying Children The CTC and ACTC are credits for individuals who claim a child as a dependent if the child meets certain conditions. To claim a child for the CTC and ACTC, the child must be your dependent, under age 17 at the end of 2025, and meet all the conditions in Steps 1 through 3 under Who Qualifies as Your Dependent in the Instructions for Form 1040. Example 1. Your child turned 17 on December 30, 2025, and is a citizen of the United States and claimed as a dependent on your return. You can’t use the child to claim the CTC or ACTC because the child was not under age 17 at the end of 2025."

### `ctc.child.lived-with-you` (pos)

Question: Did this child live with you for more than half of 2025? Count temporary absences for special circumstances, such as school, vacation, business, medical care, military service, or detention in a juvenile facility, as time the child lived with you. A child who was born or died in 2025 lived with you for more than half of 2025 if your home was the child's home for more than half the time the child was alive in 2025. A child you adopted in 2025, who was lawfully placed with you for legal adoption in 2025, or who was an eligible foster child placed with you during 2025, lived with you for more than half of 2025 if your main home was the child's main home for more than half the time since the adoption or placement. A kidnapped child is treated as living with you for more than half of the year if the child lived with you for more than half the part of the year before the date of the kidnapping or following the date of the child's return. The child must be presumed by law enforcement authorities to have been kidnapped by someone who isn't a member of your family or the child's family. This treatment applies for all years until the child is returned, but the last year it can apply is the earlier of the year there is a determination that the child is dead or the year the child would have reached age 18. Answer yes if the child lived with you for more than half of 2025. Answer no if not.

- i1040gi 1492-1495 (Step 1: lived with you): "Who lived with you for more than half of 2025. If the child didn’t live with you for the required time, see Exception to time lived with you, later. If the child lived with you for more than half of 2025, check the “Yes” box (box (a)) on row (5) of the Dependents section on page 1 of Form 1040 or 1040-SR."
- i1040gi 1881-1896 (Exception to time lived with you): "Exception to time lived with you. Temporary absences by you or the other person for special circumstances, such as school, vacation, business, medical care, military service, or detention in a juvenile facility, count as time the person lived with you. Also see Children of divorced or separated parents, earlier, or Kidnapped child, later. If the person meets all other requirements to be your qualifying child but was born or died in 2025, the person is considered to have lived with you for more than half of 2025 if your home was this person’s home for more than half the time the person was alive in 2025. If the person meets all other requirements to be your qualifying child but you adopted the person in 2025, the person was lawfully placed with you for legal adoption by you in 2025, or if the person was an eligible foster child placed with you during 2025, the person is considered to have lived with you for more than half of 2025 if your main home was this person’s main home for more than half the time since the person was adopted or placed with you in 2025."
- i1040gi 1916-1920 (Kidnapped child): "Kidnapped child. If your child is presumed by law enforcement authorities to have been kidnapped by someone who isn’t a family member, you may be able to take the child into account in determining your eligibility for head of household or qualifying surviving spouse filing status, the child tax credit, the credit for other dependents, and the earned income credit (EIC). For details, see Pub. 501 (Pub. 596 for the EIC)."
- p596 1241-1254 (Kidnapped child): "Kidnapped child. A kidnapped child is treated as living with you for more than half of the year if the child lived with you for more than half the part of the year before the date of the kidnapping or following the date of the child’s return. The child must be presumed by law enforcement authorities to have been kidnapped by someone who isn’t a member of your family or the child’s family. This treatment applies for all years until the child is returned. However, the last year this treatment can apply is the earlier of: 1. The year there is a determination that the child is dead, or 2. The year the child would have reached age 18. If your qualifying child has been kidnapped and meets these requirements, enter “KC,” instead of a number, on line 6 of Schedule EIC."

### `ctc.child.no-over-half-support` (abs)

Question: Did this child provide over half of their own support for 2025? Answer yes if the child did. Answer no if the child did not.

- i1040gi 1482-1482 (Step 1: didn't provide over half of their own support): "Who didn't provide over half of their own support for 2025 (see Pub. 501)"

### `ctc.child.citizen-or-resident` (pos)

Question: Was this child a U.S. citizen, U.S. national, or U.S. resident alien? Answer yes if so. Also answer yes if the child is your adopted child, lived with you all year as a member of your household, and you are a U.S. citizen or U.S. national. Answer no otherwise, including if the child was only a resident of Canada or Mexico.

- i1040gi 1573-1576 (Step 3 question 2): "2. Was the child a U.S. citizen, U.S. national, or U.S. resident alien? (See Pub. 519 for the definition of a U.S. national or U.S. resident alien. If the child was adopted, see Exception to citizen test, later.)"
- i1040gi 1871-1873 (Exception to citizen test): "Exception to citizen test. If you are a U.S. citizen or U.S. national and your adopted child lived with you all year as a member of your household, that child meets the requirement to be a U.S. citizen in Step 2, question 1; Step 3, question 2; Step 4, question 2; and Step 5, question 3."
- i1040gi 1519-1522 (Step 2 question 1: Canada or Mexico): "1. Was the child a U.S. citizen, U.S. national, U.S. resident alien, or a resident of Canada or Mexico? (See Pub. 519 for the definition of a U.S. national or U.S. resident alien. If the child was adopted, see Exception to citizen test, later.)"

### `odc.child.tin` (pos)

Question: Does this child have a social security number (SSN), individual taxpayer identification number (ITIN), or adoption taxpayer identification number (ATIN) issued on or before the due date of your 2025 return (including extensions)? Answer yes if the child has one, or if you apply for an ITIN or ATIN for the child on or before that date. Answer no if the child has none of these numbers.

- i1040gi 1618-1622 (Step 3 question 1): "1. Did the child have an SSN, ITIN, or adoption taxpayer identification number (ATIN) issued on or before the due date of your return (including extensions)? (Answer “Yes” if you are applying for an ITIN or ATIN for the child on or before the due date of your return (including extensions).)"
- i1040s8 97-107 (Dependent required to have a TIN): "Dependent required to have a TIN. If you have a dependent who does not have an SSN, ITIN, or ATIN issued on or before the due date of your 2025 return (including extensions), you can’t use that dependent to claim the ODC on either your original or an amended 2025 return. Instructions for Schedule 8812 (Form 1040) (2025) Catalog Number 59790P Jan 23, 2026 Department of the Treasury Internal Revenue Service www.irs.govIf you apply for an ITIN or ATIN for the dependent on or before the due date of your 2025 return (including extensions) and the IRS issues the ITIN or ATIN as a result of the application, the IRS will consider the ITIN or ATIN as issued on or before the due date of your return."

### `odc.dependent.relationship` (pos)

Question: Is this person your son, daughter, stepchild, foster child, or a descendant of any of them; your brother, sister, half brother, half sister, or a son or daughter of any of them; your father, mother, or an ancestor or sibling of either of them; or your stepbrother, stepsister, stepfather, stepmother, son-in-law, daughter-in-law, father-in-law, mother-in-law, brother-in-law, or sister-in-law? Answer yes if so. Also answer yes if this person, other than your spouse, lived with you all year as a member of your household and your relationship didn't violate local law. Answer no otherwise.

- i1040gi 1640-1657 (Step 4: a qualifying relative is your...): "A qualifying relative is your... Son, daughter, stepchild, foster child, or a descendant of any of them (for example, your grandchild) or Brother, sister, half brother, half sister, or a son or daughter of any of them (for example, your niece or nephew) or Father, mother, or an ancestor or sibling of either of them (for example, your grandmother, grandfather, aunt, or uncle) or Stepbrother, stepsister, stepfather, stepmother, son-in-law, daughter-in-law, father-in-law, mother-in-law, brother-in-law, or sister-in-law or Any other person (other than your spouse) who lived with you all year as a member of your household if your relationship didn’t violate local law. If the person didn’t live with you for the required time, see Exception to time lived with you, later."

### `odc.dependent.not-qualifying-child` (abs)

Question: Was this person a qualifying child of any taxpayer for 2025? For this question, a person isn't a taxpayer if the person isn't required to file a U.S. income tax return and either doesn't file one or files only to get a refund of withheld income tax or estimated tax paid. Answer yes if this person was a qualifying child of any taxpayer. Answer no if not.

- i1040gi 1661-1664 (Step 4: who wasn't a qualifying child): "Who wasn’t a qualifying child (see Step 1) of any taxpayer for 2025. For this purpose, a person isn’t a taxpayer if the person isn’t required to file a U.S. income tax return and either doesn’t file such a return or files only to get a refund of withheld income tax or estimated tax paid. See Pub. 501 for details and examples."

### `odc.dependent.gross-income-under-limit` (pos)

Question: Did this person have gross income of less than $5,200 in 2025? Answer yes if so. Answer no if it was $5,200 or more, even if the person was permanently and totally disabled.

- i1040gi 1668-1669 (Step 4: gross income): "Who had gross income of less than $5,200 in 2025. If the person was permanently and totally disabled, see Exception to gross income test, later."
- i1040gi 1874-1877 (Exception to gross income test): "Exception to gross income test. If your relative (including a person who lived with you all year as a member of your household) is permanently and totally disabled (defined later), certain income for services performed at a sheltered workshop may be excluded for this test. For details, see Pub. 501."

### `odc.dependent.over-half-support` (pos)

Question: Did you provide over half of this person's support in 2025? Answer yes if you did. Answer no if you did not, including where you would be treated as providing it only under a multiple support agreement. If this person is your child who is presumed by law enforcement authorities to have been kidnapped by someone who isn't a family member, you may be able to take the child into account for the credit for other dependents.

- i1040gi 1673-1675 (Step 4: support): "For whom you provided over half of the person’s support in 2025. But see Children of divorced or separated parents, Multiple support agreements, and Kidnapped child, later."
- i1040gi 1925-1933 (Multiple support agreements): "Multiple support agreements. If no one person contributed over half of the support of your relative (or a person who lived Need more information or forms? Visit IRS.gov. with you all year as a member of your household) but you and another person(s) provided more than half of your relative’s support, special rules may apply that would treat you as having provided over half of the support. For details, see Pub. 501."
- i1040gi 1916-1920 (Kidnapped child): "Kidnapped child. If your child is presumed by law enforcement authorities to have been kidnapped by someone who isn’t a family member, you may be able to take the child into account in determining your eligibility for head of household or qualifying surviving spouse filing status, the child tax credit, the credit for other dependents, and the earned income credit (EIC). For details, see Pub. 501 (Pub. 596 for the EIC)."

### `odc.dependent.tin` (pos)

Question: Does this person have a social security number (SSN), individual taxpayer identification number (ITIN), or adoption taxpayer identification number (ATIN) issued on or before the due date of your 2025 return (including extensions)? Answer yes if they have one, or if you apply for an ITIN or ATIN for them on or before that date. Answer no if they have none of these numbers.

- i1040gi 1734-1738 (Step 5 question 2): "2. Did your qualifying relative have an SSN, ITIN, or ATIN issued on or before the due date of your 2025 return (including extensions)? (Answer “Yes” if you are applying for an ITIN or ATIN for the qualifying relative on or before the return due date (including extensions).)"
- i1040s8 97-107 (Dependent required to have a TIN): "Dependent required to have a TIN. If you have a dependent who does not have an SSN, ITIN, or ATIN issued on or before the due date of your 2025 return (including extensions), you can’t use that dependent to claim the ODC on either your original or an amended 2025 return. Instructions for Schedule 8812 (Form 1040) (2025) Catalog Number 59790P Jan 23, 2026 Department of the Treasury Internal Revenue Service www.irs.govIf you apply for an ITIN or ATIN for the dependent on or before the due date of your 2025 return (including extensions) and the IRS issues the ITIN or ATIN as a result of the application, the IRS will consider the ITIN or ATIN as issued on or before the due date of your return."

### `odc.dependent.citizen-or-resident` (pos)

Question: Was this person a U.S. citizen, U.S. national, or U.S. resident alien? Answer yes if so. Also answer yes if the person is your adopted child, lived with you all year as a member of your household, and you are a U.S. citizen or U.S. national. Answer no otherwise, including if the person was only a resident of Canada or Mexico.

- i1040gi 1763-1774 (Step 5 question 3): "3. Was your qualifying relative a U.S. citizen, U.S. national, or U.S. resident alien? (See Pub. 519 for the definition of a You can’t claim this person as a dependent. Need more information or forms? Visit IRS.gov. 19 U.S. national or a U.S. resident alien. If your qualifying relative was adopted, see Exception to citizen test, later.)"
- i1040gi 1871-1873 (Exception to citizen test): "Exception to citizen test. If you are a U.S. citizen or U.S. national and your adopted child lived with you all year as a member of your household, that child meets the requirement to be a U.S. citizen in Step 2, question 1; Step 3, question 2; Step 4, question 2; and Step 5, question 3."
- i1040s8 170-172: "3. The person was a U.S. citizen, U.S. national, or U.S. resident alien. For more information, see Pub. 519. If the person is your adopted child, see Adopted child, later."
- i1040s8 186-193 (ODC condition 3; Adopted child): "Adopted child. An adopted child is always treated as your own child. An adopted child includes a child lawfully placed with you for legal adoption. If you are a U.S. citizen or U.S. national and your adopted child lived with you all year as a member of your household in 2025, that child meets condition (3), earlier, to be a qualifying person for the ODC."

### `odc.dependent.not-joint-return` (abs)

Question: Did this person file a joint return for 2025, other than one filed only to claim a refund of withheld income tax or estimated tax paid? Answer yes if so. Answer no if the person did not file a joint return, including if the person was married and filed separately, or filed one only to claim such a refund.

- i1040gi 1752-1756 (Step 4 question 3: was your qualifying relative married): "3. Was your qualifying relative married? Yes. See Married No. Continue 䊲 person, later."
- i1040gi 1921-1924 (Married person): "Married person. If the person is married and files a joint return, you can’t claim that person as your dependent. However, if the person is married but doesn’t file a joint return or files a joint return only to claim a refund of withheld income tax or estimated tax paid, you may be able to claim that person as a dependent. (See Pub. 501 for details and examples.) In that case, go to Step 2, question 3 (for a qualifying child), or Step 4, question 4 (for a qualifying relative)."


## Result lines

After the last code edit, the full suite (`pytest`, its
379 test files in eleven foreground runs, each under the ten-minute command
bound; together they are every file `pytest` collects):

- `1505 passed, 394 subtests passed in 440.92s`
- `419 passed, 2118 subtests passed in 73.19s`
- `409 passed, 1 skipped, 106 subtests passed in 368.42s`
- `759 passed, 62 subtests passed in 200.86s`
- `431 passed, 1097 subtests passed in 158.02s`
- `374 passed, 3680 subtests passed in 74.60s`
- `415 passed, 3 skipped, 2445 subtests passed in 150.75s`
- `755 passed, 782 subtests passed in 164.26s`
- `742 passed, 8 skipped, 94 subtests passed in 235.24s`
- `1141 passed, 165 subtests passed in 416.18s`
- `489 passed, 13 skipped, 190 subtests passed in 84.53s`

Together: 7439 passed, 25 skipped, 11133 subtests passed, no failure.

`python3 -m mypy` then found three typing errors in the new unit test's
validator fixture; it was annotated (no behavior change). After that last
edit:

- `python3 -m mypy`: `Success: no issues found in 531 source files`
- `pytest tests/test_eic_child_answers_walk.py`: `14 passed, 6 subtests passed in 1.18s`
- `pytest -m "not live"`: `1940 passed, 8 skipped, 5970 subtests passed in 15.62s`
- `pytest tests/test_schema_registry.py`: `14 passed in 1.22s`
- `python3 tools/governance_lint.py`: `governance lint: conformant`;
  `python3 tools/envelope_scan.py` over the Track 1 range: no finding.
