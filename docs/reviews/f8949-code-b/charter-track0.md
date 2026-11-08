# Charter: Track 0 adversarial closure of broker basis corrections

Role: Builder. Source HEAD on milestone/f8949-code-b-2025.
Plan: docs/phases/engine-breadth/milestones/f8949-code-b.md. Read it
whole, including the P0 result and Decisions. P0 evidence is in
f8949-code-b-evidence/: p0-law-state-design.md, codeb_probe.py and
codeb_prototype.py. Gate: `PROJECT_PLANNING.md`, "Track 0 Adversarial
Closure Gate". Read that section and its closing paragraphs whole. The
f8949-boxes-cf Track 0 (f8949-boxes-cf-evidence/track0-closure.md) is
the precedent. Do not read governance.

## Scope

Over the decided design (Decisions 1-4), produce the gate's six
artifacts. Build the evidence through `live_coordinate_run` on the
scratch v81, never under packages/content.

1. **Authority-lifecycle table.** List every contributed fact and what
   invalidates each:
   - the basis shown and the correct basis on the sale;
   - the paired rows;
   - the column (g) row;
   - the new question and the new in-class answer;
   - code W combined with B.
2. **Empty/nonempty authority matrix.** Cover the code B families and
   their neighbours (the A/D, A/D code W, B/E and C/F families) under each
   answer combination:
   - a "yes" with nothing recorded;
   - a code B sale with a "no";
   - a code B sale beside a v80-only in-class answer.
3. **Late-member trace.** Answer "no", compute, add a code B sale,
   re-answer, recompute. Then correct a covered sale into a code B sale.
4. **Claim reuse.** Cover the v80 grouped questions, the in-class answers,
   ADR-0061 Path B and the code W family. Give the three-part proof, or
   show none is reused.
5. **Neighbor dependency diff.** All 143 v80 returns, before and after.
   Justify the new prerequisite.
6. **Integration surface.** Cover every consumer of lines 1a, 1b, 2, 7,
   8a, 8b, 9, 15, 16 and 21, line 7a, the preferential base and both
   attachments, with cardinality. Build one model per disposition path.
   Pin each blocked line's reason and its row's (disposition, code,
   missing). Include a presentation probe of each new or changed field.

The adversarial cases must include:
- a B and W row where the wash-sale amount exceeds the loss on the
  correct basis;
- a correction equal to the shown basis;
- a column (g) row that disagrees with its worksheet;
- the same transaction recorded on the covered family and the code B
  family;
- a sale whose correction flips a gain to a loss;
- a long-term code B sale with a holding-period mismatch.

Then write the closing declaration under the plan's "Track 0 adversarial
closure" heading. A row is PASS only if no counterexample stands beside
it. Where the design must change to pass, change the scratch prototype
(as switchable repairs) and say what changed. Where it cannot pass
without an engine, schema or recording change, mark it FAIL and stop.

## Deliverables

- f8949-code-b-evidence/track0-closure.md, holding the six artifacts.
- A harness module with a unique name, and its small output.
- The plan's "Track 0 adversarial closure" section.

No production, test or content edits.

## Rules

- Synthetic demo.* only, and no absolute or temp-directory paths in
  committed files.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir).
  If the lock is held, retry every 10 s for up to 5 min.
- Never use --no-verify or a bare git stash.
- Run foreground commands only.
- No push and no spawn.
- Do not edit packages/kernel/.
