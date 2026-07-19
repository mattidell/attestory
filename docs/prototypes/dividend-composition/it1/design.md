# Design: Dividend Composition (D3, Incumbent It1)

This design instantiates the ADR-0015/0016 statement-family-composition pattern for 1099-DIV (ordinary and qualified dividends) under the charter constraints.

## D3-P1: Statement Identity and Family
**Implement Normally.** The 1099-DIV statement instance and family follow the ADR-0015/0016 pattern (payer/subject/year/instance keys). This provides the substrate.

## D3-P2: Ordinary-Dividend Composition (Line 3b) and Declared Universe
The `dividend-composition.v1` schema declares the universe for ordinary dividends.

1. **Declared Universe:** The composition strictly declares `div_ordinary` (box 1a) and `div_qualified` (box 1b) as its constituent slots.
2. **Recorded Non-Composable Exclusions:** The statement fact type (`f1099div-stmt`) accepts boxes 1a, 1b, 2a, 3, 5, 7, and 12 in its `value_schema`. However, the family composition `div_ordinary` is strictly tied to 1a, and `div_qualified` to 1b. The out-of-universe boxes (2a, etc.) are recorded on the fact but ignored by the composition rule.
3. **Box-2a Visibility:** Because box 2a is present on the statement fact, a separate return-level disposition (e.g. `requires-schedule-d`) can query the `f1099div` family for any member with `box_2a > 0`. This disposition feeds D2's contradiction check (walking the trace from the specific statement fact to the return-level block). Contrast with box 7 (foreign tax), which is recorded but not linked to D2.

## D3-P3: Qualified Subset (Line 3a) with Structural Enforcement
Line 3a (qualified dividends) composes from box 1b. The invariant 1b <= 1a per statement and 3a <= 3b per line is structurally enforced.

### Locus: Admission Machinery + Composition Contract
The subset relation is enforced at **both** admission and composition to provide safety and structural integrity:

1. **Admission (The Kill-Case):** JSON Schema cannot express cross-field comparisons (1b <= 1a). The `fact-type.v2` schema introduces an `invariants` array (e.g., `["box_1b <= box_1a"]`). The kernel's `_validate_finding` (in `packages/kernel/findings.py`) evaluates these invariants. A contribution asserting 1b > 1a is rejected with a `FindingModelError` and never recorded, fulfilling the honest-blocking/no-silent-drop mandate.
2. **Composition Contract (Line-Level Construction):** A new `subset-composition.v1` citizen (or `dividend-composition.v1` with subset semantics) explicitly declares `div_qualified` as a subset of `div_ordinary`. Both lines are constructed from the *same* closed family and horizon. Because every statement in the family satisfies 1b <= 1a (enforced at admission), and both lines sum over the exact same set of statements, the line-level relation 3a <= 3b holds by mathematical construction.
3. **The Guard:** If the declared sets could diverge (e.g., `3a` was configured to read a different family horizon than `3b`), the invariant would break. The composition contract guards this by defining the subset *within the same composition definition* — evaluating both lines atomically against a single family closure read.

## Empty Family Closure
An empty family (no statements) closes honestly. A literal-true closure of the 1099-DIV family with zero members yields subtotal 0 for both 3a and 3b. If the family is undeclared/unclosed, it remains an open input, blocking both lines (ADR-0016).
