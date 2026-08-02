# Committee Round 1 — Rival Paper Designs

Date: 2026-07-12. Foreman-assembled under the approved plan.

## Scope

Measure the two clean-room paper designs against the same charter and with
attack parity. This round does not authorize a rung climb, repair, production
work, or scope expansion.

## Exhibits

- Incumbent: `exhibits/source-completeness/it1`
  - `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-completeness/it1/`
  - `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-completeness/examination-it1.md`
- Rival: `exhibits/source-completeness/it2`
  - `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-completeness/it2/`
  - `docs/archive/2026-08-02-milestone-artifacts/prototypes/source-completeness/examination-it2.md`

Both designs answer `charter-it1.md` / `charter-it2.md` at evidence rung 1.
Reviewers may inspect production seams cited by either design only to test a
claim against current behavior; they must not propose production changes as
part of this round.

## Measurements

- Governance reviewer: run every check declared in
  `roles/reviewer-governance.md` against both designs. Failure is a cited
  governance/ADR conflict, missing required instance, unexplained authority,
  broken pin path, or scope/rung breach.
- Adversary reviewer: run every attack declared in
  `roles/reviewer-adversary.md` with equal effort on both designs. Failure is a
  concrete path or fixture under which a design violates its declared
  contract; failed attacks must also be recorded.

## Outputs and independence

- Governance: `reviews/round-1-governance.md` (≤ 150 lines).
- Adversary: `reviews/round-1-adversary.md` (≤ 150 lines).
- Reviewers work in isolated contexts and must not read the peer's output or
  commit-message body before submission.
- Findings recommend only. The foreman classifies every finding under Gate 5
  after both reviews land.
