# ADR 0065 — `attachment-rule.v7`: Family-Occupancy Applicability, Declared Closure Preconditions, Value-Checked Answers, and Declared Branch Emptiness

- Status: **proposed** (drafted 2026-08-11; awaiting owner ratification)
- Tier: 2 — additive published-schema successor for the attachment substrate.
  Future blast radius is real (every later schedule inherits the applicability
  and completeness vocabulary), migration cost is nil (every existing citizen
  instantiates unchanged), and it introduces no new schema **kind**, no new
  evaluator operator, no `source-family.v2`, and no `derivation-record` enum
  value.
- Date: 2026-08-11

## Context

This ADR exists because the owner's 2026-08-11 second ruling on the
`f8949-noncovered-basis` milestone found that the attachment substrate, as
published, lets three things that describe **one** proposition disagree with
each other on the same return:

- whether an attachment is **required** (`requirement`),
- whether a required attachment is **complete** (`completeness`),
- whether the lines the attachment accounts for actually **calculate**.

Four disagreement states were found in committed source. Each is a real state
of the ratified line at `package.core-calculations.v29.json`, not a
hypothetical.

**D1 — the two attachments disagree about the same declaration.**
`attachment-rule.v6`'s `required_answer`
(`packages/schemas/tax/attachment-rule.v6.schema.json:71–80`) admits only
`"check": {"const": "presence"}`; the `"value"` const exists in **no** schema
version other than `attachment-rule.v4`
(`packages/schemas/tax/attachment-rule.v4.schema.json:100–125`). So
`attachment.f8949.json:33–43` is presence-checked on the boundary declaration
while `attachment.schedule-d.v5.json:77–88` value-checks the same symbol at
`"yes"`. A return that answers that declaration `"no"` therefore has Form 8949
reading **complete** while Schedule D correctly blocks
`COMPLETENESS_VALUE_VIOLATION`. This is ADR-0055's defect reappearing between
two attachments instead of between an attachment and a rule.

**D2 — applicability is decided by an amount, while calculation is decided by
membership.** Both published requirement shapes are amount-shaped or
single-family:

- the threshold shape compares named subtotal symbols to a parameter
  (`runner.py:815–820`: `Decimal(str(self.symbols[s])) > threshold`, then
  `required = any(t["over"] for t in triggers)`), and every Form 8949 /
  Schedule D citizen uses **proceeds** subtotals for it
  (`attachment.f8949.json:24–27`, `attachment.schedule-d.v5.json:251–258`);
- the categorical `family_nonempty` shape (ADR-0053 Decision 1,
  `attachment-rule.v3`/`v4`) counts members correctly — `required =
  len(member_values) > 0` at `runner.py:656–658` — but names exactly **one**
  family, so it cannot express "any of these six families is occupied".

Consequently a transaction with **zero proceeds and positive basis** leaves
every proceeds subtotal at `0`, the threshold comparison false, and the
attachment `inapplicable`, while the box's column-(h) rule computes
`0 − basis` and publishes a real loss. A **zero/zero** member does the same
with a zero line. In both cases the form the taxpayer is required to file is
reported as not required while its own arithmetic runs.

**D3 — completeness does not see whole-transaction-family closure.**
`attempt_attachment` reads, for completeness, only requirement subtotals
(`runner.py:793–797`), itemization symbols (`runner.py:852–855`), and declared
answers (`runner.py:881–937`). Every one of those resolves through **scalar
companion** families. The **whole-transaction** family is named nowhere in an
attachment citizen: `rule.schedule-d-line1b.json`'s `when.all` requires
`require_closed` on `tax.us.2025.f1099b.covered-w-st` **in addition to** its
three scalar companions, and no subtotal path touches that family. So a return
whose scalar companions are closed and whose whole-transaction family is not
has Schedule D reading **complete** while line 1b blocks. This is live on the
ratified line today for lines 1a, 1b, 8a, and 8b.

**D4 — a declared contradiction is invisible to completeness.** The
`no-form8949-sources == "yes"` branch of `attachment.schedule-d.v5.json:54–71`
adds only a value check on the declaration itself, and the completeness
interpreter never consults family membership. A return with code-W members that
also answers "no Form 8949 sources" reads **complete** on Schedule D and
computes line 1b from real members. No committed test exercises that state:
`tests/test_schedule_d_form8949_covered_wash_sale_t1.py:164` selects
`BOUNDARY_PATH_A` only when there are no W members at all.

The prior Track 0 proposed to close D4 with runner code keyed on `rule_id`, on
the `GUARD_IDENTITY_KEY_COLLISION` precedent (`runner.py:195`, `863`, `869–875`).
The owner rejected that: deleting the attachment citizen would not remove the
behaviour, so the citizen would not be the account of the form it claims to be.
Every mechanism below is therefore declared in versioned content, interpreted
generically, and disappears with the artifact that declares it.

## Decision

1. **Publish `attachment-rule.v7`, an additive union of `v6` and `v4`.**
   `attachment-rule.v1`–`v6` are immutable history and are not edited. v7 takes
   v6's row model verbatim — `adjustment_rows` with its closed `kind` enum, and
   the `tie_out` shape with `operation: "subtract"`, `positive_subtotals`, and
   `adjustment_subtotals` — and takes v4's `required_answer` `oneOf` verbatim,
   so a v7 citizen may value-check an answer. Every existing v4 and v6 citizen
   instantiates unchanged under v7 with no content edit beyond its `schema`
   string; that is the additivity test, and it is the reason v7 also carries
   forward v3/v4's single-family `family_nonempty` requirement branch it does
   not itself need.

   This closes **D1**: an attachment on v7 checks the *value* of a boundary
   declaration, so two attachments reading the same declaration reach the same
   verdict by construction rather than by convention.

2. **A `requirement` may name a set of source families whose *occupancy*
   makes the attachment applicable.** v7's `requirement` is a `oneOf` over
   three branches: v6's threshold shape unchanged, v3/v4's single-family
   `family_nonempty` shape unchanged, and a new branch

   ```json
   {
     "kind": "any_of",
     "citation": {"id": "...", "version": "v1"},
     "occupancy": {
       "source_families": [{"id": "...", "version": "v1"}]
     },
     "threshold": {
       "subtotals": ["..."],
       "comparison": "strictly_greater_than",
       "threshold_parameter": {"id": "...", "version": "v1"}
     }
   }
   ```

   with `anyOf` requiring at least one of `occupancy` / `threshold` present.
   Semantics, in this order:

   - every family in `occupancy.source_families` that is not admitted (not
     closed at the family's current horizon) blocks `DEPENDENCY_ABSENT` naming
     the family ids — the same honest block
     `_attachment_family_nonempty_trigger` already emits at `runner.py:647–650`,
     never a silent "not required";
   - every symbol in `threshold.subtotals` that is absent blocks
     `DEPENDENCY_ABSENT` naming it, exactly as `runner.py:793–797` does today;
   - the attachment is **required** if any occupancy family has at least one
     member, **or** any threshold subtotal exceeds the threshold. Occupancy is
     `len(member_values) > 0` (`runner.py:656–658`) — a **count**, never an
     amount.

   Per-trigger outcomes are recorded for both halves, as they are today, so the
   walk always says which family or which subtotal made the form required.

   This closes **D2** for every family-backed source. The threshold half
   survives only for symbols that are *not* family projections — the capital-loss
   carryover symbols `tax.us.2025.capital-loss-carryover.short-term` /
   `.long-term`, which are published by `rule.capital-loss-carryover.*` rule
   content and have no source family to occupy — where "greater than zero" is
   the true applicability test rather than a proxy for one.

3. **`completeness.required_closures`: an attachment declares the source
   families whose closure it vouches for.** New, optional:

   ```json
   "completeness": {
     "required_closures": [
       {"label": "...", "source_family": {"id": "...", "version": "v1"}}
     ],
     "required_answers": [ ... ],
     "branch_requirements": [ ... ]
   }
   ```

   Interpretation: once the attachment is required, and before any answer is
   read, every named family must be admitted; any that is not blocks
   `DEPENDENCY_ABSENT` naming the family ids. Nothing about member counts or
   values is read.

   The **content obligation** that makes this load-bearing rather than
   decorative: a citizen's `required_closures` must be exactly the union of

   - every `source_set` named by a `require_closed` in the `when` of every rule
     that publishes a line the attachment itemizes or accounts for, and
   - every `source_set` named by a `collect` in the subtotal rules those lines
     read.

   Under that obligation, "the attachment is complete" **entails** "no line it
   accounts for can block for closure", because `require_closed` and `collect`
   read the same admitted set the check above reads: the runner passes
   `closed_sets=frozenset(self.admissions)` into the evaluator at
   `runner.py:336`, and `self.admissions` is the single dispatch path computed
   by `resolve_closure_admissions`
   (`packages/derivation/source_authority.py:99–166`).

   This closes **D3**, and it closes it *declaratively*: the whole-transaction
   family appears by id inside the attachment citizen, so deleting the citizen
   deletes the requirement.

4. **`branch_requirements[].asserts_families_empty`: a branch declares what its
   own answer implies about the world.** New third alternative alongside
   `adds_required` and `names_obligations`, with the containing `anyOf` widened
   to admit it:

   ```json
   {
     "when_answer": {"symbol": "...", "equals": "yes"},
     "asserts_families_empty": [
       {"label": "...", "source_family": {"id": "...", "version": "v1"}}
     ]
   }
   ```

   Interpretation, evaluated inside the existing `branch_requirements` loop the
   moment the branch's `when_answer` matches, independently of whether the same
   branch also carries `adds_required`:

   - a named family that is not admitted blocks `DEPENDENCY_ABSENT` naming it —
     its emptiness is *unknown*, which is not the same as *true*;
   - a named family that is admitted with at least one member blocks
     `BLOCK_INVALID` (`DEPENDENCY_INVALID`,
     `packages/derivation/evaluator.py:25`) naming the occupied family ids.

   **No `derivation-record` enum value is added**; that enum is closed at v6
   (`packages/derivation/records.py:38–47`) and
   `F1098_SCOPE_CONTRADICTION` is precisely the precedent not followed here.
   Unlike `GUARD_IDENTITY_KEY_COLLISION`, nothing in the interpreter names a
   rule id, a fact type, or a family: the families come from the citizen.

   This closes **D4**. A declaration that asserts an absence now has that
   assertion checked against the recorded members, in the artifact that asks
   the question.

5. **The interpreter changes are four bounded branches, and the symbol surface
   is unchanged.** Track 1 adds `"attachment-rule.v7"` to `ATTACHMENT_SCHEMAS`
   (`runner.py:140`) and to the version tuples at `runner.py:468`, `833`, `981`,
   `1035`, `1045` and `marshal.py:89`; implements Decision 2's `any_of` branch
   beside the existing two in `attempt_attachment`; implements Decisions 3 and 4
   as two `self.admissions` reads; and treats v7 exactly as v6 for row and
   tie-out handling. Eligibility (`_requires`, `runner.py:455–479`) and
   marshalling (`_rule_required_symbols`, `marshal.py:75–104`) gain the
   `any_of` branch's `threshold.subtotals`; **source families contribute no
   symbol**, exactly as ADR-0053 Decision 1 already established for
   `family_nonempty` (`runner.py:463–467`, `marshal.py:90–92`).

6. **Every read pins its evidence.** Occupancy, `required_closures`, and
   `asserts_families_empty` each pin the family's mapping, its declaration, and
   the exact current closure finding, in the shape
   `_attachment_family_nonempty_trigger` already emits (`runner.py:659–669`).
   No new pin role and no new pin vocabulary. A reader can walk from "Schedule D
   is complete" to the exact closure finding for each family it vouches for.

7. **What v7 deliberately does not do.** It adds no per-row value constraint,
   so the ADR-0062 per-transaction row guards (`_f8949_row_guard_violations`,
   `runner.py:163–172` and `679–693`, dispatched on `rule_id` at `runner.py:863` and
   `_LINE_GUARD_BOX_KEYS`) stay runner code. That is a **named residual**, not
   an oversight: those guards are about a nonzero column (g), a state the
   `f8949-noncovered-basis` supported class does not contain, and expressing
   them declaratively means designing a row-constraint vocabulary that this
   milestone has no instance to validate against. The residual's exact shape is
   recorded in Consequences so the next attachment milestone finds it.

## Production conditions (owed to Track 1; never allowlisted)

1. `python3 -m unittest tests.test_schema_registry` passes with the v7 file
   present, and no byte of `attachment-rule.v1`–`v6` changes
   (`git diff --stat` over `packages/schemas/tax/attachment-rule.v[1-6]*` is
   empty on the milestone branch).
2. **Additivity is demonstrated, not asserted:** the existing
   `attachment.schedule-d` v5 body and `attachment.f8949` v1 body each validate
   against `attachment-rule.v7` with only their `schema` string changed, in a
   test, before either successor's real edits are applied.
3. Each of Decisions 2, 3, and 4 has a fixture that observes the block at the
   production boundary through `live_coordinate_run`, with its exact code and
   its exact `missing` list: an unadmitted occupancy family, an unadmitted
   `required_closures` family, an unadmitted `asserts_families_empty` family,
   and an occupied `asserts_families_empty` family.
4. **Occupancy is proved to be a count, not an amount:** a member with zero
   proceeds and positive basis, and a zero/zero member, each make the
   attachment required.
5. The Decision 3 content obligation is checked **mechanically**, not by
   reading: a package-validation check that each v7 citizen's
   `required_closures` set equals the union of the `require_closed` and
   `collect` `source_set`s of the rules publishing the symbols it accounts for.
   If that check cannot be built against the current package graph, Track 1
   stops and returns rather than shipping the obligation as prose.
6. Every prior attachment fixture passes unmodified at its own pinned adoption;
   no historical adoption resolves a v7 citizen.

## Consequences

- Attachment **applicability** stops being an amount test wherever a family
  exists to count, so a zero-amount transaction can no longer make a required
  form report itself unnecessary.
- Attachment **completeness** acquires, for the first time, a declared
  dependency on source-family closure. The invariant "complete ⟹ no accounted
  line blocks for closure" becomes a property of the citizen rather than a
  coincidence of which symbols the threshold happened to name.
- A declared absence can be **contradicted by the record**, and the
  contradiction is stated by the artifact that asked the question. This is the
  first attachment-level contradiction check that is not runner code keyed on a
  rule id.
- **Named residual.** The ADR-0062 per-transaction row guards remain rule-id
  keyed, so a code-W row-guard violation blocks Form 8949 and line 1b/8b while
  Schedule D still reads complete. No wrong number escapes — line 1b blocks, so
  lines 7/15/16 block, and `selected-preferential-base` independently
  value-checks the same declarations
  (`rule.selected-preferential-base.v4.json:210, 302, 307`) — but Schedule D's
  own disposition is optimistic in that state. It is outside the
  `f8949-noncovered-basis` supported class (column (g) is contractually zero
  there, and `_f8949_row_guard_violations` structurally never reads a
  box-B/box-E member), and closing it needs a row-constraint vocabulary with a
  real instance to validate against. Recorded here as the next attachment
  substrate candidate.
- **Named residual, second — and it widens under this milestone.** The
  identity-key collision kill-test has the same shape as the row guards:
  `_covered_w_identity_key_collision_violations` is dispatched on `rule_id` at
  `runner.py:871–877` (line rules, via `_LINE_GUARD_BOX_KEYS`,
  `runner.py:176–179`) and at `runner.py:508–513` and `runner.py:1114–1125`
  (the Form 8949 attachment), and **never** for
  `tax.us.2025.rule.attachment.schedule-d`. So on a return carrying a collision,
  Form 8949 blocks `BLOCK_INVALID` and lines 1b/8b block while
  `attachment.schedule-d` v6 reports **complete**. Neither v7 construct catches
  it: a collision does not unadmit a family, so `required_closures` is
  satisfied, and Schedule D's own itemization symbols are the line 1a/8a/13
  subtotals, which a collision does not disturb. ADR-0063 Decision 5 **widens**
  this guard from two pairs to fifteen across all six transaction fact types, so
  it fires in strictly more states without changing where it is dispatched from.
  No wrong number escapes — line 1b blocks, so lines 7/15/16 block — but
  Schedule D's disposition is optimistic in that state. Same cause and same fix
  as the first residual: a declared row- and identity-constraint vocabulary.
  Both are recorded as the next attachment-substrate candidate.
- One more published `attachment-rule` version exists. The cost is real: the
  runner now carries seven version strings in five tuples. Decision 5 keeps that
  cost to string membership rather than branching, and no version is retired.

## Alternatives considered

- **Move `attachment.f8949` to `attachment-rule.v4` instead of publishing v7.**
  Rejected: v4 has no `adjustment_rows` and no subtractive `tie_out`, so the
  six existing box-A/box-D parts could not be expressed and the ADR-0062
  citizen would have to be rebuilt on a weaker shape. That is a regression, not
  a migration.
- **Move `attachment.schedule-d` to `attachment-rule.v6`.** Rejected for the
  mirror-image reason and already recorded in ADR-0064's alternatives: v6 has no
  value check, so the move would silently downgrade ADR-0055 semantics on the
  Schedule D boundary answers.
- **Leave Form 8949 presence-only and rely on Schedule D to block.** Rejected
  by the owner 2026-08-11: two attachments disagreeing about one return is the
  defect, whichever of them happens to be conservative.
- **Express Decision 4 as a runner guard on `BLOCK_INVALID` plus a named
  `tax.us.2025.block.*` symbol**, on the `GUARD_IDENTITY_KEY_COLLISION`
  precedent. Rejected by the owner: deleting the artifact would not remove the
  behaviour. The precedent is explicitly not followed.
- **Express "all four families closed" as declared answers in
  `adds_required`.** Rejected: it would ask the taxpayer to re-declare
  contributed authority, which is the same duplicated-authority defect the owner
  rejected for the chained discriminator, and it would be satisfiable by a
  wrong answer.
- **Generalize `family_nonempty` in place by letting its `source_family` become
  an array.** Rejected: it would change the meaning of a `kind` string across
  published versions, so a reader holding a v4 citizen and a v7 citizen would
  have to know the version to know the arity. A new `kind` costs one more
  discriminator and keeps every published meaning fixed.
- **A `derivation-record` successor carrying a dedicated contradiction code.**
  Rejected: the enum is closed at v6, `BLOCK_INVALID` already carries the
  category, and the family ids in `missing` carry the specifics.
- **Deferring the whole substrate decision to a later milestone and shipping
  boxes B/E on v6.** Rejected: D2 and D3 are already live on the ratified line
  and boxes B/E would inherit both, adding two more lines that can block while
  Schedule D reads complete.

## Links

- Plan: `docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md`
  ("Attachment substrate decision (B2)", "Track 0 adversarial closure")
- Schema-intent ledger: `milestone-schema-ledger`,
  `schema-ledger/events/f8949-noncovered-basis/20260811T120000Z-attachment-rule-6b3d91.json`
  (`propose`, `additive`)
- Builds on: ADR-0036 (attachment ontology), ADR-0053 (`family_nonempty`),
  ADR-0055 (`attachment-rule.v4` value check), ADR-0056, ADR-0061, ADR-0062
- Companions: **ADR-0063** (noncovered authority, families, completeness
  successor), **ADR-0064** (boxes B/E, lines 2/9 composition)
- Owner decision: 2026-08-11 second ruling on `f8949-noncovered-basis`
  (blockers B2–B5); lifts the standing non-goal on a new published
  `attachment-rule` version
