# Retrospective: A Box 4 "No" Is Not Asked For an Amount (2025)

Milestone key: box4-no-prompt. Plan:
`docs/phases/engine-breadth/milestones/box4-no-prompt.md`.
Closed 2026-11-17. Core v94, registry v92, release v92. Content only:
sixteen per-statement helper rules, one selection, a vocabulary bundle,
Form 1040 line 25b v9 and the box 4 amount question v2. No schema,
engine, projection or page change.

## What happened

box4-amount-asked closed on P0 with a parked note: a filer who answered
that a Form 1099-B statement shows no box 4 withholding was still shown
the amount prompt, and line 25b stayed blocked until they entered $0.
P0 reproduced it on core v93. Line 25b's `require_paired` expression
pairs every sale's statement with an amount row and never reads the
yes/no. The content repair counts, per sale subject type, whether each
statement still needs an amount (none when it has one or answered
"no"), and line 25b skips the pairing only when that count is zero;
otherwise the original expression runs unchanged. An entered amount
wins over a contradictory "no".

The replay did not show what the plan expected. None of the 775
recorded lists computes after the change: 271 move line 25b from the
statement amount to the return-level "statement with no sale" question,
which they never answered. That question was always required; nothing
defaults it. Two discarded prototype shapes changed 412 and then 14
unrelated pins before the original-pairing fallback held them still.

Track 0 found one wording fault: the amount prompt is one sentence for
the whole return, so on a mixed return it asked for statements already
answered "no" or already entered. Track 1 published new words. A Codex
usage limit ended Track 1 just after its last commit; the foreman read
the committed result and the review waited for the reset. The fresh
review found no product fault; it marked the draft gate blocking and
showed the replay classifier could put a changed value under an
expected label. The repair made the classifier reject any change but
the two named ones, with mutation checks, and reclassified the saved
replay: counts unchanged.

Dispatch: Codex (gpt-6.1-sol) throughout. One builder thread across P0
(high), Track 0 (high), Track 1 (medium) and the repair (medium); one
fresh reviewer thread (high). Builder turns read 24-56M input tokens,
98-99% cached; the review read 3.9M.

## What worked

- Keeping the original expression as the fallback. It is what made the
  change provably narrow: any statement not satisfied runs exactly the
  v93 path, so refusal codes and missing counts stay put.
- Asking Track 0 what the filer sees next, not only whether the line
  computes. That found the "each statement" prompt.

## What to change

- A charter's expected replay class must be checked against what the
  recorded lists actually answer. "Lines 25b/25d compute" was not true
  of any recorded list, because a second question stood behind the
  first.
- A replay classifier must be strict first and label second: compare
  every row, including added and removed rows, before naming a change
  expected. Mutation-test it before trusting its counts.
- A builder that may hit a usage limit should write its report before
  its last check, or the foreman reads the commits instead.

## Follow-ups

Parked in the roadmap: an amount added after a "no" leaves the earlier
zero payment findings current until a run (engine currency behaviour,
same on v93). The return-level box 4 question and total, and naming the
statement in the box 4 questions, stay parked.
