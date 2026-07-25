# ADR 0034 — Explicit Owner Approval for Every Foreman Dispatch

- Status: **superseded** by ADR-0043 (2026-07-23)
- Tier: 2
- Date: 2026-07-16

## Context

ADR-0013's reviewer-dispatch amendment treated owner approval of a prototype
plan as standing authorization for the foreman to spawn committee reviewers.
During D3, that distinction proved unsafe operationally: a foreman dispatched
seats from plan-level authorization, then had to interrupt them when the owner
withdrew the launch. A charter is useful preparation; it is not an instruction
to consume a role or begin work.

The owner directed that the foreman role must never dispatch without immediate,
explicit approval. This is a process-control decision, not a change to role
separation, evidence requirements, or the owner's ability to approve a
prototype plan in advance.

## Decision

1. **Every dispatch requires contemporaneous explicit owner approval.** This
   includes builders, committee reviewers, legibility reviewers, clerks, and any
   other sub-agent role. Plan approval, a named role in a plan, a charter,
   silence, an earlier authorization, or a generic instruction to continue is
   never dispatch authority.
2. **Approval is dispatch-specific.** The owner message identifies the topic or
   current stage and role(s) to launch; it authorizes only that immediate event,
   not later rounds, replacement seats, or a different charter.
3. **The foreman prepares but does not launch by default.** It may prepare plans,
   charters, seat records, and review packets without approval. Authorization
   exists only in the active foreman thread; it is not repository state. After
   dispatch, the foreman records the event and exact role/charter in the process
   log. If the direction is ambiguous, it holds or asks; it does not infer.
4. **Reviewer independence remains mandatory.** Once explicitly authorized,
   committee reviewers run in isolated contexts and do not see one another's
   in-progress work. This ADR changes launch authority only.

## Consequences

- The foreman has a hard stop between preparing a role and launching it.
- Owner control is visible at every consumption of agent work, including routine
  committee review.
- Prototype plans name eligible seats and capability tiers but grant no standing
  dispatch authority.
- This supersedes only ADR-0013's 2026-07-12 reviewer-sub-agent-dispatch
  amendment. ADR-0013's economic gates, role separation, rival evidence, and
  confirmation-pass rules remain accepted.

## Links

- Supersedes in part: ADR-0013, "Reviewer sub-agent dispatch" amendment.
- Process definition: `PROJECT_PLANNING.md` (Prototype-Driven Decisions).
- Prototype-foreman doctrine: `PROJECT_PLANNING.md` (Prototype-Driven
  Decisions); milestone role seeds in `docs/roles/`.
- Active-topic correction: `docs/prototypes/production-resolver/process-log.md`.
