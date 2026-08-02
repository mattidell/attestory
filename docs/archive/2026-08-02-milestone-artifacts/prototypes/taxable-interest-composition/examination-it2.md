# Examination — clean-room rival, iteration 2

## Outcome

**TIC-P1: settled at static level, conditional on declared OID/adjustment
facts.** Form 1040 line 2b is total taxable interest, and its instruction
names Form 1099-INT and Form 1099-OID. Schedule B says all taxable interest is
reported there, while 1099-INT box 8 and tax-exempt OID belong to line 2a.
[Form 1040 instructions](https://www.irs.gov/instructions/i1040gi), [Schedule
B instructions](https://www.irs.gov/instructions/i1040sb). The derived slots
are B1, B3, taxable OID/substitute, and unreported taxable interest—not one
box per 1099-INT and not tax-exempt interest.

**TIC-P2: settled at static level.** An empty zero needs every slot's
current-horizon literal-true closure; a late member displaces it through
ADR-0017 individuation plus existing ADR-0010 derivation edges.

## P1 contract

`taxable-interest-composition.v1` pins a closed universe and a bijection from
each slot to source family and authorized subtotal. Validation rejects a
missing/duplicate/extra slot, predicate/scope mismatch, unauthorized subtotal,
or a line rule whose subtotal and `require_closed` lists differ from that
bijection. The generic versioned `require_closed(source_set)` operation uses
only the committed mapping/current-horizon/current-literal-true dispatch and
blocks otherwise. Its closure reads make the line pin all four exact
mappings/declarations/closures. Coverage cites the same universe and never
calls a narrow closure complete.

## Required cases

| Case | Positive checks | Negative checks | Result |
| --- | --- | --- | --- |
| 1 | four closed empty; alternate horizons | B1-only; false/absent other | only positives yield `$0` |
| 2 | `$120` B1; zero B1/all closed | B3 open; B1-only zero | all slots required |
| 3 | B1+unreported=`$47`; B3+OID=`$13` | omitted OID; duplicate member | publish vs reject/block |
| 4 | B1-present/closed rest; B3-present/closed rest | OID open; unreported open | block; no broad coverage |
| 5 | valid four-slot line; valid B1 subtotal | B1-as-line; B1-as-coverage | both substitutions reject |
| 6 | late B1 then re-attest; late OID then re-attest | no re-attestation; removal/reclassify | old zero noncurrent; successor only after closure |

## Case 6 edge/pin audit

At empty state, `D-2b-0` pins `D-b1-0,D-b3-0,D-oid-0,D-nf-0`,
`C-b1-0,C-b3-0,C-oid-0,C-nf-0`, rule/composition/universe,
mappings/declarations, adoption, governance, and canon. Each empty subtotal
pins its own `C-*`. The B1 transition records `F-b1-1` and
`H-b1-1 ← H-b1-0`; existing individuation is `H-b1-0 → C-b1-0`, and existing
derivation is `C-b1-0 → D-b1-0 → D-2b-0` plus direct
`C-b1-0 → D-2b-0`. The old zero therefore leaves current state only through
Article 7's two edges. `C-b1-1` and explicit rerun may create `D-2b-1`; until
then the line blocks. No manual withdrawal or new standing-affecting edge is
proposed.

## Unresolved authority

The existing slice lacks adopted OID and adjustment fact taxonomy. Production
must declare that taxonomy and arithmetic before it asserts the universe is
complete. This design does not decide a reusable composition abstraction for
other lines.
