# Recheck — Track 1 repair

- Verdict: **NOT READY** — one blocking finding, narrow and cheap to close
- Reviewed at: `0f5e5dc`; repair under review `894ff23`; diff `748b8e8..894ff23`
- Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-27-presentation-real-session-attestation-track1-recheck.md`
- Reviewer: the original independent reviewer, holding its own prior findings

Verification passes: 51 tests OK, both harness manifests clean, `envelope_scan`
and `git diff --check` silent, `tools/presentation_harness/lib/server.mjs` and
both evaluation manifests byte-unchanged against `main`.

## The five prior findings — all closed

All five close the **failure named**, not merely the sentence written.

**Finding 1 — the class is now empty for the launch path, verified rather than
read.** `_classified_viewing_failure` forwards `failure.reason.value`. Every
`raise LiveViewingError(...)` site in `live_viewing.py` (lines 187–465) passes a
`ViewingReason` enum member, so `.reason.value` is structurally always a fixed
authored string with no interpolation — the guarantee holds by construction, not
by intent. `LiveViewingError.__dict__` carries only `{'reason': <enum>}`: no
message, path, or argument rides along. The unclassified branch was exercised
with `OSError(2, "No such file", "<a path>")` and confirmed to produce
`__cause__ is None`, `__suppress_context__ is True`, and a printed traceback
containing no trace of the path.

**Findings 2–5** are properly closed. Finding 5's reframing — *never state a
count over a set whose size is not already fixed and public in the repository* —
is better than the reviewer's own original version and is accepted, including
the concession that "nine sections rendered" is legal-but-pointless.

## The two changes beyond the charter

**Teardown broadening: correct, swallows nothing.** `except Exception` on both
closes converts rather than suppresses; `teardown_failed` is set and
`presentation-session-teardown-failed` is always raised. Both closes are
attempted regardless of the first failing, which is the right ordering.
`BaseException` is correctly still not caught. Cost: a genuine programming error
in teardown now surfaces as "teardown did not complete" rather than a traceback.
Right trade for this artifact; named as a residual.

**`BaseException` left unclassified: reasoning right, consequence not covered.**
Turning Ctrl-C into a refusal code would be a lie inside the vocabulary and the
code decision should stand. But the socket and browser are **not** torn down on
that path. Demonstrated empirically: after an interrupt, the residency
`.live-view` survives, a `session-*` directory remains, and the browser process
is still alive.

`LiveViewingVehicle.launch` (`live_viewing.py:434-449`) catches only
`LiveViewingError` and `(OSError, subprocess.SubprocessError, TypeError)`, so a
`KeyboardInterrupt` escapes without `_stop_process(process)` and without
`_remove_session(destinations)`. `open_presentation_session`'s
`except BaseException` branch then calls `_close_quietly(server)` — the socket
only.

## Blocking finding — the interrupt path leaves residency residue with no runbook coverage

The likely real case is not an interrupt during launch but **Ctrl-C at the
template's blocking `input()` prompt**. Then `session.close()` never runs, and
the owner is left with an orphaned headed browser — launched
`start_new_session=True` — still displaying the real return, and a
`.live-view/session-*` directory persisting inside the residency holding the
browser profile and the disk cache of the rendered real return.

**The failure this produces** is not a boundary crossing: everything left behind
is inside the residency, which is where it belongs. It is an **instruction that
is unusable in the moment**, with a durable tail:

- Ctrl-C is the most common reflex for ending a blocking terminal program, and
  the template presents a bare blocking prompt that invites it.
- Step 5 tells the owner teardown is confirmed by `close()` returning. The
  interrupt path is the one case where that confirmation never happens, and the
  runbook says nothing about it — so the owner improvises, which is the exact
  failure mode the artifact exists to prevent.
- Normal teardown removing `.live-view/session-*` is what keeps the residency
  from accumulating a cached copy of the rendered return. The interrupt path
  silently skips it. The preflight refuses on backup inclusion and content
  indexing **at session start**; nothing binds the machine afterwards, so
  residue that outlives the session outlives that guarantee too.
- No test covers this path. The four new regression tests are otherwise good —
  they assert the guarantee rather than the implementation.

## Non-blocking accuracy findings

**The runbook overclaims closure.** It states the table is "closed for this call
path." Not quite: the render/server-start block (`live_session.py:262-268`)
catches only `PresentationSessionError` and `(OSError, RuntimeError)`, so a
`ValueError`, `TypeError`, or `AttributeError` originating there would still
escape unclassified. Much narrower than the originally-named class and probably
unreachable in practice, and materially softened by the runbook's own next
sentence, which gives the owner a legal statement for exactly that case. Soften
the claim to match the code rather than widening the catch.

**"The script cannot detect or refuse it" is not accurate.** Of the
`python3 <L>/view.py` hazard. The derivation does give the same answer either
way, but `sys.argv[0]` does not — it is `"view.py"` for the safe form and the
full path for the hazardous one, so detection is trivial. Refusing would not
undo the argv and history exposure, which has already happened; but for an
unrepeatable session, telling the owner it happened is worth more than nothing.
The runbook asserts an impossibility that is only an unattractiveness.

## Residuals to carry forward

- **`__context__` is retained** on the classified exception; only
  `__suppress_context__` is set. The original `OSError`'s `.filename` still
  holds the path on the `__context__` object. Standard traceback printing does
  not show it, but any REPL, debugger, or reporting tool that walks `__context__`
  explicitly can surface it. Not the total suppression the wrapper's docstring
  implies.
- **`_close_quietly` swallows a `_PresentationServer.close()` failure**; if
  `shutdown()` raises, `server_close()` never runs and the socket can survive,
  silently. Pre-existing, unchanged by this repair.
- Teardown diagnosability, per above.
- Invocation discipline and the `cd` history entry, as the builder named.
