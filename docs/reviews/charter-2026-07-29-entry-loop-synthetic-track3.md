# Charter — The Entry Loop (synthetic), Track 3: the entry-field contract

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Evidence: `docs/reviews/2026-07-29-entry-loop-synthetic-track2e-aggregation.md`
  and `docs/reviews/2026-07-29-entry-loop-synthetic-track2-aggregation.md`
- Review gate: yes, Reviewer, after the build.

## Why this track exists

Two evaluation rounds have now been run against a synthetic W-2 entry surface,
by four independent evaluators under two briefs. The surface works: nineteen of
twenty criteria pass, including the judgement criteria that turn on what a
person can state without guessing.

The point of building it was never the form. It was to find out what an entry
surface has to **declare about itself** so that the next one — for interest, for
dividends, for a fact family nobody has thought about yet — does not have to
rediscover the same things by failing an evaluation.

This track writes that down. It is the deliverable the milestone was for.

The owner's standing direction governs it: **model the criteria and the
implementation as schema, not as an accumulation of mechanical checks.** This UI
may well be thrown away. Anything learned that lives only in a hex value, a
Svelte template, or an assertion about a specific rendered string dies with it.

## Scope, fixed by owner decision

**Model the entry-field contract. Do not model the presentation surface.**

The presentation role/context model waits until a second surface exists to
generalise from — building it now from one example would be inventing structure
rather than extracting it. Even though this milestone produced good evidence
about presentation (see "What the evidence says about presentation" below), that
evidence gets **recorded**, not modelled.

If you find yourself designing how surfaces should look or how indicators should
be themed, you are outside scope.

## 1. The field contract

Model what an entry field must declare about itself. The evidence says it is at
least these, and you should say so in whatever vocabulary the repository already
uses for schemas:

- **Source** — the document a person is holding, and the exact box or line on it
  (`Form W-2`, `Box 1`). Criterion 2.1 is currently satisfied by rendered text;
  it should be satisfiable by checking a declaration.
- **Destination** — the return line the value feeds (`Form 1040 line 1a`).
- **Purpose** — what completing it resolves, in terms a person reads. This is
  what makes 2.2 pass, and 2.2 explicitly rules out a bare "required".
- **Accepted format** — already built and already working. Track 2d's
  `w2-box1-format.js` is the prototype of this field, and it is the part of the
  contract with the most evidence behind it: one declaration governing the hint
  a person reads, the validator that accepts or refuses, and the refusal
  message. Generalise the shape; do not regress the behaviour.
- **Correction affordance** — how an already-answered fact is located and
  changed without restarting the session.

**The test of this model is 2.1, 2.2, and 2.3.** Those three criteria are
currently checked by an evaluator reading rendered text. After this track, it
should be possible to check them against declarations, with rendering derived
from the contract rather than asserted alongside it. Say plainly how close you
got, and where a human evaluator is still irreducibly required — some of these
criteria are judgement criteria and may not be fully mechanisable, which is a
legitimate finding rather than a failure.

## 2. What the format work taught, and one seam to name

Track 2d read a JavaScript declaration from Python by string-matching an
`export const` marker, so the surface and the derivation layer shared one source
of truth. It works, and the reviewer explicitly deferred it rather than treating
it as a defect.

It is also the load-bearing seam of the whole idea, and it is currently a marker
string in a `.js` file parsed by hand. Name it: say what the field contract's
canonical form should be, which side owns it, and how both sides read it without
one language parsing the other's source. **You do not have to build that
migration.** Recommend, with reasons.

## 3. Record what the evidence says about presentation

Not a model, not an ADR. A short record, in the milestone's documentation, of
what two evaluation rounds established. Keep it to what was actually observed:

- **The accessibility row failed twice on the same element for the same
  structural reason.** Track 2c correctly fixed focus contrast across background
  contexts, and the amount input was missed anyway, because the model was
  *indicator versus background* when the missing rule was *every focusable
  control must have a focus indicator distinct from its resting boundary*. The
  input had a strong resting boundary and no focus treatment, so it looked
  handled. Write down that a future presentation model needs the per-control
  rule, not only the per-context one.
- **The instrument cannot measure part of what it asserts.** Four evaluators
  across two rounds could not exercise Tab/Shift+Tab traversal or Enter/Space
  activation through the harness. The controls are native `<button>` elements so
  the requirement is almost certainly met by construction, but "almost certainly"
  is not a measurement, and a mechanical criterion has gone partly unverified
  twice.
- **The accessibility row bundles five requirements into one Pass/Fail**, so one
  narrow miss sinks a row that is otherwise comfortably met.
- **The criteria conflate two things under "without guessing"**: whether a person
  has enough knowledge to state a correct answer (judgement) and whether the
  system honours what its own guidance licensed (mechanical). The first run's
  dispute was this conflation surfacing as a disagreement. The owner resolved it
  and the repair proved the point.

These are observations about the instrument and the surface, for whoever writes
the next version of either.

## Boundaries

- **Do not amend the criteria document.** It is owner-accepted, it caught real
  defects in two rounds, and rewriting the bar after the fact is the one thing
  this process does not permit. Recording findings against it is not amending it.
- **Do not fix the open accessibility defect.** The amount input's focus
  indicator is a separate repair unit; doing it here would tangle a model with a
  CSS fix and make both harder to review.
- Do not score or re-score anything. Do not predict a cell verdict.
- **No maturity movement.** The W-2 cell stays at L1; the cell verdict is FAIL
  and this track does not change that.
- Do not build a second fact family, do not touch the residency locator, do not
  introduce real data. W-2 and synthetic throughout.
- Do not ratify ADR-0049 or ADR-0051. Both are proposed and both are the owner's
  at the milestone close.
- If the model wants to become an ADR, say so and stop. Proposing an ADR is an
  owner decision, not a builder one.

## Two carried findings to dispose

Neither blocks, both should get a sentence saying what happens to them:

1. The duplicate/out-of-order coverage passes because the kernel's
   `apply_contribution` refuses contribution-id reuse, so it does not prove
   `entry_loop.py`'s own staleness check does any work.
2. `launchChrome()` in `tools/presentation_harness/lib/chrome.mjs` leaks an
   orphaned Chrome process and its `mkdtemp` profile directory when the calling
   process is killed on timeout.

## Verification

The CI `verify` sequence, or a stated subset with each omission justified, plus
the data-safety scan and the commit you worked from — **in the commit message.**
Two repairs in this milestone recorded partial or no verification and the foreman
had to re-run them; the last one had a mypy regression that only a full run
caught.

Orient with `python3 tools/foreman_context.py --ref HEAD --format markdown` and
`python3 tools/build_orientation_block.py --ref HEAD`. If either refuses, stop
and report it rather than working around it — it refused for both Track 2e
evaluators and that should not have happened twice. No `.venv`; use system
`python3`. Ratified line `origin/main-ui`.

## Report back

What the field contract declares and in what form; how much of 2.1, 2.2, and 2.3
can now be checked against declarations rather than rendered text, and what
irreducibly cannot; your recommendation on the JS/Python seam and why; what you
recorded about presentation; and the one thing in the model you are least
confident generalises beyond W-2.
