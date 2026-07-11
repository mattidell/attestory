# Rule-Language Prototype — Seat File

This is the execution state of the prototype process. A fresh agent resuming this project takes the seat assigned below; it does not self-assign the foreman seat unless that seat is marked vacant (then it records the succession in `process-log.md`).

Context-starved seats (rival builder, legibility reviewer) are NOT filled by generic resumption: the owner pastes the launch line from the role file into a fresh session.

## Current step

Iteration 2 — the rival build (owner disposition 2026-07-10: it1 concluded and tagged `exhibits/rule-language/it1`; rival proceeds on the same charter). The rival-builder seat is **starved and owner-launched only** — a fresh agent resuming this project must NOT take it; if you resumed generically and read this file, you are not eligible for the rival seat. There is no other open seat; generically-resumed agents should stop and report.

For the rival builder (arrives via launch line, reads only what it permits): the charter is `docs/prototypes/rule-language/charter-it1.md` (v2 — it is the shared exam for both designs despite the it1 name); the harvest notes are `docs/prototypes/rule-language/harvest-notes.md`; your branch is `prototypes/rule-language/it2`.

## Seats

| Seat | Role file | Holder | Status |
|---|---|---|---|
| Foreman | `roles/foreman.md` | claude (session lineage of milestone planning, 2026-07-10) | active |
| Builder it1 | `roles/builder.md` | codex (resume session, 2026-07-10) | complete (branch `prototypes/rule-language/it1` @ `362f8a3`; `examination-it1.md`) |
| Rival builder | `roles/builder-rival.md` | — | **owner-launch now** (launch line in `roles/builder-rival.md`; branch `prototypes/rule-language/it2`) |
| Reviewer: governance | `roles/reviewer-governance.md` | — | not yet open (round 2 needs rival artifacts) |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | — | not yet open (round 2 needs rival artifacts) |
| Reviewer: legibility | `roles/reviewer-legibility.md` | — | not yet open (round 2; relaunched fresh per round) |
| Reviewer: adversary | `roles/reviewer-adversary.md` | codex (resume session, 2026-07-10) | complete (round 1: `reviews/round-1-adversary.md`) |

## Next action

Owner launches the rival builder (launch line in `roles/builder-rival.md`; first message of a fresh session, ideally a different model family than the it1 builder). When the rival examination lands: foreman assembles round 2.

Round-1 record: reviews and scoring under `reviews/round-1*`; verdicts were unanimous — proceed to rival, do not ratify it1 as-is. Round-2 lenses: contract tightness (schema-declared expression grammar, package closure, output ownership, record linkage, year identity) joins legibility as an explicit comparison axis.

## Evidence exhibits

- Tag `exhibits/rule-language/it0` — pre-process derivation spike, admitted as exhibit by owner disposition 2026-07-10. Mined by the harvest; not a process-conformant iteration.
- Tag `exhibits/rule-language/it1` — iteration 1 (primary design, expression trees) @ `362f8a3`; concluded by owner disposition 2026-07-10 after round 1. Examination on `main`; reviews under `reviews/round-1*`.
