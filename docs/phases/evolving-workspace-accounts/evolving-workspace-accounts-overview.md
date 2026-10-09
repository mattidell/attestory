# Evolving Workspace Accounts

## Purpose

A person tells the application more over time. They add details, correct an
answer, withdraw a connection, or describe something that challenges an earlier
assumption. The application should improve its account without losing what
the person said or treating a software limitation as a problem in their life.

Tax Concept Derivation demonstrated a bounded path from reported amounts and
ordinary circumstances to calculation and explanation. This phase asks how
that account changes coherently when more information arrives.

The owner's organizing principle is:

> New information changes the conclusions and assumptions it bears on. It does
> not automatically erase earlier statements or change unrelated subjects.

Four changes can look similar but mean different things: retiring an input
method, superseding a person's statement, changing the support for a conclusion,
and changing an assumption. Understanding their relationships comes before
choosing storage, schema or lifecycle mechanisms.

## Opening boundary

Start with two student-loan interest statements. One gains borrowing and
schooling details; the other retains its older eligibility answer. The current
return-wide choice of input methods refuses that combination even when both
accounts can support a result. This is a concrete place to investigate the
principle, not a mandate to build a universal conflict-resolution engine.

The first milestone is [Updating an Account Without Losing Its Meaning](milestones/account-refinement.md).
Its plan separates semantic questions, current implementation restrictions,
and evidence needed before selecting a build.

## Scope and boundaries

Explore how incoming information relates to existing answers, how adopted
rules use that information, and how the saved explanation communicates the
resulting basis. Domain models in plain language can describe more than the
first implementation supports; they are working understanding, not contracts.

No general assumption engine, free-text interpretation service, institutional
verification service, broad intake UI or new tax coverage is selected. The
owner may revise the roadmap as concrete cases expose better questions.

## What would justify concluding this phase

At least one production transition preserves the person's account while
changing its use in calculation, without disturbing an unrelated account.
Its tests distinguish additional detail, correction, adverse information and
unresolved information. A saved explanation lets another reader distinguish
what was said, what was used and what was assumed before and after the change.

The project should also have a short, understandable model of that transition
and its limits. This does not require solving every kind of assumption or
supersession. Reassess these provisional exit goals after the first milestone.

## Inherited evidence boundary

The preceding phase is concluded as a bounded derivation-and-explanation
demonstration, not complete tax coverage. Its reader was inspected by the owner;
an independent context-starved reader assessment remains unperformed. The new
phase does not silently upgrade that evidence or promise to fix every carried
engineering follow-up.
