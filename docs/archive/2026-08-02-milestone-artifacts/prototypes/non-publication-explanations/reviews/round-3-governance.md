# Governance Review: Non-Publication Explanations (Round 3)

- **Topic:** Non-Publication Explanations
- **Round:** 3 (ADR-0020 redraft)
- **Reviewer:** Governance Reviewer (Round 3)
- **Date:** 2026-07-14
- **Scope:** `docs/adr/0020-non-publication-explanation-walking.md` (redrafted 2026-07-13), the topic's `plan.md`, `it1/design.md`, `it2/design.md`, all round-1/round-2 reviews and triages, reopened `evaluation-analysis.md`, `docs/governance/`, ADRs 0002, 0004, 0006–0012, 0016, 0017, and committed `packages/derivation/` (`records.py`, `runner.py`, `explanation.py`) at `HEAD`.
- **Independence:** did not read any other round-3 review (within-round independence).

---

## Verdict

**Ready after listed corrections.**

The redrafted ADR-0020 is conceptually sound and provides an excellent synthesis of the converged Run Disposition Ledger approach. It successfully resolves the out-of-sync risks, cycle-detection, memoization, and vocabulary alignment issues. However, it cannot be ratified in its current form due to two blocking vocabulary/enum errors in Decision 1 and the incorrect deferral of a decision-blocking fixture repair (NPE-G6). Once the listed corrections are applied, the document will be fully ready for ratification.

---

## Findings

### NPE-G9 — blocking correction — applies to: ADR-0020 Decision 1
**Summary.** Decision 1 misstates the ledger-level disposition enum values (`executed` and `guard_inapplicable` instead of `published` and `inapplicable`), introducing a direct conflict with the committed `derivation-record.v1.schema.json` and `runner.py` implementation at `HEAD`.

**Detail.** Decision 1 states that the runner records "execution status (`executed`, `blocked`, `guard_inapplicable`)" in the closing record's disposition rows. However:
1. The committed `derivation-record.v1.schema.json` defines the `disposition` property enum as `["published", "inapplicable", "blocked"]`.
2. The saturation runner (`runner.py` at `HEAD`) writes `"published"`, `"inapplicable"`, and `"blocked"` to the disposition rows.
3. The term `executed` is not supported by the schema or runner implementation (which use `published` to indicate successfully computed derived findings).
4. The term `guard_inapplicable` is the walk payload term (governed by Decision 7 and ADR-0012), whereas the ledger uses `inapplicable`.

**Failure scenario.** An implementation attempting to follow ADR-0020 literally would either:
- Update the ledger schema to use `executed` and `guard_inapplicable`, breaking parity with existing runner code and schemas.
- Or keep the schema as-is, leaving the ADR's text out-of-sync with the actual committed contract.

**Resolution.** Revise Decision 1's text to state the actual ledger-level disposition values:
> "...one disposition row per eligible artifact: execution status (`published`, `blocked`, `inapplicable`), block codes, unmet dependency references, and the guard result."

---

### NPE-G10 — blocking correction — applies to: ADR-0020 Production Conditions
**Summary.** The ADR incorrectly defers the repair of the contradictory `derivation-record.completed.json` example fixture (NPE-G6) to post-ratification "Production conditions," despite the round-2 triage explicitly classifying it as decision-blocking for any ADR adopting the single-surface fold.

**Detail.** Round-2 triage and the round-2 governance review established that the committed example fixture `derivation-record.completed.json` is contradictory because it records the same artifact (`demo.rule.tax-table-line16`) as both `blocked` (in the top-level `blocked[]` array) and `inapplicable` (in the `dispositions[]` array).
ADR-0020 Decision 1 adopts the single-surface fold to resolve this contradiction. However, by deferring the actual repair of the committed fixture and schema to "Production conditions," the project is asked to ratify an ADR that claims to resolve a contradiction while the companion committed files remain contradictory.

**Failure scenario.** A consumer attempts to validate the committed example fixture against the new ADR-0020 rules before the production phase begins and finds the evidence still contradictory.

**Resolution.** Move the repair of the example fixture and the schema changes associated with the single-surface ledger fold from "Production conditions" to the immediate prerequisites of ratification (or explicitly list them as a concurrent schema amendment to land with the ADR).

---

### NPE-G11 — non-blocking / correction — applies to: ADR-0020 Decision 1
**Summary.** The scope of the conditional `guard_result` requirement in Decision 1 uses the walk-payload vocabulary (`guard_inapplicable`) rather than the ledger-level vocabulary (`inapplicable`).

**Detail.** Decision 1 states: "`guard_result` is **required** when the disposition is `guard_inapplicable`." Because `guard_result` is a property of the ledger row (inside the `derivation-record.v1` closing record schema), and the ledger disposition enum value is `inapplicable` (not `guard_inapplicable`), the requirement is slightly mis-scoped/mis-labeled.

**Failure scenario.** A schema validator looking for a property constraint under `guard_inapplicable` in the record schema fails because the property is named `inapplicable`.

**Resolution.** Correct the vocabulary in Decision 1 to refer to the ledger-level term:
> "`guard_result` is **required** when the disposition is `inapplicable`."

---

## Assignment Review

### 1. Faithful Implementation of Cited Findings
Each of the seven decisions has been mapped to its corresponding findings:
- **Decision 1 (Run Ledger & Fold):** Faithfully addresses `NPE-A4` (durability of the ledger outside the act log) and `NPE-G6` (resolving the dual-surface contradiction by folding the arrays). However, it introduces minor vocabulary errors (`executed` and `guard_inapplicable` inside the ledger) which require correction (NPE-G9/NPE-G11).
- **Decision 2 (Pure Projection Walker):** Faithfully implements the walk projection constraint and integrates the `shared` memoization table to resolve `NPE-A7` (avoiding redundant expansions of published ancestors in diamonds).
- **Decision 3 (Multi-publisher Nodes):** Faithfully implements `NPE-A6` by representing rules as an array, satisfying the conflict-semantics requirements of ADR-0006.
- **Decision 4 (Sparse-ledger Honesty):** Faithfully implements `NPE-A5` by returning a `no_disposition_recorded` fallback node for interrupted runs rather than reconstructing/inferring state.
- **Decision 5 (Cycle/Memoization):** Faithfully implements `NPE-A9` by enforcing visited-set checking and caching at expansion entry, ensuring the "expanded at most once" invariant holds.
- **Decision 6 (Currency Declaration):** Faithfully addresses the freshness concern of `NPE-G8`/`NPE-A10` by carrying `run_id` and `workspace_revision` on the payload to expose run-specific context.
- **Decision 7 (Vocabulary Layering):** Faithfully implements `NPE-G3` and `NPE-G7` by mapping the internal ledger dispositions to official ADR-0012 terms and correctly layering `invalid` as a blocked refinement.

### 2. Consistency of Single-Surface Fold and `guard_result` Scoping
- **ADR-0008 Consistency:** The fold is fully consistent with the ADR-0008 record contract. ADR-0008 decision 3 requires structured completion records containing published/blocked information but does not mandate separate surfaces. The single-surface ledger satisfies all contract requirements while simplifying the walk algorithm.
- **`guard_result` Scoping:** The requirement is correctly scoped as a conditional constraint (only required when inapplicable), but the text of Decision 1 must use the ledger-level term `inapplicable` instead of `guard_inapplicable`.

### 3. Verification of Production Conditions
The production conditions listed are appropriate and deferrable, *except* for the repair of the contradictory example fixture (NPE-G6). As noted in NPE-G10, the fixture repair is a decision-blocking defect that cannot be deferred. The other items (schema totality, parity scope, sibling vocabulary slots) are genuine implementation details that do not alter the architectural decisions.

### 4. Honesty of Alternatives Considered
The alternatives considered section is highly honest. It accurately depicts:
- The **Transient Execution Map** and why it was rejected (durability/lifetime limit per NPE-A4).
- The **Log-resident stub findings** and why they were rejected (Article 12/13 and log bloat).
- The **Pure static walk** and why it was rejected (divergence risk per NPE-G1).

### 5. Constitutional and Vocabulary Conformance
- **Article 7 (Supersession):** Compliant. Currency remains derived, and no historical records are mutated.
- **Article 12 (Contract):** Compliant. The walker is a projection over committed records; derivation itself does not read records.
- **Article 13 (Publication):** Compliant. No stub findings are written to the workspace act log. Non-publication data is stored strictly in the separate process record stream.
- **ADR-0012 Vocabulary:** Compliant at the walk-payload level (Decision 7). Ledger-level vocabulary mismatch in Decision 1 is flagged for correction (NPE-G9).
