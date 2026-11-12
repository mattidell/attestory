# Charter: Track 0 adversarial closure of age and blindness asked

Role: Builder. Source HEAD on milestone/age-blindness-asked-2025.
Plan: docs/phases/engine-breadth/milestones/age-blindness-asked.md (read it
whole, including the P0 result and Decisions 1-8). Evidence:
age-blindness-asked-evidence/ (start with p0.md). Gate: `PROJECT_PLANNING.md`,
"Track 0 Adversarial Closure Gate" (read that section and its closing
paragraphs whole). Precedent: question-wording-evidence/track0-closure.md
and its track0.py. Do not read governance.

## Scope

Every claim must come from a `live_coordinate_run` output saved in a
committed JSON file and named by case id. Hand values come from the 2025
instructions (law.json), never from what the prototype publishes. A
question is tested by answering it as a truthful filer would read its
words, never by entering values by hand. Never work under
packages/content. Load evidence files only through tests/evidence_loader.py
patterns where a test does; scripts under the evidence directory may import
each other by unique module names.

0. **Rebuild.** Make scratch v88 match Decisions 1-4 on the final
   question-wording v87 (now published on this branch): the vocabulary
   bundle v4 retitles the two spouse facts with the separate-return
   condition. Rerun probe.py and rerun.py; commit their outputs.
1. **Authority-lifecycle table** for each of the four questions: who is
   asked, what answers it, which rule reads the answer, and what replaces
   it.
2. **Empty/nonempty matrix**: single, joint, separate (spouse with and
   without income), head of household, qualifying surviving spouse, and a
   dependent filer; each with the facts true, false and unanswered; born
   January 1 and January 2, 1961; the 2025 death cases (taxpayer and
   spouse, before and after the day before the 65th birthday).
3. **Late-member traces:** filing status changed after the spouse
   questions were answered (joint to separate, joint to head of
   household); an answer replaced.
4. **Claim reuse:** every rule that reads the four facts composes; only
   the bindings, the two decided rule successors, the questions and titles
   differ between v87 and v88.
5. **Neighbour dependency diff:** the 775 recorded lists P0 reran, plus
   joint, separate and dependent recorded returns (Decision 7), on live
   v87 and scratch v88, in a subprocess, answered false as the record
   implies. Classify every change.
6. **Integration surface:** a presentation probe of the exact text the
   filer sees for each question, on a page where it is asked, and that
   every newly blocked field names a question.

## Deliverable

age-blindness-asked-evidence/track0-closure.md and track0.py with its
`track0-*.json` outputs, and a "Track 0 adversarial closure" section in the
plan in the same shape as question-wording's: each table PASS or FAIL with
counts and case ids, and "Known limitations affecting correctness".

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Do not edit packages/kernel/, packages/derivation/ or packages/schemas/;
  stop and report if the design needs it.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
  if held, retry every 10 s up to 5 min.
- Never --no-verify or a bare git stash. Run foreground commands only. No
  push, no spawn.

## Amendment (Decision 9)

Same rules. Make scratch v88 match Decision 9: the spouse age and
blindness questions and the vocabulary v4 titles drop the separate-return
condition; one return-level fact and question, asked only on a separate
return, carry it (search the published content first and reuse an
existing fact only if its meaning is exactly that condition); worksheet
line 1 v2 reads it on a separate return. Then rerun item 0 and every
Track 0 table the change touches, at least: the separate rows of the
authority and matrix tables, all three late traces (`late_joint_to_separate`
must reach 15,750 without replacing the spouse-age answer, with the
condition answered truthfully), the reuse check, the surface for a
separate return, and the 778-list neighbour diff. Update
track0-closure.md and the plan's Track 0 section, including "Known
limitations affecting correctness".
