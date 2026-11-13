# Charter: Track 0 adversarial closure of blocked lines naming their question

Role: Builder. Source HEAD on milestone/blocked-names-question-2025.
Plan: docs/phases/engine-breadth/milestones/blocked-names-question.md (read
it whole, including the P0 result and Decisions 1-6). Proposed contract:
docs/adr/0086-block-declares-missing-names.md. Evidence:
blocked-names-question-evidence/ (start with p0.md). Gate:
`PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate" (read that section
and its closing paragraphs whole). Precedent:
question-wording-evidence/track0-closure.md and its track0.py. Do not read
governance.

## Scope

Every claim comes from a `live_coordinate_run` output saved in a committed
JSON file and named by case id, on published v87 and the scratch successor.
Hand values come from the 2025 instructions, never from what the prototype
publishes. A question is tested by answering it as a truthful filer would
read it. Never work under packages/.

1. **Authority-lifecycle table**, per declared name: which block declares
   it, which question or closure mapping it resolves to, what answers it,
   and what the return does once answered (computes to hand values, or a
   different block that itself names its question).
2. **Empty/nonempty matrix**: each of P0's ten cases unanswered, then
   answered each truthful way; no case may end at a block with zero
   questions.
3. **Late-member traces:** a sale added after Form 8949 "yes" was
   answered; an amount corrected so it no longer disagrees; a wash
   adjustment added after the family closed.
4. **Claim reuse:** the declared names add no read, pin, dependency or
   answer change: the ten successors evaluate identically to their
   predecessors on every input except the `missing` list.
5. **Neighbour diff:** the 775 recorded lists on v87 and the scratch
   successor, in parallel shards (CPU count minus one, at most 4 while
   other builders share the machine), reusing P0's replay where the
   scratch core is unchanged. Classify every change.
6. **Integration surface:** for each case, the exact question sentences
   the page shows, and that every blocked filer-visible field names a
   question.

## Deliverable

blocked-names-question-evidence/track0-closure.md and track0.py with its
`track0-*.json` outputs, and a "Track 0 adversarial closure" section in the
plan: each table PASS or FAIL with counts and case ids, and "Known
limitations affecting correctness".

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Do not edit packages/. Stop and report if the design needs a kernel
  change or changes which answer a path needs.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
  if held, retry every 10 s up to 5 min.
- Never --no-verify or a bare git stash. Foreground only. No push, no
  spawn.

## Amendment: the integration-surface failure

Foreman, 2026-11-12. The 15 reasonless fields in
`exception1_personal_loss_8949` are the dead end this milestone removes, so
they are in scope.

7. **Trace.** For each of the 15 fields, on v87 and the scratch successor,
   walk the blocked producers to their roots: which rule blocks, with which
   code and `missing`, and why the projection yields no reason (an empty
   `missing`, a name with no question citizen, or the all-roots rule
   meeting an unexplainable root). Cite file:line. Say whether the same
   fields are reasonless on v87.
8. **Repair in the prototype** if the root is another undeclared
   expression block or a name with no citizen: the same mechanism (declare
   names; add a citizen), as further successors. Rerun the surface, matrix
   and reuse tables, and the neighbour diff only if the scratch core's
   affected rules changed (in parallel shards, at most 4).
   Stop and report instead if the repair needs a change to the
   presentation projection or the kernel, with the smallest change named.
9. Update track0-closure.md and the plan's Track 0 section.
