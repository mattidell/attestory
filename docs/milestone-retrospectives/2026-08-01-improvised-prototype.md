# Retrospective — Improvised Prototype

Milestone: `docs/phases/legible-entry/milestones/improvised-prototype.md`
Phase: Legible Entry. Sixth milestone; the first owner-directed one that
actually built product (Milestone 5, the prior owner-directed slot, closed
without implementation).
Closed: 2026-08-01.

## What it produced

The synthetic W-2 entry loop no longer flattens the presentation model into
disconnected status rows. Every evaluation line (all nine — the five that
change with wages and the four held for comparison) can expand into a
walkable explanation, reusing the presentation model's own already-computed
data: description, governing rule identifier, operation/parameter
identifiers, and either its immediate dependency lines (an aggregation or
bracket computation) or its cited evidence (a directly sourced amount) —
never both, never invented. A person can start at line 16 (tax), follow real
dependency chips back through 15, 11, 9, to 1a and the W-2 evidence itself,
correct the wage figure from wherever they are in that chain via a scoped
"Jump to W-2 entry" action, and watch every open panel update coherently.
Panels don't collapse as you navigate — the whole trail stays visible,
functioning as its own breadcrumb.

Two structural pieces of supporting work: a small predicate
(`_reaches` over a dependency graph built from the record's own finding
pins) that both gates the correction action on a line and annotates
dependency chips with whether they lead back to the entered fact before
they're clicked; and a working notes pair
(`docs/phases/legible-entry/milestones/improvised-prototype-contracts.md`,
`...-retrospective.md`) naming the UI shapes this round actually used —
IExplainable, a Leaf/Composite/Unsupported classification, and a
Command-pattern action, tested against a real second instance and then
partly reverted once it had answered the question it existed to answer.

## What actually happened

### The record already carried more than the UI showed

Nothing in this milestone required deriving new tax meaning. Every
experiment was "stop discarding data the coordinator already computed," not
"compute more of it" — the dependency graph, the rule/operation/parameter
identifiers, the evidence labels were all already present in
`presentation_projection.py`'s output; `entry_loop.py` was flattening them
away one function in. This matches the milestone's own stated constraint
(never invent a second explanation) working as a real design forcing
function rather than a formality.

### Reviewer cycles found real defects a build-and-inspect pass would have missed

Five review rounds ran across this milestone — an initial structured
review, two independent fresh-eyes comprehension tests (agents driving a
real headless browser with no source access), and a final holistic review
scoped to one question. Each surfaced something concrete and each was acted
on before the next round: a dead-end toggle on blocked lines, a raw
internal identifier presented as if it were evidence, unrelated correction
actions implying false causality, lost context across navigation, branching
ambiguity at multi-dependency lines, and (this round's own finding, not yet
fixed) a scroll reset after correction that silently relocates the reader
away from the panels they were reading. None of these were caught by the
test suite; all were caught by someone actually using the rendered page.

### Mechanized and human-simulated testing caught disjoint failure classes

The keyboard-operability probe (already part of this fixture's test suite)
caught three defects invisible to manual review: two controls sharing one
accessible name once several panels could be open simultaneously (twice —
once on toggle buttons, once on a since-removed second action), a Svelte
reactivity gap where state read only inside a helper function never
triggered a re-render, and a genuine Chrome quirk where `blur()` does not
reset the browser's internal tab-sequence pointer, exposed only once state
could persist across the test's phase boundary. None of these are things a
human or an agent narrating their experience would notice; all three broke
a specific, checkable invariant a script could verify. The inverse held too:
branching ambiguity and "does this read as one explanation or a pile of
boxes" are not things a script can check at all. Building both kinds of
verification in the same milestone caught defects neither would have found
alone.

### Predicate reuse, once demonstrated, immediately fixed a real gap

`_reaches(dependency_graph, line, ENTRY_LINE)` was built once, to gate a
line's own correction action. Applying the identical function to a
dependency reference instead of the line itself — no new logic — answered a
UX gap two independent reviewers had already named (which chip leads back
to the source, before you click it). This is the clearest concrete case
this milestone produced of a named abstraction paying for itself in code,
not just in naming.

## What worked

**Owner-directed mode did what it was built to do.** No criteria document,
no fixed track sequence, no maturity claim — the milestone charter's
explicit non-goals held throughout six rounds of real iteration, and the
next move each round was chosen from what the previous round's evidence
actually showed, not from a pre-committed plan.

**The record's own zero-authority discipline held under a direct request to
relax it.** Reviewers asked, reasonably, for human-readable rule and
operation names instead of raw identifiers like
`tax.us.2025.rule.form1040-line16`. Direct research confirmed no
title/description field exists anywhere in the record for rules,
operations, or parameters — this is a genuine content gap, not a UI
oversight, and the response was to say so rather than to invent prose that
would have read better and meant less.

**Live verification caught what static review would have missed twice.**
Both the Svelte reactivity gap and the Chrome tab-navigation quirk were
found only because every change in this milestone was exercised against a
real running server and a real (or headless-real) browser before being
declared done, not inferred from reading the diff.

## What to carry forward

- **Unfixed, reviewer-confirmed:** submitting a correction scrolls the page
  back to the top status banner, silently relocating the reader away from
  whatever citation panels they had open. The panels stay open and update
  correctly — the information isn't lost, just the reader's position in it.
- **Untested:** panels render at a fixed position matching the pre-existing
  line-list order, not the order navigated. It happened to look coherent
  here because the wages dependency chain matches that list's own order;
  never exercised against a dependency pointing somewhere outside it.
- **Open methodological question, not just an open feature:** the
  predicate "algebra" named in the contracts working notes has exactly one
  predicate (`reaches`), now used at two call sites. Whether that's enough
  to justify extracting a formal algebra, or whether it takes a second
  *distinct* predicate first, wasn't settled this round.
- **Unverified:** the trivial second Command-pattern action (copy a rule
  identifier to the clipboard) was built, proved the reified-action shape
  was worth it, and was then removed once it had answered that question —
  by design, not as an incomplete cleanup. See
  `improvised-prototype-contracts.md` for the reasoning.
- Full detail on criteria types, their tensions, and what the abstractions
  did and didn't buy is in
  `docs/phases/legible-entry/milestones/improvised-prototype-retrospective.md`,
  written mid-milestone rather than reconstructed at close.

## Process notes

No formal PR gated any single round; work landed as ordinary commits under
owner-directed mode, verified live and against the fixture test suite after
every change, matching the milestone's own charter. This is the closing PR.
