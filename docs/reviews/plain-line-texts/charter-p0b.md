# Charter: P0b of every line speaking plainly

Role: Builder. Source HEAD on milestone/plain-line-texts-2025.
Plan: docs/phases/engine-breadth/milestones/plain-line-texts.md (read it
whole; Decisions 1-4 govern). Precedent: this milestone's P0 evidence
(census.py, observe.mjs, content-trace.json), line16-names-evidence
(classify.py and replay scripts). Do not read governance.

## Scope

1. **Complete census.** Extend census.py to all 775 recorded lists on
   published core v95 (parallel shards, CPU count minus one; one shared
   replay). Collect every content-supplied sentence a filer sees under
   Decision 2: from the presentation projection's page model, plus the
   detail surfaces that draw content properties. Report the citizens,
   properties, page fields and list counts, and separately any content
   property drawn only inside a support trace. Page-owned captions,
   badges and banners are out of scope (Decision 1); count them once and
   do not design them.
2. **Wording.** For each flagged content sentence, decide under Decision
   3 whether it is engine language to a filer, and write a plain
   replacement checked against the 2025 Form 1040 instructions and the
   relevant schedule or form instructions in the local sources. Keep
   what the sentence says is true: a zero must still name the absence or
   completed calculation behind it. Record old and new text side by side.
3. **Scratch successor.** Build a scratch core v96 on published v95 that
   adopts content successors of exactly the citizens whose text changes,
   with byte-identical values, requires, pins, guards, `missing` names
   and refusal codes. Loaded from published content plus scratch files;
   never edit packages/. If a sentence cannot change without a schema,
   projection, page or kernel change, stop and name it.
4. **Strict replay.** Replay the 775 lists on v95 and the scratch
   successor in parallel, keep the part file outside the repo for Track
   0, and classify strictly: compare every row and every page field
   (including added or removed ones) and fail any changed value,
   disposition, refusal code, missing name or question identity before
   labelling a change expected. Expected: only the replaced sentences
   change. Include mutation controls (a changed value, disposition, code,
   missing name and an unplanned sentence must each be rejected). Report
   wall time.

## Deliverables

In docs/phases/engine-breadth/milestones/plain-line-texts-evidence/:
p0b.md (census table, wording table, scratch build, replay
classification, mutation controls, recommendation, decisions for the
foreman), scripts and small JSON outputs. Append a "P0b result" section
to the plan. No production, test or content edits.

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
- No push and no spawn. Do not edit packages/.
