# Expressiveness and Recoverability Review — Covered Long-Term Gains, Schedule D Line 8a

Audience: Owner, Foreman, Prototype Committee
Date: 2026-08-01
Track: Track 0 of Covered Long-Term Gains, Schedule D Line 8a
Seat: Expressiveness Reviewer (Medium–High Capability)

---

## 1. Review-Object Verification & Boundary Echo

Before performing analysis or rendering a verdict, the review objects, scope, evidence ceiling, independence boundary, and stop conditions are verified and recorded.

### 1.1 Object Verification & Working-Tree Discrepancy
- **Incumbent Object (Iteration 1):** Commit `d4e220376cfa29785447fe8cc183355532eb168f`
  - `docs/archive/2026-08-02-schedule-d-covered-ltcg-evidence/prototypes/schedule-d-covered-ltcg-8a/it1/design.md`
  - `docs/archive/2026-08-02-schedule-d-covered-ltcg-evidence/prototypes/schedule-d-covered-ltcg-8a/it1/examination.md`
  - `docs/archive/2026-08-02-schedule-d-covered-ltcg-evidence/prototypes/schedule-d-covered-ltcg-8a/charter-it1.md`
- **Rival Object (Iteration 2):** Commit `bbecd3f3aae6777cf06e4bdbe58d91545f4faedd`
  - `docs/archive/2026-08-02-schedule-d-covered-ltcg-evidence/prototypes/schedule-d-covered-ltcg-8a/it2/design.md`
  - `docs/archive/2026-08-02-schedule-d-covered-ltcg-evidence/prototypes/schedule-d-covered-ltcg-8a/it2/examination.md`
  - `docs/archive/2026-08-02-schedule-d-covered-ltcg-evidence/prototypes/schedule-d-covered-ltcg-8a/charter-it2.md`
- **Working-Tree Discrepancy Note:** The active workspace branch tip (`prototypes/schedule-d-covered-ltcg-8a/it2`) is one commit ahead of the pinned rival commit `bbecd3f3aae6777cf06e4bdbe58d91545f4faedd` due to commit `69e99c15...` (a non-substantive grounding-citation addition). Per charter instructions, this review evaluates the exact pinned SHA `bbecd3f3aae6777cf06e4bdbe58d91545f4faedd` rather than the working-tree tip. Both objects match their pinned SHAs exactly.

### 1.2 Scope & Evidence Ceiling
- **Scope:** Case-by-case recoverability analysis across all eleven shared cases in `plan.md` for both incumbent and rival designs across Propositions P1 (Transaction Identity/Closure), P2 (Completeness Boundary), and P3 (Schedule D Content & QDCG Binding).
- **Evidence Ceiling:** Rung 1 static paper evidence only. No Rung-2 validator/evaluator code probes or runtime execution.

### 1.3 Independence Boundary & Stop Conditions
- **Independence Boundary:** Maintained strict clean-room isolation. The adversary/contract review (`reviews/contract-adversary.md`), foreman process logs/custody notes, and builder threads/summaries were neither read, requested, nor incorporated as evidence.
- **Stop Conditions:** No governance interpretation, no production/schema file edits, no validator/evaluator code probes, no real user data, and no scope expansion beyond P1–P3 were required.

---

## 2. Per-Case, Per-Design Recoverability Analysis

For each of the eleven shared cases in `plan.md`, the six recovery questions are answered separately for the **Incumbent (IT1: Nested Member Identity + Synthesized Conclusion)** and the **Rival (IT2: Independent Family + Direct Multi-Read)**.

### Shared Case 1: Eligible Single Broker, Single Transaction

| Recovery Question | Incumbent (IT1) Design | Rival (IT2) Design |
| --- | --- | --- |
| **1. Authoritative Producer** | `tax.us.2025.f1099b.covered-ltcg-txn` fact (`demo.txn.alpha-001`), proceeds 12000, basis 9000. | `T1` (`demo.txn.a.001@t1`), proceeds 6000, basis 2000, gain 4000, anchored to `SA` (`demo.anchor.a@a1`). |
| **2. Line 8a Applicability** | Applies: long-term, covered, basis reported, no adjustment codes, `proceeds >= basis` (gain-only). Admitted to `family.f1099b-covered-ltcg`. | Applies: passes `F8` (`demo.family.line8a@v1`) predicate via contributed assertions for covered, basis-reported, long-term, gain-only, no adjustment codes. |
| **3. Source / Closure / Completeness State** | Single member under horizon `demo.horizon.f1099b-ltcg-2025`; closure `closed-with-members`. Boundary conclusion `schedule-d-boundary.conclusion = complete` (D1 closed-with-members, D2 closed-empty, D3–D9 `"yes"`). | Family `F8` closed on `H8-1` with `{T1}` (`C8-1`). Direct completeness `BASE-B`: `B1` closed, `B2` closed-empty, `B3–B9` current `"yes"`. |
| **4. Downstream Consumers** | `subtotal` -> Line 8a (12k/9k/3k) -> Part II line 15 (3000) -> Part III line 16 (3000) -> Line 7a (`rule.form1040-line7a.v2` matches D1 closed-with-members -> 3000) -> Line 9 (adds 3000 once) -> Taxable Income -> Line 16 (`rule.form1040-line16.v4` Schedule-D branch -> QDCG). | Subtotal `L8.h=4000` -> `L15=4000` -> `LD16=4000` -> `ATT-D` (required-and-complete) -> `P` (`demo.selected-preferential-base` = 4000) -> `L7A` (4000) -> `L9` (adds 4000 once) -> Taxable Income -> `TAX16` (retains ADR-0050 partition, reads `P=4000 > 0`, selects QDCG). |
| **5. What Displaces Result** | Supersession of `demo.txn.alpha-001`, horizon advance, or displacement of any boundary component D1–D9. | Supersession of `T1` or `SA`, horizon advance `H8-1`, or displacement of any direct authority `B1–B9`. |
| **6. Failure / Non-Publication State** | Unclosed -> `blocked(DEPENDENCY_ABSENT)` on closure; missing component -> `blocked(DEPENDENCY_ABSENT)` naming component; violated component -> boundary `incomplete` -> Line 7a `blocked`. | Unclosed `B1/B2` -> unclosed non-publication; missing `B3–B9` -> `blocked(DEPENDENCY_ABSENT)` naming missing; violated `B3–B9` (`"no"`) -> `ATT-D` required-and-incomplete, `LD16/P/L7A` unproduced. |

---

### Shared Case 2: Eligible Single Broker, Multiple Transactions

| Recovery Question | Incumbent (IT1) Design | Rival (IT2) Design |
| --- | --- | --- |
| **1. Authoritative Producer** | Two distinct member facts `demo.txn.alpha-001` (12k/9k) and `demo.txn.alpha-002` (5k/4k) under statement `demo.stmt.alpha-2025`. | `T1` (6k/2k/4k) and `T2` (5k/3k/2k) under statement anchor `SA`. |
| **2. Line 8a Applicability** | Both apply independently. Keyed by `{broker, statement, transaction, tax-year}` so both remain distinct members under one statement. | Both apply independently. Keyed by `(2025, subject, anchor.a, sale-001/002)` so both remain distinct members under anchor `SA`. |
| **3. Source / Closure / Completeness State** | Family closed-with-members on `demo.horizon.f1099b-ltcg-2025`. Boundary `schedule-d-boundary.conclusion = complete`. | Family `F8` closed-with-members on `H8-1` covering `{T1, T2}`. Direct completeness `BASE-B` complete. |
| **4. Downstream Consumers** | `collect_members` sums: proceeds 17000, basis 13000, gain 4000. Line 8a = (17k, 13k, 4k) -> line 15 = 4000 -> line 16 = 4000 -> line 7a = 4000 -> line 9 -> Taxable Income -> line 16 (QDCG). | Subtotal `L8 = (11k, 5k, 6k)` with two distinct member pins -> `L15=6000` -> `LD16=6000` -> `ATT-D` -> `P=6000` -> `L7A=6000` -> `L9` -> Taxable Income -> `TAX16` (QDCG). |
| **5. What Displaces Result** | Supersession of either member tuple or horizon rotation. | Supersession of `T1`, `T2`, or `SA`, or horizon rotation. |
| **6. Failure / Non-Publication State** | Same as Case 1. | Same as Case 1. |

---

### Shared Case 3: Eligible Multiple Brokers

| Recovery Question | Incumbent (IT1) Design | Rival (IT2) Design |
| --- | --- | --- |
| **1. Authoritative Producer** | Members `demo.txn.alpha-001`, `demo.txn.alpha-002` (broker alpha) and `demo.txn.beta-001` (broker beta, 8k/6k). | `T1`, `T2` (anchor `SA`, broker A) and `T3` (anchor `SB`, broker B, 9k/5k/4k). |
| **2. Line 8a Applicability** | All three pass `member_predicate`. Family identity is return-level (brokers are entities inside member identity). | All three pass `F8` predicate. Anchors `SA` and `SB` are contributed. Family `F8` covers all statement anchors. |
| **3. Source / Closure / Completeness State** | Three members across two brokers under one family closure fact. Boundary complete. | Family `F8` closed-with-members covering `{T1, T2, T3}`. Direct `BASE-B` complete. |
| **4. Downstream Consumers** | `collect_members` sums: proceeds 25000, basis 19000, gain 6000 -> Line 8a = (25k, 19k, 6k) -> line 15 = 6000 -> line 16 = 6000 -> line 7a = 6000 -> line 9 -> Taxable Income -> line 16 (QDCG). | Subtotal `L8 = (15k, 7k, 8k)` -> `L15=8000` -> `LD16=8000` -> `ATT-D` -> `P=8000` -> `L7A=8000` -> `L9` -> Taxable Income -> `TAX16` (QDCG). |
| **5. What Displaces Result** | Supersession of any transaction member or closure/horizon displacement. | Supersession of any transaction or anchor, or horizon advance. |
| **6. Failure / Non-Publication State** | Same as Case 1. | Same as Case 1. |

---

### Shared Case 4: Transaction Correction

| Recovery Question | Incumbent (IT1) Design | Rival (IT2) Design |
| --- | --- | --- |
| **1. Authoritative Producer** | Corrected `demo.txn.alpha-001` re-asserted with proceeds 12500 (basis 9000). `demo.txn.alpha-002` untouched. | Corrected `T1c` (`demo.txn.a.001@t2`, proceeds 6200, basis 2000, gain 4200) on same identity tuple. `T2` untouched. |
| **2. Line 8a Applicability** | Corrected member re-asserts same 4-key tuple and free-supersedes prior finding. | Free supersession replaces current assertion for `sale-001`. |
| **3. Source / Closure / Completeness State** | Same horizon. `collect_members` reads current finding per member. Pre-correction finding (12000) displaced to history log. `alpha-002` remains current. | Family `F8` closure `C8-1` on same horizon `H8-1` covers `{T1c, T2}`. Prior `T1` finding displaced. |
| **4. Downstream Consumers** | Subtotal: proceeds 17500, basis 13000, gain 4500 -> Line 8a = 4500 -> line 15 = 4500 -> line 16 = 4500 -> line 7a = 4500 -> line 9 -> Taxable Income -> line 16 (QDCG). | Subtotal `L8 = (11200, 5000, 6200)` -> `L15=6200` -> `LD16=6200` -> `ATT-D` -> `P=6200` -> `L7A=6200` -> `L9` -> Taxable Income -> `TAX16` (QDCG). |
| **5. What Displaces Result** | Displaces pre-correction publications (line 8a = 4000, line 7a = 4000, etc.). | Displaces prior publications pinning `T1` (`L8@p1`, `LD16@p1`, `P@p1`, `L7A@p1`). |
| **6. Failure / Non-Publication State** | Free supersession does not fail; old finding is displaced. | Old publication is displaced; graph re-evaluates against `T1c`. |

---

### Shared Case 5: Completeness Component Missing or Violated (All 9 Components)

| Recovery Question | Incumbent (IT1) Design | Rival (IT2) Design |
| --- | --- | --- |
| **1. Authoritative Producer** | Baseline: 9 components. One missing or violated at a time across D1–D9. | Baseline: 9 direct authorities `B1` through `B9`. |
| **2. Line 8a Applicability** | D1 missing -> `blocked(DEPENDENCY_ABSENT)` on D1. D2 missing -> `blocked(DEPENDENCY_ABSENT)` on D2. D3–D9 missing -> `blocked(DEPENDENCY_ABSENT)` naming missing. Violating value (e.g., D3="no" or D7="no") -> boundary conclusion `incomplete`. | Variant `5-B1` (`B1` open/absent) -> `B1` unclosed. Variant `5-B2` (`B2` open/absent) -> `B2` unclosed. Variants `5-B3` to `5-B9` (declarations missing or `"no"`). |
| **3. Source / Closure / Completeness State** | Missing component -> `schedule-d-boundary.conclusion` is `blocked(DEPENDENCY_ABSENT)`. Violated component -> `schedule-d-boundary.conclusion = incomplete`. | Missing `B1/B2` -> unclosed non-publication. Missing `B3–B9` -> `blocked(DEPENDENCY_ABSENT)` naming exact missing declaration. Violated `B3–B9` (`"no"`) -> `ATT-D` is `required-and-incomplete` naming violated members. |
| **4. Downstream Consumers** | `rule.form1040-line7a.v2` checks boundary conclusion. If `blocked` or `incomplete` -> Line 7a is `blocked(DEPENDENCY_ABSENT)` naming missing/incomplete boundary. **Does not fall through to box-2a route.** Line 9, Taxable Income, Line 16 block. No Schedule D attachment published. | `ATT-D`, `LD16`, `P`, `L7A` do **not** publish. Line 9 and `TAX16` do not publish from this route. |
| **5. What Displaces Result** | Blocks publication of all downstream symbols. | Blocks publication of `P` and `ATT-D`. |
| **6. Failure / Non-Publication State** | Boundary conclusion is `blocked` or `incomplete`. Line 7a is `blocked(DEPENDENCY_ABSENT)`. Neither numeric zero nor Schedule D form is published. | `ATT-D` is `required-and-incomplete` (for `"no"`) or blocked/unclosed (for missing/open). `P` is unpublished. No fabricated zero or Schedule D. |

---

### Shared Case 6: Box-2a Interaction, Present and Nonzero

| Recovery Question | Incumbent (IT1) Design | Rival (IT2) Design |
| --- | --- | --- |
| **1. Authoritative Producer** | `demo.txn.alpha-001` (gain 3000) AND box-2a member present & closed-with-members at 450.00 (ADR-0050). | `T1` (gain 4000) AND box-2a member `demo.box2a.a@x1` = 1200 with closed family. |
| **2. Line 8a Applicability** | D1 closed-with-members. D2 closed-with-members (satisfies D2). D3–D9 `"yes"`. Boundary conclusion = `complete`. | `B1` closed with `{T1}`, `B2` closed with `{box2a.a=1200}`, `B3–B9` `"yes"`. Direct route C1="no" (1099-B present) -> direct route `guard_inapplicable`. Schedule-D route is REQUIRED and COMPLETE. |
| **3. Source / Closure / Completeness State** | Both D1 and D2 closed-with-members. Boundary complete. | Both families closed (`B1` at 4000, `B2` at 1200). `B3–B9` `"yes"`. |
| **4. Downstream Consumers** | **CRITICAL DEFECT IN IT1:** Line 7a match selects D1 Schedule-D branch. D1 branch reads Line 8a gain (3000), but **does NOT include box 2a (450) on Schedule D line 13 or anywhere else**. IT1 explicitly chooses *precedence over summation*, dropping the box-2a 450 gain entirely! Line 7a = 3000, Line 9 = 3000, QDCG = 3000. | `L8.h = 4000`, `L13 = 1200` (**box-2a subtotal included on Schedule D line 13!**), `L15 = LD16 = 5200`. `ATT-D` required-and-complete. `P = 5200`. `L7A = 5200`. `L9` consumes 5200 once. `TAX16` selects QDCG for `P=5200 > 0`. |
| **5. What Displaces Result** | Direct box-2a route is preempted by D1 precedence. | Direct box-2a producer (`P-direct`) is `guard_inapplicable` (C1="no"). |
| **6. Failure / Non-Publication State** | **IT1 drops 450 of real taxable gain** due to unratified precedence rule. | Exactly one route publishes `P=5200`. No double-counting into line 9 or QDCG, and no gain dropped. |

---

### Shared Case 7: Box-2a Interaction, Closed Empty

| Recovery Question | Incumbent (IT1) Design | Rival (IT2) Design |
| --- | --- | --- |
| **1. Authoritative Producer** | `demo.txn.alpha-001` (gain 4500 post-correction), box-2a family closed-empty. | `T1c` (gain 4200), box-2a closed-empty. |
| **2. Line 8a Applicability** | D1 closed-with-members, D2 closed-empty. D3–D9 `"yes"`. Boundary complete. | `B1` closed (`T1c`), `B2` closed-empty, `B3–B9` `"yes"`. Direct route C1="no" -> direct route `guard_inapplicable`. |
| **3. Source / Closure / Completeness State** | D1 closed-with-members, D2 closed-empty. Boundary complete. | `B1` closed (4200), `B2` closed-empty (0). `B3–B9` `"yes"`. |
| **4. Downstream Consumers** | Line 7a match selects Schedule-D branch -> Line 7a = 4500 -> Line 9 = 4500 -> Taxable Income -> Line 16 (QDCG via `rule.form1040-line16.v4`). | `L8.h = 4200`, `L13 = 0` (closure-backed zero), `L15 = LD16 = 4200`. `ATT-D` complete. `P = 4200`. `L7A = 4200`. `L9` = 4200. `TAX16` selects QDCG (`P=4200 > 0`). |
| **5. What Displaces Result** | Box-2a fallback branch in line 7a match is bypassed. | Direct route `P-direct` is `guard_inapplicable`. |
| **6. Failure / Non-Publication State** | N/A (positive publication). | N/A (positive publication). |

---

### Shared Case 8: Family Lifecycle

| Recovery Question | Incumbent (IT1) Design | Rival (IT2) Design |
| --- | --- | --- |
| **1. Authoritative Producer** | Family closure states: undeclared, open, closed-empty, stale-horizon, corrected. | Family closure states for `F8` (`B1`): closed-empty, open, undeclared, stale-horizon, correction/restoration. |
| **2. Line 8a Applicability** | Undeclared/Open -> `blocked(DEPENDENCY_ABSENT)`. Closed-empty -> Subtotal = 0 (closure-backed). Line 7a falls through to box-2a branch. Stale-horizon -> `require_closed` blocks. | Closed-empty (with box-2a empty, `B3–B9` `"yes"`) -> Schedule D not required; direct `P` may publish closure-backed 0 under ADR-0050. Open/Undeclared/Stale -> `B1` unclosed/absent -> `LD16, P, L7A` do not publish. |
| **3. Source / Closure / Completeness State** | Tracked per lifecycle state above. | Tracked per lifecycle state. |
| **4. Downstream Consumers** | Line 7a, line 9, line 16 update or block accordingly. | P, L7A, L9, TAX16 update or block accordingly. |
| **5. What Displaces Result** | Horizon advance or supersession displaces stale/old findings. | State changes displace downstream publications. |
| **6. Failure / Non-Publication State** | Undeclared/open/stale block; closed-empty produces closure-backed 0. | Stale/open/undeclared block; closed-empty yields not-required (no fabricated attachment). |

---

### Shared Case 9: Historical / Raw-Member Reach-Around Attack

| Recovery Question | Incumbent (IT1) Design | Rival (IT2) Design |
| --- | --- | --- |
| **1. Authoritative Producer** | Attacker attempts to read raw `tax.us.2025.f1099b.covered-ltcg-txn` members or pre-correction history directly into Line 16 / QDCG or Line 9. | Attacker attempts to read raw `T1`/`T1c` or superseded `B7@d1="yes"` directly into QDCG or Line 9. |
| **2. Line 8a Applicability** | Foreclosed by construction: subtotal rule only reads via `collect_members` over `family.f1099b-covered-ltcg`. Line 16 reads `selected_line7a`. | Foreclosed by construction: `P` pins `LD16`, which pins `B1–B9` and `L15`. QDCG reads `P`. |
| **3. Source / Closure / Completeness State** | No direct pin from Line 16 or QDCG to member fact type or family. | Superseded `B7@d1` makes `ATT-D@p1`, `LD16@p1`, `P@p1` non-current. |
| **4. Downstream Consumers** | Line 16 reads `selected_line7a`. Graph attempting raw read cannot be expressed in `rule-artifact.v3`. | Package attempting to retain `ATT-D@p1` while exposing current `B7@d2="no"` has a displaced-authority graph and is rejected. |
| **5. What Displaces Result** | Rejects raw-member read graph. | Rejects reach-around / displaced-authority graph. |
| **6. Failure / Non-Publication State** | Attempted raw read fails schema validation or evaluator execution. | Invalid graph produces no `L9` or `TAX16`. |

---

### Shared Case 10: Downstream Double-Count Attack

| Recovery Question | Incumbent (IT1) Design | Rival (IT2) Design |
| --- | --- | --- |
| **1. Authoritative Producer** | Variant (a): Box 2a closed-with-members AND D1 closed-with-members. Variant (b): QDCG reading raw transaction content. | Variant (a): Both box 2a (1200) and 1099-B (4000) present. Variant (b): Raw transaction read into QDCG. Variant (c): Both routes attempting to publish `P`. |
| **2. Line 8a Applicability** | Variant (a): Line 7a match uses precedence: if D1 is closed-with-members, Schedule-D branch fires. Box 2a is NOT read. (**Note: drops box 2a gain**). Variant (b): QDCG reads only `selected_line7a`. | Variant (a): Direct route C1="no" -> direct producer `guard_inapplicable`. Schedule-D route includes box 2a on line 13 (`L13=1200`), so `LD16=P=5200`. Both gains combined. Variant (b/c): Mechanical single-producer enforcement for `P`. |
| **3. Source / Closure / Completeness State** | Exactly one branch of match fires. | `P` receives 5200 from Schedule-D route only. Direct route is `guard_inapplicable`. |
| **4. Downstream Consumers** | Line 7a receives gain from Schedule-D branch only. Line 9 receives line 7a once. | `L7A = 5200`, `L9` adds 5200 once, QDCG reads `P=5200`. |
| **5. What Displaces Result** | Precedence rule prevents double addition into line 9 / QDCG. | Direct producer is `guard_inapplicable`. |
| **6. Failure / Non-Publication State** | Precedence prevents double count, but **drops box 2a in IT1**. | Invalid graph fails closed with no `L9`/`TAX16`. |

---

### Shared Case 11: Non-Covered / Adjustment-Code Transaction Rejected

| Recovery Question | Incumbent (IT1) Design | Rival (IT2) Design |
| --- | --- | --- |
| **1. Authoritative Producer** | Transaction with `basis_reported_to_irs: no` (non-covered) or `adjustment_code_present: yes`. | Transaction with non-covered, 1f, 1g, Ordinary, QOF, or missing gain-only assertion. |
| **2. Line 8a Applicability** | Evaluated against `member_predicate` at admission. Evaluates false -> rejected at admission gate. | Evaluated against `F8` predicate (`demo.family.line8a@v1`). Fails predicate -> excluded from family `F8`. |
| **3. Source / Closure / Completeness State** | Never enters `family.f1099b-covered-ltcg`. Invisible to `collect_members`. | Not admitted to `F8`. If no other transactions pass `F8`, `F8` is closed-empty. |
| **4. Downstream Consumers** | Subtotal rule `line8a-gain` does not include them. | Relevant declaration in `B3–B9` reflects non-absence if excluded transaction requires Form 8949, causing `ATT-D` to be required-and-incomplete. |
| **5. What Displaces Result** | Excluded from family. | Excluded from family `F8`. |
| **6. Failure / Non-Publication State** | Rejection at admission gate is silent exclusion (not an error state). | Bounded Schedule D route cannot complete if an excluded transaction requires Form 8949 or other reporting. |

---

## 3. Proposition Sufficiency Judgments

### 3.1 Incumbent (Iteration 1) Sufficiency
- **P1 (Transaction Source Family & Identity): SETTLED at Rung 1.**
  IT1 successfully models transaction identity as a four-key nested member `{broker, statement, transaction, tax-year}` under `family.f1099b-covered-ltcg`. Free supersession works at transaction grain, distinct sales from the same broker remain distinct, and non-covered/adjusted transactions are silently excluded by the admission gate.
- **P2 (Completeness Boundary): UNDERSPECIFIED / FLAWED at Rung 1.**
  IT1 generalizes ADR-0050 into a single synthesized conclusion `schedule-d-boundary.conclusion`. However:
  1. Component D7 collapses seven distinct statutory forms (Forms 2439, 4684, 4797, 6252, 6781, 8824, K-1 gains) into one composite declaration without proving how source data can attest it.
  2. Truth-table binding introduces vocabulary friction (`{complete, incomplete}`) against ADR-0050's `{yes, no}` domain.
  3. Requiring `checked-conclusion-binding.v2` to support `family_closure_state` typing is an unwritten schema extension.
- **P3 (Schedule D Content & QDCG Binding): FLAWED / UNACCEPTABLE at Rung 1.**
  IT1 exhibits two major defects:
  1. **Data Loss on Box 2a (Case 6 & Case 10a):** IT1's `rule.form1040-line7a.v2` match chooses *precedence over summation* when both 1099-B gains and box-2a distributions exist. It selects the Schedule-D branch, reading only Line 8a gain (3000), and **completely drops box 2a (450)** because box 2a is not added into Schedule D Line 13 or Line 15 in IT1. This results in under-reporting total gain on Form 1040 line 7a.
  2. **Unspecified Requirement Block:** `attachment.schedule-d.v1`'s `requirement` block is left unspecified because `attachment-rule.v2` requires a threshold-shaped expression while Schedule D's existence is categorical. IT1 notes this requires an `attachment-rule.v3` successor but does not draft its contract text.

### 3.2 Rival (Iteration 2) Sufficiency
- **P1 (Transaction Source Family & Identity): SETTLED at Rung 1.**
  IT2 models statement anchors `SA` with identity `(tax-year, subject, broker, statement)` and independent transaction members `T1` with identity `(tax-year, subject, anchor, transaction)`. Family `F8` (`demo.family.line8a@v1`) operates at return level across anchors. Free supersession, distinct member preservation, and admission gating are cleanly specified.
- **P2 (Completeness Boundary): SETTLED at Rung 1.**
  IT2 eliminates the synthesizing conclusion citizen entirely. Downstream rules (`ATT-D`, `LD16`, `P`) `require_closed` the two composable families (`B1`, `B2`) and directly read the seven categorical absence declarations (`B3–B9`). Presence of all nine authorities is checked before any value is read. Missing declarations yield `blocked(DEPENDENCY_ABSENT)` naming every missing item in one pass; present `"no"` values yield `required-and-incomplete` naming every violated item.
- **P3 (Schedule D Content & QDCG Binding): SETTLED at Rung 1.**
  IT2 introduces a clean, shared `selected-preferential-base` publication `P` (`demo.selected-preferential-base`). Form 1040 Line 7a publishes `P` exactly once. Form 1040 Line 16 retains ADR-0050 Decision 7's state partition unchanged, substituting `P` for `selected_line7a`. Crucially:
  1. **Preserves Box 2a Gain (Case 6):** When both 1099-B gain (4000) and box 2a (1200) exist, direct route C1 is `"no"` (`guard_inapplicable`). The Schedule-D route includes box 2a on Schedule D Line 13 (`L13=1200`), publishing total long-term gain `LD16 = P = 5200`. Neither gain is dropped or double-counted.
  2. **Single Producer Enforcement:** Exactly one route publishes `P` at any time. Multi-producer or reach-around graphs fail closed during package/graph validation.

---

## 4. Topology Distinguishability & Evidence Assessment

### 4.1 Topology Distinguishability on Static Paper
Static paper evidence at Rung 1 is **fully sufficient to distinguish** the incumbent and rival topologies across all three propositions:

1. **P1 Identity Topology:** Nested 4-key member under statement (IT1) vs. Independent family keyed to statement anchor (IT2). Paper proves both preserve distinct sales and local supersession, but IT2 decouples transaction closure from statement closure.
2. **P2 Completeness Topology:** Synthesized conclusion citizen (IT1) vs. Direct 9-authority multi-read (IT2). Paper proves IT2 provides superior diagnostic precision (naming exact missing/violated declarations without a conclusion hop) and eliminates an unnecessary citizen layer.
3. **P3 Route-Binding Topology:** Extended Line-16 state partition with Schedule-D branch (IT1) vs. Upstream `selected-preferential-base` publication `P` with unchanged Line-16 partition (IT2). Paper proves IT1 suffers from data loss (dropping box 2a in Case 6), whereas IT2 cleanly handles multi-source gain aggregation via Schedule D Line 13.

### 4.2 Unresolved Questions: Paper-Evidence Limits vs. Underspecification

- **Incumbent (IT1):**
  - *Case 10a Precedence Data Loss:* **Underspecification / Contract Defect.** Dropping box-2a gain when 1099-B is present is an invalid tax derivation choice, not a paper limit.
  - *Unwritten `attachment-rule.v3` Requirement Contract:* **Underspecification.** Leaving the attachment requirement block draft-less is an incomplete design.
  - *Component D7 1-vs-7 Form Arity:* **Genuine Paper-Evidence Limit.** Determining whether real source data can attest a single composite claim or needs seven separate declarations requires domain/product policy input.

- **Rival (IT2):**
  - *Multi-Producer Symbol Naming vs. Selected-Binding Citizen:* **Genuine Generic Machinery Limit.** Whether existing runner schemas allow two mutually exclusive rules to name symbol `P` or require a dedicated selection binding is a generic engine machinery question, appropriately deferred from Rung 1.
  - *Present `"no"` Walk Code Formatting:* **Production Condition.** Formatting standard walk codes for categorical absence violations is a Track 1–3 implementation task.
  - *Bounded Slice Deferred Scope:* **Deferred Scope.** Extending `LD16=L15>0` to general capital losses or collectibles is explicitly out of scope for this milestone.

---

## 5. Safety Scan Verification

Per reviewer standing disciplines and charter instructions, safety envelope scans were executed for both review ranges:

```sh
python3 tools/envelope_scan.py --range origin/main..bbecd3f3aae6777cf06e4bdbe58d91545f4faedd
python3 tools/envelope_scan.py --range origin/main..d4e220376cfa29785447fe8cc183355532eb168f
```

**Scan Results:**
- Both scans returned **0 findings / CLEAN**.
- No personal data, real identifiers, private paths, credentials, or unapproved artifacts cross the data boundary.

---

## 6. Final Recommendation & Verdict

### 6.1 Proposition-Level Verdicts

| Proposition | Incumbent (IT1) | Rival (IT2) | Recommendation |
| --- | --- | --- | --- |
| **P1 — Transaction Identity** | Settled | Settled | Both viable; IT2 anchor shape is cleaner. |
| **P2 — Completeness Boundary** | Flawed | **Settled** | **Adopt IT2 Direct Multi-Read.** Eliminates conclusion hop and provides exact 9-part failure walks. |
| **P3 — Schedule D / QDCG Binding** | **Unacceptable (Data Loss)** | **Settled** | **Adopt IT2 `selected-preferential-base` P.** Preserves box 2a on Line 13 and keeps Line 16 partition unchanged. |

### 6.2 Milestone Closeout Verdict

- **Incumbent (IT1): NOT READY.** Rejection recommended due to data loss on box-2a gains (Case 6) and unspecified attachment requirement contracts.
- **Rival (IT2): READY.** Ratification recommended. IT2 provides complete, recoverable, and contract-faithful successor specifications for P1, P2, and P3 without requiring a climb to Rung 2.

**Commit SHA:** (To be committed)
**Final Status:** `READY` (for Rival IT2 topology adoption).
