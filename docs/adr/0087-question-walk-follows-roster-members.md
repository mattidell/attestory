# ADR 0087 — The question walk follows a blocked roster member

- Status: **accepted** (owner, 2026-11-23, before PR #297 went ready)
- Tier: 2. A presentation-projection contract that later content is
  written against.
- Date: 2026-11-19

## Context

The saved page attaches a question to a blocked line only when every root
the line waits on is a closure family with a question, or a fact type with
an adopted input question (ADR 0046 Requirement 2; ADR 0086 for declared
names). Roster count rules (the earned income credit, child tax credit,
other-dependent child and relative rosters) block `DEPENDENCY_INVALID`
naming a member's subject key, for example
`eic.child.relationship|child=<member>,tax-year=2025`, when one member is
missing a per-member answer (`evaluator.py:283-285`). The member's own
blocked rows are recorded under that member's subject
(`subject_dispatch.py:719`), and the walk does not follow the key to them
(`presentation_projection.py:609-669`). So the page shows no sentence on
the 9 to 18 lines a missing child or relative answer blocks.

The eic-child-answers P0 showed that content cannot fix this. An input
question for a per-member fact is not reached. The closure questions are
not reached, because the roster is closed. Declared `missing` names on a
count rule reach a question for some tests, but cannot say which child the
question is about. They also leave the tie-breaker and relative answers
silent, and change the explanation of every return with a rostered member.

## Decision

1. **The walk follows a blocked member key.** When the question walk
   reaches a root that is a member's subject key (a per-subject read,
   ADR 0081: the four rosters today, and any other per-subject read whose
   member has its own blocked rows and adopted questions), it continues to
   that member's own blocked rows and walks their missing names as it walks
   any other root. A line gets a question only if every root, including
   each followed member, resolves to a question, as today.
2. **One reason per member, labelled with that member.** The reasons for
   a member carry that member's recorded label (the label the filer gave
   when adding the member, already present in the saved record) in one
   new optional reason field, `memberLabel`. The page shows it beside
   the question so a filer with two children knows which child is missing
   the answer. A reason with no member has no `memberLabel`.
3. **Explanation only.** The change adds no reads, pins, dependencies,
   values or refusal codes, and it changes no number, no rule and no
   published schema version. A member key that does not resolve to rows, or
   whose member has no single recorded label, leaves the line without a
   sentence, as today.
4. **Content supplies the questions.** Per-member answers become
   reachable only through adopted input questions for their fact types;
   a package that adopts none shows nothing new.

## Consequences

The eic-child-answers Track 1 changes `_closure_question_reasons` in
`packages/derivation/presentation_projection.py`, its reason validator,
and the page's reason rendering (`memberLabel`). It publishes sourced
input questions for the per-member answers of the four rosters, as a core
successor. Saved pages of returns with a blocked member gain question
sentences; no other output changes.

## Links

- Plan: `docs/phases/engine-breadth/milestones/eic-child-answers.md`
- Evidence: `docs/phases/engine-breadth/milestones/eic-child-answers-evidence/p0.md`
- ADR 0046 (presentation surface contract), ADR 0086 (declared missing
  names), ADR 0081 (per-subject conditional dependencies)
