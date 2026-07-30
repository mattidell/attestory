# Owner acceptance — The Entry Loop (synthetic), Track 0

- Accepted by: **Matt Idell**, repository owner, 2026-07-29
- Accepting: `docs/phases/legible-entry/entry-usability-criteria.md` at `1e48443`
- Track: 0 of `docs/phases/legible-entry/milestones/entry-loop-synthetic.md`

## Why this note exists

Track 0's last formal review verdict is the `NOT READY` at `319521c`
(`docs/reviews/2026-07-28-entry-loop-synthetic-track0-repair-review.md`). That
recheck closed F1–F4 and F6–F8 and found no regression in the measurements that
had already passed. F5 was the only thing left open, and it was one paragraph:
the document's fail-closed fixture condition was not among the named run
dependencies, so a Track 2 conductor could believe the instrument runnable and
discover mid-evaluation that criteria 3.2 and 4.2 could not be scored.

F5 was closed at `1e48443` by naming the fixture's required mutation pattern as
a fourth run dependency, worded to match the fail-closed passage above it, with
the count corrected from three to four.

No third review cycle was run on that change. The foreman recommended skipping
it because the check is mechanical — whether the list has four entries and
whether its wording matches the passage it restates — and the owner agreed.
That left the criteria document without a `READY` on the record, which is a gap
worth closing explicitly rather than leaving for a later reader to notice.

## The acceptance

The owner has read the F5 change and accepts
`docs/phases/legible-entry/entry-usability-criteria.md` at `1e48443` as the
instrument Track 2 scores against.

This is owner acceptance, not a review verdict. It does not convert the
`NOT READY` at `319521c` into anything else, and it does not claim independent
verification. It records that the authority who owns the maturity claim read
the outstanding change and accepted the document as the bar.

Under the phase's own method, the owner reviews the criteria, the evidence, and
the result. This is the first of those three, taken before Track 2 runs, so
that the instrument is accepted without knowledge of what it scored.

## What this does not do

- It does not move any maturity cell. Track 2 scores; Track 3 moves the cell if
  and only if the evaluation passed.
- It does not amend the criteria. The document stands at `1e48443`.
- It does not reopen F1–F4 or F6–F8, which the recheck closed.
