# Track 2 aggregation — The Entry Loop (synthetic)

- Aggregated by: **Foreman**, 2026-07-29
- Procedure: `docs/phases/legible-entry/entry-usability-criteria.md`, Scoring Procedure
- Evaluator A (Builder brief): `docs/reviews/2026-07-29-entry-loop-synthetic-track2-evaluator-a.md` (`cf62ad7`)
- Evaluator B (Reviewer brief): `docs/reviews/2026-07-29-entry-loop-synthetic-track2-evaluator-b.md` (`4bfd71c`)
- Surface under evaluation: `packages/derivation/runners/entry_loop_evaluation.py`, starting-state fingerprint `sha256:7d5abe2e…`

## Cell verdict: **FAIL**

The W-2 column of the entry-loop matrix does not move to L2.

Both evaluators ran against the same starting-state fingerprint. Both filed
twenty rows, Pass or Fail, with no third value. Neither read the other's file.
Eighteen rows are Pass/Pass. Two are splits.

| Criterion | A | B | Aggregate | Effect on the cell |
| --- | --- | --- | --- | --- |
| Carries over: Accessibility baseline (mechanical) | Fail | Pass | **Disputed** | **Fails the cell** (rule 4) |
| 2.3 — a person can state the accepted format without guessing (judgement) | Pass | Fail | **Disputed** | Does not fail the cell; escalates to the owner (rule 5) |
| All eighteen others | Pass | Pass | Pass | — |

Rule 3 requires every mechanical criterion to be Pass/Pass. Rule 4 makes a
disputed mechanical criterion fail the cell. The accessibility row does both,
so the cell fails on that row alone, independently of how the owner resolves
the judgement dispute.

## The accessibility split is coverage, not contradiction

This is the part the owner should see before reading the two files as
disagreeing about a fact.

The criterion bundles five requirements into one row: text contrast, non-text
contrast for control boundaries and focus indicators, landmarks, keyboard
reachability, and focus visibility. Both evaluators measured from live computed
styles rather than by eye. They did not measure the same elements.

- **What both measured and agreed on:** one `main` landmark, one named `form`
  landmark, full Tab/Shift+Tab reachability with no trap, standard-key
  operability, an explicit `:focus-visible` rule, and text contrast comfortably
  above 4.5:1 (A's minimum 5.98:1, B's range 5.53–15.64:1).
- **What only A measured:** the focus ring on the "Review W-2 Box 1" control
  against the dark-green completion region — **1.25:1**, against a required
  3:1 — and the `#w2-box1` input's own boundary, which has no border or
  box-shadow, its fill measuring **1.02:1** against the card behind it, against
  a required 3:1 for a visible control boundary.

B measured a focus outline at 5.53:1, but on a control in the light region, and
did not separately measure the input's boundary. B's own file says it is not
claiming exhaustive coverage.

So A found two specific non-text contrast failures, and B did not look at those
two places. Nothing in B's file contradicts A's measurements. The procedure
still records this as Disputed, correctly — it scores what evaluators filed,
not what a third party thinks they would have filed had they looked. But the
underlying defect looks real rather than contested, and the repair is the same
either way.

## Escalated to the owner: criterion 2.3 (judgement)

Rule 5 sends a disputed judgement criterion to the owner with both rationales,
without failing the cell. Both are given in full in the evaluators' files;
in short:

**A scored Pass.** The field carries the text "Enter dollars and cents, for
example 90000 or 90000.50." The format is stated before typing.

**B scored Fail.** B typed `90,000` — a plausible good-faith format for a
dollar field carrying a `$` prefix — and it was rejected with a generic error
carrying no format-specific correction. B's reading: examples that do not rule
out a conventional alternative leave a person guessing, and this person guessed
and was punished for it, which is exactly the condition the criterion's
"without guessing" bar exists to catch.

B also filed a note that it considers 2.3 close to unscoreable in the strict
sense for any free-text numeric field, since no finite set of examples rules
out every plausible alternative, and says it scored against concrete evidence
rather than a demand for exhaustive format documentation.

**Foreman's recommendation: resolve for B.** A's rationale establishes that a
hint exists; B's establishes that the hint was insufficient in practice, on
evidence rather than on theory. Between "the surface says something about
format" and "a reasonable input was rejected without telling the person why,"
the second is the stronger evidence about what a person can state without
guessing. This is a recommendation, not a resolution — rule 5 makes it the
owner's.

## Owner resolution of criterion 2.3, 2026-07-29: **Pass**

The owner resolved the escalated judgement criterion for A, on reasoning that
neither evaluator put forward:

The criterion asks whether a person **can** state the format without guessing.
It does not ask whether the surface **must** state every accepted and refused
form exhaustively. The hint gives examples without commas or a currency symbol,
and commas and currency symbols are conventionally accepted in dollar fields —
so the hint reads as covering both, and a person has enough knowledge not to
need to guess. Criterion 2.3 is satisfied.

**What B found is real, and it is not 2.3.** B's evidence stands: `90,000` was
refused. On the owner's reading, that is a defect in *validation*, not in
guidance — the hint licensed a format the validator then refused. The
resolution is therefore not "B was wrong" but "B's finding belongs to a
criterion the instrument does not currently have."

**Consequence for the product:** both formats should be accepted. The accepted
set must be at least as wide as what the guidance licenses.

**Finding against the instrument, for Track 3.** The criteria conflate two
distinct requirements under one "without guessing" bar:

1. **Knowledge sufficiency** — a person has enough information to state a
   correct answer. This is what 2.3 measures, and it passes.
2. **Guidance/behaviour congruence** — the system honours what its own guidance
   licensed. Nothing in the instrument measures this, which is why a real defect
   surfaced only as a disputed judgement call.

The next version of the instrument should separate them, and (2) is mechanical
where (1) is judgement. The criteria are **not** amended for this evaluation;
they are owner-accepted and fixed for it.

## What this does not do

- No maturity cell moves. The milestone plan says a failed evaluation is a real
  outcome the milestone reports, and that a repair cycle is acceptable while
  rewriting the bar is not. The criteria are not amended.
- The two evaluator files stand as filed. Neither is corrected.
- Track 1's `READY` is unaffected. This is a usability result, not a
  correctness one.

## What would close it

Three concrete changes, all in the surface:

1. Raise the focus indicator's contrast to at least 3:1 in the dark-green
   completion region.
2. Give `#w2-box1` a visible boundary at 3:1 or better against its card.
3. If the owner resolves 2.3 for B: either state what is not accepted, or
   normalise conventional input such as comma grouping rather than rejecting
   it.

Then re-score. The eighteen unanimous rows do not need re-running; the rows
touched by these changes do — 2.1, 2.2, 2.3, and the accessibility baseline —
with two fresh evaluators under the same two briefs, since both current
evaluators now know the surface.

## Note for Track 3, on the instrument rather than the surface

The accessibility row bundles five requirements into a single Pass/Fail. Two
narrow CSS defects therefore sink a row that is otherwise comfortably met, and
the two evaluators' differing coverage of that row produced a split that reads
as disagreement when it is not. That is the bar behaving as written, and the
bar was owner-accepted before the surface existed, which is why it caught a
1.25:1 focus ring at all. But the granularity is worth recording as an observed
property of the instrument rather than leaving the next milestone to rediscover
it.
