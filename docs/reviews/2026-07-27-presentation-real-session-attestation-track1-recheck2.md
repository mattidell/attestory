# Second recheck — Track 1

- Verdict: **READY**, with named residuals
- Reviewed at: `9909cd6`; repair under review `36317be`; diff `894ff23..36317be`
- Charter: `docs/reviews/charter-2026-07-27-presentation-real-session-attestation-track1-recheck2.md`
- Reviewer: the original independent reviewer, holding its own prior findings

Full suite confirmed at **670 tests, OK**. Charter verification green.
`tools/presentation_harness/` byte-unchanged against `main`.

## The blocking finding is closed — re-measured, not re-read

The reviewer re-ran its own demonstration against the real `launch` rather than
a test double. It notes that its *earlier* probes raised the interrupt in a
subclass outside `super().launch()`, which was a test artifact; patching
`live_viewing._wait_for_devtools` puts the interrupt inside the real path.

All three originally-measured conditions are clean, for both `KeyboardInterrupt`
and `SystemExit` inside real launch: no surviving browser process, no surviving
session directory, no listening socket.

**A bonus the builder did not claim:** adding `except BaseException` to `launch`
also picks up `Exception` subclasses the two narrow handlers never caught, so an
`AttributeError` originating in launch — which previously escaped with no
teardown at all — now tears down *and* arrives classified.

**The builder's test claim was checked, not accepted.** Restoring both source
files from `894ff23` and running the four new tests against pre-fix source
produced three failures and one pass — the pass being the `with`-block test,
exactly as the builder flagged: a regression guard, not evidence of this repair.

**`__context__` is genuinely cleared.** Walking the chain on a real classified
failure carrying a path returns a single element, with `__cause__` `None`,
`__context__` `None`, `__suppress_context__` `True`, and nothing reachable by a
tool that walks the chain explicitly. The leak is closed, not hidden.

## The refactor is behaviour-preserving

`_abandon_launch` is a literal extraction; order and best-effort semantics are
identical for both rewired handlers, and the
`LiveViewingError` / `(OSError, ...)` / `BaseException` clause ordering is
correct — the narrow clauses still take precedence. `_release_quietly` preserves
`_close_quietly`'s server behaviour and adds the browser, attempting both
regardless of either failing.

## The two judgment calls

**Invisible best-effort teardown on failing paths — right call.** Making it
visible would replace the original failure, which is worse. Named in both
docstrings and the runbook's residuals section, and — the part that matters
operationally — Step 5 tells the owner to confirm teardown by looking at their
own screen and filesystem.

**`__exit__` masking an in-flight `KeyboardInterrupt` — resolves cleanly, and
better than the builder argued.** Measured with an interrupt inside a `with`
block plus a browser-close failure carrying a path: the session raises
`presentation-session-teardown-failed`, the `KeyboardInterrupt` is chained and
visible in the printed traceback, and the path is not.

There is no inconsistency with the locator-confinement work. This `__context__`
is *provably* locator-free, because `close()` swallows the path-bearing
`OSError` in its own handler and constructs a fresh exception, so the only thing
that can occupy `__context__` on this path is the interrupt itself. The two
treatments differ because the two chains carry different things.

**Recorded as reasoning** because it currently holds by the structure of
`close()` rather than by an explicit invariant.

## Runbook changes

Step 5's interrupt subsection is correct, including that a missing `torn down`
line is expected rather than a failure, and it gives the *reason* teardown
matters — residue outliving the preflight's session-start guarantee — rather
than asserting tidiness. The closure claim now matches the code. The argv
warning is correctly framed as after-the-fact notification and explicitly
separated from the structural guarantees.

On **"if you see a traceback, do not read it and do not quote it"**: judged the
right instruction rather than an unfollowable one. The objection — that the
traceback is already on screen — misreads what is asked. It does not ask the
owner to unsee it; it asks them not to *study* it and not to transcribe it, both
of which remain available choices at the moment they matter.

## Named residuals

1. **One sentence overstated what the library guarantees.** The Step 3 bullet
   claimed teardown on every exit path "including Ctrl-C at the prompt... even a
   plain `close()`." Measured, the no-`with` case leaks both a live browser and
   a surviving session directory. Ctrl-C-at-the-prompt safety is a property of
   `with`; the library covers interrupts *during startup*, a different window.
   Not blocked, because the instruction that governs owner behaviour — Step 5's
   unconditional "confirm by looking" — survives regardless.
   **Closed by the foreman after this review**, as a one-sentence correction
   rather than a further build cycle; see the disposition note below.
2. **An irreducible Python race.** A signal landing between `launch` returning
   and the `viewing = ...` store leaves `viewing` as `None` with the browser
   owned by nobody. Not closeable without returning ownership from inside
   `launch`. Named so it is not rediscovered as a bug.
3. **The builder's three, confirmed honestly stated:** invisible teardown
   failure on failing paths; a genuine programming error during teardown
   reporting as `presentation-session-teardown-failed` rather than as itself;
   invocation discipline plus the `cd` history entry.
4. **The render/server-start classification remainder** — `live_session.py`
   catches only `PresentationSessionError` and `(OSError, RuntimeError)` there.
   Correctly described in the runbook as narrow, probably unreachable, and not
   demonstrated impossible.

## Disposition

**READY.** Residual 1 was corrected by the foreman directly after this review —
a one-sentence narrowing of the Step 3 bullet plus its heading, adopting the
reviewer's own suggested framing (the library covers interrupts during startup;
`with` is what covers the prompt). Recorded here rather than silently, because
it is a post-review edit to the reviewed artifact and no independent reader has
seen it. It changes no code and no vocabulary rule.

Track 1 is complete. Residuals 2–4 carry into Track 2 named.
