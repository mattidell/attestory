# Charter: P0 of the sale family audit

Role: Builder. Source HEAD on milestone/sale-family-audit-2025.
Plan: docs/phases/engine-breadth/milestones/sale-family-audit.md (read it
whole). Precedent: the f8949-code-b milestone (plan, evidence directory,
retrospective), including its Track 0 neighbour probes and Decision 6
fixes. Do not read governance.

## Scope

1. **Field table.**
   - Cover every sale fact type on core v81: the covered, code W, code B,
     noncovered and no-1099-B sale objects and their scalar rows.
   - For each field, list the rules that read it, or "unread".
   - For each unread field, give the 2025 Form 1099-B / Form 8949 /
     Schedule D instruction text that says how it changes the return.
     Quote it with line references, from the PDFs whose checksums the
     earlier P0s recorded. If they are not local, fetch them from irs.gov
     into a temp directory outside the repo.
2. **Consumer table.**
   - For every family, list each consumer it reaches (Schedule D lines
     1a-10, 15, 16, 21, Form 1040 line 7a, the preferential base, both
     attachments, line 25b withholding), and each consumer it should reach
     but does not.
3. **Probes on core v81.**
   - Build one case through `live_coordinate_run`, with synthetic
     `demo.*` findings and honest answers, for each of these:
     - an unread field that changes the tax;
     - an unreached consumer;
     - the value edge cases in the plan.
   - Compute the right answer by hand.
   - Say whether v81 publishes a wrong return, blocks, or refuses by
     answer.
4. **Design.**
   - Give the smallest content fix for each defect: read the field,
     refuse by answer, or block with a true reason.
   - Prototype it on a scratch core v82 under
     sale-family-audit-evidence/. Load the harness under a unique module
     name.
   - Rerun every v81 return (the f8949-code-b fixture's cases) and count
     what changes.
   - Propose the committed audit test: it fails when a sale fact type
     gains a field that no rule reads and no answer refuses.

Stop and report if a fix needs an engine, schema, expression operation or
recording-surface change. Give the cause and the smallest change.

## Deliverables

In sale-family-audit-evidence/:
- audit.md: both tables, the probes with hand values, the design, and a
  recommendation;
- the probe and prototype scripts, and their small JSON outputs.

Fill the plan's "P0 result" section. No production, test or content edits.

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
