# Charter — Track 1 repair: runbook findings 1–5

- Role: **Builder** (`docs/roles/builder.md`), repair
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/presentation-real-session-attestation.md`
- Base: `milestone/presentation-real-session-attestation-tracks` @ `50a9030`. Verify the SHA before starting.
- Review returning NOT READY: `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-27-presentation-real-session-attestation-track1-review.md`

## Context Capsule

- Source ref and resolved launch commit: `50a9030` on `milestone/presentation-real-session-attestation-tracks`
- Exact object or commit range: `docs/runbooks/presentation-real-session.md`; `packages/derivation/live_session.py` and `tests/test_presentation_live_session.py` for finding 1
- Role: Builder (repair)
- Scope and evidence-rung ceiling: repair the five filed findings and nothing else. No new capability, no new surface.
- Stop conditions: any need to touch `tools/presentation_harness/lib/server.mjs` or either evaluation manifest; any need for a real workspace or a headed browser launch
- Full reads before acting: this charter; the review; the original build charter; the unit under review; `packages/derivation/live_session.py`; `packages/derivation/live_viewing.py`

## Finding 1 — fix in code, not in the template

`LiveViewingError` is not a subclass of `PresentationSessionError`, so browser-,
confinement-, and workspace-originated refusals propagate as uncaught
tracebacks. Roughly a third of the runbook's own reason-code table is affected,
including `viewing-workspace-unreadable`, which the table omits entirely.

**Wrap at the source in `open_presentation_session`, do not merely widen the
catch clause in the runbook's template.** The template is an example the owner
may retype or adapt; a guarantee that lives only in an example silently no-ops
the moment they do. This project has now named that fail-open drift class three
times — ADR-0047's sharpest residual, the rejected string-substitution fix for
the synthetic-label finding, and here — and the fix belongs where every caller
gets it.

The reason-code guarantee is what the entire vocabulary rests on: every failure
reaching the owner must arrive pre-classified. Make that true of the function,
add regression coverage that a viewing-originated failure surfaces as a
classified refusal rather than a raw exception, and add the missing table entry.

The scriptability-repair scope the original charter bounded is hereby spent on
this. It is justified by the sitting: without it, the owner's most likely
in-the-moment failure is an unclassified traceback, which is precisely the text
the vocabulary cannot describe.

## Finding 2 — make the prose and the mechanism agree

Step 2 promises an interactive `input()` prompt; the script derives the locator
from `Path(__file__).resolve().parent`. The open-question essay then analyzes
the safety properties of a mechanism the artifact does not use.

Pick one and make everything agree. The foreman's view, which you may overturn
with reasoning: **the implemented mechanism is the better one** — deriving the
locator from the script's own position keeps it out of argv, out of history, and
out of terminal echo and scrollback, which is strictly better than a typed
prompt. If you keep it, rewrite the essay to analyze *that* mechanism honestly,
including the residual the reviewer identified and you did not: an owner who
invokes `python3 <L>/view.py` instead of a bare `python3 view.py` from a
terminal already at the residency reintroduces the full argv exposure.

**State the "never invoke with a path argument" rule explicitly and where it will
be read.** A safety property that holds only for one unstated invocation form is
not a safety property yet.

## Finding 3 — give the escape hatch a real path

"Report that nothing fits" currently strands a novel failure: detectable, not
diagnosable.

There is an escape hatch the runbook has not noticed, and it is already in the
milestone's structure. **A failure that matches nothing may be reproduced
against a synthetic workspace, where description is fully legal.** Track 2 exists
precisely to make that path routine. Add it: when nothing fits, the owner's
legal move is to attempt reproduction synthetically and then describe it
without restriction, because a synthetic failure is not the owner's data.

Be honest that this does not cover failures which only manifest against real
content — say so rather than implying the hatch is total.

## Finding 4 — scope the categorical claim to what you audited

The vocabulary admits any refusal reason code on the premise that a reason code
is categorically safe. The reviewer traced `production_resolver.py`'s `Refusal`
codes forward and found the conclusion holds, but the claim was made without the
audit.

Either state the basis, or narrow the claim to the codes actually audited and say
that an unenumerated code should be reported as an unenumerated code rather than
assumed safe.

## Finding 5 — correct the section-count guidance

"Not every section rendered" was offered as the safe alternative to a bare count,
but the real page's section set is public in the repository fixture, so the
alternative conveys nearly the same bound. Severity is low — this leaks rendering
mechanics, not tax values — but the guidance as written is wrong about its own
safety, and a rule that misstates why it is safe teaches the wrong test.

Fix the guidance and the reasoning attached to it.

## Hard constraints

Unchanged from the original build charter: no confinement code or probes, no
real workspace, no headed browser launch, `server.mjs` and both manifests
byte-unchanged, no locator or absolute local path anywhere, no new surfaces.

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

Report each finding and what you did about it. Where you disagreed with the
foreman's direction, say so and give the reasoning — finding 2's mechanism
choice is explicitly open to being overturned. Name anything you could not close.
