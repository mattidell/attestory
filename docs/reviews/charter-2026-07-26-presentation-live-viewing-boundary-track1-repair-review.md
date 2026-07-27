# Charter — Track 1 focused recheck: ADR-0047 repair

- Role: **Reviewer** (`docs/roles/reviewer.md`) — the same Reviewer who issued
  `docs/reviews/2026-07-26-presentation-live-viewing-boundary-track1-review.md`
- Milestone: `docs/phases/real-return/milestones/presentation-live-viewing-boundary.md`
- Branch: `track/presentation-live-viewing-boundary-track1`
- Repair commit: `52ef7b0` (reviewed commit was `498c396`; review was `b1a630a`)

This is a **focused recheck**, not a second full review. Scope is Finding 1,
Observation 1, and the invariants the repair directly touched. Do not re-derive
measurements 1, 3, 4, or 5 except where the repair's diff reaches them.

## What the repair claims to have done

**Finding 1 — clipboard-history retention unclassified.**

- Class A is now explicitly bounded to the deliberate act with an intended
  destination; retention of that act is assigned to Class D.
- Class D enumerates clipboard-history retention and names it the third
  silently-fatal precondition alongside indexing and backup.
- The precondition disposition splits it: refuse where detectable, named owner
  responsibility where not, with partial detectability given as the stated
  reason it is listed apart from the two the preflight must always decide.
- Attestation condition 3 now covers a copy with no subsequent paste; condition
  4 names undetectable clipboard, sync, and recording software.

**Observation 1 — Class C overclaimed platform impossibility.** Class C now
states the class is open because no substrate has been selected or evaluated,
names Seatbelt/`sandbox-exec` as an unevaluated live candidate that a later
milestone should not read as foreclosed, and narrows the load-bearing claim to
"a cooperative same-UID mechanism is not a trust boundary."

The milestone plan's classification table, scope item 4, preflight contract, and
exit criterion 3, and the `0047` INDEX row, were updated to match.

## Measurements

`READY` requires all five.

1. **Finding 1 closed.** Clipboard-history retention is classified exactly once,
   in Class D, and the Class A boundary now excludes background retention
   without creating a new ambiguity about where a deliberate paste belongs.
2. **Totality preserved.** The repair does not open a new unclassified
   remainder. Re-probe the taxonomy for a channel of the same shape as the one
   you found — background software that silently converts an in-session act into
   a durable record outside the residency. State plainly if another survives.
3. **Split disposition is honest, not a loophole.** The refuse-where-detectable
   / owner-responsibility-where-not treatment must not become a route by which a
   partially-checked precondition reads as discharged. Confirm the ADR and plan
   both state that a passing clipboard check is not a completeness claim, and
   that the two always-decidable preconditions retain their unconditional
   refusal.
4. **Observation 1 addressed without overcorrection.** Class C must not now
   imply that a substrate is available, endorsed, or scheduled. Confirm it
   selects and evaluates none, that Presentation remains L2 and the data
   boundary L3, and that the narrowed Guarded Transport claim still supports
   rejecting the vehicle-first shape — the milestone's whole premise rests on
   it.
5. **Consistency across surfaces.** ADR, analysis, milestone plan, and INDEX row
   agree. No surface retains the superseded four-class wording or the
   platform-impossibility phrasing.

## Data safety

`python3 tools/envelope_scan.py --range main..HEAD` and `git diff --check`. No
residency locator, path fragment, or owner-local identifier in any changed file.

## Verdict

Return `READY` or `NOT READY` with the smallest exact residual. The plan's
repair cap is now spent; a further `NOT READY` returns to the Foreman for owner
direction rather than another repair.

Record at
`docs/reviews/2026-07-26-presentation-live-viewing-boundary-track1-repair-review.md`.
