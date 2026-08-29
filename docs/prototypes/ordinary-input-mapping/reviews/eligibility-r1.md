# Eligibility review, round 1 — Seam 6 (Ordinary input mapping)

Reviewer: eligibility seat (process/economics only; correctness is covered by
the clean-room and adversarial seats). Read: `PROJECT_PLANNING.md` §Frontier
Reduction and Direct-Build Routing, the milestone plan's Seam 1/2/6 sections,
`docs/prototypes/ordinary-input-mapping/charter.md`, `examination.md`, and
`packages/tax/obligation_acquisition_mapping.py` /
`tests/test_obligation_acquisition_translation.py` (skimmed for size/scope,
not correctness).

## 1. Routing check — Qualified yes

The milestone plan pre-designates Seam 6 as no-rival at the plan level
("A seam with no genuine second stance (Seam 4, and Seam 6 per the guidance
below) may skip the rival"), so the charter did not invent this routing
unilaterally; it inherited a milestone-level call.

The charter's stated justification ("an accepted contract already fixes the
proposition, producer, consumer, and correction behavior; the change is
additive and reversible") turned out to be built on a false premise: the
target files did not exist, so this was a first build, not a repair. That
premise mismatch is a documentation defect the examination discloses
honestly, but the charter itself was never revised to say "first build," and
the loop's step 1 says the charter is revised when scope changes. Framing
this as "repair" understates what happened and should have triggered at
least a one-line charter amendment when the builder discovered it, even
though I do not think it changes the routing conclusion (see below).

On substance, direct-build still holds. What was actually built does not
select among materially different production representations:

- The ordinary-answers schema and the five-field circumstance-fact shape are
  bounded, reversible content decisions (which ordinary questions to ask,
  which fields to carry) — not the kind of durable identity/schema/lifecycle
  fork the routing table reserves for frontier reduction.
- The one place a real architectural fork exists — kernel identity-key kind
  — is genuine: `fact-type.v1` supports exactly two kinds, `"entity"` and
  `"literal"` (`packages/schemas/kernel/fact-type.v1.schema.json`), and this
  seam's `build_obligation_acquisition_bundle` picks `"literal"`, enumerating
  the exact payer/reference/tax-year the person supplied. That is the same
  fork Seam 2 (identity association) and Seam 1 are actively working out for
  production ("richer, entity-keyed vocabulary" per the examination).
  However, the module does not present this as a production choice: it is
  scoped to one synthetic instance per test run (a fresh bundle per
  payer/reference/tax-year, not a reusable declaration), it is named
  `demo.vocabulary.*`, and both the module docstring and the examination say
  explicitly that a later integration is expected to replace it. That
  combination — real fork, but declared disposable and non-generalizing
  rather than asserted as the answer — is what keeps it a test convenience
  rather than a load-bearing architectural decision in disguise. A fixture
  that quietly generalized (e.g., were referenced elsewhere, or shaped the
  finding's `value` schema around the `"literal"` choice) would not have
  passed this test; this one does not carry that risk, because the emitted
  `finding.value` (see Q3) is agnostic to which identity-key kind eventually
  wins.

So: the charter's own reasoning was stated on a premise the builder found to
be false, but the actual work performed still lands inside the direct-build
cell of the routing table, and the one candidate fork (literal vs. entity
identity keys) is honestly named and kept non-committing rather than smuggled
through.

## 2. Proportionality — Yes

420 lines of implementation plus 292 lines of test for: a closed JSON Schema
over six fields, a question-surface constant, fact-id derivation, the
finding-shape mapper, a fixture-bundle builder, and a thin pass-through to
the real contribution boundary. Each of the charter's five requirements has
a corresponding code path and a corresponding named test class
(`TestSubjectAndScope`, `TestStructuralClosure`, `TestIdentity`,
`TestContributionAdmissionValidatesOutput`). Nothing here builds persistence,
a UI, multiple circumstances, or speculative generality beyond the one named
circumstance the charter scopes. Not over-built; not thin enough to leave a
requirement unproven (the admission-boundary tests specifically prove a
negative case — a tampered evidence mismatch is still rejected — which is
the right amount of proof for "contribution admission validates its
output," not a rubber-stamped happy path).

## 3. Minimum acceptable floor — Yes, with the caveat named above

The examination's claim that this seam left the canonical identity/
association shape to Seams 1/2/5 is verifiable and holds for the parts that
matter to a consumer:

- `map_ordinary_acquisition_answers`'s emitted `value` (`obligation:
  {payer_name, description, reference}`, `acquisition_date`,
  `accrued_interest_paid_to_seller`, `currency`, `tax_year`) names only raw,
  descriptive ordinary quantities. It does not embed a foreign key, an
  entity reference, or any structure that presupposes which of Seam 2's
  three rival association mechanisms (generic family-declared association,
  a dedicated translation/association artifact, an existing rule-owned
  relationship) wins. Any of the three could consume these same fields to
  attempt a match. This part of the claim checks out.
- `derive_obligation_acquisition_fact_id`'s docstring explicitly defers
  ambiguity resolution to Seam 2 ("this function only names what it was
  given") — consistent with T8's assignment to Seam 2/3, not Seam 6.
- The one place the claim is weaker is the identity-*key kind* used to admit
  the fact into the lattice at all (`"literal"` vs `"entity"`, discussed in
  Q1). This is a real, not merely presentational, fork that Seam 1/2 have
  not yet resolved. The examination names this honestly as a "scoped
  simplification" rather than hiding it, which is why I still answer "yes":
  the floor is met because the dependency is flagged, not because it does
  not exist. It would not meet the floor if the fixture were left unflagged
  or if it shaped the finding's public value schema — it does not.

## 4. Production-adoption eligibility — Needs an explicit boundary before adoption

The mapper logic (`map_ordinary_acquisition_answers`,
`build_ordinary_acquisition_contribution`, `contribute_ordinary_acquisition`,
`validate_ordinary_answers`) is eligible to map directly to a production
module once Seams 1/2/5 close, citing this charter and the committee's
disposition — nothing in it needs a rival architecture comparison.

`build_obligation_acquisition_bundle` is not eligible to ship as-is. It is a
test fixture whose only purpose is proving the real admission boundary is
exercised, not a producible vocabulary declaration (it enumerates one
instance's literal values per call and cannot represent a second
obligation from the same payer without a fresh bundle). Neither the charter
nor the examination states this as a hard boundary in so many words — the
examination says a "later integration is expected to adopt" a different
vocabulary, which is a prediction, not a constraint. Before this artifact is
cited as production-adoption evidence, the milestone record should say
explicitly: *the literal-identity fixture bundle does not ship; only the
mapper and its finding shape do; the production fact-type/bundle declaration
is Seam 1/2's output, not Seam 6's.*

## Overall recommendation

**Ship with named conditions.** The routing was substantively correct and
the artifact is proportionate and honestly scoped. Conditions before this is
cited as production-adoption evidence or merged toward production:

1. Amend the charter (or record in the milestone disposition) that this was
   a first build, not a repair — a one-line correction, not a re-scope.
2. State explicitly, in the examination or the milestone's production-
   adoption record, that `build_obligation_acquisition_bundle` (the
   literal-identity fixture) does not ship to production; only
   `map_ordinary_acquisition_answers`, `validate_ordinary_answers`,
   `build_ordinary_acquisition_contribution`, and
   `contribute_ordinary_acquisition` are production-adoption candidates,
   contingent on Seam 1/2's identity-key kind selection.

No Gate 1 reopening is needed: the one real fork in this build (literal vs.
entity identity keys) is already the fork Seams 1/2 are chartered to resolve,
and this seam did not decide it — it worked around it transparently.
