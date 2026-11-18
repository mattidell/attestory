# Charter: P0c of every line speaking plainly

Role: Builder. Source HEAD on milestone/plain-line-texts-2025.
Plan: docs/phases/engine-breadth/milestones/plain-line-texts.md (Decisions
1-6 govern). Continue from your P0b evidence and scratch files. Do not
read governance.

## Scope

1. **Scratch validation.** In the evidence harness only, add the plan's
   Decision 5 `"v96"` successor-graph entry to the validator's table at
   runtime (identical to `"v68"` except line-2b field v7). Do not edit
   packages/. Build and validate the scratch core v96, registry and
   release from published v95 plus the 50 prepared successor citizens.
   Show that the same scratch package with line-2b field v6 is rejected
   under the injected entry, and that v95 is unaffected. Any other
   validation failure: stop and name it.
2. **Strict replay.** Replay the 775 lists on v95 (reuse the P0b baseline
   part if it carries everything below) and on the scratch successor in
   parallel shards, keep the part file outside the repo for Track 0, and
   classify strictly: compare every row and every page field (including
   added or removed ones) and fail any changed value, disposition,
   refusal code, missing name or question identity before labelling a
   change expected. Expected: only the 57 replaced sentences change,
   each from its recorded old text to its recorded new text. Mutation
   controls: a changed value, disposition, code, missing name and an
   unplanned sentence must each be rejected. Report wall time.
3. **Wording check.** Re-read each of the 57 replacements against the
   local 2025 sources and the census context where it is drawn; fix any
   that overstates or loses what the old sentence proved.

## Deliverables

p0c.md in the evidence directory (validation, replay classification,
mutation controls, wording check, recommendation, decisions for the
foreman), scripts and small JSON outputs. Append a "P0c result" section
to the plan. No production, test or content edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only.
- No push and no spawn. Do not edit packages/.
