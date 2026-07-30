# Charter — The Entry Loop (synthetic), Track 2e: Evaluator C (Builder brief)

- Role: **Evaluator C**, the Builder brief
  (`docs/phases/legible-entry/entry-usability-criteria.md`, Scoring Procedure)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Criteria: `docs/phases/legible-entry/entry-usability-criteria.md` (owner-accepted, do not amend)
- Evidence pack: `docs/phases/legible-entry/entry-loop-synthetic-evidence-pack.md`
- File your scores to: `docs/reviews/2026-07-29-entry-loop-synthetic-track2e-evaluator-c.md`

## Why this is a partial re-score

The surface was scored once already. Eighteen of twenty rows passed
unanimously; the cell failed on the accessibility row and one judgement row was
escalated to the owner. Repairs then landed. This run re-scores **only the rows
those repairs could have moved**, and leaves the other fourteen standing as
filed.

You are a fresh evaluator. The two who scored the first run now know the
surface too well to score it again.

## What you score — six rows, and only these six

| Row | Type |
| --- | --- |
| 2.1 — field names source document and exact box | Mechanical |
| 2.2 — field states why the fact is asked for and its return destination | Mechanical |
| 2.3 — a person can state the accepted format without guessing | Judgement |
| Carries over: Accessibility baseline | Mechanical |
| Carries over: Fail-loud | Mechanical |
| Carries over: Blanket redaction | Mechanical |

The first four are the rows the aggregation named. The last two are added here
because the repairs changed how the field refuses input and what the rejection
message says, which is exactly the behaviour those two rules govern. Scoring
them off the older list would leave changed behaviour unscored.

**Do not score the other fourteen rows.** Not to confirm them, not in passing.
If you see something that looks wrong in one of them, do not score it — record
it at the end as a note, and say which row it would have touched.

**Pass or Fail. No third value.** Aggregation happens later and is not yours to
anticipate. If you want to write "partial", that is a Pass or a Fail with a
rationale, and you have to pick.

Score from the criteria document's own wording. Do not sharpen it or soften it.
2.2 states its own minimum bar: a bare "required" label does not pass, and
field-attached text must name the immediate return destination and the
completion purpose.

## Your brief

Exercise every criterion you score as an explicit system outcome, and preserve
the action/result transcript.

You are the evaluator allowed to check that what the surface *showed* you is
what actually *happened*. Where a row is about behaviour — a value was
accepted, a value was refused, nothing was echoed back — do not take the page's
word for it. Confirm it at the system level as well, and record both: what the
surface displayed, and what you independently observed.

That is your whole advantage over the other evaluator, and the reason two
briefs exist rather than one.

## The accessibility row, specifically

This is the row that failed the cell, so it gets the most spend.

It bundles five requirements: text contrast at 4.5:1, non-text contrast at 3:1
for **visible control boundaries and focus indicators**, a `main` landmark and
a named form landmark, Tab/Shift+Tab reachability with standard-key
operability, and focus visibility through `:focus-visible`.

The first run's two failures were both non-text contrast, and both were found
only because one evaluator measured in a place the other did not: a focus ring
against the dark-green completion region, and the input's own boundary against
the card behind it. **Measure focus indicators and control boundaries in every
background context the surface can put them on**, not just the one you land in
first. Enumerate the contexts you found and say how many there are.

These are measurements, not impressions. Compute contrast ratios from actual
rendered colours. Check landmarks and focus by operating the page with the
keyboard. If you cannot measure something, say so in the rationale rather than
guessing in either direction.

## Running it

```sh
python3 -m packages.derivation.runners.entry_loop_evaluation
```

It prints the URL, the W-2 Box 1 figure to enter, the corrected figure, and a
starting-state fingerprint. **Record that fingerprint in your transcript.** Stop
with Ctrl-C; a clean restart is the same command again.

Everything here is synthetic. There is no real data anywhere in this
evaluation.

## Independence

A second evaluator is scoring the same six rows under a different brief.
**Do not read their file, look for it, or wait for it.** If it exists on disk
when you run, do not open it.

Also do not read the first run's evaluator files
(`…track2-evaluator-a.md`, `…track2-evaluator-b.md`) or the aggregation record
(`…track2-aggregation.md`). They contain the previous scores and the specific
defects that were repaired. Reading them would tell you where to look and what
answer to expect, and this run exists precisely to get an answer that was not
told to you in advance.

## Boundaries

- **Score. Do not fix.** Not the surface, not a test, not a typo. If something
  is broken, that is a score and a rationale.
- Do not amend the criteria. They are owner-accepted at `1e48443`. If a
  criterion seems unscoreable as written, score it anyway, and say so
  separately as a note to the owner.
- Do not aggregate, do not predict the cell verdict, do not compare yourself to
  the other evaluator.
- No maturity claim. Nothing moves on any matrix.

## What to file

Use the evidence pack's transcript and score-sheet shapes, cut to six rows.

- Your raw transcript: the starting-state fingerprint, then every action and
  observation in order. Enough that someone could repeat your run and get your
  scores.
- The six-row score sheet: Pass or Fail, with a transcript reference and a
  rationale for each.
- Your contrast measurements as numbers, per element per background context.
- For anything you scored Fail: what specifically would have made it a Pass.
- At the end, separately: anything you could not measure, any row you found
  ambiguous, and any observation that would have touched one of the fourteen
  rows you were told not to score.

Orient with `python3 tools/build_orientation_block.py --ref HEAD`. No `.venv`;
use system `python3`. Commit your file on this branch.
