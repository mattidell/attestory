# Phase Overview: Grammar Census

- Phase key: `grammar-census`
- Status: **ACTIVE 2026-08-19**, owner-selected explicitly and independently of
  Claim Boundary Exploration (running in parallel on a different branch and
  worktree).

## Purpose

The engine's declarative rule and semantics language accumulated incrementally
as tax milestones required new capability. Before extending it again or
comparing it against external systems, the project needs a trustworthy,
reconciled account of what language actually exists today: its layers,
constructs, sources of authority, runtime interpreters, actual committed use,
and the points where schema, runtime, content, and observed behavior agree or
diverge.

This is a documentation-and-evidence phase. It produces no grammar change, no
ADR, no governance interpretation, and no external-standards claim. It scopes
a later comparative-semantics review rather than performing one.

## Scope

- Bound the term "grammar" against the engine's actual layers (rule-artifact
  clause/expression language, dependency/guard/applicability/value/
  publication/blocking semantics, operation-specific semantic specifications,
  package selection/binding/closure/output-ownership rules, adjacent
  predicate/validation languages, runtime behaviors that carry meaning without
  being grammar, and provenance/disposition/explanation consequences).
- Reconcile declared (schema/contract), implemented (runtime), and used
  (committed content) construct sets independently before synthesizing them.
- Produce a per-construct census, a small set of representative end-to-end
  traces chosen for semantic contrast, and a tension catalog limited to
  potentially actionable items.
- Produce a bounded external-comparison brief that scopes a future comparative
  review without adopting a model to imitate.

## Exit criteria

See the opening milestone plan's exit criteria for that milestone.

**The phase does not close when the opening milestone closes.** Grammar Census
remains open pending the owner's next selection. The closing milestone
presents bounded choices for what follows — comparative review, a focused
grammar decision or build, further internal verification, or stop — and the
owner selects among them. A decision to stop closes the phase; nothing else
does, and no milestone closes it automatically.

## Relationship to other phases

Independent of Claim Boundary Exploration. Both are active concurrently in
separate worktrees on separate branches from `origin/main`; neither blocks the
other. This phase makes no claim about, and does not read from, Claim Boundary
Exploration's inquiry corpus.
