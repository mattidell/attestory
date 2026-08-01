# Explanatory-walk contracts — working notes

Referenceable, not formalized. These are candidate shapes the entry-loop
explanatory walk (`entry_loop.py` + `EntryPage.svelte`) already exhibits or
could grow into, named so future work can point at one instead of
re-describing it. Status on each is honest: some are load-bearing today,
some are a single instance pretending to be a pattern, some are just an
idea. Nothing here blocks or gates anything — it's a map, not a contract in
the enforced sense.

## What exists today (built, working, live-tested)

**IIdentifiable** — a stable id (`line.line`) used as dictionary key and DOM
anchor. Implicit everywhere, never named. Only matters once a second entity
kind exists and "line" stops being an adequate field name.

**ITraversable** — identifiable + rendered as a focusable DOM node
(`id="line-${id}"`, `tabindex="-1"`) that a jump action can scroll to and
focus. Complete for lines (`jumpToLine` in `EntryPage.svelte`). Untested
against any non-line entity — the anchor-naming scheme (`line-${id}`) is
still literally spelled "line."

**IExplainable** — presence of `.explanation` gates the toggle+panel UI
(`{#if line.explanation}`). The interesting part isn't the presence check,
it's the precondition behind it: an explanation may only be built from data
the record already published (ADR-0046 zero-authority carried into this UI
layer). Call the full contract **IExplainable, fail-closed** — a node that
can't honestly explain itself returns no explanation, not an invented one.
`_line_explanation` in `entry_loop.py` already does this; it's just not
named as a rule other entities would need to follow.

**Leaf / Composite / Unsupported** (a three-way classification, not the
strict Leaf-XOR-Composite I first reached for) — every explainable node is
exactly one of:
- **Leaf**: value sourced from evidence outside this explanatory system
  (`citedEvidence` populated, `dependsOn` empty).
- **Composite**: value derived from other explainable nodes of the same
  family (`dependsOn` populated).
- **Unsupported**: neither (`hasSupport: false`, e.g. line 12's standard
  deduction) — an honest empty state, not a bug.

This is the load-bearing one. It's what let the same UI machinery handle
both "here's the W-2 evidence" (leaf) and "here's lines 11 and 12" (composite)
without the template knowing which it's looking at.

**Evaluation checklist for a new entity** (does X fit this system?):
1. Stable id? → IIdentifiable
2. Can render a real DOM anchor worth focusing? → ITraversable
3. Explanation computable from already-published data only, else refuses? →
   IExplainable, fail-closed
4. Leaf, Composite, or honestly Unsupported? → classification
5. (see below) any meaningful predicates or actions on it?

If 1–3 fail, the entity doesn't fit this system yet — that's information,
not a blocker to route around.

## What's a single instance pretending to be a pattern

**IContextualized action** — `tracesToEntry` is one boolean, computed by one
predicate (`_reaches(dependency_graph, line, "1a")`), gating one button
("Jump to W-2 entry"). It works, but it's an instance, not yet a vocabulary.
The generalization the user is pointing at: a small **predicate algebra**
over nodes — `reaches(target)`, `isLeaf()`, `isComposite()`, `hasSupport()`,
composable (`isLeaf() and hasSupport()`) — with each UI affordance gated by
a predicate expression instead of a bespoke server-computed boolean per
affordance. Not built. Worth trying the next time a second action or a
second reachability target shows up — two instances is when you find out if
the algebra actually wants to exist, or if one-off booleans were fine.

## Aspirational — named, not attempted

**Command pattern for actions** — reify "Jump to W-2 entry" as
`{ id, label, isValid(), run() }` instead of a hardcoded button wired to
`goToWages()`. A node would carry `actions: Command[]`, rendered by
iterating rather than by one `{#if tracesToEntry}` block. Cheapest way to
test whether this is worth it: convert the *one* existing action into this
shape and see if it reads as clearer or as ceremony for n=1. Command is also
the natural place for "connector" language — a Command is a typed link
between a UI affordance and a capability that lives elsewhere (the wage
correction handler today; maybe a rule-definition viewer or a
flag-for-review action later).

**Explanation builders / chaining** — `_line_explanation` currently computes
everything eagerly in one function. A builder/pipeline shape would instead
compose independent, skippable transforms — `withRule`, `withDependencies`,
`withEvidence`, `withActions` — each one gated by a predicate from the
algebra above (`when(isComposite(), withDependencies)`). This is what would
let the predicate algebra and the Command pattern actually compose with each
other instead of each living as its own special case. Natural to attempt
*after* there's a second predicate and a second action — building the
pipeline for one of each is premature.

## Suggested order if this thread continues

1. Add a second action (even a trivial one) to force the Command-pattern
   question to be real instead of hypothetical.
2. Once there are ≥2 predicates in use, extract the algebra rather than
   leaving them as separate booleans.
3. Only then consider the builder/pipeline shape — it exists to let (1) and
   (2) compose, and has nothing to prove on its own.
