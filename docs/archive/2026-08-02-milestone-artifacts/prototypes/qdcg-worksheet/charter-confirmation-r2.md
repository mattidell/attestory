# Charter: Confirmation R2 — D2 Repair 2

Status: **prepared, inactive — no seat assigned or dispatched**

This fresh confirmation review is contingent on the completed Repair 2
artifact. It becomes executable only if the owner later approves this exact
charter and explicitly releases the reviewer seat under ADR-0034.

- **Proposed role:** confirmation reviewer, Medium tier, fresh independent
  context — no access to the Repair 2 builder's session, the foreman's
  verification pass, or Confirmation R1's reviewer.
- **Inputs after release:** `charter-repair2.md`, `repair2/design.md` and
  `examination-repair2.md`, `repair1/design.md` and
  `examination-repair1.md` (the unchanged posture Repair 2 builds on),
  `reviews/confirmation-r1.md` and `confirmation-r1-triage.md` (the exact
  failing measurement being re-measured), ADR-0037 and its cited CMDN
  prototype/production evidence, and the same committed evaluator, runner,
  explanation, and package-validation surfaces measured in R1 — read
  directly, not taken on the design's citations.
- **Exclusions:** no production implementation, no ADR draft, no evaluation
  analysis, and no re-litigation of D2-P1 or D2-P3 beyond confirming Repair
  2 left them genuinely untouched.

## Scope

This is a **delta re-check**, not a fresh D2 round. Confirmation R1's five
passing measurements (single successor posture, qualified-zero reduction,
present-`yes` disposition, the D2-P3 admission/universe boundary, and
production-condition honesty) stand unless Repair 2's guard substitution
itself disturbs them. Measure exactly:

1. **The repaired case (R1's sole failure).** Qualified-positive, both
   declarations absent: the design's `conditional_dependency_set` guard
   produces one non-publication disposition naming *both* declaration
   symbols, sourced from the committed evaluator's accumulate-then-raise
   loop and the runner's guard `try`/`except` — read the actual code
   yourself and confirm it does what the design's line citations claim, not
   only that the citations exist.
2. **The single-absent case.** Qualified-positive, exactly one declaration
   absent: the walk names that declaration alone, never implying the other
   is present or silently zero.
3. **Reduction property, re-grounded.** Qualified-zero still reaches the
   unchanged ordinary result reading neither declaration, and — this is the
   specific claim Repair 2 makes that Repair 1 did not — the reduction now
   follows from `conditional_dependency_set`'s own false-condition contract
   because the node sits first and unconditionally in the guard, not from
   the outer `any`'s operand order. Confirm this structural claim against
   the actual expression tree in the design, not merely its prose.
4. **Present-`"yes"` stays structurally distinct from absence.** Trace both
   paths independently: absence must raise inside the evaluator and be
   caught by the runner's guard exception handler (→ `blocked`); a present
   `"yes"` must evaluate cleanly to a boolean `false` guard with no
   exception anywhere (→ `inapplicable`). If any code path could produce
   the same disposition for both a present-wrong-value answer and a missing
   answer, that is a decision-blocking finding.
5. **Declared-zero publish and displacement, unaffected.** Both
   declarations current at `"no"`: the worksheet still publishes, both
   declaration findings still enter the access log and get pinned, and a
   later supersession of either still displaces line 16 through the
   existing two-edge model — confirm the design's citation to ADR-0037
   decision 3's pin-integrity guarantee is apt and not merely asserted.
6. **D2-P1 and D2-P3 genuinely unchanged.** The declaration fact types,
   their `{yes, no}` domain, presence-before-value discipline, and the
   admission-locus contradiction interlock are byte-identical in posture to
   Repair 1 — confirm by direct comparison, not by the design's own claim
   that nothing changed.
7. **The reported collateral finding is accurate.** `conditional_dependency_set`
   is admissible only under `rule-artifact.v3`, not `.v2` — confirm directly
   against both schema files (grep for the op string in each) rather than
   trusting the design's stated occurrence count. Confirm this genuinely
   requires only a package-pin correction (v1→v3) and not any other
   undisclosed change to D2-P1/D2-P3's committed shape.
8. **Every HEAD citation is real.** Spot-check a sample of the design's
   line-number citations against the actual files at HEAD (they will have
   drifted somewhat since the design was written if any unrelated commits
   landed in between — confirm the *logic* the citation describes is still
   accurate, not that the exact line number is frozen).

## Verdict

The review ends with a narrow `confirmed` / `not confirmed` verdict on
whether Repair 2 resolves Confirmation R1's sole decision-blocking finding
(measurement 3) without disturbing R1's five passing measurements. It does
not reopen D1, D3, statutory-rate fidelity, or presentation, and it does not
extend into evaluation analysis or ADR drafting — those remain separately
gated on a `confirmed` result here.
