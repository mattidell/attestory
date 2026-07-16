# Process Log — D2 Contribution Boundary

Topic branch: `decision/d2-contribution` (foreman git custody; merges once at
ratification per ADR-0030). Candidate ADR-0032. Interlocks with D1 (ADR-0031,
ratified) — a contribution writes into the ratified residency boundary.

| When | Event |
|---|---|
| 2026-07-16 | Plan approved by owner (PR #4, merged `548318b`). |
| 2026-07-16 | Charters authored: `charter-it1.md` (incumbent, High), `charter-it2.md` (clean-room rival, High). **Awaiting dispatch.** |
| 2026-07-16 | Both builder artifact pairs landed under foreman custody at `32de94d`. Incumbent examination: 117 lines; rival examination: 107 lines (both within the 120-line examination cap). Rival examination attests the clean-room seal held. |
| 2026-07-16 | **Foreman error / fixed-cap incident:** the plan's 900-line total-topic Markdown cap is crossed: 1,102 lines before the required D2 seat record. The charters did not make a seat file before builder receipt. Per Gate 4, stop-and-decide; no committee dispatch pending owner disposition. |

## Round 1 seats

| Seat | Tier | Context | Charter | Status |
|---|---|---|---|---|
| Incumbent builder | High | independent | `charter-it1.md` | complete (`32de94d`) |
| Rival builder | High | independent, sealed | `charter-it2.md` | complete (`32de94d`; seal attested) |

## Delivered (Round 1)

- `it1/design.md` + `examination-it1.md` (117-line examination)
- `it2/design.md` + `examination-it2.md` (107-line examination)

## Next foreman action

Hold for the owner's Gate-4 cap disposition. On direction to proceed,
triage-classify the builder-reported findings (Gate 5), confirm process
conformance, then dispatch the Round-1 committee — Governance (Medium) +
Adversary (High) — in independent contexts under the plan's standing
authorization. Do not review artifact quality; triage and route only.
