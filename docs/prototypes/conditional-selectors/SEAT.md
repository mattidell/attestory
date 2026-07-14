# Conditional Selectors Prototype — Seat File

## Current step

**Round 1R complete and triaged** (`round-1r-triage.md`, 2026-07-13). Both independent seats: Shape A conditionally accept, Shape B reject as specified — inverting the tainted process's outcome. Pending owner decisions: ADR-0019 disposition (foreman recommends rejected status, retained), rival-builder charter in the Shape A family, evaluation-analysis rewrite.

## Seats

| Role | Holder | Status |
|---|---|---|
| Foreman | Claude, principal foreman (owner-appointed 2026-07-13, relieving previous Codex foreman) | active; owner-paced, no unapproved spawns |
| Incumbent builder | owner-launched external context | completed; it1 exhibit `exhibits/conditional-selectors/it1`, repair1 branch `prototypes/conditional-selectors/repair1` |
| Rival builder | owner-launched external context | completed; it2 exhibit committed `a6982e6` |
| Governance reviewer (round 1R) | owner-launched external context | completed 2026-07-12; `reviews/round-1r-governance.md` |
| Adversary reviewer (round 1R) | foreman-spawned sub-agent (Medium tier, owner go 2026-07-13) | completed; `reviews/round-1r-adversary.md` |

## Next action

Round 2R (committee over it2) prepared: owner launches the two seats from `roles/reviewer-governance-r2.md` and `roles/reviewer-adversary-r2.md`, separate threads, within-round independence. Outputs `reviews/round-2r-governance.md` (CS-G8R+) and `reviews/round-2r-adversary.md` (CS-A10R+). Foreman triage, then evaluation-analysis rewrite, follow; the optional-input absence question is a candidate separate Tier-2 decision. (Post-merge reconciliation review of Source Completeness is owner-launched and in flight, out of this topic.)
