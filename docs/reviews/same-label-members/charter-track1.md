# Charter: Track 1 of two members with the same name each get their question

Role: Builder. Source HEAD on milestone/same-label-members-2025.
Plan: docs/phases/engine-breadth/milestones/same-label-members.md (read it
whole; Decisions 1-3 govern). Evidence: same-label-members-evidence/p0.md
(section 7) and scratch-projection.diff. Do not read governance.

## Scope

1. In `packages/derivation/presentation_projection.py`, key the walk's
   member questions by the member (its fact or entity id), not its label,
   so each member that misses an answer gets its own reason carrying its
   `memberLabel`. Do NOT add `memberOrdinal` or any page wording change;
   that is Track 2 under proposed ADR 0090.
2. Update `tools/sale_page_observation.py` only if it must follow.
3. Tests in the `tests/test_eic_child_answers_walk.py` style: two and
   three same-label members each missing the answer; one of two missing;
   two missing different answers; distinct-label and cross-kind controls.
   A live test over a subset of `probe.CASES` with the DOM checker.
4. Full-surface replay on the built code (one shared run, parallel
   workers): expect 775 recorded lists identical, and the probe returns to
   differ only by the added member reasons.
5. Checks: substrate rule — this touches packages/derivation/, so run the
   full suite once before handing off; mypy on touched modules.

## Deliverables

Code, tests, `same-label-members-evidence/track1.md`, a "Track 1 result"
section in the plan. Commit in steps.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Do not edit packages/kernel/, any published file, or any schema.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn.
