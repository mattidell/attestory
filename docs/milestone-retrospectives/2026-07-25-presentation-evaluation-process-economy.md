# Retrospective — Presentation Evaluation Process Economy

Status: **final — closed early by owner direction; closeout PR #68 merged as
`a14e8bf` on 2026-07-25.** This is a successful foundation and an
intentionally incomplete execution of the original plan, not a claim that all
planned tracks or exit criteria passed.

## Milestone

- Planning unit: PR #65, merged to `main`.
- Accepted implementation: Track 0, PR #66, merge commit `870c8ed`.
- Closeout records: PR #68, merge commit `a14e8bf`.
- Rejected implementation: Track 1 on
  `track/presentation-economy-t1-harness-core`; independent review returned
  `NOT READY`, and the branch was not merged.
- Tracks 2–3: canceled before implementation.
- Maturity effect: none. No product presentation surface, ADR, or matrix cell
  was added or raised.

The owner stopped after the evidence answered the milestone's practical
question: the project has enough foundation to observe and compare the economy
of actual presentation milestones, while perfecting a general harness now
would spend more before a real presentation workload demonstrates the need.

## Shipped

Track 0 provides the durable presentation-economy foundation:

- strict, versioned presentation workload, observation, and comparison data;
- a machine-readable C1–C5 historical baseline that preserves approximate and
  missing values rather than reconstructing them;
- quality-before-cost comparison with workload and seeded-defect checks;
- participating-role completeness so omitted work cannot masquerade as
  savings;
- per-measure treatment of missing costs;
- deterministic comparison output; and
- append-by-new-identity plus supersession for later corrections.

Future presentation milestones can now declare comparable work, record bounded
cost and quality observations, compare treatments where evidence permits, and
retain the result. They do not need the rejected general browser harness to use
that loop.

## Verification

The Track 0 measurement-integrity review first returned `NOT READY` on omitted
participant cost. The repair independently reproduced the pre-repair false
economy result, closed it, and its delta review returned `READY`.

The accepted Track 0 record reports:

- 27 focused presentation-economy tests passing;
- 590 full unittests passing;
- mypy passing over 114 source files;
- governance lint conformant;
- envelope scan clean;
- two comparison runs byte-identical; and
- the historical baseline validating exactly.

PR #66 merged as `870c8ed`. The repository's authoritative CI `verify` workflow
was introduced later in PR #67, so PR #66 has no retrospective `verify` check
to cite. Closeout PR #68 passed `verify` and merged as `a14e8bf`.

Track 1's independent review reran 27 Node tests, the real-Chrome smoke, the
then-current full Python/mypy/governance/envelope floor, and additional
synthetic adversarial cases. Passing positive evidence did not overcome six
failure-integrity blockers; the implementation therefore did not merge.

## Decisions

- **Owner scope decision:** stop after the accepted Track 0 foundation; do not
  fund a Track 1 repair/re-review cycle before beginning actual presentation
  work.
- **Tier 1 process application:** retain the Track 1 review as negative
  evidence and retire its prepared repair/re-review prompts unexecuted.
- No Tier 2 or Tier 3 architecture decision and no ADR.

## Deviations

The original plan had four tracks and 15 exit criteria. At close:

- Exit criteria 1–3 are established by accepted Track 0.
- Criterion 14 held for all committed material.
- Criterion 15 is discharged by this retrospective.
- Criteria 4–13, to the extent they require an accepted harness, standing
  corpus, pilot, operating integration, or every planned track passing, are
  explicitly **not met**.

Track 1 was not close enough to acceptance to count as a partial harness
capability. Its six blockers were cross-tuple storage leakage, malformed
injection becoming a false pass, launch-time signal cleanup leakage, manifest
path traversal and invalid provenance, incomplete strict validation including
vacuous empty-matrix success, and raw rejected-input echo on stderr.

The prepared repair and delta-review charters are retained only to show the
repair that was considered. They authorize no later implementation by
themselves.

## Economy findings

- The Track 1 Reviewer made 41 tool calls across 42 response turns, including
  14 Chrome/adversarial probes, 12 harness invocations, and 11 Chrome launches.
- Browser work was command-line batched CDP automation. Browser output was
  comparatively small; the committed smoke was about 1.5k output tokens.
- Three context reads each returned roughly 10.9k–11.7k tokens, and several
  implementation reads returned roughly 4k–6.5k. Exact total tokens and money
  were unavailable and remain unknown.
- Directly timed command execution was about 160 seconds within 751 seconds of
  foreman-observed dispatch-to-interruption time. The remainder cannot be
  apportioned exactly among reasoning, reading, latency, and writing.
- The costly part was not granular browser clicking. It was high-effort
  adversarial case construction and interpretation, amplified by large context
  ingestion.

## Review-learning disposition

The current findings yield a reusable adversarial set:

1. isolate the actual state scope, not merely the target or tab;
2. distinguish registration/acknowledgement from execution;
3. establish cleanup ownership at resource acquisition and attack every
   cancellation boundary;
4. canonicalize and confine paths before reading or emitting provenance;
5. reject missing, unknown, wrong-type, out-of-range, and empty/vacuous
   contracts; and
6. expose only closed reason codes and fixed redacted messages.

Several were already present in the preceding exploratory findings, especially
execution over self-claim, browser-isolation topology, live fault injection,
and rejected-value echo. Merely requiring agents to read prose did not prevent
recurrence.

The promoted foreman discipline is therefore operational: before every build
or review, map prior applicable findings into shared invariants and executable
checks. The Builder closes known classes. Mechanical checks carry their
regression burden. The Reviewer receives the same map plus an explicit novel
boundary to probe. Ensuring the two seats cover new ground is part of foreman
scope-and-economy stewardship.

## Data safety

All accepted datasets, fixtures, reports, and review attacks are synthetic and
repository-relative. No real workspace, personal return output, credential,
remote page, owner browser profile, or quarantined run detail was consulted or
committed.

## Follow-ups

- Select and plan the first actual Presentation-frontier milestone toward a
  human surface.
- Use the Track 0 declare → observe → compare → retain contracts from the
  beginning of that milestone, while treating unavailable measures honestly.
- Turn applicable known adversarial findings into pre-build acceptance checks
  before chartering an expensive independent review.
- Build only the smallest workload-specific mechanical helper justified by
  the selected presentation work. Do not revive the rejected Track 1 harness
  as a prerequisite.
- If a general harness is reconsidered after repeated real-workload demand,
  start from the preserved blocker set and require a new plan/review unit.

## Planning lessons

A process-economy milestone can succeed at creating an observation foundation
without proving its first proposed intervention economical. The correct
response to an expensive, rejected intervention is not automatically a repair;
it is to ask whether the foundation is already sufficient to measure the next
real workload.

Reviews need both a regression boundary and a novelty boundary. A reviewer who
must rediscover known classes is doing necessary work under a poor allocation.
The foreman should make known findings executable before build, give them to
both seats, and reserve high-effort independent review for the unproven part.
