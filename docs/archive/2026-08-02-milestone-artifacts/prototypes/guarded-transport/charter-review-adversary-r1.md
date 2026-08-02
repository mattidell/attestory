# H1 Round 1 Adversary Review Charter

Role: **Adversary reviewer** (High tier). The owner authorized this review
dispatch on 2026-07-22 as part of the approved Track 0 plan. Work only on
branch `prototypes/guarded-transport-h1/review-adversary-r1`.

## Object under review

Attack these exact sealed exhibits, not their parent branches and not the
owner-excluded similarly named feature work:

- Incumbent: `1255b2732971c11ed0a5b4b012df7a4159c9b105`
  (`docs/archive/2026-08-02-milestone-artifacts/prototypes/guarded-transport/it1/{design.md,examination-it1.md}` and
  `prototypes/guarded-transport/h1_it1_probe.py`).
- Rival: `95b232f`
  (`docs/archive/2026-08-02-milestone-artifacts/prototypes/guarded-transport/it2/{design.md,examination-it2.md}` and
  `prototypes/guarded-transport/it2/probe.sh`).

Use `git show <commit>:<path>` or isolated temporary checkouts; do not modify
either exhibit. Your output is only
`docs/archive/2026-08-02-milestone-artifacts/prototypes/guarded-transport/reviews/round-1-adversary.md`.

## Attack measurements

Independently run or reproduce every feasible probe using only fresh temporary
repositories and constructed dummy credentials. Report `pass`, `fail`, or
`not run`, with a command/result for each.

1. Invoke raw `git push` and `git push --no-verify`; distinguish absent
   credential from a hook/scanner/remote refusal.
2. Try credential discovery through environment, credential helper, askpass,
   system/global/local config and includes, direct transport invocation, and
   the topology's private store or releaser. Attack descriptor inheritance or
   process visibility where that is the claimed boundary.
3. Seed a constructed residency marker and prove the guard refuses before
   credential release or transport invocation; then test guard-byte tamper and
   missing-install behavior.
4. Confirm each success drives actual local `git push`, not only a scanner or
   helper. Attack any unlisted discovery route exposed by the implementation.
5. Test the stated same-UID local-process adversary without escalating to a
   malicious owner. If a claim depends on an OS isolation guarantee absent
   from the fixture, mark that limit rather than inventing it.

Do not repair, broaden the threat model, or choose a preferred design. Record
findings by H1-P1/P2, H2-P1, or H3-P1 and classify decision-blocking findings.
Commit only the review file, do not push or merge, and report the commit id.
