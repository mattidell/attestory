# Charter: Track 1 of every line speaking plainly — core v96

Role: Builder. Source HEAD on milestone/plain-line-texts-2025 (main at
core v95, registry v93, release v93).
Plan: docs/phases/engine-breadth/milestones/plain-line-texts.md. Read
Decisions 1-10 (Decision 9 amends 7). Evidence:
plain-line-texts-evidence/ (track0.md, track0-wording.json,
track0_validate.py, p0c_runtime.py, p0c_replay.py, p0c_compare.py and
their JSON). Precedent for content builds and tests:
tests/test_line16_names_v95.py and tests/test_line16_names_v95_package.py.
Do not read governance.

Stop and report if anything needs an edit under packages/kernel/,
packages/schemas/ or packages/presentation/, a recording change, or any
edit under packages/derivation/ other than Decision 5's table entry.

## Build

1. **Content.** The 50 successor citizens in packages/content/tax/2025/,
   byte-identical to Track 0's scratch citizens (rebuild them with
   track0_validate.py's builder if the scratch copies are gone, and show
   the digests match `track0-validation.json`). Never edit a published
   citizen.
2. **Validator (Decision 5).** In packages/derivation/package_validation.py
   add the `"v96"` successor-graph entry, identical to `"v68"` except
   `tax.us.2025.form1040.line-2b` at `form-field.v3` v7. Nothing else in
   that file changes.
3. **Core v96, registry v94, release v94** with
   `python3 -m tools.package_successor` on published v95, replacing
   exactly the 50 members. Add the v96 loader entries in
   packages/tax/loader.py carrying v95's unchanged, and extend any test or
   allowlist that enumerates cores (see what the v95 build touched:
   `git show 0bde6638 --stat`).
4. **Full replay.** All 775 recorded lists plus Track 0's synthetic set
   on published v95 and published v96, in parallel shards (CPU count
   minus one), in the foreground, part file outside the repo. Classify
   with the strict classifier and its 16 mutation controls: expect
   Track 0's 691 expected_sentences / 84 same_error (recorded) and
   nothing else, each changed sentence equal to its manifest text.
   Report wall time.
5. **Tests.**
   - A live module on published v96 through `live_coordinate_run`, the
     presentation projection and the saved page model, each distinct act
     list once: a wage-only return, an interest and dividends return, a
     closed-empty return (zeros by absence), a rounding-to-zero return,
     a sale and a mortgage-detail case. Assert the drawn manifest texts
     appear, no census term remains in any drawn content text, and
     values match v95.
   - A fast package test: byte identity with the manifest texts, exactly
     the 50 members replaced, registry v94 add-only, the loader entries,
     v95 and earlier unchanged.
   - A fast validator test: v96 with line-2b field v7 accepted, v96 with
     field v6 rejected with `NOMINEE_RETURN_SUCCESSOR_GRAPH_MIXED`, v95
     with field v7 rejected, v95 as published accepted.

   Load evidence only through tests/evidence_loader.py, with bare-name
   siblings bound by path first; keep every test under the 3.0 s
   fast-lane budget or `@pytest.mark.live` with a measured reason.
6. **Checks.** `pytest` on the new modules, every touched test file and
   tests/test_schema_registry.py; `pytest -m "not live"`;
   `python3 -m mypy`; `python3 tools/envelope_scan.py --range
   github/main..HEAD`. Because packages/derivation/ changes, also run the
   full `pytest` once and report its result. Fill a "Track 1 result"
   section in the plan, with deviations.

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
