# Production Package Resolver (D3) — Seat File

## Current step

Iteration-3 builds delivered (owner re-authorized after the earlier rescission)
and in foreman custody. Foreman triage: both `it5`/`it6` independently close all
four Iteration-2 decision-blocking findings (release-byte authority,
current-user adoption, order-independent same-key refusal, exhaustive ledger),
retain the strict `ok == True` gate, and name RG-1 (eight core issues) as a MUST
prerequisite; seal attested. **Blocked on owner approval to dispatch a Round-3
committee (ADR-0034); no reviewer dispatched.** Cap total 2,937 lines (owner
variance in effect).

## Seats

| Seat | Status |
| --- | --- |
| Principal foreman | active; holds process and git custody on `decision/d3-production-resolver` |
| Round-1 incumbent builder | complete; `it1/design.md`, `examination-it1.md` |
| Round-1 clean-room rival | complete; `it2/design.md`, `examination-it2.md`; seal held |
| Governance reviewer | complete; `reviews/governance-r1.md` |
| Adversary reviewer | complete; `reviews/adversary-r1.md` |
| Round-2 incumbent builder | complete; `it3/design.md`, `examination-it3.md` |
| Round-2 clean-room rival | complete; `it4/design.md`, `examination-it4.md`; seal held |
| Round-2 Governance reviewer | complete; `reviews/governance-r2.md` |
| Round-2 Adversary reviewer | complete; `reviews/adversary-r2.md` |
| Iteration-3 incumbent builder | complete; `it5/design.md`, `examination-it5.md` |
| Iteration-3 clean-room rival | complete; `it6/design.md`, `examination-it6.md`; seal held |
| Round-3 Governance reviewer | not dispatched — awaiting owner approval (ADR-0034) |
| Round-3 Adversary reviewer | not dispatched — awaiting owner approval (ADR-0034) |

## Next action

Await owner direction. Do not dispatch either builder from the staged charter.
If reauthorized, both seats remain limited to the four committee findings and
Rung-2 evidence; no production code is authorized. Under ADR-0034, every future
dispatch — including committee review — needs immediate, explicit owner approval
for the exact role and current charter.
