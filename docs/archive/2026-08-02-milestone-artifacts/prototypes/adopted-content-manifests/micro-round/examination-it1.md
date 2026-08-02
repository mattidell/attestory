# Examination — ACM micro-round it1 (incumbent)

Date: 2026-07-15. Charter: `charter-it1.md`. Design: `it1/design.md`.
Evidence: Rung 2 paper + HEAD static probes (no repo edits beyond these two
outputs). Floor: ADR-0027 accepted (not re-litigated).

## Outcomes

| Proposition | Status |
| --- | --- |
| **MR-P1** | **Settled at static level.** Exact fact-surface membership needs `fact-type.v2` / `bundle.v2` (+ wholesale `act-bundle-adoption.v2`); dual pin unit (`fact-type-bundle` for vocabulary + exact fact `(id,version)` in joins); package↔adoption inclusion defeats pin/bundle drift. Does **not** pretend HEAD `*.v1` is version-pinnable. |
| **MR-P2** | **Settled at static level.** Package `composition_obligations` declares composition-governed symbols without requiring a composition citizen to exist first; validator rejects missing pin **and** missing citizen for listed symbols; structural multi-source fold forces declaration (bare sum cannot omit the list). No Article 11 symbol table; form-fields not obligation authority (ADR-0012). |

## MR-P1 contract (summary)

- Schema diffs: `fact-type.v2` + `version`; `bundle.v2` + versioned nested fact pins; adoption still wholesale but versioned; mapping.v2 exact fact pins.
- Pin unit: package member `fact-type-bundle`; bindings/mappings name exact fact identities in closed surface `F(P)`.
- Joins: binding ⊆ pinned bundle; package bundle pins ⊆ adopted set `A` with nested set equality (A7).
- HEAD probe: `fact-type.v1` / `bundle.v1` / committed W-2 bundle lack `version` — exact pins unresolvable until successors land.

## MR-P2 contract (summary)

- Declaration: `composition_obligations: [{symbol}]` on `artifact-package.v2` (content, not inferred from composition presence).
- Per listed symbol: producer integrity; required provenance-only `composition` pin; composition member with matching `publishes`; slot bijection when present.
- Structural completion: ≥2 distinct family-`authorizes_subtotal` inputs in one computation → `publishes` must be listed (else `COMPOSITION_OBLIGATION_UNDECLARED`).
- Out of floor: runner hardcoded symbols; form-field-as-authority; circular “if composition present then pin.”

## Required cases

| Case | Treatment | Result |
| --- | --- | --- |
| 1 Positive versioned surface | `U-wages@v1` pins bundle@v2 nesting fact-types@v2; bindings resolve into `F(P)` | validates |
| 2 Positive adoption inclusion | adopted act embeds same bundle@v2 body; package pin matches `A` | accepts |
| 3 Unversioned pin **(mandatory G1)** | HEAD has no version; exact pin vs `*.v1` rejected / inexpressible | reject |
| 4 Pin/bundle drift **(mandatory A7)** | bind X@v2 but adopted bundle omits X or has X@v1; or binding outside pinned bundles | reject drift codes |
| 5 Mapping fact gap (A4) | family/mapping/subtotal ok; mapping fact pins absent from `F(P)` | `MAPPING_FACT_UNPINNED` |
| 6 Positive composition unit | obligations list + citizen + pin + bijection + form-field | validates |
| 7 Bare sum **(mandatory A3)** | multi-family rule, no citizen, no pin; undeclared → obligation undeclared; declared → pin+member absent | reject (non-circular) |
| 8 Obligation without pin | list + citizen present; rule omits pin | `COMPOSITION_PIN_MISSING` |
| 9 Article 11 / presentation leak | symbol table in runner or form-field authority | out of floor / redesign |

## Claim → change → behavior (abbrev.)

| Claim | Change | Behavior |
| --- | --- | --- |
| Exact fact versions | `fact-type.v2` / `bundle.v2` | `(id,version)` resolve; v1 not pin-target |
| No adoption drift | inclusion joins + wholesale v2 acts | package surface = adopted vocabulary |
| Mapping facts closed | mapping.v2 pins ∈ `F(P)` | A4 reject |
| Non-circular obligation | package list + structural multi-source | case 7 reject without composition present |
| Provenance-only pin | ADR-0026/0027 held | pin required; no derivation edge |

## Unresolved (not fiat)

Exact issue-code strings; migration of committed v1 bundles; multi-package fact sharing; inbound reachability detail for nested facts (outbound + inclusion suffice for residual floor).

## Gate 6

Met: checkable fact-surface rule defeating cases 3–4 without HEAD pretence; non-circular composition obligation defeating case 7 without runner symbol special cases; case 5 closed with MR-P1 on paper.
