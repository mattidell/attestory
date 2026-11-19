# Charter: Track 1 of head of household needs a qualifying person

Role: Builder. Source HEAD on milestone/hoh-qualifying-person-2025.
Plan: docs/phases/engine-breadth/milestones/hoh-qualifying-person.md (read
it whole, especially the P0 result and Decisions 2-6). Evidence:
hoh-qualifying-person-evidence/p0.md, design.py (variant q and the exact
question wording), build.py, probe.py, replay.py. For how content
successors are published (package, registry, release, published checksums,
the successor-graph table in package_validation.py, loader entries), follow
the most recent content milestone: f1099b-bartering (core v97). Do not
read governance.

## Scope

1. **Publish.** Core v98, registry v96, release v96: the vocabulary bundle
   with the two return-level answers, the two input questions with
   design.py's wording, and `rule.dependents-worksheet-line-3` v2 on
   `rule-artifact.v17`, exactly as P0 built them. New files only; never
   edit a published file. Check whether the validator's
   `_successor_graphs` table needs an entry, and confirm the loader's v98
   entries carry v97's.
2. **Tests.** P0's probe returns as a live test module on v98 through the
   real coordinator and saved page:
   - head of household and qualifying surviving spouse answered yes keep
     v97's numbers (line 12e, the tax and the refund, with hand values);
   - answered no, line 12e refuses and the page shows the question;
   - unanswered, the page asks the question;
   - single, married filing jointly and married filing separately read
     nothing new and keep their numbers.
   Add a fast package test that v98 admits exactly the new members and
   the rule successor against v97. Re-pin any existing test that pins the
   current core version, as earlier milestones did.
3. **Replay.** Full-surface replay (`tools/recorded_replay.py full`) of
   the 775 recorded lists, v97 against published v98, with the version
   changes declared. Report pass/unexpected and unused expectations.

No engine, schema, projection or page edits.

## Deliverables

Content under packages/content/tax/2025/, tests, and track1.md in the
evidence directory. This touches published content: run the full suite
(`pytest`), `python3 -m mypy`, and `pytest tests/test_schema_registry.py`,
and report the result lines.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`. Use separate
  simple commands (mkdir lock; git add; git commit -F file; rmdir lock),
  retrying every 10 s for up to 5 min if the lock is held.
- Bound every command that can hang (e.g. `perl -e 'alarm 1800; exec @ARGV' ...`);
  never `rm -rf`.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn.
