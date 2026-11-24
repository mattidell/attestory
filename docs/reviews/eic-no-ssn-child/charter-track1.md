# Charter: Track 1 of a child without a valid SSN routes the earned income credit correctly

Role: Builder. Source HEAD on milestone/eic-no-ssn-child-2025.
Plan: docs/phases/engine-breadth/milestones/eic-no-ssn-child.md (read it
whole; Decisions 1-4 bind). Evidence: eic-no-ssn-child-evidence/p0.md and
its scripts. Do not read governance.

## Scope

1. **Sources first (Decision 2).** Search the 2025 Form 1040 instructions
   and Publication 596 (fetched into ignored temp/) for any sentence that
   sends a filer whose qualifying children all lack a valid SSN to Step 4
   or chapter 3. Quote what you find, or record that none exists, before
   building. Choose the scope from that.
2. **Publish.** Core v102, registry v100, release v100 from published v101
   with the P0 route, widened or not per item 1. New files only; never edit
   a published file; the loader's v102 entries carry v101's. Follow the
   schema publication protocol in AGENTS.md for any manifest.
3. **Replay.** Strict full-surface replay of the 775 recorded lists, v101
   against v102, with expected changes declared; 0 unexpected; report
   unused expectations. No recorded number changes unless an expectation
   declares it and track1.md says why.
4. **Tests.** Live tests through the real coordinator for each traced case
   in p0.md plus the widened statuses (single, qualifying surviving spouse,
   married filing jointly, unmarried head of household), each against a
   hand credit from the 2025 table; a package test that loads v102; the
   Decision 4 mutations fail a test (show it on scratch copies; do not
   commit mutants). Fast lane, the touched live tests, mypy.

## Deliverables

The content, package, registry, release, loader entries and tests; in
eic-no-ssn-child-evidence/: track1.md (sources found for item 1, scope
chosen, files published, replay result, hand-credit table, tests run).
Fill a "Track 1 result" section in the plan. Commit in steps.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Nothing over 200 KB committed.
- Do not edit packages/kernel/ or the engine; content, package, release
  and loader entries only. Stop and report if the route needs more.
- An evidence script that imports a sibling harness by bare name loads it
  by path under a unique name instead.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn.
