# Review — Track 1: session runbook and non-descriptive failure vocabulary

- Verdict: **NOT READY**
- Unit: `docs/runbooks/presentation-real-session.md` (new, 365 lines) @ `748b8e8`
- Reviewed at: `50a9030` on `milestone/presentation-real-session-attestation-tracks`
- Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-27-presentation-real-session-attestation-track1-review.md`
- Independence: independent reviewer, not the foreman. The foreman wrote the
  milestone plan and the build charter that drew the vocabulary's governing
  mechanical-versus-evaluative distinction, so a foreman review could test the
  builder's execution of that line but not the line itself.

Verification run and clean: `test_presentation_live_session`,
`test_presentation_live_viewing_vehicle`, `test_presentation_l2_integration`,
both harness manifests, `envelope_scan.py --range main..HEAD`,
`git diff --check`. `tools/presentation_harness/lib/server.mjs` and both
evaluation manifests are byte-unchanged (`git diff --stat 26661e7..748b8e8`
shows only the new runbook file).

## Finding 1 (blocking) — the worked script does not deliver the classified reason codes the vocabulary depends on

The runbook's script catches only `PresentationSessionError`. But
`open_presentation_session` does not wrap a browser-launch-time failure; it
re-raises the original exception unchanged. Failures inside
`LiveViewingVehicle.launch()` raise `LiveViewingError`, a **sibling** class of
`PresentationSessionError`, not a subclass — verified by import.

Affected codes, all of which propagate as an uncaught Python traceback:
`viewing-browser-not-found`, `viewing-browser-launch-failed`,
`viewing-browser-start-timeout`, `viewing-browser-exited-during-launch`,
`viewing-path-not-confined`, `viewing-navigation-non-loopback`, and
`viewing-workspace-unreadable` — the last of which is not in the runbook's
reason-code table at all.

**The failure it produces.** The vocabulary assumes every failure surfaces as a
pre-classified, safe-to-report code. An uncaught traceback is exactly the
unclassified, alarming, on-screen text the vocabulary exists to stop the owner
from describing, and Part 2 offers no entry for it. In the one real,
unrepeatable session this is the scenario most likely to produce an improvised
— therefore illegal — description. Roughly a third of the runbook's own
reason-code table is affected.

## Finding 2 (blocking) — the locator recommendation and the worked example describe different mechanisms

Step 2 states the adopted mechanism is an interactive `input()` prompt at run
time, and the entire open-question essay analyzes `input()`'s properties (absent
from argv, absent from shell history, confined to process memory) as the basis
for the recommendation. The Step 3 script never prompts for the locator — it
computes `L = Path(__file__).resolve().parent`. The script's one `input()` call
is the teardown confirmation.

**The failure it produces.** Two failures. First, the residual analysis the
review charter asked to be tested — terminal echo, scrollback, session logging
of a typed value — analyzes a mechanism the artifact does not use. Second, the
mechanism actually used carries its own unanalyzed residual: it is safe only
when invoked as a bare `python3 view.py` from a terminal already positioned at
the residency. An owner who instead runs `python3 <L>/view.py` silently
reintroduces the full argv exposure the essay exists to avoid, and the runbook
never states that this invocation form is unsafe. An owner following Step 2's
promise will also be confused when no prompt appears — an instruction that is
unusable in the moment.

## Finding 3 (moderate) — "report that nothing fits" is close to a dead end

The runbook is honest that this is a named limit rather than a false
completeness claim, which is the right instinct. But when a real failure matches
nothing, the only legal report carries no shape information, and a repair must
then be authored without reference to what was seen. The project can detect that
something went wrong and stop trusting the session, but cannot diagnose or
repair the underlying defect from the report alone. A real defect can be
stranded indefinitely.

## Finding 4 (minor) — categorical safety claim for unenumerated reason codes was asserted, not audited

The vocabulary admits reporting any refusal reason code, including ones outside
its table, on the premise that a reason code is categorically safe. Tracing
`production_resolver.py`'s `Refusal` codes (`ADOPTION_AMBIGUOUS`,
`HARD_GATE_REFUSED`, and siblings) forward through
`presentation-live-run-refused`'s `reason_codes` shows they describe
package/governance validation state rather than taxpayer values, so the
conclusion holds — but it was reached without that audit. A soundness gap in the
reasoning, not a present crossing.

## Finding 5 (minor) — the section-count guidance is wrong about why it is safe

"Not every section rendered" is offered as the safe alternative to "nine
sections rendered." The real page's section set is nine lines, matching
`production-shaped.v1.json`, which is public in the repository — so the
alternative already conveys nearly the same bound. This leaks rendering
mechanics rather than tax values, so severity is low against ADR-0047
precondition 5's specific concerns, but it is a genuine instance of the
combination gate, and a rule that misstates its own basis teaches the wrong
test.

## Confirmed sound

- The reason-code table matches source for preflight-originated codes.
- The clipboard rule — no copy at all while retention is in force — is stated in
  Step 4 under "read this before you look at anything," ahead of any content
  viewing.
- `PreflightProbes` is presented unambiguously as an owner-supplied injected
  value, not an unimplemented feature.
- The clipboard preflight's partiality is presented as a named
  owner-responsibility remainder, never as a clearance.
- No locator, path fragment, canonicalized form, derived identifier, or absolute
  local path appears anywhere in the unit.

## Disposition

Findings 1 and 2 block. Both are concrete and verified rather than matters of
interpretation, and both make promises about the owner's in-the-moment
experience that the underlying code does not keep. Repair chartered at
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-27-presentation-real-session-attestation-track1-repair.md`.
