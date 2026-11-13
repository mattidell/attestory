# Charter: Track 1 of blocked lines naming their question — core v89

Role: Builder. Source HEAD on milestone/blocked-names-question-2025.
Plan: docs/phases/engine-breadth/milestones/blocked-names-question.md. Read
Decisions 1-6 and "Track 0 adversarial closure". Contract: the accepted
docs/adr/0086-block-declares-missing-names.md (its Decision and
Consequences control). Evidence: blocked-names-question-evidence/
(track0-closure.md, prototype.py, track0.py and their JSON). Precedent:
ADR 0085's build (rule-artifact.v16, artifact-package.v42) in
tests/test_f1099b_selection_keyed_collect_v86.py and
tests/test_f1099b_selection_keyed_collect_v86_package.py; the content
build shape in tests/test_age_blindness_v88.py and
tests/test_age_blindness_v88_package.py. Do not read governance.

Stop and report if anything needs an edit under packages/kernel/, a change
to the presentation projection, a recording change, or a change to which
answer any path needs.

## Build

1. **Schemas.** Publish `rule-artifact.v17` (v16 plus the optional
   `missing` on an expression `block`) and `artifact-package.v43` (v42
   plus a v17 member), each with `write_manifest` (add-only; inspect the
   manifest diff). Never edit a published schema.
2. **Derivation.** Thread v17 through every enumeration that lists v16,
   and teach the evaluator to raise a selected block's code with exactly
   its declared names (none declared: the empty list, as before). Unit
   tests: declared names carried; absent names unchanged; v16 artifacts
   byte- and behavior-stable.
3. **Content.** Bring the decided members into packages/content/tax/2025/
   as new versioned citizens, byte-identical to prototype.py's build: the
   eleven rule successors (including Form 1040 line 16) and the two
   Schedule D boundary input questions. Never edit a published citizen.
4. **Core v89, registry v87, release v87** with
   `python3 -m tools.package_successor`, on artifact-package v43. Add the
   v89 loader entries in packages/tax/loader.py carrying v88's unchanged,
   and extend any test that lists cores carrying a map.
5. **Tests.**
   - A live module running the Track 0 authority, matrix, late and
     surface cases on published v89 through `live_coordinate_run` and the
     presentation model; each distinct act list once; hand values from
     the instructions; every blocked filer-visible field names a question.
   - The 298 v83 recorded lists on published v89 against their fixture in
     place: identical numbers (the 775-list result stays in the committed
     evidence; reproduce it with `tools/recorded_replay.py` only if a
     content change differs from the prototype).
   - A fast package test: byte identity against the prototype, the exact
     member edits, registry v87 add-only, the loader entries, v88 and
     earlier unchanged.

   Load evidence only through tests/evidence_loader.py. Keep every test
   under the 3.0 s fast-lane budget or `@pytest.mark.live` with a measured
   reason.
6. **Checks.** Substrate changed, so run the **full** `pytest` (shards are
   fine; sum the counts), `pytest tests/test_schema_registry.py`,
   `python3 -m mypy`, and `python3 tools/envelope_scan.py --range
   github/main..HEAD`. Fill a "Track 1 result" section in the plan.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Published citizens and schemas are immutable: successors only.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
  if held, retry every 10 s up to 5 min.
- Never --no-verify or a bare git stash. Foreground only. No push, no
  spawn.
