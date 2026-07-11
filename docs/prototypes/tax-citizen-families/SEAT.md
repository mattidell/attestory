# Tax Citizen Families Prototype - Seat File

This is the execution state for First Tax Slice Track 0. A fresh agent resuming
this project reads this file first when `docs/phase-state.md` points here. Do
not self-assign the foreman seat unless it is marked vacant; record any
succession in `process-log.md`.

Context-starved seats are not filled by generic resumption. The owner launches
them by pasting the launch line from the role file into a fresh session.

## Current Step

**Round 3 is closed; owner disposition is required at the three-iteration
cap.** Iteration 3 remains useful evidence but is not sufficient for the
contract-foundational Tier 2 decision. No fourth iteration, evaluation
analysis, or ADR is open.

## Seats

| Seat | Role file | Holder | Status |
|---|---|---|---|
| Foreman | `roles/foreman.md` | codex (planning session, 2026-07-11) | active |
| Builder it1 | `roles/builder.md` | `codex-builder-it1-2026-07-11` | complete; exhibit `exhibits/tax-citizen-families/it1` |
| Rival builder | `roles/builder-rival.md` | owner-launched clean-room session | complete (`989d9fe`; `examination-it2.md`) |
| Reviewer: governance | `roles/reviewer-governance.md` | `codex-governance-r1-2026-07-11` | round 1 complete |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | `codex-expressiveness-r1-2026-07-11` | round 1 complete |
| Reviewer: adversary | `roles/reviewer-adversary.md` | `codex-adversary-r1-2026-07-11` | round 1 complete |
| Reviewer: legibility | `roles/reviewer-legibility.md` | owner-launched fresh session | round 1 complete |
| Reviewer: governance | `roles/reviewer-governance.md` | `codex-governance-r2-2026-07-11` | round 2 complete |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | `codex-expressiveness-r2-2026-07-11` | round 2 complete |
| Reviewer: adversary | `roles/reviewer-adversary.md` | `codex-adversary-r2-2026-07-11` | round 2 complete |
| Reviewer: legibility | `roles/reviewer-legibility.md` | owner-launched fresh session | round 2 complete |
| Builder it3 | `roles/builder.md` | owner-launched it2 builder session | complete; exhibit `exhibits/tax-citizen-families/it3` |
| Reviewer: governance | `roles/reviewer-governance.md` | `Lovelace` (`019f5384-e415-7691-af20-9fbe46907be3`) | round 3 complete |
| Reviewer: expressiveness | `roles/reviewer-expressiveness.md` | `Nietzsche` (`019f5384-e48f-7403-a906-71a39169e794`) | round 3 complete |
| Reviewer: adversary | `roles/reviewer-adversary.md` | `Hume` (`019f5384-e559-7673-87f9-1fba1b904f68`) | round 3 complete |
| Reviewer: legibility | `roles/reviewer-legibility.md` | owner-launched fresh session | round 3 complete |

## Next Action

Owner decides whether to stop the effort or authorize one bounded integration
proof as iteration 4. The recommended continuation is not another broad domain
prototype: branch from exhibit it3, add no new tax breadth, and require
end-to-end evidence for authoritative projection, package/provenance joins,
record-derived coverage and explanations, correction lifecycle, citation-role
validation, and committed relationship negatives. Per owner instruction, the
foreman does not spawn a builder subagent.

## Planned Exhibits

- Tag `exhibits/tax-citizen-families/it1` - first candidate contract at
  `88f0139`.
- Tag `exhibits/tax-citizen-families/it2` - clean-room rival at `989d9fe`.
- Tag `exhibits/tax-citizen-families/it3` - targeted repair candidate at
  `be72d63`.
