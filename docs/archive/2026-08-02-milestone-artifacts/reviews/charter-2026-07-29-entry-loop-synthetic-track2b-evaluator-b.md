# Charter — The Entry Loop (synthetic), Track 2b: Evaluator B

- Role: **Evaluator B**, the Reviewer brief
  (`docs/phases/legible-entry/entry-usability-criteria.md`, Scoring Procedure)
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Criteria: `docs/phases/legible-entry/entry-usability-criteria.md` (owner-accepted, do not amend)
- Evidence pack: `docs/phases/legible-entry/entry-loop-synthetic-evidence-pack.md`
- File your scores to: `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-29-entry-loop-synthetic-track2-evaluator-b.md`

## Your brief

Approach this surface **without implementation context.** Attempt the five
steps of the loop using only the surface's own guidance, and record every point
at which the surface required you to infer something it did not tell you.

You are standing in for a person who has a tax document in front of them and
has never seen this system. That person cannot read the source, cannot check
the act log, and cannot ask the builder what a field means. Neither can you.

**Do not read any of the following**, at any point, for any reason:

- `packages/derivation/entry_loop.py`, or anything else under `packages/`;
- the Svelte source under `packages/sample_data/entry_loop_t1/`;
- `tests/test_entry_loop_t1.py` or any test;
- any charter, review, or build report for Track 1 or Track 2a;
- the milestone plan.

If you find yourself reaching for one of those to resolve a question, that is
the finding. Record the question you could not answer from the surface, and
score accordingly.

You need exactly two documents: the criteria and the evidence pack. Read them
first, then go to the page.

## What you score

Every criterion in the criteria document: 1.1 through 5.3, plus the five
carried-over ADR-0046 rules. Twenty rows.

**Pass or Fail. No third value.** If you want to write "partial", that is a
Fail with a rationale, or a Pass with a rationale, and you have to pick.

Score from the criteria document's own wording. Several criteria state their
own minimum bar — 2.2 says a bare "required" label does not pass; 1.2 says you
must not have to find the input independently in another form. Hold those as
written rather than substituting your own sense of what is reasonable.

Your brief gives you unique standing on the judgement criteria — 1.3, 2.3, 4.3,
5.3 — which all turn on what a person can state *without guessing*. You are the
one who actually cannot cheat on those. Take them seriously and be honest about
where you guessed.

The accessibility criteria are measurements, not impressions. Compute contrast
ratios from rendered colours; check landmarks and focus by operating the page
with the keyboard. If you cannot measure something, say so rather than guessing
in either direction.

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

A second evaluator is scoring the same surface under a different brief.
**Do not read their file, look for it, or wait for it.** If it exists on disk
when you run, do not open it. Where the two of you disagree, that disagreement
is signal the procedure preserves on purpose; a consensus reached by reading
each other's answers destroys the only thing this design buys.

## Boundaries

- **Score. Do not fix.** Not the surface, not a test, not a typo.
- Do not amend the criteria. They are owner-accepted at `1e48443`. If you think
  one is unscoreable as written, score it, and say so separately as a note to
  the owner.
- Do not aggregate, do not predict the cell verdict, do not compare yourself to
  the other evaluator.
- No maturity claim. Nothing moves on any matrix.

## What to file

Use the evidence pack's transcript and score-sheet shapes.

- Your raw transcript: the starting-state fingerprint, then every action and
  observation in order, including the attempts that did not work.
- The twenty-row score sheet: Pass or Fail, with a transcript reference and a
  rationale for each.
- **A list of every point where the surface required inference** — where you
  had to guess, assume, or reason from outside knowledge to keep going. This is
  the part of your file the other evaluator structurally cannot produce, and it
  is the most valuable thing you file.
- For anything you scored Fail: what specifically would have made it a Pass.
- Anything you could not measure, and any criterion you found ambiguous.

Commit your file on this branch.
