# Review Round 1 — Governance Review (Expression Language Extensions)

Reviewer: Antigravity (Gemini 3.5 Flash), 2026-07-14.
Seat: Governance Reviewer (Expression Language Extensions).

Artifacts reviewed:
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/expression-language-extensions/plan.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/expression-language-extensions/charter-it1.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/expression-language-extensions/charter-it2.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/expression-language-extensions/it1/design.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/expression-language-extensions/examination-it1.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/expression-language-extensions/it2/design.md`
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/expression-language-extensions/examination-it2.md`
- `docs/governance/` v0.1 (constitution, ontology, engineering-constraints, principles, commentary)
- Ratified ADRs 0002, 0004, 0006–0012, 0016, 0017, 0023, and 0024 (accepted 2026-07-13)
- `docs/archive/2026-08-02-milestone-artifacts/prototypes/conditional-selectors/evaluation-analysis.md`

I did not read the Adversary reviewer's output (`reviews/round-1-adversary.md`), any draft or notes toward ADR-0025, or any uncommitted working-tree changes under `packages/` or `tests/`. There are no prior ELX reviews.

---

## Convergence Under Independent Authorship

Independent clean-room authorship of both iterations yields complete convergence on the following core principles:
1. **Declared Defaults as Content (Article 11):** Both designs reject runner-resident default policy, requiring defaults to be declared in versioned content and parameter citizens.
2. **Prohibition of Overwriting (E3.1):** Both designs guarantee that asserted inputs are never overwritten by defaults; defaults are skipped entirely when an assertion exists.
3. **Derived Finding Representation (ADR-0009):** Both designs model the default value as a derived finding rather than fabricating a human assertion or using a shadow input store.
4. **Ordinary Derivation Edges (Article 7):** Both designs propagate default-based displacement to downstream consumers using only ordinary derivation edges, requiring no third edge kind.
5. **No Decimal Coercion:** Both designs agree that categorical comparison must compare exact string tokens without decimal conversion.
6. **Contained Disposition Failures (ADR-0012):** Both designs agree that type/domain mismatches must result in blocked/inapplicable dispositions rather than runner crashes.

---

## Findings

### ELX-G1: Displacement Mechanism (ELX-P1)
* **Applies to:** Incumbent (`it1/`) and Rival (`it2/`)
* **Classification:** `decision-blocking`
* **Evaluation:**
  - The incumbent (`it1/`) proposes a new root class `default_superseded`. This requires the system to dynamically pair a derivation `symbol` to a kernel `fact_id` at runtime. Because this mapping is not represented as a versioned citizen, it would have to live as ambient logic in the runner, violating Article 11. It also introduces a third class of roots, adding complexity to the core currency logic.
  - The rival (`it2/`) gives the default-resolution derived finding the same `fact_id` as the asserted finding (via `resolved_input.fact_id`). This allows the existing correction fold to naturally handle displacement based on `fact_id` equality. No symbol-to-fact mapping metadata is needed by the currency layer.
  - Neither design introduces stored standing-affecting state (currency remains derived, Article 7). However, the incumbent's mechanism quietly introduces runner-resident mapping state to pair symbols and facts, whereas the rival's mechanism is fully transparent and derived from the record.
  - **Verdict:** The rival's correction fold extension is more conformant to Article 7 and ADR-0010.

### ELX-G2: Default Declaration Structure (ELX-P1)
* **Applies to:** Incumbent (`it1/`) and Rival (`it2/`)
* **Classification:** `decision-blocking`
* **Evaluation:**
  - The incumbent introduces a new separate citizen: `optional-input-declaration.v1`.
  - The rival adds `optional_default` directly to the `fact-type.v2` citizen, pinning a parameter declaration, and maps it in `artifact-package.v2` via `input_bindings` with `mode: "optional_default"`.
  - Fact types are the canonical home for a fact's nature (`nature: "determinable"` vs `elective`) and its `value_schema`. Declaring the default on `fact-type.v2` allows static schemas to enforce that elective facts cannot default (E3.1) and that default parameter values match the fact's value schema. The incumbent's separate citizen requires duplicate symbol declarations and complex package-level cross-validation to prevent mismatching properties.
  - **Verdict:** The rival's declaration structure is cleaner, tighter, and more conformant to Article 11.

### ELX-G3: Pin Origin Traceability (ELX-P1)
* **Applies to:** Incumbent (`it1/`) and Rival (`it2/`)
* **Classification:** `production condition`
* **Evaluation:**
  - The incumbent adds a `default` pin role to record the declaration supplying the default value.
  - The rival adds a `resolved_input` block to `derived-finding.v2` and an `origin` field (`"assertion"` or `"declared_default"`) to both the default finding and downstream `input` pins.
  - Downstream rules must be able to report whether they stood on a default or an assertion to satisfy the explanation walker and ADR-0012 dispositions. Recording the origin directly in the finding structure and pins provides complete transparency.
  - **Verdict:** The rival's explicit pin origin recording is superior.

### ELX-G4: Static Validation of Categorical Comparison (ELX-P2)
* **Applies to:** Incumbent (`it1/`) and Rival (`it2/`)
* **Classification:** `decision-blocking`
* **Evaluation:**
  - The incumbent proposes a generic `match` op that accepts any expression, checking at runtime that operands are strings. It does not validate that operands share a common enum domain, so comparing `filing_status` to a state code is not caught during package validation.
  - The rival proposes `categorical_compare` and a typed `category_literal` specifying the `fact_type`. Package validation resolves the bindings and literal fact type, ensuring they share the same fact-type ID and schema version, and that the literal is a valid enum member.
  - **Citizen/Schema Conformance:** The rival's design is far more robust. It elevates domain mismatch to a static package-validation error (`MEMBER_SCHEMA_INVALID`) when knowable, protecting the evaluation graph before runtime. The incumbent's design relies purely on runtime type checks, leaving the contract loose.
  - **Verdict:** The rival's typed comparison and static validation are superior.

### ELX-G5: Mismatch Disposition Vocabulary (ELX-P2)
* **Applies to:** Incumbent (`it1/`) and Rival (`it2/`)
* **Classification:** `production condition`
* **Evaluation:**
  - Both designs successfully avoid decimal coercion by checking string exactness.
  - Both designs represent mismatch as a contained explained failure (blocked rule, no crash).
  - The rival defines specific blocked reasons: `DEPENDENCY_INVALID` for enum-invalid assertions, and `CATEGORICAL_DOMAIN_MISMATCH` for domain mismatches. This integrates cleanly with the ADR-0012 disposition vocabulary and the explanation walker. The incumbent's generic type failure is less diagnostic.
  - **Verdict:** The rival's specific blocked categories are preferred.

### ELX-G6: Code-to-Label Migration Pathway (ELX-P2)
* **Applies to:** Incumbent (`it1/`) and Rival (`it2/`)
* **Classification:** `decision-blocking`
* **Evaluation:**
  - The incumbent states that content upgrades in the milestone, but does not specify a migration mechanism.
  - The rival proposes a formal, governed migration: publishing a versioned code-to-label migration mapping artifact, presenting a successor label claim that cites the old code, and requiring the user to assert the successor claim. This ensures that old findings are displaced via ordinary correction/individuation edges (Article 7) and that human findings are never silently converted (Article 2).
  - **Article 2 / Article 7 Conformance:** The rival's migration design is highly conformant. Silent conversion of a human finding is a major governance violation; the rival's successor claim pathway is the correct governed mechanism.
  - **Verdict:** The rival's migration mechanism must be carried forward.

---

## Verdicts

### Incumbent Design (`it1/`)
- **ELX-P1 (Declared Optional Default):** `conditionally accept`
  - *Condition:* Replace the `default_superseded` root class with the rival's same-fact-ID correction fold extension, and replace `optional-input-declaration.v1` with the rival's fact-type and package bindings integration.
- **ELX-P2 (Categorical Comparison):** `reject`
  - *Reason:* Fails to provide static domain safety at package validation time, lacks a governed code-to-label migration pathway, and lacks specific blocked diagnostics.

### Rival Design (`it2/`)
- **ELX-P1 (Declared Optional Default):** `accept`
  - *Reason:* Fully satisfies Articles 7/11, provides a clean same-fact-ID correction fold, records clear pin origins, and avoids runner-resident pairing policy.
- **ELX-P2 (Categorical Comparison):** `accept`
  - *Reason:* Provides static domain validation, specific block diagnostics, and a governed, non-silent migration pathway for ADR-0024 codes.

---

## Recommendation

**Recommendation:** Carry the rival (`it2/`) design's mechanisms for both ELX-P1 (same-fact-ID correction folding and fact-type/package bindings) and ELX-P2 (categorical_compare with static domain validation and successor-claim migration) into ADR-0025.
