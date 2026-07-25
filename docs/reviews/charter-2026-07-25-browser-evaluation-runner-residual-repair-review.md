# Browser Evaluation Runner Residual Repair Delta-Review Charter

Status: **prepared next prompt.** It becomes current only after the R1/R2
Residual Repair Builder hands off.

## Context Capsule

- **Source ref:** `track/browser-evaluation-runner-completion`; resolve and
  record its commit at launch.
- **Exact object:** the R1/R2 residual-repair commit relative to the reviewed
  commit named `repair browser evaluation runner integrity`, limited to the
  files allowed by the residual repair charter. Foreman routing and prior
  review records are outside the artifact-quality object.
- **Role:** the same delta Reviewer lineage when available; otherwise one fresh
  independent delta Reviewer. High tier / medium effort.
- **Scope:** independently verify only that R1 and R2 are closed and the
  accepted F1–F6 repair plus directly touched acknowledgement/timeout
  invariants remain intact.
- **Evidence-rung ceiling:** one focused residual delta recheck. Do not reopen
  the original harness review, repeat the F1–F6 adversarial sweep, explore
  beyond R1/R2, redesign contracts, implement a repair, or make product/economy
  claims.
- **Stop conditions:** stop if the repair object cannot be resolved, either
  residual lacks a committed regression, Chrome is unavailable, the Reviewer
  has seen Builder working context, a check needs remote/personal data, or a
  conclusion would exceed the two-finding gate.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`;
  `docs/adr/INDEX.md`; the residual repair charter; the R1/R2 sections and
  `READY` baseline in the completed delta review; the residual repair diff and
  changed tests; and the plan's owner-authorized residual exception.

Before reviewing, echo the resolved repair range, two-finding scope, evidence
ceiling, and stop conditions. Treat Builder claims as input, not proof.

## Required measurements

1. Independently reproduce the original R1 busy-candidate case and show the
   acknowledgement path honors `timeout_ms`, fails with `injection-failed`, and
   cleans its tuple/context/resources.
2. Independently reproduce R2 by pre-setting the former fixed global marker
   while preventing the registered injection from completing. It must fail
   closed.
3. Confirm a valid injection still acknowledges before candidate code and
   passes when its criterion passes.
4. Confirm the marker is per-tuple/private, absent from every public output,
   and does not make normalized report/observation bytes nondeterministic.
5. Run the committed focused Node/real-Chrome suite once to prove the accepted
   F1–F6 floor remains intact. Do not recreate the original review rig or
   repeat unrelated probes.
6. Run the per-review envelope scan and `git diff --check`; reference the PR
   `verify` check for the unchanged repository-wide floor.

Blocking: R1 or R2 remains reproducible; a timeout or incomplete injection can
pass; cleanup regresses; the marker leaks; deterministic public output changes;
or an accepted F1–F6 regression fails.

## Output and verdict

Write the review to
`docs/reviews/2026-07-25-browser-evaluation-runner-residual-repair-review.md`.
Return `READY` only if both residuals are closed and the focused accepted floor
remains intact. Otherwise return `NOT READY` with the smallest exact residual.

Do not repair implementation, spawn a sub-agent, explore past the two accepted
findings, push, merge, or begin completion records.
