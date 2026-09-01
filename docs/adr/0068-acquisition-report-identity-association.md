# ADR 0068 — Acquisition-to-Report Identity Association

- Status: **accepted**
- Tier: 2 — the identity backbone supportability and rule-owned
  consequences build on; not a product-thesis or governance-meaning
  decision.
- Date: 2026-08-29

## Context

An ordinary bond-acquisition circumstance and a documentary Form
1099-INT box-1 report are entered independently, neither aware of the
other. Before any tax consequence can be computed, the engine must
establish — honestly, and without inventing authority neither side
actually carries — whether a given acquisition and a given report concern
the same real-world obligation. This is deliberately kept separate from
tax arithmetic (does the claimed amount hold up against the report),
which is a downstream, consuming question.

The acquisition side has no field a payer's own reporting system
produces; the only correlating handles are the payer's name, the tax
year, and — when the person happens to know it — the statement or account
reference printed on their own 1099-INT. A Form 1099-INT statement can
itself aggregate interest from more than one real obligation into one
box-1 figure, so even an exact statement/account match is evidence of
*which report* an acquisition's paperwork refers to, never by itself
evidence of *which obligation* within that report's total it represents.
No structural signal — a name match, a statement match, an amount match —
can stand in for the person's own knowledge of their own transaction.

## Decision

1. **A dedicated pairing record, not a repurposed collision check or a
   field on either source fact.** Association is a new, independently
   published `derived-finding.v2` instance, one-sided from the
   acquisition: the acquisition names the report(s) it corresponds to.
   There is no separate bilateral 1-1 constraint artifact — a pairing
   finding already carries both fact ids, so a second constraint artifact
   asserting uniqueness in the other direction would be redundant.
2. **Entity-kind identity, not literal enumeration — but exact string
   canonicalization, not real-world entity resolution.** The
   acquisition's payer identity uses the same entity kind Form
   1099-INT's own report already uses (`tax.us.interest-payer`); a
   dedicated `tax.us.interest-obligation` entity kind (scoped under the
   payer, disambiguated by the person's own reference or description)
   identifies the obligation itself. Fact individuation goes through the
   real kernel entity lattice, so the vocabulary admits any number of
   payers and any number of obligations per payer with no fresh content
   bundle required per instance. Payer and obligation identifiers are
   derived by one documented, deterministic convention (trim and
   concatenate) — a genuine cardinality mechanism, not a claim of
   resolved real-world identity: two spelling variants of the same real
   payer are treated as different payers, and this is a disclosed,
   deferred boundary, not attempted here.
3. **A reported statement/account reference is an ordinary, optional
   answer.** A person may know the statement or account reference printed
   on their own 1099-INT; when supplied, it is canonicalized to Form
   1099-INT's own `statement` entity kind. The acquisition-side derivation
   and a genuinely independent report-side module (zero imports of the
   acquisition-side module, with its own real report-contribution path)
   each implement the same documented canonicalization convention on
   their own side — convergence by shared, disclosed convention, never by
   one side deriving or manufacturing the other's identifier. No tax
   classification is asked; this is an ordinary fact about the person's
   own paperwork.
4. **Association is two-tiered by how the candidate report is located —
   never by whether confirmation is required.** A named statement
   reference narrows to one specific box-1 statement entity (the primary
   tier); absent one, a coarse payer+tax-year join is the fallback. At
   either tier, exact fact-id-count grouping applies: distinct
   reported-side fact ids are counted directly, never a coarser set of
   identity tuples that could silently collapse two distinct statements
   under one payer/year into a single entry. Two or more candidates, at
   either tier, always refuse `ASSOCIATION_AMBIGUOUS`, naming every
   candidate. Zero candidates: no match, silently.
5. **A single candidate, at either tier, is never associated on the
   match alone.** Association additionally requires the acquisition's
   own, separately answered `confirmed_report_match: true` — an explicit,
   accountable assertion that the claimed obligation really is
   represented in that report, scoped to the specific report identified
   at contribution time, never an inferred default and never
   substitutable by any match however specific. If the sole candidate's
   identity later changes (the confirmed report is retired and replaced
   by another), the confirmation is stale and refuses
   `ASSOCIATION_UNCONFIRMED` rather than silently retargeting onto the
   replacement. A confirmation naming no target at all is refused the
   same way, uniformly, at every vocabulary version; the current
   vocabulary version makes an untargeted confirmation unconstructible in
   the first place.
6. **One report can legitimately aggregate interest from more than one
   attested obligation.** Two acquisitions naming two genuinely different
   obligations may both attest to, and both associate with, the same
   report — a real, expected shape given how Form 1099-INT box 1 works,
   not a defect. This decision introduces no allocation policy for how a
   report's total is apportioned across the obligations attested against
   it; each attested obligation's own claimed amount participates in
   supportability and consequence dispatch as-is, with aggregate-level
   supportability across a shared report a separate, downstream concern.
7. **Correction and addition/removal re-evaluate; nothing is frozen.**
   The association is derived, not a stored, independently corrected
   object: adding a second candidate report after an association exists
   displaces it into ambiguity; removing the added report republishes the
   identical content-addressed association. A correction to either source
   fact is visible the next time the same pairing is evaluated, with no
   separate invalidation step.
8. **Provenance follows the real `pins_for` shape.** The association's
   pins name both source finding ids directly — never a payer/form-row/
   statement-name locator, and never an unpinned value field standing in
   for a pinned finding id.
9. **Tax arithmetic stays out.** This mechanism answers only "do these
   concern the same thing." Whether the accrued amount is supportable
   against the associated report is a downstream, consuming decision.

## Production conditions (owed to production implementation; never allowlisted)

- The same obligation entered twice with a mismatched amount is not
  detected by this mechanism — a named residual risk, not closed. A
  future milestone giving the ordinary-language mapper a finer
  correlating identifier could close it.
- `confirmed_report_match` has no product-surface design for how a
  person is actually asked to confirm — this repository is engine-only.
  Naming the interface contract this hands off to is separate work.
- The independent report-side contribution path has no product-surface
  document-ingestion caller in this engine-only repository; wiring an
  actual intake flow to it is separate work.
- Statement-reference canonicalization assumes the person's stated
  reference, once normalized, matches the payer's own statement
  identifier exactly; fuzzy or partial matching is not attempted.
- Multi-acquisition scale: exercise two acquisitions legitimately
  associating with two different reports under the same payer, to confirm
  the mechanism does not conflate them.

## Consequences

- Supportability and rule-owned consequences read a genuinely evidenced
  association, never a guessed one.
- A future canonical pairing between a documentary report and an ordinary
  fact repeats this pattern: a dedicated pairing record, exact fact-id
  counting, refuse on ambiguity, derive rather than cache, and reuse a
  real entity kind where the concept already exists on another side
  before introducing a new one.
- `identity_exclusivity` (`packages/derivation/runner.py`,
  `source-family.v2.schema.json`) is untouched by this decision and
  remains available for its own collision-detection use.

## Alternatives Considered

- **Invert the existing family-declared collision check
  (`identity_exclusivity`) into a cardinality check.** Rejected: this
  collapses multiple same-payer statements into one set entry, producing
  a false unique match on exactly the ambiguous case this mechanism
  exists to catch, and has no real provenance pin to the target fact.
- **A bilateral 1-1 constraint artifact alongside the pairing record.**
  Rejected as redundant: a one-sided pairing finding already names both
  fact ids.
- **Literal-kind identity keys, enumerating admissible payers/obligations
  at declaration time.** Rejected: inherently bounded cardinality: no
  enumeration strategy gives the arbitrary cardinality a real production
  vocabulary needs.
- **Auto-associate whenever exactly one candidate exists, unconditionally.**
  Rejected: "only candidate" is not evidence of "same obligation."
- **Require a statement reference always, retiring the coarse tier.**
  Rejected: many ordinary statements do not surface an account or
  reference number; the coarse tier can still handle those cases
  honestly, with an explicit accountable assertion in place of a guess.
- **Treat a statement-narrowed match as evidentially sufficient on its
  own, with no confirmation required at that tier.** Rejected: Form
  1099-INT box 1 can aggregate interest from more than one obligation and
  carries no general per-obligation instrument identifier; a match,
  however specific, proves only which report an acquisition's paperwork
  refers to, never which obligation within that report's aggregate it
  represents.
- **Require a stronger source identifier (an account/CUSIP field)
  instead of attestation.** Rejected: Form 1099-INT box 1 carries no
  general per-obligation instrument identifier to require.
