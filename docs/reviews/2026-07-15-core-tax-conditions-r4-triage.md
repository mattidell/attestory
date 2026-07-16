# R4 Triage — Core Tax Conditions Remediation

Date: 2026-07-15. Foreman triage of the independent R4 note
`2026-07-15-core-tax-conditions-r4-independent-rereview.md`.

## Finding and classification

R4 measurements 1 and 4 found that the required R1 ACM-A1 golden exists but
is not executed by the test suite. The reviewer therefore returned `not ready`.

**Classification: decision-blocking.** The mechanism is not reopened: R4
measured it as correct. But PMR-1 cannot be honestly closed while its required
golden is inert; the gap repeats the green-suite-over-unexercised-condition
failure identified as PMR-3. This classification blocks R5 but does not enlarge
the accepted ADR-0027 contract.

## Disposition

Route to one bounded `repair1`: wire the already-committed ACM-A1 scenario into
the executed golden set. The repair may not alter projection, package membership,
registry semantics, schemas, or expected content. No ADR is needed.

After the repair lands, repeat R3-style full verification and obtain a fresh
independent R4 re-review of the repair delta before R5 may open.
