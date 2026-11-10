# Charter: Track 1 of Form 1099-B backup withholding without a sale — core v85

Role: Builder. Source HEAD on milestone/f1099b-box4-only-2025.
Plan: docs/phases/engine-breadth/milestones/f1099b-box4-only.md. Read
Decisions 1-7 and "Track 0 adversarial closure". Evidence is in
f1099b-box4-only-evidence/: track0-closure.md, prototype.py (the decided
shape with the Decision 7 wording), track0.py and its JSON outputs.
Precedent for the build shape: tests/test_f1099b_box7_loss_v84.py and
tests/test_f1099b_box7_loss_v84_package.py. Do not read governance.

Stop and report if anything needs an edit under packages/kernel/,
packages/derivation/ or packages/schemas/, or a recording change.

## Build

1. **Successor citizens.** Bring the decided v85 set into
   packages/content/tax/2025/ as new versioned citizens, generated from
   prototype.py and byte-identical to it: the no-sale box 4 bundle and its
   two fact types, the two return-level questions, Form 1040 line 25b rule
   v8 and its form field v6. Never edit a published citizen.
2. **Core v85, registry v83 and release v83**, made with
   `python3 -m tools.package_successor`. Add the per-core v85 entries in
   packages/tax/loader.py, carrying v84's companion declaration and
   refusal maps.
3. **Tests.**
   - A live module running the Track 0 cases on published core v85
     through `live_coordinate_run` and the presentation model. Do not run
     two cases with the same act list; let one run assert every fixture
     row it covers. Pin Form 1040 lines 25a-25d, 33, 34 and 37, each
     blocked line's reason sentences and its (disposition, code, missing),
     and the question asked. Check hand values from track0.py's hand, not
     from the run.
   - The 298 recorded v83 runs on published v85, against
     tests/fixtures/f1099b_backup_withholding_v83/expected.json directly
     (do not copy them into a new fixture): the 207 identical as recorded;
     the 91 with the yes/no answered no, equal to the recorded values; and
     three of the 91 as recorded, blocked on the yes/no with its question.
   - Extend the committed sale-fact audit
     (sale-family-audit-evidence/tables.py) to core v85 if it covers line
     25b's reads.
   - A fast package test: byte identity against the prototype, the exact
     member edits, registry v83 add-only, and the loader entries.
   - Core v84 and earlier pinned unchanged.

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
- Never --no-verify or a bare git stash. Run foreground commands only. No
  push, no spawn.
