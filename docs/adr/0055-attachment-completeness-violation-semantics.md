# ADR 0055 — Attachment Completeness Violation Semantics

- Status: **accepted** (owner ratification 2026-08-02, Tier 2)
- Tier: 2 — narrow, additive schema/representation widening with future
  blast radius (every future schedule with an eligibility-gating
  declared-absence fact inherits the gap), not a product-thesis or
  rival-topology decision.
- Date: 2026-08-02

## Context

Track 2 of the Covered Long-Term Gains, Schedule D Line 8a milestone
(`37b4426`) landed with a flagged, not-allowlisted production condition:
the Schedule D attachment citizen's own `required-and-complete` /
`required-and-incomplete` disposition can read `required-and-complete`
while `tax.us.2025.rule.selected-preferential-base` correctly goes
`inapplicable` for the exact same current facts. No wrong tax number ever
publishes — `selected-preferential-base` independently re-checks the seven
`schedule-d-boundary.*` declarations' *values*, not just their presence,
and blocks every downstream numeric line (7a, 9, 16) on a violation — but
the attachment citizen, whose entire purpose is to be the honest, walkable
account of the form's own completeness (ADR-0036 Decision 1: "never
silence"), misrepresents it.

The root cause is that ADR-0036 Decision 4's completeness check is
presence-only, deliberately and correctly so for the citizen it was
designed against: Schedule B's Part III branch questions, where a `"no"`
answer is a factually complete, non-disqualifying response (a `"no"` on
foreign-account simply omits 7b-country from the required set; it never
itself blocks Schedule B). ADR-0036 Decision 5 states "generalization is
load-bearing... a future schedule instantiates this ADR with content
only" — Schedule D is the first schedule whose completeness genuinely
depends on a declared *value*, not merely a declared answer's *presence*:
each of its seven absence declarations must equal `"yes"` for the bounded
class to be complete, and a present, current, honestly-declared `"no"` is
a real violation, not a valid branch.

The paper spike (a producer→authority→consumer→failure map, two positive
and two negative paper instances, one lifecycle trace showing the
attachment's disposition is invariant across a correction that genuinely
flips real-world eligibility, and an evaluation of two candidate
extensions) is not retained in the repository; its charter (Gate 1 score
6, technically prototype-eligible, deliberately scoped by the owner to a
paper-spike-plus-ADR-draft rung matching the ADR-0053/ADR-0054 precedent
on this same milestone) is likewise not retained. This ADR is grounded in
that paper spike alone — no committee review, no incumbent/rival round.

## Decision

1. **A required answer may check a value, not only presence.** An additive
   successor schema, `attachment-rule.v4`, widens the `required_answer`
   shape's `check` property: alongside the existing `"presence"` (an
   answer counts as satisfied once it exists as a current finding,
   whatever its value — unchanged, and still the correct semantics for
   Schedule B and any future branch-adding declaration), a new `"value"`
   check carries a required `equals` field naming the exact categorical
   value the answer's *current* finding must hold to count as satisfied.
   `attachment-rule.v1`/`v2`/`v3` remain immutable history, unedited;
   `attachment-rule.v4` is a strict additive widening — every existing
   `"presence"`-only citizen instantiates unchanged under the new schema
   with no content edit required, should it ever adopt the new version.

2. **A value violation is a distinct, named completeness reason, not
   silence and not conflated with absence.** The generic attachment
   interpreter (`packages/derivation/runner.py`'s `attempt_attachment`)
   gains one bounded branch: for a `"value"`-checked required answer, read
   the current finding it already fetches to satisfy the presence check
   (no new lookup, no new generic evaluator capability), and compare its
   value to `equals`. A mismatch is a new, distinctly-named violation —
   not folded into the existing missing-symbol list, and never a numeric
   zero, an assumed default, or a silently-dropped row — that feeds the
   *same* `required-and-incomplete` disposition and non-publication walk
   the presence check already produces (ADR-0036 Decision 1's ratified
   triad is unchanged: three atomic dispositions, no embedded state
   field). The walk names the exact answer and the value it currently
   holds, exactly as it already names an exact missing symbol; a reader
   can distinguish "absent" from "present but disqualifying" without
   inference.

3. **Absence and violation remain independently checked, in one pass.**
   Presence is checked first, independently per answer, exactly as ADR-0036
   Decision 4 already requires ("every required answer exists as a current
   finding, checked independently per answer before any value is read");
   value is checked only for an answer already found present. One
   evaluation names every currently missing answer and every currently
   violated answer in the same walk — never only the first of either kind,
   preserving the same accumulate-then-report discipline ADR-0037's
   `conditional_dependency_set` established for absence lists.

4. **Rejected: admission-locus contradiction interlock.** ADR-0038
   Decision 5's bidirectional admission-locus interlock (a declared `"no"`
   and a contradicting signal may never both be current) is not extended
   to this case. That mechanism exists for genuinely contradictory fact
   pairs, where one of two statements must be false. Schedule D's
   declarations are not contradictory with an eligible family's existence:
   "I currently have capital losses" is a true, coherent fact that
   coexists with "I also have an eligible covered-LTCG transaction" — the
   return is simply outside this milestone's bounded class, an
   eligibility conclusion, not a factual contradiction. Rejecting the
   declaration's admission would make it impossible to honestly record a
   real capital loss alongside an eligible transaction, a category error
   against ADR-0011's presence-before-value discipline. Admission-locus
   rejection is also structurally a hard, whole-batch, admission-time
   error with no derivation-time disposition, and does not compose with
   the attachment ontology's derivation-time-only evaluation.

5. **Content-only instantiation.** This ADR adds no new evaluator
   operation, no new generic expression capability, and no new admission
   mechanism. It widens one schema (`attachment-rule.v4`) and one function
   (`attempt_attachment`'s existing per-answer loop). A future schedule
   with an eligibility-gating declared-absence fact adopts `check: "value"`
   in its own content — no new ADR is owed for that future case, matching
   ADR-0036 Decision 5's generalization promise.

## Production conditions (owed to the implementation unit; never allowlisted)

- The exact `attachment-rule.v4` JSON Schema text (additive `check` enum
  widening, required `equals` field on the `"value"` shape) and its
  schema-registry publication.
- `attempt_attachment`'s value-check branch, its new named violation
  reason in the record/walk vocabulary (a versioned schema change, per the
  precedent `ITEMIZATION_TIE_OUT_VIOLATION` set under ADR-0036 Decision 3),
  and the accumulate-both-kinds-in-one-pass behavior (Decision 3, above).
- A Schedule D attachment content successor (`attachment.schedule-d` v2 or
  equivalent) adopting `attachment-rule.v4` and `check: "value", equals:
  "yes"` for the seven boundary declarations; `attachment.schedule-d` v1
  remains immutable history.
- `package_validation.py`/`marshal.py`/`live.py`'s attachment-schema
  dispatch sets extended to admit `attachment-rule.v4` (the same three
  call sites Track 2 found `attachment-rule.v3` missing from at merge
  time; do not repeat that omission for v4).
- Coordinator-from-facts goldens proving: the N1 divergence case now
  converges (attachment reads `required-and-incomplete`, naming the
  violated declaration and its value, in the same run where
  `selected-preferential-base` is `inapplicable`); the N2 absence case is
  unaffected (still `required-and-incomplete`, naming the missing symbol,
  no value read); both P1/P2 positive cases unaffected; the T0→T2
  correction lifecycle trace, showing the attachment's disposition now
  changes in step with the correction instead of staying invariant.

## Consequences

- The Schedule D attachment's own disposition and explanation walk become
  honest about *why* the class is incomplete, closing the divergence
  between the attachment's account and the numeric route's actual
  behavior — no taxpayer or reviewer reading the attachment's walk is
  shown a fabricated "complete" account of an ineligible return.
- Every future schedule instantiating ADR-0036 with an eligibility-gating
  declared-absence fact (the pattern ADR-0038 Decision 5's contradiction
  interlock does *not* generalize to) inherits a ready-made, content-only
  fix.
- `attachment-rule.v1`/`v2`/`v3` and every existing attachment citizen
  remain byte-for-byte unchanged; nothing in this ADR requires a version
  bump for Schedule B or any other existing presence-only completeness
  answer.

## Alternatives Considered

- **ADR-0038 Decision 5's admission-locus contradiction interlock,
  extended to this case.** Rejected on paper (see Decision 4, above and
  the paper spike's Option B): a category mismatch between genuine factual
  contradiction and an eligibility conclusion, and a structural mismatch
  between admission-time hard errors and the attachment ontology's
  derivation-time-only evaluation.
- **Leaving the gap unresolved, relying on `selected-preferential-base`'s
  own correct value check.** Rejected: no wrong number ever publishes, but
  the attachment citizen's entire purpose is to be the honest completeness
  account (ADR-0036 Decision 1); leaving it silently wrong defeats that
  purpose for Schedule D and every future schedule with the same shape.
- **A synthesizing second conclusion citizen mirroring
  `selected-preferential-base`'s value check, read by the attachment.**
  Not adopted: ADR-0052 Decision 2 already rejected a synthesizing
  "Schedule D complete" conclusion citizen for the completeness boundary
  generally, on the same never-silence, no-thin-assertion grounds; adding
  one narrowly for the attachment's own read would reintroduce exactly the
  pattern that decision rejected, and would still require the generic
  attachment mechanism to gain a value-aware branch to consume it — no
  cheaper than Decision 1/2 above, with an extra citizen to keep in sync.

## Links

- Paper spike and charter: not retained in the repository.
- Builds on: ADR-0036 (attachment ontology, the completeness check this ADR
  widens), ADR-0037 (`conditional_dependency_set`, the accumulate-then-report
  discipline Decision 3 reuses), ADR-0038 (declared-absence pattern and the
  admission-locus interlock this ADR declines to extend), ADR-0052/0053
  (the Schedule D covered-LTCG contracts this gap surfaced against)
- Consumed by: a subsequent implementation unit, once ratified — not this
  charter, which is paper-and-draft only
