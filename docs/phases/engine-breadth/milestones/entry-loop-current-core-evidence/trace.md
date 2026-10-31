# Trace: the entry loop on a workspace that adopts a current core

Probe: `probe.py` in this directory (run from the repo root). Synthetic data only.
Source ref: `12782b87`.

## What the entry loop does today

- `SyntheticW2EntryRuntime` builds a fixed `PublicationSurface`: release directory
  `packages/sample_data/frrs_t3/publication_surface/releases`, registry
  `packages/content/tax/2025/published-packages.json`. Nothing reads the workspace's
  adoption.
- The shipped seed adopts package v6 / release `demo.release.2025@v1` (scope 2055).
  `resolve_adopted_surface` over `frrs_t3` resolves that seed to the same
  `published-packages.json`, so for the shipped seed the resolver and the fixed
  surface agree. The seed runs: lines 1a, 9, 11, 15, 16 are not computed until the
  W-2 Box 1 is entered; 2b, 3a, 3b, 12 are computed.

## Workspace that adopts the latest core (package v66 / release v64 / registry v64)

Seed plus a v66 adoption act (the form the correction session's tests use):

1. Fixed surface: `entry-run-refused:RELEASE_ABSENT_OR_MISMATCH`. The v64 release
   is not in `frrs_t3`, so the loop refuses on opening. Refused, not miscalculated.
2. Resolver over the SLI release directory: resolves to `published-packages.v64.json`.
   A fresh `live_coordinate_run` on that surface does run (no refusal) but with 207
   blocked rows (172 `DEPENDENCY_ABSENT`, 35 `SOURCE_SET_UNCLOSED`): the thin entry
   seed lacks the source closures the later core requires.
3. **The v66 presentation does not carry the loop's lines.** It shows lines `11a`,
   `11b` and `12e`; there are no `11` (adjusted gross income) or `12` (standard
   deduction). `entry_loop._line_values` requires all nine of
   `EVALUATION_LINES` (1a, 2b, 3a, 3b, 9, 11, 12, 15, 16) and raises
   `entry-state-unavailable` otherwise. So even with the right surface resolved,
   the loop would end in a refusal on the current core.

## Result

Resolving the surface (the charter's Track 1 fix) is necessary but not sufficient.
The entry loop's questions and line set (lines 11 and 12, and the closures its
seed omits) are defined against the v6-era core; adopting the current core needs a
change to the loop's evaluation lines and to its seed, which the charter excludes
(questions, refusals, saved shape, seeds). Stop condition met: report the trace
only; no code changed.
