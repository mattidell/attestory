# Multiple-Statement Circumstances Design Evidence

This directory holds the retained design evidence for the multiple-statement-circumstances milestone:

- `p0-account-and-trace.md` — Account and trace investigation for two Form 1099-K statements and baseline execution.
- `p7-existing-pattern-candidate-c.md` — Candidate C investigation paper evaluating the adopted student-loan combination pattern.
- `test_candidate_c_probe.py` — Diagnostic probe for Candidate C.
- `family-version-lifecycle.md` — Family-version lifecycle outline and refinement leading to ADR 0079.
- `connected-sale-design.md` — Connected sale design from recording to saved explanation.
- `family-handover-contract-proposal.md` — Contract proposal for family-version handover.
- `track0-closure-evidence.md` — Track 0 adversarial closure evidence.
- `test_track0_closure_probe.py` — Executed live coordinator test suite settling Track 0 adversarial closure.

## Running the Probes

Run each probe individually from the repository root:

```sh
pytest docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances-evidence/test_candidate_c_probe.py
pytest docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances-evidence/test_track0_closure_probe.py
```
