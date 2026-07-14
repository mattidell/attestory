# Examination — Expression Language Extensions it1 (Incumbent)

Date: 2026-07-13. Rung 2 static design + throwaway HEAD probes (outside repo).
Design: `it1/design.md`. HEAD: `d13d1fb`.

## Verdict

| Proposition | Status | Note |
|---|---|---|
| **ELX-P1** declared optional defaults | **Settled at static level** | Mechanism specified; displacement path named; three refuted workarounds explicitly not used. Implementation evidence deferred to milestone. |
| **ELX-P2** categorical comparison | **Settled at static level** | New `match` op; mismatch as contained `DEPENDENCY_INVALID`; migration from ADR-0024 codes specified. |

Paper makes the choices clear; stop at paper per Gate 2 / charter.

## HEAD probes (reproduced impossibility)

| Probe | Result |
|---|---|
| Absent `ref` | `DEPENDENCY_ABSENT` |
| Injector rule + asserted input | Asserted value overwritten |
| Dual publishers same symbol | Both publish; last write wins |
| `compare` on `"single"` | `DEPENDENCY_INVALID` (decimal coercion) |
| Non-optional absent `requires` | Blocks; no publication |

## Case coverage (claim → change → behavior → pins)

| Case | Two + | Two − | Lifecycle | Settled? |
|---|---|---|---|---|
| **1** unasserted age → default SD | Single unasserted → 15000 (two AGIs) | Asserted true → 17000; missing status blocks | Supply → default pins on SD | Yes |
| **2** assert-after-run | R1=15000 default pins; R2=17000 input pins | Mid-state no current SD; unrelated findings unmoved | T0–T6: `F_def_age` root `default_superseded` → derivation edges only → re-run | Yes (trace names every pin/edge in design) |
| **3** asserted false from start | SD=15000 with **input** pin on age | No default-supply for age; injector pattern forbidden | Assert false → skip supply → later correction is ordinary same-fact root | Yes |
| **4** categorical match | MFJ match true; single matches single branch | Wrong label → false; numeric/string match → `DEPENDENCY_INVALID` | Status correction cascade unchanged | Yes |
| **5** non-optional absent | Optionals defaulted when declared; required present publishes | Absent filing_status or AGI blocks as today | Elective status cannot be optional-declared | Yes |

## How ELX-P1 defeats the three refuted constructions

1. **Multi-publisher staging** — defaults are package materializations, not
   second rules publishing the input symbol; unique ownership untouched.
2. **Closure aggregation** — scalar optional declarations only; no `collect`.
3. **Evaluation-order tricks** — pre-saturation supply; not short-circuit
   substitutes for always-applicable taxpayer flags.

## Article 7 / 11 conformance (static)

- **Art. 7:** Edges remain derivation + individuation. `default_superseded` is
  a **root class** (like correction/withdrawal), not a third edge. Dependents
  displace only along existing derivation pins (`default` added to dependency
  roles).
- **Art. 11:** Default values and optionality live in versioned
  `optional-input-declaration.v1`; engine executes declared supply only.
- **E3.1:** Schema forces `nature: determinable`; electives cannot default.
- **Overwrite:** Supply skips when symbol ∈ asserted inputs; structural.

## Unresolved authority questions

1. Confirm ADR-0010 refinement: default-supply findings as roots under
   `default_superseded`, versus kernel-adjacent finding with `fact_id` for
   ordinary correction — both two-edge; design prefers root-class refinement.
2. Production symbol↔fact marshalling for pairing assertions to default-supply
   symbols (scenario layer today is explicit; workspace mapping not yet a
   committed citizen).
3. Spouse optional-vs-required content policy for the conditional package
   (mechanism-neutral).
4. T1: default-supply uses existing derived attribution; no fuller authority
   doctrine constructed.

## Follow-on

Rival clean-room design (plan Gate 4). Governance + adversary review.
Candidate ADR-0025 after convergence. No repo implementation in this iteration.
