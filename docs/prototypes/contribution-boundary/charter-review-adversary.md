# Charter: Round 1 Committee — Adversary Reviewer (D2)

Date: 2026-07-16. Topic D2, First Real Return Slice. Reviews both builds:
`it1/design.md` + `examination-it1.md` (incumbent), `it2/design.md` +
`examination-it2.md` (rival). Independent context; you do not see the governance
reviewer's in-progress work.

- **Seat:** Adversary reviewer, **High tier** — two failure modes, one
  irreversible (a real value leaking across the D1 boundary via contribution).
- **Mandate:** break the invariants. A single working bypass is decision-blocking.

## Read

Both builds, topic `plan.md`, both charters, `docs/governance/` (Articles 7, 10,
12, 13, 14), ADR-0023, ADR-0010/0017, ADR-0031, and the committed
`packages/kernel/` and `packages/derivation/` source (especially the run
context/evaluator and the fixture/scenario adapter).

## Attack (at least these, all synthetic)

1. **Runs-consume-facts bypass (the crux).** The incumbent's Case 6 found the
   **committed synthetic scenario adapter silently published `777`** from an
   unprojected raw input; both builders name adapter-unreachability / a
   marshal-only run context as *production* work. Attack the **contract**: find a
   path by which a live run consumes a raw contribution input (or an unasserted
   value) that the new closed run-request / `RunContext` does **not** structurally
   close. Is the invariant settled at the contract level, or does the adapter
   leave a decision-blocking hole? Distinguish "settled contract + named
   production condition" from "unclosed hole."
2. **Declaration-side leak.** Can a rule/artifact **name a contribution as a
   dependency** and pull raw input through derivation? Test the rival's E14.2
   extension and the incumbent's run-request closure — does the union close both
   the runtime and the declaration side?
3. **D1 interlock (irreversible).** Construct a contribution path that lands a
   real value in a tracked or pushable artifact (a contribution record, a
   disposition, a locator) — defeating Case 5 / ADR-0031. Show it crossing.
4. **Force an entry order (anti-wizard).** Find a contribution sequence where one
   step depends on another completing, or where two orders yield different current
   fact state — breaking the any-order commutativity claim.
5. **Break correction-by-supersession.** Make a value correction resurrect a stale
   finding, orphan a dependent, advance the family horizon (destroying closure
   authority), or require an edit/withdrawal.

## Output

`reviews/adversary-r1.md` (≤120 lines): each attack as a concrete synthetic
scenario with the observed/argued outcome (bypassed / rejected), marked
decision-blocking or not. A clean bill on a probed invariant is evidence. State
separately whether **D2-P1** and **D2-P2** survive at Rung 2.

## Stop conditions

One review file. No repo changes, no git writes, no real data — synthetic markers
only. If a bypass would require a real value, use a synthetic stand-in and stop.
