# Rule-Language Prototype — Seat File

This is the execution state of the prototype process. A fresh agent resuming this project takes the seat assigned below; it does not self-assign the foreman seat unless that seat is marked vacant (then it records the succession in `process-log.md`).

Context-starved seats (rival builder, legibility reviewer) are NOT filled by generic resumption: the owner pastes the launch line from the role file into a fresh session.

## Current step

Round 2 — review of the it2 rival build and the comparison against it1. The rival build is complete (branch `prototypes/rule-language/it2`, tip `623957c`); the examination is on `main` (`examination-it2.md`). Three seats are open **now** for fresh agents resuming this project: governance, expressiveness, adversary — scoped by `reviews/round-2.md` (comparative round; contract tightness is an explicit axis). The legibility seat is starved and owner-launched (round-2 launch line in `reviews/round-2.md`). When all four reviews exist, the foreman scores legibility, conformance-checks, and presents the owner disposition.

## Seats

| Seat | Role file | Holder | Status |
|---|---|---|---|
| Foreman | `roles/foreman.md` | claude (session lineage of milestone planning, 2026-07-10) | active |
| Builder it1 | `roles/builder.md` | codex (resume session, 2026-07-10) | complete (branch `prototypes/rule-language/it1` @ `362f8a3`; `examination-it1.md`) |
| Rival builder | `roles/builder-rival.md` | owner-launched clean room (2026-07-10) | complete (branch `prototypes/rule-language/it2` @ `623957c`; `examination-it2.md`) |
| Reviewer: governance | `roles/reviewer-governance.md` | — | **open now** (round 2: `reviews/round-2.md`) |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | — | **open now** (round 2: `reviews/round-2.md`) |
| Reviewer: legibility | `roles/reviewer-legibility.md` | — | **owner-launch now** (round-2 launch line in `reviews/round-2.md`, Legibility scope) |
| Reviewer: adversary | `roles/reviewer-adversary.md` | codex (resume session, 2026-07-10) | active (round 2: comparative review) |

## Next action

Fill the four round-2 seats: governance, expressiveness, adversary by fresh-session resumption (one seat each, first-come); legibility by the owner launch line in `reviews/round-2.md`. Then foreman scoring, conformance check, and owner disposition (iterate/converge vs conclude to evaluation analysis and ADRs).

## Evidence exhibits

- Tag `exhibits/rule-language/it0` — pre-process derivation spike, admitted as exhibit by owner disposition 2026-07-10. Mined by the harvest; not a process-conformant iteration.
- Tag `exhibits/rule-language/it1` — iteration 1 (primary design, expression trees) @ `362f8a3`; concluded by owner disposition 2026-07-10 after round 1. Examination on `main`; reviews under `reviews/round-1*`.
- Branch `prototypes/rule-language/it2` — active rival iteration under review (clean-room build; guarded single-publication clauses, schema-enumerated operations, closed packages, start/completion records); becomes tag `exhibits/rule-language/it2` when the iteration concludes.
