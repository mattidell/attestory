# Review: Form 1040 line 12d's four boxes, core v90

Reviewer: fresh reader, author-independent.
Charter: `docs/reviews/line12d-boxes/charter-review.md`.
Object: `milestone/line12d-boxes-2025` at the Track 1 head (commit removed at closeout).
The Orientation Block SHA matches `git rev-parse HEAD` on that tree. It is
diffed against `github/main`. After `git fetch`: 0 behind, 25 ahead. PR #277
is open as a draft and has not merged. This worktree is not spent.
Sources read: the plan (Decisions 1–6 and the Track 0 disposition); Track 0
and its probe; `prototype.py`'s build compared as bytes; the 17 new content
citizens; `packages/tax/loader.py`; both page copies; both new test modules;
`rerun.py` and `rerun-output.json`; `tools/recorded_replay.py`; the shared
taxpayer-fact helper. Governance was not read.

Method: live runs call `live_coordinate_run` on published core v90 /
registry v88 / release v88, through Track 0's `run`, with synthetic
`demo.*` findings. The box matrix does not call
`state_taxpayer_facts`. Recorded-list replays go through
`tools/recorded_replay.py` with parallel workers. The page text is the DOM
headless Chrome dumps for four returns. Scratch stayed outside the repo.
`git status` was clean before this file. I did not run `pytest`.

`verify` on PR #277 (run 43754271093) exits at its first step because the
PR is a draft. `quick` on that run passed. The full suite has not run on
this head.

## Findings, by consequence

### S1. Should-fix: every spouse box's inapplicable sentence names filing status, including when the box is shown

- **Where.** The `guard_inapplicable` explain at line 44 of:
  - `packages/content/tax/2025/form1040.line-12d-spouse-age.form-field.json`
  - `packages/content/tax/2025/form1040.line-12d-spouse-age-not-checked.form-field.json`
  - `packages/content/tax/2025/form1040.line-12d-spouse-blind.form-field.json`
  - `packages/content/tax/2025/form1040.line-12d-spouse-blind-not-checked.form-field.json`

  All four say: "This line 12d box is not checked on this return's filing
  status." The page prints that explain under the value "Not applicable."
  (`packages/presentation/pages/citation-walk.v1.html:1083-1085`).
- **Reproduction.** On a joint return, taxpayer age and blindness no,
  spouse age yes, spouse blindness no, core v90 publishes line 12e as
  33100. The drawn spouse-age section says "the box is checked." The
  spouse-age not-checked section, on the same page, says "Not applicable.
  This line 12d box is not checked on this return's filing status." The
  spouse-blind checked section uses that same filing-status sentence while
  the spouse-blind not-checked section correctly says "the box is not
  checked." The You twins on that page say "This line 12d box is the other
  checked/not-checked state." (`form1040.line-12d-you-age.form-field.json:44`).
  On married filing separately with the spouse condition no, and with
  spouse answers still yes, both spouse sections are "Not applicable" and
  both use the filing-status sentence. The value is fair. The sentence
  names filing status; a separate return checks these boxes when the
  condition is yes.
- **Consequence.** The check state is right. The words beside an applicable
  spouse box are not true of that return (presentation). One explain is
  used both when the box is hidden and when the section is only the other
  state of a box the return does show.
- **Fix.** Use the You-field sentence only when the section is the other
  checked/not-checked state. Use a status-or-condition sentence only when
  the box is not shown: filing status for single, head of household, and
  qualifying surviving spouse; the separate-return condition for a
  separate return whose condition is no. One `guard_inapplicable` explain
  cannot be true in both situations, so the hidden case needs its own
  disposition, or a single sentence that is true in both (and then the
  status-or-condition reason has to live somewhere that fires only when
  the box is hidden).

### S2. Should-fix: Track 1 never runs an unanswered taxpayer age or blindness

- **Where.**
  - `tests/test_line12d_boxes_v90.py:152-155` calls
    `state_taxpayer_facts(..., core="v88")` and then
    `setdefault`s taxpayer age and blindness to false before
    `expected_boxes`.
  - `tests/helpers/current_core_returns.py:279-304` records those two
    facts as false when the list leaves them unstated. It does not state
    spouse facts or the separate-return condition.
  - `tests/test_line12d_boxes_v90.py:354` requires `you_held`, which is
    true only when both taxpayer boxes are `checked` or `not_checked`
    (`tests/test_line12d_boxes_v90.py:168`).
- **Reproduction.** A single return built with no age or blindness fact
  has neither fact. After `state_taxpayer_facts(..., core="v88")` both
  are false. The 39 Track 1 rows collapse to 31 distinct act lists once
  synthetic ids are ignored. These names share one list:
  `auth_you_unanswered`, `m_single_false`, `m_single_unanswered`. The
  same collapse pairs head of household, qualifying surviving spouse, and
  the dependent single "unanswered" rows with their false-answer rows.
  Spouse-unanswered on a joint return stays distinct, because the helper
  does not fill spouse facts. A rule that published `not_checked` for an
  absent taxpayer age would still pass Track 1.
- **What the product does.** The same unanswered single return, run
  without the helper, blocks both You boxes and line 12e with
  `DEPENDENCY_ABSENT`. The drawn page says "No value published — cannot
  compute" and asks "Were you born before January 2, 1961?" and the
  blindness question. It does not draw "not checked" for either box.
- **Consequence.** The measured behavior holds the charter invariant. The
  committed test does not observe it (evidence).
- **Fix.** Add one live case that does not call the helper and does not
  `setdefault` the taxpayer facts false. Expect both You boxes and line
  12e blocked, and assert the drawn section text is the blocked copy.

### N1. Note: six Track 1 names add no run

`test_authority_matrix_and_late_on_published_v90` dedupes by act-list
digest and runs 31 lists for 39 names
(`tests/test_line12d_boxes_v90.py:346-367`). These groups are the same
run after synthetic ids are ignored:

- `auth_you_age_yes`, `late_answer_replaced_0`
- `auth_you_unanswered`, `m_single_false`, `m_single_unanswered`
- `auth_spouse_age_joint`, `late_joint_to_separate_0`, `late_joint_to_hoh_0`
- `m_hoh_false`, `m_hoh_unanswered`
- `m_qss_false`, `m_qss_unanswered`
- `m_dependent_false`, `m_dependent_unanswered`

The late steps that share the joint starting list still have their own
later steps (`late_joint_to_separate_1` is a distinct run). The
unanswered names in the last four groups are the S2 gap: the shared run
is the false-answer run.

`test_instructions_quote_the_chart` (`tests/test_line12d_boxes_v90.py:319`)
does not call the coordinator. It checks the quoted chart against Track
0's table. A wrong published rule would leave it green, which matches
its docstring.

### N2. Note: the recorded-list class cannot hide a changed number, reason, or question

`rerun.py` `pin_new_only` (`rerun.py:142-150`) accepts class `identical`,
or class `numbers_changed` with empty sentence fields, no errors, empty
line diffs, and every number-field name starting with
`rows.rule.form1040-line12d-`. `final_class` (`rerun.py:153-161`) also
requires no changed existing page section and added sections only under
`form1040.line-12d-`. A changed line fills `lines` and fails
`pin_new_only`. A changed question, reason, or blocked reason is a
sentence field (`tools/recorded_replay.py:33`, `classify` at
`tools/recorded_replay.py:282-296`) and fails it. Truncation to 40
number fields and 30 lines still leaves those lists non-empty, so a
diff past the cap still fails the class.

The committed report (`rerun-output.json`) is complete: 775 lists, 8
workers, 1550 live runs, 84 `identical`, 691
`numbers_identical_new_fields_only`, `changes` empty, outcomes
`error/error` 84 and `success/success` 691, line 34 equal on all 775.

I replayed ten lists on v89 and v90 (4 workers, 20 coordinate runs).
Every pin class was `identical`: questions, reasons, blocked reasons,
base, and attachments equal, line diffs empty, row deltas empty. Three
of them (`v81/case/a_corrected_basis_missing`,
`v82/p0_d1_codeb_negative_proceeds/honest`,
`v83/returns/case/a_corrected_basis_missing/recorded`) error on both
cores with equal pins; the classifier stores that shared error under
the baseline name. The other seven are the report's
`numbers_identical_new_fields_only` class, and the pin itself is
identical: the new fields are presentation sections, not pin rows.

A page-section diff of six of those lists (4 workers, 12 coordinate
runs), using `rerun.per_list`, agrees. The error list adds no section.
Each success list adds exactly the eight `form1040.line-12d-*` sections,
changes no existing section, and keeps line 34 equal (794 on
`v83/track0/s0/b4_beside_int_div`, 625 on `v85/matrix/m_nosale_no`,
blocked on the others). Because `page_changed` is empty, line 12e has
the same disposition and value on both cores wherever that section
exists. The pin's line set does not carry `form1040.line-12e`; the page
comparison is the one that sees it.

`test_v83_recorded_lists_keep_their_numbers` drops lines whose names
contain `form1040.line-12d` or `form1040-line12d-` and ignores `rows`
(`tests/test_line12d_boxes_v90.py:268-278`). It keeps
`form1040.line-12e`. Fixture rows are `[disposition, code, dependency
names]` (for example `tests/fixtures/f1099b_backup_withholding_v83/expected.json:116-122`).
Dropping `rows` cannot hide a dollar amount in that shape. It can hide
a dependency-name or reason-code change, which `classify` would still
see unless the row key starts with the line 12d prefix. The ten-list
sample had no row delta.

## Answers to the charter

1. **Each box is true.** Ninety live v90 runs, without the helper, match
   an independent reading of the instructions: a You box is blocked when
   that fact is absent, checked when the answer is yes, and not checked
   when the answer is no; a spouse box is hidden on single, head of
   household, qualifying surviving spouse, and a dependent single return;
   on a separate return it is blocked when the condition is unanswered,
   hidden when the condition is no, and driven by the spouse fact when
   the condition is yes; on a joint return the spouse fact drives it.
   Line 12e is blocked when any shown box is blocked, and otherwise the
   chart amount (dependent single uses the 15750 base plus 2000 per
   checked box). The matrix crosses every status with taxpayer age and
   blindness each yes, no, and unanswered, including one answered and
   one not; spouse age and blindness each yes, no, and unanswered on
   joint and on separate-with-condition-yes; a stale spouse yes on
   single, head of household, qualifying surviving spouse, and separate
   with the condition no or unanswered. Failures: none. No unstated
   fact was published as checked or not checked.

   Drawn pages, same coordinator:

   | Return | You age / blind | Spouse age / blind | Line 12e |
   | --- | --- | --- | --- |
   | Single, both taxpayer facts absent | blocked / blocked | hidden / hidden | blocked |
   | Single, both taxpayer answers no, spouse answers still yes | not checked / not checked | hidden / hidden | 15750 |
   | Joint, taxpayer no/no, spouse age yes, spouse blindness no | not checked / not checked | checked / not checked | 33100 |
   | Separate, condition no, spouse answers still yes | not checked / not checked | hidden / hidden | 15750 |

   The unanswered You sections say the value is missing and repeat the
   question. They do not say "not checked." S2 is why Track 1 does not
   show this.

2. **Hidden spouse boxes.** On single, head of household, qualifying
   surviving spouse, and separate with the condition no, each spouse
   section's value is "Not applicable." That value is one a filer can
   read as true: the instructions check a spouse box on a joint return,
   or on a separate return only when the condition is yes. The explain
   under it is S1. On a separate return with the condition unanswered,
   both spouse boxes and line 12e are blocked. Publishing "Not
   applicable" there would pick the no-box deduction (15750) without
   the answer; the blocked state leaves the question open.

   After joint is changed to separate, a stale spouse answer does not
   draw a box. One return, taxpayer age and blindness no, spouse age
   yes, spouse blindness no, then `say` to married filing separately:

   | Step | Spouse age / blind | Line 12e |
   | --- | --- | --- |
   | Joint | checked / not checked | 33100 |
   | Separate, condition unanswered | blocked / blocked | blocked |
   | Condition yes | checked / not checked | 17350 |
   | Condition no | hidden / hidden | 15750 |

   The same joint facts, then `say` to head of household: both spouse
   boxes hidden, line 12e 23625.

3. **Numbers untouched.** On the committed 775-list report, no class is
   a changed number, reason, or question, and line 34 is equal on every
   list. N2 is why `numbers_identical_new_fields_only` cannot hide one:
   the classifier rejects a line diff, a sentence diff, or a changed
   existing page section, and the ten-list pin diff plus the six-list
   page diff agree with the report. The v83 row exclusion cannot hide
   a dollar amount in the fixture's row shape. I did not re-run all
   775 lists.

4. **The page.** The only change in either `citation-walk.v1.html` is
   Decision 1. Package copy at
   `packages/presentation/pages/citation-walk.v1.html:1019-1020` and
   harness copy at
   `tools/presentation_harness/examples/pages/citation-walk.v1.html:294-295`
   are the same statement: a frozen null-prototype table maps `checked`
   to "checked" and `not_checked` to "not checked"; any other render
   throws `SectionError("missing-instruction")`. The diff against
   `github/main` is that replacement in each file and nothing else. No
   other page, baseline, golden, snapshot, or `published.json` changes.
   `git diff github/main -- packages/kernel packages/schemas` is empty.

   A lookup of `__proto__`, `constructor`, `not_elected`, `toString`,
   `valueOf`, `hasOwnProperty`, `__defineGetter__`, or `prototype` on
   that table is undefined, so the page throws rather than drawing.
   The table's own keys are only `checked` and `not_checked`. Setting
   `checked` on `Object.prototype` does not override the frozen
   null-prototype table.

5. **Immutability.** Registry v88 against v87: nothing removed or
   changed; added citizens are the 17 line 12d members, each checksum
   matching its file, plus `tax.us.2025.package.core-calculations` v90.
   Release v88 matches release v87 on every other field, and its
   registry sha matches the v88 registry. Core v90 against v89: schema
   `artifact-package.v43` on both, kept fields equal, checksums match,
   members 1005 to 1022, added exactly those 17 ids, none removed or
   changed. Each new citizen is byte-identical to `prototype.py`'s
   build. The loader diff is the v90 covered-flag map (the same object
   map v89 uses) and the v90 companion declaration (v89's pairs and
   domains). `selection_collect_satisfied_by_family` is rank at least
   86 (`packages/tax/loader.py:107-123`), so v90 is included with no
   new dict entry. The kernel diff and the published-schema diff are
   empty.

6. **CI cost and isolation.** The live module's authority test runs 31
   distinct lists (N1). The names that would have been the unanswered
   taxpayer case are the false-answer run, so that test would pass if
   an absent taxpayer age published `not_checked` (S2). The chart test
   never calls the coordinator (N1). The v83 test checks numbers
   against the fixture, including line 12e, and ignores box text and
   rows (N2). Evidence modules load only through
   `tests/evidence_loader.py`: `line12d-boxes-evidence/track0.py`,
   `line12d-boxes-evidence/prototype.py`, and
   `question-wording-evidence/track0.py`. The tests read JSON with
   `Path.read_text`.

7. **Data safety.** `python3 tools/envelope_scan.py --range github/main..HEAD`
   exits 0. This review names no machine path and no temp directory.
   Every live id is synthetic `demo.*`.

## Verified and reusable

- The product uses the recorded boolean facts. The questions already
  ask "born before January 2, 1961" and the blindness question. A 2025
  death before age 65 stays parked, as the plan says.
- Blocked You sections repeat that input question under "Why:". That is
  the existing blocked-line pattern on this page.
- On the 691 successful recorded lists the report's boxes are You
  not checked and spouse hidden, which is what the helper produces:
  taxpayer age and blindness false, spouse facts unstated.
- Both cores still raise the line 6c categorical alert on those
  successful lists. The page class compares disposition and value, so
  the new drawn word for `not_checked` is outside that comparison.
  Decision 1 is what draws it.

## Verdict

**Ready.** No blocking defect.

S1 and S2 should be repaired or dispositioned before closeout. N1 and
N2 are recorded only. Marking PR #277 ready is what runs `verify`; this
review did not run the suite.
