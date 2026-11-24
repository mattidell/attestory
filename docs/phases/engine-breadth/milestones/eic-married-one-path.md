<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "eic-married-one-path",
  "status": "Open 2026-11-24. Track 1 next.",
  "retrospective": null,
  "scope": [
    "the two earned income credit married-taxpayer selection rules published in core v103 carry one path on rule-artifact.v17 instead of a second path keyed on a fact nothing asks",
    "every computed result, question and recorded return is unchanged"
  ],
  "non_goals": [
    "no change to the married-taxpayer question, its fact, or any credit",
    "no kernel, engine, schema or page change; the published eic.married-taxpayer-inert fact type stays in its bundle (published bytes) and simply has no reader",
    "no change to the thirty-one older rules the selection-keyed-collect survey listed"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/eic-married-one-path.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/eic-married-one-path.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/eic-married-one-path.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/eic-married-one-path.md"
    ]
  }
}
-->

# The Married-Taxpayer Rules Need No Inert Path (2025)

Milestone key: eic-married-one-path.
Branch: milestone/eic-married-one-path-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-24.
Starting point: main at `66ce8a86` (core v103, registry v101, release v101).
hoh-no-worksheet-ceilings (#305, core v104) is in flight; Track 1 publishes
core v105, registry v103, release v103 once it merges.

## What we are trying to accomplish

eic-separated-married (core v103) published
`rule.eic-married-taxpayer-recorded` and
`rule.eic-married-taxpayer-from-separated` on `rule-artifact.v14`, whose
`selection.paths` needs at least two items, so each carries an inert second
path keyed on `eic.married-taxpayer-inert`, a fact nothing asks and that
is refused at assertion. `rule-artifact.v16` and `v17` accept one path
(the selection-keyed-collect survey noted this for thirty-one older rules,
and core v104's worksheet successors already use v17). Neither that
milestone's builder nor its reviewers noticed.

## Stages

1. **Track 1** (no P0; the design is mechanical). Successors of both rules
   on `rule-artifact.v17` with only the `separated-recorded` path and the
   same default, publishing the same values for every input. Prove it:
   the eic-separated-married live tests pass unchanged on v105; a
   full-surface replay v104 against v105 shows only the two version moves;
   a scratch check that a stored inert fact no longer reaches either rule.
2. **Fresh review**, repair, closeout.

## Decisions

1. The inert fact type stays in its published bundle; nothing reads it
   after v105. Its refusal at assertion stays, so a saved return can never
   carry it.
