# Charter — Track 1 review: session runbook and non-descriptive failure vocabulary

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Milestone: `docs/phases/real-return/milestones/presentation-real-session-attestation.md`
- Base: `milestone/presentation-real-session-attestation-tracks` @ `748b8e8`. Verify the SHA before starting.
- Unit under review: `docs/runbooks/presentation-real-session.md` (new, 365 lines). No code changed.

## Context Capsule

- Source ref and resolved launch commit: `748b8e8` on `milestone/presentation-real-session-attestation-tracks`
- Exact object or commit range: `26661e7..748b8e8`
- Role: Reviewer
- Scope and evidence-rung ceiling: review only. Report findings; do not repair.
- Stop conditions: any finding that requires reading a real workspace; any need to launch a headed browser
- Full reads before acting: this charter; the build charter `docs/reviews/charter-2026-07-27-presentation-real-session-attestation-track1.md`; the milestone plan; `docs/adr/0047-live-viewing-environment.md`; `docs/adr/0031-real-data-residency-boundary.md`; the unit under review; `packages/derivation/live_session.py`; `packages/derivation/live_viewing.py`; `AGENTS.md` ("Data Safety Rules")

## Why this review is independent

The foreman wrote the milestone plan and the build charter, which is where the
vocabulary's governing distinction — mechanical versus evaluative — was drawn.
A review by the author of that distinction could only test the builder's
execution of it, not the distinction itself. You are here to test both.
Preserve fresh-reader independence: form your own view of whether the line is in
the right place before reading the builder's defense of where it landed.

## The central gate — the smuggle test

The vocabulary is the only legal channel from a failed real session back to a
repair. It is a data-safety artifact governed by ADR-0047 precondition 5, which
forbids values, identifiers, **dispositions**, screenshots, and the locator from
chat, reviews, PRs, and the repository.

**Attempt to smuggle a disposition through it and expect to fail.** Construct
statements that are individually legal under the vocabulary but that, alone or
in combination, let a reader infer something about the owner's actual return.
The builder proposes a test — *"could this sentence be true regardless of what
the correct output actually was?"* — decide whether that test actually holds the
line or merely sounds like it does.

Probe at least these, which the builder either raised or which follow from what
it raised:

- **Bare counts.** The builder ruled "nine sections rendered" illegal as a
  disposition in numeric clothing. Is that right, and is it applied
  consistently? Note that the *synthetic* rehearsal record states a section
  count openly, so the rule must distinguish contexts rather than forbid counts
  outright.
- **Combination.** The builder names ordering and co-occurrence of two
  individually-legal facts as an unresolved edge. Is it genuinely unresolvable,
  or is it under-specified?
- **Repetition across attempts.** Same question.
- **Reason codes.** A refusal code is legal to report. Verify that no code in
  `live_session.py` or `live_viewing.py` encodes anything about content or the
  locator such that reporting it would itself be a crossing.

## The second gate — is it too tight?

A vocabulary so restrictive that a real failure fits nothing is not safe; it is
unsafe in the other direction, because the owner will improvise, and an
improvised description is exactly the breach. Judge usability as a safety
property, not as a convenience.

The builder's stated fallback is "report that nothing fits." Decide whether that
is a real escape hatch or a dead end — specifically, whether it leaves the
project any way to act on a failure it cannot see.

## The third gate — the locator recommendation

The builder recommends an interactive `input()` prompt over a CLI argument, an
env var, or a file, and states it is **not a full closure** because reaching a
terminal at the residency may still require a hand-typed `cd`.

Assess the reasoning, not just the conclusion. One concrete probe the foreman
wants checked rather than assumed: **`input()` echoes what is typed.** Consider
terminal scrollback, terminal session logging, and any shell or terminal
emulator that persists pane contents — and whether a non-echoing form is
materially better or merely differently exposed. Accepting exposure as a named
residual remains a legitimate outcome; an unnamed one does not.

## Also verify

- The clipboard rule — **no copy at all while clipboard-history retention is in
  force** — appears where the owner reads it *before* looking, not in a footnote.
- The reason-code glossary matches the actual stable codes in the source, with
  no invented, renamed, or stale entries.
- The runbook makes unmistakable that the three preflight answers come from the
  owner's trust domain and that the project observes nothing — `PreflightProbes`
  is an injected input by ratified design, not an unimplemented feature.
- The clipboard preflight's partiality is presented as an owner-responsibility
  remainder, never as a clearance.
- **No locator, path fragment, canonicalized form, derived identifier, or
  absolute local path** anywhere in the unit.
- The script template does not, in its own worked example, undo the locator
  recommendation.
- Docs-only was the right call: confirm `open_presentation_session` genuinely
  runs as one act, so declining the scriptability repair was correct rather than
  convenient.
- `tools/presentation_harness/lib/server.mjs` and both evaluation manifests are
  byte-unchanged.

## Verification

```text
python3 -m unittest tests.test_presentation_live_session
python3 -m unittest tests.test_presentation_live_viewing_vehicle
python3 -m unittest tests.test_presentation_l2_integration
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/citation-walk.v1.json
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/citation-walk-production-shaped.v1.json
python3 tools/envelope_scan.py --range main..HEAD
git diff --check
```

## Hand-off

Return **READY** or **NOT READY** with findings ranked most-severe first. For
each finding give the failure it produces, not just the rule it breaks — this
artifact's failures are boundary crossings and unusable-in-the-moment
instructions, so say which.

A finding that the mechanical/evaluative line is drawn in the wrong place is in
scope and is the most valuable thing you can return. So is a finding that the
build charter or the milestone plan asked for the wrong thing; the foreman wrote
both and cannot see their own framing errors.
