# Charter: Track 0a Repair Delta — Independent Re-Review

Date: 2026-07-19. Prepared by the foreman; dispatched under the owner's
standing authorization for this continuation. The reviewer is
author-independent of the repair: it verifies the foreman's repair commit
against the original review's findings, not against the foreman's account of
them.

## Object under review

The repair delta `18b2f9e..595c4e1` on `codex/dsbs-t0a-cmdn-production`
(one commit, "repair: discharge Track 0a review findings F1-F4"), read
against the original review
(`docs/reviews/2026-07-19-dsbs-t0a-cmdn-review.md`) and its charter
(`docs/reviews/charter-2026-07-19-dsbs-t0a-cmdn-review.md`).

## Scope

This is a **delta re-check**, not a fresh full review. The original review's
passing checks (1a-partial, 1b, 1c, 2, 3-property, 4, 5, 6, 7) stand unless
the repair delta itself disturbs them. Verify exactly:

1. **F1 discharged.** Three new committed negative fixtures malform
   `conditional_dependency_set`'s own fields (missing `condition`, non-array
   `members`, member missing `name`) — not merely an unknown op — and an
   executed test asserts schema rejection of all five negatives.
2. **F2 discharged.** CMDN paper case 5 (contribution ladder, member
   supersession, successor pin displacement, and loss of currency for the
   earlier published consumer via the existing derivation edges) and case 6
   (a mutation replacing the declared node with a hand-authored missing list
   is refused before any record exists) both enter through
   `live_coordinate_run` from an authoritative act log — no `RunContext`
   shortcut on the repaired paths. Confirm the case-6 refusal is the byte
   boundary doing the work, and that the test asserts absence of a record
   stream, not just a refusal object.
3. **F3 discharged.** An executed mutation test starts from a published
   finding, strips an active member pin (and the condition pin), and asserts
   rejection by the committed content-identity derivation — including the
   positive control that the intact finding verifies.
4. **F4 discharged.** The widened `_iter_ref_names` reachability walk is now
   scoped to `rule-artifact.v3`; v1/v2 edge computation is byte-identical to
   the pre-track behavior, and no existing golden changed.
5. **No collateral damage.** The delta touches nothing outside the four
   findings; scope fence and boundary discipline hold (all new fixtures are
   `demo-*` synthetic).
6. **Battery re-run.** Full `.venv/bin/python3 -m unittest`, `-m mypy`,
   `tools/governance_lint.py`, and `tools/envelope_scan.py --range
   main..HEAD` — re-run, not trusted. If the venv 127s, rebuild from
   `requirements.txt`.

## Verdict

Append a dated delta-re-review section or new file
(`docs/reviews/2026-07-19-dsbs-t0a-delta-rereview.md`) with an explicit
`ready` / `not ready` verdict for the track as a whole (original review +
this delta), findings numbered R1… . The owner holds the merge (ADR-0030).
