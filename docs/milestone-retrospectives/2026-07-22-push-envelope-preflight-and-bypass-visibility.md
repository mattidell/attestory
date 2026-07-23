# Retrospective — Push-Envelope Preflight and Bypass Visibility

Status: **independently reviewed; final on owner merge.**

## Milestone

After the Guarded Transport H1 prototype exhausted two rival local topologies
and its one repair without a reproducible actual-Git confinement proof, the
owner selected an honest-L3 rescope. The outcome is a synthetic posture audit,
not a credential-control system.

## Shipped

Track 1 (PR #45) added `tools/audit_push_envelope_posture.py`. In a disposable
local Git clone and bare remote it verifies hook bytes, proves a hooked seeded
marker push is refused, then proves the same marker reaches the synthetic
remote with `--no-verify`. Its stable output calls credential confinement
`unestablished`.

## Verification

Track 1 passed 549 tests, mypy, governance lint, and envelope scans; its
independent review found no blocking finding. Track 2's independent records
review also found no blocking finding; owner-held merge remains required
before this retrospective is final.

## Decisions

- **Tier 1:** the audit treats bypass reachability as a successful diagnostic
  observation, not a process failure. No new ADR or contract is created.
- The stopped H1 credential-confinement topic remains unratified. Its evidence
  does not authorize implementation or an L4 claim.

## Deviations

The original L3→L4 objective was not achievable from the evaluated local
credential topologies. The rescope deliberately delivers only visibility and
regression evidence. It does not verify an operator's active clone, and it is
not a meaningful substitute for actual transport protection.

## Data safety

All audit repositories, markers, remotes, and identities are synthetic and
temporary. No real credential, owner remote, workspace location, value, or
run detail entered the repository.

## Follow-ups

- Credential confinement remains ledger entry 1; any return to it begins as a
  separately chartered OS/identity/hosted-boundary Tier 3 topic.
- Raw `--no-verify` bypass remains ledger entry 2. Do not present the posture
  audit as a mitigation.

## Planning lessons

An executable limitation can be useful as a regression and communication aid,
but it must not be used to manufacture milestone value. Future planning should
only retain such a diagnostic when its operator or governance value is worth a
separate reviewed track; it is not a substitute for the deferred control.
