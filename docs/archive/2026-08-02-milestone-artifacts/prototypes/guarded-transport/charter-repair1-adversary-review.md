# H1 Repair 1 Adversary Delta-Review Charter

Role: **Adversary reviewer** (High tier). The owner authorized reviewer
dispatch at the foreman's discretion on 2026-07-22. Work only on branch
`prototypes/guarded-transport-h1/repair1-adversary-review`.

## Object and boundary

Attack only repair exhibit `00d1550194b3b63b99312cfa63d2985f06d9c135`, using
`git show <commit>:<path>` or an isolated temporary checkout. Its changed
artifacts are `docs/archive/2026-08-02-milestone-artifacts/prototypes/guarded-transport/repair1/{design.md,examination-repair1.md}`
and `prototypes/guarded-transport/repair1/scan_before_release_probe.py`.
Prior findings are context only; do not read the rejected rival or
owner-excluded similarly named feature work. Output only
`docs/archive/2026-08-02-milestone-artifacts/prototypes/guarded-transport/reviews/repair1-adversary.md`.

## Attacks

Independently run or reproduce the complete synthetic probe in a fresh
environment and report pass/fail/not-run with commands/results.

1. Verify a clean guarded actual `git push` completes, and raw plus
   `--no-verify` reach the same descriptor-absent refusal without a hook.
2. Attack the fixed update: change the constructed marker or ref expectation
   and prove no descriptor, environment release, or transport receipt occurs
   before scanner success. Test guard-byte tamper and missing install.
3. Attack all ordinary same-UID discovery routes: environment, helper,
   askpass, system/global/local config/includes, direct transport, persistent
   artifacts, and any observable descriptor path. Do not invent privileged
   inspection, but flag any capability the stated non-malicious sibling can
   actually obtain.
4. Check that the H2 server-control sentence stays an owner attestation and
   that H3's E18.1/E18.2 event-order assertions are implementable from the
   described topology.

No repair, redesign, scope expansion, push, or merge. Classify a defeated
invariant as decision-blocking. Commit only the review file and report its
commit id.
