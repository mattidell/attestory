# Track 1: a declared question for each missing amount

Role: Builder. Source HEAD on milestone/missing-input-questions-2025.
Plan: docs/phases/engine-breadth/milestones/missing-input-questions.md
(P0 result, Decisions, Tracks). Design and cases E1-E11:
missing-input-questions-evidence/p0-survey-and-design.md. Read the
closure-questions plan for the v37 admission precedent. Do not read
governance or unrelated proposals.

Build, as P0 designed and the plan decided:

1. Schema intent first: append `propose` events for `input-question.v1` and
   `artifact-package.v39` on the `milestone-schema-ledger` branch, per
   docs/process/concurrent-work.md ("Schema-intent ledger"). Use a temporary
   worktree under your own hidden `/.<agent-name>/` directory on a
   `temp/milestone/missing-input-questions-ledger` branch only if you cannot
   commit to that branch otherwise; push it to `github`; remove the temporary
   worktree and branch after. Then `publish` events once the schemas exist.
2. `input-question.v1` (blank question refused) and `artifact-package.v39`,
   new files, registered with `write_manifest`; inspect that the manifest
   diff only adds.
3. Admission at the points the closure-question schema needed
   (`package_validation.py`, `authorization_closure.py`,
   `packages/tax/loader.py`, `live.py`), each exact-version list extended,
   not loosened.
4. Eight `input-question` citizens with the plan's wording verbatim.
5. Generalise `_closure_question_reasons` as designed; earlier packages
   return exactly today's reasons.
6. Core v72, registry v70, release v70 with `tools/package_successor.py`;
   the v72 companion entry in `packages/tax/loader.py`.
7. Tests through the real coordinator and projection: E1-E11, mixed
   ordering, a blank question refused, and v68-v71 presentation models
   byte-identical before and after for the same returns.

Only successors; never edit a published schema, citizen, package or
checksum. `packages/derivation/` is touched: run `python -m mypy`, the new
tests, `tests/test_schema_registry.py`, the closure-question tests and the
FULL suite before handoff. Synthetic demo.* only; no absolute paths
committed. Commit with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir) every
time; never --no-verify; never bare git stash. Foreground commands only. No
push of the milestone branch, no spawn. Stop on any kernel change or any
need to alter a published file.
