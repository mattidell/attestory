# H1 Iteration 1 Charter — Guard-Owned Credential Release (Incumbent)

Role: **Incumbent builder** (High tier). This is the exact charter authorized
by the owner on 2026-07-22 for Track 0 of Guarded Transport and Credential
Confinement. Work only on branch `prototypes/guarded-transport-h1/it1`.

## Question

Can a guard-owned credential-release topology make the authoritative local Git
push path the only route that receives a synthetic credential, while a direct
`git push` and `git push --no-verify` have none to discover?

The topology under test may use a guard-owned credential-releaser plus a
subprocess-local transport configuration. It must not assume that an installed
pre-push hook protects the raw invocation. A result that establishes this
shape cannot be proven under the declared local threat model is a valid,
valuable conclusion.

## Required evidence

Produce exactly these documents under `docs/archive/2026-08-02-milestone-artifacts/prototypes/guarded-transport/it1/`:

1. `design.md` — the topology, credential-discovery inventory, producer →
   authority → consumer → failure map, and H2/H3 paper disposition.
2. `examination-it1.md` — commands/results for every case below, the actual
   Git entrypoint driven, and a proposition-by-proposition conclusion.

You may add throwaway prototype code only under `prototypes/guarded-transport/`
on this branch. It must create a fresh temporary local Git repository and a
dummy transport/credential fixture at runtime; do not commit a token, remote
URL, home path, or workspace detail. Do not modify production code, existing
tests, hooks, phase documents, plan/charter/seat/process-log files, ADRs, or
another topic's artifacts.

## Cases and measurement

Run all five Gate-2 cases from the approved plan:

1. A clean guarded push reaches the local dummy transport only after the
   existing envelope scan passes.
2. Direct `git push` fails because no credential is reachable; repeat with
   `git push --no-verify` and show the same reason.
3. A constructed synthetic residency marker causes the guarded entrypoint to
   refuse before credential release or transport invocation.
4. Independently attempt environment, Git credential helper, askpass, config
   include, and the guard-private store/releaser. Record pass/fail/not-run;
   no unlisted route may be silently presumed absent.
5. Show install/verification/tamper lifecycle: guard-owned-byte tamper or
   missing installation fails closed before transport.

The Rung-2 probe must drive an actual local Git transport command, not call a
scanner or helper in isolation. A fake success that bypasses `git push` is a
failure. Do not contact a network remote or use any owner credential.

## Stop and handoff

Stop when the documents and optional disposable probe satisfy the five cases.
Commit only your branch's artifacts with a descriptive message; do not merge,
rebase, push, edit shared refs, or review the rival. Report the commit id and
whether H1-P1/P2, H2-P1, and H3-P1 are settled, blocked, or deferred.
