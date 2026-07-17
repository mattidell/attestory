# Production Package Resolver (D3) — Seat File

## Current step

Iteration 2 committee is complete. Both reviewers find ADR-0033 unsupported:
the release/registry bytes are not independently verified, current user adoption
selection is not defined, and both D3-P2 ledgers overclaim or omit dispositions.

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

## Next action

Owner decides whether to authorize a bounded paired Iteration-3 build or stop
D3. Any next build must exercise verified release bytes, exact current-user
adoption selection, order-independent same-key refusal, and an item-by-item
ledger; it requires new rival and committee evidence. The actual cap total is
2,081 lines under the owner-directed committee variance.
