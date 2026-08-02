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

## Matrix (as of 2026-07-28, Presentation Row Completion records)

**Every cell is now L3 or better.** Read the Presentation row with footnote 15
before drawing any conclusion from it: all five of its columns rest on **one**
real viewing session, performed 2026-07-27. Four were recorded by amendment the
following day. There were not five sessions, and there were not two.

| Aspect ↓ / Domain → | W-2 wages (1a) | Interest (2b) | Dividends (3a/3b) | Return-level conditions (status, 12, 15, 16) | Schedule attachments |
| --- | --- | --- | --- | --- | --- |
| **Admission & identity** (facts enter with declared identity, member transitions) | L3 ⁷ | L3 ⁷ | L3 ⁹ ¹¹ | L3 ⁷ | L3 ¹¹ ¹² |
| **Source closure & completeness** (families, mappings, horizons, honest blocking) | L3 ¹ ⁷ | L3 ⁷ | L3 ⁹ ¹¹ | L3 ² ⁷ | L3 ¹¹ ¹² |
| **Computation** (rules, composition, conditionals) | L3 ⁷ | L3 ³ ⁷ | L3 ¹¹ | L3 ⁷ | L3 ¹¹ ¹² |
| **Adoption & authority** (packages, manifests, byte verification, citations) | L3 ⁴ ⁷ | L3 ⁴ ⁷ | L3 ¹¹ | L3 ⁴ ⁷ | L3 ¹¹ ¹² |
| **Explanation & audit record** (provenance, disposition ledger, non-publication walk) | L3 ⁷ | L3 ⁷ | L3 ¹¹ | L3 ⁷ | L3 ¹¹ ¹² |
| **Presentation** (form-field dispositions, rendering; human surface) | L3 ⁵ ¹⁴ | L3 ⁵ ¹⁴ ¹⁵ | L3 ⁵ ¹⁴ ¹⁵ | L3 ⁵ ¹⁴ ¹⁵ | L3 ⁵ ¹⁴ ¹⁵ |
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
   | Renderer behavior | Independently verified over the full five-disposition and T1–T3/F1–F2 synthetic regression matrix | `tools/presentation_harness/examples/manifests/citation-walk.v1.json`; `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-26-presentation-citation-walk-track1-repair-review.md` |
   | Coordinator projection | Production-shaped synthetic `live_coordinate_run` verified; every resolved field/attachment joins from coordinator-owned inputs | `tests/test_presentation_l2_integration.py`; `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-26-presentation-l2-integration-grounding-track1-review.md`; `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-26-presentation-l2-integration-grounding-track1-recheck.md` |
   | Renderer input | Internal `presentation-model.v1`, strictly validated and regenerated byte-for-byte | `packages/derivation/presentation_projection.py`; `tools/presentation_harness/examples/pages/citation-walk-fixtures/production-shaped.v1.json` |
   | Browser path | Evaluation harness: two synthetic manifests only, deliberately synthetic-bounded. Live viewing: a confined headed invocation vehicle now exists and is synthetic-tested; it has never been invoked against a real workspace | `tools/presentation_harness/examples/manifests/citation-walk.v1.json`; `tools/presentation_harness/examples/manifests/citation-walk-production-shaped.v1.json`; `packages/derivation/live_viewing.py`; `tests/test_presentation_live_viewing_vehicle.py` |
   | Live viewing environment | Decided. ADR-0047 classifies every headed-browser channel into four classes, states exactly what the owner would attest, and names the enforcement-substrate residual. Amended twice on 2026-07-27: Class C confinement and Class D precondition observation are owner-held outside the project supply chain; the session's own loopback socket is classified Class B | `docs/adr/0047-live-viewing-environment.md` |
   | Session path | Exists as one act. `open_presentation_session` runs capability → preflight → model → loopback → browser → teardown, refuses on every preflight refusal, and takes preflight answers as parameters rather than observing the machine | `packages/derivation/live_session.py`; `tests/test_presentation_live_session.py` |
   | Product surface | A separate file from the evaluation fixture, asserting no provenance in either direction; the session refuses fail-closed to serve any page declaring itself synthetic | `packages/presentation/pages/citation-walk.v1.html` |
   | Rehearsal | The full path ran end to end against a synthetic workspace: fail-closed default, all three refusals, the clear path, teardown, and the failure path — with a stub in place of a browser. **Both remaining rehearsal gaps closed 2026-07-27** (footnote 14): a real headed browser was launched by the real path, and it rendered the product page | `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-27-presentation-live-session-path-track3-rehearsal.md`; `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-27-presentation-real-session-attestation-track2-rehearsal.md` |
   | Real operation | **Performed 2026-07-27** against the real residency, with the ADR-0031 Decision 7 non-descriptive attestation and all five ADR-0047 preconditions affirmed. This is what moves the W-2 wages (1a) cell to L3 and nothing else (footnote 14) | `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-27-presentation-real-session-attestation-track3-attestation.md` |

   **Live Session Path (2026-07-27)** built and rehearsed everything the L3
   session needs without performing one. Its two findings are the durable
   lesson, and both are one mistake in different clothes: the parts were correct
   and the *join* between them was not. Serving a real model through an
   evaluation-shaped page over an open loopback socket put the owner's complete
   return behind nothing but an ephemeral port — which is not a secret, the full
   range being scannable in well under a second — and put the words "synthetic
   `demo-*` data only" in the title of the screen the owner would read while
   forming the attestation. Neither defect was visible from inside either
   component. What remains for L3 is one owner act: supply the three preflight
   answers, run the session, look, and attest.
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
    ratified shape — archived review families under
    `docs/archive/2026-08-02-milestone-artifacts/reviews/` for
    `2026-07-19-dsbs-t2-*`, `2026-07-20-dsbs-t3-*`, and
    `2026-07-20-dsbs-t4-*`),
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
14. **Evidential basis for the Presentation W-2 wages (1a) L3 claim
    (Ontology §8), and why the other four Presentation cells stay L2.**
    Presentation — Real Session and Attestation, 2026-07-27.

    Same pattern as footnotes 7 and 11, and it holds for the same two reasons.
    First, the synthetic battery exercises the **identical path** in-repo:
    `tests/test_presentation_live_session.py`,
    `tests/test_presentation_live_viewing_vehicle.py`, and
    `tests/test_presentation_l2_integration.py`, plus both evaluation manifests
    as an unchanged regression floor. Second, the owner's non-descriptive
    attestation establishes that the capability **operated on real data with the
    boundary intact** — the session performed, dispositions observed in
    quarantine, no artifact crossed — with each of ADR-0047's five honesty
    preconditions affirmed individually rather than in summary, conditions 3 and
    4 being owner knowledge rather than mechanism
    (`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-27-presentation-real-session-attestation-track3-attestation.md`).

    **No L3 claim here rests on, or may ever cite, quarantined run detail.** L3
    asserts the capability operated. It asserts no disposition was correct, and
    no reader should infer one from this cell.

    One thing is new relative to footnotes 7 and 11, and it is the reason this
    milestone had a Track 2 at all. For a *human surface*, the person who would
    see a defect is the one person forbidden to describe it. So the first real
    render was deliberately not the real session: a real headed browser was
    launched by `open_presentation_session` against a **synthetic** workspace
    and rendered the product page there, where description is safe, before the
    real residency was touched
    (`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-27-presentation-real-session-attestation-track2-rehearsal.md`).
    That rehearsal closed both gaps this footnote's predecessor named, and found
    no page defect. It also gave the interrupt-teardown repair its first human
    confirmation — no surviving browser, no surviving session directory.

    **The other four Presentation cells remain L2, and this is by design rather
    than by omission.** One attestation raises only what it covers. The owner
    named the W-2 wages (1a) column at plan stage, and the milestone's non-goals
    foreclose inferring the rest; nothing about the session mechanically
    distinguishes the columns, but the *record* distinguishes them, and the
    record is what a maturity claim rests on. Raising Interest, Dividends,
    Return-level conditions, or Schedule attachments requires the owner to say
    so in an attestation — naming a column is not describing content — not an
    inference drawn here.

    **Named gap.** Track 2's browser-start-failure exercise was skipped, which
    its charter permitted. The classified-refusal path — a browser that fails to
    start arriving as a stable reason code rather than as a traceback — is
    established by tests and by independent review, and **not** by human
    observation. It is the least-exercised part of the session path.
15. **The whole Presentation row rests on one session.** Presentation — Completing
    the Row, 2026-07-28. **Read this before footnote 14 or the row itself.**

    There has been exactly **one** real viewing session in this project's
    history: 2026-07-27. It rendered all nine published lines and Schedule B
    Parts I and II from real data in a single render. Footnote 14 recorded the
    W-2 wages (1a) column from it. This footnote records the other four, from the
    **same session**, on an amendment the owner filed the following day naming
    the columns they observed
    (`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-27-presentation-real-session-attestation-track3-attestation.md`,
    "Amendment, 2026-07-28").

    **No part of this row asserts that five sessions occurred, or two.** A row
    filled in over two days by two milestones is exactly the shape that invites
    that misreading, which is why it is foreclosed here rather than left to
    inference.

    **Why an amendment is sufficient, on the ratified terms.** Three things, and
    the third is the one that does the work. The surface covers all five columns
    — verified directly rather than inherited from the prior closeout, which had
    itself said "no build gap" before three code defects were found: the
    production-shaped fixture carries sections for lines 1a, 2b, 3a, 3b, 9, 11,
    12, 15, and 16, plus a Schedule B citation group with Part I (interest,
    box-1 / 1099-INT family) and Part II (ordinary dividends, box-1a / 1099-DIV
    family), and `_resolve_attachment` in
    `packages/derivation/presentation_projection.py` projects attachments into
    the model. The session rendered that surface from real data. And **L3 asserts
    the capability operated, not that the owner audited it** — footnotes 7 and 11
    have said exactly that since 2026-07-18, so extending the claim to columns
    the same render covered is a statement of the already-ratified kind.

    **What the owner supplied, because the repository cannot.** ADR-0031
    Decision 7's shape includes that the owner observed dispositions in
    quarantine, so naming a column asserts observation of it. The milestone
    required an explicit statement per column rather than inferring observation
    from the render, and specified that **a column the owner did not name would
    not move**. All four were named. The control did not fire, but it was real:
    the row could have closed ragged.

    **No L3 claim here rests on, or may ever cite, quarantined run detail** —
    same posture as footnotes 7, 11, and 14, unchanged. L3 asserts the capability
    operated and asserts no disposition was correct.

    **Two gaps stand open and do not close with this row.** Both need a session
    to exercise, and this milestone performed none. First, the
    **classified-refusal path still has no human confirmation** — that a browser
    failing to start arrives as a stable reason code rather than a traceback
    rests on tests and independent review only (footnote 14). It is the oldest
    open item on this path. Second, the **session runbook has an unidentified
    unclarity**, reported by its first human user with the sentence unnamed.
    Neither concerns the capability that operated; both concern the failure path
    and the instructions.

## Frontier reading

**The matrix is complete at L3 or better in every cell**, as of 2026-07-28. One
aspect (Correction & supersession lifecycle) is L4 everywhere. There is no
ragged row and no L2 cell left.

This is the condition the Real Return phase was aimed at, and it means the
matrix has stopped being a selection instrument for this phase: **frontier-driven
selection has no frontier left inside these five columns.** What remains is
either hardening the covered region, widening the columns, or leaving the
instrument's coordinate system entirely.

Read that completion accurately before spending it. It is **breadth-limited and
hardening-limited by construction**: five income/return domains, one implemented
schedule, one human surface, one real viewing session behind the entire
Presentation row (footnote 15). It is not a claim that the product is finished
for its user.

The live candidates (Tier 3, owner-held):

1. **A new phase.** The Real Return roadmap sets no ladder and one standing test:
   *"does the product now do something for its user that it could not do
   before?"* That test is met — the system holds and computes the owner's real
   data, explains it with citations, and now shows it to them on a human surface
   that has really operated. With every cell at L3 the phase has a legible
   boundary, and the matrix's own silence is the argument: the next question for
   this product is not on these axes. **This is the recommended reading.**

   Two items follow into whatever comes next, named so they are not lost with the
   row that carried them: the **classified-refusal path has never been confirmed
   by a human** (footnote 14 — the oldest open item on this path, and it needs a
   session to close), and the **session runbook has an unidentified unclarity**
   reported by its first human user.
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
