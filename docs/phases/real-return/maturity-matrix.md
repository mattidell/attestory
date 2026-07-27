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

## Matrix (as of 2026-07-26, Presentation Live Viewing Boundary records)

| Aspect ↓ / Domain → | W-2 wages (1a) | Interest (2b) | Dividends (3a/3b) | Return-level conditions (status, 12, 15, 16) | Schedule attachments |
| --- | --- | --- | --- | --- | --- |
| **Admission & identity** (facts enter with declared identity, member transitions) | L3 ⁷ | L3 ⁷ | L3 ⁹ ¹¹ | L3 ⁷ | L3 ¹¹ ¹² |
| **Source closure & completeness** (families, mappings, horizons, honest blocking) | L3 ¹ ⁷ | L3 ⁷ | L3 ⁹ ¹¹ | L3 ² ⁷ | L3 ¹¹ ¹² |
| **Computation** (rules, composition, conditionals) | L3 ⁷ | L3 ³ ⁷ | L3 ¹¹ | L3 ⁷ | L3 ¹¹ ¹² |
| **Adoption & authority** (packages, manifests, byte verification, citations) | L3 ⁴ ⁷ | L3 ⁴ ⁷ | L3 ¹¹ | L3 ⁴ ⁷ | L3 ¹¹ ¹² |
| **Explanation & audit record** (provenance, disposition ledger, non-publication walk) | L3 ⁷ | L3 ⁷ | L3 ¹¹ | L3 ⁷ | L3 ¹¹ ¹² |
| **Presentation** (form-field dispositions, rendering; human surface) | L2 ⁵ ⁷ | L2 ⁵ ⁷ | L2 ⁵ ¹¹ | L2 ⁵ ⁷ | L2 ⁵ ¹¹ |
| **Correction & supersession lifecycle** | L4 ⁶ ⁷ | L4 ⁶ ⁷ | L4 ⁶ ¹¹ | L4 ⁶ ⁷ | L4 ⁶ ¹¹ |
| **Data boundary** (real-data residency, contribution, privacy) | L3 ⁷ ⁸ ¹³ | L3 ⁷ ⁸ ¹³ | L3 ⁸ ¹⁰ ¹¹ ¹³ | L3 ⁷ ⁸ ¹³ | L3 ⁸ ¹⁰ ¹¹ ¹³ |

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
5. **Presentation remains L2 after L2 Integration Grounding.** Presentation —
   Citation Walk on Real Derivation Output moved the row from an overstated L3
   to L2 and supplied the ADR-0046 renderer. L2 Integration Grounding then
   closed the coordinator-to-model gap on production-shaped synthetic data:
   `live_coordinate_run` now derives a strictly validated internal model from
   the resolved graph, projected record state, publications, and dispositions,
   and writes it below `LiveWorkspace`. Independent review returned `NOT READY`
   on one coordinator-level projector-failure cleanup gap; the one repair
   closed it and focused recheck returned `READY`. The browser harness remains
   deliberately synthetic-only and no real operation occurred, so none of this
   raises Presentation to L3. The table below is the durable handoff.

   **Live Viewing Boundary and Invocation Vehicle (2026-07-26)** then closed the
   vehicle gap without lifting the row. Its first act was to reject its own
   obvious shape: a milestone chartered to build flag-confined browser
   containment would have failed on inspection, because Chrome's
   `--disable-background-networking`-style flags are cooperative settings inside
   a same-UID process and ADR-0044 already forecloses that as a trust boundary.
   The milestone instead defined the environment first (ADR-0047), then built
   only what the classification calls controllable by construction: destinations
   confined to the live workspace, canonicalized against symlink escape, and a
   fail-closed preflight that returns reason codes and cannot emit the residency
   locator on any surface. No real workspace was touched, no viewing session
   performed, and no attestation made, so the row stays at L2.

   | Presentation capability | Current state | Evidence |
   | --- | --- | --- |
   | Surface contract | ADR-0046 accepted; no contract change in this milestone | `docs/adr/0046-presentation-surface-contract.md` |
   | Renderer behavior | Independently verified over the full five-disposition and T1–T3/F1–F2 synthetic regression matrix | `tools/presentation_harness/examples/manifests/citation-walk.v1.json`; `docs/reviews/2026-07-26-presentation-citation-walk-track1-repair-review.md` |
   | Coordinator projection | Production-shaped synthetic `live_coordinate_run` verified; every resolved field/attachment joins from coordinator-owned inputs | `tests/test_presentation_l2_integration.py`; `docs/reviews/2026-07-26-presentation-l2-integration-grounding-track1-review.md`; `docs/reviews/2026-07-26-presentation-l2-integration-grounding-track1-recheck.md` |
   | Renderer input | Internal `presentation-model.v1`, strictly validated and regenerated byte-for-byte | `packages/derivation/presentation_projection.py`; `tools/presentation_harness/examples/pages/citation-walk-fixtures/production-shaped.v1.json` |
   | Browser path | Evaluation harness: two synthetic manifests only, deliberately synthetic-bounded. Live viewing: a confined headed invocation vehicle now exists and is synthetic-tested; it has never been invoked against a real workspace | `tools/presentation_harness/examples/manifests/citation-walk.v1.json`; `tools/presentation_harness/examples/manifests/citation-walk-production-shaped.v1.json`; `packages/derivation/live_viewing.py`; `tests/test_presentation_live_viewing_vehicle.py` |
   | Live viewing environment | Decided. ADR-0047 classifies every headed-browser channel into four classes, states exactly what the owner would attest, and names the enforcement-substrate residual | `docs/adr/0047-live-viewing-environment.md` |
| Real operation | Not exercised; no viewing session performed and no owner attestation made. This, not the vehicle, is now the whole remaining distance to L3 | Presentation remains L2 |
6. **Correction-authority policy retired 2026-07-22** (Correction Authority
   and Marshaller Simplification milestone; ADR-0041, Track 1, PR #53): the
   supersession-policy vocabulary is no longer an unrestricted no-op — it
   closes to `free`/`locked`/`closed-on-attestation`, enforced at the
   existing dispatch site in `packages/kernel/findings.py`. Every existing
   fact type still declares `free`, unaffected — ADR-0041 compels no
   migration — so this row moves to L4 because the named production
   condition ("any actor supersedes any finding without restriction") is
   discharged, not because any existing content's behavior changed. Ships
   as new `fact-type.v3`/`bundle.v3` schema versions; `v1`/`v2` of each stay
   byte-for-byte untouched (ADR-0003/Canon Article 9 immutability).
   `closed-on-attestation` is scoped to fact types sharing identity-key
   names with their gate/closure fact type (family-level elections); it
   does not yet reach differently-keyed per-item facts — named as a new
   deferral, not a defect (see the milestone's deferral ledger).
7. **Evidential basis for every L3 claim (Ontology §8):** the synthetic
   battery exercises the identical path end-to-end in-repo, and the owner's
   non-descriptive attestation (milestone plan, Verification, 2026-07-18)
   establishes that the slice ran on real data in quarantine with the
   boundary intact. No L3 claim rests on — or may ever cite — quarantined
   run detail. L3 asserts the *capability operated*, not any particular
   disposition.
8. ADR-0031/0032/0033 ratified and implemented: out-of-repo residency with
   installed byte-verified envelope gates (Track 4b), contribution as a
   first-class event, fail-closed classification. ADR-0044 defines the
   intended Developer/Supply, Publication, Live-Run Data, and Owner
   Authorization domains but implements no mechanical authority separation;
   that missing enforcement is what holds this row short of L4. **That bar is
   ratified, not incidental:** ADR-0044's future implementation gate requires a
   selected enforcement substrate and a mechanical showing that Developer/Supply
   cannot reach the live workspace, and states that "only that implementation
   and verification can support an L4 data-boundary claim." This cell is a
   deliberate ceiling with a known cost, not an unfinished task. Guarded
   transport / credential confinement remains a separate, unimplemented
   publication-integrity deferral and cannot raise the live-data boundary by
   itself.
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
13. **Push-envelope posture audit (PR #45) is visibility only.** It proves in
    a disposable local Git fixture that a byte-verified hook refuses a seeded
    marker when it runs and that raw `--no-verify` remains bypass-reachable.
    It holds no credential, contacts no owner remote, does not verify a
    particular operator clone, and reports credential confinement as
    `unestablished`. It therefore leaves every data-boundary cell at L3 and
    preserves ledger entries 1 and 2.

## Frontier reading

The covered region (all five domains, all eight aspects) is uniformly L3 or
better; one aspect (Correction & supersession lifecycle) is now L4 across
every domain. The matrix is breadth- and hardening-limited, not
depth-limited within its covered domains. The live frontiers for the
owner's next selection (Tier 3):

1. **Presentation L2 → L3 — available, not selected.** The projector and
   renderer are production-shaped and synthetic end-to-end, the live viewing
   environment is decided (ADR-0047), and a confined headed invocation vehicle
   with a fail-closed preflight now exists and is synthetic-tested (footnote 5).
   The vehicle gap is closed. What remains is **real operation and the owner's
   non-descriptive attestation** — a live viewing session performed against the
   real workspace, under the five honesty preconditions ADR-0047 names. That is
   an owner act, not a build, and it is the whole remaining distance. The
   synthetic evaluation harness remains deliberately not that vehicle.
2. **L3 → L4 hardening** — retire remaining named deferrals from the
   milestone ledgers (`dividends-schedule-b-slice-deferral-ledger.md`,
   `correction-authority-and-marshaller-simplification-deferral-ledger.md`).
   ADR-0044 now separates live-run authority enforcement (required for a
   data-boundary L4 claim) from guarded publication transport (publication
   hardening). It selects or schedules neither. Other candidates remain
   ADR-0026 interest scope, ADR-0028 migration, the `closed-on-attestation`
   cross-scope projection gap, and the Track 4 F2 scaffold-visibility note.
   Free supersession policy and the marshaller binding-route duplication are
   retired.
3. **New domain breadth** — dividend boxes outside the declared universe
   (2a/3/5/7/12; deferral ledger entry 4), a second schedule attachment
   beyond Schedule B (the D1 ontology's Schedule D stub is evidence this is
   now a content question, not a design question), or a second
   income/return-level domain not yet on the matrix's columns at all.
