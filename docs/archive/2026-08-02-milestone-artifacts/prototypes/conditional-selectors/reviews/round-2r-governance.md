# Governance Review — Conditional Selectors, Round 2R (over it2)

- **Date:** 2026-07-13
- **Reviewer Seat:** Governance reviewer, Medium tier
- **Evidence Reviewed:** `plan.md`, `charter-it2.md`, `it2/design.md`, `examination-it2.md`, `reviews/round-1r-governance.md`, `reviews/round-1r-adversary.md`, `round-1r-triage.md`, the ratified governance set (`docs/governance/`), ADRs 0002–0012 and 0016–0017, and the committed `packages/derivation/` and `packages/kernel/` source at `HEAD`.
- **Exclusions Honored:** Excluded all tainted rounds (`reviews/round-1-*.md`, `round-1-triage.md`, `repair1/`, `charter-repair1.md`, `examination-repair1.md`, `reviews/round-2-adversary.md`, `reviews/round-2-governance.md`, `round-2-triage.md`), `evaluation-analysis.md`, `docs/adr/0019-*.md`, `docs/adr/0020-*.md`, the other round-2R review, and all `wip/`/`archive/` branches.

---

## Findings

### CS-G8R — Workaround for String Comparisons (Filing Status Numeric Strings)

- **Observation:** To compare filing status, the `it2` design maps the 5 statuses to numeric strings `"1"` (Single) through `"5"` (QSS). This is a direct workaround for the committed evaluator's `compare` operator (`packages/derivation/evaluator.py` lines 148–151), which unconditionally coerces all comparison operands to decimal values via `_as_decimal`.
- **Consequence:** While this representation is fully executable at Rung 2, it is a significant legibility concession. Arbitrary numbers replace clear categorical labels (like `"single"` or `"married_filing_jointly"`), violating the spirit of Article 11 (Legibility).
- **Verdict:** Evades the CS-G1R failure mode successfully for the prototype, but cannot be accepted for production. String comparison support must be added to the evaluator or a proper enum matching schema introduced.

### CS-G9R — Optional-Input Absence Detection Constraint (Forces Explicit Zero Assertions)

- **Observation:** The `it2` rules resolve the CS-A4R silent overwrite hazard by removing the default-injecting rules entirely. However, because the evaluator lacks absence-detection primitives and `requires` checks presence only, any unasserted input (e.g. absent age/blindness/spouse flags) causes a direct `ref` evaluation to raise `EvalBlocked(BLOCK_ABSENT)` and blocks standard deduction computation.
- **Consequence:** To execute the standard deduction rule, all optional inputs must be explicitly asserted (e.g., to `"0"` or `"1"`). This prevents tracing the required displacement lifecycle where an unasserted input defaults and then gives way to a later assertion.
- **Verdict:** Shows that CS-P1 cannot be fully settled without an engine/language extension for defaults/absence that conforms to Article 7 (no third edge) and Article 11 (legibility).

### CS-G10R — Bracket-Fold Canon and Row Shape Conformance

- **Observation:** The `it2` design successfully authors the missing `operation-semantics.v1` citizen for `bracket_fold` (using lower-inclusive/upper-exclusive bounds) and structures bracket table rows with legal `lower`, `upper`, and `rate` fields.
- **Consequence:** This ensures full conformance with the evaluator's `_bracket_fold` contract and satisfies the operation-semantics registry requirements.
- **Verdict:** Satisfied. Fully resolves prior failures CS-A1R and CS-A2R.

### CS-G11R — Spouse Eligibility Scoping and Exhaustiveness

- **Observation:** The `it2` rules handle standard deduction lookup and spouse additional deduction constraints exhaustively across all 5 filing statuses. Spousal additional deductions are correctly restricted to MFJ, and MFS when the separate eligibility fact is asserted.
- **Consequence:** Replaces status-specific rule duplication with unified logic referencing parameter tables, preserving graph simplicity.
- **Verdict:** Satisfied. Fully resolves prior failure CS-A3R.

---

## Rule on the Examination's Proposition Verdicts

1. **CS-P2 (Separation of Logic and Data):**
   - **Verdict:** Sound. The parameter citizens `p.standard-deduction`, `p.additional-deduction`, and `p.brackets` separate all policy amounts/rates from logic. The rules carry only references and control mechanics, conforming to Articles 9 and 11.
2. **CS-P1 (Derivation Cascade Modeling / Optional-Input Absence Gap):**
   - **Verdict:** Correct. The examination's deliberate non-settlement of CS-P1 due to the optional-input absence gap is contractually correct and honest under Articles 10/11. The system cannot assume or hardcode defaults, and the current language lacks an absence-detection construct.

---

## Assessment of Surfaced Authority Questions

1. **Authority Question 1 (Optional Input Default Mechanism):**
   - **Status:** **Genuine contract gap**. Currently, the system has no way to default unasserted elective/optional facts without introducing runner-resident policy (violating Article 11) or a third edge type (violating Article 7).
   - **Resolution Body:** **Governance Body** (or the owner via a Tier-3 ADR). It affects the core semantics of derivation and workspace edges.
2. **Authority Question 2 (Itemized Deduction Package):**
   - **Status:** **Resolvable within existing contracts**. Does not require engine changes. It simply requires designing a future rule package for itemized deductions that publishes to a distinct symbol or uses conflict semantics.
   - **Resolution Body:** **Foreman/Builder** (technical/product domain).

---

## Verdict

### Iteration 2 (Clean-Room Rival): **Conditionally Accept**

Conditions:
1. **String Comparison:** Design and adopt an evaluator/language update supporting text string comparison to eliminate numeric status codes (satisfying Article 11 legibility).
2. **Absence Contract:** Resolve the optional-input absence contract gap (Authority Question 1) via a schema-valid absence test or non-overwriting default mechanism conforming to Articles 7 and 11.

### Recommendation on CS-P1 Disposition

**Defer full ratification.** We recommend accepting the resolved subset (guarded derivation cascade) while pausing full implementation/merging of the conditional selectors feature until the optional-input absence contract is settled by the Governance Body.
