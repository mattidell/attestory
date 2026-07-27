# Charter — Track 1 decision review: ADR-0047 Live Viewing Environment

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Milestone: `docs/phases/real-return/milestones/presentation-live-viewing-boundary.md`
- Branch: `track/presentation-live-viewing-boundary-track1`
- Commit under review: `498c396`
- Author: Foreman. You are author-independent. Preserve fresh-reader
  independence: form your own reading of the sources before accepting any
  framing in this charter.

## Subject

One decision record and its companion analysis:

- `docs/adr/0047-live-viewing-environment.md`
- `docs/adr/analyses/0047-live-viewing-environment.md`
- the `0047` row appended to `docs/adr/INDEX.md`

No code is in scope. Track 2 has not been chartered.

## Sources

- `docs/adr/0044-live-run-system-boundary-and-trust-domains.md`
- `docs/adr/0031-real-data-residency-boundary.md`
- `docs/adr/0046-presentation-surface-contract.md`
- `docs/phases/real-return/maturity-matrix.md` (footnotes 5, 7, 8)
- `docs/phases/real-return/milestones/presentation-live-viewing-boundary.md`
- `tools/presentation_harness/lib/chrome.mjs` (the existing launch posture the
  ADR characterizes)
- `AGENTS.md#Data Safety Rules`

## Measurements

`READY` requires all five to pass.

1. **Derivation.** Every claim derives from accepted decisions and completed
   records. The ADR introduces no new evidence, consults no real workspace, and
   asserts no experimental result. In particular, verify the Class C conclusion
   is presented as resting on the Guarded Transport records plus a platform
   limitation — **not** as a general impossibility theorem across isolation
   substrates, which ADR-0044 explicitly declines to claim.

2. **Classification totality.** The four classes cover the viewing session with
   no unclassified remainder, and the stated default for an unrecognized channel
   is to block. Probe for a channel the classification misses or that could be
   argued into two classes at once. Assess in particular whether any Class A
   item is doing concealment work that belongs in Class B — that is, whether
   something the vehicle *could* control has been filed as an irreducible human
   residual.

3. **Attestation containment.** The stated attestation stays within ADR-0031
   Decision 7 and adds no descriptive content. Its five honesty conditions are
   checkable statements rather than sentiment, and the ADR is explicit about
   which of them are owner knowledge rather than mechanism.

4. **Claim discipline.** The Class C disclaimer is stated plainly, not implied,
   and nothing in the ADR, analysis, or INDEX row can be read as claiming
   mechanical egress prevention. Confirm the ADR selects no enforcement
   substrate and lifts no maturity row: Presentation must remain L2 and the data
   boundary L3.

5. **Precondition disposition soundness.** Independently assess the decision
   that residency backup inclusion and content indexing are **refusals** rather
   than disclosed risks. Test the reasoning both ways: is a content index or
   backup copy correctly characterized as a completed crossing under ADR-0031
   Decisions 2 and 7, and is the stated owner remedy real? A finding that this
   should instead be a warning, or that the remedy does not exist on the
   platform, is in scope and blocking.

## Data safety

The ADR and analysis must contain no residency locator, path fragment, or
owner-local identifier. Confirm the locator-confinement decision is stated as a
requirement on diagnostics, not left to implementation. Run
`python3 tools/envelope_scan.py --range main..HEAD`.

## Verdict

Return `READY` or `NOT READY` with the smallest exact residual. The plan allows
at most one findings-only repair plus a focused recheck.

Record the review at
`docs/reviews/2026-07-26-presentation-live-viewing-boundary-track1-review.md`.
