# Charter: Round 3 Committee — Adversary Reviewer (D3)

Date: 2026-07-16. Topic D3 (last Track-0 decision), First Real Return Slice.
Reviews the **Iteration-3** builds: `it5/design.md` + `examination-it5.md`
(incumbent), `it6/design.md` + `examination-it6.md` (rival). Independent context;
you do not see the governance reviewer's in-progress work. Owner-authorized
dispatch (ADR-0034, 2026-07-16).

- **Seat:** Adversary reviewer, Medium tier. D3's failure mode is
  resolution/availability (recoverable); the leak surface is ADR-0031's wall —
  attack whether resolution can **bypass** it, don't re-audit it.
- **Mandate:** this is a **confirmation round**. Try to break the four fixes
  Iteration 3 claims. A single working bypass is decision-blocking. If you cannot
  break them, a clean bill is the evidence that closes D3.

## Read

`it5`/`it6` builds, topic `plan.md`, the Iteration-2 reviews (the four standing
findings), `docs/governance/` (Ontology §4, Article 4), ADR-0027 (D6/PC3, d7),
ADR-0028, ADR-0031/0032, and the committed `packages/derivation/` code. You may run
read-only probes against committed surfaces; change nothing.

## Attack (at least these, all synthetic)

1. **Forge past release-byte authority.** Construct a release/registry whose bytes
   the adoption pin would still accept while carrying forged supply — or show the
   pin→release→registry→package/member chain has no gap. Test caller-selected `L`
   registry and forged catalog (it5 probes 2–4; it6 P1–P3).
2. **Break current-user adoption selection.** Make an automation/non-user act,
   a stale superseded act, or two competing same-scope tips resolve to a package
   the contract should refuse — or confirm it selects exactly one current user
   act (it5 probes 8–12; it6 P4–P5).
3. **Defeat same-key refusal by ordering.** Find an enumeration order (or a
   same-key identical-vs-distinct byte case) that admits an unintended candidate
   (it5 probes 13–14; it6 P6/P7/P10).
4. **Byte-verification / strict-gate.** Find a fail-open path (member,
   package-instance, `PACKAGE_VERSION_REWRITE`), or test whether the `ok == True`
   gate **over-fires** on a genuinely clean package or a **leniency** would admit a
   silently-partial one. Confirm the **eight** core-package issues and that RG-1 is
   the honest fix, not a gate weakening.
5. **Ledger honesty + D1 interlock.** Find a ledger slot that falsely claims
   discharge (esp. a D1/D2 interlock claimed installed), and a resolution path that
   copies live `L` content into a tracked/pushable artifact (ADR-0031 bypass).

## Output

`reviews/adversary-r3.md` (≤120 lines): each attack as a concrete synthetic
scenario with the outcome (bypassed / rejected), marked decision-blocking or not.
Then an explicit verdict: do **D3-P1** and **D3-P2** survive at Rung 2 — is D3
finally converged, or does a decision-blocking bypass remain?

## Stop conditions

One review file. No repo changes, no git writes, synthetic markers only. If a
bypass would require a real value, use a synthetic stand-in and stop.
