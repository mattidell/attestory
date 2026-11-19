# Charter: fresh review of Chrome cleanup does not hang CI

Role: Reviewer, fresh context. Source HEAD on
milestone/chrome-cleanup-hang-2025. Plan:
docs/phases/engine-breadth/milestones/chrome-cleanup-hang.md (read it
whole). Evidence: chrome-cleanup-hang-evidence/track1.md. Range:
`github/main..HEAD`. Do not read governance.

## Questions

1. **Mechanism.** Does the reproduction show the CI failure's
   mechanism (`cleanup-complete`, then no exit, `browser-cleanup-failed`),
   or a different hang that happens to look similar?
2. **Process ownership.** Does the harness now end every process it
   starts, and only those? Check group handling on macOS and Linux, the
   exit hooks (do they override or chain with existing SIGINT/SIGTERM
   handlers in run.mjs and other entry points?), and the SIGKILL gap
   Decision 2 accepts. Could a group kill ever reach a process the
   harness did not start?
3. **Honesty.** With a profile that cannot be removed, or a group that
   will not die, does the observer still fail with the right reason and
   exit code, promptly? Is any failure now hidden (Decision 1: no
   timeout or retry that hides a real failure; is the bounded profile
   retry within that)?
4. **Tests.** Do the new Node tests fail on the old code and pass on
   the new, and would they fail if the group kill, the stream destroy
   or the prompt exit were removed? Mutate in a scratch copy; do not
   commit mutations. Is the parallel-run failure of
   real-chrome-repair.test.mjs truly pre-existing?

## Output

docs/reviews/chrome-cleanup-hang/review.md: a verdict (READY, READY
with notes, or NOT READY), numbered findings (CCH-R1 …) each with
file:line, a concrete failure scenario and a severity, and what you
ran. Commit it under `$(git rev-parse --git-dir)/collaboration-commit.lock`
(mkdir … rmdir), staging that one path. No code edits, no push, no
spawn. Leave no Chrome or fake-Chrome processes running. No absolute
paths in committed files.
