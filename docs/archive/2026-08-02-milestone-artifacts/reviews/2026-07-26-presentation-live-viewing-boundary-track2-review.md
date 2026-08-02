# Presentation — Live Viewing Boundary Track 2 Review Gate

Status: **NOT READY**
Date: 2026-07-26
Role: independent Reviewer
Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-26-presentation-live-viewing-boundary-track2-review.md`

## Capsule echo (pre-review)

| Item | Resolved value |
| --- | --- |
| **Source ref** | `track/presentation-live-viewing-boundary-track2`, resolved and verified at `fda54df` (build commit under review: `d8083f9`, based on `main` at `b37c536`, which carries Track 1's merged ADR-0047). |
| **Exact object** | `packages/derivation/live_viewing.py` (new, 475 lines) and `tests/test_presentation_live_viewing_vehicle.py` (new, 198 lines). `git diff main..HEAD --stat` confirms no other product file changed; `tools/presentation_harness/lib/{chrome,server,manifest}.mjs` and both demo manifests/pages are byte-unchanged. |
| **Role** | One independent Reviewer. |
| **Scope** | The confined headed invocation vehicle and fail-closed preflight only, against ADR-0047's four-class specification. No real workspace, no enforcement substrate, no renderer/ADR-0046 change. |
| **Stop conditions** | None tripped: no published schema/citizen, substrate implementation, real workspace, or ADR-0047 classification change was found or required to complete the review. |

Independently reran the build charter's verification block rather than accepting the hand-off report, then read `packages/derivation/live_viewing.py` and its test file fresh, without seeking the Builder's own account of what it proves.

## Verification rerun

- `python3 -m unittest tests.test_presentation_live_viewing_vehicle` — 9/9 pass.
- `python3 -m unittest tests.test_presentation_l2_integration` — 29/29 pass.
- `node tools/presentation_harness/run.mjs --manifest .../citation-walk.v1.json` — 26 pass, 0 fail.
- `node tools/presentation_harness/run.mjs --manifest .../citation-walk-production-shaped.v1.json` — 19 pass, 0 fail.
- `python3 tools/envelope_scan.py --range main..HEAD` — exit 0, no output.
- `git diff --check main..HEAD` — exit 0, no output.

## Measurements

| # | Measurement | Result |
| --- | --- | --- |
| 1 | Locator containment is total across return values, logs, exception messages/`args`, `repr`/`str`, assertion output, and untested failure paths. | **Pass.** `LiveViewingError.__init__` stores only `reason.value` (a static `ViewingReason` string) as the exception's `args`; `str()`/`repr()` never include a path. Every `except` clause that could catch a path-bearing `OSError` (`_confined_destinations`, `_make_destinations`, `_remove_session`, `LiveViewingVehicle.launch`) converts unconditionally to a `LiveViewingError` via `raise ... from None`, discarding the original message from all `str`/`repr`/traceback-printed surfaces. No `print`, `logging`, or f-string ever interpolates a `Path` into anything raised or returned. `grep` confirms no logging/print calls in the module at all. (Non-blocking note below on `__context__` retention.) |
| 2 | Fail-closed is total, with no third outcome, for each covered precondition, including indeterminate probe results. | **Fail — see Finding 1.** Backup and content-indexing are correctly total by direct inspection and by test (`test_always_decidable_preconditions_are_fail_closed`, `test_unreadable_observer_is_a_refusal`): any state other than `ABSENT` refuses. Clipboard-history's split disposition is implemented correctly by inspection (the `owner_responsibilities` code is attached whenever the session is allowed, regardless of whether the probe returned `ABSENT` or `UNKNOWN`/`UNREADABLE` — never silently upgraded to a clearance) but this exact invariant, the one the milestone's two prior repair cycles were about, has no test covering the explicit-`ABSENT` input. |
| 3 | Class B confinement is actually by construction: profile/cache/downloads/print resolve inside the capability workspace; canonicalization defeats symlink escape; no default, env fallback, or caller-supplied path; behavior when the capability is absent, empty, or malformed. | **Pass, with a non-blocking coverage note.** `_confined_destinations` computes every destination from `capability.location.resolve(strict=True)` alone, checks `_within()` against the canonicalized root for each, and separately refuses a pre-existing symlink at any level (`candidate.is_symlink()`); `_make_destinations` re-checks after creation to close the mkdir race window. No `tmpdir()`, no `os.environ` read, no caller-supplied destination parameter exists anywhere in `launch()`'s signature. `_capability_ready` refuses `None`, a non-`WorkspaceCapability`, and a location that isn't a readable directory (catching `OSError`/`RuntimeError`/`TypeError`). Independently confirmed by inspection and by `test_symlink_escape_refuses_without_diagnostic_path`. The `capability=None`/malformed case is verified only via the preflight test (`test_missing_capability_refuses`) and by reading `_confined_destinations`/`_capability_ready`, not via a `LiveViewingVehicle.launch()`-level test as the charter also asks for; low-risk since it's the first line of `launch()`, but worth naming (see Non-blocking observations). |
| 4 | Claim discipline: no artifact reads as claiming egress prevention or clipboard-check completeness; no enforcement substrate implemented or wired. | **Pass.** `grep -n "prevent\|block\|wall\|guarantee\|complete"` over the module surfaces only two hits, both explicit negations ("not... represented as a complete clearance", "does not... block mechanically"). The module docstring states plainly that it "does not create a trust boundary for a same-authority browser process." No `sandbox-exec`, container, or OS-identity code appears anywhere in the diff. |
| 5 | Teardown on every exit path: launch failure, refusal after partial construction, exception mid-session, normal close; nothing outside the workspace removed. | **Pass.** Launch failure is tested directly (`test_launch_failure_tears_down_owned_session`) and normal close is tested directly (`test_destinations_are_inside_capability_and_browser_is_headed`, asserting `.live-view` is gone after `close()`). By inspection: `_confined_destinations` (called before the `try` in `launch()`) performs no filesystem mutation, so a refusal there has nothing to tear down; a failure inside `_make_destinations` is caught by the enclosing `try`/`except LiveViewingError` and cleaned via `_remove_session`'s `shutil.rmtree`, which is correct for a partially-created tree. `LiveViewingSession.__exit__` unconditionally calls `close()`, covering exception-mid-session use as a context manager. `_remove_session` confines its own `rmtree` call to a path re-validated against the canonical root immediately before deletion, so nothing outside the workspace can be removed even on a symlink race. |
| 6 | Scope: no real workspace touched; `synthetic: true` boundary unweakened; `chrome.mjs` unmodified; vehicle not reusable as an evaluation path; Presentation still claimed at L2. | **Pass.** All tests use `tempfile.TemporaryDirectory`. `git diff main..HEAD --stat -- tools/presentation_harness/lib/chrome.mjs tools/presentation_harness/lib/server.mjs tools/presentation_harness/lib/manifest.mjs .../citation-walk.v1.json .../citation-walk.v1.html` is empty. `live_viewing.py` is an entirely new module with no import from or into the harness; the two evaluation manifests both still pass at their established counts (26/0, 19/0). No maturity-matrix edit is in this diff. |

## Blocking finding

### Finding 1 — The clipboard-history split disposition's most load-bearing case (a confirmed-absent probe still yields the owner-responsibility code, not a clearance) is untested

**File/line evidence** (`packages/derivation/live_viewing.py:153-165`):

```python
clipboard = _state(_observe(probes.clipboard_history))
if clipboard is ProbeState.PRESENT:
    refusals.append(ViewingReason.CLIPBOARD_HISTORY_PRESENT.value)

if refusals:
    return PreflightVerdict(False, tuple(refusals))

# The false/absent result only reports what this probe observed.  It never
# upgrades a partially decidable clipboard check into a clearance claim.
return PreflightVerdict(
    True,
    owner_responsibilities=(ViewingReason.CLIPBOARD_HISTORY_UNDETECTABLE.value,),
)
```

By inspection, this is **correctly implemented**: when the session is allowed, `owner_responsibilities` unconditionally carries `CLIPBOARD_HISTORY_UNDETECTABLE`, whether `clipboard` resolved to `ABSENT` (a confirmed "no known clipboard-manager process found") or `UNKNOWN`/`UNREADABLE`. This is exactly ADR-0047's point: an enumerable clipboard-manager check can rule out only the managers it knows to look for, never certify that *no* clipboard-history software of any kind is running, so even a clean, confirmed-absent result must not read as a completeness claim.

**What's untested.** `test_clipboard_result_is_partial_and_detectable_presence_refuses` (the only test exercising this branch) checks exactly two inputs: `ProbeState.UNKNOWN` (owner-responsibility code present, correct) and `True`/`PRESENT` (refusal, correct). It never calls `run_viewing_preflight` with `clipboard_history=False` — the confirmed-`ABSENT` case — to confirm the owner-responsibility code is *still* attached rather than silently dropped. This is precisely the input the milestone's own review history (`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-26-presentation-live-viewing-boundary-track1-review.md` Finding 1; two repair cycles fixing exactly this class of claim-discipline error in the ADR text) shows is the natural place to introduce a regression: a future edit that "cleans up" the function by gating the owner-responsibility code on `clipboard is not ProbeState.ABSENT` would look like a correct simplification, would pass every existing test, and would silently reintroduce the completeness claim ADR-0047 explicitly forbids.

**Failure scenario:** a later change narrows the final `return` to attach `owner_responsibilities` only `if clipboard is not ProbeState.ABSENT else ()`. All 9 tests in this file still pass (none constructs the `ABSENT` case), `envelope_scan` and `diff --check` are unaffected, and the preflight now silently certifies a session as fully clipboard-clear whenever a known-manager scan finds nothing — exactly the claim ADR-0047's Class D and precondition-disposition sections were repaired twice to prevent.

**Recommended repair (not prescribed, Builder's choice):** add a fourth case to `test_clipboard_result_is_partial_and_detectable_presence_refuses` (or a sibling test) asserting `run_viewing_preflight(_capability(root), PreflightProbes(False, False, False)).owner_responsibilities == (ViewingReason.CLIPBOARD_HISTORY_UNDETECTABLE.value,)` — i.e., confirmed-absent still carries the owner-responsibility code, not an empty tuple.

## Non-blocking observations

1. **`__context__` retention on chained exceptions.** Every `raise LiveViewingError(...) from None` sets `__suppress_context__ = True`, which correctly prevents `str()`, `repr()`, and standard `traceback` printing from ever showing the original path-bearing exception. The original exception object is still technically reachable via `exc.__context__` for any future caller that walks it explicitly (none currently does). Worth a one-line note in the module docstring if this file is touched again, not a blocking gap today.
2. **`capability=None`/malformed input has no `LiveViewingVehicle.launch()`-level test**, only preflight-level (`test_missing_capability_refuses`) and by-inspection coverage of `_confined_destinations`/`_capability_ready`. Low risk, since the check is the unconditional first line of `launch()`, but the charter named this case explicitly; a direct `vehicle.launch(None, ...)` test would close the gap cheaply alongside any Finding 1 repair.

## Verdict

**NOT READY.** Five of six measurements pass on independent verification, including a full rerun of the build charter's stated verification block. Measurement 2 surfaces one exact residual (Finding 1): the clipboard-history split disposition is implemented correctly, but its most consequential input — a confirmed-absent probe still yielding the owner-responsibility code rather than a clearance — is the one case the test suite does not exercise, on the exact invariant this milestone's Track 1 spent two repair cycles establishing in the governing ADR. This is a single findings-only repair (a test addition, no production-code change indicated) within the plan's stated cap.
