<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "eic-married-one-path",
  "status": "Open 2026-11-24. Track 1 built; fresh review next.",
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

## Track 1 result

Evidence: `eic-married-one-path-evidence/track1.md` (published core v105,
registry v103, release v103, from published v104).

- **Published.** Successors of the two married-taxpayer selection rules
  are new files, 4,296 and 4,360 bytes, under the 5,000 earned-income cap
  the `rule.eic-*` guard already applies. Each keeps the separated-recorded
  path and the v1 default on rule-artifact v17. Package v105 replaces only
  those two pins (v1 on rule-artifact v14 to v2 on v17). The registry adds
  those citizens and the v105 row. The release differs from v102 in version
  and the registry digest. Loader v105 carries v104's map and declaration.
  No schema manifest changed. Published v104 and the v1 rules were not
  edited. The package is 241,297 bytes, the same size as v104. The registry
  is 322,194 bytes.
- **Same plan when the inert path is inactive.** The runner counts active
  paths, not declared paths. With no separated-spouse fact, v1 and v2 both
  take the default. With only that fact, both take separated-recorded.
  Neither v2 file names the inert fact. A stored inert fact is still
  refused at assertion.
- **Replay.** All 775 recorded lists pass, v104 against v105. 691 carry
  the package version and 84 are identical errors. Zero unexpected
  differences and no number change. The two rule-version expectations are
  unused because those rules are not pinned on the recorded lists.
- **Tests.** The package test, the size guard, the covered-flag list, and
  the 37 live cases passed. The fast lane passed (1,984 passed, 8 skipped,
  6,001 subtests). mypy reported no issues in 545 source files.
