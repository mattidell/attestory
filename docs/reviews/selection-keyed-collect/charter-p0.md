# Charter: P0 of a selection path collecting a keyed family directly

Role: Builder. Source HEAD on milestone/selection-keyed-collect-2025.
Plan: docs/phases/engine-breadth/milestones/selection-keyed-collect.md
(read it whole). Background: docs/reviews/f1099b-backup-withholding/rereview.md
(findings 1 and 2) and the f1099b-backup-withholding retrospective.
Precedent for a versioned engine switch: the core-v75 closure-question and
core-v76 later-arm switches in packages/tax/loader.py. Do not read
governance.

## Scope

1. **Survey.** Every adopted rule, on every core, that publishes a
   stand-in value under a fact id so a selection path can name it, and
   every selection carrying a path on a fact type nothing writes. Write a
   small committed tool or test that finds them.
2. **Mechanism.** Read and cite the code that ties a path's `requires` to
   its collect (validation), withholds the path until the name is a symbol
   (runner), and binds or does not bind keyed assertions (marshal). Say
   why the stand-in works today.
3. **Design.** The smallest engine change that lets a selection path's
   collect be satisfied by its source family's current members (and the
   family's own activity), with no stand-in. Gate it by package so every
   earlier core behaves byte-identically. Say whether the two-path minimum
   should drop, and if so in which new schema version. Prototype on a
   scratch branch of the code under
   selection-keyed-collect-evidence/ only if it can be done without
   editing tracked files under packages/; otherwise write the change as a
   patch file in the evidence directory and apply it only in a temporary
   copy. Build a scratch core v86 that retires
   `rule.f1099b-b4-amount-symbol` and the inert path.
4. **Measure.** Run every case in the plan's "Cases that will shape the
   design" through `live_coordinate_run` on core v85 and scratch v86, and
   rerun every recorded return in
   tests/fixtures/f1099b_backup_withholding_v83/expected.json (as
   recorded, plus the box 4 yes/no answered no where core v85 asks it) on
   both. Show the explanation walks. Classify every change from measured
   runs.
5. **ADR.** Say whether this changes a rule-language contract. If it
   does, draft a proposed ADR under docs/adr/ using the repo's next free
   number and the shape in PROJECT_PLANNING.md; do not mark it accepted.

Stop and report before any edit to packages/kernel/ or to a published
schema file.

## Deliverables

In docs/phases/engine-breadth/milestones/selection-keyed-collect-evidence/:
- p0.md: survey, mechanism, design, measurements, ADR verdict, and a
  recommendation with the decisions the foreman must make. Every case id
  it cites must appear in a committed output file.
- scripts, patch, and small JSON outputs.

Fill the plan's "P0 result" section. No production, schema, content or
test edits beyond the survey tool.

## Rules

- Synthetic demo.* only, and no absolute or temp-directory paths in
  committed files, prose included.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir).
  If the lock is held, retry every 10 s for up to 5 min.
- Never use --no-verify or a bare git stash.
- Run foreground commands only. No push and no spawn.
