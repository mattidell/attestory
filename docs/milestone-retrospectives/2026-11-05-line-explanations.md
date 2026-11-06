# Retrospective: Every Line Says What It Adds (2025)

Milestone key: line-explanations. Plan:
`docs/phases/engine-breadth/milestones/line-explanations.md`.
Closed 2026-11-05.

## What happened

A parked note said many form lines explain nothing: line 9 said "published
total income" and many guards said "guard false". P0 inventoried all 73
fields on core v77 (365 texts, 126 generic, 36 fields with a generic text
the page can show) and found that new field versions and a package
successor were enough. Its drafted wording was still generic ("is zero
because the calculation comes to zero"), so the foreman set a wording
standard. Track 1 succeeded 31 fields on core v78. The fresh review found
nine sentences false on some return. The repair fixed them; the foreman
rewrote the last one, line 16's guard.

## What worked

- Rendering the page in P0 showed which texts a filer can read at all: a
  blocked line's own text is hidden when questions show, and 20 guard texts
  can never be selected. That cut the work to what a filer sees.
- A reviewer reading each sentence against its rule's `when` found false
  statements that the values-equal cases could never catch: rounding
  zeros, inverted scope guards, a blocked text naming the wrong input.

## What to change

- A wording standard belongs in the P0 charter, not after P0. Drafting
  first and setting the standard second produced a draft list that could
  not be used.
- A guard sentence should be written from the rule's `when` read aloud,
  then shortened. Both long guards started as a list of every compare.

## Follow-ups

- Show a blocked line's own text beside its questions, and decide what a
  numeric line with no citation shows (page behaviors).
- Name more than a rule's first cause when it blocks.
