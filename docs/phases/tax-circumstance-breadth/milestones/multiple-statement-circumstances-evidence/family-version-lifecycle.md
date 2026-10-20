# Family-Version Lifecycle Outline & Refinement

Audience: Foreman, Reviewer, Builder.
Milestone: `multiple-statement-circumstances`
Status: Checkpoint 3 Refinement (Proposed contract requirements for paper analysis, bounded carrier proposal, repaired case table, and admission/replay refinement; no production code edits or probes).

---

## 1. Purpose and Checkpoint Scope

The exact-version candidate implemented exact-version selection in `marshal_closure_authority` for distinct family versions, but independent review Finding 1 demonstrated that when both v1 and v2 chains have genesis and closure in a workspace, an ordinary `member-transition` on the unselected v1 chain leaves the selected v2 closure admitted and its derived zero current.

Independent review feedback and the Checkpoint 3 Foreman checks directed a bounded paper refinement of explicit handover. Coordinated active chains (Approach B) and admission-refusal alone (Approach C) are ruled out as repairs for Finding 1.

This document fulfills Checkpoint 3 of the family-version lifecycle investigation:
- Locates "before any member exists" in the published schema descriptions rather than ADR-0017 Decision 1.
- Specifies exact proposed preconditions for a dedicated handover act: across all versions there is only one active family-id/scope chain, source and target have matching family ID and scope with different versions, target is absent and not previously retired, horizon ID is fresh, and predecessor entity is current.
- Defines remembered retirement to prevent reopening via a subsequent genesis.
- Specifies a shared new-write admission validator for direct `append` and `append_batch` to refuse second-genesis bypasses, while keeping historical two-genesis logs replayable on read.
- Treats already-both-current logs as readable historical containment where ambiguous authority is refused, without claiming saved-zero displacement or supported recovery.
- Corrects Case 8 in the decisive case table so that no approach promises independent calculation from key shape alone.
- Delivers a grounded provisional recommendation with value, cost, risk, and explicit containment limits. All mechanisms are proposed contract requirements, not implemented APIs or independent acceptance.

---

## 2. Action 1: Plain-Language Requirements & Behavioral Promises

### Completeness Is Not Emptiness
A family closure asserts completeness—that all member facts for that family and scope have been accounted for. A closed family set may be:
- **Closed-empty:** Zero member facts exist, and the closure asserts that no statements or transactions occurred.
- **Closed-nonempty:** One or more member facts exist (e.g. Form 1099-K statements or wash-sale transactions), and the closure asserts that the recorded set is complete.

The defect in Finding 1 is not that member facts exist; it is that a *later membership change* was accepted on one version's chain without being reflected in the other version's horizon, yet the unadvanced horizon's closure still claimed completeness for that predicate, leaving an earlier pinned zero current.

### Distinguishing Promises
1. **Replaying the Historical Prefix (Immutable Readability):**
   Evaluating the historical prefix of a workspace (prior to any version upgrade or subsequent transitions) against the historical package that created it (e.g. core v20 adopting v1) allows historical tools to read and project the prefix. It preserves historical auditability without promising a blanket new byte-identity contract across changing environments.
2. **Evaluating a Changed Full Log Under an Old Package:**
   Running an old package against an entire act log that has undergone subsequent upgrades, handovers, or transitions is a different question. Preserving history guarantees the prefix is readable; it does not promise that obsolete write authority or earlier closures survive subsequent lifecycle events in a mutated log.
3. **Package Adoption Is Not Handover:**
   A calculation package declaring an adoption of v2 families (e.g. `package.core-calculations.v48.json`) is static catalog metadata. It does not alter recorded workspace acts, does not retire an existing v1 horizon chain, and does not establish fresh v2 authority. Handover, if adopted, must be an explicit recorded event.

### Candidate Architectural Stance: Single Active Write Authority (Provisional Recommendation)
Restricting active write authority to one version per family and scope at a time resolves split-brain writing. Coordinated concurrent writing across multiple active versions is rejected due to compound transition carrier costs and lack of multi-version registry mappings.

---

## 3. Action 2: Current Source Trace of the Defect (Finding 1)

Tracing from family/version/scope down to the derived zero reveals why Finding 1 survives today's currency roots:

```
[Family + Version + Scope]
       │
       ▼
packages/kernel/horizons.py: ChainKey = (family_id, version, scope_tuple)
       │
       ▼
packages/kernel/horizons.py: HorizonState.current_by_chain[ChainKey]
       │
       ├── (id, "v1", scope) ──► current: demo.wst-p.v1.h0 (transitions to h1)
       └── (id, "v2", scope) ──► current: demo.wst-p.v2.h0 (UNTOUCHED)
```

1. **Chain Isolation in Horizons:**
   `packages/kernel/horizons.py` keys each chain by `ChainKey = (family["id"], family["version"], tuple(sorted(scope.items())))`. Chains for `("tax.us.2025.f1099b.covered-w-st-proceeds", "v1", ...)` and `("tax.us.2025.f1099b.covered-w-st-proceeds", "v2", ...)` are independent entries in `HorizonState.current_by_chain`.
2. **Transition Scope & Entity Supersession:**
   `packages/kernel/findings.py#apply_member_transition` invokes `horizons.apply_transition` strictly on the `payload["family"]` named in the act. When an act transitions `v1`, only `demo.wst-p.v1.h0` is marked superseded in `HorizonState.horizons`. In `packages/kernel/facts.py`, only entity `demo.wst-p.v1.h0` transitions to `status="superseded"`.
3. **Individuation Roots and Two-Edge Currency Closure:**
   `packages/kernel/currency.py#compute_currency` gathers displacement roots from `superseded_entity_ids(state.fact_state)`.
   - `demo.wst-p.v1.h0` is superseded, which displaces `demo.closure.proceeds.v1` via the individuation edge (`Fact.individuated_by`).
   - `demo.wst-p.v2.h0` is **not** superseded. Consequently, `demo.closure.proceeds.v2` (individuated by `demo.wst-p.v2.h0`) remains in `current_finding_ids`.
4. **Derivation Currency Cascade:**
   The derived zero publication is **not** pinned directly to the horizon; it is pinned with role `input` to the closure finding (`packages/derivation/runner.py`). In `packages/derivation/projection.py#compute_derivation_currency`, displacement cascades along declared derivation pins. Because `demo.closure.proceeds.v2` is not displaced, the derived zero publication remains in `current_derived_ids`.
5. **Admission and Coverage:**
   In `packages/derivation/marshal.py#marshal_closure_authority`, the adopted v2 mapping looks up current horizons for `(family_id, "v2")`. It finds `demo.wst-p.v2.h0`, sees its current literal-true closure finding, admits the family, and `coverage_report` marks it `closed`—even though a live member fact matching the predicate (`tax.us.2025.f1099b.covered-w-st-txn.proceeds`) was added via the v1 transition.
6. **Recorder Version Selection:**
   Recorders (such as `packages/tax/f1099k_statement_recording.py` lines 418–420) statically specify `FAMILY_VERSION = "v1"`. Repository catalog changes do not alter recorded workspace state.

---

## 4. Action 3: Comparison of Architectural Approaches

### Approach A: Explicit Handover
- **Core Concept:** An explicit recorded handover event retires older write authority for a family and scope when a successor version is adopted, transitioning active writing to the new version.
- **Consequences:**
  - *Old Authority & Pinned Results:* The older version's write authority is retired. The retired horizon entity becomes a superseded-entity root; the closure finding drops through individuation; and the derived zero drops through its `input` pin.
  - *Retained Members:* Existing member facts and findings in the lattice remain in history, but are members of the successor **only if** the successor declaration's member predicate fact type, identity keys, and member constraints admit them. Mismatch is a block or refusal, not a silent conversion.
  - *Fresh Authority Required:* The successor version requires fresh authority at its own horizon (new initial horizon citizen, member validation if applicable, and an explicit closure finding if the set is complete). It does **not** inherit or auto-copy closure from v1.
  - *Stale Writes Prevented:* Subsequent writes attempting to target the retired version are rejected by admission via remembered retirement.
- **Mechanism Boundary:** Merely superseding a horizon entity via `apply_entity_superseded` displaces horizon-keyed facts, but `current_by_chain` is separate; entity supersession does not retire the chain key or prevent later writes. Retiring the chain key requires an explicit mechanism in the pure fold (see Section 6).

### Approach B: Coordinated Active Versions
- **Core Concept:** Both versions remain concurrently active and writable. Any membership transition on either version coordinates an atomic advancement of all chains sharing the member predicate.
- **Consequences:**
  - A member-transition naming `v1` atomically advances both `v1` and `v2` horizon chains, superseding both horizon entities and displacing all version closures simultaneously.
- **Conditional Carrier / Mechanism Costs:**
  - High complexity. Requires amending ADR-0017 (which mandates exactly one predecessor and one successor per member transition) to support multi-horizon advancement.
  - Requires a multi-horizon carrier schema or compound transition act.
  - Requires `SchemaRegistry` to maintain a replay-stable mapping from member predicate to all declared family versions, which the current flat `set[str]` in `registry.family_member_predicates` lacks.

### Approach C: Bounded Refusal Containment
- **Core Concept:** Kernel or marshal admission strictly refuses operations when coexisting or desynchronized version states are detected.
- **Limitations as a Repair for Finding 1:**
  - Refusal at admission stops a later marshal from treating the v2 closure as authority only if the runner never publishes.
  - The closure finding stays in `current_finding_ids` and the derived zero pinned to it stays in `current_derived_ids` until an actual displacement root fires. Admission refusal alone does not displace a saved zero.
  - Furthermore, refusal-only does not provide a forward migration path: it blocks ordinary subsequent updates if versions coexisted. Refusal is containment, not delivery.

---

## 5. Decisive Case Table (Repaired)

| Case | Scenario Description | Approach A (Explicit Handover) | Approach B (Coordinated Versions) | Approach C (Bounded Refusal) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Fresh v2 Setup** | Clean workspace: v2 genesis establishes initial empty horizon; members arrive later on that same chain; v2 closure. | **Admitted.** Single active v2 chain. Normal closed-empty or closed-nonempty operation. | **Admitted.** Single chain operates normally. | **Admitted.** No conflicting versions exist. |
| **2. Populated v1 History + v2 Adoption** | Workspace has v1 genesis, statements, and closure; package adopts v2. No v2 acts yet. | **Handover required.** v1 prefix replayable; v2 requires recorded handover establishing successor horizon; fresh closure required for completeness. | **Dual active.** Both chains track state; high synchronization overhead. | **Refused** if v2 authority is required by package but absent from workspace. |
| **3. Member Add on Unselected v1 (Finding 1)** | Workspace has both v1 and v2 chains current with closures (unhandovered); later member-transition names v1. | **Ambiguous Authority Refused.** Log remains readable; marshal refuses ambiguous authority (two current versions for same family and scope). Saved zero stays current (containment, not recovery). | **Both chains advance.** Both v1 and v2 horizons advance; v2 closure displaced; zero displaced. | **Admission Refused.** Marshal detects uncoordinated transition; refuses v2 closure admission. (Does not displace saved zero). |
| **4. Member Add on Selected v2** | Handover complete; member-transition names active v2. | **v2 advances.** v2 horizon advances; v2 closure displaced via individuation; derived zero displaced via input pin. | **Both advance.** Both v1 and v2 horizons advance; closures displaced. | **v2 advances.** v2 horizon advances; closure displaced. |
| **5. Value Correction on Unchanged Member** | Correction to an existing member fact via ordinary assertion (no horizon advance). | **Preserved.** Member value updates; horizon untouched; existing closure remains current. Cannot revive an already displaced closure. | **Preserved.** Same-member correction does not alter horizons. | **Preserved.** Same-member correction does not alter horizons. |
| **6. Historical Prefix Replay (v20 Package)** | Historical workspace prefix evaluated against core v20 (v1 adopted). | **Prefix Readable.** v1 chain is read and projected under historical package; past records remain auditable. | **Prefix Readable.** v1 chain evaluated as adopted. | **Prefix Readable.** Historical single-version path sound. |
| **7. Attempted Write on Retired Version** | Write attempted on v1 after handover to v2. | **Refused atomically.** Admission rejects member-transitions, closure assertions, and genesis against retired chain. Ordinary current-member value correction allowed (carries no family version). | **Accepted and synchronized** to v2 (high coordination cost). | **Refused or desync** (unless explicit guard rejects write). |
| **8. Shared vs. Distinct Scopes & Predicates** | Multiple statements in same scope vs. distinct tax years/predicates. | **Boundary Question.** Multiple statements sharing scope share the horizon chain; different scopes/predicates have separate chain keys, but calculation/consumer isolation is not proven by chain key shape alone. | **Boundary Question.** Scope keys separate horizon rows, but calculation/consumer isolation is not proven by chain key shape alone. | **Boundary Question.** Scope keys separate horizon rows, but calculation/consumer isolation is not proven by chain key shape alone. |
| **9. Member Removal After Handover** | Statement removed via transition on active successor version. | **v2 advances.** Active v2 horizon advances; v2 closure displaced via individuation; derived zero displaced via input pin. | **Both advance.** Both horizons advance; closures displaced. | **v2 advances.** v2 horizon advances; closure displaced. |

---

## 6. Checkpoint 3 Addendum: Carrier, Admission, and Replay Refinement

### Contract Location: The "Before Any Member Exists" Sentence
The sentence:
> `"predecessor is null only for the genesis horizon established before any member exists."`

lives in the published description of `packages/schemas/kernel/family-horizon.v1.schema.json` (and the `packages/schemas/kernel/act-horizon-genesis.v1.schema.json` payload description), **not** in ADR-0017 Decision 1.
- ADR-0017 Decision 1 requires that each versioned declaration and scope has a recorded horizon with explicit succession.
- The schema’s `predecessor` property allows `string | null`.
- `packages/kernel/horizons.py#apply_genesis` rejects repeated chain keys, but does not verify whether member facts exist in the lattice.
- However, because published schema files are immutable under ADR-0003 and Article 9, their published text cannot be edited in place. Neither Option 1 nor Option 2 is "automatically compatible with ADR-0017": ADR-0017 normed within-version membership succession, not cross-version handover. A dedicated act still requires its own explicit lifecycle contract sentences.

---

### Concrete Carrier Comparison

#### Carrier Option 1: Logical Atomic Handover Using Existing Recorded Acts
- **Concept:** Combine an `entity-superseded` act (superseding the old horizon entity) and an `act-horizon-genesis.v1` act (recording a `family-horizon.v1` citizen for the successor) in a single save.
- **Defects & Limitations:**
  - *Persistence vs. Kernel Admission:* `ActLog.append_batch` provides durable all-or-none write atomicity, but does not execute the prospective kernel fold (`apply_act`). When acts replay through kernel projection, pure functions evaluate them sequentially.
  - *Failure to Retire Chain:* `apply_entity_superseded` marks `state.entities[entity_id].status = "superseded"`, but does not touch `HorizonState.current_by_chain`. `apply_member_transition` does not check entity status before overwriting it; thus, `entity-superseded` alone fails to stop future transitions on the old version.
  - *Contract Mismatch:* Reusing `act-horizon-genesis.v1` (mandating `predecessor: null`) for a populated successor with existing members in the lattice contradicts the published description of the genesis horizon.

#### Carrier Option 2: Dedicated Handover Act (Bounded Proposal)
- **Concept:** A dedicated kernel act schema (e.g. `act-family-handover.v1`) recording an explicit transition from a predecessor family/version/scope to a successor family/version/scope.
- **Exact Proposed Preconditions (Contract Requirements):**
  - **Single Active Predecessor Across All Versions:** Across all versions for that family ID and scope, there must be **exactly one active horizon chain** in `state.horizon_state.current_by_chain`.
  - **Identity Match & Version Distinction:** Predecessor and successor carry the exact same family ID (`predecessor.family.id == successor.family.id`) and equal scope (`predecessor.scope == successor.scope`), but differing versions (`predecessor.family.version != successor.family.version`).
  - **Predecessor Currency:** The named predecessor horizon matches the current horizon of that single active chain, AND the predecessor horizon entity in `state.fact_state.entities` is currently in `status="current"`.
  - **Absent & Non-Retired Target:** The target version must be **absent** from `current_by_chain` and **not previously retired** in that scope.
  - **Fresh Horizon ID:** The target `horizon_id` must be new (unrecorded in `state.horizons` or `state.fact_state.entities`).
  - **Refusal on Invalid State:** If a target chain already exists, the predecessor entity is already superseded, the target was previously retired, or multiple active versions exist, handover is **refused**. It does not claim to adopt or recover an existing target chain.
- **Atomic Pure Fold Effect:**
  A single pure transition function atomically:
  1. Validates all preconditions above.
  2. Marks the predecessor horizon entity in `state.fact_state.entities` as `status="superseded"`, with the successor horizon as replacement entity. (This triggers existing individuation displacement of old closure findings and input-pin displacement of derived zeros).
  3. Records a **remembered retirement** for `(predecessor_family_id, predecessor_version, scope)` in `HorizonState`.
  4. Establishes the successor horizon in `state.horizon_state.current_by_chain` with explicit lineage back to the predecessor horizon.

---

### Admission, Replay, and Invariant Enforcement

#### Prevention of Second-Genesis Bypasses (New-Write Validation vs. Replay Pure Fold)
- **The Bypass Risk:** After a handover to v2, a subsequent writer could attempt an ordinary `act-horizon-genesis.v1` for another version (e.g. v3 or a concurrent v2) beside an existing active chain for that family ID and scope, recreating the split-brain / ambiguous-authority defect.
- **Architectural Separation:**
  1. **Shared New-Write Validation (Pre-Persistence Gate):**
     - Before appending an `act-horizon-genesis.v1` to disk, both append paths (`ActLog.append` and `ActLog.append_batch`) run a shared new-write validation rule.
     - **Rule:** Refuse genesis if any active horizon chain already exists for that family ID and scope across all versions.
     - **Replay Exemption:** This rule is strictly a **new-write-only admission rule**. It is **not** run during historical log replay (`read` / `project`), so historical workspaces with old two-genesis logs remain readable and auditable.
  2. **Pure Replay Fold & Post-Retirement Guards:**
     - The pure kernel fold executes monotonically during both new writes and historical replay.
     - It maintains the **remembered retirement set** for `(family_id, version, scope)`.
     - Replay and new writes alike reject `member-transition`, closure `assertion`, or `genesis` naming any explicitly retired version in that scope.

#### Monotonic Remembered Retirement
- A removed dictionary key in `current_by_chain` alone cannot prevent `apply_genesis` from reopening that version later, because `apply_genesis` interprets a missing key as "no chain yet".
- The pure fold must maintain a remembered retirement set for `(family_id, version, scope)`:
  - Rejects any subsequent `member-transition` naming the retired version.
  - Rejects any closure `assertion` naming the retired horizon.
  - Rejects any subsequent `genesis` attempting to reopen the retired family version in that scope.
- **Explicit Exception:** An ordinary `assertion` performing a same-member value correction carries no family version (it targets a `fact_id` in the fact lattice). Value corrections on existing current member facts remain admitted normally.

#### Already-Both-Current Logs as Containment Boundary
- In workspaces where both versions already have current chains without a recorded handover (Finding 1 setup):
  - The log remains readable; historical acts replay without error.
  - Current calculation / marshal admission fails closed: `marshal_closure_authority` refuses ambiguous authority (two coexisting versions for the same family ID and scope).
  - **Containment Limit:** Refusal does **not** displace an already-saved derived zero in derivation currency, and does **not** silently record a handover or manufacture a historical retirement.
  - The synthetic helper that introduced two active versions alongside each other must be replaced before delivery; it is not a supported production setup.

#### Successor Membership Conditions, Removal, and Correction
- **Member Retention Condition:** Retained member facts remain in the lattice, but are recognized as members of the successor **if and only if** the successor declaration's `member_predicate.fact_type`, identity key schema, and `member_constraints` admit them. If constraints fail, admission blocks or refuses; it does not silently rewrite facts.
- **Removal After Handover:** Statement removal is recorded as a `member-transition` with `action: "remove"` naming the active successor version. It advances the successor horizon, displaces the successor closure via individuation, and displaces the derived zero via the `input` pin.
- **Correction Monotonic Limit:** A same-member value correction updates the finding in the lattice. Because supersession roots accumulate monotonically, a value correction cannot revive or un-displace a closure that was previously displaced by a transition or handover.

---

## 7. Provisional Recommendation: Value, Cost, Risk, and Boundaries

### Provisional Recommendation
**Adopt Approach A via Carrier Option 2 (Dedicated Handover Act):**
- **Value:** Provides a clean, monotonic lifecycle transition. Uses existing two-edge currency cascade (horizon entity supersession -> closure finding individuation -> derived zero input pin) without inventing new edge types or currency roots. Allows single-successor member transitions on the active version while permanently retiring the old version from split-brain writing.
- **Cost:** Requires allocating and publishing a dedicated kernel act schema (e.g. `act-family-handover.v1`), implementing its pure fold transition in `packages/kernel/`, and binding prospective pre-write pure validation to `ActLog.append` and `append_batch`.
- **Risk:** Requires explicit lifecycle contract text defining handover semantics; payload is strictly bounded to an absent target chain and cannot recover unhandovered both-current logs.
- **Explicit Containment Limitation:** Workspaces containing already-both-current logs without a handover act remain readable, but their ambiguous authority is refused by admission without displacing saved zeros. Such synthetic setups must be cleanly retired in test fixtures rather than handled via retroactive migration.

All items in this proposal represent **proposed contract requirements** submitted for Foreman and independent review, not implemented APIs, authorized changes, or owner-accepted decisions.
