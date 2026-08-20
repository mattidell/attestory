# Foreman Correction — the round-3 ruling on 5b-ii rested on a false premise

Audience: Foreman, Track 2b and Track 3 Builders, any later reader of the
Track 0 corpus.

Filed by the Foreman 2026-08-20, on evidence produced by Track 2
(`f276cc5b`) and independently re-run by the Foreman before filing.

This record corrects the **reasoning** of a Foreman ruling, not its
conclusion. It is filed because exit criterion 4 requires disagreement to
stay visible, and a ruling whose stated basis is known false is not made
visible by leaving it in place.

## What was asserted

The round-3 ruling in
`docs/reviews/2026-08-19-grammar-census-track-0-boundary-corpus-builder-charter.md:273-280`,
carried into the closed Track 0 deliverable at
`docs/phases/grammar-census/inquiries/track-0-boundary-and-corpus.md:389-399`,
states:

> **Round 2 missed an enforcement site.** The bound is enforced at package
> admission: `packages/derivation/package_validation.py:2037` defines its own
> `MAX_PREDICATE_DEPTH = 6`, and `:2051-2056` rejects deeper predicates with
> issue code `MEMBER_CONSTRAINT_TOO_DEEP`. That is the same admission gate
> that makes surface 4 grammar proper — **a package carrying an over-deep
> predicate is refused before it can execute.** The bound is therefore
> enforced by contract, twice, on the module side of the module/store line.

The emphasised clause is false for term trees, and the "twice" it supports is
false as stated.

## What is actually true

`packages/derivation/package_validation.py:182-188`:

```python
def _predicate_depth(node: Any) -> int:
    if not isinstance(node, dict):
        return 0
    args = node.get("args")
    if isinstance(args, list) and args:
        return 1 + max(_predicate_depth(arg) for arg in args)
    return 1
```

It recurses through `args` only. Of the operators the evaluator accepts in a
`violated_when` tree, only `all` and `any` carry `args`. `add`, `subtract`
and `compare` carry `left`/`right`; `floor_zero` carries `value`. The
evaluator walks all of them — `declarative_validation.py:61-95` recurses on
`left` and `right` with `depth + 1` and raises `MemberConstraintTooDeep`
above `MAX_PREDICATE_DEPTH`.

So the two constants are equal and the two algorithms are not. Foreman
synthetic, `compare(add^n(field, 1), 0)` against member `{x: 1}`:

```
 nest  admission_depth  admission                  runtime
    1                1     ACCEPT             evaluated OK
    3                1     ACCEPT             evaluated OK
    4                1     ACCEPT             evaluated OK
    5                1     ACCEPT  MemberConstraintTooDeep
    8                1     ACCEPT  MemberConstraintTooDeep
   20                1     ACCEPT  MemberConstraintTooDeep
```

Admission reports depth 1 for a twenty-level nested term tree and admits it.
Track 2 reached the same result independently by a different route
(`track-2-reconciliation.md` spot-check S2, verification V4, disagreement D4,
construct U-124).

## Three consequences, stated plainly

**1. A published contract is not enforced as written.** ADR-0066 decision 2
says "Resolver admission rejects predicate depth greater than six." For any
tree whose nesting runs through `left`/`right`/`value` — which is every
arithmetic and comparison tree — it does not. This is the most consequential
single finding of the milestone so far, and it is a **finding, not a repair**:
this milestone changes no production code. Whether admission should be made
to walk the other keys, or the ADR amended to describe what admission does,
is a code-or-contract change and belongs to a later, owner-selected unit. It
is recorded as Track 2 surviving open question 5.

**2. Track 0 representational gap 8 understated itself.** It says the two
untied literals mean admission and evaluation "can silently diverge." They
already do. The gap is not a latent hazard; it is a realised one, and Track 2b
should carry it into the tension catalog in that stronger form.

**3. The ruling's conclusion survives; its stated basis does not.** Under the
round-4 amended primary criterion, 5b-ii is grammar proper because the depth
bound is a well-formedness constraint on the separately versioned
`source-family.v2` citizen, whose shape is contractually enforced by published
JSON Schema (`SchemaRegistry.validate_declared`) **or** by package admission
**or both** — the criterion does not require that *this particular*
constraint be the one admission enforces, and 5b-i's vocabulary is
schema-enforced regardless. The evaluator's enforcement of the bound at
`declarative_validation.py:20,62,87` is real and unaffected. What fails is the
narrower round-3 argument that admission enforcement makes 5b-ii identical in
kind to surface 4. It does not: surface 4's admission gate does what it says;
this one does not.

Net effect on the census: **no label moves.** 5b-ii stays `proper`. The
supporting sentence is struck.

## The methodological point, which is the reason this is a separate record

The round-3 ruling was reached by the Foreman reading the admission gate's
*constant and rejection block* and stopping there. Both citations were
correct. The constant is 6; the rejection block exists; the issue code is
right. Every checkable fact in the sentence checks out, and the sentence is
still false, because the depth-computing function between them was never
opened.

This is the same failure shape as the Q1 correction recorded in
`docs/reviews/2026-08-19-grammar-census-track-0-boundary-map-external-critique.md`:
checking the specific claims a piece of reasoning makes is not the same as
checking the conclusion drawn from them. There the Foreman and an external
model agreed on a wrong conclusion from true premises about filenames. Here
the Foreman drew a wrong conclusion from true premises about a constant and a
rejection site. **Both were caught by someone who ran the thing rather than
reading around it** — Track 0 round 2 by opening the schema whose name gave no
hint, Track 2 by executing the two code paths against the same input.

The census's method is vindicated by this, not embarrassed by it. Three
isolated readings plus an adversarial reconciliation that is required to
spot-check agreements is exactly the structure that surfaces an error the
Foreman planted in the corpus himself.

## Actions taken

- This record filed.
- A superseded-marker note inserted at the false clause in the closed Track 0
  deliverable, pointing here. The original wording is preserved struck, not
  deleted; the Track 0 record of what was ruled and why must remain readable.
- Track 0 representational gap 8 annotated as **realised, not latent**.
- Track 2 accepted at `f276cc5b`.

## Actions deliberately not taken

- `_predicate_depth` not changed. No production code changes in this
  milestone.
- ADR-0066 not amended. This milestone produces no ADR.
- The 5b-ii label not re-opened. A reader who rejects the
  enforcement-versus-declaration distinction still reaches `adjacent`; that
  disagreement was already recorded and stays recorded.
