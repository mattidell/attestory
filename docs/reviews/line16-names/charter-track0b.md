# Charter: Track 0b — line 16 and the preferential base name the failing Exception 1 criteria

Role: Builder. Source HEAD on milestone/line16-names-2025.
Plan: docs/phases/engine-breadth/milestones/line16-names.md, read whole,
especially "Track 0 disposition" (Decisions 6-9), which replaces
Decision 1. Evidence: line16-names-evidence/ (p0.md, track0-closure.md,
prototype.py, track0.py, classify.py and outputs). Do not read
governance. Do not edit packages/ or tests/.

## Scope

1. **Redesign.** Build a new scratch successor on published v94:
   `rule.form1040-line16` v9 and `rule.selected-preferential-base` v12,
   both on rule-artifact v17. In the state "Schedule D required, no sale
   recorded, `no-form8949-sources` yes", each block declares exactly the
   Exception 1 criteria whose current answer fails the exception. Every
   other branch, value, requires and pin is unchanged from v8 and v11.
   Use the smallest admitted content shape (nested choose over the four
   criteria, helper rules, or another); say what it costs and why.
2. **Item 1 again.** Rerun Track 0 item 1 on the new content for the four
   targets and three neighbours, plus states with two, three and four
   failing criteria. PASS when every name shown is a failing criterion
   whose truthful correction moves or unblocks the line, and no failing
   criterion is left unnamed.
3. **Every field agrees.** On those states, quote the sentences on
   line 16, its four dependants and every field explained by the
   preferential base (the page model's own sentences, no punctuation
   filter). They name the same criteria; no field names a passing
   criterion or a sale or boundary question. FAIL a field with no
   actionable sentence.
4. **Nothing else moved.** Rerun Track 0 items 2 and 4 on the new
   content: boundary states (Decision 3), the personal-loss case and the
   other nine pinned cases (Decision 2), computing neighbours.
5. **Replay.** Full 775-list replay of v94 against the new successor
   with `python3 tools/recorded_replay.py` in parallel (CPU count minus
   one workers), part file outside the repo, strict classification
   (extend classify.py: only line 16 and preferential-base missing names
   and the matching sentences may change, in the target state). Report
   wall time.

Stop and report if the state-sensitive names need more than content (a
projection, page, schema or engine change), or if an admitted content
shape cannot express them.

## Deliverables

In line16-names-evidence/: the revised prototype, track0b.py,
track0b-*.json, track0b-closure.md (tables, PASS/FAIL per item,
recommendation). Add a "Track 0b" section to the plan. No production,
test or content edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Load sibling harnesses by path under a unique name.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Write your JSON report before your final checks, and update it when
  they finish.
- Never --no-verify or a bare git stash. Foreground commands only; no
  background jobs left running.
- No push and no spawn. Do not edit packages/ or tests/.
