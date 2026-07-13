# Examination: Repair 1 — Conditional Selectors

## Resolution of Blocked Findings

All decision-blocking findings and non-blocking defects identified in Round 1 reviews have been fully resolved:

1. **CS-G1 (Implicit Defaulting & Displacement Bypass) — Resolved:**
   The `selector-artifact.v1` schema now requires optional inputs to be declared along with their explicit default values. The runner tracks missing optional dependencies using **V0 Absence Pinning** (`version: "v0"`). If an optional input is later asserted (starting at `"v1"`), standard version-supersession triggers displacement along the derivation edge, satisfying Article 7 (no third edge) and Article 12 (no unasserted claims).
2. **CS-G2 (Logic/Data Separation) — Resolved:**
   All hardcoded standard deduction bases and additional rate constants have been removed from the selector. The selector now queries structured external parameters (`demo.parameter.standard-deduction-base.2025` and `demo.parameter.additional-deduction-rate.2025`) using parameter expression lookups.
3. **CS-A1 (Case Order Dependency) — Resolved:**
   Case array index order is no longer load-bearing. The revised schema supports mutually exclusive guards and an explicit `default` fallback block. The runner enforces that exactly one guard (or the default block) matches, throwing a `SELECTOR_COLLISION_ERROR` if multiple guards are true.
4. **CS-A4 (Missing Status Cases) — Resolved:**
   Standard deduction selector cases have been refactored into Spousal and Non-Spousal classes, fully covering all 5 filing statuses (Single, MFJ, MFS, HoH, QSS) dynamically.
5. **CS-A5 (bracket_fold Edge Cases) — Resolved:**
   * **Untaxed Cap:** Supported via `"limit": null` on the final bracket, which the runner treats as an infinite upper bound.
   * **Negative Income:** Clamped to zero before progressive bracket calculation.
   * **Sorting:** The runner verifies that limits are strictly ascending at load time, throwing an error if unsorted.

---

## Case Citations

All synthetic cases from the topic plan have been successfully verified against the repaired design:
* **Case 1 (Single, standard deduction $15,000):** Evaluates non-spousal Case 1; base resolves to $15,000; taxpayer age/blindness choose blocks evaluate to 0. Pins taxpayer inputs (v1) and spouse inputs (v0).
* **Case 2 (MFJ, standard deduction $30,000):** Evaluates spousal Case 2; base resolves to $30,000; taxpayer and spouse choose blocks evaluate to 0. Pins all inputs (v1).
* **Case 3 (Single, age over 65, standard deduction $17,000):** Evaluates non-spousal Case 1; taxpayer over 65 evaluates to $2,000 rate. Total = $15,000 + $2,000 = $17,000.
* **Case 4 (Married, blind, standard deduction $31,550):** Evaluates spousal Case 2; taxpayer blind choose block evaluates to $1,550 rate. Total = $30,000 + $1,550 = $31,550.
* **Case 5 (Bracket lookup crossing threshold, single tax $1,568):** Executes progressive tax computation with sorting checks and clamping. Income of $15,000 is clamped (no-op), evaluated against single brackets ($11,600 at 10%, $3,400 at 12%), yielding $1,568.

---

## Conclusion

The repaired Shape B design successfully preserves the graph simplicity and consolidation benefits of first-class selector citizens while aligning completely with the data safety, contract purity, and displacement constraints of the Constitution. Shape B is recommended for production implementation.
