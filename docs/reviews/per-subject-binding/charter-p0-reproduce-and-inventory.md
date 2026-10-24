# P0 — reproduce the cross-subject binding and inventory shipped rules

Audience: Builder.

Plan: `docs/phases/engineering-health/milestones/per-subject-binding.md`.
The worktree and branch are supplied at launch. Commit on that branch; do
not push. P0 changes no production code, content, fixture or existing test.

## Deliverables

Write `docs/phases/engineering-health/milestones/per-subject-binding-evidence/p0-reproduce-and-inventory.md`
and probes beside it. Tables and bullets; every claim backed by a command you
ran, and every number pasted from its output.

1. **Smallest failing case.** Start from
   `docs/phases/engine-breadth/milestones/eic-qualifying-children-evidence/child_dispatch_probe.py`
   (variant `flat-alone`). Reduce it to the smallest synthetic case that binds
   one subject's evaluation to another subject's answer, or to a run-wide
   value it should not read. Name the exact lines in
   `packages/derivation/subject_dispatch.py` (and any caller in `runner.py`
   or `live.py`) responsible: the shared-name join in `_scope`, the run-wide
   fallback through `run.symbols` / `run.symbol_pin`, or something else.
   Show the pins the wrong evaluation records.
2. **Inventory.** For every shipped rule with a `subject` that is a member of
   any package on `main` (list them from the packages, not from file names),
   record: package versions that adopt it; its subject type; each required
   input and how it is bound on the live path (the subject itself, a
   declared `joined` type, a shared-name scoped type, a run-wide symbol, a
   parameter, a declared default). Mark each rule exposed or not, with the
   reason.
3. **Real effect.** For each exposed rule, build the smallest synthetic case
   on the latest package that adopts it (two subjects of its family, one
   answer missing or different) and run it through the real coordinator.
   Record whether a result is wrong today, and how.
4. **Fix options.** Propose at most two fixes, for example: a required input
   that names a collected per-subject fact type must bind from this
   subject's scope or block, never from the run-wide environment; or a
   shared-name join that finds no row for this subject blocks. For each, say
   which existing tests and goldens it changes (run them against a local,
   uncommitted patch and revert it), whether any rule language or schema
   change is needed, and how return-level inputs keep working.
5. **Recommendation** with its cost in files and tests.

## Rules

- Synthetic data only. No absolute local paths in committed files. Never
  commit with `--no-verify`.
- Do not read `docs/governance/`. Edit no production code, published content,
  fixture or existing test in a commit; experimental patches stay
  uncommitted and are reverted before you commit.
- Commit under the lock (`mkdir "$(git rev-parse --git-path
  collaboration-commit.lock)"`; retry every 10 seconds up to 5 minutes if
  held; never remove a lock you did not create), explicit paths, no
  trailers. Commit each deliverable as it is done.
- You may run the full suite once, against an uncommitted patch, for
  deliverable 4.

## Stop conditions

The fix needs a rule-language or schema change; or a shipped result is wrong
today (report it immediately with the case, then continue the inventory).

## Return

Commit SHAs, evidence path, the failing code path, the exposed rules and any
wrong shipped result, the recommended fix and what it changes.
