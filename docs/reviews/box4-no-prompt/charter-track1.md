# Charter: Track 1 of a box 4 "no" not being asked for an amount — core v94

Role: Builder. Source HEAD on milestone/box4-no-prompt-2025 (main at
core v93, registry v91, release v91).
Plan: docs/phases/engine-breadth/milestones/box4-no-prompt.md. Read
Decisions 1-6 and "Track 0 disposition" (Decisions 7-8). Evidence:
box4-no-prompt-evidence/ (p0.md, track0-closure.md, prototype.py,
prototype-build.json, track0.py, classify.py and their JSON). Precedent
for the content build and tests: tests/test_line6b_reason_v93.py,
tests/test_line6b_reason_v93_package.py and
tests/test_page_alerts_v92.py. Do not read governance.

Stop and report if anything needs an edit under packages/kernel/,
packages/derivation/, packages/schemas/ or packages/presentation/, or a
recording change.

## Build

1. **Content.** In packages/content/tax/2025/: the P0 prototype's
   helper rules, vocabulary bundle and line 25b v9, byte-identical to
   `prototype-build.json`; and an `input-question.f1099b-box4` successor
   (v2) with Decision 7's words exactly, same fact type and answer shape
   as v1. Never edit a published citizen.
2. **Core v94, registry v92, release v92** with
   `python3 -m tools.package_successor` on published v93, adopting the
   prototype's members and entrypoints and replacing the box 4 question
   member with v2. Add the v94 loader entries in packages/tax/loader.py
   carrying v93's unchanged, and extend any test or allowlist that
   enumerates cores (the v93 build touched
   tests/test_noncovered_sales_v78_switch.py).
3. **Full replay.** All 775 recorded lists on published v93 and
   published v94 with `python3 tools/recorded_replay.py`, CPU count minus
   one workers, in the foreground, part file outside the repo. Classify
   with classify.py (extended if needed): expected P0's 420 identical /
   84 same error / 271 next-question, plus the amount sentence's new
   words wherever shown; zero value, disposition or refusal-code
   changes. Then rerun Track 0's computing neighbours (track0.py,
   parallel) on v93 vs v94: zero differences. Report wall times.
4. **Tests.**
   - A live module on published v94 through `live_coordinate_run`, the
     presentation projection and the saved page model, each distinct act
     list once: one statement answered "no" (lines 25b = 0 and 25d
     publish, no amount sentence on them); "yes" with no amount (amount
     sentence with Decision 7's words); mixed "no" + unanswered (still
     blocked on the unanswered statement); two sales on one "no"
     statement; "no" with 200 (200 counts); one "no" case for a second
     sale subject type; a "no" whose return-level question is
     unanswered (line 25b names that question); a no-1099-B neighbour
     unchanged. Hand values from the facts, not from the run.
   - A fast package test: byte identity with the prototype, exactly the
     members and entrypoints added or replaced, registry v92 add-only,
     the loader entries, v93 and earlier unchanged.

   Load evidence only through tests/evidence_loader.py. A harness that
   imports a sibling by bare name must have that sibling loaded by path
   under that name first (see `_line12d_names` in
   tests/test_page_alerts_v92.py); run each new module once with an
   unrelated evidence directory first on PYTHONPATH to prove it. Keep
   every test under the 3.0 s fast-lane budget or `@pytest.mark.live`
   with a measured reason.
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
