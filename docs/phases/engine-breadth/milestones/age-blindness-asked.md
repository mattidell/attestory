<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "age-blindness-asked",
  "status": "Open. Track 1 built; review ready with should-fix; repair chartered (Decision 11).",
  "scope": [
    "a return cannot publish the standard deduction, the additional amounts for age 65 or older and blindness, or the senior deduction while the filer's (and on a joint return the spouse's) age or blindness may be unasked",
    "each question says what its rule reads, per the 2025 instructions, including the day-before-the-birthday rule and a death in 2025",
    "every recorded return computes the same numbers once answered as its record implies"
  ],
  "non_goals": [
    "no engine, schema or kernel change unless P0 shows none can be avoided and the owner agrees",
    "the dependent's standard deduction worksheet beyond what age and blindness already feed"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/age-blindness-asked.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/age-blindness-asked.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/age-blindness-asked.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/age-blindness-asked.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Age and Blindness Are Asked (2025)

Milestone key: age-blindness-asked.
Branch: milestone/age-blindness-asked-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-11.
Starting point: `milestone/question-wording-2025` at `9dab3113`
(PR #273, scratch core v87; stacked on PR #270, core v86).

## What we are trying to accomplish

The question-wording Track 0 measured that the four facts for the filer's
and spouse's age 65 or older and blindness default to false and no question
asks for them. A filer born before January 2, 1961 gets the 15,750
standard deduction instead of 17,750 plus the 6,000 senior deduction. The
useful outcome is a core that asks, and cannot publish those amounts while
the answers are missing.

## What we know

- question-wording P0 and Track 0 (`alc_title_age`,
  `alc_title_spouse_age`, `alc_title_spouse_died_before_65`,
  `alc_title_blind`) show the hand values when the facts are recorded true.
- **What we do not know.** Where the default comes from (rule, binding or
  recording surface); whether a question can be added by content alone;
  which rules read the facts (standard deduction, the senior deduction,
  credits, the dependent worksheet); how many recorded returns would newly
  be asked, and whether any number changes once answered as recorded.

## Actions the team will take

1. **P0: measure and design.** Trace the four facts and their default.
   Quote the 2025 instructions. Probe v86 and scratch v87. Prototype the
   smallest content-only fix on a scratch core after v87. Stop and report
   if it needs an engine, schema, selection or recording change.
2. **Decide**, after the owner's disposition on PR #273.
3. **Track 0 adversarial closure.**
4. **Track 1: build.**
5. **Close.** Review, repair, exact-head CI, retrospective, roadmap.

## Cases that will shape the design

- Single filer born January 1, 1961; born January 2, 1961; born
  January 1, 1960 and blind.
- Joint return: one spouse 65, the other not; spouse died in 2025 before
  65; spouse died in 2025 after turning 65.
- A filer who can be claimed as a dependent and is 65 or blind.
- Every recorded return earlier milestones replay.

## Process

Dispatch through the grok CLI. Owner, 2026-11-11: no Opus or Sonnet
sub-agents when grok is at its limit; wait for the reset. Hand values come
from the instructions. Stacked on question-wording (PR #273), which is
closed.

## P0 result

Evidence: `age-blindness-asked-evidence/p0.md` (scripts and outputs beside
it). No stop condition was hit.

- **The default.** The false comes from two pieces of package content. Each
  fact's input binding is `optional_default`, and its fact type names
  `parameter.default-false`. Three rules read the facts: dependents
  worksheet line 1, which feeds both standard deduction paths, and
  Schedule 1-A lines 36a and 36b. No question, form field or recording
  surface names them.
- **The design (scratch core v88 on question-wording's v87).** Content
  only:
  - the four bindings become `required`;
  - four input questions follow the 2025 instructions (the day before the
    birthday, a 2025 death, the blindness statement, and the
    separate-return condition for a spouse);
  - worksheet line 1 v2 reads the spouse only on a joint or separate return
    and asks every missing answer at once;
  - line 36b v2 reads the spouse only on a joint return.
- **Probes.** 11 cases, each reaching its hand value on v86, v87 and v88 when
  answered. Unanswered, v86 and v87 are silently wrong in 7 of them. v88
  blocks 20 fields and asks only the new questions.
- **Recorded returns.** Of 775 lists, 691 compute; all 691 are newly asked
  (the taxpayer's two questions; all are single returns). Answered false as
  the record implies, 690 are identical to v86, and the last is identical to
  v87 (question-wording's own sentence). The other 84 are refused
  identically on every run.
- **One intended number change.** A qualifying surviving spouse return no
  longer counts the spouse's boxes, per the 2025 chart. No recorded return
  has one.
- **Decisions for the foreman** are in p0.md: take the design; qualifying
  surviving spouse; the separate-return title; the unused default; the
  question words; the Track 1 loader and test-helper scope; joint and
  dependent recorded returns for Track 0; rebuild if PR #273 changes v87.

## Decisions

Foreman, 2026-11-11, on P0. Each is the P0 recommendation.

1. **Design.** Take it: the four bindings become `required`, four input
   questions, dependents worksheet line 1 v2 and Schedule 1-A line 36b v2.
   Content only.
2. **Qualifying surviving spouse.** Count only the taxpayer's boxes, as the
   2025 chart does. This is the one intended number change; no recorded
   return has it.
3. **Separate-return condition.** The two spouse facts are retitled to carry
   it, in a vocabulary bundle v4 built on question-wording's v3 (which now
   also names December 31, 2025 for blindness).
4. **The unused default** stays on the fact types. The binding mode decides;
   no fact-type successor.
5. **Question words.** The P0 sentences stand, including the taxpayer's
   death-before-65 sentence (Publication 501) and the separate-return
   sentence on both spouse questions. Track 0 tests each the way a truthful
   filer reads it, including the populations the law excludes.
6. **Track 1 scope.** The v88 loader entries (as for v87) and the test
   helper: every test that runs a return on v88 states the taxpayer's two
   facts.
7. **Track 0** adds joint, separate and dependent returns to the rerun set.
   Blindness for someone who died in 2025 is parked: neither source says
   how it is judged.
8. **Order.** PR #273 changed v87 after P0 (the Exception 1 words, the
   blindness title). Track 0 first rebuilds scratch v88 on the final v87 and
   reruns the probe and the rerun.

9. **The separate-return condition is its own fact** (foreman, 2026-11-12,
   on Track 0's `late_joint_to_separate`). Decision 3 put the condition in
   the spouse questions and titles, so a spouse-age yes recorded on a
   joint return kept counting after the status became separate (line 12e
   17,350, not 15,750). The spouse age and blindness facts and questions
   state only age and blindness, true whatever the filing status. One
   return-level fact, asked only on a separate return, states the
   condition (the spouse had no income, is not filing a return, and cannot
   be claimed as a dependent); worksheet line 1 counts the spouse's boxes
   on a separate return only when it is yes. If an existing fact already
   says exactly this, it is reused instead. Track 0 reruns every table
   the change touches.

10. **The condition is asked as a question** (foreman, 2026-11-12, on the
    Decision 9 rerun). The condition fact's question becomes "Is it true
    that your spouse had no income, isn't filing a return, and can't be
    claimed as a dependent on another person's return?", in the "Is it
    true that" form the Exception 1 question uses, with the same three
    conditions the 2025 instructions state. Track 1 builds it; nothing
    else in Decision 9 changes.

11. **Review repair** (foreman, 2026-11-12, on
    `docs/reviews/age-blindness-asked/review.md`, verdict ready). The v88
    members are branch-only, so they are regenerated in place.
    - F1: on a separate return the spouse's age and blindness are asked
      only when the condition is yes; a no publishes the box count without
      them. This narrows Decision 9's always-asked set to the three facts
      that can move a number.
    - F2: the live module replays the 298 v83 lists, as earlier milestones
      do; the 775-list replay stays in the committed evidence
      (`tools/recorded_replay.py` reproduces it on demand).
    - F3: pin line 16 for the qualifying surviving spouse and the
      separate-with-income cases.
    - F4: both blindness questions and titles add the instructions'
      alternative, a statement that the condition is not likely to improve
      beyond those limits. Blindness at a 2025 death stays parked.

## Track 0 adversarial closure

Evidence: `age-blindness-asked-evidence/track0-closure.md` and the
`track0-*.json` files that `track0.py` writes. Every case is a
`live_coordinate_run` on published v87 and scratch v88. Scratch v88
carries Decisions 1-4 and Decision 9 on the final v87, including
vocabulary bundle v4 and the separate-return condition fact.

- Authority-lifecycle table: PASS. `track0-authority.json` has 20 of 20
  cases. Each fact names who is asked, what answers it, which rule reads
  the answer, and what replaces it. Anchors: `alc_taxpayer_age_jan1`,
  `alc_taxpayer_died_before`, `alc_spouse_died_on_day`,
  `alc_spouse_separate_qualifies` (condition yes, 17,350 on both cores),
  `alc_spouse_separate_has_income` (spouse age stays yes, condition no,
  v88 line 12e 15,750, v87 17,350), `alc_qss_ignores_recorded_spouse`
  (v87 line 12e 33,100, v88 31,500), and `alc_separate_unanswered` (asks
  the condition; `alc_joint_unanswered` does not).
- Empty/nonempty authority matrix: PASS. `track0-matrix.json` has 35 of
  35 cases. Single, joint, separate with a qualifying spouse, separate
  with a spouse who has income, head of household, qualifying surviving
  spouse, and a dependent filer; each unanswered, false, true, and born
  January 1, 1961; plus the 2025 death readings.
  `m_separate_has_income_true` is v88 line 12e 18,950 and v87 22,150.
  `m_qss_spouse_age_recorded` is the qualifying-surviving-spouse number
  change.
- Late-member lifecycle: PASS. `track0-late.json` has 3 of 3 traces.
  `late_joint_to_separate` is 33,100 on both cores, then v88 blocked on
  the condition question while v87 publishes 17,350, then v88 15,750 and
  v87 17,350. The spouse-age yes is not replaced.
  `late_joint_to_hoh` is 33,100, then 23,625. `late_answer_replaced` is
  17,750, then 15,750. `supersession_act` is false on each trace.
- Neighboring capability dependency diff: PASS. `track0-neighbour.json`
  has 778 lists: 775 recorded and 3 derived from
  `v83/track0/s0/b4_amount_no_answer`. All 778 are identical. 84 lists
  refuse the same way on both cores. The derived separate return answers
  the condition false. The derived ids are
  `derived-joint/v83/track0/s0/b4_amount_no_answer`,
  `derived-separate/v83/track0/s0/b4_amount_no_answer`, and
  `derived-dependent/v83/track0/s0/b4_amount_no_answer`.
- Reused-claim semantic/lifecycle equivalence: PASS. `track0-reuse.json`
  has 12 of 12 checks. Eight members differ: five questions added, the
  two rule successors, and vocabulary v3 to v4. The four bindings move
  from `optional_default` to `required`, and
  `spouse_separate_condition` is added `required`. Spouse titles are
  unchanged. The other two readers are byte-identical. Live cases:
  `reuse_single_false`, `reuse_joint_spouse_age`,
  `reuse_dependent_age`, `reuse_qss_spouse_recorded` (v87 33,100, v88
  31,500), and `reuse_separate_condition_no` (v88 15,750, v87 17,350).
- Integration surface: PASS. `track0-surface.json` has 7 of 7. Each
  question's exact sentence appears on a page where it is asked. Every
  newly blocked field names one of those questions. `surface_separate`
  asks the condition question and newly blocks 20 of its 22 blocked
  fields. The other two are already blocked on v87.
  `surface_age_answered_blind_open` asks only `taxpayer-blind`, blocks
  line 12e, and publishes line 13b at 6,000.
- Known limitations affecting correctness: owner disposition required
  for blindness at a 2025 death. Decision 9 retires the stale spouse-age
  yes. `late_joint_to_separate` reaches 15,750 on v88 with that yes still
  recorded and the condition answered no.
  - Blindness for someone who died in 2025 is parked by Decision 7. No
    hand value is claimed. It is outside the stated-law class.
  - The late traces replace an assertion in the act list.
    `supersession_act` is false.
  - Line 12d's boxes are still absent as form fields (P0 finding 6,
    carried).
  - `form1040.line-6d` and `form1040.line-6d-not-checked` are blocked on
    a separate return on v87 and name no question (`surface_separate`).

**Disposition.** Foreman, 2026-11-12, under the owner's standing grant to
apply recommended choices. Blindness at a 2025 death stays parked
(Decision 7): neither the instructions nor Publication 501 says how it is
judged, so no hand value can be claimed. The other items change no number.
Track 0 is accepted and Track 1 is chartered
(`docs/reviews/age-blindness-asked/charter-track1.md`).

## Track 1 result

Charter: `docs/reviews/age-blindness-asked/charter-track1.md`. Builder,
2026-11-12.

- **Condition question.** Decision 10's sentence, verbatim: "Is it true
  that your spouse had no income, isn't filing a return, and can't be
  claimed as a dependent on another person's return?"
- **Successors.** Eight members are in `packages/content/tax/2025/`,
  generated from `prototype.py` and byte-identical to it: the four age
  and blindness questions, the condition question, dependents worksheet
  line 1 v2, Schedule 1-A line 36b v2, and vocabulary bundle v4. The
  condition fact type lives in that bundle. No published citizen was
  edited.
- **Core v88, registry v86, release v86** were made with
  `python3 -m tools.package_successor`. Registry v86 only adds the eight
  citizens and core v88. `packages/tax/loader.py` gives v88 v87's
  companion declaration and covered-flag refusal map.
  `tests/test_noncovered_sales_v78_switch.py` names v88 among the cores
  with that map.
- **Taxpayer facts.** `state_taxpayer_facts` records the taxpayer's age
  and blindness as false on core v88 when a list leaves them unstated.
  Earlier cores, and a caller that omits the core, stay unchanged. The
  helper leaves the spouse facts and the separate-return condition
  unstated.
- **Live module** (`tests/test_age_blindness_v88.py`). The 20 authority
  cases, 35 matrix cases and 3 late traces (7 steps) reduce to 38
  distinct act lists. Each runs once on published core v88 through
  `live_coordinate_run` and the presentation model, and every spec that
  shares the list is judged on that run. Hand values come from
  `law.json` and `track0.py`, and each asked question is pinned to its
  sentence. All 38 were judged clean. The check printed
  `ABA_V88_CASES runs=38 wall_s=227.8 failed=0`.
- **775 recorded runs.** Answered false as the record implies, against
  the fixture files in place, on 4 workers. The check printed
  `ABA_V88_RECORDED runs=775 wall_s=1333.4 workers=4 diffs=0 of=775
  v81_earlier=104`. The v83 pins match their fixture. On v82, v84 and
  v85 every number both sides publish matches, and a watched
  standard-deduction number the fixture publishes is still a number.
  No run asks an age, blindness, or condition sentence.
- **Package test** (`tests/test_age_blindness_v88_package.py`, fast):
  byte identity with the prototype, the eight member edits, registry
  v86 add-only, release v86, the v88 loader entries, and v87 and
  earlier unchanged.
- **Checks.** `pytest` on `tests/test_age_blindness_v88.py`,
  `tests/test_age_blindness_v88_package.py` and
  `tests/test_noncovered_sales_v78_switch.py`: 16 passed in 1621.37 s.
  Fast lane (`pytest -m "not live"`): 1810 passed, 8 skipped, 4256
  subtests passed in 17.88 s. `python3 -m mypy`: no issues in 486
  source files. `python3 tools/envelope_scan.py --range
  github/main..HEAD`: clean.
- **Deviation.** 104 uncorrected v81 lists block or refuse where the
  v81 fixture published a number, because questions added after v81 are
  unanswered. That is already how published v87 treats those lists.
  `v81/case/a_bw` and `v81/case/m_q3_yes_nothing_beside_w` were
  rechecked identical to published v87. No number both sides publish
  differs. No kernel, derivation, or schema edit, and no recording
  change.

**Review repair** (charter `docs/reviews/age-blindness-asked/charter-repair.md`,
Decision 11). This updates the live and recorded counts above.

- **F1.** On a separate return the spouse's age and blindness are asked
  only when the condition is yes. `alc_separate_condition_no_spouse_unanswered`
  answers the condition no and leaves the spouse unanswered: line 12e is
  15,750, line 16 is 3,875, and nothing is asked about the spouse.
  `alc_separate_unanswered` asks the taxpayer's two questions and the
  condition, and does not ask the spouse.
- **F4.** Both blindness questions and both titles add the instructions'
  alternative, quoted from `law.json` `blindness`: "If your eye condition
  isn't likely to improve beyond the conditions listed above, you can get
  a statement certified by your eye doctor (ophthalmologist or
  optometrist) to this effect instead." The spouse sentence uses the same
  words with the spouse as the person. Blindness at a 2025 death stays
  parked.
- **F3.** Line 16 is pinned at 3,875 for a separate return with taxable
  income 34,250, and at 1,853 for a qualifying surviving spouse with
  taxable income 18,500.
- **F2.** The live module replays the 298 v83 lists. The 775-list result
  stays in `age-blindness-asked-evidence/track0-neighbour.json`.
- **Run count.** The check printed `ABA_V88_CASES runs=39 wall_s=236.4
  failed=0` and `ABA_V88_RECORDED runs=298 wall_s=558.2 workers=4
  diffs=0 of=298 v81_earlier=0`. The 39 lists are the previous 38 plus
  the F1 case. All 298 v83 pins match their fixture.
- **Checks.** `pytest` on `tests/test_age_blindness_v88.py` and
  `tests/test_age_blindness_v88_package.py`: 11 passed in 855.22 s.
  Fast lane (`pytest -m "not live"`): 1810 passed, 8 skipped, 4256
  subtests passed in 17.70 s. `python3 -m mypy`: no issues in 486
  source files. `python3 tools/envelope_scan.py --range
  github/main..HEAD`: clean. No kernel, derivation, or schema edit, and
  no recording change. The branch-only v88 citizens were regenerated in
  place.
