# Retrospective — Browser Evaluation Runner Completion

Status: **complete.** Track 1 (adopt-and-repair) plus the owner-authorized
R1/R2 residual repair merged as PR #71, `c329afd`, on 2026-07-25. This is a
bounded tooling-completion milestone: it establishes the browser evaluation
runner as trustworthy development tooling and makes no product, economy, or
maturity-matrix claim.

## Milestone

- Planning unit: owner-directed plan prepared 2026-07-25 on `main`.
- Implementation: `track/browser-evaluation-runner-completion`, adopting the
  preserved implementation commit "implement Track 1 instrumented harness
  core and fail-closed lifecycle" from
  `track/presentation-economy-t1-harness-core` (the runner rejected by the
  Presentation Evaluation Process Economy milestone's Track 1 review) rather
  than rebuilding it.
- Accepted implementation: PR #71, "Complete browser evaluation runner
  integrity," merged `c329afd94286b348b027360d38bf06301034166d` at
  2026-07-25T23:12:23Z. CI `verify` passed on the merge commit
  (https://github.com/mattidell/attestory/actions/runs/30178895861).
- Maturity effect: none. No product presentation surface, ADR, or matrix cell
  was added or raised.

## Shipped

The runner now closes all six blockers the original independent review found
in the adopted implementation:

1. per-tuple browser storage (cookies/`localStorage`) isolation within one
   Chrome process per invocation;
2. injection parse/execution proven before candidate code; a malformed or
   non-executed injection can no longer become a pass;
3. cancellation-safe cleanup of every runner-owned child, target/context,
   server, and temporary profile on normal, error, `SIGINT`, and `SIGTERM`
   paths;
4. canonical manifest-path confinement with normalized repository-relative
   provenance (traversal/absolute/symlink inputs rejected);
5. strict, non-vacuous check-parameter and selection validation; and
6. redacted external error output — fixed, closed reason codes replace raw
   exception text, stack traces, and rejected-input echo.

It also completes the four measurements the original review had transferred
as incomplete: explicit live process/target enumeration, cleanup evidence for
every exit class, exhaustive public-output leakage scanning, and whole-dataset
validation of a captured `presentation-economy-observation.v1` fragment
against the public Track 0 surface.

After the delta review returned `READY`, voluntary post-verdict exploration
(at owner invitation, past the chartered boundary) surfaced two non-blocking
residuals:

- **R1** — the injection-acknowledgement wait could bypass the manifest
  `timeout_ms` and still return a pass.
- **R2** — the fixed acknowledgement marker was guessable/collision-fragile
  across tuples.

The owner authorized one narrow repair charter plus one focused two-finding
recheck as an explicit exception to the plan's fixed one-repair/one-review
cap. The repair bounded the acknowledgement wait by `timeout_ms` and made the
marker per-tuple and non-guessable, without changing public output. The
focused recheck returned `READY` with no new in-scope finding.

## Verification

- Original delta review (`docs/reviews/2026-07-25-browser-evaluation-runner-repair-review.md`):
  `READY`. Reproduced F1–F6 closed; full focused Node suite 33/33 and Python
  focused suite 27/27 passing; batch continuation and non-loopback blocking
  unmodified and passing; governance lint conformant, envelope scan clean,
  `git diff --check` clean; PR #71 CI `verify` green
  (https://github.com/mattidell/attestory/actions/runs/30175915176).
- Residual R1/R2 delta review
  (`docs/reviews/2026-07-25-browser-evaluation-runner-residual-repair-review.md`):
  `READY`. Both R1 and R2 independently reproduced closed; accepted F1–F6
  floor intact (34/34 focused tests); scope held to the chartered two
  findings plus directly touched invariants, no re-opening of the original
  sweep.
- Final state: PR #71 merged with CI `verify` green on the merge commit
  itself, confirmed directly against `origin/main` at re-entry.

## Decisions

- **Owner scope decision, 2026-07-25:** adopt the existing reviewed
  implementation rather than a clean-room rebuild, per the milestone's
  non-goals.
- **Owner exception, 2026-07-25:** authorize exactly one R1/R2 residual
  repair and one focused two-finding recheck as a bounded exception to the
  plan's fixed cap, rather than opening a second general review cycle or
  deferring the residuals unaddressed.
- No Tier 2/3 architecture decision and no ADR — consistent with the plan's
  decision posture.

## Deviations

None from the ratified plan's exit criteria, except that criterion 16 (focused
R1/R2 recheck, "no further review cycle opens automatically") required the
owner's explicit one-time exception rather than being inside the plan's
original fixed cap; the plan anticipated this path and named it as an
allowed exception, not an open-ended one.

## Disposition

- The Presentation Evaluation Process Economy milestone's rejected Track 1
  browser harness is superseded: its implementation is the one adopted and
  repaired here, and it does not need separate re-review.
- The runner is now available as trustworthy tooling for later presentation
  work. It carries no economy claim, product finding, or comparison of its
  own — that remains for a future milestone to use and measure separately.
- The Presentation frontier toward a human surface remains the selected but
  deliberately deferred direction (per the phase roadmap); this milestone
  removes the "runner not trustworthy" blocker on beginning that work, without
  itself starting it.

## Next

`track/browser-evaluation-runner-completion` may be deleted; its content is
fully contained in `main` at `c329afd`. No further review cycle is open. The
next owner-directed milestone selection is the Presentation frontier, or
another maturity-matrix frontier candidate, at the owner's discretion.
