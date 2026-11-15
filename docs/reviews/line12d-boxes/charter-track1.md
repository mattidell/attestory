# Charter: Track 1 of line 12d's boxes — core v90

Role: Builder. Source HEAD on milestone/line12d-boxes-2025.
Plan: docs/phases/engine-breadth/milestones/line12d-boxes.md. Read
Decisions 1-6, "Track 0 adversarial closure" and its Disposition.
Evidence: line12d-boxes-evidence/ (track0-closure.md, prototype.py,
track0.py, observe.mjs, track0-page.diff and their JSON). Precedent for
the content build: tests/test_age_blindness_v88.py and
tests/test_age_blindness_v88_package.py. Do not read governance.

Stop and report if anything needs an edit under packages/kernel/,
packages/derivation/ or packages/schemas/, a recording change, or a page
change beyond the categorical branch in track0-page.diff.

## Build

1. **Page.** Apply track0-page.diff exactly to
   packages/presentation/pages/citation-walk.v1.html, and the same change
   to tools/presentation_harness/examples/pages/citation-walk.v1.html
   where it carries the same branch (Decision 2). Run every test file
   that reads either page and the harness's baseline checks; report any
   that needed a change and why.
2. **Content.** Bring the 17 decided members into
   packages/content/tax/2025/ as new versioned citizens, byte-identical to
   prototype.py's build. Never edit a published citizen.
3. **Core v90, registry v88, release v88** with
   `python3 -m tools.package_successor`. Add the v90 loader entries in
   packages/tax/loader.py carrying v89's unchanged, and extend any test or
   allowlist that enumerates cores (the v89 build needed
   tests/test_noncovered_sales_v78_switch.py,
   tests/test_later_year_basis_reuse_track0.py and
   tools/required_versus_read_allowlist.json).
4. **Full replay.** Run all 775 recorded lists on published v89 and v90
   with line12d-boxes-evidence/rerun.py (it drives
   `tools/recorded_replay.py`), 8 workers, part file in a scratch
   directory outside the repo; resume across the 10-minute command limit.
   Commit the complete rerun-output.json: the target is identical numbers
   with only the line 12d sections added. Update the plan's Track 0
   limitation 1 with the result.
5. **Tests.**
   - A live module running the Track 0 authority, matrix and late cases
     on published v90 through `live_coordinate_run` and the presentation
     model; each distinct act list once; box states and line 12e from the
     2025 instructions (law.json), never from the run. Every case states
     the taxpayer's age and blindness facts through the shared helper and
     is held to its values whether or not a question remains.
   - A drawn-page test: the checked, not-checked, hidden and blocked box
     texts on the committed page, and that a `not_elected` render still
     alerts. Prefer the existing no-browser page harness if one asserts
     drawn output; if it needs Chrome, mark it `@pytest.mark.live` with
     the reason and use the short owned temp root from
     tools/sale_page_observation.py.
   - The 298 v83 recorded lists on published v90 against their fixture in
     place: identical numbers.
   - A fast package test: byte identity with the prototype, the exact
     member additions, registry v88 add-only, the loader entries, v89 and
     earlier unchanged.

   Load evidence only through tests/evidence_loader.py. Keep every test
   under the 3.0 s fast-lane budget or `@pytest.mark.live` with a measured
   reason.
6. **Checks.** `pytest` on the new modules and every test file touched or
   named in item 1, `pytest -m "not live"`, `python3 -m mypy`,
   `python3 tools/envelope_scan.py --range github/main..HEAD`. CI `verify`
   is the gate for the full suite. Fill a "Track 1 result" section in the
   plan.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Published citizens and schemas are immutable: successors only.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
  if held, retry every 10 s up to 5 min.
- Never --no-verify or a bare git stash. Foreground only. No push, no
  spawn.
