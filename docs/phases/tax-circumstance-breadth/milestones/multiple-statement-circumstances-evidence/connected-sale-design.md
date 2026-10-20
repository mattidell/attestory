# Connected Sale Design — From Account to Saved Explanation

Audience: Foreman, Builder, Reviewer.
Status: Connected design aligned with accepted ADR 0079 and implementation review for Track 0 review.
Target Assignment: Connected sale design finalization
Scope & Boundaries: Pure design and bounded diagnostic probe; no production code changes, no new schema allocations or ADRs, no general multi-document intake. Retains the one-statement Form 1098 limit.

---

## 1. High-Level Path: Strata Decoupling and Information Flow

To ensure each Form 1099-K retains its own account through the entire pipeline, the design cleanly decouples the existing recording foundation from the intended evaluation, combination, and saved explanation layers.

### Existing Recording Foundation (Current Behavior)
1. **Statement Intake and Identity:**
   - Statements are durably recorded in the act log via `record_f1099k_statement_durably` in `packages/tax/f1099k_statement_recording.py`.
   - Each statement is a member of the `tax.us.2025.f1099k` family and carries the canonical three-part statement identity key:
     ```text
     payer:     <payer-entity-id>
     statement: <statement-entity-id>  # stmt.{payer_id}.{tax_year}.{payer_ref}
     tax-year:  "2025"
     ```
   - Box 1a (`tax.us.2025.f1099k.box1a-gross-amount`) is asserted as the family member finding.
   - Box 4 (`tax.us.2025.f1099k.box4-federal-withholding`) is asserted as an attributed companion documentary finding with the same statement identity keys.
2. **Ordinary Circumstance Answers:**
   - The taxpayer answers fifteen finite circumstance questions per statement (purchase cost, platform fees, shipping arrangement, exclusive personal use, etc.).
   - All circumstance answers are durably recorded via `answer_f1099k_statement_answer_durably` and carry that statement's exact identity keys.
   - *Current Mechanism Gap:* While the recorder stores full statement keys, these keys do **not** currently prevent calculation leakage during evaluation. In the baseline engine, non-subject inputs are not emitted as keyed sources; they fall back to run-wide scalars in `marshal.py`, causing sibling statements to borrow each other's answers or block on scalar disagreement. The recording keys provide the essential input ownership that evaluation and transport must be designed to preserve.

### Intended Evaluation, Combination, and Explanation (To Be Built)
3. **Per-Statement Evaluation (Intended):**
   - The engine evaluates each statement's own facts independently under subject dispatch (`packages/derivation/subject_dispatch.py`).
   - For each statement subject, the engine derives four Tier 1 intermediate figures and one Tier 2 figure:
     1. `expected-box1a-gross-amount` (Tier 1: agreed price + sales tax + buyer-paid shipping)
     2. `amount-realized` (Tier 1: agreed price + conditionally buyer shipping - refund)
     3. `selling-expenses` (Tier 1: platform fees + seller-paid shipping)
     4. `adjusted-basis` (Tier 1: returns `purchase-cost` *only* when `cost-basis-known == "yes"` and `lasting-improvements-or-adjustments == "no"`; `lasting-improvements-or-adjustments` is categorical, and basis adjustments are unsupported in this route, evaluating to `"not-computed"`)
     5. `net-proceeds` (Tier 2: amount realized - selling expenses; consumes only derived Tier 1 symbols)
   - For each statement subject, the engine derives the categorical disposition `statement-loss-reason` (e.g., `supported-loss`, `cost-basis-unknown`, `unsupported-gain`, `unexplained-reconciliation-discrepancy`, `personal-use-unconfirmed`).
4. **Combined Schedule 1 Entry (Owner-Selected Policy 1 + Candidate C, Intended):**
   - An ordinary raw subtotal rule (`tax.us.2025.rule.f1099k-box1a-subtotal`) aggregates Box 1a gross amounts across the family under ADR-0016 collect authority. Under ADR-0014 Decision 5 and ADR-0016, present-source aggregation does not consult or pin closure authority: a nonempty `collect` rule sums raw present member facts without itself waiting for family closure.
   - A top-entry selection rule (`rule.schedule1-top-entry.v3`, adopting Candidate C's two-path selection) inspects all per-subject `statement-loss-reason` findings and requires whole-family closure.
   - The combined Box 1a entry is published to Schedule 1 top entry *only when every current statement in the closed family is a supported personal loss*.
   - A closed-empty family produces $0.00; any unresolved, unknown, non-loss, or unclosed family halts aggregate publication with a named generic reason.
5. **Saved Presentation and Review (Intended):**
   - `packages/derivation/presentation_projection.py` projects `f1099kStatementExplanation`, iterating over all current Form 1099-K statement subjects sourced from current finding state (`FindingState` + `compute_currency` + `lattice`), capturing each statement's distinct reported figures, answers, derived figures, and local reason (or local blocked disposition).
   - `packages/tax/f1099k_statement_review.py` reloads saved presentations, decoupling each statement's own status and Box 1a from the return-level top-entry field.

---

## 2. Per-Statement Input Transport: Concrete Mechanism Comparison & Fail-Closed Refusal (F4)

### Complete Inventory of Inputs Requiring Transport
The fifteen circumstance answers are declared in `packages/content/tax/2025/f1099k-circumstances.bundle.json`. Box 4 withholding is declared in `packages/content/tax/2025/f1099k.bundle.v3.json`. All sixteen are bound in `package.core-calculations.v48.json` with `mode: "optional_default"`, `version: "v1"`, and identity keys `["payer", "statement", "tax-year"]`.

| Symbol / Fact Type ID | Declared Bundle | Primary Consumers |
| :--- | :--- | :--- |
| `tax.us.2025.f1099k.box4-federal-withholding` | `f1099k.bundle.v3.json` | `statement-loss-reason` |
| `tax.us.2025.f1099k.covers-only-single-item` | `f1099k-circumstances.bundle.json` | `statement-loss-reason` |
| `tax.us.2025.f1099k.acquired-by-purchase` | `f1099k-circumstances.bundle.json` | `statement-loss-reason` |
| `tax.us.2025.f1099k.primary-purpose-at-acquisition` | `f1099k-circumstances.bundle.json` | `statement-loss-reason` |
| `tax.us.2025.f1099k.exclusive-personal-use` | `f1099k-circumstances.bundle.json` | `statement-loss-reason` |
| `tax.us.2025.f1099k.digital-asset-involvement` | `f1099k-circumstances.bundle.json` | `statement-loss-reason` |
| `tax.us.2025.f1099k.agreed-item-price` | `f1099k-circumstances.bundle.json` | `expected-box1a`, `amount-realized`, `statement-loss-reason` |
| `tax.us.2025.f1099k.shipping-arrangement` | `f1099k-circumstances.bundle.json` | `amount-realized`, `selling-expenses`, `statement-loss-reason` |
| `tax.us.2025.f1099k.platform-fees` | `f1099k-circumstances.bundle.json` | `selling-expenses`, `statement-loss-reason` |
| `tax.us.2025.f1099k.seller-paid-shipping` | `f1099k-circumstances.bundle.json` | `selling-expenses`, `statement-loss-reason` |
| `tax.us.2025.f1099k.sales-tax-collected-by-platform`| `f1099k-circumstances.bundle.json` | `expected-box1a`, `statement-loss-reason` |
| `tax.us.2025.f1099k.refund-amount` | `f1099k-circumstances.bundle.json` | `amount-realized`, `statement-loss-reason` |
| `tax.us.2025.f1099k.buyer-paid-shipping` | `f1099k-circumstances.bundle.json` | `expected-box1a`, `amount-realized`, `statement-loss-reason` |
| `tax.us.2025.f1099k.cost-basis-known` | `f1099k-circumstances.bundle.json` | `adjusted-basis`, `statement-loss-reason` |
| `tax.us.2025.f1099k.purchase-cost` | `f1099k-circumstances.bundle.json` | `adjusted-basis`, `statement-loss-reason` |
| `tax.us.2025.f1099k.lasting-improvements-or-adjustments`| `f1099k-circumstances.bundle.json`| `adjusted-basis`, `statement-loss-reason` |

---

### Option A: Existing-Schema Content Decomposition (16 Helper Rules)
- **Concept:** Under `rule-artifact.v14`, each rule permits only one `joined` pin. Option A introduces 16 intermediate 1-to-1 helper projection rules (one for Box 4 and each of the 15 answers).
- **Representative Shape:**
  Each helper rule declares:
  ```json
  "subject": { "id": "tax.us.2025.f1099k.box1a-gross-amount", "version": "v1" },
  "joined": { "id": "tax.us.2025.f1099k.<input>", "version": "v1" },
  "direction": "joined_contains_subject",
  "requires": ["tax.us.2025.f1099k.<input>"],
  "publishes": "tax.us.2025.f1099k.subject-<input>"
  ```
- **Footprint and Evidence Assessment:**
  - *Content Footprint:* Requires 16 new rule files (`rule.f1099k-subject-<input>.json`), 16 new published symbol declarations, and rewiring the 5 actual raw consumer rules (`expected-box1a`, `amount-realized`, `selling-expenses`, `adjusted-basis`, and `statement-loss-reason`) to read `tax.us.2025.f1099k.subject-<input>`. Note that `net-proceeds` consumes only derived Tier 1 figures, so it does not need rewiring.
  - *DAG Impact:* Under ADR-0076 scheduling, adds a full derivation tier; helper rules must evaluate before figure rules can evaluate.
  - *Explanation Trace:* Lengthens explanation trees and audit ledgers with 16 artificial pass-through derivation records.
  - *Compliance & Risk:* It does not require modifying `packages/derivation/`. However, it is **unexecuted** across the full 16 inputs; optional default fallback through intermediate joined rules has not been demonstrated in production fixtures, and managing 16 rewired rules creates long-term content maintenance drag.
- **Status:** Unselected. Engine changes cannot be claimed unavoidable without recognizing Option A's structural existence.

---

### Option B: Bounded Declaration Discovery & Named Fail-Closed Refusal (F4)
- **Concept:** Narrowly expand `emission_only` discovery in `packages/derivation/live.py` within `_resolved_run_material` to emit required raw inputs for subject-scoped rules as `SourceFact` rows, allowing `subject_dispatch.py`'s existing `_scope(subject, candidates)` to bind them directly by shared keys.
- **Explicit Bounded Emission Predicate in `_resolved_run_material` (`live.py`):**
  1. **Rule Target:** Inspect only rules declaring a non-null `subject` pin matching `tax.us.2025.f1099k.box1a-gross-amount` (version `v1`).
  2. **Allowed Input Set:** Restrict emission candidates strictly to the explicit set of 16 allowed identifiers (the 15 circumstance questions and Box 4 withholding).
  3. **Symbol Matching & Alias Exclusion:** For each symbol in `rule.get("requires", [])`:
     - Match against `package["input_bindings"]`.
     - **Strict Alias Exclusion:** Require `binding["symbol"] == binding["fact_type"]["id"]` (canonical bindings only; aliases strictly excluded).
     - **Binding Mode & Version:** Require `binding.get("mode") == "optional_default"` and `binding["fact_type"]["version"] == "v1"`.
  4. **Key Conformance:** Look up the fact type declaration in resolved `fact_types`. Require its `identity_keys` to match the Box 1a subject's identity keys exactly: `["payer", "statement", "tax-year"]`.
  5. **Emission Target:** Append discovered symbols to `emission_only` if not already in `collect_names` or `emission_only`.
- **Named Fail-Closed Boundary (Finding F4):**
  - *The Hazard:* In the engine baseline, a required symbol omitted from emission does not raise an error; it falls through to run-wide scalars in `marshal.py` or `_optional_default` in `subject_dispatch.py`. A silent discovery skip would therefore cause disagreeing answers to be replaced by declared defaults or agreeing answers to share a single unkeyed pin.
  - *Fail-Closed Contract:* To prevent an unhandled exception escape, `TransportContractError` is a newly proposed internal validation exception (not a current API). The proposed validation in `_resolved_run_material` raises this exception when a declaration mismatch occurs (e.g. alias present, non-`v1` fact type version, non-`optional_default` mode, or mismatched identity-key names/order). `live_coordinate_run` must catch this exception before reservation or run execution begins, immediately returning an existing `Refusal(reason=..., detail=...)` with no run performed and no output published. In current derivation contracts, `Refusal.reason` is a plain string; no published schema allocation is implied or required.
  - Under no circumstances will a non-conforming required symbol be permitted to fall back to a run-wide scalar or declared default. Matching conforming names stay strictly `emission_only` (never added to `collect_names`).
- **Scalar Compatibility & Scope Isolation:**
  - `emission_only` sources do not mark findings as "used", leaving ordinary scalar fallback for genuine scalar rules unaltered.
  - Mortgage rules (Form 1098) and student loan interest (SLI) rules do not declare the Box 1a subject and are completely unaffected by this predicate.

---

### Comparison and Recommendation
| Dimension | Option A (16 Helper Rules) | Option B (Bounded Emission in `live.py`) |
| :--- | :--- | :--- |
| **Engine Footprint** | Unmodified engine code | Targeted predicate in `_resolved_run_material` |
| **Content Footprint** | 16 new rules + 5 rules rewired + 16 new symbols | 0 new rules, 0 rewired rules |
| **DAG / Scheduling** | Adds 1 derivation tier; lengthens explanation DAG | Unchanged; direct evaluation |
| **Explanation Trace** | Artificial `subject-<input>` derivation hops | Direct attribution to raw inputs |
| **Safety Bound** | Bounded by joined helper contract | Coordinator catch to existing `Refusal(reason/detail)` |
| **Verification State**| Unexecuted across 16 inputs; unverified defaults | Executed for all 16 inputs in Step 6 probe |

**Recommendation:** Option B is the cleaner, more direct, and more maintainable path.

---

## 3. Candidate C Connection & Content Successors (F2, F3)

Candidate C was demonstrated on disposable content in P7 (`test_candidate_c_probe.py`). The connected production design adopts this exact pattern without duplicating P7 JSON.

### Required Content Successors (Findings F2, F3)
1. **Reason Rule Successor (`tax.us.2025.rule.f1099k-statement-loss-reason`, Finding F2):**
   - The adopted `rule.f1099k-statement-loss-reason.v3.json` publishes `multiple-f1099k-out-of-scope` whenever `shared_key_count` of Box 1a on `tax-year` > 1.
   - The successor rule removes this tax-year count guard, allowing multiple 2025 Form 1099-K statements to evaluate to their substantive categorical reasons (e.g. `supported-loss`).
   - **Form 1098 Invariant:** Form 1098 mortgage interest rules carry their own independent count stops. Form 1098's count stops remain strictly untouched.
2. **Family Claim & Mapping Successors (`tax.us.2025.f1099k`):**
   - Declare successor family claim (`family.f1099k`) authorizing `tax.us.2025.f1099k.box1a-subtotal` as a collected raw subtotal under ADR-0016 collect authority.
   - Declare closure mapping successor (`closure-mapping.f1099k`) admitting `tax.us.2025.f1099k.box1a-subtotal`.
3. **Raw Subtotal Rule (`tax.us.2025.rule.f1099k-box1a-subtotal`):**
   - Ordinary computation rule with `when: true`.
   - Collects `tax.us.2025.f1099k.box1a-gross-amount` over source set `tax.us.2025.f1099k`.
   - **Exact Cent Precision:** Preserves raw dollar-and-cent amounts via plain `add(collect)`; strictly avoids importing SLI whole-dollar rounding.
   - Under ADR-0014 Decision 5, does **not** wait for or consult family closure. (Note: P7's citation to "Decision 8" was an old erroneous number; ADR-0014 contains exactly five decisions, and present-source aggregation is Decision 5).
4. **Schedule 1 Top-Entry Selection Rule (`rule.schedule1-top-entry`):**
   - Adopts Candidate C's two-path selection pattern (`reads_subject_results`).
   - Requires whole-family closure.
   - Evaluates per-subject reasons: if all current statements are `supported-loss`, selects the raw subtotal; if any statement is unmodeled, unknown, or non-loss, halts aggregate publication with a named reason; if family is closed-empty, publishes $0.00.
5. **Schedule 1 Attachment Rule Successor (`rule.attachment.schedule-1`, Finding F3):**
   - In `rule.attachment.schedule-1.v3.json` (part `sch1-top-entry-f1099k`), `subtotal_symbol` and `tie_out.line_symbol` are currently pinned to `tax.us.2025.schedule1.top-entry`.
   - Under `package_validation.py`, a row subtotal and single-family tie-out line MUST equal the family's declared `authorizes_subtotal`.
   - The successor attachment rule updates its family pin, `subtotal_symbol`, and `tie_out.line_symbol` to follow the family's successor `authorizes_subtotal` (`tax.us.2025.f1099k.box1a-subtotal`).
   - **Crucial Invariant:** The attachment's row subtotal and tie-out follow the raw authority (`box1a-subtotal`), while the root `requirement.subtotals` retains the final top-entry symbol (`tax.us.2025.schedule1.top-entry`), not an enclosing-part requirement or new part field.
6. **Unresolved Rule Successor (`rule.f1099k-unresolved`, Finding F3):**
   - In `rule.f1099k-unresolved.v2.json`, path `statement` treats `count` of Box 1a > 1 as unresolved (`block` / `DEPENDENCY_ABSENT`).
   - The successor unresolved rule stops treating count > 1 as unresolved when every current statement reason is `supported-loss`.
7. **Package Graph Membership & Adoption (Finding F3):**
   - Content files are inert until included in an adopted package. The successor package (successor to `package.core-calculations.v48.json`) includes the reason successor, family successor, mapping successor, raw subtotal rule, top-entry selection rule, attachment successor, and unresolved rule successor.
   - The package is registered in the content package registry, followed by checksum-verified release and adoption; published schema manifests do not register packages.

### Exact Distinction of Aggregate Outcomes (Finding F3)
Under Candidate C, aggregate results are strictly distinguished using actual engine generic codes:
1. **Published Unknown:** When a statement's circumstance answers are incomplete (e.g. `cost-basis-unknown`), the statement's reason publishes normally. The top entry halts selection and records disposition code `DEPENDENCY_ABSENT`.
2. **Blocked / Uncovered Subject:** When a statement's reason calculation itself fails to evaluate (e.g. missing required dependency), the reason finding is absent. The top entry halts and records disposition code `DEPENDENCY_INVALID`, specifically citing that subject's Box 1a fact ID.
3. **Closed-Empty Family:** When the family is closed and contains zero statements, the top entry evaluates under `require_closed` and publishes `$0.00`.
4. **Unclosed Family:** When the family is unclosed (including an unclosed empty family), the top entry halts and records disposition code `SOURCE_SET_UNCLOSED`. It does **not** publish zero.

---

## 4. Statement Lifecycle, Change & Membership (ADR 0079, F6)

Handling changes and membership across multiple statements requires tracing each mutation through actual recorder operations in `packages/tax/f1099k_statement_recording.py` and honoring the exact constraints of ADR-0016, ADR-0017, and ADR 0079.

### 1. Answer Correction & Withdrawal
- **Answer Correction:** `correct_f1099k_statement_answer_durably` stages an assertion act for the new finding, displacing the prior finding for that statement's question. Sibling statement findings have disjoint fact IDs and remain current and unaffected.
- **Answer Withdrawal:** `withdraw_f1099k_statement_answer_durably(current_findings=[finding_id], ...)` stages a `finding-retracted` act for the specific statement's answer finding. Sibling statement findings remain intact.

### 2. Statement Correction (Same Horizon, Ordinary Assertions)
- `record_f1099k_statement_durably(..., corrected=True)` (lines 560–640) uses ordinary `assertion` acts on the **same** family horizon (`cur_h`). Under ADR-0017 Decision 4, a same-member value correction that does not change predicate membership does **not** advance the horizon.
- *Tax Logic Consequence:* If a taxpayer corrects Statement 1 Box 1a from $800 to $900 without updating circumstance answers, `expected-box1a` ($800) will no longer match Box 1a ($900). In `statement-loss-reason`, this mismatch evaluates to `unexplained-reconciliation-discrepancy`, halting Schedule 1 publication. It does not automatically remain `supported-loss` or produce a $1,500 aggregate.

### 3. Atomic Statement Removal Operation Design (`ActLog.append_batch` through `_commit`, Finding F6)
The recorder currently has **no API** to delete or retract an entire Form 1099-K statement.
- **Kernel Grammar Constraint:** `packages/kernel/contribution.py` sets `_SUCCESSOR_KINDS` to exactly `assertion` and `member-transition`. `apply_contribution_batch` raises `ContributionError` for any other kind. As corrected by the reviewer, `apply_contribution_batch` does NOT admit `finding-retracted`. Contribution grammar must not be widened.
- **Atomic Save Boundary:** The atomic operation in the kernel that already accepts `finding-retracted` is `ActLog.append_batch`.
- **Bounded Removal Function (`retract_f1099k_statement_durably`):**
  When removing Statement A while Statement B stands (or removing the last member):
  1. **Stage Remove Transition:** Construct an `act-member-transition.v3` act:
     ```json
     {
       "family": family_ref,
       "scope": scope,
       "member": {
         "action": "remove",
         "fact_id": fact_b1a_id
       },
       "successor": { "id": succ_h, "predecessor": pred_h }
     }
     ```
     Under ADR-0017 Decision 3, `apply_member_transition` validates the horizon and withdraws `fact_b1a_id`. A bad predecessor raises immediately and writes nothing.
  2. **Stage Companion Box 4 Retraction:** Stage a `finding-retracted` act for Statement A's `box4-federal-withholding` finding.
  3. **Stage Orphan Answers Retraction:** Query all current circumstance answers matching Statement A's `(payer, statement, tax-year)` keys and stage a `finding-retracted` act for each. This guarantees that if Statement A is ever re-asserted in a subsequent submission, stale circumstance answers do not silently reattach via `_scope`.
  4. **Single Atomic Commit via `_commit`:** Call the existing `_commit` helper with registry, original `LogContents`, full staged history, provenance, and expected revision. `_commit` validates the full act sequence, derives the new additions slice, and calls `log.append_batch` once, ensuring all-or-nothing persistence with no new contribution carrier grammar. If any act is invalid, none are written.
  5. **Post-Removal Closure & Last-Member Behavior (ADR-0017):**
     - Sibling statement member facts remain current.
     - The predecessor horizon's closure is displaced.
     - If Statement A was the last statement, the family is now empty. However, under Candidate C, an empty family does NOT automatically publish $0.00; it publishes $0.00 only when closed (`require_closed`). Until a fresh closure is attested on `succ_h`, the empty family remains unclosed, halting with `SOURCE_SET_UNCLOSED`.
     - A fresh closure attestation naming `succ_h` is recorded as a separate affirmative user act; the old closure is never copied or upgraded.
  6. **Alignment with ADR 0079:** Statement removal operates strictly as an `act-member-transition.v3` (`action: "remove"`) on the current active chain (the successor version). Under ADR 0079, same-version member transitions remain governed by ADR-0017 Decision 3; `apply_transition` checks that the predecessor horizon is current and the chain is active and not in `retired_chains`. Because removal mutates the active successor chain, it is completely unaffected by the retirement of earlier versions. The companion Box 4 retraction and circumstance answer retractions are staged as `finding-retracted` acts within the single all-or-none `ActLog.append_batch` call. Therefore, Unit 3's removal operation fits ADR 0079 completely unchanged.

### 4. Settled Successor-Family Authority Route & Membership After Handover (ADR 0079)

The owner accepted ADR 0079 on 2026-10-19 following independent review of its implementation. The previously open owner choice on Finding F1 is settled. Kernel handover, containment, and writer protections are implemented, and the clean v2 wash-sale fixture policy has resolved historical base fixture mismatches.

#### Settled Authority Route for the Form 1099-K Successor
1. **Successor Family Declaration & Mapping:**
   - Author a successor family declaration (`family.f1099k.v2.json`) whose closure claim explicitly authorizes the multi-payer Box 1a sum across multiple platforms under Policy 1 (replacing v1's single-statement limitation). It uses `source-family.v1`, which has no `member_constraints`, so every retained statement with the same member fact type and keys stays a member. Choosing `source-family.v2` would require stating each constraint's effect on retained statements first.
   - Author a matching closure-mapping successor (`closure-mapping.f1099k.v2.json`) admitting `tax.us.2025.f1099k.box1a-subtotal` for family version `v2`.
2. **Automatic Handover on Successor Write (ADR 0079 Option A):**
   - The durable writers (`record_f1099k_statement_durably` and `record_f1099k_no_statements_durably` in `packages/tax/f1099k_statement_recording.py`) take `family_version`.
   - When invoked with the successor version (e.g. `"v2"`), the writer checks active chains for `(tax.us.2025.f1099k, scope)`.
   - If an active predecessor chain (e.g. `"v1"`) exists, the writer automatically stages an `act-family-handover.v1` act in the same all-or-none `ActLog.append_batch` save before appending the first successor-version member transition or genesis.
   - Handover atomically retires the v1 chain (recorded in `HorizonState.retired_chains`), displaces the v1 horizon entity and all closure facts keyed on it, and establishes the initial successor horizon citizen (`family-horizon.v1`) with `predecessor` pointing across versions (ADR 0079 Decision 2).
   - Handover authorizes nothing by itself: an explicit fresh closure attestation on the successor horizon is required before the combined Schedule 1 entry can publish.
3. **Containment of Both-Current Logs & Refusal of Older-Version Writes:**
   - **Containment:** Under ADR 0079 Decision 4, `marshal_closure_authority` in `packages/derivation/marshal.py` refuses closure authority when more than one version chain is current for the same family ID and scope, raising `SourceAuthorityError("family has multiple active version chains")`. Calculation fails closed, and any saved prior result stays current.
   - **Refusal of Stale Writes:** If a durable writer is called with a version numerically older than the active chain (e.g. attempting to write `"v1"` when `"v2"` is active), `_version_number(cur_ver) > _version_number(family_version)` triggers immediate refusal with `F1099KRecordingRefused`, preventing accidental rollback or concurrent chain pollution.
   - **Pre-Persistence Fold & Second-Genesis Refusal:** Under ADR 0079 Decision 5 and ADR-0077, `ActLog.append` and `append_batch` enforce prospective lifecycle fold checks and refuse any new-write second genesis beside an active chain with `HorizonModelError("active chain already exists in scope")`.

#### Obtaining the Successor Version at the Recording Entry Point
- **Mechanism Selection:** `FAMILY_VERSION` stays `"v1"`. The caller that has adopted the successor package passes `family_version="v2"` through the writers' existing parameter. The recorder does not load the package. A workspace still adopted at core calculations v46–v48, which map the v1 family (`package.core-calculations.v48.json:3627-3636`), keeps writing v1.
- **Cost Assessment:**
  - *Why not move the constant:* existing single-statement fixtures (for example `tests/test_f1099k_personal_item_sale_track1.py`, on v47 and v48) call the writers without `family_version`. A v2 default would write a v2 chain that their v1 mapping cannot select, breaking them as the wash-sale bases broke.
  - *Cost of the parameter route:* each successor-package caller must pass the version explicitly, and a test of the successor route must do the same. No runtime cost and no new coupling.
  - *Displaced Alternative:* Dynamically looking up the active family version from the workspace's adopted package was considered, but rejected because it couples durable statement recording to derivation package loading and workspace registry state for no added safety benefit.

#### Membership After Handover
Under ADR 0079 and ADR-0017 Decision 5, horizon succession displaces the predecessor horizon entity in `fact_state.entities`, causing predecessor closure facts and findings to drop automatically. In contrast, retained statement facts (Box 1a member findings, Box 4 withholding, and circumstance answers) have statement identity keys (`payer`, `statement`, `tax-year`) independent of the horizon entity, and thus survive intact in the fact lattice across handover.
- **Successor Admission Rule:** Retained v1 statement facts are admitted as members of the successor family during calculation **only if** the successor family declaration retains the exact canonical member predicate `tax.us.2025.f1099k.box1a-gross-amount` and its matching identity keys (`payer`, `statement`, `tax-year`).
- **Member Constraints & Effect on Retained Statements:** Any new member constraints declared in the successor family (e.g. requiring positive amounts or platform exclusivity) evaluate directly against all retained statement facts during validation. Any retained statement that violates a successor constraint causes family validation to fail closed; retained statements are never silently mutated, coerced, or dropped. If the successor declaration adds no new member constraints, all retained v1 statements continue as valid members under the successor version.

---

## 5. Full-Identity Saved Projection and Review Remediation (F5)

Source inspection of `packages/tax/f1099k_statement_review.py` and `packages/derivation/presentation_projection.py` identified critical presentation hazards and honest remediation paths.

### Identified Hazards and Honest Remediation (Finding F5)
1. **Own Box 1a in Statement Review (Route 2 Snapshot):**
   - *Current Bug:* `f1099k_statement_review.py` sets `saved_calc["box1a"]` from `top_val`, which is the return-level Schedule 1 total (`tax.us.2025.schedule1.top-entry.form-field`). On a multi-statement return, this incorrectly reports the combined sum as the statement's own Box 1a.
   - *Route 2 Remediation:* `prepare_f1099k_statement_review` already extracts the statement's own `box1a` directly from current finding state (`review["statement"]["box1a"]`). Once `associate_saved_run` confirms revision currency, `review_f1099k_statement_with_saved_presentation` sets `saved_calc["box1a"] = review["statement"]["box1a"]`. This is minimal, grounded, and avoids fabricating unaccepted carrier fields like `reportedBox1a`.
2. **Sourcing Current Subjects Whose Reason Blocked:**
   - *Current Bug:* `_f1099k_statement_explanation` iterates only over `reason_publications`. If a statement's reason calculation itself blocked (e.g. `DEPENDENCY_ABSENT`), no publication exists, and the statement is silently omitted from `f1099kStatementExplanation`.
   - *Remediation:* Current subjects MUST be sourced from current finding state (`FindingState` + `compute_currency` + `lattice`). For each current Box 1a statement subject, the projector records an explanation entry containing either the published `reason` from `RunResult.publications`, or if evaluation blocked, captures the blocked disposition code and missing dependencies from `RunResult.dispositions`.
3. **Decoupling Local Reasons from Aggregate Blockage:**
   - *Current Bug:* The review reader currently sets status to `supported-loss` only if `top_entry` published and no unresolved block exists; otherwise, it labels the statement `actually-unresolved`. On a mixed pair, a supported statement is incorrectly branded with the aggregate block.
   - *Remediation:* When the revision matches, status is taken from the explanation entry whose `statementKeys` equal `review["statement"]["keys"]`:
     - If the entry has a published `reason`, use that local reason (e.g. `supported-loss`, `cost-basis-unknown`).
     - If the reason did not publish, use the subject block's `code` and `missing`.
     - The top-entry field remains the combined amount only. An aggregate blockage on the top entry does NOT relabel a sibling statement whose own local status is `supported-loss`.
4. **Structured-Key Matching & Identity Grounding:**
   - `statements.statement_entity_id(key)` returns `f"stmt.{key.payer_id}.{key.tax_year}.{key.payer_ref}"`, which embeds `payer_id` and `tax_year`.
   - The review reader matches explanation rows to statements using structured keys (`statementKeys: {"payer": ..., "statement": ..., "tax-year": ...}`) matching `review["statement"]["keys"]`.
5. **Legacy Fallback & Gating:**
   - *Currency Rule:* Any saved run whose revision does not match current workspace revision returns `recalculation-needed` and suppresses saved calculation.
   - *Legacy Fallback Gate:* The reader treats an unkeyed presentation as valid ONLY if:
     1. Exactly one current Form 1099-K statement subject exists in the workspace.
     2. Completed run revision matches review revision.
     If more than one statement exists, the reader refuses legacy unkeyed presentations as incompatible, reporting `recalculation-needed`.

---

## 6. Step 6 Executed Diagnostic Probe Evidence

The diagnostic probe for the connected sale design was executed directly against `packages/derivation/` and real recorded workspaces.

### Execution Output and Scope Limitations
- **Test Results:** 6 passed in 35.41s (`pytest -n auto`), targeted mypy passed with zero errors.
- **Rule Adapter Nature:** In `test_01`–`test_04`, the probe uses an in-memory adapter that replaces the reason rule's `value` with its `else` branch *after* package resolution to bypass the count guard (`shared_key_count > 1`). This is a disposable in-memory lift, **not** a checksum-published rule or adopted package successor.
- **Ownership Scope Boundary:** The probe proved actual source-row discovery and emission for all 16 inputs (16 rows per statement, 32 total), and verified representative provenance pins on `expected-box1a` (`agreed-item-price`). Full pin matrix assertions across all intermediate figures and categorical reasons remain a production verification condition.
- **Component Closure Diagnostics:** Tests 05 and 06 are component-level measurements of `marshal_closure_authority` and `resolve_closure_admissions`:
  1. *Test 05:* Measured before ADR 0079: pairing mapping v2 with a v1 closure then admitted closed membership through family-ID-only indexing. That behavior no longer holds. Exact-version selection now leaves the family out of `current_horizons` when only the v1 chain is current (`packages/derivation/marshal.py:320-333`).
  2. *Test 06:* Confirmed that dual horizon chains (`v1` and `v2`) for the same family ID raise `SourceAuthorityError` in `marshal_closure_authority`.

---

## 7. Concrete Acceptance Cases & Small Build Units

### Small Build Units (Ordinary Implementation Sequence Starting From Accepted Kernel)

With ADR 0079 accepted and implemented, no engine authority work remains: the `act-family-handover.v1` act kind, prospective lifecycle fold validation, remembered retirement, both-current containment in `marshal_closure_authority`, and recorder handover and refusal protections are already delivered in the kernel. The implementation units proceed directly from the accepted kernel foundation:

1. **Unit 1: Bounded Input Transport & Refusal (`packages/derivation/live.py`):**
   - *Requires Engine Change:* Yes. In baseline derivation, non-subject circumstance inputs for subject-scoped rules are not emitted as keyed sources; without this targeted discovery step in `_resolved_run_material`, they fall back to unkeyed scalars or declared defaults in `marshal.py` and `subject_dispatch.py`.
   - *Deliverables:*
     - Implement the bounded emission predicate in `_resolved_run_material` (`packages/derivation/live.py`) for the 16 allowed inputs of the Box 1a subject.
     - Implement the fail-closed validation check raising internal `TransportContractError` on alias, non-v1, non-`optional_default`, or mismatched identity keys.
     - Catch `TransportContractError` in `live_coordinate_run` before run reservation/start, immediately returning `Refusal(reason=..., detail=...)` without running derivation.
2. **Unit 2: Content Successors & Package Adoption (`packages/content/tax/2025/`):**
   - *Requires Engine Change:* No (pure declarative tax content and package release).
   - *Deliverables:*
     - Author reason rule successor (`tax.us.2025.rule.f1099k-statement-loss-reason`) removing the Box 1a tax-year count stop while leaving Form 1098 untouched.
     - Author family successor (`family.f1099k.v2.json`) authorizing `tax.us.2025.f1099k.box1a-subtotal` as a collected raw subtotal under ADR-0016 collect authority for multi-statement sums under Policy 1.
     - Author closure mapping successor (`closure-mapping.f1099k.v2.json`) admitting `tax.us.2025.f1099k.box1a-subtotal` for family version `v2`.
     - Author raw subtotal rule (`tax.us.2025.rule.f1099k-box1a-subtotal`) collecting Box 1a with exact cent precision via `add(collect)`.
     - Author Schedule 1 top-entry selection rule (`rule.schedule1-top-entry`) selecting the raw subtotal when all statements are `supported-loss` and family is closed.
     - Author Schedule 1 attachment rule successor (`rule.attachment.schedule-1`) with raw subtotal and single-family tie-out line following `box1a-subtotal`, while root `requirement.subtotals` retains `tax.us.2025.schedule1.top-entry`.
     - Author unresolved rule successor (`rule.f1099k-unresolved`) that does not treat count > 1 as unresolved when all reasons are `supported-loss`.
     - Adopt all successors into a successor core-calculations package, register in the content package registry, and release via verified checksum.
3. **Unit 3: Atomic Statement Removal (`packages/tax/f1099k_statement_recording.py`):**
   - *Requires Engine Change:* No (tax statement recording logic using existing kernel APIs).
   - *Deliverables:*
     - Implement `retract_f1099k_statement_durably` staging `act-member-transition.v3` (`action: "remove"`), companion Box 4 retraction (`finding-retracted`), and orphan answers retraction (`finding-retracted`) in one call to the existing `_commit` helper, which calls `ActLog.append_batch` once for all-or-none persistence.
     - Confirm removal executes on the active successor horizon without mutating contribution carrier grammar, fitting ADR 0079 unchanged.
4. **Unit 4: Presentation Projection & Saved Review Remediation (`packages/derivation/presentation_projection.py` & `packages/tax/f1099k_statement_review.py`):**
   - *Requires Engine Change:* Yes. Presentation projection lives in `packages/derivation/presentation_projection.py` and must be enhanced to iterate all current statement subjects from finding state and currency and project per-statement blocked rows into `f1099kStatementExplanation`.
   - *Deliverables:*
     - In `packages/derivation/presentation_projection.py`, source current statement subjects from finding state and currency, projecting explanation rows with local reason or subject-blocked code/missing dependencies.
     - In `packages/tax/f1099k_statement_review.py`, implement Route 2 review snapshot extracting own-Box-1a from `review["statement"]["box1a"]`.
     - Decouple local statement review status from the aggregate top-entry block using structured-key matching (`statementKeys`).
     - Gate legacy unkeyed presentations to single-statement workspaces at matching revisions, returning `recalculation-needed` for multi-statement runs.

### Concrete Acceptance Cases
1. **Two Supported Personal Losses (Differing Amounts):**
   - Statement 1 ($880 Box 1a, loss) + Statement 2 ($460 Box 1a, loss).
   - Expected: Schedule 1 top entry publishes $1,340.00. Statement 1 review shows own Box 1a ($880) and `supported-loss`. Statement 2 review shows own Box 1a ($460) and `supported-loss`.
2. **Two Supported Personal Losses (Identical Amounts & Answers):**
   - Statement 1 ($500 Box 1a, loss) + Statement 2 ($500 Box 1a, loss) with identical circumstance answers.
   - Expected: Separate provenance pins; Schedule 1 publishes $1,000.00; no finding ID collision.
3. **Mixed Outcome (One Supported Loss + One Unknown Cost Basis):**
   - Statement 1 ($880 Box 1a, loss) + Statement 2 ($460 Box 1a, `cost-basis-unknown`).
   - Expected: Schedule 1 top entry is blocked (`DEPENDENCY_ABSENT`). Statement 1 review preserves local status `supported-loss` with own Box 1a ($880). Statement 2 review shows its published reason, `cost-basis-unknown`.
4. **Answer Withdrawal on One Statement:**
   - Statement 1 and Statement 2 both initially supported.
   - Taxpayer withdraws exclusive personal use on Statement 2.
   - Expected: Statement 2 evaluates to `personal-use-unconfirmed`. Statement 1 remains `supported-loss`. Schedule 1 top entry blocks (`DEPENDENCY_ABSENT`).
5. **Statement Correction with Amount Mismatch:**
   - Taxpayer records corrected Statement 1 ($900 Box 1a) without updating agreed price ($800).
   - Expected: Statement 1 evaluates to `unexplained-reconciliation-discrepancy`. Statement 2 stands unaffected. Schedule 1 top entry blocks on Statement 1 discrepancy.
6. **Atomic Statement Removal:**
   - Statement 2 is removed via atomic `action: "remove"` member transition, companion Box 4 retraction, and answer retractions via existing `_commit` calling `ActLog.append_batch` once.
   - Expected: Statement 2 is completely removed. Return recalculates as a single-statement return for Statement 1 ($880.00 top entry) once fresh closure is attested for the successor horizon.
7. **Single-Statement & Form 1098 Invariant:**
   - Verify existing single-statement Form 1099-K fixtures and single-statement Form 1098 mortgage fixtures.
   - Expected: Zero regressions in single-statement tax and answer behavior; existing saved presentation files remain preserved and readable. Intended successor pins and explanation metadata may legitimately evolve under new package versions without invalidating historical saved outputs.
8. **v1 Closed-Empty Workspace Upgraded on First Statement:**
   - Workspace has a v1 closed-empty chain (`demo.f1099k.h0`) and closure attesting zero statements.
   - User records first statement under successor version `v2`.
   - Expected: Durable writer automatically stages `act-family-handover.v1` from v1 to v2 before the v2 member transition in the same `append_batch`. The v1 chain is retired; the v1 closure and derived $0.00 zero drop. Predecessor zero is no longer published; the family is unclosed at the v2 horizon that the member transition creates after the handover horizon; the handover horizon is already superseded once the member is recorded, and the fresh closure names the post-transition horizon. Completeness question must be answered under v2; Schedule 1 top entry halts (`SOURCE_SET_UNCLOSED`) until fresh v2 closure is attested.
9. **v1 Single-Statement Workspace Upgraded on Second Statement:**
   - Workspace has one v1 statement ($880 Box 1a) and its v1 closure.
   - User records a second statement ($460 Box 1a) under successor version `v2`.
   - Expected: Writer stages `family-handover` from v1 to v2 followed by the new v2 member transition. Retained v1 statement remains a member under v2 (matching canonical member predicate and keys); new v2 statement is added as member. Handover displaces the v1 closure attestation. Completeness must be asked and attested again under v2. The combined Schedule 1 top entry ($1,340.00) publishes only after fresh v2 closure is attested.
10. **Untouched v1 Workspace Under Successor Package:**
    - Workspace has v1 statement(s) and closure under v1 package; no new writes occur; core-calculations package advances to successor (adopting v2 family/mapping).
    - Expected: The v1 closure and its saved presentation stay current at the historical revision, readable through `associate_saved_run`. The successor mapping does not admit that closure, so the Form 1099-K family is absent from `current_horizons` and its dependent entries block; other adopted families in the run still marshal.
11. **Stale Older-Version Write Refused:**
    - Workspace has active successor chain (e.g. `v2`), and a caller or stale client invokes `record_f1099k_statement_durably` or `record_f1099k_no_statements_durably` with `family_version="v1"`.
    - Expected: Writer compares versions numerically via `_version_number` and immediately raises `F1099KRecordingRefused("cannot handover to older family version: current chain is v2, writer requested v1")`. The log remains completely unmutated.
