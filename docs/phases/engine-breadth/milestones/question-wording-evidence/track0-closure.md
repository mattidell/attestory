# Track 0 adversarial closure: questions say what their rules read

Evidence for `docs/phases/engine-breadth/milestones/question-wording.md`.
Charter: `docs/reviews/question-wording/charter-track0.md`.
Gate: `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate".

Every case is a `live_coordinate_run` on published core v86 and on scratch
core v87 (registry v85, release v85), which `prototype.py` builds outside the
repository. `track0.py` produces every JSON file named below.

A question is answered the way a truthful filer reads its words on each core.
Where the two cores' words lead a truthful filer to different answers, the
case carries one act list per core. Hand values come from the 2025
instructions (`law.json`): wages 50,000, standard deduction 15,750 single or
31,500 joint, and tax from the 2025 Tax Table. On v87 the act log re-adopts
the three bundle successors; the kernel supersedes a fact type when it is
re-adopted.

## Item 0: the prototype matches Decisions 1-4

`prototype-build.json` lists seven replaced members:
- closure mappings `f1099b-covered-w-st-adjustment` and `-lt-adjustment`, v4
- `input-question.exception1-only-box2a-capital-gains` v3
- `input-question.sli-scope-not-claimed-as-dependent` v2
- `exception1.vocabulary` v2, which retitles `exception1.only-box2a-capital-gains`:
  "... and the filer sold no stock, funds or other property in 2025,
  including a sale with no gain or loss ..."
- `sli-scope.vocabulary` v2, which retitles `sli-scope.not-claimed-as-dependent`:
  "neither the filer nor, on a joint return, the filer's spouse is claimed
  ..."
- `core_calculations.vocabulary` v3, with the four age and blindness titles

Repair: this unit added the two fact-title bundle successors to
`prototype.py`. Nothing else in the prototype changed.

## Item 1: authority-lifecycle table

`track0-authority.json`: 16 cases, 16 pass on both cores.

| Fact or claim | Meaning (v87 words) | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| `f1099b.covered-w-st-adjustment.source-closure` (and `-lt-`) | The filer has recorded the wash-sale adjustment of every covered sale with one | One family horizon of the adjustment family | The members recorded at that horizon | A member transition makes a new horizon, and the closure is no longer current: `late_wash_member`. Unanswered, the question is asked: `alc_wash_st_unanswered`, `alc_wash_lt_unanswered`. A false answer leaves the line blocked: `alc_wash_st_no`. A yes computes: `alc_wash_st_yes`, `alc_wash_lt_yes`. |
| `exception1.only-box2a-capital-gains` | No capital gains other than box 2a, and no 2025 sale that must be reported on Form 8949 or Schedule D (sales inside an IRA or 401(k) and losses on personal items do not count) | The return | The filer's answer. It is read only through `schedule-d-required.conclusion`, and only while no sale is recorded | A later answer replaces it in the act list (`late_exc1_sale_after_yes` step 3; no supersession act is exercised). Unanswered, it is asked with or without a sale: `alc_exc1_unanswered`, `alc_exc1_sale_unanswered`. No sale and yes: line 7b checked (`alc_exc1_yes`). A sale and no: line 7b `guard_inapplicable` (`alc_exc1_sale_no`). |
| `sli-scope.not-claimed-as-dependent` | Neither the filer nor, on a joint return, the spouse is claimed | The return | The filer's answer; the page's "no" records yes | A later answer replaces it in the act list (`late_sli_superseded`; no supersession act is exercised). Unanswered, it is asked: `alc_sli_unanswered`. Yes gives 500 (`alc_sli_not_claimed`); no gives the legal 0 (`alc_sli_claimed`). |
| `taxpayer-over-65`, `spouse-over-65` (titles) | Born before January 2, 1961; age 65 is reached the day before the 65th birthday; a 2025 death before 65 is excluded | The return | The filer's boolean; it defaults to false and no question asks for it | A later boolean, or bundle re-adoption for the title. True: `alc_title_age` (17,750; senior 6,000), `alc_title_spouse_age` (joint 33,100; senior 6,000). The spouse who died February 12, 2025 stays false: `alc_title_spouse_died_before_65` (31,500, 0). |
| `taxpayer-blind`, `spouse-blind` (titles) | As of December 31, 2025, totally blind, or 20/200 or a 20-degree field of vision as an eye doctor's certified statement says (review F4) | The return | The filer's boolean, as above | As above. `alc_title_blind` gives 17,750. |

## Item 2: empty/nonempty matrix

`track0-matrix.json`: 14 cases, 14 pass on v87.

| Family state | v86 words, truthful | v87 words, truthful | v87 result (hand) |
| --- | --- | --- | --- |
| No covered sale, adjustment family closed empty (`m_wash_none`) | yes | yes | 1b 0, line 16 3,875 |
| No covered sale, closure unanswered (`m_wash_none_unanswered`) | asked | asked (v87 words) | 1b blocked |
| Covered sales with no adjustment (`m_wash_plain`) | no: blocked (counterexample) | yes | 1a 200, 1b 0, 7a 200, line 16 3,899 |
| One covered wash sale only (`m_wash_one`) | yes | yes | 1b 0, column (g) 200 |
| Both kinds (`m_wash_both`) | no: blocked (counterexample) | yes | 1a 200, 1b 0, column (g) 200, line 16 3,899 |
| Exception 1, no sale (`m_exc1_nosale`) | yes | yes | line 7b checked, line 16 3,875 |
| Exception 1, no sale recorded, only a personal item sold at a loss with no Form 1099-S or 1099-K (`m_exc1_personal_loss`, review F1) | yes | yes | line 7b checked, line 16 3,875 |
| Exception 1, zero-net sale (`m_exc1_zero`) | yes | no | 7a 0, line 7b `guard_inapplicable`, line 16 3,875 on both |
| Exception 1, gain sale (`m_exc1_gain`) | no | no | 7a 200, line 16 3,899 |
| Student loan, single, not claimed / claimed (`m_sli_single_not`, `m_sli_single_claimed`) | no / yes | no / yes | 500 / 0 |
| Joint, neither spouse claimed (`m_sli_joint_neither`) | no | no | 500, line 16 1,803 |
| Joint, the filer claimed (`m_sli_joint_filer_claimed`) | yes | yes | 0, line 16 1,853 |
| Joint, only the spouse claimed (`m_sli_joint_spouse_claimed`) | no: 500 (counterexample) | yes | 0, line 16 1,853 |

The three v86 counterexamples are the defects the milestone fixes; the
v87 words fix each one (`v86_counterexample_fixed`). Every case that uses
the same act list on both cores publishes identical lines and symbols
(`numbers_identical`).

## Item 3: late-member lifecycle

`track0-late.json`: 3 traces, all steps pass on both cores. Review F2: in the
Exception 1 and student-loan traces each later answer replaces the earlier
one in the act list (the harness's `say` strips the earlier assertion); no
supersession act is exercised, so those steps show that a different answer
computes its hand value, not that a superseded finding becomes non-current.

| Trace | Before | Change | After | What became unusable |
| --- | --- | --- | --- | --- |
| `late_wash_member` | Plain covered sale, closure yes: 1b 0, 7a 200 | A covered wash sale (500, 700, 200) is added to its four families with no new closure answer | 1b and 7a blocked; the page asks the wash-sale family's closure question | Every closure on the earlier horizon, and the line 1b, 7a and 16 findings. Closing again at the new horizons gives 1a 200, 1b 0, column (g) 200, line 16 3,899. |
| `late_exc1_sale_after_yes` | No sale, only-box-2a yes: conclusion no, line 7b checked | A gain sale is added and Exception 1 is left at yes | Line 7b `guard_inapplicable`, 7a 200, line 16 3,899 | The line 7b checked finding. See the note below this table on the stale yes. With the answer replaced by no in the act list (step 3), the run publishes conclusion yes and the same numbers. |
| `late_sli_superseded` | Not claimed: 500 | The answer replaced by claimed, then by not claimed, in the act list | 0, then 500 | Not observed: each step carries one answer, so no earlier finding is shown non-current |

**Stale "yes" beside a sale.** After a sale is recorded, only-box-2a "yes"
still publishes conclusion "no". The proposition the gate cares about did
not lose its reader scope. All three readers of the conclusion take the
Schedule D path first when any sale count or covered proceeds is above 0:
- `form1040-line7b` v2
- `form1040-line16` v7
- `selected-preferential-base` v10

Their versions and bytes are identical in both cores (item 4). So the "no
sale" part of the answer is never relied on while a sale exists. Step 2
reaches the hand values, so no number or line depends on the stale value.

## Item 4: claim reuse

`track0-reuse.json`: every check passes.
- **Members:** exactly the seven listed in item 0 differ. Each differs only in
  `question`, `closure_question` or a fact `title`, plus its version.
- **Bundles:** fact-type identities (id, version, schema, keys, value schema,
  supersession) are unchanged.
- **Questions:** every question's fact pin, family, admits symbol and
  admission are unchanged.
- **Package:** input bindings are unchanged.
- **Readers:** the 19 rules that read these answers or their bindings are the
  same version and the same bytes. They include `schedule-d-required.conclusion`,
  `sli-worksheet` v6, `form1040-standard-deduction` v3,
  `dependents-worksheet-line-1`, `schedule1a-part-v-line-36a`/`36b`, the
  closure checks, adjustment subtotals and admissions, and `schedule-d-line1b`
  and `-line8b` v3.

## Item 5: neighbour dependency diff

`track0-neighbour.json` has 775 distinct recorded act lists. Each ran on live
v86 and scratch v87 in subprocess shards.

| Set | Fixture | Lists | Identical | Sentences only |
| --- | --- | --- | --- | --- |
| v83 | `f1099b_backup_withholding_v83` (the 298 the v86 test replays) | 298 | 298 | 0 |
| v81 | `code_b_sales_v81` (exported returns, uncorrected) | 206 | 206 | 0 |
| v82 | `sale_family_audit_v82` Track 0, built for v82 | 170 | 169 | 1 |
| v84 | `f1099b_box7_loss_v84` Track 0 grid | 58 | 58 | 0 |
| v85 | `f1099b_box4_only_v85` Track 0 grid | 43 | 43 | 0 |

The one change is `v82/m_empty_exc1_unanswered/honest`. It asks the
only-box-2a question, so the page shows the v3 words. No number changes.

83 lists are refused identically on both cores. They were built for earlier
cores (`same_error_on_both_cores`): 66 v81, 12 v82, 6 v83.

No neighbouring capability gains a prerequisite. A return with none of these
activities computes the same on both cores (`m_wash_none`, `m_exc1_nosale`,
and the identical rows).

## Item 6: integration surface

`track0-surface.json`: 6 of 6 pass. No rule, form field, attachment or entry
point changes, so no externally bound symbol gains or loses a producer
(item 4).

Each changed question is shown verbatim, and on the same fields on both
cores (27 to 32 fields, among them Schedule D lines 1b and 8b and Form 1040
lines 7a, 7b and 16, and Schedule 1 line 21):
- `alc_wash_st_unanswered` and `m_wash_none_unanswered`: the short-term
  wash-sale question
- `alc_wash_lt_unanswered`: the long-term wash-sale question
- `alc_exc1_unanswered` and `alc_exc1_sale_unanswered`: only-box-2a
- `alc_sli_unanswered`: the student-loan question

The six retitled facts' titles appear on no page on either core
(`titles_shown_on_any_page` is empty). A title reaches a workspace only
through bundle adoption, and every v87 run re-adopts the successors without
a refusal.

## Known limitations

These are recorded by the foreman as Decision 6 (parked). They are
unchanged between v86 and v87, and no word change can reach them:

- With a recorded wash sale and only the adjustment family open, the page
  asks no question (P0 `wash-st-unclosed`). When the whole wash sale is open,
  the page does ask: `late_wash_member` step 2.
- Age and blindness default to false and are never asked.

Owner disposition is required by the gate before these can be called
settled.
