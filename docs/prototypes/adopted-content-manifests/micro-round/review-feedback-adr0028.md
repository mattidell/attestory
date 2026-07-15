# Review Feedback — ADR-0028 decision 7 (owner-requested foreman review, 2026-07-15)

Status: **ADR-0028 is not ratification-ready as drafted.** One decision-blocking
finding on **decision 7** (the broadened structural force-declare). The rest of
the micro-round — the split from ADR-0027, the it2 rejection, the it1 MR-P1
resolution, and the judgment to side with the adversary over governance on it1
MR-P2 — is sound and faithful to the reviews. This note is feedback for the
foreman to resolve before ADR-0028 goes to the owner for ratification.

## Finding — decision 7 fixes a proven under-trigger with an un-tested over-trigger

**What MR-A7 proved (real, keep the fix's intent):** it1's family-subtotal-only
force-declare *under*-fires — a line-2b computed as a raw `add(ELX(box1),
ELX(box3), ELX(oid))` that bypasses the family/mapping machinery escapes the
trigger and validates as a bare sum. That hole is genuine and must be closed.

**What the fix did (the problem):** ADR-0028 decision 7 broadens the trigger to
fire when a computation "aggregates two or more distinct adopted inputs that are
`authorizes_subtotal` values **or otherwise composition-shaped multi-source
folds … (including multi-input aggregations that omit family pins)**."

That parenthetical **over-fires on ordinary downstream arithmetic** — which is
this milestone's very next implementation work:

- Line 9 (total income) = line 1a + line 2b
- Line 11 (AGI), line 15 (taxable income) = line 11 − line 12, line 16 (tax)

Line 9 is "a multi-input aggregation that omits family pins" of two distinct
adopted inputs → under a literal read of decision 7 it must appear in
`composition_obligations` → then decision 6 requires a composition citizen +
slot bijection it has no business having → **the validator rejects a valid
package**, or forces spurious composition citizens on every arithmetic line.

**Why the round missed it:** the over-trigger direction was never tested. MR-A7
pushed only toward *more* inclusion ("no multi-source publishing path validates
without composition license"); governance read the family-subtotal trigger as
adequate (MR-P2 case 7 "valid") and didn't probe either boundary. No seat
constructed the line-9 case.

**Communication assessment (2026-07-15).** The drafting foreman *mentioned* the
broadening and offered a repair exhibit — but conditioned it on the owner judging
whether the broadening "feels out-of-evidence," and otherwise defaulted the
recommendation toward ratification. **That is a communication miss, not adequate
surfacing.** Mentioning a risk is not the same as communicating it. Two problems:

1. **It offloads an un-evaluable judgment onto the owner.** Whether a fix is
   "out-of-evidence" is a technical call about what the round's evidence supports
   — precisely what the foreman exists to assess and the owner is not positioned
   to. Punting it to the owner defaults to permissive.
2. **It defaults the wrong way.** A fix that is foreman-authored and never
   builder-tested or reviewer-checked should default to *more review*, with the
   foreman **proactively recommending** a confirmation pass — not to
   ratification-unless-the-owner-objects.

The conservative disposition is the foreman's obligation: when you author a
patch to close an adversary finding, recommend the scoped confirmation pass by
default and tell the owner the specific thing it must test — do not make further
review contingent on the owner detecting a problem the owner cannot see. The
finding below stands in full: **decision 7 is not ratification-ready; the default
is further review.** (An earlier version of this note softened this to a mere
"framing" nuance; that softening was wrong.)

**The missing distinction (the actual fix target):** ADR-0026 "composition" means
coextensiveness over the **sources of one quantity** (all taxable-interest
sources → line 2b). Ordinary arithmetic aggregates **distinct quantities**
(wages + interest → total income). A structural "≥2 adopted inputs" net can't
see that line, so it can only under-fire (miss A7) or over-fire (catch line 9).
The trigger must key on *same-quantity source aggregation*, not input count.

## Recommended resolution (small; no full builder round)

1. **Retype the decision-7 trigger to same-quantity source aggregation.** Fire
   when a published symbol `S` aggregates ≥2 adopted inputs that are *alternative
   sources / subtotals of `S`'s own tax quantity* — source-family
   `authorizes_subtotal` values **or** raw source amounts of that same quantity —
   **not** any ≥2 distinct adopted inputs. This still catches MR-A7's raw-amount
   line 2b while exempting line 9's cross-quantity sum.
2. **Add the negative golden to PC1:** line 9 = line 1a + line 2b **validates
   without** a `composition_obligations` entry. Current PC1 goldens test only the
   reject direction; the over-trigger boundary is untested.
3. **One scoped confirmation pass before ratification.** Because decision 7 is a
   *mandatory-reject validator rule fixed post-committee with no re-test*, a
   single adversary seat scoped to the trigger boundary in **both** directions
   (A7 raw-sum still caught; lines 9/11/15/16 not caught) is cheap insurance —
   far smaller than a builder round. Update decision 7 first, then this pass
   confirms the retyped trigger.

## Not in scope of this finding (confirmed sound)

- The split (ADR-0027 floor ratified; residual round on N1/N2 only) — correct.
- it2 reject on both propositions (MR-G1–G4; MR-A2/A3/A6/A10/A11) — faithful.
- it1 MR-P1 dual fact surface + A4 orphan-pin closure (decisions 1–4, PC2) —
  sound; siding with the adversary's A4 production condition is right.
- The non-circular obligation *discoverability* mechanism (decision 5–6) — sound;
  only decision 7's *structural net* over-fires.
