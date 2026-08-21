# Grammar Census — Engine Language Map: Final Report

Filed by the Foreman 2026-08-20 on milestone completion. Audience: owner.

Full evidence chain: `docs/phases/grammar-census/inquiries/` (seven files),
`docs/phases/grammar-census/exit-criteria-assessment.md`,
`docs/reviews/2026-08-20-grammar-census-foreman-correction-5b-ii-ruling-reasoning.md`.
This report is a summary with pointers, not a substitute for those files.

## What language the engine actually has

Two expression grammars, not one, sharing no operators and evaluated by
different modules:

- The **primary language** — `add`/`subtract`/`multiply`/`divide`/`collect`/
  `count`/`choose`/`round`/`range_lookup`/`bracket_fold`/`categorical_compare`/
  etc. — declared across `rule-artifact` and `operation-semantics` schema
  versions, dispatched by `evaluator.py`'s 23-op chain, and used across all
  134 primary 2025 rule-artifacts.
- A **second, nested grammar** — `term`/`predicate` with `left`/`right`/
  `args`/`value` — declared in `source-family.v2` `$defs/term` and
  `$defs/predicate`, evaluated separately by `declarative_validation.py`,
  used for `member_constraints` and `identity_exclusivity` well-formedness.

Both are gated at package admission, both are versioned, both are content
(not schema alone). 166 constructs were reconciled across them: 157 active,
7 unused, 1 legacy-only, 1 apparently unreachable. The engine's own account
of "the grammar" undercounted itself — the second grammar's location gave no
hint it existed, and finding it took a third independent reader.

## The most consequential agreements, mismatches, and unknowns

**Most consequential finding: a published contract is not enforced as
written.** ADR-0066 decision 2 states "Resolver admission rejects predicate
depth greater than six." It does not, for any term tree nesting through
`left`/`right`/`value` rather than `args` — which is every arithmetic and
comparison tree. Only the evaluator enforces the bound. This was caught by
running two independent depth-computation code paths against the same
synthetic input and watching them disagree; it also **falsified the stated
reasoning of a ruling I made** during Track 0, which is now corrected on the
record without moving the affected construct's label.

**Second: two published schema files claim one identity.**
`attachment-rule.v5.schema.json` declares `"$id": "tax/attachment-rule.v3"`
— the same `$id` as the actual v3 file, with different bytes. The instance
discriminator resolves to v3; v5's content is unreachable by any production
path. No content hosts v5.

**Mismatches of a lesser but real kind:** `_bracket_fold` binds its declared
canon spec and never reads it again — 95 committed uses of an operation whose
declared spec does not govern its arithmetic. `loader.OPERATION_VOCABULARY`
(14 ops) is dead code next to the evaluator's 23. `truth_table` has no reader
anywhere in `packages/derivation/`.

**Genuine unknowns, left open rather than guessed at:** whether
`selected_producer` should be made the runtime tie-break winner it currently
is not; whether the `_predicate_depth`/evaluator split should be closed by
making admission walk more keys (a code change, out of this milestone's
scope either way); the full taxonomy of what the 216 distinct `ref` names
denote as store kinds.

## Whether the census is reliable enough to close

**Yes**, with one caveat stated plainly. Reliability here doesn't mean zero
errors — it means errors surface and get corrected rather than propagate
silently, and this census demonstrated that property on itself, twice. Track
0's own boundary corpus needed five repair rounds, two of which were found by
a builder using source over my charter text. My own round-3 ruling was later
falsified by evidence the milestone's own Track 2 produced, and that
correction is on the record rather than absorbed. A method that catches its
own author's error, using evidence produced downstream of the error, is
doing what it's supposed to do.

The caveat: verification was **sampled**, not exhaustive. I independently
re-checked roughly a dozen specific claims across seven deliverables — every
one held — but 166 constructs and nine tension entries were not each
individually re-derived by me. The census's own discipline (spot-check
three-way agreements, don't trust consensus) is the same discipline I applied
to it; neither is total coverage.

## The strongest case against its conclusions

Three lines an owner could reasonably press on:

1. **The primary criterion for "grammar proper" was amended mid-milestone to
   fit a ruling, and the ruling's own reasoning was later shown false.** The
   label survives under the amended criterion for reasons independent of the
   false reasoning — but a skeptical reader could argue the amendment itself
   was contaminated by wanting a particular answer, not just the sentence
   that got struck. The map states this risk explicitly rather than hiding
   it; that doesn't resolve it.
2. **Track 1c's "observed usage" reflects one snapshot's committed content**,
   134 primary rule-artifacts at one commit. Frequency claims ("368 uses,
   all `cmp: eq`") are true of that snapshot and could look different after
   the next tax year's content lands. Nothing in this census is a claim about
   the future.
3. **The comparison brief's external-system characterizations are recollection,
   not verification**, and are marked as such — but a reader skimming past
   the markers could still walk away trusting a DMN or Catala claim this
   milestone had no way to check.

## Bounded choices for what follows

The phase stays open; this milestone selects nothing. Four live options,
not mutually exclusive:

- **Comparative review**, scoped to the seven dimensions in
  `track-3-comparison-brief.md`, each already tied to a specific question and
  a specific census artifact rather than a general survey.
- **A focused grammar or code decision**, on one of the tension catalog's
  contract-versus-enforcement entries (T1 predicate depth, T2 the `$id`
  collision) — these are the ones where the project currently believes
  something about itself that isn't true.
- **Further internal verification**, closing the eight surviving Track 2
  open questions or extending my sampled verification toward exhaustive.
- **Stop here for the phase.** The eight exit criteria are met; nothing
  requires this milestone to produce a redesign or a recommendation, and it
  produces neither.

**"Stop here" closes the milestone. It does not close T1, T2, T5, or T8.**
These four tension-catalog entries are governance-relevant defects,
independently reverified against source and dispositioned at
`docs/reviews/2026-08-20-grammar-census-governance-disposition-advisor-
review.md`: T1 is an open product-contract implementation defect (ADR-0066's
admission-depth bound is not enforced as written) unless ADR-0066 is
superseded; T2 is a Canon/identity conformance defect under ADR-0003 (two
published schema files claim one `$id`); T5 is an ADR-0006 conformance
defect and a legibility hazard (`bracket_fold`'s declared canon spec is
loaded and never read); T8 is a locus-of-meaning conflict awaiting an owner
call (tax-specific exclusivity axioms live as unversioned Python rather than
declared package-language content). Choosing "stop here" for the phase
leaves all four open on the record rather than resolving them by omission.
