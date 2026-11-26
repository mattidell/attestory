# Review: same-label-members Track 1 (fresh)

Reviewer seat. Source: `milestone/same-label-members-2025` at `956aedc04`.
Built unit: `9b734b5d1`, `d47bcf0d6`, `de1451660` (after `9f6b57c75`).
Charter: `docs/reviews/same-label-members/charter-review.md`.

Verdict: **READY**. No blocking finding. Four low or informational
findings follow.

## What was verified

1. **Keying (Q1).** `_closure_question_reasons` adds to `member_facts` at
   exactly two sites (`presentation_projection.py:1029`, `:1039`), both now
   `(fact type, member subject keys)`. `_WalkFrame.absorb` and the memo
   carry the pairs as a set, so one member reached twice under the same keys
   gives one reason (unit control
   `test_the_same_member_reached_twice_is_asked_once`, passes on parent and
   built). Reasons are built once from `(label, sentence, keys)` and sorted,
   and the keys are never emitted. No path is still keyed by label. In
   core v107 every child roster subject uses the same `child=...,tax-year=...`
   keys, and a member-keyed fact type matches only keys that name its own
   entity key. So one entity cannot be reached under two key strings for
   the same question.
2. **Downstream (Q2).** The page (`citation-walk.v1.html:1448-1464`) and
   `tools/sale_page_observation.py:716` render each reason by index and
   remove no duplicates. `reasonIndices` for families and facts exclude
   `memberLabel` reasons (`:1105`). The validator (`:5925`) and
   `presentation-model.v3` have no uniqueness rule. Sorting adds only the
   unseen keys as a final tiebreak, so lines with distinct labels keep
   their order.
3. **ADR 0087 (Q3).** Decision 2, "one reason per member", is now met.
   `memberLabel` is unchanged, and no `memberOrdinal`, page wording or
   question link was added, which matches plan Decisions 1-3. Telling
   same-named members apart stays with Track 2 (ADR 0090, proposed).
4. **Tests and controls (Q4).** I checked out the parent `9f6b57c75` in a
   temporary worktree and added the new test files plus the Track 1
   `probe.py`. The unit file showed 6 failures there (4 test methods plus
   2 subtests of a fifth); the other 5 methods are controls and pass. In
   the live file, 6 tests failed on the parent, exactly the same-answer
   same-label cases; the 19 controls and page tests passed. On HEAD:
   unit and `test_eic_child_answers_walk.py` 25 passed; live 25 passed;
   mypy on the three files is clean. `replay.py` uses
   `recorded_replay.classify_full` with no expectations, and the swap
   covers only `_closure_question_reasons`. `replay-track1.json` shows
   recorded lists at 775/775 identical (691 success/success, 84
   error/error). The 9 of 23 probe lists that differ are exactly the
   same-label same-answer cases, with 323 differences = 111 `memberLabel`
   + 111 `sentence` + 101 `reasons@order`. These match the note.
5. **Evidence prose and data (Q5).** The text is plain and contains no
   absolute or temporary paths. Labels are `Demo Sam` and `Demo Alex`
   only. `python3 tools/envelope_scan.py --range github/main..HEAD` exits
   0 with no output.

## Findings

- **SLM-R1** (low, evidence)
  `tests/test_same_label_members_live.py:58-70`. The live test covers 6 of
  the 9 probe shapes that change. `kid2/AA/u17@1+u17@2`,
  `kid2/AA/dtb-another@1+dtb-another@2` and `mfj/kid2/AA/age@1+age@2` are
  evidenced only by the one-time replay. Failure scenario: a later change
  merges the under-17 or tie-breaker member reasons (a different walk
  branch, `reach_member` at `:1016-1030` through a subject publisher), or
  merges them on a joint return. No standing test would fail. Repair: add
  the three cases to `SAME_LABEL`.
- **SLM-R2** (info, prose)
  `same-label-members-evidence/track1.md:44`. The note says "Six of them
  fail on the pre-Track-1 projection" right after "10 tests". In fact 5 of
  the 10 test methods fail; the sixth failure is a second subtest. A reader
  could take this to mean 6 of 10 methods. Repair: say "5 tests (6 cases
  with subtests)".
- **SLM-R3** (info, pre-existing, not changed by this track)
  `presentation_projection.py:1461-1484` (`_reasons_beside`) and `:1385`
  (`_finalize_question_references`). Both match closure reasons only by
  `sentence`. On a selection-attached line, a member reason whose sentence
  equals a selection reason is dropped. A member reason whose sentence
  equals a linked fact question would get that question's
  `reasonIndices`. Track 1 changes how many such reasons there are, not
  this behavior, and no v107 case reaches it (replay identical). Flagged
  for Track 2, which adds a member field to the reason.
- **SLM-R4** (info, meaning; expected under Decision 2)
  `presentation_projection.py:1070-1073`. Member reasons are sorted by
  label, then sentence. Two "Demo Sam" members who each miss two answers
  show Sam: age, Sam: age, Sam: parent, Sam: parent, so the filer cannot
  pair the answers with a person. This is the gap ADR 0090 addresses.
  Track 2 should decide whether to order reasons by member as well as add
  the ordinal.

## Gates

Draft PR #315 is at head `956aedc04`. `verify` has not run on it (draft).
This review does not stand in for the gate. The builder's full-suite count
is self-reported and is not evidence of record.
