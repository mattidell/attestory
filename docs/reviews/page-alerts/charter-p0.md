# Charter: P0 of saved pages without alerts on line 6c and Schedule 1

Role: Builder. Source HEAD on milestone/page-alerts-2025.
Plan: docs/phases/engine-breadth/milestones/page-alerts.md (read it
whole). Precedent: line12d-boxes-evidence/ (p0.md, its probe and browser
check, track0 files), sale-page-observation-evidence/, and
box4-amount-asked-evidence/p0.md. Do not read governance.

## Scope

1. **Reproduce first.** On published core v91, run the plan's cases as
   synthetic `demo.*` act lists through the real coordinator, the
   presentation projection and the saved citation-walk page, and open
   each saved page in headless Chrome as the line12d-boxes evidence did.
   List every safe-render alert the drawn page shows: field, the value
   or missing part that caused it, and the exact alert text. Read the
   page model's own values and the drawn DOM; do not classify by
   punctuation or by a filtered list. If neither parked alert
   reproduces, stop and report.
2. **Census.** Over the recorded lists, count alerts per field from the
   presentation model (no browser needed once item 1 shows the model
   value that produces each alert). Report any alert on a computing
   return beyond the two parked ones.
3. **Trace.** For each alert, name the content member that supplies the
   value or omits the citation and the page code that refuses to draw
   it. Cite file:line.
4. **Design.** The smallest repair for each alert. Prefer content
   successors (a field or rule successor whose value the page already
   draws; a citation on the top-entry field). For line 6c, say what the
   page would show in each state and whether those words are true:
   "not checked" is only right if the form has a box there. Compare with
   a page change and say what each costs. Prototype the preferred design
   as scratch core v92 on published v91, loaded from published content,
   never by editing packages/, and show the drawn pages without the
   alerts.
5. **Rerun.** Replay the recorded lists with
   `python3 tools/recorded_replay.py` on v91 and scratch v92, in parallel
   (CPU count minus one workers). Keep the part file so Track 0 can
   reuse the replay. Classify every change; the target is no number
   changed and no return newly asked a question. Report wall time.

Stop and report if the design needs an engine, schema, projection, page
or kernel change; name the smallest one. A projection or page change
overlaps another foreman's open milestone (blocked-sale-pages) and is
the foreman's decision.

## Deliverables

In docs/phases/engine-breadth/milestones/page-alerts-evidence/: p0.md
(reproduction table, census, trace, design comparison, drawn-page
results, rerun classification, recommendation, decisions for the
foreman), the scripts and their small JSON outputs. Fill the "P0 result"
section in the plan. No production, test or content edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Never --no-verify or a bare git stash. Foreground commands only.
- No push and no spawn. Do not edit packages/.
