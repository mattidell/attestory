# Browser Evaluation Runner Repair Delta-Review Charter

Status: **current prompt after the repair Builder landed on
`track/browser-evaluation-runner-completion` (PR #71).** This is the one
focused delta review permitted by the milestone plan.

## Context Capsule

- **Source ref:** `track/browser-evaluation-runner-completion`; resolve and
  record its commit when this prompt is used to launch the role.
- **Exact object:** the focused repair relative to the pre-repair Track 1
  implementation commit named by subject
  `implement Track 1 instrumented harness core and fail-closed lifecycle`,
  ending at the branch commit named
  `repair browser evaluation runner integrity`,
  limited to `tools/presentation_harness/**` and the repaired Track 1 README
  sections. Reconcile it against the six blockers in
  `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-24-presentation-economy-t1-harness-core-review.md`.
  Foreman continuity and charter/review records are outside the
  artifact-quality object.
- **Role:** the original Reviewer resumed along its own review lineage when
  available; otherwise one fresh independent delta Reviewer. High tier /
  medium effort, technical-adversary lens.
- **Scope:** independently verify that the repair closes F1–F6 without
  weakening one-process batching, closed exit/reason semantics, network
  confinement, deterministic content-free reports, or Track 0-compatible
  observations. Complete the four original measurements transferred from the
  interrupted review.
- **Evidence-rung ceiling:** focused delta review of browser evaluation runner
  completion. Do not redesign contracts, implement another repair, add product
  checks/corpus work, run an economy or novelty experiment, or generalize into
  a browser framework.
- **Stop conditions:** stop if the source ref or repair object cannot be
  resolved, the completed review/repair charter is absent, Chrome is
  unavailable, the Reviewer has seen Builder working context, a check requires
  personal/machine-specific data or remote access, or the conclusion would
  exceed the Track 1 gate.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`;
  `docs/adr/INDEX.md`; the completed Track 1 review and repair charter; the
  repair diff and changed tests/examples/README; the Browser Evaluation Runner
  Completion plan's Contracts, Verification, Data safety, Review gate, and
  Track 1 sections; and the original review charter's seven measurement
  headings.

The completed review already records the historical seed and full
implementation context. Do not reload the exploratory corpus or re-derive the
review rig unless a repair change touches a settled technique and that exact
source is necessary.

Before reviewing, echo the resolved repair object, scope, evidence ceiling, and
stop conditions. Treat Builder claims and committed regression output as
inputs, not proof.

## Prior evidence credit — do not repeat

The independent review at
`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-24-presentation-economy-t1-harness-core-review.md`
already established the pre-repair baseline and substantial passing behavior.
It is the evidence for the six historical failures and for unchanged runner
ground. Do not check out the pre-repair commit merely to reproduce failures
that review already measured.

In particular, do not reconstruct the harness seed, reopen settled design
alternatives, reload the presentation exploratory corpus, or repeat the
original broad 42-turn technical review. Treat F1–F6 as known attack classes,
not findings to rediscover. Fresh reviewer effort goes to:

1. one independent repaired-outcome witness for each F1–F6 class;
2. the four measurements explicitly transferred by the prior review; and
3. only the adjacent invariants touched by the repair.

Use the committed focused battery first and batch live-browser measurements
where practical. Add an ad hoc probe only when a required delta measurement is
not already observable from that battery. Existing evidence for unrelated
runner behavior remains credited.

## Required delta measurements

1. **Mechanical repair battery:** independently run the committed focused Node
   and real-Chrome battery. Map its cases to F1–F6 and show the repaired
   outcomes in one compact result packet. Use the completed review as the
   pre-fix baseline; rerun the pre-repair commit only if a repaired result
   conflicts with that recorded baseline.
2. **Tuple isolation:** verify one Chrome process serves the invocation while
   consecutive tuples cannot observe each other's cookies or `localStorage`.
   Enumerate the live Chrome main process, browser contexts, and targets.
3. **Injection integrity:** exercise syntactically invalid, registered-but-not-
   executed, valid-executed, and intentional candidate-fault cases. Only
   harness injection failure may yield `injection-failed`/exit `2`.
4. **Lifecycle cleanup:** measure process/profile/context/target counts before
   and after normal completion, criterion failure, infrastructure error,
   launch-time `SIGINT`/`SIGTERM`, and post-launch `SIGINT`/`SIGTERM`.
5. **Path/provenance confinement:** attack `..`, absolute path, symlink escape,
   and repository-neighbor spellings. Confirm refusal occurs before Chrome and
   validate a captured normal observation through the public Track 0 dataset
   validator with a compatible synthetic workload.
6. **Strict validation:** attack every existing check's missing, unknown,
   wrong-type, and out-of-range parameters plus empty top-level selections and
   matrix. No vacuous pass is permitted.
7. **Output safety:** scan stdout/stderr from argument, manifest, Chrome,
   server, target/load, injection, timeout, non-loopback, and internal failures
   for raw rejected input, content, paths, ports, PIDs, browser details, and
   stacks.
8. **Regression boundary:** for the adjacent invariants the repair touched,
   use the existing committed tests and smoke path to recheck exits `0`/`1`/`2`,
   batch continuation, non-loopback blocking, real keyboard/contrast technique,
   deterministic golden output, honest observation counts/missing measures,
   and README agreement. Do not create a replacement corpus or second review
   rig. Reassess the raw-NUL binary-diff advisory only if the repair touched it.
9. **Repository gate:** reference the PR's authoritative `verify` check when
   available. Locally run only focused commands needed for the findings,
   governance lint, envelope scan, and `git diff --check`; do not duplicate the
   full suite routinely.

Blocking: any original failure remains; one-process batching is replaced by
per-case browser launches; an infrastructure/configuration failure becomes a
pass or ordinary criterion failure; state/network/content escapes; cleanup
remains incomplete; deterministic output changes without explanation; or
normal observations fail Track 0 validation.

## Output and verdict

Write the review to
`docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-25-browser-evaluation-runner-repair-review.md`.
Return `READY` only if F1–F6 are closed, the four transferred measurements are
completed, and no regression remains. Otherwise return `NOT READY` with the
exact failed measurement and smallest evidence-backed remediation.

Do not repair the implementation, spawn a sub-agent, push, open a PR, merge,
or begin completion records.
