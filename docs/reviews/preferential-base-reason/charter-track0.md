# Charter: Track 0 adversarial closure of the lines below line 16

Role: Builder. Source HEAD on milestone/preferential-base-reason-2025.
Plan: docs/phases/engine-breadth/milestones/preferential-base-reason.md
(read it whole, including the P0 result and Decisions 1-6). Evidence:
preferential-base-reason-evidence/ (start with p0.md). Gate:
`PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate" (read that
section and its closing paragraphs whole). Precedent:
blocked-names-question-evidence/track0-closure.md and its track0.py. Do
not read governance.

## Scope

Every claim comes from a `live_coordinate_run` output saved in a
committed JSON file and named by case id, on published v90 and the P0
scratch v91. Hand values come from the 2025 instructions, never from what
the prototype publishes. Never work under packages/.

1. **Authority-lifecycle table** for the successor's guard: every
   combination of activity (none, a sale, a Schedule D amount without a
   sale) with the Schedule D conclusion (no, required, open) and the
   boundary answers (open, answered). For each: v10 result, v11 result,
   and which is right. Any combination where v11 differs from v10 other
   than "required, no activity" is a FAIL.
2. **Empty/nonempty matrix** over the four recorded returns and
   synthetic neighbours: Exception 1 "no" on each of its two questions,
   with box 2a only, with nothing, with a capital-loss carryover, with a
   Schedule D amount from another source. Unanswered: every blocked
   filer-visible field names a question (list any that does not).
   Answered truthfully: hand values.
3. **Are the four names enough (Decision 6).** For the filer with no sale
   to enter (`t4_s1_removed`, and a mistaken Exception 1 "no"): answer
   each of the four named questions every truthful way and record whether
   anything unblocks. Then show what does unblock the return. Say whether
   the block can truthfully also name the Exception 1 question (is there
   a question citizen for it, does the projection resolve the name, and
   does naming it ask a computing return anything new), prototype that
   variant on scratch, and recommend one. Say whether line 16 v8 has the
   same gap.
4. **Late-member traces:** a sale entered after the block (the block
   clears and numbers match the hand); the sale removed again; Exception
   1 changed from no to yes with no sale.
5. **Claim reuse:** the successor adds no read, pin or scheduling
   dependency; every other v90 member composes unchanged; a v90 workspace
   opened on v91 needs no new answer.
6. **Neighbour table:** reuse the P0 replay part file (keep it outside
   the repo) if the recommended variant is the P0 scratch; if item 3
   changes the successor, replay again with
   `python3 tools/recorded_replay.py` in parallel (CPU count minus one),
   in the foreground, and classify every change. Report wall time.
7. **Integration surface:** on the four recorded returns and two
   neighbours, the page-level question list and each field's questions on
   v90 and v91; no question appears twice on a field; no field that
   computed on v90 is blocked on v91.

Do not run the full test suite or mypy. Run every command in the
foreground and do not end your turn while a command is running. Stop and
report if anything needs an engine, schema, projection, page or kernel
change.

## Deliverable

preferential-base-reason-evidence/track0-closure.md and track0.py with
its `track0-*.json` outputs, and a "Track 0 adversarial closure" section
in the plan: each table PASS or FAIL with counts and case ids, the item 3
recommendation, and "Known limitations affecting correctness".

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
  if held, retry every 10 s up to 5 min.
- Never --no-verify or a bare git stash. Foreground only. No push, no
  spawn.
