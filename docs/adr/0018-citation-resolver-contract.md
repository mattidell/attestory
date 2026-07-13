# ADR 0018 — Citation Resolver Contract and Semantic Pins

- Status: proposed
- Tier: 2
- Date: 2026-07-13

## Context

ADR-0012 established form-field citizens and their rendered dispositions, but left citation references as inert opaque strings (e.g. `"IRC Sec. 61"`). Opaque strings cannot be validated, verified, or traversed by automated tools. To ensure all tax calculations cite real, verifiable legal authorities, we need a semantic citation resolver contract that models legal and form authority structure.

## Decision

1. **Structured Citation Schema:** Citation references on form-field citizens and rules must conform to the structured citation JSON Schema. We define two primary authorities:
   - `IRC` (Internal Revenue Code): structured by Title, Section, Subsection, and Paragraph.
   - `IRS_AUTHORITY` (Form Instructions, Publications, Rev. Proc.): structured by Form/Publication identifier, Tax Year, Page, and Section/Line identifier.

2. **Semantic Citation Format:**
   An IRC citation instance:
   ```json
   {
     "authority": "IRC",
     "title": "26",
     "section": "61",
     "subsection": "a",
     "paragraph": "4",
     "display": "IRC Sec. 61(a)(4)"
   }
   ```
   An IRS Authority citation instance:
   ```json
   {
     "authority": "IRS_AUTHORITY",
     "document": "Form 1040 Instructions",
     "year": 2025,
     "page": 16,
     "line": "2b",
     "display": "Form 1040 Instructions (2025), p. 16, Line 2b"
   }
   ```

3. **Resolver Validation:** The package loader resolves and validates all structured citations. It checks that:
   - The citation structure matches its authority schema.
   - The citation's `display` string matches a canonical computed format, preventing inconsistent abbreviations.

## Consequences

- citation references on form fields become structured and machine-readable.
- Discrepancies, typos, or dead links in legal citations can be caught statically during package loading.
- Presentation layers can parse the structured citations to link directly to official Cornell LII or IRS PDF pages.
