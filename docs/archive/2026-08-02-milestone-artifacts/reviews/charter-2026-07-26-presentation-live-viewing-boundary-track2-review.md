# Charter — Track 2 review: confined vehicle and fail-closed preflight

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/presentation-live-viewing-boundary.md`
- Build charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-26-presentation-live-viewing-boundary-track2.md`
- Under review: `d8083f9` on `track/presentation-live-viewing-boundary-track2`
  (`packages/derivation/live_viewing.py`, `tests/test_presentation_live_viewing_vehicle.py`)
- Governing decision: **ADR-0047** (accepted). Its four-class classification is
  the specification.

The build charter's verification block was run at hand-off and passed: focused
module 9 tests, `tests.test_presentation_l2_integration` 29 tests, both harness
manifests, `envelope_scan --range main..HEAD` silent, `git diff --check` clean.
Re-run to confirm, but spend the review on the measurements below rather than on
re-establishing that the suite is green.

## Measurements

1. **Locator containment is total.** The charter made this a test obligation,
   not a convention. Read every path the locator could reach a human or a file:
   return values, log records, exception messages and their `args`, `repr`/`str`
   of any dataclass or enum, assertion failure output, and test fixtures. A
   confinement check naturally reports the offending path; confirm this one
   cannot, including on the failure paths the tests do not exercise. Verify the
   reason codes are stable identifiers that carry no fragment of the locator.

2. **Fail-closed is total, with no third outcome.** ADR-0031 D2: uncertainty is
   a rejection. For each covered precondition, confirm an unreadable, missing,
   erroring, or indeterminate probe result yields refusal — not a pass, not a
   warning, not a skip. Confirm there is no advisory mode and no override.

3. **Class B confinement is actually by construction.** Profile, cache,
   downloads, and print destination all resolve inside the capability-supplied
   workspace; canonicalization defeats symlink escape; there is no default, no
   environment fallback, and no caller-supplied path. Check what happens when
   the capability is absent, empty, or malformed.

4. **Claim discipline.** No artifact — code, comment, docstring, test name,
   reason code — may read as claiming egress prevention, or as claiming the
   clipboard-history check is complete. Non-loopback refusal is
   accidental-leakage reduction only. Confirm no enforcement substrate was
   implemented or wired.

5. **Teardown on every exit path.** The suite covers launch failure. Determine
   whether teardown also holds on the other exits — refusal after partial
   construction, exception mid-session, and normal close — and whether anything
   outside the workspace can be removed.

6. **Scope.** No real workspace is touched, the `synthetic: true` evaluation
   boundary is unweakened, `chrome.mjs` is unmodified, and the vehicle is not
   reusable as an evaluation path. Presentation is still claimed at L2.

## Verdict

`READY` or `NOT READY` with numbered observations, each tied to a measurement
and marked blocking or non-blocking. Record at
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-26-presentation-live-viewing-boundary-track2-review.md`'s
sibling result file per the seat file's convention.

## Data safety

No absolute local path in the review, a PR body, or chat. Run
`python3 tools/envelope_scan.py --range main..HEAD` before handing back.
