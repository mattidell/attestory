# Triage: Non-Publication Explanations Round 1

Date: 2026-07-13
Foreman: Codex Foreman

This document records the triage of findings from Round 1 reviews of the `non-publication-explanations` prototype, in accordance with Gate 5 of the prototype process.

## Findings Classification

### 1. Decision-Blocking Findings (Must be resolved in final evaluation and ADR drafts)

* **NPE-G1 (Shape A Dynamic Guard Out-of-Sync Risk):** **Decision-Blocking.**
  - *Description:* Re-evaluating rule guards statically in the explanation walker is fragile, duplicates code, and risks getting out of sync with the runner's actual execution path.
  - *Resolution:* The runner must compile a lightweight, transient "Execution Map" (rule status log) during evaluation, recording the boolean execution status and guard evaluation result for each scheduled rule (stored as run metadata, not as findings in the log). The walker reads this execution map rather than evaluating rule ASTs statically.
* **NPE-A1 (Cyclic Dependencies and Walk Stack Overflow):** **Decision-Blocking.**
  - *Description:* Recursive walking is vulnerable to infinite loops on cyclic rules.
  - *Resolution:* The walker algorithm must implement cycle detection (tracking a visited set) and memoization.

### 2. Production Conditions (To be addressed during production implementation)

* **NPE-A2 (Combinatorial Explosion of Stubs in Shape B):** **Production Condition.**
  - *Description:* Confirms Shape B is unusable for production due to log bloat and ontology violations.
  - *Resolution:* Reconfirm Shape A as the only allowed path.

### 3. Non-Blocking Defects & Deferred Breadth (Log and defer / easily repairable)

* **NPE-A3 (Validation and Constraint Reporting):** **Non-Blocking Defect.**
  - *Description:* The schema needs better support for linking direct validation failures.
  - *Resolution:* Add explicit validation constraint details and failed fact identifiers to the walk payload schema in the final design.

---

## Foreman Recommendation

Shape B is rejected due to Ontology/ledger violations (Article 12 and 13) and log bloat (combinatorial stub explosion).

We recommend proceeding with **Shape A (Rule AST/Schema Dependency Walk)** with the following refinements to be documented in the final **Evaluation Analysis** and drafted **ADRs**:
1. The runner records a lightweight, transient "Execution Map" (mapping rule IDs to status: `executed`, `blocked`, `inapplicable`) as run metadata.
2. The walker walks the rule definitions but queries this map to resolve guard results without dynamic AST evaluation.
3. The walker implements cycle detection and memoization.
