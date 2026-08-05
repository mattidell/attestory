# Owner-Launch Charter — 2025 SSA-1099 Benefits Line 6 Track 1

Audience: Builder

Status: chartered for owner launch after Track 0 ratification.

## Context Capsule

- Source ref and resolved launch commit: `origin/main` /
  `9cecf30ea7eca62aefe2462620ea063345e72cae` (re-resolve at launch).
- Exact object: Track 1 of
  `docs/phases/engine-breadth/milestones/ssa1099-benefits-line6.md`.
- Role: Builder, owner-launched, medium/high after Track 0 settles the
  statement and component boundaries.
- Evidence ceiling: bounded synthetic source-family implementation and focused
  integration tests; no new evaluator, generic substrate, or product contract.
- Stop conditions: unresolved box/recipient identity, ambiguous correction or
  duplicate semantics, unsupported RRB/foreign/lump-sum/withholding path,
  schema or package collision, or any semantic-ledger loss on rebase.

## Work packet

Implement only the source side of the bounded ordinary SSA-1099 path:

- synthetic 2025 statement facts for recipient identity, claim/statement
  identity, correction state, boxes 3, 4, 5, and the guarded box-6 state;
- exact box-3/4/5 reconciliation and nonnegative boundary;
- the source family, current family horizon, closure mapping, closure-backed
  zero behavior, and correction/duplicate/late-member lifecycle;
- taxpayer/spouse subject handling for joint returns and honest rejection of a
  statement belonging to another taxpayer;
- the minimum exact IRS citation citizens and source/lifecycle/blocked tests
  Track 2 consumes.

Do not implement the worksheet, line 6a/6b arithmetic, line 9 successor,
package/release/adoption integration, or presentation except for the minimum
content pins and interfaces. Do not reserve future versions before re-running
the current-base inventory. Use only synthetic `demo.*` values and ids.

## Focused case packet

| Case | Expected result |
| --- | --- |
| One valid SSA-1099 | Current member, box reconciliation, and family closure are accepted. |
| Two distinct statements/claims | Both members remain distinct and available for aggregation. |
| Taxpayer and spouse on joint return | Subjects remain authoritative and distinct; no name/SSN fixture leakage. |
| Same logical statement corrected | Same identity supersedes the old member; no double count. |
| Duplicate original or conflicting correction | Admission rejects or blocks deterministically. |
| Late member after closure | Family horizon advances; old closure and consumers displace. |
| Box 5 = box 3 − box 4, including zero | Accepted. |
| Box 5 mismatch, negative, repayment over benefit, RRB/SSA-1042S, other taxpayer, lump sum, or positive box 6 | Ordinary family path blocks honestly. |

Before editing, run `python3 tools/build_orientation_block.py --ref HEAD`,
verify its commit against Git, and echo scope, evidence ceiling, and stop
conditions. While iterating run only touched unittest modules; run schema
registry tests when schemas/manifests change, plus `git diff --check`.

## Owner launch prompt

Paste into a fresh owner-launched Builder context:

> Pick up the current task as Track 1 Builder for the 2025 SSA-1099 Benefits
> Line 6 milestone. Read `AGENTS.md`, run
> `python3 tools/build_orientation_block.py --ref HEAD`, verify the resolved
> commit, then read this charter and its cited milestone/ADR sources. Echo
> your scope, evidence ceiling, and stop conditions before editing. Implement
> only the synthetic ordinary Form SSA-1099 statement family: authoritative
> taxpayer/spouse recipient identity, logical claim/statement identity,
> correction and duplicate lifecycle, boxes 3/4/5 reconciliation, guarded
> box-6 withholding exclusion, family horizon, closure, and exact citations.
> Preserve the published tree and use no future version until inventory. Do
> not implement RRB, foreign, lump-sum, excess-repayment, withholding,
> worksheet, line 6a/6b, line 9, package, or presentation scope. Stop on any
> unresolved contract or rebase semantic-ledger loss. Use synthetic demo data,
> run focused tests, and leave a clean committed Track 1 handoff.
