# An Ontology of Change

Status: exploratory, not binding.

## The Routing Problem

If disputes originate in change, then governing disputes means classifying
changes — an ontology of change whose purpose is routing: this kind of
change goes to that court. Type systems do exactly this for values (this
operation is checked at compile time, that one at runtime, this one is
undefined behavior and forbidden); an ontology of change does it for diffs.

The alternative to explicit routing is implicit routing, which every project
already has: everything goes to whatever court the author feels like, which
under time pressure is the null court. Explicit routing does not add
governance to an ungoverned system; it redistributes governance from mood to
policy.

## Axes of Classification

Several independent axes, each predicting something about the right court:

- Authority touched. Does the change alter canon shape (a schema, a graph
  node), canon content (a definition file, a parameter set), a derived view
  (generated docs, projections), behavior (engine code), vocabulary (a term
  of art), or process (the rules themselves)? Canon-shape changes are
  upstream of everything and deserve the strongest court; derived-view
  changes are mechanically checkable and deserve almost none.
- Reversibility. A change that one commit can undo differs in kind from one
  that other work will build upon within a week. Irreversibility is mostly a
  function of what gets built on top, which means it is a function of time —
  a useful reframe: the question is not "can this be undone" but "how
  expensive is this to undo after N more milestones."
- Blast radius. Local to a module; crossing a boundary; global to the
  system's shape. Boundary-crossing changes are where seam disputes live and
  where review attention pays best.
- Novelty. Routine changes have precedent; novel ones do not. Novelty is the
  single best escalation trigger, and it has a reliable phenomenology: the
  "sounds defensible but feels arbitrary" sensation is a novelty detector
  firing — it means the proposal is being justified by general convention
  rather than by anything specific to this system.

## Courts, Reprised

Mapped against the ladder from document 01, a routing table takes shape.
Illustratively, not prescriptively:

| Change class | Court |
|---|---|
| Derived views, formatting, internal refactors | Mechanical checks only |
| Routine content within settled shapes | Self-adjudicated, logged |
| New contracts other code will consume | Default-with-veto: decided, announced, reversible on objection |
| Canon shape, boundaries, vocabulary, anything novel | Judgment, recorded as a commitment |
| The rules themselves — principles, ontology, this table | Constitutional: slow, explicit, rare |

Two properties matter more than the table's contents. First, the routing
happens at declaration time: the change proposal states its own class, which
makes misclassification itself reviewable — an agent that declares a canon-
shape change as routine content has made a checkable error, which is a far
better failure mode than a silent one. Second, novelty overrides downward
routing: anything unprecedented moves up one court regardless of its
declared class. Precedent is what earns a dispute class its demotion to a
cheaper court; nothing starts cheap.

## The Cautionary Genre

There is a rich cautionary literature here, mostly written in blood by
enterprise IT: change-advisory boards, ITIL change management, deployment
freeze calendars. The consistent failure mode is court inflation — routing
ever more change classes to ever more expensive courts, because each
incident retroactively justifies one more gate. The result is a system where
the official process is so slow that all real change flows through the
emergency path, which has no court at all. The design discipline that
resists this: every court must be cheap enough that using it is easier than
evading it, and every escalation of a change class to a higher court should
carry a sunset — a scheduled re-examination of whether the promotion is
still earning its cost.

The opposite failure is subtler: routing tables that exist but are never
consulted because they live in a wiki nobody opens. The remedy is the same
one that works for all governance artifacts — put the routing where the
change is made (in the plan template, in the PR description, in the agent's
briefing), not in a separate ceremony. Law that is not encountered at the
moment of conduct might as well not exist; this is as true for a routing
table as it is for a speed limit.
