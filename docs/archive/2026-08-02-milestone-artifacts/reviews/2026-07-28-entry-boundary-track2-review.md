# Review — Entry Boundary, Track 2: ADR-0048, with Track 1b folded in

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-28-entry-boundary-track2-review.md`
- Branch: `milestone/entry-boundary`, at `f2c1b22`
- Object: `docs/adr/0048-entry-boundary.md` and its `docs/adr/INDEX.md` row;
  Track 1b (`513ff93`) folded in
- Envelope scan: `python3 tools/envelope_scan.py --range main..f2c1b22` — clean,
  exit 0, no output.
- `pytest -n auto`: `670 passed, 2451 subtests passed`, run independently on
  this branch, not accepted from any report.

## Orientation note

`python3 tools/build_orientation_block.py --ref main --role reviewer` reports
a topic mismatch (`docs/phase-state.md` on `main` still names
`real-return-phase-close`). That is expected: this milestone's phase-state
updates live on `milestone/entry-boundary`, which has not merged to `main`
yet. I read the charter and `docs/phase-state.md` on this branch directly
(current_role names "Foreman — Entry Boundary, Track 2 (ADR-0048) chartered
and in flight", consistent with the charter I was given) and proceeded on
that basis rather than treating the mismatch as a stop condition, since it is
explained by normal pre-merge branch state, not by a wrong pickup.

## Measurement 1 — does the confinement claim actually cover everything Chrome writes?

Read `packages/derivation/live_viewing.py` directly, independent of the ADR's
own account.

**What is verified, from source:**

- `_confined_destinations()` computes exactly four destinations —
  `profile`, `cache`, `downloads`, `print_to_file` — all descendants of
  `capability.location/.live-view/session-<uuid>/`, checked with `_within()`
  against the resolved residency root twice (before and after directory
  creation), with an explicit symlink refusal at both checks. This mechanism
  is real, correctly implemented, and independent of whatever Chrome chooses
  to do with the paths it is given. This part of the ADR's claim holds.
- `launch()`'s Chrome argument list is: `--no-first-run`,
  `--no-default-browser-check`, `--disable-extensions`,
  `--disable-background-networking`, `--disable-sync`, `--disable-translate`,
  `--mute-audio`, `--disable-gpu`, `--user-data-dir=<profile>`,
  `--disk-cache-dir=<cache>`, `--download-default-directory=<downloads>`,
  `--print-to-pdf=<print_to_file>`, `--remote-debugging-port=0`, plus
  `--no-sandbox` only under `getuid() == 0`. **There is no
  `--disable-breakpad`, `--disable-crash-reporter`, `--crash-dumps-dir=`, or
  any other flag that disables or redirects Chrome's own crash-reporting
  subsystem.** This is a positive, source-verified fact, not an inference:
  the module does not attempt to address this channel at all, in either
  direction.
- `--disable-gpu` **is** present, and it is directly relevant to the
  GPU-shader-cache half of the concern the ADR's own "Weakest point" section
  raises — a disabled GPU process very plausibly writes little or nothing to
  a shader cache regardless of where that cache would otherwise live. The
  ADR's "Weakest point" and "Left undecided" sections do not mention this
  flag at all, so they neither credit it as a partial mitigant nor explain
  why it doesn't settle the question. I can't settle from source alone
  whether `--disable-gpu` fully suppresses GPU-process shader-cache writes
  on every Chrome build (some builds still launch a software-fallback GPU
  process for compositing or WebGL) — that is a real, version-dependent
  behavior this module's source does not pin down.

**What is not determined by reading, and what would settle it:** whether the
Chrome binary actually resolved on a given machine places a crash-reporter
database inside `--user-data-dir` (some Chromium builds have) or at a fixed,
un-redirected per-account location (some builds have done this historically,
for crash reports specifically). Source reading cannot settle this; it
requires either authoritative version documentation for the exact resolved
binary or an empirical test: repeat Track 1/1b's crash probe (`SIGKILL` to
the browser process), but widen the post-crash filesystem inventory beyond
the confined session directory and the synthetic workspace root to the whole
home directory / standard OS crash-log locations, and check whether any new
file appears outside `.live-view/session-<uuid>/`. Neither Track 1 nor Track
1b did this — both greps were scoped to the workspace/session tree, which is
exactly the region this gap says might not be exhaustive. **This is
undetermined, not refuted, and the ADR is candid about that in its own
"Weakest point" section** — that candor is real and I confirm it against the
source rather than taking it on trust.

**Where the ADR's own wording overstates what it just conceded.** The
"Decision 1 — answer" section states: "No new retention channel this project
has not already named would escape confinement, because confinement does not
depend on knowing which channel exists — it depends only on where the
browser is allowed to write, which is already total." Read against the
source, "already total" is not correct as written: the vehicle confines
exactly four named destinations, and the launch arguments leave the
crash-reporting channel neither disabled nor redirected. The ADR's own
"Weakest point" section (two sections later, in the same document)
correctly states the opposite — that this is unverified and could be a
"genuine gap in the confinement claim." Both cannot be true at once. A
reader who stops at "Decision 1 — answer" (a plausible stopping point, since
it is titled as the answer) comes away believing something the ADR's own
later section retracts.

**Coupling to the "untidy, not an escape" argument (Measurement 2).** The
crash-survival reasoning depends on the same premise: "nothing about a crash
moves those bytes anywhere else" is true only if everything Chrome writes
during the session lands inside `.live-view/session-<uuid>/`. If a crash
report is written to a fixed per-account location outside that directory
(the same gap Measurement 1 identifies), that specific artifact is not
"untidy" — it is outside the residency entirely, which is what the ADR's own
vocabulary calls an escape. This is not a second, independent finding; it is
the same unresolved gap surfacing in a second place the ADR treats as
settled.

**Answer to Measurement 1:** undetermined by reading, as instructed, with a
concrete asymmetry: the crash-reporting half of the gap is confirmed
unaddressed by any flag (source fact), while the GPU-shader-cache half is
partially, unquantifiably mitigated by `--disable-gpu` (a fact the ADR does
not mention at all). What would settle it is the widened-inventory crash
probe described above, run against the actual resolved Chrome binary.

**Does this invalidate the ADR's central claim, or narrow it?** **It
narrows, and does not invalidate.** The confinement mechanism itself —
checked-before-write, symlink-safe, independent of Chrome's cooperation — is
real and correctly built for the paths it manages; that is not in question.
What is wrong is the strength of two specific sentences: "already total" in
Decision 1's answer, and the unconditional form of "untidy, not an escape."
Both should read as conditional on the crash-reporting/GPU-cache question
being resolved, exactly as the "Weakest point" section already (correctly)
treats it — the repair is to make the rest of the ADR's language consistent
with that section, not to reopen Decision 1 or Decision 2 wholesale. I
recommend this gap be promoted from "weakest point" musing to an explicit
named condition on the "yes," parallel to how the spellcheck condition is
already handled (Decision 1's answer already conditions the "yes" on
spellcheck being closed; it should condition it on this too, or explicitly
scope "already total" to "total over the destinations this vehicle directs
Chrome to use").

## Measurement 2 — is "untidy, not an escape" right?

The reasoning that confinement is established at destination-computation
time, independent of `close()` running, is correct and verified in source:
`_confined_destinations()` and `_make_destinations()` run and check before
any browser process starts; `close()`/`_remove_session()` are teardown-only
and not load-bearing for confinement itself. Given that, a profile that
survives a crash is, for everything actually written to the four named
destinations, still inside the residency — the ADR's reasoning holds for
that subset. The reasoning does **not** cover the crash-reporting/GPU-cache
gap named above (see coupling note in Measurement 1); to that extent
"untidy, not an escape" is asserted more broadly than the source supports.

On discoverability/lifetime: I checked whether ADR-0048 connects the
"orphan sweep is undecided" point to ADR-0047's classification of backup
inclusion and content indexing as silently fatal preconditions, as the
charter directs. **It does not — `docs/adr/0048-entry-boundary.md` contains
no mention of backup or indexing at all** (confirmed by direct grep: zero
hits). This is a real gap, not a stylistic one: an orphaned session
directory is content ADR-0047's own preflight has no reason to know about,
because the preflight's backup/indexing check runs at the *next* session's
start, not continuously, and a crash-orphaned directory can sit in the
residency for an arbitrary time between the crash and the next session (if
one ever runs). If the residency's backup exclusion lapses in that window —
for a reason unrelated to viewing or entry entirely — the orphaned profile,
which may hold form-history or session-restore content this ADR itself
flags as possible, gets backed up along with everything else. That is a
materially different situation from ADR-0047's general "the whole residency
was backed up" framing, because this content exists in the residency
*only* because of a crashed entry session, and only the orphan-sweep
decision (currently left undecided) determines how long it persists there.
The ADR should either address this connection or explicitly note it as an
open interaction, the same way it already names the spellcheck and
crash-reporting gaps; right now it is silent rather than deferred.

## Measurement 3 — is the spellcheck condition real or decorative?

Verified against source. The launch arguments do not include any flag
disabling spellcheck or its enhanced/network mode; `--disable-background-networking`,
`--disable-sync`, and `--disable-translate` are the only network-adjacent
flags present, and none of them touches the spellcheck feature specifically.
The ADR's characterization — that these are cooperative, same-UID reductions
in accidental traffic, not a boundary — is correctly drawn by analogy to
ADR-0047's Class C, which states exactly that about the same three flags in
the viewing-session vehicle. The ADR states the requirement as binding
("Decision: an entry surface must launch with spellcheck's network path
affirmatively closed, not merely observed to be off") and is honest that
this is not yet done ("a vehicle change... not a decision this ADR can make
binding by itself"). This is real, stated as a condition rather than a
completed fact, and is not quietly assumed away. **Measurement 3 passes.**

## Measurement 4 — is question 2 as settled as the ADR says?

Checked against ADR-0002 and ADR-0032 directly, not against the ADR's
summary of them.

- ADR-0002: the sole authoritative store is an append-only `acts.jsonl`; all
  other state is a derived, discardable, rebuildable projection. This
  supports the ADR's claim that a direct fact/finding mutation is not a
  parallel option quietly declined but structurally unavailable — there is
  no mutable record to write into.
- ADR-0032 Decision 1 (contribution is a first-class event distinct from a
  run), Decision 2 (retained `evidence_ids` channel, admission-time
  consistency check), Decision 4 ("a contribution is initiated by the user
  with any batch"; `act-contribution.v1` "carrying a manually-entered
  batch"), Decision 5 (correction is supersession, never edit — "no edit, no
  manual withdrawal, no third mechanism") all read exactly as ADR-0048
  represents them. The claim that a direct-write path would also break
  Decision 2's admission check and Decision 5's supersession-only rule is
  correct: a fact written without an evidence-linked, admitted contribution
  event has no `evidence_id` to check and no supersession record to route
  through. **This is verified, not overclaimed.**

On the actor/origin question: ADR-0032 Decision 4's "initiated by the user"
language is real and supports "a contribution is already inherently
human-initiated." ADR-0048 asserts "there is no second actor a 'who typed
this' field would ever need to distinguish from," which is true of the
project's *current* state (one owner, one Owner Authorization domain per
ADR-0044), but the ADR does not name what would reopen this reasoning if a
second person or a machine-assisted entry path were ever introduced — it
states the current fact without naming its own reopening condition. The
charter specifically asked whether the ADR "should say what would reopen
it"; it does not. This is a minor completeness gap, not a wrong conclusion:
the "no field needed" answer is correct for the system as it exists today,
but a reader a year from now has no signal in the ADR itself for when to
revisit it.

## Measurement 5 — Track 1b

- `git diff ca8d023^..513ff93 -- packages/derivation/live_viewing.py tools/presentation_harness/lib/chrome.mjs tools/presentation_harness/lib/server.mjs` is empty, and I independently re-ran the wider check across the whole Track 1+1b range (`main..513ff93` and `7442bbb^..513ff93`) — also empty. All three files are unmodified, verified against base rather than accepted on the claim.
- `tools/entry_probe/headed_launch.py` imports `live_viewing.py`/`live_workspace.py` unmodified and touches only the public `websocket_url` field, consistent with its own stated design.
- The grep positive control was genuinely re-run for the headed vehicle: the findings note reports the specific binary re-confirmed (`/usr/bin/grep`, BSD grep, not the interactive shell's `ugrep` alias) and shows the exact exit-code contrast (`-rlaI` exit 1, `-rla` exit 0) against a freshly planted token — this is a concrete, reproducible claim, not narrative-only.
- Headless results were preserved rather than overwritten: the amended findings note reports both vehicles side by side per channel, and explicitly separates "byte-writing fired" from "behavioral restore-prompt untested" for channel 2 in both vehicles.
- Confirmed synthetic-only: `headed_launch.py`'s own docstring and the findings note both state a bare temp directory stands in for a workspace; grep for a real-path/residency-locator pattern across `git show 513ff93` finds no hit beyond the expected prose mention of "never a real... residency locator."
- Confirmed not wired into CI: no hit for `entry_probe` in `.github/`, `tools/verify*`, or any workflow file.
- The "no channel differed" conclusion is drawn narrowly and correctly: the note states the headed profile's entries are a strict subset of the headless one, explains the difference is unexplained rather than hand-waved, and never converts "no difference in this run" into "confinement is now proven general." This matches the caution the Track 1 review demanded.

**Measurement 5 passes.**

## Measurement 6 — scope

The ADR decides two things (browser-form acceptability; contribution vs.
direct write) and is explicit that it decides neither packaging,
correction mechanism, nor UI design, and that "no maturity cell moves." It
explicitly declines to extend ADR-0047's preflight/attestation/Class
framing to an entry session, naming that as the next milestone's business.
I found no place where a packaging, correction, or UI-design choice is made
by implication. **Measurement 6 passes.**

## Measurement 7 — is it legible on its own?

Reading `docs/adr/0048-entry-boundary.md` alone (as a reader a year from now
would): the two questions, the two decisions, and the conditions on the
"yes" are stated clearly, and the "Left undecided" and "Weakest point"
sections are unusually candid compared to most ADRs of this shape. The one
real legibility failure is the one already named in Measurement 1: "Decision
1 — answer" asserts confinement is "already total," and a reader who takes
that section as the ADR's bottom line (a reasonable reading — it is
literally titled "answer") will not learn that the ADR's own later section
disagrees with that word, or that the "untidy, not an escape" claim is
coupled to the same open question. This is exactly the class of failure
this phase exists to catch: not a missing fact, but an internal
inconsistency between a document's headline claim and its own hedged
appendix, discoverable only by reading the whole thing rather than the
section a skimming reader would stop at. I also confirm the actor/origin
question (Measurement 4) is legible as a present-tense fact but not as a
standing decision with a named trigger for revisiting it.

## Measurement 8 — are the four undecided items honestly held?

- **Orphan sweep** — named as undecided, but see Measurement 2: it is not
  connected to ADR-0047's backup/indexing framing, which the ADR should at
  minimum flag as an open interaction rather than leave silent.
- **Spellcheck mechanism** — genuinely deferred; Decision 1's "yes" is
  explicitly conditioned on it, not quietly load-bearing. Passes.
- **The Chrome-writes-elsewhere question** — this review's central finding.
  Named in "Weakest point" and "Left undecided," but the ADR's own "Decision
  1 — answer" and "untidy, not an escape" paragraphs do not carry that same
  hedge, so a reader can be misled about which parts of the decision depend
  on it. Not honestly held *throughout the document*, though it is honestly
  named in the two sections that discuss it directly.
- **Entry session's preflight/attestation shape** — explicitly and clearly
  deferred to the packaging milestone; no load-bearing use of it here.
  Passes.

## Verdict

**NOT READY**, on Measurement 1 as answered above (undetermined by reading,
with a concrete gap identified) coupled with the Measurement 7 legibility
failure it produces: the "already total" and "untidy, not an escape"
sentences in Decision 1 overstate what the ADR's own later sections concede,
and Measurement 2's backup/indexing interaction (charter-directed) is not
addressed at all.

**This narrows the ADR's central argument; it does not invalidate it.** The
confinement mechanism is real, source-verified, and correctly implemented
for the four destinations the vehicle manages, and the contribution-boundary
decision (Decision 2) is independently sound and untouched by this finding.
The repair is wording and scope discipline, not a re-decision:

1. Soften "already total" in Decision 1's answer to state what is actually
   established — total over the destinations this vehicle directs Chrome to
   use — and make that section's certainty consistent with "Weakest point."
2. Either condition the "yes" on the crash-reporting/GPU-cache question the
   same way it is already conditioned on spellcheck, or state plainly that
   this condition is not yet closed and say what would close it (the
   widened-inventory crash probe described in Measurement 1).
3. Note, even briefly, how an orphaned session directory interacts with
   ADR-0047's backup/indexing silently-fatal framing, or state explicitly
   that this interaction is left to whoever resolves the orphan-sweep
   question.
4. Optionally, name the condition under which the "no actor/origin field
   needed" reasoning would need revisiting (a second person, a
   machine-assisted entry path).

None of these require new engineering or a new probe run to *state*; only
item 2's full closure requires new evidence. Track 1b's own work
(Measurement 5) and the rest of the ADR's structure and reasoning
(Measurements 3, 4, 6) are sound as committed.
