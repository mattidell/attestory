# Charter: P0 of the v70 entry seed generating without test helpers

Role: Builder. Source HEAD on milestone/seed-generator-independence-2025.
Plan: docs/phases/engine-breadth/milestones/seed-generator-independence.md
(read it whole). Do not read governance.

## Scope

1. **Trace.** Every test module, function and constant that
   `tools/generate_entry_loop_v70_fixture.py` reaches, transitively, with
   the reason each is reached. Which other test modules import the same
   helpers. Commit a small tool that prints this trace.
2. **Prototype both shapes** in scratch copies under the evidence
   directory, never in tracked test or tool files:
   - **Move:** the reached helper code moves to a non-test module, and
     the tests import it from there.
   - **Source fixture:** the complete return's acts, as the generator
     receives them before its own edits, are committed as a named
     synthetic source file, and the generator reads that file.
   For each, regenerate the seed and show it is byte-identical to the
   committed fixture. Measure lines moved or added, tests touched, and
   what the existing byte-regeneration test in
   `tests/test_entry_loop_t1.py` would still catch (helper drift,
   source-fixture drift).
3. **Recommend** one shape, its file locations, and the check that fails
   if the generator imports a test module.

Stop and report before any change under packages/.

## Deliverables

In docs/phases/engine-breadth/milestones/seed-generator-independence-evidence/:
p0.md (trace, both prototypes, measurements, recommendation and the
decisions for the foreman), the trace tool, scratch prototypes, and small
JSON outputs. Fill the plan's "P0 result" section. No test, tool or
production edits outside the evidence directory.

## Rules

- Synthetic demo.* only. No absolute or temp-directory paths in committed
  files, prose included.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Never --no-verify or a bare git stash. Run foreground commands only. No
  push, no spawn. Do not edit packages/.
