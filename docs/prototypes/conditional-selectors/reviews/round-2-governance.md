# Governance Review — Conditional Selectors Round 2

Date: 2026-07-12
Seat: governance reviewer
Scope: Verification of Shape B Repair Pass against the governance set (Constitution, Ontology, and Engineering Constraints) and Iteration 1 triage.

## Determination

The revised **Shape B (First-class Selector Citizen)** design, as detailed in [design.md](file:///Users/mattidell/git/personal/finances/docs/prototypes/conditional-selectors/repair1/design.md) and examined in [examination-repair1.md](file:///Users/mattidell/git/personal/finances/docs/prototypes/conditional-selectors/examination-repair1.md), successfully resolves all previously identified governance violations (**CS-G1** and **CS-G2**), as well as associated design defects (**CS-A1**, **CS-A4**, and **CS-A5**). 

The Governance Reviewer **accepts Shape B for production implementation**.

---

## Governance Basis

- **Article 7 (Supersession):** Displacement propagates only along derivation and individuation edges. No third edge types or specialized absence-tracking edges are permitted.
- **Article 11 (Legibility):** All tax meaning lives in declared, versioned rule/selector artifacts. The engine remains thin and must not contain implicit defaulting or hardcoded logic pathways.
- **Article 12 (Contract):** Derivation consumes findings and artifacts only, never unasserted claims.
- **CS-P2 (Logic/Parameter Separation):** Computational logic must remain separated from annual parameters (e.g., deduction amounts, tax bracket thresholds).

---

## Conformance Evaluation

The repaired design was evaluated against the four core governance questions:

### 1. Does it eliminate hardcoded values and maintain logic/parameter separation? (CS-G2 / CS-P2)
**Yes (Pass).**
The revised standard deduction selector payload ([demo.selector.standard-deduction.2025.json](file:///Users/mattidell/git/personal/finances/docs/prototypes/conditional-selectors/repair1/design.md#L167-L252)) has eliminated all hardcoded numeric constants (e.g., `15000`, `30000`, `2000`, `1550`). Instead, it references external parameter tables via the standard parameter operator:
* Base amounts are fetched from [demo.parameter.standard-deduction-base.2025.json](file:///Users/mattidell/git/personal/finances/docs/prototypes/conditional-selectors/repair1/design.md#L107-L123) using `{ "op": "parameter", "parameter_id": "demo.parameter.standard-deduction-base.2025", "key": { "op": "ref", "name": "filing_status" } }`.
* Additional rates are fetched from [demo.parameter.additional-deduction-rate.2025.json](file:///Users/mattidell/git/personal/finances/docs/prototypes/conditional-selectors/repair1/design.md#L125-L142) using `{ "op": "parameter", "parameter_id": "demo.parameter.additional-deduction-rate.2025", "key": { "op": "ref", "name": "filing_status" } }`.

This successfully maintains logic/parameter separation. Modifying yearly standard deduction thresholds or rates will now only require updating the parameter artifacts, avoiding selector code modifications or logic duplication.

### 2. Does the "V0 Absence Pining" model conform to Article 7 (no third edge) and Article 12 (no unasserted claims)? (CS-G1)
**Yes (Pass).**
* **Article 7 Conformance:** The runner achieves optional dependency displacement without introducing a "third edge" (such as a specialized absence-tracking edge). By recording a **V0 Absence Pin** (`{"role": "input", "id": "spouse_over_65", "version": "v0"}`) for absent optional inputs, the runner utilizes standard version-supersession. When a user subsequently asserts `spouse_over_65`, it enters the workspace at version `"v1"`. Because `"v1"` supersedes `"v0"`, the derived finding"s pin becomes stale, triggering normal displacement. This is elegant, standard, and fully conformant with Article 7.
* **Article 12 Conformance:** The runner does not derive findings from unasserted claims. Instead, the absence of the input is explicitly treated as a versioned state (pinned as `"v0"`). The default value is bound using the contractually declared default in the selector"s schema rather than implicit runner-level logic, ensuring the derivation consumes only declared and versioned artifacts.

### 3. Does it declare optional defaults explicitly in the schema? (CS-G1)
**Yes (Pass).**
The refined `selector-artifact.v1.schema.json` explicitly defines the `optional` property:
```json
    "optional": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["symbol", "default"],
        "additionalProperties": false,
        "properties": {
          "symbol": { "type": "string", "minLength": 1 },
          "default": { "type": ["string", "number", "boolean", "null"] }
        }
      },
      "uniqueItems": true
    }
```
In the payload, the default values for `spouse_over_65` and `spouse_blind` are declared as `false`. This completely removes implicit defaulting logic from the runner and places it in the declarative artifact, satisfying Article 11 (Legibility).

### 4. Are case match conditions mutually exclusive and order-independent? (CS-A1)
**Yes (Pass).**
The repaired evaluation algorithm avoids sequential array-index dependencies:
* **Exclusivity Enforcement:** The runner evaluates the `when` guards for all cases. If > 1 guard evaluates to `true`, the runner aborts and raises a `SELECTOR_COLLISION_ERROR`.
* **Order Independence:** Since guards are required to be mutually exclusive, the order of cases in the array is not load-bearing.
* **Explicit Fallback:** An explicit `default` fallback is supported. If no cases match, the default value is returned; if no default is specified, the runner raises `SELECTOR_NO_MATCH_ERROR`.

---

## Detailed Tradeoff Matrix (Updated)

The updated matrix compares the repaired Shape B against Shape A:

| Governance Dimension | Shape A (Rule-driven Cascade) | Shape B (First-class Selector - Repaired) | Governance Status |
| :--- | :--- | :--- | :--- |
| **Runner Purity (Art 11)** | **High.** Runner has no knowledge of optional defaulting; all logic is explicit in rules. | **High.** All default values are explicitly declared in the selector payload, keeping runner thin. | Both pass. |
| **Dependency Integrity (Art 7/12)** | **High.** Strict static dependency pins. Missing inputs explicitly block rule execution. | **High.** V0 Absence Pinning tracks absent inputs, enabling correct displacement via standard version-supersession. | Both pass. |
| **Logic/Parameter Separation (CS-P2)** | **High.** All standard deduction values and tax brackets are in parameter files. | **High.** Numeric values and rates are successfully factored out into parameter citizens and queried via expressions. | Both pass. |
| **Graph Complexity** | **High.** Requires 7 rules, 2 parameter files, and 2 default-injectors (9 files total). | **Low.** Consolidated into 1 selector and 3 parameter files (4 files total). | Repaired Shape B provides a cleaner dependency graph. |
| **Explainability (Art 15)** | **High.** Chain of 7 explicit rule executions pins every intermediate value. | **High/Medium.** Case guards are mutually exclusive and order-independent; output carries clear input version pins. | Both pass. |

---

## Conclusion & Recommendations

1. **Ratify Repaired Shape B:** The revised design successfully resolves the architectural boundaries, dependency pinning, and logic-parameter separation issues that led to the rejection of the initial draft.
2. **Transition to Milestone Execution:** We recommend merging these design schemas and moving to the production implementation phase. The runner must be updated to implement V0 Absence Pinning and Case Exclusivity Checks as described in the refined design.
