# Charter: Round 1 Committee — Governance Reviewer (D3)

Date: 2026-07-16. Topic D3 (last Track-0 decision), First Real Return Slice.
Reviews both builds: `it1/design.md` + `examination-it1.md` (incumbent),
`it2/design.md` + `examination-it2.md` (rival). Independent context; you do not
see the adversary reviewer's in-progress work.

- **Seat:** Governance reviewer, Medium tier.
- **Mandate:** conformance, not preference. Judge both designs against the
  committed contracts; do not redesign. Report findings classified
  decision-blocking or not.

## Read

Topic `plan.md`, both charters, both builds, `docs/governance/`, ADR-0027
(esp. decision 7 exclusive projection and its production conditions), ADR-0028
(byte-verification, quantity/composition closure, fail-closed at load), ADR-0031
(D1 residency — consumed), ADR-0032 (D2 — the marshal-only `RunContext`), and the
committed `packages/derivation/loader.py`, `package_validation.py`, runner.

## Measure

1. **Exclusive projection beyond fixtures (ADR-0027 d7).** Does the production
   contract keep only the resolved member graph executable/renderable, with
   co-located unpinned files inert — and does the rival's R6 (pin-directed supply,
   unpinned bytes never read) strengthen rather than alter the guarantee?
2. **Byte-verification fail-closed (ADR-0028).** Are member and package-instance
   checksum mismatches rejected at load with no fail-open path, and is the
   `PACKAGE_VERSION_REWRITE` (recomputed-self-checksum) attack closed against the
   publication registry?
3. **Strict-superset guarantee.** Is the production path provably a superset of
   the fixture path (same validator, more mandatory inputs, stricter gate) — never
   a weaker sibling? Confirm by construction, not only by test.
4. **The R5 no-leniency gate + RG-1 (the crux).** The rival's `ok == True` gate
   would refuse the currently committed package (validates `ok == False`, seven
   contained issues). Is enforcing `ok == True` the **conformant** reading of
   fail-closed / no-silent-partial (ADR-0028, plan case 5) — i.e. is RG-1 a
   correct named production obligation (fix the validator `optional_default`
   reachability edge + the v1-generation content debt / ADR-0028 PC2), or would a
   leniency carve-out be conformant? State which, and whether the incumbent's
   softer framing understates a real obligation.
5. **Discharge/defer ledger completeness (D3-P2).** Does the ledger account for
   **every** ADR-0027/0028 named production condition — discharged, carried,
   deferred-with-reason, or N/A — with no silent partial discharge? Is rejecting
   embedded schema-byte checksums (vs deferring) faithful to ADR-0027's partial
   rejection?
6. **Interlocks consumed, not weakened.** Are ADR-0031 (leak wall) and ADR-0032
   (marshal-only `RunContext`) consumed correctly — the resolver supplies adopted
   machinery while raw input/contribution values never enter resolution?

## Output

`reviews/governance-r1.md` (≤120 lines): per-measure findings each marked
decision-blocking or not, citing the design section and contract clause. State
separately whether **D3-P1** and **D3-P2** are conformant at Rung 2 or have a
decision-blocking gap, and give an explicit verdict on the R5-gate/RG-1 question.
Do not redesign.

## Stop conditions

One review file. No repo changes, no git writes, all examples synthetic. If a
finding turns on a contract the governance docs do not contain, say so.
