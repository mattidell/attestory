# Triage: Conditional Selectors Round 1

Date: 2026-07-13
Foreman: Codex Foreman

This document records the triage of findings from Round 1 reviews of the `conditional-selectors` prototype, in accordance with Gate 5 of the prototype process.

## Findings Classification

### 1. Decision-Blocking Findings (Must be resolved before design ratification)

* **CS-G1 (Shape B Implicit Defaulting & Displacement Bypass):** **Decision-Blocking.** 
  - *Description:* Resolving unasserted optional inputs to `false` inside runner code violates Articles 11 and 12. Furthermore, bypassing dependency tracking for absent inputs prevents correct displacement propagation when they are later asserted, violating Article 7.
  - *Resolution:* Shape B must be revised to declare defaults explicitly in the selector schema or payload, and the displacement mechanism must correctly register dependencies on optional inputs whether present or absent.
* **CS-G2 (Shape B Logic/Data Hardcoding - CS-P2 Violation):** **Decision-Blocking.**
  - *Description:* Hardcoding standard deduction amounts directly in value expressions violates CS-P2.
  - *Resolution:* Shape B must be refactored to fetch rates and bases from structured parameter tables via parameter references.
* **CS-A1 (Shape B Case Order Dependency):** **Decision-Blocking.**
  - *Description:* Sequential first-match logic makes array index order load-bearing and error-prone, lacking exclusivity checks.
  - *Resolution:* Revised Shape B schema must support mutually exclusive guards, or explicitly declare a fallback case.

### 2. Production Conditions (To be addressed during production implementation)

* **CS-A3 (Shape A Publisher Collisions):** **Production Condition.**
  - *Description:* Asserting inputs on default-injected fields causes publisher collisions.
  - *Resolution:* The workspace service layer or runner admission logic must handle or prevent input conflicts with default-injectors.

### 3. Non-Blocking Defects & Deferred Breadth (Log and defer / easily repairable)

* **CS-A2 (Shape A Logic Leakage):** **Non-Blocking Defect.**
  - *Description:* Single filers receive spouse deductions if spouse inputs are asserted.
  - *Resolution:* Can be easily fixed in Shape A by adding filing status guards directly to the share-counting rules.
* **CS-A4 (Shape B Missing Status Cases):** **Non-Blocking Defect.**
  - *Description:* Lack of HoH, MFS, QSS standard deduction cases.
  - *Resolution:* Easily fixed by expanding case payloads in the next design draft.
* **CS-A5 (bracket_fold Progressive Edge Cases):** **Non-Blocking Defect.**
  - *Description:* Untaxed income above highest bracket limit, negative income calculations, and sorting dependencies.
  - *Resolution:* To be fixed by updating the parameter schemas to support `null` limit for the final open bracket, clamping tax calculation at zero, and verifying sorting at load time.

---

## Foreman Recommendation

Although Shape A is conformant out-of-the-box, it leads to significant graph density and file explosion (9 files for standard deduction alone). Shape B's consolidation is highly desirable for long-term scalability, but it is rejected due to major Article 7, 11, 12, and CS-P2 violations.

We recommend executing a **repair pass (`repair1`)** to salvage Shape B. The builder will be chartered to write a revised Shape B design that:
1. References external parameter files instead of hardcoding values.
2. Formally declares optional inputs and their defaults in the schema/payload.
3. Outlines how the runner tracks absent optional dependencies to ensure correct displacement without violating Article 7.
4. Corrects the sequential case ordering issue and progressive bracket edge cases.
