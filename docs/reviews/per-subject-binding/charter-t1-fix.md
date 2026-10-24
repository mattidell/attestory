# Track 1 — bind per-subject inputs only from their own subject

Audience: Builder.

Plan: `docs/phases/engineering-health/milestones/per-subject-binding.md`,
"P0 result" and "Contract". Evidence and probes:
`per-subject-binding-evidence/`. The worktree and branch are supplied at
launch. Commit on that branch; do not push.

## Build

1. **Tests first.** In `tests/test_per_subject_binding.py`, add the contract
   item 4 cases through the real coordinator, using the P0 probes' setups:
   two Form 1098 statements on core v54 where only the first has
   circumstance answers (the second statement's
   `tax.us.2025.rule.f1098-residence-interest-reason` must block
   `DEPENDENCY_ABSENT` naming its own missing answers, and pin none of the
   first statement's findings); two EIC children in the flat shape (the
   child without a residency answer blocks); and a per-subject rule that
   reads a return-level input such as filing status (still read). Commit them
   as failing tests marked `xfail(strict=True)` with the reason.
2. **The fix (contract item 1).** Generalize per-subject input discovery in
   `packages/derivation/live.py` so a required input whose fact type shares
   identity keys with a subject-scoped rule's subject is emitted per subject,
   replacing the Form 1099-K-only path without changing its behaviour. In
   `packages/derivation/subject_dispatch.py`, such an input binds only from
   the subject's scope; when absent it blocks, never falling through to
   `run.symbols`. Return-level inputs keep the run-wide binding. Keep the
   change small and comment the rule the code enforces. Remove the `xfail`
   marks.
3. **No content change.** No file under `packages/content/` changes.

## Before handing off

Run the new module, every `tests/test_f1098_*`, `tests/test_f1099k_*`,
`tests/test_sli_*` and EIC module, then the **full suite** (`pytest`) and
`python3 -m mypy`, because this is substrate work. Every golden must be
unchanged; if any test's expectation changes, stop and report it with why.
`python3 tools/governance_lint.py` and `python3 tools/envelope_scan.py
--range origin/main..HEAD`. Synthetic data only; no absolute local paths in
committed files; never `--no-verify`. Commit under the collaboration-commit
lock (retry every 10 seconds up to 5 minutes; never remove a lock you did not
create), explicit paths, no trailers: one commit for the failing tests, one
for the fix.

## Stop conditions

A golden or existing test expectation changes; the fix needs a content,
schema or rule-language change; or a return-level input stops binding.

## Return

Commit SHAs, lines changed per file, test counts including the full suite
and mypy, and any test whose expectation changed.
