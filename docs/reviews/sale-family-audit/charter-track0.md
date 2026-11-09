# Charter: Track 0 adversarial closure of the sale family audit

Role: Builder. Source HEAD on milestone/sale-family-audit-2025.
Plan: docs/phases/engine-breadth/milestones/sale-family-audit.md (read it
whole, including the P0 result and Decisions). Evidence:
sale-family-audit-evidence/ (audit.md, probe.py, prototype.py, tables.py,
rerun_v81.py). Gate: `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure
Gate" (read that section and its closing paragraphs whole). Precedent:
f8949-code-b-evidence/track0-closure.md. Do not read governance.

## Scope

Over the decided fixes (Decisions 1-5), produce the gate's six artifacts.
Build the evidence through `live_coordinate_run` on the scratch v82, in
both the honest and base answer modes. Never work under packages/content.

1. **Authority-lifecycle table.** Cover every fact the fixes read: the sale
   counts, `long_term`, box 1g on direct sales, row-to-sale pairing, the
   box 4 and box 7 answers, and the Exception 1 facts. Give what
   invalidates each.
2. **Empty/nonempty matrix.** Cover each family with the counts and with
   the new answers. Include the Exception 1 answers in both polarities.
3. **Late-member trace.**
   - A wage return computes; add a box E sale; recompute through the
     Schedule D route (D1).
   - A box 4 "no" followed by a sale that has box 4 withholding.
4. **Claim reuse.** Cover line 16's Exception 1 path, the preferential
   base, and line 25b. Give the three-part proof, or show that none is
   reused.
5. **Neighbor dependency diff.** All 213 v81 returns, before and after.
   Classify every change under Decisions 1-5. Anything unclassified is a
   counterexample.
6. **Integration surface.** Cover every consumer of line 16, lines 24, 33,
   34 and 37, line 25b, line 7a, the preferential base and both
   attachments, with cardinality. Pin each blocked line's reason and its
   (disposition, code, missing). Include a presentation probe of each new
   or changed field and question.

Then write the closing declaration under the plan's "Track 0 adversarial
closure" heading. A row is PASS only if no counterexample stands beside
it. Make repairs as switchable changes to the scratch prototype. Where a
fix cannot pass without an engine, schema or recording change, mark it
FAIL and stop.

## Deliverables

- sale-family-audit-evidence/track0-closure.md.
- A harness with a unique module name that mutates no other module's
  globals, and its small output.
- The plan's "Track 0 adversarial closure" section.

No production, test or content edits.

## Rules

- Synthetic demo.* only, and no absolute or temp-directory paths in
  committed files.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir).
- Never use --no-verify or a bare git stash.
- Run foreground commands only.
- No push and no spawn.
- Do not edit packages/kernel/.
