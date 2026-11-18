# Charter: fresh review of replays compare the whole saved return

Role: Reviewer, fresh context. Source HEAD on
milestone/full-surface-replay-2025. Plan:
docs/phases/engine-breadth/milestones/full-surface-replay.md (read it
whole). Evidence: full-surface-replay-evidence/track1.md, its scripts
and JSON. Range: `github/main..HEAD`. Read
docs/reviews/line16-names/review.md (L16-R1) for the gap this closes.
Do not read governance.

## Questions

1. **Completeness.** Does the snapshot hold every saved value, status,
   text, question and report row a later milestone would claim
   unchanged? Construct a change to the saved model or report that the
   snapshot or diff does not see (try the exclusions track1.md names:
   aliased finding hashes, order of hash-keyed items, dict key order,
   the rendered page). Say whether each blind spot matters.
2. **Strictness of expectations.** Can an expectation accept more than
   it names (Decision 1)? In particular, can `text_change`, matching
   page, attachment and model kinds, accept an unrelated sentence
   change, or a change on a field it was not meant for? Can an unused
   expectation hide anything?
3. **Controls.** Do the controls mutate before the snapshot, as L16-R1
   asked, and would each fail if the corresponding part of the
   snapshot or diff were removed? Mutate the tool in memory to check;
   do not commit mutations.
4. **Demonstrations.** Are the v96-v96 and v95-v96 runs what they claim?
   Was widening `text_change` after the first failing run a tool fix,
   or did it loosen the check?
5. **Compatibility.** Do existing callers of the old pin and classify
   functions behave unchanged?

## Output

docs/reviews/full-surface-replay/review.md: a verdict (READY, READY
with notes, or NOT READY), numbered findings (FSR-R1 …) each with
file:line, a concrete failure scenario and a severity, and what you ran.
Commit it under `$(git rev-parse --git-dir)/collaboration-commit.lock`
(mkdir … rmdir), staging that one path. No code edits, no push, no
spawn. Synthetic demo.* only; no absolute paths in committed files.
