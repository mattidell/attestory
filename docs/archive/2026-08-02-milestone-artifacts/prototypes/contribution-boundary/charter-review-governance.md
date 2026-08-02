# Charter: Round 1 Committee — Governance Reviewer (D2)

Date: 2026-07-16. Topic D2, First Real Return Slice. Reviews both builds:
`it1/design.md` + `examination-it1.md` (incumbent), `it2/design.md` +
`examination-it2.md` (rival). Independent context; you do not see the adversary
reviewer's in-progress work.

- **Seat:** Governance reviewer, Medium tier.
- **Mandate:** conformance, not preference. Judge both designs against the
  committed contracts; do not redesign. Report findings classified
  decision-blocking or not.

## Read

Topic `plan.md`, both charters, both builds, `docs/governance/` (Articles 7
supersession, 10 declaration, 12 contract/lineage, 14 record), ADR-0023 (member
assertion and transition boundaries), ADR-0010/0017 (the two-edge doctrine and
horizons), ADR-0031 (D1 residency — consumed here), and the committed
`packages/kernel/` and `packages/derivation/` schemas.

## Measure

1. **Contribution as a declared citizen (Article 10).** Are the new citizens
   (`act-contribution`, `contribution`/`contribution-record`, `finding.v2`)
   declared before instances, with no committed schema version edited (new
   versions only)? Confirm schema-as-canon.
2. **Provenance linkage (Article 12) — divergence.** The incumbent pins
   contribution `{id,version}` + document `{id,version}` on the finding and adds a
   standalone `contribution-record`; the rival chains finding → contribution →
   evidence → admitting act, with document-"version" = the immutable evidence id
   and consistency enforced at admission (the contribution's `evidence_id` must
   appear in the finding's `evidence_ids`). Which conforms better to Article 12's
   pinned-lineage requirement and the existing evidence model? State the
   conformance condition.
3. **Provenance is not a standing edge (ADR-0010/0017, Article 7).** Both make the
   contribution pin provenance-only, creating no third edge; the rival argues
   contributions are unsupersedable so no displacement can originate there.
   Confirm this holds the two-edge doctrine — or find where a contribution pin
   could affect standing.
4. **Correction by supersession (Article 7, ADR-0023).** A corrected value is a
   new contribution routed through ordinary assertion; confirm the family horizon
   does **not** advance (closure authority survives a value correction), both
   findings stay on the record, and there is no edit/withdrawal/third mechanism.
5. **Runs-consume-facts (Article 13/14).** Is a run structurally unable to consume
   a raw contribution input — the run request/context carries no value-bearing
   member — with any missing current finding producing a recorded block, never a
   silent read?
6. **D1 interlock (Case 5, ADR-0031).** Do contribution artifacts (acts, findings,
   records) correctly inherit personal provenance → `NEVER_CROSSES`, writing only
   to the residency `L`, never a tracked/pushable artifact?

## Output

`reviews/governance-r1.md` (≤120 lines): per-measure findings each marked
decision-blocking or not, citing the design section and contract clause. State
separately whether **D2-P1** and **D2-P2** are conformant at Rung 2 or have a
decision-blocking gap. Name defects against the clause each violates; do not
redesign.

## Stop conditions

One review file. No repo changes, no git writes, all examples synthetic. If a
finding turns on a contract the governance docs do not contain, say so.
