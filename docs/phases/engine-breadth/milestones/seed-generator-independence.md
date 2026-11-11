<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "seed-generator-independence",
  "status": "Open. P0 measured; Decisions 1-5; Track 1 chartered.",
  "scope": [
    "tools/generate_entry_loop_v70_fixture.py regenerates the committed v70 entry seed without importing any test module",
    "the committed seed fixture bytes are unchanged, and the byte-regeneration test fails when the committed source and the committed seed disagree",
    "no test asserts less than before, and no published package, schema or content changes"
  ],
  "non_goals": [
    "no change under packages/ except where the decision names a non-runtime sample-data source",
    "no change to the seed's acts, ids or bytes",
    "the other golden generators under tools/ that import test modules"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/seed-generator-independence.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/seed-generator-independence.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/seed-generator-independence.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/seed-generator-independence.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# The v70 Entry Seed Generates Without Test Helpers

Milestone key: seed-generator-independence.
Branch: milestone/seed-generator-independence-2025.
Phase: Engine Breadth, tooling. Opening plan: 2026-11-11.
Starting point: `github/main` at `e196842d` (core v85).

## What we are trying to accomplish

The entry loop's production runtime reads one committed synthetic seed, the
v70 W-2 entry seed. The tool that writes it,
`tools/generate_entry_loop_v70_fixture.py`, builds the seed from a complete
current-core return assembled by test helpers:
`tests.helpers.current_core_returns.base_return`,
`tests.test_form_1099_k_income._handover` and
`tests.test_refund_or_amount_owed_track1._finish`, which in turn import
several more test modules. A refactor of any of those tests can silently
change how the seed would regenerate. The useful outcome is a generator
whose inputs are named, committed and independent of test modules, with the
seed's bytes unchanged.

## What we know

- The runtime imports none of these helpers; only the generator and its
  byte-regeneration test (`tests/test_entry_loop_t1.py`) do.
- `tests/helpers/current_core_returns.py` itself imports at least eight test
  modules.
- **What we do not know.** The full transitive set of test code the seed
  depends on; whether to move that code out of `tests/`, or to commit the
  complete return's acts as a named source fixture and generate from it;
  which other tests share the helpers and would move with them.

## Actions the team will take

1. **P0: measure.** Trace every test module and function the generator
   reaches. Prototype both shapes (move the helpers; commit a source
   fixture) far enough to show the seed regenerates byte-identical, and
   measure each shape's diff size and what other tests it touches. Stop
   and report before any change under `packages/`.
2. **Decide.** The shape, its file locations, and the drift check.
3. **Track 1: build.** The chosen shape, the generator importing no test
   module, and a test that fails if it does.
4. **Close.** Fresh-reader review, repair, exact-head CI, retrospective,
   roadmap. Merge on green verify (owner standing approval, 2026-11-07).

Track 0 adversarial closure does not apply: no tax claim or engine
contract changes. The review checks that the seed bytes and every
assertion are unchanged.

## Process

Dispatch is through the grok CLI (owner, 2026-11-09). Each unit commits on
this branch as it goes. The milestone publishes no package, so it does not
stack on PR #270's core v86.

## P0 result

The source-fixture shape is the one to build. Both scratch prototypes regenerate the committed v70 seed byte for byte. The source fixture is 294 lines of synthetic acts plus a 246-line generator, and it leaves every test import where it is. The move copies 1,870 lines of helpers into a 2,493-line package and would retarget 56 other test modules and 2 tools. Track 1 should commit the complete return as `packages/sample_data/entry_loop_v70/complete-core-return.jsonl`, point the generator at that file, and fail if the generator imports a test module. The byte-regeneration test then catches source-fixture drift. Evidence: `docs/phases/engine-breadth/milestones/seed-generator-independence-evidence/p0.md`. No change under `packages/` in P0.

## Decisions

Foreman, 2026-11-11, on P0. Both shapes regenerate the seed byte for byte;
the source fixture costs a fraction of the move and touches no test.

1. **Source fixture.** The complete current-core return the generator
   receives, before its own edits, is committed as a synthetic source file
   and the generator reads it. No helper moves.
2. The source lives at
   `packages/sample_data/entry_loop_v70/complete-core-return.jsonl`, beside
   the seed it produces. Nothing at runtime reads it; Track 1 confirms no
   loader, manifest or checksum enumerates that directory in a way the new
   file would change.
3. **Checks.** A test fails if the generator imports a test module,
   directly or transitively. The existing byte-regeneration test now
   catches source-fixture drift; a change to the complete return is a
   deliberate source refresh, not a side effect of a test refactor.
4. The other golden generators under `tools/` that import test modules
   stay out of scope.
5. The seed's bytes do not change. Nothing else under `packages/`
   changes.

## Track 1 result

The generator reads `packages/sample_data/entry_loop_v70/complete-core-return.jsonl`. That file is the complete return produced once from the current test helpers, before the generator's own edits: 294 lines, 324079 bytes, sha256 `20cf8ee754967a81fdb1ab8f49c4bc6a373995e03d2e829d96362c854c1e0bb7`. The generator's docstring records that production and that refreshing the file is deliberate.

Byte check. Regenerating the seed matches the committed files. `workspace/acts.jsonl` is sha256 `52898046d652a9e15f7f062ae09fc3c8a1b8dcb93c007f448624818035a4a4d7` (323526 bytes). `evaluation-w2.json` is sha256 `95a796542960ca745ec9efeace603fa7f77bbce27a28d726e3413982ad3bfcad` (386 bytes).

Enumerators. `load_seed_acts` reads `workspace/acts.jsonl` by name. The directory has no manifest or checksum. Schema checksums stay in schema directories. `tests/test_incremental_lattice.py` globs `**/acts*.jsonl`, which does not select this file. The entry-loop data-safety scan walks `entry_loop_t1`. The envelope scan reads the diff. The new file leaves those behaviors unchanged.

Counts. `tests/test_entry_loop_t1.py` had 61 tests before this track and collects 62 after. The added test is `FixtureRegeneration.test_v70_generator_imports_no_test_module`. No other test module changed, and no existing assertion changed.

What the checks catch. `test_v70_seed_regenerates_and_leaves_only_box1_open` fails when the source fixture and the committed seed disagree. A later edit to a test helper leaves the seed where it is until the source file is refreshed on purpose. `test_v70_generator_imports_no_test_module` fails when a fresh interpreter that imports the generator and renders the fixture has a `tests` module loaded. Before the generator change, that check saw 22 such modules.
