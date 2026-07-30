# Track 4 — foreman inspection

- Inspected by: **Foreman**, 2026-07-29
- Object: `146aede` — Track 4, focus indicators stated per control
- Charter: `docs/reviews/charter-2026-07-29-entry-loop-synthetic-track4-focus.md`
- Status: **Foreman inspection, not a review verdict.** The charter set no review
  gate; the owner is cutting the milestone here.

## Verification reproduces

Re-run independently at `146aede`:

| Check | Result |
| --- | --- |
| `pytest -n auto` | 723 passed, 3245 subtests |
| `mypy` | clean, 135 source files |
| `governance_lint.py` | conformant |
| `envelope_scan.py --range origin/main-ui..HEAD` | clean, exit 0 |
| `generate_entry_loop_t1_fixtures` | 943 entries, 5,085,046 bytes, byte-identical |

Every number in the commit message reproduced. The metadata regenerates to the
same total with no working-tree change, so the manifest, registry, release, and
adoption pins agree.

## The invariant test bites, and proving that took one extra step

The claim under inspection is that reverting the `!important` fix fails
`FocusIndicators` specifically and only on `#w2-box1`.

Reverting the three declarations alone makes the test fail with
`entry-surface-refused:SURFACE_ENTRY_CHECKSUM_MISMATCH` — the surface artifact
declines to resolve because the content tree no longer matches its pinned
checksum. That is correct behaviour, but it means a mutation of the content tree
**always** fails this test, for a reason unrelated to focus indicators. Taken at
face value it would be a vacuous confirmation, the same shape as the defect the
Track 3 review caught in the F2 fixtures.

With the surface metadata regenerated after the revert, the failure is precise:

```
6 subtests passed
SUBFAILED control='INPUT#w2-box1...' phase='incomplete'
  {'differsFromResting': False,
   'ratios': [{'component': 'box-shadow', 'ratio': 1.0165762898917061}]}
```

One control fails, it is the right control, the measured ratio is the 1.02:1 both
Track 2e evaluators reported, and the other five pass unchanged. Restoring the
fix restores the pass. **The test is non-vacuous and the invariant is computed
from rendered colours rather than a stored snapshot.**

**Note for future mutation tests on this surface:** any content-tree mutation must
be followed by `python3 -m tools.generate_entry_loop_t1_fixtures` before the
result means anything. Without it the checksum gate answers first.

## The root cause is different from the foreman's diagnosis

The foreman's Track 4 charter attributed the missing indicator to a rule modelled
per background context that never included the input. That was wrong. The global
rule already named every focusable control by element type — it was already per
control. What cancelled it was a Svelte scoped-style specificity tie: a
component-scoped `input { outline: 0; box-shadow: ... }` compiles to the same
specificity as `:global(input:focus-visible)`, and CSS breaks a tie by source
order, so the later resting rule won for the one control that declares those two
properties itself.

The builder found this and said so. The charter's *prescription* — state the rule
per control, once, so a control added later inherits it — was still the right
one, and the fix follows it: `!important` on the focus rule's outline and
box-shadow, no rule added for `#w2-box1` specifically. But the reasoning in the
charter was mistaken and is corrected here rather than left to stand.

## What is covered now

Six focusable controls, enumerated by real Tab traversal of the compiled served
page in both incomplete and complete states: the wordmark link, `Enter this
fact`, `#w2-box1`, the submit button (`Add`/`Update`, same element), `Correct
this fact`, `Review W-2 Box 1`. The `tabindex="-1"` status-card live region is
excluded as not a control. `#w2-box1` moves from 1.02:1 to **15.90:1**; the
others measure 13.85–15.64:1. The `Review W-2 Box 1` outer ring was left alone
per the charter.

## Disposition

No finding. The defect is repaired, the repair is guarded by one durable test
rather than a battery, and the numbers hold.

**No maturity movement.** The Track 2e cell verdict stays FAIL and the W-2 cell
stays at L1. Nothing re-scored the surface, so repairing the defect after the
evaluation does not move the cell — the milestone reports a failed evaluation as
a real outcome.

The surface has changed, so any future re-score is against the new starting-state
fingerprint `sha256:ac7735a5d9ab4e057e193966aec89df7534e478ee329e47e9f7b8b19018b79e8`,
superseding `sha256:212e525d…`.
