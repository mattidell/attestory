# Track 2e aggregation — The Entry Loop (synthetic), partial re-score

- Aggregated by: **Foreman**, 2026-07-29
- Procedure: `docs/phases/legible-entry/entry-usability-criteria.md`, Scoring Procedure
- Evaluator C (Builder brief): `docs/reviews/2026-07-29-entry-loop-synthetic-track2e-evaluator-c.md` (`10a98df`)
- Evaluator D (Reviewer brief): `docs/reviews/2026-07-29-entry-loop-synthetic-track2e-evaluator-d.md` (`18cb167`)
- Starting-state fingerprint, both runs: `sha256:212e525dd6d29292cd4c692c72ba15b7e03a74fa2e6c17f3c46bae0aebe5c5a5`
- Prior run: `docs/reviews/2026-07-29-entry-loop-synthetic-track2-aggregation.md`

Both evaluators ran against the same fingerprint, which differs from the first
run's `sha256:7d5abe2e…`. The surface under evaluation is genuinely the repaired
one.

## Cell verdict: **FAIL**

The W-2 column of the entry-loop matrix does not move to L2.

| Row | C | D | Aggregate | Effect |
| --- | --- | --- | --- | --- |
| 2.1 — names source document and box (mechanical) | Pass | Pass | Pass | — |
| 2.2 — states purpose and return destination (mechanical) | Pass | Pass | Pass | — |
| 2.3 — format stateable without guessing (judgement) | Pass | Pass | Pass | — |
| Carries over: Accessibility baseline (mechanical) | **Fail** | **Fail** | **Fail/Fail** | **Fails the cell** (rule 3) |
| Carries over: Fail-loud (mechanical) | Pass | Pass | Pass | — |
| Carries over: Blanket redaction (mechanical) | Pass | Pass | Pass | — |

The fourteen rows outside this partial re-score stand as filed in the first run.

## What the repairs did close

**The format work is done, and it is no longer contested.** Criterion 2.3 was
the escalated judgement dispute of the first run; it is now Pass under both
briefs, including the reviewer brief that structurally cannot cheat on a
"without guessing" bar. Evaluator D read the guidance before typing, recorded
the accepted syntax from the field itself — dollars and cents, optional comma
grouping, optional `$` prefix, with examples — and separately confirmed the
validation behaviour was consistent with that guidance.

That is the guidance/behaviour congruence the owner identified as the real
defect behind the first run's dispute. It was fixed at the level the owner asked
for: one declaration governing hint, error, and validator.

Fail-loud and blanket redaction, added to this re-score because Tracks 2c and 2d
changed the refusal path, both hold. A malformed value produces a visible
`role=alert`, the rejected string does not reach the error text, and Evaluator C
confirmed at the system boundary that no contribution was admitted.

## What still fails, and why it failed twice

One defect, agreed by both evaluators from rendered colours: **the amount input
has no focus-specific indicator.** Its `:focus-visible` rendering is a cream
`rgb(255,253,248)` ring against a white `rgb(255,255,255)` field — **1.02:1**
against a required 3:1. C additionally recorded that the input's computed focus
style is `outline-style:none, outline-width:0px`, so what is being measured is
the control's unchanged resting shadow rather than a focus treatment at all.

**This is the same measurement, on the same element, that failed the first run.**
Track 2c was chartered to fix contrast "against every background context the
surface can put them on" rather than patching the one literal that failed, and
it did that well for buttons: the focus ring is now a two-tone dark/light
treatment holding across the region backgrounds, and every button focus state
measured in this run has a component at or above 7.5:1.

The input was missed anyway, and the reason is worth stating precisely, because
it is not a missed hex value. The repair modelled *how a focus ring should
contrast against the region behind it*. It did not establish that *every
focusable control must have a focus indicator distinct from its resting
boundary*. The input has a strong resting boundary — 15.64:1 against its card —
and no focus treatment layered on top, so it reads as handled until someone
measures the focus state specifically. A context-and-colour model cannot catch a
control that never enters the model.

That is a modelling gap, not a workmanship one, and it is direct evidence for
the standing owner directive that these findings must be carried by schema
rather than by accumulated checks. It is recorded here for Track 3.

## One measurement the two evaluators read differently

The `Review W-2 Box 1` focus ring in the dark-green completion region is a
two-tone indicator. Both measured both components and got the same numbers:

- inner light `#fffdf8` against `#075e4f` — **7.71:1**
- outer dark `#17251f` against `#075e4f` — C recorded **1.00:1**, D **2.06:1**

They differ on what that means. C treated the ring as passing because one
component contrasts sufficiently and named that reasoning explicitly. D scored
the outer component against the 3:1 bar on its own and listed it among what
would have to change.

Both scored the row Fail regardless, on the input, so this does not affect the
verdict. It is recorded because a repair charter must not silently pick a side:
a two-tone indicator whose light component clears 3:1 against the region is a
legitimate treatment, and the foreman's reading is that C is right on this
element. The outer dark ring is an aesthetic edge against dark green, not a
missing indicator, and the correct repair scope is the input alone.

## Unmeasured in both runs: the keyboard sub-requirements

Neither evaluator could measure Tab/Shift+Tab traversal or Enter/Space
activation. Both attempted it repeatedly through more than one browser interface,
both found focus did not advance and key presses did not activate controls while
clicking the same controls did, and **both declined to score that as a surface
failure** because they could not separate the surface from their own tooling.
That judgement was correct under both briefs.

The foreman resolved it at the source level, which no evaluator was permitted to
do. Every control in `EntryPage.svelte` is a native `<button type="button">`
with an `on:click` handler, plus a native `type="submit"` inside the form, an
`<a>`, and an `<input>`. Native buttons dispatch click on Enter and Space, and
native focus order provides Tab traversal. The keyboard sub-requirements are
almost certainly met, by construction.

**"Almost certainly" is not a measurement, and that is the finding.** The
accessibility criterion asserts a requirement the evaluation harness cannot
currently exercise. Two independent evaluators hitting the same wall makes this a
documented capability gap rather than an evaluator limitation, and it means part
of a mechanical criterion has now gone unverified in two consecutive runs. It
belongs to the instrument, not to the surface.

## Process defect in this run, foreman's own

Both evaluators reported that `tools/foreman_context.py` refused to render,
because the foreman set `milestone_state` to `track-2e` and
`tools/foreman_context.py:206` accepts only `track-<digits>`. Both ran the
evaluation with no orientation block, and both correctly declined to infer scope
from the failure and continued under their charters.

The sub-unit letter belongs in the prose fields, not the machine-readable track
number. Corrected to `track-2`. No evidence in either file appears to have been
affected, but the foreman broke a tool the roles depend on and the record should
say so plainly.

## What would close the cell

One repair, narrower than the first round's:

1. Give the amount input a focus indicator distinct from its resting boundary,
   with a component at 3:1 or better against the field it sits in — and
   establish it in a way that covers every focusable control rather than that
   one input.

Then re-score the accessibility row only. The other five rows in this partial
re-score are unanimous Pass and do not need re-running.

## Notes for Track 3

Three findings about the instrument, none of which amend it for this evaluation:

1. **Focus indicators need to be declared per focusable control, not per
   background context.** This row has now failed twice on the same element for
   this reason.
2. **The harness cannot measure keyboard traversal or activation**, so a
   mechanical criterion is partly unverifiable as the evaluation is currently
   run.
3. Carried from the first run: the accessibility row bundles five requirements
   into one Pass/Fail, so a single narrow miss sinks a row that is otherwise
   comfortably met; and the criteria conflate knowledge sufficiency (judgement)
   with guidance/behaviour congruence (mechanical).
