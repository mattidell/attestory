# Recheck — Entry Boundary, Track 2: the repair to ADR-0048

- Role: **Reviewer** (`docs/roles/reviewer.md`) — same Reviewer who issued
  `docs/reviews/2026-07-28-entry-boundary-track2-review.md` (`17aea58`)
- Charter: `docs/reviews/charter-2026-07-28-entry-boundary-track2-recheck.md`
- Branch: `milestone/entry-boundary`, at `8758a21`; repair commit `0df113e`
- Scope: focused. Measurements 4, 5, and 6 of the original review are not
  re-derived except where `0df113e`'s diff reaches them.
- Envelope scan: `python3 tools/envelope_scan.py --range main..8758a21` —
  clean, exit 0.

## Measurement 1 — Finding 1 closed?

**Pass.** The contradiction is gone, and gone the right way — by making the
answer carry its own limits, not by hedging the document into mush.

Read as a reader who stops at "Decision 1 — answer": that section now states
the "yes" is scoped to "the four destinations `_confined_destinations()`
computes — profile, cache, downloads, print target," and then, in the same
section rather than in an appendix the reader may not reach, states plainly
what the first draft got wrong and why. The sentence I flagged — "which is
already total" — is gone from the answer, and every remaining occurrence of
"total" in the document (lines 208, 227, 290, 459, 537, checked by grep) is
either quoting the retracted claim in order to retract it, or is explicitly
scoped ("Confinement is total over the paths this vehicle *directs* Chrome
to use; it is not established, and is now known not to be true, that those
paths are the only ones Chrome uses"). A reader stopping at the answer now
comes away with a claim the ADR can support. The `INDEX.md` row carries the
same scoping ("not a claim that these are the only destinations Chrome
uses") rather than being left behind at the old strength.

## Measurement 2 — is the new claim exactly as strong as the evidence?

**Fail, on one paragraph.** Everywhere the repair touched, the answer is
yes. One place it did not touch still carries the disproven claim, and it is
not a peripheral one.

The **Disposal** subsection (`docs/adr/0048-entry-boundary.md`, the paragraph
beginning "**This is real, and it is the better foundation...**") is
unchanged by the repair — confirmed by diff, not by reading impression:
`git diff 3e9e6c3..0df113e -- docs/adr/0048-entry-boundary.md` shows no
change to it. It still reads:

> It is a single mechanism covering every channel at once, including
> channels this project has never enumerated and Chrome might add tomorrow.

That is precisely the claim Part 1 disproved. The single-instance-lock
mechanism *is* "a channel this project has never enumerated," and disposal
does **not** cover it — the ADR's own "Weakest point" section says so
directly, three sections later: "disposal does not touch that artifact (it
is never inside the session root `close()` deletes)." The findings note says
the same thing independently: "nothing in `live_viewing.py`'s
`close()`/`_remove_session()` path touches this location even on a clean
exit."

This is the *same* defect as my original Finding 1 — a headline section
asserting a strength the document's own later section retracts — relocated
from Confinement to Disposal. The asymmetry is what makes it a finding
rather than a quibble: the Confinement subsection immediately above it
received exactly the treatment this one needed ("**This holds, for exactly
the destinations it names.**"), so the document demonstrably knows the move;
Disposal simply did not get it. A reader working through Decision 1's two
named load-bearing properties in order reads a correctly scoped confinement
claim followed immediately by an unscoped disposal claim, and has no signal
that the second is weaker than it sounds until the "Weakest point" section
much later.

On the parts the repair *did* address, the strength calibration is good and
I could not find a slide-back: "no typed content was found outside
confinement" is stated as the resting claim in the answer section, the
evidence-limits section names it as "one observation, on one machine, on one
resolved Chrome build," the Weakest-point section distinguishes "evidence of
an absence on this machine, in these runs" from "a mechanism," and the
Crashpad absence is explicitly described as narrowing rather than closing.
The ADR also correctly declines to make the claim true by construction (the
rejected `--disable-breakpad` alternative) and says why. That is honest work.

**What would close this:** scope the Disposal paragraph the same way the
Confinement paragraph was scoped — one sentence. Nothing else in the
document needs to move.

## Measurement 3 — is the singleton finding characterized honestly?

**Pass, with one thing named that the charter did not ask about.**

The reasoning that neither artifact carries typed content is a real
conclusion drawn from direct inspection, not an assumption from file names:

- `SingletonSocket` is a Unix domain socket (`srwx------`, 0 bytes). A socket
  inode carries no persisted bytes at all — data traverses kernel buffers and
  is never written to the filesystem. This is structural, not observational,
  and it is the correct reason. It holds independent of what was typed.
- `SingletonCookie` is a symlink whose **target string** is the payload, and
  the builder read that target directly rather than reasoning from the name
  — a random 15–19 digit IPC authentication number, checked across four
  separate instances. `file` reporting it as a broken symlink to that number
  is the right check for this shape of artifact.

Attribution is the strongest part: `lsof` against the exact pid the vehicle
launched, tying the open descriptor at
`$TMPDIR/com.google.Chrome.<random>/SingletonSocket` to this vehicle's own
process rather than to the machine's unrelated running Chrome. That is
process-level evidence, not timestamp correlation, and the findings note is
explicit that this is why it was done that way.

**One limitation worth stating plainly, which the ADR and note carry
implicitly but not in these words:** the automated `wideFilesystemScan()` in
`tools/entry_probe/probe.mjs` greps only entries for which
`statSync(p).isFile()` is true. Neither of these two artifacts is a regular
file, so `tokenHit` is `null` for both — the automated grep did not cover
them. The "no typed content" claim for the singleton pair rests entirely on
the hand-verification and the structural socket argument above, not on the
probe's own token scan. That is adequate evidence and the note does describe
the hand-verification, but the distinction matters for anyone later reading
"the widened scan found no token" as if it had scanned these two files.

**Does existence outside confinement matter for reasons other than content?
Yes, in two ways, and I would carry both forward:**

1. **A locator question the search did not ask.** Everything outside
   confinement was checked for *typed tokens*. Nothing checked whether
   anything outside confinement encodes the residency path itself. Chrome
   derives this temp directory's name randomly, so on the structure of the
   mechanism this is unlikely — but it is unverified, and it is a different
   question from the one asked. The residency locator is protected in its own
   right (ADR-0031 D4/D5), so "holds no typed content" does not by itself
   settle "reveals nothing about the residency."
2. **Accumulation.** The findings note reports more than a dozen
   `com.google.Chrome.<random>` directories already present under the temp
   directory, dated across prior days, with nothing on the machine sweeping
   them. The ADR routes the *redirect-or-account-for* question to the next
   milestone, which is right, but it does not carry the accumulation
   observation itself — that this is a second orphan-accumulation surface,
   outside the residency, in addition to the one inside it that the
   orphan-sweep question covers. Not a defect in the decision; a fact worth
   surviving into whichever milestone picks the artifact up.

## Measurement 4 — Finding 2 closed without overcorrection?

**Pass.** The new subsection ("The orphan-sweep question is not independent
of ADR-0047's backup/indexing framing") engages the preconditions
substantively rather than gesturing at them: it identifies the specific
dimension on which an orphaned directory differs from a normal session's
(unbounded lifetime versus one session's length, measured against backup and
indexing cycle intervals), which is the actual mechanism of the exposure and
matches the reasoning I raised.

It reaches a position and states it as one: "this changes 'untidy, not an
escape' from an unconditional answer to one that depends on the same
silently-fatal preconditions ADR-0047 already names." It names what is owed
("must treat a crash-orphaned session directory as subject to ADR-0047's
backup/indexing preconditions for the entire time it survives"). And it
explicitly refuses to overcorrect: "that milestone should decide the
mechanism (sweep, preflight, attestation) rather than this ADR designing it
in advance." No sweep is designed, no preflight condition is added, and
nothing is implied to be scheduled — the "Left undecided" and "Consequences"
entries both keep it as an inherited obligation, not a plan.

## Measurement 5 — boundaries held?

**Pass**, verified rather than accepted:

- `git diff main..8758a21 -- packages/derivation/ tools/presentation_harness/`
  is **empty** (0 lines). `live_viewing.py`, `chrome.mjs`, and `server.mjs`
  are unmodified against base. No product code changed anywhere in the range.
- `git diff 3e9e6c3..8758a21 --name-only` touches only `docs/` and
  `tools/entry_probe/` — the throwaway probe, which is not product code and
  is not wired into CI.
- The ADR status line still reads **proposed** (not ratified).
- No residency locator. `git show 0df113e | grep -E "^\+.*(/Users/[a-z]|/home/[a-z])"`
  returns nothing. This mattered more than usual here, since the new findings
  section reports on real per-user directories for the first time in this
  milestone: it names them by category (`~/Library/Logs/DiagnosticReports`,
  `~/Library/Caches`, `$TMPDIR`) in tilde-relative, non-identifying form, and
  the probe code is deliberately built to preserve that — `wideFilesystemScan()`
  records `relativeToRoot` with an explicit comment that it is "never the real
  absolute path under the user's home directory." That is the right design,
  not an accident of what happened to get pasted in.
- Existing findings preserved, not rewritten: the findings note's diff is
  `179 insertions, 0 deletions` — purely additive, with the new material in
  its own "Track 2 repair, Part 1" section.
- `INDEX.md` row is consistent with the repaired ADR, including the
  scoped-confinement wording and the singleton finding.

## Method notes on Part 1 that I checked and accept

Two design choices in the widened search are load-bearing and correct:
birthtime (`stat -f %B`) rather than mtime as the operative filter, which is
what makes the result survive an unrelated real Chrome running throughout
(that browser modifies pre-existing files without creating new ones), and the
`find -newer` prefilter being mtime-based is safe because any file created
after the marker necessarily has mtime at or after it, so nothing new is
missed by the prefilter. The `-maxdepth 5` bound is a real limitation and the
note discloses it rather than omitting it.

## Pointer state (reported, not fixed)

`docs/phase-state.md` `current_role` and `current_prompt` still name the
**repair** charter (`charter-2026-07-28-entry-boundary-track2-repair.md`),
which the repair commit discharged, rather than this recheck's charter. Per
`docs/roles/reviewer.md` I do not own that pointer and have not touched it.
Reporting rather than silently ignoring it: this is the same drift pattern
that has recurred on this milestone.

## Verdict

**NOT READY**, on Measurement 2 only, and narrowly.

Measurements 1, 3, 4, and 5 pass. The repair does the substantive work well:
it went and looked, found a real counterexample to its own strongest claim,
reported it plainly as a fact rather than softening it, verified attribution
at the process level rather than by timing, rewrote the answer section to
carry its own limits, connected the orphan question to ADR-0047 substantively,
and added the reopening trigger. The evidence-strength calibration in every
section the repair touched is honest.

**What fails, and what closes it:** the Disposal subsection's claim that
disposal is "a single mechanism covering every channel at once, including
channels this project has never enumerated" is now known to be false, by this
ADR's own Part 1 evidence, and the ADR says so elsewhere. Scope that
paragraph the way the Confinement paragraph immediately above it was already
scoped — disposal covers every channel that writes *into the four confined
destinations*, which is still the strong and useful property, and it is not a
claim about channels that write elsewhere. That is one sentence in one
paragraph, in the file already under repair, with no new evidence required.

I recognize the milestone closes on this recheck and that this is a small
edit. I am calling it blocking rather than a residual for one reason: it is
the *identical* defect the original NOT READY was issued for, in the
document's other load-bearing property section, and letting it through would
mean the ADR ships with the same internal contradiction it was just repaired
to remove — in a phase whose entire purpose is documents that are honest to a
reader who arrives without context.

## Residuals to carry, if the foreman closes after that edit

These are not blocking and I do not want them repaired now — they belong to
whichever milestone next touches `live_viewing.py` or packages an entry
surface:

1. **The crash-reporter/Crashpad-database question remains open.** Part 1
   narrowed it (no Crashpad-named artifact appeared outside confinement) but
   the note is correct that `SIGKILL` gives the OS no crash to report, so this
   run's proxy for "the controlling process dies without warning" cannot speak
   to the OS-level crash-report channel at all. A `SIGSEGV`/`SIGABRT` variant
   would.
2. **Whether anything outside confinement encodes the residency locator** —
   asked of typed content only, never of the locator itself (Measurement 3).
3. **The singleton directory is a second orphan-accumulation surface**,
   outside the residency, that nothing sweeps — observed in the findings note,
   not carried into the ADR.
4. **The automated wide scan covers regular files only**; non-regular
   artifacts (sockets, symlinks) need hand inspection, as they got here. Any
   future widened search should say so up front rather than rediscovering it.
5. **`--disable-gpu` as a partial, unquantified mitigant** for the
   shader-cache half — correctly named in the ADR now, still untested.
