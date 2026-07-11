# Rule-Language Prototype — Seat File

This is the execution state of the prototype process. A fresh agent resuming this project takes the seat assigned below; it does not self-assign the foreman seat unless that seat is marked vacant (then it records the succession in `process-log.md`).

Context-starved seats (rival builder, legibility reviewer) are NOT filled by generic resumption: the owner pastes the launch line from the role file into a fresh session.

## Current step

Round 1 — review of the it1 build. The build is complete (branch `prototypes/rule-language/it1`, tip `362f8a3`); the examination is on `main` (`examination-it1.md`). One seat is open **now** for fresh agents resuming this project: adversary — scoped by `reviews/round-1.md`. The legibility seat is starved and owner-launched (launch line in `reviews/round-1.md`). When all four reviews exist, the foreman scores legibility, conformance-checks, and presents the owner disposition.

## Seats

| Seat | Role file | Holder | Status |
|---|---|---|---|
| Foreman | `roles/foreman.md` | claude (session lineage of milestone planning, 2026-07-10) | active |
| Builder it1 | `roles/builder.md` | codex (resume session, 2026-07-10) | complete (branch `prototypes/rule-language/it1` @ `362f8a3`; `examination-it1.md`) |
| Rival builder | `roles/builder-rival.md` | — | not yet open (starved seat; launch line in role file) |
| Reviewer: governance | `roles/reviewer-governance.md` | codex (resume session, 2026-07-10) | complete (round 1: `reviews/round-1-governance.md`) |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | codex (resume session, 2026-07-10) | complete (round 1: `reviews/round-1-expressiveness.md`) |
| Reviewer: legibility | `roles/reviewer-legibility.md` | — | **owner-launch now** (round 1 launch line in `reviews/round-1.md`, Legibility scope) |
| Reviewer: adversary | `roles/reviewer-adversary.md` | — | **open now** (round 1: `reviews/round-1.md`; round-0 work complete: `reviews/round-0-adversary.md`, `-delta.md`) |

## Next action

Fill the remaining round-1 seats: adversary by fresh-session resumption; legibility by the owner launch line in `reviews/round-1.md`. Then foreman scoring, conformance check, and owner disposition.

## Evidence exhibits

- Tag `exhibits/rule-language/it0` — pre-process derivation spike, admitted as exhibit by owner disposition 2026-07-10. Mined by the harvest; not a process-conformant iteration.
- Branch `prototypes/rule-language/it1` — active iteration under review; becomes tag `exhibits/rule-language/it1` when the iteration concludes.
