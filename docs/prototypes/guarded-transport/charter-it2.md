# H1 Iteration 2 Charter — Guarded Transport Executor (Clean-Room Rival)

Role: **Rival builder** (High tier). This is the exact charter authorized by
the owner on 2026-07-22 for Track 0 of Guarded Transport and Credential
Confinement. Work only on branch `prototypes/guarded-transport-h1/it2`.

## Clean-room boundary and question

Do not read `prototypes/guarded-transport/it1`, `docs/prototypes/guarded-transport/it1`,
or any output from the incumbent. Independently determine whether a guarded
transport-executor topology — rather than a credential-helper/release topology
— can make a real local Git push receive a synthetic credential only inside the
guarded execution path, while raw Git and `--no-verify` fail before transport.

The remote credential must not be configured in normal Git settings or a
globally discoverable helper. Do not rely on a pre-push hook as the control.
If the local same-user threat model makes this topology unprovable, demonstrate
the exact reachable route and report that failure.

## Required evidence

Produce exactly these documents under `docs/prototypes/guarded-transport/it2/`:

1. `design.md` — the rival topology, credential-discovery inventory, producer
   → authority → consumer → failure map, and H2/H3 paper disposition.
2. `examination-it2.md` — commands/results for every case below, the actual
   Git entrypoint driven, and a proposition-by-proposition conclusion.

You may add throwaway prototype code only under `prototypes/guarded-transport/`
on this branch. It must construct a fresh temporary local Git repository,
dummy transport, and non-secret credential at runtime. Do not modify
production code, existing tests, hooks, phase documents,
plan/charter/seat/process-log files, ADRs, or any artifact outside your
iteration directory.

## Cases and measurement

Run all five Gate-2 cases from the approved plan:

1. A clean guarded push reaches the local dummy transport only after the
   existing envelope scan passes.
2. Direct `git push` fails because no credential is reachable; repeat with
   `git push --no-verify` and show the same reason.
3. A constructed synthetic residency marker causes the guarded entrypoint to
   refuse before credential release or transport invocation.
4. Independently attempt environment, Git credential helper, askpass, config
   include, and the executor-private store/releaser. Record pass/fail/not-run;
   no unlisted route may be silently presumed absent.
5. Show install/verification/tamper lifecycle: guard-owned-byte tamper or
   missing installation fails closed before transport.

The Rung-2 probe must drive an actual local Git transport command, not a
downstream helper. Test a direct transport invocation and configuration
precedence (system/global/local config plus environment) as adversarial cases.
No network remote or owner credential may be used.

## Stop and handoff

Stop when the documents and optional disposable probe satisfy the five cases.
Commit only your branch's artifacts with a descriptive message; do not merge,
rebase, push, edit shared refs, or review the incumbent. Report the commit id
and whether H1-P1/P2, H2-P1, and H3-P1 are settled, blocked, or deferred.
