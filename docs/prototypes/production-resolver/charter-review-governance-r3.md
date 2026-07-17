# Charter: Round 3 Committee — Governance Reviewer (D3)

Date: 2026-07-16. Topic D3 (last Track-0 decision), First Real Return Slice.
Reviews the **Iteration-3** builds: `it5/design.md` + `examination-it5.md`
(incumbent), `it6/design.md` + `examination-it6.md` (rival). Independent context;
you do not see the adversary reviewer's in-progress work. Owner-authorized
dispatch (ADR-0034, 2026-07-16).

- **Seat:** Governance reviewer, Medium tier.
- **Mandate:** conformance, not preference. This is a **confirmation round** — the
  question is whether Iteration 3 *closes* the four standing decision-blocking
  findings and yields a ratifiable contract, or whether a blocker survives.
  Confirm-or-refute; do not open unrelated new scope. Report findings marked
  decision-blocking or not.

## Read

`it5`/`it6` builds, topic `plan.md`, the Iteration-2 committee reviews
(`reviews/governance-r2.md`, `reviews/adversary-r2.md`) for the standing findings,
`docs/governance/` (Ontology §1/§4 actor, Article 4), ADR-0027 (esp. Decision 6 /
PC3 publication-registry authority, decision 7 exclusive projection), ADR-0028
(byte-verification), ADR-0031/0032 (consumed interlocks), and the committed
`packages/derivation/` loader/validation/`verify_published_package`.

## Measure — do the Iteration-3 builds close each standing blocker?

1. **Registry/release authority (ADR-0027 D6/PC3).** Is a versioned
   release/registry citizen's **actual bytes** verified against the adoption pin
   *before* it authenticates any package/member, so a caller-selected or forged
   registry/catalog cannot agree with forged supply? Confirm release-byte
   mismatch (not merely entry mismatch) rejects.
2. **Current-user adoption (Ontology §4 / Article 4).** Is exactly one **current
   user** adoption selected by declared scope, revision, and exact
   package/trust-anchor, with supersession currency over stale/competing acts, and
   automation/non-user actors ineligible — never caller choice?
3. **Order-independent same-key refusal.** Are same-key distinct-byte candidates
   refused by the set of digests regardless of enumeration order?
4. **Exhaustive ledger (D3-P2).** Does the ledger enumerate **every** ADR-0027
   Decision 1–7 / PC1–PC4 and ADR-0028 Decision 1–9 / PC1/PC1b/PC1c/PC2/PC3 as
   contract-settled / production-condition-with-owner / deferred-with-reason / N/A,
   with **no** false discharge of D1/D2 interlocks and no unclassified entry?
5. **Strict gate + RG-1.** Is `validation.ok == True` retained (no allowlist), and
   is RG-1 named precisely (the validator-reachability repair for the four
   `MEMBER_UNREACHABLE` issues + the v1-generation content debt behind the other
   four of the **eight** issues) as a MUST production prerequisite — not a reason
   to weaken the gate?

## Output

`reviews/governance-r3.md` (≤120 lines): per-measure, state **closed** or
**still-blocking** with the design section and contract clause. Then an explicit
verdict: are **D3-P1** and **D3-P2** conformant and ratifiable at Rung 2, or does a
decision-blocking gap survive? If ratifiable, note which build (or synthesis) is
the basis. Do not redesign.

## Stop conditions

One review file. No repo changes, no git writes, all examples synthetic. If a
finding turns on a contract the governance docs do not contain, say so.
