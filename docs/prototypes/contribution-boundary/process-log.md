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

## Round 2 — committee (staged)

| Seat | Tier | Context | Charter |
|---|---|---|---|
| Governance reviewer | Medium | independent sub-agent | `charter-review-governance.md` |
| Adversary reviewer | High | independent sub-agent | `charter-review-adversary.md` |

## Next foreman action (after committee)

Collate + triage committee findings; if convergence confirmed with no surviving
decision-blocking defect, author ADR-0032 (recommending a scoped confirmation
pass for any foreman-authored fix); else charter a Round-2 build iteration.
