# Entry Boundary — Track 1 retention-probe findings

Evidence ceiling: **observation on synthetic fixtures only.** Everything below
is what `tools/entry_probe/probe.mjs`, driving the existing confined
invocation vehicle (`tools/presentation_harness/lib/chrome.mjs` +
`lib/server.mjs`, unmodified), observed on one machine in one run. It is not a
claim about what Chrome does in general, about a non-headless Chrome, about
any other browser, or about real data. It reports observations; it does not
recommend a write path or say whether a browser form is acceptable — that is
Track 2's question to answer, and it may reach a different conclusion than
what these observations seem to suggest.

Probe: `tools/entry_probe/probe.mjs`. Fixture: `tools/entry_probe/form.html`.
Full method notes: `tools/entry_probe/README.md`.

## Method summary

- Launched headless Chrome (`--headless=new`, plus the other flags already in
  `chrome.mjs`: `--disable-extensions`, `--disable-background-networking`,
  `--disable-sync`, `--disable-translate`, `--mute-audio`) against a fresh
  disposable profile, twice.
- Served `form.html` — five text inputs with realistic `name`/`id`/`type`/
  `autocomplete` (`fullName` autocomplete=name, `ssn` autocomplete=off,
  `wages` autocomplete=off, `email` autocomplete=email, `notes`
  autocomplete=off, deliberately including a misspelled phrase) — from the
  harness's own loopback-only server.
- Typed a distinct synthetic token per field via real CDP-dispatched
  keystrokes (`Input.dispatchKeyEvent`, matching the event shape a genuine
  keypress produces), read the DOM back to confirm each field held the
  intended value verbatim, then submitted the form (a real navigation).
- Ran this once through to a **clean-ish close** (the probe sends the Chrome
  process `SIGTERM` itself and waits for exit) and once through to a
  **simulated crash** (`SIGKILL`, no warning).
- In both cases the probe finds the browser's OS pid and profile directory by
  reading `ps` output — pure external process inspection, `chrome.mjs` was
  not modified — signals the process itself rather than calling
  `chromeHandle.dispose()` (whose own last act is to delete the profile
  directory, which would destroy the evidence first), waits for exit, then
  greps the still-on-disk profile recursively and binary-safely
  (`grep -rla <token> <profileDir>`) before deleting it itself.
- Every non-loopback network request attempted during the whole run was
  captured via the CDP `Fetch` domain (the same block-and-record pattern
  `executor.mjs` already uses) and checked for the tokens, in the URL and any
  POST body.

**Method correction made during this work, stated because it would otherwise
look like a silent negative:** the grep step originally used `grep -rlaI`.
`-I` on this system's `grep` (`ugrep`) means "treat a binary file as
non-matching" — the opposite of what `-a` ("treat binary as text") is for.
That combination silently suppressed every match inside a binary store
(SQLite, LevelDB) for two full runs. It was caught only by a positive-control
test (planting a known token inside a synthetic binary file and confirming
`grep -rlaI` failed to find it while `grep -rla` did) before any finding
below was written down. The flag was removed. Every result below is from the
corrected `grep -rla` and was independently re-confirmed against a
positive-control token.

**Typing artifact caught and fixed the same way:** an early version of
`typeInto()` set the `text` property on `keyDown`, `char`, and `keyUp` CDP
events, which double-inserted every character (confirmed by reading the DOM
value back: `ENTRYPROBE` came back as `EENNTTRRYYPPRROOBBEE...`). Fixed to
carry `text` only on the `char` event, matching how a real keypress is
represented in three CDP events; the DOM readback then matched the intended
token exactly, and the probe now asserts that readback on every run.

## Findings by channel

### 1. Form history / autofill

**Observed: not fired.** `Default/Web Data` (the SQLite store Chrome's
autofill/form-history feature writes to) existed in both profiles after
close and was grepped with the rest of the tree; no token appeared in it or
anywhere else. This held for the `autocomplete=off` fields (`ssn`, `wages`,
`notes`) and, notably, also for the fields given realistic non-off
autocomplete hints (`fullName` → `autocomplete="name"`, `email` →
`autocomplete="email"`) that are exactly the ones a real autofill heuristic
would be expected to key off. No distinction in outcome was observed between
the two groups in this headless, single-submission run.

Confinement: N/A — nothing was found to contain.

### 2. Session restore and crash recovery

**Observed: fired (files are written), but did not contain the typed
values.** `Default/Sessions/` was empty in a bare `about:blank` sanity check
with no navigation, but after the form-navigation flow it held real files in
both scenarios — `Session_<id>` and `Tabs_<id>` after the clean-ish close;
`Session_<id>` only after the simulated `SIGKILL` crash (no `Tabs_` file that
time, itself a same-vehicle observation, not further interpreted here).
`Default/Session Storage/` (a separate LevelDB store) also had real content
(`000003.log`, `CURRENT`, `LOCK`, `LOG`, `MANIFEST-000001`) in both cases.
The whole-tree grep covered these files along with everything else in the
profile and found no token in any of them.

Untested, and why: whether relaunching Chrome pointed at the **same**
(crashed) profile would actually surface a "restore pages" prompt — the
behavioral part of "crash recovery," not just whether bytes get written —
was not tested. `chrome.mjs`'s `launchChrome()` always creates a fresh
`mkdtemp` profile per call and has no parameter to reuse an existing one;
exercising a same-profile relaunch would require adding one, which the
charter forbids touching. Only "were crash-recovery bytes written, and do
they contain the typed values" was tested, not "does the browser then offer
to restore them."

Confinement: contained by construction under normal harness operation —
`chrome.mjs`'s own `dispose()` deletes this whole directory, including these
files, on every clean run. This probe bypassed only `dispose()` itself (not
`chrome.mjs`) to see the files before that deletion.

### 3. Undo buffer persistence

**Observed: present in-memory within the page, cleared by navigation, never
touched disk.** After typing the `notes` token, the field was cleared
(`execCommand('delete')`) and `execCommand('undo')` was called: the full
token came back exactly (confirmed byte-for-byte once the typing artifact
above was fixed). The page was then navigated away and back to the same
form; calling `undo` again on the now-fresh `notes` field returned an empty
string — the undo stack did not survive the navigation. No token from this
sequence appeared anywhere in the profile-directory grep.

Confinement: N/A — this channel does not appear to write to disk at all in
this vehicle; it lives and dies with the renderer's in-page document state.

### 4. Spellcheck

**Observed: not fired, for the default (local) configuration only.** The
`notes` field's token included a deliberately misspelled phrase
("wagess recieved teh amoutn") with `spellcheck="true"` set. Across both
sessions, zero non-loopback network requests were observed at all (see
below) — not merely zero requests containing the token, zero requests full
stop.

Untested, and why: Chrome's *enhanced* ("send text to Google for improved
spellchecking") mode is opt-in and was not tested. Enabling it requires
either a signed-in Google account in the profile or a Chrome preference/
policy that none of `chrome.mjs`'s existing launch flags set; adding one
would be a change to `chrome.mjs` itself, which the charter forbids. Only
the vehicle's actual default — local, no network calls attempted for
spellcheck during this run — was observed. This is not a claim that
enhanced spellcheck cannot leak typed text; it is untested here.

Confinement: contained — no data left the loopback boundary in this mode.

### 5. Anything else the browser writes on its own

**Observed: the browser wrote many files unprompted by the page; none
contained a token.** A fresh `Default/` profile directory after this run
contained roughly 70 top-level entries even though the served page used no
JavaScript storage APIs at all: `History`, `Cookies`, `Favicons`,
`Top Sites`, `Network Action Predictor`, `Login Data`, `Web Data`,
`Extension State`, several Chrome-feature-specific SQLite/LevelDB stores
unrelated to this page (`chrome_cart_db`, `parcel_tracking_db`,
`discounts_db`, `optimization_guide_hint_cache_store`,
`shared_proto_db`, `AutofillStrikeDatabase`, `Segmentation Platform`, and
more), `GPUCache` and `Code Cache`, and `Preferences`/`Secure Preferences`.
The whole-tree grep covered every one of these and found no token in any of
them. No `IndexedDB` directory was created at all in this profile — the
served page never called an IndexedDB API, and none appeared regardless.

Untested, and why: dictation is not applicable to this vehicle as
configured — headless Chrome exposes no microphone/dictation surface, and
`chrome.mjs` already launches with `--mute-audio`; there is no channel here
to exercise. Not attempted, not "fired" or "not fired."

Confinement: contained by construction — same as channel 2, all of this is
inside the disposable profile directory that `chrome.mjs`'s own `dispose()`
deletes on every clean run.

## Network egress (all channels, combined observation)

Across both sessions, the CDP `Fetch`-domain interception recorded **zero**
requests to any origin other than the harness's own loopback server. Nothing
was blocked because nothing outside the loopback origin was ever attempted.
This is the vehicle's current default with `--disable-background-networking`,
`--disable-sync`, and `--disable-translate` already set by `chrome.mjs`; it is
not evidence about a differently configured browser.

## What could not be tested, summarized

- Whether a real "restore session" prompt appears on relaunch against a
  crashed profile (channel 2) — requires reusing an existing profile
  directory, which `chrome.mjs` does not support and which the charter
  forbids adding.
- Enhanced/cloud spellcheck (channel 4) — opt-in, requires a profile
  configuration this vehicle's launch flags don't set.
- Dictation — not applicable to this headless, muted-audio vehicle; no
  channel exists here to exercise.

## Charter-stop findings

None. Driving the confined vehicle did not require changing
`chrome.mjs` or `server.mjs`; no channel required touching real data; no
typed content was observed leaving the machine over the network.
