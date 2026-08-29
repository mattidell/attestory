# Eligibility Review — Round 1

Reviewer: eligibility (Gate 0-8 process/economics only, per `plan.md`;
domain correctness is covered by the clean-room and adversarial seats,
run in parallel). Read: `plan.md`, `charter-it1.md`, `charter-it2.md`,
`examination-it1.md`, `examination-it2.md` (via `git show
prototypes/standing-authorization-successor/it2:...`),
`docs/prototypes/standing-authorization-currentness/examination.md` (Seam 4's
spike), and the milestone document's Integration section. No adversarial
review (`reviews/adversary-r1.md`) is committed on either branch as of this
writing; checked again before closing this note — still absent.

## Gate 1 — was prototyping warranted, and did two builders add value?

**Yes, and the two-builder shape earned its keep here for a different
reason than usual.** There is no incumbent to anchor against — Seam 4's
spike already established that per-family closure is "not a starting point
to adapt, it is a different mechanism." So the two-builder value isn't
rival-vs-incumbent triangulation; it's testing whether the plan's six paper
cases actually *force* a unique design, or underdetermine it. They diverge
on exactly the axis that tests this:

- **Citizen category.** it1 mirrors `horizons.py`'s chain-key pattern
  directly (a kernel-analog design, explicitly grounded in reading that
  file). it2 independently argues the citizen must be none of finding,
  Ontology Grant, or package-adoption, and lands on a distinct "permission
  citizen" category riding the ordinary act log — a different taxonomic
  argument reaching a compatible but not identical shape (grant/end acts
  with `supersedes`, vs. it1's suspend/reinstate/withdraw four-act chain).
- **SA-P2 scope of the boundary hash.** it1 hashes only the referenced-input
  dependency closure of the specific rule composition the authorization
  covers (narrower, but needs-rung-2 on whether that closure computation
  exists). it2 hashes the full adopted source-family/fact-type surface for
  the tax year (broader, admits by its own per-case table that "the six
  Gate-2 cases do not... force it to a specific answer").

That divergence is the real finding: the six cases discriminate the SA-P1
core (both converge on chain-keyed-by-scope, fail-closed, decoupled from
membership) but do not discriminate SA-P2. One builder alone could not have
shown that; it would have produced one boundary rule and no way to tell if
it was forced or a stance. That is worth the second builder's cost here,
independent of whether it1 or it2 wins.

## Gate 3 — evidence rung discipline

**Right amount, and both sides self-limit correctly.** it1 names three
needs-rung-2 items: the diagnostic near-miss lookup's cost against a real
chain index (cases 2/3), reinstate-after-withdrawal rejection at admission
time (case 5), and whether "dependency closure of a rule composition"
already exists as machinery (SA-P2). it2's list is broader and more
conservative: it marks cases 1, 2, 3, 5, and 6 all as needing rung 2 before
production, on the single ground that paper cannot prove "the real path
consults this citizen and cannot fall through to `closed_sets`" — i.e. it2
treats *wiring into the real admission path* itself, not just the internal
state-machine logic, as unsettled for every case except 4 (structural
non-coupling, an absence-of-call argument both builders treat as
paper-decidable and correctly so, since it is a claim about which appliers
exist today, not about future integration).

Neither over-built (no fixtures, no code — both branches diff to one
markdown file each, 199 and 187 lines, within the ≤200-line cap) nor
under-built (both explicitly refuse to call the admission-path integration
question settled at paper, which is the one thing plan.md's Gate 3 climb
criterion asks: "does the chosen scope-comparison mechanism actually fail
closed against the real act-log/finding admission path, or only against a
paper description of it?"). it2's more conservative rung-2 list is the
better-calibrated one of the two, but it1's narrower list is not wrong —
it1's remaining "settled at paper" cases (1, 3, 4, 6 core mechanics) really
are dict-key-match or absence-of-call arguments checkable by inspection,
matching Seam 4's own precedent for what counts as paper-settled.

## Gate 6 — has the floor been met, or does it require rung 2 regardless of winner?

**Rung 2 is required regardless of which design wins.** Both examinations
say so themselves: it2's own per-case table marks cases 2 and 3 (the exact
floor — "fail-closed behavior demonstrated for wrong-taxpayer and
wrong-year against a real... admission/consumer path") as needing rung 2,
and it1 flags the diagnostic lookup underlying those same two cases as
needing rung 2 against a real chain index. Paper alone settles the *state
machine* (which refusal code fires) for both designs, but plan.md's floor
explicitly requires it "against a real... admission/consumer path," and no
prototype-local admission path exists yet on either branch — only Python
snippets illustrating intended logic. No adversarial review has landed to
add or subtract from this; checked again immediately before writing this
note.

## Gate 7 — what would the ADR need to state?

Concretely: (1) the selected citizen shape (identity/scope tuple, act
kinds, chain/current-resolution rule) as a schema description, not
prose; (2) the SA-P2 boundary rule as a checkable predicate over adopted
content, picking a specific scope (referenced-composition closure vs. full
surface digest) rather than leaving both live; (3) the coexistence contract
with per-family closure — both examinations independently state narrow
family confirmations remain the fallback when standing authorization is
absent/suspended, and the ADR must make that boundary explicit rather than
implied; (4) that this is a **net-new** mechanism, not a migration. Because
Seam 4 already found no real implementation exists today, there is no
existing data to migrate, no dual-write period, no deprecation of a working
mechanism — simpler than usual in that respect. But it is harder in the
adjacent respect the prior seam's spike flags directly: the Integration
diagram already assumes this node is real, so the ADR must state the
producer/consumer wiring (who calls the new resolver, where it's exposed
on `Environment`, what provenance it writes) as production conditions, not
leave them as prototype sketch — because unlike a seam replacing a working
mechanism, there is no fallback behavior to inherit if the wiring is left
implicit.

## Relationship to Integration

**Not ready at rung 1; Integration needs a rung-2 build first.** The
milestone's Integration section states "a suspended standing authorization
blocks currentness without touching tax semantics" as a property it will
*run*, not merely cite — Integration reruns T1-T9 in full over composed,
working seam outputs. Neither examination has a working admission path;
both are paper documents with illustrative code, and both self-report that
the exact property Integration needs to exercise (fail-closed against a
real path) is unsettled. This matches Gate 6's own conclusion above: the
seam cannot supply Integration a real component until at least a rung-2
spike of the selected (or synthesized) design exists.

## Recommendation

**Rung-2 spike on the winner only.** Gate 1's discrimination goal is met —
the six paper cases forced convergence on SA-P1's core shape and exposed
that SA-P2 is genuinely underdetermined by them, which is real evidence,
not a symptom of running too few or too many builders. Running rung 2 on
both would re-spend the two-builder cost on a question paper has already
resolved (SA-P1's core state machine); the discriminating question left is
whether the *chosen* design's admission path actually wires and fails
closed against a real log, which is a single-design question. Pending
adversarial and clean-room findings on domain correctness should decide
which of it1/it2 (or a synthesis, e.g. it1's narrower SA-P2 closure with
it2's grant/end act envelope) is "the winner" before that spike starts.
