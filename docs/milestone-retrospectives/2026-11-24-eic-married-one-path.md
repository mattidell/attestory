# Retrospective: The Married-Taxpayer Rules Need No Inert Path

Milestone key: eic-married-one-path. Plan:
`docs/phases/engine-breadth/milestones/eic-married-one-path.md`.
Closed 2026-11-24. Core v105, registry v103, release v103.

## What happened

eic-separated-married (core v103) published two selection rules on
`rule-artifact.v14`, whose two-path minimum forced an inert second path and
a fact refused at assertion. While scanning the parked list the foreman saw
that `rule-artifact.v16` and `v17` accept one path. A grok builder moved
both rules to v17 with one path and proved no case or recorded list moved.

## What worked

- Reading the parked list after a milestone closes: a note left by an
  earlier survey answered a design compromise made the same night.

## What to change

- Before a builder works around a schema limit, check the newest schema
  version of the citizen; builders and reviewers on eic-separated-married
  all read v14 and none looked at v17.
