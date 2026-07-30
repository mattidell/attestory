# Charter — Re-score the Entry Loop, Track 2: Evaluator F (Reviewer brief)

- Role: **Evaluator F**, the Reviewer brief
  (`docs/phases/legible-entry/entry-usability-criteria.md`, Scoring Procedure)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-rescore.md`
- Branch: `track/entry-loop-rescore-track2-evaluator-f`, from `main-ui` after PR #119 merges
- Criteria: `docs/phases/legible-entry/entry-usability-criteria.md` (owner-accepted, **read-only for this entire milestone**)
- Evidence pack: `docs/phases/legible-entry/entry-loop-synthetic-evidence-pack.md`
- File your scores to: `docs/reviews/2026-07-30-entry-loop-rescore-track2-evaluator-f.md`

## Why this is a full re-score

The W-2 cell was scored, failed, and repaired — twice. It has never been scored
end-to-end against the surface that now exists; the partial re-scores covered
only the rows the repairs were expected to move. The current surface has **no
complete score of record**.

So this run scores **all twenty rows**, from scratch. Nothing carries over. No
row is confirmed by a previous run.

You are a fresh evaluator. Four agents have scored this surface before you and
all four now know it too well to score it again.

## What you score — all twenty rows

The fifteen numbered criteria across the five loop steps (1.1–1.3, 2.1–2.3,
3.1–3.3, 4.1–4.3, 5.1–5.3), plus the five rows carried over from ADR-0046:
sub-section blast containment, accessibility baseline, no derived value from
invalid or blocked input, fail-loud, and blanket redaction.

Score every one. Do not skip a row because it looks obviously fine.

**Pass or Fail. No third value.** If you want to write "partial", that is a Pass
or a Fail with a rationale, and you have to pick.

Score from the criteria document's own wording rather than your own sense of
what is reasonable. Where a criterion states its own minimum bar, hold that bar
exactly — 2.2, for instance, says a bare "required" label does not pass, and
that field-attached text must name the immediate return destination and the
completion purpose.

## Your brief

Approach this surface **without implementation context.** Work the loop using
only the surface's own guidance, and record every point at which the surface
required you to infer something it did not tell you.

You are standing in for a person who has a W-2 in front of them and has never
seen this system. That person cannot read the source, cannot check the act log,
and cannot ask the builder what a field means. Neither can you.

**Do not read any of the following**, at any point, for any reason:

- anything under `packages/` — including `packages/derivation/entry_loop.py`,
  the Svelte source, and the fixture and format declaration under
  `packages/sample_data/entry_loop_t1/`;
- anything under `tests/` — including
  `tests/helpers/entry_loop_keyboard_operability_client.mjs` and
  `tests/test_entry_loop_t1.py`;
- **`docs/reviews/2026-07-30-entry-loop-rescore-track2a-dependencies.md`** — it
  enumerates the surface's controls, states, and focus-indicator CSS, which is
  exactly the implementation context your brief denies you. Evaluator E may
  read it. You may not;
- any charter, review, build report, or aggregation record for any track of
  this milestone or the two before it — including every prior evaluator file
  (`…track2-evaluator-a.md`, `…-b.md`, `…track2e-evaluator-c.md`, `…-d.md`) and
  the charters that briefed them;
- the milestone plan, the roadmap, or `docs/phase-state.md`.

If you find yourself reaching for one of those to resolve a question, **that is
the finding.** Record the question you could not answer from the surface, and
score accordingly.

You need exactly two documents: the criteria and the evidence pack. Read them,
then go to the page.

## The accessibility row, specifically

This row failed the cell in the first run. It gets the most spend.

It bundles five requirements: text contrast at 4.5:1; non-text contrast at 3:1
for **visible control boundaries and focus indicators**; a `main` landmark and
a named form landmark; **Tab/Shift+Tab reachability with standard-key
operability**; and focus visibility through `:focus-visible`.

**Do not score it as one impression.** Score it only after you have a finding
for each of the five requirements separately. A Pass on this row asserts all
five, so a Pass you cannot decompose is a Pass you cannot defend.

Check landmarks, reachability and operability by **operating the page with the
keyboard yourself** — Tab forward through every action, Shift+Tab back, and
activate each control with its standard Enter or Space key. You are not
permitted the test harness, and you do not need it: this requirement is about
whether a person using a keyboard can work the loop, and you are that person.
Record the order you observed going forward and the order you observed coming
back.

**Measure focus indicators and control boundaries in every background context
the surface can put them on**, including states the page reaches only after you
have entered something. Enumerate the contexts you found.

These are measurements, not impressions. Compute contrast ratios from rendered
colours. If you cannot measure something, say so rather than guessing in either
direction.

## Running it

```sh
python3 -m packages.derivation.runners.entry_loop_evaluation
```

It prints the URL, the W-2 Box 1 figure to enter, the corrected figure, and a
starting-state fingerprint. **Record that fingerprint in your transcript.** It
differs on every run by design, so record *your* run's value; do not expect it
to match anyone else's.

Stop with Ctrl-C; a clean restart is the same command again. Run your own
instance and do not share one with anyone.

Everything here is synthetic. There is no real data anywhere in this
evaluation.

## Independence — the prior scores are withheld from you on purpose

A second evaluator, E, is scoring the same twenty rows under a different brief.
**Do not read their file, look for it, or wait for it.** If it exists on disk
when you run, do not open it. Where the two of you disagree, that disagreement
is signal the procedure preserves on purpose; a consensus reached by reading
each other's answers destroys the only thing this design buys.

The prior runs' scores are withheld from you deliberately. They would tell you
where to look and what answer to expect, and this run exists precisely to get
an answer nobody told you in advance.

## Boundaries

- **Score. Do not fix.** Not the surface, not a test, not a typo.
- **Do not amend the criteria document.** It is read-only for this entire
  milestone, for every unit, including you. If one seems unscoreable as
  written, score it anyway and say so separately as a note to the owner.
- Do not aggregate, do not predict the cell verdict, do not compare yourself to
  the other evaluator.
- No maturity claim. Nothing moves on any matrix.
- **A second FAIL is a legitimate outcome.** The milestone plan says so
  explicitly. Do not shade a marginal row toward Pass.

## What to file

Use the evidence pack's transcript and score-sheet shapes, at full twenty rows.

- Your raw transcript: the starting-state fingerprint, then every action and
  observation in order, **including the attempts that did not work**.
- The twenty-row score sheet: Pass or Fail, with a transcript reference and a
  rationale for each.
- For the accessibility row: a separate finding for each of its five
  requirements, your observed forward and backward focus orders, and your
  contrast measurements as numbers, per element per background context.
- **A list of every point where the surface required inference** — where you had
  to guess, assume, or reason from outside knowledge to keep going. This is the
  part of your file the other evaluator structurally cannot produce, and it is
  the most valuable thing you file.
- For anything you scored Fail: what specifically would have made it a Pass.
- At the end, separately: anything you could not measure, and any row you found
  ambiguous as written.

## Done when

Your file is **committed and pushed** on your branch, and you have opened a PR
against `main-ui` (each track gets its own PR as of 2026-07-30) without merging
it. Three builders on this milestone have now left work in an uncommitted
working tree; do not be the fourth.

Orient with `git rev-parse HEAD` to record the commit you scored. Do **not** run
`tools/foreman_context.py` — it prints the phase state, which your brief denies
you. No `.venv`; use system `python3`.
