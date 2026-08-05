# Qualitative Review Standard

Audience: Reviewers and Foremen chartering review.

This is the project's living method for qualitative review. It complements a
review charter: the charter defines the object, scope, and required checks;
this document defines the questions a Reviewer brings to every object. Reviewer
posture and execution disciplines remain in `docs/roles/reviewer.md`; short
earned heuristics remain in `docs/roles/craft-notes.md`.

## How this document changes

Add guidance here when a review lesson recurs across milestones or the owner
directs that it become standing review practice. State the reusable question or
failure pattern, not the milestone story that exposed it. Do not copy product
contracts, role posture, commands, or one-off findings into this file. Remove a
question when tooling or another authoritative process document makes it
mechanical.

## Start by drawing the box

Before judging an implementation, describe the reviewed capability as a box:

- what facts or artifacts may enter;
- what authority makes each input usable;
- what the box may derive or publish;
- what must remain outside; and
- which neighboring or historical behavior must remain unchanged.

Then distinguish the kinds of state in that box. An observed world fact, a
user declaration, a derived fact, and an operational completeness or closure
state are not interchangeable merely because they sometimes carry the same
value. If the implementation normalizes them, confirm that it preserves the
distinction needed for explanation, correction, and audit.

## Ask four questions about every material claim

1. **What does the claim mean?** Identify the real-world or rule-level statement,
   including exclusions and boundedness. Do not let a convenient storage shape
   silently redefine it.
2. **What authority establishes it?** Trace the exact declaration, source fact,
   closure, mapping, citation, or adopted contract that licenses the claim.
3. **What happens when that authority changes?** Exercise correction,
   supersession, displacement, reopening, late membership, and path switching
   where applicable. A correct initial number with a missing dependency edge is
   still incorrect.
4. **What evidence would fail if the implementation were lying?** Require an
   observation that reaches the real boundary and would detect the named defect,
   not an assertion that repeats the intended result.

## Preserve meaning without fetishizing shape

Branches are appropriate when the law, the world, or the authority genuinely
has alternatives. Normalize alternatives behind one adapter or producer when
downstream consumers need the same canonical meaning. Reject both scattered
consumer branching and premature normalization that erases material provenance.

In particular, a declared absence may derive a numeric zero when the bounded
rule makes them extensionally equivalent. The derived value may be the same as
an observed zero; its pins and explanation must still show which authority
produced it. Review the semantic distinction and the downstream contract
separately.

## Treat provenance and lifecycle as correctness

Check more than the displayed value. A derived result must pin every authority
whose correction should displace it, directly or through a valid dependency
chain. Missing authorities, companion facts, identity matches, mappings, or
citations must fail closed. A broad exception handler, silent `continue`,
default, or fallback deserves scrutiny whenever it can turn "not established"
into apparent success.

When a repair changes shared machinery, identify every sibling consumer of that
mechanism. Require a regression at the shared boundary, not only a new-domain
happy path. A local milestone does not make a generic runner change local in
blast radius.

## Make evidence load-bearing

Judge what a test actually observes:

- A canonical golden must be required, never created by its own test, and must
  compare the contract surface it claims to freeze. If the complete artifact is
  deterministic, prefer complete structural equality; otherwise define and
  compare one explicit canonical projection.
- A negative test must invoke the actual validator, projector, resolver,
  transport, or publication boundary. Mutating an already-produced dictionary,
  checking a Python type, or accepting an argument error does not prove that the
  production boundary rejects malformed input.
- A lifecycle test must observe displacement evidence such as finding identity,
  currentness, or exact pins, not merely an unchanged numeric answer.
- A compatibility test must run the actual sibling or historical route whose
  preservation is claimed.
- A passing test establishes no more than the path and evidence type it
  exercised. Read the fixture and helper before accepting the test name.

## Separate semantic verdict from mechanical gates

Review semantic correctness independently, then check the required mechanical
gates before recommending publication. Formatting, typing, schema-registry,
data-envelope, and CI failures may be mechanically simple, but a candidate with
a required failing gate is not `READY`. A review record describes the measured
candidate; it must not anticipate a repair or a future green check.

## Write findings as falsifiable measurements

For each finding, name:

- the violated claim or invariant;
- the exact artifact and observable reproduction;
- the consequence, including whether it is semantic, lifecycle, evidence,
  compatibility, data-safety, or publication-gate risk; and
- the smallest property-level repair that would close it without expanding
  scope.

Lead with findings ordered by consequence. Distinguish "behavior is wrong"
from "the evidence does not establish the claimed behavior." Record what was
successfully verified so a bounded repair can preserve and reuse that evidence.
