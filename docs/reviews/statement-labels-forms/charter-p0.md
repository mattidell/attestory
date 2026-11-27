# Charter: P0 of every statement question names its statement

Role: Builder (P0 design, no build). Source HEAD on
milestone/statement-labels-forms-2025.
Plan: docs/phases/engine-breadth/milestones/statement-labels-forms.md
(read it whole). Contract to extend: docs/adr/0089-statement-question-labels.md.
Precedent code: `_StatementQuestions` and `STATEMENT_QUESTION_NEEDS` in
packages/derivation/presentation_projection.py and packages/tax, and the
evidence under statement-question-labels-evidence/. Do not read governance.

## Scope

Do the plan's P0 stage. Write `statement-labels-forms-evidence/p0.md`
next to the plan: inventory per form, route per form, scratch proof,
replay result and controls, and a recommendation. Include any probe
script that tests could reuse. Fill a "P0 result" section in the plan and
list the decisions you need from the foreman or owner. Put the ADR 0089
amendment draft in `statement-labels-forms-evidence/adr-draft.md` (status
proposed). Do not edit docs/adr/.

## Rules

- Scratch builds outside the repo tree or under ignored paths (temp/);
  commit only evidence, not raw output larger than a summary. Synthetic
  demo.* only; no absolute or temp-directory paths in committed files,
  prose included.
- Do not edit packages/kernel/, any published file, or any product code.
- Run the full-surface replay in parallel shards with one shared run, and
  no resume cache unless it is keyed to the code under test.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`.
- Never --no-verify or a bare git stash. No push and no spawn.
