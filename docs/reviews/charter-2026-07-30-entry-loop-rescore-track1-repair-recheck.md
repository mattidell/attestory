# Charter — Re-score the Entry Loop, Track 1 repair recheck (F1)

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-rescore.md`
- Repair charter: `docs/reviews/charter-2026-07-30-entry-loop-rescore-track1-repair.md`
- Prior review: `docs/reviews/2026-07-30-entry-loop-rescore-track1-review.md` (**NOT READY**, F1)
- Under review: `track/entry-loop-rescore-track1` @ `6ca0d6f`, range `3ec7d08..6ca0d6f`
- **Focused recheck: F1 only.** N1–N4 were verified sound in the prior review and are not reopened.

## Read this first: the repair arrived without a report

The repair was **recovered from an uncommitted working tree by the foreman.**
The builder did not commit, did not push, and filed no report. There is
therefore:

- **no self-reported verification** for this diff — nobody has stated that
  `pytest`, `mypy`, `governance_lint`, or `envelope_scan` pass on it;
- **no statement of what the new order check does against the real surface** —
  in particular, nobody has said whether the real surface passes or fails it.

The foreman does not run the suite, so neither of those has been established
by anyone. **You are the first party to verify any of it.** Do not read the
commit message's description of the change as a report; it is the foreman's
reading of a diff, not a builder's account of what it did and observed.

If the full quartet does not pass, that is a blocking finding.

## What F1 was

The milestone requires that Shift+Tab "returns through the same set **in
reverse order**." The probe checked only set membership; order was collected
and never compared. A defect visiting every control in a scrambled order would
report `matches: true` with no finding at all.

## What to verify

1. **Is the termination condition principled, or a disguised trim?** The
   charter forbade fixing the wraparound artifact by dropping the last element.
   The repair adds `collectBackwardOrder(seedKey, ...)`, which breaks when the
   walk returns to its seed and records `returnedToSeed`. Establish that this
   is sound — including what happens when the walk **never** returns to the
   seed, and whether `returnedToSeed: false` is actually treated as a failure
   rather than quietly producing a short sequence that happens to match a short
   expectation.

2. **Is the positional comparison correct?** `actualBackward` is built as
   `[seedKey, ...backwardStepKeys]` and compared element-wise against
   `forwardKeys` reversed, reporting `mismatchIndex`. Confirm the two sequences
   are genuinely comparable — in particular that prepending the seed is right
   rather than off by one, and that a length difference is caught rather than
   passing when one sequence is a prefix of the other.

3. **Does the order check actually bite?** The repair ships a `scramble-order`
   injection and
   `test_reverse_traversal_check_bites_when_order_is_scrambled`, which asserts
   the required contrast: `setMatches: True` with `forwardOnly`/`backwardOnly`
   empty, while `orderMatches: False` with a non-null `mismatchIndex`. **Run
   it yourself against a fresh server** — the prior review found that reusing a
   server across probe invocations produced a misleading result — and confirm
   it fails for the injected reason rather than by breaking the page or the
   probe. The contrast is the point: the injection must be one that set
   membership provably cannot catch.

4. **Is the injection honest?** `scramble-order` routes Shift+Tab by matching
   on class names and description substrings (`.primary`, `"Enter this fact"`,
   `w2-box1`, `a[href]`). Consider whether it genuinely preserves the reachable
   set — if it silently drops a control, the test would be demonstrating the
   *set* check, not the order check, and the `setMatches: True` assertion is
   what stands between those two cases. Confirm that assertion is load-bearing.

5. **What does the real surface do?** Run the unmodified probe and state
   whether the order check passes against the real compiled surface, in both
   the incomplete and complete phases. **If it fails, that is a legitimate
   finding about the surface, not a defect in the repair** — report it as
   such and do not treat it as grounds to weaken the check.

6. **Scope.** Range `3ec7d08..6ca0d6f` should touch only the probe client and
   its test file. Confirm `entry-usability-criteria.md` is untouched, no
   surface behaviour changed, and the set check and its existing
   demonstration still work as the prior review found them.

## Verification

Run the full quartet — `pytest -n auto`, `-m mypy`, `governance_lint`,
`envelope_scan` — because nobody else has. Report each result.

**CI now runs on this line as of PR #116** (`verify` was triggering only on
`main`, so no check had ever run on `main-ui`). If that PR has merged by the
time you review, a real CI result may be available for the branch; prefer it
over a local rerun and reference the check. If it has not merged, say so and
report your local runs as local runs.

## Verdict

`READY` or `NOT READY`. If READY, say explicitly that the order check has been
observed to fail on a scrambled order and pass on the real surface — those two
observations together are what closes F1, and either alone does not.
