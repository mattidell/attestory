# Charter: P0 of the Rust kernel experiment (profile)

Role: Builder. Source HEAD on milestone/rust-kernel-experiment-2025.
Plan: docs/phases/engine-breadth/milestones/rust-kernel-experiment.md
(read it whole). Tooling: tools/recorded_replay.py (the recorded-list
replay harness) and the replay scripts in
plain-line-texts-evidence/ (track1_replay.py) as precedent. Do not read
governance.

## Scope

1. **Pick the workload.** On published core v96, choose (a) the median
   and the slowest recorded act list by wall time, and (b) one long
   correction story from the test suite (the 2026-10 profile used
   `tests/test_sli_track1_combined_standing.py` case K13; pick the
   current slowest live test if that one is gone). Record how you chose
   and the sizes (acts, assertions, facts).
2. **Profile.** cProfile (and a sampling profiler such as py-spy if
   installed; do not install system packages) each workload in a single
   process. Report cumulative time by layer: kernel act log/fact
   store/finding model, derivation evaluator/runner, presentation
   projection, jsonschema validation, JSON (de)serialization, file I/O.
   Name the top 15 functions by cumulative and by own time, with
   file:line and call counts.
3. **Shape of the cost.** For the slowest list, time the replay at
   prefixes of its act log (for example 25/50/75/100 %) and say whether
   the cost grows linearly or faster. Name the loop that makes it
   superlinear, if any, with file:line.
4. **Lever comparison.** For the top cost centres, say which part is
   algorithmic (repeated work a cache or incremental update in Python
   would remove) and which is constant-factor (work that must happen,
   where a compiled language helps). Estimate each lever's saving from
   the profile, not by guess. Do not implement either.
5. **Port candidate.** Name the smallest kernel slice whose port would
   capture most of the constant-factor cost: its modules and functions,
   the data crossing the Python boundary per call, and how the result
   would be checked byte-identical. Say what it does not cover. Note any
   coupling to jsonschema or to Python objects that would make a binding
   costly.

Stop and report if profiling needs a change under packages/ to run.

## Deliverables

In docs/phases/engine-breadth/milestones/rust-kernel-experiment-evidence/:
p0.md (workloads, layer table, top functions, growth curve, lever
comparison, port candidate, recommendation, decisions for the foreman),
the scripts, and small JSON summaries. Do not commit raw .prof files or
anything over 200 KB. Fill the "P0 result" section in the plan. No
production, test or content edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- An evidence script that imports a sibling harness by bare name loads it
  by path under a unique name instead.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Write your JSON report before your final checks, so a usage limit
  does not lose it; update it when the checks finish.
- Never --no-verify or a bare git stash. Foreground commands only; do not
  leave background jobs running when you finish.
- No push and no spawn. Do not edit packages/ or tests/.
