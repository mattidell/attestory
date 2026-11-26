# Draft ADR — Members who share a recorded label are told apart by entry order

- Status: **proposed** (P0 draft; not filed; it gets the next free number when
  the owner accepts it)
- Tier: 2. A presentation-projection contract that later content is
  written against.
- Date: 2026-11-25

## Context

ADR 0087 lets the question walk follow a blocked roster member and labels
each member's question with the member's recorded label (`memberLabel`), "one
reason per member". The walk records a member's question by
`(fact type, label)` (`presentation_projection.py:1028`, `:1038`), so members
with the same recorded label collapse into one reason. On v107, two children
both recorded as "Demo Sam" and both missing the age answer get one question
on the 9 lines it blocks; two missing different answers get two reasons both
headed "Demo Sam"; one missing gets "Demo Sam" with no way to say which.
An entity's only recorded attributes are its id, kind and label
(`entity.v1`), and a label is never empty, so the label cannot be made
unique from what the filer entered, and an id must never be shown.

Evidence: `docs/phases/engine-breadth/milestones/same-label-members-evidence/p0.md`.

## Decision

1. **One reason per member, keyed by the member.** The walk records a
   member's question by the member's subject keys, not its label, so each
   member missing an answer gets its own reason. This is what ADR 0087
   Decision 2 already requires.
2. **A shared label carries the member's place in entry order.** When another
   current entity of the same kind has the same recorded label, the member's
   reasons carry one new optional reason field, `memberOrdinal`: the member's
   1-based position among those entities in the order the workspace
   introduced them. It is present only beside `memberLabel`, and absent when
   the label is unique within the kind. The page shows it with the label
   (for example "Demo Sam (the second one you added with this name)").
   `memberLabel` stays the recorded label.
3. **Explanation only.** As ADR 0087 Decision 3: no reads, pins,
   dependencies, values, refusal codes, question groups or answer targets
   change, and no published schema version changes (the `presentation-model`
   schema does not constrain reason entries; the projection's validator
   admits the field). A return whose members have distinct labels is
   unchanged.

## Consequences

The same-label-members Track 1 changes `_RosterMembers`,
`_closure_question_reasons` and `_validate_resolved` in
`packages/derivation/presentation_projection.py`, the reason prefix in
`packages/presentation/pages/citation-walk.v1.html`, and the mirrored prefix
in `tools/sale_page_observation.py`. Saved pages of returns with two
same-named members on one roster gain the second member's reasons and the
ordinal; the 775 recorded lists are unchanged (P0 replay). A member replaced
by a successor entity moves to the end of the entry order.

## Links

- Plan: `docs/phases/engine-breadth/milestones/same-label-members.md`
- Evidence: `docs/phases/engine-breadth/milestones/same-label-members-evidence/p0.md`
- ADR 0087 (question walk follows roster members), ADR 0046 (presentation
  surface contract)
