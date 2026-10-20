# Family-Handover Contract Proposal

Audience: Foreman, Reviewer, Builder.\
Status: Repaired after independent review; owner approved the four recommendations 2026-10-19; contract not yet implemented or accepted; no schema allocated, no ADR, no kernel change.

---

## 1. Actions in Plain Language

### The Concrete Form 1099-K Sale Story
Consider a workspace with existing v1 Form 1099-K history: either a recorded "no Form 1099-K received" closed-empty answer (`packages/tax/f1099k_statement_recording.py:687`, genesis at 716–726), or one recorded statement with its closure (`packages/tax/f1099k_statement_recording.py:349`, genesis at 443–453). The person now records another statement under a v2 package:
1. **The Handover Event:** The workspace transitions from v1 to v2 write authority for that family and scope.
2. **What the Person Sees (Not Seamless):** The earlier completeness answer ("these are all my statements") stops counting. The user is prompted again for completeness under v2.
   - *Closed-empty case:* The pinned zero gross proceeds drops from current standing.
   - *Closed-nonempty case:* Closure-backed subtotals and validation results drop from current standing.
3. **What Stays:** Earlier statement documents, reported box amounts, and answers remain intact in the fact lattice. Retained statement facts survive because their identity keys are `payer`, `statement`, and `tax-year` (`packages/content/tax/2025/f1099k.bundle.v3.json:13-30`), which do not bind `family-horizon`.
4. **What Drops:** Every fact individuated on the predecessor horizon entity drops via the superseded-entity root (`packages/kernel/currency.py:225`) and individuation edges (`packages/kernel/currency.py:156-168`). For Form 1099-K, this is strictly the closure fact `tax.us.2025.f1099k.source-closure` (`packages/content/tax/2025/f1099k.bundle.v3.json:81-90`).
5. **Why Fresh Closure Is Needed:** The successor makes a distinct completeness claim under v2 rules; completeness cannot be silently inherited or copied.
6. **Real Writers Covered:** Handover applies when recording a statement (`record_f1099k_statement_durably`, line 349) or a "no Form 1099-K" closure (`record_f1099k_no_statements_durably`, line 687). The answers writer (`record_f1099k_statement_answers_durably`, line 802) records answers on existing statements and opens no horizon. There is no statement removal writer today.
7. **The Untouched Workspace:** When a package adopting v2 arrives but no write has occurred, no handover is recorded. The v1 closure and its derived zero stay current, while the new package does not calculate.

### Who Records the Handover (Deliberate vs. Automatic)
- **Option A (Automatic in Same Save):** Statement recorder stages `act-family-handover.v1` in the same `append_batch` save as the first v2 write. Retires v1 immediately; requires re-attesting completeness, but avoids manual ceremony. Recommended.
- **Option B (Separate Deliberate Step):** User or runner executes an explicit upgrade step before any v2 statement can be written. Writers continue on v1 until deliberate upgrade. Left open for owner choice.

---

## 2. Supported Handover & Proposed Recorded Payload (Charter Item 1)

### Preconditions (Proposed Contract)
Handover is admitted if and only if all of the following hold atomically:
1. **Identity & Scope Match:** `predecessor.family.id == successor.family.id` and `predecessor.scope == successor.scope`.
2. **Version Distinction & Direction:** `predecessor.family.version != successor.family.version`. The kernel does not track package adoption (`packages/kernel/horizons.py:1`); application layer must ensure successor version is adopted. If an unadopted version is handed over, exact-version authority (the exact-version candidate, unaccepted) fails closed (`coverage: unclosed`).
3. **Single Active Chain:** Across all versions for that `(family.id, scope)`, exactly one chain key exists in `state.horizon_state.current_by_chain`.
4. **Predecessor Currency:** `predecessor.horizon_id == current_by_chain[(family.id, predecessor.version, scope)]`, and `state.fact_state.entities[predecessor.horizon_id].status == "current"`.
5. **Absent & Unretired Target:** `(family.id, successor.version, scope)` is absent from `current_by_chain` and not in `state.horizon_state.retired_chains`.
6. **Fresh Successor Horizon ID:** `successor.horizon_id` is unrecorded in `state.horizons` and `state.fact_state.entities`.

### Proposed Payload Fields (Coordinates Only)

| Field | Type | Meaning | Why Needed | Redundant / Derivable |
| :--- | :--- | :--- | :--- | :--- |
| `predecessor.family.id` | string | Family identifier being retired | Identifies family | Redundant with successor; checked for match |
| `predecessor.family.version` | string | Version being retired | Identifies retiring chain key | Required to identify predecessor chain |
| `predecessor.scope` | object | Scope of the family | Binds handover to exact scope | Redundant with successor; checked for match |
| `predecessor.horizon_id` | string | Horizon being superseded | Witnesses current state | Checked against `current_by_chain` & entity |
| `successor.family.id` | string | Successor family identifier | Binds successor chain | Redundant with predecessor; checked for match |
| `successor.family.version` | string | Successor version taking authority | Establishes new chain key | Required to establish successor chain |
| `successor.scope` | object | Scope of successor family | Binds successor scope | Redundant with predecessor; checked for match |
| `successor.horizon_id` | string | New horizon citizen identifier | Initial successor horizon | Required citizen identifier |

Predicate matching is omitted from the act payload: genesis carries coordinates only and the kernel does not hold predicates (`packages/kernel/horizons.py:30`).

### Contrast with Published Schemas
- Published `packages/schemas/kernel/act-horizon-genesis.v1.schema.json`: *"the genesis horizon's predecessor is null by construction, so no predecessor field exists here."*
- Published `packages/schemas/kernel/family-horizon.v1.schema.json`: *"predecessor is null only for the genesis horizon established before any member exists."*
- **Lineage Contract:** In `packages/kernel/horizons.py`, nothing outside `horizons.py` reads `predecessor`. A `family-horizon.v1` citizen whose family is the successor version and whose `predecessor` names the predecessor horizon is schema-valid. The contract explicitly norms that cross-version lineage (`successor.predecessor` naming predecessor horizon) is permitted for handover initial horizons, distinguishing them from null-predecessor genesis horizons.

### Deterministic Pure-Fold Effect
1. Validate preconditions; on failure, raise `HorizonModelError` (atomic rejection; zero state mutated).
2. **Entity State (`fact_state.entities`):** Update `entities[predecessor.horizon_id]` to `status="superseded"`, `successor_id=successor.horizon_id`. Record new entity `successor.horizon_id` with `status="current"`.
3. **Horizon Lifecycle (`horizon_state.horizons`):** Update `horizons[predecessor.horizon_id]` to `status="superseded"`, `successor_id=successor.horizon_id`. Record new horizon `successor.horizon_id` with `status="current"`.
4. **Active Chains (`horizon_state.current_by_chain`):** Remove key `(family.id, predecessor.version, scope)`. Insert `(family.id, successor.version, scope) -> successor.horizon_id`.
5. **Remembered Retirement (`horizon_state.retired_chains`):** Add `(family.id, predecessor.version, scope)` to retired set (keyed by `ChainKey` to prevent genesis reopening).
6. **Currency Cascade (No New Root):**
   - Predecessor entity becomes a superseded-entity root in `packages/kernel/facts.py:228` and feeds `packages/kernel/currency.py:225`.
   - Individuation edges built at `packages/kernel/currency.py:156-168` drop the closure fact `tax.us.2025.f1099k.source-closure` (`f1099k.bundle.v3.json:81-90`).
   - Derived findings drop along declared derivation pins at `packages/derivation/projection.py:66-75`.

### Refusal Outcomes (Atomic)
- Stale predecessor or non-current entity -> `HorizonModelError("predecessor horizon is not current")`.
- Target exists or ambiguous active authority -> `HorizonModelError("successor chain already exists or ambiguous active authority")`.
- Previously retired target -> `HorizonModelError("successor chain is retired")`.
- Reused successor horizon ID -> `HorizonModelError("horizon id already recorded")`.
- Differing scopes or identical versions -> `HorizonModelError("malformed handover payload")`.

---

## 3. Fences Across Write and Replay Paths (Charter Item 2)

### Current Persistence vs. Replay Behavior
- In `packages/kernel/act_log.py:198-265`, `append` and `append_batch` check schema, revision, and ADR-0077 new-write checks (`act_log.py:206-209, 262-263`), but **do not** execute prospective `apply_act`. `ActLog.read` parses committed lines (`act_log.py:133`) and validates schemas (`act_log.py:170-171`), but does not fold.
- In `packages/tax/f1099k_statement_recording.py:178,452`, recorders stage acts by calling `apply_act` locally before calling `append_batch`.
- **The Failure Mode:** If an act the kernel fold would reject is appended to disk, subsequent calls to `project` (`packages/kernel/findings.py:1408`) execute `apply_act`, encounter the model error, and crash, rendering workspace projection impossible.

### Proposed Pre-Persistence Validation
1. **Shared Pre-Persistence Kernel Fold:** `ActLog.append` and `append_batch` run prospective fold validation (`apply_act`) before writing bytes to disk. (See Open Choices for scope).
2. **New-Write Second-Genesis Rule:** Before persisting `act-horizon-genesis.v1`, `append` and `append_batch` refuse genesis if any active horizon chain already exists for that `(family.id, scope)` across all versions. Strictly **new-write-only**; does not run on historical replay (`project`).
3. **Replayed Pure Fold Guards:** Replay enforces:
   - Rejection of `member-transition` naming a version in `state.horizon_state.retired_chains`.
   - Rejection of closure `assertion` naming a superseded horizon entity (already enforced by existing finding validation: `packages/kernel/findings.py:644-647` resolves against current lattice, which omits facts keyed on superseded entities `packages/kernel/facts.py:272`).
   - Rejection of `act-horizon-genesis.v1` naming a version in `retired_chains`.
   - *Replay Safety Dependency:* Replayed post-retirement refusals are safe for legitimate historical logs **only because** the handover act is new and every path saving after it runs pre-persistence checks.

### Concrete Recorder Bypass & Resolution
In `packages/tax/f1099k_statement_recording.py:443-453` and `716-726`, `cur_h` checks only exact `family_ref`. When updated to v2, `cur_h` is `None`, so the recorder stages a v2 genesis beside active v1 history. Under Option A, the recorder must inspect `current_by_chain` for any active version in scope and stage `act-family-handover.v1` instead of genesis. Under Option B, it refuses to record until handover is present.

---

## 4. Case Coverage Matrix (Charter Item 3)

| Case | Recorded Acts in Order | Admission Result | What Is Current Afterwards | What the Person Sees |
| :--- | :--- | :--- | :--- | :--- |
| **1. Retained Member Correction** | v1 statements + v1 closure -> handover to v2 -> ordinary assertion on v1 statement fact | **Admitted.** Member correction carries no family version. | Member value updated; v1 closure remains displaced; v2 horizon untouched. | Updated statement value reflected; completeness still unclosed. |
| **2. Add After Handover** | Handover to v2 -> v2 `member-transition` (assert) | **Admitted.** Operates on active v2 chain. | v2 horizon advances to h1; new statement member current. | New statement added; completeness unclosed until explicit closure. |
| **3. Remove After Handover** | Handover to v2 -> v2 `member-transition` (remove) | **Admitted.** Operates on active v2 chain. | v2 horizon advances to h1; statement withdrawn; v2 closure displaced. | Statement removed; completeness unclosed. |
| **4. Fresh Closure & Rerun** | Handover to v2 -> fresh v2 closure assertion -> coordinator rerun | **Admitted.** Keyed on current v2 horizon. | v2 closure current; derived results current. | Completeness closed; tax subtotal authorized. |
| **5. Repeated Handover** | Handover v1->v2 -> repeated handover v1->v2 | **Refused.** v1 is retired; v2 chain exists. | State unchanged; v2 remains active. | Error: predecessor retired / target exists. |
| **6. Stale Predecessor Handover** | Handover v1->v2 -> handover v1->v3 naming superseded v1 horizon | **Refused.** Named predecessor horizon is superseded. | State unchanged; v2 remains active. | Error: predecessor horizon not current. |
| **7. Chained Handover (v2->v3)** | Handover v1->v2 -> Handover v2->v3 | **Admitted.** Exactly one active chain (v2) present. | v2 retired; v3 active at h0; v2 closure displaced. | v2 retired; prompted for fresh v3 completeness. |
| **8. Reverse Direction (Downgrade)** | Handover v1->v2 -> Handover v2->v1 | **Refused.** v1 is in `retired_chains`. | State unchanged; v2 remains active. | Error: target version was previously retired. |
| **9. Scope Mismatch** | Handover with `predecessor.scope != successor.scope` | **Refused.** Precondition 1 violated. | State unchanged. | Error: malformed handover scope. |
| **10. Old-Version Transition** | Handover v1->v2 -> v1 `member-transition` | **Refused.** v1 is in `retired_chains`. | State unchanged; v2 remains active. | Error: family version is retired. |
| **11. Third-Version Genesis** | Handover v1->v2 -> `act-horizon-genesis` for v3 | **Refused.** New-write rule blocks genesis beside active v2 chain. | State unchanged; v2 remains active. | Error: active chain already exists in scope. |
| **12. Historical Prefix Replay** | Workspace prefix before handover replayed | **Admitted.** Evaluates historical v1 log. | v1 horizon and closure current in prefix. | Historical prefix readable; v1 authority current within it (no output-identity promise). |
| **13. Unrelated Family / Scope** | Handover for 1099-K -> writes to W-2 or 1099-K 2026 | **Admitted.** Independent chain keys. | Targeted family/scope untouched. | Unrelated chain keys unaffected (calculation isolation is boundary question). |

*Preserved facts vs. membership:* Statement facts remain in the lattice across all cases, but only satisfy successor membership if admitted by the successor declaration.

---

## 5. Successor Membership Requirements for the Sale Family

`packages/content/tax/2025/family.f1099k.json:1-16` v1 is the only declaration on the branch; its closure claim authorizes only a single statement's box 1a and explicitly *"does not authorize a multi-payer sum."*\
A future successor declaration (v2) must fulfill the following contract requirements:
- **Canonical Member Predicate:** Must retain `tax.us.2025.f1099k.box1a-gross-amount`.
- **Identity Keys:** Must match member fact identity keys: `payer` (`tax.us.1099k-platform`), `statement` (`tax.us.1099k-statement`), and `tax-year` (`packages/content/tax/2025/f1099k.bundle.v3.json:13-30`).
- **Member Constraints:** Any new constraints (e.g. platform exclusivity) evaluate against retained statement facts. Retained statements violating constraints block validation; they are not silently rewritten.
- **Closure Claim:** Must explicitly state completeness and authorization scope for multiple statements across distinct payers before Policy 1 combined entry can publish.

---

## 6. Containment & Compatibility Boundaries

### Proposed Containment Rule for Both-Current Logs
In `packages/derivation/marshal.py:307-322`, the exact-version candidate narrowed horizon lookup to `c_ver == version`, which newly *admitted* both-current logs under the adopted version (Finding 1 path). Baseline marshal raised on any family with multiple chains (`if family_id in current_horizons:`).
- **Proposed Containment Rule:** `marshal_closure_authority` must **refuse closure authority** whenever more than one version chain is current for the same family ID and scope.
- **Consequence:** Refuses a second current version chain, as the pre-candidate marshal did, without restoring that raise on every second chain (this branch's raise is now scope-only, `marshal.py:316-319`); keeps exact-version selection only where exactly one chain is current. A both-current log remains readable, but its ambiguous authority is refused with `SourceAuthorityError("family has multiple active version chains")`, blocking calculation, while the saved zero stays current. Handover is refused (Precondition 3). There is **no supported path forward** inside handover. The synthetic helper `append_wash_sale_v2_empty_authority` (`tests/source_completeness/fixture_authority.py:59`) must stop appending concurrent active chains.

### Engine Compatibility Boundary
`ActLog._parse_committed_line` (`packages/kernel/act_log.py:164-173`) validates committed acts against `SchemaRegistry`. An older engine lacking the `act-family-handover` schema will raise `ActLogCorruption` on `read()`. An older engine **cannot read** a log containing a handover act. Historical-prefix replay is valid only for the slice recorded prior to handover.

---

## 7. Neighboring Family-Version Boundary

In `docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances.md:367`, eight wash-sale families (`tax.us.2025.f1099b.covered-w-*`) have recorded v1 chains while package v48 adopts v2:
- **Proposal Scope:** Specifies handover semantics; does not automate wash-sale migration.
- **Calculation Before Handover:** With exact-version lookup, v1 chains are unmarshalled, blocking closed-empty admission (`DEPENDENCY_ABSENT`).
- **Calculation After Handover:** Handover retires v1 and establishes v2, but authorizes nothing by itself; a fresh true closure and explicit rerun are still required before empty subtotals can publish.
- *Owner Boundary:* Whether synthetic fixtures cut clean v2 genesis from creation vs. record explicit handovers is an owner decision.

---

## 8. Contract Clauses & Comparison (Charter Item 5)

### Exact Contract Clauses Supplemented or Succeeded

| Clause / Document | Exact Quoted Text | Status | Justification |
| :--- | :--- | :--- | :--- |
| **ADR-0017 Decision 1** | *"Each versioned source-family declaration and scope has an ordinary recorded membership-horizon citizen with explicit succession."* | **Supplement** | Handover adds explicit cross-version succession (`family-horizon.v1` citizen with string `predecessor` pointing across versions). |
| **ADR-0017 Decision 3** | *"Every accepted membership-changing transition—add, remove, or change across the canonical member predicate—atomically records exactly one successor horizon for the same family/scope and current predecessor."* | **Unchanged** | Same-version member transitions remain unchanged. Handover is an explicit act kind for version transitions, not an overloaded member-transition. |
| **ADR-0017 Decision 5** | *"Horizon succession is an individuation root. It displaces closure facts and findings keyed on the predecessor horizon; existing derivation edges from the closure finding displace closure-backed results."* | **Unchanged** | Superseding the predecessor horizon entity already feeds `currency.py:225` and existing derivation pins. |
| **ADR-0017 Decision 6** | *"Currency is derived from immutable accepted acts. Incremental projection and full rebuild must agree. Supersession roots accumulate, so removal cannot resurrect an old result."* | **Unchanged (Relied On)** | Currency projection agrees across rebuilds; accumulated roots ensure displaced closures stay displaced. |
| **ADR-0017 Decision 7** | *"After a horizon change, new true closure attestation and explicit rerun are required before a successor closure-backed result may publish."* | **Unchanged (Relied On)** | Handover requires explicit fresh closure and rerun before successor results can publish. |
| **`family-horizon.v1` / `act-horizon-genesis.v1`** | *"predecessor is null only for the genesis horizon established before any member exists."* | **Unchanged** | Preserves null-predecessor genesis before members exist. Handover initial horizons carry string predecessor, honoring this distinction without mutating published schemas. |
| **ADR-0077 Decision Part 5** | *"The new-write admission boundary is `ActLog.append` in `packages/kernel/act_log.py`, at one new step."* (section "Where a new write is refused") | **Unchanged (Relied On)** | Installs the new-write second-genesis refusal into that same pre-persistence boundary on `ActLog.append` and `append_batch`. |

### Why a Dedicated Act Is Preferable
Synthesizing handover from an `entity-superseded` + genesis batch is deficient:
1. `apply_entity_superseded` (`packages/kernel/facts.py:128`) marks entities superseded but leaves `HorizonState.current_by_chain` active, permitting later transitions.
2. `append_batch` (`packages/kernel/act_log.py:218`) provides disk atomicity but does not run the prospective kernel fold.
3. Genesis schema description mandates `predecessor: null` before members exist, conflicting with populated upgrades.
4. An engine replaying acts cannot distinguish an intentional handover batch from independent operations. A dedicated act (`act-family-handover.v1`) executes atomic pure-fold validation, remembered retirement, and cross-version lineage monotonically.

---

## 9. Prospective Test Matrix

All tests below are **unexecuted** specifications for later implementation:

| Test Name | Category | Path Tested | Expected Result |
| :--- | :--- | :--- | :--- |
| `test_finding_1_helper_log_containment` | Failing-before / Passing-after | Full coordinator run on both-current log via helper (`tests/source_completeness/fixture_authority.py:59`) | Marshal refuses ambiguous authority with `SourceAuthorityError`; saved zero not displaced; run fails closed. |
| `test_finding_1_reached_through_real_recorder` | Failing-before / Passing-after | Real `f1099k_statement_recording.py` writing v2 genesis beside active v1 log | Pre-persistence check refuses genesis; if bypassed, marshal refuses ambiguous authority. |
| `test_recorder_bypass_second_genesis_refused` | Refusal | Real `f1099k_statement_recording.py:443` staging genesis for v2 beside active v1 history via `ActLog.append_batch` | Pre-persistence check refuses genesis: `HorizonModelError("active chain already exists in scope")`. |
| `test_atomic_handover_replaces_closure_and_zero` | Lifecycle | Recorder stages `act-family-handover.v1` -> fresh v2 statement -> fresh v2 closure via `ActLog.append_batch` | v1 retired; v1 closure & derived zero displaced; fresh v2 closure admitted; v2 subtotal authorized. |
| `test_closed_nonempty_handover_replaces_closure_and_subtotal` | Lifecycle | Handover on v1 with statements and closure | Statements preserved; closure & subtotal displaced; prompted for fresh v2 closure. |
| `test_stale_predecessor_handover_refusal` | Refusal | Handover naming already-superseded horizon via `ActLog.append` | Atomic refusal: `HorizonModelError("predecessor horizon is not current")`; log unmutated. |
| `test_chained_v2_to_v3_handover` | Lifecycle | Handover v1->v2 followed by handover v2->v3 | v2 retired; v3 active at h0; v2 closure displaced; prompted for fresh v3 completeness. |
| `test_reverse_handover_downgrade_refused` | Refusal | Handover v1->v2 followed by handover v2->v1 | Atomic refusal: `HorizonModelError("successor chain is retired")`. |
| `test_third_version_genesis_beside_active_chain_refused` | Refusal | Handover v1->v2 followed by `act-horizon-genesis.v1` for v3 | Pre-persistence check refuses genesis: `HorizonModelError("active chain already exists in scope")`. |
| `test_post_retirement_transition_refusal` | Refusal | Member-transition naming retired v1 after handover via `ActLog.append` | Pre-persistence & pure fold refuse: `HorizonModelError("family version is retired")`. |
| `test_same_member_value_correction_after_handover` | Lifecycle | Ordinary `assertion` updating retained v1 statement fact after handover via `ActLog.append` | Admitted; member value updated; v1 closure remains displaced; v2 horizon untouched. |
| `test_old_engine_schema_boundary` | Refusal | Engine lacking handover schema calling `ActLog.read` on log with handover act | `ActLogCorruption` raised by `_parse_committed_line` on schema validation. |
| `test_historical_prefix_replay` | Lifecycle | Slice of log prior to handover replayed through historical engine | Prefix projects clean v1 state without error. |
| `test_historical_two_genesis_log_stays_readable` | Lifecycle | Historical log with two genesis acts read and projected under new engine | `read` and `project` succeed; new-write-only second-genesis check does not fire on replay. |
| `test_untouched_workspace_standing` | Lifecycle | Package adopting v2 over v1 workspace without writes | v1 closure and derived zero stay current; new package refuses to calculate. |

---

## 10. Evidence Classification

| Evidence Category | File / Source | Status |
| :--- | :--- | :--- |
| **Existing Executed Evidence** | Independent review of the exact-version candidate (summarized in ADR 0079, Context) | Executed counterexample proving the Finding 1 defect. |
| **Existing Executed Evidence** | `tests/source_completeness/test_exact_family_version.py` | 7 passing component tests for the exact-version candidate exact-version selection. |
| **Existing Executed Evidence** | `docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances.md:367` | Executed inventory of 8 wash-sale families with v1 chains under v48 package. |
| **Paper Requirements** | `docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances-evidence/family-handover-contract-proposal.md` | Proposed contract requirements and 13-row case coverage matrix. |
| **Unexecuted Tests** | Section 9 Prospective Test Matrix (15 test cases) | Unexecuted test specifications for future implementation gate. |

---

## 11. Consequential Owner Decisions

| Choice | Value | Cost | Risk | Limitation |
| :--- | :--- | :--- | :--- | :--- |
| **1. Handover Trigger:**<br>A. Recorder stages handover in same save as first v2 write.<br>B. Separate deliberate upgrade step.<br>*(Recommended: A)* | A avoids a v2 genesis beside v1.<br>B keeps v1 writes until person upgrades. | A couples family writers to new act.<br>B blocks v2 writes until step exists. | A still asks completeness question again.<br>B leaves stale v1 writers if caller skips step. | Neither creates a 1099-K v2 declaration or removal operation. Answers do not open the horizon. |
| **2. Pre-Persistence Fold Scope:**<br>Full fold before every save, or targeted lifecycle kinds only.<br>*(Recommended: Targeted)* | Full fold refuses bad closure assertion before durable.<br>Targeted matches acts that move chains. | Full fold projects every save.<br>Targeted leaves direct closure assertion to fail at `project`. | Missed kind makes saved log unreadable at `project` while `read` parses. | Replay must not gain the second-genesis rule. Statement recorders already fold staged acts. |
| **3. Containment Failure Mode:**<br>Refuse closure authority when two versions current for one family id and scope.<br>*(Recommended: Refuse Authority)* | Stops Finding 1's adopted closure from being admitted. | Synthetic helper must stop appending a second current chain. | Calling this the old raise, or quiet unclosed family, changes who else calculates. | Saved zero stays current. There is no supported repair of that log inside handover. |
| **4. Wash-Sale Fixture Policy:**<br>Clean v2 genesis, or explicit handover in setup.<br>*(Recommended: Clean Genesis)* | Clean genesis avoids both-current baseline. | Handover in setup records retirement tests must understand. | Either choice is fixture policy, not wash-sale migration. | After handover, empty subtotal still needs its own fresh closure. |

---

*This completes the repaired contract proposal for owner disposition.*
