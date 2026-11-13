# Track 0 adversarial closure: age and blindness are asked

Evidence for `docs/phases/engine-breadth/milestones/age-blindness-asked.md`.
Charter: `docs/reviews/age-blindness-asked/charter-track0.md`.
Gate: `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate".

Every case is a `live_coordinate_run`. Published v87 is the live core
(registry v85, release v85). Scratch v88 (registry v86, release v86) is
built outside the repository by `prototype.py`. Wage-return v88 runs
re-adopt `exception1.bundle.v2.json`, `sli-scope.bundle.v2.json` and
`core_calculations.bundle.v4.json`. Hand values come from the 2025
instructions (`law.json`): wages 50,000, the chart's base plus 2,000 or
1,600 a box, and the senior deduction of 6,000 under the phaseout. A
question is answered as a truthful filer reads its words. Amendment
(Decision 9): the sections below are the rerun after the separate-return
condition became its own fact.

## Item 0: the prototype matches Decisions 1-4 and Decision 9

`prototype-build.json` lists the eight members on the final question-wording
v87:

- four input questions, v1, with the P0 sentences (Decision 5), including
  the day-before-the-birthday rule and a death in 2025. The spouse age and
  blindness questions state only age and blindness
- `input-question.standard-deduction.spouse-separate-condition` v1. No
  published fact states the condition, so this fact is new. Its question
  is "Answer yes if your spouse had no income, isn't filing a return, and
  can't be claimed as a dependent on another person's return."
- `rule.dependents-worksheet-line-1` v2, which counts the spouse's boxes on
  a separate return only when that fact is yes
- `rule.schedule1a-part-v-line-36b` v2
- `core_calculations.vocabulary` v4, built on v3. The two spouse titles are
  the v3 titles. `parameter.default-false` stays (Decision 4)

The four age and blindness bindings, and the new condition binding, are
`required`. `inherited_inconsistencies` is empty. The wage-return tables
re-adopt vocabulary bundle v4, and an assertion of the condition fact is
valid only after that adoption. Published v87 does not receive the
assertion. Recorded lists that are not separate returns keep the bundle
adoptions they were recorded with.

`probe-output.json` was rerun on this core. Truthful runs match the chart
on v86, v87, and v88. `separate-spouse-qualifies` truthful is line 12e
17,350 on all three, with the condition answered yes on v88 only.
Unanswered v88 on a separate return asks the condition question along with
the four age and blindness questions. Joint, single, head of household,
and qualifying surviving spouse do not ask it. Qualifying surviving spouse
with the spouse's age recorded is line 12e 33,100 on v86 and v87 and
31,500 on v88.

`rerun-output.json` reruns the 775 recorded lists on published v86 and scratch v88, as recorded and answered false the way the record implies. 691 lists compute on v86. All 691 of those are newly asked the taxpayer's two questions on v88, and none states either fact. 690 answered runs are identical to v86. The remaining one, `v82/m_empty_exc1_unanswered/honest`, changes only a sentence against v86 and is identical to published v87. 84 lists are refused the same way on v86, on v88 as recorded, and on v88 answered. Every computing list is a single filer.

## Item 1: authority-lifecycle table

`track0-authority.json`: 20 cases, 20 pass on published v87 and scratch v88.

| Fact | Meaning | Who is asked | What answers it | Rule that reads it | What replaces it |
| --- | --- | --- | --- | --- | --- |
| `taxpayer-over-65` | Born before January 2, 1961. Age 65 is reached the day before the 65th birthday. A 2025 death counts only if the filer was already 65. | Every return, including a filer who can be claimed | Yes or no to `input-question.taxpayer-over-65` | `dependents-worksheet-line-1` v2 and `schedule1a-part-v-line-36a` v1 | A later answer (`late_answer_replaced`). Absent, the binding blocks rather than defaulting: `alc_taxpayer_age_unanswered`. |
| `taxpayer-blind` | On December 31, 2025, totally blind, or 20/200, or a 20-degree field, as an eye doctor's certified statement says | Every return | Yes or no to `input-question.taxpayer-blind` | `dependents-worksheet-line-1` v2. The senior deduction does not read it. | A later answer. Blindness for someone who died in 2025 is not stated (Decision 7). |
| `spouse-over-65` | The same birthday and 2025-death test. The answer is age only. | A joint or separate return. Not single, head of household, qualifying surviving spouse, or a dependent filer. | Yes or no to `input-question.spouse-over-65`. The v4 title is the v3 age title. | `dependents-worksheet-line-1` v2 on a joint return, and on a separate return only when the condition fact is yes. `schedule1a-part-v-line-36b` v2 on a joint return only | A later answer. A filing-status change does not by itself replace it (`late_joint_to_separate`). |
| `spouse-blind` | The December 31, 2025 blindness test. The answer is blindness only. | A joint or separate return | Yes or no to `input-question.spouse-blind`. The v4 title is the v3 blindness title. | `dependents-worksheet-line-1` v2 on a joint return, and on a separate return only when the condition fact is yes. Line 36b does not read blindness. | A later answer. The same parked death question as the taxpayer's blindness. |
| `standard-deduction.spouse-separate-condition` | The spouse had no income, isn't filing a return, and can't be claimed as a dependent on another person's return. | A separate return only | Yes or no to `input-question.standard-deduction.spouse-separate-condition` | `dependents-worksheet-line-1` v2, and only on a separate return. A yes lets the spouse's two boxes count. | A later answer. While it is unanswered on a separate return, line 12e blocks (`alc_separate_unanswered`, `late_joint_to_separate`). |

Measured anchors, both cores unless noted:

- Single, born January 1, 1961, not blind (`alc_taxpayer_age_jan1`): line 12e 17,750, senior 6,000, line 15 26,250, line 16 2,915. Born January 2 (`alc_taxpayer_age_jan2`): 15,750 and senior 0.
- Died December 30, 2025, the day before that January 1 birthday reaches 65 (`alc_taxpayer_died_before`): truthful no, 15,750. Died December 31 (`alc_taxpayer_died_on_day`): truthful yes, 17,750.
- Blind only (`alc_taxpayer_blind_yes`): 17,750 and senior 0.
- Joint, spouse age yes (`alc_spouse_age_joint_yes`): 33,100 and spouse senior 6,000. Spouse born January 2 (`alc_spouse_age_joint_no`): 31,500. Spouse died February 12, 2025 (`alc_spouse_died_before`): truthful no, 31,500. Died February 13 (`alc_spouse_died_on_day`): truthful yes, 33,100. Spouse blind only (`alc_spouse_blind_joint_yes`): 33,100 and senior 0.
- Separate, spouse qualifies (`alc_spouse_separate_qualifies`): condition yes, 17,350 and line 36b 0 on both cores. Spouse has income (`alc_spouse_separate_has_income`): spouse age stays yes, the condition is no, v88 line 12e is 15,750 and v87 is 17,350.
- Head of household and qualifying surviving spouse unanswered (`alc_spouse_not_on_hoh`, `alc_spouse_not_on_qss`): v88 asks only the taxpayer's two questions. v87 publishes the silent default (23,625 and 31,500).
- Qualifying surviving spouse with spouse age recorded true (`alc_qss_ignores_recorded_spouse`): v87 line 12e 33,100, v88 31,500. That is the one intended number change (Decision 2).
- Dependent filer unanswered (`alc_dependent_unanswered`) asks the taxpayer's two questions. Age yes (`alc_dependent_age_yes`): worksheet line 12e 17,750 and senior 6,000.
- Joint unanswered (`alc_joint_unanswered`) asks all four and blocks on all four symbols. It does not ask the condition. Separate unanswered (`alc_separate_unanswered`) asks the four and the condition; line 36b publishes 0 because the return is not joint.

## Item 2: empty/nonempty matrix

`track0-matrix.json`: 35 cases, 35 pass on published v87 and scratch v88.

Each population is single, joint, separate with a spouse who qualifies, separate with a spouse who has income, head of household, qualifying surviving spouse, and a filer who can be claimed. Each is unanswered, answered false (born January 2, 1961, not blind), answered true, and born January 1, 1961. The 2025 death cases are their own ids even when the truthful answers match a January 1 or January 2 case.

| Population | Unanswered on v88 | False (January 2) | True, as the question allows | Born January 1, 1961 |
| --- | --- | --- | --- | --- |
| Single | asks the taxpayer's two; v87 15,750 | 15,750 | 19,750 and senior 6,000 | 17,750 and senior 6,000 |
| Joint | asks all four; v87 31,500 | 31,500 | 37,900 and senior 12,000 | 33,100 and taxpayer senior 6,000 |
| Separate, spouse qualifies | asks the four and the condition; v87 15,750 | 15,750 | 22,150 and senior 0, both cores | 17,350 and senior 0 |
| Separate, spouse has income | asks the four and the condition; v87 15,750 | 15,750 | v88 18,950 (taxpayer's two boxes; condition no), v87 22,150 | 17,350 and senior 0 (spouse age is no) |
| Head of household | asks the taxpayer's two; v87 23,625 | 23,625 | 27,625 and senior 6,000 | 25,625 and senior 6,000 |
| Qualifying surviving spouse | asks the taxpayer's two; v87 31,500 | 31,500 | 34,700 and senior 6,000 | 33,100 and senior 6,000 |
| Dependent filer | asks the taxpayer's two; v87 15,750 | 15,750 | 19,750 and senior 6,000 | 17,750 and senior 6,000 |

Death readings, both cores: taxpayer born January 1, 1961 and died December 30 (`m_taxpayer_died_before_jan1_birthday`, and the joint twin `m_taxpayer_died_before_on_joint`) is a no. The same person died December 31 (`m_taxpayer_died_on_jan1_birthday`, `m_taxpayer_died_on_day_on_joint`) is a yes. Spouse born February 14, 1960 and died February 12 (`m_spouse_died_before`) is a no, 31,500. Died February 13 (`m_spouse_died_on_day`) is a yes, 33,100.

`m_qss_spouse_age_recorded` records the spouse's age on a qualifying surviving spouse return. v87 line 12e is 33,100. v88 is 31,500.

## Item 3: late-member lifecycle

`track0-late.json`: 3 traces, 3 pass. `say` replaces the earlier assertion in the act list. No supersession act is recorded (`supersession_act` false).

| Trace | Steps | Line 12e |
| --- | --- | --- |
| `late_joint_to_separate` | Spouse age yes on a joint return, then the status becomes separate with the condition unanswered, then the condition is answered no. The spouse-age yes is not replaced | 33,100 on both, then v88 blocked and v87 17,350, then v88 15,750 and v87 17,350 |
| `late_joint_to_hoh` | The same joint yes, then the status becomes head of household | 33,100, then 23,625 |
| `late_answer_replaced` | Single, age yes, then that answer replaced with no | 17,750, then 15,750 |

`late_joint_to_separate` leaves the spouse-age yes in the act list (`spouse_age_still_yes` true on every step). After the status becomes separate, v88 asks only `standard-deduction.spouse-separate-condition` and blocks line 12e. Answering that question no, because the spouse has income, is the truthful reading. v88 line 12e is then 15,750. Published v87 has no condition fact, so that step runs without the assertion and still publishes 17,350. Head of household does not read the spouse fact, so the recorded yes no longer changes line 12e.

## Item 4: claim reuse

`track0-reuse.json`: the published v87 package against scratch v88. All twelve checks pass.

Eight members differ and no others. The five input questions are added at v1. `dependents-worksheet-line-1` and `schedule1a-part-v-line-36b` move from v1 to v2 and their bodies differ. `core_calculations.vocabulary` moves from v3 to v4. The four age and blindness bindings change from `optional_default` to `required`, and the condition binding is added as `required`. Spouse titles are unchanged. The new fact is the only fact-type identity added.

Four computations mention the age and blindness facts. `form1040-standard-deduction` v3 and `schedule1a-part-v-line-36a` v1 are byte-identical. The two successors are the ones that differ.

Live composition:

- `reuse_single_false`: 15,750
- `reuse_joint_spouse_age`: 33,100
- `reuse_dependent_age`: 17,750
- `reuse_qss_spouse_recorded`: v87 line 12e 33,100, v88 31,500
- `reuse_separate_condition_no`: spouse age stays yes, the condition is no, v88 line 12e 15,750, v87 17,350

## Item 5: neighbour dependency diff

`track0-neighbour.json` compares published v87 with scratch v88. It covers the 775 recorded lists plus three derived returns, each answered false for the facts v88 asks and the record leaves unstated. 778 lists are identical. The change list is empty. 84 lists refuse the same way on both cores.

The derived returns start from `v83/track0/s0/b4_amount_no_answer`, and each is class `identical`:

- `derived-joint/v83/track0/s0/b4_amount_no_answer`
- `derived-separate/v83/track0/s0/b4_amount_no_answer`
- `derived-dependent/v83/track0/s0/b4_amount_no_answer`

Spouse facts on these returns are answered false, and the derived separate return answers the condition false, so this diff does not carry the qualifying surviving spouse number change or the separate-return condition change. Those changes are `alc_qss_ignores_recorded_spouse`, `reuse_qss_spouse_recorded`, `alc_spouse_separate_has_income`, and `reuse_separate_condition_no`. No neighbouring capability gains a prerequisite.

## Item 6: integration surface

`track0-surface.json`: 7 cases, 7 pass. Each question's exact sentence, from `prototype-build.json`, is shown on a blocked field of a page where that question is asked. Every newly blocked field (present on v88, absent on v87) carries one of the questions that case asks.

- `surface_single`: newly blocked 20; taxpayer-blind on 19, taxpayer-over-65 on 20
- `surface_joint`: newly blocked 20; spouse-blind on 19, spouse-over-65 on 20, taxpayer-blind on 19, taxpayer-over-65 on 20
- `surface_separate`: newly blocked 20; spouse-blind on 19, spouse-over-65 on 19, taxpayer-blind on 19, taxpayer-over-65 on 20, `standard-deduction.spouse-separate-condition` on 19. Each sentence is the question text, and the spouse questions do not carry the condition
- `surface_hoh`: newly blocked 20; taxpayer-blind on 19, taxpayer-over-65 on 20
- `surface_qss`: newly blocked 20; taxpayer-blind on 19, taxpayer-over-65 on 20
- `surface_dependent`: newly blocked 20; taxpayer-blind on 19, taxpayer-over-65 on 20
- `surface_age_answered_blind_open`: newly blocked 19; taxpayer-blind on 19

With age answered and blindness still open (`surface_age_answered_blind_open`), v88 asks only `taxpayer-blind`. Line 12e is blocked. Line 13b is 6000, so the senior deduction publishes from the age answer while the standard deduction still waits on blindness. Nineteen fields are newly blocked, one fewer than the twenty on a fully unanswered return.

On a separate return (`surface_separate`), published v87 already blocks `form1040.line-6d` and `form1040.line-6d-not-checked`. Scratch v88 blocks those two and 20 more. The 20 are the newly blocked set, and each names a question this case asks. The two earlier fields name no question, and they are outside that set.

## Known limitations

The six tables pass. Decision 9 retires the stale spouse-age yes: `late_joint_to_separate` reaches line 12e 15,750 on v88 with that yes still recorded and the condition answered no. Owner disposition is still required for blindness at a 2025 death, which Decision 7 parks with no hand value.

- **Blindness at a 2025 death is parked by Decision 7.** The 2025 instructions and Publication 501 judge blindness on December 31, 2025, and on the last day of the year. They leave unstated how blindness is judged for a taxpayer or spouse who died in 2025. No case claims a hand value. This sits outside the stated-law class. The age-at-death readings are a different question and they pass: `alc_taxpayer_died_before`, `alc_taxpayer_died_on_day`, `alc_spouse_died_before`, `alc_spouse_died_on_day`, and the matrix twins.
- **`say` records no supersession act.** `late_answer_replaced`, `late_joint_to_separate`, and `late_joint_to_hoh` each have `supersession_act` false. The harness replaces the earlier assertion in the act list.
- **Line 12d's boxes are still absent as form fields.** Carried from P0 finding 6. This track adds no new field inventory for those boxes.
- **Two separate-return fields are blocked with no question.** `surface_separate` blocks `form1040.line-6d` and `form1040.line-6d-not-checked` on published v87 and on scratch v88. They are the two fields outside the newly blocked set. The surface row passes because every newly blocked field names a question.
