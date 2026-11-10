# Charter: Track 1 of Form 1099-B box 7 beside a loss — core v84

Role: Builder. Source HEAD on milestone/f1099b-box7-loss-2025.
Plan: docs/phases/engine-breadth/milestones/f1099b-box7-loss.md. Read
Decisions 1-6 and "Track 0 adversarial closure". Evidence is in
f1099b-box7-loss-evidence/: track0-closure.md, prototype.py (the decided
16-rule shape with the sale-count requirements kept), track0.py and its
JSON outputs. Precedent for the build shape:
tests/test_f1099b_backup_withholding_v83.py and
tests/test_f1099b_backup_withholding_v83_package.py. Do not read
governance.

Stop and report if anything needs an edit under packages/kernel/,
packages/derivation/ or packages/schemas/, or a recording change.

## Build

1. **Successor citizens.** Bring the decided v84 set into
   packages/content/tax/2025/ as new versioned citizens, generated from
   prototype.py and byte-identical to it: the verdict bundle, the eight
   per-sale verdict rules, the eight family checks, Schedule D line 16 v4
   and its form field v4. Never edit a published citizen.
2. **Core v84, registry v82 and release v82**, made with
   `python3 -m tools.package_successor`. Add the per-core v84 entries in
   packages/tax/loader.py, carrying v83's companion declaration and
   refusal maps.
3. **Tests.**
   - A live module running every Track 0 case on published core v84
     through `live_coordinate_run` and the presentation model. Pin
     Schedule D lines 1a-16 and 21, Form 1040 lines 7a, 15, 16, 24, 33, 34
     and 37, each blocked line's reason sentences and its (disposition,
     code, missing). Check hand values from track0.py's hand, not from the
     run.
   - The 298 recorded v83 runs on published v84, asserted equal to
     tests/fixtures/f1099b_backup_withholding_v83/expected.json directly;
     do not copy them into a new fixture. Keep the new fixture to the
     Track 0 cases.
   - Extend the committed sale-fact audit
     (sale-family-audit-evidence/tables.py) to core v84, so the box 7
     answer counts as read only by the verdict rules' value side.
   - A fast package test: byte identity against the prototype, the exact
     member edits, registry v82 add-only, and the loader entries.
   - Core v83 and earlier pinned unchanged.

   Load evidence harnesses under unique module names and never assign
   another module's globals. Keep every test under the 3.0 s fast-lane
   budget or `@pytest.mark.live` with a measured reason. Report the live
   module's run count and wall time.
4. **Checks.** Run `pytest -m "not live"`, then the full `pytest` (split
   into shards if one command is too long, and sum the counts), then
   `python3 -m mypy`, and `python3 tools/envelope_scan.py --range
   github/main..HEAD`. Fill a "Track 1 result" section in the plan with
   case counts, the 298-run result, fixture size, run count, and any
   deviation.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Published citizens and schemas are immutable: successors only.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
  if held, retry every 10 s up to 5 min.
- Never --no-verify or a bare git stash. No push, no spawn.
