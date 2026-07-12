# Round 4 Adversary Review - Tax Citizen Families it4

Reviewer label: Harvey (`019f53df-80d1-7470-b663-cdd74a312710`)
Target: `exhibits/tax-citizen-families/it4` at `9debc4d`
Role: adversary reviewer

I read the adversary role, governance-review inputs, `charter-it4.md`,
`reviews/round-4.md`, the governance set, First Tax Slice planning inputs, the
it4 examination and exhibit, prior-round adversary material, and official IRS
sources. I did not read same-round peer reviews or commit-message bodies.

## Method and primary sources

Baseline reproduction from an archive of the tag:

```sh
git archive exhibits/tax-citizen-families/it4 | tar -x -C /tmp/tcf-it4-review
PYTHONPATH=/tmp/tcf-it4-review python3 /tmp/tcf-it4-review/docs/prototypes/tax-citizen-families/it4/tools/harness.py
PYTHONPATH=/tmp/tcf-it4-review python3 /tmp/tcf-it4-review/docs/prototypes/tax-citizen-families/it4/tools/regression.py
```

Result: the harness reported all 92 checks passing and the regression reported
all 14 scenarios passing, both exit 0. I then ran no-write mutation probes
against the extracted exhibit. Commands are summarized under the attacks; the
reported outputs are the reproducible exhibits.

Tax semantics were checked against the official [2025 Form
1040](https://www.irs.gov/pub/irs-prior/f1040--2025.pdf), [2025 Form 1040
instructions](https://www.irs.gov/pub/irs-prior/i1040gi--2025.pdf), [2025 W-2
and W-3 instructions](https://www.irs.gov/pub/irs-prior/iw2w3--2025.pdf), and
[Instructions for Forms 1099-INT and
1099-OID](https://www.irs.gov/instructions/i1099int). Relevant pressure points:
Form 1040 line 1a totals W-2 box 1 subject to stated exceptions; line 2b is
total taxable interest and is not limited to 1099-INT box 1; W-2c identifies
both previously reported and corrected values; and 1099-INT distinguishes box
1, box 3, box 8, bond-premium adjustments, and account identity.

## I1 - Authoritative materialization

**Attack 1 - fixture booleans still create authority: succeeds in part.**
`integration.py:188-197` reads `wage_closed`, `interest_closed`,
`line1_other_closed`, `std_ordinary_eligible`, and `ordinary_tax_method`
directly from the scenario and turns them into asserted findings. The runner
does consume projected findings, so the narrow I1 claim that booleans are not
passed directly into `RunContext` survives. But authority is manufactured from
the same fixture booleans one step earlier; no assertion payload or act is
independently supplied. This is especially material for eligibility and method,
where the scalar is already the tax conclusion the projection rule republishes.

**Attack 2 - actual workspace path: fails.** The ordinary positive path does use
the real `ActLog`, kernel fact lattice and finding projection, persisted
`RecordStream`, runner, publication acts, and workspace currency. Removing a
closure assertion blocks the projection rule and its dependent line. This is a
real improvement over it3's direct context construction.

## I2 - Adoption and pin integrity

**Attack 3 - package adoption is not a workspace fact: succeeds.** The only
adoption act appended is `bundle-adoption`. `run_authoritative` instead creates
`adopted = {content["package_2025"]["id"]}` in code (`integration.py:298-306`).
Thus the package's standing is asserted by the adapter, not projected from the
workspace record. The adoption pin comes from scenario provenance, and the gate
checks only its id.

Mutation command shape:

```sh
PYTHONPATH=/tmp/tcf-it4-review python3 - <<'PY'
# load w2_and_interest, change provenance.package_version to v999,
# materialize, then call run_authoritative
PY
```

Exhibit: `published=13`; the completed record carried adoption pin
`{id: us.package.f1040-first-slice.2025, version: v999}`. A nonexistent version
therefore passes the adoption gate.

**Attack 4 - same-id/same-version content substitution: succeeds.** I replaced
the value expression of `us.rule.f1040.line1a.wages` with constant 999 while
retaining rule id/version and package id/version. The ordinary path published
line 1a = 999. Its pins were indistinguishable at the identity level from the
unmodified run: package `v1` and rule `v1`. No content digest or immutable
artifact lookup closes the substitution. This defeats the claimed adoption/pin
integrity even for the symbol projections that the examination calls closed.

**Attack 5 - `closed_sets` is an unmodeled authority input: succeeds and is
admitted.** `CLOSURE_SET_2025` is a hard-coded tax map and `closed_sets` is a
bare `frozenset` assembled in `integration.py:204-276`. No adopted artifact
produces it and no resulting finding pins it. Withholding it blocks an otherwise
supported empty-set publication. I2 is therefore failed/escalated, not closed.
The scalar closure symbol does not remove this second, unpinned authority input.

## I3 - W-2 correction and displacement

**Attack 6 - same-fact correction and cascade: fails.** Two W-2 slips from the
same employer/year have distinct slip citizens and fact ids. Asserting a new
finding on the first fact displaces only its old finding, propagates
displacement to the old line 1a chain, and re-derivation publishes 47000. This
is genuine kernel/ADR-0010 behavior, not a hard-coded expected total.

**Attack 7 - corrected documentary provenance: succeeds.** The correction is a
new `documentary` finding for 35000 that cites the original evidence id
`ev:acme-ctrl-001`; no corrected/reissued evidence or replacement act is
submitted (`harness.py:176-195`). The IRS W-2c instructions require the changed
item's previously reported and correct information. Here the new amount is
documentarily attributed to evidence whose original scenario value was 30000.
The displacement mechanics work, but the correction exhibit does not prove an
honest W-2/W-2c provenance lifecycle.

## I4 - Closed package and provenance generality

**Attack 8 - package closure excludes most claimed citizen roles: succeeds.**
`package.tax-2025.json` contains only rules and parameters. It does not contain
the fact-type bundle, fact types, symbol bindings, citations, citation
attachments, form fields, citation resolver, or scenario-provenance contract.
The harness joins these from `full_content()` and bespoke sets outside
`validate_package`. Consequently there is no package-level
scenario -> package -> bundle/fact types -> bindings/citations/attachments ->
form-fields closure as claimed by I4.

**Attack 9 - later-year generality: succeeds.** The 2026 positive only calls
`validate_package` over 2026 rules and parameters. It is not adopted into a
workspace or run through materialization, bindings, citations, resolver,
records, or explanations. Several mixed-year checks are local comparisons
(`cy_ok`, regex extraction, dictionary membership), not normal package
validation. The exhibit proves selected scope checks, not a general provenance
join across every included citizen role.

## I5 - Record-derived coverage

**Attack 10 - record/publication persistence ordering: succeeds.** I replaced
the adapter's imported `append_publications` with a function that raises, then
ran the ordinary path. Output:

```text
error=simulated publication persistence failure
record_phases=['started', 'completed']
record_published=13
publication_acts=0
```

`run_and_record` writes the completion record, including its claimed published
surface, before `run_authoritative` appends publication acts
(`integration.py:303-310`). Coverage and explanations can therefore consume a
completed record that claims outputs absent from authoritative state. The
charter's required persistence ordering is not interruption-safe.

**Attack 11 - non-closure dependencies disappear: succeeds.** Coverage is a
hard-coded two-family map in `harness.py:284-296`. It reports a family `open`
only when that family's selected rule is blocked specifically on the chosen
closure symbol; every other state defaults to `closed`. Removing rounding while
keeping closure makes the output rule block on a non-closure dependency, yet
coverage still reports the family closed. It neither derives covered families
from declared package content nor represents non-closure gaps honestly.

**Attack 12 - contradictory stored projection: fails narrowly.** The supplied
stale coverage object is ignored by `coverage_from_record`; it cannot override
the selected record. That check passes, but it does not cure attacks 10-11.

## I6 - Record-grounded explanations

**Attack 13 - numeric explanation pin walk: fails.** Present zero and
closure-backed zero use real derived-finding pins. Removing the closure finding
prevents line 2b publication. Those two explanation states are grounded.

**Attack 14 - disposition walks are not walks: succeeds.** For no source/no
closure and false guard, I6 only searches a completion-record dictionary and
asserts fields (`harness.py:343-358`). It never invokes one explanation API
starting at the requested output disposition and walking through adopted rule,
projection, records, and findings. Unreached blocked dispositions produced by
the runner carry empty pins. The committed explanation examples likewise name
one expected terminal and compare it with a pin set; they do not serialize or
validate the required end-to-end walk.

**Attack 15 - invalid-source explanation: succeeds.** The invalid assertion can
be appended and fails only when projecting findings. No derivation run or
record-grounded output disposition exists, so the claimed explanation
"terminates at the kernel value_schema" is an exception observation, not a walk
beginning at a requested form/output disposition as I6 requires.

## I7 - Citation resolver semantics

**Attack 16 - attachment-controlled expectations: succeeds.** The resolver
trusts `expected.locator_kind`, `expected.locator_contains`, and
`expected.tax_year` from the attachment itself. Mutating the W-2 subject's
citation to the valid 1099-INT box-1 citation and changing the expected
substring to `Box 1` returned `(True, "ok")`. Thus a semantically false
subject-to-source relationship passes when the attachment lies consistently.

**Attack 17 - subject kind and jurisdiction: succeeds.** Changing the known W-2
fact-type subject's declared kind to `parameter` also returned `(True, "ok")`.
`resolve_attachment` pools all subject ids without checking kind, and despite
the resolver contract's prose it performs no jurisdiction comparison. The role
table constrains locator kinds, not which citations are authoritative for a
particular citizen. I7's wrong-subject negative catches one hand-selected
substring mismatch; it does not establish resolver semantics.

## I8 - Committed relationship examples

**Attack 18 - files exist, but several negatives have no rejecting authority:
succeeds.** The projection-rule negative is accepted by the published JSON
Schema and rejected only by `_refs_in`, a harness helper. The correction
negative is merely compared to a hard-coded original fact id and labeled "not a
correction"; no authority rejects it as an ordinary finding. Coverage and
explanation examples are note-bearing expected dictionaries with no citizen
schema, adoption, or normal consumer. Presence of committed files satisfies
the literal inventory, but does not satisfy I8's claim that each relationship
is checked by a real authority.

**Attack 19 - ordinary schema examples: fails.** Form-field, citation,
attachment, scenario, symbol-binding, fact-value, and package-role examples are
hand-written and reproducibly accepted/rejected by their named schema,
validator, or resolver. The attack is limited to the added relationship
examples above.

## I9 - Bypass resistance

**Attack 20 - named it3 bypass probes: fails narrowly.** Direct closure false,
withheld projection membership, unknown package id, stale coverage map, and a
fabricated explanation id do not change the supplied positive outcomes. These
specific probes reproduce.

**Attack 21 - adjacent bypasses defeat the same boundaries: succeeds.** A known
package id with bogus version passes; same-id/same-version rule substitution
changes authority while retaining pins; a consistently lying citation
attachment passes; and completion-before-publication lets the record claim
nonexistent outputs. I9 tests exact strings and selected mutations, not bypass
resistance of the authoritative components.

## Observations

1. The it4 change inventory says eligibility and method objects became one
scalar boolean, while `spikes/integration-substrate.md:44-49` says they became
five and three condition facts with an `all(not each)` projection. The code and
bundle implement the former, not the latter.
2. That scalarization loses condition identity and provenance. "Dependent,"
"age 65," "blind," "spouse itemizes," and "dual-status" collapse into one
attested eligibility conclusion; qualified-dividend/capital-gain, foreign-earned
income, and other alternate-method triggers collapse into another. A user
cannot recover which condition applied, correct one condition as the same fact,
or explain the conclusion from its constituent findings. Tax meaning moved
from declared rule structure into an attested scalar and descriptive prose.
3. The 1099-INT model keys interest by payer/year/box only. Official instructions
make account number required for multiple accounts in relevant cases and allow
different box and adjustment semantics. Multiple same-payer/year/box statements
cannot coexist as distinct facts, so the W-2 slip-identity lesson was not
generalized to the other source family.
4. The First Tax Slice's taxable-interest rule sums 1099-INT boxes 1 and 3. The
Form 1040 instructions require total taxable interest, which can include OID and
other interest and can require bond-premium/market-discount adjustments. This
is acceptable only as an explicitly bounded source-family slice; the current
closure phrase "I have no other interest income" is broader than the modeled
sources and risks authorizing a false line 2b zero/total.
5. The exhibit's governance pins say `v1`, while the ratified governance set is
identified as `v0.1`. This is another version-integrity mismatch accepted by the
ordinary path.

## Dissent

I dissent from concluding that the it4 evidence closes I1-I9 or is sufficient
to ratify the citizen-family contract.

- I2 is expressly failed for `closed_sets`, and adoption itself is hard-coded,
  version-blind, and content-substitutable.
- I4 does not package or validate the majority of the citizen roles whose join
  it claims to close.
- I5/I6 are undermined by completion-before-publication and by helper-local
  coverage/disposition interpretations.
- I7's resolver admits semantically wrong attachments when their self-declared
  expectations are internally consistent.
- The scalar eligibility and method facts discard condition structure and move
  tax meaning into attestation/prose, contrary to the prototype's purpose.

The successful same-fact displacement, real act-log projection, and numeric pin
walks are useful evidence. They do not cure these contract failures. At minimum,
the evaluation analysis should carry them as unresolved dissent; adoption/pin
integrity, publication ordering, package closure, citation relationship
authority, structured conditions, and native closure authority need another
decision or bounded proof before production adoption.
