# Participant Materials

Frozen at design revision 3 (2026-10-12). Both planners receive the prompt
below verbatim, differing only in the workspace path. Later facilitator
messages are recorded in the trial log. The earlier draft is in git history.

## Setup per planner

- A fresh standalone clone of `e591d296` at
  `<temporary directory>/workspace-<random>`: one branch `main`, no remote,
  no tags, no stash, no milestone object. It contains no experiment document.
- A headless Claude Code session started in the clone:

  ```sh
  env -u ANTHROPIC_API_KEY claude -p --model opus \
    --setting-sources project --strict-mcp-config \
    --permission-mode bypassPermissions \
    --disallowedTools Agent SendMessage ListAgents TaskStop \
    --output-format json "<prompt>"
  ```

  Each later facilitator message resumes it with `--resume <session-id>`.
  (`ANTHROPIC_API_KEY` is unset so the session uses the owner's Claude login;
  the environment's key had no credit.)
- The planning files are new files under `planning/` in the clone, committed
  there per snapshot. The facilitator imports the history after the trial and
  then removes the clone.

## Prompt

```text
You are a planning participant in an experiment about how development plans
develop. Your plan history and working account will be studied. You are not
being steered toward an expected answer.

Work only in the git repository at <WORKSPACE>. It holds this project's
application as merged. Use absolute paths under it; do not `cd`. Put any
scratch files in <WORKSPACE>/temp/, which git ignores. Do not read files
outside the workspace (public web sources are fine) or `docs/governance/`.
Do not push. You hold none of the repository's seats (foreman, builder,
reviewer, advisor): skip the orientation commands and seat files, although
you may read any other project documents in the workspace. Narrow test runs
are fine; do not run the full suite.

## Task

The application calculates the student loan interest deduction (Schedule 1,
line 21) for tax year 2025 from Form 1098-E statements and a person's answers.
Plan the work the development team would do to decide how the application
should handle a joint return on which both spouses have student-loan interest
reported on Form 1098-E.

The endpoint is a readiness claim: whether the team understands enough to
select an approach, with what supports that claim, or what must be
established first. Do not select a representation or implement anything.

## How to plan

Plan incrementally.

1. Begin with a short list of the actions the development team will take,
   in plain language. Write it to planning/plan.md. This is snapshot 0.
2. Then develop one action, or a small connected group of actions, at a time,
   as investigation gives you grounds for more specificity. Different actions
   may be at different levels of specificity at the same time. Investigate as
   you need to: the code, tests and documents in the workspace, and public
   sources. Revise planning/plan.md freely; git keeps its history.
3. Take a snapshot after developing one action or connected group, before
   starting another. To take a snapshot, add an entry to
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
- Process redirection, if a planner jumps to a complete technical design,
  takes several snapshots in one turn or stops snapshotting: a recorded
  reminder of steps 2–4, naming no substantive problem.
- Trial 2 only: a reviewer challenge, delivered verbatim, prefixed
  `Reviewer comment:`.
