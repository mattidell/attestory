# ADR 0048 — The Entry Boundary

- Status: **proposed** (not ratified — ratification is the owner's). Builder
  draft, Entry Boundary milestone Track 2
  (`docs/reviews/charter-2026-07-28-entry-boundary-track2.md`).
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
`docs/phases/legible-entry/milestones/entry-boundary-retention-findings.md`.

### Why this ADR does not rest on the probe's negative results

The probe observed, in both vehicles: no retained token in any on-disk store,
and zero non-loopback network requests. Read at face value, that looks like
"browsers don't retain typed text here." It is a weaker result than that,
for two specific reasons the Track 1 review
(`docs/reviews/2026-07-28-entry-boundary-track1-review.md`) and the probe's
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
background stores, in both vehicles, and none of them left the confined
directory tree — are used only as confirmation of those two properties, not
as the basis for a claim about Chrome's retention behavior in general.

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

**This holds.** Every path the browser can write into is inside the
residency, checked before use, independent of whatever Chrome itself
chooses to write, retain, or forget.

### Disposal

`LiveViewingSession.close()` calls `_stop_process()` then
`_remove_session()`, which `rmtree`s the session root. A failure in either
step raises `BROWSER_TEARDOWN_FAILED` rather than swallowing the error — a
loud failure, not a quiet one. Used as a context manager (`__enter__`/
`__exit__`), `close()` runs whenever Python's own exception handling gets a
chance to run, including most launch-time failure paths (`_abandon_launch()`
is called from every named exception branch of `launch()`, itself
best-effort and documented as such in the module's own comment).

**This is real, and it is the better foundation than the probe's
per-channel negatives, exactly as the charter argues.** Whatever a browser
retains about typed text — proven or not, tested or not — dies with the
profile directory on a normal close, regardless of which retention channel
did the retaining. It is a single mechanism covering every channel at once,
including channels this project has never enumerated and Chrome might add
tomorrow. That is a materially stronger property than "we checked five
channels and none fired."

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
asserted:** confinement is established once, at destination-computation
time, before anything is written — it does not depend on `close()` running
at all. A profile that survives a crash still sits under
`capability.location/.live-view/session-<uuid>/`, inside the residency
ADR-0031 already treats as the place real data lives. Nothing about a crash
moves those bytes anywhere else. **This is untidy, not an escape.** The
practical consequence is an operational one, not a boundary breach: orphaned
session directories accumulate under `.live-view/` with every crash this
vehicle does not currently sweep up on a later launch, and they hold
whatever the browser wrote before the kill — potentially including, per
above, form-history writes accepted via a save prompt or session-restore
snapshots, if a future session ever drives those interactions. This ADR
leaves that sweep undecided; see "Left undecided" below.

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

This is a narrower "yes" than "browsers are safe." It is: *this vehicle's
filesystem confinement holds regardless of clean or crashed exit, and its
disposal-on-close eliminates the retention question for every filesystem
channel at once on a normal session, with one closeable gap named above and
one operational residual (orphaned crash directories) left undecided.* No
new retention channel this project has not already named would escape
confinement, because confinement does not depend on knowing which channel
exists — it depends only on where the browser is allowed to write, which is
already total.

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
- The next milestone (packaging) inherits two open obligations this ADR
  names but does not discharge: an affirmative spellcheck-disabling flag,
  and a decision about whether crash-orphaned session directories need a
  sweep.

## Left undecided

- **Whether stale `.live-view/session-<uuid>` directories from a crashed
  controlling process need to be swept on a later launch.** Untidy, not an
  escape, per the reasoning above — but this ADR does not decide whether
  that untidiness is acceptable indefinitely or needs a cleanup mechanism.
- **The exact mechanism for closing the spellcheck network path** (a launch
  flag, a Chrome policy, or something else) — named as a requirement, not
  designed here.
- **Whether Chrome writes anything at all outside the paths
  `live_viewing.py` explicitly redirects.** Neither this ADR's reading of
  the module nor the Track 1 probe checked locations outside the confined
  session directory and the synthetic workspace root — global,
  per-user-account Chrome state that some Chromium versions place outside
  `--user-data-dir` regardless of the flag (crash-reporting and GPU-shader
  disk caches are the known historical candidates) was never inspected by
  either. See "weakest point" below.
- **The entry session's own preflight/attestation shape**, if it differs
  from a viewing session's — explicitly left to the packaging milestone.

## Weakest point in this ADR's own reasoning

The confinement argument is strong only to the extent that
`--user-data-dir` and `--disk-cache-dir` actually capture *everything*
Chrome writes for a given profile. This ADR's source reading and the Track 1
probe both operated entirely inside the paths those flags name (plus the
synthetic workspace root as a whole, for the probe). Neither checked whether
this or another Chrome build writes anything to a fixed, per-user-account
location that is not redirected by any flag `live_viewing.py` currently
passes. If such a location exists, disposal does not touch it (it is never
inside the session root `close()` deletes) and confinement does not apply to
it either (it was never checked against the residency root, because nothing
in `_confined_destinations()` considers it). That would be a genuine gap in
the confinement claim, not merely an untested channel — and this ADR cannot
rule it out from what was read. It reads as a plausible, testable next
question rather than a known hole, but it is the one place this ADR's
"confinement is total because it's checked before any write" claim could be
wrong.

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

## Links

- Milestone: `docs/phases/legible-entry/milestones/entry-boundary.md`
- Charter: `docs/reviews/charter-2026-07-28-entry-boundary-track2.md`
- Probe findings (both vehicles):
  `docs/phases/legible-entry/milestones/entry-boundary-retention-findings.md`
- Track 1 review (headless-only scope, corrected by Track 1b):
  `docs/reviews/2026-07-28-entry-boundary-track1-review.md`
- Vehicle: `packages/derivation/live_viewing.py`
- Residency: `docs/adr/0031-real-data-residency-boundary.md`
- Contribution: `docs/adr/0032-contribution-boundary.md`
- Viewing session: `docs/adr/0047-live-viewing-environment.md`
- Trust domains: `docs/adr/0044-live-run-system-boundary-and-trust-domains.md`

## Evidence limits

No real workspace, residency locator, browser profile, or owner attestation
was consulted for this decision. This ADR's evidence is: the committed
source of `packages/derivation/live_viewing.py` as read directly for this
ADR, and the Track 1/1b findings note and its review, cited only for the
confirmatory role described in Context — never as the basis for the
retention claim itself.
