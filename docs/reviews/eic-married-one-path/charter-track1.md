# Charter: Track 1 of the married-taxpayer rules need no inert path

Role: Builder. Source HEAD on milestone/eic-married-one-path-2025.
Plan: docs/phases/engine-breadth/milestones/eic-married-one-path.md (read it
whole). Precedents: eic-separated-married (plan Decisions 5 and 8, track1.md,
tests), hoh-no-worksheet-ceilings (rule-artifact.v17 successors). Do not
read governance.

## Scope

1. **Schema.** Read `packages/schemas/derivation/rule-artifact.v17.schema.json`
   and confirm a one-path `exclusive_presence` selection validates and the
   engine evaluates it like the two-path form when the second path is
   inactive. Quote what you rely on.
2. **Successors.** v2 of `rule.eic-married-taxpayer-recorded` and
   `rule.eic-married-taxpayer-from-separated` on `rule-artifact.v17`, with
   only the `separated-recorded` path and the existing default; every
   other field unchanged except the schema and version.
3. **Publish** core v105, registry v103, release v103 from published v104
   (rebase onto main first if #305 has merged; if not, stop and report
   instead of publishing a v104). New files only; loader v105 entries carry
   v104's. The fast size guard covers the two files (they are `rule.eic-*`).
4. **Prove nothing moved.** The eic-separated-married live tests pass on
   v105 (point them at v105 the way earlier milestones did, or add a v105
   test that reruns every case); a full-surface replay v104 against v105
   declares only the two version moves, 0 unexpected, no number change; a
   scratch check that the v2 rules read no `eic.married-taxpayer-inert`.
5. **Checks.** Fast lane, touched live tests, mypy.

## Deliverables

Content, package, registry, release, loader entries and tests; in
eic-married-one-path-evidence/: track1.md. Fill a "Track 1 result" section
in the plan. Commit in steps.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Do not edit packages/kernel/, the engine or a schema. Stop and report if
  a one-path selection does not behave the same.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn.
