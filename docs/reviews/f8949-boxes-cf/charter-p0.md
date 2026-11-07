# Charter: P0 of sales without a Form 1099-B

Role: Builder. Source HEAD on milestone/f8949-boxes-cf-2025.
Plan: docs/phases/engine-breadth/milestones/f8949-boxes-cf.md (read it
whole). Precedent to build on: the noncovered-sales milestone (plan
docs/phases/engine-breadth/milestones/noncovered-sales.md and its evidence
directory, ADR 0084, retrospective
docs/milestone-retrospectives/2026-11-06-noncovered-sales.md). Do not read
governance.

## Scope

1. **Law.** From the local 2025 Form 8949 and Schedule D instruction
   sources the package citations name (find them under `temp/` or the
   citation corpus; say if a source is not local): what boxes C and F
   require, which Schedule D lines they feed (3 and 10), how a
   filer-supplied proceeds and basis and a code W adjustment are reported.
   Quote with line references.
2. **State on core v79.** Through `live_coordinate_run` with synthetic
   `demo.*` findings, the plan's cases: what each publishes, blocks or
   refuses, and which answer refuses it. Compute the right answer for the
   gain, loss, wash and mixed cases by hand (every Schedule D line, Form
   1040 lines 7a, 15, 16).
3. **Design.** The smallest successor set following the v79 noncovered
   pattern: families, fact types, the closure question shape (extend the
   v79 grouped question, or a second v4 mapping — compare what the filer
   sees and what each does to a v79 workspace that already answered), rules
   (Schedule D lines 3 and 10, lines 7 and 15, line 7a, preferential base),
   Form 8949 and Schedule D attachment successors, boundary answer. Prototype
   it on a scratch copy under the evidence directory (never under
   packages/content) and run the cases, asserting every attachment
   disposition. Count what changes for returns v79 computes.

Stop and report if the class needs an engine, schema, expression operation
or recording-surface change; give the cause and the smallest change.

## Deliverables

docs/phases/engine-breadth/milestones/f8949-boxes-cf-evidence/:
p0-law-state-design.md (law with quotes, cases table with hand values,
design, one-paragraph recommendation), the probe script and its JSON
output, the prototype and its output. Fill the plan's "P0 result" section
(a short summary that links the evidence). No production, test or content
edits. Keep committed output small: no copies of the content tree.

## Rules

Synthetic demo.* only; no absolute paths in committed files. Commit
incrementally with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
retry every 10 s up to 5 min if held); never --no-verify; never bare git
stash. Foreground commands only; no pgrep or sleep waiters. No push or
spawn. Do not edit packages/kernel/.
