# Owner-Launch Charter — Findings-Only Repair for Form 1099-R IRA Line 4b

Status: dispatched by owner authorization; findings-only repair in flight.

## Context Capsule

- Source ref and resolved launch commit: the reviewed candidate on
  `milestone/form1099r-ira-distributions-line4b`, `443ac7f3e108f8d9ba271aa724faa878e25497d2`.
- Exact object: the single bounded repair cycle in the milestone plan.
- Role: original implementation Builder, Luna, Medium/medium.
- Evidence ceiling: address only numbered findings against the committed
  charter; no new contract, scope, or version family.
- Stop conditions: second substantive defect, new product decision, scope
  expansion, or any semantic-ledger loss. Return to the foreman.

## Work packet

For each finding, reproduce it, patch only the named production/fixture/docs
defect, run the focused checks, and report the exact delta. Preserve all
published history and synthetic-data constraints. The repair does not reopen
the paper boundary or add any basis, rollover, or special-distribution path.
The Reviewer rechecks only semantic findings; mechanical/type fixes use the
focused checks and CI.

## Owner launch prompt

Paste this prompt into the original Luna Builder context if repair is needed:

> Resume the Form 1099-R IRA Line 4b repair charter. Read `AGENTS.md`, orient
> from `HEAD`, and read the review findings plus this charter. Echo the exact
> numbered findings you will address. Make only findings-only repairs inside
> the existing bounded class; do not add scope, redesign contracts, allocate
> unverified versions, or alter published history. Re-run focused checks,
> document the delta, and leave a clean committed repair for independent
> re-review. Stop if a finding requires a new decision or semantic expansion.
