# Retrospective — Student Loan Deduction Completion

## What differed from the plan

The plan began as eight plain sentences and expected six build tracks. The
result keeps all eight sentences but needed far more engine work than the
plan foresaw. The route map showed that the recorded links alone could not
replace the tax-labelled answer. The owner chose two ordinary questions in its
place. The closure checks then found three engine capabilities missing: a
count that follows a shared key, a same-run read of per-statement results, and
presence selection beyond Form 1040 line 2b. Owner review added two more
contracts: a declared basis for a favorable result, and write-side refusal of
an unscoped statement rewrite. All five became ADR 0077.

Track 0 took eight units instead of one. Track 2's fail-open fix moved into
the worksheet integration, because presence selection needs both paths. The
favorable result was renamed from `qualified` to `plain-case-supported`,
because its basis includes five assumptions and four conditions left with the
person.

## What it cost

Thirty-odd builder units across Grok and then Opus 5.5 sub-agents, several
usage-limit interruptions, and five owner reviews that each found a real
defect the Foreman had passed. The costliest pattern was declaring a
mechanism closed because each part looked right on its own. The owner caught
four instances: counting remaining affirmatives after the recorder had removed
the uncertain ones; an evidence reference treated as authority for any update;
two ADR parts that did not compose into one runnable rule; and an omitted link
that selected a path but never reached its own statement's decision. Track 7's
readiness check found three interrupted saves that had recovered to a more
favorable deduction. None had been suspected.

Running two builders in one worktree worked when files were assigned
explicitly. Resuming a builder's own session after an interruption kept its
context and was cheaper than starting fresh.

The final repair handoff retained the prior agent's enrollment invalidation
and history-required replay changes. Testing a removed statement beside a
supported one exposed another instance of the omission problem: checking only
current statements lost the unresolved inclusion of the removed statement.
The repair checks those markers directly using existing declared-result reads.
An answer must still concern the circumstances now linked, a run must use the
history needed to establish applicability, and removed subjects must not make
unresolved relationships disappear from either calculation or explanation.

## Follow-ups

- **Torn log line.** `ActLog.append` writes onto a torn last line and corrupts
  the log. This predates the milestone and affects every workspace. Decide
  whether to refuse the write or set the torn line aside.
- **Runner disagreement.** An optional default on a symbol that a per-subject
  rule also publishes stops the reference runner running that rule. Fix in
  `packages/derivation/`.
- **Entrypoint pin check.** Packages on `artifact-package.v32`–`v34` skip the
  exact entrypoint-pin check. Enabling it could reject published packages.
- **Older workspaces.** A v1-era history that holds a no, cannot-tell or
  withdrawal is refused rather than upgraded to relationship bundle v2.
- **Atomic saves.** These assume one writer per workspace. A crash can leave
  an `acts.jsonl.pending` file until the next save.
- **Trace the person's "no".** When a statement link is corrected to "no",
  the blocked line 21 traces to the statement but not to the saved "no". The
  sentence is right; pinning the denial needs new rule versions.
- **Line 21 page wording.** A blocked line with reasons still shows the code
  line "Missing dependency code(s): DEPENDENCY_INVALID". Reader wording
  remains unaccepted.
- **Lump-sum election page error.** Line 6c shows "missing its rendering
  instruction" for a `not_elected` value. It reproduces on `main`.
- **Worksheet v3 note.** Its published `notes` say "Successor to v2"; v2 was
  superseded before publication and appears in no registry. Published bytes
  stay as they are.
- **Next scope.** Person-supplied scoped values, mixed periods (ADR 0076
  Part 3) and the explanation of a return line remain parked.

## What should change in the next plan

Before calling a design closed, run one artifact that uses every part
together, and include the mixed case: one usable input beside one removed,
uncertain or unbound input. Check what an upstream step removed before
counting what remains. Bind authorizing evidence to the exact change it
authorizes. Name the basis of a favorable result before naming the result.
Give each builder a readiness table of what an interruption leaves, before
any code.
