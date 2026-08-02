# Charter — Entry Boundary, Track 2 repair: widen the probe, then fix ADR-0048

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-boundary.md`
- Branch: `milestone/entry-boundary` (ADR at `3e9e6c3`, review at `17aea58`)
- Review being repaired: `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-28-entry-boundary-track2-review.md`

Two pieces, in this order. The second depends on what the first finds.

## Part 1 — widen the probe

The review found the ADR's load-bearing claim undetermined: the vehicle's launch
arguments contain no `--disable-breakpad`, no `--disable-crash-reporter`, and no
`--crash-dumps-dir`, so nothing establishes that Chrome writes only inside the
confined session directory. Source reading cannot settle it. Observation can.

Re-run the existing crash scenario in `tools/entry_probe/`, with the filesystem
search **widened beyond the confined session directory**. The previous runs only
looked inside the directory the vehicle manages, which is exactly where the
question is not.

Search the places a Chromium build could plausibly write for the current user
outside a redirected profile. On macOS the known candidates are the per-user
crash-report directory, the per-user caches directory, temporary directories,
and any Chrome or Chromium application-support location. Determine what actually
appeared as a result of your run rather than cataloguing what exists.

Method notes that matter:

- **Take a before-and-after inventory.** These locations have pre-existing
  contents that have nothing to do with you. A file that was already there is
  not a finding. Snapshot before launch, snapshot after the crash, diff.
- Search for the synthetic tokens, and separately for anything new the run
  produced regardless of whether it holds a token. A crash dump that exists but
  contains no typed text is a different finding from one that does, and both
  matter.
- Exercise the **crash** path specifically — `SIGKILL`, no clean close. A clean
  close deletes the session directory and is not the case in question.
- Re-confirm your grep with a positive control, as the previous runs did.

Fold the result into
`docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-boundary-retention-findings.md` as a
new section. Do not delete or rewrite the existing findings.

The honest possible outcomes are: nothing was written outside the confined
directory; something was written but holds no typed content; or typed content
was found outside the boundary. Report which, plainly. **The third would be the
most important finding of this milestone** — if you find it, stop probing, record
exactly what you saw and where, and say so first in your report.

## Part 2 — repair ADR-0048

Do this after Part 1, and let Part 1's result decide what the ADR can claim.

**Repair 1 — the internal contradiction.** The section titled "Decision 1 —
answer" asserts confinement is "already total" and a surviving crashed profile is
"untidy, not an escape." The later "Weakest point" section concedes it cannot
rule out writes outside the redirected paths. Both cannot stand.

A reader who stops at the section called "answer" must not come away with a
stronger claim than the ADR actually supports. Make the answer section carry its
own limits. Do not fix this by softening every sentence — state what is
established, state what is not, and let the difference be visible.

If Part 1 found nothing outside the boundary, the claim gets stronger but is
still bounded by one observation on one machine on one Chrome build. Say that.
An observed absence is not a mechanism, and the ADR should not present it as one.

**Repair 2 — the orphaned profile against ADR-0047.** ADR-0047 classified backup
and indexing as silently fatal preconditions. ADR-0048 does not mention them at
all. A profile orphaned by a crash sits inside the residency for an unbounded
time, which is materially different from one that exists for the length of a
session — it is exposed to whatever backs up or indexes that location.

Work through whether that changes "untidy, not an escape." Reach a position and
state it. If the answer is that an orphaned profile needs a sweep, or a preflight
condition, or an owner attestation, say which and name it as owed to a later
milestone — do not design it here.

**Repair 3 — check your own consistency.** The review found one place where a
section's confidence outran the ADR's own later concession. Re-read the whole ADR
for the same pattern, including in the spellcheck condition and in Decision 2's
claim that the write path was structurally forced rather than merely preferred.

## Boundaries

- **Do not modify product code.** Not `live_viewing.py`, not `chrome.mjs`, not
  `server.mjs`. Adding `--disable-breakpad` would make the ADR's claim true by
  construction and is the obviously tempting move; it is out of scope for this
  milestone and belongs to whichever milestone builds the entry surface. If your
  findings argue for it, **recommend it in the ADR as owed work** rather than
  doing it.
- Synthetic only. No real workspace, no residency locator anywhere — take extra
  care here, because Part 1 has you searching real per-user directories for the
  first time in this milestone. Report paths in a form that names the location
  category, not anything that identifies a residency.
- Do not ratify. The ADR stays proposed.
- Do not revise the review.

## Stop conditions

- Typed content found outside the confined directory. Stop and report first.
- Repairing the ADR turns out to require deciding packaging or correction.
- Part 1 cannot be run without modifying the vehicle.

## Report back

Part 1's before/after method and what it found, stated as one of the three
outcomes above. Then the ADR diff, what claim it now makes, and the weakest point
that remains.
