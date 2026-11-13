# Charter: Track 1 of age and blindness asked — core v88

Role: Builder. Source HEAD on milestone/age-blindness-asked-2025.
Plan: docs/phases/engine-breadth/milestones/age-blindness-asked.md. Read
Decisions 1-10, "Track 0 adversarial closure" and its Disposition.
Evidence is in age-blindness-asked-evidence/: track0-closure.md,
prototype.py (the decided v88 shape), track0.py, rerun.py and their JSON
outputs. Precedent for the build shape: tests/test_question_wording_v87.py
and tests/test_question_wording_v87_package.py. Do not read governance.

Stop and report if anything needs an edit under packages/kernel/,
packages/derivation/ or packages/schemas/, or a recording change.

## Build

1. **Decision 10.** Change the condition question's words in prototype.py
   to Decision 10's sentence, rebuild scratch v88, and rerun only the
   track0 cases that show that sentence (the surface for a separate
   return and the cases that ask it). Commit the JSON.
2. **Successor citizens.** Bring the decided v88 members into
   packages/content/tax/2025/ as new versioned citizens, generated from
   prototype.py and byte-identical to it: the four age and blindness
   questions and the condition question, the condition fact type, the
   vocabulary bundle v4, dependents worksheet line 1 v2 and Schedule 1-A
   line 36b v2, with the four bindings `required`. Never edit a published
   citizen.
3. **Core v88, registry v86 and release v86**, made with
   `python3 -m tools.package_successor`. Add the per-core v88 entries in
   packages/tax/loader.py, carrying v87's entries unchanged, and extend any
   test that lists cores carrying a map (as v87 extended
   tests/test_noncovered_sales_v78_switch.py).
4. **Test helper.** Every test that runs a return on v88 states the
   taxpayer's two facts (Decision 6): add that to the shared helper the
   v87 modules use, so existing callers stay unchanged on earlier cores.
5. **Tests.**
   - A live module running the Track 0 authority, matrix and late cases
     on published v88 through `live_coordinate_run` and the presentation
     model. Run each distinct act list once. Pin hand values from
     law.json / track0.py, never from the run, and each question's exact
     sentence.
   - The recorded returns on published v88, answered false as the record
     implies, against their fixtures in place (do not copy them): all
     identical. Run them in parallel shards (CPU count minus one, at most
     4 while other builders share the machine) and report wall time.
   - A fast package test: byte identity against the prototype, the exact
     member edits, registry v86 add-only, the loader entries, and v87 and
     earlier unchanged.

   Load evidence files only through tests/evidence_loader.py. Keep every
   test under the 3.0 s fast-lane budget or `@pytest.mark.live` with a
   measured reason. Report the live module's run count and wall time.
6. **Checks.** `pytest` on the new modules and every test file you
   touched, `pytest -m "not live"`, `python3 -m mypy`, and
   `python3 tools/envelope_scan.py --range github/main..HEAD`. Fill a
   "Track 1 result" section in the plan with case counts, the recorded-run
   result, run count, wall times and any deviation.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Published citizens and schemas are immutable: successors only.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
  if held, retry every 10 s up to 5 min.
- Never --no-verify or a bare git stash. Run foreground commands only. No
  push, no spawn.
