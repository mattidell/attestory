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

## Round 2 — committee (staged, awaiting dispatch)

| Seat | Tier | Context | Charter |
|---|---|---|---|
| Governance reviewer | Medium | independent | `charter-review-governance.md` |
| Adversary reviewer | High | independent | `charter-review-adversary.md` |

Per ADR-0013's reviewer-dispatch amendment, owner plan approval is standing
authorization to spawn reviewers as sub-agents; owner has elected external
launch for prior seats. Dispatch mode is the owner's call.

## Next foreman action (after committee)

Collate committee findings, triage-classify, and either (a) author ADR-0031 if
the committee confirms convergence with no decision-blocking defect, recommending
a scoped confirmation pass for any foreman-authored fix (ADR-0013 2026-07-15
amendment); or (b) charter a Round-2 build iteration if a decision-blocking
defect survives.
