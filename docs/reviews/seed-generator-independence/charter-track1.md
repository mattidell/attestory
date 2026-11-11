# Charter: Track 1 of the v70 entry seed generating without test helpers

Role: Builder. Source HEAD on milestone/seed-generator-independence-2025.
Plan: docs/phases/engine-breadth/milestones/seed-generator-independence.md
(read it whole, Decisions 1-5 control). Evidence: P0 in
seed-generator-independence-evidence/p0.md and its source-fixture
prototype. Do not read governance.

## Scope

1. Commit the complete return as
   `packages/sample_data/entry_loop_v70/complete-core-return.jsonl`,
   produced from the current test helpers once, and record in the
   generator's docstring how it was produced and that refreshing it is
   deliberate.
2. Change `tools/generate_entry_loop_v70_fixture.py` to read that file and
   import no test module. Keep its public functions (`render_fixture_files`
   and anything else `tests/test_entry_loop_t1.py` imports) and their
   output unchanged.
3. Add a test that fails if the generator imports any `tests` module,
   directly or transitively (for example, import it in a subprocess and
   list `sys.modules`). Show it failing against the old generator.
4. Confirm nothing that enumerates `packages/sample_data/entry_loop_v70/`
   (runtime loader, manifests, checksums, data-safety or envelope scans)
   changes behaviour with the new file. If something does, stop and
   report.
5. Regenerate and show the committed seed files are byte-identical.

## Deliverables

The source file, the generator change, the new test, and a filled
"Track 1 result" section in the plan with the byte check, the
before/after test counts for the touched modules, and what each check now
catches. Run the touched test modules and the fast lane
(`pytest -m "not live"`); `python3 -m mypy`; and
`python3 tools/envelope_scan.py --range github/main..HEAD`.

## Rules

- Synthetic demo.* only. No absolute or temp-directory paths in committed
  files, prose included.
- No change to any test assertion, the seed bytes, or anything else under
  packages/. Stop and report if the byte check fails.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Never --no-verify or a bare git stash. Run foreground commands only. No
  push, no spawn.
