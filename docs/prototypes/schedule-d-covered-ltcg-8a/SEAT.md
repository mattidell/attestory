# Covered Long-Term Gains, Schedule D Line 8a — Seat File

## Current step

Repair 1 returned, claiming CA-02 and CA-04 both resolved at Rung 1 with an
exact pin contract. A focused, author-independent confirmation reviewer is
chartered to attempt to falsify that claim before contract synthesis.

## Seats

| Role | Holder | Status |
| --- | --- | --- |
| Foreman | Current foreman thread | Active; scope/economy and custody only |
| Incumbent Builder | Returned on `prototypes/schedule-d-covered-ltcg-8a/it1` | Complete; not carried forward (owner disposition 2026-08-01) |
| Rival Builder | Returned on `prototypes/schedule-d-covered-ltcg-8a/it2` | Complete; selected topology |
| Contract/adversary Reviewer | Returned | Complete; `NOT READY`. `reviews/contract-adversary.md` (commit `4fa6c10`) |
| Expressiveness Reviewer | Returned | Complete; `READY` for rival topology. `reviews/expressiveness.md` (commit `8d8811f`) |
| Repair Builder | Returned on `prototypes/schedule-d-covered-ltcg-8a/it2` | Complete; `repair1/design.md`, `repair1/examination.md` (commit `e6747fd`). Claims CA-02 and CA-04 both resolved |
| Confirmation Reviewer | Owner-launched context on `prototypes/schedule-d-covered-ltcg-8a/it2` (continuing branch) | Chartered; not yet launched |

## Binding handoff

- Branch: `prototypes/schedule-d-covered-ltcg-8a/it2` (continuing)
- Charter:
  `docs/prototypes/schedule-d-covered-ltcg-8a/charter-repair1-confirmation.md`
- Repair object: `e6747fd`
- Output: `reviews/repair1-confirmation.md`
- Evidence ceiling: Rung 1 paper only

## Next action

Owner launches the Confirmation Reviewer against the exact charter. On
return, the foreman takes custody. If `READY`, the foreman proceeds to
contract synthesis (drafting the successor ADR against the full evidence
chain) for owner ratification. If `NOT READY`, this repair pass is spent
(Gate 4 fixed cap); any further defect returns to the owner as a fresh
disposition question, not an automatic second repair.
