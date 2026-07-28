# Charter — Track 1 focused recheck

- Role: **Reviewer** (`docs/roles/reviewer.md`), focused recheck
- Milestone: `docs/phases/real-return/milestones/presentation-real-session-attestation.md`
- Base: `milestone/presentation-real-session-attestation-tracks` @ `894ff23`. Verify the SHA before starting.
- Prior verdict: NOT READY, `docs/reviews/2026-07-27-presentation-real-session-attestation-track1-review.md`

## Context Capsule

- Source ref and resolved launch commit: `894ff23`
- Exact object or commit range: `748b8e8..894ff23` — `docs/runbooks/presentation-real-session.md`, `packages/derivation/live_session.py`, `tests/test_presentation_live_session.py`
- Role: Reviewer (focused recheck)
- Scope and evidence-rung ceiling: the five filed findings, plus the two changes the builder made beyond them, plus anything the repair newly introduced. Not a re-review of what you already passed.
- Stop conditions: any need for a real workspace or a headed browser launch
- Full reads before acting: this charter; the repair charter; the repair diff `748b8e8..894ff23`

This is a **focused recheck**, not a fresh review. You hold your own prior
findings and your own independently-formed view of where the
mechanical-versus-evaluative line belongs. Re-derive nothing you already
settled; the sections you confirmed sound are not back in scope unless the
repair touched them.

## Confirm the five findings are closed

For each, decide whether the repair closes the *failure* you named or merely the
sentence you wrote. Finding 1 in particular: you named a class of failures
reaching the owner unclassified — confirm that class is now empty for this call
path, not merely that the specific codes you listed are handled.

## Scrutinize the two changes the builder made beyond the findings

The builder went past the charter twice, flagged both, and the foreman wants
them reviewed as new work rather than accepted on the builder's account of them.

1. **`BaseException` is deliberately left unclassified.** The reasoning: a
   `KeyboardInterrupt` is the owner's own act, not a session refusal, and
   turning Ctrl-C into a refusal code would be a lie inside the vocabulary.
   Assess that. Consider what the owner sees and what the vocabulary lets them
   say when they interrupt a session themselves — and whether the socket and
   browser are actually torn down on that path.
2. **Teardown's catch was broadened.** `close()` previously caught only
   `(LiveViewingError, OSError)`. The reasoning: "teardown did not complete" is
   only legal vocabulary if incomplete teardown actually arrives as that code.
   Assess whether the broadening is correct and whether it can now swallow
   something that should have escaped.

## Probe the repair's own new surface

- `_classified_viewing_failure` forwards a `LiveViewingError`'s stable code as a
  sub-code. **Verify no message text, path, argument, or interpolated detail
  travels with it** — the whole point of the wrap is that only stable codes
  cross. Check what `LiveViewingError` actually carries, not just what the
  wrapper intends to take from it.
- The unclassified branch drops detail and raises `from None`. Confirm the
  suppression is complete: no `__cause__`, no `__context__`, and nothing in the
  traceback frames that would print a path if the owner's terminal shows it.
- `except Exception` precedes `except BaseException`. Confirm the ordering and
  the `_close_quietly` placement leave no path on which the server socket
  survives.
- The five new regression tests: do they test the guarantee, or the
  implementation of it? A test that asserts the wrapper was called is weaker
  than one that asserts nothing unclassified escapes.

## Assess the two residuals the builder says it could not close

Invocation discipline and shell `cd` history. Decide whether "not closeable by
anything this repository can write" is accurate or merely convenient, and
whether they are named where the owner will actually read them.

Also assess the Finding 3 limit as restated: a defect manifesting only against
real content stays detectable, non-reproducible, and repairable only by
reasoning about code. Is that stated honestly, and is it in the right place?

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

Confirm `tools/presentation_harness/lib/server.mjs` and both evaluation
manifests are still byte-unchanged.

## Hand-off

Return **READY** or **NOT READY**. If READY, say what remains as a named
residual rather than implying closure the artifact does not have — Tracks 2 and
3 are owner-operated and unrepeatable, so an overstated READY here is expensive
in a way an overstated READY on a normal build track is not.
