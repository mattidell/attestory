# Review — Entry Boundary, Track 1: the retention probe

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-28-entry-boundary-track1-review.md`
- Branch: `milestone/entry-boundary`, reviewed commit `a33458a`
- Object: `tools/entry_probe/` (probe, form fixture, README) and
  `docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-boundary-retention-findings.md`
- Envelope scan: `python3 tools/envelope_scan.py --range main..HEAD` — clean,
  exit 0, no output.
- `pytest -n auto`: `670 passed, 2451 subtests passed` on this branch, run
  independently by this review, not accepted from the builder's report.
- `tests/test_kernel_fixtures.py` (fixture-safety scan): `2 passed, 5 subtests
  passed`.

## The charter's central claim, verified independently

The charter states the Builder drove the headless synthetic evaluation
harness rather than the headed vehicle a person would actually type into. I
verified this from source rather than accepting it:

- `tools/presentation_harness/lib/chrome.mjs` line 80 hardcodes
  `"--headless=new"` in the Chrome launch args, unconditionally, with no
  parameter to disable it.
- `packages/derivation/live_viewing.py`'s `LiveViewingVehicle.launch()`
  builds its own `args` list independently (it does not call into
  `chrome.mjs` at all) and never passes `--headless`. The module's own test
  suite (`tests/test_presentation_live_viewing_vehicle.py`,
  `test_destinations_are_inside_capability_and_browser_is_headed`) asserts
  `assertNotIn("--headless=new", args)` — the headed property is already a
  checked contract of this module, not an inference of mine.
- ADR-0047 ("Live Viewing Environment") is the record that defines this
  vehicle and its confinement rationale; it is the accepted mechanism a
  person actually views real tax content through.
- `git diff 8d41cc2..a33458a -- tools/presentation_harness/` is empty:
  `chrome.mjs` and `server.mjs` are byte-identical to base. The probe
  imports them unmodified, as claimed.

**The claim is correct.** Track 1's probe drove
`tools/presentation_harness/lib/chrome.mjs` (`--headless=new`, hardcoded),
which is a different code path from `packages/derivation/live_viewing.py`
(no headless flag, different launch args, different confined-destination
shape keyed off a `WorkspaceCapability` rather than a bare temp dir). These
are not two configurations of the same vehicle; they are two different
pieces of code. The charter's attribution — that this is a charter defect
(the foreman named the wrong vehicle) rather than a Builder defect — also
holds: the Builder's charter explicitly named `chrome.mjs` as "the existing
confined invocation vehicle," and the Builder built exactly that, correctly,
including catching and fixing two of its own method bugs along the way.

## Measurement 1 — is each "not fired" a confinement fact or a headless artifact?

Answered per channel, not as one blanket answer, because the evidence differs:

- **Form history / autofill (channel 1).** **Undetermined by reading.**
  Nothing in `chrome.mjs`'s flag list disables Chrome's autofill/form-history
  subsystem explicitly (no `--disable-features=Autofill...` or similar); the
  only headless-related input is `--headless=new` itself. Whether Chrome's
  autofill-save heuristic is suppressed, altered, or unaffected in headless
  mode is an empirical property of Chrome's own internals, not something
  this repository's source settles. This is exactly the channel the charter
  is most worried about, and I cannot close it from reading alone — it needs
  the headed vehicle.
- **Session restore / crash recovery (channel 2).** **Partially settled, in
  the direction that undercuts the "it's just headless" worry, but only
  partially.** The note itself reports that `Sessions/` and `Session
  Storage/` files *were* written in headless mode — the byte-writing part of
  this channel fired. What is genuinely untested (and the note says so) is
  whether relaunching against the same crashed profile produces an actual
  "restore pages" UI prompt — that is inherently a headed-mode-only
  behavior (headless has no such prompt to show), so this half of the
  channel cannot be tested by any headless run, headless-artifact or not.
- **Undo buffer (channel 3).** **Low risk of being a headless artifact.**
  This is Blink's in-page editing/undo stack, driven through
  `execCommand`, not a browser-chrome feature gated by `--headless`. I have
  no code-level evidence that headless mode changes this behavior, but I
  also cannot prove a negative from reading alone; I'd call this channel
  "likely representative" rather than "settled."
- **Spellcheck (channel 4).** **This is the channel I am least willing to
  accept as settled, and the one that matters most.** The note's finding —
  zero non-loopback network requests observed at all — is the highest-value
  possible result if it generalizes, and the highest-risk possible false
  negative if it does not. Headless Chrome has historically differed in
  spellcheck/dictionary and enhanced-spellcheck code paths from headed
  Chrome (the "send text to Google for improved spellchecking" toggle is a
  UI-mediated preference), and I cannot rule out from source that
  `--headless=new` simply never attempts the enhanced path regardless of
  configuration, independent of any confinement `chrome.mjs` provides. I
  am reporting this as **undetermined**, not refuted — the note itself
  is honest that enhanced spellcheck specifically was not tested, but the
  *default*-mode "not fired" result is exactly the one most plausible to be
  a headless artifact rather than a confinement property, and it is the
  worst channel to get wrong.
- **Everything-else channel (channel 5 / network egress).** **Likely
  representative.** `History`, `Cookies`, `Web Data`, `Favicons`, and the
  ~70-entry profile scaffold are core profile-initialization writes that
  Chrome performs regardless of headless/headed status; I have no reason
  from reading to believe these differ. Network egress capture (CDP
  `Fetch` domain) is a browser-protocol-level interception that should work
  identically headed or headless.

**Net answer to Measurement 1:** two of five channels (form history,
spellcheck) are genuinely undetermined as to whether "not fired" reflects
the confinement or the harness's headless mode, and spellcheck is the
higher-stakes of the two. One channel (session restore) is split — the
byte-writing half is confirmed to fire in headless, the behavioral
restore-prompt half is untestable in headless by construction. This is
answered, per the charter's own bar, not resolved to a single verdict.

## Measurement 2 — can `live_viewing.py` be driven synthetically?

Read-only investigation, as instructed; the module was not modified or run.

**Requirements to launch, read from the module:**

- A `WorkspaceCapability` (`packages/derivation/live_workspace.py`), whose
  only load-bearing field for `launch()` is `location: Path`, checked only
  via `capability.location.is_dir()`. Nothing about it requires a real
  residency — the module's own test suite constructs it from a bare
  `tempfile.TemporaryDirectory()` throughout
  (`tests/test_presentation_live_viewing_vehicle.py`, `_capability()`).
  **This requirement is trivially satisfiable synthetically.**
- A resolvable Chrome/Chromium executable, found by the same fixed
  candidate-path list `chrome.mjs` uses (or an explicit
  `chrome_executable=` override, which the test suite exercises with a
  throwaway shell-script stand-in). Since the entry probe already located a
  real Chrome on this machine to drive `chrome.mjs`, the same binary would
  resolve here. **Satisfiable, and already proven available on this
  machine.**
- Confined destinations are computed entirely from the capability's
  `location` — `location/.live-view/session-<uuid>/{profile,cache,
  downloads,print/view.pdf}` — with symlink and containment checks
  (`_within`, `_confined_destinations`). None of this needs a real fact or
  a real workspace; a synthetic empty temp directory satisfies every check
  the module performs.
- The module launches via `subprocess.Popen` directly (or an injected
  `process_factory`), waits on a `DevToolsActivePort` file the same way
  `chrome.mjs` does, and returns a `LiveViewingSession` whose
  `websocket_url` is the CDP endpoint. `LiveViewingSession.navigate()` only
  *validates* a URL is loopback (`_validate_navigation_url`); it does not
  itself drive the browser. Any actual typing/reading/grepping of the
  profile would have to be done externally against that `websocket_url`,
  the same way `probe.mjs` currently does against `chromeHandle.wsUrl` — the
  existing `cdp.mjs`, `typeInto()`, and `grepDirForTokens()` machinery in
  `tools/entry_probe/probe.mjs` is reusable as-is against this different
  endpoint, in a future track, not by me.

**One requirement the module's own tests do not exercise and I could not
settle by reading: a real, non-headless Chrome process needs an actual
window server / display to launch successfully at all** (this is a property
of Chrome, not of this module — headed Chrome without a display server
typically fails to start or hangs). The existing test suite mocks the
process entirely (`_SyntheticProcess`, a fake `process_factory`) and never
launches real Chrome, headed or otherwise, so it gives no evidence either
way about whether *this machine or whatever machine ultimately runs Track 2*
has a display available. I did not test this — doing so would mean running
the module, which is out of scope for me — but it is the one concrete
precondition that could turn "cheap" into "blocked," and it should be the
first thing a corrected Track 1 checks, before writing any probe code.

**Answer to Measurement 2:** a corrected Track 1 against `live_viewing.py`
is **cheap at the code level and not blocked by anything I read** — the
vehicle's synthetic-workspace requirements are already proven satisfiable by
its own test suite, and the driving mechanics (CDP over the returned
websocket) are the same shape the existing probe already implements against
a different launcher. The one open precondition — whether a headed browser
can actually open a window in whatever environment runs the probe — is an
operational fact, not a code fact, and this review could not and did not
test it.

## Measurement 3 — is the negative result trustworthy on its own terms?

- **The typing-artifact fix is real and now self-checked.** `probe.mjs`
  carries `text` only on the CDP `char` event (lines 107–111), and the probe
  asserts a DOM readback matches the intended token exactly on every run
  (lines 214–228) — this is not merely a claim, it is an executable
  assertion in the committed code.
- **The grep-flag fix is real, and I independently reproduced its
  mechanism** rather than trusting the note's account. On this machine's
  `grep` (`ugrep 7.5.0`), planting a token in a binary file:
  `grep -rlaI TOKEN file` exits 1 (no match — silently wrong);
  `grep -rla TOKEN file` exits 0 (found). The shipped `grepDirForTokens()`
  in `probe.mjs` (line 181) uses `-rla`, matching the fix described in the
  note.
- **One gap: the note's specific claim of a "positive-control test" (a
  token planted in a synthetic binary file, confirming `-rlaI` failed while
  `-rla` succeeded) is not preserved anywhere in the committed repo as a
  script, fixture, or re-runnable check** — it is asserted narrative only.
  I could not verify that *specific* test was performed, only that the
  general mechanism it describes is real (which I confirmed independently
  above) and that the shipped code reflects the corrected flag. This is a
  minor traceability gap, not a correctness problem: the underlying claim
  is true and reproducible; its specific verification-history is simply not
  load-bearing evidence in the artifact itself.
- **Every finding in the note is consistent with post-correction code.**
  There is only one committed version of `probe.mjs`; there is no evidence
  of a pre-correction commit whose findings leaked into the note.

**Measurement 3 passes**, with the one gap noted above as non-blocking.

## Measurement 4 — does the note stay inside its evidence ceiling?

Read the full findings note against this bar. It consistently:

- States its evidence ceiling at the top and repeats scoped hedges
  ("in this headless, single-submission run," "this vehicle," "not a claim
  about... any other browser, or about real data").
- Reports "observed: not fired" / "observed: fired" per channel without
  reaching for "therefore acceptable" or "therefore unacceptable" language.
- Explicitly declines to answer Track 2's question in its own framing
  paragraph and again in the closing summary.

I found no sentence that leans toward a verdict Track 2 has not made. **This
measurement passes.**

## Measurement 5 — boundary compliance

- Tokens (`ENTRYPROBE-NAME-<hex>`, `ENTRYPROBE-SSNFIELD-<hex>`,
  `ENTRYPROBE-WAGES-<hex>`, `entryprobe-<hex>@example.invalid`,
  `ENTRYPROBE-NOTES-<hex> wagess recieved teh amoutn`) are obviously
  synthetic, clearly prefixed, and do not resemble real SSN/EIN/account-number
  shapes.
- `git show a33458a` and its commit message contain no real path, no
  fragment of one, and no derived identifier — checked by direct grep, not
  by trusting the structure (`grep -niE "/Users/|residenc|\.attestory|workspace-root|/home/"` over the
  full commit diff: no hits).
- `grep -rn "entry_probe"` across CI/verify/test-suite configuration finds
  no wiring anywhere outside the probe's own directory and the review/plan
  documents that reference it in prose. Not wired into CI or `verify`.
- `git diff 8d41cc2..a33458a -- tools/presentation_harness/` is empty:
  `chrome.mjs` and `server.mjs` are unmodified, verified against base
  rather than taken on the claim.
- `python3 tools/envelope_scan.py --range main..HEAD` returns clean.

**Measurement 5 passes.**

## Measurement 6 — is "untested" honest?

Three items are recorded as untested: the restore-session prompt on
relaunch, cloud spellcheck, and dictation.

- **Restore-session prompt.** Confirmed genuinely blocked within charter
  scope: `chrome.mjs`'s `launchChrome()` calls `mkdtemp()` for a fresh
  profile on every invocation and has no parameter to reuse an existing
  (crashed) profile directory. Adding one would be exactly the kind of
  vehicle modification the charter forbids. Honest.
- **Cloud/enhanced spellcheck.** Confirmed genuinely blocked: none of
  `chrome.mjs`'s hardcoded flags set a policy or preference enabling
  enhanced spellcheck, and doing so would again require modifying the
  vehicle. Honest, though see Measurement 1 — the *default* spellcheck
  result recorded as "not fired" carries more uncertainty than "untested"
  alone conveys, because it may also be a headless artifact rather than a
  confinement property.
- **Dictation.** Confirmed inapplicable as stated: headless Chrome exposes
  no microphone/dictation surface, and `--mute-audio` is already set. There
  is no channel to exercise here regardless of vehicle. Honest.

Nothing else appears quietly left out relative to the charter's channel
list; the note also names a channel the charter didn't explicitly ask for
(the ~70-entry unprompted profile scaffold) rather than omitting it.

**Measurement 6 passes.**

## Verdict

Measurements 3 through 6 pass (one minor, non-blocking traceability gap
under Measurement 3). Measurements 1 and 2 are answered, as the charter
requires, not resolved to a single clean verdict — and that is itself the
finding.

**Which situation the foreman is facing:**

**The findings stand only for headless mode, and Track 1 needs a second run
against the headed vehicle before Track 2 can use them.**

This is not the middle option by default — it follows from the specific
answers above. Three of five channels (session-restore's behavioral half,
form history, and — the one that matters most — spellcheck) cannot be
confirmed to generalize from `chrome.mjs`'s headless run to
`packages/derivation/live_viewing.py`'s headed one, because they are
plausible candidates for exactly the kind of headless-suppresses-the-real-
behavior artifact the charter worried about, and I could not close that gap
by reading source. The other two channels (undo buffer, and the
unprompted-write / network-egress observations) are lower-risk and likely
representative, but "likely" is doing real work in that sentence — this
review did not prove it.

At the same time, Measurement 2 found no reason to think a corrected run is
expensive or blocked: `packages/derivation/live_viewing.py` is drivable
against a synthetic workspace with the same shape of evidence
(`WorkspaceCapability` over a bare temp directory, a resolvable local Chrome
binary, CDP over the returned websocket) that the existing probe already
knows how to produce, contingent on one operational precondition — a real
display/window server being available wherever that probe runs — that this
review could not test and flags as the first thing to check before writing
any new code.

**Recommendation to the foreman:** Track 1 is sound work against the wrong
target, not unsound work. The Builder should not be graded down. The
correction is a second, focused probe run against
`packages/derivation/live_viewing.py` instead of `chrome.mjs` — reusing the
existing probe's CDP-driving machinery against the headed vehicle's
`websocket_url` — prioritizing the spellcheck and form-history channels,
before Track 2 (the ADR deciding whether a browser form is acceptable) treats
these findings as settled evidence.
