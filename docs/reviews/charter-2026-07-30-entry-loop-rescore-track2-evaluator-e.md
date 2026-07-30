# Charter — Re-score the Entry Loop, Track 2: Evaluator E (Builder brief)

- Role: **Evaluator E**, the Builder brief
  (`docs/phases/legible-entry/entry-usability-criteria.md`, Scoring Procedure)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-rescore.md`
- Branch: `track/entry-loop-rescore-track2-evaluator-e`, from `main-ui` after PR #119 merges
- Criteria: `docs/phases/legible-entry/entry-usability-criteria.md` (owner-accepted, **read-only for this entire milestone**)
- Evidence pack: `docs/phases/legible-entry/entry-loop-synthetic-evidence-pack.md`
- Run dependencies: `docs/reviews/2026-07-30-entry-loop-rescore-track2a-dependencies.md` (all four confirmed; you may read this)
- File your scores to: `docs/reviews/2026-07-30-entry-loop-rescore-track2-evaluator-e.md`

## Why this is a full re-score

The W-2 cell was scored, failed, and repaired — twice. It has never been
scored end-to-end against the surface that now exists. Partial re-scores
covered only the rows the repairs were expected to move, which means the
current surface has **no complete score of record**, and the cell sits at L1.

So this run scores **all twenty rows**, from scratch, against the surface as it
stands today. Nothing carries over. No row is confirmed by a previous run.

You are a fresh evaluator. Four agents have scored this surface before you and
all four now know it too well to score it again.

## What you score — all twenty rows

The fifteen numbered criteria across the five loop steps (1.1–1.3, 2.1–2.3,
3.1–3.3, 4.1–4.3, 5.1–5.3), plus the five rows carried over from ADR-0046:
sub-section blast containment, accessibility baseline, no derived value from
invalid or blocked input, fail-loud, and blanket redaction.

Score every one. Do not skip a row because it looks obviously fine.

**Pass or Fail. No third value.** Aggregation happens later and is not yours to
anticipate. If you want to write "partial", that is a Pass or a Fail with a
rationale, and you have to pick.

Score from the criteria document's own wording. Do not sharpen it or soften it.
Where a criterion states its own minimum bar, hold that bar exactly — 2.2, for
instance, says a bare "required" label does not pass, and that field-attached
text must name the immediate return destination and the completion purpose.

## Your brief

Exercise every criterion you score as an explicit system outcome, and preserve
the action/result transcript.

You are the evaluator allowed to check that what the surface *showed* you is
what actually *happened*. Where a row is about behaviour — a value was
accepted, a value was refused, nothing was echoed back, no derived value
reached the DOM — do not take the page's word for it. Confirm it at the system
level as well, and record both: what the surface displayed, and what you
independently observed.

That is your whole advantage over the other evaluator, and the reason two
briefs exist rather than one.

## The accessibility row, specifically

This row failed the cell in the first run and is the reason the milestone
exists. It gets the most spend.

It bundles five requirements: text contrast at 4.5:1; non-text contrast at 3:1
for **visible control boundaries and focus indicators**; a `main` landmark and
a named form landmark; **Tab/Shift+Tab reachability with standard-key
operability**; and focus visibility through `:focus-visible`.

Two things you must not do with it:

1. **Do not score it as one impression.** Score it only after you have a
   finding for each of the five requirements separately. A Pass on this row
   asserts all five, so a Pass you cannot decompose is a Pass you cannot
   defend.

2. **Do not assume the keyboard requirement is unmeasurable.** It used to be.
   Track 1 of this milestone built a Chrome DevTools Protocol probe for it —
   `tests/helpers/entry_loop_keyboard_operability_client.mjs`, exercised by the
   `KeyboardOperability` class in `tests/test_entry_loop_t1.py`. It dispatches
   real key events, walks the forward Tab order, walks Shift+Tab back, and
   compares the reverse walk **positionally** against the forward one, not just
   as a set. Your brief permits you to use it. Use it, read what it actually
   asserts, and report what it found — including in both the incomplete and
   complete phases, since the surface's control set differs between them.

   The probe is a measurement instrument, not a verdict. It tells you what the
   focus order is; whether that satisfies the criterion is still your call.

**Measure focus indicators and control boundaries in every background context
the surface can put them on**, not just the one you land in first. The first
run's two failures were both non-text contrast, and both were found only
because one evaluator measured somewhere the other did not — a focus ring
against the dark-green completion region, and the input's own boundary against
the card behind it. Enumerate the contexts you found and say how many there
are.

These are measurements, not impressions. Compute contrast ratios from actual
rendered colours. If you cannot measure something, say so in the rationale
rather than guessing in either direction.

## Running it

```sh
python3 -m packages.derivation.runners.entry_loop_evaluation
```

It prints the URL, the W-2 Box 1 figure to enter, the corrected figure, and a
starting-state fingerprint. **Record that fingerprint in your transcript.** It
differs on every run by design — fresh temp workspace, fresh port and token —
so record *your* run's value; do not expect it to match anyone else's.

Stop with Ctrl-C; a clean restart is the same command again. Run your own
instance and do not share one with anyone, since a submitted contribution
advances the state.

Everything here is synthetic. There is no real data anywhere in this
evaluation.

## Independence — the prior scores are withheld from you on purpose

A second evaluator, F, is scoring the same twenty rows under a different brief.
**Do not read their file, look for it, or wait for it.** If it exists on disk
when you run, do not open it.

**Do not read any prior evaluator or aggregation file**, including:

- `docs/reviews/2026-07-29-entry-loop-synthetic-track2-evaluator-a.md`
- `docs/reviews/2026-07-29-entry-loop-synthetic-track2-evaluator-b.md`
- `docs/reviews/2026-07-29-entry-loop-synthetic-track2e-evaluator-c.md`
- `docs/reviews/2026-07-29-entry-loop-synthetic-track2e-evaluator-d.md`
- any aggregation record from either prior run,
- the charters that briefed those evaluators.

They contain the previous scores and name the specific defects that were
repaired. Reading them would tell you where to look and what answer to expect.
This run exists precisely to get an answer nobody told you in advance, and
that is the only reason a full re-score is worth its cost.

You may read the Track 2a dependency report and the Track 1 keyboard-probe
code. Those are instruments and preconditions, not prior scores.

## Boundaries

- **Score. Do not fix.** Not the surface, not a test, not a typo. If something
  is broken, that is a score and a rationale.
- **Do not amend the criteria document.** It is read-only for this entire
  milestone, for every unit, including you. If a criterion seems unscoreable as
  written, score it anyway and say so separately as a note to the owner.
- Do not aggregate, do not predict the cell verdict, do not compare yourself to
  the other evaluator.
- No maturity claim. Nothing moves on any matrix.
- **A second FAIL is a legitimate outcome.** The milestone plan says so
  explicitly. Do not shade a marginal row toward Pass because the surface has
  already failed twice and you can infer that someone wants it to pass.

## What to file

Use the evidence pack's transcript and score-sheet shapes, at full twenty rows.

- Your raw transcript: the starting-state fingerprint, then every action and
  observation in order. Enough that someone could repeat your run and get your
  scores.
- The twenty-row score sheet: Pass or Fail, with a transcript reference and a
  rationale for each.
- For the accessibility row: a separate finding for each of its five
  requirements, and your contrast measurements as numbers, per element per
  background context.
- What the keyboard probe reported, in both phases, and how you read it.
- For anything you scored Fail: what specifically would have made it a Pass.
- At the end, separately: anything you could not measure, and any row you found
  ambiguous as written.

## Done when

Your file is **committed and pushed** on your branch, and you have opened a PR
against `main-ui` (each track gets its own PR as of 2026-07-30) without merging
it. Three builders on this milestone have now left work in an uncommitted
working tree; do not be the fourth.

Orient with `python3 tools/foreman_context.py --ref HEAD --format markdown`. No
`.venv`; use system `python3`.
