# Governance Review: Citation Resolution (Round 1)

**Reviewer:** Owner-Launched Governance Reviewer (Medium-tier)  
**Date:** 2026-07-15  
**Milestone:** Core Tax Conditions remediation, Track 0.c  
**Scope:** Two independent designs (incumbent `it1/` and clean-room rival `it2/`) for Citation Resolution (CIT-P1 and CIT-P2).

---

## 1. Governance Context and Floor

This review measures the compliance of both candidate designs against the ratified project governance:
- **Article 9 (Canon):** Schema-governed citizens, schema as the sole authority, strict validation, rejection of tolerant readers or repair.
- **Article 11 (Legibility):** Runner must remain thin, executing only what artifacts declare and contributing no tax/legal meaning.
- **Article 18 (Quarantine):** Fixtures must be synthetic and safe to publish.
- **ADR-0012 (Form Fields):** Form-fields are presentation-only citizens. Citations attached to them are descriptive/inert content. The field-to-symbol binding is one-way presentation.
- **ADR-0027 (Package Membership):** The adopted content package (`artifact-package.v2`) remains the sole membership and adoption authority. No path-based manifest.
- **ADR-0028 (Fact Surface & Obligation):** Fact types and bundles are versioned members; composition obligations are package-declared and non-circular.

---

## 2. Findings

### CIT-G1: Citation Identity - Citizen vs Value vs Pin Model
- **Classification:** Non-blocking
- **Evaluation:** Both `it1` and `it2` correctly reject inlining citation details as unstructured, unversioned values inside form-field or rule schemas. They both model a citation as a first-class, versioned **content citizen** (`citation.v1`) with an opaque ID, and use exact `{id, version}` pins for attachment. This satisfies ADR-0003 and prevents metadata drift.
- **Verdict (it1):** Accepted
- **Verdict (it2):** Accepted

### CIT-G2: Single Membership Authority
- **Classification:** Non-blocking
- **Evaluation:** Both designs reject the path-based `manifest.json` (from the inert ADR-0022) and declare that the adopted content package (`artifact-package.v2`) remains the sole membership and adoption authority. Citation citizens are pinned as members with a dedicated role, respecting ADR-0027.
- **Verdict (it1):** Accepted
- **Verdict (it2):** Accepted

### CIT-G3: Immutability and Version Control under Article 9
- **Classification:** Non-blocking
- **Evaluation:** Both designs adhere strictly to Article 9 (immutability). Citation citizens and package instances cannot be edited in-place. Updates (such as typo fixes) require publishing a new version (e.g., `v2`) and updating the referencing pins, validated via package/registry checksums.
- **Verdict (it1):** Accepted
- **Verdict (it2):** Accepted

### CIT-G4: Attachment Boundaries on Form-Fields and Rules
- **Classification:** Decision-blocking
- **Evaluation:** 
  - `it1` implements an array of citations (`citation_refs`) on both `form-field.v2` and `rule-artifact.v2`.
  - `it2` restricts `form-field.v2` to a single exact citation pin (`citation`), while allowing an array of citations (`citations`) on `rule-artifact.v2`.
  - **Ruling:** `it2`'s model is superior. Under ADR-0012, a form-field is a presentation citizen representing a single printed location. Its meaning is defined by a single specific authority (typically form instructions). Multi-authority grounding should live on the computation rule, not the form-field citizen itself. A single citation pin on the form-field prevents semantic drift and preserves presentation-only clean boundaries. Allowing multiple citations on a form-field violates the singular definition of "a source-citation reference" in ADR-0012 §2.
- **Verdict (it1):** Rejected (violates ADR-0012 presentation boundaries by allowing multiple source-citation references on a single form-field citizen).
- **Verdict (it2):** Accepted

### CIT-G5: Display Canonicalization and Resolver Overreach
- **Classification:** Decision-blocking
- **Evaluation:**
  - `it1` requires a `display` field in the citation citizen and enforces deterministic display canonicalization in the resolver (generating string templates for IRC and IRS_AUTHORITY and comparing them to `display`, raising `CANONICAL_DISPLAY_MISMATCH` if there is a mismatch).
  - `it2` excludes canonical-display templates from the resolver, arguing that display canonicalization requires a separately adopted rendering contract rather than formatting code inside the runner's resolver.
  - **Ruling:** `it2`'s exclusion is correct. Under Article 11, the runner must remain thin and free of legal/policy logic. Embedding specific string-formatting templates for federal law citations inside the package resolver is a runner-resident policy. Formatting conventions (abbreviations, capitalization, punctuation) are presentation policy and should be governed by a rendering engine or a presentation contract, not hardcoded into the structural load-time resolver. Doing so creates runner-resident formatting policies that are not declared as content.
- **Verdict (it1):** Rejected (violates Article 11 by hardcoding presentation formatting templates inside the runner-resident resolver).
- **Verdict (it2):** Accepted

### CIT-G6: Verifiable Depth, Registry Definition, and False Confidence
- **Classification:** Decision-blocking
- **Evaluation:**
  - `it1` describes checking the citation details against "adopted registry presence" and rejects misses with `CLOSURE_MISSING_CITATION`.
  - `it2` explicitly limits the resolver's claim to "structural-and-adoption verifiability only". It rejects the idea of checking against an external corpus of federal law truth at load time, labeling the output as `statically_resolved` rather than `legal_verified` to prevent false confidence.
  - **Ruling:** `it2`'s boundary is correct. Evaluating the legal existence of a citation (e.g., verifying if a section actually exists in the federal code or if it is currently active) is an external corpus lookup that violates the static, self-contained runner posture. Claiming a citation is "legally verified" when only its package membership and schema structure have been checked creates false confidence. The resolver should perform package closure (ensuring that all referenced citation IDs resolve to citizens pinned within the package manifest), but must make no claim of legal verification.
- **Verdict (it1):** Rejected (implied external registry verification creates false confidence and exceeds static boundaries).
- **Verdict (it2):** Accepted

### CIT-G7: Authority Families Structure and Locator Discriminators
- **Classification:** Production-condition
- **Evaluation:**
  - `it1` proposes two authority families (`IRC` and `IRS_AUTHORITY`) and implements them via schema conditional `if/then` blocks.
  - `it2` proposes four authority families (`us-code`, `irs-form`, `irs-instructions`, `irs-publication`) and implements them via a strict discriminated `oneOf` locator structure, separating code references from different IRS document types.
  - **Ruling:** `it2`'s authority family structure and discriminated `oneOf` schema are superior. Treating form editions, instructions, and publications as distinct families rather than grouping them under a generic `IRS_AUTHORITY` string provides better schema-enforced validation and prevents spelling errors or document-type confusion. Furthermore, `it2`'s inclusion of a versioned `scope` block (`tax_year`, `jurisdiction`, `family`) in the citation citizen ensures consistency with ADR-0006/0027 package-level scope validation.
- **Verdict (it1):** Rejected (insufficient locator discrimination).
- **Verdict (it2):** Accepted

### CIT-G8: Contained Validation Compliance
- **Classification:** Non-blocking
- **Evaluation:** Both designs correctly implement contained validation as demanded by ADR-0006 decision 3. Citation defects are recorded as contained issues (`MemberIssue`) and do not crash the package loader, allowing the validator to capture all structural issues across the entire package.
- **Verdict (it1):** Accepted
- **Verdict (it2):** Accepted

---

## 3. Verdict Summary

| Proposition / Design | Incumbent (`it1/`) | Clean-Room Rival (`it2/`) |
| --- | --- | --- |
| **CIT-P1 (Citation Identity & Authority)** | **Rejected** (due to CIT-G4 multi-citation form-field and CIT-G7 locator group issues) | **Accepted** |
| **CIT-P2 (Resolver Contract & Integrity)** | **Rejected** (due to CIT-G5 display canonicalization and CIT-G6 verifiability overreach) | **Accepted** |

---

## 4. Carry-Forward Recommendation for Candidate ADR-0029

Ratify the clean-room rival (`it2/`) structural and adoption-only resolution model as the foundation for ADR-0029, incorporating a single exact `{id, version}` citation pin on `form-field.v2` presentation citizens, an array of unique exact citation pins on `rule-artifact.v2` computation citizens, and the four discriminated authority-family locator shapes (`us-code`, `irs-form`, `irs-instructions`, `irs-publication`), while explicitly excluding resolver-enforced display canonicalization and external legal-correctness registries in strict compliance with Article 11.
