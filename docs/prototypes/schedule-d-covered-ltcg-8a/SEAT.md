# Covered Long-Term Gains, Schedule D Line 8a — Seat File

## Current step

The owner selected the rival topology, adopted CA-02/P2-S5, and authorized
the CA-04 repair. The bounded repair is chartered, assigned back to the
rival Builder for design continuity.

## Seats

| Role | Holder | Status |
| --- | --- | --- |
| Foreman | Current foreman thread | Active; scope/economy and custody only |
| Incumbent Builder | Returned on `prototypes/schedule-d-covered-ltcg-8a/it1` | Complete; not carried forward (owner disposition 2026-08-01) |
| Rival Builder | Returned on `prototypes/schedule-d-covered-ltcg-8a/it2` | Complete; selected topology, pending this repair |
| Contract/adversary Reviewer | Returned | Complete; `NOT READY`. `reviews/contract-adversary.md` (commit `4fa6c10`) |
| Expressiveness Reviewer | Returned | Complete; `READY` for rival topology. `reviews/expressiveness.md` (commit `8d8811f`) |
| Repair Builder | Owner-launched context on `prototypes/schedule-d-covered-ltcg-8a/it2` (continuing branch) | Chartered; not yet launched |

## Binding handoff

- Branch: `prototypes/schedule-d-covered-ltcg-8a/it2` (continuing)
- Charter: `docs/prototypes/schedule-d-covered-ltcg-8a/charter-repair1.md`
- Triage record: `docs/prototypes/schedule-d-covered-ltcg-8a/round-1-triage.md`
- Repair object: rival design at `bbecd3f3aae6777cf06e4bdbe58d91545f4faedd`
- Outputs: `repair1/design.md`, `repair1/examination.md`
- Evidence ceiling: Rung 1 paper only
- Scope: CA-02 (explicit P2-S5 successor sentence) and CA-04 (exact P3 pin
  contract) only. Not P1. Not CA-05/CA-06.

## Next action

Owner launches the Repair Builder against the exact charter. On return, the
foreman takes custody and charters one focused confirmation reviewer to
recheck only CA-02, CA-04, and regression of the already-settled P1/P2/P3
boundaries — per the plan, this repair spends the fixed pass; a second
substantive defect returns to the owner.
