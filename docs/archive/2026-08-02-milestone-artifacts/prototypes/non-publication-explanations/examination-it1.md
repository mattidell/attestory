# Examination: Iteration 1 — Non-Publication Explanations

## Proposition Status

* **NPE-P1 (Reconstructing lineage from ASTs/definitions instead of mock values):** Settled at static level. Both designs successfully model non-publication states, proving that we can explain unexecuted pathways without storing mock values or polluting the active log with blank findings.
* **NPE-P2 (Structured walk API distinguishing blocked vs. inapplicable):** Settled at static level. The proposed `explanation-walk.v1` schema successfully models and traverses recursive lineage trees, cleanly separating missing dependencies (`missing_dependency` or `unclosed_collection`) from failed applicability conditions (`failed_guard`).

---

## Case Citations

All synthetic cases from the topic plan have been successfully modeled and verified:
1. **Case 1 (Unclosed collection blocking 2b and downstream):** Traced from `demo.form1040.line9` (blocked) -> requires `demo.form1040.line2b` (blocked) -> requires `demo.1099int` (blocked due to `unclosed_collection`).
2. **Case 2 (Inapplicable itemization override):** Shows `demo.form1040.line12` successfully published (resolving to standard deduction $30,000) while citing `demo.rule.itemized-deduction-override` as `inapplicable` due to `failed_guard` (12000 > 30000 => false).
3. **Case 3 (Invalid finding blocking derivations):** Traced from `demo.form1040.line1a` (blocked) -> requires `demo.w2.box1` which is present but flagged as `invalid` because the source fact failed the `negative_value` validation constraint.

---

## Recommendation: Shape A (Rule AST/Schema Dependency Walk)

We recommend proceeding with **Shape A** for the following architectural reasons:

1. **Workspace and Act Log Purity (Articles 12 and 13):**
   Shape B violates the core ledger principles of the Constitution by flooding the act log with non-factual stub findings for every unexecuted rule path. Shape A keeps the workspace pure: only actual, successfully derived findings are recorded.
2. **Zero Execution Overhead:**
   Under Shape A, rule failures incur no serialization or storage costs during the runner's evaluation loop. Non-publication explanations are computed on-demand only when requested by the user, saving memory and disk I/O.
3. **Displacement and Cache Simplicity:**
   Because Shape B writes stub findings to the active derived store, the runner must implement complex cache-invalidation and garbage-collection routines to clean up or update these stubs when inputs change. Shape A eliminates this state management complexity entirely since unexecuted rules have no presence in the derived store.
4. **Feasibility of Static AST Tracing:**
   Since the rule language utilizes a strictly closed operations vocabulary and structured JSON schemas, the explanation walker can statically inspect rule ASTs and evaluate their expressions with high fidelity, making on-demand reconstruction reliable and robust.
