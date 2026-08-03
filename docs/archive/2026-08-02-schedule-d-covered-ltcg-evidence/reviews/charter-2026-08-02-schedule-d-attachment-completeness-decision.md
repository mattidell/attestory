# Schedule D Attachment Completeness-Violation Semantics — Decision Unit Charter

Audience: Builder (paper-spike + ADR draft, not implementation)

Status: **chartered for owner launch** (approved 2026-08-02)

## Why this exists

Track 2 landed (`37b4426`, `milestone/schedule-d-covered-ltcg-8a-continuation`)
with a flagged, not-allowlisted production condition: the Schedule D
attachment's own `required-and-complete`/`required-and-incomplete`
disposition uses ADR-0036 Decision 4's generic completeness check, which
validates only *presence* of the seven absence declarations, not their
*value*. A declared `"yes"` on a disqualifying condition (which should make
the class ineligible) is still "present," so the attachment's own
disposition can read `required-and-complete` while the numeric route is
correctly blocked. `rule.selected-preferential-base` independently
re-checks declaration values and goes inapplicable on a violation, so no
numeric result is wrong — but the attachment citizen's own disposition is
inconsistent with the route it gates, which breaks the explanation walk's
honesty property (ADR-0036 Decision 1: "never silence").

ADR-0036 Decision 4 was designed for Schedule B, where every branch-adding
answer only ever *adds* required facts (a `"yes"` on foreign-account adds
7b-country to the required set). It has no concept of a value that should
itself *block* completeness. ADR-0036 also states "generalization is
load-bearing... a future schedule instantiates this ADR with content only"
— so this gap is not Schedule-D-local; any future schedule with an
eligibility-gating declared-absence fact (the ADR-0038 pattern, e.g. its
Decision 5 contradiction interlock) will hit the same hole.

## Gate 1 — eligibility score

- Future blast radius: **2** (every future schedule instantiating ADR-0036
  with an eligibility-gating declared-absence fact inherits the gap).
- Migration cost: **1** (additive only; ADR-0036 is not edited in place).
- Residual paper uncertainty: **2** (no existing citizen models
  "presence-satisfied but value-violates" as a distinct disposition from
  "absent"; ADR-0038 Decision 5's contradiction interlock is the nearest
  precedent but is an admission-locus hard error, not a completeness
  disposition — unclear which pattern this should follow).
- Inability to test cheaply: **1** (payload/disposition shape, not a new
  evaluator primitive — testable on paper).

**Total 6 — prototype-eligible by the letter of Gate 1, but this charter
scopes it to Gate 1's paper-spike-plus-ADR-draft rung deliberately**: the
uncertainty is about which of two known, already-ratified patterns
(ADR-0036's presence-check generalization, or ADR-0038 Decision 5's
admission-locus contradiction interlock) the fix should extend, not about
an unexplored mechanism. If the paper spike (Gate 2) shows the two
alternatives are not paper-distinguishable, escalate to a full prototype
round rather than forcing a premature ADR draft.

## Scope

1. State the exact gap as a producer → authority → consumer → failure map:
   which citizen produces the seven declarations, which rule/attachment
   authority reads them for completeness, which downstream consumers
   (attachment disposition vs. `selected-preferential-base`) diverge today,
   and the precise failure mode (attachment reads complete/published while
   the numeric route is blocked).
2. Two positive instances (declaration correctly absent/satisfied; both
   citizens agree) and two meaningful negatives (a declaration violated;
   the attachment and the numeric route currently disagree) per Gate 2.
3. One lifecycle trace: declaration contributed → attachment completeness
   evaluated → violated → later corrected → both citizens converge.
4. Evaluate the two candidate extensions on paper:
   - extend ADR-0036's completeness check with a value-conditioned
     disposition (new reason code / new atomic disposition state,
     additive to the ratified triad, never edited in place), or
   - reuse ADR-0038 Decision 5's admission-locus contradiction-interlock
     pattern (hard error at the declaration boundary rather than a
     completeness-time distinction).
5. Draft a proposed successor ADR (do not edit ADR-0036 or ADR-0038 in
   place) capturing the chosen extension, its production conditions, and
   which citizens it is owed to.

## Non-goals

No code, no schema, no content changes, no test/golden changes. This is a
paper-and-ADR-draft unit only. No Track 3 work. No re-litigation of
ADR-0036 Decision 1-3 or ADR-0038 Decisions 1-4.

## Stop conditions

Stop and report if: the two paper alternatives are not distinguishable on
paper (route to full prototype per Gate 1's own escalation clause); the fix
cannot be expressed additively (would require editing ADR-0036 or ADR-0038
in place); or the gap turns out to already have a committed resolution
elsewhere in the codebase.

## Deliverable

One proposed ADR draft (numbered successor, e.g. `docs/adr/0055-*.md`,
status **proposed**, not accepted) plus its paper evidence (Gate 2 rung),
for owner review and ratification. Implementation is a separate,
subsequent unit once the owner ratifies.

## Full reads before acting

`docs/adr/0036-schedule-attachment-ontology.md`,
`docs/adr/0038-qdcg-worksheet-and-declared-absence.md`,
`docs/adr/0037` (conditional_dependency_set, for the admission-locus
pattern's generic capability precedent), `docs/adr/0052`, `0053`, `0054`,
`packages/content/tax/2025/attachment.schedule-d.json`, the commit message
of `37b4426` in full, `PROJECT_PLANNING.md` Gates 1-3, `docs/roles/builder.md`.
