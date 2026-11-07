# Charter: Track 0 adversarial closure of sales without a Form 1099-B

Role: Builder. Source HEAD on milestone/f8949-boxes-cf-2025.
Plan: docs/phases/engine-breadth/milestones/f8949-boxes-cf.md (read it
whole: P0 result and Decisions). P0 evidence:
f8949-boxes-cf-evidence/p0-law-state-design.md, cf_probe.py,
cf_prototype.py and cf-prototype-rules/. Gate: `PROJECT_PLANNING.md`,
"Track 0 Adversarial Closure Gate" (read that section and its closing
paragraphs whole). Do not read governance.

## Scope

Over the decided design (Decisions 1-3), produce the gate's six
artifacts. Build the evidence through `live_coordinate_run` on the
scratch v80 under the evidence directory, never under packages/content.
First add Decision 3 (the missing-amount check on lines 2 and 9) to the
scratch prototype.

1. **Authority-lifecycle table.** List every contributed fact and what
   invalidates each:
   - the filer-supplied proceeds and basis;
   - the new no-1099-B question;
   - the new in-class answer and the v79 in-class answer;
   - code W on boxes C and F.
2. **Empty/nonempty authority matrix.** Cover the new box C/F families
   and the B/E families under each combination of the two grouped
   questions, including a "yes" with nothing recorded and a Form 8949
   "no".
3. **Late-member trace.** Attest, answer the new question "no", compute,
   add a box F sale, reanswer, recompute. Do the same with a box C sale
   added after a v79-style return already computed.
4. **Claim reuse.** Say whether any existing claim is reused (the v79
   grouped answer, the ADR-0061 boundary pair, the preferential-base
   gate) and give the three-part proof, or show that none is.
5. **Neighbor dependency diff.** Compare every return v79 computes,
   before and after: the 46 cases P0 ran plus the box B/E missing-amount
   cases. Justify or remove any new prerequisite on a return with no
   sales; the new question is the obvious one.
6. **Integration surface.** Cover every consumer of Schedule D lines 2, 3,
   7, 9, 10, 15, 16 and 21, Form 1040 line 7a, the preferential base and
   the Form 8949 and Schedule D attachments, with cardinality. Build one
   model per disposition path and assert each attachment disposition.
   Include a presentation-model probe for each new or changed form field:
   value, explanation sentence, blocked reason and question shown.

Then write the closing declaration under the plan's "Track 0 adversarial
closure" heading. A row is PASS only if no counterexample stands beside
it. Where the design must change to pass, change the scratch prototype
and say what changed. Where it cannot pass without an engine, schema or
recording change, mark it FAIL and stop.

## Deliverables

- f8949-boxes-cf-evidence/track0-closure.md, holding the six artifacts.
- The scratch prototype and its output. Keep them small, with no copies of
  the content tree.
- The plan's "Track 0 adversarial closure" section.

No production, test or content edits.

## Rules

- Synthetic demo.* only, and no absolute paths in committed files.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir).
  If the lock is held, retry every 10 s for up to 5 min.
- Never use --no-verify or a bare git stash.
- Run foreground commands only, with no pgrep or sleep waiters.
- No push and no spawn.
- Do not edit packages/kernel/.
