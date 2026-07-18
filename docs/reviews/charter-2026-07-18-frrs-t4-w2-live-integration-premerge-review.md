# Charter: Track 4 — W-2 Closure and Live Integration — Pre-Merge Review

Date: 2026-07-18. Owner-authorized, author-independent pre-merge review of
`track/frrs-t4-w2-closure-live-integration`. Review delta: `6858ad7` →
`c39a79b` (one grouped implementation commit). Implementation charter:
`docs/reviews/charter-2026-07-18-frrs-t4-w2-closure-live-integration.md`.
The reviewer must not merge, repair, push, open GitHub review objects, handle
personal data, or dispatch another agent.

## Required measurements

1. **RG-1 and immutable content:** prove core-v2 resolves with
   `validation.ok == True`, core-v1 still refuses with the historical eight
   contained issues, and no published v1 citizen is rewritten. Verify the
   regenerated package registry, release, and adoption bytes independently.
2. **ADR-0014 W-2 closure:** execute true empty closure, present-wage, false,
   absent, displaced, non-boolean, and duplicate cases. Measure pins: closure
   authority appears only for the empty zero; present-source aggregation carries
   no closure pin. Confirm mapping/family authority is adopted, exact, and not
   caller-supplied.
3. **ADR-0027/0028 ledger:** measure role-canon/form-field integrity,
   versioned bundle/fact members, dual surface/nested-set equality, exact mapping
   edges, composition obligation/binding, quantity vocabulary, and force-declare
   reject and non-trigger behavior. Confirm the closing note disposes of every
   ADR-0033 §4 PC(T4) row without claiming historical-v1 migration is complete.
4. **Live coordinator and D1/D2:** independently probe that a bootstrapped
   synthetic `L` plus authoritative acts can resolve → project → marshal →
   execute → write paired records/declared output only inside `L`; refusal must
   write no run record. Prove caller-selected package authority, raw `RunContext`,
   fixture `runner.run`, unminted marshal token, uninstalled/tampered envelope
   guard, raw transport, and path escape each refuse. Do not use real data.
5. **Track-3 residuals:** verify physical-layout order independence and exact
   member-byte refusal; ensure F2/F3/F4/F6/F7 are actually discharged rather
   than merely restated.
6. **Scope and safety:** no personal data, workspace locator, real-run report,
   UI/OCR/e-file/coverage expansion, new ADR, or rewrite of published v1 bytes.
   Run the full safety scan over the implementation delta.
7. **Verification:** re-run focused Track-4 and Track-3 suites, the full suite,
   mypy, and governance lint. Report exact results.

## Output

Write exactly one review record:

`docs/reviews/2026-07-18-frrs-t4-w2-live-integration-premerge-review.md`

Give an explicit merge-ready/not-merge-ready verdict and classify every finding
as blocking, scope defect, production condition (with owning track), or
non-blocking. The review is advisory; the owner decides merge disposition.
