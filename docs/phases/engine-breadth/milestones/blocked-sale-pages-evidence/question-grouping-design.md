# Track 2: Question identity and saved-model compatibility

## Scope and evidence

This is an evidence-only design note for `charter-question-grouping.md` at
`d64c65af`. It traces committed synthetic content and the projection, saved
model validator, writer, and browser reader. No production or published file
was changed, and no tests were run.

## Findings

### The question text loses its identity before saving

`_closure_question_reasons` resolves source-closure families and input fact
types to their declared question sentences, then returns a sorted set of those
sentences as `{"sentence": ...}` (`packages/derivation/presentation_projection.py:608-625,794-802`).
It does not retain the source question citizen, answer fact type, fact
instance, family scope, or currentness. The generic blocked-row renderer reads
only `reason.sentence` (`packages/presentation/pages/citation-walk.v1.html:1036-1045`).

The noncovered sale closure mapping is a concrete shared target. Its
`closure_fact_type` is
`tax.us.2025.f1099b.noncovered-sold.source-closure` v1, and one question is
declared for eight short- and long-term sale families in
`packages/content/tax/2025/closure-mapping.f1099b-noncovered.json:14-103`.
The target fact type has only the `tax-year` identity key
(`packages/content/tax/2025/schedule-d-boundary-noncovered.bundle.json:33-45`).
Thus the family is the scope to which the answer applies; it is not a separate
closure answer target. The stale case records that the same tax-year answer
can be stale for the newly present long-term family while that family has a
separate current horizon
(`docs/phases/engine-breadth/milestones/blocked-sale-pages-evidence/current-baseline.md:94-103`,
`docs/phases/engine-breadth/milestones/blocked-sale-pages-evidence/track1.md:14-19,51-55`).

Text equality is also not question identity. Four exception-1 input-question
citizens use the same exact sentence but point to four different fact types.
For example, `input-question.exception1-no-capital-losses.v1.json:2-9` and
`input-question.exception1-only-box2a-capital-gains.v1.json:2-9` share the
wording while naming `exception1.no-capital-losses` and
`exception1.only-box2a-capital-gains`. Those targets are separately declared
facts with tax-year identity keys in `exception1.bundle.v2.json:7-45`.

One source question can also have distinct answer instances. The Form 1099-B
box-4 question directs entry for each recorded statement
(`input-question.f1099b-box4.v1.json:2-10`); its answer fact type is keyed by
both `statement` and `tax-year` (`f1099b-box4.bundle.json:8-25`). Grouping by
question citizen alone would merge the different statements' answers.

### Minimum identity and row linkage

The source data already available during projection can provide these stable
parts:

- **Question source:** schema, citizen ID, and version. For an `input-question`,
  the citizen points to its fact type; for a `source-closure-mapping.v4`, the
  mapping declares the closure fact type and its family list. Preserve this
  reference as provenance, but whether it is part of group identity remains an
  owner choice below.
- **Answer target:** fact-type ID and version plus the complete canonical
  values for that fact type's identity keys. This distinguishes same-worded
  questions about different fact types and per-statement instances of one
  question definition.
- **Row applicability:** the family IDs reached by a closure walk, or the
  specific answer instance for an input question. A blocked row should link to
  the shared prompt by a typed reference and keep any independent blocker as a
  separate reason. This lets one question be presented once without dropping
  the row's separate amount-check reason.

Family scope and currentness should be attached to the row-to-question
relationship, not included in the prompt grouping key. The mapping explicitly
uses one closure answer across several families. Including each family in the
key would split that shared answer into repeated prompts. Likewise, currentness
can change when a new member changes the family horizon; it describes whether
the saved answer applies to that row's scope, not a new question identity. A
row link must preserve its family scope and whether that scope needs
reconfirmation so that one current family does not hide a stale one.

The evidence does not settle whether the question-source reference belongs in
the group key. The sale closure mapping and
`input-question.f1099b-noncovered-sold` both name the same closure fact type
and declare the same sentence (`closure-mapping.f1099b-noncovered.json:2-9`,
`input-question.f1099b-noncovered-sold.json:1-9`). Keying only by the answer
target would give one prompt with two source references; keying by producer plus
target would create two groups for the same target. My recommendation is to
key by answer fact-type ID/version plus the full fact-instance identity, and
retain all source citizen IDs/versions as provenance. If multiple sources for
one target disagree on question text or scope, the contract should reject the
ambiguous target or require an explicit source choice. The owner should decide
whether source ID/version participates in identity or only records provenance.

`factId` is not a suitable place for this relationship: its current producer
attaches a pinned statement fact to statement-selection reasons, and existing
SLI projection uses it to recover statement identity
(`presentation_projection.py:303-320`, `current-baseline.md:75-103`).

### The saved v2 reader cannot reconstruct the missing information

The v2 model contains sections, an explanation graph, and `dispositionNodes`;
the latter retain disposition records, dependency symbols, and child links
(`presentation_projection.py:5034-5095`). They do not contain the resolved
source-closure or input-question members needed to map a sentence to a
question definition or its target. The live writer has those members while
building the model, then serializes only the model
(`packages/derivation/live.py:785-811`). The saved-page loader reads and
validates that JSON and embeds it in the fixed page template
(`packages/derivation/live_session.py:36-37,150-172`). The browser therefore
has no adopted-member data from which to recover the lost relationship.

The published v2 schema is immutable and closed at its root
(`packages/schemas/derivation/presentation-model.v2.schema.json:3,18-33,283`;
registered in `packages/schemas/derivation/published.json:76`). Its
`sections.items` schema is only `type: object`, but the runtime validator is
stricter: it requires exactly `id`, `field`, `resolved`, and `citationSites`
for a section, and each blocked reason allows only `sentence` plus optional
`factId` and `statementLabel` (`presentation_projection.py:5240-5254,5595-5609`).
So section-local question metadata might pass that one permissive JSON Schema
item, but it fails saved-model validation; a new top-level group property also
fails the closed v2 root schema. The optional `provenanceGroups` property has
separate citation and attachment semantics and cannot carry question groups.

The page reader accepts `presentation-model.v1` and `.v2`; for v2 it reads the
shared explanation, and it rejects any other schema with the existing
`malformed-shared-explanation` error (`citation-walk.v1.html:847-853`). The
writer always uses the fixed `citation-walk.v1.html` path and validates before
embedding the model (`live_session.py:36-37,150-172`). Therefore an in-place
v2 extension is not compatible, and the browser cannot infer prompt grouping
from saved v2 data.

## Recommendation for owner disposition

Use a new `presentation-model.v3` contract with typed page-level question
records and row references. The recommended group key is the answer fact-type
ID/version plus its full identity key values; keep question citizen ID/version
as source provenance unless the owner chooses producer-plus-target identity.
Keep family scope and scope-currentness on each row reference; preserve other
blocker reasons independently. Update the writer, strict validator, and reader
to write/read v3, while continuing to render existing v1 and v2 saves
unchanged. Old readers would continue to render their v1/v2 models and reject
v3; a new reader would render v1/v2 as before and render v3 using its typed
groups.

**Owner decision requested before implementation:** choose whether group
identity is (A) answer target only—fact-type ID/version plus all identity-key
values, with producer refs kept as provenance—or (B) producer plus answer
target, which can split one target when separate declarations name it. Also
confirm that family scope and currentness belong on each row reference, not in
the group key, and whether to use a new v3 contract. This unit records the
recommendation and evidence; it does not implement either choice.
