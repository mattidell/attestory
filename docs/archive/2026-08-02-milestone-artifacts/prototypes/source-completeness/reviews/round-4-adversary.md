# Round 4 Adversary Review — Source Completeness

Date: 2026-07-12  
Seat: adversary, Medium tier / medium effort  
Evidence rung: focused shape-A construction boundary (repair4)

## Method and observations

I read the round-4 charter, the `repair4/surface.py` implementation, the `test_surface.py` suite, and the previous round-3 adversary review. I did not read any same-round peer review outputs. I ran the test suite (`python3 -m unittest -v test_surface`) and confirmed all 12 tests pass. I evaluated the single public `compute` surface against the chartered adversary attacks.

By restricting the public API to a single `compute(rule, source_rows, mapping, findings)` entrypoint, the design eliminates the duck-carrier injection vectors and the raw bypasses found in round 3.

## Attacks: attack → outcome → exhibit

1. **False-closure trap — failed attack (design holds).** Passing a false, unknown, or superseded closure finding with an empty source blocks successfully. In all cases, `_resolve_authority` fails to admit the family, causing `_collect` to raise `Blocked`.
   **Exhibit:** `repair4/surface.py` lines 77-84, 93-98; `test_surface.py` lines 60-75.

2. **Caller-set smuggle — failed attack (design holds).** The public `compute` signature takes no carrier, environment, or closed-set parameters. Closed membership is derived strictly internally from the declared mapping and findings.
   **Exhibit:** `repair4/surface.py` lines 114-127; `test_surface.py` lines 119-126.

3. **Identity trap — not reproduced at this boundary.** Payer/account details are not modeled in the inputs or keys of this prototype.
   **Exhibit:** `repair4/surface.py` lines 86-99; `test_surface.py` lines 54-59.

4. **Rekeying trap — not reproduced at this boundary.** Fact identity is tax-year only; there is no input correction or replacement path that rekeys rule queries.
   **Exhibit:** `repair4/surface.py` lines 77-84, 102-111.

5. **Family-boundary trap — not reproduced at this boundary.** The mapping family maps to a closure fact without defining constituent member names.
   **Exhibit:** `repair4/surface.py` lines 86-99; `test_surface.py` lines 30-33.

6. **Stale-pin trap — failed attack (design holds).** When a stale finding is superseded by a current finding in the findings list, the resolver filters out the stale one, uses the current successor for admission, and pins it correctly.
   **Exhibit:** `repair4/surface.py` lines 102-111; `test_surface.py` lines 83-92.

7. **Evolution trap — failed attack (design holds).** Adding future boxes or reporting format changes does not force mapping rewrites or rekeying.
   **Exhibit:** `repair4/surface.py` lines 77-84, 114-129.

## Verdict and recommendation

I withdraw the prior adversary dissent. The selected shape-A prototype surface successfully closes the duck-carrier and alternate-callable bypasses while retaining prior completeness and exact pin guarantees. The evidence at this boundary is sufficient to proceed to drafting the SC-P1 shape-A ADR.

The remaining routing, mapping validation, and displacement propagation concerns are production-only implementation details (Track 2/3) that are correctly identified as residuals.
