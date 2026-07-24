# 03 — Process Roles

Advice, partly speculative. Economy touched only briefly (see `04-economy.md`).

## Observed role set (all cycles)
Foreman (1) + rival builders (2) + reviewers (2), per cycle. All builders/reviewers
Sonnet/Medium. Owner = Tier-3 director + human-eye reviewer (rarely invoked).

## Observed inefficiencies
- **Undifferentiated reviewers** — both applied the same lens; redundant coverage on settled axes, thin coverage on novel ones.
- **Rivalry decayed on convergence** — builds diverged sharply C1–C2, near-identical C4–C5; second builder bought little late-stage signal.
- **Foreman serial-carries context** — unbounded growth; single-threaded bottleneck across the whole arc.
- **Reviewers re-derived the check rig** each cycle (see `04`).

## Suggested stage-keyed role assignment (milestone arc = explore → converge → verify)
| Stage | Builders | Reviewers | Harness |
|---|---|---|---|
| **Explore** (new property, open space) | 2 rivals (High) | 2, differentiated: adversary/technical + information-design | seed/absent |
| **Converge** (property known, refining) | 1 (Medium) | 1 specialized | run for settled criteria |
| **Verify** (settled) | 0 | 1 thin (novel/perceptual only) | full battery (auto) |

Rationale: rivalry earns its cost only where the design space is open; once
builds converge, the marginal rival is waste. Reviewer specialization matches the
diverged heuristic classes (technical vs communication) instead of duplicating.

## Personas the work implies
- **Clerk / harness-provisioner (Economy)** — isolation setup, fixture serving,
  harness execution, output collation. Removes plumbing from builders/reviewers;
  ADR-0013 already permits an Economy/Medium clerk.
- **Adversary/technical reviewer** — tamper + fault injection + honesty invariants;
  **thins** as the harness absorbs its mechanizable share.
- **Information-design reviewer (High)** — communication-layer judgment
  (see `07-information-design.md`); the reasoning-heavy seat that does not mechanize.
- **Foreman** — bound own context by re-entering from the cycle log (shed raw
  agent returns); steward tier-down as convergence rises.

## Tier note
Medium (Sonnet) builders/reviewers were sufficient across all five cycles; the
loop worked without High-tier. Escalate only for genuinely novel judgment
(information-design seat, new-property exploration). Do not default to High.
