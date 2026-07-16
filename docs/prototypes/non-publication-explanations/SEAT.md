# Non-Publication Explanations Prototype — Seat File

## Current step

Round 3 prepared (2026-07-13, owner-approved): review of the redrafted ADR-0020 (durable Run Disposition Ledger, redraft landed `fc9a855`). Owner launches the two seats from `roles/reviewer-governance-r3.md` and `roles/reviewer-adversary-r3.md`, separate threads. Outputs `reviews/round-3-governance.md` (NPE-G9+) and `reviews/round-3-adversary.md` (NPE-A12+). Foreman triage follows; then the `evaluation-analysis.md` rewrite and owner ratification of ADR-0020.

## Seats

| Role | Holder | Status |
|---|---|---|
| Foreman | Claude, principal foreman (owner-appointed 2026-07-13, relieving previous Codex foreman) | active; owner-paced, no unapproved spawns |
| Incumbent builder | owner-launched external context | completed; branch `prototypes/non-publication-explanations/it1`, exhibit `exhibits/non-publication-explanations/it1` |
| Rival builder | foreman-spawned sub-agent (High tier) | completed; it2 in working tree (uncommitted; owner holds git custody) |
| Governance reviewer | foreman-spawned sub-agent (Medium tier) | rounds 1 and 2 completed |
| Adversary reviewer | foreman-spawned sub-agent (Medium tier) | rounds 1 and 2 completed |

## Next action

Owner: review round-2 triage; decide on evaluation-analysis rewrite and ADR-0020 redraft; commit/tag the it2 exhibit and round-2 documents.
