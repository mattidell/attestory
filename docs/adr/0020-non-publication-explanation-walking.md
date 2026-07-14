# ADR 0020 — Non-Publication Explanation Walking

- Status: proposed (round-4 redraft 2026-07-14, folding the round-3 triage's seven decision-blocking findings and NPE-A14 into decision text; round-2→round-3 durable-ledger shape unchanged)
- Tier: 2
- Date: 2026-07-14

## Context

ADR-0012 defined the non-publication dispositions for form-field citizens: `blocked`, `guard_inapplicable`, and `invalid` (a refinement of blocked, not a peer). To ensure the auditability of the tax engine (Article 15), consumers must be able to walk the derivation cascade to reconstruct the exact lineage and reason why a symbol was not published — without violating workspace act-log purity (Articles 12/13) or causing log bloat.

The prototype (`docs/prototypes/non-publication-explanations/`) produced two independent designs. Iteration 1 walked rule definitions statically, patched in round 1 with a transient runner "Execution Map." The clean-room rival (iteration 2) placed the record durably: a disposition ledger inside the ADR-0008 closing record. Round 2 established that the transient map fails the normal case — a walk requested after the runner process exits has nothing to query (NPE-A4) — and that which guard was false or which symbol was absent is a *run fact*, not recoverable from static rule text. Both reviewers converged on the durable placement. Round 3 reviewed the durable redraft and returned seven decision-blocking findings (see `docs/prototypes/non-publication-explanations/round-3-triage.md`); this round-4 text folds them in. The converged shape is unchanged; the corrections are to its decision text and the `npe-walk.v1` schema.

## Vocabulary layering (resolves NPE-G9/G11)

Two distinct surfaces use two distinct vocabularies, and the redraft previously conflated them:

- **Ledger level** — the ADR-0008 closing-record disposition rows. Uses the committed `derivation-record.v1` enum **exactly**: `published`, `blocked`, `inapplicable`.
- **Walk-payload level** — the `npe-walk.v1` lineage tree the walker returns. Uses the ADR-0012 vocabulary **exactly**: `blocked`, `guard_inapplicable`, and `invalid` (a refinement of blocked).

Decision 7 defines the mapping between them (ledger `inapplicable` → payload `guard_inapplicable`). No surface invents a term the other owns.

## Decision

1. **Run Disposition Ledger.** The derivation runner records, in the ADR-0008 closing record (durable, outside the workspace act log), one disposition row **per rule and selector artifact in the adopted package** — not only the artifacts that became eligible (resolves NPE-A18: totality is what lets the walker be a pure projection rather than reconstructing unreached rules statically). Each row carries the ledger-level execution status (`published`, `blocked`, `inapplicable`), block codes, unmet dependency references, and the guard result; `guard_result` is **required** when the disposition is `inapplicable`. The ledger is the **single authoritative** disposition surface. The closing record's legacy top-level `blocked[]` array is **retained as a compatibility read-model derived from the ledger** (the rows with disposition `blocked`), so existing record consumers (`records.py`, its tests) keep a stable surface while the single source of truth is the ledger (resolves NPE-A12a — no consumer is broken and there is no second authoritative surface). No stub findings are ever written to the act log (Articles 12/13).

   **1a. Conflict-loser disposition (resolves NPE-A12b — the one new decision this round surfaced).** Under ADR-0006 decision 7's declared conflict semantics, when a higher-priority rule has already published an output symbol, a lower-priority rule publishing the same symbol is an *unselected conflict-loser*. It is recorded `inapplicable` (guard result: superseded by the selected publisher), **not** `blocked` — regardless of whether its own dependencies are present. Both runners must agree: the saturation runner records it `inapplicable` as it loops past the already-satisfied symbol, and the reference runner's `finalize_unreached()` must classify a swept rule whose output symbol is already published as `inapplicable` rather than `blocked`. This makes the ledger portable across scheduling strategies.

2. **Walker as pure projection.** The explanation walker (`npe-walk.v1`) projects the ledger plus the adopted rule graph into a recursive lineage tree; it never re-evaluates guards or rule ASTs. Published nodes delegate to the ADR-0007/0009 pin-lineage walker (`explanation.py`) under a **shared** memoization table so cross-branch diamonds are expanded at most once end-to-end (NPE-A7). This **requires modifying `explanation.py`** to accept and participate in the shared table: the previous "unchanged delegation" wording is retracted (resolves NPE-A17), because the committed walker passes its `_seen` set by value and tracks only active cycle loops, not cross-branch duplicates. The modification is additive (an optional shared table parameter) and preserves the committed single-branch behavior when absent.

3. **Multi-publisher nodes.** A lineage node carries an **array** of publishing rule references (`rule_references[]`), since ADR-0006 decision 7 permits multiple rules publishing one symbol under declared conflict semantics (NPE-A6). The `npe-walk.v1` schema declares `rule_references` as an array (not a singular `artifact_id`), and the walker resolves **all** producers of a symbol under the package's conflict order rather than a singular `publisher_of` lookup (resolves NPE-A16: the decision text and the schema now agree).

4. **Sparse-ledger honesty, act-log first.** A walk for a symbol first consults the workspace act log: **if the finding is published there, the walker walks it via the pin-lineage walker regardless of the ledger's state** — a published value always has a lineage (resolves NPE-A13, which showed an interrupted run's empty ledger otherwise reported `no_disposition_recorded` for a live, visible finding, violating Articles 8/15). Only when a symbol is **neither** published in the act log **nor** present as a ledger row does the walk return an explicit `no_disposition_recorded` node naming the run's completion state (interrupted / recovered). The walk never infers a disposition (NPE-A5).

5. **Cycle detection and memoization.** The walker tracks a visited set (raising `CYCLIC_DEPENDENCY_ERROR` on cycles) and memoizes so each node is *expanded* at most once, enforced at expansion entry (NPE-A9). The **shared** table is the canonical store of expanded node results, keyed by node id and populated on first expansion; a node reached again is emitted as a **reference** to its shared entry, never re-expanded (resolves NPE-A14: the entry-guarantee no longer tensions with "diamonds only" — every expanded node has a shared entry, and *inline vs. reference* is a rendering choice at projection time, not a correctness constraint; a node referenced more than once is by definition the diamond case).

6. **Currency declaration.** The walk payload carries the `run_id` and workspace revision it explains, so consumers can detect that facts asserted or withdrawn after the run are not reflected; a walk explains a *run*, never current workspace state by implication (NPE-G8, NPE-A10). (Carrying a *characterization* of what changed since the run — added vs. withdrawn facts — is advisory and deferred; NPE-A15.)

7. **Vocabulary.** Walk-payload dispositions use the ADR-0012 vocabulary exactly (`guard_inapplicable`, not the ledger's `inapplicable`), and `invalid` is layered as a refinement of blocked, not a sixth sibling disposition (NPE-G3, NPE-G7). The walker maps each ledger row to its payload term per the vocabulary-layering section above.

## Prerequisites landing with the ADR (not deferred)

- **Single-surface fold + fixture repair (resolves NPE-G10).** The `derivation-record.v1` schema change (ledger as authoritative surface, `blocked[]` derived) and the repair of the self-contradictory `derivation-record.completed.json` example fixture — which records one artifact as both `blocked` and `inapplicable` — land **concurrently** with this ADR's ratification, not in a later production phase. Ratifying a fold that claims to resolve the contradiction while the committed fixture stays contradictory is incoherent.

## Production conditions

- State ledger totality in the record schema (one row per package rule/selector artifact) and confirm `finalize_unreached()` and the saturation loop both satisfy it, including conflict-losers per decision 1a (NPE-G5, NPE-A11, NPE-A8 context).
- Add a disposition vocabulary slot, if needed, for guarded-exclusivity siblings blocked with an empty unmet list (NPE-A8), now largely subsumed by decision 1a.
- Two-runner parity scope extends to disposition rows and their conflict-loser classification, not only published findings.

## Consequences

- Workspace act-log purity is preserved; explanation evidence lives in the already-ratified record stream rather than new transient state.
- Walks are durable and portable: any later session, and either runner, explains any recorded run identically.
- Recording dispositions adds bounded per-run record size (one row per package rule/selector artifact — linear, not combinatorial).
- The prior draft's zero-execution-overhead claim is traded away deliberately: run-time recording is the price of post-hoc explainability.
- `explanation.py` gains an optional shared-memoization parameter; its committed single-branch behavior is unchanged when the parameter is absent.

## Alternatives Considered

- **Transient Execution Map (prior draft of this ADR).** Rejected: no durable home; a walk after runner exit has nothing to query (NPE-A4).
- **Log-resident stub finding acts.** Rejected in round 1: Article 12/13 violations and combinatorial log bloat.
- **Pure static AST walk with on-demand guard evaluation.** Rejected: guard truth is a run fact; re-evaluation risks divergence from the runner's actual verdict (NPE-G1).
- **Two authoritative disposition surfaces (pre-fold).** Rejected: the dual `blocked[]` / `dispositions[]` surfaces produced the self-contradictory fixture (NPE-G6); a single authoritative ledger with a derived compatibility read-model replaces them.
- **Recording only eligible artifacts.** Rejected: a sparse ledger forces the walker to reconstruct unreached rules from static text, defeating the pure-projection property (NPE-A18).

## Links

- Evidence: `docs/prototypes/non-publication-explanations/` — it1 and it2 designs and examinations, round-1/2/3 reviews, `round-1-triage.md`, `round-2-triage.md`, `round-3-triage.md`, `evaluation-analysis.md`.
- Contracts: ADR-0006 (conflict semantics), ADR-0007, ADR-0008 (record placement), ADR-0009, ADR-0012 (dispositions). Governance: Articles 8, 12, 13, 15.
- Process: ADR-0005, ADR-0013 (and its 2026-07-13 rival-evidence amendment).
