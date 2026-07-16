# Charter: Repair 1 — Conditional Selectors

Date: 2026-07-13. Iteration 1 reviews triaged; repair pass authorized.

- **Branch:** `prototypes/conditional-selectors/repair1`
- **Builder:** incumbent, Medium/medium (imitation/repair builder), owner-launched external context.
- **Evidence:** Static schemas and design updates with paper walkthroughs.
- **Questions:** Resolution of all decision-blocking findings (CS-G1, CS-G2, CS-A1) and non-blocking defects (CS-A4, CS-A5).

## Assignment

Refactor the Shape B design to resolve all governance violations and adversary defects identified in Round 1 reviews:

1. **Logic/Parameter Separation (CS-G2):**
   - Eliminate all hardcoded numeric deduction amounts and rate constants from standard-deduction case expressions.
   - Show how the selector references external parameter citizen tables.

2. **Optional Defaults & Displacement (CS-G1):**
   - Update `selector-artifact.v1` schema to allow declaring optional inputs along with their explicit default values.
   - Walk through the displacement logic: show how the runner tracks and pins the absence of optional inputs so that if those optional facts are later asserted, the selector finding is correctly displaced, without violating Article 7.

3. **Case Exclusivity & Order Independence (CS-A1):**
   - Update the schema to support a clear default/fallback case.
   - Detail how case matching avoids sequential index dependency (e.g., mutually exclusive guards).

4. **Edge Cases & Statuses (CS-A4, CS-A5):**
   - Support standard deduction cases for all five filing statuses (Single, MFJ, MFS, HoH, QSS).
   - Update the tax brackets parameters and progressive lookup (`bracket_fold`) to handle:
     - An open-ended final bracket (e.g., limit = `null`).
     - Clamping negative taxable income at zero.
     - Sorted limit validation.

## Outputs

- `docs/prototypes/conditional-selectors/repair1/design.md`
- `docs/prototypes/conditional-selectors/examination-repair1.md` (≤120 lines)

The examination states whether all blocked findings are settled, cites all cases, and provides the finalized design schemas and payloads.

## Stop conditions

Stop at static files. No runtime implementation or python script execution.
