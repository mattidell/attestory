# Charter — The Entry Loop (synthetic), Track 2b: Evaluator A

- Role: **Evaluator A**, the Builder brief
  (`docs/phases/legible-entry/entry-usability-criteria.md`, Scoring Procedure)
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Criteria: `docs/phases/legible-entry/entry-usability-criteria.md` (owner-accepted, do not amend)
- Evidence pack: `docs/phases/legible-entry/entry-loop-synthetic-evidence-pack.md`
- File your scores to: `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-29-entry-loop-synthetic-track2-evaluator-a.md`

## Your brief

Exercise every criterion as an explicit system outcome, and preserve the
action/result transcript.

You are the evaluator who is allowed to check that what the surface *showed*
you is what actually *happened*. Where a criterion is about the system's
behaviour — a fact was accepted, these five lines changed, those four did not,
the return is complete — do not take the page's word for it. Confirm it at the
system level as well, and record both: what the surface displayed, and what you
independently observed.

That is the whole of your advantage over the other evaluator, and it is the
reason two briefs exist rather than one.

## What you score

Every criterion in the criteria document: 1.1 through 5.3, plus the five
carried-over ADR-0046 rules. Twenty rows.

**Pass or Fail. No third value.** The aggregation happens later and is not
yours to anticipate. If you find yourself wanting to write "partial", that is a
Fail with a rationale, or a Pass with a rationale, and you have to pick.

Score from the criteria document's own wording. Do not sharpen it, soften it,
or substitute your own judgement about what a good entry surface should do.
Several criteria state their own minimum bar explicitly — 2.2 says a bare
"required" label does not pass; 1.2 says the evaluator must not have to find
the input independently. Hold those bars as written.

The accessibility criteria are measurements, not impressions. Contrast ratios
are computed from actual rendered colours, landmarks and focus behaviour are
checked by operating the page with the keyboard. If you cannot measure
something, say so in the rationale rather than guessing in either direction.

## Running it

```sh
python3 -m packages.derivation.runners.entry_loop_evaluation
```

It prints the URL, the W-2 Box 1 figure to enter, the corrected figure for the
correction step, and a starting-state fingerprint. Record that fingerprint in
your transcript. Stop it with Ctrl-C; a clean restart is the same command
again.

Everything here is synthetic. There is no real data anywhere in this
evaluation.

## Independence

A second evaluator is scoring the same surface under a different brief, at the
same time or shortly after. **Do not read their file, look for it, or wait for
it.** If it exists on disk when you run, do not open it. Disagreement between
you is signal the procedure preserves deliberately; a consensus reached by one
of you reading the other's answers destroys the only thing this two-evaluator
design buys.

Do not read the Track 1 or Track 2a review records, charters, or build reports
either. They will tell you what the builder believes they satisfied, and your
job is what the surface actually does.

## Boundaries

- **Score. Do not fix.** Not the surface, not a test, not a typo. If something
  is broken, that is a score and a rationale.
- Do not amend the criteria. They are owner-accepted at `1e48443`. If you think
  a criterion is unscoreable as written, score it, and say so separately as a
  note to the owner.
- Do not aggregate, do not predict the cell verdict, do not compare yourself to
  the other evaluator.
- No maturity claim. Nothing moves on any matrix.

## What to file

Use the evidence pack's transcript and score-sheet shapes.

- Your raw transcript: the starting-state fingerprint, then every action you
  took and what you observed, in order. Enough that someone could repeat your
  run and get your scores.
- The twenty-row score sheet: Pass or Fail, with a transcript reference and a
  rationale for each.
- For anything you scored Fail: what specifically would have made it a Pass.
- Separately, at the end: anything you could not measure, and any criterion you
  found ambiguous to score.

Commit your file on this branch.
