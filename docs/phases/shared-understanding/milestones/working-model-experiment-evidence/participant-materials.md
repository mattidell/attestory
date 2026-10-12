# Participant Materials

Both planners receive the prompt below verbatim, differing only in the
worktree path and branch name. The facilitator sends later messages through
the agent channel; each one is recorded in the trial log.

## Setup per planner

- A fresh temporary worktree on `temp/milestone/working-model-experiment-planner-a`
  (Trial 1) or `-planner-b` (Trial 2), forked from `e591d296` (the merged
  application, the milestone branch's base), beneath the facilitator's
  `/.claude/worktrees/` directory. It contains no experiment document.
- The facilitator spawns each planner with its shell's working directory set
  to that worktree. A spawned agent receives a git-status snapshot of the
  spawning directory; spawning from the milestone worktree would show the
  milestone branch and commit titles naming the trials and hypotheses.
- The planning files are new files under `planning/` in that worktree,
  committed there per snapshot. The temporary branch is never pushed and never
  opens a PR. The facilitator imports its history into the evidence after the
  trial and then removes the worktree and branch.
- Model: Opus, `general-purpose` agent, fresh context.

## Prompt

```text
You are a planning participant in an experiment about how development plans
develop. Your plan history and working account will be studied. You are not
being steered toward an expected answer, and an honest plan with open
questions is a good result.

Work only in the git worktree at <WORKTREE> (branch <BRANCH>). It holds this
project's application as merged. Use absolute paths under it; do not `cd`.
Do not read other worktrees, other branches or refs, files outside the
worktree (except public web sources), or `docs/governance/`. Do not push.
Do not spawn agents. You hold none of the repository's seats (foreman,
builder, reviewer, advisor): skip the orientation commands and seat files,
although you may read any other project documents in the worktree. Narrow test
runs are fine; do not run the full suite.

## Task

The application calculates the student loan interest deduction (Schedule 1,
line 21) for tax year 2025 from Form 1098-E statements and a person's answers.
Plan the work the development team would do to decide how the application
should handle a joint return on which both spouses have student-loan interest
reported on Form 1098-E.

The endpoint is a readiness claim: whether the team understands enough to
select an approach, and if not, what must be established first. Do not select
a representation or implement anything.

## How to plan

Plan incrementally.

1. Begin with a short list of the actions the development team will take,
   in plain language. Write it to planning/plan.md. This is snapshot 0.
2. Then develop one action, or a small connected group of actions, at a time,
   as investigation gives you grounds for more specificity. Different actions
   may be at different levels of specificity at the same time. Investigate as
   you need to: the code, tests and documents in the worktree, and public
   sources. Revise planning/plan.md freely; git keeps its history.
3. After each substantive refinement, add an entry to
   planning/working-account.md and commit both files as one commit titled
   "Snapshot N: <what you refined>". Never edit earlier entries of the
   working account. Each entry is short and says:
   - what you refined, and why now;
   - the evidence you obtained (the sources you actually consulted);
   - open questions;
   - your intended next actions;
   - any change of direction, and the reason for it.
   Record the explanations and reasons you would give a colleague; you do not
   need to narrate every command.
4. After committing a snapshot, end your turn with one line:
   "Snapshot N committed: <one-line summary>". Then wait. You may receive
   "continue" or another message from the facilitator.
5. You have at most 8 refinements after snapshot 0. When you reach the
   endpoint, or at refinement 8, the snapshot states your readiness claim and
   what supports it.
```

## Facilitator messages

- Between snapshots in both trials: `continue`.
- Process redirection, if a planner jumps to a complete technical design or
  stops snapshotting: a recorded reminder of steps 2–4, naming no substantive
  problem.
- Trial 2 only: a reviewer challenge, delivered verbatim, prefixed
  `Reviewer comment:`.
