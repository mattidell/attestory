# Adopted-Content Manifests Prototype — Seat File

## Current step

Both builder exhibits conformant and committed. Committee round-1 **partial**:
Adversary review under custody (`reviews/round-1-adversary.md`, ACM-A1–A7).
**Governance review still missing** — owner-launched seats exited before writing
`reviews/round-1-governance.md`. Owner relaunches Governance only (fresh independent
context) from `roles/reviewer-governance.md`. Do not share the adversary review
with the governance seat (independence exclusion). After governance lands under
custody, foreman triage → `evaluation-analysis.md` → ADR-0027 draft.

## Seats

| Role | Holder | Status |
|---|---|---|
| Foreman | principal foreman (owner-appointed) | active; owner-paced, no unapproved spawns |
| Incumbent builder | owner-launched external context | completed — `it1/` |
| Rival builder | owner-launched external context | completed — `it2/` |
| Governance reviewer | owner-launched external context | **chartered — relaunch required** (prior seats exited without delivery) |
| Adversary reviewer | owner-launched external context | **completed** — `reviews/round-1-adversary.md` |

## Next action

Owner: relaunch **Governance only** from `roles/reviewer-governance.md` (separate
context; do not pass adversary output). Drop `reviews/round-1-governance.md`
(ACM-G*) for foreman custody. Adversary is done; do not relaunch Adversary.
