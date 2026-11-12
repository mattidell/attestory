<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "question-wording",
  "status": "Open. Track 0 closed; limitations disposed; Track 1 chartered.",
  "scope": [
    "each question in scope says exactly what its consuming rule reads, for the population it is asked of, per the 2025 instructions",
    "the successors are content only: question citizens, bundles, core v87, registry v85, release v85",
    "every recorded return computes the same numbers on v87 as on v86 when answered truthfully"
  ],
  "non_goals": [
    "no engine, schema, expression-operation or recording-surface change",
    "no new question, rule or line; no change to which returns are asked a question",
    "the refusal with no question after a false Exception 1 no (an engine change; stays parked)"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/question-wording.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/question-wording.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/question-wording.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/question-wording.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Questions Say What Their Rules Read (2025)

Milestone key: question-wording.
Branch: milestone/question-wording-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-11.
Starting point: `milestone/selection-keyed-collect-2025` at `7fb81080`
(PR #270, core v86, stacked; ADR 0085 awaits acceptance).

## What we are trying to accomplish

Three parked wording defects let a filer answer a question truthfully and
still give its rule the wrong input:

1. The two Form 1099-B wash-sale adjustment questions ask for an amount
   "of every covered sale", while their basis and proceeds siblings limit
   to sales with an adjustment.
2. The v2 Exception 1 questions still invite "yes" beside a zero-net sale,
   where no rule reads them since line 7b v2.
3. The age questions say "born before January 2, 1961" and handle a death
   in 2025 before age 65 loosely; the student-loan dependent answer says
   "is claimed" and asks the filer only, beside the newer "can be claimed"
   answer.

The useful outcome is a core v87 whose wording, for each question, matches
what the consuming rule reads and the 2025 instructions, with no change to
any published number for a truthful answer.

## What we know

- Each item is listed as wording in the roadmap's parked list.
- **What we do not know.** For each question: its exact current text, the
  rule that reads it and what that rule reads, the instruction it rests
  on, and whether a truthful answer under the current words can differ
  from one under the corrected words for any recorded return. Whether any
  item needs more than a question successor.

## Actions the team will take

1. **P0: measure and design.** For every question in scope, quote its
   text, its consuming rules, and the 2025 instruction; state who is asked;
   propose words. Probe a truthful filer on core v86 where the current
   words mislead. Prototype a scratch core v87 and rerun recorded returns.
   Stop and report any item that needs more than content.
2. **Decide.** The words, and which items are in.
3. **Track 0 adversarial closure.** Over the new words.
4. **Track 1: build.** Core v87, registry v85, release v85, with live and
   package tests.
5. **Close.** Fresh-reader review, repair, exact-head CI, retrospective,
   roadmap. Merge on green verify after #270 (owner standing approval,
   2026-11-07).

## Cases that will shape the design

- A covered sale with a wash-sale adjustment beside one without: what each
  wash-sale question's answer should total.
- A zero-net sale beside the Exception 1 questions.
- A filer born on January 1, 1961, on January 2, 1961, and a filer who died
  in 2025 before turning 65.
- A student-loan filer who can be claimed as a dependent but is not.
- Every recorded return the earlier milestones replay: identical numbers on
  v87 when answered as recorded.

## Process

Dispatch is through the grok CLI (owner, 2026-11-09). Each unit commits on
this branch as it goes. Hand values come from the instructions, never from
what a prototype publishes. A sentence the filer reads is a claim: P0
records the text the presentation actually shows. Stacked on #270; if ADR
0085 is not accepted, this branch is rebuilt on main with the next free
core version.

## P0 result

Evidence: `question-wording-evidence/p0.md`, with `law.json`, `probe.py` /
`probe-output.json` (v86), `probe-v87-output.json`, `prototype.py` /
`prototype-build.json` and `rerun.py` / `rerun-output.json`.

- **All three items are content only.** None needs an engine, schema,
  expression-operation, selection or recording-surface change. Scratch core
  v87 (registry v85, release v85) replaces five members:
  - the two wash-sale adjustment closure questions (v4)
  - the Exception 1 only-box-2a question (v3)
  - the student-loan dependent question (v2)
  - the vocabulary bundle (v3), which retitles the four age and blindness
    facts without changing their versions
- **Truthful answers under the current words:**
  - A plain covered sale stays blocked on the wash-sale question.
  - A filer born January 1, 1961 gets 15,750 and no senior deduction,
    instead of 17,750 and 6,000.
  - A joint filer whose spouse is claimed deducts 500 instead of 0.
  - A zero-net sale moves no number, whatever the Exception 1 answers.
- **Under the proposed words**, all 25 probe cases reach their instruction
  hand values on v87.
- **Rerun:** the 298 recorded v83 lists that the v86 test replays are 298
  identical on v86 and v87, and every v86 pin equals its fixture pin. None
  of them shows a question in scope. In the probes, 5 cases change only
  their sentences and 20 are identical.
- **Outside the words, reported, not fixed:**
  - With a recorded wash sale and the adjustment family open, the page asks
    nothing (an admission check with no question).
  - Age and blindness are never asked (default false, no question), and
    their titles are not shown on any page measured.
- **Decisions:**
  - whether to retitle the Exception 1 and student-loan facts in their
    bundles
  - whether to keep the age and blindness title successor
  - the v87 loader entries in `packages/tax/loader.py` (code, as every core
    since v80)
  - whether to park the mixed wash-sale finding

## Decisions

Foreman, 2026-11-11, on P0. Every item is content only; the 298 recorded
returns are identical on v86 and scratch v87.

1. **Wash sale.** Both wash-sale amount questions take the P0 v4 words:
   the amount of every covered sale *with* a wash-sale loss adjustment.
2. **Exception 1.** The only-box-2a question takes the P0 v3 words, which
   exclude any 2025 sale, a zero-net sale included. The fact's title in a
   successor of `exception1.bundle.json` says the same.
3. **Student-loan dependency.** The question takes the P0 v2 words ("Is
   someone else claiming you (or your spouse, on a joint return) as a
   dependent on their 2025 return?"), and the fact's title in a successor
   of `sli-scope.bundle.json` names the spouse too.
4. **Age and blindness titles.** The vocabulary bundle successor takes the
   P0 v3 titles: born before January 2, 1961, the day-before-the-birthday
   rule, the death-in-2025 rule, and the blindness test as the instruction
   states it. Fact versions do not change. No page shows these titles
   today; they are kept so the fact means what the law says when it is
   asked.
5. Core v87, registry v85 and release v85, with their entries in
   `packages/tax/loader.py` as for every core since v80. Nothing else in
   code changes.
6. **Parked**, not built: with a recorded wash sale and the adjustment
   family open, the page asks no question; age and blindness are never
   asked and default to false.

7. **Review repair** (foreman, 2026-11-11, on review 584aa65a).
   - F1: the Exception 1 v3 sale clause covers sales that need no Form
     8949 or Schedule D (personal-use losses, sales inside an IRA or
     401(k)), so a truthful filer answers no and is blocked with no
     question. The clause is limited to sales that must be reported on
     Form 8949 or Schedule D, with a short exclusion sentence, and the
     fact title follows. The v87 members are regenerated in place: none
     is on a ratified line yet.
   - F1 follow-up: a personal-item loss reported on Form 1099-K or
     1099-S must be reported, so it counts. The exclusion sentence and
     fact title name those two forms (the Schedule D personal-use
     instruction names Form 1099-K and Form 1099-S). Track 0 row
     `m_exc1_personal_loss_1099k`: no sale recorded, truthful no under
     the v87 words, parked no-question refusal (the existing parked
     engine gap, not a wording defect).
   - R1: a Form 1099-K personal-item loss may go on Schedule 1, which
     files no Form 8949 or Schedule D, so it does not defeat Exception 1.
     The exclusion sentence and fact title name Form 1099-S or a report
     on Form 8949. Track 0 splits the 1099-K row:
     `m_exc1_personal_loss_1099k_sch1` answers yes and computes to the
     no-sale hand values; `m_exc1_personal_loss_1099k_8949` answers no
     and reaches the parked no-question refusal (the existing engine
     gap, named as such).
   - F2: the student-loan and Exception 1 late steps replace an answer;
     they do not supersede one. The claim is reworded to what the
     traces show.
   - F4: the blindness title names December 31, 2025.
   - F5: the two live runs that repeat a sibling are dropped.
   - F3 stays a note.

## Track 0 adversarial closure

Evidence: `question-wording-evidence/track0-closure.md` and the
`track0-*.json` files that `track0.py` writes. Every case is a
`live_coordinate_run` on published v86 and scratch v87. Scratch v87 now
carries Decisions 1-4, including the exception1 and sli-scope title
successors (seven members).

- Authority-lifecycle table: PASS. `track0-authority.json` has 16 of 16
  cases. For each changed question it shows that the question is asked when
  unanswered, that a no and a yes reach their hand values, and which rule
  reads the answer. Examples: `alc_wash_st_unanswered`, `alc_wash_st_no`,
  `alc_exc1_sale_unanswered`, `alc_sli_claimed`, and `alc_title_spouse_age`
  against `alc_title_spouse_died_before_65`.
- Empty/nonempty authority matrix: PASS. `track0-matrix.json` has 14 of 14
  cases on v87. On v86 the words lead a truthful filer to three
  counterexamples, and the v87 words fix each one: `m_wash_plain`,
  `m_wash_both` and `m_sli_joint_spouse_claimed`. After review F1,
  `m_exc1_personal_loss` adds a filer with no recorded sale who sold only
  a personal item at a loss: the repaired words are answered yes and the
  return computes.
- Late-member lifecycle: PASS. `track0-late.json` has 3 of 3 traces.
  - `late_wash_member`: a member added after the closure makes the closure
    non-current, and reclosing computes.
  - `late_sli_superseded`: each later answer replaces the earlier one in
    the act list, and computes its hand value. No supersession act is
    exercised (review F2).
  - `late_exc1_sale_after_yes`: the stale yes is never read beside a sale,
    because all three readers of the conclusion, unchanged, take the
    Schedule D path first. The step reaches its hand values.
- Neighboring capability dependency diff: PASS. `track0-neighbour.json` has
  775 distinct recorded lists (v83 298, v81 206, v82 170, v84 58, v85 43).
  774 are identical. One, `v82/m_empty_exc1_unanswered/honest`, changes only
  the only-box-2a sentence it asks. 83 lists are refused identically on both
  cores. No neighbour gains a prerequisite.
- Reused-claim semantic/lifecycle equivalence: PASS. `track0-reuse.json`
  shows that only words, titles and versions differ. The 19 readers are
  byte-identical, and the fact-type identities, question pins and input
  bindings are unchanged.
- Integration surface: PASS. `track0-surface.json` has 6 of 6: each changed
  question is shown verbatim on the same 27-32 fields on both cores. No
  externally bound symbol gains or loses a producer, and no page shows a
  retitled fact title.
- Known limitations affecting correctness: two, parked by Decision 6 and
  unchanged by the words. Owner disposition is required:
  - with a recorded wash sale and only the adjustment family open, the page
    asks nothing
  - age and blindness are never asked

**Disposition.** Foreman, 2026-11-11, under the owner's standing grant to
apply recommended choices (the owner may reverse it before merge; nothing
here merges ahead of #270). Both limitations are outside this milestone's
class: the words cannot fix a question that is never asked. Age and
blindness being asked is the next milestone
(`milestone/age-blindness-asked-2025`, stacked on this branch). The page
asking nothing beside a recorded wash sale stays parked in the roadmap.
Track 0 is accepted and Track 1 is chartered
(`docs/reviews/question-wording/charter-track1.md`).

## Track 1 result

Charter: `docs/reviews/question-wording/charter-track1.md`. Builder,
2026-11-11.

- **Successors.** The seven members are in `packages/content/tax/2025/`,
  generated from `prototype.artifacts` and byte-identical to it: the two
  wash-sale adjustment closure mappings (v4), the Exception 1 only-box-2a
  question (v3), the student-loan dependent question (v2), and the
  exception1 (v2), sli-scope (v2) and vocabulary (v3) bundles. No published
  citizen was edited.
- **Core v87, registry v85, release v85** were made with
  `python3 -m tools.package_successor` from v86, v84 and v84. Registry v85
  only adds core v87 and the seven successors. `packages/tax/loader.py`
  gives v87 v86's companion declaration and covered-flag refusal map; the
  selection-collect switch is on from v86 by rank, so v87 carries it
  unchanged. `tests/test_noncovered_sales_v78_switch.py` names v87 among
  the cores with the refusal map, as v86's build did.
- **Live module** (`tests/test_question_wording_v87.py`). The 16
  authority cases, 13 matrix cases and 9 late steps reduce to 28 distinct
  v87 act lists; each runs once on published core v87 through
  `live_coordinate_run` and the presentation model, and every case sharing
  it is judged on that run. A test proves no two runs share an act list.
  All 38 cases and steps reach their hand values, written in the test from
  track0.py's instruction values (and checked equal to them). The four
  decided sentences are pinned exactly: each is shown where its question
  is asked (a false wash-sale closure answer is asked again), and no v86
  sentence is shown anywhere. With a recorded wash sale and the
  adjustment family open, the page shows no wash-sale question, as
  Decision 6 parks.
- **298 recorded runs.** The 298 recorded v83 lists replay on published
  v87 against `tests/fixtures/f1099b_backup_withholding_v83/expected.json`
  in place: 207 as recorded and 91 restored with no-sale box 4
  present=no, as the v86 module replays them. All 298 are identical to
  their fixture pins.
- **Run count.** The live module makes 326 `live_coordinate_run` calls
  (28 + 298) in 329 tests; one local run of the module took 334 s wall.
- **Package test** (`tests/test_question_wording_v87_package.py`, fast):
  byte identity with the prototype, the decided words, each successor
  differing from its predecessor only in words, titles and version, the
  seven member edits, registry v85 add-only, release v85 pinning registry
  v85, the v87 loader entries, and v86 and earlier unchanged.
- **Checks.** Fast lane (`pytest -m "not live"`): 1801 passed, 8
  skipped. Full suite, run as seven shards that cover `tests/` (sum):
  6909 passed, 24 skipped, 4 failed. The four failures are in
  `tests/test_explanation_saved_browser.py` (headless browser calls with a
  40 s timeout) and occurred while two shards ran at once; the file passes
  8 of 8 run alone. No file this track touches is involved. CI `verify` is
  the gate of record. `python3 -m mypy`: no issues in 484 source files.
  `python3 tools/envelope_scan.py --range github/main..HEAD`: clean.
- **Deviations.** None from the charter. The covered-flag refusal test in
  `tests/test_noncovered_sales_v78_switch.py` was extended to v87, as the
  v86 build extended it to v86.

**Review repair** (charter `docs/reviews/question-wording/charter-repair.md`,
Decision 7). This updates the counts above.

- **F1.** The only-box-2a v3 question now reads: "Is it true that you had
  no capital gains in 2025 other than capital gain distributions in box 2a
  of Form 1099-DIV, and that you had no sale in 2025 of stock, bonds, funds
  or other property that you must report on Form 8949 or Schedule D (even
  one with no gain or loss)? Sales inside an IRA or 401(k) do not count,
  and neither does a loss on a personal item unless you received a Form
  1099-S for it or you report it on Form 8949." The exception1 fact title
  has the same operative scope. `law.json` quotes the Schedule D
  personal-use instruction, including the Form 1099-K and 1099-S reporting
  sentences. The Track 0 row `m_exc1_personal_loss` passes on both cores:
  no sale is recorded, no Form 1099-K or 1099-S, the answer is yes, and the
  return computes 7a 0, 15 34,250, 16 3,875, with line 7b checked.
- **F1 follow-up.** `m_exc1_personal_loss_1099k`: no sale recorded, the
  filer had a personal-item loss reported on a Form 1099-K, truthful no
  under the then-current v87 words. The page hits the parked no-question
  refusal (conclusion yes, lines 7a, 13b and 15 blocked, line 7b
  `guard_inapplicable`, no Exception 1 question). That is the existing
  parked engine gap, not a wording defect; the words lead to the true
  answer. Track 0 was rerun (cases, merge, reuse): authority 16/16,
  matrix 15/15, late 3/3, surface 6/6, reuse pass. The neighbour diff was
  not rerun: it replays recorded answers, which no wording can move.
- **R1.** A Form 1099-K personal-item loss may go on Schedule 1, which
  files no Form 8949 or Schedule D, so it does not defeat Exception 1.
  The v3 trailing sentence and the exception1 fact title now name Form
  1099-S or a report on Form 8949. Track 0 splits the 1099-K row:
  `m_exc1_personal_loss_1099k_sch1` answers yes and computes to the
  no-sale hand values (line 7b checked, 7a 0, 15 34,250, 16 3,875);
  `m_exc1_personal_loss_1099k_8949` answers no and reaches the parked
  no-question refusal (the existing engine gap, named as such). Track 0
  was rerun (cases, merge, reuse): authority 16/16, matrix 16/16, late
  3/3, surface 6/6, reuse pass.
- **F4.** The blindness titles put the eye-doctor test as of December 31,
  2025 too.
- **Regenerated in place.** The two affected branch-only members (only-box-2a
  v3 and exception1 bundle v2), plus registry v85 and release v85, were
  regenerated. Core v87's member list and checksum are unchanged. Registry
  v85 still only adds to v84 on `milestone/selection-keyed-collect-2025`.
- **F2.** The late-step claim is reworded: each later answer replaces the
  earlier one in the act list. **F5.** The two repeated student-loan runs
  are dropped. Act lists are compared with `demo.*` ids normalized.
- **Live module.** 27 distinct v87 runs judge the 16 authority cases, 16
  matrix cases and 9 late steps (41 rows), all at their hand values, plus
  the 298 recorded runs, all identical. That is 325 `live_coordinate_run`
  calls in 328 tests. The two v87 modules and the v78 switch test pass
  342 of 342 in 374 s wall.
- **Checks.** `pytest tests/test_question_wording_v87.py
  tests/test_question_wording_v87_package.py
  tests/test_noncovered_sales_v78_switch.py`: 342 passed in 374 s wall.
  `python3 -m mypy`: no issues in 484 source files.
  `envelope_scan.py --range
  github/milestone/selection-keyed-collect-2025..HEAD`: clean.
- **Harness.** The Track 0 harness now counts a page sentence as a
  question when it contains a question mark. The repaired words end with
  a note after the mark.
