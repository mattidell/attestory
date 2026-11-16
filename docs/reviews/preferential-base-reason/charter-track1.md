# Charter: Track 1 of the lines below line 16 — core v91

Role: Builder. Source HEAD on milestone/preferential-base-reason-2025.
Plan: docs/phases/engine-breadth/milestones/preferential-base-reason.md.
Read Decisions 1-9 and "Track 0 adversarial closure". Evidence:
preferential-base-reason-evidence/ (p0.md, track0-closure.md,
prototype.py, track0.py and their JSON). Precedent for the content build
and tests: tests/test_blocked_names_question_v89.py,
tests/test_blocked_names_question_v89_package.py and
tests/test_line12d_boxes_v90_package.py. Do not read governance.

Stop and report if anything needs an edit under packages/kernel/,
packages/derivation/, packages/schemas/ or packages/presentation/, or a
recording change.

## Build

1. **Content.** Two new versioned citizens in packages/content/tax/2025/
   on `rule-artifact.v17`; never edit a published citizen.
   - `rule.selected-preferential-base` v11: the eight-name variant Track 0
     item 6 replayed, byte-identical to prototype.py's build of it.
   - `rule.form1040-line16` v9 (Decision 8): v8 with the eight names only
     where Schedule D is required and no sale is recorded. Extend
     prototype.py to build it and show, before going on, that the ten
     blocked-names-question Track 0 cases and the line 16 case give the
     same `missing` names, questions and values on v8 and v9. If they do
     not, stop and report; do not publish v9.
2. **Core v91, registry v89, release v89** with
   `python3 -m tools.package_successor`. Add the v91 loader entries in
   packages/tax/loader.py carrying v90's unchanged, and extend any test
   or allowlist that enumerates cores (the v90 build touched
   tests/test_noncovered_sales_v78_switch.py).
3. **Full replay.** All 775 recorded lists on published v90 and published
   v91 with `python3 tools/recorded_replay.py`, CPU count minus one
   workers, in the foreground, part file outside the repo. Commit the
   classification: the target is the four recorded returns changing only
   blocked rows and sentences, 771 identical, no line value changed, no
   computing return gaining or losing a question. Report wall time.
4. **Tests.**
   - A live module on published v91 through `live_coordinate_run` and the
     presentation projection, each distinct act list once: the Track 0
     authority cells, matrix and late steps; on the four recorded returns
     every blocked filer-visible field names a question and the 23 fields
     name the eight; the no-sale return is unblocked by Exception 1 "yes"
     and reaches the wage hand; a sale reaches the sale hand. Hand values
     come from the 2025 instructions and are held whether or not a
     question remains. A case named "unanswered" must leave that fact out
     of its act list; do not let a shared helper answer it.
   - The ten blocked-names-question cases on v91: unchanged names,
     questions and values.
   - A fast package test: byte identity with the prototype, exactly two
     members changed, registry v89 add-only, the loader entries, v90 and
     earlier unchanged.

   Load evidence only through tests/evidence_loader.py. Keep every test
   under the 3.0 s fast-lane budget or `@pytest.mark.live` with a
   measured reason.
5. **Checks.** `pytest` on the new modules and every test file touched,
   `pytest -m "not live"`, `python3 -m mypy`,
   `python3 tools/envelope_scan.py --range github/main..HEAD`. CI
   `verify` is the gate for the full suite. Fill a "Track 1 result"
   section in the plan, with deviations.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Published citizens and schemas are immutable: successors only.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
  if held, retry every 10 s up to 5 min.
- Never --no-verify or a bare git stash. Foreground only: never end your
  turn while a command is running. No push, no spawn.
