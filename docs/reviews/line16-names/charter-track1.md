# Charter: Track 1 of line 16 naming the failing Exception 1 criteria — core v95

Role: Builder. Source HEAD on milestone/line16-names-2025 (main at
core v94, registry v92, release v92).
Plan: docs/phases/engine-breadth/milestones/line16-names.md. Read
Decisions 2-3 and 6-11 (Decision 1 is replaced). Evidence:
line16-names-evidence/ (p0.md, track0-closure.md, track0b-closure.md,
the Track 0b prototype, classify.py and their JSON). Precedent for the
content build and tests: tests/test_preferential_base_reason_v91.py and
its package test, tests/test_box4_no_prompt_v94.py and its package test.
Do not read governance.

Stop and report if anything needs an edit under packages/kernel/,
packages/derivation/, packages/schemas/ or packages/presentation/, or a
recording change.

## Build

1. **Speed first (Decision 11).** On the Track 0b scratch successor and
   published v94, time the same 40 recorded lists (across every recorded
   set, including the four targets) back to back on each core, same
   worker count, nothing else running from you. Report per-list medians.
   If the successor is more than 10% slower, stop and report, naming
   which rule's evaluation costs the time.
2. **Content.** `rule.form1040-line16.v9.json` and
   `rule.selected-preferential-base.v12.json` in
   packages/content/tax/2025/, byte-identical to the Track 0b minimized
   prototype. Never edit a published citizen.
3. **Core v95, registry v93, release v93** with
   `python3 -m tools.package_successor` on published v94, replacing the
   two members. Add the v95 loader entries in packages/tax/loader.py
   carrying v94's unchanged, and extend any test or allowlist that
   enumerates cores (the v94 build touched
   tests/test_noncovered_sales_v78_switch.py).
4. **Full replay.** All 775 recorded lists on published v94 and published
   v95 with `python3 tools/recorded_replay.py`, CPU count minus one
   workers, in the foreground, part file outside the repo. Classify with
   the strict classifier: expected Track 0b's 687 / 84 / 4 and nothing
   else. Report wall time.
5. **Tests.**
   - A live module on published v95 through `live_coordinate_run`, the
     presentation projection and the saved page model, each distinct act
     list once: one, two and four failing criteria (line 16, one
     dependant and one preferential-base field name exactly those); a
     correction of one failing criterion removes its name; the
     personal-loss case keeps its four names (Decision 2); an unanswered
     Form 8949 boundary asks that question (Decision 3); a computing
     neighbour unchanged. Expected names from the facts, not the run.
   - A fast package test: byte identity with the prototype, exactly the
     two members replaced, registry v93 add-only, the loader entries,
     v94 and earlier unchanged.

   Load evidence only through tests/evidence_loader.py, with bare-name
   siblings bound by path first (`_line12d_names` in
   tests/test_page_alerts_v92.py); run each new module once with an
   unrelated evidence directory first on PYTHONPATH. Keep every test under
   the 3.0 s fast-lane budget or `@pytest.mark.live` with a measured
   reason.
6. **Checks.** `pytest` on the new modules and every test file touched,
   `pytest -m "not live"`, `python3 -m mypy`,
   `python3 tools/envelope_scan.py --range github/main..HEAD`. CI
   `verify` is the gate for the full suite. Fill a "Track 1 result"
   section in the plan, with deviations and the speed measurement.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Published citizens and schemas are immutable: successors only.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
  if held, retry every 10 s up to 5 min.
- Write your JSON report before your final checks, and update it when
  they finish.
- Never --no-verify or a bare git stash. Foreground only: never end your
  turn while a command is running. No push, no spawn.
