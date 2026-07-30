# Review — Expressiveness and Recoverability

Audience: Foreman, Owner, Reviewers

Date: 2026-07-28. Track 0 of Capital-Gain Distributions and Form 1040 Line 7a.

## 1. Verification and Independence Attestation

### Launch Commit and Object Verification
- **Resolved Launch Commit:** `ae4397d489ca9a1c8a21c75ae58f466214df345c` (`ae4397d`) on branch `prototypes/capital-gain-distributions-line7a/it2`.
- **Incumbent Object:** `1a7530faa68cd382f5216e2a4f1373416632a3ae` (`it1`), measuring `docs/prototypes/capital-gain-distributions-line7a/it1/design.md` and `docs/prototypes/capital-gain-distributions-line7a/it1/examination.md`.
- **Rival Object:** `099882e` (`it2`), measuring `docs/prototypes/capital-gain-distributions-line7a/it2/design.md` and `docs/prototypes/capital-gain-distributions-line7a/it2/examination.md`.
- **Evidence Rung:** Rung 1 (static paper schema and content instances only).

### Independence Attestation
I attest that:
1. I have **not** read `docs/prototypes/capital-gain-distributions-line7a/reviews/contract-adversary.md`.
2. I have **not** read the foreman's early incumbent check, either Builder's thread, summary, or uncommitted work, or any future triage, repair, or disposition.
3. My analysis is based strictly on the committed Rung-1 paper artifacts (`it1` and `it2`) and the governing contracts named in the charter.

---

## 2. 20-Row Recovery Matrix (10 Shared Cases × 2 Designs)

For each case and design, the six required recovery questions are evaluated:
1. **Q1 (Producer):** Authoritative producer.
2. **Q2 (Route):** Why direct route applies, blocks, or is inapplicable.
3. **Q3 (Source/Closure):** Exact current source set, horizon, and closure.
4. **Q4 (Consumers):** Downstream consumers through line 7a, line 9, taxable income, and line 16.
5. **Q5 (Displacement):** Fact, transition, or supersession that displaces the result.
6. **Q6 (Failure State):** Exact failure or non-publication state.

Legend: `recovered` (R), `contradictory` (C), `missing` (M).

| Case | Design | Q1 Producer | Q2 Route | Q3 Source/Closure | Q4 Consumers | Q5 Displacement | Q6 Failure State | Matrix Result | Citation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **1. Single Payer** | Incumbent | R | R | R | R | R | R | **recovered** | `it1/design.md` §1, §6 |
| | Rival | R | R | R | R | R | R | **recovered** | `it2/design.md` §P1-P3, Case 1 |
| **2. Multi Payer** | Incumbent | R | R | R | R | R | R | **recovered** | `it1/design.md` §1, §6, Case 2 |
| | Rival | R | R | R | R | R | R | **recovered** | `it2/design.md` §P1-P3, Case 2 |
| **3. Auth Missing** | Incumbent | R | R | R | R | R | R | **recovered** | `it1/design.md` §1, §6, Case 3 |
| | Rival | R | R | R | R | R | R | **recovered** | `it2/design.md` §P1-P3, Case 3 |
| **4. Schedule D Req** | Incumbent | R | R | R | R | R | R | **recovered** | `it1/design.md` §1, §6, Case 4 |
| | Rival | R | R | R | R | R | R | **recovered** | `it2/design.md` §P1-P3, Case 4 |
| **5. Contradiction** | Incumbent | R | R | R | R | R | R | **recovered** | `it1/design.md` §1, §6, Case 5 |
| | Rival | R | R | R | R | R | R | **recovered** | `it2/design.md` §P1-P3, Case 5 |
| **6. Auth Lifecycle** | Incumbent | R | R | R | R | R | R | **recovered** | `it1/design.md` §1, §6, Case 6 |
| | Rival | R | R | R | R | R | R | **recovered** | `it2/design.md` §P1-P3, Case 6 |
| **7. Family Lifecycle** | Incumbent | R | R | R | R | R | R | **recovered** | `it1/design.md` §1, §6, Case 7 |
| | Rival | R | R | R | R | R | R | **recovered** | `it2/design.md` §P2, Case 7 |
| **8. Reach-Around** | Incumbent | R | R | R | R | R | R | **recovered** | `it1/design.md` §1, §6, Case 8 |
| | Rival | R | R | R | R | R | R | **recovered** | `it2/design.md` §P2, Case 8 |
| **9. Double-Count** | Incumbent | R | R | R | R | R | R | **recovered** | `it1/design.md` §1, §6, Case 9 |
| | Rival | R | R | R | R | R | R | **recovered** | `it2/design.md` §P3, Case 9 |
| **10. Qual-Zero** | Incumbent | R | R | R | R | R | R | **recovered** | `it1/design.md` §1, §6, Case 10 |
| | Rival | R | R | R | R | R | R | **recovered** | `it2/design.md` §P3, Case 10 |

---

## 3. Detailed Case-by-Case Recoverability Breakdown

### Case 1 — Eligible Single Payer (Positive Baseline)
- **Incumbent (`it1`):** Recovered (`it1/design.md` §1, §6).
  - Q1: `tax.us.2025.schedule-d-required` = `"no"`; member `box2a.alpha-1` = 400.
  - Q2: `schedule-d-required` == `"no"` and family `2a` closed on `h0`.
  - Q3: `{box2a.alpha-1}`, horizon `h0`, `closure-2a.h0` == true.
  - Q4: `line7a-total` = 400 → `line9` (+400 once) → `taxable-income` → `line16` (QDCG base Q+400).
  - Q5: Supersession of `schedule-d-required` or membership change/closure loss.
  - Q6: N/A (positive case; publishes 400).
- **Rival (`it2`):** Recovered (`it2/design.md` §P1-P3, Case 1).
  - Q1: 3 Exception-1 components (`only-box2a`="yes", `no-losses`="yes", `no-qof`="yes") forming predicate E; checked conclusion `schedule-d-required.conclusion`="no"; member `box2a.alpha-1` = 1500.
  - Q2: Predicate E holds and family `2a` closed on `demo-horizon-2a-h0`.
  - Q3: `{box2a.alpha-1}`, horizon `demo-horizon-2a-h0`, `closure-2a.h0` == true.
  - Q4: `line7a-total` = 1500 → `line7b` (affirmative) → `line9` (+1500 once) → `taxable-income` → `line16` (QDCG base Q+1500).
  - Q5: Supersession of any Exception-1 component or membership change/closure loss.
  - Q6: N/A (positive case; publishes 1500).

### Case 2 — Eligible Multiple Payers (Positive Composition)
- **Incumbent (`it1`):** Recovered (`it1/design.md` §1, §6, Case 2).
  - Subtotal 550 from members `alpha` (400) + `beta` (150); dual member pins on `2a-subtotal`; line 7a publishes 550; included once in line 9 and QDCG.
- **Rival (`it2`):** Recovered (`it2/design.md` §P1-P3, Case 2).
  - Subtotal 1750 from members `alpha-1` (1500) + `beta-1` (250); dual member pins; line 7a publishes 1750; included once in line 9 and QDCG.

### Case 3 — Authority Missing (Mandatory Negative)
- **Incumbent (`it1`):** Recovered (`it1/design.md` §1, §6, Case 3).
  - Q1: `tax.us.2025.schedule-d-required` is missing.
  - Q2: Presence-before-value requirement fails.
  - Q3: Member `alpha` = 400, horizon `h0`, closure true.
  - Q4: Line 7a blocked; line 9 omits direct line 7a; line 16 has no line 7a input.
  - Q5: Contribution of `schedule-d-required` initiates a new run.
  - Q6: `blocked` state (non-publication walk names missing `tax.us.2025.schedule-d-required`; no zero inference).
- **Rival (`it2`):** Recovered (`it2/design.md` §P1-P3, Case 3).
  - Q1: Component `no-qof-deferral` is missing (or all 3 missing).
  - Q2: Predicate E fails; `schedule-d-required.conclusion` is undefined.
  - Q3: Member `alpha` = 1500, horizon `h0`, closure true.
  - Q4: Line 7a blocked; line 9 omits direct line 7a; line 16 has no line 7a input.
  - Q5: Contribution of missing component initiates a new run.
  - Q6: `blocked` state (non-publication walk names exact missing component `tax.us.2025.exception1.no-qof-deferral`; no zero inference).

### Case 4 — Schedule D Required (Mandatory Negative)
- **Incumbent (`it1`):** Recovered (`it1/design.md` §1, §6, Case 4).
  - Q1: Contributed `tax.us.2025.schedule-d-required` = `"yes"`.
  - Q2: Direct route inapplicable due to categorical `"yes"`.
  - Q3: Member `alpha` = 400, horizon `h0`, closure true.
  - Q4: Line 7a not published; line 9 omits line 7a; QDCG line 16 `guard_inapplicable` (no Schedule D or attachment artifact produced).
  - Q5: Supersession of `schedule-d-required` to `"no"`.
  - Q6: `guard_inapplicable` (structurally distinct from `blocked`).
- **Rival (`it2`):** Recovered (`it2/design.md` §P1-P3, Case 4).
  - Q1: Component `only-box2a-capital-gains` = `"no"`. Checked conclusion `schedule-d-required.conclusion` = `"yes"`.
  - Q2: Direct route inapplicable because predicate E fails due to `"no"` value.
  - Q3: Member `alpha` = 1500, horizon `h0`, closure true.
  - Q4: Line 7a not published; line 7b does not claim exception; line 9 omits line 7a; QDCG line 16 `guard_inapplicable` (no Schedule D or attachment artifact produced).
  - Q5: Supersession of component `"no"` to `"yes"`.
  - Q6: `inapplicable` / `guard_inapplicable`.

### Case 5 — Contradiction Interlock (Mandatory Negative / Admission)
- **Incumbent (`it1`):** Recovered (`it1/design.md` §1, §6, Case 5).
  - ADR-0038 decision 5 contradiction between `CAPITAL_GAIN_DISTRIBUTION_RECORDED` signal from box 2a member and `capital-gain-distributions` = `"no"`. Declaration-first, statement-first, and same-batch all fail closed at admission.
- **Rival (`it2`):** Recovered (`it2/design.md` §P1-P3, Case 5).
  - Interlock preserved with signal re-homed to successor family member. Declaration-first (5a), statement-first (5b), and same-batch (5c) fail closed at admission.

### Case 6 — Authority Lifecycle (Mandatory Lifecycle)
- **Incumbent (`it1`):** Recovered (`it1/design.md` §1, §6, Case 6).
  - Bidirectional trace: `schedule-d-required` supersedes `"no"` → `"yes"` → `"no"`. Prior line 7a, line 9, line 16 findings displaced via derivation pins; new run derives updated findings without editing history.
- **Rival (`it2`):** Recovered (`it2/design.md` §P1-P3, Case 6).
  - Bidirectional trace: `only-box2a-capital-gains` supersedes `"yes"` → `"no"` → `"yes"`. Predicate E transitions true → false → true; derivation edges displace downstream findings cleanly.

### Case 7 — Family Lifecycle (Mandatory Lifecycle)
- **Incumbent (`it1`):** Recovered (`it1/design.md` §1, §6, Case 7).
  - 7a closed-empty → line 7a = 0 (published zero, not inapplicable); 7b open / 7c undeclared / 7d stale-horizon → line 7a `blocked` under `require_closed`; 7e member value correction → line 7a updates to 1600; 7f member removal → advances horizon to `h1`, displacing prior closure.
- **Rival (`it2`):** Recovered (`it2/design.md` §P2, Case 7).
  - 7a closed-empty → line 7a = 0 (when E holds); 7b open / 7c undeclared / 7d stale-horizon → line 7a `blocked`; 7e member value correction → line 7a updates to 1600; 7f member removal → advances horizon to `h1`.

### Case 8 — Historical Reach-Around Attack (Mandatory Negative)
- **Incumbent (`it1`):** Recovered (`it1/design.md` §1, §6, Case 8).
  - Rule collect attack (8a) and mixed package graph (8b) rejected by package exclusivity sentence (S2.7) and universe guard.
- **Rival (`it2`):** Recovered (`it2/design.md` §P2, Case 8).
  - Rule collect attack (8a) and mixed package graph (8b) rejected by package exclusivity sentence and `dividend-universe.v2`.

### Case 9 — Downstream Double-Count Attack (Mandatory Negative)
- **Incumbent (`it1`):** Recovered (`it1/design.md` §1, §6, Case 9).
  - Line 9 double-path (9a) and QDCG direct-read (9b) unrepresentable / rejected under declared package pins (line 9 pins `line7a-total` once; QDCG pins `line7a-total` symbol only).
- **Rival (`it2`):** Recovered (`it2/design.md` §P3, Case 9).
  - Line 9 double-path (9a) and QDCG direct-read (9b) rejected by package validation (line 9 v3 pins `line7a` symbol once; QDCG pins `line7a` symbol only).

### Case 10 — Qualified-Zero Neighbor (Positive Boundary)
- **Incumbent (`it1`):** Recovered (`it1/design.md` §1, §6, Case 10).
  - Q = 0, box 2a = 400, `schedule-d-required` = `"no"`. Line 7a publishes 400 on income side; line 9 includes 400; line 16 tax computation does not read capital-gain declarations when Q=0, preserving ADR-0038 qualified-zero reduction (ordinary tax on total taxable income).
- **Rival (`it2`):** Recovered (`it2/design.md` §P3, Case 10).
  - Q = 0, box 2a = 1500, E holds. Line 7a publishes 1500 on income side; line 9 includes 1500; line 16 tax computation does not read Exception-1 components when Q=0, preserving ADR-0038 qualified-zero reduction.

---

## 4. Findings and Recommended Gate-5 Classifications

### `FINDING-EXP-001` — Incumbent Conclusion-Level Authority Cost
- **Proposition:** P1 (Direct-route authority and completeness).
- **Citation:** `it1/design.md` §6 P1 (U1); `it1/examination.md` §P1.
- **Description:** The incumbent topology relies solely on a single contributed categorical conclusion (`tax.us.2025.schedule-d-required` = `"no"`). It does not explicitly capture or check the statutory components of Form 1040 Exception 1 (`only-box2a-capital-gains`, `no-capital-losses`, `no-qof-deferral`).
- **Gate-5 Classification Recommendation:** `separate-decision` / residual topology uncertainty. (Non-blocking for paper sufficiency of the incumbent charter; represents a design trade-off between fewer contributed facts and less granular assertion checking).

### `FINDING-EXP-002` — Rival Component-Backed Authority Topology Cost
- **Proposition:** P1 (Direct-route authority and completeness).
- **Citation:** `it2/design.md` §P1 sentences 1–5; `it2/examination.md` §P1.
- **Description:** The rival topology requires taxpayers to contribute +3 categorical fact types (`only-box2a-capital-gains`, `no-capital-losses`, `no-qof-deferral`) and adds a checked-conclusion binding for `schedule-d-required.conclusion`.
- **Gate-5 Classification Recommendation:** `production-condition`. (Non-blocking for paper sufficiency; represents the contribution cost required for explicit statutory condition checking).

### `FINDING-EXP-003` — Case 10 QDCG Preferential Expression Detail
- **Proposition:** P3 (Line-7a and QDCG handoff).
- **Citation:** `it2/design.md` Case 10; `it2/examination.md` §P3.
- **Description:** Whether the 2025 IRS QDCG worksheet requires applying preferential rate schedules to capital-gain distributions when qualified dividends are zero is an expression detail on the successor line 16 rule.
- **Gate-5 Classification Recommendation:** `production-condition`. (Implementation expression detail for Track 2; does not affect paper contract selection or double-count protection).

---

## 5. Proposition-Level Sufficiency Summary

| Proposition | Incumbent (`it1`) Sufficiency | Rival (`it2`) Sufficiency | Blocking Gaps |
| --- | --- | --- | --- |
| **P1: Direct-route authority** | **Sufficient at Rung 1** | **Sufficient at Rung 1** | None |
| **P2: Box-2a family promotion** | **Sufficient at Rung 1** | **Sufficient at Rung 1** | None |
| **P3: Line-7a and QDCG handoff** | **Sufficient at Rung 1** | **Sufficient at Rung 1** | None |

Both designs provide complete, precise successor contract sentences and concrete synthetic evidence across all ten shared cases at Rung 1.

---

## 6. Topology Comparison and Rung-2 Judgment

### Topology Comparison
1. **Fact and State Economy:**
   - The **Incumbent (conclusion-level)** topology is recoverable with fewer contributed facts (1 categorical declaration vs 3) and fewer conditional state checks (1 presence/value check vs 3).
2. **Explicitness and Explainability:**
   - The **Rival (component-backed)** topology makes missing, contradiction, and correction states explicit per statutory condition rather than inferred inside a single opaque conclusion. Each component (`only-box2a`, `no-losses`, `no-qof`) is independently contributable, correctable, and explainable.
3. **P2/P3 Independence:**
   - Neither topology fails to close P2 or P3. Both designs successfully promote box 2a into a horizon-closed composable family without mixing historical recorded content, enforce package exclusivity, publish line 7a once into line 9, hand off to QDCG as a selected publication, and preserve inapplicability when Schedule D is required.
4. **Paper Distinguishability:**
   - Paper already fully distinguishes both authority topologies and their trade-offs across all 10 cases at Rung 1.

### Rung-2 Judgment
- **Judgment:** **No Rung-2 climb is required.**
- **Rationale:** The plan's single authorized Rung-2 validator question ("Can committed validators mechanically distinguish successor box 2a from historical recorded box 2a and reject a mixed graph?") is answered completely on paper by structural package exclusivity rules (S2.7 / `dividend-universe.v2`). Neither design leaves an unresolved evaluator-semantics or validator-contract question. Mechanical kill-tests should remain standard production conditions in Track 1 rather than blocking prototype contract selection.

---

## 7. Final Verdict and Recommendation

**Final Recommendation:** **`READY`**

Both the Incumbent and Clean-Room Rival designs are fully specified, recoverable across all 10 shared cases, and closed across P1, P2, and P3 at Rung 1. The Foreman and Owner have complete, unblocked paper evidence to compare conclusion-level vs component-backed direct-route authority and select the contract topology for production Tracks 1–3.

