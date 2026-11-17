# Charter: Track 0 adversarial closure of a box 4 "no" not being asked for an amount

Role: Builder. Source HEAD on milestone/box4-no-prompt-2025.
Plan: docs/phases/engine-breadth/milestones/box4-no-prompt.md, read whole,
especially Decisions 1-6. P0 evidence: box4-no-prompt-evidence/ (p0.md,
probe.py, prototype.py, classify.py, replay_candidate.py and outputs).
Seat reading: docs/roles/qualitative-review.md. Do not read governance.

Work on P0's final scratch successor (v94 on published v93). Do not edit
packages/ or tests/.

## Scope

1. **Statement locality.** Two and three statements with mixed answers:
   no + yes-with-amount, no + unanswered, no + yes-without-amount,
   no + no. Line 25b computes only when every sale statement is
   satisfied, sums only recorded amounts, and otherwise blocks naming the
   statement amount it still needs. FAIL if one statement's "no"
   satisfies another's.
2. **Repeated sales on one statement.** Two and three sales on one
   statement answered "no", and answered "yes" with one amount: the
   statement's amount counts once.
3. **Contradiction and zero.** "No" with $0; "no" with 200 (200 counts,
   Decision 2); "yes" with $0.
4. **Correction and withdrawal.** Answer "no", then change to "yes"
   (amount prompt returns); withdraw the "no" (back to v93 behaviour);
   enter an amount after "no".
5. **Every sale subject type.** One case per each of the eight sale
   fact types the pairing names, each answered "no" alone.
6. **What the filer sees next.** For each case where line 25b still
   blocks after a "no", quote every reason and question sentence on
   lines 25b, 25d, 33 and 37. Judge whether the return-level "statement
   with no sale" question reads truthfully to a filer who has just
   answered "no" for their sale statements (the page model's own
   sentences, no punctuation filter). FAIL a sentence that is untrue or
   that tells the filer to do something already done; propose words.
7. **Neighbours.** No Form 1099-B; a 1099-B return with every answer in
   so it computes; single, joint and separate. Every page field's
   value, disposition and reason sentence, v93 vs successor; classify
   every difference. FAIL a computing return that changes or gains a
   question.
8. **Smaller shape (optional, Decision 4).** If an admitted content shape
   with fewer rules keeps items 1-5 passing, show it; do not block on it.
9. **Replay reuse.** Reuse P0's part file; replay again only if content
   bytes change, then with `python3 tools/recorded_replay.py` in
   parallel (CPU count minus one workers), and report wall time.

Write a PASS/FAIL table per item. If a FAIL needs more than content (a
projection, page, schema or engine change), stop and report.

## Deliverables

In box4-no-prompt-evidence/: track0.py, track0-*.json, track0-closure.md
(tables, FAILs with proposed fixes, recommendation). Add a "Track 0
adversarial closure" section to the plan after Decisions. No production,
test or content edits.

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
