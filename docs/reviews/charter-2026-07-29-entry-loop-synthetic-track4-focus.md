# Charter — The Entry Loop (synthetic), Track 4: focus indicators, stated per control

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Against: `docs/reviews/2026-07-29-entry-loop-synthetic-track2e-aggregation.md` (cell FAIL)
- **No review gate.** The owner is cutting the milestone here; verification and a
  foreman inspection stand in for it. A re-score is **not** planned.

## The defect

Two independent evaluators, measuring from rendered colours, agreed: the
`#w2-box1` amount input has **no focus indicator**. Its computed focus style is
`outline-style: none, outline-width: 0px`, so what they measured — a cream
`rgb(255,253,248)` ring at **1.02:1** against the white field — is the control's
unchanged *resting* shadow, not a focus treatment. Required is 3:1.

This is the only defect keeping the W-2 cell off L2, and it has now failed the
accessibility row **twice**.

## Why it failed twice, which is the part that matters

Track 2c was chartered to fix focus contrast "against every background context the
surface can put them on" rather than patching the one literal that failed, and it
did that well. Buttons now carry a two-tone dark/light ring, and every button
focus state measured in the second evaluation has a component at 7.5:1 or better
across all region backgrounds.

The input was missed anyway. Not because a colour was wrong — because the model
was **indicator versus background**, and the rule that was missing is a different
shape:

> Every focusable control must have a focus indicator **distinct from its resting
> boundary**, with a component at 3:1 or better against the background adjacent
> to it.

The input has a strong resting boundary — 15.64:1 against its card — and nothing
layered on focus. Under a per-context model it looks handled. A control that never
enters the model cannot be caught by it.

**So state the rule per control, not per context.** That is the whole point of
this track, and it is what makes the fix survive a UI this project may well throw
away.

## What to build

1. **The rule, once.** A single focus treatment that applies to every focusable
   control, expressed so that adding a control later inherits it rather than
   needing to be remembered. Do not add a rule for `#w2-box1` specifically.
   Enumerate the focusable controls you found and confirm each one is covered —
   the wordmark link, `Enter this fact`, the amount input, the submit button in
   both its `Add` and `Update` states, `Correct this fact`, and `Review W-2 Box 1`.
   If there are others, say so; the count is part of the finding.

2. **Distinct from resting.** The indicator must be identifiable as a focus state,
   not merely present. Where a control already has a strong resting boundary, the
   focus treatment has to add something measurable on top of it. Say for each
   control what changes on focus and by how much.

3. **One durable check, not a battery.** The owner's standing direction is that
   this UI must not require a battery of validations per change, and that findings
   must survive future milestones. So do not add per-colour or per-element
   assertions. Add **one** test that enumerates the focusable controls from the
   rendered page and asserts the general invariant for each: the focus style
   differs from the resting style, and some component of the focus indicator
   measures at least 3:1 against its adjacent background, computed from rendered
   colours rather than compared to a stored snapshot.

   That test should keep passing when someone changes the palette, and start
   failing when someone adds a control without a focus indicator. If you cannot
   write it that way, say so and explain what forced the compromise rather than
   landing a snapshot test.

## What not to touch

- **Do not chase the `Review W-2 Box 1` outer ring.** One evaluator measured its
  dark outer component at 2.06:1 against the green completion region and listed it
  as needing change; the other treated the ring as passing because its light inner
  component measures 7.71:1. The foreman's resolution is that a two-tone indicator
  with one component clearing 3:1 against the region is a legitimate treatment, so
  this is an aesthetic edge and not a missing indicator. Leave it.
- Text contrast, control boundaries, landmarks, and keyboard behaviour all
  measured clean in the second evaluation. Do not revisit them.
- **Do not touch the criteria document.** Two evaluation rounds rest on it.
- Do not touch the field contract, the schema, the loader, or the derivation test.
  Track 3 is done and inspected.
- Do not score or re-score anything, and do not predict a verdict. **No maturity
  movement:** the cell verdict stays FAIL and the W-2 cell stays at L1. The
  milestone reports a failed evaluation as a real outcome. Repairing the defect
  after the fact does not move the cell, because nothing re-scored it.
- No second fact family, no real data, no residency locator, W-2 and synthetic
  throughout.
- Do not draft an ADR. ADR-0049 and ADR-0051 are the owner's at the close.

## Verification

This is a content-tree change, so the surface metadata must be regenerated:
`python3 -m tools.generate_entry_loop_t1_fixtures`, and the manifest, registry,
release, and adoption pins must all agree afterwards. Say what the byte total moved
to and that the change accounts for it.

The CI `verify` sequence, or a stated subset with each omission justified, plus the
data-safety scan and the commit you worked from — **in the commit message.** There
is no review gate here, so the commit message is the whole of what a later reader
gets. The last three rounds recorded this properly and all three reproduced when
re-run independently; hold that standard.

**Measure and report the numbers.** For every focusable control: the resting style,
the focus style, and the contrast ratio of the focus indicator against its adjacent
background, per background context the control can appear in. Before and after for
the input.

Orient with `python3 tools/foreman_context.py --ref HEAD --format markdown` and
`python3 tools/build_orientation_block.py --ref HEAD`. If either refuses, stop and
report it. No `.venv`; use system `python3`. Stand the surface up with
`python3 -m packages.derivation.runners.entry_loop_evaluation`.

## Report back

How the rule is expressed and why a control added next milestone inherits it; the
enumerated focusable controls and the measured numbers for each; what your one
invariant test asserts and how it would fail if someone added an unindicated
control; whether it survives a palette change; and the new starting-state
fingerprint, since the surface has changed and any future re-score must be against
that rather than `sha256:212e525d…`.
