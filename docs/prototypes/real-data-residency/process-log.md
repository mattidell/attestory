# Process Log — D1 Real-Data Residency Boundary

Topic branch: `decision/d1-real-data-residency` (foreman git custody; merges once
at ratification per ADR-0030). Candidate ADR-0031. Owner directed D1 **solo**.

| When | Event |
|---|---|
| 2026-07-16 | Plan approved by owner (PR #2, merged `c33cd66`). |
| 2026-07-16 | Charters authored: `charter-it1.md` (incumbent, High), `charter-it2.md` (clean-room rival, High). Pushed on topic branch. |
| 2026-07-16 | Dispatch: owner launches both builders externally (foreman confirmation gate resolved by owner). |
| 2026-07-16 | Round 1 builds landed; foreman took custody (both outputs committed, data-safety scan clean). Triage below. |

## Round 1 seats

| Seat | Tier | Context | Status |
|---|---|---|---|
| Incumbent builder | High | independent, external (owner-launched) | delivered |
| Rival builder | High | independent, external, sealed from incumbent | delivered |

## Foreman triage — Round 1 (Gate 5; routing, not adjudication)

**Seal:** held. Rival uses independent vocabulary (`NEVER_CROSSES`/`MAY_CROSS`,
exit 42/43, crossing-envelope) and cites no incumbent material.

**Governance anchors:** verified real — Constitution Article 18, E18.1/E18.2/E18.3,
Ontology quarantine + sensitivity-inheritance + synthetic-by-default. The
provenance-manifest design discharges E18.3's recorded debt entry.

**Convergence (both independently — record as settled-at-Rung-2 pending committee
confirmation, not for redesign):** out-of-repo residency by rule; directional
capability wall (run reads workspace, authoring env has no capability to it);
total **fail-closed** binary classifier with no undecided class (resolves Case 5);
**independent** commit and push gates scanning the full envelope, not a diff from
`main` (resolves ADR-0030 §C.8); CI/remote as audit-only because receipt is
publication; synthetic derivation by **independent construction** (not
sanitization) with manifest + byte-regeneration + value-overlap check;
sensitivity inheritance — a live disposition report is quarantined even without
amounts.

**Decision-blocking items routed to committee (divergences + named seams):**
1. **Locator model divergence.** Incumbent commits a pointer indirection (env var
   *or* an ignored-root pointer file, e.g. `local-data/…`); rival commits **no**
   locator in any form (runtime capability only). §C.8 forbids a load-bearing
   ignore — is an ignored-root pointer file load-bearing? → Adversary pressures
   the incumbent's ignored-root pointer; committee names the adopted model.
2. **Hook-bypass seam.** Both flag per-clone bypassable hooks; both name guarded
   transport + structural hook install + integrity check as production
   conditions. → The ADR must state precisely which of these are Rung-2-settled
   contract vs named production conditions (Article 18 "structural where
   structure can hold it").
3. **Kill-surface completeness.** Incumbent found a *live* gap (tag-annotation
   leak crossed under v2 → v2.1 object scan); rival's push design covered tag
   messages a priori and makes omission mechanically detectable (delete `push`
   → exit 43). → Adversary hunts a surface the **union** still misses; committee
   confirms omission-detection covers the incumbent's found gap.
4. **D1-P2 shape channel.** Incumbent flagged it open (can shape alone encode a
   value?); rival's grammar excludes observed string lengths and "features whose
   only authority is a live document." → Adversary tests whether the converged
   grammar closes the shape channel.

**Deferred (not decision-blocking):** exact scan/policy-schema bytes and
rule-numbering (Track 1/3); the concrete filesystem path (owner picks at
bootstrap); exit-code/rule-name vocabulary.

## Round 2 — committee (delivered)

| Seat | Tier | Context | Output | Status |
|---|---|---|---|---|
| Governance reviewer | Medium | sub-agent, isolated | `reviews/governance-r1.md` | delivered |
| Adversary reviewer | High | sub-agent, isolated | `reviews/adversary-r1.md` | delivered |

Spawned as isolated sub-agents under the plan's standing authorization; each
returned its review as a final message (never on disk during the other's run),
so within-round independence held. Both committed under foreman custody.

## Foreman triage — committee (Gate 5)

**Both reviewers independently converge:** the **rival (it2) design is
conformant / survives at Rung 2**; the **incumbent (it1) carries
decision-blocking gaps on the same three axes** the rival resolves. This is
convergence with a clear winner, not an open split.

**Decision-blocking (all against it1; each resolved by adopting it2):**
1. **§C.8 push independence.** it1's push scan keys on remote-tracking state
   (`rev-list --not --remotes`) — the forbidden diff-from-remote mechanism
   (Governance M2). it2 scans the full outgoing envelope independently.
2. **Sensitivity inheritance.** it1's content-screen classifier cannot catch
   *description-based* sensitivity — a review describing a real run passes
   (Governance M4, Ontology §8). it2 makes personal *description* →
   `NEVER_CROSSES`.
3. **Locator model.** it1's ignored-root pointer is a load-bearing ignore, and
   its locator screen is a prefix denylist that a novel absolute root
   (`/Volumes/…`) evades on a fresh clone/CI (Governance M6, Adversary A2).
   it2 commits **no** locator (runtime capability only).
4. **D1-P2 shape channel.** it1's extract-then-fill leaks observed field names,
   exact cardinality, and closure topology *as shape* (Adversary A4). it2's
   independent-construction-from-public-grammar rule closes all three. D1-P2
   ratifies as one rule; the union does not rescue it1 — it2's rule is adopted.

**Blocking-adjacent:** the hook-bypass seam (Adversary A3) closes only under
it2's guarded-transport credential-custody framing; it1's remote purge-and-rotate
is not load-bearing-safe under §C.8. Both name guarded transport as a Gate-7
production condition.

**Confirmed sound (both):** surface enumeration is complete (Adversary A1, clean
bill on remote-crossing surfaces); fail-closed totality holds, no third class
(Adversary A5); E18.3 discharged (Governance M5; it2's byte-regeneration
stronger).

**Named residuals for the ADR (not blocking):** `git add`→index is local-only
(no remote carry); coverage-expansion decision log must stay quarantined
(Adversary A5 selection-pattern channel); the locator screen's
provenance/allow-list form (permitted synthetic-path grammar; deny all other
absolute forms) is a **foreman-authored refinement** beyond either builder →
per ADR-0013 (2026-07-15) it defaults to a scoped confirmation pass before
ratifiable text.

**Owner-held reconciliation (blocks ratification):** Governance M4 surfaced a
Constitution/Ontology-vs-milestone-plan conflict — milestone Verification says
"the report (dispositions, not values) is what reviews cite," but Ontology §8
sensitivity-inheritance makes a disposition report describing a real run
sensitive. The Constitution governance note classes such conflicts as **defects
requiring versioned correction** — owner's to reconcile before ADR-0031.

## Round 3 — ADR + confirmation pass

| When | Event |
|---|---|
| 2026-07-16 | Owner decisions: (1) Ontology governs the doc-vs-doc conflict → milestone plan Verification corrected by version (disposition detail quarantined; only a non-descriptive attestation crosses). (2) Author ADR-0031 on the it2 basis with the confirmation pass. |
| 2026-07-16 | **ADR-0031 authored** (`docs/adr/0031-real-data-residency-boundary.md`, status **proposed**). Decisions 1–4, 6–8 on the it2/committee basis; Decision 5 (provenance/allow-list locator screen) is a foreman-authored fix marked **pending scoped confirmation**. Production conditions named for Tracks 1/3. |
| 2026-07-16 | Confirmation pass chartered (`charter-confirm-locator-screen.md`, Medium) exercising the **over-inclusion** direction of Decision 5; dispatched as an isolated sub-agent. **Awaiting `reviews/confirm-locator-screen.md`.** |

## Next foreman action (after confirmation pass)

If the pass returns clean: finalize Decision 5 as ratifiable and open the D1
ratification PR (ADR-0031 + full evidence bundle) for owner-held merge. If it
finds over-fire: apply the minimal named amendment (e.g. a scoped declaration
privilege), re-confirm if the amendment is itself foreman-authored, then open the
PR. Ratification (proposed → accepted) is owner-held.
