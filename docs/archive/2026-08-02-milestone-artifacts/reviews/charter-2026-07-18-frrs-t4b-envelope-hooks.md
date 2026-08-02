# Charter: Track 4b — Repo-Side Envelope Hook Installation

Date: 2026-07-18. Owner-directed unit, implemented by the foreman in-session
(no sub-agent dispatch; ADR-0034 satisfied by direct owner instruction).
Branch: `track/frrs-t4b-envelope-hooks`. The owner holds the merge.

## Origin

The foreman's post-merge review of Tracks 1–4 (this session) found that
ADR-0031's production condition — commit/push envelope gates as *installed,
integrity-checked hooks* — was discharged only as an in-process model
(`LiveWorkspace.guarded_commit/guarded_push`), which a real `git commit
--no-verify` or raw `git push` never executes. The Track-4 closing note's
"installed integrity-checked envelope entrypoints" row overclaimed against the
ADR's definition. The owner directed this unit to install the repo-side half
before the first real run.

## Deliverables

1. **Committed scanner** (`tools/envelope_scan.py`): scans the added lines and
   staged paths of a commit or push envelope for path-shaped variants of the
   reviewed residency-marker vocabulary (the substrings every track safety test
   scans for) plus an SSN-shaped pattern. Path-shaped, because review records
   legitimately *quote* bare markers; a required following path segment
   distinguishes documentation from a leak. A visible per-line pragma declares
   a deliberate synthetic occurrence.
2. **Committed installer** (`tools/install_envelope_hooks.py`): writes
   byte-exact pre-commit/pre-push shims into the clone's hooks directory
   (worktree-aware) and verifies them.
3. **Per-clone structural requirement** (`tests/test_envelope_hooks.py`): the
   suite byte-verifies the installed shims in the running clone and fails with
   the remedy command when they are absent, tampered, or stale — so the
   standard verification battery any gate runs cannot pass in an ungated
   clone. Executed goldens: seeded-marker staged/commit/push refusals (including
   a real `git commit` refused by the installed hook), clean-envelope passes,
   quoted-bare-marker documentation passes, pragma exemption, tamper detection.

## Scope fence

Synthetic seeded markers only, built by concatenation so no committed byte
forms a marker. No ADR edit, no schema, no change to the in-process
`LiveWorkspace` gates, no personal data, no UI/OCR/coverage growth.

## Named residuals (owner-visible, not silently closed)

- **Operator-level bypass:** a determined operator can still run
  `git commit --no-verify` or delete the hooks; the suite's per-clone check
  then fails the next gate battery, making the bypass *detected*, not
  *impossible*. OS/server-level prevention (e.g. GitHub push protection) is a
  standalone owner decision.
- **Guarded transport / credential confinement** (ADR-0031's "remote
  credentials reachable only through the guarded push path") remains **not
  implemented**; this unit explicitly re-defers it as a named deferral for the
  Track 5 ledger rather than claiming it.
- The pragma exempts a line visibly; a reviewer reads it in the diff.

## Verification

Focused suite; full `python3 -m unittest`; `mypy packages tools tests`;
`python3 tools/governance_lint.py`; hooks installed in the working clone and
exercised by this branch's own commits and push (dogfood).

## Review gate

Foreman-authored under direct owner instruction; the owner reviews at the PR.
The owner may instead authorize an author-independent review seat before
merging (recommended default for safety-boundary code; owner's call under
ADR-0034).
