# Process Log — D3 Production Package Resolver

Topic branch: `decision/d3-production-resolver` (foreman git custody; merges once
at ratification per ADR-0030). Candidate ADR-0033. **Last Track-0 decision.**
Tier 2 (default + veto). Interlocks: consumes D1 (ADR-0031, residency/leak wall)
and extends ADR-0027 d7 / ADR-0028 beyond the fixture boundary.

| When | Event |
|---|---|
| 2026-07-16 | Plan approved by owner (PR #6, merged `a213cf3`). |
| 2026-07-16 | Charters authored: `charter-it1.md` (incumbent, High), `charter-it2.md` (clean-room rival, High). **Awaiting dispatch (owner-launched builders, per established pattern).** |

## Round 1 seats

| Seat | Tier | Context | Charter | Status |
|---|---|---|---|---|
| Incumbent builder | High | independent | `charter-it1.md` | staged |
| Rival builder | High | independent, sealed | `charter-it2.md` | staged |

## Awaiting (Round 1 deliverables)

- `it1/design.md` (≤300) + `examination-it1.md` (≤120)
- `it2/design.md` (≤300) + `examination-it2.md` (≤120)

## Cap tracking (recalibrated)

Running total watched at each round boundary (foreman duty per role template).
Target ≤ 1,800 lines through committee; per-design ≤ 300.

## Next foreman action (on receipt)

Triage-classify each builder's findings (Gate 5), confirm the seal held and the
running cap total, then dispatch the Round-1 committee — Governance (Medium) +
Adversary (Medium) — in independent contexts under the plan's standing
authorization. Do not review artifact quality; triage and route only.
