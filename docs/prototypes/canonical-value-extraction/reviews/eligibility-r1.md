# Eligibility Review — Round 1

Reviewer: eligibility (Gate 0-8 process/economics only, per
`docs/prototypes/canonical-value-extraction/plan.md`; domain correctness is
covered by the clean-room and adversarial seats). Read: `plan.md`,
`charter-it1.md`, `charter-it2.md`, `examination-it1.md`,
`examination-it2.md` (via `git show
prototypes/canonical-value-extraction/it2:...`), and the committed
`reviews/clean-room-r1.md` already on this branch. No adversarial review is
committed yet on either branch as of this writing.

## Gate 1 — was prototyping warranted?

**Yes, and the rival genuinely earned its keep, though not by finding a
different destination.** Both examinations land on the identical mechanism
(direct per-item rule access via an optional `field` on `ref`) and both
independently ground it in ADR-0054 (verified real:
`docs/adr/0054-covered-ltcg-twin-scalar-collectible-members.md`), which
actually rejected a generic marshal/evaluator field-projection substrate for
a structurally adjacent problem. It1 was allowed to read the prior attempt
as reference; it2 was barred from all of it and found ADR-0054's Decision 1
anyway, from the schema/evaluator code alone. That is the load-bearing
corroboration: the constraint is a property of the actual codebase, not
institutional memory a lone incumbent-informed build might apply
uncritically.

Independence added a second, sharper value: it1 asserts CV-P1 causes "no
expression-language growth." It2 treats the same move as a named schema
successor (`v6`&rarr;`v7`, an optional `field` on `ref_expr`, currently
rejected by `v6`'s `additionalProperties: false`) and shows the milestone's
auto-prefer clause does not literally fire — the recommendation survives
because the growth is bounded and cheaper than A/B, not because there is
none. `reviews/clean-room-r1.md` independently flags this same rigor gap in
it1. A solo incumbent-informed build would plausibly have kept the
easier, self-flattering "no growth" framing. This is not evidence
prototyping was wasted.

## Gate 3 — evidence rung discipline

**Right amount, on both sides.** Diff against the charter parent
(`f982050f`) confirms each iteration added exactly one markdown file (200
and 192 lines) — no code, no fixtures, no schema edits, matching Gate 3's
rung-1 authorization and Gate 4's caps. No over-build.

No under-build either. The one case both flag as not paper-settleable
(case 6) is genuinely undecidable on paper: both independently confirm, by
reading `package_validation.py`, that no field-name check exists yet, and
it2 additionally notes today's `v6` schema would reject the `field`
property itself — the wrong failure mode. That is exactly a claim paper
cannot settle (a predicate about code that doesn't exist yet), correctly
deferred. Every other case is tied to an already-existing code path
(`env.symbols`, `DEPENDENCY_ABSENT`, correction fold, pin granularity),
the correct bar for "paper-settled." The clean-room review's carried-forward
question (whether it1's other "settled" calls quietly lean on the same
unbuilt check) is a legitimate cross-check, not evidence of under-build —
it2's document is more explicit that the check is absent for every case,
which weakens rather than deepens the worry.

## Gate 6 — has the minimum acceptable converged subset been met?

**Not yet — the rung-2 climb on case 6 is still outstanding.** The floor is
"CV-P1's mechanism selection, with fail-closed behavior demonstrated
against the real rule loader (climbing to rung 2 only if paper cannot
settle case 6)." Both examinations independently agree paper cannot settle
case 6. I checked whether that climb already happened: `docs/prototypes/
canonical-value-extraction/reviews/` contains only `clean-room-r1.md`,
itself a paper-rung legibility review that carries the unresolved case
forward rather than resolving it. No adversarial review is committed on
this branch, and there is no `process-log.md` recording a rung-2 climb.
Mechanism selection is converged on paper; the fail-closed demonstration
the floor requires is not done. Someone still needs to run a throwaway
validator-mutation exercise (rung 2) over a real, synthetic package fixture
with a misspelled `field` and confirm `package_validation.py` (or its
necessary `v7` successor) actually rejects it.

## Gate 7 — production adoption boundary

**Not yet eligible.** Gate 7 requires the seam to close and map to an
accepted ADR or milestone disposition with a real production test; neither
exists, and Gate 6's floor is unmet. Based on what the examinations actually
showed, that ADR would need to state, concretely:

1. **Schema change and version boundary** — `ref` gains an optional `field`
   (it2: `v6`&rarr;`v7` successor); today's `v6` actively rejects `field`
   via `additionalProperties: false`, so this is not additive/backward
   compatible and the ADR must say so.
2. **Validation obligation** — package validation checks any declared
   `field` against the bound fact type's `value_schema.properties` at
   load time, failing closed (never a runtime silent default) — demonstrated
   against the real loader (the owed rung-2 climb), not merely designed.
3. **Runtime resolution contract** — resolution reads the *current* finding
   at evaluation time; a schema-valid object missing the key yields
   `DEPENDENCY_ABSENT`, never zero-fill, distinct from `collect`'s
   empty-closed-set path.
4. **Provenance/citation shape** — whether the pin records
   `{fact_type_id, identity, finding_id, field}` or remains
   expression-tree-derived (it2's honest caveat) — load-bearing for
   downstream seams 2, 3, 5.
5. **What CV-P2 actually concedes** — growth is real but bounded (one
   optional property on one existing op, statically checked), not "zero
   growth."
6. **Explicit non-adoption of A and B**, and why, so later seams don't
   re-litigate already-compared candidates.

## Overall recommendation

**One more rung-2 spike needed on case 6 only.** Gate 1 and Gate 3
discipline were both handled well — the rival comparison was worth running,
and neither builder over- or under-built relative to charter. But Gate 6's
own floor is unmet: the single fact both examinations agree paper cannot
settle has not been demonstrated against real code by anyone on this
branch, and Gate 7 correctly blocks production adoption until that closes
into an ADR. This is a narrow, single-question climb, not a reopening of
CV-P1's mechanism selection.
