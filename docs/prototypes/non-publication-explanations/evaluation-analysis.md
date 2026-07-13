# Prototype Evaluation Analysis — Non-Publication Explanations

Foreman, 2026-07-13. Status: **reopened 2026-07-12 by shadow foreman** — the plan's clean-room rival requirement (Gates 4/8) was not met in iteration 1 (the incumbent authored both shapes; see process log), so the statement below that "the rival requirement is satisfied" is withdrawn. Round-1 conclusions stand as evidence but are provisional pending the it2 clean-room rival and round-2 committee review. Prior text preserved unedited below.

Shape A (Rule AST/Schema Dependency Walk) is recommended with Execution Map and cycle detection refinements.

## Decision under evidence

This analysis evaluates how non-publication dispositions (`blocked`, `guard_inapplicable`, and `invalid`) are explained and walked in the derivation cascade.

## Evidence

| Evidence | Contribution |
|---|---|
| `exhibits/non-publication-explanations/it1` (`fd91e75` at tip) | Shape A (AST Walk) vs Shape B (Stub findings) design, schemas, and trace |
| Round 1 reviews/triage | Governance rejection of Shape B due to log bloat and ontology violations; adversary out-of-sync dynamic guard risk |

The rival requirement is satisfied: iteration 1 compared Shape A (AST Walk) and Shape B (Stub findings) across all 3 required cases.

## Supported conclusions

### C1 — Shape A preserves workspace purity and avoids combinatorial log explosion
Shape A (AST/Schema Walk) computes explanation paths dynamically on-demand, leaving the workspace act log strictly limited to factual, successfully computed findings. Shape B (Stub findings) generates stub records for every unexecuted rule path, which violates Article 12/13 and causes combinatorial log bloat (producing thousands of stubs for simple filers).

Evidence: `it1` comparative analysis; Round 1 reviews.

### C2 — Static AST walking requires a transient Execution Map to prevent out-of-sync guard evaluation
Evaluating guard expressions statically inside the explanation walker is fragile and risks getting out of sync with the runner's execution verdict if guards depend on dynamic parameter lookups. Instead of evaluating ASTs on-demand, the runner must record a transient **Execution Map** during execution (mapping rule IDs to execution status and guard result), which the walker queries directly.

Evidence: Adversary and Governance Round 1 reviews.

### C3 — Recursive walking requires cycle detection and memoization
To prevent infinite stack recursion on circular rules (e.g. mutual dependencies) and redundant walking overhead, the walker algorithm must track a visited set (cycle detection) and cache traversed paths (memoization).

Evidence: Adversary Round 1 review.

---

## Rejected alternatives

- **Shape B (Stub Findings):** Rejected due to Ontology/ledger violations (Article 12 and 13) and log bloat.
- **On-Demand Guard AST Evaluation:** Rejected due to out-of-sync risks and code duplication.

---

## Production conditions

- Implement `explanation-walk.v1` schema and walker.
- Modify the derivation runner to output a transient `Execution Map` containing rule execution status and guard result flags as metadata on the run record.
- Implement cycle detection and memoization in the walker algorithm.
