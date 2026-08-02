# Charter — The Entry Loop (synthetic), Track 0: close F5

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Repairing: `docs/phases/legible-entry/entry-usability-criteria.md`
- Against: `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-28-entry-loop-synthetic-track0-repair-review.md` (`NOT READY`, F5 partial)

## Scope: one finding, one paragraph

The recheck closed F1–F4 and F6–F8 and found no regression in the three
measurements that previously passed. **F5 is the only thing open**, and it is
narrow.

The document says the evaluation fixture must make every expected-impact member
change and every untouched-comparison member stay unchanged, and that the
evaluation cannot run otherwise. That is correct and it is fail-closed. But the
dependency list immediately below says the evaluation cannot run until its
*three* listed dependencies are demonstrated — and the fixture's mutation
pattern is not one of them. The first listed dependency, seeding every required
non-W-2 fact so W-2 is the only missing family, does not imply it: a workspace
can be seeded correctly and still produce a fixture where one of the five
expected-impact lines does not move.

The consequence the reviewer names: a Track 2 conductor demonstrates the three
listed conditions, believes the instrument runnable, starts the evaluation, and
only then discovers criteria 3.2 and 4.2 cannot be scored. The instrument fails
late and ambiguously instead of up front.

## What to change

Make the fixture's required mutation pattern a **named run dependency**, either
as a fourth entry in that list or as an explicit clause of the seed dependency.
Either shape is acceptable; pick one and make the list complete and internally
consistent — the count in the surrounding prose has to match the list, and the
fail-closed condition further up must read as the same requirement, not a
second one.

That is the whole change. Expect it to be a paragraph.

## Boundaries

- **F5 only.** F1–F4 and F6–F8 are closed; do not revisit them, do not
  "improve" them while you are in the file.
- Do not confirm the dependency — naming it is the fix. Whether a fixture can
  actually produce the pattern is Track 1's to establish.
- Do not add criteria, change the aggregation rule, or touch the evaluator
  briefs.
- Documentation only. No product code, no matrix movement.
- If you believe the reviewer is wrong that this is load-bearing, say so in your
  report and change nothing.

## Verification

Same standard the last repair met, which the reviewer confirmed: the CI `verify`
sequence or a stated subset with each omission justified, the data-safety scan,
and the commit you worked from, recorded in the commit message. There is no
`.venv`; use system `python3`.

Orient with `python3 tools/build_orientation_block.py --ref HEAD`. The ratified
line is `origin/main-ui` and is derived for you; the merged PR #109 is the
milestone's opening plan PR and does not mean this workspace is spent.

## Report back

The change, and whether you made it a fourth dependency or a clause of the
first; confirmation that the fail-closed condition and the dependency list now
say the same thing; and anything you noticed but did not touch.
