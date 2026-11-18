# Charter: P0 of every line speaking plainly

Role: Builder. Source HEAD on milestone/plain-line-texts-2025.
Plan: docs/phases/engine-breadth/milestones/plain-line-texts.md (read it
whole). Precedent: line16-names-evidence/ (classify.py, the replay and
probe scripts), page-alerts and line6b-reason evidence for the page
model and saved-page harnesses. Do not read governance.

## Scope

1. **Census first.** On published core v95, collect every sentence a
   filer can see on the saved page: each field's plain/explain text,
   blocked reason, categorical render text, question sentence and any
   other page-model string. Use the real live coordinate run and the
   presentation projection over the 775 recorded lists (reuse a recorded
   replay part file if one serves; otherwise run in parallel shards,
   CPU count minus one) and the plan's synthetic cases. Read the page
   model's own strings. Flag each sentence that carries an engine term:
   at least "derived finding", "finding", "closed-empty", "closed with
   members", "authority", "authorizes", "subtotal 0", "publishes",
   "honest", "family", "citizen", ids or version strings; extend the
   list from what you find, and record the full term list. If no
   filer-visible sentence carries one, stop and report.
2. **Trace.** For each flagged sentence, name the content file, version
   and field that supplies it, and which page fields show it, on how
   many lists. Cite file:line. Separate texts no page draws.
3. **Design.** The smallest repair. Prefer content successors of the
   citizens that carry the sentences, with plain wording checked against
   the 2025 Form 1040 instructions and the relevant schedule in the
   local sources. Never change which answer a path needs, a refusal
   code, a value, a requires, a pin or a `missing` name. If many
   citizens are touched, say how to group them and what one package
   costs. Prototype as a scratch core successor on published v95, loaded
   from published content, never by editing packages/.
4. **Rerun.** Replay the recorded lists on v95 and the scratch successor
   in parallel, keep the part file outside the repo so Track 0 reuses
   it, and classify every change strictly: compare every row (including
   added or removed rows) and fail any changed value, disposition,
   refusal code or missing name before giving a change an expected
   label. Include mutation controls. Expected: only the replaced
   sentences change. Report wall time.

Stop and report if the design needs an engine, schema, projection, page
or kernel change; name the smallest one. A projection or page change
overlaps another foreman's open milestone (blocked-sale-pages).

## Deliverables

In docs/phases/engine-breadth/milestones/plain-line-texts-evidence/:
p0.md (term list, census table, trace, design comparison, prototype
results, rerun classification, recommendation, decisions for the
foreman), the scripts and their small JSON outputs. Fill the "P0 result"
section in the plan. No production, test or content edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- An evidence script that imports a sibling harness by bare name loads it
  by path under a unique name instead.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Write your JSON report before your final checks, so a usage limit
  does not lose it; update it when the checks finish.
- Never --no-verify or a bare git stash. Foreground commands only; do not
  leave background jobs running when you finish.
- No push and no spawn. Do not edit packages/.
