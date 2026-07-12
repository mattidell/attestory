# Charter: Iteration 3 — SC-P1 Rung-2 Enforcement Repair

Date: 2026-07-12. Foreman-issued after owner ratification of round-1 triage.
This is the plan's single owner-authorized repair pass, assigned to the original
it1 builder for continuity.

- **Branch:** `prototypes/source-completeness/it3`
- **Evidence rung:** 2 — validator/resolver mutations only. No throwaway
  evaluator (rung 3), persisted integration (rung 4), or production edits.
- **Builder seat:** original it1 builder, High tier (high effort). Tier remains
  High because the repair must compare two rival authority shapes at a defect
  boundary that previously escaped paper review.
- **Proposition:** SC-P1 affirmative-only enforcement only. SC-P2 is partially
  disposed to the rival statement-instance candidate; SC-P3 is deferred. Do
  not redesign or implement either.

## Single question

Can each surviving adopted mapping shape project closed membership through a
validator/resolver boundary only from one exact, current closure finding whose
value is literal boolean `true`, while rejecting false, absent, displaced,
ambiguous, and caller-injected authority and retaining the exact finding needed
for explanation pins—without a presence-only adapter?

## Inputs

- Approved `plan.md`, ADR-0011/0012, governance set, and this charter.
- Both preserved paper exhibits:
  `exhibits/source-completeness/it1` and
  `exhibits/source-completeness/it2`.
- Round-1 reviews and `round-1-triage.md` as measured constraints, not as
  invitations to expand scope.
- Current production `collect`, `RunContext`, and pin seams for grounding only.

## Deliverables

All work stays under `docs/prototypes/source-completeness/it3/`, plus
`examination-it3.md` (≤ 200 lines):

1. Minimal validator/resolver mutations for the dedicated-mapping-citizen
   shape and the embedded-adopted-parameter shape. Shared mechanics may be
   factored once, but each authority shape must be independently exercised.
2. Executable tests or deterministic mutation cases for:
   - exactly one current literal-true finding → admitted;
   - current false, absent, and displaced historical true → blocked;
   - ambiguous/duplicate mappings or matching closure findings → blocked;
   - caller-supplied membership injection → rejected or unrepresentable;
   - admitted membership retains the exact closure-finding identity used by
     explanation pins.
3. A presence-only mutant that would admit on finding existence must be killed
   by the false-closure case for each shape.
4. `examination-it3.md`: commands/results, evidence paths, every negative
   result, and one disposition—SC-P1 enforcement settled at rung 2 or the
   precise reason rung 3 is still needed.

## Pre-declared checks

1. No mutation accepts `false`, absence, displacement, or ambiguity.
2. Presence-only mutants fail deterministically for both authority shapes.
3. No caller-controlled bare set can augment resolved closed membership.
4. The exact admitted closure finding, not merely a family string, survives
   resolver output for pins.
5. Changes remain prototype-only and do not execute the production evaluator.
6. SC-P2, SC-P3, SC-D1, production schemas, and coverage remain untouched.

## Stop conditions

Stop after rung-2 evidence. A need for the real two-layer evaluator becomes a
finding recommending rung 3; it is not authorization. Any new SC-P3 claim or
identity issue is recorded as deferred and does not enter this repair pass.
