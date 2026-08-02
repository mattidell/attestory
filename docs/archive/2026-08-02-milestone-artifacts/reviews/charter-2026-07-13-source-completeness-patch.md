# Charter: Source Completeness Reconciliation Patch

Date: 2026-07-13. Owner-commissioned; issued by the principal foreman. Closes the decision-blocking findings of `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-13-source-completeness-reconciliation.md`. Precedents: `patch-kernel-reconciliation` (2026-07-10 review), Derivation Cascade Reconciliation (merge `18ce073`, 2026-07-11 review).

- **Builder:** patch builder, High tier, owner-launched external context.
- **Branch:** `patch-source-completeness-reconciliation`, created from the tip of `main` (`5116e01`). Not from the milestone branch. The builder works and commits on this branch only; merge to `main` is the owner's, non-ff, after verification.
- **Scope:** exactly the review's minimal finding set — SC-R1 and SC-R2 — plus their regression probes. No successor-milestone content, no prototype material, no unrelated hardening.

## SC-R1 — authoritative membership routing/admission boundary

A predicate-matching member fact for an adopted family must not be admittable through a plain `assertion` while leaving the family's closure finding, closure-backed zero, and `closed` coverage current. Establish the authoritative boundary the review names: either **reject** such an assertion at admission (directing it to the member-transition path) or **route it atomically** through a successor horizon. The builder proposes which, with rationale grounded in ADR-0016/0017 and Articles 7/12/13; rejection-at-admission is presumptively simpler (no new atomic composite act), but the choice is the builder's to argue.

If the chosen fix changes a declared contract (kernel admission semantics were explicitly recorded as a workspace-service-layer obligation), draft the accompanying Tier-2 ADR in the same branch: context citing the review, decision, consequences, alternatives. The ADR lands as `proposed`; the owner ratifies at merge.

## SC-R2 — same-member corrections are not membership transitions

`apply_member_transition` must verify that an `assert`-arm transition actually changes predicate membership: a transition asserting a fact already in the family must be rejected (ADR-0017 decision 4 — value corrections belong on the ordinary assertion path and do not advance the horizon). The admission boundary must distinguish add/remove/reclassification from same-member correction.

## Required evidence

- End-to-end regression probes reproducing **both accepted-act paths from the review exactly as written** (the B1 genesis → plain assertion path; the double-transition path), asserting the corrected behavior.
- The existing valid-transition lifecycle guarantees remain green untouched: incremental/rebuild equality, atomic rejection, family isolation, old-zero displacement, re-attestation + rerun, no-resurrection.
- Full verification per milestone convention: `.venv/bin/python -m unittest`, `.venv/bin/python tools/governance_lint.py`, `.venv/bin/python -m mypy`, data-safety scan over changed content.

## Commits

One commit per finding (fix + its probes), plus the ADR commit if needed. Each commit message cites its finding id.

## Stop conditions

Stop at SC-R1 + SC-R2 closed and verification green. If closing a finding exposes an adjacent defect, record it as a note in the review file's topic directory for triage — do not absorb it. Report unresolved authority questions explicitly.
