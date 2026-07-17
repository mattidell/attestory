# Charter: Round 2 Incumbent Builder — Production Resolver (D3)

Date: 2026-07-16. First Real Return Slice, Track 0 D3. This is a bounded
Rung-2 paper/probe repair round, authorized for charter by the owner; **do not
begin work until separately dispatched.**

- **Seat:** incumbent builder, High.
- **Role separation:** build, do not review. You may read the Round-1 evidence
  and both committee reviews; do not contact the Round-2 rival or inspect its
  work before the foreman takes custody.
- **Question:** can one production resolution contract preserve ADR-0027 d7 and
  ADR-0028 byte-verification beyond `L` while closing every Round-1 blocker?

## Read on dispatch

`SEAT.md`, `plan.md`, `process-log.md`, both Round-1 charters, examinations,
and reviews; ADR-0027, ADR-0028, ADR-0031, ADR-0032; and the committed loader,
validator, runner, and publication registry surfaces named by the reviews.

## Build

Design a source-neutral, registry-anchored production resolver. It must declare
the current package-selection/adoption act as a versioned, Article-4-shaped
carrier (actor, scope, provenance, exact package pin, and immutable public
trust-anchor/release pin); an `L` catalog may locate bytes but never authenticate
publication. Resolve only package pins after registry verification, require
package + member checksum verification and `validation.ok == True` before a
graph exists, and keep co-located files unreadable/inert.

Publish an explicit D3-P2 matrix accounting for every ADR-0027 Decisions 1–7
and PC1–PC4 plus ADR-0028 Decisions 1–9 and PC1–PC3: discharged contract,
carried production condition, deferred-with-reason, or N/A. Embedded
schema-byte checksums remain rejected, not deferred. Do not silently turn D1
wall or D2 marshal-only installation into a D3 discharge.

Exercise synthetic scratch-`L` probes for: clean parity; unpinned/co-located
inertness; package/member mismatch and recomputed-checksum rewrite; incumbent
catalog substitution against the immutable registry; an undeclared or stale
adoption carrier; missing ratified member; complete ledger enumeration; and the
strict gate on one clean package and the current core package's **eight**
contained issues. Show a clean package does not over-fire; name RG-1 repairs as
MUST production conditions rather than applying leniency.

## Evidence boundary and outputs

All inputs are synthetic. Use a scratch out-of-repo `L`; no real workspace,
values, locators, code, schemas, or production resolver implementation may be
committed. Write only `it3/design.md` (≤300 lines) and `examination-it3.md`
(≤120 lines). The examination maps claim → probe → observed outcome and names
unresolved questions. Stop after those documents; do not review, commit, or
change any other file.

## Stop conditions

Stop and report if closing a finding needs a new boundary beyond D3, an actual
ADR-0031/D2 implementation claim, a weaker validation gate, or evidence above
Rung 2. The foreman alone takes custody and schedules review.
