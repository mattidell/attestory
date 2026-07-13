# Prototype Evaluation Analysis — Conditional Selectors

Foreman, 2026-07-13. Status: **reopened 2026-07-12 by shadow foreman, owner-directed** — the plan's clean-room rival requirement (Gates 4/8) was not met (the incumbent authored both shapes; see process log), and a repair pass ran without the plan pre-authorizing one. Remediation proceeds owner-paced, starting with an independent re-performance of the round-1 review (round 1R, owner-launched seats). Round-1/2 conclusions stand as evidence but are provisional. Prior text preserved unedited below.

Shape B (First-class Selector Citizen) is recommended with payload-level spousal-case grouping refactoring.

## Decision under evidence

This analysis evaluates how conditional standard-deduction status lookups and tax bracket method/rate selection are modeled and resolved within the derivation cascade.

## Evidence

| Evidence | Contribution |
|---|---|
| `exhibits/conditional-selectors/it1` (`55331c8`) | Shape A (rule cascade) vs Shape B (first-class selector) design, cases, and trace |
| Round 1 reviews/triage | Goverance rejection of Shape B due to implicit defaults and displacement bypass; adversary case matching bugs |
| `prototypes/conditional-selectors/repair1` (`36d2fe8`) | Repaired Shape B with parameters, explicit defaults, V0 absence pinning, mutually exclusive guards, and clamp/null-brackets progressive lookup |
| Round 2 reviews/triage | Governance ratification of repaired Shape B; adversary spousal-case grouping logic leak identified |

The rival requirement is satisfied: iteration 1 compared Shape A (standard rule cascade) and Shape B (first-class selector citizen) across all 5 required cases.

## Supported conclusions

### C1 — First-class Selector Citizen (Shape B) preserves graph simplicity and logic-parameter separation
A dedicated selector citizen consolidates complex conditional branching and optional dependency lookups into a single node. This reduces file count from 9 files (under Shape A's cascade) to 2 files (1 selector, 1 base parameters), preventing dependency graph explosion. Hardcoded constants are factored out to parameter files, satisfying CS-P2.

Evidence: `repair1` design payloads; Round 2 reviews.

### C2 — Optional dependencies require V0 Absence Pinning to preserve displacement integrity
When optional inputs (such as spouse fields for standard deduction adjustments) are unasserted, the runner cannot establish standard version-displacement checks if these inputs are later provided, unless it tracks their absence. By writing a **V0 Absence Pin** for absent optional symbols and evaluating them as their declared default values, the runner can evaluate safely (Article 12) without hardcoded hacks (Article 11). If the optional facts are later asserted at version `v1` or higher, standard version-supersession triggers displacement along the derivation edge, satisfying Article 7's two-edge constraint.

Evidence: `repair1` evaluation mechanics; Round 2 governance approval.

### C3 — Case match conditions must be mutually exclusive and order-independent
To prevent sequential array-index dependencies, case guards must be evaluated concurrently. The runner enforces that exactly one case matches (or executes a declared fallback), throwing a collision error if multiple guards are true.

Evidence: `repair1` collision checks; Round 2 reviews.

### C4 — MFS and QSS must be treated as non-spousal cases to prevent logic leakage
Qualifying Surviving Spouse (QSS) and Married Filing Separately (MFS) receive standard deduction bases and rates but cannot claim additional spouse deductions. Grouping MFS and QSS with MFJ in the spousal case allows unasserted spouse claims to leak into their calculations. They must be grouped under Case 1 (non-spousal), leaving Case 2 strictly for MFJ.

Evidence: Round 2 adversary findings.

---

## Rejected alternatives

- **Shape A (Rule Cascade):** Rejected due to graph density explosion (9 files for standard deduction) and rule-level logic leakage (spouse shares applied to single filers).
- **Implicit Defaulting in Runner:** Rejected as it embeds tax meaning in code (violating Article 11) and derives from unasserted claims (violating Article 12).
- **Default fallback `default: null`:** Rejected. Fallback defaults override fast-failing error checks and hide unsupported status errors.

---

## Production conditions

- Implement `selector-artifact.v1` schema and loader.
- Implement V0 Absence Pinning in the runner.
- Enforce mutual exclusivity and throw `SELECTOR_COLLISION_ERROR` at runtime.
- Clamp taxable income to zero and check sorted order in `bracket_fold`.
- Support `"limit": null` as an infinite upper bound on progressive brackets.
- Refactor standard-deduction cases to place MFS and QSS under Case 1 (non-spousal).
