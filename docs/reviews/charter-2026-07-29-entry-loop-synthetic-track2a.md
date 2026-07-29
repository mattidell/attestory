# Charter — The Entry Loop (synthetic), Track 2a: the evaluation launcher

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Working from: `4dd0063` (Track 1 `READY`)
- Deliverable: one command that stands the evaluation up, and the evidence pack
  that goes with it.

## Why this exists

Track 2 puts two independent evaluators in front of the entry surface and has
them score it against
`docs/phases/legible-entry/entry-usability-criteria.md`. The procedure says both
evaluators receive the same seeded synthetic workspace, the same surface URL,
the same synthetic W-2 source data, and the same fixed evaluation sets.

Right now there is no way to hand them that. The surface is stood up inside
`tests/test_entry_loop_t1.py`; there is no entry point that seeds a workspace
and serves the page. Two evaluators hand-rolling their own launcher would
introduce variance into exactly the thing being measured, and one of the two is
deliberately kept away from the implementation, so it cannot be asked to write
one at all.

This track builds that command. It is small. Do not let it grow.

## What to build

**1. A launcher.** One command that seeds a fresh synthetic workspace, serves
the entry surface, and prints the URL. Reuse what the tests already do — this
should mostly be lifting an existing path into a runnable entry point, not new
machinery. If that turns out not to be true, stop and report before writing a
parallel path.

It must be repeatable: two evaluators running it independently, and the same
evaluator running it twice, must each get an identical starting state. An
evaluation where the two evaluators saw different starting conditions is not an
evaluation.

It must print, at startup, everything an evaluator needs and nothing about how
it works:

- the URL;
- the synthetic W-2 figures to type, and the corrected figure to type for the
  correction step;
- how to stop it and how to get back to a clean starting state.

**2. An evidence pack document** the evaluators are pointed at, carrying the
fixed W-2 evaluation sets, the criterion list, and the score sheet shape.
Assemble it from the criteria document; do not restate the criteria in your own
words and do not add, drop, or sharpen any of them. If you find one you cannot
carry across without interpreting it, that is a finding — report it, do not
resolve it.

## Boundaries

- No change to the entry surface, the loop, the server, or any test. If
  standing this up requires changing the surface, stop and report.
- No change to the criteria document. It is owner-accepted at `1e48443`
  (`docs/reviews/2026-07-29-entry-loop-synthetic-track0-owner-acceptance.md`).
- **Do not score anything.** Not one criterion, not informally, not in your
  report. You have implementation context, which is exactly what disqualifies
  you as an evaluator.
- Do not write anything into the evidence pack that reveals how the surface is
  built. Evaluator B approaches it without implementation context, and a
  helpful hint in the pack destroys that.
- Synthetic only, W-2 only, no residency locator anywhere including the
  launcher's own output.
- No maturity movement.

## Two findings carried in from the Track 1 repair review

Neither blocks Track 2 and neither is yours to fix. They are here so you do not
rediscover them and think they are new:

- `tools/presentation_harness/lib/chrome.mjs`'s `launchChrome()` leaves an
  orphaned Chrome process and its temp profile directory behind when the calling
  process is killed on a timeout rather than exiting normally.
- The duplicate-submission and out-of-order tests pass because the kernel's
  `apply_contribution` independently refuses contribution-id reuse, so they do
  not prove `entry_loop.py`'s own staleness check does any work.

If your launcher makes either one worse or more likely to bite an evaluator,
say so.

## Verification

The CI `verify` sequence or a stated subset with each omission justified, the
data-safety scan, and the commit you worked from, in the commit message. The
prior commits on this branch set the standard.

Orient with `python3 tools/build_orientation_block.py --ref HEAD`. No `.venv`;
use system `python3`. Ratified line `origin/main-ui`, derived for you; the
merged PR #109 is the milestone's opening plan PR.

## Report back

The command and what it prints; what you lifted versus what you had to write;
your evidence that two runs produce the same starting state; anything in the
criteria you could not carry into the evidence pack without interpreting it;
and the weakest part of what you built.
