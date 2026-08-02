# Entry Boundary — retention-probe findings (headless and headed)

Evidence ceiling: **observation on synthetic fixtures only, on this machine, in
these runs.** Everything below is what `tools/entry_probe/probe.mjs` observed
driving two different, unmodified vehicles against the same throwaway form. It
is not a claim about what Chrome does in general, about any other machine, or
about real data. It reports observations; it does not recommend a write path
or say whether a browser form is acceptable — that is Track 2's question to
answer, and it may reach a different conclusion than what these observations
seem to suggest.

- **Headless vehicle:** `tools/presentation_harness/lib/chrome.mjs` +
  `lib/server.mjs`, unmodified, hardcoded `--headless=new`. This is the
  synthetic evaluation harness, not the vehicle a person actually types into.
- **Headed vehicle:** `packages/derivation/live_viewing.py`, unmodified
  (ADR-0047's confined headed viewing vehicle). Never passes `--headless`; its
  own test suite (`tests/test_presentation_live_viewing_vehicle.py`) asserts
  the headed property directly. Driven here via the throwaway bridge
  `tools/entry_probe/headed_launch.py`, against a **synthetic** workspace
  directory (a bare temp directory standing in for a real one — never a real
  workspace, never a real fact, never a residency locator).

Probe: `tools/entry_probe/probe.mjs`. Fixture: `tools/entry_probe/form.html`.
Bridge: `tools/entry_probe/headed_launch.py`. Full method notes:
`tools/entry_probe/README.md`.

## Method summary (identical across both vehicles)

- Served `form.html` — five text inputs with realistic `name`/`id`/`type`/
  `autocomplete` (`fullName` autocomplete=name, `ssn` autocomplete=off,
  `wages` autocomplete=off, `email` autocomplete=email, `notes`
  autocomplete=off, deliberately including a misspelled phrase) — from the
  harness's own loopback-only server, reused for both vehicles.
- Typed a distinct synthetic token per field via real CDP-dispatched
  keystrokes (`Input.dispatchKeyEvent`, matching the event shape a genuine
  keypress produces), read the DOM back to confirm each field held the
  intended value verbatim, then submitted the form (a real navigation).
- Exercised a clean-ish close (probe sends `SIGTERM` itself) and a simulated
  crash (`SIGKILL`, no warning) for each vehicle.
- Found the browser's OS pid and confined directories by reading `ps` output
  — pure external process inspection, neither vehicle was modified — signalled
  the process itself rather than calling the vehicle's own teardown (whose
  last act deletes the confined directory, destroying the evidence first),
  waited for exit, then grepped the still-on-disk directory recursively and
  binary-safely (`grep -rla <token> <dir>`) before deleting it itself.
- Every non-loopback network request attempted during the whole run was
  captured via the CDP `Fetch` domain and checked for the tokens, in the URL
  and any POST body.

**Headed-vehicle-specific method note:** `packages/derivation/live_viewing.py`
confines Chrome's profile, disk cache, and downloads into three *separate*
sibling directories under one session root
(`.live-view/session-<uuid>/{profile,cache,downloads}`), unlike `chrome.mjs`,
which sets only `--user-data-dir` (cache lives inside the profile directory by
Chrome's own default). The probe greps the whole synthetic workspace directory
for the headed vehicle, not just the profile subdirectory, so this shape
difference does not create a blind spot.

**Operational difference observed, not a channel finding:** the headed
vehicle's Chrome process did not exit within 5 seconds of `SIGTERM` in either
session of either run recorded here; the probe's existing 5-second-then-force
`SIGKILL` fallback (unchanged from Track 1) engaged both times. The headless
vehicle's process exited within that window in every run. This may reflect
real GUI teardown work (window/compositor shutdown) that a headless process
does not do; this probe did not investigate further, and it does not bear on
any of the five channels below.

## Grep positive control (re-confirmed this run)

Track 1 found that `grep -rlaI` — the `-I` flag meaning "treat binary files as
non-matching" — silently suppressed every match inside a binary store
(SQLite, LevelDB). This run re-confirmed that finding independently, against
the actual binary `node`'s `execFileSync("grep", ...)` invokes (`/usr/bin/grep`,
BSD grep 2.6.0-FreeBSD on this machine — not the interactive shell's `ugrep`
alias, which is a different program only present in the interactive terminal,
not in a `node`-spawned subprocess), by planting a known token inside a
synthetic binary file:

```
$ /usr/bin/grep -rlaI POSITIVECONTROL-TOKEN-abc123 <dir>   # exit 1, no match — silently wrong
$ /usr/bin/grep -rla  POSITIVECONTROL-TOKEN-abc123 <dir>   # exit 0, file found — correct
```

`grepDirForTokens()` in `probe.mjs` uses `-rla` (the corrected flag). Every
result below is from the corrected flag, re-confirmed against a positive
control on this run, not inherited on trust from Track 1's account.

## Findings by channel

### 1. Form history / autofill

**Observed: not fired, in both vehicles.** `Default/Web Data` (the SQLite
store Chrome's autofill/form-history feature writes to) existed in all four
profiles (headless × 2, headed × 2) after close and was grepped with the rest
of the tree; no token appeared in it, or anywhere else, in any of the four
sessions. This held for the `autocomplete=off` fields (`ssn`, `wages`,
`notes`) and, notably, also for the fields given realistic non-off
autocomplete hints (`fullName` → `autocomplete="name"`, `email` →
`autocomplete="email"`) that are exactly the ones a real autofill heuristic
would be expected to key off.

**Headless vs. headed: no difference observed.** Track 1's review flagged this
as the channel most plausibly a headless artifact, since headless Chrome
could in principle suppress the autofill-save subsystem outright. That did not
happen here in the sense of the subsystem being absent: `Web Data` exists and
is writable in both vehicles. What this run did **not** exercise, in either
vehicle, is a real user accepting Chrome's own "Save this info?" prompt — that
prompt is a UI infobar the form-submission flow surfaces, and no step in this
probe (headless or headed) drives that acceptance. A "not fired" result here
is honestly a report of "no token was saved without an explicit save
confirmation," in both vehicles equally — not evidence that the confirmation
step itself is unreachable or unreachable-by-a-real-user in the headed
vehicle. This is the same undetermined status Track 1's review already named,
now narrowed: it is undetermined because the save-confirmation UI path was
not driven, in either vehicle, not because headless mode hides the feature
from the headed one.

Confinement: N/A — nothing was found to contain.

### 2. Session restore and crash recovery

**Observed: fired (files are written) in both vehicles, and did not contain
the typed values in either.** `Default/Sessions/` held real files in both
vehicles after the form-navigation flow — `Session_<id>` and `Tabs_<id>` after
the clean-ish close; `Session_<id>` only after the simulated `SIGKILL` crash
(no `Tabs_` file that time, in both vehicles, itself a same-shape
observation not further interpreted here). `Default/Session Storage/` (a
separate LevelDB store) also had identical-shaped content (`000003.log`,
`CURRENT`, `LOCK`, `LOG`, `MANIFEST-000001`) across all four sessions. The
whole-tree grep covered these files along with everything else in each
profile/workspace and found no token in any of them, in any run.

**Headless vs. headed: no difference observed in the byte-writing half of
this channel.** The behavioral half — whether relaunching Chrome pointed at
the same (crashed) profile actually surfaces a "restore pages" prompt — is
still untested in both vehicles; see below.

Untested, and why (unchanged from Track 1, now confirmed to apply to both
vehicles): whether relaunching Chrome pointed at the **same** (crashed)
profile would actually surface a "restore pages" prompt was not tested.
Neither `chrome.mjs`'s `launchChrome()` nor `live_viewing.py`'s
`LiveViewingVehicle.launch()` has a parameter to reuse an existing (crashed)
profile/session directory — each computes a fresh one every call
(`chrome.mjs` via `mkdtemp`; `live_viewing.py` via a fresh
`.live-view/session-<uuid>`). Adding one to either would be exactly the kind
of vehicle modification the charter forbids. Only "were crash-recovery bytes
written, and do they contain the typed values" was tested in either vehicle,
not "does the browser then offer to restore them."

Confinement: contained by construction under normal operation in both
vehicles — `chrome.mjs`'s own `dispose()` and `live_viewing.py`'s own
`LiveViewingSession.close()` both delete their respective confined
directories, including these files, on every clean run. This probe bypassed
only that teardown step in each vehicle (not the vehicle itself) to see the
files before deletion.

### 3. Undo buffer persistence

**Observed: present in-memory within the page, cleared by navigation, never
touched disk — identically in both vehicles.** After typing the `notes`
token, the field was cleared (`execCommand('delete')`) and `execCommand('undo')`
was called: the full token came back exactly, in all four sessions. The page
was then navigated away and back to the same form; calling `undo` again on the
now-fresh `notes` field returned an empty string in all four sessions — the
undo stack did not survive the navigation, in either vehicle. No token from
this sequence appeared anywhere in any profile/workspace grep.

**Headless vs. headed: no difference observed.** This matches Track 1's
review assessment that this channel (Blink's in-page `execCommand` undo
stack) is unlikely to be gated by `--headless`; this run found the identical
behavior in the vehicle that does not pass that flag at all.

Confinement: N/A — this channel does not appear to write to disk at all in
either vehicle; it lives and dies with the renderer's in-page document state.

### 4. Spellcheck

**Observed: not fired, for the default (local) configuration, in both
vehicles.** The `notes` field's token included a deliberately misspelled
phrase ("wagess recieved teh amoutn") with `spellcheck="true"` set. Across all
four sessions (headless × 2, headed × 2), zero non-loopback network requests
were observed at all (see below) — not merely zero requests containing the
token, zero requests full stop.

**Headless vs. headed: no difference observed in the default configuration.**
This is the channel Track 1's review was least willing to accept as settled,
because headless Chrome has historically differed from headed Chrome in
spellcheck/dictionary code paths, and enhanced ("send text to Google") mode is
UI-mediated. This run's headed result narrows that specific worry for the
*default* configuration: the real, headed vehicle a person would actually type
into also attempted zero non-loopback requests during typing, undo, and
submission of a misspelled field, in both a clean and a crashed session.

Untested, and why, in both vehicles (unchanged from Track 1): Chrome's
*enhanced* spellcheck mode is opt-in and was not tested in either vehicle.
Enabling it requires either a signed-in Google account in the profile or a
Chrome preference/policy that neither `chrome.mjs`'s nor `live_viewing.py`'s
launch flags set; adding one to either would be a change to the vehicle
itself, which the charter forbids. Only each vehicle's actual default — local,
no network calls attempted for spellcheck during this run — was observed.
This is not a claim that enhanced spellcheck cannot leak typed text in either
vehicle; it is untested in both.

Confinement: contained — no data left the loopback boundary in this mode, in
either vehicle.

### 5. Anything else the browser writes on its own

**Observed: the browser wrote many files unprompted by the page in both
vehicles; none contained a token in either.** A fresh headless profile
directory after this run contained roughly 75 top-level entries even though
the served page used no JavaScript storage APIs at all. The headed vehicle's
profile directory, after the equivalent run, contained roughly 55 top-level
entries — most of the same names (`History`, `Cookies`, `Favicons`,
`Web Data`, `Login Data`, `Segmentation Platform`,
`Site Characteristics Database`, `chrome_cart_db`, `parcel_tracking_db`,
`discounts_db`, `shared_proto_db`, and more), but the headed profile did not
have several entries the headless one did:

**The most important sentence in this section is the negative, not a
positive:** no channel newly fired in the headed vehicle that had not already
fired headless — every difference below is an entry present headless and
*absent* headed, never the reverse, and none of the absent-headed entries
were found to contain a token in the headless run either. This is reported
because the difference is itself part of what Track 2 asked for, not because
it changes any channel's verdict.

Entries present in the headless profile but **not observed** in the headed
profile in this run: `Cache`, `Code Cache` (plausibly explained by
`live_viewing.py` setting a separate `--disk-cache-dir`, confirmed present as
a sibling `cache/Default/` directory instead — see below), `Network Action
Predictor`, `AutofillStrikeDatabase`, `AutofillAiModelCache`, `DIPS` /
`DIPS-wal`, `GCM Store`, `BrowsingTopicsSiteData`, `BrowsingTopicsState`,
`BudgetDatabase`, `Shortcuts`, `Web Applications`, `blob_storage`,
`heavy_ad_intervention_opt_out.db`, `optimization_guide_hint_cache_store`,
`PreferredApps`. This probe did not investigate why these specific stores are
absent headed — plausible causes include headed-vs-headless differences in
which background feature subsystems Chrome starts, lazier initialization that
the fixed ~1.8s post-submission wait in this probe did not capture, or
first-run/foreground-state differences — and does not resolve which. It is
reported as an observed fact, not explained.

**Confirmed vehicle-shape difference, not merely inferred:** `live_viewing.py`
passes `--disk-cache-dir=<workspace>/.live-view/session-<uuid>/cache`
(confirmed from source and from the `ps` command line of the launched
process). The probe found a `Default/` subdirectory inside that separate
cache directory in every headed session, consistent with Chrome's on-disk
cache having moved there rather than living inside the profile directory
`chrome.mjs`'s single `--user-data-dir` produces. This probe grepped the
whole workspace, so this relocation did not create a blind spot; no token was
found in the cache directory contents observed either.

No `IndexedDB` directory was created at all in either vehicle's profile — the
served page never called an IndexedDB API, and none appeared regardless.

Untested, and why (unchanged from Track 1, applies to both vehicles):
dictation is not applicable to this vehicle as configured in either
vehicle — headless Chrome exposes no microphone/dictation surface at all, and
both vehicles' launch flags include `--mute-audio`. Not attempted in either,
not "fired" or "not fired" in either.

Confinement: contained by construction in both vehicles — same as channel 2,
all of this is inside the confined directory each vehicle's own teardown
deletes on every clean run.

## Network egress (all channels, combined observation)

Across all four sessions (headless × 2, headed × 2), the CDP `Fetch`-domain
interception recorded **zero** requests to any origin other than the
harness's own loopback server, in every session. Nothing was blocked because
nothing outside the loopback origin was ever attempted, in either vehicle.
For the headless vehicle this is the default with
`--disable-background-networking`, `--disable-sync`, and `--disable-translate`
already set by `chrome.mjs`. For the headed vehicle, the same three flags are
set by `live_viewing.py`. Neither vehicle's flags were changed by this probe.

## Which channels differ between headless and headed (plain statement)

**None of the five channels produced a different observed result between the
headless and headed vehicles in this run.** Specifically:

1. **Form history / autofill:** not fired, both vehicles. Undetermined in
   both, for the same reason (the save-confirmation UI step was not driven in
   either), not resolved by the headed run.
2. **Session restore / crash recovery:** files written, no token, both
   vehicles. The restore-prompt half remains untested in both, for the same
   reason (neither vehicle's launch call can reuse an existing profile
   without modification).
3. **Undo buffer:** present in-page, cleared by navigation, no disk write —
   identical in both vehicles.
4. **Spellcheck (default/local):** zero non-loopback requests, both vehicles.
   Enhanced/cloud spellcheck remains untested in both, for the same reason
   (requires a vehicle-flag or account change in either).
5. **Everything else / network egress:** many unprompted writes in both
   vehicles, no token in either, zero non-loopback network requests in
   either. The headed profile's top-level entry list is a strict subset of
   the headless one in this run (a handful of feature-specific stores present
   headless, absent headed — see channel 5 above); this is a vehicle-shape
   difference this probe observed and did not explain, and it did not change
   any channel's token/network-egress result.

This narrows, but does not fully close, the two channels Track 1's review
flagged as most likely to be headless artifacts (form history and
spellcheck): the headed vehicle's *default*, no-cloud, no-explicit-save-
confirmation behavior matches the headless one exactly, in this run, on this
machine. It does not settle what a real user's actual save-confirmation
interaction or an enhanced-spellcheck-enabled profile would do in either
vehicle, because this probe drove neither in either vehicle.

## What could not be tested, summarized

- Whether a real "restore session" prompt appears on relaunch against a
  crashed profile (channel 2) — requires reusing an existing profile/session
  directory, which neither vehicle's launch call supports, and which the
  charter forbids adding to either.
- Whether accepting Chrome's own "Save this info?" prompt actually populates
  `Web Data` with the typed tokens (channel 1) — requires driving a UI
  infobar interaction this probe does not attempt in either vehicle.
- Enhanced/cloud spellcheck (channel 4) — opt-in, requires a profile
  configuration neither vehicle's launch flags set.
- Dictation — not applicable to either vehicle as configured; no channel
  exists here to exercise, in either.
- Why the headed profile's top-level entry list is missing a handful of
  headless-observed, non-token-bearing feature stores (channel 5) — observed,
  not explained; see channel 5 above.

## Charter-stop findings

None. Driving the headed vehicle did not require changing
`packages/derivation/live_viewing.py`, `packages/derivation/live_workspace.py`,
`tools/presentation_harness/lib/chrome.mjs`, or `lib/server.mjs`. A real
window server was present on this machine and a real headed browser window
was observed to launch and close normally. No channel required touching real
data. No typed content was observed leaving the machine over the network in
either vehicle.

## Track 2 repair, Part 1 — widened search, outside the confined directory

Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-28-entry-boundary-track2-repair.md`.
Everything above searched only inside the directory
`packages/derivation/live_viewing.py` itself manages
(`.live-view/session-<uuid>/{profile,cache,downloads}` and the print target).
The Track 2 review found that region insufficient to settle the ADR's central
claim: it does not say whether the resolved Chrome binary writes anything to
a fixed, per-user-account location no launch flag redirects. This section
widens the search to real per-user macOS locations outside that tree, on the
same machine, against the same unmodified headed vehicle
(`packages/derivation/live_viewing.py`, driven via the same unmodified
`headed_launch.py` bridge), exercising the same **crash** path (`SIGKILL`, no
clean close).

**Result, stated as one of the three possible outcomes named by the charter:
something was written outside the confined directory, but it holds no typed
content.** This is not "nothing was found" and it is not "typed content was
found" — it is the middle outcome, and it is a real, verified fact rather
than an inference from timing.

### Method

`tools/entry_probe/probe.mjs` gained a `--wide-search` flag (see its README
for the full method note). Summary: a marker file is touched immediately
before the headed vehicle launches; after the crash and the existing
confined-directory grep run, every candidate location is asked which entries
have a **creation** time (macOS `stat -f %B`, birthtime — not mtime) at or
after the marker's, via `find <root> -maxdepth 5 -newer <marker>` followed by
a per-candidate birthtime check. Birthtime, not mtime, is the operative
filter: this machine's own real, independently-running Chrome install (56
processes, confirmed via `ps` before this run started — an ordinary,
unrelated, already-running user session, not anything this probe launched)
continuously *modifies* pre-existing files in its own profile without
*creating* new ones most of the time, so an mtime-only diff would have been
swamped by that unrelated activity. Any new file the scan turns up is grepped
for the same synthetic tokens the rest of this probe uses (`-rla`, the
corrected flag).

Candidate locations searched (macOS, per the charter's own list): the
per-user crash-report directories (`~/Library/Logs/DiagnosticReports`,
`~/Library/Application Support/CrashReporter`), the per-user caches directory
(`~/Library/Caches`), `$TMPDIR` and `/tmp`, and the Chrome/Chromium per-user
application-support directories (`~/Library/Application Support/Google`,
`~/Library/Application Support/Chromium`). Run twice (clean-ish `SIGTERM` and
crash `SIGKILL`), both against the headed vehicle only — the vehicle a person
actually types into, which is what this repair is about.

### What was found, and where it was verified independently of the probe

Both headed runs (clean-ish and crash) turned up the same category of
finding: a new directory named `com.google.Chrome.<six random characters>`
created directly under `$TMPDIR` — **a sibling of, not a descendant of,**
this run's confined `.live-view/session-<uuid>/` tree. This is exactly the
shape of finding the charter's outcome 2 describes.

This was not accepted on the wide-search scan's word alone. It was
independently reproduced and checked by hand against the actual OS process:
launched the headed vehicle directly via `headed_launch.py` against a fresh
synthetic workspace, found its real Chrome pid by the same external `ps`
method the rest of this probe uses, then ran `lsof -p <that exact pid>` —
process-level evidence of what file descriptors *this specific process*
holds open, not an inference from timestamps or naming. Result: the pid
matching this run's `--user-data-dir=<our confined workspace>` held an open
Unix-domain-socket file descriptor at
`$TMPDIR/com.google.Chrome.<random>/SingletonSocket` — a path entirely
outside the confined directory this vehicle computes and checks with
`_within()`. This ties the artifact to this exact vehicle instance, not to
the machine's independently-running real Chrome, and not to coincidence.

**What is in it, checked directly:** the directory holds exactly two entries,
in every case observed (four separate launches, including the two full
`--wide-search` probe runs and two hand-verification runs):

- `SingletonSocket` — an anonymous Unix domain socket (`srwx------`, 0 bytes
  reported by `ls`/`stat`; a socket has no "content" in the file-bytes sense).
- `SingletonCookie` — not a regular file. It is a symlink whose **target
  string itself** is the payload: a random 15-19 digit number
  (e.g. `5358790730500827854`), used as an authentication token for the
  single-instance IPC protocol this pair implements. `cat`ing it returns
  nothing (`file` reports it as "broken symbolic link to <the number>" —
  the target is never meant to exist as a real path). No form field's typed
  value, no token planted by this probe, and nothing resembling either
  appeared in this string in any of the four checked instances.

**Survival across a crash, checked directly:** in the hand-verification run,
the directory and both entries were confirmed present, unchanged, after
`SIGKILL` to the browser process — the same orphaning behavior ADR-0048
already documents for the confined session directory applies here too, and
nothing in `live_viewing.py`'s `close()`/`_remove_session()` path touches
this location even on a clean exit, because it is never inside the tree
`close()` manages.

**Accumulation, observed independently of this run:** while cleaning up
after this probe's own runs, more than a dozen `com.google.Chrome.<random>`
directories were found already present under `$TMPDIR`, dated across the
prior two days — plausibly from this milestone's own earlier Track 1b runs
and/or other Chrome invocations on this machine, not created or explained by
this session. Nothing on this machine appears to sweep this location ever;
it is an orphan-accumulation surface in addition to, not instead of, the one
ADR-0048 already names for the confined tree.

### What did not turn up anything

- **No token, in either run, in the singleton directory or anywhere else the
  widened scan checked.** The main grep of the confined directory (unchanged
  from the rest of this note) also found nothing.
- **No entry appeared in either OS crash-report location**
  (`~/Library/Logs/DiagnosticReports`, `~/Library/Application
  Support/CrashReporter`) in either run. Consistent with how macOS's own
  crash reporter works: it is invoked for signals a process does not itself
  handle in a way the OS recognizes as a crash (`SIGSEGV`, `SIGABRT`,
  `SIGBUS`, etc.), not for `SIGKILL`, which gives the target process no
  chance to do anything at all, and gives the OS no "crash" to report either.
  This narrows what `SIGKILL` as this milestone's proxy for "the controlling
  process dies without warning" can tell us about that specific OS-level
  channel — it is a real absence, but not evidence that a different kind of
  crash (one the OS's own reporter would catch) behaves the same way.
- **No new entry in `~/Library/Caches` attributable to this vehicle.** The
  crash run's scan did turn up 41 new entries under `~/Library/Caches`, all
  under `com.apple.helpd/` (Spotlight/Help-system indexing artifacts) — an
  unrelated OS background process re-indexing help content during the test
  window, not this vehicle; none held a token, none were Chrome- or
  Chromium-named, and this vehicle has no plausible mechanism to write there.
  Named here as a confound ruled out, not a finding.
- **No new entry under `~/Library/Application Support/Google` attributable
  to this vehicle.** Both runs showed exactly one changed file,
  `Chrome/CrashpadMetrics-active.pma`, inside Matt's own, already-running,
  independent Chrome installation's default profile location (not this
  vehicle's confined one — the path does not contain this run's workspace at
  all, and the vehicle never launches against that profile). This is the
  real browser's own periodic metrics-file churn, unrelated to this test;
  named here as a confound ruled out, not a finding. No token was present.
- **`~/Library/Application Support/Chromium` does not exist on this
  machine** (only Google Chrome is installed; `_resolve_browser()` in
  `live_viewing.py` picked Google Chrome, confirmed from the actual launched
  process's binary path). This candidate could not be exercised on this
  machine.

### What this settles, and what it does not

This is direct, process-level, reproduced evidence that the resolved Chrome
binary on this machine creates a filesystem artifact **outside** every
destination `_confined_destinations()` computes and `_within()` checks —
refuting, as a fact rather than an open question, the claim that the
vehicle's confinement is "already total." It also, in the same breath,
supports the ADR's narrower "no typed content escaped" framing for this
specific artifact: what escapes is an IPC authentication token and an
unconnected socket, not anything a person typed.

This remains **one observation, on one machine, on one resolved Chrome
build, for one specific channel (the single-instance-lock mechanism)**. It
does not settle the crash-reporter/Crashpad-database question the ADR's
"Weakest point" section raises — no Crashpad-named artifact appeared outside
the confined directory in either run on this machine, which is itself worth
recording (see below), but the absence of one specific channel's escape is
not proof no channel escapes, and this observation should not be read as
having tested every channel a different Chrome version, OS version, or
account configuration might exercise.

**On the Crashpad question specifically:** no `Crashpad`-named directory or
file was observed newly created outside the confined tree in either run on
this machine — the only Chrome-attributable artifact found outside
confinement was the singleton-lock pair described above, not a crash-report
database. This narrows, but does not close, the "Weakest point" section's
open question about a fixed, un-redirected crash-reporter database location;
it is evidence of one specific absence on one machine, not a mechanism ruling
the possibility out in general.

### Charter-stop findings (Part 1)

None triggered. This finding is the charter's outcome 2 ("something was
written but holds no typed content"), not outcome 3 ("typed content found
outside the boundary") — the stop-and-report-first condition does not apply.
It is nonetheless reported first and plainly, as the charter asks for the
most significant finding of this repair, because it is direct, verified
evidence against the ADR's strongest wording, not merely an unresolved
question.
