# H1 Round 1 Triage

Foreman record, 2026-07-22. Inputs: incumbent exhibit `1255b273`, clean-room
rival exhibit `95b232f`, Governance review `56c0df6`, and Adversary review
`587e605`. This is a Gate-5 classification record, not a quality re-review of
the artifacts.

## Findings and classification

| Id | Evidence | Proposition | Classification | Disposition |
| --- | --- | --- | --- | --- |
| GT-G1 | Governance: the incumbent's `--verify` checks hook-byte installation, but its actual outgoing-envelope scan is the pre-push hook after the token descriptor has already gone to the Git child. | H1-P1/P2 | **decision-blocking** | A confinement topology may not release a credential before the envelope has passed. The incumbent cannot support ratification as exhibited. |
| GT-A1 | Adversary: a fresh incumbent probe hangs before its clean actual-transport and later attack cases complete. | H1-P1/P2 | **decision-blocking** | The authoritative-surface measurement is unreproduced; no positive confinement claim may rest on it. |
| GT-G2 / GT-A2 | Governance and Adversary: a same-UID process can read the rival's mode-600 executor store. | H1-P1/P2 | **decision-blocking** | A local private file is not a capability boundary for the named local-process adversary. The rival topology is rejected for this topic. |
| GT-G3 / GT-A3 | Governance: H2's owner-attested server backstop and H3's complete E18.1/E18.2 form are incomplete; Adversary reports H2/H3 deferred. | H2-P1/H3-P1 | **decision-blocking for a complete H1 ratification** | The implementation-plan contract cannot be ratified without the explicit provable/attested line and audit inventory. It does not enlarge the active subject. |

No finding is classified as a production condition, separate decision,
deferred breadth, or non-blocking defect. The round therefore resolves no
ratifiable proposition.

## Process and evidence status

The required clean-room rival and two distinct reviewer measurements occurred.
The reviewers attacked the actual local `git push` surface, not only a helper
or scanner. The evidence contains only constructed credentials, local dummy
transports, and constructed markers. No artifact cites a real credential,
remote, workspace, or run detail.

## Recommendation and owner decision

**Recommendation: do not ratify H1 and do not open an automatic repair.**
The single repair pass permitted by Gate 4 must be owner-authorized and bounded
to a testable invariant, not an attempt to rescue both failed shapes.

The smallest plausible repair charter would retain only the incumbent's
descriptor-release family and must prove all of the following from actual Git
transport: (1) the exact outgoing envelope is scanned and accepted *before*
the descriptor exists in the Git child; (2) the fresh probe completes all
clean/raw/`--no-verify`/marker/tamper cases; (3) a same-UID sibling process has
no credential discovery route under the declared, non-malicious local-process
threat; and (4) H2's named owner-attested server control plus H3's enumerated
E18.1/E18.2 battery are written as the honest implementation boundary.

If that invariant cannot be made testable without a new operating-system,
identity, or hosted-service boundary, classify that need as a **separate
decision** rather than enlarging H1 by repair. The owner may instead stop H1
at this evidence and select a different hardening approach. No builder or
reviewer is authorized until the owner chooses one of those outcomes.
