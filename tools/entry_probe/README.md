This is a throwaway instrument, not product code. It exists to answer one
question for the Entry Boundary milestone (Track 1) and then goes away.

Charter: `docs/reviews/charter-2026-07-28-entry-boundary-track1.md`.
Findings: `docs/phases/legible-entry/milestones/entry-boundary-retention-findings.md`.

## What it does

Drives the existing confined invocation vehicle
(`tools/presentation_harness/lib/chrome.mjs` + `lib/server.mjs`, unmodified —
imported, never touched) to launch headless Chrome against a fresh disposable
profile, serve `form.html` (a minimal page with realistic tax-form-looking
text inputs) over the harness's own loopback-only server, type distinctive
synthetic tokens into those inputs with real CDP-dispatched keystrokes, submit
the form, and then inspect what ended up on disk under two shutdown paths:

1. A clean-ish close — the probe sends `SIGTERM` to the Chrome process itself
   and waits for exit.
2. A simulated crash — the probe sends `SIGKILL` directly.

It deliberately does **not** call `chromeHandle.dispose()` from `chrome.mjs`
for either of these: `dispose()`'s last act is to delete the whole profile
directory, which would erase the evidence before this script could inspect
it. Instead the probe finds the browser's OS pid and `--user-data-dir` by
reading `ps` output (pure external process inspection — chrome.mjs was not
changed and does not need to be), signals the process itself, waits for it to
exit, greps the profile directory for the synthetic tokens, and only then
deletes the directory itself. `chrome.mjs`'s own `dispose()` already deletes
this directory unconditionally on every normal harness run; this probe's
existence is only about seeing what was in it before that deletion, once.

It also captures every non-loopback network request the browser attempts
during the run (via the CDP `Fetch` domain, blocking each one and recording
its URL/method/postData) — the same pattern `executor.mjs` already uses for
its own confinement — so a spellcheck- or telemetry-service call would show
up as a recorded, blocked attempt rather than silently succeeding.

## Running it

```
node tools/entry_probe/probe.mjs
```

Requires a local Chrome/Chromium install discoverable the same way
`chrome.mjs` finds one (or `PRESENTATION_HARNESS_CHROME` set). Prints
progress to stderr and a JSON report to stdout. Not wired into `verify`, CI,
or any test suite — run by hand only.

## Cleanup

The probe deletes every profile directory it creates before exiting, on both
the success and the token-found-in-network-egress abort paths. If it is
killed mid-run, an orphaned `presentation-harness-profile-*` directory may be
left in `$TMPDIR`; check `ps -axww -o pid,command | grep presentation-harness-profile-`
and clean up by hand.

## Disposal

Per the charter and the milestone plan, this directory is parked here only
long enough to produce the findings note. It is not maintained and should be
deleted once Track 2 (the ADR) no longer needs to re-run it for verification.
