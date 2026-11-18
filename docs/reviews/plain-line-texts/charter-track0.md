# Charter: Track 0 adversarial closure — every line speaking plainly

Role: Builder (adversarial closure), fresh context. Source HEAD on
milestone/plain-line-texts-2025. Plan:
docs/phases/engine-breadth/milestones/plain-line-texts.md (read it whole;
Decisions 1-8 govern). Evidence: plain-line-texts-evidence/ (p0b.md,
p0c.md, p0c-wording.json, the P0c scripts). Do not read governance. You
did not write this wording; test it, do not defend it.

## Items

1. **True in every drawn state.** For each of the 57 replacements, find
   every state in which the page draws it (from the census and the
   rule's branches that select that disposition), and check the new
   sentence is true in each, including single, joint and separate
   statuses, a spouse's records, a zero reached by rounding, a zero
   reached by absence, and a corrected or retracted answer. Build
   synthetic `demo.*` act lists for any drawn state the 775 lists do not
   reach. A sentence that claims a record, answer or form the state does
   not have fails.
2. **Nothing proved is dropped.** For each, say what the old sentence
   told the filer about the basis of the value (absence, completeness,
   a calculation, a closure) and confirm the new one still says it in
   plain words. Losing the basis fails.
3. **Plain and consistent.** Flag any remaining engine term from the
   census term list, and any name that differs from the 2025
   instructions' own name for the line or form. Check that sibling lines
   (for example lines 2a/2b, 3a/3b, 25a-25c) use the same pattern.
4. **Drawn page.** Draw the scratch v96 saved page in Chrome for at
   least a wage-only, an interest and dividends, a sale and a mortgage
   case, and confirm each new text appears where expected with no
   render alert, and attachment headings show the plain part.
5. **Replay reuse.** Re-run the strict classifier on P0c's part files
   with the content bytes confirmed unchanged; no new live replay unless
   content changes. If you change any wording, rebuild the scratch
   successor and re-run the strict replay and mutation controls.

Fix wording failures in the scratch manifest and record each change
with its reason. Stop and report if a fix needs anything beyond a
content successor and the Decision 5 validator entry.

## Deliverables

track0.md in the evidence directory (item verdicts, a table of every
replacement with verdict, changes made), scripts and small JSON outputs.
Append a "Track 0 adversarial closure" section to the plan. No
production, test or content edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- An evidence script that imports a sibling harness by bare name loads it
  by path under a unique name instead.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only.
- No push and no spawn. Do not edit packages/.
