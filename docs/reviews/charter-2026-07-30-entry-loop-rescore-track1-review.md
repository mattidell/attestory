# Charter — Re-score the Entry Loop, Track 1 review

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-rescore.md`
- Build charter: `docs/reviews/charter-2026-07-30-entry-loop-rescore-track1.md`
- Under review: `track/entry-loop-rescore-track1` @ `b261aae`, base `main-ui` @ `8d903f6`
- Self-orient via the pickup protocol. Preserve fresh-reader independence.

## What this track was for

The usability criteria require every action to be reachable with Tab and
Shift+Tab and operable with its standard Enter or Space key. **No evaluation
has ever measured that.** Both Milestone 3 rounds scored the accessibility row
on colour contrast alone. This track exists to make the requirement checkable
*before* Milestone 4 re-scores the surface.

The stakes shape your review. This instrument is about to be used on a surface
we would like to pass, and the build reports that **every control passes and
nothing failed**. A probe that cannot fail produces exactly that result. Your
job is to establish that the checks are real.

## The specific risk

Milestone 3 rejected one track three times, every rejection the same shape:
machinery that asserted something untrue. A discriminator that did not
discriminate. Tests that never reached the code they guarded. An equality check
that could not be false.

The build reports finding **two false-negative bugs in its own probe**: CDP
`rawKeyDown` never triggers a control's native default action, so activation
checks were guaranteed to pass; and the submit button's synchronous
self-disable was being read as the observed effect, letting a stale fingerprint
bleed into the next control's reading. Both were fixed. That the builder found
these itself is a good sign — and it also establishes that this probe's failure
mode is silent false passes, which is why the remaining checks deserve
independent scrutiny rather than deference.

## What to verify

**Verify these against the code, not against the build's report of them.**

1. **Do the two demonstration tests actually demonstrate?** The build ships
   `test_reverse_traversal_check_bites_when_backward_reachability_breaks` and
   `test_activation_check_bites_when_a_control_swallows_its_key` as defect
   injections. Confirm each genuinely fails the check it targets, and that it
   fails *for the injected reason* rather than by breaking the probe or the
   page in some broader way. A demonstration that fails because the harness
   crashed proves nothing.

2. **Is the reverse-traversal check as strong as the charter asked for?** The
   charter said Shift+Tab must return "through the same set in reverse order."
   The probe collects the traversal sequence but `matches` compares only set
   membership — `forwardOnly` and `backwardOnly` are set differences.
   **Reverse order appears to be unverified.** Determine whether that gap is
   real, and if so whether set membership alone satisfies the criterion. State
   your reasoning either way; if order does not need checking, say why, because
   the next person will ask.

3. **Is backward traversal seeded honestly?** The probe reaches the last
   forward control with a programmatic `el.focus()` before Shift+Tabbing back.
   Consider whether a programmatically-focused starting point can mask a
   control that real Tab traversal would never have reached, or otherwise
   weakens the claim relative to a purely key-driven path.

4. **Can the activation fingerprint change for reasons unrelated to
   activation?** Activation is confirmed by a page-level fingerprint (URL,
   focused-control identity, status heading, "Accepted" flag, answered-fact
   count, error text). Focused-control identity is a component of that
   fingerprint, and key presses can move focus on their own. Establish whether
   any actionable control could register as activated purely because focus
   shifted or the page scrolled.

5. **Does `settle()` mask anything?** It waits for the submit button to
   re-enable before comparing. Consider whether it can wait past a *different*
   control's effect, or return early and reintroduce the bleed it was added to
   fix.

6. **Is the vacuous-pass property preserved?** The Track 4 `FocusIndicators`
   test guards against an empty finding set with a minimum count and a named
   control. Confirm the new checks cannot pass by reporting nothing — for
   traversal, for activation, and for the mouse-event count.

7. **Scope discipline.** Confirm `docs/phases/legible-entry/entry-usability-criteria.md`
   is untouched, no surface behaviour changed, and no defect was repaired
   rather than reported.

## Verification

Run `pytest` only to confirm a specific claim you are making. You may run the
new tests, and you may modify code locally to test whether a check bites —
do not commit such changes.

**Note a gap that is not the builder's fault and is not yours to fix.** The
`verify` workflow triggers only on pull requests to `main` and pushes to
`main`. This line works on `main-ui`, so **no CI has run on this branch, and
none ran on PR #112 or #115 either.** The build charter's done-criterion
"CI `verify` is green on the branch head" is currently unsatisfiable here. The
build reports running the full quartet locally with all green. Treat that as a
self-report — which `AGENTS.md` says is not a substitute for the check — and
confirm whatever you need to confirm directly. The governance gap is recorded
for the owner separately; do not attempt to fix the workflow in this review.

## Verdict

`READY` or `NOT READY`, per your seat file, with each finding stated as a
specific defect and a reason. If the checks are sound, say so plainly — the
correct outcome of this review may well be that a sharpened instrument found
nothing wrong with the surface, and that result is worth more if it survives
scrutiny than if it is waved through.
