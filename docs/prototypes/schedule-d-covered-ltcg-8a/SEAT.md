# Covered Long-Term Gains, Schedule D Line 8a — Seat File

## Current step

Both prototype iterations are complete. The contract/adversary committee
review is chartered. The expressiveness review is not yet chartered — it
follows after this one returns, to keep review-in-progress isolated.

## Seats

| Role | Holder | Status |
| --- | --- | --- |
| Foreman | Current foreman thread | Active; scope/economy and custody only |
| Incumbent Builder | Returned on `prototypes/schedule-d-covered-ltcg-8a/it1` | Complete; outputs at `it1/design.md`, `it1/examination.md` (commit `d4e2203`) |
| Rival Builder | Returned on `prototypes/schedule-d-covered-ltcg-8a/it2` | Complete; outputs at `it2/design.md`, `it2/examination.md`, including the self-corrected P3-S4/S6 cycle fix (commit `bbecd3f`) |
| Contract/adversary Reviewer | Owner-launched context on `prototypes/schedule-d-covered-ltcg-8a/it2` (continuing branch) | Chartered; not yet launched |
| Expressiveness Reviewer | Unassigned independent context | Not chartered |
| Repair Builder | Unassigned | Not chartered; owner direction required after both reviews |

## Binding handoff

- Branch: `prototypes/schedule-d-covered-ltcg-8a/it2` (continuing)
- Charter:
  `docs/prototypes/schedule-d-covered-ltcg-8a/charter-review-contract-adversary.md`
- Plan: `docs/prototypes/schedule-d-covered-ltcg-8a/plan.md`
- Review objects: incumbent `d4e2203`, rival `bbecd3f`
- Output: `reviews/contract-adversary.md`
- Evidence ceiling: Rung 1 paper only

## Next action

Owner launches the contract/adversary Reviewer against the exact charter. On
return, the foreman takes custody and charters the isolated expressiveness
review, continuing on the same branch — the reviewer's own charter instructs
it not to read the first review, and the two run as separate agent contexts
in sequence.
