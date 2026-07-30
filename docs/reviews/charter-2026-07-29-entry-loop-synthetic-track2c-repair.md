# Charter — The Entry Loop (synthetic), Track 2c: repair the evaluated defects

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Against: `docs/reviews/2026-07-29-entry-loop-synthetic-track2-aggregation.md` (cell FAIL)
- **No review gate.** The owner accepted this repair without one. Verification
  still applies, and a re-score follows.

## What failed and why it matters

Track 2 scored the surface against the owner-accepted criteria with two
independent evaluators. Eighteen of twenty rows passed unanimously. Two did
not, and the accessibility row failed the cell.

The defects are narrow. **Do not treat that as permission to patch literals.**
The owner's standing direction for this work is that findings have to survive
future milestones: this UI may well end up being thrown away, and a fix that
lives in one hex value on one region dies with it. Where a fix can be made once
in a way that holds for surfaces that do not exist yet, make it there.

## D1 — focus indicators and control boundaries

Two measured misses, both against a required 3:1:

- the focus ring on "Review W-2 Box 1" measures **1.25:1** against the
  dark-green completion region;
- `#w2-box1` has no border or box-shadow, and its fill measures **1.02:1**
  against the card behind it, so the control has no visible boundary at all.

**The interesting part is why.** The focus ring almost certainly has a single
colour chosen against the light regions, and the completion region later became
dark without that ring being rechecked against it. That is not a bad colour
choice. It is a surface with no declared relationship between *the contexts a
control can sit on* and *the indicators that must remain visible on all of
them*.

So fix it that way. Make the focus indicator and the control boundary hold at
3:1 **against every background context the surface can put them on**, not just
against the one that failed. If that means the indicator carries its own
contrast rather than depending on what is behind it — a two-tone ring, an
outline plus offset, whatever the mechanism — that is the better answer,
because it stays true when someone adds a sixth region colour next milestone.

Name the contexts you found. If there are five region backgrounds and one focus
treatment, say so; that count is the finding.

## D2 — the accepted input format is stated in three places and they disagree

Evaluator B typed `90,000` into a field prefixed with `$` and got a generic
rejection with no format-specific correction.

The criterion this bears on is Disputed and **the owner's resolution is still
outstanding**, so do not treat this as a scored fix. Do it anyway, because it
is a defect independent of the dispute: the accepted format is currently
expressed three separate times — in the hint text a person reads, in the
validator that accepts or rejects, and in the error message shown on rejection
— and those three statements are not derived from each other. That is why a
person can read the hint, comply with it in good faith, and be refused without
being told what was wrong.

Close it by making the format **one declaration** that the hint, the validation,
and the rejection message all derive from. Then either the declaration accepts
comma grouping or it does not, but a person cannot be told one thing and judged
by another.

State which you chose and why. Silently normalising input and loudly refusing it
are both defensible; having the field imply one and do the other is not.

## What to record for Track 3

Track 3 writes the model this milestone's build was supposed to reveal, and
these two defects are evidence about what it has to carry. Write a short note —
not a design, not an ADR — saying what a specification would have needed to
declare in order to make each of these defects impossible rather than
detectable:

- for D1, what a presentation model needs to know about surface contexts and
  the indicators that must survive them;
- for D2, what an entry field needs to declare about its own accepted format so
  that guidance, validation, and refusal cannot drift apart.

Keep it to what you actually learned from fixing them. Track 3 does the
modelling; you are supplying the evidence it works from.

## Boundaries

- D1 and D2 only. If you find a third defect, report it.
- **Do not touch the criteria document.** It is owner-accepted, it caught these,
  and a failed evaluation is a real outcome. Nothing here adjusts the bar.
- Do not score anything, do not re-score, do not predict the re-score.
- Do not restructure the surface, rewrite the page, or start building the model
  itself. That is Track 3's, and doing it here would preempt an owner decision
  that has not been made.
- W-2 only, synthetic only, no residency locator anywhere.
- No maturity movement.

## Verification

The CI `verify` sequence or a stated subset with each omission justified, the
data-safety scan, and the commit you worked from, in the commit message. There
is no review gate on this repair, so the verification record is the whole of
what a later reader gets. Measure the contrast ratios you changed and put the
numbers in your report — before and after, per context.

Orient with `python3 tools/build_orientation_block.py --ref HEAD`. No `.venv`;
use system `python3`. Ratified line `origin/main-ui`.

You can stand the surface up with:

```sh
python3 -m packages.derivation.runners.entry_loop_evaluation
```

## Report back

The measured contrast ratios before and after, per context, for both the focus
indicator and the control boundary; how many background contexts the surface
has and whether one treatment now covers all of them; what the format
declaration is and which behaviour you chose for comma grouping; and the note
for Track 3.
