# P0: a question for each yes/no scope answer and filing status

Role: Builder. Source HEAD on milestone/scope-answer-questions-2025.
Plan: docs/phases/engine-breadth/milestones/scope-answer-questions.md.
Read the plan, the missing-input-questions plan and its evidence
(missing-input-questions-evidence/p0-survey-and-design.md and
probe-output.json for the list of 79 roots), and the eight existing
input-question citizens. Do not read governance or unrelated proposals.

Assigned evidence only:
docs/phases/engine-breadth/milestones/scope-answer-questions-evidence/
(p0-questions.md, probe.py, probe-output.json).

1. List the 79 yes/no roots and filing status from the survey, confirmed on
   core v72 (each still blocks a line when withheld; record the lines).
2. For each: the fact-type title, the recorded values, what each value does
   in the rules that read it (trace the content), and the condition under
   which it is asked.
3. Draft one question per fact, in the filer's words, matching the eight
   existing ones' style. State, for each, which value a "yes" and a "no"
   records, and confirm the natural reading matches. Where the fact asserts
   an absence, phrase the question so "yes" means the thing is present only
   if the recorded value agrees; otherwise say plainly what each answer
   means. Group repeated patterns (for example the 23 direct-FTC scope
   answers) and flag any you cannot phrase without misleading.
4. Filing status: how the projection could reach a declared question from
   the binding symbol, and the smallest change. Draft its question.
5. Verify on a scratch v73 (outside the repo) that each citizen attaches
   under its lines and that v72 renders unchanged.

No production, test, content or schema edits. Stop if any fact needs a
schema or engine change, and report. Synthetic demo.* only; no absolute
paths in committed files. Commit evidence with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir) every
time; never --no-verify; never bare git stash. Foreground commands only. No
push or spawn. Report the table, flags and limitations.
