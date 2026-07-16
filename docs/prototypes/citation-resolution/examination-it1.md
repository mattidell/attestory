# Examination: Citation Resolution (Iteration 1)

Date: 2026-07-15.
Milestone: Core Tax Conditions remediation, Track 0.c.
Evaluator: Owner-launched High-tier incumbent builder.

## 1. Prototype Status

- **CIT-P1 (Citation Identity and Authority Model):** **settled-at-static-level**.
- **CIT-P2 (Resolver Contract and Load-Time Integrity):** **settled-at-static-level**.

---

## 2. Gate-2 Cases Verification

### Case 1: Positive — field with structured cite
- **Claim:** A form-field carries a structured citation reference.
- **Contract/Schema:** `form-field.v2` defines `citation_refs` as an array of exact citizen pins `{id, version}`. Pinned member `cite.irc.26.61.a.4` validates against `citation.v1`.
- **Behavior:** Pinned member resolves, validates against its schema, and its canonical display matches its display value. Accepted.
- **Trace:** `tax.form-1040.line-2b@v1` → `cite.irc.26.61.a.4@v1` → Resolver checks display → Accepted.

### Case 2: Positive — rule-attached cite
- **Claim:** A rule carries a structured citation reference.
- **Contract/Schema:** `rule-artifact.v2` includes optional `citation_refs` matching `form-field.v2` pin shape.
- **Behavior:** The rule pins `cite.irc.26.61.a.4@v1`. The citation is loaded and resolved from the package. Validated and accepted.
- **Justification:** Essential for auditing intermediate rule computations against tax code without relying solely on presentation layers.

### Case 3: Negative — opaque string residual (Mandatory)
- **Claim:** A form-field or rule with legacy opaque string citation is rejected.
- **Contract/Schema:** `form-field.v2` and `rule-artifact.v2` schemas require the structured pin object.
- **Behavior:** An instance containing `"citation_ref": "IRC Sec. 61"` fails JSON schema validation.
- **Issue Code:** `MEMBER_SCHEMA_INVALID` with detail code `PACKAGE_SCHEMA_INVALID`. Rejected.

### Case 4: Negative — malformed / incomplete structure (Mandatory)
- **Claim:** Citations with missing fields or display string mismatches are rejected.
- **Contract/Schema:** `citation.v1` requires `details.title` and `details.section` (under `IRC`).
- **Behavior:**
  - Missing title: Fails JSON Schema. Issue `MEMBER_SCHEMA_INVALID`.
  - Display mismatch: A citation with section `"61"` and display `"IRC 61a4"` fails display check.
- **Issue Code:** `CANONICAL_DISPLAY_MISMATCH` (mismatch of `"IRC Sec. 61(a)(4)"` vs `"IRC 61a4"`). Rejected.

### Case 5: Negative — unresolved registry miss (Package Closure)
- **Claim:** Referenced citation not in the package is rejected.
- **Contract/Schema:** Package graph closure requires all referenced citizens to be members of `artifact-package.v2`.
- **Behavior:** A field references `cite.irc.26.61.a.4@v1` but it is not pinned in package `members` under `citation` role.
- **Issue Code:** `CLOSURE_MISSING_CITATION` (similar to `CLOSURE_MISSING_PARAMETER`). Rejected.

### Case 6: Negative — Article 11 / overreach
- **Claim:** Resolver does not evaluate legal holdings or taxpayer facts.
- **Contract/Schema:** Thin engine contract. Resolver does not contain or run legal applicability tests.
- **Behavior:** Validates structure and display syntax only. If any code attempts to evaluate legal holdings in the runner, it is out of floor and rejected. Validated offline.

### Case 7: Lifecycle / Immutability (Mandatory)
- **Claim:** In-place updates to published citation citizens reject.
- **Contract/Schema:** Article 9 (Canon) immutability.
- **Behavior:**
  - Citation `cite.irc.26.61.a.4@v1` has a display typo.
  - Attempting to correct the typo in-place changes its file checksum, failing package-checksum validation.
  - Correct path: Publish `cite.irc.26.61.a.4@v2` as a new immutable citizen, and update form-field pin to `v2`.
- **Issue Code:** `PACKAGE_INSTANCE_REWRITE_REJECT`. Rejected.
