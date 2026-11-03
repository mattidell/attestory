# P0: a statement recorded without its withholding answer

Role: Builder. Source HEAD on milestone/statement-withholding-answer-2025.
Plan: docs/phases/engine-breadth/milestones/statement-withholding-answer.md.
Orient with this charter. Read the plan, the withholding-closure and
refund-or-amount-owed retrospectives, line 25a and 25b in core v70, and the
recorders for Forms 1099-INT, 1099-DIV, 1099-R, 1099-G and SSA-1099. Do not
read governance or unrelated proposals.

Assigned evidence only:
docs/phases/engine-breadth/milestones/statement-withholding-answer-evidence/
(p0-trace-and-design.md, probe.py, probe-output.json).

1. Reproduce on v70 through `live_coordinate_run` (or
   `tests/helpers/current_core_returns.py`): for each of the five families, a
   statement recorded without its box 4 (box 6) answer, the family's closure
   attested true. Show what line 25b and the bottom line publish, and the
   same return with $0 answered.
2. Trace the Form W-2 box 2 check on line 25a: the citizens, the `count`
   comparison, what it names when it blocks, and how a $0 answer is recorded
   and told apart from absence.
3. Trace how each 1099 statement and its withholding are recorded: one act
   or several, which fact carries the statement, whether a $0 box 4 can be
   recorded today, and what the companion declarations require.
4. Design the smallest successor set that blocks line 25b while any
   statement lacks its answer, leaving answered returns byte-identical.
   Give citizen counts, the blocked reason and what it names, and the
   alternatives considered.
5. Measure the cost: which committed fixtures, goldens, sample workspaces
   and tests on v70 carry a 1099 statement without its withholding answer,
   and what an existing return is asked when adopted onto v71.
6. Hand-computed expectations for every case in the plan.

No production, test, content or schema edits. Stop if the fix needs a
kernel, schema, expression-operation or engine change, and report what and
why. Synthetic demo.* data only; no absolute paths in committed files.
Commit evidence increments with explicit paths under the commit lock
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
never --no-verify. No push or spawn. Report the outcome and its limitations
for the foreman's decisions.
