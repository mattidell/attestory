# Committee Round 2 — Executable SC-P1 Evidence

Date: 2026-07-12. Foreman-assembled after repair1 and repair2.

## Scope

Determine whether the new executable evidence settles SC-P1 affirmative-only
enforcement and whether it distinguishes the two surviving authority shapes.
Do not reopen SC-P2, SC-P3, SC-D1, production implementation, or schema design.

## Exhibits

- Paper designs: `exhibits/source-completeness/it1` and `it2`.
- Resolver/mutation evidence: `exhibits/source-completeness/repair1`.
- Throwaway calculation-path evidence: `exhibits/source-completeness/repair2`.
- `round-1-triage.md` supplies the findings these repairs were required to
  address.

## Measurements

- **Governance:** rerun round-1 checks 1, 2, 5, 6, and 7 against the executable
  evidence. Report whether current-true-only authority, no caller-supplied set,
  declared meaning, exact pins, and scope now hold; keep schema declarations as
  a production condition rather than demanding production artifacts here.
- **Adversary:** rerun attacks A1, A2, A6, and the SC-P1 portion of A7 with
  equal effort on both shapes. Attempt a new authority writer, presence/value
  confusion, ambiguity overwrite, stale pin, and mapping-evolution divergence.
- **Expressiveness:** independently run the repair1 and repair2 suites before
  reading their examinations; map every repair charter fixture to an executed
  result and report any mismatch or untested distinction.

## Failure shapes

Failure is a reproducible path where false, absent, displaced, ambiguous, or
caller-injected authority publishes; a published zero lacks the exact current
closure pin; production behavior is smuggled into the prototype; a charter case
is missing; or a claimed result cannot be independently reproduced.

## Outputs and independence

- `reviews/round-2-governance.md` (≤ 150 lines)
- `reviews/round-2-adversary.md` (≤ 150 lines)
- `reviews/round-2-expressiveness.md` (≤ 150 lines)

All reviewers work independently and do not read same-round peer outputs or
commit-message bodies. Findings recommend only; foreman owns final triage.
