# Review: the v70 entry seed generates without test helpers

Reviewer: fresh reader, author-independent.
Charter: `docs/reviews/seed-generator-independence/charter-review.md`.
Object: `milestone/seed-generator-independence-2025` at the review charter commit (removed at closeout).
The Orientation Block SHA matches `git rev-parse HEAD` at the start of this review.
Diffed against `github/main` at `e196842dc156961a8ec36bcee40fdb8ff5730f01`, which is also `origin/main`.
After `git fetch`: 0 behind, 10 ahead. PR #272 is open as a draft and has not merged. The branch is not spent.
Sources read: the milestone plan, the P0 record, the generator, the entry-loop test diff, the loader and evaluation runner, and the evidence tree's file list. Governance was not read.

The box. The generator may read the committed synthetic source `packages/sample_data/entry_loop_v70/complete-core-return.jsonl`, the legacy v6 seed named by `load_seed_acts`, and the v70 entry profile constants. Authority for regeneration is that source file. The generator publishes two seed files, `workspace/acts.jsonl` and `evaluation-w2.json`. Test modules stay outside. The seed bytes, the existing assertions, and the published schemas stay as they are on `github/main`.

## Findings

### S1. Should-fix: the scope capsule still says the byte test fails on helper drift

- **Where.** `docs/phases/engine-breadth/milestones/seed-generator-independence.md:9`.
- **Violated claim.** The scope sentence says the byte-regeneration test still fails on helper drift. Decision 3 (lines 112-115) says the opposite: the test catches source-fixture drift, and a change to the complete return is a deliberate refresh.
- **Reproduction.** Append one synthetic act from a replaced `tests.helpers.current_core_returns.base_return`. `render_fixture_files()` returns the same bytes as before the replacement. The helper call that `github/main`'s generator used, `_complete_core_return()`, returns different bytes under the same replacement. The helper modules themselves are unchanged on this branch; only the generator stopped calling them.
- **Consequence.** Plan evidence. A later unit that treats the capsule as the contract would put the helpers back on the regeneration path. The code matches Decision 3.
- **Fix.** Change the scope sentence so it says the byte test fails when the committed source and the committed seed disagree. Leave the generator independent of test modules.

### S2. Should-fix: the import test stays green for a `tests` import that render does not execute

- **Where.** `tests/test_entry_loop_t1.py:337`. Decision 3, lines 112-113.
- **Violated claim.** A test fails if the generator imports a test module, directly or transitively. The test observes `sys.modules` after `render_fixture_files()` in a fresh interpreter. An import the render path does not execute loads nothing, so the test passes.
- **Reproduction.** Both edits were restored and left uncommitted.
  - A module-level `import tests.helpers.current_core_returns` placed after the generator's import block makes `FixtureRegeneration.test_v70_generator_imports_no_test_module` fail: the child exits 1 and the assertion is `1 != 0`.
  - An uncalled function in the same file with that import leaves the same test passing (`1 passed`).
- **Consequence.** Evidence. The committed generator does not import a test module. Its static imports are the standard library plus `packages.derivation.entry_loop`. The clean test passed (`1 passed` in the same run as the byte test). The check does not establish Decision 3 for a `tests` import that `render_fixture_files` never reaches. P0 asked for a parse of the generator as well as the `sys.modules` check.
- **Fix.** Parse `tools/generate_entry_loop_v70_fixture.py` and fail on `import tests` or `from tests`. Keep the fresh-interpreter check so an import executed through `render_fixture_files` still fails.

### S3. Should-fix: the docstring names the refresh chain and cannot be run

- **Where.** `tools/generate_entry_loop_v70_fixture.py:4-10`. The callees are `tests/test_refund_or_amount_owed_track1.py:129` (`_finish`) and `tests/test_form_1099_k_income.py:113` (`_handover`).
- **Violated claim.** The docstring is the refresh recipe for `complete-core-return.jsonl`. It names `base_return`, `_finish` against the v70 core package and the v68 worksheet release, an adopted surface, and `_handover`.
- **Reproduction.** Calling `_finish` with only the act list raises `TypeError`. Calling `_handover` with only the act list raises `TypeError`. `_finish` requires `package_path`, `package_version`, `release_path`, `release_version`, and `note`. `_handover` requires `surface` and `reconfirm`. None of those arguments appear in the docstring. The committed source's package-adoption audit note is `demo.entry-loop.v70-complete-seed`, and its handover was produced with `reconfirm=True`: re-executing `github/main`'s `_complete_core_return()` writes bytes identical to the committed source (below).
- **Consequence.** A deliberate refresh that follows only the docstring cannot be executed. Guessing the missing note or omitting the reconfirm act would change the source, and then the seed.
- **Fix.** Record the exact call in the docstring, including `note="demo.entry-loop.v70-complete-seed"` and `reconfirm=True`, and the package and release filenames that call uses. Leave the source bytes as they are.

### N1. Note: a source edit the generator discards does not fail the byte test

- **Where.** `tests/test_entry_loop_t1.py:307` and `tools/generate_entry_loop_v70_fixture.py:82-94`.
- **What was measured.** `test_v70_seed_regenerates_and_leaves_only_box1_open` compares `render_fixture_files()` with the two committed seed files. Replacing the value on the one W-2 Box 1 member in a copy of the source leaves those rendered bytes identical, because `seed_acts` drops that member. Replacing the package-adoption audit note in a copy of the source changes the rendered seed. Decision 3's source-fixture drift is drift that survives into the seed. The open Box 1 member is outside the seed on purpose.
- **Fix.** None required for this unit. A direct byte compare of `complete-core-return.jsonl` would pin the discarded acts too, which this decision does not ask for.

### N2. Note: the moved-helper prototype does not run in CI, and it should stay as evidence

- **Where.** `docs/phases/engine-breadth/milestones/seed-generator-independence-evidence/move/seed_helpers/` (2,493 lines across the package) and `move/generate.py` (300 lines). `pytest.ini:14` sets `testpaths = tests`. `mypy.ini:3` sets `files = tools/, tests/, packages/`. `tools/governance_lint.py` lints `docs/governance/` only.
- **What was measured.** Default `pytest` does not collect this tree. `python -m mypy` does not type-check it. The files are in the `github/main..HEAD` diff, so `envelope_scan` does read them; that scan exited 0. The plan and `p0.md` cite this package as the measurement of the shape that was not chosen.
- **Fix.** Leave it. It is the record of that measurement. Product code should keep importing the generator in `tools/`, which reads the committed source.

## Measured against the charter

### Bytes

`render_fixture_files()` matches the committed seed, and those two files match `github/main`:

| File | Bytes | sha256 |
| --- | --- | --- |
| `workspace/acts.jsonl` | 323526 | `52898046d652a9e15f7f062ae09fc3c8a1b8dcb93c007f448624818035a4a4d7` |
| `evaluation-w2.json` | 386 | `95a796542960ca745ec9efeace603fa7f77bbce27a28d726e3413982ad3bfcad` |

`complete-core-return.jsonl` is 294 lines, 324079 bytes, sha256 `20cf8ee754967a81fdb1ab8f49c4bc6a373995e03d2e829d96362c854c1e0bb7`. Those bytes equal `github/main`'s `_complete_core_return()` and equal the evidence copy under `seed-generator-independence-evidence/source-fixture/`. The only path under `packages/` that differs from `github/main` is this source file. `packages/schemas` is unchanged.

### Independence

The generator file has no static `tests` import. `FixtureRegeneration.test_v70_generator_imports_no_test_module` and `test_v70_seed_regenerates_and_leaves_only_box1_open` passed together (`2 passed`). S2 records the hole in the import check and the edit that makes the check fail.

### Drift

On this branch the byte test fails when a kept act in the source, or the generator's own edits, disagree with the committed seed (N1). On `github/main` the same test also failed when `base_return` changed, because the generator called it. A core-package or release byte change still has a live observer elsewhere: the source adoption pins package `tax.us.2025.package.core-calculations` v70 checksum `fefc27600f12e577810c7a7b8cddbb354a710f258131a38750f67a11b275dc72`, which equals that package file's `package_checksum`, and release `demo.release.sli-worksheet-integration.2025` v68 checksum `3faac080d2806733b82ff473094f56fe7142055b16d6b0985f91d63d57cb9116`, which equals the sha256 of that release file. `production_resolver` admits a release only when that checksum matches (`packages/derivation/production_resolver.py:255`) and admits the package only when the adoption pin matches (`production_resolver.py:422`). `test_selected_members_read_exact_bindings_from_both_packages` and `test_surface_selection_follows_each_adoption_and_refuses_wrong_root` call that resolver on the v70 seed. Those two tests were not re-run in this review.

### Enumerators

`load_seed_acts` reads `workspace/acts.jsonl` by name (`packages/derivation/entry_loop.py:406`). The evaluation launcher reads `evaluation-w2.json` by name (`packages/derivation/runners/entry_loop_evaluation.py:39`). Its directory walk is the built surface distribution, not the fixture directory. The entry-loop data-safety scan walks `entry_loop_t1` (`tests/test_entry_loop_t1.py:2466`). `tests/test_incremental_lattice.py:32` globs `**/acts*.jsonl` and, under this directory, selects `workspace/acts.jsonl` only. On `github/main` the directory is the two seed files. HEAD adds `complete-core-return.jsonl` and no manifest.

### Assertions

`tests/test_entry_loop_t1.py` has 61 test methods on `github/main` and 62 on HEAD. The added method contributes one `assertEqual`. The multiset of assertion calls lost nothing. The 13 skipped tests are the same methods, with the same skip conditions, on both sides. No marker changed. The diff of that file is `import sys` plus the new test.

### Data safety

`python3 tools/envelope_scan.py --range github/main..HEAD` exited 0. The source actor is `demo.user.filer-1`. The file has 508 `demo.*` strings and none of the home-directory or ignored-local-data markers the entry-loop data-safety test forbids. A minority of act ids keep the helpers' existing synthetic forms (`act-syn-v2-*`, `ssa.handover.*`, `f.closure.demo.synthetic.*`). Those forms are already how this return is written. The scan and the read found no personal value.

### Evidence weight

Answered in N2. The prototype does not run in CI and is not type-checked. It should stay as the cited measurement.

## Verdict

ready

No blocking finding. Should-fix before closeout is the plan sentence (S1), the unexecuted-import hole (S2), and the refresh recipe (S3). The seed bytes, the helper-chain source, the passing import check on the committed generator, and the unchanged assertions can be reused as they stand.
