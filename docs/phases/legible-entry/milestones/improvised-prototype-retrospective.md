# Improvised Prototype — retrospective, round 1

Taken mid-stream, after: line 1a walk → full 9-line dependency graph → chip
navigation → scoped correction action → honest "no support" note → stacked
(non-collapsing) trail → command-pattern actions (jump + copy) → chip-level
predicate annotation. Two independent fresh-eyes comprehension tests and
three owner reviews ran across this sequence.

## What we learned from the experiments

- The presentation model already carried the dependency graph, rule ids,
  operation/parameter pins -- richer than the UI exposed. Nothing new had to
  be derived; the work was almost entirely *stop discarding data*, not
  *compute more of it*.
- The real structural shape is **Leaf / Composite / Unsupported**, not the
  Leaf-XOR-Composite I first reached for. One template block handles all 9
  lines because of this three-way split, not despite the lines being
  structurally different.
- A predicate built to gate one thing (a line's own action) turned out to
  answer a second, different question (which dependency chip to click) with
  zero new logic -- same function, second call site. That's the clearest
  concrete win reuse gave us this round.
- Non-collapsing panels solved "lost context" (confirmed independently by
  both comprehension tests) but introduced a risk nobody asked for: panels
  render at a *fixed* position matching the pre-existing line-list order,
  not the order clicked. It happened to look coherent because the wages
  chain matches that list's order. Untested against a dependency pointing
  somewhere outside that fixed list.
- Mechanized tests and fresh-eyes tests are genuinely complementary, not
  redundant duplicates of each other. The keyboard-operability probe caught
  three real bugs (accessible-name collisions across simultaneously-open
  instances, a Svelte reactivity gap, a Chrome focus-navigation-pointer
  quirk) that no amount of visual/manual checking would have surfaced.
  Fresh-eyes testing caught the opposite class of thing (branching
  ambiguity, "does this feel like one explanation or a pile of boxes") that
  no script can check. Neither replaces the other.

## What remains open

- Chip order vs. navigation order (above) -- real but unexercised risk.
- Rule/operation/parameter ids are still raw identifiers. Confirmed by
  direct research: no title/description field exists anywhere in the record
  for rules, operations, or parameters. This isn't a UI gap, it's a content
  gap -- the zero-authority rule correctly refuses to paper over it.
- The predicate "algebra" named in the contracts doc has exactly one
  predicate (`reaches`), now used in two places. Whether two *uses* of one
  predicate justifies extraction, or whether it takes a second *distinct*
  predicate, is an open methodological question, not just an open feature.
- Explanation-builder/pipeline pattern: still untried, per the contracts
  doc's own ordering (premature before a second predicate exists).
- Clipboard copy's actual success is unverified -- the last comprehension
  test's sandboxed browser denied clipboard-read permission, so only the
  UI's own "Copied" feedback was confirmed, not the clipboard contents.

## Interaction patterns reviewers actually used

Both the owner and the fresh-eyes agents converged on the same rubric
independently: *trace a value back to its source, then attempt a
correction.* One is human reasoning in tax-domain terms (recognizing 1040's
structure to guess which chip mattered); one is a scripted agent that
explicitly avoided reading source and instead verified claims against the
DOM (confirming a "jump" action moved real keyboard focus, not just scroll
position, before treating it as a pass). That the same walk-trace-correct
protocol produced useful signal from both suggests it's a reusable
evaluation shape independent of who runs it -- worth keeping as the default
comprehension-test template rather than re-inventing one per round.

## Criteria: what exists, what moved, what's in tension

No formal criteria document exists for this milestone -- deliberately; its
own charter names "no maturity claim or broad criteria exercise" as a
non-goal. What actually governed decisions this round was **emergent, not
declared**, and it split into three distinct kinds:

1. **Hard/structural** -- zero-authority (never invent displayed text),
   fail-closed behavior, basic accessibility (unique names, real keyboard
   operability). Pre-existing, non-negotiable, inherited from project
   governance (ADR-0046) rather than discovered here. These *constrained*
   every experiment's design space from the start.
2. **Soft/emergent** -- coherence, predictability, "does this read as one
   explanation." Not derivable from governance; discovered by watching
   reviewers struggle, and refined after each round. These are what the
   experiments actually *produced*, not what they started from.
3. **Mechanized/procedural** -- keyboard traversal returns to its seed,
   activation produces an observed effect, no console exceptions. Checkable
   by a script with no judgment involved, and orthogonal to the other two:
   a control can be perfectly honest and perfectly navigable to a human
   while still failing this category on an accessible-name collision.

**Direct tension observed, not hypothetical:** the hard criterion (never
invent) blocks the soft criterion (coherence) exactly at the rule-id
display -- humanizing `tax.us.2025.rule.form1040-line16` would clearly read
better, and the record gives us nothing honest to replace it with. Separate
tension: the soft/product criterion (leave panels open across the trail)
directly broke a mechanized criterion's hidden assumption (Chrome resets
tab-navigation state on blur) -- satisfying one required fixing the other's
own implementation, not trading one off against the other.

**Time and sequence matter more than expected.** Several failures were
properties of *history*, not of any single render: two identically-labeled
buttons are only a problem once both are open *simultaneously* (a
consequence of the trail's persistence across time); the Chrome
focus-navigation bug only manifested because state persisted *across* a
phase boundary the test script assumed was a clean snapshot. Some criteria
that looked like simple per-render checks turned out to actually be
per-session checks once state was allowed to accumulate -- that distinction
wasn't visible until something broke on it.

## What we didn't foresee

- Comparison lines (2b/3a/3b/12) are computed *before* wage entry (they
  don't depend on the W-2 at all), so they had live, interactive
  explanations before the milestone's own "main event" -- an artifact of
  the return's actual structure, not a design choice.
- Svelte's legacy reactivity has a blind spot for state read only inside a
  helper function rather than at the template call site -- a framework
  surprise that produced a real, silent bug (the "Copied" label never
  updating) with no error or warning.
- The finding-id-matching approach to building the dependency graph
  resolved the entire 9-line graph correctly on the first attempt, with no
  special-casing needed -- better than expected going in.
- Headless-browser clipboard permission behavior is unreliable enough that
  the copy action had to be built defensively (non-blocking, feedback not
  gated on success) before we knew that was necessary.

## Abstractions, and whether they earned their keep

The contracts doc (`improvised-prototype-contracts.md`) named
IIdentifiable, ITraversable, IExplainable (fail-closed), Leaf/Composite/
Unsupported, an IContextualized-action predicate, and a Command pattern.
This round added one more, found empirically rather than designed in
advance: **a predicate can annotate an edge (a dependency reference), not
just a node's own actions.** `dependsOn` entries are now a small typed
shape -- a reference plus a predicate result -- not a bare pointer.

Concrete payoff, not just conceptual tidiness: reusing `_reaches()`
verbatim across both call sites fixed a real, reviewer-confirmed UX gap
(branching ambiguity) with zero new logic. The Leaf/Composite/Unsupported
split is what lets one template block serve nine structurally different
lines without per-line special-casing -- that's the abstraction paying for
itself in code size and correctness, measurably, not just in naming.

**Where the abstractions run out:** the *data*-side contracts (shape,
graph, predicates) are fully checkable without a browser -- most of this
round's graph and predicate logic was verified via direct JSON inspection
before a browser was ever opened. The *interaction*-side contracts
(ITraversable's actual focus-and-scroll behavior, name-uniqueness under
simultaneous-open state, the Chrome tab-navigation quirk) are not
independently checkable that way -- every bug actually hit this round lived
in that second category. These are two genuinely separate evaluation
surfaces. Treating the data-side abstraction as a stand-in for the
interaction-side one would have hidden every bug found today.
