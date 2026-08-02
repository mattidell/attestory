# Presentation — Live Viewing Boundary Track 2 Focused Recheck

Status: **READY**
Date: 2026-07-26
Role: independent Reviewer (same Reviewer as the Track 2 review)
Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-26-presentation-live-viewing-boundary-track2-recheck.md`

## Capsule echo (pre-recheck)

| Item | Resolved value |
| --- | --- |
| **Source ref** | `track/presentation-live-viewing-boundary-track2`, current at `fa47e16`. Repair commit under recheck: `fa47e16` (prior review: `974bbac`, `NOT READY`, Finding 1). |
| **Repair author** | Foreman, applied directly — the finding recommended a test-only repair and the owner's standing instruction is to fix rather than charter a Builder round for this shape of fix. |
| **Scope** | Focused: only Finding 1's closure, the regression-guard mutation, test-only-ness of the diff, and Observation 2's closure. Measurements 1, 3, 4, 5, 6 from the original review are not reopened. |

## Measurements

| # | Measurement | Result |
| --- | --- | --- |
| 1 | Finding 1 is closed: a test exercises `run_viewing_preflight` with a confirmed-`ABSENT` clipboard probe and asserts the owner-responsibility code's *content*, not merely that the session is allowed. | **Pass.** `test_confirmed_absent_clipboard_is_still_not_a_clearance` (`tests/test_presentation_live_viewing_vehicle.py`) calls `run_viewing_preflight` with `PreflightProbes(False, False, False)` and asserts `absent.owner_responsibilities == (ViewingReason.CLIPBOARD_HISTORY_UNDETECTABLE.value,)` — an equality check on the tuple's content, not an `assertTrue(absent.allowed)`-only check. This is exactly the assertion strength the finding required; a weaker allowed-only check would not have caught the predicted regression (confirmed independently under measurement 2 below). |
| 2 | The guard actually bites: the predicted mutation (gating `owner_responsibilities` on `clipboard is not ProbeState.ABSENT`) causes exactly one test to fail. | **Pass, independently reproduced.** I applied the mutation myself (not from the Foreman's report) — replaced the unconditional `owner_responsibilities=(...)` with a conditional expression yielding `()` when `clipboard is ProbeState.ABSENT` — and ran `python3 -m unittest tests.test_presentation_live_viewing_vehicle`. Result: 11 tests run, exactly 1 failure, and it is `test_confirmed_absent_clipboard_is_still_not_a_clearance` (`AssertionError: Tuples differ: () != ('viewing-clipboard-history-undetectable-remainder',)`). All 10 other tests still passed under the mutation, so the guard is neither too weak (it fires) nor accidentally coupled to unrelated behavior (nothing else broke). The file was restored to its committed state immediately after (`git status --short` confirms clean; the restored suite reruns 11/11 pass). |
| 3 | The repair is test-only; production behavior is byte-identical to what measurements 1 and 3–6 already passed against. | **Pass, confirmed rather than assumed.** `git diff 974bbac..fa47e16 --stat` touches only `tests/test_presentation_live_viewing_vehicle.py` (+25 lines), plus `docs/phase-state.md` and the recheck charter itself — `packages/derivation/live_viewing.py` does not appear in the diff at all. Since the module under review is byte-unchanged, the original review's measurements 1 (locator containment), 3 (Class B confinement), 4 (claim discipline), 5 (teardown), and 6 (scope) stand without re-verification. |
| 4 | Observation 2 is closed without scope creep: a `LiveViewingVehicle.launch()`-level test refuses a `None` capability and asserts no process is spawned, adding no production code and no claim beyond refusal. | **Pass.** `test_launch_refuses_a_missing_capability_and_spawns_nothing` calls `vehicle.launch(None, chrome_executable="/nonexistent", launch_timeout_seconds=0.2)` with a `process_factory` that raises `AssertionError("no process may be spawned without a capability")` if ever invoked — so the test fails loudly if a process is spawned, not merely if the exception is missing — and asserts `caught.exception.args == (ViewingReason.CAPABILITY_UNAVAILABLE.value,)`. This adds a test only (confirmed under measurement 3's diff-stat) and asserts exactly refusal-plus-no-spawn, no broader claim. |

**Non-blocking observation 1 disposition.** The charter states `__context__` retention was left unaddressed because it was a conditional docstring suggestion ("worth a one-line note... if this file is touched again") and the file was not touched. I agree this is the right disposition: measurement 3 confirms the module is byte-identical, so the stated condition for revisiting it did not arise, and re-opening a non-blocking, already-dispositioned observation on a recheck that is charter-scoped to Finding 1 alone would be scope creep in the other direction — inventing a delta requirement the recheck charter does not name.

## Data safety

`python3 tools/envelope_scan.py --range main..HEAD` — exit 0, no output. `git diff --check main..HEAD` — exit 0, no output. No residency locator, path fragment, or owner-local identifier in the changed test file.

## Verdict

**READY.** All four charter measurements pass on independent verification, including an independent reproduction of the regression-guard mutation (not accepted from the Foreman's self-report) that confirms the guard fires on exactly the predicted failure and nothing else. The repair is test-only and the reviewed module's production behavior is unchanged, so the original review's other five measurements stand undisturbed. Track 2's review-and-repair stage is complete.
