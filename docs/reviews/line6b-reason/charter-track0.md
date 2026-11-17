# Charter: Track 0 adversarial closure of line 6b naming why it is blocked

Role: Builder. Source HEAD on milestone/line6b-reason-2025.
Plan: docs/phases/engine-breadth/milestones/line6b-reason.md, read whole,
especially Decisions 1-7. P0 evidence: line6b-reason-evidence/ (p0.md,
probe.py, prototype.py, computing_neighbours.py and outputs). Seat
reading: docs/roles/qualitative-review.md. Do not read governance.

Work on the P0 scratch successor (ten input-question citizens on
published v91). Do not edit packages/ or tests/.

## Scope

1. **Question meaning.** For each of the ten questions: quote the fact
   it pins, the rule(s) that read it and the value each rule needs on the
   path that publishes line 6b, and the 2025 Form 1040 or instruction
   passage (local sources, file:line) the question restates. Then answer
   each question yes and no *through the question* as the page's entry
   path would record it (not by setting the fact by hand) and show the
   recorded fact value and line 6b's outcome. A negative-named fact
   (`no-...`) whose question asks "Do you have ...?" must still record the
   meaning the filer intended. FAIL any question whose answer records the
   opposite meaning, cannot be recorded through the entry path, or whose
   words are not true to the passage. Propose corrected words for each
   FAIL.
2. **Placement.** For every case in P0's probe and the seven computing
   neighbours: list every field that gains a question on the successor
   and its v91 disposition and `missing` names. FAIL any field that
   publishes a value and gains a question, and any added question on a
   field not already blocked on the fact it asks about.
3. **Each root alone.** For each of the ten facts, a case where only that
   fact is unanswered: line 6b (and any other blocked field) shows exactly
   that one question and no generic blocked text. Pair cases: two facts
   unanswered show both questions.
4. **Neighbours.** No benefit statement; benefits with every scope fact
   answered so line 6b computes; single, joint, separate; lump-sum
   election made and not made; SSA source set closed and open. Every page
   field's value, disposition and reason sentence is compared v91 vs
   successor; classify every difference.
5. **Drawn page.** Save the citation-walk page for one reproduced case
   and one separate-filing case and open each in headless Chrome as the
   page-alerts evidence did; confirm the question text draws under the
   field and no safe-render alert appears.
6. **Replay reuse.** Reuse P0's replay result; do not replay again unless
   a citizen's bytes change, and if they do, rerun with
   `python3 tools/recorded_replay.py` in parallel (CPU count minus one
   workers) and report wall time.

Write a PASS/FAIL table per item. If a FAIL needs more than new question
words (a rule, projection, page, schema or engine change), stop and
report.

## Deliverables

In line6b-reason-evidence/: track0.py, track0-*.json, track0-closure.md
(tables, FAILs with proposed fixes, recommendation). Update the plan's
"Track 0 adversarial closure" section (add it after Decisions). No
production, test or content edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Load sibling harnesses by path under a unique name, never a bare
  `import probe`.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Never --no-verify or a bare git stash. Foreground commands only; no
  background jobs left running.
- No push and no spawn. Do not edit packages/ or tests/.
