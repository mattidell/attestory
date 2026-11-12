# Charter: Track 1 of question wording — core v87

Role: Builder. Source HEAD on milestone/question-wording-2025.
Plan: docs/phases/engine-breadth/milestones/question-wording.md. Read
Decisions 1-6, "Track 0 adversarial closure" and its Disposition.
Evidence is in question-wording-evidence/: track0-closure.md, prototype.py
(the decided v87 shape, seven members), track0.py and its JSON outputs.
Precedent for the build shape: tests/test_f1099b_selection_keyed_collect_v86.py
and tests/test_f1099b_selection_keyed_collect_v86_package.py. Do not read
governance.

Stop and report if anything needs an edit under packages/kernel/,
packages/derivation/ or packages/schemas/, or a recording change.

## Build

1. **Successor citizens.** Bring the decided v87 members into
   packages/content/tax/2025/ as new versioned citizens, generated from
   prototype.py and byte-identical to it: the two wash-sale adjustment
   questions (v4), the Exception 1 only-box-2a question (v3), the
   student-loan dependent question (v2), and the exception1, sli-scope and
   vocabulary bundle successors. Never edit a published citizen.
2. **Core v87, registry v85 and release v85**, made with
   `python3 -m tools.package_successor`. Add the per-core v87 entries in
   packages/tax/loader.py, carrying v86's entries (including the
   selection-collect switch) unchanged.
3. **Tests.**
   - A live module running the Track 0 authority, matrix and late cases on
     published core v87 through `live_coordinate_run` and the presentation
     model. Do not run two cases with the same act list. Pin each case's
     hand values from law.json / track0.py's hand, never from the run, and
     the exact question text shown.
   - The 298 recorded v83 runs on published v87 against
     tests/fixtures/f1099b_backup_withholding_v83/expected.json directly
     (do not copy them into a new fixture): all identical.
   - A fast package test: byte identity against the prototype, the exact
     member edits (seven), registry v85 add-only, and the loader entries.
   - Core v86 and earlier pinned unchanged.

   Load evidence files only through tests/evidence_loader.py (the guard
   test `test_in_process_evidence_loads_use_the_loader` fails a direct
   load). Keep every test under the 3.0 s fast-lane budget or
   `@pytest.mark.live` with a measured reason. Report the live module's
   run count and wall time.
4. **Checks.** Run `pytest -m "not live"`, then the full `pytest` (split
   into shards if one command is too long, and sum the counts), then
   `python3 -m mypy`, and `python3 tools/envelope_scan.py --range
   github/main..HEAD`. Fill a "Track 1 result" section in the plan with
   case counts, the 298-run result, run count, and any deviation.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Published citizens and schemas are immutable: successors only.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
  if held, retry every 10 s up to 5 min.
- Never --no-verify or a bare git stash. Run foreground commands only. No
  push, no spawn.
