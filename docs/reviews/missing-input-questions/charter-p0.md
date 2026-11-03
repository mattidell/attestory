# P0: what a line blocked on a missing input tells the person

Role: Builder. Source HEAD on milestone/missing-input-questions-2025.
Plan: docs/phases/engine-breadth/milestones/missing-input-questions.md.
Read the plan, the closure-questions plan and retrospective, and
`_closure_question_reasons` and its call site in
packages/derivation/presentation_projection.py. Do not read governance or
unrelated proposals.

Assigned evidence only:
docs/phases/engine-breadth/milestones/missing-input-questions-evidence/
(p0-survey-and-design.md, probe.py, probe-output.json).

1. On core v71, through the real coordinator and presentation projection,
   build returns that withhold one filer-answerable input at a time (W-2
   box 2, Form 1099 box 4, SSA-1099 box 6, and the other inputs the
   current-core builders record). For each blocked line record the root
   codes and `missing` ids and the text the page shows.
2. Classify each root: filer-answerable fact, unconfirmed family, or derived
   (invalid value, fault, guard). Count lines and distinct roots.
3. For each answerable fact, find any existing declared, filer-facing wording
   (fact-type, ordinary-question, recorder or presentation content) that
   could be copied verbatim. Say where it lives and whether it is published
   in the v71 package. Do not compose new wording.
4. Design the smallest change: where a missing-input question is declared,
   how the projection reaches it (including the mixed case), and what v70
   and earlier render (must be byte-identical). Give citizen and schema
   counts and the alternatives.
5. Hand-written expectations for every case in the plan.

No production, test, content or schema edits. Stop if the design needs a
kernel or engine change beyond the presentation projection, and report.
Synthetic demo.* data only; no absolute paths. Commit evidence increments
with explicit paths under `$(git rev-parse --git-dir)/collaboration-commit.lock`
(mkdir … rmdir); never --no-verify; never bare git stash. Run commands in the
foreground. No push or spawn. Report the outcome and limitations.
