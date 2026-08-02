# Charter — The Entry Loop (synthetic), Track 2e: Evaluator D (Reviewer brief)

- Role: **Evaluator D**, the Reviewer brief
  (`docs/phases/legible-entry/entry-usability-criteria.md`, Scoring Procedure)
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Criteria: `docs/phases/legible-entry/entry-usability-criteria.md` (owner-accepted, do not amend)
- Evidence pack: `docs/phases/legible-entry/entry-loop-synthetic-evidence-pack.md`
- File your scores to: `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-29-entry-loop-synthetic-track2e-evaluator-d.md`

## Why this is a partial re-score

The surface was scored once already. Most rows passed unanimously; the cell
failed, repairs landed, and this run re-scores **only the rows those repairs
could have moved**. The rest stand as filed.

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

**Do not score the other fourteen rows.** If you see something wrong in one of
them, do not score it — record it at the end as a note, and say which row it
would have touched.

**Pass or Fail. No third value.** If you want to write "partial", that is a Pass
or a Fail with a rationale, and you have to pick.

Score from the criteria document's own wording rather than your own sense of
what is reasonable. 2.2 states its own minimum bar: a bare "required" label
does not pass, and field-attached text must name the immediate return
destination and the completion purpose.

## Your brief

Approach this surface **without implementation context.** Work the field using
only the surface's own guidance, and record every point at which the surface
required you to infer something it did not tell you.

You are standing in for a person who has a W-2 in front of them and has never
seen this system. That person cannot read the source, cannot check the act log,
and cannot ask the builder what a field means. Neither can you.

**Do not read any of the following**, at any point, for any reason:

- `packages/derivation/entry_loop.py`, or anything else under `packages/`;
- the Svelte source or the format declaration under
  `packages/sample_data/entry_loop_t1/`;
- `tests/test_entry_loop_t1.py` or any test;
- any charter, review, build report, or aggregation record for any track of
  this milestone — including the first run's evaluator files;
- the milestone plan or `docs/phase-state.md`.

If you find yourself reaching for one of those to resolve a question, **that is
the finding.** Record the question you could not answer from the surface, and
score accordingly.

You need exactly two documents: the criteria and the evidence pack. Read them,
then go to the page.

## Criterion 2.3, specifically

This row turns on what a person can state **without guessing** before typing.

Read the criterion's own wording carefully and hold it as written. It asks what
a person *can* state, not what the surface *must* exhaustively document. Score
what you could actually determine from the field's own guidance before you
typed anything — and record, separately, what happened when you typed.

If the guidance and the behaviour disagree, say so plainly in your rationale and
score the criterion as written. Do not silently fold a behaviour complaint into
a guidance score, and do not fold a guidance complaint into a behaviour score.
Which of the two you observed is the useful part of your file.

Your brief gives you unique standing here: you are the one who genuinely cannot
cheat on a "without guessing" bar. Be honest about where you guessed.

## The accessibility row, specifically

It bundles five requirements: text contrast at 4.5:1, non-text contrast at 3:1
for **visible control boundaries and focus indicators**, a `main` landmark and a
named form landmark, Tab/Shift+Tab reachability with standard-key operability,
and focus visibility through `:focus-visible`.

Measure focus indicators and control boundaries in **every background context
the surface can put them on**, including any state the page reaches only after
you have entered something. Enumerate the contexts you found.

These are measurements, not impressions. Compute contrast ratios from rendered
colours; check landmarks and focus by operating the page with the keyboard. If
you cannot measure something, say so rather than guessing in either direction.

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

A second evaluator is scoring the same six rows under a different brief. **Do
not read their file, look for it, or wait for it.** If it exists on disk when
you run, do not open it. Where the two of you disagree, that disagreement is
signal the procedure preserves on purpose; a consensus reached by reading each
other's answers destroys the only thing this design buys.

## Boundaries

- **Score. Do not fix.** Not the surface, not a test, not a typo.
- Do not amend the criteria. They are owner-accepted at `1e48443`. If one seems
  unscoreable as written, score it anyway, and say so separately as a note to
  the owner.
- Do not aggregate, do not predict the cell verdict, do not compare yourself to
  the other evaluator.
- No maturity claim. Nothing moves on any matrix.

## What to file

Use the evidence pack's transcript and score-sheet shapes, cut to six rows.

- Your raw transcript: the starting-state fingerprint, then every action and
  observation in order, **including the attempts that did not work**.
- The six-row score sheet: Pass or Fail, with a transcript reference and a
  rationale for each.
- Your contrast measurements as numbers, per element per background context.
- **A list of every point where the surface required inference** — where you had
  to guess, assume, or reason from outside knowledge to keep going. This is the
  part of your file the other evaluator structurally cannot produce, and it is
  the most valuable thing you file.
- For anything you scored Fail: what specifically would have made it a Pass.
- At the end, separately: anything you could not measure, any row you found
  ambiguous, and any observation that would have touched one of the fourteen
  rows you were told not to score.

Orient with `python3 tools/build_orientation_block.py --ref HEAD`. No `.venv`;
use system `python3`. Commit your file on this branch.
