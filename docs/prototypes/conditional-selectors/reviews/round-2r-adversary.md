# Review: Round 2R (Adversary) — Conditional Selectors, Iteration 2

Independent adversary review of the clean-room rival's iteration 2 (`it2/design.md`, `examination-it2.md`) under `charter-it2.md`. Evaluated against the committed `packages/derivation/evaluator.py`, `packages/derivation/runner.py`, and `docs/governance/` at `HEAD`.

---

## Finding CS-A10R: Evaluation Order Block on Absent Spouse Inputs for Non-Spouse Statuses (Decision-Blocking)

**Input State:** `filing_status_code` is `"1"` (Single), `"4"` (HoH), or `"5"` (QSS), and `spouse_age65` or `spouse_blind` is absent from `symbols`.

**Expected Result:** `r.standard-deduction` resolves to the base standard deduction amount ($15,000 for Single, $22,500 for HoH, $30,000 for QSS) without blocking, since spouse adjustments are inapplicable.

**Observed/Argued Result:** The rule blocks, raising `EvalBlocked(BLOCK_ABSENT, ["spouse_age65"])`.

**Mechanism:** 
The standard deduction rule in `it2/design.md` computes the additional standard deduction via:
```text
choose(all(EQ(R("spouse_age65"),1), spouse_allowed), P("p.additional-deduction",R("filing_status_code")), 0)
```
In the committed `evaluator.py`, the `all` operator evaluates its arguments sequentially from left to right:
```python
    if op == "all":
        return all(bool(evaluate(a, env, access)) for a in expr["args"])
```
Because the reference to `spouse_age65` is the first argument in `all`, the evaluator attempts to evaluate it before evaluating `spouse_allowed`. Since `spouse_age65` is absent, `evaluate` raises `EvalBlocked(BLOCK_ABSENT, ["spouse_age65"])`, which aborts evaluation. The short-circuiting behavior of `spouse_allowed` (which evaluates to `False` for Single/HoH/QSS) is never reached. Consequently, Single, HoH, and QSS filers will always block unless spouse demographic flags are explicitly asserted in the workspace.

---

## Finding CS-A11R: Evaluation Order Block on MFS with Ineligible Spouse (Decision-Blocking)

**Input State:** `filing_status_code` is `"3"` (MFS), `mfs_spouse_eligible` is `"0"` (spouse ineligible), and `spouse_age65` or `spouse_blind` is absent from `symbols`.

**Expected Result:** `r.standard-deduction` resolves to $15,000 without blocking.

**Observed/Argued Result:** The rule blocks on `spouse_age65` or `spouse_blind`.

**Mechanism:**
For MFS status, when `mfs_spouse_eligible` is `"0"`, `spouse_allowed` evaluates to `False`. However, due to the same evaluation-order issue identified in CS-A10R, the evaluator evaluates the absent `spouse_age65` first, raising `EvalBlocked` before checking `spouse_allowed`.

---

## Finding CS-A12R: Non-Spouse Exclusivity and Fallback Behavior (Verified)

**Input State:** `filing_status_code` is `"5"` (QSS), and `spouse_age65` is asserted as `"1"`.

**Expected Result:** The spouse adjustments are ignored; standard deduction resolves to $30,000.

**Observed/Argued Result:** If `spouse_age65` is asserted as `"1"`, the expression evaluates successfully. `spouse_allowed` evaluates to `False` for QSS (status code `"5"`). The `choose` guards for spouse adjustments evaluate to `False`, returning `0` and ignoring the asserted spouse value. 

This confirms that the spouse scoping logic is exclusive and fallback behavior is correct for asserted inputs. However, this verification is subject to the blockers CS-A10R and CS-A11R when inputs are absent.

---

## Finding CS-A13R: Zero/Negative Taxable Income and Threshold Math (Verified)

**Input State:** `taxable_income` crosses the $10,000 / $11,000 boundary.

**Expected/Observed Results:**
- At $10,000 taxable income, the tax resolves to $1,000.
- At $11,000 taxable income, the tax resolves to $1,120.
- At $0 or negative taxable income (derived via `max(0, AGI - standard_deduction)`), the tax resolves to $0.

**Mechanism:**
The marginal fold in `_bracket_fold` loops through the rows of `p.brackets`. For $10,000, row 1 (`lower: 0`, `upper: 10000`, `rate: 0.10`) contributes $1,000, and row 2 (`lower: 10000`) is skipped because `value <= lower` (10,000 <= 10,000) evaluates to `True`. Zero and negative inputs evaluate correctly to $0 as all rows are skipped.

---

## Finding CS-A14R: Itemization Override and Downstream Blocking (Verified)

**Input State:** `deduction_method_code` is `"1"` (asserted itemization override).

**Expected/Observed Result:** `r.standard-deduction` is inapplicable and publishes nothing. Downstream rules `r.taxable-income` and `r.regular-tax` block on the missing dependency `standard_deduction`.

**Mechanism:**
The applicability guard `when: EQ(R("deduction_method_code"), 0)` evaluates to `False`. The runner records the disposition as `inapplicable`. Because `standard_deduction` is not published, `r.taxable-income` (which requires `standard_deduction`) never becomes eligible and saturates as blocked (`DEPENDENCY_ABSENT`). This is the correct contract behavior, preventing the system from inventing a zero deduction before the itemized deduction package is adopted.

---

## Ruling on the Optional-Input Impossibility Claim

The clean-room rival's examination asserts that:
> *"...the committed contracts have no honest optional-input absence mechanism (overwrite/block dilemma reproduced by Rung-2 probe)."*

We **accept and confirm** this impossibility claim for all scalar inputs in `symbols`. 

### Refutation of Potential Counterexamples

1. **Staged Rules with Multiple Publishers:**
   One might attempt to define two rules publishing to the same symbol (e.g. `taxpayer_age65_effective`):
   - Rule A (`requires: ["taxpayer_age65"]`) publishes the asserted value.
   - Rule B (`requires: []`) publishes `0` as a default.
   
   *Refutation:* This approach violates the single-producer contract. `package_validation.py` will reject the package with `OUTPUT_OWNERSHIP_CONFLICT` unless the package declares conflict semantics. Furthermore, the committed runner lacks any runtime conflict-resolution logic; if both rules execute, they will both publish, resulting in duplicate publication acts and order-dependent overwriting in `self.symbols`. If we try to guard Rule B on the absence of Rule A's output, evaluating `ref("taxpayer_age65_effective")` in the guard raises `EvalBlocked`, deadlocking the run.

2. **Source-Collection Closure Aggregation:**
   One could model demographic flags as facts in source collections and query them using `collect` with `source_set` closure (which returns `[]` rather than blocking when empty).
   
   *Refutation:* While executable under the current evaluator, this is not a true optional default. It requires the workspace record to submit explicit closure mapping and transition acts for each individual demographic field. This shifts the complexity to the record layer, violates the ontology's distinction between scalar inputs and aggregated source facts, and still blocks on `SOURCE_SET_UNCLOSED` if the closure act is missing.

3. **Evaluation Order Short-Circuiting:**
   As demonstrated in CS-A10R, while we can re-order `all` arguments to short-circuit spouse adjustments when the spouse is ineligible, this trick fails for the taxpayer's own demographic flags (`taxpayer_age65`, `taxpayer_blind`). Because the taxpayer is always applicable, there is no eligibility flag that evaluates to `False` to short-circuit the expression before it hits the absent symbol reference.

Thus, under committed contracts, any reference to an absent scalar input unconditionally blocks, and any default-injecting rule unconditionally overwrites. The impossibility claim holds.

---

## Verdict on IT2

We **conditionally accept** the clean-room rival's iteration 2 design.

### Conditions for Acceptance:
1. **Re-order expression arguments for spouse adjustments:** The `all` expressions inside the `choose` guards for spouse adjustments must place `spouse_allowed` before the reference to the spouse demographic inputs:
   ```text
   choose(all(spouse_allowed, EQ(R("spouse_age65"),1)), P("p.additional-deduction",R("filing_status_code")), 0)
   choose(all(spouse_allowed, EQ(R("spouse_blind"),1)), P("p.additional-deduction",R("filing_status_code")), 0)
   ```
   This ensures that the evaluator short-circuits and skips the absent spouse references for Single, HoH, QSS, and ineligible MFS filers.
2. **Explicitly document demographic input requirements:** The design must state that taxpayer demographic inputs (`taxpayer_age65`, `taxpayer_blind`) and spouse inputs (when `spouse_allowed` is `True`) must be explicitly asserted (even if `0`) to avoid blocking, as no safe runner-side defaulting mechanism exists under current contracts.
