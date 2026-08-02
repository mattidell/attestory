# Covered Long-Term Gains, Schedule D Line 8a — Seat File

## Current step

Both committee reviews are complete. The foreman's Gate-5 triage
(`round-1-triage.md`) records reviewer agreement, one unresolved dissent
(CA-04 on the rival's P3 pin contract), and a recommended repair scope.
**Owner disposition is required** before any repair is chartered: topology
selection, CA-02/P2-S5 adoption, and CA-04 repair authorization.

## Seats

| Role | Holder | Status |
| --- | --- | --- |
| Foreman | Current foreman thread | Active; scope/economy, custody, and Gate-5 triage only |
| Incumbent Builder | Returned on `prototypes/schedule-d-covered-ltcg-8a/it1` | Complete; not recommended to carry forward (CA-01/CA-03, corroborated case-6 data loss) |
| Rival Builder | Returned on `prototypes/schedule-d-covered-ltcg-8a/it2` | Complete; recommended topology, pending CA-04 repair and explicit P2-S5 adoption |
| Contract/adversary Reviewer | Returned | Complete; `NOT READY`. `reviews/contract-adversary.md` (commit `4fa6c10`) |
| Expressiveness Reviewer | Returned | Complete; `READY` for rival topology, does not address CA-04. `reviews/expressiveness.md` (commit `8d8811f`) |
| Repair Builder | Unassigned | **Not chartered.** Owner must select topology and authorize repair scope first (Gate 4: one bounded pass, owner-directed) |

## Binding handoff

- Branch: `prototypes/schedule-d-covered-ltcg-8a/it2` (continuing)
- Triage record: `docs/prototypes/schedule-d-covered-ltcg-8a/round-1-triage.md`
- Both reviews: `reviews/contract-adversary.md`, `reviews/expressiveness.md`

## Next action

Owner reviews `round-1-triage.md` and dispositions: (1) confirm the rival
topology as the selected direction; (2) adopt or reject CA-02/P2-S5 as the
completeness-boundary successor; (3) authorize the CA-04 repair pass. Only
after that does the foreman charter the repair.
