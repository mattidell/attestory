This is a throwaway instrument, not product code. It exists to answer one
question for the Entry Boundary milestone (Tracks 1 and 1b) and then goes
away.

Charters: `docs/reviews/charter-2026-07-28-entry-boundary-track1.md` (Track 1,
headless) and `docs/reviews/charter-2026-07-28-entry-boundary-track1b.md`
(Track 1b, headed).
Findings: `docs/phases/legible-entry/milestones/entry-boundary-retention-findings.md`.

## What it does

Drives two different, unmodified vehicles against the same throwaway form
(`form.html`) and the same five channels, and greps the resulting profile
directory for synthetic tokens under two shutdown paths — a clean-ish close
(the probe signals the Chrome process itself with `SIGTERM` and waits) and a
simulated crash (`SIGKILL`).

- **Headless vehicle** (Track 1):
  `tools/presentation_harness/lib/chrome.mjs` + `lib/server.mjs`, unmodified —
  imported, never touched. Launches headless Chrome (`--headless=new`,
  hardcoded by `chrome.mjs`) against a fresh disposable profile.
- **Headed vehicle** (Track 1b): `packages/derivation/live_viewing.py`,
  unmodified (ADR-0047's confined headed viewing vehicle — never passes
  `--headless`). Launched via the throwaway bridge `headed_launch.py`
  against a synthetic workspace directory (a bare temp directory standing in
  for a real one).

In both cases the probe serves `form.html` (a minimal page with realistic
tax-form-looking text inputs) over the harness's own loopback-only server,
types distinctive synthetic tokens into those inputs with real
CDP-dispatched keystrokes, submits the form, and inspects what ended up on
disk.

It deliberately does **not** call the vehicle's own teardown
(`chromeHandle.dispose()` for the headless vehicle, `LiveViewingSession.close()`
for the headed one) for either shutdown path: each one's last act is to
delete the confined directory, which would erase the evidence before this
script could inspect it. Instead the probe finds the browser's OS pid and
confined directory by reading `ps` output (pure external process
inspection — neither vehicle needs to expose anything, and neither is
changed), signals the process itself, waits for it to exit, greps the
directory for the synthetic tokens, and only then deletes it itself.

It also captures every non-loopback network request the browser attempts
during the run (via the CDP `Fetch` domain, blocking each one and recording
its URL/method/postData) — the same pattern `executor.mjs` already uses for
its own confinement — so a spellcheck- or telemetry-service call would show
up as a recorded, blocked attempt rather than silently succeeding.

## `headed_launch.py`

A throwaway Python bridge, not product code. It imports
`packages/derivation/live_viewing.py` and `live_workspace.py` unmodified,
launches `LiveViewingVehicle` against a synthetic workspace directory passed
as its one argument, prints the resulting session's public `websocket_url` as
one line of JSON, and then blocks reading stdin until killed. It never calls
`session.close()` itself — the Node-side probe kills the discovered Chrome
pid directly, for the same evidence-preservation reason described above. The
launched Chrome process runs in its own session
(`start_new_session=True`, set by `live_viewing.py`, not by this bridge), so
killing this bridge script does **not** kill the Chrome process it launched;
the Node-side probe must (and does) signal the Chrome pid directly.

## Running it

```
node tools/entry_probe/probe.mjs                  # both vehicles (default)
node tools/entry_probe/probe.mjs --mode=headless  # Track 1's vehicle only
node tools/entry_probe/probe.mjs --mode=headed    # Track 1b's vehicle only
node tools/entry_probe/probe.mjs --mode=headed --wide-search  # Track 2 repair, Part 1
```

`--wide-search` (Track 2 repair, Part 1) extends the headed vehicle's two runs
with a search of real per-user macOS locations *outside* the confined session
directory — the region every earlier run in this milestone left unchecked.
Method: touch a marker file immediately before launch, then after the
crash/close, ask each candidate location which entries have a **creation**
time (`stat -f %B`, not mtime) at or after the marker's, and grep any such
file for the same synthetic tokens. Creation time, not modification time, is
used deliberately: this machine's own real Chrome install may be running for
unrelated reasons (it was, the day this was run — see the findings note), and
a running real browser continuously modifies pre-existing files in its own
profile without creating new ones most of the time; filtering on birthtime
keeps the signal to "something new appeared here in this exact window," not
"something in a directory a real, unrelated process also uses got touched."
Candidate locations (see `wideSearchRoots()` in `probe.mjs`): the macOS
per-user crash-report directories, the per-user caches directory, `$TMPDIR`
and `/tmp`, and the Chrome/Chromium per-user application-support directories.
Only meaningful for the headed vehicle (the one a person actually types
into); has no effect in `--mode=headless`.

**Operational note the ordinary cleanup section above does not cover:** if
this flag turns anything up outside `$TMPDIR`'s or another candidate
location's confined subtree, that artifact is *not* something this probe (or
`live_viewing.py`) created inside a directory either one manages, so neither
one's cleanup path removes it. Check by hand after a `--wide-search` run
(nothing is deleted automatically for you outside the confined tree).

Requires a local Chrome/Chromium install discoverable the same way each
vehicle finds one (or `PRESENTATION_HARNESS_CHROME` set, for the headless
vehicle), and `python3` on `PATH` for the headed vehicle's bridge. Prints
progress to stderr and a JSON report (tagged per session with a `vehicle`
field) to stdout. Not wired into `verify`, CI, or any test suite — run by
hand only.

The headed vehicle needs a real display / window server to launch a real
(non-headless) Chrome window. If none is available, this is a stop condition
per the Track 1b charter — do not fall back to headless for the headed run;
report it instead.

## Cleanup

The probe deletes every profile directory and synthetic workspace directory
it creates before exiting, on both the success and the
token-found-in-network-egress abort paths. If it is killed mid-run, an
orphaned `presentation-harness-profile-*` directory (headless) or
`entry-probe-headed-workspace-*` directory (headed, containing a
`.live-view/session-<uuid>/` subtree) may be left in `$TMPDIR`; check
`ps -axww -o pid,command | grep -E "presentation-harness-profile-|entry-probe-headed-workspace-"`
and clean up by hand.

## Disposal

Per the charters and the milestone plan, this directory is parked here only
long enough to produce the findings note. It is not maintained and should be
deleted once Track 2 (the ADR) no longer needs to re-run it for
verification.
