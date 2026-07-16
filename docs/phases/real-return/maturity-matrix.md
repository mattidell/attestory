# Maturity Matrix

Audience: Product (planning instrument); Shared (status)

The milestone-selection instrument for the Real Return phase (and successors),
per the aspects × domain-coverage methodology agreed 2026-07-03. Rows are
**aspects** — capability dimensions the product must eventually have everywhere.
Columns are **domains** — regions of tax content coverage. Each cell holds a
maturity level. Milestone selection picks frontier cells; a milestone plan
names the cells it raises, and this file is updated at milestone close.

v1 is deliberately a hand-maintained markdown table. If cell claims start
drifting from reality, the recorded remedy is mechanization (single-source
data + renderer + freshness check, the artifact-graph pattern) — not more
careful hand-editing.

## Levels

| Level | Meaning |
| --- | --- |
| **L0** | Absent — no ratified contract, no implementation. |
| **L1** | Decided — contract ratified by ADR, implementation absent or partial. |
| **L2** | Synthetic — implemented and verified end-to-end on synthetic fixtures. |
| **L3** | Real — operates on the owner's actual data under the ratified data boundary. |
| **L4** | Hardened — named production conditions discharged; deferrals retired. |

## Matrix (as of 2026-07-15, post-Foundation)

| Aspect ↓ / Domain → | W-2 wages (1a) | Interest (2b) | Dividends (3a/3b) | Return-level conditions (status, 12, 15, 16) | Schedule attachments |
| --- | --- | --- | --- | --- | --- |
| **Admission & identity** (facts enter with declared identity, member transitions) | L2 | L2 | L0 | L2 | L0 |
| **Source closure & completeness** (families, mappings, horizons, honest blocking) | L1 ¹ | L2 | L0 | L2 ² | L0 |
| **Computation** (rules, composition, conditionals) | L2 | L2 ³ | L0 | L2 | L0 |
| **Adoption & authority** (packages, manifests, byte verification, citations) | L2 ⁴ | L2 ⁴ | L0 | L2 ⁴ | L0 |
| **Explanation & audit record** (provenance, disposition ledger, non-publication walk) | L2 | L2 | L0 | L2 | L0 |
| **Presentation** (form-field dispositions, rendering; human surface) | L2 ⁵ | L2 ⁵ | L0 | L2 ⁵ | L0 |
| **Correction & supersession lifecycle** | L2 ⁶ | L2 ⁶ | L0 | L2 ⁶ | L0 |
| **Data boundary** (real-data residency, contribution, privacy) | L0 | L0 | L0 | L0 | L0 |

Footnotes (honest qualifications, from the Foundation closing briefing):

1. The W-2 family has no closure mapping — an empty W-2 set blocks (honest,
   not deficient). Contract exists (ADR-0014); content absent.
2. Demographic inputs carry adopted defaults; filing status is a first-class
   categorical domain (ADR-0024/0025).
3. Named deferrals: further positive interest sources (K-1, market discount)
   and the subtractive-adjustment mechanism (nominee/accrued/premium)
   (ADR-0026).
4. Package resolution operates only inside the fixture boundary; a production
   resolver is deferred (ADR-0027). Byte verification of package instances and
   member citizens is in place.
5. E8.1 UI coverage deferred; citation *display* formatting is a deferred
   rendering contract. Presentation today is form-field disposition content,
   not a human surface.
6. Free supersession policy is a standing shim.

## Frontier reading

The computation/record aspects are uniformly L2 across covered domains; the
matrix is bottom-heavy. The three live frontiers, in the order the owner
prioritized (2026-07-15):

1. **Data boundary row: L0 → L3** across covered domains — the First Real
   Return Slice milestone. Raising this row also lifts every covered L2 cell
   to L3, because "operates on real data" is exactly what L3 means.
2. **Dividends / Schedule-attachments columns: L0 → L2** — coverage breadth
   (1099-DIV, lines 3a/3b, the Schedule B $1,500 conditional — the designated
   first hard trace case).
3. **Presentation aspect toward a human surface** — E8.1, citation display.
