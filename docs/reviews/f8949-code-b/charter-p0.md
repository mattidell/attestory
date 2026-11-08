# Charter: P0 of broker basis corrections

Role: Builder. Source HEAD on milestone/f8949-code-b-2025.
Plan: docs/phases/engine-breadth/milestones/f8949-code-b.md (read it
whole). Build on the precedent of the f8949-boxes-cf milestone: its plan,
its evidence directory (cf_prototype.py, track0.py) and its retrospective
docs/milestone-retrospectives/2026-11-07-f8949-boxes-cf.md. Also read
ADR 0084 and ADR-0061. Do not read governance.

## Scope

1. **Law.** Use the 2025 Form 8949 and Schedule D instructions. The
   f8949-boxes-cf P0 recorded their checksums. If the PDFs are not on
   this machine, fetch them from irs.gov into a temp directory outside
   the repo and record the checksums. Answer, with line-referenced
   quotes:
   - what code B requires;
   - which box a covered sale with a wrong reported basis uses;
   - what goes in columns (e) and (g);
   - how B combines with W on one row;
   - whether code B applies to boxes B, C, E and F.
2. **State on core v80.** Run the plan's cases through
   `live_coordinate_run` with synthetic `demo.*` findings. For each, say
   what it publishes, blocks or refuses, and which answer refuses it.
   Compute every Schedule D line and Form 1040 lines 7a, 15 and 16 by
   hand for each case.
3. **Design.** The smallest successor set, following the v80 pattern:
   - how the corrected basis is supplied, and how it pairs with its sale;
   - the column (g) arithmetic;
   - the in-class answer change. Check its words against its proposition;
   - lines 1b, 2, 8b and 9, and the attachments.

   Prototype it on a scratch copy under the evidence directory
   f8949-code-b-evidence/, never under packages/content. Load harness
   modules under unique names. Run the cases, asserting every attachment
   disposition and each blocked line's reason, and its row's
   (disposition, code, missing). Count what changes for returns v80
   computes.

Stop and report if the class needs an engine, schema, expression
operation or recording-surface change. Give the cause and the smallest
change.

## Deliverables

In docs/phases/engine-breadth/milestones/f8949-code-b-evidence/:
- p0-law-state-design.md: the law with quotes, the cases table with hand
  values, the design, and a one-paragraph recommendation;
- the probe script and its JSON output;
- the prototype and its output.

Also fill the plan's "P0 result" section with a short summary that links
the evidence. No production, test or content edits. Keep committed output
small, with no copies of the content tree.

## Rules

- Synthetic demo.* only, and no absolute paths in committed files. The
  envelope gate also rejects temp-directory paths in prose.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir).
  If the lock is held, retry every 10 s for up to 5 min.
- Never use --no-verify or a bare git stash.
- Run foreground commands only.
- No push and no spawn.
- Do not edit packages/kernel/.
