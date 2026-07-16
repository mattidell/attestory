# Clean-room rival design — taxable-interest composition, iteration 2

## Boundary and Rung-2 scope

This is static Rung-2 evidence: proposed versioned schema/canon/content diffs
and traces against the committed authority, horizon, runner, and currency
contracts. It changes no runner, schema, horizon, or git state.

The 2025 Form 1040 instruction calls line 2b **total taxable interest income**
and names both Form 1099-INT and Form 1099-OID. Schedule B says to report all
taxable interest from Forms 1099-INT, 1099-OID, or substitute statements, but
places tax-exempt 1099-INT box 8 and tax-exempt OID on line 2a. [Form 1040
instructions](https://www.irs.gov/instructions/i1040gi), [Schedule B
instructions](https://www.irs.gov/instructions/i1040sb).

Thus the boundary comes from whether an amount is taxable interest reportable
on line 2b, not its form label. A naive one-1099-INT-box reading is wrong: it
must add box 3 and taxable OID, and must omit box 8. Taxable interest with no
information statement remains in; tax-exempt interest remains out.

## TIC-P1 — declared coextensive universe

For one taxpayer/tax-year scope, a proposed
`form1040.line2b.taxable-interest.v1` universe declares this disjoint,
exhaustive slot set:

| Slot | Canonical member class | Boundary reason |
| --- | --- | --- |
| `int_box1` | taxable 1099-INT box 1 stated interest | taxable interest |
| `int_box3` | taxable 1099-INT box 3 U.S.-savings-bond/Treasury interest | taxable interest |
| `taxable_oid` | taxable OID/periodic interest on 1099-OID or substitute | Form 1040 expressly includes 1099-OID |
| `unreported_taxable_interest` | taxable interest not in either reported class | reportability does not depend on receiving a form |

The universe's exact closure claim says every taxable-interest amount fitting
one of these canonical predicates is recorded and no line-2a tax-exempt amount
is a member. Its predicates are mutually exclusive. The committed B1 family is
therefore one slot only; its truthful narrow claim cannot prove this universe.

### Paper contract diff and validation

Add versioned, adopted `taxable-interest-composition.v1`: scope, output symbol,
a universe id/version pin, and constituents of `{slot, family:{id,version},
subtotal_symbol}`. The universe citizen carries the closed slot list, each
predicate, and its exact claim. A validator rejects unless:

1. the output is `tax.us.2025.form1040.line2b.taxable-interest`;
2. constituents are a bijection with the universe slots (no omission,
   duplication, substitution, or extra slot);
3. each family predicate/scope/claim equals its pinned slot; and
4. each subtotal is that family's existing `authorizes_subtotal`.

The package closure contains universe, composition, all families/mappings,
subtotals, and the line rule. It also rejects a line rule unless both its four
subtotal refs and its closure checks are that same slot bijection. Deleting B3,
OID, or unreported interest is therefore invalid adopted content, not a B1 sum
that happens to publish. This is ADR-0016(4)'s explicit composition, not the
implicit promotion ADR-0016(5) forbids.

Add generic versioned operation `require_closed(source_set)`. Its canon: use
the existing adopted mapping/current-horizon/literal-true dispatch; return
additive zero and record the closure read, or block `SOURCE_SET_UNCLOSED`.
It has no tax/form name. The versioned rule schema also gains a required
`composition:{id,version}` pin for a line rule, and the runner records that
composition and its universe as `package` pins. The line rule adds four
subtotal refs and one such operation per slot. Even a nonempty subtotal cannot
make line 2b eligible without its closure check. The line finding pins its
rule, composition, universe, four subtotals, every exact
mapping/declaration/current closure finding read, package/adoption,
governance, and relevant canon. Coverage names and pins this universe and calls
it complete only when this composition passes.

### Cases 1–5

| Case | Two positives | Two negatives | Expected outcome |
| --- | --- | --- | --- |
| 1 Empty | four closed-empty slots; same with different empty horizons | B1-only closure; false/absent other closure | only positives publish closure-backed `$0` |
| 2 B1 only | `$120` B1/all others closed empty; B1 `$0`/all closed | B3 open; B1-only zero | all four closure reads required |
| 3 Multi-source | B1 `$40` + unreported `$7`; B3 `$9` + OID `$4` | omitted OID; duplicate B1/unreported member | `$47`/`$13`; defect rejects or blocks |
| 4 One open | B1 present/others closed; B3 present/others closed | OID open; unreported open | negative blocks; coverage names open slot |
| 5 Narrow substitution | valid four-slot line; valid B1 subtotal | B1 rule offered as line; B1 closure offered as coverage | validator rejects both |

Positive subtotal findings pin raw input findings, or their own mapping,
declaration, and closure finding when empty. The line always pins all direct
closure findings. A negative publishes no line finding; its completed run
records the typed block or validation error, and records never become inputs.

## TIC-P2 — honest zero and late member

Line 2b zero is eligible only when every slot has exactly one current,
literal-true closure on its current horizon. It is therefore coextensive, not
an empty collection or B1's zero.

### Case 6 mandatory lifecycle trace

Let genesis horizons be `H-b1-0`, `H-b3-0`, `H-oid-0`, `H-nf-0`; asserted true
closures `C-b1-0`, `C-b3-0`, `C-oid-0`, `C-nf-0`; empty subtotals
`D-b1-0`, `D-b3-0`, `D-oid-0`, `D-nf-0`; and zero `D-2b-0`.

1. Name the four family declarations `S-b1/S-b3/S-oid/S-nf`, mappings
   `M-b1/M-b3/M-oid/M-nf`, subtotal rules `R-b1/R-b3/R-oid/R-nf`, line rule
   `R-2b`, composition `P-2b`, universe `U-2b`, adoption `A`, governance
   pins `G`, and closure-operation canon `K-closed`. `D-2b-0` publishes `$0`
   with pins: computation `R-2b`; package `P-2b,U-2b,M-b1,S-b1,M-b3,S-b3,
   M-oid,S-oid,M-nf,S-nf`; inputs `D-b1-0,D-b3-0,D-oid-0,D-nf-0` and
   `C-b1-0,C-b3-0,C-oid-0,C-nf-0`; operation-semantics `K-closed`; adoption
   `A`; and `G`. Each empty subtotal `D-x-0` pins computation `R-x`, package
   `M-x,S-x`, input `C-x-0`, rounding canon, `A`, and `G`. Existing derivation
   edges are each `C-x-0 → D-x-0`, each `D-x-0 → D-2b-0`, and each direct
   `C-x-0 → D-2b-0` for x = b1, b3, oid, nf.
2. Late B1 arrival is one atomic `member-transition`: member finding `F-b1-1`
   plus successor `H-b1-1 ← H-b1-0`. The successor is the existing
   individuation root: `H-b1-0 → C-b1-0`; those existing derivation edges
   displace `D-b1-0` and `D-2b-0`. No withdrawal, stored flag, or third edge.
3. Until a current true `C-b1-1` is asserted for `H-b1-1`, line 2b blocks
   `SOURCE_SET_UNCLOSED` for B1 and coverage reports the universe incomplete;
   historical `D-2b-0` stays reachable but noncurrent.
4. After re-attestation and explicit rerun, `D-b1-1` pins `F-b1-1`; new
   `D-2b-1` pins it, the other subtotals, `C-b1-1/C-b3-0/C-oid-0/C-nf-0`, all
   mapping/declaration versions, composition/universe/rule, adoption,
   governance, and canon. It may publish only then.

The second positive lifecycle is the same trace with a late OID member. The
two negatives are arrival without re-attestation (block) and a removal or
reclassification (the same atomic transition/successor path). A same-member
value correction advances no horizon; ordinary correction roots and existing
derivation edges displace its descendants.

## Explicit unresolved authority

The cited instructions settle that taxable OID belongs in the boundary, but the
committed slice has no adopted OID/market-discount/premium/nominee/accrued-
interest adjustment taxonomy. Production must declare those predicates and
their arithmetic before claiming this universe complete; it may not silently
drop them. This design also does not decide a reusable all-lines composition
family. Those omissions do not authorize a narrower line-2b claim.
