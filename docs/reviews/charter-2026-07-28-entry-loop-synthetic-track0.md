# Charter — The Entry Loop (synthetic), Track 0: usability criteria for entry

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Deliverable: `docs/phases/legible-entry/entry-usability-criteria.md` — the
  criteria a guided entry loop must meet, and the procedure that scores a cell
  against them.

## What you are writing, in one sentence

The bar that the next track has to clear, written before that track exists, so
that the thing scoring the entry surface was not shaped by the entry surface.

## Why this comes first

In this phase a matrix cell reaches L2 when a usability evaluation passes — not
when a builder or reviewer inspects it and approves. That evaluation has never
been written. If it gets written after the surface is built, it will describe
whatever got built, and the L2 claim will be circular. So it goes first, and
the builder who comes next aims at a bar someone else set.

That is the whole point of this track. Nothing you write here should depend on
knowing how the surface will be implemented.

## What the criteria are about

The loop, not the form. Five steps, and the criteria should cover each:

1. **Know what is missing.** What must a person be able to tell about the gap
   between where their return is and where it needs to be?
2. **Enter a fact.** What must a person be able to tell about a field *before*
   they type in it — what it is asking for, why it is being asked, what a
   correct answer looks like, where the number comes from on a real document?
3. **See it land.** What must they be able to tell *after* — that it was
   accepted, what it changed, what it did not change?
4. **Correct an entered fact.** Can they find a fact they already answered,
   change it, and understand the result?
5. **Know the return is complete.** What does "done" have to look like to
   count? This one is the least obvious and worth the most thought.

Be specific to entry. "The interface should be clear" is not a criterion.
"A person can state, without guessing, which document and which box a field is
asking them to read from" is.

## How specific is specific enough

Two competent evaluators looking at the same surface should reach the same
verdict on most criteria without negotiating. That is the test to apply to your
own draft. Where a criterion cannot be made that sharp, say so and mark it as
requiring judgement rather than pretending it is mechanical — the split between
what is checkable and what needs judgement is itself useful, and prior work in
this project measured roughly two thirds of UI quality as mechanizable.

## The scoring procedure

The criteria are half of it. The other half is how a cell gets scored:

- **Who evaluates.** The phase's method is a mix of agent viewpoints, chosen so
  that different backgrounds meet the same material. Say how many, and what
  makes them different from each other in a way that matters.
- **What they are given.** Define the evidence an evaluation runs against, so
  the same evaluation could be run twice.
- **What happens to disagreement.** Where evaluators disagree, that is signal.
  Say what happens to it. Do not average it away into a score.
- **What a pass is.** Per criterion and per cell. Say whether any criterion is
  individually fatal.
- **Who decides.** The owner reviews the criteria, the evidence, and the
  result. Say what is put in front of them.

## Prior art, and its limits

`docs/adr/0046-presentation-surface-contract.md` is the nearest thing this
project has: zero-authority foreclosure, blanket redaction of rejected values,
section-level blocked-state salience. Read it. **Do not assume entry inherits
it** — it was written for a surface that only displays, and this phase inverts
that. Where a rule of ADR-0046 carries over, say why. Where it does not, say
that too.

`docs/prototypes/human-presentation-citation-walk/analysis/` holds the
evaluation-method findings from the exploratory milestone. Useful for how to
run an evaluation; not a source of entry criteria.

## Boundaries

- **No product code.** Not a prototype, not a sketch, not a mock. If you find
  yourself needing to build something to know what to write, that is a finding
  — report it, do not build it.
- **No per-field explanation schema.** The milestone deliberately leaves that
  shape to emerge from the build and records it at close. You are writing what
  a field must accomplish, not what structure carries it.
- **Nothing is scored in this track.** There is nothing to score yet.
- **No maturity claim.** No matrix cell moves.
- W-2 is the family the next track builds, so ground your examples there. The
  criteria themselves should not be W-2-specific unless there is a reason.

## Stop conditions

- The criteria cannot be written without knowing the implementation. That would
  mean this track is in the wrong order, and it is worth knowing.
- ADR-0046 turns out to constrain entry in a way that makes a criterion
  unwritable until an ADR settles it.
- You conclude the phase's stated evaluation method — agent evaluators, owner
  decides — cannot produce a defensible L2 verdict. Say so plainly. That is a
  finding worth more than a document written around the problem.

## Verification

The CI `verify` sequence, or a stated subset with each omission justified.
Include the data-safety scan. This track is documentation, so most of the suite
will be unaffected; say which parts you ran and why the rest do not apply.
State the commit you worked from.

## Report back

The criteria and the scoring procedure; which parts are mechanically checkable
and which need judgement; what you took from ADR-0046 and what you rejected;
where you think the criteria are weakest; and any criterion you wanted to write
but could not make sharp enough to be worth having.
