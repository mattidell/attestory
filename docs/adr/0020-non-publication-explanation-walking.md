# ADR 0020 — Non-Publication Explanation Walking

- Status: proposed (redrafted 2026-07-13 from round-2 rival evidence; prior draft's transient Execution Map withdrawn)
- Tier: 2
- Date: 2026-07-13

## Context

ADR-0012 defined the non-publication dispositions for form-field citizens: `blocked`, `guard_inapplicable`, and `invalid` (a refinement of blocked, not a peer). To ensure the auditability of the tax engine (Article 15), consumers must be able to walk the derivation cascade to reconstruct the exact lineage and reason why a symbol was not published — without violating workspace act-log purity or causing log bloat.

The prototype (`docs/prototypes/non-publication-explanations/`) produced two independent designs. Iteration 1 walked rule definitions statically, patched in round 1 with a transient runner "Execution Map." The clean-room rival (iteration 2) placed the record durably: a disposition ledger inside the ADR-0008 closing record. Round 2 established that the transient map fails the normal case — a walk requested after the runner process exits has nothing to query (NPE-A4) — and that which guard was false or which symbol was absent is a *run fact*, not recoverable from static rule text. Both reviewers converged on the durable placement.

## Decision

1. **Run Disposition Ledger.** The derivation runner records, in the ADR-0008 closing record (durable, outside the workspace act log), one disposition row per eligible artifact: execution status (`executed`, `blocked`, `guard_inapplicable`), block codes, unmet dependency references, and the guard result. `guard_result` is **required** when the disposition is `guard_inapplicable`. The ledger is the **single** authoritative disposition surface: the closing record's separate top-level `blocked[]` surface is folded into it (resolves NPE-G6's dual-surface contradiction). No stub findings are ever written to the act log (Articles 12/13).

2. **Walker as pure projection.** The explanation walker (`npe-walk.v1`) projects the ledger plus the adopted rule graph into a recursive lineage tree; it never re-evaluates guards or rule ASTs. Published nodes delegate to the existing ADR-0007/0009 pin walker under a **shared** memoization table so cross-branch diamonds are expanded at most once end-to-end (NPE-A7).

3. **Multi-publisher nodes.** A lineage node carries an *array* of publishing rules (adopted from iteration 1's structure), since ADR-0006 decision 7 permits multiple rules publishing one symbol under declared conflict semantics (NPE-A6).

4. **Sparse-ledger honesty.** If no disposition row exists for a queried artifact (interrupted or recovered runs write an empty ledger), the walk returns an explicit `no_disposition_recorded` node naming the run's completion state; it never infers a disposition (NPE-A5).

5. **Cycle detection and memoization.** The walker tracks a visited set (raising `CYCLIC_DEPENDENCY_ERROR` on cycles) and memoizes so each node is *expanded* at most once — the guarantee is enforced at expansion entry, not detected after a second full expansion (NPE-A9).

6. **Currency declaration.** The walk payload carries the `run_id` and workspace revision it explains, so consumers can detect that facts asserted after the run are not reflected; a walk explains a *run*, never current workspace state by implication (NPE-G8, NPE-A10).

7. **Vocabulary.** Payload dispositions use the ADR-0012 vocabulary exactly (`guard_inapplicable`, not `inapplicable`), and `invalid` is layered as a refinement of blocked, not a sixth sibling disposition (NPE-G3, NPE-G7).

## Production conditions

- State ledger totality in the record schema, scoped to normally completed runs (`finalize_unreached()` guarantees it; interrupted runs are excluded and covered by decision 4) (NPE-G5, NPE-A11).
- Add a disposition vocabulary slot for guarded-exclusivity siblings blocked with an empty unmet list (NPE-A8).
- Repair the self-contradictory `derivation-record.completed.json` example fixture when the single-surface fold lands (NPE-G6).
- Two-runner parity scope extends to disposition rows, not only published findings (NPE-A8 context).

## Consequences

- Workspace act-log purity is preserved; explanation evidence lives in the already-ratified record stream rather than new transient state.
- Walks are durable: any later session can explain any recorded run.
- Recording dispositions adds bounded per-run record size (one row per eligible artifact — linear, not combinatorial).
- The prior draft's zero-execution-overhead claim is traded away deliberately: run-time recording is the price of post-hoc explainability.

## Alternatives Considered

- **Transient Execution Map (prior draft of this ADR).** Rejected: no durable home; a walk after runner exit has nothing to query (NPE-A4).
- **Log-resident stub finding acts.** Rejected in round 1: Article 12/13 violations and combinatorial log bloat.
- **Pure static AST walk with on-demand guard evaluation.** Rejected: guard truth is a run fact; re-evaluation risks divergence from the runner's actual verdict (NPE-G1).

## Links

- Evidence: `docs/prototypes/non-publication-explanations/` — it1 and it2 designs and examinations, round-1/round-2 reviews, `round-1-triage.md`, `round-2-triage.md`, reopened `evaluation-analysis.md`.
- Contracts: ADR-0007, ADR-0008 (record placement), ADR-0009, ADR-0012 (dispositions).
- Process: ADR-0005, ADR-0013 (and its 2026-07-13 rival-evidence amendment).
