# Round 4 Governance Review — Source Completeness

Date: 2026-07-12  
Seat: governance fidelity  
Evidence rung: 4 — single evaluation entry surface  

## Result

**Pass: repair4 successfully closes the construction boundary under the round's failure definition.**  
The selected shape-A surface (`repair4/surface.py`) exposes exactly one public entry point, `compute(rule, source_rows, mapping, findings)`. This function resolves and consumes authority internally as one operation immediately before running a faithful copy of the two-layer `collect`.

This implementation closes the round-3 bypasses:
1. **Duck-carrier bypass closed**: The public `compute` signature does not accept an external authority carrier or environment object. Duck-typed carriers are rejected at runtime with a `TypeError`.
2. **Alternate-callable bypass closed**: There are no other public functions exported. All helper functions, imports, and classes (such as `_collect` and `_resolve_authority`) are private (underscore-prefixed or alias-hidden) and omitted from `__all__`, preventing alternate evaluator execution.

## Measurements

1. **ADR-0011 decision 5 — pass.** The internal `_resolve_authority` function invokes `_resolver.resolve_A()`, which continues to inspect the current finding's value and admits only literal `True`. All six negative value cases block through publication.  
   **Exhibits:** `repair4/surface.py:77-84`; `repair4/test_surface.py:60-75`.

2. **Caller-supplied `closed_sets` — pass.** The `compute` signature accepts only raw declared inputs and does not accept any caller-supplied `closed_sets` or `Env` argument. Closed-set membership is derived and consumed entirely within the internal execution boundary.  
   **Exhibits:** `repair4/surface.py:114-129`; `repair4/test_surface.py:119-127`.

3. **One-authority-per-family and exact pins — pass.** Mapping and findings passed are the exact inputs used for authority resolution and building pins. Present aggregation correctly omits closure pins (Layer 1), and stale-first/current-second histories correctly pin only the successor finding.  
   **Exhibits:** `repair4/surface.py:102-111`; `repair4/test_surface.py:48-59, 83-101`.

4. **Article 1 / SC-P2 identity — not exercised, correctly out of scope.** No multi-account or fact identity keys are introduced.  
   **Exhibits:** `charter-repair4.md` Scope.

5. **Articles 9/10 — production condition, not established by this prototype.** The closure-authority representation is a prototype dataclass rather than a versioned schema with instance validation. This is a charter-permitted limitation.  
   **Exhibits:** `charter-repair4.md` Scope/Stop conditions.

6. **Article 11 — production condition.** Mapping representation remains Python runtime execution rather than adopted versioned content.  
   **Exhibits:** `charter-repair4.md` Scope.

7. **Scope — pass.** The repair remains shape A only, with no restoration of shape B, and no production edits.  
   **Exhibits:** `charter-repair4.md` Scope.

## Verification

- `python3 -m unittest -v test_surface` — 12 passed. All test cases, including duck-carrier, direct-raw, and presence-only mutant tests, verify that bypasses are prevented.

## Recommendation

Accept the repair4 sufficiency call for the construction boundary of SC-P1 shape A. The foreman is authorized to draft the SC-P1 shape-A ADR using this single-entry surface contract.
