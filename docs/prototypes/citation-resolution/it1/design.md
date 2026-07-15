# Design: Citation Resolution (Iteration 1)

This document presents the Iteration 1 design for the Citation Resolution prototype (**Track 0.c**). It resolves **CIT-P1** (citation identity and authority model) and **CIT-P2** (resolver contract and load-time integrity) as settled-at-static-level. 

This design supersedes the inert, unratified **ADR-0018** prior art without inheriting its assumptions. It is grounded in the ratified project governance (Articles 9, 11, and 18) and the accepted constraints of ADR-0003, ADR-0006, ADR-0012, ADR-0027, and ADR-0028.

---

## 1. CIT-P1: Citation Identity and Authority Model

### 1.1 Citation as a First-Class Content Citizen
We reject nesting citation schemas directly inside form-field or rule schemas as inline, unversioned values. Doing so would violate **Article 9 (Canon)** and **Article 10 (Declaration)** by allowing unstructured drift of legal metadata, duplicate data across files, and complicating cross-citation references. 

Instead, a citation is a **first-class versioned content citizen** (`citation.v1` schema) stored under `packages/schemas/kernel/citation.v1.schema.json`. 
- **Opaque Identity:** Every citation citizen carries a unique, caller-supplied opaque ID (e.g. `cite.irc.26.61.a.4`) with no runtime-parsed semantics, satisfying **ADR-0003**.
- **Immutability and Versioning:** Published citation instances are immutable (**Article 9**). Updates to display format, spelling corrections, or page numbers are achieved by publishing a new version of the citizen (e.g., `v1` to `v2`) under the standard schema-version rules, preventing in-place mutations.

### 1.2 Schema and Authority Families
The `citation.v1` schema supports two primary authority families for federal tax rules:
1. **IRC (Internal Revenue Code):** Structured by Title, Section, Subsection, Paragraph, and Subparagraph.
2. **IRS_AUTHORITY (Form Instructions, Publications, Rev. Proc., Rev. Rul., Treas. Reg.):** Structured by Document Identifier (e.g., `"Form 1040 Instructions"`, `"Pub 550"`), Tax Year, Page, and Location/Line Identifier.

The JSON schema matches the structure verified in the scratch prototype:
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "kernel/citation.v1",
  "title": "Citation",
  "description": "A first-class versioned content citizen representing a legal authority reference.",
  "type": "object",
  "properties": {
    "schema": { "const": "citation.v1" },
    "id": { "type": "string", "pattern": "^[a-z][a-z0-9]*(\\.[a-z0-9-]+)+$" },
    "version": { "type": "string", "pattern": "^v[0-9]+$" },
    "authority": { "enum": ["IRC", "IRS_AUTHORITY"] },
    "details": { "type": "object" },
    "display": { "type": "string", "minLength": 1 }
  },
  "required": ["schema", "id", "version", "authority", "details", "display"],
  "allOf": [
    {
      "if": { "properties": { "authority": { "const": "IRC" } } },
      "then": {
        "properties": {
          "details": {
            "type": "object",
            "properties": {
              "title": { "type": "string", "pattern": "^[0-9]+$" },
              "section": { "type": "string", "pattern": "^[0-9]+[A-Z]?$" },
              "subsection": { "type": "string", "pattern": "^[a-z]$" },
              "paragraph": { "type": "string", "pattern": "^[0-9]+$" },
              "subparagraph": { "type": "string", "pattern": "^[A-Z]$" }
            },
            "required": ["title", "section"],
            "additionalProperties": false
          }
        }
      }
    },
    {
      "if": { "properties": { "authority": { "const": "IRS_AUTHORITY" } } },
      "then": {
        "properties": {
          "details": {
            "type": "object",
            "properties": {
              "doc_id": { "type": "string", "minLength": 1 },
              "tax_year": { "type": "integer" },
              "page": { "type": "integer", "minimum": 1 },
              "location_id": { "type": "string", "minLength": 1 }
            },
            "required": ["doc_id", "tax_year"],
            "additionalProperties": false
          }
        }
      }
    }
  ],
  "additionalProperties": false
}
```

### 1.3 Package Membership Integration
We do not invent a secondary membership authority. Citation citizens are package members. The package manifest schema `artifact-package.v2` (from **ADR-0027**) is extended to include `"citation"` in the enum of valid member pin roles:
```json
"role": {
  "enum": [
    "parameter",
    "computation",
    "applicability",
    "field-mapping",
    "cross-form-bridge",
    "form-field",
    "source-family",
    "source-closure-mapping",
    "composition",
    "citation"
  ]
}
```

### 1.4 Attachment Hooks
Citations attach to presentation and computation elements via explicit versioned references (pins) to citation citizens:
- **Form-Fields:** Redefine the inert `citation_ref` in `form-field.v1` to `citation_refs` in `form-field.v2`. It is an array of exact citation pins:
  ```json
  "citation_refs": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "version": { "type": "string", "pattern": "^v[0-9]+$" }
      },
      "required": ["id", "version"],
      "additionalProperties": false
    },
    "minItems": 1
  }
  ```
- **Rules:** The `rule-artifact.v2` schema introduces an optional `citation_refs` field of the identical pin-array shape. This supports tracing rule computation branches to legal authorities.

---

## 2. CIT-P2: Resolver Contract and Load-Time Integrity

### 2.1 Verifiable Resolution
A citation reference is "resolved" at load-time when:
1. **Structural Verification:** The referenced citation citizen is present as a pinned `"citation"` role member in the adopted package manifest, and it successfully validates against the `citation.v1` schema.
2. **Display Canonicalization:** The citation's `display` string matches the exact value generated deterministically by the resolver from `details`:
   - **IRC:** `f"IRC Sec. {section}"` with optional sub-parts appended as `({subsection})({paragraph})({subparagraph})`. E.g., `"IRC Sec. 61(a)(4)"`.
   - **IRS_AUTHORITY:** `f"{doc_id} ({tax_year})"` with optional additions `f", p. {page}"` and `f", {location_id}"`. E.g., `"Form 1040 Instructions (2025), p. 16, Line 2b"`.

If the display string differs by a single character (e.g. `IRC 61a4`), the package loader flags it. This checks abbreviations and prevents user-visible spelling inconsistencies.

### 2.2 Contained Validation Failures
To comply with **ADR-0006 decision 3**, citation resolution failures never abort package loading. The validator records defects as `MemberIssue` objects and returns them within `PackageValidation`.

### 2.3 Exclusions and Boundaries (Article 11)
To protect **Article 11 (Legibility)** and the thin engine posture, the following items are strictly **out of scope** for the resolver:
- **Live network fetching:** The runner never calls external services (e.g., Cornell LII or IRS PDFs) to verify legal documents. All checks are self-contained.
- **Legal Correctness:** The resolver does not evaluate whether a citation is legally applicable or active for a taxpayer's situation. Legal logic remains pure rule evaluation (**Article 11**).
- **Multi-Jurisdiction Ingestion:** State-level or international tax authorities are excluded, though the `IRS_AUTHORITY` string structures act as clean extension hooks if needed.

---

## 3. Conformance to Gate-2 Test Cases

### Case 1: Positive — field with structured cite
A form-field (e.g., line 2b) pins `cite.irc.26.61.a.4@v1` and `cite.irs.1040-inst.2025.p16.line-2b@v1`. Both citations are present as package members of role `citation`. Validation passes.

### Case 2: Positive — rule-attached cite
A rule computing taxable interest carries a `citation_refs` pin to `cite.irc.26.61.a.4@v1`. The citation is a pinned package member. Validation passes.

### Case 3: Negative — opaque string residual
A form-field uses a legacy string citation `"IRC Sec. 61"` in place of the structured pin object. Schema validation fails on `form-field.v2` with `MEMBER_SCHEMA_INVALID`.

### Case 4: Negative — malformed / incomplete structure
A citation `cite.irc.malformed@v1` has a detail block missing `title` or `section`, or its display string is `"IRC 61a4"` instead of `"IRC Sec. 61(a)(4)"`. Loader registers a contained `CANONICAL_DISPLAY_MISMATCH` or `MEMBER_SCHEMA_INVALID` issue.

### Case 5: Negative — unresolved registry miss (Package Closure)
A form-field references a citation ID/version not pinned as a member in the package manifest. The package validator rejects with `CLOSURE_MISSING_CITATION`.

### Case 6: Negative — Article 11 / overreach
The loader executes code attempting to verify if the citation's section is active for the taxpayer's income facts. This is out of the runner's floor and is rejected.

### Case 7: Lifecycle (Immutability)
If a typo is found in `cite.irc.26.61.a.4@v1`'s display string, the builder must not edit it in-place. The publication registry checksum comparison rejects the package as a rewrite of version `v1` (violating **Article 9**). Instead, `cite.irc.26.61.a.4@v2` is published, and the form-field updates its pin to `v2`.
