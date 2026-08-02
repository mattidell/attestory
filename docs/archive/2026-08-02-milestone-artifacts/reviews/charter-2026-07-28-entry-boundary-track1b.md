# Charter — Entry Boundary, Track 1b: the probe, against the headed vehicle

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-boundary.md`
- Branch: `milestone/entry-boundary` (Track 1 at `a33458a`, review at `367de61`)
- Evidence ceiling: **observation on synthetic fixtures only**, on this machine,
  in this run. No claim about real data, no claim about browsers in general.

## Why this exists

Track 1 built a good instrument and pointed it at the wrong browser. Its
charter named `tools/presentation_harness/lib/chrome.mjs`, which hardcodes
`--headless=new`. That is the synthetic evaluation harness. The vehicle a
person would actually type into is the **headed** one,
`packages/derivation/live_viewing.py`, defined by ADR-0047.

Headless Chrome stubs or disables some of the exact features the probe was
built to detect. So Track 1's "form history: not fired" and "spellcheck: not
fired" may be facts about headless mode rather than facts about the
confinement. The review (`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-28-entry-boundary-track1-review.md`)
could not settle those two channels by reading, and reached this: the findings
stand only for headless mode.

That is the dangerous kind of wrong result. A false negative here reads as
permission. Your job is to re-run the same observations against the browser
that matters.

This is a foreman charter defect, not a build defect. Nothing in Track 1's
method or workmanship is under suspicion — reuse it.

## What to do

Re-run the Track 1 probe against the headed vehicle, against a **synthetic**
workspace directory, and record what changes.

The review established that this is cheap at the code level:
`live_viewing.py`'s `WorkspaceCapability` requires only that its location is a
directory, and the vehicle's own tests already drive it against bare temp
directories. Read `tests/test_presentation_live_viewing_vehicle.py` to see how
it is launched before writing anything.

One operational precondition the review could not check: headed Chrome needs a
display. You are on macOS, so a window server should be present. If it is not,
that is a **stop condition** — report it rather than falling back to headless,
because falling back reproduces the exact defect this track exists to correct.

Keep everything else from Track 1 unchanged: the same form fixture, the same
five channels, the same synthetic tokens, the same binary-safe grep with a
positive control, the same network capture. The point is a controlled
comparison. Change the vehicle, not the method.

## Deliverables

**1. An extended probe.** Extend `tools/entry_probe/` rather than starting
over. Both modes should be runnable, so the comparison is reproducible.

**2. An amended findings note.** Update
`docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-boundary-retention-findings.md` so
that every channel reports **both** modes, and states plainly where they
differ. Do not delete the headless results — the difference between the two is
itself the finding, and it is the part Track 2 will lean on most.

Where a channel now fires that previously did not, that is the most important
sentence in the document. Give it the file path, the store type, and the
contents. Do not soften it.

## Boundaries

- **Synthetic only.** A temp directory standing in for a workspace. No real
  workspace, no real fact, no residency locator anywhere — not in the probe,
  the note, or a commit message.
- **Do not modify `live_viewing.py`, `chrome.mjs`, or `server.mjs.`** If the
  headed vehicle cannot be driven without changing it, that is a charter-stop
  finding. Report it.
- **Do not run the headed vehicle against anything real.** Ever, including to
  "check that it works."
- **Do not wire the probe into CI** or any existing suite.
- **Do not decide anything.** You are not writing ADR-0048, not recommending a
  write path, not saying whether a browser form is acceptable. Track 2 does
  that and must be free to disagree with what your observations suggest.

## Stop conditions

- No display available for a headed launch. Report; do not fall back to
  headless.
- Driving the headed vehicle requires modifying it.
- A channel can only be tested by touching something real.
- **Typed content leaving the machine over the network.** Stop immediately,
  record exactly what you saw, and do not continue probing.

## Verification

State, as Track 1 did: `pytest -n auto` unaffected, fixture-safety scan passes,
envelope scan clean, and no token you introduced resembles real personal data.

Re-confirm your grep with a positive control on this run too. Track 1 found a
flag combination that silently suppressed binary-store matches; do not inherit
that result on trust.

## Report back

The commands you ran and what they printed, the amended note, a plain statement
of which channels differ between headless and headed, anything you could not
test and why, and any charter-stop finding stated plainly.
