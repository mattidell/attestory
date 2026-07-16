# Triage: Non-Publication Explanations Round 2

Date: 2026-07-12
Foreman: shadow foreman (Claude, owner-directed)

Round 2 reviewed both the incumbent iteration 1 (Shape A as refined by round-1 triage) and the clean-room rival iteration 2 (Run Disposition Ledger in the ADR-0008 closing record, outside the act log). Reviews: `reviews/round-2-governance.md` (NPE-G2–G8), `reviews/round-2-adversary.md` (NPE-A4–A11).

## Convergence result

The clean-room rival, denied all round-1 material, independently landed in the same architectural family round-1 triage patched Shape A toward: runner-recorded non-execution evidence outside the act log, projected on demand. Independent convergence from two contexts is strong evidence for the family; the remaining dispute is only where the record lives (transient run metadata vs the durable ADR-0008 closing record) and its contract details.

## Decision-blocking findings

- **NPE-A4 (it1):** the round-1 "transient Execution Map" has no durable home — a walk requested after the runner exits has nothing to query. This breaks it1's refined shape as specified and favors the rival's durable-ledger placement.
- **NPE-G6 (it2):** the shipped example fixture `derivation-record.completed.json` records the same artifact as both `blocked` and `inapplicable`; the row-fold must be made single-surface (reconcile the two blocked surfaces in `derivation-record.v1`) before any ADR adopts it.
- **NPE-A5 (it2):** interrupted-run recovery writes an empty dispositions ledger; the walk algorithm needs an explicit "no row found" branch (sparse-ledger fallback or refusal with reason).
- **NPE-A6 (it2):** multi-publisher symbols (legitimate under ADR-0006 decision 7) cannot be represented by a singular `publisher_of`; adopt it1's `rules: array` structure here.
- **NPE-A7 (it2):** delegation to the unmodified pin walker breaks the O(artifacts) claim on published fan-out ancestors; cross-branch memoization must extend to the published-lineage walk.

## Production conditions

NPE-G3 (it1 disposition enum mislayers `invalid` — ADR-0012 d4), NPE-G4 (`guard_result` must be required when `disposition` is inapplicable), NPE-G5/NPE-A11 (ledger totality: guaranteed by `finalize_unreached()` on normal completion; must be stated in the record schema and scoped to exclude interrupted runs), NPE-G8 (currency/freshness contract for walk-vs-workspace staleness; rival's `run_id`/`workspace_revision` fields adopted — NPE-A10), NPE-A8 (disposition vocabulary slot for guarded-exclusivity siblings blocked with empty `missing`), NPE-A9 (fix memoization pseudocode to match the "expanded at most once" claim).

## Non-blocking

NPE-G2 (it1 text unamended post-round-1 — cite triage jointly in the ADR), NPE-G7 (align payload vocabulary to ADR-0012 `guard_inapplicable`).

## Foreman recommendation

Adopt the **converged shape**: durable Run Disposition Ledger in the ADR-0008 closing record (rival placement) with it1's multi-rule node structure and round-1's cycle-detection requirement, under the five decision-blocking repairs above. ADR-0020 as currently drafted ("transient Execution Map") does **not** match this converged shape and should be revised before ratification. The reopened `evaluation-analysis.md` should be rewritten from both iterations plus both rounds; owner decides whether that revision (and the ADR-0020 redraft) proceeds.
