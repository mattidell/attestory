# Governance Disposition — Advisor Review of the Engine Language Map Closeout

Filed by the Foreman 2026-08-20, on owner direction to independently verify
and disposition an advisor review of the closed Grammar Census milestone.
This record does not change any production code, schema, ADR, or governance
document — it establishes how four tension-catalog entries are to be carried
forward so a future "stop here" cannot be read as silently disposing of them.

## Verification

Each entry the advisor named was independently re-read against source before
any disposition was recorded.

**T1 — `docs/phases/grammar-census/inquiries/track-2-tension-catalog.md:86`.**
`packages/derivation/package_validation.py:182-188` (`_predicate_depth`)
recurses through `args` only. Of the term/predicate operators
`declarative_validation.py` accepts, only `all`/`any` carry `args`;
`add`/`subtract`/`compare` carry `left`/`right`, `floor_zero` carries
`value`. Confirmed by synthetic (reproduced independently by the Foreman,
by Track 2, and again by Track 2b-i and 2b-ii on separate runs):
`compare(add^n(field,1),0)` scores admission depth 1 for every `n` and
evaluator `MemberConstraintTooDeep` at `n≥5`. `docs/adr/0066-declarative-
structured-validation-and-consumer-closure.md` decision 2 states "Resolver
admission rejects predicate depth greater than six." **Verified: the ADR's
stated contract is not what admission does.**

**T2 — `track-2-tension-catalog.md:155`.** Hash-verified this session:
`packages/schemas/tax/attachment-rule.v3.schema.json` and `.v5.schema.json`
both declare `"$id": "tax/attachment-rule.v3"`; SHA-256 prefixes
`5b3f219879095db2` (v3) and `aecd3bf51c16fac9` (v5) — different bytes, same
declared identity, both confirmed against `packages/schemas/tax/published.json`.
The instance discriminator resolves to v3; v5's content is unreachable by
any production path. **Verified.** `docs/adr/0003-json-schema-citizens-and-
opaque-ids.md` establishes schema `$id` as the citizen-identity mechanism
("the schema, not the reader, says what a thing is") — two files claiming
one `$id` is a violation of that identity discipline, independent of any
grammar-boundary question this census otherwise asks.

**T5 — `track-2-tension-catalog.md:364`.** `packages/derivation/
evaluator.py:345-360` (`_bracket_fold`) binds `canon =
env.canon["bracket_fold"]["spec"]` at line 346 and never references `canon`
again; the fold arithmetic is a hardcoded formula. `docs/adr/0006-rule-
artifact-language.md` decision 4 (`:18`) states operation semantics
including `bracket_fold` "carry their own versioned semantic
specification; an enum name alone is not canon," and decision 3 (`:17`)
states in the ADR's own words: "A schema document not wired to enforcement
does not satisfy this ADR." **Verified — the tension catalog's own T5 entry
already quotes the ADR-0006 language that names this as non-conformance;**
95 committed uses (`U-019`) of an operation whose declared canon spec does
not govern its arithmetic.

**T8 — `track-2-tension-catalog.md:511`.** `packages/derivation/
package_validation.py:197-206` (`_LINE_1A_8A_NON_CONFUSION_IDS`) and
`:1635-1662` (`MIXED_BOX2A_GRAPH` and three siblings) are Python literals
naming specific tax rule ids, with inline comments citing ADR-0061 decision
5, ADR-0059 decision 7, and ADR-0050 decision 3 as the invariants being
preserved. 83 distinct `MemberIssue.code` strings (`U-084`) exist only in
Python, enumerated nowhere in a schema. **Verified.** The census's own
framing (Track 2 surviving question 3) leaves the *locus* question
unsettled rather than calling it a settled defect; the advisor's framing —
that Python-resident, tax-specific exclusivity axioms conflict with the
architecture's declared-artifact locus of tax meaning (the same principle
`docs/adr/0003` and `docs/adr/0006` establish for other surfaces) — is a
governance judgment consistent with the verified evidence, not a
disagreement with it. The census left the call open; the advisor is making
the call. Both readings are recorded below rather than collapsed into one.

## Disposition

**None of T1, T2, T5, or T8 is closed by this milestone, and none is closed
by any future "stop here."** The Engine Language Map milestone was
documentation-and-evidence only by design (`docs/phases/grammar-census/
milestones/engine-language-map.md`, exit criterion 8) and correctly made no
code, schema, or ADR change. That design choice describes what this
milestone was for. It does not describe what these four findings are —
they are not merely documented curiosities; each names a place where a
publication or an architectural principle diverges from what the system
does.

- **T1 — remains an open product-contract implementation defect.** ADR-0066
  decision 2's admission-depth bound is not enforced as written. It stays
  open until either admission is changed to match the ADR, or the ADR is
  superseded to describe what admission actually does. Neither happened in
  this milestone and neither is implied by it.
- **T2 — is a Canon/identity conformance defect under ADR-0003.** Two
  published schema files claim one `$id`. This is not contingent on any
  grammar-boundary judgment call the way T1/T8 are — it is a straightforward
  publishing defect in the schema corpus, independently reproducible by
  anyone who hashes both files.
- **T5 — is an ADR-0006 conformance defect, and a legibility hazard.** The
  ADR's own text ("a schema document not wired to enforcement does not
  satisfy this ADR") already names this class of problem; `bracket_fold`'s
  canon spec meets that description. A maintainer editing the canon `spec`
  fields will reasonably believe they take effect. They do not.
- **T8 — is a locus-of-meaning conflict, owner call on remediation
  required.** The invariants are ADR-backed; their expression as unversioned
  Python literals rather than declared package-language content is, on the
  advisor's framing, in tension with the architecture's own stated
  principle that tax meaning belongs to declared, versioned artifacts. The
  census left this an open question rather than a settled defect; this
  disposition record does not resolve that disagreement — it ensures the
  disagreement survives as a carried, owner-held item rather than
  disappearing into "documentation only, no action."

## What this record is not

It is not an ADR amendment, an ADR supersession, a code change, or a
governance-document change — none occurred. It is not a ranking of urgency;
that ranking is produced separately per the owner's direction, after
publication, as a recommendation rather than an action. It is the record
that these four items were seen, agreed with on the evidence, and carried
forward rather than allowed to close by omission when this milestone's
own findings are read as "nothing to do."
