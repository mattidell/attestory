# Track 7 — interruption safety of multi-record saves

Audience: Foreman, reviewer.

## 1. Readiness: what an interruption leaves today

Read before any Track 7 code. Each relationship save appends
its acts one `ActLog.append` at a time. An interruption after an act leaves
the acts before it.

- **Usable:** the rules read the state before the save, or the completed save.
- **Refused:** line 21 blocks with a named reason, and is no more favorable
  than before the save or than the completed save.
- **Misleading:** the rules read a different answer than the person gave, or
  a deduction gets through.

"Probe" rows were run with `temp/track7/probe.py` (ignored). The probe used
the Track 5 synthetic return, interrupted after act *k*, recovered fresh and
ran `live_coordinate_run`. The other rows come from reading the code.

| Writer | Acts in order | After each act | Rating |
| --- | --- | --- | --- |
| `record_submission_durably` (`save_review`) | evidence; per answered clause a contribution and an assertion (yes, or with bundle v2 a no / cannot-tell outcome or a statement doubt); a retraction of each earlier outcome or doubt it replaces | Before the first assertion: the before state. Financing written, inclusion not: no loan link. Yes written, earlier outcome not ended: a current unresolved, withdrawn or doubt fact blocks, and a current denied fact reads as the completed yes | usable / refused |
| `_withdraw_with_outcome_durably` (v2 withdraw) | evidence, contribution, withdrawn outcome, retractions of earlier outcomes, retraction of the affirmation | The yes and the withdrawn fact are both current, so the pair blocks | usable / refused |
| `_answer_with_outcome_durably`, cannot-tell | evidence, contribution, unresolved outcome, retractions, retraction of the affirmation | The yes and the unresolved fact are both current, so the pair blocks | usable / refused |
| `_answer_with_outcome_durably`, **no** | evidence, contribution, denied outcome, retractions, retraction of the affirmation | The yes and the denied fact are both current. No rule reads a denial as blocking, so the yes counts. Probe, inclusion and financing: after the denied assertion line 21 still publishes **1500**; the completed save blocks | **misleading** |
| `answer_relationship_claim_durably`, v1 path | retraction of the affirmation; evidence; for cannot-tell, a contribution and the sample unresolved fact | After the retraction, the link is absent and no answer is saved. The rules read this the same as the completed v1 answer: v1 writes nothing a rule reads, and no rule reads the sample unresolved type. A v1 workspace cannot record the two answers, so its statement is never supported | usable (carried item 2) |
| `_answer_unresolved_inclusion_no_durably`, `_record_unresolved_inclusion_durably` (v1) | retraction of the sample fact, then evidence; or a contribution and the sample assertion | Only the sample type changes, and no rule reads it | usable |
| `correct_relationship_claim_durably`, affirmation current | retraction of the predecessor; evidence; contribution; successor yes | After the retraction the pair is absent and the statement has no loan link. If that link was the return's only loan-link record and the old yes/no answers are present, line 21 takes the old path and deducts. Before the save, and after the completed save, both paths are present and it blocks | **misleading** (code reading) |
| `correct_relationship_claim_durably`, outcome current | evidence, contribution, successor yes, retraction of the outcome | Same as the first row | usable / refused |
| `_record_borrowing_answer_durably` (record and correct) | evidence, contribution, answer | The before state until the answer is saved. In a v1 workspace it is refused before any act, so the workspace is stuck (carried item 1) | usable |
| `_append_statement_source_correction_durably` | corrected-source evidence, contribution, box 1 assertion | The before state until the assertion. If the new-write step refuses the assertion, the evidence and contribution stay in the log (carried item 3) | usable, leaves litter |
| `apply_statement_correction_review`, amount-only | scope evidence, then the three source-correction acts | The before state until the corrected box 1 is saved | usable |
| `apply_statement_correction_review`, **inclusion-added** | scope evidence; the three source-correction acts; then the added pair's evidence, contribution and yes | After the corrected box 1 and before the added yes, the statement has the new amount and only its earlier loan. Probe: line 21 publishes **2200** after acts 4–6. Before the save it published 1500; the completed save blocks with two loans | **misleading** |
| `apply_statement_correction_review`, **inclusion-removed** (v2) | the "no" answer row above, then the three source-correction acts | After the denied fact, the "no" row applies. After the retraction and before the corrected box 1, the old amount stands with only the remaining loan. Probe: line 21 publishes **2200** after acts 4–6. Before the save it blocked with two loans; the completed save publishes 1500 | **misleading** |
| `apply_statement_correction_review`, inclusion-uncertain (v2) | the cannot-tell answer row, then the three source-correction acts | An unresolved fact is current throughout, so the statement blocks | refused |
| `apply_statement_correction_review`, v1 removed or uncertain | the v1 answer row, then the three source-correction acts | The v1 workspace's statement is never supported | refused |
| Any writer, **torn last line** | — | Recovery sets the partial line aside and reads the same state as a clean stop at that act. The next relationship save is then refused ("ActLog has an incomplete tail"), so the workspace is stuck. Probe: a writer that calls `ActLog.append` directly writes onto the torn bytes, and the next read raises `ActLogCorruption` at that line | refused, stuck; **corrupts** on a direct append |

Single-act writers are outside this table: `introduce_borrowing_reference_durably`,
the v1 withdrawal, and `withdraw_borrowing_answer_durably`.

## 2. Planned design

**One save, one atomic write.** `ActLog` gains `append_batch(acts, expected_revision)`.
It validates every act and runs the ADR 0077 Part 5 new-write step on each
act against the acts staged before it, all before anything is written. It
then writes the existing log plus the new lines to a pending file beside
`acts.jsonl`, fsyncs it, and renames it over the log. An interruption
before the rename leaves the log byte for byte as it was. An interruption
after the rename leaves the whole save. Each relationship writer, including
the composite statement-correction review, stages its whole save and commits
it with one `append_batch`.

This choice is per writer, with one outcome for all of them: an interrupted
save is refused cleanly, and the next read sees the state before the save.
It is smaller than the alternatives:

- **Reordering acts** cannot close the misleading rows. Ending the yes before
  writing a "no" loses the loan-link presence that keeps an old-and-new return
  blocked. Writing the added yes before the corrected box 1 lets a statement
  that had no loan deduct the old amount.
- **A clean refusal on the next read** would need the replay applicability
  marker to mean "save interrupted". ADR 0077 Part 5 defines that marker as
  an unreviewed same-identity change of the statement. Widening it changes an
  accepted ADR, which is a stop condition. The marker also cannot reach
  financing links.
- **Continuation** would need every writer to reconstruct the rest of an
  unfinished save from the log, case by case.

The batch also closes carried item 3. If the new-write step refuses any act,
nothing is written. The batch refuses a log with an uncommitted tail instead
of writing onto it. The same change to `ActLog.append` was planned here but
dropped during the build; see section 3, open question 1.

Carried item 1: when the person first answers one of the two borrowing
questions in a v1 workspace, the same atomic save adopts relationship bundle
v2 first. Carried item 2: the v1 window rated usable above disappears anyway,
because the retraction and the answer are now one write.

## 3. Built

Implemented on this branch:

| Commit | What |
| --- | --- |
| Readiness | This readiness table |
| Failing tests | Failing tests: every multi-act writer interrupted after each act |
| Batch append | `ActLog.append_batch` |
| Relationship writers | Answers, withdrawals, claim corrections and borrowing answers save as one batch; v2 adoption on the first borrowing answer |
| Statement correction | The reviewed statement correction saves as one batch; the sweep replays each writer's batch |

### Choice per writer

Every writer in section 1 now stages its whole save, then commits it with one
`append_batch`. That includes the v1 answer path, and the composite statement
correction, which stages its scope answer and its corrected source together.
An interrupted save is refused cleanly: recovery reads the state before the
save. The reasons:

- **Answer no, inclusion and financing:** the denied fact and the end of the
  yes are one write, so the yes can no longer count beside a no.
- **Claim correction:** the predecessor's end and its successor are one
  write, so the loan-link path cannot drop out between them.
- **Inclusion added or removed:** the corrected box 1 and the inclusion change
  are one write. Neither the new amount with the old loans nor the old amount
  with the new loans can be read.
- **Rows already usable or refused:** they become all-or-nothing as well,
  because one mechanism for every writer is smaller than keeping two.

`append` is unchanged. Single-act writers still use it:
`introduce_borrowing_reference_durably`, the v1 withdrawal, and
`withdraw_borrowing_answer_durably`.

### Carried items

1. **Bundle v2 on the first answer.** In a workspace whose relationship
   vocabulary is v1, the first borrowing answer's save is the v2
   `bundle-adoption`, then the answer's evidence, contribution and finding.
   It is adopted once. A workspace that never adopted the relationship bundle
   still refuses. A v1 history that holds a no, a cannot-tell or a withdrawal
   is refused with a reason and is not upgraded: v1 kept no current fact for
   those answers, so under v2 they would read as never said.
2. **The v1 answer window.** It was rated usable: the rules read it the same
   as the completed v1 answer. It no longer exists, because the retraction,
   the answer and the sample unresolved status are one write.
3. **Refusal by the new-write step.** `append_batch` runs the ADR 0077 Part 5
   step on each act against the acts staged before it, before writing. A
   correction refused at its box 1 act leaves no evidence or contribution
   behind.

### Cases and results

`tests/test_sli_track7_interruption_safety.py` runs 15 writer sweeps. Each
starts from the Track 5 synthetic return, saved and recovered fresh. The
writer runs once, crashing on its last act with a torn line, and its save
must be exactly one `append_batch`. That batch is then committed again from
the same starting log, with a crash after each act, torn and clean. After
every crash the recovered log is the log from before the save, with no
uncommitted tail. Line 21 and each statement's standing, run through
`live_coordinate_run` on both runners, are no more favorable than before the
save. The same save then completes from the recovered log, even when the
crash's pending file is still beside it.

| Sweep | Before | Completed save |
| --- | --- | --- |
| Both links in one review | blocked | 1500 |
| Yes after a withdrawn link | blocked | 1500 |
| No, inclusion | 1500 | blocked |
| No, financing | 1500 | blocked |
| Cannot tell, inclusion | 1500 | blocked |
| Withdraw, inclusion | 1500 | blocked |
| Correct the only link beside old answers | blocked | blocked |
| Answer a borrowing question | blocked | 1500 |
| Correct a borrowing answer | 1500 | blocked |
| First answer in a v1 workspace (adopts v2) | blocked | blocked, second answer missing |
| Amount-only correction | 1500 | 1000 |
| Correction adding a loan | 1500 | blocked |
| Correction removing a loan | blocked | 1500 |
| Correction with an uncertain loan | 1500 | blocked |
| v1 no, inclusion | blocked | blocked |

Other cases:

- A v1 workspace answers both questions and line 21 publishes 1500.
- v1 history with a withdrawal, or with a no, refuses the first answer and
  leaves the log byte-identical.
- A workspace without the relationship bundle still refuses.
- A correction refused by the new-write step leaves the log byte-identical,
  and the bound correction is then admitted.
- A workspace with no relationship claims writes act by act through `append`,
  never batches, and line 21 publishes 1500.
- `tests/test_act_log_batch.py`, 11 tests, covers the log-level batch:
  - the bytes equal one append per act;
  - a crash at every line, torn and clean, or before the rename leaves the
    log as it was;
  - a leftover pending file is harmless;
  - a bad act, a stale revision, a revision gap, a duplicate id, an empty
    batch, an uncommitted tail, a read-only log and a log changed during the
    save are each refused without writing.

Against the writers before Track 7, the first version of the sweep in
The failing tests failed 129 subtests before the fix. Every interrupted save left part of itself.
Three cases published a more favorable line 21:

- correcting the only link beside old answers: 1500 over blocked;
- a correction adding a loan: 2200 over 1500;
- a correction removing a loan: 2200 over blocked.

A torn line stranded the next save.

Four test files that relied on partial saves were updated:

- Track 3: an interrupted answer or withdrawal now saves nothing, and a
  v1-only workspace adopts v2.
- Track 16: the source change is injected before the save's single write.
- Track 18: a failed answer write saves nothing, and the intermediate checks
  read the log just before the save.

### Verification

All runs were on the final Track 7 code.

- Tests written first: the failing tests failed as described above, with
  `ActLog.append_batch` absent.
- The Track 7 file passed: 20 tests, 134 subtests, in 131 s at `-n 8`.
- The relationship files plus the Track 5 and Track 6 files and the act log
  and E6.1 tests passed: all `tests/test_sli_*.py` and
  `tests/test_scoped_supersession_new_write_step.py`, with
  `tests/test_act_log.py`, `tests/test_act_log_batch.py` and
  `tests/conformance/test_e6_1_interruption_safety.py`. That is 376 passed
  and 736 subtests.
- The full suite, `pytest` with `-n auto`, gave **2668 passed, 20 skipped**,
  exit 0, in 517.57 s.
- Repository `python3 -m mypy`: no issues in 321 source files.
- `python3 tools/governance_lint.py`: conformant.
- No fixture, schema, package or release file changed.

### Open questions

1. **`ActLog.append` writes onto an uncommitted tail.** The probe confirmed
   it: the next read raises `ActLogCorruption`. Track 7 leaves `append`
   alone, because a workspace with no relationship claims must not behave
   differently, and every relationship batch refuses a torn log. A kernel fix
   is a separate decision: refuse, or set the tail aside. Until then, a torn
   single-act relationship write leaves the workspace refusing relationship
   saves.
2. **v1 history with a no, cannot tell or withdrawal** is refused rather than
   upgraded. Upgrading it would mean writing v2 facts reconstructed from v1
   evidence.
3. **A completed v1 "no" in a v1 workspace drops loan-link presence.** If old
   answers are present, the old path then deducts; v2 keeps the denial
   present and blocks. This gap was there before Track 7 and has nothing to
   do with interruption.
4. **Single writer.** `append_batch` refuses a log that grew while the save
   was being written. Like the revision check in `append`, it does not
   exclude a writer that races the final rename.
5. **Pending file.** After a crash, `acts.jsonl.pending` can stay beside the
   log until the next batch overwrites it. Anything that copies a workspace
   directory copies it too.
6. **Cost.** The Track 7 file takes about 2 minutes at `-n 8`, and its
   slowest test about 80 seconds.
