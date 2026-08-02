# Evaluation Analysis — D3 Production Package Resolver

Date: 2026-07-17. Topic: First Real Return Slice, Track 0 D3. Tier 2
production-resolution contract. Status: **evidence converged; ADR-0033
recommended.**

## Question

Can an adopted rule package resolve from live residency `L` without weakening
ADR-0027's exclusive execution projection or ADR-0028's byte verification, and
can its D3-P2 ledger account for every named production condition without
claiming D1/D2 installation?

## Evidence and conclusions

| Proposition | Evidence | Conclusion |
|---|---|---|
| D3-P1 — trusted production resolution | Incumbent `it5/design.md` §§1–3 and examination probes 1–16; sealed rival `it6/design.md` §1 and P1–P12; Round-3 Governance Measures 1–3/5; Round-3 Adversary A1–A4 | Converged at Rung 2. A current user adoption selects a pinned release; release bytes authenticate registry bytes before registry entries authenticate the package and members; pin-directed verified supply then requires `validation.ok == True` before the exclusive graph exists. |
| D3-P2 — exhaustive discharge/defer ledger | `it5/design.md` §4; `it6/design.md` §2; both examinations' completeness probes; Round-3 Governance Measure 4; Round-3 Adversary A5 | Converged at Rung 2. Every ADR-0027/0028 item has an explicit permitted disposition; ADR-0031/0032 remain consumed production conditions and embedded schema-byte checksums remain rejected. |

### D3-P1 measured cases

1. **Release-byte authority.** Both builds reject a forged release/registry
before any entry authenticates supply. The adversary could not make a
caller-selected registry or `L` catalog authorize forged synthetic bytes
([Governance Measure 1](reviews/governance-r3.md),
[Adversary A1](reviews/adversary-r3.md)).
2. **Current user adoption.** Both reject caller metadata, non-user acts, stale
acts, and ambiguous tips; selection is derived from scope, revision, and
supersession ([Governance Measure 2](reviews/governance-r3.md),
[Adversary A2](reviews/adversary-r3.md)).
3. **Exclusive, order-independent supply.** Unpinned files never enter the
member graph, missing pins fail closed, and same-key evidence cannot become a
filesystem-order choice ([Governance Measure 3](reviews/governance-r3.md),
[Adversary A3](reviews/adversary-r3.md)).
4. **Hard gate.** A clean synthetic package passes `ok == True`; the committed
core package reports exactly eight issues and is refused. No reviewer found a
conformant leniency path ([Governance Measure 5](reviews/governance-r3.md),
[Adversary A4](reviews/adversary-r3.md)).

### Chosen contract basis

ADR-0033 adopts the sealed rival's `it6` authority chain because it separately
pins and verifies release-citizen bytes and registry-document bytes, and its
ledger keeps fixture-contract obligations as owning-track production conditions.
This is a selection among builder-designed, committee-confirmed mechanisms, not
a foreman-authored repair. The incumbent is independent corroboration: its
different tip-set and digest-set mechanisms passed the same charter.

The chosen same-key rule admits only candidate bytes matching the verified
expected digest; zero matches rejects and identical matching duplicates collapse.
It is order-independent and cannot admit an evil same-key body. A stricter
"any distinct digest refuses" policy remains an implementation choice, not a
contract requirement.

## Conditions carried to implementation

- The production resolver, release/adoption schemas, and refusal/golden suites
  are Track-3 work; this paper decision installs none of them.
- ADR-0031's residency wall and ADR-0032's marshal-only live-entrypoint proof
  are consumed interlocks and remain their owning Tracks 1–3 conditions.
- **RG-1** is a MUST before a live package may pass the production gate: repair
  four `MEMBER_UNREACHABLE` defects and the v1-generation debt represented by
  `SCHEMA_NOT_ADMITTED`, `ROLE_MISMATCH`, and two mapping-fact-surface issues.
  The gate itself remains `validation.ok == True`; no allowlist is permitted.

## Dissent and residuals

No committee finding remains decision-blocking. The reviewers noted only a
non-blocking choice: incumbent refusal of any same-key distinct-byte set is
stricter than rival filtering to the verified expected digest. Both prevent
order-based impostor admission; the ADR adopts the rival's explicit
verified-candidate rule. Publication root physical layout, schema installation,
and exact error-code strings are production implementation details subject to
the stated contract and existing registry rules.

## Process and data safety

Three paired build iterations were necessary because Iterations 1 and 2 exposed
new authority questions rather than resolving none. Iteration 3's confirmation
round answered all four pre-declared blockers. The topic exceeded its original
Markdown target under owner-directed variance; the evidence cap model is a
separate process follow-up. All committed evidence uses synthetic packages,
acts, identifiers, and scratch-`L` probes; no personal workspace, values, or
locator appears.

## Traceability

- Builder custody: `1462ddf` — `it5/`, `it6/`, examinations, and seal.
- Round-3 charters: `f160959` — confirmation-only measurements.
- Committee custody: `e596b6e` — `reviews/governance-r3.md` and
  `reviews/adversary-r3.md`.
- Prior blockers: `reviews/governance-r2.md` and `reviews/adversary-r2.md`.
- Contracts: ADR-0027 Decisions 1, 6, 7 and PC1–PC4; ADR-0028 Decisions 1–9
  and PC1/PC1b/PC1c/PC2/PC3; ADR-0031; ADR-0032; Constitution Articles 4, 9,
  11, 18; Ontology §§1, 4, 8.
