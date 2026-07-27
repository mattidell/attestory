# Charter — Track 2 focused recheck

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Milestone: `docs/phases/real-return/milestones/presentation-live-viewing-boundary.md`
- Prior review: `docs/reviews/2026-07-26-presentation-live-viewing-boundary-track2-review.md` (NOT READY, Finding 1)
- Repair commit: on `track/presentation-live-viewing-boundary-track2`, applied by
  the Foreman rather than a Builder round — the finding recommended a test-only
  repair and the owner's standing instruction is to fix rather than charter.

This is a **focused** recheck. Measurements 1, 3, 4, 5, and 6 passed on
independent verification and are not reopened. Do not re-review the module.

## Measurements

1. **Finding 1 is closed.** A test now exercises `run_viewing_preflight` with a
   confirmed-`ABSENT` clipboard probe and asserts the owner-responsibility code
   is still attached. Confirm it asserts the tuple's *content*, not merely that
   the session is allowed — an allowed-only assertion would not catch the
   regression the finding described.

2. **The guard actually bites.** The Foreman ran the mutation the finding
   predicted (gating `owner_responsibilities` on `clipboard is not
   ProbeState.ABSENT`) and observed exactly one test fail, then restored the
   module. Reproduce this independently rather than accepting the report. A
   regression guard that passes under the mutation it exists to catch is worse
   than none.

3. **The repair is test-only and nothing else moved.** `git diff` against the
   reviewed build commit touches only the test module. Production behavior is
   byte-identical to what measurements 1 and 3–6 passed against, so those
   verdicts still stand. Confirm this rather than assume it.

4. **Non-blocking observation 2 is closed without scope creep.** A
   `LiveViewingVehicle.launch()`-level test now refuses a `None` capability and
   asserts no process is spawned. Confirm it adds no production code and makes
   no claim beyond refusal.

Non-blocking observation 1 (`__context__` retention) is deliberately **not**
addressed. It was a docstring suggestion conditional on the file being touched
again, and the file was not touched. Confirm this is the right disposition or
say so.

## Verdict

`READY` or `NOT READY`, numbered against the four measurements above.

## Data safety

`python3 tools/envelope_scan.py --range main..HEAD` before handing back. No
absolute local path in the record, a PR body, or chat.
