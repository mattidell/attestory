# Charter: Repair 2 — QDCG Worksheet Missing-Declaration Walk (D2)

Status: **prepared, inactive — no seat assigned or dispatched**

This is the bounded follow-up Confirmation R1 required ("A bounded follow-up
must address that missing-declaration walk only",
`reviews/confirmation-r1.md`), now eligible because the substrate gap that
blocked it has been separately ratified and production-hardened: **ADR-0037**
(`conditional_dependency_set`) is accepted, and its production Track 0a
merged (`main` `6f303fe`, PR #30) after a full not-ready → repair →
ready review chain. It becomes executable only if the owner approves this
exact charter and explicitly releases its builder seat under ADR-0034.

- **Proposed role:** incumbent-repair builder, Medium tier (the substrate is
  now ratified contract, not novel ground — Repair 1 and D1's precedent both
  set this at Medium once the hard question is settled elsewhere).
- **Proposed working location:**
  `docs/prototypes/qdcg-worksheet/repair2/`.
- **Evidence rung:** Rung 1 only. No probe, production code, schema edit, or
  git write outside the prototype tree by the builder.
- **Inputs:** this charter; `repair1/design.md` and
  `examination-repair1.md` (the posture Repair 2 must not disturb);
  `reviews/confirmation-r1.md` and `confirmation-r1-triage.md` (the exact
  finding C1 being repaired, measurement 3); `round-1-triage.md` and
  `plan.md` (standing D2 context — Gate 2 case 3, Gate 6 floor); **ADR-0037**
  and its cited CMDN prototype evidence
  (`docs/prototypes/conditional-multi-dependency-nonpublication/`); the
  committed `conditional_dependency_set` node
  (`packages/derivation/evaluator.py`) and its production review chain
  (`docs/reviews/2026-07-19-dsbs-t0a-cmdn-review.md`,
  `2026-07-19-dsbs-t0a-delta-rereview.md`) for what the node actually
  guarantees at HEAD, not what the paper proposed. Real data is forbidden.

## What is already settled and must not reopen

Repair 1 resolved D2-P1 (declared-absence fact types, presence-before-value,
no default) and D2-P3 (bidirectional admission-locus contradiction interlock,
no reach-around to box 2a) at Rung 1; Confirmation R1 passed measurements 1,
2, 4, 5, 6 — the single successor posture, the qualified-zero lazy reduction,
the honest present-`yes` disposition, the D2-P3 boundary, and the
production-condition honesty of the whole design. **Repair 2 must preserve
every one of these outcomes unchanged.** It is not a fresh D2 round; it is a
one-finding patch.

## The one finding to repair

Confirmation R1 measurement 3 (fail): a qualified-positive return
(`demo-q-600`) with *both* capital-gain declarations absent must non-publish
naming both declarations as the contributable gaps. Repair 1's guard used a
plain `all([ref(cg_dist), ref(sched_d)])` inside the qualified-positive
branch; `ref` raises on the first absent symbol, `all` short-circuits, and
neither the runner's recorded `missing` list nor the NPE walk could ever
carry more than the first absent declaration — the exact defect
`conditional_dependency_set` exists to fix (ADR-0037 decision 2: "a true
condition evaluates every member exactly once, accumulates only
dependency-absence, and propagates every non-absence failure unchanged").

## Required repair

Produce one paper design and examination that replaces the qualified-positive
declaration-presence check with the ratified `conditional_dependency_set`
node, and re-derives every Repair-1 case against it:

1. **Missing-declaration walk (the fix).** When qualified dividends are
   positive and one or both declarations are absent, line 16 blocks with a
   single non-publication disposition naming **both** contributable
   declarations in one walk when both are absent, or exactly the one absent
   declaration when only one is — never fewer than the true absent set,
   never an implied zero. The design must cite `conditional_dependency_set`
   as the mechanism (condition = qualified dividends > 0; members = the two
   declaration refs) and show, from the committed evaluator/runner/
   explanation source (not the CMDN paper), that this actually produces the
   ordered multi-missing walk at HEAD.
2. **Reduction property preserved.** Qualified = 0 must still reach the
   unchanged `OrdTax(T)` result without reading, naming, or pinning either
   declaration — `conditional_dependency_set`'s own false-condition contract
   ("the node succeeds without evaluating, naming, or pinning a member")
   must be the cited reason, not a separate short-circuit the design has to
   maintain by hand.
3. **Present-`yes` outcome preserved.** When qualified dividends are
   positive and both declarations are present but at least one reads
   `"yes"`, the outcome remains the committed `inapplicable` /
   `guard_inapplicable` disposition Repair 1 established — never a blocked
   code, never treated as a missing-declaration case. Show precisely how the
   guard expression distinguishes "absent" (blocks, via CMDN) from "present
   but yes" (inapplicable, via an ordinary guard read) — these are different
   evaluator paths and the design must not conflate them.
4. **Declared-zero publish and displacement unchanged.** Qualified positive
   with both declarations current at `"no"` still publishes the worksheet
   result, pinning both declaration findings (CMDN's true-condition contract:
   "a published finding pins the condition and all active members through
   existing derivation edges"); a later supersession of either declaration
   still displaces line 16 to non-current through the existing two-edge
   model — cite this from ADR-0037's ratified pin-integrity guarantee, not
   asserted fresh.
5. **No collateral change to D2-P1/D2-P3.** The fact types, their domains,
   the admission-locus contradiction interlock, and the no-reach-around
   universe boundary are Repair 1's design, unmodified. If the CMDN
   substitution requires touching any of them, that is itself a finding to
   report, not something to design around silently.

## Cases and outputs

Re-run Repair 1's full case set (`repair1/design.md`, "Cases"), with case 3
("Q>0, decls absent") now required to show the two-declaration walk
explicitly — both absent, and each singly absent — plus the present-`yes`
case (6) shown as structurally distinct from the absence case. All values
synthetic `demo-*`.

Outputs are only `repair2/design.md` (≤180 lines — this is a one-finding
patch, not a full worksheet re-derivation) and `examination-repair2.md`
(≤80 lines). The examination must state explicitly whether D2-P2 is now
settled at Rung 1 in full (all of Repair 1's posture plus the missing-
declaration walk) or identify what remains. It may not claim a production
condition is live at HEAD — citing ADR-0037's ratified text and its merged
Track 0a production code is citing committed contract and committed code,
which is different from claiming the *D2 worksheet itself* is implemented;
keep that distinction explicit. Stop after those two documents.

## After this repair

If the examination finds D2-P2 fully settled, the next step is a fresh,
narrowly-scoped confirmation pass (mirroring `charter-confirmation-r1.md`,
re-measuring only what Repair 2 changed) — not immediately an evaluation
analysis or ADR draft, and not pre-authorized by this charter. If confirmed,
D2's evaluation analysis and ADR drafting become eligible, and only after
ratification can the milestone plan's Track 3 be chartered as a production
build. This charter authorizes none of that; it authorizes only the two
Repair 2 documents.
