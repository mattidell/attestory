# Charter: Round 1 Committee — Governance Reviewer (D1)

Date: 2026-07-16. Topic D1, First Real Return Slice. Reviews both builds:
`it1/design.md` + `examination-it1.md` (incumbent), `it2/design.md` +
`examination-it2.md` (rival). Independent context; you do not see the adversary
reviewer's in-progress work.

- **Seat:** Governance reviewer, Medium tier.
- **Mandate:** conformance, not preference. Judge both designs against the
  committed contracts; do not redesign the boundary or resolve dissent by
  rewording. Report findings classified as decision-blocking or not.

## Read

Topic `plan.md`, both charters, both builds, `docs/governance/` (esp.
Constitution Article 18; Engineering Constraints E18.1/E18.2/E18.3; Ontology
quarantine, sensitivity inheritance, synthetic-by-default), ADR-0030 (esp. the
§C.8 amendment), the milestone plan's Data-safety and Verification sections, and
`tests/test_kernel_fixtures.py` (the current narrow floor).

## Measure

1. **Classification totality and determinism.** Is the classifier genuinely
   total with no undecidable ("cannot decide") state, and is fail-closed /
   default-deny correctly the only outcome for missing/unknown/contradictory
   proof? Confirm Case 5 is actually resolved, not asserted.
2. **§C.8 push independence.** Does the push gate scan the full outgoing
   envelope (objects, trees, commit *and tag* messages, ref names) independent
   of remote-tracking state and visibility — not a diff from `main`? Is the
   interim private-remote posture nowhere load-bearing?
3. **Structural-vs-procedural (Article 18).** Article 18 requires the boundary
   "structural where structure can hold it; grants complement walls, never
   replace them." Assess each design's honesty about what is a structural wall
   vs a bypassable hook, and whether guarded transport / hook integrity are
   correctly named as production conditions rather than papered over.
4. **Sensitivity inheritance.** Do disposition reports, ledgers, process logs,
   reviews, and derivation records correctly inherit workspace sensitivity
   (Ontology) — i.e. quarantined even without amounts? Flag any surface treated
   as safe because "it's just metadata."
5. **E18.3 discharge.** Do the provenance-manifest + byte-regeneration designs
   actually discharge E18.3's recorded debt (a runnable manifest check), or
   only restate it?
6. **Locator model (decision-blocking divergence).** The incumbent commits a
   pointer indirection (env var or ignored-root pointer file); the rival commits
   no locator at all. Judge each against §C.8's "no load-bearing ignore" —
   is an ignored-root pointer file a load-bearing ignore? State which model
   conforms; if both can, say so and name the conformance condition.

## Output

`reviews/governance-r1.md` (≤120 lines): per-measure findings, each marked
decision-blocking or not, citing the specific design section and contract
clause. State separately whether **D1-P1** and **D1-P2** are conformant at Rung 2
or have a decision-blocking gap. Do not propose a redesign; name the defect and
the clause it violates.

## Stop conditions

One review file. No repo changes, no git writes. All examples synthetic. If a
finding turns on a contract the governance docs do not actually contain, say so
rather than inventing authority.
