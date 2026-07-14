# ADR 0020 — Non-Publication Explanation Walking

- Status: proposed (round-5 corrective redraft 2026-07-14, applying the round-4 confirmation review's two decision-blocking corrections NPE-A19/A20 plus NPE-A22; round-4 folded the round-3 triage's seven blockers + NPE-A14; durable-ledger shape unchanged since round 2)
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

1. **Run Disposition Ledger.** The derivation runner records, in the ADR-0008 closing record (durable, outside the workspace act log), one disposition row **per rule artifact in the adopted package (and any other derivation-producing package member kinds actually adopted)** — not only the artifacts that became eligible (resolves NPE-A18: totality is what lets the walker be a pure projection rather than reconstructing unreached rules statically; the stale "selector artifact" phrasing is dropped per NPE-A22, since ADR-0024 rejected first-class selector citizens). Each row carries the ledger-level execution status (`published`, `blocked`, `inapplicable`), block codes, unmet dependency references, and the disposition evidence per decision 1a. The ledger is the **single authoritative** disposition surface. The closing record's legacy top-level `blocked[]` array is **retained as a compatibility read-model derived from the ledger** (the rows with disposition `blocked`), so existing record consumers (`records.py`, its tests) keep a stable surface while the single source of truth is the ledger (resolves NPE-A12a — no consumer is broken and there is no second authoritative surface). No stub findings are ever written to the act log (Articles 12/13).

   **1a. Classification order and conflict-loser disposition (resolves NPE-A12b; corrected per NPE-A19).** Each artifact's ledger row is classified in this fixed order, applied identically by the saturation runner's `attempt` and the reference runner's `finalize_unreached()` so the ledger is portable across scheduling strategies:

   1. **If any declared dependency is absent → `blocked`** (`BLOCK_ABSENT`, `missing` listing the absent symbols) — **even if a higher-priority sibling has already published the output symbol.** A dependency gap is a real run fact and must not be masked as a conflict outcome (if the winner were later removed, the rule still could not publish). This is the NPE-A19 correction: the round-4 "regardless of dependencies" clause is withdrawn.
   2. **Else, if the output symbol is already published by another producer** under ADR-0006 decision 7 declared conflict semantics → **`inapplicable`** as an *unselected conflict-loser*. The row carries a `superseded_by` reference to the selected publisher as its disposition evidence — **not** a synthetic `guard_result` (decision 2 forbids inventing a guard evaluation that never ran).
   3. **Else evaluate the guard/value** as today: `published`; or `inapplicable` with a real `guard_result` for a false guard; or `blocked` for a value error.

   `guard_result` is required only for a decision-1a-step-3 `inapplicable` (a genuinely false guard). A conflict-loser `inapplicable` (step 2) is ledger-level completeness bookkeeping: because its output symbol *is* published (by the winner), symbol-level walks are unaffected, and the `superseded_by` reference is the evidence for any rule-level query — so no new payload-vocabulary term is invented (ADR-0012 stays fixed).

2. **Walker as pure projection.** The explanation walker (`npe-walk.v1`) projects the ledger plus the adopted rule graph into a recursive lineage tree; it never re-evaluates guards or rule ASTs. Published nodes delegate to the ADR-0007/0009 pin-lineage walker (`explanation.py`) under a **shared** memoization table so cross-branch diamonds are expanded at most once end-to-end (NPE-A7). This **requires modifying `explanation.py`** to accept and participate in the shared table: the previous "unchanged delegation" wording is retracted (resolves NPE-A17), because the committed walker passes its `_seen` set by value and tracks only active cycle loops, not cross-branch duplicates. The modification is additive (an optional shared table parameter) and preserves the committed single-branch behavior when absent.

3. **Multi-publisher nodes.** A lineage node carries an **array** of publishing rule references (`rule_references[]`), since ADR-0006 decision 7 permits multiple rules publishing one symbol under declared conflict semantics (NPE-A6). The `npe-walk.v1` schema declares `rule_references` as an array (not a singular `artifact_id`), and the walker resolves **all** producers of a symbol under the package's conflict order rather than a singular `publisher_of` lookup (resolves NPE-A16: the decision text and the schema now agree).

4. **Sparse-ledger honesty, run-scoped selection.** A walk for run `R` and symbol `S` selects the finding (or disposition) to explain in this fixed order (corrected per NPE-A20 — the round-4 "act-log first regardless of the ledger" is withdrawn because, unscoped, it could attach a *later* run's finding while claiming to explain `R`):

   1. If the closing ledger for `R` has a `published` row for a producer of `S` naming a finding id → walk **that** finding via the pin-lineage walker.
   2. Else if the workspace act log contains a `derived-publication` whose `payload.run_id == R` that publishes `S` → walk that finding. This is the NPE-A13 case — the interrupted/recovered run whose ledger is empty though the publication reached the act log — now **run-scoped** so a later run's finding can never explain an earlier run.
   3. Else if the ledger has a non-published row (`blocked` / `inapplicable`) for a producer of `S` → project that ledger row.
   4. Else → an explicit `no_disposition_recorded` node naming the run's closing phase (interrupted / recovered / open).

   The walk never infers a disposition (NPE-A5), never consults a publication of `S` not bound to run `R`, and never ignores a complete ledger's finding reference in favor of a later act. A pin-lineage walk of a correctly selected historical finding projects its committed pins even if later acts superseded those inputs — that is honest run-scoped history (Article 15), and decision 6's currency declaration lets consumers detect staleness against the live workspace.

5. **Cycle detection and memoization.** The walker tracks a visited set (raising `CYCLIC_DEPENDENCY_ERROR` on cycles) and memoizes so each node is *expanded* at most once, enforced at expansion entry (NPE-A9). The **shared** table is the canonical store of expanded node results, keyed by node id and populated on first expansion; a node reached again is emitted as a **reference** to its shared entry, never re-expanded (resolves NPE-A14: the entry-guarantee no longer tensions with "diamonds only" — every expanded node has a shared entry, and *inline vs. reference* is a rendering choice at projection time, not a correctness constraint; a node referenced more than once is by definition the diamond case).

6. **Currency declaration.** The walk payload carries the `run_id` and workspace revision it explains, so consumers can detect that facts asserted or withdrawn after the run are not reflected; a walk explains a *run*, never current workspace state by implication (NPE-G8, NPE-A10). (Carrying a *characterization* of what changed since the run — added vs. withdrawn facts — is advisory and deferred; NPE-A15.)

7. **Vocabulary.** Walk-payload dispositions use the ADR-0012 vocabulary exactly (`guard_inapplicable`, not the ledger's `inapplicable`), and `invalid` is layered as a refinement of blocked, not a sixth sibling disposition (NPE-G3, NPE-G7). The walker maps each ledger row to its payload term per the vocabulary-layering section above.

## Prerequisites landing with the ADR (not deferred)

- **Single-surface fold + fixture repair (resolves NPE-G10).** The `derivation-record.v1` schema change (ledger as authoritative surface, `blocked[]` derived) and the repair of the self-contradictory `derivation-record.completed.json` example fixture — which records one artifact as both `blocked` and `inapplicable` — land **concurrently** with this ADR's ratification, not in a later production phase. Ratifying a fold that claims to resolve the contradiction while the committed fixture stays contradictory is incoherent.

## Production conditions

- State ledger totality in the record schema (one row per package rule artifact) and confirm `finalize_unreached()` and the saturation loop both satisfy it, applying the decision-1a classification order identically (NPE-G5, NPE-A11, NPE-A8 context).
- Add a disposition vocabulary slot, if needed, for guarded-exclusivity siblings blocked with an empty unmet list (NPE-A8), now largely subsumed by decision 1a.
- Two-runner parity scope extends to disposition rows and their decision-1a classification, not only published findings.
- When the `npe-walk.v1` schema is written, define the mixed-disposition projection for a multi-publisher symbol node (NPE-A21): when producers of one symbol carry mixed ledger rows (e.g. one `published`, one conflict-loser `inapplicable`, one `blocked`), fix the symbol node's `node_kind` and where each producer's disposition evidence attaches (per-reference sub-nodes vs annotations). This does not reopen decision 3's array/schema agreement.

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
