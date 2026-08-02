# Charter — Track 1 second repair: interrupt-path teardown and three accuracy corrections

- Role: **Builder** (`docs/roles/builder.md`), repair
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/presentation-real-session-attestation.md`
- Base: `milestone/presentation-real-session-attestation-tracks` @ `0f5e5dc`. Verify the SHA before starting.
- Recheck returning NOT READY: `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-27-presentation-real-session-attestation-track1-recheck.md`

## Context Capsule

- Source ref and resolved launch commit: `0f5e5dc`
- Exact object or commit range: `docs/runbooks/presentation-real-session.md`; `packages/derivation/live_session.py`; `packages/derivation/live_viewing.py`; `tests/test_presentation_live_session.py`
- Role: Builder (second repair)
- Scope and evidence-rung ceiling: the blocking finding, the two accuracy findings, and two of the named residuals. Nothing else.
- Stop conditions: any need to touch `tools/presentation_harness/lib/server.mjs` or either evaluation manifest; any need for a real workspace or a headed browser launch
- Full reads before acting: this charter; the recheck record; the repair diff you authored; `packages/derivation/live_viewing.py` around `launch` and `close`

## Blocking — the interrupt path, fixed structurally and not in the template

The reviewer demonstrated that Ctrl-C leaves an orphaned headed browser still
displaying the real return, plus a `.live-view/session-*` directory holding the
browser profile and the disk cache of that render. The preflight refuses on
backup inclusion and content indexing **at session start**; residue that
outlives the session outlives that guarantee.

The reviewer's suggested fix is a `try/finally` in the runbook's script
template. **Do not stop there.** That is the same fail-open drift this track has
now hit twice: a guarantee that lives only in a copyable example no-ops the
moment the owner retypes it, and the owner retyping it is not a hypothetical —
the runbook invites adaptation. The template is where the guarantee is
*demonstrated*, not where it lives.

Fix in three places, innermost first:

1. **`LiveViewingVehicle.launch`** — a `BaseException` escaping mid-launch must
   still `_stop_process(process)` and `_remove_session(destinations)` before
   propagating. Keep it propagating as itself; the code decision to leave
   `BaseException` unclassified stands and is correct.
2. **`open_presentation_session`'s `BaseException` branch** — tear down the
   browser and the session directory, not only the socket.
3. **The returned session object** — make it a **context manager**, so
   `with open_presentation_session(...) as session:` guarantees teardown on any
   exit path including an interrupt at a prompt inside the block. Keep `close()`
   working for existing callers. Then rewrite the template to use `with`, which
   makes the safe form also the natural form for an owner adapting it.

If you think the context-manager shape is wrong, say so with reasoning rather
than implementing something else — but the principle it serves is not
negotiable: teardown must not depend on the owner having copied a `finally`.

**Runbook.** Tell the owner what an interrupted session leaves behind, how to
confirm it is gone, and that an interrupt is the one case where Step 5's
"teardown confirmed by `close()` returning" does not apply. Add regression
coverage for the interrupt path — no orphaned process, no surviving session
directory, no listening socket.

## Accuracy — soften the closure claim

The runbook says the reason-code table is "closed for this call path." It is
not: `live_session.py:262-268` catches only `PresentationSessionError` and
`(OSError, RuntimeError)`, so a `ValueError`, `TypeError`, or `AttributeError`
from the render/server-start block escapes unclassified.

**Soften the claim to match the code. Do not widen the catch** — the runbook's
own next sentence already gives the owner a legal statement for exactly that
case, and an artifact that overstates its own completeness teaches the wrong
trust.

## Accuracy — the argv hazard is detectable

The runbook says the script "cannot detect or refuse" the
`python3 <L>/view.py` form. It can: `sys.argv[0]` is `"view.py"` for the safe
form and the full path for the hazardous one.

Refusal would not undo the exposure, which has already happened by then. But for
an unrepeatable session, telling the owner it happened is worth more than
nothing. Add the detection to the template as a warning, correct the prose, and
be explicit that this is a template convenience rather than a structural
guarantee — the same distinction the blocking finding is about.

## Residuals — close two of the four

- **`__context__` retention.** The wrapper's docstring implies total
  suppression; `__suppress_context__` alone does not deliver it, and the
  original `OSError.filename` still holds the path on the `__context__` object,
  reachable by any tool that walks it explicitly. Clear it, or correct the
  docstring to claim only what is true. Prefer clearing: the whole purpose is
  locator confinement.
- **`_close_quietly` swallowing a `shutdown()` failure**, after which
  `server_close()` never runs and the socket can survive silently. Pre-existing,
  but a surviving socket serving the real return is squarely this milestone's
  concern. Make `server_close()` run regardless.

Leave the other two — teardown diagnosability, and invocation discipline plus
the `cd` history entry — as named residuals. They are honestly named and not
closeable here.

## Hard constraints

Unchanged: no confinement code or probes, no real workspace, no headed browser
launch, `server.mjs` and both manifests byte-unchanged, no locator or absolute
local path anywhere, no new surfaces.

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

Report each item and what you did. Name any disagreement with the direction
above, especially on the context-manager shape. Name anything you could not
close.
