# P0 Evidence: Reproduce and Inventory of Per-Subject Rule Binding

## 1. Smallest Failing Case

The defect was reduced from `child_dispatch_probe.py` (flat-alone) to an exact minimal probe committed at:
`docs/phases/engineering-health/milestones/per-subject-binding-evidence/smallest_failing_case_probe.py`

### Scenario Structure
- Two children: `demo-child-1` and `demo-child-2`.
- One per-child rule: `probe.eic.rule.child-counts-flat`, declaring:
  - `subject`: `probe.eic.child.relationship` (entity kind `probe.child`)
  - `requires`: `["probe.eic.child.residency"]`
- Assertions in state:
  - `demo-child-1`: has `relationship = "yes"` and `residency = "yes"` (finding ID: `demo.probe.residency.demo-child-1`).
  - `demo-child-2`: has `relationship = "yes"`, but residency is **unanswered**.

### Exact Failing Code Path Across Engine Modules
1. **`packages/derivation/live.py` (lines 271, 318–360, 400–484)**:
   - `collect_names` only gathers `family["member_predicate"]["fact_type"]` (line 271) and domain-specific companion lists.
   - Per-subject required inputs (`probe.eic.child.residency`) are not declared as collect source names or companion presences.
   - While Form 1099-K has a hardcoded whitelist (`F1099K_ALLOWED_PER_STATEMENT_INPUTS`, lines 400–484) that adds its inputs to `emission_only`, no general discovery exists for other per-subject inputs.
2. **`packages/derivation/marshal.py` (lines 466–490, 529–560)**:
   - In `marshal_run()`, finding rows whose fact type is not in `emission_names` (`collect_names | emission_only`) do not become `SourceFact` rows in `ctx.sources`.
   - Instead, `probe.eic.child.residency` falls into `fallback_matches` (lines 529–560). Because only one finding exists across the entire return (`demo.probe.residency.demo-child-1`), line 553 binds it as a single run-wide scalar `InputFinding(symbol="probe.eic.child.residency", value="yes", finding_id="demo.probe.residency.demo-child-1")` into `ctx.inputs`.
3. **`packages/derivation/runner.py` (lines 440–445)**:
   - `_Run.setup()` initializes `run.symbols` and `run.symbol_pin` from `ctx.inputs`.
   - `run.symbols["probe.eic.child.residency"] = "yes"` and `run.symbol_pin["probe.eic.child.residency"] = ("demo.probe.residency.demo-child-1", "v1", "input", "assertion")`.
4. **`packages/derivation/subject_dispatch.py` (lines 612–615, 688–690, 715–719)**:
   - `other_names` (line 612) is populated only from `sources`. Since `probe.eic.child.residency` was never marshaled into `sources`, `scoped` contains no entry for it.
   - In the required symbol loop (line 691), `req in scoped` (line 694) is `False`.
   - Execution falls through to line 715:
     ```python
     if req in run.symbol_pin and req in run.symbols:
         local_symbols[req] = run.symbols[req]
         symbol_pin[req] = run.symbol_pin[req]
         fact_types[req] = _fact_type_of(run, req)
         continue
     ```
   - For `demo-child-2`, `local_symbols["probe.eic.child.residency"]` receives `"yes"` from `run.symbols`, and `symbol_pin` records `demo.probe.residency.demo-child-1`.

### Exact Pins Recorded in the Wrong Disposition
Running `smallest_failing_case_probe.py` produces:
```
Symbol: probe.eic.child.counts-flat|probe.eic.child.relationship|child=demo-child-2,tax-year=2025
Disposition: published (value: 1)
Pins:
  - adoption id=probe.package.eic-children
  - computation id=probe.eic.rule.child-counts-flat
  - input id=demo.probe.rel.demo-child-2
  - input id=demo.probe.residency.demo-child-1  <-- LEAKED CROSS-SUBJECT PIN
```

---

## 2. Inventory of Shipped Per-Subject Rules on Main

We scanned all 52 published manifests (`published-packages.v1.json` through `published-packages.v52.json`) containing 58 distinct packages.

Across all packages on `main`, there are exactly **67 distinct published rules** declaring a `subject` member.

### Category Breakdown

| Category | Count | Rules | Exposure Status | Reason |
| :--- | :--- | :--- | :--- | :--- |
| **Empty Requires** | 33 | 16 EIC child test rules (v1 & v2: `age-met`, `relationship-met`, `residency-met`, `ssn-met`, `joint-return-met`, `other-claimant-clear`), 16 child helper rules, and `tax.us.2025.rule.f1098-residence-interest-unresolved@v1` | **Not Exposed** | `requires: []` is empty; rule reads only the subject row and binds no other input symbols. |
| **Joined SLI Rules** | 5 | `tax.us.2025.rule.sli-answer-status-qualified-student-loan@v1`, `tax.us.2025.rule.sli-answer-status-taxpayer-primary-obligation@v1`, `tax.us.2025.rule.sli-answer-status-sole-obligation@v1`, `tax.us.2025.rule.sli-answer-status-no-qualified-employer-plan-interest@v1`, `tax.us.2025.rule.sli-answer-status-no-related-person-interest@v1` | **Not Exposed** | Declare `joined: <fact_type>`. Under ADR-0076, `joined` is emitted in `emission_only` and filtered via `_presence_matched` / `_scope`. |
| **Chained SLI Rules** | 19 | `sli-statement-loan-support@v1`, `sli-statement-support-reason@v1`, `sli-statement-line21-standing@v1`, `sli-statement-combined-standing@v1`, `sli-inclusion-support@v1`, `sli-inclusion-support-reason@v1`, `sli-flag-inclusion-*`, `sli-financing-schooling-link@v1` | **Not Exposed** | Required inputs are derived intermediate publications keyed by statement or pairing. Scoped per subject via `_scope`. |
| **Form 1099-K Rules** | 7 | `f1099k-adjusted-basis@v1`, `f1099k-amount-realized@v1`, `f1099k-expected-box1a-gross-amount@v1`, `f1099k-net-proceeds@v1`, `f1099k-selling-expenses@v1` & `@v2`, `f1099k-statement-loss-reason@v1` | **Not Exposed** | Protected by hardcoded `F1099K_ALLOWED_PER_STATEMENT_INPUTS` in `live.py` (lines 400–484), which places them in `emission_only` -> `sources`. Missing inputs take `optional_default` in `subject_dispatch.py` (lines 703–706) and never fall through to `run.symbols`. |
| **EIC Child Count Rule** | 1 | `tax.us.2025.rule.eic-child.counts@v1` | **Not Exposed (in shipped form)** | Shipped rule requires 6 intermediate publications (`*-met`) published per child, which are filtered by `_scope`. |
| **Form 1098 Residence Interest** | 2 | `tax.us.2025.rule.f1098-residence-interest-reason@v1` (in `package.core-calculations.v44`), `tax.us.2025.rule.f1098-residence-interest-reason@v2` (in `package.core-calculations.v45`..`v54`) | **EXPOSED** | Flat rule requiring 14 inputs (11 per-statement circumstance inputs). Inputs are not in `emission_only` or `collect_names`, have no input bindings in the package, and enter `run.symbols` via `marshal.py` fallback matches. In `subject_dispatch.py`, missing answers fall through to `run.symbols` and bind another statement's answers. |

---

## 3. Real Effect on Latest Adopting Package (`package.core-calculations.v54.json`)

We implemented a full live coordinator probe at:
`docs/phases/engineering-health/milestones/per-subject-binding-evidence/f1098_two_statement_probe.py`

### Scenario
- Environment: Latest production surface (`published-packages.v52.json`, `package.core-calculations.v54.json`, release `demo.release.sli-worksheet-integration.2025.v52.json`).
- Two Form 1098 mortgage statements:
  - Statement A (`demo.f1098.lender.a`, `demo.f1098.stmt.a`): interest $20,000, principal $200,000, box 3 "2020-06-01", box 9 1.0. All 9 circumstance answers asserted:
    - `filing-unit-owns-home = yes`
    - `shared-main-home = yes`
    - `home-is-collateral = yes`
    - `owes-the-loan = yes`
    - `paid-the-interest = yes`
    - `no-one-else-owes-it = yes`
    - `what-the-money-paid-for = bought-the-home`
    - `this-is-the-original-loan = yes`
    - `mortgage-credit-certificate-received = not-received`
  - Statement B (`demo.f1098.lender.b`, `demo.f1098.stmt.b`): interest $10,000, principal $100,000, box 3 "2020-06-01", box 9 1.0. **Zero circumstance answers asserted.**

### Actual Shipped Execution Result
Executing `f1098_two_statement_probe.py` through `live_coordinate_run` produces:
1. Two published dispositions for `tax.us.2025.rule.f1098-residence-interest-reason`:
   - Statement A: published `qualified`
   - Statement B: **published `qualified`** (WRONG SHIPPED RESULT)
2. Statement B's disposition records 13 input pins, including all 9 circumstance finding IDs from Statement A:
   ```
   Statement A answer pins on Statement B: [
       'demo.f1098.ans.a.0',
       'demo.f1098.ans.a.1',
       'demo.f1098.ans.a.2',
       'demo.f1098.ans.a.3',
       'demo.f1098.ans.a.4',
       'demo.f1098.ans.a.5',
       'demo.f1098.ans.a.6',
       'demo.f1098.ans.a.7',
       'demo.f1098.ans.a.8'
   ]
   ```
### Real-World Consequence
If a taxpayer has two mortgage statements (e.g., primary home and second home, or a refinanced mortgage) and answers circumstance questions only for the first statement, the engine silently marks the second statement as fully qualified instead of blocking as `unresolved` or `DEPENDENCY_ABSENT`.

---

## 4. Fix Options

### Option A: Engine Coordinator Discovery & Subject Dispatch Isolation (Recommended)
**Changes:**
1. In `packages/derivation/live.py` (`_resolve_run_material`):
   - Replace the hardcoded `F1099K_ALLOWED_PER_STATEMENT_INPUTS` loop with a general structural discovery:
     For any rule declaring a `subject`, inspect every symbol in `rule.get("requires", [])`. If that symbol resolves to a fact type whose identity keys share the subject entity/keys, automatically add it to `emission_only`.
2. In `packages/derivation/subject_dispatch.py`:
   - Include any required per-subject fact type in `other_names` so that `scoped` explicitly maps it per subject.
   - When evaluating required symbols for a subject, if `req in scoped`:
     If `scoped[req]` is empty and no default exists, record `DEPENDENCY_ABSENT` and block the subject.
     Never fall through to `run.symbols[req]`.
   - Genuine return-level inputs (e.g. `filing_status`, `tax.us.2025.agi`, return parameters) have identity keys that do not contain subject entity keys; they are not in `scoped` and continue falling through to `run.symbols` as intended.

**Testing with uncommitted patch:**
- `f1098_two_statement_probe.py`: Statement B blocks with `DEPENDENCY_ABSENT`, 0 leaked pins; Statement A publishes normally.
- `smallest_failing_case_probe.py`: Child 2 blocks; Child 1 publishes.
- Fast-lane test suite (`pytest -m "not live"`): **1528 passed, 8 skipped, 0 failed**.
- Form 1098 test suite (`pytest tests/test_f1098_*.py`): **30 passed in 65s, 0 failed**.
- Schema / Rule Language Changes: **None**. No schema changes, no DSL changes, no package migration.

### Option B: Rule Shape Migration (Chained Test Architecture)
**Changes:**
1. Migrate Form 1098 from the flat rule shape to the chained test pattern (identical to SLI and EIC child):
   - Create intermediate test rules for each circumstance question, declaring `joined: <fact_type>` and publishing scoped test results (e.g. `tax.us.2025.f1098.home-collateral-met|payer=...,statement=...`).
   - The reason rule requires only the derived intermediate publications, which are scoped per subject via `_scope`.
2. In `subject_dispatch.py`, disallow reading raw unjoined fact types from `run.symbols`.

**Trade-offs:**
- Requires authoring 10+ new rule citizens, publishing new schema/citizen artifacts, revving `package.core-calculations` to `v55`, and updating migration/adoption tests.
- High churn in content packages; does not protect against future flat per-subject rules if an author forgets to chain.

---

## 5. Recommendation

**Adopt Fix Option A (Engine Coordinator Discovery & Subject Dispatch Isolation).**

### Justification:
1. **Root cause fix**: Fixes the transport and dispatch layer where the leakage actually occurs. It guarantees that *any* subject-scoped rule automatically receives only its own subject's facts, regardless of whether the rule is flat or chained.
2. **Zero content churn**: Does not require revving published packages, schemas, or citizens.
3. **Verified zero regressions**: Verified locally against the full fast-lane test suite (1528 tests) and Form 1098 integration suite (30 tests) with 100% pass rate.
4. **Preserves return-level inputs**: Return-level facts (e.g., `filing_status`, `tax.us.2025.agi`, parameters) are distinguished by identity keys and continue to pass through `run.symbols` to per-subject rules.

### Estimated Implementation Cost:
- **Production files modified (2 files, ~40 lines)**:
  - `packages/derivation/live.py`: ~20 lines in `_resolve_run_material` to generalize per-subject input discovery into `emission_only`.
  - `packages/derivation/subject_dispatch.py`: ~20 lines in `other_names` and `required` loop to enforce strict subject isolation.
- **Tests added (2 files)**:
  - `tests/test_f1098_two_statement_isolation.py` (formal regression test based on `f1098_two_statement_probe.py`).
  - Unit test in `tests/derivation/test_subject_dispatch.py` for per-subject missing answer isolation.
