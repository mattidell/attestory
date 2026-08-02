# Round 1 Adversary Review — Expression Language Extensions

Date: 2026-07-14  
Seat: adversary reviewer, Medium/medium  
Evidence rung: paper and static-table only  

I reviewed `plan.md`, this seat's charter, the two paper builders, and their examinations. I did not read the Governance reviewer's output (`reviews/round-1-governance.md`) or any draft of ADR-0025. No code or production contract was available to run; the exhibits below are the declared paper behavior.

---

## Method

I mounted concrete counterexamples and adversarial scenarios against both `it1` (incumbent) and `it2` (clean-room rival) designs across the five assigned categories:
1. **The three refuted workarounds** (staged multi-publisher rules, closure-aggregation misuse, and evaluation-order tricks).
2. **Displacement ordering** (assert-after-run, assert-then-supersede, default-then-remove, and default-value change).
3. **Pin-origin integrity** (local and transitive traceability of default origins).
4. **Categorical comparison** (type mismatch, invalid enum values, legacy numeric codes, and migration windows).
5. **Case-5 floor** (non-optional absent inputs).

---

## Adversarial Measurements and Findings

### ELX-A1: Multi-Default Collision Under Package Upgrade (ELX-P1)
* **Applies to:** Incumbent (`it1/`)
* **Classification:** `decision-blocking`
* **Scenario:** A package is upgraded (revision changes) and a default parameter value changes (e.g. from `false` to `true`) with no assertion present.
  - *Input state:* Run 1 under Package v1 (default age `false`). `F_def_age_v1` is published and current. Downstream `F_sd_v1` pins it. Then Package v2 is adopted (default age `true`). Run 2 is executed.
  - *Expected result:* `F_def_age_v1` and its dependent `F_sd_v1` must be displaced. `F_def_age_v2` must become the sole current default-supply finding.
  - **Incumbent fails:** The incumbent's `default_superseded` root class is only triggered when a *kernel finding* (assertion) becomes current. An upgraded default is a derived publication, not a kernel finding, so no displacement root is created. Because derived findings have no `fact_id` in the incumbent design, they do not participate in same-fact correction folding. Both `F_def_age_v1` and `F_def_age_v2` remain current in the workspace, causing a Multi-Default Collision and breaking the single-value constraint.
  - **Rival survives:** The rival assigns the default finding the same `fact_id` as the asserted finding (via `resolved_input.fact_id`). Both default findings share the same `fact_id` and participate in the same-fact correction fold. The newer `D-age0_v2` automatically corrects and displaces `D-age0_v1`, which propagates displacement to `D-std0`.

### ELX-A2: Transitive Loss of Pin-Origin Integrity (ELX-P1)
* **Applies to:** Incumbent (`it1/`)
* **Classification:** `production condition`
* **Scenario:** A downstream consumer (e.g., `tax` or `taxable`) needs to report whether its lineage depends on an optional default.
  - *Expected result:* Transitive default provenance must be locally inspectable at every level of the derived finding graph without recursively walking the entire upstream tree.
  - **Incumbent fails:** The incumbent adds a `default` pin role, but it is only recorded on the immediate consumer (`standard_deduction`). Downstream derived findings (`taxable`, `tax`) pin their immediate inputs as ordinary `input` pins. A renderer or explanation walker looking at `taxable`'s pins cannot locally distinguish whether the input was derived from a default or an assertion.
  - **Rival survives:** The rival adds a required `origin` field (`"assertion"` or `"declared_default"`) to every `input` pin. Downstream rules copy this origin dynamically (e.g., `D-taxable0` pins `D-std0` with `origin: "declared_default"`). Transitive origin integrity is preserved locally at every level.

### ELX-A3: Silent Fallback on Invalid Category Assertions (ELX-P2)
* **Applies to:** Incumbent (`it1/`)
* **Classification:** `decision-blocking`
* **Scenario:** The user asserts an invalid value for a categorical fact (e.g., `filing_status` = `"MFJ"` instead of `"married_filing_jointly"`).
  - *Expected result:* The run must block honestly on `DEPENDENCY_INVALID` or equivalent, flagging the malformed assertion.
  - **Incumbent fails:** The incumbent's generic `match` op performs a plain string comparison. Since `"MFJ"` is a valid string, the comparison `"MFJ" == "married_filing_jointly"` silently returns `False`. The rule continues evaluating without blocking, treating the invalid assertion as a simple mismatch. This violates E9.1 (no tolerant readers) and conceals the error.
  - **Rival survives:** The rival's `categorical_compare` checks enum membership against the fact type's declared string enum at runtime, raising `DEPENDENCY_INVALID` and blocking the rule honestly.

### ELX-A4: Silent Fallback on Categorical Domain Mismatches (ELX-P2)
* **Applies to:** Incumbent (`it1/`)
* **Classification:** `decision-blocking`
* **Scenario:** A legacy numeric fact code (e.g., `"1"` for Single) is bound to a category guard expecting a string label (e.g., `"single"`).
  - *Expected result:* The mismatch must be caught statically or block honestly at runtime to prevent logic errors.
  - **Incumbent fails:** The incumbent's `match` op compares `"1"` and `"single"`. Since both are strings, it silently returns `False`. The Single rule path is evaluated as false, causing standard deduction to block on inapplicability or default to single without warning.
  - **Rival survives:** The rival's package validator rejects legacy bindings statically as `MEMBER_SCHEMA_INVALID` when knowable. If a mismatch occurs at runtime, it raises `CATEGORICAL_DOMAIN_MISMATCH` and blocks honestly, preventing silent logic failures.

### ELX-A5: Dual-Read and Silent Conversion in Migration Window (ELX-P2)
* **Applies to:** Incumbent (`it1/`)
* **Classification:** `decision-blocking`
* **Scenario:** Upgrading a package from ADR-0024 interim numeric codes to first-class string labels.
  - *Expected result:* No silent conversion of human findings; legacy packages must be blocked from dual-reading codes and labels.
  - **Incumbent fails:** The incumbent provides no explicit migration design, stating only that content upgrades in the milestone. This leaves a major risk of silent conversion or dual-reading during transition.
  - **Rival survives:** The rival proposes an explicit migration pathway (mapping citizen, successor claim, and manual user assertion). Categorical rules reject legacy bindings statically during package validation, preventing any dual-reading.

### ELX-A6: Resistance to the Three Refuted Workarounds (ELX-P1)
* **Applies to:** Incumbent (`it1/`) and Rival (`it2/`)
* **Classification:** `non-blocking`
* **Scenario:** Can the default mechanism be subverted to reconstruct multi-publisher staging, closure-aggregation, or evaluation-order tricks, particularly for the taxpayer's own age flag (`taxpayer_age65`) where no false guard exists to short-circuit?
  - **Both designs survive:** 
    - Both designs restrict defaults to package materializations (no multi-publisher rules writing the symbol).
    - Both designs operate on scalar types directly (no closure-aggregation).
    - Both designs evaluate defaults prior to rule execution (no evaluation-order tricks).

### ELX-A7: Displacement on default-then-remove (ELX-P1)
* **Applies to:** Incumbent (`it1/`) and Rival (`it2/`)
* **Classification:** `non-blocking`
* **Scenario:** A user asserts an input (displacing the default), then later withdraws/removes that assertion.
  - *Expected result:* The default must correctly reactivate.
  - **Both designs survive:** 
    - The incumbent's `default_superseded` rule is no longer active once the displacing kernel finding is withdrawn/displaced, restoring the default finding to currency.
    - The rival's input resolver detects that no current assertion exists and publishes a new default-resolution finding `D-age0_v2` in the next run, which corrected the displaced assertion and restored the default.

### ELX-A8: Case-5 Floor (ELX-P1)
* **Applies to:** Incumbent (`it1/`) and Rival (`it2/`)
* **Classification:** `non-blocking`
* **Scenario:** A non-optional absent input (e.g. `adjusted_gross_income`) is omitted.
  - *Expected result:* The run must block on `DEPENDENCY_ABSENT` exactly as today.
  - **Both designs survive:** Neither design defaults non-optional inputs; the Case-5 floor is maintained.

---

## Proposition Disposition

| Proposition | Design | Adversary Verdict | Reason |
|---|---|---|---|
| **ELX-P1** (optional default) | Incumbent (`it1/`) | `reject` | Fails on package upgrade default value changes (ELX-A1) and transitive pin-origin loss (ELX-A2). |
| **ELX-P1** (optional default) | Rival (`it2/`) | `accept` | Survives multi-default collision via same-fact-ID correction folding and preserves pin-origin integrity. |
| **ELX-P2** (categorical compare) | Incumbent (`it1/`) | `reject` | Fails on invalid assertions (ELX-A3), domain mismatches (ELX-A4), and has no governed migration (ELX-A5). |
| **ELX-P2** (categorical compare) | Rival (`it2/`) | `accept` | Enforces domain invariants statically/runtime, prevents silent fallbacks, and defines a governed migration pathway. |

Advisory: the owner decides disposition.
