# Craft Notes

Audience: Agents filling the foreman, builder, and reviewer seats.

A living record of **pithy, durable reminders** — the how-to-hold-the-tool
lessons that recur across tracks but belong in neither an ADR (they decide
nothing) nor a retrospective (they are not history). Each line is a
reusable heuristic with a one-line why, and — where it helps — the track
that earned it.

This file grows by **promotion**: when a retrospective or advisor counsel
surfaces a lesson worth carrying forward as craft, the owner approves and
the foreman records it here. Keep entries short; if a reminder needs a
paragraph, it probably wants an ADR or a plan section instead. Prune lines
that have hardened into tooling or ratified process.

## Foreman

- **Charter the invariant, not the symptom.** A remediation charter should
  name the end-state property you want ("select one explicit target; fail
  loudly if it is missing"), not just the outcome ("make the battery
  green"). Ask only for the outcome and a builder will reach it by the
  cheapest path — often reproducing the very shape that caused the defect.
  *(Track 3: the F1 fix re-introduced the first-match smell; a
  property-level charter would have collapsed the R1 round.)*

- **Exclude the charter commit from the object-under-review range.** When
  you charter a re-review of commit X, the object is X's own diff, not
  `charter-commit..X`. A range that swallows its own charter forces the
  reviewer to spend a finding reconciling file counts. *(Track 3: finding
  R2, and again on the next charter until explicitly guarded.)*

- **A clean first review is an upstream win.** When a build passes every
  content check on the first pass, the charter carried the prior track's
  lessons well — that is where the work paid off. When it does not, look
  first at what the charter left implicit, not at the builder.

## Builder

- **Verify a "pre-existing" failure against base before you claim it.**
  Never assert a failing test pre-dates your branch without running the
  base to confirm. The check is cheap; a misattribution is not — it can
  cost a full review cycle to unwind. *(Track 3: two failures claimed
  pre-existing were genuinely branch-caused.)*

- **Fix the shape, not the instance.** When remediating a fragility,
  remove the pattern that caused it (an implicit ordering assumption, an
  unguarded first match), not just the one occurrence that broke. Leaving
  the shape in place invites the next instance.

## Reviewer

- **Rerun load-bearing claims; don't accept the self-report.** The
  builder's own account of what the battery shows, or what pre-dates the
  branch, is input — not evidence. Independently rerun the base
  comparison, the live case, the failing test. *(Track 3: the reviewer
  disproved the builder's "pre-existing" claim by rerunning base.)*

- **Grep for the shortcut and the forbidden symbol.** Confirm goldens
  actually enter through the authoritative surface (`live_coordinate_run`,
  not a `RunContext` shortcut) and that forbidden bindings are truly
  absent — by direct grep, not by trusting the structure to exclude them.
