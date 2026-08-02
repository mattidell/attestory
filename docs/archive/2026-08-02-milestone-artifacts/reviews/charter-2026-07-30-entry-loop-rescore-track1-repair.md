# Charter — Re-score the Entry Loop, Track 1 repair: check traversal order

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-loop-rescore.md`
- Branch: `track/entry-loop-rescore-track1`, continuing from `3ec7d08`
- Against: `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-30-entry-loop-rescore-track1-review.md` (**NOT READY**, F1)
- Review gate: **yes.** A focused recheck of F1 only.

## The finding

**F1 blocks.** The milestone plan and the build charter both require that
Shift+Tab "returns through the same set **in reverse order**." The probe
checks only set membership:

```js
matches: forwardOnly.length === 0 && backwardOnly.length === 0,
```

Order is collected and then never compared. The reviewer captured the raw
arrays from the unmodified surface and confirmed the check would report
`matches: true`, `forwardOnly: []`, `backwardOnly: []` for a defect that
visits every control in a scrambled order — for example a custom handler that
reassigns focus out of native tab sequence while still eventually landing on
everything.

Order matters to the requirement itself: a keyboard user expects Shift+Tab to
retrace Tab's exact path, not to visit the same elements in some order. This
is the whole reason Track 1 exists — an unmeasured half of a criterion — so
shipping a traversal check that does not measure traversal order would
reproduce the milestone's own defect inside the instrument built to fix it.

## The complication, which is the interesting part

The reviewer found that `backward` is **not** simply the reverse of `forward`
on the current, correct surface:

```
incomplete forward:  [wordmark, "Enter this fact", w2-box1 input, "Add W-2 Box 1"]
incomplete backward: [w2-box1 input, "Enter this fact", wordmark, "Add W-2 Box 1"]
```

`collectOrder` seeds the backward pass by focusing `forward[last]` and pressing
Shift+Tab, so the walk exhausts the true reverse path and then **wraps around
the tab cycle**, re-recording the seeding control at the tail. Excluding that
wraparound entry, the order is genuinely correct here.

**Do not fix this by trimming the last element.** A blind trim is exactly the
shape of machinery this milestone keeps rejecting: it would silently discard a
real trailing defect, and it asserts "the tail is always a wraparound
artifact," which is not something you have established. Terminate the backward
walk on a principled condition instead — for example, stop when the walk
returns to the control it was seeded from, and record that it did — so the
collected sequence is the true reverse path by construction rather than by
post-hoc correction. If you find a different principled termination, take it;
what is not acceptable is a length-based or position-based fudge.

## What to build

1. **Compare order positionally.** `backward`, once correctly terminated, must
   equal `forward` reversed element-for-element. Report the mismatch position
   and both sequences when it does not.

2. **Keep the set check.** Membership and order are different defects with
   different causes. A control reachable forward but not backward should still
   be reported as such, distinctly from an ordering mismatch — the reviewer
   confirmed the existing set check works and bites, so preserve it rather
   than folding it into the order comparison.

3. **Prove the order check bites, with an order-scrambling injection.** The
   reviewer explicitly left this demonstration to you and named why: F1 rests
   on reading the computation and on a captured counterexample, not on a
   constructed failure. Ship a defect injection that **preserves the reachable
   set but scrambles the order** — a handler that reassigns focus out of
   native sequence while still eventually visiting every control — and confirm
   the new check fails on it while the set check still reports
   `forwardOnly: []` and `backwardOnly: []`. That contrast is the deliverable:
   it demonstrates the order check catches something set membership cannot.

4. **Confirm the clean run still passes** with the trap removed, and that
   `mouseEventsDispatched` stays zero throughout both runs.

## Scope

**F1 only.** N1–N4 are recorded as sound and need no work. Do not revisit the
activation check, `settle()`, the seeding question, or the vacuous-pass guard;
the reviewer verified each independently and they hold.

Everything the build charter forbade still binds:

- `docs/phases/legible-entry/entry-usability-criteria.md` is **read-only**.
- Do not repair any surface defect the sharpened check exposes — report it.
  If the order check now fails against the real surface, **that is a genuine
  finding and the correct outcome.** Do not soften the check to make the
  surface pass.
- No surface behaviour change, no derivation package change, no real data.

## Verification

`python3 -m unittest tests.test_entry_loop_t1` while iterating; the full
quartet — `pytest -n auto`, `-m mypy`, `governance_lint`, `envelope_scan` —
once before you report.

**Report the quartet as a self-report, and say so.** No CI runs on this branch:
the `verify` workflow triggers only on `main`, and this line is `main-ui`. That
gap is recorded for the owner and is not yours to fix here.

## Done when

1. Backward traversal terminates on a principled condition, not a trim, and
   you can say what that condition is and why it is sound.
2. Order is compared positionally against `forward` reversed, with set
   membership still reported as its own distinct finding.
3. An order-scrambling injection demonstrates the new check fails where the
   set check passes — both results captured, not just the failure.
4. The clean run passes and dispatches zero mouse events.
5. Your report states what the real surface does under the order check,
   including a failure if there is one.
