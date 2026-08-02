# Capital-Gain Distributions to Line 7a — Clean-Room Rival Seat

## Current step

The owner ratified ADR-0050 on 2026-07-29 after the final recheck returned
`READY FOR OWNER RATIFICATION` with no residuals. No Builder or Reviewer role
is active. The complete Track-0 decision unit is PR #110; production remains
blocked until the owner merges it to `main`.

## Seats

| Role | Holder | Status |
| --- | --- | --- |
| Foreman | Current foreman thread | Active; scope/economy and custody only |
| Rival Builder | Owner-launched context on `prototypes/capital-gain-distributions-line7a/it2` | Returned at `099882e` |
| Contract/adversary Reviewer | Local independent context | Returned at `7dc6c40` |
| Expressiveness Reviewer | Local independent context | Returned at `d73fca2` |
| Repair Builder | Selected rival Builder context | Returned at `a60e2d1` |
| Repair 1 Confirmation Reviewer | Author-independent local context | Returned at `f84b2ba` — `NOT READY` |
| Repair 2 Builder | Dispatched High/high context | Returned at `c534f95` |
| Repair 2 Confirmation Reviewer | Fresh author-independent context | Returned at `1e18e64` — `READY` |
| Contract Synthesis Builder | Fresh High/high context | Returned at `6ec26fd` |
| ADR-0050 Contract Reviewer | Fresh author-independent High/high context | Returned at `4784316` — `NOT READY` |
| ADR-0050 Contract Repair Builder | Synthesis context | Returned at `4a1c643` |
| ADR-0050 Recheck Reviewer | Author-independent focused context | Returned at `fe7a0cd` — `NOT READY` |
| ADR-0050 Repair 2 Builder | Synthesis context | Returned at `4e19c09` |
| ADR-0050 Final Recheck Reviewer | Author-independent focused context | Returned at `4048596` — `READY FOR OWNER RATIFICATION` |

## Binding handoff

- Branch: `prototypes/capital-gain-distributions-line7a/it2`
- Charter:
  `docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/charter-it2.md`
- Plan: `docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/plan.md`
- Outputs: `it2/design.md`, `it2/examination.md`
- Evidence ceiling: Rung 1 paper only
- Clean-room seal: no iteration-1 branch, output, review, thread, or summary

## Next action

Owner merge of PR #110 after CI `verify` is green. No production role starts
before that merge reaches `main`.
