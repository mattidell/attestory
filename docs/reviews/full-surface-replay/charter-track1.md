# Charter: Track 1 of replays compare the whole saved return

Role: Builder. Source HEAD on milestone/full-surface-replay-2025.
Plan: docs/phases/engine-breadth/milestones/full-surface-replay.md (read
it whole, especially Decision 1). Read: tools/recorded_replay.py and
tests/test_recorded_replay.py; docs/reviews/line16-names/review.md
(L16-R1 in full); precedents
plain-line-texts-evidence/track1_replay.py (strict classifier and
mutation controls), sale-reasons-plain-evidence/srp_replay.py, and
rust-kernel-experiment-evidence/track1_dump.py (complete-output hashes).
Do not read governance.

## Scope

1. **Snapshot.** Add to `tools/recorded_replay.py` a full-surface
   snapshot of one run: every saved page field (identity, value,
   disposition, plain and explain text, blocked reasons, questions,
   categorical render text, any other model string), every report row
   with its full identity (artifact, symbol, disposition, code, missing
   names, value), and the error class and message for a list that
   fails. Derive it from the saved model and report, not from a list of
   watched lines. Say what, if anything, of the saved output it still
   leaves out and why (for example run-specific paths, which it masks).
2. **Diff and classify.** Compare two snapshots and return every
   difference as a typed record (kind, identity, attribute, before,
   after). A caller passes expectations per Decision 1; any difference
   not expected fails the list. Keep the existing pin and classify
   functions working unchanged.
3. **Controls.** Controls mutate the saved model or report before the
   snapshot is taken, as L16-R1 did: at least a changed field value
   outside any watched line (line 12e), an unwatched report row's code,
   a removed and an added field, a changed disposition, a changed
   missing name, a changed question, and a changed sentence that is not
   expected. Each must fail; an expected sentence change must pass.
4. **Demonstrate.** Run all 775 recorded lists through the parallel
   replay (CPU count minus one) for (a) v96 against v96, all identical,
   and (b) v95 against v96, with plain-line-texts' expected sentence
   changes declared: report how many lists pass and list every
   unexpected difference. If (b) finds differences plain-line-texts did
   not report, record them exactly and stop short of judging them; the
   foreman decides. Report wall time.
5. **Tests.** Fast tests for the diff and classifier on synthetic
   snapshots, and the controls on one real saved output (honestly
   marked live if slow).

## Deliverables

Code in tools/ and tests/; in
docs/phases/engine-breadth/milestones/full-surface-replay-evidence/:
track1.md (what the snapshot holds and leaves out, the expectation
interface with an example, controls, both demonstration runs), scripts
and small JSON summaries. Update the tool's docstring with usage. Run
`pytest -m "not live"` plus the new and changed test modules, and
`python3 -m mypy`; report the lines. No edits under packages/.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Nothing over 200 KB committed.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn.
