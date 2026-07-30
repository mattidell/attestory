# Charter — The Entry Loop (synthetic), Track 0 repair recheck

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Under review: `4d8e7cb` — the repair of `docs/phases/legible-entry/entry-usability-criteria.md`
- Prior review: `docs/reviews/2026-07-28-entry-loop-synthetic-track0-review.md` (`NOT READY`, F1–F8)
- Repair charter: `docs/reviews/charter-2026-07-28-entry-loop-synthetic-track0-repair.md`
- Verdict: `READY` or `NOT READY`.

This is a **focused delta recheck**, not a fresh review. The prior review stands
as the finding set. Your question is whether the repair closed it without
breaking something that was already working.

## Orientation

Orient with `python3 tools/build_orientation_block.py --ref HEAD`. If you were
told anywhere to use `--ref main`, that instruction is stale — it was fixed at
`bd7211c`. The ratified line for this work is `origin/main-ui` and the tooling
derives it; do not compare against `origin/main`. A merged PR exists for this
branch (#109, the milestone's opening plan PR) and does not mean the workspace
is spent.

## Part 1 — did each finding close?

Take F1 through F8 in turn. For each: closed, partially closed, or not closed,
with the evidence you checked.

Two need more than a spot check:

**F1 — criterion 3.3.** The builder kept it in the Mechanical class and made it
observable by naming a fixed untouched comparison set. That was the charter's
preferred route, and it is the route with the most ways to go subtly wrong.
Check that the criterion as rewritten can actually be scored from the set
without reintroducing a judgement call, and that the omission note is honest
about what was given up — the prior review's objection was that the criterion
*was* the split, so a fixed set that still requires the evaluator to reason
about expectations has not closed it.

**F2 — the aggregation rule.** The charter dictated the rule verbatim. Check it
appears once, that the text matches what was dictated, and — more importantly —
that no other passage in the document contradicts it. The original defect was
two rules in different places, not a wrong rule.

## Part 2 — did the repair break anything?

The repair added roughly 50 lines to a 60-line document. That is a large enough
change to regress measurements the prior review passed.

**Re-run these three from the prior review, which passed then:**

- **Implementation independence** (prior measurement 3, PASS). The new fixed
  W-2 evaluation sets are the main risk. A named set of derived lines that must
  visibly change or stay unchanged is close to the line between "what the
  surface must accomplish" and "what the surface must contain." Say which side
  it lands on. If it constrains the build's structure, that is a finding.
- **Scope** (prior measurement 7, PASS). The milestone leaves the per-field
  explanation schema to emerge from the build. Check the added specificity has
  not started specifying it.
- **Coverage** (prior measurement 6, PASS). Check no step lost ground.

**Also check the new runnability constraint.** The document now says the
evaluation fixture must make every expected-impact member change, and that the
evaluation is not runnable if the fixture cannot produce that condition. Read
that against the F5 dependency list. Is it consistent with them, or does it add
a fourth dependency that is not named as one?

## Part 3 — the standing question

The instrument's purpose is to be executable by someone who did not write it,
against a surface nobody has built. The prior review's closing observation was
that a real run most likely dies on a split over 3.3 with no rule to resolve it.
Say whether that is still the most likely failure, and if not, what replaced it.

## Boundaries

- Findings are limited to F1–F8, regressions of previously passing measurements,
  and anything the repair newly introduced. Do not reopen matters the prior
  review considered and accepted.
- Do not rewrite the criteria.
- Do not lower or raise the bar because you would have written it differently.
- No product code, no maturity claim, no matrix movement.

## Verification

The prior review's F7 was a missing verification record. `4d8e7cb` carries one
in its commit message. Confirm it is present and that its claims hold — re-run
what it says it ran. Include your own data-safety scan.

## Report back

The verdict; F1–F8 each with its evidence; the three re-run measurements; where
the fixed evaluation sets land on implementation independence; and the single
thing most likely to go wrong when Track 2 runs this for real.
