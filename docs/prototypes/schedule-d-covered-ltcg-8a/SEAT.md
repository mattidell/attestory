# Covered Long-Term Gains, Schedule D Line 8a — Seat File

## Current step

The contract/adversary review returned `NOT READY` with four decision-blocking
findings (CA-01 through CA-04) and three separate-decision prerequisites
(CA-05 through CA-07). The expressiveness review is now chartered, pinned to
the same exact objects, independently of the first review's findings.

## Seats

| Role | Holder | Status |
| --- | --- | --- |
| Foreman | Current foreman thread | Active; scope/economy and custody only |
| Incumbent Builder | Returned on `prototypes/schedule-d-covered-ltcg-8a/it1` | Complete; outputs at `it1/design.md`, `it1/examination.md` (commit `d4e2203`) |
| Rival Builder | Returned on `prototypes/schedule-d-covered-ltcg-8a/it2` | Complete; outputs at `it2/design.md`, `it2/examination.md` (reviewed object `bbecd3f`; a later non-substantive grounding-citation commit `e52710c` sits in the branch but was excluded from both reviews' evidence) |
| Contract/adversary Reviewer | Returned on `prototypes/schedule-d-covered-ltcg-8a/it2` | Complete; `NOT READY`. `docs/prototypes/schedule-d-covered-ltcg-8a/reviews/contract-adversary.md` (commit `4fa6c10`). Findings CA-01/02/03/04 decision-blocking; CA-05/06/07 separate-decision prerequisites |
| Expressiveness Reviewer | Owner-launched context on `prototypes/schedule-d-covered-ltcg-8a/it2` (continuing branch) | Chartered; not yet launched |
| Repair Builder | Unassigned | Not chartered; owner direction required after both reviews and Gate-5 triage |

## Binding handoff

- Branch: `prototypes/schedule-d-covered-ltcg-8a/it2` (continuing)
- Charter:
  `docs/prototypes/schedule-d-covered-ltcg-8a/charter-review-expressiveness.md`
- Plan: `docs/prototypes/schedule-d-covered-ltcg-8a/plan.md`
- Review objects (pinned, same as first review): incumbent `d4e2203`, rival
  `bbecd3f`
- Output: `reviews/expressiveness.md`
- Evidence ceiling: Rung 1 paper only

## Next action

Owner launches the expressiveness Reviewer against the exact charter. On
return, the foreman takes custody, compares both sealed reviews, and performs
Gate-5 finding triage before recommending a disposition (repair, partial
ratification, or recharter) to the owner.
