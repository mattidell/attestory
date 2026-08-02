# Review — The Entry Loop (synthetic), Track 1 repair

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-29-entry-loop-synthetic-track1-repair-review.md`
- Repair charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-29-entry-loop-synthetic-track1-repair.md`
- Prior review: `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-29-entry-loop-synthetic-track1-review.md` (`NOT READY`)
- Branch: `milestone/entry-loop-synthetic`, at `60452ec`
- Under review: `2e62c4a` — 2 files, 272 insertions, tests only (worked from `5275ed0`)

## Orientation and review object

`python3 tools/build_orientation_block.py --ref HEAD` resolved reviewer at
`60452ec31024fd0fcb1e1ab3dde03a6dededd41a`, matching `git rev-parse HEAD`. The
derived ratified line is `origin/main-ui`; the merged opening-plan PR #109
does not make the workspace spent. Current role per phase state matches the
charter: "Reviewer — The Entry Loop (synthetic), Track 1 repair review."

## Verdict: READY for Track 1 as a whole

F1 is disposed correctly — ADR-0051 changed the premise the prior blocking
finding rested on, and the repair introduces no false claim of browser or OS
isolation. F2 and F3 are closed by durable, non-vacuous coverage: five of the
seven fail-closed tests break cleanly under direct mutation of the exact
behaviour they name, and the remaining two (duplicate/out-of-order
submission) are protected by genuine, if redundant, layered guards rather
than by nothing. The browser test runs, unskipped, on the machine of record
and drives the client's own relative `./api/*` requests through completion.
One non-blocking, real finding remains open: a timed-out browser probe can
orphan a headless Chrome process and its temporary profile directory, which
I reproduced directly.

## Findings

### Weakening

**F1 (new). A timed-out browser probe leaks a Chrome process and its temp
profile.** `CompiledClientIntegration` runs the Node helper under
`subprocess.run(..., timeout=30, check=False)` with no process-group handling.
Python's timeout kill only reaches the direct Node child; if Node is killed
before its `finally` block runs, the headless Chrome process it spawned (and
that process's `mkdtemp`-created profile directory under `tmpdir()`) are never
disposed. I reproduced this directly (see Measurement 4): a Node script that
launches Chrome via the same `launchChrome()` helper and never returns,
killed by a 5-second `subprocess.run` timeout exactly as the test's own
30-second timeout would kill a genuinely hung probe, left one `Google Chrome`
headless process and one `presentation-harness-profile-*` directory on disk
after the Python call returned. Nothing in the profile path, launch
arguments, or process command line carries a residency locator — the leak is
a hygiene defect, not a data-boundary breach — but a CI worker that
accumulates timed-out runs accumulates orphaned Chrome processes and profile
directories. This is pre-existing behaviour in
`tools/presentation_harness/lib/chrome.mjs` (used unmodified by the repair,
not introduced by it), and the same exposure already exists for any other
caller of `launchChrome()` under a hard timeout. Recommend either passing a
timeout the helper's own `dispose()` gets to run under (SIGTERM with a grace
period, not `subprocess.run`'s SIGKILL), or accepting this as a documented
gap for a later track — it does not block Track 1, since a normal run (Chrome
present, workspace healthy) never hits the timeout path.

**F2 (weakening, informational). The duplicate/out-of-order tests do not
isolate which layer refuses.** See Measurement 1 below for the mutation
detail. `test_duplicate_submission_fails_closed` and
`test_out_of_order_submission_fails_closed` both replay the exact same
one-time contribution template (same nonce, same `act_id`, same
`committed_against`) that a prior request already consumed. Disabling
`entry_loop.py`'s own staleness check (`entry-event-stale`) alone does not
break either test, because the template-nonce comparison in
`_validate_template` independently catches the replay. Disabling *both*
checks still does not break either test, because the kernel's own
`apply_contribution` refuses re-use of the same `contribution_id`
(`FindingModelError: contribution already exists: ...`) before any act
appends. All three fail-closed properties genuinely hold at every layer I
tried to remove, which is a stronger result than the charter asked for — but
it also means these two tests cannot be used as evidence that
`entry_loop.py`'s own staleness line does anything; they only prove the
system as a whole (kernel included) refuses replay. That is fine as product
behaviour and is not a blocking finding, but the review should record it so
a future editor does not delete the (apparently redundant) staleness check on
the mistaken belief that removing it is untested.

## Measurements

### 1. Are the seven fail-closed tests non-vacuous?

I broke each guarded behaviour directly in `packages/derivation/entry_loop.py`,
ran the single affected test, confirmed it failed, then restored the file from
an unmodified copy and reconfirmed the full suite passed clean.

| Test | Mutation | Result | Which of the three parts fires |
| --- | --- | --- | --- |
| `test_wrong_content_type_fails_closed` | Removed the `Content-Type != application/json` → 415 check | Broke: `AssertionError: 400 != 415` | Refusal (status) |
| `test_oversized_body_fails_closed` | Raised `_MAX_REQUEST_BYTES` from 16,384 to 16,384,000 | Broke: `AssertionError: 422 != 400` (falls through to template validation, still refuses but on the wrong ground) | Refusal (status) |
| `test_malformed_json_fails_closed` | Caught `JSONDecodeError`/`ValueError` from `json.loads` and substituted `{}` instead of propagating | Broke: `AssertionError: 422 != 400` | Refusal (status) |
| `test_json_type_confusion_fails_closed` | Replaced the non-dict-body `raise ValueError` with a silent fallback to `{}` | Broke: `AssertionError: 422 != 400` | Refusal (status) |
| `test_template_tampering_fails_closed` | Removed `"actor"` from `_validate_template`'s compared-key set | Broke: `AssertionError: 200 != 422` — the tampered actor was **accepted** | Refusal (status) — and this mutation is the one that shows a real acceptance, not just a wrong error code |
| `test_duplicate_submission_fails_closed` | See F2 above: front-line checks alone insufficient to break it; broke only when I also disabled the kernel's `apply_contribution` duplicate-id detection is not something I touched (kernel, out of repair scope) — with only the two `entry_loop.py`-level checks removed, the test **still passes** because the kernel refuses re-use of `contribution_id` | Not directly breakable within the repair's own code alone (kernel backstop holds) | All three (status, no echo, no log advance) — verified via `_assert_fails_closed`'s three assertions, satisfied by the kernel's own refusal path |
| `test_out_of_order_submission_fails_closed` | Same as above | Same as above | Same as above |

For every one of the seven, `_assert_fails_closed` asserts all three parts of
the prior review's fail-closed definition uniformly: `actual_status ==
status`, `marker not in response`, and `snapshot().revision` unchanged before
and after. None of the seven only checks a status code.

### 2. Does the browser test drive the real compiled client?

Yes. `EntryPage.svelte`'s `stateUrl()` builds `new URL("./api/${name}",
window.location.href)` and issues its own `fetch()` calls from
`loadState()`/`submitWages()`; the Node helper
(`tests/helpers/entry_loop_browser_client.mjs`) never issues an HTTP request
itself. It launches real headless Chrome via
`tools/presentation_harness/lib/chrome.mjs`, navigates to the built page,
waits on DOM text asserted through `Runtime.evaluate`, sets the input value
and calls `input.form.requestSubmit()` (a real form submission through the
compiled Svelte handler, not a synthesized fetch), and only *observes*
`Network.requestWillBeSent` events to detect the `/api/state` and
`/api/contributions` paths. The Python test then asserts
`self.runtime.snapshot().payload["complete"]` — the same server-side runtime
instance the loopback server serves — confirming the browser-originated
contribution reached the same act log the Python-side tests exercise, not a
separate code path.

### 3. Is that test real coverage or a test that never runs?

It runs, unskipped, on this machine. `node --version` reports v25.8.0,
`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` exists, and
`packages/sample_data/entry_loop_t1/surface/content/app/node_modules` is
present (vendored, gitignored per the Packaging milestone's decision).
`python3 -m unittest tests.test_entry_loop_t1 -v` shows
`test_compiled_client_drives_the_real_entry_api ... ok` among 24 tests run,
0 skipped. I did not check CI's own Chrome/Node/vendored-tree availability
independently — I have no CI log to read from this session, only the
machine of record — so whether it runs in CI specifically is unconfirmed by
me; the charter's premise (six *other* surface tests already skip in CI
without the vendored tree) suggests this one likely skips there too, but I
did not verify.

### 4. Data safety, with a live browser in the loop

`python3 tools/envelope_scan.py --range 5275ed0..2e62c4a` exits 0, no output.
`launchChrome()` (unmodified, reused infra) uses `--headless=new`, a fresh
`mkdtemp(tmpdir(), "presentation-harness-profile-")` profile per launch,
`--remote-debugging-port=0` (OS-assigned), a loopback WebSocket URL, and
disposes the profile with `rm(profileDir, {recursive:true, force:true})` in
its own `dispose()`. No residency locator appears in launch arguments,
profile paths, page URLs (loopback, high-entropy route capability), console
output, or the helper's failure text (`entry-browser-probe-failed`, no
detail). On the happy path and on ordinary CDP-level failures, cleanup is
correct — I drove the helper through its `catch`/`finally` and confirmed no
leftover process or directory.

Reading for what the scan cannot see: I reproduced the one gap the scan
cannot catch by construction, since it's a process/filesystem hygiene issue,
not data in a tracked file. I wrote a Node script that calls the *same*
`launchChrome()` helper and then hangs forever without ever calling
`dispose()`, ran it under `subprocess.run(..., timeout=5, check=False)` (the
same code shape as the test's `timeout=30`), and confirmed:

- baseline: 0 headless Chrome processes, 0 `presentation-harness-profile-*`
  directories in `$TMPDIR`;
- after the timeout fired and Python's `subprocess.run` raised
  `TimeoutExpired`: one live headless `Google Chrome` process (plus its GPU
  helper) and one `presentation-harness-profile-*` directory remained on
  disk, both still present a second after the Python call returned.

I killed the orphaned processes and removed the directory manually before
continuing. See F1 above.

### 5. Regression and scope

`git diff 5275ed0..2e62c4a --stat` shows exactly two files, both under
`tests/`, 272 insertions, 0 deletions: `tests/test_entry_loop_t1.py` and the
new `tests/helpers/entry_loop_browser_client.mjs`. No product code changed.
`git diff 5275ed0..2e62c4a -- tests/test_entry_loop_t1.py | grep '^-' ` shows
only the diff header — no line was deleted from the existing file, so the
four Phase A dependency tests (mutation-tested and held in the prior review)
are untouched by construction, not just by inspection.

### 6. Verification

Re-ran the full sequence recorded in `2e62c4a`'s commit message, worked from
`5275ed0`:

- `pytest -n auto`: 711 passed, 3,220 subtests passed — matches;
- `python3 -m mypy`: "Success: no issues found in 134 source files" — matches;
- `python3 tools/governance_lint.py`: "governance lint: conformant" — matches;
- `python3 tools/envelope_scan.py --range 5275ed0..2e62c4a`: exit 0, no
  output — matches;
- `git diff 5275ed0..2e62c4a --check`: clean — matches.

All claims hold.

### F1 disposal (ADR-0051)

Read `docs/adr/0051-entry-surface-contract.md` before the prior review, per
the charter's instruction. It supersedes ADR-0048 Decision 1 (the
vehicle-level spellcheck-closure condition) only; Decision 2 (the
contribution boundary) is untouched and the prior review's PASS findings on
it (no direct fact-writing shortcut, ADR-0049 route, loopback POST boundary)
are unaffected by this repair, which touches none of that code. I did not
re-argue F1's merits. I confirmed the premise changed (phase-state records
"THE OWNER WITHDREW ADR-0048's ENTRY-VEHICLE CONDITION on 2026-07-29") and
grepped the diff and the existing surface source for any presentation of
`spellcheck="false"` as a security control: the only occurrence is a plain
HTML attribute on the W-2 input with no adjacent comment or documentation
claiming it closes any network path. That satisfies ADR-0051's "no false
claim of isolation" clause. F1 is disposed.

One note for the owner, separate from the verdict, not reopening F1 on its
merits: ADR-0051 itself is still recorded as `Status: proposed` in both the
ADR file and `docs/adr/INDEX.md`. The owner's withdrawal of ADR-0048's
condition is recorded independently in phase-state and is what F1's
disposal actually rests on, so this review does not treat ADR-0051's
ratification status as blocking — but a future reader comparing the ADR
file's "proposed" status against phase-state's more definite "the owner
withdrew..." language should not have to reconcile the two by inference.

## Report back

**Verdict: READY for Track 1 as a whole.**

**F1** (prior blocking finding) is disposed on recheck: ADR-0051 changed the
governing rule, and nothing in the repair or the existing surface presents a
browser setting as a security control.

**F2/F3** (prior weakening findings) are closed: seven fail-closed tests are
committed and non-vacuous, and the compiled client is now driven in real
Chrome against the loopback API through completion.

**New findings, both weakening, neither blocking:** an orphan-on-timeout gap
in the shared browser-launch helper (F1 in this review, reproduced directly),
and an observation that two of the seven tests are protected by redundant
layered guards rather than by the specific application-layer line they were
apparently written to cover (F2 in this review, informational).

**Which of the seven refusals I broke and what happened:** five broke
directly and cleanly under a single, targeted mutation of the exact code
each test names (wrong content type, oversized body, malformed JSON, JSON
type confusion, template tampering — the last one is the most informative,
since the break produced a live `200` acceptance of a tampered actor field,
not just a wrong status code). The remaining two (duplicate submission,
out-of-order submission) held even after I disabled both of
`entry_loop.py`'s own front-line checks, because the kernel's own
contribution-id uniqueness constraint refused the replay independently — a
stronger result than a single-layer mutation test can show, but one that
means those two tests can't be read as proof that `entry_loop.py`'s own
staleness check specifically works.

**Whether the browser test runs or skips:** it runs, unskipped, on this
machine (Node v25.8.0, Chrome present, vendored tree present) and passed.
Whether it runs in CI is not something I could confirm from committed
sources in this session.

**The single thing most likely to be wrong that I could not prove either
way:** whether the timeout-orphan gap (F1 above) is actually reachable by
the committed test in ordinary CI operation, as opposed to only by my
synthetic hang script. I proved the mechanism is real — the same
`launchChrome()` helper, killed the same way `subprocess.run`'s timeout kills
it, leaves a process and a directory behind — but I did not prove that
`CompiledClientIntegration`'s own 30-second timeout is ever actually hit in
practice (a healthy CI run should complete well under it). I could not
determine, from committed sources alone, how likely a CI worker is to be
slow or loaded enough to trigger it, or whether CI has any environmental
sweep that would clean up an orphan regardless.

No product code, fixture, criterion, or matrix entry was changed in this
review.
