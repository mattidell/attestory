# Prototype Evaluation Analysis — Expression Language Extensions

Foreman synthesis, 2026-07-14. Advisory to the owner; the owner decides
disposition and ratifies any ADR.

## Decision under evidence

Two contract gaps in the rule expression language, both established by the
remediated conditional-selectors evidence: **ELX-P1** — a declared default
mechanism for optional scalar inputs; **ELX-P2** — first-class categorical
(string) comparison. Candidate ADR-0025.

## Evidence

Two independently authored, clean-room-separated designs of the same two
propositions and five Gate 2 cases:

- Incumbent (`it1/design.md`, `examination-it1.md`) — committed exhibit `a9e4b9c`.
- Clean-room rival (`it2/design.md`, `examination-it2.md`) — committed exhibit
  `b2b9022`. The rival attested it did not read the incumbent's outputs.

Reviewed by two independent-context committee seats:

- Governance (`reviews/round-1-governance.md`, findings ELX-G1–G6).
- Adversary (`reviews/round-1-adversary.md`, findings ELX-A1–A8).

Both reviewers passed foreman conformance (governance 110 lines, adversary 101
lines; each returns a verdict per proposition per design). Neither read the
other's output.

## Convergence under independent authorship

The two designs, authored in sealed contexts, converged on six load-bearing
principles (governance convergence section, corroborated by adversary A6–A8):
defaults are declared versioned content, not runner policy (Article 11);
asserted inputs are never overwritten (E3.1); the default value is a derived
finding, not a fabricated assertion (ADR-0009); displacement propagates through
the two existing edge kinds only, no third edge (Article 7); categorical
comparison matches exact string tokens with no decimal coercion; and
type/domain mismatch is a contained blocked disposition, not a crash (ADR-0012).
The three refuted conditional-selectors workarounds (multi-publisher staging,
closure-aggregation misuse, evaluation-order tricks) are defeated by **both**
designs (ELX-A6), as are default-then-remove reactivation (ELX-A7) and the
Case-5 non-optional-absence floor (ELX-A8).

Convergence on the shape, with divergence isolated to the mechanism, is the
strongest signal this round could produce: the shape is sound, and the choice
is a clean mechanism comparison rather than an open design question.

## Foreman triage — the decision-blocking divergences all resolve for the rival

Both reviewers, independently, carry the **rival (it2)** design forward for both
propositions and reject the incumbent's two distinctive mechanisms. I confirm
their classifications; every decision-blocking finding is a divergence that the
rival wins on governance grounds *and* on a concrete adversary counterexample:

- **D1 — ELX-P1 displacement mechanism (ELX-G1 / ELX-A1, decision-blocking).**
  The incumbent's `default_superseded` displacement root class pairs a
  derivation `symbol` to a kernel `fact_id` at runtime through mapping the
  currency layer does not hold as versioned content — ambient runner state,
  violating Article 11 (ELX-G1). It also only fires when a *kernel* finding
  becomes current, so a package upgrade that changes a default value with no
  assertion present leaves two default findings current — a multi-default
  collision breaking the single-value constraint (ELX-A1). The rival gives the
  default-resolution finding the *same* `fact_id` as the asserted finding
  (`resolved_input.fact_id`), so the existing correction fold handles
  displacement by `fact_id` equality with no new root class and no runner-
  resident mapping — and folds successive default versions correctly.
- **D2 — ELX-P1 declaration structure (ELX-G2, decision-blocking).** The
  incumbent's separate `optional-input-declaration.v1` citizen duplicates symbol
  declarations and needs package-level cross-validation to stay consistent. The
  rival declares `optional_default` directly on `fact-type.v2` (the canonical
  home for `nature` and `value_schema`), letting static schemas enforce that
  elective facts cannot default (E3.1) and that the default parameter validates
  against the fact's value schema.
- **D3 — ELX-P2 comparison contract (ELX-G4 / ELX-A3, ELX-A4, decision-
  blocking).** The incumbent's generic `match` op checks only that operands are
  strings, so `"MFJ"` vs `"married_filing_jointly"` and a legacy `"1"` vs
  `"single"` both *silently return false* — tolerant-reader behavior forbidden
  by E9.1. The rival's `categorical_compare` + typed `category_literal` resolve
  a declared common enum domain, catch mismatches statically at package
  validation (`MEMBER_SCHEMA_INVALID`) when knowable, and block honestly at
  runtime (`DEPENDENCY_INVALID`, `CATEGORICAL_DOMAIN_MISMATCH`) otherwise.
- **D4 — ELX-P2 code→label migration (ELX-G6 / ELX-A5, decision-blocking).**
  The incumbent leaves migration unspecified ("upgrades in the milestone"),
  risking silent conversion or dual-reading of the ADR-0024 interim codes. The
  rival specifies a governed, append-only pathway: a versioned code-to-label
  mapping artifact, a presented successor claim citing the old code, and an
  explicit user assertion — no human finding is silently converted (Article 2),
  and legacy code bindings are rejected rather than dual-read.

## Supported conclusions

- **C1 — ELX-P1 is settled at the static level, on the rival's mechanism.**
  A `determinable` optional scalar declares one adopted parameter default on
  `fact-type.v2`; the input resolver publishes a marked default-resolution
  derived finding sharing the input's `fact_id` only when no current assertion
  exists; a later assertion is an ordinary correction root that displaces the
  default and, through existing `input` edges, its consumers. Pins record
  `origin: assertion | declared_default` on every `input` pin.
- **C2 — ELX-P2 is settled at the static level, on the rival's mechanism.**
  A closed `categorical_compare` op with a typed `category_literal` compares two
  values of one declared string-enum domain, never as decimals; mismatch is a
  statically-caught or contained blocked disposition; ADR-0024's numeric codes
  migrate by governed successor claim.
- **C3 — the incumbent design corroborates but is superseded.** Its
  convergence on the six principles is evidence the shape is right; its two
  distinctive mechanisms (`default_superseded` root class, generic `match` op)
  are rejected by both reviewers and are not carried forward.

## Rejected alternatives

- **`default_superseded` displacement root class (incumbent).** Rejected:
  runner-resident symbol→fact mapping (Article 11) and multi-default collision
  on package upgrade (ELX-A1).
- **Separate `optional-input-declaration.v1` citizen (incumbent).** Rejected:
  duplicative and weaker static enforcement than declaring on `fact-type.v2`.
- **Generic string `match` op (incumbent).** Rejected: silent-false on invalid
  and cross-domain operands, violating E9.1 (ELX-A3/A4).
- **Unspecified milestone-time categorical migration (incumbent).** Rejected:
  admits silent conversion / dual-reading of human findings (Article 2).

## Production conditions (implementation-time, not decision-blocking)

Carried into the ADR and the eventual milestone implementation:

- **PC1 (from ELX-G3 / ELX-A2).** The `origin` field must be recorded on *every*
  `input` pin and copied transitively, so any consumer states default-vs-
  assertion provenance locally without walking the upstream tree.
- **PC2 (from ELX-G5).** `CATEGORICAL_DOMAIN_MISMATCH` is a *new* disposition
  reason; adding it (and confirming `DEPENDENCY_INVALID` covers enum-invalid
  assertions) is a change to the ADR-0012 disposition vocabulary and must be
  reflected in the disposition/explanation contracts.
- **PC3.** The rival's mechanism is paper-settled at HEAD but not executed;
  production remains conditional on mixed-family correction-fold validation for
  default-resolution findings, two-runner parity, schema/package negatives, and
  the five Gate 2 cases as synthetic fixtures (rival's own stated conditions).

## Recommendation

Ratify **ADR-0025** adopting the rival (it2) mechanisms for both ELX-P1 and
ELX-P2, with PC1–PC3 as production conditions. Gate 6's minimum converged
subset (ELX-P1 surviving the three refuted workarounds without violating
Articles 7/11) is met. No repair pass is needed; the rival is accepted outright
and the incumbent's convergence corroborates the shape.
