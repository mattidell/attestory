# Citation Resolution — Iteration 2 Clean-Room Rival Design

## Scope and result

This is a Rung-2 static-contract design.  It proposes no corpus import, live
lookup, legal conclusion, UI, or runner interpretation.  A citation can be
*statically resolved* only against the adopted package and the published
schema registry; that phrase deliberately does not mean that a government
source exists, that its current text was fetched, or that it supports a rule.

| Proposition | Static-level result |
| --- | --- |
| CIT-P1 — identity and authority model | **settled-at-static-level** |
| CIT-P2 — resolver and load-time integrity | **settled-at-static-level** |

The unresolved work is intentionally external to both propositions: authority
corpus ingestion, link rendering, legal correctness, temporal legal research,
and jurisdictions beyond the v1 families.

## CIT-P1 — Citation identity and authority model

### Decision

A citation is a first-class, versioned **content citizen**, not a free-text
value and not a bare attachment pin.  An attachment is an exact `{id,
version}` pin to that citizen.  This separates the cite's independently
versioned content from each field or rule that uses it, while retaining one
package membership authority.

`citation.v1` is a strict JSON Schema 2020-12 citizen under ADR-0003.  Its
`id` is opaque; neither an authority family nor a locator is inferred from the
id, filename, package position, or runner code.  Published citation bytes and
schema bytes are immutable.  A correction creates a new citation version (or
a distinct citation where the referent changes); an offered body with an
existing `(id, version)` and different bytes is rejected by the established
publication check.

The v1 authority-family enum is deliberately small:

- `us-code` — a United States Code reference;
- `irs-form` — an IRS form edition;
- `irs-instructions` — an IRS form-instructions edition; and
- `irs-publication` — an IRS publication edition.

Each family selects one closed discriminated `oneOf` locator shape in the
citation schema.
For example, `us-code` has `title`, `section`, and an ordered array of
subdivisions; IRS document families have `document_id`, `edition_tax_year`,
and an optional printed locator.  All locator tokens are strings or integers
with schema-declared constraints.  The schema does not accept an unstructured
`url`, `display`, `reference`, or catch-all payload.  It also makes no claim
of a canonical display string: that would need a separately adopted rendering
contract rather than formatter behavior hidden in a resolver.

Illustrative schema delta (names are proposal names, not implementation):

```json
{
  "$id": "tax/citation.v1",
  "required": ["schema", "id", "version", "scope", "authority_family", "locator"],
  "properties": {
    "schema": {"const": "citation.v1"},
    "id": {"type": "string"}, "version": {"pattern": "^v[0-9]+$"},
    "authority_family": {"enum": ["us-code", "irs-form", "irs-instructions", "irs-publication"]},
    "scope": {"$ref": "#/$defs/scope"}
  },
  "oneOf": [
    {"properties": {"authority_family": {"const": "us-code"}, "locator": {"$ref": "#/$defs/us-code"}}},
    {"properties": {"authority_family": {"enum": ["irs-form", "irs-instructions", "irs-publication"]}, "locator": {"$ref": "#/$defs/irs-document"}}}
  ],
  "$defs": {
    "scope": {"type": "object", "required": ["tax_year", "jurisdiction", "family"], "additionalProperties": false},
    "us-code": {"type": "object", "required": ["title", "section", "subdivisions"], "additionalProperties": false},
    "irs-document": {"type": "object", "required": ["document_id", "edition_tax_year"], "additionalProperties": false}
  },
  "additionalProperties": false
}
```

The real successor schema must make the family/locator pairing discriminated
and must carry the normal package-compatible scope.  That detail is a schema
authoring task, not a reason to retain opaque text.

### Attachment and adoption

`form-field.v2` replaces required `citation_ref: string` with required
`citation: {id, version}`.  It changes no field disposition, symbol binding,
or rendering authority: the citation remains descriptive content attached to
the presentation citizen (ADR-0012 decisions 1–6).

`rule-artifact.v2` admits optional `citations: [{id, version}, ...]`; when
present, entries are unique exact pins.  Rule citations are explanatory
metadata only.  They neither alter `when`, `value`, blocking, output
ownership, nor create a derivation edge.  This puts rule attachment in scope
without smuggling tax meaning into the runner.

The package successor adds `citation` through a new immutable role-canon
generation and admits exact citation members.  Every attachment pin must
resolve to exactly one member with that role, and every citation member must
be inbound-reachable through a
field or rule attachment.  These are typed package-closure joins; they are not
Article-7 standing edges.  The package remains the only membership/adoption
authority: no directory scan, URL cache, side registry, or co-located file can
make a citation adopted.  The package admits the new schema generations in
`admitted_schemas` and relies on ADR-0003's published schema registry for byte
integrity, rather than embedding duplicate schema hashes.

### P1 issue map

| Defect class | Contained issue / package outcome |
| --- | --- |
| legacy free-text `citation_ref` in residual-closed content | `CITATION_OPAQUE_RESIDUAL`; reject package |
| attachment lacks an exact pin or names a nonmember | `CITATION_ATTACHMENT_UNRESOLVED`; reject package |
| citation member has the wrong role, duplicate identity, or no inbound attachment | `CITATION_CLOSURE_INVALID`; reject package |
| unrecognized family or locator shape | `CITATION_STRUCTURE_INVALID`; reject package |

## CIT-P2 — Static resolver and load-time integrity

### Decision

The resolver is a contained package-validation pass, not a network client or a
legal interpreter.  For each field/rule attachment it follows the exact pin,
checks the cited citizen against its declared published schema, checks the
citation role/member and inbound closure, and checks the registry-backed bytes
of the package and every resolved citizen.  It collects all defects before it
returns.  Any citation defect makes the package invalid for adoption/execution,
but does not abort validation or erase issues for unaffected members (ADR-0006
decision 3).

The resolver claims **structural-and-adoption verifiability only**.  It does
not claim an external authority registry or corpus-presence check.  Therefore
case 5 is not an external-registry miss: an externally nonexistent but
well-formed locator cannot be declared legally verified by this contract.  The
surface prevents false confidence by using the qualified term
`statically_resolved`, never `legal_verified`, and by preserving the authority
family and locator for a future evidence-bearing authority service.  A later
service may add a separately versioned, adopted authority-corpus contract; it
must not silently widen this resolver.

No resolver branch may fetch an authority site, infer that a Code section
applies, decide a holding, derive an amount, or hold an authority-family table
in runner code.  The family enum and locator requirements are declared schema
content; package validation only enforces those declarations.  Thus deleting
or changing a rule/citation artifact, not a runner branch, accounts for every
tax-meaning difference (Article 11).

### Resolution algorithm and outcomes

For a package P, resolve each attachment A as follows:

1. Validate P and its declared schema generations through the published
   registry; unadmitted generations are defects.
2. Require A to be an exact object pin, never a string; find exactly that
   `citation` member in P.
3. Resolve `(id, version)` to the published citation citizen, validating its
   strict family/locator schema and registry bytes.
4. Confirm typed closure in both directions: A reaches the citation member and
   the citation member is reachable from an attached field or rule.
5. Emit every detected issue.  `ok=false` rejects adoption/execution of P;
   successful attachments report `statically_resolved` with their exact pin.

The only registry asserted here is the existing publication/schema registry:
it proves that named, adopted content has not been rewritten.  It is not a
registry of federal-law truth.  A missing package citizen, a mismatched
published checksum, a bad schema generation, or a malformed locator is a
static reject.  A live-source miss is outside this resolver and cannot be
reported as either acceptance or legal failure.

| Defect class | Contained issue / package outcome |
| --- | --- |
| undeclared schema / malformed citation or locator | `CITATION_SCHEMA_INVALID`; reject package |
| exact pin absent, version-mismatched, or unadmitted | `CITATION_PIN_INVALID`; reject package |
| published package/citation bytes differ from registry | `CITATION_IMMUTABILITY_VIOLATION`; reject package |
| requested live lookup or encoded legal/applicability decision | `CITATION_RESOLVER_OVERREACH`; reject/redesign boundary |

## Gate-2 trace

| Case | P1 contract | P2 behavior |
| --- | --- | --- |
| 1 positive field | `form-field.v2.citation` is an exact pin to a package `citation` member | strict schema + package closure accept; trace field → citation pin → published citizen |
| 2 positive rule | optional exact rule pin is in scope and has the same citizen model | accept when package closure resolves it; no evaluator behavior changes |
| 3 opaque residual | strings are not a successor attachment shape | `CITATION_OPAQUE_RESIDUAL`, reject |
| 4 malformed/incomplete | closed family/locator `oneOf` has no permissive text fallback | `CITATION_SCHEMA_INVALID`, reject |
| 5 registry miss | no external authority registry is claimed | static resolution is structural/adoption-only; no claim of legal verification |
| 6 Article 11 overreach | citation has no executable semantics | reject a live fetch, holding, or applicability branch as resolver overreach |
| 7 lifecycle | C@v1 and C@v2 are distinct immutable published versions; attachments pin one exactly | old P@v1 resolves C@v1 forever; rewriting C@v1 bytes rejects; P@v2 may pin C@v2 |

## Boundary and follow-up

This design is compatible with the ADR-0027/0028 package floor: it adds one
role-canon member kind and typed non-derivation joins, while preserving exact
members, admitted schemas, package-byte immutability, exclusive projection,
and contained validation.  It does not reopen fact-surface, composition, or
form disposition decisions.

Implementation must first ratify a Tier-2 successor ADR, then add successor
schemas, role canon, strict validators, synthetic goldens, and a migration
policy.  A migration window, if ever adopted, must be an explicit schema and
package-generation policy; it cannot make `citation_ref` a co-equal runtime
input in residual-closed packages.
