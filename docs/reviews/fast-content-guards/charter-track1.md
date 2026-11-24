# Charter: Track 1 of content guards run in the fast lane

Role: Builder. Source HEAD on milestone/fast-content-guards-2025.
Plan: docs/phases/engine-breadth/milestones/fast-content-guards.md (read it
whole). Do not read governance.

## Scope

1. **Inventory.** Every test that guards a content file's byte size
   (`git grep -n st_size -- tests`): the module, whether conftest marks it
   live, the glob or file list it checks, its cap, and its exception list
   with the reason written beside it. Record it in track1.md.
2. **One fast guard.** A new module, for example
   `tests/test_content_file_sizes.py`, that imports nothing live (no token
   from `LIVE_SOURCE_TOKENS` in tests/conftest.py) and checks exactly the
   union of what the existing guards check, with one table of exceptions
   (file, cap, reason). Same files, same caps, same reasons. Remove the
   repeated guards from the live modules (single-source rule, AGENTS.md).
   Show the union is identical: list files and caps before and after.
3. **Proof.** On a scratch copy, grow a rule file over its cap and show
   the fast lane (`pytest -m "not live"`) fails; restore. Show the new
   module is collected under `-m "not live"`.
4. **Observer test.** Make
   `test_node_observer_emits_safe_manifest_stage_without_starting_chrome`
   pass with FORCE_COLOR=1, with NO_COLOR=1 and with both, without
   weakening its assertions (for example by clearing those variables in
   the child's environment, or by parsing only the JSON line). Say which
   and why.
5. **Checks.** Fast lane, the live modules you edited, mypy on touched
   Python, envelope scan.

## Deliverables

Tests and helpers only. In
docs/phases/engine-breadth/milestones/fast-content-guards-evidence/:
track1.md (inventory, before/after union, proof, observer fix, checks).
Fill a "Track 1 result" section in the plan. Commit in steps.

## Rules

- No package, rule, schema, kernel or page edit; no change to a cap or an
  exception; no change to tests/conftest.py.
- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn.
