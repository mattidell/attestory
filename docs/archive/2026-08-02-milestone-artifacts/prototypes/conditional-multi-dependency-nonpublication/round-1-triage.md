# Triage — Conditional Multi-Dependency Non-Publication, Round 1

Date: 2026-07-18
Foreman: principal foreman

This is the Gate-5 disposition of the independent Governance and Adversary R1
measurements. It classifies findings; it does not select an accepted contract
or overrule either reviewer’s artifact judgment.

## Finding disposition

| Findings | Classification | Disposition |
|---|---|---|
| Adversary A1 — IT2 conditionally demands members for admission but relies on separate value references to create their pins | **decision-blocking — IT2 only** | Reject IT2 as a converged candidate. A declared member omitted from value would control eligibility without an input pin; later supersession would not displace the published finding. Repairing that would change IT2’s core pin/eligibility account, so do not wordsmith it into acceptance. |
| Governance GR1-F1 through GR1-F5 — IT1’s per-rule-halt wording, inactive-to-active trace detail, no-reach-around argument, and NPE-surface precision | **non-blocking defects** | Preserve as ADR/production-analysis precision requirements. They do not alter IT1’s evaluated shape, widen scope, or require another builder pass. |
| Both reviews — IT1 CMDN-P1/P2/P3 | **settled paper evidence** | IT1 supplies the active/inactive behavior, all-missing non-publication, declared semantics, and two-edge currency account required by the Gate-6 floor. |
| Governance pass on IT2 P1/P2 and adversary failure on P3 | **rival evidence retained** | IT2 remains valuable negative evidence: the top-level conditional-requires placement exposes the mandatory pinning invariant, but it is not a production candidate. |

## Owner check-in

**Evidence status:** two genuinely different paper shapes were exercised on the
same six cases. The incumbent’s evaluator-node shape is sufficient at Rung 1
for CMDN-P1/P2/P3, subject to named production conditions. The rival’s
artifact-level pre-guard shape is rejected on a concrete supersession attack.
No authorized Rung-2 probe is needed: paper and committed-code review
distinguished the alternatives.

**Process incidents:** both external review artifacts landed within their
single-file boundaries. The prior no-length-cap amendment allowed the
governance review to report all measured evidence without compression. No
additional role was dispatched.

**Recommendation:** accept the incumbent conditional_dependency_set shape as
the converged prototype candidate; carry GR1-F1–F5 as precision obligations;
write the evaluation analysis, then draft the ADR and plain-language companion
for owner ratification. Do not repair IT2 or begin production implementation.
