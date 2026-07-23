# Milestone Rescope: Push-Envelope Preflight and Bypass Visibility

Status: **active — Track 1 ready for owner-held integration** (2026-07-22).
The implementation commit `7ceb54a` on `track/push-envelope-posture-audit`
passed independent review `344b620`; Track 2 records await its integration.
This is the successor planning surface for the stopped Guarded Transport and
Credential Confinement H1 topic. It operates under ADR-0030 and ADR-0034.

## Objective

Give the operator a mechanically reproducible, synthetic-only audit of the
existing push-envelope gates: prove what installed hooks block when they run,
and report that raw `git push --no-verify` is still bypass-reachable. This
improves visibility and voluntary preflight discipline at **L3**; it does not
confine credentials, prevent raw publication, or claim L4.

## Current state

ADR-0031's installed pre-commit/pre-push hooks and byte verifier already scan
envelopes. The stopped H1 prototype showed that the missing credential wall
cannot be honestly inferred from these hooks: raw `--no-verify` skips the
pre-push hook, and neither tested local topology produced a reproducible
scan-before-credential-release proof. Those conclusions remain intact; this
rescope does not retry them.

## Scope

1. **Synthetic posture audit.** Add a local command that creates only
   disposable repositories, installs the committed hook shims, and reports a
   stable posture record with: hook byte-verification; seeded-marker refusal
   when the pre-push hook executes; raw `--no-verify` bypass reachability; and
   `credential_confinement: unestablished`.
2. **Voluntary preflight guidance.** The command and README explain how to
   invoke the existing envelope scan before an operator chooses to push. It
   does not wrap, replace, or hold the actual transport credential.
3. **Regression battery.** Focused tests prove all posture states using only
   constructed markers, temporary repositories, and a local bare remote.
4. **Honest records.** Reaffirm deferral-ledger entries 1 and 2 as touched,
   not retired; retain the data-boundary row at L3; record that no live run or
   server attestation is acceptance evidence for this rescope.

## Non-goals

- No credential, credential helper, askpass, operating-system store, remote
  setting, GitHub configuration, or actual owner push.
- No claim that the audit prevents raw push or discharges ADR-0031's guarded
  transport production condition.
- No maturity-matrix upgrade, deferral retirement, Tier 3 ADR, or reopening
  of the stopped H1 evidence.

## Contracts and fixtures

The command reuses `tools/envelope_scan.py` and
`tools/install_envelope_hooks.py`; it introduces no schema or persisted
artifact. Its stable report is an operator diagnostic, not a credential or
server-control attestation. Fixtures construct the marker from fragments and
use a local temporary bare Git repository, matching `tests/test_envelope_hooks.py`.

## Verification and data safety

- Focused audit tests prove four states: hooks verified; hooked marker push
  refused; `--no-verify` marker push accepted by the synthetic remote and
  reported as bypass-reachable; hook tamper/missing installation reported.
- Full unit suite, mypy, governance lint, and envelope scan remain green.
- No test invokes a network remote, owner credential store, quarantined
  workspace, or real data; markers are constructed from fragments.

## Exit criteria

1. The audit emits a clear, stable distinction between hook protection and
   credential confinement, naming the latter `unestablished`.
2. The four focused posture states are exercised through real temporary Git
   push commands, not helper-only calls.
3. Documentation tells the operator that the audit is visibility/preflight
   support only; raw `--no-verify` remains bypass-reachable.
4. Ledger entries 1 and 2 are re-affirmed, not retired; the matrix remains L3
   with a footnote to this limited aid.
5. No personal data, credential, real remote, or live-run detail enters the
   repository.

## Tracks

### Track 1 — Synthetic push-envelope posture audit

Implement the bounded audit command and focused synthetic Git tests. The
authoritative surface is the command's actual temporary `git push` sequence;
the test must demonstrate both hook refusal and `--no-verify` bypass, never
claiming that the latter is safe. One implementation branch, independent
review before merge.

### Track 2 — Documentation and records

Add README guidance and the explicit deferral/maturity/phase-state records.
No owner live run: this rescope does not change real-data transport safety.
Review and merge records separately after Track 1's review.
