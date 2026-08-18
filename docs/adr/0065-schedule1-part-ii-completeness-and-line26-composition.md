# ADR 0065 — Schedule 1 Part II Completeness and Line-26 Composition

- Status: **accepted** (Track 4 of `f1098e-student-loan-interest-agi`)
- Tier: 2 — contract/architecture choice for schema shape and evaluator behavior.
- Date: 2026-08-16

*(Note: Re-numbering this ADR at merge time is expected and acceptable practice in this repository due to concurrent unmerged work.)*

## Context

Form 1040 Schedule 1 line 26 requires the addition of lines 11 through 23 and 25. For the Form 1098-E route, completeness must be asserted over this entire Part II universe to honestly compute the line-26 total, even though this route only produces a present value for line 21.

## Decision

1. **Mixed-Shape Composition.** The required universe for Schedule 1 line 26 is explicitly composed of:
   - The twelve existing Schedule-1-native absence facts (e.g., lines 11-20, 23, 25), each contributing $0 when "yes".
   - Line 21, which is a genuinely computed, present value.
   - Line 22, which is a structural $0 requiring no fact at all (the printed form has no entry box for it).
2. **First Application of Mixed Composition.** This ratifies the first application of ADR-0016 decision 4 ("a broader result may consume a subtotal when the required universe is identical or an explicit composition is established as coextensive") to a *mixed* absent/present/structural-zero total, rather than a uniformly absence-shaped one.
3. **Honesty Mechanism.** Implemented by `tax.us.2025.rule.schedule1-line26` (`packages/content/tax/2025/rule.schedule1-line26.json`). The `SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE` block disposition fires if any of the twelve absence facts answers "no" (meaning the return has an unaccounted-for adjustment). This ensures the composition never silently underweights an unaccounted-for adjustment.
4. **Order Independence.** Track 6b's `collect_categorical_all_equal` repair provides the supporting evidence that the eligibility-gathering substrate this composition depends on is now order-independent.

## Consequences

- This is now the corpus's first precedent for a *mixed* absent/present/
  structural-zero composition under ADR-0016 decision 4, not just a
  uniformly absence-shaped one. Any future milestone that adds a rule
  producing a genuinely present value for one of the twelve currently
  absence-only Schedule 1 Part II lines (e.g. lines 11-20, 23, or 25)
  must retire or restructure this composition's assumption that those
  lines are absence-only — that line moves from the "twelve absence
  facts, each contributing $0 when 'yes'" bucket to the "genuinely
  computed, present value" bucket line 21 already occupies, and
  `rule.schedule1-line26.json` must be revised accordingly, not silently
  left reading a now-stale absence fact for that line.
- The `SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE` disposition block is a
  standing constraint on this route's bounded class: it is what makes
  the composition honest today, and it must keep firing (or be
  explicitly re-derived) for as long as any of the twelve lines remains
  absence-only. It cannot be dropped or narrowed without re-examining
  every line it currently guards.
- Line 22's treatment as a structural $0 requiring no fact at all is now
  a citable precedent for "no entry box on the printed form" as a third
  composition shape, distinct from both "asserted absent" and
  "genuinely computed." A future line with the same printed-form
  property can reuse this shape without re-arguing it, but a line that
  merely has *no rule yet* (as opposed to no entry box) may not
  silently borrow this treatment.
- Because Track 6b's `collect_categorical_all_equal` repair is what makes
  the twelve-fact eligibility-gathering substrate order-independent, this
  composition's honesty is coupled to that repair holding; a future
  change to `marshal.py`'s disagreement guard or to the twelve absence
  facts' own gathering shape must re-verify this composition's fixtures,
  not just the eligibility-gathering tests in isolation.

## Alternatives considered

- **Mint a fourteenth Schedule-1-native absence-style fact for line 21**
  (matching the twelve existing absence facts' shape) instead of treating
  it as a genuinely present, computed value. Rejected: T0-6 already
  settled that line 21 is computed, not absent, for any filer who
  reaches the Student Loan Interest Deduction Worksheet with a nonzero
  result; forcing it into the absence-fact shape would misrepresent a
  present value as a "did you have this adjustment" yes/no answer and
  would require a second, parallel present-value pathway to actually
  carry the dollar amount — strictly more machinery than the mixed
  composition this ADR ratifies.
- **Scope the honesty block to only the twelve absence facts and treat
  line 22 as silently included in the total without a structural
  argument for why it needs no fact.** Rejected: leaving line 22
  unaccounted-for in the composition's stated universe, even though its
  $0 contribution is correct, would be dishonest completeness under
  ADR-0016 decision 4's own standard (an explicit composition must be
  established as coextensive with the required universe, not merely
  produce the right number by coincidence) and under decision 5's
  "closure...does not authorize...silent broader completion" precedent.
  This ADR's Decision 1 states line 22's structural-zero rationale (no
  printed entry box) explicitly instead.
- **Treat the composition as a uniform absence-shaped subtotal** (the
  same shape ADR-0016 originally ratified for Form 1099-INT box-1) by
  pretending line 21 and line 22 are additional absence facts. Rejected
  for the same reason as the fourteenth-fact alternative above: it would
  require line 21's real dollar amount to be smuggled in through an
  absence-fact "yes/no" answer, which is not what that fact shape means.

## Links

- Track charter: milestone plan
  `docs/phases/engine-breadth/milestones/f1098e-student-loan-interest-agi.md`,
  "## Tracks", Track 4 (Schedule 1 line-26 composition) and Track 4b
  (itemization-tie-out repair, unaffected by this composition).
- Composition authority: ADR-0016 decisions 4 and 5 (subtotal consumption
  by a broader result requires an identical or explicitly coextensive
  required universe; closure of one family does not authorize a broader
  silent completion).
- Prior settlement: T0-6 (Schedule 1 Part II completeness and line 21
  against the thirteen-fact absence population, milestone plan Track 0).
- Order-independence dependency: ADR-0064 (this ADR's `## Decision` point
  4 depends on ADR-0064's `collect_categorical_all_equal` op and Track
  6b's `marshal.py` disagreement guard).
- Content: `packages/content/tax/2025/rule.schedule1-line26.json`.
- Fixtures: Track 4's and Track 6's Schedule 1 line-26 tests (single-
  statement arithmetic unchanged; ten synthetic disposition-path models
  in `tests/test_f1098e_student_loan_interest_agi_track6.py`).
