# Charter — The Entry Loop (synthetic), Track 2d: make the format declaration honour itself

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Following: Track 2c (`Repair entry loop contrast and format drift`)
- **No review gate**, on the same owner acceptance as 2c.

## Where 2c got to

The contrast work landed and is good: focus 1.25 → 7.59, control boundary
1.02 → 13.85, held across six named contexts rather than patched on the one
that failed.

The format work is half done, and the missing half is the interesting one.

`packages/sample_data/entry_loop_t1/surface/content/app/src/w2-box1-format.js`
now declares the format once, and `packages/derivation/entry_loop.py` reads that
same declaration rather than restating it — so the hint a person reads, the
rejection message, and the validator all derive from one source. That is the
right shape and it is what was asked for.

But the declaration currently says `"commaGrouping": "refused"`, and the
acceptance path only implements the refusing branch. `_parse_box1_with_format`
rejects a value containing a comma when the declaration refuses commas, and
otherwise hands the raw string to `Decimal(...)` — which fails on `90,000`
anyway. So flipping the flag to `"accepted"` today would produce a hint reading
"with comma grouping" over a validator that still refuses commas.

That is the same drift the repair set out to remove, pointing the other way. A
declaration that only governs the wording is not yet a declaration that governs
behaviour.

## The owner's decision

Criterion 2.3 resolved **Pass**: the hint gives a person enough to state a
correct answer without guessing. But the hint's examples do not rule out commas
or a currency symbol, and those are conventional in a dollar field — so the
accepted set has to be at least as wide as what the guidance licenses.

**Accept both forms.** Change the declaration to accept comma grouping, and
make the acceptance path actually implement it by normalising rather than
refusing. A leading currency symbol should be accepted on the same reasoning —
the field renders a `$` prefix, so typing `$` is a form the surface itself
invites.

## What to build

1. The declaration expresses what is accepted, including comma grouping and a
   currency symbol, and remains the single source the hint, the error, and the
   validator all derive from.
2. The acceptance path implements every form the declaration accepts, by
   normalising input to a canonical value before parsing.
3. Refusal still refuses. Normalising `90,000` must not become "accept anything
   vaguely numeric" — `9,0,0` and `$$90000` and `90,00.5` are still invalid, and
   the existing fail-closed behaviour and redaction are unchanged. The seven
   adversarial regressions from the Track 1 repair must all still pass, and if
   any needs changing to accommodate this, stop and report rather than
   adjusting it.
4. A regression that fails if the declaration and the acceptance behaviour ever
   drift apart again — that the validator accepts exactly the forms the
   declaration says it does. This is the durable part; the rest is a bug fix.

## Boundaries

- Format only. The contrast work is done; do not revisit it.
- Do not touch the criteria document.
- Do not score or re-score anything.
- Do not generalise this into the field-contract model. That is Track 3, and it
  is scoped to the field contract only by owner decision — the presentation
  model waits for a second surface to generalise from.
- W-2 only, synthetic only, no residency locator anywhere.

## Verification, and a note about it

**Record the verification in the commit message.** Track 2c did not — its
message is a single subject line. The foreman re-ran it independently and it
was clean (712 passed, mypy clean on 135 files, governance lint conformant,
envelope scan clean over `200dffe..HEAD`), so nothing is wrong with the work.
But there is no review gate on these repairs, which means the commit message is
the entire record a later reader gets, and this one records nothing.

The CI `verify` sequence or a stated subset with each omission justified, the
data-safety scan, and the commit you worked from.

Orient with `python3 tools/build_orientation_block.py --ref HEAD`. No `.venv`;
use system `python3`. Stand the surface up with
`python3 -m packages.derivation.runners.entry_loop_evaluation`.

## Report back

What the declaration now says; how normalisation works and where it happens;
which invalid forms you confirmed are still refused; how the anti-drift
regression would fail if someone changed the declaration without changing the
validator; and whether reading a JS declaration from Python is a seam worth
naming for Track 3.
