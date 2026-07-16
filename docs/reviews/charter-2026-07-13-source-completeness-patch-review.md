# Charter: Source Completeness Reconciliation Patch — Pre-Merge Review

Date: 2026-07-13. Owner-commissioned; issued by the principal foreman. Subject: branch `patch-source-completeness-reconciliation` (commits `12d1f8a`, `c8ddb30`, `92d7e7d` at charter time), built under `charter-2026-07-13-source-completeness-patch.md` to close SC-R1 and SC-R2 of `2026-07-13-source-completeness-reconciliation.md`. The owner merges non-ff to `main` only after this review's verdict.

- **Seat:** patch reviewer, Medium tier, owner-launched external context, independent of the patch builder and of the reconciliation reviewer.
- **Method:** check out or `git show` the patch branch read-only. You may run the full verification suite on the patch branch via the project `.venv` and write throwaway probes outside the repository. Your only repository write is the review file below.

## Scope

1. **SC-R1 closure.** Does the admission boundary now reject (or atomically route) a plain `assertion` whose fact matches an adopted family's member predicate? Re-run the reconciliation review's SC-R1 reproduction *exactly as written* and confirm the outcome is now rejection/routing with the closure finding, zero, and coverage unable to survive a late member. Assess the boundary *choice* the builder made (reject-at-admission vs atomic routing) against ADR-0016/0017 and Articles 7/12/13 — is the rationale sound and the placement authoritative (kernel-enforced, not honor-system relocated)?
2. **SC-R2 closure.** Re-run the double-transition reproduction; confirm a same-member `assert`-arm transition is rejected and the horizon does not advance (ADR-0017 decision 4), while genuine add/remove/reclassification still passes.
3. **No collateral damage.** All previously verified lifecycle guarantees stay green: incremental/rebuild equality, atomic rejection, family isolation, old-zero displacement after valid transition, re-attestation + rerun, no-resurrection. Full suite, lint, and mypy on the patch branch.
4. **Scope discipline.** The diff contains only SC-R1, SC-R2, their probes, and the accompanying ADR — nothing absorbed from adjacent defects or successor-milestone material. `packages/tax/loader.py` and `packages/kernel/schema_registry.py` changes must be justified by the findings.
5. **ADR conformance and numbering.** The builder committed the boundary ADR as **ADR-0018**. That number is free on `main` but **collides with ADR-0018 (citation resolver contract) on `milestone/core-tax-conditions`**, which will merge later. Finding required: the patch ADR must be renumbered to the next globally free number (**0023**; 0018–0022 are occupied on the milestone branch) before merge. Also review the ADR's substance: status `proposed`, correct tier, context citing the review, decision matching the implemented boundary, consequences and alternatives honest.
6. **Regression probe quality.** Probes reproduce the review's accepted-act paths end-to-end (not just unit-level), and would fail on the pre-patch code.

## Output

`docs/reviews/2026-07-13-source-completeness-patch-review.md` (write it on the **milestone branch working tree**, where the other review documents live — do not commit on the patch branch). Findings labeled SC-PR1, SC-PR2, …, each with severity (**merge-blocking** / production condition / non-blocking) and reproduction. End with a verdict: merge-ready as-is / merge-ready after listed corrections / not merge-ready. Advisory: the owner decides and merges.

## Stop conditions

Stop at the single review file. Record fixes as findings; do not implement them, do not touch the patch branch.
