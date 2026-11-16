# Review: preferential base reason (core v91)

Reviewer, fresh reader. Charter: `docs/reviews/preferential-base-reason/charter-review.md`.
Object: `github/main` (`2478955196a10f34da16fc15db2d89362568d267`) `..` HEAD
(`c6a5b25a2a719d35c4632310316a3e75f2318b00`) on
`milestone/preferential-base-reason-2025`. Orientation block verified at
that HEAD. Governance not read.

Scope: on a return where Schedule D is required and no sale or Schedule D
amount is recorded, the blocked Form 1040 lines a filer sees name the
questions that unblock them. Answering truthfully reaches the 2025-instruction
hand values. Recorded returns keep their numbers. Evidence is the committed
tree, the tests, and fresh coordinator runs. Stop after this review is
committed.

Runs used published core v90 (registry v88, release v88) and published core
v91 (registry v89, release v89) through the real coordinator. The authority
grid is activity `none` / `sale` / `amount`, Schedule D conclusion `no` /
`required` / `open`, boundary `open` / `answered`. The four recorded returns
are `m_2a_only_exc1_only2a_no`, `m_empty_exc1_nolosses_no`,
`m_empty_exc1_only2a_no`, and `t4_s1_removed`. Hands below are the
2025-instruction values already used by the v91 test: wage (line 7a 0, 11a
50000, 15 34250, 16 3875, 24 3875, 33 4500, 37 0), box 2a inside the 0% band
(7a 1000, 11a 51000, 15 35250, 16 3875), and the entered short-term sale
(Schedule D lines 3 and 7 are -6000, line 21 is 3000, Form 1040 line 7a
-3000, 11a 47000, 15 31250, 16 3515).

## Findings

### N1 (note). The published test accepts a wrong line, a wrong sentence, and an answered "unanswered" case

- **Where.** `tests/test_preferential_base_reason_v91.py:108`
  (`_leave_unanswered`), `:244` (authority cells), `:342` (recorded
  unanswered fields). `preferential-base-reason-evidence/track0.py:306`
  (`signature`) keeps disposition, code, guard, missing, and value.
- **Claim.** The test locks the one allowed disposition change, the eight
  question count, and the hand values on the answered paths.
- **Consequence.** Evidence gap. A wrong rule can still pass.
  The authority loop fails only when producer signatures differ outside
  `none` / `required` / `answered`, so a downstream line can change and the
  cell still passes. The recorded loop checks that each of the 23 fields
  has eight questions, so a different sentence at the same count passes,
  and it does not require the v90 and v91 line maps to be equal. A case
  whose id contains `unanswered` may still assert the eight facts:
  `_leave_unanswered` rejects only an act list that contains `pbr-sale`,
  and rejects a Path B assertion only for `bnq/sd_path_b_unanswered`.
  The four recorded `/unanswered` lists already assert seven of the eight
  facts. The file has one live test, so no live run merely repeats a
  sibling. Both v91 test modules load evidence through
  `tests/evidence_loader.py`.
- **Reproduction.** The recorded honest lists, read as act assertions,
  contain `exception1.only-box2a-capital-gains`, `exception1.no-capital-losses`,
  `exception1.no-qof-deferral`, `exception1.no-boxes-2b-2c-2d`,
  `f1099b.noncovered-sold.source-closure`, `f8949.no1099b-sold.source-closure`,
  and `schedule-d-boundary.no-form8949-sources`. `_leave_unanswered` returns
  for those lists. Fresh coordinator runs, recorded under "Verified", show
  the lines and the eight sentences are in fact stable; the test does not
  establish that on its own.
- **Fix.** Compare line maps on every authority cell, compare the eight
  question strings rather than the count, and reject the eight fact ids in
  any case whose name means those facts are absent. Leave the single live
  test as the coordinator run.

### N2 (note). Line 16 and four lines that explain through it still name four questions

- **Where.** `packages/content/tax/2025/rule.form1040-line16.v8.json:387`
  blocks `DEPENDENCY_ABSENT` with the four sale-boundary names. Published
  core v91 still carries line 16 v8.
- **Claim.** Decision 8 parks a line 16 successor when it would change one
  of the ten blocked-names-question cases. The charter asks whether the
  resulting four-versus-eight split is harmful, and whether that gate
  reading is right.
- **Consequence.** Visible inconsistency, and the dead end on the 23 fields
  is still closed. On each recorded unanswered return and on
  `authority/none/required/answered`, 23 fields show the eight adopted
  sentences. Five fields show the four sale-boundary sentences: Form 1040
  lines 16 and 20, Schedule 3 lines 1 and 8, and Schedule 8812 worksheet A
  line 5. Those five are unchanged from v90. No blocked field on these
  returns has an empty question list. `form1040.line-25b` and `line-25d`
  are not in that blocked set.
- **Reproduction.** Re-ran the ten non-internal blocked-names-question
  cases on published v90 and on a scratch core whose only added member is
  the unpublished line 16 successor from `prototype.line16_body`. One case
  differs: `exception1_personal_loss_8949`. On that case the watched line
  values stay equal, line 16's missing list grows from the four sale names
  to the eight names, and sixteen fields keep their own missing lists while
  their question count grows from 4 to 8 (line 16 itself, lines 19, 20, 24,
  28, 32, 33, 34, 35a, 37, tax after credits, Schedule 3 lines 1 and 8, and
  Schedule 8812 lines 14, 17, and worksheet A line 5). The other nine cases
  match. That is the change the gate recorded, and it is why the successor
  stays unpublished.
- **Fix.** None in this unit. Parking is the prescribed stop. Answering the
  eight questions on the 23 fields, or entering the sale, publishes line 16
  at the hand value, so a filer who can see line 7a or line 15 is not stuck.
  A later line 16 successor has to preserve `exception1_personal_loss_8949`,
  or the owner reopens that case.

## Verified

1. **One state changes.** Undoing the single `else` at
   `rule.selected-preferential-base.v11.json:1126` and restoring v10's
   schema and version reproduces v10. The new `else` is `DEPENDENCY_ABSENT`
   with the eight names. Across the 18 authority cells, the four recorded
   returns (unanswered, sale entered, Exception 1 set to yes), the late
   sale-entered / exception-yes / sale-removed lists, and the ten
   blocked-names-question cases, the preferential-base disposition differs
   in exactly five act lists, all the same state: no sale and no Schedule D
   amount, conclusion `yes` (Schedule D required), boundary answered. v90
   is `inapplicable` with an empty missing list. v91 is `blocked`,
   `DEPENDENCY_ABSENT`, missing the eight names, value null. Every other
   cell keeps its disposition, code, missing list, and value. Open-boundary
   cells block on the family count names on both cores, before this `else`.
   Presentation lines and the kept publication values match on every list.
   On the four cells sampled for pins (the changed cell, a published
   carryover with Exception 1 holding, a published sale with Schedule D
   required, and `bnq/sd_path_b_unanswered`), pin counts and resolved input
   symbols match. Derived finding ids differ because each derived finding
   hashes the adopted package version. The eight names appear in no pin
   list. The other unequal pin lists have the same shape: the adoption pin
   moves from v90 to v91, asserted `demo.*` ids stay, and derived ids are
   replaced one for one.

2. **The eight names are the adopted questions.** Core v91 adopts one
   question citizen for each name: the two sale questions and the two
   Schedule D boundary questions at v1, three Exception 1 questions at v2,
   and `exception1.only-box2a-capital-gains` at v3. The sentences on the
   23 fields are those eight texts, one each. No field repeats a sentence.
   On the four recorded returns, seven of the eight facts are already
   asserted. The asserted "no" is the Exception 1 component that keeps
   Schedule D required; setting Exception 1 to yes is what reaches the
   hand. The asserted "yes" answers are restated, which is the same
   static missing-list mechanism line 16 already uses for its four names.
   `schedule-d-boundary.no-other-form8949-adjustments` is the name those
   four lists leave open, and it is the adopted yes/no question. Asking
   the already-answered sentences again does not publish a different number
   when the same answer is repeated.

3. **The dead end closes, and published lines stay put.** On a return with
   nothing to enter as a sale, setting Exception 1 to yes publishes every
   previously blocked line. `m_2a_only_exc1_only2a_no` reaches the box 2a
   hand (line 7a 1000, 16 3875). The two empty recorded returns and the
   late exception-yes return reach the wage hand (line 7a 0, 16 3875).
   Entering the short-term sale (proceeds 2000, basis 8000) on each
   recorded return and on the late blocked start reaches the sale hand
   (line 7a -3000, 16 3515, Schedule D line 21 3000). Those returns have
   no blocked field left. v90 publishes the same numbers on each of those
   paths. On the newly blocked preferential base, the lines that were
   blocked and questionless on v90 stay blocked, now with the eight
   questions, and Schedule D lines 3, 7, and 21 stay 0. No line that
   published a number on v90 becomes blocked or changes value.

4. **Line 16 stays parked, and the gate reading is right.** See N2.
   Published v91 does not change the ten blocked-names-question cases.

5. **The four `numbers_changed` lists do not hide a line value.** The
   classifier marks a pin `numbers_changed` when any non-sentence field
   differs, and it diffs only the watched projection lines. Re-ran ten
   lists on v90 and v91, including all four changed honest returns
   (`v82/m_2a_only_exc1_only2a_no/honest`,
   `v82/m_empty_exc1_nolosses_no/honest`,
   `v82/m_empty_exc1_only2a_no/honest`, `v82/t4_s1_removed/honest`) and
   `v81/case/a_8949_yes`, `v82/m_empty_q2_unanswered/honest`,
   `v83/track0/s0/b4_amount_no_answer`,
   `v83/returns/case/a_8949_yes/recorded`,
   `v84/authority/alc_closed_empty`, `v85/authority/alc_double_count`.
   Full presentation lines match on all ten. The only disposition-row
   change is `rule.selected-preferential-base`, from `inapplicable` to
   `blocked` with the eight names, and only on the four honest returns.
   Those four add the Exception 1 sentences to the page question set. The
   six others add and remove no question. `track1-replay.json` classes
   those four as `numbers_changed` with an empty line diff and
   `rows.selected-preferential-base` as the number field, which matches
   this re-run. The class name records the disposition row.

6. **Publication is add-only.** Registry v89 adds the v11 citizen and core
   v91, and changes no earlier row. Release v89 keeps every field of v88
   other than its version and registry hash, and that hash matches the
   v89 registry. Core v91 keeps every v90 member and replaces only
   `rule.selected-preferential-base`. The published v11 bytes equal
   `prototype.artifacts()`. The v91 covered-flag map and companion
   declaration equal v90. `git diff github/main...HEAD` over
   `packages/kernel`, `packages/derivation`, `packages/schemas`, and
   `packages/presentation` is empty. The loader diff is the v91 map entry
   and the v91 companion entry.

7. **Tests.** See N1. The package tests check the byte identity, the one
   replaced member, the add-only registry, and the v91 loader entries.

8. **Data safety.** `python3 tools/envelope_scan.py --range github/main..HEAD`
   exits 0 with no finding.

## Verdict

ready

N1 and N2 are notes. No blocking finding.
