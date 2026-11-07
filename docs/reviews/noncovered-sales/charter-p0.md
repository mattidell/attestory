# Charter: P0 of noncovered sales

Role: Builder. Source HEAD on milestone/noncovered-sales-2025.
Plan: docs/phases/engine-breadth/milestones/noncovered-sales.md (read it
whole). Do not read governance.

## Scope

1. **Law.** From the local 2025 Form 8949 and Schedule D instruction
   sources the package citations name (find them under `temp/` or the
   citation corpus; say if a source is not local): what boxes B and E
   (and C and F) require, which Schedule D lines they feed,
   how a filer-supplied basis and a wash-sale adjustment are reported,
   and what the 1099-B box 12 and box 1e fields mean. Quote with line
   references.
2. **State on core v78.** Through `live_coordinate_run` with synthetic
   `demo.*` findings, the plan's cases: what each publishes, blocks or
   refuses, and which answer refuses it. The hand-computed right answer
   for each.
3. **What exists.** Read `coverage-frontier.md` row "Noncovered /
   basis-not-reported Form 8949 transactions", ADR-0061 Decision 4,
   ADR-0066, and ADRs 0067-0071 (digests in `docs/adr/INDEX.md`; full
   text only where you act on it). What the covered families, Form 8949
   attachment v2 and Schedule D rules already carry; whether a
   filer-supplied basis fits an existing fact type or needs a new one;
   what the C3 closure-gate question is and whether it is still open.
4. **Design.** The smallest successor set: families, fact types,
   questions, rules, attachment rows, boundary answer. Prototype it in a
   scratch copy under the evidence directory (never under
   packages/content) and run the cases on it. Count what changes for
   returns v78 computes, fixtures and goldens.

Stop and report if the class needs an engine, schema, expression
operation or recording-surface change; give the cause and the smallest
change.

## Deliverables

docs/phases/engine-breadth/milestones/noncovered-sales-evidence/:
p0-law-state-design.md (law with quotes, cases table, what exists,
design, and a one-paragraph recommendation), the probe script and its
JSON output, the prototype and its output. Fill the plan's "P0 result"
section (a short summary that links the evidence). No production, test
or content edits. Keep committed output small: no copies of the content
tree.

## Rules

Synthetic demo.* only; no absolute paths in committed files. Commit
incrementally with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
retry every 10 s up to 5 min if held); never --no-verify; never bare git
stash. Foreground commands only; no pgrep or sleep waiters. No push or
spawn. Do not edit packages/kernel/.
