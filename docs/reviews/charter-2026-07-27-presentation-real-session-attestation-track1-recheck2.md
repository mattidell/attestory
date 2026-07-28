# Charter — Track 1 second recheck

- Role: **Reviewer** (`docs/roles/reviewer.md`), focused recheck
- Milestone: `docs/phases/real-return/milestones/presentation-real-session-attestation.md`
- Base: `milestone/presentation-real-session-attestation-tracks` @ `36317be`. Verify the SHA before starting.
- Prior verdict: NOT READY, `docs/reviews/2026-07-27-presentation-real-session-attestation-track1-recheck.md`

## Context Capsule

- Source ref and resolved launch commit: `36317be`
- Exact object or commit range: `894ff23..36317be` — the runbook, `live_session.py`, `live_viewing.py`, `tests/test_presentation_live_session.py`
- Role: Reviewer (second focused recheck)
- Scope and evidence-rung ceiling: your blocking finding, your two accuracy findings, the two residuals directed closed, and anything this repair newly introduced. Nothing you already passed.
- Stop conditions: any need for a real workspace or a headed browser launch
- Full reads before acting: this charter; the second repair charter; the diff `894ff23..36317be`

You hold your own prior findings and your own demonstration of the interrupt
residue. Re-derive nothing already settled.

## Confirm the blocking finding is closed

You demonstrated the failure by running it. **Confirm the fix the same way.** The
builder says it reproduced your demonstration as a test before fixing, and
verified the new failure-path tests fail against pre-fix source. Check that
claim rather than accept it, and check the state you originally measured: no
surviving browser process, no surviving session directory, no listening socket,
after an interrupt.

Note the builder's own honesty flag: `LivePresentationSession` **already had**
`__enter__`/`__exit__`, so the context-manager test passes against pre-fix code
and is a regression guard rather than evidence of this repair. Decide what that
means for coverage — the half that actually changed is the template using
`with`, and a template is not covered by a test.

## Review the refactor as new work

`_abandon_launch(process, destinations)` was extracted and the **two
pre-existing** teardown handlers in `launch` were rewired to call it. That is a
change to paths you already passed. Confirm it is behaviour-preserving for both,
and that ordering and best-effort semantics are unchanged.

Same for `_release_quietly(viewing, server)` replacing `_close_quietly(server)`.

## Probe the specific mechanisms

- **The hoisting window.** The builder says `launch` tearing down its own partial
  state does not cover the gap between `launch` returning and
  `open_presentation_session` returning, where `viewing` is live and owned by
  nobody, and that hoisting `viewing = None` before the `try` closes it. Verify
  the window is actually closed, including on `BaseException`.
- **`__context__`.** The builder found that `raise X from None` **re-attaches**
  `__context__` at raise time regardless of how the object was constructed, and
  moved the raise outside the handler so `sys.exc_info()` is clear. Verify
  independently — this is the locator-confinement claim and you were the one who
  found the original leak. Confirm `__context__`, `__cause__`, and
  `__suppress_context__` on a real classified failure carrying a path.
- **`_PresentationServer.close`** now runs `server_close()` in a `finally`.
  Confirm a `shutdown()` failure can no longer leave a listening socket.

## Assess the two judgment calls left open

The builder named both rather than resolving them silently. Assess each; either
may be accepted as a named residual.

1. `_abandon_launch` and `_release_quietly` are best-effort by construction —
   they run while another exception is in flight and must not replace it, so a
   teardown failure *on a failing path* is invisible. The builder judged that
   making it visible would mask the original failure, which is worse. Is that
   right, and is the invisibility named where a reader will find it?
2. `LivePresentationSession.__exit__` raises `PresentationSessionError` on
   teardown failure, which would **mask an in-flight `KeyboardInterrupt`**. The
   builder left this deliberately, reasoning that a failed teardown is the more
   urgent fact and Python chains the interrupt onto `__context__`. Note the
   tension with the locator-confinement work above, where `__context__` is
   treated as a surface that must be cleared.

## Runbook changes

- The Step 5 interrupt subsection: does it tell the owner the right thing,
  including that the absence of a `torn down` message is expected rather than a
  failure?
- The softened closure claim: does it now match the code?
- The new instruction **"if you see a traceback, do not read it and do not quote
  it."** This is new and was not requested. Assess it — it is either the
  sharpest sentence in the artifact or an instruction the owner cannot follow,
  since a traceback is already on screen by the time they could obey.
- The argv warning and its framing as after-the-fact notification rather than
  protection, explicitly contrasted with the structural guarantees.
- The new "Named residuals of this runbook" section: is it complete and honest?

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

`live_viewing.py` is used beyond this module; the builder ran the full suite
(670 tests). Confirm.

## Hand-off

Return **READY** or **NOT READY**. If READY, list what remains as named
residuals — Tracks 2 and 3 are owner-operated and unrepeatable, so an overstated
READY costs more here than on a normal build track.

If you find yourself reaching for a third round on something that is genuinely a
residual rather than a defect, say so plainly and return READY with it named.
The foreman would rather carry an honest residual into Track 2 than spend a
cycle closing something that was never going to be closed.
