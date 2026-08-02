# Covered Long-Term Gains, Schedule D Line 8a — Seat File

## Current step

Repair 1 is independently confirmed `READY` (CA-02 and CA-04 both confirmed,
regression boundary intact). Track 0's evidence chain is complete. Contract
synthesis is chartered on a fresh decisions branch to draft the proposed
successor ADR.

## Seats

| Role | Holder | Status |
| --- | --- | --- |
| Foreman | Current foreman thread | Active; scope/economy and custody only |
| Incumbent Builder | Returned on `prototypes/schedule-d-covered-ltcg-8a/it1` | Complete; not carried forward |
| Rival Builder | Returned on `prototypes/schedule-d-covered-ltcg-8a/it2` | Complete; selected topology |
| Contract/adversary Reviewer | Returned | Complete; `NOT READY`. `reviews/contract-adversary.md` (`4fa6c10`) |
| Expressiveness Reviewer | Returned | Complete; `READY` for rival. `reviews/expressiveness.md` (`8d8811f`) |
| Repair Builder | Returned | Complete; `repair1/design.md`, `repair1/examination.md` (`e6747fd`) |
| Confirmation Reviewer | Returned | Complete; `READY`. `reviews/repair1-confirmation.md` (`b6dabec`) |
| Contract Synthesis Builder | Owner-launched context on `decisions/schedule-d-covered-ltcg-8a` (new branch, cut from `origin/main`) | Chartered; not yet launched |

## Binding handoff

- Branch: `decisions/schedule-d-covered-ltcg-8a` (new, cut from `origin/main`
  at `a05d637` — separate from the `it1`/`it2` prototype branches)
- Charter:
  `docs/prototypes/schedule-d-covered-ltcg-8a/charter-contract-synthesis.md`
- Full evidence chain: `it1/`, `it2/`, `repair1/`, `reviews/`,
  `round-1-triage.md`, all on `prototypes/schedule-d-covered-ltcg-8a/it1` and
  `it2`
- Outputs: `evaluation-analysis.md`, `docs/adr/0052-covered-long-term-gains-schedule-d-line-8a.md`,
  `docs/adr/INDEX.md` (one appended row)

## Next action

Owner launches the Contract Synthesis Builder against the exact charter. On
return, the foreman takes custody, prepares the ADR for owner review and
ratification (the merge to `main` is the ratification record), then closes
out Track 0 and hands off to the milestone's production tracks (1-4).
