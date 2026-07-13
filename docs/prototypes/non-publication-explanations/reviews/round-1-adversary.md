# Adversary Review: Iteration 1 — Non-Publication Explanations

- **Topic:** Non-Publication Explanations in the Derivation Cascade
- **Iteration:** 1
- **Reviewer:** Adversary Reviewer (Subagent)
- **Date:** 2026-07-13
- **Artifacts Reviewed:**
  - Topic Plan: [plan.md](file:///Users/mattidell/.gemini/antigravity/brain/7e3848b3-ae96-4887-b089-6efbf5c538a8/.system_generated/worktrees/subagent-Adversary-Reviewer-self-624de5cb/docs/prototypes/non-publication-explanations/plan.md)
  - Iteration Charter: [charter-it1.md](file:///Users/mattidell/.gemini/antigravity/brain/7e3848b3-ae96-4887-b089-6efbf5c538a8/.system_generated/worktrees/subagent-Adversary-Reviewer-self-624de5cb/docs/prototypes/non-publication-explanations/charter-it1.md)
  - Design Proposal: [design.md](file:///Users/mattidell/.gemini/antigravity/brain/7e3848b3-ae96-4887-b089-6efbf5c538a8/.system_generated/worktrees/subagent-Adversary-Reviewer-self-624de5cb/docs/prototypes/non-publication-explanations/it1/design.md)
  - Examination: [examination-it1.md](file:///Users/mattidell/.gemini/antigravity/brain/7e3848b3-ae96-4887-b089-6efbf5c538a8/.system_generated/worktrees/subagent-Adversary-Reviewer-self-624de5cb/docs/prototypes/non-publication-explanations/examination-it1.md)

---

## Executive Summary

The incumbent builder's design proposal presents a clear dichotomy between **Shape A** (static AST/schema walker) and **Shape B** (runner-written dry-run stub findings). This review evaluates both shapes against adversary scenarios designed to expose edge cases, cycle handling failures, scalability bottlenecks, and validation modeling issues.

We find that:
1. **Shape A** is vulnerable to evaluation failures for dynamic/runtime-dependent guards and is highly prone to stack overflows/redundant evaluations in cyclic or multi-path dependency graphs if left unmitigated.
2. **Shape B** is structurally sound for walking but creates a severe risk of log-size combinatorial explosion and introduces massive complexity in incremental displacement/cache management.
3. Both designs lack necessary details to handle record collections, validation indexes, and optional/fallback input paths cleanly.

---

## Adversary Checks & Counterexamples

### 1. Dynamic Expressions & Runtime Context (Shape A)

**The Check:** If a rule has a dynamic expression that depends on runtime parameters, can the walker evaluate the `when` guard statically without having the full runner context? What happens if a guard is highly dynamic or complex?

* **Evaluation:** Shape A assumes the walker can evaluate guards statically by reading values from the asserted fact store. However, if the guard relies on:
  - Runtime parameters (e.g., current tax year, system flags, filing configurations).
  - Intermediate, unpersisted calculator variables.
  - Multi-stage/iterative state changes (where a variable value depends on the iteration step).
  then static evaluation will fail or yield incorrect results.
* **Counterexample Scenario:** Consider an itemized deduction limit rule that determines applicability based on a dynamic phase-out threshold:
  ```yaml
  symbol: demo.form1040.itemization_override
  when: "itemized_deductions > get_standard_deduction_limit(filing_status, taxpayer_age, blind_status)"
  ```
  If `taxpayer_age` and `blind_status` are computed properties, or if `get_standard_deduction_limit` is a complex function defined in the runner engine, the explanation walker must duplicate the entire evaluation engine and run with the exact same runtime parameters. 
* **Consequences:** 
  - **Code Duplication & Out-of-Sync Risk:** The walker must replicate the runner's expression evaluation logic. Any divergence between the runner's evaluation and the walker's reconstruction results in incorrect explanations.
  - **Undefined Dependencies:** If the guard depends on a symbol that was itself blocked, trying to evaluate the guard expression will throw an evaluation error (e.g., type error or null reference) unless the walker has complex handling for partial/undefined states.

---

### 2. Cyclic Dependencies and Multi-Path Blocks (Shape A)

**The Check:** What happens if there are cyclic dependencies or multi-path blocks (e.g., symbol `S` is blocked because of `A` and `B`, but `A` is blocked because of `B`)? Does the walk loop infinitely, or does it handle cycles?

* **Evaluation:** The walk algorithm described in [design.md](file:///Users/mattidell/.gemini/antigravity/brain/7e3848b3-ae96-4887-b089-6efbf5c538a8/.system_generated/worktrees/subagent-Adversary-Reviewer-self-624de5cb/docs/prototypes/non-publication-explanations/it1/design.md) specifies recursive traversal without cycle-detection or node memoization.
* **Counterexample 1 (Cyclic Loop):** 
  - Rule 1: `S1` requires `S2`.
  - Rule 2: `S2` requires `S1`.
  - If both are missing/blocked, `walk(S1)` resolves Rule 1, flags `S2` as missing, and calls `walk(S2)`. `walk(S2)` resolves Rule 2, flags `S1` as missing, and calls `walk(S1)`.
  - **Result:** Infinite recursion leading to a Stack Overflow.
* **Counterexample 2 (Multi-Path Redundancy):**
  - Rule 1: `S` requires `A` and `B`.
  - Rule 2: `A` requires `B`.
  - If `B` is blocked, `walk(S)` walks `A` (which triggers `walk(B)`) and also walks `B` directly.
  - **Result:** Node `B` is evaluated and serialized twice. For deep, highly interconnected dependency trees (e.g., standard US 1040 dependency networks), this redundancy leads to exponential growth of both evaluation time and returned payload size.
* **Consequences:** The explanation walker MUST implement a `visited` set to track symbols in the current stack path (raising an explicit cyclic dependency error) and a memoization cache to avoid traversing the same sub-graph multiple times.

---

### 3. Combinatorial Explosion of Stubs (Shape B)

**The Check:** Does writing stub findings for all unexecuted rules lead to a combinatorial explosion of stubs in the log for large rulesets?

* **Evaluation:** Shape B requires writing stub records (`stub-finding.v1`) to the workspace log for every rule that is blocked or inapplicable.
* **Counterexample Scenario:** 
  - A standard tax ruleset contains thousands of rules spanning dozens of forms (Schedules A, B, C, D, E, F, SE, State returns, etc.).
  - For a simple W-2 filer with no business or investment income, only ~5% of these rules are executed. The other 95% are inapplicable or blocked.
  - If the ruleset contains 2,000 rules, the runner will serialize and write ~1,900 stub findings to the workspace log.
* **Consequences:**
  - **Log Bloat:** A run log that should contain ~100 actual findings will instead contain ~2,000 findings, inflating disk space and serialization/deserialization times.
  - **Runner Performance Degradation:** The runner must spend cycles constructing and verifying stubs for every unexecuted pathway during the execution loop.
  - **Displacement Complexity:** When an input fact changes, a waterfall of rules shifts status. Under Shape B, the runner must retract or update hundreds of stubs, introducing high cache invalidation complexity and garbage collection overhead.

---

### 4. Edge Cases: Validation & Optional Inputs

**The Check:** Identify any edge cases in failed validation constraints or inapplicable optional inputs representation.

#### Failed Validation Constraints (Invalid State)
* **Collection Indices:** If a rule depends on a collection of records (e.g., multiple W-2s) and one record is invalid, the entire collection blocks. The walk payload schema `explanation-walk.v1` specifies:
  ```json
  "failed_constraint": { "type": "string", "description": "Validation constraint description that failed." }
  ```
  This lacks the capability to pinpoint *which* record in the collection failed (e.g., W-2 at index 2). Without this index link, the consumer cannot render a useful validation correction interface.
* **Cross-Field Validation:** If a validation constraint fails due to a relation between two fields (e.g., `spouse_ssn` must not equal `primary_ssn`), the invalidity is shared. Linking this failure to a single "invalid input fact" is insufficient; the schema must support multi-symbol validation targets.

#### Inapplicable Optional Inputs (Fallback Paths)
* **Optional Fallbacks:** Many rules accept optional inputs (e.g., a manual override). If the optional input is not provided, the rule falls back to a standard calculation path. 
  - Under both Shape A and B, how is this represented? If the override rule is skipped, does the walker report it as "blocked" due to a missing dependency, or "inapplicable" due to a failed guard? 
  - If it is reported as a failure, it creates false positives in the explanation UI. The user did not "fail" to provide the override; they simply opted for the standard path. The walk schema must distinguish between *missing mandatory dependencies* and *absent optional inputs*.
* **Alternative Rules:** When two rules publish the same symbol (e.g., Simplified vs. Actual Home Office Deduction):
  - If the user qualifies for both, one is chosen (or one is selected by default). The non-selected rule is inapplicable. 
  - The walk payload needs to indicate that the symbol *was* published, but alternative calculation paths were bypassed, without labeling those bypassed paths as "failures".

---

## Recommendations for Refinement

To address these vulnerabilities, we recommend modifying the proposed **Shape A** rather than adopting Shape B:

1. **Cycle Detection & Memoization:** The walker algorithm must maintain a `visited` set to detect loops and a cache to prevent redundant evaluations of multi-path dependencies.
2. **Runner-Assisted Context:** Instead of the walker trying to parse and evaluate complex/dynamic guards statically, the runner should write a minimal "Inapplicability Trace" or "Execution Map" of which guards failed. This map should be a separate, lightweight lookup structure in the workspace metadata—not a set of individual stub findings in the act log.
3. **Refined Validation and Optional Input Schema:** Update `explanation-walk.v1` to:
   - Include a `record_index` or `fact_id` in validation failures.
   - Distinguish between `missing_mandatory_dependency` and `absent_optional_input`.
