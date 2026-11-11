# Charter: P0 of live evidence harnesses running in isolation

Role: Builder. Source HEAD on milestone/live-harness-isolation-2025.
Plan: docs/phases/engine-breadth/milestones/live-harness-isolation.md
(read it whole). Do not read governance.

## Scope

1. **Inventory.** Every test module that loads a file by path or imports
   an evidence harness; which harnesses each loads; every place a harness
   or test assigns another module's attribute or a shared global
   (including `sys.modules` entries and module-level caches). Commit a
   small tool that prints this inventory.
2. **Reproduce.** Run pairs of modules that share harnesses on one worker
   (`-n 0` or `-p no:xdist`) in both orders, live lane included where
   needed, and record any order-dependent failure. Keep runs bounded:
   choose pairs from the inventory, not the full cross product. Record
   what the #264 harness-leak fix changed and whether the class remains.
3. **Design.** One shared loader under tests/ that gives each test module
   private copies of the harnesses it names, or a subprocess where a
   harness mutates global engine state. Measure its cost on two modules.
   List every module to move.

Stop and report before any change under packages/.

## Deliverables

In docs/phases/engine-breadth/milestones/live-harness-isolation-evidence/:
p0.md (inventory, reproductions, design, cost, module list, and decisions
for the foreman), the inventory tool, and small JSON outputs. Fill the
plan's "P0 result" section. No test or production edits beyond the tool.

## Rules

- No absolute or temp-directory paths in committed files, prose included.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Never --no-verify or a bare git stash. Run foreground commands only. No
  push, no spawn. Do not edit packages/.
