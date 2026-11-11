# Retrospective: Live Evidence Harnesses Run in Isolation

Milestone key: live-harness-isolation. Plan:
`docs/phases/engine-breadth/milestones/live-harness-isolation.md`.
Closed 2026-11-11. Tooling only: no package, schema or content changed.

## What happened

P0 inventoried every test module that loads a Python file by path. Twenty
reached a milestone evidence harness in-process, and four of those reached
a harness that writes an engine attribute without restoring it. One-worker
runs of the suspect pairs passed in both orders, so the work was preventive.

Track 1 added one loader, `tests/evidence_loader.py`. Each test module gets
private copies of the harness modules, nested bare imports included, while
`packages.*` and `tests.*` stay shared. Engine attributes a harness writes
are snapshotted and restored when the owning module is parked or finished,
so no module needed a subprocess. All twenty modules moved. A guard test
fails if a module loads an evidence file another way, or if a harness
writes an engine attribute the loader cannot put back. Test counts matched
before and after apart from the loader's own tests, and module walls did
not move.

The fresh review found the guard blind to `exec` of a file's text, and that
reactivating a parked owner could overwrite a value set outside the
harness. Both were repaired with tests that fail without the repair.

## What worked

- Preferring restore over subprocess. P0 priced the subprocess, but
  restoring proved exact for every write, so CI paid nothing.
- A guard built on the P0 inventory tool, so the measurement became the
  pin.

## What to change

- The build found two sharing bugs only by running the live modules: a
  package child binding lost on park, and C code (`datetime.strptime`)
  reading the interpreter's own module dict. A loader that swaps module
  tables should test both from the start.
- Track 1 ran for over four hours of wall time, mostly re-running live
  modules to time them. A wall table for the slowest modules would have
  done.

## Follow-ups

None parked. The three subprocess modules and the eight modules that load a
tool or another test stay as they are, by decision.
