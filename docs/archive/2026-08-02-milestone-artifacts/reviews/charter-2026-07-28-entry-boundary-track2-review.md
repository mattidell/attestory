# Charter — Entry Boundary, Track 2 review: ADR-0048, with Track 1b folded in

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-boundary.md`
- Branch: `milestone/entry-boundary`, reviewed commit `3e9e6c3`
- Under review: `docs/adr/0048-entry-boundary.md`, its `docs/adr/INDEX.md` row,
  **and** Track 1b (`513ff93`), whose separate review the owner folded into this
  one

This is the last gate before the milestone's closing PR. Nothing else stands
between this review and the record.

## What is being claimed

ADR-0048 answers yes-with-conditions to "is a browser form an acceptable place
to type real tax facts," and "contribution event" to the write-path question.

Its argument deliberately does **not** rest on the probe's negative results,
because those are narrowed but not closed on two channels. It rests instead on
confinement: every browser-writable path is checked against the residency root
before anything is created, so retained text was retained inside the boundary
and never crossed it. Disposal by `rmtree` on `close()` is the secondary claim.

## The measurement that matters most

**Measurement 1 — does the confinement claim actually cover everything Chrome
writes?**

The Builder named this as the weakest point in its own reasoning, which is to
its credit and does not discharge it. The claim holds only if `--user-data-dir`
and `--disk-cache-dir` capture every location Chrome writes for a profile.
Historically some Chromium builds write crash dumps and GPU shader caches to
fixed per-user locations that no such flag redirects.

If such a location exists, it is outside both the confinement check and the
disposal `rmtree`. That is not an untested channel — it is a hole in the load-
bearing argument, and the ADR would be asserting containment it does not have.

Read `packages/derivation/live_viewing.py`'s launch arguments and determine
what is and is not redirected. Check specifically whether crash reporting is
disabled or redirected, and whether any cache or dump path is left at its
default. Report what you find concretely. If you cannot settle it by reading,
say it is undetermined and say what would settle it — do not resolve it by
assuming in either direction.

**Measurement 2 — is "untidy, not an escape" right?** On a SIGKILL or power
loss, `close()` never runs and the profile survives. The ADR reasons that
confinement is established at launch, independent of teardown, so a surviving
profile is inside the residency and therefore not an escape. Test that
reasoning. Consider whether anything about a surviving profile is materially
different from a live one — discoverability, lifetime, whether anything else on
the machine indexes or backs up that location. ADR-0047 already classified
backup and indexing as silently fatal preconditions; check whether that
interacts with an orphaned profile and whether ADR-0048 accounts for it.

**Measurement 3 — is the spellcheck condition real or decorative?** The ADR
requires the network path be affirmatively closed by a launch flag rather than
observed off. Confirm that condition is stated as binding, that the ADR does not
quietly rely on a default, and that it is honest about a cooperative flag not
being a boundary — the same reasoning ADR-0047 applied to its own Class C.

**Measurement 4 — is question 2 as settled as the ADR says?** It claims direct
fact writes are structurally unavailable under ADR-0002's append-only act log
and ADR-0032, so the write path was never a live fork. Verify that against those
ADRs' actual text. An ADR that reports a decision as forced when it was merely
preferred misleads a later reader about how much room they have.

It also concludes no actor or origin field is needed, since a contribution is
already inherently human-initiated and there is one owner. Check that against
ADR-0032. Consider whether the reasoning survives a second person or a machine-
assisted entry path, and whether the ADR should say what would reopen it.

## Track 1b, folded in

**Measurement 5.** Track 1b (`513ff93`) re-ran the probe against the headed
vehicle. It had no separate review gate, so it gets one here.

Confirm: `live_viewing.py`, `chrome.mjs`, and `server.mjs` are unmodified —
verify against base rather than accepting the claim. The grep positive control
was genuinely re-run for this vehicle and proves what it claims. The headless
results were preserved rather than overwritten. Synthetic only, no residency
locator, not wired into CI. The "no channel differed" conclusion follows from
what was actually observed.

## The rest

**Measurement 6 — scope.** The ADR must not decide packaging, correction, or any
UI design, and must make no maturity claim. Flag anything that decides one of
those by implication.

**Measurement 7 — is it legible on its own?** Someone reading only ADR-0048 a
year from now should learn whether a browser form is permitted and what write
path it must use, without reconstructing this milestone. Read it as that person.
Name any place it assumes context it does not carry — this phase exists to fix
exactly that failure, so an ADR that commits it is worth catching.

**Measurement 8 — are the four undecided items honestly held?** Orphan sweep,
spellcheck mechanism, the Chrome-writes-elsewhere question, and the entry
session's preflight shape. Confirm each is genuinely deferred rather than
quietly load-bearing, and that a reader can tell which parts of the decision
depend on one being resolved later.

## Verdict

`READY` requires 2 through 8 to pass and measurement 1 to be answered.

Measurement 1 may legitimately land on "there is a gap." If so, say whether the
gap invalidates the ADR's central claim or narrows it — those call for different
repairs, and the foreman needs to know which.

Write your review to `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-28-entry-boundary-track2-review.md`.
Do not repair anything yourself.
