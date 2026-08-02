# ADR 0048 — The Entry Boundary

- Status: **accepted 2026-07-28**, ratified by the owner merging PR #102
  (`c451a40`). Builder
  draft, Entry Boundary milestone Track 2
  (`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-28-entry-boundary-track2.md`); repaired per
  the Track 2 review's NOT READY verdict
  (`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-28-entry-boundary-track2-review.md`) under
  `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-28-entry-boundary-track2-repair.md`. The
  repair added a widened, outside-confinement filesystem search (see "What
  Part 1's widened search settles, and does not") and narrowed this ADR's
  own wording to match what that search and the rest of this document's
  reasoning actually establish.
- Tier: 3
- Date: 2026-07-28

## Context — entry turns a read into a write

Today the owner gets tax facts into the product by hand-editing JSON. Every
other thing the product does with real data is a **read**: a live viewing
session (ADR-0047) opens a browser, shows something already in the residency,
and leaves nothing behind. A browser form is different in kind, not degree —
the browser becomes the place real financial data **first appears**, and it
passes through a text input before anything else sees it.

Browsers are built to be helpful about typed text: autofill, session-restore
drafts, in-page undo, spellcheck (locally and, opt-in, to a remote service),
and more. Any of those could retain a Social Security number or a wage figure
somewhere the product never looks. Track 1 of this milestone built a
throwaway probe and ran it against both the synthetic evaluation harness
(`tools/presentation_harness/lib/chrome.mjs`, headless) and the real headed
vehicle a person would actually type into
(`packages/derivation/live_viewing.py`, ADR-0047), on a synthetic workspace.
Findings:
`docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-boundary-retention-findings.md`.

### Why this ADR does not rest on the probe's negative results

The probe observed, in both vehicles: no retained token in any on-disk store,
and zero non-loopback network requests. Read at face value, that looks like
"browsers don't retain typed text here." It is a weaker result than that,
for two specific reasons the Track 1 review
(`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-28-entry-boundary-track1-review.md`) and the probe's
own findings note name:

- Chrome only writes typed values into its persistent form-history store
  after a user accepts a "Save this info?" prompt. The probe never drove
  that prompt to a yes, in either vehicle. "Not fired" here means "the
  condition that makes it fire was not created," not "the condition was
  created and nothing happened."
- Enhanced ("send to Google") spellcheck is opt-in and was off in both
  vehicles. "Zero non-loopback requests" is a true statement about the
  *default* configuration, not a statement about what an enabled account
  would do.

An ADR that rested its permission on these two observations would be resting
on an untested precondition dressed as a tested one, and a false negative
here reads as a green light. This ADR does not use the probe's per-channel
"not fired" results as evidence for question 1. It rests the decision on two
architectural properties of the vehicle that do not depend on what a browser
chooses to do: **confinement** and **disposal**. The probe's positive
findings — files *are* written by session-restore and the browser's own
background stores, in both vehicles — are used only as confirmation of those
two properties, not as the basis for a claim about Chrome's retention
behavior in general. Those runs searched only inside the confined tree, so
they could not have established that nothing left it; the widened search that
addressed that question came later, and found that something does (see "What
Part 1's widened search settles, and does not").

## The two questions

**1. Is a browser form an acceptable place for a person to type real tax
facts?**

**2. Does an entry surface write facts directly, or emit contribution events
through the existing boundary (ADR-0032)?**

## Decision 1 — confinement and disposal, verified against the vehicle

`packages/derivation/live_viewing.py` is the accepted headed vehicle
(ADR-0047). Two properties of it, read from source rather than taken from
this milestone's charter, carry the argument:

### Confinement

`_confined_destinations()` computes every destination the browser is given —
profile, cache, downloads, print target — as a descendant of
`capability.location / ".live-view" / "session-<uuid>"`, where
`capability.location` **is** the residency ADR-0031 defines. Containment is
checked with `_within()` against the resolved residency root, twice
(immediately after computing the paths, and again after creating them, to
close a symlink/race window), and a symlinked destination is refused outright
at both checks. This is a load-bearing precondition of `launch()`: a failing
check raises `PATH_NOT_CONFINED` before a directory is created or a browser
process is started. Confinement is established at launch time, not at
teardown, and does not depend on the session closing cleanly.

**This holds, for exactly the destinations it names.** Every path
`_confined_destinations()` computes is inside the residency, checked before
use, independent of whatever Chrome itself chooses to write, retain, or
forget into *those* paths. It is not, on its own, a claim that these are the
only paths Chrome writes to for a given launch — see "What Part 1's widened
search settles, and does not," below, which found a concrete case where they
are not.

### Disposal

`LiveViewingSession.close()` calls `_stop_process()` then
`_remove_session()`, which `rmtree`s the session root. A failure in either
step raises `BROWSER_TEARDOWN_FAILED` rather than swallowing the error — a
loud failure, not a quiet one. Used as a context manager (`__enter__`/
`__exit__`), `close()` runs whenever Python's own exception handling gets a
chance to run, including most launch-time failure paths (`_abandon_launch()`
is called from every named exception branch of `launch()`, itself
best-effort and documented as such in the module's own comment).

**This is real, and it is a better foundation than the probe's per-channel
negatives.** Whatever a browser retains about typed text — proven or not,
tested or not — dies with the profile directory on a normal close, regardless
of which retention channel did the retaining. Within that directory it is a
single mechanism covering every channel at once, including channels this
project has never enumerated and Chrome might add tomorrow. That is a
materially stronger property than "we checked five channels and none fired."

**Its reach is the same as confinement's, and no wider.** Disposal removes the
confined session root. It does not touch anything the browser writes outside
that root, and Part 1 established that such a thing exists: the single-instance
lock directory is created outside the session tree, is never passed to
`_remove_session()`, and survives both a clean close and a crash. So disposal
is total over what it disposes of, not over everything Chrome writes. Do not
read the paragraph above as a claim about unenumerated channels in general — it
holds for unenumerated channels *inside the profile directory*, which is a
narrower and weaker statement than it first appears.

**Where it fails — verified, not asserted.** `close()` is Python code. A
`SIGKILL` to the controlling process, a segfault, or a power loss means no
Python code runs at all — no context-manager `__exit__`, no `finally`, no
`_remove_session()`. The session-root directory, with whatever the browser
had written into it up to that instant, survives on disk. The probe's own
crash test (`SIGKILL` to the *browser* process, not the controlling process)
independently confirms the shape of this gap in practice: after a simulated
crash, `Default/Sessions/` held a `Session_<id>` file in both vehicles that
was not present before the crash and was never written by anything but
Chrome's own crash-recovery code. Disposal, in other words, is conditional
on the close path executing, and the probe caught a real instance of it not
executing.

**Is a surviving profile an escape, or merely untidy? Reasoned through, not
asserted, and bounded by what "confinement" was just shown to cover:**
confinement is established once, at destination-computation time, before
anything is written — it does not depend on `close()` running at all. A
profile that survives a crash still sits under
`capability.location/.live-view/session-<uuid>/`, inside the residency
ADR-0031 already treats as the place real data lives, **for everything the
vehicle actually confines there.** Nothing about a crash moves those bytes
anywhere else. **For that content, this is untidy, not an escape.** This
claim is deliberately narrower than the unqualified form this section
previously stated: it is not a claim that a crash cannot leave anything
anywhere else, because Part 1's widened search (see below) found a case
where the vehicle itself writes something outside this tree during a normal
launch, unrelated to whether the session then crashes. That artifact holds
no typed content, so it does not change the answer to question 1 — but it
does mean "untidy, not an escape" is true of the four confined destinations,
not of everything a launch produces.

The practical consequence for the confined tree is an operational one, not a
boundary breach: orphaned session directories accumulate under `.live-view/`
with every crash this vehicle does not currently sweep up on a later launch,
and they hold whatever the browser wrote before the kill — potentially
including, per above, form-history writes accepted via a save prompt or
session-restore snapshots, if a future session ever drives those
interactions. This ADR leaves that sweep undecided; see "Left undecided"
below — and see the next subsection for why "undecided" is not the same as
"inconsequential."

### The orphan-sweep question is not independent of ADR-0047's backup/indexing framing

ADR-0047 classifies whether the residency's *backup inclusion* and *content
indexing* are excluded as **silently fatal preconditions** — not a boundary
the viewing vehicle enforces itself, but something that must be true of the
residency for that vehicle's guarantees to mean what they say. ADR-0048, as
first drafted, never mentioned this. That silence was a real gap, not a
stylistic one, worked through here rather than left open:

An orphaned `.live-view/session-<uuid>/` directory is different in kind from
a normal session's directory, on exactly the dimension ADR-0047's
precondition cares about: a normal session's directory exists for the length
of one viewing session and is gone before any backup or indexing cycle is
likely to run against it. A crash-orphaned directory has no such bound — it
sits inside the residency for however long elapses until a sweep (if one is
ever built) or a person notices, which could be longer than the gap between
two backup or indexing passes. If the residency's backup exclusion or
indexing exclusion lapses in that window, for a reason that has nothing to
do with viewing or entry at all, the orphaned profile — which may hold
form-history or session-restore content this ADR already flags as possible —
gets swept up along with everything else. That is a materially different
exposure than ADR-0047's general framing of "the whole residency was
backed up," because this specific content exists in the residency *only*
because of a crashed session, and its lifetime there is exactly the
orphan-sweep question this ADR otherwise treats as a purely operational,
low-stakes loose end.

**Position:** this changes "untidy, not an escape" from an unconditional
answer to one that depends on the same silently-fatal preconditions
ADR-0047 already names — a crash-orphaned profile is untidy-not-an-escape
only for as long as those preconditions continue to hold over an unbounded
window, not just the length of a session. This ADR does not resolve the
orphan-sweep question (see "Left undecided"), but it now names what a
resolution needs to account for: whichever milestone builds the sweep, a
preflight check, or an owner attestation for entry sessions must treat a
crash-orphaned session directory as subject to ADR-0047's backup/indexing
preconditions for the entire time it survives, not just for the length of a
normal session — and that milestone should decide the mechanism (sweep,
preflight, attestation) rather than this ADR designing it in advance.

### What Part 1's widened search settles, and does not

Every search above this point, in this ADR's own source reading and in
Track 1/1b's probe, looked only inside the four destinations
`_confined_destinations()` computes. The Track 2 review found that
insufficient to support "already total," and this ADR's own repair (Part 1,
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-28-entry-boundary-track2-repair.md`) went and
looked outside that tree, against the same unmodified vehicle, exercising
the same crash path. Full method and evidence:
`docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-boundary-retention-findings.md`,
"Track 2 repair, Part 1."

**What it found, plainly:** the resolved Chrome binary on the machine this
was run on creates a directory (`com.google.Chrome.<random>`, holding a
Unix-domain socket and a symlink-encoded authentication token — Chrome's own
single-instance-lock mechanism) directly under the OS temp directory, a
sibling of, not a descendant of, the confined session tree. This was
verified at the process level — `lsof` against the exact pid this vehicle
launched, not inferred from file timestamps — so it is tied to this
vehicle's own launch, not to anything else running on the machine. It
survives a `SIGKILL` to the browser process, the same way an orphaned
session directory does, and nothing in `close()`/`_remove_session()` touches
it, because it was never inside the tree that code manages.

**What it means for this ADR's claim:** "already total" was wrong, not
merely unverified — this is a real, verified exception, not a hypothetical
one. **What it does not mean:** the exception holds no typed content. A
random IPC authentication number and an unconnected socket are not a wage
figure or a Social Security number; nothing planted by this ADR's own probe
or by hand-verification appeared in either. The "yes" this ADR reaches does
not rest on "nothing is ever written outside confinement" — it now can't —
it rests on the narrower, now-tested claim that no *typed content* escaped,
across every channel this milestone exercised, including this one.

**What it does not settle:** this is one channel (the single-instance lock),
on one machine, on one resolved Chrome build. It does not test the
crash-reporter/Crashpad-database question the "Weakest point" section below
still names as open — no Crashpad-named artifact appeared outside
confinement in either run here, which narrows that question without closing
it. A different Chrome version, a different OS, or a differently configured
account could behave differently, for this channel or another one this
milestone has not looked for at all.

### Spellcheck does not inherit this argument

A disposable, confined profile stops nothing that already left the machine
over the network before disposal ran. Confinement and disposal are
filesystem properties; enhanced spellcheck is a network-egress property, and
the vehicle's cooperative network flags
(`--disable-background-networking`, `--disable-sync`, `--disable-translate`)
are, by ADR-0047's own Class C framing, not a boundary — they reduce
accidental traffic from a same-UID process, they do not prevent it. Neither
`--disable-background-networking` nor any flag `live_viewing.py` currently
passes disables spellcheck outright; the probe's "zero non-loopback
requests" result is the *default*-configuration observation, not a
guarantee that a differently-configured or future-Chrome default stays that
way.

**Decision: an entry surface must launch with spellcheck's network path
affirmatively closed, not merely observed to be off.** This is a vehicle
change (a launch flag or policy — e.g. disabling the spellcheck feature
outright, or forcing local-only dictionaries), not a decision this ADR can
make binding by itself; it is recorded here as the condition under which
Decision 1 below holds, and it belongs to whichever milestone next touches
`packages/derivation/live_viewing.py` or its successor entry vehicle.

## Decision 1 — answer

**A browser form is an acceptable place for a person to type real tax facts,
under the confined, disposing vehicle this project already has, provided the
spellcheck network path is affirmatively closed rather than left to
observed default behavior.**

This is a narrower "yes" than "browsers are safe," and narrower again than
this ADR's own first draft stated it. It is: *this vehicle's filesystem
confinement holds, regardless of clean or crashed exit, for the four
destinations `_confined_destinations()` computes — profile, cache,
downloads, print target — and its disposal-on-close eliminates the retention
question for those destinations at once on a normal session, with one
closeable gap named above (spellcheck) and one operational residual
(orphaned crash directories, now understood to interact with ADR-0047's
backup/indexing preconditions rather than being merely operational) left
undecided.*

**What this ADR's first draft got wrong, and the correction:** it stated
that confinement "does not depend on knowing which channel exists — it
depends only on where the browser is allowed to write, which is already
total." That is not correct, and Part 1 of this ADR's own repair (see
"What Part 1's widened search settles, and does not," below) found a
concrete counterexample: the vehicle's launch produces at least one
filesystem artifact — a single-instance-lock socket and an authentication
token, not typed content — outside every destination
`_confined_destinations()` names or `_within()` checks. Confinement is total
over the paths this vehicle *directs* Chrome to use; it is not established,
and is now known not to be true, that those paths are the only ones Chrome
uses. The "yes" answered here rests on a narrower, verified claim: **no
typed content was found outside confinement, in any channel this milestone
tested, including the one now-known filesystem escape** — not on the
stronger, unverified claim that no escape of any kind exists.

## Decision 2 — write path: contribution events, not direct facts

The product already has an append-only act log as its only store (ADR-0002)
and a contribution as a first-class, distinct product event, separate from a
run (ADR-0032 Decision 1). ADR-0032 Decision 4 already frames a contribution
as user-initiated ("a contribution is initiated by the user with any
batch"); `act-contribution.v1` is already modeled as carrying "a
manually-entered batch." A direct-write path — an entry surface mutating a
fact or finding record without going through a contribution — is not a
parallel option this ADR is choosing against; it is not available at all
under ADR-0002's append-only act-log model, and it would also break
ADR-0032 Decision 2's admission-time consistency check (a contribution's
`evidence_id` must be a member of the finding's `evidence_ids`) and Decision
5's supersession-only correction (no edit, no third mechanism). A form that
wrote a fact directly would have no evidence linkage and no supersession
path — it would not be a smaller version of the existing model, it would be
outside it.

**Decision: an entry surface, if built, must emit contribution events
(`act-contribution.v1`) through whatever admission path already assembles
them — the same path any other contribution takes. It has no write
authority beyond that.**

### What changes if a human becomes an origin of contributions — and what does not

The charter asks what the event must carry, what it may not, and whether a
later reviewer needs to be able to tell a human-originated contribution from
a machine-originated one.

**Nothing in the event's shape needs to change, and no distinction needs to
exist.** ADR-0032's ontology has exactly one machine-originated event kind —
a **run** — and a run does not produce contributions; it only consumes
findings. A **contribution**, in this ontology, is already definitionally a
human act (Decision 4's own word is "initiated by the user"). There is no
second, machine-originated kind of contribution for a browser-originated one
to be confused with. Today the owner produces a contribution by hand-editing
JSON; a future browser form would produce the same kind of event through a
different transport. The transport is not part of the event's identity, and
this project has exactly one owner and one Owner Authorization domain
(ADR-0044) — there is no second actor a "who typed this" field would ever
need to distinguish from. Adding an origin/channel marker to
`act-contribution.v1` would record a fact about entry mechanism that
changes nothing about provenance, evidence linkage, or supersession, and
this ADR does not propose one.

**What would reopen this:** the "no field needed" answer is correct for the
system as it exists today — one owner, one Owner Authorization domain. It is
not a standing property of the ontology; it is a fact about the current
single-actor system. If a second person, or a machine-assisted entry path
that originates (not merely consumes) a contribution, is ever introduced,
this reasoning no longer applies and the actor/origin question would need
to be reopened, not merely extended.

**What must not change:** the evidence-linkage requirement (ADR-0032
Decision 2) and the supersession-only correction rule (Decision 5) apply to
a browser-originated contribution exactly as they apply to any other one.
An entry surface gets no exemption and no shortcut through either.

**What is new, and is not resolved here:** a viewing session (ADR-0047)
consumes material already inside the residency and holds "no publication
credential or path" — it is explicitly not a crossing because nothing is
created. An entry session originates content. Reusing `live_viewing.py`'s
confinement and disposal machinery for entry is, on this ADR's reasoning,
sound for the filesystem question, but the *session type* — one that
creates a contribution rather than only rendering one — is not the session
type ADR-0047 evaluated, and this ADR does not extend ADR-0047's preflight,
attestation, or Class A–D framing to cover it. That extension, and how a
typed batch actually reaches the admission path (packaging), are explicitly
out of scope here per the charter and belong to the next milestone.

## Consequences

- A browser form is permitted as an entry surface, conditioned on: reusing
  (or equaling) `live_viewing.py`'s confinement and disposal properties, and
  closing the spellcheck network path affirmatively rather than by observed
  default.
- An entry surface's only write authority is emitting `act-contribution.v1`
  events through the existing admission path. It may never write a fact or
  finding directly.
- No new actor/origin field is added to the contribution schema. A
  browser-originated contribution is not distinguished from any other
  contribution.
- No maturity cell moves. This is a decision, not an implementation.
- The next milestone (packaging) inherits three open obligations this ADR
  names but does not discharge: an affirmative spellcheck-disabling flag; a
  decision about whether crash-orphaned session directories need a sweep,
  now understood to interact with ADR-0047's backup/indexing preconditions
  over an unbounded window rather than being purely operational; and
  investigating whether the vehicle can redirect (or must otherwise account
  for) the single-instance-lock artifact Part 1 of this ADR's repair found
  written outside every confined destination — see "What Part 1's widened
  search settles, and does not." Recorded here as owed investigation, not
  designed: a candidate is disabling or redirecting Chrome's crash-reporting
  subsystem outright (e.g. a `--disable-breakpad`-class flag) for the
  related, still-open crash-reporter-database question named in "Weakest
  point," but this ADR does not add any launch flag itself, and neither
  should the milestone that packages an entry surface without first
  confirming what such a flag would and would not cover.

## Left undecided

- **Whether stale `.live-view/session-<uuid>` directories from a crashed
  controlling process need to be swept on a later launch.** Untidy, not an
  escape, per the reasoning above — but only for as long as ADR-0047's
  backup/indexing preconditions hold over however long the orphan survives,
  which this ADR now names explicitly rather than treating as a purely
  operational loose end (see "The orphan-sweep question is not independent
  of ADR-0047's backup/indexing framing"). This ADR does not decide whether
  that untidiness is acceptable indefinitely or needs a cleanup mechanism.
- **The exact mechanism for closing the spellcheck network path** (a launch
  flag, a Chrome policy, or something else) — named as a requirement, not
  designed here.
- **Whether Chrome writes anything at all outside the paths
  `live_viewing.py` explicitly redirects.** This ADR's own repair (Part 1,
  see "What Part 1's widened search settles, and does not") answered part of
  this: yes, confirmed, for the single-instance-lock mechanism, which writes
  a socket and an authentication token outside the confined tree and holds
  no typed content. The crash-reporting-database and GPU-shader-cache
  candidates named by the original review remain untested — no
  Crashpad-named artifact appeared outside confinement in the runs
  performed, which narrows but does not close that question. See "Weakest
  point" below.
- **Whether the single-instance-lock artifact can be redirected or must
  instead be accounted for explicitly in the residency boundary.** Newly
  named by Part 1's finding; not investigated further here (out of scope
  per this repair's own charter — no vehicle change was made).
- **Whether anything written outside confinement encodes the residency
  locator.** Everything searched so far looked for *typed tokens*. The
  locator is protected in its own right, independently of any fact typed
  into a form, and no run has searched for it. The single-instance-lock
  directory is a named place to start, since it is created outside the
  session tree and its name is derived by the browser rather than by the
  vehicle. This is a gap in what has been checked, not a finding that
  anything leaks.
- **That the single-instance-lock directory is a second orphan surface, and
  it is outside the residency.** The orphan-sweep question above concerns
  `.live-view/session-<uuid>` directories, which at least survive *inside*
  the boundary. This one does not. Nothing sweeps it, and a repeated crash
  accumulates instances. Recorded here because Part 1 observed it in the
  findings note and the reasoning above does not otherwise reach it.
- **The entry session's own preflight/attestation shape**, if it differs
  from a viewing session's — explicitly left to the packaging milestone.

## Weakest point in this ADR's own reasoning

The confinement argument is strong only to the extent that
`--user-data-dir` and `--disk-cache-dir` actually capture *everything*
Chrome writes for a given profile. This ADR's source reading and the Track
1/1b probe operated entirely inside the paths those flags name (plus the
synthetic workspace root as a whole, for the probe); this ADR's own repair
(Part 1) then looked outside that tree and **found a real instance of this
gap**: the single-instance-lock socket and authentication token described
above, verified by `lsof` against the vehicle's own launched process, not
merely inferred. That confirms the shape of this weakness is real, not
hypothetical — disposal does not touch that artifact (it is never inside the
session root `close()` deletes) and confinement does not apply to it either
(it was never checked against the residency root, because nothing in
`_confined_destinations()` considers it) — exactly as this section
originally speculated, now with a named, verified example rather than a
guess.

**What remains open after Part 1:** the single-instance-lock channel is
closed as a question (found, characterized, holds no typed content); the
crash-reporting-database and GPU-shader-cache channels named by the Track 2
review are not. No Crashpad-named artifact appeared outside confinement in
either headed run performed for Part 1, which narrows this question — it is
evidence of an absence on this machine, in these runs, not a mechanism that
rules a fixed crash-reporter-database location out on a different Chrome
build, OS version, or account configuration. This ADR still cannot rule
that specific gap out from what has been read or observed, and the
"confinement is total because it's checked before any write" claim remains
true only of the four named destinations, never of "everything Chrome
writes," which this ADR no longer asserts.

For the GPU-shader-cache half of this question specifically: `launch()`
already passes `--disable-gpu`, which is directly relevant — a disabled GPU
process very plausibly writes little or nothing to a shader cache regardless
of where that cache would otherwise live. This is named here, not silently
assumed: it is a real, partial, but unquantified mitigant, not a closed
question — this ADR's own reading of the source cannot settle whether
`--disable-gpu` fully suppresses shader-cache writes on every Chrome build
(some builds still launch a software-fallback GPU process for compositing
or WebGL), and neither Part 1 nor any earlier probe run specifically tested
for a GPU shader cache outside the confined tree.

**Recorded as owed investigation, not designed here:** whichever milestone
next touches `packages/derivation/live_viewing.py` or its successor entry
vehicle should determine (a) whether Chrome's crash-reporting subsystem can
be disabled or redirected outright — a `--disable-breakpad`-class flag is
the obvious candidate, and doing so would make part of this ADR's "yes"
true by construction rather than by continued observation, which is exactly
why this repair's own charter kept it out of scope here — and (b) whether
the single-instance-lock location can be redirected or must instead be
named as a permanent, accounted-for exception to the residency boundary.

## Alternatives considered

- **Rest the decision on the probe's per-channel "not fired" results.**
  Rejected for the reason given in Context: two of five channels were never
  driven into the condition that would make them fire, so "not fired" would
  be reporting an untested precondition as a tested one.
- **Treat cooperative network flags as sufficient for spellcheck.** Rejected
  on the same grounds ADR-0047 Class C already establishes: a cooperative,
  same-UID flag is not a boundary, and "was off in this run" is not
  "cannot be turned on."
- **Add an actor/origin field to `act-contribution.v1` now, pre-emptively.**
  Rejected: nothing in the current single-owner ontology needs it, and
  ADR-0032's non-goals already scope schema changes out of this milestone.
- **Answer "no" to question 1 and stop.** Considered seriously, since "no"
  is a real answer this milestone's own framing invites. Rejected because
  the confinement and disposal properties, read from the actual vehicle,
  are strong enough to support a conditioned "yes" — the condition being the
  spellcheck flag this ADR names as owed, not built.
- **Disable Chrome's crash-reporting subsystem now (a `--disable-breakpad`-
  class flag), to make "no typed content escapes" true regardless of what
  Part 1's search did or did not find.** Rejected for this repair: it would
  be a change to `packages/derivation/live_viewing.py`, out of scope for an
  ADR repair per its own charter, and would make the claim true by
  construction rather than by continued observation — the same reasoning
  that already rejects resting this decision on the probe's untested
  preconditions in Context. Recorded instead as owed investigation in
  "Weakest point."

## Links

- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-boundary.md`
- Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-28-entry-boundary-track2.md`
- Repair charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-28-entry-boundary-track2-repair.md`
- Probe findings (both vehicles, plus Track 2 repair's widened,
  outside-confinement search):
  `docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-boundary-retention-findings.md`
- Track 1 review (headless-only scope, corrected by Track 1b):
  `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-28-entry-boundary-track1-review.md`
- Track 2 review (NOT READY, the review this repair addresses):
  `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-28-entry-boundary-track2-review.md`
- Vehicle: `packages/derivation/live_viewing.py`
- Residency: `docs/adr/0031-real-data-residency-boundary.md`
- Contribution: `docs/adr/0032-contribution-boundary.md`
- Viewing session: `docs/adr/0047-live-viewing-environment.md`
- Trust domains: `docs/adr/0044-live-run-system-boundary-and-trust-domains.md`

## Evidence limits

No real workspace, residency locator, browser profile, or owner attestation
was consulted for this decision. This ADR's evidence is: the committed
source of `packages/derivation/live_viewing.py` as read directly for this
ADR; the Track 1/1b findings note and its review, cited only for the
confirmatory role described in Context — never as the basis for the
retention claim itself; and, for the "already total" claim specifically,
Track 2's repair's own widened filesystem search (Part 1), which is used as
direct, load-bearing evidence — not merely confirmatory — for the narrower
claim this ADR now makes about that channel, verified against the actual OS
process (`lsof`) and not accepted from timing alone. That search remains
one observation, on one machine, on one resolved Chrome build, on real
per-user macOS locations (never a real workspace, residency locator, or real
typed data) — see the findings note's own evidence-ceiling statement.

**One coverage limit in that search, stated so it is not misread.** The
widened scan greps only regular files. The two artifacts it found outside
confinement are a socket and a symlink, so neither was covered by the
automated token scan. The claim that they hold no typed content rests on two
other things instead: the symlink target was read by hand across four
instances, and a Unix domain socket has no persisted bytes to hold anything
in the first place — a structural property, not an observation. Both are
adequate. But "the widened scan found no token" must not be read as covering
these two artifacts, because it did not examine them.
