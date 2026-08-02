# Governance Review: Non-Publication Explanations (Iteration 1)

- **Topic:** Non-Publication Explanations
- **Iteration:** 1
- **Reviewer:** Governance Reviewer
- **Date:** 2026-07-13
- **Status:** Completed

---

## Executive Summary

This review evaluates the Iteration 1 design proposal for the [non-publication-explanations](../../../../../../docs/archive/2026-08-02-milestone-artifacts/prototypes/non-publication-explanations/plan.md) prototype. We examine the conformance of both **Shape A (Rule AST/Schema Dependency Walk)** and **Shape B (Dry-Run / Stub Finding Acts)** against the [constitution.md](../../../../../../docs/governance/constitution.md) and the [engineering-constraints.md](../../../../../../docs/governance/engineering-constraints.md).

### Verdict
We **recommend Shape A** with specific refinements to ground explanations in runner-emitted process records. We **reject Shape B** due to severe violations of workspace purity, the fact/finding ontology invariants, and the mechanics of supersession.

---

## 1. Shape A Evaluation: Workspace and Act Log Purity

### Conformance with Article 12 and Article 13
Shape A proposed in the [design.md](../../../../../../docs/archive/2026-08-02-milestone-artifacts/prototypes/non-publication-explanations/it1/design.md) preserves the purity of the workspace and the act log by refusing to write mock values, placeholder claims, or empty findings.
* **Article 12 (Contract):** Derived findings must pin vouched-for inputs. Storing placeholder or mock values representing unexecuted code paths would create derived findings based on empty or non-factual dependencies, violating this article.
* **Article 13 (Publication):** "A run may stop anywhere leaving the workspace incomplete, never wrong." Under Shape A, unexecuted rules simply do not publish findings. The workspace remains *incomplete* (possessing open facts) rather than *wrong* (polluted with fake findings). This conforms exactly to the ontology definition of an **Open Fact** in [ontology.md](../../../../../../docs/governance/ontology.md), which states that questions of fact exist unvalued and that facts must exist without findings to indicate coverage gaps.

### Constitutional Tension & Refinement
The proposed Shape A dynamically reconstructs the unexecuted pathway on-demand by re-evaluating the AST and the rule's guard expressions. This introduces an **Out-of-Sync Risk** (the dynamic walker evaluator might diverge from the runner's evaluation logic) and creates tension with:
* **Article 15 (Explanation):** "Every value connects to the findings... grounded in the record — never reconstructed." While non-publication applies to facts that *lack* a value, generating explanations through post-hoc AST traversal rather than consulting execution logs diverges from the principle of grounding explanations in historical execution state.
* **Article 14 (Record):** "Every process that reads or writes authoritative state leaves an immutable process record... identifying... what blocked it, and why it stopped. Failed executions record."

> [!TIP]
> **Refined Shape A (Process-Record Grounded Walker):**
> Rather than evaluating the rule AST and applicability guards dynamically on-demand (which introduces divergence risks), the runner should record why a rule was blocked, inapplicable, or invalid directly into the run's immutable **process record** (Article 14). The explanation walker should then traverse these process records. This combines the workspace purity of Shape A (no mock findings in the active finding store) with the historical grounding required by Article 15.

---

## 2. Shape B Evaluation: Finding Invariants and Cache Pollution

We find that Shape B introduces multiple architectural and constitutional violations:

### Violation of Fact/Finding Invariants
* Under the [ontology.md](../../../../../../docs/governance/ontology.md) definitions, a **Finding** is a determination of a fact (an answer). An **Open Fact** is explicitly defined as a fact with no current finding.
* Shape B writes "stub findings" to represent blocked or inapplicable states. This turns open facts into facts possessing a finding, breaking the semantic definition of open facts and violating the integrity of the active derived finding store.

### Violation of Supersession and Deletion Mechanics
* **Article 7 (Supersession):** "History only accumulates... There is no deletion, no editing, no second mechanism for special cases."
* Under Shape B, when input facts change, the status of downstream rules changes (a blocked rule might become eligible, or an inapplicable rule might become applicable). 
* To prevent the workspace from containing obsolete stubs, the runner would have to garbage-collect, invalidate, or delete stub findings. This introduces a separate state management mechanism (garbage collection of stubs) that violates Article 7's single mechanism constraint ("no deletion").
* If stubs are not deleted, they must accumulate. Iterative editing of input facts would flood the workspace history with hundreds of obsolete "stub findings" for every transitional state, polluting the log.

---

## 3. Schema Evaluation: `explanation-walk.v1`

We reviewed the proposed [explanation-walk.v1.schema.json](../../../../../../docs/archive/2026-08-02-milestone-artifacts/prototypes/non-publication-explanations/it1/design.md#L45) and the instance payloads:

### Strengths
1. **Clear Distinctions:** The schema distinguishes between standard values and non-published states using the `disposition` field (`blocked`, `guard_inapplicable`, `invalid`).
2. **Failure Types:** It maps failure types (`missing_dependency`, `unclosed_collection`, `failed_guard`, `invalid_dependency`) cleanly, which fully answers NPE-P2 by separating dependencies from applicability guards.
3. **Recursive Lineage:** The `dependencies` array uses a recursive `$ref` structure, allowing full traversal of multi-step block cascades.

### Identified Gap & Recommendation
* **Root Validation Failure:** The `failures` structure currently places validation errors under `invalid_dependency` (a rule blocked because one of its dependencies is invalid). However, a rule might execute and produce a value that itself fails a validation constraint (making the direct target symbol disposition `invalid`). 
* **Recommendation:** Expand the schema's failure types to include a `failed_validation` type at the rule/symbol level to represent when a derived value itself fails constraints, rather than only tracing invalid dependencies downstream.

---

## Conclusion & Next Steps

1. **Adopt Shape A:** Proceed with Shape A for the milestone implementation.
2. **Refine Walker Mechanics:** Ground the explanation walker's query loop in the runner's immutable process records (Article 14) rather than performing dynamic AST expression evaluation on-demand.
3. **Update Schema:** Merge the refined `explanation-walk.v1` schema to include direct validation failures.
