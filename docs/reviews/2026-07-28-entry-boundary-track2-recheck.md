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

---

# Confirmation round — the Disposal scoping fix (`95bd997`)

- Scope: **Measurement 2 only.** Measurements 1, 3, 4, and 5 are not
  re-derived; they passed at `0df113e` and the fix's diff does not reach them.
- Fix applied by the foreman directly (`95bd997`), not by a builder.
- Boundaries spot-checked anyway, because they are cheap and the fix touched
  the ADR: `git diff main..95bd997 -- packages/derivation/ tools/presentation_harness/`
  is still **empty** (0 lines), and the ADR status line still reads
  **proposed**. Nothing about the fix changed either.

## Does the fix close what I said would close it?

**Yes.** I said the Disposal paragraph needed the same scoping the
Confinement paragraph immediately above it already had, and that one sentence
would do it. The fix does more than that and does it better.

The offending sentence is now bounded in place — "**Within that directory** it
is a single mechanism covering every channel at once" — so the paragraph no
longer overstates on its own terms. The new paragraph that follows does the
part I would not have thought to ask for and which is worth more than the
scoping itself:

> Do not read the paragraph above as a claim about unenumerated channels in
> general — it holds for unenumerated channels *inside the profile directory*,
> which is a narrower and weaker statement than it first appears.

That last clause is the useful one. The original defect was not that the
sentence was technically false; it was that it *read* stronger than it was,
and a reader had no signal to slow down. Telling the reader explicitly that
the preceding claim is weaker than it sounds is a stronger repair than
silently narrowing it would have been, because the narrowed version would
still have read as impressive to someone skimming. It also names the
counterexample in place ("the single-instance lock directory is created
outside the session tree, is never passed to `_remove_session()`, and
survives both a clean close and a crash"), so the reader does not have to
reach the Weakest-point section to learn that one exists.

"Its reach is the same as confinement's, and no wider" is also the right
framing to have chosen: it makes the two load-bearing properties symmetric,
which is exactly what was missing when Confinement was scoped and Disposal
was not.

## Has the defect relocated a third time?

I checked the whole document rather than only the edited region, since the
pattern has now moved once. Method: grep for absolute-strength constructions
(`every channel`, `all channels`, `everything Chrome`, `any channel`,
`every path`, `covers every`, `nothing is`, `at once`) and read each hit in
context against what Part 1 established.

**In the fix's own region and in every section the earlier repair touched:
no.** Every remaining absolute is either scoped in the same sentence
("across every channel this milestone exercised," "in any channel this
milestone tested," "for those destinations at once on a normal session"), or
is quoting the retracted claim in order to retract it ("never of
'everything Chrome writes,' which this ADR no longer asserts").

**One pre-existing sentence is now stale, and I want it on the record.** It
is not in the fixed region and was not introduced by this fix — it is
original Context text, in "Why this ADR does not rest on the probe's negative
results":

> The probe's positive findings — files *are* written by session-restore and
> the browser's own background stores, in both vehicles, and none of them
> left the confined directory tree — are used only as confirmation of those
> two properties [...]

"None of them left the confined directory tree" is the same *class* of
statement Part 1 disproved, and it was never a claim Track 1/1b was in a
position to make: those runs searched only inside the confined tree, so they
had no visibility into whether anything left it. Part 1 then showed something
does.

**I am not calling this blocking, and I want to be explicit about why, since
I blocked on the last one.** Three things distinguish it:

1. **It is not load-bearing.** The Disposal instance sat inside one of
   Decision 1's two named architectural properties — the thing the "yes"
   rests on. This sits in a framing paragraph whose entire purpose is to
   tell the reader *not* to rely on the probe's results ("This ADR does not
   use the probe's per-channel 'not fired' results as evidence for question
   1"). A section that discounts its own evidence in the next clause is a
   much weaker place for an overclaim to do damage.
2. **The document now contradicts it loudly and in four places** — the
   scoped Confinement paragraph, the new Disposal paragraph, the "What Part
   1's widened search settles" section, and the answer section's explicit
   "what this ADR's first draft got wrong." A reader is not going to leave
   this document believing nothing escapes.
3. **Proportionality.** Blocking a third time on a progressively smaller
   instance would be the reviewer failure mode, not diligence. I named the
   Disposal instance as blocking because it was the identical defect in the
   other pillar; this one is a stale summary clause in a discounting
   paragraph.

**The foreman's call, stated as a choice rather than a demand:** deleting the
clause "and none of them left the confined directory tree" — or replacing it
with "and none of them left the confined directory tree *in the region those
runs searched*" — is a one-clause edit before the closing PR. If it does not
happen, this is what ships, and I would rather it be a named residual in this
record than an unremarked one.

## Are the two new "Left undecided" entries genuinely held open?

**Yes, both.** Neither reads as scheduled work, and neither was investigated,
which they correctly say.

**The locator entry** is the more careful of the two and closes with exactly
the right sentence: "This is a gap in what has been checked, not a finding
that anything leaks." That distinction is the whole point — I raised it as an
unasked question, not as a suspicion, and the entry preserves that
distinction rather than upgrading it into an implied problem. Naming the
single-instance-lock directory as "a named place to start" is a pointer, not
an assignment: there is no milestone named, no "must," and no mechanism
proposed.

**The orphan-surface entry** is phrased as a recorded fact rather than an
open question, which is slightly odd placement under a heading called "Left
undecided" — the observation is settled (Part 1 saw it); what is undecided is
what to do about it. But it does not imply scheduled work: it states what was
observed, states that nothing sweeps it, and says why it is recorded here
("Part 1 observed it in the findings note and the reasoning above does not
otherwise reach it"). It proposes no sweep and names no owner. The
distinction it draws — that the existing orphan question concerns directories
that "at least survive *inside* the boundary" while "this one does not" — is
the substantive part and is correct.

Checked separately: the **Consequences** section was not touched by this fix,
so neither new entry leaked into the list of obligations the next milestone
"inherits." They are held in "Left undecided," which is where an
uninvestigated question belongs.

## The coverage limit in Evidence limits

Reads accurately and says the thing I was worried a later reader would miss:
"'the widened scan found no token' must not be read as covering these two
artifacts, because it did not examine them." It also correctly separates the
two supports — the hand-read symlink target and the structural fact that a
socket has no persisted bytes — and labels the second as "a structural
property, not an observation," which is the distinction that makes the claim
hold beyond the four instances actually inspected.

## Verdict

**READY.**

Measurement 2 passes. The Disposal claim is now bounded, its reach is stated
as equal to confinement's and no wider, the counterexample is named in place,
and the reader is told explicitly not to read the preceding paragraph as
general. The two carry-forwards are held open honestly without being dressed
as plans. Measurements 1, 3, 4, and 5 passed at `0df113e` and are unaffected.

ADR-0048 is `proposed`, not ratified; ratification remains the owner's.

## Residuals I would carry into a later milestone

The five from the previous round stand unchanged (crash-reporter/Crashpad
still open and untestable by `SIGKILL`; the locator question; the singleton
orphan surface; regular-files-only scan coverage; `--disable-gpu` as an
unquantified partial mitigant). Items 2, 3, and 4 are now recorded in the ADR
itself rather than only in this review record, which is where they belong.

One added:

6. **The stale Context clause** described above ("none of them left the
   confined directory tree"), if it is not edited before the closing PR.

And one observation about this milestone rather than the artifact, offered
for the retrospective and not as a finding: the same defect — a headline
claim stronger than the document's own later sections support — appeared
three times in one ADR, in three different sections, and each instance was
caught only by reading the whole document against itself rather than by
reading any section on its own. That is worth knowing for a phase whose
stated purpose is documents that are honest to a reader arriving without
context, because it suggests the failure is structural to how a long ADR gets
revised, not a lapse by any one author.
