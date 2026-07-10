# Rule-Language Prototype — Seat File

This is the execution state of the prototype process. A fresh agent resuming this project takes the seat assigned below; it does not self-assign the foreman seat unless that seat is marked vacant (then it records the succession in `process-log.md`).

Context-starved seats (rival builder, legibility reviewer) are NOT filled by generic resumption: the owner pastes the launch line from the role file into a fresh session.

## Current step

Round 0 — delta confirmation. Owner disposition (2026-07-10): charter amended to v2 with all ten review findings; the dissenting adversary delta-confirms the amendment. One seat is open **now**: adversary delta-confirmation (bounded scope — see "Delta confirmation" in `reviews/round-0.md`). A fresh agent resuming this project takes that seat. On dissent withdrawal (or owner override), the foreman opens the it1 builder seat.

## Seats

| Seat | Role file | Holder | Status |
|---|---|---|---|
| Foreman | `roles/foreman.md` | claude (session lineage of milestone planning, 2026-07-10) | active |
| Builder it1 | `roles/builder.md` | — | not yet open (opens after charter disposition) |
| Rival builder | `roles/builder-rival.md` | — | not yet open (starved seat; launch line in role file) |
| Reviewer: governance | `roles/reviewer-governance.md` | codex (resume session, 2026-07-10) | complete (round 0, charter review: `reviews/round-0-governance.md`) |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | — | not yet open (needs artifacts) |
| Reviewer: legibility | `roles/reviewer-legibility.md` | — | not yet open (starved seat; launch line in role file) |
| Reviewer: adversary | `roles/reviewer-adversary.md` | codex (resume session, 2026-07-10) | **open now**: delta-confirmation of charter v2 (`reviews/round-0.md`, Delta confirmation) |

## Next action

Fill the adversary delta-confirmation seat (fresh session; generic resumption dispatches here). On dissent withdrawal: foreman opens the it1 builder seat.

## Evidence exhibits

- `prototypes/rule-language/it0` — pre-process derivation spike, admitted as exhibit by owner disposition 2026-07-10. Mined by the harvest; not a process-conformant iteration.
