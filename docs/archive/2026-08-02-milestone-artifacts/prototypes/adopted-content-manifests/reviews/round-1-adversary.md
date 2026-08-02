# Adversary Review — Adopted-Content Manifests, Round 1

Reviewer: Medium-tier Adversary (owner-launched independent context), 2026-07-14.

Scope: ACM-P1 and ACM-P2 in it1/design.md and it2/design.md, against the
accepted governance set, listed ratified ADRs, and the committed
package/loader/content surface. This is paper/static-contract analysis. I did
not read reviews/round-1-governance.md or any ADR-0027 draft or notes.

## ACM-A1 — A closed validator is not yet the sole execution/render authority

**Applies:** it1 (fails); it2 (survives at contract level, with a production
condition). **Classification:** production condition.

**Input state → expected result.** A valid v2 package pins a wages rule and its
peers. A co-located unpinned form field binds that rule's symbol, or an
unpinned rule publishes another symbol; a loader walks the directory and hands
all discovered content to derivation/rendering. Only the resolved member graph
may be active. Co-location may populate the corpus for pin resolution, but
must not make a citizen adopted or renderable.

**Result.** it1 validates only its member set but does not require the
runner/renderer boundary to select from it; its stated exclusions leave
directory layout out of scope. A filesystem walk can therefore render or derive
from the unpinned citizen after validation: a silent second authority. it2 says
paths are not membership authority, makes graph members exact, and limits roots
to package entrypoints, so it survives on paper. Production must pass only the
resolved graph—not the raw corpus/directory traversal—to both runners and
renderers and test a co-located orphan.

## ACM-A2 — Incumbent's conflict escape leaves an orphan field admissible

**Applies:** it1 (fails); it2 (survives as written). **Classification:**
decision-blocking.

**Input state → expected result.** Pin a form field with binds_symbol
tax.example.orphan, pin no producer, and add a syntactically valid
conflict_semantics item that names the symbol but identifies no actual
producer. Reject: a presentation consumer needs an adopted producer (or a
conflict mechanism selecting an adopted producer), not merely a named symbol.

**Result.** it1 permits a field bind to output_owners **or**
conflict_semantics; its required negative rejects only when neither exists. The
described conflict shape names a symbol/resolution, so this construction routes
around the orphan check. it2 requires exactly one reachable package producer,
with a conflict rule authorizing that producer, and rejects ambiguity. It
survives if its future conflict schema records/selects the actual member rather
than retaining a free-text resolution.

## ACM-A3 — “Composition-governed” has no non-circular declared trigger

**Applies:** it1 and it2 (both fail). **Classification:** decision-blocking.

**Input state → expected result.** A v2 package contains the exact line-2b
rule, form field, families/mappings, and constituent subtotals, but no
composition citizen and no rule composition pin. No member declares that the
output is composition-governed. Reject before adoption with the missing-pin
issue required by ADR-0026 decision 4; a bare line-2b sum must not validate
because there is no composition object from which to infer the obligation.

**Result.** it1 requires a pin when a composition citizen publishes the symbol;
with no citizen, that predicate is false. it2 says the same thing for a
composition-governed symbol, but supplies no versioned package/rule field that
makes the obligation discoverable. A form field cannot do so: ADR-0012 makes it
presentation-only. Both need a declared, checkable output contract requiring
the exact pin independently of the composition being present. Otherwise the
advertised missing-composition issue is an unimplementable symbol-name special
case or a vacuous audit.

## ACM-A4 — Incumbent leaves source-mapping fact-type dependencies unpinned

**Applies:** it1 (fails); it2 (survives). **Classification:** decision-blocking.

**Input state → expected result.** Pin a source-family and source-closure-mapping
whose member_fact_type and closure_fact_type are absent from the package. Give
the mapping a matching family and subtotal so all it1-listed mapping edges
otherwise succeed. Reject: ADR-0014's adopted mapping names both fact-type
dependencies and they need exact adopted versions/bundles.

**Result.** it1 requires only mapping-to-family and admits_symbol/subtotal
joins. It asserts fact-type membership generally but declares no
mapping-to-fact-type edge, version join, or negative. The committed mapping
schema's fields are bare ids, so this construction passes the stated design.
it2 expressly closes mappings through fact types and bundles and its
source-authority issue includes bundle-supplied types. It survives if both
mapping fact-type fields—not only the family predicate—are checked.

## ACM-A5 — Exact pins need immutable published-content verification

**Applies:** it1 and it2 (both incomplete; it2 is stronger for the package
body). **Classification:** production condition.

**Input state → expected result.** Publish/adopt U at v1; then offer either a
different member set under the same U v1, or a rule/form/mapping/fact-type whose
bytes changed while retaining its published id/version. Reject both at the
publication/adoption boundary. Article 9 and ADR-0003 make every citizen
version immutable; a complete U v2 requires a new adoption.

**Result.** it1 acknowledges that a registry is needed but leaves hash mechanics
unresolved, so a corpus keyed only by id/version can accept altered bytes. it2
defines ACM_PACKAGE_VERSION_REWRITE from a package checksum, which defeats the
altered package body. Its schema-contract checksums protect schema bytes, not
resolved member-citizen bytes. Both need a published-content registry/check for
the package and every resolved member before trusting the graph.

## ACM-A6 — Incumbent's additive role list cannot detect semantic skew

**Applies:** it1 (fails); it2 (survives subject to canon enforcement).
**Classification:** decision-blocking.

**Input state → expected result.** Admit v1 and v2 schemas that both accept
composition, but v2 interprets it as an executable input/dependency rather than
ADR-0026 provenance; alternatively change computation's member meaning. All
tokens remain in the same additive enum. Reject before execution: one token
cannot gain two meanings or create a third standing-affecting edge.

**Result.** it1's admitted_schemas is an id list and vocabulary monotony proves
only that the token is known. There is no pinned semantic canon or
generation-to-role-meaning join, so this construction passes the stated
validator. it2 pins a role vocabulary plus schema contracts and rejects unequal
meanings as ACM_ROLE_SEMANTIC_DIVERGENCE. It survives if that canon/mapping is
immutable validated content, not a loader constant.

## ACM-A7 — Individual fact pins and bundle adoption can drift

**Applies:** it1 (fails); it2 (survives with a bundle-version condition).
**Classification:** decision-blocking.

**Input state → expected result.** A package individually pins tax.example.age
at v2 for an ELX binding, while workspace adoption supplies a bundle omitting it
or supplying a different generation. Conversely a broader bundle supplies an
unclosed type that a runtime route uses. Reject: the fact surface used by the
rule must be exact, adopted, and version-locked.

**Result.** it1 calls bundles authoring convenience but provides no join from
individual pins to the adopted bundle that instantiates the workspace
vocabulary. Its binding check can pass while runtime adoption exposes another
surface. it2 pins both exact fact type and exact bundle and requires inclusion,
which defeats both constructions in the design. Production must introduce
versioned bundles and nested fact-type versions: committed bundle.v1 has
neither, and enforce the package/adoption join at the runner boundary.

## Verdicts

| Proposition | it1 | it2 |
| --- | --- | --- |
| **ACM-P1** | **Reject.** A1 allows filesystem-resurrected active content; A4/A7 leave authority and fact surfaces incompletely closed; A5 is not enforceable. | **Conditionally accept** — only if the adopted graph is the exclusive runner/renderer projection (A1), every member has immutable published-byte verification (A5), and fact bundles become versioned exact citizens (A7). |
| **ACM-P2** | **Reject.** A2 permits a conflict-table orphan; A3 leaves mandatory composition circular; A6 admits dual role meaning; A4 leaves dangling mapping fact types. | **Conditionally accept** — only after a versioned non-circular declaration marks an output composition-governed and requires its exact pin before composition exists (A3), with the stated role canon and immutable member checks implemented (A5–A6). |

