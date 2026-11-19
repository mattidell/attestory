# Charter: Track 1 of a Form 1099-B bartering amount is not lost

Role: Builder. Source HEAD on milestone/f1099b-bartering-2025.
Plan: docs/phases/engine-breadth/milestones/f1099b-bartering.md (read it
whole, especially Decisions 1-3). Evidence: f1099b-bartering-evidence/
p0.md, wording.json (variant q), build.py, probe.py, replay.py. For how
content successors are published (package, registry, release, published
checksums, the successor-graph table in package_validation.py), follow
the most recent content milestone: plain-line-texts (core v96). Do not
read governance.

## Scope

1. **Publish.** Core v97, registry v95, release v95: the five
   input-question successors of variant q exactly as wording.json gives
   them, nothing else. New files only; never edit a published file.
   Check whether the validator's `_successor_graphs` table needs an
   entry (P0 says no; confirm).
2. **Tests.** P0's nine probe returns as a live test module on v97
   through the real coordinator and saved page: the box-13 returns
   answered no still compute (the engine cannot see box 13), the
   unanswered case shows the new sentence on the page, and the yes case
   refuses line 10 with the line 8 through 37 block. A fast package test
   that v97 admits the five successors and changes nothing else in the
   package members against v96. Re-pin any existing test that pins the
   current core version, as earlier milestones did.
3. **Replay.** Full-surface replay (`tools/recorded_replay.py full`) of
   the 775 recorded lists, v96 against published v97, with the version
   and sentence changes declared: report pass/unexpected and unused
   expectations.

No engine, schema, projection or page edits.

## Deliverables

Content under packages/content/tax/2025/, tests, and track1.md in the
evidence directory. This touches published content: run the full suite
(`pytest`) and `python3 -m mypy`, and `pytest tests/test_schema_registry.py`;
report the lines.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn.
