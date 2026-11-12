# Review: question wording (core v87, registry v85, release v85)

Reviewer, fresh reader. Charter: `docs/reviews/question-wording/charter-review.md`.
Object: `github/milestone/selection-keyed-collect-2025` (7fb81080) `..` HEAD
80d1cf23 on `milestone/question-wording-2025`. Orientation block verified
at 80d1cf23. Governance not read. Sources: the committed content, tests and
evidence, plus `law.json`'s 2025 IRS extracts and the public 2025
instructions. No builder thread or summary was used as evidence.

## Findings, ordered by consequence

### F1 (blocking). The Exception 1 v3 words leave a truthful filer blocked with no question

- **Where.**
  - `packages/content/tax/2025/input-question.exception1-only-box2a-capital-gains.v3.json:7`
  - the matching fact title in `packages/content/tax/2025/exception1.bundle.v2.json` (fact `exception1.only-box2a-capital-gains`)
  - the source of both: `question-wording-evidence/prototype.py:49-51`
  - pinned in `tests/test_question_wording_v87.py:62-64`
- **Claim violated.** "Each question in scope says exactly what its
  consuming rule reads, for the population it is asked of." The v3 words
  say "and that you did not sell stock, funds or other property in 2025
  (even a sale with no gain or loss)". The rule reads one thing through
  `schedule-d-required.conclusion`: whether Exception 1 applies, which
  means no Schedule D and no Form 8949. "Other property" is broader than
  that. These filers sold something truthfully, need no Form 8949 or
  Schedule D, and so meet Exception 1:
  - someone who sold a used car or household goods at a loss. The 2025
    Schedule D instructions say a loss on personal-use property is not
    deductible, and the sale is reported only when a Form 1099-B, 1099-K or
    1099-S was received. This quote is not in `law.json`; add it if the
    finding is accepted.
  - someone whose IRA or 401(k) sold funds inside the account.

  Under the v2 words ("no capital gains ... other than box 2a (for example,
  no gain from selling ...)") these filers answer yes. Under the v3 words a
  literal reader answers no.
- **Consequence (semantic).** A "no" with no recorded sale reaches the
  parked refusal: the return is blocked and no question is asked. The
  words therefore move a truthful filer from a computed return to a dead
  end, which is the failure this milestone set out to remove. The
  population is large: everyone whose return has no sale, because the
  question is asked while the fact is absent.
- **Reproduction** (published core v87, through the milestone's own
  `track0.execute`, which runs `live_coordinate_run` and the presentation
  model):
  ```python
  t = <load question-wording-evidence/track0.py>
  core = t.harness().Core("v87", "v85", "v85")
  r = t.execute(core, t.say(t.complete(), t.ONLY2A, "no", "rv"), "demo.qw.review.nosale_only2a_no")
  ```
  Result:
  - outcome success
  - Form 1040 lines 7a, 13b and 15: `blocked`
  - line 16: `guard_inapplicable`
  - `schedule-d-required.conclusion`: yes
  - `questions`: `[]`

  The same list with the answer yes (`complete`) computes 7a 0, 15 34,250
  and 16 3,875.
- **Fix.** Limit the sale clause to sales that must be reported, for
  example: "..., and that you had no sale of stock, bonds, funds or other
  investments in 2025 that you must report on Form 8949 or Schedule D
  (even one with no gain or loss)?" Also consider adding: "Sales inside an
  IRA or 401(k), and losses on personal items, do not count." Change the
  fact title to the same scope. Rebuild from `prototype.py`, update the
  pinned `WORDS` / `ONLY_BOX2A`, and add a probe or Track 0 row: no sale
  plus a non-reportable personal-use sale, answered truthfully, computes.
  The citizens are not yet on a ratified line. The foreman decides whether
  to regenerate v87 in place before merge or to publish a further
  successor.

### F2 (should-fix). The "superseded" late steps contain no supersession, so the lifecycle claim is not established

- **Where.**
  - `question-wording-evidence/track0.py:496-503` (`sli_trace`), and the
    `late_exc1_sale_after_yes` step 3 built the same way
  - `tests/test_question_wording_v87.py:156-157`
  - the claim: plan `question-wording.md:198` ("each superseding answer
    replaces the earlier one") and `track0-closure.md:44,80`
- **Measurement.**
  - Each step calls the audit harness's `say`, which first runs
    `strip(acts, fact_type)` ("replacing any earlier one"). The steps are
    therefore fresh single answers.
  - Built on v87, `late_sli_superseded/superseded_claimed`,
    `.../superseded_not_claimed` and
    `late_exc1_sale_after_yes/only2a_superseded_no` each carry exactly one
    assertion of the fact (338, 338 and 340 acts).
  - `superseded_claimed` and `superseded_not_claimed` differ from
    `alc_sli_claimed` and `alc_sli_not_claimed` only in the one answer id
    (`demo.sfa.answer.sli-late-no` / `-late-yes` against `sli-claimed`).
  - `test_runs_are_the_distinct_v87_act_lists` passes only because of that
    id.
- **Consequence (evidence).** No displacement of an earlier answer, no
  currentness and no finding identity is observed. The behavior is
  probably fine, because supersession is unchanged engine behavior. The
  committed claim says more than the evidence shows.
- **Fix.** Either build the steps as real supersessions (an assertion that
  supersedes the earlier finding, with the earlier line 21 finding shown
  non-current), or reword the plan and closure rows to "a different answer
  computes its hand value" and drop the two duplicate SLI runs (see F5).

### F3 (note). The wash-sale v4 words ask a filer with no wash sale to answer yes

- **Where.** `closure-mapping.f1099b-covered-w-st-adjustment.v4.json:11` (and `-lt-`).
- **Measurement.** The v4 words are true of what
  `f1099b-covered-w-*-adjustment-subtotal` v4 reads: the box 1g amounts of
  covered sales with a wash-sale adjustment (Form 8949 instructions, code
  W). On v87, a plain covered sale with no wash sale and the closure
  answered yes gives Schedule D 1a 200 and 1b 0, Form 1040 line 7a 200,
  line 15 34,450 and line 16 3,899. A wash sale (500 / 700, box 1g 200)
  beside a plain sale gives 1a 200, 1b 0 and column (g) subtotal 200, with
  the same lines 7a, 15 and 16. Both match the hand values.
  - For the population the milestone targets, filers with no wash sale,
    the truthful answer is a vacuous "yes".
  - "Have you recorded the amount of every sale with an adjustment?" can
    read as "not applicable" or "no" to someone who has none.
  - The basis and proceeds siblings have the same shape, so this is
    consistent, not a regression.
  - The phrase "wash-sale loss adjustment" appears twice in a 50-word
    sentence.
- **Fix (optional, later).** Add "(answer yes if you had none)" across the
  covered-W family's questions in a future wording pass.

### F4 (note). Two SLI hand cases are fact patterns that cannot occur, and the blindness title has no date

- `m_sli_joint_spouse_claimed` / `m_sli_joint_filer_claimed` (and the
  P0 `sli-mfj-claimed-no`):
  - A spouse on a joint return with $1,853 of tax cannot be anyone's
    dependent under the joint-return test.
  - The single "claimed" cases leave the standard-deduction
    `can-be-claimed-as-dependent` at its default no, which is inconsistent
    with being claimed.
  - The hand values are still right. At $50,000 of earned income the
    dependents worksheet gives the full $15,750 / $31,500, and line 21 is
    $0 as the instruction says.
  - The counterexample that motivated Decision 3 cannot happen on a return
    that owes tax. The spouse clause is still the Form 1040 line 21 text
    and is harmless.
  - Record this; no change is needed.
- `core_calculations.bundle.v3.json`, `taxpayer-blind` / `spouse-blind`
  title: "or has a statement certified by an eye doctor ..." does not say
  "as of December 31, 2025". The instruction's test is the condition at
  the end of 2025, and the statement documents it. No page shows the
  title today. Fix it when the next milestone (age and blindness asked)
  turns this into a question.

### F5 (note). CI cost

- **Measured.** The 28 live runs are distinct only up to ids:
  - normalizing `demo.*` ids leaves 26 distinct lists
  - `late_sli_claimed` equals `sli_claimed`
  - `late_sli_not_claimed` equals `sli_not_claimed`
- **Saving.** Dropping those two runs, or making them real supersessions
  per F2, removes 2 runs (about 2 s) and loses no Track 0 row witness,
  since each row stays on its sibling run.
- **The 298 replays** are about 91% of the module's runs:
  - They are 298 distinct act lists (283 after id normalization) with 222
    distinct recorded pins.
  - Dropping the 15 near-duplicates would lose the literal "298 identical"
    claim the charter asks to keep, so I do not recommend it.
  - The four `title_*` runs exercise only unchanged v86 rules, because no
    rule or page reads a title. They are still the only witnesses of the
    `alc_title_*` rows.
- **Floor.** Under the charter's constraint the module can shrink to 324
  runs and no further. Shrinking more requires replacing the 298 replay
  with a structural argument: the seven member edits, byte-identical
  readers (`track0-reuse.json`), and the v86 module's own 298 replay. That
  is an owner decision, not a defect.

## Charter questions answered

1. **Truth by hand.** Each fact was checked against the 2025 Form 1040,
   Form 8949, Schedule D and Pub. 970 extracts in `law.json`:
   - The wash-sale words are true (F3 is a note).
   - The SLI words match the Form 1040 line 21 text.
   - The age titles match the line 12d and Schedule 1-A Part V rules,
     including the day-before rule and the death example.
   - The blindness title omits the date (F4).
   - The Exception 1 words are not true for their population (F1).

   I ran these on published v87 through `live_coordinate_run` with
   synthetic `demo.qw.review.*` ids:

   | Case | Lines the rule feeds | Hand value |
   | --- | --- | --- |
   | Plain covered sale, no wash sale | 1a 200, 1b 0, 7a 200, 15 34,450, 16 3,899 | matches |
   | Wash sale beside a plain sale | 1a 200, 1b 0, adjustment subtotal 200, 16 3,899 | matches |
   | Zero-net sale, only-box-2a no | 1a 0, 7a 0, 7b `guard_inapplicable`, 15 34,250, 16 3,875 | matches |
   | Zero-net sale, only-box-2a yes | the same numbers; conclusion "no" beside a sale (stale and unread, as `track0-closure.md` explains) | matches |
   | Joint return, spouse claimed | line 21 0, 15 18,500, 16 1,853 | matches |
   | Single filer claimed | line 21 0, 12e 15,750, 15 34,250, 16 3,875 | matches |

   Tax Table midpoints check, for example 34,275 gives 3,874.50, rounded
   to 3,875. Independently recomputed hand values: 17,750 / 6,000 / 2,915
   (age), 3,635 (blind), 33,100 / 1,093 and 31,500 / 1,853 (joint), and
   500 / 3,815. **No hand value pinned in `tests/test_question_wording_v87.py`
   is wrong.**
2. **Meaning change.**
   - **Exception 1.** A recorded v86 "yes" beside a recorded sale is false
     under v3, but nothing reads it while a sale exists. The real risk is
     F1: a fresh truthful answer moves a computed return to a blocked one.
   - **Wash sale.** A recorded v86 "no" from a plain-sale filer is false
     under v4. It stays recorded and blocks line 1b, but the page asks
     again (`wash_st_no` shows the v4 sentence), so the filer can correct
     it.
   - **SLI.** A recorded v86 "no" from a joint filer whose spouse is
     claimed would now be false and is not asked again. The fact pattern
     cannot occur on a return that owes tax (F4).
   - **Numbers.** No number moves the wrong way for a truthful answer,
     apart from the F1 block.
3. **What the filer sees.**
   - The SLI words are plain.
   - The wash-sale words are long and have the vacuous-yes problem (F3).
   - The Exception 1 words promise more than the rule (F1).
4. **Immutability.**
   - The diff over `packages/schemas`, `packages/kernel` and
     `packages/derivation` is empty.
   - Under `packages/` only `packages/tax/loader.py` is modified; every
     other file is added.
   - Registry v85, compared with v84 as sets, removes nothing, changes no
     entry and adds exactly the seven successors and core v87.
   - Release v85 pins the sha256 of `published-packages.v85.json`.
   - All seven successors are byte-identical to
     `prototype.artifacts(True)`, rerun independently.
   - The loader diff adds only the v87 keys. Its companion declaration and
     covered-flag map equal v86's.
5. **CI cost.** See F5.
6. **Test isolation.**
   - Both new modules load evidence harnesses (`track0.py`,
     `audit_harness.py`, `prototype.py`) only through
     `tests/evidence_loader.load`.
   - The one by-path load of a non-evidence file is the v83 *test* module
     (`_module`). The loader refuses non-evidence paths, and the v86
     module uses the same pattern.
   - A grep of the two test modules and `track0.py` for `setattr`, attribute
     assignment and `global` finds no assignment to another module's
     globals.
7. **Browser failures.** No.
   - `tests/test_explanation_saved_browser.py` runs core v8 against
     registry v3 (`generate_capital_gain_distributions_line7a_t3_presentation_goldens._surface`)
     and calls Chrome with a 40 s timeout.
   - This diff touches no derivation, presentation or browser code. The
     only shared code it changes is two v87-keyed loader entries, and the
     new closure-mapping files are schema v3 mappings that the loader
     validates one at a time.
   - Nothing in the diff reaches that path. The failures fit parallel
     Chrome contention.
8. **Data safety.**
   `python3 tools/envelope_scan.py --range github/milestone/selection-keyed-collect-2025..HEAD`
   exits 0. The diff has no absolute local paths; the only matches are
   scrub needles in the evidence code.

The suite was not run; no claim needed it. The live cases above were
single coordinator runs.

## Verdict

**Not ready.** Blocking: F1. Should-fix: F2. F3 to F5 are notes.

## Re-review

Reviewer, fresh reader. Charter: `docs/reviews/question-wording/charter-rereview.md`.
Orientation block verified at `a39d94d8`. Object: the repair after `584aa65a`,
diffed against `github/milestone/selection-keyed-collect-2025`. Governance
not read. Sources: the committed citizens, `law.json`, the 2025 Form 1040,
Form 8949 and Schedule D instructions, and coordinator runs on published
core v87 through `question-wording-evidence/track0.py` (`live_coordinate_run`).
No builder thread was used as evidence.

### R1 (blocking). A Form 1099-K personal-item loss reported on Schedule 1 still meets Exception 1, and the v3 words say it does not

- **Where.**
  - `packages/content/tax/2025/input-question.exception1-only-box2a-capital-gains.v3.json:7`
  - the same scope in `packages/content/tax/2025/exception1.bundle.v2.json:11`
  - both generated from `question-wording-evidence/prototype.py:50-56` and `:85-96`
  - the row that calls the blanket no the true answer: `question-wording-evidence/track0.py:461-463`
- **Claim violated.** The question and the fact title have to be true of what `schedule-d-required.conclusion` reads, for everyone asked, per the 2025 instructions. The conclusion (`rule.schedule-d-required.conclusion.json:12-36`) is "no" only when all four Exception 1 components are yes. Component C1 is this fact. A "no" makes the conclusion "yes" (Schedule D required).
- **What the instructions say.** Schedule D, Capital Assets Held for Personal Use (`law.json` `personal-use`): a personal-use loss is not deductible; a Form 1099-S loss on personal-use real estate must be reported on Form 8949; a Form 1099-K loss on personal property must be reported on Form 8949 or on Schedule 1. The 2025 Form 1040 instructions put a personal item sold at a loss in the entry space at the top of Schedule 1, and send a personal item sold at a gain to Form 8949 and Schedule D. The 2025 Form 8949 instructions say a personal-property loss generally should not be reported on Form 8949, and that a Form 1099-K loss may be zeroed on that Schedule 1 entry space or on Form 8949. The Schedule 1 path files neither Form 8949 nor Schedule D, so Exception 1 still holds when the only capital gains are box 2a.
- **What the words say.** "Neither does a loss on a personal item unless you received a Form 1099-K or 1099-S for it." Any Form 1099-K loss defeats C1. The title's operative sentence says the same, then quotes the Schedule D sentence that allows Schedule 1. The quote and the operative sentence disagree.
- **Consequence (semantic).** A filer who follows the Form 1040 instructions and reports the Form 1099-K loss on Schedule 1 is asked this question (nothing records that sale) and answers no. The conclusion becomes Schedule D required, and the return hits the parked refusal. The Form 1099-S half is consistent: that loss must be reported on Form 8949. The no-form personal loss and the IRA sale are consistent: both answer yes and compute.
- **Reproduction** (published core v87, synthetic `demo.qw.rereview.*` ids):
  ```python
  t = <load question-wording-evidence/track0.py>
  core = t.harness().Core("v87", "v85", "v85")
  yes = t.complete()  # truthful C1 yes: no sale, personal-item loss with no form, or IRA sales only
  no = t.say(t.complete(), t.ONLY2A, "no", "only2a-1099k")
  ```
  The personal-item loss with no form, and sales inside an IRA only, are the same act list as no sale: nothing records either one. All three yes runs: outcome success, conclusion "no", line 7b `published_categorical`, 7a 0, 13b 0, 15 34,250, 16 3,875. The Form 1099-K run answered no, as the v3 words require: outcome success, conclusion "yes", 7a blocked, 7b `guard_inapplicable`, 13b blocked, 15 blocked, 16 `guard_inapplicable`, and the Exception 1 sentence is not asked. With the fact unanswered, the page shows the whole v3 sentence, including the note after the question mark. The yes act list is what a Schedule 1 reporter should answer, and it computes.
- **Fix.** In the question and the fact title, a personal-item loss counts only when it must be reported on Form 8949 or Schedule D. A Form 1099-S loss does. A Form 1099-K loss does only when the filer reports it on Form 8949; the Schedule 1 entry space does not. Rebuild those two citizens from `prototype.py` in place, and stop calling the blanket no the true answer. Leave the parked refusal after a true no as the engine gap it is.

## Charter questions

1. **F1, the four runs.** No sale, a personal item sold at a loss with no form, and sales inside an IRA only each answer yes and compute to 7a 0, 15 34,250, 16 3,875, with line 7b checked and the conclusion "no". The same personal-item loss with a Form 1099-K, answered as the words require, is the parked refusal above. The sentence matches the instruction for no form, for Form 1099-S, and for an IRA. It does not match the Form 1099-K rule (R1). The fact title has the same operative scope.
2. **F2, F4, F5, against Decision 7.**
   - **F2 fixed.** `say` strips the earlier assertion. Each later Exception 1 step and each later student-loan step carries one assertion of that fact (340 acts on the Exception 1 replacement, 338 on each student-loan step). After `demo.*` ids are normalized, `late_sli_superseded/superseded_claimed` equals `alc_sli_claimed`, and `superseded_not_claimed` equals `alc_sli_not_claimed`. `track0-closure.md:80-90` and Decision 7 say that, and no longer say a supersession act was exercised.
   - **F4 fixed.** `core_calculations.bundle.v3.json:82` and `:138` name December 31, 2025 on the eye-doctor test. From `584aa65a` to HEAD those two titles are the only change in that bundle.
   - **F5 fixed.** `tests/test_question_wording_v87.py:151-156` judges the later student-loan answers on the sibling runs. The module lists 27 runs. The two id-only repeats are not among them.
3. **Regeneration.** `prototype.artifacts(True)` matches all seven v87 members byte for byte, and each registry checksum matches `citizen_checksum`. Core v87's `package_checksum` matches `package_instance_checksum`. Against `published-packages.v84.json` on `github/milestone/selection-keyed-collect-2025`, registry v85 changes no old entry and adds the seven successors plus core v87. That v84 file is unchanged on this branch. Release v85's `package_registry_sha256` is the sha256 of the v85 registry bytes. `git diff --name-only` over `packages/schemas`, `packages/kernel` and `packages/derivation` for that range is empty.
4. **Anything new.** R1. The harness now treats a sentence that contains a question mark as a question (`track0.py:207-208`). On the unanswered no-sale run the page shows the full v3 sentence, note included. The other question on a computed no-sale return is the existing box 4 question. No schema, kernel, or derivation file changed.
5. **Data safety.** `python3 tools/envelope_scan.py --range github/milestone/selection-keyed-collect-2025..HEAD` exits 0 and prints nothing. This section has no absolute path and no temp-directory path.

The suite was not run. No failing claim needed it. The five coordinator runs above are the measurements.

## Re-review verdict

**Not ready.** Blocking: R1. F2, F4 and F5 are fixed as Decision 7 says. Regeneration and the substrate diff hold.

## R1 check

Reviewer. Object: `bc807dfe`..`edf2e404`. The v3 question
(`input-question.exception1-only-box2a-capital-gains.v3.json:7`) and the
exception1 v2 title (`exception1.bundle.v2.json:11`) now say a personal-item
loss does not count unless the filer received a Form 1099-S or reports that
loss on Form 8949. Both are byte-identical to `prototype.py`.

Published core v87, through `track0.execute`, synthetic `demo.qw.r1.*`:

- No form, Form 1099-K on Schedule 1, and IRA-only sales. Truthful answer
  yes. Those three share the no-sale act list. Each run: conclusion "no",
  line 7b `published_categorical`, 7a 0, 13b 0, 15 34,250, 16 3,875.
- Form 1099-S, and Form 1099-K reported on Form 8949. Truthful answer no.
  Those two share one act list. Each run: conclusion "yes", 7a blocked, 7b
  `guard_inapplicable`, 13b blocked, 15 blocked, 16 `guard_inapplicable`,
  Exception 1 question not shown. That is the parked engine gap after a
  true no.
- Unanswered, the page shows the whole v3 sentence, including the note
  after the question mark.

Those five answers are what the 2025 Form 1040, Form 8949, and Schedule D
instructions require of this fact. The conclusion reads the yes/no; yes
computes Exception 1, and no means Schedule D is required.

Regeneration holds. All seven v87 members match `prototype.artifacts(True)`
byte for byte, and the registry checksums match. Against v84 on
`github/milestone/selection-keyed-collect-2025`, registry v85 changes no
old entry and adds the seven successors plus core v87. Release v85 pins
the v85 registry bytes. The diff under `packages/schemas`,
`packages/kernel`, and `packages/derivation` is empty.
`envelope_scan.py` on `bc807dfe^..HEAD` and on
`github/milestone/selection-keyed-collect-2025..HEAD` exits 0.

Note: `law.json` reading still quotes the previous v3 phrase "unless you
received a Form 1099-K or 1099-S". The IRS extracts in that file are
unchanged. The citizens do not use that phrase.

## R1 check verdict

**Ready.** Blocking list: none.
