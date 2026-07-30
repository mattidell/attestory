# Charter — The Entry Loop (synthetic), Track 0 review: usability criteria for entry

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Under review: `0ddc0a5` — `docs/phases/legible-entry/entry-usability-criteria.md`
- Builder charter: `docs/reviews/charter-2026-07-28-entry-loop-synthetic-track0.md`
- Verdict: `READY` or `NOT READY`, with findings.

## What this track was for

The next track builds a guided entry loop for W-2 on a synthetic workspace. In
this phase a matrix cell reaches L2 when a usability evaluation passes, not when
someone inspects the surface and approves it. This track wrote that evaluation
*before* the surface exists, so that the bar was not shaped by the thing it
scores.

So the question in front of you is not "are these reasonable usability ideas."
It is whether this document can actually be run as an evaluation, by someone who
did not write it, against a surface nobody has built yet.

## Measurements

Take each in turn and say what you found.

**1. The sharpness test.** The builder's charter set it: two competent
evaluators looking at the same surface should reach the same verdict on most
criteria without negotiating. Apply it criterion by criterion. For any criterion
where you believe two evaluators could reasonably split, say so and say why.

**2. The mechanical/judgement split.** Each criterion is labelled one or the
other. Check the labels against the criteria. A criterion labelled mechanical
that in fact requires a judgement call is a defect in the instrument, because
the scoring procedure treats the two classes differently and treats a mechanical
failure as fatal.

**3. Implementation independence.** The charter forbade anything that depends on
knowing how the surface will be built. Check whether any criterion presumes a
particular interaction model, layout, or technology. A criterion that can only
be satisfied one way has quietly designed the surface.

**4. The ADR-0046 disposition.** The document says which of the presentation
contract's rules carry over to entry and which do not. Open
`docs/adr/0046-presentation-surface-contract.md` and check each claim against
what the ADR actually says. Both directions matter: a rule wrongly carried over
imposes a bar entry should not have, and a rule wrongly dropped removes one it
should.

**5. Is the scoring procedure runnable, twice?** Who evaluates, what they are
given, what happens to disagreement, what a pass is, who decides. Read it as
someone who has to execute it. Name anything you could not do from the text
alone. Pay particular attention to whether the pass rule and the disagreement
rule are consistent with each other.

**6. Coverage of the five steps.** Know what is missing, enter a fact, see it
land, correct an entered fact, know the return is complete. Is any step
under-served relative to what it has to prove? Step 5 is the least obvious and
the milestone plan flags it as such.

**7. Scope.** The milestone deliberately leaves the per-field explanation schema
to emerge from the build and records it at close. Check that this document
describes what a field must *accomplish* and has not started specifying the
structure that carries it. Also check it stayed documentation — no product code,
no prototype.

**8. Stated dependencies.** The document's evaluation setup may rely on premises
this milestone has not yet confirmed against the code. Identify any premise it
rests on, and say whether the document is honest about resting on it. Do not go
confirm the premises yourself; that is Track 1's job. Naming them is yours.

**9. Verification.** The builder's charter required a stated verification: the
CI `verify` sequence or a subset with each omission justified, including the
data-safety scan, and the commit worked from. Check the record contains it.
Report its absence as a finding if it does not.

## Boundaries

- Do not rewrite the criteria. Report findings; repair is a separate charter if
  the owner authorises one.
- Do not evaluate a surface. There is none.
- Do not lower or raise the bar because you would have written it differently.
  A criterion you disagree with but that is sharp, correctly labelled, and
  runnable is not a finding.
- No product code. No maturity claim; nothing moves on any matrix.

## Verdict

`READY` or `NOT READY`. If `NOT READY`, each finding gets a number, a statement
of what is wrong, and what would close it. Distinguish findings that make the
instrument unrunnable from findings that make it weaker — the first block, the
second are worth recording either way.

## Report back

The verdict; each measurement and what it found; which criteria you judged
unsharp or mislabelled and why; what you checked ADR-0046 against and what you
found; and the single thing most likely to go wrong when someone tries to run
this evaluation for real.
