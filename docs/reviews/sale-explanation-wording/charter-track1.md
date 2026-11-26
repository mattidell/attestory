# Charter: Track 1 of the sale block explanations read plainly

Role: Builder. Source HEAD on milestone/sale-explanation-wording-2025.
Plan: docs/phases/engine-breadth/milestones/sale-explanation-wording.md
(read it whole; the "Wording bar" section governs the text). Precedents:
sale-block-explanations (ADR 0088, its evidence wording.json, core v106
and its tests), eic-separated-married (question text, its fast clause test).
Do not read governance.

## Scope

1. **Safety check first.** Find what pins a `family-block-explanation`
   and an `input-question` citizen (package, saved records, answers,
   workspaces). Show in a scratch copy that adopting v2 of one of each
   unpins no saved record and changes no number. If either would unpin a
   saved record, stop and report with the evidence; do not publish.
2. **Wording.** Write the 30 explanations and the 8 sale
   `*-adjustment` questions (6 wash-sale, 2 code B) to the plan's
   wording bar. Start from the current text and
   `sale-block-explanations-evidence/wording.json` (its IRS citations).
   Record old, new and the IRS section for each in
   `sale-explanation-wording-evidence/wording.json`.
3. **Publish** v2 citizens and the next core, registry and release from
   the latest published on this branch. New files only; loader entries
   for the new core carry the previous core's. Keep the fast size guard
   passing.
4. **Prove only words moved.** A full-surface replay of the previous core
   against the new one declares only the explanation and question
   sentence changes plus the version moves, 0 unexpected, no number,
   disposition or block-code change. Run the replay in parallel shards
   with one shared run, not one process per list.
5. **Tests.** A fast content test that each new explanation and question
   meets the mechanical parts of the bar (no engine words, no semicolon,
   no parentheses, at most two sentences, short-term and long-term pairs
   equal where the rule is equal). Point the existing
   family-block-explanation package tests at the new core the way earlier
   milestones did. Rendered-page check that a wash-sale block shows the new
   explanation and still links its question.
6. **Checks.** Fast lane, touched live tests, mypy on touched modules.

## Deliverables

Content, package, registry, release, loader entries and tests; in
`docs/phases/engine-breadth/milestones/sale-explanation-wording-evidence/`:
track1.md and wording.json. Fill a "Track 1 result" section in the plan.
Commit in steps.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Do not edit packages/kernel/, the engine, the projection or a schema.
  Never edit a published file.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn.
