# Milestone: Correction Authority and Marshaller Simplification

Status: **draft — awaiting owner approval** (drafted 2026-07-22 in the
foreman seat at owner request; ADR-0013 requires owner approval of this plan
before any charter is cut). Fourth milestone of the Real Return phase;
operates under ADR-0030 per-ADR / per-track merges and ADR-0034
owner-approved dispatch. This is the phase's second **hardening (L3→L4)**
milestone: the first, Guarded Transport and Credential Confinement, stopped
its H1 topic unratified and was succeeded by the honest-L3 rescope
`push-envelope-preflight-and-bypass-visibility.md`; this milestone does not
reopen that topic.

## Decision summary (tiered)

- **Tier 2 (default + veto): the correction-authority contract.** Today any
  actor supersedes any finding without restriction
  (`dividends-schedule-b-slice-deferral-ledger.md` entry 13, carried since
  the First Real Return Slice). Default proposed: a closed, named vocabulary
  of which actor/role may supersede which fact family, enforced as a
  validation gate on the existing supersession mechanism — not a new UI, a
  contract constraint. This is a genuine new contract (it touches every fact
  family's correction path), so it earns its own ADR, but does not need a
  rival-prototype cycle: the shape is closed-vocabulary-plus-predicate, the
  same pattern ADR-0006 (pin-role vocabulary) and ADR-0016 (closure claims)
  already established. Gate 0 confirms whether any part of this needs a
  prototype; the default assumption is no.
- **Tier 1 (log only): marshaller binding-route simplification.**
  `packages/derivation/marshal.py` has grown a fourth binding route
  (deferral ledger entry 8, re-affirmed and grown at every track that has
  touched the file since the Dividends and Schedule B Slice). Bounded
  refactor: no contract change, no schema change, one implementation track.

## Why this milestone

Two named deferrals have been carried and re-affirmed across multiple prior
milestones without ever being scheduled as the primary object of a track.
Both are genuinely hardening (not new tax content), both are bounded, and
both are ready to execute now — unlike the other L3→L4 hardening candidates:
ADR-0026's further interest sources and subtractive-adjustment mechanism are
new domain content wearing a hardening label (they need their own Tier 3
contract decision and rival evidence, not a cleanup track), and ADR-0028's
historical-v1 migration has no real migration need yet. Scoped narrow per
owner decision 2026-07-22.

## Non-goals

- No ADR-0026 interest-source or subtractive-adjustment work — that is a
  future domain-breadth or hardening milestone in its own right.
- No ADR-0028 historical-v1 migration.
- No new tax domain, schedule, or presentation surface (E8.1 / citation
  display stay on the frontier).
- Does not reopen guarded transport / credential confinement (deferral
  ledger entries 1 and 2 stay exactly as recorded — untouched by this
  milestone).

## Scope

1. **Track 0 — correction-authority contract (Tier 2 ADR).** Define, as a
   closed vocabulary, which actor/role may supersede a finding of a given
   fact family. Predicate-based, consistent with the existing pin-role
   pattern (ADR-0006) and closure-claim pattern (ADR-0016). No rival
   prototype required unless Gate 0 finds otherwise.
2. **Track 1 — enforcement.** Implement the contract as a validation gate on
   the supersession mechanism. Regression goldens prove an unauthorized
   supersession is rejected and an authorized one still succeeds, including
   at least one multi-family boundary case.
3. **Track 2 — marshaller simplification.** Collapse the fourth binding
   route in `packages/derivation/marshal.py` into its intended shape without
   changing the existing `current_findings`-only read semantics. Regression
   suite proves no behavior change across all four routes' existing callers.
4. **Track 3 — records.** Retire deferral-ledger entries 8 and 13 by name;
   update maturity matrix footnote 6 (free supersession policy); rewrite the
   phase-state briefing's shims-in-place paragraph.

## Contracts

### Existing (build on, do not reopen)

ADR-0006 (pin-role closed vocabulary), ADR-0016 (closure claims, family
subtotal declaration), ADR-0030/0034 (process), the existing supersession
mechanism (entity supersession act, record-only displacement — Foundation
kernel), and `packages/derivation/marshal.py`'s existing four binding routes
(all read exclusively from `current_findings`; that off-record property must
continue to hold after simplification).

### Decided here

The correction-authority contract (Track 0) — a new closed-vocabulary ADR,
owner-ratified, no prototype cycle assumed unless Gate 0 finds a genuine
rival-design question.

## Verification

- Full in-repo suite, mypy, governance lint stay green throughout.
- Track 1: goldens proving rejection of an unauthorized supersession attempt
  and success of an authorized one, across at least two distinct fact
  families.
- Track 2: full regression across all existing callers of the four (soon
  fewer) binding routes; no change to `current_findings`-only read semantics
  — an explicit assertion, not just "tests still pass."
- No real data, credential, or live-run detail is required or permitted by
  any test in this milestone (it touches no boundary or transport surface).

## Exit criteria

1. Correction-authority ADR ratified; supersession is rejected when the
   actor/family predicate fails and accepted when it holds.
2. The marshaller has one binding-route shape per requirement, not four
   routes carrying redundant logic; `current_findings`-only read semantics
   provably unchanged.
3. Full suite, mypy, governance lint green.
4. Deferral-ledger entries 8 and 13 retired by name in the next ledger;
   maturity matrix footnote 6 updated; phase-state briefing rewritten.

## Tracks

Per ADR-0030, each track is its own short-lived branch with its own review
gate and no-ff merge; dependency order (Track 1 depends on Track 0's
ratified contract; Track 2 is independent; Track 3 depends on both).

### Track 0 — Correction-authority contract

Draft and ratify the closed-vocabulary ADR. Owner-approved; Gate 0 reports
whether any part of this needs a rival prototype before the ADR is drafted.

### Track 1 — Enforcement

Implement the validation gate once Track 0 ratifies. Independent pre-merge
review.

### Track 2 — Marshaller simplification

Independent of Track 0/1; may run in parallel. Independent pre-merge review
focused on regression proof, not just green tests.

### Track 3 — Records

Retire the two ledger entries, update the matrix footnote and phase-state
briefing. Runs after Tracks 1 and 2 both merge.
