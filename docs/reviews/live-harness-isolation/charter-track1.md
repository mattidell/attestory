# Charter: Track 1 of live evidence harness isolation

Role: Builder. Source HEAD on milestone/live-harness-isolation-2025.
Plan: docs/phases/engine-breadth/milestones/live-harness-isolation.md
(read Decisions 1-5). Evidence: live-harness-isolation-evidence/p0.md and
the inventory tool. Do not read governance.

## Build

1. **Loader.** One module under tests/ implementing Decisions 1 and 2,
   with unit tests: two test modules loading the same harness get
   different objects; a nested bare import resolves to the owner's copy;
   an engine attribute a harness writes is restored after the owner
   finishes.
2. **Moves.** Move the twenty modules named in p0.md to the loader. Do
   not change any assertion, case list, fixture byte, or marker. Record
   each module's before/after wall time for its own run.
3. **Guard.** The guard test of Decision 4, using the inventory tool.
4. **Checks.** Run the inner loop on each moved module, `pytest -m "not
   live"`, then the full `pytest` (split into shards, sum the counts), and
   the one-worker pair reproductions from P0 in both orders. Then
   `python3 -m mypy` and `python3 tools/envelope_scan.py --range
   github/main..HEAD`. Fill a "Track 1 result" section in the plan:
   counts before and after (they must match), walls, any subprocess
   fallback and its cost, any deviation.

Stop and report before any change under packages/ or to an evidence file,
or if any assertion would have to change.

## Rules

- No absolute or temp-directory paths in committed files, prose included.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Never --no-verify or a bare git stash. Run foreground commands only. No
  push, no spawn.
