# Charter — Packaging the Surface, Track 2: the ADR

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/packaging-the-surface.md`
- Branch: `milestone/packaging-the-surface` (Track 1 `0fd05e7`, review `ee50b8f`
  READY)
- Deliverable: `docs/adr/0049-*.md` and its `docs/adr/INDEX.md` row. Proposed,
  not ratified — ratification is the owner's.

## What this ADR is for

Someone reading only this document a year from now should learn: UI code
reaches the live workspace in its own adopted artifact, separate from the rule
package; that artifact carries opaque program bytes verified by digest and
never validated for meaning; it builds at the workspace, offline; and here is
why the rule package was left alone.

Track 1 built all of that and it passed review. You are writing down what
already exists and what it rests on, not designing anything. Read the Track 1
code and its review before writing a word:
`packages/derivation/surface_resolver.py`,
`packages/schemas/derivation/surface-artifact.v1.schema.json`,
`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-28-packaging-the-surface-track1-review.md`, and the
milestone plan.

## What it must decide, not merely describe

Three things are open. Do not paper over them.

**1. What the build's output rests on.** Every input is digest-verified. The
output — the thing the browser actually runs — is not, because it did not
exist until the workspace made it. The trust chain is "verified inputs plus one
fixed command." Say whether that is sufficient, and if it is, say exactly what
it assumes about the build being deterministic. If it is not sufficient, say
what would make it so and name that as future work rather than pretending this
ADR closed it. This is the weakest joint in the whole design and the review
agreed. Give it real thought rather than a paragraph.

**2. The Node toolchain as a workspace precondition.** The build needs Node
and Node ships in neither container. That makes it a condition of the live
workspace rather than something a crossing carries — a category this project
has not declared before. ADR-0047 already has a framing for preconditions the
mechanism cannot see. Decide whether this belongs in it, and say what happens
if the assumption is wrong (missing Node, or a different version producing
different output).

**3. Why the rule package was left alone.** State the reasoning for two
containers rather than one, including the cost — a second thing the owner
adopts. Someone will propose merging them later; this section is what they
have to argue against.

## What it should record plainly

- The container's shape and how it verifies, including that it reuses
  ADR-0033's release and registry chain and diverges only where that chain's
  member-graph validation cannot apply.
- The adoption route: a distinct `surface-adoption` kind reusing
  `act-package-adoption.v1`'s payload, and why a second payload schema would
  have recorded nothing new.
- The offline build, scoped honestly: structurally offline because no package
  manager runs, with enforcement proved only under macOS `sandbox-exec`, and
  no CI coverage because the tests need Node and Chrome present. Do not
  upgrade that into a stronger claim than Track 1 earned.
- The measured cost: 941 entries, 5,065,001 bytes, one direct dependency.

## Known weak points to carry, not hide

The review and the builder between them named these. The ADR should state
them in its own words:

- The offline enforcement is macOS-only and uncovered by CI, so the evidence
  exists but is not continuously checked.
- `surface_resolver.py` reuses three underscore-private names from
  `production_resolver.py`. Real reuse, fragile coupling. Say what would
  happen if it drifts.
- The sample page uses no TypeScript, so the toolchain cost of TypeScript
  compilation is untested and will appear later.

## Boundaries

- Do not change product code. This track writes a decision about code that
  already exists and passed review.
- Do not ratify. Status is proposed.
- Do not revise Track 1's code, tests, or review. If you think something in
  them is wrong, say so in the ADR and report it — do not edit the evidence.
- No maturity claim.

## How to write it

Plainly. State the decision, the reasoning, and the cost. Where you are not
confident, say so in your own words instead of hedging every sentence. Match
the structure of a recent ADR; `0047` and `0048` are the closest analogues.
Shorter is better here — this documents something already built and tested,
and the last two ADRs in this line ran long.

## Stop conditions

- Writing it honestly requires changing Track 1's code.
- You conclude the two-container decision was wrong. Say so; the owner would
  rather know now.

## Verification

The CI `verify` sequence or a stated subset with omissions justified.

## Report back

The ADR, the INDEX row, your answer to each of the three open questions, and
the weakest point in your own reasoning.
