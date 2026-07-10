# Governance

This directory holds the project's governance set: the versioned artifacts that carry all contract authority for this repository. Development agents treat these documents as the source of truth for what the system is and what implementations may do. The set was ratified by the user and stamped v0.1 on 2026-07-09.

## The set

| Artifact | File | Role |
|---|---|---|
| Constitution | `constitution.md` | Norms. Nineteen articles; each states a norm, its foreclosures, and an aphorism. |
| Ontology | `ontology.md` | Meaning. Defines every term the Constitution uses; defines and never commands. Ends with the register the closure check reads mechanically. |
| Engineering Constraints | `engineering-constraints.md` | Implementation patterns. Entries keyed to articles; each states the foreclosed pattern, the permitted alternative, and a detection. The detections are the conformance suite's specification. |
| Principles | `principles.md` | The generative layer. Fifteen convictions with arguments; articles cite principles as parentage. |
| Commentary | `commentary.md` | Interpretation. Per-article notes and standing essays; interprets, never amends; expandable by accretion. |

## Authority order

1. The **Constitution** norms; the **Ontology** defines. Conflicts between them are defects requiring versioned correction (Constitution, governance note).
2. The **Engineering Constraints** are subordinate to both; they bind implementations.
3. Where the Constitution and Ontology are silent, the **Principles** interpret first (Principles preamble).
4. The **Commentary** carries the lowest normative authority; it interprets and never amends.

## Versioning

Every artifact carries a version header (artifact, version, status, date). Published versions are immutable — change means a new version, per Article 9 as applied to the governance documents themselves (governance note). Process records pin the governance versions they operated under (Article 14).

## Version log

- **v0.1** (2026-07-09) — Initial ratified set. The two closure-check defects were closed with user-ratified wording (Revision entry; Article 14 citation and governance note). See `records/2026-07-09-closure-check-v0.1.md` and ADR-0001.

## Records

`records/` holds governance process records — closure checks and future conformance audits. The v0.1 closure check's debt register (six review-dependent detections: E1.1, E7.2, E10.1, E11.3, E17.1, E18.3) and open-work list (T1 derived-finding authority; T2 stance/position; redaction detail; multi-party authority; canonical reference names; consent-mechanism design; claim-sameness rule scope) are the standing conformance backlog.

## Conformance

`tools/governance_lint.py` checks the structural integrity of this set (version headers, article count, citation resolution, constitutional term resolution against the register, article–principle parentage, no unpromoted intake drafts). Run it with the test suite before committing changes that touch governance or contracts.
