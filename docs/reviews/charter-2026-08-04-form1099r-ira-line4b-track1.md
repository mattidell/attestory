# Owner-Launch Charter — Form 1099-R IRA Line 4b Track 1

Status: dispatched by owner authorization; Track 1 Builder in flight.

## Context Capsule

- Source ref and resolved launch commit: `origin/main` / `20a67ce162fe0e41d80dd0132619e24008beccf5`.
- Exact object: Track 1 of `docs/phases/engine-breadth/milestones/form1099r-ira-distributions-line4b.md`.
- Role: Builder, Luna, Medium/medium after the paper checkpoint.
- Branch/worktree: `milestone/form1099r-ira-distributions-line4b` /
  dedicated clean milestone worktree.
- Evidence ceiling: production implementation and focused integration tests;
  no new evaluator or product contract. Track 0 is paper-first and owner-held.
- Stop conditions: missing contract, unresolved 1099-R identity, any basis or
  special-treatment requirement, schema publication collision, or a rebase
  semantic-ledger loss. Stop and report; do not broaden the class.

## Work packet

Implement only the source-to-line-4b boundary:

- synthetic 2025 Form 1099-R statement facts for IRA/SEP/SIMPLE indicator,
  code 7, box 1, box 2a, and explicit box-2b-not-determined false state;
- logical statement identity, same-statement correction, distinct-statement
  aggregation, affirmative source closure, family horizon, and adopted mapping;
- fully-taxable line-4b content, with exact equality enforced; do not create a
  line-4a publication because the supported fully taxable class leaves line 4a
  blank;
- exact IRS citation citizens and source/lifecycle/blocked fixtures;
- focused tests for P1–P4 and N1–N4 in the milestone evidence matrix.

Do not implement line 9/package/release/presentation integration here except
for the minimum content pins and interfaces Track 2 consumes. Do not assign
future version numbers until the current-base inventory and required rebase
checkpoint are complete. Preserve every published byte.

Before writing, run `python3 tools/build_orientation_block.py --ref HEAD`,
verify the printed commit against Git, and echo scope, evidence ceiling, and
stop conditions. While iterating run only touched unittest modules. Run schema
registry tests when schemas or manifests change, plus `git diff --check`.

## Owner launch prompt

Paste this prompt into a fresh Luna builder context:

> Pick up the current task as the Track 1 Builder for the Form 1099-R IRA
> Line 4b milestone. Read `AGENTS.md`, run the orientation command with
> `--ref HEAD`, verify its commit, then read this charter and its cited sources.
> Echo your understood scope, evidence ceiling, and stop conditions before
> editing. Implement only the bounded 2025 IRA/SEP/SIMPLE, code-7, box-1 equals
> box-2a, explicit-box-2b state source path and line 4b, leaving line 4a blank
> for the fully taxable class. Use only synthetic demo data. Do not calculate
> basis, rollovers, Roth or special
> distributions; do not allocate versions before inventory; stop on any
> contract, collision, or semantic-ledger issue. Run focused tests and leave a
> clean committed Track 1 handoff.
