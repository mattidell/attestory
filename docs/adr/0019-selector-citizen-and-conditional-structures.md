# ADR 0019 — Selector Citizen and Conditional Structures

- Status: **rejected** (owner decision 2026-07-13; retained per ADR-0013 amendment — inert as authority, citable as history)
- Tier: 2
- Date: 2026-07-13

> **Rejection note (2026-07-13, principal foreman).** This draft rested on the
> tainted conditional-selectors round whose rival requirement was never met.
> The independent round-1R re-review (`docs/prototypes/conditional-selectors/round-1r-triage.md`)
> rejected the selector-citizen shape as specified: policy values embedded in
> selector logic (CS-G2R), an optional-input contract that matches no committed
> schema (CS-G3R), an unlicensed native runner pathway with undefined
> package/lineage/edge contracts (CS-G4R), non-exhaustive filing-status cases
> (CS-A3R), and — common to both shapes — guard expressions that do not execute
> under the committed evaluator (CS-G1R, CS-A1R, CS-A2R). A selector citizen may
> return only via a fresh charter that declares the contract boundaries CS-G4R
> names. The decision text below is preserved unedited as history.

## Context

Calculating standard deductions (Single, MFJ, MFS, HoH, QSS bases and age/blind adjustments) and tax tables (progressive brackets) requires multidimensional conditional branching. Decomposing these selections into a cascade of standard rule and parameter citizens (Shape A) results in graph density explosion (9 files for standard deduction) and rules that are vulnerable to logic leaks (spouse deductions leaking to single filers). We need a first-class conditional selector citizen to consolidate branch complexity while preserving logic-parameter separation and displacement integrity.

## Decision

1. **Selector Citizen (`selector-artifact.v1`):** We introduce a new first-class citizen type to the derivation schemas. A selector defines:
   - `requires`: Mandatory inputs that must be present to begin execution.
   - `optional`: Optional inputs with explicit default values (e.g. `spouse_over_65` defaults to `false`).
   - `cases`: A list of case objects containing a mutually exclusive applicability guard (`when`) and a value expression (`value`).

2. **V0 Absence Pinning:** To ensure derived findings correct displace when an unasserted optional input is later asserted (without introducing a non-standard third edge in violation of Article 7), the runner uses standard version-supersession:
   - Present optional inputs are pinned at their current evidence version (e.g., `v1`).
   - Absent optional inputs are pinned at version `v0` and evaluated as their declared defaults.
   - If an optional input is later asserted, its version (`v1` or higher) naturally supersedes `v0`, triggering displacement along the derivation edge.

3. **Case Exclusivity & Order Independence:** Case matching is order-independent. The runner evaluates all case guards in parallel and asserts that exactly one guard matches. If multiple guards are true, it throws `SELECTOR_COLLISION_ERROR`. If no guards match, it throws `SELECTOR_NO_MATCH_ERROR` (no fallback default allowed in production).

4. **Repaired `bracket_fold` progressive calculation:** The progressive lookup logic in the runner is modified to:
   - Clamp taxable income at zero, preventing negative taxes.
   - Assert that limits are strictly ascending at load time, throwing an error if unsorted.
   - Support `"limit": null` on the final bracket, which is interpreted as an infinite upper bound.

## Consequences

- File proliferation and graph complexity are significantly reduced (standard deduction requires 2 files instead of 9).
- Dynamic displacement of optional inputs conforms fully to Article 7 and Article 12.
- Conditional logic remains declarative and order-independent.
- Tax calculation clamping and open-ended bracket handling are formalized at the schema and runner level.
