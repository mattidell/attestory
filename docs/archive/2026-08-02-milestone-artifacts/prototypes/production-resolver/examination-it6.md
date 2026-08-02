# Examination — D3 Iteration-3 Clean-Room Rival (`it6`)

Date: 2026-07-16. Seat: clean-room rival, High. Rung 2. Synthetic only.
Companion: `it6/design.md`. **Seal:** held from incumbent until foreman custody.

## Read surface (clean-room)

Read: `SEAT.md`, `plan.md`, `process-log.md`, Iteration-2 reviews, ADR-0027/0028/
0031/0032/0034, Ontology §1/§4, committed `package_validation` /
`load_published_*` / `verify_published_package` / `validate_package`, tax 2025
registry and packages. **Not read:** `it5/`, `examination-it5.md`, incumbent
designs.

## Probe method

Throwaway scratch-`L` under system temp (out-of-repo). Paper selection/release
gates executed as pure functions over synthetic acts and digests; integrity and
validation called on committed surfaces read-only. No production code edited.

## Probe results

| Id | Case | Observed |
| --- | --- | --- |
| P1 | Release-byte replacement | `RELEASE_BYTE_MISMATCH` — forged release digest ≠ adoption pin |
| P2 | Registry forgery under honest release | `REGISTRY_BYTE_MISMATCH` — registry SHA ≠ `registry_sha256` |
| P3 | Package entry rewrite | `PACKAGE_VERSION_REWRITE` via `verify_published_package` |
| P4 | Current-user adoption (5 shuffles) | always `act-A-user-current`; automation ineligible |
| P5 | Stale vs current / non-user | current wins when present; non-user alone → `NO_CURRENT_USER_ADOPTION` |
| P6 | Same-key honest+evil, both orders | admits only registry checksum match |
| P7 | Evil-only same key | `MISSING_PINNED_BYTES` |
| P8 | Unpinned co-located `demo.evil` | not in graph (19/19 pins only) |
| P9 | Missing pinned member | refuse; no partial graph |
| P10 | Reversed member enumeration | identical graph id-set |
| P11 | Clean success (interest-slice) | `validation.ok is True`, n_issues=0, full chain admits |
| P12 | Eight-issue refusal (core-calculations) | `ok is False`, **exactly 8** issues; gate blocks graph |
| P13 | Ledger completeness | every ADR-0027 D1–D7/PC1–PC4 and ADR-0028 D1–D9/PC1/PC1b/PC1c/PC2/PC3 has one disposition in design §2 |

**P12 issue codes (committed measurement):** SCHEMA_NOT_ADMITTED, ROLE_MISMATCH,
MAPPING_FACT_TYPE_NOT_ADMITTED ×2, MEMBER_UNREACHABLE ×4.

**ok == True preserved:** P11 requires true; P12 and all integrity failures refuse
before graph/execution/rendering. No allowlist of the eight issues.

## Claim → evidence

| Claim | Evidence |
| --- | --- |
| Publication authority is release-byte verified before registry use | P1, P2; design §1.1 |
| Registry/catalog forgery cannot authenticate evil supply under pinned release | P1, P2; forged catalog blocked at release |
| Entry mismatch/rewrite fails closed | P3 |
| Adoption is current user act; caller cannot select authority | P4, P5; design §1.2 |
| Same-key refusal is order-independent | P6, P7, P10 |
| Unpinned inert; missing pin non-partial | P8, P9 |
| Strict clean success / eight-issue refusal | P11, P12 |
| D3-P2 exhaustive, no D1/D2 false discharge | P13; design §2.3 |
| RG-1 MUST prerequisite | design §1.5; eight issues named as reachability + v1-generation debt |

## Disposition summary

- **D3-P1:** independent contract proposed — release root → verified registry →
  package/member pins → `ok == True` → exclusive graph. Survives P1–P12 at Rung 2
  paper/probe depth. Not installed.
- **D3-P2:** item-by-item ledger present; CS vs PC(T) vs DEF vs N/A distinguished;
  ADR-0031/0032 consumed interlocks; embedded schema checksums N/A rejected.
- **RG-1:** carried as validator-reachability and v1-generation MUST prerequisite;
  not discharged.

## Stop / seal

No implementation, schemas, commits, or incumbent review. Stop at Rung-2 paper
boundary. Escalation: weaken all-or-nothing validation, or reassign registry/act
selection to the caller.

**SEAL** — `examination-it6.md` sealed with `it6/design.md` for foreman custody.
