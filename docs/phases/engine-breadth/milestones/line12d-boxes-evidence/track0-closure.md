# Track 0 adversarial closure: line 12d's boxes are shown

Evidence for `docs/phases/engine-breadth/milestones/line12d-boxes.md`.
Charter: `docs/reviews/line12d-boxes/charter-track0.md`.
Gate: `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate".

Every case is a `live_coordinate_run` on published v89 and on scratch v90.
Scratch v90 is built outside the repository by `prototype.py` and is
unchanged since P0. Each case is run by `track0.py` and saved in the
`track0-*.json` file named below, by case id. Expected box states and line
12e come from the 2025 instructions (`age-blindness-asked-evidence/law.json`,
quoted in `trace.json`). They are coded in `track0.py` as `expected_boxes`
and `hand_12e` and are never read from the prototype. The base return is the
P0 probe's wage return: wages 50,000, 4,500 withheld, every other question
answered. Nothing under `packages/` was edited.

## Item 0: the page prototype (`track0-page.diff`, `track0-page.json`)

`track0-page.diff` changes only the `published_categorical` branch of
`renderLine` in `packages/presentation/pages/citation-walk.v1.html`:

```diff
-    if (instruction.render !== "checked") throw new SectionError("missing-instruction");
-    container.appendChild(el("p", { class: "line-value", role: "status", "aria-label": field.label + ": checked" }, ["checked"]));
+    // Only a declared render string listed here draws; any other is an error.
+    const shown = Object.freeze({ __proto__: null, checked: "checked", not_checked: "not checked" })[instruction.render];
+    if (typeof shown !== "string") throw new SectionError("missing-instruction");
+    container.appendChild(el("p", { class: "line-value", role: "status", "aria-label": field.label + ": " + shown }, [shown]));
```

The declared `published_value.render` is still the only display source. The
branch never reads `resolved.act.finding.value`
(`track0-page.json` `reads_finding_value: false`), and nothing outside the
branch changed. The map has a null prototype, so a render such as
`constructor` cannot pick up an inherited value. Any render string other
than `checked` or `not_checked`, such as line 6c's `not_elected`, is still
`missing-instruction` (Decision 3). `track0.py page` applies the diff to a
scratch copy of the page, and every drawn page below uses that copy. The
harness example copy
(`tools/presentation_harness/examples/pages/citation-walk.v1.html`) carries
the same branch, which Decision 2 says follows in the Track 1 commit.

## Item 1: authority-lifecycle table (`track0-authority.json`)

`track0-authority.json` has 9 cases, and all 9 pass. Each case passes only
if three things hold. On v90 the four box states equal the instructions. On
v89 no box exists. On both cores line 12e equals the chart, and every v89
section is unchanged on v90.

| Box (fields) | Meaning | Answer that feeds it | Rules that show it | Hidden when | What replaces it |
| --- | --- | --- | --- | --- | --- |
| You, born before January 2, 1961 (`form1040.line-12d-you-age`, `-not-checked`) | Born before January 2, 1961 | `taxpayer-over-65` | `rule.form1040-line12d-you-age`, `-not-checked` | Never. Every status checks it | A later answer (`late_answer_replaced_1`). Unanswered, both fields block (`auth_you_unanswered`) |
| You, blind (`form1040.line-12d-you-blind`, `-not-checked`) | Blind on December 31, 2025 | `taxpayer-blind` | `rule.form1040-line12d-you-blind`, `-not-checked` | Never | A later answer (`late_answer_replaced_2`) |
| Spouse, born before January 2, 1961 (`form1040.line-12d-spouse-age`, `-not-checked`) | The spouse was born before January 2, 1961 | `spouse-over-65`, `filing-status`, `standard-deduction.spouse-separate-condition` | `rule.form1040-line12d-spouse-age`, `-not-checked` | Single, head of household, qualifying surviving spouse, a separate return whose condition is no, and a dependent filer, even with the spouse fact recorded true (`auth_spouse_recorded_on_hoh`, `auth_spouse_recorded_on_qss`, `auth_spouse_separate_no`) | A later answer, a status change (`late_joint_to_hoh_1`) or a condition change (`late_joint_to_separate_2`, `_3`) |
| Spouse, blind (`form1040.line-12d-spouse-blind`, `-not-checked`) | The spouse was blind on December 31, 2025 | `spouse-blind`, `filing-status`, the condition | `rule.form1040-line12d-spouse-blind`, `-not-checked` | As for the spouse age box | As for the spouse age box |

The boxes add no new authority. Each rule restates one fact that core v88
already made required, and the spouse rules also read the facts that decide
whether the instructions check the spouse boxes at all. Measured anchors:
`auth_you_age_yes` 17,750, `auth_spouse_age_joint` 33,100,
`auth_spouse_separate_yes` 17,350, `auth_spouse_separate_no` 15,750,
`auth_spouse_recorded_on_hoh` 23,625 and `auth_spouse_recorded_on_qss`
31,500. In the last two, a recorded spouse fact checks nothing.

## Item 2: empty/nonempty matrix (`track0-matrix.json`)

`track0-matrix.json` has 21 cases, and all 21 pass on both cores. The
statuses are single, joint, separate with the condition yes, separate with
the condition no, head of household, qualifying surviving spouse, and a
dependent filer. Each status runs three ways:

- `true`: every asked fact is true.
- `false`: every asked fact is false.
- `unanswered`: none of the four facts is answered. The condition keeps the
  status's value.

| Status | true: boxes, 12e | false: boxes, 12e | unanswered: boxes, 12e |
| --- | --- | --- | --- |
| single (`m_single_*`) | you checked x2, spouse hidden; 19,750 | you not checked x2, spouse hidden; 15,750 | you blocked, spouse hidden; blocked |
| joint (`m_joint_*`) | all four checked; 37,900 | all four not checked; 31,500 | all four blocked; blocked |
| separate, condition yes (`m_separate_yes_*`) | all four checked; 22,150 | all four not checked; 15,750 | all four blocked; blocked |
| separate, condition no (`m_separate_no_*`) | you checked, spouse hidden; 18,950 | you not checked, spouse hidden; 15,750 | you blocked, spouse hidden; blocked |
| head of household (`m_hoh_*`) | you checked, spouse hidden; 27,625 | you not checked, spouse hidden; 23,625 | you blocked, spouse hidden; blocked |
| qualifying surviving spouse (`m_qss_*`) | you checked, spouse hidden; 34,700 | you not checked, spouse hidden; 31,500 | you blocked, spouse hidden; blocked |
| dependent filer (`m_dependent_*`) | you checked, spouse hidden; 19,750 | you not checked, spouse hidden; 15,750 | you blocked, spouse hidden; blocked |

How each state is decided:

- **Applicable but negative** shows as not checked.
- **Inapplicable** shows the spouse box hidden. That covers the four
  statuses whose instructions leave the spouse boxes unchecked, and the
  dependent filer.
- **Missing authority** shows as blocked, and only for the box that reads
  the missing answer. A separate return whose condition is no keeps its
  spouse boxes hidden even when the spouse facts are unanswered
  (`m_separate_no_unanswered`), because the instructions never check them
  there.
- **Line 12e** equals the chart on v89 and v90 in all 21 cases.

## Item 3: late-member traces (`track0-late.json`)

`track0-late.json` has 3 traces with 9 steps, and all 9 pass on both cores.

- `late_joint_to_separate`:
  - Step 0, joint: the spouse age box is checked, line 12e 33,100.
  - Step 1, the status becomes separate and the condition is unanswered:
    both spouse boxes block, as does line 12e. The earlier checked state is
    not carried over.
  - Step 2, the condition is answered yes: the spouse age box is checked,
    line 12e 17,350.
  - Step 3, the condition is replaced with no: the spouse boxes are hidden,
    line 12e 15,750.
- `late_joint_to_hoh`:
  - Step 0, joint: the spouse age box is checked, line 12e 33,100.
  - Step 1, the status becomes head of household: the spouse boxes are
    hidden even though the spouse facts stay recorded, line 12e 23,625.
- `late_answer_replaced`:
  - Step 0: the age box is checked, line 12e 17,750.
  - Step 1, the age answer is replaced with no: the age box is not checked,
    line 12e 15,750.
  - Step 2, the blindness answer is replaced with yes: the blind box is
    checked, line 12e 17,750.

The publications carry no state of their own. Each run reads the current
answers, so a superseded answer or status changes the box in the same run.

## Item 4: claim reuse and neighbour dependency diff (`track0-reuse.json`)

The check passes on all of the following:

- All 1,005 v89 members appear unchanged in v90. v90 adds 17: the
  citation, eight rules and eight fields.
- No existing content artifact reads any of the eight new symbols
  (`new_symbols_read_by_existing_content: {}`).
- Each new rule reads only `taxpayer_over_65`, `taxpayer_blind`,
  `spouse_over_65`, `spouse_blind`, `filing_status` and
  `spouse_separate_condition`. Since v88 these are the inputs of
  `dependents-worksheet-line-1` v2, which line 12e reads.
- Line 12e is equal on v89 and v90 in 21 of 21 matrix cases, and every v89
  section is unchanged in every case in items 1 to 3.

The neighbours are line 12e, the senior deduction (lines 36a and 36b), line
6d and every other line. Their prerequisites are the same before and after:
no new question and no new required answer. A box blocks only where line
12e already blocks for the same missing answer.

## Item 5: neighbour sample (`track0-neighbour.json`)

**This is a sample. The full 775-list replay was NOT run** (Decision 5). It
is owed before the PR goes ready.

- **Size and time:** 40 lists, 8 evenly spaced in each fixture set (v81,
  v82, v83, v84, v85). That is 80 live runs at 4 workers, with a replay
  wall time of 146.5 s.
- **Answers:** every list is answered as `rerun.py` answers it, with the
  taxpayer's two facts false.
- **Classes:** 36 lists are `numbers_identical_new_fields_only`: the pins
  are equal, every v89 section is unchanged, and v90 adds only the eight
  line 12d sections. 4 lists are `identical` because they error the same
  way on both cores before any page exists: `v81/case/t2_stage1`,
  `v81/v80/carried_covered_flag_no_st`,
  `v81/v80/probe_a_bw_on_w_fixed_path_b_yes` and
  `v82/r_f1_w_adjustment_row_alone/honest`. There are 0 other changes.
- **Per set:** v81 has 5 new-fields-only and 3 identical, v82 has 7 and 1,
  and v83, v84 and v85 have 8 new-fields-only each.
- **Page alerts:** on the unmodified page, v90 alerts on both "you"
  not-checked fields in all 36 lists. On the scratch page the only
  categorical alert left is line 6c, the same as v89.

## Item 6: integration surface, drawn in Chrome (`track0-surface.json`)

The new symbols have these consumers:

| Consumer | Binding | Cardinality it expects | Satisfied? |
| --- | --- | --- | --- |
| Presentation projection | each `form1040.line-12d-*` field's `binds_symbol` | exactly one publisher per symbol | Yes: one rule per symbol. Every path records one disposition (published, guard_inapplicable or blocked); see items 1 to 3 |
| Saved citation-walk page | `renderLine`, with the item 0 diff | a declared render of `checked` or `not_checked` | Yes, drawn below |
| Every other rule | none | none | Yes: no existing reader (item 4) |

**The cases.** Seven v90 returns were run through `live_coordinate_run`.
Each page was rendered by the coordinator's own `_render_page` step twice,
once with the scratch page and once with the unmodified page, then drawn in
headless Chrome 157.0.8103.78 by `observe.mjs`. All 7 pass, with no line
12d alert on the scratch page:

- `s_single_both_false`
- `s_single_age_true`
- `s_joint_spouse_age`
- `s_separate_condition_no`
- `s_separate_lived_with_spouse`
- `s_hoh`
- `s_single_unanswered`

The drawn box states are:

- you not checked, spouse hidden: `s_single_both_false`,
  `s_separate_condition_no`, `s_separate_lived_with_spouse`, `s_hoh`
- you age checked, you blind not checked, spouse hidden:
  `s_single_age_true`
- you not checked, spouse age checked, spouse blind not checked:
  `s_joint_spouse_age`
- you blocked, spouse hidden: `s_single_unanswered`

**The exact drawn text.** Each box is two page sections: the checked field
and the not-checked field.

- **Checked box** (`s_single_age_true`, `line-12d-you-born-before-1961`):
  heading "You were born before January 2, 1961 (Line
  12d-you-born-before-1961)", badge "PUBLISHED CATEGORICAL", value
  "checked", explain "Line 12d You were born before January 2, 1961: the
  box is checked.", and one citation button. Its twin
  `line-12d-you-born-before-1961-not-checked` draws "Not applicable." with
  "This line 12d box is the other checked/not-checked state."
- **Unchecked box** (`s_single_age_true`, `line-12d-you-blind-not-checked`):
  heading "You are blind (not checked) (Line 12d-you-blind-not-checked)",
  badge "PUBLISHED CATEGORICAL", value "not checked", aria-label "You are
  blind (not checked): not checked", explain "Line 12d You are blind: the
  box is not checked.", and one citation button. Its twin `line-12d-you-blind`
  draws "Not applicable." with the same "other state" sentence.
- **Hidden spouse box** (Decision 4; `s_single_age_true`, `s_hoh`): both
  sections draw badge "GUARD INAPPLICABLE", value "Not applicable.", explain
  "This line 12d box is not checked on this return's filing status.", and no
  citation.
- **Blocked box** (`s_single_unanswered`): badge "BLOCKED", "No value
  published — cannot compute.", and the age or blindness question as the
  reason.

**Line 6d and line 6c.**

- **Line 6d's alert clears.** In `s_separate_lived_with_spouse` (lived with
  the spouse, so line 6d publishes `not_checked`), the unmodified page
  alerts on `line-6d-not-checked` and the scratch page draws "not checked".
  In the other cases line 6d is not applicable, or blocked on a separate
  return that does not answer the lived-apart question, so there is no 6d
  alert to clear.
- **Line 6c's `not_elected` alert stays** on every page, unmodified and
  scratch (Decision 3). So does the parked `line-sch1-top` citation alert.

**v89 is unchanged.** `s_single_both_false` on v89, drawn with the
unmodified page and with the scratch page, gives byte-identical section
text (`v89_page_identical_on_scratch_and_unmodified: true`): 77 sections,
with the alerts on line 6c and line-sch1-top only. The v90 pages have 85
sections, the 8 line 12d sections added.

The browser drive took 4.4 s. The pages, models and DOM capture stay in a
scratch directory outside the repository.

## Known limitations affecting correctness

1. **The full 775-list replay is owed** before the PR goes ready (Decision
   5). The P0 partial covers 269 lists and the Track 0 sample covers 40;
   both found no numeric change.
2. **Each box is two sections, and one of them always reads "Not
   applicable."** This is the line 6d pattern: for a checked box, the
   not-checked twin is guard-inapplicable, and the reverse. The headings
   carry field line names such as "Line 12d-you-blind-not-checked". A
   reader sees the right state, but also a "Not applicable." twin per box,
   which could be misread. Changing that is a projection or content
   question, not part of this design.
3. **Unanswered returns repeat the question.** A blocked box carries the
   age or blindness question as its reason, so an unanswered return shows
   that question on four more sections, on top of the roughly 20 lines that
   already repeat it. This is the parked "shared questions repeat" page
   defect, not a new mechanism.
4. **Line 6c's `not_elected` alert remains** (Decision 3, parked).
5. **The harness copy of the page** (`tools/presentation_harness/examples/
   pages/citation-walk.v1.html`) carries the same branch and describes
   itself as a frozen evaluation baseline. Decision 2 says to change it in
   the same commit; Track 1 should confirm that does not break its
   baseline tests.
