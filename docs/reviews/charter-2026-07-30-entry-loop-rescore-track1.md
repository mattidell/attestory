# Charter — Re-score the Entry Loop, Track 1: make keyboard operability measurable

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-rescore.md`
- Branch: `track/entry-loop-rescore-track1` (from `main-ui` @ `5add975`)
- Review gate: **yes.** This track is reviewed before any evaluator is briefed.

## The gap

The usability criteria's accessibility row requires, among other things:

> every action must be reachable with Tab and Shift+Tab and operable with the
> control's standard Enter or Space key

**No evaluation has ever measured that.** Milestone 3 scored this row twice —
both times on colour contrast alone — and closed carrying the finding that the
harness *cannot* measure keyboard operability. The row failed twice on a
measurable colour defect, which is the only reason the unmeasured half never
mattered. Now the colour defect is repaired, and Milestone 4 is about to
re-score the row. If it comes back Pass on the same harness, that Pass asserts
a requirement nothing checked.

Your job is to make it checkable, before anyone scores it.

**Understand what this means for the outcome.** You are sharpening an
instrument immediately before it is used on a surface we would like to pass.
Your work can only make that row harder to clear. If the surface fails the
checks you add, that is the track succeeding, not failing — you will have found
a real defect two rounds of evaluation were structurally unable to see. **Do
not soften a check because the surface fails it.** Report the failure; the
repair is a separate decision that is not yours or mine to make here.

## What already exists

Most of the machinery is there. Read it before designing anything:

- `tests/helpers/entry_loop_focus_indicator_client.mjs` — a real CDP client
  that already drives `Input.dispatchKeyEvent`, already has `pressTab(shift)`
  including the shift variant, and already enumerates every control reachable
  by Tab from the compiled, browser-rendered page in both the incomplete and
  the complete states.
- `tests/test_entry_loop_t1.py`, class `FocusIndicators` — the Track 4 test
  that consumes it. Note its **vacuous-pass guard**: it asserts at least six
  findings and that `w2-box1` is among them, precisely so a broken probe
  reports an empty list and fails rather than trivially passing. Preserve that
  property in whatever you add.

Prefer extending this path over building a second one. Two probes that both
drive the page is a maintenance seam and a source of disagreement about which
is authoritative.

## What to build

1. **Reverse traversal.** Shift+Tab from the last focusable control returns
   through the same set in reverse order. No control may be reachable forward
   but not backward. Report the forward set and the backward set; if they
   differ, that difference is the finding.

2. **Activation by observed effect.** Every actionable control activates with
   its standard key — Enter or Space as appropriate to the control type — and
   activation is confirmed by an **observed system effect**: the state the
   surface actually reaches, or the contribution the admission path actually
   receives. A button that silently swallows Enter must fail this check. The
   absence of an exception is not evidence of activation.

3. **No mouse.** The traversal and activation path completes without
   synthesising a pointer event. If any step of the entry loop can only be
   completed by clicking, say so — that is a finding about the surface, and
   it is exactly the kind of thing this track exists to surface.

4. **One durable rule, not a list of controls.** Same standing direction as
   Track 4: express the check so that a control added later is covered by
   being reachable, rather than by someone remembering to add it. Do not
   hard-code the current control set as the definition of correct.

## The trap, named explicitly

Milestone 3 rejected one track **three times**, every rejection the same
shape: the build added machinery that asserted something that was not true. A
format discriminator that did not discriminate. Tests that never reached the
code they claimed to guard, because a fixture marker mismatched the parser, so
every case failed at parse time and would have kept "passing" with validation
deleted outright. An equality check that could not be false.

A keyboard probe is unusually prone to this. `dispatchKeyEvent` followed by
"no exception was raised" is a check that cannot fail. So:

**Every assertion you add must be demonstrated to bite.** For each one:
disable the behaviour it guards, confirm the check fails, restore the
behaviour, confirm it passes. Record what you disabled and what you observed.
That demonstration is part of the deliverable, not a courtesy — a check whose
failure mode you have not personally observed is not evidence of anything.

All three Milestone 3 rejections closed by **subtracting** — deleting a false
claim or an inert mechanism — not by adding a layer to compensate. If you find
yourself adding something to make a claim true, consider whether the honest
move is to narrow the claim instead.

## Not in this track

- **Do not touch `docs/phases/legible-entry/entry-usability-criteria.md`.** It
  is read-only for this entire milestone. If you believe a criterion is wrong
  or unmeasurable as written, say so in your report and implement it as
  written.
- Do not repair any surface defect your new checks expose. Report it.
- Do not unbundle the accessibility criterion, or change how anything is
  scored.
- No change to the entry surface's behaviour, the derivation packages, or any
  tax rule.
- No real data. Synthetic workspace only, per `AGENTS.md#Data Safety Rules`
  and `AGENTS.md#Fixture Rules`.

## Verification

Full CI `verify` sequence, no omissions: `pytest -n auto`, `-m mypy`,
`governance_lint`, `envelope_scan`.

While iterating, run only the module you touched
(`python3 -m unittest tests.test_entry_loop_t1`). Run the full suite once
before you report. Do not re-run a deterministic result to confirm it.

The new checks need Node, a local Chrome/Chromium, and the vendored surface
tree — the same `skipUnless` conditions as `FocusIndicators`. **If those
conditions are not met in your environment, say so plainly in your report.**
A skipped test reported as a pass is the exact failure this milestone exists
to prevent.

## Done when

1. Reverse traversal, activation by observed effect, and the no-mouse path are
   all mechanically checked against the real compiled surface.
2. Every new assertion has been demonstrated to fail when the behaviour it
   guards is removed, with what you disabled and what you observed recorded.
3. The vacuous-pass guard property is preserved: a broken probe fails rather
   than reporting an empty finding set.
4. CI `verify` is green on the branch head.
5. Your report states what the surface actually does under keyboard-only
   operation — including any control that fails, which is a legitimate and
   useful result.
