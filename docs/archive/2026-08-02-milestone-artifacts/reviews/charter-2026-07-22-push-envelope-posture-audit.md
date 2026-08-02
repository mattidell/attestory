# Track 1 Charter — Push-Envelope Posture Audit

Role: **Builder** (Medium tier). Owner approved the rescope plan on
2026-07-22 and previously authorized builder dispatch at foreman discretion.
Work only on branch `track/push-envelope-posture-audit`.

## Goal

Add a local, synthetic-only audit command that tells the operator exactly what
the existing envelope boundary proves and what it does not: installed hook
integrity and a hooked seeded-marker refusal are verified; raw
`git push --no-verify` is reported as bypass-reachable; credential confinement
is reported as `unestablished`.

## Outputs

- `tools/audit_push_envelope_posture.py`, with a no-argument command-line
  entrypoint that emits a stable JSON record and an explicit exit status.
- Focused tests, normally `tests/test_push_envelope_posture.py`.
- Minimal README command documentation.

The success record must include boolean `hooks_verified`, boolean
`hooked_marker_refused`, boolean `no_verify_bypass_reachable`, and literal
`credential_confinement: "unestablished"`. Expected bypass reachability is a
successful, honest audit result—not a green safety claim. A missing or tampered
installed hook is an audit failure with a nonzero exit.

## Required authoritative-path evidence

Using a fresh temporary repository and local bare remote only, drive actual
Git commands to prove:

1. The cloned workspace hook bytes verify.
2. A constructed synthetic marker pushed with hooks enabled is refused before
   the remote update.
3. The same constructed marker pushed with `--no-verify` reaches the local
   synthetic remote; the audit reports this as `no_verify_bypass_reachable`.
4. Tampered or missing hooks report failure, never an affirmative posture.

The marker is assembled from fragments, as in `tests/test_envelope_hooks.py`.
No test may call a network remote, inspect credential helpers/stores, hold a
token, or emit an absolute user path. Do not implement a credential wrapper,
transport wrapper, server integration, a matrix change, or a live-run harness.

## Existing inputs and boundaries

Reuse `tools/envelope_scan.py` and `tools/install_envelope_hooks.py`; do not
change their existing scanner semantics unless an isolated correctness defect
in the new audit makes that unavoidable and is recorded. The audit is a
diagnostic over the already-installed gate, never a replacement for it.

## Verification and handoff

Run focused tests, the full unit suite, mypy, governance lint, and the envelope
scan. Commit only the completed Track 1 work on this branch. Do not push,
merge, alter the two deferral ledger entries, or review your own work. Report
the commit id, commands/results, and any scope deviation.
