# H1 Repair 1 Governance Delta-Review Charter

Role: **Governance reviewer** (Medium tier). The owner authorized reviewer
dispatch at the foreman's discretion on 2026-07-22. Work only on branch
`prototypes/guarded-transport-h1/repair1-governance-review`.

## Object and boundary

Review only repair exhibit `00d1550194b3b63b99312cfa63d2985f06d9c135`, using
`git show <commit>:<path>` or an isolated temporary checkout. Its changed
artifacts are `docs/prototypes/guarded-transport/repair1/{design.md,examination-repair1.md}`
and `prototypes/guarded-transport/repair1/scan_before_release_probe.py`.
Prior round findings are context only; do not re-review the rejected rival,
the owner-excluded similarly named feature work, or unmodified incumbent
surface. Output only `docs/prototypes/guarded-transport/reviews/repair1-governance.md`.

## Measurements

For each report pass/fail/not-run with direct evidence.

1. **Ordering and exactness.** Confirm the scanner receives the same fixed
   new-ref update that the subsequent local `git push` attempts, and that it
   completes cleanly before token-pipe creation or inheritance by a Git child.
   Confirm marker/tamper/missing-install paths create no descriptor and invoke
   no transport.
2. **Non-skippable raw posture.** Confirm actual raw `git push` and
   `git push --no-verify` fail for the same descriptor-absent reason, not a
   hook, scanner, or remote refusal.
3. **Honest same-UID boundary.** Check the ordinary sibling-process inventory
   against every declared route. Confirm privileged inspection is explicitly
   excluded as a malicious-owner/OS-escalation concern rather than silently
   claimed safe, and judge whether that limit is coherent with the milestone's
   named local-process threat.
4. **H2/H3 contract.** Confirm H2 names only an owner-attested server backstop
   and does not claim a local proof; confirm H3 specifies implementable E18.1
   and E18.2 assertions including no descriptor before scan acceptance.
5. **Boundary/process.** Confirm synthetic-only data and no scope expansion.

Classify any failed required invariant as decision-blocking. Do not repair or
redesign. Commit only the review file, do not push or merge, and report its
commit id.
