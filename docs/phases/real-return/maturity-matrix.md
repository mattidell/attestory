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

## Matrix (as of 2026-07-21, post-Dividends-and-Schedule-B-Slice)

| Aspect ↓ / Domain → | W-2 wages (1a) | Interest (2b) | Dividends (3a/3b) | Return-level conditions (status, 12, 15, 16) | Schedule attachments |
| --- | --- | --- | --- | --- | --- |
| **Admission & identity** (facts enter with declared identity, member transitions) | L3 ⁷ | L3 ⁷ | L3 ⁹ ¹¹ | L3 ⁷ | L3 ¹¹ ¹² |
| **Source closure & completeness** (families, mappings, horizons, honest blocking) | L3 ¹ ⁷ | L3 ⁷ | L3 ⁹ ¹¹ | L3 ² ⁷ | L3 ¹¹ ¹² |
| **Computation** (rules, composition, conditionals) | L3 ⁷ | L3 ³ ⁷ | L3 ¹¹ | L3 ⁷ | L3 ¹¹ ¹² |
| **Adoption & authority** (packages, manifests, byte verification, citations) | L3 ⁴ ⁷ | L3 ⁴ ⁷ | L3 ¹¹ | L3 ⁴ ⁷ | L3 ¹¹ ¹² |
| **Explanation & audit record** (provenance, disposition ledger, non-publication walk) | L3 ⁷ | L3 ⁷ | L3 ¹¹ | L3 ⁷ | L3 ¹¹ ¹² |
| **Presentation** (form-field dispositions, rendering; human surface) | L3 ⁵ ⁷ | L3 ⁵ ⁷ | L3 ⁵ ¹¹ | L3 ⁵ ⁷ | L3 ⁵ ¹¹ |
| **Correction & supersession lifecycle** | L3 ⁶ ⁷ | L3 ⁶ ⁷ | L3 ⁶ ¹¹ | L3 ⁶ ⁷ | L3 ⁶ ¹¹ |
| **Data boundary** (real-data residency, contribution, privacy) | L3 ⁷ ⁸ | L3 ⁷ ⁸ | L3 ⁸ ¹⁰ ¹¹ | L3 ⁷ ⁸ | L3 ⁸ ¹⁰ ¹¹ |

Footnotes (honest qualifications; renumbered at milestone close 2026-07-18,
extended at milestone close 2026-07-21):

1. The W-2 family's closure mapping now exists as immutable horizon-keyed v3
   content (Tracks 4/4c, ADR-0014 pattern); a stale closure is a hard
   projection error, and an empty declared set can close honestly.
2. Demographic inputs carry adopted defaults; filing status is a first-class
   categorical domain (ADR-0024/0025).
3. Named deferrals: further positive interest sources (K-1, market discount)
   and the subtractive-adjustment mechanism (nominee/accrued/premium)
   (ADR-0026). See the milestone deferral ledger.
4. The production package resolver operates outside the fixture boundary
   (ADR-0033, Track 3): current-user adoption pins a verified release; bytes
   are registry-verified before a strict `validation.ok == True` exclusive
   graph resolves. ADR-0028 historical-v1 migration remains deferred.
5. E8.1 UI coverage deferred; citation *display* formatting is a deferred
   rendering contract. Presentation today is form-field disposition content,
   not a human surface.
6. Free supersession policy is a standing shim.
7. **Evidential basis for every L3 claim (Ontology §8):** the synthetic
   battery exercises the identical path end-to-end in-repo, and the owner's
   non-descriptive attestation (milestone plan, Verification, 2026-07-18)
   establishes that the slice ran on real data in quarantine with the
   boundary intact. No L3 claim rests on — or may ever cite — quarantined
   run detail. L3 asserts the *capability operated*, not any particular
   disposition.
8. ADR-0031/0032/0033 ratified and implemented: out-of-repo residency with
   installed byte-verified envelope gates (Track 4b), contribution as a
   first-class event, fail-closed classification. Guarded transport /
   credential confinement is a named deferral (ledger), which is what holds
   this row (and the matrix) short of L4.
9. **Declared dividend universe is boxes 1a/1b only** (ADR-0035, D3;
   milestone plan, owner-ratified at plan stage): boxes 2a, 3, 5, 7, and 12
   are named honest-block exclusions, not silently dropped — deferral ledger
   entry 4. Admission-locus 1b ≤ 1a rejection and 3a ≤ 3b hold by
   construction within the declared universe.
10. Dividends and Schedule attachments share the same data-boundary infra as
    W-2/interest (footnote 8) — no new boundary contract was introduced; the
    owner's real 1099-DIV facts entered the same quarantined workspace and
    contribution boundary.
11. **Evidential basis for Dividends/Schedule-attachments L3 claims
    (Ontology §8):** the DSBS synthetic battery drives the full widened
    slice from the authoritative surface through the named golden classes
    (3a/3b publication, line 9 with dividends, Schedule B not-required /
    required-and-complete / required-and-incomplete, line 16 under D2's
    ratified shape — `docs/reviews/2026-07-19-dsbs-t2-*`,
    `docs/reviews/2026-07-20-dsbs-t3-*`, `docs/reviews/2026-07-20-dsbs-t4-*`),
    and the owner's non-descriptive attestation (milestone plan,
    Verification, "Owner attestation", 2026-07-21) establishes the slice ran
    on real 1099-DIV data in quarantine with the boundary intact. Same
    posture as footnote 7: no L3 claim here rests on, or may ever cite,
    quarantined run detail — L3 asserts the capability operated, not any
    particular disposition.
12. **Schedule B is the only implemented schedule attachment.** The
    attachment ontology (ADR-0036) is demonstrated generically — a Schedule D
    stub in the D1 prototype exercised the same citizen/states/completeness
    shape with zero Schedule-B-specific surface — but no other actual
    schedule has production content yet. L3 here reflects the capability
    operating for Schedule B specifically, not universal schedule coverage;
    the Schedule-attachments column's L3 is scoped to the aspects Schedule B
    exercises (all eight rows), per the milestone plan's exit criterion 6.

## Frontier reading

The covered region (all five domains, all eight aspects) is now uniformly
L3; the matrix is breadth- and hardening-limited, not depth-limited within
its covered domains. The live frontiers for the owner's next selection
(Tier 3):

1. **Presentation aspect toward a human surface** — E8.1, citation display.
   The first aspect a real user (the owner) now touches every run, across
   every domain the matrix covers.
2. **L3 → L4 hardening** — retire named deferrals from the milestone ledger
   (`dividends-schedule-b-slice-deferral-ledger.md`): guarded transport
   still first (holds the data-boundary row at L3 across every domain);
   then supersession policy, ADR-0026 interest scope, ADR-0028 migration,
   the marshaller binding-route simplification, and the newer Track 4 F2
   scaffold-visibility note.
3. **New domain breadth** — dividend boxes outside the declared universe
   (2a/3/5/7/12; deferral ledger entry 4), a second schedule attachment
   beyond Schedule B (the D1 ontology's Schedule D stub is evidence this is
   now a content question, not a design question), or a second
   income/return-level domain not yet on the matrix's columns at all.
