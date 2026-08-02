# Governance Review — Conditional Selectors Round 1

Date: 2026-07-13
Seat: governance reviewer
Scope: CS-P1 and CS-P2, measured against the governance set (Constitution, Ontology, and Engineering Constraints) and Iteration 1 design proposals.

## Determination

* **Shape A (Rule-driven Cascade)** is conformant to existing engine architecture. It avoids runner changes and out-of-order execution, but relies on "default-injector rules" (`rule.spouse-over-65-default` and `rule.spouse-blind-default`) to bypass strict saturation blocking when optional inputs (like spouse fields for single filers) are absent. While not a direct violation, this pollutes the workspace with synthetic default facts.
* **Shape B (First-class Selector Citizen)**, as proposed, introduces several violations of the Constitution and Engineering Constraints:
  1. **Runner-Level Hacks / Implicit Defaulting:** The runner resolves missing optional dependencies by implicitly initializing them to `false` or `null` in evaluator code, violating Article 11 (Legibility) and Article 12 (Contract - deriving from unasserted claims).
  2. **Supersession & Dependency Graph Bypass:** Under Shape B, the runner bypasses tracking the *absence* of optional dependencies. If these are subsequently asserted, the cascade cannot track that it needs to displace the selector finding without introducing a non-standard dependency edge on the *absence* of a fact, violating Article 7 (Supersession - no third edge).
  3. **Violation of Logic/Parameter Separation (CS-P2):** The standard deduction selector payload in Shape B hardcodes numerical values (`15000`, `30000`, `2000`, `1550`) directly inside the selector's case logic instead of querying structured parameter citizens. This violates the core tenet of CS-P2 and the separation of concerns.

Therefore, the Governance Reviewer **rejects Shape B in its current proposed form**. We recommend either proceeding with Shape A with cleaner default handling, or revising Shape B to resolve the governance violations (e.g. declaring defaults in the schema, referencing parameter tables, and maintaining strict version pinning and displacement for optional dependencies).

---

## Governance basis

- **Article 7 (Supersession):** Displacement propagates only along derivation and individuation edges. Currency is derived, never stored.
- **Article 11 (Legibility):** All tax meaning lives in declared, versioned rule artifacts. The engine is thin and executes what artifacts declare.
- **Article 12 (Contract):** Derivation consumes findings and artifacts only, never unasserted claims.
- **Article 13 (Publication):** Computation publishes complete derived findings and is not allowed to use fixed form-order orchestration or internal runner-level eligibility/default hacks.
- **CS-P2 (Separation of Logic/Parameters):** Standard deduction and tax bracket lookup tables must be represented as structured parameter citizens that rules query, preserving separation between logic and data.

---

## Conformance Evaluation

### 1. Execution Order and Runner-Level Hacks (Article 11 & Article 13)

* **Shape A (Pass):** Uses the existing saturation runner. Evaluation sequence follows the dataflow dependency graph. No out-of-order execution or runner modifications are introduced. Default-injector rules are standard rule artifacts, although they add complexity to the dependency graph.
* **Shape B (Fail):**
  - **Implicit Defaulting:** The runner resolves missing optional dependencies by initializing them to `false` or `null` internally. This behavior is embedded in runner code rather than in the artifact or schema, violating Article 11's requirement that all tax meaning live in declared, versioned artifacts.
  - **Derivation from Unasserted Claims:** Article 12 states that derivation consumes findings and artifacts only, never unasserted claims. By defaulting missing optional facts to `false` or `null` inside the runner, the system derives a standard deduction value from unasserted spouse claims.
  - **Dynamic Dependencies & Displacement (Article 7):** If a taxpayer's spouse information is initially unasserted, the standard deduction is derived without pinning those spouse findings. If the spouse facts are subsequently asserted, the standard deduction finding must be displaced. However, because the optional spouse inputs were missing during the first run, the derived finding does not carry their versions as pins. Without pinning them or registering a dependency on their absence, the engine cannot trigger displacement when they are added. Tracking the absence of facts requires a non-standard dependency edge, which violates the strict two-edge (derivation/individuation) constraint of Article 7.

### 2. Selector Schema and Append-Only Invariants (Article 9 & Article 10)

* **Shape A (Pass):** Uses existing production-ready schemas which are strictly append-only.
* **Shape B (Partial Pass / Schema Laxity):**
  - The proposed `selector-artifact.v1.schema.json` is clean and defines a versioned citizen.
  - It does not directly violate append-only invariants, as the outputs are published as standard derived findings.
  - However, the schema suffers from the same laxity as the rule-language prototype: the expression grammar is undefined, and the output types are unconstrained.

### 3. Logic and Parameter Separation (CS-P2)

* **Shape A (Pass):** Perfectly preserves separation. All thresholds and rates are in parameter citizens (`demo.parameter.standard-deduction-base.2025` and `demo.parameter.additional-deduction-rate.2025`). Rules contain only logic and reference these parameters.
* **Shape B (Fail):**
  - The standard deduction selector (`selector.standard-deduction.2025.json`) hardcodes values (`15000`, `30000`, `2000`, `1550`) directly inside the selector logic.
  - No parameter query is performed for standard deduction. This directly violates the Topic Plan's requirement (CS-P2) that standard deduction lookup tables are represented as structured parameter citizens.
  - Embedding annual parameters inside a logic artifact means that any change in annual tax thresholds requires a rewrite or duplication of the selector artifact itself.

---

## Detailed Tradeoff Matrix

| Governance Dimension | Shape A (Rule-driven Cascade) | Shape B (First-class Selector) | Governance Status |
| :--- | :--- | :--- | :--- |
| **Runner Purity (Art 11)** | **High.** Runner has no knowledge of optional defaulting; all logic is explicit in rules. | **Low.** Runner must implement defaulting conventions (`false`/`null`) for missing optional facts. | Shape A passes; Shape B violates Article 11. |
| **Dependency Integrity (Art 7/12)** | **High.** Strict static dependency pins. Missing inputs explicitly block rule execution. | **Low.** Fragile. Either fails to displace when optional inputs are added, or requires a third edge (absence dependency). | Shape A passes; Shape B violates Articles 7 and 12. |
| **Logic/Parameter Separation (CS-P2)** | **High.** All standard deduction values and tax brackets are in parameter files. | **Low.** Hardcodes standard deduction rates and thresholds inside the logic cases. | Shape A passes; Shape B violates CS-P2. |
| **Graph Complexity** | **High.** Requires 7 rules, 2 parameter files, and 2 default-injectors (9 files total). | **Low.** Grouped into 1 selector and 1 base parameter (2 files total). | Tradeoff: Graph density vs. architectural correctness. |
| **Explainability (Art 15)** | **High.** Chain of 7 explicit rule executions pins every intermediate value. | **Medium.** Single derived finding hides case branch complexity from the cascade trace. | Shape A passes; Shape B simplifies trace at the cost of detail. |

---

## Recommendations

1. **Reject Shape B in its current proposed form.** The benefits of reduced graph density are outweighed by the serious architectural violations of Articles 7, 11, 12, and CS-P2.
2. **Proceed with Shape A as the baseline.** Shape A conforms fully to the Constitution and Engineering Constraints. The complexity of default-injectors is a legitimate, explicit trade-off of the declarative saturation model.
3. **Alternative Direction for Iteration 2 (Refined Shape B):**
   If the foreman chooses to pursue Shape B to address graph complexity, the builder must submit a revised design that:
   - Eliminates hardcoded numbers in selectors, instead resolving values via references to external parameter citizens (restoring CS-P2).
   - Declares the default values for optional dependencies explicitly in the schema and selector payload (e.g., `"optional": [{"name": "spouse_over_65", "default": false}]`), rather than letting the evaluator code implicitly default them (restoring Article 11).
   - Solves the displacement problem when optional inputs are asserted, showing how the runner tracks and pins the absence of optional inputs without violating Article 7.
