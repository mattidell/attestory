# Charter: Round 1 Committee — Adversary Reviewer (D3)

Date: 2026-07-16. Topic D3 (last Track-0 decision), First Real Return Slice.
Reviews both builds: `it1/design.md` + `examination-it1.md` (incumbent),
`it2/design.md` + `examination-it2.md` (rival). Independent context; you do not
see the governance reviewer's in-progress work.

- **Seat:** Adversary reviewer, Medium tier. D3's failure mode is a
  resolution/availability defect (recoverable); the *leak* surface is ADR-0031's
  wall — attack whether resolution can **bypass** it, not re-audit it.
- **Mandate:** break the resolver. A single working bypass is decision-blocking.

## Read

Both builds, topic `plan.md`, both charters, `docs/governance/`, ADR-0027 (d7 +
production conditions), ADR-0028 (byte-verification), ADR-0031, ADR-0032, and the
committed `packages/derivation/loader.py`, `package_validation.py`, runner.

## Attack (at least these, all synthetic)

1. **Parity gap.** Find a guarantee the fixture path enforces that the production
   path drops (or vice versa) — the production path must be a **strict superset**.
   Probe the same synthetic package from a fixture and a scratch-`L` source and
   hunt for graph drift or a check that only one path runs.
2. **Unverified / co-located member into the graph.** Slip a co-located unpinned
   file, a same-key impostor, or a member with mismatched bytes into the resolved
   graph so it executes or renders. Test the rival's R3 checksum arbitration
   against the **unsorted fixture-glob enumeration-order race** it names — is the
   race real, and is it closed independent of ordering?
3. **Byte-verification fail-open.** Find any path where a member or
   package-instance mismatch loads instead of rejecting — including the
   recomputed-self-checksum (`PACKAGE_VERSION_REWRITE`) attack and the committed
   runner's untyped `KeyError` failure mode (is it fail-closed in effect?).
4. **The R5 gate / RG-1 (the crux).** The rival's `ok == True` gate refuses the
   currently committed package (`ok == False`, seven issues). Adversarially test
   the reverse: is there a value in the strict gate that **over-fires** — refusing
   a package that is genuinely clean — or a leniency that would let a *silently
   partial* package through? Judge whether RG-1 (repair the validator
   `optional_default` reachability edge + the v1-generation debt) is the honest
   fix or masks a contract weakness.
5. **D1 interlock bypass.** Construct a resolution path that copies live package
   content from `L` into a tracked/pushable artifact, defeating ADR-0031. Show it
   crossing, or confirm the resolver's write surface is `L`-only.

## Output

`reviews/adversary-r1.md` (≤120 lines): each attack as a concrete synthetic
scenario with the observed/argued outcome (bypassed / rejected), marked
decision-blocking or not. A clean bill on a probed invariant is evidence. State
separately whether **D3-P1** and **D3-P2** survive at Rung 2, and your verdict on
the R5-gate/RG-1 question.

## Stop conditions

One review file. No repo changes, no git writes, no real data — synthetic markers
only. If a bypass would require a real value, use a synthetic stand-in and stop.
