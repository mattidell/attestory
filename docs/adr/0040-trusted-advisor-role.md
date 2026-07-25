# ADR 0040 — The Trusted Advisor Role

- Status: **retired** (ADR-0045, 2026-07-25) — history only, not authority. Previously: **accepted** (owner ratification 2026-07-19)
- Tier: 2
- Date: 2026-07-19

> **Retired 2026-07-25 by [ADR-0045](0045-agent-instruction-consolidation.md).**
> Process is the owner's operational domain and is no longer recorded as ADRs.
> This record is retained permanently as history and rationale — cite it for
> *why* a practice exists, never as binding authority. Its still-operative
> content lives in `docs/roles/advisor.md`.

## Context

The foreman seat has bifurcated in practice. Track execution — chartering,
custody, triage, dispatch, verification — runs well at Medium tier on
per-track threads with handoffs, because the operating rules are now
written (ADR-0039 role cores; the handoff Standing-policy block). What the
owner still wants from a long-lived, high-context session is different in
kind: strategic counsel — frontier reading, plan critique, scope calls,
economics judgment — at the handful of moments per milestone where the
decision is the owner's (Tier 3) and its blast radius is large. Keeping a
High-tier foreman resident through execution buys that counsel at the cost
of a 150k-token thread re-read mostly uncached at owner cadence; the
counsel's actual inputs are a small set of durable strategic documents.
This ADR separates the seats so intelligence is bought where it
concentrates.

## Decision

1. **The Advisor is a distinct, stateless, High-tier seat.** It is
   consulted, not resident: each consultation is a fresh session seeded
   from `docs/roles/advisor.md` (the seat file this ADR governs), and it
   ends when the counsel is delivered. Continuity lives in the durable
   record, never in the thread — if counsel was worth keeping, it gets
   written (see decision 5).

2. **Context seed (the strategic set, nothing operational).** The seat
   file directs the Advisor to read, in order: the product thesis and
   phase roadmap; `docs/phase-state.md`; the maturity matrix; the active
   milestone plan; the current deferral ledger(s); the milestone
   retrospectives; and `docs/adr/INDEX.md` (digests only — full ADR text
   on demand). Explicitly **not** seeded: charters, reviews, build state,
   the handoff note, source code. The Advisor pulls any of these on demand
   for a specific question; they are not its resident frame. Target boot:
   ≤ 30k tokens.

3. **Invocation points (owner-initiated, typically 3–6 per milestone).**
   - **Milestone selection** — an independent frontier reading before or
     against the foreman's recommendation.
   - **Milestone-plan approval** — a pre-approval critique: scope shape,
     decision-topic tiering, verification posture, what the plan
     forecloses.
   - **Tier 3 ratifications on request** — a second read of a
     prototype-backed shape when the owner wants counsel beyond the
     committee record, especially where the foreman is structurally
     conflicted (foreman-authored syntheses; scope-and-economy calls where
     the foreman is also the economy steward).
   - **Retrospective review** — which lessons deserve promotion to
     standing policy versus one-time record.
   - **Phase boundaries and process changes** — the largest-radius calls.
   - The Advisor is **not** invoked for charters, triage, repairs, track
     reviews, or anything inside a merge unit; that is committee and
     foreman ground.

4. **Authority: none.** The Advisor decides nothing, dispatches nothing,
   merges nothing, and is not a gate — no process step waits on it. It
   does not overrule the foreman or any committee finding; where its read
   conflicts with the foreman's, both positions go to the owner as
   labeled dissent. It binds itself to the same data-boundary rules as
   every seat (ADR-0031; the attestation form is the only real-run fact
   it may ever see or cite).

5. **Counsel worth keeping gets written or it is lost — by design.** The
   Advisor ends consequential counsel with explicit *promotion
   candidates*: a line for the handoff Standing-policy block, a
   retrospective lesson, a plan amendment, or a proposed-ADR sketch. The
   owner decides what is adopted; the foreman records it. This is the
   capture mechanism replacing long-thread memory.

6. **Tier and economics.** High tier (the named-model map's top row),
   justified by concentration: a few consultations per milestone at ≤ 30k
   boot each, versus a resident high-tier thread re-read uncached across
   dozens of execution turns. ADR-0034 applies unchanged: if a foreman
   spawns the Advisor as a sub-agent it needs owner approval per dispatch;
   the normal mode is owner-launched.

## Consequences

- Execution foremen can run at Medium tier on per-track threads without
  the owner losing a high-judgment counterpart; the counsel function gets
  *more* independent, since the Advisor no longer shares the execution
  thread's framing and sunk context.
- The owner gains a structural second opinion at exactly the moments the
  process has no other independent check on the foreman (selection
  framing, plan shape, foreman-authored syntheses).
- The seat only works if the strategic documents stay honest — a stale
  matrix or ledger now misleads two seats, which sharpens the existing
  duty to keep them current (their freshness checks remain the remedy).

## Alternatives Considered

- **Keep one long-lived High-tier foreman thread.** Rejected on
  economics (uncached re-reads at owner cadence dominate) and on
  independence (the advisor function inherits the execution thread's
  framing).
- **Advisor as a standing gate on Tier 3 decisions.** Rejected: adds a
  mandatory round to every ratification — the cost ADR-0013 exists to
  cut; consultation stays owner-discretionary.
- **Capture judgment by preserving threads or transcript digests.**
  Rejected: unbounded content growth, and implicit judgment was already
  being lost to compaction; written promotion candidates are the bounded
  form.

## Links

- Extends: ADR-0013 (role capability tiers; this adds a named seat),
  ADR-0034 (dispatch gate applies), ADR-0039 (routing and role cores the
  seat file builds on)
- Seat file: `docs/roles/advisor.md`
