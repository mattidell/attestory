# Charter — Entry Boundary, Track 2 focused recheck

- Role: **Reviewer** (`docs/roles/reviewer.md`) — the same Reviewer who issued
  `docs/reviews/2026-07-28-entry-boundary-track2-review.md`
- Branch: `milestone/entry-boundary`
- Repair commit: `0df113e` (reviewed commit was `3e9e6c3`; review was `17aea58`)

This is a **focused recheck**, not a second full review. Scope is the findings
you raised and the artifacts the repair touched. Do not re-derive measurements
4, 5, or 6 except where the repair's diff reaches them.

## What the repair claims

**Part 1 — the probe was widened past the confined directory**, before-and-after
inventory, crash path exercised with `SIGKILL`, birthtime rather than mtime used
to distinguish this run's artifacts from unrelated churn (the machine had an
unrelated Chrome running throughout).

Result: the vehicle creates `com.google.Chrome.<random>/{SingletonSocket,
SingletonCookie}` directly under the temp directory — a **sibling of**, not
inside, the confined session tree. It survives `SIGKILL` and `close()` never
touches it. Contents are a Unix domain socket and a symlink to a random IPC
authentication number. No typed field value in either, across four instances.
Attribution was made at the process level via `lsof` on the launched pid rather
than inferred from timing.

Nothing attributable to the vehicle appeared in crash-report directories,
caches, or application support. No Crashpad artifact appeared.

**Part 2 — the ADR was repaired.** It no longer claims confinement is total. It
claims confinement is total over the four destinations `_confined_destinations()`
computes, and states as established fact that this does not cover everything
Chrome writes, naming the exception. "Untidy, not an escape" is scoped the same
way. A new subsection ties an orphaned profile to ADR-0047's backup and indexing
preconditions and names sweep work as owed. A reopening trigger was added for the
actor/origin reasoning. `--disable-breakpad`-class work is recorded as owed
rather than done.

## Measurements

`READY` requires all five.

1. **Finding 1 closed.** The contradiction between the answer section and the
   weakest-point section is gone, and gone by making the answer carry its limits
   rather than by hedging everything. A reader who stops at the answer section
   must now come away with a claim the ADR can support. Read it as that reader.

2. **The new claim is exactly as strong as the evidence.** The ADR now rests on
   "no *typed content* was found outside confinement," not "nothing is written
   outside confinement" — which the repair itself disproved. Confirm the ADR
   does not slide back toward the stronger claim anywhere, and that it is honest
   that this is one observation on one machine and one Chrome build, not a
   mechanism.

3. **The singleton finding is characterized honestly.** Check the reasoning that
   a socket and an IPC cookie carry no typed content, and that this is a real
   conclusion rather than an assumption from what those files are named. Consider
   whether their *existence* outside confinement matters for any reason other
   than content — lifetime, what they reveal, whether an orphan accumulates.
   Say so if it does.

4. **Finding 2 closed without overcorrection.** The orphaned-profile subsection
   must engage ADR-0047's backup and indexing preconditions substantively, reach
   a position, and name what is owed — without designing a sweep, adding a
   preflight condition, or implying either is scheduled.

5. **Boundaries held.** `live_viewing.py`, `chrome.mjs`, and `server.mjs`
   unmodified — verify against base, do not accept the claim. No product code
   changed. The ADR is still `proposed`. No residency locator anywhere, with
   particular care in the new findings section, which reports on real per-user
   directories for the first time in this milestone: locations must be named by
   category, never in a form that identifies a residency. Existing findings
   preserved rather than rewritten. INDEX row consistent with the ADR.

## Verdict

If `READY`, say so plainly and name any residual you would want a later
milestone to carry — the milestone closes on this recheck.

If `NOT READY`, be specific about which measurement failed and what would close
it.

Write your recheck to
`docs/reviews/2026-07-28-entry-boundary-track2-recheck.md`. Do not repair
anything yourself.
