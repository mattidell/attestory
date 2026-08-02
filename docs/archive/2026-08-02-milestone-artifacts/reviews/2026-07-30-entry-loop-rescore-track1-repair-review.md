# Review — Re-score the Entry Loop, Track 1 repair recheck: check traversal order (F1)

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-30-entry-loop-rescore-track1-repair-recheck.md`
- Repair charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-30-entry-loop-rescore-track1-repair.md`
- Prior review: `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-30-entry-loop-rescore-track1-review.md` (**NOT READY**, F1)
- Under review: `track/entry-loop-rescore-track1` @ `6ca0d6f`, range `3ec7d08..6ca0d6f`

## Orientation and review object

`python3 tools/build_orientation_block.py --ref HEAD` resolved reviewer at `be346b202294421770b807166084e58f5f226fbc`, matching `git rev-parse HEAD`. The charter directs a focused recheck of **F1 only** on `track/entry-loop-rescore-track1` at commit `6ca0d6f`.

Per the charter's directive, I note that the repair arrived without a builder's self-report. The verification battery below represents the first independent execution and measurement of this repair diff.

## Verdict: READY

The repair directly resolves **F1**. Traversal order is positionally checked against `forward` reversed, backward traversal terminates on a sound `returnedToSeed` condition rather than a trim, and the check is observed to **fail on an order-scrambled injection** while **passing cleanly on the real, unmodified surface**.

## Verification Measurements

### 1. Principled Termination — PASS

`collectBackwardOrder(seedKey, maxIterations)` seeds from `forward[last].key` (`seedKey`) and issues Shift+Tab events. The loop terminates immediately when `focused.key === seedKey`, setting `returnedToSeed = true` and breaking without appending a wraparound duplicate to `backward`.

If traversal never returns to `seedKey` (e.g. in `break-reverse-traversal` where Shift+Tab is trapped), `returnedToSeed` remains `false`. `orderMatches` evaluates `returnedToSeed && mismatchIndex === null`, ensuring a non-returning walk evaluates to `orderMatches: false` rather than passing on a truncated prefix.

### 2. Positional Comparison Accuracy — PASS

`actualBackward` is constructed as `[seedKey, ...backwardStepKeys]` and compared against `expectedBackward = forwardKeys.slice().reverse()`. Prepending `seedKey` is mathematically exact because `seedKey` is the starting active element when the backward pass begins.

Comparison evaluates up to `maxLen = Math.max(expectedBackward.length, actualBackward.length)`. Any length mismatch results in an out-of-bounds `undefined` comparison, capturing length discrepancies at `mismatchIndex` and failing `orderMatches`.

### 3. Order Check Bites (Scrambled Order Demonstration) — PASS

I independently ran `test_reverse_traversal_check_bites_when_order_is_scrambled` with a fresh server instance. Under `scramble-order` (which re-routes Shift+Tab into a scrambled cycle visiting every control):
- `setMatches`: `true` (`forwardOnly: []`, `backwardOnly: []`)
- `orderMatches`: `false` (`mismatchIndex: 1`)
- `matches`: `false`

This demonstrates the required contrast: positional order comparison catches an ordering defect that set membership alone reports as `matches: true`.

### 4. Injection Honesty — PASS

The `scramble-order` injection re-routes Shift+Tab across all controls in the DOM tab order (`.primary` -> `button:not(.primary)` -> `#w2-box1` -> `a[href]` -> `.primary`). Every control is visited, ensuring `setMatches: true` is load-bearing and not a symptom of dropped controls.

### 5. Real Surface Performance — PASS

Driven against the real, unmodified compiled surface across fresh server runs:
- `incomplete` phase: `returnedToSeed: true`, `setMatches: true`, `orderMatches: true`, `matches: true`.
- `complete` phase: `returnedToSeed: true`, `setMatches: true`, `orderMatches: true`, `matches: true`.
- `mouseEventsDispatched`: `0`.

The real surface passes the sharpened order check cleanly.

### 6. Scope Discipline — PASS

`git diff 3ec7d08..6ca0d6f` touches strictly two files (`tests/helpers/entry_loop_keyboard_operability_client.mjs` and `tests/test_entry_loop_t1.py`). `docs/phases/legible-entry/entry-usability-criteria.md` is untouched, surface behavior is unchanged, and prior findings N1–N4 remain sound.

### 7. Verification Battery Results — PASS

- `python3 -m unittest tests.test_entry_loop_t1`: 40 passed (144.70s).
- `pytest -n auto`: 748 passed (131.01s).
- `python3 -m mypy packages tests tools`: no issues found in 136 source files.
- `python3 tools/governance_lint.py`: conformant.
- `python3 tools/envelope_scan.py --range main-ui..HEAD`: clean (0 leaks).

## Summary

Track 1 (keyboard operability probe) is fully repaired, verified, and **READY**.
