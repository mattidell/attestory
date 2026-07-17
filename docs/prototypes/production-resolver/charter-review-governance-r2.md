# Charter: Iteration 2 Committee — Governance Reviewer (D3)

Date: 2026-07-16. First Real Return Slice, Track-0 D3. Review the new paired
builds only: incumbent `it3/design.md` + `examination-it3.md`; clean-room rival
`it4/design.md` + `examination-it4.md`. Independent context; do not see the
Adversary review while it is in progress.

- **Seat:** Governance reviewer, Medium.
- **Mandate:** conformance measurement, not design preference. Classify each
  finding as decision-blocking, production condition, or non-blocking.

## Read

`SEAT.md`, `plan.md`, `process-log.md`, both Iteration-2 charters/builds and
Round-1 reviews; ADR-0027, ADR-0028, ADR-0031, ADR-0032; governance documents;
and the committed loader, package validator, runner, adoption and publication
registry surfaces. Do not read a concurrent Adversary output.

## Measure

1. **Publication authority:** does each design anchor the package and every
   member to ADR-0027 Decision 6 / PC3's immutable publication registry, closing
   self-authenticating `L` catalog substitution and package-version rewrite?
2. **Adoption authority:** is the proposed current package-selection carrier a
   declared Article-4 act with an appropriate actor, scope, provenance, exact
   package, and trust-anchor pin—not caller metadata, a process record, or an
   undeclared noun? Check the actor claim against the current Ontology.
3. **Exclusive graph and strict superset:** are members pin-directed, unpinned
   co-located bytes inert, and `ok == True` mandatory before graph, execution, or
   rendering, preserving all fixture guarantees without a leniency path?
4. **D3-P2 ledger:** verify explicit, accurate dispositions for every ADR-0027
   Decision 1–7 / PC1–PC4 and ADR-0028 Decision 1–9 / PC1–PC3. Distinguish a
   contract decision from a Track-3 installed-production discharge; preserve the
   rejection of embedded schema-byte checksums.
5. **Interlocks and RG-1:** confirm D1/D2 are consumed but not falsely claimed
   installed, and RG-1 is a MUST prerequisite with the observed eight issues.

## Output and stop

Write only `reviews/governance-r2.md` (≤120 lines). Cite the exact design and
contract clauses for each result; state separately whether D3-P1 and D3-P2 are
conformant at Rung 2 and whether an ADR-0033 draft is supportable. All examples
synthetic. No implementation, schema, process-log, or git changes.
