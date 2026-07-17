# Process Log — D2 Contribution Boundary

Topic branch: `decision/d2-contribution` (foreman git custody; merges once at
ratification per ADR-0030). Candidate ADR-0032. Interlocks with D1 (ADR-0031,
ratified) — a contribution writes into the ratified residency boundary.

| When | Event |
|---|---|
| 2026-07-16 | Plan approved by owner (PR #4, merged `548318b`). |
| 2026-07-16 | Charters authored: `charter-it1.md` (incumbent, High), `charter-it2.md` (clean-room rival, High). **Awaiting dispatch.** |
| 2026-07-16 | Both builder artifact pairs landed under foreman custody at `32de94d`. Incumbent examination: 117 lines; rival examination: 107 lines (both within the 120-line examination cap). Rival examination attests the clean-room seal held. |
| 2026-07-16 | **Foreman error / fixed-cap incident:** the plan's 900-line total-topic Markdown cap is crossed: 1,102 lines before the required D2 seat record. The charters did not make a seat file before builder receipt. Per Gate 4, stop-and-decide; no committee dispatch pending owner disposition. |

## Round 1 seats

| Seat | Tier | Context | Charter | Status |
|---|---|---|---|---|
| Incumbent builder | High | independent | `charter-it1.md` | complete (`32de94d`) |
| Rival builder | High | independent, sealed | `charter-it2.md` | complete (`32de94d`; seal attested) |

## Delivered (Round 1)

- `it1/design.md` + `examination-it1.md` (117-line examination)
- `it2/design.md` + `examination-it2.md` (107-line examination)

## Gate-4 cap disposition (owner, 2026-07-16)

Owner directed **proceed + recalibrate**. Foreman verification found the flag
miscalibrated: D2 (1,130 lines) is **leaner than D1** (1,548, shipped unflagged);
the overage is thorough designs (261/286), not scope pathology (no extra
iterations, no adjacent-defect creep, no implementation bleed). Owned stewardship
misses: not tracking the running total, no SEAT at charter time. Root-cause fix
applied: the foreman role template's cap calibration is rewritten (per-design
≤ 300; total target ≤ 1,800 through committee; a crossing is a signal to check
for pathology, not an automatic defect; the running total is the foreman's to
watch each round) and the D2 plan's cap updated. D2 now sits under the
recalibrated target; committee cleared to dispatch.

## Foreman triage — Round 1 (Gate 5; routing, not adjudication)

**Seal:** held. Rival attests it, uses an independent probe (`probe_d2_it2.py`,
15/15) and distinct vocabulary (`RunContext` TypeError probes, `finding.v2`
`contribution_id`).

**Convergence (both independently — record as settled-at-Rung-2 pending committee):**
contribution as one **atomic act** with asserted findings pinning it; a separate
contribution-record (Article 14); the contribution↔fact link as **provenance-only,
not a standing edge** (two-edge doctrine preserved); runs-consume-facts enforced
**structurally** (closed run-request / `RunContext` with no raw-input slot, probed
by validation/`TypeError`); any-order **commutativity** (disjoint facts/horizons,
currency from record not arrival); **correction by supersession** via ordinary
assertion with the family horizon **not** advancing; D1 interlock — contribution
writes only to `L`.

**Decision-blocking item routed to committee (the crux):** the **fixture/scenario
adapter as a live bypass.** Incumbent Case 6: the committed adapter silently
published `777` from an unprojected raw input. Both name adapter-unreachability /
a marshal-only run context as *production* work. The committee (Adversary) must
resolve whether runs-consume-facts is **settled at the contract level** (rival:
structurally, no raw-input slot) with adapter-unreachability as a named production
condition, or whether the adapter is an **unclosed hole**.

**Divergence for Governance:** provenance-linkage model — incumbent's standalone
`contribution-record` + contribution/document pins vs rival's chain
finding→contribution→evidence→act (document-version = immutable evidence id,
consistency enforced at admission). Which conforms to Article 12 + the existing
evidence model.

**Deferred (not decision-blocking):** OCR/import/UI, multi-party/consent
contribution, the marshal-only constructor made structural (D3), E14.2
registration (Track 2).

## Round 2 — committee (delivered)

| Seat | Tier | Context | Output |
|---|---|---|---|
| Governance reviewer | Medium | isolated sub-agent | `reviews/governance-r1.md` |
| Adversary reviewer | High | isolated sub-agent | `reviews/adversary-r1.md` |

Spawned as isolated sub-agents (standing plan authorization); each returned its
review as a final message (never on disk during the other's run) — within-round
independence held. Both committed under custody.

## Foreman triage — committee (Gate 5)

**Both propositions survive at Rung 2; no decision-blocking hole.** The committee
splits its preference by axis — a synthesis, not "adopt one build":

- **Provenance basis → rival (it2)** (Governance M2): retain `evidence_ids` (the
  Article 1 documentary channel), add optional `contribution_id`, enforce
  contribution↔evidence consistency at admission, evidence-id-as-version. The
  incumbent's `evidence_ids` *removal* is a divergence that weakens Art. 1.
- **Runs-consume-facts framing → incumbent (it1)** (Adversary A1): the Adversary
  **reproduced the bypass at the runner** (published `7770000` pinned to ghost
  ids via a directly-constructed `RunContext`). The incumbent is honest (closes
  the *request*; names the marshaller as production); the rival **overclaimed**
  "structural by type" — false, since `inputs`/`sources` accept invented value+id.
  **MUST conditions for the ADR:** (a) `run-request.v1 ≠ RunContext`; (b) a
  marshal-only `RunContext` constructor + entrypoint-unreachability kill-test;
  (c) strike the rival's "structural by type" claim.
- **Any-order scoped to independent facts** (Adversary A4): a correction of fact X
  legitimately depends on X's asserting contribution (SC-R1); "any order" is not
  unconditional. The ADR names this scoping.
- **Settled (both):** two-edge doctrine held (provenance pin is not an edge, M3/A2);
  correction-by-supersession clean, horizon does not advance (M4/A5); D1 interlock
  rests on ADR-0031's fail-closed default, consumed not re-proven (M6/A3).

**Named conditions for the ADR / Track 2 (not decision-blocking):** rival's
successor carrier act schemas (`act-member-transition.v2` / `act-assertion.v2`
admitting finding.v2, Governance M1); the E14.2 static check (rule cannot name a
contribution dependency); contribution-record registration; the marshal-only
constructor made structural (interlocks D3).

**Authority note:** Art. 12 literally governs *derived*-finding lineage; the
contribution pin rides a *human* finding, so Art. 1/15 govern with Art. 12 by
analogy (Governance M2). A precision note for the ADR, not a doc conflict.

**No foreman-authored fix:** every adopted position is builder-designed and
reviewer-endorsed (a selection among reviewed options per the committee's steer),
so no scoped confirmation pass is required (ADR-0013 2026-07-15).

## Next foreman action

Author **ADR-0032** on this synthesis (rival provenance + incumbent runs-framing,
MUST conditions, any-order scoping, named production conditions) and open the D2
ratification PR for owner-held merge. Ratification (proposed → accepted) is
owner-held.
